# Change iris, pupil or outer-eye color

Status: tested in Petz 4 Scottie/Siamese previews only. Evidence: [EYE-001](../experiments/eye-001.md). Native-game validation remains open.

| Desired change | Field | Dogz right / left IDs | Catz right / left IDs |
| --- | --- | --- | --- |
| Iris ring | Outline Color Override | 38 / 14 | 28 / 27 |
| Pupil center | Color Info Override on iris balls | 38 / 14 | 28 / 27 |
| Outer eye region | Color Info Override on host eye balls | 32 / 8 | 15 / 14 |

For example, to change both Catz iris rings to palette index 125, preserve existing rows in Outline Color Override and append:

```text
27, 125
28, 125
```

Add the section header if the section is absent, after checking [inheritance](../format-reference/inheritance.md). These rows are not Ballz Info rows: override sections explicitly include a ball ID, whereas Ballz Info identifies balls by row position. Palette 125 is the diagnostic index tested here, not a universal requested color. Palette selection needs its own guide.

Keep pupil fill, outline mode/width and sizes unchanged when changing only iris hue. In EYE-001 this retained geometry and changed the visible iris rings. For one eye, edit one iris ID. At tested front yaw 0°, the asset's right eye is viewer-left; use IDs instead of assuming screen sides at other angles.

Render an aligned baseline comparison with fixed seed, adult age and fatness. Inspect both eyes for color, pupil contrast, clipping and unintended changes. Other breeds may have overrides, variation choices or unusual eye styling; inspect effective sections rather than assuming stock defaults. Saved pets and young resources are outside this recipe's tested scope.
