# Protocol B110: does the gain beyond paq8px track the generator's progress? (released curriculum learners)

Frozen before any B110 checkpoint is scored. Inference only (Modal A10G), no training. Approved by Ariel 2026-09-29.

Question (Discussion hypothesis): in the authors' Figure 3, epiplexity of the generator's outputs rises from
generator round 1024 to 4096 while 1M learners trained on those outputs stop improving on DCLM and keep improving
on planar CIFAR-10. Does the realized gain beyond paq8px follow the same split?

Learners: released `curriculum/<arm>_seed-*/learner_4095.pth` (1M architecture), arms G0, T256, T512, T1024, T2048,
T4096, all 8 released seeds each; scored with the authors' `seed_probs` unchanged (as B102). Rows: the first 256
rows of each label in runs/battery/b75/modal_data, identical to B98. Labels: the eight T labels (metamath,
aitdcc_b_c_source, llm_compression_python, llm_compression_arxiv_math, dclm, llm_compression_cc, kolmogorov_text,
dclm_ranked) and cifar10_rgb_hwc, cifar10_rgb_planar, audio_8bit, musicnet_pcm8.
Measure: G = mean[-log2 q - bits of M_0.001(q, p_ens8)], Battery 100 two-member rule, standard-mode paq8px per-byte
bits from B98 (identical to forced mode on the T labels), retained rows only. Own loss E8 of each ensemble reported.

Gates (fail closed; a failure makes outcomes inadmissible): 48 checkpoints, 8 per arm; arrays [256, 4095] finite in
(0, 1]; row count equals B98 retained rows per label; parity: for G0/T4096 own-loss on dclm and cifar10_rgb_planar
within 0.01 of the authors' Figure 3 ensemble_K8 values (8.18394/4.94678 and 8.42626/6.12245) — these use the
authors' own held-out rows, so a mismatch beyond 0.3 fails the gate and 0.01-0.3 is reported as a row difference.

Predictions:
- C1: G <= 0.002 in at least 46 of the 48 cells (6 arms x 8 T labels).
- C2: on both CIFAR-10 layouts, G(T4096) > G(G0).
- C3: on cifar10_rgb_planar, Spearman(T, G) over the six arms (G0 as T = 0) >= 0.8.
- C4: on at least 7 of the 8 T labels, max minus min of G over the six arms is <= 0.001.
Realized gains of this combiner only; not a measure of information. Failed predictions are reported.
Runner probe/b110_modal.py (shared with B111); output runs/battery/battery110.json.
