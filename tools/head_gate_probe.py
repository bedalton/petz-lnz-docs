"""Test the A==100 Head Enlargement position gate with private copies."""
import asyncio,json,sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.positions import modify_positions
from petz_renderer.rendering.pose import posed_geometry
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/head-002'
PAIRS={'neutral':(100,0),'gate':(100,25),'above':(101,25),'below':(99,25)}
def xyz(b):return (b.x,b.y,b.z)

async def main():
    OUT.mkdir(parents=True,exist_ok=True);cases=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,_,_=adult(species);paths={};hashes={};checks=[]
        for variant,pair in PAIRS.items():
            sections=dict(base);sections['Head Enlargement']=tuple(str(v) for v in pair)
            path=OUT/f'{species}-{variant}{source.suffix}'
            hashes[variant]=write_copy(raw,leaf,sections,path);paths[variant]=path.name
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            frames={v:modify_positions(a.appearance,a.frame) for v,a in assets.items()}
            shapes={v:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for v,a in assets.items()}
            assert frames['gate']==frames['neutral']
            assert frames['above']!=frames['gate'] and frames['below']!=frames['gate']
            for v in PAIRS:
                changed=[i for i,(a,b) in enumerate(zip(frames['neutral'].balls,frames[v].balls)) if xyz(a)!=xyz(b)]
                radii=[i for i,(a,b) in enumerate(zip(shapes['neutral'],shapes[v])) if a.radius!=b.radius]
                checks.append({'pose':pose,'variant':v,'raw_position_changed_ids':changed,'radius_changed_ids':radii})
                if v=='gate': assert not changed and radii
        cases.append({'species':species,'source_sha256':SHA(raw),'paths':paths,'input_hashes':hashes,'geometry_checks':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    renders=[]
    async with Client(transport) as client:
        for case in cases:
            for before,after in [('neutral','gate'),('gate','above')]:
                args={'before_path':case['paths'][before],'after_path':case['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':0}
                stem=f"{case['species']}-{before}-{after}"
                png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                renders.append({'species':case['species'],'controls':args,'png_sha256':SHA(png),'cell_hashes':[c['pixel_sha256'] for c in meta['cells']]})
                (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'HEAD-002','pairs':PAIRS,'renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'cases':cases,'comparisons':renders}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/head-002.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
