# Retained texture orientation

Scope: Petz4 Scottie/Siamese renderer paths plus sampled saved Fuzzkin/Homebody. This is a focused state reference, not a complete Texture List authoring specification. Native-game behavior remains unvalidated.

**Updated build:** [UPDATE-002](../experiments/update-002.md) confirms the selected history effects and corrects their pixel counts. FrameState now also retains per-paint texture angles; host-orientation-only resets are not complete texture-state resets.

A default-state MCP still starts with fresh state. Repeated direct frames can retain geometry ordering, shading and per-ball texture orientations independently. In explicit renderer code, persist the FrameState returned by `draw_prepared_frame`, including texture sampler write-back; retaining only prepared state omits that write-back.

[TEXTURE-001](../experiments/texture-001.md) holds the animation frame and geometry fixed, resets line randomness/step, and separates geometry-only from texture-only retained state. Scottie sitting yaw0 first changes pixels on frame3; the historical host-orientation-only state reproduces121 changed pixels while geometry-only/fresh matches frame1. On6c1d883,the focused Scottie sitting/front recheck reproduces128 changed pixels at frame3 and141 at frame8;paint-angle-only stays fresh,while host-only and combined texture state match full. [UPDATE-006](../experiments/update-006.md) now rechecks all twelve fixtures on6c1d883:the other eleven remain pixel-stable for eight frames. At frames3/8,host-only and combined texture state match full;paint-only and geometry-only match fresh in all twelve. Do not infer native drift or universal stability from these samples.

[TEXTURE-002](../experiments/texture-002.md) replays the affected ball42 orientation: its constant quantized matrix has a nonidentity self-product, producing rounded delta(0,-1) each repeat. All seven saved repeat states match the arithmetic trace. GAP-006 remains open pending independent native evidence.

When comparing morph activation or geometry edits, record whether frames start fresh or retain state. [MORPH-005](../experiments/morph-005.md) shows why:47 different retained sort orders have no pixel effect in its views, while retained texture preparation changes ten Dogz sitting results. An order-only counterfactual is needed before attributing a visible difference to draw order.

[TEXTURE-004](../experiments/texture-004.md) returns camera/head/tilt controls to their initial values after four explicit retained draws. In48 Petz4 Scottie/Siamese compositions,34 whole scenes differ from fresh despite equal final ball geometry. Geometry-only,texture-only and order-only counterfactuals separate supplied state components; they are not additive attributions. All48 isolated diagnostic connector rasters match fresh. Twelve MCP calls validate only the fresh baselines, not the retained trajectories. Draw order can change occlusion and shared fuzz RNG consumption even when line randomness starts fresh each draw.

Relevant controls: input hash/seed, game version, pose and frame, camera, fatness/age, complete state history, line RNG, raster seed/step, texture-sampler state, renderer/source/dependency hashes. These controls support reproducibility; they do not establish game fidelity. See [renderer gaps](../troubleshooting/rendering-gaps.md) and [add groups](add-groups.md).

[UPDATE-007](../experiments/update-007.md) adds paint-only and combined-texture controls to all48 updated motion histories:host-only equals combined,and paint-only equals fresh in all48;combined differs from full in33. The diagnostic connector stays unchanged. This authored-connector matrix does not establish general painted-marking or saved-group behavior.

The UPDATE-007 pre-target paint-angle vectors are all zero (16 slots each). Its equal-pixel controls therefore do not test retention of accumulated nonzero paint angles.

[PAINT-001](../experiments/paint-001.md) exercises nonzero paint angles:all24 Fuzzkin histories have three nonzero pre-target pairs,paint-only changes2–63 pixels,and host-only differs from combined texture. Homebody haszero paint-only effects in24 histories. Save the complete draw-returned FrameState;host-only orientation is insufficient for these textured markings. Named animation frames and raster RNG are fixed;native behavior remains unvalidated.
