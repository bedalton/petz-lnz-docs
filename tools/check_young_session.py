"""Audit young research hashes, links, pixels and current HTTP health."""
import asyncio,base64,io,json,subprocess,sys
from pathlib import Path
from fastmcp import Client
from PIL import Image
from young_breed_probe import ROOT,digest,provenance
OUT=ROOT/'scratch/research/young-session'
def read(name): return json.loads((ROOT/f'experiments/{name}.json').read_text())
def check_png(path,row):
    png=path.read_bytes();assert digest(png)==row['png_sha256'],path
    im=Image.open(io.BytesIO(png)).convert('RGBA')
    if 'rgba_sha256' in row: assert digest(im.tobytes())==row['rgba_sha256']
    if 'size' in row: assert list(im.size)==row['size']
async def main():
    OUT.mkdir(exist_ok=True,parents=True)
    reports=[read(f'young-00{i}') for i in (1,2,3)]
    assert all(r['provenance']==provenance() for r in reports)
    first,second,third=reports
    cross=[]
    bykey={(x['version'],x['species'],x['label']):x for x in first['cases']}
    for row in first['cases']:
        stem=f"{row['version']}-{row['species']}-{row['label']}"
        check_png(ROOT/f'scratch/research/young-001/{stem}.png',row)
        assert digest((ROOT/'games'/row['version']/row['controls']['path']).read_bytes())==row['input_sha256']
        if row['version']!='petz4':
            base=bykey['petz4',row['species'],row['label']]
            cross.append({'version':row['version'],'species':row['species'],'label':row['label'],'rgba_equal':(row['rgba_sha256'],row['size'],row['offset'])==(base['rgba_sha256'],base['size'],base['offset'])})
    for row in second['cases']:
        stem=f"{row['name']}-{row['mode']}-{row['look']}-{row['age']}-{row['yaw_degrees']}"
        check_png(ROOT/f'scratch/research/young-002/{stem}.png',row)
    saved_bykey={(x['name'],x['mode'],x['look'],x['age'],x['yaw_degrees']):x for x in second['cases']}
    saved_endpoints=[]
    def signature(row): return row['rgba_sha256'],row['size'],row['offset']
    for name in ('Fuzzkin','Homebody','Goobe'):
        for mode in ('baseline','missing-adult','missing-young','missing-both'):
            for yaw in (0,90):
                age12=saved_bykey[name,mode,'age',12,yaw]; young=saved_bykey[name,mode,'puppy',0,yaw]
                age100=saved_bykey[name,mode,'age',100,yaw]; adult=saved_bykey[name,mode,'adult',100,yaw]
                saved_endpoints.append({'name':name,'mode':mode,'yaw_degrees':yaw,'age12_equals_forced_young':signature(age12)==signature(young),'age100_equals_forced_adult':signature(age100)==signature(adult)})
    for source in second['copies']:
        assert digest((ROOT/'games/petz4'/source['source']).read_bytes())==source['source_sha256']
        for row in source['variants'].values():assert digest((ROOT/'scratch/research/young-002'/row['path']).read_bytes())==row['sha256']
    for row in third['renders']:
        stem=f"{row['species']}-{row['mode']}-{row['look']}-{row['age']}-{row['yaw']}"
        check_png(ROOT/f'scratch/research/young-003/{stem}.png',row)
    for row in third['copies']:assert digest((ROOT/'scratch/research/young-003'/row['path']).read_bytes())==row['sha256']
    originals=json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True))
    assert all(x['ok'] for x in originals['checks'])
    async with Client('http://127.0.0.1:8765/mcp') as client:
        tools=await client.list_tools();assert len(tools)==6
        capabilities=await client.call_tool('get_capabilities')
        controls=bykey['petz4','Dogz','age-12-standing-0']['controls']
        response=await client.call_tool('render_pet',controls);assert not response.is_error
        png=base64.b64decode(next(x.data for x in response.content if x.type=='image'))
        assert digest(png)==bykey['petz4','Dogz','age-12-standing-0']['png_sha256']
        (OUT/'http-capabilities.json').write_text(json.dumps(capabilities.data,indent=2))
    record={'renderer_revision':first['provenance']['revision'],'counts':{'research_pngs':len(first['cases'])+len(second['cases'])+len(third['renders']),'breed_mcp_renders':len(first['cases']),'saved_direct_renders':len(second['cases']),'saved_mcp_matches':len(second['mcp']),'young_edit_direct_renders':len(third['renders']),'young_edit_original_control_renders':28,'young_edit_mcp_matches':len(third['mcp']),'numerical_age_records':len(third['numeric']),'numerical_field_assertions':sum(x['assertions'] for x in third['numeric']),'original_hash_checks':len(originals['checks']),'private_saved_fixtures':12,'private_breed_fixtures':6,'aligned_breed_equalities':len(first['relationships']),'saved_command_png_equalities':len(second['relationships'])},'saved_endpoints':saved_endpoints,'cross_version':cross,'cross_version_rgba_equal':sum(x['rgba_equal'] for x in cross),'manifests':{f'young-00{i}':digest((ROOT/f'experiments/young-00{i}.json').read_bytes()) for i in (1,2,3)},'scripts':{p:digest((ROOT/'tools'/p).read_bytes()) for p in ('young_breed_probe.py','young_saved_probe.py','young_layer_edits.py','young_sheets.py','check_young_session.py')},'http_health':'fresh discovery/capability and age12 Scottie render pass','originals':originals}
    record['renderer_source_count']=len(first['provenance']['sources'])
    record['replay_logs']={}
    for unit in ('young-001','young-002','young-003'):
        log=(ROOT/f'scratch/{unit}-verify.log').read_bytes()
        assert b'FULL REPLAY PASS' in log and b'Traceback' not in log,unit
        record['replay_logs'][unit]={'path':f'scratch/{unit}-verify.log','sha256':digest(log)}
    sheets=json.loads((OUT/'sheets.json').read_text())
    assert len(sheets)==4
    for sheet in sheets:assert digest((ROOT/sheet['path']).read_bytes())==sheet['sha256']
    record['reviewed_sheets']=sheets
    (ROOT/'experiments/young-session.json').write_text(json.dumps(record,indent=2)+'\n')
    (OUT/'audit.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ('counts','cross_version_rgba_equal','http_health')},indent=2))
if __name__=='__main__': asyncio.run(main())
