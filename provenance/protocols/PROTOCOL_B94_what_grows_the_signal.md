# Protocol B94: what increases the learners' non-redundant signal?

Frozen before any B94 number is computed. Saved artifacts only: per-byte learner probabilities
(`runs/battery/b75/p/`), per-byte V_match (`runs/battery/b86/V_match__*.npz`) and per-byte V_auto
(`runs/battery/b80/a/V_auto__*.npz`). No inference, training, cloud or download.

Mixture: the Battery 86 fixed-share rule generalized to K members (share 0.01, weights start at 1/K,
redistribution share/K); for K = 2 it is the Battery 86 C_mix exactly. "Ensemble" is the probability average
over the stated seeds at the label's published-minimum configuration (`probe.b85_modal._ens`, B75 seeds)
unless stated. Row intervals: `probe.battery75.ci`, seed 940.

Disclosure: the idea that the signal concentrates in formal and symbolic data came from the Battery 86
per-label gains relative to V_match, which we had seen. T3 re-tests it against a stronger reference, so it is
not a blind test of the pattern; the group assignment below is fixed now, before any T3 value.

## T1: combining self-play rounds

Labels with 8 common seeds at 24M saved at both the published-minimum round and round 8191: dclm_ranked (768),
arithmetic (5888), audio_8bit (5888), audio_16bit (5376), mutopia_melody_16th (5376).
X = M(early, V_match) - M(early, late, V_match), bits per byte.
- Q1: X >= 0.005 on at least 3 of the 5 labels.

## T2: number of seeds

All 26 labels at the published-minimum configuration, nested seed subsets k = 1, 2, 4, 8 (first k of the B75
seed list). G_k = V_match - M(ensemble_k, V_match). G_8 must equal the Battery 86 value (parity gate, 1e-12).
- Q2a: G_8 > G_1 on at least 22 of 26 labels.
- Q2b: the median over labels of G_8 - G_1 is at least 0.01 bits per byte.

## T3: a stricter reference

G_both = M(V_auto, V_match) - M(ensemble, V_auto, V_match): what the learners add beyond both of our online
predictors. Groups fixed now:
- F, formal and symbolic: metamath, aitdcc_b_c_source, llm_compression_python, llm_compression_arxiv_math,
  mutopia_melody_16th.
- N, natural-language text: dclm, dclm_ranked, llm_compression_cc, kolmogorov_text.
- W, raw waveforms: audio_8bit, audio_16bit, musicnet_pcm8, musicnet_pcm8_11khz, esc50_pcm8,
  esc50_pcm8_11khz, speech_commands_pcm8, speech_commands_pcm8_8khz.
- I, images: cifar10_rgb_hwc, cifar10_rgb_planar.
- O, other: dna, kolmogorov_dna, aitdcc_a_protein, aitdcc_d_glibc_rand, aitdcc_e_atlas_float32,
  aitdcc_g_astronomy, arithmetic.
Predictions:
- Q3a: median G_both over F exceeds the median over W by at least 0.03 bits per byte.
- Q3b: G_both > 0.02 on at least 4 of the 5 F labels.
- Q3c: G_both < 0.05 on both image labels (the image gain relative to V_match is mostly structure V_auto has).

## Reporting

Failed predictions are reported. G measures information the learners add to the stated online predictors on
these rows; it does not separate prior knowledge from in-window mechanisms and says nothing beyond 24M.
Output `runs/battery/battery94.json`; runner `probe/battery94.py` (`t1`, `t2`, `t3` run as separate
processes, then `summary`).
