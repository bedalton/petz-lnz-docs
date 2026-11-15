# MOUTH-002: reshape existing Labrador mouth details

2026-11-15. Exact Petz 4 blank Labrador from ANATOMY-002; renderer `20cd02946c53ea702db789d5b6eeda62c54c429d`. Local stdio MCP and numerical evidence, not native-game validation. Controls retain the source construction and edit only existing added rows.

## Reproduce and preserve

Run `scratch/petz-local-x86-venv/bin/python tools/mouth_detail_probe.py`; use `--out` for a separate replay folder. [Harness](../tools/mouth_detail_probe.py), [independent retained-evidence auditor](../tools/check_mouth_details.py). Private files: `scratch/research/mouth-002`. Both scripts retain proprietary resources, coordinates and renders under ignored scratch. The [compact manifest](mouth-002.json) records completed verification.

The constrained writer changes only the original LR/LRPUP spans, preserves variation syntax and all other resource bytes, and retains young inheritance of adult Add Ball. A roundtrip-only variant matches both original section tables at seeds 0–255: 512 parser comparisons. No original file, renderer source or Mastiff artifact is modified.

Every variant keeps all base/added IDs and row order, attachment parents, optional size references, groups, textures, omissions, connectors, Move and Project Ball rows. The effective appearances differ only in the stated added-row fields. Geometry checks assert that all unlisted IDs remain exactly unchanged, including base mouth anatomy; visible/parked flags remain unchanged throughout.

## Deliberate controls

| Variant | Existing-row edit | Interpretation |
| --- | --- | --- |
| cheek_x | 78 x+6; 79 x−6 | Paired cheek surface offsets in the original chin-relative frames |
| lip_jowl_x | 80/91 x+4; 81/92 x−4 | Coordinated existing mouth-corner and jowl surface offsets; original hosts remain |
| lower_y | 88–92 y+6 | Existing chin/jowl detail offsets only; diagnostic, not an approved lower-jaw design |
| tongue_relative0 | 77 ordinary size −1→0; keep parent 63 and size reference 63 | Zero relative offset retains frame-driven reference radius rather than suppressing the tongue |

These are exact controls for this asset, not universal mouth IDs or final screen-space directions. Source and compaction-only roundtrip complete the six-variant set. Face Extension and all original base mouth positions remain unchanged.

Two forced looks (adult100/puppy12), five states (standing/sitting/lying and raw Dogz animation27/frame5, animation19/frame31), two yaws (0/90), six variants = 120 actual MCP renders. Seed41, fatness50. Sixty geometry records and ten aligned nearest-neighbor sheets retain the controls. Raw frame numbers are data identifiers; no behavior name or native scheduler interpretation is assigned.

The cheek, lip/jowl and lower-y controls change respectively 20/20,19/20,20/20 sampled PNGs. Only their target added IDs change numerical geometry, and radii stay unchanged. Tongue-relative0 changes 3/20 PNGs: its radius becomes exactly base63's radius; both closed-mouth preset looks retain zero radius. The sampled raw frames give a frame-driven positive radius. An unchanged image does not establish that an edit has no numerical effect.

Visual review of the complete adult raw27 and puppy standing sheets covers 24 displayed cells. The cheek and mouth-corner/jowl controls adjust the existing contour. Lower-y covers more of the visible tongue in the raw27 front/profile previews despite retaining tongue geometry. Therefore preservation checks are necessary but insufficient: retain tongue references and review mouth occlusion in open states. No control here is a finished Mastiff muzzle or a native animation approval.

## Scope and verification

Python3.12.16, renderer0.1.0, FastMCP4.1.6, Pillow13.0.0;62 installed Python sources match checkout. Five original input/dependency hashes and six private copy hashes are retained and checked. The independent audit rehashes130 PNGs, compares120 anchor-aligned RGBA pairs and verifies60 saved geometry records. Full replay matches all120 render PNGs and ten sheets byte-for-byte; geometry records agree exactly.

Other breeds, Catz, Petz3/5, continuous age interpolation, combined shape controls, native expressions/eating/panting, genetics and game loading remain unvalidated. Keeping a closed-mouth zero size reference is specifically different from replacing or permanently exposing the tongue. Review the [mouth preservation guide](../visual-editing/existing-mouth-and-muzzle.md) before adapting any control.
