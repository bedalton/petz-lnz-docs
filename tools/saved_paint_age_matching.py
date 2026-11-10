"""PAINT-008: selective adult/young paint-cache edits through saved assembly."""
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

OUT=ROOT/'scratch/research/paint-008';MANIFEST=ROOT/'experiments/paint-008.json'
SOURCE='Adopted Petz/Fuzzkin.pet';GAME=ROOT/'games/petz4'
AGES=(0,12,33,50,99,100);POSES=('standing','sitting','lying');YAWS=(0,64)
MODES=('baseline','young-color','adult-color','young-size','young-size-drop','young-reorder')


def rewrite(cache,mode):
    lines=cache.splitlines(keepends=True);active=False;targets=[]
    for i,line in enumerate(lines):
        if line.strip().startswith(b'['):active=line.strip()==b'[Paint Ballz]'
        if active and re.match(rb'^\s*50\s+',line):targets.append(i)
    assert len(targets)==3 and targets==list(range(targets[0],targets[0]+3))
    if mode=='young-reorder':
        a,b=targets[0],targets[2];lines[a],lines[b]=lines[b],lines[a]
    else:
        for j,i in enumerate(targets):
            line=lines[i]
            if mode=='young-size-drop' and j==2:
                lines[i]=re.sub(rb'[^\r\n]',b' ',line);continue
            tokens=list(re.finditer(rb'[^, \t\r\n\v\f]+',line))
            token=tokens[5 if mode.endswith('color') else 1]
            value=b'65' if mode.endswith('color') else b'12'
            assert len(token.group())==len(value)
            lines[i]=line[:token.start()]+value+line[token.end():]
    out=b''.join(lines);assert len(out)==len(cache) and out!=cache
    return out


def copies(verify):
    raw=(GAME/SOURCE).read_bytes();pet=read_saved_appearance(raw);records={}
    original={cache:load_saved_layer(pet,cache=cache).appearance for cache in ('adult','young')}
    for mode in MODES[1:]:
        label=mode.split('-')[0];cache=getattr(pet,label+'_cache')
        assert raw.count(cache)==1
        start=raw.index(cache);end=start+len(cache);modified=rewrite(cache,mode)
        edited=raw[:start]+modified+raw[end:];other=read_saved_appearance(edited)
        assert replace(other,**{label+'_cache':cache})==pet
        a=load_saved_layer(other,cache=label).appearance;base=original[label]
        assert replace(a,paint_balls=base.paint_balls)==base
        first=[p for p in base.paint_balls if p.base==50];second=[p for p in a.paint_balls if p.base==50]
        assert [p for p in a.paint_balls if p.base!=50]==[p for p in base.paint_balls if p.base!=50]
        if mode.endswith('color'):assert second==[replace(p,color=65) for p in first]
        elif mode=='young-reorder':assert second==first[::-1]
        else:assert second==[replace(p,diameter_percent=12) for p in (first[:-1] if mode.endswith('drop') else first)]
        path=OUT/f'Fuzzkin-{mode}.pet'
        if verify:assert path.read_bytes()==edited
        else:path.write_bytes(edited)
        records[mode]={'path':path.name,'file_sha256':SHA(edited),'cache':label,'offset':start,
            'length':len(cache),'original_cache_sha256':SHA(cache),'edited_cache_sha256':SHA(modified),
            'changed_bytes':sum(x!=y for x,y in zip(raw,edited)),'host50_rows':len(second)}
    return {'original_sha256':SHA(raw),'variants':records}


def expected(age,adult,young):
    weight=100 if age<12 else 100-(age-12)*100//88
    result=[]
    for host in set(p.base for p in adult):
        ai=[(i,p) for i,p in enumerate(adult) if p.base==host];yp=[p for p in young if p.base==host]
        if age==100 or len(ai)!=len(yp):result.extend(ai);continue
        for (i,a),b in zip(ai,yp):
            vector=tuple((1-weight/100)*x+(weight/100)*y for x,y in zip(a.direction,b.direction))
            norm=math.hypot(*vector)
            result.append((i,replace(a,diameter_percent=a.diameter_percent+math.trunc((b.diameter_percent-a.diameter_percent)*weight/100),
                fuzz=a.fuzz+math.trunc((b.fuzz-a.fuzz)*weight/100),direction=tuple(x/norm for x in vector))))
    return tuple(p for _,p in sorted(result))


