"""Verify the updated GAP-006 trace and six explicit state resets."""
import json
from pathlib import Path
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,FrameState
from morph_pixel_probe import draw,pixel_diff
from research_common import ROOT,SHA
import petz_renderer
recorded=json.loads((ROOT/'experiments/update-001.json').read_text())
for rel,h in recorded['source_hashes'].items():assert SHA((Path(petz_renderer.__file__).parent/rel).read_bytes())==h
folder=ROOT/'scratch/research/update-002/static-trace';r=json.loads((folder/'report.json').read_text());source=ROOT/'games/petz4/Resource/Dogz/Scottie.dog';assert SHA(source.read_bytes())==r['source_sha256']
a=load_breed_assets(ResourceResolver((ROOT/'games/petz4',)),'Resource/Dogz/Scottie.dog',pose='sitting',seed=0,age=100,fatness=50)
state=None;first=None
for frame in range(1,9):
    if frame==3:before=state
    p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,fatness=50);fb,state,png=draw(a,p,p.geometry.ordering.bounds)
    if first is None:first=fb;bounds=p.geometry.ordering.bounds
    rec=r['frames'][frame-1];assert SHA(png)==rec['png_sha256']==SHA((folder/rec['png']).read_bytes());assert SHA(fb.pixels)==rec['indexed_sha256']
    assert pixel_diff(first.pixels,fb.pixels)==rec['changed_from_first'] and list(state.orientations[42].angles)==rec['ball42_angles']
choices={'full':before,'geometry_only':FrameState(geometry=before.geometry),'host_texture_only':FrameState(orientations=before.orientations),'paint_angles_only':FrameState(paint_angles=before.paint_angles),'all_texture_only':FrameState(orientations=before.orientations,paint_angles=before.paint_angles),'fresh':None}
for name,state in choices.items():
    p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,fatness=50);fb,_,png=draw(a,p,bounds);rec=r['third_resets'][name]
    assert SHA(png)==rec['png_sha256']==SHA((folder/(name+'.png')).read_bytes()) and SHA(fb.pixels)==rec['indexed_sha256']
    assert pixel_diff(first.pixels,fb.pixels)==rec['changed_from_first']
assert [x['changed_from_first'] for x in r['frames']]==[0,0,128,128,128,128,128,141]
assert r['third_resets']['full']['indexed_sha256']==r['third_resets']['host_texture_only']['indexed_sha256']==r['third_resets']['all_texture_only']['indexed_sha256']
meta=json.loads((folder/'mcp-first-render.json').read_text());assert meta['png_sha256']==r['frames'][0]['png_sha256']==SHA((folder/'mcp-first.png').read_bytes())
public={'experiment':'UPDATE-002-static','renderer_revision':json.loads((ROOT/'experiments/update-001.json').read_text())['renderer_revision'],'report_sha256':SHA((folder/'report.json').read_bytes()),'verified':{'frames':8,'state_resets':6,'mcp_baselines':1},'trace':r['frames'],'third_resets':r['third_resets'],'controls':r['controls'],'scope':'Scottie sitting/front only; no native-game evidence'}
for path in (folder/'verification.json',ROOT/'experiments/update-002-static.json'):path.write_text(json.dumps(public,indent=2)+'\n')
print(json.dumps(public['verified']))
