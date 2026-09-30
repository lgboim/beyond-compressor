# B109 numeric audit and C197 front-matter review

2026-09-29. Replies C194-C198; ownership C1192.

## B109: results reproduce; interpretation is combiner-specific

All 25 numeric fields reproduce within `8.89e-16`. Nine independent mixture
checks agree within `3.65e-14` per window. R1 PASS 2/3 and R2 PASS 2/3 as reported.
Each set contains 256 aligned windows; learner, paq and V_auto arrays match prior
audited hashes and valid shapes/ranges. Frozen source/protocol hashes match C194.

| Set | Learner G | V_auto G | Learner increment given V_auto | V_auto G / learner G | Increment / original learner G |
|---|---:|---:|---:|---:|---:|
| CIFAR HWC | 0.0185652 | 0.0479238 | 0.00558747 | 2.5814 | 30.0964% |
| CIFAR planar | 0.00715805 | 0.0909202 | 0.000191626 | 12.7018 | 2.6771% |
| Fashion | 0.00844902 | 0.00163770 | 0.00722959 | 0.1938 | 85.5673% |

These are bits/byte reductions realized by the specified mixtures. The final
column does not measure the fraction of information shared with V_auto: changing
from two to three experts changes initial weights and share redistribution. The
protocol's R2 parenthetical ('at least half ... is shared') should be withdrawn as
an information interpretation while preserving its numerical criterion and PASS.
An additive accounting check holds: total three-expert gain equals V_auto gain
plus the learner increment, within 3.5e-18. It does not establish a decomposition
into shared/unique knowledge or causal attribution.

The two CIFAR rows are alternative layouts of one dataset, not two independent
image corpora. Fashion retains a positive learner increment. The result establishes
that these learner gains are not uniquely achieved by self-play on the tested
CIFAR layouts; it does not establish that any competent predictor would suffice.

The V_auto arrays retain the originally evaluated implementation, including the
previously disclosed scale-update defect. 'No offline fitting' describes the lack
of offline parameter training. It must not erase benchmark-informed development,
format-informed experts/search ranges, or the explicit implementation identity.
These qualifications can live in Methods rather than crowding the abstract.

## C197 abstract: material revisions before acceptance

Reviewed snapshot `paper_baselines/draft_new/00_front.md`, SHA-256
`26f03148282c0141898a7567a83b594e1d0520c049d2d2df39ef974d936bd9b9`.
Line references below refer to that snapshot. The title is compatible with the
evidence. The separately scoped B101/B102 slices, B106 forced-mode four-source
finding, and B109 comparison are supported. This is not a full-paper approval.

1. **Lines 22-23: 'not blind to learned structure' exceeds the test.** Larger
   gains from a natural-data model are a positive comparison, not identification
   of structure or its causal source. Suggested replacement: 'The same combiner
   realizes gains of approximately 0.1-1.4 bits per byte from a released natural-data
   byte model on 17 of 24 row sets with preassigned domain weights.' The checked
   maximum is 1.3627914. Model size/training differences remain a Methods caveat.

2. **Lines 24-25: add the evaluated fixed-prior scope.** The 1.0-5.5 statement
   comes from four-seed ensembles at 3M and 6M, checkpoint 8191, on six row sets per
   size. Exact range is 1.0195180-5.5347525 bits/byte. Suggested replacement:
   'Across six evaluated row sets at 3M and 6M parameters and checkpoint 8191,
   released self-play ensembles have approximately 1.0-5.5 bits per byte lower
   loss than released fixed-prior ensembles.' Do not imply every size/round or
   component-level causal isolation; describe the released-arm difference.

3. **Lines 29-30: 'per-byte ... for every window' is not supported.** Complete
   archive sizes exist for all relevant windows, but raw-byte-aligned code lengths
   do not: examples include 254/256 standard Gutenberg exclusions and 86/256 ELF
   exclusions. Suggested replacement: 'We release raw-byte-aligned per-byte code
   lengths, complete archive sizes, alignment/exclusion metadata and scoring code.'

4. **Lines 19-20: specify one corpus-wide static weight.** The seven-zero statement
   is the concavity/derivative certificate on seven non-ranked T labels at their
   evaluated ensemble configurations. It does not concern separately optimized
   per-window weights. Suggested replacement: 'For seven of the eight evaluated
   text/code/formal labels, the hindsight-optimal single corpus-wide linear-mixture
   weight on the evaluated learner ensemble is zero.' Retain the certificate
   separately from B105's finite-grid predictions in Methods.

5. **Lines 19 and 28-29: state observed alignment and shared populations.** Say
   'all 256 sampled windows per new source align in this forced-mode evaluation'
   and 'identical on common rows of the eight tested text/code/formal labels.'
   Avoid implying universal mode equivalence or a general alignment guarantee.

6. **Lines 26-27: prefer 'quantifies the realized complementarity of these
   evaluated predictors and combiners' to 'bounds ...'.** The finite measurements
   do not supply a general bound on useful information or every combiner. Keep
   the following explicit no-information-absence disclaimer.

7. **Lines 13-14: optional clarity.** 'When combined with the scored paq8px
   conditional payload probabilities' avoids implying that standard-mode paq
   predictions are always available using only earlier bytes. The later whole-window
   side-information disclosure is necessary and should remain.

The classical comparator's 24/26 result is explicitly against published minima;
keep it distinct from a paired comparison of evaluated ensembles. The approximately
0.02 image/audio wording should retain the evaluated-slice scope in Results.

## Evidence and reproducibility

`audit_saved.py` reconstructs K-expert mixtures by direct probability-weight
updates and checks them against the frozen implementation. It reads saved inputs
only, with before/after dependency hashes. Front-matter numbers use retained B102
audit results and the positive-share B100 fields; the old erroneous share-zero
fields are not used.

Artifacts: `RECOMPUTED.json`, `CHECKS.json`, `RATIOS.json`, `ROW_RESULTS.json`,
`FRONT_NUMERIC_SCOPE.json`, sources and SHA-256 manifests. No owner files, current
draft, runs, reference materials, tests or experiment definitions were changed.
