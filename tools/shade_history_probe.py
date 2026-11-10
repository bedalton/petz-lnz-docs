"""SHADE-002: isolate retained ShadeState from ordering/texture/RNG history."""
import asyncio
import base64
import importlib.metadata
import json
import sys
from dataclasses import asdict
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.assembly import GeometryState
from petz_renderer.rendering.shading import ShadeState,update_shading
from petz_renderer.rendering.preparation import FrameState,prepare_frame
from petz_renderer.rendering.output import render_portrait
from morph_pixel_probe import draw,pixel_diff
from static_texture_probe import sheet_png
from shade_slope_probe import rounded_ratio
from research_common import ROOT,SHA
OUT=ROOT/'scratch/research/shade-002'
HISTORIES={'repeat':({}, {}, {}, {}),'small_yaw':({'yaw_delta':2},{'yaw_delta':4},{'yaw_delta':2},{}),'yaw_arc':({'yaw_delta':16},{'yaw_delta':32},{'yaw_delta':16},{}),'head_arc':({'head_rotation':16},{'head_rotation':32},{'head_rotation':16},{})}

def synthetic():
    traces=[]
    for sign in (-1,1):
        for extent in (60,120):
            for slope in (0,100):
                state=ShadeState();events=[]
                for distance,enabled in ((0,True),(10,True),(11,True),(1,True),(0,True),(30,True),(20,True),(19,True),(60,False),(60,True),(49,True)):
                    depths=(0,0,sign*distance);active=(True,True,enabled)
                    prior=state;state=update_shading(state,depths,active,chest=0,butt=1,pose_depth=extent,slope=slope)
                    changed=enabled and abs(sign*distance-prior.last_distances[2])>10
                    expected=max(-6,min(6,rounded_ratio(sign*distance*3*(slope+110),25*extent))) if changed else prior.offsets[2]
                    assert state.offsets[2]==expected
                    assert state.last_distances[2]==(sign*distance if changed else prior.last_distances[2])
                    events.append({'distance':sign*distance,'active':enabled,'updated':changed,'offset':state.offsets[2],'last_distance':state.last_distances[2]})
                traces.append({'slope':slope,'pose_depth':extent,'events':events})
    # Zero depth or invalid anchors preserves the exact object and all saved history.
    guards=[]
    for chest,butt,extent in ((-1,1,120),(0,3,120),(0,1,0)):
        result=update_shading(state,(0,0,100),(True,)*3,chest=chest,butt=butt,pose_depth=extent,slope=100)
        assert result is state;guards.append({'chest':chest,'butt':butt,'pose_depth':extent,'identity_preserved':True})
    # Midpoint division truncates toward zero, including a negative odd sum.
    midpoint=[]
    for chest_z,butt_z,middle in ((-2,-1,-1),(-1,0,0),(1,2,1)):
        state=update_shading(ShadeState(),(chest_z,butt_z,10),(True,)*3,chest=0,butt=1,pose_depth=120,slope=0)
        assert state.last_distances[2]==10-middle
        midpoint.append({'depths':[chest_z,butt_z,10],'expected_middle':middle,'target_distance':state.last_distances[2]})
    # Only first512 slots participate; surplus inputs are accepted and cannot grow state.
    state=update_shading(ShadeState(),(0,)*513,(True,)*513,chest=0,butt=1,pose_depth=120,slope=0)
    assert len(state.offsets)==512 and state.last_distances==(0,)*512
    return {'threshold_traces':traces,'guards':guards,'midpoints':midpoint,'slot_limit':512}

def compose(a,target,steps):
    fresh=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,**target)
    bounds=fresh.geometry.ordering.bounds
    first=draw(a,fresh,bounds);shade=fresh.state.geometry.shade;trace=[]
    for changes in steps:
        controls=dict(target);controls.update({k:v for k,v in changes.items() if k!='yaw_delta'});controls['yaw']+=changes.get('yaw_delta',0)
        state=FrameState(geometry=GeometryState(shade=shade))
        current=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,**controls)
        shade=current.state.geometry.shade
        trace.append({'controls':controls,'shade':asdict(shade)})
    assert current.geometry.balls==fresh.geometry.balls
    assert current.geometry.ordering==fresh.geometry.ordering
    assert current.state.orientations==fresh.state.orientations
    second=draw(a,current,bounds)
    png,hashes,size=sheet_png((first[2],second[2]))
    record={'cell_size':size,'cell_labels':['fresh','retained_shade_only'],'cell_hashes':hashes,'indexed_hashes':[SHA(o[0].pixels) for o in (first,second)],'changed_pixels':pixel_diff(first[0].pixels,second[0].pixels),'changed_offsets':[i for i,(x,y) in enumerate(zip(fresh.geometry.state.shade.offsets,shade.offsets)) if x!=y],'changed_fills':[i for i,(x,y) in enumerate(zip(fresh.geometry.fills,current.geometry.fills)) if x!=y],'changed_circles':[i for i,(x,y) in enumerate(zip(fresh.balls,current.balls)) if x.circle!=y.circle],'fresh_offsets':list(fresh.geometry.state.shade.offsets[:len(fresh.balls)]),'retained_offsets':list(shade.offsets[:len(fresh.balls)]),'same_geometry':True,'same_order':True,'same_prepared_orientations':True}
    private={'trace':trace,'fresh_shade':asdict(fresh.state.geometry.shade),'final_shade':asdict(shade),'indexed_pixels':[list(o[0].pixels) for o in (first,second)]}
    return record,private,png,first[2]

