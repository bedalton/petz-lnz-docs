# Status

Updated: 2026-11-09

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
- Visibility: [VIS-001](experiments/vis-001.md) audits unchanged IDs in three poses; zero-radius groups separated, Catz 55/56 still unresolved.
- Focused visibility: [VIS-002](experiments/vis-002.md) finds Catz 55/56 omissions unchanged in 12 pose/yaw combinations; cause unresolved.
- Eye visibility: [EYE-002](experiments/eye-002.md) confirms iris-only omission no-op, host-only equals both in two views/species. GAP-004 stays open.
- Next: exposed tongue-frame/isolation probes, more frames/breeds, connected details and morphs.
- Gaps: visual validation of anatomy maps, multi-view edited tests, version generalization and original-game validation.
- Resume: [HANDOFF.md](HANDOFF.md).
