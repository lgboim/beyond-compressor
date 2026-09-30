# Battery 75 protocol: published-configuration ensembles on identical rows, row identity, MusicNet

Frozen 2026-09-29 before any Battery 75 score was computed; its sha256 is recorded in AGENT_CHAT (C094) before the
scoring job starts. Inference only, no training. Downloads approved by Ariel 2026-09-29. The only model output seen
before freezing: a timing test of the already-scored B74 checkpoint (24M seed 0 r8191) on 32 DNA rows.

## Inputs

- Labels: the 24 labels of the paired suite (B74) plus `musicnet_pcm8` and `musicnet_pcm8_11khz`, baked 2026-09-29 with
  the authors' `prepare_musicnet_benchmark.py` (unchanged copy, context 4096). First 256 rows of each file (fewer where a
  corpus has fewer), exactly as B74.
- Checkpoints: released `learner_<round>.pth` files, read from the local Hugging Face cache with the network disabled.
  The sha256 of every checkpoint file is recorded at scoring time.
- Scoring: identical to B74 (prefix `O`, all 4095 targets, MLX fp32 port). For every (checkpoint, label) the probability
  of each actual next byte is saved (float32, rows x 4095), so ensembles are formed afterwards without rescoring.
- Ensemble (the authors' definition in `score_from_hf.py`): average the seeds' probabilities of the actual byte, then
  -log2, then mean. A row's value is its mean over positions; a label's value is the mean over rows.
- Published values: `refs/official/figures/fig1_overview/frontier_traj_perk.json` (rung, round, corpus, K). The
  published reference of a label is its minimum over all entries (as in the paper).

## Part A: row identity (100k = d64h1L1, round 8191)

Eight seeds are released and the published entry has n_seeds = 8, so K = 1 (mean of the eight single-seed values) and
K = 8 (the one eight-seed ensemble) are exactly reproducible. All 26 labels are scored.
A label *reproduces the published score* if |ours - published| <= 0.002 bits per byte at both K = 1 and K = 8.

- A1 (validity check): all six shipped corpora reproduce. If one fails, Part A is a scoring mismatch, not a row finding.
- A2 (prediction): at least 18 of the 20 rebuilt labels reproduce.

## Part B: cause of the P3 gap (24M, round 8191)

Eight seeds released, published n_seeds = 8. The six shipped corpora are scored with all eight seeds.

- B1 (prediction): our K = 1 reproduces the published K = 1 within 0.002 on all six. If it does, the B74 diagnostic gap
  (seed 0 below the published K = 1 average) is attributed to seed-to-seed variation, and per-seed values are reported.

## Part C: the configuration behind each published minimum, on identical rows

For each of the 26 labels, the (rung, round, K) of its published minimum. The ensemble scored is:

- *exact* where the published n_seeds equals the released seeds and K = n_seeds: 24M rounds 5376, 5888, 6144 (K = 8).
- *identified* for 3M rounds 4096, 4608, 5632 (published 8 of 9 released) and 100k round 6144 (8 of 10): the 8-seed
  subset whose K = 8 ensemble on the shipped DNA corpus reproduces the published DNA K = 8 value at that configuration
  within 0.002. If no subset, or more than one, qualifies, all released seeds are used and the label is flagged
  approximate.
- *approximate* for 24M rounds 768, 1024, 1536 (published K = 11 of 11 seeds) and 5120 (K = 9 of 9): the K = 8 ensemble
  of the eight released seeds. The published K = 8 and K-minimum values at that configuration are reported alongside,
  as an unpaired calibration of the approximation.

Readout per label: mean of V_base minus the ensemble, and of the best of the six fixed methods (selected by mean,
outside resampling) minus the ensemble, with 95% row bootstraps (seed 750, 2000 draws); counts over the 26 labels and
over source groups (the 13 of the paper plus MusicNet as a fourteenth).

- C1 (prediction): V_base is lower, interval below zero, on at least 13 of the 15 labels where it is numerically below
  the published reference (unpaired, the 24 original labels).
- C2 (prediction): the ensemble is lower than every tested method, interval of best-of-six minus ensemble above zero, on
  CIFAR-10 (both layouts), 16-bit audio, float32 and astronomy.
- C3 (prediction): V_base is lower, interval below zero, on at least one label of each of the eight new source groups
  where it is below the published reference.

## Part D: MusicNet (never scored by any method before this protocol)

The six fixed methods (B74 code, unchanged; V_base frozen since before the 13 new groups were scored) and the five B74
checkpoints (seed 0, round 8191) are scored on both MusicNet labels, plus the Part C ensembles.

- D1 (prediction): V_base is numerically below the published reference on both MusicNet labels (basis: all four ESC-50
  and Speech Commands labels).
- D2 (prediction): on identical rows, V_base is lower than the best of the five B74 checkpoints on both, interval below
  zero.

## Order, analysis and reporting

Order: A, D (methods, then checkpoints), C (3M, 100k, 24M exact, 24M approximate), B. The scoring job prints progress
only, no loss values. `probe/battery75.py --part summary` is written before any readout and computes every number above.
All outcomes are reported, including failed predictions. Anything not listed here is post hoc and labelled so.
