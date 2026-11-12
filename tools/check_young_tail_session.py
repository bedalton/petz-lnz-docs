"""YOUNG-008/009/010/011 integrity, field attribution and local HTTP audit."""
import asyncio,base64,json,subprocess,sys
from pathlib import Path
from fastmcp import Client
from young_breed_probe import ROOT,digest,provenance
from check_young_upgrade_session import independent_difference
async def run():
    out=ROOT/'scratch/research/young-tail-session';out.mkdir(parents=True,exist_ok=True)
    units=['young-008','young-009','young-010','young-011'];reports={u:json.loads((ROOT/f'experiments/{u}.json').read_text()) for u in units}
    source=provenance();files={};logs={};audits={}
    scripts=['young_tail_interactions.py','young_count_controls.py','young_tail_yaws.py','young_hidden_fields.py']
    for u,script in zip(units,scripts):
        report=reports[u];assert report['provenance']==source
        assert digest((ROOT/'tools'/script).read_bytes())==report['script_sha256']
        for row in report['renders']:
            p=ROOT/f'scratch/research/{u}'/row['file'];assert digest(p.read_bytes())==row['png_sha256'];files[str(p.relative_to(ROOT))]=row['png_sha256']
        log=ROOT/f'scratch/{u}-verify.log';assert 'FULL REPLAY PASS' in log.read_text();logs[str(log.relative_to(ROOT))]=digest(log.read_bytes())
        if u!='young-011':
            ap=ROOT/f'scratch/research/{u}/verification.json';audit=json.loads(ap.read_text())
            assert audit['manifest_sha256']==digest((ROOT/f'experiments/{u}.json').read_bytes())
            checker='check_young_tail.py' if u=='young-008' else 'check_young_tail_followups.py'
            assert audit['checker_sha256']==digest((ROOT/'tools'/checker).read_bytes())
            assert audit['sheet_sha256']==digest((ap.parent/('minimal-sheet.png' if u=='young-008' else 'control-sheet.png')).read_bytes())
            audits[u]=digest(ap.read_bytes())
    report=reports['young-011'];rows=report['renders'];prior=reports['young-010'];checks=0;links=0
    assert report['prior_manifest_sha256']==digest((ROOT/'experiments/young-010.json').read_bytes())
    for row in rows:
        key=tuple(row[k] for k in ('mode','pose','yaw'));base=ROOT/'scratch/research/young-011'
        target=next(r for r in rows if tuple(r[k] for k in ('mode','pose','yaw'))==key and r['label']=='none')
        n=independent_difference(base/row['file'],row['offset'],base/target['file'],target['offset']);checks+=1
        assert n==row['pixels_vs_full'] and row['ball93_visible']
        if row['label']=='body_area':
            assert n==0 and row['geometry_equal_full'] and row['fills_equal_full'] and row['commands_equal_full']
        if row['label']=='x':
            both=next(r for r in rows if tuple(r[k] for k in ('mode','pose','yaw'))==key and r['label']=='both')
            assert independent_difference(base/row['file'],row['offset'],base/both['file'],both['offset'])==0;checks+=1
        if row['label'] in ('none','both'):
            label='unomit-full' if row['label']=='none' else 'unomit-revert26'
            old=next(r for r in prior['renders'] if tuple(r[k] for k in ('mode','pose','yaw'))==key and r['label']==label)
            assert row['png_sha256']==old['png_sha256'];links+=1
    # Remove later area passes to isolate authored-zero base inheritance.
    from dataclasses import replace
    from petz_renderer.formats.resolver import ResourceResolver
    from petz_renderer.local import load_saved_assets
    from petz_renderer.appearance.evaluation import body_areas
    from young_endpoint_fields import FACTORS,modify
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'));area_controls=[]
    for mode in ('missing-adult','missing-young'):
        v=report['inputs']['variants'][mode]
        a=load_saved_assets(resolver,v['path'],look='age',age=12)
        b=load_saved_assets(resolver,v['path'],look='puppy',age=12)
        full=modify(a.appearance,b.appearance,FACTORS);full=replace(full,omissions=full.omissions-{93})
        assert full.add_balls[26].base==52
        for authored in (0,8):
            adds=list(full.add_balls);adds[26]=replace(adds[26],body_area=authored)
            for control in ('original','no-lists','no-links','no-lists-links'):
                ap=replace(full,add_balls=tuple(adds))
                if 'lists' in control:ap=replace(ap,body_area_lists=tuple(() for _ in ap.body_area_lists))
                if 'links' in control:ap=replace(ap,lines=(),whiskers=())
                areas=body_areas(ap)
                assert areas[52]==areas[93]==8
                area_controls.append({'mode':mode,'authored':authored,'control':control,'base52_area':areas[52],'ball93_area':areas[93]})
    original=json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True));assert len(original['checks'])==21 and all(r['ok'] for r in original['checks'])
    http=[]
    async with Client('http://127.0.0.1:8765/mcp') as client:
        assert len(await client.list_tools())==6
        cap=await client.call_tool('get_capabilities');assert not cap.is_error
        for row in reports['young-010']['mcp']:
            response=await client.call_tool('render_pet',row['controls']);assert not response.is_error
            png=base64.b64decode(next(c.data for c in response.content if c.type=='image'));assert digest(png)==row['png_sha256'];http.append(row)
    result={'provenance':source,'manifests':{u:digest((ROOT/f'experiments/{u}.json').read_bytes()) for u in units},
            'scripts':{p:digest((ROOT/'tools'/p).read_bytes()) for p in scripts+['check_young_tail.py','check_young_tail_followups.py','check_young_tail_session.py']},
            'saved_pngs':files,'replay_logs':logs,'unit_audits':audits,'field_independent_rgba_checks':checks,
            'field_prior_links':links,'area_controls':area_controls,'originals':original,'http_matches':http,
            'summary':{'numerical_area_controls':len(area_controls),'research_pngs':len(files),'research_mcp_matches':18,'total_independent_rgba_comparisons':1536+816+720+checks,'factor_signature_pairs':5376,'prior_links':36+links,'originals':21,'installed_sources':len(source['sources'])}}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['summary'],indent=2));print('SESSION AUDIT PASS')
if __name__=='__main__':asyncio.run(run())
