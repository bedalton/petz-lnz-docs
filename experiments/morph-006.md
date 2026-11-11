# MORPH-006: current relative-morph replay

Date: 2026-11-11. Petz 3/4/5 Scottie and Siamese; renderer integration `6c1d88325ced89109f8e4b9d724fa8ab6037b42c`. This is code-supported and renderer-observed evidence, not original-game validation. No renderer changes.

The exact [MORPH-002](morph-002.md) relative-size activation behavior persists on the current build. All six species/version fixtures have the same 24 numerical records as the historical Petz 4 fixture for that species. This closes the current-build numerical replay caveat for this case only.

- Group 15 relative-size 20 initializes evaluated size zero and retains zero at 0/25/50/100%.
- Offsets scale; the marker is parked at 0%. At each positive tested amount its radius equals the head radius.
- At 100% its complete posed geometry equals static relative-size 0, and its radius differs from static relative-size 20.
- Ordinary-size controls scale size and equal the static ordinary counterpart at full activation.
- The ordered 100→0→50 history equals a direct 50 update in each species/pose.

There are 144 numerical records across standing/sitting/lying, 30 fixed-span private breed copies, and 36 fresh local stdio MCP comparison pairs (72 RGBA cells). MCP covers default state only: dormant relative/ordinary markers match, static relative 0/20 differ, and static relative 0/dormant relative 20 differ, in front/side views. The twelve Petz 3 and twelve Petz 5 pairs each exactly match the corresponding current Petz 4 cell hashes and PNG bytes. Matching previews do not establish native cross-version semantics.

Reproduce with `scratch/petz-local-x86-venv/bin/python tools/revalidate_relative_morph.py`; fresh runs refuse existing evidence. `--verify` rebuilds all input bytes in memory, reloads every numerical fixture, rehashes/crops every saved MCP sheet, and checks dependencies, all 62 installed/checkout sources, actual checkout revision, original breeds and twelve shared-engine hashes. Both run and verification passed. The Petz 4 private copies exactly match MORPH-002 input hashes; historical reports and private artifacts are preserved.

[Manifest](morph-006.json), [script](../tools/revalidate_relative_morph.py); private evidence `scratch/research/morph-006`, run/verify logs in `scratch/morph-006-{run,verify}.log`. First setup attempt omitted the resolver's version setting and stopped on the Petz 3 fixture before producing a result; its copies/log are preserved in `scratch/research/morph-006-attempt1` and the run log was superseded by the successful run. No game originals were written. Native intended behavior remains [GAP-005](../troubleshooting/rendering-gaps.md).
