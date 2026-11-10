The renderer you experiment with (petz-native, via the Petz Render MCP) changed
in commits `c6f1eda` and `b3dc464`. Re-check old findings and experiments in the
areas below. Some "no effect" or "looks like X" conclusions came from renderer
gaps or a bug, not from the game. Re-run the experiments after the MCP is updated,
and mark each affected finding as confirmed, corrected or withdrawn.

## 1. [Paint Ballz] texture column (10th value): previously ignored, now drawn
- A paint ball is textured when the texture loaded and its colour (after any group
  paint override and the host's depth shade) is in the shading ramp [10, 149].
  Colours outside the ramp (e.g. 244 black; LNZ 0 remaps to 244) stay flat.
- A textured paint ball draws texture over its whole visible area. Its outline
  colour and outline-type columns then have no visible effect. Untextured paint
  balls still use them.
- Its texture turns with the host ball when the host's own texture rotates.
- Re-check: any finding that the paint-ball texture column "does nothing", and any
  conclusion about outline columns drawn from textured paint balls.

## 2. [Lnz Version]
- When it is missing from the breed file and from everything it chains to, the
  version is below 2. Then each paint ball's texture t is replaced by the
  [Ballz Info] texture of ball number t, read after [Color Info Override].
  Texture 3 on a paint ball then means "whatever texture ball 3 has", or none.
  This is the original's behaviour (a kept quirk), not a port bug.
- Already true before this change, still relevant: the body-area sections
  ([Body Balls], [Head Balls] ...) are only read when the version is above 1
  (or species is 0).
- Re-check: experiments on edited files without [Lnz Version], especially
  surprising paint-ball textures.

## 3. [Ballz Info] / [Add Ball] outline types >= 1 with a texture
- The interior of an Outline-style ball is now textured. Previously it was flat
  fill colour.
- Outline type 1 (thickness 0): only each row's end pixels are outline colour.
- Outline type n >= 2: a ring of n-1 px, with the poles solid outline colour.
- When 2*(n-1) >= the ball's drawn diameter, the whole ball is outline colour.
- The ring is now drawn exactly as the original draws it. Thick rings on fuzzy
  balls may differ from earlier renders by a pixel.
- Re-check: anything documented about textures being lost on outlined balls, and
  outline thickness versus ball size.

## 4. Clipping at a ball's edge (paint balls, irises)
- Paint balls and the iris are clipped to their host ball. The clip shrinks by
  the host's ring thickness only when the host is Outline style (type >= 1:
  inset = type - 1). Normal, Emboss and other styles don't shrink it at all.
- The old renderer wrongly shrank non-Outline hosts by 1 px. So paint balls near
  the rim (and irises on non-Outline eye-whites) now reach 1 px further.
- Re-check: rim-placement findings for flat-mode markings (11th value 0) and paw
  pads near the edge, and iris/eye-white measurements.

## 5. [Project Ball] entries naming an add ball: previously ignored, now applied
- Line format: ballA, ballB, percent.
- When either ball is an add ball (index >= 67 for both dogs and cats; add balls
  are numbered from 67 in [Add Ball] order), ballB is moved every frame to
  ballA + (ballB - ballA) * percent / 100 per axis (integer, truncated).
  This happens before head rotation.
- percent 100 leaves B alone, 0 puts it on A, and values over 100 push it past.
- An entry whose ballA is an add ball that isn't currently placed pulls B toward
  a far-off sentinel position. Avoid this in tests, or document it as odd.
- Moving balls changes the pose's depth range, so the depth shading of every
  ball can shift a little.
- Entries naming two real balls behave as before (applied once to the animation).
- Re-check: any finding that add-ball project entries "have no effect".
  20 stock files use them (e.g. Great Dane `58, 83, 50` and `15, 89, 86`;
  Tabby has 34).

## 6. Painted (group-coloured) paint balls
- A painted paint ball's texture is now retinted to the painted colour.

## Still not rendered (no "no effect" conclusion is valid for these yet)
- Clothing: [Flat Clothing], [Add Clothing], [Adjust Clothing].
- [Head Shot] and [Little one].
- [Fur Markings] and [Fur Color Areas]: genetics/breeding, which don't affect how
  an existing pet is drawn.
- A one-pixel edge case for flat-mode paint balls whose previous position was
  off the top or left of the screen.

## Sample pets for regression checks
- Frisky (Maine Coon), Homebody (Persian), Fuzzkin (Pomeranian): muzzle paint
  balls are now textured.
- Goobe (Great Dane): add-ball project entries.
- Chip (Scottie): unchanged.
- There is no Dalmatian or Calico sample, and those breeds have the most
  textured paint balls.