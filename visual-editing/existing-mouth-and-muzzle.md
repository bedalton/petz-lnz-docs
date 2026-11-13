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

Use [Move](../format-reference/move.md) for documented local offsets, [Project Ball](../format-reference/project-ball.md) for documented endpoint relationships, and [Add Ball fields](../format-reference/add-ball.md) for existing attached-row coordinates/size. General head controls affect spacing and radius differently; read the [head guide](head-ball.md). The tested head-to-nose projection is a localized control, not a tested full-muzzle recipe. Face Extension and coordinated jowl/lip shaping still need dedicated shared controls before offering numerical presets.

The authoring agent should reuse established field behavior, preserve the original functional construction and report an unmet shape requirement when a recipe is missing. It must not invent replacement mouth geometry or independently repeat fundamental research on each task. The shared research priorities below identify the missing knowledge explicitly.

## Required mouth review

- Inventory original and final base/added mouth components. Every original row must retain its ID and attachment relationship; identify deliberate coordinate/size/color edits separately.
- Confirm no new omissions, parked groups or effective zero sizes suppress mouth parts. Preserve original conditional visibility and inspect size-reference behavior before treating zero-radius geometry as disposable.
- Preserve texture slots still referenced by hidden or conditionally visible parts. A closed-mouth preview cannot establish that an invalid hidden reference is harmless.
- Review muzzle depth, paired jowls/lips, jaw/chin continuity and nostrils in front and profile, adult and young. Check the mouth after any head or muzzle proportion change.
- Where available, inspect open-mouth/tongue-out, panting, eating/drinking and expressive motion. If the renderer cannot expose these states, record them as untested; standing/sitting/lying stills do not establish mouth function.

## Shared research still required

The preservation rule is firm; the missing design recipes must be researched centrally. Priorities are controlled Face Extension effects on the entire original muzzle and its dependents; coordinated original jowl/cheek/lip width, depth and size changes; chin/jaw and tongue size-reference interactions; then open-mouth motion, growth and native-game comparisons. Record species, exact baseline, version/build and tested states with each result, then publish the reusable recipe here. No new mouth-shaping or native-motion experiment is claimed by this page.
