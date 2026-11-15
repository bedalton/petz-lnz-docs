# Untracked istall-node investigation

2026-11-15. `/workspace/istall-node` is a3907-byte Bash script configuring the NodeSource Node.js24 apt repository. It installs prerequisites and writes repository/key configuration if executed, then prints a separate nodejs installation command. It contains no mechanism to create another copy of itself. It was inspected, not executed, deleted or modified.

Current permissions0644; recorded modification/birth timestamp2026-11-09 21:11 UTC and inode-change timestamp2026-11-14 15:17 UTC. These timestamps do not identify the creator and can survive file transfer. Historical handoffs/session notes repeatedly record it as an existing unrelated untracked file from2026-11-10 onward. Earlier agents deliberately preserved it; repeated Git status output alone does not show repeated creation. Git contains no tracked history for this path.

No creator was found in searched project tooling, selected shell startup files, /etc, /opt or /usr/local/bin. Codex history/session files contain mentions, but no creator is established by this investigation. A downloaded environment/setup script is a plausible origin, not a verified attribution. Sync/restoration could also preserve an older file; no recurrence was observed or experimentally reproduced. No startup configuration was changed.

Private size/hash/stat evidence: `scratch/research/workspace-node-installer/inspection.json`. The file remains in place because the request was to explain its origin; no removal or Git-ignore change was requested.
