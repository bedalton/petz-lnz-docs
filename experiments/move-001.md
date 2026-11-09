# MOVE-001: reference rotation and zero-offset entries

Date: 2026-11-09. Petz 4 Scottie and Siamese. Status: renderer-observed/code-supported; native-game semantics unresolved.

## Procedure

Run `scratch/petz-local-venv/bin/python tools/move_probe.py`. Fixed-span, seed-resolved copies preserve every byte outside the adult LNZ span. Append Move rows to the existing section rather than replacing its contents. Target the head (Dogz 52 / Catz 24); use chest reference 50 / 6. Variants: unchanged, zero vector with chest reference, vector (20,7,-3) with omitted reference, explicit self reference, chest reference, and two copies of the explicit self-reference row.

Direct numerical checks load all six variants in standing/sitting/lying for both species: 36 asset loads. Eight local MCP aligned side-view comparisons check control/zero and implicit/explicit in sitting, plus self/chest references in sitting and lying. Controls: seed 0, age 100, fatness 50, yaw 90°. Environment/renderer revision matches SMOKE-001. Private evidence is scratch/research/move-001; [manifest](move-001.json) includes rows, hashes, geometry deltas and comparison cell equality.

## Findings

- Zero-vector chest-reference rows leave complete modified raw frames unchanged in all six species/pose combinations. Sitting comparison cells are pixel-identical for both species.
- Omitting the fifth value matches explicitly naming the target itself. Raw frames match in all six combinations and sitting comparison cells are pixel-identical.
- With nonzero vectors, changing reference from self to chest changes sitting and lying displacement. Both sampled standing frames have identical head/chest rotation triples (0,0,0), so both references give (20,7,-3) there.
- Example sitting deltas: Dogz self (18,9,-3), chest (19,1,-8); Catz self (18,9,-3), chest (19,2,-7). These are raw frame units, not pixel offsets.
- Two identical self-reference rows double the head's observed displacement in all tested poses. Rows are cumulative here; later rows do not replace earlier Move rows targeting the same ball.
- In Catz only the head base-ball position changes. In Scottie, head movement also changes base balls 6,30,63 through subsequent Project Ball operations. An initial head-only assertion exposed this interaction and was corrected to retain measured downstream changes. This is an experimental finding, not a renderer failure.

The dog sitting and cat lying self/chest comparisons were visually reviewed. They show displaced head components; this remains a diagnostic probe, not a usable head-repositioning recipe.

## Community discrepancy

[Nova's preserved anchoring tutorial](https://petzmainstreet.com/petzu/tutorial/nova-s-guide-to-anchoring-ballz-in-move-lnzpro) describes a fifth-column anchor, including zero-offset entries. This implementation rotates the supplied offset by that ball's frame rotation and does not establish a positional constraint when the vector is zero. The observed no-op therefore does not validate the tutorial's anchoring effect. Record the gap; do not claim the tutorial wrong or patch the renderer without independent native evidence.

Missing evidence: changing raw animation frames beyond named poses, native behavior with matching inputs, saved-pet differences and edited cross-version behavior.
