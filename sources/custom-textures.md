# Community texture authoring notes

Reviewed2026-11-15 for [custom texture authoring](../visual-editing/custom-textures.md). These are source-reported workflows, not independent game validation.

| Primary community source | Focused finding | Applicability/uncertainty |
| --- | --- | --- |
| [Shadowfinder: Convert Textures to the Petz Palette](https://petzhexing.weebly.com/furfilepalette.html) | Import the supplied palette in IrfanView, then save BMP | Does not specify the application's exact index-remapping behavior; no version-specific verification here |
| [Cat Magic: Custom Texture How-To](https://catmagic.neocities.org/texturemaking) | Draw original art, recommends32×32 or64×64; convert through Photoshop Indexed Color with a custom Petz palette and export eight-bit BMP | Recommendations concern source art; does not establish our renderer's expanded tile dimensions or orientation |
| [Unique Petz: Experiments in dithering](https://uniquepetz.spellwork.dev/dither/) | Discusses palette-constrained dithering, restricted color selections and manual edits | Useful design context; our first converter intentionally performs nearest-color mapping without dithering |

The browser retrieved Shadowfinder; Cat Magic and Unique Petz failed through the browser but direct HTTPS GET returned200 and readable tutorial HTML. Raw pages stay private under `scratch/research/custom-textures-sources/`; byte hashes and URLs are in [the retrieval record](custom-textures-retrieval.json). No tutorial artwork or downloadable texture pack was copied into our example tiles. The sources do not establish a universal UV/orientation convention; the guide uses an original asymmetric probe and records renderer observations separately.

Our tool makes the otherwise ambiguous word “palette” explicit: replacing RGB table entries preserves indices; nearest-color conversion chooses new indices; index remapping deliberately recolors selected pixel classes. The renderer's current omission of foreign-palette mapping is [code-supported and controlled](../experiments/custom-001.md), and should not be attributed to these tutorials or generalized to the game.
