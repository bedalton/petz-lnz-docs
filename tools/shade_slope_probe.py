"""SHADE-001: scalar depth gain and palette-band controls, without game claims."""
import asyncio
import importlib.metadata
import json
import sys
from dataclasses import asdict
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.appearance.core import read_core
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.assembly import assemble_geometry
from petz_renderer.rendering.shading import ShadeState, shade_color, update_shading
from research_common import ROOT, SHA, adult, write_copy, save_result
OUT=ROOT/'scratch/research/shade-001'
VARIANTS={'absent':None,'empty':0,'zero':0,'neutral':-110,'weak':-100,'strong':100,'reverse':-220}

def rounded_ratio(n,d):
    return (1 if n>=0 else -1)*((2*abs(n)+d)//(2*d))

def synthetic():
    parser=[]
    for rows,expected in ((None,0),((),0),(('bad',),0),(('0',),0),(('-110',),-110),(('100',),100)):
        actual=read_core({} if rows is None else {'Z Shade Slope':rows}).z_shade_slope
        assert actual==expected
        parser.append({'rows':rows,'expected':expected})
    arithmetic=[]
    for slope in (-220,-110,-100,0,100):
        for extent in (60,120,240):
            depths=(0,0,*range(-120,121,5))
            state=update_shading(ShadeState(),depths,(True,)*len(depths),chest=0,butt=1,pose_depth=extent,slope=slope)
            expected=tuple(max(-6,min(6,rounded_ratio(z*3*(slope+110),25*extent))) for z in depths)
            assert state.offsets[:len(depths)]==expected
            assert state.last_distances[:len(depths)]==depths
            arithmetic.append({'slope':slope,'pose_depth':extent,'depths':depths,'offsets':expected})
    palette=[]
    for color in range(256):
        for offset in range(-6,7):
            actual=shade_color(color,offset)
            band=10+10*((color-10)//10)
            expected=max(band,min(band+9,color+offset)) if 10<=color<=149 else color
            assert actual==expected
            palette.append(actual)
    return {'parser':parser,'arithmetic':arithmetic,'palette_assertions':len(palette),'palette_outputs_sha256':SHA(bytes(palette))}

def numerical(folder,case):
    rows=[];resolver=ResourceResolver((ROOT/'games/petz4',folder))
    for pose in ('standing','sitting','lying'):
        for yaw in (0,64):
            baseline=None
            for name,slope in VARIANTS.items():
                a=load_breed_assets(resolver,case['paths'][name],pose=pose,seed=0,age=100,fatness=50)
                assert a.appearance.z_shade_slope==(case['inherited_slope'] if slope is None else slope)
                g=assemble_geometry(a.appearance,a.sizes,a.frame,fatness=50,yaw=yaw)
                invariant=(g.balls,g.areas,g.irises,g.ordering)
                if baseline is None:baseline=invariant
                assert invariant==baseline
                keys=a.appearance.key_balls;middle=int((g.balls[keys.chest].z+g.balls[keys.butt].z)/2)
                for i,b in enumerate(g.balls):
                    if not b.parked:
                        expected=max(-6,min(6,rounded_ratio((b.z-middle)*3*((case['inherited_slope'] if slope is None else slope)+110),25*g.ordering.bounds.depth)))
                        assert g.state.shade.offset(i)==expected
                if name=='neutral':assert set(g.state.shade.offsets)=={0}
                rows.append({'pose':pose,'yaw':yaw,'variant':name,'bounds':asdict(g.ordering.bounds),'offsets':list(g.state.shade.offsets[:len(g.balls)]),'last_distances':list(g.state.shade.last_distances[:len(g.balls)]),'fills':list(g.fills),'geometry_sha256':SHA(repr(invariant).encode())})
    return rows

async def main():
    OUT.mkdir(parents=True,exist_ok=False);direct=synthetic();cases=[];renders=[]
    package=Path(petz_renderer.__file__).parent
    sources={p:SHA((package/p).read_bytes()) for p in ('appearance/core.py','rendering/assembly.py','rendering/shading.py','rendering/ordering.py','rendering/preparation.py')}
    for p,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    engines={str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in sorted((ROOT/'games/petz4').glob('Resource/* 4 Rez.dll'))}
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species);paths={};hashes={}
        inherited=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0).appearance.z_shade_slope
        for name,slope in VARIANTS.items():
            sections=dict(base);sections.pop('Z Shade Slope',None)
            if slope is not None:sections['Z Shade Slope']=() if name=='empty' else (str(slope),)
            path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,sections,path)
        case={'species':species,'source_path':str(source.relative_to(ROOT)),'source_sha256':SHA(raw),'inherited_slope':inherited,'paths':paths,'input_hashes':hashes}
        case['checks']=numerical(OUT,case);cases.append(case)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after in (('absent','strong'),('empty','zero'),('neutral','zero'),('weak','zero'),('zero','strong'),('zero','reverse')):
                for pose in ('standing','sitting'):
                    for yaw in (0,90):
                        args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':pose,'seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                        stem=f"{c['species']}-{pose}-{before}-{after}-{yaw}"
                        png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                        equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                        assert meta['game_version']=='petz4'
                        if before in ('absent','empty'):assert equal
                        renders.append({'species':c['species'],'pair':[before,after],'stem':stem,'controls':args,'png_sha256':SHA(png),'game_version':meta['game_version'],'renderer_version':meta['renderer_version'],'cells_equal':equal,'cell_hashes':[x['pixel_sha256'] for x in meta['cells']]})
                        (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,equal,flush=True)
    for c in cases:assert SHA((ROOT/c['source_path']).read_bytes())==c['source_sha256']
    report={'experiment':'SHADE-001','backend':'local stdio MCP, asset-backed assembly and asset-free arithmetic','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':sources,'engine_hashes':engines,'synthetic':direct,'cases':cases,'comparisons':renders}
    for path in (OUT/'report.json',ROOT/'experiments/shade-001.json'):path.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
