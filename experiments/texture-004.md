# TEXTURE-004: returning to the same pose after motion

**Updated renderer review:** [UPDATE-002](update-002.md) classifies confirmed relationships,corrected counts and state-schema changes on6c1d883. Values below remain historical unless explicitly rechecked there.

Date: 2026-11-10. Explicit retained-state renderer compositions, with local stdio MCP fresh-baseline checks only. Petz4 Scottie/Siamese adult seed0 copies from [LINE-021](line-021.md), appended128×128 marker texture. No native-game validation or MCP animation claim. [Manifest](texture-004.json). Reproducer `scratch/petz-local-venv/bin/python tools/texture_motion_history.py` refuses overwrite; verifier `scratch/petz-local-venv/bin/python tools/check_texture_motion_history.py`. Private evidence scratch/research/texture-004 and audit scratch/research/texture-004-verification.json. Renderer unchanged at9d72d7afd5f7460ef18133c6179caaf8055082d9.

Twelve fixtures (2 species ×3 named poses ×yaw0/90) start with a fresh preparation and draw. Four subsequent draws retain the returned FrameState. Each history ends at the exact initial controls: four repeats; yaw offsets16,32,16,0; head rotations16,32,16,0; or tilt8,16,8,0. All offsets are engine turn/256 units. Animation frame, appearance/topology, age100 and fatness50 stay fixed. Each draw uses fresh line RNG seed1, raster seed1/step0; this does not simulate continuously retained fuzz randomness.

Every final comparison uses five aligned cells: fresh; full retained state; geometry-only retained state; texture-orientation-only retained state; and fresh commands with only the retained sorted/draw order substituted. Final posed ball geometry and bounds equal fresh in every cell. Forty-eight sheets contain240 cells; twelve separate fresh PNGs match local stdio MCP byte-for-byte. Intermediate frames use their own bounds; final comparisons share fresh target bounds. Replay verifies192 transition states,48 before-final states and240 final states against private snapshots, along with saved indexed pixels and sheet crops.

| History (12 fixtures each) | Full changes | Geometry-only changes | Texture-only changes | Order-only changes |
| --- | --- | --- | --- | --- |
| Repeat | 1 | 0 | 1 | 0 |
| Yaw arc | 12 | 12 | 12 | 12 |
| Head arc | 12 | 12 | 12 | 12 |
| Tilt arc | 9 | 9 | 5 | 9 |

Overall34 full-state cases differ from fresh;33 geometry-only,30 texture-only and33 order-only comparisons differ. The repeat change is the known Scottie sitting yaw0 texture trace:121 pixels after the four repeats. Three repeat fixtures have different sort orders without pixel changes, so changed order alone still does not guarantee a visible effect.

Yaw histories change final fill arrays in10/12 fixtures; tilt changes one; head/repeat change none. All motion histories change final sort order in12/12 fixtures. Texture-only and geometry-only resets each fail to reproduce full retained pixels in all twelve yaw/head cases. The counterfactuals isolate supplied state components; they do not prove additive pixel contributions. In particular, changing draw order can change both occlusion and consumption of fresh shared fuzz RNG. No per-primitive attribution is attempted.

The diagnostic head-to-marker textured connector's isolated512×512 raster matches fresh across all48 full histories, even when whole scenes differ. This narrows attribution: these scene changes are not a universal effect on every textured connector. Block/paint/raster records are saved for all five cells. The marker's own texture circle and stock scene remain part of the composed result.

Four sheets reviewed: Dogz standing front yaw arc, Catz sitting side head arc, Dogz sitting front repeat, Catz lying front tilt arc. Differences include facial visibility/order and fur appearance; connector silhouette/texture remains visually stable. All original and reused-copy hashes, sources, engine resources and dependencies are checked. These results establish history dependence in the tested renderer paths, not intended game behavior or a renderer defect. GAP-006 still lacks independent native evidence.
