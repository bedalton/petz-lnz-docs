# UPDATE-009: reinstall and restart branch fix

2026-11-12. [Manifest](update-009.json). User requested reinstall/restart after the MCP implementation fix. Local service verification only; no native-game or hosted-deployment claim.

The existing checkout already contains `49c7f62eab51b61b9f68801ba7571178670c433e` (`fix(appearance): align mcp branch numbering`). Reinstalled it into `/workspace/scratch/petz-local-x86-venv` using uv, workspace cache/tmp paths, `--reinstall --no-deps`. Package display version remains0.1.0; revision and62 source hashes identify the installed build. Every installed Python source matches checkout. No renderer source changes were made. Checkout AGENTS.md/CLAUDE.md are still dangling symlinks; no additional instructions could be read there.

Stopped old HTTP PID28026 and restarted the Petz4 server as PID28631, managed session86021:

```sh
/workspace/scratch/petz-local-x86-venv/bin/python -I -m petz_renderer.service.local_mcp \
  --game-root /workspace/games/petz4 --transport http --port 8765
```

Endpoint: `http://127.0.0.1:8765/mcp`. Fresh HTTP discovery returns six tools. All five branch-choice schema fields across inspection,single render,contact sheet and before/after comparison now specify minimum1 and explicitly describe one-based authored numbers. Capabilities and four HTTP renders pass:Scottie/Siamese,adult/puppy,standing/front,age12,seed41,fatness50.

A fresh local stdio server using the same installed package and the private YOUNG-004 branch fixture confirms:

| Branch | Updated behavior |
| --- | --- |
| 0 | Rejected by form validation: greater than or equal to1 required |
| 1 | Valid first authored branch; PNG matches a fresh direct render from this installed build |
| 2 | Selects the intentionally missing second branch; missing_asset names ZZMISSING |
| 3 | Rejected as outside the declared branch range |

The numbering behavior for valid existing callers is preserved;the previously misleading schema/minimum is corrected. The branch1 PNG differs from the historical4c4d3df image. The intervening checkout includes other appearance changes;this smoke check does not attribute that pixel drift to a particular commit or establish broad historical render equivalence. Original historical manifests and their pre-fix observations remain unchanged. The [scratch implementation handoff](../scratch/mcp-branch-numbering-handoff.md) is marked superseded by this verification.

Reproduce with `scratch/petz-local-x86-venv/bin/python tools/check_mcp_branch_reload.py`. It overwrites this unit's private artifacts/public report with a fresh run, checks installed/source/runtime/dependency provenance, discovers the actual HTTP schemas, repeats four HTTP renders and four stdio branch probes,and rechecks all21 tracked original hashes. Evidence: scratch/research/update-009; installation log:scratch/update-009-install.log; successful verifier:scratch/update-009-check-final.log. No additional dependency install was needed. Pytest is not installed in this runtime; verification here used actual MCP clients rather than running the checkout's pytest suite.

The server is restarted in this Docker container. The separately hosted chat endpoint and any client-side cached schemas are outside this action; no hosted redeploy or automatic external registry refresh is claimed. Original game files,the pre-existing renderer .gitignore change,and unrelated istall-node remain untouched. Broader rendering changes in intervening commits were not historically replayed by this reload smoke test.
