"""Rebuild a private old/new endpoint correction sheet from recorded evidence."""
import json
from PIL import Image,ImageDraw
from young_breed_probe import ROOT,digest
OUT=ROOT/'scratch/research/update-011'
def build():
 report=json.loads((ROOT/'experiments/update-011.json').read_text())
 labels=[('young-005','none'),('young-005','young'),('young-005','balls-add_balls'),('young-006','outline14-outline38-add-tail'),('young-007','line-11')]
 canvas=Image.new('RGB',(620,5*150+34),'#d9e1e8');draw=ImageDraw.Draw(canvas)
 draw.text((245,8),'4c4d3df',fill='black');draw.text((365,8),'49c7f62',fill='black');draw.text((485,8),'changed RGBA',fill='black')
 for i,(unit,label) in enumerate(labels):
  row=next(r for r in report['renders'] if (r['unit'],r['mode'],r['pose'],r['yaw'],r['label'])==(unit,'missing-young','lying',0,label))
  stem=f'missing-young-lying-0-{label}'
  old=Image.open(ROOT/f'scratch/research/{unit}/{stem}.png').convert('RGBA');new=Image.open(OUT/f'{unit}-{stem}.png').convert('RGBA')
  assert old.size==new.size and row['offset']==[32,48]
  draw.text((5,45+i*150),f'{unit}\n{label}\nnew vs young: {row["pixels_vs_young"]}',fill='black')
  mask=Image.new('RGBA',old.size);mask.putdata([(255,20,70,255) if a!=b else (0,0,0,0) for a,b in zip(old.getdata(),new.getdata())])
  for j,im in enumerate((old,new,mask)):canvas.paste(im,(245+j*120,40+i*150),im)
 path=OUT/'endpoint-correction-sheet.png';canvas.save(path)
 metadata={'path':str(path.relative_to(ROOT)),'sha256':digest(path.read_bytes()),'cells':labels,'scale':1,'alignment':'identical recorded 32,48 offsets and dimensions; no resampling'}
 (OUT/'sheet.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps(metadata,indent=2))
if __name__=='__main__':build()
