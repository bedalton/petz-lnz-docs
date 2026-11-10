# MORPH-002: relative sizing in a morph group

**Renderer update review:** [UPDATE-001](update-001.md#completed-historical-mcp-replay) confirms this unit's replayed comparison relationships on6c1d883. The measurements below remain the historical9d72d7a record; exact pixels and numerical geometry are revalidated only where explicitly listed in the review.

Date: 2026-11-10. Petz 4 Scottie/Siamese, numerical renderer and default-state MCP evidence. Native-game semantics unvalidated; no renderer fixes.

Run `scratch/petz-local-venv/bin/python tools/relative_morph_probe.py`; refuses existing output. [Manifest](morph-002.json) records five variants/species, private-copy hashes, numerical geometry, controls, twelve MCP PNG hashes, dependency versions, engine hashes and installed source hashes. Private evidence: scratch/research/morph-002. Evaluation, morph and attachment source bytes match checkout revision 9d72d7afd5f7460ef18133c6179caaf8055082d9. Four engine hashes match RESTORE-002. Fixed-span copy safeguards and source hash checks preserve original game files and unrelated resources.

## Controls

Append one marker with offsets (-36,-80,0), area 8, a head connector, and either ordinary size 20 or head-relative size 20/0. Group 15 is checked unused before adding the marker. Group 0 controls are static; group 15 controls start dormant. Seed 0, age 100, fatness 50; standing/sitting/lying.

Forty-eight numerical checks cover two grouped variants × four explicit percentages (0/25/50/100) × three poses × two species. Each records evaluated size, offset, head radius and marker geometry. Ordered updates 100→0→50 equal a direct 50 update for both variants in all six species/pose settings.

| Group-15 variant | Morph size at 0/25/50/100 | Radius when active | Full-activation counterpart |
| --- | --- | --- | --- |
| ordinary size 20 | 0/5/10/20 | ordinary diameter formula | static ordinary size 20 |
| head-relative size 20 | 0/0/0/0 | referenced head radius | static head-relative size 0 |

Both variants scale their offsets with percentage. Both park at 0% with radius zero. The relative marker has the full referenced head radius at every tested positive percentage, even 25%; its radius does not scale down with its offsets.

Code-supported explanation: morph initialization gives nonzero groups size zero. Subsequent group updates scale ordinary sizes only; a valid size-reference field excludes size updates. Attachment then adds that zero size contribution to the referenced radius. A static group-0 relative-size-20 marker instead retains its initial size 20. Full activation of the grouped marker consequently differs from the authored-size static counterpart, while its entire posed geometry equals the static relative-size-0 variant.

This is a reproducible implementation distinction, not proof of a defect. Native intended behavior needs independent evidence before any fix; tracked as GAP-005 in [renderer gaps](../troubleshooting/rendering-gaps.md). No automatic animation or activated MCP render claim.

## MCP controls

Twelve local stdio MCP standing comparisons at yaw 0/90, both species and other controls above. Group-relative20/group-ordinary20 default dormant images match (four pairs); static-relative0/static-relative20 differ (four); static-relative0/group-relative20 differ (four). All expectations asserted. These images only cover default activation, not explicit numerical percentage updates.

Dogz-static_relative0-static_relative20-90 and Catz-static_relative0-group_relative20-0 sheets reviewed at native resolution: former shows the larger static size offset; latter loses the dormant marker and connector. Only two Petz 4 breeds and one otherwise-unused group are sampled. Negative sizes, relative references to other added markers, multiple groups and native runtime remain separate topics.
