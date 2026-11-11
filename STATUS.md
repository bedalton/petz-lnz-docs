# Status

- Latest MCP upgrade: [UPDATE-008](experiments/update-008.md), renderer `4c4d3df`; reinstalled in scratch/petz-local-x86-venv and local HTTP restarted (session58703, port8765). Fresh discovery/look schema and six Petz4 adult/young/age renders pass;21 original hashes unchanged. This supersedes older current-build/server statements below. Hosted chat endpoint remains separate.

- Workspace recovery: [RESTORE-003](experiments/restore-003.md). All21 recorded game originals match; six cross-version MCP smoke pairs pass. Copied ARM runtime replaced operationally by scratch/petz-local-x86-venv; local HTTP MCP restarted and render-checked. Full installation completeness remains unverified.

Updated: 2026-11-11

- Upgrade review complete: [current index](docs/renderer-upgrade-2026-11-10.md).659 selected historical comparison/sheet relationships preserved;affected numerical/pixel findings corrected. All missing-input top-level controls recovered. Remaining scope is explicit in the index.
- Renderer upgraded/restarted: [UPDATE-001](experiments/update-001.md),integration6c1d883. Textured paint/Outline blanket restrictions are withdrawn for this build after differential controls; clothing remains unsupported. Historical pixel evidence requires the linked replay review.

- Environment restored: [RESTORE-002](experiments/restore-002.md); game folders corrected, local Petz 4 HTTP MCP connected, six cross-version stdio smoke pairs pass and match prior hashes. Prior private artifacts are still absent.

