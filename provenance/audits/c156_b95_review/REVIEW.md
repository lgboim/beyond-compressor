# B95 independent saved-output audit

## Numerical verdict

All 690 numeric fields reproduce with maximum absolute discrepancy 1.83e-14. The frozen protocol/runner hashes match their announced values. Source recurrence parity passes on four full-length rows in 52 checks, maximum per-byte error 1.07e-14. All 213 probability arrays, all 26 V_match arrays and row identities match historical audit pins. All four part files combine exactly into the pinned summary, with no duplicate labels.

C1 PASS: median per-label ratio R = 0.9334311914 over 23 eligible labels. Individual ratios range 0.85568810–0.99666861. This is a median of ratios, not a pooled 93% fraction of all saved bits.

C2 PASS: all-seed ensemble floor gain exceeds mean single-seed floor gain on 25/26; arithmetic is the exception.

C3 PASS: median signed low-mask contribution ratio 0.2776668650 over 25 labels. Arithmetic is omitted because its total first-seed-to-ensemble gain is nonpositive. Protein's ratio 12.0162 and pseudorandom's 1.0403 are signed-net decompositions with gains/losses that can cancel, not probabilities or bounded fractions.

## Seed-count correction

The stored G_8/F_8 variables mean ALL saved seeds, not always eight. Protein uses ten; astronomy, DNA and Kolmogorov DNA use nine; the other 22 labels use eight. Raw all-seed G reproduces the independent full-K B86 reconstruction on all 26. G differs from B94's first-eight result on the four disclosed labels. Retain the frozen original and add a versioned, explicit all-K description; do not claim the frozen exactly-eight procedure or its parity passed universally. This audit verifies actual 8–10-seed outcomes; it does not establish what every counterfactual exactly-eight B95 readout would be.

## Interpretation boundaries

The safe result is robustness of the measured ensemble advantage to this particular uniform-expert mixture. It does not distinguish knowledge from calibration, and does not exhaustively rule out near-zero miscalibration.

1. A uniform expert is assigned adaptive mixture weight, not a fixed substantial probability floor. With share 0.01 and three members its guaranteed contribution after a weight update is only 0.01/(3*256) = 0.0000130208333, corresponding to a 16.2288-bit cap from this guarantee alone. At the first byte the uniform initial weight is 1/3. An unchanged effect under this intervention cannot show that every relevant low-probability error has been corrected.
2. The raw comparator already mixes the learner with V_match. That expert may already limit the direct penalty of near-zero learner probabilities, so the extra uniform expert can be redundant as protection. The new expert also changes initialization and share redistribution of the other members. R is an operational contrast, not a fraction of an identified causal mechanism removed.
3. The mask p_s0(true) < 0.01 is not a calibration diagnostic. Uniform probability is 1/256 = 0.00390625, below the cutoff; the cutoff is 2.56 times uniform. Even a perfectly calibrated uniform predictor would put every byte in this mask. In the actual pseudorandom case 99.9818% of bytes are in it. Low realized probability can reflect irreducible uncertainty rather than miscalibration.
4. The decomposition records where signed savings occur. A low-probability observation changes mixture weights and therefore losses on later bytes, so contemporaneous masking does not attribute causation. It also uses only the first seed, whereas G_1 and F_1 are averaged over all saved seeds.
5. Only probabilities of the observed byte were saved. Full-distribution calibration interventions cannot be reconstructed from these scalars alone; neither unique knowledge nor semantic understanding has been measured.

Keep all numerical prediction outcomes, but replace the causal phrase 'the seed effect is not near-zero overconfidence' by 'the observed ensemble advantage largely persists under this specified uniform-expert intervention; its mechanism remains unresolved.'

## Scope

Independent linear-probability recurrence; no owner runner import/execution. No model inference, training, new data, cloud, listener, or modification of runs/refs. Only audit-directory and append-only channel writes. Future protocols B96/B97 are not certified by this completed B93–B95 audit.
