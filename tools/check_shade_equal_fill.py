import sys,json
# Run from the workspace virtual environment; inputs are private copies.
from dataclasses import replace,fields
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,FrameState
from petz_renderer.rendering.assembly import GeometryState
from research_common import ROOT,SHA
from morph_pixel_probe import draw,pixel_diff
report=json.loads((ROOT/'experiments/shade-003.json').read_text())
case=next(c for c in report['inputs'] if c['species']=='Catz')
for name,digest in case['input_hashes'].items():assert SHA((ROOT/'scratch/research/shade-003'/case['paths'][name]).read_bytes())==digest
assert SHA((ROOT/case['source_path']).read_bytes())==case['source_sha256']
for name,digest in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==digest
import petz_renderer
from pathlib import Path
for name,digest in report['source_hashes'].items():
    for root in (Path(petz_renderer.__file__).parent,ROOT/'petz-renderer-mcp/src/petz_renderer'):assert SHA((root/name).read_bytes())==digest
r=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/shade-003'))
a=load_breed_assets(r,'Catz-baseline.cat',pose='sitting',seed=0,age=100,fatness=50)
fresh=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50,yaw=0)
app=replace(a.appearance,omissions=a.appearance.omissions|{44});a=replace(a,appearance=app)
omitted=prepare_frame(app,a.sizes,a.frame,textures=a.textures,fatness=50,yaw=0)
held=prepare_frame(app,a.sizes,a.frame,textures=a.textures,state=FrameState(geometry=GeometryState(shade=fresh.state.geometry.shade)),fatness=50,yaw=0)
changed={i:[f.name for f in fields(b) if getattr(b,f.name)!=getattr(c,f.name)] for i,(b,c) in enumerate(zip(omitted.balls,held.balls)) if b!=c}
print('changed prepared fields',changed)
base=draw(a,omitted,fresh.geometry.ordering.bounds)[0];control=draw(a,held,fresh.geometry.ordering.bounds)[0]
endpoint=replace(omitted,balls=tuple(replace(b,endpoint=c.endpoint) for b,c in zip(omitted.balls,held.balls)))
endpointfb=draw(a,endpoint,fresh.geometry.ordering.bounds)[0]
paint=replace(omitted,balls=tuple(replace(b,paints=c.paints) for b,c in zip(omitted.balls,held.balls)))
paintfb=draw(a,paint,fresh.geometry.ordering.bounds)[0]
result={'changed_fields':changed,'fresh_vs_held_pixels':pixel_diff(base.pixels,control.pixels),'endpoint_swap_vs_held_pixels':pixel_diff(endpointfb.pixels,control.pixels),'paint_swap_vs_held_pixels':pixel_diff(paintfb.pixels,control.pixels),'report_sha256':SHA((ROOT/'experiments/shade-003.json').read_bytes()),'backend':'direct Python; same Petz4 controls as SHADE-003','indexed_sha256':{'fresh':SHA(base.pixels),'held':SHA(control.pixels),'endpoint_swap':SHA(endpointfb.pixels),'paint_swap':SHA(paintfb.pixels)}}
assert changed=={64:['endpoint']}
assert result['fresh_vs_held_pixels']==result['paint_swap_vs_held_pixels']==1
assert result['endpoint_swap_vs_held_pixels']==0
print(json.dumps(result));(ROOT/'scratch/research/shade-003-equal-fill-attribution.json').write_text(json.dumps(result,indent=2)+'\n')
