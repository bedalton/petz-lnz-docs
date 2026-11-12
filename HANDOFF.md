# Handoff

- Latest completed session: [puppy/kitten appearance and audit](docs/session-2026-11-11-young-appearance.md), YOUNG-001/002/003 on4c4d3df. Three full replays and final audit pass;606 research PNGs,606 numerical age records,204 cross-version pixel matches,21 unchanged originals. Local HTTP restarted/rechecked in session82886. Fifteen-minute continuation complete;next work needs a new requested duration.

- Latest MCP upgrade: [UPDATE-008](experiments/update-008.md), renderer `4c4d3df`; reinstalled in scratch/petz-local-x86-venv and local HTTP restarted (session58703, port8765). Fresh discovery/look schema and six Petz4 adult/young/age renders pass;21 original hashes unchanged. This supersedes older current-build/server statements below. Hosted chat endpoint remains separate.

Updated: 2026-11-11

## Resume

Read AGENTS.md, STATUS.md and agent-guides/start.md; use docs/coverage.md for remaining topics. Latest completed research is the [puppy/kitten session](docs/session-2026-11-11-young-appearance.md), YOUNG-001/002/003, on renderer4c4d3df. Use `scratch/petz-local-x86-venv/bin/python` on this x86 host. Local HTTP MCP restarted on port8765 in managed session82886 after final audit found the earlier process absent; recheck on resume. Earlier build/server notes below are historical.

The latest user authorization is this fifteen-minute continuation only. Follow the next requested duration and do not infer an ongoing longer run. Update STATUS/HANDOFF and commit each logical unit. Identity: bedalton <3941960+bedalton@users.noreply.github.com>; conventional titles preferably under50 characters, hard limit65; never coauthors. Original-game behavior remains unvalidated.

## Known incomplete features

