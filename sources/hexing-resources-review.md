# Hexing resources: initial triage

Reviewed 2026-11-13. [Wiki directory](https://petz.miraheze.org/wiki/Hexing_Resources_and_Guides), [link inventory](hexing-resources-inventory.json), [existing source ledger](community-index.md).

This is a useful discovery index, not a specification. Initial review covers the directory and six readable linked tutorials (LNZ Pro 101, LNZ File Details landing page, addgroups, double tails, textures, baby-stage differences). The Rat Shack breed-from-scratch page was attempted but could not be fetched by the web tool. This is not a complete accuracy audit, link-health check or archive/live comparison. No new game or renderer experiments were run.

## Inventory and access

Raw wikitext contains 163 external HTTP(S) bullet entries, 149 pointing through the Internet Archive, representing 162 distinct original URLs. These counts exclude wiki-local PDFs, wiki tutorials and links in prose. The same Thor spreadsheet URL appears live and archived; this is one exact URL duplicate after archive normalization. Similar subjects do not by themselves establish redundant content.

The web browser returned 403 for the directory. Python urllib with a Mozilla/5.0 user agent retrieved HTML, raw wikitext and API wikitext successfully. Private captures: `scratch/research/wiki-hexing-resources/fetch-0.txt` (raw), `fetch-1.txt` (API), `fetch-2.txt` (HTML). The inventory records the raw SHA-256 and both listed and original URLs. Reproduce via `https://petz.miraheze.org/wiki/Hexing_Resources_and_Guides?action=raw`; extract external links from bullet lines and remove `https://web.archive.org/web/<capture>/` to compare original URLs. Original URL recovery does not establish current availability or equivalent content. Archive timestamps are not publication dates.

## What merits attention

| Source / topic | Value for this project | Evidence and next action |
| --- | --- | --- |
| [Carolyn: LNZ File Details](https://homebody.eu/carolyn/downloabx/tutorials/tutorialbits/LNZdetails.htm) | High: a multi-page section reference and species-specific body-area links | Landing page read; follow its individual chunks before extracting claims. It explicitly separates Oddballz-only material. Source-reported, not a unified Petz specification. |
| [Kalium: double-tail inheritance](https://lilaclynx.net/petz/doubletail) | High: breeding and animation failure modes beyond static appearance | Author reports offspring examples and suggests basing added tails on existing tail balls. Our body-area/render tests do not validate genetic inheritance; native breeding trials required. |
| [Carolyn: baby-stage differences](https://homebody.eu/carolyn/downloabx/tutorials/tutorialbits/GivingBabyStagesADifferentLook.txt) | High: directly intersects current young-appearance work | Source reports equal adult/young added-ball counts as a requirement. Compare against [current young reference](../format-reference/young-appearance.md) and its missing-young/count controls; do not treat renderer behavior as proof or disproof of the game's rule. Tooling advice about resource size is historical and unverified here. |
| [Kalium: addgroups](https://lilaclynx.net/petz/addgroups) | High: behavior-triggered feature visibility | Author reports excitement/basket activation and acknowledges uncertainty about the trigger. [Our group controls](../format-reference/add-groups.md) test numerical renderer inputs, not the game behavior scheduler. Keep the trigger claim source-reported. |
| [Shadowfinder: textures](https://petzhexing.weebly.com/textures.html) | Medium/high: concrete texture-list, path and transparency examples | Good authoring explanation; [our texture reference](../format-reference/texture-state.md) and texture experiments cover overlapping renderer questions. Exact crash/path claims need game/tool-version checks. |
| [Filthy Hippie: LNZ Pro 101](https://petz.filthyhippie.net/lnz-pro-101.html) | Medium: readable orientation and section names | Much overlaps existing guides. Extract navigation help selectively; audit absolute statements individually (below). |
| Ball-number charts, eye charts and copy-paste features | Candidate visual/recipe aids | Directory entries inventoried, contents not reviewed here. Compare against existing anatomy/eye references and test species-specific IDs before adoption. |
| Rat Shack: breed-from-scratch and reverse engineering | Promising packaging/format leads | Listed in directory; breed tutorial fetch failed. Contents unassessed. |
| Behavior, genetics, conversion, second-generation failures | Separate research queue | Potentially valuable gaps beyond our appearance workflow; renderer previews cannot validate these systems. Contents mostly unreviewed. |
| Clothes, toys, playscenes, Babyz and Oddballz | Lower priority for current breed appearance work | Keep discoverable; do not merge their rules into Petz Dogz/Catz guidance. Clothing is currently unsupported by our renderer. |

## Specific accuracy and overlap findings

LNZ Pro 101 says the fourth Linez field must always be `-1`. [LINE-005](../experiments/line-005.md) supports explicit fill colors and end-selected fill in sampled Petz 4 Scottie/Siamese renderer controls; [current replay review](../experiments/update-001.md) preserves the tested relationships. Therefore this restriction should not be copied into our renderer authoring guide. That is a renderer-supported disagreement, not new native-game validation.

The same guide's simple head-size explanation is incomplete for our renderer: [Head Enlargement](../format-reference/head-enlargement.md) distinguishes diameter and spacing, including the A=100 boundary. Keep the introductory description as orientation, not a precise formula.

Its claim that adding a zero after paint texture always anchors spots needs a separate field-level review against [saved paint experiments](../experiments/paint-001.md). This review does not adjudicate it. Do not turn a tutorial's shortcut into a universal rule without identifying defaults, field position and version.

The directory has multiple tutorials on iris colors, paint anchoring, texture use, no-grow features, conversion and pet editing. These are topical clusters, not verified duplicates: written/video variants, game versions, screenshots and different failure cases can add information. Retain attribution and one canonical project explanation per topic; link alternate tutorials where they contribute distinct evidence.

## Integration decision

Keep the directory as a lead source. Prioritize LNZ detail chunks, young/adult transitions, tail inheritance and behavioral addgroups. Add concise attributed claims to the existing focused references only after checking applicability and linking evidence. Preserve useful diagrams by linking their pages; do not bulk-copy tutorials or discard older sources based on presentation. Track claims as source-reported, code-supported, renderer-observed or game-validated separately. This initial pass adds navigation and assessment only; canonical technical rules remain unchanged.
