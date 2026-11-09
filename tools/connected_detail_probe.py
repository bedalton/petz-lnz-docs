"""Connect a copy-only added marker with Linez; test endpoint omissions."""
import asyncio,json,sys
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/line-001'
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        assert len(base['Add Ball'])==len(layer.appearance.add_balls)
        marker_row=f'{head}, -35, -80, 0, 125, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        line_row=f'{head}, {marker}, 0, 125, 244, 244, 100, 100, 0, 1'
        paths={};hashes={};checks=[]
        for v in ('marker','connected','marker_hide_marker','connected_hide_marker','marker_hide_head','connected_hide_head'):
            s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row)
            s['Linez']=(*layer.sections.get('Linez',()),*((line_row,) if v.startswith('connected') else ()))
            if '_hide_' in v:
                omitted=marker if v.endswith('_marker') else head
                s['Omissions']=(*base.get('Omissions',()),str(omitted))
            path=OUT/f'{species}-{v}{source.suffix}'
            hashes[v]=write_copy(raw,leaf,s,path);paths[v]=path.name
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            shapes={v:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for v,a in assets.items()}
            for suffix in ('','_hide_marker','_hide_head'):
                before,after='marker'+suffix,'connected'+suffix
                a,b=assets[before],assets[after]
                assert shapes[before]==shapes[after]
                assert len(b.appearance.lines)-len(a.appearance.lines)==(1 if not suffix else 0)
                assert len(b.appearance.add_balls)==len(assets['marker'].appearance.add_balls)
                checks.append({'pose':pose,'pair':[before,after],'line_counts':[len(a.appearance.lines),len(b.appearance.lines)],'marker_visible':shapes[after][marker].visible,'head_visible':shapes[after][head].visible,'marker_radius':shapes[after][marker].radius})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'marker_row':marker_row,'line_row':line_row,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for suffix in ('','_hide_marker','_hide_head'):
                for yaw in (0,90):
                    before,after='marker'+suffix,'connected'+suffix
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-connected{suffix}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal==bool(suffix)
                    renders.append({'species':c['species'],'pair':[before,after],'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'LINE-001','backend':'local stdio MCP','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','cases':cases,'comparisons':renders}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'experiments/line-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
