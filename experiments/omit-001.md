# OMIT-001: base-ball omission sweep

**Renderer recovery review:** [UPDATE-004](update-004.md) confirms the recovered comparison/visibility outcomes on6c1d883. Measurements below are historical except the explicitly corrected Catz omission union count.

Date: 2026-11-09. Status: Petz 4 renderer-observed/code-supported, not game-validated. Scottie and Siamese. Same renderer/runtime as SMOKE-001.

## Method

Run `scratch/petz-local-venv/bin/python tools/omission_sweep.py` for a fresh output directory, or add `--resume` when a checkpoint exists. Fresh runs refuse to overwrite a checkpoint. Archive scratch/research/omit-001 before starting a changed experiment.

Each private breed copy resolves stock variation at seed 0, then adds one synthetic 68-branch omission block: a control plus one variant for each base ID 0–66. Seeds are chosen to select each branch. Every effective section is checked against its intended control; only the target omission row may differ. Typed appearance can also lose lines incident to that endpoint, which is an expected consequence rather than a second input edit. All other typed fields must match.

136 direct standing asset loads validate the 68 branches for each species. Twenty local MCP sheets cover standing yaw 0°/90°, adult age 100, fatness 50. Each sheet contains its own control followed by up to 15 target IDs, aligned at common scale. This produces 268 omission/view observations plus 20 control cells. Different seeds select only the authored omission; no original variation alternatives remain. Sheet rendering uses a fixed raster seed in the renderer. Each cell is compared only with its same-sheet control, avoiding crop-dependent comparisons across sheets.

Private copies, inspection results, PNGs, provenance and atomic progress checkpoints: scratch/research/omit-001. [Public manifest](omit-001.json) records seed maps, hashes, cell order, pixel equality and line counts. Resume verifies source/sweep file hashes and completed sheet PNG hashes. It assumes the renderer/runtime/shared engines remain unchanged; preserve those with the evidence. The initial process was interrupted with exit 143 after 15 sheets; resume completed the remaining five. Final assertions check 20 pages and all 268 unique species/yaw/ID observations.

## Results

| Species | IDs changing pixels at front | At side | In either view | Already omitted base IDs |
| --- | --- | --- | --- | --- |
| Dogz | 53 | 53 | 57 | 4, 5, 28, 29, 65, 66 |
| Catz | 50 | 50 | 54 | 37, 65, 66 |

IDs unchanged in both views:

- Dogz: 4, 5, 14, 28, 29, 38, 63, 64, 65, 66.
- Catz: 27, 28, 37, 55, 56, 57, 58, 59, 60, 61, 62, 65, 66.

All pre-existing omissions correctly remain pixel-identical to control. Other unchanged cases must not be classified as absent anatomy: occlusion, zero size, drawing rules and overlay behavior need separate checks. Only one animation frame per pose was tested here.

The iris IDs (Dogz 14/38; Catz 27/28) do not change either image when omitted. EYE-001 already showed their colors affect rendered eyes. In the current implementation iris commands are drawn through host-eye overlays without applying the iris omission as a separate visibility gate. This is a documented preview behavior, not established native correctness; see GAP-004.

Omitting connected endpoints removes incident parsed lines. Example: Dogz head omission changes line count 70→66; Catz head omission 51→50. Thus pixel differences are not necessarily isolated circles. The first validation attempt incorrectly assumed typed lines would remain unchanged; the final procedure verifies the one-section input change and records the resulting line counts.

Six sheets were visually reviewed: Dogz IDs 0–14 front, 45–59 front/side; Catz IDs 0–14 front, 15–29 front/side. This supports initial regional inspection, not visual confirmation of every anatomical label. The remaining sheets have automated pixel/hash checks only.

## Map implications and next tests

The anatomy indices now show front/side omission sensitivity separately from targeted visual probes. Dogz labels originate from Dalmatian comments while this sweep uses Scottie; cross-breed visual identity still needs testing. Utility IDs 65/66 also have conflicting Dogz stock comments: Dalmatian Ballz Info labels and Scottie Omissions labels swap the z-orientation/z-translation names. Keep those names unresolved.

Next: quantitative geometry for zero-size/occluded cases, other views and frames, omission of iris/host combinations, and another breed per species. Do not mark the full ball atlas game-validated from this sweep.
