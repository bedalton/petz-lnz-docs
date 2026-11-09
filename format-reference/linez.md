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
| 10 | Draw after | 1 used; order alternatives untested |

The current parser accepts at least two leading numeric fields and fills omitted fields with defaults. This is code-supported acceptance, not a native syntax guarantee. At revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, appearance/core.py defines the mapping; rendering/connectors.py derives each endpoint width from its thickness percentage times `min(2 * radius - 1, 127)`. [LINE-002](../experiments/line-002.md) checks this formula on explicit posed endpoints in three poses and compares actual local MCP images in front/side views. Both zero widths reject the block; otherwise each rounded endpoint width is clamped to at least 1. A zero at one end can still draw a narrow tip. Equal percentages taper when endpoint radii differ.

Adding the tested connector changed no computed ball geometry. Omitting either endpoint dropped the connector during appearance parsing. Omitting the parent head did not automatically hide the attached marker. Retain rows/IDs when hiding experimental details, and check each component's visibility separately.

Preserve effective inherited Linez when introducing a breed-level section; LINE-001 materializes those rows before appending. This experiment does not establish general inheritance behavior for Linez. See [attached details](../visual-editing/attached-details.md) and [omissions](omissions.md).
