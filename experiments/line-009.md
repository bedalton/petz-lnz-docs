# LINE-009: automatic connector edge mode

Date: 2026-11-10. Code-supported resolved appearance and renderer-observed Petz4 Scottie/Siamese; no native validation. [Manifest](line-009.json). Run `scratch/petz-local-venv/bin/python tools/line_auto_edge_probe.py`; refuses overwrite. Private evidence scratch/research/line-009. Uses explicit ten-field rows with edge-mode sentinel -2, not omitted columns.

48 numerical loads (eight variants, three poses, two species) confirm that mode -2 resolves to -1 only when both edge colors are exactly -1. Colors180/200, mixed -1/200 and -2/-2 resolve to mode0. Explicit modes -1/0 remain as supplied. Thus arbitrary negative edge colors do not all select fill-only mode automatically, although they inherit fill during rasterization. Geometry and all frozen existing lines remain unchanged.

Twenty local stdio MCP standing comparisons at yaws0/90, seed0, age100, fatness50 are equal in their expected pairs: automatic -1/-1 versus explicit plain; automatic180/200 versus explicit mode0; automatic mixed colors versus explicit mode0; automatic -2/-2 versus explicit mode0 with -1/-1; automatic -1/-1 versus explicit mode0 with -1/-1. The last pair is an identifiability control: different resolved edge modes can have equal pixels when all edges inherit the flat fill220. Pixel equality alone cannot establish mode selection.

Head/marker colors180/200 and texture-free overrides, widths100/100, fuzz0 and draw_after1 reuse LINE-006 controls. Two sheets reviewed: Dogz automatic-colored/explicit front and Catz automatic-plain/forced-scan side. Source/dependency/engine/original/copy and PNG/cell hashes are recorded. No renderer changes. No synthetic raster fixtures are claimed for this unit.

Omitted-column parsing, partial rows, other negative combinations, other breeds/versions and native syntax/fidelity remain untested. Parser source supplies -2 as the omitted edge-mode default, but that is a code-supported lead rather than an omitted-row MCP experiment.
