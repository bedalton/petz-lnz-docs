"""Independent saved-evidence/provenance audit for MORPH-006/007/008."""
import asyncio
import base64
from io import BytesIO
import json
from pathlib import Path

from fastmcp import Client
from PIL import Image, ImageDraw
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.output import render_portrait
from research_common import ROOT, SHA
from revalidate_relative_morph import provenance, audit_cells

RESEARCH=ROOT/'scratch/research'


def main():
    prov=provenance()
    reports={u:json.loads((ROOT/f'experiments/{u}.json').read_text()) for u in ('morph-006','morph-007','morph-008')}
    pngs,metadata,copies,originals,logs={},{},{},{},{}
    for unit,r in reports.items():
        assert r==json.loads((RESEARCH/unit/'report.json').read_text())
        for key,value in prov.items():
            assert r[key]==value
        log=(ROOT/'scratch'/f'{unit}-verify.log').read_bytes()
        assert ('Verified 144 numerical cases and 36 MCP pairs' if unit=='morph-006' else 'Full replay verified') in log.decode()
        logs[unit]=SHA(log)
    six=reports['morph-006']
    for version,records in six['engine_hashes'].items():
        resolver=ResourceResolver((ROOT/'games'/version,),game_version=version)
        for name,digest in records.items():
            resolved=resolver.resolve(name)
            assert SHA(resolved.path.read_bytes())==digest
            originals[str(resolved.path.relative_to(ROOT))]=digest
    for c in six['cases']:
        assert c['historical_petz4_geometry_equal']
        assert SHA((ROOT/c['source']).read_bytes())==c['source_sha256']
        originals[c['source']]=c['source_sha256']
        for name,path in c['paths'].items():
            p=RESEARCH/'morph-006'/path
            assert SHA(p.read_bytes())==c['input_hashes'][name]
            copies[str(p.relative_to(ROOT))]=c['input_hashes'][name]
    for row in six['comparisons']:
        folder=RESEARCH/'morph-006'
        meta=audit_cells(folder,row['stem'],row['equal_expected'],row['png_sha256'])
        for cell,path in zip(meta['cells'],(row['controls']['before_path'],row['controls']['after_path']),strict=True):
            assert cell['appearance']['input_sha256']==SHA((folder/path).read_bytes())
            assert cell['game_version']==row['version']
            assert cell['pose']['name']==row['controls']['pose']
            for key in ('age','seed','fatness'):
                assert cell['appearance'][key]==row['controls'][key]
        assert meta['camera']['requested_degrees']==row['controls']['yaw_degrees']
        p=folder/(row['stem']+'.png');pngs[str(p.relative_to(ROOT))]=SHA(p.read_bytes())
        p=folder/(row['stem']+'-render.json');metadata[str(p.relative_to(ROOT))]=SHA(p.read_bytes())
    base=[r for r in six['comparisons'] if r['version']=='petz4']
    for version in ('petz3','petz5'):
        rows=[r for r in six['comparisons'] if r['version']==version]
        for a,b in zip(rows,base,strict=True):
            assert a['species']==b['species'] and a['controls']['yaw_degrees']==b['controls']['yaw_degrees']
            assert a['png_sha256']==b['png_sha256'] and a['cell_hashes']==b['cell_hashes']
    links=0;comparisons=[];sheets={}
    for unit in ('morph-007','morph-008'):
        r=reports[unit];folder=RESEARCH/unit
        assert r['baseline_manifest_sha256']==SHA((ROOT/'experiments/morph-006.json').read_bytes())
        for c in r['cases']:
            assert SHA((ROOT/c['source']).read_bytes())==c['source_sha256']
            assert originals[c['source']]==c['source_sha256'];links+=1
        for fixture in r['rasters']:
            images={}
            for row in fixture['records']:
                p=folder/row['png'];raw=p.read_bytes();assert SHA(raw)==row['png_sha256']
                pngs[str(p.relative_to(ROOT))]=SHA(raw)
                im=Image.open(BytesIO(raw)).convert('RGBA')
                assert im.size==(row['width'],row['height'])
                if 'rgba_sha256' in row:assert SHA(im.tobytes())==row['rgba_sha256']
                images[row['name']]=im
            pairs=[]
            if unit=='morph-007':
                for prior in ('active','dormant'):
                    for target in ('forward','outside'):
                        pairs.append((prior+'-self',prior+'-'+target,True))
            else:
                for topology in ('chain','cycle'):
                    for mode in ('static','all_group15','root_static','root_dormant','root_activated'):
                        pairs.append((f'{topology}-{mode}-ABC',f'{topology}-{mode}-CBA',None))
            for left,right,expected in pairs:
                a,b=images[left],images[right];assert a.size==b.size
                x,y=a.tobytes(),b.tobytes()
                changed=sum(x[i:i+4]!=y[i:i+4] for i in range(0,len(x),4))
                if expected:assert changed==0
                comparisons.append({'unit':unit,'species':fixture['species'],'pose':fixture['pose'],
                                    'left':left,'right':right,'rgba_changed_pixels':changed})
            if unit=='morph-008' and fixture['pose']=='standing':
                names=[f'{topology}-{mode}-{order}' for topology in ('chain','cycle') for mode in ('static','all_group15','root_static') for order in ('ABC','CBA')]
                w,h=next(iter(images.values())).size
                sheet=Image.new('RGBA',(w*4,(h+20)*3),(255,255,255,255));d=ImageDraw.Draw(sheet)
                for i,name in enumerate(names):
                    x=(i%4)*w;y=(i//4)*(h+20)
                    d.text((x+2,y+3),name,fill=(0,0,0,255));sheet.paste(images[name],(x,y+20))
                p=folder/f'{fixture["species"]}-standing-chain-sheet.png';sheet.save(p)
                sheets[str(p.relative_to(ROOT))]={'sha256':SHA(p.read_bytes()),'cells':names,'cell_size':[w,h],'label_height':20}
    # Check each reviewed boundary sheet cell against its independently saved raster.
    for row in json.loads((RESEARCH/'morph-007/review-sheets.json').read_text()):
        folder=RESEARCH/'morph-007';p=folder/row['png'];assert SHA(p.read_bytes())==row['sha256']
        im=Image.open(p).convert('RGBA');w,h=row['cell_size'];species=row['png'].split('-')[0]
        for i,name in enumerate(row['cells']):
            x=(i%3)*w;y=(i//3)*(h+20)+20
            assert im.crop((x,y,x+w,y+h)).tobytes()==Image.open(folder/f'{species}-standing-{name}.png').convert('RGBA').tobytes()
        sheets[str(p.relative_to(ROOT))]=row
    assert (len(pngs),len(metadata),len(copies),len(originals),links,len(comparisons))==(228,36,30,18,12,84)
    numerical=sum(len(c['geometry']) for c in six['cases'])+sum(len(c['checks']) for u in ('morph-007','morph-008') for c in reports[u]['cases'])
    assert numerical==2808
    restoration=json.loads((ROOT/'scratch/relative-morph-originals.log').read_text())
    assert len(restoration['checks'])==21 and all(c['ok'] for c in restoration['checks'])
    result={'renderer_revision':prov['renderer_revision'],'source_files':len(prov['source_hashes']),
        'restoration_originals_checked':21,'restoration_log_sha256':SHA((ROOT/'scratch/relative-morph-originals.log').read_bytes()),
        'numerical_records':numerical,'research_pngs':len(pngs),'mcp_comparison_pairs':36,'direct_rasters':192,
        'copies':len(copies),'original_hash_links':len(originals),'cross_unit_original_links':links,
        'rgba_pair_checks':len(comparisons),'rgba_comparisons':comparisons,'review_sheets':sheets,
        'unit_replay_log_hashes':logs,'png_hashes':pngs,'metadata_hashes':metadata,'copy_hashes':copies,'original_hashes':originals,
        'manifest_hashes':{u:SHA((ROOT/f'experiments/{u}.json').read_bytes()) for u in reports},
        'tool_hashes':{name:SHA((ROOT/'tools'/name).read_bytes()) for name in ('revalidate_relative_morph.py','morph_reference_boundaries.py','morph_size_chains.py','check_relative_morph_session.py')}}
    (RESEARCH/'relative-morph-session-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if isinstance(v,(int,str))})
    for mode in ('static','all_group15','root_static','root_dormant','root_activated'):
        print(mode,[(t,sum(c['rgba_changed_pixels']>0 for c in comparisons if c['unit']=='morph-008' and c['left']==f'{t}-{mode}-ABC')) for t in ('chain','cycle')])


async def health():
    controls={'path':'Resource/Dogz/Scottie.dog','pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':0}
    resolver=ResourceResolver((ROOT/'games/petz4',))
    assets=load_breed_assets(resolver,controls['path'],pose='standing',seed=0,age=100,fatness=50)
    expected=render_portrait(assets,fatness=50).png
    async with Client('http://127.0.0.1:8765/mcp') as client:
        tools=await client.list_tools();caps=await client.call_tool('get_capabilities',{})
        response=await client.call_tool('render_pet',controls)
        assert len(tools)==6 and not caps.is_error and not response.is_error
        png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
        assert png==expected
        meta=response.data
        assert meta['game_version']=='petz4' and meta['pose']['name']=='standing'
        assert meta['appearance']['input_sha256']==SHA((ROOT/'games/petz4'/controls['path']).read_bytes())
        for key in ('age','seed','fatness'):
            assert meta['appearance'][key]==controls[key]
        result={'tools':[t.name for t in tools],'capabilities':caps.data,'controls':controls,
                'png_sha256':SHA(png),'metadata':response.data,'direct_png_match':True}
        (RESEARCH/'relative-morph-session-health.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Local HTTP discovery/capabilities/actual render match passed')


if __name__=='__main__':
    main();asyncio.run(health())
