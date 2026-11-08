# Agent-first LNZ research plan

## Goal and sequence

Enable an agent to design a recognizable pet from an image or concept, while building a thorough LNZ reference for agents and people. Start with Petz 4 Dogz and Catz; expand to both species in Petz 3 and 5. Practical design guidance comes first, with exhaustive format coverage tracked throughout. A user-facing website is deferred.

## Phase 1: durable infrastructure

Maintain README.md as the navigation hub, AGENTS.md as working rules, STATUS.md as a lightweight progress index and HANDOFF.md as restart instructions. Store all durable work under /workspace. Update status and handoff and commit after every logical unit, using the required identity and commit rules.

Keep proprietary inputs, extracted stock resources, raw renders and environments in ignored persistent storage. Track an artifact manifest with hashes, provenance, generation commands and private paths. Persistent local storage is not an independent backup. Review derived illustrations before public inclusion; publish original explanations and synthetic examples by default.

Inspect the existing renderer checkout and record its revision, dependencies and integration approach before changing or vendoring it. Do not add the whole workspace to Git.

## Phase 2: establish the experiment loop

1. Install Python 3.12 and pinned renderer dependencies under scratch. Follow petz-renderer-mcp/docs/local-mcp.md.
2. Run local checks and use a scripted stdio MCP client to inspect and render one dog and one cat for each game version. Prefer local rendering; fall back to hosted MCP when necessary.
3. Inventory breeds, master LNZ, young/adult resources, textures, selectors and diagnostics.
4. Establish extraction, editing and repacking on breed copies. Verify unrelated resources remain intact and the selected resource contains the intended edit.
5. Change a single ball's size, position and color in separate experiments. Save aligned comparisons and exact patches.

Exit criterion: documented commands reproduce a controlled edit and visual comparison without modifying originals. Advertised version support is not sufficient evidence of successful local operation.

## Phase 3: investigate anatomy and format

Organize focused pages under format-reference, visual-editing, experiments, examples and agent-guides; add troubleshooting pages from observed failures. Create a topic/coverage ledger from stock resources, implementation inspection and attributed community sources, including unsupported and unknown sections.

Investigate syntax, inheritance and section replacement, resource selection, variation blocks, numbering, coordinate conventions, units and defaults. Build separate Dogz and Catz atlases: base-ball ID, anatomical role, left/right convention, relationships, annotated views and evidence. Added-ball identities remain breed-specific.

Prioritize silhouette and proportions, facial features and eyes, added/omitted balls, lines and projections, colors, textures, paint, fuzz and outlines. Then investigate age, fatness, variation and interactions. Expand toward every discovered section and field without implying that renderer coverage equals format coverage.

Start with single-variable tests, followed by interaction tests. Keep seed, age, fatness, resource selectors, pose and camera fixed unless under study. Use aligned front, rear and side views; inspect standing, sitting and lying where pose matters. A visually unchanged result does not prove that a field has no effect.

Every experiment has a stable ID and machine-readable manifest recording hypothesis, input/resource hashes, exact patch, controls, renderer/runtime versions, backend, commands, artifact locations, diagnostics, observations and limitations. Reference claims link to evidence and distinguish source-reported, code-supported, renderer-observed and game-validated results, with explicit species/version applicability. Preserve disagreements and uncertainty.

Research community sources with links and attribution. Seek independent game evidence where feasible; do not make unavailable game captures a prerequisite for all progress. Renderer repeatability is distinct from original-game fidelity.

## Phase 4: convert findings into design guides

Write task recipes connecting desired visual changes to fields, with prerequisites, minimal edits, expected effects, interactions, verification views and failure modes. Cover goals such as longer muzzles, larger paws, different ears and markings as evidence becomes available.

Document the agent workflow: interpret reference, identify anatomical targets, select base breed, plan edits, change one feature group, render/compare, refine and validate. Deliver three Petz 4 examples: proportion editing, marking design and combined concept-to-breed design. Preserve instructive failed attempts.

Evaluate a fresh-context agent using only documented entry points. Record completion, corrections, unsupported assumptions and unnecessary reading. Improve guides from these failures. Use stable document IDs, relative links and structured indexes suitable for a later website.

## Phase 5: expand and validate

Verify every base-ball mapping for both species across all three versions. Validate high-value recipes across versions; reuse procedures without assuming equivalent numbering means equivalent behavior. Record failed or unavailable combinations as gaps. Expand interaction tests where differences warrant them.

Repair renderer defects that block important topics. Each fix needs a reproducer and appropriate regression tests; record the renderer revision, rerun affected experiments and mark superseded evidence. Keep renderer regressions separate from game-correctness claims.

Check links, manifests, evidence references and coverage indexes automatically. Verify example patches apply to declared baselines and reproduce documented effects.

## Milestones and completion

First milestone: persistent project setup, working local experiment loop, initial Dogz/Catz anatomy maps and one reproducible design recipe.

Next milestones: three worked Petz 4 examples and agent evaluation; six-combination anatomy coverage; expanded format and interaction reference.

Long-term completion requires every discovered section and field to be documented or explicitly unresolved, recorded coverage for all six species/version combinations, and successful representative agent design tasks. Saved-pet behavior is secondary and included where it affects appearance or validation.
