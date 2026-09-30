# Protocol B103: do the learners know program structure that paq8px lacks, in their own domain?

Frozen before any B103 score exists. Inference and compression only (Modal A10G for released learners, Modal
CPU for the logging-only paq8px of Battery 98). No training.

## Data

Program outputs from our reimplementation of the Brainf*ck-like machine of Cowsik et al. (App. E):
`probe/b103_machine.py`. Alphabet: the 8 instructions, the end token F and the 10 macro tokens of their Table 4
(expanded to their stated Brainf*ck definitions); programs sampled from the uniform prior g0 (i.i.d. tokens until
F). Execution: circular tape, cells mod 256, ',' reads uniform random bytes, unmatched brackets are no-ops.
Resource limits are NOT published; ours are tape 256 cells, 200,000 steps, program length <= 1024 tokens, output
length T = 4095. Kept: programs whose output reaches 4095 bytes and is not constant over its last 2048 bytes
(256 of 130,517 sampled; seed 1030). File runs/battery/b103/data/program_outputs.jsonl, SHA-256
dd6823e40482f5d1dd21b2a51f13f42385913594302e3ac80ab617c32db1e161. The appendix example program reproduces
(1, 2, 3, halt). Because our limits and filter differ from the authors' (unknown) settings, this is an
approximation of their training domain, not a copy.

## Models

Round 8191: self-play 24M (8 seeds), self-play 6M (first 4 sorted seeds), fixed-prior (uniform) 6M (4 seeds),
self-play 100k (8 seeds); probability average per arm. paq8px per-byte code lengths as in Battery 98.

## Measures and predictions

E: an arm's own loss; G_paq: Battery 100 two-member rule with share 0.001 (realized gain only).
- H1: the self-play 24M ensemble's own loss is below paq8px by at least 0.3 bits per byte.
- H2: G_paq of the self-play 24M ensemble is at least 0.1 bits per byte (versus about zero on natural text,
  Battery 101).
- H3: the fixed-prior 6M ensemble has lower own loss than the self-play 6M ensemble on these uniform-prior
  outputs.
Failed predictions are reported. Runner `probe/b103_modal.py` (`run`, then `analyze`); output
`runs/battery/battery103.json`.
