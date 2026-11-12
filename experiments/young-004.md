# YOUNG-004: young resource routing and failures

2026-11-12. [Manifest](young-004.json). Renderer4c4d3df, Petz4 Scottie/Siamese only. Code-supported and renderer-observed; no original-game validation.

Fourteen private breed copies replace only the adult resource span with seed41-resolved sections and a controlled Little one row. The seven variants per species are a valid selector, lowercase filename with path/extension, exact X sentinel, lowercase x, missing resource, missing first row followed by a valid second row, and a two-branch selector. Resource layout, other resource payloads and bytes outside the edited span are checked unchanged by the shared copy writer. Originals are never written.

Ninety direct loader cases and90 local stdio MCP calls agree:54 successes and36 expected failures, with108 direct front/side PNGs and54 exact MCP front matches. Eighty-four recorded equality relationships check forced adult and explicit valid young overrides against controls; six additional path/branch front/side relationships per species are asserted in the script.

- Little one path/extension and lowercase stem normalize to the stock uppercase selector; the second row is not tried after a missing first row.
- Exact X reports absent young selection; lowercase x normalizes to resource X and reports a missing resource instead. Both fail for young and age100.
- Explicit young_name rescues every invalid Little one variant. Unlike Little one text, explicit lowercase young_name is used case-sensitively and fails in these breeds.
- Forced adult succeeds despite broken Little one and ignores even an explicit missing young_name.
- Branch1 selects the valid young resource; branch2 fails on the missing dependency. An explicit valid young_name rescues branch2. Seed41 chooses the missing branch in this authored fixture.

Reproduce: `scratch/petz-local-x86-venv/bin/python tools/young_resource_routing.py --verify`. It reconstructs and byte-compares every private copy, reruns all cases and both-view renders, and repeats every MCP call. The Python loader accepts branch_selections; the MCP form accepts branch_choices objects. The initial harness incorrectly passed the Python field to MCP, so its failure and artifacts are retained in scratch/young-004-attempt1.log and scratch/research/young-004-attempt1. The corrected run uses the MCP form and passes. This was a harness error; no renderer change was needed.

Private evidence is scratch/research/young-004. The manifest includes input/copy/source/runtime/dependency hashes and exact controls; shared engine hashes are audited in the continuation session. Empty sections,259-character truncation, inheritance cycles, alternate breeds/versions and native-game behavior remain outside this matrix.

The continuation session completed full replay and reviewed two aligned routing sheets. Its [audit](young-continuation.json) additionally isolates the MCP branch-number schema inconsistency:the form describes zero-based numbers,but this build rejects0 and uses1/2 for these two branches. See the [session evidence](../docs/session-2026-11-12-young-routing.md) for exact scope.
