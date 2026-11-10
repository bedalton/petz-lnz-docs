"""PAINT-009: same-length reordering and retained paint-angle identity."""
from dataclasses import replace
from io import BytesIO
import json
import sys
from PIL import Image
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.preparation import FrameState,prepare_frame
from petz_renderer.rendering.texture_rotation import TextureOrientation
from morph_pixel_probe import draw
from research_common import ROOT,SHA
from saved_colour_arrays import provenance

OUT=ROOT/'scratch/research/paint-009';MANIFEST=ROOT/'experiments/paint-009.json'
ORDER=tuple(range(16))+(18,17,16)
DELTAS=((37,-23),(-17,11),(7,41))


def evaluate(case,assets,verify):
    state_path=ROOT/'scratch/research/paint-001'/case['folder']/'states.json'
    raw=state_path.read_bytes();assert SHA(raw)==case['private_states_sha256']
    before=json.loads(raw)['before_final']
    original_state=FrameState(orientations=tuple(TextureOrientation(**{k:tuple(v) for k,v in o.items()}) for o in before['orientations']),
        paint_angles=tuple(tuple(a) for a in before['paint_angles']))
    paints=assets.appearance.paint_balls;angles=original_state.paint_angles
    assert len(paints)==len(angles)==19
    assert [i for i,a in enumerate(angles) if any(a)]==[16,17,18] and len(set(angles[16:]))==1
    assert len({p.base for p in paints[16:]})==1 and len(set(paints[16:]))==3
    appearance=replace(assets.appearance,paint_balls=tuple(paints[i] for i in ORDER))
    reordered=replace(assets,appearance=appearance)
    tagged=angles[:16]+tuple(tuple(a+d for a,d in zip(pair,delta)) for pair,delta in zip(angles[16:],DELTAS))
    assert len(set(tagged[16:]))==3
    def prepare(asset,vector):
        return prepare_frame(asset.appearance,asset.sizes,asset.frame,textures=asset.textures,
            fatness=asset.preview.fatness,yaw=case['yaw_units'],state=replace(original_state,paint_angles=vector))
    original_tagged=prepare(assets,tagged)
    prepared={name:(a,prepare(a,v)) for name,a,v in (
        ('original_actual',assets,angles),('reordered_actual',reordered,angles),
        ('reordered_actual_remap',reordered,tuple(angles[i] for i in ORDER)),
        ('reordered_tagged_stale',reordered,tagged),
        ('reordered_tagged_remap',reordered,tuple(tagged[i] for i in ORDER)))}
    assert prepared['reordered_actual'][1]==prepared['reordered_actual_remap'][1]
    stale=prepared['reordered_tagged_stale'][1];remap=prepared['reordered_tagged_remap'][1]
    assert stale.geometry==remap.geometry
    def paint_commands(p):return {c.paint_index:c for b in p.balls for c in b.paints}
    old=paint_commands(original_tagged);mapped=paint_commands(remap);wrong=paint_commands(stale)
    assert set(old)==set(mapped)==set(wrong)=={16,17,18}
    for i in mapped:
        assert mapped[i]==replace(old[ORDER[i]],paint_index=i)
        assert replace(wrong[i],angles=mapped[i].angles)==mapped[i]
    assert [i for i in sorted(mapped) if mapped[i].angles!=wrong[i].angles]==[16,18]
    for s,r in zip(stale.balls,remap.balls,strict=True):assert replace(s,paints=r.paints)==r
    results={};images={}
    for name,(a,p) in prepared.items():
        fb,_,png=draw(a,p,p.geometry.ordering.bounds);image=Image.open(BytesIO(png)).convert('RGBA');rgba=image.tobytes()
        filename=f'{case["folder"]}-{name}.png'
        if verify:assert (OUT/filename).read_bytes()==png
        else:(OUT/filename).write_bytes(png)
        results[name]={'png':filename,'png_sha256':SHA(png),'rgba_sha256':SHA(rgba),'indexed_sha256':SHA(fb.pixels)}
        images[name]=rgba
    assert results['original_actual']['png_sha256']==case['outputs']['all_texture_only']['png_sha256']
    assert images['reordered_actual']==images['reordered_actual_remap']
    def changed(a,b):
        x,y=images[a],images[b];assert len(x)==len(y)
        return sum(x[i:i+4]!=y[i:i+4] for i in range(0,len(x),4))
    return {'prior_folder':case['folder'],'state_sha256':SHA(raw),'outputs':results,
        'actual_active_angles':[list(a) for a in angles[16:]],
        'tagged_stale_command_angles':[list(wrong[i].angles) for i in (16,17,18)],
        'tagged_remap_command_angles':[list(mapped[i].angles) for i in (16,17,18)],
        'tagged_stale_remap_rgba_changed':changed('reordered_tagged_stale','reordered_tagged_remap'),
        'actual_order_only_rgba_changed':changed('original_actual','reordered_actual')}


def main():
    verify='--verify' in sys.argv
    if not verify:OUT.mkdir(parents=True,exist_ok=False)
    prior_path=ROOT/'experiments/paint-001.json';prior=json.loads(prior_path.read_text());prov=provenance();cases=[];cache={}
    resolver=ResourceResolver((ROOT/'games/petz4',))
    for c in prior['cases']:
        if c['name']!='Fuzzkin':continue
        assert SHA((ROOT/'games/petz4'/c['path']).read_bytes())==c['input_sha256']
        if c['pose'] not in cache:cache[c['pose']]=load_saved_assets(resolver,c['path'],pose=c['pose'])
        cases.append(evaluate(c,cache[c['pose']],verify))
    report={'experiment':'PAINT-009','backend':'direct retained-state paint permutation; no new MCP calls',
        'provenance':prov,'prior_manifest_sha256':SHA(prior_path.read_bytes()),
        'controls':{'new_index_to_old_index':ORDER,'angle_deltas':DELTAS,'raster_seed':1,'line_seed':1,'step':0,
            'geometry_state':'fresh; only PAINT-001 host orientations and paint angles retained'},
        'cases':cases,'summary':{'histories':len(cases),'draws':5*len(cases),'prior_png_links':len(cases),
            'actual_angle_remap_equivalences':len(cases),
            'tagged_stale_remap_pixel_changes':sum(c['tagged_stale_remap_rgba_changed']>0 for c in cases),
            'actual_order_pixel_changes':sum(c['actual_order_only_rgba_changed']>0 for c in cases)}}
    report=json.loads(json.dumps(report))
    if verify:assert report==json.loads(MANIFEST.read_text())==json.loads((OUT/'report.json').read_text())
    else:
        for p in (MANIFEST,OUT/'report.json'):p.write_text(json.dumps(report,indent=2)+'\n')
    print('PAINT-009 verified' if verify else 'PAINT-009 complete',report['summary'],flush=True)

if __name__=='__main__':main()
