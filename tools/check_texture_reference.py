"""Reproduce code-supported LNZ texture orientation reference controls; no renders."""
import hashlib
import inspect
import json
from dataclasses import asdict
from pathlib import Path

from petz_renderer.appearance.core import read_core
from petz_renderer.appearance.lnz import parse_sections
from petz_renderer.formats.animation import BallPosition
from petz_renderer.rendering.texture import TiledTexture, sample_window
from petz_renderer.rendering.texture_rotation import TextureOrientation, update_texture_orientation

ROOT = Path(__file__).resolve().parents[1]

def read(text):
    return read_core(parse_sections(text.encode()))

cases = [('', []), ('42\n', [42]), ('42 90 180\n', [42]),
         ('42\n43\n', [42, 43]), ('-1\n', list(range(512))),
         ('42\n-1\n', [42]), ('512\n-1\n2\n', [2]),
         ('bad\n-1\n', list(range(512)))]
controls = []
for rows, expected in cases:
    a = read('[No Texture Rotate]\n' + rows)
    actual = [i for i, enabled in enumerate(a.texture_rotates) if not enabled]
    assert actual == expected
    controls.append(dict(rows=rows, disabled=actual))
base = read('[Texture List]\n\\art\\textures\\hair10.bmp 1 256 256\n')
extra = read('[Texture List]\n\\art\\textures\\hair10.bmp 1 256 256 90 180\n')
assert base.textures == extra.textures
orientation = TextureOrientation()
assert orientation.angles == (0, 0)
position = BallPosition(0, 0, 0, 0, 0, 0)
yawed = update_texture_orientation(orientation, position, yaw=64)
assert yawed.angles != orientation.angles
texture = TiledTexture(256, 256, bytes(256*256), 128, 128)
w0 = sample_window(texture, 32, 32)
w1 = sample_window(texture, 32, 32, (64, 0))
assert w1.start_x - w0.start_x == 16 and w1.start_y == w0.start_y
sources = []
for obj in (read_core, parse_sections, sample_window, update_texture_orientation):
    installed = Path(inspect.getsourcefile(obj))
    relative = installed.parts[installed.parts.index('petz_renderer'):]
    checkout = ROOT / 'petz-renderer-mcp/src' / Path(*relative)
    assert checkout.read_bytes() == installed.read_bytes(), str(checkout)
    sources.append(dict(path=str(Path(*relative)), sha256=hashlib.sha256(installed.read_bytes()).hexdigest()))
report = dict(scope='Synthetic parser/arithmetic controls; no rendering or native-game validation',
              sources=sources, no_rotate_controls=controls,
              extra_texture_columns_ignored=True, initial_orientation=asdict(orientation),
              yaw64_orientation=asdict(yawed), sample_windows=[asdict(w0), asdict(w1)])
out = ROOT / 'scratch/research/texture-reference/verification.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2)+'\n')
print('Passed 8 section controls, extra-column comparison, fresh/yaw orientation and 16px window shift; 4 installed source files match checkout.')
