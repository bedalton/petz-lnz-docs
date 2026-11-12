"""Independent decoded-image/minimal-set audit of YOUNG-008."""
import itertools, json
from PIL import Image, ImageDraw
from young_breed_probe import ROOT, digest, provenance
from check_young_upgrade_session import independent_difference

def run():
    path=ROOT/'experiments/young-008.json'; report=json.loads(path.read_text())
    prior_path=ROOT/'experiments/update-011.json'; prior=json.loads(prior_path.read_text())
    assert digest(prior_path.read_bytes())==report['prior_manifest_sha256']
    assert provenance()==report['provenance']
    assert digest((ROOT/'tools/young_tail_interactions.py').read_bytes())==report['script_sha256']
    out=ROOT/'scratch/research/young-008'; checked=0; links=0; influences=[]
    canvas=Image.new('RGB',(720,12*120+30),'#d9e1e8');draw=ImageDraw.Draw(canvas)
    for x,label in ((250,'No tail edits'),(390,'Minimal subset'),(530,'Forced young')):draw.text((x,8),label,fill='black')
    for index, fixture in enumerate(report['fixtures']):
        key=tuple(fixture[k] for k in ('mode','pose','yaw'))
        rows=[r for r in report['renders'] if tuple(r[k] for k in ('mode','pose','yaw'))==key]
        assert sorted(r['mask'] for r in rows)==list(range(128))
        target=next(r for r in prior['renders'] if (r['unit'],r['mode'],r['pose'],r['yaw'],r['label'])==('young-005',*key,'young'))
        target_path=ROOT/'scratch/research/update-011'/f"young-005-{key[0]}-{key[1]}-{key[2]}-young.png"
        assert digest(target_path.read_bytes())==target['png_sha256']==fixture['target_sha256']
        for row in rows:
            image_path=out/row['file'];assert digest(image_path.read_bytes())==row['png_sha256']
            assert list(Image.open(image_path).size)==row['size']
            n=independent_difference(image_path,row['offset'],target_path,target['offset'])
            assert n==row['pixels_vs_young']
            assert (n==0)==row['equals_young']
            assert row['selected']==[f for i,f in enumerate(report['factors']) if row['mask']&(1<<i)]
            checked+=1
        sufficient={tuple(r['selected']) for r in rows if r['equals_young']}
        minimal=[s for s in sufficient if not any(set(t)<set(s) for t in sufficient)]
        assert sorted(map(list,minimal))==sorted(fixture['minimal_subsets'])
        assert rows[127]['png_sha256']==fixture['prior_full_sha256'];links+=1
        violations=[]
        for a in rows:
            if not a['equals_young']:continue
            for b in rows:
                if set(a['selected'])<=set(b['selected']) and not b['equals_young']:violations.append([a['mask'],b['mask']])
        assert violations==fixture['monotonicity_violations']
        signatures={}
        for r in rows:
            im=Image.open(out/r['file']).convert('RGBA')
            signatures[r['mask']]=(im.size,r['offset'],im.tobytes())
        for bit,factor in enumerate(report['factors']):
            pairs=[(r,rows[r['mask']|(1<<bit)]) for r in rows if not r['mask']&(1<<bit)]
            influences.append({'mode':key[0],'pose':key[1],'yaw':key[2],'factor':factor,
                'different_rgba_pairs':sum(signatures[a['mask']]!=signatures[b['mask']] for a,b in pairs),
                'gained_equalities':sum(not a['equals_young'] and b['equals_young'] for a,b in pairs),
                'lost_equalities':sum(a['equals_young'] and not b['equals_young'] for a,b in pairs)})
        chosen=next(r for r in rows if r['mask']==fixture['minimal_masks'][0])
        draw.text((5,index*120+38),f'{key[0]} {key[1]} yaw{key[2]}\n'+','.join(chosen['selected']),fill='black')
        for j,(p,offset) in enumerate(((out/rows[0]['file'],rows[0]['offset']),(out/chosen['file'],chosen['offset']),(target_path,target['offset']))):
            im=Image.open(p).convert('RGBA');canvas.paste(im,(280+j*140-offset[0],index*120+100-offset[1]),im)
    sheet=out/'minimal-sheet.png';canvas.save(sheet)
    result={'manifest_sha256':digest(path.read_bytes()),'checker_sha256':digest(__import__('pathlib').Path(__file__).read_bytes()),
            'influences':influences,'independent_rgba_checks':checked,'prior_links':links,'sheet_sha256':digest(sheet.read_bytes()),'sheet_scale':1,
            'pngs':{r['file']:r['png_sha256'] for r in report['renders']}}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: {checked} independent RGBA checks; {links} prior links; minimal sets and monotonicity verified')
if __name__=='__main__':run()
