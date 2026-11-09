# PROJECT-002: breed projection controls

Date: 2026-11-09. Renderer-observed Petz 4 Scottie/Siamese results; no native-game validation.

## Method

Run `scratch/petz-local-venv/bin/python tools/projection_breed_probe.py`. The script refuses to overwrite its private output directory. It creates seed-resolved adult LNZ copies with Project Ball explicitly empty (control), or a single head-to-nose row at 100, 50 or 150 percent. These are isolated controls, not unchanged stock baselines: inherited projection rows are deliberately replaced. Other effective sections are left to the usual resource pipeline. Fixed-span copy safeguards verify resource metadata, unrelated payloads and bytes outside the adult LNZ span. Originals remain unchanged.

Targets: Dogz head 52 → nose 55; Catz head 24 → nose 37. Geometry checks use standing/sitting/lying. Twelve local stdio MCP comparisons use standing, yaws 0/90, seed 0, age 100, fatness 50. [Manifest](project-002.json) contains input/output hashes, exact rows, positions and controls. Full responses, PNGs and private copies: scratch/research/project-002. Renderer revision and runtime hashes: [RESTORE-002](restore-002.json).

## Results

All twelve edited geometry checks match the componentwise integer formula from [PROJECT-001](project-001.md). Only the target nose position changes in each 50/150 case. All six identity geometry loads equal the empty-projection control. Four identity image pairs are pixel-identical; all eight 50/150 image pairs differ.

All eight edited front/side comparison sheets were reviewed at native resolution. The local nose placement changes while the rest of the muzzle remains visually separate; the side view makes the extension especially clear in Siamese. This does not demonstrate coherent muzzle reshaping or imply that other facial balls follow the nose. Comparison cells use common controls/scaling, but framing is not a raw-coordinate measurement.

## Limits

Two breeds, adult Petz 4, three numerical poses and one rendered pose. Negative percentages, ordering and invalid IDs retain synthetic/code evidence only. No added-ball targeting, age blending, other breeds or edited cross-version claims. The explicit empty control does not establish inheritance behavior for Project Ball. No renderer code changes.
