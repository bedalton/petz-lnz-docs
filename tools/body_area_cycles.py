"""AREA-005: anchored-cycle evaluation and late overrides, using copy-only breed controls."""
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
OUT=ROOT/'scratch/research/area-005'
EDGES=[(0,1),(1,2),(2,0),(2,3)]
SETTINGS={'forward':([0,1,2,3],False,False,[8,8,3,3]),'reverse_ids':([3,2,1,0],False,False,[3,3,3,3]),'interleaved':([0,2,1,3],False,False,[8,3,3,3]),'reverse_lines':([0,1,2,3],False,False,[8,8,3,3]),'omit_anchor':([3,2,1,0],True,False,[8,8,8,0]),'late_head_list':([3,2,1,0],False,True,[3,3,8,3])}
async def main():
    OUT.mkdir(parents=True,exist_ok=False); cases=[]; renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head
        first=67+len(layer.appearance.add_balls)
        paths={}; hashes={}; checks=[]; id_maps={}
        for variant,(order,omitted,listed,expected) in SETTINGS.items():
            s=dict(base)
            ids={semantic:first+i for i,semantic in enumerate(order)}
            id_maps[variant]=ids
            rows=[f'{head}, {i*28-36}, -80, 0, 125, 244, -1, 0, -1, -1, 20, {3 if i==3 else 8}, 0, -1, -1' for i in order]
            s['Add Ball']=(*base['Add Ball'],*rows)
            edges=list(reversed(EDGES)) if variant=='reverse_lines' else EDGES
            if omitted:s['Omissions']=(*base.get('Omissions',()),str(ids[3]))
            if listed:
                s['Lnz Version']=('3',)
                s['Head Balls']=(*layer.sections.get('Head Balls',()),str(ids[2]))
            s['Linez']=(*layer.sections.get('Linez',()),*(f'{ids[a]}, {ids[b]}, 0, 125, 244, 244, 10, 10, 0, 1' for a,b in edges))
            path=OUT/f'{species}-{variant}{source.suffix}';paths[variant]=path.name;hashes[variant]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            for variant,(_,_,_,expected) in SETTINGS.items():
                a=load_breed_assets(resolver,paths[variant],pose=pose,seed=0,age=100,fatness=50)
                ids=id_maps[variant]; areas=body_areas(a.appearance)
                observed=[areas[ids[i]] for i in range(4)]
                assert observed==expected,(species,pose,variant,observed)
                neutral=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50)
                rotated=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,head_rotation=32)
                xyz=lambda b:(b.x,b.y,b.z)
                for i,area in enumerate(expected):
                    assert (xyz(neutral[ids[i]])!=xyz(rotated[ids[i]]))==(area==8)
                checks.append({'pose':pose,'variant':variant,'semantic_areas':observed,'neutral_markers':[asdict(neutral[ids[i]]) for i in range(4)],'head_rotated_markers':[asdict(rotated[ids[i]]) for i in range(4)]})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'id_maps':id_maps,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after in (('forward','reverse_ids'),('reverse_ids','late_head_list')):
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal,(c['species'],before,after,yaw)
                    renders.append({'species':c['species'],'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    print(stem,equal,flush=True)
    report={'experiment':'AREA-005','backend':'local stdio MCP default head pose; direct Python head rotation32','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','edges':EDGES,'settings':SETTINGS,'cases':cases,'comparisons':renders}
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text())
    resolver=ResourceResolver((ROOT/'games/petz4',))
    for path,expected in provenance['shared_engine_hashes']['petz4'].items():
        assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    installed_source=Path(evaluation.__file__).read_bytes()
    assert installed_source==(ROOT/'petz-renderer-mcp/src/petz_renderer/appearance/evaluation.py').read_bytes()
    report['evaluation_source_sha256']=SHA(installed_source)
    report['shared_engine_hashes']=provenance['shared_engine_hashes']['petz4']
    report['dependency_versions']={name:importlib.metadata.version(name) for name in ('fastmcp','numpy','Pillow','pydantic')}
    for target in (OUT/'report.json',ROOT/'experiments/area-005.json'):target.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
