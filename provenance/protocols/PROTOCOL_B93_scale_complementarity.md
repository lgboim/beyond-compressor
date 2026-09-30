# Protocol B93: does the learners' non-redundant signal grow with model size?

Frozen before any B93 number is computed. Saved artifacts only: per-byte learner probabilities in
`runs/battery/b75/p/` and per-byte V_match code lengths in `runs/battery/b86/V_match__<label>.npz`.
No inference, no training, no cloud, no download.

## Question

The most frequent public question about Cowsik et al. (2026) is whether the result improves with scale.
Battery 91 found that extrapolating the loss curve is unreliable. B93 asks a narrower question that the
saved data can answer: does the part of the learners' prediction that an online predictor (V_match) lacks
grow with learner size?

## Measures (per label and learner configuration, on identical rows)

- E: ensemble log loss (probability average over the stated seeds; authors' definition), bits per byte.
- V: V_match code length (Battery 86 arrays).
- M: C_mix, the Battery 86 two-member fixed-share mixture (share 0.01, weights start at 1/2, no fitting),
  code copied from `probe/b85_modal.py::summary86`.
- G = V - M: complementarity gain, the bits per byte the learner adds to V_match. G >= 0 up to mixture
  regret; G near 0 means the learner adds nothing V_match lacks.
- Position split: G and E restricted to positions 0-15, 16-255 and 256-4094 of each 4095-byte window.
- Row intervals: paired row bootstrap, `probe.battery75.ci` (2000 draws, seed 930).

## Comparisons

- S (primary, size at the final round 8191): 100k against 24M on the 8 labels with both saved:
  arithmetic, audio_16bit, audio_8bit, dclm_ranked, dna, mutopia_melody_16th (the 8 seeds saved for both
  sizes), musicnet_pcm8, musicnet_pcm8_11khz (seed-40354564 only, the one 24M seed saved).
- L (size ladder): musicnet_pcm8 and musicnet_pcm8_11khz, seed-40354564, sizes 100k, 500k, 1M, 3M, 6M, 24M
  at round 8191.
- R (descriptive only, rounds at 24M): dclm_ranked 768 vs 8191; arithmetic and audio_8bit 5888 vs 8191;
  audio_16bit and mutopia_melody_16th 5376 vs 8191 (8 seeds); musicnet_pcm8 1536 vs 8191 (seed-40354564).
  The early round of each pair is the published-minimum round for that label, so it was selected for low
  loss; R is selection-confounded and no hypothesis is tested on it.

## Predictions (stated before scoring)

- P1: G(24M) - G(100k) > 0 on at least 6 of the 8 S labels.
- P2: in L, Spearman correlation between size and G is at least 0.8 on both MusicNet labels.
- P3: at positions 0-15, E(24M) < E(100k) on at least 6 of the 8 S labels (a better prior at the start of a
  window, where no in-window statistics exist yet).
- P4: at positions 0-15, E(24M) < V on at least 6 of the 8 S labels.
- P5: G(24M) - G(100k) is larger on positions 256-4094 than on positions 0-15 on at least 5 of 8 labels
  (growth mostly where context exists).

Failed predictions are reported.

## Interpretation rule (fixed now)

- Growth of G with size means the learners' non-redundant signal relative to V_match grows with size. We
  attribute to prior knowledge (transfer) only growth at positions 0-15. Growth at later positions is
  reported as unresolved between prior knowledge and in-window mechanisms V_match lacks.
- No growth of G with size (P1 fails) means the size-related improvement is redundant with an online
  predictor on these labels.
- Nothing here is compared with paq8px, and no statement about larger models than 24M is made.

## Outputs

`runs/battery/battery93.json` (per label: E, V, M, G and position splits per configuration; S differences
with intervals; L correlations; R values; P1-P5 outcomes). Runner: `probe/battery93.py`.
