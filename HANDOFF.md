# Handoff

Updated: 2026-11-08

## Resume

Read AGENTS.md, STATUS.md and docs/research-plan.md. The user approved Petz 4 first, community sources plus experiments, practical design guidance growing into an exhaustive reference, private raw evidence with curated public material, and renderer repairs when needed.

## Environment findings

/workspace is the only guaranteed persistent location. It contains games/petz3, games/petz4, games/petz5, an existing petz-renderer-mcp checkout and scratch/petz-engines. These are ignored, not committed. uv is available; Python 3.12 and a working local environment have not been verified.

The connected hosted Petz Renderer MCP reports breed support for Petz 3/4/5, saved .pet support only for Petz 4, and unverified original-game fidelity. Local instructions are in petz-renderer-mcp/docs/local-mcp.md; read that checkout's AGENTS.md before modifying it. The local renderer has not been started or tested during planning.

## Next concrete actions

Inspect renderer Git state and instructions; record revision/integration strategy. Build a pinned Python 3.12 environment under scratch. Run setup checks and scripted stdio MCP smoke tests for a dog and cat in each version. Persist results and commands, update status/handoff, and commit the logical unit. Then prove extraction/edit/repacking before anatomy research.

No LNZ behavior claims, anatomy maps or experimental results have been produced yet. Raw renders and extracted proprietary inputs must remain private under ignored persistent storage.

## Research update: local MCP operational

The preceding environment notes describe the planning baseline. Python 3.12.16 and installed dependencies now live in scratch/petz-local-venv. Run scratch/petz-local-venv/bin/python tools/local_smoke.py. Use uv --link-mode copy on this mount; default installation failed with cached-wheel permission errors, then copy-mode reinstall succeeded.

Six local stdio inspection/render pairs passed; see experiments/smoke-001.md and its JSON manifest. Private PNGs and complete provenance/diagnostics are in scratch/research/smoke-001. No visual review, repeated-run check or edited breed experiment has occurred yet. The renderer checkout revision is 9d72d7afd5f7460ef18133c6179caaf8055082d9 with a pre-existing .gitignore modification; no source edits made. Its AGENTS.md was absent at research start despite earlier planning notes mentioning it.

Next: inspect LNZ resources with petz_renderer.formats.pe.ResourceFile (resource leaves expose offset and size); inventory master/breed sections. Establish a safe copy-only edit/repack procedure and verify unrelated resources before experimental edits. Initial whole-section merge finding is documented in format-reference/inheritance.md as code-supported only.

## 2026-11-09: first controlled edits complete

Read experiments/ball-001.md. tools/ball_probe.py creates seed-resolved, fixed-resource-span copies and asserts all unrelated bytes/resources unchanged. Ten final Petz 4 renders passed; original/control PNGs matched each other and prior smoke results. Independent size/color/move variants changed both species' PNGs. Native images reviewed. Head anchors from master Key Balls: Dogz 52, Catz 24. Moving the base circle alone separates it from other facial components.

Private evidence is scratch/research/ball-001; tracked hash manifest is experiments/ball-001.json. First trial mistakenly used existing Scottie color 35 and correctly produced no change; corrected final trial uses 125. No renderer source changes. Procedure resolves/removes variation alternatives in copies, so it is not a general variation-preserving resource editor. Reruns overwrite the private directory.

Next: master section and ball-label inventory, aligned multi-view comparison and numerical geometry checks, inheritance experiments and Head Enlargement/group controls. Community-source research remains outstanding. Commit this logical unit with no co-authors.
