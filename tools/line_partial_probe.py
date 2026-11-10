"""Copy-only Linez prefixes of lengths 3–9 versus fully resolved rows."""
import asyncio,importlib.metadata,json,sys
from dataclasses import asdict
from pathlib import Path
import petz_renderer
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.core import Line
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/line-010'
PROFILES={'a':{'thickness':25,'before':1},'b':{'thickness':73,'before':0}}
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];comparisons=[]
    installed=Path(petz_renderer.__file__).parent
    sources={p:SHA((installed/p).read_bytes()) for p in ('appearance/core.py','appearance/layers.py','rendering/lines.py','rendering/connectors.py')}
    for p,h in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/p).read_bytes())==h
    engines={str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in sorted((ROOT/'games/petz4').glob('Resource/* 4 Rez.dll'))}
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species);layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        marker_row=f'{head}, -35, -80, 0, 200, 244, -1, 0, -1, -1, 20, 0, 0, -1, -1'
        frozen=tuple(', '.join(str(int(x)) for x in vars(line).values()) for line in layer.appearance.lines)
        paths={};hashes={};rows={};expected={};checks=[];pairs=[]
        full=[head,marker,1,220,180,200,33,67,1,1]
        for profile,control in PROFILES.items():
            for length in range(3,10):
                prefix=full[:length]
                defaults=[0,0,0,-1,244,244,control['thickness'],control['thickness'],-2,-1]
                resolved=prefix+defaults[length:]
                resolved[8]=(-1 if resolved[4]==resolved[5]==-1 else 0) if resolved[8]==-2 else resolved[8]
                resolved[9]=(control['before']==0) if resolved[9]==-1 else bool(resolved[9])
                line=Line(*resolved)
                pair=[]
                for kind,values in (('short',prefix),('full',list(vars(line).values()))):
                    name=f'{kind}{length}{profile}';pair.append(name)
                    s=dict(base);s['Add Ball']=(*base['Add Ball'],marker_row)
                    s['Color Info Override']=(*base.get('Color Info Override',()),f'{head}, 180, -1, -1')
                    s['Default Linez Thickness']=(str(control['thickness']),)
                    s['Draw Linez Before Ballz']=(str(control['before']),)
                    rows[name]=', '.join(str(int(x)) for x in values);s['Linez']=(*frozen,rows[name])
                    path=OUT/f'{species}-{name}{source.suffix}';paths[name]=path.name;hashes[name]=write_copy(raw,leaf,s,path);expected[name]=asdict(line)
                pairs.append(pair)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            reference=None
            for name,path in paths.items():
                assets=load_breed_assets(resolver,path,pose=pose,seed=0,age=100,fatness=50)
                shape=posed_geometry(assets.appearance,assets.sizes,assets.frame,fatness=50)
                if reference is None:reference=shape
                assert shape==reference
                assert assets.appearance.lines[:-1]==layer.appearance.lines
                assert asdict(assets.appearance.lines[-1])==expected[name]
                checks.append({'pose':pose,'variant':name,'resolved':expected[name]})
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'marker_row':marker_row,'paths':paths,'input_hashes':hashes,'line_rows':rows,'geometry':checks,'pairs':pairs})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after in c['pairs']:
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    hashes=[x['pixel_sha256'] for x in meta['cells']];assert hashes[0]==hashes[1],stem
                    comparisons.append({'species':c['species'],'pair':[before,after],'controls':args,'png_sha256':SHA(png),'cells_equal':True,'cell_hashes':hashes})
                    (OUT/'progress.json').write_text(json.dumps(comparisons,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'LINE-010','backend':'local stdio MCP plus resolved breed appearance/geometry','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'profiles':PROFILES,'source_hashes':sources,'engine_hashes':engines,'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','Pillow')},'cases':cases,'comparisons':comparisons}
    for p in (OUT/'report.json',ROOT/'experiments/line-010.json'):p.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
