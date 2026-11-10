# PAINT-005: saved color-array prefix controls

Date: 2026-11-10. Petz4 Fuzzkin, Homebody and Goobe saved files; integration6c1d883. [Manifest](paint-005.json), [reproducer/verifier](../tools/saved_colour_arrays.py). Private copies, PNGs and MCP metadata are under scratch/research/paint-005.

## Result

Each of three prefix arrays, and all three together, can be changed in these copies without changing the returned SavedAppearance, loaded appearance, frame, sizes, textures, palette, prepared commands, indexed pixels or PNG bytes. Twelve copies yield72 edited views across standing/sitting/lying and front/side;72 separate baseline draws agree. Thirty fresh local stdio MCP renders include six original baselines and24 edited views;all match their direct controls. Forty-eight edited Fuzzkin/Homebody views also link exactly to PAINT-001 fresh PNG hashes.

This is renderer-observed behavior, supported by the reader implementation: it validates array counts and skips each payload rather than returning it. load_saved_assets subsequently parses the authoritative adult/young caches. This does not identify the native meaning of each skipped array, prove valid game checksums or establish original-game fidelity. The source labels these arrays as saved colour arrays;array ordinal is used here rather than an inferred semantic name.

## Controls and provenance

All three files contain arrays of512 one-byte entries,15 four-byte entries and512 four-byte entries. Copy variants set array0 bytes to1;array1 and array2 little-endian entries to65;the combined variant applies all three. Counts, lengths and every byte outside selected payload ranges remain identical. All three original arrays are hash-recorded;no raw payload is committed. Returned saved metadata and both caches remain exactly equal. Original hashes are checked again after rendering.

The direct and MCP paths retain saved age, seed and fatness; fixed named poses use fresh state, yaw0/64 engine units (0/90 degrees), raster/line seed1 and step0. Source, engine, dependency and PAINT-001 manifest hashes are recorded. All62 installed Python sources match checkout. Copies are renderer probes: the PetzInfo stream checksum is neither recomputed nor validated by this build, so do not load these probes into the game as validated saves.

## Reproduce and limitations

```sh
scratch/petz-local-venv/bin/python tools/saved_colour_arrays.py --verify
```

Generation refuses an existing evidence directory. Verification reconstructs every copy,checks byte boundaries and parsed equality,reloads/rerenders all72 edited and72 baseline views,checks persisted PNG hashes and checks MCP game-version metadata. It does not make new MCP calls.

This isolates skipped prefix arrays,not cached paint group tokens. The sampled saved pets use their stored mixed-age appearance;no broad young/adult-age sweep,other version or native retint claim follows. Next:independent cached Paint Ballz group/color controls and native evidence.
