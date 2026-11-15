"""Independent retained-evidence audit for FACE-001; no original assets emitted."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()

def aligned_difference(folder,a,b):
    # Native-sized pixel dictionary in shared anchor coordinates, including alpha.
    def pixels(record):
        im=Image.open(folder/record['file']).convert('RGBA')
        ox,oy=record['meta']['offset']
        return {(x-ox,y-oy):rgba for (x,y),rgba in
                (((x,y),im.getpixel((x,y))) for y in range(im.height) for x in range(im.width)) if rgba[3]}
    left,right=pixels(a),pixels(b)
    return sum(left.get(p,(0,0,0,0))!=right.get(p,(0,0,0,0)) for p in left.keys()|right.keys())

def audit(folder,replay=None):
    report=json.loads((folder/'report.json').read_text())
    assert report['parse_checks']==1024
    assert report['script_sha256']==sha((ROOT/'tools/face_extension_probe.py').read_bytes())
    assert report['helper_sha256']==sha((ROOT/'tools/native_anatomy_probe.py').read_bytes())
    for path,digest in report['input_hashes'].items():assert sha((ROOT/path).read_bytes())==digest,path
    for path,digest in report['copy_hashes'].items():assert sha((ROOT/path).read_bytes())==digest,path
    for item in report['renders']+report['sheets']:assert sha((folder/item['file']).read_bytes())==item['sha256'],item['file']
    assert len(report['geometry'])==60 and len(report['renders'])==240 and len(report['sheets'])==12
    geometry=[]
    for r in report['geometry']:
        before,after=r['before'],r['after']
        changed=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b]
        assert changed==r['changed_geometry_ids']
        for a,b in zip(before,after):
            assert all(a[k]==b[k] for k in ('radius','visible','parked'))
        geometry.append({k:r[k] for k in ('breed','look','pose','variant','effective_face_extension','changed_geometry_ids')})
    groups={}
    for r in report['renders']:
        key=(r['breed'],r['look'],r['args']['pose'],r['args']['yaw_degrees'])
        groups.setdefault(key,{})[r['variant']]=r
    pairs=[]
    for key,variants in groups.items():
        for name,r in variants.items():
            n=aligned_difference(folder,variants['source'],r)
            assert (n>0)==r['differs_from_source']
            if name in ('source','roundtrip'):assert n==0
            pairs.append({'breed':key[0],'look':key[1],'pose':key[2],'yaw':key[3],'variant':name,'changed_rgba_pixels':n})
    replay_count=0
    if replay:
        other=json.loads((replay/'report.json').read_text())
        assert report['geometry']==other['geometry']
        assert report['runtime']==other['runtime']
        for a,b in zip(report['renders']+report['sheets'],other['renders']+other['sheets'],strict=True):
            assert a['file']==b['file'] and a['sha256']==b['sha256']
            assert sha((replay/b['file']).read_bytes())==a['sha256']
            replay_count+=1
    result={'report_sha256':sha((folder/'report.json').read_bytes()),'auditor_sha256':sha(Path(__file__).read_bytes()),
      'png_checks':252,'input_checks':len(report['input_hashes']),'copy_checks':len(report['copy_hashes']),
      'geometry':geometry,'rgba_comparisons':pairs,'replay_png_checks':replay_count}
    (folder/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 252 PNG hashes; 240 anchor-aligned RGBA comparisons; 60 geometry checks;',replay_count,'replay matches')
    for breed in ('labrador','siamese'):
        for v in ('face0','face-12','face12'):
            selected=[r for r in pairs if r['breed']==breed and r['variant']==v]
            print(breed,v,sum(r['changed_rgba_pixels']>0 for r in selected),'/',len(selected),'changed; range',min(r['changed_rgba_pixels'] for r in selected),max(r['changed_rgba_pixels'] for r in selected))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,default=ROOT/'scratch/research/face-001');p.add_argument('--replay',type=Path)
    a=p.parse_args();audit(a.folder,a.replay)
