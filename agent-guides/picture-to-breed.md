# Create a breed from a picture

This authoring workflow incorporates the [Mastiff trial review](../docs/mastiff-authoring-trial-review.md) and [existing-anatomy research](../experiments/anatomy-002.md). A clean independent end-to-end trial remains unperformed. Most editing evidence concerns Petz 4 Scottie/Siamese; other breeds, versions and saved pets require checking the linked scope. A successful preview is renderer-observed, not game-validated.

## Start with a usable task

Read the project's AGENTS.md, then fill in the [task brief](task-brief.md). Use the [feature map](feature-to-control.md) as needed, rather than reading every experiment. STATUS/HANDOFF contain historical environment notes: verify the running tools instead of assuming an old PID, installation or build remains current. The user's current task takes precedence over historical session time limits.

You need the reference image, an authorized baseline breed and dependencies, a renderer, and an editing method that can write the requested output format. Documentation alone does not provide the private game assets or a general-purpose breed-file writer. If any required input is missing, record exactly what is missing; continue image analysis and planning where possible, but do not invent an executable result.

Keep inputs, working copies, renders and notes under `/workspace/scratch/authoring/<task-id>/`. Make separate inputs, working, previews and evidence subfolders. Never edit originals or commit proprietary files, extracted stock LNZ or raw renders. Follow the project's status, handoff and commit requirements for documentation/code units.

## Preserve and reshape existing anatomy

Reuse existing ears, tails, mouth/tongue details and their attachments. Do not hide, delete, park, suppress through zero effective size or recreate an existing ear or tail to change its appearance. Do not blanket-omit stock added balls. Use the researched [existing ear/tail recipes](../visual-editing/existing-ears-and-tail.md); adding genuinely new ornaments is a separate operation. Preserve original IDs, attachment parents, connector topology, required texture references and variation structure.

Authoring agents should apply the shared recipes and compare their design candidates, not rediscover fundamental field behavior on every task. If the requested anatomy cannot yet be achieved with documented controls, retain it and record the precise missing recipe for central research. An undocumented shape is an unmet requirement, not permission to substitute a replacement chain.

## 1. Turn the image into an edit plan

Inspect the image directly. Record species, viewpoint, apparent age/style and the three to five features most responsible for recognition. Distinguish observed features from guesses about the hidden side, depth, anatomy or markings. Perspective and pose can mimic proportion differences.

Use relative measurements where useful: head width/body width, muzzle length/head width, eye spacing/head width, ear height/head height and leg length/body height. These are design targets, not conversions into LNZ coordinates. Record approximate targets and uncertainty rather than false precision.

Build a short plan:

| Priority | Observed feature | Baseline mismatch | Proposed control | Review views | Unknowns |
| --- | --- | --- | --- | --- | --- |
| 1 | Fill from the actual image | Compare after baseline render | Link from feature map | Front/side, then relevant pose | Hidden depth, applicability, etc. |

Choose reasonable assumptions for minor missing details and record them. Ask for clarification when species/version, required output or a defining hidden feature would change the work substantially. A single image supports an interpretation, not a uniquely recoverable 3D breed.

## 2. Choose and inspect a baseline

For supplied Petz 4 blanks, start with the [blank dog catalog](../clean_dogs/README.md): each exact filename links to six-view blank and stock sheets. Overview thumbnails fit each dog separately; compare full sheets for relative size. Transfer the ignored reference images with the breed files when handing off to another agent.

Prefer an available breed with similar overall construction, proportions, ears, muzzle and coat organization. Record why it is suitable; do not choose solely by coat color. If several candidates exist, render a small comparison before committing. If only one is available, state the compromise.

