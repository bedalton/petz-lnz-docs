"""Verify 2026-11-10 morph-session evidence without rerendering or edits."""
import json,importlib.metadata
from collections import Counter
from pathlib import Path
from PIL import Image
from petz_renderer.formats.resolver import ResourceResolver
from research_common import ROOT,SHA
EXPERIMENTS=('area-006','morph-002','morph-003')
def main():
    summary=[]
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent
    for experiment in EXPERIMENTS:
        report=json.loads((ROOT/'experiments'/f'{experiment}.json').read_text());folder=ROOT/'scratch/research'/experiment;inputs=0
        assert report==json.loads((folder/'report.json').read_text())
        for c in report['cases']:
            filename='Scottie.dog' if c['species']=='Dogz' else 'Siamese.cat'
            original=ROOT/'games/petz4/Resource'/c['species']/filename
            assert SHA(original.read_bytes())==c['source_sha256'],original
            for variant,name in c['paths'].items():
                assert SHA((folder/name).read_bytes())==c['input_hashes'][variant],name;inputs+=1
        expected=Counter(r['png_sha256'] for r in report['comparisons']);actual=Counter(SHA(p.read_bytes()) for p in folder.glob('*.png'))
        assert expected==actual,experiment
        pixel_cells=0;diagnostic_codes=set();renderer_versions=set()
        for png_path in folder.glob('*.png'):
            metadata=json.loads(png_path.with_name(png_path.stem+'-render.json').read_text())
            assert SHA(png_path.read_bytes())==metadata['png_sha256']
            renderer_versions.add(metadata['renderer_version'])
            with Image.open(png_path) as decoded:
                image=decoded.convert('RGBA')
                assert image.size==(metadata['width'],metadata['height'])
                cell_hashes=[]
                for cell in metadata['cells']:
                    x,y=cell['origin'];crop=image.crop((x,y,x+metadata['cell_width'],y+metadata['cell_height']))
                    pixel_hash=SHA(crop.tobytes());assert pixel_hash==cell['pixel_sha256'];cell_hashes.append(pixel_hash);pixel_cells+=1
                    diagnostic_codes.update(d['code'] for d in cell['diagnostics'])
                expected_record=next(r for r in report['comparisons'] if r['png_sha256']==metadata['png_sha256'])
                assert (cell_hashes[0]==cell_hashes[1])==expected_record['cells_equal']
        for name,version in report['dependency_versions'].items():assert importlib.metadata.version(name)==version
        for name,expected in report.get('source_hashes',{}).items():assert SHA((installed/name).read_bytes())==expected
        if 'evaluation_source_sha256' in report:assert SHA((installed/'appearance/evaluation.py').read_bytes())==report['evaluation_source_sha256']
        summary.append({'experiment':experiment,'private_inputs_verified':inputs,'comparison_pngs_verified':sum(actual.values()),'original_hashes_match':True,'runtime_matches':True,'rgba_cells_verified':pixel_cells,'renderer_versions':sorted(renderer_versions),'diagnostic_codes':sorted(diagnostic_codes)})
    public=json.loads((ROOT/'experiments/morph-004.json').read_text());private=json.loads((ROOT/'scratch/research/morph-004/report.json').read_text());snapshots=0
    for c,full in zip(public['cases'],private['cases'],strict=True):
        for name,h in c['histories'].items():
            for mode in ('batch','incremental'):
                expected=h[f'{mode}_snapshot_sha256'];actual=SHA(json.dumps(full['histories'][name][mode],sort_keys=True).encode());assert actual==expected;snapshots+=1
    for name,version in public['dependency_versions'].items():assert importlib.metadata.version(name)==version
    for name,expected in public['source_hashes'].items():assert SHA((installed/name).read_bytes())==expected
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text());engine_count=0
    for version,entries in provenance['shared_engine_hashes'].items():
        resolver=ResourceResolver((ROOT/'games'/version,),game_version=version)
        for path,expected in entries.items():assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path;engine_count+=1
    print(json.dumps({'experiments':summary,'assembly_snapshots_verified':snapshots,'shared_engine_files_verified':engine_count},indent=2))
if __name__=='__main__':main()
