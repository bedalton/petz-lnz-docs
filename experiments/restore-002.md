# RESTORE-002: local MCP restored

Date: 2026-11-09. Renderer-observed setup/smoke evidence, not game validation.

User supplied games/ with full installations nested at games/games/petz3, petz4 and petz5. Moved those directories to games/petz3, games/petz4 and games/petz5 without changing file contents. Left the separate games/petz-engines directory in place. All game files remain ignored.

Installed local launcher check for /workspace/games/petz4 reports ready, six tools, local_forms and memory limits enabled. Started the Petz 4 server with:

```sh
scratch/petz-local-venv/bin/python -I -m petz_renderer.service.local_mcp --game-root /workspace/games/petz4 --transport http --port 8765
```

Connected a real FastMCP HTTP client to http://127.0.0.1:8765/mcp; listed all six tools and successfully called get_capabilities. This loopback process is running for the current container session; it is not an automatic startup service. Research scripts can also launch independent stdio servers.

Reran tools/local_smoke.py through runpy with OUT redirected to scratch/research/restore-002, preserving the historical experiment manifest. All six real stdio inspect/render pairs passed for Scottie/Siamese across Petz 3/4/5. Controls: standing, yaw 0, seed 0, age 100, fatness 50. Every input/PNG hash and report record matches SMOKE-001. This confirms the sampled outputs, not full runtime equivalence or game fidelity. No new visual review.

[Manifest](restore-002.json) records revision, Python, shared-engine hashes, controls and output hashes. Dependencies, capabilities, full render/inspection responses and PNGs remain private under scratch/research/restore-002. Prior private experimental copies/checkpoints are still absent. Renderer source unchanged. [Previous recovery blocker](restore-001.md) is resolved.
