"""LINE-018: viewport-clamped connector texture windows, asset-free."""
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

OUT = ROOT / 'scratch/research/line-018'
CANVAS = 24
CASES = {
    'horizontal_both': (-20, 12, 44, 12),
    'vertical_both': (12, -20, 12, 44),
    'diagonal_both': (-20, -10, 44, 34),
    'diagonal_left': (-20, 3, 20, 20),
    'diagonal_top': (3, -20, 20, 20),
    'diagonal_right': (3, 3, 44, 20),
    'diagonal_bottom': (3, 3, 20, 44),
    'outside_left': (-20, 3, -10, 20),
    'outside_right': (34, 3, 44, 20),
    'outside_top': (3, -20, 20, -10),
    'outside_bottom': (3, 34, 20, 44),
    'inside': (3, 3, 20, 20),
}


def draw(block, size=CANVAS):
    fb, renderer = Framebuffer(size, size), LineRenderer(seed=1)
    renderer.draw(fb, block)
    return fb, renderer


def support(fb):
    return [(i % fb.width, i // fb.width) for i, value in enumerate(fb.pixels) if value]


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    records, private = [], []
    for name, points in CASES.items():
        base = LineBlock(*points, start_thick=3, end_thick=3, color=125,
                         left_color=-1, right_color=-1, edge_mode=-1)
        flat0, _ = draw(base)
        coords = support(flat0)
        assert coords
        left, top = min(x for x, y in coords), min(y for x, y in coords)
        width = max(x for x, y in coords) - left + 1
        height = max(y for x, y in coords) - top + 1
        # Oversized framebuffer translates the same geometry away from every edge.
        shift = 40
        large = replace(base, x1=base.x1+shift, x2=base.x2+shift,
                        y1=base.y1+shift, y2=base.y2+shift)
        full, _ = draw(large, 120)
        cropped = bytes(full.get_pixel(x+shift, y+shift) for y in range(CANVAS) for x in range(CANVAS))
        fullcoords = support(full)
        fullsize = [max(x for x,y in fullcoords)-min(x for x,y in fullcoords)+1,
                    max(y for x,y in fullcoords)-min(y for x,y in fullcoords)+1]
        crop_delta = sum(a != b for a,b in zip(flat0.pixels, cropped))
        for fuzz in (0, 1, 7):
            # For fuzz>0, corner clamps reserve margins, shrinking the polygon.
            # Measure that polygon using a large untextured probe? Instead use
            # fixed 24x24 and 23x23 tiles plus a roomy control, and inspect guards.
            for tilesize in (8, 23, 24, 32, 80):
                pixels = bytes(20+(x+17*y)%220 for y in range(tilesize) for x in range(tilesize))
                art = TiledTexture(tilesize, tilesize, pixels, 0, 0)
                block = replace(base, fuzz=fuzz, paint=TexturePaint(art, 0, False))
                fb, renderer = draw(block)
                flat, flat_renderer = draw(replace(block, paint=None))
                rejected = not any(fb.pixels)
                if fuzz == 0:
                    assert rejected == (width > tilesize or height > tilesize)
                if tilesize >= CANVAS:
                    assert not rejected
                if rejected:
                    assert renderer._state == 1 and not any(renderer._tables)
                else:
                    assert support(fb) == support(flat)
                    assert renderer._state == flat_renderer._state and renderer._tables == flat_renderer._tables
                samples = []
                if not rejected and fuzz == 0:
                    srcx = (tilesize-width)//2
                    srcy = tilesize-height-(tilesize-height)//2
                    for x,y in support(fb):
                        tx,ty = srcx+x-left,srcy+y-top
                        value = pixels[ty*tilesize+tx]
                        assert fb.get_pixel(x,y) == value
                        samples.append([x,y,tx,ty,value])
                record = {'case': name, 'endpoints': points, 'fuzz': fuzz, 'tile_size': tilesize,
                          'plain_bounds_fuzz0': [left,top,width,height], 'unclamped_size_fuzz0': fullsize,
                          'plain_clamp_vs_crop_pixels_fuzz0': crop_delta,
                          'rejected': rejected, 'colored_pixels': len(support(fb)),
                          'sample_assertions': len(samples), 'rng_after': renderer._state,
                          'table_lengths': [len(t) for t in renderer._tables],
                          'indexed_sha256': SHA(fb.pixels), 'plain_indexed_sha256': SHA(flat.pixels)}
                records.append(record)
                private.append({'record':record, 'pixels':list(fb.pixels), 'samples':samples,
                                'plain_pixels':list(flat.pixels), 'unclamped_crop_pixels_fuzz0':list(cropped)})
    installed = Path(petz_renderer.__file__).parent
    sources = {n: SHA((installed/n).read_bytes()) for n in
               ('rendering/lines.py','rendering/texture.py','rendering/framebuffer.py','rendering/rotation.py')}
    for name,digest in sources.items():
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    payload = json.dumps(private,separators=(',',':')).encode()
    (OUT/'pixels.json').write_bytes(payload)
    report = {'experiment':'LINE-018','backend':'asset-free direct indexed raster; no MCP',
              'renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9',
              'python':sys.version,'dependencies':{'petz-renderer-mcp':importlib.metadata.version('petz-renderer-mcp')},
              'source_hashes':sources,'private_pixels_sha256':SHA(payload),
              'controls':{'canvas':[24,24],'seed':1,'widths':[3,3],'shade_offset':0,'has_sign':False,
                          'edge_mode':-1,'texture_period':[0,0],'art':'20+(x+17*y)%220',
                          'unclamped_canvas':[120,120],'unclamped_translation':[40,40]},
              'records':records,
              'summary':{'fixtures':len(records),'accepted':sum(not r['rejected'] for r in records),
                         'rejected':sum(r['rejected'] for r in records),
                         'sample_assertions':sum(r['sample_assertions'] for r in records),
                         'clamp_differs_from_crop_cases':len({r['case'] for r in records if r['plain_clamp_vs_crop_pixels_fuzz0']})}}
    for target in (OUT/'report.json',ROOT/'experiments/line-018.json'):
        target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']))
    print(json.dumps({r['case']:r['plain_clamp_vs_crop_pixels_fuzz0'] for r in records}))


if __name__ == '__main__':
    main()
