# SMOKE-001: local MCP baseline

Date: 2026-11-08. Evidence status: renderer-observed, not game-validated.

All six inspection/render pairs succeeded over real stdio MCP: Scottie and Siamese in Petz 3, 4 and 5. Dog outputs were 91×131; cat outputs were 71×149. Controls: standing, yaw 0°, seed 0, adult age 100, fatness 50. This is one pose and two stock breeds, not comprehensive feature acceptance.

## Reproduce

From /workspace:

```sh
UV_CACHE_DIR=/workspace/scratch/uv-cache UV_PYTHON_INSTALL_DIR=/workspace/scratch/python uv venv --python 3.12 scratch/petz-local-venv
UV_CACHE_DIR=/workspace/scratch/uv-cache uv pip install --link-mode copy --python scratch/petz-local-venv/bin/python -c petz-renderer-mcp/requirements.txt ./petz-renderer-mcp
scratch/petz-local-venv/bin/python tools/local_smoke.py
```

Python: CPython 3.12.16. Renderer checkout: 9d72d7afd5f7460ef18133c6179caaf8055082d9; pre-existing .gitignore modification left untouched. Installed noneditable from the checkout, package version 0.1.0. The external checkout remains separate and ignored by the documentation repository. No renderer source changes were made.

Default uv installation failed with a permission error while installing a cached wheel. Retrying with `--link-mode copy --reinstall` succeeded. Use copy mode on this mount.

Private PNGs, full render provenance, inspection output and capabilities are under scratch/research/smoke-001. The tracked smoke-001.json contains controls and input/output hashes only. The script overwrites this baseline directory on rerun; preserve a copy before rerunning if investigating changes.

## Limits and next questions

Diagnostics include unsupported-section notices and other warnings; retain their full code/message rather than interpreting every diagnostic as unsupported behavior. No images have yet been visually reviewed, and repeatability has not yet been tested by a second run. Equal dimensions or pixel hashes across versions do not prove equivalent engines or full compatibility.

Next: inspect master and breed sections, establish a copy-only edit workflow, then test one ball's size, position and color independently. Compare both appearance geometry and aligned renders.
