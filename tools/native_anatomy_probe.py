"""Copy-only Labrador ear/tail controls preserving anatomy and variation syntax.

Uses bounded in-place resource spans, not a general-purpose breed writer.
All proprietary resources, numerical detail and PNGs remain in ignored scratch.
"""
import asyncio
import base64
import dataclasses
import hashlib
import importlib.metadata
import json
import re
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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/research/anatomy-002'
SOURCE = ROOT/'clean_dogs/petz4/Labrador.dog'
VARIANTS = ('source', 'roundtrip', 'ear70', 'ear130', 'ear_fold',
            'ear_width', 'tail_short', 'tail_lower')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tok(row):
    return re.split(r'[,\s]+', row.strip())


def section_edit(text, section, edit):
    pattern = re.compile(r'(^\['+re.escape(section)+r'\][^\n]*\n)(.*?)(?=^\[|\Z)', re.M | re.S)
    matches = list(pattern.finditer(text))
    assert len(matches) == 1, section
    return pattern.sub(lambda m: m[1] + edit(m[2]).rstrip()+'\n', text)


def variant_text(raw, variant):
    # Strip only comments/blank lines; preserve variation directives and order.
    text = '\n'.join(s for line in raw.decode('cp1252').splitlines()
                     if (s := line.split(';', 1)[0].strip()))+'\n'
    if variant in ('ear70', 'ear130'):
        text = section_edit(text, 'Ear Extension', lambda _: variant[3:]+'\n')
    elif variant == 'ear_fold':
        rows = ['5,0,8,0,5', '29,0,8,0,29',
                '6,0,18,0,6', '30,0,18,0,30']
        text = section_edit(text, 'Move', lambda s: s+'\n'+'\n'.join(rows))
    elif variant == 'ear_width' and '[Add Ball]' in text:
        def widen(body):
            rows = body.strip().splitlines()
            assert len(rows) == 28 and not any('#' in s for s in rows)
            for index in range(82, 88):
                values = tok(rows[index-67])
                # Existing alternating left/right attached ear details.
                values[1] = str(int(values[1])+(-6 if index % 2 == 0 else 6))
                rows[index-67] = ','.join(values)
            return '\n'.join(rows)
        text = section_edit(text, 'Add Ball', widen)
    elif variant == 'tail_short':
        def shorten(body):
            rows = body.strip().splitlines()
            changed = []
            for i, row in enumerate(rows):
                values = tok(row)
                pair = tuple(map(int, values[:2]))
                if pair in ((57, 58), (58, 59), (59, 60)):
                    values[2] = str({(57,58):45, (58,59):75, (59,60):75}[pair])
                    rows[i] = ','.join(values)
                    changed.append(pair)
            assert changed == [(57,58), (58,59), (59,60)]
            return '\n'.join(rows)
        text = section_edit(text, 'Project Ball', shorten)
    elif variant == 'tail_lower':
        rows = [f'{i},0,{(i-56)*6},0,{i}' for i in range(57,61)]
        text = section_edit(text, 'Move', lambda s: s+'\n'+'\n'.join(rows))
    return text.encode('cp1252')


def write_variant(raw, variant):
    pe = ResourceFile(raw)
    edited = bytearray(raw)
    spans = []
    for name in ('LR', 'LRPUP'):
        leaf = next(x for x in pe.resources if x.type == 'LNZ' and x.name == name)
        payload = variant_text(pe.read('LNZ', name), variant)
        assert len(payload) <= leaf.size
        edited[leaf.offset:leaf.offset+leaf.size] = payload.ljust(leaf.size, b' ')
        spans.append((leaf.offset, leaf.offset+leaf.size))
    result = bytes(edited)
    check = ResourceFile(result)
    assert check.resources == pe.resources
    for leaf in pe.resources:
        if leaf.type != 'LNZ' or leaf.name not in ('LR','LRPUP'):
            assert pe.read(leaf.type,leaf.name,leaf.language) == check.read(leaf.type,leaf.name,leaf.language)
    cursor = 0
    for start,end in sorted(spans):
        assert raw[cursor:start] == result[cursor:start]
        cursor = end
    assert raw[cursor:] == result[cursor:]
    (OUT/f'{variant}.dog').write_bytes(result)
    return check


def xyz(ball):
    return ball.x,ball.y,ball.z


def geometry(assets):
    return default_geometry(assets.appearance, assets.sizes, assets.frame, fatness=50)


