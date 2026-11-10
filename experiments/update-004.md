# UPDATE-004: recovered early experiment controls

Date: 2026-11-10. Follow-up to [UPDATE-001](update-001.md),using6c1d883. [Manifest](update-004.json). `tools/recover_renderer_controls.py` rebuilds old copies under scratch/research/update-004;every replayed input must match its historical hash. `tools/check_recovered_renderer_controls.py` verifies the64 controls,400 RGBA cells and historical relationships. No originals or historical JSON are edited.

| Recovered unit | Controls | Updated result |
| --- | --- | --- |
| ADD-001 |12 comparisons |**Confirmed** recorded equalities/inequalities;prepare-phase attachment/size assertions pass |
| HEAD-001 |8 comparisons |**Confirmed** edited images differ;prepare-phase size/spacing assertions pass |
| MOVE-001 |8 comparisons |**Confirmed** zero-vector/reference/repetition image relationships;prepare-phase numerical assertions pass |
| HEAD-002 |4 comparisons |**Confirmed** neutral/gated image distinction;above/below numerical loads are outside this recovered replay |
| OMIT-001 |20 contact sheets |**Confirmed** all268 recorded omission-versus-control visibility outcomes |
| VIS-002 |12 contact sheets |**Confirmed** hidden tongue omissions remain unchanged,head controls differ |

The recipes generate42 private copies;38 distinct paths are used by the recovered MCP calls. The omission preparation verifies all68 branch resolutions per species. Numerical prepare assertions are recorded for ADD-001,HEAD-001,MOVE-001 and OMIT-001;this is not a replay of every old numerical field. Images and exact colours can change despite preserved visible/no-op relationships.

**Documentation count corrected:**the old OMIT-001 prose/table said53 Catz IDs changed in at least one view. Its historical JSON already records54;the unchanged-ID list has13 entries out of67,also implying54. New observations match every historical boolean and give54 as well. This was a union-count arithmetic error,not a renderer-induced visibility change. Dogz remains57. Front/side counts remain53/53 Dogz and50/50 Catz. The old JSON is preserved;derived documentation now uses54 with this correction linked.

An initial recovery run stopped after the first omission sheet because the old observation schema uses `yaw`,not `yaw_degrees`. Its evidence remains archived in scratch/research/update-004-observation-schema-attempt. The final pass ran into a fresh folder and passed all64 relationship checks. All previously missing-input top-level controls are now recovered:583 initial+12 rebuilt eyes+64 recovered=659 comparisons/contact sheets reviewed across37 historical manifests (cross-version PROJECT-003 manifests counted separately).

This closes the missing-input list in the initial UPDATE-001 inventory. Nested LINE-016 reports,other baseline-only/synthetic/history experiments and original-game fidelity are not silently certified by this replay. See [the upgrade overview](../docs/renderer-upgrade-2026-11-10.md) for current scope.
