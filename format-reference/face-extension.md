# Face Extension

`[Face Extension]` contains one signed integer. Zero disables this displacement; it does not mean “restore this breed's source value.” Adult and young resources may supply separate values. [FACE-001](../experiments/face-001.md) tests `0`, `-12` and `12` on Petz 4 blank Labrador and stock Siamese with existing anatomy retained.

## Code-supported operation

On the recorded renderer build, a 67-ball Dogz/Catz frame uses the vector from nose to jaw after earlier body/leg shape operations. Let that vector be **v**, and `L = floor(sqrt(v·v))`. For nonzero `L`, the added displacement on each coordinate is `trunc(-E × v / L)`, where `E` is Face Extension and truncation is toward zero. Zero-length input yields a zero vector. Positions use signed 16-bit wrapping. This is a displacement, not a percent scale or radius change.

The implementation adds the same vector to a fixed species-specific list:

| Species | Raw-frame IDs in the implementation's list |
| --- | --- |
| Dogz | 55, 56, 51, 39, 15, 63, 64, 17, 41, 65, 65 |
| Catz | 37, 40, 7, 31, 30, 55, 56, 4, 5, 57, 58, 59, 60, 61, 62, 65, 65 |

ID 65 occurs twice in each implementation list and receives two additions. Its source labels are uncertain; this code observation supplies no authoring reason to edit or replace it. The head and jaw anchors are outside these lists. This control consequently changes muzzle-to-jaw relationships; it does not translate the entire face as one rigid object.

Head spacing, Ear Extension, Move and Project Ball run later. Added balls attach afterward, and projections involving added IDs can move them again. A moved attachment therefore need not have a moved parent. Pet scale and integer rounding mean `12` does not promise a 12-pixel shift in the final PNG. Face Extension does not directly enlarge radii or alter visibility. A small nonzero scalar can truncate to a zero vector: the sampled young Siamese source value −1 does so in all three FACE-001 frames, and setting it to zero leaves geometry unchanged. This is distinct from a geometry change hidden in the rendered image.

## Renderer-observed scope

[FACE-002](../experiments/face-002.md) extends the scalar controls to stock Scottie/Siamese in Petz 3/4/5 on the same 20cd029 build. All 720 matched Petz 3/5 geometry records and 360 anchor-aligned images equal the Petz 4 controls. Three look modes, numerical ages 0/12/50/100, three poses and the recorded front/profile samples are covered; no other breed/version equivalence is implied. Age 12/100 match forced young/adult geometry in 180 comparisons; age 0 has separate juvenile shrink and differs in all 90 forced-young comparisons despite matching Face Extension values.

[FACE-001](../experiments/face-001.md) records the exact inputs, current build, local MCP controls, unchanged anatomy/dependencies, arithmetic oracle and aligned comparisons. Its isolated oracle disables unrelated shape/Move/Project controls before checking the formula; the asset sweep separately records the complete original construction. Do not substitute isolated displacements for final breed geometry.

Use the [mouth guide](../visual-editing/existing-mouth-and-muzzle.md) for the authoring loop and preservation requirement. Values here are diagnostic controls, not a safe range, finished muzzle recipe or native-game specification. Native behavior, expression blending, extreme values, genetics and other breeds remain outside these experiments. [Community cautions](../sources/mouth-shaping.md) remain attributed source reports.
