# Mastiff authoring trial: independent review

Date: 2026-11-13. Scope: frozen Petz 4 English Mastiff against its exact blank Labrador base. No breed, authoring tool, prior evidence or guide was edited. No native-game test was performed.

Current authoring policy now requires preserving and reshaping existing ears/tails: [researched recipes](../visual-editing/existing-ears-and-tail.md). The historical finding below that appended nodes have identifiable purposes does not authorize replacement anatomy.

## Verdict

The extra balls have identifiable design purposes; their presence alone is not a defect. The implementation preserves numbering while replacing substantial visible anatomy with appended geometry. It is a reproducible static-preview prototype with specific cleanup and movement questions, rather than a demonstrated game-ready breed.

The author's private evaluation is at `scratch/breed-attempts/english-mastiff/EVALUATION.md` (the shorter supplied path was absent). Read its `evidence/evaluation-002/structure.md`, `guide-use.md` and `problems-and-proposals.md` for the author's account. Some reproduction paths still refer to the former `/workspace/breeds` and `/workspace/lnz-docs` layout; those commands need relocation. This review uses the present paths.

## Independently checked

[Review script](../tools/review_mastiff_trial.py) reads the binaries directly using the installed resource reader and resolves adult/young layers at seed 41. This is independent of the author's audit script, but shares the renderer/parser implementation; it is not an independent game-format implementation.

| Check | Result |
| --- | --- |
| Exact base and input copy | Both SHA-256 `9fb4c5a84a417ae53783e7409d88ac8e0d7c50a4b95670819534a993a36699c0` |
| Frozen final | SHA-256 `d6ff4af9e19a5c5e96055ac6d1851674e513f875469c44e957527ab4135f5256` |
| Resource keys/order | All 118 retained; exactly four payloads changed: LR, LRPUP, string table 6/63/1033, identifier 10/1003/1033 |
| Effective adult and young counts | Each changes from 67 base + 28 added to 67 base + 48 added |
| Original added rows 67–94 | All retained in place; only raw speckle field changes 0 to −1. Parents, coordinates, sizes and other fields match |
| Original Linez endpoints | All 99 original endpoint pairs retained in their original order; 25 rows appended |
| Original added-ball visibility | All 28 old added balls are omitted in final adult and young |
| Selected reference checks | No invalid ball IDs among parsed connectors, parents, size references, omissions, Move, Project Ball, paint hosts and checked override targets at seed 41 |
| Invalid effective texture slots | Eleven per layer, all omitted: 80–88, 91, 92; slot 1/2 references remain with only slot 0 available |
| Fresh local MCP replay | All 34 PNG byte hashes match the recorded evaluation renders and actual retained PNGs |
| Preservation | All 441 task files excluding `.DS_Store`, plus seven exact base/final/dependency input paths, unchanged through successful run |

Base-ball row count remains 67; their appearance values intentionally change. Preserving IDs does not mean preserving appearance. The author's inventory of omitted parts is corroborated by comments in the original Labrador LNZ: tongue 77, cheeks 78/79, mouth corners 80/81, ears 82–87, chin 88, jowls 89–92, chest 93, tail 94. These are asset labels, not independent animation validation.

## Changes that deserve attention

**Broad omissions:** 34 omissions were added, bringing the total from 14 to 48. Hiding replaced ears/tail is understandable. Hiding every stock added ball also removes tongue/mouth/chin/chest geometry. Static closed-mouth previews do not establish whether panting, eating or expressions remain convincing. This is the highest-priority functional review. Restore parts selectively only on a new candidate copy, after identifying intended visual replacements.

**Replacement attachment:** IDs 95–104 are ten ear nodes parented to skull 52; 105–108 are four jowl nodes parented to snout 56; 109–114 are six tail nodes all parented to butt 49. Lines connect tail nodes visually, but their Add Ball parents are not a joint chain. The tail's explicit resolved body area is 13; that does not prove native tail articulation or genetic inheritance. Skull attachment similarly follows the head without establishing native ear articulation. Check actual motion before deciding whether these are acceptable design compromises. The tail-parent choice is also a specific candidate for the [community inheritance tutorial](../sources/hexing-resources-review.md), whose game claims remain source-reported here.

