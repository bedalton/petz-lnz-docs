"""Hash-check and align routing and field-attribution research sheets."""
import json
from young_breed_probe import ROOT,digest
from young_sheets import draw
OUT=ROOT/'scratch/research/young-continuation';OUT.mkdir(parents=True,exist_ok=True)
records=[]
r=json.loads((ROOT/'experiments/young-004.json').read_text());source=ROOT/'scratch/research/young-004'
for species in ('Dogz','Catz'):
 entries=[]
 for row,yaw in enumerate((0,90)):
  for col,(mode,label) in enumerate((('control','adult'),('control','young'),('path','young'),('branch','branch-valid'),('branch','branch-rescued'))):
   case=next(x for x in r['cases'] if (x['species'],x['mode'],x['label'])==(species,mode,label))
   item=next(x for x in case['renders'] if x['yaw']==yaw)
   entries.append((row,col,source/f'{species}-{mode}-{label}-{yaw}.png',f'{mode}/{label}\nyaw{yaw}',item))
 records.append(draw(entries,5,OUT/f'{species}-routing-sheet.png'))
r=json.loads((ROOT/'experiments/young-006.json').read_text());prior=json.loads((ROOT/'experiments/young-005.json').read_text());source=ROOT/'scratch/research/young-006'
for mode in ('missing-adult','missing-young'):
 entries=[]
 for row,(pose,yaw) in enumerate((p,y) for p in ('standing','sitting','lying') for y in (0,90)):
  for col,label in enumerate(('none','outline14-outline38','outline14-outline38-add-tail','young')):
   if label=='young':
    item=next(x for x in prior['renders'] if (x['mode'],x['pose'],x['yaw'],x['groups'])==(mode,pose,yaw,'forced-young'))
    path=ROOT/f'scratch/research/young-005/{mode}-{pose}-{yaw}-young.png'
   else:
    item=next(x for x in r['renders'] if (x['mode'],x['pose'],x['yaw'],x['label'])==(mode,pose,yaw,label))
    path=source/f'{mode}-{pose}-{yaw}-{label}.png'
   entries.append((row,col,path,f'{pose}/yaw{yaw}\n{label}',item))
 records.append(draw(entries,4,OUT/f'{mode}-field-sheet.png'))
(OUT/'sheets.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
