# Protocol B100: the paq8px comparison with low-overhead combiners and pre-assigned bGPT weights

Frozen before any B100 number is computed. Saved artifacts only (Battery 98 per-byte paq8px code lengths on
aligned windows, Battery 99 bGPT probabilities, saved learner ensembles). No inference, cloud or download.

## Why

C1166: the two-expert fixed-share combiner with share 0.01 has a comparator overhead of about 0.0075 bits per
byte, so its negative gains say only that this combiner did not improve on paq8px. B99's post hoc table also
picked the best of three bGPT weights after the fact.

## Combiners

M_s: the Battery 94 fixed-share rule with share s. Comparator overhead for two experts at T = 4095 is at most
1/T + (T-1)/T * -log2(1 - s/2) bits per byte: about 0.00097 for s = 0.001 and 0.00024 for s = 0 (Bayesian
mixture, no switching).
G_paq(x, s) = mean[-log2 p_paq - bits of M_s(x, p_paq)] for x = the learners' ensemble (as in Battery 98) or
bGPT with the weight fixed now by domain:
- text weights: dclm, llm_compression_cc, kolmogorov_text, llm_compression_python, aitdcc_b_c_source,
  llm_compression_arxiv_math, metamath, hewiki, dewiki, go_source, python_docs_html, uci_adult;
- image weights: cifar10_rgb_hwc, cifar10_rgb_planar, fashion_mnist;
- audio weights: audio_8bit, audio_16bit, musicnet_pcm8, musicnet_pcm8_11khz, esc50_pcm8, esc50_pcm8_11khz,
  speech_commands_pcm8, speech_commands_pcm8_8khz, yesno_pcm16;
- no bGPT domain (reported for the learners only): dclm_ranked, dna, kolmogorov_dna, aitdcc_a_protein,
  aitdcc_d_glibc_rand, aitdcc_e_atlas_float32, aitdcc_g_astronomy, arithmetic, mutopia_melody_16th, elf_x86_64.

## Predictions

- L1: for the learners with s = 0.001, G_paq > 0.005 on at most 5 of the 26 benchmark labels.
- L2: for the learners with s = 0, G_paq <= 0.001 on at least 18 of the 26 benchmark labels.
- L3: on every row set with a bGPT domain, G_paq(bGPT, 0.001) exceeds G_paq(learners, 0.001), and by at least
  0.1 bits per byte on at least 15 of the 24 such row sets.

Interpretation fixed now: G_paq measures what a specific online combination gains from adding the model to
paq8px on these windows. A gain near zero with a low-overhead combiner means no such gain was realized; it is
not a proof that the model contains no information paq8px lacks. The bGPT comparison is not size- or
architecture-matched and cannot isolate the effect of natural-data training. Failed predictions are reported.
Output `runs/battery/battery100.json`; runner `probe/battery100.py`.
