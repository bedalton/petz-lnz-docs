# UPDATE-001: renderer upgrade and finding review

Date: 2026-11-10. User supplied [RENDERER_CHANGES.md](../RENDERER_CHANGES.md), naming native-port changes c6f1eda/b3dc464. The local Python integration is commit6c1d88325ced89109f8e4b9d724fa8ab6037b42c, replacing9d72d7afd5f7460ef18133c6179caaf8055082d9. These are different repositories/commit identities; native commits are source-reported, the integration diff is code-inspected. No game-validated evidence is added.

The noneditable workspace package was still old. It was force-reinstalled with workspace uv cache/tmp paths, then HTTP PID428 was terminated and replaced by PID8300 on127.0.0.1:8765/mcp with explicit Petz4. HTTP discovery/get_capabilities succeeds; fresh stdio processes perform replays. All installed Python sources are checked against the updated checkout. Package display version stays0.1.0, so revision/source hashes identify the upgrade. The checkout's pre-existing .gitignore change is preserved; no renderer source edits are made by this research.

## Changed-path controls

[Control audit](update-001-controls.json). `tools/renderer_change_controls.py` runs against the historical source archived privately from git and the new installed package; `tools/check_renderer_change_controls.py` reruns both and checks expected differences. Private outputs and hashes: scratch/research/update-001/{old-controls,new-controls,controls-verification}.json. Twelve outline rasters,21 paint rasters,eight clip rasters,12 add-ball projections and three parser cases are executed per revision. Art is synthetic, asset-free. Updated checkout regression tests:68 pass across core,attachment,circle dispatch,texture,paint,preparation,composition. Their native goldens compare with a native **port**, not the original game.

| Affected statement/path | Review status and evidence |
| --- | --- |
| Blanket textured paint balls are unimplemented (GAP-007) | **Withdrawn for this updated renderer.** Nine shaded-colour controls now carry texture; out-of-ramp colours stay flat. Textured paint output is identical across sampled outline types-1/1/4. This establishes sampled renderer support, not game fidelity. |
| Blanket textured Outline balls are unimplemented (GAP-007) | **Withdrawn for this updated renderer.** Textured styles1/2/4 now differ from the old flat interior; untextured controls and fully filled oversize rings remain unchanged in this corpus. |
| Non-Outline host clipping inset1 | **Corrected to0.** Styles-4/-3/-2/-1/0 gain52 clipped pixels in the synthetic case; Outline1/2/4 keep insets0/1/3. Iris/rim measurements need new pixels. |
| Legacy paint texture is a direct slot | **Corrected below version2.** With ball3's overridden texture7, missing/version1 paint texture3 resolves7; version2 keeps3. Historical direct-slot assumptions are invalid for those low-version paths. |
| Add-ball projection entries are ignored | **Corrected implementation behavior.** All12 new controls satisfy integer projection for real→add,add→real,add→add at0/50/100/150; only three identities matched before. Prior PROJECT-001/field reference explicitly left full added-ball behavior untested, rather than claiming native no effect. |
| Group-colour retint | Three resolved shaded colours yield distinct remapped-art hashes. **Source/code-supported integration; saved-group override not separately re-exercised.** Do not substitute this check for end-to-end genetic/saved-group evidence. |
| Body-area lists require version>1 or species0 | Code path unchanged in this update; existing version-gate evidence remains historical until a selected numerical replay confirms it. |

Paint rotation is exercised at the preparation API boundary with supplied frame delta(3,-2). That is narrower than validating host-derived rotation across an animation. Clothing remains unrendered; Head Shot/Little one and the source-reported offscreen flat-paint edge case remain unsupported/unresolved. Fur Markings/Fur Color Areas are source-reported genetic/breeding controls, not appearance draws for an existing pet.

**Column-number caveat:** the notice calls texture the10th value and flat mode the11th. The inspected Python parser uses zero-based indices10/11, i.e. the11th/12th whitespace-separated fields including base, percentage and all three direction components. Controls preserve their full rows; use parsed field names rather than copying the notice's ordinal numbering. Color Info Override uses its own distinct column layout.

Initial control attempts used an incorrect CircleClip attribute and a dormant add-group/incorrect override row. They are archived privately; corrected controls explicitly activate add group0 and verify ball3 texture7 before interpretation. An initial replay harness encountered a list-shaped inventory manifest; it was corrected to skip non-object manifests. No historical evidence was overwritten.

## Historical replays

Available top-level path-based comparison/contact-sheet controls are being replayed into scratch/research/update-001, using exact historical input hashes and explicit game versions. Historical experiment JSON and raw evidence stay intact. Final replay counts, finding classifications and pending scope will be recorded here after completion. A pixel-hash change does not by itself overturn a comparison relationship or numerical claim.
