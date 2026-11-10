# LINE-005: connector fill and endpoint selection

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-10. Code-supported synthetic blocks and renderer-observed Petz 4 Scottie/Siamese; no native-game validation.

Run `scratch/petz-local-venv/bin/python tools/line_color_probe.py`. Refuses overwrite. Private copies and pixels: scratch/research/line-005. [Manifest](line-005.json) records input/PNG/cell hashes, installed/checkout source hashes, dependencies and three resource DLL hashes. Animation BHD/BDT hashes are in the private MCP metadata. Renderer revision: 9d72d7afd5f7460ef18133c6179caaf8055082d9. No renderer changes.

## Controls and results

The head is set to diagnostic color180, texture -1 via Color Info Override; its attached marker has color200, texture -1. Both colors lie outside the shadeable10–149 interval. Existing Linez rows are frozen in full, and assertions retain them unchanged. Added connector widths100/100, fuzz0, edges244/244, edge mode0 and draw_after1 stay fixed. Seed0, age100, fatness50; standing MCP yaws0/90. Thirty-six numerical variant/pose loads across standing/sitting/lying retain identical posed geometry.

Twenty local stdio MCP pairs pass: sixteen equivalence comparisons and four differing-color comparisons. Fill -1 matches explicit start color180; fill -2 matches explicit end color200. Reversing endpoints makes -1 match explicit200 and -2 match explicit180. Start-selected versus end-selected fills differ in both views/species. Two sheets visually reviewed: Dogz start/end front shows the fill change; Catz reversed-start/explicit-end side shows equality. Endpoint reversal equality is specific to these flat-color, equal-percentage, symmetric-edge controls, not a general geometric guarantee.

72 synthetic block cases independently cover fields -3/-2/-1/0/125/200, reversed endpoints, three shade-offset pairs and texture present/absent. Exactly -1 selects the start endpoint; other tested negatives select the end. Nonnegative colors bypass endpoint texture. Negative fields inherit selected endpoint texture in these shadeable-color cases. Fill shade uses the endpoint-offset average truncated toward zero and clamps within the selected ten-color band. These synthetic fixtures bypass camera, assembly and rasterization; they establish block construction only. The -3 case has no MCP/native syntax claim.

## Limits and harness corrections

An initial run completed pixels but failed reporting because the package distribution was named incorrectly. A duplicate initial invocation was also archived privately. Final rerun uses petz-renderer-mcp metadata and removes an unsupported Texture Override section, replacing it with the supported four-field Color Info Override. Only final evidence is counted. Original files stay unchanged; fixed-span resource-copy safeguards pass.

Texture routing is synthetic only, not a demonstration of textured breed connectors. Edge colors/modes, fuzz, other breeds/versions and native semantics remain pending.
