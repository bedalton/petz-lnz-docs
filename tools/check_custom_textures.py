"""Verify CUSTOM-001 saved evidence and exercise the public authoring CLI."""
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image
from research_common import ROOT, SHA
from petz_renderer.formats.bmp import decode_bmp8

OUT = ROOT/'scratch/research/custom-001'
report = json.loads((OUT/'report.json').read_text())
for group in ('originals', 'engine_hashes'):
    for path, digest in report[group].items():
        assert SHA((ROOT/path).read_bytes()) == digest, path
assert SHA((ROOT/'tools/custom_texture_probe.py').read_bytes()) == report['script_sha256']
assert SHA((ROOT/'tools/texture_author.py').read_bytes()) == report['author_tool_sha256']
for path, digest in report['sources'].items():
    assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/path).read_bytes()) == digest
for name, digest in report['png_hashes'].items():
    assert SHA((OUT/name).read_bytes()) == digest, name
for name, info in report['files'].items():
    data = (OUT/info['file']).read_bytes(); bmp = decode_bmp8(data)
    assert SHA(data) == info['sha256']
    assert SHA(bmp.pixels) == info['indices_sha256']
    assert SHA(bytes(v for c in bmp.palette for v in c)) == info['palette_sha256']
assert report['files']['base']['indices_sha256'] == report['files']['table']['indices_sha256']
assert report['files']['base']['palette_sha256'] != report['files']['table']['palette_sha256']
assert len(report['mcp']) == 84
for item in report['mcp']:
    c = item['controls']
    species, variant = Path(c['path']).stem.split('-', 1)
    stem = f'{species}-{variant}-{c["pose"]}-{c["yaw_degrees"]}'
    mcp = Image.open(OUT/f'{stem}-mcp.png').convert('RGBA')
    direct = Image.open(OUT/f'{stem}-direct.png').convert('RGBA')
    assert mcp.size == direct.size and mcp.tobytes() == direct.tobytes()
    assert SHA(mcp.tobytes()) == item['rgba_sha256']
for case in report['cases']:
    for info in case['copies'].values(): assert SHA((OUT/info['file']).read_bytes()) == info['sha256']
    for view in case['views']:
        assert view['direct']['base'] == view['direct']['table']
        for variant in ('indices', 'cw90', 'mirror', 'fur', 'mode1'):
            assert view['direct']['base']['indices_sha256'] != view['direct'][variant]['indices_sha256']

# CLI end-to-end checks use a synthetic, original palette; no game data needed.
with tempfile.TemporaryDirectory(prefix='texture-author-check-', dir=ROOT/'scratch') as temp:
    folder = Path(temp)
    palette = [[i, (i*3)%256, 255-i] for i in range(256)]
    (folder/'palette.json').write_text(json.dumps(palette))
    def run(*args, okay=True):
        p = subprocess.run([sys.executable, str(ROOT/'tools/texture_author.py'), *map(str,args)], capture_output=True, text=True)
        assert (p.returncode == 0) == okay, p.stderr
    run('generate', folder/'base.bmp', '--palette', folder/'palette.json')
    raw = (folder/'base.bmp').read_bytes()
    assert struct.unpack_from('<H', raw, 28)[0] == 8
    assert struct.unpack_from('<I', raw, 30)[0] == 0
    run('generate', folder/'base.bmp', '--palette', folder/'palette.json', okay=False)
    assert (folder/'base.bmp').read_bytes() == raw
    run('orient', folder/'base.bmp', folder/'cw.bmp', '--turns', 1)
    base = decode_bmp8(raw); cw = decode_bmp8((folder/'cw.bmp').read_bytes())
    for y in range(64):
        for x in range(64): assert cw.pixels[x*64+63-y] == base.pixels[y*64+x]
    run('orient', folder/'base.bmp', folder/'shift.bmp', '--shift', 5, -3)
    shifted = decode_bmp8((folder/'shift.bmp').read_bytes())
    for y in range(64):
        for x in range(64):
            assert shifted.pixels[((y-3)%64)*64+(x+5)%64] == base.pixels[y*64+x]
    run('remap', folder/'base.bmp', folder/'remap.bmp', '--map', '{"25":65}')
    remap = decode_bmp8((folder/'remap.bmp').read_bytes())
    assert remap.pixels == bytes(65 if i == 25 else i for i in base.pixels)
    assert remap.palette == base.palette
    alternate = [[255-i, i, i] for i in range(256)]
    (folder/'alternate.json').write_text(json.dumps(alternate))
    run('palette-table', folder/'base.bmp', folder/'table.bmp', '--palette', folder/'alternate.json')
    table = decode_bmp8((folder/'table.bmp').read_bytes())
    assert table.pixels == base.pixels and table.palette != base.palette
    Image.new('RGB', (2, 2), tuple(palette[45])).save(folder/'source.png')
    run('convert', folder/'source.png', folder/'converted.bmp', '--palette', folder/'palette.json')
    assert decode_bmp8((folder/'converted.bmp').read_bytes()).pixels == bytes([45])*4
    Image.new('RGBA', (1, 1), (0,0,0,0)).save(folder/'alpha.png')
    run('convert', folder/'alpha.png', folder/'alpha.bmp', '--palette', folder/'palette.json', okay=False)
    run('generate', folder/'fur.bmp', '--palette', folder/'palette.json', '--pattern', 'fur')
    fur = decode_bmp8((folder/'fur.bmp').read_bytes())
    assert set(fur.pixels) == set(range(10,18))
    run('extract-palette', ROOT/'games/petz4/Petz 4.exe', folder/'extracted.json')
    assert json.loads((folder/'extracted.json').read_text()) == json.loads((OUT/'palette.json').read_text())
verification = {'experiment': 'CUSTOM-001', 'report_sha256': SHA((OUT/'report.json').read_bytes()),
                'checker_sha256': SHA(Path(__file__).read_bytes()), 'mcp_direct_pairs': 84,
                'png_files_checked': len(report['png_hashes']), 'cli_controls': 'pass',
                'original_hashes': 'pass', 'source_hashes': 'pass'}
(OUT/'verification.json').write_text(json.dumps(verification, indent=2)+'\n')
print('PASS: 84 MCP/direct RGBA pairs, saved hashes, originals and authoring CLI controls')
