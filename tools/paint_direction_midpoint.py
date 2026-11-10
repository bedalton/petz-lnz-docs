"""PAINT-010: exact opposing paint directions at the age-weight midpoint."""
import asyncio
from dataclasses import replace
from io import BytesIO
import json
import math
import re
import sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image
from petz_renderer.appearance.layers import load_saved_layer
from petz_renderer.formats.pet import read_saved_appearance
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from research_common import ROOT,SHA,save_result
from saved_colour_arrays import provenance
from saved_paint_age_matching import GAME,SOURCE

OUT=ROOT/'scratch/research/paint-010';MANIFEST=ROOT/'experiments/paint-010.json'
MODES=('matched-surface','opposed-surface','matched-nonsurface','opposed-nonsurface')


def rewrite(cache,z,surface):
    lines=cache.splitlines(keepends=True);active=False;targets=[]
    for i,line in enumerate(lines):
        if line.strip().startswith(b'['):active=line.strip()==b'[Paint Ballz]'
        if active and re.match(rb'^\s*50\s+',line):targets.append(i)
    assert len(targets)==3
    for index,i in enumerate(targets):
        line=lines[i];body=line.rstrip(b'\r\n');suffix=line[len(body):]
        replacement=(f'50 32 0 0 {z} 15 -1 3 -1 2 0 {int(surface)}'.encode() if index==0 else b'')
        assert len(replacement)<=len(body)
        lines[i]=replacement.ljust(len(body))+suffix
    output=b''.join(lines);assert len(output)==len(cache)
    return output


def copies(verify):
    raw=(GAME/SOURCE).read_bytes();pet=read_saved_appearance(raw);variants={}
    for mode in MODES:
        surface=mode.endswith('-surface');edited=raw;spans=[]
        for cache in ('adult','young'):
            source=getattr(pet,cache+'_cache');assert raw.count(source)==1
            start=raw.index(source);z=1 if cache=='young' and mode.startswith('opposed') else -1
            patch=rewrite(source,z,surface);edited=edited[:start]+patch+edited[start+len(source):]
            spans.append({'cache':cache,'start':start,'length':len(source),'original_sha256':SHA(source),'edited_sha256':SHA(patch)})
        other=read_saved_appearance(edited)
        assert replace(other,adult_cache=pet.adult_cache,young_cache=pet.young_cache)==pet
        for cache in ('adult','young'):
            baseline=load_saved_layer(pet,cache=cache).appearance;actual=load_saved_layer(other,cache=cache).appearance
            assert replace(actual,paint_balls=baseline.paint_balls)==baseline
            assert actual.paint_balls[:16]==baseline.paint_balls[:16] and len(actual.paint_balls)==17
            z=1 if cache=='young' and mode.startswith('opposed') else -1
            assert actual.paint_balls[16]==replace(baseline.paint_balls[16],direction=(0.,0.,float(z)),surface=surface)
        path=OUT/f'Fuzzkin-{mode}.pet'
        if verify:assert path.read_bytes()==edited
        else:path.write_bytes(edited)
        variants[mode]={'path':path.name,'sha256':SHA(edited),'cache_spans':spans}
    return {'original_sha256':SHA(raw),'variants':variants}


