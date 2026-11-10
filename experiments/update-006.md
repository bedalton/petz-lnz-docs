# UPDATE-006: complete static texture matrix

Date: 2026-11-10. [Manifest](update-006.json). Integration6c1d883, Petz4 Scottie/Siamese, standing/sitting/lying, front/side. This extends [UPDATE-002](update-002.md)'s single-fixture recheck to all12 [TEXTURE-001](texture-001.md) fixtures. Historical evidence stays intact.

**Confirmed with corrected counts:** eleven fixtures remain pixel-stable through eight fixed-pose draws. Scottie sitting/front changes128 pixels on frame3 and141 on frame8; sequence counts are0,0,128,128,128,128,128,141. Its historical counts differ; the other eleven count vectors match. Ball geometry and bounds stay equal to fresh throughout.

At both frame3 and frame8, all12 fixtures receive six reset controls: full retained state, geometry only, host orientation only, paint angles only, combined host/paint texture state, and fresh. Host-only and combined-texture pixels match full in all24 target checks; geometry-only and paint-angle-only match fresh. These counterfactuals isolate the observed static pixel change to retained host orientation in this matrix. Equal pixels do not show that paint-angle state never changes or is generally irrelevant.

Controls: seed0,age100,fatness50; fixed named animation frame; fresh line RNG seed1, raster seed1/step0 on every draw. Persist the FrameState returned after drawing, including sampler write-back. Local stdio MCP validates all12 fresh baselines only; retained trajectories are direct renderer evidence, not MCP animation or native-game validation.

Run `scratch/petz-local-venv/bin/python tools/revalidate_static_matrix.py` into a fresh scratch/research/update-006 folder. `scratch/petz-local-venv/bin/python tools/check_static_matrix_update.py` independently repeats all96 sequence draws and144 reset draws, checks exact saved PNG bytes and240 post-draw state hashes,12 MCP PNG/metadata links, original breed/engine hashes, dependencies and62 installed/checkout sources. Total saved PNGs252. No renderer source or original assets changed. GAP-006 remains open pending independent native evidence.
