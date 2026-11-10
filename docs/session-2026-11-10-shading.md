# Fifteen-minute depth shading continuation

Date: 2026-11-10. Requested continuation: fifteen minutes. Research resumed from the texture-authoring handoff and moved to the previously untested Z Shade Slope section. Petz4 adult Scottie/Siamese only, seed0, age100, fatness50. No native-game evidence or renderer fix. The exclusions for clothing, textured paint balls and textured Outline balls remain in [GAP-007](../troubleshooting/rendering-gaps.md#known-incomplete-features-do-not-infer-from-mcp).

| Unit | Question | Evidence |
| --- | --- | --- |
| [SHADE-001](../experiments/shade-001.md) | What does slope change, and how does inheritance affect it? |84 assembly loads,48 MCP pairs,765 rational arithmetic slots,3,328 palette checks,six parser cases |
| [SHADE-002](../experiments/shade-002.md) | Can shading history alone survive a return to the original pose? |96 shade-only histories,384 transitions,192 indexed/RGBA cells,24 exact MCP fresh baselines,88 synthetic update events plus guards/midpoints/slot cap |
| [SHADE-003](../experiments/shade-003.md) | Can omission alter other shading through visible depth bounds? |804 assemblies,23 three-cell counterfactual compositions,23 MCP pairs,46 exact direct/MCP cell links |

Main renderer findings: the sampled absent sections inherit100, while empty resolves0; slope0 still enables depth shading, and -110 gives zero fresh offsets. The shade update gate compares each active ball's midpoint-relative distance with its last accepted distance:10 is retained,11 updates. Keeping only ShadeState through a wider yaw arc changes20/24 final scenes despite equal final ball geometry, ordering and prepared texture orientations. Omitting a depth-extreme ball can change the common shading denominator:11/804 omissions reduce depth,seven change fills,eight change shade-only counterfactual pixels. Equal fills do not guarantee equal shade state or output.

The new [field reference](../format-reference/z-shade-slope.md) is indexed in the [agent entry point](../agent-guides/start.md) and [coverage ledger](coverage.md). The [omissions reference](../format-reference/omissions.md) now explains consequential shading changes. Findings distinguish code-supported equations, direct renderer controls and MCP fresh rendering. Repeatability does not establish native-game fidelity.

## Reproducers and audit

Run each reproducer only into a fresh private output folder; they refuse overwrite. Failed harness/verifier attempts and their causes are documented in the unit pages. Successful private evidence lives under scratch/research/shade-001,shade-002,shade-003.

```
scratch/petz-local-venv/bin/python tools/check_shade_slope.py
scratch/petz-local-venv/bin/python tools/check_shade_history.py
scratch/petz-local-venv/bin/python tools/check_shade_omissions.py
scratch/petz-local-venv/bin/python tools/check_shading_session.py
scratch/petz-local-venv/bin/python tools/check_docs.py
```

All unit verifiers pass. They replay arithmetic and assembly/state controls, verify exact saved indexed pixels/RGBA crops, check copies against original PE boundaries/other resources and audit dependencies/engine/source hashes. Unit3 also checks that loading omissions prunes incident lines, and directly compares46 MCP cells with the matching private composition cells.

The session verifier checks public/private report equality and verified-report hashes, verifies39 cross-unit pixel links (16 SHADE-002 baselines to SHADE-001 and23 SHADE-003 baselines to SHADE-002), checks duplicate baseline input hashes, and compares every installed Python source with the renderer checkout. It saves research-tool hashes, a current game-executable hash, the full source map and its tree digest. It also compares all four Petz4 engine/executable hashes and both original breed hashes with [RESTORE-002](../experiments/restore-002.md): six unchanged original-file links pass. These hash links establish byte agreement with the recorded restoration, not game fidelity.

| Audited quantity | Count |
| --- | --- |
| Saved private copies / unique byte hashes |26 /24 |
| MCP comparison pairs / fresh baselines |71 /24 |
| Slope assembly loads / omission assemblies |84 /804 |
| Isolated retained histories / transition states |96 /384 |
| Omission counterfactual compositions |23 |
| Saved PNGs / decoded RGBA cells |214 /427 |
| Saved private indexed buffers |261 |
| Cross-unit pixel links |39 |
| Installed/checkout Python source matches |62 |

Seven sheets reviewed across the three units. The one-pixel omission control is a numerical finding, not a visual identification. Private summaries: scratch/research/shade-001-verification.json,shade-002-verification.json,shade-003-verification.json,shading-session-verification.json. Source map: scratch/research/shading-source-audit.json, tree digest `72acdc38ea4c7de54053aad0aa07d03608ef6fbb5d4da0321b68d55075736a8a`. Local HTTP MCP discovery/capabilities passed; health record scratch/research/shading-session-mcp-health.json. Actual comparison/baseline rendering uses local stdio MCP with explicit Petz4. Renderer revision9d72d7afd5f7460ef18133c6179caaf8055082d9 remains clean.

Next routes: broader breed/version or young-resource shading controls; component attribution for the single-pixel equal-fill case; other untouched shape/eye/whisker fields; independent native iris/texture/shading evidence. GAP-006 remains open. Future continuations should follow their newly requested duration. Unrelated untracked istall-node remains untouched.
