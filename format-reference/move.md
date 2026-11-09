# Move

Status: Petz 4 renderer-observed in Scottie/Siamese. [MOVE-001](../experiments/move-001.md). Native anchoring behavior remains unresolved.

```text
[Move]
ball, x, y, z, referenceBall
```

The fifth column is optional in this renderer and defaults to `ball`. The first four values identify a target and a displacement vector. The renderer rotates that vector using referenceBall's raw frame rotations, then adds it to the target. It does not copy referenceBall's position. Raw units are not screen pixels.

- Preserve existing Move rows when adding an experiment. Multiple rows for the same target accumulate in tested cases.
- Zero-vector rows have no observed effect here, even with a different reference ball.
- Reference changes can be invisible in a neutral frame and visible in other poses. Test more than standing.
- Project Ball runs after Move and can propagate changes to other balls. Scottie head displacement affected ear-tip and tongue positions in MOVE-001; Catz did not share that dependency for the tested head.
- Addball placement is a separate mechanism. These tests target base balls only.

[Nova's anchoring tutorial](https://petzmainstreet.com/petzu/tutorial/nova-s-guide-to-anchoring-ballz-in-move-lnzpro) uses stronger anchoring language than these results establish. See [rendering gaps](../troubleshooting/rendering-gaps.md). Do not promise positional anchoring from a zero-vector entry in this preview system.

Implementation sources at revision 9d72d7afd5f7460ef18133c6179caaf8055082d9: appearance/core.py parses optional referenceBall; rendering/positions.py rotates/applies Move rows, then Project Ball rows. Broader validity limits and game semantics need separate investigation.
