# Handoff

Updated: 2026-11-09

## Resume

Read AGENTS.md, STATUS.md and agent-guides/start.md; use docs/coverage.md for remaining topics. User wants autonomous continuation through logical units until roughly 65% context use; exact context percentage is not exposed. Update documentation/status/handoff and commit each logical unit. Identity: bedalton <3941960+bedalton@users.noreply.github.com>; conventional titles preferably under 50 characters, hard limit 65; never co-authors.

## Environment and persistence

Only /workspace is guaranteed persistent. Python 3.12.16 environment is scratch/petz-local-venv; uv cache and managed Python are under scratch. Use uv --link-mode copy on this mount (default cached-wheel installation failed with permission errors). Setup commands: experiments/smoke-001.md and petz-renderer-mcp/docs/local-mcp.md.

Renderer is a separate ignored checkout at 9d72d7afd5f7460ef18133c6179caaf8055082d9, noneditable installed package, with a pre-existing .gitignore modification. No source fixes made. No renderer AGENTS.md found at research start. Local stdio MCP works; hosted available as fallback. Saved .pet support is Petz 4 only. Use `git -c safe.directory=/workspace ...` if ownership checks require it; author/committer configuration is repository-local.

Private inputs/copies/images/provenance live under ignored scratch/research/<experiment-id-lowercase>. games/ and renderer checkout are also ignored. Older experiment scripts overwrite output folders: archive evidence before changing/rerunning them. OMIT-001 instead refuses a fresh run over an existing checkpoint and supports --resume with source/sweep/PNG hash checks. Its resume assumes unchanged renderer/runtime/shared engines; check these before continuing across environment changes. Checkpoints are replaced atomically.

## Completed research

README.md links twelve experiment writeups and manifests. All behavior findings remain renderer/asset/code evidence, not native-game validation.

- SMOKE-001: Scottie/Siamese inspection/renders across Petz 3/4/5.
- ANATOMY-001: 67 candidate labels per species from Dalmatian/Siamese; cross-version label/key agreement, not complete visual semantics.
- BALL-001, HEAD-001/002: head anchors Dogz 52/Catz 24; isolated changes differ from coherent feature edits. Head Enlargement uses A+B for base diameters, A-B for spacing with an A!=100 gate confirmed in three poses.
- INHERIT-001: absent/empty/partial/full Key Balls confirms whole-section replacement in sampled Petz 4 breeds.
- MOVE-001: local rotated offsets, self-reference default, zero-vector no-op, cumulative rows and downstream projections. Community anchoring claim remains GAP-001.
- EYE-001: eight reviewed MCP comparisons plus 30 numerical pose loads separate pupil fill, iris outline and host fill. Right iris appears viewer-left in tested front view. Recipe: visual-editing/eye-colors.md.
- ADD-001: 42 numerical loads / 12 comparisons; ordinary head-attached marker does not automatically enlarge, optional size-reference radius follows head, omission hides without deleting. Parent/marker pixel deltas can differ through scaling/rotation. See add-ball reference/attached-details guide.
- OMIT-001: all 67 base IDs per species at front/side, 20 sheets / 268 omission observations. 57 Dogz and 53 Catz IDs change pixels in at least one view. Six sheets reviewed; other sheets checked automatically. Iris omissions are no-ops through current overlay path (GAP-004), not evidence of absent irises. Connected endpoints lose lines. Dogz utility labels 65/66 conflict among stock comments. Process exited 143 after 15 sheets; resume finished five, then added numerical line counts without rerendering sheets.

- VIS-001: three-pose numerical audit of all unchanged OMIT-001 IDs. Dogz 63/64 and Catz 57–62 have zero radius; Catz 55/56 remain positive (4 standing, 1 sitting/lying), with occlusion only a hypothesis. No new renders. See [writeup](experiments/vis-001.md), manifest and tools/visibility_geometry.py.

- VIS-002: local MCP, 12 sheets / 24 target observations for Catz 55/56 across three poses and four yaws. All unchanged; head controls all change. Three sheets visually reviewed. See [writeup](experiments/vis-002.md). Uses unchanged OMIT-001 private copy; atomic resume checks in tools/visibility_views.py.

## Next research

Test iris/host omission combinations. VIS-002 broadened Catz 55/56 sampling without exposing a contribution; seek an open-mouth frame or isolation probe before calling this occlusion. Test more frames/angles and another breed per species before promoting visual atlas identities. Consider iris/host omission combinations and independent native evidence. Expand connected added details, body areas/morph groups, remaining shape/color/texture sections and edited cross-version checks. Do not repair ambiguous renderer behavior without a reproducer and evidence of intended native semantics.

## Checks and safeguards

Run `scratch/petz-local-venv/bin/python tools/check_docs.py` for Markdown targets, JSON/hash syntax and private-file exclusion. Rebuild docs/coverage.md with tools/coverage_index.py. tools/anatomy_inventory.py regenerates label indices and includes OMIT-001 sensitivity if its manifest exists. Update generators when changing generated docs.

tools/research_common.py checks unchanged resource metadata, unrelated payloads and bytes outside a fixed adult LNZ span. It serializes seed-resolved sections, removing comments/variation alternatives: this is not a general variation-preserving resource editor. Original game files remain read-only. No complete native-validated anatomy atlas or concept-to-breed workflow exists yet; website deferred.
