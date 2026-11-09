"""Focused, checkpointed local MCP omission views for Catz 55/56."""
import asyncio
import json
import sys
import subprocess
from pathlib import Path
import petz_renderer
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from research_common import ROOT, SHA, adult, save_result

OUT = ROOT / 'scratch/research/vis-002'

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sweep_bytes = (ROOT / 'experiments/omit-001.json').read_bytes()
    sweep = json.loads(sweep_bytes)
    case = next(c for c in sweep['cases'] if c['species'] == 'Catz')
    geometry = json.loads((ROOT / 'experiments/vis-001.json').read_text())
    runtime_hash = SHA(b''.join(
        p.relative_to(Path(petz_renderer.__file__).parent).as_posix().encode() + b'\0' + p.read_bytes()
        for p in sorted(Path(petz_renderer.__file__).parent.rglob('*.py'))))
    assert runtime_hash == geometry['installed_python_sources_sha256']
    assert subprocess.check_output(['git', '-C', str(ROOT / 'petz-renderer-mcp'),
                                    'rev-parse', 'HEAD'], text=True).strip() == sweep['renderer_revision']
    master_hash = SHA((ROOT / 'games/petz4/Resource/Catz 4 Rez.dll').read_bytes())
    assert master_hash == next(c for c in geometry['cases'] if c['species'] == 'Catz')['master_sha256']
    assert SHA(adult('Catz')[1]) == case['source_sha256']
    assert SHA((ROOT / 'scratch/research/omit-001' / case['path']).read_bytes()) == case['input_sha256']
    pages = []
    checkpoint = OUT / 'progress.json'
    if checkpoint.exists():
        saved = json.loads(checkpoint.read_text())
        assert saved['omission_manifest_sha256'] == SHA(sweep_bytes)
        assert saved['installed_python_sources_sha256'] == runtime_hash
        assert saved['python'] == sys.version
        pages = saved['pages']
        for page in pages:
            assert SHA((OUT / (page['stem'] + '.png')).read_bytes()) == page['png_sha256']
    report = {'experiment': 'VIS-002', 'backend': 'local stdio MCP render_contact_sheet',
              'renderer_revision': sweep['renderer_revision'], 'python': sys.version,
              'runtime_reference': 'vis-001.json', 'master_sha256': master_hash,
              'installed_python_sources_sha256': geometry['installed_python_sources_sha256'],
              'source_sha256': case['source_sha256'], 'input_sha256': case['input_sha256'],
              'omission_manifest_sha256': SHA(sweep_bytes), 'pages': pages}
    transport = StdioTransport(sys.executable, ['-I', '-m', 'petz_renderer.service.local_mcp',
        '--game-root', str(ROOT / 'games/petz4'), '--asset-root', str(ROOT / 'scratch/research/omit-001')])
    async with Client(transport) as client:
        for pose in ('standing', 'sitting', 'lying'):
            for yaw in (0, 90, 180, 270):
                stem = f'Catz-{pose}-yaw{yaw}'
                if any(p['stem'] == stem for p in pages):
                    continue
                ids = [None, 55, 56, 24]
                seeds = [case['control_seed']] + [case['seed_by_ball'][str(i)] for i in ids[1:]]
                args = {'path': case['path'], 'pose': pose,
                        'age': 100, 'fatness': 50, 'yaw_degrees': yaw,
                        'seeds': seeds, 'columns': 4}
                png, meta = await save_result(client, 'render_contact_sheet', args, OUT, stem)
                assert len(meta['cells']) == 4
                control = meta['cells'][0]['pixel_sha256']
                pages.append({'stem': stem, 'controls': args, 'cell_ball_ids': ids,
                              'png_sha256': SHA(png),
                              'cells': [{'ball': ball, 'pixel_sha256': cell['pixel_sha256'],
                                         'same_as_control': cell['pixel_sha256'] == control}
                                        for ball, cell in zip(ids, meta['cells'])]})
                temp = checkpoint.with_suffix('.tmp')
                temp.write_text(json.dumps(report, indent=2) + '\n')
                temp.replace(checkpoint)
                print(stem, [(c['ball'], c['same_as_control']) for c in pages[-1]['cells']], flush=True)
    assert len(pages) == 12
    assert len({(p['controls']['pose'], p['controls']['yaw_degrees']) for p in pages}) == 12
    assert all(not p['cells'][3]['same_as_control'] for p in pages)
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    (ROOT / 'experiments/vis-002.json').write_text(json.dumps(report, indent=2) + '\n')

if __name__ == '__main__':
    asyncio.run(main())
