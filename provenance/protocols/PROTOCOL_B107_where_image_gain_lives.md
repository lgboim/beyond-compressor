# Protocol B107: where the learners' small gain beyond paq8px on images sits (saved artifacts only)

Frozen before any B107 number is computed. No inference, cloud or download.

Hypothesis (from B103/B88: the learners beat paq8px clearly only on arithmetic progressions): the realized gain
beyond paq8px on image bytes concentrates at bytes that continue a local arithmetic progression along the pixel
stride.

## Data

Per-byte learner ensemble probabilities and per-byte paq8px code lengths (aligned windows only):
cifar10_rgb_hwc (published-minimum ensemble, B98 bits; stride s = 3), cifar10_rgb_planar (s = 1), fashion_mnist
(E24, B98 bits; s = 1), kmnist_images (E24 from B106, B106 standard-mode bits; s = 1).

## Per-byte gain

g_t = -log2 q_t - b_t, where b_t is the per-byte code length of the Battery 100 two-member mixture (share 0.001)
of learner and paq8px. This is an accounting of where the mixture's savings occur, not a causal attribution
(mixture weights carry information across bytes).

## Byte classes (by the preceding bytes only), for t >= 2s

- K (constant): x_t = x_{t-s} = x_{t-2s}.
- A (arithmetic continuation, non-constant): x_{t-s} != x_{t-2s} and |x_t - (2 x_{t-s} - x_{t-2s})| <= 1, differences
  taken as integers (no wrap).
- O (other): all remaining bytes with t >= 2s.

## Predictions

- W1: on cifar10_rgb_hwc, mean g over A bytes is at least 2 times the mean g over O bytes.
- W2: the share of total gain carried by A bytes exceeds the A share of bytes by a factor of at least 1.5 on at
  least 3 of the 4 image row sets.
- W3: mean g over K bytes is below mean g over A bytes on at least 3 of the 4 row sets.
Failed predictions are reported. Runner `probe/battery107.py`; output `runs/battery/battery107.json`.
