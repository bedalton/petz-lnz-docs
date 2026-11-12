"""NATIVE-004: preserve embedded display profiles in qualitative comparisons."""
import argparse
from collections import Counter
import io
import json
from pathlib import Path

import PIL
from PIL import Image, ImageCms, ImageDraw
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from native_pixel_grid import ROOT, sha, spans
from saved_colour_arrays import arrays

OUT = ROOT/'scratch/research/native-004'
MANIFEST = ROOT/'experiments/native-004.json'


def png_bytes(im, profile):
    buf = io.BytesIO();im.save(buf,format='PNG',icc_profile=profile);return buf.getvalue()


def put(path, raw, verify):
    if verify:
        assert path.read_bytes() == raw, path
    else:
        path.write_bytes(raw)


def counts(im, palette):
    colors = Counter(im.get_flattened_data())
    errors = {rgb:min(max(abs(a-b) for a,b in zip(rgb,p)) for p in palette) for rgb in colors}
    return {'pixels':sum(colors.values()),'unique_rgb':len(colors),
            'exact_palette_pixels':sum(n for rgb,n in colors.items() if errors[rgb]==0),
            'within_one_channel_level_pixels':sum(n for rgb,n in colors.items() if errors[rgb]<=1),
            'max_nearest_palette_channel_error':max(errors.values())}


def reduce_grid(im, selected):
    xs,_ = spans(im.width,2,selected['phase_x']);ys,_ = spans(im.height,2,selected['phase_y'])
    out = Image.new('RGB',(len(xs),len(ys)))
    out.putdata([im.getpixel((x,y)) for y in ys for x in xs])
    return out


def save_sheet(report, profile):
    # Same encoded sample scale for stills; no geometric registration or resize.
    labels = [('Goobe current','11-'),('Goobe historical','15-'),('Homebody','03-')]
    canvas = Image.new('RGB',(660,690),'#dedede');draw = ImageDraw.Draw(canvas)
    for row,(label,prefix) in enumerate(labels):
        source = next(r for r in report['stills'] if Path(r['file_srgb']).name.startswith(prefix))
        im = Image.open(OUT/source['file_srgb']).convert('RGB')
        canvas.paste(im,(10,row*230+25));draw.text((10,row*230+5),label+' / profile converted',fill='black')
        name = 'Homebody' if label=='Homebody' else 'Goobe'
        control = 'capture' if label!='Goobe historical' else 'prior'
        side = 1 if control=='capture' else 0
        im = Image.open(ROOT/f'scratch/research/native-002/{name}-{control}-standing-0-a{side}-f{side}.png').convert('RGBA')
        canvas.paste(im,(300,row*230+25),im)
        draw.text((300,row*230+5),'Renderer stock standing (unregistered)',fill='black')
    canvas.save(OUT/'qualitative-sheet.png',icc_profile=profile)


