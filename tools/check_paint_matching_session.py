"""Audit PAINT-008/009/010 copies, image evidence, metadata, and prior links."""
import asyncio
import base64
from io import BytesIO
import json
import subprocess
from fastmcp import Client
from PIL import Image
from research_common import ROOT,SHA
from saved_colour_arrays import provenance
from saved_paint_age_matching import GAME,SOURCE

RESEARCH=ROOT/'scratch/research';REVIEW=RESEARCH/'paint-matching-review'


def main():
    prov=provenance();head=subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip()
    assert prov['renderer_revision']==head
    units=('paint-008','paint-009','paint-010')
    reports={u:json.loads((ROOT/f'experiments/{u}.json').read_text()) for u in units}
    pngs={};metadata={};copies={};logs={};review={};rgba_checks=0;links=0;states={}
    prior7=json.loads((ROOT/'experiments/paint-007.json').read_text())
    prior1=json.loads((ROOT/'experiments/paint-001.json').read_text())
    REVIEW.mkdir(parents=True,exist_ok=True)
    def check(folder,row):
        path=folder/row['png'];raw=path.read_bytes();assert SHA(raw)==row['png_sha256'];pngs[str(path.relative_to(ROOT))]=SHA(raw)
        im=Image.open(BytesIO(raw)).convert('RGBA')
        if 'rgba_sha256' in row:assert SHA(im.tobytes())==row['rgba_sha256']
        return im
    def diff(a,b):
        nonlocal rgba_checks
        assert a.size==b.size;rgba_checks+=1;x,y=a.tobytes(),b.tobytes()
        return sum(x[i:i+4]!=y[i:i+4] for i in range(0,len(x),4))
    def sheet(name,cells):
        w,h=cells[0].size;assert all(c.size==(w,h) for c in cells)
        out=Image.new('RGBA',(w*len(cells),h))
        for i,im in enumerate(cells):out.paste(im,(w*i,0))
        path=REVIEW/name;out.save(path);review[name]=SHA(path.read_bytes())
    for unit,r in reports.items():
        folder=RESEARCH/unit;assert r==json.loads((folder/'report.json').read_text()) and r['provenance']==prov
        log=(ROOT/'scratch'/f'{unit}-verify.log').read_bytes();assert f'{unit.upper()} verified' in log.decode();logs[unit]=SHA(log)
        for v in r.get('source',{}).get('variants',{}).values():
            p=folder/v['path'];digest=SHA(p.read_bytes());assert digest==v.get('sha256',v.get('file_sha256'));copies[str(p.relative_to(ROOT))]=digest
        for c in r['cases']:
            cells={name:check(folder,row) for name,row in c['outputs'].items()}
            if unit=='paint-008':
                for mode,row in c['outputs'].items():assert diff(cells['baseline'],cells[mode])==row['rgba_changed']
                if c['age'] in (0,50,100):
                    prior=next(x for x in prior7['cases'] if (x['age'],x['pose'],x['yaw'])==(c['age'],c['pose'],c['yaw']))
                    assert prior['outputs']['baseline']['png_sha256']==c['outputs']['baseline']['png_sha256'];links+=1
                if c['age'] in (0,50) and c['pose']=='standing':
                    sheet(f"008-{c['age']}-{c['yaw']}.png",[cells[k] for k in ('baseline','young-color','adult-color','young-size','young-size-drop','young-reorder')])
            elif unit=='paint-009':
                prior=next(x for x in prior1['cases'] if x['folder']==c['prior_folder'])
                assert prior['outputs']['all_texture_only']['png_sha256']==c['outputs']['original_actual']['png_sha256'];links+=1
                path=RESEARCH/'paint-001'/c['prior_folder']/'states.json';digest=SHA(path.read_bytes())
                assert digest==c['state_sha256']==prior['private_states_sha256'];states[c['prior_folder']]=digest
                assert diff(cells['reordered_actual'],cells['reordered_actual_remap'])==0
                assert diff(cells['original_actual'],cells['reordered_actual'])==c['actual_order_only_rgba_changed']
                assert diff(cells['reordered_tagged_stale'],cells['reordered_tagged_remap'])==c['tagged_stale_remap_rgba_changed']
                if c is max(r['cases'],key=lambda x:x['tagged_stale_remap_rgba_changed']):
                    sheet('009-largest-angle-difference.png',[cells[k] for k in ('reordered_tagged_stale','reordered_tagged_remap')])
            else:
                for mode in ('surface','nonsurface'):
                    assert diff(cells['matched-'+mode],cells['opposed-'+mode])==c['opposed_changed_rgba'][mode]==0
                if c['age']==56:sheet(f"010-midpoint-{c['yaw']}.png",[cells[k] for k in ('matched-surface','opposed-surface','matched-nonsurface','opposed-nonsurface')])
        for m in r.get('mcp',[]):
            im=check(folder,m);path=folder/m['metadata'];raw=path.read_bytes();meta=json.loads(raw);args=m['controls']
            assert meta['game_version']=='petz4' and meta['png_sha256']==m['png_sha256']
            assert (meta['width'],meta['height'])==im.size
            assert meta['pose']['name']==args['pose'] and meta['camera']['requested_degrees']==args['yaw_degrees']
            a=meta['appearance'];input_path=GAME/SOURCE if args['path']==SOURCE else folder/args['path']
            assert a['input_sha256']==SHA(input_path.read_bytes()) and a['age']==args['age']
            assert a['age_source']=='override' and a['seed_source']==a['fatness_source']=='saved'
            metadata[str(path.relative_to(ROOT))]=SHA(raw)
        assert {str(p.relative_to(ROOT)) for p in folder.glob('*.png')}=={p for p in pngs if p.startswith(str(folder.relative_to(ROOT))+'/')}
    previous=json.loads((RESEARCH/'paint-group-session-verification.json').read_text())
    originals=previous['original_hashes']
    for name,digest in originals.items():assert SHA((ROOT/name).read_bytes())==digest
    for unit in ('paint-008','paint-010'):assert reports[unit]['source']['original_sha256']==originals[str((GAME/SOURCE).relative_to(ROOT))]
    assert (len(pngs),len(metadata),len(copies),links,len(states),rgba_checks,len(review),len(originals))==(412,44,9,42,24,304,7,21)
    tools=('saved_paint_age_matching.py','paint_state_reordering.py','paint_direction_midpoint.py','check_paint_matching_session.py')
    result={'revision':head,'source_files':len(prov['source_hashes']),'research_pngs':len(pngs),'direct_draws':368,
        'mcp_metadata_records':len(metadata),'copies':len(copies),'original_hash_links':len(originals),
        'prior_png_links':links,'prior_state_links':len(states),'rgba_difference_checks':rgba_checks,'review_sheets':review,
        'tool_hashes':{t:SHA((ROOT/'tools'/t).read_bytes()) for t in tools},'unit_replay_log_hashes':logs,
        'manifest_hashes':{u:SHA((ROOT/f'experiments/{u}.json').read_bytes()) for u in units},
        'png_hashes':pngs,'metadata_hashes':metadata,'copy_hashes':copies,'original_hashes':originals,'state_hashes':states}
    (RESEARCH/'paint-matching-session-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not k.endswith('_hashes')}),flush=True)


async def health():
    async with Client('http://127.0.0.1:8765/mcp') as client:
        tools=await client.list_tools();caps=await client.call_tool('get_capabilities',{})
        result=await client.call_tool('render_pet',{'path':SOURCE,'pose':'standing','yaw_degrees':0})
        assert not caps.is_error and not result.is_error and len(tools)==6
        raw=base64.b64decode(next(c.data for c in result.content if c.type=='image'))
        old=json.loads((RESEARCH/'paint-group-session-health.json').read_text());assert SHA(raw)==old['control_png_sha256']
        record={'tools':[t.name for t in tools],'capabilities':caps.data,'control_png_sha256':SHA(raw),'control_metadata':result.data}
        (RESEARCH/'paint-matching-session-health.json').write_text(json.dumps(record,indent=2)+'\n')
    print('HTTP capabilities and actual baseline render pass',flush=True)

if __name__=='__main__':main();asyncio.run(health())
