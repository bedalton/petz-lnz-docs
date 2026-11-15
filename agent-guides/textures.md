# Texture reference for client agents

Use this page when choosing a material, assigning it to a ball or paint marking, recoloring it, or positioning a directional gradient. Preserve original game files and functional anatomy; work on copies. The catalog is a shortlist of artwork, not a game resource specification.

## Find and assess artwork

| Need | Start here | What to verify |
| --- | --- | --- |
| Natural fur or a patterned coat | [Visual catalog](../texture-index/INDEX.md), Pet Fur / Animal Markings tables | Inspect individual PNG at its original aspect ratio; descriptions and stock-breed assignments are editorial |
| Wrinkles, skin or an eye motif | Facial Features table | Surface appearance does not create anatomy; keep the existing mouth, nose and eyes functional |
| Cloth, decoration or a hard surface | Fabric, novelty and environment tables | A material image does not imply supported clothing mechanics |
| A precise gradient or directional marking | [Create/recolor/orient artwork](../visual-editing/custom-textures.md), gradient recipe below | Calibrate on the actual host; no universal bitmap-to-anatomy orientation is established |
| Filename/dimensions/duplicate candidates | [index.json](../texture-index/index.json), [audit.json](../texture-index/audit.json) | Source dimensions, RGB preview, palette-index bytes and whole-file identity are different checks |

For a compact candidate list, run from `/workspace`:

```bash
python3 tools/texture_catalog.py search wiry --category fur --limit 5
python3 tools/texture_catalog.py search stripe --limit 8
```

Or open the [offline explorer](../texture-index/catalog.html). The 238 local candidates include Babyz and test artwork with unknown provenance and target-version availability. All 238 BMP/PNG pairs and source dimensions were file-verified; four entries are missing from the preserved contact sheets but present in the tables/explorer. See [catalog instructions](../texture-index/README.md).

## Assign a texture without breaking slots

[Texture List](../format-reference/texture-list.md) rows decode in the inspected renderer as `path, mode, tile_width, tile_height`. Slot numbers are zero-based effective row order. Preserve inherited rows and existing assignments when appending a dedicated slot. Use the complete [added-ball fields](../format-reference/add-ball.md) or [Paint Ballz fields](../format-reference/paint-ball.md) for the host; do not paste an abbreviated Ballz row from a visual example. For Lnz Version below 2, paint texture lookup differs; read that reference before assigning a slot.

Source BMP size is not the same as Texture List tile size. The mode field is not a starting angle. It controls renderer level/tint handling; do not substitute a degree value there. A path in the catalog does not prove a resource is installed: current renderer loading searches embedded BMP resources, and the tested loose BMP path failed. Use the [custom loading limits](../visual-editing/custom-textures.md#load-and-inspect-the-files) before deployment.

PNG thumbnails display the BMP's embedded RGB palette. In the tested renderer, index bytes, mode, host color and shading determine the result; an RGB palette-table edit alone did not recolor the sampled pet. Use index remapping or target-palette conversion for artwork changes. Magenta in an opaque preview is not proof of an alpha channel; CLEAR is not a general invisible-ball or collision control.

## Starting rotation and motion

**No supported per-ball LNZ starting-angle field was found in the inspected renderer/parser or the reviewed tutorials.** Do not invent a Texture Rotation section, append degrees to Texture List rows, or treat paint direction as bitmap rotation. Extra columns do not create orientation in the checked parser.

[No Texture Rotate](../format-reference/no-texture-rotate.md) accepts ball IDs, one per row. It disables their automatic texture-angle updates in the renderer. It does not accept yaw/pitch/roll or “point dark side away from face.” It can make a pattern stay visually fixed while the animal turns; that differs from anatomical attachment. Existing [retained-state experiments](../format-reference/texture-state.md) also show that motion history can affect texture appearance.

To change the initial artwork presentation, rotate, mirror or wrap-offset the **bitmap copy**, then assign that separate resource to the intended host. The [orientation workflow](../visual-editing/custom-textures.md#orient-a-texture-on-the-intended-host) uses exact indexed transforms. This is a calibrated artwork workaround, not a general LNZ UV control or a motion guarantee.

## Gradient: light toward the face, dark away

First distinguish two acceptance criteria: a correctly oriented gradient in a specified view/pose, or a dark region that remains anatomically away from the face while the pet turns and moves. A still preview can establish only the first.

1. Identify the actual host ball(s) and what “away from the face” means on that anatomy. Record the relevant head/nose direction in the host's local frame. Screen-right in one view will not define the same anatomical direction in every view. Paired left/right hosts may need separate mirrored artwork or separate paint placement.
2. For a still texture approach, apply an asymmetric diagnostic with distinguishable light/dark ends to that existing host. Keep geometry, host color, mode and tile dimensions fixed. Inspect which bitmap region reaches the face-facing side. Rotate/mirror/offset a copy of the gradient to make the light end faceward and the dark end outward. Keep all other hosts on their original slots.
3. Check the gradient at the intended ball size. A ball may sample only a small window of the expanded tile: a gradient across the full bitmap can appear almost flat in that window. Reposition or resize the artwork's transition deliberately; do not assume the whole image wraps around the visible ball. Recheck seams and neighboring views.
4. If the dark region must stay anatomically outward, **test a surface-paint approach**: place several overlapping, progressively darker markings toward the outward side on the existing host, using Paint Ballz direction for location. Use small color steps and compare overlaps at native size; this approximates a gradient and may show bands. Direction changes placement, not texture orientation. No ready recipe for this particular host has been game-validated.
5. Inspect front, both sides, back, head turns and standing/sitting/lying, plus the relevant age. Compare fresh stills and retained motion separately. `[No Texture Rotate]` is an optional comparison, not an automatic solution. Verify the final candidate in the intended game before promising face-relative attachment through motion.

Do not move or rebuild anatomy to compensate for a texture orientation problem. If a tiled gradient cannot meet the movement requirement, report that limit and retain the best verified surface-marking candidate rather than claiming a universal texture solution.

## Record and deliver

Return chosen filenames/resources and source hashes, effective slot numbers, mode/tile dimensions, modified hosts, palette/index operation, bitmap transform, renderer/backend revision and controlled views. State which game/species/age was checked and whether frames were fresh or retained. Separate file-verified facts, code-supported behavior, rendered observations and native-game validation. Include remaining uncertainty and the intended still/motion acceptance criterion.

Evidence: [catalog review](../docs/texture-index-review.md), [custom texture controls](../experiments/custom-001.md), [starting-orientation code controls and source review](../format-reference/no-texture-rotate.md). The gradient workflow is an authoring proposal; no target breed or new composed gradient render was supplied/tested in this unit.
