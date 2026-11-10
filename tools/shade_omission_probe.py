"""SHADE-003: omission-induced depth bounds and nonlocal fresh shading."""
import asyncio,json,sys,importlib.metadata
from dataclasses import replace,asdict
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.assembly import assemble_geometry,GeometryState
from petz_renderer.rendering.preparation import prepare_frame,FrameState
from petz_renderer.rendering.shading import ShadeState,update_shading
from morph_pixel_probe import draw,pixel_diff
from static_texture_probe import sheet_png
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/shade-003'

def scan(a,yaw):
    target={'fatness':50,'yaw':yaw};base=assemble_geometry(a.appearance,a.sizes,a.frame,**target);rows=[]
    coords=lambda g:tuple((b.x,b.y,b.z,b.radius,b.parked) for b in g.balls)
    for i in range(67):
        app=replace(a.appearance,omissions=a.appearance.omissions|{i})
        g=assemble_geometry(app,a.sizes,a.frame,**target);assert coords(g)==coords(base)
        keys=app.key_balls
        original_depth=update_shading(ShadeState(),tuple(b.z for b in g.balls),tuple(not b.parked for b in g.balls),chest=keys.chest,butt=keys.butt,pose_depth=base.ordering.bounds.depth,slope=app.z_shade_slope)
        assert original_depth==base.state.shade
        if g.ordering.bounds.depth==base.ordering.bounds.depth:assert g.state.shade==base.state.shade and g.fills==base.fills
        rows.append({'omitted_id':i,'depth':g.ordering.bounds.depth,'changed_offsets':[j for j,(x,y) in enumerate(zip(base.state.shade.offsets,g.state.shade.offsets)) if x!=y],'changed_fills':[j for j,(x,y) in enumerate(zip(base.fills,g.fills)) if x!=y],'was_visible':base.balls[i].visible,'was_parked':base.balls[i].parked})
    return {'base_depth':base.ordering.bounds.depth,'rows':rows}

def composition(a,yaw,ball):
    target={'fatness':50,'yaw':yaw};base=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,**target)
    app=replace(a.appearance,omissions=a.appearance.omissions|{ball})
    altered=prepare_frame(app,a.sizes,a.frame,textures=a.textures,**target)
    held=prepare_frame(app,a.sizes,a.frame,textures=a.textures,state=FrameState(geometry=GeometryState(shade=base.state.geometry.shade)),**target)
    assert altered.geometry.balls==held.geometry.balls and altered.geometry.ordering==held.geometry.ordering and altered.state.orientations==held.state.orientations
    assert held.geometry.fills==base.geometry.fills and held.state.geometry.shade==base.state.geometry.shade
    bounds=base.geometry.ordering.bounds
    output=[draw(replace(a,appearance=which),p,bounds) for which,p in ((a.appearance,base),(app,altered),(app,held))]
    png,hashes,size=sheet_png([o[2] for o in output])
    record={'cell_size':size,'cell_labels':['baseline','omitted_fresh','omitted_original_shade'],'cell_hashes':hashes,'indexed_hashes':[SHA(o[0].pixels) for o in output],'omitted_vs_held_changed_pixels':pixel_diff(output[1][0].pixels,output[2][0].pixels),'baseline_vs_omitted_changed_pixels':pixel_diff(output[0][0].pixels,output[1][0].pixels),'fresh_depth':base.geometry.ordering.bounds.depth,'omitted_depth':altered.geometry.ordering.bounds.depth,'fresh_offsets':list(base.state.geometry.shade.offsets[:len(base.balls)]),'omitted_offsets':list(altered.state.geometry.shade.offsets[:len(base.balls)])}
    private={'indexed_pixels':[list(o[0].pixels) for o in output]}
    return record,private,png

