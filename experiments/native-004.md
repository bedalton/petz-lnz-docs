# NATIVE-004 — screenshot color profiles

All21 source PNGs contain an embedded ICC profile named `Display`; there are two different profile hashes. Qualitative color review must retain or convert those profiles. The [NATIVE-003](native-003.md) untagged reductions preserve encoded RGB samples for grid analysis, but do not preserve their display interpretation.

## Reproduce

```sh
scratch/petz-local-x86-venv/bin/python tools/native_colour_profiles.py
scratch/petz-local-x86-venv/bin/python tools/native_colour_profiles.py --verify
scratch/petz-local-x86-venv/bin/python tools/check_native_colour_profiles.py
```

The initial command requires a fresh private output directory. [Manifest](native-004.json) records source/profile/output hashes and installed Pillow/LittleCMS versions. The backend is local Pillow ImageCms/LittleCMS, with the installed renderer palette inspected at49c7f62; no hosted rendering is used. The referenced NATIVE-002 manifest identifies renderer source/dependency/resource hashes.

Private output: `scratch/research/native-004`. Each source gets a reduced copy tagged with its original profile, plus a converted sRGB copy tagged with a captured target profile. That target ICC file is retained for exact replay because generated ICC timestamps may vary. Conversion uses relative colorimetric intent1, flags0. No original is changed and no raw image, profile or game data is committed.

## Controls and results

The21 conversion-before/after-reduction controls match exactly. The21 same-source-profile transforms are exact no-ops. All sources are RGB or fully opaque RGBA; no meaningful alpha is discarded. Most report DPI metadata near144, which is metadata rather than proof of physical display scaling.

| Source profile | Stills | Reduced pixels | Exact palette RGB before | Exact palette RGB after | After, within1 per channel |
| --- | --- | --- | --- | --- | --- |
|1164 bytes,`f27c6fd473b8…` |18 |375,409 |41,497 |177,762 |369,566 |
|4024 bytes,`272072582a21…` |3 |35,281 |2,118 |2,118 |3,002 |

The second profile occurs in the two frontal/side Frisky stills and the Homebody still. The matching test uses the loaded Petz4 executable palette and includes backgrounds/UI as well as pets. It is not a pet segmentation, color-error score or game-fidelity measure. Some RGBs remain outside the palette after conversion. No inference of bad captures, exact runtime palette equality, or completeness of color management follows from this tally.

The audit uses a separately built LittleCMS transform over1,583 unique input colors and checks all410,690 reduced output pixels,42 embedded output profiles,84 palette tallies and all25 unchanged intake hashes. This is an artifact-consistency check using the same LittleCMS engine, not an independent color-science implementation. Full replay and audit pass; logs are `scratch/native-004-{run,replay,audit}.log`.

## Qualitative and saved-state scope

The profile-tagged `qualitative-sheet.png` was reviewed at unchanged image sample scale, showing latest/historical Goobe and Homebody alongside unregistered stock standing renders. Untagged renderer RGB is treated as sRGB for this display; renderer color-space fidelity is not independently established. Poses, expressions, clothing, framing and scene illumination differ.

The latest Goobe remains tan/gold; the historical capture remains reddish-brown after conversion. All Goobe source PNGs share the same ICC profile hash, so differing profile tags do not explain that historical difference. The cause remains open. Nine bounded saved prefix arrays (three each for Fuzzkin/Goobe/Homebody) match byte-for-byte between the old/capture-time saves; this supplies no changed-array explanation either. Other native state is not ruled out.

An initial harness incorrectly required RGBA for the three RGB cat stills; its partial artifacts/log are preserved in `scratch/research/native-004-initial` and `scratch/native-004-initial.log`. A first complete report is archived separately before a sheet-spacing correction. Neither is the final replay target.
