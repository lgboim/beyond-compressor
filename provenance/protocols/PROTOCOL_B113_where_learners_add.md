# Protocol B113: where, byte by byte, the learners add beyond lpaq1, and whether paq8px covers the same bytes

Frozen before any B113 number is computed. Local CPU only; no new model or compressor run. Inputs are saved arrays:
Battery 88 rows (`runs/battery/b88/rows`), Battery 98 per-byte paq8px code lengths (standard mode, commit c84f576,
`probe.b98_modal.load_all`), Battery 104 per-byte lpaq1 code lengths with all components on (`L5`, mask 127, coder
byte-identical to the original lpaq1), and the learners' evaluated ensembles (the Battery 98 configuration,
`probe.battery94.config`, `probe.battery75.P`).

## Rows and quantities

Labels T: metamath, aitdcc_b_c_source, llm_compression_python, llm_compression_arxiv_math, dclm, llm_compression_cc,
kolmogorov_text, dclm_ranked. Windows: those retained by paq8px in Battery 98 (logged bytes equal the raw window).

For a reference R (lpaq1 or paq8px) with per-byte code length b_R(i, t), the per-byte realized gain is
g_R(i, t) = b_R(i, t) - b_M(i, t), where M is the paper's two-expert fixed-share mixture of the learners and R
(share 0.001, equal initial weights); the mean of g_R over bytes is the paper's G. paq8px's per-byte advantage over
lpaq1 is d(i, t) = b_lpaq1(i, t) - b_paq8px(i, t).

## Strata (from the window bytes only)

- A, position: A1 t < 64; A2 64 <= t < 512; A3 512 <= t < 2048; A4 t >= 2048.
- B, byte class of x_t (the seven ASCII labels, i.e. T without dclm_ranked): word-start (x_t in [A-Za-z0-9_] and
  t = 0 or x_{t-1} not in that set), word-internal (both in the set), space (0x20), newline (0x0A or 0x0D), other.
- C, repeat: with the most recent earlier position j < t whose preceding 8 bytes equal x_{t-8..t-1} (t >= 8):
  repeat-hit if x_j = x_t, repeat-miss if x_j != x_t, no-repeat if no such j.

Per stratum and label: share of bytes, share of the label's total sum of g_lpaq1, of g_paq8px and of d, and the mean
per-byte g_lpaq1, g_paq8px and d.

## Predictions

- Q1: A1 + A2 (the first 512 positions, 12.5% of bytes) carry at least 25% of the total g_lpaq1 on at least 6 of 8.
- Q2: A1 + A2 carry at least 25% of the total d on at least 6 of 8.
- Q3: the mean per-byte g_lpaq1 at repeat-hit bytes is below the label's overall mean g_lpaq1 on at least 6 of 8.
- Q4: word-start bytes carry a larger share of the total g_lpaq1 than their share of bytes on at least 5 of 7.
- Q5: the Spearman correlation over a label's retained bytes between g_lpaq1 and d is positive on at least 7 of 8.

Everything else is descriptive. Failed predictions are reported. Runner `probe/battery113.py`; output
`runs/battery/battery113.json`.
