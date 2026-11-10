# LINE-013: asset-backed connector textures

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date:2026-11-10. Renderer-observed Petz4 Scottie/Siamese; no native-game validation. [Manifest](line-013.json). Reproducer `scratch/petz-local-venv/bin/python tools/line_texture_probe.py` refuses overwrite. Private evidence scratch/research/line-013. No renderer changes; revision9d72d7afd5f7460ef18133c6179caaf8055082d9, installed/checkout source hashes, dependencies, resource DLL hashes, original/copy and PNG/cell hashes recorded.

Both head and marker have base color125. The head retains its stock texture slot (Scottie1, Siamese0); the marker has texture -1. Connector fuzz0, edges244/244, widths100/100, edge mode0 and draw_after1 are fixed. Existing parsed Linez rows are frozen and checked unchanged. Seed0, age100, fatness50; three numerical poses, standing MCP yaws0/90.

Thirty numerical loads verify unchanged posed geometry and existing lines. Negative fill selecting the head yields a texture paint equal to remapping that endpoint's loaded stock tiled texture at the connector's shaded color. Negative fill selecting the untextured marker and explicit fill125 yield no paint. Original and remapped texture pixel hashes are recorded; no stock texture pixels are committed.

Sixteen local stdio MCP pairs pass: head-selected -1 differs from explicit125 in all four species/view cases; marker-selected -2 equals explicit125; reversed -2 selecting the head equals forward -1; reversed -1 selecting the marker equals explicit125. Thus the tested inherited texture changes visible connector pixels even with equal endpoint base colors. Endpoint reversal equality is specific to these symmetric-edge, zero-fuzz controls. Two sheets reviewed: Dogz inherited/explicit front and Catz reversed/forward head texture side.

This extends LINE-005's synthetic routing evidence to actual loaded breed textures and MCP images. It does not validate other texture entries, growth, negative color -3, other breeds/versions or native-game behavior. Long connectors, tile-size limits and texture sampling details remain pending.
