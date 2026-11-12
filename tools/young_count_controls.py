"""YOUNG-009: distinguish count changes from indexed visibility/size controls."""
import argparse,json
from dataclasses import replace
from pathlib import Path
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT,digest,provenance
from young_endpoint_attribution import difference,sig
from young_endpoint_fields import FACTORS,modify
OUT=ROOT/'scratch/research/young-009';MANIFEST=ROOT/'experiments/young-009.json'

def run(verify):
    old=json.loads(MANIFEST.read_text()) if verify else None
    if not verify:OUT.mkdir(parents=True,exist_ok=False)
    priorpath=ROOT/'experiments/young-008.json';prior=json.loads(priorpath.read_text());source=prior['inputs']
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'))
    report={'provenance':provenance(),'backend':'direct installed renderer; immutable appearance controls; existing MCP-linked endpoints',
            'script_sha256':digest(Path(__file__).read_bytes()),'prior_manifest_sha256':digest(priorpath.read_bytes()),
            'inputs':source,'renders':[],'fixtures':[]}
    for mode in ('missing-adult','missing-young'):
        v=source['variants'][mode];assert digest((ROOT/'scratch/research/young-002'/v['path']).read_bytes())==v['sha256']
        for pose in ('standing','sitting','lying'):
            age=load_saved_assets(resolver,v['path'],pose=pose,look='age',age=12)
            young=load_saved_assets(resolver,v['path'],pose=pose,look='puppy',age=12)
            a,b=age.appearance,young.appearance;full=modify(a,b,FACTORS)
            tail=(a.add_balls if len(a.add_balls)==32 else b.add_balls)[29:]
            long=replace(full,add_balls=full.add_balls[:29]+tail)
            assert len(long.balls)==67 and len(long.add_balls)==32
            variants={f'prefix-{n}':replace(long,add_balls=long.add_balls[:n]) for n in range(29,33)}
            for mask in range(8):
                disabled=[i for i in range(3) if not mask&(1<<i)]
                variants[f'omit-{mask}']=replace(long,omissions=long.omissions|frozenset(96+i for i in disabled))
                rows=list(long.add_balls)
                for i in disabled:rows[29+i]=replace(rows[29+i],size=0)
                variants[f'zero-{mask}']=replace(long,add_balls=tuple(rows))
            for yaw in (0,90):
                targets={k:render_portrait(replace(age,appearance=ap),yaw=yaw*256//360) for k,ap in variants.items()}
                target=render_portrait(young,yaw=yaw*256//360);short=targets['prefix-29'];longresult=targets['prefix-32']
                endpoint=longresult if mode=='missing-adult' else short
                priorfixture=next(f for f in prior['fixtures'] if (f['mode'],f['pose'],f['yaw'])==(mode,pose,yaw))
                assert digest(endpoint.png)==priorfixture['prior_full_sha256']==digest(target.png)
                for label,result in targets.items():
                    file=f'{mode}-{pose}-{yaw}-{label}.png'
                    if verify:assert (OUT/file).read_bytes()==result.png
                    else:(OUT/file).write_bytes(result.png)
                    g=result.prepared.geometry
                    shared_fills=g.fills[:96];shared_geometry=g.balls[:96]
                    row={'mode':mode,'pose':pose,'yaw':yaw,'label':label,'file':file,'png_sha256':digest(result.png),
                         'size':[result.width,result.height],'offset':list(result.offset),
                         'pixels_vs_short':difference(result,short),'pixels_vs_long':difference(result,longresult),
                         'pixels_vs_young':difference(result,target),'equals_young':sig(result)==sig(target),
                         'shared_fills_equal_short':shared_fills==short.prepared.geometry.fills[:96],
                         'shared_geometry_equal_short':shared_geometry==short.prepared.geometry.balls[:96],
                         'shared_commands_equal_short':result.prepared.balls[:96]==short.prepared.balls[:96],
                         'total_geometry_balls':len(g.balls)}
                    report['renders'].append(row)
                assert sig(targets['omit-7'])==sig(longresult)==sig(targets['zero-7'])
                report['fixtures'].append({'mode':mode,'pose':pose,'yaw':yaw,'prior_endpoint_sha256':digest(endpoint.png),
                    'omission_matches_short':[m for m in range(8) if sig(targets[f'omit-{m}'])==sig(short)],
                    'zero_matches_short':[m for m in range(8) if sig(targets[f'zero-{m}'])==sig(short)],
                    'omission_matches_long':[m for m in range(8) if sig(targets[f'omit-{m}'])==sig(longresult)],
                    'zero_matches_long':[m for m in range(8) if sig(targets[f'zero-{m}'])==sig(longresult)]})
            print(f'{mode}/{pose}: 40 index-preserving/count controls pass',flush=True)
    report['summary']={'renders':len(report['renders']),'prior_endpoint_links':len(report['fixtures']),
                       'omit_none_matches_short':sum(0 in f['omission_matches_short'] for f in report['fixtures']),
                       'zero_none_matches_short':sum(0 in f['zero_matches_short'] for f in report['fixtures'])}
    if verify:assert report==old;print('FULL REPLAY PASS',flush=True)
    else:MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');run(p.parse_args().verify)
