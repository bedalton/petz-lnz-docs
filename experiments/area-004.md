# AREA-004: connected chains and evaluation order

Date: 2026-11-10. Petz 4 Scottie/Siamese. Code-supported and renderer-observed; native-game fidelity unvalidated. No renderer modifications.

Reproduce with `scratch/petz-local-venv/bin/python tools/body_area_chains.py`; refuses an existing output directory. [Manifest](area-004.json) records inputs, controls, numerical geometry, eight MCP image hashes, dependencies, engine hashes and evaluation-source hash. Private copies, PNGs and responses: scratch/research/area-004. Installed evaluation source matches checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9; four engine hashes match RESTORE-002. Original breed hashes remain unchanged, and copy safeguards check unrelated resources and bytes outside the adult LNZ span.

## Controls and results

Append three static group-0 head-attached markers, A/B/C, at fixed semantic positions. A/B start in area 8; C starts in area 3 except in the all-area-8 cycle control. Preserve effective stock Linez, then append A–B and B–C connections. Reversing added-row order remaps every connector endpoint to retain the same semantic geometry. Seed 0, age 100, fatness 50; numerical standing/sitting/lying checks.

| Variant | Added ID order | Added links in row order | Final A/B/C areas |
| --- | --- | --- | --- |
| forward | A/B/C | A–B, B–C | 8/3/3 |
| reverse_ids | C/B/A | A–B, B–C | 3/3/3 |
| reverse_lines | A/B/C | B–C, A–B | 8/3/3 |
| cycle | A/B/C | A–B, B–C, C–A | 8/8/8 |

Twenty-four variant/species/pose loads pass. Direct `posed_geometry(head_rotation=32)` changes coordinates exactly for the markers classified as area 8 (72 marker eligibility assertions). Geometry and classifications are recorded separately from MCP pixels.

The evaluator visits added IDs once in ascending order and reads mutable current neighbor areas. In forward order A sees B still at 8; B subsequently sees C at 3. It does not revisit A. In reverse order B acquires 3 before A is visited, so the classification reaches A. This is an ordered pass, rather than iteration until every linked head marker acquires area 3. Reversing these two line rows does not affect this fixture; this does not supersede first-eligible-neighbor precedence when a marker has conflicting eligible neighbors ([AREA-002](area-002.md)). The all-8 cycle stays 8; anchored cycles and longer chains remain untested.

## Images and service

The existing loopback HTTP MCP at http://127.0.0.1:8765/mcp passed real FastMCP tool discovery and get_capabilities. No replacement was needed. The research harness uses its own local stdio MCP with a restricted private asset root.

Eight aligned standing comparisons: forward versus reverse_ids and forward versus reverse_lines, both species, yaw 0/90, other controls above. All cell pixel hashes match despite forward/reverse_ids classification differences. Default-head-pose images therefore conceal this effect. Dogz-reverse_ids-90 and Catz-reverse_lines-0 sheets were visually reviewed at native resolution: matching pair members with added markers visible. These are comparison-sheet reviews, not independent anatomy validation or rendered head-rotation evidence.

Scope remains two breeds in Petz 4. No claims about original-game propagation, all possible cycles, other list interactions, animations or other game versions.
