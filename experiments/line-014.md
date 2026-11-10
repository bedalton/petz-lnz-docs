# LINE-014: connector texture windows and size limits

Date:2026-11-10. Asset-free code-supported direct indexed raster fixtures; no MCP, game assets or native validation. [Manifest](line-014.json). Reproducer `scratch/petz-local-venv/bin/python tools/line_texture_window.py` refuses overwrite. Private raw synthetic pixels scratch/research/line-014/pixels.json. Renderer unchanged; source/dependency hashes recorded.

72 fixtures cross an8x8 synthetic texture, periods0/8, horizontal/vertical axes, spans7/8/9, endpoint reversal and fuzz0/1/7. Endpoint thickness3, edge mode -1, shade offset0 and seed1 are fixed; the texture contains distinct row-major values160–223. Each textured raster has an untextured control with the same geometry.

28 textured fixtures draw and44 are entirely rejected. Every untextured control draws. Rejection occurs when raster width (including fuzz margin) or height exceeds texture dimensions. Rejected cases leave RNG/tables unchanged: the size guard precedes fuzz-table generation. Fuzz can therefore push an otherwise fitting connector over the texture-width limit. This is implementation behavior, not an inferred native limit.

For accepted fuzz0 cases,120 centerline sample assertions confirm a centered crop: source x uses floor((texture_width-raster_width)/2), while source y uses ceil((texture_height-raster_height)/2). Odd spare space is biased differently on the two axes. Reversal preserves these sample coordinates. Texture period0 versus8 produces identical pixels in all36 paired fixtures: this raster path does not wrap the connector window to rescue an oversized block.

The controls deliberately bypass remap_texture, use a small synthetic TexturePaint and avoid clipping. Actual stock texture sizes, diagonal geometry, shaded/signed sampling, textured fuzz histories and composed breed rejection need separate evidence. No renderer fix is proposed.
