"""FACE-002: explicit Face Extension controls across Petz3/4/5.

Compares arithmetic/geometry across matched source assets; uses local MCP for
all sampled pose/look/yaw endpoints. Private resources remain under scratch.
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
from petz_renderer.appearance.lnz import parse_sections
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.attachment import default_geometry
from face_extension_probe import write_variant, isolated_oracle, sha

ROOT=Path(__file__).resolve().parents[1]
VARIANTS=('source','roundtrip','face0','face-12','face12')
SPECIES=(('Dogz','Scottie.dog',('SC','SCPUP'),'puppy'),('Catz','Siamese.cat',('SI','SIKIT'),'kitten'))

async def run(out):
    out.mkdir(parents=True,exist_ok=False)
    package=Path(petz_renderer.__file__).parent
    sources={str(p.relative_to(package)):sha(p.read_bytes()) for p in package.rglob('*.py')}
    checkout=ROOT/'petz-renderer-mcp/src/petz_renderer'
    assert sources=={str(p.relative_to(checkout)):sha(p.read_bytes()) for p in checkout.rglob('*.py')}
    report={'experiment':'FACE-002','backend':'local stdio MCP',
      'revision':subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip(),
      'packages':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','Pillow','fastmcp')},
      'sources':sources,'script_sha256':sha(Path(__file__).read_bytes()),
      'helper_sha256':sha((ROOT/'tools/face_extension_probe.py').read_bytes()),
      'input_hashes':{},'copy_hashes':{},'parse_checks':0,'geometry':[],'renders':[]}
    for version in ('petz3','petz4','petz5'):
        folder=out/version;folder.mkdir()
        game=ROOT/'games'/version
        for path in [game/f'Petz {version[-1]}.exe',*[game/'Resource'/f'{s} {version[-1]} Rez.dll' for s in ('Dogz','Catz','Petz')]]:
            report['input_hashes'][str(path.relative_to(ROOT))]=sha(path.read_bytes())
        for species,filename,names,young in SPECIES:
            original=game/'Resource'/species/filename
            raw=original.read_bytes();pe=ResourceFile(raw)
            report['input_hashes'][str(original.relative_to(ROOT))]=sha(raw)
            for v in VARIANTS:
                target=folder/f'{v}{Path(filename).suffix}'
                if v=='source':target.write_bytes(raw)
                else:
                    after=write_variant(raw,names,v,target)
                    if v=='roundtrip':
                        for name in names:
                            for seed in range(256):
                                assert dict(parse_sections(pe.read('LNZ',name),seed))==dict(parse_sections(after.read('LNZ',name),seed))
                                report['parse_checks']+=1
                report['copy_hashes'][str(target.relative_to(ROOT))]=sha(target.read_bytes())
        resolver=ResourceResolver((game,folder),game_version=version)
        for species,filename,names,young in SPECIES:
            for look in ('adult',young,'age'):
                for age in (0,12,50,100):
                    for pose in ('standing','sitting','lying'):
                        assets={v:load_breed_assets(resolver,f'{v}{Path(filename).suffix}',look=look,age=age,seed=41,fatness=50,pose=pose) for v in VARIANTS}
                        base=assets['source'];before=default_geometry(base.appearance,base.sizes,base.frame,fatness=50)
                        for v,a in assets.items():
                            assert dataclasses.replace(a.appearance,shape=base.appearance.shape)==base.appearance
                            assert dataclasses.replace(a.appearance.shape,face_extension=base.appearance.shape.face_extension)==base.appearance.shape
                            assert a.frame==base.frame and a.sizes==base.sizes
                            after=default_geometry(a.appearance,a.sizes,a.frame,fatness=50)
                            assert all((a.radius,a.visible,a.parked)==(b.radius,b.visible,b.parked) for a,b in zip(before,after))
                            report['geometry'].append({'version':version,'species':species,'look':look,'age':age,'pose':pose,'variant':v,
                              'effective_face_extension':a.appearance.shape.face_extension,
                              'isolated':isolated_oracle(a.appearance,a.frame),
                              'geometry':[dataclasses.asdict(b) for b in after],
                              'changed_geometry_ids':[i for i,(a,b) in enumerate(zip(before,after)) if a!=b]})
        transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(game),'--game-version',version,'--asset-root',str(folder)])
        async with Client(transport) as client:
            for species,filename,names,young in SPECIES:
                for look in ('adult',young,'age'):
                    for pose in ('standing','sitting','lying'):
                        for yaw in (0,90):
                            baseline=None
                            for v in VARIANTS:
                                args=dict(path=f'{v}{Path(filename).suffix}',look=look,age=100 if look=='adult' else 12,seed=41,fatness=50,pose=pose,yaw_degrees=yaw)
                                response=await client.call_tool('render_pet',args)
                                assert not response.is_error,response.data
                                png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                                digest=sha(png)
                                if v=='source':baseline=digest
                                if v=='roundtrip':assert digest==baseline
                                name=f'{version}/{species}-{look}-{pose}-{yaw}-{v}.png'
                                (out/name).write_bytes(png)
                                report['renders'].append({'version':version,'species':species,'look':look,'variant':v,'args':args,'file':name,'sha256':digest,'meta':response.data,'differs_from_source':digest!=baseline})
                        (out/'progress.json').write_text(json.dumps(report['renders'],indent=2)+'\n')
                        print(version,species,look,pose,'10 MCP renders complete',flush=True)
        (out/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    assert report['input_hashes']=={p:sha((ROOT/p).read_bytes()) for p in report['input_hashes']}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',len(report['geometry']),'geometry records;',len(report['renders']),'MCP renders;',report['parse_checks'],'parse controls',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'scratch/research/face-002')
    asyncio.run(run(p.parse_args().out.resolve()))
