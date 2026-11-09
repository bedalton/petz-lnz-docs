# BALL-001: head size, color and movement

Date: 2026-11-09. Status: renderer-observed and code-supported; not game-validated. Petz 4 only, Scottie and Siamese.

## Method and safeguards

Run `scratch/petz-local-venv/bin/python tools/ball_probe.py` from /workspace. Uses the same installed renderer and Python as [SMOKE-001](smoke-001.md). All calls use local stdio MCP, standing pose, yaw 0°, seed 0, age 100 and fatness 50.

The script reads the adult breed LNZ and resolves it at seed 0. It serializes this section table into the original resource span, padding with spaces to retain its exact byte length. It rejects payloads exceeding that span. This is a constrained experimental technique, not a general PE resource editor: comments and alternative variation branches are removed in the private control copies. Do not distribute these as variation-preserving edits.

Assertions verify every other resource payload and every byte outside the edited resource span is unchanged. Original files are never written. Original and normalized control PNGs matched exactly for both breeds. Full render provenance and private section-count inventories are in scratch/research/ball-001. [Tracked manifest](ball-001.json) records input/output hashes and controls. Script reruns overwrite that directory; preserve evidence before changing the procedure.

## Results

The master LNZ Key Balls section identifies head ball 52 for Dogz and 24 for Catz. These are initial anatomical anchors, not complete atlas entries.

Each variant starts from the same normalized control and appends one row to the existing section (creating that section if absent):

| Variant | Section | Dogz row | Catz row | Result |
| --- | --- | --- | --- | --- |
| Size | Ball Size Override | 52, 25 | 24, 25 | Both PNG hashes change; head circle appears larger |
| Color | Color Info Override | 52, 125 | 24, 125 | Both PNG hashes change; exposed head regions change color |
| Move | Move | 52, 20, 0, 0 | 24, 20, 0, 0 | Both PNG hashes change; head circle separates from facial features |

All ten final renders completed. Original/control matching also reproduced the previous smoke PNG hashes for the two originals. This is narrow repeatability evidence, not a complete repeatability matrix.

Images were reviewed at native resolution. They suggest that moving or enlarging the head base ball alone does not carry all facial features with it. No world-axis or screen-direction claim is established: Move vectors are rotated using the referenced frame ball in the renderer, and the omitted fifth field defaults to the target ball.

The first trial used color 35, already the Scottie head's base value; its unchanged PNG was a valid no-op, not evidence that the color section failed. The final trial uses 125 for both species. Palette appearance remains dependent on texture and rendering context; no universal color-name mapping is claimed.

## Implementation interpretation

At renderer revision 9d72d7afd5f7460ef18133c6179caaf8055082d9:

- appearance/core.py applies Ball Size Override by replacing the ball's static size field, rather than adding to that field. rendering/sizing.py subsequently adds the static value to the animated diameter before scaling and clamping. Thus a value of 25 is not an instruction for a 25-pixel ball.
- Color Info Override replaces base color; optional columns can affect group/texture. This experiment uses only the first two columns.
- Move rows accumulate with existing rows, and positions.py rotates their vectors before applying them. The guide must distinguish individual-ball displacement from moving an anatomical group.

## Next tests

Add aligned comparison sheets and geometry assertions; test multiple views, positive/negative increments, head-group edits and inheritance with absent/empty/partial sections. Inventory all master ball labels before expanding mappings. Verify these findings across breeds and versions before generalizing.
