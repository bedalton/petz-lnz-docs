# MORPH-008: size chains and cycles by row order

Date: 2026-11-11. Petz 4 Scottie/Siamese, renderer integration `6c1d88325ced89109f8e4b9d724fa8ab6037b42c`; immutable appearance copies with parsed synthetic rows. Code-supported and renderer-observed only; no native-game validation, renderer changes, game-file writes or new MCP calls.

Size-reference resolution is a single pass over added IDs. Correctly remapping references after a row permutation preserves the intended graph but does not preserve radius results. [MORPH-007](morph-007.md) established the individual boundary; this matrix checks chains and cycles.

Three diagnostic markers have authored sizes A20/B-8/C10 and fixed identity-specific offsets. The chain is A→head, B→A, C→B. The cycle is A→C, B→A, C→B. All six ABC permutations are tested, with every numeric reference remapped by identity. Five modes cover all static, all group15, static A with grouped B/C, dormant group14 A with grouped B/C, and explicitly activated group14 A with grouped B/C. Active amounts1/25/100 are tested; static controls use100%.

- In ABC order, the fully grouped chain inherits the head radius through all three markers at every positive tested amount. CBA leaves only A with head radius; B and C have unresolved forward references and stay radius0.
- With all three markers grouped and activated, every cycle has all radii0 in all six permutations. There is no nonzero prior radius or authored evaluated-size contribution to propagate.
- With A dormant, all chain/cycle radii stay0; B/C remain unparked and visible. Activating A restores the head-rooted chain only where references resolve in order; it does not add a radius source to the cycle.
- Static authored contributions make cycle results depend on order too. They do not trigger a solver that revisits earlier entries.
- Reversing distinct-group update order preserves complete final posed geometry in every case. This checks fresh explicit evaluation, not retained rendering order or runtime animation.

There are936 numerical records(two species ×three poses ×two graphs ×six permutations ×13 mode/amount settings), each checking size, radius, visibility and parked flags against an identity-keyed recurrence. The120 direct rasters cover ABC/CBA at100% in every mode/graph/species/pose, with common XY bounds, fresh state, raster/line RNG seeds1 and step0. Seed0, age100, fatness50, yaw0.

Independent decoded RGBA comparisons find ABC/CBA differences in all six species/pose fixtures for static chains/cycles, static-root chains/cycles, fully grouped chains and activated-root chains. Fully grouped cycles, dormant-root chains/cycles and activated-root cycles match in all six. Equal pixels do not establish equal marker positions or native semantics.

Two standing sheets reviewed at native resolution show three large markers for forward-propagating chains, one large marker for reversed grouped chains, and no visible cycle markers in the all-group15 case. Static cycle probes retain the small order-dependent dots. No anatomy meaning is assigned to these synthetic probes.

Reproduce: `scratch/petz-local-x86-venv/bin/python tools/morph_size_chains.py`; refuses existing output. `--verify` replays all936 numerical records and120 draws, requiring byte-identical PNGs and report contents. Both passed. [Manifest](morph-008.json), [script](../tools/morph_size_chains.py); private `scratch/research/morph-008` and `scratch/morph-008-{run,verify}.log`. The [session audit script](../tools/check_relative_morph_session.py) independently compares60 ABC/CBA RGBA pairs and records sheet cell layouts/hashes. All62 installed/checkout sources, actual revision, dependencies and original breed digests are checked; shared-engine provenance links to [MORPH-006](morph-006.md). Other breeds/versions, omitted reference targets, non-default fatness/scales and native behavior remain open.
