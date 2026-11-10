"""LINE-014: asset-free connector texture crop and size-rejection fixtures."""
import importlib.metadata,json,sys
from dataclasses import replace
from pathlib import Path
import petz_renderer
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineBlock,LineRenderer
from petz_renderer.rendering.texture import TiledTexture,TexturePaint
from research_common import ROOT,SHA
OUT=ROOT/'scratch/research/line-014'
def main():
    OUT.mkdir(parents=True,exist_ok=False);records=[];private=[];pairs={}
    for period in (0,8):
        art=TiledTexture(8,8,bytes(range(160,224)),period,period);paint=TexturePaint(art,0,False)
        for axis in ('vertical','horizontal'):
            for span in (7,8,9):
                for reverse in (False,True):
                    for fuzz in (0,1,7):
                        points=(20,20,20,20+span-1) if axis=='vertical' else (20,20,20+span-1,20)
                        if reverse:points=points[2:]+points[:2]
                        block=LineBlock(*points,start_thick=3,end_thick=3,color=125,fuzz=fuzz,edge_mode=-1,paint=paint)
                        fb=Framebuffer(60,60);r=LineRenderer(seed=1);r.draw(fb,block)
                        plain=Framebuffer(60,60);LineRenderer(seed=1).draw(plain,replace(block,paint=None))
                        width=(3 if axis=='vertical' else span)+fuzz;height=span if axis=='vertical' else 3
                        rejected=width>8 or height>8
                        assert (not any(fb.pixels))==rejected
                        assert any(plain.pixels)
                        if rejected:assert r._state==1 and not any(r._tables)
                        samples=[]
                        if not rejected and fuzz==0:
                            srcx=(8-width)//2;srcy=8-height-(8-height)//2
                            for i in range(span):
                                x,y=(20,20+i) if axis=='vertical' else (20+i,20)
                                tx,ty=(srcx+1,srcy+i) if axis=='vertical' else (srcx+i,srcy+1)
                                expected=160+ty*8+tx;assert fb.get_pixel(x,y)==expected
                                samples.append({'destination':[x,y],'source':[tx,ty],'value':expected})
                        key=(axis,span,reverse,fuzz)
                        if period==0:pairs[key]=fb.pixels
                        else:assert pairs[key]==fb.pixels
                        record={'period':period,'axis':axis,'span':span,'reverse':reverse,'fuzz':fuzz,'computed_raster_size':[width,height],'rejected':rejected,'colored_pixels':sum(x!=0 for x in fb.pixels),'indexed_sha256':SHA(fb.pixels),'plain_indexed_sha256':SHA(plain.pixels),'rng_after':r._state,'table_lengths':[len(t) for t in r._tables],'centerline_samples':samples}
                        records.append(record);private.append({'record':record,'indexed_pixels':list(fb.pixels)})
    installed=Path(petz_renderer.__file__).parent;hashes={n:SHA((installed/n).read_bytes()) for n in ('rendering/lines.py','rendering/texture.py','rendering/framebuffer.py')}
    for n,h in hashes.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/n).read_bytes())==h
    report={'experiment':'LINE-014','backend':'asset-free direct Python indexed raster fixtures; no MCP/game data','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'source_hashes':hashes,'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp',)},'controls':{'texture_size':[8,8],'texture_values':'160..223 in row-major order','shade_offset':0,'has_sign':False,'canvas':[60,60],'line_seed':1,'widths':[3,3],'edge_mode':-1},'records':records,'summary':{'fixtures':len(records),'rejected':sum(r['rejected'] for r in records),'accepted':sum(not r['rejected'] for r in records),'sample_assertions':sum(len(r['centerline_samples']) for r in records)}}
    (OUT/'pixels.json').write_text(json.dumps(private)+'\n')
    for dest in (OUT/'report.json',ROOT/'experiments/line-014.json'):dest.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']))
if __name__=='__main__':main()
