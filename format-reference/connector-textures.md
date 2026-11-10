# Connector texture selection and raster limits

Evidence: [LINE-013](../experiments/line-013.md), [LINE-014](../experiments/line-014.md), [LINE-015](../experiments/line-015.md), [LINE-016](../experiments/line-016.md). Renderer revision9d72d7afd5f7460ef18133c6179caaf8055082d9; no native-game validation. See [Linez fields](linez.md) and [randomness controls](connector-state.md).

Negative fill values select endpoint appearance: -1 chooses start; -2 chooses end in the breed samples. With both endpoints at base color125, selecting a textured head produces visible texture while selecting an untextured marker matches explicit125. Reversing the endpoints preserves the tested selection equivalences. Explicit fill bypasses endpoint texture. The code additionally requires the selected shaded color to lie in10–149 before creating texture paint; outside-band behavior is a code-supported condition, not a new breed test here.

The connector remaps selected endpoint tiled art at the connector's averaged depth shade. It does not simply copy the endpoint circle's final pixels. LINE-013 records loaded/remapped texture hashes and compares actual MCP pixels. LINE-016 matches those controls and PNGs in Petz3/5 Scottie/Siamese; this is narrow version evidence.

The current line raster path crops a window from the tile. Synthetic8x8 fixtures show centered x/y crop with different odd-space bias: x uses floor of spare/2; y uses ceil. Period0/8 controls match, and oversized windows do not wrap. If the raster box exceeds tile width or height, the line produces no pixels. Fuzz margin counts toward width; rejection occurs before fuzz RNG/table generation.

LINE-015 confirms a composed Petz4 example: head-to-marker offset -800 with an inherited256x256 texture equals marker-only, while the equivalent explicit125 line draws. Short -80 controls draw both. The long line still parses and builds a valid textured block. This distinguishes a raster size rejection from an absent line or ineligible endpoint. It does not establish the native game's limit.

For a disappearing textured connector, compare matched textured, explicit-fill and no-line controls; inspect block construction and raster dimensions. Keep offset/pose/geometry identical within each comparison. Do not assume a successful untextured render validates the textured path. Texture-size rejection remains tested only in Petz4 Scottie/Siamese composed scenes and small synthetic fixtures.

Remaining: threshold sweeps with other tile dimensions, diagonals, signed/shaded texture sampling, other breeds, retained evolving scenes and independent native evidence.
