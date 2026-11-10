# LINE-010: partial connector rows

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date:2026-11-10. Renderer-observed Petz4 Scottie/Siamese and code-supported resolved appearance. No native syntax/fidelity claim. [Manifest](line-010.json). Run `scratch/petz-local-venv/bin/python tools/line_partial_probe.py`; refuses overwrite. Private copies/images: scratch/research/line-010. Source/dependency/engine/original/input/PNG/cell hashes recorded; renderer unchanged at9d72d7afd5f7460ef18133c6179caaf8055082d9.

## Controls

Seven numeric prefix lengths3–9 of a ten-field connector are compared with equivalent fully resolved ten-field rows. Prefix fields after endpoints are fuzz1, fill220, left180, right200, start33, end67, edge mode1. Two global profiles: thickness25/before1 and thickness73/before0. Existing parsed lines are frozen fully, so global changes cannot change them. Head/marker colors180/200, texture-free overrides and ordinary marker size20 match prior styling controls. Seed0, age100, fatness50.

168 numerical loads (28 variants ×3 poses ×2 species) retain identical posed geometry and original lines. Every parsed connector matches its expected resolved fields. All56 local stdio MCP standing pairs at yaws0/90 are pixel-identical. Two sheets reviewed: Dogz length3/profilea/front and Catz length8/profileb/side. Equality is paired within each profile/length, not between different prefixes.

## Resolved defaults

| Supplied fields | Remaining tested defaults |
| --- | --- |
| 3: endpoints/fuzz | Fill -1; edge colors244/244; both widths from global; automatic mode0; draw flag from global |
| 4: plus fill | Edge colors244/244; widths/global, automatic mode0, global draw flag |
| 5: plus left color | Right244; widths/global, automatic mode0, global draw flag |
| 6: plus right color | Widths/global, automatic mode0, global draw flag |
| 7: plus start width33 | End width from global; automatic mode0; global draw flag |
| 8: plus end width67 | Automatic mode0; global draw flag |
| 9: plus edge mode1 | Global draw flag |

All short rows omit draw column10, confirming before1 resolves false and before0 resolves true. Length8 omits edge column9 and exercises automatic selection with positive edge colors; this adds actual omitted-column evidence to LINE-009's explicit -2 sentinel controls. A supplied start width does not copy into an omitted end width: length7 takes its end width from the global profile.

No malformed tokens, blank interior fields, comments, partial nonnumeric rows, other breeds/versions or native tests. Numeric-prefix acceptance is specific to this renderer, not permission to infer a complete native grammar.
