# Battery 81 protocol: does richer in-sequence context statistics close the text gaps? (V_ctx)

Frozen 2026-09-29 before V_ctx scored any benchmark label (a synthetic word sequence was used only to check the
code). Hashes in AGENT_CHAT (C121). No learner is run.

**Why.** B80 found that on ranked text and Metamath the evaluated ensembles gain on V_auto mainly at positions where an
earlier match could be copied, and the ensembles lead V_auto overall on four text and code labels: ranked DCLM text,
Metamath, C source and Python. V_base and V_auto use counts of order 0 and 1 and a longest-match copy expert, but no
higher-order contexts, which classical PPM-style compressors use.

**Method (probe/white_box5.py).** V_ctx = frozen V_auto (white_box4, unchanged, including its known scale-update
defect) plus four experts: for k in {2, 3, 4, 6}, Dirichlet-smoothed counts (prior 0.05) of the bytes that followed
earlier occurrences of the current k-byte context in the same row. Same mixing and constants. Scored on all 26 labels
as B76/B77 (first 256 rows, all 4095 targets), on cloud CPU containers, with per-row means saved.

**Predictions.**
- K1: on the four text and code labels above, V_ctx is below V_auto.
- K2: V_ctx is below the published minimum on at least 2 of those 4 labels.
- K3: on at least 18 of the other 22 labels, V_ctx is within 0.03 bits per byte of V_auto.

Readouts also include V_ctx minus the frozen B75 evaluated ensemble on identical rows (row bootstrap, seed 810).