**Invalid hidden textures:** keeping omitted definitions while removing their texture slots leaves dormant invalid references. Omission should not be assumed to make malformed dependencies harmless in the game. Preserve valid unused slots or deliberately remap hidden-row textures in a separate candidate, then compare previews and native loading. This review demonstrates no crash.

**Variation loss:** the author's raw-source review reports one three-way puppy Body Extension variation (−12/−8/−14) replaced by fixed −12. Our seed-41 resolution reproduces −12 on both sides; it does not independently test the other two branches. This can be an intentional single-appearance scope decision, but must be disclosed.

**Writer bug:** reading `tools/build.py` confirms texture selection tests `int(v[1]) not in dark`, where `v[1]` is an outline color and `dark` contains ball IDs. That is the wrong comparison for selecting hosts by ID. Overrides may conceal the visible effect; no visible defect is established by code inspection alone. Fix the writer separately before reuse, with explicit affected-ID and render comparisons.

Six latent adult tail Move rows and retained Labrador sounds/art/name details are reported by the author. These are lower-priority cleanup/scope matters than the missing mouth details and invalid texture references. No automatic cleanup was applied.

## Visual review and limits

I inspected the existing adult, forced-puppy and growth comparison sheets, encompassing all 34 constituent images whose PNGs were freshly reproduced. The head/mask and hanging ears clearly change the character; the body retains substantial Labrador styling. Eyes remain prominent and white, the muzzle reads as smooth rounded lobes, the ears as simplified flaps, and the tail is thin. These are visual design judgments, not numerical photo-fidelity measurements. No claim of photographic agreement is made in this review.

Standing front/quarter/side/rear, sitting side and lying side remain coherent in these samples. Growth previews show changing proportions and tail shape, but five isolated ages are not sustained game growth. Successful previews do not establish mouth/ear/tail animation, collisions, breeding, installation, saved-cache behavior or Petz fidelity.

## What this says about the guide

The trial successfully produced a packaged artifact and reproducible comparisons, while exposing a gap between creating a good still and preserving a functioning animal. The strongest improvements are a preflight that inventories effective resources/references/variations, an anatomy-preservation checklist requiring a reason for each omission, and multi-node examples that distinguish attachment parents, connecting lines, body areas and native movement.

A palette/texture atlas and supported writer would reduce trial-and-error work. The discovered writer bug strengthens the tooling case. The author also reports performing the mandatory unchanged-write control late and skipping required reading: these are adherence failures, not proof that those existing instructions were absent. The author reports prior exposure to an earlier Mastiff attempt; without the transcript, this review cannot independently establish its extent. Treat this as informative trial feedback, not a clean test of an agent using only the guide.

The next practical checks are native mouth/tongue and ear/tail movement, followed by offspring inheritance. Freeze this artifact and compare any repairs as separate candidates.

## Reproduction and evidence

Run `scratch/petz-local-venv/bin/python tools/review_mastiff_trial.py` from `/workspace`. It refuses to overwrite its evidence directory; archive an existing run first. Private output: `scratch/research/mastiff-review-001/verification.json`, `protected-before.json`, `preservation-differences.json` and 34 PNGs. The verification JSON records source hashes, dependency/input hashes, requests, returned controls, image hashes and protected task-file hashes. Backend: real local stdio MCP; renderer 0.1.0, Python 3.12.16, FastMCP 4.1.6, Pillow 13.0.0, pefile 2024.8.26. Checkout revision is 49c7f62eab51b61b9f68801ba7571178670c433e; installed-source hashes are the operational provenance.

Controls reproduce the author's requests: seed 41, fatness 50, adult age 100 or forced puppy age 12, six pose/yaw combinations per breed/look; age-blended standing yaw 45 at 1/6/12/50/100. No branch overrides. Exact returned poses/frames and dependency metadata are retained privately.

An initial run matched all 34 images but failed its final whole-folder preservation assertion without retaining the initial hash map. Its exact cause cannot be established. Outputs are preserved at `scratch/research/mastiff-review-001-incomplete`; that run is excluded from preservation claims. The successful run records its starting map, excludes Finder `.DS_Store` metadata and passes all 441 file comparisons. No authoring/evaluation script was rerun or modified.

Successful verification JSON SHA-256: `b8c6ad79c52705bea7bada4baf16368fd86dc8455d20620f21c93a84760f645e`. All 62 installed renderer Python source hashes equal the author's recorded runtime hashes.
