# Choose head controls by the desired effect

Evidence: Petz 4 Scottie/Siamese [BALL-001](../experiments/ball-001.md) and [HEAD-001](../experiments/head-001.md). Renderer-observed only. These are starting procedures, not a completed concept-to-breed recipe.

| Desired effect | Starting control | Check before accepting |
| --- | --- | --- |
| Change the head base circle only | Ball Size Override on Dogz 52 / Catz 24 | Facial features may no longer sit naturally on the circle |
| Larger head-area balls and more spread-out features | Increase first Head Enlargement row relative to baseline | Front/side spacing, eyes, muzzle connections, ears and attached details |
| Larger head-area balls with tighter feature spacing | Increase second Head Enlargement row relative to baseline | Eye crowding and overlap; this was visibly strong in the test |
| Reposition an entire head | Identify and move the required feature group; workflow pending | Moving only ball 52/24 leaves facial features behind |

Read [Head Enlargement field behavior](../format-reference/head-enlargement.md) first: its rows combine differently for radii and spacing, and spacing has conditional gates. Ball Size Override sets a static diameter adjustment, not a final pixel diameter. Move uses a rotated local vector with an optional reference-ball column; screen-space direction cannot be assumed from sign alone.

Use a private copy, preserve effective section rows, record the baseline pair and hold seed/age/fatness fixed. Test one control at a time and compare aligned front and side views. The +25 increments in HEAD-001 are diagnostic probes, not recommended universal design increments. Check sitting/lying and added details before delivering a breed; those edited views have numerical but not visual coverage in HEAD-001.
