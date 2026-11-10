# PAINT-004: paint group preparation controls

Date: 2026-11-10. Backend: installed local Python preparation API, integration6c1d883. Synthetic assets only; no MCP, raster, saved-pet or native-game calls. [Manifest](paint-004.json), [reproducer/verifier](../tools/paint_group_controls.py).

## Question and result

Does changing only the Paint Ballz group field affect prepared paint commands? In 180 comparisons against group0, groups -1/1/2/15/255 produce exactly equal CircleBlock records. All180 nonzero-group cases emit `unsupported_paint_fields`; all36 group0 cases omit it. This agrees with code inspection: preparation never reads `paint.group`, and the preview diagnostic explicitly says group color controls are not applied.

The216 commands span six source colors (9/10/35/125/149/150), three shade offsets (-6/0/6), and flat/textured selection. Fill equals the independent shade_color result. Texture preparation occurs only for textured cases whose resolved fill is10–149. Replacing the source color with65 changes fill in all216 positive controls, showing the fixture reaches color resolution. Command equality includes prepared texture data, bounds, outlines and paint indices.

Controls: host bounds0/0/41/41, diameter50%, direction0/0/-1, zero rotations, synthetic16x16 all-byte texture, levels enabled/own level-1. Manifest records package version, checkout revision, all62 installed Python hashes and exact checkout-source agreement. No original files or renderer code changed.

## Reproduce

```sh
scratch/petz-local-venv/bin/python tools/paint_group_controls.py --verify
scratch/petz-local-venv/bin/python tools/check_docs.py
```

Initial generation requires a missing manifest and refuses overwrite. First run reached all assertions but used the wrong distribution name for version metadata; corrected to petz-renderer-mcp before manifest generation. No partial report was written.

## Limits and next work

This is renderer-observed command equality and code-supported diagnostic behavior, not pixel or game validation. The synthetic fixture bypasses parsing and saved-pet assembly; it does not establish saved-group retint semantics or behavior across species, ages or versions. The parser stores group separately from resolved color; that source observation alone does not prove all saved-pet routes ignore group data. End-to-end saved-group overrides and independent native evidence remain open.
