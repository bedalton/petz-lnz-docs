"""PAINT-002: substitute only individual prepared paint-command angles."""
from dataclasses import replace
import json
from pathlib import Path
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.preparation import prepare_frame, FrameState
from texture_motion_history import HISTORIES
from morph_pixel_probe import draw, pixel_diff
from research_common import ROOT,SHA

OUT=ROOT/'scratch/research/paint-002'


def evaluate(case, assets, folder, verify=False):
    target={'fatness':assets.preview.fatness,'yaw':case['yaw_units']}
    def prepare(state=None,controls=target):
        return prepare_frame(assets.appearance,assets.sizes,assets.frame,textures=assets.textures,state=state,**controls)
    fresh=prepare()
    _,state,_=draw(assets,fresh,fresh.geometry.ordering.bounds)
    for changes in HISTORIES[case['history']][:-1]:
        controls=dict(target)
        controls.update({k:v for k,v in changes.items() if k!='yaw_delta'})
        controls['yaw']+=changes.get('yaw_delta',0)
        p=prepare(state,controls)
        _,state,_=draw(assets,p,p.geometry.ordering.bounds)
    host=prepare(FrameState(orientations=state.orientations))
    combined=prepare(FrameState(orientations=state.orientations,paint_angles=state.paint_angles))
    assert host.geometry==combined.geometry
    eligible=[]
    for h,c in zip(host.balls,combined.balls,strict=True):
        assert replace(h,paints=c.paints)==c
        for hp,cp in zip(h.paints,c.paints,strict=True):
            assert replace(hp,angles=cp.angles)==cp
            if hp.angles!=cp.angles:
                eligible.append(cp.paint_index)
    assert sorted(eligible)==[16,17,18]
    def substitute(ids):
        balls=[]
        for hb,cb in zip(host.balls,combined.balls,strict=True):
            lookup={p.paint_index:p for p in hb.paints}
            balls.append(replace(cb,paints=tuple(lookup[p.paint_index] if p.paint_index in ids else p for p in cb.paints)))
        return replace(combined,balls=tuple(balls))
    modes={'combined':combined,'host':host,**{f'reset_{i}':substitute({i}) for i in eligible},'reset_all':substitute(set(eligible))}
    output={};pixels={}
    for name,p in modes.items():
        fb,_,png=draw(assets,p,combined.geometry.ordering.bounds)
        path=folder/(name+'.png')
        if verify:assert path.read_bytes()==png
        else:path.write_bytes(png)
        output[name]={'png':path.name,'png_sha256':SHA(png),'indexed_sha256':SHA(fb.pixels)}
        pixels[name]=fb.pixels
    assert output['combined']['png_sha256']==case['outputs']['all_texture_only']['png_sha256']
    assert output['host']['png_sha256']==case['outputs']['host_texture_only']['png_sha256']
    assert pixels['reset_all']==pixels['host']
    for name in output:
        output[name]['changed_from_combined']=pixel_diff(pixels['combined'],pixels[name])
        output[name]['remaining_from_host']=pixel_diff(pixels['host'],pixels[name])
    return {'eligible_indices':sorted(eligible),'outputs':output,
        'angle_changes':[{'index':i,'host':list(next(p.angles for b in host.balls for p in b.paints if p.paint_index==i)),
            'combined':list(next(p.angles for b in combined.balls for p in b.paints if p.paint_index==i))} for i in eligible]}


def main():
    OUT.mkdir(parents=True,exist_ok=False)
    prior_path=ROOT/'experiments/paint-001.json'
    prior=json.loads(prior_path.read_text())
    for name,digest in prior['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes())==digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==digest
    resolver=ResourceResolver((ROOT/'games/petz4',));cache={};cases=[]
    for index,c in enumerate(c for c in prior['cases'] if c['name']=='Fuzzkin'):
        assert SHA((ROOT/'games/petz4'/c['path']).read_bytes())==c['input_sha256']
        if c['pose'] not in cache:cache[c['pose']]=load_saved_assets(resolver,c['path'],pose=c['pose'])
        folder=OUT/f'case{index:02d}';folder.mkdir()
        result={k:c[k] for k in ('name','path','input_sha256','pose','yaw_degrees','yaw_units','history')}
        result.update(folder=folder.name,prior_folder=c['folder'])
        result.update(evaluate(c,cache[c['pose']],folder))
        cases.append(result)
        print(folder.name,[o['changed_from_combined'] for o in result['outputs'].values()],flush=True)
    summary={'cases':len(cases),'final_draws':6*len(cases),'prior_pixel_links':2*len(cases),
        'all_angle_resets_match_host':len(cases),
        'individual_visible_cases':{str(i):sum(bool(c['outputs'][f'reset_{i}']['changed_from_combined']) for c in cases) for i in (16,17,18)}}
    report={'experiment':'PAINT-002','renderer_revision':prior['renderer_revision'],
        'backend':'direct prepared-command angle substitutions; linked PAINT-001 baselines only',
        'source_hashes':prior['source_hashes'],'dependencies':prior['dependencies'],
        'prior_manifest_sha256':SHA(prior_path.read_bytes()),'controls':prior['controls'],
        'cases':cases,'summary':summary}
    for path in (OUT/'report.json',ROOT/'experiments/paint-002.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print(summary,flush=True)


if __name__=='__main__':main()
