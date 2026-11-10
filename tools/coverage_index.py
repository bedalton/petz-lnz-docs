"""Build a compact section ledger from the sampled derived inventory."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'experiments/anatomy-001.json').read_text())
names={k for r in rows for field in ('breed_sections','master_sections') for k in r[field]}
names.add('Draw Linez Before Ballz')
names.update(('Ball Size Override','Outline Color Override','Fuzz Override','Add Ball Override'))
known={
 'Default Linez Thickness':'25/100, empty fallback and explicit-row precedence: [LINE-004](../experiments/line-004.md)',
 'Draw Linez Before Ballz':'Global 0/1 fallback and row overrides: [LINE-003](../experiments/line-003.md)',
 'Linez':'Base-to-added connector and endpoint omissions: [LINE-001](../experiments/line-001.md); [fields](../format-reference/linez.md); endpoint widths: [LINE-002](../experiments/line-002.md); draw-order fallback/override: [LINE-003](../experiments/line-003.md); short-row/default-thickness controls: [LINE-004](../experiments/line-004.md); other styling pending',
 'Add Ball':'Synthetic attachment, ordinary/relative sizing: [ADD-001](../experiments/add-001.md); connected detail/omissions: [LINE-001](../experiments/line-001.md); default add-group behavior: [MORPH-001](../experiments/morph-001.md); body-area propagation: [AREA-001](../experiments/area-001.md); conflicting-neighbor precedence: [AREA-002](../experiments/area-002.md); body-area lists and format-version gate: [AREA-003](../experiments/area-003.md); chain ID-order propagation: [AREA-004](../experiments/area-004.md); anchored cycles and late lists: [AREA-005](../experiments/area-005.md); remaining fields need tests',
 'Omissions':'All 67 base IDs front/side sampled: [OMIT-001](../experiments/omit-001.md); [VIS-001](../experiments/vis-001.md) separates zero-radius cases; iris/native/morph cases pending',
 'Head Enlargement':'Tested size/spacing and A=100 gate: [HEAD-001](../experiments/head-001.md), [HEAD-002](../experiments/head-002.md)',
 'Outline Color Override':'Iris-ring perturbation: [EYE-001](../experiments/eye-001.md)',
 'Move':'Tested reference/default/zero/repeated rows: [MOVE-001](../experiments/move-001.md); native anchoring unresolved',
 'Key Balls':'Master IDs inventoried; section replacement tested: [INHERIT-001](../experiments/inherit-001.md)',
 'Ball Size Override':'Head-only perturbation: [BALL-001](../experiments/ball-001.md)',
 'Color Info Override':'Head-only perturbation: [BALL-001](../experiments/ball-001.md)',
 'Ballz Info':'67 labels per species inventoried; complete column/visual coverage pending: [ANATOMY-001](../experiments/anatomy-001.md)',
 'Eyes':'Colors: [EYE-001](../experiments/eye-001.md); right iris/host omissions: [EYE-002](../experiments/eye-002.md); shape/clip controls pending',
 'Project Ball':'[Field reference](../format-reference/project-ball.md); synthetic arithmetic/order: [PROJECT-001](../experiments/project-001.md); Head/nose controls: [PROJECT-002](../experiments/project-002.md), [cross-version PROJECT-003](../experiments/project-003.md); [second breeds PROJECT-004](../experiments/project-004.md); other targets pending',
 'Default Linez File':'Selected master recorded in provenance; selection/recursion test pending',
}
lines=['# Research coverage ledger','','This is a lower-bound topic inventory, not a complete LNZ specification. It combines six sampled adult breed/master resources with override sections already encountered in code/experiments. More stock breeds, young resources and community references may add topics.','','Most controlled editing results concern Petz 4 Scottie/Siamese; PROJECT-003 also samples Project Ball edits in Petz 3 and 5. No topic has native-game validation. Ball-label agreement across versions is asset evidence only.','','| Topic | Current evidence / remaining work |','| --- | --- |']
lines += [f'| {name} | {known.get(name,"Inventoried or implementation lead only; dedicated reference/experiment pending")} |' for name in sorted(names)]
lines += ['','## Species/version matrix','','| Evidence | Dogz 3 | Catz 3 | Dogz 4 | Catz 4 | Dogz 5 | Catz 5 |','| --- | --- | --- | --- | --- | --- | --- |','| Stock render smoke | Passed | Passed | Passed | Passed | Passed | Passed |','| Stock label/key inventory | Sampled | Sampled | Sampled | Sampled | Sampled | Sampled |','| Controlled edits | Projection only | Projection only | Sampled | Sampled | Projection only | Projection only |','| Base omission sweep (two views) | Pending | Pending | Sampled | Sampled | Pending | Pending |','| Complete per-ball visual map | Pending | Pending | Pending | Pending | Pending | Pending |','| Native-game validation | Pending | Pending | Pending | Pending | Pending | Pending |','','## Next priorities','','1. Seek native iris omission evidence after EYE-002; tongue-out validation deferred (user reports provided MCP animations lack it, VIS-002).','2. Expand eye recipe beyond two stock breeds and front-view color tests.','3. Expand connectors, body areas and morph groups beyond MORPH-001 ordinary sizing.','4. Another breed per species; broaden edited cross-version checks beyond PROJECT-003 projections.','5. Further shape/color/texture/marking sections, growth/variation and design examples.','','Generated by tools/coverage_index.py from derived inventory and explicit evidence links. Update the generator when promoting topic coverage.']
(ROOT/'docs/coverage.md').write_text('\n'.join(lines)+'\n')
