# Connector texture sampling continuation

Date: 2026-11-10. User requested ten minutes. Four research units, local renderer unchanged; all findings remain asset-free implementation or renderer-observed breed evidence, not native-game validation.

| Unit | Evidence | Result |
| --- | --- | --- |
| [LINE-017](../experiments/line-017.md) | 360 synthetic rasters;10,512 exact samples;180 reversal pairs | Diagonal/tapered screen-aligned sampling; exact-fit and one-pixel-short thresholds |
| [LINE-018](../experiments/line-018.md) | 180 synthetic rasters;2,184 exact samples;12 large-canvas crop controls | Viewport corner clamps change geometry and can make oversized windows fit |
| [LINE-019](../experiments/line-019.md) | 30 asset loads;16 local MCP pairs;four sheets reviewed | Dalmatian/Persian Petz4 confirm endpoint texture routing; both use256x256 tiles |
| [LINE-020](../experiments/line-020.md) | 60 synthetic rasters;30,660 body/15,420 edge assertions | Sign flag gates shade below10; sampled bytes bypass flat-color substitutions |

## Verification

`tools/check_line_sampling_session.py` passes600 persisted synthetic indexed buffers,43,356 exact body samples,15,420 explicit-edge assertions,10 private edited copies,16 MCP PNGs/32 decoded RGBA cells,30 reloaded numerical cases and all public/private report matches. It verifies rejected state controls, reversed raster pairs, saved crop differences, shade arithmetic, private raw-pixel hashes, original resource hashes and unchanged bytes outside each edited leaf resource. For LINE-020 it reconstructs flat-control masks, verifies their saved hashes, and checks every saved edge/background byte as well as every body sample. It checks original/current source/resource DLL/dependency hashes. It also verifies all62 installed Python sources against the clean checkout and the previous whole-source hash audit. For LINE-019 it reloads all30 saved breed/pose cases and verifies pose-geometry invariance, block colors/paint presence, texture configuration/dimensions, texture hashes and remapped paint against recorded results. These are renderer consistency checks, not an independent geometry oracle or native-game validation.

Private summary: scratch/research/line-sampling-session-verification.json. Public manifest hashes are recorded there. Source-tree digest remains `e1cd30b0543fcd99d18ed9252a7c44de2a31a4decbcd482266df6af755681374`.

HTTP MCP discovery and get_capabilities pass at127.0.0.1:8765/mcp; private health record scratch/research/line-sampling-session-mcp-health.json. Actual16 image comparisons used local stdio MCP with Petz4 metadata; no hosted rendering. The default CLI version for the completed run was Petz4; the reproducer now supplies it explicitly and asserts saved metadata, without rerendering unchanged results.

Documentation links, manifest/hash syntax and private-file exclusion pass `tools/check_docs.py`. Raw synthetic buffers, stock resources, edited copies and PNGs remain ignored under scratch/games. Every research unit is committed using the required identity. Unrelated untracked istall-node is untouched.

## Scope and next steps

The new synthetic controls cover bounded framebuffer behavior; composed camera normalization can add behavior not tested here. Plain-raster masks deliberately avoid duplicating connector corner arithmetic, and sign/shade controls begin after texture remapping. Zero-index writes are indexed-buffer observations, not a claim about exporter transparency. Breed coverage expands texture routing only; native fidelity, retained evolving textured scenes, composed tiles with other dimensions and broader cross-version edits remain open. Independent native evidence remains the limit on fidelity claims.
