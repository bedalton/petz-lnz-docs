"""Audit the private catalog and replay six representative local MCP views."""
import asyncio
import base64
import hashlib
import json
import sys
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'clean_dogs/reference'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def main():
    m=json.loads((OUT/'manifest.json').read_text())
    assert len(m['blanks'])==28 and len(m['inputs'])==38 and len(m['renders'])==228
    assert len({(r['key'],r['view']) for r in m['renders']})==228
    for entry in m['inputs']:
        assert sha(ROOT/entry['path'])==entry['sha256']
        assert sha(OUT/entry['sheet'])==entry['sheet_sha256']
    for path,h in m['runtime']['engines'].items():
        assert sha(ROOT/path)==h
    layout=m['sheet_layout']
    nw,nh=layout['native_canvas']
    left,top=layout['origin']
    by_key={entry['key']:entry for entry in m['inputs']}
    # Independently reconstruct and compare every displayed image tile.
    for r in m['renders']:
        path=OUT/r['image']
        assert sha(path)==r['png_sha256']==r['metadata']['png_sha256']
        im=Image.open(path).convert('RGBA')
        assert list(im.size)==r['size'] and list(im.getbbox())==r['alpha_bbox']
        a=r['metadata']['appearance']
        assert a['input_sha256']==by_key[r['key']]['sha256']
        assert a['age']==100 and a['fatness']==50 and a['seed']==41 and a['look']=='adult'
        assert r['metadata']['pose']['name']==r['arguments']['pose']
        assert r['metadata']['camera']['requested_degrees']==r['arguments']['yaw_degrees']
        ox,oy=r['metadata']['offset']
        assert 0<=left-ox and left-ox+im.width<=nw
        assert 0<=top-oy and top-oy+im.height<=nh
        expected=Image.new('RGBA',(nw,nh),layout['background'])
        expected.alpha_composite(im,(left-ox,top-oy))
        expected=expected.convert('RGB').resize((2*nw,2*nh),Image.Resampling.NEAREST)
        idx=next(i for i,v in enumerate(m['views']) if v[0]==r['view'])
        x=(idx%3)*2*nw
        y=68+(idx//3)*(2*nh+34)
        actual=Image.open(OUT/by_key[r['key']]['sheet']).convert('RGB').crop((x,y,x+2*nw,y+2*nh))
        assert ImageChops.difference(expected,actual).getbbox() is None
    assert sha(OUT/'overview.png')==m['overview_sha256']
    assert sha(ROOT/'tools/render_clean_dogs.py')==m['script_sha256']
    replay=[]
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp',
        '--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'clean_dogs')])
    selections=[('blank-bulldog','front'),('stock-bulldog','front'),
                ('blank-great-dane','side'),('stock-great-dane','side'),
                ('blank-poodle','three-quarter'),('stock-poodle','three-quarter')]
    async with Client(transport) as c:
        for key,view in selections:
            r=next(r for r in m['renders'] if r['key']==key and r['view']==view)
            result=await c.call_tool('render_pet',r['arguments'])
            assert not result.is_error
            image=next(x for x in result.content if x.type=='image')
            h=hashlib.sha256(base64.b64decode(image.data)).hexdigest()
            assert h==r['png_sha256']
            replay.append(dict(key=key,view=view,png_sha256=h))
    report=dict(inputs_verified=38,raw_pngs_verified=228,sheet_tiles_verified=228,
                sheets_verified=38,source_integrity=True,replays=replay,
                manifest_sha256=sha(OUT/'manifest.json'))
    target=ROOT/'scratch/research/clean-dogs-catalog/audit.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    asyncio.run(main())
