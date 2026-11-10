# Connector randomness and comparison controls

Scope: renderer revision9d72d7afd5f7460ef18133c6179caaf8055082d9. Direct raster evidence and Petz4 Scottie/Siamese composed-scene samples; native-game state rules remain unvalidated. See [Linez fields](linez.md).

A fixed seed alone does not isolate fuzzy connector pixels when earlier draws change. The renderer retains one RNG plus row-offset tables indexed by clamped fuzz0–7. It reuses existing offsets and generates more only when needed. Whiskers share this RNG; their step0 path consumes a random value, while the tested step1 path does not.

[LINE-007](../experiments/line-007.md) shows identical static blocks repeat without additional table/RNG changes. [LINE-008](../experiments/line-008.md) isolates prior positive-fuzz and whisker draws on a cleared framebuffer. A short same-fuzz prefix matches fresh; inserting another fuzz draw before table extension can change later rows. Different histories need not always produce different pixels.

[LINE-011](../experiments/line-011.md) holds twelve prepared breed scenes fixed: prior-pose scenes change11/12 target renders; whisker0 priming changes12/12. Targetstep1, fixed commands and discarded prior pixels isolate retained LineRenderer state. Same-step1 repeat and whisker1 controls stay equal. Twelve fresh step0 PNGs match local MCP exactly.

[LINE-012](../experiments/line-012.md) attributes the whisker0-priming difference to positive-fuzz connector pixels in12/12 fixtures using research-only state substitutions. The diagnostic connector alone leaves residual changes from existing fuzzy connectors. This is an explanatory intervention, not a proposed renderer patch.

For controlled comparisons, record seed, raster step, prior connector/whisker schedule and whether LineRenderer is fresh or retained. Keep prepared geometry/texture commands fixed to isolate line state; clear or discard prior framebuffers to exclude overdraw. Fresh MCP still comparisons start with fresh state, so they do not independently validate retained animation. Texture FrameState is separate; see [texture state](texture-state.md).

Remaining: actual evolving animation with all retained state, other breeds/versions, other history attribution and independent native evidence. Private states and image hashes are indexed by the experiment manifests.
