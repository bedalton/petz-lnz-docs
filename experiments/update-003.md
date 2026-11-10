# UPDATE-003: available saved-pet regression samples

Date: 2026-11-10. Follow-up to [UPDATE-001](update-001.md), integration6c1d883. The available [change-notice](../RENDERER_CHANGES.md) samples are Fuzzkin,Goobe and Homebody. Frisky and Chip are absent; there is no Dalmatian/Calico sample in this check. No original-game captures are used. [Manifest](update-003.json).

`tools/renderer_sample_pets.py` renders three poses ×front/side per pet against the archived historical9d72d7a source and the updated installed package. Inputs remain read-only. `tools/check_renderer_sample_pets.py` verifies old/new input and image hashes,checks updated source hashes,and matches every updated direct PNG byte-for-byte to a fresh local stdio MCP render. Private inputs remain in games/petz4/Adopted Petz;reports and36 old/new PNGs plus18 MCP PNGs/metadata are under scratch/research/update-003. The old source snapshot is the same62-file hash-verified checkout archive used in UPDATE-001.

The tests preserve each pet's saved appearance seed,age and fatness,without overrides. Saved caches remain authoritative;breed text is not substituted. Three input hashes and all resolved age/fatness values are in the manifest. All18 updated views differ from their historical PNGs and match new MCP exactly. PNG differences alone are not per-feature pixel attribution.

| Available sample | Saved age / fatness | Old→new geometry | Paint texture observation |
| --- | --- | --- | --- |
| Fuzzkin |33 /50 |Changed in6/6 views;standing front IDs79/82/89 |Three configured paint-texture entries;three prepared textured paints per new view,zero before |
| Goobe |12 /50 |Changed in6/6 views;standing front IDs83–90 |No configured paint textures in this saved appearance;this is the add-ball projection regression sample |
| Homebody |15 /50 |Unchanged in6/6 views |No configured paint textures in this available saved cache;no prepared textured paints before or after |

Fuzzkin and Goobe provide **confirmed updated renderer observations** consistent with the changed paint/project paths. Homebody's available cache does **not** demonstrate the notice's textured-muzzle claim. All its parsed paint texture indices are absent (-1);loaded texture slots exist and its effective Lnz Version is2. This is a sample-specific evidence limitation,not evidence that paint textures are generally ignored. Frisky/Chip statements remain **source-reported and unvalidated here**;especially do not treat other Scottie stock PNG changes as a test of the missing Chip.pet.

Two old/new pairs visually reviewed: Fuzzkin standing front and Goobe standing side. Renderer appearance differences are small at native resolution,so field/pixel hashes support the quantitative claims. No saved file,breed,engine file or renderer source was changed. Existing clothing/saved-tail limitations remain. This comparison supports renderer regression review,not native-game fidelity or broad saved-group override validation.
