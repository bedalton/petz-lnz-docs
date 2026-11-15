"""Audit local texture metadata/previews or search candidates. Requires Pillow for audit."""
import argparse
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def audit(root, rows):
    from PIL import Image, __version__ as pillow_version
    errors, records = [], []
    names = [r['filename'] for r in rows]
    if len(set(n.casefold() for n in names)) != len(names):
        errors.append('duplicate/case-colliding catalog filenames')
    visual_index = (root / 'INDEX.md').read_text()
    for row in rows:
        expected = f"**`{row['filename']}`** | {row['subcategory']} | `{row['width']}x{row['height']}` | {row['description']} | {row['usage']} |"
        if visual_index.count(expected) != 1:
            errors.append(f"{row['filename']}: visual table differs from JSON")
    disk_names = {p.name for p in root.glob('*.bmp')}
    if disk_names != set(names):
        errors.append(f'BMP coverage differs: {sorted(disk_names ^ set(names))}')
    for row in rows:
        name = row['filename']
        if any(Path(row[k]).name != row[k] for k in ('filename', 'png_file')):
            errors.append(f'{name}: paths must be basenames')
            continue
        try:
            bmp, png = root / name, root / row['png_file']
            with Image.open(bmp) as art, Image.open(png) as preview:
                art.load(); preview.load()
                if art.mode != 'P':
                    errors.append(f'{name}: expected indexed BMP, got {art.mode}')
                if art.size != (row['width'], row['height']):
                    errors.append(f'{name}: metadata dimensions differ')
                rgba = preview.convert('RGBA')
                if preview.size != art.size or art.convert('RGB').tobytes() != rgba.convert('RGB').tobytes():
                    errors.append(f'{name}: preview RGB differs')
                if rgba.getchannel('A').getextrema() != (255, 255):
                    errors.append(f'{name}: preview has unexpected alpha')
                counts = collections.Counter(art.tobytes())
                size_prefix = f'{art.width}x{art.height}:'.encode()
                records.append(dict(filename=name, bmp_sha256=digest(bmp.read_bytes()),
                    png_sha256=digest(png.read_bytes()), source_mode=art.mode,
                    width=art.width, height=art.height,
                    indexed_pixels_sha256=digest(size_prefix + art.tobytes()),
                    rgb_pixels_sha256=digest(size_prefix + art.convert('RGB').tobytes()),
                    palette_sha256=digest(bytes(art.getpalette() or [])),
                    used_indices=sorted(counts), unique_indices=len(counts),
                    index_253_pixels=counts.get(253, 0), preview_is_opaque=True))
        except (OSError, ValueError) as exc:
            errors.append(f'{name}: {exc}')
    if errors:
        raise SystemExit('\n'.join(errors))
    groups = {}
    for field in ('bmp_sha256', 'indexed_pixels_sha256', 'rgb_pixels_sha256'):
        buckets = collections.defaultdict(list)
        for record in records:
            buckets[record[field]].append(record['filename'])
        groups[field] = sorted(sorted(g) for g in buckets.values() if len(g) > 1)
    return dict(schema_version=1, scope='Local file verification only; provenance, resource availability and game behavior unvalidated.',
        pillow_version=pillow_version, index_sha256=digest((root / 'index.json').read_bytes()),
        entry_count=len(rows), bmp_count=len(disk_names),
        categories=dict(sorted(collections.Counter(r['category'] for r in rows).items())),
        duplicate_groups=groups, records=records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT / 'texture-index')
    sub = parser.add_subparsers(dest='command', required=True)
    search = sub.add_parser('search', help='All query words must match; returns candidate metadata as JSON')
    search.add_argument('query', nargs='*')
    search.add_argument('--category', help='Case-insensitive category substring')
    search.add_argument('--limit', type=int, default=20)
    check = sub.add_parser('audit', help='Validate BMP coverage, dimensions and exact opaque RGB previews')
    output = check.add_mutually_exclusive_group()
    output.add_argument('--write', type=Path, help='Write reproducible report')
    output.add_argument('--check', type=Path, help='Compare with retained report')
    args = parser.parse_args()
    rows = json.loads((args.root / 'index.json').read_text())
    if args.command == 'search':
        terms = [q.casefold() for q in args.query]
        matches = [r for r in rows if all(t in json.dumps(r, ensure_ascii=False).casefold() for t in terms)
                   and (not args.category or args.category.casefold() in r['category'].casefold())]
        print(json.dumps(dict(total=len(matches), entries=matches[:max(0, args.limit)]), indent=2))
    else:
        report = audit(args.root, rows)
        if args.check and json.loads(args.check.read_text()) != report:
            raise SystemExit('Audit differs from retained report; inspect changed inputs/tool version.')
        if args.write:
            args.write.write_text(json.dumps(report, indent=2) + '\n')
        print(f"Verified {report['entry_count']} entries: BMP coverage, dimensions, indexed sources and exact opaque RGB previews.")


if __name__ == '__main__':
    main()
