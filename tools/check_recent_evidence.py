"""Verify current-session private evidence without changing it."""
import json
from collections import Counter
from petz_renderer.formats.resolver import ResourceResolver
from research_common import ROOT,SHA
EXPERIMENTS=('line-002','line-003','morph-001','area-001','line-004','area-002','area-003')
summary=[]
for experiment in EXPERIMENTS:
    report=json.loads((ROOT/'experiments'/f'{experiment}.json').read_text())
    folder=ROOT/'scratch/research'/experiment
    inputs=0
    for case in report['cases']:
        filename='Scottie.dog' if case['species']=='Dogz' else 'Siamese.cat'
        original=ROOT/'games/petz4/Resource'/case['species']/filename
        assert SHA(original.read_bytes())==case['source_sha256'], original
        for variant,name in case['paths'].items():
            assert SHA((folder/name).read_bytes())==case['input_hashes'][variant],name
            inputs+=1
    expected=Counter(r['png_sha256'] for r in report['comparisons'])
    actual=Counter(SHA(p.read_bytes()) for p in folder.glob('*.png'))
    assert expected==actual,experiment
    summary.append({'experiment':experiment,'private_inputs_verified':inputs,'comparison_pngs_verified':sum(actual.values()),'original_hashes_match':True})
provenance=json.loads((ROOT/'experiments/restore-002.json').read_text())
engine_count=0
for version,entries in provenance['shared_engine_hashes'].items():
    resolver=ResourceResolver((ROOT/'games'/version,),game_version=version)
    for path,expected in entries.items():
        assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
        engine_count+=1
print(json.dumps({'experiments':summary,'shared_engine_files_verified':engine_count},indent=2))
