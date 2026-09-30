# Protocol B109: is the learners' image residual beyond paq8px special to self-play?

Frozen before any B109 number is computed. Saved artifacts only. No inference or cloud.

Question: would any competent predictor with errors different from paq8px's realize a similar gain? Reference:
V_auto, our frozen hand-built online predictor (no offline fitting), whose own loss on these images is close to the
learners' (cifar hwc 5.055 vs ensemble 5.034 bits per byte, Battery 94 T3).

Row sets with per-byte V_auto on the same rows: cifar10_rgb_hwc and cifar10_rgb_planar (runs/battery/b80/a), and
fashion_mnist (runs/battery/b87/methods). Learners and paq8px as in Battery 107.

Measures (fixed-share, share 0.001, K members, weights start at 1/K, redistribution share/K):
- G_L = M(paq) - M(paq, learners); G_V = M(paq) - M(paq, V_auto) (M(paq) = paq8px alone);
- G_L|V = M(paq, V_auto) - M(paq, V_auto, learners): what the learners add beyond both.

Predictions:
- R1: G_V >= 0.5 G_L on at least 2 of the 3 sets (a hand-built online predictor realizes comparable gain).
- R2: G_L|V <= 0.5 G_L on at least 2 of the 3 sets (at least half of the learners' residual is shared with V_auto).
Failed predictions are reported. Realized gains of these combiners only. Runner `probe/battery109.py`; output
`runs/battery/battery109.json`.
