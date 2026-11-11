# Relative morph continuation: 2026-11-11

Three research units extend current-build evidence without modifying the renderer or original game files. All claims below are code-supported/renderer-observed. Original-game semantics remain unvalidated.

| Unit | Scope | Verification |
| --- | --- | --- |
| [MORPH-006](../experiments/morph-006.md) | Exact relative-size activation replay on Scottie/Siamese in Petz 3/4/5; all six fixtures match historical Petz 4 geometry |144 numerical records,30 private fixed-span copies,36 local stdio MCP comparison pairs/72 RGBA cells |
| [MORPH-007](../experiments/morph-007.md) | Nonnegative size-reference gate versus earlier-ID radius lookup; dormant references, negative sizes and 1% activation |1,728 numerical records,72 direct rasters, two reviewed standing sheets |
| [MORPH-008](../experiments/morph-008.md) | Identity-remapped size-reference chains/cycles across all six marker permutations and five group modes |936 numerical records,120 direct rasters, two reviewed standing sheets |

The grouped relative-size behavior from GAP-005 persists on integration `6c1d88325ced89109f8e4b9d724fa8ab6037b42c`. Its current-build numerical caveat is closed for the exact sampled fixtures. Petz 3/5 default-state comparison PNGs equal current Petz 4. This does not establish native version equivalence.

Morph size updates test the sign of the size-reference token; radius inheritance separately requires an earlier assembled target. An activated probe can therefore be visible and unparked with radius 0 when its reference is unresolved or dormant. Remapping IDs after a row reorder does not remove this dependency. Head-rooted grouped chains propagate radius only through earlier markers; fully grouped cycles remain all 0 in these controls.

The full unit verifiers pass. [The aggregate audit](../tools/check_relative_morph_session.py) independently verifies 2,808 numerical-record coverage,228 research PNG hashes,36 MCP metadata/input/control records,30 copy hashes,18 engine/breed original links,12 cross-unit source links,24 cross-version sheet equivalences and 84 decoded RGBA pair comparisons. It reconstructs/checks four review sheets against individual saved images. The separate restoration audit checks all 21 recorded originals, including the three untouched saved pets. All 62 installed Python sources match the checkout; dependency versions, actual renderer HEAD, four tool hashes, three replay-log hashes and manifest digests are recorded privately. No historical experiment evidence was overwritten.

Reproduction commands, using the current x86 environment:

```sh
scratch/petz-local-x86-venv/bin/python tools/revalidate_relative_morph.py --verify
scratch/petz-local-x86-venv/bin/python tools/morph_reference_boundaries.py --verify
scratch/petz-local-x86-venv/bin/python tools/morph_size_chains.py --verify
python3 tools/check_game_restore.py > scratch/relative-morph-originals.log
scratch/petz-local-x86-venv/bin/python tools/check_relative_morph_session.py
python3 tools/check_docs.py
```

Fresh research runs refuse existing folders; verify modes preserve inputs and PNGs. The aggregate refreshes only its ignored audit/sheet/health records. Private final evidence: `scratch/research/relative-morph-session-verification.json`, `scratch/research/relative-morph-session-health.json`, and `scratch/relative-morph-session-audit.log`.

The HTTP server was absent at final audit. Restarted with the restored x86 environment at `http://127.0.0.1:8765/mcp`, PID15068/managed session90208. Six-tool discovery, capabilities and an actual Scottie standing/seed0/age100/fatness50/yaw0 render pass; the PNG equals a fresh direct portrait. This additional health render is separate from the 36 research comparison calls. No hosted-backend calls were needed.

Originals and renderer source remain unchanged. The renderer retains its pre-existing `.gitignore` modification; unrelated untracked `istall-node` remains untouched. Commits use the required bedalton author/committer identity and no coauthor trailers. The fifteen-minute authorization applies to this continuation only.

Next useful work: independent native/source evidence for GAP-005, omitted size-reference targets, or controlled other-breed/non-default scale/fatness probes. Current chain/cycle results apply to the two sampled Petz 4 breeds only. The exact isolated replay covers six Scottie/Siamese Petz 3/4/5 fixtures; the reference-boundary and chain matrices do not inherit that wider version coverage. Do not convert these renderer boundaries into game-file authoring rules without independent validation.
