"""LINE-021: isolated appended texture slots and composed tile dimensions."""
import asyncio
import importlib.metadata
import json
import sys
from dataclasses import replace
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.connectors import build_line_block
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineRenderer
from research_common import ROOT, SHA, adult, write_copy, save_result
OUT=ROOT/'scratch/research/line-021'
DIMS=((32,256),(256,32),(64,64),(128,128),(256,256))

async def main():
    OUT.mkdir(parents=True,exist_ok=False)
    cases=[];renders=[]
    package=Path(petz_renderer.__file__).parent
    sources={p:SHA((package/p).read_bytes()) for p in ('appearance/core.py','rendering/connectors.py','rendering/texture.py','rendering/lines.py','rendering/preparation.py')}
    for p,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    engines={str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in sorted((ROOT/'games/petz4').glob('Resource/* 4 Rez.dll'))}
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        slot=len(layer.appearance.textures);art=layer.appearance.textures[layer.appearance.balls[head].texture].path
        # Explicitly preserve every effective stock slot and connector.
        stock_textures=tuple(f'{t.path}, {1 if t.has_levels else 0}, {t.tile_width}, {t.tile_height}' for t in layer.appearance.textures)
        assert all(t.own_level==-1 for t in layer.appearance.textures)
        stock_lines=tuple(', '.join(str(int(v)) for v in vars(line).values()) for line in layer.appearance.lines)
        for width,height in DIMS:
            paths={};hashes={};checks=[]
            for variant in ('textured','explicit','absent'):
                sections=dict(base)
                sections['Texture List']=(*stock_textures,f'{art}, 1, {width}, {height}')
                sections['Add Ball']=(*base['Add Ball'],f'{head}, -35, -160, 0, 125, 244, -1, 0, -1, -1, 20, 0, 0, {slot}, -1')
                sections['Linez']=stock_lines if variant=='absent' else (*stock_lines,f'{head}, {marker}, 0, {-2 if variant=="textured" else 125}, 244, 244, 100, 100, 0, 1')
                path=OUT/f'{species}-{width}x{height}-{variant}{source.suffix}'
                paths[variant]=path.name;hashes[variant]=write_copy(raw,leaf,sections,path)
            resolver=ResourceResolver((ROOT/'games/petz4',OUT))
            for pose in ('standing','sitting','lying'):
                assets={n:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for n,p in paths.items()}
                geometry={n:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for n,a in assets.items()}
                assert geometry['textured']==geometry['explicit']==geometry['absent']
                for variant,a in assets.items():
                    assert a.appearance.textures[:slot]==layer.appearance.textures
                    assert a.appearance.lines[:len(layer.appearance.lines)]==layer.appearance.lines
                    texture=a.textures[slot];assert (texture.width,texture.height)==(width,height)
                    record={'pose':pose,'variant':variant,'texture_size':[width,height],'texture_sha256':SHA(texture.pixels),'texture_config':vars(a.appearance.textures[slot])}
                    if variant!='absent':
                        prepared=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50)
                        block=build_line_block(a.appearance.lines[-1],tuple(b.endpoint for b in prepared.balls));assert block is not None
                        assert (block.paint is not None)==(variant=='textured')
                        # Translate away from the viewport to isolate size from clipping.
                        block=replace(block,x1=block.x1+256,y1=block.y1+256,x2=block.x2+256,y2=block.y2+256)
                        fb=Framebuffer(512,512,background=254);LineRenderer(seed=1).draw(fb,block)
                        changed=sum(v!=254 for v in fb.pixels)
                        record.update(block={k:v for k,v in vars(block).items() if k!='paint'},paint_sha256=None if block.paint is None else SHA(block.paint.texture.pixels),isolated_pixels=changed,isolated_sha256=SHA(fb.pixels))
                        if variant=='explicit':assert changed>0
                    checks.append(record)
            assert SHA(source.read_bytes())==SHA(raw)
            cases.append({'species':species,'source_path':str(source.relative_to(ROOT)),'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'texture_slot':slot,'dimensions':[width,height],'paths':paths,'input_hashes':hashes,'checks':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for variant in ('textured','explicit'):
                for yaw in (0,90):
                    args={'before_path':c['paths']['absent'],'after_path':c['paths'][variant],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{c['dimensions'][0]}x{c['dimensions'][1]}-{variant}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    assert meta['game_version']=='petz4'
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    if variant=='explicit':assert not equal
                    renders.append({'species':c['species'],'dimensions':c['dimensions'],'variant':variant,'controls':args,'png_sha256':SHA(png),'game_version':meta['game_version'],'renderer_version':meta['renderer_version'],'cells_equal':equal,'cell_hashes':[x['pixel_sha256'] for x in meta['cells']]})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,equal,flush=True)
    report={'experiment':'LINE-021','backend':'local stdio MCP plus asset-backed block/raster checks','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':sources,'engine_hashes':engines,'cases':cases,'comparisons':renders}
    for path in (OUT/'report.json',ROOT/'experiments/line-021.json'):path.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
