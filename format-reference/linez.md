# Linez: first connected-detail reference

Evidence: [LINE-001](../experiments/line-001.md), Petz 4 Scottie/Siamese local renderer; native-game behavior remains unvalidated.

| Column | Parsed field | Evidence |
| --- | --- | --- |
| 1–2 | Start/end ball IDs | Base head to appended marker tested |
| 3 | Fuzz | 0 used |
| 4 | Fill color | 125 diagnostic color used |
| 5–6 | Left/right colors | 244 used; independent effects untested |
| 7–8 | Start/end thickness | 100/100 tested, produces broad taper |
| 9 | Edge mode | 0 used; other modes untested |
| 10 | Draw after | 1 used; order alternatives untested |

The current parser accepts at least two leading numeric fields and fills omitted fields with defaults. This is code-supported acceptance, not a native syntax guarantee. At revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, appearance/core.py defines the mapping; rendering/connectors.py derives each endpoint width from its thickness percentage times `min(2 * radius - 1, 127)`. The percentage formula is code-supported; no width sweep has been performed.

Adding the tested connector changed no computed ball geometry. Omitting either endpoint dropped the connector during appearance parsing. Omitting the parent head did not automatically hide the attached marker. Retain rows/IDs when hiding experimental details, and check each component's visibility separately.

Preserve effective inherited Linez when introducing a breed-level section; LINE-001 materializes those rows before appending. This experiment does not establish general inheritance behavior for Linez. See [attached details](../visual-editing/attached-details.md) and [omissions](omissions.md).
