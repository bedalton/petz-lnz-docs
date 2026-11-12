"""NATIVE-002: old/capture-time saves with crossed age and fatness controls.

Reads game files without modification. Derived PNGs/metadata remain in scratch.
Neither the stock poses nor yaw values are claimed to match a native capture.
"""
import argparse
import asyncio
import base64
from dataclasses import asdict, fields
import json
from pathlib import Path
import subprocess
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image, ImageDraw
from petz_renderer.formats.pet import read_saved_appearance
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT, digest, provenance
from young_endpoint_attribution import difference, sig

OUT = ROOT / 'scratch/research/native-002'
MANIFEST = ROOT / 'experiments/native-002.json'
CAPTURES = {
    'Fuzzkin': 'Fuzzkin-walkaround.pet',
    'Goobe': 'dogz/great-dane/Goobe--2026-11-12-645.pet',
    'Homebody': 'catz/Homebody.pet',
}
POSES = ('standing', 'sitting', 'lying')
YAWS = tuple(range(0, 360, 45))


def changed(a, b):
    return [f.name for f in fields(a) if getattr(a, f.name) != getattr(b, f.name)]


def save_bytes(path, data, verify):
    if verify:
        assert path.read_bytes() == data, path
    else:
        path.write_bytes(data)


def sheets(report):
    """Unscaled previews: comparison aids, not native-game alignment."""
    for name in CAPTURES:
        selected = [r for r in report['renders'] if r['name'] == name and
                    r['source'] == 'capture' and r['yaw_degrees'] in (0, 90, 180, 270)]
        w = max(r['size'][0] for r in selected) + 24
        h = max(r['size'][1] for r in selected) + 42
        sheet = Image.new('RGB', (w * 4, h * 12), '#dedede')
        draw = ImageDraw.Draw(sheet)
        for r in selected:
            row = POSES.index(r['pose']) * 4 + r['age_side'] * 2 + r['fatness_side']
            col = (0, 90, 180, 270).index(r['yaw_degrees'])
            im = Image.open(OUT / r['file']).convert('RGBA')
            x, y = col * w, row * h
            sheet.paste(im, (x + (w-im.width)//2, y+30), im)
            draw.text((x+5, y+3), f"{r['pose']} yaw{r['yaw_degrees']} age{r['age']} fat{r['fatness']}", fill='black')
        sheet.save(OUT / f'{name}-controls.png')


async def run(verify):
    old = json.loads(MANIFEST.read_text()) if verify else None
    if not verify:
        OUT.mkdir(parents=True, exist_ok=False)
    resolver = ResourceResolver((ROOT/'games/petz4', ROOT/'scratch/screenshots'))
    report = {
        'experiment': 'NATIVE-002', 'provenance': provenance(),
        'backend': 'installed direct API; fresh local stdio MCP endpoint controls',
        'script_sha256': digest(Path(__file__).read_bytes()),
        'intake_sha256': digest((ROOT/'scratch/research/native-001/inventory.json').read_bytes()),
        'controls': {'look': 'age', 'poses': POSES, 'yaw_degrees': YAWS,
                     'raster_seed': 1, 'line_seed': 1, 'step': 0,
                     'claim_scope': 'Renderer controls only; no native pixel alignment or clothing simulation'},
        'inputs': [], 'renders': [], 'comparisons': [], 'mcp': [],
    }
    endpoints = {}
    for name, capture_path in CAPTURES.items():
        paths = {'prior': f'Adopted Petz/{name}.pet', 'capture': capture_path}
        physical = {'prior': ROOT/'games/petz4'/paths['prior'],
                    'capture': ROOT/'scratch/screenshots'/capture_path}
        raw = {k: p.read_bytes() for k, p in physical.items()}
        pets = {k: read_saved_appearance(v) for k, v in raw.items()}
        defaults = {k: load_saved_assets(resolver, p, pose='standing') for k, p in paths.items()}
        ages = [defaults[k].preview.age for k in paths]
        fats = [defaults[k].preview.fatness for k in paths]
        assert pets['prior'].adult_cache == pets['capture'].adult_cache
        assert pets['prior'].young_cache == pets['capture'].young_cache
        source = {'name': name, 'paths': {k: str(p.relative_to(ROOT)) for k,p in physical.items()},
                  'sha256_by_source': {k: digest(v) for k,v in raw.items()},
                  'cache_equal': True, 'ages': ages, 'fatnesses': fats,
                  'default_asset_changes': changed(defaults['prior'], defaults['capture']),
                  'default_appearance_changes': changed(defaults['prior'].appearance, defaults['capture'].appearance),
                  'cache_hashes': {k: digest(getattr(pets['prior'], k)) for k in ('adult_cache', 'young_cache')},
                  'default_previews': {k: asdict(v.preview) for k,v in defaults.items()},
                  'dependencies': [asdict(u) for u in defaults['capture'].provenance]}
        report['inputs'].append(source)
        for pose in POSES:
            assets = {}
            for ai, age in enumerate(ages):
                for fi, fat in enumerate(fats):
                    pair = {k: load_saved_assets(resolver, p, pose=pose, age=age, fatness=fat)
                            for k,p in paths.items()}
                    assert set(changed(pair['prior'], pair['capture'])) <= {'preview', 'diagnostics'}
                    assets[ai,fi] = pair
            for degrees in YAWS:
                outputs = {}
                for (ai, fi), pair in assets.items():
                    for side, asset in pair.items():
                        result = render_portrait(asset, yaw=degrees*256//360)
                        outputs[side,ai,fi] = result
                        file = f'{name}-{side}-{pose}-{degrees}-a{ai}-f{fi}.png'
                        save_bytes(OUT/file, result.png, verify)
                        report['renders'].append({
                            'name': name, 'source': side, 'pose': pose, 'yaw_degrees': degrees,
                            'age_side': ai, 'fatness_side': fi, 'age': ages[ai], 'fatness': fats[fi],
                            'file': file, 'png_sha256': digest(result.png),
                            'indexed_sha256': digest(result.indices), 'size': [result.width,result.height],
                            'offset': list(result.offset)})
                for ai in range(2):
                    for fi in range(2):
                        a,b = outputs['prior',ai,fi],outputs['capture',ai,fi]
                        assert sig(a) == sig(b) and a.prepared == b.prepared and a.indices == b.indices
                a,b,c,d = [outputs['capture',ai,fi] for ai,fi in ((0,0),(1,0),(0,1),(1,1))]
                report['comparisons'].append({'name': name,'pose':pose,'yaw_degrees':degrees,
                    'source_equal_at_all_four_controls': True,
                    'default_pixels': difference(a,d), 'age_only_pixels': difference(a,b),
                    'fatness_only_pixels': difference(a,c),
                    'new_age_fatness_pixels': difference(b,d),
                    'new_fatness_age_pixels': difference(c,d)})
                if degrees in (0,90):
                    for side,ai,fi in (('prior',0,0),('capture',1,1)):
                        direct = render_portrait(load_saved_assets(resolver, paths[side], pose=pose),
                                                 yaw=degrees*256//360)
                        assert sig(direct) == sig(outputs[side,ai,fi])
                        endpoints[name,side,pose,degrees] = direct.png
            print(f'{name}/{pose}: 64 crossed-control images pass', flush=True)
        for k,p in physical.items():
            assert p.read_bytes() == raw[k]
    transport = StdioTransport(sys.executable, ['-I','-m','petz_renderer.service.local_mcp',
        '--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/screenshots')])
    async with Client(transport) as client:
        assert len(await client.list_tools()) == 6
        caps = await client.call_tool('get_capabilities')
        assert not caps.is_error
        save_bytes(OUT/'capabilities.json', (json.dumps(caps.data,indent=2)+'\n').encode(), verify)
        for name, capture in CAPTURES.items():
            for side,path in (('prior',f'Adopted Petz/{name}.pet'),('capture',capture)):
                for pose in POSES:
                    for degrees in (0,90):
                        controls = {'path':path,'pose':pose,'yaw_degrees':degrees}
                        response = await client.call_tool('render_pet',controls)
                        assert not response.is_error
                        png = base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                        assert png == endpoints[name,side,pose,degrees]
                        file = f'{name}-{side}-{pose}-{degrees}-mcp.json'
                        save_bytes(OUT/file,(json.dumps(response.data,indent=2)+'\n').encode(),verify)
                        report['mcp'].append({'name':name,'source':side,'controls':controls,
                                              'png_sha256':digest(png),'metadata':file})
    originals = json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True))
    assert all(r['ok'] for r in originals['checks'])
    report['original_checks'] = originals['checks']
    report['summary'] = {'direct_pngs': len(report['renders']), 'mcp_matches': len(report['mcp']),
                         'source_equalities': 3*3*8*4,
                         'per_pet': {name: {'views':24, **{key:sum(r[key]>0 for r in report['comparisons'] if r['name']==name)
                            for key in ('default_pixels','age_only_pixels','fatness_only_pixels')}} for name in CAPTURES}}
    report = json.loads(json.dumps(report))
    if verify:
        assert report == old
        print('FULL REPLAY PASS', flush=True)
    else:
        for path in (MANIFEST,OUT/'report.json'):
            path.write_text(json.dumps(report,indent=2)+'\n')
        sheets(report)
    print(json.dumps(report['summary'],indent=2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify',action='store_true')
    asyncio.run(run(parser.parse_args().verify))
