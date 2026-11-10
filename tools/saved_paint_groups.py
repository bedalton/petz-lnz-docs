"""PAINT-006: same-length cached paint group/color substitutions in copies."""
import asyncio
from dataclasses import asdict, replace
from io import BytesIO
import json
import re
import sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image
from petz_renderer.formats.pet import read_saved_appearance
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from saved_colour_arrays import provenance
from research_common import ROOT,SHA,save_result

OUT=ROOT/'scratch/research/paint-006';MANIFEST=ROOT/'experiments/paint-006.json'


def rewrite(cache,mode):
    active=False;result=[];edits=0
    for line in cache.splitlines(keepends=True):
        stripped=line.strip()
        if stripped.startswith(b'['):active=stripped==b'[Paint Ballz]'
        elif active and stripped:
            tokens=list(re.finditer(rb'[^, \t\r\n\v\f]+',line))
            if len(tokens)>=11:
                column=5 if mode=='color65' else 9
                token=tokens[column];old=token.group();value=b'65' if mode=='color65' else b'0' if mode=='group0' else b'1'
                assert len(value)<=len(old)
                line=line[:token.start()]+value.rjust(len(old))+line[token.end():];edits+=1
        result.append(line)
    assert edits>0
    output=b''.join(result);assert len(output)==len(cache)
    return output,edits


def copies(name,verify):
    source=ROOT/f'games/petz4/Adopted Petz/{name}.pet';raw=source.read_bytes();pet=read_saved_appearance(raw)
    spans=[]
    # Locate each exact authoritative cache; uniqueness prevents accidental replacement.
    for label,cache in (('adult',pet.adult_cache),('young',pet.young_cache)):
        assert raw.count(cache)==1
        spans.append((label,raw.index(cache),cache))
    variants=[]
    for mode in ('group0','group1','color65'):
        edited=bytearray(raw);rows={};allowed=set()
        for label,start,cache in spans:
            replacement,rows[label]=rewrite(cache,mode)
            edited[start:start+len(cache)]=replacement;allowed.update(range(start,start+len(cache)))
        edited=bytes(edited);assert len(edited)==len(raw)
        assert all(a==b for i,(a,b) in enumerate(zip(raw,edited)) if i not in allowed)
        other=read_saved_appearance(edited)
        assert replace(other,adult_cache=pet.adult_cache,young_cache=pet.young_cache)==pet
        path=OUT/f'{name}-{mode}.pet'
        if verify:assert path.read_bytes()==edited
        else:path.write_bytes(edited)
        variants.append({'mode':mode,'path':path.name,'sha256':SHA(edited),'rows':rows,
            'changed_bytes':sum(a!=b for a,b in zip(raw,edited))})
    return {'name':name,'path':str(source.relative_to(ROOT/'games/petz4')),'sha256':SHA(raw),
        'cache_spans':[{'cache':label,'offset':start,'length':len(cache),'sha256':SHA(cache)} for label,start,cache in spans],
        'variants':variants}


