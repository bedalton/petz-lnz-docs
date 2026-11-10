# LINE-016: connector textures across Petz versions

Date:2026-11-10. Renderer-observed Scottie/Siamese controls in Petz3/5 compared with Petz4 LINE-013. No native-game validation. [Manifest](line-016.json) embeds both version reports and hashes its baseline manifest. Reproducer `scratch/petz-local-venv/bin/python tools/line_texture_versions.py` refuses overwrite; private output scratch/research/line-016/petz3 and petz5. Renderer unchanged.

Reuses LINE-013's five variants: textured-head selection, untextured-marker selection, explicit125 and reversed-endpoint controls. Both endpoint base colors125; stock head texture retained, marker untextured. Fuzz0, edges244/244, widths100/100, edge mode0 and draw_after1 fixed. Existing effective Linez rows frozen. Seed0/age100/fatness50; three numerical poses and standing MCP yaws0/90.

Sixty additional numerical loads preserve geometry within each species/version and verify selected texture remapping. All block/texture check records match the corresponding Petz4 records. Thirty-two local stdio MCP comparisons pass their equal/different expectations; all32 PNGs and64 cell hashes match corresponding Petz4 LINE-013 controls exactly. Two sheets reviewed: Petz3 Dogz inherited/explicit side and Petz5 Catz inherited/explicit front. Metadata explicitly reports the intended game versions, despite the service's generic Petz4 Renderer display name.

The match is limited to these controls in sampled stock breeds. It does not establish version equivalence for long-line rejection, fuzz histories, other texture slots or general breed rendering. Version-specific source/engine/copy/PNG hashes and dependencies are recorded. No stock textures/images are committed.

Initial harness attempts incorrectly passed game_version to load_breed_assets, then omitted the MCP process's version flag. Those attempts are archived privately. Final setup passes version to ResourceResolver and the local MCP CLI; all final metadata uses the intended version. Original files remain unchanged.
