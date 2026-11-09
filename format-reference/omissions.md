# Omissions

Status: Petz 4 renderer-observed in Scottie/Siamese. [OMIT-001](../experiments/omit-001.md), plus [ADD-001](../experiments/add-001.md). Native-game behavior remains unverified.

```text
[Omissions]
ballID
```

Use one numeric ID per row. Preserve existing rows. The renderer reads the first numeric token; examples here use a single token to avoid ambiguity. IDs refer to base or added balls; adding an ID does not remove or renumber its definition.

| Tested case | Observed result |
| --- | --- |
| Ordinary visible ball | Can disappear; incident lines are removed too |
| Already omitted ball | No further pixel change |
| Added unconnected marker | Visibility becomes false; position/radius and row retained |
| Iris ID | No pixel change in tested views because iris drawing uses host-eye overlays |

An unchanged image is not proof that an ID is unused or incorrectly labeled. Check effective omissions, pose, radius, depth, line dependencies and special overlays. The Siamese base nose ID 37 is already omitted in the stock resource; this does not mean the visible nose is absent or controlled solely by that ID.

Omitting a host-eye ball and omitting an iris ball are different operations in this implementation. Do not assume every named component obeys a single visibility path; see [GAP-004](../troubleshooting/rendering-gaps.md).

Implementation source at revision 9d72d7afd5f7460ef18133c6179caaf8055082d9: appearance/core.py parses omissions and drops Linez endpoints; rendering/attachment.py marks ordinary geometry invisible; rendering/assembly.py and preparation.py implement iris overlays. Other group/morph/head-tracking interactions remain open.
