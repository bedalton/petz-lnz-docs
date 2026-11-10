"""Verify LINE-021 copies, MCP cells and numerical/raster evidence."""
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


def main():
    folder=ROOT/'scratch/research/line-021'
    report=json.loads((ROOT/'experiments/line-021.json').read_text())
    assert report==json.loads((folder/'report.json').read_text())
    for name,digest in report['source_hashes'].items():
        for root in (Path(petz_renderer.__file__).parent,ROOT/'petz-renderer-mcp/src/petz_renderer'):
            assert SHA((root/name).read_bytes())==digest
    for name,version in report['dependencies'].items():assert importlib.metadata.version(name)==version
    for name,digest in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==digest
    counts={'copies':0,'numerical_loads':0,'isolated_rasters':0,'mcp_pairs':0,'rgba_cells':0}
    for case in report['cases']:
        source,raw,leaf,_,master,_=adult(case['species'])
        assert SHA(raw)==case['source_sha256'] and str(source.relative_to(ROOT))==case['source_path']
        original=ResourceFile(raw);layer=load_layer(original,master,name=leaf.name,seed=0)
        for variant,filename in case['paths'].items():
            data=(folder/filename).read_bytes();assert SHA(data)==case['input_hashes'][variant]
            assert len(data)==len(raw) and data[:leaf.offset]==raw[:leaf.offset] and data[leaf.offset+leaf.size:]==raw[leaf.offset+leaf.size:]
            edited=ResourceFile(data);assert edited.resources==original.resources
            for resource in original.resources:
                if resource!=leaf:assert original.read(resource.type,resource.name,resource.language)==edited.read(resource.type,resource.name,resource.language)
            counts['copies']+=1
        geometry={}
        for record in case['checks']:
            variant=record['variant'];pose=record['pose']
            a=load_breed_assets(ResourceResolver((ROOT/'games/petz4',folder)),case['paths'][variant],pose=pose,seed=0,age=100,fatness=50)
            shape=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50)
            if pose in geometry:assert shape==geometry[pose]
            else:geometry[pose]=shape
            slot=case['texture_slot'];texture=a.textures[slot]
            assert a.appearance.textures[:slot]==layer.appearance.textures
            assert a.appearance.lines[:len(layer.appearance.lines)]==layer.appearance.lines
            assert vars(a.appearance.textures[slot])==record['texture_config']
            assert [texture.width,texture.height]==record['texture_size']==case['dimensions']
            assert SHA(texture.pixels)==record['texture_sha256']
            if variant!='absent':
                prepared=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50)
                block=build_line_block(a.appearance.lines[-1],tuple(b.endpoint for b in prepared.balls))
                block=replace(block,x1=block.x1+256,y1=block.y1+256,x2=block.x2+256,y2=block.y2+256)
                assert {k:v for k,v in vars(block).items() if k!='paint'}==record['block']
                assert (block.paint is not None)==(variant=='textured')
                assert (None if block.paint is None else SHA(block.paint.texture.pixels))==record['paint_sha256']
                fb=Framebuffer(512,512,background=254);LineRenderer(seed=1).draw(fb,block)
                assert SHA(fb.pixels)==record['isolated_sha256']
                assert sum(v!=254 for v in fb.pixels)==record['isolated_pixels']
                assert (record['isolated_pixels']==0)==(variant=='textured' and case['dimensions'] in ([32,256],[256,32],[64,64]))
                counts['isolated_rasters']+=1
            counts['numerical_loads']+=1
    for record in report['comparisons']:
        width,height=record['dimensions'];args=record['controls']
        stem=f"{record['species']}-{width}x{height}-{record['variant']}-{args['yaw_degrees']}"
        png=(folder/f'{stem}.png').read_bytes();assert SHA(png)==record['png_sha256']
        meta=json.loads((folder/f'{stem}-render.json').read_text())
        assert meta['game_version']==record['game_version']=='petz4'
        im=Image.open(BytesIO(png)).convert('RGBA')
        for cell,digest in zip(meta['cells'],record['cell_hashes'],strict=True):
            x,y=cell['origin'];pixels=im.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes()
            assert SHA(pixels)==digest==cell['pixel_sha256']
            counts['rgba_cells']+=1
        equal=record['cell_hashes'][0]==record['cell_hashes'][1]
        assert equal==record['cells_equal']==(record['variant']=='textured' and [width,height] in ([32,256],[256,32],[64,64]))
        counts['mcp_pairs']+=1
    assert counts=={'copies':30,'numerical_loads':90,'isolated_rasters':60,'mcp_pairs':40,'rgba_cells':80}
    result={'experiment':'LINE-021','report_sha256':SHA((ROOT/'experiments/line-021.json').read_bytes()),'verified':counts}
    (ROOT/'scratch/research/line-021-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
