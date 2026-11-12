"""YOUNG-010: test the pixel-inert entry26 result beyond front/side."""
import argparse,asyncio,base64,json,sys
from dataclasses import replace
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT,digest,provenance
from young_endpoint_attribution import difference,sig
from young_endpoint_fields import FACTORS,modify
OUT=ROOT/'scratch/research/young-010';MANIFEST=ROOT/'experiments/young-010.json'
async def run(verify):
    old=json.loads(MANIFEST.read_text()) if verify else None
    if not verify:OUT.mkdir(parents=True,exist_ok=False)
    priorpath=ROOT/'experiments/young-008.json';prior=json.loads(priorpath.read_text());source=prior['inputs']
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'))
    report={'provenance':provenance(),'backend':'direct installed renderer; local stdio MCP forced-young opposite-side controls',
            'script_sha256':digest(Path(__file__).read_bytes()),'prior_manifest_sha256':digest(priorpath.read_bytes()),
            'inputs':source,'renders':[],'fixtures':[],'mcp':[]}
    endpoints={}
    for mode in ('missing-adult','missing-young'):
        v=source['variants'][mode];assert digest((ROOT/'scratch/research/young-002'/v['path']).read_bytes())==v['sha256']
        for pose in ('standing','sitting','lying'):
            age=load_saved_assets(resolver,v['path'],pose=pose,look='age',age=12)
            young=load_saved_assets(resolver,v['path'],pose=pose,look='puppy',age=12)
            a,b=age.appearance,young.appearance;full=modify(a,b,FACTORS)
            assert 93 in a.omissions and 93 in b.omissions
            rows=list(full.add_balls);rows[26]=a.add_balls[26];reverted=replace(full,add_balls=tuple(rows))
            for yaw in range(0,360,45):
                results={label:render_portrait(assets,yaw=yaw*256//360) for label,assets in
                         [('young',young),('full',replace(age,appearance=full)),('revert26',replace(age,appearance=reverted)),
                          ('unomit-full',replace(age,appearance=replace(full,omissions=full.omissions-{93}))),
                          ('unomit-revert26',replace(age,appearance=replace(reverted,omissions=reverted.omissions-{93})))]}
                endpoints[mode,pose,yaw]=results['young'].png
                for label,result in results.items():
                    file=f'{mode}-{pose}-{yaw}-{label}.png'
                    if verify:assert (OUT/file).read_bytes()==result.png
                    else:(OUT/file).write_bytes(result.png)
                    report['renders'].append({'mode':mode,'pose':pose,'yaw':yaw,'label':label,'file':file,
                        'png_sha256':digest(result.png),'size':[result.width,result.height],'offset':list(result.offset),
                        'pixels_vs_young':difference(result,results['young']),'pixels_vs_full':difference(result,results['full']),
                        'ball93_visible':result.prepared.geometry.balls[93].visible,
                        'pixels_vs_unomit_full':difference(result,results['unomit-full'])})
                if yaw in (0,90):
                    p=next(r for r in prior['renders'] if (r['mode'],r['pose'],r['yaw'],r['mask'])==(mode,pose,yaw,127))
                    assert digest(results['full'].png)==p['png_sha256']
                    assert sig(results['full'])==sig(results['revert26'])
                report['fixtures'].append({'mode':mode,'pose':pose,'yaw':yaw,
                    'full_pixels_vs_young':difference(results['full'],results['young']),
                    'reversion_pixels_vs_full':difference(results['revert26'],results['full']),
                    'unomitted_reversion_pixels':difference(results['unomit-revert26'],results['unomit-full'])})
            print(f'{mode}/{pose}: eight yaws, five controls pass',flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/young-002')])
    async with Client(transport) as client:
        for mode in ('missing-adult','missing-young'):
            for pose in ('standing','sitting','lying'):
                args={'path':source['variants'][mode]['path'],'pose':pose,'look':'puppy','age':12,'yaw_degrees':270}
                response=await client.call_tool('render_pet',args);assert not response.is_error
                png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                assert png==endpoints[mode,pose,270]
                report['mcp'].append({'controls':args,'png_sha256':digest(png)})
    report['summary']={'renders':len(report['renders']),'mcp_matches':len(report['mcp']),'prior_links':12,
        'reversion_changed_views':sum(f['reversion_pixels_vs_full']>0 for f in report['fixtures']),
        'unomitted_changed_views':sum(f['unomitted_reversion_pixels']>0 for f in report['fixtures']),
        'full_changed_vs_young':sum(f['full_pixels_vs_young']>0 for f in report['fixtures'])}
    if verify:assert report==old;print('FULL REPLAY PASS',flush=True)
    else:MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
