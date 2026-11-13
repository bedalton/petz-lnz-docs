# Agent ingestion assessment

2026-11-13: documentation review only; no independent agent trial, render or game validation performed.

## Readiness

The [agent entry point](../agent-guides/start.md) already routes editing tasks to focused references and provides a controlled editing loop. The [head guide](../visual-editing/head-ball.md) and [attachment guide](../visual-editing/attached-details.md) provide useful procedures with explicit limits. This supports a supervised first attempt, but does not demonstrate a complete picture-to-breed workflow.

The main gap is synthesis: baseline selection, image feature breakdown, prioritizing edits and delivery criteria. [STATUS](../STATUS.md) and [HANDOFF](../HANDOFF.md) also retain conflicting historical “latest” and resume statements. The [coverage ledger](coverage.md) is a research inventory rather than an authoring sequence. Reorganization cannot fill missing tests or establish game fidelity.

## Recommendation

Extend agent-guides rather than copying the corpus to a new folder. Add these pages in a future implementation:

- Picture-to-breed workflow: inputs, species/version, baseline selection, visible versus inferred anatomy, silhouette/proportions, face, markings, details and multi-pose review.
- Feature-to-control map: desired visual change, candidate controls, applicability/evidence level, failure modes and links to canonical references. Untested choices remain hypotheses.
- Task brief template: reference image, private baseline paths, intended style, output expectations and acceptance criteria.
- Delivery checklist: editable output, change summary, reproducible baseline/preview controls, front/side/other-pose review, known mismatches and renderer-versus-game validation status.

Keep start.md short; resolve current versus historical operational facts in a later STATUS/HANDOFF cleanup. Keep existing references and experiments canonical. Markdown is sufficient; add machine-readable formats only when a consuming tool requires them.

## Portability and trial

A receiving agent also needs the reference image, authorized private baseline assets, a working renderer and current invocation instructions. Git intentionally excludes private inputs and raw evidence, so documentation links alone are not a portable execution package. The entry point warns that research scripts are not general editing utilities and some overwrite output folders.

Test the authoring layer with one fresh-agent attempt using one image and authorized baseline. Record clarification needs, control selection, multi-view resemblance, reproducibility and preservation of originals. This trial has not been run. No corpus reorganization was performed during this assessment.

## Implementation follow-up

2026-11-13: the [authoring workflow](../agent-guides/picture-to-breed.md), feature map and task/trial templates are now available through the agent entry point. The proposed layer is implemented; independent trial and historical STATUS/HANDOFF cleanup remain outstanding.
