"""YOUNG-004: private-copy young dependency routing and failure controls."""
import argparse, asyncio, base64, json, sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.output import render_portrait
from petz_renderer.appearance.lnz import parse_sections
from petz_renderer.appearance.variations import inspect_variations
from research_common import write_copy
from young_breed_probe import ROOT,digest,provenance
OUT=ROOT/'scratch/research/young-004'; MANIFEST=ROOT/'experiments/young-004.json'

async def run(verify):
    expected=json.loads(MANIFEST.read_text()) if verify else None
    if not verify: OUT.mkdir(parents=True,exist_ok=False)
    report={'provenance':provenance(),'backend':'installed direct renderer and local stdio MCP','copies':[],'cases':[],'mcp':[],'relationships':[]}
    resolver=ResourceResolver((ROOT/'games/petz4',OUT)); observed={}; requests=[]
    for species,filename,adult,young in [('Dogz','Scottie.dog','SC','SCPUP'),('Catz','Siamese.cat','SI','SIKIT')]:
        source=ROOT/f'games/petz4/Resource/{species}/{filename}'; raw=source.read_bytes(); breed=ResourceFile(raw)
        leaf=next(r for r in breed.resources if r.type=='LNZ' and r.name==adult)
        original=dict(parse_sections(breed.read('LNZ',adult),41))
        variants={'control':(young,), 'path':(f'folder\\{young.lower()}.lnz',), 'sentinel':('X',),'lower-x':('x',),'missing':('ZZMISSING',),'first-row':('ZZMISSING',young),'branch':('#2', 'ZZMISSING','#1',young,'##')}
        for mode,rows in variants.items():
            sections={**original,'Little one':rows}; path=OUT/f'{species}-{mode}{Path(filename).suffix}'
            temporary=path.with_name(path.stem+'-replay'+path.suffix) if verify else path
            sha=write_copy(raw,leaf,sections,temporary)
            if verify: assert temporary.read_bytes()==path.read_bytes();temporary.unlink()
            report['copies'].append({'species':species,'mode':mode,'path':path.name,'sha256':sha,'source':str(source.relative_to(ROOT)),'source_sha256':digest(raw),'offset':leaf.offset,'length':leaf.size})
            branch={}
            if mode=='branch':
                trace=inspect_variations(ResourceFile(path.read_bytes()).read('LNZ',adult),41)
                blocks=[b for b in trace.blocks if 'Little one' in b.affected_sections]; assert len(blocks)==1
                branch={'branch_selections':{blocks[0].block_id:1}}
            tests=[('adult',{'look':'adult','age':100},True),('age100',{'look':'age','age':100},mode in ('control','path')),('young',{'look':'puppy','age':12},mode in ('control','path')),('override',{'look':'puppy','age':12,'young_name':young},True),('bad-override',{'look':'puppy','age':12,'young_name':young.lower()},False),('adult-bad-override',{'look':'adult','age':100,'young_name':'ZZMISSING'},True)]
            if mode=='branch':
                tests.extend([('branch-valid',{'look':'puppy','age':12,**branch},True),('branch-missing',{'look':'puppy','age':12,'branch_selections':{blocks[0].block_id:2}},False),('branch-rescued',{'look':'puppy','age':12,'young_name':young,'branch_selections':{blocks[0].block_id:2}},True)])
                # The seeded branch is measured independently rather than assumed.
                seeded=trace.sections['Little one'][0]==young
                tests=[(label,args,seeded if label in ('age100','young') else ok) for label,args,ok in tests]
            for label,args,ok in tests:
                controls={'path':path.name,'pose':'standing','seed':41,'fatness':50,'yaw_degrees':0,**args}
                row={'species':species,'mode':mode,'label':label,'controls':controls,'success':ok}
                try:
                    assets=load_breed_assets(resolver,path.name,pose='standing',seed=41,fatness=50,**args)
                except Exception as exc:
                    assert not ok,(species,mode,label,str(exc))
                    row.update(error_type=type(exc).__name__,error=str(exc))
                else:
                    assert ok,(species,mode,label)
                    images=[]
                    for yaw in (0,90):
                        result=render_portrait(assets,yaw=yaw*256//360);stem=f'{species}-{mode}-{label}-{yaw}'
                        if verify: assert (OUT/f'{stem}.png').read_bytes()==result.png
                        else: (OUT/f'{stem}.png').write_bytes(result.png)
                        images.append({'yaw':yaw,'png_sha256':digest(result.png),'size':[result.width,result.height],'offset':list(result.offset)})
                        observed[species,mode,label,yaw]=result.png
                    row['renders']=images;row['layers']=[x.label for x in assets.preview.layers]
                report['cases'].append(row); requests.append(row)
        for mode in variants:
            for yaw in (0,90):
                for label,baseline in [('adult','adult'),('adult-bad-override','adult'),('override','young')]:
                    assert observed[species,mode,label,yaw]==observed[species,'control',baseline,yaw]
                    report['relationships'].append({'species':species,'mode':mode,'label':label,'baseline':baseline,'yaw':yaw,'equal':True})
        for yaw in (0,90):
            assert observed[species,'path','young',yaw]==observed[species,'control','young',yaw]
            for label in ('branch-valid','branch-rescued'):
                assert observed[species,'branch',label,yaw]==observed[species,'control','young',yaw]
        print(f'{species}: routing and missing-dependency controls pass',flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for row in requests:
            mcp_controls=dict(row['controls'])
            if 'branch_selections' in mcp_controls:
                mcp_controls['branch_choices']=[{'block_id':k,'branch':v} for k,v in mcp_controls.pop('branch_selections').items()]
            response=await client.call_tool('render_pet',mcp_controls,raise_on_error=False)
            assert response.is_error != row['success'],row
            entry={'controls':mcp_controls,'species':row['species'],'mode':row['mode'],'label':row['label'],'success':not response.is_error}
            if row['success']:
                png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                assert png==observed[row['species'],row['mode'],row['label'],0]
                entry['png_sha256']=digest(png)
            else: entry['error']=str(response.content)
            report['mcp'].append(entry)
    if verify: assert report==expected;print('FULL REPLAY PASS',flush=True)
    else: MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
