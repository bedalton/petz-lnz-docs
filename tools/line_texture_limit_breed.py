"""Composed oversized textured-connector versus explicit and absent controls."""
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
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.output import offset_prepared_frame
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineRenderer
from petz_renderer.rendering.connectors import ConnectorBall, build_line_block
from petz_renderer.rendering.texture import TiledTexture, remap_texture
from research_common import ROOT, SHA, adult, write_copy, save_result
OUT=ROOT/'scratch/research/line-015'
VARIANTS={f'{span}_{style}':(offset,color) for span,offset in (('short',-80),('long',-800)) for style,color in (('texture',-1),('explicit',125),('none',None))}
PAIRS=[('short_texture','short_none',False),('short_explicit','short_none',False),('long_texture','long_none',True),('long_explicit','long_none',False)]
def synthetic():return []
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
        head_texture=layer.appearance.balls[head].texture
        assert head_texture>=0
        marker_row=f'{head}, -35, -80, 0, 125, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        frozen=tuple(', '.join(str(int(x)) for x in vars(line).values()) for line in layer.appearance.lines)
        paths={};hashes={};rows={};checks=[]
        for name,(offset,color) in VARIANTS.items():
            s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row.replace('-80',str(offset)))
            s['Color Info Override']=(*base.get('Color Info Override',()),f'{head}, 125, -1, {head_texture}')
            rows[name]=None if color is None else f'{head}, {marker}, 0, {color}, 244, 244, 100, 100, 0, 1'
            s['Linez']=(*frozen,*((rows[name],) if rows[name] else ()))
            path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={n:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for n,p in paths.items()}
            shapes={n:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for n,a in assets.items()}
            for n,a in assets.items():
                span,style=n.split('_');assert shapes[n]==shapes[span+'_texture']
                if style=='none':
                    assert a.appearance.lines==layer.appearance.lines
                    checks.append({'pose':pose,'variant':n,'connector':False});continue
                assert a.appearance.lines[:-1]==layer.appearance.lines
                prepared=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50)
                bounds=prepared.geometry.ordering.bounds
                prepared=offset_prepared_frame(prepared,-bounds.min_x,-bounds.min_y)
                block=build_line_block(a.appearance.lines[-1],tuple(b.endpoint for b in prepared.balls));assert block is not None
                assert (block.paint is not None)==(style=='texture')
                fb=Framebuffer(bounds.max_x-bounds.min_x+1,bounds.max_y-bounds.min_y+1)
                r=LineRenderer(seed=1);r.draw(fb,block)
                count=sum(v!=0 for v in fb.pixels)
                assert (count==0)==(span=='long' and style=='texture'),(species,pose,n,count)
                checks.append({'pose':pose,'variant':n,'connector':True,'paint_present':block.paint is not None,'block_endpoints':[block.x1,block.y1,block.x2,block.y2],'isolated_line_colored_pixels':count,'canvas':[fb.width,fb.height],'tile_size':None if block.paint is None else [block.paint.texture.width,block.paint.texture.height]})
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
    report={'experiment':'LINE-015','backend':'local stdio MCP plus asset-backed connector block checks','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':source_hashes,'engine_hashes':engines,'synthetic':blocks,'cases':cases,'comparisons':renders}
    for path in (OUT/'report.json',ROOT/'experiments/line-015.json'):path.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
