# Battery 85 protocol: is the Metamath residual a word-level statistic? (V_word)

Frozen 2026-09-29 before V_word scored any benchmark label (run only on a synthetic word sequence; with the word
experts off it equals V_match exactly, and with everything off V_auto exactly); hashes in AGENT_CHAT (C129).

**Why.** After B84 the evaluated ensembles are lower than V_match by more than 0.02 bits per byte only on Metamath
(0.106), at positions where the copy proposal is wrong (0.95) or absent (0.27). Metamath is a sequence of
space-separated tokens (labels, math symbols, keywords). Context-mixing compressors also use word models: counts of
the next byte given the current partial word, and given the previous word plus the current partial word.

**Method (probe/white_box7.py).** V_match plus two experts, online, per row, from past bytes only: word0 (counts of
the next byte given the current partial word, up to 24 bytes) and word1 (given the previous word and the current
partial word), Dirichlet prior 0.05. The separator is the most frequent byte of the row so far (from byte 16), so no
alphabet is assumed. Same mixing, gate and probability map. All 26 labels, first 256 rows, all 4095 targets; cloud
CPU containers; per-position arrays kept for Metamath, ranked DCLM and C source.

**Predictions.**
- W1: on Metamath, V_word is lower than V_match by at least 0.05 bits per byte.
- W2: on Metamath, V_word is lower than the evaluated ensemble.
- W3: V_word is not higher than V_match by more than 0.01 bits per byte on at least 24 of 26 labels.
Readouts also: V_word minus ensemble with row bootstrap (seed 850), labels below the published minimum, and the
Metamath residual split by position within a word (descriptive).
