# LINE-003: connector draw order and fallback

Date: 2026-11-09. Renderer-observed Petz 4 Scottie/Siamese, with direct scheduler checks. Native-game behavior unvalidated.

Run `scratch/petz-local-venv/bin/python tools/line_order_probe.py`. Refuses overwrite. Creates six private adult-copy variants with the LINE-001 marker/connector. Existing parsed lines are serialized with all ten fields explicit, including resolved draw flags; assertions verify they remain identical in every loaded variant. This freezes existing connectors while changing the new row/global flag. Original resource safeguards apply.

| Variant | Draw Linez Before Ballz | New row column 10 | Parsed draw_after |
| --- | --- | --- | --- |
| before | 1 | 0 | false |
| after | 1 | 1 | true |
| default_before | 1 | -1 | false |
| default_after | 0 | -1 | true |
| override_before | 0 | 0 | false |
| override_after | 0 | 1 | true |

All 36 numerical loads across three poses preserve ball geometry. Direct two-endpoint schedules check both endpoint visit orders: before draws the line before the first endpoint circle; after draws it after both endpoint circles. These isolated schedules are code execution, not captured full-frame schedules. The flag controls endpoint-relative scheduling, not a universal last pass over the image.

Twenty local stdio MCP standing comparisons use yaws 0/90, seed 0, age 100, fatness 50. All four before/after pairs differ. Sixteen fallback/override equivalence pairs are pixel-identical. Four before/after sheets reviewed, spanning both species/views: after mode can cover part of the endpoint/head region that before mode leaves visible. Other sheets checked by assertions/hashes.

[Manifest](line-003.json) records flags, rows, schedules, input/output hashes and controls. Runtime/engine hashes: [RESTORE-002](restore-002.json); renderer revision 9d72d7afd5f7460ef18133c6179caaf8055082d9. Private evidence: scratch/research/line-003.

Only explicit 0/1 and fallback -1 tested, one connector style/two breeds/one rendered pose. No all-scene ordering promise, nonstandard flag values, other versions or native validation. No renderer source changes.
