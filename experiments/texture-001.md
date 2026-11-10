# TEXTURE-001: repeated static frames and texture state

Date: 2026-11-10. Petz 4 Scottie/Siamese, renderer-observed only. No original-game validation or renderer modifications.

Run `scratch/petz-local-venv/bin/python tools/static_texture_probe.py`; refuses existing output. [Manifest](texture-001.json) records original hashes, twelve pose/view fixtures, two reset-control sheets and an eight-frame sequence per fixture, cell/PNG/indexed hashes, texture orientation traces, dependencies and six installed source hashes. The public manifest keeps orientation-state hashes and changed angles; full orientation snapshots remain in the private report. Private images/responses: scratch/research/texture-001. The initial run with two-frame controls is preserved at scratch/research/texture-001-two-frame-controls; the final run adds third-frame isolation. Four engine hashes match RESTORE-002; installed sources match checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9. Original game files remain unchanged and are only read.

## Controls

Two species × standing/sitting/lying × yaw0/90 = twelve fixtures. Fixed animation frame per named pose, seed0, age100, fatness50; no added markers or morph updates. Every draw uses fresh line RNG seed1, raster seed1 and step0. Geometry and animation stay fixed while FrameState is retained. Each fixture's initial direct PNG equals render_portrait and a local stdio MCP render_pet PNG byte-for-byte (twelve MCP checks).

Compare first frame, fully retained state, geometry-only state, texture-only state and completely fresh state. Apply these reset comparisons both after one prior draw (second-frame controls) and after two prior draws (third-frame controls). Eight-frame sequences separately retain the complete state throughout. Geometry is asserted unchanged.

## Observations

Every second-frame control is pixel-identical to the first frame. Only Scottie sitting at yaw0 changes on the third frame:

| Third-frame preparation | Pixels different from first |
| --- | --- |
| full retained state | 121 |
| geometry state only, texture orientations fresh | 0 |
| texture orientations only, geometry state fresh | 121 |
| entirely fresh state | 0 |

Full and texture-only pixels match in every fixture. This isolates the observed static-frame difference to retained texture orientations in these controls, independently of added markers, morph histories and geometry ordering. The effect in [MORPH-005](morph-005.md) is consequently reproducible without morph changes.

Scottie sitting yaw0 sequence changed-pixel counts versus frame1: 0,0,121,121,121,121,121,131 for frames1–8. Only prepared ball42 changes its drawing command at frame3; its texture angles progress (-5,16),(-5,15),(-5,14),…(-5,9), with a repeated update delta (0,-1). Geometry is constant. This establishes retained angle drift in this sampled renderer path, not its intended native semantics or exact numerical origin. Other eleven fixture sequences remain pixel-identical for all eight frames; that does not prove their orientation caches are identical.

Dogz-sitting-0-third-resets, Dogz-sitting-0-sequence and Catz-sitting-0-third-resets sheets visually reviewed at native resolution. Reset-sheet order: first, full retained, geometry-only, texture-only, fresh. Sequence order: frames1–8. Scottie stock texture changes appear in full/texture-only cells; Catz control cells match. Thirty-six sheets contain216 recorded RGBA cells; only these three sheets received visual review.

Tracked as GAP-006 pending independent native evidence. Do not repair the renderer solely because a static input drifts: the intended original-game orientation algorithm has not been validated by this project.
