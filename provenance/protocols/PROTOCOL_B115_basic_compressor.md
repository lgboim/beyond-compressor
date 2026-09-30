# Protocol B115: a basic compressor that absorbs the learners - which cold-start fixes to lpaq1 are needed

Frozen before any B115 learner gain (G) is computed. Local CPU only; no model inference or training. Motivated by
B113 (post hoc: the learners' gain beyond lpaq1 sits in the first 512 positions and at early repeat hits) and B114
(paq8px's order-n, match and word groups already leave the learners at the floor). Seen before freezing: a smoke test
on 3 metamath windows (own code lengths only: U0 1.3485, UA 1.2524 bits per byte; U0 per-byte bits equal B104 L5
exactly; every variant decompresses to the input).

## Instrument

`probe/b115_lpaq/lpaq1_b115.cpp`: the B104 logging lpaq1 (mask 127, all components on) with five switchable
upgrades (`LPAQ_UP` bitmask; 0 = original lpaq1, byte-identical). Each is a complete, self-consistent compressor
(encoder and decoder share the change); nothing is masked.

- U1 (1): mixer weights start at 0.3 instead of 0.
- U2 (2): match-model confidence is learned per match length and bit, not also per previous byte.
- U3 (4): the mixer's weight set is selected by the order/match-length state only (8 sets), not also by 3 bits of
  the previous byte (80 sets).
- U4 (8): an eighth mixer input, an order-0 bit-history context.
- U5 (16): mixer learning rate x3 for the first 4096 coded bits (512 bytes), then the original rate.

Variants: U0 (0), each single upgrade (1, 2, 4, 8, 16), all (UA, 31), and all-but-one (30, 29, 27, 23, 15).
Memory option 4; one process per window.

## Rows and measures

Primary: all Battery 88 rows of the eight labels T (metamath, aitdcc_b_c_source, llm_compression_python,
llm_compression_arxiv_math, dclm, llm_compression_cc, kolmogorov_text, dclm_ranked), learners = evaluated ensembles
(Battery 98 configuration). Secondary (held out from all compressor development): the four Battery 106 text-like
sources (gutenberg_en, rust_ripgrep, js_lodash, json_countries), learners = E24 (mean of the eight Battery 106 seed
files). Windows whose logged bytes equal the raw window. H = own mean code length; G = the learners' realized gain
beyond the variant (two-expert fixed share 0.001, the paper's scorer); early part G_512 = the sum over positions
t < 512 of per-byte gain, divided by 4095.

## Gate

G0: U0's per-byte code lengths equal Battery 104 L5 exactly on every primary row; otherwise inadmissible.

## Predictions

- P1: UA has lower G than U0 on all 8 primary labels.
- P2: UA gives G <= 0.002 on at least 6 of 8 primary labels.
- P3: the reduction of G_512 (U0 minus UA) is at least 70% of the reduction of G on at least 6 of 8 primary labels.
- P4: among the five single upgrades, U2 gives the largest reduction of G averaged over the 8 primary labels.
- P5 (secondary): UA gives G <= 0.002 on at least 3 of the 4 held-out sources.

Everything else (H, all-but-one variants) is descriptive. Failed predictions are reported. Runner
`probe/battery115.py`; output `runs/battery/battery115.json`.
