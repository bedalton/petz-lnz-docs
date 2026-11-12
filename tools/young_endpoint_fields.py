"""YOUNG-006: narrow list attribution to ball outlines and added-list partitions."""
import argparse,asyncio,itertools,json
from dataclasses import replace
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT,digest,provenance
from young_endpoint_attribution import difference,sig
OUT=ROOT/'scratch/research/young-006';MANIFEST=ROOT/'experiments/young-006.json'
FACTORS=('outline14','outline38','add-prefix','add-tail','lines')
def modify(a,b,factors):
    balls=list(a.balls)
    for i in (14,38):
        if f'outline{i}' in factors:balls[i]=replace(balls[i],outline_color=b.balls[i].outline_color)
    adds=a.add_balls
    if 'add-prefix' in factors:adds=b.add_balls[:23]+adds[23:]
    if 'add-tail' in factors:adds=adds[:23]+b.add_balls[23:]
    return replace(a,balls=tuple(balls),add_balls=adds,lines=b.lines if 'lines' in factors else a.lines)
async def run(verify):
    old=json.loads(MANIFEST.read_text()) if verify else None
    if not verify:OUT.mkdir(parents=True,exist_ok=False)
    prior=json.loads((ROOT/'experiments/young-005.json').read_text());source=prior['inputs']
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'))
    report={'provenance':provenance(),'backend':'direct installed renderer with immutable field substitutions; no new MCP calls','prior_manifest_sha256':digest((ROOT/'experiments/young-005.json').read_bytes()),'inputs':source,'fixtures':[],'renders':[]}
    subsets=[tuple(g for i,g in enumerate(FACTORS) if mask&(1<<i)) for mask in range(32)]
    for mode in ('missing-adult','missing-young'):
        path=source['variants'][mode]['path']
        assert digest((ROOT/'scratch/research/young-002'/path).read_bytes())==source['variants'][mode]['sha256']
        for pose in ('standing','sitting','lying'):
            age=load_saved_assets(resolver,path,pose=pose,look='age',age=12)
            young=load_saved_assets(resolver,path,pose=pose,look='puppy',age=12)
            a,b=age.appearance,young.appearance
            assert len(a.add_balls)!=len(b.add_balls)
            assert all(replace(x,speckle_color=y.speckle_color,outline_color=y.outline_color)==y for x,y in zip(a.balls,b.balls))
            assert [i for i,(x,y) in enumerate(zip(a.balls,b.balls)) if x.outline_color!=y.outline_color]==[14,38]
            assert all(replace(x,body_area=y.body_area)==y for x,y in zip(a.add_balls[:23],b.add_balls[:23]))
            fixture={'mode':mode,'pose':pose,'views':[]}
            for yaw in (0,90):
                target=render_portrait(young,yaw=yaw*256//360);baseline=render_portrait(age,yaw=yaw*256//360);outputs={}
                controls={'speckle-only':replace(a,balls=tuple(replace(x,speckle_color=y.speckle_color) for x,y in zip(a.balls,b.balls))),'paints-only':replace(a,paint_balls=b.paint_balls),'all-non-speckle':modify(a,b,FACTORS)}
                for label,appearance in [*[(('-'.join(g) or 'none'),modify(a,b,g)) for g in subsets],*controls.items()]:
                    result=render_portrait(replace(age,appearance=appearance),yaw=yaw*256//360)
                    stem=f'{mode}-{pose}-{yaw}-{label}'
                    if verify:assert (OUT/f'{stem}.png').read_bytes()==result.png
                    else:(OUT/f'{stem}.png').write_bytes(result.png)
                    row={'mode':mode,'pose':pose,'yaw':yaw,'label':label,'png_sha256':digest(result.png),'size':[result.width,result.height],'offset':list(result.offset),'pixels_vs_young':difference(result,target),'equals_young':sig(result)==sig(target),'equals_age':sig(result)==sig(baseline)}
                    report['renders'].append(row);outputs[label]=result
                assert sig(outputs['speckle-only'])==sig(baseline)
                assert sig(outputs['paints-only'])==sig(baseline)
                assert sig(outputs['all-non-speckle'])==sig(target)
                priorrow=next(r for r in prior['renders'] if (r['mode'],r['pose'],r['yaw'],r['groups'])==(mode,pose,yaw,[]))
                assert digest(baseline.png)==priorrow['png_sha256']
                sufficient=[list(g) for g in subsets if sig(outputs['-'.join(g) or 'none'])==sig(target)]
                minimal=[g for g in sufficient if not any(set(h)<set(g) for h in sufficient)]
                fixture['views'].append({'yaw':yaw,'minimal_sufficient_substitutions':minimal,'baseline_pixels_vs_young':difference(baseline,target)})
            report['fixtures'].append(fixture);print(f'{mode}/{pose}: 32 field combinations plus 3 controls per view pass',flush=True)
    if verify:assert report==old;print('FULL REPLAY PASS',flush=True)
    else:MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
