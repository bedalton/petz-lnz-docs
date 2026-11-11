# UPDATE-008: puppy/kitten MCP reload

2026-11-11. [Manifest](update-008.json). Renderer-observed and filesystem evidence; no game validation.

Reinstalled the updated local checkout at `4c4d3df` into `scratch/petz-local-x86-venv` using uv with workspace cache/tmp directories, without changing dependencies. Package display version remains0.1.0; the revision and source manifest identify this build. All installed Python sources match checkout. Renderer AGENTS.md/CLAUDE.md remain dangling symlinks; no renderer source modifications were made. Pre-existing renderer .gitignore modification and unrelated istall-node remain untouched.

Stopped old HTTP PID15068 and started a fresh Petz4 server at `http://127.0.0.1:8765/mcp`, managed process session58703. A fresh FastMCP HTTP client rediscovered all six tools, confirmed the render `look` schema, inspected Scottie/Siamese and successfully rendered each in adult, puppy/kitten and age modes. Controls: age6, standing, yaw0, seed41, fatness50. All six PNG hashes differ. This verifies updated rendering paths respond; it does not establish visual correctness or game fidelity. Petz3/5 and saved pets were not exercised in this unit. Historical research used the previous build and retains its original provenance; no wholesale revalidation is claimed.

All21 recorded original game hashes still match. Private reproducer, wire schemas, capabilities, dependency/source versions, inspection/render metadata and raw PNGs stay under ignored `scratch/research/update-005`; run its `check.py` with the active environment against the server to repeat. It overwrites this unit’s private outputs. Public manifest records the original run hashes.

The local container HTTP server is reloaded and fresh clients receive its new schema. The separately hosted chat MCP endpoint is independent; no hosted deployment or chat registry reload is claimed.