def evaluate(source,pose,yaw,verify):
    resolver=ResourceResolver((ROOT/'games/petz4',OUT))
    base=load_saved_assets(resolver,source['path'],pose=pose)
    first=render_portrait(base,yaw=yaw);outputs={};images=[]
    for mode in ('baseline','group0','group1','color65'):
        variant=next((v for v in source['variants'] if v['mode']==mode),None)
        asset=base if variant is None else load_saved_assets(resolver,variant['path'],pose=pose)
        if mode.startswith('group'):
            assert all(p.group==int(mode[-1]) for p in asset.appearance.paint_balls)
            assert replace(asset.appearance,paint_balls=tuple(replace(p,group=old.group) for p,old in zip(asset.appearance.paint_balls,base.appearance.paint_balls)))==base.appearance
            assert len(asset.appearance.paint_balls)==len(base.appearance.paint_balls)
            assert any(d.code=='unsupported_paint_fields' for d in asset.diagnostics)==(mode=='group1')
        result=render_portrait(asset,yaw=yaw)
        assert result.width==first.width and result.height==first.height
        assert result.prepared.geometry==first.prepared.geometry
        if mode.startswith('group'):
            assert result.prepared==first.prepared
            assert result.png==first.png
        if mode=='color65':
            assert all(p.color==65 for p in asset.appearance.paint_balls)
        path=OUT/f"{source['name']}-{pose}-{yaw}-{mode}.png"
        if verify:assert path.read_bytes()==result.png
        else:path.write_bytes(result.png)
        rgba=Image.open(BytesIO(result.png)).convert('RGBA');images.append(rgba)
        original=Image.open(BytesIO(first.png)).convert('RGBA')
        original_bytes=original.tobytes();rgba_bytes=rgba.tobytes()
        outputs[mode]={'png':path.name,'png_sha256':SHA(result.png),'indexed_sha256':SHA(result.indices),
            'rgba_sha256':SHA(rgba.tobytes()),'indexed_changed':sum(a!=b for a,b in zip(first.indices,result.indices)),
            'rgba_changed':sum(original_bytes[i:i+4]!=rgba_bytes[i:i+4] for i in range(0,len(rgba_bytes),4)),
            'prepared_commands_changed':result.prepared!=first.prepared,
            'paint_groups':sorted(set(p.group for p in asset.appearance.paint_balls)),
            'paint_count':len(asset.appearance.paint_balls)}
    stem=f"{source['name']}-{pose}-{yaw}-sheet.png";sheet=Image.new('RGBA',(first.width*4,first.height))
    for i,im in enumerate(images):sheet.paste(im,(i*first.width,0))
    b=BytesIO();sheet.save(b,format='PNG');data=b.getvalue()
    if verify:assert (OUT/stem).read_bytes()==data
    else:(OUT/stem).write_bytes(data)
    return {'name':source['name'],'pose':pose,'yaw':yaw,'outputs':outputs,'sheet':stem,'sheet_sha256':SHA(data),
        'cell_size':[first.width,first.height],'cell_order':['baseline','group0','group1','color65']}


async def main():
    verify='--verify' in sys.argv
    if verify:
        report=json.loads(MANIFEST.read_text());assert report==json.loads((OUT/'report.json').read_text())
        assert provenance()==report['provenance']
        sources=[copies(n,True) for n in ('Fuzzkin','Homebody','Goobe')]
        assert sources==report['sources']
        for c in report['cases']:
            source=next(s for s in sources if s['name']==c['name'])
            assert evaluate(source,c['pose'],c['yaw'],True)==c
        for row in report['mcp']:assert SHA((OUT/row['png']).read_bytes())==row['png_sha256']
        print('PAINT-006 verified',report['summary']);return
    OUT.mkdir(parents=True,exist_ok=False);prov=provenance();sources=[copies(n,False) for n in ('Fuzzkin','Homebody','Goobe')];cases=[]
    for source in sources:
        for pose in ('standing','sitting','lying'):
            for yaw in (0,64):cases.append(evaluate(source,pose,yaw,False))
        print(source['name'],'group/cache controls pass',flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4',
        '--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    mcp=[]
    async with Client(transport) as client:
        for source in sources:
            for yaw in (0,64):
                case=next(c for c in cases if c['name']==source['name'] and c['pose']=='standing' and c['yaw']==yaw)
                for variant in source['variants']:
                    args={'path':variant['path'],'pose':'standing','yaw_degrees':yaw*360/256}
                    stem=f"{source['name']}-{variant['mode']}-{yaw}-mcp"
                    png,meta=await save_result(client,'render_pet',args,OUT,stem)
                    assert SHA(png)==case['outputs'][variant['mode']]['png_sha256']
                    assert meta['game_version']=='petz4'
                    mcp.append({'controls':args,'png':stem+'.png','png_sha256':SHA(png),'metadata':stem+'-render.json'})
    summary={'copies':9,'fixtures':18,'direct_draws':72,'group_pixel_equivalences':36,'mcp_views':18,
        'color_positive_pixel_changes':sum(c['outputs']['color65']['rgba_changed']>0 for c in cases)}
    report={'experiment':'PAINT-006','backend':'copy-only cached Paint Ballz substitutions; direct API and local stdio MCP',
        'provenance':prov,'controls':{'age_seed_fatness':'saved','raster_seed':1,'line_seed':1,'step':0,
            'cache_edits':'both adult/young; original byte lengths; only group or color token'},
        'sources':sources,'cases':cases,'mcp':mcp,'summary':summary}
    for p in (MANIFEST,OUT/'report.json'):p.write_text(json.dumps(report,indent=2)+'\n')
    print(summary,flush=True)

if __name__=='__main__':asyncio.run(main())
