"""Independently decode NATIVE-002 PNGs and audit source/control comparisons."""
from collections import defaultdict
from dataclasses import fields
import json
from pathlib import Path

from PIL import Image
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from young_breed_probe import ROOT, digest, provenance

OUT = ROOT/'scratch/research/native-002'


def pixel_map(row):
    im = Image.open(OUT/row['file']).convert('RGBA')
    assert list(im.size) == row['size']
    ox,oy = row['offset']
    # Sparse absolute-coordinate mapping; transparent RGB values have no effect
    # in the renderer's keyed-alpha output and are checked separately below.
    result = {}
    for y in range(im.height):
        for x in range(im.width):
            rgba = im.getpixel((x,y))
            if rgba[3]:
                result[x-ox,y-oy] = rgba
    return result


def delta(a,b):
    return sum(a.get(p,(0,0,0,0)) != b.get(p,(0,0,0,0)) for p in a.keys()|b.keys())


def main():
    manifest = ROOT/'experiments/native-002.json'
    report = json.loads(manifest.read_text())
    assert report == json.loads((OUT/'report.json').read_text())
    assert report['provenance'] == provenance()
    assert digest((ROOT/'tools/native_saved_controls.py').read_bytes()) == report['script_sha256']
    groups = defaultdict(dict)
    for row in report['renders']:
        path = OUT/row['file']
        assert digest(path.read_bytes()) == row['png_sha256']
        im = Image.open(path).convert('RGBA')
        # Transparent pixels must be canonical, making sparse comparisons exact.
        assert all(p == (0,0,0,0) or p[3] == 255 for p in im.get_flattened_data())
        key = row['name'],row['pose'],row['yaw_degrees']
        groups[key][row['source'],row['age_side'],row['fatness_side']] = (row,pixel_map(row))
    comparisons = 0
    for item in report['comparisons']:
        group = groups[item['name'],item['pose'],item['yaw_degrees']]
        for ai in (0,1):
            for fi in (0,1):
                a,pa = group['prior',ai,fi]
                b,pb = group['capture',ai,fi]
                assert a['size'] == b['size'] and a['offset'] == b['offset'] and pa == pb
                assert (OUT/a['file']).read_bytes() == (OUT/b['file']).read_bytes()
                comparisons += 1
        a,b,c,d = [group['capture',ai,fi][1] for ai,fi in ((0,0),(1,0),(0,1),(1,1))]
        for key,left,right in (('default_pixels',a,d),('age_only_pixels',a,b),
                               ('fatness_only_pixels',a,c),('new_age_fatness_pixels',b,d),
                               ('new_fatness_age_pixels',c,d)):
            assert delta(left,right) == item[key], (item,key)
            comparisons += 1
    for row in report['mcp']:
        c = row['controls']
        side = 0 if row['source']=='prior' else 1
        direct = groups[row['name'],c['pose'],c['yaw_degrees']][row['source'],side,side][0]
        assert direct['png_sha256'] == row['png_sha256']
        metadata = json.loads((OUT/row['metadata']).read_text())
        assert metadata['game_version'] == 'petz4'
        assert metadata['appearance']['age_source'] == 'saved'
        assert metadata['appearance']['fatness_source'] == 'saved'
    resolver = ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/screenshots'))
    appearance_checks = []
    for source in report['inputs']:
        for side,path in source['paths'].items():
            assert digest((ROOT/path).read_bytes()) == source['sha256_by_source'][side]
        for pose in ('standing','sitting','lying'):
            paths = [source['paths'][side].removeprefix(prefix) for side,prefix in
                     (('prior','games/petz4/'),('capture','scratch/screenshots/'))]
            a,b = [load_saved_assets(resolver,p,pose=pose) for p in paths]
            changes = {}
            for group in ('balls','add_balls'):
                assert len(getattr(a.appearance,group)) == len(getattr(b.appearance,group))
                changed_fields = sorted({f.name for x,y in zip(getattr(a.appearance,group),getattr(b.appearance,group))
                                         for f in fields(x) if getattr(x,f.name) != getattr(y,f.name)})
                changes[group] = changed_fields
                allowed = {'size','fuzz'} if source['name'] == 'Homebody' else {'size'}
                assert set(changed_fields) <= allowed
            assert a.palette == b.palette and a.textures == b.textures
            appearance_checks.append({'name':source['name'],'pose':pose,
                                       'ball_fields_changed':changes,'same_palette_and_textures':True})
    result = {'manifest_sha256':digest(manifest.read_bytes()),
              'script_sha256':digest(Path(__file__).read_bytes()),
              'decoded_pngs':len(report['renders']),'independent_rgba_comparisons':comparisons,
              'mcp_links':len(report['mcp']),'appearance_checks':appearance_checks}
    (OUT/'independent-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    print('INDEPENDENT AUDIT PASS')


if __name__ == '__main__':
    main()
