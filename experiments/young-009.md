# YOUNG-009: count, omission and zero-size controls

2026-11-12. [Manifest](young-009.json). Renderer49c7f62/package0.1.0, all62 installed Python sources match checkout. Petz4 Fuzzkin age12; two mixed-cache modes, three poses, front/side. Renderer-observed and code-supported, not game-validated. Follows [exhaustive tail subsets](young-008.md).

Hold the sufficient young outline/prefix/line/tail substitutions fixed. Build a32-entry added list, preserving the first29 entries. Compare four trailing prefixes of lengths29–32 with all eight visibility masks on entries29–31, implemented separately by omissions of ball IDs96–98 and zero size on those same rows. Every32-entry fixture retains existing indices; masks name the active entries, with bit0=entry29, bit1=30, bit2=31. Existing omissions remain set. These20 variants across12 fixtures yield240 direct PNGs, with12 exact links to the preceding MCP-backed endpoint controls. No new MCP requests or private file copies.

Omitting all three trailing entries and zeroing all three sizes both match the29-entry short control in every fixture. Every matched omission/zero-size pair agrees in pixels. The96 shared geometry balls, fills and prepared commands also equal the short control in all240 outputs. Geometry still has99 balls in the indexed controls, versus96 in the short list; pixel equality does not establish identical topology.

| Front pose | Active masks matching short | Active masks matching full32 |
| --- | --- | --- |
| standing |0|6,7|
| sitting |0,1|6,7|
| lying |0,1,4,5|2,3,6,7|

Both cache modes and both omission/zero-size methods give this table. On side views all masks equal both short and full32. Thus entries30+31 together recover the full32 front output in standing/sitting; entry30 alone recovers it lying. This describes visibility controls on this fixed background; it does not establish independent row-deletion behavior for arbitrary lists, dependency graphs or shades. Entry29 alone produces an intermediate standing result even though it is unnecessary on the full background.

Reproduce with `scratch/petz-local-x86-venv/bin/python tools/young_count_controls.py --verify`. Independently check `scratch/petz-local-x86-venv/bin/python tools/check_young_tail_followups.py --unit young-009`. The latter hashes/decodes all240 images, performs720 aligned RGBA comparisons against short/full/young controls, reconstructs mask equality lists and checks12 prior links. Private evidence:scratch/research/young-009;logs:scratch/young-009-verify.log and scratch/young-009-audit.log. Geometry/command assertions come from the complete renderer replay, not from the independent PNG checker. Originals and renderer source remain untouched.

Initial run, full replay and independent audit pass;the six-row native-scale sheet was reviewed. Other backgrounds, versions and game behavior remain unvalidated.
