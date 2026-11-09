# Diagnose a ball that appears unchanged

Evidence: [OMIT-001](../experiments/omit-001.md), [VIS-001 geometry audit](../experiments/vis-001.md). Tested scope: Petz 4 Scottie/Siamese, standing front/side pixels and three-pose geometry.

1. Confirm the selected adult/young resource and effective master/breed sections. Check input hashes so a renderer is not receiving an older copy.
2. Check the existing Omissions list before adding the same ID again. Keep IDs stable; do not delete rows to hide a detail.
3. Use another camera angle and frame. Some omissions change one view but not the other. VIS-001 finds zero radius for Dogz 63/64 and Catz 57–62 in three poses. Catz 55/56 retain positive radii; occlusion remains unproven.
4. Inspect dependent lines and attached details. Omitting an endpoint can remove connecting lines without deleting its position or every child detail.
5. Handle eyes separately: [eye-color edits](eye-colors.md) affect iris overlays even where omitting the iris ID has no observed effect. Do not substitute a host-eye deletion when only the iris was requested.
6. Record unresolved behavior rather than inventing a universal field rule or anatomical interpretation.

The [Dogz](../format-reference/anatomy/dogz.md) and [Catz](../format-reference/anatomy/catz.md) indices include automated front/side omission sensitivity. That is a discovery aid, not a completed visual atlas. In particular, stock utility-ball comments can conflict and visible regions can involve several base/added balls.
