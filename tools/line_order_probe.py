"""Isolate Linez row draw flags and their global fallback."""
import asyncio,json,sys
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.lines import line_draw_schedule
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/line-003'
SETTINGS={'before':(1,0),'after':(1,1),'default_before':(1,-1),'default_after':(0,-1),'override_before':(0,0),'override_after':(0,1)}
PAIRS=[('before','after'),('before','default_before'),('after','default_after'),('before','override_before'),('after','override_after')]
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        frozen=tuple(', '.join(str(int(v)) for v in vars(line).values()) for line in layer.appearance.lines)
        marker_row=f'{head}, -35, -80, 0, 125, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        paths={};hashes={};rows={};checks=[]
        for v,(global_value,row_value) in SETTINGS.items():
            s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row)
            rows[v]=f'{head}, {marker}, 0, 125, 244, 244, 100, 100, 0, {row_value}'
            s['Linez']=(*frozen,rows[v]);s['Draw Linez Before Ballz']=(str(global_value),)
            path=OUT/f'{species}-{v}{source.suffix}';paths[v]=path.name;hashes[v]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            shapes={v:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for v,a in assets.items()}
            for v,a in assets.items():
                assert shapes[v]==shapes['before']
                assert a.appearance.lines[:-1]==layer.appearance.lines
                line=a.appearance.lines[-1];expected=v in ('after','default_after','override_after')
                assert line.draw_after==expected
                schedules=[]
                for order in ((head,marker),(marker,head)):
                    schedule=line_draw_schedule((line,),order,marker+1)
                    line_at=schedule.index(('line',0))
                    visits=[schedule.index(('circle',i)) for i in order]
                    assert (line_at>max(visits)) if expected else (line_at<min(visits))
                    schedules.append({'circle_order':order,'events':schedule})
                checks.append({'pose':pose,'variant':v,'parsed_draw_after':line.draw_after,'isolated_endpoint_schedules':schedules})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'marker_row':marker_row,'line_rows':rows,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after in PAIRS:
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal==((before,after)!=('before','after'))
                    renders.append({'species':c['species'],'pair':[before,after],'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'LINE-003','backend':'local stdio MCP plus direct scheduler','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','settings':SETTINGS,'cases':cases,'comparisons':renders}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/line-003.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
