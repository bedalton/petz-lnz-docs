"""UPDATE-007: separate host orientations and paint angles after motion."""
import json
from dataclasses import asdict, replace
from pathlib import Path
import importlib.metadata
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame
from morph_pixel_probe import draw, pixel_diff
from texture_motion_history import HISTORIES, diagnostic
from revalidate_static_matrix import choices, state_hash
from research_common import ROOT, SHA

OUT = ROOT/'scratch/research/update-007'
PRIOR = ROOT/'scratch/research/update-002/texture-004'


def evaluate(case, historical, folder, verify=False):
    root = ROOT/'scratch/research/line-021'
    assert SHA((root/case['input']).read_bytes()) == case['input_sha256']
    resolver = ResourceResolver((ROOT/'games/petz4', root))
    assets = load_breed_assets(resolver, case['input'], pose=case['pose'], seed=0, age=100, fatness=50)
    target = {'fatness': 50, 'yaw': case['yaw_units']}
    def prepare(state=None, controls=target):
        return prepare_frame(assets.appearance, assets.sizes, assets.frame,
                             textures=assets.textures, state=state, **controls)
    fresh = prepare()
    bounds = fresh.geometry.ordering.bounds
    initial, state, _ = draw(assets, fresh, bounds)
    saved_raw = (PRIOR/historical['private_state_file']).read_bytes()
    assert SHA(saved_raw) == historical['private_state_sha256']
    saved = json.loads(saved_raw)
    transitions = []
    for index, changes in enumerate(HISTORIES[case['history']]):
        controls = dict(target)
        controls.update({k:v for k,v in changes.items() if k != 'yaw_delta'})
        controls['yaw'] += changes.get('yaw_delta', 0)
        if index == 3:
            before = state
        p = prepare(state, controls)
        _, state, _ = draw(assets, p, p.geometry.ordering.bounds)
        assert saved['trace'][index]['controls'] == controls
        assert saved['trace'][index]['state'] == json.loads(json.dumps(asdict(state)))
        transitions.append({'controls': controls, 'state_sha256': state_hash(state)})
    assert saved['before_final_state'] == json.loads(json.dumps(asdict(before)))
    full = prepare(before)
    prepared = {name: prepare(value) for name, value in choices(before).items()}
    prepared['order_only'] = replace(fresh, geometry=replace(fresh.geometry,
        ordering=replace(fresh.geometry.ordering, sorted_order=full.geometry.ordering.sorted_order,
                         draw_order=full.geometry.ordering.draw_order)))
    output = {}
    for name, p in prepared.items():
        assert p.geometry.balls == fresh.geometry.balls
        assert p.geometry.ordering.bounds == bounds
        fb, after, png = draw(assets, p, bounds)
        path = folder/(name+'.png')
        if verify:
            assert path.read_bytes() == png
        else:
            path.write_bytes(png)
        output[name] = {'png': path.name, 'png_sha256': SHA(png), 'indexed_sha256': SHA(fb.pixels),
            'state_sha256': state_hash(after), 'changed_from_fresh': pixel_diff(initial.pixels, fb.pixels),
            'diagnostic': diagnostic(assets, p)}
    for name, index in (('fresh',0), ('full',1), ('geometry_only',2), ('host_texture_only',3), ('order_only',4)):
        assert output[name]['indexed_sha256'] == historical['indexed_hashes'][index]
        assert output[name]['changed_from_fresh'] == historical['changed_from_fresh'][index]
    return {'transitions': transitions, 'outputs': output,
        'host_equals_combined': output['host_texture_only']['indexed_sha256'] == output['all_texture_only']['indexed_sha256'],
        'paint_only_equals_fresh': output['paint_angles_only']['indexed_sha256'] == output['fresh']['indexed_sha256'],
        'combined_equals_full': output['all_texture_only']['indexed_sha256'] == output['full']['indexed_sha256']}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    prior_path = PRIOR/'report.json'
    prior = json.loads(prior_path.read_text())
    upgrade = json.loads((ROOT/'experiments/update-001.json').read_text())
    for name, digest in upgrade['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    cases = []
    for index, historical in enumerate(prior['cases']):
        case = {k: historical[k] for k in ('species','pose','yaw_degrees','yaw_units','history','input','input_sha256')}
        folder = OUT/f'case{index:02d}'
        folder.mkdir()
        case['folder'] = folder.name
        case.update(evaluate(case, historical, folder))
        cases.append(case)
        print(folder.name, case['history'], 'host=combined', case['host_equals_combined'],
              'paint=fresh', case['paint_only_equals_fresh'], flush=True)
    summary = {'histories': len(cases), 'transition_states': 4*len(cases), 'final_draws': 7*len(cases),
        'host_vs_combined_differences': sum(not c['host_equals_combined'] for c in cases),
        'paint_only_vs_fresh_differences': sum(not c['paint_only_equals_fresh'] for c in cases),
        'combined_vs_full_differences': sum(not c['combined_equals_full'] for c in cases),
        'diagnostic_changes': sum(o['diagnostic']['indexed_sha256'] != c['outputs']['fresh']['diagnostic']['indexed_sha256']
                                   for c in cases for o in c['outputs'].values())}
    paint_scope = []
    for historical in prior['cases']:
        saved = json.loads((PRIOR/historical['private_state_file']).read_text())
        angles = saved['before_final_state']['paint_angles']
        paint_scope.append({'slots': len(angles), 'nonzero_pairs': sum(any(a) for a in angles)})
    result = {'experiment':'UPDATE-007', 'renderer_revision': upgrade['renderer_revision'],
        'backend':'direct renderer state components; linked UPDATE-002 fresh MCP baselines only',
        'source_hashes': upgrade['source_hashes'], 'prior_report_sha256': SHA(prior_path.read_bytes()),
        'dependencies': {n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','pillow')},
        'controls': prior['controls'], 'engine_hashes':prior['engine_hashes'], 'cases':cases, 'summary':summary,
        'before_final_paint_angle_scope': paint_scope}
    for path in (OUT/'report.json', ROOT/'experiments/update-007.json'):
        path.write_text(json.dumps(result, indent=2)+'\n')
    print(summary, flush=True)


if __name__ == '__main__':
    main()
