"""Independently verify UPDATE-001 saved MCP pixels, controls and provenance."""
import importlib.metadata,json
from pathlib import Path
from io import BytesIO
from PIL import Image
import petz_renderer
from research_common import ROOT,SHA
from revalidate_renderer_update import partition

def main():
    path=ROOT/'experiments/update-001.json';folder=ROOT/'scratch/research/update-001';r=json.loads(path.read_text());assert r==json.loads((folder/'report.json').read_text())
    installed=Path(petz_renderer.__file__).parent;checkout=ROOT/'petz-renderer-mcp/src/petz_renderer'
    for name,h in r['source_hashes'].items():
        assert SHA((installed/name).read_bytes())==h==SHA((checkout/name).read_bytes())
    for name,version in r['dependencies'].items():assert importlib.metadata.version(name)==version
    assert SHA((ROOT/'RENDERER_CHANGES.md').read_bytes())==r['change_notice_sha256']
    originals=json.loads((ROOT/'experiments/restore-002.json').read_text());original_links={}
    for version,records in originals['shared_engine_hashes'].items():
        paths={str(p.relative_to(ROOT/'games'/version)).lower():p for p in (ROOT/'games'/version).rglob('*') if p.is_file()}
        for name,h in records.items():assert SHA(paths[name].read_bytes())==h;original_links[f'{version}/{name}']=h
    for old in originals['results']:
        assert SHA((ROOT/'games'/old['version']/old['path']).read_bytes())==old['input_sha256'];original_links[f"{old['version']}/{old['path']}"]=old['input_sha256']
    for name,h in r['historical_reports'].items():assert SHA((ROOT/f'experiments/{name}.json').read_bytes())==h
    cells=0;input_files={};relationships=0
    for row in r['replays']:
        old=json.loads((ROOT/f"experiments/{row['experiment']}.json").read_text());old=(old.get('comparisons',[])+old.get('pages',[]))[row['index']]
        assert row['controls']==old['controls']
        for name,h in row['input_hashes'].items():
            path=ROOT/row['asset_root']/name;assert SHA(path.read_bytes())==h;input_files[str(path.relative_to(ROOT))]=h
        raw=(folder/(row['stem']+'.png')).read_bytes();assert SHA(raw)==row['png_sha256']
        meta=json.loads((folder/(row['stem']+'-render.json')).read_text());assert meta['game_version']==row['game_version']
        im=Image.open(BytesIO(raw)).convert('RGBA')
        for cell,h in zip(meta['cells'],row['cell_hashes'],strict=True):
            x,y=cell['origin'];assert SHA(im.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes())==h==cell['pixel_sha256'];cells+=1
        assert row['same_png']==(SHA(raw)==old['png_sha256'])
        if row['old_cell_hashes']:
            assert row['same_cells']==(row['old_cell_hashes']==row['cell_hashes'])
            expected=partition(row['old_cell_hashes'])==partition(row['cell_hashes'])
        elif 'cells_equal' in old:expected=(row['cell_hashes'][0]==row['cell_hashes'][1])==old['cells_equal']
        else:expected=None
        assert expected==row['same_equality_relationships'];relationships+=expected is True
    for row in r['smoke']:
        raw=(folder/(row['stem']+'.png')).read_bytes();assert SHA(raw)==row['png_sha256']
        meta=json.loads((folder/(row['stem']+'-render.json')).read_text());assert meta['png_sha256']==row['png_sha256'] and meta['game_version']==row['version']
        assert meta['appearance']['input_sha256']==row['input_sha256']
        assert (row['png_sha256']==row['old_png_sha256'])==row['same_png']
    assert len(r['replays'])==relationships==583 and cells==1166 and len(r['smoke'])==6
    assert r['summary']=={'replays':583,'pixel_drift':415,'changed_relationships':0,'pending':76,'smoke_png_changed':6}
    result={'report_sha256':SHA((ROOT/'experiments/update-001.json').read_bytes()),'verified':{'comparisons':583,'rgba_cells':cells,'comparison_relationships_confirmed':relationships,'distinct_private_inputs':len(input_files),'stock_smoke_pairs':6,'restoration_original_hash_links':len(original_links)},'source_tree_sha256':SHA(json.dumps(r['source_hashes'],sort_keys=True,separators=(',',':')).encode()),'original_hash_links':original_links}
    (folder/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='original_hash_links'}))
if __name__=='__main__':main()
