# Protocol B98: what do the learners add beyond paq8px, byte by byte?

Frozen before any B98 output exists. Cloud CPU compression of the Battery 88 windows (all 34 row sets) with
paq8px at the Battery 88 commit c84f576fc2c522194cd320743708652a154daf6b, level -8, one file per window, with a
logging-only patch to `Encoder::compressByte` (`probe/b98_paq/Encoder.cpp`): for every coded byte it records
whether the main predictor coded it, the byte, and the sum over its 8 bits of -log2 of the probability the
arithmetic coder used. Coding itself is unchanged. No inference or training.

## Gates

- Every compressed size equals the Battery 88 size for the same window (the patch does not change coding).
- The logged code length of a window never exceeds 8 x its compressed size.
- A window is used only if the bytes coded by the main predictor equal the window bytes in order (no transform
  or reordering); the number of aligned windows per row set is reported.

## Measures

p_paq(byte) = 2^(-logged bits). M: the Battery 94 fixed-share rule. Ensembles: published-minimum
configuration with all saved seeds (benchmark) and E24 (the eight B87 sources).
- G_paq = mean[-log2 p_paq - bits of M(ensemble, p_paq)]: what the learners add beyond paq8px.
- G_all = M(p_paq, V_auto, V_match) - M(ensemble, p_paq, V_auto, V_match), benchmark labels.
- G_both on the same aligned rows, for comparison with Battery 94 T3.
These are realized complementarity of this combiner, not identified unique information.

## Predictions (benchmark labels; groups as in Battery 94)

- R1: G_paq > 0.01 bits per byte on at least 8 of 26 labels.
- R2: the median G_paq over group F exceeds the median over group W by more than 0.005.
- R3: G_paq <= G_both on at least 22 of 26 labels (paq8px leaves less for the learners to add than our two
  predictors).

The eight B87 sources are reported descriptively. Failed predictions are reported. Runner `probe/b98_modal.py`
(`score` on Modal, then `analyze`); output `runs/battery/battery98.json`.
