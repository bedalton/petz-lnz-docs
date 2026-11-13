# ANATOMY-002: reshape existing Labrador ears/tail

Date: 2026-11-13. Petz 4 blank Labrador, local renderer-observed and code-supported. No native-game validation. Authoring outcome: [reusable ear/tail recipes](../visual-editing/existing-ears-and-tail.md). Source copy is the same exact blank used in the [Mastiff trial](../docs/mastiff-authoring-trial-review.md); no Mastiff artifact is modified.

## Reproduction and preservation

Run `scratch/petz-local-venv/bin/python tools/native_anatomy_probe.py` from `/workspace`. [Script](../tools/native_anatomy_probe.py) refuses an existing output directory. Archive a prior run before replay. Inputs, private resource copies, frames, PNGs, returned metadata and eight aligned nearest-neighbor sheets live in `scratch/research/anatomy-002`. [Compact manifest](anatomy-002.json) indexes hashes and derived results; complete numerical coordinates remain private.

The source is `clean_dogs/petz4/Labrador.dog`, SHA-256 `9fb4c5a84a417ae53783e7409d88ac8e0d7c50a4b95670819534a993a36699c0`. A constrained writer strips LNZ comments/blank lines and edits only the existing LR/LRPUP byte spans, padding to the original resource sizes. Resource trees and all other payloads/bytes remain identical. It preserves raw variation directives rather than serializing a selected seed. The unchanged-write control compares both resources at seeds 0–255: 512 section-table equalities. This demonstrates preservation for those parser selections; it is not a game parser proof or exhaustive variation analysis.

Each variant retains 67 base balls, 28 added balls, the original omissions, all parsed Linez, textures and added-ball parent IDs. No added row is inserted/deleted/reordered. No native ear/tail or unrelated mouth detail is hidden. Adult and young own their separate Move/Project/Ear Extension controls; young inherits the adult Add Ball edits. Geometry checks cover all eight variants in standing/sitting/lying and forced adult/young: 48 asset/geometry records. Original animation frames are unchanged for every case.

## Controls and findings

| Variant | Intervention | Changed geometry IDs in sampled poses | Changed images / 12 |
| --- | --- | --- | ---: |
| source | Exact unmodified binary | None | 0 |
| roundtrip | Comment/blank-line compaction only | None | 0 |
| ear70 | Ear Extension=70 in LR/LRPUP | 5/6/29/30/86/87 | 12 |
| ear130 | Ear Extension=130 in LR/LRPUP | 5/6/29/30/86/87 | 12 |
| ear_fold | Append mid-ear self-reference y=8 and tip self-reference y=18 offsets | 5/6/29/30/86/87 | 12 |
| ear_width | Modify local x only on existing added ear details 82–87 | 82–87 | 12 |
| tail_short | Edit existing 57→58,58→59,59→60 projection percentages to 45/75/75 | 58/59/60/94 | 11 |
| tail_lower | Append native 57–60 self-reference y offsets 6/12/18/24 | 57/58/59/60/94 | 12 |

The table lists the union of changed IDs; rounding leaves 58 unchanged in some tail-short cases. All changed-ID sets are recorded per pose/look in the private report and compact manifest. Tail controls do not alter unrelated geometry. Ear width control changes only the six existing attached nodes. Other controls retain every Add Ball field unchanged. Existing Linez and attachment roots remain available; this does not establish animated game behavior.

Ear Extension's source implementation scales Dogz mid-ear 5/29 around the head, then tips 6/30 around their changed midpoints, before Move and Project Ball. Attached details 86/87 follow their existing parents. It does not directly rescale every ear detail or radius. The ear-fold label names a hypothesis; images establish lowered tips, not a fully authored Mastiff fold. The width label also names the control dimension: the tested signs actually compact the front outline because local frames matter.

Tail shortening retains the native chain and existing added tail detail 94, including its 59→94 projection. Standing adult front has identical PNG bytes despite changed numerical tail positions; profiles reveal the change. The lower-tail control retains those projections and changes existing nodes rather than attaching a new chain to the butt.

I inspected all eight sheets: adult/young standing front/profile, sitting profile and lying profile, 64 displayed cells. All 96 raw renders also include resting front views; those remaining 32 images are hash-recorded but are not claimed individually visually reviewed. The static samples show shape changes with original anatomy retained. They are not a finished Mastiff design, a native motion test or evidence of collision-free extreme values.

## Backend and controls

96 fresh real local stdio MCP render calls: eight variants × two looks × three poses × two yaws. Seed 41, fatness 50; forced adult age 100 and forced puppy age 12; yaw 0/90; standing/sitting/lying with returned effective pose/frame metadata retained. The 12 source/roundtrip pairs are byte-identical PNGs. No branch overrides or saved pets are used.

Runtime: renderer 0.1.0, Python 3.12.16, FastMCP 4.1.6, Pillow 13.0.0. Checkout revision 49c7f62eab51b61b9f68801ba7571178670c433e. The manifest records script, installed source, input/dependency, report and image hashes. The five original input/dependency files remain hash-identical after rendering. Renderer source and game files are untouched.

Two preparatory harness failures are preserved privately: `anatomy-002-initial` attempted to edit a nonexistent local young Add Ball section instead of retaining inheritance; `anatomy-002-second` completed geometry but lacked a base64 import before saving renders. Neither is counted in final evidence. The corrected successful run supplies all stated checks and outputs.

## Limits and next shared work

This establishes six reusable nonreplacement controls on one Petz 4 blank Labrador, using the current renderer. It does not establish exact native-game interpretation, genetics, transient expressions, motion blending, sustained growth, combined-control aesthetics, large drooping tails, soft folded-ear volume/taper, other breeds/species/versions or saved-pet routing. These are explicit shared research gaps. Authoring agents should reuse the applicable controls and retain anatomy when a requested result exceeds them.
