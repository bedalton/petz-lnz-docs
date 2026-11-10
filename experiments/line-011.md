# LINE-011: composed breed pixels and retained line RNG

Date:2026-11-10. Direct local renderer composition with Petz4 Scottie/Siamese copies plus local stdio MCP baseline checks. No native-game validation or renderer changes. [Manifest](line-011.json). Run `scratch/petz-local-venv/bin/python tools/line_composed_history.py`; refuses overwrite. Reuses verified fuzz7 copies from [LINE-007](line-007.md); private output scratch/research/line-011.

## Isolation

Twelve prepared scenes (two species, three poses, yaws0/90) are held fixed across seven line-renderer histories. Each history starts with LineRenderer(seed1), performs prior operations if specified, discards prior pixels and draws the same immutable target PreparedFrame into a fresh framebuffer. No geometry, shading or texture FrameState is retained; prepared representation hashes remain unchanged after every target draw. Target raster step1 suppresses whisker RNG consumption in the target scene. This is an explicit state-isolation experiment, not a retained animation simulation.

Each fixture also saves a fresh step0 baseline. All12 baselines match render_portrait and actual local stdio MCP PNGs byte-for-byte at seed0/age100/fatness50. Twelve eight-cell sheets contain96 RGBA cells: fresh step0 followed by the seven step1 history targets. Two sheets reviewed: Dogz standing/front and Catz standing/side. Manifest records source/dependency/resource DLL/original/reused-copy/PNG/cell hashes;168 before/after line states are saved privately with hashes.

## Results

| Prior line-renderer history | Changed target fixtures /12 |
| --- | --- |
| Fresh | 0 |
| Same scene at step1 | 0 |
| Same scene at step0 | 3 |
| Other pose scene at step1 | 11 |
| Synthetic whisker at step0 | 12 |
| Synthetic whisker at step1 | 0 |
| Synthetic fuzz3 connector | 12 |

The three prior-step0 differences occur in Catz side views (standing198, sitting235, lying173 indexed pixels). Other-pose history changes109–470 pixels in11 cases; Catz sitting/front stays equal. Synthetic whisker0 priming changes265–440 pixels; fuzz3 priming changes199–458. These are whole-scene differences, not per-connector attribution. Existing stock lines and whiskers remain in the scene.

Repeated step1 scene and whisker1 controls match fresh in all12 fixtures. Together with discarded prior pixels and fixed prepared commands, the differences establish an effect of retained line RNG/tables in these composed scenes. They do not imply that every different history must change visible pixels, or that the native game uses these exact state rules.

Broader breeds/versions, actual evolving poses/FrameState, connector-only pixel attribution and native comparison remain pending. Source hashes match installed/checkout files; originals remain unchanged.
