# Preserve and reshape the existing mouth and muzzle

Authoring requirement: reshape the existing muzzle/snout, nose/nostrils, cheeks, jowls, lips/mouth corners, chin, jaw and tongue in place. Preserve their original IDs, attachment parents, visibility, groups, size references, connectors, projections and valid texture references. Change documented shape/position/size controls deliberately; do not hide, delete, park, suppress through zero effective size or recreate these parts to obtain a cleaner closed-mouth silhouette. A zero Ball Size Override delta is not suppression.

This requirement also applies to [ears and tail](existing-ears-and-tail.md) and other functional anatomy. Additional ornaments do not replace anatomy. Existing baseline omissions can remain; preserving anatomy does not mean unomitting every stock row or making the tongue permanently visible.

## What happened in the Mastiff

The [independent review](../docs/mastiff-authoring-trial-review.md) established that all original added balls 67–94 were omitted. That includes added tongue, cheek, mouth-corner, chin and jowl detail. It did **not** establish that every mouth component was hidden: base jowls 15/39, chin 51, jaw 53, nose 55 and snout 56 remain outside the final omission list. The agent also appended four new jowl balls. Preserved base mouth balls do not compensate for blanket removal of their attached details.

Original Labrador asset comments identify these existing added parts:

| IDs in this exact Labrador | Source label | Preservation concern |
| --- | --- | --- |
| 77 | Tongue | Retain its parent 63 and size reference; zero radius in a closed-mouth sample does not establish that it is unused |
| 78–79 | Cheeks | Keep the existing attachments instead of omitting the stock pair |
| 80–81 | Mouth corners | Preserve both corners, their connectors and valid texture slots |
| 88 | Chin | Preserve the existing attached surface detail |
| 89–90 | Jowl cover-up parts | Do not discard as redundant based on one resting image |
| 91–92 | Jowls | Reshape existing rows rather than omitting them and appending a new pair |

These are asset-reported names for the exact Petz 4 Labrador, not universal addball IDs or game-validated animation roles. Other breeds/species require their own existing-resource mapping. Consult the [Dogz](../format-reference/anatomy/dogz.md) or [Catz](../format-reference/anatomy/catz.md) base-ball indices and effective inherited sections.

## Use existing controls without discarding dependencies

Start from the original mouth inventory, including all attached details and incoming/outgoing Move, Project Ball and Linez rows. A muzzle comprises multiple hosts and dependents; moving one visible ball is not a coherent muzzle edit. Keep the original parent and optional size-reference fields when reshaping an attached cheek, jowl or lip. Check whether young inherits the adult row or defines a separate controlling section before changing either layer.

Use [Move](../format-reference/move.md) for documented local offsets, [Project Ball](../format-reference/project-ball.md) for documented endpoint relationships, and [Add Ball fields](../format-reference/add-ball.md) for existing attached-row coordinates/size. General head controls affect spacing and radius differently; read the [head guide](head-ball.md). The tested head-to-nose projection is a localized control, not a tested full-muzzle recipe. [Face Extension](../format-reference/face-extension.md) now has dedicated scalar controls; [existing-detail controls](../experiments/mouth-002.md) now cover paired cheek, mouth-corner/jowl and chin/jowl offsets. A complete coordinated base-mouth design still needs further work.

The authoring agent should reuse established field behavior, preserve the original functional construction and report an unmet shape requirement when a recipe is missing. It must not invent replacement mouth geometry or independently repeat fundamental research on each task. The shared research priorities below identify the missing knowledge explicitly.

## Tested Face Extension loop

[FACE-001](../experiments/face-001.md) retains the full original construction while testing Face Extension `0`, `-12` and `12` in adult/young Petz 4 blank Labrador and stock Siamese. Use these as diagnostic examples, not a safe interval or finished design. The source scalar may already be nonzero.

1. Read the effective adult and young scalar separately; preserve all inherited sections and original anatomy.
2. Make a small deliberate scalar adjustment, then compare aligned front, three-quarter and profile views against the unchanged source.
3. Review jaw/head continuity and attached surfaces. The control moves a fixed muzzle set, not the whole face; projections can also move details with unchanged parents. In this Labrador even existing ear details 82/83 respond through mouth projections.
4. Check numerical positions when rounding or occlusion hides a change. Keep original size references and frame-dependent visibility. Treat motion and native behavior as untested until separately observed.

## Existing Labrador surface controls

[MOUTH-002](../experiments/mouth-002.md) tests the following exact Petz4 blank Labrador adjustments with original IDs/parents/size references retained. These are controlled primitives, not universal IDs or a finished mouth. Young inherits the adult Add Ball rows in this asset.

| Existing part | Tested change | Review requirement |
| --- | --- | --- |
| Cheek details78/79 | Local x+6/−6 | Check both cheek boundaries in front and profile, adult and young |
| Mouth corners80/81 and jowls91/92 | Paired local x+4/−4 | Retain original host balls and connectors; check joins in raw mouth states |
| Chin/jowl details88–92 | Local y+6 | Diagnostic only: the sampled raw27 preview covers more of the tongue; do not accept from a closed-mouth still |
| Relative tongue detail77 | Ordinary size−1→0, keeping parent/reference63 | Sampled closed presets remain radius0; raw frames retain positive reference-driven size. Zero relative offset does not suppress the tongue |

Only the listed added IDs change numerical geometry in these controls; base mouth anatomy remains unchanged. Coordinate-only controls retain all radii. The relative tongue edit changes only detail77 and equals the original reference63 radius. For a different breed, inventory the actual rows first. Native function, intermediate growth and combined edits remain unvalidated.

## Additional raw mouth states

[MOUTH-001](../experiments/mouth-001.md) inventories Petz4 raw animation data and selects twelve tongue-size-positive frames per species. Existing Labrador/Siamese anatomy is previewed in adult/young with exact local MCP/direct agreement. For example, Dogz animation27/frame5 exposes positive tongue geometry. Use explicit raw frame controls and retain the exact species/version/asset identity; do not assign a panting/eating label or claim native motion from an isolated frame. These additional samples extend the preset review; native expression scheduling and continuous movement remain untested.

## Required mouth review

- Inventory original and final base/added mouth components. Every original row must retain its ID and attachment relationship; identify deliberate coordinate/size/color edits separately.
- Confirm no new omissions, parked groups or effective zero sizes suppress mouth parts. Preserve original conditional visibility and inspect size-reference behavior before treating zero-radius geometry as disposable.
- Preserve texture slots still referenced by hidden or conditionally visible parts. A closed-mouth preview cannot establish that an invalid hidden reference is harmless.
- Review muzzle depth, paired jowls/lips, jaw/chin continuity and nostrils in front and profile, adult and young. Check the mouth after any head or muzzle proportion change.
- Where available, inspect open-mouth/tongue-out, panting, eating/drinking and expressive motion. If the renderer cannot expose these states, record them as untested; standing/sitting/lying stills do not establish mouth function.

## Shared research still required

The preservation rule is firm; the missing design recipes must be researched centrally. Face Extension scalar effects now have [scoped evidence](../experiments/face-001.md). Existing-detail offsets and one reference-preserving tongue adjustment now have [scoped controls](../experiments/mouth-002.md). Remaining priorities are coordinated base-host plus attached-surface width/depth/size design; chin/jaw interactions; sustained open-mouth motion, growth and native-game comparisons. Record species, exact baseline, version/build and tested states with each result, then publish the reusable recipe here. The scalar experiment establishes static renderer behavior; native motion and a complete muzzle design remain unvalidated.
