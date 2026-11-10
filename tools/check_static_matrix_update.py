"""Replay UPDATE-006 states and independently audit saved PNG/provenance links."""
import importlib.metadata
import json
from pathlib import Path
from PIL import Image
import petz_renderer
from research_common import ROOT, SHA
from revalidate_static_matrix import evaluate


def main():
    path = ROOT/'experiments/update-006.json'
    folder = ROOT/'scratch/research/update-006'
    report = json.loads(path.read_text())
    assert report == json.loads((folder/'report.json').read_text())
    old_path = ROOT/'experiments/texture-001.json'
    assert SHA(old_path.read_bytes()) == report['historical_manifest_sha256']
    old = json.loads(old_path.read_text())
    current = json.loads((ROOT/'experiments/update-001.json').read_text())
    assert report['source_hashes'] == current['source_hashes']
    assert report['renderer_revision'] == current['renderer_revision']
    for name, digest in report['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    for name, version in report['dependencies'].items():
        assert importlib.metadata.version(name) == version
    originals = {str(p.relative_to(ROOT/'games/petz4')).lower(): p
                 for p in (ROOT/'games/petz4').rglob('*') if p.is_file()}
    for name, digest in report['engine_hashes'].items():
        assert SHA(originals[name].read_bytes()) == digest
    assert len(report['cases']) == 12
    pngs = state_links = 0
    attribution = []
    for case, historical in zip(report['cases'], old['cases'], strict=True):
        for key in ('species', 'source', 'source_sha256', 'pose', 'yaw_degrees', 'yaw_units'):
            assert case[key] == historical[key]
        assert case['historical_changed_counts'] == [r['changed_from_first'] for r in historical['sequence']['frames']]
        local = folder/case['folder']
        replayed = evaluate(case, local, verify=True)
        assert replayed == {k: case[k] for k in ('frames', 'resets')}
        for row in case['frames'] + case['resets']:
            assert SHA((local/row['png']).read_bytes()) == row['png_sha256']
            with Image.open(local/row['png']) as im:
                assert im.width > 0 and im.height > 0
            pngs += 1
            state_links += 1
        meta = json.loads((local/'mcp-first-render.json').read_text())
        assert SHA((local/'mcp-first.png').read_bytes()) == meta['png_sha256'] == case['frames'][0]['png_sha256']
        assert meta['game_version'] == 'petz4'
        assert meta['appearance']['input_sha256'] == case['source_sha256']
        assert case['mcp_controls'] == {'path': case['source'], 'pose': case['pose'], 'seed': 0,
                                       'age': 100, 'fatness': 50, 'yaw_degrees': case['yaw_degrees']}
        pngs += 1
        for frame in (3, 8):
            rows = {r['component']: r for r in case['resets'] if r['frame'] == frame}
            full = rows['full']['indexed_sha256']
            fresh = rows['fresh']['indexed_sha256']
            attribution.append({'fixture': case['folder'], 'frame': frame,
                'full_changed_pixels': rows['full']['changed_from_first'],
                'host_matches_full': rows['host_texture_only']['indexed_sha256'] == full,
                'combined_texture_matches_full': rows['all_texture_only']['indexed_sha256'] == full,
                'paint_only_matches_fresh': rows['paint_angles_only']['indexed_sha256'] == fresh,
                'geometry_only_matches_fresh': rows['geometry_only']['indexed_sha256'] == fresh})
    assert pngs == 252 and state_links == 240
    summary = {'fixtures': 12, 'sequence_frames': 96, 'reset_draws': 144, 'mcp_fresh_baselines': 12,
        'fixtures_with_sequence_drift': sum(any(r['changed_from_first'] for r in c['frames']) for c in report['cases']),
        'fixtures_with_count_corrections': sum([r['changed_from_first'] for r in c['frames']] != c['historical_changed_counts'] for c in report['cases'])}
    assert summary == report['summary']
    result = {'report_sha256': SHA(path.read_bytes()), 'verified': summary, 'pngs': pngs,
              'replayed_draw_state_links': state_links, 'attribution': attribution}
    (folder/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
