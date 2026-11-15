# Preserved-mouth research session

2026-11-15; user authorized 30 minutes, beginning 15:29:57 UTC. Research focuses on reusable controls for existing mouth anatomy. Renderer revision `20cd02946c53ea702db789d5b6eeda62c54c429d`; original game behavior remains unvalidated.

## Results and evidence

| Unit | Result | Reproduce / detailed evidence |
| --- | --- | --- |
| Community review | Attributed Face Extension and tongue-reference claims, with version/motion uncertainty retained | [Source review](../sources/mouth-shaping.md); private retrieval metadata and content hashes |
| FACE-001 | Fixed muzzle translation, original projected attachments retained; setting zero can change a nonzero source. Parents alone do not reveal all affected details | [Experiment](../experiments/face-001.md), [reference](../format-reference/face-extension.md), [manifest](../experiments/face-001.json) |
| FACE-002 | Matched stock Scottie/Siamese geometry and pixels agree across sampled Petz 3/4/5 controls. Age 0 has additional juvenile shrink; age 12/100 match forced young/adult geometry | [Experiment](../experiments/face-002.md), [manifest](../experiments/face-002.json) |
| MOUTH-001 | Raw frame data exposes positive tongue geometry beyond the three named presets, without establishing behavior labels or native scheduling | [Experiment](../experiments/mouth-001.md), [manifest](../experiments/mouth-001.json) |
| MOUTH-002 | Existing cheek/lip/jowl detail offsets and a reference-preserving tongue adjustment; a lower surface can cover tongue pixels while its geometry/flags remain intact | [Experiment](../experiments/mouth-002.md), [manifest](../experiments/mouth-002.json), [authoring controls](../visual-editing/existing-mouth-and-muzzle.md#existing-labrador-surface-controls) |

The source and field pages separate source-reported claims, code-supported arithmetic, renderer-observed geometry/pixels and untested native behavior. The new controls preserve existing IDs, parents, optional size references, groups, texture slots, connectors and original omissions. This is a set of scoped design primitives, not a finished muzzle, completed Mastiff or native animation approval.

## Verification

[Aggregate auditor](../tools/check_mouth_session.py), run with `scratch/petz-local-x86-venv/bin/python tools/check_mouth_session.py`, passes:

- 1,218 retained research PNG hashes; 1,344 saved geometry records.
- 46 private breed copies and 19 unique input/dependency hashes; all 21 separately recorded game originals unchanged.
- All 62 installed Python sources agree with checkout and all four experiment reports.
- Six fresh real local stdio MCP renders, one adult standing source per species/version, match retained cross-version baselines; six-tool discovery passes for each explicit version.
- All four public compact manifests match their report/verification hashes.

Private aggregate evidence: `scratch/research/mouth-session-2026-11-15/verification.json`; the [public session manifest](session-2026-11-15-mouth-controls.json) records its digest and tool hashes. The aggregate rehashes retained evidence and checks fresh service controls; it does not rerun the full numerical or RGBA analyses.

The unit auditors separately verify 1,092 source/variant anchor-aligned comparisons plus 360 cross-version RGBA pairs, 720 cross-version geometry pairs, 180 age endpoint equalities and 90 age-zero shrink differences. MOUTH-001 independently re-reads all 29,497 raw frame tongue modifier/coordinate/tag records using integer parsing independent of the renderer's frame decoder. It retains 288 exact fresh direct/MCP comparisons. All 4,608 roundtrip parser selections pass.

FACE-001 and MOUTH-002 full replays preserve all 382 retained PNGs (render outputs plus sheets) and their geometry records. FACE-002 and MOUTH-001 have the specifically described independent audits and fresh backend controls; no complete second sweep is claimed for those units. Successful initial sweeps made 1,188 MCP render calls; the two full replays add 360 and final health controls add six. Preparatory harness/auditor failures are preserved privately and excluded from these counts.

Visual review is deliberately narrower than the hashed corpus: four FACE-001 sheets (80 cells), four MOUTH-002 sheets (48 cells) and four individual MOUTH-001 source previews. Other images remain available for further review without being described as visually approved.

## Resume and remaining work

Start with the [mouth guide](../visual-editing/existing-mouth-and-muzzle.md) and [Face Extension reference](../format-reference/face-extension.md). Use exact original-resource mappings; the Labrador added IDs are not species-wide constants. Reuse the existing controls rather than replacing anatomy.

High-value next steps are coordinated base-host plus attached-surface width/depth/size design; continuous growth and combined-control checks; raw state sequences with native expression overlays; and controlled game comparisons. Raw frame IDs are not panting/eating labels, and positive radii are not proof of visible pixels or native function. The new raw-state evidence extends VIS-002's preset scope while preserving its historical observations.

No renderer source or original game files were edited. Proprietary resources, raw renders and environments remain ignored under `/workspace`. Each research unit updates STATUS/HANDOFF and has its own conventional commit under the required identity. This session does not authorize an automatic continuation beyond the requested duration.
