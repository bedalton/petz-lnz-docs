# Texture index review

## Completed review — 2026-11-15

The user restored the supplied folder after the initial missing-directory preflight below. [Agent entry point](../texture-index/README.md), [visual tables](../texture-index/INDEX.md), [search metadata](../texture-index/index.json), [file audit](../texture-index/audit.json), [reproducer](../tools/texture_catalog.py).

### Verified from local files

All 238 JSON entries correspond to all 238 local BMP filenames. All sources decode as indexed images; all listed source dimensions match. Every corresponding PNG has exactly matching embedded-palette RGB pixels and fully opaque alpha. These checks concern the supplied files, not an executable palette or rendered pet. The retained report records Pillow version, catalog SHA-256, individual BMP/PNG/palette/pixel hashes, dimensions, used indices and index-253 pixel counts. It contains no texture pixel arrays or palette tables.

Ten groups share dimensions and indexed pixels; ten groups share dimensions and decoded RGB; eight groups are whole-BMP-identical. Duplicate names remain separate because game resource availability is unknown. Twenty-seven BMPs use index 253; this is a byte observation, not a transparency finding. `CLEAR.bmp` is 128×128, with every pixel index 253; its supplied PNG is opaque magenta.

The original five contact sheets were visually inspected as overview images. Their displayed counts total 234 (43+56+71+27+37), matching the original 234 Markdown rows. Four JSON/BMP entries had no table row or sheet tile: EGYPTM03, HERRING, HERRING2 and SCRIBBLE. The tables now contain all 238 entries, checked against JSON descriptions, uses and dimensions. Original contact sheets are preserved; both entry points explicitly document the four omissions. No pixel-by-pixel sheet reconstruction or exhaustive individual-image semantic review was performed.

### Corrections and consuming-agent improvements

- Removed the unsupported claim of a complete Petz texture inventory. Added per-entry unknown provenance/resource availability and editorial-description status.
- Replaced duplicated README/INDEX instructions with a focused selection workflow and a browsable index. Added discovery links from the project README, agent entry point, feature map and Texture List reference.
- Corrected the second Texture List field from “transparent color index” to renderer mode, linking existing [field evidence](../format-reference/texture-list.md). Removed invalid abbreviated Ballz syntax, fixed named tint promises, and withdrawn universal filename/loading compatibility claims. Source bitmap dimensions are distinguished from authored tile dimensions.
- Corrected visible counterexamples: Bunny is an illustrated motif, BLACK has dark bands, PURP/Pink have grain, and BUBBLESB/P are circular outline patterns. Removed assumed alpha/visibility/collision behavior for CLEAR and hair-transition descriptions. Existing sheet labels remain historical and may differ from corrected tables.
- Added JSON candidate search with AND queries, category filtering and limits, plus a reproducible audit that detects metadata/table drift, missing/unindexed BMPs, incorrect dimensions and differing/transparent previews.
- Ignored local BMPs, PNGs and editor sidecars; extended documentation checks to texture-index pages and prohibited tracking those assets. Only text metadata, references and tooling are committed.

All remaining stock-breed assignments and artistic uses are explicitly unverified editorial suggestions. This review does not supply their missing attribution or prove their accuracy. Broad search categories were retained for discoverability, including Babyz/test artwork; they are not species/version applicability guarantees.

### Verification

Run from `/workspace`:

```bash
scratch/petz-local-x86-venv/bin/python tools/texture_catalog.py audit --check texture-index/audit.json
python3 tools/check_docs.py
python3 tools/texture_catalog.py search wiry --category fur
```

Full retained audit passes all 238 entries. Search controls pass zero-match, case-insensitive query/category, Babyz category count (28) and two-result limit checks. Isolated copied-fixture controls reject metadata/table dimension drift, a changed RGB pixel, unexpected PNG alpha and an extra unindexed BMP; baseline/restored controls pass. Detailed private control results: `scratch/research/texture-index-review/verification.json`. Supplied artwork was read only; fixture changes are confined to ignored scratch copies.

No renderer/backend was invoked, changed or newly validated. No breed/game original was edited. Existing renderer observations are linked from [CUSTOM-001](../experiments/custom-001.md) and the Texture List reference, with their original version/species/control scope. Native game loading, tinting, transparency, orientation, collision and motion remain unvalidated. Resource provenance and target-version availability need separate verification before deployment.

## Initial preflight — superseded

The requested `/workspace/texture-index` directory was initially absent. `git ls-files '*texture*index*'` returned no tracked paths, and `find /workspace -type d -iname '*texture*index*'` returned no directories. The worktree was clean before that record. The user subsequently restored the folder; the missing-files condition is resolved.
