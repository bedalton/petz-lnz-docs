"""Replay PAINT-003 vector interventions and check all cross-unit pixels."""
import importlib.metadata
import json
from pathlib import Path
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from paint_state_shape import evaluate
from research_common import ROOT,SHA


def main():
    folder=ROOT/'scratch/research/paint-003';path=ROOT/'experiments/paint-003.json'
    report=json.loads(path.read_text());assert report==json.loads((folder/'report.json').read_text())
    prior_path=ROOT/'experiments/paint-001.json'
    assert SHA(prior_path.read_bytes())==report['prior_manifest_sha256']
    prior=json.loads(prior_path.read_text())
    assert report['source_hashes']==prior['source_hashes']
    assert report['renderer_revision']==prior['renderer_revision']
    for name,digest in report['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes())==digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==digest
    for name,version in report['dependencies'].items():assert importlib.metadata.version(name)==version
    originals={str(p.relative_to(ROOT/'games/petz4')).lower():p for p in (ROOT/'games/petz4').rglob('*') if p.is_file()}
    for name,digest in prior['engine_hashes'].items():assert SHA(originals[name].read_bytes())==digest
    resolver=ResourceResolver((ROOT/'games/petz4',));cache={}
    for c in report['cases']:
        old=next(p for p in prior['cases'] if p['folder']==c['prior_folder'])
        assert old['name']=='Fuzzkin'
        assert SHA((ROOT/'games/petz4'/old['path']).read_bytes())==old['input_sha256']
        if old['pose'] not in cache:cache[old['pose']]=load_saved_assets(resolver,old['path'],pose=old['pose'])
        now=evaluate(old,cache[old['pose']],folder/c['folder'],verify=True)
        assert now=={k:c[k] for k in now}
        for name,oldname in (('combined','all_texture_only'),('host','host_texture_only')):
            p=old['outputs'][oldname]
            assert SHA((ROOT/'scratch/research/paint-001'/old['folder']/p['png']).read_bytes())==p['png_sha256']==c['outputs'][name]['png_sha256']
    assert len(report['cases'])==24 and len(list(folder.rglob('*.png')))==168
    summary={'cases':24,'final_draws':168,'prior_pixel_links':48,'length_mismatch_resets':48,
             'exact_zero_controls':24,'active_only_equivalences':24,'inactive_slot_equivalences':24}
    assert summary==report['summary']
    result={'report_sha256':SHA(path.read_bytes()),'verified':summary,'new_mcp_calls':0}
    (folder/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':main()
