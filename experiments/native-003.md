# NATIVE-003 — exact screenshot pixel grids

All21 supplied PNGs are exactly representable as cropped2× nearest-neighbor replication grids. Each has one exact phase among the29 phase/factor combinations tested (factors2,3,4). This is an encoded-raster observation, not proof of Mac DPI, original engine resolution, capture method or renderer/game geometry equivalence.

## Reproduce and evidence

```sh
scratch/petz-local-x86-venv/bin/python tools/native_pixel_grid.py
scratch/petz-local-x86-venv/bin/python tools/native_pixel_grid.py --verify
scratch/petz-local-x86-venv/bin/python tools/check_native_pixel_grid.py
```

The first command requires a fresh private output folder. [Manifest](native-003.json) records input/reduced-image hashes, exact mismatch counts for609 still-image grid candidates, NumPy/Pillow versions and19 synthetic controls. `scratch/research/native-003` holds21 reduced PNGs, the report and an independent audit. No renderer or hosted backend is used; this tests source RGB samples. Original screenshot/save/video files stay read-only.

## Full-image controls

All pixels are included, including clipped first/last rows and columns. A phase of1 means the first full doubled block starts at coordinate1, leaving a clipped singleton at coordinate0. The reduced copy retains that boundary representative; it is not a generic resize or a claim to recover the missing off-crop pixel.

| First full block phase (x,y) | PNG count |
| --- | --- |
|0,0 |14 |
|0,1 |5 |
|1,0 |1 |
|1,1 |1 |

The independent Pillow/scalar verifier reconstructs all1,639,127 source RGB pixels from the reduced images without NumPy grid helpers. It independently confirms657 exact/non-exact decisions:609 still candidates and48 video-sample candidates. Every non-exact candidate has a saved first-mismatch witness. All25 intake file hashes still match.

Synthetic controls cover16 combinations of one-pixel clipping on all four sides, one-channel/one-pixel corruption, bilinear scaling, and4× replication. The latter is compatible with both2× and4× grids, demonstrating why a passing2× test alone does not establish a fundamental pixel scale. The real PNGs reject all tested3× and4× grids. Full replay and independent audit pass; logs are `scratch/native-003-{run,replay,audit}.log`.

## Video and native scope

None of the12 decoded H.264 samples is an exact2× grid at any phase. This does not disprove an underlying doubled game image: lossy video encoding/resampling can destroy exact repetition. Do not apply the still-image lossless reduction to the video as an established inverse transform.

These untagged reductions preserve encoded RGB samples at half the replicated interior dimensions. They do not preserve embedded ICC interpretation: use the later [NATIVE-004 tagged/converted copies](native-004.md) for qualitative color review. They do not solve camera projection, animated pose, head movement, expression, clothing, pet size or screenshot-to-render alignment. Quantitative native geometry/fidelity remains unvalidated. See the [capture intake](../docs/native-capture-intake-2026-11-12.md) and [saved-state controls](native-002.md) for separate provenance and renderer evidence.
