# LINE-001: connected added detail and omissions

Date: 2026-11-09. Renderer-observed Petz 4 Scottie/Siamese; no native-game validation.

## Method

Run `scratch/petz-local-venv/bin/python tools/connected_detail_probe.py`. Refuses existing output directory. Appends a diagnostic marker and optionally a head-to-marker Linez row. Preserves effective seed-0 Linez rows, including inherited rows, by materializing them in the adult copy. Fixed-span safeguards check unrelated payloads/metadata and source preservation. The marker is ID 90 in these two files; compute rather than reuse it for another breed.

Six variants per species: marker, connected, each with marker omission or head omission. Numerical loads cover standing/sitting/lying. Twelve local stdio MCP standing comparisons cover front/side, seed 0, age 100, fatness 50. [Manifest](line-001.json) records rows, parsed line counts, visibility, hashes and controls. Runtime/engine hashes: [RESTORE-002](restore-002.json); renderer 9d72d7afd5f7460ef18133c6179caaf8055082d9. Private files under scratch/research/line-001.

## Results

All eighteen species/pose/pair geometry checks pass: adding the connector changes no ball geometry. Unomitted connected variants have exactly one more parsed line. Marker omission removes that extra line while retaining the marker definition and radius; head omission also removes the connector but leaves the added marker visible. These are independent visibility flags, not a recursive hide tree.

Four unomitted image pairs differ; all eight omitted-endpoint pairs equal their corresponding controls without the extra connector. Four sheets visually reviewed: Dogz connected front, Catz connected side, Dogz marker omission front, Catz head omission side. The connector is a filled taper rather than a thin stroke in the tested 100/100 endpoint-width configuration; the front Dogz sheet shows a broad wedge. This is a diagnostic style, not a recommended finished ornament.

Counts in standing (also recorded for other poses): Dogz 70→71 unomitted, 70→70 marker-omitted, 66→66 head-omitted. Catz 51→52, 51→51 and 50→50 respectively. Head omission removes other existing incident lines too, so compare within each omission state.

## Limits

Only one line joining a base head to an added marker, two breeds, one rendered pose/two views. Other widths/colors/edge modes/draw order and chains of added parents remain untested. Materializing inherited rows does not test Linez inheritance. No native semantics or cross-version connector validation; no renderer changes.
