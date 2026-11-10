"""UPDATE-006: all twelve static fixtures, complete state reset controls."""
import asyncio
from dataclasses import asdict
import importlib.metadata
import json
from pathlib import Path
import sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame, FrameState
from morph_pixel_probe import draw, pixel_diff
from research_common import ROOT, SHA, save_result

OUT = ROOT/'scratch/research/update-006'


def choices(state):
    return {'full': state, 'geometry_only': FrameState(geometry=state.geometry),
            'host_texture_only': FrameState(orientations=state.orientations),
            'paint_angles_only': FrameState(paint_angles=state.paint_angles),
            'all_texture_only': FrameState(orientations=state.orientations, paint_angles=state.paint_angles),
            'fresh': None}


def state_hash(state):
    return SHA(json.dumps(asdict(state), sort_keys=True).encode())


def evaluate(case, folder, verify=False):
    """Reproduce fixed geometry with fresh raster RNG; persist draw write-back."""
    resolver = ResourceResolver((ROOT/'games/petz4',))
    assert SHA((ROOT/'games/petz4'/case['source']).read_bytes()) == case['source_sha256']
    assets = load_breed_assets(resolver, case['source'], pose=case['pose'], seed=0, age=100, fatness=50)
    state = first = initial = None
    frames, resets = [], []

    def record(prepared, name):
        fb, after, png = draw(assets, prepared, bounds)
        path = folder/(name+'.png')
        if verify:
            assert path.read_bytes() == png
        else:
            path.write_bytes(png)
        return fb, after, {'png': path.name, 'png_sha256': SHA(png),
            'indexed_sha256': SHA(fb.pixels), 'changed_from_first': pixel_diff(first.pixels, fb.pixels) if first else 0,
            'state_sha256': state_hash(after)}

    for frame in range(1, 9):
        before = state
        prepared = prepare_frame(assets.appearance, assets.sizes, assets.frame,
            textures=assets.textures, state=before, fatness=50, yaw=case['yaw_units'])
        if initial is None:
            initial = prepared
            bounds = prepared.geometry.ordering.bounds
        assert prepared.geometry.balls == initial.geometry.balls
        assert prepared.geometry.ordering.bounds == bounds
        fb, state, rec = record(prepared, f'frame{frame}')
        if first is None:
            first = fb
        frames.append({'frame': frame, **rec})
        if frame in (3, 8):
            for name, supplied in choices(before).items():
                control = prepare_frame(assets.appearance, assets.sizes, assets.frame,
                    textures=assets.textures, state=supplied, fatness=50, yaw=case['yaw_units'])
                assert control.geometry.balls == initial.geometry.balls
                assert control.geometry.ordering.bounds == bounds
                _, _, result = record(control, f'frame{frame}-{name}')
                resets.append({'frame': frame, 'component': name, **result})
            full = next(r for r in resets if r['frame'] == frame and r['component'] == 'full')
            assert full['indexed_sha256'] == rec['indexed_sha256']
            fresh = next(r for r in resets if r['frame'] == frame and r['component'] == 'fresh')
            assert fresh['indexed_sha256'] == frames[0]['indexed_sha256']
    return {'frames': frames, 'resets': resets}


async def main():
    OUT.mkdir(parents=True, exist_ok=False)
    historical_path = ROOT/'experiments/texture-001.json'
    historical = json.loads(historical_path.read_text())
    upgrade = json.loads((ROOT/'experiments/update-001.json').read_text())
    for name, digest in upgrade['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    cases = []
    for old in historical['cases']:
        stem = f"{old['species']}-{old['pose']}-{old['yaw_degrees']}"
        folder = OUT/stem
        folder.mkdir()
        case = {k: old[k] for k in ('species', 'source', 'source_sha256', 'pose', 'yaw_degrees', 'yaw_units')}
        case['folder'] = stem
        case.update(evaluate(case, folder))
        case['historical_changed_counts'] = [r['changed_from_first'] for r in old['sequence']['frames']]
        cases.append(case)
        print(stem, [r['changed_from_first'] for r in case['frames']], flush=True)
    transport = StdioTransport(sys.executable, ['-I', '-m', 'petz_renderer.service.local_mcp',
        '--game-version', 'petz4', '--game-root', str(ROOT/'games/petz4')])
    async with Client(transport) as client:
        for case in cases:
            args = {'path': case['source'], 'pose': case['pose'], 'seed': 0,
                    'age': 100, 'fatness': 50, 'yaw_degrees': case['yaw_degrees']}
            png, meta = await save_result(client, 'render_pet', args, OUT/case['folder'], 'mcp-first')
            assert meta['game_version'] == 'petz4'
            assert SHA(png) == case['frames'][0]['png_sha256']
            case['mcp_controls'] = args
    report = {'experiment': 'UPDATE-006', 'renderer_revision': upgrade['renderer_revision'],
        'backend': 'direct explicit FrameState; local stdio MCP fresh baselines',
        'historical_manifest_sha256': SHA(historical_path.read_bytes()),
        'source_hashes': upgrade['source_hashes'],
        'dependencies': {n: importlib.metadata.version(n) for n in ('petz-renderer-mcp', 'fastmcp', 'pillow')},
        'controls': {'game_version': 'petz4', 'seed': 0, 'age': 100, 'fatness': 50,
            'raster_seed': 1, 'line_rng_seed': 1, 'step': 0, 'animation_frame': 'fixed named pose',
            'state': 'persist draw-returned FrameState; reset controls branch from before target draw'},
        'engine_hashes': json.loads((ROOT/'experiments/restore-002.json').read_text())['shared_engine_hashes']['petz4'],
        'cases': cases,
        'summary': {'fixtures': len(cases), 'sequence_frames': 8*len(cases), 'reset_draws': 12*len(cases),
            'mcp_fresh_baselines': len(cases),
            'fixtures_with_sequence_drift': sum(any(r['changed_from_first'] for r in c['frames']) for c in cases),
            'fixtures_with_count_corrections': sum([r['changed_from_first'] for r in c['frames']] != c['historical_changed_counts'] for c in cases)}}
    for path in (OUT/'report.json', ROOT/'experiments/update-006.json'):
        path.write_text(json.dumps(report, indent=2)+'\n')
    print(report['summary'], flush=True)


if __name__ == '__main__':
    asyncio.run(main())
