"""MORPH-007: parsed size-reference boundaries under explicit activation.

Uses immutable in-memory appearance copies; never writes game files. --verify
repeats every geometry/draw assertion and compares saved evidence exactly.
"""
import argparse
from dataclasses import asdict, replace
from io import BytesIO
import json

from PIL import Image
from petz_renderer.appearance.core import read_core
from petz_renderer.appearance.evaluation import fatness_delta
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.morphs import evaluate_morphs
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.rotation import _round
from morph_pixel_probe import draw
from research_common import ROOT, SHA, adult
from revalidate_relative_morph import provenance

OUT = ROOT/'scratch/research/morph-007'
PUBLIC = ROOT/'experiments/morph-007.json'


def clamp(value):
    return min(64, max(0, value))


def appearance_for(assets, reference, prior_dormant, group, size):
    appearance = assets.appearance
    head = appearance.key_balls.head
    first = len(assets.frame.balls)+len(appearance.add_balls)
    assert len(assets.frame.balls) == 67
    assert not ({14,15} & {a.add_group for a in appearance.add_balls})
    assert all(p.start < first and p.end < first for p in appearance.projections)
    refs = {'minus2': -2, 'ordinary': -1, 'real0': 0, 'head': head,
            'previous': first, 'self': first+1, 'forward': first+2, 'outside': 10000}
    rows = (
        f'{head}, -60, -95, 0, 125, 244, -1, 0, -1, -1, 40, 8, {14 if prior_dormant else 0}, -1, -1',
        f'{head}, 0, -140, 0, 125, 244, -1, 0, -1, -1, {size}, 8, {group}, -1, {refs[reference]}',
        f'{head}, 60, -95, 0, 125, 244, -1, 0, -1, -1, 40, 8, 0, -1, -1',
    )
    parsed = read_core({'Add Ball': rows}).add_balls
    assert parsed[1].size_base_ball == refs[reference]
    return replace(appearance, add_balls=appearance.add_balls+parsed), first, refs[reference]


