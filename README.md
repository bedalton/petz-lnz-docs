# Petz LNZ research

An evidence-backed, agent-first guide to designing Petz breeds from images and concepts, growing into a thorough LNZ reference. Research starts with Petz 4 Dogz/Catz, then validates edited behavior across Petz 3 and 5. Current findings describe renderer behavior; original-game fidelity remains unverified.

Renderer upgrade: [completed review](docs/renderer-upgrade-2026-11-10.md) reviews changed findings after paint texture,Outline,clipping and add-ball projection fixes. Puppy/kitten loading and age defaults on4c4d3df are covered in the [young appearance session](docs/session-2026-11-11-young-appearance.md). Clothing remains unsupported. The [current young-appearance upgrade review](docs/session-2026-11-12-young-upgrade.md) replays these controls on49c7f62 and corrects one endpoint line requirement. Renderer observations do not establish original-game fidelity.

## Start here

- [Blank dog baseline gallery](clean_dogs/README.md): six-view blank and stock references
- [Independent Mastiff authoring-trial review](docs/mastiff-authoring-trial-review.md)
- [Picture-to-breed authoring workflow](agent-guides/picture-to-breed.md), [task brief](agent-guides/task-brief.md), [trial report](agent-guides/trial-report.md)
- [Agent editing entry point](agent-guides/start.md)
- [Status](STATUS.md), [handoff](HANDOFF.md), [agent instructions](AGENTS.md)
- [Research plan](docs/research-plan.md), [coverage ledger](docs/coverage.md)
- [Community source ledger](sources/community-index.md)

## Reference and editing

- [Dogz base-ball labels](format-reference/anatomy/dogz.md), [Catz base-ball labels](format-reference/anatomy/catz.md): include automated front/side omission sensitivity; semantic visual checks mostly pending
- [Section inheritance](format-reference/inheritance.md)
- [Young appearance and age controls](format-reference/young-appearance.md)
- [Head Enlargement](format-reference/head-enlargement.md), [choosing head controls](visual-editing/head-ball.md)
- [Linez and connections](format-reference/linez.md)
- [Face Extension](format-reference/face-extension.md), [preserved muzzle controls](experiments/face-001.md)
- [Move](format-reference/move.md), [Project Ball](format-reference/project-ball.md)
- [Iris/pupil colors](visual-editing/eye-colors.md)
- [Body areas](format-reference/body-areas.md)
- [Added-ball groups](format-reference/add-groups.md)
- [Client-agent texture reference](agent-guides/textures.md): selection, assignment, initial orientation and face-relative gradients
- [Texture selection catalog](texture-index/README.md): searchable local candidates, verified dimensions/previews and availability limits
- [Custom texture creation, palettes and orientation](visual-editing/custom-textures.md)
- [Retained texture state](format-reference/texture-state.md)
- [Preserve and reshape the mouth/muzzle](visual-editing/existing-mouth-and-muzzle.md), [raw tongue-state controls](experiments/mouth-001.md)
- [Reshape existing ears and tail](visual-editing/existing-ears-and-tail.md), [ANATOMY-002 controls](experiments/anatomy-002.md)
- [Added-ball fields](format-reference/add-ball.md), [attached details](visual-editing/attached-details.md)
- [Omissions](format-reference/omissions.md), [visibility diagnosis](visual-editing/visibility.md)
- [Renderer evidence gaps](troubleshooting/rendering-gaps.md)

## Evidence

- [Preserved-mouth controls, raw frames and session audit](docs/session-2026-11-15-mouth-controls.md)

- [Puppy/kitten growth, saved caches and session audit](docs/session-2026-11-11-young-appearance.md)

- [Current relative morph session and integrity audit](docs/session-2026-11-11-relative-morphs.md)

- [Connector texture session and verification](docs/session-2026-11-10-connector-textures.md)

- [Partial rows/composed RNG session and verification](docs/session-2026-11-10-line-history.md)

- [Connector styling session and integrity checks](docs/session-2026-11-10-line-styles.md)

- [Texture/pixel session and integrity checks](docs/session-2026-11-10-textures.md)
- [Morph session and integrity checks](docs/session-2026-11-10-morphs.md)
- [TEXTURE-001: retained static-frame pixels](experiments/texture-001.md), [TEXTURE-002: angle arithmetic](experiments/texture-002.md)
- [MORPH-005: explicit-state pixel controls](experiments/morph-005.md)
- [MORPH-004: retained assembly histories](experiments/morph-004.md)
- [MORPH-003: multiple groups and prefixes](experiments/morph-003.md)
- [MORPH-002: relative-size group activation](experiments/morph-002.md)
- [MORPH-006: current cross-version relative morph replay](experiments/morph-006.md)
- [MORPH-007: size-reference resolution boundaries](experiments/morph-007.md)
- [MORPH-008: size-reference chains and cycles](experiments/morph-008.md)
- [AREA-006: omitted markers and lists](experiments/area-006.md)
- [AREA-005: anchored cycles and late lists](experiments/area-005.md)
- [AREA-004: connected-chain ID ordering](experiments/area-004.md)
- [Connector session overview and integrity checks](docs/session-2026-11-09-connectors.md)

