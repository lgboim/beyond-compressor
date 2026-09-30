# Protocol B95: is the seed effect of Battery 94 calibration or knowledge?

Frozen before any B95 number is computed. Saved artifacts only (as in Battery 94). No inference, training,
cloud or download.

## Background and limit

Battery 94 T2: the learners' non-redundant signal G_k = V_match - M(ensemble_k, V_match) grows with the number
of averaged seeds k (median G_8 - G_1 = 0.024 bits per byte). Averaging can add knowledge or only temper
overconfident single-seed probabilities. Only p(true byte) is saved, so temperature scaling (which needs the
full distribution) is not possible here. B95 tests the part of miscalibration that p(true) can address:
probability mass too close to zero on the true byte. A negative result does not rule out moderate
(temperature-like) miscalibration.

## Definitions

Mixture M: the Battery 94 K-member fixed-share rule (share 0.01; K = 2 is Battery 86 C_mix). u: the uniform
byte distribution, p = 1/256 on every byte. Published-minimum configuration and B75 seeds as in Battery 94.
Single-seed quantities are averaged over all 8 seeds (each seed alone), not the first seed only.

- Raw: G_1 = mean over seeds s of [V - M(p_s, V)]; G_8 = V - M(p_ens8, V).
- Floor: F_1 = mean over s of [M(u, V) - M(p_s, u, V)]; F_8 = M(u, V) - M(p_ens8, u, V). With u in the mixture,
  a single seed's near-zero probabilities are bounded by the mixture's floor.
- R = (F_8 - F_1) / (G_8 - G_1), per label with G_8 - G_1 > 0.005: the share of the seed effect left after the
  floor.
- Decomposition (first seed): per byte d = bits of M(p_s0, V) - bits of M(p_ens8, V); share of sum(d) coming from
  bytes with p_s0(true) < 0.01.

## Predictions

- C1: the median of R over eligible labels is at least 0.5 (most of the seed effect is not near-zero
  overconfidence).
- C2: F_8 > F_1 on at least 22 of 26 labels.
- C3: the median over labels of the share of the first-seed-to-ensemble gain from bytes with p_s0(true) < 0.01
  is below 0.5.

## Interpretation (fixed now)

R near 1 and C3 holding: the seed effect is not explained by near-zero overconfidence; it is consistent with
additional knowledge or with moderate miscalibration, which B95 cannot separate. R near 0: the seed effect is
mostly the floor, i.e. single seeds are overconfident rather than less knowledgeable. Failed predictions are
reported. Output `runs/battery/battery95.json`; runner `probe/battery95.py` (4 parallel parts, then summary).
