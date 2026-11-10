# LINE-004: short rows and default thickness

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-09. Renderer-observed Petz 4 Scottie/Siamese; no native syntax/fidelity claim.

Run `scratch/petz-local-venv/bin/python tools/line_defaults_probe.py`. Refuses overwrite. Appends the diagnostic head marker from LINE-001. Existing parsed lines are serialized fully to freeze their resolved style; numerical assertions verify they remain identical. Only the new connector consumes the tested global thickness defaults. Copy/resource safeguards preserve originals.

Controls: short row containing only start/end IDs at Default Linez Thickness 25 or 100; equivalent full ten-field rows; explicit 25/25 with global 100; and a short row with an explicitly empty Default Linez Thickness section. Global Draw Linez Before Ballz is 1 throughout. An empty section deliberately overrides inherited values; absent-section inheritance is not tested.

Thirty-six numerical variant/pose checks across standing/sitting/lying confirm short rows resolve to fuzz 0, fill -1, left/right 244, edge mode 0, draw_after false, and both endpoint percentages from the global value. Empty thickness resolves to 100. Explicit row thickness 25/25 wins over global 100. Ball geometry and frozen existing lines remain unchanged. Direct connector-block checks also pass, using flat-color posed endpoints as in LINE-002; these are not camera-derived raster measurements.

All sixteen local stdio MCP standing comparisons at yaws 0/90, seed 0, age 100, fatness 50 are pixel-identical within their equivalence pairs. Two sheets reviewed (Dogz short25/full25 front, Catz empty100/full100 side); other sheets checked by hashes. This establishes tested implementation acceptance of two-field rows, not native syntax for every game/version.

[Manifest](line-004.json) records exact row forms, expected widths, input/output hashes and controls. Global settings are defined in the reproducer and above. Runtime/engine provenance: [RESTORE-002](restore-002.json); renderer 9d72d7afd5f7460ef18133c6179caaf8055082d9. Private evidence under scratch/research/line-004.

No partial rows of lengths 3–9, malformed tokens, absent-section inheritance, other global values, other breeds/versions or native tests. No renderer source changes.
