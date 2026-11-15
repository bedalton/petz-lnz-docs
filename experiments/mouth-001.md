# MOUTH-001: raw-frame tongue controls

2026-11-15. Petz 4 Dogz/Catz animation libraries on renderer `20cd02946c53ea702db789d5b6eeda62c54c429d`. Asset/code and local renderer observations; no native-game behavior validation. This extends preset-only sampling without assigning behavior names to animation numbers.

## Inventory and sampling

[Inventory harness](../tools/mouth_frame_inventory.py) reads the original BHD/BDT resources without modifying them. Run `scratch/petz-local-x86-venv/bin/python tools/mouth_frame_inventory.py`. It refuses an existing folder. Private index: `scratch/research/mouth-001/inventory.json`; coordinates/raw rows remain uncommitted.

| Library | Animations in index | Frames decoded | Frames with positive tongue-size modifiers |
| --- | ---: | ---: | ---: |
| Dogz 4 | 445 | 13,457 | 2,666 |
| Catz 4 | 493 | 16,040 | 5,655 |

Base BHD tongue sizes are zero for Dogz63/64 and Catz55/56. Positive dynamic modifiers identify potential tongue states; they do not prove visibility, behavior or an accessible native action. The script ranks frames by descending sum of those two modifiers, then animation/frame number, selecting the first frame from each of twelve distinct animations per species. This is a deterministic extreme-state sample, not representative animation coverage.

## Preserved-mouth previews

[Render harness](../tools/mouth_frame_probe.py) uses the existing FACE-001 source/−12/+12 copies, without another breed edit. Run `scratch/petz-local-x86-venv/bin/python tools/mouth_frame_probe.py`; it refuses an existing render folder. Each of24 selected frames is tested in two forced looks, two yaws and three scalar variants:288 real local stdio MCP calls, each byte-identical to a fresh direct Python render. Seed41/fatness50; adult100 and puppy/kitten12; yaws0/90. Explicit raw animation/frame controls replace the named presets.

144 geometry records verify unchanged radii, visibility and parked flags between scalar variants, including the two original tongue balls and Labrador's original relative-size detail77. Existing parents, size references, groups, projections, connectors, textures and base anatomy are retained through the FACE-001 copy checks. Source frames and sizes match between variants. Eight aligned nearest-neighbor sheets retain all288 cells; frame metadata and input/source hashes remain private.

The raw library can supply positive-sized tongue geometry absent from the three closed-mouth presets. This narrows the earlier VIS-002 limitation: its preset samples remain valid; they did not exhaust raw animations. Raw frames do not reproduce native scheduling, interpolation, expression overlays or eating/drinking behavior. Use them as additional renderer review states while retaining native tests as an open requirement.

Four individual source previews were visually inspected: Labrador adult27/5 profile, puppy19/31 front, Siamese adult167/4 profile and kitten257/20 front. Visible Labrador tongue detail and noncanonical cat orientations confirm why these must remain raw state identifiers. The complete eight sheets are retained/hash-checked, not claimed individually visually reviewed.

## Verification and limits

[Independent auditor](../tools/check_mouth_frames.py) re-reads original BHD/BDT integer fields with `struct`, independently of renderer frame decoding, and compares all29,497 saved tongue modifier/coordinate/tag records. It also audits deterministic selection, source hashes,296 PNG hashes,144 saved tongue records and192 anchor-aligned scalar comparisons. All checks pass; [compact manifest](mouth-001.json). Evaluated tongue radii across selected looks/scalars span Labrador63/64=4–7, relative detail77=3–6; Siamese55=4–7 and56=4–8. These are rendered-unit radii for these controls, not native sizes.

A positive radius does not establish visible pixels. A visible pink feature does not validate its native function. The selected frames can involve extreme poses and the scalar interventions can distort joins. These are diagnostic controls for the exact sampled Petz4 Labrador/Siamese, not an action catalogue, continuous motion test, other-version result or safe range.

The first render-harness attempt supplied a named pose together with raw frame arguments and was rejected before rendering. The corrected direct loader omits pose for raw frames; MCP uses its documented `pose=default` raw control. The failed private folder is excluded. No renderer defect is claimed.
