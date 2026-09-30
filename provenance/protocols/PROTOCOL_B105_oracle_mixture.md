# Protocol B105: oracle convex mixtures with paq8px (diagnostic)

Frozen before any B105 number is computed. Saved artifacts only (Battery 98 per-byte paq8px code lengths on aligned
windows, learner ensembles as in Battery 98, bGPT domain weights as in Battery 100). No inference or cloud.

Question (review suggestion): is the near-zero realized gain beyond paq8px on text, code and formal data a
limitation of the online combiners, or does even a hindsight-optimal static mixture gain nothing?

For a row set with paq8px probabilities q and model probabilities p (true byte), over a grid of weights
a in {0, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, ..., 1.0}:
- corpus oracle: O_c = mean(-log2 q) - min_a mean(-log2(a p + (1 - a) q)), one a per row set chosen after seeing
  the data (an upper bound on what a single static weight could realize here, optimistic by construction);
- window oracle: O_w = mean over windows of [mean(-log2 q) - min_a mean(-log2(a p + (1 - a) q))], one a per
  4095-byte window (more optimistic still).
Models: the learners' ensemble (all 34 row sets); bGPT with the Battery 100 pre-assigned domain weight (24 row sets).
These are post hoc oracles, not predictors; they are reported only as diagnostics of combiner sensitivity.

Predictions (text, code and formal group T of Battery 104):
- O1: learners' corpus oracle O_c <= 0.002 on at least 6 of the 8 T labels.
- O2: learners' window oracle O_w <= 0.005 on at least 6 of the 8 T labels.
- O3: bGPT's corpus oracle exceeds the learners' on every one of the 7 T labels that have a bGPT domain.
Failed predictions are reported. Runner `probe/battery105.py`; output `runs/battery/battery105.json`.
