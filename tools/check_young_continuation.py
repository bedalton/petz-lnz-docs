"""Independent hash/RGBA/link/original audit for YOUNG-004 through007."""
import asyncio,base64,io,json,subprocess,sys
from PIL import Image
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from young_breed_probe import ROOT,digest,provenance
OUT=ROOT/'scratch/research/young-continuation'
def aligned_pixels(a,b):
    # Independent reconstruction from saved PNGs, offsets and alpha bytes.
    images=[Image.open(p).convert('RGBA') for p,_ in (a,b)]
    x0=min(-o[0] for _,o in (a,b));y0=min(-o[1] for _,o in (a,b))
    x1=max(im.width-o[0] for im,(_,o) in zip(images,(a,b)));y1=max(im.height-o[1] for im,(_,o) in zip(images,(a,b)))
    decoded=[]
    for im,(_,offset) in zip(images,(a,b)):
        canvas=Image.new('RGBA',(x1-x0,y1-y0));canvas.paste(im,(-offset[0]-x0,-offset[1]-y0));decoded.append(canvas.tobytes())
    return sum(decoded[0][i:i+4]!=decoded[1][i:i+4] for i in range(0,len(decoded[0]),4))
async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    reports={i:json.loads((ROOT/f'experiments/young-00{i}.json').read_text()) for i in (4,5,6,7)}
    current=provenance();assert all(r['provenance']==current for r in reports.values())
    result={'renderer_revision':current['revision'],'source_count':len(current['sources']),'pngs':[],'counts':{},'links':[]}
    def check(path,row,unit):
        raw=path.read_bytes();assert digest(raw)==row['png_sha256'],path
        image=Image.open(io.BytesIO(raw)).convert('RGBA');assert list(image.size)==row['size']
        result['pngs'].append({'unit':unit,'path':str(path.relative_to(ROOT)),'png_sha256':digest(raw),'rgba_sha256':digest(image.tobytes())})
    for row in reports[4]['copies']:
        assert digest((ROOT/row['source']).read_bytes())==row['source_sha256']
        assert digest((ROOT/'scratch/research/young-004'/row['path']).read_bytes())==row['sha256']
    for row in reports[4]['cases']:
        for image in row.get('renders',[]):
            check(ROOT/f'scratch/research/young-004/{row["species"]}-{row["mode"]}-{row["label"]}-{image["yaw"]}.png',image,4)
    previous=json.loads((ROOT/'experiments/young-002.json').read_text())
    assert digest((ROOT/'experiments/young-002.json').read_bytes())==reports[5]['prior_manifest_sha256']
    for i in (6,7):assert digest((ROOT/f'experiments/young-00{i-1}.json').read_bytes())==reports[i]['prior_manifest_sha256']
    inputs=reports[5]['inputs']
    assert all(reports[i]['inputs']==inputs for i in (6,7))
    assert digest((ROOT/'games/petz4'/inputs['source']).read_bytes())==inputs['source_sha256']
    for variant in inputs['variants'].values():assert digest((ROOT/'scratch/research/young-002'/variant['path']).read_bytes())==variant['sha256']
    targets={}
    for row in reports[5]['renders']:
        label='young' if row['groups']=='forced-young' else '-'.join(row['groups']) or 'none'
        path=ROOT/f'scratch/research/young-005/{row["mode"]}-{row["pose"]}-{row["yaw"]}-{label}.png'
        check(path,row,5)
        if label=='young':targets[row['mode'],row['pose'],row['yaw']]=(path,row['offset'])
    pixel_checks=0
    for i in (5,6,7):
        for row in reports[i]['renders']:
            if i==5:
                if row['groups']=='forced-young':continue
                label='-'.join(row['groups']) or 'none'
            else:label=row['label']
            path=ROOT/f'scratch/research/young-00{i}/{row["mode"]}-{row["pose"]}-{row["yaw"]}-{label}.png'
            if i!=5:check(path,row,i)
            count=aligned_pixels((path,row['offset']),targets[row['mode'],row['pose'],row['yaw']])
            assert count==row['pixels_vs_young'],(i,path,count,row['pixels_vs_young'])
            assert row['equals_young']==(digest(path.read_bytes())==digest(targets[row['mode'],row['pose'],row['yaw']][0].read_bytes()) and list(row['offset'])==list(targets[row['mode'],row['pose'],row['yaw']][1]))
            pixel_checks+=1
    # Link unchanged baselines independently across all four manifests.
    p5={(r['mode'],r['pose'],r['yaw'],tuple(r['groups']) if isinstance(r['groups'],list) else r['groups']):r for r in reports[5]['renders']}
    p6={(r['mode'],r['pose'],r['yaw'],r['label']):r for r in reports[6]['renders']}
    for r in reports[6]['renders']:
        if r['label']=='none':
            old=p5[r['mode'],r['pose'],r['yaw'],()];assert r['png_sha256']==old['png_sha256'];result['links'].append({'from':6,'to':5,'sha256':r['png_sha256']})
    for r in reports[7]['renders']:
        if r['label']=='full':
            old=p6[r['mode'],r['pose'],r['yaw'],'all-non-speckle'];assert r['png_sha256']==old['png_sha256'];result['links'].append({'from':7,'to':6,'sha256':r['png_sha256']})
    for r in previous['cases']:
        if r['name']=='Fuzzkin' and ((r['look']=='age' and r['age']==12) or (r['look']=='puppy' and r['age']==0)):
            old=p5[r['mode'],'standing',r['yaw_degrees'],() if r['look']=='age' else 'forced-young'];assert r['png_sha256']==old['png_sha256'];result['links'].append({'from':5,'to':2,'sha256':r['png_sha256']})
    originals=json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True));assert all(r['ok'] for r in originals['checks'])
    result['originals']=originals
    scripts=('young_resource_routing.py','young_endpoint_attribution.py','young_endpoint_fields.py','young_endpoint_entries.py','young_continuation_sheets.py','check_young_continuation.py')
    result['scripts']={name:digest((ROOT/'tools'/name).read_bytes()) for name in scripts}
    result['manifests']={str(i):digest((ROOT/f'experiments/young-00{i}.json').read_bytes()) for i in reports}
    result['replay_logs']={}
    for i in reports:
        path=ROOT/f'scratch/young-00{i}-verify.log';raw=path.read_bytes();assert b'FULL REPLAY PASS' in raw and b'Traceback' not in raw
        result['replay_logs'][str(i)]={'path':str(path.relative_to(ROOT)),'sha256':digest(raw)}
    result['sheets']=json.loads((OUT/'sheets.json').read_text());assert len(result['sheets'])==4
    for sheet in result['sheets']:assert digest((ROOT/sheet['path']).read_bytes())==sheet['sha256']
    async with Client('http://127.0.0.1:8765/mcp') as client:
        discovered=await client.list_tools();assert len(discovered)==6
        assert 'young_name' in next(t.input_schema for t in discovered if t.name=='render_pet')['properties']
        cap=await client.call_tool('get_capabilities');assert not cap.is_error
        args={'path':'Resource/Dogz/Scottie.dog','pose':'standing','seed':41,'age':12,'look':'puppy','fatness':50,'yaw_degrees':0}
        response=await client.call_tool('render_pet',args);assert not response.is_error
        png=base64.b64decode(next(x.data for x in response.content if x.type=='image'))
        baseline=next(r for r in reports[4]['cases'] if (r['species'],r['mode'],r['label'])==('Dogz','control','young'))
        assert digest(png)==baseline['renders'][0]['png_sha256']
        result['http']={'controls':args,'png_sha256':digest(png),'tools':len(discovered),'capabilities':'pass'}
        (OUT/'http-capabilities.json').write_text(json.dumps(cap.data,indent=2)+'\n')
    # Audit the schema's zero-based wording against this controlled two-branch fixture.
    branch=next(r for r in reports[4]['mcp'] if (r['species'],r['mode'],r['label'])==('Dogz','branch','branch-valid'))
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/young-004')])
    result['branch_numbering_audit']=[]
    async with Client(transport) as client:
        schema=next(t.input_schema for t in await client.list_tools() if t.name=='render_pet')
        result['branch_choice_schema']=schema['properties']['branch_choices']['anyOf'][0]['items']
        for number in (0,1,2,3):
            args=dict(branch['controls']);args['branch_choices']=[{**args['branch_choices'][0],'branch':number}]
            response=await client.call_tool('render_pet',args,raise_on_error=False)
            assert response.is_error==(number!=1)
            entry={'branch':number,'success':not response.is_error}
            if response.is_error:entry['content']=str(response.content)
            else:
                png=base64.b64decode(next(x.data for x in response.content if x.type=='image'));assert digest(png)==branch['png_sha256'];entry['png_sha256']=digest(png)
            result['branch_numbering_audit'].append(entry)
    result['counts']={'saved_research_pngs':len(result['pngs']),'decoded_rgba_comparisons':pixel_checks,'original_hashes':len(originals['checks']),'new_private_breed_copies':14,'reused_saved_copies':4,'initial_mcp_requests':len(reports[4]['mcp'])+len(reports[5]['mcp']),'initial_mcp_successes':sum(r['success'] for r in reports[4]['mcp'])+len(reports[5]['mcp']),'initial_expected_mcp_errors':sum(not r['success'] for r in reports[4]['mcp']),'prior_png_links':len(result['links']),'reviewed_sheets':len(result['sheets'])}
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n');(ROOT/'experiments/young-continuation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['counts'],indent=2));print('SESSION AUDIT PASS')
if __name__=='__main__':asyncio.run(main())
