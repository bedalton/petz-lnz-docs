"""Independent pixels/links audit for YOUNG-009/010."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from young_breed_probe import ROOT,digest,provenance
from check_young_upgrade_session import independent_difference

def run(unit):
    mp=ROOT/f'experiments/{unit}.json';report=json.loads(mp.read_text());out=ROOT/f'scratch/research/{unit}'
    priorpath=ROOT/'experiments/young-008.json';prior=json.loads(priorpath.read_text())
    assert digest(priorpath.read_bytes())==report['prior_manifest_sha256']
    assert provenance()==report['provenance']
    script='young_count_controls.py' if unit=='young-009' else 'young_tail_yaws.py'
    assert digest((ROOT/'tools'/script).read_bytes())==report['script_sha256']
    rows=report['renders'];checks=0;links=0
    for row in rows:
        path=out/row['file'];assert digest(path.read_bytes())==row['png_sha256']
        assert list(Image.open(path).size)==row['size']
        key=tuple(row[k] for k in ('mode','pose','yaw'))
        references={'short':'prefix-29','long':'prefix-32','young':'prefix-32' if row['mode']=='missing-adult' else 'prefix-29'} if unit=='young-009' else {'young':'young','full':'full','unomit_full':'unomit-full'}
        for metric,label in references.items():
            target=next(r for r in rows if tuple(r[k] for k in ('mode','pose','yaw'))==key and r['label']==label)
            n=independent_difference(path,row['offset'],out/target['file'],target['offset'])
            assert n==row[f'pixels_vs_{metric}'];checks+=1
            if metric=='young' and 'equals_young' in row:assert (n==0)==row['equals_young']
    for fixture in report['fixtures']:
        key=tuple(fixture[k] for k in ('mode','pose','yaw'))
        if unit=='young-009':
            for method,field in [('omit','omission'),('zero','zero')]:
                for endpoint in ('short','long'):
                    masks=[m for m in range(8) if next(r for r in rows if tuple(r[k] for k in ('mode','pose','yaw'))==key and r['label']==f'{method}-{m}')[f'pixels_vs_{endpoint}']==0]
                    assert masks==fixture[f'{field}_matches_{endpoint}']
            p=next(f for f in prior['fixtures'] if tuple(f[k] for k in ('mode','pose','yaw'))==key)
            assert p['prior_full_sha256']==fixture['prior_endpoint_sha256'];links+=1
        elif fixture['yaw'] in (0,90):
            p=next(r for r in prior['renders'] if tuple(r[k] for k in ('mode','pose','yaw'))==key and r['mask']==127)
            r=next(r for r in rows if tuple(r[k] for k in ('mode','pose','yaw'))==key and r['label']=='full')
            assert p['png_sha256']==r['png_sha256'];links+=1
    # Native pixels, position each pet by its recorded origin with no resampling.
    if unit=='young-009':
        fixtures=[f for f in report['fixtures'] if f['yaw']==0]
        labels=['prefix-29','prefix-32','omit-1','omit-6','zero-0']
    else:
        fixtures=[f for f in report['fixtures'] if f['pose']=='lying']
        labels=['full','revert26','unomit-full','unomit-revert26']
    canvas=Image.new('RGB',(220+140*len(labels),30+120*len(fixtures)),'#d9e1e8');draw=ImageDraw.Draw(canvas)
    for j,label in enumerate(labels):draw.text((220+j*140,8),label,fill='black')
    for i,fixture in enumerate(fixtures):
        key=tuple(fixture[k] for k in ('mode','pose','yaw'));draw.text((5,40+i*120),' '.join(map(str,key)),fill='black')
        for j,label in enumerate(labels):
            row=next(r for r in rows if tuple(r[k] for k in ('mode','pose','yaw'))==key and r['label']==label)
            im=Image.open(out/row['file']).convert('RGBA');canvas.paste(im,(250+j*140-row['offset'][0],100+i*120-row['offset'][1]),im)
    sheet=out/'control-sheet.png';canvas.save(sheet)
    result={'manifest_sha256':digest(mp.read_bytes()),'checker_sha256':digest(Path(__file__).read_bytes()),
            'independent_rgba_comparisons':checks,'pngs':len(rows),'prior_links':links,'sheet_sha256':digest(sheet.read_bytes()),'sheet_scale':1}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f'{unit}: PASS {len(rows)} PNG hashes, {checks} independent RGBA comparisons, {links} prior links')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--unit',choices=['young-009','young-010'],required=True);run(p.parse_args().unit)
