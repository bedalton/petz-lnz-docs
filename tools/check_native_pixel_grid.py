"""Independent scalar/Pillow check of NATIVE-003, including cropped borders."""
import json
from pathlib import Path
from PIL import Image
from native_pixel_grid import ROOT, OUT, sha


def first_mismatch(image, factor, phase_x, phase_y):
    pixels = image.load()
    for y in range(image.height):
        sy = max(0,phase_y + ((y-phase_y)//factor)*factor)
        for x in range(image.width):
            sx = max(0,phase_x + ((x-phase_x)//factor)*factor)
            if pixels[x,y] != pixels[sx,sy]:
                return [x,y]
    return None


def main():
    manifest = ROOT/'experiments/native-003.json'
    report = json.loads(manifest.read_text())
    assert report == json.loads((OUT/'report.json').read_text())
    assert sha((ROOT/'tools/native_pixel_grid.py').read_bytes()) == report['script_sha256']
    intake = json.loads((ROOT/'scratch/research/native-001/inventory.json').read_text())
    for row in intake['inputs']:
        assert sha((ROOT/row['path']).read_bytes()) == row['sha256']
    witnesses = []
    reconstructed_pixels = 0
    for row in report['stills']:
        original = Image.open(ROOT/row['path']).convert('RGB')
        latent = Image.open(OUT/row['file']).convert('RGB')
        assert sha((OUT/row['file']).read_bytes()) == row['png_sha256']
        selected = row['selected']
        assert selected['factor'] == 2
        assert list(latent.size) == selected['latent_dimensions']
        px,py = selected['phase_x'],selected['phase_y']
        # Rebuild each original coordinate from a latent sample, including the
        # optional clipped first and last column/row. No NumPy/spans/repeat used.
        src,dst = original.load(),latent.load()
        for y in range(original.height):
            ly = (y-py)//2 + bool(py)
            for x in range(original.width):
                lx = (x-px)//2 + bool(px)
                assert src[x,y] == dst[lx,ly], (row['path'],x,y)
                reconstructed_pixels += 1
        exact = 0
        for candidate in row['candidates']:
            witness = first_mismatch(original,candidate['factor'],candidate['phase_x'],candidate['phase_y'])
            assert (witness is None) == (candidate['mismatching_pixels']==0)
            exact += witness is None
            witnesses.append({'path':row['path'],'factor':candidate['factor'],
                              'phase':[candidate['phase_x'],candidate['phase_y']],
                              'first_mismatch':witness})
        assert exact == 1
    for row in report['video_samples']:
        im = Image.open(ROOT/row['path']).convert('RGB')
        for candidate in row['candidates']:
            witness = first_mismatch(im,2,candidate['phase_x'],candidate['phase_y'])
            assert witness is not None and candidate['mismatching_pixels'] > 0
            witnesses.append({'path':row['path'],'factor':2,
                              'phase':[candidate['phase_x'],candidate['phase_y']],
                              'first_mismatch':witness})
    result = {'manifest_sha256':sha(manifest.read_bytes()),
              'script_sha256':sha(Path(__file__).read_bytes()),
              'unchanged_intake_files':len(intake['inputs']),
              'fully_reconstructed_rgb_pixels':reconstructed_pixels,
              'grid_decisions':len(witnesses),'witnesses':witnesses}
    (OUT/'independent-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='witnesses'},indent=2))
    print('INDEPENDENT AUDIT PASS')


if __name__ == '__main__':
    main()
