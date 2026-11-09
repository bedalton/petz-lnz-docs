# PROJECT-003: edited cross-version projections

Date: 2026-11-09. Renderer-observed, not native-game validated.

## Reproduce

Run tools/projection_breed_probe.py with `--game-version petz3`, then `--game-version petz5`, using scratch/petz-local-venv/bin/python. The script uses distinct output directories and manifests and refuses overwrite. [Petz 3 manifest](project-003-petz3.json); [Petz 5 manifest](project-003-petz5.json). Each records controls, original/copy hashes, raw geometry and PNG hashes. Shared engine/runtime provenance: [RESTORE-002](restore-002.json). Renderer revision 9d72d7afd5f7460ef18133c6179caaf8055082d9.

The shared adult-copy helper now accepts an engine version, retaining petz4 as its default. Both numerical resolver and MCP server explicitly select that engine. A first Petz 3 numerical attempt omitted the resolver's engine argument and failed seeking Dogz 4 Rez.dll, before rendering. Corrected the harness; retained failed private copies at scratch/research/project-003-petz3-harness-failed. No renderer source change.

## Results

The same isolated empty/100/50/150 head-to-nose controls as [PROJECT-002](project-002.md) passed in Scottie and Siamese for each version. Twelve edited geometry checks per version span standing/sitting/lying; identity frames equal control in all six species/pose pairs per version. Twelve local stdio MCP standing comparisons per version span yaws 0/90. Four identity pairs per version are pixel-identical; eight edited pairs differ. All recorded geometry and all twelve PNG hashes per version equal the corresponding Petz 4 records.

Four additional sheets visually reviewed: Petz 3 Dogz-long-90, Catz-half-0; Petz 5 Catz-long-90, Dogz-half-0. They agree with the localized nose changes seen in Petz 4. Other sheets were checked by hashes and assertions. Private responses, copies and images remain under scratch/research/project-003-petz3 and project-003-petz5.

## Limits

This is the first controlled edited cross-version sample in this project, confined to these projection rows, two stock breeds, adult age 100/fatness 50/seed 0 and the selected poses/views. Identical pixels do not establish native engine equivalence or comprehensive support. Projection inheritance, added-ball targets, young resources and unrelated sections remain untested here. Original inputs were checked unchanged after preparation; fixed-span resource safeguards apply.
