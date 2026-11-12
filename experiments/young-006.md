# YOUNG-006: endpoint field attribution

2026-11-12. [Manifest](young-006.json). Renderer4c4d3df, Petz4 Fuzzkin, missing-adult/missing-young fixtures reused from [YOUNG-002](young-002.md). Narrows [YOUNG-005](young-005.md) with immutable appearance substitutions; no original-game validation or new MCP calls.

Each of the12 pose/view/mixed-cache fixtures exhausts32 combinations of five factors:ball14 outline color,ball38 outline color,added-ball entries0–22,added-ball entries23 onward,and the line list. The added-ball prefix differs only in body_area;the line list differs only in edge_mode on entries11–14. Three further controls substitute speckle colors alone,paints alone,and all five factors together. All420 outputs are retained privately and replayed byte-for-byte. The12 unchanged baseline PNG hashes match YOUNG-005;that unit supplies24 fresh MCP baseline checks.

| View | Minimal sufficient factors in both mixed-cache modes |
| --- | --- |
| standing/front |outline14,outline38,add-tail|
| standing/side |outline14,add-tail|
| sitting/front |outline14,outline38,add-tail,lines|
| sitting/side |outline14,add-tail,lines|
| lying/front |outline14,outline38,add-tail,lines|
| lying/side |outline14,add-tail|

Every speckle-only and paint-only control equals its age12 baseline. Every all-factor control equals forced young. Added-prefix substitution is unnecessary in all12 minimal sets;this does not establish that body_area is inert under other rotations or edits. Ball38's outline is unnecessary in the sampled side view. The add-tail factor includes both differing entries and the29-versus32 count change;individual tail entries have not been isolated. The four edge-mode entries are treated together. Minimality is established only within this explicitly tested factor family.

Two aligned field sheets were reviewed at native resolution. Outline substitution visibly changes the eye rims;tail substitution restores or removes the extra rendered details. Small line residuals require numerical comparison;visual similarity is not counted as equality. The routing unit's two sheets were also reviewed. Regenerate all four with `scratch/petz-local-x86-venv/bin/python tools/young_continuation_sheets.py`;all source PNG hashes are checked before composition. Sheets and their manifest remain under scratch/research/young-continuation.

Reproduce `scratch/petz-local-x86-venv/bin/python tools/young_endpoint_fields.py --verify`. It checks source/copy/prior-manifest hashes, reloads inputs, asserts the field partition, reruns all420 outputs and all12 previous baseline links, and byte-compares the complete report. Private evidence:scratch/research/young-006;replay:scratch/young-006-verify.log. No original game files,renderer source or saved copies are modified. Native endpoint semantics,other ages/pets/versions and individual line/tail attribution remain open.
