# Add a detail that follows a body part

Initial scope: Petz 4 Scottie/Siamese, a synthetic head marker and one base-to-marker connector. Evidence: [ADD-001](../experiments/add-001.md). [LINE-001](../experiments/line-001.md) adds connector/endpoint-omission tests. This does not yet cover ears made from multiple balls/lines or inherited second-generation behavior.

1. Inspect the effective Add Ball section and count its parsed rows. Compute the appended ID from base-ball count plus existing added-ball count; do not assume another file's ID.
2. Choose the parent by anatomy. Start with add group 0, an untextured/fuzz-free diagnostic marker and an offset that is visible in front/side views. Read the [field layout](../format-reference/add-ball.md).
3. Append a row, preserving existing rows and dependent references. Render insertion and movement comparisons with fixed controls.
4. If the parent changes shape, explicitly inspect the detail. Ordinary attachment can follow movement while keeping its own radius and offset unchanged under Head Enlargement.
5. If size should follow another ball, investigate the optional size-reference field. It adds a scaled radius adjustment to the referenced radius; it does not simply interpret size as an ordinary diameter.
6. Check sitting/lying, depth overlap, connections and omissions before accepting the detail. Integer rounding means parent and attachment pixel deltas need not match exactly.

Hide an experimental marker by adding its ID to Omissions rather than removing its row and shifting later IDs. [LINE-001](../experiments/line-001.md) also tests a connected marker: omitting either endpoint removes the connector. Omitting the parent head leaves the marker visible; hide each desired component explicitly. Read the [Linez field reference](../format-reference/linez.md) before adding connections.
