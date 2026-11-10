"""Audit TEXTURE-003 saved provenance, leaves, modes, isolated rasters and MCP cells."""
import importlib.metadata
import json
from dataclasses import replace
from io import BytesIO
from pathlib import Path
from PIL import Image
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
from research_common import ROOT,SHA,adult
from texture_mode_probe import synthetic


def main():
    folder=ROOT/'scratch/research/texture-003';path=ROOT/'experiments/texture-003.json'
    report=json.loads(path.read_text());assert report==json.loads((folder/'report.json').read_text())
    assert report['synthetic']==synthetic()
    for name,digest in report['source_hashes'].items():
        for root in (Path(petz_renderer.__file__).parent,ROOT/'petz-renderer-mcp/src/petz_renderer'):
            assert SHA((root/name).read_bytes())==digest
    for name,version in report['dependencies'].items():assert importlib.metadata.version(name)==version
    for name,digest in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==digest
    counts={'copies':0,'numerical_loads':0,'isolated_rasters':0,'mcp_pairs':0,'rgba_cells':0,'parser_cases':len(report['synthetic']['parser']),'all_byte_remaps':len(report['synthetic']['all_byte_remaps'])}
    expected={-1:(False,-1),0:(False,-1),1:(True,-1),2:(True,0),10:(True,0),125:(True,11),149:(True,13),150:(True,0)}
    for case in report['cases']:
        source,raw,leaf,_,master,_=adult(case['species']);assert SHA(raw)==case['source_sha256'] and str(source.relative_to(ROOT))==case['source_path']
        original=ResourceFile(raw);layer=load_layer(original,master,name=leaf.name,seed=0)
        for name,filename in case['paths'].items():
            data=(folder/filename).read_bytes();assert SHA(data)==case['input_hashes'][name]
            assert len(data)==len(raw) and data[:leaf.offset]==raw[:leaf.offset] and data[leaf.offset+leaf.size:]==raw[leaf.offset+leaf.size:]
            edited=ResourceFile(data);assert edited.resources==original.resources
            for resource in original.resources:
                if resource!=leaf:assert original.read(resource.type,resource.name,resource.language)==edited.read(resource.type,resource.name,resource.language)
            counts['copies']+=1
        shapes={};raster={}
        for rec in case['checks']:
            mode,variant,pose=rec['mode'],rec['variant'],rec['pose'];name=f'm{mode}-{variant}'
            a=load_breed_assets(ResourceResolver((ROOT/'games/petz4',folder)),case['paths'][name],pose=pose,seed=0,age=100,fatness=50)
            shape=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50)
            if pose in shapes:assert shape==shapes[pose]
            else:shapes[pose]=shape
            slot=case['texture_slot'];config=a.appearance.textures[slot];texture=a.textures[slot]
            assert a.appearance.textures[:slot]==layer.appearance.textures
            assert a.appearance.lines[:len(layer.appearance.lines)]==layer.appearance.lines
            assert vars(config)==rec['texture_config'] and (config.has_levels,config.own_level)==expected[mode]
            assert SHA(texture.pixels)==rec['texture_sha256'] and (texture.width,texture.height)==(256,256)
            if variant!='absent':
                p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50)
                block=build_line_block(a.appearance.lines[-1],tuple(b.endpoint for b in p.balls))
                block=replace(block,x1=block.x1+256,y1=block.y1+256,x2=block.x2+256,y2=block.y2+256)
                assert {k:v for k,v in vars(block).items() if k!='paint'}==rec['block']
                paint=None if block.paint is None else {'sha256':SHA(block.paint.texture.pixels),'shade_offset':block.paint.shade_offset,'has_sign':block.paint.has_sign}
                assert paint==rec['paint'] and (paint is not None)==(variant=='textured')
                fb=Framebuffer(512,512,background=254);LineRenderer(seed=1).draw(fb,block)
                assert SHA(fb.pixels)==rec['isolated_sha256'] and any(v!=254 for v in fb.pixels)
                raster[(pose,mode,variant)]=rec['isolated_sha256'];counts['isolated_rasters']+=1
            counts['numerical_loads']+=1
        for pose in shapes:
            for variant in ('textured','explicit'):
                assert raster[(pose,-1,variant)]==raster[(pose,0,variant)]
                assert len({raster[(pose,m,variant)] for m in (2,10,150)})==1
            for mode in expected:assert raster[(pose,mode,'textured')]!=raster[(pose,mode,'explicit')]
            # Report distinct connector-only images separately from composed sheets.
            print(case['species'],pose,'textured classes',len({raster[(pose,m,'textured')] for m in expected}))
    for rec in report['comparisons']:
        before,after=rec['pair'];stem=f"{rec['species']}-{before}-{after}-{rec['controls']['yaw_degrees']}"
        png=(folder/f'{stem}.png').read_bytes();assert SHA(png)==rec['png_sha256']
        meta=json.loads((folder/f'{stem}-render.json').read_text());assert meta['game_version']==rec['game_version']=='petz4'
        im=Image.open(BytesIO(png)).convert('RGBA')
        for cell,digest in zip(meta['cells'],rec['cell_hashes'],strict=True):
            x,y=cell['origin'];assert SHA(im.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes())==digest==cell['pixel_sha256'];counts['rgba_cells']+=1
        equal=rec['cell_hashes'][0]==rec['cell_hashes'][1]
        assert equal==rec['cells_equal']==(rec['pair'] in [['m-1-textured','m0-textured'],['m2-textured','m10-textured'],['m2-textured','m150-textured']])
        counts['mcp_pairs']+=1
    assert counts=={'copies':48,'numerical_loads':144,'isolated_rasters':96,'mcp_pairs':84,'rgba_cells':168,'parser_cases':18,'all_byte_remaps':40}
    result={'experiment':'TEXTURE-003','report_sha256':SHA(path.read_bytes()),'verified':counts}
    (ROOT/'scratch/research/texture-003-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
