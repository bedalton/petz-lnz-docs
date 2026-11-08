# Section inheritance: initial implementation finding

Evidence status: code-supported only. Species/version game semantics remain unverified.

The local renderer parses LNZ into named sections, then merges the master and breed section tables. Its `merge_sections` replaces a complete master section with the breed section of the same name, including an empty section. It does not merge individual rows.

Source: renderer revision 9d72d7afd5f7460ef18133c6179caaf8055082d9, src/petz_renderer/appearance/lnz.py, merge_sections. parse_sections applies seeded variation selection before returning the section table.

Editing implication to test: adding a partial replacement section may remove inherited rows. Do not recommend appending a single row to an absent breed section until the section's row semantics and inheritance have been verified.

Pending experiment: compare absent, empty and partial sections on a private breed copy; inspect effective appearance and render differences. This page is a hypothesis guide, not an established game-format rule.
