# Connector styling research: 2026-11-10

Ten-minute continuation requested by the user. Five research units; renderer unchanged. These are code-supported and local-renderer observations, not native-game validation.

| Unit | Focus | Direct checks | MCP pairs |
| --- | --- | --- | --- |
| [LINE-005](../experiments/line-005.md) | Fill/endpoint selection and synthetic texture routing | 72 blocks +36 breed loads | 20 |
| [LINE-006](../experiments/line-006.md) | Edge colors and modes | 48 rasters +42 breed loads | 20 |
| [LINE-007](../experiments/line-007.md) | Fuzz bounds and repeated draws | 40 rasters +30 breed loads | 16 |
| [LINE-008](../experiments/line-008.md) | Shared fuzz/whisker RNG history | 96 history rasters | 0 |
| [LINE-009](../experiments/line-009.md) | Automatic edge mode | 48 breed loads | 20 |

Totals:76 local stdio MCP pairs,156 numerical breed loads,72 synthetic blocks and184 isolated/history rasters. Eight sheets visually reviewed, two for each MCP unit. Stock breed scope is Petz4 Scottie/Siamese, fixed seed0/age100/fatness50; standing front/side MCP controls, three numerical poses. Synthetic histories use fresh line seed1 and clear prior pixels.

Fill -1 follows the start endpoint; -2 follows the end. Negative edge colors inherit shaded fill while explicit edges bypass fill shading. Mode0 uses scan-row boundaries, mode1 polygon-side strokes, -1 no special edges. Fuzz clamps0–7 and cached rows share RNG with whiskers. Automatic edge sentinel -2 selects -1 only for exact edge colors -1/-1. Flat inherited edges can hide resolved-mode differences in pixels.

## Integrity and provenance

`tools/check_line_session.py` verifies52 private copies,76 PNGs,152 cropped RGBA cell hashes,192 full RNG/table states, public/private report agreement, installed/checkout sources, dependencies, three resource DLL hashes and original breed hashes. All pass; private summary scratch/research/line-session-verification.json. Local HTTP MCP discovery/get_capabilities also pass; scratch/research/line-session-mcp-health.json. All actual experiment images used the local stdio MCP backend.

Each unit records corrections and scope; initial failed harness folders are preserved privately and excluded from counts. No proprietary assets or raw images are tracked. [Linez reference](../format-reference/linez.md) and [coverage ledger](coverage.md) index the findings.

Next: partial3–9-field rows/omitted edge columns, actual composed fuzzy-breed history, textured connector examples, other breeds/versions or independent native evidence. Existing texture and iris fidelity gaps remain open.
