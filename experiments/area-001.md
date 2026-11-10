# AREA-001: connections can change body area

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-09. Petz 4 Scottie/Siamese renderer evidence. Direct head-rotation geometry is separate from default-head-pose MCP images. Native-game behavior unvalidated.

Run `scratch/petz-local-venv/bin/python tools/body_area_probe.py`. Refuses overwrite. Appends a group-0 head-attached marker and optionally connects it to head or base ID 0 (stock label ankle). Variants use body-area column 0, explicit 8 or explicit 1; ankle/marker omission controls remove the connection. Effective existing Linez preserved; source-copy safeguards applied.

The initial harness assumed Catz ID 0 used built-in area 2. Its effective Siamese area is 3, as is Scottie's. Failed partial copies remain at scratch/research/area-001-assumption-failed. Corrected the assumption and checked resolved areas before testing. No renderer code change.

Forty-two numerical variant/pose checks span standing/sitting/lying, seed 0, age 100, fatness 50. Expected marker areas all match: no link/head link → 8; ankle link with column 0 or explicit 8 → 3; explicit 1 stays 1; omitted ankle restores 8; omitted marker yields 0. Thus explicit 8 is still eligible for the renderer's connection-based area reassignment; it is not a fixed-area override in this case.

Direct posed_geometry head_rotation=32 changes marker coordinates only in area-8 variants among these controls. Neutral geometry with area 3 versus area 1 can look identical despite different classifications. Eight standing MCP comparison pairs at yaw 0/90 confirm equal pixels for ankle-link versus explicit8 and explicit1 variants. MCP calls do not request head rotation. Two explicit1 sheets reviewed (Dogz front, Catz side); both show identical pair members. Other sheets checked by hashes.

[Manifest](area-001.json) contains row settings, resolved areas, neutral/rotated geometry and hashes. Runtime/engine provenance: [RESTORE-002](restore-002.json), renderer 9d72d7afd5f7460ef18133c6179caaf8055082d9. Private evidence under scratch/research/area-001.

One marker/neighbor/two breeds; no native area names beyond stock labels, all-neighbor precedence, multiple links, explicit body-area-list edits, growth/morph coupling or cross-version checks. Built-in species tables alone cannot predict effective breed areas.
