# Ten-minute upgrade continuation

Date: 2026-11-10. Requested duration: ten minutes. Renderer integration6c1d88325ced89109f8e4b9d724fa8ab6037b42c, package display0.1.0. No source repairs or original asset edits. All observations remain renderer evidence, not native-game validation.

| Unit | Result | Validation |
| --- | --- | --- |
| [UPDATE-005](../experiments/update-005.md) | Nested Petz3/5 connector relationships confirmed; current Petz4 PNGs match exactly |32 MCP pairs/64 RGBA cells,60 connector loads |
| [UPDATE-006](../experiments/update-006.md) | Eleven static fixtures stable;Scottie sitting/front retains128/141-pixel drift |96 sequence draws,144 resets,12 new MCP fresh baselines |
| [UPDATE-007](../experiments/update-007.md) | Host=combined texture and paint-only=fresh in48 motion histories;pre-target paint angles are all zero |192 transitions,336 final draws,240 prior pixel links,12 existing MCP baseline links |

All three unit verifiers pass. `scratch/petz-local-venv/bin/python tools/check_upgrade_continuation.py` aggregates their manifest/verification hashes, counts620 saved PNGs and checks all62 installed Python sources against the checkout for each unit. It also verifies18 restoration-original hash links across Petz3/4/5. The aggregate does not replace the unit pixel/numerical replays. Private summary: scratch/research/upgrade-continuation-verification.json. Historical manifests and private copies remain intact.

The final HTTP check initially found no server listening;the old PID8300 handoff record was stale. Restarted the installed module on127.0.0.1:8765 with explicit Petz4 root. Current process11252,managed exec session98207. Discovery and get_capabilities pass with six tools;private health scratch/research/continuation-2026-11-10-upgrade-health.json. The research comparisons used fresh stdio processes,so the HTTP outage did not affect them. A background nohup launch did not survive the command lifecycle;the managed session did. Recheck health on later resumes rather than trusting the PID.

Research MCP render calls total44:32 comparisons plus12 fresh baselines. An additional final HTTP render health control matches the UPDATE-006 Scottie sitting/front baseline exactly. UPDATE-007 makes no new MCP calls. Static and motion histories reset raster RNG/step per draw and retain post-draw FrameState, as documented in their manifests. Equal pixels do not establish equal internal state or game fidelity.

Next useful scope: nonzero paint-angle retention using an eligible textured saved pet (Fuzzkin),saved-group retint controls,other historical baseline/synthetic units or independent original-game evidence. All48 UPDATE-007 pre-target paint-angle vectors contain16 zero pairs,so its no-difference observation does not close general paint-angle attribution. Frisky/Chip remain unavailable. Unrelated untracked istall-node remains untouched.

Final provenance audit also checks checkout HEAD against each new manifest and records hashes of all seven new reproducers/verifiers in the aggregate summary. Git author and committer match the required identity;no co-author trailers. Renderer checkout still has only its pre-existing .gitignore change.
