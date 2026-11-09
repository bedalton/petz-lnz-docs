# RESTORE-001: fresh container recovery

Date: 2026-11-09. Setup evidence only; no rendering performed.

The new container retained tracked documentation but lacked games/, scratch/ and the ignored renderer checkout. Recovered the renderer at the recorded revision 9d72d7afd5f7460ef18133c6179caaf8055082d9 and reinstalled package 0.1.0 with CPython 3.12.16 using the SMOKE-001 uv commands. No renderer source changes. Dependencies are freshly resolved under the checkout constraints; equivalence to the old runtime is not established. Private installation metadata remains under scratch/petz-local-venv.

The installed local launcher was executed with `--game-root /workspace/games/petz4 --check`. It exited 2: `/workspace/games` does not exist. LocalRunner validates engine resources before constructing the MCP server, so no local server or connection is running. Raw check output: scratch/research/restore-001/check.txt (ignored).

To unblock, restore the user's game resources under games/petz4, including Petz 4.exe and Resource/Petz 4 Rez.dll, Dogz 4 Rez.dll and Catz 4 Rez.dll. Controlled scripts additionally need Resource/Dogz/Scottie.dog and Resource/Catz/Siamese.cat. Restore other installations for cross-version work. Do not fabricate files to bypass startup checks. Prior private images/checkpoints were not recovered; tracked manifests remain historical evidence.

Then run the launcher check and a real MCP client smoke test in a new evidence directory, recording dependency and shared-engine hashes before comparisons. See [original setup](smoke-001.md).
