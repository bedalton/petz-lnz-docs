"""MORPH-005: explicit retained-state pixels and isolated ordering controls."""
import asyncio,base64,json,sys,importlib.metadata
from dataclasses import replace
from io import BytesIO
from pathlib import Path
from PIL import Image
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,draw_prepared_frame
from petz_renderer.rendering.output import offset_prepared_frame,encode_png,render_portrait
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineRenderer
from morph_history_probe import HISTORIES
from research_common import ROOT,SHA,adult
OUT=ROOT/'scratch/research/morph-005'
def prepare(a,history=(),state=None):
    return prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,fatness=50,morph_updates=history)
def draw(a,p,bounds):
    width=bounds.max_x-bounds.min_x+1;height=bounds.max_y-bounds.min_y+1
    fb=Framebuffer(width,height,background=255)
    shifted=offset_prepared_frame(p,-bounds.min_x,-bounds.min_y)
    state=draw_prepared_frame(fb,shifted,a.appearance,line_renderer=LineRenderer(seed=1),seed=1,step=0)
    return fb,state,encode_png(fb,a.palette)
def pixel_diff(a,b):
    assert len(a)==len(b)
    return sum(x!=y for x,y in zip(a,b))
async def main():
    OUT.mkdir(parents=True,exist_ok=False)
    prior=json.loads((ROOT/'experiments/morph-003.json').read_text());cases=[];baselines=[]
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/morph-003'))
    for c in prior['cases']:
        source,raw,*_=adult(c['species']);assert SHA(raw)==c['source_sha256']
        for variant in ('dormant_body','dormant_head'):
            path=ROOT/'scratch/research/morph-003'/c['paths'][variant];assert SHA(path.read_bytes())==c['input_hashes'][variant]
            for pose in ('standing','sitting','lying'):
                a=load_breed_assets(resolver,path.name,pose=pose,seed=0,age=100,fatness=50)
                initial=prepare(a);bounds=initial.geometry.ordering.bounds
                fb,_,png=draw(a,initial,bounds)
                portrait=render_portrait(a,fatness=50)
                assert png==portrait.png and fb.pixels==portrait.indices
                stem=f"{c['species']}-{variant}-{pose}-baseline";(OUT/f'{stem}.png').write_bytes(png)
                baselines.append({'species':c['species'],'variant':variant,'pose':pose,'input':path.name,'png':f'{stem}.png','png_sha256':SHA(png)})
                for name,history in HISTORIES.items():
                    batch=prepare(a,history)
                    current=initial
                    # Every intermediate draw persists FrameState; raster RNG/step are reset controls.
                    _,state,_=draw(a,current,current.geometry.ordering.bounds)
                    for n in range(1,len(history)+1):
                        current=prepare(a,history[:n],state)
                        _,state,_=draw(a,current,current.geometry.ordering.bounds)
                    assert batch.geometry.balls==current.geometry.balls
                    assert batch.geometry.ordering.bounds==current.geometry.ordering.bounds
                    final_bounds=batch.geometry.ordering.bounds
                    bf,_,bp=draw(a,batch,final_bounds);cf,_,cp=draw(a,current,final_bounds)
                    # Keep every batch command unchanged, substitute only retained sorted order.
                    order_only=replace(batch,geometry=replace(batch.geometry,ordering=replace(batch.geometry.ordering,sorted_order=current.geometry.ordering.sorted_order,draw_order=current.geometry.ordering.draw_order)))
                    of,_,op=draw(a,order_only,final_bounds)
                    width,height=bf.width,bf.height
                    images=[Image.open(BytesIO(p)).convert('RGBA') for p in (bp,cp,op)]
                    sheet=Image.new('RGBA',(width*3,height))
                    for i,im in enumerate(images):sheet.paste(im,(width*i,0))
                    stem=f"{c['species']}-{variant}-{pose}-{name}"
                    buf=BytesIO();sheet.save(buf,format='PNG');sheet_bytes=buf.getvalue();(OUT/f'{stem}.png').write_bytes(sheet_bytes)
                    record={'species':c['species'],'variant':variant,'pose':pose,'history':name,'input':path.name,'input_sha256':c['input_hashes'][variant],'sheet':f'{stem}.png','sheet_sha256':SHA(sheet_bytes),'cell_size':[width,height],'cell_order':['batch','retained','batch_commands_retained_order'],'cell_hashes':[{'rgba_sha256':SHA(im.tobytes()),'indexed_sha256':SHA(f.pixels)} for im,f in zip(images,(bf,cf,of))],'batch_retained_changed_pixels':pixel_diff(bf.pixels,cf.pixels),'batch_order_only_changed_pixels':pixel_diff(bf.pixels,of.pixels),'retained_order_only_changed_pixels':pixel_diff(cf.pixels,of.pixels),'same_prepared_commands':batch.balls==current.balls,'same_sorted_order':batch.geometry.ordering.sorted_order==current.geometry.ordering.sorted_order,'same_fills':batch.geometry.fills==current.geometry.fills}
                    cases.append(record)
                print(c['species'],variant,pose,flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/morph-003')])
    async with Client(transport) as client:
        for row in baselines:
            result=await client.call_tool('render_pet',{'path':row['input'],'pose':row['pose'],'seed':0,'age':100,'fatness':50,'yaw_degrees':0})
            assert not result.is_error
            png=base64.b64decode(next(block.data for block in result.content if block.type=='image'))
            assert SHA(png)==row['png_sha256'],row
            row['local_mcp_png_match']=True
            (OUT/(Path(row['png']).stem+'-mcp.json')).write_text(json.dumps(result.data,indent=2)+'\n')
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent;hashes={}
    for name in ('appearance/evaluation.py','rendering/morphs.py','rendering/attachment.py','rendering/assembly.py','rendering/ordering.py','rendering/shading.py','rendering/preparation.py','rendering/composition.py','rendering/output.py'):
        content=(installed/name).read_bytes();assert content==(ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes();hashes[name]=SHA(content)
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text())
    for path,expected in provenance['shared_engine_hashes']['petz4'].items():assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    summary={key:sum(bool(c[key]) for c in cases) for key in ('batch_retained_changed_pixels','batch_order_only_changed_pixels','retained_order_only_changed_pixels')}
    report={'experiment':'MORPH-005','backend':'direct Python explicit-state indexed composition; local stdio MCP default-state crosschecks','renderer_revision':prior['renderer_revision'],'python':sys.version,'controls':{'seed':0,'raster_seed':1,'raster_step':0,'line_rng':'fresh seed1 per draw, including retained frames','age':100,'fatness':50,'yaw':0,'head_rotation':0},'reused_input_manifest':'morph-003.json','histories':HISTORIES,'cases':cases,'baselines':baselines,'changed_case_counts':summary,'source_hashes':hashes,'shared_engine_hashes':provenance['shared_engine_hashes']['petz4'],'dependency_versions':{n:importlib.metadata.version(n) for n in ('fastmcp','numpy','Pillow','pydantic')}}
    for target in (OUT/'report.json',ROOT/'experiments/morph-005.json'):target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
if __name__=='__main__':asyncio.run(main())
