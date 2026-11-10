# Retained pixels and texture session, 2026-11-10

Three completed units in the second requested ten-minute continuation. Evidence remains code-supported/renderer-observed in Petz 4 Scottie/Siamese. Original game files preserved; no renderer source changes or native-game claims.

| Unit | Evidence | Finding |
| --- | --- | --- |
| [MORPH-005](../experiments/morph-005.md) | 60 pixel triples, 12 local MCP baseline checks | Retained sort order alone changes no pixels; full retained preparation changes ten Dogz sitting cases. |
| [TEXTURE-001](../experiments/texture-001.md) | 12 stock pose/view fixtures, eight frames each, independent state resets, 12 MCP baseline checks | Scottie sitting yaw0 changes121 pixels on frame3 without morphs; texture-only state reproduces it, geometry-only does not. |
| [TEXTURE-002](../experiments/texture-002.md) | Seven exact orientation-state replays and identity arithmetic control | Constant Q8 matrix self-product/rounding produces repeated(0,-1) angle delta. Native intended behavior still unknown. |

Five sheets visually reviewed: two explicit morph-history sheets and three static texture/reset sheets. The full retained pixel path deliberately resets line RNG/raster seed/step while retaining FrameState. These are controlled compositions, not automatic native animation or ordinary MCP still controls. Default-state baselines match local MCP byte-for-byte.

## Integrity and navigation

Run `scratch/petz-local-venv/bin/python tools/check_texture_session.py`:96 sheet PNGs,396 decoded RGBA cells,24 local MCP baselines,96 full/private orientation snapshot hashes, original/reused input hashes, installed sources/dependencies and Petz4 engine hashes all pass. Twelve additional morph baseline PNGs are also checked. The existing loopback HTTP MCP passes final live discovery/get_capabilities; private record scratch/research/texture-session-mcp-health.json. Private output: scratch/research/texture-session-verification.json. Run tools/check_docs.py for links, JSON/hash syntax and private-file exclusion.

The compact public texture manifest keeps hashes and changed angles; full orientation snapshots remain private. This avoids duplicating unchanged matrices across frames. Each completed research unit is committed separately with updated status and handoff.

Read [texture state](../format-reference/texture-state.md) for practical comparison limits. GAP-006 has a reproducer and numerical explanation; independent native evidence is still needed before deciding whether to change the renderer. Other next topics: broader breed/version texture samples, connector styling, and unresolved relative-size morph semantics (GAP-005).
