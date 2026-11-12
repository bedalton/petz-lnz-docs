"""UPDATE-012: current-build age arithmetic, edited resources and dependency routing."""
import argparse,asyncio,base64,json,sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.appearance.age import aged_appearance
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT,digest,provenance
from young_layer_edits import check
import revalidate_young_upgrade as replay
OUT=ROOT/'scratch/research/update-012';MANIFEST=ROOT/'experiments/update-012.json'
async def run(verify):
 previous=json.loads(MANIFEST.read_text()) if verify else None
 if not verify:OUT.mkdir(parents=True,exist_ok=False)
 replay.OUT=OUT
 priors={u:json.loads((ROOT/f'experiments/{u}.json').read_text()) for u in ('young-003','young-004')}
 report={'provenance':provenance(),'backend':'installed direct renderer; local stdio MCP; independent age arithmetic','prior_manifests':{u:digest((ROOT/f'experiments/{u}.json').read_bytes()) for u in priors},'numeric':[],'renders':[],'routing':[],'mcp':[],'relationships':[]}
 for version in ('petz3','petz4','petz5'):
  resolver=ResourceResolver((ROOT/'games'/version,),game_version=version)
  for species,file in [('Dogz','Scottie.dog'),('Catz','Siamese.cat')]:
   path=f'Resource/{species}/{file}';args={'pose':'standing','seed':41,'fatness':50}
   adult=load_breed_assets(resolver,path,look='adult',age=100,**args).appearance;young=load_breed_assets(resolver,path,look='puppy',age=0,**args).appearance
   for age in range(101):
    actual=aged_appearance(adult,young,age) if age not in (0,11,12,13,50,99,100) else load_breed_assets(resolver,path,look='age',age=age,**args).appearance;n=check(actual,adult,young,age)
    row={'version':version,'species':species,'age':age,'assertions':n,'pet_scale':actual.pet_scale,'ball_scale':actual.ball_scale}
    assert row==next(x for x in priors['young-003']['numeric'] if (x['version'],x['species'],x['age'])==(version,species,age));report['numeric'].append(row)
   print(f'{version}/{species}: 101 independent arithmetic cases (7 full-loader boundaries)',flush=True)
 observations={}
 for unit,prior in priors.items():
  resolver=ResourceResolver((ROOT/'games/petz4',ROOT/f'scratch/research/{unit}'))
  for copied in prior['copies']:
   assert digest((ROOT/f'scratch/research/{unit}'/copied['path']).read_bytes())==copied['sha256']
   if 'source' in copied:source=ROOT/copied['source']
   else:source=ROOT/f"games/petz4/Resource/{copied['species']}/"/('Scottie.dog' if copied['species']=='Dogz' else 'Siamese.cat')
   assert digest(source.read_bytes())==copied['source_sha256']
  if unit=='young-003':
   for old in prior['renders']:
    copied=next(c for c in prior['copies'] if (c['species'],c['mode'])==(old['species'],old['mode']))
    args={'path':copied['path'],'pose':'standing','look':old['look'],'age':old['age'],'seed':41,'fatness':50}
    assets=load_breed_assets(resolver,args.pop('path'),**args);result=render_portrait(assets,yaw=old['yaw']*256//360)
    stem=f"{old['species']}-{old['mode']}-{old['look']}-{old['age']}-{old['yaw']}"
    row={k:old[k] for k in ('species','mode','look','age','yaw')};row.update(unit=unit,**replay.output_record(result.png,result.offset,old,ROOT/f'scratch/research/{unit}'/f'{stem}.png',f'{unit}-{stem}',verify))
    assert assets.appearance.balls[copied['head']].size==old['head_size'] and assets.appearance.balls[copied['head']].color==old['head_color']
    report['renders'].append(row);observations[unit,old['species'],old['mode'],old['look'],old['age'],old['yaw']]=result
   for rel in prior['relationships']:
    a=observations[unit,rel['species'],rel['mode'],rel['look'],rel['age'],rel['yaw']];b=observations[unit,rel['species'],'control',rel['look'],rel['age'],rel['yaw']]
    report['relationships'].append({'unit':unit,**rel,'equal':a.png==b.png})
  else:
   for old in prior['cases']:
    controls=dict(old['controls']);path=controls.pop('path');controls.pop('yaw_degrees')
    try:assets=load_breed_assets(resolver,path,**controls)
    except Exception as exc:
     assert not old['success'],old;assert type(exc).__name__==old['error_type'] and str(exc)==old['error']
     report['routing'].append({'species':old['species'],'mode':old['mode'],'label':old['label'],'success':False,'error_type':type(exc).__name__,'error':str(exc)})
    else:
     assert old['success'];report['routing'].append({'species':old['species'],'mode':old['mode'],'label':old['label'],'success':True,'layers':[x.label for x in assets.preview.layers]})
     for oldrender in old['renders']:
      yaw=oldrender['yaw'];result=render_portrait(assets,yaw=yaw*256//360);stem=f"{old['species']}-{old['mode']}-{old['label']}-{yaw}"
      row={'unit':unit,'species':old['species'],'mode':old['mode'],'label':old['label'],'yaw':yaw,**replay.output_record(result.png,result.offset,oldrender,ROOT/f'scratch/research/{unit}'/f'{stem}.png',f'{unit}-{stem}',verify)}
      report['renders'].append(row);observations[unit,old['species'],old['mode'],old['label'],yaw]=result
   for rel in prior['relationships']:
    a=observations[unit,rel['species'],rel['mode'],rel['label'],rel['yaw']];b=observations[unit,rel['species'],'control',rel['baseline'],rel['yaw']]
    report['relationships'].append({'unit':unit,**rel,'equal':a.png==b.png})
  transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/f'scratch/research/{unit}')])
  async with Client(transport) as client:
   for old in prior['mcp']:
    response=await client.call_tool('render_pet',old['controls'],raise_on_error=False);expected=old.get('success',True);assert not response.is_error==expected
    row={'unit':unit,'controls':old['controls'],'success':not response.is_error}
    if not response.is_error:
     png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
     if unit=='young-003':
      copied=next(x for x in prior['copies'] if x['path']==old['controls']['path']);result=observations[unit,copied['species'],copied['mode'],old['controls']['look'],old['controls']['age'],0]
     else:result=observations[unit,old['species'],old['mode'],old['label'],0]
     assert png==result.png;row['png_sha256']=digest(png)
    else:row['error_text']=[c.text for c in response.content if c.type=='text']
    report['mcp'].append(row)
  print(f'{unit}: direct and MCP resource replay complete',flush=True)
 report['script_sha256']=digest(__import__('pathlib').Path(__file__).read_bytes());report['helper_sha256']=digest((ROOT/'tools/revalidate_young_upgrade.py').read_bytes())
 report['summary']={'numeric':len(report['numeric']),'renders':len(report['renders']),'changed_rgba':sum(not r['same_aligned_rgba'] for r in report['renders']),'routing_cases':len(report['routing']),'routing_errors':sum(not r['success'] for r in report['routing']),'mcp_requests':len(report['mcp']),'mcp_matches':sum(r['success'] for r in report['mcp']),'relationships':len(report['relationships']),'failed_relationships':sum(not r['equal'] for r in report['relationships'])}
 if verify:assert report==previous;print('FULL REPLAY PASS',flush=True)
 else:MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report['summary'],indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
