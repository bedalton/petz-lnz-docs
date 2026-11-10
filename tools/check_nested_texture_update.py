"""Verify UPDATE-005 bytes, provenance and current cross-version links."""
import importlib.metadata
import json
from pathlib import Path
from PIL import Image
import petz_renderer
from research_common import ROOT, SHA
from revalidate_renderer_update import partition
from revalidate_nested_textures import geometry_checks


def main():
    folder = ROOT/'scratch/research/update-005'
    path = ROOT/'experiments/update-005.json'
    report = json.loads(path.read_text())
    assert report == json.loads((folder/'report.json').read_text())
    old_path = ROOT/'experiments/line-016.json'
    p4_path = ROOT/'experiments/update-001.json'
    assert SHA(old_path.read_bytes()) == report['historical_manifest_sha256']
    assert SHA(p4_path.read_bytes()) == report['updated_petz4_manifest_sha256']
    old = json.loads(old_path.read_text())
    p4 = json.loads(p4_path.read_text())
    assert report['renderer_revision'] == p4['renderer_revision']
    assert report['source_hashes'] == p4['source_hashes']
    for name, digest in report['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    for name, version in report['dependencies'].items():
        assert importlib.metadata.version(name) == version
    for name, digest in {**report['input_hashes'], **report['engine_hashes']}.items():
        assert SHA((ROOT/name).read_bytes()) == digest
    for nested in old['reports']:
        version = nested['game_version']
        assert geometry_checks(nested, ROOT/'scratch/research/line-016'/version) == report['geometry_checks'][version]
    cells = drift = 0
    assert len({(r['game_version'], r['index']) for r in report['replays']}) == 32
    for row in report['replays']:
        nested = next(r for r in old['reports'] if r['game_version'] == row['game_version'])
        historical = nested['comparisons'][row['index']]
        current = next(r for r in p4['replays'] if r['experiment'] == 'line-013' and r['index'] == row['index'])
        assert row['controls'] == historical['controls'] == current['controls']
        raw = (folder/(row['stem']+'.png')).read_bytes()
        assert SHA(raw) == row['png_sha256'] == current['png_sha256']
        meta = json.loads((folder/(row['stem']+'-render.json')).read_text())
        assert meta['game_version'] == row['game_version']
        assert meta['png_sha256'] == row['png_sha256']
        assert row['cell_hashes'] == current['cell_hashes']
        with Image.open(folder/(row['stem']+'.png')) as im:
            rgba = im.convert('RGBA')
            for cell, digest in zip(meta['cells'], row['cell_hashes'], strict=True):
                assert cell['game_version'] == row['game_version']
                x, y = cell['origin']
                assert SHA(rgba.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes()) == digest == cell['pixel_sha256']
                cells += 1
        assert row['historical_relationship_confirmed'] is True
        assert partition(historical['cell_hashes']) == partition(row['cell_hashes'])
        assert row['updated_petz4_png_match'] is True
        changed = historical['cell_hashes'] != row['cell_hashes']
        assert row['historical_cells_changed'] == changed
        drift += changed
    summary = {'comparisons': 32, 'rgba_cells': cells, 'numerical_loads': 60,
               'historical_cell_pairs_changed': drift, 'current_petz4_exact_matches': 32}
    assert summary == report['summary']
    result = {'report_sha256': SHA(path.read_bytes()), 'verified': summary,
              'private_inputs': len(report['input_hashes']), 'installed_sources': len(report['source_hashes'])}
    (folder/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
