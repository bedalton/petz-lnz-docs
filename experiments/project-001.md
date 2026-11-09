# PROJECT-001: synthetic projection semantics

Date: 2026-11-09. Code-supported through direct execution; no MCP, images, stock assets or native game. Renderer revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, package 0.1.0, Python 3.12.16.

Run `scratch/petz-local-venv/bin/python tools/projection_probe.py`. Eleven assertions passed; [manifest](project-001.json) records source hashes, controls, rows and numerical outputs. The three-ball frame uses species 0 and zero rotations, bypassing species shape transformations. This isolates implementation arithmetic rather than an actual breed pipeline.

The parser in appearance/core.py reads the first three leading integers into Projection(start, end, percent), skipping rows with fewer than three. rendering/positions.py applies projections after moves and in row order. The observed operation is end = start + trunc((end - start) * percent / 100), componentwise with signed 16-bit wrapping. Parser behavior and wrapping are code inspection findings, not separately exercised by this probe.

For start x=0 and end x=10, percentages 0/50/100/150/-50 yield 0/5/10/15/-5. Two 50-percent rows yield 2 after truncation. With x coordinates 0,10,20, rows (0,1,50) then (1,2,50) yield 0,5,12; reversing them yields 0,5,15. Moving start to 2 before projecting end yields end 6. Self projection preserves coordinates; negative/out-of-frame indices are ignored in these cases.

Limits: no species anatomy, added-ball targeting, age blending, LNZ parser execution, camera behavior or game fidelity is established. Full rendering and another breed per species remain pending resource restoration. [MOVE-001](move-001.md) contains earlier asset-backed downstream observations.
