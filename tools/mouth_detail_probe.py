"""MOUTH-002: edit existing Labrador mouth rows; retain every dependency.

Controls are diagnostic surfaces and a zero-relative-offset tongue, not a
production breed writer or native-motion validation.
"""
import argparse
import asyncio
import base64
import dataclasses
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path
import petz_renderer
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image,ImageDraw
from petz_renderer.appearance.lnz import parse_sections
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.attachment import default_geometry
from face_extension_probe import compact,sha
from native_anatomy_probe import section_edit,tok

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'clean_dogs/petz4/Labrador.dog'
VARIANTS=('source','roundtrip','cheek_x','lip_jowl_x','lower_y','tongue_relative0')
STATES=(('standing',None,None),('sitting',None,None),('lying',None,None),('raw27',27,5),('raw19',19,31))
EDITS={'cheek_x':{78:('x',6),79:('x',-6)},
       'lip_jowl_x':{80:('x',4),81:('x',-4),91:('x',4),92:('x',-4)},
       'lower_y':{88:('y',6),89:('y',6),90:('y',6),91:('y',6),92:('y',6)},
       'tongue_relative0':{77:('size',1)}}


def write_variant(raw,v,target):
    pe=ResourceFile(raw);edited=bytearray(raw);spans=[]
    for name in ('LR','LRPUP'):
        leaf=next(r for r in pe.resources if r.type=='LNZ' and r.name==name)
        text=compact(pe.read('LNZ',name))
        if v in EDITS and '[Add Ball]' in text:
            def edit(body):
                rows=body.strip().splitlines();assert len(rows)==28
                for i,(field,delta) in EDITS[v].items():
                    values=tok(rows[i-67]);column={'x':1,'y':2,'size':10}[field]
                    if v=='tongue_relative0':assert int(values[column])==-1 and int(values[14])==63
                    values[column]=str(int(values[column])+delta);rows[i-67]=','.join(values)
                return '\n'.join(rows)
            text=section_edit(text,'Add Ball',edit)
        payload=text.encode('cp1252');assert len(payload)<=leaf.size
        edited[leaf.offset:leaf.offset+leaf.size]=payload.ljust(leaf.size,b' ')
        spans.append((leaf.offset,leaf.offset+leaf.size))
    result=bytes(edited);after=ResourceFile(result);assert pe.resources==after.resources
    cursor=0
    for start,end in sorted(spans):assert raw[cursor:start]==result[cursor:start];cursor=end
    assert raw[cursor:]==result[cursor:]
    for r in pe.resources:
        if r.type!='LNZ' or r.name not in ('LR','LRPUP'):assert pe.read(r.type,r.name,r.language)==after.read(r.type,r.name,r.language)
    target.write_bytes(result);return after


