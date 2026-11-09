# Status

Updated: 2026-11-09

- Environment restored: [RESTORE-002](experiments/restore-002.md); game folders corrected, local Petz 4 HTTP MCP connected, six cross-version stdio smoke pairs pass and match prior hashes. Prior private artifacts are still absent.

- Complete: local MCP baseline across six species/version combinations; first copy-only Petz 4 edits and native-resolution visual review.
- Latest inventory: [ANATOMY-001](experiments/anatomy-001.md), with 67 candidate labels per species across versions; [community sources](sources/community-index.md).
- Prior: [BALL-001](experiments/ball-001.md), [manifest](experiments/ball-001.json), [head editing note](visual-editing/head-ball.md).
- Inheritance: [INHERIT-001](experiments/inherit-001.md) confirms whole-section replacement for Key Balls in both sampled Petz 4 breeds.
- Findings: master head IDs Dogz 52/Catz 24; isolated size/color/move edits change renders, but head-ball movement does not move all facial features.
- Latest shape result: [HEAD-001](experiments/head-001.md) separates head radius and spacing effects; eight aligned comparisons and three-pose numerical checks.
- Move: [MOVE-001](experiments/move-001.md) confirms rotated offsets, zero-vector no-op and downstream projection effects. Native anchoring discrepancy tracked as GAP-001.
- Head boundary: [HEAD-002](experiments/head-002.md) confirms A=100 skips spacing while neighboring values activate it.
- Navigation/checks: [agent entry point](agent-guides/start.md), [coverage ledger](docs/coverage.md); tools/check_docs.py checks links, JSON/hash syntax and private-file exclusion.
- Eye colors: [EYE-001](experiments/eye-001.md) distinguishes pupil fill, iris outline and host-eye fill; [editing recipe](visual-editing/eye-colors.md).
- Added details: [ADD-001](experiments/add-001.md) tests attachment, relative radius and omission; [guide](visual-editing/attached-details.md).
- Base visibility: [OMIT-001](experiments/omit-001.md) covers all 67 base IDs per species in front/side views (268 observations); anatomy indices show pixel sensitivity, not full semantic validation.
- Visibility: [VIS-001](experiments/vis-001.md) audits unchanged IDs in three poses; zero-radius groups separated.
- Focused visibility: [VIS-002](experiments/vis-002.md) finds Catz 55/56 omissions unchanged in 12 pose/yaw combinations; user identifies hidden tongue parts and no tongue-out MCP animation. Current investigation closed; direct visual validation deferred.
- Eye visibility: [EYE-002](experiments/eye-002.md) confirms iris-only omission no-op, host-only equals both in two views/species. GAP-004 stays open.
- Projection: [PROJECT-001](experiments/project-001.md) checks eleven synthetic cases; code-supported arithmetic/order only, no new renders.
- Projection in breeds: [PROJECT-002](experiments/project-002.md); three-pose geometry checks and twelve local MCP comparisons confirm isolated head-to-nose scaling in Petz 4.
- Edited cross-version sample: [PROJECT-003](experiments/project-003.md); Petz 3/5 projection controls match Petz 4 geometry and PNGs, narrowly scoped.
- Second breeds: [PROJECT-004](experiments/project-004.md); Dalmatian/Persian pass isolated projection checks and twelve MCP comparisons.
- Connections: [LINE-001](experiments/line-001.md); twelve MCP comparisons verify endpoint omissions remove a head-to-marker line; parent omission leaves marker visible.
- Connector widths: [LINE-002](experiments/line-002.md); 24 MCP pairs and 36 block checks distinguish zero/zero rejection from single-zero tip clamping.
- Connector order: [LINE-003](experiments/line-003.md); twenty MCP comparisons separate explicit row flags and global fallback, preserving existing lines.
- Add groups: [MORPH-001](experiments/morph-001.md); default group 15 parks a marker, distinct from omission; explicit numerical percentages scale offsets/ordinary size.
- Body areas: [AREA-001](experiments/area-001.md); an ankle connection reassigns the marker from area 8 to 3, changing numerical head-rotation response.
- Line defaults: [LINE-004](experiments/line-004.md); sixteen MCP equivalence pairs confirm short rows, default thickness 25/100, empty fallback and row precedence.
- Latest session: [connector overview](docs/session-2026-11-09-connectors.md), 80 MCP pairs and 174 numerical checks; private inputs/images and original/engine hashes verified.
- Latest: [AREA-002](experiments/area-002.md), 36 numerical checks and eight local MCP pairs: first eligible neighbor row wins; default-pose pixels conceal the classification change.
- Latest: [AREA-003](experiments/area-003.md), 36 numerical checks/eight MCP pairs: lists override connection areas; Head Balls beats Body Balls independent of section order; Lnz Version 1 bypasses lists in sampled species.
- Next: connected chains and other list conflicts, relative-size/multi-group morphs, connector styling and native iris-omission evidence.
- Gaps: visual validation of anatomy maps, multi-view edited tests, version generalization and original-game validation.
- Resume: [HANDOFF.md](HANDOFF.md).
