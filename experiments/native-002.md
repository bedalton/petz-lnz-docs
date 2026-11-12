# NATIVE-002 — capture-time saved-state controls

Petz4 Fuzzkin, Goobe and Homebody on renderer49c7f62. This is a renderer experiment using saves associated with native captures, not a controlled game/render equivalence test. The [intake](../docs/native-capture-intake-2026-11-12.md) records capture provenance and limitations.

## Reproduce

```sh
scratch/petz-local-x86-venv/bin/python tools/native_saved_controls.py
scratch/petz-local-x86-venv/bin/python tools/native_saved_controls.py --verify
scratch/petz-local-x86-venv/bin/python tools/check_native_saved_controls.py
```

The first command requires a fresh output directory; preserve existing evidence rather than overwriting it. Public metadata: [manifest](native-002.json). Private images, MCP response metadata, three unscaled comparison sheets and independent audit are under `scratch/research/native-002`. Logs: `scratch/native-002-{run,replay,audit}.log`.

Backend: installed direct API plus fresh local stdio MCP;62 installed Python source hashes match the checkout. The manifest records renderer revision, dependency versions, six save hashes, cache hashes, resource provenance and controls. No saved file, extracted LNZ or raw image is committed. Original files remain read-only.

## Controls and results

Both adult and young caches match exactly within each old/capture-time pair. Saved inputs resolved as follows; age is the renderer's saved age field, not independently verified chronological age.

| Pet | Prior age / fatness | Capture-time age / fatness |
| --- | --- | --- |
| Fuzzkin |33 /50 |69 /12 |
| Goobe |12 /50 |51 /47 |
| Homebody |15 /50 |12 /50 |

Cross both ages and both fatness values on both saves in standing/sitting/lying at eight45° yaws. The576 saved PNGs include288 matched-source comparisons. All288 pairs have identical prepared frames, indexed pixels, output dimensions, origins and PNG bytes. Only preview provenance and diagnostics differ between the loaded assets at common controls.36 fresh MCP endpoints match direct API output exactly; their age and fatness are taken from the save without overrides.

| Pet | Default endpoints differ | Age-only differs | Fatness-only differs |
| --- | --- | --- | --- |
| Fuzzkin |24/24 views |24/24 |24/24 |
| Goobe |24/24 |24/24 |23/24 |
| Homebody |24/24 |24/24 |0/24 |

The Homebody fatness axis deliberately repeats50 as a no-op control. This table measures any aligned RGBA difference, not perceptual size or color change. Native screenshot geometry is not used in these comparisons.

The independent audit decodes all576 PNGs, reconstructs absolute-coordinate pixel maps and checks648 RGBA relationships:288 source equalities and360 age/fatness differences. Nine additional default loads check palettes/textures and per-entry changes: Fuzzkin/Goobe ball records change size; Homebody changes size and fuzz. Palettes and texture assets match within all three source pairs. The generator also checks all21 previously recorded original hashes. An initial audit assertion incorrectly expected size-only changes for Homebody; its failure is retained in `scratch/native-002-audit-initial.log`, and the corrected audit explicitly permits its observed fuzz changes.

## Visual interpretation and limits

Three unscaled12-row sheets were reviewed. Both old and capture-time Goobe renders have a tan/gold coat; changing saved age/fatness changes geometry and some raster pixels but does not reproduce the older screenshots' reddish-brown coat. The cause of that game-observed historical color difference remains unresolved. Identical caches do not establish that all game appearance state is decoded.

The contemporaneous Goobe game capture shows clothing and an extended tongue. These stock still previews do not reproduce that exact scene or pose; the missing top hat is consistent with the separately documented clothing limitation. Fuzzkin's dark coat/orange markings and Homebody's light coat are qualitatively recognizable, without a measured shape/texture correspondence claim.

The findings establish how this renderer handles these six saves. They do not establish native age/fatness semantics, exact game pose/yaw, screenshot scaling, ignored-state irrelevance in the game, or fidelity across other pets/versions.
