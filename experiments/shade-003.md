# SHADE-003: omission can change shading elsewhere

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-10. Petz4 adult Scottie/Siamese, slope100, seed0, age100, fatness50. Direct assembly/preparation with local stdio MCP comparisons. Renderer9d72d7afd5f7460ef18133c6179caaf8055082d9 unchanged. Renderer-observed/code-supported evidence only, no native-game validation. [Manifest](shade-003.json). Reproducer `scratch/petz-local-venv/bin/python tools/shade_omission_probe.py` refuses overwrite; verifier `scratch/petz-local-venv/bin/python tools/check_shade_omissions.py`. Private evidence scratch/research/shade-003; audit scratch/research/shade-003-verification.json.

The sweep independently omits each base ID0–66 across two species ×three poses ×yaw0/64 engine units:804 assembly cases. All center coordinates, radii and parked flags remain identical. Eleven omissions reduce visible depth bounds; seven change fill arrays. All793 cases preserving depth also preserve shade state and fills. Recomputing each altered case with the original depth denominator exactly restores the complete baseline ShadeState. Midpoint anchor coordinates and active-slot flags remain unchanged, so this is a bounds-driven effect in the tested fresh states.

For each of the eleven depth-changing cases, plus one visible depth-preserving control per pose/view/species, three aligned cells compare baseline, omission with fresh shading, and the same omission with original shade offsets. The third cell passes the baseline ShadeState into a fresh GeometryState; unchanged midpoint-relative distances make the update gate retain it. Ordering and prepared texture orientations match between omitted cells. Raster seed1/step0 and fresh line RNG seed1 stay fixed. This is an explicit counterfactual shade control, not an ordinary retained animation or an instruction to retain state across appearance edits.

| Species / pose / yaw degrees | Omitted ID | Depth before → after | Pixels differing only with shade substitution |
| --- | --- | --- | --- |
| Dogz standing90 |18 |81→79 |116 |
| Dogz sitting0 |62 |159→157 |79 |
| Dogz sitting90 |46 |84→81 |0 |
| Catz standing90 |9 |73→70 |58 |
| Catz standing90 |54 |73→71 |23 |
| Catz sitting0 |44 |140→136 |1 |
| Catz sitting90 |9 |83→78 |40 |
| Catz sitting90 |54 |83→81 |0 |
| Catz lying0 |48 |191→181 |35 |
| Catz lying90 |9 |64→61 |7 |
| Catz lying90 |61 |64→62 |0 |

Eight of eleven depth-changing cases change these counterfactual pixels; all twelve depth-preserving controls match. Catz sitting0 omission44 changes one pixel despite unchanged fill arrays. Fill equality alone is therefore not a complete shading-state diagnostic; no per-primitive attribution is asserted here. This does not establish support for the incomplete textured paint/Outline paths excluded by [GAP-007](../troubleshooting/rendering-gaps.md#known-incomplete-features-do-not-infer-from-mcp).

Twelve private copies include two baselines and deduplicated omission variants. Only the seed-resolved adult resource span changes; other PE resources and originals are verified. All23 local MCP baseline/omission pairs match the first two direct RGBA cells exactly (46 cross-backend cell links). Loading a real omission copy also prunes incident line rows, as expected from earlier omission research; the verifier checks that pruning and all other CoreAppearance fields. Direct composition supplies omissions to its normal line path. Its exact MCP cell agreement checks the tested equivalence.

The verifier replays804 sweep cases,23 three-cell compositions and69 indexed buffers/RGBA cells, and checks46 MCP RGBA crops, copy hashes, original boundaries and installed/checkout source/dependency/engine hashes. An initial verifier incorrectly expected only the omissions field to change after loading; it was corrected to verify incident-line pruning explicitly and then rerun. Three sheets reviewed: Dogz standing side omission18, Catz standing side omission9, and Catz sitting front omission44. The one-pixel case is established numerically rather than identified by eye.

These controls distinguish removed geometry from a consequential palette/depth effect. They do not expand semantic ball labels, versions, young resources or native behavior beyond previous evidence. See [Z Shade Slope](../format-reference/z-shade-slope.md) and [omissions](../format-reference/omissions.md).

## Equal-fill case follow-up

`tools/check_shade_equal_fill.py` isolates the Catz sitting-front omission44 one-pixel result. Only PreparedBall64's endpoint differs between fresh and held-shade preparations; circle and paint commands match. Substituting the held endpoints into the fresh omitted commands exactly reproduces held pixels; substituting paints leaves the one-pixel residual. This establishes endpoint-shade routing for this case, without identifying a particular incident connector. Four additional direct draws provide this focused control; they are outside the23 saved composition/69-buffer counts above. Private hashes/results: scratch/research/shade-003-equal-fill-attribution.json.
