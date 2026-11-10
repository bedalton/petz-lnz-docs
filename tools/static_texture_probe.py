"""TEXTURE-001: repeated static frames with isolated persistent state."""
import asyncio,base64,json,sys,importlib.metadata
from dataclasses import asdict
from io import BytesIO
from pathlib import Path
from PIL import Image
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,FrameState
from petz_renderer.rendering.output import render_portrait
from morph_pixel_probe import draw,pixel_diff
from research_common import ROOT,SHA,adult
OUT=ROOT/'scratch/research/texture-001'
def sheet_png(pngs):
    images=[Image.open(BytesIO(p)).convert('RGBA') for p in pngs]
    w,h=images[0].size;assert all(im.size==(w,h) for im in images)
    sheet=Image.new('RGBA',(w*len(images),h))
    for i,im in enumerate(images):sheet.paste(im,(w*i,0))
    out=BytesIO();sheet.save(out,format='PNG')
    return out.getvalue(),[{'rgba_sha256':SHA(im.tobytes())} for im in images],(w,h)
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[]
    resolver=ResourceResolver((ROOT/'games/petz4',))
    for species in ('Dogz','Catz'):
        source,raw,*_=adult(species)
        relative=str(source.relative_to(ROOT/'games/petz4'))
        for pose in ('standing','sitting','lying'):
            a=load_breed_assets(resolver,relative,pose=pose,seed=0,age=100,fatness=50)
            for degrees,yaw in ((0,0),(90,64)):
                call=lambda state=None:prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,fatness=50,yaw=yaw)
                first=call();bounds=first.geometry.ordering.bounds
                f1,state1,p1=draw(a,first,bounds)
                assert p1==render_portrait(a,fatness=50,yaw=yaw).png
                full=call(state1)
                geom=call(FrameState(geometry=state1.geometry))
                texture=call(FrameState(orientations=state1.orientations))
                fresh=call()
                prepared=[first,full,geom,texture,fresh]
                output=[draw(a,p,bounds) for p in prepared]
                assert all(p.geometry.balls==first.geometry.balls for p in prepared)
                stem=f'{species}-{pose}-{degrees}'
                png,hashes,size=sheet_png([o[2] for o in output]);(OUT/f'{stem}-resets.png').write_bytes(png)
                reset={'sheet':f'{stem}-resets.png','sheet_sha256':SHA(png),'cell_size':size,'cell_labels':['first','second_full_state','second_geometry_only','second_texture_only','fresh'],'cell_hashes':hashes,'indexed_hashes':[{'sha256':SHA(o[0].pixels)} for o in output],'changed_from_first':[pixel_diff(f1.pixels,o[0].pixels) for o in output],'full_vs_texture_only_changed_pixels':pixel_diff(output[1][0].pixels,output[3][0].pixels),'geometry_only_vs_fresh_changed_pixels':pixel_diff(output[2][0].pixels,output[4][0].pixels),'changed_command_ids':[i for i,(b,c) in enumerate(zip(first.balls,full.balls)) if b!=c],'texture_angle_changes':[{'ball':i,'first':b.circle.angles,'second':c.circle.angles} for i,(b,c) in enumerate(zip(first.balls,full.balls)) if b.circle.angles!=c.circle.angles]}
                state2=output[1][1]
                third_prepared=[first,call(state2),call(FrameState(geometry=state2.geometry)),call(FrameState(orientations=state2.orientations)),call()]
                output=[draw(a,p,bounds) for p in third_prepared]
                png,hashes,size=sheet_png([o[2] for o in output]);(OUT/f'{stem}-third-resets.png').write_bytes(png)
                third_reset={'sheet':f'{stem}-third-resets.png','sheet_sha256':SHA(png),'cell_size':size,'cell_labels':['first','third_full_state','third_geometry_only','third_texture_only','fresh'],'cell_hashes':hashes,'indexed_hashes':[{'sha256':SHA(o[0].pixels)} for o in output],'changed_from_first':[pixel_diff(f1.pixels,o[0].pixels) for o in output],'full_vs_texture_only_changed_pixels':pixel_diff(output[1][0].pixels,output[3][0].pixels),'geometry_only_vs_fresh_changed_pixels':pixel_diff(output[2][0].pixels,output[4][0].pixels),'changed_command_ids':[i for i,(b,c) in enumerate(zip(first.balls,third_prepared[1].balls)) if b!=c],'texture_angle_changes':[{'ball':i,'first':b.circle.angles,'second':c.circle.angles} for i,(b,c) in enumerate(zip(first.balls,third_prepared[1].balls)) if b.circle.angles!=c.circle.angles]}
                pngs=[p1];frames=[{'frame':1,'indexed_sha256':SHA(f1.pixels),'changed_from_first':0,'orientation_state':[(i,asdict(state1.orientations[i])) for i,b in enumerate(first.balls) if b.circle.angles is not None]}]
                state=state1
                for n in range(2,9):
                    p=call(state);assert p.geometry.balls==first.geometry.balls
                    fb,state,png=draw(a,p,bounds);pngs.append(png)
                    frames.append({'frame':n,'indexed_sha256':SHA(fb.pixels),'changed_from_first':pixel_diff(f1.pixels,fb.pixels),'orientation_state':[(i,asdict(state.orientations[i])) for i,b in enumerate(p.balls) if b.circle.angles is not None]})
                seq,seq_hashes,_=sheet_png(pngs);(OUT/f'{stem}-sequence.png').write_bytes(seq)
                cases.append({'species':species,'source':relative,'source_sha256':SHA(raw),'pose':pose,'yaw_degrees':degrees,'yaw_units':yaw,'resets':reset,'third_resets':third_reset,'sequence':{'sheet':f'{stem}-sequence.png','sheet_sha256':SHA(seq),'cell_size':size,'cell_hashes':seq_hashes,'frames':frames},'first_png_sha256':SHA(p1)})
                print(stem,reset['changed_from_first'],[f['changed_from_first'] for f in frames],flush=True)
        assert SHA(source.read_bytes())==SHA(raw)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4')])
    async with Client(transport) as client:
        for c in cases:
            result=await client.call_tool('render_pet',{'path':c['source'],'pose':c['pose'],'seed':0,'age':100,'fatness':50,'yaw_degrees':c['yaw_degrees']})
            assert not result.is_error
            png=base64.b64decode(next(b.data for b in result.content if b.type=='image'));assert SHA(png)==c['first_png_sha256'];c['first_local_mcp_match']=True
            (OUT/f"{c['species']}-{c['pose']}-{c['yaw_degrees']}-mcp.json").write_text(json.dumps(result.data,indent=2)+'\n')
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent;source_hashes={}
    for name in ('rendering/preparation.py','rendering/texture_rotation.py','rendering/texture.py','rendering/output.py','rendering/assembly.py','rendering/ordering.py'):
        content=(installed/name).read_bytes();assert content==(ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes();source_hashes[name]=SHA(content)
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text())
    for path,expected in provenance['shared_engine_hashes']['petz4'].items():assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    summary={'third_frame_pixel_changes':sum(bool(c['third_resets']['changed_from_first'][1]) for c in cases),'third_geometry_only_pixel_changes':sum(bool(c['third_resets']['changed_from_first'][2]) for c in cases),'third_texture_only_pixel_changes':sum(bool(c['third_resets']['changed_from_first'][3]) for c in cases),'third_full_vs_texture_only_differences':sum(bool(c['third_resets']['full_vs_texture_only_changed_pixels']) for c in cases),'second_frame_pixel_changes':sum(bool(c['resets']['changed_from_first'][1]) for c in cases),'geometry_only_pixel_changes':sum(bool(c['resets']['changed_from_first'][2]) for c in cases),'texture_only_pixel_changes':sum(bool(c['resets']['changed_from_first'][3]) for c in cases),'full_vs_texture_only_differences':sum(bool(c['resets']['full_vs_texture_only_changed_pixels']) for c in cases)}
    report={'experiment':'TEXTURE-001','backend':'direct Python retained FrameState composition; local stdio MCP first-frame checks','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'controls':{'seed':0,'age':100,'fatness':50,'raster_seed':1,'step':0,'line_rng':'fresh seed1 every draw','animation_frame':'fixed per named pose; no morph updates'},'cases':cases,'summary':summary,'source_hashes':source_hashes,'shared_engine_hashes':provenance['shared_engine_hashes']['petz4'],'dependency_versions':{n:importlib.metadata.version(n) for n in ('fastmcp','numpy','Pillow','pydantic')}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    public=json.loads(json.dumps(report))
    for c in public['cases']:
        first={i:o for i,o in c['sequence']['frames'][0]['orientation_state']}
        for f in c['sequence']['frames']:
            state=f.pop('orientation_state')
            f['orientation_state_sha256']=SHA(json.dumps(state,sort_keys=True).encode())
            f['changed_orientations_from_first']=[{'ball':i,'angles':o['angles'],'frame_angles':o['frame_angles']} for i,o in state if o['angles']!=first[i]['angles']]
    (ROOT/'experiments/texture-001.json').write_text(json.dumps(public,indent=2)+'\n')
    print(summary)
if __name__=='__main__':asyncio.run(main())