- [AREA-003: body-area-list precedence](experiments/area-003.md)
- [AREA-002: conflicting neighbor precedence](experiments/area-002.md)
- [AREA-001: connection-derived body areas](experiments/area-001.md)
- [MORPH-001: dormant groups and explicit geometry](experiments/morph-001.md)
- [Connector sampling session verification](docs/session-2026-11-10-connector-sampling.md)
- [Texture authoring/motion session audit](docs/session-2026-11-10-texture-authoring.md)
- [Recovered early renderer controls](experiments/update-004.md)
- [Nested cross-version texture replay](experiments/update-005.md)
- [Complete updated static texture matrix](experiments/update-006.md)
- [Motion texture component attribution](experiments/update-007.md)
- [Renderer update and historical comparison review](experiments/update-001.md)
- [Updated eye/shading/state findings](experiments/update-002.md)
- [Available saved-pet upgrade samples](experiments/update-003.md)
- [Depth shading session and integrity audit](docs/session-2026-11-10-shading.md)
- [SHADE-003: omission-induced depth shading](experiments/shade-003.md)
- [SHADE-002: isolated retained shading histories](experiments/shade-002.md)
- [SHADE-001: depth gain and section inheritance](experiments/shade-001.md)
- [TEXTURE-004: returning to a pose after motion](experiments/texture-004.md)
- [TEXTURE-003: Texture List modes and remapping](experiments/texture-003.md)
- [LINE-021: appended texture slots and dimensions](experiments/line-021.md)
- [LINE-020: texture shading and sign boundaries](experiments/line-020.md)
- [LINE-019: Dalmatian/Persian texture routing](experiments/line-019.md)
- [LINE-018: viewport clamping and texture eligibility](experiments/line-018.md)
- [LINE-017: diagonal texture thresholds and samples](experiments/line-017.md)
- [LINE-016: connector texture routing across versions](experiments/line-016.md)
- [LINE-015: oversized textured breed connectors](experiments/line-015.md)
- [LINE-014: texture crop and size limits](experiments/line-014.md)
- [LINE-013: asset-backed connector textures](experiments/line-013.md)
- [LINE-012: fuzzy connector pixel attribution](experiments/line-012.md)
- [LINE-011: composed breed random history](experiments/line-011.md)
- [LINE-010: partial connector rows](experiments/line-010.md)
- [LINE-009: automatic edge selection](experiments/line-009.md)
- [LINE-008: fuzz/whisker random history](experiments/line-008.md)
- [LINE-007: fuzz bounds and repeated draws](experiments/line-007.md)
- [LINE-006: edge colors and modes](experiments/line-006.md)
- [LINE-005: fill and endpoint selection](experiments/line-005.md)
- [LINE-004: short rows and default thickness](experiments/line-004.md)
- [LINE-003: connector draw order](experiments/line-003.md)
- [LINE-002: connector widths](experiments/line-002.md)
- [LINE-001: connected marker and omissions](experiments/line-001.md)

- [RESTORE-001: container recovery](experiments/restore-001.md), [RESTORE-002: local MCP restored](experiments/restore-002.md)
- [PROJECT-004: Dalmatian/Persian projections](experiments/project-004.md)
- [PROJECT-003: edited cross-version projections](experiments/project-003.md)
- [PROJECT-001: synthetic projection semantics](experiments/project-001.md), [PROJECT-002: breed projection controls](experiments/project-002.md)

- [SMOKE-001: local rendering across versions](experiments/smoke-001.md)
- [BALL-001: isolated head-ball edits](experiments/ball-001.md)
- [ANATOMY-001: labels and master keys](experiments/anatomy-001.md)
- [INHERIT-001: section replacement](experiments/inherit-001.md)
- [HEAD-001: head size versus spacing](experiments/head-001.md)
- [MOVE-001: reference-column behavior](experiments/move-001.md)
- [HEAD-002: A=100 spacing boundary](experiments/head-002.md)
- [EYE-001: pupil, iris and host-eye colors](experiments/eye-001.md)
- [EYE-002: iris/host omission combinations](experiments/eye-002.md)
- [ADD-001: attachment, resizing and omission](experiments/add-001.md)
- [OMIT-001: all-base-ball omission sweep](experiments/omit-001.md)
- [VIS-001: geometry behind unchanged omissions](experiments/vis-001.md)
- [VIS-002: Catz 55/56 across poses and views](experiments/vis-002.md)

Raw stock resources, private breed copies and rendered images remain outside Git under ignored persistent scratch storage. Each experiment links its machine-readable manifest; read that only when checking detailed evidence.

Documentation checks: `scratch/petz-local-venv/bin/python tools/check_docs.py`. Regenerate the section ledger with `tools/coverage_index.py` using the same interpreter.

- [Saved-pet paint-angle motion](experiments/paint-001.md)
- [Individual paint-angle attribution](experiments/paint-002.md)
- [Paint-state vector length controls](experiments/paint-003.md)
- [Saved-paint continuation audit](docs/session-2026-11-10-saved-paints.md)
