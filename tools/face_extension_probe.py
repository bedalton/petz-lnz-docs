"""FACE-001: copy-only existing muzzle controls, private resources/evidence.

Fixed-span writer retains variation syntax; no general-purpose breed export.
"""
import argparse
import asyncio
import base64
import dataclasses
import importlib.metadata
import json
import math
import subprocess
import sys
from pathlib import Path

import petz_renderer
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image, ImageDraw
from petz_renderer.appearance.lnz import parse_sections
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.attachment import default_geometry
from petz_renderer.rendering.positions import modify_positions
from native_anatomy_probe import section_edit, sha

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    'labrador': ('clean_dogs/petz4/Labrador.dog', ('LR', 'LRPUP'), '.dog'),
    'siamese': ('games/petz4/Resource/Catz/Siamese.cat', ('SI', 'SIKIT'), '.cat'),
}
VARIANTS = ('source', 'roundtrip', 'face0', 'face-12', 'face12')
# Deliberately explicit independent expected ID lists, including repeated utility ID.
MUZZLES = {2: (55,56,51,39,15,63,64,17,41,65,65),
           1: (37,40,7,31,30,55,56,4,5,57,58,59,60,61,62,65,65)}


def compact(raw):
    return '\n'.join(s for line in raw.decode('cp1252').splitlines()
                     if (s := line.split(';', 1)[0].strip()))+'\n'


def write_variant(raw, names, variant, target):
    before = ResourceFile(raw)
    edited = bytearray(raw)
    spans = []
    for name in names:
        leaf = next(r for r in before.resources if r.type == 'LNZ' and r.name == name)
        text = compact(before.read('LNZ', name))
        if variant.startswith('face'):
            text = section_edit(text, 'Face Extension', lambda _: variant[4:]+'\n')
        payload = text.encode('cp1252')
        assert len(payload) <= leaf.size
        edited[leaf.offset:leaf.offset+leaf.size] = payload.ljust(leaf.size,b' ')
        spans.append((leaf.offset,leaf.offset+leaf.size))
    result = bytes(edited)
    after = ResourceFile(result)
    assert before.resources == after.resources
    for r in before.resources:
        if r.type != 'LNZ' or r.name not in names:
            assert before.read(r.type,r.name,r.language) == after.read(r.type,r.name,r.language)
    cursor = 0
    for start,end in sorted(spans):
        assert raw[cursor:start] == result[cursor:start]
        cursor = end
    assert raw[cursor:] == result[cursor:]
    target.write_bytes(result)
    return after