async def main():
    OUT.mkdir(parents=True,exist_ok=False);direct=synthetic();cases=[];baselines=[]
    prior=json.loads((ROOT/'experiments/shade-001.json').read_text());input_root=ROOT/'scratch/research/shade-001';resolver=ResourceResolver((ROOT/'games/petz4',input_root))
    for c in prior['cases']:
        assert SHA((ROOT/c['source_path']).read_bytes())==c['source_sha256']
        for variant in ('zero','strong'):
            filename=c['paths'][variant];digest=c['input_hashes'][variant];assert SHA((input_root/filename).read_bytes())==digest
            for pose in ('standing','sitting','lying'):
                a=load_breed_assets(resolver,filename,pose=pose,seed=0,age=100,fatness=50)
                for degrees,yaw in ((0,0),(90,64)):
                    target={'yaw':yaw,'fatness':50};stem=f"{c['species']}-{variant}-{pose}-{degrees}"
                    for history,steps in HISTORIES.items():
                        rec,private,png,baseline=compose(a,target,steps)
                        assert baseline==render_portrait(a,**target).png
                        sheet=f'{stem}-{history}.png';(OUT/sheet).write_bytes(png)
                        statefile=f'{stem}-{history}-state.json';raw=json.dumps(private,separators=(',',':')).encode();(OUT/statefile).write_bytes(raw)
                        rec.update(species=c['species'],variant=variant,pose=pose,yaw_degrees=degrees,yaw_units=yaw,history=history,input=filename,input_sha256=digest,sheet=sheet,sheet_sha256=SHA(png),private_state_file=statefile,private_state_sha256=SHA(raw))
                        cases.append(rec)
                        if history=='repeat':
                            name=f'{stem}-baseline.png';(OUT/name).write_bytes(baseline)
                            baselines.append({'species':c['species'],'variant':variant,'pose':pose,'yaw_degrees':degrees,'input':filename,'input_sha256':digest,'png':name,'png_sha256':SHA(baseline)})
                    print(stem,[r['changed_pixels'] for r in cases[-4:]],flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(input_root)])
    async with Client(transport) as client:
        for b in baselines:
            result=await client.call_tool('render_pet',{'path':b['input'],'pose':b['pose'],'seed':0,'age':100,'fatness':50,'yaw_degrees':b['yaw_degrees']});assert not result.is_error
            png=base64.b64decode(next(x.data for x in result.content if x.type=='image'));assert SHA(png)==b['png_sha256']
            assert result.data['game_version']=='petz4';b['local_mcp_match']=True
            (OUT/(Path(b['png']).stem+'-mcp.json')).write_text(json.dumps(result.data,indent=2)+'\n')
    package=Path(petz_renderer.__file__).parent;sources={n:SHA((package/n).read_bytes()) for n in ('rendering/shading.py','rendering/assembly.py','rendering/preparation.py','rendering/output.py','rendering/composition.py','rendering/ordering.py','rendering/texture.py','rendering/lines.py')}
    for n,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/n).read_bytes())==h
    for n,h in prior['engine_hashes'].items():assert SHA((ROOT/n).read_bytes())==h
    summary={history:{'cases':sum(c['history']==history for c in cases),'changed_pixels':sum(c['history']==history and c['changed_pixels']>0 for c in cases),'changed_offsets':sum(c['history']==history and bool(c['changed_offsets']) for c in cases),'changed_fills':sum(c['history']==history and bool(c['changed_fills']) for c in cases)} for history in HISTORIES}
    report={'experiment':'SHADE-002','backend':'direct ShadeState-only preparations; local stdio MCP fresh baselines only','renderer_revision':prior['renderer_revision'],'python':sys.version,'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':sources,'engine_hashes':prior['engine_hashes'],'reused_manifest':'shade-001.json','controls':{'seed':0,'age':100,'fatness':50,'raster_seed':1,'raster_step':0,'retained_component':'ShadeState only','history_units':'engine turns/256','frame':'fixed named pose throughout each case'},'histories':HISTORIES,'synthetic':direct,'baselines':baselines,'cases':cases,'summary':summary}
    for path in (OUT/'report.json',ROOT/'experiments/shade-002.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print(summary,flush=True)
if __name__=='__main__':asyncio.run(main())
