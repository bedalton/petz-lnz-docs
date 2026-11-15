# No Texture Rotate and starting orientation

There is no per-ball initial texture-angle field in the inspected renderer appearance model. Texture List supplies path, mode and tile dimensions; ordinary/add-ball records supply a texture index. `[No Texture Rotate]` supplies a list of IDs whose automatic texture updates are disabled. It is not an angle setter.

Scope: code inspected and synthetic controls on local renderer checkout `20cd02946c53ea702db789d5b6eeda62c54c429d`; four relevant installed source files match checkout. No new breed renders or native-game validation. Existing render experiments retain their own version/species scopes. See the [client-agent reference and gradient recipe](../agent-guides/textures.md).

## List syntax

Illustrative IDs only; substitute the intended host's actual ID and preserve the other effective entries:

```text
[No Texture Rotate]
42
43
```

These are ball IDs, not Texture List slots, degrees or an axis vector. The parser considers only the first token of each list row; `42 90 180` still disables only ball42. Added hosts use their final ball IDs in the renderer's 512-entry flag table; confirm the actual model's ID mapping. Do not assume a copied ID identifies the same anatomy across species/breeds.

Code-supported edge cases: absent/empty section leaves all flags enabled. IDs0–511 disable their flags. A first parsed integer of -1 disables all512 flags and ends the scan; -1 after another parsed integer does not. Out-of-range integers can consume that first-integer position; nonintegers do not. **Do not use -1 as a portable recipe:** Carolyn's older tutorial describes it as default loose rotation, in disagreement with this renderer. Native semantics of that conflict remain unresolved.

## What changes orientation

`appearance/core.py:read_core` parses the flag list. `rendering/preparation.py:prepare_frame` calls `update_texture_orientation` only for eligible visible positive-radius textured hosts with their rotation flag enabled. It passes animation/body/head rotations. Fresh `TextureOrientation` begins with identity matrix and angles(0,0), but preparation can update those angles before the first draw; zero initial state does not imply an unshifted first portrait. Added hosts use their base ball's animation record in this path.

`rendering/texture_rotation.py` computes updated sampler angles from those rotations and prior state. `rendering/texture.py:sample_window` uses them to shift the sampled window, rather than rotating the bitmap plane by that many degrees. With a256×256 tile and diameter32, changing sampler angles from none to(64,0) moves the sample start16 pixels right. There is no exposed LNZ starting sampler-angle pair in these inspected paths. Renderer API state injection is separate from a distributable LNZ feature.

Disabling updates makes preparation pass no sampler angles for the host; it does not capture an arbitrary desired frame's orientation, set a faceward axis, or bind a dark edge to anatomy. See [retained texture state](texture-state.md) for sampled motion/history effects. Direct painting directions position surface markings and are not texture-roll settings.

## Community reports

| Primary source | Source-reported guidance | Boundary |
| --- | --- | --- |
| [Waverly Academy: No Texture Rotate](https://waverlyacademypetz.weebly.com/no-texture-rotate.html) | Add the section and list the affected ball IDs, one per row; demonstrates a textured Mutt | No arbitrary starting-angle parameter described; game/version coverage not specified |
| [Lida: No Texture Rotate eyes](https://lida.fantazzled.com/notexrotateeyes.html) | Uses the section for eye artwork; offsets the bitmap to align it and suggests a horizontal mirror for the opposite eye | Source workflow only; no independent test here. Its iris-replacement steps are not endorsed by this project's preserve-anatomy workflow |
| [Carolyn: LNZ breakdown, third part](https://homebody.eu/carolyn/downloabx/tutorials/tutorialbits/LNZ3rd.txt) | Describes listed-ball textures staying screen-facing during pickup rather than anatomically fixed, and -1 as default loose rotation | Older account, including2004 updates; -1 conflicts with inspected renderer. No game-specific reconciliation performed |

These accounts support caution about anatomical attachment; they do not prove behavior for the user's gradient. No tutorial supplies a general arbitrary starting-angle field. Absence in these sources is not proof that no undocumented game feature exists.

## Reproduce the code controls

```bash
scratch/petz-local-x86-venv/bin/python tools/check_texture_reference.py
```

The [checker](../tools/check_texture_reference.py) verifies eight list-parser cases, equality with extra Texture List columns, default orientation, a yaw-driven angle change, and the16-pixel sample shift. It records source SHA-256 values and exact numerical outputs in ignored `scratch/research/texture-reference/verification.json`. No game files are loaded or modified; synthetic controls support parser/arithmetic claims, not rendered appearance or game fidelity.
