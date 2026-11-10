# PAINT-006: cached paint group versus color

Date: 2026-11-10. Petz4 Fuzzkin/Homebody/Goobe, integration6c1d883. [Manifest](paint-006.json), [reproducer/verifier](../tools/saved_paint_groups.py). Private evidence:scratch/research/paint-006.

## Results

Changing every Paint Ballz group to0 or1 in both authoritative caches leaves prepared commands and PNG/indexed pixels identical in all36 comparisons across three poses and front/side views. The final loaded paint records retain the requested group value. Group0 clears the unsupported-paint-fields diagnostic;group1 retains it. Thus an unchanged image does not mean the parser discarded the edit.

Changing only each paint's color to65 supplies separate positive controls. All six Fuzzkin views change (front/side respectively:standing90/58,sitting49/48,lying3/21 RGBA pixels). Homebody and Goobe have no prepared-command or pixel changes in these sampled views. Their source paint colors still parse as65;they are not positive visible controls. The experiment does not assign those paints anatomical meaning.

Eighteen local stdio MCP edited renders (three variants ×three pets ×front/side standing) exactly match direct outputs. Direct evidence comprises72 draws in18 four-cell fixtures,with18 contact sheets. Six standing front/side sheets were inspected at native resolution;columns are baseline/group0/group1/color65. Fuzzkin's color edit is visibly distinct;group columns remain identical. This is renderer observation,not game validation.

## Copy integrity and controls

Nine copies preserve original file/cache lengths. A token-span replacement touches only field9 (zero-based group) or field5 (color) within adult/young Paint Ballz rows. The verifier reconstructs edits,checks all outside-cache bytes,exact saved metadata apart from caches,all source hashes,and parsed field changes. Other appearance fields remain equal for group variants;geometry remains equal for all variants. Header/tail bytes remain untouched. The renderer does not validate the saved PetzInfo checksum;these are renderer probes,not validated game saves.

Saved age/seed/fatness remain effective;three named poses,yaw0/64 engine units,fresh state,raster/line seed1,step0. Manifest records all62 installed/checkout Python hashes,dependencies,engine hashes and PAINT-001 provenance. No renderer or original files changed.

## Reproduce

```sh
scratch/petz-local-venv/bin/python tools/saved_paint_groups.py --verify
```

Verification rerenders all72 cells,reconstructs nine copies and checks persisted MCP PNG hashes;it makes no new MCP calls. Generation refuses an existing output directory. A first attempt incorrectly required every color edit to change prepared commands;Homebody has no such change. That failed evidence remains in scratch/research/paint-006-attempt1 with its log. The final experiment records positive-control outcomes rather than assuming visibility. An implementation-only RGBA comparison optimization was replay-verified after generation.

## Limits

This extends PAINT-004 from preparation to sampled saved-pet cache loading,including stored mixed-age assembly. It does not decode native saved-group retint semantics,prove fidelity of skipped prefix arrays,or generalize to other pets/species/versions. Explicit age extremes and native evidence remain separate work.
