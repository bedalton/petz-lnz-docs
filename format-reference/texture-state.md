# Retained texture orientation

Scope: Petz 4 Scottie/Siamese renderer paths. This is a focused state reference, not a complete Texture List authoring specification. Native-game behavior remains unvalidated.

A default-state MCP still starts with fresh state. Repeated direct frames can retain geometry ordering, shading and per-ball texture orientations independently. In explicit renderer code, persist the FrameState returned by `draw_prepared_frame`, including texture sampler write-back; retaining only prepared state omits that write-back.

[TEXTURE-001](../experiments/texture-001.md) holds the animation frame and geometry fixed, resets line randomness/step, and separates geometry-only from texture-only retained state. Scottie sitting yaw0 first changes pixels on frame3; texture-only state reproduces all121 changed pixels while geometry-only/fresh state matches frame1. Other eleven pose/view fixtures match for eight frames. Do not infer native drift or universal stability from these samples.

[TEXTURE-002](../experiments/texture-002.md) replays the affected ball42 orientation: its constant quantized matrix has a nonidentity self-product, producing rounded delta(0,-1) each repeat. All seven saved repeat states match the arithmetic trace. GAP-006 remains open pending independent native evidence.

When comparing morph activation or geometry edits, record whether frames start fresh or retain state. [MORPH-005](../experiments/morph-005.md) shows why:47 different retained sort orders have no pixel effect in its views, while retained texture preparation changes ten Dogz sitting results. An order-only counterfactual is needed before attributing a visible difference to draw order.

[TEXTURE-004](../experiments/texture-004.md) returns camera/head/tilt controls to their initial values after four explicit retained draws. In48 Petz4 Scottie/Siamese compositions,34 whole scenes differ from fresh despite equal final ball geometry. Geometry-only,texture-only and order-only counterfactuals separate supplied state components; they are not additive attributions. All48 isolated diagnostic connector rasters match fresh. Twelve MCP calls validate only the fresh baselines, not the retained trajectories. Draw order can change occlusion and shared fuzz RNG consumption even when line randomness starts fresh each draw.

Relevant controls: input hash/seed, game version, pose and frame, camera, fatness/age, complete state history, line RNG, raster seed/step, texture-sampler state, renderer/source/dependency hashes. These controls support reproducibility; they do not establish game fidelity. See [renderer gaps](../troubleshooting/rendering-gaps.md) and [add groups](add-groups.md).
