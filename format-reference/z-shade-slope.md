# Z Shade Slope in the renderer

Evidence: [SHADE-001](../experiments/shade-001.md) and [SHADE-002](../experiments/shade-002.md), Petz4 adult Scottie/Siamese and synthetic arithmetic. Renderer9d72d7afd5f7460ef18133c6179caaf8055082d9; no native-game validation.

`[Z Shade Slope]` takes a scalar integer. A standalone absent/empty/invalid value defaults to0, but absent leaf sections inherit: both sampled breed/master combinations resolve100. An explicit empty section instead resolves0.

| Setting | Fresh-state renderer behavior |
| --- | --- |
|0 | Depth gain2.2; shading remains enabled |
|100 | Depth gain4.2; matches absent section in the sampled breeds |
|-100 | Depth gain0.2 |
|-110 | Depth gain0; all tested fresh offsets0 |
|-220 | Depth gain-2.2; reverses the response relative to0 |

The shading midpoint is the truncated mean of chest/butt center depths. A ball's distance from it is scaled by `6 * (2.2 + 0.02 * slope) / pose_depth`, rounded halfway away from zero and clamped to[-6,6]. Pose depth comes from visible geometry bounds, including ball radii. Shape and ordering do not change in the controlled slope edits.

Flat fill colors10–149 clamp within their original ten-color palette band; other indices pass through this helper unchanged. Host-eye fills are exempt in assembly. Textured circles/connectors use additional remapping and raster rules; see [Texture List](texture-list.md) and [connector textures](connector-textures.md). This section does not validate incomplete paths in [GAP-007](../troubleshooting/rendering-gaps.md#known-incomplete-features-do-not-infer-from-mcp).

Retained shading only updates when an active slot's midpoint-relative distance changes by more than10 from its last accepted distance. Synthetic controls distinguish changes of10 from11; inactive slots retain history. In isolated shade-only return-to-pose compositions, wider yaw arcs change20/24 final scenes despite equal geometry/order/texture orientation; repeats and small yaw arcs change none. Head arcs can change stored offsets without changing fills or pixels. These are controlled renderer histories, not native animation validation. Use fresh preparation when comparing authoring changes; appearance/topology changes invalidate retained FrameState. Other breeds, young resources, versions and native behavior remain untested.

Omitting a depth-extreme visible ball can also change the denominator. [SHADE-003](../experiments/shade-003.md) sweeps804 base omissions:11 reduce depth,seven change fills,eight change shade-only counterfactual pixels. Unomitted coordinates/radii remain fixed. All793 depth-preserving cases preserve shade/fills. An omission preview can therefore include shading changes elsewhere; it is not solely a mask of removed geometry. Scope remains the two adult Petz4 breeds.
