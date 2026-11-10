"""Aggregate PAINT-001/002/003 integrity after their complete unit replays."""
import json
from pathlib import Path
import subprocess
import petz_renderer
from PIL import Image
from research_common import ROOT,SHA


def main():
    revision=subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip()
    reports={};pngs=0
    for unit,count in (('paint-001',348),('paint-002',144),('paint-003',168)):
        folder=ROOT/'scratch/research'/unit;path=ROOT/'experiments'/(unit+'.json')
        r=json.loads(path.read_text());v=json.loads((folder/'verification.json').read_text())
        assert r==json.loads((folder/'report.json').read_text())
        assert v['report_sha256']==SHA(path.read_bytes())
        assert r['renderer_revision']==revision
        assert len(list(folder.rglob('*.png')))==count;pngs+=count
        checked=set()
        for c in r['cases']:
            for o in c['outputs'].values():
                p=folder/c['folder']/o['png']
                assert SHA(p.read_bytes())==o['png_sha256'];checked.add(p)
            if unit=='paint-001':
                assert SHA((folder/c['folder']/'states.json').read_bytes())==c['private_states_sha256']
        for b in r.get('baselines',[]):
            p=folder/(b['stem']+'.png')
            assert SHA(p.read_bytes())==b['png_sha256'];checked.add(p)
        assert len(checked)==count
        for name,digest in r['source_hashes'].items():
            assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes())==digest
            assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==digest
        reports[unit]={'manifest_sha256':SHA(path.read_bytes()),'verification_sha256':SHA((folder/'verification.json').read_bytes())}
    restore=json.loads((ROOT/'experiments/restore-002.json').read_text());originals={}
    for version,engines in restore['shared_engine_hashes'].items():
        paths={str(p.relative_to(ROOT/'games'/version)).lower():p for p in (ROOT/'games'/version).rglob('*') if p.is_file()}
        for name,digest in engines.items():
            assert SHA(paths[name].read_bytes())==digest;originals[f'{version}/{name}']=digest
    for r in restore['results']:
        p=ROOT/'games'/r['version']/r['path'];assert SHA(p.read_bytes())==r['input_sha256'];originals[str(p.relative_to(ROOT))]=r['input_sha256']
    prior=json.loads((ROOT/'experiments/paint-001.json').read_text())
    for c in prior['cases']:
        p=ROOT/'games/petz4'/c['path'];assert SHA(p.read_bytes())==c['input_sha256'];originals[str(p.relative_to(ROOT))]=c['input_sha256']
    assert len(originals)==20 and pngs==660
    # Independently check displayed RGBA differences, not only indexed buffers.
    def rgba(path):
        with Image.open(path) as im:
            raw=im.convert('RGBA').tobytes()
            return tuple(raw[i:i+4] for i in range(0,len(raw),4))
    def differences(a,b):
        assert len(a)==len(b)
        return sum(x!=y for x,y in zip(a,b,strict=True))
    rgba_checks=0;rgba_count_corrections=[]
    for unit in ('paint-001','paint-002','paint-003'):
        r=json.loads((ROOT/'experiments'/(unit+'.json')).read_text())
        for c in r['cases']:
            folder=ROOT/'scratch/research'/unit/c['folder']
            images={name:rgba(folder/o['png']) for name,o in c['outputs'].items()}
            for name,o in c['outputs'].items():
                refs=(('fresh','changed_from_fresh'),) if unit=='paint-001' else (('combined','changed_from_combined'),('host','remaining_from_host' if unit=='paint-002' else 'changed_from_host'))
                for reference,key in refs:
                    displayed=differences(images[name],images[reference])
                    if displayed!=o[key]:
                        rgba_count_corrections.append({'unit':unit,'case':c['folder'],'component':name,
                            'reference':reference,'indexed_changes':o[key],'rgba_changes':displayed})
                    rgba_checks+=1
    assert rgba_count_corrections==[
        {'unit':'paint-001','case':'Fuzzkin-sitting-90-yaw_arc','component':'geometry_only','reference':'fresh','indexed_changes':146,'rgba_changes':144},
        {'unit':'paint-001','case':'Fuzzkin-sitting-90-yaw_arc','component':'order_only','reference':'fresh','indexed_changes':116,'rgba_changes':114}]
    health_path=ROOT/'scratch/research/paint-session-health.json'
    health=json.loads(health_path.read_text());assert len(health['tools'])==6
    scripts=('saved_paint_motion.py','check_saved_paint_motion.py','paint_angle_attribution.py',
             'check_paint_angle_attribution.py','paint_state_shape.py','check_paint_state_shape.py','check_paint_session.py')
    tools={p:SHA((ROOT/'tools'/p).read_bytes()) for p in scripts}
    review={p.name:SHA(p.read_bytes()) for p in (ROOT/'scratch/research/paint-session-review').glob('*.png')}
    assert len(review)==2
    result={'renderer_revision':revision,'reports':reports,'research_pngs':pngs,'review_sheets':review,
        'original_hash_links':originals,'source_files_per_unit':62,'tool_hashes':tools,
        'health_sha256':SHA(health_path.read_bytes()),'new_mcp_baselines':12,'saved_pets':2,
        'persisted_motion_transitions':192,'final_direct_draws':648,'cross_unit_pixel_links':96,
        'decoded_rgba_difference_checks':rgba_checks,
        'rgba_count_corrections':rgba_count_corrections,
        'scope':'Integrity aggregation; unit verifiers execute the state/pixel replays.'}
    (ROOT/'scratch/research/paint-session-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('original_hash_links','tool_hashes','reports')}))


if __name__=='__main__':main()
