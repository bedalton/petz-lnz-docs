# Connector research session: 2026-11-09

Approximately ten-minute continuation starting 21:41 UTC. Petz 4 Scottie/Siamese; local stdio MCP and separately identified direct Python checks. Native-game behavior remains unvalidated. Renderer source unchanged.

| Unit | Numerical variant/pose checks | MCP pairs | Sheets visually reviewed |
| --- | --- | --- | --- |
| [LINE-002](../experiments/line-002.md): thickness | 36 | 24 | 6 |
| [LINE-003](../experiments/line-003.md): draw order | 36 | 20 | 4 |
| [MORPH-001](../experiments/morph-001.md): groups | 24 | 12 | 4 |
| [AREA-001](../experiments/area-001.md): connection-derived area | 42 | 8 | 2 |
| [LINE-004](../experiments/line-004.md): defaults | 36 | 16 | 2 |
| Total | 174 | 80 | 18 |

Each unit has a committed reproducer, manifest and focused writeup. Rendered pose is standing at yaw 0/90, seed 0, age 100, fatness 50. Numerical checks additionally use sitting/lying. Explicit morph updates and head rotation were numerical only; their behavior is not established by default-state MCP images.

Final evidence verification command: `scratch/petz-local-venv/bin/python tools/check_recent_evidence.py`. It verified all 62 private experimental inputs and 80 private comparison PNGs against committed manifests; both original breed files still match their recorded hashes; all 12 shared engine files across Petz 3/4/5 still match RESTORE-002. The checker reads existing evidence without rerendering or changing it. It requires this session's ignored private artifacts and fails if missing. Hash agreement establishes integrity, not native fidelity.

Documentation checks and generated coverage rebuild pass. Agent entry routes and attached-detail guide now link the new controls. Follow-up priorities: multi-neighbor body-area precedence; morph relative sizing/multiple groups; connector fuzz/edge/color semantics; other breeds/versions for connectors; native validation. The existing iris and hidden-tongue limitations remain unchanged.
