"""YOUNG-007: one-entry reversions of sufficient endpoint substitutions."""
import argparse,json
from dataclasses import replace
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT,digest,provenance
from young_endpoint_attribution import difference,sig
from young_endpoint_fields import FACTORS,modify
OUT=ROOT/'scratch/research/young-007';MANIFEST=ROOT/'experiments/young-007.json'
def run(verify):
 old=json.loads(MANIFEST.read_text()) if verify else None
 if not verify:OUT.mkdir(parents=True,exist_ok=False)
 prior=json.loads((ROOT/'experiments/young-006.json').read_text());source=prior['inputs']
 resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'))
 report={'provenance':provenance(),'backend':'direct installed renderer; one-entry immutable reversions; no new MCP calls','prior_manifest_sha256':digest((ROOT/'experiments/young-006.json').read_bytes()),'inputs':source,'renders':[]}
 for mode in ('missing-adult','missing-young'):
  path=source['variants'][mode]['path'];assert digest((ROOT/'scratch/research/young-002'/path).read_bytes())==source['variants'][mode]['sha256']
  for pose in ('standing','sitting','lying'):
   age=load_saved_assets(resolver,path,pose=pose,look='age',age=12);young=load_saved_assets(resolver,path,pose=pose,look='puppy',age=12)
   a,b=age.appearance,young.appearance;full=modify(a,b,FACTORS)
   variants={'full':full}
   for i in range(23,29):
    rows=list(full.add_balls);rows[i]=a.add_balls[i];variants[f'add-{i}']=replace(full,add_balls=tuple(rows))
   # Cardinality is a three-entry group; do not shift a single unmatched index.
   rows=full.add_balls[:29]+a.add_balls[29:];assert len(rows)==len(a.add_balls)
   variants['add-count']=replace(full,add_balls=rows)
   for i in (11,12,13,14):
    rows=list(full.lines);rows[i]=a.lines[i];variants[f'line-{i}']=replace(full,lines=tuple(rows))
   for yaw in (0,90):
    target=render_portrait(young,yaw=yaw*256//360)
    for label,appearance in variants.items():
     result=render_portrait(replace(age,appearance=appearance),yaw=yaw*256//360);stem=f'{mode}-{pose}-{yaw}-{label}'
     if verify:assert (OUT/f'{stem}.png').read_bytes()==result.png
     else:(OUT/f'{stem}.png').write_bytes(result.png)
     row={'mode':mode,'pose':pose,'yaw':yaw,'label':label,'png_sha256':digest(result.png),'size':[result.width,result.height],'offset':list(result.offset),'equals_young':sig(result)==sig(target),'pixels_vs_young':difference(result,target)}
     report['renders'].append(row)
     if label=='full':
      assert sig(result)==sig(target)
      previous=next(x for x in prior['renders'] if (x['mode'],x['pose'],x['yaw'],x['label'])==(mode,pose,yaw,'all-non-speckle'))
      assert digest(result.png)==previous['png_sha256']
   print(f'{mode}/{pose}: 12 single/group reversion controls in two views pass',flush=True)
 if verify:assert report==old;print('FULL REPLAY PASS',flush=True)
 else:MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');run(p.parse_args().verify)
