"""UPDATE-004: rebuild remaining old inputs byte-identically and replay them."""
import asyncio,json,sys,traceback
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import addball_probe,head_shape_probe,move_probe,omission_sweep
from head_gate_probe import PAIRS
from revalidate_renderer_update import digests,hashes,partition
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/update-004'
async def main():
    OUT.mkdir(parents=True,exist_ok=False);builds=[];rows=[]
    for name,module in (('add-001',addball_probe),('head-001',head_shape_probe),('move-001',move_probe),('omit-001',omission_sweep)):
        module.OUT=OUT/name;module.OUT.mkdir()
        try:cases=module.prepare();builds.append({'experiment':name,'prepare_assertions_pass':True})
        except AssertionError as exc:
            (module.OUT/'prepare-error.txt').write_text(traceback.format_exc());builds.append({'experiment':name,'prepare_assertions_pass':False,'error':str(exc)})
    gate=OUT/'head-002';gate.mkdir()
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,_,_=adult(species)
        for name,pair in PAIRS.items():
            s=dict(base);s['Head Enlargement']=tuple(str(v) for v in pair);write_copy(raw,leaf,s,gate/f'{species}-{name}{source.suffix}')
    for name in ('add-001','head-001','move-001','head-002','omit-001','vis-002'):
        old=json.loads((ROOT/f'experiments/{name}.json').read_text());records=old.get('comparisons',[])+old.get('pages',[]);root=OUT/('omit-001' if name=='vis-002' else name);known=digests(old)
        transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(root)])
        async with Client(transport) as client:
            for index,rec in enumerate(records):
                args=rec['controls'];paths=[args[k] for k in ('before_path','after_path','path') if k in args];inputs={p:SHA((root/p).read_bytes()) for p in paths};assert all(h in known for h in inputs.values())
                op='render_contact_sheet' if 'path' in args else 'compare_appearance';stem=f'{name}-{index:03d}';png,meta=await save_result(client,op,args,OUT,stem);h=[c['pixel_sha256'] for c in meta['cells']]
                oldh=hashes(rec)
                if oldh:confirmed=partition(oldh)==partition(h)
                elif 'cells_equal' in rec:confirmed=(h[0]==h[1])==rec['cells_equal']
                elif name=='head-001':confirmed=h[0]!=h[1]
                elif name=='vis-002':confirmed=all((x==h[0])==c['same_as_control'] for x,c in zip(h,rec['cells'],strict=True))
                elif name=='omit-001':
                    observations=[o for o in old['observations'] if o['species']==rec['species'] and o['yaw']==args['yaw_degrees']]
                    byid={o['ball']:o for o in observations}
                    confirmed=all((h[i]==h[0])==byid[ball]['same_as_control'] for i,ball in enumerate(rec['cell_ball_ids']) if ball is not None)
                else:raise AssertionError('unclassified historical relationship')
                rows.append({'experiment':name,'index':index,'stem':stem,'controls':args,'asset_root':str(root.relative_to(ROOT)),'input_hashes':inputs,'png_sha256':SHA(png),'cell_hashes':h,'old_cell_hashes':oldh,'relationship_confirmed':confirmed,'same_png':SHA(png)==rec['png_sha256']})
                (OUT/'progress.json').write_text(json.dumps(rows,indent=2)+'\n')
        print(name,len(records),'complete',flush=True)
    report={'experiment':'UPDATE-004','renderer_revision':json.loads((ROOT/'experiments/update-001.json').read_text())['renderer_revision'],'backend':'byte-identical rebuilt copies; fresh local stdio MCP','builds':builds,'replays':rows,'summary':{'controls':len(rows),'relationship_confirmed':sum(r['relationship_confirmed'] for r in rows),'cells':sum(len(r['cell_hashes']) for r in rows)},'historical_reports':{n:SHA((ROOT/f'experiments/{n}.json').read_bytes()) for n in ('add-001','head-001','move-001','head-002','omit-001','vis-002')}}
    for path in (OUT/'report.json',ROOT/'experiments/update-004.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print(report['summary'],flush=True)
if __name__=='__main__':asyncio.run(main())
