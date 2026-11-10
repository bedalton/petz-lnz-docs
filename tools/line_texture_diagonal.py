"""LINE-017: diagonal connector crop thresholds and screen-space samples.

Asset-free fixtures only. Expected windows are derived from the plain raster
support, avoiding a second implementation of connector corner rounding.
"""
import importlib.metadata
import json
import sys
from dataclasses import replace
from pathlib import Path
import petz_renderer
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineBlock, LineRenderer
from petz_renderer.rendering.texture import TiledTexture, TexturePaint
from research_common import ROOT, SHA

OUT = ROOT / 'scratch/research/line-017'


def draw(block):
    fb = Framebuffer(80, 80)
    renderer = LineRenderer(seed=1)
    renderer.draw(fb, block)
    return fb, renderer


def support(fb):
    return [(i % fb.width, i // fb.width) for i, value in enumerate(fb.pixels) if value]


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    records, private, reversal = [], [], {}
    for delta in ((7, 7), (11, 4), (4, 11), (-7, 7), (-11, 4), (-4, 11)):
        for thickness in ((3, 3), (3, 7)):
            for reverse in (False, True):
                points = (30, 30, 30 + delta[0], 30 + delta[1])
                widths = thickness
                if reverse:
                    points, widths = points[2:] + points[:2], widths[::-1]
                base = LineBlock(*points, start_thick=widths[0], end_thick=widths[1],
                                 color=125, left_color=-1, right_color=-1, edge_mode=-1)
                plain, _ = draw(base)
                coords = support(plain)
                assert coords
                left, top = min(x for x, y in coords), min(y for x, y in coords)
                width = max(x for x, y in coords) - left + 1
                height = max(y for x, y in coords) - top + 1
                for fuzz in (0, 1, 7):
                    for spare in ((-1, 0), (0, -1), (0, 0), (1, 1), (2, 3)):
                        tw, th = width + fuzz + spare[0], height + spare[1]
                        pixels = bytes(20 + (x + 17 * y) % 220 for y in range(th) for x in range(tw))
                        art = TiledTexture(tw, th, pixels, 0, 0)
                        block = replace(base, fuzz=fuzz, paint=TexturePaint(art, 0, False))
                        fb, renderer = draw(block)
                        flat, flat_renderer = draw(replace(block, paint=None))
                        rejected = min(spare) < 0
                        assert bool(support(fb)) == (not rejected)
                        assert support(flat)
                        samples = []
                        if rejected:
                            assert renderer._state == 1 and not any(renderer._tables)
                        else:
                            assert support(fb) == support(flat)
                            assert renderer._state == flat_renderer._state
                            assert renderer._tables == flat_renderer._tables
                            # Bounding box expands to the left by floor(fuzz/2),
                            # while row shifts still use absolute screen x.
                            window_left = left - fuzz // 2
                            srcx = spare[0] // 2
                            srcy = spare[1] - spare[1] // 2
                            for x, y in support(fb):
                                tx, ty = srcx + x - window_left, srcy + y - top
                                value = pixels[ty * tw + tx]
                                assert fb.get_pixel(x, y) == value
                                samples.append([x, y, tx, ty, value])
                        record = {'delta': delta, 'thickness': thickness, 'reversed': reverse,
                                  'fuzz': fuzz, 'spare': spare, 'plain_bounds': [left, top, width, height],
                                  'texture_size': [tw, th], 'rejected': rejected,
                                  'sample_assertions': len(samples), 'colored_pixels': len(support(fb)),
                                  'indexed_sha256': SHA(fb.pixels), 'plain_indexed_sha256': SHA(flat.pixels),
                                  'rng_after': renderer._state, 'table_lengths': [len(t) for t in renderer._tables]}
                        key = (delta, thickness, fuzz, spare)
                        if not reverse:
                            reversal[key] = fb.pixels
                        else:
                            assert reversal[key] == fb.pixels
                        records.append(record)
                        private.append({'record': record, 'pixels': list(fb.pixels), 'samples': samples})
    installed = Path(petz_renderer.__file__).parent
    sources = {n: SHA((installed / n).read_bytes()) for n in
               ('rendering/lines.py', 'rendering/texture.py', 'rendering/framebuffer.py', 'rendering/rotation.py')}
    for name, digest in sources.items():
        assert SHA((ROOT / 'petz-renderer-mcp/src/petz_renderer' / name).read_bytes()) == digest
    payload = json.dumps(private, separators=(',', ':')).encode()
    (OUT / 'pixels.json').write_bytes(payload)
    report = {'experiment': 'LINE-017', 'backend': 'direct Python indexed raster; asset-free; no MCP',
              'renderer_revision': '9d72d7afd5f7460ef18133c6179caaf8055082d9',
              'python': sys.version, 'dependencies': {'petz-renderer-mcp': importlib.metadata.version('petz-renderer-mcp')},
              'source_hashes': sources, 'private_pixels_sha256': SHA(payload),
              'controls': {'canvas': [80, 80], 'seed': 1, 'edge_mode': -1, 'shade_offset': 0,
                           'has_sign': False, 'texture_period': [0, 0], 'art': '20+(x+17*y)%220'},
              'records': records,
              'summary': {'fixtures': len(records), 'accepted': sum(not r['rejected'] for r in records),
                          'rejected': sum(r['rejected'] for r in records),
                          'sample_assertions': sum(r['sample_assertions'] for r in records),
                          'reversal_pairs': len(reversal)}}
    for target in (OUT / 'report.json', ROOT / 'experiments/line-017.json'):
        target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
