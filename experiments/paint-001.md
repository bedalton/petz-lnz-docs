# PAINT-001: saved-pet paint-angle motion

Date: 2026-11-10. [Manifest](paint-001.json). Petz4 integration6c1d88325ced89109f8e4b9d724fa8ab6037b42c. Read-only Fuzzkin and Homebody saved inputs,three poses,front/side,four repeat/yaw/head/tilt histories returning to the original target. This extends [UPDATE-007](update-007.md) beyond its all-zero paint-angle fixtures.

| Saved pet | Histories | Nonzero pre-target paint state | Paint-only changes fresh pixels | Host-only differs from combined texture |
| --- | --- | --- | --- | --- |
| Fuzzkin |24 |24 |24 |24 |
| Homebody |24 |0 |0 |0 |

Fuzzkin prepares three textured paints. All24 pre-target states retain three nonzero paint-angle pairs;paint-only counterfactuals change2–63 pixels from fresh. Even the repeated fixed-pose history changes pixels. Homebody has no configured textured paints and supplies a negative control,not a matching geometry/species control. Combined texture differs from full retained state in18 histories per pet,so texture components do not explain all full-state differences.

All final ball geometry/bounds match fresh. Raster RNG seed1 and step0 reset on each draw. The draw-returned FrameState carries geometry,host orientations and paint angles independently. Seven final controls are full,geometry-only,host-only,paint-only,combined texture,fresh,and order-only. These are counterfactual components,not additive shares of changed pixels.

Saved age/fatness/seed are preserved without overrides (Fuzzkin age33,Homebody15;fatness50). All48 fresh outputs match UPDATE-003,with12 new local stdio MCP baseline checks using explicit Petz4 root/version. MCP checks only fresh stills;the192 motion transitions and336 final draws are direct renderer evidence. No native-game validation is claimed.

Run `scratch/petz-local-venv/bin/python tools/saved_paint_motion.py` into a fresh scratch/research/paint-001 folder. `scratch/petz-local-venv/bin/python tools/check_saved_paint_motion.py` reruns all histories/final controls and verifies348 exact PNGs,private full transition/final state bytes,48 earlier baseline links,saved input/engine/dependency hashes and62 installed sources against checkout. Both pass. No original files,renderer sources or historical manifests changed.

The initial ad-hoc probe omitted tools from Python's module path and failed before loading inputs;the corrected probe and committed reproducer use the workspace tools. This is harness setup,not a renderer failure. Scope remains two saved Petz4 inputs with fixed named animation frames;group retint and native behavior remain separate questions.
