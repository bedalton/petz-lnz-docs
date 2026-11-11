"""YOUNG-003: edit young resources in private copies; independent age arithmetic."""
import argparse, asyncio, base64, json, sys
from pathlib import Path
from dataclasses import fields,replace
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.appearance.layers import load_layer,kitten_name
from petz_renderer.appearance.age import aged_appearance
from petz_renderer.appearance.lnz import parse_sections
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.output import render_portrait
from research_common import write_copy
from young_breed_probe import ROOT,digest,provenance
OUT=ROOT/'scratch/research/young-003';MANIFEST=ROOT/'experiments/young-003.json'
def blend(a,b,age):
    weight=100 if age<12 else 100-(age-12)*100//88
    delta=(b-a)*weight
    return a+(abs(delta)//100)*(-1 if delta<0 else 1)
def check(actual,adult,young,age):
    shrink=max(0,12-age)*2; count=0
    for name in ('pet_scale','ball_scale'):
        assert getattr(actual,name)==blend(getattr(adult,name),getattr(young,name),age)-shrink;count+=1
    for f in fields(adult.shape):
        a,b,c=(getattr(x.shape,f.name) for x in (adult,young,actual))
        if isinstance(a,tuple): assert c==tuple(blend(x,y,age) for x,y in zip(a,b));count+=len(a)
        else: assert c==blend(a,b,age);count+=1
    for a,b,c in zip(adult.balls,young.balls,actual.balls):
        assert c.size==blend(a.size,b.size,age) and c.fuzz==blend(a.fuzz,b.fuzz,age)
        assert c.color==a.color;count+=3
    return count
async def run(verify):
    expected=json.loads(MANIFEST.read_text()) if verify else None
    if not verify: OUT.mkdir(parents=True,exist_ok=False)
    report={'provenance':provenance(),'backend':'direct renderer and local stdio MCP','numeric':[],'copies':[],'renders':[],'mcp':[],'relationships':[]}
    for version in ('petz3','petz4','petz5'):
        resolver=ResourceResolver((ROOT/'games'/version,),game_version=version)
        for species,file in [('Dogz','Scottie.dog'),('Catz','Siamese.cat')]:
            path=f'Resource/{species}/{file}'
            adult=load_breed_assets(resolver,path,pose='standing',look='adult',seed=41,age=100,fatness=50).appearance
            young=load_breed_assets(resolver,path,pose='standing',look='puppy',seed=41,age=0,fatness=50).appearance
            for age in range(101):
                # Replays exercise the public loader at boundaries and the age API elsewhere.
                if verify and age not in (0,11,12,13,50,99,100):
                    actual=aged_appearance(adult,young,age)
                else:
                    actual=load_breed_assets(resolver,path,pose='standing',look='age',seed=41,age=age,fatness=50).appearance
                n=check(actual,adult,young,age)
                report['numeric'].append({'version':version,'species':species,'age':age,'assertions':n,'pet_scale':actual.pet_scale,'ball_scale':actual.ball_scale})
            print(f'{version}-{species}: 101 independent arithmetic records pass',flush=True)
    observations={}; resolver=ResourceResolver((ROOT/'games/petz4',OUT))
    for species,file,selector,head in [('Dogz','Scottie.dog','SC',52),('Catz','Siamese.cat','SI',24)]:
        path=f'Resource/{species}/{file}';raw=(ROOT/'games/petz4'/path).read_bytes();breed=ResourceFile(raw)
        master=ResourceFile((ROOT/f'games/petz4/Resource/{species} 4 Rez.dll').read_bytes())
        adult=load_layer(breed,master,name=selector,seed=41); name=kitten_name(adult.sections)
        leaf=next(x for x in breed.resources if x.type=='LNZ' and x.name==name)
        own=dict(parse_sections(breed.read('LNZ',name),41));young=load_layer(breed,master,name=name,seed=41)
        for mode in ('control','size','color'):
            sections=dict(own)
            if mode=='size': sections['Ball Size Override']=(*young.sections.get('Ball Size Override',()),f'{head}, 35')
            if mode=='color': sections['Color Info Override']=(*young.sections.get('Color Info Override',()),f'{head}, 125')
            target=OUT/f'{species}-{mode}{Path(file).suffix}'
            if verify:
                # Reconstruct to a separate scratch path, preserving recorded fixtures.
                target2=OUT/f'{species}-{mode}-replay{Path(file).suffix}'; value=write_copy(raw,leaf,sections,target2); assert target.read_bytes()==target2.read_bytes();target2.unlink()
            else: value=write_copy(raw,leaf,sections,target)
            report['copies'].append({'species':species,'mode':mode,'path':target.name,'sha256':value,'source_sha256':digest(raw),'young_resource':name,'edited_offset':leaf.offset,'edited_length':leaf.size,'head':head})
            for look,ages in [('age',(0,6,12,50,100)),('adult',(100,)),('puppy',(0,))]:
                for age in ages:
                    assets=load_breed_assets(resolver,target.name,pose='standing',look=look,age=age,seed=41,fatness=50)
                    for yaw in (0,90):
                        output=render_portrait(assets,yaw=yaw*256//360); stem=f'{species}-{mode}-{look}-{age}-{yaw}'
                        if verify: assert digest((OUT/f'{stem}.png').read_bytes())==digest(output.png)
                        else: (OUT/f'{stem}.png').write_bytes(output.png)
                        report['renders'].append({'species':species,'mode':mode,'look':look,'age':age,'yaw':yaw,'head_size':assets.appearance.balls[head].size,'head_color':assets.appearance.balls[head].color,'png_sha256':digest(output.png),'size':[output.width,output.height],'offset':list(output.offset)})
                        observations[species,mode,look,age,yaw]=output
        # The compact young control must preserve the original seeded result.
        for look,ages in [('age',(0,6,12,50,100)),('adult',(100,)),('puppy',(0,))]:
            for age in ages:
                original=load_breed_assets(resolver,path,pose='standing',look=look,age=age,seed=41,fatness=50)
                for yaw in (0,90): assert render_portrait(original,yaw=yaw*256//360).png==observations[species,'control',look,age,yaw].png
        for yaw in (0,90):
            for mode in ('size','color'):
                for look,age in [('adult',100),('age',100)]:
                    a=observations[species,mode,look,age,yaw];b=observations[species,'control',look,age,yaw]
                    report['relationships'].append({'species':species,'mode':mode,'look':look,'age':age,'yaw':yaw,'equal':a.png==b.png})
                    assert a.png==b.png
            for age in (0,6,12,50):
                assert observations[species,'color','age',age,yaw].png==observations[species,'control','age',age,yaw].png
            assert observations[species,'color','puppy',0,yaw].png!=observations[species,'control','puppy',0,yaw].png
        print(f'{species}: private young-resource controls pass',flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for row in report['copies']:
            for look,age in [('age',0),('age',50),('age',100),('puppy',0)]:
                args={'path':row['path'],'look':look,'age':age,'pose':'standing','seed':41,'fatness':50,'yaw_degrees':0}
                result=await client.call_tool('render_pet',args);assert not result.is_error
                png=base64.b64decode(next(x.data for x in result.content if x.type=='image'));assert png==observations[row['species'],row['mode'],look,age,0].png
                report['mcp'].append({'controls':args,'png_sha256':digest(png),'appearance':result.data['appearance']})
    if verify: assert report==expected;print('FULL REPLAY PASS')
    else: MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
