# Project instructions

- Keep all environments, caches, notes, evidence and memories under `/workspace`; other container paths may disappear.
- Read STATUS.md and HANDOFF.md before work. Update both after every logical unit, linking detailed evidence rather than duplicating it.
- Commit every logical unit. Use conventional commits; target titles under 50 characters and never exceed 65.
- Set Git author and committer to bedalton <3941960+bedalton@users.noreply.github.com>.
- Never include agent co-authors or any other co-authors or Co-authored-by trailers.
- Preserve original game files. Edit copies only. Never commit proprietary game files, extracted stock LNZ, raw renders, environments or credentials.
- User-authorized exception: include the supplied `texture-index/*.bmp` and `texture-index/*.png` catalog assets (including contact sheets) in Git so users can obtain them with the repository. Keep editor `.import` sidecars excluded; this exception does not cover other game files or raw renders.
- User-authorized exception: version the supplied `clean_dogs/petz4/*.dog` blanks and `clean_dogs/reference/` catalog images and JSON evidence so the referenced baseline catalog is usable from a clone. Do not include original stock binaries from `games/` or unrelated renders.
- Prefer local petz-render MCP; use hosted rendering when needed. Record backend, versions, hashes and controls.
- Distinguish source-reported, code-supported, renderer-observed and game-validated claims. Repeatability does not establish game fidelity.
- Keep reference pages focused and indexed. Link claims to reproducible evidence and explicitly record uncertainty and species/version applicability.
- Follow applicable instructions within the renderer checkout before modifying it. Renderer fixes require reproducers and appropriate regression checks.
