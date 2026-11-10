"""PAINT-005: copy-only prefix-array mutations through saved-pet loading."""
import asyncio
from dataclasses import asdict
import importlib.metadata
import json
from pathlib import Path
import sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from petz_renderer.formats.pet import _Reader, read_saved_appearance
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from research_common import ROOT, SHA, save_result

OUT=ROOT/'scratch/research/paint-005'
MANIFEST=ROOT/'experiments/paint-005.json'


def arrays(raw):
    # Exact supported prefix walk; production parser independently validates it.
    read_saved_appearance(raw)
    r=_Reader(raw);r.take(816);r.tag();r.take(62+4+2400+36+4+6)
    rows=[]
    for maximum,width in ((512,1),(15,4),(512,4)):
        n=r.u32();assert 0<n<=maximum
        start=r.pos;payload=r.take(n*width)
        rows.append({'offset':start,'count':n,'width':width,'sha256':SHA(payload)})
    return rows


def copies(name,verify=False):
    source=ROOT/f'games/petz4/Adopted Petz/{name}.pet';raw=source.read_bytes()
    spans=arrays(raw);variants=[]
    for mode,selected in [('array0',(0,)),('array1',(1,)),('array2',(2,)),('all',(0,1,2))]:
        edited=bytearray(raw);changed=set()
        for index in selected:
            span=spans[index];start=span['offset'];size=span['count']*span['width']
            value=b'\x01' if span['width']==1 else (65).to_bytes(4,'little')
            edited[start:start+size]=value*span['count'];changed.update(range(start,start+size))
        edited=bytes(edited)
        assert len(edited)==len(raw)
        assert all(a==b for i,(a,b) in enumerate(zip(raw,edited)) if i not in changed)
        assert raw!=edited
        # Prefix fields/caches/tail length returned by parser must all be equal.
        assert read_saved_appearance(raw)==read_saved_appearance(edited)
        actual_changed=sum(a!=b for a,b in zip(raw,edited))
        path=OUT/f'{name}-{mode}.pet'
        if verify:assert path.read_bytes()==edited
        else:path.write_bytes(edited)
        variants.append({'mode':mode,'path':path.name,'sha256':SHA(edited),'changed_bytes':actual_changed,'array_indices':selected})
    return {'name':name,'path':str(source.relative_to(ROOT/'games/petz4')),'sha256':SHA(raw),
        'arrays':spans,'variants':variants}


def render_case(source,variant,pose,yaw,verify=False):
    resolver=ResourceResolver((ROOT/'games/petz4',OUT))
    baseline=load_saved_assets(resolver,source['path'],pose=pose)
    edited=load_saved_assets(resolver,variant['path'],pose=pose)
    for field in ('appearance','sizes','frame','textures','palette'):
        assert getattr(baseline,field)==getattr(edited,field),field
    for field in ('age','fatness','seed','age_source','fatness_source','seed_source','mode'):
        assert getattr(baseline.preview,field)==getattr(edited.preview,field)
    assert baseline.diagnostics==edited.diagnostics
    first=render_portrait(baseline,yaw=yaw);second=render_portrait(edited,yaw=yaw)
    assert first.prepared==second.prepared
    assert first.png==second.png and first.indices==second.indices
    stem=f"{source['name']}-{variant['mode']}-{pose}-{yaw}"
    path=OUT/f'{stem}.png'
    if verify:assert path.read_bytes()==second.png
    else:path.write_bytes(second.png)
    prior=json.loads((ROOT/'experiments/paint-001.json').read_text())
    if source['name'] in ('Fuzzkin','Homebody'):
        c=next(c for c in prior['cases'] if c['name']==source['name'] and c['pose']==pose and c['yaw_units']==yaw)
        assert SHA(first.png)==c['outputs']['fresh']['png_sha256']
    return {'name':source['name'],'mode':variant['mode'],'path':variant['path'],'pose':pose,'yaw':yaw,
        'png':path.name,'png_sha256':SHA(second.png),'indexed_sha256':SHA(second.indices),
        'dimensions':[second.width,second.height],'species':edited.appearance.species,
        'age':edited.preview.age,'fatness':edited.preview.fatness,'seed':edited.preview.seed,
        'same_appearance_geometry_commands_and_pixels':True}


