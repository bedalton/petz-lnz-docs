"""Audit LINE-017..020 persisted pixels, samples, MCP crops and provenance."""
import importlib.metadata
import json
from io import BytesIO
from pathlib import Path
from PIL import Image
import petz_renderer
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineBlock,LineRenderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.appearance.layers import load_layer
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.connectors import build_line_block
from petz_renderer.rendering.texture import remap_texture
from research_common import ROOT,SHA,adult


def main():
    package=Path(petz_renderer.__file__).parent
    counts={'synthetic_buffers':0,'exact_body_samples':0,'explicit_edge_assertions':0,
            'mcp_png_pairs':0,'rgba_cells':0,'private_copies':0,'numerical_breed_loads':0}
    provenance={}
    for name in ('line-017','line-018','line-019','line-020'):
        folder=ROOT/'scratch/research'/name
        report_path=ROOT/'experiments'/f'{name}.json'
        report=json.loads(report_path.read_text())
        assert report==json.loads((folder/'report.json').read_text())
        provenance[name]=SHA(report_path.read_bytes())
        for source,digest in report['source_hashes'].items():
            assert SHA((package/source).read_bytes())==digest
            assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/source).read_bytes())==digest
        for dependency,version in report['dependencies'].items():
            assert importlib.metadata.version(dependency)==version
        for source,digest in report.get('engine_hashes',{}).items():
            assert SHA((ROOT/source).read_bytes())==digest
        if name!='line-019':
            payload=(folder/'pixels.json').read_bytes()
            assert SHA(payload)==report['private_pixels_sha256']
            rows=json.loads(payload)
            canvas=report['controls']['canvas'];cw,ch=canvas
            assert len(rows)==report['summary']['fixtures']
            observed_samples=0;reverse={}
            for record,row in zip(report['records'],rows,strict=True):
                assert record==row['record']
                pixels=bytes(row['pixels']);assert len(pixels)==cw*ch
                assert SHA(pixels)==record['indexed_sha256']
                counts['synthetic_buffers']+=1
                if name=='line-020':
                    points=(10,12,265,12) if record['axis']=='horizontal' else (12,10,12,265)
                    plain=Framebuffer(cw,ch,background=254)
                    LineRenderer(seed=1).draw(plain,LineBlock(*points,start_thick=3,end_thick=3,color=125,
                        left_color=180,right_color=200,fuzz=0,edge_mode=record['edge_mode']))
                    assert SHA(plain.pixels)==record['plain_indexed_sha256']
                    body_indices={y*cw+x for x,y,_,_ in row['samples']}
                    assert body_indices=={i for i,v in enumerate(plain.pixels) if v==125}
                    edge_count=0
                    for i,value in enumerate(plain.pixels):
                        if i not in body_indices:
                            assert pixels[i]==value
                            edge_count+=value in (180,200)
                    assert edge_count==record['explicit_edge_assertions']
                    for x,y,sample,value in row['samples']:
                        expected=sample if record['has_sign'] and sample>=10 else (sample+record['shade_offset'])%256
                        assert value==expected and pixels[y*cw+x]==value
                    counts['explicit_edge_assertions']+=record['explicit_edge_assertions']
                    assert sum(s[-1]==0 for s in row['samples'])==record['zero_output_samples']
                else:
                    assert sum(p!=0 for p in pixels)==record['colored_pixels']
                    if record['rejected']:
                        assert not any(pixels) and record['rng_after']==1 and not any(record['table_lengths'])
                    for x,y,tx,ty,value in row['samples']:
                        assert value==20+(tx+17*ty)%220 and pixels[y*cw+x]==value
                    if name=='line-018':
                        plain=bytes(row['plain_pixels']);assert SHA(plain)==record['plain_indexed_sha256']
                        if not record['rejected']:
                            assert [i for i,v in enumerate(pixels) if v]==[i for i,v in enumerate(plain) if v]
                        if record['fuzz']==0:
                            crop=bytes(row['unclamped_crop_pixels_fuzz0'])
                            assert sum(a!=b for a,b in zip(plain,crop,strict=True))==record['plain_clamp_vs_crop_pixels_fuzz0']
                    else:
                        key=json.dumps({k:record[k] for k in ('delta','thickness','fuzz','spare')},sort_keys=True)
                        if record['reversed']:assert reverse[key]==pixels
                        else:reverse[key]=pixels
                assert len(row['samples'])==record['sample_assertions']
                observed_samples+=len(row['samples'])
            assert observed_samples==report['summary']['sample_assertions']
            counts['exact_body_samples']+=observed_samples
        else:
            for case in report['cases']:
                source,raw,leaf,base,master,_=adult(case['species'],filename=case['breed']['filename'],selector=case['breed']['selector'])
                assert SHA(source.read_bytes())==case['source_sha256']
                assert str(source.relative_to(ROOT))==case['source_path']
                for variant,filename in case['paths'].items():
                    edited=(folder/filename).read_bytes()
                    assert SHA(edited)==case['input_hashes'][variant]
                    assert len(edited)==len(raw)
                    assert edited[:leaf.offset]==raw[:leaf.offset]
                    assert edited[leaf.offset+leaf.size:]==raw[leaf.offset+leaf.size:]
                    counts['private_copies']+=1
                resolver=ResourceResolver((ROOT/'games/petz4',folder),game_version='petz4')
                stock=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
                reference_shapes={}
                for check in case['geometry']:
                    variant,pose=check['variant'],check['pose']
                    assets=load_breed_assets(resolver,case['paths'][variant],pose=pose,seed=0,age=100,fatness=50)
                    shape=posed_geometry(assets.appearance,assets.sizes,assets.frame,fatness=50)
                    if pose in reference_shapes:assert shape==reference_shapes[pose]
                    else:reference_shapes[pose]=shape
                    frame=prepare_frame(assets.appearance,assets.sizes,assets.frame,textures=assets.textures,fatness=50)
                    assert assets.appearance.lines[:-1]==stock.appearance.lines
                    line=assets.appearance.lines[-1]
                    block=build_line_block(line,tuple(b.endpoint for b in frame.balls))
                    assert block is not None
                    slot=check['texture_index'];texture=assets.textures[slot]
                    assert texture is not None
                    assert check['line_color']==line.color and check['block_color']==block.color
                    assert check['paint_present']==(block.paint is not None)
                    assert check['texture_pixels_sha256']==SHA(texture.pixels)
                    assert check['texture_size']==[texture.width,texture.height]
                    config=assets.appearance.textures[slot]
                    assert check['texture_config']==vars(config)
                    if block.paint is not None:
                        assert check['paint_pixels_sha256']==SHA(block.paint.texture.pixels)
                        assert block.paint==remap_texture(texture,block.color,has_levels=config.has_levels,own_level=config.own_level)
                    else:assert check['paint_pixels_sha256'] is None
                    counts['numerical_breed_loads']+=1
            for row in report['comparisons']:
                stem=f"{row['species']}-{row['pair'][0]}-{row['pair'][1]}-{row['controls']['yaw_degrees']}"
                data=(folder/f'{stem}.png').read_bytes();assert SHA(data)==row['png_sha256']
                meta=json.loads((folder/f'{stem}-render.json').read_text())
                assert meta['png_sha256']==row['png_sha256']
                assert meta['game_version']==row['game_version']=='petz4'
                assert meta['renderer_version']==row['renderer_version']
                assert [c['pixel_sha256'] for c in meta['cells']]==row['cell_hashes']
                assert row['cells_equal']==(row['cell_hashes'][0]==row['cell_hashes'][1])
                assert row['cells_equal']==(row['pair']!=['head_texture','explicit_plain'])
                with Image.open(BytesIO(data)) as im:
                    rgba=im.convert('RGBA');w,h=meta['cell_width'],meta['cell_height']
                    for cell,digest in zip(meta['cells'],row['cell_hashes'],strict=True):
                        assert cell['game_version']=='petz4'
                        x,y=cell['origin'];assert SHA(rgba.crop((x,y,x+w,y+h)).tobytes())==digest
                        counts['rgba_cells']+=1
                counts['mcp_png_pairs']+=1
    assert counts=={'synthetic_buffers':600,'exact_body_samples':43356,'explicit_edge_assertions':15420,
                    'mcp_png_pairs':16,'rgba_cells':32,'private_copies':10,'numerical_breed_loads':30}
    audit=json.loads((ROOT/'scratch/research/line-texture-session-source-audit.json').read_text())
    assert len(audit['source_hashes'])==62
    assert SHA(json.dumps(audit['source_hashes'],sort_keys=True).encode())==audit['source_tree_sha256']
    for source,digest in audit['source_hashes'].items():
        assert SHA((package/source).read_bytes())==digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/source).read_bytes())==digest
    summary={'counts':counts,'public_manifest_hashes':provenance,'installed_checkout_source_files_verified':62,
             'source_tree_sha256':audit['source_tree_sha256'],'sources_dependencies_engines_originals_verified':True}
    (ROOT/'scratch/research/line-sampling-session-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
