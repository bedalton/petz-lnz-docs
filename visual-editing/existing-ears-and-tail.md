# Reshape existing ears and tail

Authoring requirement: reuse the baseline's anatomy and attachments. Do not omit, delete, park, suppress through zero effective size or replace an existing ear or tail to achieve a different shape. Do not blanket-hide stock addballs. Additional ornaments are a separate feature, not a substitute for missing knowledge about anatomy.

This page supplies researched controls, so authoring agents need not rediscover the field behavior. Apply the applicable recipe and review the resulting design. If a requested shape exceeds the documented controls, retain the original anatomy and record the specific missing capability for the central research corpus. Do not silently substitute a replacement chain or spend each authoring task repeating fundamental control experiments.

## Scope and evidence

[ANATOMY-002](../experiments/anatomy-002.md) tests the exact Petz 4 blank Labrador used for the Mastiff, adult and forced young, in three poses and two views. It establishes local renderer controls while retaining all 67 base balls, 28 addballs, original omissions, Linez, attachment parents, texture references and variation syntax. Native animation, inheritance and the final Mastiff silhouette are not established. The recipes below are measured starting points, not universal breed presets. No added balls are needed for these changes.

For another baseline, inspect its effective sections and feature IDs; do not copy Labrador's addball numbers into an unrelated file. The [Dogz](../format-reference/anatomy/dogz.md) and [Catz](../format-reference/anatomy/catz.md) indices provide candidate base IDs, but these new recipes have only been tested on this Labrador. Ordinary fixed-control design comparisons remain necessary; they do not require redoing this research.

## Understand the existing construction

For the tested Labrador:

| Feature | Existing components | Editing consequence |
| --- | --- | --- |
| Ears | Base balls 4/5/6 and 28/29/30; existing added details 82–87 are parented to 4/28 or 5/29 | Reshape the base ear and adjust its existing surface details; preserve those parent IDs |
| Tail | Base balls 57–62; 61/62 are already omitted by this baseline; existing added detail 94 is parented to 58 | Keep the original visibility and reuse the visible native chain and its detail |
| Tail projections | Existing ordered pairs 57→58, 58→59, 59→60 and 59→94 | Edit relevant percentages in place; keep the final detail projection and row order |
| Young data | Young has its own Move, Project Ball and Ear Extension; Add Ball is inherited from adult | Update each actual controlling layer; do not materialize a whole new young anatomy table |

A Ball Size Override value of 0 is a zero delta, not a command to hide a ball; the restriction concerns suppressing actual anatomy. Inventory all incoming/outgoing Linez, Move and Project Ball rows before editing. A connected outline is not the attachment hierarchy: Linez joins visible circles, while Add Ball's first column chooses its parent. Retain groups, body-area routing, optional size references, stock mouth/tongue details and valid texture slots.

## Ear length and spread: Ear Extension

Change the existing single value under `[Ear Extension]`. In the tested file it is 100. The 70 and 130 controls both changed all six sampled adult views and all six young views; front views show a more compact and more extended ear outline respectively.

The renderer's operation is more specific than scaling an entire ear mesh: for Dogz it scales base 5 around head 52, base 29 around head 52, then 6 around the already changed 5 and 30 around the already changed 29. Base 4/28 are not directly changed by that operation. Existing Move rows and Project Ball execute afterward. Only the tested attached details 86/87 follow the changed mid-ear parents; not every ear surface node automatically stretches with Ear Extension.

Use this control for length/spread, then adjust existing local details if needed. Do not interpret 130 as a guarantee of a 30% larger final silhouette, and do not use Head Enlargement to isolate an ear change. Field order and limits: [Move](../format-reference/move.md), [Project Ball](../format-reference/project-ball.md).

## Ear posture: move native ear nodes

The `ear_fold` experiment preserves all existing Move rows and appends these diagnostic deltas to the adult and the young's own Move section:

```text
5,0,8,0,5
29,0,8,0,29
6,0,18,0,6
30,0,18,0,30
```

