"""PAINT-001: saved-pet motion with independent paint-angle state controls."""
import asyncio
from dataclasses import asdict, replace
import importlib.metadata
import json
from pathlib import Path
import sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.preparation import prepare_frame
from texture_motion_history import HISTORIES
from revalidate_static_matrix import choices, state_hash
from morph_pixel_probe import draw, pixel_diff
from research_common import ROOT, SHA, save_result

OUT = ROOT/'scratch/research/paint-001'


def evaluate(assets, yaw, history, folder, verify=False):
    target = {'fatness': assets.preview.fatness, 'yaw': yaw}
    def prepare(state=None, controls=target):
        return prepare_frame(assets.appearance, assets.sizes, assets.frame,
                             textures=assets.textures, state=state, **controls)
    fresh = prepare()
    bounds = fresh.geometry.ordering.bounds
    initial, state, _ = draw(assets, fresh, bounds)
    trace = []
    for index, changes in enumerate(HISTORIES[history]):
        controls = dict(target)
        controls.update({k:v for k,v in changes.items() if k != 'yaw_delta'})
        controls['yaw'] += changes.get('yaw_delta',0)
        if index == 3:
            before = state
        p = prepare(state, controls)
        _, state, _ = draw(assets, p, p.geometry.ordering.bounds)
        trace.append({'controls':controls, 'state':asdict(state)})
    full = prepare(before)
    prepared = {name:prepare(value) for name,value in choices(before).items()}
    prepared['order_only'] = replace(fresh, geometry=replace(fresh.geometry,
        ordering=replace(fresh.geometry.ordering, sorted_order=full.geometry.ordering.sorted_order,
                         draw_order=full.geometry.ordering.draw_order)))
    output, states = {}, {}
    for name,p in prepared.items():
        assert p.geometry.balls == fresh.geometry.balls
        assert p.geometry.ordering.bounds == bounds
        fb, after, png = draw(assets,p,bounds)
        path = folder/(name+'.png')
        if verify:
            assert path.read_bytes() == png
        else:
            path.write_bytes(png)
        output[name] = {'png':path.name,'png_sha256':SHA(png),'indexed_sha256':SHA(fb.pixels),
            'changed_from_fresh':pixel_diff(initial.pixels,fb.pixels),'state_sha256':state_hash(after),
            'textured_paints':sum(paint.paint is not None for ball in p.balls for paint in ball.paints),
            'paint_angles':list(p.state.paint_angles)}
        states[name] = asdict(after)
    raw = json.dumps({'trace':trace,'before_final':asdict(before),'final_states':states},sort_keys=True).encode()
    path = folder/'states.json'
    if verify:
        assert path.read_bytes() == raw
    else:
        path.write_bytes(raw)
    return json.loads(json.dumps({'outputs':output,'private_states_sha256':SHA(raw),
        'before_nonzero_paint_angles':sum(any(pair) for pair in before.paint_angles),
        'host_vs_combined_changed':output['host_texture_only']['indexed_sha256'] != output['all_texture_only']['indexed_sha256'],
        'paint_vs_fresh_changed':output['paint_angles_only']['indexed_sha256'] != output['fresh']['indexed_sha256'],
        'combined_vs_full_changed':output['all_texture_only']['indexed_sha256'] != output['full']['indexed_sha256']}))


async def main():
    OUT.mkdir(parents=True,exist_ok=False)
    resolver = ResourceResolver((ROOT/'games/petz4',))
    upgrade = json.loads((ROOT/'experiments/update-001.json').read_text())
    for name,digest in upgrade['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    cases, baselines = [], []
    old = json.loads((ROOT/'experiments/update-003.json').read_text())
    for name in ('Fuzzkin','Homebody'):
        path = f'Adopted Petz/{name}.pet'
        digest = SHA((ROOT/'games/petz4'/path).read_bytes())
        for pose in ('standing','sitting','lying'):
            assets = load_saved_assets(resolver,path,pose=pose)
            for degrees,yaw in ((0,0),(90,64)):
                for history in HISTORIES:
                    stem = f'{name}-{pose}-{degrees}-{history}'
                    folder = OUT/stem
                    folder.mkdir()
                    case = {'name':name,'path':path,'input_sha256':digest,'pose':pose,
                        'yaw_degrees':degrees,'yaw_units':yaw,'history':history,'folder':stem,
                        'preview':asdict(assets.preview)}
                    case.update(evaluate(assets,yaw,history,folder))
                    prior = next(c for c in old['cases'] if c['name']==name and c['controls']['pose']==pose
                                 and c['controls']['yaw_degrees']==degrees)
                    assert case['outputs']['fresh']['png_sha256'] == prior['png_sha256']
                    cases.append(case)
                    print(stem,'nonzero',case['before_nonzero_paint_angles'],
                          'paint pixels',case['outputs']['paint_angles_only']['changed_from_fresh'],flush=True)
                baselines.append({'name':name,'path':path,'pose':pose,'yaw_degrees':degrees,
                    'input_sha256':digest,'png_sha256':cases[-1]['outputs']['fresh']['png_sha256']})
        assert SHA((ROOT/'games/petz4'/path).read_bytes()) == digest
    transport = StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp',
        '--game-version','petz4','--game-root',str(ROOT/'games/petz4')])
    async with Client(transport) as client:
        for b in baselines:
            args = {'path':b['path'],'pose':b['pose'],'yaw_degrees':b['yaw_degrees']}
            stem = f"{b['name']}-{b['pose']}-{b['yaw_degrees']}-mcp"
            png,meta = await save_result(client,'render_pet',args,OUT,stem)
            assert SHA(png) == b['png_sha256']
            assert meta['game_version']=='petz4'
            assert meta['appearance']['age_source']=='saved' and meta['appearance']['fatness_source']=='saved'
            b.update(stem=stem,controls=args)
    summary = {name:{'histories':len(rows := [c for c in cases if c['name']==name]),
        'nonzero_pre_target_states':sum(bool(c['before_nonzero_paint_angles']) for c in rows),
        'paint_only_pixel_changes':sum(c['paint_vs_fresh_changed'] for c in rows),
        'host_vs_combined_differences':sum(c['host_vs_combined_changed'] for c in rows),
        'combined_vs_full_differences':sum(c['combined_vs_full_changed'] for c in rows)} for name in ('Fuzzkin','Homebody')}
    report = {'experiment':'PAINT-001','renderer_revision':upgrade['renderer_revision'],
        'backend':'direct retained FrameState; local stdio MCP fresh saved-pet baselines',
        'source_hashes':upgrade['source_hashes'],
        'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','pillow')},
        'engine_hashes':json.loads((ROOT/'experiments/restore-002.json').read_text())['shared_engine_hashes']['petz4'],
        'baseline_manifest_sha256':SHA((ROOT/'experiments/update-003.json').read_bytes()),
        'controls':{'saved_seed_age_fatness':True,'raster_seed':1,'line_rng_seed':1,'step':0,
            'animation_frame':'fixed named pose','history_units':'engine turns/256'},
        'cases':cases,'baselines':baselines,'summary':summary}
    for path in (OUT/'report.json',ROOT/'experiments/paint-001.json'):
        path.write_text(json.dumps(report,indent=2)+'\n')
    print(summary,flush=True)


if __name__=='__main__':
    asyncio.run(main())
