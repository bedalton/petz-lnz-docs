# Texture authoring and motion continuation

User requested a fifteen-minute continuation on2026-11-10; work began17:39:50 UTC. This session follows the connector sampling continuation and does not imply ongoing authorization. All findings are renderer/asset/code evidence, with no native-game validation. No renderer sources or original game files changed.

| Unit | Result | Evidence |
| --- | --- | --- |
| LINE-021 | Dedicated appended marker slots load five authored dimensions. Three small dimensions suppress a connector while explicit-fill controls draw. | [Writeup](../experiments/line-021.md), [manifest](../experiments/line-021.json), [reproducer](../tools/line_texture_dimensions.py), [verifier](../tools/check_texture_dimensions.py) |
| TEXTURE-003 | Mode decoding/defaults, all-byte remaps and composed controls. -1=0 and2=10=150;0/1/2 differ. | [Writeup](../experiments/texture-003.md), [manifest](../experiments/texture-003.json), [reproducer](../tools/texture_mode_probe.py), [verifier](../tools/check_texture_modes.py) |
| TEXTURE-004 | Return-to-pose histories leave34/48 scenes different despite equal final geometry. All diagnostic connector rasters match fresh. | [Writeup](../experiments/texture-004.md), [manifest](../experiments/texture-004.json), [reproducer](../tools/texture_motion_history.py), [verifier](../tools/check_texture_motion_history.py) |

New focused [Texture List reference](../format-reference/texture-list.md) is indexed from the agent entry point. Connector texture/state references and coverage ledger link the new scope. Twelve sheets reviewed across the three units; exact sheet identities are recorded in their writeups.

## Verification

All three unit verifiers pass. Private summaries: scratch/research/{line-021,texture-003,texture-004}-verification.json. The [session verifier](../tools/check_texture_authoring_session.py) checks report hashes/public-private agreement,dependencies,twenty cross-unit pixel links and all62 installed Python sources against checkout. Output: scratch/research/texture-authoring-session-verification.json. It uses unit verifier records tied to the current report hashes; it does not replace their full replays.

Totals:78 newly edited private copies;234 numerical authoring loads;12 history asset fixtures;60+96 isolated authoring rasters;48 histories with240 final diagnostic rasters;18 parser controls and40 all-byte remaps;124 local MCP comparison pairs and12 exact fresh-baseline checks.184 saved PNGs contain500 RGBA cells (80 dimension cells +168 mode cells +240 history cells +12 baseline images). History replay checks192 transition states,48 before-final states and240 final states, with persisted indexed bytes and crop verification.

All48 history fresh cells additionally match their twelve MCP-checked baseline images, whose PNG hashes match saved MCP metadata. Twenty exact cross-unit links verify mode1 matches the earlier256×256 scenes, and standing history baselines match128×128 comparison cells. This goes beyond input/hash reuse to confirm actual sampled pixels. All original sources and private copies retain their recorded hashes, and edited leaves preserve every other resource and outer file boundary.

Whole-source tree digest: `72acdc38ea4c7de54053aad0aa07d03608ef6fbb5d4da0321b68d55075736a8a`. Full map: scratch/research/texture-authoring-source-audit.json. Checkout remains clean at9d72d7afd5f7460ef18133c6179caaf8055082d9. HTTP MCP discovery/get_capabilities pass at127.0.0.1:8765/mcp; record scratch/research/texture-authoring-session-mcp-health.json. Actual image calls used local stdio with explicit Petz4 metadata, no hosted backend.

Final mode audit asserts three isolated pixel classes in every pose/species: {-1,0,125,149}, {1}, {2,10,150}. Modes125/149 still decode differently from0; standing Catz125 has different whole remapped-art bytes while the sampled connector matches. This local equality does not establish general equivalent modes or native semantics, and has no new direct MCP pair claim.

Reproducers refuse overwrite. Two failed LINE-021 attempts remain archived under scratch/research/line-021-attempt-{1,2}; the misplaced texture field was corrected before final data. Existing unrelated untracked istall-node remains untouched. All committed work uses bedalton identity and no co-author trailers.

## Remaining limits

Composed tests remain two adult Petz4 breeds; only standing front/side has new authored-mode/dimension MCP pixels. Three numerical poses and direct histories do not broaden native fidelity. Motion histories reset line RNG each draw and keep the named animation frame fixed; they are not game animation simulations. Order-only counterfactuals can change shared fuzz consumption as well as occlusion. Custom art, young resources, broader versions and independent native texture/iris evidence remain open. GAP-006 stays unresolved.
