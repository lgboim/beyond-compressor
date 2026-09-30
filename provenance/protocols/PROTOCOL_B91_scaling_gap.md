# Battery 91 protocol: does self-play compute close the gap to an off-the-shelf compressor?

Frozen 2026-09-29 before any B91 fit or readout; hashes in AGENT_CHAT (C146). Analysis of saved data only (the
published compute frontier and the B88 paq8px rates); no inference. Motivated by Codex's novelty critique: connect the
calibration to the original paper's central claim, that loss falls predictably with self-play compute.

**Data.** For each of the 26 labels, the published compute frontier built with the authors' own code
(`refs/official/figures/table2_scaling_exponents/scaling_analysis.py`, `compute_frontier`, default options) from
their file `frontier_traj_perk.json` (rungs 500k-24M; compute C = K x N x 1536 x 4096 x (round + 1)), and the B88
paq8px rate P (full files, headers counted) on the same rows.

**Fits (the authors' functions).** (a) The paper's Figure 1 law, a pure power law loss = A C^(-alpha), fitted in log
space (`fit_log_power_law`). (b) The floor form loss = E + A C^(-alpha) (`fit_curve_power_law_with_floor`).
Held-out rung: both fits are repeated on the frontier built without the 24M rung (`omit_rungs=("d512h8L8",)`) and
used to predict the minimum loss of the full frontier at compute at or beyond the smallest 24M-rung frontier point
(the 24M part of the envelope).

**Readouts.** C* = the compute at which the fitted law reaches P, as a multiple of the largest frontier compute
Cmax (pure law: C* = (A/P)^(1/alpha); floor law: infinite if E >= P). Per label and median over the labels where P is
below the published minimum.

**Predictions.**
- E1: the pure power law fitted without the 24M rung predicts the 24M part of the frontier (its minimum loss) within
  0.10 bits per byte on at least 13 of 26 labels.
- G1: under the pure power law fitted to the full frontier, reaching paq8px requires more than 100 x Cmax on at least
  13 of the 24 labels where paq8px is below the published minimum.
- G2: under the floor law fitted to the full frontier, the fitted floor E is at or above P on at least 12 of those 24.
Reading fixed in advance: a compute multiple is reported as a headline only if E1 holds; otherwise the extrapolation
is reported as unreliable. All fits are extrapolations beyond observed compute, not demonstrated limits.
