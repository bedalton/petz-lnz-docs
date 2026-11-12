"""Inventory user game captures without changing inputs.

Run with the renderer Python; optional PyAV is needed for video inspection.
All derived media and manifests remain private under scratch.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image
from petz_renderer.formats.pet import read_saved_appearance

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/research/native-001'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for p in sorted((ROOT / 'scratch/screenshots').rglob('*')):
        if p.suffix.lower() not in ('.png', '.pet', '.mov'):
            continue
        r = {'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size, 'sha256': sha(p)}
        if p.suffix.lower() == '.png':
            im = Image.open(p).convert('RGB')
            r['dimensions'] = im.size
            # Exact repeated pairs are diagnostic only: crops can start at either phase.
            import PIL
            r['pillow'] = PIL.__version__
            r['equal_adjacent_fraction'] = {
                'horizontal': sum(a == b for a,b in zip(im.crop((0,0,im.width-1,im.height)).getdata(), im.crop((1,0,im.width,im.height)).getdata())) / ((im.width-1)*im.height),
                'vertical': sum(a == b for a,b in zip(im.crop((0,0,im.width,im.height-1)).getdata(), im.crop((0,1,im.width,im.height)).getdata())) / (im.width*(im.height-1))}
        elif p.suffix.lower() == '.pet':
            pet = read_saved_appearance(p.read_bytes())
            r.update(name=pet.name, breed=pet.breed_name, saved_age_field=pet.biorhythms[8],
                     age_interpretation='Renderer uses biorhythms[8]; not independently game-validated chronological age')
            prior = ROOT / 'games/petz4/Adopted Petz' / (pet.name + '.pet')
            if prior.exists():
                old = read_saved_appearance(prior.read_bytes())
                r['prior'] = {'path':str(prior.relative_to(ROOT)), 'sha256':sha(prior), 'same_file':sha(prior)==r['sha256'],
                              'adult_cache_equal':old.adult_cache==pet.adult_cache,
                              'young_cache_equal':old.young_cache==pet.young_cache,
                              'saved_age_field':old.biorhythms[8]}
        else:
            import av
            c = av.open(str(p)); s = c.streams.video[0]
            r['video'] = {'backend':'PyAV', 'version':av.__version__, 'libraries':av.library_versions,
                          'dimensions':[s.width,s.height], 'duration_seconds':float(s.duration*s.time_base),
                          'average_rate':str(s.average_rate), 'codec':s.codec_context.name}
            frames = list(c.decode(video=0))
            r['video']['decoded_frames'] = len(frames)
            r['video']['samples'] = []
            for i in sorted({round(j*(len(frames)-1)/11) for j in range(12)}):
                f=frames[i]; target=OUT / f'video-{i:03d}.png';f.to_image().save(target)
                r['video']['samples'].append({'frame_index':i,'seconds':f.time,'path':str(target.relative_to(ROOT)),'sha256':sha(target)})
        records.append(r)
    result={'inputs':records,'controls':'Read-only originals; no renderer comparison, resize or age override performed.'}
    (OUT/'inventory.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'files':len(records),'counts':{s:sum(Path(r['path']).suffix==s for r in records) for s in ('.png','.pet','.mov')},
                      'pets':[r for r in records if 'name' in r]},indent=2))

if __name__ == '__main__':
    main()
