"""Connector fuzz clamping and retained random tables."""
import asyncio, importlib.metadata, json, sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.appearance.core import Line
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.connectors import ConnectorBall, build_line_block
from petz_renderer.rendering.texture import TiledTexture, remap_texture
from research_common import ROOT, SHA, adult, write_copy, save_result
OUT=ROOT/'scratch/research/line-007'
VARIANTS={'negative':-1,'zero':0,'one':1,'seven':7,'eight':8}
PAIRS=[('negative','zero',True),('seven','eight',True),('zero','one',False),('zero','seven',False)]
def synthetic():
    from petz_renderer.rendering.framebuffer import Framebuffer
    from petz_renderer.rendering.lines import LineBlock,LineRenderer
    rows=[]
    for endpoints in ((20,20,80,70),(80,70,20,20),(20,50,80,50),(50,20,50,80)):
        for widths in ((12,12),(20,6)):
            outputs={}
            for name,fuzz in VARIANTS.items():
                block=LineBlock(*endpoints,start_thick=widths[0],end_thick=widths[1],color=220,left_color=180,right_color=200,edge_mode=0,fuzz=fuzz)
                renderer=LineRenderer(seed=1);fb=Framebuffer(100,100)
                renderer.draw(fb,block);first=fb.pixels;state=renderer._state
                tables=[list(t) for t in renderer._tables]
                fb.clear(0);renderer.draw(fb,block)
                assert fb.pixels==first and renderer._state==state and renderer._tables==tables
                fresh=Framebuffer(100,100);LineRenderer(seed=1).draw(fresh,block)
                assert fresh.pixels==first
                clamped=max(0,min(7,fuzz))
                assert all(not t for i,t in enumerate(tables) if i!=clamped)
                if clamped==0:assert state==1
                else:assert len(tables[clamped])>0 and state!=1
                outputs[name]=first
                rows.append({'endpoints':endpoints,'widths':widths,'variant':name,'fuzz':fuzz,'clamped_fuzz':clamped,'indexed_sha256':SHA(first),'rng_after_first':state,'table_lengths':[len(t) for t in tables],'repeat_equal':True,'fresh_equal':True})
            assert outputs['negative']==outputs['zero'] and outputs['seven']==outputs['eight']
    return rows
async def main():
    OUT.mkdir(parents=True,exist_ok=False); blocks=synthetic();cases=[];renders=[]
    package=Path(petz_renderer.__file__).parent
    source_hashes={p:SHA((package/p).read_bytes()) for p in ('appearance/core.py','rendering/connectors.py','rendering/shading.py','rendering/texture.py','rendering/lines.py')}
    for p,h in source_hashes.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    engines={str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in sorted((ROOT/'games/petz4').glob('Resource/* 4 Rez.dll'))}
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        marker_row=f'{head}, -35, -80, 0, 200, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        frozen=tuple(', '.join(str(int(x)) for x in vars(line).values()) for line in layer.appearance.lines)
        paths={};hashes={};rows={};checks=[]
        for name,fuzz in VARIANTS.items():
            s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row)
            s['Color Info Override']=(*base.get('Color Info Override',()),f'{head}, 180, -1, -1')
            rows[name]=f'{head}, {marker}, {fuzz}, 220, 180, 200, 100, 100, 0, 1'
            s['Linez']=(*frozen,*((rows[name],) if rows[name] else ()))
            path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={n:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for n,p in paths.items()}
            shapes={n:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for n,a in assets.items()}
            for n,a in assets.items():
                assert shapes[n]==shapes['zero']
                assert a.appearance.lines[:-1]==layer.appearance.lines
                assert a.appearance.lines[-1].fuzz==VARIANTS[n]
                checks.append({'pose':pose,'variant':n,'fuzz':VARIANTS[n]})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'marker_row':marker_row,'line_rows':rows,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after,expected in PAIRS:
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal==expected,(stem,equal,expected)
                    renders.append({'species':c['species'],'pair':[before,after],'controls':args,'png_sha256':SHA(png),'cells_equal':equal,'cell_hashes':[x['pixel_sha256'] for x in meta['cells']]})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'LINE-007','backend':'local stdio MCP and synthetic Python blocks','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':source_hashes,'engine_hashes':engines,'synthetic':blocks,'cases':cases,'comparisons':renders}
    for path in (OUT/'report.json',ROOT/'experiments/line-007.json'):path.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
