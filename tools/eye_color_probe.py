"""Separate iris-disc fill, outline and host-eye color effects."""
import asyncio,json,sys
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from petz_renderer.rendering.preparation import prepare_frame
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/eye-001'

async def main():
    OUT.mkdir(parents=True,exist_ok=True);cases=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        layer=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0)
        eyes=layer.appearance.eyes
        iris_ids=(eyes.right_iris,eyes.left_iris);eye_ids=(eyes.right_eye,eyes.left_eye)
        variants={'control':None,'pupil_fill':('Color Info Override',iris_ids),'iris_outline':('Outline Color Override',iris_ids),'right_outline':('Outline Color Override',iris_ids[:1]),'host_fill':('Color Info Override',eye_ids)}
        paths={};hashes={};edits={};checks=[];overlays={}
        for v,edit in variants.items():
            s=dict(base);edits[v]={}
            if edit:
                section,ids=edit;rows=tuple(f'{i}, 125' for i in ids)
                s[section]=(*s.get(section,()),*rows);edits[v]={'section':section,'rows':rows}
            path=OUT/f'{species}-{v}{source.suffix}'
            hashes[v]=write_copy(raw,leaf,s,path);paths[v]=path.name
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for pose in ('standing','sitting','lying'):
            assets={v:load_breed_assets(resolver,p,pose=pose,seed=0,age=100,fatness=50) for v,p in paths.items()}
            control=assets['control'];geometry=posed_geometry(control.appearance,control.sizes,control.frame,fatness=50)
            for v,a in assets.items():
                assert posed_geometry(a.appearance,a.sizes,a.frame,fatness=50)==geometry
                changed=[]
                for i,(before,after) in enumerate(zip(control.appearance.balls,a.appearance.balls)):
                    if before!=after:changed.append(i)
                if variants[v]: assert sorted(changed)==sorted(variants[v][1])
                else: assert not changed
                checks.append({'pose':pose,'variant':v,'geometry_equal':True,'changed_ball_info_ids':changed})
                if pose=='standing':
                    p=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=50)
                    overlays[v]={str(i):{'fill':p.balls[i].eye.iris.fill,'outline_color':p.balls[i].eye.iris.second,'outline_type':p.balls[i].eye.iris.outline_type,'host_fill':p.balls[i].circle.fill,'bounds':asdict(p.balls[i].eye.iris.bounds)} for i in eye_ids}
        cases.append({'species':species,'eyes':asdict(eyes),'source_sha256':SHA(raw),'input_hashes':hashes,'paths':paths,'edits':edits,'checks':checks,'standing_overlays':overlays})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    comparisons=[]
    async with Client(transport) as client:
        for c in cases:
            for v in variants:
                if v=='control':continue
                args={'before_path':c['paths']['control'],'after_path':c['paths'][v],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':0}
                stem=f"{c['species']}-{v}"
                png,meta=await save_result(client,'compare_appearance',args,OUT,stem)
                cell_hashes=[m['pixel_sha256'] for m in meta['cells']]
                assert cell_hashes[0]!=cell_hashes[1]
                comparisons.append({'species':c['species'],'variant':v,'controls':args,'png_sha256':SHA(png),'cell_hashes':cell_hashes})
                (OUT/'progress.json').write_text(json.dumps(comparisons,indent=2)+'\n');print(stem,flush=True)
    report={'experiment':'EYE-001','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'cases':cases,'comparisons':comparisons}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/eye-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
