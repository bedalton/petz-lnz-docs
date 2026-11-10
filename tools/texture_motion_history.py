"""TEXTURE-004: return-to-pose camera/head histories with state isolation."""
import asyncio
import base64
import importlib.metadata
import json
import sys
from dataclasses import asdict,replace
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,FrameState
from petz_renderer.rendering.connectors import build_line_block
from petz_renderer.rendering.output import render_portrait
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineRenderer
from morph_pixel_probe import draw,pixel_diff
from static_texture_probe import sheet_png
from research_common import ROOT,SHA
OUT=ROOT/'scratch/research/texture-004'
HISTORIES={'repeat':({}, {}, {}, {}),'yaw_arc':({'yaw_delta':16},{'yaw_delta':32},{'yaw_delta':16},{}),'head_arc':({'head_rotation':16},{'head_rotation':32},{'head_rotation':16},{}),'tilt_arc':({'tilt':8},{'tilt':16},{'tilt':8},{})}

def diagnostic(a,p):
    block=build_line_block(a.appearance.lines[-1],tuple(b.endpoint for b in p.balls))
    assert block is not None and block.paint is not None
    block=replace(block,x1=block.x1+256,y1=block.y1+256,x2=block.x2+256,y2=block.y2+256)
    fb=Framebuffer(512,512,background=254);LineRenderer(seed=1).draw(fb,block)
    return {'block':{k:v for k,v in vars(block).items() if k!='paint'},'paint_sha256':SHA(block.paint.texture.pixels),'shade_offset':block.paint.shade_offset,'has_sign':block.paint.has_sign,'indexed_sha256':SHA(fb.pixels)}

