# LINE-012: attributing RNG differences to fuzzy connectors

Date:2026-11-10. Direct local renderer composition; no new MCP calls or native-game validation. [Manifest](line-012.json). Reproducer `scratch/petz-local-venv/bin/python tools/line_rng_attribution.py`; refuses overwrite. Reuses verified LINE-007 inputs and LINE-011 controls. Private evidence scratch/research/line-012; original four-cell exploratory output archived as line-012-target-only. Renderer unchanged.

## Method

Twelve Petz4 Scottie/Siamese pose/view fixtures each produce six aligned cells: fresh, whisker0-primed, only diagnostic connector primed, primed except diagnostic connector, all positive-fuzz connectors primed, and primed except all positive-fuzz connectors. Target step1, seed1, prepared commands and raster dimensions are fixed. Prior pixels are discarded.

A research-only LineRenderer subclass records pre-draw state. For substituted connector pixels it advances the main renderer using a discarded framebuffer, then draws that connector into the real framebuffer with a separate renderer restored to the alternate state's RNG/tables. Thus subsequent draw calls retain the main path's expected state. Assertions verify final RNG/tables are unchanged by substitution relative to their corresponding original path, and the diagnostic block is visited exactly once. No renderer source patch is involved.

Fresh and primed cells exactly match LINE-011's corresponding cells in all12 fixtures, reusing its12 exact MCP baseline checks. Twelve six-cell sheets contain72 RGBA cells. Before-target/after-scene state pairs are saved for all72 compositions (144 state snapshots). Two sheets reviewed: Dogz standing/front and Catz lying/front.

## Results

The diagnostic fuzz7 connector alone does **not** account for the complete scene change: substituting only it leaves24–179 indexed pixels different from the fully primed scene. Restoring it in a primed scene still leaves24–178 pixels different from fresh. Existing fuzzy connectors contribute to the residual.

Substituting all positive-fuzz connector draws reproduces the fully primed scene exactly in12/12 fixtures. Restoring all positive-fuzz connector draws reproduces fresh exactly in12/12. The main RNG/table state still follows its original path in each case. This attributes the observed whisker0-priming scene difference to positive-fuzz connector raster pixels under these controls; no residual needs a geometry, circle texture or target-whisker explanation.

Pixel changes need not add because drawing can overlap. This is an intervention on pixel production, not a decomposition into independent semantic body parts. It does not establish attribution for other prior histories, moving frames, breeds/versions or native gameplay. Private snapshots, source/dependency/resource DLL/reused-copy hashes and per-cell hashes support reproduction. Original breed hashes rechecked.
