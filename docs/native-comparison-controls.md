# Native comparison controls

The November12 captures provide game-observed appearance references. They do not yet supply a controlled native-game validation of renderer geometry, animation, color or LNZ edits. Use the [capture intake](native-capture-intake-2026-11-12.md) for identity, chronology and unresolved runtime provenance.

| Question | Evidence and present boundary |
| --- | --- |
| Which saved state should a preview use? | [NATIVE-002](../experiments/native-002.md): three old/capture-time pairs have matching caches; age/fatness differ. At matched controls all288 sampled source pairs match in the renderer. Native effects of other state remain open. |
| Can the stills be reduced without interpolating samples? | [NATIVE-003](../experiments/native-003.md): all21 PNGs have unique exact cropped2× grids among tested factors2/3/4. Every source RGB pixel reconstructs, including clipped borders. This does not establish engine resolution or pose scale. |
| Which copies preserve color interpretation? | [NATIVE-004](../experiments/native-004.md): use original-profile tagged or converted sRGB copies under `scratch/research/native-004`. Earlier untagged reductions are sample-grid evidence only. |
| Does the moving video have the same exact grid? | Twelve lossy decoded samples fail exact2× replication; the underlying display scale is unresolved. No fixed-pose texture-drift conclusion follows. |
| Is Goobe's historical coat change explained? | No. Same cache texts, bounded prefix arrays and ICC profile tags do not identify a changed input explaining the reddish historical versus tan/gold current native appearance. |

Keep source PNGs/saves/video unchanged. Use paired capture-time saves where available and preserve old photos as historical states. Preview stock poses/yaws are comparison candidates, not recovered animation states. Screenshot backgrounds, tongue expressions, clothing, head rotations and occlusion can differ even when broad body orientation looks similar.

Any future numerical native comparison must record the exact runtime/resources, saved input, pose/expression, camera/scale and color pipeline. Until those correspondences are established, report visible similarities/differences qualitatively and keep renderer-only substitutions separate. Repeated previews and exact MCP/direct matches establish reproducibility rather than native fidelity.
