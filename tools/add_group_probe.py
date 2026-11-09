"""Default MCP add-group visibility plus explicit numerical morph updates."""
import asyncio,json,sys
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.morphs import evaluate_morphs
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/morph-001'
GROUP=15
async def main():
    OUT.mkdir(parents=True,exist_ok=False);cases=[];renders=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        assert GROUP not in {a.add_group for a in layer.appearance.add_balls}
        head=layer.appearance.key_balls.head;marker=67+len(layer.appearance.add_balls)
        line_row=f'{head}, {marker}, 0, 125, 244, 244, 25, 25, 0, 1'
        paths={};hashes={};rows={};checks=[]
        for v in ('original','active','dormant','omitted'):
            s=dict(base);s['Linez']=layer.sections.get('Linez',())
            if v!='original':
                group=GROUP if v=='dormant' else 0
                rows[v]=f'{head}, -36, -80, 0, 125, 244, -1, 0, -1, -1, 20, 0, {group}, -1, -1'
                s['Add Ball']=(*base['Add Ball'],rows[v]);s['Linez']=(*s['Linez'],line_row)
                if v=='omitted':s['Omissions']=(*base.get('Omissions',()),str(marker))
            path=OUT/f'{species}-{v}{source.suffix}';paths[v]=path.name;hashes[v]=write_copy(raw,leaf,s,path)
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            shapes={v:posed_geometry(a.appearance,a.sizes,a.frame,fatness=50) for v,a in assets.items()}
            assert shapes['dormant'][:marker]==shapes['original']
            assert shapes['dormant'][marker].parked and shapes['dormant'][marker].radius==0 and shapes['dormant'][marker].visible
            assert not shapes['omitted'][marker].visible and not shapes['omitted'][marker].parked
            assert len(assets['dormant'].appearance.lines)==len(assets['active'].appearance.lines)
            a=assets['dormant']
            for amount in (0,25,50,100):
                updates=((GROUP,amount),)
                m=evaluate_morphs(a.appearance,len(a.frame.balls),updates)
                g=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=updates)
                assert m.offsets[-1]==(-36*amount//100,-80*amount//100,0)
                assert m.sizes[-1]==20*amount//100
                assert g[:marker]==shapes['original']
                if amount==100: assert g==shapes['active']
                if amount==0: assert g==shapes['dormant']
                if amount>0: assert not g[marker].parked and g[marker].radius>0
                checks.append({'pose':pose,'amount':amount,'offset':m.offsets[-1],'diameter':m.sizes[-1],'marker':asdict(g[marker]),'group_amount':m.group_amounts[-1],'visible_prefix':m.visible_count,'group_mask':m.group_mask})
            again=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=((GROUP,100),(GROUP,0),(GROUP,50)))
            half=posed_geometry(a.appearance,a.sizes,a.frame,fatness=50,morph_updates=((GROUP,50),))
            assert again==half
        assert SHA(source.read_bytes())==SHA(raw)
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'marker_rows':rows,'line_row':line_row,'paths':paths,'input_hashes':hashes,'geometry':checks})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            for before,after in [('original','dormant'),('active','dormant'),('dormant','omitted')]:
                for yaw in (0,90):
                    args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                    stem=f"{c['species']}-{before}-{after}-{yaw}"
                    png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                    equal=meta['cells'][0]['pixel_sha256']==meta['cells'][1]['pixel_sha256']
                    assert equal==((before,after)!=('active','dormant'))
                    renders.append({'species':c['species'],'pair':[before,after],'controls':args,'png_sha256':SHA(png),'cells_equal':equal})
                    (OUT/'progress.json').write_text(json.dumps(renders,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'MORPH-001','backend':'local stdio MCP default state; direct Python explicit updates','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'runtime_provenance':'restore-002.json','group':GROUP,'cases':cases,'comparisons':renders}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/morph-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
