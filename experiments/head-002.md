# HEAD-002: A=100 position-scaling boundary

Date: 2026-11-09. Status: Petz 4 renderer-observed and code-supported, not game-validated. Scottie and Siamese; same environment/revision as SMOKE-001.

## Procedure

Run `scratch/petz-local-venv/bin/python tools/head_gate_probe.py`. Private fixed-span copies use Head Enlargement pairs neutral (100,0), gate (100,25), above (101,25), below (99,25). Other effective sections are unchanged. Direct geometry checks cover all four variants in standing/sitting/lying, seed 0, age 100, fatness 50: 24 asset loads. Four local MCP front-view standing comparisons cover neutral→gate and gate→above for both species. Private results: scratch/research/head-002. [Tracked controls/hashes/checks](head-002.json).

## Findings

For both species in all three poses, (100,25) and (100,0) give identical complete modified raw frames. Their radii differ: 26 Dogz / 16 Catz base-ball radii change. Increasing B at A=100 therefore enlarges head-area balls without this shape-position operation moving their centers.

Changing A from 100 to either 99 or 101 with B=25 activates position scaling. Versus (100,0), 27 Dogz / 25 Catz centers change in every inspected pose. Three comparison images were visually reviewed: Catz neutral→gate, Catz gate→above, Dogz gate→above. A one-unit change across the gate can produce a visible jump in feature placement, not a smooth one-percent progression.

This agrees with the explicit `A != 100` branch in rendering/positions.py. It is recorded behavior of this implementation, not yet a confirmed native-game requirement or bug. The A+B base-diameter term still applies across the boundary. Integer quantization explains why count-of-changed-radii is not a complete area-membership test.

## Editing consequence

Do not interpolate head spacing blindly through A=100 when B is nonzero. Preserve the baseline pair, compare exact neighboring values, and check feature overlap. Do not change the renderer to smooth this discontinuity without native evidence. Decreasing farther, testing negative/extreme pairs, added-ball effects and cross-version validation remain open.
