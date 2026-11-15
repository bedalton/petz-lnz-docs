"""Index-preserving texture authoring. All outputs refuse existing paths.

Requires Pillow. Palette extraction additionally requires the local renderer.
No game palette or artwork is bundled. See visual-editing/custom-textures.md.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


def palette(path):
    path = Path(path)
    if path.suffix.lower() == '.json':
        colors = json.loads(path.read_text())
        if (not isinstance(colors, list) or len(colors) != 256
                or any(not isinstance(c, list) or len(c) != 3
                       or any(type(v) is not int or not 0 <= v <= 255 for v in c)
                       for c in colors)):
            raise ValueError('palette JSON must contain 256 RGB integer triples')
        return [v for c in colors for v in c]
    image = indexed(path)
    return image.getpalette()[:768]


def indexed(path):
    with Image.open(path) as source:
        if source.mode != 'P' or len(source.getpalette() or []) != 768:
            raise ValueError('requires indexed image with a full 256-entry RGB palette')
        return source.copy()


def save(image, output):
    output = Path(output)
    if output.suffix.lower() != '.bmp':
        raise ValueError('texture output must end in .bmp')
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('xb') as stream:
        image.save(stream, format='BMP', bits=8)


def diagnostic(colors):
    """Original 64px tile: local axes, unequal corners and repeated bands."""
    image = Image.new('P', (64, 64), 15)
    image.putpalette(colors)
    draw = ImageDraw.Draw(image)
    for y in range(64):
        for x in range(64):
            image.putpixel((x, y), 10 + ((x // 8 + 3 * (y // 8)) % 14) * 10 + 5)
    draw.rectangle((0, 0, 7, 7), fill=25)
    draw.rectangle((52, 0, 63, 11), fill=65)
    draw.rectangle((0, 48, 15, 63), fill=105)
    draw.rectangle((44, 44, 63, 63), fill=135)
    # +u points right; +v points down in bitmap coordinates.
    draw.line((24, 32, 43, 32), fill=9, width=2)
    draw.polygon(((43, 32), (38, 28), (38, 36)), fill=9)
    draw.line((32, 24, 32, 43), fill=9, width=2)
    draw.polygon(((32, 43), (28, 38), (36, 38)), fill=9)
    draw.text((44, 27), 'U', fill=9)
    draw.text((28, 45), 'V', fill=9)
    return image


def convert_rgb(source, colors, allowed):
    """Nearest encoded-RGB distance, no dithering; ties choose lowest index."""
    rgba = source.convert('RGBA')
    if rgba.getextrema()[3] != (255, 255):
        raise ValueError('flatten transparency explicitly before conversion')
    allowed = sorted(set(allowed))
    if not allowed or any(not 0 <= i <= 255 for i in allowed):
        raise ValueError('allowed indices must lie in 0..255')
    triples = [tuple(colors[i:i + 3]) for i in range(0, 768, 3)]
    rgb = rgba.convert('RGB')
    raw = rgb.tobytes()
    pixels = [tuple(raw[i:i+3]) for i in range(0, len(raw), 3)]
    mapping = {c: min(allowed, key=lambda i: sum((a-b)**2 for a, b in zip(c, triples[i])))
               for c in set(pixels)}
    image = Image.frombytes('P', rgb.size, bytes(mapping[c] for c in pixels))
    image.putpalette(colors)
    return image


def orient(image, turns=0, mirror=False, shift=(0, 0)):
    for _ in range(turns % 4):
        image = image.transpose(Image.Transpose.ROTATE_270)
    if mirror:
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return ImageChops.offset(image, *shift)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    extract = sub.add_parser('extract-palette')
    extract.add_argument('executable')
    extract.add_argument('output')
    generate = sub.add_parser('generate')
    generate.add_argument('output')
    generate.add_argument('--palette', required=True)
    generate.add_argument('--pattern', choices=('diagnostic', 'fur'), default='diagnostic')
    table = sub.add_parser('palette-table')
    table.add_argument('input'); table.add_argument('output')
    table.add_argument('--palette', required=True)
    remap = sub.add_parser('remap')
    remap.add_argument('input'); remap.add_argument('output')
    remap.add_argument('--map', required=True, help='JSON object of old index to new index')
    convert = sub.add_parser('convert')
    convert.add_argument('input'); convert.add_argument('output')
    convert.add_argument('--palette', required=True)
    convert.add_argument('--indices', default='10:150', help='half-open index range; default 10:150')
    transform = sub.add_parser('orient')
    transform.add_argument('input'); transform.add_argument('output')
    transform.add_argument('--turns', type=int, default=0, help='clockwise quarter turns')
    transform.add_argument('--mirror', action='store_true', help='horizontal AFTER rotation')
    transform.add_argument('--shift', type=int, nargs=2, default=(0, 0), metavar=('X', 'Y'))
    args = parser.parse_args()
    if args.command == 'extract-palette':
        from petz_renderer.formats.bmp import decode_palette
        from petz_renderer.formats.pe import ResourceFile
        colors = decode_palette(ResourceFile(Path(args.executable).read_bytes()).read('BMP', 'PALETTE'))
        with Path(args.output).open('x') as stream:
            json.dump(colors, stream); stream.write('\n')
        return
    if args.command == 'generate':
        colors = palette(args.palette)
        image = diagnostic(colors)
        if args.pattern == 'fur':
            # Original periodic strokes; edge neighbors continue across the seam.
            image = Image.frombytes('P', (64, 64), bytes(
                10 + ((x + 2*y) % 8) for y in range(64) for x in range(64)))
            image.putpalette(colors)
    elif args.command == 'convert':
        start, stop = map(int, args.indices.split(':'))
        with Image.open(args.input) as source:
            image = convert_rgb(source, palette(args.palette), range(start, stop))
    else:
        image = indexed(args.input)
        if args.command == 'palette-table':
            image.putpalette(palette(args.palette))
        elif args.command == 'remap':
            table = list(range(256))
            for old, new in json.loads(args.map).items():
                old = int(old)
                if not 0 <= old <= 255 or type(new) is not int or not 0 <= new <= 255:
                    raise ValueError('map indices must lie in 0..255')
                table[old] = new
            image = Image.frombytes('P', image.size, image.tobytes().translate(bytes(table)))
            image.putpalette(indexed(args.input).getpalette())
        else:
            image = orient(image, args.turns, args.mirror, tuple(args.shift))
    save(image, args.output)


if __name__ == '__main__':
    main()
