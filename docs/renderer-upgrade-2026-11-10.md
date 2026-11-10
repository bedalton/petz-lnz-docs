# Renderer upgrade review

The local Petz4 HTTP MCP was reinstalled and restarted on127.0.0.1:8765/mcp from integration6c1d88325ced89109f8e4b9d724fa8ab6037b42c. All62 installed Python sources match the checkout;the package display version remains0.1.0. The native-port changes named in [RENDERER_CHANGES.md](../RENDERER_CHANGES.md) are c6f1eda/b3dc464 in the upstream source report,not integration commit IDs in this checkout. The pre-existing renderer .gitignore modification is preserved. This research edited no renderer source or original game/saved-pet files.

| Review | Main result |
| --- | --- |
| [UPDATE-001](../experiments/update-001.md) |Restart and source audit,68 focused renderer tests,old/new synthetic changed-path controls,583 historical MCP comparison relationships preserved |
| [UPDATE-002](../experiments/update-002.md) |12 eye controls rebuilt byte-identically;selected shade/motion outcomes confirmed;Dogz geometry/shade snapshots and specific pixel counts corrected;new paint-angle state documented |
| [UPDATE-003](../experiments/update-003.md) |18 old/new views for three available saved pets;all18 new PNGs match MCP,with saved controls preserved |
| [UPDATE-004](../experiments/update-004.md) |64 remaining controls recovered byte-identically;all relationship checks pass,including268 omission observations;corrected old Catz union-count typo |
| [UPDATE-005](../experiments/update-005.md) |32 nested Petz3/5 texture comparisons confirmed;all match current Petz4 PNGs;60 numerical connector checks confirmed |

The32 separately replayed nested LINE-016 comparisons bring the selected historical comparison/contact-sheet total to691. All659 selected top-level historical comparison/contact-sheet controls preserve their tested comparison relationships. This covers37 historical manifests;cross-version PROJECT-003 manifests are separate entries. Exact pixels are not unchanged:all415 initial comparisons carrying old cell hashes drift,and several selected numerical/state measurements change. The manifests and unit reviews identify what was actually checked. Original historical JSON and images remain evidence for9d72d7a;old source-hash verifiers should reject the new installation rather than have their guards removed.

Current important corrections:

- The blanket textured paint/Outline incompleteness statement is withdrawn for this build after differential controls;clothing remains unsupported.
- Non-Outline clipping inset is0;low-version paint texture lookup and add-ball projections follow the new paths. The notice's ordinal paint-column numbering differs from the inspected parser;the full tested rows and caveat are recorded in UPDATE-001.
- Scottie sitting/front retained orientation still drifts,but frame3 changes128 pixels and frame8 changes141. Host-orientation state reproduces the effect;GAP-006 remains an original-game evidence gap.
- Dogz standing-side omission18 shade-only count is68,previously116. Three shade-history counts and18 texture-motion vectors also change.
- The available Homebody saved cache has no configured paint textures,so it does not demonstrate the notice's textured-muzzle claim. Frisky/Chip are unavailable.

Verification commands are in the unit pages. Completed checks include1,166 initial MCP RGBA cells,32 rebuilt-eye cells,400 recovered-control cells,84 slope loads,804 omission assemblies,96 shade-only histories,48 texture-motion histories and their saved transitions/buffers. The static follow-up explicitly separates host orientations from new per-paint angles. Twelve fresh motion baselines,one stock static baseline,eighteen saved-pet baseline matches andsix cross-version stock smoke pairs supplement the comparison replays. Eighteen original engine/executable/breed hashes still match RESTORE-002;three saved-pet inputs stay byte-identical.

All five update verifiers and the focused static verifier pass. Source/dependency/engine/input/report hashes,raw renders,snapshots and health records remain private under scratch/research/update-001 through update-005. No raw game assets are committed. The original-gap tracker and editing references now link the new evidence.

Remaining scope is explicit:the generic pass does not cover every baseline-only/synthetic/history unit;UPDATE-005 separately covers nested LINE-016 reports;only the affected Scottie fixture was rerun for all eight static frames;separate saved-group and paint-angle motion attribution is incomplete;Frisky/Chip and original-game comparisons are unavailable. Native-port golden tests and repeatable MCP images are not original-game validation. Future experiments should use the new source map and retain revision-specific results.
