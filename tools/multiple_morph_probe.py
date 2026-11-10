"""MORPH-003: independent group percentages, shared members and prefix state."""
import asyncio,json,sys,importlib.metadata
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
OUT=ROOT/'scratch/research/morph-003'
OFFSETS=((-36,-80,0),(-8,-110,0),(30,-80,0))
SETTINGS={'dormant_body':((14,15,14),1),'dormant_head':((14,15,14),8),'static_all':((0,0,0),8),'active_a':((0,15,0),8),'active_b':((14,0,14),8)}
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        assert not ({14,15}&{a.add_group for a in layer.appearance.add_balls})
        head=layer.appearance.key_balls.head;first=67+len(layer.appearance.add_balls)
        paths={};hashes={};checks=[]
        for variant,(groups,area) in SETTINGS.items():
            s=dict(base)
            rows=[f'{head}, {x}, {y}, {z}, 125, 244, -1, 0, -1, -1, 20, {area}, {group}, -1, -1' for (x,y,z),group in zip(OFFSETS,groups)]
            s['Add Ball']=(*base['Add Ball'],*rows)
            s['Linez']=layer.sections.get('Linez',()) # no new lines: preserve area1/8 fixture
            path=OUT/f'{species}-{variant}{source.suffix}';paths[variant]=path.name;hashes[variant]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            static=posed_geometry(assets['static_all'].appearance,assets['static_all'].sizes,assets['static_all'].frame,fatness=50)
            for variant in ('dormant_body','dormant_head'):
                a=assets[variant]
                for pa in (0,50,100):
                    for pb in (0,50,100):
                        updates=((14,pa),(15,pb));reverse=tuple(reversed(updates))
                        m=evaluate_morphs(a.appearance,len(a.frame.balls),updates)
                        rev=evaluate_morphs(a.appearance,len(a.frame.balls),reverse)
                        assert m==rev # transition traces deliberately excluded from dataclass equality
                        g=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=updates)
                        rg=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=reverse)
                        assert g==rg
                        assert m.group_amounts[-3:]==(pa,pb,pa)
                        assert bool(m.group_mask&(1<<14))==(pa>0)
                        assert bool(m.group_mask&(1<<15))==(pb>0)
                        for i,amount in enumerate((pa,pb,pa)):
                            assert m.offsets[-3+i]==tuple(_round(v*amount*.01) for v in OFFSETS[i])
                            assert m.sizes[-3+i]==_round(20*amount*.01)
                            assert g[first+i].parked==(amount==0)
                        if variant=='dormant_head':assert m.visible_count==len(a.appearance.add_balls)
                        else:
                            expected=len(a.appearance.add_balls) if pa else len(a.appearance.add_balls)-1 if pb else len(layer.appearance.add_balls)
                            assert m.visible_count==expected,(species,pose,pa,pb,m.visible_count,expected)
                        if pa==pb==100:assert g==static
                        checks.append({'pose':pose,'variant':variant,'amounts':[pa,pb],'visible_prefix':m.visible_count,'mask':m.group_mask,'forward_transitions':m.transitions,'reverse_transitions':rev.transitions,'marker_offsets':m.offsets[-3:],'marker_sizes':m.sizes[-3:],'markers':[asdict(b) for b in g[first:]]})
                direct=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=((14,50),(15,100)))
                ordered=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=((14,100),(15,50),(14,0),(14,50),(15,100)))
                assert ordered==direct
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'first_marker_id':first,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after,expected in (('dormant_body','dormant_head',True),('active_a','static_all',False),('active_b','dormant_head',False)):
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256'];assert equal==expected,(stem,equal)
                    renders.append({'species':c['species'],'controls':args,'png_sha256':SHA(png),'cells_equal':equal});print(stem,equal,flush=True)
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent;source_hashes={}
    for name in ('appearance/evaluation.py','rendering/morphs.py','rendering/attachment.py'):
        content=(installed/name).read_bytes();assert content==(ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes();source_hashes[name]=SHA(content)
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text());resolver=ResourceResolver((ROOT/'games/petz4',))
    for path,expected in provenance['shared_engine_hashes']['petz4'].items():assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    report={'experiment':'MORPH-003','backend':'local stdio MCP default state; direct Python explicit morph updates','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','settings':SETTINGS,'offsets':OFFSETS,'cases':cases,'comparisons':renders,'source_hashes':source_hashes,'shared_engine_hashes':provenance['shared_engine_hashes']['petz4'],'dependency_versions':{name:importlib.metadata.version(name) for name in ('fastmcp','numpy','Pillow','pydantic')}}
    for target in (OUT/'report.json',ROOT/'experiments/morph-003.json'):target.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