def evaluate(age,pose,yaw,source,verify):
    resolver=ResourceResolver((GAME,OUT));first=None;first_rgba=None;outputs={}
    for mode in MODES:
        path=SOURCE if mode=='baseline' else source['variants'][mode]['path']
        raw=(GAME/path if mode=='baseline' else OUT/path).read_bytes();pet=read_saved_appearance(raw)
        adult,young=(load_saved_layer(pet,cache=layer).appearance.paint_balls for layer in ('adult','young'))
        asset=load_saved_assets(resolver,path,pose=pose,age=age)
        assert asset.preview.age==age and asset.preview.fatness_source=='saved' and asset.preview.seed_source=='saved'
        expected_rows=expected(age,adult,young);actual=asset.appearance.paint_balls
        assert len(expected_rows)==len(actual)==19
        for e,a in zip(expected_rows,actual):
            assert replace(e,direction=a.direction)==a
            assert all(math.isclose(x,y,rel_tol=1e-12,abs_tol=1e-12) for x,y in zip(e.direction,a.direction))
        result=render_portrait(asset,yaw=yaw)
        rgba=Image.open(BytesIO(result.png)).convert('RGBA').tobytes()
        if first is None:first=result;first_rgba=rgba
        assert result.prepared.geometry==first.prepared.geometry and len(rgba)==len(first_rgba)
        if mode in ('young-color','young-size-drop') or (age==100 and mode.startswith('young-')):
            assert result.prepared==first.prepared and result.png==first.png
        filename=f'{age}-{pose}-{yaw}-{mode}.png'
        if verify:assert (OUT/filename).read_bytes()==result.png
        else:(OUT/filename).write_bytes(result.png)
        paints=[p for p in actual if p.base==50]
        outputs[mode]={'png':filename,'png_sha256':SHA(result.png),'rgba_sha256':SHA(rgba),
            'indexed_sha256':SHA(result.indices),'dimensions':[result.width,result.height],
            'rgba_changed':sum(rgba[i:i+4]!=first_rgba[i:i+4] for i in range(0,len(rgba),4)),
            'prepared_changed':result.prepared!=first.prepared,'host50_sizes':[p.diameter_percent for p in paints],
            'host50_colors':[p.color for p in paints],'host50_directions':[list(p.direction) for p in paints]}
    return {'age':age,'pose':pose,'yaw':yaw,'outputs':outputs}


async def main():
    verify='--verify' in sys.argv
    prior=ROOT/'experiments/paint-007.json';old=json.loads(prior.read_text())
    if not verify:OUT.mkdir(parents=True,exist_ok=False)
    prov=provenance();source=copies(verify);cases=[];links=0
    for age in AGES:
        for pose in POSES:
            for yaw in YAWS:
                c=evaluate(age,pose,yaw,source,verify);cases.append(c)
                if age in (0,50,100):
                    reference=next(r for r in old['cases'] if (r['age'],r['pose'],r['yaw'])==(age,pose,yaw))
                    assert c['outputs']['baseline']['png_sha256']==reference['outputs']['baseline']['png_sha256'];links+=1
        print('age',age,'six fixtures verified',flush=True)
    if verify:
        report=json.loads(MANIFEST.read_text());assert report==json.loads((OUT/'report.json').read_text())
        assert report['source']==source and report['cases']==cases and report['provenance']==prov
        assert report['prior_manifest_sha256']==SHA(prior.read_bytes())
        for row in report['mcp']:assert SHA((OUT/row['png']).read_bytes())==row['png_sha256']
        print('PAINT-008 verified',report['summary']);return
    mcp=[];transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4',
        '--game-root',str(GAME),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            if c['age'] not in (0,50,100) or c['pose']!='standing':continue
            for mode,row in c['outputs'].items():
                args={'path':SOURCE if mode=='baseline' else source['variants'][mode]['path'],'pose':'standing',
                    'age':c['age'],'yaw_degrees':c['yaw']*360/256}
                stem=f"{c['age']}-{c['yaw']}-{mode}-mcp";png,meta=await save_result(client,'render_pet',args,OUT,stem)
                assert SHA(png)==row['png_sha256'] and meta['game_version']=='petz4'
                assert meta['appearance']['age_source']=='override' and meta['appearance']['age']==c['age']
                mcp.append({'controls':args,'png':stem+'.png','png_sha256':SHA(png),'metadata':stem+'-render.json'})
    assert SHA((GAME/SOURCE).read_bytes())==source['original_sha256']
    summary={'copies':5,'fixtures':len(cases),'direct_draws':len(cases)*len(MODES),'mcp_views':len(mcp),'prior_png_links':links,
        'rgba_changes_by_mode':{mode:sum(c['outputs'][mode]['rgba_changed']>0 for c in cases) for mode in MODES[1:]}}
    report={'experiment':'PAINT-008','backend':'private Petz4 saved-cache mutations; direct and local stdio MCP',
        'source':source,'provenance':prov,'prior_manifest_sha256':SHA(prior.read_bytes()),
        'controls':{'ages':AGES,'poses':POSES,'yaw_units':YAWS,'seed_fatness':'saved','raster_seed':1,'line_seed':1,'step':0},
        'cases':cases,'mcp':mcp,'summary':summary}
    for p in (MANIFEST,OUT/'report.json'):p.write_text(json.dumps(report,indent=2)+'\n')
    print(summary,flush=True)

if __name__=='__main__':asyncio.run(main())
