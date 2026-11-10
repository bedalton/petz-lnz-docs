# Paint cache matching and state: ten-minute continuation

Date: 2026-11-10. Petz 4 Fuzzkin, integration `6c1d883`. The three available saved pets were already sampled; this continuation uses selective Fuzzkin cache edits and retained state controls. Original files and renderer source remain unchanged. Results concern this renderer build; native-game validation remains open.

| Unit | Finding | Evidence |
| --- | --- | --- |
| [PAINT-008](../experiments/paint-008.md) | Adult supplies color. Young size and direction pair by ordinal within a host when counts match. Dropping one young row preserves that host's adult rows. | Five copies, 216 direct draws, 36 MCP matches, 18 PAINT-007 baseline links. |
| [PAINT-009](../experiments/paint-009.md) | Same-length reorder can misattach distinct retained angles. Actual same-host angles are equal in these histories, so their remap changes nothing. | 120 direct draws, 24 prior state/PNG links, diagnostic angle-only differences in 23/24 views. |
| [PAINT-010](../experiments/paint-010.md) | Exact opposing directions cancel at age 56: surface command skips, non-surface command centers. | Four copies, 32 direct draws, eight MCP matches. All 16 opposed/matched RGBA comparisons equal. |

The [Paint Ballz reference](../format-reference/paint-ball.md) records the editing implications. A color change confined to young was ineffective across the sampled ages. Keep the adult and young row order/count aligned for matching marks. Start with fresh FrameState after an appearance edit; an unchanged vector length does not establish identity. The midpoint test demonstrates a command difference without visible coverage and does not explain why coverage was absent.

## Verification

```sh
scratch/petz-local-venv/bin/python tools/saved_paint_age_matching.py --verify
scratch/petz-local-venv/bin/python tools/paint_state_reordering.py --verify
scratch/petz-local-venv/bin/python tools/paint_direction_midpoint.py --verify
scratch/petz-local-venv/bin/python tools/check_paint_matching_session.py
scratch/petz-local-venv/bin/python tools/check_docs.py
```

All three complete unit replays and the [aggregate audit](../tools/check_paint_matching_session.py) pass. The session totals 368 direct draws and 44 fresh local stdio MCP renders. The aggregate independently checks 412 PNG hashes, 44 MCP metadata records (input hashes, age and camera controls), nine private copies, 21 original-file hashes, 304 decoded RGBA comparisons, 42 prior PNG links, and 24 prior state-file hashes. All 62 installed sources agree with the checkout; four tool hashes, engine/dependency versions and unit replay logs are recorded.

Seven private sheets were reviewed at native resolution: PAINT-008 standing front/side at ages 0 and 50, PAINT-009's largest diagnostic angle difference, and both PAINT-010 midpoint views. PAINT-008 sheet order is baseline, young color, adult color, young size, young size with a row dropped, young reorder. PAINT-009 shows stale versus remapped test angles. PAINT-010 shows matched/opposed surface, then matched/opposed non-surface. These sheets are separate from the 412 research PNGs.

Private evidence: `scratch/research/paint-{008,009,010}`, `scratch/research/paint-matching-review`, `scratch/research/paint-matching-session-verification.json` and `scratch/paint-{008,009,010}-verify.log`. Saved-file probes preserve bytes outside edited caches; native stream checksums remain unvalidated.

Local HTTP MCP discovery and capabilities pass, and a separate Fuzzkin standing/front render matches the prior health control. Research uses stdio; this health call is outside research totals. The prior HTTP process remained active. The renderer checkout retains only its pre-existing `.gitignore` edit; unrelated untracked `istall-node` remains untouched.

Next: additional hosts, ages and textured pets when available; other versions through controlled breed copies; or independent native evidence. Near-opposite directions and the lack of visible midpoint coverage remain open. The requested ten-minute continuation ends with this audit.
