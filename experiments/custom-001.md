# CUSTOM-001: generated indexed textures and orientation

Date:2026-11-15. Backend: local stdio MCP and direct Python, renderer `49c7f62eab51b61b9f68801ba7571178670c433e`. Scope: Petz4 adult Scottie and Siamese, copied seed-resolved adult LNZ leaves, age100/fatness50/requested seed0 (renderer resolves0 to41). No renderer changes; no game validation. [Manifest](custom-001.json), [authoring recipe](../visual-editing/custom-textures.md), [community review](../sources/custom-textures.md).

## Reproduce

Run `scratch/petz-local-x86-venv/bin/python tools/custom_texture_probe.py`. Output `scratch/research/custom-001` must not exist; archive a previous run first. Run `scratch/petz-local-x86-venv/bin/python tools/check_custom_textures.py` to independently verify saved hashes, all84 aligned MCP/direct RGBA pairs, original/engine/source hashes and authoring CLI behavior. The verifier writes private `verification.json`. Inputs are private original game files already present in this workspace; no proprietary data is committed. Generated BMPs contain the extracted game palette and remain private as well.

Six original64×64 BMP variants: asymmetric diagnostic, RGB-table inversion only, index remap, clockwise90°, horizontal mirror, periodic fur strokes. A seventh configuration reuses the base diagnostic with mode1 instead of0; fur also uses mode1. Expanded tiles are256×256. The script round-trips tight top-down bytes through the independent renderer BMP decoder. It checks4,096 coordinates each for rotation and mirror; conversion tie/alpha controls and five sample-window cases are asserted. The CLI verifier separately exercises actual export, duplicate-path refusal, recolor, table replacement, orientation, nearest-color conversion, alpha rejection, fur generation and palette extraction.

For each species, append one slot after all effective inherited slots and one head-relative diagnostic marker: offset(-35,-160,0), size60, base color125. Existing anatomy is retained; no diagnostic connector is added. Effective stock texture entries are checked unchanged. The private fixed-span writer substitutes generated BMP bytes into existing portrait resource CHIP/SOPHISTO and asserts all other resource payloads are identical. Adult LNZ replacement is separately checked to change only that leaf. These are deliberately limited seed-resolved test copies, not a branch-preserving general breed editor or production resource-insertion tool. Portrait replacement is unsuitable for a finished distributable breed.

Six views/configuration: standing yaw0/90/180/270 degrees, sitting0, lying90. Direct Python uses native yaw0/64/128/192 respectively. Totals:16 edited private breed copies (including two failure controls),84 direct portraits and84 MCP portraits. The169th PNG is the14-row/four-camera comparison sheet. Backend/dependency versions,62 installed-vs-checkout source hashes, engine/original/copied-input hashes, decoded indices/palette hashes, full MCP metadata and PNG/RGBA hashes are in private `report.json`; compact public provenance is in the manifest.

## Findings and limits

| Claim | Evidence level and result |
| --- | --- |
| Table replacement differs from pixel remapping | Renderer-observed: inverted BMP RGB table preserves base pixels in12/12 fixtures; remapped indices differ in12/12 |
| Artwork transformations affect the sampled host | Renderer-observed: clockwise90° and mirror each differ from baseline in12/12; exact source-index coordinate controls pass |
| Mode influences the visible texture | Renderer-observed: mode1 differs from base mode0 in12/12; a specific color result is not generalized |
| Original procedural fur can load and render | Renderer-observed: all12 fur views match MCP/direct controls; no natural-coat or game-fidelity claim |
| Loose BMP paths load directly | Rejected in both species: an existing loose CUSTOM_DIAG.bmp under the configured root still yields missing BMP/CUSTOM_DIAG |
| Texture “angles” rotate artwork in degrees | Code-supported counterexample: sample-window angle(64,0) shifts the crop16 pixels right for diameter32/expanded256; artwork rotation is a separate transform |

Code path: `rendering/assets.py` obtains BMP by normalized resource basename from breed/shared PE resources, decodes the indices, then `rendering/texture.py:tile_texture` copies indices without foreign-palette remapping. Final output uses the executable palette. `sample_window` centers a crop, adds diameter-scaled angle offsets and wraps/clamps. This explains the controlled palette-table no-op and the distinction between source tile transformations and retained sampler state. It does not establish native Petz foreign-palette behavior.

Visual review of the full private orientation sheet: the marker shows unequal colored sectors in mode0, rotated/mirrored layouts are distinguishable, table-inverted rows match base, mode1 becomes muted and fur has diagonal strokes. Small marker windows often sample corner markers instead of central U/V labels. Body/camera views are context, not a calibrated UV map; transferring the motif to a different real host requires its own multi-view controls.

An initial harness run used degree values directly as native yaw in direct Python. The MCP comparison exposed the mismatch at90°; partial artifacts are archived at `scratch/research/custom-001-initial-yaw` and excluded from all successful counts. The successful harness explicitly converts degrees to native units. No renderer repair was required. After replacing a deprecated Pillow pixel accessor in the converter, a full run against the final authoring source again passes all84 MCP/direct pairs; all169 PNG hashes equal the archived first successful run (`scratch/research/custom-001-first-success`). The independent verifier passes against the final report and CLI source.

Remaining: in-game color/orientation/loading checks, general resource insertion with an original new name, external texture deployment, young resources, other breeds/versions, connectors/paint with these new tiles, retained animation and perceptual/profile-aware conversion or dithering. Reproducibility establishes this renderer's behavior, not native fidelity.
