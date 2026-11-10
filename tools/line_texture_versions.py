"""Texture routing in Petz 3/5 compared with Petz 4 controls."""
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
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.connectors import ConnectorBall, build_line_block
from petz_renderer.rendering.texture import TiledTexture, remap_texture
from research_common import ROOT, SHA, adult, write_copy, save_result
OUT=ROOT/'scratch/research/line-016'
VARIANTS={'head_texture':(-1,False),'end_plain':(-2,False),'explicit_plain':(125,False),'reverse_head':(-2,True),'reverse_end':(-1,True)}
PAIRS=[('head_texture','explicit_plain',False),('end_plain','explicit_plain',True),('reverse_head','head_texture',True),('reverse_end','explicit_plain',True)]
def synthetic():return []
async def run(version):
    global OUT
    OUT=ROOT/'scratch/research/line-016'/version
    OUT.mkdir(parents=True,exist_ok=False); blocks=synthetic();cases=[];renders=[]
    package=Path(petz_renderer.__file__).parent
    source_hashes={p:SHA((package/p).read_bytes()) for p in ('appearance/core.py','rendering/connectors.py','rendering/shading.py','rendering/texture.py')}
    for p,h in source_hashes.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    engines={str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in sorted((ROOT/'games'/version).glob(f'Resource/* {version[-1]} Rez.dll'))}
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species,version)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        head_texture=layer.appearance.balls[head].texture
        assert head_texture>=0
        marker_row=f'{head}, -35, -80, 0, 125, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        frozen=tuple(', '.join(str(int(x)) for x in vars(line).values()) for line in layer.appearance.lines)
        paths={};hashes={};rows={};checks=[]
        for name,(color,reverse) in VARIANTS.items():
            s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row)
            s['Color Info Override']=(*base.get('Color Info Override',()),f'{head}, 125, -1, {head_texture}')
            a,b=(marker,head) if reverse else (head,marker)
            rows[name]=f'{a}, {b}, 0, {color}, 244, 244, 100, 100, 0, 1'
            s['Linez']=(*frozen,rows[name])
            path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games'/version,OUT),game_version=version)
        for pose in ('standing','sitting','lying'):
            assets={n:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for n,p in paths.items()}
            shapes={n:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for n,a in assets.items()}
            for n,a in assets.items():
                assert shapes[n]==shapes['head_texture']
                assert a.appearance.lines[:-1]==layer.appearance.lines
                assert a.appearance.lines[-1].color==VARIANTS[n][0]
                prepared=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50)
                endpoints=tuple(b.endpoint for b in prepared.balls)
                block=build_line_block(a.appearance.lines[-1],endpoints);assert block is not None
                textured=n in ('head_texture','reverse_head')
                assert (block.paint is not None)==textured
                texture=a.textures[head_texture];assert texture is not None
                if textured:assert block.paint==remap_texture(texture,block.color,has_levels=a.appearance.textures[head_texture].has_levels,own_level=a.appearance.textures[head_texture].own_level)
                checks.append({'pose':pose,'variant':n,'line_color':a.appearance.lines[-1].color,'block_color':block.color,'paint_present':block.paint is not None,'texture_index':head_texture,'texture_pixels_sha256':SHA(texture.pixels),'paint_pixels_sha256':None if block.paint is None else SHA(block.paint.texture.pixels)})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'marker_row':marker_row,'line_rows':rows,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version',version,'--game-root',str(ROOT/'games'/version),'--asset-root',str(OUT)])
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
    report={'experiment':'LINE-016','game_version':version,'backend':'local stdio MCP plus asset-backed connector block checks','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow')},'source_hashes':source_hashes,'engine_hashes':engines,'synthetic':blocks,'cases':cases,'comparisons':renders}
    baseline=json.loads((ROOT/'experiments/line-013.json').read_text())
    for c,b in zip(cases,baseline['cases'],strict=True):
        assert c['species']==b['species']
        c['texture_and_block_checks_match_petz4']=c['geometry']==b['geometry']
    matches=[]
    for r,b in zip(renders,baseline['comparisons'],strict=True):
        assert (r['species'],r['pair'],r['controls']['yaw_degrees'])==(b['species'],b['pair'],b['controls']['yaw_degrees'])
        matches.append({'species':r['species'],'pair':r['pair'],'yaw_degrees':r['controls']['yaw_degrees'],'png_matches_petz4':r['png_sha256']==b['png_sha256'],'cells_match_petz4':r['cell_hashes']==b['cell_hashes']})
    report['cross_version_matches']=matches
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
async def main():
    root=ROOT/'scratch/research/line-016';root.mkdir(parents=True,exist_ok=False)
    reports=[]
    for version in ('petz3','petz5'):reports.append(await run(version))
    report={'experiment':'LINE-016','backend':'local stdio MCP per game version plus asset-backed texture/block checks','baseline_manifest':'line-013.json','baseline_manifest_sha256':SHA((ROOT/'experiments/line-013.json').read_bytes()),'reports':reports}
    for path in (root/'report.json',ROOT/'experiments/line-016.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print([(r['game_version'],sum(x['png_matches_petz4'] for x in r['cross_version_matches'])) for r in reports])
if __name__=='__main__':asyncio.run(main())
