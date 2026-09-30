# Battery 92 protocol: the text case of "Language Modeling Is Compression" (enwik9, 2048-byte chunks)

Frozen 2026-09-29 before any enwik9 byte was downloaded; hash in AGENT_CHAT (C147). Cloud CPU; no training.

**Why.** A balancing case: on text, large language models trained on text (which may include Wikipedia) are expected
to beat any general-purpose compressor. Delétang et al. (2024), Table 1, chunk 2048: gzip 48.1%, LZMA2 50.0%,
Transformer 3.2M trained on enwik8 17.0%, Llama 2 7B 8.9%, Chinchilla 70B 8.3%.

**Data.** enwik9 (mattmahoney.net/dc/enwik9.zip; hash recorded), split into consecutive 2048-byte chunks; 2,000 chunk
indices drawn without replacement with `numpy.random.default_rng(920)`. Each chunk is coded on its own.

**Methods.** gzip level 9 and LZMA (Python defaults), paq8px (the B88 commit, level -8, one file per chunk), and
frozen V_base and V_match (online, per chunk). Rates in % of 8 bits per byte; compressors with every file counted in
full (primary) and with one header per collection (reported); predictors as ideal code length. Chunk bootstrap
(seed 921) for intervals.

**Predictions.**
- T1 (sanity): gzip is within 1.5 points of the published 48.1%.
- T2: paq8px (full files) is above both Llama 2 7B (8.9%) and Chinchilla 70B (8.3%).
- T3: paq8px (full files) is above the enwik8-trained Transformer 3.2M (17.0%).
Comparisons with published values are unpaired (different chunks); the language models may have seen Wikipedia text.
