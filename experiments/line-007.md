# LINE-007: connector fuzz bounds and repeated draws

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-10. [Manifest](line-007.json). Renderer-observed Petz4 Scottie/Siamese plus code-supported isolated raster controls. No native validation or renderer changes. Run `scratch/petz-local-venv/bin/python tools/line_fuzz_probe.py`; refuses overwrite. Private evidence: scratch/research/line-007. Manifest records renderer revision, installed/checkout hashes, dependencies, source/copy hashes and resource DLL hashes; pose asset hashes remain in private MCP metadata.

Five fuzz fields -1/0/1/7/8 are tested with fixed connector fill220, edges180/200, mode0, widths100/100 and draw_after1. All original lines are frozen. Thirty numerical variant/pose loads across Scottie/Siamese standing/sitting/lying preserve geometry and original lines. Sixteen local stdio MCP standing comparisons at yaws0/90, seed0, age100, fatness50 pass: -1 equals0; 8 equals7; 1 and7 each differ from0. Two sheets reviewed (Dogz0/7 front, Catz0/1 side).

Forty isolated raster fixtures cross four endpoint orientations and two width pairs with five fuzz values. Fuzz clamps to0–7. A fresh LineRenderer(seed1) reproduces the first draw. Drawing the same block a second time with the same renderer also preserves pixels, RNG state and tables: fuzz offsets are cached by clamped fuzz index and row, rather than regenerated for every static frame. Fuzz0 consumes no RNG; positive fuzz creates a nonempty cached table. This does not establish stability when connector height, previous draws, whiskers or animation changes.

The low/high boundary of each raster row receives the same random horizontal offset in this implementation; fuzz is not independent noise at every edge pixel. Raster placement includes clipping/margin calculations, so do not infer a general visual equivalence for unrelated widths or views.

Broader random-history interactions, other breeds/versions and native-game behavior remain untested. The synthetic fixtures bypass breed assembly and palette conversion. Existing game files are unchanged.
