# Battery 82 protocol: how scale and calibration shape where the learners gain

Frozen 2026-09-29 before any B82 score; hashes in AGENT_CHAT (C121). Inference only on cloud GPUs.

**Data and models.** The five B74 checkpoints (500k, 1M, 3M, 6M, 24M; seed 0; round 8191) on all 26 labels (first 256
rows, prefix `O`, all 4095 targets), scored with the authors' own model code (`refs/official/scoring`), fp32.
Per position: loss -log2 p(actual byte) and the entropy of the predictive distribution, both averaged over rows; per
row, means over the position bins [0,16), [16,64), [64,256), [256,1024), [1024,4095).

**Predictions.**
- L1 (scale): the per-byte gain from 500k to 24M (loss_500k - loss_24M) is larger in bytes 16-255 than in bytes 0-15
  on at least 18 of 26 labels.
- L2 (early miscalibration): for 24M, mean loss exceeds mean predictive entropy in bytes 0-15 (overconfidence) on at
  least 18 of 26 labels.
- L3: for 24M, loss minus entropy is larger in bytes 0-15 than in bytes 1024-4094 on at least 18 of 26 labels.

Parity check: the 24M per-row mean loss equals the saved B74 value within 1e-3 bits per byte on every label.
