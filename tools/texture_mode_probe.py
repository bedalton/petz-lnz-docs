"""TEXTURE-003: Texture List mode decoding and composed connector remapping."""
import asyncio
import importlib.metadata
import json
import sys
from dataclasses import replace
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.appearance.core import read_core
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.connectors import build_line_block
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineRenderer
from petz_renderer.rendering.texture import TiledTexture, remap_texture
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/texture-003'
MODES=(-1,0,1,2,10,125,149,150)
# Independently stated boundary expectations, including absent/invalid fields.
PARSER_CASES=[('art.bmp',True,-1,256,256),('art.bmp, nope',True,-1,256,256),
 ('art.bmp, -2',False,-1,256,256),('art.bmp, -1',False,-1,256,256),
 ('art.bmp, 0',False,-1,256,256),('art.bmp, 1',True,-1,256,256),
 ('art.bmp, 2',True,0,256,256),('art.bmp, 9',True,0,256,256),
 ('art.bmp, 10',True,0,256,256),('art.bmp, 19',True,0,256,256),
 ('art.bmp, 20',True,1,256,256),('art.bmp, 125',True,11,256,256),
 ('art.bmp, 149',True,13,256,256),('art.bmp, 150',True,0,256,256),
 ('art.bmp, 999',True,0,256,256),('art.bmp, 1, 64, 128',True,-1,64,128),
 ('art.bmp, 1, bad, 128',True,-1,256,128),('art.bmp, 1, 64',True,-1,64,256)]

def synthetic():
    parser=[]
    for row,levels,own,w,h in PARSER_CASES:
        texture=read_core({'Texture List':(row,)}).textures[0]
        assert (texture.has_levels,texture.own_level,texture.tile_width,texture.tile_height)==(levels,own,w,h)
        parser.append({'row':row,'decoded':vars(texture)})
    art=TiledTexture(256,1,bytes(range(256)),0,0);records=[]
    for color in (10,19,20,125,149):
        paints={}
        for mode in MODES:
            config=read_core({'Texture List':(f'art.bmp, {mode}',)}).textures[0]
            paint=remap_texture(art,color,has_levels=config.has_levels,own_level=config.own_level)
            assert paint.texture.pixels[:10]==art.pixels[:10] and paint.texture.pixels[150:]==art.pixels[150:]
            assert paint.has_sign==(config.own_level>=0)
            paints[mode]=paint
            records.append({'color':color,'mode':mode,'has_levels':config.has_levels,'own_level':config.own_level,'shade_offset':paint.shade_offset,'has_sign':paint.has_sign,'remapped_sha256':SHA(paint.texture.pixels),'changed_art_bytes':sum(x!=y for x,y in zip(art.pixels,paint.texture.pixels))})
        assert paints[-1]==paints[0] and paints[2]==paints[10]==paints[150]
        assert paints[0]!=paints[1] and paints[1]!=paints[2]
    return {'parser':parser,'all_byte_remaps':records}

