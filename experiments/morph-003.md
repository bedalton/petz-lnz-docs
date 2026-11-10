# MORPH-003: multiple groups and dormant prefixes

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-10. Petz 4 Scottie/Siamese, renderer-observed/code-supported only. Native runtime and game fidelity unvalidated.

Run `scratch/petz-local-venv/bin/python tools/multiple_morph_probe.py`; refuses existing output. [Manifest](morph-003.json) records inputs, controls, offsets, geometry, transition traces, masks, twelve MCP PNG hashes, dependency versions and source/engine hashes. Private evidence: scratch/research/morph-003. Three installed evaluation/morph/attachment sources match checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9; four engine hashes match RESTORE-002. Original game files and unrelated resources remain unchanged under copy safeguards.

## Numerical setup and results

Append three ordinary-size-20 head-attached markers A/B/C, with A/C in group 14 and B in group 15. Both groups are checked unused in stock additions. Use separate area-1 and area-8 variants without new connectors, avoiding connection-derived reclassification. Static controls use group 0 for all markers or only A/C or B. Seed 0, age 100, fatness 50; standing/sitting/lying.

108 numerical cases cover two grouped variants × nine combinations of 0/50/100 for groups 14/15 × three poses × two species. Each combination checks group membership, offset/size scaling, parked state, active mask bits, prefix length and reversed update order. Both groups at 100% equal the entire static-all posed geometry. A repeated sequence 14:100→15:50→14:0→14:50→15:100 equals direct 14:50→15:100 in all twelve variant/species/pose settings.

- A and C share group 14 and receive the same percentage; B independently follows group 15.
- Reversing updates to distinct groups preserves final MorphGeometry (whose equality excludes transition traces) and final posed geometry.
- Dormant area-8 markers extend the evaluated added-ball prefix to all three appended markers even at 0%. They still remain parked, radius zero and visibility flag true. Prefix membership alone does not mean a marker is drawn.
- With area-1 markers, the prefix ends at C when group 14 is active, at B when only group 15 is active, and before the new markers when both are dormant.
- Transition histories differ for the 48 cases where both groups become positive, despite identical final geometry. For example, body-area groups at 50/50 pass through prefixes 26 versus 25 and masks 16385 versus 32769 before reaching prefix26/mask49153. These values include 23 existing additions and group0. Final pose equivalence does not establish persistent sort/shading equivalence; those layers are outside this experiment.

## MCP controls

Twelve default-state local stdio MCP standing comparisons, both species at yaw0/90. Dormant body/head variants match in all four pairs despite different evaluated prefixes. Active-A/static-all and active-B/dormant-head differ in all eight pairs. All expectations asserted. Dogz-active_a-static_all-0 and Catz-active_b-dormant_head-90 sheets reviewed at native resolution: missing B distinguishes the former, and visible B distinguishes the latter. No explicit-activation MCP pixels were generated.

Only two groups, ordinary sizes and two breeds are sampled. Relative-size behavior remains separately limited by [MORPH-002](morph-002.md)/GAP-005. Persistent ordering, shading, automatic group scheduling and native animation need separate evidence.
