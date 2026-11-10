"""Verify UPDATE-004 input identity, cell bytes and historical relationships."""
import json
from pathlib import Path
from io import BytesIO
from PIL import Image
import petz_renderer
from research_common import ROOT,SHA
from revalidate_renderer_update import digests,partition
folder=ROOT/'scratch/research/update-004';path=ROOT/'experiments/update-004.json';r=json.loads(path.read_text());assert r==json.loads((folder/'report.json').read_text())
for name,h in json.loads((ROOT/'experiments/update-001.json').read_text())['source_hashes'].items():assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes())==h
for name,h in r['historical_reports'].items():assert SHA((ROOT/f'experiments/{name}.json').read_bytes())==h
cells=0;confirmed=0;inputs={};omission_observations=[]
for row in r['replays']:
    old=json.loads((ROOT/f"experiments/{row['experiment']}.json").read_text());rec=(old.get('comparisons',[])+old.get('pages',[]))[row['index']]
    assert rec['controls']==row['controls'];known=digests(old)
    for filename,h in row['input_hashes'].items():
        p=ROOT/row['asset_root']/filename;assert SHA(p.read_bytes())==h and h in known;inputs[str(p.relative_to(ROOT))]=h
    png=(folder/(row['stem']+'.png')).read_bytes();assert SHA(png)==row['png_sha256'];meta=json.loads((folder/(row['stem']+'-render.json')).read_text());assert meta['game_version']=='petz4';im=Image.open(BytesIO(png)).convert('RGBA')
    h=row['cell_hashes']
    for c,digest in zip(meta['cells'],h,strict=True):
        x,y=c['origin'];assert SHA(im.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes())==digest==c['pixel_sha256'];cells+=1
    if row['old_cell_hashes']:expected=partition(row['old_cell_hashes'])==partition(h)
    elif 'cells_equal' in rec:expected=(h[0]==h[1])==rec['cells_equal']
    elif row['experiment']=='head-001':expected=h[0]!=h[1]
    elif row['experiment']=='vis-002':expected=all((x==h[0])==c['same_as_control'] for x,c in zip(h,rec['cells'],strict=True))
    else:
        observations={o['ball']:o for o in old['observations'] if o['species']==rec['species'] and o['yaw']==rec['controls']['yaw_degrees']}
        expected=True
        for i,ball in enumerate(rec['cell_ball_ids']):
            if ball is None:continue
            same=h[i]==h[0];expected=expected and same==observations[ball]['same_as_control'];omission_observations.append({'species':rec['species'],'yaw':rec['controls']['yaw_degrees'],'ball':ball,'same_as_control':same})
    assert expected==row['relationship_confirmed'];confirmed+=expected
assert len(r['replays'])==64 and cells==400 and len(omission_observations)==268
result={'report_sha256':SHA(path.read_bytes()),'verified':{'controls':64,'rgba_cells':cells,'confirmed_relationships':confirmed,'rebuilt_private_inputs':len(inputs),'omission_observations':len(omission_observations)},'omission_changed_in_any_view':{s:len({o['ball'] for o in omission_observations if o['species']==s and not o['same_as_control']}) for s in ('Dogz','Catz')}}
assert result['verified']['confirmed_relationships']==r['summary']['relationship_confirmed']
(folder/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
