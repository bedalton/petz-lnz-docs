# Linez: first connected-detail reference

Evidence: [LINE-001](../experiments/line-001.md), Petz 4 Scottie/Siamese local renderer; native-game behavior remains unvalidated.

| Column | Parsed field | Evidence |
| --- | --- | --- |
| 1–2 | Start/end ball IDs | Base head to appended marker tested |
| 3 | Fuzz | 0 used |
| 4 | Fill color | 125 diagnostic color used |
| 5–6 | Left/right colors | 244 used; independent effects untested |
| 7–8 | Start/end thickness | 0/0, 10/10, 25/25, 100/100, 100/0, 0/100 tested ([LINE-002](../experiments/line-002.md)) |
| 9 | Edge mode | 0 used; other modes untested |
| 10 | Draw after | 0/1 override; -1 follows global fallback ([LINE-003](../experiments/line-003.md)) |

The current parser accepts at least two leading numeric fields and fills omitted fields with defaults. [LINE-004](../experiments/line-004.md) exercises two-field rows through breed loading and actual local MCP comparisons; this remains implementation acceptance, not a native syntax guarantee. At revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, appearance/core.py defines the mapping; rendering/connectors.py derives each endpoint width from its thickness percentage times `min(2 * radius - 1, 127)`. [LINE-002](../experiments/line-002.md) checks this formula on explicit posed endpoints in three poses and compares actual local MCP images in front/side views. Both zero widths reject the block; otherwise each rounded endpoint width is clamped to at least 1. A zero at one end can still draw a narrow tip. Equal percentages taper when endpoint radii differ.

Adding the tested connector changed no computed ball geometry. Omitting either endpoint dropped the connector during appearance parsing. Omitting the parent head did not automatically hide the attached marker. Retain rows/IDs when hiding experimental details, and check each component's visibility separately.

Preserve effective inherited Linez when introducing a breed-level section; LINE-001 materializes those rows before appending. This experiment does not establish general inheritance behavior for Linez. See [attached details](../visual-editing/attached-details.md) and [omissions](omissions.md).

[LINE-003](../experiments/line-003.md) tests column 10 as 0 (before endpoint visits), 1 (after both endpoint visits), and -1 (global fallback). `Draw Linez Before Ballz` 1 defaults to before; 0 defaults to after. Explicit 0/1 override either global setting. This is endpoint-relative scheduling, not a promise to draw after every object in the scene. Existing line flags were frozen to isolate the comparisons.

Connections can affect body-area classification as well as pixels. [AREA-001](../experiments/area-001.md) links a head-attached marker to an ankle and observes area 8 become area 3, changing its direct head-rotation response. See [body areas](body-areas.md).

For tested two-field rows, `Default Linez Thickness` supplies both endpoint percentages. Values 25 and 100 match equivalent explicit rows; explicit row widths override global thickness. An explicitly empty thickness section falls back to 100 in LINE-004; absent-section inheritance was not tested. Other resolved defaults in that experiment are fuzz 0, fill -1, edge colors 244/244, edge mode 0, and before-endpoint scheduling with global Draw Linez Before Ballz=1.

[LINE-005](../experiments/line-005.md) isolates fill selection: -1 follows the start endpoint; -2 follows the end, including reversed endpoints, in twenty Petz4 Scottie/Siamese MCP pairs with flat diagnostic colors. Nonnegative values use explicit fill. Synthetic blocks additionally show -3 selecting the end and negative values inheriting selected endpoint texture; explicit fill bypasses texture. Shading averages endpoint offsets with truncation toward zero, then clamps within a palette band for colors10–149. Synthetic texture routing and -3 acceptance are not native syntax/fidelity claims. Edge colors remain separate and untested by this unit.
