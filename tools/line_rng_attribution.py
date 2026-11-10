"""LINE-012: per-connector RNG substitution inside fixed prepared scenes."""
import importlib.metadata,json,sys
from pathlib import Path
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,draw_prepared_frame
from petz_renderer.rendering.output import offset_prepared_frame,encode_png
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineRenderer
from petz_renderer.rendering.connectors import build_line_block
from static_texture_probe import sheet_png
from line_composed_history import line_state
from research_common import ROOT,SHA,adult
OUT=ROOT/'scratch/research/line-012'
def restore(r,state):
    r._state=state['rng'];r._tables=[list(t) for t in state['tables']]
class Traced(LineRenderer):
    def __init__(self,target,substitute=None,all_substitute=None):
        super().__init__(seed=1);self.target=target;self.substitute=substitute;self.all_substitute=all_substitute;self.visits=[];self.all_visits=[];self.fuzzes=[]
    def draw(self,fb,block):
        index=len(self.all_visits);self.all_visits.append(line_state(self));self.fuzzes.append(block.fuzz)
        if block==self.target:self.visits.append(line_state(self))
        substitute=self.all_substitute[index] if self.all_substitute is not None and block.fuzz>0 else (self.substitute if block==self.target else None)
        if substitute is None:return super().draw(fb,block)
        # Advance the main renderer exactly as it would normally draw the target.
        # Discard these pixels; a separate renderer draws only its substituted pixels.
        super().draw(Framebuffer(fb.width,fb.height,background=255),block)
        alternate=LineRenderer(seed=1);restore(alternate,substitute);alternate.draw(fb,block)
def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];states=[]
    prior=json.loads((ROOT/'experiments/line-011.json').read_text());resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/line-007'))
    for fixture in prior['cases']:
        path=ROOT/fixture['input'];assert SHA(path.read_bytes())==fixture['input_sha256']
        source,raw,*_=adult(fixture['species']);assert SHA(raw)==fixture['source_sha256']
        a=load_breed_assets(resolver,path.name,pose=fixture['pose'],seed=0,age=100,fatness=50)
        p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50,yaw=fixture['yaw_degrees']*256//360)
        b=p.geometry.ordering.bounds;w,h=b.max_x-b.min_x+1,b.max_y-b.min_y+1
        shifted=offset_prepared_frame(p,-b.min_x,-b.min_y)
        target=build_line_block(a.appearance.lines[-1],tuple(ball.endpoint for ball in shifted.balls),omissions=a.appearance.omissions,mode=a.appearance.line_render_mode)
        assert target is not None and target.fuzz==7
        def draw(primed,substitute=None,all_substitute=None):
            r=Traced(target,substitute,all_substitute)
            if primed:r.draw_whisker(Framebuffer(100,100),15,15,85,70,125,step=0)
            fb=Framebuffer(w,h,background=255)
            draw_prepared_frame(fb,shifted,a.appearance,line_renderer=r,step=1,seed=1)
            assert len(r.visits)==1
            return fb,encode_png(fb,a.palette),r.visits[0],line_state(r),r.all_visits,r.fuzzes
        fresh=draw(False);primed=draw(True)
        target_only=draw(False,primed[2]);others_only=draw(True,fresh[2])
        all_lines=draw(False,all_substitute=primed[4]);except_lines=draw(True,all_substitute=fresh[4])
        assert all_lines[3]==fresh[3] and except_lines[3]==primed[3]
        # State substitution changes pixels only, preserving each path's own final state.
        assert fresh[3]==target_only[3] and primed[3]==others_only[3]
        pngs=[r[1] for r in (fresh,primed,target_only,others_only,all_lines,except_lines)]
        png,hashes,size=sheet_png(pngs);stem=f"{fixture['species']}-{fixture['pose']}-{fixture['yaw_degrees']}";(OUT/f'{stem}.png').write_bytes(png)
        base=fresh[0].pixels;pp=primed[0].pixels;tp=target_only[0].pixels;op=others_only[0].pixels
        dif=lambda x,y:sum(a!=b for a,b in zip(x,y,strict=True))
        case={'species':fixture['species'],'pose':fixture['pose'],'yaw_degrees':fixture['yaw_degrees'],'input':fixture['input'],'input_sha256':fixture['input_sha256'],'source_sha256':fixture['source_sha256'],'sheet':f'{stem}.png','sheet_sha256':SHA(png),'cell_size':size,'cell_labels':['fresh','whisker0_primed','only_target_connector_primed','primed_except_target_connector','all_positive_fuzz_lines_primed','primed_except_positive_fuzz_lines'],'cell_hashes':hashes,'primed_vs_fresh':dif(pp,base),'target_only_vs_fresh':dif(tp,base),'target_only_vs_primed':dif(tp,pp),'others_only_vs_fresh':dif(op,base),'all_fuzzy_vs_primed':dif(all_lines[0].pixels,pp),'except_fuzzy_vs_fresh':dif(except_lines[0].pixels,base),'positive_fuzz_draw_count':sum(f>0 for f in fresh[5]),'line_draw_count':len(fresh[5]),'fresh_matches_line011':hashes[0]['rgba_sha256']==fixture['cell_hashes'][1]['rgba_sha256'],'primed_matches_line011':hashes[1]['rgba_sha256']==fixture['cell_hashes'][5]['rgba_sha256']}
        assert case['fresh_matches_line011'] and case['primed_matches_line011']
        for label,result in zip(case['cell_labels'],(fresh,primed,target_only,others_only,all_lines,except_lines),strict=True):
            state={'before_target':result[2],'after_scene':result[3]};case[label+'_state_sha256']=SHA(json.dumps(state,sort_keys=True).encode());states.append({'fixture':stem,'label':label,'state':state})
        cases.append(case);print(stem,case['primed_vs_fresh'],case['target_only_vs_primed'],case['others_only_vs_fresh'],flush=True)
    installed=Path(petz_renderer.__file__).parent;sources={n:SHA((installed/n).read_bytes()) for n in ('rendering/lines.py','rendering/preparation.py','rendering/composition.py','rendering/connectors.py','rendering/output.py')}
    for n,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/n).read_bytes())==h
    for n,h in prior['engine_hashes'].items():assert SHA((ROOT/n).read_bytes())==h
    report={'experiment':'LINE-012','backend':'direct Python per-connector state substitution; reuses LINE-011 exact MCP-backed controls, no new MCP','renderer_revision':prior['renderer_revision'],'python':sys.version,'source_hashes':sources,'engine_hashes':prior['engine_hashes'],'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','Pillow')},'controls':prior['controls'],'cases':cases,'summary':{'fixtures':len(cases),'target_only_matches_primed':sum(c['target_only_vs_primed']==0 for c in cases),'others_only_matches_fresh':sum(c['others_only_vs_fresh']==0 for c in cases),'all_fuzzy_matches_primed':sum(c['all_fuzzy_vs_primed']==0 for c in cases),'except_fuzzy_matches_fresh':sum(c['except_fuzzy_vs_fresh']==0 for c in cases)}}
    (OUT/'states.json').write_text(json.dumps(states,indent=2)+'\n')
    for dest in (OUT/'report.json',ROOT/'experiments/line-012.json'):dest.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']))
if __name__=='__main__':main()
