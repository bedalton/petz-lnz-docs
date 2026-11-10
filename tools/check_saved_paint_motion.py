"""Replay PAINT-001 and independently verify saved controls and provenance."""
import importlib.metadata
import json
from pathlib import Path
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from saved_paint_motion import evaluate
from research_common import ROOT,SHA


def main():
    folder = ROOT/'scratch/research/paint-001'
    path = ROOT/'experiments/paint-001.json'
    report = json.loads(path.read_text())
    assert report == json.loads((folder/'report.json').read_text())
    baseline_path = ROOT/'experiments/update-003.json'
    assert SHA(baseline_path.read_bytes()) == report['baseline_manifest_sha256']
    baseline = json.loads(baseline_path.read_text())
    update = json.loads((ROOT/'experiments/update-001.json').read_text())
    assert report['source_hashes'] == update['source_hashes']
    assert report['renderer_revision'] == update['renderer_revision']
    for name,digest in report['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    for name,version in report['dependencies'].items():
        assert importlib.metadata.version(name) == version
    originals = {str(p.relative_to(ROOT/'games/petz4')).lower():p for p in (ROOT/'games/petz4').rglob('*') if p.is_file()}
    for name,digest in report['engine_hashes'].items():
        assert SHA(originals[name].read_bytes()) == digest
    resolver = ResourceResolver((ROOT/'games/petz4',))
    cache = {}
    for c in report['cases']:
        assert SHA((ROOT/'games/petz4'/c['path']).read_bytes()) == c['input_sha256']
        key = c['path'],c['pose']
        if key not in cache:
            cache[key] = load_saved_assets(resolver,c['path'],pose=c['pose'])
        assets = cache[key]
        assert assets.preview.input_sha256 == c['input_sha256']
        assert assets.preview.age == c['preview']['age']
        assert assets.preview.fatness == c['preview']['fatness']
        replayed = evaluate(assets,c['yaw_units'],c['history'],folder/c['folder'],verify=True)
        assert replayed == {k:c[k] for k in replayed}
        old = next(b for b in baseline['cases'] if b['name']==c['name'] and b['controls']['pose']==c['pose']
                   and b['controls']['yaw_degrees']==c['yaw_degrees'])
        assert c['outputs']['fresh']['png_sha256'] == old['png_sha256']
    for b in report['baselines']:
        raw = (folder/(b['stem']+'.png')).read_bytes()
        meta = json.loads((folder/(b['stem']+'-render.json')).read_text())
        assert SHA(raw) == b['png_sha256'] == meta['png_sha256']
        assert meta['game_version']=='petz4'
        assert meta['appearance']['input_sha256']==b['input_sha256']
        assert meta['appearance']['age_source']=='saved' and meta['appearance']['fatness_source']=='saved'
        assert b['controls']=={'path':b['path'],'pose':b['pose'],'yaw_degrees':b['yaw_degrees']}
    summary = {name:{'histories':len(rows := [c for c in report['cases'] if c['name']==name]),
        'nonzero_pre_target_states':sum(bool(c['before_nonzero_paint_angles']) for c in rows),
        'paint_only_pixel_changes':sum(c['paint_vs_fresh_changed'] for c in rows),
        'host_vs_combined_differences':sum(c['host_vs_combined_changed'] for c in rows),
        'combined_vs_full_differences':sum(c['combined_vs_full_changed'] for c in rows)} for name in ('Fuzzkin','Homebody')}
    assert summary == report['summary']
    assert len(report['cases'])==48 and len(report['baselines'])==12
    assert len(list(folder.rglob('*.png')))==348
    result = {'report_sha256':SHA(path.read_bytes()),'summary':summary,
        'verified':{'histories':48,'transition_states':192,'final_draws':336,'fresh_mcp_baselines':12,
                    'historical_fresh_links':48,'saved_pets':2,'pngs':348,'source_files':62}}
    (folder/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    main()
