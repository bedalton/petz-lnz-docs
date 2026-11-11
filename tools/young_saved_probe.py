"""YOUNG-002: copy-only saved-cache omission and look routing."""
import argparse, asyncio, base64, io, json, sys
from dataclasses import replace
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image
from petz_renderer.formats.pet import read_saved_appearance
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT, digest, provenance
OUT=ROOT/'scratch/research/young-002'; MANIFEST=ROOT/'experiments/young-002.json'
MODES={'baseline':(), 'missing-adult':('adult',), 'missing-young':('young',), 'missing-both':('adult','young')}
def copies(name,verify):
    source=ROOT/f'games/petz4/Adopted Petz/{name}.pet'; raw=source.read_bytes(); pet=read_saved_appearance(raw); result={}
    for mode,removed in MODES.items():
        spans=[]
        for cache in removed:
            text=getattr(pet,cache+'_cache'); assert text and raw.count(text)==1
            spans.append((raw.index(text),len(text)))
        data=raw
        for start,size in sorted(spans,reverse=True): data=data[:start]+data[start+size:]
        parsed=read_saved_appearance(data)
        assert replace(parsed,adult_cache=pet.adult_cache,young_cache=pet.young_cache)==pet
        assert data[-pet.unparsed_bytes:]==raw[-pet.unparsed_bytes:]
        path=OUT/f'{name}-{mode}.pet'
        if verify: assert path.read_bytes()==data
        else: path.write_bytes(data)
        result[mode]={'path':path.name,'sha256':digest(data),'removed':list(removed),'removed_bytes':sum(n for _,n in spans)}
    return {'name':name,'source':str(source.relative_to(ROOT/'games/petz4')),'source_sha256':digest(raw),'breed':pet.breed_file,'breed_sha256':digest(ResourceResolver((ROOT/'games/petz4',)).read_bytes(pet.breed_file,limit=16777216).data),'saved_age':pet.biorhythms[8],'saved_seed':pet.variation_seed,'variants':result}
def cases():
    return [(look,age,yaw) for look,ages in [('age',(0,12,50,100)),('adult',(0,100)),('puppy',(0,100)),('kitten',(0,))] for age in ages for yaw in (0,90)]
async def run(verify):
    expected=json.loads(MANIFEST.read_text()) if verify else None
    if not verify: OUT.mkdir(parents=True,exist_ok=False)
    report={'provenance':provenance(),'backend':'direct installed renderer with local stdio MCP cross-checks','copies':[],'cases':[],'relationships':[],'mcp':[]}
    resolver=ResourceResolver((ROOT/'games/petz4',OUT)); observations={}
    for name in ('Fuzzkin','Homebody','Goobe'):
        source=copies(name,verify); report['copies'].append(source)
        for mode,variant in source['variants'].items():
            for look,age,yaw in cases():
                assets=load_saved_assets(resolver,variant['path'],pose='standing',age=age,look=look)
                assert assets.preview.seed==source['saved_seed'] and assets.preview.fatness_source=='saved'
                requested=('young',) if look in ('puppy','kitten') else ('adult',) if look=='adult' else ('adult','young')
                labels=[x.label for x in assets.preview.layers]
                for cache in requested: assert any(x.endswith('/'+cache) and ':cache/' in x for x in labels)==(cache not in variant['removed'])
                fallback=any(x in variant['removed'] for x in requested)
                assert assets.preview.mode==('saved_fallback' if fallback else 'saved_cache')
                render=render_portrait(assets,yaw=yaw*256//360)
                im=Image.open(io.BytesIO(render.png)).convert('RGBA'); stem=f'{name}-{mode}-{look}-{age}-{yaw}'
                row={'name':name,'mode':mode,'look':look,'age':age,'yaw_degrees':yaw,'png_sha256':digest(render.png),'rgba_sha256':digest(im.tobytes()),'size':list(im.size),'offset':list(render.offset) if hasattr(render,'offset') else [render.width,render.height],'appearance_mode':assets.preview.mode,'layers':[{'label':x.label,'sha256':x.sha256} for x in assets.preview.layers]}
                observations[name,mode,look,age,yaw]=(render,assets,row)
                if verify: assert digest((OUT/f'{stem}.png').read_bytes())==row['png_sha256']
                else: (OUT/f'{stem}.png').write_bytes(render.png)
                report['cases'].append(row)
        def equal(m1,l1,a1,m2,l2,a2,yaw,kind):
            left=observations[name,m1,l1,a1,yaw][0]; right=observations[name,m2,l2,a2,yaw][0]
            assert left.png==right.png and left.prepared==right.prepared,(name,kind,yaw)
            report['relationships'].append({'name':name,'yaw_degrees':yaw,'a':[m1,l1,a1],'b':[m2,l2,a2],'kind':kind,'equal_commands_and_png':True})
        for mode in MODES:
            for yaw in (0,90):
                equal(mode,'adult',0,mode,'adult',100,yaw,'forced adult ignores age')
                equal(mode,'puppy',0,mode,'puppy',100,yaw,'forced young ignores age')
                equal(mode,'puppy',0,mode,'kitten',0,yaw,'young aliases')
                # Age averaging retains adult-only metadata; endpoint pixel equality is measured separately.
                for look,age in [('adult',0),('puppy',0)]:
                    irrelevant='missing-young' if look=='adult' else 'missing-adult'
                    if mode==irrelevant: equal(mode,look,age,'baseline',look,age,yaw,'unused cache omission is inert')
        print(f'{name}: 72 direct renders, cache routing/commands pass',flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for name in ('Fuzzkin','Homebody','Goobe'):
            for mode in MODES:
                for look,age in [('age',12),('adult',0),('puppy',0)]:
                    path=next(x for x in report['copies'] if x['name']==name)['variants'][mode]['path']
                    response=await client.call_tool('render_pet',{'path':path,'look':look,'age':age,'pose':'standing','yaw_degrees':0})
                    assert not response.is_error
                    png=base64.b64decode(next(x.data for x in response.content if x.type=='image'))
                    direct=observations[name,mode,look,age,0][0]; assert png==direct.png
                    row={'name':name,'mode':mode,'look':look,'age':age,'png_sha256':digest(png),'appearance':response.data['appearance']}; report['mcp'].append(row)
                    if not verify: (OUT/f'{name}-{mode}-{look}-mcp.json').write_text(json.dumps(response.data,indent=2))
    if verify: assert report==expected; print('FULL REPLAY PASS')
    else: MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--verify',action='store_true'); asyncio.run(run(p.parse_args().verify))
