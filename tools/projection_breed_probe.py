"""Copy-only, asset-backed Project Ball probe through local MCP."""
import argparse,asyncio,json,sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.positions import modify_positions
from research_common import ROOT,SHA,adult,write_copy,save_result
BREEDS={}
VERSION='petz4'
EXPERIMENT='PROJECT-002'
OUT=ROOT/'scratch/research/project-002'
def xyz(b): return (b.x,b.y,b.z)
def trunc(n): return n//100 if n>=0 else -((-n)//100)
async def main():
    OUT.mkdir(parents=True,exist_ok=False)
    cases=[];renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,_,_=adult(species, VERSION, **BREEDS.get(species, {}))
        head,nose=(52,55) if species=='Dogz' else (24,37)
        variants={'control':(), 'identity':(f'{head}, {nose}, 100',),
                  'half':(f'{head}, {nose}, 50',), 'long':(f'{head}, {nose}, 150',)}
        paths={};hashes={}
        for v,rows in variants.items():
            sections=dict(base);sections['Project Ball']=rows
            path=OUT/f'{species}-{v}{source.suffix}'
            hashes[v]=write_copy(raw,leaf,sections,path);paths[v]=path.name
        resolver=ResourceResolver((ROOT/'games'/VERSION,OUT),game_version=VERSION);checks=[]
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            frames={v:modify_positions(a.appearance,a.frame) for v,a in assets.items()}
            control=frames['control'];start=xyz(control.balls[head]);end=xyz(control.balls[nose])
            assert frames['identity']==control
            for v,percent in [('half',50),('long',150)]:
                changed=[i for i,(a,b) in enumerate(zip(control.balls,frames[v].balls)) if xyz(a)!=xyz(b)]
                expected=tuple(s+trunc((e-s)*percent) for s,e in zip(start,end))
                assert changed==[nose] and xyz(frames[v].balls[nose])==expected
                checks.append({'pose':pose,'variant':v,'start_xyz':start,'control_end_xyz':end,'edited_end_xyz':expected,'changed_ids':changed})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_file':source.name,'source_sha256':SHA(raw),'head_id':head,'target_id':nose,'paths':paths,'input_hashes':hashes,'project_rows':variants,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games'/VERSION),'--game-version',VERSION,'--asset-root',str(OUT)])
    async with Client(transport) as client:
        caps=await client.call_tool('get_capabilities');(OUT/'capabilities.json').write_text(json.dumps(caps.data,indent=2))
        for case in cases:
            for v in ('identity','half','long'):
                for yaw in (0,90):
                    args={'before_path':case['paths']['control'],'after_path':case['paths'][v],'pose':'standing','yaw_degrees':yaw,'seed':0,'age':100,'fatness':50}
                    stem=f"{case['species']}-{v}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal == (v=='identity')
                    renders.append({'species':case['species'],'variant':v,'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':EXPERIMENT,'game_version':VERSION,'backend':'local stdio MCP','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','cases':cases,'comparisons':renders}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'experiments'/f'{EXPERIMENT.lower()}.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--game-version',choices=('petz3','petz4','petz5'),default='petz4')
    parser.add_argument('--alternate-breeds',action='store_true')
    args=parser.parse_args()
    VERSION=args.game_version
    if VERSION!='petz4':
        EXPERIMENT=f'PROJECT-003-{VERSION}'
        OUT=ROOT/'scratch/research'/EXPERIMENT.lower()
    if args.alternate_breeds:
        if VERSION!='petz4': parser.error('alternate breed experiment currently requires petz4')
        BREEDS={'Dogz':{'filename':'Dalmatian.dog','selector':'DM'},'Catz':{'filename':'Persian.cat','selector':'PR'}}
        EXPERIMENT='PROJECT-004'
        OUT=ROOT/'scratch/research/project-004'
    asyncio.run(main())
