# Add a detail that follows a body part

Use this page for genuinely new ornaments or diagnostic markers. For existing ears/tail use [reshape existing anatomy](existing-ears-and-tail.md); for muzzle, cheeks, jowls, lips, chin, jaw or tongue use [mouth/muzzle preservation](existing-mouth-and-muzzle.md). Do not use an added chain to replace hidden native anatomy.

Initial scope: Petz 4 Scottie/Siamese, a synthetic head marker and one base-to-marker connector. Evidence: [ADD-001](../experiments/add-001.md). [LINE-001](../experiments/line-001.md) adds connector/endpoint-omission tests. This does not yet cover ears made from multiple balls/lines or inherited second-generation behavior.

1. Inspect the effective Add Ball section and count its parsed rows. Compute the appended ID from base-ball count plus existing added-ball count; do not assume another file's ID.
2. Choose the parent by anatomy. Start with add group 0, an untextured/fuzz-free diagnostic marker and an offset that is visible in front/side views. Read the [field layout](../format-reference/add-ball.md).
3. Append a row, preserving existing rows and dependent references. Render insertion and movement comparisons with fixed controls.
4. If the parent changes shape, explicitly inspect the detail. Ordinary attachment can follow movement while keeping its own radius and offset unchanged under Head Enlargement.
5. If size should follow another ball, investigate the optional size-reference field. It adds a scaled radius adjustment to the referenced radius; it does not simply interpret size as an ordinary diameter.
6. After adding a connector, inspect effective body area. [AREA-001](../experiments/area-001.md) finds an ankle connection reassigns a head marker from area 8 to 3, changing its numerical head-rotation response. Explicit area 8 did not prevent reassignment.
7. Check add group and parked state. [MORPH-001](../experiments/morph-001.md) distinguishes dormant geometry from omission; visible=true alone is insufficient.
8. Check sitting/lying, depth overlap, connections and omissions before accepting the detail. Integer rounding means parent and attachment pixel deltas need not match exactly.

An unwanted newly added diagnostic marker can be omitted rather than shifting IDs by deleting its row; do not apply this cleanup rule to existing ears/tails or stock mouth details. [LINE-001](../experiments/line-001.md) also tests a connected marker: omitting either endpoint removes the connector. Omitting the parent head leaves the marker visible; hide each desired component explicitly. Read the [Linez field reference](../format-reference/linez.md) before adding connections.


## Connector controls tested so far

| Need | Tested control and evidence |
| --- | --- |
| Narrow a broad connector | Reduce endpoint percentages; equal percentages still depend on separate ball radii ([LINE-002](../experiments/line-002.md)) |
| Suppress the connector with widths | Both zero reject its block; a single zero leaves a clamped tip in these tests ([LINE-002](../experiments/line-002.md)) |
| Place fill relative to endpoint circles | Column 10: 0 before first visit, 1 after both; -1 uses global fallback ([LINE-003](../experiments/line-003.md)) |
| Use a shortened row | Two IDs use defaults including global endpoint thickness; explicit row widths override it ([LINE-004](../experiments/line-004.md)) |

These are sampled renderer controls, not a native-validated ornament recipe. Keep independent controls for appearance, body-area response and group visibility.
