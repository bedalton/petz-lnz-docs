# YOUNG-005: mixed-cache endpoint attribution

2026-11-12. [Manifest](young-005.json). Renderer4c4d3df, Petz4 Fuzzkin, baseline and three cache-omission copies from [YOUNG-002](young-002.md). This is renderer evidence, not native-game fidelity.

The age12 appearance and forced-young appearance are compared in standing/sitting/lying, front/side. Both resolve identical frames, sizes, texture tiles and palettes; substitutions change immutable appearance lists while keeping those dependencies fixed. All fields outside balls,add_balls,lines and paint_balls are equal. Baseline and missing-both differ only in paint direction normalization; their six views each match pixels without substitutions.

For each mixed-cache fixture, all16 subsets of the four differing lists are substituted from forced young into age12. For baseline and missing-both, both subsets of their single differing list are tested. The240 saved direct PNGs comprise216 substitution outputs and24 forced-young targets. Twenty-four fresh local stdio MCP baselines match exactly;16 standing PNG links match YOUNG-002. Full replay passes.

| Pose/view | Missing-adult pixels | Missing-young pixels | Minimal sufficient lists |
| --- | ---: | ---: | --- |
| standing/front |239|218|balls,add_balls|
| standing/side |63|62|balls,add_balls|
| sitting/front |241|229|balls,add_balls,lines|
| sitting/side |47|46|balls,add_balls,lines|
| lying/front |211|220|balls,add_balls,lines|
| lying/side |58|63|balls,add_balls|

Differences count aligned decoded RGBA pixels on the union canvas using recorded portrait offsets. Each listed sufficient set is minimal among all tested list subsets;paint replacement is not required in any view. This is not additive attribution or proof that paint is inert under other list combinations. The manifest retains all subset outcomes,field-level record differences and dimensions/offsets.

Code in appearance/age.py retains adult-only ball metadata and lines, and keeps the adult added-ball list when lengths differ. Here the mixed caches have29 versus32 added balls;the base-ball differences are speckle colors and outline colors on14/38;four lines differ in edge_mode. These observations motivate the narrower [field controls](young-006.md). The source's list rules explain why100% young weight need not equal forced-young appearance.

Reproduce: `scratch/petz-local-x86-venv/bin/python tools/young_endpoint_attribution.py --verify`. It checks prior manifest/input hashes, reloads the inputs, repeats every substitution/render, byte-compares saved PNGs, rechecks prior links and repeats all24 MCP baselines. Private evidence: scratch/research/young-005;successful replay log:scratch/young-005-verify.log. No new game-file copies,original/source changes or native validation. Other pets,ages and versions remain untested by this unit.
