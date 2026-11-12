"""YOUNG-011: separate x/body-area changes behind omitted ball93."""
import argparse,json
from dataclasses import fields,replace
from pathlib import Path
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT,digest,provenance
from young_endpoint_attribution import difference
from young_endpoint_fields import FACTORS,modify
OUT=ROOT/'scratch/research/young-011';MANIFEST=ROOT/'experiments/young-011.json'
def run(verify):
    old=json.loads(MANIFEST.read_text()) if verify else None
    if not verify:OUT.mkdir(parents=True,exist_ok=False)
    pp=ROOT/'experiments/young-010.json';prior=json.loads(pp.read_text());source=prior['inputs']
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'))
    report={'provenance':provenance(),'backend':'direct installed renderer; unomitted diagnostic field substitutions; no new MCP',
        'script_sha256':digest(Path(__file__).read_bytes()),'prior_manifest_sha256':digest(pp.read_bytes()),'inputs':source,'renders':[]}
    for mode in ('missing-adult','missing-young'):
        v=source['variants'][mode];assert digest((ROOT/'scratch/research/young-002'/v['path']).read_bytes())==v['sha256']
        for pose in ('standing','sitting','lying'):
            age=load_saved_assets(resolver,v['path'],pose=pose,look='age',age=12)
            young=load_saved_assets(resolver,v['path'],pose=pose,look='puppy',age=12)
            a,b=age.appearance,young.appearance
            assert {f.name for f in fields(a.add_balls[26]) if getattr(a.add_balls[26],f.name)!=getattr(b.add_balls[26],f.name)}=={'x','body_area'}
            full=modify(a,b,FACTORS);full=replace(full,omissions=full.omissions-{93})
            for yaw in range(0,360,45):
                target=render_portrait(replace(age,appearance=full),yaw=yaw*256//360)
                for label,names in [('none',()),('x',('x',)),('body_area',('body_area',)),('both',('x','body_area'))]:
                    rows=list(full.add_balls);rows[26]=replace(rows[26],**{f:getattr(a.add_balls[26],f) for f in names})
                    result=render_portrait(replace(age,appearance=replace(full,add_balls=tuple(rows))),yaw=yaw*256//360)
                    file=f'{mode}-{pose}-{yaw}-{label}.png'
                    if verify:assert (OUT/file).read_bytes()==result.png
                    else:(OUT/file).write_bytes(result.png)
                    g=result.prepared.geometry;tg=target.prepared.geometry
                    row={'mode':mode,'pose':pose,'yaw':yaw,'label':label,'file':file,'png_sha256':digest(result.png),
                        'size':[result.width,result.height],'offset':list(result.offset),'pixels_vs_full':difference(result,target),
                        'ball93_visible':g.balls[93].visible,'ball93_area':g.areas[93],
                        'geometry_equal_full':g.balls==tg.balls,'fills_equal_full':g.fills==tg.fills,
                        'commands_equal_full':result.prepared.balls==target.prepared.balls}
                    if label in ('none','both'):
                        oldlabel='unomit-full' if label=='none' else 'unomit-revert26'
                        link=next(r for r in prior['renders'] if (r['mode'],r['pose'],r['yaw'],r['label'])==(mode,pose,yaw,oldlabel))
                        assert row['png_sha256']==link['png_sha256']
                    report['renders'].append(row)
            print(f'{mode}/{pose}: 32 field controls pass',flush=True)
    report['summary']={'renders':len(report['renders']),'prior_links':96,
        'changed_views_by_label':{label:sum(r['pixels_vs_full']>0 for r in report['renders'] if r['label']==label) for label in ('none','x','body_area','both')}}
    if verify:assert report==old;print('FULL REPLAY PASS',flush=True)
    else:MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');run(p.parse_args().verify)
