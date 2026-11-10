"""TEXTURE-002: trace the observed constant-pose orientation delta."""
import json,math,sys,importlib.metadata
from pathlib import Path
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.appearance.evaluation import body_areas
from petz_renderer.rendering.sizing import _HEAD_AREAS
from petz_renderer.rendering.rotation import _round,calc_after_tilt
from petz_renderer.rendering.texture_rotation import TextureOrientation,transpose_times,update_texture_orientation
from research_common import ROOT,SHA
OUT=ROOT/'scratch/research/texture-002'
def main():
    OUT.mkdir(parents=True,exist_ok=False)
    prior=json.loads((ROOT/'scratch/research/texture-001/report.json').read_text())
    case=next(c for c in prior['cases'] if c['species']=='Dogz' and c['pose']=='sitting' and c['yaw_degrees']==0)
    resolver=ResourceResolver((ROOT/'games/petz4',));a=load_breed_assets(resolver,case['source'],pose='sitting',seed=0,age=100,fatness=50)
    assert SHA((ROOT/'games/petz4'/case['source']).read_bytes())==case['source_sha256']
    states=[dict(f['orientation_state'])[42] for f in case['sequence']['frames']]
    matrix=tuple(states[0]['matrix']);product=transpose_times(matrix,matrix)
    unrounded=[math.atan2(v,product[8])*256/(2*math.pi) if v or product[8] else 0 for v in product[6:8]]
    delta=tuple(_round(v) for v in unrounded);assert delta==(0,-1)
    identity=(256,0,0,0,256,0,0,0,256)
    assert transpose_times(identity,identity)==identity
    after=calc_after_tilt(0,a.frame.balls[a.appearance.key_balls.chest])
    current=TextureOrientation(**{k:tuple(v) for k,v in states[0].items()});checks=[]
    for i in range(1,8):
        current=update_texture_orientation(current,a.frame.balls[42],head_area=body_areas(a.appearance)[42] in _HEAD_AREAS,yaw=0,after_tilt=after)
        expected=TextureOrientation(**{k:tuple(v) for k,v in states[i].items()})
        assert current==expected,(i,current,expected)
        assert current.matrix==matrix and current.frame_angles==delta
        checks.append({'frame':i+1,'angles':current.angles,'frame_delta':current.frame_angles,'matches_saved_post_draw_state':True})
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent;hashes={}
    for name in ('rendering/rotation.py','rendering/texture_rotation.py'):
        content=(installed/name).read_bytes();assert content==(ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes();hashes[name]=SHA(content)
    for path,expected in prior['shared_engine_hashes'].items():assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    for name,version in prior['dependency_versions'].items():assert importlib.metadata.version(name)==version
    report={'experiment':'TEXTURE-002','backend':'direct Python arithmetic and replay of TEXTURE-001 private orientation states; no new images','renderer_revision':prior['renderer_revision'],'python':sys.version,'source_manifest':'texture-001.json','source_sha256':case['source_sha256'],'source_hashes':hashes,'shared_engine_hashes':prior['shared_engine_hashes'],'dependency_versions':prior['dependency_versions'],'observed_matrix':matrix,'transpose_self_product':product,'unrounded_angle_delta':unrounded,'rounded_angle_delta':delta,'identity_control_self_product':identity,'resolved_after_tilt':after,'checks':checks,'limits':'Numerical origin traced in current renderer; no independent native algorithm or game validation.'}
    for p in (OUT/'report.json',ROOT/'experiments/texture-002.json'):p.write_text(json.dumps(report,indent=2)+'\n')
    print(product,unrounded,delta,'Seven saved repeat states match')
if __name__=='__main__':main()
