"""AREA-002: ordered conflicting neighbors, using copy-only breed controls."""
import asyncio, json, sys
import importlib.metadata
from pathlib import Path
import petz_renderer.appearance.evaluation as evaluation
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.appearance.evaluation import body_areas
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/area-002'
SETTINGS={'three_four':([3,4],False,None,3),'four_three':([4,3],False,None,4),'reverse_endpoints':([3,4],True,None,3),'skip_one_eight':([1,8,4,3],False,None,4),'omit_first':([3,4],False,3,4),'only_ignored':([1,8],False,None,8)}
async def main():
    OUT.mkdir(parents=True,exist_ok=False); cases=[]; renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head
        first=67+len(layer.appearance.add_balls)
        neighbors={area:first+i for i,area in enumerate((1,3,4,8))}; marker=first+4
        paths={}; hashes={}; checks=[]
        for variant,(order,reverse,omitted,expected) in SETTINGS.items():
            s=dict(base)
            rows=[f'{head}, {i*12}, -50, 0, 125, 244, -1, 0, -1, -1, 12, {area}, 0, -1, -1' for i,area in enumerate((1,3,4,8))]
            rows.append(f'{head}, -36, -80, 0, 125, 244, -1, 0, -1, -1, 20, 8, 0, -1, -1')
            s['Add Ball']=(*base['Add Ball'],*rows)
            pairs=[(marker,neighbors[a]) if reverse else (neighbors[a],marker) for a in order]
            s['Linez']=(*layer.sections.get('Linez',()),*(f'{a}, {b}, 0, 125, 244, 244, 10, 10, 0, 1' for a,b in pairs))
            if omitted is not None:s['Omissions']=(*base.get('Omissions',()),str(neighbors[omitted]))
            path=OUT/f'{species}-{variant}{source.suffix}';paths[variant]=path.name;hashes[variant]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            for variant,(_,_,_,expected) in SETTINGS.items():
                a=load_breed_assets(resolver,paths[variant],pose=pose,seed=0,age=100,fatness=50)
                areas=body_areas(a.appearance); assert areas[marker]==expected,(species,pose,variant,areas[marker])
                neutral=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50)
                rotated=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,head_rotation=32)
                xyz=lambda b:(b.x,b.y,b.z)
                assert (xyz(neutral[marker])!=xyz(rotated[marker]))==(expected==8)
                checks.append({'pose':pose,'variant':variant,'marker_area':areas[marker],'neighbor_areas':{k:areas[v] for k,v in neighbors.items()},'neutral_marker':asdict(neutral[marker]),'head_rotated_marker':asdict(rotated[marker])})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'neighbor_ids':neighbors,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for after in ('four_three','reverse_endpoints'):
                for yaw in (0,90):
                    args={'before_path':c['paths']['three_four'],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    renders.append({'species':c['species'],'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    print(stem,equal,flush=True)
    report={'experiment':'AREA-002','backend':'local stdio MCP default head pose; direct Python head rotation32','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','settings':SETTINGS,'cases':cases,'comparisons':renders}
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text())
    resolver=ResourceResolver((ROOT/'games/petz4',))
    for path,expected in provenance['shared_engine_hashes']['petz4'].items():
        assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    installed_source=Path(evaluation.__file__).read_bytes()
    assert installed_source==(ROOT/'petz-renderer-mcp/src/petz_renderer/appearance/evaluation.py').read_bytes()
    report['evaluation_source_sha256']=SHA(installed_source)
    report['shared_engine_hashes']=provenance['shared_engine_hashes']['petz4']
    report['dependency_versions']={name:importlib.metadata.version(name) for name in ('fastmcp','numpy','Pillow','pydantic')}
    for target in (OUT/'report.json',ROOT/'experiments/area-002.json'):target.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
