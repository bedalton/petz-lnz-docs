# MORPH-007: size-reference resolution boundaries

Date: 2026-11-11. Petz 4 Scottie/Siamese, integration `6c1d88325ced89109f8e4b9d724fa8ab6037b42c`. Parsed synthetic rows appended to immutable in-memory copies of loaded appearances. No breed resources or originals were written; no renderer changes and no new MCP calls. Results are code-supported and renderer-observed, not game-validated.

Two separate gates control relative sizing. Morph evaluation tests whether column15 is negative; attachment tests whether it points to an already assembled ball. A nonnegative unresolved reference therefore suppresses size updates even though it cannot supply a radius. This distinction is narrower than saying only a valid reference suppresses size updates.

For authored size20 at 100% in group15:

| Column15 target | Evaluated size | Result |
| --- | --- | --- |
| -1 or -2 | 20 | Ordinary diameter scaling |
| Real ball0 or head | 0 | Inherits that real ball's radius |
| Earlier active ordinary marker | 0 | Inherits the earlier marker's radius |
| Earlier dormant marker | 0 | Inherits zero radius; target remains unparked and visible |
| Self, later marker, or10000 | 0 | No reference resolution; ordinary zero-size fallback gives radius 0; target remains unparked and visible |

A static group0 size20 control retains evaluated size20. Earlier valid targets add the size contribution using the relative shift by8. Self/later/out-of-range targets instead use ordinary scaling with shift9. Neither case automatically retries the reference after later balls are assembled. Negative authored sizes and zero are also covered; all calculated radii clamp to0–64. These are current implementation boundaries, not recommended native-file encodings.

The1,728 numerical cases span two species ×three named poses ×two earlier-marker states ×eight reference choices ×three sizes(-20/0/20) ×six group/amount settings(static group0 at 100%, group15 at 0/1/25/50/100%). Every record checks the independently calculated size/radius, offset scaling, parked/visible flags and earlier-marker state. Group15 is verified unused before appending; earlier dormant marker uses otherwise-unused14. Fatness is50; seed0, age100 and yaw0. Row parsing preserves every reference token. Existing game projections are checked not to target the appended IDs.

Seventy-two direct fresh-state rasters cover activated group15 size20 for head/earlier/self/later/out-of-range/ordinary references under both earlier-marker states, in all six species/pose fixtures. All self/later/out-of-range triples match within each fixture/state. Common XY bounds preserve alignment. Raster RNG and connector RNG reset to1, step0; host/paint state is fresh for each draw. These draws are explicit activation controls; [MORPH-006](morph-006.md) supplies separate default-state MCP provenance, not MCP validation of this expanded matrix.

Two private standing contact sheets were reviewed at native resolution: both species show the large head-radius probe, smaller earlier-marker-radius probe, and absent zero-radius probe; the earlier dormant-reference case hides both earlier marker and target while leaving the independent later marker visible. The targeted comparisons support the numerical visibility distinction without assigning anatomy semantics to synthetic balls.

Run `scratch/petz-local-x86-venv/bin/python tools/morph_reference_boundaries.py`; refuses existing output. `--verify` reloads every stock fixture and repeats all 1,728 calculations and 72 draws, requiring byte-identical PNGs and report contents. Fresh run and full replay passed. [Manifest](morph-007.json), [script](../tools/morph_reference_boundaries.py); private `scratch/research/morph-007`, reviewed sheet hashes/layout in `review-sheets.json`, logs `scratch/morph-007-{run, verify}.log`. All 62 installed/checkout source hashes, actual revision, dependencies and original breed digests are recorded/checked. The linked MORPH-006 manifest records the shared engines; final session audit checks those hashes again. Added-ID order for chains/cycles, other breeds/versions and native behavior remain separate scope.
