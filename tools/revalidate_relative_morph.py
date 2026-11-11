"""MORPH-006: current-build relative morph replay across Petz 3/4/5.

Fresh runs refuse existing evidence. --verify rebuilds bytes in memory, reloads
all numerical fixtures, and checks saved MCP cells without making new calls.
"""
import argparse
import asyncio
from dataclasses import asdict
from io import BytesIO
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image
import petz_renderer
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.morphs import evaluate_morphs
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.rotation import _round
from relative_morph_probe import SETTINGS
from research_common import ROOT, SHA, adult, save_result, write_copy

OUT = ROOT/'scratch/research/morph-006'
PUBLIC = ROOT/'experiments/morph-006.json'


def copied_bytes(raw, leaf, sections):
    payload = ('\n'.join('['+k+']\n'+'\n'.join(v) for k, v in sections.items())+'\n').encode('cp1252')
    assert len(payload) <= leaf.size
    return raw[:leaf.offset]+payload.ljust(leaf.size, b' ')+raw[leaf.offset+leaf.size:]


def provenance():
    installed = Path(petz_renderer.__file__).parent
    hashes = {}
    for path in sorted(installed.rglob('*.py')):
        name = path.relative_to(installed).as_posix()
        data = path.read_bytes()
        assert data == (ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes(), name
        hashes[name] = SHA(data)
    revision = subprocess.check_output(['git', '-c', 'safe.directory='+str(ROOT/'petz-renderer-mcp'), '-C', str(ROOT/'petz-renderer-mcp'), 'rev-parse', 'HEAD'], text=True).strip()
    return {'renderer_revision': revision, 'source_hashes': hashes,
            'dependencies': {n: importlib.metadata.version(n) for n in ('petz-renderer-mcp', 'fastmcp', 'Pillow', 'numpy', 'pydantic')},
            'python': sys.version}


def evaluate(version, species, verify=False):
    source, raw, leaf, base, master, _ = adult(species, version)
    layer = load_layer(ResourceFile(raw), master, name=leaf.name, seed=0)
    assert 15 not in {a.add_group for a in layer.appearance.add_balls}
    head = layer.appearance.key_balls.head
    marker = 67+len(layer.appearance.add_balls)
    paths, hashes, checks = {}, {}, []
    for variant, (group, size, relative) in SETTINGS.items():
        sections = dict(base)
        sections['Add Ball'] = (*base['Add Ball'], f'{head}, -36, -80, 0, 125, 244, -1, 0, -1, -1, {size}, 8, {group}, -1, {head if relative else -1}')
        sections['Linez'] = (*layer.sections.get('Linez', ()), f'{head}, {marker}, 0, 125, 244, 244, 25, 25, 0, 1')
        path = OUT/f'{version}-{species}-{variant}{source.suffix}'
        expected = copied_bytes(raw, leaf, sections)
        if verify:
            assert path.read_bytes() == expected
        else:
            assert write_copy(raw, leaf, sections, path) == SHA(expected)
        paths[variant], hashes[variant] = path.name, SHA(expected)
    resolver = ResourceResolver((ROOT/'games'/version, OUT), game_version=version)
    for pose in ('standing', 'sitting', 'lying'):
        assets = {v: load_breed_assets(resolver, p, pose=pose, seed=0, age=100, fatness=50) for v, p in paths.items()}
        static = {v: posed_geometry(a.appearance, a.sizes, a.frame, fatness=50) for v, a in assets.items() if v.startswith('static')}
        for variant in ('group_relative20', 'group_ordinary20'):
            a = assets[variant]
            for amount in (0, 25, 50, 100):
                updates = ((15, amount),)
                m = evaluate_morphs(a.appearance, len(a.frame.balls), updates)
                g = posed_geometry(a.appearance, a.sizes, a.frame, fatness=50, morph_updates=updates)
                relative = variant == 'group_relative20'
                assert m.offsets[-1] == tuple(_round(v*amount*.01) for v in (-36, -80, 0))
                assert m.sizes[-1] == (0 if relative else _round(20*amount*.01))
                assert g[marker].parked == (amount == 0)
                if amount == 0:
                    assert g[marker].radius == 0
                elif relative:
                    assert g[marker].radius == g[head].radius
                if amount == 100:
                    assert g == static['static_relative0' if relative else 'static_ordinary20']
                    if relative:
                        assert g[marker].radius != static['static_relative20'][marker].radius
                checks.append({'pose': pose, 'variant': variant, 'amount': amount,
                    'morph_offset': m.offsets[-1], 'morph_size': m.sizes[-1],
                    'head_radius': g[head].radius, 'marker': asdict(g[marker]),
                    'static_relative20_marker': asdict(static['static_relative20'][marker]),
                    'static_relative0_marker': asdict(static['static_relative0'][marker])})
            ordered = posed_geometry(a.appearance, a.sizes, a.frame, fatness=50, morph_updates=((15,100),(15,0),(15,50)))
            direct = posed_geometry(a.appearance, a.sizes, a.frame, fatness=50, morph_updates=((15,50),))
            assert ordered == direct
    assert SHA(source.read_bytes()) == SHA(raw)
    return {'version': version, 'species': species, 'source': str(source.relative_to(ROOT)),
            'source_sha256': SHA(raw), 'head_id': head, 'marker_id': marker,
            'paths': paths, 'input_hashes': hashes, 'geometry': checks}


def audit_cells(folder, stem, expected, png_digest):
    png = (folder/(stem+'.png')).read_bytes()
    assert SHA(png) == png_digest
    meta = json.loads((folder/(stem+'-render.json')).read_text())
    assert meta['png_sha256'] == png_digest
    with Image.open(BytesIO(png)) as im:
        pixels = im.convert('RGBA')
        # Metadata bounds locate actual image cells independently of padding.
        for cell in meta['cells']:
            x, y = cell['origin']
            crop = pixels.crop((x, y, x+meta['cell_width'], y+meta['cell_height']))
            assert SHA(crop.tobytes()) == cell['pixel_sha256']
    assert (meta['cells'][0]['pixel_sha256'] == meta['cells'][1]['pixel_sha256']) == expected
    return meta


async def main(verify=False):
    current = provenance()
    historical = json.loads((ROOT/'experiments/morph-002.json').read_text())
    if verify:
        report = json.loads(PUBLIC.read_text())
        assert report == json.loads((OUT/'report.json').read_text())
        for key, value in current.items():
            assert report[key] == value, key
    else:
        OUT.mkdir(parents=True, exist_ok=False)
    cases, comparisons, engines = [], [], {}
    for version in ('petz3', 'petz4', 'petz5'):
        engine_records = json.loads((ROOT/'experiments/restore-002.json').read_text())['shared_engine_hashes'][version]
        resolver = ResourceResolver((ROOT/'games'/version,))
        for path, digest in engine_records.items():
            assert SHA(resolver.read_bytes(path, limit=268435456).data) == digest
        engines[version] = engine_records
        for species in ('Dogz', 'Catz'):
            case = evaluate(version, species, verify)
            # Exact old geometry comparisons are deliberately separate from assertions.
            old = next(c for c in historical['cases'] if c['species'] == species)
            normalized = json.loads(json.dumps(case))
            case['historical_petz4_geometry_equal'] = normalized['geometry'] == old['geometry']
            if version == 'petz4':
                assert case['input_hashes'] == old['input_hashes']
            cases.append(case)
            print(version, species, 'historical geometry equal:', case['historical_petz4_geometry_equal'], flush=True)
        if not verify:
            transport = StdioTransport(sys.executable, ['-I','-m','petz_renderer.service.local_mcp', '--game-version', version,
                '--game-root', str(ROOT/'games'/version), '--asset-root', str(OUT)])
            async with Client(transport) as client:
                for case in cases[-2:]:
                    for before, after, expected in (('group_relative20','group_ordinary20',True),('static_relative0','static_relative20',False),('static_relative0','group_relative20',False)):
                        for yaw in (0, 90):
                            args = {'before_path': case['paths'][before], 'after_path': case['paths'][after],
                                    'pose': 'standing', 'seed': 0, 'age': 100, 'fatness': 50, 'yaw_degrees': yaw}
                            stem = f'{version}-{case["species"]}-{before}-{after}-{yaw}'
                            png, meta = await save_result(client, 'compare_appearance', args, OUT, stem)
                            assert meta['game_version'] == version
                            assert (meta['cells'][0]['pixel_sha256'] == meta['cells'][1]['pixel_sha256']) == expected
                            comparisons.append({'version': version, 'species': case['species'], 'stem': stem,
                                'controls': args, 'equal_expected': expected, 'png_sha256': SHA(png),
                                'cell_hashes': [c['pixel_sha256'] for c in meta['cells']]})
    # Normalize tuples as persisted JSON before comparing fresh replay structures.
    cases = json.loads(json.dumps(cases))
    if verify:
        assert cases == report['cases']
        assert engines == report['engine_hashes']
        assert SHA((ROOT/'experiments/morph-002.json').read_bytes()) == report['historical_manifest_sha256']
        for row in report['comparisons']:
            meta = audit_cells(OUT, row['stem'], row['equal_expected'], row['png_sha256'])
            assert [c['pixel_sha256'] for c in meta['cells']] == row['cell_hashes']
            assert meta['game_version'] == row['version']
        print('Verified', len(cases)*24, 'numerical cases and', len(report['comparisons']), 'MCP pairs')
        return
    report = {'experiment': 'MORPH-006', **current,
        'backend': 'direct Python explicit morph percentages; local stdio MCP default state',
        'controls': {'seed': 0, 'age': 100, 'fatness': 50, 'poses': ['standing','sitting','lying'],
                     'morph_percentages': [0,25,50,100], 'mcp_yaw_degrees': [0,90], 'mcp_pose': 'standing'},
        'historical_manifest_sha256': SHA((ROOT/'experiments/morph-002.json').read_bytes()),
        'engine_hashes': engines, 'cases': cases, 'comparisons': comparisons}
    for path in (PUBLIC, OUT/'report.json'):
        path.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    asyncio.run(main(parser.parse_args().verify))
