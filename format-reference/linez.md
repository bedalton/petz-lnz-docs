# Linez: connector fields

Evidence: [LINE-001](../experiments/line-001.md), Petz 4 Scottie/Siamese local renderer; native-game behavior remains unvalidated.

| Column | Parsed field | Evidence |
| --- | --- | --- |
| 1–2 | Start/end ball IDs | Base head to appended marker tested |
| 3 | Fuzz | -1/0/1/7/8 tested; clamps0–7 ([LINE-007](../experiments/line-007.md)) |
| 4 | Fill color | Explicit values and endpoint selectors -1/-2 ([LINE-005](../experiments/line-005.md)) |
| 5–6 | Left/right colors | 180/200 and negative fill inheritance tested ([LINE-006](../experiments/line-006.md)) |
| 7–8 | Start/end thickness | 0/0, 10/10, 25/25, 100/100, 100/0, 0/100 tested ([LINE-002](../experiments/line-002.md)) |
| 9 | Edge mode | -1 fill-only, 0 scan-row edges, 1 polygon-side edges; 2 no pixels in sampled controls ([LINE-006](../experiments/line-006.md)) |
| 10 | Draw after | 0/1 override; -1 follows global fallback ([LINE-003](../experiments/line-003.md)) |

The current parser accepts at least two leading numeric fields and fills omitted fields with defaults. [LINE-004](../experiments/line-004.md) exercises two-field rows through breed loading and actual local MCP comparisons; this remains implementation acceptance, not a native syntax guarantee. At revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, appearance/core.py defines the mapping; rendering/connectors.py derives each endpoint width from its thickness percentage times `min(2 * radius - 1, 127)`. [LINE-002](../experiments/line-002.md) checks this formula on explicit posed endpoints in three poses and compares actual local MCP images in front/side views. Both zero widths reject the block; otherwise each rounded endpoint width is clamped to at least 1. A zero at one end can still draw a narrow tip. Equal percentages taper when endpoint radii differ.

Adding the tested connector changed no computed ball geometry. Omitting either endpoint dropped the connector during appearance parsing. Omitting the parent head did not automatically hide the attached marker. Retain rows/IDs when hiding experimental details, and check each component's visibility separately.

Preserve effective inherited Linez when introducing a breed-level section; LINE-001 materializes those rows before appending. This experiment does not establish general inheritance behavior for Linez. See [attached details](../visual-editing/attached-details.md) and [omissions](omissions.md).

[LINE-003](../experiments/line-003.md) tests column 10 as 0 (before endpoint visits), 1 (after both endpoint visits), and -1 (global fallback). `Draw Linez Before Ballz` 1 defaults to before; 0 defaults to after. Explicit 0/1 override either global setting. This is endpoint-relative scheduling, not a promise to draw after every object in the scene. Existing line flags were frozen to isolate the comparisons.

Connections can affect body-area classification as well as pixels. [AREA-001](../experiments/area-001.md) links a head-attached marker to an ankle and observes area 8 become area 3, changing its direct head-rotation response. See [body areas](body-areas.md).

For tested two-field rows, `Default Linez Thickness` supplies both endpoint percentages. Values 25 and 100 match equivalent explicit rows; explicit row widths override global thickness. An explicitly empty thickness section falls back to 100 in LINE-004; absent-section inheritance was not tested. Other resolved defaults in that experiment are fuzz 0, fill -1, edge colors 244/244, edge mode 0, and before-endpoint scheduling with global Draw Linez Before Ballz=1.

[LINE-005](../experiments/line-005.md) isolates fill selection: -1 follows the start endpoint; -2 follows the end, including reversed endpoints, in twenty Petz4 Scottie/Siamese MCP pairs with flat diagnostic colors. Nonnegative values use explicit fill. Synthetic blocks additionally show -3 selecting the end and negative values inheriting selected endpoint texture; explicit fill bypasses texture. Shading averages endpoint offsets with truncation toward zero, then clamps within a palette band for colors10–149. Synthetic texture routing and -3 acceptance are not native syntax/fidelity claims. Edge colors remain separate and untested by this unit.

