"""YOUNG-005: field substitution attribution for saved-cache age12 endpoints."""
import argparse,asyncio,base64,io,itertools,json,sys
from dataclasses import fields,replace
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT,digest,provenance
OUT=ROOT/'scratch/research/young-005';MANIFEST=ROOT/'experiments/young-005.json'
GROUPS=('balls','add_balls','lines','paint_balls')
def sig(result): return digest(result.png),result.width,result.height,result.offset

def difference(a,b):
    left,top=min(-a.offset[0],-b.offset[0]),min(-a.offset[1],-b.offset[1])
    right,bottom=max(a.width-a.offset[0],b.width-b.offset[0]),max(a.height-a.offset[1],b.height-b.offset[1])
    size=(right-left,bottom-top);canvases=[]
    for result in (a,b):
        canvas=Image.new('RGBA',size); im=Image.open(io.BytesIO(result.png)).convert('RGBA')
        canvas.paste(im,(-result.offset[0]-left,-result.offset[1]-top));canvases.append(canvas)
    return sum(x!=y for x,y in zip(canvases[0].getdata(),canvases[1].getdata()))

async def run(verify):
    old=json.loads(MANIFEST.read_text()) if verify else None
    if not verify: OUT.mkdir(parents=True,exist_ok=False)
    source=json.loads((ROOT/'experiments/young-002.json').read_text())
    fuzz=next(x for x in source['copies'] if x['name']=='Fuzzkin')
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'))
    report={'provenance':provenance(),'backend':'direct installed renderer, immutable appearance substitutions, local stdio MCP baselines','prior_manifest_sha256':digest((ROOT/'experiments/young-002.json').read_bytes()),'inputs':fuzz,'fixtures':[],'renders':[],'mcp':[]}
    baseline_png={}
    for mode,variant in fuzz['variants'].items():
        assert digest((ROOT/'scratch/research/young-002'/variant['path']).read_bytes())==variant['sha256']
        for pose in ('standing','sitting','lying'):
            age=load_saved_assets(resolver,variant['path'],pose=pose,look='age',age=12)
            young=load_saved_assets(resolver,variant['path'],pose=pose,look='puppy',age=12)
            # Substitutions retain identical frame, palette and texture dependencies.
            assert (age.sizes,age.frame,age.textures,age.palette)==(young.sizes,young.frame,young.textures,young.palette)
            differing=[f.name for f in fields(age.appearance) if getattr(age.appearance,f.name)!=getattr(young.appearance,f.name)]
            assert set(differing)<=set(GROUPS)
            detail={}
            for group in differing:
                a,b=getattr(age.appearance,group),getattr(young.appearance,group)
                detail[group]={'age_length':len(a),'young_length':len(b),'changed_entries':[i for i,(x,y) in enumerate(zip(a,b)) if x!=y],'changed_fields':{str(i):[f.name for f in fields(x) if getattr(x,f.name)!=getattr(y,f.name)] for i,(x,y) in enumerate(zip(a,b)) if x!=y}}
            fixture={'mode':mode,'pose':pose,'differing_fields':differing,'detail':detail,'views':[]}
            outputs={}
            # Exhaust all subsets of actually differing lists, including empty/full.
            subsets=[tuple(g for bit,g in enumerate(differing) if mask&(1<<bit)) for mask in range(1<<len(differing))]
            for yaw in (0,90):
                target=render_portrait(young,yaw=yaw*256//360)
                for groups in subsets:
                    appearance=replace(age.appearance,**{g:getattr(young.appearance,g) for g in groups})
                    output=render_portrait(replace(age,appearance=appearance),yaw=yaw*256//360)
                    label='-'.join(groups) or 'none';stem=f'{mode}-{pose}-{yaw}-{label}'
                    if verify: assert (OUT/f'{stem}.png').read_bytes()==output.png
                    else: (OUT/f'{stem}.png').write_bytes(output.png)
                    outputs[groups,yaw]=output
                    report['renders'].append({'mode':mode,'pose':pose,'yaw':yaw,'groups':list(groups),'png_sha256':digest(output.png),'size':[output.width,output.height],'offset':list(output.offset),'equals_young':sig(output)==sig(target),'pixels_vs_young':difference(output,target)})
                stem=f'{mode}-{pose}-{yaw}-young'
                if verify: assert (OUT/f'{stem}.png').read_bytes()==target.png
                else: (OUT/f'{stem}.png').write_bytes(target.png)
                report['renders'].append({'mode':mode,'pose':pose,'yaw':yaw,'groups':'forced-young','png_sha256':digest(target.png),'size':[target.width,target.height],'offset':list(target.offset)})
                assert sig(outputs[tuple(differing),yaw])==sig(target)
                baseline_png[mode,pose,'age',yaw]=outputs[(),yaw].png
                baseline_png[mode,pose,'puppy',yaw]=target.png
                sufficient=[list(g) for g in subsets if sig(outputs[g,yaw])==sig(target)]
                minimal=[g for g in sufficient if not any(set(h)<set(g) for h in sufficient)]
                fixture['views'].append({'yaw':yaw,'baseline_pixels_vs_young':difference(outputs[(),yaw],target),'minimal_sufficient_substitutions':minimal})
                if pose=='standing':
                    for look,previous_age in [('age',12),('puppy',0)]:
                        prior=next(x for x in source['cases'] if (x['name'],x['mode'],x['look'],x['age'],x['yaw_degrees'])==('Fuzzkin',mode,look,previous_age,yaw))
                        assert digest(baseline_png[mode,pose,look,yaw])==prior['png_sha256']
            report['fixtures'].append(fixture)
            print(f'{mode}/{pose}: {len(subsets)} field subsets, both views pass',flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/young-002')])
    async with Client(transport) as client:
        for mode,variant in fuzz['variants'].items():
            for pose in ('standing','sitting','lying'):
                for look in ('age','puppy'):
                    args={'path':variant['path'],'pose':pose,'look':look,'age':12,'yaw_degrees':0}
                    result=await client.call_tool('render_pet',args);assert not result.is_error
                    png=base64.b64decode(next(c.data for c in result.content if c.type=='image'))
                    assert png==baseline_png[mode,pose,look,0]
                    report['mcp'].append({'controls':args,'png_sha256':digest(png)})
    if verify: assert report==old;print('FULL REPLAY PASS',flush=True)
    else: MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
