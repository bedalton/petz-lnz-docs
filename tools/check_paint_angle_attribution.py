"""Verify PAINT-002 exact reproductions and PAINT-001 cross-unit links."""
import importlib.metadata
import json
from pathlib import Path
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from paint_angle_attribution import evaluate
from research_common import ROOT,SHA


def main():
    folder=ROOT/'scratch/research/paint-002';path=ROOT/'experiments/paint-002.json'
    report=json.loads(path.read_text());assert report==json.loads((folder/'report.json').read_text())
    prior_path=ROOT/'experiments/paint-001.json'
    assert SHA(prior_path.read_bytes())==report['prior_manifest_sha256']
    prior=json.loads(prior_path.read_text())
    assert report['source_hashes']==prior['source_hashes']
    assert report['renderer_revision']==prior['renderer_revision']
    assert report['controls']==prior['controls']
    for name,digest in report['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes())==digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==digest
    for name,version in report['dependencies'].items():assert importlib.metadata.version(name)==version
    originals={str(p.relative_to(ROOT/'games/petz4')).lower():p for p in (ROOT/'games/petz4').rglob('*') if p.is_file()}
    for name,digest in prior['engine_hashes'].items():assert SHA(originals[name].read_bytes())==digest
    resolver=ResourceResolver((ROOT/'games/petz4',));cache={}
    for c in report['cases']:
        old=next(p for p in prior['cases'] if p['folder']==c['prior_folder'])
        for key in ('name','path','input_sha256','pose','yaw_degrees','yaw_units','history'):assert c[key]==old[key]
        assert SHA((ROOT/'games/petz4'/c['path']).read_bytes())==c['input_sha256']
        if c['pose'] not in cache:cache[c['pose']]=load_saved_assets(resolver,c['path'],pose=c['pose'])
        replayed=evaluate(old,cache[c['pose']],folder/c['folder'],verify=True)
        assert replayed=={k:c[k] for k in replayed}
        for name,oldname in (('combined','all_texture_only'),('host','host_texture_only')):
            oldrow=old['outputs'][oldname]
            assert SHA((ROOT/'scratch/research/paint-001'/old['folder']/oldrow['png']).read_bytes())==oldrow['png_sha256']==c['outputs'][name]['png_sha256']
    summary={'cases':len(report['cases']),'final_draws':6*len(report['cases']),'prior_pixel_links':2*len(report['cases']),
        'all_angle_resets_match_host':sum(c['outputs']['reset_all']['indexed_sha256']==c['outputs']['host']['indexed_sha256'] for c in report['cases']),
        'individual_visible_cases':{str(i):sum(bool(c['outputs'][f'reset_{i}']['changed_from_combined']) for c in report['cases']) for i in (16,17,18)}}
    assert summary==report['summary']
    assert len(report['cases'])==24 and len(list(folder.rglob('*.png')))==144
    result={'report_sha256':SHA(path.read_bytes()),'verified':summary,'new_mcp_calls':0,'pngs':144}
    (folder/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':main()
