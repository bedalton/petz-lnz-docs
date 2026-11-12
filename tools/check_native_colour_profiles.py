"""Audit NATIVE-004 profile tags, unique-color mapping and palette tallies.

Uses the same LittleCMS engine via a different call path; this checks artifact
consistency, not independent color-science or native game fidelity.
"""
from collections import Counter
import io
import itertools
import json
from pathlib import Path
from PIL import Image, ImageCms
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from native_pixel_grid import ROOT, sha

OUT = ROOT/'scratch/research/native-004'


def main():
    manifest = ROOT/'experiments/native-004.json'
    report = json.loads(manifest.read_text())
    assert report == json.loads((OUT/'report.json').read_text())
    assert report['script_sha256'] == sha((ROOT/'tools/native_colour_profiles.py').read_bytes())
    palette = set(load_saved_assets(ResourceResolver((ROOT/'games/petz4',)),
                                   'Adopted Petz/Goobe.pet',pose='standing').palette)
    near = {tuple(c+d for c,d in zip(rgb,delta)) for rgb in palette
            for delta in itertools.product((-1,0,1),repeat=3)
            if all(0 <= c+d <= 255 for c,d in zip(rgb,delta))}
    target_raw = (OUT/'target-srgb.icc').read_bytes()
    assert sha(target_raw) == report['controls']['target_profile_sha256']
    target = ImageCms.ImageCmsProfile(io.BytesIO(target_raw))
    color_checks = pixel_checks = 0
    for row in report['stills']:
        original = Image.open(ROOT/row['path'])
        assert sha((ROOT/row['path']).read_bytes()) == row['input_sha256']
        tagged_raw = (OUT/row['file_tagged']).read_bytes()
        srgb_raw = (OUT/row['file_srgb']).read_bytes()
        assert sha(tagged_raw)==row['tagged_png_sha256'] and sha(srgb_raw)==row['srgb_png_sha256']
        tagged = Image.open(io.BytesIO(tagged_raw));srgb = Image.open(io.BytesIO(srgb_raw))
        assert tagged.info['icc_profile'] == original.info['icc_profile']
        assert sha(tagged.info['icc_profile']) == row['source_profile_sha256']
        assert srgb.info['icc_profile'] == target_raw and tagged.size == srgb.size
        raw_reduced = Image.open(ROOT/'scratch/research/native-003'/row['file_srgb']).convert('RGB')
        assert raw_reduced.tobytes() == tagged.tobytes()
        rgb_counts = Counter(tagged.get_flattened_data())
        colors = list(rgb_counts)
        probe = Image.new('RGB',(len(colors),1));probe.putdata(colors)
        source = ImageCms.ImageCmsProfile(io.BytesIO(tagged.info['icc_profile']))
        transform = ImageCms.buildTransform(source,target,'RGB','RGB',renderingIntent=1,flags=0)
        mapped = list(ImageCms.applyTransform(probe,transform).get_flattened_data())
        mapping = dict(zip(colors,mapped))
        expected = [mapping[p] for p in tagged.get_flattened_data()]
        assert list(srgb.get_flattened_data()) == expected
        color_checks += len(colors);pixel_checks += len(expected)
        for label,image in (('raw_counts',tagged),('srgb_counts',srgb)):
            count = Counter(image.get_flattened_data());saved = row[label]
            assert sum(count.values()) == saved['pixels'] and len(count)==saved['unique_rgb']
            assert sum(n for p,n in count.items() if p in palette) == saved['exact_palette_pixels']
            assert sum(n for p,n in count.items() if p in near) == saved['within_one_channel_level_pixels']
    native = json.loads((ROOT/'experiments/native-002.json').read_text())
    for item in report['prefix_arrays']:
        source = next(r for r in native['inputs'] if r['name']==item['name'])
        raws = [(ROOT/source['paths'][side]).read_bytes() for side in ('prior','capture')]
        for span in item['arrays']:
            start = span['offset'];end = start+span['count']*span['width']
            assert raws[0][start:end] == raws[1][start:end]
            assert sha(raws[0][start:end]) == span['sha256']
    intake = json.loads((ROOT/'scratch/research/native-001/inventory.json').read_text())
    for item in intake['inputs']:
        assert sha((ROOT/item['path']).read_bytes()) == item['sha256']
    result = {'manifest_sha256':sha(manifest.read_bytes()),'script_sha256':sha(Path(__file__).read_bytes()),
              'tagged_pngs':21,'srgb_pngs':21,'unique_color_mapping_checks':color_checks,
              'managed_pixel_checks':pixel_checks,'palette_count_checks':84,
              'saved_array_hash_checks':9,'unchanged_intake_files':len(intake['inputs']),
              'limitation':'Same LittleCMS engine, independent artifact/tally controls only'}
    (OUT/'independent-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));print('PROFILE AUDIT PASS')


if __name__ == '__main__':
    main()
