# LINE-008: retained fuzz tables and shared RNG

Date: 2026-11-10. Code-supported, asset-free direct indexed rasterization. No MCP pixels, breed loading, species/version generalization or native-game validation. [Manifest](line-008.json). Run `scratch/petz-local-venv/bin/python tools/line_fuzz_history.py`; refuses overwrite. Private full states: scratch/research/line-008/states.json. No renderer changes.

96 target rasters combine fuzz1/3/7, four endpoint orientations and eight histories. All target controls fixed: seed1, canvas120x120, widths12/12, fill220, edges180/200, mode0. Clear framebuffer after prior operations so prior pixels cannot contaminate the target. Record target indexed hash, changed pixel count, before/after RNG, table lengths and full-state hashes. Installed source equals checkout; source/dependency hashes recorded. This test uses no game assets or engines.

| Prior history | Changed targets /12 |
| --- | --- |
| Fresh | 0 |
| Same target once | 0 |
| Same target at fuzz0 | 0 |
| Same target at another positive fuzz index | 12 |
| Whisker at step0 | 12 |
| Whisker at step1 | 0 |
| Short connector at same fuzz index | 0 |
| Short same-fuzz connector, then another positive fuzz index | 9 |

The current renderer has one RNG and separate cached row-offset tables indexed by clamped fuzz. Drawing another positive fuzz consumes random values before the target table is initialized. Whisker step0 consumes RNG; step1 does not in this code path. A short same-fuzz connector uses the same initial sequence and any target extension continues it, matching the fresh target. Inserting another fuzz draw before extension can change only the subsequently generated offsets; three fixtures had no pixel change, so a different history is not a universal visible difference.

Assertions enforce equality for repeat, fuzz0, step1 whisker and short same-fuzz histories. Other changed counts are recorded observations rather than universally assumed invariants. This explains why a fixed seed alone cannot isolate a fuzzy connector when earlier line/whisker scheduling changes. Actual composed breed scenes and retained animation remain untested here.
