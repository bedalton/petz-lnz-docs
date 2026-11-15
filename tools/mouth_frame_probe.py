"""MOUTH-001 raw-frame previews: existing tongue geometry and face controls.

Uses only prior FACE-001 copies; does not edit anatomy or assign behavior names.
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
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.attachment import default_geometry
from petz_renderer.rendering.output import render_portrait
from face_extension_probe import sha

ROOT=Path(__file__).resolve().parents[1]
COPIES=ROOT/'scratch/research/face-001'
INVENTORY=ROOT/'scratch/research/mouth-001/inventory.json'
VARIANTS=('source','face-12','face12')

def make_sheet(out,records,breed,look,yaw):
    selected=[r for r in records if (r['breed'],r['look'],r['args']['yaw_degrees'])==(breed,look,yaw)]
    # Individual frame groups align their origin; shared native-sized cell extents.
    left=max(r['meta']['offset'][0] for r in selected);top=max(r['meta']['offset'][1] for r in selected)
    right=max(r['meta']['width']-r['meta']['offset'][0] for r in selected)
    bottom=max(r['meta']['height']-r['meta']['offset'][1] for r in selected)
    w,h=left+right+12,top+bottom+24
    canvas=Image.new('RGB',(w*3*2,h*12*2),'#a9aeb2');draw=ImageDraw.Draw(canvas)
    for i,r in enumerate(selected):
        im=Image.open(out/r['file']).convert('RGBA');tile=Image.new('RGBA',(w,h))
        tile.alpha_composite(im,(left-r['meta']['offset'][0]+6,top-r['meta']['offset'][1]+20))
        tile=tile.resize((w*2,h*2),Image.Resampling.NEAREST)
        x,y=(i%3)*w*2,(i//3)*h*2;canvas.paste(tile,(x,y),tile)
        draw.text((x+4,y+4),f"{r['variant']} a{r['args']['animation']} f{r['args']['frame']}",fill='black')
    name=f'sheet-{breed}-{look}-{yaw}.png';canvas.save(out/name)
    return {'file':name,'sha256':sha((out/name).read_bytes())}

async def run(out):
    out.mkdir(parents=True,exist_ok=False)
    inventory=json.loads(INVENTORY.read_text())
    face=json.loads((COPIES/'report.json').read_text())
    report={'experiment':'MOUTH-001','backend':'local stdio MCP plus fresh direct Python',
      'revision':subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip(),
      'packages':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','Pillow','fastmcp')},
      'script_sha256':sha(Path(__file__).read_bytes()),'inventory_sha256':sha(INVENTORY.read_bytes()),
      'source_report_sha256':sha((COPIES/'report.json').read_bytes()),'input_hashes':face['input_hashes'],
      'copy_hashes':face['copy_hashes'],'sources':face['runtime']['sources'],'geometry':[],'renders':[]}
    package=Path(petz_renderer.__file__).parent
    assert report['sources']=={str(p.relative_to(package)):sha(p.read_bytes()) for p in package.rglob('*.py')}
    resolver=ResourceResolver((ROOT/'games/petz4',COPIES))
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(COPIES)])
    async with Client(transport) as client:
        for item in inventory['species']:
            breed,ext,young=('labrador','.dog','puppy') if item['species']=='Dogz' else ('siamese','.cat','kitten')
            for look in ('adult',young):
                for selection in item['selected']:
                    animation,frame=selection['animation'],selection['frame']
                    assets={v:load_breed_assets(resolver,f'{breed}-{v}{ext}',look=look,animation=animation,frame=frame,seed=41,age=100 if look=='adult' else 12,fatness=50) for v in VARIANTS}
                    base=assets['source'];before=default_geometry(base.appearance,base.sizes,base.frame,fatness=50)
                    for variant,a in assets.items():
                        assert a.frame==base.frame and a.sizes==base.sizes
                        assert dataclasses.replace(a.appearance,shape=base.appearance.shape)==base.appearance
                        after=default_geometry(a.appearance,a.sizes,a.frame,fatness=50)
                        assert all((x.radius,x.visible,x.parked)==(y.radius,y.visible,y.parked) for x,y in zip(before,after))
                        tongue=[{'id':i,'before':dataclasses.asdict(before[i]),'after':dataclasses.asdict(after[i])} for i in item['tongue_ids']]
                        if breed=='labrador':tongue.append({'id':77,'before':dataclasses.asdict(before[77]),'after':dataclasses.asdict(after[77])})
                        report['geometry'].append({'breed':breed,'look':look,'animation':animation,'frame':frame,'variant':variant,'tongue':tongue,'changed_geometry_ids':[i for i,(x,y) in enumerate(zip(before,after)) if x!=y]})
                    for yaw in (0,90):
                        for variant,a in assets.items():
                            args=dict(path=f'{breed}-{variant}{ext}',look=look,pose='default',animation=animation,frame=frame,seed=41,age=100 if look=='adult' else 12,fatness=50,yaw_degrees=yaw)
                            response=await client.call_tool('render_pet',args);assert not response.is_error,response.data
                            png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                            direct=render_portrait(a,yaw=yaw*256//360)
                            assert png==direct.png
                            name=f'{breed}-{look}-a{animation}-f{frame}-{yaw}-{variant}.png';(out/name).write_bytes(png)
                            report['renders'].append({'breed':breed,'look':look,'variant':variant,'args':args,'file':name,'sha256':sha(png),'meta':response.data,'matches_fresh_direct':True})
                    (out/'progress.json').write_text(json.dumps(report['renders'],indent=2)+'\n')
                print(breed,look,'72 exact MCP/direct matches',flush=True)
    report['sheets']=[make_sheet(out,report['renders'],breed,look,yaw) for breed,looks in [('labrador',('adult','puppy')),('siamese',('adult','kitten'))] for look in looks for yaw in (0,90)]
    assert report['input_hashes']=={p:sha((ROOT/p).read_bytes()) for p in report['input_hashes']}
    assert report['copy_hashes']=={p:sha((ROOT/p).read_bytes()) for p in report['copy_hashes']}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS 288 exact MCP/direct pairs; 144 geometry checks; eight sheets',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'scratch/research/mouth-001/renders')
    asyncio.run(run(p.parse_args().out.resolve()))