[LINE-006](../experiments/line-006.md) separates edge styles with flat fill220: modes0/1 differ from each other and from -1. Mode0 uses scan-row boundaries; mode1 strokes polygon sides. Edge colors are not anatomical sides. Negative edge colors inherit shaded fill; explicit edge colors bypass fill shading. Invalid mode2 draws no pixels in tested controls. Automatic -2 selection is tested in LINE-009.

[LINE-007](../experiments/line-007.md) tests fuzz: -1 equals0 and8 equals7; positive1/7 change the sampled MCP pixels. Isolated repeated draws reuse row-offset tables without advancing RNG after the first identical block. Other connector/whisker histories may change those tables; static repeatability is not native fidelity.

[LINE-008](../experiments/line-008.md) isolates random history in96 asset-free rasters: another positive fuzz index or a step0 whisker changes all12 target fixtures; repeat/fuzz0/step1 whisker controls match fresh. Fuzz tables share RNG with whiskers and retain generated rows. Clear pixels between operations to distinguish state effects from overdraw; fixed seed alone does not isolate changed scheduling. No composed-breed/native claim.

[LINE-009](../experiments/line-009.md) confirms automatic mode -2 selects -1 only for edge colors exactly -1/-1; positive, mixed and -2/-2 cases select0. Fully inherited flat edges can make distinct resolved modes pixel-identical. Omitted columns are subsequently sampled in LINE-010.

[LINE-010](../experiments/line-010.md) tests numeric row prefixes3–9 against full equivalents in56 MCP pairs. Omitted end width follows global thickness even when start width is supplied. Omitted edge mode resolves automatically; omitted draw flag follows the global before setting. Tested global thickness25/73 and before1/0. Malformed/interior-empty syntax and native grammar remain unvalidated.

[LINE-011](../experiments/line-011.md) extends RNG history to twelve composed Scottie/Siamese scenes: same-step1 repeats match, other-pose histories change11/12 and step0-whisker priming changes12/12. Prepared geometry/commands are fixed, prior pixels discarded, and targetstep1 held constant. Twelve fresh step0 MCP PNGs match exactly. Whole-scene differences are not connector-only attribution or native evidence.

[LINE-012](../experiments/line-012.md) attributes the whisker0-priming difference in those twelve fixed scenes: the diagnostic line alone leaves residual pixels, while substituting all positive-fuzz connector pixels reproduces the full primed scene exactly; the reverse substitution recovers fresh. Main-path RNG consumption is preserved. This is research-only state intervention, not a renderer fix or native claim.

For retained RNG behavior and isolation controls, use the focused [connector state reference](connector-state.md).

[LINE-013](../experiments/line-013.md) confirms visible inherited textures in Scottie/Siamese MCP renders: equal endpoint base color125, textured head and untextured marker; head-selected negative fill differs from explicit125, marker-selected negative fill matches it. Reversed endpoint controls agree. Actual loaded/remapped texture hashes are recorded; native fidelity remains unvalidated.

[LINE-014](../experiments/line-014.md) tests synthetic texture windows: oversized raster boxes are rejected before fuzz RNG use; fuzz margin counts toward width. Accepted windows crop centrally, with opposite odd-space bias on x/y. Period0/8 controls match; no wrapping rescues oversized connectors in this path. Actual composed-size rejection remains a separate question.

[LINE-015](../experiments/line-015.md) corroborates texture-size rejection in actual breed scenes: long offset -800 with inherited256x256 head texture equals marker-only, while explicit125 still draws; short -80 controls draw both styles. Parsed line/block survive. This is a renderer limitation with native behavior unvalidated.

[LINE-016](../experiments/line-016.md) repeats the five texture-routing controls in Petz3/5: sixty numerical loads and32 MCP pairs match Petz4 block/texture records and PNGs. This narrowly broadens texture-routing evidence; size rejection and RNG histories remain Petz4-only breed samples.

For texture selection, crop/size limits and disappearing-line controls, use the focused [connector texture reference](connector-textures.md).
