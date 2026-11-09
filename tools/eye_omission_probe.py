"""Iris/host omission combinations with four-branch local MCP sheets."""
import asyncio
import json
import subprocess
import sys
from dataclasses import fields
from pathlib import Path
import petz_renderer
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.appearance.variations import inspect_variations
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame
from research_common import ROOT, SHA, adult, write_copy, save_result

OUT = ROOT / 'scratch/research/eye-002'

def checkpoint(report):
    temp = OUT / 'progress.tmp'
    temp.write_text(json.dumps(report, indent=2) + '\n')
    temp.replace(OUT / 'progress.json')

def prepare():
    cases = []
    for species in ('Dogz', 'Catz'):
        source, raw, leaf, base, master, _ = adult(species)
        baseline = load_layer(ResourceFile(raw), master, name=leaf.name, seed=0)
        eye = baseline.appearance.eyes
        variants = {'control': [], 'iris': [eye.right_iris], 'host': [eye.right_eye],
                    'both': [eye.right_iris, eye.right_eye]}
        rows = list(base.get('Omissions', ()))
        rows.append('#4.0')
        rows.extend(('#3', str(eye.right_iris), '#2', str(eye.right_eye),
                     '#1', str(eye.right_iris), str(eye.right_eye), '##'))
        sections = dict(base)
        sections['Omissions'] = tuple(rows)
        path = OUT / f'{species}-eye-omissions{source.suffix}'
        digest = write_copy(raw, leaf, sections, path)
        data = path.read_bytes()
        payload = ResourceFile(data).read('LNZ', leaf.name)
        seeds = {}
        for seed in range(1000):
            trace = inspect_variations(payload, seed=seed)
            assert len(trace.blocks) == 1
            seeds.setdefault(trace.blocks[0].selected_branch, seed)
            if len(seeds) == 4:
                break
        assert len(seeds) == 4
        resolver = ResourceResolver((ROOT / 'games/petz4', OUT))
        checks = []
        for branch, (variant, ids) in zip((4, 3, 2, 1), variants.items()):
            layer = load_layer(ResourceFile(data), master, name=leaf.name, seed=seeds[branch])
            expected = dict(baseline.sections)
            if ids:
                expected['Omissions'] = (*expected.get('Omissions', ()), *(str(i) for i in ids))
            assert dict(layer.sections) == expected
            a = load_breed_assets(resolver, path.name, pose='standing', seed=seeds[branch], age=100, fatness=50)
            assert a.appearance.omissions == baseline.appearance.omissions | set(ids)
            assert all(getattr(a.appearance, f.name) == getattr(baseline.appearance, f.name)
                       for f in fields(a.appearance) if f.name not in ('omissions', 'lines'))
            p = prepare_frame(a.appearance, a.sizes, a.frame, textures=a.textures, fatness=50)
            checks.append({'variant': variant, 'seed': seeds[branch], 'added_omissions': ids,
                           'host_visible': p.balls[eye.right_eye].visible,
                           'iris_visible': p.balls[eye.right_iris].visible,
                           'host_overlay_exists': p.balls[eye.right_eye].eye is not None,
                           'line_count': len(a.appearance.lines)})
        cases.append({'species': species, 'path': path.name, 'source_sha256': SHA(raw),
                      'input_sha256': digest, 'master_sha256': SHA((ROOT / f'games/petz4/Resource/{species} 4 Rez.dll').read_bytes()),
                      'right_host_id': eye.right_eye, 'right_iris_id': eye.right_iris, 'checks': checks})
    return cases

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    root = Path(petz_renderer.__file__).parent
    runtime_hash = SHA(b''.join(p.relative_to(root).as_posix().encode() + b'\0' + p.read_bytes()
                              for p in sorted(root.rglob('*.py'))))
    reference = json.loads((ROOT / 'experiments/vis-001.json').read_text())
    assert runtime_hash == reference['installed_python_sources_sha256']
    revision = subprocess.check_output(['git', '-C', str(ROOT / 'petz-renderer-mcp'), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == reference['renderer_revision']
    if (OUT / 'progress.json').exists():
        report = json.loads((OUT / 'progress.json').read_text())
        assert report['installed_python_sources_sha256'] == runtime_hash and report['python'] == sys.version
        for c in report['cases']:
            assert SHA(adult(c['species'])[1]) == c['source_sha256']
            assert SHA((OUT / c['path']).read_bytes()) == c['input_sha256']
            assert SHA((ROOT / f"games/petz4/Resource/{c['species']} 4 Rez.dll").read_bytes()) == c['master_sha256']
        for p in report['pages']:
            assert SHA((OUT / (p['stem'] + '.png')).read_bytes()) == p['png_sha256']
    else:
        report = {'experiment': 'EYE-002', 'backend': 'local stdio MCP render_contact_sheet',
                  'renderer_revision': revision, 'python': sys.version,
                  'installed_python_sources_sha256': runtime_hash, 'cases': prepare(), 'pages': []}
        checkpoint(report)
    transport = StdioTransport(sys.executable, ['-I', '-m', 'petz_renderer.service.local_mcp',
        '--game-root', str(ROOT / 'games/petz4'), '--asset-root', str(OUT)])
    async with Client(transport) as client:
        for c in report['cases']:
            for yaw in (0, 90):
                stem = f"{c['species']}-yaw{yaw}"
                if any(p['stem'] == stem for p in report['pages']):
                    continue
                args = {'path': c['path'], 'pose': 'standing', 'seeds': [x['seed'] for x in c['checks']],
                        'age': 100, 'fatness': 50, 'yaw_degrees': yaw, 'columns': 4}
                png, meta = await save_result(client, 'render_contact_sheet', args, OUT, stem)
                assert len(meta['cells']) == 4
                hashes = [x['pixel_sha256'] for x in meta['cells']]
                report['pages'].append({'stem': stem, 'species': c['species'], 'controls': args,
                                        'cell_variants': ['control', 'iris', 'host', 'both'],
                                        'png_sha256': SHA(png), 'cell_hashes': hashes,
                                        'iris_equal_control': hashes[1] == hashes[0],
                                        'host_equal_both': hashes[2] == hashes[3],
                                        'host_equal_control': hashes[2] == hashes[0]})
                checkpoint(report)
                print(stem, report['pages'][-1], flush=True)
    assert len(report['pages']) == 4
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    (ROOT / 'experiments/eye-002.json').write_text(json.dumps(report, indent=2) + '\n')

if __name__ == '__main__':
    asyncio.run(main())
