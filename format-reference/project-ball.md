# Project Ball

Evidence: code-supported renderer behavior at revision 9d72d7afd5f7460ef18133c6179caaf8055082d9; [PROJECT-001](../experiments/project-001.md) supplies synthetic numerical checks. [PROJECT-002](../experiments/project-002.md) adds Petz 4 Scottie/Siamese geometry and local MCP comparisons; native semantics remain unvalidated.

Rows are read as `start end percent`. The current renderer scales the end position relative to start: 100 preserves its distance, 0 collapses it onto start, 50 halves it, and negative values cross to the opposite side. Integer truncation and signed 16-bit wrapping apply. This changes coordinates, not ball radius.

Rows run sequentially after Move. A later row sees positions changed by earlier rows, so ordering and repeated entries matter. Out-of-frame indices are ignored by the position stage. The synthetic probe does not establish how added-ball IDs behave through the full pipeline.

For actual editing, preserve inherited rows and use [copy-only controls](../agent-guides/start.md). Species-specific shapes, age interpolation and valid anatomy IDs require separate checks. Earlier downstream effects are recorded in [MOVE-001](../experiments/move-001.md).

In those sampled breeds, a single head-to-nose row at 50/150 changes only the nose raw position in standing/sitting/lying; 100 matches an explicit empty-projection control. Front/side images show localized nose movement. This is not a coherent muzzle extension recipe. The experiment deliberately replaces inherited projection rows to isolate the field.

[PROJECT-003](../experiments/project-003.md) repeats these isolated controls with Petz 3 and 5 engine resources. Sampled raw geometry and comparison PNG hashes match Petz 4 for both breeds. This cross-version evidence applies only to the tested controls; native behavior remains unvalidated.

[PROJECT-004](../experiments/project-004.md) repeats the isolated head-to-nose controls in Petz 4 Dalmatian/Persian, with the same position assertions and identity/image-change outcomes. Two breeds per species are now sampled; other anatomy and growth remain untested.
