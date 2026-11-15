# Create, recolor and orient custom textures

Use [texture_author.py](../tools/texture_author.py) to generate original tiles, convert artwork to indexed BMP, recolor indices, or rotate/mirror/shift the artwork without resampling. Outputs refuse existing paths. Pillow is required; palette extraction also requires the installed renderer. Keep palettes, generated assets and game copies under ignored `scratch/`.

Evidence: [CUSTOM-001](../experiments/custom-001.md), local renderer `49c7f62`, adult Petz4 Scottie/Siamese. Native-game loading, orientation and color fidelity are unvalidated. [Community notes](../sources/custom-textures.md) distinguish tutorial recommendations from our tests.

## Choose the operation

| Intent | Operation | What changes |
| --- | --- | --- |
| Recolor an existing indexed texture in Petz | `remap` | Pixel indices change; the palette table stays fixed |
| Replace the RGB table while retaining index meaning | `palette-table` | Palette RGB triples change; pixel indices stay fixed |
| Preserve the approximate appearance of RGB artwork using Petz colors | `convert` | RGB pixels are assigned nearest allowed target indices |
| Reorient or reposition a pattern | `orient` | Indexed pixels rotate, mirror, or wrap-shift; colors stay fixed |

In the tested renderer, a palette-table-only change gives identical output in all twelve species/pose/view fixtures. Remapping indices changes all twelve. The texture's embedded RGB table is decoded but not used to convert texture indices into the executable palette. A foreign-palette BMP can therefore look correct in an image editor and wrong in the preview. Converting its RGB appearance to target indices is a separate operation. Native foreign-palette mapping is not tested.

## Generate usable example files

Run from `/workspace`. These examples use the existing private Petz4 executable as the palette authority, without modifying it or distributing its palette:

```bash
mkdir -p scratch/custom-textures
scratch/petz-local-x86-venv/bin/python tools/texture_author.py extract-palette \
  'games/petz4/Petz 4.exe' scratch/custom-textures/palette.json
scratch/petz-local-x86-venv/bin/python tools/texture_author.py generate \
  scratch/custom-textures/diagnostic.bmp --palette scratch/custom-textures/palette.json
scratch/petz-local-x86-venv/bin/python tools/texture_author.py generate \
  scratch/custom-textures/fur.bmp --palette scratch/custom-textures/palette.json --pattern fur
```

The original 64×64 diagnostic has unequal corner markers, bands and bitmap axes: +U points right and +V points down. A small ball samples a crop, so its preview may show only corner markers rather than the central labels. The fur tile uses periodic diagonal strokes and indices10–17. It is a simple material example, not a calibrated coat. Every generated BMP is uncompressed, eight-bit indexed, with 256 palette entries.

## Recolor or convert artwork

For an exact index substitution:

```bash
scratch/petz-local-x86-venv/bin/python tools/texture_author.py remap \
  scratch/custom-textures/diagnostic.bmp scratch/custom-textures/recolored.bmp \
  --map '{"25":65,"65":105}'
```

Mappings are simultaneous: original25 becomes65, original65 becomes105. Values not listed remain unchanged. These are diagnostic indices, not promises of named coat colors. Texture mode, host color and shading can alter the result; compare on the actual host.

To replace only the embedded RGB table, use `palette-table INPUT.bmp OUTPUT.bmp --palette OTHER.json`. The JSON format is exactly256 `[red, green, blue]` integer triples in index order. A full indexed image palette can also be supplied instead of JSON. This operation does **not** find nearest colors.

To convert original RGB artwork:

```bash
scratch/petz-local-x86-venv/bin/python tools/texture_author.py convert \
  scratch/custom-textures/artwork.png scratch/custom-textures/artwork.bmp \
  --palette scratch/custom-textures/palette.json --indices 10:150
```

