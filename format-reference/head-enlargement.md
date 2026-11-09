# Head Enlargement

Status: Petz 4 renderer-observed and code-supported for Scottie/Siamese. [HEAD-001 evidence](../experiments/head-001.md). Game fidelity and edited cross-version behavior remain unverified.

The two values occupy **separate rows**, not two columns on one row:

```text
[Head Enlargement]
A
B
```

A and B above are placeholders for integers. The renderer defaults missing values to A=100, B=0; these defaults are code-supported, not tested here as native-game rules.

| Component | Renderer behavior |
| --- | --- |
| Head-area animation base diameters | Multiply by (A+B)/100, truncating toward zero |
| Head-area base-ball center spacing | Scale around head center by (A-B)/100, only when A != 100 and species/topology gates pass |
| Final pixel radii | Also depend on static size, frame modifiers, fatness, scale, rounding and clamping |

The diameter term describes animation base diameters, not final radii or all added balls. A==100 skips this position-scaling operation even if B is nonzero; that gate is now confirmed by [HEAD-002](../experiments/head-002.md) for both sampled breeds in three poses. Move and Project Ball execute afterward and can alter spacing further.

In tested pairs (103,0)→(128,0)/(103,25) for Scottie and (105,0)→(130,0)/(105,25) for Siamese, both edits give the same radius arrays, but increasing B crowds features inward while increasing A spreads them. See the [head editing workflow](../visual-editing/head-ball.md) before using this control.

At B=25, moving A from 100 to 99 or 101 activates spacing changes that are skipped at exactly 100. Do not assume smooth interpolation across that boundary. Native-game correctness is still unverified.
