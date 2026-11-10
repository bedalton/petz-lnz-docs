# MORPH-001: dormant add group versus omission

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-09. Petz 4 Scottie/Siamese renderer evidence. MCP default-state images and direct explicit-update geometry are distinct evidence paths. No native-game validation.

## Method

Run `scratch/petz-local-venv/bin/python tools/add_group_probe.py`. Refuses overwrite. Verifies group 15 is unused in the sampled effective additions. Appends a head marker with ordinary diameter 20, offset (-36,-80,0), and a 25/25 connector. Four adult-copy variants: original without marker, active group 0, dormant group 15, omitted group 0. Effective Linez preserved, source-copy/resource safeguards applied.

Direct geometry loads span standing/sitting/lying, age 100, fatness 50, seed 0. Group 15 updates at 0/25/50/100 are passed directly to evaluate_morphs and posed_geometry. Twelve local stdio MCP standing comparisons at yaw 0/90 use default state only. The MCP calls do not request explicit group percentages or demonstrate runtime animation.

[Manifest](morph-001.json) records exact rows, group state, offsets, sizes, positions and hashes. Runtime/engine provenance: [RESTORE-002](restore-002.json), renderer 9d72d7afd5f7460ef18133c6179caaf8055082d9, Python 3.12.16. Private evidence under scratch/research/morph-001.

## Results

All 24 species/pose/percentage checks pass. Default group 15 is dormant: marker parked at (20480,20480,20480), radius 0, visible flag true. Group 0 omission instead yields visible false, nonparked geometry. Both preserve rows/IDs. The dormant variant retains the connector in parsed appearance; omission removes its row during parsing. Identical images therefore do not imply identical intermediate state.

Explicit numerical updates scale this marker's local offsets and ordinary diameter: 25 → (-9,-20,0), diameter 5; 50 → (-18,-40,0), diameter 10; 100 → (-36,-80,0), diameter 20. At 100 all posed geometry equals the static group-0 active variant. At 0 it equals dormant geometry. Existing geometry remains unchanged. Ordered updates 100→0→50 yield the same final geometry as direct 50 for each species/pose; this does not compare transition histories or runtime ordering.

Eight default-state MCP equivalence pairs (original/dormant and dormant/omitted) are pixel-identical; four active/dormant pairs differ. Four sheets reviewed: Dogz active/dormant front and dormant/omitted side; Catz active/dormant side and original/dormant front. Images confirm marker/connector absent in default dormant state. Partial-activation images were not rendered.

## Limits

One unused nonzero group, ordinary size, two breeds, three numerical poses, one rendered pose/two views. No relative-size morph, multiple-group interaction, automatic game animation, native morph semantics, saved-pet state or cross-version validation. No renderer source changes.
