"""Connection-derived body area and explicit head-rotation response."""
import asyncio,json,sys
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
OUT=ROOT/'scratch/research/area-001'
SETTINGS={'inherit':(0,None,None),'head_link':(0,'head',None),'ankle_link':(0,0,None),'explicit8':(8,0,None),'explicit1':(1,0,None),'ankle_omitted':(0,0,0),'marker_omitted':(0,0,'marker')}
def xyz(b):return (b.x,b.y,b.z)
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        expected_ankle=3  # Effective sampled breeds override the built-in Catz area 2.
        assert body_areas(layer.appearance)[head]==8 and body_areas(layer.appearance)[0]==expected_ankle
        paths={};hashes={};checks=[];rows={}
        for v,(area,other,omitted) in SETTINGS.items():
            s=dict(base);rows[v]=f'{head}, -36, -80, 0, 125, 244, -1, 0, -1, -1, 20, {area}, 0, -1, -1'
            s['Add Ball']=(*base['Add Ball'],rows[v]);s['Linez']=layer.sections.get('Linez',())
            if other is not None:
                endpoint=head if other=='head' else other
                s['Linez']=(*s['Linez'],f'{endpoint}, {marker}, 0, 125, 244, 244, 10, 10, 0, 1')
            if omitted is not None:
                s['Omissions']=(*base.get('Omissions',()),str(marker if omitted=='marker' else omitted))
            path=OUT/f'{species}-{v}{source.suffix}';paths[v]=path.name;hashes[v]=write_copy(raw,leaf,s,path)
        expected={'inherit':8,'head_link':8,'ankle_link':expected_ankle,'explicit8':expected_ankle,'explicit1':1,'ankle_omitted':8,'marker_omitted':0}
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            for v,a in assets.items():
                areas=body_areas(a.appearance);assert areas[marker]==expected[v]
                neutral=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50)
                rotated=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,head_rotation=32)
                changed=xyz(neutral[marker])!=xyz(rotated[marker])
                assert changed==(expected[v]==8)
                checks.append({'pose':pose,'variant':v,'computed_marker_area':areas[marker],'neutral_marker':asdict(neutral[marker]),'head_rotated_marker':asdict(rotated[marker]),'head_rotation_units':32})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'ankle_id':0,'ankle_area':expected_ankle,'marker_rows':rows,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for after in ('explicit8','explicit1'):
                for yaw in (0,90):
                    args={'before_path':c['paths']['ankle_link'],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-ankle_link-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256'];assert equal
                    renders.append({'species':c['species'],'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'AREA-001','backend':'local stdio MCP default head pose; direct Python head rotation','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','settings':SETTINGS,'cases':cases,'comparisons':renders}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/area-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
