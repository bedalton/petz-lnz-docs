"""Connector edge modes/colors: isolated raster and copy-only controls."""
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
OUT=ROOT/'scratch/research/line-006'
VARIANTS={'scan':(0,180,200),'polygon':(1,180,200),'plain':(-1,180,200),'invalid':(2,180,200),'inherit':(0,-1,-1),'explicit_fill':(0,220,220),'marker':None}
PAIRS=[('inherit','explicit_fill',True),('scan','plain',False),('polygon','plain',False),('scan','polygon',False),('invalid','marker',True)]
def synthetic():
    from petz_renderer.rendering.framebuffer import Framebuffer
    from petz_renderer.rendering.lines import LineBlock,LineRenderer
    rows=[]
    for endpoints in ((20,20,80,70),(80,70,20,20),(20,50,80,50),(50,20,50,80)):
        for widths in ((12,12),(20,6)):
            outputs={}
            for name,style in VARIANTS.items():
                if style is None:continue
                mode,left,right=style
                block=LineBlock(*endpoints,start_thick=widths[0],end_thick=widths[1],color=220,left_color=left,right_color=right,edge_mode=mode)
                fb=Framebuffer(100,100);LineRenderer(seed=1).draw(fb,block)
                counts={str(c):fb.pixels.count(c) for c in (0,220,180,200)}
                outputs[name]=fb.pixels
                if name=='invalid':assert counts['0']==10000
                if name in ('plain','inherit','explicit_fill'):assert counts['180']==counts['200']==0
                if name in ('scan','polygon'):assert counts['180']>0 and counts['200']>0
                rows.append({'endpoints':endpoints,'widths':widths,'variant':name,'pixel_counts':counts,'indexed_sha256':SHA(fb.pixels)})
            assert outputs['inherit']==outputs['explicit_fill']==outputs['plain']
            assert outputs['scan']!=outputs['plain'] and outputs['polygon']!=outputs['plain']
    return rows
async def main():
    OUT.mkdir(parents=True,exist_ok=False); blocks=synthetic();cases=[];renders=[]
    package=Path(petz_renderer.__file__).parent
    source_hashes={p:SHA((package/p).read_bytes()) for p in ('appearance/core.py','rendering/connectors.py','rendering/shading.py','rendering/texture.py','rendering/lines.py')}
    for p,h in source_hashes.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    engines={str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in sorted((ROOT/'games/petz4').glob('Resource/* 4 Rez.dll'))}
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        marker_row=f'{head}, -35, -80, 0, 200, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        frozen=tuple(', '.join(str(int(x)) for x in vars(line).values()) for line in layer.appearance.lines)
        paths={};hashes={};rows={};checks=[]
        for name,style in VARIANTS.items():
            s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row)
            s['Color Info Override']=(*base.get('Color Info Override',()),f'{head}, 180, -1, -1')
            rows[name]=None if style is None else f'{head}, {marker}, 0, 220, {style[1]}, {style[2]}, 100, 100, {style[0]}, 1'
            s['Linez']=(*frozen,*((rows[name],) if rows[name] else ()))
            path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={n:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for n,p in paths.items()}
            shapes={n:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for n,a in assets.items()}
            for n,a in assets.items():
                assert shapes[n]==shapes['marker']
                if n=='marker':assert a.appearance.lines==layer.appearance.lines
                else:
                    assert a.appearance.lines[:-1]==layer.appearance.lines
                    line=a.appearance.lines[-1]
                    assert (line.edge_mode,line.left_color,line.right_color)==VARIANTS[n]
                checks.append({'pose':pose,'variant':n,'style':VARIANTS[n]})
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
    report={'experiment':'LINE-006','backend':'local stdio MCP and synthetic Python blocks','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':source_hashes,'engine_hashes':engines,'synthetic':blocks,'cases':cases,'comparisons':renders}
    for path in (OUT/'report.json',ROOT/'experiments/line-006.json'):path.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