Identify version, species, adult/young resources, master inheritance, effective sections, existing addballs, textures and variation branches. Use [anatomy indices](start.md#route-by-task) as candidate labels; confirm important IDs with a controlled visible change. Row positions and explicit IDs are different conventions: consult the field reference before editing.

An existing saved `.pet` is a separate target: Petz 4 saved caches can remain authoritative after breed edits. Do not assume changing a breed will change an existing pet. See [young appearance and caches](../format-reference/young-appearance.md). Agree whether the deliverable is a new breed, a saved pet or an LNZ prototype.

## 3. Establish rendering and writing controls

Prefer local petz-render MCP. Call its `get_capabilities`, then `list_poses` and `inspect_input` as appropriate; use the current returned schemas. Record backend, renderer/runtime versions, input/dependency hashes and exact render arguments. Test one baseline render before making edits.

Local tools use paths under configured asset roots; connected hosted tools use upload bundles and cannot read local paths. For local setup, consult `petz-renderer-mcp/docs/local-mcp.md` if that checkout is present. If absent, get the matching setup documentation with the renderer; it is an ignored external dependency, not part of this guide's portable files. Configure a private working asset root rather than modifying game resources. For hosted fallback, follow the live capability upload guide and record which assets were supplied.

For an adult breed shape study, explicitly set `look=adult`, age 100, fatness 50 and seed 41 where supported. Fix pose, yaw, scale/framing and all other controls between comparisons; record returned effective values. These are proposed trial controls, not the renderer's defaults. Fresh breed defaults can select young appearance. For a young or saved target, choose the intended controls and retain saved identity/cache behavior rather than imposing adult settings. Start with standing front yaw 0 and side yaw 90, then use verified sitting/lying poses and additional angles.

Before a substantive edit, prove the write/read path: create a separate unchanged copy, inspect it and confirm its render matches the original at identical controls. If the writer normalizes or resolves variation, compare a normalized control too and disclose the loss of alternatives. Research scripts use constrained resource-span edits and may overwrite outputs; they are not general breed writers. See [BALL-001's method](../experiments/ball-001.md#method-and-safeguards). Use a suitable resource editor for binary `.dog`/`.cat` containers; do not save plain LNZ text under a binary extension. If no writer is available, deliver an explicitly labeled edit specification/prototype and report the packaging blocker.

## 4. Iterate from large features to small ones

Work on silhouette and proportions first, then face/eyes, coat and markings, and finally small details. This order is a proposed authoring strategy, not an experimentally proven optimum. Keep the original baseline and a last accepted checkpoint.

For each edit:

1. State the desired visual effect, proposed field/IDs, applicability and expected side effects. Read its linked reference before choosing values.
2. Inspect effective inherited rows. Introducing a section can replace the whole master section: preserve required rows, not just the new row. See [inheritance](../format-reference/inheritance.md).
3. Make one small change, or a clearly documented coordinated feature-group change. Record exact before/after values. Do not reuse diagnostic experiment values as universal design settings.
4. Render baseline/checkpoint and candidate with identical controls. Inspect the actual images at native resolution and optionally nearest-neighbor enlargement. Compare front/side; add other poses before accepting a coherent structural change.
5. Accept, revise or revert. Record why and checkpoint accepted outputs. Numerical changes or differing hashes alone do not establish visual improvement.

For example, a broad-headed reference suggests trying the [head controls](../visual-editing/head-ball.md), then inspecting eye spacing, muzzle, ears and attachments in front/side views. It does not justify moving only the master head ball or using a universal enlargement amount. For ear or tail changes, reshape the existing native nodes and attached details using the [researched recipes](../visual-editing/existing-ears-and-tail.md). Existing attachment parents and native joint structure must remain; a connected replacement silhouette does not preserve those relationships.

Select coat/eye palette values by rendering candidate swatches on the actual host and lighting/texture setup. There is no complete validated palette-to-color guide here. Texture, shading and color profiles affect appearance; do not infer a palette index directly from a photograph's RGB value.

## 5. Diagnose failures without losing the design task

If an edit is invisible, inspect diagnostics, effective sections, selected variation/cache, visibility, size, groups, texture eligibility and occlusion using [visibility](../visual-editing/visibility.md). Confirm a positive control changes the intended feature. Do not repeatedly increase a number without identifying what it controls.

If comparisons drift, start fresh requests with identical controls and inspect [texture state](../format-reference/texture-state.md) and [connector randomness](../format-reference/connector-state.md). Fresh stills do not prove retained animation behavior. If the reference is a native game capture, use [native comparison controls](../docs/native-comparison-controls.md) before attributing color or scale differences to the breed.

Use the existing control reference before investigating uncertainty. Repeating established mechanics is not part of routine authoring. If a needed anatomy recipe is missing, record the baseline, target feature, relevant effective rows and specific unanswered question for shared research; retain the anatomy and mark that feature unresolved. A supported approximation must also preserve the existing anatomy. Do not silently expand the task into renderer repair or exhaustive research. Any renderer fix requires its own applicable checkout instructions, reproducer and regression checks.

## 6. Review and deliver

Review the final result against the image and the task's priorities. Use the [delivery checklist and trial report](trial-report.md). Include front/side standing, sitting/lying and feature-revealing views where supported. Look for detached features, clipping, gaps, connector widths, unintended missing parts and markings crossing unsuitable surfaces. Compare ball counts/order, omissions, attachment parents, Linez endpoint pairs, texture references and variations against the base. Reject hidden/recreated ears or tails and blanket stock-detail omissions.

A single fixed seed/age is a prototype scope. If the requested breed includes variation, growth or native installation, validate those separately where tools permit, or list them as untested. Do not claim that a rendered LNZ prototype is a packaged installable breed. Give the receiving user the editable artifact's private location, dependencies, settings, known mismatches and next steps.

Complete the pain-point report even if blocked. The trial is testing whether this guide supports authoring; a documented obstacle is useful evidence, and should not be disguised as a completed feature.
