# Agent entry point

Read this page first for editing tasks; read STATUS.md and HANDOFF.md when continuing research. This project is an early evidence base, not yet a complete design-from-image system.

Read the [renderer update review](../experiments/update-001.md) before using historical pixels. Textured paint/Outline support has changed; clothing remains unsupported. Keep renderer observations separate from original-game evidence.

## Route by task

| Need | Read next |
| --- | --- |
| Identify base-ball IDs | [Dogz index](../format-reference/anatomy/dogz.md) or [Catz index](../format-reference/anatomy/catz.md); mostly asset labels, not visually tested |
| Enlarge or reshape a head | [Head control guide](../visual-editing/head-ball.md), then [field details](../format-reference/head-enlargement.md) |
| Change iris/pupil colors | [Eye color guide](../visual-editing/eye-colors.md) |
| Move a ball | [Move](../format-reference/move.md); distinguish local rotated offsets from native anchoring claims |
| Add a body-attached detail | [Attachment guide](../visual-editing/attached-details.md) and [row fields](../format-reference/add-ball.md) |
| Connect details or change connector width/order/style | [Linez](../format-reference/linez.md) |
| A connected detail responds differently to head movement | [Body areas](../format-reference/body-areas.md) |
| An added detail is dormant despite visible=true | [Add groups](../format-reference/add-groups.md) |
| Introduce or clear a section | [Inheritance](../format-reference/inheritance.md) |
| A ball edit appears invisible | [Visibility diagnosis](../visual-editing/visibility.md) and [Omissions](../format-reference/omissions.md) |
| Change depth shading | [Z Shade Slope](../format-reference/z-shade-slope.md) |
| Author Texture List slots or modes | [Texture List](../format-reference/texture-list.md) |
| Texture a connector or diagnose a long invisible line | [Connector textures](../format-reference/connector-textures.md) |
| Fuzzy connector pixels change with prior draws | [Connector randomness](../format-reference/connector-state.md) |
| Author paint markings or retain their texture angles | [Paint Ballz](../format-reference/paint-ball.md) |
| Texture changes between repeated static frames | [Retained texture state](../format-reference/texture-state.md) |
| Assess preview reliability | [Evidence gaps](../troubleshooting/rendering-gaps.md) and the relevant experiment |
| Find unresearched topics | [Coverage ledger](../docs/coverage.md) |

## Minimal evidence-aware editing loop

1. Identify species, version, adult/young resource and a private baseline copy. Original game files stay read-only.
2. Inspect the effective breed/master sections and preserve required rows. Never infer IDs from the other species.
3. Write a hypothesis and exact minimal edit. Fix seed, pose, camera, age and fatness. Keep a baseline hash and renderer revision.
4. Render aligned baseline/edited comparisons locally; inspect numerical geometry if the image hides a change. Review diagnostics and at least front/side views before interpreting shape.
5. Test other poses, related feature balls and attached details before treating the edit as a coherent design.
6. Record evidence and limits. Stop a visual claim at the level actually tested; successful previews do not establish native game fidelity.

For new research, use the experiment manifests and scripts as reproducibility examples, not general-purpose breed-editing utilities. Their fixed-span replacements resolve one seed and remove alternative variation branches. Preserve private artifacts before rerunning scripts, which currently overwrite their output folders.