- Complete: local MCP baseline across six species/version combinations; first copy-only Petz 4 edits and native-resolution visual review.
- Latest inventory: [ANATOMY-001](experiments/anatomy-001.md), with 67 candidate labels per species across versions; [community sources](sources/community-index.md).
- Prior: [BALL-001](experiments/ball-001.md), [manifest](experiments/ball-001.json), [head editing note](visual-editing/head-ball.md).
- Inheritance: [INHERIT-001](experiments/inherit-001.md) confirms whole-section replacement for Key Balls in both sampled Petz 4 breeds.
- Findings: master head IDs Dogz 52/Catz 24; isolated size/color/move edits change renders, but head-ball movement does not move all facial features.
- Latest shape result: [HEAD-001](experiments/head-001.md) separates head radius and spacing effects; eight aligned comparisons and three-pose numerical checks.
- Move: [MOVE-001](experiments/move-001.md) confirms rotated offsets, zero-vector no-op and downstream projection effects. Native anchoring discrepancy tracked as GAP-001.
- Head boundary: [HEAD-002](experiments/head-002.md) confirms A=100 skips spacing while neighboring values activate it.
- Navigation/checks: [agent entry point](agent-guides/start.md), [coverage ledger](docs/coverage.md); tools/check_docs.py checks links, JSON/hash syntax and private-file exclusion.
- Eye colors: [EYE-001](experiments/eye-001.md) distinguishes pupil fill, iris outline and host-eye fill; [editing recipe](visual-editing/eye-colors.md).
- Added details: [ADD-001](experiments/add-001.md) tests attachment, relative radius and omission; [guide](visual-editing/attached-details.md).
- Base visibility: [OMIT-001](experiments/omit-001.md) covers all 67 base IDs per species in front/side views (268 observations); anatomy indices show pixel sensitivity, not full semantic validation.
- Visibility: [VIS-001](experiments/vis-001.md) audits unchanged IDs in three poses; zero-radius groups separated.
- Focused visibility: [VIS-002](experiments/vis-002.md) finds Catz 55/56 omissions unchanged in 12 pose/yaw combinations; user identifies hidden tongue parts and no tongue-out MCP animation. Current investigation closed; direct visual validation deferred.
- Eye visibility: [EYE-002](experiments/eye-002.md) confirms iris-only omission no-op, host-only equals both in two views/species. GAP-004 stays open.
- Projection: [PROJECT-001](experiments/project-001.md) checks eleven synthetic cases; code-supported arithmetic/order only, no new renders.
- Projection in breeds: [PROJECT-002](experiments/project-002.md); three-pose geometry checks and twelve local MCP comparisons confirm isolated head-to-nose scaling in Petz 4.
- Edited cross-version sample: [PROJECT-003](experiments/project-003.md); Petz 3/5 projection controls match Petz 4 geometry and PNGs, narrowly scoped.
- Second breeds: [PROJECT-004](experiments/project-004.md); Dalmatian/Persian pass isolated projection checks and twelve MCP comparisons.
- Connections: [LINE-001](experiments/line-001.md); twelve MCP comparisons verify endpoint omissions remove a head-to-marker line; parent omission leaves marker visible.
- Connector widths: [LINE-002](experiments/line-002.md); 24 MCP pairs and 36 block checks distinguish zero/zero rejection from single-zero tip clamping.
- Connector order: [LINE-003](experiments/line-003.md); twenty MCP comparisons separate explicit row flags and global fallback, preserving existing lines.
- Add groups: [MORPH-001](experiments/morph-001.md); default group 15 parks a marker, distinct from omission; explicit numerical percentages scale offsets/ordinary size.
- Body areas: [AREA-001](experiments/area-001.md); an ankle connection reassigns the marker from area 8 to 3, changing numerical head-rotation response.
- Line defaults: [LINE-004](experiments/line-004.md); sixteen MCP equivalence pairs confirm short rows, default thickness 25/100, empty fallback and row precedence.
- Latest session: [connector overview](docs/session-2026-11-09-connectors.md), 80 MCP pairs and 174 numerical checks; private inputs/images and original/engine hashes verified.
- Latest: [AREA-002](experiments/area-002.md), 36 numerical checks and eight local MCP pairs: first eligible neighbor row wins; default-pose pixels conceal the classification change.
- Latest: [AREA-003](experiments/area-003.md), 36 numerical checks/eight MCP pairs: lists override connection areas; Head Balls beats Body Balls independent of section order; Lnz Version 1 bypasses lists in sampled species.
- Latest: [AREA-004](experiments/area-004.md), 24 numerical loads and eight local MCP pairs: chain propagation depends on added-ID order; all-area-8 cycle stays 8. HTTP MCP discovery/capabilities passed.
- Latest: [AREA-005](experiments/area-005.md), 36 numerical loads and eight MCP pairs: anchored-cycle areas depend on ID order; late lists do not rerun neighbor propagation.
- Latest: [AREA-006](experiments/area-006.md), 42 numerical loads/twelve MCP pairs: lists reclassify omitted markers without restoring visibility or incident lines.
- Latest: [MORPH-002](experiments/morph-002.md), 48 numerical cases/twelve MCP pairs: initially dormant relative-size marker retains zero evaluated size on activation (GAP-005).
- Latest: [MORPH-003](experiments/morph-003.md), 108 numerical cases/twelve MCP pairs: independent group amounts, shared members and dormant head-area prefixes; final geometry can match despite differing transition traces.
- Latest: [MORPH-004](experiments/morph-004.md), sixty asset-backed assembly histories: final geometry/fills match, but 47 batch/incremental cases differ in draw order; repeated-frame controls also matter. No new pixels.
- Latest: [MORPH-005](experiments/morph-005.md), sixty pixel triples and twelve MCP baselines: isolated order changes no pixels; full retained preparation differs in ten Dogz sitting cases (121 pixels each).
- Latest: [TEXTURE-001](experiments/texture-001.md), twelve static pose/views and twelve MCP baselines: Scottie sitting yaw0 changes from frame3; texture-only state reproduces the121-pixel difference (GAP-006).
- Latest: [TEXTURE-002](experiments/texture-002.md), seven exact state replays trace constant-pose angle drift to quantized matrix self-product/rounding; GAP-006 remains open.
- Latest: [LINE-005](experiments/line-005.md), 72 synthetic blocks/36 numerical loads/twenty local MCP pairs: fill -1 selects start, -2 selects end; flat-color reversal controls pass.
- Latest: [LINE-006](experiments/line-006.md),48 raster fixtures/42 numerical loads/twenty MCP pairs: scan-row/polygon edges differ; negative edge colors inherit shaded fill.
- Latest: [LINE-007](experiments/line-007.md),40 raster fixtures/30 numerical loads/sixteen MCP pairs: fuzz clamps0–7; repeated identical direct draws reuse cached offsets.
- Latest: [LINE-008](experiments/line-008.md),96 asset-free history rasters: positive-fuzz/step0-whisker prior draws affect shared RNG; repeat/zero/step1 controls match.
- Latest: [LINE-009](experiments/line-009.md),48 numerical loads/twenty MCP pairs: automatic edge mode tests exact -1/-1; equal pixels can conceal resolved-mode differences.
- Latest: [LINE-010](experiments/line-010.md),168 numerical loads/56 MCP pairs: partial3–9-field rows match full equivalents; omitted end width follows global, omitted draw flag follows before setting.
- Latest: [LINE-011](experiments/line-011.md),twelve composed fixtures/84 history targets/twelve exact MCP baselines: other-pose RNG history changes11/12 scenes; step0-whisker priming changes12/12.
- Latest: [LINE-012](experiments/line-012.md),72 composed rasters: all positive-fuzz connector pixel substitutions explain full whisker0-primed differences in12/12 fixtures; diagnostic connector alone is insufficient.
- Latest: [LINE-013](experiments/line-013.md),30 numerical loads/sixteen MCP pairs: textured-head selection changes connector pixels, untextured-end and explicit fill match; reversed controls agree.
- Latest: [LINE-014](experiments/line-014.md),72 synthetic rasters/120 sample assertions: texture-size rejection precedes fuzz RNG; periods do not wrap oversize connector windows.
- Latest: [LINE-015](experiments/line-015.md),36 numerical loads/sixteen MCP pairs: long textured connector equals marker-only while explicit fill draws; parsed/block eligibility survives.
- Latest: [LINE-016](experiments/line-016.md),60 numerical loads/32 MCP pairs: Petz3/5 sampled connector texture routing matches Petz4 block/texture records and PNGs.
- Next: independent native texture evidence, other list conflicts/whiskers, broader style breeds/versions, evolving fuzzy scenes and native iris-omission evidence.
- Gaps: visual validation of anatomy maps, multi-view edited tests, version generalization and original-game validation.
- Session verification: [2026-11-10 morphs](docs/session-2026-11-10-morphs.md): four units, 36 MCP pairs, 198 numerical morph/list cases and 60 assembly histories; 34 copies/72 RGBA cells/120 snapshots/12 engines verified.
- Pixel/texture session: [2026-11-10 textures](docs/session-2026-11-10-textures.md): three units,24 MCP baseline checks,96 sheets/396 RGBA cells and96 orientation snapshots verified.
- Styling session verification: [2026-11-10 connector styles](docs/session-2026-11-10-line-styles.md): five units,76 MCP pairs,156 breed loads,256 synthetic block/raster/history checks;52 copies/152 RGBA cells/192 RNG states verified.
- History session verification: [partial rows/composed RNG](docs/session-2026-11-10-line-history.md): three units,68 local MCP comparison/baseline checks,168 numerical loads,156 history/intervention compositions;58 copies/92 PNGs/292 RGBA cells/312 RNG snapshots verified, including cross-unit cell links and state-preserving attribution; Catz step0/1 control differences explicitly documented.
- Texture connector session: [overview/verification](docs/session-2026-11-10-connector-textures.md): four units,64 MCP pairs,126 numerical loads,72 synthetic buffers/120 exact samples;42 copies/128 RGBA cells verified; all62 installed sources match clean renderer checkout; handoff duration/scope audited.
- Latest: [LINE-017](experiments/line-017.md), 360 asset-free diagonal rasters/10,512 exact pixel samples: exact-fit thresholds, screen-aligned sampling and 180 reversed-taper equivalences; no MCP/native claim.
- Latest: [LINE-018](experiments/line-018.md),180 asset-free rasters/2,184 samples: viewport corner clamping precedes size rejection; nine of twelve plain cases differ from cropping a larger render.
- Latest: [LINE-019](experiments/line-019.md),30 numerical loads/sixteen local MCP pairs extend texture routing to Petz4 Dalmatian/Persian;256x256 tiles, four sheets reviewed.
- Latest: [LINE-020](experiments/line-020.md),60 asset-free rasters/30,660 body and15,420 edge assertions: sign flag gates shade addition at source10; sampled0 writes directly to indexed buffer.
- Sampling continuation: [session/audit](docs/session-2026-11-10-connector-sampling.md),four units;600 synthetic buffers/43,356 body samples/15,420 edge assertions,10 copies/16 MCP PNGs/32 RGBA cells,30 numerical loads verified. All62 installed sources match checkout; HTTP MCP health passes.
- Sampling audit strengthened: saved LINE-020 edge/background bytes are independently checked against reconstructed flat controls; focused texture reference includes second-breed scope. See the [session audit](docs/session-2026-11-10-connector-sampling.md).
- Final sampling verification reloads all30 saved breed/pose cases against recorded block/texture results and unchanged stock line rows; front/side visual review totals four sheets. [Session evidence](docs/session-2026-11-10-connector-sampling.md).
- Latest: [LINE-021](experiments/line-021.md),90 numerical loads/60 isolated rasters/40 MCP pairs: appended marker slots confirm small tile dimensions hide connectors while explicit fill draws; stock slots/lines preserved.
- Latest: [TEXTURE-003](experiments/texture-003.md),18 parser cases/40 all-byte remaps/144 loads/96 isolated rasters/84 MCP pairs: mode equivalences and visible remap differences; [Texture List reference](format-reference/texture-list.md).
- Latest: [TEXTURE-004](experiments/texture-004.md),48 return-to-pose histories/240 RGBA cells/twelve MCP fresh baselines:34 full scenes differ,all diagnostic connector rasters match fresh; state-isolation controls recorded.
- Texture authoring continuation: [session/audit](docs/session-2026-11-10-texture-authoring.md),three research units;78 copies/184 PNGs/500 RGBA cells,124 MCP pairs+twelve fresh baselines,234 authoring loads+12 history fixtures,20 cross-unit pixel links and48 history fresh-baseline links verified. All62 installed sources match clean checkout; local HTTP MCP healthy.
- Latest: [SHADE-001](experiments/shade-001.md),84 assembly loads/48 local MCP pairs,765 arithmetic slots/3,328 palette checks: absent inherits100,empty resolves0; slope changes shade without geometry changes.
- Latest: [SHADE-002](experiments/shade-002.md),96 isolated shade histories/384 transitions/24 MCP fresh baselines: wider yaw arcs change20/24 scenes with equal final geometry/order/texture orientation;10-distance gate retains history.
- Latest: [SHADE-003](experiments/shade-003.md),804 omission cases/23 local MCP pairs/69 counterfactual cells:11 reduce depth,seven change fills,eight change pixels through shade substitution;46 direct/MCP cell links pass.
- Shading continuation audit: [session index](docs/session-2026-11-10-shading.md),three units;71 MCP pairs+24 fresh baselines,84 slope loads/804 omission assemblies,96 histories/384 transitions,214 PNGs/427 RGBA cells/261 indexed buffers,39 cross-unit links;62 installed sources match clean checkout.
- Focused SHADE-003 follow-up: the equal-fill one-pixel case isolates to ball64 endpoint state; endpoint substitution removes the residual,paint substitution does not. [Evidence](experiments/shade-003.md#equal-fill-case-follow-up).
- Renderer replays: [UPDATE-001 completed review](experiments/update-001.md#completed-historical-mcp-replay),583 comparison relationships confirmed;415 historical cell-hash pairs drift;1,166 new RGBA cells and18 restoration-original links verified. Missing-input and nested-report scope remains explicit.
- Latest revalidation: [UPDATE-002](experiments/update-002.md) confirms rebuilt eye relationships and selected shade/motion outcomes;corrects Dogz records,three shade-history counts,one omission count and18 motion vectors. GAP-006 is128 pixels at frame3/141 at frame8 on the new build; attribution retained.
- Sample regression: [UPDATE-003](experiments/update-003.md),three saved pets/18 old-new views;all18 new views match local MCP. Fuzzkin prepares textured paints,Goobe geometry changes;available Homebody cache has no paint textures. Frisky/Chip unavailable.
- Resume: [HANDOFF.md](HANDOFF.md); latest audit and next research routes are consolidated there.

- Latest: [UPDATE-005](experiments/update-005.md),32 nested Petz3/5 texture comparisons and60 assembly checks confirmed;64 RGBA cells exactly match updated Petz4. Selected upgrade relationships now total691;historical pixels remain revision-specific.

- Latest: [UPDATE-006](experiments/update-006.md),all12 static fixtures replayed:eleven stable through eight frames;Scottie sitting/front retains128/141-pixel drift. 96 sequence+144 reset draws and12 MCP baselines verified.

- Latest: [UPDATE-007](experiments/update-007.md),48 motion histories/192 transitions/336 final draws separate host and paint angles. Host=combined and paint-only=fresh throughout;combined differs from full in33 histories. Existing MCP baseline links only.

- Ten-minute continuation audited: [session evidence](docs/session-2026-11-10-upgrade-continuation.md),UPDATE-005/006/007 verifiers pass;620 PNGs,18 original hash links and62 installed sources checked. HTTP restarted after stale-process discovery;health passes.

- Final continuation provenance:checkout revision and seven tool hashes recorded in the [session audit](docs/session-2026-11-10-upgrade-continuation.md);renderer retains only its pre-existing .gitignore change.

- Final HTTP render control exactly matches the updated Scottie static baseline;health/audit hashes refreshed.

- Latest: [PAINT-001](experiments/paint-001.md),Fuzzkin nonzero paint-angle state changes pixels in24/24 histories;Homebody negative control0/24. 192 transitions/336 final draws/12 new MCP baselines pass;348 PNGs verified.

- Latest: [PAINT-002](experiments/paint-002.md),three paint-angle command substitutions explain all24 Fuzzkin host/combined differences;144 PNGs/48 cross-unit links verified. Two front/side sheets reviewed.

- Latest: [PAINT-003](experiments/paint-003.md),wrong-length paint-state vectors reset all angles:48 short/long controls match host-only;168 PNGs/48 prior links pass. Preserve full indexed state vectors.

- Saved-paint session audited: [evidence/index](docs/session-2026-11-10-saved-paints.md),three units,660 research PNGs/648 final draws/192 persisted transitions/12 MCP baselines.20 original hashes and62-source agreement pass;new Paint Ballz reference indexed.

- Final saved-paint RGBA audit distinguishes two palette-alias counts in PAINT-001 geometry/order controls;all paint-angle counts agree. Details in the [session audit](docs/session-2026-11-10-saved-paints.md).

- Final aggregate independently rehashes all660 PNGs and48 state files;all match their manifests.

- Latest: [PAINT-004](experiments/paint-004.md),216 synthetic commands/180 group-only equivalences and216 color positive controls; nonzero groups diagnose unsupported. Saved-pet group retint remains open.

- Latest: [PAINT-005](experiments/paint-005.md),12 copy-only saved-array mutations retain72 direct views and24 MCP variant views across three Petz4 saves. Skipped prefix data is distinct from cached paint groups.

- Latest: [PAINT-006](experiments/paint-006.md),nine cached group/color copies:36 group equivalences,72 direct draws and18 MCP matches. Fuzzkin color controls change six views;other sampled paints lack visible positive controls.

- Latest: [PAINT-007](experiments/paint-007.md),Fuzzkin ages0/50/100:36 group equivalences,72 direct draws and16 MCP matches;17/18 color controls change pixels.

- Paint-group continuation audited: [session](docs/session-2026-11-10-paint-groups.md),three complete unit replays pass;298 PNGs,21 copies/21 original hash links,64 MCP records,144 RGBA counts and18 cross-unit links verified. HTTP restarted and actual render matches baseline. No native claim.

- Final reference review consolidates current group evidence and species/pet scope;[session audit](docs/session-2026-11-10-paint-groups.md) remains the resume index.

- Latest: [PAINT-008](experiments/paint-008.md),five selective cache copies and216 direct/36 MCP draws: adult supplies color, matched young rows blend geometry by host ordinal, host count mismatch retains adult.

- Latest: [PAINT-009](experiments/paint-009.md),24 same-length reorder fixtures/120 draws: actual active angles equal;distinct test angles misattach by stale index and change23/24 views.

- Latest: [PAINT-010](experiments/paint-010.md),exact opposing directions at age56 reject surface paint or center non-surface commands. 32 direct/8 MCP draws; all opposed/matched sampled RGBA pairs equal.

- Paint matching continuation audited: [session](docs/session-2026-11-10-paint-matching.md),368 direct/44 MCP draws,412 PNGs,9 copies,21 originals,304 RGBA comparisons,42 prior PNG and24 state links verified. Local HTTP health passes.

- Renderer source review questions are collected in private `scratch/renderer-source-review.md`.

- MCP follow-up: local client reconnected and six-tool discovery/render reverified; no user action needed for local research. Chat-host registry reload was attempted but unconfirmed; see [RESTORE-003](experiments/restore-003.md).

- Latest: [MORPH-006](experiments/morph-006.md), current-build Petz3/4/5 replay:144 numerical records and36 local MCP pairs retain relative-size activation behavior;all six fixtures match historical Petz4 geometry. No native claim.

- Latest: [MORPH-007](experiments/morph-007.md),1,728 numerical cases/72 direct rasters separate the nonnegative morph-size gate from earlier-ID radius lookup. Unresolved references or a dormant prior target can yield visible,unparked,radius0 markers. Full replay passes;Petz4 only,no native claim.

- Latest: [MORPH-008](experiments/morph-008.md),936 numerical records/120 direct rasters show row-order-dependent size chains/cycles despite identity-remapped references;fully grouped cycles stay radius0. Full replay passes;Petz4 only,no native claim.

- Relative morph continuation audited: [session](docs/session-2026-11-11-relative-morphs.md),2,808 numerical records,228 research PNGs,36 MCP pairs,192 direct rasters,30 copies,84 RGBA comparisons/four reviewed sheets;all21 recorded originals and62-source agreement pass. Local HTTP restarted andactual render matches fresh direct baseline.

## Puppy/kitten continuation: fresh breeds

[YOUNG-001](experiments/young-001.md):306 local stdio MCP renders and132 aligned relationships pass across Petz3/4/5 Scottie/Siamese on4c4d3df. Age endpoints, aliases, defaults, three poses and front/side views sampled;two Petz4 sheets reviewed. Full replay is underway. No native-game claim or original/renderer edits. Fifteen-minute continuation remains active.
