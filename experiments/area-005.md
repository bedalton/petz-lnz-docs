# AREA-005: anchored cycles and late list overrides

Date: 2026-11-10. Petz 4 Scottie/Siamese. Code-supported and renderer-observed only; native-game fidelity remains unvalidated. No renderer changes.

Run `scratch/petz-local-venv/bin/python tools/body_area_cycles.py`; existing output is refused. [Manifest](area-005.json) records controls, source/copy hashes, semantic ID maps, geometry, image hashes, dependencies, engine hashes and installed evaluation-source hash. Private evidence: scratch/research/area-005. Four Petz 4 engine hashes match RESTORE-002, and installed evaluation source matches checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9. Copy safeguards preserve unrelated resources and bytes outside the adult LNZ span; original hashes are unchanged.

## Setup and numerical evidence

Append four static, head-attached group-0 markers A/B/C/D at fixed semantic offsets. A/B/C start at area 8 and form a triangle A–B, B–C, C–A. D starts at area 3, with C–D linking it to the cycle. Preserve effective stock Linez. Reorder Add Ball rows while remapping all new line endpoints, keeping semantic geometry fixed. Seed 0, age 100, fatness 50; standing/sitting/lying.

| Variant | Added ID order | Additional control | Final A/B/C/D areas |
| --- | --- | --- | --- |
| forward | A/B/C/D | none | 8/8/3/3 |
| reverse_ids | D/C/B/A | none | 3/3/3/3 |
| interleaved | A/C/B/D | none | 8/3/3/3 |
| reverse_lines | A/B/C/D | reverse all four new line rows | 8/8/3/3 |
| omit_anchor | D/C/B/A | omit D | 8/8/8/0 |
| late_head_list | D/C/B/A | append C to effective Head Balls, LNZ Version 3 | 3/3/8/3 |

Thirty-six numerical variant/species/pose checks pass. Another 144 marker eligibility assertions confirm that direct `posed_geometry(head_rotation=32)` changes coordinates exactly for markers finally classified as area 8. The omitted D remains geometrically unrotated in this fixture; this does not imply it is rendered.

The anchored cycle does not force a common final area. As in [AREA-004](area-004.md), ascending added-ID evaluation can leave earlier markers at area 8 while later markers acquire area 3. Reversing these four line rows does not alter this fixture; conflicting eligible areas were tested separately in [AREA-002](area-002.md).

Omitting D removes its connected influence, leaving an all-area-8 triangle. The late list control restores C to area 8 after A/B have already acquired area 3. A/B remain 3: the list override does not rerun connected propagation. This combines the ordered pass with the later list precedence tested in [AREA-003](area-003.md). It does not establish behavior for every list, arbitrary graph, or original-game runtime.

## MCP evidence and limits

Eight local stdio MCP aligned comparisons: forward versus reverse_ids, reverse_ids versus late_head_list, both species, standing at yaw 0/90, other controls above and default head rotation. Every pair has matching cell pixel hashes, asserted by the harness. Dogz-late_head_list-0 and Catz-reverse_ids-90 were visually reviewed at native resolution; pair members match and markers are visible. Rotation conclusions come from direct numerical geometry, not these default-pose images.

Only two Petz 4 breeds are sampled. No native-game, animation or cross-version claim. Remaining topics include omitted marker membership in explicit lists, other conflicting lists/whiskers, relative-size/multi-group morphs and connector styling.
