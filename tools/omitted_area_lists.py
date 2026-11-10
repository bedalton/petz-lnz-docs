"""AREA-006: omitted-marker list reassignment, using copy-only breed controls."""
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
OUT=ROOT/'scratch/research/area-006'
SETTINGS={'visible':([],3,False,3),'omitted':([],3,True,0),'omitted_body':(['Body Balls'],3,True,1),'omitted_head':(['Head Balls'],3,True,8),'omitted_both':(['Body Balls','Head Balls'],3,True,8),'omitted_head_v1':(['Head Balls'],1,True,0),'visible_head':(['Head Balls'],3,False,8)}
async def main():
    OUT.mkdir(parents=True,exist_ok=False); cases=[]; renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head
        marker=67+len(layer.appearance.add_balls)
        paths={}; hashes={}; checks=[]; section_orders={}
        for variant,(lists,version,omitted,expected) in SETTINGS.items():
            s=dict(base)
            s['Add Ball']=(*base['Add Ball'],f'{head}, -36, -80, 0, 125, 244, -1, 0, -1, -1, 20, 8, 0, -1, -1')
            s['Linez']=(*layer.sections.get('Linez',()),f'0, {marker}, 0, 125, 244, 244, 10, 10, 0, 1')
            s['Lnz Version']=(str(version),)
            if omitted:s['Omissions']=(*base.get('Omissions',()),str(marker))
            # Freeze effective stock lists, then append target membership.
            from petz_renderer.appearance.core import BODY_AREA_SECTIONS
            for section in BODY_AREA_SECTIONS:
                if section:
                    s.pop(section,None)
            for section in BODY_AREA_SECTIONS:
                if section and section not in lists:
                    s[section]=layer.sections.get(section,())
            for section in lists:
                s[section]=(*layer.sections.get(section,()),str(marker))
            section_orders[variant]=[k for k in s if k in BODY_AREA_SECTIONS]
            path=OUT/f'{species}-{variant}{source.suffix}';paths[variant]=path.name;hashes[variant]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            for variant,(_,version,omitted,expected) in SETTINGS.items():
                a=load_breed_assets(resolver,paths[variant],pose=pose,seed=0,age=100,fatness=50)
                areas=body_areas(a.appearance); assert areas[marker]==expected,(species,pose,variant,areas[marker])
                neutral=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50)
                rotated=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,head_rotation=32)
                xyz=lambda b:(b.x,b.y,b.z)
                assert neutral[marker].visible==rotated[marker].visible== (not omitted)
                incident=sum(marker in (line.start,line.end) for line in a.appearance.lines)
                assert incident== (0 if omitted else 1) # assembly drops omitted endpoints
                rotated_changed=xyz(neutral[marker])!=xyz(rotated[marker])
                checks.append({'pose':pose,'variant':variant,'marker_area':areas[marker],'lnz_version':a.appearance.lnz_version,'omitted':omitted,'incident_parsed_lines':incident,'rotation_changed':rotated_changed,'neutral_marker':asdict(neutral[marker]),'head_rotated_marker':asdict(rotated[marker])})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'list_section_order':section_orders,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after in (('omitted','omitted_head'),('omitted_head','omitted_body'),('visible_head','omitted_head')):
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal==(before!='visible_head'),(c['species'],before,after,yaw)
                    renders.append({'species':c['species'],'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    print(stem,equal,flush=True)
    report={'experiment':'AREA-006','backend':'local stdio MCP default head pose; direct Python head rotation32','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','settings':SETTINGS,'cases':cases,'comparisons':renders}
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text())
    resolver=ResourceResolver((ROOT/'games/petz4',))
    for path,expected in provenance['shared_engine_hashes']['petz4'].items():
        assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    installed_source=Path(evaluation.__file__).read_bytes()
    assert installed_source==(ROOT/'petz-renderer-mcp/src/petz_renderer/appearance/evaluation.py').read_bytes()
    report['evaluation_source_sha256']=SHA(installed_source)
    report['shared_engine_hashes']=provenance['shared_engine_hashes']['petz4']
    report['dependency_versions']={name:importlib.metadata.version(name) for name in ('fastmcp','numpy','Pillow','pydantic')}
    for target in (OUT/'report.json',ROOT/'experiments/area-006.json'):target.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
