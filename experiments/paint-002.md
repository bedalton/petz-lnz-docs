# PAINT-002: individual paint-angle attribution

Date: 2026-11-10. [Manifest](paint-002.json). Fuzzkin/Petz4 integration6c1d883. Builds on all24 Fuzzkin histories from [PAINT-001](paint-001.md),using the same saved controls,three poses,two views and four histories.

**Renderer-observed:** the host-only and combined-texture prepared frames have equal geometry and all equal commands except the angles of paint entries16,17,18. Replacing those three angle fields restores host-only pixels exactly in24/24 cases. Individual substitutions change visible pixels in4/24 cases for entry16,23/24 for17,and16/24 for18. These are renderer paint-list indices,not anatomical ball IDs. Hidden/occluded contributions and overlapping markings prevent treating counts as universal anatomical visibility or additive causal shares.

For each case,six saved draws compare combined texture,host-only,three individual angle resets,and all three resets. The substitute retains combined geometry,ordering,ball commands,textures/fills,paint bounds and every non-angle paint field. The returned state may still differ;the claim is exact drawn pixels,not full-state equivalence. Combined-versus-host differences range2–52 indexed pixels in these24 fixtures.

`tools/paint_angle_attribution.py` requires a fresh scratch/research/paint-002 folder. `tools/check_paint_angle_attribution.py` replays all cases,checks144 exact PNGs,48 PAINT-001 links,unchanged saved input/engine/dependency/source hashes,and assertions that only the three angles differ. Both pass. No new MCP calls:the earlier fresh saved-pet baselines remain the MCP boundary;retained controls are direct renderer evidence. No original files or renderer source changed.

Two PAINT-001 standing front/side sheets were visually reviewed privately (scratch/research/paint-session-review);the visible changes are subtle surface pixels,consistent with unchanged numerical geometry. This adds no native-game validation. Painted-group retint,other saved pets/versions and independent native evidence remain outside this experiment.
