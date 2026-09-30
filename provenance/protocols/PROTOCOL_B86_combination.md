# Battery 86 protocol: are the learners and an online predictor complementary? (training-free combination)

Frozen 2026-09-29 before any combined score; hashes in AGENT_CHAT (C129). Inference only; no parameter is fitted.

**Data.** Per position, the probability of the actual byte under (a) the evaluated B75 ensemble of each label (saved
probabilities) and (b) frozen V_match (white_box6, gate and apm on), rescored on cloud CPU containers with
per-position output and the match state (no proposal, or length bucket 3-4, 5-8, 9-16, 17-32). Parity: V_match's
per-row means equal B84's (float64 labels within 1e-9; float32-stored labels within float32 rounding). All 26 labels,
first 256 rows, all 4095 targets.

**Combinations (online, per row, from past bytes only; same fixed-share rule and share 0.01 as V_auto's mixtures).**
- C_mix: a two-member Bayesian fixed-share mixture of the ensemble and V_match, prior weights 1/2.
- C_gate: the same with a separate weight pair for each of the five match states.

**Predictions.**
- X1: C_mix is lower than the better of its two members by at least 0.02 bits per byte on at least 18 of 26 labels.
- X2: C_mix is below the published minimum on all 26 labels.
- X3: C_gate is lower than C_mix on at least 18 of 26 labels.
Readouts also: C_mix minus each member with row bootstrap (seed 860), and the mean weight on the ensemble by
position bin (0-15, 16-63, 64-255, 256-1023, 1024-4094). The combination uses the learners themselves, so it is
reported as a statement about complementarity, not as a training-free baseline.
