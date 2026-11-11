# Renderer evidence gaps

A successful PNG is not a certificate of original-game correctness. Retain complete diagnostics and exact engine/input hashes for reproduction.

## Known incomplete features: do not infer from MCP

**Update:** [UPDATE-001](../experiments/update-001.md) reinstalls/restarts integration6c1d883 and confirms changed renderer paths. The blanket textured paint/Outline restrictions below are **historical and withdrawn for that build**. Clothing remains unsupported. Sampled new renderer support does not establish native-game appearance. The original report is preserved below for provenance.

On 2026-11-10 the user relayed this answer from the Petz4 porting agent when asked whether the renderer was complete:

> So a stock breed with no clothes should look almost entirely right. The visible gaps are clothing, textured paint balls and textured Outline balls

This is a **source-reported limitation**, relayed by the user; the originating conversation, exact renderer build and independent native comparisons were not supplied. At the time, these features were recorded as incomplete:

- Clothing.
- Textured paint balls.
- Textured Outline balls (the source's terminology).

**Do not infer their game appearance, behavior or authoring rules from MCP output.** A successful render, missing effect, partial effect or pixel match cannot validate these features. Use independent game evidence or an independently validated implementation before making claims about them. Keep renderer-only observations explicitly scoped as such.

The stock-breed assessment is also source-reported, not a project-wide fidelity guarantee. Existing ordinary ball/connector texture and flat outline-color experiments do not establish support for textured paint balls or textured Outline balls. This report concerns the Petz4 renderer; applicability to other versions and later fixes remains unverified. The linked update supplies implementation/control evidence for lifting the blanket textured paint/Outline restriction; game fidelity remains open.

## Other evidence gaps

| ID | Topic | Established observation | Missing evidence / next action |
| --- | --- | --- | --- |
| GAP-001 | Move anchoring | [MOVE-001](../experiments/move-001.md): fifth column rotates offsets; zero offsets are no-ops in tested frames | Community tutorial describes anchoring. Need native evidence or an independently traced algorithm before choosing a renderer repair. |
| GAP-002 | Diagnostic coverage | [SMOKE-001](../experiments/smoke-001.md) retains notices and warnings even for successful stock renders | Classify each diagnostic code/message by section before treating it as unsupported behavior. |
| GAP-004 | Iris omission | [OMIT-001](../experiments/omit-001.md): omitting iris IDs leaves front/side images unchanged, while EYE-001 color edits affect them; [EYE-002](../experiments/eye-002.md) finds host-only equals host-plus-iris and differs from control | [UPDATE-002](../experiments/update-002.md) confirms the omission relationship on the new build; host-eye overlay path bypasses a separate iris visibility gate; native behavior and intended authoring practice require validation. |
| GAP-005 | Relative-size morphs | [MORPH-002](../experiments/morph-002.md): grouped relative-size20 stays evaluated size0, full activation equals static relative-size0 instead of size20; [MORPH-006](../experiments/morph-006.md) revalidates current build and sampled Petz3/5 | Need native evidence or independent algorithm provenance before deciding whether this implementation distinction warrants repair. |
| GAP-006 | Retained texture orientation | [TEXTURE-001](../experiments/texture-001.md) historically changes121 pixels at frame3; [UPDATE-002](../experiments/update-002.md) confirms host-orientation attribution but corrects the updated count to128 (141 at frame8) | [TEXTURE-002](../experiments/texture-002.md) traces the repeated(0,-1) delta to quantized matrix self-product/rounding. Independent native arithmetic evidence is still needed before judging or repairing behavior. |
| GAP-007 | Incomplete rendering features | Earlier blanket paint/Outline limitation withdrawn for6c1d883: [UPDATE-001](../experiments/update-001.md). Clothing remains unsupported | New texture paths have differential renderer controls; native-game fidelity and remaining paths stay open. |
| GAP-003 | Original-game fidelity | Repeated/controlled inputs produce measurable renderer results | No controlled native captures or independent geometry oracle validated by this research project yet. |

When a feature is unresolved, document the limitation beside its recipe. Use other research topics while collecting evidence; repair confirmed renderer defects with a reproducer and regression tests. Do not make a speculative change solely to match an ambiguous tutorial.