def trunc(n,d):
    return (abs(n)//d) * (-1 if n<0 else 1)


def narrow(n):
    return (n+32768)%65536-32768


def isolated_oracle(appearance, frame):
    """Independent integer arithmetic; unrelated shape/move/project paths disabled."""
    clean = dataclasses.replace(appearance, shape=dataclasses.replace(appearance.shape,
        body_extension=0, leg_extension=(0,0), head_enlargement=(100,0),
        ear_extension=100, feet_enlargement=(100,0)), moves=(), projections=())
    positions = [(b.x,b.y,b.z) for b in frame.balls]
    jaw,nose = (53,55) if appearance.species==2 else (29,37)
    direction = tuple(a-b for a,b in zip(positions[jaw],positions[nose]))
    length = math.isqrt(sum(v*v for v in direction))
    delta = tuple(trunc(-v*appearance.shape.face_extension,length) for v in direction) if length else direction
    expected = list(positions)
    if appearance.shape.face_extension:
        for i in MUZZLES[appearance.species]:
            expected[i] = tuple(narrow(p+d) for p,d in zip(expected[i],delta))
    actual = modify_positions(clean,frame)
    assert expected == [(b.x,b.y,b.z) for b in actual.balls]
    assert all((a.rot_byte6,a.rot_byte7,a.rot_byte8)==(b.rot_byte6,b.rot_byte7,b.rot_byte8)
               for a,b in zip(actual.balls,frame.balls))
    return {'direction':direction,'length':length,'delta':delta,
            'changed_ids':[i for i,(a,b) in enumerate(zip(positions,expected)) if a!=b]}


def sheets(out, records):
    result=[]
    for breed in CASES:
        for look in ('adult','young'):
            for pose in ('standing','sitting','lying'):
                entries=[r for r in records if (r['breed'],r['look'],r['args']['pose'])==(breed,look,pose)]
                left=max(r['meta']['offset'][0] for r in entries)
                top=max(r['meta']['offset'][1] for r in entries)
                right=max(r['meta']['width']-r['meta']['offset'][0] for r in entries)
                bottom=max(r['meta']['height']-r['meta']['offset'][1] for r in entries)
                w,h=left+right+12,top+bottom+24
                canvas=Image.new('RGB',(w*len(VARIANTS)*2,h*4*2),'#adb1b5')
                draw=ImageDraw.Draw(canvas)
                for i,r in enumerate(entries):
                    im=Image.open(out/r['file']).convert('RGBA')
                    tile=Image.new('RGBA',(w,h))
                    tile.alpha_composite(im,(left-r['meta']['offset'][0]+6,top-r['meta']['offset'][1]+20))
                    tile=tile.resize((w*2,h*2),Image.Resampling.NEAREST)
                    x,y=(i%len(VARIANTS))*w*2,(i//len(VARIANTS))*h*2
                    canvas.paste(tile,(x,y),tile)
                    draw.text((x+5,y+4),f"{r['variant']} yaw {r['args']['yaw_degrees']}",fill='black')
                name=f'sheet-{breed}-{look}-{pose}.png'
                canvas.save(out/name)
                result.append({'file':name,'sha256':sha((out/name).read_bytes())})
    return result


async def run(out):
    out.mkdir(parents=True,exist_ok=False)
    inputs={}
    copies={}
    parse_checks=0
    for breed,(source,names,ext) in CASES.items():
        raw=(ROOT/source).read_bytes()
        inputs[source]=sha(raw)
        original=ResourceFile(raw)
        for variant in VARIANTS:
            target=out/f'{breed}-{variant}{ext}'
            if variant=='source': target.write_bytes(raw)
            else:
                after=write_variant(raw,names,variant,target)
                if variant=='roundtrip':
                    for name in names:
                        for seed in range(256):
                            assert dict(parse_sections(original.read('LNZ',name),seed)) == dict(parse_sections(after.read('LNZ',name),seed))
                            parse_checks+=1
            copies[str(target.relative_to(ROOT))]=sha(target.read_bytes())
    dependencies=[ROOT/'games/petz4/Petz 4.exe', *[ROOT/'games/petz4/Resource'/n for n in ('Dogz 4 Rez.dll','Catz 4 Rez.dll','Petz 4 Rez.dll')]]
    inputs.update({str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in dependencies})
    package=Path(petz_renderer.__file__).parent
    sources={str(p.relative_to(package)):sha(p.read_bytes()) for p in package.rglob('*.py')}
    checkout=ROOT/'petz-renderer-mcp/src/petz_renderer'
    assert sources=={str(p.relative_to(checkout)):sha(p.read_bytes()) for p in checkout.rglob('*.py')}
    report={'experiment':'FACE-001','backend':'local stdio MCP',
      'revision':subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip(),
      'runtime':{'python':sys.version,'packages':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','Pillow','fastmcp')},'sources':sources},
      'input_hashes':inputs,'copy_hashes':copies,'parse_checks':parse_checks,
      'script_sha256':sha(Path(__file__).read_bytes()),'helper_sha256':sha((ROOT/'tools/native_anatomy_probe.py').read_bytes()),
      'geometry':[],'renders':[]}
    resolver=ResourceResolver((ROOT/'games/petz4',out))
    for breed,(_,_,ext) in CASES.items():
        for look in ('adult','young'):
            for pose in ('standing','sitting','lying'):
                assets={v:load_breed_assets(resolver,f'{breed}-{v}{ext}',look=('puppy' if breed=='labrador' else 'kitten') if look=='young' else look,pose=pose,seed=41,age=100 if look=='adult' else 12,fatness=50) for v in VARIANTS}
                base=assets['source']
                baseline=default_geometry(base.appearance,base.sizes,base.frame,fatness=50)
                for v,a in assets.items():
                    c=a.appearance
                    assert dataclasses.replace(c,shape=base.appearance.shape)==base.appearance
                    assert dataclasses.replace(c.shape,face_extension=base.appearance.shape.face_extension)==base.appearance.shape
                    assert a.frame==base.frame and a.sizes==base.sizes
                    actual=default_geometry(c,a.sizes,a.frame,fatness=50)
                    changed=[i for i,(x,y) in enumerate(zip(baseline,actual)) if x!=y]
                    assert all((x.radius,x.visible,x.parked)==(y.radius,y.visible,y.parked) for x,y in zip(baseline,actual))
                    if v in ('source','roundtrip'):assert not changed
                    report['geometry'].append({'breed':breed,'look':look,'pose':pose,'variant':v,
                      'effective_face_extension':c.shape.face_extension,'isolated':isolated_oracle(c,a.frame),
                      'changed_geometry_ids':changed,'before':[dataclasses.asdict(b) for b in baseline],
                      'after':[dataclasses.asdict(b) for b in actual]})
    (out/'prepared.json').write_text(json.dumps(report,indent=2)+'\n')
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(out)])
    async with Client(transport) as client:
        for breed,(_,_,ext) in CASES.items():
            for look in ('adult','young'):
                for pose in ('standing','sitting','lying'):
                    for yaw in (0,45,90,180):
                        baseline=None
                        for variant in VARIANTS:
                            args=dict(path=f'{breed}-{variant}{ext}',look=('puppy' if breed=='labrador' else 'kitten') if look=='young' else look,pose=pose,seed=41,age=100 if look=='adult' else 12,fatness=50,yaw_degrees=yaw)
                            response=await client.call_tool('render_pet',args)
                            assert not response.is_error, response.data
                            png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                            digest=sha(png)
                            if variant=='source':baseline=digest
                            if variant=='roundtrip':assert digest==baseline
                            name=f'{breed}-{look}-{pose}-{yaw}-{variant}.png'
                            (out/name).write_bytes(png)
                            report['renders'].append({'breed':breed,'look':look,'variant':variant,'args':args,'file':name,'sha256':digest,'meta':response.data,'differs_from_source':digest!=baseline})
                    (out/'progress.json').write_text(json.dumps(report['renders'],indent=2)+'\n')
                    print(breed,look,pose,'20 MCP renders complete',flush=True)
    report['sheets']=sheets(out,report['renders'])
    assert inputs=={p:sha((ROOT/p).read_bytes()) for p in inputs}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',len(report['renders']),'MCP renders;',len(report['geometry']),'geometry records;',parse_checks,'parse controls',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=ROOT/'scratch/research/face-001')
    asyncio.run(run(parser.parse_args().out.resolve()))
