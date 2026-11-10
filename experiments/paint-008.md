# PAINT-008: adult and young paint cache matching

Date: 2026-11-10. Petz 4 Fuzzkin, integration `6c1d883`. [Manifest](paint-008.json), [reproducer/verifier](../tools/saved_paint_age_matching.py). Private evidence: `scratch/research/paint-008`.

Five same-length saved-file copies isolate the three paint rows on host 50. Each edits one cache: young color to 65, adult color to 65, young diameter to 12%, young diameter to 12% with the third row blanked, or first/last young row swapped. Other fields and bytes outside the selected cache stay unchanged. These probes do not have game-validated PetzInfo checksums.

| Variant | Prepared appearance and pixels |
| --- | --- |
| Young color | Adult color survives all 36 fixtures; commands and pixels match baseline. |
| Adult color | Color 65 survives every age; 34/36 views show a difference. |
| Young size | Host sizes at ages 0/12, 33, 50, 99/100 are respectively `[12,12,12]`, `[17,19,17]`, `[21,25,21]`, `[32,42,32]`. Changes are visible in 22/36 views. |
| Young size with row dropped | Host count mismatch leaves all three adult sizes and directions in use; 36/36 prepared frames and PNGs match baseline. |
| Young reorder | Paired directions follow young row order within the host, changing 24/36 views. Age 99 still changes directions even when the size edit rounds away; age 100 bypasses young. |

An independent arithmetic prediction checks all 19 resolved rows in each of 216 direct draws. Equal host counts pair by ordinal within the host. The renderer blends diameter, fuzz and normalized direction; the remaining fields come from adult. This experiment directly perturbs diameter, direction and color; fuzz behavior is code-supported and checked with unchanged source values. The mismatched case concerns one host in this saved pet. Young-only rows and additional hosts are outside the composed fixture.

Ages 0/12/33/50/99/100, three named poses, yaw 0/64, saved seed/fatness, fresh raster/line seed 1 and step 0. All 36 fresh local stdio MCP renders (standing front/side, ages 0/50/100) match direct output. Eighteen baseline links match PAINT-007. Age 33 is an explicit override to the saved numerical age. All 62 Python sources match checkout; original and engine hashes are checked.

```sh
scratch/petz-local-venv/bin/python tools/saved_paint_age_matching.py --verify
```

Verification reconstructs copies, reloads and rerenders 216 outputs, checks exact PNGs and recorded MCP hashes, and makes no new MCP calls. Generation refuses an existing evidence directory. This is sampled renderer behavior, not native game validation.
