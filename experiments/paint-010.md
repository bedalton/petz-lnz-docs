# PAINT-010: exact paint direction cancellation

Date: 2026-11-10. Synthetic direction edits in private Petz 4 Fuzzkin copies, integration `6c1d883`. [Manifest](paint-010.json), [reproducer/verifier](../tools/paint_direction_midpoint.py).

Four length-preserving copies isolate one paint on host 50. In both caches, the adult direction is `(0,0,-1)`. The matched young control is also `(0,0,-1)`; the opposed young direction is `(0,0,1)`. The second and third host-50 rows are blanked in every copy. Cross both direction choices with surface on/off. Other paint hosts and non-paint fields stay unchanged.

At ages 55/56/57, young weights are 52/50/49. The opposed resolved direction goes from positive Z to a zero-vector sentinel to negative Z. The exact cancellation produces an all-NaN internal direction, which the paint geometry code maps to `(0,0,0)`. With surface enabled, that point fails the front-side test. With surface disabled, the prepared command has the full diameter-scaled extent centered on the host. Both midpoint front/side views verify these command outcomes and the latter's exact bounds. Age 100 bypasses the young direction.

**Command evidence only for the difference:** all 16 opposed/matched RGBA comparisons are equal in the sampled standing views, even where prepared paint commands differ. For example, at midpoint front, the matched surface variant prepares one command and the opposed surface variant prepares none, yet the images match. No cause for the lack of visible coverage is established. This does not show a visible disappearance or establish behavior for near-opposite, non-axis directions.

Four copies, eight age/view fixtures, 32 direct draws and eight fresh local stdio MCP midpoint views. Saved seed/fatness, explicit ages 55/56/57/100, yaw 0/64, fresh raster/line seed 1 and step 0. MCP PNGs match direct exactly. The copies preserve every byte outside the two cache ranges; the renderer does not validate their PetzInfo stream checksums. No original or renderer edits, and no native game validation.

```sh
scratch/petz-local-venv/bin/python tools/paint_direction_midpoint.py --verify
```

The verifier reconstructs the copies, reloads and redraws all 32 views, and checks persisted MCP hashes. It makes no new MCP calls. Private evidence: `scratch/research/paint-010`.
