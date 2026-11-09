"""Short Linez rows, explicit width fields and global default thickness."""
import asyncio,json,sys
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.connectors import ConnectorBall,build_line_block
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/line-004'
WIDTHS={'short25':(25,25),'full25':(25,25),'short100':(100,100),'full100':(100,100),'override25':(25,25),'empty100':(100,100)}
PAIRS=[('short25','full25'),('short100','full100'),('override25','full25'),('empty100','full100')]
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        marker_row=f'{head}, -35, -80, 0, 125, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        paths={};hashes={};rows={};checks=[]
        frozen=tuple(', '.join(str(int(v)) for v in vars(line).values()) for line in layer.appearance.lines)
        for v in ('marker',*WIDTHS):
            s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row)
            rows[v]=None if v=='marker' else (f'{head}, {marker}' if v in ('short25','short100','empty100') else f'{head}, {marker}, 0, -1, 244, 244, {WIDTHS[v][0]}, {WIDTHS[v][1]}, 0, 0')
            s['Default Linez Thickness']=() if v=='empty100' else ('25' if v in ('short25','full25') else '100',)
            s['Draw Linez Before Ballz']=('1',)
            s['Linez']=(*frozen,*((rows[v],) if rows[v] else ()))
            path=OUT/f'{species}-{v}{source.suffix}';paths[v]=path.name;hashes[v]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            shapes={v:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for v,a in assets.items()}
            for v,(st,et) in WIDTHS.items():
                assert shapes[v]==shapes['marker']
                line=assets[v].appearance.lines[-1]
                assert assets[v].appearance.lines[:-1]==layer.appearance.lines
                assert (line.fuzz,line.color,line.left_color,line.right_color,line.edge_mode,line.draw_after)==(0,-1,244,244,0,False)
                assert (line.start,line.end,line.start_thickness,line.end_thickness)==(head,marker,st,et)
                balls=tuple(ConnectorBall(b.x,b.y,b.radius,125) for b in shapes[v])
                block=build_line_block(line,balls)
                sw=st*min(2*balls[head].radius-1,127)//100
                ew=et*min(2*balls[marker].radius-1,127)//100
                assert (block is None)==(st==et==0)
                if block is not None: assert (block.start_thick,block.end_thick)==(max(sw,1),max(ew,1))
                checks.append({'pose':pose,'variant':v,'endpoint_radii':[balls[head].radius,balls[marker].radius],'preclamp_widths':[sw,ew],'block_widths':None if block is None else [block.start_thick,block.end_thick]})
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
                    assert equal
                    renders.append({'species':c['species'],'pair':[before,after],'controls':args,'png_sha256':SHA(png),'cells_equal':equal,'cell_hashes':[x['pixel_sha256'] for x in meta['cells']]})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'LINE-004','backend':'local stdio MCP plus direct block construction','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','widths':WIDTHS,'cases':cases,'comparisons':renders}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/line-004.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
