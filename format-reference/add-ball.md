# Add Ball: initial row and attachment reference

Status: Petz 4 renderer-observed in a synthetic head detail, plus code-supported field layout. [ADD-001](../experiments/add-001.md). Full native-game semantics remain unverified.

A row begins with the **parent/base ID**, not its own new ID. Added IDs are assigned by row order after the base-ball table. With 67 base balls, first added ID is 67. Append rather than insert unless updating every affected reference. ADD-001's marker was 90 only because those particular files already had 23 addballs.

| Column (1-based) | Parsed field | Current evidence |
| --- | --- | --- |
| 1 | Base ball | Marker follows head; offsets rotate using base frame rotations |
| 2–4 | X, Y, Z offset | Local raw units, not final screen pixels |
| 5 | Color | 125 used as diagnostic marker color |
| 6 | Outline color | 244 used; styling modes not explored here |
| 7 | Speckle color | -1 used; renderer warns speckles are not drawn |
| 8 | Fuzz | 0 used |
| 9 | Color group | -1 used; inheritance/painting semantics untested |
| 10 | Outline mode | -1 used |
| 11 | Size | Ordinary diameter; optional size reference changes radius calculation |
| 12 | Body area | 0 inherits base area in this renderer; not a color group |
| 13 | Add group | 0 is active in default renderer state; other groups need morph tests |
| 14 (optional) | Texture index | -1 used (untextured) |
| 15 (optional) | Size-base-ball ID | -1 means no reference; head reference tested |

The current parser requires at least 13 numeric values and defaults optional fields to -1. This is an implementation acceptance rule, not established native syntax for every game.

## Scaling and hiding

An ordinary head-attached marker did **not** automatically grow or stretch away from its parent when the first Head Enlargement value increased. Head position itself is the enlargement center. Body-area membership does not by itself establish ornament scaling.

With a valid size-base-ball ID, rendering/attachment.py computes radius as `(size * ball_scale >> 8) + referenced_ball.radius`, then clamps it. This differs from ordinary addball diameter scaling, which uses a shift by 9. ADD-001 used size=-8 relative to the head and observed matching radius growth. Keep this distinction and clamping in mind; do not convert that row into a general pixel-size promise.

To hide a detail, append its ID to Omissions. In the tested unconnected marker this preserved its row, ID and computed dimensions while hiding it. [LINE-001](../experiments/line-001.md) tests a head-to-marker connector: omitting either endpoint removes it; omitting the parent does not hide the marker. Groups and morphs still need separate investigation.

Source revision: 9d72d7afd5f7460ef18133c6179caaf8055082d9; appearance/core.py, appearance/evaluation.py, rendering/attachment.py and rendering/morphs.py. Only a subset of these fields has controlled visual tests.
