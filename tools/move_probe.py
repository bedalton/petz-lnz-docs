"""Test Move reference rotation, zero vectors and repeated target rows."""
import asyncio,json,sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.positions import modify_positions
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/move-001'
def xyz(b):return (b.x,b.y,b.z)

def prepare():
    cases=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,masterfile,master=adult(species)
        head,chest=(52,50) if species=='Dogz' else (24,6)
        variants={'control':(), 'zero':(f'{head}, 0, 0, 0, {chest}',),'implicit':(f'{head}, 20, 7, -3',),'explicit':(f'{head}, 20, 7, -3, {head}',),'chest':(f'{head}, 20, 7, -3, {chest}',),'twice':(f'{head}, 20, 7, -3, {head}',f'{head}, 20, 7, -3, {head}')}
        paths={};hashes={}
        for variant,rows in variants.items():
            sections=dict(base);sections['Move']=(*base.get('Move',()),*rows)
            path=OUT/f'{species}-{variant}{source.suffix}'
            hashes[variant]=write_copy(raw,leaf,sections,path);paths[variant]=path.name
        geometry=[];resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            frames={v:modify_positions(a.appearance,a.frame) for v,a in assets.items()}
            baseframe=frames['control']
            assert frames['zero']==baseframe
            assert frames['implicit']==frames['explicit']
            for v,frame in frames.items():
                changed=[i for i,(a,b) in enumerate(zip(baseframe.balls,frame.balls)) if xyz(a)!=xyz(b)]
                assert not changed if v in ('control','zero') else head in changed
                d=[b-a for a,b in zip(xyz(baseframe.balls[head]),xyz(frame.balls[head]))]
                double=[b-a for a,b in zip(xyz(baseframe.balls[head]),xyz(frames['twice'].balls[head]))]
                if v=='explicit': assert double==[2*x for x in d]
                geometry.append({'pose':pose,'variant':v,'changed_base_ball_ids':changed,'head_delta_raw':d,'reference_rotation':{str(i):[assets[v].frame.balls[i].rot_byte6,assets[v].frame.balls[i].rot_byte7,assets[v].frame.balls[i].rot_byte8] for i in (head,chest)}})
        cases.append({'species':species,'source_sha256':SHA(raw),'input_hashes':hashes,'added_rows':variants,'paths':paths,'geometry':geometry})
    return cases

async def main():
    OUT.mkdir(parents=True,exist_ok=True);cases=prepare();comparisons=[]
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for case in cases:
            for before,after,pose in [('control','zero','sitting'),('implicit','explicit','sitting'),('explicit','chest','sitting'),('explicit','chest','lying')]:
                args={'before_path':case['paths'][before],'after_path':case['paths'][after],'pose':pose,'seed':0,'age':100,'fatness':50,'yaw_degrees':90}
                stem=f"{case['species']}-{before}-{after}-{pose}"
                png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                if after in ('zero','explicit'): assert equal
                comparisons.append({'species':case['species'],'before':before,'after':after,'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                (OUT/'progress.json').write_text(json.dumps(comparisons,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'MOVE-001','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'cases':cases,'comparisons':comparisons}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'experiments/move-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
