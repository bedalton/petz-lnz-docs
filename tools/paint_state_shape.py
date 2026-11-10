"""PAINT-003: state vector length/index controls on Fuzzkin motion targets."""
from dataclasses import replace
import json
from pathlib import Path
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.preparation import prepare_frame,FrameState
from texture_motion_history import HISTORIES
from morph_pixel_probe import draw,pixel_diff
from research_common import ROOT,SHA

OUT=ROOT/'scratch/research/paint-003'


def evaluate(c,assets,folder,verify=False):
    target={'fatness':assets.preview.fatness,'yaw':c['yaw_units']}
    def prep(state=None,controls=target):
        return prepare_frame(assets.appearance,assets.sizes,assets.frame,textures=assets.textures,state=state,**controls)
    p=prep();_,state,_=draw(assets,p,p.geometry.ordering.bounds)
    for changes in HISTORIES[c['history']][:-1]:
        controls=dict(target);controls.update({k:v for k,v in changes.items() if k!='yaw_delta'});controls['yaw']+=changes.get('yaw_delta',0)
        p=prep(state,controls);_,state,_=draw(assets,p,p.geometry.ordering.bounds)
    angles=state.paint_angles
    assert len(angles)==len(assets.appearance.paint_balls)
    assert [i for i,a in enumerate(angles) if any(a)]==[16,17,18]
    host=FrameState(orientations=state.orientations)
    combined=replace(host,paint_angles=angles)
    only_active=tuple(a if i in (16,17,18) else (0,0) for i,a in enumerate(angles))
    inactive=list(angles);inactive[0]=(47,-23)
    modes={'host':host,'combined':combined,'short':replace(combined,paint_angles=angles[:-1]),
        'long':replace(combined,paint_angles=angles+((0,0),)),
        'exact_zero':replace(combined,paint_angles=((0,0),)*len(angles)),
        'only_active':replace(combined,paint_angles=only_active),
        'inactive_changed':replace(combined,paint_angles=tuple(inactive))}
    outputs={};buffers={}
    for name,s in modes.items():
        p=prep(s);fb,_,png=draw(assets,p,p.geometry.ordering.bounds)
        path=folder/(name+'.png')
        if verify:assert path.read_bytes()==png
        else:path.write_bytes(png)
        outputs[name]={'png':path.name,'png_sha256':SHA(png),'indexed_sha256':SHA(fb.pixels),
            'supplied_slots':len(s.paint_angles),'prepared_slots':len(p.state.paint_angles),
            'prepared_active_angles':[list(p.state.paint_angles[i]) for i in (16,17,18)]}
        buffers[name]=fb.pixels
    assert outputs['combined']['png_sha256']==c['outputs']['all_texture_only']['png_sha256']
    assert outputs['host']['png_sha256']==c['outputs']['host_texture_only']['png_sha256']
    for name in ('short','long','exact_zero'):assert buffers[name]==buffers['host']
    for name in ('only_active','inactive_changed'):assert buffers[name]==buffers['combined']
    assert buffers['host']!=buffers['combined']
    for name in outputs:
        outputs[name]['changed_from_host']=pixel_diff(buffers['host'],buffers[name])
        outputs[name]['changed_from_combined']=pixel_diff(buffers['combined'],buffers[name])
    return {'paint_slots':len(angles),'outputs':outputs}


def main():
    OUT.mkdir(parents=True,exist_ok=False)
    prior_path=ROOT/'experiments/paint-001.json';prior=json.loads(prior_path.read_text())
    for name,digest in prior['source_hashes'].items():
        assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes())==digest
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==digest
    resolver=ResourceResolver((ROOT/'games/petz4',));cache={};cases=[]
    for i,c in enumerate(c for c in prior['cases'] if c['name']=='Fuzzkin'):
        assert SHA((ROOT/'games/petz4'/c['path']).read_bytes())==c['input_sha256']
        if c['pose'] not in cache:cache[c['pose']]=load_saved_assets(resolver,c['path'],pose=c['pose'])
        folder=OUT/f'case{i:02d}';folder.mkdir()
        result={'prior_folder':c['folder'],'folder':folder.name,**evaluate(c,cache[c['pose']],folder)}
        cases.append(result);print(folder.name,'length/index controls passed',flush=True)
    report={'experiment':'PAINT-003','renderer_revision':prior['renderer_revision'],
        'backend':'direct API state-vector interventions; no new MCP calls',
        'source_hashes':prior['source_hashes'],'dependencies':prior['dependencies'],
        'prior_manifest_sha256':SHA(prior_path.read_bytes()),'cases':cases,
        'summary':{'cases':len(cases),'final_draws':7*len(cases),'prior_pixel_links':2*len(cases),
            'length_mismatch_resets':2*len(cases),'exact_zero_controls':len(cases),
            'active_only_equivalences':len(cases),'inactive_slot_equivalences':len(cases)}}
    for path in (OUT/'report.json',ROOT/'experiments/paint-003.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print(report['summary'],flush=True)


if __name__=='__main__':main()
