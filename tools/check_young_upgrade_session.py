"""Independent integrity and pixel audit for UPDATE-010/011/012."""
import asyncio,base64,io,json,subprocess,sys
from pathlib import Path
from PIL import Image
from fastmcp import Client
from young_breed_probe import ROOT,digest,provenance
OUT=ROOT/'scratch/research/young-upgrade-session'
def image_bytes(path):
 im=Image.open(path).convert('RGBA');return im.size,im.tobytes()
def independent_difference(ap,ao,bp,bo):
 (aw,ah),a=image_bytes(ap);(bw,bh),b=image_bytes(bp)
 left=min(-ao[0],-bo[0]);top=min(-ao[1],-bo[1]);right=max(aw-ao[0],bw-bo[0]);bottom=max(ah-ao[1],bh-bo[1]);count=0
 for y in range(top,bottom):
  for x in range(left,right):
   ax,ay=x+ao[0],y+ao[1];bx,by=x+bo[0],y+bo[1]
   av=a[(ay*aw+ax)*4:(ay*aw+ax+1)*4] if 0<=ax<aw and 0<=ay<ah else bytes(4)
   bv=b[(by*bw+bx)*4:(by*bw+bx+1)*4] if 0<=bx<bw and 0<=by<bh else bytes(4)
   count+=av!=bv
 return count
