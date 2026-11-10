# Connector texture research: 2026-11-10

Third ten-minute connector continuation. Four research units, no renderer modifications and no native-game validation.

| Unit | Question | Evidence |
| --- | --- | --- |
| [LINE-013](../experiments/line-013.md) | Does selected endpoint texture affect breed connector pixels? | 30 numerical loads,16 local MCP pairs |
| [LINE-014](../experiments/line-014.md) | How are texture windows cropped or rejected? | 72 asset-free rasters,120 exact samples |
| [LINE-015](../experiments/line-015.md) | Does size rejection occur in composed breeds? | 36 numerical loads,16 local MCP pairs |
| [LINE-016](../experiments/line-016.md) | Do selected routing controls match Petz3/5? | 60 numerical loads,32 local MCP pairs |

Totals:126 numerical breed loads,64 local MCP pairs,72 synthetic indexed buffers and120 exact texture samples. Six sheets visually reviewed, two for each MCP unit. Scope is Scottie/Siamese; texture routing additionally sampled in Petz3/5, whereas composed size rejection remains Petz4 only.

Equal endpoint base colors isolate texture from fill selection. Negative fill choosing the textured head differs from explicit125; selecting an untextured marker matches explicit125. All32 Petz3/5 comparison PNGs and their cell hashes match corresponding Petz4 controls. This does not imply general version fidelity.

Synthetic raster boxes larger than their tile are rejected, without advancing fuzz RNG. Periods do not rescue oversize windows. Long offset -800 breed controls reproduce the effect with stock256x256 textures: textured equals no-line; explicit fill still draws. The line remains parsed and builds a block, so this is a raster-path limitation. Native behavior remains unknown.

## Integrity and reproducibility

`tools/check_line_texture_session.py` verifies42 unique private copies,64 MCP PNG pairs,128 cropped RGBA cell hashes,126 numerical-load records,72 full synthetic indexed buffers and120 exact sample values. It also verifies public/private report agreement, installed/checkout source hashes, dependencies, resource DLLs and original breeds for each version. All pass. Private summary scratch/research/line-texture-session-verification.json.

LINE-016 records its Petz4 baseline manifest hash. Version flags are explicit in ResourceResolver and the MCP CLI; metadata reports the intended game versions despite the generic service display name. Failed initial harness runs are archived privately and excluded from counts. Raw textures, breed copies and renders remain ignored.

See [focused texture reference](../format-reference/connector-textures.md), [field reference](../format-reference/linez.md) and [coverage](coverage.md). Next: other breeds/tile dimensions, threshold/diagonal controls, retained evolving scenes or independent native evidence. Existing texture-drift and iris-omission gaps remain open.

Final local HTTP MCP discovery/get_capabilities pass; private health record scratch/research/line-texture-session-mcp-health.json. Actual experiment comparisons used version-specific local stdio processes.

Final provenance audit: renderer checkout is clean, all session commits use the required author/committer without co-author trailers, and the only unrelated worktree item remains untracked istall-node. Handoff resume guidance now reflects the current timed request rather than an older context-based continuation note.

Complete source audit: all62 installed Python sources match checkout9d72d7afd5f7460ef18133c6179caaf8055082d9. Sorted source-hash map digest `e1cd30b0543fcd99d18ed9252a7c44de2a31a4decbcd482266df6af755681374`; private manifest scratch/research/line-texture-session-source-audit.json. The session verifier now checks this full map as well as per-experiment source records.
