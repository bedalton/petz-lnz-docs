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
