"""Independent geometry/RGBA evidence audit for MOUTH-002."""
import argparse,hashlib,json
from pathlib import Path
from check_face_extension import aligned_difference
ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
EXPECTED={'source':set(),'roundtrip':set(),'cheek_x':{78,79},'lip_jowl_x':{80,81,91,92},'lower_y':{88,89,90,91,92},'tongue_relative0':{77}}

def main(folder,replay):
    r=json.loads((folder/'report.json').read_text())
    assert r['script_sha256']==sha((ROOT/'tools/mouth_detail_probe.py').read_bytes())
    assert len(r['geometry'])==60 and len(r['renders'])==120 and len(r['sheets'])==10 and r['parse_checks']==512
    for p,h in {**r['input_hashes'],**r['copy_hashes']}.items():assert sha((ROOT/p).read_bytes())==h,p
    for x in r['renders']+r['sheets']:assert sha((folder/x['file']).read_bytes())==x['sha256']
    summaries=[]
    for x in r['geometry']:
        changed={i for i,(a,b) in enumerate(zip(x['before'],x['after'])) if a!=b}
        assert changed==set(x['changed_geometry_ids']) and changed<=EXPECTED[x['variant']]
        assert all((a['visible'],a['parked'])==(b['visible'],b['parked']) for a,b in zip(x['before'],x['after']))
        if x['variant']=='tongue_relative0':
            assert x['after'][77]['radius']==x['after'][63]['radius']
            assert all(a==b for i,(a,b) in enumerate(zip(x['before'],x['after'])) if i!=77)
            if x['state'] in ('standing','sitting','lying'):assert x['before'][77]['radius']==x['after'][77]['radius']==0
        else:assert all(a['radius']==b['radius'] for a,b in zip(x['before'],x['after']))
        summaries.append({**{k:x[k] for k in ('look','state','variant','changed_geometry_ids')},'tongue_before_radius':x['before'][77]['radius'],'tongue_after_radius':x['after'][77]['radius']})
    groups={}
    for x in r['renders']:groups.setdefault((x['look'],x['state'],x['args']['yaw_degrees']),{})[x['variant']]=x
    pairs=[]
    for key,variants in groups.items():
        for name,x in variants.items():
            n=aligned_difference(folder,variants['source'],x);assert (n>0)==x['differs_from_source']
            if name in ('source','roundtrip'):assert n==0
            pairs.append({'look':key[0],'state':key[1],'yaw':key[2],'variant':name,'changed_rgba_pixels':n})
    replay_matches=0
    if replay:
        other=json.loads((replay/'report.json').read_text());assert r['geometry']==other['geometry']
        for a,b in zip(r['renders']+r['sheets'],other['renders']+other['sheets'],strict=True):
            assert a['file']==b['file'] and a['sha256']==b['sha256']==sha((replay/b['file']).read_bytes());replay_matches+=1
    v={'report_sha256':sha((folder/'report.json').read_bytes()),'auditor_sha256':sha(Path(__file__).read_bytes()),'png_checks':130,'input_checks':len(r['input_hashes']),'copy_checks':len(r['copy_hashes']),'geometry':summaries,'rgba_comparisons':pairs,'replay_png_matches':replay_matches}
    (folder/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
    print('PASS 130 PNG hashes;120 anchor-aligned pairs;60 geometry records;',replay_matches,'replay PNG matches')
    for variant in ('cheek_x','lip_jowl_x','lower_y','tongue_relative0'):
        selected=[x for x in pairs if x['variant']==variant]
        print(variant,sum(x['changed_rgba_pixels']>0 for x in selected),'/',len(selected),'changed')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,default=ROOT/'scratch/research/mouth-002');p.add_argument('--replay',type=Path)
    args=p.parse_args();main(args.folder,args.replay)
