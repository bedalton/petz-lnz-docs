# SHADE-002: retained shading after returning to a pose

Date: 2026-11-10. Direct renderer preparations retain **only ShadeState**, with local stdio MCP fresh baselines. Petz4 Scottie/Siamese adult copies from [SHADE-001](shade-001.md), explicit slopes0 and100. No native-game or MCP-animation claim. [Manifest](shade-002.json). Reproducer `scratch/petz-local-venv/bin/python tools/shade_history_probe.py` refuses overwrite; verifier `scratch/petz-local-venv/bin/python tools/check_shade_history.py`. Private evidence scratch/research/shade-002; audit scratch/research/shade-002-verification.json. Renderer unchanged at9d72d7afd5f7460ef18133c6179caaf8055082d9.

Twenty-four fixtures cover two species ×two slopes ×three poses ×yaw0/90 degrees. Each starts fresh, then prepares four further frames ending at the original controls. Histories: repeat; yaw offsets2,4,2,0; yaw offsets16,32,16,0; and head rotations16,32,16,0 (engine turns/256). Named animation frame, seed0, age100 and fatness50 stay fixed. Each preparation receives `FrameState(geometry=GeometryState(shade=prior_shade))`: ordering and texture orientation histories reset. Intermediate frames are prepared without drawing. Final draws use fresh line RNG seed1, raster seed1/step0 and shared fresh bounds. This isolates ShadeState, rather than simulating ordinary full-state animation.

| History | Cases | Changed offsets | Changed fills | Changed pixels |
| --- | --- | --- | --- | --- |
| Repeat |24 |0 |0 |0 |
| Small yaw arc |24 |0 |0 |0 |
| Wider yaw arc |24 |20 |20 |20 |
| Head arc |24 |3 |0 |0 |

Every final geometry, ordering and prepared texture orientation equals its fresh counterpart. Thus the wider-yaw differences can arise from retained shade alone in these controlled compositions. A changed offset need not change a fill or visible pixel: the three head-history cases demonstrate that limitation. Textured output and connectors receive the changed shade through normal preparation; no per-primitive additive attribution is claimed.

Eight synthetic histories contain88 update events across both distance signs, slopes0/100 and depths60/120. A distance change exactly10 retains both prior offset and prior accepted distance;11 triggers an update. The comparison uses the **last accepted distance**, not the immediately preceding frame. Inactive slots retain both values. Three early-return controls show invalid chest/butt keys or zero pose depth preserve the exact state object. Three negative/positive midpoint examples check truncation toward zero; a513-input case confirms state remains512 slots.

The independent verifier replays384 transition states,96 final compositions,192 indexed buffers and192 RGBA cells, checks original/reused-input/source/dependency/engine hashes, and links every fresh cell to its saved baseline. Twenty-four fresh baseline PNGs match local stdio MCP byte-for-byte; metadata checks input, age, fatness, seed and camera controls. These MCP checks validate fresh frames only. An initial verifier mistakenly expected comparison-sheet metadata from render_pet; it stopped after completing replay, was corrected to the render_pet PNG/control fields, then rerun.

Two sheets reviewed: Dogz slope100 standing side wider-yaw and Catz slope100 sitting side wider-yaw. Fur/body shade differences are visible with aligned silhouettes. These results narrow one possible contributor to [TEXTURE-004](texture-004.md) return-to-pose scene differences; they do not claim the same inputs or prove all of that experiment's geometry-state effects are shading. Appearance/topology changes still require resetting retained state. No renderer modification or native-fidelity conclusion.
