# Native capture intake, 2026-11-12

The user supplied game screenshots and a Fuzzkin movement video. This is an intake and visual review, not a controlled renderer/game comparison. Petz4 is the working association from the existing saves; exact runtime/version and screenshot scale are not independently established.

## Inventory and reproduction

Private inputs are under `scratch/screenshots`: 21 PNG screenshots, three saved pets and one MOV. SHA-256 hashes, dimensions, saved appearance cache comparisons, video metadata and twelve decoded frame hashes are in `scratch/research/native-001/inventory.json`. Reproduce with:

```sh
PYTHONPATH=/workspace/scratch/native-media-deps scratch/petz-local-x86-venv/bin/python tools/inventory_native_captures.py
```

Pillow handles stills; PyAV19.0.2 handles video, with linked library versions recorded in the manifest. PyAV was extracted privately under scratch after a uv wheel extraction permission failure; renderer sources were not modified. Video is H.264, 2046×1472, 2.43 seconds, 138 decoded frames. Samples retain original dimensions. Private contact sheets `contact.png` and `video-contact.png` were visually reviewed, as was the full new Goobe PNG. Contact sheets are navigation aids, not pixel comparison evidence.

The user reports possible Mac2× rendering, older screenshots mostly near adoption, no available puppies/kittens, Scottie images depicting Chip, and lowercase cat-name prefixes matching Adopted Petz names. Preserve these as user-reported provenance. Exact scaling is unresolved; differing crop dimensions and adjacent repeated pixels do not independently establish a uniform2× transform. Do not rescale originals or treat screenshot dimensions as pet geometry.

## Save associations

| Capture | Matching save | Interpretation |
| --- | --- | --- |
| Fuzzkin movement video | `scratch/screenshots/Fuzzkin-walkaround.pet` | User reports snapshot immediately afterward; snapshot means saved pet file here, no separate Fuzzkin PNG found |
| New Goobe front/tongue photo | `scratch/screenshots/dogz/great-dane/Goobe--2026-11-12-645.pet` | User supplied contemporaneous pair; actual path differs from the initially described scratch/workspace path |
| Homebody photo | `scratch/screenshots/catz/Homebody.pet` | Existing save candidate, no exact capture-time guarantee |
| Scottie photos | `games/petz4/Adopted Petz/Chip.pet` | Identity user-reported; older capture-time state uncertain |
| Frisky photos | `games/petz4/Adopted Petz/Frisky.pet` | Filename/identity association; older capture-time state uncertain |
| Boston Terrier photos | Unresolved | Breed folder alone does not identify an individual save |

New save age fields are Fuzzkin69, Goobe51 and Homebody12; prior copies have33,12 and15 respectively. These are `biorhythms[8]` values, which the installed renderer reads as its saved age input; they are not verified real-world ages or proof of puppy/adult status. Each new save differs from the prior same-name file, while both adult and young cached appearance texts match exactly. Other saved state can still affect appearance.

## Observed game evidence and limits

Goobe's latest screenshot clearly displays an extended red tongue and a top hat. His apparent coat is substantially lighter than in the older Great Dane images. This is an observed difference, not an attributed cause; illumination, saved state, age, tinting or other effects have not been isolated. Clothing support is a separate renderer limitation.

The video shows Fuzzkin moving through different orientations in the yard. Natural animation means head/body pose, screen location, occlusion and camera projection can change together. It supplies useful game appearance references but does not isolate fixed-pose texture drift. No exact yaw or forced-pose correspondence is claimed.

The tongue screenshot confirms visible tongue appearance in this Dogz example. It does not validate Catz55/56 labels, iris omission, morph activation, or an unedited renderer's tongue animation. Those require targeted controls.

## Next use

Start with the contemporaneous Fuzzkin and Goobe saves for qualitative multi-view comparisons. Keep old photos as separate historical appearance states. Establish image scaling from scene/UI pixel structure before quantitative alignment. A fixed-view idle clip would complement the moving video for texture-state questions, but no additional capture or breed installation is required for this intake.
