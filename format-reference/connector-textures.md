# Connector texture selection and raster limits

Evidence: [LINE-013](../experiments/line-013.md), [LINE-014](../experiments/line-014.md), [LINE-015](../experiments/line-015.md), [LINE-016](../experiments/line-016.md), [LINE-017](../experiments/line-017.md), [LINE-018](../experiments/line-018.md), [LINE-019](../experiments/line-019.md), [LINE-020](../experiments/line-020.md). Renderer revision9d72d7afd5f7460ef18133c6179caaf8055082d9; no native-game validation. See [Linez fields](linez.md) and [randomness controls](connector-state.md).

Negative fill values select endpoint appearance: -1 chooses start; -2 chooses end in the breed samples. With both endpoints at base color125, selecting a textured head produces visible texture while selecting an untextured marker matches explicit125. Reversing the endpoints preserves the tested selection equivalences. Explicit fill bypasses endpoint texture. The code additionally requires the selected shaded color to lie in10–149 before creating texture paint; outside-band behavior is a code-supported condition, not a new breed test here.

The connector remaps selected endpoint tiled art at the connector's averaged depth shade. It does not simply copy the endpoint circle's final pixels. LINE-013 records loaded/remapped texture hashes and compares actual MCP pixels. LINE-016 matches those controls and PNGs in Petz3/5 Scottie/Siamese; this is narrow version evidence.

The current line raster path crops a window from the tile. Synthetic8x8 fixtures show centered x/y crop with different odd-space bias: x uses floor of spare/2; y uses ceil. Period0/8 controls match, and oversized windows do not wrap. If the raster box exceeds tile width or height, the line produces no pixels. Fuzz margin counts toward width; rejection occurs before fuzz RNG/table generation.

LINE-015 confirms a composed Petz4 example: head-to-marker offset -800 with an inherited256x256 texture equals marker-only, while the equivalent explicit125 line draws. Short -80 controls draw both. The long line still parses and builds a valid textured block. This distinguishes a raster size rejection from an absent line or ineligible endpoint. It does not establish the native game's limit.

For a disappearing textured connector, compare matched textured, explicit-fill and no-line controls; inspect block construction and raster dimensions. Keep offset/pose/geometry identical within each comparison. Do not assume a successful untextured render validates the textured path. Texture-size rejection remains tested only in Petz4 Scottie/Siamese composed scenes and small synthetic fixtures.

Synthetic diagonal extension [LINE-017](../experiments/line-017.md) covers 360 fixtures and 10,512 exact pixel samples: exact-fit tiles draw; tiles one pixel too narrow or short reject. Sampling stays aligned to screen x/y rather than rotating along the connector, including tapered and fuzzy lines. Reversing both endpoints and taper widths preserves all 180 paired rasters. These controls avoid clipping and use unsigned, unshaded paint.

Viewport clipping changes these bounds: [LINE-018](../experiments/line-018.md) observes corner clamping before texture-size rejection. A smaller viewport can make a previously oversized texture window fit. Clamped diagonals can differ from simply cropping a larger render, and fully offscreen connectors can collapse onto a border instead of being culled. These are asset-free renderer controls, not native clipping semantics.

Direct signed/shaded TexturePaint controls [LINE-020](../experiments/line-020.md) sample all byte values with offsets-128/-1/0/1/127. Unsigned paint shades every byte modulo256; has_sign=true shades only source values below10. Sampled0 is written to the indexed buffer, and sampled texture bytes bypass flat-color substitutions. Explicit edge colors remain unchanged by texture shading. These controls begin after remapping and do not establish native semantics or exporter transparency.

Remaining: other tile dimensions in composed breeds, retained evolving scenes and independent native evidence.