Clothing remains unsupported. The earlier blanket textured paint/Outline limitation is withdrawn for integration6c1d883 after changed-path controls; see [UPDATE-001](experiments/update-001.md). Original-game appearance remains unvalidated. [GAP-007](troubleshooting/rendering-gaps.md#known-incomplete-features-do-not-infer-from-mcp) preserves the quote, evidence level, version/build uncertainty and conditions for revisiting the restriction. Ordinary connector texture and flat outline-color tests do not establish support for these paths.

## Earlier container recovery (RESTORE-002)

[RESTORE-002](experiments/restore-002.md): user restored games; moved nested games/games/petz3–5 to games/petz3–5. Local Petz 4 HTTP server is running at http://127.0.0.1:8765/mcp in this container session; real HTTP discovery/capability call passed. Six stdio inspect/render pairs pass and match prior SMOKE-001 records exactly. New private evidence: scratch/research/restore-002. Previous private experiments remain missing; do not assume their copies/checkpoints exist. Dependencies freshly resolved; manifest records engine and dependency hashes. No source changes.

## Persistence and historical environment

Only /workspace is guaranteed persistent. Python 3.12.16 environment is scratch/petz-local-venv; uv cache and managed Python are under scratch. Use uv --link-mode copy on this mount (default cached-wheel installation failed with permission errors). Setup commands: experiments/smoke-001.md and petz-renderer-mcp/docs/local-mcp.md.

Renderer is a separate ignored checkout now at6c1d88325ced89109f8e4b9d724fa8ab6037b42c,noneditable installed package reinstalled and HTTP restarted(PID8300,port8765). All62 installed sources match. The pre-existing .gitignore modification remains;this research did not edit renderer source. Earlier9d72d7a audits are historical. No source fixes made. No renderer AGENTS.md found at research start. Local stdio MCP works; hosted available as fallback. Saved .pet support is Petz 4 only. Use `git -c safe.directory=/workspace ...` if ownership checks require it; author/committer configuration is repository-local.

Private inputs/copies/images/provenance live under ignored scratch/research/<experiment-id-lowercase>. games/ and renderer checkout are also ignored. Older experiment scripts overwrite output folders: archive evidence before changing/rerunning them. OMIT-001 instead refuses a fresh run over an existing checkpoint and supports --resume with source/sweep/PNG hash checks. Its resume assumes unchanged renderer/runtime/shared engines; check these before continuing across environment changes. Checkpoints are replaced atomically.

## Completed research

README.md indexes the experiment writeups and manifests. All behavior findings remain renderer/asset/code evidence, not native-game validation.

- SMOKE-001: Scottie/Siamese inspection/renders across Petz 3/4/5.
- ANATOMY-001: 67 candidate labels per species from Dalmatian/Siamese; cross-version label/key agreement, not complete visual semantics.
- BALL-001, HEAD-001/002: head anchors Dogz 52/Catz 24; isolated changes differ from coherent feature edits. Head Enlargement uses A+B for base diameters, A-B for spacing with an A!=100 gate confirmed in three poses.
- INHERIT-001: absent/empty/partial/full Key Balls confirms whole-section replacement in sampled Petz 4 breeds.
- MOVE-001: local rotated offsets, self-reference default, zero-vector no-op, cumulative rows and downstream projections. Community anchoring claim remains GAP-001.
- EYE-001: eight reviewed MCP comparisons plus 30 numerical pose loads separate pupil fill, iris outline and host fill. Right iris appears viewer-left in tested front view. Recipe: visual-editing/eye-colors.md.
- ADD-001: 42 numerical loads / 12 comparisons; ordinary head-attached marker does not automatically enlarge, optional size-reference radius follows head, omission hides without deleting. Parent/marker pixel deltas can differ through scaling/rotation. See add-ball reference/attached-details guide.
- OMIT-001: all 67 base IDs per species at front/side, 20 sheets / 268 omission observations. 57 Dogz and54 Catz IDs (union-count typo corrected in UPDATE-004) change pixels in at least one view. Six sheets reviewed; other sheets checked automatically. Iris omissions are no-ops through current overlay path (GAP-004), not evidence of absent irises. Connected endpoints lose lines. Dogz utility labels 65/66 conflict among stock comments. Process exited 143 after 15 sheets; resume finished five, then added numerical line counts without rerendering sheets.

- VIS-001: three-pose numerical audit of all unchanged OMIT-001 IDs. Dogz 63/64 and Catz 57–62 have zero radius; Catz 55/56 remain positive (4 standing, 1 sitting/lying), initially leaving occlusion as a hypothesis; see subsequent user clarification in VIS-002. No new renders. See [writeup](experiments/vis-001.md), manifest and tools/visibility_geometry.py.

- VIS-002: local MCP, 12 sheets / 24 target observations for Catz 55/56 across three poses and four yaws. All unchanged; head controls all change. User subsequently clarified that the tongue is hidden inside the mouth and provided MCP animations lack tongue-out animation. Current investigation closed as expected hidden anatomy on user-reported context; direct visual validation deferred. Three sheets visually reviewed. See [writeup](experiments/vis-002.md). Uses unchanged OMIT-001 private copy; atomic resume checks in tools/visibility_views.py.

- EYE-002: right iris/host/both combinations in Scottie/Siamese, standing front/side; four local MCP sheets all reviewed. Iris equals control; host changes; both equals host. Prepared iris visibility is false even in control (assembly hides standalone iris), unlike earlier posed geometry. No line-count changes. See [writeup](experiments/eye-002.md), tools/eye_omission_probe.py. GAP-004 remains open.

## Latest code-only research

[PROJECT-001](experiments/project-001.md): eleven asset-free projection assertions pass, covering percentages, truncation, row order, invalid IDs and Move ordering. [Reference](format-reference/project-ball.md). Run tools/projection_probe.py with the restored environment; output manifest has source hashes. No MCP or native claims.

## Latest asset-backed research

[PROJECT-002](experiments/project-002.md): explicit empty versus head-to-nose 100/50/150 Project Ball rows in Scottie/Siamese. Three poses checked numerically; twelve front/side standing MCP comparisons, all eight edited sheets reviewed. Only target raw coordinates change; identity controls equal. Script refuses existing output directory. Private files under scratch/research/project-002. Native fidelity unvalidated.

## Latest cross-version sample

[PROJECT-003](experiments/project-003.md): same projection controls in Petz 3/5; 24 additional local MCP comparisons, numerical checks in three poses/species/version. Geometry and PNG hashes match Petz 4. Four sheets reviewed. tools/projection_breed_probe.py now accepts --game-version; shared adult helper defaults to petz4. First harness failure archived; numerical resolver must receive game_version explicitly. More breeds and other edited fields remain pending.

## Latest breed expansion

[PROJECT-004](experiments/project-004.md): Dalmatian/Persian Petz 4 projection controls pass three-pose geometry and twelve MCP comparisons. Four side sheets reviewed. tools/projection_breed_probe.py --alternate-breeds; refuses overwrite. adult helper now permits filename/selector keyword overrides, keeping old defaults. Two breeds/species sampled for this field only.

## Latest connected-detail research

[LINE-001](experiments/line-001.md): marker versus connected marker, with marker/head omissions, in Scottie/Siamese Petz 4. Eighteen numerical species/pose/pair checks and twelve front/side MCP comparisons. Four sheets reviewed. Either omitted endpoint removes connector; head omission leaves marker visible. Width 100/100 produces broad taper. tools/connected_detail_probe.py refuses overwrite; preserves effective Linez rows explicitly. Fields/reference and attached-detail/omission guides updated. Styling/order, other breeds/versions and morph groups remain pending.

## Latest connector-width research

[LINE-002](experiments/line-002.md): 36 direct posed-endpoint block checks and 24 local MCP pairs, six sheets reviewed. Zero/zero rejects block; single-zero tip clamps to 1 if other end positive. Equal percentages scale against separate endpoint radii. tools/line_width_probe.py refuses overwrite. Direct blocks bypass camera/shading, distinguished from actual MCP images. Draw order and other styling remain pending.

## Latest connector-order research

[LINE-003](experiments/line-003.md): 36 numerical loads, isolated endpoint schedules and twenty MCP comparisons; four before/after sheets reviewed. Column 10 0/1 overrides global; -1 follows Draw Linez Before Ballz (1 before, 0 after). Existing parsed lines serialized explicitly and checked unchanged. Ordering is endpoint-relative, not global topmost. tools/line_order_probe.py refuses overwrite.

## Latest add-group research

[MORPH-001](experiments/morph-001.md): unused group 15 default dormant, distinct from omission. 24 direct numerical percentage checks in three poses, twelve MCP default-state pairs, four sheets reviewed. Direct 100% geometry equals static group0, ordered 100→0→50 equals direct50 geometry. No explicit-activation MCP images/automatic animation claims. tools/add_group_probe.py refuses overwrite. Reference and visibility guide updated. Relative-size/multi-group/body-area and native runtime tests pending.

## Latest body-area research

[AREA-001](experiments/area-001.md): 42 numerical variant/pose checks and eight default-head-pose MCP pairs; two sheets reviewed. Head marker area0 inherits8; ankle connection reassigns8→3 even explicit8; explicit1 stays1. Omitted ankle restores8; marker omission area0. Direct head_rotation32 changes only area8 marker. Effective Siamese ankle area3 differs from built-in2; failed harness assumption archived. tools/body_area_probe.py refuses overwrite. Multi-neighbor/list precedence and native semantics pending.

## Latest line-default research

[LINE-004](experiments/line-004.md): 36 numerical checks and sixteen MCP equivalence pairs, two sheets reviewed. Two-field rows resolve defaults; global thickness25/100 matches full rows; explicit25 overrides global100; empty section falls back100. Existing line styles frozen explicitly. tools/line_defaults_probe.py refuses overwrite. Missing-section inheritance and partial3–9-field rows remain untested.

## Session verification and navigation

[Session overview](docs/session-2026-11-09-connectors.md) indexes five units: 80 MCP pairs, 174 numerical checks, 18 reviewed sheets. tools/check_recent_evidence.py verifies 62 private inputs, 80 PNGs, original breed hashes and 12 shared-engine files without rerendering. All pass. Agent routes/attached-detail controls updated. Next targeted topics: multi-neighbor area precedence, relative-size/multi-group morphs, connector fuzz/edge/color, other connector breeds/versions, native validation.

## Next research

Iris/host combinations are now sampled by EYE-002; seek native evidence before resolving GAP-004. Do not keep investigating Catz 55/56 no-ops in supplied poses: the user explained the hidden tongue and missing tongue-out animation; see VIS-002 for attribution and limits. Test more frames/angles and another breed per species before promoting visual atlas identities. Consider left-pair/other-breed checks and independent native evidence. Expand connected added details, body areas/morph groups, remaining shape/color/texture sections and edited cross-version checks. Do not repair ambiguous renderer behavior without a reproducer and evidence of intended native semantics.

## Checks and safeguards

Run `scratch/petz-local-venv/bin/python tools/check_docs.py` for Markdown targets, JSON/hash syntax and private-file exclusion. Rebuild docs/coverage.md with tools/coverage_index.py. tools/anatomy_inventory.py regenerates label indices and includes OMIT-001 sensitivity if its manifest exists. Update generators when changing generated docs.

tools/research_common.py checks unchanged resource metadata, unrelated payloads and bytes outside a fixed adult LNZ span. It serializes seed-resolved sections, removing comments/variation alternatives: this is not a general variation-preserving resource editor. Original game files remain read-only. No complete native-validated anatomy atlas or concept-to-breed workflow exists yet; website deferred.

## Latest conflicting-neighbor research

[AREA-002](experiments/area-002.md): 36 numerical checks across Scottie/Siamese and three poses; first eligible connection wins, area1/8 neighbors skipped, endpoint reversal unchanged, omitted first neighbor lets second win. Eight local stdio MCP default-head-pose pairs are pixel-identical; two sheets reviewed. Direct head_rotation32 moves only area8 marker. Installed evaluation source matches checkout; four Petz4 engine hashes match RESTORE-002. tools/body_area_neighbors.py refuses overwrite; private evidence scratch/research/area-002. Next: body-area-list overrides, connected chains/cycles, relative-size/multi-group morphs or connector styling. No native-game claims. Local HTTP MCP was already running after this restart; discovery/capabilities passed, no restart needed.

## Latest body-area-list research

[AREA-003](experiments/area-003.md): 36 numerical checks in Scottie/Siamese, three poses; Lnz Version3 Body Balls/Head Balls override connection-derived marker area3 with area1/8. Both lists resolve8 regardless of textual order. Synthetic Lnz Version1 bypasses lists; this is a format flag, not game version. Eight default-head-pose MCP pairs pixel-identical; two reviewed. Direct head_rotation32 moves only area8 markers. Four engine hashes and installed evaluation source verified. tools/body_area_lists.py refuses overwrite; private evidence scratch/research/area-003. Next: connected chains/cycles, omitted-marker/list interactions, other list conflicts/whisker handling, relative sizing/groups or connector styling. No native claims.

## Latest chain research

[AREA-004](experiments/area-004.md): 24 numerical loads, 72 marker rotation checks and eight local stdio MCP pairs. Three-marker A–B–C chain resolves 8/3/3 in forward ID order, 3/3/3 in reverse ID order; reversed line rows unchanged. All-8 cycle remains8. Default-pose pairs identical; two sheets reviewed. Private evidence scratch/research/area-004; script tools/body_area_chains.py refuses overwrite. Engine/evaluation-source and original hashes verified. Existing HTTP MCP discovery/capabilities passed. No native claims. Next: anchored cycles, omitted-marker/list interactions, relative-size/multi-group morphs or connector styling.

## Latest anchored-cycle research

[AREA-005](experiments/area-005.md): 36 numerical loads, 72 marker rotation assertions, eight local stdio MCP pairs (all equal, asserted), two reviewed sheets. Triangle A/B/C linked to area3 D resolves differently with ID order; omitted D restores cycle area8. Late Head Balls C override leaves already-derived A/B areas3. Source/engine hashes verified; no native claims or renderer changes. Script tools/body_area_cycles.py refuses overwrite; private evidence scratch/research/area-005. Next: omitted-marker/list interactions or other lists/whiskers, relative-size/multi-group morphs, connector styling.

## Latest omitted-marker research

[AREA-006](experiments/area-006.md): 42 numerical loads/twelve local MCP pairs, two sheets reviewed. Late lists restore omitted marker areas1/8 without visibility or incident lines; hidden area8 geometry rotates numerically. Version1 bypasses lists. Initial incorrect harness assumption about parsed line retention was corrected; failed copies archived. Source/engine/original hashes verified. tools/omitted_area_lists.py refuses overwrite; scratch/research/area-006 private evidence. No renderer/native claims. Next: relative-size/multi-group morphs, other list conflicts/whiskers or connector styling.

## Latest relative-size morph research

[MORPH-002](experiments/morph-002.md): 48 numerical cases, twelve default-state local MCP pairs, two reviewed sheets. Group15 head-relative size20 retains evaluated size0 at positive percentages, so radius equals reference head; 100% geometry equals static relative0, differs from static relative20. Offsets scale normally; ordinary group15 size20 fully activates to static ordinary20. Ordered100→0→50 equals direct50. GAP-005 records uncertain native semantics; no renderer repair. Three installed sources/four engine hashes verified. tools/relative_morph_probe.py refuses overwrite; private scratch/research/morph-002. Next: multiple groups/update ordering, body-area prefix exceptions, other lists/whiskers or connector styling.

## Latest multiple-group research

[MORPH-003](experiments/morph-003.md): 108 numerical cases, twelve default-state MCP pairs, two reviewed sheets. Groups14/15 independent; A/C share14. Reversing distinct updates preserves final morph/posed geometry, but 48 cases have different transition traces. Dormant head-area additions extend prefix yet remain parked and match dormant body-area pixels. Full100/100 equals static-all. Final geometry does not imply persistent sort/shading equivalence. Three source/four engine hashes verified; tools/multiple_morph_probe.py refuses overwrite; private scratch/research/morph-003. Next: retained-state assembly/order/shading, other lists/whiskers or connector styling.

## Latest retained-history research

[MORPH-004](experiments/morph-004.md): sixty asset-backed Python assembly histories, no new MCP pixels. Batch/incremental final geometry/bounds/fills match; 47 draw orders differ. Six retained AB/BA pairs differ; two repeated-frame no-update controls also change order (Dogz sitting), so avoid attributing all differences to morphs. Cycle leaves different shade distance caches in 12 cases, current offsets/fills match. Non-prefix histories rejected; unused/noop batch snapshots equal directAB. Reused MORPH-003 private inputs verified; six installed sources/four engines match. tools/morph_history_probe.py refuses overwrite; full private snapshots scratch/research/morph-004, compact public manifest. Next: pixel consequences/independent native evidence, other list conflicts/whiskers or connector styling.

## Ten-minute session verification

[Session index](docs/session-2026-11-10-morphs.md) links AREA-006 and MORPH-002/003/004. tools/check_morph_session.py verifies 34 copies, 36 PNGs, 72 RGBA cell hashes, 120 assembly snapshots, original hashes, installed versions and 12 engine files. All pass; private output scratch/research/morph-session-verification.json. HTTP MCP live discovery/capabilities pass; health record scratch/research/morph-session-mcp-health.json. Six sheets reviewed. GAP-005 remains uncertainty, no speculative repair. Existing unrelated untracked istall-node left untouched.

## Latest retained-state pixels

[MORPH-005](experiments/morph-005.md):60 direct three-cell sheets (180 cells), twelve byte-identical local MCP baselines, two sheets reviewed. Order-only substitution changes no pixels despite47 changed sort orders. Full retained preparation changes121 pixels in all ten Dogz sitting cases; prepared commands differ, geometry/fills match. Fresh line RNG seed1/raster step0 held every draw; texture FrameState persisted. Exact texture-state cause still to isolate. Nine installed sources/four engines verified. tools/morph_pixel_probe.py refuses overwrite; scratch/research/morph-005 private evidence. Next: repeated static frames and independent geometry/texture-state resets; no native claims.

## Latest static texture research

[TEXTURE-001](experiments/texture-001.md): twelve stock pose/view fixtures,36 sheets/216 RGBA cells, twelve byte-identical MCP first frames, three reviewed sheets. Scottie sitting yaw0 changes121 pixels on frame3,131 on frame8, without morphs. Third-frame texture-only retained state exactly reproduces full-state pixels; geometry-only/fresh match frame1. Ball42 texture angles drift by(0,-1) each repeat; numerical origin/native semantics pending GAP-006. Six installed source/four engine hashes verified. tools/static_texture_probe.py refuses overwrite; scratch/research/texture-001 private evidence, two-frame initial run archived. Next: Q8 orientation arithmetic trace/independent native evidence; no speculative renderer fix.

## Latest texture arithmetic trace

[TEXTURE-002](experiments/texture-002.md): seven exact replayed frame2–8 states for Scottie sitting ball42. Constant Q8 matrix self-product has last row(-2,-4,255), giving rounded(0,-1) angle delta. Identity self-product control stays identity. Sampler write-back not needed to match this specific trace. Two installed sources/four engines/dependencies verified. tools/texture_arithmetic_probe.py refuses overwrite, requires TEXTURE-001 full private snapshots. No new pixels/MCP or renderer fix. GAP-006 now has numerical origin but still lacks independent native evidence.

## Pixel/texture session verification

[Session index](docs/session-2026-11-10-textures.md) links MORPH-005/TEXTURE-001/002. tools/check_texture_session.py verifies96 sheets,396 RGBA cells,24 MCP baselines (including twelve saved morph baseline PNGs),96 full/private orientation state hashes, sources/dependencies/engine hashes. Final HTTP MCP discovery/capabilities pass; private health record scratch/research/texture-session-mcp-health.json. Five sheets reviewed. Focused format-reference/texture-state.md and agent route added; README evidence links consolidated. All checks pass. Next: independent native evidence for GAP-006, broader breeds/versions or connector styling. No renderer changes.

## Latest connector fill research

[LINE-005](experiments/line-005.md): 72 synthetic blocks,36 numerical loads,twenty local MCP pairs; two sheets reviewed. Flat diagnostic color180/200 controls confirm -1 selects start,-2 selects end including endpoint reversal. Synthetic -3/texture/shade cases pass but have no textured-breed/native claim. Installed/checkout sources,dependencies,three resource DLLs and original hashes recorded. Two failed-report harness runs archived privately; final evidence scratch/research/line-005. No renderer changes. Next: edge modes/colors and fuzz or independent native texture evidence.

## Latest connector edge research

[LINE-006](experiments/line-006.md):48 isolated rasters,42 numerical loads,twenty MCP pairs; two sheets reviewed. Modes -1/0/1/2 and edge colors180/200/-1 tested with fill220. Negative edges inherit shaded fill; explicit edges bypass fill shading (initial fill125 equivalence assumption failed and archived). Initial obsolete-variant harness also archived. Final scratch/research/line-006; no renderer/native claims. Next: fuzz/default edge selection or native texture evidence.

## Latest connector fuzz research

[LINE-007](experiments/line-007.md):40 isolated rasters,30 numerical loads,sixteen MCP pairs; two reviewed sheets. Fuzz -1=0 and8=7, positive1/7 differ from0. Same renderer/block repeats preserve pixels/RNG/table after first draw; fresh seed1 matches. Other history/height/whisker interactions not yet sampled. Final scratch/research/line-007; no renderer changes/native claims.

## Latest random-history research

[LINE-008](experiments/line-008.md):96 asset-free rasters; other-fuzz and step0-whisker histories change all12 target fixtures, short+other history changes9. Repeat,zero,step1,short-same controls all equal fresh. Full states private scratch/research/line-008/states.json; installed/checkout sources verified. No MCP/breed/native claims. Next: actual composed fuzzy breed history/default edge selection or independent native evidence.

## Latest automatic edge research

[LINE-009](experiments/line-009.md):48 numerical loads,twenty equal MCP pairs; two sheets reviewed. Explicit sentinel -2 resolves -1 only for exact edge colors -1/-1; -2/-2 resolves0. Inherited flat edges conceal mode differences. No omitted-column test despite parser-default code lead. Final scratch/research/line-009; no renderer/native claims. Next: partial3–9-field rows or actual fuzzy breed histories/native evidence.

## Ten-minute connector styling session

[Session index](docs/session-2026-11-10-line-styles.md) links LINE-005 through009. Five units:76 MCP pairs,156 numerical breed loads,256 synthetic block/raster/history checks; eight sheets reviewed. `tools/check_line_session.py` passes52 private copies,76 PNGs,152 RGBA cells,192 full RNG/table states,public/private reports,sources/dependencies/resource DLLs/originals. Summary scratch/research/line-session-verification.json. HTTP discovery/capabilities pass,health scratch/research/line-session-mcp-health.json. All units committed, no renderer changes, no native fidelity claims. Current user request was a ten-minute continuation; no ongoing longer-duration authorization assumed. Next: partial3–9-field rows,actual fuzzy breed histories/textured connectors or independent native evidence. Unrelated untracked istall-node remains untouched.

Final aggregate audit corrected LINE-005 synthetic count to72 (2 texture states ×2 endpoint orders ×3 shade pairs ×6 fields); total direct cases256. Counts now asserted by the session verifier.

## Latest partial-row research

[LINE-010](experiments/line-010.md):168 numerical loads,56 equal MCP pairs; two sheets reviewed. Prefix lengths3–9, globals thickness25/73 and before1/0; start-only width does not set end width. Actual omitted edge/draw columns now sampled. Private scratch/research/line-010; no renderer/native claims. Next: composed fuzzy breed history, malformed syntax only if useful, textured connectors or broader breeds/versions.

## Latest composed line-history research

[LINE-011](experiments/line-011.md):12 fixtures,84 history targets,12 eight-cell sheets,12 exact MCP baselines; two sheets reviewed. Fixed prepared scenes,targetstep1,discarded prior pixels. Same-step1 repeat/whisker1 controls equal fresh; other-pose history changes11/12,step0-whisker/fuzz3 priming changes12/12. Prior-scene-step0 changesthree Catz sideviews. Whole-scene attribution only; no retained FrameState or native simulation.168 RNG/table states private scratch/research/line-011/states.json. Reuses LINE-007 fuzz7 copies, verified hashes. Next: connector-only attribution, broader styles/species/version or native evidence.

## Latest connector pixel attribution

[LINE-012](experiments/line-012.md):12 six-cell sheets/72 compositions,144 before-target/after-scene RNG states; two sheets reviewed. Diagnostic connector-only swaps leave residual; all positive-fuzz connector pixel swaps reproduce primed12/12 and restore fresh12/12, while main-path state is preserved. Fresh/primed cells match LINE-011 exactly; no new MCP. Initial four-cell exploration archived privately, final scratch/research/line-012. No renderer/native claims. Next: other history attribution, broader breeds/versions, textured connector controls or native evidence.

## Second ten-minute connector continuation

[Session index](docs/session-2026-11-10-line-history.md) covers LINE-010/011/012.68 local MCP comparison/baseline checks,168 partial-row numerical loads,84 composed history targets and72 intervention compositions. Six sheets reviewed. `tools/check_line_history_session.py` verifies58 unique copies,92 PNGs,292 RGBA cells,312 RNG snapshots,sources/dependencies/resource DLLs/originals; summary scratch/research/line-history-session-verification.json. [Focused connector state reference](format-reference/connector-state.md) added to agent routes. No renderer/native claims. Next: broader breeds/versions,texture-bearing connectors,evolving retained scenes or independent native evidence. Untracked istall-node untouched.

Final local HTTP MCP discovery/capabilities pass; private health scratch/research/line-history-session-mcp-health.json. Renderer checkout remains unchanged.

Final integrity audit extends the session verifier to cross-unit cell links,all-fuzzy substitution equivalences,diagnostic-only residuals and preserved final main-path states. All pass; see the session index for details.

Final scope clarification: fresh step0 versusstep1 differs in six Catz fixtures and zero Dogz fixtures; MCP validates step0 only. History/intervention targets hold step1 fixed. Separate these effects from the three prior-step0 Catz side-view changes; detailed counts in LINE-011.

## Latest asset-backed connector textures

[LINE-013](experiments/line-013.md):30 numerical loads,sixteen MCP pairs; two sheets reviewed. Equal base color125,head stock texture(slot1 Dogz/0 Catz),untextured marker. Head-selected negative fill differs from explicit125; end-selected equals explicit; reversed endpoint controls pass. Loaded/remapped texture hashes recorded,private scratch/research/line-013. No renderer/native claims. Next: texture raster size limits/sampling,broader breeds/versions or native evidence.

## Latest connector texture window research

[LINE-014](experiments/line-014.md):72 asset-free rasters,28 accepted/44 rejected,120 exact centerline samples; untextured controls all draw. Raster width includes fuzz; oversized texture windows reject before RNG/table generation. Period0/8 outputs match; centered x/y crops bias opposite ways on odd spare space. Private synthetic pixels scratch/research/line-014/pixels.json. No MCP/native/renderer changes. Next: actual breed oversized connector controls.

## Latest composed texture-size controls

[LINE-015](experiments/line-015.md):36 numerical loads,sixteen MCP pairs; two sheets reviewed. Offsets -80/-800 compare textured,explicit125 and absent line within each distance. Long textured line parses/builds but raster empty and MCP equals marker-only; long explicit remains visible. Stock256x256 tiles. Private scratch/research/line-015. No renderer repair/native-limit claim. Next: other tile thresholds,version/breed texture routing or native evidence.

## Latest cross-version connector textures

[LINE-016](experiments/line-016.md):60 numerical loads,32 local MCP pairs across Petz3/5; all block/texture records and PNG/cell hashes match Petz4 LINE-013. Two sheets reviewed. Metadata versions explicitly checked (display name remains Petz4 Renderer). Version belongs on ResourceResolver and MCP CLI, not load_breed_assets; two harness attempts archived. Final private scratch/research/line-016/{petz3,petz5}. No native/general-version claims; long-line limits and RNG histories not expanded. Coverage matrix updated narrowly.

## Third ten-minute connector continuation

[Texture session index](docs/session-2026-11-10-connector-textures.md) links LINE-013/014/015/016. Four units:64 local MCP pairs,126 numerical loads,72 synthetic buffers,120 exact texture samples; six sheets reviewed. `tools/check_line_texture_session.py` verifies42 copies,64 PNGs,128 RGBA cells,private/public reports,raw synthetic pixels,sources/dependencies/resource DLLs/originals and explicit MCP game-version metadata. Summary scratch/research/line-texture-session-verification.json. [Connector textures](format-reference/connector-textures.md) added to agent route. No renderer/native claims. Next: other breeds/tile sizes,threshold/diagonal sampling,evolving retained scenes or independent native evidence. Untracked istall-node untouched.

Final HTTP MCP discovery/capabilities pass; health scratch/research/line-texture-session-mcp-health.json. Actual comparisons used local stdio processes with explicit versions.

Full installed-source audit:62 Python sources match renderer checkout; hash map private scratch/research/line-texture-session-source-audit.json,tree digest in the texture session index. Session verifier checks it. No source modification or native-fidelity promotion.

## Latest diagonal texture research

[LINE-017](experiments/line-017.md): 360 asset-free direct rasters,216 accepted/144 rejected,10,512 exact samples and180 reversed endpoint/taper pairs. Exact-fit tiles draw; one-pixel-short width/height rejects before RNG. Screen-aligned sampling holds across six slopes/directions and fuzz0/1/7. Plain support supplies window bounds; no clipping/signed shading/MCP/native claim. Private pixels/samples scratch/research/line-017/pixels.json hash-linked from manifest. Source hashes match installed/checkout; renderer unchanged. Reproducer tools/line_texture_diagonal.py refuses overwrite. Next: clipping or signed/shaded sampling, other breeds/evolving scenes or independent native evidence.

## Latest clipped texture research

[LINE-018](experiments/line-018.md):180 asset-free rasters,128 accepted/52 rejected,2,184 exact fuzz0 samples. Viewport corner clamps precede texture size guard; tile24 draws all cases on24x24 canvas. Nine of twelve plain geometry cases differ from cropping large translated controls; outside lines can collapse onto borders. Positive-fuzz support/RNG checks do not independently trace corner math. Private pixels/samples scratch/research/line-018 hash-linked; sources match checkout. No renderer/MCP/native claims. Next: signed/shaded paint,broader breeds/evolving scenes or native evidence.

## Latest second-breed connector textures

[LINE-019](experiments/line-019.md): Dalmatian/Persian Petz4,30 numerical loads/sixteen local stdio MCP pairs; two side sheets reviewed. Head-selected texture differs from explicit125,untextured end equals it,endpoint reversals agree. Both selected textures slot1 hair10,256x256,has_levels true/own_level-1. No new tile dimension or broader version/size/fuzz claim. Inputs/originals/source/engine/loaded texture/remapped paint/PNG/cell hashes recorded,metadata petz4 asserted. Private scratch/research/line-019. Initial ad-hoc selector lookup used incorrect DA/PE; inspected resource names resolved DM/PR before making copies. No renderer/native claims. Next: signed/shaded sampling or evolving histories/native evidence.

## Latest texture shade/sign research

[LINE-020](experiments/line-020.md):60 synthetic rasters,30,660 body/15,420 edge assertions,75 zero-index writes. All-byte art,offsets-128/-1/0/1/127,sign flags,edge modes-1/0/1,horizontal/vertical. Sign true shades only source<10; false shades all modulo256. Texture samples bypass flat-color substitutions; explicit edges unchanged. Background254 plus flat mask prevents zero/254 samples from being mistaken for absence. No exporter/remap configuration/MCP/native claim. Private pixels/samples scratch/research/line-020 hash-linked,sources match checkout; no renderer change. Next: session evidence audit,composed other tile dimensions/evolving scenes or native evidence.

## Fourth ten-minute connector continuation

[Sampling session index](docs/session-2026-11-10-connector-sampling.md) links LINE-017/018/019/020. Four units:600 synthetic rasters,43,356 body samples/15,420 edge assertions,30 breed loads,sixteen local MCP pairs. Two sheets reviewed. `tools/check_line_sampling_session.py` verifies all persisted pixels/samples,private raw hashes,reversal/crop/shade controls,10 copies/16 PNGs/32 RGBA cells,original leaf boundaries,source/dependency/engine hashes and62-source whole-tree agreement. Summary scratch/research/line-sampling-session-verification.json. HTTP discovery/capabilities pass;health scratch/research/line-sampling-session-mcp-health.json. Renderer unchanged,no native claims. Next: composed other tile dimensions,retained evolving textured scenes or independent native evidence. Latest request is ten minutes only; do not infer longer authorization. Untracked istall-node untouched.

Final sampling audit additionally reconstructs LINE-020 flat masks,checks their saved hashes and verifies every saved edge/background byte,not only body samples/counts. Focused texture reference now explicitly states LINE-019 second-breed scope. All checks pass; no new native claim.

Final sampling numerical audit now actually reloads all30 LINE-019 cases,checks variant pose-geometry invariance,block colors/paint presence,texture config/dimensions/hashes and remapped paint. All pass. Two additional front sheets reviewed;LINE-019 now has four reviewed sheets total (front/side for each breed). Originals and renderer remain unchanged.

The final reload verifier also re-parses each original adult layer and asserts all preceding stock connector rows survive every variant unchanged. Duration and evidence scope remain limited to this ten-minute continuation.

## Latest fifteen-minute continuation

[Texture authoring/motion session](docs/session-2026-11-10-texture-authoring.md) indexes LINE-021, TEXTURE-003 and TEXTURE-004, their reproducers, controls and complete audit counts. New [Texture List reference](format-reference/texture-list.md) is indexed for agents. Main findings: authored tile dimensions can suppress connectors; distinct modes can yield identical sampled pixels; returning camera/head controls to their original values can retain scene differences despite identical ball geometry. The tested diagnostic connector remains unchanged through those histories. Renderer evidence only; no native claim or renderer fix.

All three unit verifiers and `tools/check_texture_authoring_session.py` pass. The session verifier checks cross-unit and fresh-baseline pixel links, report hashes and all installed source files against the clean checkout. Private evidence is under scratch/research/{line-021,texture-003,texture-004}; audit, source map and HTTP MCP health use scratch/research/texture-authoring-*. Two failed LINE-021 harness attempts remain archived privately; see its writeup. Originals and renderer unchanged; unrelated untracked istall-node untouched.

Next: custom art, young resources/broader versions, other evolving scenes, or independent native texture/iris evidence. GAP-006 remains open. Latest authorization was this fifteen-minute continuation only; follow the next requested duration.

## Latest depth shading research

[SHADE-001](experiments/shade-001.md): Petz4 Scottie/Siamese,84 assembly loads/48 local MCP pairs,765 synthetic arithmetic slots/3,328 palette assertions. Absent section inherits100; empty equals0; -110 yields zero fresh offsets; -220 reverses0 response. [Reference](format-reference/z-shade-slope.md). Two sheets reviewed; verifier checks copies/PE boundaries,assembly,RGBA crops,sources/dependencies/engines. Private scratch/research/shade-001; two failed pre-MCP attempts archived and documented. Renderer/originals unchanged; no native claim. Next: retained shading threshold/history controls; this fifteen-minute continuation is ongoing.

## Latest isolated shade histories

[SHADE-002](experiments/shade-002.md):96 shade-only retained histories,384 transitions,192 indexed/RGBA cells,24 exact local MCP fresh baselines. Wider yaw changes20/24 scenes;repeat/small yaw none;head arc offsets change3 but no fills/pixels.88 synthetic events distinguish distance10/11 and active-slot retention;guard/midpoint/512-slot controls included. Two sheets reviewed; private scratch/research/shade-002. Verifier replays all states/compositions and checks baseline links/provenance. No renderer/native claim. Next: omissions affecting bounds/shading or other unresearched sections; fifteen-minute continuation remains ongoing.

## Latest omission/shade interaction

[SHADE-003](experiments/shade-003.md):804 base omission assemblies,23 three-cell shade counterfactuals,23 local MCP pairs/46 exact direct-MCP cell links.11 omissions reduce depth,seven change fills,eight change shade-only pixels;793 depth-preserving cases retain shade/fills.12 copies,69 indexed/RGBA cells checked,three sheets reviewed. Private scratch/research/shade-003; verifier checks loader incident-line pruning separately. Renderer/originals unchanged; no native claim. This fifteen-minute continuation is entering final integrity audit.

## Fifteen-minute shading continuation audit

[Session index](docs/session-2026-11-10-shading.md) consolidates SHADE-001/002/003 and exact verification counts. All three unit verifiers and tools/check_shading_session.py pass:26 saved copies/24 unique hashes,71 MCP pairs+24 fresh baselines,84 slope loads/804 omission assemblies,96 retained-shade histories/384 transitions,23 omission counterfactual compositions,214 PNGs/427 RGBA cells/261 indexed buffers,39 cross-unit pixel links. Seven sheets reviewed. All62 installed Python sources match the clean renderer checkout; local HTTP MCP discovery/capabilities passes. Sources/tool hashes,executable hash and health are private scratch/research/shading-*. No renderer/native claim; GAP-006/007 unchanged.

Next: other breeds/versions/young-resource shading;component attribution for the one-pixel equal-fill omission case;untested shape/eyes/whiskers;or independent native evidence. All requested research stays in copies; unrelated istall-node untouched. Latest authorization is this fifteen-minute continuation only; follow the next requested duration.

Final focused follow-up: [SHADE-003 equal-fill attribution](experiments/shade-003.md#equal-fill-case-follow-up), tools/check_shade_equal_fill.py,isolates the one-pixel Catz sitting-front omission44 residual to ball64 endpoint state. Endpoint substitution matches held pixels;paint substitution leaves the residual. Four extra direct draws,not additional saved buffers. Particular connector attribution remains open. Private result scratch/research/shade-003-equal-fill-attribution.json.

## Renderer upgrade in progress

[UPDATE-001](experiments/update-001.md): reinstalled noneditable package from6c1d883,restarted local HTTP MCP (PID8300),health passed.68 focused renderer tests pass;asset-free old/new controls confirm paint textures,Outline interiors,clip inset correction,legacy paint mapping and12 add-ball projection cases. No renderer source changes;pre-existing .gitignore modification preserved. Full top-level historical MCP replay underway under scratch/research/update-001; do not run old source-hash verifiers as if they validate the new build. Historical reports remain intact.

## Completed renderer MCP replay

[UPDATE-001](experiments/update-001.md#completed-historical-mcp-replay):583 top-level comparison relationships confirmed,415 known cell-hash comparisons drift,168 only carry equality evidence,565 PNG bytes differ. Six stock cross-version inspect/render pairs pass with changed PNGs. tools/check_renderer_update.py verifies1,166 RGBA cells,392 distinct inputs and18 restoration-original hash links. Sources match6c1d883.76 controls initially pending;rebuilt eyes and latest numerical/state checks are in UPDATE-002;64 other missing-input controls and nested LINE-016 remain outside this pass. Historical JSON/raw evidence preserved.

## Updated eyes and numerical/state evidence

[UPDATE-002](experiments/update-002.md),public manifests update-002.json/update-002-static.json. Rebuilt12 eye copies exactly;8 pairs+4 pages confirm old relationships with changed pixels.84 slope loads:all42 Dogz snapshots change,42 Catz match;within-build slope assertions pass.96 shade histories retain outcomes butthree pixel counts change.804 omission sweep outcomes stay11 depth/seven fill cases;Dogz side omission18 shade count116→68.48 motion histories keep aggregate counts but18 vectors change;new paint_angles state must be considered. Static Scottie sitting/front now128 pixels frame3,141 frame8;host-orientation-only and combined texture match full,paint-only/geometry/fresh stay baseline. Both update/state and static verifiers pass. Historical JSON/snapshots preserved;remaining missing-input controls64.

## Available saved-pet upgrade regressions

[UPDATE-003](experiments/update-003.md):Fuzzkin,Goobe,Homebody ×three poses ×front/side,18 direct views per revision/18 new MCP matches. Saved ages33/12/15 and fatness50 preserved,no seed override. All18 PNGs change;Fuzzkin/Goobe geometry changes12 views,Homebody geometry unchanged. Fuzzkin prepares3 textured paints per view;available Homebody cache hasno configured paint textures and doesnot confirm notice muzzle claim. Frisky/Chip absent.36 old/new+18 MCP PNGs private;two pairs reviewed. No original files/source changed.

Resume from UPDATE-001/002/003 and RENDERER_CHANGES.md. Outstanding:64 missing-input controls;generic replay excludes nested LINE-016/baseline-only units;remaining static fixtures and separate painted-group/paint-angle motion attribution;missing sample pets;independent original-game evidence. Use updated source hashes and preserve historical evidence rather than altering old verifiers. Latest request was this renderer upgrade/review,not an ongoing timed continuation.

## Final upgrade recovery and resume

[UPDATE-004](experiments/update-004.md) recovers the remaining64 top-level controls byte-identically;all64 relationship checks/400 RGBA cells pass.42 copies built,38 paths replayed;ADD/HEAD/MOVE numerical prepare assertions pass.268 omission outcomes match,as do12 focused tongue sheets. Catz changed-in-either-view union is54,not53:old JSON already implied54;this is a documentation arithmetic correction. All initially missing controls are now covered across UPDATE-002/004.

[Current upgrade index](docs/renderer-upgrade-2026-11-10.md):659 selected historical comparison/contact-sheet controls across37 manifests preserve their relationships. Pixel/numerical corrections remain in UPDATE-002;do not promote this to full old-state or native-game equivalence. Nested LINE-016,other baseline-only/synthetic/history units,broader static replays,paint-angle/saved-group attribution and missing Frisky/Chip remain scoped out. Server PID8300 on8765 uses6c1d883;all62 installed sources match;pre-existing renderer .gitignore change untouched. Original historical JSON/assets preserved;istall-node untouched.

## Ten-minute continuation: nested texture replay

[UPDATE-005](experiments/update-005.md) closes the nested LINE-016 replay exclusion:32 local stdio MCP comparisons/64 RGBA cells preserve historical relationships and exactly match current Petz4 LINE-013 PNGs. All60 numerical connector records match;20 private inputs,engines,dependencies and62 installed sources verified. Both new scripts pass;historical manifests/copies and renderer/originals unchanged. Selected historical comparison/contact-sheet total is691 (659 top-level+32 nested). Earlier nested-scope exclusions above are historical. Other baseline-only/synthetic/history units,broader static replay,paint/group attribution and native evidence remain open. Latest authorization is this ten-minute continuation.

## Complete static matrix after upgrade

[UPDATE-006](experiments/update-006.md) covers all12 TEXTURE-001 fixtures,96 sequence draws/144 resets/12 fresh MCP baselines,252 saved PNGs and240 draw-state links. Eleven fixtures stay stable through eight frames;Scottie sitting/front gives128 pixels frame3,141 frame8. At both targets,host-only/combined texture match full;geometry-only/paint-only match fresh in every fixture. Both scripts pass,originals/sources untouched. Broader static exclusion above is now closed for this12-fixture matrix only;motion paint-angle/group attribution and native validation remain open.

## Motion component continuation

[UPDATE-007](experiments/update-007.md) separates paint-only and combined-texture state in48 TEXTURE-004 histories. All192 transitions/240 prior cells match UPDATE-002;336 final PNG/state outputs verify. Host-only equals combined in48;paint-only equals fresh in48;combined differs from full in33. All diagnostic connector rasters match fresh. Links12 existing MCP baselines,no new MCP calls. Saved-pet/group attribution and broader/native evidence remain open;do not generalize this authored-connector matrix to arbitrary textured markings.

Motion scope audit:all48 pre-target paint states contain16 zero pairs;UPDATE-007 does not exercise accumulated nonzero paint angles. The manifest/verifier record this explicitly. Next useful paint-state work should use an eligible textured saved pet such as Fuzzkin.

## Ten-minute continuation final audit

[Session index](docs/session-2026-11-10-upgrade-continuation.md) links UPDATE-005/006/007 and the aggregate verifier. All unit checks pass;620 PNGs,18 original hash links,62-source agreement verified. Old HTTP PID8300 was stale;managed process11252/session98207 now serves8765 and discovery/capabilities pass. Recheck on resume. Research used fresh stdio processes. Next:nonzero paint-angle saved-pet controls,saved-group retint or independent native evidence. No renderer/original edits;istall-node untouched. Duration authorization ends with this ten-minute continuation.

Final audit records seven tool hashes and checks actual checkout HEAD against all new manifests;see the session index. Required Git identities/no-coauthor rules verified.

A final actual HTTP render (Scottie sitting/front,fixed controls) matches UPDATE-006 exactly,extending capabilities-only health. One additional health render call is separate from the44 research render calls.

## Second ten-minute continuation: saved paint motion

[PAINT-001](experiments/paint-001.md) closes the all-zero-state limitation for sampled Fuzzkin:three nonzero paint-angle pairs before every target;paint-only changes2–63 pixels and host-only differs from combined in24/24 histories. Homebody negative control haszero effects. All192 transitions/336 final draws/12 fresh local stdio MCP baselines verify;348 PNGs and48 UPDATE-003 fresh links checked. Saved controls preserved;originals/sources untouched. Nonzero paint-state behavior is renderer evidence only. Group retint/per-paint attribution remain open. Latest authorization is another ten minutes.

## Individual paint-angle attribution

[PAINT-002](experiments/paint-002.md) isolates PAINT-001 host-versus-combined changes to angles on paint-list entries16/17/18. All other commands/geometry equal;all-three substitution restores host-only pixels in24/24. Individual visible counts4/23/16 of24;not anatomical semantics or additive attribution.144 PNGs/48 prior links verified,two private standing front/side sheets reviewed. No new MCP calls,renderer/original edits or native claims.

## Paint-state vector controls

[PAINT-003](experiments/paint-003.md):Fuzzkin has19 paint entries;18/20-entry states reset the whole paint vector during preparation.48 mismatch controls match host-only;24 exact-zero controls do too. Active-only and inactive-slot controls each match combined in24.168 PNGs/48 prior links verify;no new MCP calls or renderer/original edits. Same-count paint reordering is not tested;retain state with its exact appearance/index ordering.

## Saved-paint continuation final audit

[Session index](docs/session-2026-11-10-saved-paints.md) consolidates PAINT-001/002/003 and their complete verifiers. Aggregate tools/check_paint_session.py passes:660 research PNGs,two reviewed sheets,20 original hash links,62-source agreement,seven tool hashes. New [Paint Ballz reference](format-reference/paint-ball.md) indexed for agents. HTTP discovery/capabilities healthy;research uses stdio. No renderer/original edits. Next:saved-group retint,other textured pets/versions or independent native evidence. Nonzero paint-angle gap now sampled with Fuzzkin;all-zero UPDATE-007 scope remains intact. Latest authorization is this ten-minute continuation only.

Final decoded RGBA audit checks960 differences:only Fuzzkin sitting/side yaw-arc geometry146→144 and order116→114 differ from indexed-byte counts. Paint-angle results/counts unchanged. Aggregate records exact corrections;original PAINT-001 manifest preserved.

Final aggregate additionally rehashes all660 PNG files and48 private state files against manifest digests;all pass. Working tree retains only unrelated untracked istall-node.

## Paint group preparation continuation

[PAINT-004](experiments/paint-004.md) narrows the saved-group question:216 synthetic prepared commands,180 group-only equivalences,180 unsupported-field diagnostics and216 color positive controls pass. Manifest includes all62 installed/checkout source hashes,package version and controls. Reproduce with tools/paint_group_controls.py --verify; no private assets,MCP calls,pixels or renderer/original edits. This bypasses parser/saved-pet assembly;end-to-end saved-group overrides remain open. Next:trace saved-pet group data into appearance assembly,other textured pets/versions or native evidence. Unrelated istall-node remains untouched.

## Saved prefix-array continuation

[PAINT-005](experiments/paint-005.md):three saved pets ×four prefix-array mutations,12 copies;72 direct edited/72 baseline draws and30 fresh stdio MCP views agree. Reader skips three count-checked array payloads;exact original/cache/tail boundaries retained. Forty-eight PAINT-001 fresh PNG links pass. Copies are renderer probes with unvalidated PetzInfo checksums,not game-ready files. tools/saved_colour_arrays.py --verify reconstructs/reloads all fixtures;private evidence scratch/research/paint-005. Cached group/color controls follow separately. Original files/renderer unchanged;ten-minute continuation ongoing.

## Cached group/color controls

[PAINT-006](experiments/paint-006.md) parses group0/group1 from both edited caches in Fuzzkin/Homebody/Goobe;all36 group comparisons preserve prepared commands/pixels. Diagnostics distinguish0 from1. Six Fuzzkin color65 controls change pixels;Homebody/Goobe commands do not change despite parsed colors. Nine copies,72 direct draws,18 MCP matches andsix reviewed sheets. First failed blanket-positive assertion archived privately in paint-006-attempt1. tools/saved_paint_groups.py --verify passes;private evidence scratch/research/paint-006. Explicit Fuzzkin age controls follow. Originals/renderer unchanged;ten-minute continuation ongoing.

## Paint groups across ages

[PAINT-007](experiments/paint-007.md):Fuzzkin ages0/50/100 ×three poses ×front/side;36 group0/group1 equalities,72 direct draws and16 fresh MCP matches. Both caches contribute below100;adult only at100. Three textured paints prepare in every fixture;17/18 color65 controls change pixels,age50 lying/front does not. tools/paint_group_ages.py --verify passes;copies reused from PAINT-006. No broader/native claim. Ten-minute continuation entering final integrity audit.

## Ten-minute paint-group continuation audit

[Session index](docs/session-2026-11-10-paint-groups.md) consolidates PAINT-005/006/007. All three full copy/load/render replays andtools/check_paint_group_session.py pass:298 research PNGs,21 private copies,21 original hash links,64 MCP PNG/metadata records,144 decoded RGBA counts,18 sheet reconstructions/six reviewed sheets,18 cross-unit baseline links and62-source agreement. Four tool hashes andunit replay logs recorded privately in scratch/research/paint-group-session-verification.json. HTTP was absent after server recovery;restarted PID12934/session41600 on8765. Discovery/capabilities andactual Fuzzkin front render match PAINT-005;health render excluded from research totals. No renderer/original edits;pre-existing renderer .gitignore andunrelated istall-node untouched. Next:other textured pets/versions ornative saved-array/group evidence. End-to-end group behavior is now sampled in three Petz4 saves andacross ages forFuzzkin;native retint remains unvalidated. Authorization ends with this ten-minute continuation.

Final reference review adds Goobe to the Paint Ballz scope and places native-semantic uncertainty after all current group controls. Evidence and counts unchanged;documentation checks pass.

## Selective paint cache matching

[PAINT-008](experiments/paint-008.md):Fuzzkin ages0/12/33/50/99/100,three poses/front-side;five copy variants,216 direct draws,36 MCP matches,18 PAINT-007 links. Young color has no effect;adult color changes34/36 views. Matched size changes22/36;young reorder changes24/36;one young row dropped makes all three host rows use adult,exactly matching baseline. Code and independent arithmetic support matching by host ordinal. Replay tools/saved_paint_age_matching.py --verify;private evidence scratch/research/paint-008. Originals/renderer unchanged,no native claim. Ten-minute continuation ongoing.

## Same-length paint state reordering

[PAINT-009](experiments/paint-009.md):24 Fuzzkin histories/120 direct draws. Same-host real angles equal,so remap changes nothing. Distinct diagnostic angle pairs isolate stale index binding;entries16/18 misattach in24/24 and pixels differ23/24 while geometry/ordering/non-angle commands stay fixed. Reorder alone also changes23 actual views. All24 PAINT-001 state and PNG links verify. tools/paint_state_reordering.py --verify passes;no new MCP,original/renderer edits or native claims. Ten-minute continuation ongoing.

## Exact paint direction midpoint

[PAINT-010](experiments/paint-010.md):four same-length axis-direction copies,ages55/56/57/100,32 direct/8 MCP views. Age56 exact opposite directions produce the internal zero-vector sentinel;surface commands absent,non-surface centered in both views. All16 opposed/matched RGBA pairs equal,so difference is command-level only. tools/paint_direction_midpoint.py --verify passes;private evidence scratch/research/paint-010. Originals/renderer unchanged,no native claim. Ten-minute continuation entering audit.

## Ten-minute paint matching continuation audit

[Session index](docs/session-2026-11-10-paint-matching.md) consolidates PAINT-008/009/010. Full unit replays and tools/check_paint_matching_session.py pass:368 direct draws,44 MCP records,412 PNGs,nine copies,21 original hash links,304 decoded RGBA comparisons,42 prior PNG and24 state links,62-source agreement. Seven sheets reviewed;four tool hashes and unit logs recorded in scratch/research/paint-matching-session-verification.json. HTTP discovery/capabilities and actual Fuzzkin baseline pass;no restart needed. Original files/renderer unchanged;unrelated istall-node untouched. Next: additional hosts/textured pets, controlled breed-version comparisons or native evidence. Midpoint command change has no sampled pixel signal. Authorization ends with this ten-minute continuation.

## Renderer source review

Private `scratch/renderer-source-review.md` lists prioritized discrepancies, controls, source paths, and questions for Renderer MCP. Start with fixed-pose texture drift, iris omission, and relative-size morph activation.

## Copied workspace recovery (2026-11-11)

[RESTORE-003](experiments/restore-003.md) records 21 matching original hashes, six passing cross-version stdio pairs and HTTP discovery/capabilities/render success. Use scratch/petz-local-x86-venv/bin/python on this x86_64 host; copied old environment is ARM. Endpoint127.0.0.1:8765/mcp, managed session6836. Same renderer revision6c1d883,62 installed sources match. Game originals untouched; full installation completeness is outside available manifests. Client metadata refresh/hosted app reload is separate. Reproduce originals with python3 tools/check_game_restore.py.

- MCP follow-up: local client reconnected and six-tool discovery/render reverified; no user action needed for local research. Chat-host registry reload was attempted but unconfirmed; see [RESTORE-003](experiments/restore-003.md).

## Fifteen-minute relative morph continuation

[MORPH-006](experiments/morph-006.md) replays the exact relative-size activation case on6c1d883 across Petz3/4/5 Scottie/Siamese:144 numerical records,30 private copies,36 local stdio MCP pairs/72 RGBA cells. All six geometry fixtures match historical Petz4;Petz3/5 PNGs match current Petz4. Full verifier passes;62-source/engine/original hashes checked. Use scratch/petz-local-x86-venv/bin/python tools/revalidate_relative_morph.py --verify. Native intent remains open;no renderer/original edits. Reference-boundary study follows during this fifteen-minute authorization.

## Relative size reference boundaries

[MORPH-007](experiments/morph-007.md):Petz4 Scottie/Siamese,1,728 numerical cases/72 direct rasters/two reviewed sheets;full replay passes. Morph size updates require a negative size-reference token,while radius inheritance requires an earlier assembled target. Self/forward/out-of-range nonnegative refs suppress grouped size updates but fall back to ordinary radius0. Earlier dormant target also yields radius0 without parking the activated probe. Negative sizes/1% activation included. Parsed synthetic rows in immutable memory copies only;no new MCP or file/source edits. Script tools/morph_reference_boundaries.py --verify. Chains/cycles and native behavior remain open. Fifteen-minute continuation ongoing.

## Size-reference chains/cycles

[MORPH-008](experiments/morph-008.md):936 Petz4 Scottie/Siamese numerical records/120 direct rasters;all six identity-remapped ABC permutations,chain/cycle graphs,five group modes,positive activation1/25/100. One-pass earlier-ID lookup changes radii with row order;fully grouped cycles remain all0. Reversed distinct-group updates preserve geometry. Full replay tools/morph_size_chains.py --verify passes;two standing sheets reviewed. No new MCP/game-file/source writes;native behavior open. Fifteen-minute continuation entering session audit.

## Fifteen-minute relative morph session audit

[Session evidence](docs/session-2026-11-11-relative-morphs.md) consolidates MORPH-006/007/008. Three full replays and tools/check_relative_morph_session.py pass:2,808 numerical records,228 research PNGs,36 local MCP pairs,192 direct rasters,30 private copies,84 decoded RGBA pair checks,four reviewed sheets,18 engine/breed hash links and12 cross-unit source links. Separate restoration check confirms all21 recorded originals;62 installed sources match checkout. Four tool hashes,three replay logs,manifest/image/copy hashes recorded privately. HTTP restarted PID15068/session90208;actual Scottie render equals fresh direct baseline. No renderer/original edits;pre-existing renderer .gitignore andunrelated istall-node untouched. Next:independent native evidence for GAP-005,omitted size-reference targets,other breeds or non-default scale/fatness. This fifteen-minute authorization ends with the session.

## Puppy/kitten continuation: fresh breeds

[YOUNG-001](experiments/young-001.md):306 local stdio MCP renders and132 aligned relationships pass across Petz3/4/5 Scottie/Siamese on4c4d3df. Age endpoints, aliases, defaults, three poses and front/side views sampled;two Petz4 sheets reviewed. Full replay is underway. No native-game claim or original/renderer edits. Fifteen-minute continuation remains active.

## Saved young-cache continuation

[YOUNG-002](experiments/young-002.md):three Petz4 saves,12 private fixtures (nine cache-omission edits),216 direct renders,84 prepared-command/PNG equalities and36 exact local MCP matches. Present caches stay authoritative;missing requested caches fall back independently at saved seed. Copies are not game-ready. Full replay underway;fifteen-minute continuation remains active.

## Young-resource edits and integer ages

[YOUNG-003](experiments/young-003.md):606 full-loader age records pass against independent scale/shape/ball arithmetic across Petz3/4/5. Six private Petz4 young-resource copies,84 direct outputs,28 original controls and24 exact MCP matches isolate young size/color edits;two edit sheets reviewed. Focused [reference](format-reference/young-appearance.md) and Little one coverage updated. Full replay underway;fifteen-minute continuation entering final audit.

## Young resource routing continuation

[YOUNG-004](experiments/young-004.md) tests14 Petz4 Scottie/Siamese copies:90 direct/MCP cases,54 successful MCP PNG matches,36 expected failures and108 direct front/side PNGs. Explicit young_name is case-sensitive;Little one normalizes stems,uses first row and distinguishes exact X from lowercase x. Forced adult skips young dependencies;branch overrides change effective routing and explicit young_name rescues broken branches. Full replay passes; see the final session audit below. First harness MCP-field mismatch archived privately;renderer/originals unchanged. Fifteen-minute authorization remains active.

## Mixed-cache endpoint attribution

[YOUNG-005](experiments/young-005.md) exhausts differing-list subsets for Fuzzkin,four cache modes,three poses/front-side:240 direct PNGs,24 exact MCP baselines and16 YOUNG-002 standing links. Full replay passes. Mixed-cache differences are46–241 aligned RGBA pixels;balls+add_balls restore standing/lying-side,lines also required for sitting/lying-front. Baseline/missing-both match pixels despite paint direction differences. Field controls now running;no originals/renderer edits or native claim. Fifteen-minute continuation active.

## Endpoint field attribution

[YOUNG-006](experiments/young-006.md):420 outputs,32 factor combinations+three controls in12 mixed-cache pose/views. Ball14 outline+added-list tail always required;ball38 outline required front only;line edge modes required sitting/both and lying/front. Speckle-only/paint-only controls preserve age pixels;added-prefix unnecessary in minimal sets. Full replay passes; see the final session audit below. Four aligned routing/field sheets reviewed and reproducible with tools/young_continuation_sheets.py. Originals/renderer unchanged;native claims remain open. Continuation entering integrity audit.

## Individual endpoint entry reversions

[YOUNG-007](experiments/young-007.md):144 PNGs,12 prior links,one-entry/group reversions on the sufficient substituted background. Line11 accounts for sitting-side/lying-front residuals;line14 or12 for sitting-front depending on cache mode. Added26 inert in sampled backgrounds;three-entry count group affects front only. Individual sensitivity is not exhaustive interaction attribution. Full replay and the four-unit session integrity audit pass. Original/renderer unchanged.

## Fifteen-minute young-routing final audit

[Session evidence](docs/session-2026-11-12-young-routing.md) consolidates YOUNG-004/005/006/007. All four full replays and tools/check_young_continuation.py pass:912 saved research PNGs,780 independent decoded-RGBA comparisons,40 prior links,14 new breed copies/four reused saves,four reviewed sheets,21 unchanged original hashes and62-source agreement. Initial research114 MCP requests=78 exact PNG matches+36 expected errors;replay calls and the five render calls per completed audit are separate; audit retries also made health renders. HTTP was absent,restarted PID28026/session90633;discovery/capabilities/actual young Scottie render pass. Schema branch-number wording discrepancy recorded with0/1/2/3 controls;no renderer fix. Originals/source unchanged,pre-existing renderer .gitignore andunrelated istall-node untouched. Next:native endpoint evidence,other pets/versions,added-tail interactions or isolated branch-schema correction. Earlier ongoing/replay-pending notes above are superseded. This fifteen-minute authorization ends with the session.

## MCP implementation-agent prompt

Requested scratch document: `scratch/mcp-branch-numbering-handoff.md`. Includes exact source cause, local fixture/controls,0/1/2/3 responses, proposed one-based schema correction with compatibility review, and focused service regressions. Links existing public evidence instead of duplicating manifests. No renderer/source changes; historical audits intentionally record pre-fix behavior.

## MCP branch fix reinstalled and restarted

[UPDATE-009](experiments/update-009.md):checkout already at49c7f62,reinstalled without dependency changes. Old PID28026 stopped;new HTTP PID28631/session86021 serves127.0.0.1:8765/mcp. Fresh discovery validates allfive one-based branch schema fields;four HTTP stock renders andfour stdio fixture probes pass. Branch0 now fails form validation,branch1 matches fresh direct rendering (historical PNG differs;not attributed by this smoke test),branch2 reaches intended missing dependency,branch3 fails range. All62 installed sources match checkout;all21 tracked originals match. Scratch handoff marked fixed/superseded;historical audit unchanged. No hosted reload claimed or renderer/original edits;pre-existing .gitignore/istall-node untouched. tools/check_mcp_branch_reload.py reproduces.

## Current endpoint attribution replay

[UPDATE-011](experiments/update-011.md) replays YOUNG-005/006/007 on49c7f62:804 direct PNGs all differ historically,24 MCP baselines agree. Missing-young lying/front balls+adds now suffice; field minimum omits lines and line11 reversion is now inert. Five endpoint equality observations/two minimal-set records change for that one fixture;other34 minima agree. Full replay and session audit progress are recorded in the forthcoming session index. Private sheet reviewed;no renderer/original edits. Fifteen-minute continuation ongoing.

The focused [young reference](format-reference/young-appearance.md) now carries the UPDATE-011 correction alongside the historical build scope. Use the current minimum for missing-young lying/front;do not erase the original4c4d3df result.

## Fresh and saved young upgrade replay

[UPDATE-010](experiments/update-010.md):306 Petz3/4/5 Scottie/Siamese MCP controls,216 Petz4 saved direct draws,36 fresh direct/MCP matches. All132 fresh and84 saved historical relationships survive;all522 PNGs change aligned RGBA. All21 originals match,62 installed sources agree. Initial replay complete;exact current-build verification running in scratch/update-010-verify.log. Evidence remains build-specific;no source/original edits.

## Current age arithmetic and dependency routing

[UPDATE-012](experiments/update-012.md):606 age records (42 loader boundaries+564 age-API calls),192 direct PNGs,90 routing cases and114 MCP requests on49c7f62. All100 historical equalities and numerical records survive;all192 historical RGBA images change.78 exact MCP matches+36 expected errors. Initial harness failure archived;successful-run scope explicitly documented. Exact replay and independent session audit are underway;no renderer/original edits.

## Young upgrade independent audit

[Session index](docs/session-2026-11-12-young-upgrade.md) consolidates UPDATE-010/011/012. tools/check_young_upgrade_session.py passes all1,518 independent historical/current RGBA checks,804 endpoint checks,204 cross-version and44 cross-unit links,21 originals and62 sources. HTTP restarted PID29894/session35819;four health renders match fresh baselines. One correction sheet reviewed. Exact UPDATE-010/012 replays are finishing;UPDATE-011 full replay already passes. No source/original edits;next native endpoint evidence,other pets or command/raster cause isolation.

## Young upgrade continuation complete

All three exact current-build replays and the independent [session audit](docs/session-2026-11-12-young-upgrade.md) pass. Final replay log digests: scratch/research/young-upgrade-session/replay-logs.json. Earlier pending statements above are superseded.1,518 research PNGs,606 numeric records,316 preserved historical equalities,one corrected endpoint fixture,21 unchanged originals and62-source agreement. HTTP session35819 on8765 passes actual render checks. No renderer/original edits. Next:native endpoint evidence,other pets/breeds or controlled command/raster cause isolation. This fifteen-minute continuation is complete.

## Exhaustive added-tail interactions

[YOUNG-008](experiments/young-008.md):1,536 direct renders,12 exact local MCP endpoint matches,12 UPDATE-011 links. Each of12 fixtures has one minimal subset;no monotonicity violations on the fixed sufficient outline/line background. Entry26 inert across768 matched pairs;count group required front only. Full replay and tools/check_young_tail.py pass,including1,536 independent RGBA checks and5,376 factor pairs. Native-scale12-row sheet reviewed. Private evidence scratch/research/young-008;all21 original hashes unchanged. No renderer/original/copy edits. Count controls and wider yaws follow during the active fifteen-minute continuation.

## Added count visibility controls

[YOUNG-009](experiments/young-009.md):240 direct outputs,two cache modes/three poses/front-side,four list prefixes andeight masks each for omission/zero-size. Full replay passes;all-disabled indexed controls equal the short list in12/12. Shared96 geometry/fills/commands equal short inall240,while topology differs. Independent720-RGBA audit andsix-row sheet review pass;private evidence scratch/research/young-009. No renderer/original/copy writes;continuation active.

## Hidden added-entry release control

[YOUNG-010](experiments/young-010.md):240 direct renders across eight yaws,two modes/three poses;6 exact local MCP matches,12 prior links. Entry26 maps to omitted ball93. All48 retained-omission reversions match;removing omission93 makes15/48 reversion outputs differ by1–15 pixels. Full replay,720 independent RGBA comparisons and16-row native sheet review pass. Initial narrower survey archived/excluded. Field split follows;no originals/renderer/copy writes;continuation active.

## Hidden added-entry field split

[YOUNG-011](experiments/young-011.md):192 direct PNGs,96 YOUNG-010 links,full replay passes. X-only reproduces both-field reversion across48 views,15 pixel changes;body-area-only preserves geometry/fills/commands andpixels. All resolved areas8. Code supports zero-area inheritance from base52;later-pass isolation remains outside scope. Final session checker adds240 independent RGBA comparisons. Originals/renderer/copies untouched;session audit underway.

## Young added-tail final audit

[Session index](docs/session-2026-11-12-young-tails.md) consolidates YOUNG-008/009/010/011. All four full replays andindependent audits pass:2,208 saved research PNGs,18 local MCP endpoint matches,3,312 aligned RGBA comparisons,5,376 factor signature pairs,132 prior PNG links,three reviewed sheets,21 unchanged originals and62-source agreement. Final checker adds16 numerical controls removing area lists/links:authored0/8 both resolveball93 frombase52 toarea8. Strengthened count checker directly compares96 omission/zero image pairs. HTTP absent,restarted PID32042/session52464 on8765;discovery/capabilities andsix actual Fuzzkin renders match endpoints. Private audit/replay hashes:scratch/research/young-tail-session/verification.json. Source/originals/private copies untouched;pre-existing renderer .gitignore andunrelated istall-node untouched. Next:other ages/fatness/pets ornative evidence. Final documentation checks pass;all four replays andthe session audit are complete. Earlier pending/ongoing notes above are superseded. This fifteen-minute continuation is complete.

Final reference pass gives the [current-build tail controls](format-reference/young-appearance.md#current-build-added-tail-controls) an explicit build/pet/age scope and session index. Evidence counts are unchanged;documentation checks pass.


## Native game capture intake

[2026-11-12 intake](docs/native-capture-intake-2026-11-12.md) records21 PNGs,three saves and2.43-second/138-frame Fuzzkin video. Private hashed manifest and12 decoded samples: scratch/research/native-001/inventory.json; reproduce with tools/inventory_native_captures.py and private PyAV dependency path documented there. Goobe tongue/top hat visible; older coat differs without causal attribution. Saved renderer age fields Fuzzkin69/Goobe51/Homebody12,not chronological-age claims;both cached texts equal prior same-name saves. Scottie=Chip user-reported;cat prefixes mapped;Boston identity unresolved. No separate Fuzzkin PNG found;paired snapshot is.pet. Uniform2× scale and exact pose correspondence unresolved. No renderer or game original edits. Next:qualitative comparisons using contemporaneous saves,then scale/pose controls.
# Capture-time saved-state continuation

[NATIVE-002](experiments/native-002.md) crosses prior/capture-time age and fatness for Fuzzkin,Goobe,Homebody on49c7f62:576 direct PNGs,288 exact common-control source pairs,36 local stdio MCP matches. Full replay and independent648-RGBA audit pass;three unscaled sheets reviewed,nine palette/texture/entry-field checks pass. Homebody age changes fuzz as well as size;initial size-only audit assertion archived/corrected. Goobe previews remain tan/gold on both saves;historical reddish coat cause unresolved. All21 prior original hashes match. Scale-grid verification follows within the active20-minute continuation. Originals/renderer untouched.

[NATIVE-003](experiments/native-003.md) resolves encoded PNG replication:21/21 unique exact cropped2× grids among609 factor2/3/4 candidates.21 lossless reduced copies private;full replay and independent scalar1,639,127-pixel/657-grid audit pass.19 synthetic controls include clipped borders,corruption,bilinear and4× ambiguity;25 intake hashes unchanged. Twelve H.264 samples have no exact2× phase;do not infer video scale or Mac DPI. Next:reduced-still qualitative comparisons and coat-color scope;20-minute continuation active.

[NATIVE-004](experiments/native-004.md) inventories two embedded Display ICC hashes across21 stills;18 use1164-byte profile,three RGB cat stills use4024-byte profile.21 source-tagged+21 sRGB reduced copies private;full replay/profile audit pass (410,690 pixels,1,583 unique-color mappings,84 palette tallies,nine identical old/new prefix arrays,25 unchanged intake files). Conversion controls use LittleCMS2.19,relative colorimetric1/flags0;target ICC captured privately. Earlier NATIVE-003 untagged reductions retain raw encoded RGB only. Corrected RGB/RGBA assumption and sheet spacing;prior outputs archived. Profile-aware sheet reviewed;historical Goobe reddish coat remains unexplained. [Focused index](docs/native-comparison-controls.md) added. Final session integrity/HTTP check follows;20-minute continuation active.

