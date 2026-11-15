"""Independent retained-evidence checks for FACE-002."""
import hashlib,json
from pathlib import Path
from PIL import Image
from check_face_extension import aligned_difference
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/research/face-002'
def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    r=json.loads((OUT/'report.json').read_text())
    assert len(r['geometry'])==1080 and len(r['renders'])==540 and r['parse_checks']==3072
    assert r['script_sha256']==sha((ROOT/'tools/face_extension_versions.py').read_bytes())
    assert r['helper_sha256']==sha((ROOT/'tools/face_extension_probe.py').read_bytes())
    for p,h in {**r['input_hashes'],**r['copy_hashes']}.items():assert sha((ROOT/p).read_bytes())==h,p
    for x in r['renders']:assert sha((OUT/x['file']).read_bytes())==x['sha256']
    geometry={(x['version'],x['species'],x['look'],x['age'],x['pose'],x['variant']):x for x in r['geometry']}
    endpoints=[]
    for version in ('petz3','petz4','petz5'):
        for species,young in [('Dogz','puppy'),('Catz','kitten')]:
            for pose in ('standing','sitting','lying'):
                for variant in ('source','roundtrip','face0','face-12','face12'):
                    for age,look in [(12,young),(100,'adult')]:
                        a=geometry[version,species,'age',age,pose,variant]
                        b=geometry[version,species,look,age,pose,variant]
                        assert a['geometry']==b['geometry']
                        assert a['effective_face_extension']==b['effective_face_extension']
                        endpoints.append({'version':version,'species':species,'pose':pose,'variant':variant,'age':age,'matches_forced':True})
    shrink=[]
    for x in r['geometry']:
        if x['look']!='age' or x['age']!=0:continue
        young='puppy' if x['species']=='Dogz' else 'kitten'
        b=geometry[x['version'],x['species'],young,0,x['pose'],x['variant']]
        assert x['effective_face_extension']==b['effective_face_extension']
        assert x['geometry']!=b['geometry']
        shrink.append({'version':x['version'],'species':x['species'],'pose':x['pose'],'variant':x['variant'],'face_matches_forced_young':True,'geometry_differs':True})
    cross_geometry=[]
    for x in r['geometry']:
        if x['version']=='petz4':continue
        baseline=geometry['petz4',x['species'],x['look'],x['age'],x['pose'],x['variant']]
        cross_geometry.append({'version':x['version'],'species':x['species'],'look':x['look'],'age':x['age'],'pose':x['pose'],'variant':x['variant'],
          'geometry_matches_petz4':x['geometry']==baseline['geometry'],
          'face_matches_petz4':x['effective_face_extension']==baseline['effective_face_extension']})
    groups={}
    for x in r['renders']:groups.setdefault((x['version'],x['species'],x['look'],x['args']['pose'],x['args']['yaw_degrees']),{})[x['variant']]=x
    pairs=[]
    for key,variants in groups.items():
        for name,x in variants.items():
            n=aligned_difference(OUT,variants['source'],x)
            assert (n>0)==x['differs_from_source']
            if name in ('source','roundtrip'):assert n==0
            pairs.append({'version':key[0],'species':key[1],'look':key[2],'pose':key[3],'yaw':key[4],'variant':name,'changed_rgba_pixels':n})
    render_map={(x['version'],x['species'],x['look'],x['args']['pose'],x['args']['yaw_degrees'],x['variant']):x for x in r['renders']}
    cross_png=[]
    for x in r['renders']:
        if x['version']=='petz4':continue
        b=render_map['petz4',x['species'],x['look'],x['args']['pose'],x['args']['yaw_degrees'],x['variant']]
        # Compare anchor-aligned RGBA, not merely encoded PNG bytes.
        n=aligned_difference(OUT,b,x)
        cross_png.append({'file':x['file'],'petz4_file':b['file'],'changed_rgba_pixels':n})
    v={'report_sha256':sha((OUT/'report.json').read_bytes()),'auditor_sha256':sha(Path(__file__).read_bytes()),
       'png_checks':540,'input_checks':len(r['input_hashes']),'copy_checks':len(r['copy_hashes']),
       'age_endpoint_checks':endpoints,'age_zero_shrink_controls':shrink,'cross_version_geometry':cross_geometry,'rgba_comparisons':pairs,'cross_version_rgba':cross_png}
    (OUT/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
    print('PASS 540 PNG hashes,540 source RGBA pairs,360 cross-version RGBA pairs,720 cross-version geometry records,180 age endpoints,90 age0 shrink controls')
    print('cross geometry matches:',sum(x['geometry_matches_petz4'] for x in cross_geometry),'/',len(cross_geometry))
    print('cross RGBA matches:',sum(x['changed_rgba_pixels']==0 for x in cross_png),'/',len(cross_png))

if __name__=='__main__':main()
