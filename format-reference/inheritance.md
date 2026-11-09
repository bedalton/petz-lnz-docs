# Master and breed section inheritance

Status: renderer-observed and code-supported. Native game behavior and cross-version equivalence remain unverified. Evidence: [INHERIT-001](../experiments/inherit-001.md).

The renderer resolves seeded variation choices separately in the selected breed and master LNZ, then replaces complete master sections with breed sections of the same name. It does not merge rows across those two sections.

| Breed section | Effective result |
| --- | --- |
| Absent | Master section retained, if present |
| Present but empty | Empty section replaces the master section |
| Present with some rows | Only breed rows retained |

In Petz 4 Scottie and Siamese copies, a partial Key Balls section containing only the head ID left every other key slot at -1. An empty section left all key slots -1. A full copy of the master section reproduced the absent-section PNG exactly. These are controlled observations for one section, with broader implementation support from merge_sections.

Editing rule: inspect the effective master before introducing a section; retain required rows explicitly when replacing it. Preserve the distinction between an absent section and an empty section. Per-section readers determine defaults and validation after merging, so an empty section is not universally equivalent to a missing section.

Source: renderer revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, appearance/lnz.py (parse_sections, merge_sections) and appearance/layers.py (load_layer). Default Linez File selects a master resource in the renderer; selection/recursion details still need a dedicated reference.
