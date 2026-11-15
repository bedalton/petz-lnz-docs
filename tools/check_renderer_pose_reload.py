"""UPDATE-013: check installed sources and live HTTP named/raw pose rendering."""
import asyncio
import base64
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path

from fastmcp import Client
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.output import render_portrait
from petz_renderer.rendering.presets import PRESETS
from research_common import ROOT, SHA

OUT = ROOT/'scratch/research/update-013'


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    package = Path(petz_renderer.__file__).parent
    sources = {str(p.relative_to(package)): SHA(p.read_bytes()) for p in package.rglob('*.py')}
    checkout = ROOT/'petz-renderer-mcp/src/petz_renderer'
    assert set(sources) == {str(p.relative_to(checkout)) for p in checkout.rglob('*.py')}
    for path, digest in sources.items():
        assert SHA((checkout/path).read_bytes()) == digest, path
    report = {'backend': 'restarted local HTTP MCP and fresh installed direct Python',
              'endpoint': 'http://127.0.0.1:8765/mcp',
              'revision': subprocess.check_output(['git', '-c', f'safe.directory={ROOT}/petz-renderer-mcp', '-C', str(ROOT/'petz-renderer-mcp'), 'rev-parse', 'HEAD'], text=True).strip(),
              'dependencies': {p: importlib.metadata.version(p) for p in ('petz-renderer-mcp', 'pillow', 'fastmcp', 'pefile')},
              'sources': sources, 'renders': [], 'script_sha256': SHA(Path(__file__).read_bytes()),
              'install_log_sha256': SHA((OUT/'install.log').read_bytes())}
    resolver = ResourceResolver((ROOT/'games/petz4',))
    expected = {'DOG': (79, 29), 'CAT': (263, 24)}
    async with Client(report['endpoint']) as client:
        tools = await client.list_tools()
        report['tools'] = sorted(t.name for t in tools)
        assert len(tools) == 6
        (OUT/'schemas.json').write_text(json.dumps([t.model_dump() for t in tools], indent=2)+'\n')
        caps = await client.call_tool('get_capabilities'); assert not caps.is_error
        (OUT/'capabilities.json').write_text(json.dumps(caps.data, indent=2)+'\n')
        poses = await client.call_tool('list_poses'); assert not poses.is_error
        (OUT/'poses.json').write_text(json.dumps(poses.data, indent=2)+'\n')
        for species, filename, kind in (('Dogz', 'Scottie.dog', 'DOG'), ('Catz', 'Siamese.cat', 'CAT')):
            path = f'Resource/{species}/{filename}'
            inspection = await client.call_tool('inspect_input', {'path': path, 'seed': 41})
            assert not inspection.is_error
            for pose in ('standing', 'sitting', 'lying'):
                preset = next(p for p in PRESETS if p.set_name == kind and p.name == pose)
                assert preset.catalogue == 'petz4-stock-v3'
                if pose == 'lying': assert (preset.animation, preset.frame) == expected[kind]
                assets = load_breed_assets(resolver, path, pose=pose, seed=41, age=100, fatness=50)
                for degrees in (0, 90):
                    controls = {'path': path, 'pose': pose, 'seed': 41, 'age': 100, 'fatness': 50, 'yaw_degrees': degrees}
                    named = await client.call_tool('render_pet', controls); assert not named.is_error
                    raw_controls = {**controls, 'pose': 'default', 'animation': preset.animation, 'frame': preset.frame}
                    raw = await client.call_tool('render_pet', raw_controls); assert not raw.is_error
                    png = base64.b64decode(next(c.data for c in named.content if c.type == 'image'))
                    raw_png = base64.b64decode(next(c.data for c in raw.content if c.type == 'image'))
                    direct = render_portrait(assets, yaw=degrees*256//360)
                    assert png == raw_png == direct.png
                    assert named.data['pose']['catalogue'] == 'petz4-stock-v3'
                    assert (named.data['animation'], named.data['frame']) == (preset.animation, preset.frame)
                    stem = f'{species}-{pose}-{degrees}'
                    (OUT/f'{stem}.png').write_bytes(png)
                    report['renders'].append({'controls': controls, 'raw_controls': raw_controls, 'png_sha256': SHA(png), 'matches_raw_and_direct': True, 'metadata': named.data})
            print(species, 'six named/raw/direct checks pass', flush=True)
    originals = json.loads(subprocess.check_output([sys.executable, str(ROOT/'tools/check_game_restore.py')], text=True))
    assert all(r['ok'] for r in originals['checks'])
    report['originals'] = originals
    (OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(f'RELOAD PASS: {len(sources)} installed source matches, six tools, 12 named/raw/direct triples, {len(originals["checks"])} originals')


if __name__ == '__main__':
    asyncio.run(main())
