"""Cross-unit PAINT-005/006/007 evidence audit after full unit replays."""
import asyncio
import base64
from io import BytesIO
import json
from pathlib import Path
import subprocess
from fastmcp import Client
from PIL import Image
from research_common import ROOT,SHA
from saved_colour_arrays import provenance


def main():
    reports={u:json.loads((ROOT/f'experiments/{u}.json').read_text()) for u in ('paint-005','paint-006','paint-007')}
    prov=provenance();revision=subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip()
    assert revision==prov['renderer_revision']
    pngs={};metadata={};sheets={};rgba_checks=0;copies={};originals={};manifests={}
    def check_png(folder,row):
        p=folder/row['png'];assert SHA(p.read_bytes())==row['png_sha256'];pngs[str(p.relative_to(ROOT))]=row['png_sha256']
        with Image.open(p) as im:rgba=im.convert('RGBA');raw=rgba.tobytes()
        if 'rgba_sha256' in row:assert SHA(raw)==row['rgba_sha256']
        return rgba
    for unit,r in reports.items():
        folder=ROOT/'scratch/research'/unit;assert r==json.loads((folder/'report.json').read_text())
        assert r['provenance']==prov
        manifests[unit]=SHA((ROOT/f'experiments/{unit}.json').read_bytes())
        for s in r.get('sources',[]):
            p=ROOT/'games/petz4'/s['path'];assert SHA(p.read_bytes())==s['sha256'];originals[str(p.relative_to(ROOT))]=s['sha256']
            for v in s['variants']:
                p=folder/v['path'];assert SHA(p.read_bytes())==v['sha256'];copies[str(p.relative_to(ROOT))]=v['sha256']
        for c in r['cases']:
            if unit=='paint-005':check_png(folder,c);continue
            cells={name:check_png(folder,row) for name,row in c['outputs'].items()}
            first=cells['baseline'].tobytes()
            for name,im in cells.items():
                raw=im.tobytes();assert len(raw)==len(first)
                changed=sum(raw[i:i+4]!=first[i:i+4] for i in range(0,len(raw),4))
                assert changed==c['outputs'][name]['rgba_changed'];rgba_checks+=1
                if name.startswith('group'):assert raw==first
            if 'sheet' in c:
                p=folder/c['sheet'];assert SHA(p.read_bytes())==c['sheet_sha256'];pngs[str(p.relative_to(ROOT))]=c['sheet_sha256']
                sheet=Image.open(p).convert('RGBA');w,h=c['cell_size'];assert sheet.size==(4*w,h)
                for i,name in enumerate(c['cell_order']):assert sheet.crop((i*w,0,(i+1)*w,h)).tobytes()==cells[name].tobytes()
                sheets[p.name]=SHA(p.read_bytes())
        for row in r['mcp']:
            im=check_png(folder,row);p=folder/row['metadata'];raw=p.read_bytes();meta=json.loads(raw)
            assert meta['game_version']=='petz4' and meta['png_sha256']==row['png_sha256']
            assert [meta['width'],meta['height']]==list(im.size)
            controls=row['controls'];input_path=ROOT/'games/petz4'/controls['path']
            if not input_path.exists():input_path=(ROOT/'scratch/research/paint-006' if unit=='paint-007' else folder)/controls['path']
            assert meta['appearance']['input_sha256']==SHA(input_path.read_bytes())
            assert meta['pose']['name']==controls['pose']
            assert meta['camera']['requested_degrees']==controls['yaw_degrees']
            if 'age' in controls:assert meta['appearance']['age']==controls['age']
            assert meta['appearance']['age_source']==('override' if unit=='paint-007' else 'saved')
            assert meta['appearance']['seed_source']=='saved' and meta['appearance']['fatness_source']=='saved'
            if 'group0' in row['controls']['path']:assert not any(d['code']=='unsupported_paint_fields' for d in meta['diagnostics'])
            if 'group1' in row['controls']['path']:assert any(d['code']=='unsupported_paint_fields' for d in meta['diagnostics'])
            metadata[str(p.relative_to(ROOT))]=SHA(raw)
        assert {str(p.relative_to(ROOT)) for p in folder.glob('*.png')}=={p for p in pngs if p.startswith(str(folder.relative_to(ROOT))+'/')}
    links=0
    for c in reports['paint-006']['cases']:
        old=next(o for o in reports['paint-005']['cases'] if o['name']==c['name'] and o['mode']=='all' and o['pose']==c['pose'] and o['yaw']==c['yaw'])
        assert old['png_sha256']==c['outputs']['baseline']['png_sha256'];links+=1
    assert len(pngs)==298 and len(metadata)==64 and len(copies)==21 and links==18 and len(sheets)==18
    restore=json.loads((ROOT/'experiments/restore-002.json').read_text())
    for version,engines in restore['shared_engine_hashes'].items():
        paths={str(p.relative_to(ROOT/'games'/version)).lower():p for p in (ROOT/'games'/version).rglob('*') if p.is_file()}
        for name,digest in engines.items():
            p=paths[name];assert SHA(p.read_bytes())==digest;originals[str(p.relative_to(ROOT))]=digest
    for row in restore['results']:
        p=ROOT/'games'/row['version']/row['path'];assert SHA(p.read_bytes())==row['input_sha256'];originals[str(p.relative_to(ROOT))]=row['input_sha256']
    unit_logs={}
    for unit in reports:
        p=ROOT/'scratch'/f'{unit}-verify.log';raw=p.read_bytes();assert f'{unit.upper()} verified' in raw.decode()
        unit_logs[unit]=SHA(raw)
    tools=('saved_colour_arrays.py','saved_paint_groups.py','paint_group_ages.py','check_paint_group_session.py')
    result={'renderer_revision':revision,'manifest_hashes':manifests,'png_count':len(pngs),'metadata_count':len(metadata),
        'copy_count':len(copies),'original_file_hash_links':len(originals),'cross_unit_png_links':links,
        'decoded_rgba_difference_checks':rgba_checks,'sheets_checked':len(sheets),
        'reviewed_sheets':[f'{name}-standing-{yaw}-sheet.png' for name in ('Fuzzkin','Homebody','Goobe') for yaw in (0,64)],
        'tool_hashes':{p:SHA((ROOT/'tools'/p).read_bytes()) for p in tools},
        'png_hashes':pngs,'metadata_hashes':metadata,'copy_hashes':copies,'original_hashes':originals,
        'unit_replay_log_hashes':unit_logs,'source_files':len(prov['source_hashes']),'direct_draws':288,'research_mcp_views':64,
        'scope':'Aggregate integrity; unit --verify commands execute complete copy/load/render replays.'}
    (ROOT/'scratch/research/paint-group-session-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not k.endswith('_hashes')}))


async def health():
    async with Client('http://127.0.0.1:8765/mcp') as client:
        tools=await client.list_tools();result=await client.call_tool('get_capabilities',{})
        assert not result.is_error and len(tools)==6
        control=await client.call_tool('render_pet',{'path':'Adopted Petz/Fuzzkin.pet','pose':'standing','yaw_degrees':0})
        assert not control.is_error
        png=base64.b64decode(next(c.data for c in control.content if c.type=='image'))
        report=json.loads((ROOT/'experiments/paint-005.json').read_text())
        reference=next(c for c in report['cases'] if c['name']=='Fuzzkin' and c['mode']=='all' and c['pose']=='standing' and c['yaw']==0)
        assert SHA(png)==reference['png_sha256']
        (ROOT/'scratch/research/paint-group-session-http-control.png').write_bytes(png)
        record={'control_png_sha256':SHA(png),'control_metadata':control.data,'endpoint':'http://127.0.0.1:8765/mcp','tools':[t.name for t in tools],'capabilities':result.data}
        (ROOT/'scratch/research/paint-group-session-health.json').write_text(json.dumps(record,indent=2)+'\n')
    print('Local HTTP MCP discovery/capabilities passed')

if __name__=='__main__':main();asyncio.run(health())
