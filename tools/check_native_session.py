"""Verify native continuation links, retained evidence and local HTTP endpoints."""
import asyncio
import base64
import json
from pathlib import Path
import subprocess
import sys
from fastmcp import Client
from young_breed_probe import ROOT, digest, provenance

OUT = ROOT/'scratch/research/native-session'


async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifests = {n:json.loads((ROOT/f'experiments/native-{n:03d}.json').read_text()) for n in (2,3,4)}
    hashes = {str(n):digest((ROOT/f'experiments/native-{n:03d}.json').read_bytes()) for n in manifests}
    assert manifests[2]['provenance'] == provenance()
    assert manifests[4]['grid_manifest_sha256'] == hashes['3']
    assert manifests[4]['renderer_reference']['manifest_sha256'] == hashes['2']
    result = {'script_sha256':digest(Path(__file__).read_bytes()),'manifest_hashes':hashes,
              'replays':{},'audits':{},'http':[],'source_count':len(manifests[2]['provenance']['sources'])}
    audit_scripts = {2:'check_native_saved_controls.py',3:'check_native_pixel_grid.py',
                     4:'check_native_colour_profiles.py'}
    artifacts = 0
    for n in manifests:
        replay = ROOT/f'scratch/native-{n:03d}-replay.log'
        assert 'FULL REPLAY PASS' in replay.read_text()
        result['replays'][str(n)] = {'path':str(replay.relative_to(ROOT)),'sha256':digest(replay.read_bytes())}
        audit_path = ROOT/f'scratch/research/native-{n:03d}/independent-audit.json'
        audit = json.loads(audit_path.read_text())
        assert audit['manifest_sha256'] == hashes[str(n)]
        assert audit['script_sha256'] == digest((ROOT/'tools'/audit_scripts[n]).read_bytes())
        result['audits'][str(n)] = {'path':str(audit_path.relative_to(ROOT)),
                                    'sha256':digest(audit_path.read_bytes())}
    for row in manifests[2]['renders']:
        assert digest((ROOT/'scratch/research/native-002'/row['file']).read_bytes()) == row['png_sha256']
        artifacts += 1
    for row in manifests[3]['stills']:
        assert digest((ROOT/'scratch/research/native-003'/row['file']).read_bytes()) == row['png_sha256']
        artifacts += 1
    for row in manifests[4]['stills']:
        for file_key,hash_key in (('file_tagged','tagged_png_sha256'),('file_srgb','srgb_png_sha256')):
            assert digest((ROOT/'scratch/research/native-004'/row[file_key]).read_bytes()) == row[hash_key]
            artifacts += 1
    intake = json.loads((ROOT/'scratch/research/native-001/inventory.json').read_text())
    for row in intake['inputs']:
        assert digest((ROOT/row['path']).read_bytes()) == row['sha256']
    originals = json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True))
    assert all(r['ok'] for r in originals['checks'])
    result['originals'] = originals['checks']
    result['intake_files'] = len(intake['inputs'])
    result['hashed_pngs'] = artifacts
    async with Client('http://127.0.0.1:8765/mcp') as client:
        names = sorted(t.name for t in await client.list_tools());assert len(names)==6
        result['http_tools'] = names
        caps = await client.call_tool('get_capabilities');assert not caps.is_error
        (OUT/'http-capabilities.json').write_text(json.dumps(caps.data,indent=2)+'\n')
        for source in manifests[2]['inputs']:
            path = source['paths']['capture'].removeprefix('scratch/screenshots/')
            for degrees in (0,90):
                controls = {'path':path,'pose':'standing','yaw_degrees':degrees}
                response = await client.call_tool('render_pet',controls);assert not response.is_error
                png = base64.b64decode(next(x.data for x in response.content if x.type=='image'))
                row = next(r for r in manifests[2]['renders'] if
                           (r['name'],r['source'],r['pose'],r['yaw_degrees'],r['age_side'],r['fatness_side']) ==
                           (source['name'],'capture','standing',degrees,1,1))
                assert digest(png) == row['png_sha256']
                assert response.data['appearance']['age_source'] == 'saved'
                assert response.data['appearance']['fatness_source'] == 'saved'
                result['http'].append({'controls':controls,'png_sha256':digest(png)})
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in
                     ('source_count','intake_files','hashed_pngs','manifest_hashes')},indent=2))
    print(f"NATIVE SESSION PASS: {len(result['http'])} HTTP renders, {len(result['originals'])} originals")


if __name__ == '__main__':
    asyncio.run(main())
