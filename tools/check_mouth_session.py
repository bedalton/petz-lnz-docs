"""Aggregate immutable evidence and fresh local MCP controls for mouth session."""
import asyncio,base64,hashlib,json,subprocess,sys
from pathlib import Path
import petz_renderer
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/research/mouth-session-2026-11-15'

def sha(data):return hashlib.sha256(data).hexdigest()

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    units={name:json.loads((ROOT/f'experiments/{name}.json').read_text()) for name in ('face-001','face-002','mouth-001','mouth-002')}
    hashes={};copies={};inputs={};reports={};tools={};geometry=0;mcp=0
    for name,unit in units.items():
        path=ROOT/unit['report_path'];assert sha(path.read_bytes())==unit['report_sha256']
        verification=ROOT/unit['verification_path'];assert sha(verification.read_bytes())==unit['verification_sha256']
        report=json.loads(path.read_text());reports[name]=report
        assert report['revision']==units['face-001']['revision']
        geometry+=len(report['geometry']);mcp+=len(report['renders'])
        for p,h in report['input_hashes'].items():
            if p in inputs:assert inputs[p]==h
            inputs[p]=h
        for p,h in report['copy_hashes'].items():
            if p in copies:assert copies[p]==h
            copies[p]=h
        folder=path.parent
        for row in report['renders']+report.get('sheets',[]):
            p=folder/row['file'];assert sha(p.read_bytes())==row['sha256'];hashes[str(p.relative_to(ROOT))]=row['sha256']
        for field in ('script_sha256','helper_sha256','inventory_script_sha256'):
            if field in unit:tools[f'{name}:{field}']=unit[field]
    for p,h in {**inputs,**copies}.items():assert sha((ROOT/p).read_bytes())==h,p
    package=Path(petz_renderer.__file__).parent
    sources={str(p.relative_to(package)):sha(p.read_bytes()) for p in package.rglob('*.py')}
    checkout=ROOT/'petz-renderer-mcp/src/petz_renderer'
    assert sources=={str(p.relative_to(checkout)):sha(p.read_bytes()) for p in checkout.rglob('*.py')}
    for r in reports.values():assert r.get('sources',r.get('runtime',{}).get('sources'))==sources
    originals=json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True))
    assert len(originals['checks'])==21 and all(x['ok'] for x in originals['checks'])
    fresh=[]
    for version in ('petz3','petz4','petz5'):
        assets=ROOT/f'scratch/research/face-002/{version}'
        transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/f'games/{version}'),'--game-version',version,'--asset-root',str(assets)])
        async with Client(transport) as client:
            discovery=await client.list_tools();assert len(discovery)==6
            for species in ('Dogz','Catz'):
                r=next(x for x in reports['face-002']['renders'] if (x['version'],x['species'],x['look'],x['args']['pose'],x['args']['yaw_degrees'],x['variant'])==(version,species,'adult','standing',0,'source'))
                response=await client.call_tool('render_pet',r['args']);assert not response.is_error
                png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                assert sha(png)==r['sha256']
                fresh.append({'version':version,'species':species,'controls':r['args'],'png_sha256':sha(png),'matches_retained':True})
    result={'revision':units['face-001']['revision'],'backend':'fresh local stdio MCP, three explicit game versions',
       'unit_manifests':{name:sha((ROOT/f'experiments/{name}.json').read_bytes()) for name in units},
       'png_hashes':hashes,'input_hashes':inputs,'copy_hashes':copies,'geometry_records':geometry,'initial_mcp_renders':mcp,
       'sources':sources,'originals':originals,'fresh_mcp':fresh,'script_sha256':sha(Path(__file__).read_bytes()),
       'tool_hashes':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in (ROOT/'tools').glob('*.py') if p.name in ('face_extension_probe.py','face_extension_versions.py','mouth_frame_inventory.py','mouth_frame_probe.py','mouth_detail_probe.py','check_face_extension.py','check_face_versions.py','check_mouth_frames.py','check_mouth_details.py','check_mouth_session.py','native_anatomy_probe.py')}}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',len(hashes),'PNG hashes;',geometry,'geometry records;',mcp,'initial MCP renders;',len(copies),'copies;',len(inputs),'inputs;21 recorded originals;62 sources;six fresh MCP matches')

if __name__=='__main__':asyncio.run(main())
