# Paint Ballz

Scope: inspected Python parser/preparation on integration6c1d883; synthetic changed-path controls plus sampled Petz4 Fuzzkin/Homebody/Goobe saved-pet state and group experiments. Original-game semantics and broader versions remain unvalidated.

The code-inspected row order is:

```text
base, diameter_percent, direction_x, direction_y, direction_z, color, outline_color, fuzz, outline, group, texture, surface
```

The first eleven fields are required by this parser; surface is optional and defaults true. This is a code-supported layout, not a newly exhaustive parser experiment. The [change notice](../RENDERER_CHANGES.md) calls texture the10th value; the inspected Python parser uses zero-based index10 (the11th field). Keep full rows and use field names when translating examples. Malformed required fields are skipped; the parser normalizes finite direction vectors. Group-colour support is not established by the texture-state experiments below.

[UPDATE-001](../experiments/update-001.md) tests textured paint preparation, legacy texture lookup and outline bypass. A loaded paint texture is used when the resolved, host-shaded fill lies in10–149. Out-of-ramp fills stay flat. Textured paint bypasses the sampled outline style/colour appearance; untextured controls remain distinct. Below Lnz Version2, the texture field resolves through that numbered base ball's texture after overrides, rather than directly naming a texture slot. Do not apply a blanket historical 'paint texture has no effect' conclusion to this build.

Paints clip against their host. The updated non-Outline host inset is0; Outline inset is type minus1. See UPDATE-001 for controlled differences and limitations. Rim placement and visual anatomy still require specific composed tests.

[PAINT-001](../experiments/paint-001.md) demonstrates nonzero retained paint angles in Fuzzkin:three textured paints change pixels in all24 sampled motion/repeat histories. Homebody supplies24 zero-effect controls with no configured paint texture. [PAINT-002](../experiments/paint-002.md) isolates host-versus-combined differences to angles on entries16/17/18, holding every other prepared-command field equal. Those are paint-list indices, not ball IDs.

For direct retained renders, persist the complete FrameState returned after drawing, including per-paint sampler write-back. [PAINT-003](../experiments/paint-003.md) shows that the vector is indexed by original paint-list order and a length mismatch resets the whole vector. Equal vector length does not prove compatibility after appearance edits. [PAINT-009](../experiments/paint-009.md) shows stale indices attaching distinct test angles to the wrong rows after a same-length reorder. The actual sampled same-host angles are equal, so their remap has no effect. Start fresh after changing paint order. Fresh MCP stills do not exercise retained motion histories. See [texture state](texture-state.md) for controls and revision-specific evidence.

[PAINT-004](../experiments/paint-004.md) checks180 group-only synthetic comparisons:prepared commands remain equal across groups0/-1/1/2/15/255, with180 nonzero-group diagnostics. Color positive controls change fills in216/216 cases. This bypasses saved-pet assembly and supplies no new pixels.

[PAINT-005](../experiments/paint-005.md) changes three skipped saved-prefix arrays independently/together in copies of Fuzzkin, Homebody and Goobe:72 direct edited views and24 fresh MCP variant views match unchanged caches/baselines. This tests ignored prefix payloads, not native array semantics or cached paint group tokens. PetzInfo checksums remain unvalidated.

[PAINT-006](../experiments/paint-006.md) follows group edits through both saved caches and mixed-age assembly:all36 group0/group1 comparisons retain commands/pixels, while diagnostics change. Fuzzkin color65 edits change six views; Homebody/Goobe lack visible positive controls here. This establishes sampled renderer behavior, not native retint semantics.

[PAINT-007](../experiments/paint-007.md) extends Fuzzkin group equivalence across ages0/50/100, three poses and front/side (36 comparisons; 16 MCP matches). Color controls change17/18 fixtures; prepared paint eligibility does not guarantee a displayed change.

[PAINT-008](../experiments/paint-008.md) separates adult and young cache edits. In the sampled Fuzzkin host, adult supplies color at every tested age. Equal counts pair by ordinal within that host and blend size and direction; a count mismatch retains its adult rows. Reordering young rows changes direction pairing below age 100.

[PAINT-010](../experiments/paint-010.md) checks exactly opposing axis directions at the 50% young weight (age 56). Cancellation skips surface paint and centers the non-surface command. The sampled images remain equal; command changes need not be visible.

Uncertainty:the installed diagnostic explicitly reports nonzero paint group controls as unsupported; UPDATE-001's resolved-colour remap checks do not establish end-to-end saved-group override. Native saved-group retint semantics remain open. Clothing and source-reported offscreen flat-paint edge behavior are separate gaps. No renderer observation here is game validation.
