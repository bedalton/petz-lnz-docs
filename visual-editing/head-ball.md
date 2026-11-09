# Editing a head ball is not reshaping the whole head

Initial Petz 4 evidence: [BALL-001](../experiments/ball-001.md). Renderer-observed only; tested on Scottie and Siamese.

The master resources identify Dogz head ball 52 and Catz head ball 24. Changing only that ball's size or position can expose gaps between the head circle and facial features. For a coherent larger or repositioned head, investigate group-wide controls such as Head Enlargement and the associated feature balls before recommending individual-ball edits.

Ball Size Override sets a static diameter adjustment, subsequently combined with animated sizing and scale. It is not a final pixel diameter. Move uses a rotated local vector, with an optional reference-ball column; screen-space direction cannot be assumed from the sign alone.

Use a controlled copy, fixed seed/age/fatness, and several camera angles. Preserve inherited section rows when experimenting; the renderer replaces complete sections during master/breed merging. These initial recipes do not yet establish safe full-head transformations.
