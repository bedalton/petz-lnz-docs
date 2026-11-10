"""PAINT-007: age interpolation controls using PAINT-006 Fuzzkin copies."""
import asyncio
import json
import sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image
from io import BytesIO
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from saved_colour_arrays import provenance
from research_common import ROOT,SHA,save_result

OUT=ROOT/'scratch/research/paint-007';MANIFEST=ROOT/'experiments/paint-007.json'


def evaluate(age,pose,yaw,source,verify):
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/paint-006'))
    outputs={};first=None
    for mode in ('baseline','group0','group1','color65'):
        path=source['path'] if mode=='baseline' else next(v['path'] for v in source['variants'] if v['mode']==mode)
        asset=load_saved_assets(resolver,path,pose=pose,age=age)
        assert asset.preview.age==age and asset.preview.age_source=='override'
        if mode.startswith('group'):assert all(p.group==int(mode[-1]) for p in asset.appearance.paint_balls)
        portrait=render_portrait(asset,yaw=yaw)
        if first is None:first=portrait
        assert portrait.prepared.geometry==first.prepared.geometry
        if mode.startswith('group'):assert portrait.prepared==first.prepared and portrait.png==first.png
        rgba=Image.open(BytesIO(portrait.png)).convert('RGBA').tobytes()
        original=Image.open(BytesIO(first.png)).convert('RGBA').tobytes()
        assert len(rgba)==len(original)
        png=f'{age}-{pose}-{yaw}-{mode}.png'
        if verify:assert (OUT/png).read_bytes()==portrait.png
        else:(OUT/png).write_bytes(portrait.png)
        outputs[mode]={'png':png,'png_sha256':SHA(portrait.png),'rgba_sha256':SHA(rgba),
            'indexed_sha256':SHA(portrait.indices),'rgba_changed':sum(rgba[i:i+4]!=original[i:i+4] for i in range(0,len(rgba),4)),
            'eligible_paint_commands':sum(len(b.paints) for b in portrait.prepared.balls),
            'textured_paint_commands':sum(p.paint is not None for b in portrait.prepared.balls for p in b.paints),
            'layer_count':len(asset.preview.layers),'paint_count':len(asset.appearance.paint_balls)}
    return {'age':age,'pose':pose,'yaw':yaw,'outputs':outputs}


async def main():
    verify='--verify' in sys.argv
    prior=ROOT/'experiments/paint-006.json';old=json.loads(prior.read_text());source=next(s for s in old['sources'] if s['name']=='Fuzzkin')
    assert SHA((ROOT/'games/petz4'/source['path']).read_bytes())==source['sha256']
    for v in source['variants']:assert SHA((ROOT/'scratch/research/paint-006'/v['path']).read_bytes())==v['sha256']
    if verify:
        report=json.loads(MANIFEST.read_text());assert report==json.loads((OUT/'report.json').read_text())
        assert SHA(prior.read_bytes())==report['prior_manifest_sha256'] and provenance()==report['provenance']
        for c in report['cases']:assert evaluate(c['age'],c['pose'],c['yaw'],source,True)==c
        for c in report['mcp']:assert SHA((OUT/c['png']).read_bytes())==c['png_sha256']
        print('PAINT-007 verified',report['summary']);return
    OUT.mkdir(parents=True,exist_ok=False);prov=provenance();cases=[]
    for age in (0,50,100):
        for pose in ('standing','sitting','lying'):
            for yaw in (0,64):cases.append(evaluate(age,pose,yaw,source,False))
        print('age',age,'six fixtures pass',flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4',
        '--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/paint-006')])
    mcp=[]
    async with Client(transport) as client:
        for c in cases:
            if c['pose']!='standing' or c['age']==50:continue
            for mode,row in c['outputs'].items():
                path=source['path'] if mode=='baseline' else next(v['path'] for v in source['variants'] if v['mode']==mode)
                args={'path':path,'pose':'standing','age':c['age'],'yaw_degrees':c['yaw']*360/256}
                stem=f"{c['age']}-{c['yaw']}-{mode}-mcp"
                png,meta=await save_result(client,'render_pet',args,OUT,stem)
                assert SHA(png)==row['png_sha256'] and meta['game_version']=='petz4'
                assert meta['appearance']['age_source']=='override'
                mcp.append({'controls':args,'png':stem+'.png','png_sha256':SHA(png),'metadata':stem+'-render.json'})
    summary={'age_fixtures':18,'direct_draws':72,'group_equivalences':36,'mcp_views':16,
        'color_positive_changes':sum(c['outputs']['color65']['rgba_changed']>0 for c in cases)}
    report={'experiment':'PAINT-007','backend':'direct age override + local stdio MCP; existing private PAINT-006 copies',
        'prior_manifest_sha256':SHA(prior.read_bytes()),'provenance':prov,
        'controls':{'ages':[0,50,100],'seed_and_fatness':'saved','yaw_units':[0,64],'raster_seed':1,'line_seed':1,'step':0},
        'cases':cases,'mcp':mcp,'summary':summary}
    for p in (MANIFEST,OUT/'report.json'):p.write_text(json.dumps(report,indent=2)+'\n')
    print(summary,flush=True)

if __name__=='__main__':asyncio.run(main())