async def run():
 OUT.mkdir(parents=True,exist_ok=True);reports={u:json.loads((ROOT/f'experiments/{u}.json').read_text()) for u in ('update-010','update-011','update-012')}
 current=provenance();counts={};current_paths={}
 for unit,report in reports.items():
  assert report['provenance']==current
  for prior,h in report['prior_manifests'].items():assert digest((ROOT/f'experiments/{prior}.json').read_bytes())==h
  script={'update-010':'revalidate_young_upgrade.py','update-011':'revalidate_young_attribution.py','update-012':'revalidate_young_routing.py'}[unit]
  assert digest((ROOT/'tools'/script).read_bytes())==report['script_sha256']
  if 'helper_sha256' in report:assert digest((ROOT/'tools/revalidate_young_upgrade.py').read_bytes())==report['helper_sha256']
  rows=report.get('fresh',[])+report.get('saved',[])+report.get('renders',[])
  for row in rows:
   if unit=='update-010':
    if 'version' in row:prior='young-001';stem=f"{row['version']}-{row['species']}-{row['label']}"
    else:prior='young-002';stem=f"{row['name']}-{row['mode']}-{row['look']}-{row['age']}-{row['yaw_degrees']}"
    newstem=stem
   else:
    prior=row['unit']
    if prior in ('young-005','young-006','young-007'):stem=f"{row['mode']}-{row['pose']}-{row['yaw']}-{row['label']}"
    elif prior=='young-003':stem=f"{row['species']}-{row['mode']}-{row['look']}-{row['age']}-{row['yaw']}"
    else:stem=f"{row['species']}-{row['mode']}-{row['label']}-{row['yaw']}"
    newstem=f'{prior}-{stem}'
   path=ROOT/f'scratch/research/{unit}/{newstem}.png';oldpath=ROOT/f'scratch/research/{prior}/{stem}.png'
   assert digest(path.read_bytes())==row['png_sha256'];assert digest(oldpath.read_bytes())==row['historical_png_sha256']
   size,pixels=image_bytes(path);assert list(size)==row['size'] and digest(pixels)==row['rgba_sha256']
   # Recover old offset from historical manifest; never assume equal framing.
   if prior=='young-001':old=next(r for r in first['cases'] if (r['version'],r['species'],r['label'])==(row['version'],row['species'],row['label']))
   elif prior=='young-002':old=next(r for r in second['cases'] if all(r[k]==row[k] for k in ('name','mode','look','age','yaw_degrees')))
   elif prior in ('young-005','young-006','young-007'):old=next(r for r in priors[prior]['renders'] if (r['mode'],r['pose'],r['yaw'],('-'.join(r['groups']) or 'none') if isinstance(r.get('groups'),list) else ('young' if r.get('groups')=='forced-young' else r.get('label')))==(row['mode'],row['pose'],row['yaw'],row['label']))
   elif prior=='young-003':old=next(r for r in priors[prior]['renders'] if all(r[k]==row[k] for k in ('species','mode','look','age','yaw')))
   else:case=next(c for c in priors[prior]['cases'] if all(c[k]==row[k] for k in ('species','mode','label')));old=next(r for r in case['renders'] if r['yaw']==row['yaw'])
   n=independent_difference(path,row['offset'],oldpath,old['offset']);assert n==row['pixels_vs_historical']
   oldsize,oldpixels=image_bytes(oldpath);assert row['same_aligned_rgba']==(list(size)==list(oldsize) and row['offset']==old['offset'] and pixels==oldpixels)
   current_paths[unit,newstem]=path
  counts[unit]={'pngs':len(rows),'independent_historical_rgba_checks':len(rows)};print(f'{unit}: {len(rows)} independent image checks',flush=True)
 cross_version=0
 for r in reports['update-010']['fresh']:
  if r['version']=='petz4':continue
  peer=next(x for x in reports['update-010']['fresh'] if (x['version'],x['species'],x['label'])==('petz4',r['species'],r['label']))
  assert (r['size'],r['offset'],r['rgba_sha256'])==(peer['size'],peer['offset'],peer['rgba_sha256']);cross_version+=1
 cross_unit=0
 for r in reports['update-011']['renders']:
  if r['unit']!='young-005' or r['pose']!='standing' or r['label'] not in ('none','young'):continue
  look,age=('age',12) if r['label']=='none' else ('puppy',0)
  peer=next(x for x in reports['update-010']['saved'] if (x['name'],x['mode'],x['look'],x['age'],x['yaw_degrees'])==('Fuzzkin',r['mode'],look,age,r['yaw']))
  assert (r['size'],r['offset'],r['rgba_sha256'])==(peer['size'],peer['offset'],peer['rgba_sha256']);cross_unit+=1
 for r in reports['update-012']['renders']:
  if r['unit']!='young-003' or r['mode']!='control':continue
  label=f"{r['look']}-{r['age']}-standing-{r['yaw']}"
  peer=next(x for x in reports['update-010']['fresh'] if (x['version'],x['species'],x['label'])==('petz4',r['species'],label))
  assert (r['size'],r['offset'],r['rgba_sha256'])==(peer['size'],peer['offset'],peer['rgba_sha256']);cross_unit+=1
 # Independently compare all endpoint interventions against current forced-young targets.
 endpoint=reports['update-011'];endpoint_checks=0
 for row in endpoint['renders']:
  target=next(r for r in endpoint['renders'] if (r['unit'],r['mode'],r['pose'],r['yaw'],r['label'])==('young-005',row['mode'],row['pose'],row['yaw'],'young'))
  stem=f"{row['unit']}-{row['mode']}-{row['pose']}-{row['yaw']}-{row['label']}";targetstem=f"young-005-{row['mode']}-{row['pose']}-{row['yaw']}-young"
  n=independent_difference(current_paths['update-011',stem],row['offset'],current_paths['update-011',targetstem],target['offset']);assert n==row['pixels_vs_young'] and row['equals_young']==(n==0);endpoint_checks+=1
 original=json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True));assert all(x['ok'] for x in original['checks'])
 http=[]
 async with Client('http://127.0.0.1:8765/mcp') as client:
  assert len(await client.list_tools())==6;cap=await client.call_tool('get_capabilities');assert not cap.is_error
  for species in ('Dogz','Catz'):
   for label in ('age-12-standing-0','adult-100-standing-0'):
    row=next(r for r in reports['update-010']['fresh'] if (r['version'],r['species'],r['label'])==('petz4',species,label))
    response=await client.call_tool('render_pet',row['controls']);assert not response.is_error
    png=base64.b64decode(next(c.data for c in response.content if c.type=='image'));assert digest(png)==row['png_sha256'];http.append({'controls':row['controls'],'png_sha256':digest(png)})
 scripts=['revalidate_young_upgrade.py','revalidate_young_attribution.py','revalidate_young_routing.py','young_upgrade_sheet.py','check_young_upgrade_session.py']
 report={'provenance':current,'units':counts,'endpoint_rgba_checks':endpoint_checks,'cross_version_links':cross_version,'cross_unit_links':cross_unit,'http_matches':http,'originals':original,'manifests':{u:digest((ROOT/f'experiments/{u}.json').read_bytes()) for u in reports},'scripts':{p:digest((ROOT/'tools'/p).read_bytes()) for p in scripts},'sheet':json.loads((ROOT/'scratch/research/update-011/sheet.json').read_text())}
 assert digest((ROOT/report['sheet']['path']).read_bytes())==report['sheet']['sha256']
 (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print('SESSION AUDIT PASS',flush=True)
if __name__=='__main__':
 first=json.loads((ROOT/'experiments/young-001.json').read_text());second=json.loads((ROOT/'experiments/young-002.json').read_text());priors={u:json.loads((ROOT/f'experiments/{u}.json').read_text()) for u in ('young-003','young-004','young-005','young-006','young-007')};asyncio.run(run())
