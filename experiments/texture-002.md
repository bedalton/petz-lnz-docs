# TEXTURE-002: constant-pose orientation arithmetic

Date: 2026-11-10. Code-supported numerical explanation of [TEXTURE-001](texture-001.md), not native-game validation or a renderer fix. No new images/MCP calls.

Run `scratch/petz-local-venv/bin/python tools/texture_arithmetic_probe.py`; refuses existing output and requires private TEXTURE-001 snapshots. [Manifest](texture-002.json) records matrix arithmetic, seven exact state matches, controls, source/engine/dependency hashes and runtime version. Private report: scratch/research/texture-002. Original Scottie hash matches TEXTURE-001; four engine hashes match its verified provenance. Installed rotation/orientation source bytes match checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9.

## Observed calculation

Use stock Scottie sitting, seed0, age100, fatness50, yaw0, fixed pose frame, observed prepared ball42. The same integer orientation matrix is retained on every sampled repeat:

```
243  -58   54
 74  228  -90
-30   97  233
```

The evaluator's Q8 `transpose_times(matrix,matrix)` is:

```
255    0   -2
  0  252   -4
 -2   -4  255
```

It is not the Q8 identity. The last-row terms feed `atan2(value,255)*256/(2*pi)`: approximately -0.31955 and -0.63906 angle units. Rounding produces (0,-1), matching the per-repeat delta. An exact Q8 identity matrix self-product remains identity, providing a numerical no-drift arithmetic control.

Replaying `update_texture_orientation` from the observed first post-draw state with the unchanged real frame-ball rotations and resolved after-tilt reproduces all seven saved frame2–8 states exactly, including matrix, accumulated angles and frame deltas. No sampler write-back adjustment is needed to match this specific trace. This traces the observed angle drift to the current integer matrix self-product/rounding path rather than morph activation or changing geometry.

This explanation covers one demonstrated matrix/path. It does not establish intended native arithmetic, whether the original game retains identical quantized matrices, or whether this is a renderer defect. GAP-006 remains open for independent native evidence; no speculative repair or game-fidelity claim.
