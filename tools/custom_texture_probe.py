"""CUSTOM-001: generated BMP palette/index controls and multi-view orientation.

Run with scratch/petz-local-x86-venv/bin/python. Refuses existing output.
Private fixed-span research copies only; not a distributable breed writer.
"""
import asyncio
import importlib.metadata
import io
import json
import subprocess
import sys
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image, ImageDraw
import petz_renderer
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.bmp import decode_bmp8, decode_palette
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.output import render_portrait
from petz_renderer.rendering.texture import sample_window, tile_texture
from research_common import ROOT, SHA, adult, write_copy, save_result
from texture_author import diagnostic, save, orient, convert_rgb

OUT = ROOT/'scratch/research/custom-001'
VIEWS = [('standing', y) for y in (0, 90, 180, 270)] + [('sitting', 0), ('lying', 90)]


def embed(raw, name, bmp):
    pe = ResourceFile(raw)
    leaf = next(r for r in pe.resources if r.type == 'BMP' and r.name == name)
    assert len(bmp) <= leaf.size
    result = raw[:leaf.offset] + bmp.ljust(leaf.size, b'\0') + raw[leaf.offset+leaf.size:]
    after = ResourceFile(result)
    assert pe.resources == after.resources
    for r in pe.resources:
        if r != leaf:
            assert pe.read(r.type, r.name, r.language) == after.read(r.type, r.name, r.language)
    assert raw[:leaf.offset] == result[:leaf.offset]
    assert raw[leaf.offset+leaf.size:] == result[leaf.offset+leaf.size:]
    return result


