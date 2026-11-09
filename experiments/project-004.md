# PROJECT-004: another breed per species

Date: 2026-11-09. Renderer-observed Petz 4; native-game behavior unvalidated.

Run `scratch/petz-local-venv/bin/python tools/projection_breed_probe.py --alternate-breeds`. Uses Dalmatian adult DM and Persian adult PR. The shared copy helper accepts explicit filename/selector overrides; defaults for previous experiments are unchanged. Output refuses overwrite.

Same isolated empty/100/50/150 head-to-nose controls as [PROJECT-002](project-002.md). Twelve edited geometry checks across standing/sitting/lying pass; only nose 55 (Dogz) or 37 (Catz) changes raw position at 50/150. Identity frames equal control in all six species/pose pairs. Twelve local stdio MCP front/side standing comparisons pass: four identity pairs equal, eight edited pairs differ. Four edited side sheets reviewed (half/long for both breeds); nose placement changes locally, most visibly extending the Persian nose at 150. Front sheets checked numerically, not visually reviewed.

[Manifest](project-004.json) records source filenames, input hashes, raw positions, rows, controls and output hashes. Fixed-span safeguards preserve unrelated resources and original inputs. Runtime/engine hashes: [RESTORE-002](restore-002.json); renderer 9d72d7afd5f7460ef18133c6179caaf8055082d9, Python 3.12.16. Private files: scratch/research/project-004.

This expands the sampled Petz 4 projection behavior to two breeds per species. It does not establish a complete anatomy atlas, coherent muzzle transformation, young-resource behavior or all-breed/version generality. Explicit empty projection controls replace inherited rows; inheritance remains a separate question. No renderer source changes.
