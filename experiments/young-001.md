# YOUNG-001: fresh breed age/look controls

2026-11-11. [Manifest](young-001.json). Renderer-observed controls on revision4c4d3df; no original-game validation.

`tools/young_breed_probe.py` uses fresh local stdio MCP servers for Petz3/4/5 Scottie and Siamese. Each species/version has51 renders: standing front/side at ages0/6/11/12/13/50/99/100; forced adult at0/100 in standing/sitting/lying front/side; additional age0/12/100 sitting/lying; puppy/kitten aliases at0/100 front/side; omitted defaults, explicit defaults and seed0. Explicit controls use seed41,fatness50. All306 renders are preserved privately with wire metadata, input/PNG/RGBA hashes, dimensions and offsets. Inspection and fresh six-tool discovery run for each version; drawing schemas expose look.

There are132 asserted aligned equality relationships: forced adult ignores age in six pose/views; age100 equals forced adult; puppy/kitten aliases agree; forced young ignores age; age12 agrees with forced young in the sampled standing views; omitted defaults equal explicit age12/seed41/fatness50; seed0 resolves41. Equality includes decoded RGBA,dimensions and offsets. These stock endpoints do not establish equivalence for arbitrary edited metadata or mismatched list structures.

Two Petz4 contact sheets were reviewed at native pixel scale: Scottie/Siamese ages0/6/11/12/13/50/99/100 plus forced adult/young, front/side. They show smaller juvenile forms growing toward the adult endpoint. Sheet generation uses saved offsets to align the cells; images remain private. No visual fidelity conclusion is drawn.

Reproduce with `scratch/petz-local-x86-venv/bin/python tools/young_breed_probe.py --verify`. The verifier requires exact source/dependency/runtime provenance, reruns all306 MCP renders and132 relationships, compares complete public records and checks preserved PNG bytes. Fresh runs refuse to overwrite existing private evidence. Private output: scratch/research/young-001. The manifest includes source/dependency/runtime versions and resource/cache identities; final session audit adds engine/original hashes and cross-version comparisons.
