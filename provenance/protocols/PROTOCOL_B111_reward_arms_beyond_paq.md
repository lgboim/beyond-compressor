# Protocol B111: does the generator's reward change the gain beyond paq8px? (released reward-ablation arms)

Frozen before any B111 checkpoint is scored. Inference only (Modal A10G), no training. Approved by Ariel 2026-09-29.

Arms at 1M, round 8191, first 4 sorted seeds that have learner_8191: canonical (the 1M ladder, `1M/seed-*`),
signed, shuffle, last_step, loss_delta, negate (`ablations/reward-arms/<arm>/seed-*`), and uniform
(`baselines/uniform-prior/1M/seed-*`). Scoring, rows, labels, paq8px bits and mixture exactly as B110; 4-seed
probability ensembles. Gates as B110 (arrays, rows) plus parity: the canonical arm's single-seed own loss on the
labels also saved in Battery 97 (1M, p1) within 1e-4 per seed.

Predictions:
- W1: G <= 0.002 in at least 54 of the 56 cells (7 arms x 8 T labels).
- W2: on both CIFAR-10 layouts, the canonical arm's G exceeds both the negate and the uniform arm's G (4 comparisons,
  all must hold).
- W3: on cifar10_rgb_hwc, Spearman(own loss E4, G) across the 7 arms <= -0.6.
Realized gains of this combiner only. Failed predictions are reported. Output runs/battery/battery111.json.
