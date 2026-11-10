"""LINE-011: retained line RNG with fixed prepared breed scenes."""
import asyncio,base64,importlib.metadata,json,sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,draw_prepared_frame
from petz_renderer.rendering.output import offset_prepared_frame,encode_png,render_portrait
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineRenderer,LineBlock
from static_texture_probe import sheet_png
from research_common import ROOT,SHA,adult
OUT=ROOT/'scratch/research/line-011'
HISTORIES=('fresh','repeat_scene_step1','prior_scene_step0','prior_other_pose_step1','whisker0','whisker1','prime_fuzz3')
def line_state(r):return {'rng':r._state,'tables':[list(t) for t in r._tables]}
def draw(a,p,r,step):
    b=p.geometry.ordering.bounds
    fb=Framebuffer(b.max_x-b.min_x+1,b.max_y-b.min_y+1,background=255)
    draw_prepared_frame(fb,offset_prepared_frame(p,-b.min_x,-b.min_y),a.appearance,line_renderer=r,step=step,seed=1)
    return fb,encode_png(fb,a.palette)
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];states=[]
    prior=json.loads((ROOT/'experiments/line-007.json').read_text())
    inputs=ROOT/'scratch/research/line-007';resolver=ResourceResolver((ROOT/'games/petz4',inputs))
    for c in prior['cases']:
        source,raw,*_=adult(c['species']);assert SHA(raw)==c['source_sha256']
        path=inputs/c['paths']['seven'];assert SHA(path.read_bytes())==c['input_hashes']['seven']
        for pose in ('standing','sitting','lying'):
            a=load_breed_assets(resolver,path.name,pose=pose,seed=0,age=100,fatness=50)
            other_pose='lying' if pose=='standing' else 'standing'
            other=load_breed_assets(resolver,path.name,pose=other_pose,seed=0,age=100,fatness=50)
            for degrees,yaw in ((0,0),(90,64)):
                p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50,yaw=yaw)
                op=prepare_frame(other.appearance,other.sizes,other.frame,textures=other.textures,fatness=50,yaw=yaw)
                prepared_hash=SHA(repr(p).encode());outputs=[];records=[]
                basefb,basepng=draw(a,p,LineRenderer(seed=1),0)
                assert basepng==render_portrait(a,fatness=50,yaw=yaw).png
                for history in HISTORIES:
                    r=LineRenderer(seed=1)
                    if history=='repeat_scene_step1':draw(a,p,r,1)
                    elif history=='prior_scene_step0':draw(a,p,r,0)
                    elif history=='prior_other_pose_step1':draw(other,op,r,1)
                    elif history.startswith('whisker'):
                        r.draw_whisker(Framebuffer(100,100),15,15,85,70,125,step=0 if history=='whisker0' else 1)
                    elif history=='prime_fuzz3':r.draw(Framebuffer(100,100),LineBlock(20,20,80,70,start_thick=12,end_thick=12,color=220,fuzz=3,edge_mode=0))
                    before=line_state(r);fb,png=draw(a,p,r,1);after=line_state(r)
                    if not outputs:fresh=fb.pixels
                    changed=sum(x!=y for x,y in zip(fb.pixels,fresh,strict=True))
                    if history in ('fresh','repeat_scene_step1','whisker1'):assert changed==0,(c['species'],pose,degrees,history,changed)
                    assert SHA(repr(p).encode())==prepared_hash
                    record={'history':history,'indexed_sha256':SHA(fb.pixels),'pixels_different_from_fresh_step1':changed,'state_before_sha256':SHA(json.dumps(before,sort_keys=True).encode()),'state_after_sha256':SHA(json.dumps(after,sort_keys=True).encode())}
                    states.append({'species':c['species'],'pose':pose,'yaw_degrees':degrees,'record':record,'before':before,'after':after})
                    records.append(record);outputs.append(png)
                stem=f"{c['species']}-{pose}-{degrees}"
                png,hashes,size=sheet_png([basepng,*outputs]);(OUT/f'{stem}.png').write_bytes(png);(OUT/f'{stem}-baseline.png').write_bytes(basepng)
                cases.append({'species':c['species'],'pose':pose,'yaw_degrees':degrees,'prior_other_pose':other_pose,'input':str(path.relative_to(ROOT)),'input_sha256':SHA(path.read_bytes()),'source_sha256':SHA(raw),'prepared_repr_sha256':prepared_hash,'sheet':f'{stem}.png','sheet_sha256':SHA(png),'cell_size':size,'cell_labels':['fresh_step0',*HISTORIES],'cell_hashes':hashes,'baseline':f'{stem}-baseline.png','baseline_sha256':SHA(basepng),'step0_vs_fresh_step1_changed_pixels':sum(x!=y for x,y in zip(basefb.pixels,fresh,strict=True)),'histories':records})
                print(stem,[r['pixels_different_from_fresh_step1'] for r in records],flush=True)
        assert SHA(source.read_bytes())==SHA(raw)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(inputs)])
    async with Client(transport) as client:
        for c in cases:
            r=await client.call_tool('render_pet',{'path':Path(c['input']).name,'pose':c['pose'],'seed':0,'age':100,'fatness':50,'yaw_degrees':c['yaw_degrees']});assert not r.is_error
            png=base64.b64decode(next(b.data for b in r.content if b.type=='image'));assert SHA(png)==c['baseline_sha256']
            c['local_mcp_baseline_match']=True
            (OUT/f"{c['species']}-{c['pose']}-{c['yaw_degrees']}-mcp.json").write_text(json.dumps(r.data,indent=2)+'\n')
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent
    sources={name:SHA((installed/name).read_bytes()) for name in ('rendering/lines.py','rendering/preparation.py','rendering/composition.py','rendering/output.py','rendering/framebuffer.py')}
    for name,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==h
    summary={h:sum(r['pixels_different_from_fresh_step1']>0 for c in cases for r in c['histories'] if r['history']==h) for h in HISTORIES}
    report={'experiment':'LINE-011','backend':'direct prepared breed composition with retained LineRenderer; local stdio MCP first-frame controls','renderer_revision':prior['renderer_revision'],'python':sys.version,'controls':{'seed':0,'age':100,'fatness':50,'line_seed':1,'target_step':1,'baseline_step':0,'prepared_scene':'identical frozen target; no FrameState retained','prior_pixels':'discarded before target'},'source_hashes':sources,'engine_hashes':prior['engine_hashes'],'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','Pillow')},'summary_changed_fixture_counts':summary,'cases':cases}
    for name,h in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==h
    (OUT/'states.json').write_text(json.dumps(states,indent=2)+'\n')
    for dest in (OUT/'report.json',ROOT/'experiments/line-011.json'):dest.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
if __name__=='__main__':asyncio.run(main())
