"""UPDATE-005: replay nested LINE-016 without replacing historical evidence."""
import asyncio
import importlib.metadata
import json
import sys
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.connectors import build_line_block
from research_common import ROOT, SHA, adult, save_result
from revalidate_renderer_update import partition

OUT = ROOT / 'scratch/research/update-005'


def geometry_checks(report, folder):
    version = report['game_version']
    resolver = ResourceResolver((ROOT/'games'/version, folder), game_version=version)
    results = []
    for case in report['cases']:
        source, *_ = adult(case['species'], version)
        assert SHA(source.read_bytes()) == case['source_sha256']
        for name, digest in case['input_hashes'].items():
            assert SHA((folder/case['paths'][name]).read_bytes()) == digest
        shapes = {}
        for old in case['geometry']:
            pose, name = old['pose'], old['variant']
            assets = load_breed_assets(resolver, case['paths'][name], pose=pose,
                                       seed=0, age=100, fatness=50)
            shape = posed_geometry(assets.appearance, assets.sizes, assets.frame, fatness=50)
            if pose in shapes:
                assert shapes[pose] == shape
            else:
                shapes[pose] = shape
            prepared = prepare_frame(assets.appearance, assets.sizes, assets.frame,
                                     textures=assets.textures, fatness=50)
            block = build_line_block(assets.appearance.lines[-1], tuple(b.endpoint for b in prepared.balls))
            assert block is not None
            texture = assets.textures[old['texture_index']]
            new = {'pose': pose, 'variant': name,
                   'line_color': assets.appearance.lines[-1].color,
                   'block_color': block.color, 'paint_present': block.paint is not None,
                   'texture_index': old['texture_index'],
                   'texture_pixels_sha256': SHA(texture.pixels),
                   'paint_pixels_sha256': None if block.paint is None else SHA(block.paint.texture.pixels)}
            assert new == old, (version, case['species'], pose, name, new, old)
            results.append({'species': case['species'], **new})
    return results


async def main():
    OUT.mkdir(parents=True, exist_ok=False)
    old_path = ROOT/'experiments/line-016.json'
    old = json.loads(old_path.read_text())
    baseline_path = ROOT/'experiments/update-001.json'
    baseline = json.loads(baseline_path.read_text())
    sources = baseline['source_hashes']
    for name, digest in sources.items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    rows, geometry, inputs, engines = [], {}, {}, {}
    for report in old['reports']:
        version = report['game_version']
        folder = ROOT/'scratch/research/line-016'/version
        geometry[version] = geometry_checks(report, folder)
        for name, digest in report['engine_hashes'].items():
            assert SHA((ROOT/name).read_bytes()) == digest
            engines[name] = digest
        for case in report['cases']:
            for name, digest in case['input_hashes'].items():
                inputs[str((folder/case['paths'][name]).relative_to(ROOT))] = digest
        transport = StdioTransport(sys.executable, ['-I', '-m', 'petz_renderer.service.local_mcp',
            '--game-version', version, '--game-root', str(ROOT/'games'/version), '--asset-root', str(folder)])
        async with Client(transport) as client:
            for index, rec in enumerate(report['comparisons']):
                stem = f'{version}-{index:02d}'
                png, meta = await save_result(client, 'compare_appearance', rec['controls'], OUT, stem)
                assert meta['game_version'] == version
                assert all(c['game_version'] == version for c in meta['cells'])
                cells = [c['pixel_sha256'] for c in meta['cells']]
                assert partition(cells) == partition(rec['cell_hashes'])
                p4 = next(r for r in baseline['replays'] if r['experiment'] == 'line-013' and r['index'] == index)
                assert p4['controls'] == rec['controls']
                assert cells == p4['cell_hashes']
                assert SHA(png) == p4['png_sha256']
                rows.append({'game_version': version, 'index': index, 'stem': stem,
                    'controls': rec['controls'], 'png_sha256': SHA(png), 'cell_hashes': cells,
                    'historical_cells_changed': cells != rec['cell_hashes'],
                    'historical_relationship_confirmed': True, 'updated_petz4_png_match': True})
                (OUT/'progress.json').write_text(json.dumps(rows, indent=2)+'\n')
                print(stem, 'confirmed; current Petz4 exact match', flush=True)
    result = {'experiment': 'UPDATE-005', 'backend': 'local stdio MCP, explicit Petz3/5 roots',
        'renderer_revision': baseline['renderer_revision'], 'source_hashes': sources,
        'dependencies': {n: importlib.metadata.version(n) for n in ('petz-renderer-mcp', 'fastmcp', 'pillow')},
        'historical_manifest_sha256': SHA(old_path.read_bytes()),
        'updated_petz4_manifest_sha256': SHA(baseline_path.read_bytes()),
        'input_hashes': inputs, 'engine_hashes': engines, 'geometry_checks': geometry, 'replays': rows,
        'summary': {'comparisons': len(rows), 'rgba_cells': 2*len(rows),
                    'numerical_loads': sum(map(len, geometry.values())),
                    'historical_cell_pairs_changed': sum(r['historical_cells_changed'] for r in rows),
                    'current_petz4_exact_matches': len(rows)}}
    for path in (OUT/'report.json', ROOT/'experiments/update-005.json'):
        path.write_text(json.dumps(result, indent=2)+'\n')
    print(result['summary'], flush=True)


if __name__ == '__main__':
    asyncio.run(main())
