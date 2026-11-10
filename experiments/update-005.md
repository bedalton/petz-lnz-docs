# UPDATE-005: nested cross-version texture replay

Date: 2026-11-10. [Manifest](update-005.json). Follow-up to [LINE-016](line-016.md) on integration6c1d88325ced89109f8e4b9d724fa8ab6037b42c. Local stdio MCP processes use explicit Petz3/Petz5 game roots and version flags; the display name remains Petz4 Renderer.

**Confirmed:** all32 nested historical comparison relationships survive. All32 new PNGs and64 RGBA cells exactly match their corresponding updated Petz4 LINE-013 replays from UPDATE-001. All32 historical cell pairs change pixels. This closes the nested LINE-016 exclusion in the earlier upgrade review, without extending the tested breed, pose, texture-size or original-game scope.

The60 assembly loads (Scottie/Siamese, three poses, five variants, two versions) retain their recorded connector fill, texture selection, source texture bytes and remapped paint bytes. Geometry is equal across variants within each species/pose/version. Numerical equality here concerns the recorded connector fields, not complete old-versus-new geometry snapshots. The MCP comparisons cover standing front/side only.

Reproduction: `scratch/petz-local-venv/bin/python tools/revalidate_nested_textures.py` requires a fresh output folder. Verification: `scratch/petz-local-venv/bin/python tools/check_nested_texture_update.py`. The verifier reassembles all60 cases and checks32 saved PNGs/64 cropped cells, controls, cross-version links,20 private copy hashes, engine hashes, dependency versions and all62 installed sources against the checkout. The private report and verification live under scratch/research/update-005. Historical manifests and private input copies are unchanged; no renderer source or original game files were edited.

This is code-supported and renderer-observed evidence only. Repeatability and cross-version agreement do not establish native-game fidelity. Other baseline-only, synthetic and retained-history units remain outside this replay.
