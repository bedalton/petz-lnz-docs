"""Replay TEXTURE-004 transitions and audit persisted state/pixel attribution."""
import importlib.metadata
import json
from dataclasses import asdict,replace
from io import BytesIO
from pathlib import Path
from PIL import Image
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.preparation import prepare_frame,FrameState
from texture_motion_history import HISTORIES,diagnostic
from morph_pixel_probe import draw,pixel_diff
from research_common import ROOT,SHA


def main():
    folder=ROOT/'scratch/research/texture-004';path=ROOT/'experiments/texture-004.json'
    report=json.loads(path.read_text());assert report==json.loads((folder/'report.json').read_text())
    assert report['histories']==json.loads(json.dumps(HISTORIES))
    for name,digest in report['source_hashes'].items():
        for root in (Path(petz_renderer.__file__).parent,ROOT/'petz-renderer-mcp/src/petz_renderer'):
            assert SHA((root/name).read_bytes())==digest
    for name,version in report['dependencies'].items():assert importlib.metadata.version(name)==version
    for name,digest in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==digest
    prior=json.loads((ROOT/'experiments/line-021.json').read_text());input_root=ROOT/'scratch/research/line-021'
    resolver=ResourceResolver((ROOT/'games/petz4',input_root));counts={'histories':0,'sheets':0,'rgba_cells':0,'transition_states':0,'final_states':0,'baseline_pngs':0,'mcp_baselines':0}
    inputs=set()
    for n,c in enumerate(report['cases']):
        previous=next(x for x in prior['cases'] if x['species']==c['species'] and x['dimensions']==[128,128])
        assert c['input']==previous['paths']['textured'] and c['input_sha256']==previous['input_hashes']['textured']
        assert SHA((input_root/c['input']).read_bytes())==c['input_sha256'];inputs.add(c['input'])
        assert SHA((ROOT/previous['source_path']).read_bytes())==previous['source_sha256']
        raw=(folder/c['private_state_file']).read_bytes();assert SHA(raw)==c['private_state_sha256'];saved=json.loads(raw);assert saved['case']==n
        a=load_breed_assets(resolver,c['input'],pose=c['pose'],seed=0,age=100,fatness=50)
        target={'fatness':50,'yaw':c['yaw_units']}
        call=lambda state=None,controls=target:prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,state=state,**controls)
        fresh=call();bounds=fresh.geometry.ordering.bounds;initial_fb,state,_=draw(a,fresh,bounds)
        for i,changes in enumerate(HISTORIES[c['history']]):
            controls=dict(target);controls.update({k:v for k,v in changes.items() if k!='yaw_delta'});controls['yaw']+=changes.get('yaw_delta',0)
            if i==3:before=state
            p=call(state,controls);_,state,_=draw(a,p,p.geometry.ordering.bounds)
            assert saved['trace'][i]['controls']==controls
            assert saved['trace'][i]['state']==json.loads(json.dumps(asdict(state)))
            counts['transition_states']+=1
        assert saved['before_final_state']==json.loads(json.dumps(asdict(before)))
        full=call(before);geom=call(FrameState(geometry=before.geometry));tex=call(FrameState(orientations=before.orientations))
        order=replace(fresh,geometry=replace(fresh.geometry,ordering=replace(fresh.geometry.ordering,sorted_order=full.geometry.ordering.sorted_order,draw_order=full.geometry.ordering.draw_order)))
        prepared=(fresh,full,geom,tex,order);output=[draw(a,p,bounds) for p in prepared]
        assert output[1][1]==state
        assert all(p.geometry.balls==fresh.geometry.balls and p.geometry.ordering.bounds==bounds for p in prepared)
        assert [diagnostic(a,p) for p in prepared]==c['diagnostic']
        assert (fresh.geometry.fills==full.geometry.fills)==c['same_fills']
        assert (fresh.geometry.ordering.sorted_order==full.geometry.ordering.sorted_order)==c['same_order']
        assert [i for i,(x,y) in enumerate(zip(fresh.balls,full.balls)) if x.circle!=y.circle]==c['changed_circle_ids']
        assert [pixel_diff(initial_fb.pixels,o[0].pixels) for o in output]==c['changed_from_fresh']
        assert pixel_diff(output[1][0].pixels,output[2][0].pixels)==c['full_vs_geometry']
        assert pixel_diff(output[1][0].pixels,output[3][0].pixels)==c['full_vs_texture']
        png=(folder/c['sheet']).read_bytes();assert SHA(png)==c['sheet_sha256'];im=Image.open(BytesIO(png)).convert('RGBA');w,h=c['cell_size']
        for i,o in enumerate(output):
            pixels=bytes(saved['indexed_pixels'][i]);assert pixels==o[0].pixels and SHA(pixels)==c['indexed_hashes'][i]
            assert saved['final_states'][i]==json.loads(json.dumps(asdict(o[1])))
            rgba=Image.open(BytesIO(o[2])).convert('RGBA').tobytes();assert SHA(rgba)==c['cell_hashes'][i]['rgba_sha256']
            assert im.crop((i*w,0,(i+1)*w,h)).tobytes()==rgba
            counts['rgba_cells']+=1;counts['final_states']+=1
        counts['histories']+=1;counts['sheets']+=1
    for b in report['baselines']:
        raw=(folder/b['png']).read_bytes();assert SHA(raw)==b['png_sha256'] and b['local_mcp_match']
        meta=json.loads((folder/(Path(b['png']).stem+'-mcp.json')).read_text());assert meta['game_version']=='petz4'
        assert b['input_sha256'] in json.dumps(meta)
        counts['baseline_pngs']+=1;counts['mcp_baselines']+=1
    summary={'cases':len(report['cases']),'changed_full':sum(bool(c['changed_from_fresh'][1]) for c in report['cases']),'changed_geometry_only':sum(bool(c['changed_from_fresh'][2]) for c in report['cases']),'changed_texture_only':sum(bool(c['changed_from_fresh'][3]) for c in report['cases']),'changed_order_only':sum(bool(c['changed_from_fresh'][4]) for c in report['cases']),'changed_diagnostic':sum(c['diagnostic'][0]['indexed_sha256']!=c['diagnostic'][1]['indexed_sha256'] for c in report['cases'])}
    assert summary==report['summary']
    assert counts=={'histories':48,'sheets':48,'rgba_cells':240,'transition_states':192,'final_states':240,'baseline_pngs':12,'mcp_baselines':12}
    result={'experiment':'TEXTURE-004','report_sha256':SHA(path.read_bytes()),'verified':counts,'reused_copies':len(inputs),'summary':summary}
    (ROOT/'scratch/research/texture-004-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
