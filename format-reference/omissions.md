# Omissions

Status: Petz 4 renderer-observed in Scottie/Siamese. [OMIT-001](../experiments/omit-001.md), plus [ADD-001](../experiments/add-001.md) and [EYE-002](../experiments/eye-002.md). Native-game behavior remains unverified.

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
| Connected added marker | Omission removes its incident connector; parent omission leaves marker visible ([LINE-001](../experiments/line-001.md)) |
| Iris ID | No pixel change in tested views because iris drawing uses host-eye overlays |
| Right host eye / host plus iris | Same pixels as each other, different from control in EYE-002 front/side |

An unchanged image is not proof that an ID is unused or incorrectly labeled. Check effective omissions, pose, radius, depth, line dependencies and special overlays. The Siamese base nose ID 37 is already omitted in the stock resource; this does not mean the visible nose is absent or controlled solely by that ID.

Omitting a host-eye ball and omitting an iris ball are different operations in this implementation. Do not assume every named component obeys a single visibility path; see [GAP-004](../troubleshooting/rendering-gaps.md).

Implementation source at revision 9d72d7afd5f7460ef18133c6179caaf8055082d9: appearance/core.py parses omissions and drops Linez endpoints; rendering/attachment.py marks ordinary geometry invisible; rendering/assembly.py and preparation.py implement iris overlays. Other group/morph/head-tracking interactions remain open.

Explicit area lists can reclassify an omitted added marker without making it visible: [AREA-006](../experiments/area-006.md). Head Balls restores area 8 and numerical head-rotation response, while visible remains false and incident parsed lines remain absent in sampled Petz 4 Scottie/Siamese.

## Consequential shading changes

[SHADE-003](../experiments/shade-003.md) separates removed geometry from changed depth shading in fresh Petz4 Scottie/Siamese states. Eleven of804 base omission cases reduce visible depth bounds;seven change fill arrays and eight change pixels when compared with the same omission holding original shade offsets. Unomitted ball positions/radii remain fixed. Thus image differences can include shading elsewhere as well as omitted balls/incident lines. See [depth shading](z-shade-slope.md); no native-game claim.
