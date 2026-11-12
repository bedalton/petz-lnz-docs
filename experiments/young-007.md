# YOUNG-007: individual endpoint entry reversions

2026-11-12. [Manifest](young-007.json). Renderer4c4d3df, Petz4 Fuzzkin mixed caches; code-supported and renderer-observed, not game-validated. Follows [YOUNG-006](young-006.md).

Start with the sufficient full field substitution from YOUNG-006. Revert one added-ball entry23–28 to its age12 record,restore the three-entry count difference as a group,or revert one line entry11–14. These11 reversions plus the full-substitution control give144 PNGs across two mixed-cache modes,three poses and two views. All12 full controls match prior PNG hashes and forced-young pixels. Frames/palettes/textures are held fixed as in the preceding units;no new MCP calls or game-file copies.

Individual line reversions explain the small residuals measured in the earlier units:

| Pose/view | Missing-adult reversion | Missing-young reversion |
| --- | --- | --- |
| sitting/front |line14:1 pixel|line12:1 pixel|
| sitting/side |line11:2 pixels|line11:1 pixel|
| lying/front |line11:3 pixels|line11:2 pixels|

Every other individual line reversion equals forced young in these fixtures. Entry13 changes no pixels in any view. This is one-entry sensitivity on the sufficient substituted background,not exhaustive interaction attribution.

Added entry26 changes no sampled pixels on that background;other entries have pose- and cache-dependent effects detailed in the manifest. Reverting the three-entry count group changes all six front views,15–41 pixels,and no side views. The shared-index probes do not establish semantic equivalence of stock versus saved entries:positions can represent different content when list lengths differ. The count group preserves existing common indices and adds/removes entries29–31 together;it does not identify their individual effects.

Reproduce `scratch/petz-local-x86-venv/bin/python tools/young_endpoint_entries.py --verify`. It checks prior/input hashes,reloads appearances,repeats all144 renders,rehashes saved PNGs,rechecks12 prior full-control links and compares the complete report. Private artifacts:scratch/research/young-007;replay:scratch/young-007-verify.log. Original files and renderer source remain untouched. Other backgrounds,combined reversions,ages,pets,versions and native-game behavior remain open.

Full replay passes;the [independent session audit](young-continuation.json) checks all144 saved outputs and their RGBA differences. Forty of the132 reversion outputs differ from the sufficient background;the12 full controls match.