def run(verify):
    old = json.loads(MANIFEST.read_text()) if verify else None
    if not verify:
        OUT.mkdir(parents=True,exist_ok=False)
        # Capture this generated profile once; ICC creation timestamps may vary.
        (OUT/'target-srgb.icc').write_bytes(ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
    target_raw = (OUT/'target-srgb.icc').read_bytes()
    target = ImageCms.ImageCmsProfile(io.BytesIO(target_raw))
    gridpath = ROOT/'experiments/native-003.json';grid = json.loads(gridpath.read_text())
    resolver = ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/screenshots'))
    assets = load_saved_assets(resolver,'Adopted Petz/Goobe.pet',pose='standing')
    palette = assets.palette
    reference = ROOT/'experiments/native-002.json'
    report = {'experiment':'NATIVE-004','script_sha256':sha(Path(__file__).read_bytes()),
              'renderer_reference':{'manifest_sha256':sha(reference.read_bytes()),
                                    'revision':json.loads(reference.read_text())['provenance']['revision']},
              'grid_manifest_sha256':sha(gridpath.read_bytes()),
              'backend':'Pillow ImageCms / LittleCMS; local renderer palette inspection only',
              'versions':{'pillow':PIL.__version__,'littlecms':ImageCms.core.littlecms_version},
              'controls':{'intent':int(ImageCms.Intent.RELATIVE_COLORIMETRIC),'flags':0,
                          'target_profile_sha256':sha(target_raw),
                          'palette_sha256':sha(bytes(c for p in palette for c in p)),
                          'renderer_rgb_assumption':'Treat untagged preview RGB as sRGB for qualitative display; no native color-fidelity claim'},
              'stills':[],'prefix_arrays':[]}
    for row in grid['stills']:
        path = ROOT/row['path'];raw = path.read_bytes();assert sha(raw)==row['input_sha256']
        original = Image.open(io.BytesIO(raw))
        assert original.mode in ('RGB','RGBA')
        if original.mode == 'RGBA':
            assert original.getchannel('A').getextrema() == (255,255)
        profile_raw = original.info['icc_profile']
        profile = ImageCms.ImageCmsProfile(io.BytesIO(profile_raw))
        rgb = original.convert('RGB');reduced = reduce_grid(rgb,row['selected'])
        prior = Image.open(ROOT/'scratch/research/native-003'/row['file']).convert('RGB')
        assert reduced.tobytes() == prior.tobytes()
        srgb = ImageCms.profileToProfile(rgb,profile,target,renderingIntent=1,outputMode='RGB',flags=0)
        managed_reduced = reduce_grid(srgb,row['selected'])
        independent_order = ImageCms.profileToProfile(reduced,profile,target,renderingIntent=1,outputMode='RGB',flags=0)
        assert managed_reduced.tobytes() == independent_order.tobytes()
        # Same-profile transform is a no-op control for this RGB input.
        identity = ImageCms.profileToProfile(reduced,profile,profile,renderingIntent=1,outputMode='RGB',flags=0)
        assert identity.tobytes() == reduced.tobytes()
        tagged_file = 'tagged-'+row['file'];srgb_file = row['file']
        tagged = png_bytes(reduced,profile_raw);managed = png_bytes(managed_reduced,target_raw)
        put(OUT/tagged_file,tagged,verify);put(OUT/srgb_file,managed,verify)
        record = {'path':row['path'],'input_sha256':sha(raw),
                  'source_profile_sha256':sha(profile_raw),'source_profile_bytes':len(profile_raw),
                  'source_profile_name':ImageCms.getProfileName(profile).strip(),
                  'source_mode':original.mode,
                  'dpi_metadata':original.info.get('dpi'),
                  'file_tagged':tagged_file,'tagged_png_sha256':sha(tagged),
                  'file_srgb':srgb_file,'srgb_png_sha256':sha(managed),
                  'raw_counts':counts(reduced,palette),'srgb_counts':counts(managed_reduced,palette),
                  'conversion_commutes_with_reduction':True,'same_profile_identity':True}
        report['stills'].append(record)
        assert path.read_bytes() == raw
    # These bounded prefix arrays are ignored by the renderer's appearance parser;
    # compare bytes, without attributing any native color effect to them.
    for name,capture in [('Goobe','dogz/great-dane/Goobe--2026-11-12-645.pet'),
                         ('Fuzzkin','Fuzzkin-walkaround.pet'),('Homebody','catz/Homebody.pet')]:
        a = (ROOT/f'games/petz4/Adopted Petz/{name}.pet').read_bytes()
        b = (ROOT/'scratch/screenshots'/capture).read_bytes()
        aa,bb = arrays(a),arrays(b)
        assert aa == bb
        report['prefix_arrays'].append({'name':name,'prior_sha256':sha(a),'capture_sha256':sha(b),
                                       'arrays':aa,'equal':True})
    report['summary'] = {'stills':len(report['stills']),'source_profile_counts':dict(Counter(r['source_profile_sha256'] for r in report['stills'])),
                         'tagged_copies':21,'srgb_copies':21,'same_profile_controls':21,
                         'conversion_order_controls':21,'equal_saved_prefix_arrays':9,
                         'raw_exact_palette_pixels':sum(r['raw_counts']['exact_palette_pixels'] for r in report['stills']),
                         'srgb_exact_palette_pixels':sum(r['srgb_counts']['exact_palette_pixels'] for r in report['stills']),
                         'pixels':sum(r['raw_counts']['pixels'] for r in report['stills'])}
    report = json.loads(json.dumps(report))
    if verify:
        assert report == old
        print('FULL REPLAY PASS')
    else:
        for path in (MANIFEST,OUT/'report.json'):
            path.write_text(json.dumps(report,indent=2)+'\n')
        save_sheet(report,target_raw)
    print(json.dumps(report['summary'],indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser();parser.add_argument('--verify',action='store_true')
    run(parser.parse_args().verify)
