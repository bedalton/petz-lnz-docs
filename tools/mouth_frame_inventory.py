"""MOUTH-001: raw Petz4 frame tongue-size inventory (no behavior labels)."""
import dataclasses
import hashlib
import json
from pathlib import Path
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.animation import decode_bhd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/research/mouth-001'
def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=False)
    report={'experiment':'MOUTH-001','scope':'raw Petz4 BHD/BDT decode; no native behavior labels','species':[],
            'script_sha256':sha(Path(__file__).read_bytes())}
    for species,kind,tongue in [('Dogz','DOG',(63,64)),('Catz','CAT',(55,56))]:
        path=ROOT/f'games/petz4/Resource/{species} 4 Rez.dll'
        data=path.read_bytes();resources=ResourceFile(data)
        bhd=resources.read('BHD',kind);index=decode_bhd(bhd)
        rows=[];bdt_hashes={}
        for animation in range(len(index.animation_ends)):
            count=index.frame_count(animation)
            if not count:continue
            bdt=resources.read('BDT',f'{kind}{animation}')
            bdt_hashes[str(animation)]=sha(bdt)
            for frame in range(count):
                decoded=index.decode_frame(bdt,animation,frame)
                mods={m.ball_index:m.delta for m in decoded.size_mods}
                rows.append({'animation':animation,'frame':frame,'tag':decoded.tag,
                             'tongue_size_mods':[mods.get(i,0) for i in tongue],
                             'tongue_raw_xyz':[[decoded.balls[i].x,decoded.balls[i].y,decoded.balls[i].z] for i in tongue]})
        assert len(rows)==index.total_frames
        candidates=[r for r in rows if any(x>0 for x in r['tongue_size_mods'])]
        top=sorted(candidates,key=lambda r:(-sum(r['tongue_size_mods']),r['animation'],r['frame']))
        selected=[];seen=set()
        for r in top:
            if r['animation'] in seen:continue
            selected.append(r);seen.add(r['animation'])
            if len(selected)==12:break
        report['species'].append({'species':species,'kind':kind,'path':str(path.relative_to(ROOT)),
          'source_sha256':sha(data),'bhd_sha256':sha(bhd),'bdt_hashes':bdt_hashes,
          'tongue_ids':tongue,'tongue_bhd_sizes':[index.ball_sizes[i] for i in tongue],
          'animations':len(index.animation_ends),'frames':index.total_frames,
          'positive_mod_frames':len(candidates),'positive_mod_animations':len({r['animation'] for r in candidates}),
          'selected':selected,'frames_private':rows})
        print(species,index.total_frames,'frames;',len(candidates),'positive tongue modifiers;',selected[:2],flush=True)
        assert sha(path.read_bytes())==sha(data)
    (OUT/'inventory.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