def sheets(out,records):
    result=[]
    for look in ('adult','puppy'):
        for state,_,_ in STATES:
            entries=[r for r in records if r['look']==look and r['state']==state]
            left=max(r['meta']['offset'][0] for r in entries);top=max(r['meta']['offset'][1] for r in entries)
            right=max(r['meta']['width']-r['meta']['offset'][0] for r in entries)
            bottom=max(r['meta']['height']-r['meta']['offset'][1] for r in entries)
            w,h=left+right+12,top+bottom+24
            canvas=Image.new('RGB',(w*6*2,h*2*2),'#acb1b5');draw=ImageDraw.Draw(canvas)
            for i,r in enumerate(entries):
                im=Image.open(out/r['file']).convert('RGBA');tile=Image.new('RGBA',(w,h))
                tile.alpha_composite(im,(left-r['meta']['offset'][0]+6,top-r['meta']['offset'][1]+20))
                tile=tile.resize((w*2,h*2),Image.Resampling.NEAREST)
                x,y=(i%6)*w*2,(i//6)*h*2;canvas.paste(tile,(x,y),tile)
                draw.text((x+4,y+4),r['variant'],fill='black')
            name=f'sheet-{look}-{state}.png';canvas.save(out/name);result.append({'file':name,'sha256':sha((out/name).read_bytes())})
    return result


async def run(out):
    out.mkdir(parents=True,exist_ok=False);raw=SOURCE.read_bytes();pe=ResourceFile(raw);parse_checks=0
    copy_hashes={}
    for v in VARIANTS:
        target=out/f'{v}.dog'
        if v=='source':target.write_bytes(raw)
        else:
            after=write_variant(raw,v,target)
            if v=='roundtrip':
                for name in ('LR','LRPUP'):
                    for seed in range(256):
                        assert dict(parse_sections(pe.read('LNZ',name),seed))==dict(parse_sections(after.read('LNZ',name),seed));parse_checks+=1
        copy_hashes[str(target.relative_to(ROOT))]=sha(target.read_bytes())
    package=Path(petz_renderer.__file__).parent
    source_hashes={str(p.relative_to(package)):sha(p.read_bytes()) for p in package.rglob('*.py')}
    checkout=ROOT/'petz-renderer-mcp/src/petz_renderer'
    assert source_hashes=={str(p.relative_to(checkout)):sha(p.read_bytes()) for p in checkout.rglob('*.py')}
    inputs=[SOURCE,ROOT/'games/petz4/Petz 4.exe',*[ROOT/'games/petz4/Resource'/n for n in ('Dogz 4 Rez.dll','Catz 4 Rez.dll','Petz 4 Rez.dll')]]
    report={'experiment':'MOUTH-002','backend':'local stdio MCP','revision':subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip(),
      'packages':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','Pillow','fastmcp')},'sources':source_hashes,
      'input_hashes':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in inputs},'copy_hashes':copy_hashes,
      'script_sha256':sha(Path(__file__).read_bytes()),'parse_checks':parse_checks,'geometry':[],'renders':[]}
    resolver=ResourceResolver((ROOT/'games/petz4',out))
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(out)])
    async with Client(transport) as client:
        for look in ('adult','puppy'):
            for state,animation,frame in STATES:
                load=dict(pose=state) if animation is None else dict(animation=animation,frame=frame)
                assets={v:load_breed_assets(resolver,f'{v}.dog',look=look,seed=41,age=100 if look=='adult' else 12,fatness=50,**load) for v in VARIANTS}
                base=assets['source'];before=default_geometry(base.appearance,base.sizes,base.frame,fatness=50)
                for v,a in assets.items():
                    assert dataclasses.replace(a.appearance,add_balls=base.appearance.add_balls)==base.appearance
                    assert a.frame==base.frame and a.sizes==base.sizes
                    for i,(old,new) in enumerate(zip(base.appearance.add_balls,a.appearance.add_balls)):
                        if i+67 in EDITS.get(v,{}):
                            field,delta=EDITS[v][i+67];assert dataclasses.replace(new,**{field:getattr(old,field)})==old
                            assert getattr(new,field)==getattr(old,field)+delta
                        else:assert old==new
                    after=default_geometry(a.appearance,a.sizes,a.frame,fatness=50)
                    changed=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y]
                    assert set(changed)<=set(EDITS.get(v,{}))
                    assert all((x.visible,x.parked)==(y.visible,y.parked) for x,y in zip(before,after))
                    if v!='tongue_relative0':assert all(x.radius==y.radius for x,y in zip(before,after))
                    if v=='tongue_relative0':
                        assert after[77].radius==after[63].radius
                        if animation is None:assert before[77].radius==after[77].radius==0
                    report['geometry'].append({'look':look,'state':state,'variant':v,'changed_geometry_ids':changed,
                      'before':[dataclasses.asdict(b) for b in before],'after':[dataclasses.asdict(b) for b in after]})
                for yaw in (0,90):
                    baseline=None
                    for v in VARIANTS:
                        args=dict(path=f'{v}.dog',look=look,seed=41,age=100 if look=='adult' else 12,fatness=50,yaw_degrees=yaw,**(load if animation is None else dict(pose='default',**load)))
                        response=await client.call_tool('render_pet',args);assert not response.is_error,response.data
                        png=base64.b64decode(next(c.data for c in response.content if c.type=='image'));digest=sha(png)
                        if v=='source':baseline=digest
                        if v=='roundtrip':assert digest==baseline
                        name=f'{look}-{state}-{yaw}-{v}.png';(out/name).write_bytes(png)
                        report['renders'].append({'look':look,'state':state,'variant':v,'args':args,'file':name,'sha256':digest,'meta':response.data,'differs_from_source':digest!=baseline})
                (out/'progress.json').write_text(json.dumps(report['renders'],indent=2)+'\n')
                print(look,state,'12 MCP renders complete',flush=True)
    report['sheets']=sheets(out,report['renders'])
    assert report['input_hashes']=={p:sha((ROOT/p).read_bytes()) for p in report['input_hashes']}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS 120 MCP renders; 60 geometry records; 512 parse controls',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'scratch/research/mouth-002')
    asyncio.run(run(p.parse_args().out.resolve()))
