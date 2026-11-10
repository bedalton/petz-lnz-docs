# Saved paint groups: ten-minute continuation

Date: 2026-11-10. Current build:integration6c1d883. All findings below are source/code-supported or renderer-observed; none are game-validated. Private artifacts remain under scratch/research; original game files and renderer source were not edited.

## Research units

| Unit | Controlled question | Evidence |
| --- | --- | --- |
| [PAINT-005](../experiments/paint-005.md) | Does skipped saved-prefix array data affect the sampled load/render path? | Three pets, four mutations each; 72 edited/72 baseline draws, 30 MCP views. Parsed appearance and pixels remain equal. |
| [PAINT-006](../experiments/paint-006.md) | Do cached paint groups reach assembly and affect output? | Nine copies, 72 direct draws, 18 MCP views. Groups0/1 parse and alter diagnostics but preserve36 prepared-frame/pixel comparisons. Fuzzkin color controls change6/6 views; other two pets lack visible positive controls. |
| [PAINT-007](../experiments/paint-007.md) | Does the group result survive explicit ages? | Fuzzkin ages0/50/100, three poses/front-side:72 direct draws, 36 group equivalences, 16 MCP views. Color controls change17/18 fixtures. |

The source reader skips three count-checked saved arrays, then loads authoritative adult/young LNZ caches. Array numbering in PAINT-005 deliberately avoids assigning unverified native meanings. PAINT-006 isolates group tokens in those caches. PAINT-007 tests cache interpolation and adult-only loading. Together they narrow the sampled renderer limitation without establishing native retint behavior.

At age50 lying/front, three eligible textured paints still produce no displayed color-edit difference. Do not equate prepared eligibility with visible coverage. No cause or anatomical interpretation is established. PAINT-006's first attempt incorrectly demanded a prepared-command change in every color control; the failed attempt/log is archived under scratch/research/paint-006-attempt1. Final reports preserve negative controls explicitly.

## Reproducible verification

```sh
scratch/petz-local-venv/bin/python tools/saved_colour_arrays.py --verify
scratch/petz-local-venv/bin/python tools/saved_paint_groups.py --verify
scratch/petz-local-venv/bin/python tools/paint_group_ages.py --verify
scratch/petz-local-venv/bin/python tools/check_paint_group_session.py
scratch/petz-local-venv/bin/python tools/check_docs.py
```

All three complete unit replays pass. [Aggregate verifier](../tools/check_paint_group_session.py) checks:

- 298 research PNGs:102 PAINT-005, 108 PAINT-006, 88 PAINT-007; every file is manifest-linked and rehashed.
- 21 reconstructed private copies and 21 unchanged original-file hash links, including restored stock resources/engines across versions plus three saved pets.
- 64 persisted MCP PNG/metadata records with dimensions, input controls and saved/override metadata checked; group diagnostics independently checked in MCP output.
- 144 independently decoded RGBA difference counts; 18 contact sheets reconstructed cell-by-cell and six native-resolution standing front/side sheets reviewed.
- 18 PAINT-005→PAINT-006 baseline PNG links; PAINT-005 additionally verifies48 links to PAINT-001 fresh controls.
- All62 installed Python sources against checkout, actual checkout HEAD, engine/dependency hashes, four current tool hashes and full-unit replay-log hashes.

The session totals288 direct draws and 64 research MCP views. Saved-file probes retain lengths and unaffected bytes; the renderer does not validate the PetzInfo checksum. They are not game-validated saves.

Private aggregate:scratch/research/paint-group-session-verification.json. Logs:scratch/paint-{005, 006, 007}-verify.log. Source/copy checks are executed by unit verifiers; the aggregate preserves their evidence hashes and independently checks saved pixels/metadata/links.

## Local service and remaining work

The HTTP server was absent after environment/server recovery; it was restarted on127.0.0.1:8765 (PID12934, managed exec session41600). Discovery/capabilities pass. A separate HTTP Fuzzkin standing/front control matches PAINT-005 exactly. This additional service-health render is excluded from64 research MCP views and 298 research PNGs. Health/result/control PNG and server log use scratch/research/paint-group-session-* paths. Research used independent fresh stdio processes.

Renderer checkout retains its pre-existing .gitignore change only. Unrelated untracked istall-node remains untouched. Required Git identities and absence of coauthor trailers checked.

Next:other textured pets/versions, source-grounded native saved-array/group semantics, or independent game validation. Group behavior is now sampled end-to-end in three Petz4 saves and across ages for Fuzzkin; broader retint fidelity remains open. This continuation is limited to the requested ten minutes.
