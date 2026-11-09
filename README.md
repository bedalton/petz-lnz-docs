# Petz LNZ research

An evidence-backed, agent-first guide to designing Petz breeds from images and concepts, growing into a thorough LNZ reference. Research starts with Petz 4 Dogz/Catz, then validates edited behavior across Petz 3 and 5. Current findings describe renderer behavior; original-game fidelity remains unverified.

## Start here

- [Agent editing entry point](agent-guides/start.md)
- [Coverage ledger](docs/coverage.md)

- [Status](STATUS.md), [handoff](HANDOFF.md), [agent instructions](AGENTS.md)
- [Research plan](docs/research-plan.md)
- [Community source ledger](sources/community-index.md)

## Reference and editing

- [Dogz base-ball labels](format-reference/anatomy/dogz.md), [Catz base-ball labels](format-reference/anatomy/catz.md): visual checks mostly pending
- [Section inheritance](format-reference/inheritance.md)
- [Move](format-reference/move.md) and [renderer evidence gaps](troubleshooting/rendering-gaps.md)
- [Head Enlargement](format-reference/head-enlargement.md)
- [Choosing head editing controls](visual-editing/head-ball.md)

## Evidence

- [SMOKE-001: local rendering across versions](experiments/smoke-001.md)
- [BALL-001: isolated head-ball edits](experiments/ball-001.md)
- [ANATOMY-001: labels and master keys](experiments/anatomy-001.md)
- [INHERIT-001: section replacement](experiments/inherit-001.md)
- [HEAD-001: head size versus spacing](experiments/head-001.md)

Raw stock resources, private breed copies and rendered images remain outside Git under ignored persistent scratch storage. Each experiment links its machine-readable hash/control manifest.
- [MOVE-001: reference-column behavior](experiments/move-001.md)
- [HEAD-002: A=100 spacing boundary](experiments/head-002.md)

Documentation checks: `scratch/petz-local-venv/bin/python tools/check_docs.py`. Regenerate the section ledger with `tools/coverage_index.py` using the same interpreter.
