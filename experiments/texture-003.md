# TEXTURE-003: Texture List modes and connector remapping

Date: 2026-11-10. Asset-free parser/remap, asset-backed block/raster and local stdio MCP evidence for Petz4 Scottie/Siamese seed0 adults. No native-game validation. [Manifest](texture-003.json). Reproducer `scratch/petz-local-venv/bin/python tools/texture_mode_probe.py` refuses overwrite; verifier `scratch/petz-local-venv/bin/python tools/check_texture_modes.py`. Private evidence scratch/research/texture-003; audit scratch/research/texture-003-verification.json. Renderer unchanged at9d72d7afd5f7460ef18133c6179caaf8055082d9.

Eighteen parser fixtures cover mode and dimension defaults, malformed numeric tokens and mode boundaries. Forty all-byte remaps cover eight modes ×five colors(10,19,20,125,149). Source bytes0–9 and150–255 remain unchanged in the remapped art; downstream shade addition is separate (LINE-020). No independent derivation of the renderer's ramp lookup tables or native calibration is claimed.

| Mode field | Decoded has_levels | Decoded own_level |
| --- | --- | --- |
| -2,-1,0 | false | -1 |
| 1, absent or malformed | true | -1 |
| 2,9,10,19,150,999 | true | 0 |
| 20 | true | 1 |
| 125 | true | 11 |
| 149 | true | 13 |

The code-supported general rule is: mode>0 sets has_levels; mode<2 gives own_level=-1; mode10–149 gives floor((mode-10)/10); other mode>=2 values give0. Missing/invalid width or height defaults independently to256. The parser accepts values before the asset loader validates dimensions; this experiment does not test invalid-dimension loading.

For assets, a new marker-only256×256 slot repeats modes-1,0,1,2,10,125,149,150. Stock slots/lines are preserved. Marker offset(-35,-160,0), size20 and base color125 stay fixed. Each mode has textured end-selected(-2), explicit125 and absent-line variants.144 numerical loads (2 species ×8 modes ×3 variants ×3 poses) preserve geometry.96 isolated translated512×512 rasters confirm connector paint and output; all textured variants differ from explicit125, and mode equivalences hold independently of the marker circle.

84 MCP standing front/side pairs pass:32 absent/textured comparisons differ;32 explicit/textured comparisons differ;12 equivalence comparisons match(-1=0,2=10,2=150);8 comparisons differ(0 versus1,1 versus2). Every mode draws the line. Same requested dimensions load identical original art bytes across modes; paint metadata and remapped byte hashes vary. Composed mode-to-mode sheets also change the marker's texture, so connector-only claims rely on isolated rasters rather than attributing every composed difference to the line.

Four sheets reviewed: Dogz0/1 front and1/2 side; Catz0/1 side and2/150 front. Modes0/2 show a high-contrast multicolor diagnostic connection; mode1 appears muted. The2/150 sheet is identical. These descriptions concern the supplied stock art/color125 example; color families, own levels, species, versions and native behavior are not generalized. Source, dependencies, engine, original/copy, texture/paint, block/raster, PNG and RGBA hashes are recorded and rechecked. No renderer fixes.
