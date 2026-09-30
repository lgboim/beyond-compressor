# Protocol B102: gain beyond paq8px along self-play compute, and self-play versus the fixed prior

Frozen before any B102 output exists. Inference only of released checkpoints (Modal A10G, the authors'
`score_from_hf.py` functions `load_corpora`, `model_arch`, `seed_probs`, unchanged). Labels (Battery 75 inputs,
first 256 rows): cifar10_rgb_hwc, cifar10_rgb_planar, musicnet_pcm8, audio_8bit, metamath, dclm. paq8px per-byte
code lengths from Battery 98 (all windows of these labels aligned).

## Checkpoints

- A (compute axis): self-play 24M at rounds 0, 256, 512, 1024, 2048, 4096, 6144, 8191; the 8 released seeds.
- B (fixed prior): `baselines/uniform-prior/{3M,6M}` at round 8191, the 4 released seeds, against the first 4
  sorted self-play seeds at the same size and round (Battery 97 files).

## Measures

G_paq = mean[-log2 p_paq - bits of M_0.001(x, p_paq)] (Battery 100 two-member rule, share 0.001; comparator
overhead about 0.001 bits per byte), x = the probability average over the stated seeds. E = x's own loss.
Realized gain of this combiner only.

## Gate

Round-8191 24M probabilities must reproduce Battery 97's saved p_1 on the four shared labels (cifar10_rgb_hwc,
musicnet_pcm8, audio_8bit, metamath): per-label |mean difference| <= 1e-4 bits per byte and per-row maximum
<= 1e-3. If the gate fails, no outcome is reported.

## Predictions

- A1: on cifar10_rgb_hwc, Spearman(round, G_paq) >= 0.8 over rounds 256..8191 (8 seeds).
- A2: on metamath and dclm, G_paq <= 0.002 at every round, 0..8191 (16 cells).
- A3: on musicnet_pcm8 and audio_8bit, G_paq at round 8191 exceeds G_paq at round 256 (both labels).
- B1: on cifar10_rgb_hwc, G_paq of the self-play 4-seed average exceeds that of the fixed-prior 4-seed average
  at both 3M and 6M.
- B2: at 6M, the self-play 4-seed average has lower own loss E than the fixed-prior average on at least 4 of the
  6 labels.

No extrapolation beyond the released range. Failed predictions are reported. Runner `probe/b102_modal.py`
(`run`, then `analyze`); output `runs/battery/battery102.json`.
