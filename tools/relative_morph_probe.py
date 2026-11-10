"""MORPH-002: relative-size additions under explicit group percentages."""
import asyncio, json, sys, importlib.metadata
from pathlib import Path
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.morphs import evaluate_morphs
from petz_renderer.rendering.rotation import _round
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/morph-002'
SETTINGS={'static_relative20':(0,20,True),'static_relative0':(0,0,True),'group_relative20':(15,20,True),'group_ordinary20':(15,20,False),'static_ordinary20':(0,20,False)}
async def main():
    OUT.mkdir(parents=True,exist_ok=False); cases=[]; renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        assert 15 not in {a.add_group for a in layer.appearance.add_balls}
        head=layer.appearance.key_balls.head; marker=67+len(layer.appearance.add_balls)
        paths={};hashes={};checks=[]
        for variant,(group,size,relative) in SETTINGS.items():
            s=dict(base)
            s['Add Ball']=(*base['Add Ball'],f'{head}, -36, -80, 0, 125, 244, -1, 0, -1, -1, {size}, 8, {group}, -1, {head if relative else -1}')
            s['Linez']=(*layer.sections.get('Linez',()),f'{head}, {marker}, 0, 125, 244, 244, 25, 25, 0, 1')
            path=OUT/f'{species}-{variant}{source.suffix}';paths[variant]=path.name;hashes[variant]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            static={v:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for v,a in assets.items() if v.startswith('static')}
            for variant in ('group_relative20','group_ordinary20'):
                a=assets[variant]
                for amount in (0,25,50,100):
                    updates=((15,amount),)
                    m=evaluate_morphs(a.appearance,len(a.frame.balls),updates)
                    g=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=updates)
                    relative=variant=='group_relative20'
                    assert m.offsets[-1]==tuple(_round(v*amount*.01) for v in (-36,-80,0))
                    assert m.sizes[-1]==(0 if relative else _round(20*amount*.01))
                    assert g[marker].parked==(amount==0)
                    if amount==0:assert g[marker].radius==0
                    elif relative:assert g[marker].radius==g[head].radius
                    if amount==100:
                        assert g==static['static_relative0' if relative else 'static_ordinary20']
                        if relative:assert g[marker].radius!=static['static_relative20'][marker].radius
                    checks.append({'pose':pose,'variant':variant,'amount':amount,'morph_offset':m.offsets[-1],'morph_size':m.sizes[-1],'head_radius':g[head].radius,'marker':asdict(g[marker]),'static_relative20_marker':asdict(static['static_relative20'][marker]),'static_relative0_marker':asdict(static['static_relative0'][marker])})
                ordered=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=((15,100),(15,0),(15,50)))
                direct=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=((15,50),))
                assert ordered==direct
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after,equal_expected in (('group_relative20','group_ordinary20',True),('static_relative0','static_relative20',False),('static_relative0','group_relative20',False)):
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal==equal_expected,(stem,equal)
                    renders.append({'species':c['species'],'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    print(stem,equal,flush=True)
    modules=('appearance/evaluation.py','rendering/morphs.py','rendering/attachment.py')
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent
    hashes={}
    for name in modules:
        content=(installed/name).read_bytes()
        assert content==(ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()
        hashes[name]=SHA(content)
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text())
    resolver=ResourceResolver((ROOT/'games/petz4',))
    for path,expected in provenance['shared_engine_hashes']['petz4'].items():
        assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    report={'experiment':'MORPH-002','backend':'local stdio MCP default state; direct Python explicit morph updates','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','settings':SETTINGS,'cases':cases,'comparisons':renders,'source_hashes':hashes,'shared_engine_hashes':provenance['shared_engine_hashes']['petz4'],'dependency_versions':{name:importlib.metadata.version(name) for name in ('fastmcp','numpy','Pillow','pydantic')}}
    for target in (OUT/'report.json',ROOT/'experiments/morph-002.json'):target.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
