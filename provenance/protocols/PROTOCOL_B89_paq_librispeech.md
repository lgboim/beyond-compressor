# Battery 89 protocol: paq8px on the LibriSpeech chunks of Section 4

Frozen 2026-09-29 before any paq8px output on these chunks; hashes in AGENT_CHAT (C135). Cloud CPU, no training.

**Data and method.** The 20,000 B78 chunks (2048 bytes each; byte = (s >> 8) + 128 of 16-bit samples), and within
them the 2,000 chunks of B79 (seed-790 subsample). paq8px exactly as in B88 (same commit, level -8, default
options, one file named `w` per chunk). Rates in % of 8 bits per byte, all 8 bits coded: (a) headers counted once
per collection, as for FLAC, gzip and LZMA in B78 (subtract the 1-byte-file output size minus 1 from every chunk but
one); (b) headers counted on every chunk (reported). Utterance bootstrap (seed 890) as in B79.

**Predictions (headers counted once, the same 2,000 chunks).**
- R1: paq8px is below FLAC (30.6%).
- R2: paq8px is below V_base with all 8 bits (25.9%).
- R3: paq8px is below both open 7B language models with all 8 bits (Mistral-7B 34.7%, Qwen2.5-7B 28.9%).
Readouts also on all 20,000 chunks, beside the published rates (an unpaired comparison under a different bit
convention for the language models).
