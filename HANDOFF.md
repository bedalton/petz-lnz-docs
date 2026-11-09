# Handoff

Updated: 2026-11-09

## Read first

AGENTS.md → STATUS.md → docs/research-plan.md. Commit every logical unit using bedalton identity, conventional titles under 50 characters preferred/65 hard limit, no co-authors. Keep all durable work under /workspace. User requests autonomous continuation through next steps until roughly 65% context use; exact context percentage is not exposed.

## Environment

- Local environment: scratch/petz-local-venv, CPython 3.12.16. uv cache and managed Python under scratch. Use uv --link-mode copy; default cached-wheel install hit a mount permission error.
- Renderer is a separate ignored checkout, revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, with a pre-existing .gitignore modification. Noneditable installed package; no renderer source changes. No AGENTS.md found inside it at research start.
- Read petz-renderer-mcp/docs/local-mcp.md for setup. Stdio MCP works for all six species/version samples. Hosted MCP is available as fallback; saved .pet inputs supported only in Petz 4.
- games/, scratch/ and renderer checkout are ignored. Private outputs are under scratch/research/<experiment-id-lowercase>. Scripts currently overwrite their experiment directories on rerun: copy prior evidence before changing procedures.
- Git ownership can require `git -c safe.directory=/workspace ...`; use the scoped override instead of relying on global configuration.

## Completed evidence

- SMOKE-001: six successful Scottie/Siamese local renders across 3/4/5. Hash manifest and procedure in experiments/.
- BALL-001: Petz 4 isolated head size/color/move edits; normalized controls match originals and prior smoke PNGs. Head movement separates circle from facial features. First color attempt was a no-op because 35 already matched Scottie; final uses 125.
- ANATOMY-001: 67 candidate labels per species, using Dalmatian comments/Siamese labels; labels and master key/eye IDs agree across sampled 3/4/5 assets. Visual tests mostly pending. Master LNZ has no Ballz Info in samples. Cat jaw/chin key slots -1 do not mean those anatomical balls are absent.
- INHERIT-001: absent/empty/partial/full Key Balls variants through local MCP, eight renders. Empty/partial sections clear unspecified master slots; full section matches absent PNG. See updated format-reference/inheritance.md.
- Three community sources indexed in sources/community-index.md. Zero-offset Move anchoring claims differ from renderer's rotated-vector interpretation; needs explicit tests and independent validation.

## Next actions

HEAD-001 completed: see experiments/head-001.md and tools/head_shape_probe.py. Eight aligned MCP comparisons (front/side standing), numerical checks in three poses. Equal +25 increments to A or B give identical radius arrays but spread versus crowd feature centers; renderer uses A+B for base diameters, A-B for spacing with an A!=100 gate. Four comparison images reviewed. MOVE-001 now complete: tools/move_probe.py, 36 numerical asset loads and eight MCP comparisons. Zero-vector reference rows are no-ops; omitted reference equals self; nonzero reference matters in sitting/lying, hidden by neutral standing rotations. Scottie projections propagate head movement to 6,30,63. Community anchoring gap documented, not a confirmed renderer defect. HEAD-002 now confirms A=100 gate with 24 numerical asset loads and four MCP comparisons: (100,25) changes radii but not raw centers versus (100,0); (99,25)/(101,25) activate center scaling. Three images reviewed. Coverage/navigation/checks now exist: agent-guides/start.md, docs/coverage.md (generator tools/coverage_index.py), tools/check_docs.py. The ledger currently contains 41 section topics, a six-combination evidence matrix and priorities. EYE-001 now complete: eight visually reviewed MCP comparisons and 30 numerical pose checks separate pupil fill, iris outline and host-eye fill. See eye-colors recipe. Right iris is viewer-left in tested front views. Next: added-ball/head interactions and controlled visual anatomy validation. Expand ball-map visual coverage systematically, not by assuming stock labels prove behavior. Documentation structure is agent-first; website deferred.

## Safeguards and open limits

tools/research_common.py safely rewrites only a fixed-size adult LNZ span, checking resource metadata and unrelated bytes/payloads. It serializes seed-resolved sections, removing comments/variation alternatives; this is not a variation-preserving general PE editor. tools/ball_probe.py has its original equivalent implementation. Original games are never written. Rendering is evidence for this implementation, not established original-game fidelity. Public material excludes proprietary files and raw renders. No complete anatomy validation, concept-to-breed workflow, or native game comparison exists yet.

## Resume commands and final checks

Run `scratch/petz-local-venv/bin/python tools/check_docs.py` for Markdown targets, manifest JSON/hash syntax and exclusion of private tracked files. It does not establish scientific correctness. Rebuild docs/coverage.md with the same interpreter and tools/coverage_index.py; update its explicit evidence mapping when promoting coverage. Do not rerun expensive render experiments unless changing inputs or resolving a specific uncertainty. Eye experiment tool: tools/eye_color_probe.py; evidence scratch/research/eye-001 and experiments/eye-001.md/JSON. Future eye work should test more breeds/views, shape/clipping controls and saved/young differences.
