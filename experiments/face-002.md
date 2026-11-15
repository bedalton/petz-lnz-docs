# FACE-002: Face Extension across Petz 3/4/5

2026-11-15. Stock Scottie/Siamese in each game version, renderer `20cd02946c53ea702db789d5b6eeda62c54c429d`. Code/asset and local stdio MCP evidence, not native-game validation. Unlike FACE-001, the dog sample here is stock Scottie, not the blank Labrador.

## Reproduction and controls

Run `scratch/petz-local-x86-venv/bin/python tools/face_extension_versions.py`. The [harness](../tools/face_extension_versions.py) refuses an existing output directory; `--out` selects another. The [retained-evidence auditor](../tools/check_face_versions.py) independently checks hashes, age endpoint relationships and anchor-aligned comparisons. Private copies, complete geometry and PNGs: `scratch/research/face-002`. The [compact manifest](face-002.json) records completed verification.

For each of six source breeds, bounded adult/young LNZ edits produce source, roundtrip, Face Extension `0`, `-12`, `12` copies. The writer retains raw variation syntax and all bytes outside the two resource spans, resource trees and unrelated payloads. Roundtrip tables match seeds 0–255 across twelve resources: 3,072 parser comparisons. No original or renderer source is edited.

Numerical matrix: three versions × two species × three look modes (forced adult, forced puppy/kitten, interpolated age) × four age values (0,12,50,100) × three poses × five variants = 1,080 records. Each appearance differs only in Face Extension. Frame/sizes and original anatomy/dependencies remain unchanged; radii, visible and parked fields match the variant's unchanged source at the same controls. The independent integer oracle from FACE-001 checks each isolated raw-frame displacement separately from complete asset geometry.

Actual local MCP matrix: three versions × two species × three look modes × three poses × two yaws × five variants = 540 renders. Forced adult uses age 100; forced young and interpolated look use age 12. Seed 41, fatness 50, yaw0/90, standing/sitting/lying. Resolvers and MCP services receive explicit game versions. Effective metadata and revision-specific preset catalogues are retained; the same pose name alone would not establish matching frames.

## Audit interpretation

The auditor checks 540 PNG hashes and source/variant aligned RGBA pairs, 180 interpolated-age endpoint equalities (age 12 equals forced young; age 100 equals forced adult), 720 matched Petz 3/5-versus-Petz 4 geometry records and 360 aligned cross-version image pairs. Age0 is separate: its scalar agrees with forced young but its geometry differs in all 90 controls because juvenile scale shrink applies below 12. This agrees with the [existing age reference](../format-reference/young-appearance.md). All 720 cross-version geometry records and 360 aligned image pairs match Petz 4 exactly. All 108 source/roundtrip PNG pairs match. All remaining hash, source/variant and endpoint checks pass. This establishes only these matched assets/controls, not general game-version equivalence.

The initial preparation attempt omitted the direct resolver's explicit version and requested a Petz 4 DLL from the Petz3 root. It failed before rendering and is retained privately as `face-002-initial`. The successful harness supplies both resolver and MCP version parameters. This is a harness correction, not a renderer defect.

No new visual review of all 540 PNGs is claimed. This experiment tests numerical relationships and retained pixels; FACE-001 supplies the separately described visual sample. Native motion/scheduling, genetics, saved pets, other breeds, extreme scalars and a complete coordinated muzzle design remain unvalidated.

The first audit incorrectly equated age 0 geometry with forced young. It failed; independent inspection identified the already-documented juvenile scale shrink. The corrected auditor uses age 12/100 endpoint equalities and explicitly checks all 90 age 0 differences. The failed log remains private; the render matrix itself required no change.
