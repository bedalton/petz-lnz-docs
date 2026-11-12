"""NATIVE-003: exact cropped replication grids; private lossless reductions.

This tests encoded RGB samples, not display DPI or the game's coordinate system.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import PIL
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/research/native-003'
MANIFEST = ROOT/'experiments/native-003.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def spans(length, factor, phase):
    starts = list(range(phase,length,factor))
    if phase:
        starts.insert(0,0)
    return starts, np.diff(starts+[length])


def test_grid(rgb, factor, phase_x, phase_y):
    ys, yr = spans(rgb.shape[0],factor,phase_y)
    xs, xr = spans(rgb.shape[1],factor,phase_x)
    latent = rgb[np.ix_(ys,xs)]
    rebuilt = np.repeat(np.repeat(latent,yr,axis=0),xr,axis=1)
    assert rebuilt.shape == rgb.shape
    mismatches = int(np.count_nonzero(np.any(rgb != rebuilt,axis=2)))
    return {'factor':factor,'phase_x':phase_x,'phase_y':phase_y,
            'mismatching_pixels':mismatches,'latent_dimensions':[len(xs),len(ys)]}, latent


def candidates(rgb, factors=(2,3,4)):
    return [test_grid(rgb,f,x,y)[0] for f in factors for y in range(f) for x in range(f)]


def synthetic_controls():
    y,x = np.indices((9,11))
    base = np.stack(((x*31+y*17)%256,(x*67+y*23)%256,(x*13+y*79)%256),axis=2).astype('uint8')
    doubled = np.repeat(np.repeat(base,2,axis=0),2,axis=1)
    results = []
    for left in (0,1):
        for top in (0,1):
            for right in (0,1):
                for bottom in (0,1):
                    crop = doubled[top:doubled.shape[0]-bottom,left:doubled.shape[1]-right]
                    exact = [r for r in candidates(crop,(2,)) if r['mismatching_pixels']==0]
                    assert len(exact)==1 and (exact[0]['phase_x'],exact[0]['phase_y'])==(left,top)
                    results.append({'case':'cropped-double','crop':[left,top,right,bottom],'exact':exact})
    corrupt = doubled.copy();corrupt[7,7,0] ^= 1
    bilinear = np.asarray(Image.fromarray(base).resize((22,18),Image.Resampling.BILINEAR))
    for label, rgb in (('one-channel-one-pixel-corruption',corrupt),('bilinear',bilinear)):
        exact = [r for r in candidates(rgb,(2,)) if r['mismatching_pixels']==0]
        assert not exact
        results.append({'case':label,'exact':exact})
    quadrupled = np.repeat(np.repeat(base,4,axis=0),4,axis=1)
    exact = [r for r in candidates(quadrupled,(2,4)) if r['mismatching_pixels']==0]
    assert {r['factor'] for r in exact} == {2,4}
    results.append({'case':'quadruple-is-also-double-compatible','exact':exact})
    return results


def run(verify):
    old = json.loads(MANIFEST.read_text()) if verify else None
    if not verify:
        OUT.mkdir(parents=True,exist_ok=False)
    intake_path = ROOT/'scratch/research/native-001/inventory.json'
    intake = json.loads(intake_path.read_text())
    report = {'experiment':'NATIVE-003','script_sha256':sha(Path(__file__).read_bytes()),
              'backend':'NumPy exact RGB grid reconstruction; Pillow PNG decoding/encoding; no renderer calls',
              'versions':{'numpy':np.__version__,'pillow':PIL.__version__},
              'intake_sha256':sha(intake_path.read_bytes()),
              'controls':synthetic_controls(),'stills':[],'video_samples':[],
              'scope':'Exact encoded raster replication only; no Mac DPI, engine resolution or renderer geometry claim'}
    for index,item in enumerate(r for r in intake['inputs'] if Path(r['path']).suffix.lower()=='.png'):
        path = ROOT/item['path'];raw = path.read_bytes()
        assert sha(raw) == item['sha256']
        rgb = np.asarray(Image.open(io.BytesIO(raw)).convert('RGB'))
        records = candidates(rgb)
        exact = [r for r in records if r['mismatching_pixels']==0]
        assert len(exact)==1 and exact[0]['factor']==2, (path,exact)
        selected = exact[0]
        _,latent = test_grid(rgb,2,selected['phase_x'],selected['phase_y'])
        buf = io.BytesIO();Image.fromarray(latent).save(buf,format='PNG');png = buf.getvalue()
        file = f'{index:02d}-{path.stem}.png'
        if verify:
            assert (OUT/file).read_bytes() == png
        else:
            (OUT/file).write_bytes(png)
        report['stills'].append({'path':item['path'],'input_sha256':sha(raw),
                                'dimensions':[rgb.shape[1],rgb.shape[0]],'candidates':records,
                                'selected':selected,'file':file,'png_sha256':sha(png)})
        assert path.read_bytes() == raw
    video = next(r for r in intake['inputs'] if 'video' in r)
    for item in video['video']['samples']:
        raw = (ROOT/item['path']).read_bytes();assert sha(raw)==item['sha256']
        rgb = np.asarray(Image.open(io.BytesIO(raw)).convert('RGB'))
        records = candidates(rgb,(2,))
        assert not any(r['mismatching_pixels']==0 for r in records)
        report['video_samples'].append({'frame_index':item['frame_index'],'path':item['path'],
                                        'input_sha256':sha(raw),'candidates':records})
    report['summary'] = {'stills':len(report['stills']),'exact_double_grids':len(report['stills']),
                         'still_candidate_grids':sum(len(r['candidates']) for r in report['stills']),
                         'video_frames_sampled':len(report['video_samples']),
                         'video_exact_double_grids':0,'synthetic_controls':len(report['controls'])}
    if verify:
        assert report == old
        print('FULL REPLAY PASS')
    else:
        for path in (MANIFEST,OUT/'report.json'):
            path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary'],indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser();parser.add_argument('--verify',action='store_true')
    run(parser.parse_args().verify)