async def main():
    OUT.mkdir(parents=True, exist_ok=False)
    exe = ROOT/'games/petz4/Petz 4.exe'
    colors = decode_palette(ResourceFile(exe.read_bytes()).read('BMP', 'PALETTE'))
    flat = [v for rgb in colors for v in rgb]
    (OUT/'palette.json').write_text(json.dumps(colors)+'\n')
    image = diagnostic(flat)
    swapped = image.copy(); swapped.putpalette([255-v for v in flat])
    recolored = Image.frombytes('P', image.size, image.tobytes().translate(bytes(
        10 + ((i-10+40) % 140) if 10 <= i < 150 else i for i in range(256))))
    recolored.putpalette(flat)
    fur = Image.frombytes('P', (64, 64), bytes(10+(x+2*y)%8 for y in range(64) for x in range(64)))
    fur.putpalette(flat)
    images = {'base': image, 'table': swapped, 'indices': recolored,
              'cw90': orient(image, 1), 'mirror': orient(image, mirror=True), 'fur': fur}
    files = {}
    for name, im in images.items():
        path = OUT/f'{name}.bmp'; save(im, path)
        bmp = decode_bmp8(path.read_bytes())
        assert bmp.pixels == im.tobytes() and (bmp.width, bmp.height) == im.size
        files[name] = {'file': path.name, 'sha256': SHA(path.read_bytes()),
                       'indices_sha256': SHA(bmp.pixels), 'palette_sha256': SHA(bytes(v for c in bmp.palette for v in c))}
    # Exact transform controls, independent pixel-coordinate checks.
    assert orient(image, 4).tobytes() == image.tobytes()
    assert orient(orient(image, mirror=True), mirror=True).tobytes() == image.tobytes()
    for y in range(64):
        for x in range(64):
            assert images['cw90'].getpixel((63-y, x)) == image.getpixel((x, y))
            assert images['mirror'].getpixel((63-x, y)) == image.getpixel((x, y))
    # Nearest-color conversion and duplicate-color index policy.
    synthetic = [0]*768; synthetic[30:33] = [100, 20, 30]; synthetic[33:36] = [100, 20, 30]
    assert convert_rgb(Image.new('RGB', (1, 1), (100, 20, 30)), synthetic, [11, 10]).tobytes() == b'\x0a'
    try:
        convert_rgb(Image.new('RGBA', (1, 1), (0, 0, 0, 0)), flat, range(10, 150))
    except ValueError:
        pass
    else:
        raise AssertionError('transparent RGB conversion should be explicit')
    # Sample-window angles move a crop, not a degree-based image rotation.
    texture = tile_texture(decode_bmp8((OUT/'base.bmp').read_bytes()), 256, 256)
    windows = []
    for angles in (None, (0, 0), (64, 0), (0, 64), (-64, 0)):
        w = sample_window(texture, 32, 64, angles)
        windows.append({'angles': angles, 'start': [w.start_x, w.start_y]})
    assert [w['start'] for w in windows] == [[112,112],[112,112],[128,112],[112,128],[96,112]]
    cases = []; originals = {}
    for species in ('Dogz', 'Catz'):
        source, raw, leaf, sections, master, _ = adult(species)
        originals[str(source.relative_to(ROOT))] = SHA(raw)
        layer = load_layer(ResourceFile(raw), master, name=leaf.name, seed=0)
        app = layer.appearance; head = app.key_balls.head
        name = 'CHIP' if species == 'Dogz' else 'SOPHISTO'
        slot = len(app.textures); marker = 67+len(app.add_balls)
        assert all(t.own_level == -1 for t in app.textures)
        stock = tuple(f'{t.path}, {int(t.has_levels)}, {t.tile_width}, {t.tile_height}' for t in app.textures)
        paths = {}
        for variant in (*images, 'mode1', 'external'):
            edited = dict(sections)
            art = 'CUSTOM_DIAG' if variant == 'external' else name
            edited['Texture List'] = (*stock, f'\\art\\textures\\{art}.bmp, {1 if variant in ("mode1", "fur") else 0}, 256, 256')
            edited['Add Ball'] = (*sections['Add Ball'], f'{head}, -35, -160, 0, 125, 244, -1, 0, -1, -1, 60, 0, 0, {slot}, -1')
            path = OUT/f'{species}-{variant}{source.suffix}'
            write_copy(raw, leaf, edited, path)
            if variant != 'external':
                bmp = (OUT/f'{"base" if variant == "mode1" else variant}.bmp').read_bytes()
                path.write_bytes(embed(path.read_bytes(), name, bmp))
            paths[variant] = path
        # Explicit loose BMP exists but the current loader searches PE resources.
        external = OUT/'art/textures/CUSTOM_DIAG.bmp'
        external.parent.mkdir(parents=True, exist_ok=True); external.write_bytes((OUT/'base.bmp').read_bytes())
        resolver = ResourceResolver((ROOT/'games/petz4', OUT))
        try:
            load_breed_assets(resolver, paths['external'].name, pose='standing', seed=0, age=100, fatness=50)
        except ValueError as exc:
            assert 'missing BMP/CUSTOM_DIAG' in str(exc)
            error = str(exc)
        else:
            raise AssertionError('unexpected loose BMP support')
        case = {'species': species, 'head': head, 'marker': marker, 'slot': slot,
                'resource': name, 'external_error': error,
                'copies': {v: {'file': p.name, 'sha256': SHA(p.read_bytes())} for v,p in paths.items()}, 'views': []}
        for pose, yaw in VIEWS:
            outputs = {}
            for variant in (*images, 'mode1'):
                assets = load_breed_assets(resolver, paths[variant].name, pose=pose, seed=0, age=100, fatness=50)
                assert assets.appearance.textures[:slot] == app.textures
                expected_bmp = decode_bmp8((OUT/f'{"base" if variant == "mode1" else variant}.bmp').read_bytes())
                assert assets.textures[slot].pixels == tile_texture(expected_bmp, 256, 256).pixels
                portrait = render_portrait(assets, yaw=yaw * 256 // 360)
                stem = f'{species}-{variant}-{pose}-{yaw}'
                (OUT/f'{stem}-direct.png').write_bytes(portrait.png)
                outputs[variant] = {'indices_sha256': SHA(portrait.indices), 'png_sha256': SHA(portrait.png)}
            assert outputs['base'] == outputs['table']
            for variant in ('indices', 'cw90', 'mirror', 'fur', 'mode1'):
                assert outputs['base']['indices_sha256'] != outputs[variant]['indices_sha256']
            case['views'].append({'pose': pose, 'yaw': yaw, 'direct': outputs})
        cases.append(case)
    transport = StdioTransport(sys.executable, ['-I', '-m', 'petz_renderer.service.local_mcp', '--game-version', 'petz4', '--game-root', str(ROOT/'games/petz4'), '--asset-root', str(OUT)])
    mcp = []
    async with Client(transport) as client:
        for case in cases:
            for view in case['views']:
                for variant in (*images, 'mode1'):
                    stem = f'{case["species"]}-{variant}-{view["pose"]}-{view["yaw"]}'
                    args = {'path': case['copies'][variant]['file'], 'pose': view['pose'], 'yaw_degrees': view['yaw'], 'seed': 0, 'age': 100, 'fatness': 50}
                    png, meta = await save_result(client, 'render_pet', args, OUT, stem+'-mcp')
                    a = Image.open(io.BytesIO(png)).convert('RGBA')
                    b = Image.open(OUT/f'{stem}-direct.png').convert('RGBA')
                    assert a.size == b.size and a.tobytes() == b.tobytes()
                    mcp.append({'controls': args, 'png_sha256': SHA(png), 'rgba_sha256': SHA(a.tobytes()), 'metadata': meta})
            print(case['species'], 'MCP controls pass', flush=True)
    for p,h in originals.items(): assert SHA((ROOT/p).read_bytes()) == h
    # Compact view sheet: each variant has front, side, back, opposite side.
    rows = []
    for case in cases:
        for variant in (*images, 'mode1'):
            rows.append((case['species'], variant))
    sheet = Image.new('RGB', (1000, len(rows)*220), '#dddddd'); draw = ImageDraw.Draw(sheet)
    for row,(species,variant) in enumerate(rows):
        draw.text((2,row*220+2), f'{species} {variant}', fill='black')
        for col,yaw in enumerate((0,90,180,270)):
            im = Image.open(OUT/f'{species}-{variant}-standing-{yaw}-direct.png').convert('RGBA')
            sheet.paste(im, (col*250,row*220+20), im)
    sheet.save(OUT/'orientation-sheet.png')
    package = Path(petz_renderer.__file__).parent
    sources = {str(p.relative_to(package)): SHA(p.read_bytes()) for p in package.rglob('*.py')}
    for p,h in sources.items(): assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes()) == h
    report = {'experiment': 'CUSTOM-001', 'backend': 'local stdio MCP and direct Python',
              'revision': subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip(),
              'python': sys.version, 'dependencies': {p: importlib.metadata.version(p) for p in ('petz-renderer-mcp','pillow','fastmcp','pefile')},
              'originals': originals, 'engine_hashes': {str(p.relative_to(ROOT)): SHA(p.read_bytes()) for p in (exe, *sorted((ROOT/'games/petz4/Resource').glob('* 4 Rez.dll')))},
              'sources': sources, 'script_sha256': SHA(Path(__file__).read_bytes()), 'author_tool_sha256': SHA((ROOT/'tools/texture_author.py').read_bytes()),
              'files': files, 'windows': windows, 'cases': cases, 'mcp': mcp,
              'png_hashes': {p.name: SHA(p.read_bytes()) for p in OUT.glob('*.png')}}
    (OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print('PASS', len(mcp), 'MCP/direct matches;', len(report['png_hashes']), 'private PNGs')


if __name__ == '__main__':
    asyncio.run(main())
