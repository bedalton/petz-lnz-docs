"""UPDATE-011: replay endpoint substitutions without assuming old pixel conclusions."""
import argparse,asyncio,base64,itertools,json,sys
from dataclasses import replace
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT,digest,provenance
from young_endpoint_attribution import difference,sig
from young_endpoint_fields import FACTORS,modify
import revalidate_young_upgrade as replay
OUT=ROOT/'scratch/research/update-011';MANIFEST=ROOT/'experiments/update-011.json'
def entry_variants(a,b):
 full=modify(a,b,FACTORS);result={'full':full}
 for i in range(23,29):
  rows=list(full.add_balls);rows[i]=a.add_balls[i];result[f'add-{i}']=replace(full,add_balls=tuple(rows))
 result['add-count']=replace(full,add_balls=full.add_balls[:29]+a.add_balls[29:])
 for i in (11,12,13,14):
  rows=list(full.lines);rows[i]=a.lines[i];result[f'line-{i}']=replace(full,lines=tuple(rows))
 return result
async def run(verify):
 previous=json.loads(MANIFEST.read_text()) if verify else None
 if not verify:OUT.mkdir(parents=True,exist_ok=False)
 replay.OUT=OUT
 priors={u:json.loads((ROOT/f'experiments/{u}.json').read_text()) for u in ('young-005','young-006','young-007')}
 source=priors['young-005']['inputs'];resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'))
 for value in source['variants'].values():assert digest((ROOT/'scratch/research/young-002'/value['path']).read_bytes())==value['sha256']
 report={'provenance':provenance(),'backend':'direct installed renderer with immutable appearance substitutions; local stdio MCP baseline checks','inputs':source,'prior_manifests':{u:digest((ROOT/f'experiments/{u}.json').read_bytes()) for u in priors},'renders':[],'fixtures':[],'mcp':[]};baselines={}
 for mode,variant in source['variants'].items():
  for pose in ('standing','sitting','lying'):
   age=load_saved_assets(resolver,variant['path'],pose=pose,look='age',age=12);young=load_saved_assets(resolver,variant['path'],pose=pose,look='puppy',age=12);a,b=age.appearance,young.appearance
   for yaw in (0,90):
    target=render_portrait(young,yaw=yaw*256//360);baseline=render_portrait(age,yaw=yaw*256//360)
    baselines[mode,pose,yaw,'age']=baseline;baselines[mode,pose,yaw,'puppy']=target
    for unit,prior in priors.items():
     olds=[r for r in prior['renders'] if (r['mode'],r['pose'],r['yaw'])==(mode,pose,yaw)]
     if not olds:continue
     variants=entry_variants(a,b) if unit=='young-007' else {}
     current=[]
     for old in olds:
      if unit=='young-005':
       groups=old['groups'];label='young' if groups=='forced-young' else '-'.join(groups) or 'none'
       appearance=b if groups=='forced-young' else replace(a,**{g:getattr(b,g) for g in groups})
      else:
       label=old['label']
       if unit=='young-007':appearance=variants[label]
       elif label=='speckle-only':appearance=replace(a,balls=tuple(replace(x,speckle_color=y.speckle_color) for x,y in zip(a.balls,b.balls)))
       elif label=='paints-only':appearance=replace(a,paint_balls=b.paint_balls)
       else:appearance=modify(a,b,FACTORS if label=='all-non-speckle' else (() if label=='none' else label.split('-'))) if label in ('all-non-speckle','none') else None
       # Hyphens occur inside factor names: reconstruct the authored subset label.
       if appearance is None:
        factors=next(g for n in range(6) for g in itertools.combinations(FACTORS,n) if '-'.join(g)==label);appearance=modify(a,b,factors)
      result=render_portrait(replace(age,appearance=appearance),yaw=yaw*256//360)
      oldstem=f'{mode}-{pose}-{yaw}-{label}';stem=f'{unit}-{oldstem}'
      row={'unit':unit,'mode':mode,'pose':pose,'yaw':yaw,'label':label,**replay.output_record(result.png,result.offset,old,ROOT/f'scratch/research/{unit}'/f'{oldstem}.png',stem,verify),'equals_young':sig(result)==sig(target),'pixels_vs_young':difference(result,target),'equals_age':sig(result)==sig(baseline)}
      if 'equals_young' in old:row['historical_equals_young']=old['equals_young']
      if 'pixels_vs_young' in old:row['historical_pixels_vs_young']=old['pixels_vs_young']
      report['renders'].append(row);current.append(row)
     if unit in ('young-005','young-006'):
      subsets=[r for r in current if r['label'] not in ('young','speckle-only','paints-only','all-non-speckle') and r['equals_young']]
      factors=[f.name for f in __import__('dataclasses').fields(a) if getattr(a,f.name)!=getattr(b,f.name)] if unit=='young-005' else FACTORS
      def selected(label):
       return next(g for n in range(len(factors)+1) for g in itertools.combinations(factors,n) if ('-'.join(g) or 'none')==label)
      suff=[selected(r['label']) for r in subsets];minimal=[list(g) for g in suff if not any(set(h)<set(g) for h in suff)]
      oldfixture=next(f for f in prior['fixtures'] if (f['mode'],f['pose'])==(mode,pose));oldview=next(v for v in oldfixture['views'] if v['yaw']==yaw)
      report['fixtures'].append({'unit':unit,'mode':mode,'pose':pose,'yaw':yaw,'minimal_sufficient_substitutions':minimal,'historical_minimal':oldview['minimal_sufficient_substitutions'],'same_minimal':sorted(minimal)==sorted(oldview['minimal_sufficient_substitutions']),'baseline_pixels_vs_young':difference(baseline,target),'historical_baseline_pixels_vs_young':oldview['baseline_pixels_vs_young']})
   print(f'{mode}/{pose}: list, field and entry replay complete',flush=True)
 transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/young-002')])
 async with Client(transport) as client:
  for mode,variant in source['variants'].items():
   for pose in ('standing','sitting','lying'):
    for look in ('age','puppy'):
     args={'path':variant['path'],'pose':pose,'look':look,'age':12,'yaw_degrees':0};response=await client.call_tool('render_pet',args);assert not response.is_error
     png=base64.b64decode(next(c.data for c in response.content if c.type=='image'));assert png==baselines[mode,pose,0,look].png
     report['mcp'].append({'controls':args,'png_sha256':digest(png)})
 report['script_sha256']=digest(__import__('pathlib').Path(__file__).read_bytes())
 report['helper_sha256']=digest((ROOT/'tools/revalidate_young_upgrade.py').read_bytes())
 report['summary']={'renders':len(report['renders']),'changed_rgba':sum(not r['same_aligned_rgba'] for r in report['renders']),'endpoint_equality_changes':sum(r['equals_young']!=r['historical_equals_young'] for r in report['renders'] if 'historical_equals_young' in r),'changed_minimal_sets':sum(not f['same_minimal'] for f in report['fixtures']),'mcp_matches':len(report['mcp'])}
 if verify:assert report==previous;print('FULL REPLAY PASS',flush=True)
 else:MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report['summary'],indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
