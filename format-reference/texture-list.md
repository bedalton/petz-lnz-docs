# Texture List: preview fields

Evidence: [TEXTURE-003](../experiments/texture-003.md) and [LINE-021](../experiments/line-021.md). Renderer9d72d7afd5f7460ef18133c6179caaf8055082d9, Petz4 Scottie/Siamese adult copies; no native-game validation. These are decoded renderer fields, not an independently validated game specification.

Rows are interpreted as `art_path, mode, tile_width, tile_height`. Slot indices follow row order; ball/add-ball texture indices select them. Preserve effective inherited slots when overriding the section. The controlled experiments append a dedicated slot for a diagnostic marker rather than changing existing slot indices.

| Field | Code-supported decoding and sampled controls |
| --- | --- |
| Path | Art resource name; experiments reuse a loaded stock path |
| Mode absent/invalid | Defaults to1 |
| Mode<=0 | has_levels=false, own_level=-1; -1 and0 match in composed controls |
| Mode1 | has_levels=true, own_level=-1 |
| Mode>=2 | has_levels=true; own_level=floor((mode-10)/10) for10–149, otherwise0;2,10,150 match in composed controls |
| Width/height absent/invalid | Independently default to256; valid64×128 and partial rows checked in parser |
| Authored dimensions |32×256,256×32,64×64,128×128,256×256 loaded and compared in LINE-021 |

Mode0,1 and2 produce different sampled connector pixels at base color125. Modes125/149 decode own levels11/13; do not interpret the raw field as a direct output color. The renderer uses has_levels/own_level when remapping original texture bytes and supplying shade/sign metadata. Forty synthetic all-byte remaps show bytes0–9 and150–255 unchanged at this remap stage; later raster shade addition can still change them. See [connector textures](connector-textures.md) for selection, limits and raster shading, and [retained texture state](texture-state.md) for frame history.

All effective slots are loaded, so parser acceptance alone does not establish that dimensions or resources can be rendered. Invalid dimension loading, custom external art, young resources, other breeds/versions and native tint semantics remain untested here. Repeated preview agreement is not game validation.
