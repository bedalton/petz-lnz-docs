"""Verify LINE-013 through016 private texture evidence without rendering."""
import importlib.metadata,json
from io import BytesIO
from pathlib import Path
from PIL import Image
import petz_renderer
from research_common import ROOT,SHA,adult

def main():
    package=Path(petz_renderer.__file__).parent;copies=set();pngs=cells=loads=raws=samples=0
    for experiment in ('line-013','line-014','line-015','line-016'):
        aggregate=json.loads((ROOT/'experiments'/f'{experiment}.json').read_text());root=ROOT/'scratch/research'/experiment
        assert aggregate==json.loads((root/'report.json').read_text())
        reports=aggregate.get('reports',[aggregate])
        if experiment=='line-016':
            assert SHA((ROOT/'experiments/line-013.json').read_bytes())==aggregate['baseline_manifest_sha256']
        for report in reports:
            version=report.get('game_version','petz4');folder=root/version if experiment=='line-016' else root
            assert report==json.loads((folder/'report.json').read_text())
            for name,h in report['source_hashes'].items():
                assert SHA((package/name).read_bytes())==h
                assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==h
            for name,v in report['dependencies'].items():assert importlib.metadata.version(name)==v
            for name,h in report.get('engine_hashes',{}).items():assert SHA((ROOT/name).read_bytes())==h
            for c in report.get('cases',[]):
                source,*_=adult(c['species'],version);assert SHA(source.read_bytes())==c['source_sha256']
                loads+=len(c['geometry'])
                for name,path in c['paths'].items():
                    path=folder/path;assert SHA(path.read_bytes())==c['input_hashes'][name];copies.add(str(path))
            for r in report.get('comparisons',[]):
                before,after=r['pair'];stem=f"{r['species']}-{before}-{after}-{r['controls']['yaw_degrees']}"
                data=(folder/f'{stem}.png').read_bytes();assert SHA(data)==r['png_sha256'];pngs+=1
                meta=json.loads((folder/f'{stem}-render.json').read_text());assert meta['png_sha256']==r['png_sha256']
                assert meta['game_version']==version and all(c['game_version']==version for c in meta['cells'])
                assert [c['pixel_sha256'] for c in meta['cells']]==r['cell_hashes']
                assert r['cells_equal']==(r['cell_hashes'][0]==r['cell_hashes'][1])
                with Image.open(BytesIO(data)) as im:
                    rgba=im.convert('RGBA');w,h=meta['cell_width'],meta['cell_height']
                    for c,expected in zip(meta['cells'],r['cell_hashes'],strict=True):
                        x,y=c['origin'];assert SHA(rgba.crop((x,y,x+w,y+h)).tobytes())==expected;cells+=1
            if experiment=='line-016':
                baseline=json.loads((ROOT/'experiments/line-013.json').read_text())
                for r,b,match in zip(report['comparisons'],baseline['comparisons'],report['cross_version_matches'],strict=True):
                    assert match['png_matches_petz4']==(r['png_sha256']==b['png_sha256'])
                    assert match['cells_match_petz4']==(r['cell_hashes']==b['cell_hashes'])
        if experiment=='line-014':
            private=json.loads((root/'pixels.json').read_text());assert len(private)==72
            for record,row in zip(aggregate['records'],private,strict=True):
                assert record==row['record'];pixels=bytes(row['indexed_pixels']);raws+=1
                assert len(pixels)==3600 and SHA(pixels)==record['indexed_sha256']
                assert sum(x!=0 for x in pixels)==record['colored_pixels']
                for sample in record['centerline_samples']:
                    x,y=sample['destination'];assert pixels[y*60+x]==sample['value'];samples+=1
    assert (len(copies),pngs,cells,loads,raws,samples)==(42,64,128,126,72,120)
    summary={'unique_private_copies':len(copies),'mcp_png_pairs':pngs,'rgba_cells':cells,'numerical_breed_loads':loads,'synthetic_indexed_buffers':raws,'exact_texture_samples':samples,'sources_dependencies_resource_dlls_originals_verified':True}
    (ROOT/'scratch/research/line-texture-session-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
