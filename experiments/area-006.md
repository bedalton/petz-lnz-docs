# AREA-006: omitted markers and explicit lists

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-10. Petz 4 Scottie/Siamese, renderer-observed and code-supported only. Original-game behavior remains unvalidated. No renderer changes.

Run `scratch/petz-local-venv/bin/python tools/omitted_area_lists.py`; refuses existing output. [Manifest](area-006.json) records inputs/hashes, controls, list ordering, geometry, 12 MCP comparisons, dependencies, engine hashes and evaluation-source hash. Private evidence: scratch/research/area-006. The first harness wrongly expected omitted incident lines to survive assembly; this assertion was corrected, with failed copies preserved under scratch/research/area-006-harness-failed. No renderer fix was needed. Four engine hashes match RESTORE-002; installed evaluation source matches checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9. Originals and unrelated resources remain unchanged under fixed-span copy safeguards.

## Controlled results

One static head-attached marker starts with explicit area 8 and connects to base ID 0 (effective area 3). Preserve effective stock Linez and body-area lists, then append selected marker membership. LNZ Version is explicitly 3 except the synthetic version-1 gate control. Seed 0, age 100, fatness 50; standing/sitting/lying.

| Variant | Marker omitted | Explicit lists | Format version | Final area | Visible | Head rotation changes coordinates |
| --- | --- | --- | --- | --- | --- | --- |
| visible | no | none | 3 | 3 | true | no |
| omitted | yes | none | 3 | 0 | false | no |
| omitted_body | yes | Body Balls | 3 | 1 | false | no |
| omitted_head | yes | Head Balls | 3 | 8 | false | yes |
| omitted_both | yes | Body Balls, Head Balls | 3 | 8 | false | yes |
| omitted_head_v1 | yes | Head Balls | 1 | 0 | false | no |
| visible_head | no | Head Balls | 3 | 8 | true | yes |

Forty-two variant/species/pose loads pass area, visibility and parsed incident-line checks. The omitted variants have zero incident parsed lines; visible variants retain one. Direct `posed_geometry(head_rotation=32)` records the coordinate changes above. Reclassification occurs after initial omission-derived area 0, without reversing omission. Hidden geometry can therefore respond to head rotation while the marker remains invisible. LNZ Version 1 bypasses these lists for the sampled species; this flag is not the Petz game version.

## MCP images

Twelve local stdio MCP standing front/side pairs (yaw 0/90, other controls above). Omitted versus omitted_head and omitted_head versus omitted_body are pixel-identical in all eight pairs, despite classification differences. Visible_head versus omitted_head changes pixels in all four pairs. Harness assertions enforce these expectations. Dogz-visible_head-omitted_head-0 and Catz-omitted_head-omitted_body-90 sheets were visually reviewed at native resolution: the former loses the marker/connector, the latter matches. No rendered head-rotation claim; that evidence is numerical.

Scope: two breeds in Petz 4, one attached marker. Other lists, whiskers, growth and native runtime semantics remain untested. See [body areas](../format-reference/body-areas.md), [omissions](../format-reference/omissions.md) and [AREA-003](area-003.md).