def evaluate(verify=False):
    resolver = ResourceResolver((ROOT/'games/petz4',))
    cases, rasters = [], []
    for species in ('Dogz', 'Catz'):
        source, raw, *_ = adult(species)
        for pose in ('standing', 'sitting', 'lying'):
            assets = load_breed_assets(resolver, str(source.relative_to(ROOT/'games/petz4')),
                                       pose=pose, seed=0, age=100, fatness=50)
            checks = []
            selected = {}
            for dormant in (False, True):
                for reference in ('minus2', 'ordinary', 'real0', 'head', 'previous', 'self', 'forward', 'outside'):
                    for size in (-20, 0, 20):
                        for group in (0, 15):
                            appearance, first, ref = appearance_for(assets, reference, dormant, group, size)
                            for amount in ((100,) if group == 0 else (0, 1, 25, 50, 100)):
                                updates = () if group == 0 else ((15, amount),)
                                morph = evaluate_morphs(appearance, 67, updates)
                                geometry = posed_geometry(appearance, assets.sizes, assets.frame,
                                                          fatness=50, morph_updates=updates)
                                index = first+1
                                msize = size if group == 0 else _round(size*amount*.01) if ref < 0 else 0
                                assert morph.sizes[-2] == msize
                                assert morph.offsets[-2] == tuple(_round(v*amount*.01) for v in (0,-140,0))
                                assert fatness_delta(appearance, index, 50) == 0
                                parked = amount == 0
                                if parked:
                                    expected_radius = 0
                                elif 0 <= ref < index:
                                    expected_radius = clamp((msize*appearance.ball_scale >> 8)+geometry[ref].radius)
                                else:
                                    expected_radius = clamp(msize*appearance.ball_scale >> 9)
                                    if appearance.draw_small_balls and msize > 0 and expected_radius < 1:
                                        expected_radius = 1
                                marker = geometry[index]
                                assert marker.radius == expected_radius
                                assert marker.parked == parked and marker.visible
                                assert geometry[first].parked == dormant
                                checks.append({'reference': reference, 'reference_id': ref, 'prior_dormant': dormant,
                                    'authored_size': size, 'group': group, 'amount': amount,
                                    'morph_size': msize, 'marker': asdict(marker),
                                    'prior_radius': geometry[first].radius, 'expected_radius': expected_radius})
                                # Active-target pixel controls: host-relative zero size, prior-ref and unresolved refs.
                                if size == 20 and group == 15 and amount == 100 and reference in ('head','previous','self','forward','outside','ordinary'):
                                    name = f'{"dormant" if dormant else "active"}-{reference}'
                                    p = prepare_frame(appearance, assets.sizes, assets.frame, textures=assets.textures,
                                                      fatness=50, morph_updates=updates)
                                    selected[name] = (replace(assets, appearance=appearance), p)
            # Common bounds for every selected scene; retain image positions across reference changes.
            boxes = [p.geometry.ordering.bounds for _,p in selected.values()]
            bounds = replace(boxes[0], min_x=min(b.min_x for b in boxes), min_y=min(b.min_y for b in boxes),
                             max_x=max(b.max_x for b in boxes), max_y=max(b.max_y for b in boxes))
            images, records = {}, []
            for name, (a,p) in selected.items():
                fb, _, png = draw(a, p, bounds)
                filename = f'{species}-{pose}-{name}.png'
                path = OUT/filename
                if verify:
                    assert path.read_bytes() == png
                else:
                    path.write_bytes(png)
                im = Image.open(BytesIO(png)).convert('RGBA')
                images[name] = im
                records.append({'name': name, 'png': filename, 'png_sha256': SHA(png),
                    'rgba_sha256': SHA(im.tobytes()), 'indexed_sha256': SHA(fb.pixels),
                    'width': fb.width, 'height': fb.height})
            # Self/forward/outside all leave an active, visible, zero-radius probe in these controls.
            for prior in ('active', 'dormant'):
                assert images[prior+'-self'].tobytes() == images[prior+'-forward'].tobytes() == images[prior+'-outside'].tobytes()
            rasters.append({'species': species, 'pose': pose, 'bounds': asdict(bounds), 'records': records})
            cases.append({'species': species, 'pose': pose, 'source': str(source.relative_to(ROOT)),
                          'source_sha256': SHA(raw), 'checks': checks})
            assert source.read_bytes() == raw
            print(species, pose, len(checks), 'checks,', len(records), 'rasters', flush=True)
    return cases, rasters


def main(verify=False):
    if not verify:
        OUT.mkdir(parents=True, exist_ok=False)
    cases, rasters = evaluate(verify)
    prior = ROOT/'experiments/morph-006.json'
    report = {'experiment': 'MORPH-007', **provenance(),
        'backend': 'direct Python immutable appearance copies; parsed synthetic Add Ball rows; no new MCP calls',
        'controls': {'game_version': 'petz4', 'seed': 0, 'age': 100, 'fatness': 50, 'yaw': 0,
            'poses': ['standing','sitting','lying'], 'sizes': [-20,0,20], 'target_groups': [0,15],
            'active_group15_percentages': [0,1,25,50,100], 'prior_group': '0 or dormant14',
            'raster_seed': 1, 'line_rng_seed': 1, 'step': 0, 'state': 'fresh each draw'},
        'baseline_manifest_sha256': SHA(prior.read_bytes()), 'baseline_links': 'MORPH-006 default-state controls only',
        'cases': cases, 'rasters': rasters,
        'summary': {'numerical_cases': sum(len(c['checks']) for c in cases),
                    'pngs': sum(len(r['records']) for r in rasters)}}
    report = json.loads(json.dumps(report))
    if verify:
        assert report == json.loads(PUBLIC.read_text()) == json.loads((OUT/'report.json').read_text())
        print('Full replay verified:', report['summary'])
    else:
        for path in (PUBLIC, OUT/'report.json'):
            path.write_text(json.dumps(report, indent=2)+'\n')
        print(report['summary'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    main(parser.parse_args().verify)
