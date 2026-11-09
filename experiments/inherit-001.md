# INHERIT-001: absent, empty and partial sections

Date: 2026-11-09. Status: renderer-observed and code-supported; not game-validated. Petz 4 Scottie and Siamese only.

## Question and procedure

Does adding a breed section merge its rows with master rows? Run `scratch/petz-local-venv/bin/python tools/inheritance_probe.py` from /workspace. Runtime/renderer match [SMOKE-001](smoke-001.md); shared engine provenance is retained in private render metadata.

Using the fixed-span, seed-resolved copy safeguards from [BALL-001](ball-001.md), create four variants of each adult resource. Change only the Key Balls section relative to its resolved control: absent, empty, one head-ID row, or all ten original master rows. Use explicit selectors SC/SI for numerical inspection. Check effective sections with load_layer, then render all eight variants through local stdio MCP at standing, yaw 0°, seed 0, age 100 and fatness 50.

## Findings

| Breed section | Effective row count | Effective key fields | PNG versus absent |
| --- | --- | --- | --- |
| Absent | 10 | All ten master values | Baseline |
| Empty | 0 | All ten slots become -1 | Different, both species |
| Head row only | 1 | Head retained; all nine remaining slots -1 | Different, both species |
| Full master rows | 10 | Same as master | Identical, both species |

All eight renders completed; assertions checked effective rows and full-versus-absent PNG identity. The partial case does not inherit missing key slots. These results directly support whole-section replacement in this renderer, including empty overrides. Key Balls drives several rendering behaviors; these PNG differences do not isolate which behavior causes each changed pixel. Images were not separately visually interpreted in this experiment.

[Hash and effective-key manifest](inherit-001.json). Private copies, PNGs, diagnostics and provenance: scratch/research/inherit-001. Reruns overwrite that directory. Original resources remain untouched; all bytes outside the edited adult resource span and all unrelated resource payloads are checked unchanged.

## Editing consequence

Before adding a breed section, inspect the selected master and preserve any rows that remain necessary. Distinguish whole-section inheritance from within-section operations: repeated override rows or multiple Move entries can have their own processing order. This experiment does not establish every section's row syntax, native game fidelity or cross-version behavior.