async def main():
    OUT.mkdir(parents=True,exist_ok=False);direct=synthetic();cases=[];renders=[]
    package=Path(petz_renderer.__file__).parent
    sources={p:SHA((package/p).read_bytes()) for p in ('appearance/core.py','rendering/connectors.py','rendering/texture.py','rendering/lines.py','rendering/assets.py','rendering/preparation.py')}
    for p,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    engines={str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in sorted((ROOT/'games/petz4').glob('Resource/* 4 Rez.dll'))}
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species);layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls);slot=len(layer.appearance.textures)
        art=layer.appearance.textures[layer.appearance.balls[head].texture].path
        assert all(t.own_level==-1 for t in layer.appearance.textures)
        stock_textures=tuple(f'{t.path}, {1 if t.has_levels else 0}, {t.tile_width}, {t.tile_height}' for t in layer.appearance.textures)
        stock_lines=tuple(', '.join(str(int(v)) for v in vars(line).values()) for line in layer.appearance.lines)
        paths={};hashes={};checks=[]
        for mode in MODES:
            for variant in ('textured','explicit','absent'):
                name=f'm{mode}-{variant}';s=dict(base)
                s['Texture List']=(*stock_textures,f'{art}, {mode}, 256, 256')
                s['Add Ball']=(*base['Add Ball'],f'{head}, -35, -160, 0, 125, 244, -1, 0, -1, -1, 20, 0, 0, {slot}, -1')
                s['Linez']=stock_lines if variant=='absent' else (*stock_lines,f'{head}, {marker}, 0, {-2 if variant=="textured" else 125}, 244, 244, 100, 100, 0, 1')
                path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            shapes={};blocks={}
            for mode in MODES:
                for variant in ('textured','explicit','absent'):
                    name=f'm{mode}-{variant}';a=load_breed_assets(resolver,paths[name],pose=pose,seed=0,age=100,fatness=50)
                    shape=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50)
                    if shapes:assert shape==next(iter(shapes.values()))
                    shapes[name]=shape
                    assert a.appearance.textures[:slot]==layer.appearance.textures
                    assert a.appearance.lines[:len(layer.appearance.lines)]==layer.appearance.lines
                    config=a.appearance.textures[slot];texture=a.textures[slot]
                    rec={'pose':pose,'mode':mode,'variant':variant,'texture_config':vars(config),'texture_sha256':SHA(texture.pixels)}
                    if variant!='absent':
                        p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50)
                        block=build_line_block(a.appearance.lines[-1],tuple(b.endpoint for b in p.balls));assert block is not None
                        assert (block.paint is not None)==(variant=='textured')
                        block=replace(block,x1=block.x1+256,y1=block.y1+256,x2=block.x2+256,y2=block.y2+256)
                        fb=Framebuffer(512,512,background=254);LineRenderer(seed=1).draw(fb,block)
                        assert any(v!=254 for v in fb.pixels)
                        rec.update(block={k:v for k,v in vars(block).items() if k!='paint'},paint=None if block.paint is None else {'sha256':SHA(block.paint.texture.pixels),'shade_offset':block.paint.shade_offset,'has_sign':block.paint.has_sign},isolated_sha256=SHA(fb.pixels))
                        blocks[(mode,variant)]=rec
                    checks.append(rec)
            for variant in ('textured','explicit'):
                assert blocks[(-1,variant)]['isolated_sha256']==blocks[(0,variant)]['isolated_sha256']
                assert len({blocks[(m,variant)]['isolated_sha256'] for m in (2,10,150)})==1
            for mode in MODES:assert blocks[(mode,'textured')]['isolated_sha256']!=blocks[(mode,'explicit')]['isolated_sha256']
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_path':str(source.relative_to(ROOT)),'source_sha256':SHA(raw),'texture_slot':slot,'head_id':head,'marker_id':marker,'paths':paths,'input_hashes':hashes,'checks':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            pairs=[(f'm{m}-absent',f'm{m}-textured',False) for m in MODES]
            pairs +=[(f'm{m}-explicit',f'm{m}-textured',False) for m in MODES]
            pairs +=[('m-1-textured','m0-textured',True),('m2-textured','m10-textured',True),('m2-textured','m150-textured',True),('m0-textured','m1-textured',False),('m1-textured','m2-textured',False)]
            for before,after,expected in pairs:
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert meta['game_version']=='petz4' and equal==expected,(stem,equal,expected)
                    renders.append({'species':c['species'],'pair':[before,after],'controls':args,'png_sha256':SHA(png),'game_version':meta['game_version'],'renderer_version':meta['renderer_version'],'cells_equal':equal,'cell_hashes':[x['pixel_sha256'] for x in meta['cells']]})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,equal,flush=True)
    report={'experiment':'TEXTURE-003','backend':'local stdio MCP plus asset-backed block/raster and asset-free parser/remap checks','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':sources,'engine_hashes':engines,'synthetic':direct,'cases':cases,'comparisons':renders}
    for path in (OUT/'report.json',ROOT/'experiments/texture-003.json'):path.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
