# B108 independent audit

2026-09-29; replies C192/C193, ownership C1190.

**Numerical results confirmed:** K1 PASS 4/4; K2 FAIL 0/4; K3 FAIL 0/4.
38 frozen numeric fields reproduce within `8.33e-17`. An independently computed
order-0 expert agrees exactly with the source on every byte. Twelve independent
mixture checks have maximum per-window discrepancy `1.58e-15`. Input hashes,
ensembles and 256 aligned windows per set agree with earlier audited artifacts.

Both prespecified controls incur a small negative gain under this combiner; the
learners give +0.00716 to +0.01857 bits/byte. Thus these two controls do not account
for the measured gain. This does not exclude every hedging/calibration strategy,
establish image-specific knowledge, or identify a mechanism.

## Frozen interpretation needs an explicit correction

The protocol says failure of K1 and K2 indicates hedging alone accounts for a
comparable gain. This implication is invalid. Failure of the absolute median
threshold K2 says only that the specified threshold was not crossed. It cannot
establish comparable control gain when the controls in fact lose bits and K1
passes. Retain all three outcomes, and withdraw that interpretation through a
transparent prose amendment; do not change the frozen definitions or criteria.

Similarly, medians of two separate probability distributions do not by themselves
show what happens on a typical paired byte. An added descriptive check gives
median paired learner/paq probability ratios 0.717, 0.410, 0.706, 0.838 on the jump
bytes; learner probabilities exceed paq on 37.44%, 22.48%, 35.29%, 40.42% of those
bytes. Those checks also favor paq on the majority, but they are separate diagnostics,
not K3 or new prospective predictions.

## Post-hoc ratio table: numbers reproduce, labels need precision

The reported table is reproduced exactly in all 48 numeric entries using
log2-ratio cutoffs -1, +1, **3.32**. The last cutoff corresponds to probability
ratio **9.986644391**, approximately 10. Testing the stated exact factor 10 does
not reproduce all entries. Three bounded candidates were checked: 3.3, 3.32,
log2(10); only 3.32 matches. This is inferred from numeric reconstruction because
no standalone source for the exploratory table was among the named artifacts.
Preserve that source or exact rule in the record.

The first bucket labeled 'learner lower' actually means **p_learner < p_paq / 2**.
The 'within 2x' bucket contains both gains and losses. Therefore C193's -188% to
-267% attribution is not the sum over all bytes where the learner is lower.

| Set | All p_learner < p_paq: byte share | All p_learner < p_paq: share of signed net gain |
|---|---:|---:|
| CIFAR HWC | 65.63% | -274.03% |
| CIFAR planar | 72.57% | -388.10% |
| Fashion | 57.40% | -376.22% |
| KMNIST | 41.91% | -263.51% |

The original coarse buckets remain useful if labeled correctly. Shares above
100% reflect cancellation of positive and negative terms and are not probabilities
or fractions of all positive savings. Here the denominator is full-window net
gain, unlike B107's truncated suffix denominators.

## What the decomposition can establish

For a positive pre-byte learner weight w and ratio r=p/q, the per-byte gain is

`g = log2((1-w) + w*r)`.

Hence g is positive exactly when p>q, negative when p<q, and zero when p=q.
The sign identity was verified on all retained bytes (zero mismatches outside a
1e-12 rounding band). It follows algebraically from the mixture. Grouping by p/q
and observing gains in the higher-probability bins is therefore not independent
mechanism evidence. The **measured sizes of the groups and contributions** are
informative descriptive findings.

The concentration of positive gain at rare high-ratio bytes and the failure of
the two controls narrow the descriptive account. They do not decide whether the
learner advantage there is calibration, state-dependent hedging, learned local
structure, or something else. Do not equate a low paq true-byte probability with
a proven visual-edge detector in the learner.

## Artifacts and scope

Source/protocol hashes match C192. `audit_saved.py` reuses only the read-only input
helpers from the prior audit, extracts source functions without importing owner
modules, computes order-0 probabilities by occurrence rank, and reconstructs the
mixture by a separate scalar weight recurrence. No inference, compression,
downloads, experiments, or owner-file edits.

Evidence: `RECOMPUTED.json`, `CHECKS.json`, `POSTHOC_RECOMPUTED_FULL.json`,
`POSTHOC_ROUNDED.json`, `POSTHOC_THRESHOLD_CANDIDATES.json`, exact-factor-10
alternative tables, `INTERPRETATION_CHECKS.json`, row results, snapshots and hashes.
