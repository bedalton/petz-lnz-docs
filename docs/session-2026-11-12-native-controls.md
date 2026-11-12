# Twenty-minute native-capture continuation

This session advances the [November12 native intake](native-capture-intake-2026-11-12.md) into reproducible saved-state, raster-grid and color-profile controls. It does not establish controlled native-game fidelity. The [focused comparison index](native-comparison-controls.md) is the entry point for future work.

## Completed units

| Unit | Evidence | Outcome |
| --- | --- | --- |
| [NATIVE-002](../experiments/native-002.md) |576 saved direct PNGs,36 initial local stdio MCP matches,288 source-pair equalities,648 independently decoded RGBA relationships | Three old/capture-time save pairs render identically at common age/fatness. Default endpoints differ; native meaning of other saved state remains open. |
| [NATIVE-003](../experiments/native-003.md) |21 lossless encoded-sample reductions,609 still candidates,48 video candidates,19 synthetic controls | All21 PNGs exactly fit cropped2× replication; all1,639,127 source RGB pixels reconstruct. No exact2× phase in12 lossy video samples. |
| [NATIVE-004](../experiments/native-004.md) |21 original-profile tagged and21 sRGB reduced copies;410,690 managed pixels,1,583 unique-color mappings,84 palette tallies | Preserve embedded ICC interpretation for visual review. Two source profiles; conversion improves palette correspondence for18 stills, without explaining all color differences. Nine old/new prefix arrays agree. |

All three full replays pass. Their independent audits also pass, with NATIVE-004 explicitly using the same LittleCMS engine through a different artifact-checking path. Three unscaled saved-control sheets and one profile-aware qualitative sheet were reviewed. Initial harness assumptions and superseded sheet layout are retained privately and described in the unit records.

## Integrity and backend

Run:

```sh
scratch/petz-local-x86-venv/bin/python tools/check_native_session.py
scratch/petz-local-x86-venv/bin/python tools/check_docs.py
```

The session checker links manifest/audit/script hashes, validates all three replay logs, rehashes 639 retained experimental PNGs, checks all 25 native intake files and 21 previously recorded game originals, and confirms all 62 installed renderer Python sources match checkout `49c7f62`. The detailed private record is `scratch/research/native-session/verification.json`; replay/audit log paths are recorded there and in the unit pages. Input scope is recorded files, not a complete installation audit.

The local HTTP service was absent and was restarted with the game root plus screenshot/young-fixture asset roots. PID 33654, exec session 86330, endpoint `http://127.0.0.1:8765/mcp`. Six-tool discovery, capabilities and six actual capture-time saved-pet renders (three pets, standing front/side) pass against direct PNG hashes per completed session audit. Two successful audit runs made 12 HTTP render requests; the second added audit-script hash links. These are separate from the initial 36 stdio research renders and 36 full-replay renders. Hosted service state is not inferred.

No renderer source or original game/capture file was modified. The renderer's pre-existing `.gitignore` change remains untouched. Proprietary inputs, extracted text, raw images, profiles, environments and logs remain under ignored workspace scratch/game paths. Each research unit is committed with the requested identity; no co-author trailers are added.

## What remains unresolved

The latest Goobe native screenshot is tan/gold while historical screenshots are reddish-brown. Both renderer save endpoints remain tan/gold, and cache texts, bounded prefix arrays and all Goobe ICC tags match across their respective pairs. These controls do not identify the native cause.

Exact native runtime/resources, pose, expression, head movement, clothing, camera projection and renderer color-space fidelity remain unvalidated. The still-grid result supplies an exact image-sample reduction, not an engine-scale calibration. Next useful work is a controlled native pose/state correspondence or additional decoded appearance-state evidence; repeating identical previews would not resolve those questions.
