# Fifteen-minute young-routing continuation

2026-11-12, 12:09–12:24 UTC. Continues [the young-appearance session](session-2026-11-11-young-appearance.md) on renderer `4c4d3df`. Scope is Petz 4 Scottie/Siamese routing and Fuzzkin cache endpoints. Findings are code-supported or renderer-observed; original-game validation remains open.

| Unit | New evidence |
| --- | --- |
| [YOUNG-004](../experiments/young-004.md) | 14 private breed copies, 90 direct loader/MCP cases, 108 PNGs; 54 successes and 36 expected missing-resource failures |
| [YOUNG-005](../experiments/young-005.md) | 240 PNGs exhaust differing-list subsets across four cache modes and six pose/views; 24 exact MCP baseline matches |
| [YOUNG-006](../experiments/young-006.md) | 420 PNGs exhaust five field factors and three controls per mixed-cache pose/view |
| [YOUNG-007](../experiments/young-007.md) | 144 PNGs test individual added-ball/line reversions and a three-entry count group |

Explicit young selectors rescue broken Little one routing and are case-sensitive. Forced adult skips young dependencies; age100 still requires them. Branch-driven routing follows the effective selected branch. Mixed-cache Fuzzkin age12 differs from forced young because age composition retains adult metadata and unequal-length added lists. Outline colors on balls 14/38, added-list entries 23 onward and selected line edge modes suffice to restore the sampled pixels. Individual line reversions reproduce residuals of 1–3 pixels; the count group affects front views only. These are scoped substitution results, not exhaustive semantic or anatomical validation.

All four full replays pass. The [session audit](../experiments/young-continuation.json) records 912 saved research PNG hashes and decoded RGBA hashes, 780 independently reconstructed pixel differences, 40 prior-image links, 14 new private breed copies,four reused saved fixtures,four reviewed sheets, 21 unchanged original hashes and 62 installed/checkout source matches. Initial research made 114 MCP requests: 78 successful PNG matches and 36 expected errors. The four unit replays repeat those calls separately. A fresh HTTP health render and four branch-numbering audit calls are additional checks,excluded from the 114 research requests. Audit retries made additional health renders; the five render calls describe one completed final auditor invocation, not a lifetime retry total. There are 948 initial direct render calls,including 36 unsaved target/baseline controls; 912 outputs are retained. Replay counts are separate.

Reproduce the unit scripts with `--verify`, then rebuild the sheets and run the session audit:

```sh
scratch/petz-local-x86-venv/bin/python tools/young_resource_routing.py --verify
scratch/petz-local-x86-venv/bin/python tools/young_endpoint_attribution.py --verify
scratch/petz-local-x86-venv/bin/python tools/young_endpoint_fields.py --verify
scratch/petz-local-x86-venv/bin/python tools/young_endpoint_entries.py --verify
scratch/petz-local-x86-venv/bin/python tools/young_continuation_sheets.py
scratch/petz-local-x86-venv/bin/python tools/check_young_continuation.py
python3 tools/check_docs.py
```

The auditor expects successful replay logs in scratch/young-00{4,5,6,7}-verify.log. It records their hashes,manifest/script hashes,engine and original hashes,and runtime/dependency/source agreement. Detailed evidence and the four sheets remain in scratch/research/young-continuation. No proprietary binary,text resource or raw render is committed.

The first audit reached the health check but found HTTP unavailable;its traceback remains in scratch/young-continuation-audit.log. Server restarted as PID28026,managed session90633,on127.0.0.1:8765/mcp. The successful final log is scratch/young-continuation-audit-final-retry.log; the earlier successful health retry is scratch/young-continuation-audit-retry.log. An intermediate audit attempt expected an unflattened JSON Schema $defs entry and failed; the schema actually embeds the branch object inline. That harness error was corrected and its traceback is preserved in scratch/young-continuation-audit-final.log. Discovery,capabilities and an actual forced-young Scottie render pass against the private-copy baseline. The old process's exit cause is unknown;this does not reload the separately hosted chat endpoint.

The MCP BranchChoice schema describes a zero-based branch index and accepts a schema minimum of0,but the controlled branch audit finds0 rejected,1 selecting the valid first branch,2 selecting the missing second branch,and3 rejected as out of range. The schema and exact responses are recorded in the audit. No renderer fix was made;the wording/validation inconsistency needs a separate source change with its own reproducer and regression checks. Use the observed one-based branch numbers for this build rather than inferring behavior from the schema description.

Original game files and renderer source remain unchanged. The renderer's pre-existing .gitignore edit and unrelated istall-node remain untouched. All four research units were committed using the required identity and no co-author trailers.

Next: native evidence for age endpoint semantics; controlled other-pet/version samples; remaining added-tail interactions; or the isolated MCP branch-numbering schema inconsistency. Historical experiments retain their earlier-build provenance. This fifteen-minute authorization ends with the session.

Final status review removed transient replay-pending entries from STATUS.md and marked the corresponding handoff units complete. The only root working-tree remainder is the pre-existing untracked istall-node.
