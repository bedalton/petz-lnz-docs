# Body areas for added details

Evidence: [AREA-001](../experiments/area-001.md), Petz 4 Scottie/Siamese renderer geometry and default-pose MCP comparisons. Native-game semantics remain unvalidated.

Add Ball column 12 is body area. In the tested marker, 0 inherits the parent head's area 8. A Linez connection from the marker to effective ankle area 3 reassigns the marker to area 3. Explicit 8 is also reassigned; explicit 1 remains 1. Omitting the ankle removes the connecting row and restores inherited head area. Omitting the marker yields area 0 in these controls.

This classification affects head-rotation eligibility: direct head_rotation=32 changes this marker in area-8 variants, but not in sampled area-3/1/0 variants. Default-head-pose images alone did not reveal the difference. A cosmetic connector can therefore change more than visible pixels.

Code at revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, appearance/evaluation.py, initializes species tables, inherits/adds areas, processes eligible connected neighbors for area 8, then applies later lists and whisker handling. Only the narrow outcomes above have controlled tests. Multiple-neighbor precedence and body-area-list overrides need dedicated experiments.

Inspect effective breed areas rather than assuming species-table values: sampled Siamese ID 0 resolves to area 3 although the built-in Catz table has 2. This is an implementation/breed observation, not a universal species mapping. See [add fields](add-ball.md), [Linez](linez.md) and [groups](add-groups.md).
