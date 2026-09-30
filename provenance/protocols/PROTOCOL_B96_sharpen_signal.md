# Protocol B96: sharpening the learners' non-redundant signal (saved artifacts only)

Frozen before any B96 number is computed. No inference, training, cloud or download. Mixture M: the
Battery 94 K-member fixed-share rule (share 0.01). g (per byte) = bits of M(V_auto, V_match) - bits of
M(ensemble, V_auto, V_match), the strict gain of Battery 94 T3; G_both is its mean. This is realized
complementarity of this combiner, not identified unique information (C1158, C1159). Row intervals:
`probe.battery75.ci`, seed 960.

## S1: out-of-sample test of the formal-data pattern (eight Battery 87 sources)

Inputs: `runs/battery/b87/learners/E24_probs__<src>.npy` (E24 ensemble, p of true byte),
`runs/battery/b87/methods/V_match__<src>.npy` and `V_auto__<src>.npy` (bits). G_both has never been computed on
these sources. Groups fixed now: code/markup {go_source, python_docs_html}; natural text {hewiki, dewiki};
waveform {yesno_pcm16}; image {fashion_mnist}; other {elf_x86_64, uci_adult}.
- S1a: min(G_both of go_source, python_docs_html) > max(G_both of hewiki, dewiki).
- S1b: mean G_both over code/markup minus G_both of yesno_pcm16 >= 0.03 bits per byte.
- S1c: G_both of fashion_mnist > 0.02.

## S2: where the gain sits in formal data (delimiters and nesting)

Labels: aitdcc_b_c_source, llm_compression_python, llm_compression_arxiv_math, metamath (published-minimum
ensembles, all saved seeds, rows as in `probe/b85_modal.py::_rows`) and go_source (E24, Battery 87 rows).
Opening delimiters ( [ {; closing ) ] }. Depth before a byte: running count within the window, +1 after an
opening, -1 after a closing, floored at 0.
Ratios use per-byte g: r_close = mean g on closing bytes / mean g on all bytes; r_open likewise.
- S2a: r_close >= 2 on at least 3 of the 5 labels.
- S2b: mean g on closing bytes with depth before >= 2 exceeds that with depth before = 1 on at least 3 of 5.
- S2c: r_close > r_open on at least 3 of 5.
Per-byte attribution is accounting, not causal (mixture weights carry over between bytes).

## S3: shape of the seed curve

All 26 labels, published-minimum configuration, all saved seeds (8-10). For k = 1..8, G(k) = mean over
subsets of V_match - M(ensemble of the subset, V_match): all subsets when there are at most 8, else 8 random
subsets (numpy seed 960). Labels with G(8) > 0.02 are eligible.
- S3a: G(8) - G(4) >= G(4) - G(2) on at least half of the eligible labels (no diminishing return in log k
  within 1..8).
- Descriptive: least-squares fit G(k) = a - b/k on k = 1..8; a reported only where R^2 >= 0.9, as an
  in-range description, not a forecast beyond 8.

Failed predictions are reported. Output `runs/battery/battery96.json`; runner `probe/battery96.py`
(parts s1, s2, s3a..s3f in parallel, then summary).
