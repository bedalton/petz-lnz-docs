# LINE-006: connector edge colors and modes

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-10. Code-supported isolated raster checks and renderer-observed Petz4 Scottie/Siamese; no native validation. [Manifest](line-006.json). Reproducer: `scratch/petz-local-venv/bin/python tools/line_edge_probe.py`; refuses overwrite. Private evidence: scratch/research/line-006. Renderer revision9d72d7afd5f7460ef18133c6179caaf8055082d9; installed/checkout source hashes, dependencies, original/copy hashes and resource DLL hashes recorded. No renderer modifications.

## Controls

Reuses LINE-005 head/marker diagnostic colors180/200 and texture-free overrides. Connector fill220 lies outside shadeable palette bands. Widths100/100, fuzz0 and draw_after1 fixed; existing lines frozen and checked unchanged. **42 numerical variant/pose loads**: seven variants, three poses, two species. All posed geometry matches the marker-only control.

Twenty local stdio MCP comparisons, standing yaws0/90, seed0, age100, fatness50, pass. Modes0 and1 each differ from -1, and from each other, with edge colors180/200. Negative edge colors -1/-1 equal explicit fill220/220 in mode0. Edge mode2 equals marker-only: the connector produces no visible pixels in these samples. Two sheets reviewed: Dogz mode0/1 front and Catz mode2/marker side. No broad native invalid-mode claim.

## Code and isolated raster evidence

48 isolated raster fixtures use four endpoint orientations (including reversal, horizontal and vertical), two width pairs12/12 and20/6, and six styles. Pixel counts and indexed hashes recorded. Mode -1 draws fill without edge colors. Mode0 colors scan-row low/high x boundaries; rows at most two pixels wide take the left color. Mode1 fills then strokes the two connector polygon sides, so “left/right” does not universally mean anatomical left/right. Mode2 returns without drawing. Negative edge colors use the fill. Assertions verify edge colors appear in modes0/1, disappear in plain/inherited-fill cases, and inherited/explicit220/plain outputs match.

These fixtures bypass breed assembly/camera/palette conversion; mode semantics are code-supported plus narrow MCP pixel comparisons, not a complete raster specification.

## Corrections and limits

An initial harness referenced an obsolete variant name; archived privately. A second attempt used fill125 and expected negative edges to equal explicit125. It failed because connector fill receives depth shading while explicit edge colors do not. That private failed case is preserved; the final unit isolates modes using fill220. Negative edges inherit the already shaded fill in current code, not necessarily the literal fill field.

Fuzz, automatic default edge selection(-2), asymmetric shading/texture combinations, other breeds/versions and native behavior remain pending. All source game files unchanged.