These changed the native mid/tip positions and existing details 86/87, with no new nodes or omissions. All 12 sampled images changed. The example lowers the ear tips in the sampled views; its experiment name does not establish a complete soft folded Mastiff ear.

The fifth value uses each target's own animation-frame rotation for the displacement. Do not change it to skull 52 merely to make a standing image easier to align: references can agree at rest but differ in another pose. Move rows accumulate, so apply a delta once and track it; repeated appends are not assignments. For production editing, revise the accepted row or delta rather than stacking unrecorded attempts.

## Ear outline: reshape existing added details

In the existing Add Ball rows for IDs 82–87, edit local coordinates and, when separately supported, size while retaining parent, row position, groups and references. ANATOMY-002 specifically tests the x-coordinate control: add −6 to local x on even IDs 82/84/86 and +6 on odd IDs 83/85/87. Only those six geometry records changed; all 12 sampled images changed. The front-view outline becomes more compact in this control.

This is the `ear_width` experiment label, not a claim that those signs increase width. Offsets rotate in the existing parent's local frame; raw positive x does not mean screen-right. Read [Add Ball fields](../format-reference/add-ball.md) before selecting a column. These controls do not yet establish a size/taper recipe.

Because the tested young inherits Add Ball, the adult coordinate edit applies to young without adding or copying a young Add Ball section. Preserve that inheritance and the original body-length variation. Inspect both looks to choose a coherent outline.

## Tail length: adjust existing projections

For the tested Labrador's adult and young Project Ball sections, edit these three existing rows in place:

| Existing pair | Tested new percentage |
| --- | ---: |
| 57→58 | 45 |
| 58→59 | 75 |
| 59→60 | 75 |

Preserve every other row, including 59→94 and its original percentage. Do not replace the whole section with this table. The tested original first percentage is 60 in adult and 50 in young; the other two are 100 in both.

Only 58/59/60 and the existing detail 94 changed geometry across the sampled poses. The tail became shorter in the reviewed profiles, with 11 of 12 sampled images changing; adult standing front concealed the difference. This is why a front-only comparison cannot determine whether a tail edit worked.

Projection percentages scale each endpoint relative to its start in row order; they do not define a new absolute tail curve or radius. Keeping the ordered native structure avoids discarding the existing attachment and projection relationships.

## Tail posture: displace native tail nodes

The `tail_lower` control appends these deltas to each layer's existing Move section:

```text
57,0,6,0,57
58,0,12,0,58
59,0,18,0,59
60,0,24,0,60
```

This changes native tail nodes 57–60 and, through existing dependencies, added detail 94. All 12 sampled images changed. Reviewed side views show a lower tail; sitting/lying still need separate inspection because pose-local axes rotate. The control does not establish a fully hanging tail, joint-angle retargeting or freedom from floor contact.

Keep the existing Project Ball rows. They run after these offsets and affect the final curve and detail position. Do not delete a projection because it counters the first movement attempt: choose between the documented posture and length controls, or identify a specific remaining research question. A Move vector changes coordinates, not the source animation rotations. Preserving the source rig is necessary here but does not itself prove game motion quality.

## Acceptance and remaining shared research

Accept a candidate only after confirming unchanged ball counts/order, original omissions, attachment parents, Linez endpoint pairs and variation structure, plus valid texture references. Record the deliberate scalar/coordinate changes. Review both ears, root and tip continuity, the full tail, mouth/tongue/chest details, standing front/profile and resting poses. Inspect adult and young controllers separately. Final binary equality with the baseline is not expected; anatomy identity and required dependencies should be preserved.

Research already completed: ear extension, native ear-tip offsets, existing ear-detail offsets, ordered tail shortening and native-tail posture offsets on this exact Labrador. Future shared work should add genuine folded-ear shape/taper recipes, fully dropped tails with contact checks, motion-frame controls and native observations, then extend to other Dogz/Catz constructions and versions. Do not describe those missing results as available presets or assign their rediscovery to every authoring agent. Until a required capability is documented, keep the anatomy intact and identify the unmet design feature.
