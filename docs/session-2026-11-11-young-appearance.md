# Fifteen-minute puppy/kitten continuation

2026-11-11, starting17:15UTC. Renderer4c4d3df in scratch/petz-local-x86-venv. This session follows [UPDATE-008](../experiments/update-008.md); it does not claim to revalidate all historical experiments after the loader/default changes.

| Unit | Scope | Initial-run evidence |
| --- | --- | --- |
| [YOUNG-001](../experiments/young-001.md) | Petz3/4/5 Scottie/Siamese age/look/default controls |306 local stdio MCP renders,132 aligned equality relationships,two reviewed Petz4 sheets |
| [YOUNG-002](../experiments/young-002.md) | Three Petz4 saved pets with independently missing caches |12 private fixtures,nine cache-omission edits,216 direct renders,84 command/PNG equalities,36 exact MCP matches |
| [YOUNG-003](../experiments/young-003.md) | All integer ages and young-only Petz4 edits |606 numerical records,six private breed fixtures,84 direct outputs,28 original-control renders,24 exact MCP matches |

The [focused reference](../format-reference/young-appearance.md) records lookup,defaults,age arithmetic and cache applicability. The coverage ledger's earlier “Little one unrendered” statement is superseded for this build. All findings remain code-supported or renderer-observed. Native-game behavior,clothing,other breeds and general equivalence of forced young versus blended appearance are not established.

## Integrity and replay

Run the three unit `--verify` commands and `scratch/petz-local-x86-venv/bin/python tools/check_young_session.py`. The session auditor checks public manifests and private artifacts,all606 research PNG hashes and recorded RGBA/dimensions,input/copy hashes,source/dependency/runtime agreement,204 cross-version pixel comparisons,21 historical original hashes and a fresh HTTP age12 Scottie render. Unit verifiers additionally reconstruct/reload copies and repeat arithmetic/rendering; YOUNG-003 documents its loader-boundary/API replay split.

Detailed audit,capabilities and replay logs remain under ignored scratch/research/young-session and scratch/young-00{1,2,3}-verify.log. No original game files or renderer source files were edited. The renderer's pre-existing .gitignore change and unrelated istall-node remain untouched. The first final-audit attempt found the earlier HTTP process absent and failed to connect; its traceback is preserved in scratch/young-session-final-audit.log. Restarted the server in managed session82886 and reran the audit; the successful retry log is scratch/young-session-final-audit-retry.log. The cause of the old process exit was not established. Local HTTP uses127.0.0.1:8765/mcp; the separately hosted chat MCP is independent.

All three full unit replays pass. The final audit confirms606 research PNGs,606 numerical age records and128,472 field assertions,366 initial MCP render/match calls,328 direct renders including28 original controls,18 private fixtures andfour reviewed sheets. All204 Petz3/5 aligned comparisons match Petz4;62 installed Python sources match checkout;all21 tracked originals retain their hashes. Research/replay/health render counts are kept separate. The [public audit](../experiments/young-session.json) links input/manifest/script/log hashes and cross-version/endpoint comparisons.

Next: isolate which fields cause the mixed-cache Fuzzkin endpoint difference,or test explicit young-name/branch selection and missing-resource errors with private breed copies. Historical paint/texture/geometry experiments retain their earlier-build provenance;this session is not a wholesale replay. This fifteen-minute authorization ends with the session.
