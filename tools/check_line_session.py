"""Verify saved connector styling evidence without rerendering game assets."""
import importlib.metadata,json
from io import BytesIO
from pathlib import Path
from PIL import Image
import petz_renderer
from research_common import ROOT,SHA,adult

def main():
    package=Path(petz_renderer.__file__).parent;copies=sheets=cells=states=loads=direct=0
    for exp in ('line-005','line-006','line-007','line-008','line-009'):
        report=json.loads((ROOT/'experiments'/f'{exp}.json').read_text());folder=ROOT/'scratch/research'/exp
        assert report==json.loads((folder/'report.json').read_text())
        loads+=sum(len(c['geometry']) for c in report.get('cases',[]))
        direct+=len(report.get('synthetic',[]))+len(report.get('records',[]))
        for name,h in report['source_hashes'].items():
            assert SHA((package/name).read_bytes())==h
            assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==h
        for name,v in report['dependencies'].items():assert importlib.metadata.version(name)==v
        for name,h in report.get('engine_hashes',{}).items():assert SHA((ROOT/name).read_bytes())==h
        for case in report.get('cases',[]):
            source,*_=adult(case['species']);assert SHA(source.read_bytes())==case['source_sha256']
            for variant,name in case['paths'].items():
                assert SHA((folder/name).read_bytes())==case['input_hashes'][variant];copies+=1
        for comparison in report.get('comparisons',[]):
            before,after=comparison['pair'];args=comparison['controls'];stem=f"{comparison['species']}-{before}-{after}-{args['yaw_degrees']}"
            png=(folder/f'{stem}.png').read_bytes();assert SHA(png)==comparison['png_sha256'];sheets+=1
            meta=json.loads((folder/f'{stem}-render.json').read_text());assert meta['png_sha256']==comparison['png_sha256']
            with Image.open(BytesIO(png)) as im:
                rgba=im.convert('RGBA');w,h=meta['cell_width'],meta['cell_height']
                for i,(cell,expected) in enumerate(zip(meta['cells'],comparison['cell_hashes'],strict=True)):
                    x,y=cell['origin'];assert SHA(rgba.crop((x,y,x+w,y+h)).tobytes())==expected==cell['pixel_sha256'];cells+=1
            assert comparison['cells_equal']==(comparison['cell_hashes'][0]==comparison['cell_hashes'][1])
        if exp=='line-008':
            full=json.loads((folder/'states.json').read_text())
            for record,snapshot in zip(report['records'],full,strict=True):
                assert record==snapshot['record']
                for when in ('before','after'):
                    assert SHA(json.dumps(snapshot[when],sort_keys=True).encode())==record[f'state_{when}_sha256'];states+=1
    assert (loads,direct)==(156,256)
    summary={'numerical_breed_loads':loads,'direct_block_raster_cases':direct,'private_copies':copies,'mcp_sheets':sheets,'rgba_cells':cells,'full_rng_table_states':states,'sources_dependencies_engines_originals_verified':True}
    out=ROOT/'scratch/research/line-session-verification.json';out.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
