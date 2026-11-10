# Z Shade Slope in the renderer

Evidence: [SHADE-001](../experiments/shade-001.md), Petz4 adult Scottie/Siamese and synthetic arithmetic. Renderer9d72d7afd5f7460ef18133c6179caaf8055082d9; no native-game validation.

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

Retained shading only updates when an active slot's midpoint-relative distance changes by more than10 from its last accepted distance. A fresh-state slope edit does not test this history behavior. Use fresh preparation when comparing authoring changes; appearance/topology changes invalidate retained FrameState. Other breeds, young resources, versions and native behavior remain untested.
