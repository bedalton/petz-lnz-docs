# Ten-minute saved-paint continuation

Date: 2026-11-10. Requested duration: another ten minutes. Renderer integration6c1d88325ced89109f8e4b9d724fa8ab6037b42c;package display0.1.0. No source repairs or original asset edits.

| Unit | Result | Verification |
| --- | --- | --- |
| [PAINT-001](../experiments/paint-001.md) |Fuzzkin nonzero paint state affects24/24 targets;Homebody0/24 |192 persisted transitions,336 final draws,12 new MCP fresh baselines,348 PNGs |
| [PAINT-002](../experiments/paint-002.md) |Three angle fields explain all24 host/combined differences |144 final draws,48 prior pixel links |
| [PAINT-003](../experiments/paint-003.md) |18/20-entry vectors reset all19 Fuzzkin paint angles |168 final draws,48 prior pixel links,48 length-mismatch controls |

All three unit verifiers pass. `scratch/petz-local-venv/bin/python tools/check_paint_session.py` checks660 research PNGs,two privately reviewed front/side sheets,all manifest/verification hashes,20 original asset hash links and62 installed sources against the checkout per unit. It checks actual renderer HEAD and records seven tool hashes. Private summary scratch/research/paint-session-verification.json. This aggregate verifies integrity;the unit verifiers perform full state/pixel reproductions.

The12 new local stdio MCP calls preserve saved seed/age/fatness and validate fresh stills only. PAINT-002/003 make no new MCP calls. All retained-history and intervention conclusions are direct renderer evidence. PAINT-001 also checks48 earlier UPDATE-003 fresh-baseline links. Raster RNG seed1 and step0 reset per draw. The648 final direct draws are separate from192 persisted motion transitions;additional reconstructed histories in PAINT-002/003 are not counted as new persisted transition records.

Final HTTP discovery/get_capabilities succeeds on127.0.0.1:8765/mcp with six tools;private health scratch/research/paint-session-health.json. Research comparisons use fresh stdio processes. Originals,old manifests and renderer source are unchanged;renderer checkout retains only its pre-existing .gitignore modification. Required Git author/committer identity and absence of co-author trailers checked. Untracked istall-node untouched.

The new [Paint Ballz reference](../format-reference/paint-ball.md) indexes field-order caveats,updated texture support and the retained-state contract. Source-inspected statements are identified separately from tested outcomes. Nonzero group diagnostics remain unsupported in the inspected integration;resolved remap colours alone do not validate saved-group override. Do not infer native-game fidelity from repeated renderer results.

Next: end-to-end painted-group retint if suitable saved data is available,other textured pets/versions,same-count appearance/state compatibility,or independent original-game texture/iris evidence. Fuzzkin now provides nonzero paint-angle evidence;UPDATE-007's all-zero limitation stays part of its historical scope.

Final decoded-pixel audit independently checks960 RGBA difference counts across all saved final controls. Two PAINT-001 indexed counts overstate displayed changes by2:geometry-only146→144 and order-only116→114 for Fuzzkin sitting/side yaw arc. Every paint-angle count and all other counts match. Palette aliases explain why indexed-byte changes and displayed-pixel changes must be distinguished;the original manifest remains unchanged.

The aggregate also independently rehashes every one of the660 PNG files against its manifest and all48 persisted state files against their recorded hashes;unit verification checkpoints are not the only integrity guard.
