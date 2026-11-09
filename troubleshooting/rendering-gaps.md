# Renderer evidence gaps

A successful PNG is not a certificate of original-game correctness. Retain complete diagnostics and exact engine/input hashes for reproduction.

| ID | Topic | Established observation | Missing evidence / next action |
| --- | --- | --- | --- |
| GAP-001 | Move anchoring | [MOVE-001](../experiments/move-001.md): fifth column rotates offsets; zero offsets are no-ops in tested frames | Community tutorial describes anchoring. Need native evidence or an independently traced algorithm before choosing a renderer repair. |
| GAP-002 | Diagnostic coverage | [SMOKE-001](../experiments/smoke-001.md) retains notices and warnings even for successful stock renders | Classify each diagnostic code/message by section before treating it as unsupported behavior. |
| GAP-004 | Iris omission | [OMIT-001](../experiments/omit-001.md): omitting iris IDs leaves front/side images unchanged, while EYE-001 color edits affect them | Current host-eye overlay path bypasses a separate iris visibility gate; native behavior and intended authoring practice require validation. |
| GAP-003 | Original-game fidelity | Repeated/controlled inputs produce measurable renderer results | No controlled native captures or independent geometry oracle validated by this research project yet. |

When a feature is unresolved, document the limitation beside its recipe. Use other research topics while collecting evidence; repair confirmed renderer defects with a reproducer and regression tests. Do not make a speculative change solely to match an ambiguous tutorial.
