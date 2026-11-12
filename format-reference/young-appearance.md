# Young appearance and age controls

Scope: renderer4c4d3df; Scottie/Siamese fresh breeds in Petz3/4/5, selected Petz4 saves and private young-resource edits. This is code-supported and renderer-observed behavior, not original-game validation.

For a fresh breed, use `look=age` to blend adult and young appearance at the requested age. Omitted age defaults to12; omitted or zero seed resolves41; omitted fatness defaults to50. Use `look=adult` for the adult layer or `look=puppy`/`kitten` for the young layer. Puppy and kitten are aliases in this implementation: metadata canonicalizes puppy to kitten. Forced looks ignore age for appearance selection and skip juvenile shrinking, though metadata still reports the requested age.

The young resource follows the effective adult `[Little one]` section. The implementation takes its first row, limits it to259 characters, normalizes the filename stem to uppercase and treats exact `X` as absent. `young_name` explicitly overrides this choice for breeds. Explicit `young_name` is used as a case-sensitive resource selector rather than normalized like Little one text. Forced adult ignores it. [Private-copy routing controls](../experiments/young-004.md) confirm first-row selection, path normalization, exact X versus lowercase x failures, and branch-driven routing in Petz4 Scottie/Siamese. A valid explicit selector rescues an invalid effective Little one branch. Resource inheritance searches the breed before master at every hop, keeps earlier sections and stops at16 resources. Each file restarts variation sampling with the same resolved seed. These lookup limits and sentinel details are code-supported in appearance/layers.py and breed_variations.py; the stock experiment samples only the present breed chains.

| Age | Young weight | Scale subtraction |
| --- | --- | --- |
| 0–11 | 100% | 2 × (12 − age) |
| 12–100 | 100 − floor((age − 12) × 100 / 88)% | 0 |

The subtraction applies to pet and ball scales after blending. Integer fields use adult + trunc((young − adult) × weight /100), where truncation is toward zero. Age13 still has100% young weight. Growth is quantized; neighboring ages need not produce distinct pixels.

Age averaging selects fields to blend; it does not switch wholesale between resources. Shape fields, scales, ball size and fuzz blend, while ordinary ball colors retain adult values. Forced young uses the young appearance directly. Consequently, a young-only color edit can affect forced puppy/kitten output while leaving age-based output unchanged. Keep `look` explicit when comparing an edited young resource with adult or saved previews.

Saved Petz4 inputs default to saved age/fatness/seed. Present adult/young caches are authoritative and do not inherit breed text. Missing caches fall back independently to the named breed at the saved resolved nonzero seed. Forced adult needs the adult layer; forced young needs the young layer; age mode loads both even at100. A missing young dependency can therefore make age100 fail while forced adult succeeds. In the saved controls, Fuzzkin with exactly one missing cache has different age12 and forced-young pixels in both views; this endpoint equality is not universal. Saved inputs reject seed and branch overrides. Petz3/5 saved inputs remain unsupported.

Evidence: [fresh controls](../experiments/young-001.md), [saved-cache controls](../experiments/young-002.md), [young-resource edits and arithmetic](../experiments/young-003.md). Renderer source paths are recorded in those manifests. Paint directions, count-mismatched lists, inheritance cycles and original-game behavior require their own evidence; endpoint equality in the stock sample does not establish universal field equivalence.
