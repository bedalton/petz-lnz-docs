# AREA-002: conflicting neighbor precedence

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-09. Petz 4 Scottie/Siamese only. Code-supported and renderer-observed results; no native-game validation.

Run `scratch/petz-local-venv/bin/python tools/body_area_neighbors.py`. The script refuses an existing output directory. Private copies, responses and PNGs are under scratch/research/area-002. [Manifest](area-002.json) records original/copy hashes, controls, geometry, engine hashes, dependency versions and the installed evaluation-source hash (checked against the renderer checkout). No renderer changes. Existing effective Linez rows are preserved and fixed-span resource-copy safeguards apply.

Four head-attached added neighbors use explicit areas 1, 3, 4 and 8; a fifth marker uses explicit area 8. Six variants vary the order of marker-to-neighbor rows, reverse endpoint direction, omit the first eligible neighbor or use only ignored neighbors. These are synthetic added neighbors, not an atlas of native body-region names.

## Numerical results

Thirty-six variant/species/pose checks pass across standing, sitting and lying, seed 0, age 100 and fatness 50:

| Neighbor row order / control | Marker area |
| --- | --- |
| 3 then 4 | 3 |
| 4 then 3 | 4 |
| 3 then 4, endpoint direction reversed | 3 |
| 1 then 8 then 4 then 3 | 4 |
| 3 then 4, area-3 neighbor omitted | 4 |
| 1 then 8 only | 8 |

At this revision, the evaluator walks each marker's neighbor list in reverse and repeatedly replaces the candidate with any area outside 1/8. Consequently the first eligible Linez row wins in these isolated controls. Areas 1 and 8 are skipped. Endpoint orientation does not alter the result. Omitting a neighbor removes that connection from consideration. This supports row-order dependence for these fixtures, not a universal graph-resolution rule: chains, cycles and later body-area-list overrides remain untested.

Direct `posed_geometry(head_rotation=32)` changes the target marker's coordinates only in the area-8 variant in all three poses. The source evaluator's internal order is code evidence; these numerical calls observe that implementation, independently of image visibility.

## MCP image controls

Eight local stdio MCP comparisons use standing, yaw 0/90, seed 0, age 100, fatness 50 and default head rotation. Compare 3→4 against 4→3, and against reversed endpoints, in both species. All pair members have identical pixel hashes despite different area classification in the first comparison. Dogz front and Catz side row-order sheets were visually reviewed at native resolution: identical pair members with added markers and narrow connectors. Other sheets were checked by hashes.

Default-pose pixel equality does not establish equivalence during head movement. MCP did not receive a head-rotation request; the rotation finding above is numerical only. This expands [AREA-001](area-001.md); other breeds, versions, multiple connected added-ball chains, explicit body-area-list precedence and original-game behavior remain open.
