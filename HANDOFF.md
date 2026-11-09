# Handoff

Updated: 2026-11-09

## Resume

Read AGENTS.md, STATUS.md and agent-guides/start.md; use docs/coverage.md for remaining topics. User wants autonomous continuation through logical units until roughly 65% context use; exact context percentage is not exposed. Update documentation/status/handoff and commit each logical unit. Identity: bedalton <3941960+bedalton@users.noreply.github.com>; conventional titles preferably under 50 characters, hard limit 65; never co-authors.

## Current container recovery

[RESTORE-002](experiments/restore-002.md): user restored games; moved nested games/games/petz3–5 to games/petz3–5. Local Petz 4 HTTP server is running at http://127.0.0.1:8765/mcp in this container session; real HTTP discovery/capability call passed. Six stdio inspect/render pairs pass and match prior SMOKE-001 records exactly. New private evidence: scratch/research/restore-002. Previous private experiments remain missing; do not assume their copies/checkpoints exist. Dependencies freshly resolved; manifest records engine and dependency hashes. No source changes.

## Environment and persistence

Only /workspace is guaranteed persistent. Python 3.12.16 environment is scratch/petz-local-venv; uv cache and managed Python are under scratch. Use uv --link-mode copy on this mount (default cached-wheel installation failed with permission errors). Setup commands: experiments/smoke-001.md and petz-renderer-mcp/docs/local-mcp.md.

Renderer is a separate ignored checkout at 9d72d7afd5f7460ef18133c6179caaf8055082d9, noneditable installed package, with a pre-existing .gitignore modification. No source fixes made. No renderer AGENTS.md found at research start. Local stdio MCP works; hosted available as fallback. Saved .pet support is Petz 4 only. Use `git -c safe.directory=/workspace ...` if ownership checks require it; author/committer configuration is repository-local.

Private inputs/copies/images/provenance live under ignored scratch/research/<experiment-id-lowercase>. games/ and renderer checkout are also ignored. Older experiment scripts overwrite output folders: archive evidence before changing/rerunning them. OMIT-001 instead refuses a fresh run over an existing checkpoint and supports --resume with source/sweep/PNG hash checks. Its resume assumes unchanged renderer/runtime/shared engines; check these before continuing across environment changes. Checkpoints are replaced atomically.

## Completed research

README.md links thirteen experiment writeups and manifests. All behavior findings remain renderer/asset/code evidence, not native-game validation.

- SMOKE-001: Scottie/Siamese inspection/renders across Petz 3/4/5.
- ANATOMY-001: 67 candidate labels per species from Dalmatian/Siamese; cross-version label/key agreement, not complete visual semantics.
- BALL-001, HEAD-001/002: head anchors Dogz 52/Catz 24; isolated changes differ from coherent feature edits. Head Enlargement uses A+B for base diameters, A-B for spacing with an A!=100 gate confirmed in three poses.
- INHERIT-001: absent/empty/partial/full Key Balls confirms whole-section replacement in sampled Petz 4 breeds.
- MOVE-001: local rotated offsets, self-reference default, zero-vector no-op, cumulative rows and downstream projections. Community anchoring claim remains GAP-001.
- EYE-001: eight reviewed MCP comparisons plus 30 numerical pose loads separate pupil fill, iris outline and host fill. Right iris appears viewer-left in tested front view. Recipe: visual-editing/eye-colors.md.
- ADD-001: 42 numerical loads / 12 comparisons; ordinary head-attached marker does not automatically enlarge, optional size-reference radius follows head, omission hides without deleting. Parent/marker pixel deltas can differ through scaling/rotation. See add-ball reference/attached-details guide.
- OMIT-001: all 67 base IDs per species at front/side, 20 sheets / 268 omission observations. 57 Dogz and 53 Catz IDs change pixels in at least one view. Six sheets reviewed; other sheets checked automatically. Iris omissions are no-ops through current overlay path (GAP-004), not evidence of absent irises. Connected endpoints lose lines. Dogz utility labels 65/66 conflict among stock comments. Process exited 143 after 15 sheets; resume finished five, then added numerical line counts without rerendering sheets.

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

## Next research

Iris/host combinations are now sampled by EYE-002; seek native evidence before resolving GAP-004. Do not keep investigating Catz 55/56 no-ops in supplied poses: the user explained the hidden tongue and missing tongue-out animation; see VIS-002 for attribution and limits. Test more frames/angles and another breed per species before promoting visual atlas identities. Consider left-pair/other-breed checks and independent native evidence. Expand connected added details, body areas/morph groups, remaining shape/color/texture sections and edited cross-version checks. Do not repair ambiguous renderer behavior without a reproducer and evidence of intended native semantics.

## Checks and safeguards

Run `scratch/petz-local-venv/bin/python tools/check_docs.py` for Markdown targets, JSON/hash syntax and private-file exclusion. Rebuild docs/coverage.md with tools/coverage_index.py. tools/anatomy_inventory.py regenerates label indices and includes OMIT-001 sensitivity if its manifest exists. Update generators when changing generated docs.

tools/research_common.py checks unchanged resource metadata, unrelated payloads and bytes outside a fixed adult LNZ span. It serializes seed-resolved sections, removing comments/variation alternatives: this is not a general variation-preserving resource editor. Original game files remain read-only. No complete native-validated anatomy atlas or concept-to-breed workflow exists yet; website deferred.
