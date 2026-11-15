# Blank dog reference catalog

2026-11-13. Entry point: [clean_dogs/README.md](../clean_dogs/README.md). The [authoring workflow](../agent-guides/picture-to-breed.md) and agent entry point link to the catalog.

## Scope and outputs

Rendered all 28 supplied Petz 4 blank `.dog` files and ten corresponding original stock breeds. Six views per input: standing yaw 0/45/90/180, sitting yaw 90 and lying yaw 90. Total: 228 private transparent PNGs, 38 six-view sheets and a 28-blank front/side overview. Exact filenames link to blank sheets and stock counterparts; ear labels are filename-reported, not a complete verified edit inventory.

Renderer-observed: the overview and Great Dane blank/stock full sheets were visually reviewed. White/cream shapes remain readable on the neutral gray background. The catalog records qualitative form cues from these views. This is not a full visual anatomy audit or game validation. Other seeds, growth, fatness and motion histories were not sampled.

## Backend and controls

Local stdio MCP, Python 3.12.16 on aarch64, renderer checkout `49c7f62eab51b61b9f68801ba7571178670c433e`. The copied local environment initially contained older installed sources; reinstalled the existing checkout with uv, no dependency changes. All 62 installed Python source hashes match the checkout. No renderer source edits; pre-existing checkout `.gitignore` modification and dangling AGENTS.md link left untouched. No claim about any existing HTTP server's installed code is made.

Recorded packages: petz-renderer-mcp 0.1.0, Pillow 13.0.0, numpy 2.5.4, pefile 2024.8.26, pydantic 2.14.3, fastmcp 4.1.6.

Explicit controls: seed 41, age 100, fatness 50, look adult. Named stock poses and BHD/BDT hashes come from local `list_poses`. Full request/response metadata, source/resource hashes, diagnostics and capabilities remain private in `clean_dogs/reference/`. Seven root resource DLL hashes and 38 breed input hashes are recorded and unchanged after rendering.

Code-supported presentation: the renderer returns individually cropped canvases. Sheets align reported projection offsets in a shared 330×237 native canvas, then use uniform nearest-neighbor 2× zoom. Each sheet is 1980×1050 including labels. Background #a4a9b0. No per-breed size normalization in full sheets. The overview alone crops/fits each silhouette into a thumbnail and cannot support relative-size comparisons. No breed contents or colors were modified.

## Reproduction and verification

From `/workspace` with the recorded local environment and matching assets:

```sh
scratch/petz-local-venv/bin/python tools/render_clean_dogs.py
scratch/petz-local-venv/bin/python tools/check_clean_dogs.py
python3 tools/check_docs.py
```

The [builder](../tools/render_clean_dogs.py) resumes hash-checked frames only with an identical input/runtime/control fingerprint. Archive `clean_dogs/reference/` before changing those inputs. An initial sheet assembly assumed common renderer canvas dimensions and rejected the varying crops; corrected to projection-origin alignment, reusing the verified 228 frames. The successful final build and audit supersede that failed presentation attempt.

The [audit](../tools/check_clean_dogs.py) verifies all 38 inputs, seven resource DLLs, 228 PNG hashes/dimensions/alpha bounds, effective render controls and input identities, 38 sheet hashes, and 228 independently reconstructed sheet tiles. Six fresh local MCP renders reproduce exact PNG hashes: blank/stock Bulldog front, Great Dane side and Poodle three-quarter. No empty renders or clipped placements in the shared canvas. Documentation checks include the catalog and percent-encoded filenames; private breed files and rendered outputs remain excluded from Git.

Private evidence:

- `clean_dogs/reference/manifest.json`: SHA-256 `e1aa9e2c743322ec579dc2ab9daac0e513ced83c089069feeffcfd4fe4eef30c`.
- `scratch/research/clean-dogs-catalog/audit.json`: SHA-256 `db345fa6edb3a3c220327d8cd8c5ba7571648c4f06e0d5b2b644156b2759c5bd`.
- Logs: `scratch/research/clean-dogs-catalog/run.log`, `resume.log`, `final-build.log`, `audit.log`.

## Handoff

Transfer the whole `clean_dogs/` folder, including ignored `petz4/` breed inputs and `reference/` images/metadata, with the documentation. Stock preview sheets are included there; stock binary links additionally need `games/petz4/`. A Git clone alone contains only the index and reproducible tooling. Input game files and renders were not committed. Original-game fidelity remains unverified.

## Repository inclusion — 2026-11-15

At the user’s request, the supplied baseline catalog is now versioned: 28 blank `.dog` inputs, 228 raw PNG views, 38 six-view sheets, the overview and 41 JSON evidence files. This supersedes the earlier ignored/private-only handoff instructions. Original stock binaries and game resources remain excluded; their table links are local-installation references. The catalog JSON records historical local paths and the renderer build above, not credentials. Supplied-file provenance and redistribution licensing remain unverified.

No catalog assets were modified or regenerated. Retained input, image and sheet hashes and all 228 independently reconstructed tiles were checked against the original manifest; the documentation/private-file checks pass with assets staged. This verifies repository packaging of existing evidence, not current-renderer replay or native-game fidelity. The historical manifest and builder are preserved, including its original generated README wording; the current README supplies the revised sharing guidance.

The local commit is ready for upload. GitHub delivery remains pending because this workspace has no HTTPS GitHub credentials, as recorded during texture delivery.
