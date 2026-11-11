"""Rebuild native-resolution age/edit sheets from hash-checked private PNGs."""
import argparse,json
from PIL import Image,ImageDraw
from young_breed_probe import ROOT,digest

def draw(entries,columns,target):
    loaded=[]
    for row,col,path,label,record in entries:
        raw=path.read_bytes();assert digest(raw)==record['png_sha256']
        im=Image.open(path).convert('RGBA');loaded.append((row,col,im,label,record['offset']))
    left=min(-o[0] for _,_,_,_,o in loaded);top=min(-o[1] for _,_,_,_,o in loaded)
    right=max(im.width-o[0] for _,_,im,_,o in loaded);bottom=max(im.height-o[1] for _,_,im,_,o in loaded)
    w=max(112,right-left+12);h=bottom-top+42;rows=1+max(r for r,_,_,_,_ in loaded)
    sheet=Image.new('RGB',(w*columns,h*rows),(215,215,215));d=ImageDraw.Draw(sheet)
    for row,col,im,label,o in loaded:
        x,y=col*w,row*h;d.text((x+3,y+3),label,fill='black');sheet.paste(im,(x+6-left-o[0],y+34-top-o[1]),im)
    sheet.save(target);return {'path':str(target.relative_to(ROOT)),'sha256':digest(target.read_bytes())}
def main():
    p=argparse.ArgumentParser();p.add_argument('--edits-only',action='store_true');args=p.parse_args();records=[]
    if not args.edits_only:
        report=json.loads((ROOT/'experiments/young-001.json').read_text());out=ROOT/'scratch/research/young-001'
        for species in ('Dogz','Catz'):
            labels=[f'age-{a}-standing' for a in (0,6,11,12,13,50,99,100)]+['adult-100-standing','puppy-0-standing'];entries=[]
            for row,yaw in enumerate((0,90)):
                for col,label in enumerate(labels):
                    item=next(x for x in report['cases'] if (x['version'],x['species'],x['label'])==('petz4',species,f'{label}-{yaw}'))
                    entries.append((row,col,out/f'petz4-{species}-{label}-{yaw}.png',label.replace('-standing','')+f'\nyaw{yaw}',item))
            records.append(draw(entries,len(labels),out/f'{species}-age-sheet.png'))
    report=json.loads((ROOT/'experiments/young-003.json').read_text());out=ROOT/'scratch/research/young-003'
    for species in ('Dogz','Catz'):
        entries=[]
        for row,(look,age,yaw) in enumerate((('age',12,0),('age',12,90),('puppy',0,0),('puppy',0,90))):
            for col,mode in enumerate(('control','size','color')):
                item=next(x for x in report['renders'] if (x['species'],x['mode'],x['look'],x['age'],x['yaw'])==(species,mode,look,age,yaw))
                entries.append((row,col,out/f'{species}-{mode}-{look}-{age}-{yaw}.png',f'{mode} {look}{age} yaw{yaw}\nhead size{item["head_size"]} color{item["head_color"]}',item))
        records.append(draw(entries,3,out/f'{species}-edit-sheet.png'))
    dest=ROOT/'scratch/research/young-session';dest.mkdir(parents=True,exist_ok=True);(dest/'sheets.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
