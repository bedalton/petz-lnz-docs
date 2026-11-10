"""Recheck the GAP-006 stock Scottie sitting/front trace after the renderer update."""
import asyncio,json,sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,FrameState
from morph_pixel_probe import draw,pixel_diff
from research_common import ROOT,SHA,save_result
import petz_renderer
recorded=json.loads((ROOT/'experiments/update-001.json').read_text())
for rel,h in recorded['source_hashes'].items():assert SHA((Path(petz_renderer.__file__).parent/rel).read_bytes())==h
OUT=ROOT/'scratch/research/update-002/static-trace'
async def main():
    OUT.mkdir(parents=True,exist_ok=False);path='Resource/Dogz/Scottie.dog';source=ROOT/'games/petz4'/path;digest=SHA(source.read_bytes());a=load_breed_assets(ResourceResolver((ROOT/'games/petz4',)),path,pose='sitting',seed=0,age=100,fatness=50)
    state=None;first=None;frames=[];before_third=None
    for frame in range(1,9):
        if frame==3:before_third=state
        p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,fatness=50)
        fb,state,png=draw(a,p,p.geometry.ordering.bounds)
        if first is None:first=fb;bounds=p.geometry.ordering.bounds
        assert p.geometry.ordering.bounds==bounds
        name=f'frame{frame}.png';(OUT/name).write_bytes(png)
        frames.append({'frame':frame,'png':name,'png_sha256':SHA(png),'indexed_sha256':SHA(fb.pixels),'changed_from_first':pixel_diff(first.pixels,fb.pixels),'ball42_angles':list(state.orientations[42].angles)})
    reset={}
    choices={'full':before_third,'geometry_only':FrameState(geometry=before_third.geometry),'host_texture_only':FrameState(orientations=before_third.orientations),'paint_angles_only':FrameState(paint_angles=before_third.paint_angles),'all_texture_only':FrameState(orientations=before_third.orientations,paint_angles=before_third.paint_angles),'fresh':None}
    for name,state in choices.items():
        p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,fatness=50);fb,_,png=draw(a,p,bounds);(OUT/(name+'.png')).write_bytes(png)
        reset[name]={'png_sha256':SHA(png),'indexed_sha256':SHA(fb.pixels),'changed_from_first':pixel_diff(first.pixels,fb.pixels)}
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4')])
    async with Client(transport) as client:
        png,_=await save_result(client,'render_pet',{'path':path,'pose':'sitting','seed':0,'age':100,'fatness':50,'yaw_degrees':0},OUT,'mcp-first');assert SHA(png)==frames[0]['png_sha256']
    assert SHA(source.read_bytes())==digest
    report={'source_sha256':digest,'controls':{'pose':'sitting','yaw_degrees':0,'seed':0,'age':100,'fatness':50,'line_rng_seed':1,'raster_seed':1,'step':0},'frames':frames,'third_resets':reset,'mcp_first_match':True}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
if __name__=='__main__':asyncio.run(main())
