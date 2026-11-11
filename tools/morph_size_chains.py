"""MORPH-008: remapped size-reference chains/cycles and row order."""
import argparse
from dataclasses import asdict, replace
from itertools import permutations
import json

from petz_renderer.appearance.core import read_core
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.morphs import evaluate_morphs
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.rotation import _round
from morph_pixel_probe import draw
from research_common import ROOT, SHA, adult
from revalidate_relative_morph import provenance

OUT = ROOT/'scratch/research/morph-008'
PUBLIC = ROOT/'experiments/morph-008.json'
SIZES = {'A':20, 'B':-8, 'C':10}
OFFSETS = {'A':(-60,-140,0), 'B':(0,-140,0), 'C':(60,-140,0)}


def clamp(v):
    return max(0,min(64,v))


def evaluate(verify=False):
    cases, rasters = [], []
    resolver = ResourceResolver((ROOT/'games/petz4',))
    for species in ('Dogz','Catz'):
        source,raw,*_ = adult(species)
        for pose in ('standing','sitting','lying'):
            assets = load_breed_assets(resolver,str(source.relative_to(ROOT/'games/petz4')),pose=pose,seed=0,age=100,fatness=50)
            stock = assets.appearance
            assert not ({14,15} & {a.add_group for a in stock.add_balls})
            first = 67+len(stock.add_balls)
            assert all(p.start < first and p.end < first for p in stock.projections)
            head = stock.key_balls.head
            checks, selected = [], []
            for topology in ('chain','cycle'):
                for mode in ('static','all_group15','root_static','root_dormant','root_activated'):
                    for order in permutations('ABC'):
                        ids = {name:first+i for i,name in enumerate(order)}
                        refs = {'A':head if topology=='chain' else ids['C'], 'B':ids['A'], 'C':ids['B']}
                        groups = {name:0 if mode=='static' or (name=='A' and mode=='root_static') else 14 if name=='A' and mode.startswith('root_') else 15 for name in order}
                        rows = []
                        for name in order:
                            x,y,z = OFFSETS[name]
                            rows.append(f'{head}, {x}, {y}, {z}, 125, 244, -1, 0, -1, -1, {SIZES[name]}, 8, {groups[name]}, -1, {refs[name]}')
                        adds = read_core({'Add Ball':tuple(rows)}).add_balls
                        appearance = replace(stock,add_balls=stock.add_balls+adds)
                        for amount in ((100,) if mode=='static' else (1,25,100)):
                            updates = ((15,amount),)+(((14,100),) if mode=='root_activated' else ())
                            m = evaluate_morphs(appearance,67,updates)
                            g = posed_geometry(appearance,assets.sizes,assets.frame,fatness=50,morph_updates=updates)
                            # Independent identity-keyed recurrence: only already encountered refs resolve.
                            expected = {}
                            for name in order:
                                active = not (name=='A' and mode=='root_dormant')
                                evaluated = SIZES[name] if groups[name]==0 else 0
                                ref_name = {'A':'head' if topology=='chain' else 'C','B':'A','C':'B'}[name]
                                if not active:
                                    radius = 0
                                elif ref_name=='head':
                                    radius = clamp((evaluated*stock.ball_scale >> 8)+g[head].radius)
                                elif ref_name in expected:
                                    radius = clamp((evaluated*stock.ball_scale >> 8)+expected[ref_name])
                                else:
                                    radius = clamp(evaluated*stock.ball_scale >> 9)
                                    if stock.draw_small_balls and evaluated>0 and radius<1:
                                        radius=1
                                expected[name]=radius
                                assert m.sizes[ids[name]-67] == evaluated
                                assert g[ids[name]].radius == radius
                                assert g[ids[name]].parked == (not active)
                                assert g[ids[name]].visible
                            reversed_g = posed_geometry(appearance,assets.sizes,assets.frame,fatness=50,morph_updates=tuple(reversed(updates)))
                            assert reversed_g == g
                            if topology=='cycle' and mode in ('all_group15','root_dormant','root_activated'):
                                assert set(expected.values()) == {0}
                            if topology=='chain' and order==tuple('ABC') and mode in ('all_group15','root_activated'):
                                assert set(expected.values()) == {g[head].radius}
                            checks.append({'topology':topology,'mode':mode,'order':''.join(order),'amount':amount,
                                'ids':ids,'references':refs,'groups':groups,'morph_sizes':{name:m.sizes[ids[name]-67] for name in order},
                                'expected_radii':expected,'markers':{name:asdict(g[ids[name]]) for name in 'ABC'},
                                'head_radius':g[head].radius,'reversed_updates_geometry_equal':True})
                            if amount==100 and ''.join(order) in ('ABC','CBA'):
                                p = prepare_frame(appearance,assets.sizes,assets.frame,textures=assets.textures,fatness=50,morph_updates=updates)
                                selected.append((f'{topology}-{mode}-{"".join(order)}',replace(assets,appearance=appearance),p))
            boxes = [p.geometry.ordering.bounds for _,_,p in selected]
            bounds = replace(boxes[0],min_x=min(b.min_x for b in boxes),min_y=min(b.min_y for b in boxes),
                             max_x=max(b.max_x for b in boxes),max_y=max(b.max_y for b in boxes))
            records=[]
            for name,a,p in selected:
                fb,_,png = draw(a,p,bounds)
                filename=f'{species}-{pose}-{name}.png'
                if verify:
                    assert (OUT/filename).read_bytes()==png
                else:
                    (OUT/filename).write_bytes(png)
                records.append({'name':name,'png':filename,'png_sha256':SHA(png),'indexed_sha256':SHA(fb.pixels),
                                'width':fb.width,'height':fb.height})
            cases.append({'species':species,'pose':pose,'source':str(source.relative_to(ROOT)),
                          'source_sha256':SHA(raw),'checks':checks})
            rasters.append({'species':species,'pose':pose,'bounds':asdict(bounds),'records':records})
            assert source.read_bytes()==raw
            print(species,pose,len(checks),'checks',len(records),'rasters',flush=True)
    return cases,rasters


def main(verify=False):
    if not verify:
        OUT.mkdir(parents=True,exist_ok=False)
    cases,rasters=evaluate(verify)
    report={'experiment':'MORPH-008',**provenance(),
        'backend':'direct Python immutable appearance copies; parsed synthetic rows; no MCP calls',
        'controls':{'game_version':'petz4','seed':0,'age':100,'fatness':50,'yaw':0,
            'sizes':SIZES,'offsets':OFFSETS,'reference_ids':'remapped by marker identity after each permutation',
            'raster_seed':1,'line_rng_seed':1,'step':0,'state':'fresh every draw'},
        'baseline_manifest_sha256':SHA((ROOT/'experiments/morph-006.json').read_bytes()),
        'cases':cases,'rasters':rasters,
        'summary':{'numerical_cases':sum(len(c['checks']) for c in cases),'pngs':sum(len(c['records']) for c in rasters)}}
    report=json.loads(json.dumps(report))
    if verify:
        assert report==json.loads(PUBLIC.read_text())==json.loads((OUT/'report.json').read_text())
        print('Full replay verified',report['summary'])
    else:
        for p in (PUBLIC,OUT/'report.json'):
            p.write_text(json.dumps(report,indent=2)+'\n')
        print(report['summary'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true')
    main(parser.parse_args().verify)
