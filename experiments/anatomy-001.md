# ANATOMY-001: stock label and key inventory

Date: 2026-11-09. Status: asset-reported, not full visual validation.

`tools/anatomy_inventory.py` reads Dalmatian and Siamese adult LNZ resources plus DOGMASTER/CATMASTER in each of Petz 3, 4 and 5. It collects factual labels, hashes, section row counts, key IDs and eye IDs, without publishing stock LNZ rows or extracted files. Run with scratch/petz-local-venv/bin/python. Renderer/Python environment is recorded in SMOKE-001.

All six inputs have 67 Ballz Info rows. Dalmatian row comments and Siamese enumeration labels supply complete candidate indices. Each species' 67 labels, ten master key IDs and four eye IDs match across the three sampled versions. Assertions check these facts. This does not establish that all breeds have identical semantics, that every ball is visible or independently movable, or that labels were correctly interpreted by the original game.

- [Dogz labels](../format-reference/anatomy/dogz.md)
- [Catz labels](../format-reference/anatomy/catz.md)
- [Hashes and derived inventory](anatomy-001.json)

An important limitation: the sampled master LNZ resources do not contain Ballz Info. They identify selected key balls and eyes, but the complete aesthetic table is in these breed resources. Cat master jaw/chin key slots contain -1 even though labeled jaw/chin balls exist in the breed. Do not treat missing key slots as proof that the anatomy is absent.

Label agreement is an economical starting map; per-ball perturbation and multi-view review remain necessary. L/R means the stock label, with anatomical-side interpretation pending. The only initial visual perturbations concern head IDs 52 (Dogz) and 24 (Catz) in BALL-001.