def evaluate(age,yaw,source,verify):
    resolver=ResourceResolver((GAME,OUT));outputs={};images={};geometry=None
    for mode in MODES:
        asset=load_saved_assets(resolver,source['variants'][mode]['path'],pose='standing',age=age)
        paint=asset.appearance.paint_balls[16];surface=mode.endswith('-surface');opposed=mode.startswith('opposed')
        midpoint=age==56 and opposed
        expected='zero-vector sentinel' if midpoint else [0.,0.,1. if age==55 and opposed else -1.]
        if midpoint:assert all(math.isnan(x) for x in paint.direction)
        else:assert list(paint.direction)==expected
        portrait=render_portrait(asset,yaw=yaw);host=portrait.prepared.balls[50]
        if geometry is None:geometry=portrait.prepared.geometry
        assert portrait.prepared.geometry==geometry
        if midpoint:
            if surface:assert not host.paints
            else:
                block,=host.paints;assert block.paint_index==16
                h=host.circle.bounds;size=32*(h.width-1)//100
                x=math.trunc((h.left+h.right)/2)-(size+1)//2
                y=math.trunc((h.top+h.bottom)/2)-(size+1)//2
                assert (block.bounds.left,block.bounds.top,block.bounds.right,block.bounds.bottom)==(x,y,x+size+1,y+size+1)
        image=Image.open(BytesIO(portrait.png)).convert('RGBA');rgba=image.tobytes();images[mode]=rgba
        filename=f'{age}-{yaw}-{mode}.png'
        if verify:assert (OUT/filename).read_bytes()==portrait.png
        else:(OUT/filename).write_bytes(portrait.png)
        outputs[mode]={'png':filename,'png_sha256':SHA(portrait.png),'rgba_sha256':SHA(rgba),
            'indexed_sha256':SHA(portrait.indices),'direction':expected,'prepared_host50_paints':len(host.paints)}
    if age>=57:
        for surface in ('surface','nonsurface'):assert images['matched-'+surface]==images['opposed-'+surface]
    changed={}
    for surface in ('surface','nonsurface'):
        a=images['matched-'+surface];b=images['opposed-'+surface];assert len(a)==len(b)
        changed[surface]=sum(a[i:i+4]!=b[i:i+4] for i in range(0,len(a),4))
    return {'age':age,'yaw':yaw,'outputs':outputs,'opposed_changed_rgba':changed}


async def main():
    verify='--verify' in sys.argv
    if not verify:OUT.mkdir(parents=True,exist_ok=False)
    prov=provenance();source=copies(verify)
    cases=[evaluate(age,yaw,source,verify) for age in (55,56,57,100) for yaw in (0,64)]
    if verify:
        report=json.loads(MANIFEST.read_text());assert report==json.loads((OUT/'report.json').read_text())
        assert report['source']==source and report['cases']==cases and report['provenance']==prov
        for row in report['mcp']:assert SHA((OUT/row['png']).read_bytes())==row['png_sha256']
        print('PAINT-010 verified',report['summary'],flush=True);return
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4',
        '--game-root',str(GAME),'--asset-root',str(OUT)])
    mcp=[]
    async with Client(transport) as client:
        for c in cases:
            if c['age']!=56:continue
            for mode,row in c['outputs'].items():
                args={'path':source['variants'][mode]['path'],'pose':'standing','age':56,'yaw_degrees':c['yaw']*360/256}
                stem=f"56-{c['yaw']}-{mode}-mcp";png,meta=await save_result(client,'render_pet',args,OUT,stem)
                assert SHA(png)==row['png_sha256'] and meta['game_version']=='petz4'
                mcp.append({'controls':args,'png':stem+'.png','png_sha256':SHA(png),'metadata':stem+'-render.json'})
    assert SHA((GAME/SOURCE).read_bytes())==source['original_sha256']
    report={'experiment':'PAINT-010','backend':'direct private saved-cache controls and local stdio MCP','source':source,
        'provenance':prov,'controls':{'ages':[55,56,57,100],'yaw_units':[0,64],'pose':'standing','saved_seed_fatness':True,
            'raster_seed':1,'line_seed':1,'step':0},'cases':cases,'mcp':mcp,
        'summary':{'copies':4,'fixtures':8,'direct_draws':32,'mcp_views':8,'midpoint_surface_rejections':2,'midpoint_nonsurface_center_commands':2}}
    for p in (MANIFEST,OUT/'report.json'):p.write_text(json.dumps(report,indent=2)+'\n')
    print(report['summary'],flush=True)

if __name__=='__main__':asyncio.run(main())
