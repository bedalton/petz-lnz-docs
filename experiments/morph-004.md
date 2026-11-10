# MORPH-004: retained assembly history

Date: 2026-11-10. Asset-backed numerical renderer evidence in Petz 4 Scottie/Siamese. No new MCP images, pixel claims or native-game validation. No renderer changes.

Run `scratch/petz-local-venv/bin/python tools/morph_history_probe.py`; refuses existing output. Reuses hash-verified private [MORPH-003](morph-003.md) body/head variants without changing them. [Manifest](morph-004.json) records sixty history comparisons, changed draw-order positions, final markers, snapshot hashes, six installed source hashes and four engine hashes. Full snapshots remain private in scratch/research/morph-004/report.json. The initial successful run is archived under scratch/research/morph-004-initial; the final run adds repeated-frame controls and a compact public manifest. Engine hashes match RESTORE-002 and installed sources match checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9. Original/copy input hashes verified.

## Controls

Use groups14/15 and three markers from MORPH-003: A/C share14 and B uses15, with separate body-area1/head-area8 variants. Two species × two variants × three poses × five histories = sixty history cases. Seed0, age100, fatness50, default head rotation.

Every history ends at group14=50, group15=50:

| History | Updates |
| --- | --- |
| a_then_b | 14:50,15:50 |
| b_then_a | 15:50,14:50 |
| cycle | 14:100,15:100,14:0,14:50,15:50 |
| noops | 14:50,14:50,15:50,15:50 |
| unused | 13:100,14:50,15:50; group13 verified unused |

For each, compare fresh `assemble_geometry` with the complete history against assembly of the initial state followed by every intermediate prefix with retained state. This explicitly varies frame sampling/history, not just final amounts. Assembly computes ordering and shading but does not produce circles, overlays or pixels.

## Results

All sixty cases have identical batch/incremental ball geometry and bounds. All have identical final fills and shade offsets. Batch no-op/unused histories equal batch a_then_b snapshots in all twelve fixture settings. Another identical retained frame preserves balls/fills in all sixty cases. Non-prefix retained histories are rejected in all sixty checks, as required by the assembly API.

| History | Different final draw/sorted order (of 12) | Different fills | Different stored shade distances |
| --- | --- | --- | --- |
| a_then_b | 9 | 0 | 0 |
| b_then_a | 8 | 0 | 0 |
| cycle | 12 | 0 | 12 |
| noops | 9 | 0 | 0 |
| unused | 9 | 0 | 0 |

Forty-seven of sixty batch/incremental cases differ in draw and sorted order despite equal final geometry. Six of twelve retained a_then_b/b_then_a fixture pairs have different draw orders. This narrows MORPH-003's commutativity finding to final evaluated/posed geometry; it cannot be extended to persistent assembly ordering.

A baseline repeated frame without morph updates also changes draw order in two of twelve controls (Dogz sitting in both variants), while balls/fills match. Do not attribute every ordering difference solely to morph transitions. Code retains prior depth ordering, uses a reset-dependent sorting threshold and applies forced feature ordering, all of which can make frame sampling matter. The experiment records effects, not a native correctness judgment.

The cycle history retains different shading distance caches in all twelve cases while current shade offsets/fills still match. Equal present fills therefore do not establish identical future state. No claim that these sampled order/cache differences alter PNG pixels; visual occlusion and later movement are separate tests. No native-game or automatic animation claim.