def provenance():
    p=Path(petz_renderer.__file__).parent
    hashes={str(f.relative_to(p)):SHA(f.read_bytes()) for f in sorted(p.rglob('*.py'))}
    for name,digest in hashes.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==digest
    prior=json.loads((ROOT/'experiments/paint-001.json').read_text())
    assert hashes==prior['source_hashes']
    resolver=ResourceResolver((ROOT/'games/petz4',))
    for path,digest in prior['engine_hashes'].items():assert SHA(resolver.read_bytes(path,limit=268435456).data)==digest
    return {'renderer_revision':prior['renderer_revision'],'source_hashes':hashes,'engine_hashes':prior['engine_hashes'],
        'dependencies':{n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','fastmcp','pillow')},
        'prior_manifest_sha256':SHA((ROOT/'experiments/paint-001.json').read_bytes())}


async def main():
    verify='--verify' in sys.argv
    if verify:
        report=json.loads(MANIFEST.read_text());assert report==json.loads((OUT/'report.json').read_text())
        assert provenance()==report['provenance']
        sources=[copies(name,True) for name in ('Fuzzkin','Homebody','Goobe')]
        assert json.loads(json.dumps(sources))==report['sources']
        for c in report['cases']:
            source=next(s for s in sources if s['name']==c['name'])
            variant=next(v for v in source['variants'] if v['mode']==c['mode'])
            assert render_case(source,variant,c['pose'],c['yaw'],True)==c
        for b in report['mcp']:
            assert SHA((OUT/b['png']).read_bytes())==b['png_sha256']
            meta=json.loads((OUT/b['metadata']).read_text())
            assert meta['game_version']=='petz4'
        print('PAINT-005 verified',report['summary']);return
    OUT.mkdir(parents=True,exist_ok=False)
    prov=provenance();sources=[copies(n) for n in ('Fuzzkin','Homebody','Goobe')];cases=[]
    for source in sources:
        for variant in source['variants']:
            for pose in ('standing','sitting','lying'):
                for yaw in (0,64):cases.append(render_case(source,variant,pose,yaw))
        print(source['name'],'24 direct variant renders pass',flush=True)
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4',
        '--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    mcp=[]
    async with Client(transport) as client:
        for source in sources:
            for yaw in (0,64):
                for mode in ('baseline','array0','array1','array2','all'):
                    c=next(c for c in cases if c['name']==source['name'] and c['pose']=='standing' and c['yaw']==yaw and c['mode']==('all' if mode=='baseline' else mode))
                    args={'path':source['path'] if mode=='baseline' else c['path'],'pose':'standing','yaw_degrees':yaw*360/256}
                    stem=f"{source['name']}-{mode}-{yaw}-mcp"
                    png,meta=await save_result(client,'render_pet',args,OUT,stem)
                    assert SHA(png)==c['png_sha256'] and meta['game_version']=='petz4'
                    mcp.append({'name':source['name'],'mode':mode,'controls':args,'png':stem+'.png',
                        'metadata':stem+'-render.json','png_sha256':SHA(png)})
    for source in sources:assert SHA((ROOT/'games/petz4'/source['path']).read_bytes())==source['sha256']
    report={'experiment':'PAINT-005','backend':'copy-only Petz4 saved-file prefix mutations; direct API and fresh local stdio MCP',
        'provenance':prov,'controls':{'seed_age_fatness':'saved','poses':['standing','sitting','lying'],
            'yaw_units':[0,64],'raster_seed':1,'line_seed':1,'step':0,'array0_byte':1,'array1_and_2_u32':65},
        'sources':sources,'cases':cases,'mcp':mcp,
        'summary':{'saved_pets':3,'copies':12,'direct_variant_views':72,'direct_baseline_draws':72,
            'mcp_views':30,'mcp_variant_equivalences':24,'prior_pixel_links':48}}
    for path in (MANIFEST,OUT/'report.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print(report['summary'],flush=True)

if __name__=='__main__':asyncio.run(main())
