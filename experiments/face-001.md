# FACE-001: preserve existing muzzle construction

2026-11-15. Petz 4 blank Labrador and stock Siamese, renderer `20cd02946c53ea702db789d5b6eeda62c54c429d`. Local stdio MCP and numerical geometry evidence; no native-game validation. Reusable [field reference](../format-reference/face-extension.md) and [mouth guide](../visual-editing/existing-mouth-and-muzzle.md).

## Reproduction

Run `scratch/petz-local-x86-venv/bin/python tools/face_extension_probe.py`. The [harness](../tools/face_extension_probe.py) refuses an existing output directory; replay into another directory with `--out`. Run [the independent auditor](../tools/check_face_extension.py) with `--replay scratch/research/face-001-replay` after the replay completes. Proprietary copies, geometry, metadata and PNGs remain private in `scratch/research/face-001`; the [compact manifest](face-001.json) records final verification.

Inputs are the exact Petz 4 blank Labrador used by ANATOMY-002 and stock Siamese. Each has source, compaction-only roundtrip, Face Extension `0`, `-12`, `12` variants. Both adult and young resources receive the scalar edit; raw variation syntax is retained. Original resource trees, all other payloads and all bytes outside the two bounded LNZ spans remain identical. The roundtrip writer matches the original parsed section tables at seeds 0–255 in four resources: 1,024 comparisons. This is sampled parser preservation, not a native parser proof.

## Controls

Five variants × two breeds × two forced looks × three poses × four yaws = 240 actual local stdio MCP render calls. Seed 41, fatness 50, forced adult age 100 and forced puppy/kitten age 12; standing/sitting/lying; yaw 0/45/90/180. The current lying presets are Dogz 79/frame29 and Catz 263/frame24. Returned effective pose metadata is retained. Twelve aligned nearest-neighbor sheets retain all 240 cells.

Sixty geometry records check all variant/breed/look/pose combinations. Each effective appearance differs only in Face Extension; original added rows, parents, size references, omissions, groups, connectors, textures, Move and Project Ball rows are retained. Frame/size inputs and every evaluated radius/visible/parked field match the baseline. An independent integer oracle checks isolated raw-frame displacement in each record, with unrelated shape operations and Move/Project disabled only for that oracle.

## Findings

| Asset | Face=0 changed PNGs / 24 | Face=-12 | Face=12 |
| --- | ---: | ---: | ---: |
| Blank Labrador | 23 | 23 | 24 |
| Stock Siamese | 10 | 24 | 24 |

All 48 source/roundtrip render pairs are byte-identical. Unchanged views can conceal numerical changes. The twelve young Siamese Face=0 images are a different case: its source scalar −1 truncates to an isolated zero displacement in all three sampled frames, and the complete geometry is unchanged. Adult Siamese Face=0 changes geometry in all three poses, yet lying yaw0/180 retain identical pixels. Distinguish integer no-ops from pixel-hidden geometry changes. The source adult scalar is -2 for this Labrador and +2 for this Siamese; setting zero is an intervention rather than a general no-op.

The field translates a fixed species-specific muzzle set without directly resizing it; the [reference](../format-reference/face-extension.md) records the formula, ordering and repeated utility ID. The complete asset result is broader than that fixed base set because original attachments and projections remain active. In the Labrador, added ear details 82/83 can move despite unchanged parents 4/28: existing projections 51→82/83 and 39→82 /15→83 couple them to the mouth. Do not infer dependency scope from parent IDs alone.

Visual review covers four full sheets: adult standing and young lying for each species (80 displayed cells). Profiles show nose/muzzle advance or retraction; the jaw/head relationship and retained surface construction require review rather than assuming rigid translation. Other sheets are retained and hash-checked, not claimed individually visually reviewed. These controls are not a finished aesthetically approved muzzle.

Full replay retains all 240 render PNGs and twelve sheets byte-for-byte. The independent auditor passes 252 PNG hashes, 240 anchor-aligned RGBA comparisons and 60 geometry records; six original hashes and ten private copy hashes also pass.

## Provenance and limits

Runtime: Python 3.12.16, renderer package 0.1.0, FastMCP 4.1.6, Pillow 13.0.0; all 62 installed Python sources match checkout. Six original input/dependency hashes remain unchanged. No renderer or original-game file is edited.

Preparatory failures are retained privately: the initial unsupported `young` alias, and a second run affected by moving its output folder while an earlier process was still exiting. Neither supplies reported evidence. The successful run uses explicit puppy/kitten values and has a separate replay folder/log. These harness failures do not establish a renderer defect.

Native mouth motion, sustained transitions, genetics, extreme scalars, other assets and cross-version applicability are not established here. Keep the original tongue, jaw, jowls and all attachments even when hidden in a preset still. Follow-up raw-frame and version controls are separate experiments.
