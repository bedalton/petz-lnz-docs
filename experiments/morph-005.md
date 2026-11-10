# MORPH-005: pixel consequences of retained state

Date: 2026-11-10. Petz 4 Scottie/Siamese; renderer-observed only, with no native-game fidelity claim. No renderer source changes.

Run `scratch/petz-local-venv/bin/python tools/morph_pixel_probe.py`; refuses existing output. Reuses verified [MORPH-003](morph-003.md) private copies and the five [MORPH-004](morph-004.md) histories. [Manifest](morph-005.json) records sixty three-cell sheets, indexed/RGBA/PNG hashes, changed-pixel counts, twelve MCP baseline checks, controls, dependencies, nine installed source hashes and engine hashes. Private images/responses: scratch/research/morph-005. Installed sources match checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9; four engine hashes match RESTORE-002. Originals and reused copies retain recorded hashes.

## Controlled rendering path

Two species × two area variants × three poses × five histories = sixty cases. Input seed0, age100, fatness50, yaw0, default head rotation. Explicit morph percentages are direct Python controls, outside the current MCP default-state interface.

For each case render three aligned cells with the same final geometry bounds:

1. Fresh preparation with the entire history applied in one batch.
2. Retained FrameState after preparing and drawing the initial frame and every intermediate history prefix.
3. The batch drawing commands with only sorted/draw order replaced by the retained order.

The third cell isolates ordering while retaining batch circles, paint, eye overlays, textures, fills and endpoints. Each draw deliberately resets LineRenderer to seed1, raster seed1 and step0, including intermediate draws. Texture/geometry FrameState persists in cell2. This is a controlled explicit-state experiment, not a full simulation of runtime line randomness or animation timing.

Twelve initial default-state direct compositions equal `render_portrait` byte-for-byte and match twelve local stdio MCP render_pet PNGs (both species, both variants, three poses). This checks the harness path at default activation; it does not expose explicit history controls through MCP or validate native fidelity.

## Results

| Comparison | Cases with different pixels (of 60) |
| --- | --- |
| batch versus retained preparation | 10 |
| batch versus retained order alone | 0 |
| retained preparation versus batch commands with retained order | 10 |

The prior 47 ordering differences have no pixel consequence in these sampled views and states. That is narrower than saying ordering never matters.

The ten differing cases are every Dogz sitting history in both body/head variants. Each changes121 indexed pixels; batch/retained prepared commands also differ in these same cases. All other50 cases have equal prepared commands and pixels. Final geometry/fills still match. The order-only control therefore excludes sorted order as the cause of these sampled differences; it does not alone prove the exact remaining texture-state mechanism. Follow-up: repeat static frames without morph changes and independently reset texture/geometry state.

Dogz-dormant_body-sitting-cycle and Catz-dormant_head-lying-cycle sheets reviewed at native resolution. Cell order is batch, retained, batch commands with retained order. The Dogz stock texture pattern changes in the middle cell; the Catz example matches across cells. These are explicit local renderer compositions, not native screenshots. All180 RGBA cells have recorded hashes; only these two sheets received visual review.
