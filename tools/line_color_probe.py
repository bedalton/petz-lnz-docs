"""Connector fill selection: synthetic blocks and copy-only Petz 4 controls."""
import asyncio, importlib.metadata, json, sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.appearance.core import Line
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.connectors import ConnectorBall, build_line_block
from petz_renderer.rendering.texture import TiledTexture, remap_texture
from research_common import ROOT, SHA, adult, write_copy, save_result
OUT=ROOT/'scratch/research/line-005'
# All endpoint colors are diagnostic, texture-free and outside shadeable bands.
VARIANTS={'start':(-1,False),'end':(-2,False),'explicit_start':(180,False),'explicit_end':(200,False),'reverse_start':(-1,True),'reverse_end':(-2,True)}
PAIRS=[('start','explicit_start',True),('end','explicit_end',True),('start','end',False),('reverse_start','explicit_end',True),('reverse_end','explicit_start',True)]
def synthetic():
    rows=[]
    texture=TiledTexture(2,2,bytes((10,11,12,13)),2,2)
    for textured in (False,True):
        for reverse in (False,True):
            for shades in ((0,0),(-5,2),(6,6)):
                balls=(ConnectorBall(10,10,15,25,shades[0],texture=texture if textured else None),ConnectorBall(80,40,10,85,shades[1],texture=texture if textured else None))
                for color in (-3,-2,-1,0,125,200):
                    start,end=(1,0) if reverse else (0,1)
                    line=Line(start,end,0,color,244,244,100,100,0,True)
                    block=build_line_block(line,balls);assert block is not None
                    source=balls[start if color==-1 else end]
                    selected=color if color>=0 else source.base_color
                    shade=int(sum(shades)/2)
                    expected=max((selected-10)//10*10+10,min((selected-10)//10*10+19,selected+shade)) if 10<=selected<=149 else selected
                    assert block.color==expected
                    expected_paint=remap_texture(texture,expected,has_levels=False,own_level=-1) if textured and color<0 else None
                    assert block.paint==expected_paint
                    rows.append({'textured':textured,'reverse':reverse,'shades':shades,'color_field':color,'expected_color':expected,'texture_inherited':block.paint is not None})
    return rows
async def main():
    OUT.mkdir(parents=True,exist_ok=False); blocks=synthetic();cases=[];renders=[]
    package=Path(petz_renderer.__file__).parent
    source_hashes={p:SHA((package/p).read_bytes()) for p in ('appearance/core.py','rendering/connectors.py','rendering/shading.py','rendering/texture.py')}
    for p,h in source_hashes.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    engines={str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in sorted((ROOT/'games/petz4').glob('Resource/* 4 Rez.dll'))}
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        marker_row=f'{head}, -35, -80, 0, 200, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        frozen=tuple(', '.join(str(int(x)) for x in vars(line).values()) for line in layer.appearance.lines)
        paths={};hashes={};rows={};checks=[]
        for name,(color,reverse) in VARIANTS.items():
            s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row)
            s['Color Info Override']=(*base.get('Color Info Override',()),f'{head}, 180, -1, -1')
            a,b=(marker,head) if reverse else (head,marker)
            rows[name]=f'{a}, {b}, 0, {color}, 244, 244, 100, 100, 0, 1'
            s['Linez']=(*frozen,rows[name])
            path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={n:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for n,p in paths.items()}
            shapes={n:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for n,a in assets.items()}
            for n,a in assets.items():
                assert shapes[n]==shapes['start']
                assert a.appearance.lines[:-1]==layer.appearance.lines
                assert a.appearance.lines[-1].color==VARIANTS[n][0]
                checks.append({'pose':pose,'variant':n,'line_color':a.appearance.lines[-1].color})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'marker_row':marker_row,'line_rows':rows,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after,expected in PAIRS:
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal==expected,(stem,equal,expected)
                    renders.append({'species':c['species'],'pair':[before,after],'controls':args,'png_sha256':SHA(png),'cells_equal':equal,'cell_hashes':[x['pixel_sha256'] for x in meta['cells']]})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'LINE-005','backend':'local stdio MCP and synthetic Python blocks','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':source_hashes,'engine_hashes':engines,'synthetic':blocks,'cases':cases,'comparisons':renders}
    for path in (OUT/'report.json',ROOT/'experiments/line-005.json'):path.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