def sheet(records, look, pose, yaw):
    entries = [r for r in records if r['args']['look'] == look
               and r['args']['pose'] == pose and r['args']['yaw_degrees'] == yaw]
    left = max(r['meta']['offset'][0] for r in entries)
    top = max(r['meta']['offset'][1] for r in entries)
    right = max(r['meta']['width']-r['meta']['offset'][0] for r in entries)
    bottom = max(r['meta']['height']-r['meta']['offset'][1] for r in entries)
    w,h = left+right+20,top+bottom+30
    out = Image.new('RGB',(w*4*2,h*2*2),'#a5abb0')
    draw = ImageDraw.Draw(out)
    for i,r in enumerate(entries):
        im = Image.open(OUT/r['file']).convert('RGBA')
        tile = Image.new('RGBA',(w,h))
        tile.alpha_composite(im,(left-r['meta']['offset'][0]+10,top-r['meta']['offset'][1]+24))
        tile = tile.resize((w*2,h*2),Image.Resampling.NEAREST)
        x,y = (i%4)*w*2,(i//4)*h*2
        out.paste(tile,(x,y),tile)
        draw.text((x+8,y+6),r['variant'],fill='black')
    name=f'sheet-{look}-{pose}-{yaw}.png'
    out.save(OUT/name)
    return {'file':name,'sha256':sha((OUT/name).read_bytes())}


async def main():
    OUT.mkdir(parents=True,exist_ok=False)
    raw = SOURCE.read_bytes()
    (OUT/'source.dog').write_bytes(raw)
    pe = ResourceFile(raw)
    variants = {v:write_variant(raw,v) for v in VARIANTS if v!='source'}
    # Normalized writer control preserves every branch selected by these seeds.
    for name in ('LR','LRPUP'):
        for seed in range(256):
            assert dict(parse_sections(pe.read('LNZ',name),seed)) == dict(parse_sections(variants['roundtrip'].read('LNZ',name),seed))
    resolver = ResourceResolver((ROOT/'games/petz4',OUT))
    checks = []
    for look in ('adult','puppy'):
        for pose in ('standing','sitting','lying'):
            assets = {v:load_breed_assets(resolver,f'{v}.dog',look=look,pose=pose,
                       seed=41,age=100 if look=='adult' else 12,fatness=50) for v in VARIANTS}
            base = assets['source'].appearance
            before = geometry(assets['source'])
            for v,a in assets.items():
                c = a.appearance
                assert len(c.balls) == 67 and len(c.add_balls) == 28
                assert c.omissions == base.omissions
                assert c.lines == base.lines
                assert c.textures == base.textures
                assert [b.base for b in c.add_balls] == [b.base for b in base.add_balls]
                if v!='ear_width':
                    assert c.add_balls == base.add_balls
                else:
                    for j,(old,new) in enumerate(zip(base.add_balls,c.add_balls)):
                        assert dataclasses.replace(new,x=old.x) == old
                        assert (old.x != new.x) == (82<=67+j<=87)
                after = geometry(a)
                changed = [i for i,(x,y) in enumerate(zip(before,after)) if x!=y]
                if v in ('source','roundtrip'):
                    assert not changed
                else:
                    assert changed, (look,pose,v)
                if v.startswith('tail_'):
                    assert set(changed) <= {57,58,59,60,61,62,94}
                if v=='ear_width':
                    assert set(changed) <= set(range(82,88))
                checks.append({'look':look,'pose':pose,'variant':v,
                    'changed_geometry_ids':changed,
                    'coordinates':{str(i):{'before':xyz(before[i]),'after':xyz(after[i])} for i in changed},
                    'frame_rotations_unchanged': assets[v].frame == assets['source'].frame})
    # Preserve dependency/source hashes before renders; assert again at finish.
    deps = [SOURCE,ROOT/'games/petz4/Petz 4.exe',
            *[ROOT/'games/petz4/Resource'/n for n in ('Dogz 4 Rez.dll','Catz 4 Rez.dll','Petz 4 Rez.dll')]]
    hashes = {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in deps}
    report = {'experiment':'ANATOMY-002','input_hashes':hashes,
        'variant_hashes':{v:sha((OUT/f'{v}.dog').read_bytes()) for v in VARIANTS},
        'seed_parse_checks':512,'geometry':checks,'renders':[],
        'runtime':{'python':sys.version,'backend':'local stdio MCP',
          'packages':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','Pillow')},
          'renderer_sources':{str(p.relative_to(Path(petz_renderer.__file__).parent)):sha(p.read_bytes())
           for p in Path(petz_renderer.__file__).parent.rglob('*.py')}},
        'script_sha256':sha(Path(__file__).read_bytes())}
    (OUT/'prepared.json').write_text(json.dumps(report,indent=2)+'\n')
    transport = StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp',
                  '--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for look in ('adult','puppy'):
            for pose in ('standing','sitting','lying'):
                for yaw in (0,90):
                    baseline = None
                    for v in VARIANTS:
                        args = dict(path=f'{v}.dog',look=look,pose=pose,yaw_degrees=yaw,
                                    age=100 if look=='adult' else 12,seed=41,fatness=50)
                        response = await client.call_tool('render_pet',args)
                        assert not response.is_error, (v,response.data)
                        png = base64.b64decode(next(x.data for x in response.content if x.type=='image'))
                        digest = sha(png)
                        if v=='source':baseline=digest
                        if v=='roundtrip':assert digest==baseline
                        name=f'{look}-{pose}-{yaw}-{v}.png'
                        (OUT/name).write_bytes(png)
                        report['renders'].append({'variant':v,'args':args,'file':name,
                                                  'sha256':digest,'meta':response.data,
                                                  'differs_from_source':digest!=baseline})
                    (OUT/'progress.json').write_text(json.dumps(report['renders'],indent=2)+'\n')
                    print(look,pose,yaw,'8 renders complete',flush=True)
    report['sheets']=[sheet(report['renders'],look,pose,yaw) for look in ('adult','puppy')
                       for pose,yaw in [('standing',0),('standing',90),('sitting',90),('lying',90)]]
    assert hashes == {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in deps}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 96 MCP renders, 48 geometry records, 512 branch-preserving parse checks',flush=True)


if __name__=='__main__':
    asyncio.run(main())
