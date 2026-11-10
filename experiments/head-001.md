# HEAD-001: separate head radius and feature spacing

**Renderer recovery review:** [UPDATE-004](update-004.md) confirms the recovered comparison/visibility outcomes on6c1d883. Measurements below are historical except the explicitly corrected Catz omission union count.

Date: 2026-11-09. Status: renderer-observed/code-supported, not game-validated. Petz 4 Scottie and Siamese.

## Procedure

Run `scratch/petz-local-venv/bin/python tools/head_shape_probe.py`. Same environment and renderer revision as SMOKE-001. Private outputs are under scratch/research/head-001; [tracked manifest](head-001.json) records inputs, controls, hashes and changed-ball summaries. Full raw coordinates and radii stay private.

Starting from resolved private copies, independently increase the first or second Head Enlargement value by 25. Controls are Scottie (103, 0) and Siamese (105, 0), where each pair is stored as two separate LNZ rows. No other effective sections change. Fixed-span safeguards check unrelated resource bytes. Numerical inspection loads standing, sitting and lying for all three variants per species, with seed 0, adult age 100 and fatness 50. Eight local MCP aligned comparisons cover each edited variant against control at standing yaw 0° and 90°.

## Results

- Increasing either value by 25 produces identical radius arrays between the two edited variants, for every ball in all three inspected poses. This equality is asserted.
- Their position arrays differ: the first value spreads head-area feature centers around the head center, while the second brings them inward for these tested pairs. Head base centers stay fixed during this shape operation; other processing still applies afterward.
- In all three poses, 27 Dogz and 25 Catz base-ball centers change versus control. Radius changes occur on 26 Dogz and 16 Catz base balls. These counts are specific to the selected increments and integer rounding, not definitive membership lists.
- The side-view dog comparisons and front-view cat comparisons were visually reviewed. First-value increases produce larger, more spread-out head features. Second-value increases create a crowded face despite equally enlarged ball radii.

This explains why a single generic head-size slider is insufficient for precise design. Uniformly changing one base ball differs again: see BALL-001.

## Implementation interpretation

At revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, rendering/sizing.py multiplies head-area animation base diameters by (A+B)/100, before frame/static/fatness adjustments, integer rounding and final radius limits. rendering/positions.py scales head-area base-ball centers around the species head by (A-B)/100 when A != 100. Shape-position processing also requires a recognized species and a 67-ball frame. These gates matter: the formula must not be applied unconditionally.

Radius arrays include added balls, but the two Head Enlargement values do not directly resize every addball identically. Added-ball position/size dependencies, body areas, subsequent Move/Project Ball operations and integer quantization need separate treatment. These tests do not prove image similarity to an arbitrary requested design.

## Next checks

A=100 with B=25 and neighboring A values are now tested in [HEAD-002](head-002.md). Next inspect added-ball behavior, render sitting/lying comparisons and validate another breed before broad recipe claims. Cross-version edited tests remain outstanding.
