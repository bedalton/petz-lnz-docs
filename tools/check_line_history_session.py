"""Integrity verification for LINE-010/011/012 saved evidence."""
import importlib.metadata,json
from io import BytesIO
from pathlib import Path
from PIL import Image
import petz_renderer
from research_common import ROOT,SHA,adult

def main():
    package=Path(petz_renderer.__file__).parent;copies=set();sheets=cells=states=mcp=loads=0
    def png_check(path,expected,cell_size,hashes):
        nonlocal sheets,cells
        data=path.read_bytes();assert SHA(data)==expected;sheets+=1
        with Image.open(BytesIO(data)) as im:
            rgba=im.convert('RGBA');w,h=cell_size;assert rgba.size==(w*len(hashes),h)
            for i,expected_cell in enumerate(hashes):
                expected_cell=expected_cell['rgba_sha256'] if isinstance(expected_cell,dict) else expected_cell
                assert SHA(rgba.crop((w*i,0,w*(i+1),h)).tobytes())==expected_cell;cells+=1
    for exp in ('line-010','line-011','line-012'):
        report=json.loads((ROOT/'experiments'/f'{exp}.json').read_text());folder=ROOT/'scratch/research'/exp
        assert report==json.loads((folder/'report.json').read_text())
        for name,h in report['source_hashes'].items():
            assert SHA((package/name).read_bytes())==h
            assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==h
        for name,v in report['dependencies'].items():assert importlib.metadata.version(name)==v
        for name,h in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==h
        for c in report['cases']:
            source,*_=adult(c['species']);assert SHA(source.read_bytes())==c['source_sha256']
            if exp=='line-010':
                loads+=len(c['geometry'])
                for variant,name in c['paths'].items():
                    path=folder/name;assert SHA(path.read_bytes())==c['input_hashes'][variant];copies.add(str(path))
            else:
                path=ROOT/c['input'];assert SHA(path.read_bytes())==c['input_sha256'];copies.add(str(path))
                png_check(folder/c['sheet'],c['sheet_sha256'],c['cell_size'],c['cell_hashes'])
                if exp=='line-011':
                    meta=json.loads((folder/f"{c['species']}-{c['pose']}-{c['yaw_degrees']}-mcp.json").read_text())
                    assert meta['png_sha256']==c['baseline_sha256'];mcp+=1
                    assert c['cell_hashes'][1]==c['cell_hashes'][2]==c['cell_hashes'][6]
                    assert c['local_mcp_baseline_match']
                    png_check(folder/c['baseline'],c['baseline_sha256'],c['cell_size'],[c['cell_hashes'][0]])
        for comparison in report.get('comparisons',[]):
            before,after=comparison['pair'];yaw=comparison['controls']['yaw_degrees'];stem=f"{comparison['species']}-{before}-{after}-{yaw}"
            meta=json.loads((folder/f'{stem}-render.json').read_text());assert meta['png_sha256']==comparison['png_sha256']
            assert [c['pixel_sha256'] for c in meta['cells']]==comparison['cell_hashes']
            assert comparison['cells_equal'] and comparison['cell_hashes'][0]==comparison['cell_hashes'][1]
            png_check(folder/f'{stem}.png',comparison['png_sha256'],(meta['cell_width'],meta['cell_height']),comparison['cell_hashes']);mcp+=1
        if exp=='line-011':
            full=json.loads((folder/'states.json').read_text());assert len(full)==84
            for c in report['cases']:
                rows=[r for r in full if (r['species'],r['pose'],r['yaw_degrees'])==(c['species'],c['pose'],c['yaw_degrees'])]
                for record,row in zip(c['histories'],rows,strict=True):
                    assert record==row['record']
                    for when in ('before','after'):
                        assert SHA(json.dumps(row[when],sort_keys=True).encode())==record[f'state_{when}_sha256'];states+=1
        elif exp=='line-012':
            full=json.loads((folder/'states.json').read_text());assert len(full)==72
            for c in report['cases']:
                stem=f"{c['species']}-{c['pose']}-{c['yaw_degrees']}"
                prior=json.loads((ROOT/'experiments/line-011.json').read_text())
                original=next(x for x in prior['cases'] if (x['species'],x['pose'],x['yaw_degrees'])==(c['species'],c['pose'],c['yaw_degrees']))
                assert c['cell_hashes'][0]==original['cell_hashes'][1]
                assert c['cell_hashes'][1]==original['cell_hashes'][5]
                assert c['cell_hashes'][4]==c['cell_hashes'][1] and c['cell_hashes'][5]==c['cell_hashes'][0]
                assert c['cell_hashes'][2]!=c['cell_hashes'][1] and c['cell_hashes'][3]!=c['cell_hashes'][0]
                group={r['label']:r['state'] for r in full if r['fixture']==stem}
                assert len(group)==6
                assert group['fresh']['after_scene']==group['only_target_connector_primed']['after_scene']==group['all_positive_fuzz_lines_primed']['after_scene']
                assert group['whisker0_primed']['after_scene']==group['primed_except_target_connector']['after_scene']==group['primed_except_positive_fuzz_lines']['after_scene']
                for row in (r for r in full if r['fixture']==stem):
                    assert SHA(json.dumps(row['state'],sort_keys=True).encode())==c[row['label']+'_state_sha256'];states+=2
    assert (len(copies),sheets,cells,states,mcp,loads)==(58,92,292,312,68,168)
    summary={'unique_private_copies':len(copies),'pngs_verified':sheets,'rgba_cells_verified':cells,'rng_table_snapshots_verified':states,'local_mcp_comparisons_or_baselines':mcp,'numerical_breed_loads_line010':loads,'sources_dependencies_resource_dlls_originals_verified':True}
    (ROOT/'scratch/research/line-history-session-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
