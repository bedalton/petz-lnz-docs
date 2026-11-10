# PAINT-009: same-length paint reordering

Date: 2026-11-10. Fuzzkin/Petz 4, integration `6c1d883`. [Manifest](paint-009.json), [reproducer/verifier](../tools/paint_state_reordering.py). Direct API only; private evidence: `scratch/research/paint-009`.

The three active paint entries 16/17/18 have identical angle pairs in each of the 24 persisted PAINT-001 histories. Reversing those entries changes draw order and can change pixels (23/24 views), but remapping the actual angle vector produces no further change: its values are equal. These entries share host 50. The test does not claim angle equality for arbitrary markings or hosts.

To distinguish paint identities, add three distinct angle deltas to the prior vectors, then compare two draws using the same reversed appearance. One retains index order; the other moves each angle with its corresponding paint row. Preparation accepts both vectors because their lengths match. The stale vector assigns the wrong angles to entries 16 and 18 in all 24 cases. The remapped commands recover their original per-marking angles and all other fields, adjusting only the paint-list index. With geometry, paint order and every non-angle field held equal, stale and remapped images differ in 23/24 fixtures, by 1–42 RGBA pixels when visible. The exception is lying/front after the yaw arc.

The intervention uses synthetic distinct angles to expose indexing; it is not a reproduced failure of natural saved motion. The direct API documents retaining FrameState only for unchanged appearance. For normal authoring, start fresh after changing paint order. The experimental remap isolates paint angles; it does not make arbitrary retained state compatible across appearance changes.

The 120 persisted draws include 24 exact links to PAINT-001 combined-texture PNGs. The verifier rehashes all 24 prior state files, replays the five draws per fixture, checks exact commands and PNGs, and verifies installed source, engine, dependency and original hashes. No new MCP calls, original edits, renderer changes or native-game claims.

```sh
scratch/petz-local-venv/bin/python tools/paint_state_reordering.py --verify
```
