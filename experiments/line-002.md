# LINE-002: endpoint thickness sweep

Date: 2026-11-09. Renderer-observed Petz 4 Scottie/Siamese; direct connector-block checks supplement real local MCP images. No native-game validation.

## Reproduce and controls

Run `scratch/petz-local-venv/bin/python tools/line_width_probe.py`. Refuses an existing output directory. Copies the adult resource using fixed-span safeguards and appends the same diagnostic marker as LINE-001. Preserves effective Linez rows. Sweeps start/end percentages 0/0, 10/10, 25/25, 100/100, 100/0 and 0/100, each against a marker-only control. Draw-after 1, fill 125, edges 244, fuzz 0, edge mode 0.

Thirty-six numerical cases cover three poses/species/six widths. All variants preserve ball geometry. Direct build_line_block calls use posed geometry with explicit flat color 125 and default shading, without camera transforms; they are block-construction checks, not measurements extracted from the MCP raster. Twenty-four standing MCP comparisons span yaw 0/90, seed 0, age 100, fatness 50. [Manifest](line-002.json) records rows, controls, radii, preclamp/block widths and hashes. Runtime/engine provenance: [RESTORE-002](restore-002.json). Private evidence under scratch/research/line-002.

## Findings

Four zero/zero image pairs equal the marker-only control; all twenty other pairs differ. Zero/zero keeps the parsed row but rejects its raster block. If only one endpoint width rounds to zero, the accepted block clamps that endpoint to 1. Thus a zero endpoint is not the same as disabling the whole connector.

Standing direct-check radii are head 22, marker 5 (Dogz) or 4 (Catz). At 100/100 the block widths are 43/9 or 43/7; at 10/10 they are 4/1 for both species, with the marker endpoint rounding from zero before clamping. 25/25 yields 10/2 or 10/1. 100/0 yields 43/1, and 0/100 yields 1/9 or 1/7. All three-pose checks match the percentage formula and clamping.

Six sheets visually reviewed: Dogz thin-front, quarter-front, taper-side, reverse-side; Catz thin-side and full-side. Smaller percentages narrow the filled connector. Equal percentages do not imply equal absolute width. Reversing the zero endpoint reverses which end stays narrow. Other sheets checked by assertions/hashes.

## Limits

Only two breeds, adult Petz 4, zero fuzz, one color/edge mode/draw order. No negative/>100 width sweep, radius-cap boundary, camera-derived block inspection, other species/version or native validation. No renderer source changes. See [LINE-001](line-001.md) for omission behavior.
