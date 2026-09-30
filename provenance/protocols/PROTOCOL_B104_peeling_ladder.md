# Protocol B104: a peeling ladder - the simplest context-mixing compressor after which the learners add nothing

Frozen before any B104 number is computed. Local CPU only (no inference, cloud or download beyond the lpaq1
source already fetched: mattmahoney.net/dc/lpaq1.zip, SHA-256 e4b54c3e03d3217c87d12c0ee20c4e756cd9bafd893583c4e326b043d57e3b47,
GPL). Learner probabilities and rows are the saved Battery 88/98 inputs.

## Instrument

lpaq1 (Mahoney 2007) with a logging-and-masking patch (`probe/b104_lpaq/lpaq1_b104.cpp`): an environment mask
switches off (input 0 to the mixer) any of its seven components - context statistics of order 1, 2, 3, 4, 6, the
lowercase word context, and the match model (whose length is then also hidden from the mixer selector); the two
SSE stages and the mixer stay on. Per coded byte it logs the byte and the sum over its 8 bits of -log2 of the
coder's probability. With all components on, the compressed file is byte-identical to the original lpaq1 (checked);
the logged bytes equal the input and the logged total is below the file size. Memory option 4; one process per
window. Unlike paq8px, lpaq1 has no block detection or look-ahead, so its per-byte probabilities are strictly
sequential.

## Ladder

L1 orders 1-2 (mask 3); L2 orders 1-4 (15); L3 orders 1-6 (31); L4 orders 1-6 + match (95); L5 full lpaq1 with
the word context (127).

## Measures

For each of the 34 Battery 88 row sets and each level: H_L = mean -log2 p_L (own code length) and
G_L = mean[-log2 p_L - bits of M_0.001(x, p_L)], x = the learners' ensemble (published-minimum configuration for
benchmark labels, E24 for the eight new sources), M the Battery 100 two-member rule (share 0.001). Realized
gain of this combiner only; pointwise row intervals (`probe.battery75.ci`, seed 1040).

## Predictions (text, code and formal group T: metamath, aitdcc_b_c_source, llm_compression_python,
llm_compression_arxiv_math, dclm, llm_compression_cc, kolmogorov_text, dclm_ranked)

- P1: G_L5 <= 0.002 on at least 6 of the 8 T labels.
- P2: G_L1 > 0.02 on at least 6 of the 8 T labels.
- P3: the lowest level with G_L <= 0.002 is at or below L4 (word context not needed) for at least 5 of the 8 T
  labels.
Images, audio, numeric and the new sources are reported descriptively. Failed predictions are reported. Runner
`probe/battery104.py`; output `runs/battery/battery104.json`.
