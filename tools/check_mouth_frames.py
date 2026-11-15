"""Audit MOUTH-001 inventory, PNGs, tongue states and direct/MCP evidence."""
import hashlib,json,struct
from petz_renderer.formats.pe import ResourceFile
from pathlib import Path
from check_face_extension import aligned_difference
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/research/mouth-001'
def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    inventory=json.loads((OUT/'inventory.json').read_text());folder=OUT/'renders';r=json.loads((folder/'report.json').read_text())
    assert inventory['script_sha256']==sha((ROOT/'tools/mouth_frame_inventory.py').read_bytes())
    assert r['script_sha256']==sha((ROOT/'tools/mouth_frame_probe.py').read_bytes())
    assert r['inventory_sha256']==sha((OUT/'inventory.json').read_bytes())
    assert len(r['geometry'])==144 and len(r['renders'])==288 and len(r['sheets'])==8
    for p,h in {**r['input_hashes'],**r['copy_hashes']}.items():assert sha((ROOT/p).read_bytes())==h,p
    inventory_summary=[]
    for item in inventory['species']:
        assert sha((ROOT/item['path']).read_bytes())==item['source_sha256']
        rows=item['frames_private'];assert len(rows)==item['frames']
        # Re-read original BHD/BDT independently of decode_bhd/decode_frame.
        pe=ResourceFile((ROOT/item['path']).read_bytes());bhd=pe.read('BHD',item['kind'])
        table=struct.unpack_from('<H',bhd,0)[0];balls=struct.unpack_from('<H',bhd,6)[0]
        animations=struct.unpack_from('<H',bhd,172)[0]
        ends=struct.unpack_from(f'<{animations}H',bhd,174);cache={}
        assert balls==67 and ends[-1]==len(rows)
        for row in rows:
            animation,frame=row['animation'],row['frame']
            if animation not in cache:cache[animation]=pe.read('BDT',f'{item["kind"]}{animation}')
            data=cache[animation];start=ends[animation-1] if animation else 0
            offset=struct.unpack_from('<I',bhd,table+4*(start+frame))[0]
            mod_offset=offset+14+10*balls;count=struct.unpack_from('<H',data,mod_offset)[0]
            mods=dict(struct.unpack_from('<hh',data,mod_offset+2+4*i) for i in range(count))
            assert row['tongue_size_mods']==[mods.get(i,0) for i in item['tongue_ids']]
            assert row['tongue_raw_xyz']==[list(struct.unpack_from('<3h',data,offset+14+10*i)) for i in item['tongue_ids']]
            assert row['tag']==struct.unpack_from('<H',data,offset+12)[0]
        assert item['bdt_hashes']=={str(k):sha(v) for k,v in cache.items()}
        positive=[x for x in rows if any(v>0 for v in x['tongue_size_mods'])]
        assert len(positive)==item['positive_mod_frames']
        assert len({x['animation'] for x in positive})==item['positive_mod_animations']
        selected=[];seen=set()
        for x in sorted(positive,key=lambda x:(-sum(x['tongue_size_mods']),x['animation'],x['frame'])):
            if x['animation'] in seen:continue
            selected.append(x);seen.add(x['animation'])
            if len(selected)==12:break
        assert selected==item['selected']
        inventory_summary.append({k:item[k] for k in ('species','animations','frames','positive_mod_frames','positive_mod_animations','tongue_bhd_sizes')})
    for x in r['geometry']:
        for t in x['tongue']:
            assert all(t['before'][k]==t['after'][k] for k in ('radius','visible','parked'))
    for x in r['renders']+r['sheets']:assert sha((folder/x['file']).read_bytes())==x['sha256']
    assert all(x['matches_fresh_direct'] for x in r['renders'])
    groups={}
    for x in r['renders']:groups.setdefault((x['breed'],x['look'],x['args']['animation'],x['args']['frame'],x['args']['yaw_degrees']),{})[x['variant']]=x
    pairs=[]
    for key,variants in groups.items():
        for name in ('face-12','face12'):
            n=aligned_difference(folder,variants['source'],variants[name])
            pairs.append({'breed':key[0],'look':key[1],'animation':key[2],'frame':key[3],'yaw':key[4],'variant':name,'changed_rgba_pixels':n})
    verification={'inventory_sha256':sha((OUT/'inventory.json').read_bytes()),'report_sha256':sha((folder/'report.json').read_bytes()),
      'auditor_sha256':sha(Path(__file__).read_bytes()),'png_checks':296,'inventory':inventory_summary,'rgba_comparisons':pairs,
      'geometry_records':144,'mcp_direct_matches':288,
      'tongue_radius_range':{breed:{str(i):[min(t['after']['radius'] for x in r['geometry'] if x['breed']==breed for t in x['tongue'] if t['id']==i),max(t['after']['radius'] for x in r['geometry'] if x['breed']==breed for t in x['tongue'] if t['id']==i)] for i in ids} for breed,ids in [('labrador',(63,64,77)),('siamese',(55,56))]}}
    (OUT/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    print('PASS inventory 29,497 frames;296 PNGs;192 aligned face comparisons;144 tongue records;288 recorded exact direct/MCP matches')
    print(json.dumps(verification['tongue_radius_range']))

if __name__=='__main__':main()
