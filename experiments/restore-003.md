# RESTORE-003: copied workspace recovery

2026-11-11. [Manifest](restore-003.json). Filesystem/hash and renderer-observed evidence only; no game validation.

`python3 tools/check_game_restore.py` verifies all 21 recorded original inputs: twelve engine/executable files, six Scottie/Siamese breeds across Petz3/4/5, and Fuzzkin/Homebody/Goobe Petz4 saves. All match historical hashes. Current folders contain 818/1573/1734 files respectively (including metadata). No game files were moved, overwritten or fabricated. These checks cover known research inputs, not every file of a complete installation; no complete original installation manifest is available. The old separate petz-engines folder is absent, but the required resources are present in each version's installation.

Copied Python binaries target aarch64 and fail on this x86_64 host. Preserved those files and installed CPython3.12.16 under scratch/python-x86, with a fresh environment at scratch/petz-local-x86-venv. All caches/evidence are under scratch. Installed the copied renderer with requirements.txt constraints; all62 installed Python sources match checkout revision6c1d883. This is the same revision recorded in UPDATE-001; no newer local revision was found. Dependencies are recorded privately; cross-platform runtime equivalence is not assumed. Renderer AGENTS.md/CLAUDE.md symlinks point to an absent external agentic directory; no renderer files were modified.

Six fresh stdio inspection/render pairs pass using tools/local_smoke.py with OUT redirected to scratch/research/restore-003 (historical evidence preserved). Controls: standing,yaw0,seed0,age100,fatness50. Input/PNG hashes are in the manifest. Matching repeatability does not establish game fidelity.

Started the local HTTP MCP using:

```sh
scratch/petz-local-x86-venv/bin/python -I -m petz_renderer.service.local_mcp --game-root /workspace/games/petz4 --transport http --port 8765
```

Endpoint http://127.0.0.1:8765/mcp advertises all six tools. A real HTTP client successfully calls capabilities and renders Scottie with the same fixed controls/hash as the stdio check. Managed process session6836; recheck after container/session restarts. Client-side reconnect may still be needed to refresh cached metadata; this work does not reload the separately hosted MCP app.

Raw capabilities, source/dependency lists, HTTP check, PNGs and reports remain ignored at scratch/research/restore-003. Prior copied ARM environment remains preserved; use the new x86 environment for this host.
