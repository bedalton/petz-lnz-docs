# Petz LNZ research

An evidence-backed, agent-first guide to designing Petz breeds from images and concepts, growing into a thorough LNZ reference. Research starts with Petz 4 Dogz/Catz, then validates edited behavior across Petz 3 and 5. Current findings describe renderer behavior; original-game fidelity remains unverified.

## Start here

- [Agent editing entry point](agent-guides/start.md)
- [Status](STATUS.md), [handoff](HANDOFF.md), [agent instructions](AGENTS.md)
- [Research plan](docs/research-plan.md), [coverage ledger](docs/coverage.md)
- [Community source ledger](sources/community-index.md)

## Reference and editing

- [Dogz base-ball labels](format-reference/anatomy/dogz.md), [Catz base-ball labels](format-reference/anatomy/catz.md): include automated front/side omission sensitivity; semantic visual checks mostly pending
- [Section inheritance](format-reference/inheritance.md)
- [Head Enlargement](format-reference/head-enlargement.md), [choosing head controls](visual-editing/head-ball.md)
- [Linez and connections](format-reference/linez.md)
- [Move](format-reference/move.md), [Project Ball](format-reference/project-ball.md)
- [Iris/pupil colors](visual-editing/eye-colors.md)
- [Body areas](format-reference/body-areas.md)
- [Added-ball groups](format-reference/add-groups.md)
- [Retained texture state](format-reference/texture-state.md)
- [Added-ball fields](format-reference/add-ball.md), [attached details](visual-editing/attached-details.md)
- [Omissions](format-reference/omissions.md), [visibility diagnosis](visual-editing/visibility.md)
- [Renderer evidence gaps](troubleshooting/rendering-gaps.md)

## Evidence

- [Texture/pixel session and integrity checks](docs/session-2026-11-10-textures.md)
- [Morph session and integrity checks](docs/session-2026-11-10-morphs.md)
- [TEXTURE-001: retained static-frame pixels](experiments/texture-001.md), [TEXTURE-002: angle arithmetic](experiments/texture-002.md)
- [MORPH-005: explicit-state pixel controls](experiments/morph-005.md)
- [MORPH-004: retained assembly histories](experiments/morph-004.md)
- [MORPH-003: multiple groups and prefixes](experiments/morph-003.md)
- [MORPH-002: relative-size group activation](experiments/morph-002.md)
- [AREA-006: omitted markers and lists](experiments/area-006.md)
- [AREA-005: anchored cycles and late lists](experiments/area-005.md)
- [AREA-004: connected-chain ID ordering](experiments/area-004.md)
- [Connector session overview and integrity checks](docs/session-2026-11-09-connectors.md)

- [AREA-003: body-area-list precedence](experiments/area-003.md)
- [AREA-002: conflicting neighbor precedence](experiments/area-002.md)
- [AREA-001: connection-derived body areas](experiments/area-001.md)
- [MORPH-001: dormant groups and explicit geometry](experiments/morph-001.md)
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
