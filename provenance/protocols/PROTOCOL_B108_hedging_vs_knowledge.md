# Protocol B108: is the learners' small gain beyond paq8px on images hedging or specific prediction?

Frozen before any B108 number is computed. Saved artifacts only (the Battery 107 inputs: cifar10_rgb_hwc,
cifar10_rgb_planar, fashion_mnist, kmnist_images; aligned windows). No inference or cloud.

## Dumb experts (no knowledge of images)

- U: uniform, p = 1/256 for every byte.
- Z: causal order-0 counts within the window, p_t(x) = (c_t(x) + 0.5) / (t + 128), c_t the count of x in bytes
  0..t-1 of the same window.

## Measures

G_x = mean[-log2 q - bits of M_0.001(x, q)] (Battery 100 two-member rule, share 0.001) for x in {learners, U, Z},
q = paq8px. Big-jump bytes: |x_t - x_{t-s}| > 32 with the Battery 107 strides; at these bytes, the median of
p_learner(true byte), p_paq(true byte) and p_Z(true byte).

## Predictions

- K1: G_learners > max(G_U, G_Z) on at least 3 of the 4 image row sets (the learners give more than flat or
  frequency hedging).
- K2: at big-jump bytes, the median learner probability of the true byte exceeds 4/256 on at least 3 of the 4
  sets (more specific than a flat hedge).
- K3: at big-jump bytes, the median learner probability of the true byte exceeds the median paq8px probability on
  at least 3 of the 4 sets.
Interpretation fixed now: K1 and K2 passing indicate specific predictive content at those bytes beyond hedging;
failing indicates that hedging alone accounts for a comparable gain. Neither identifies a mechanism. Failed
predictions are reported. Runner `probe/battery108.py`; output `runs/battery/battery108.json`.
