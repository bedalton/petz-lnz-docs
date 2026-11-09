"""Synthetic added-ball attachment, head-shape and relative-size experiment."""
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
from petz_renderer.rendering.attachment import default_geometry
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/add-001'
def xyz(b):return (b.x,b.y,b.z)

def prepare():
    cases=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        a=layer.appearance;head=a.key_balls.head;marker=67+len(a.add_balls)
        assert len(base['Add Ball'])==len(a.add_balls)
        paths={};hashes={};rows={};fields={}
        for v in ('original','control','enlarged','moved','relative','relative_enlarged','omitted'):
            s=dict(base)
            if v!='original':
                relative=v.startswith('relative')
                values=[head,-35,-50,0,125,244,-1,0,-1,-1,-8 if relative else 20,0,0,-1,head if relative else -1]
                row=', '.join(str(x) for x in values);rows[v]=row
                s['Add Ball']=(*base['Add Ball'],row)
                if v in ('enlarged','relative_enlarged'):
                    first,second=a.shape.head_enlargement;s['Head Enlargement']=(str(first+25),str(second))
                if v=='moved':s['Move']=(*s.get('Move',()),f'{head}, 20, 0, 0')
                if v=='omitted':s['Omissions']=(*s.get('Omissions',()),str(marker))
            path=OUT/f'{species}-{v}{source.suffix}';hashes[v]=write_copy(raw,leaf,s,path);paths[v]=path.name
        resolver=ResourceResolver((ROOT/'games/petz4',OUT));checks=[]
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            shapes={v:posed_geometry(x.appearance,x.sizes,x.frame,fatness=50) for v,x in assets.items()}
            assert shapes['control'][:marker]==shapes['original']
            assert shapes['control'][marker]==shapes['enlarged'][marker]
            before,after=shapes['control'],shapes['moved']
            marker_delta=tuple(y-x for x,y in zip(xyz(before[marker]),xyz(after[marker])))
            head_delta=tuple(y-x for x,y in zip(xyz(before[head]),xyz(after[head])))
            prebody={v:default_geometry(assets[v].appearance,assets[v].sizes,assets[v].frame,fatness=50) for v in ('control','moved')}
            premarker=tuple(y-x for x,y in zip(xyz(prebody['control'][marker]),xyz(prebody['moved'][marker])))
            prehead=tuple(y-x for x,y in zip(xyz(prebody['control'][head]),xyz(prebody['moved'][head])))
            assert all(abs(a-b)<=1 for a,b in zip(premarker,prehead))
            r1,r2=shapes['relative'],shapes['relative_enlarged']
            assert r2[marker].radius-r1[marker].radius==r2[head].radius-r1[head].radius>0
            assert not shapes['omitted'][marker].visible
            assert shapes['omitted'][:marker]==shapes['control'][:marker]
            for v,shape in shapes.items():
                if v=='original':continue
                marker_ball=shape[marker]
                checks.append({'pose':pose,'variant':v,'marker':asdict(marker_ball),'head':asdict(shape[head]),'body_area':body_areas(assets[v].appearance)[marker],'movement_probe':{'posed_marker_delta':marker_delta,'posed_head_delta':head_delta,'prebody_marker_delta':premarker,'prebody_head_delta':prehead}})
                if pose=='standing':fields[v]=asdict(assets[v].appearance.add_balls[-1])
        cases.append({'species':species,'source_sha256':SHA(raw),'head_id':head,'marker_id':marker,'paths':paths,'input_hashes':hashes,'added_rows':rows,'marker_fields':fields,'geometry':checks})
    return cases

async def main():
    OUT.mkdir(parents=True,exist_ok=True);cases=prepare();comparisons=[]
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            pairs=[('original','control','standing',0),('control','enlarged','standing',0),('control','enlarged','standing',90),('control','moved','sitting',90),('relative','relative_enlarged','standing',0),('control','omitted','standing',0)]
            for before,after,pose,yaw in pairs:
                args={'before_path':c['paths'][before],'after_path':c['paths'][after],'pose':pose,'seed':0,'age':100,'fatness':50,'yaw_degrees':yaw}
                stem=f"{c['species']}-{before}-{after}-{pose}-yaw{yaw}"
                png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                comparisons.append({'species':c['species'],'before':before,'after':after,'controls':args,'png_sha256':SHA(png),'cell_hashes':[x['pixel_sha256'] for x in meta['cells']]})
                (OUT/'progress.json').write_text(json.dumps(comparisons,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'ADD-001','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'cases':cases,'comparisons':comparisons}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/add-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
