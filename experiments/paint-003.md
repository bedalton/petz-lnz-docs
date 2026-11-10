# PAINT-003: paint-state vector length and indices

Date: 2026-11-10. [Manifest](paint-003.json). Fuzzkin/Petz4 integration6c1d883. Direct API controls using all24 nonzero-state motion targets from [PAINT-001](paint-001.md). No original saved-pet data is edited.

**Code-supported and renderer-observed:** `prepare_frame` uses retained paint angles only when their vector length equals `len(appearance.paint_balls)`. Otherwise it starts a zero vector for the entire paint list. The sampled Fuzzkin has19 paint entries,with nonzero pre-target angles at indices16/17/18. Both18-entry and20-entry supplied vectors discard retained paint angles;all48 mismatch controls match host-only pixels exactly. These vectors pass FrameState pair/type validation;the reset happens during preparation rather than as an input error.

A correctly sized19-entry zero vector also matches host-only. A19-entry vector retaining just the three active pairs matches combined texture in24/24;changing only inactive entry0 to(47,-23) also leaves combined pixels unchanged in24/24. That entry's inactivity is specific to these sampled prepared scenes;it is not a general unused-index guarantee. Correct-length zero pairs are processed alongside host frame-angle deltas,so the prepared active angles need not remain zero.

Each case saves seven draws:host-only,combined,short,long,exact zero,active-only,and altered inactive slot. All168 PNGs and48 prior host/combined pixel links verify. Fresh baseline MCP evidence is inherited from PAINT-001;this unit makes no new MCP calls. No game/native claims are made.

Reproduce with `scratch/petz-local-venv/bin/python tools/paint_state_shape.py` into a fresh scratch/research/paint-003 directory. Verify with `scratch/petz-local-venv/bin/python tools/check_paint_state_shape.py`,which repeats the histories/interventions and checks exact PNG bytes,parsed controls/vector lengths/active angles,original input/engine hashes,dependencies and62 installed/checkout sources. Renderer and original files are unchanged.

For direct retained-state experiments,persist the full draw-returned FrameState against the same appearance/paint-list ordering. A length mismatch is insufficient as an invalidation strategy when paint entries are reordered without changing count;that scenario is not tested here. This API contract does not describe original-game storage or behavior.
