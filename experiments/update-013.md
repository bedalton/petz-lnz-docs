# UPDATE-013: reinstall and reload corrected poses

## Completed after source restoration

The user restored the full checkout at `20cd029`; reinstall and local reload now pass. Installed into `scratch/petz-local-x86-venv` using `UV_CACHE_DIR=/workspace/scratch/uv-cache-x86 TMPDIR=/workspace/scratch/tmp uv pip install --python /workspace/scratch/petz-local-x86-venv/bin/python --reinstall --no-deps /workspace/petz-renderer-mcp`. Package display version remains0.1.0; revision and source hashes identify the build. All62 installed Python sources match checkout; `rendering/presets.py` is the only changed Python source relative to preflight. No dependencies or renderer sources were edited. The restored checkout's AGENTS.md/CLAUDE.md links are dangling; the readable instructions from the previously supplied documentation were already inspected. Existing .gitignore modification and untracked uv.lock remain untouched.

Setup check passes. Local HTTP MCP now serves `http://127.0.0.1:8765/mcp`, PID1543, managed session9456. No prior server was running. Startup command:

```bash
/workspace/scratch/petz-local-x86-venv/bin/python -I -m petz_renderer.service.local_mcp \
  --game-root /workspace/games/petz4 \
  --asset-root /workspace/scratch/screenshots \
  --asset-root /workspace/scratch/research/young-002 \
  --asset-root /workspace/scratch/research/custom-001 --transport http --port 8765
```

Fresh HTTP discovery returns six tools; capabilities, list_poses and both breed inspections pass. Twelve named/raw/direct triples pass exactly: Scottie/Siamese × standing/sitting/lying × front/side, requested seed41/age100/fatness50. This includes24 live HTTP rendering calls and12 fresh direct portraits. Named lying metadata confirms DOG79/29 and CAT263/24, with catalogue petz4-stock-v3. All21 recorded original game-file hashes match. Reproduce service/install checks with `scratch/petz-local-x86-venv/bin/python tools/check_renderer_pose_reload.py` while the server is running. This script updates private report/images; the public compact [manifest](update-013.json) records the completed run.

Private install log, schemas, capabilities, pose metadata, PNGs and full report remain at `scratch/research/update-013/`. Only documentation, hashes and the check script are committed. This verifies the local package/service; no hosted endpoint or external client's cached discovery was refreshed. Historical experiment pixels, including CUSTOM-001 lying views, retain their original build scope and were not broadly replayed. Original-game fidelity remains unvalidated.

## Initial preflight (superseded)

2026-11-15. User requested reinstall/reload of the updated renderer. The supplied `/workspace/petz-renderer-mcp` directory currently contains AGENTS.md, HANDOFF.md, PLAN.md, notes, journals and archives, but no `src/`, `pyproject.toml` or renderer `.git` checkout. Searching the workspace found only older installed/cache packages, not updated installable source. The renderer briefing reports source20cd029 (corrected DOG79/29, CAT263/24 lying presets), but these notes are not an installable distribution.

The existing `scratch/petz-local-x86-venv` still contains62 Python sources and the historical lying choices DOG84/9 and CAT311/0. Port8765 has no listener. No reinstall or reload has been performed; no source has been reconstructed from prose. All21 recorded original game-file hashes match. The user has been asked to restore the full checkout or supply its repository URL/alternate workspace path.

Private evidence: `scratch/research/update-013/preflight.json`, SHA256 `771e6c0ee9a03099c6c3652dbc761f7653c61e07a3952379d3b19f4bf3965ebd`. It records directory entries/missing paths, installed source hashes and exact pose records, listener probe and original hash audit. No renderer/game files were modified. This is a pending installation request, not completed update validation. Once source is available, read its instructions, install into the existing x86 environment with workspace cache/tmp paths, restart the local HTTP MCP with appropriate asset roots, then check fresh discovery/capabilities and actual named/raw dog/cat renders.
