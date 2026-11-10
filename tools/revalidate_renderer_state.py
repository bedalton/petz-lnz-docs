"""UPDATE-002: rebuilt eye controls and retained-state studies on the updated renderer."""
import asyncio,json,sys,subprocess
from contextlib import contextmanager
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
import eye_color_probe,eye_omission_probe,texture_motion_history
from shade_slope_probe import numerical
from shade_history_probe import compose,HISTORIES
from shade_omission_probe import scan,composition
from research_common import ROOT,SHA,save_result
OUT=ROOT/'scratch/research/update-002'
REV=subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip()

@contextmanager
def redirected_reports(folder):
    original=Path.write_text
    def write(path,data,*args,**kwargs):
        target=path
        if path.parent==ROOT/'experiments':target=folder/'report.json'
        if target==folder/'report.json':
            obj=json.loads(data);obj['previous_report_renderer_revision']=obj.get('renderer_revision');obj['renderer_revision']=REV;data=json.dumps(obj,indent=2)+'\n'
        return original(target,data,*args,**kwargs)
    Path.write_text=write
    try:yield
    finally:Path.write_text=original

async def main():
    OUT.mkdir(parents=True,exist_ok=False);eye=[]
    eye_color_probe.OUT=OUT/'eye-001'
    with redirected_reports(eye_color_probe.OUT):await eye_color_probe.main()
    old=json.loads((ROOT/'experiments/eye-001.json').read_text());new=json.loads((eye_color_probe.OUT/'report.json').read_text())
    assert all(n['input_hashes']==o['input_hashes'] for n,o in zip(new['cases'],old['cases'],strict=True))
    eye.append({'experiment':'eye-001','rebuilt_copies':10,'mcp_pairs':len(new['comparisons']),'confirmed_all_edits_change_pixels':all(r['cell_hashes'][0]!=r['cell_hashes'][1] for r in new['comparisons']),'pixel_drift':sum(n['cell_hashes']!=o['cell_hashes'] for n,o in zip(new['comparisons'],old['comparisons'],strict=True))})
    eye_omission_probe.OUT=OUT/'eye-002';eye_omission_probe.OUT.mkdir()
    cases=eye_omission_probe.prepare();old=json.loads((ROOT/'experiments/eye-002.json').read_text());pages=[]
    for n,o in zip(cases,old['cases'],strict=True):assert n['input_sha256']==o['input_sha256']
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(eye_omission_probe.OUT)])
    async with Client(transport) as client:
        for page in old['pages']:
            png,meta=await save_result(client,'render_contact_sheet',page['controls'],eye_omission_probe.OUT,page['stem']);h=[c['pixel_sha256'] for c in meta['cells']]
            assert h[0]==h[1] and h[2]==h[3] and h[0]!=h[2]
            pages.append({'stem':page['stem'],'controls':page['controls'],'png_sha256':SHA(png),'cell_hashes':h,'old_cell_hashes':page['cell_hashes'],'same_cells':h==page['cell_hashes']})
    (eye_omission_probe.OUT/'report.json').write_text(json.dumps({'renderer_revision':REV,'cases':cases,'pages':pages},indent=2)+'\n')
    eye.append({'experiment':'eye-002','rebuilt_copies':2,'mcp_pages':len(pages),'confirmed_iris_noop_and_host_both_equivalence':True,'pixel_drift':sum(not p['same_cells'] for p in pages)})
    # Assembly findings are compared separately from their changed pixels.
    prior=json.loads((ROOT/'experiments/shade-001.json').read_text());slope=[]
    for c in prior['cases']:
        now=numerical(ROOT/'scratch/research/shade-001',c)
        slope.append({'species':c['species'],'loads':len(now),'same_records':now==c['checks'],'records':now,'changed_fields':[{'pose':n['pose'],'yaw':n['yaw'],'variant':n['variant'],'fields':[k for k in n if n[k]!=o[k]]} for n,o in zip(now,c['checks'],strict=True) if n!=o]})
    r=json.loads((ROOT/'experiments/shade-002.json').read_text());resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/shade-001'));assets={};hist=[];histfolder=OUT/'shade-002';histfolder.mkdir()
    for index,c in enumerate(r['cases']):
        assert SHA((ROOT/'scratch/research/shade-001'/c['input']).read_bytes())==c['input_sha256']
        key=(c['input'],c['pose'])
        if key not in assets:assets[key]=load_breed_assets(resolver,c['input'],pose=c['pose'],seed=0,age=100,fatness=50)
        now,private,png,baseline=compose(assets[key],{'yaw':c['yaw_units'],'fatness':50},HISTORIES[c['history']]);stem=f'{index:03d}';sheet=stem+'.png';(histfolder/sheet).write_bytes(png)
        statefile=stem+'-state.json';raw=json.dumps(private,separators=(',',':')).encode();(histfolder/statefile).write_bytes(raw)
        hist.append({'species':c['species'],'variant':c['variant'],'pose':c['pose'],'yaw_degrees':c['yaw_degrees'],'history':c['history'],'sheet':sheet,'sheet_sha256':SHA(png),'private_state_file':statefile,'private_state_sha256':SHA(raw),'old_changed_pixels':c['changed_pixels'],'same_offsets':now['fresh_offsets']==c['fresh_offsets'] and now['retained_offsets']==c['retained_offsets'],'same_changed_fills':now['changed_fills']==c['changed_fills'],**now})
    r=json.loads((ROOT/'experiments/shade-003.json').read_text());resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/shade-003'));assets={};scans=[];composed=[];cfolder=OUT/'shade-003';cfolder.mkdir()
    for s in r['scans']:
        key=(s['species'],s['pose'])
        if key not in assets:
            c=next(c for c in r['inputs'] if c['species']==s['species']);assert SHA((ROOT/'scratch/research/shade-003'/c['paths']['baseline']).read_bytes())==c['input_hashes']['baseline']
            assets[key]=load_breed_assets(resolver,c['paths']['baseline'],pose=s['pose'],seed=0,age=100,fatness=50)
        now=scan(assets[key],s['yaw_units']);scans.append({'species':s['species'],'pose':s['pose'],'yaw_units':s['yaw_units'],'same_records':all(now[k]==s[k] for k in now),'cases':len(now['rows']),'records':now})
    for index,c in enumerate(r['cases']):
        now,private,png=composition(assets[(c['species'],c['pose'])],c['yaw_units'],c['omitted_id']);stem=f'{index:03d}';sheet=stem+'.png';(cfolder/sheet).write_bytes(png)
        statefile=stem+'-pixels.json';raw=json.dumps(private,separators=(',',':')).encode();(cfolder/statefile).write_bytes(raw)
        composed.append({'species':c['species'],'pose':c['pose'],'yaw_degrees':c['yaw_degrees'],'omitted_id':c['omitted_id'],'sheet':sheet,'sheet_sha256':SHA(png),'private_pixels_file':statefile,'private_pixels_sha256':SHA(raw),'old_shade_changed_pixels':c['omitted_vs_held_changed_pixels'],**now})
    # Re-run the historical motion method without overwriting its old report or snapshots.
    texture_motion_history.OUT=OUT/'texture-004'
    with redirected_reports(texture_motion_history.OUT):await texture_motion_history.main()
    motion=json.loads((texture_motion_history.OUT/'report.json').read_text());oldmotion=json.loads((ROOT/'experiments/texture-004.json').read_text())
    summary={'experiment':'UPDATE-002','renderer_revision':REV,'eye':eye,'slope':slope,'shade_histories':hist,'omission_scans':scans,'omission_compositions':composed,'texture_motion':{'old_summary':oldmotion['summary'],'new_summary':motion['summary'],'report_sha256':SHA((texture_motion_history.OUT/'report.json').read_bytes()),'state_schema_note':'new paint_angles component is retained by full state; geometry/host-orientation-only counterfactuals reset it'},'historical_reports':{name:SHA((ROOT/f'experiments/{name}.json').read_bytes()) for name in ('eye-001','eye-002','shade-001','shade-002','shade-003','texture-004')}}
    for path in (OUT/'report.json',ROOT/'experiments/update-002.json'):path.write_text(json.dumps(summary,indent=2)+'\n')
    print('UPDATE-002 complete',flush=True)
if __name__=='__main__':asyncio.run(main())
