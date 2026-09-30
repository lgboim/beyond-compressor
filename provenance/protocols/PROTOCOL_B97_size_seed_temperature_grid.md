# Protocol B97: size x seed grid with temperature calibration (cloud inference only)

Frozen before any B97 output exists. Inference of released checkpoints only (no training), on Modal GPUs with
the authors' scorer code (`refs/official/scoring/score_from_hf.py`: `load_corpora`, `model_arch`, and the
`seed_probs` model loading, unchanged); only the output step is extended to several temperatures.

## Grid

- Sizes 100k, 500k, 1M, 3M, 6M, 24M at round 8191; the first 8 released seeds of each size in sorted order.
- Labels (first 256 rows, Battery 75 inputs): metamath, aitdcc_b_c_source, dclm_ranked, cifar10_rgb_hwc,
  mutopia_melody_16th, musicnet_pcm8, audio_8bit.
- Per byte and checkpoint: p_1 (temperature 1, the standard probability) and p_cal, an online causal
  temperature calibration: the Battery 94 fixed-share mixture (share 0.01, uniform start) over the same model at
  temperatures T in {0.7, 0.8, 0.9, 1.0, 1.15, 1.35, 1.6, 2.0}, computed in the container from full
  distributions.

## Gate

p_1 must reproduce saved Battery 75 files where they exist (100k r8191 on all 7 labels; 24M r8191 on
dclm_ranked, mutopia_melody_16th, audio_8bit, musicnet_pcm8 seed-40354564): per-label mean absolute difference
<= 1e-4 bits per byte and per-row maximum <= 1e-3 (Battery 75 gate). If the gate fails, no D outcome is
reported.

## Measures and predictions (V = V_match per byte, Battery 86; M = Battery 94 fixed-share rule)

- G_k(size) = V - M(average of k seeds' p_1, V); single-seed values are averaged over the 8 seeds.
- D1 (size curve with seeds): Spearman correlation between size and G_8 >= 0.8 on at least 5 of 7 labels.
- D2 (equal parameter budget): G_8(3M) > G_1(24M) on at least 4 of 7 labels (8 x 3M = 24M parameters; the
  authors' compute proxy counts ensemble members).
- D3 (calibration versus seeds, 24M): share = (G_1cal - G_1) / (G_8 - G_1), where G_1cal uses p_cal. The median
  share over labels with G_8 - G_1 > 0.005 is below 0.5 (temperature calibration explains less than half of the
  seed effect).
- Descriptive: G_8 from calibrated members; G_k for k = 1, 2, 4, 8 at every size; iso-parameter comparisons
  (8 x 100k vs 1M, 2 x 500k vs 1M, 4 x 6M vs 24M).

Temperature calibration covers moderate over- and under-confidence; it does not cover every form of
miscalibration. G is realized complementarity of this combiner, not identified unique information. Failed
predictions are reported. Runner `probe/b97_modal.py` (`run`, then `analyze`); output
`runs/battery/battery97.json`.
