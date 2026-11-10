# LINE-015: oversized textured connector in breeds

Date:2026-11-10. Renderer-observed Petz4 Scottie/Siamese, not native-game validation. [Manifest](line-015.json). Reproducer `scratch/petz-local-venv/bin/python tools/line_texture_limit_breed.py` refuses overwrite. Private copies/images scratch/research/line-015. No renderer changes; hashes/dependencies/backend recorded.

Builds short offset -80 and long offset -800 head-attached marker controls. Within each distance group, compare inherited head texture (fill -1), explicit125 and no appended connector. Both endpoints have base color125; head retains its stock256x256 texture and marker is untextured. Fuzz0, edges244/244, widths100/100, edge mode0 and draw_after1 fixed; existing lines are frozen. Seed0, age100, fatness50.

36 numerical loads across three poses/species preserve geometry within each distance group. Both short line styles produce isolated raster pixels. The long textured line still parses, is retained in appearance and builds a non-null block with a texture paint, but its isolated raster has zero colored pixels. The equivalent long explicit line produces pixels. Line/canvas dimensions and counts are recorded; endpoint visibility/eligibility and parser rejection do not explain this isolated distinction.

All16 local stdio MCP comparisons pass in standing front/side: short textured and explicit lines each differ from marker-only; long inherited-texture line equals marker-only; long explicit line differs from marker-only. Two sheets reviewed: Dogz long-texture/none front and Catz long-explicit/none side. This corroborates LINE-014's size guard in composed breed images: a long textured connector can disappear while the equivalent explicit-fill connector remains visible.

This is a sampled renderer limitation, not evidence that the native game has the same limit. No speculative fix is proposed. Exact threshold sweeps, diagonals, other tile sizes/breeds/versions and native fidelity remain pending. Different offsets intentionally change marker geometry; comparisons are only within matching offset groups. Originals remain unchanged and private texture pixels/renders are not tracked.
