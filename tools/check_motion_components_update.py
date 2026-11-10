"""Replay UPDATE-007 and audit its UPDATE-002 state/baseline links."""
import json
from pathlib import Path
import importlib.metadata
import petz_renderer
from research_common import ROOT, SHA
from revalidate_motion_components import evaluate, PRIOR


def main():
    path = ROOT/'experiments/update-007.json'
    folder = ROOT/'scratch/research/update-007'
    report = json.loads(path.read_text())
    assert report == json.loads((folder/'report.json').read_text())
    prior_path = PRIOR/'report.json'
    assert SHA(prior_path.read_bytes()) == report['prior_report_sha256']
    prior = json.loads(prior_path.read_text())
    update = json.loads((ROOT/'experiments/update-001.json').read_text())
    assert report['source_hashes'] == update['source_hashes']
    assert report['renderer_revision'] == update['renderer_revision']
    assert report['controls'] == prior['controls']
    for name, digest in report['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    for name, version in report['dependencies'].items():
        assert importlib.metadata.version(name) == version
    for name, digest in report['engine_hashes'].items():
        assert SHA((ROOT/name).read_bytes()) == digest
    authoring = json.loads((ROOT/'experiments/line-021.json').read_text())
    baseline_links = set()
    for case, old, paint_scope in zip(report['cases'], prior['cases'], report['before_final_paint_angle_scope'], strict=True):
        saved = json.loads((PRIOR/old['private_state_file']).read_text())
        angles = saved['before_final_state']['paint_angles']
        assert paint_scope == {'slots':len(angles), 'nonzero_pairs':sum(any(a) for a in angles)}
        for key in ('species','pose','yaw_degrees','yaw_units','history','input','input_sha256'):
            assert case[key] == old[key]
        source = next(c for c in authoring['cases'] if c['species'] == case['species'] and c['dimensions'] == [128,128])
        assert case['input'] == source['paths']['textured']
        assert case['input_sha256'] == source['input_hashes']['textured']
        assert SHA((ROOT/source['source_path']).read_bytes()) == source['source_sha256']
        regenerated = evaluate(case, old, folder/case['folder'], verify=True)
        assert regenerated == {k:case[k] for k in regenerated}
        baseline = next(b for b in prior['baselines'] if (b['species'],b['pose'],b['yaw_degrees']) ==
                        (case['species'],case['pose'],case['yaw_degrees']))
        assert baseline['input_sha256'] == case['input_sha256']
        assert case['outputs']['fresh']['png_sha256'] == baseline['png_sha256']
        assert SHA((PRIOR/baseline['png']).read_bytes()) == baseline['png_sha256']
        meta = json.loads((PRIOR/(Path(baseline['png']).stem+'-mcp.json')).read_text())
        assert meta['game_version'] == 'petz4' and meta['png_sha256'] == baseline['png_sha256']
        assert baseline['input_sha256'] in json.dumps(meta)
        baseline_links.add(baseline['png'])
    cases = report['cases']
    summary = {'histories':len(cases), 'transition_states':4*len(cases), 'final_draws':7*len(cases),
        'host_vs_combined_differences':sum(not c['host_equals_combined'] for c in cases),
        'paint_only_vs_fresh_differences':sum(not c['paint_only_equals_fresh'] for c in cases),
        'combined_vs_full_differences':sum(not c['combined_equals_full'] for c in cases),
        'diagnostic_changes':sum(o['diagnostic']['indexed_sha256'] != c['outputs']['fresh']['diagnostic']['indexed_sha256']
                                 for c in cases for o in c['outputs'].values())}
    assert summary == report['summary']
    assert len(cases) == 48 and len(baseline_links) == 12
    result = {'report_sha256':SHA(path.read_bytes()), 'verified':summary,
              'linked_existing_mcp_baselines':len(baseline_links), 'new_mcp_calls':0,
              'prior_final_pixel_links':5*len(cases), 'source_files':len(report['source_hashes'])}
    (folder/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
