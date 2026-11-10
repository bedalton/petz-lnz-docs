# PAINT-007: saved paint groups across ages

Date: 2026-11-10. Petz4 Fuzzkin, integration6c1d883. [Manifest](paint-007.json), [reproducer/verifier](../tools/paint_group_ages.py). Uses the existing PAINT-006 private copies; no new saved-file edits.

## Result and controls

At explicit ages0/50/100, group0 and group1 copies retain exactly equal prepared frames and PNGs relative to baseline in all36 comparisons. The18 fixtures cover standing/sitting/lying and front/side; 72 direct draws are persisted. Sixteen fresh local stdio MCP views cover standing front/side at ages0/100, all four variants; every PNG matches direct output.

The loaded appearance retains group edits. Ages0/50 use two cache layers; age100 uses adult only. All18 baseline fixtures prepare three paint commands, all textured. Seed and fatness stay saved; age is explicitly overridden. State is fresh, yaw0/64, raster/line seed1, step0. Geometry is equal across each fixture's four variants.

Color65 changes displayed pixels in17/18 fixtures. Age50 lying/front changes zero pixels despite three eligible paints; eligibility alone is not visible coverage. No occlusion/anatomical cause is established here. This is a recorded negative positive-control outcome, not evidence of group semantics. Other counts and hashes are in the manifest.

Source/copy hashes are inherited and checked against PAINT-006; all62 installed Python sources, engine/dependency hashes and prior manifest hash are checked. Original game files and renderer remain unchanged. Private evidence:scratch/research/paint-007.

## Reproduce and limits

```sh
scratch/petz-local-venv/bin/python tools/paint_group_ages.py --verify
```

The verifier reloads/renders all72 direct outputs and checks persisted MCP PNGs, without new MCP calls. Generation refuses an existing evidence directory. This samples age-dependent cache assembly in one saved pet, not broader pets/species/versions or native game retint behavior. Copy checksums remain unvalidated for game use as described in PAINT-006.
