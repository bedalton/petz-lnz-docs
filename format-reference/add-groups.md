# Added-ball groups and dormant geometry

Evidence: [MORPH-001](../experiments/morph-001.md), Petz 4 Scottie/Siamese. Default-state local MCP images plus explicit numerical renderer updates; native-game behavior unvalidated.

Add Ball column 13 is the add group. In the tested default state, group 0 is active and an unused group 15 starts at zero. The latter marker remains defined but is parked with radius zero; its visibility flag alone is still true. Check parked status, radius, group amount and omissions together when diagnosing invisible details.

Dormancy and omission differ. The dormant marker keeps a parsed incident connector, but the default image shows neither marker nor connector. An omitted marker has visible false and retains its geometry while incident lines are dropped during parsing. Both can produce identical pixels.

Direct Python `posed_geometry(..., morph_updates=((15, percent),))` checks at 0/25/50/100 scale the ordinary marker's local offsets and size. Full activation matches the static group-0 counterpart in this sample. These are explicit implementation controls, not an LNZ section assigning a percentage and not automatic game animation. MCP comparisons in MORPH-001 exercise only the default state.

Keep existing rows and compute IDs before changing groups. Activating a group can affect every member; the experiment first verified group 15 unused in stock additions. Relative sizing, body-area exceptions, multiple groups and native runtime transitions need separate tests. See [Add Ball fields](add-ball.md), [connected details](linez.md) and [visibility diagnosis](../visual-editing/visibility.md).
