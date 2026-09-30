# Protocol B101: gain beyond paq8px as a function of learner size

Frozen before any B101 number is computed. Saved artifacts only: Battery 97 per-byte p_1 for 6 sizes x 8 seeds
at round 8191 on 7 labels, and Battery 98 per-byte paq8px code lengths (all windows of these labels are
aligned). No inference, cloud or download.

G_paq(x) = mean[-log2 p_paq - bits of M_s(x, p_paq)], with M_s the two-member fixed-share rule of Battery 100
(share s = 0.001, comparator overhead about 0.001 bits per byte; s = 0.01 also reported). x is the 8-seed
probability average (k = 8) or a single seed (k = 1, averaged over the 8 seeds). This is the realized gain of
this combiner, not a measure of all information in the model.

## Predictions (s = 0.001, k = 8)

- Z1: on metamath, aitdcc_b_c_source and dclm_ranked, G_paq <= 0.002 at every one of the 6 sizes (18 cells).
- Z2: on cifar10_rgb_hwc, G_paq at 24M exceeds G_paq at 100k by at least 0.005, and the Spearman correlation
  between size and G_paq is at least 0.8.
- Z3: on musicnet_pcm8 and audio_8bit, G_paq at 24M exceeds G_paq at 100k (both labels).
- mutopia_melody_16th (17 rows) is reported descriptively only.

No extrapolation beyond 24M is made. Failed predictions are reported. Output `runs/battery/battery101.json`;
runner `probe/battery101.py` (one process per label, then summary).