Conversion uses nearest squared distance in encoded RGB, no dithering; ties select the lowest allowed index. `10:150` includes10–149, the renderer's remapped coat bands. This conservative default excludes other index roles. Choose a narrower range deliberately if the material needs one band. `0:256` permits every index but does not establish transparency or shading semantics. Transparent input is rejected: explicitly flatten it onto the intended background first. There is no resizing or automatic palette optimization. RGB distances do not account for perceptual color or profiles; use actual-host previews rather than relying on the source picture alone.

## Orient a texture on the intended host

Start with the asymmetric diagnostic on a **copy** of the target breed, append a dedicated effective Texture List slot, and change only the intended host's texture assignment. Preserve inherited slots and all existing anatomy. Read [Texture List](../format-reference/texture-list.md) and the correct host fields, including [added ball](../format-reference/add-ball.md), or [paint](../format-reference/paint-ball.md) fields before editing.

```bash
scratch/petz-local-x86-venv/bin/python tools/texture_author.py orient \
  scratch/custom-textures/diagnostic.bmp scratch/custom-textures/cw90.bmp --turns 1
scratch/petz-local-x86-venv/bin/python tools/texture_author.py orient \
  scratch/custom-textures/diagnostic.bmp scratch/custom-textures/mirror.bmp --mirror
scratch/petz-local-x86-venv/bin/python tools/texture_author.py orient \
  scratch/custom-textures/diagnostic.bmp scratch/custom-textures/shifted.bmp --shift 16 0
```

`--turns 1` rotates clockwise90°; `--mirror` flips horizontally **after** rotation; shift is applied last and wraps at tile edges. PositiveX moves artwork right; positiveY moves it down. These operations preserve exact palette indices. No interpolation is used. For a vertical flip combine `--turns 2 --mirror`.

Hold host, geometry, slot mode/dimensions, color, pose, age, fatness, seed and camera fixed while comparing artwork variants. Then inspect front, both sides, back and at least sitting/lying. Record which corner or arrow reaches the desired visible location on that particular host. Transfer the same artwork transformation to the finished tile and recheck. A different host, diameter, camera or pose can sample a different crop; there is no validated universal “bitmap top equals animal back” rule here. For markings, direction vectors place Paint Ballz on the host; they are not a general image-rotation parameter.

The renderer's retained texture “angles” shift a sample window. They are not a BMP rotation in degrees. In the isolated256×256/diameter32 control, angle(64,0) moves the sample start16 pixels right. Rotate the artwork for an actual90° change. Start with fresh stills after editing; see [texture state](../format-reference/texture-state.md) before evaluating retained motion.

## Load and inspect the files

Current local loading searches BMP resources embedded in the breed/shared PE files, using the uppercased basename without extension. In CUSTOM-001, a loose `art/textures/CUSTOM_DIAG.bmp` beside the asset root still fails with missing BMP/CUSTOM_DIAG. Adding a Texture List path alone therefore does not make this renderer load a loose BMP.

The [research harness](../tools/custom_texture_probe.py) demonstrates a controlled workaround: replace one existing BMP resource in a **private copied breed**, point a newly appended slot at that resource, and assign it only to a new diagnostic marker. It checks all other resource payloads remain unchanged. This intentionally repurposes the breed's portrait BMP resource, so these research copies are not finished distributable breeds. The fixed-span writer only supports a BMP that fits the existing resource span. A general resource insertion/renaming tool, external texture deployment and native game installation remain separate work.

Use64×64 source art tiled into256×256 for this tested path. Source bitmap size and Texture List tile dimensions are different controls. Community32/64 artwork recommendations do not contradict the [connector tile-size limits](../format-reference/connector-textures.md): those tests concerned the expanded tile/window, not source artwork size.

Ready generated examples are private at `scratch/research/custom-001/{base,table,indices,cw90,mirror,fur}.bmp`; actual CLI examples are in `scratch/custom-textures/`, with a ready `examples.zip` pack containing the BMPs, RGB conversion example and a short README. The private `orientation-sheet.png` compares seven variants across two species and four camera views. See the experiment for hashes, controls, reproducibility and remaining limits. Before claiming game compatibility, load a copy in the intended game version, compare the same diagnostic corners/colors and inspect motion.