async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];scans=[];inputs=[];comparisons=[]
    prior=json.loads((ROOT/'experiments/shade-001.json').read_text());input_root=ROOT/'scratch/research/shade-001';resolver=ResourceResolver((ROOT/'games/petz4',input_root))
    for c in prior['cases']:
        species=c['species'];filename=c['paths']['strong'];source,raw,leaf,base,_,_=adult(species)
        assert SHA(raw)==c['source_sha256'] and SHA((input_root/filename).read_bytes())==c['input_hashes']['strong']
        needed=set();todo=[]
        for pose in ('standing','sitting','lying'):
            a=load_breed_assets(resolver,filename,pose=pose,seed=0,age=100,fatness=50)
            for degrees,yaw in ((0,0),(90,64)):
                result=scan(a,yaw);scans.append({'species':species,'pose':pose,'yaw_units':yaw,**result})
                selected=[r for r in result['rows'] if r['depth']!=result['base_depth']]
                control=next(r for r in result['rows'] if r['depth']==result['base_depth'] and r['was_visible'] and not r['was_parked'])
                for row in (*selected,control):
                    ball=row['omitted_id'];needed.add(ball);stem=f'{species}-{pose}-{degrees}-omit{ball}'
                    rec,private,png=composition(a,yaw,ball);sheet=stem+'.png';(OUT/sheet).write_bytes(png)
                    payload=json.dumps(private,separators=(',',':')).encode();statefile=stem+'-pixels.json';(OUT/statefile).write_bytes(payload)
                    rec.update(species=species,pose=pose,yaw_degrees=degrees,yaw_units=yaw,omitted_id=ball,is_depth_control=row is control,sheet=sheet,sheet_sha256=SHA(png),private_pixels_file=statefile,private_pixels_sha256=SHA(payload))
                    if row is control:assert rec['omitted_vs_held_changed_pixels']==0
                    cases.append(rec);todo.append((pose,degrees,ball,stem))
        paths={};hashes={}
        # Strong baseline reproduces SHADE-001, with only Omissions changed in variants.
        for ball in (None,*sorted(needed)):
            s=dict(base);s['Z Shade Slope']=('100',)
            if ball is not None:
                a=load_breed_assets(resolver,filename,pose='standing',seed=0,age=100,fatness=50)
                s['Omissions']=tuple(str(i) for i in sorted(a.appearance.omissions|{ball}))
            name='baseline' if ball is None else f'omit{ball}';path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,s,path)
        assert hashes['baseline']==c['input_hashes']['strong']
        inputs.append({'species':species,'source_path':c['source_path'],'source_sha256':c['source_sha256'],'paths':paths,'input_hashes':hashes,'todo':todo})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in inputs:
            for pose,degrees,ball,stem in c['todo']:
                args={'before_path':c['paths']['baseline'],'after_path':c['paths'][f'omit{ball}'],'pose':pose,'seed':0,'age':100,'fatness':50,'yaw_degrees':degrees}
                png,meta=await save_result(client,'compare_appearance',args,OUT,stem+'-mcp');assert meta['game_version']=='petz4'
                comparisons.append({'stem':stem+'-mcp','controls':args,'game_version':meta['game_version'],'renderer_version':meta['renderer_version'],'png_sha256':SHA(png),'cell_hashes':[x['pixel_sha256'] for x in meta['cells']]})
    package=Path(petz_renderer.__file__).parent;sources={n:SHA((package/n).read_bytes()) for n in ('rendering/shading.py','rendering/assembly.py','rendering/preparation.py','rendering/attachment.py','rendering/ordering.py','rendering/output.py')}
    for n,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/n).read_bytes())==h
    for n,h in prior['engine_hashes'].items():assert SHA((ROOT/n).read_bytes())==h
    summary={'sweep_cases':sum(len(s['rows']) for s in scans),'depth_changed':sum(r['depth']!=s['base_depth'] for s in scans for r in s['rows']),'fill_changed':sum(bool(r['changed_fills']) for s in scans for r in s['rows']),'compositions':len(cases),'shade_pixel_changed':sum(bool(c['omitted_vs_held_changed_pixels']) for c in cases),'mcp_pairs':len(comparisons)}
    report={'experiment':'SHADE-003','backend':'asset-backed omission sweep and isolated shade controls; local stdio MCP pairs','renderer_revision':prior['renderer_revision'],'python':sys.version,'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':sources,'engine_hashes':prior['engine_hashes'],'controls':{'seed':0,'age':100,'fatness':50,'slope':100,'raster_seed':1,'raster_step':0},'inputs':inputs,'scans':scans,'cases':cases,'comparisons':comparisons,'summary':summary}
    for path in (OUT/'report.json',ROOT/'experiments/shade-003.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print(summary,flush=True)
if __name__=='__main__':asyncio.run(main())