async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];baselines=[];private=[]
    prior=json.loads((ROOT/'experiments/line-021.json').read_text())
    input_root=ROOT/'scratch/research/line-021';resolver=ResourceResolver((ROOT/'games/petz4',input_root))
    for species in ('Dogz','Catz'):
        c=next(c for c in prior['cases'] if c['species']==species and c['dimensions']==[128,128])
        filename=c['paths']['textured'];digest=c['input_hashes']['textured'];assert SHA((input_root/filename).read_bytes())==digest
        assert SHA((ROOT/c['source_path']).read_bytes())==c['source_sha256']
        for pose in ('standing','sitting','lying'):
            a=load_breed_assets(resolver,filename,pose=pose,seed=0,age=100,fatness=50)
            for degrees,yaw in ((0,0),(90,64)):
                target={'fatness':50,'yaw':yaw}
                fresh=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,**target)
                bounds=fresh.geometry.ordering.bounds
                initial_fb,initial_state,initial_png=draw(a,fresh,bounds)
                assert initial_png==render_portrait(a,fatness=50,yaw=yaw).png
                stem=f'{species}-{pose}-{degrees}'
                (OUT/f'{stem}-baseline.png').write_bytes(initial_png)
                baselines.append({'species':species,'pose':pose,'yaw_degrees':degrees,'input':filename,'input_sha256':digest,'png':f'{stem}-baseline.png','png_sha256':SHA(initial_png)})
                for history,steps in HISTORIES.items():
                    state=initial_state;trace=[]
                    for changes in steps:
                        controls=dict(target);controls.update({k:v for k,v in changes.items() if k!='yaw_delta'});controls['yaw']+=changes.get('yaw_delta',0)
                        p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,**controls)
                        # Intermediate frames use their own bounds; only final target comparisons share bounds.
                        _,state,_=draw(a,p,p.geometry.ordering.bounds)
                        trace.append({'controls':controls,'state':asdict(state)})
                    # Replay the final target from the state BEFORE its last preparation/draw.
                    prior_state=initial_state
                    for changes in steps[:-1]:
                        controls=dict(target);controls.update({k:v for k,v in changes.items() if k!='yaw_delta'});controls['yaw']+=changes.get('yaw_delta',0)
                        p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=prior_state,**controls)
                        _,prior_state,_=draw(a,p,p.geometry.ordering.bounds)
                    call=lambda s:prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=s,**target)
                    full=call(prior_state);geom=call(FrameState(geometry=prior_state.geometry));texture=call(FrameState(orientations=prior_state.orientations))
                    assert all(q.geometry.balls==fresh.geometry.balls for q in (full,geom,texture))
                    assert all(q.geometry.ordering.bounds==bounds for q in (full,geom,texture))
                    order=replace(fresh,geometry=replace(fresh.geometry,ordering=replace(fresh.geometry.ordering,sorted_order=full.geometry.ordering.sorted_order,draw_order=full.geometry.ordering.draw_order)))
                    prepared=(fresh,full,geom,texture,order);output=[draw(a,q,bounds) for q in prepared]
                    assert output[1][1]==state
                    png,hashes,size=sheet_png([o[2] for o in output]);sheet=f'{stem}-{history}.png';(OUT/sheet).write_bytes(png)
                    record={'species':species,'pose':pose,'yaw_degrees':degrees,'yaw_units':yaw,'history':history,'input':filename,'input_sha256':digest,'sheet':sheet,'sheet_sha256':SHA(png),'cell_size':size,'cell_labels':['fresh','retained_full','retained_geometry_only','retained_texture_only','fresh_commands_retained_order'],'cell_hashes':hashes,'indexed_hashes':[SHA(o[0].pixels) for o in output],'changed_from_fresh':[pixel_diff(initial_fb.pixels,o[0].pixels) for o in output],'full_vs_geometry':pixel_diff(output[1][0].pixels,output[2][0].pixels),'full_vs_texture':pixel_diff(output[1][0].pixels,output[3][0].pixels),'same_fills':fresh.geometry.fills==full.geometry.fills,'same_order':fresh.geometry.ordering.sorted_order==full.geometry.ordering.sorted_order,'changed_circle_ids':[i for i,(b,c) in enumerate(zip(fresh.balls,full.balls)) if b.circle!=c.circle],'diagnostic':[diagnostic(a,q) for q in prepared]}
                    payload={'case':len(cases),'trace':trace,'before_final_state':asdict(prior_state),'final_states':[asdict(o[1]) for o in output],'indexed_pixels':[list(o[0].pixels) for o in output]}
                    raw=json.dumps(payload,separators=(',',':')).encode();statefile=f'{stem}-{history}-state.json';(OUT/statefile).write_bytes(raw)
                    record.update(private_state_file=statefile,private_state_sha256=SHA(raw));cases.append(record)
                print(stem,[x['changed_from_fresh'] for x in cases[-4:]],flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(input_root)])
    async with Client(transport) as client:
        for b in baselines:
            result=await client.call_tool('render_pet',{'path':b['input'],'pose':b['pose'],'seed':0,'age':100,'fatness':50,'yaw_degrees':b['yaw_degrees']});assert not result.is_error
            png=base64.b64decode(next(x.data for x in result.content if x.type=='image'));assert SHA(png)==b['png_sha256']
            assert result.data['game_version']=='petz4';b['local_mcp_match']=True
            (OUT/(Path(b['png']).stem+'-mcp.json')).write_text(json.dumps(result.data,indent=2)+'\n')
    package=Path(petz_renderer.__file__).parent;sources={n:SHA((package/n).read_bytes()) for n in ('rendering/preparation.py','rendering/texture.py','rendering/texture_rotation.py','rendering/assembly.py','rendering/ordering.py','rendering/shading.py','rendering/output.py','rendering/connectors.py','rendering/lines.py')}
    for n,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/n).read_bytes())==h
    for n,h in prior['engine_hashes'].items():assert SHA((ROOT/n).read_bytes())==h
    summary={'cases':len(cases),'changed_full':sum(bool(c['changed_from_fresh'][1]) for c in cases),'changed_geometry_only':sum(bool(c['changed_from_fresh'][2]) for c in cases),'changed_texture_only':sum(bool(c['changed_from_fresh'][3]) for c in cases),'changed_order_only':sum(bool(c['changed_from_fresh'][4]) for c in cases),'changed_diagnostic':sum(c['diagnostic'][0]['indexed_sha256']!=c['diagnostic'][1]['indexed_sha256'] for c in cases)}
    report={'experiment':'TEXTURE-004','backend':'direct Python retained FrameState compositions; local stdio MCP fresh baselines only','renderer_revision':prior['renderer_revision'],'python':sys.version,'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':sources,'engine_hashes':prior['engine_hashes'],'reused_manifest':'line-021.json','controls':{'seed':0,'age':100,'fatness':50,'raster_seed':1,'raster_step':0,'line_rng':'fresh seed1 every draw','history_units':'engine turns/256','frame':'fixed named pose throughout each case'},'histories':HISTORIES,'baselines':baselines,'cases':cases,'summary':summary}
    for path in (OUT/'report.json',ROOT/'experiments/texture-004.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print(summary,flush=True)
if __name__=='__main__':asyncio.run(main())
