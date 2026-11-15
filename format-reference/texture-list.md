# Texture List: preview fields

Evidence: [TEXTURE-003](../experiments/texture-003.md) and [LINE-021](../experiments/line-021.md). Renderer9d72d7afd5f7460ef18133c6179caaf8055082d9, Petz4 Scottie/Siamese adult copies; no native-game validation. These are decoded renderer fields, not an independently validated game specification.

**Renderer update:** [UPDATE-001](../experiments/update-001.md) confirms new sampled textured paint/Outline support and legacy paint mapping. Historical connector controls here do not validate those separate paths; use the update controls. Clothing remains unsupported; original-game fidelity remains open.

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

The isolated connector samples also group modes125/149 with mode0 despite different flags/shade metadata. Standing Catz mode125 has a different whole remapped-art hash but equal connector-window pixels. Treat these equal previews as local observations, not equivalent authoring settings.

All effective slots are loaded, so parser acceptance alone does not establish that dimensions or resources can be rendered. Invalid dimension loading, young resources, other breeds/versions and native tint semantics remain untested here. [CUSTOM-001](../experiments/custom-001.md) now tests original generated artwork embedded into private copied breed resources; loose external BMP loading fails in those controls. Use the [custom texture workflow](../visual-editing/custom-textures.md) for palette conversion and artwork transforms. Repeated preview agreement is not game validation.
