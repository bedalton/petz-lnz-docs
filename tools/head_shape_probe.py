"""Separate Head Enlargement size and spacing effects with geometry/MCP evidence."""
import asyncio,json,sys
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.positions import modify_positions
from petz_renderer.rendering.pose import posed_geometry
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/head-001'

def xyz(b):return [b.x,b.y,b.z]

def prepare():
    cases=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,sections,master,_=adult(species)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        values=[int(line.split()[0]) for line in sections['Head Enlargement']]
        assert len(values)==2
        paths={};inputs={}
        for variant,deltas in [('control',(0,0)),('first',(25,0)),('second',(0,25))]:
            changed=dict(sections)
            pair=[v+d for v,d in zip(values,deltas)]
            changed['Head Enlargement']=tuple(str(v) for v in pair)
            path=OUT/f'{species}-{variant}{source.suffix}'
            inputs[variant]={'pair':pair,'sha256':write_copy(raw,leaf,changed,path)};paths[variant]=path.name
        geometry=[]
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            baseline=assets['control']; raw_control=modify_positions(baseline.appearance,baseline.frame)
            base_radii=posed_geometry(baseline.appearance,baseline.sizes,baseline.frame,fatness=50)
            for variant in ('first','second'):
                asset=assets[variant]; frame=modify_positions(asset.appearance,asset.frame)
                shape=posed_geometry(asset.appearance,asset.sizes,asset.frame,fatness=50)
                geometry.append({'pose':pose,'variant':variant,'raw_position_changed_ids':[i for i,(a,b) in enumerate(zip(raw_control.balls,frame.balls)) if xyz(a)!=xyz(b)],'radius_changed_ids':[i for i,(a,b) in enumerate(zip(base_radii,shape)) if a.radius!=b.radius],'raw_positions':[xyz(b) for b in frame.balls],'radii':[b.radius for b in shape]})
            first,second=[posed_geometry(assets[v].appearance,assets[v].sizes,assets[v].frame,fatness=50) for v in ('first','second')]
            assert [b.radius for b in first]==[b.radius for b in second]
        (OUT/f'{species}-geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
        cases.append({'species':species,'source_sha256':SHA(raw),'inputs':inputs,'paths':paths,'geometry_summary':[{k:v for k,v in g.items() if k not in ('raw_positions','radii')} for g in geometry]})
    return cases

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cases=prepare();renders=[]
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for case in cases:
            for variant in ('first','second'):
                for yaw in (0,90):
                    args={'before_path':case['paths']['control'],'after_path':case['paths'][variant],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{case['species']}-{variant}-yaw{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    renders.append({'species':case['species'],'variant':variant,'controls':args,'png_sha256':SHA(png)})
                    (OUT/'comparisons.json').write_text(json.dumps(renders,indent=2)+'\n')
                    print(stem,flush=True)
    report={'experiment':'HEAD-001','cases':cases,'comparisons':renders,'renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'backend':'local stdio MCP comparisons; direct same-package numerical geometry'}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'experiments/head-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
