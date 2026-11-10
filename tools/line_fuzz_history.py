"""Asset-free retained connector fuzz table and shared whisker RNG probe."""
import importlib.metadata,json,sys
from dataclasses import replace
from pathlib import Path
import petz_renderer
from petz_renderer.rendering.lines import LineBlock,LineRenderer
from petz_renderer.rendering.framebuffer import Framebuffer
from research_common import ROOT,SHA
OUT=ROOT/'scratch/research/line-008'
def snapshot(r):return {'rng':r._state,'tables':[list(t) for t in r._tables]}
def main():
    OUT.mkdir(parents=True,exist_ok=False);records=[];private=[]
    for fuzz in (1,3,7):
        for endpoints in ((20,20,80,70),(80,70,20,20),(20,50,80,50),(50,20,50,80)):
            target=LineBlock(*endpoints,start_thick=12,end_thick=12,color=220,left_color=180,right_color=200,edge_mode=0,fuzz=fuzz)
            results={}
            for history in ('fresh','repeat','zero','other_fuzz','whisker0','whisker1','short_same','short_other_then_same'):
                renderer=LineRenderer(seed=1);fb=Framebuffer(120,120)
                short=replace(target,x1=20,y1=20,x2=40,y2=24)
                if history=='repeat':renderer.draw(fb,target)
                elif history=='zero':renderer.draw(fb,replace(target,fuzz=0))
                elif history=='other_fuzz':renderer.draw(fb,replace(target,fuzz=3 if fuzz!=3 else 7))
                elif history.startswith('whisker'):renderer.draw_whisker(fb,15,15,85,70,125,step=0 if history=='whisker0' else 1)
                elif history=='short_same':renderer.draw(fb,short)
                elif history=='short_other_then_same':
                    renderer.draw(fb,short)
                    renderer.draw(fb,replace(target,fuzz=3 if fuzz!=3 else 7))
                before=snapshot(renderer);fb.clear(0);renderer.draw(fb,target);after=snapshot(renderer)
                results[history]=fb.pixels
                record={'fuzz':fuzz,'endpoints':endpoints,'history':history,'indexed_sha256':SHA(fb.pixels),'state_before_sha256':SHA(json.dumps(before,sort_keys=True).encode()),'state_after_sha256':SHA(json.dumps(after,sort_keys=True).encode()),'table_lengths_before':[len(t) for t in before['tables']],'table_lengths_after':[len(t) for t in after['tables']],'rng_before':before['rng'],'rng_after':after['rng']}
                records.append(record);private.append({'record':record,'before':before,'after':after})
            for history in ('repeat','zero','whisker1','short_same'):assert results[history]==results['fresh'],(fuzz,endpoints,history)
            for record in records[-8:]:
                pixels=results[record['history']];baseline=results['fresh'];record['pixels_different_from_fresh']=sum(a!=b for a,b in zip(pixels,baseline,strict=True))
    package=Path(petz_renderer.__file__).parent
    hashes={p:SHA((package/p).read_bytes()) for p in ('rendering/lines.py','rendering/framebuffer.py','rendering/rotation.py')}
    for p,h in hashes.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    summary={h:{'cases':sum(r['history']==h for r in records),'changed':sum(r['history']==h and r['pixels_different_from_fresh']>0 for r in records)} for h in results}
    report={'experiment':'LINE-008','backend':'asset-free direct Python rasterization; no MCP or game data','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp',)},'source_hashes':hashes,'controls':{'seed':1,'canvas':[120,120],'fill':220,'edges':[180,200],'widths':[12,12],'edge_mode':0,'clear_between_history_and_target':True},'summary':summary,'records':records}
    (OUT/'states.json').write_text(json.dumps(private,indent=2)+'\n')
    for p in (OUT/'report.json',ROOT/'experiments/line-008.json'):p.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
