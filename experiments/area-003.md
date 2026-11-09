# AREA-003: body-area-list precedence

Date: 2026-11-09. Petz 4 Scottie/Siamese, code-supported and renderer-observed only. Original-game behavior unvalidated.

Run `scratch/petz-local-venv/bin/python tools/body_area_lists.py`. Refuses existing output. Copies/images/responses remain private under scratch/research/area-003. [Manifest](area-003.json) records six variants, serialized list-section ordering, original/copy hashes, geometry, controls, dependency versions, engine hashes and installed evaluation-source hash. Four Petz 4 engine hashes match RESTORE-002; installed evaluation source matches checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9. No renderer changes.

## Controlled setup

Append one group-0 head-attached marker with explicit area 8 and a Linez connection to base ID 0. Its control connection-derived area is 3. Preserve effective existing Linez and every effective body-area list explicitly; append the marker to selected lists. Copy safeguards verify other resources and bytes outside the adult LNZ span are unchanged; original hashes are checked after preparation.

Main variants explicitly use `Lnz Version` 3. This field is an LNZ format flag, not the Petz game version. A synthetic version-1 control changes the global flag: it tests the implementation gate, not isolated equivalence of the whole appearance or native Petz 1 compatibility.

## Numerical results

Thirty-six checks pass: six variants × two species × standing/sitting/lying. Seed 0, age 100, fatness 50.

| Variant | Lnz Version | Marker lists | Resolved area |
| --- | --- | --- | --- |
| linked | 3 | none | 3 |
| body | 3 | Body Balls | 1 |
| head | 3 | Head Balls | 8 |
| both | 3 | Body Balls then Head Balls | 8 |
| both_reversed | 3 | Head Balls then Body Balls | 8 |
| version1_head | 1 | Head Balls | 3 |

Body-area-list membership overrides connection-derived classification in the version-3 fixtures. Conflicting membership resolves by the evaluator's fixed area-index order: Head Balls (8) wins over Body Balls (1), regardless of their textual section order. This is different from connection-row precedence in [AREA-002](area-002.md). It does not establish precedence among every possible list.

Code evaluates these lists when species is 0 or LNZ version is greater than 1. The sampled species are Dogz/Catz, not species 0. The version-1 control observes the lists being bypassed and the connected marker staying in area 3; species-0 and other version values were not tested.

Direct `posed_geometry(head_rotation=32)` changes the marker's coordinates in all area-8 variants and no others, in all three poses. This is numerical renderer evidence, separate from MCP rendering. No animation or original-game claims.

## MCP image controls

Eight local stdio MCP comparisons: linked versus head, and both versus both_reversed; two species at yaw 0/90, standing, seed 0, age 100, fatness 50, default head rotation. All pair members are pixel-identical, including the linked/head pair with different classifications. Dogz linked/head front and Catz both/both_reversed side sheets visually reviewed at native resolution; other sheets checked by hashes. Default-pose equality does not imply equivalent head-motion behavior.

Remaining: added-ball chains/cycles, other list conflicts and whisker precedence, omitted markers reassigned by lists, more breeds/versions, native validation. References: [body areas](../format-reference/body-areas.md), [AREA-001](area-001.md), [AREA-002](area-002.md).
