# Choose a texture

Use this catalog to shortlist artwork, then test it on a copy of the intended host. The collection has 238 supplied BMPs, 238 matching opaque PNG previews and five contact sheets. It mixes pet materials, Babyz hair, environment artwork and test images. Its original source and game/version coverage are unknown; it is not an inventory of everything installed in Petz.

Open the [offline HTML explorer](catalog.html) for browser search and category filtering. It embeds the same metadata, so it works without a local server; images require the local PNGs. The audit rejects drift between its embedded data and `index.json`.

1. Search [index.json](index.json) by filename, category, tags or description. All descriptions and uses are editorial candidates; named stock-breed assignments are unverified. Browse the [visual index](INDEX.md) or its contact sheets, then open the individual PNG at native aspect ratio. A rabbit illustration (`Bunny.bmp`) is different from a fur tile (`BUNNYBROWN.bmp`).
2. Check [audit.json](audit.json) for source dimensions, exact file hashes, palette-index usage and duplicate groups. RGB-identical previews do not necessarily establish equivalent indices or resources. Use `indexed_pixels_sha256` to compare dimensions plus index bytes, and `bmp_sha256` for whole-file identity. Duplicate filenames are preserved because availability may differ between games.
3. Verify the chosen resource exists in the intended game/version and loader. A local BMP or catalog entry does not prove it is installed. The current renderer loads embedded BMP resources by normalized basename; loose BMP loading failed in [CUSTOM-001](../experiments/custom-001.md). Preserve the filename spelling and avoid assuming path/case behavior transfers to other tools or native games.
4. Read [Texture List fields](../format-reference/texture-list.md) before editing. Rows are `art_path, mode, tile_width, tile_height` in the tested renderer. The second field is **mode**, not a transparent palette index. Slots follow effective row order; preserve inherited assignments and append a dedicated slot when appropriate. Source bitmap dimensions in this catalog are not recommended Texture List dimensions. Use the actual [added-ball](../format-reference/add-ball.md) or [paint](../format-reference/paint-ball.md) field reference; the former catalog's abbreviated Ballz row was not executable syntax.
5. Preview the material with controlled host, mode, color, tile dimensions, seed, age, fatness, pose and camera. Compare front, sides and back, then sitting/lying. Record renderer/backend version, input hashes and controls. Keep renderer observations separate from game validation. Check native loading, color, orientation and motion before claiming game compatibility.

## Search and verify

Run from `/workspace`. Search uses the Python standard library; audit also needs Pillow (the existing local renderer environment provides it):

```bash
python3 tools/texture_catalog.py search wiry --category fur
python3 tools/texture_catalog.py search stripe --limit 8
python3 tools/texture_catalog.py search --category babyz
scratch/petz-local-x86-venv/bin/python tools/texture_catalog.py audit --check texture-index/audit.json
```

Query words are ANDed, case-insensitively, across each JSON entry; `--category` filters a category substring. Results include total matches and at most `--limit` entries (20 by default). Treat result order as catalog order, not a suitability ranking. Use `audit --write scratch/texture-catalog-audit.json` to inspect intentional changes without replacing the retained report.

## Palette and visibility cautions

The audit verifies exact RGB equality between each supplied BMP and its PNG, with fully opaque preview alpha. It does not verify how the embedded palette compares with an executable's palette. In the tested renderer, texture index bytes, host color, mode and shading determine appearance; changing only the BMP's RGB palette did not change sampled renders. A yellow-looking preview therefore does not promise a yellow coat. See the [palette conversion and orientation workflow](../visual-editing/custom-textures.md).

`CLEAR.bmp` is a 128×128 bitmap filled with index 253, not a 1×1 alpha image. Magenta regions in the Babyz and diagnostic artwork are opaque in these previews. No transparency, invisible-ball, collision or alpha behavior was established by this catalog. Texture artwork cannot establish collision behavior. Clothing-themed images can be material candidates; the renderer's clothing system remains unsupported. This review does not establish native Babyz applicability.

## Evidence and maintenance

[Review findings](../docs/texture-index-review.md) distinguish file checks, sampled visual corrections and existing renderer evidence. [audit.json](audit.json) records hashes, Pillow version, dimensions, index usage and duplicates. The catalog's descriptive text has no supplied primary-source attribution. No new breed rendering or native-game testing was performed for this review.

The BMPs, PNGs, contact sheets and editor `.import` sidecars stay local and ignored. Do not commit supplied game artwork. Share metadata/tooling separately from assets; recipients need their own local copies to open previews or replay the audit. Keep `index.json` and `INDEX.md` in sync when changing descriptions; rerun the audit after intentional metadata changes.

The five supplied contact sheets cover 234 entries. `EGYPTM03.bmp`, `HERRING.bmp`, `HERRING2.bmp` and `SCRIBBLE.bmp` are absent from those sheets; use their individual previews in the [General Patterns table](INDEX.md#general-patterns--textures-4-textures).
