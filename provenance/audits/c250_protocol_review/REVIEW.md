# C250–C251: B113 results and B114 protocol audit

Scope: independent read-only audit of the frozen protocols, the submitted neutral-mode patch, and completed B113 saved-array results. No training, model inference, compressor invocation, cloud dispatch, or writes to run directories. B114 was running during this review; its numerical S0 and S1–S3 results are not certified here.

## Verdict

B113's submitted numerical results reproduce. The prespecified outcome is **Q1 and Q5 pass; Q2, Q3 and Q4 fail**. The position × repetition breakdown is correctly labelled post hoc. It localizes realized mixture gains; it does not establish a neural copying mechanism or a causal explanation for pretraining transfer.

B114 is interpretable as a **direct mixer-feature and context-selection intervention in the full compressor**. It is not removal of a self-contained module, a minimal compressor construction, or a replication of lpaq1. The draft's asserted direction of bias is not justified. Its analysis needs complete-input checks, an enforced S0 acceptance gate, and explicit mask comparability before scientific results are accepted.

## Frozen sources and identity

- B113 protocol SHA256: `0cb606c990c804a0e9889ef5e369fc6b9c64b7f5cad4ebf5f613ff641188c81d`.
- B114 protocol SHA256: `d0bc759d7f5abc737c905e9c33a4430adda7cff696b0431bfbda9b3a298358f2`.
- Patch concatenation in alphabetical filename order (`ContextModelGeneric.cpp`, `ContextModelText.cpp`, `Encoder.cpp`, `Mixer.cpp`) matches C250: `3df0d018a4bd59007efff8080f5a6ed794c55da6a6a23d9fa2103d40a111118d`.
- B114 Encoder is byte-identical to B98's logger.
- B113 submitted output SHA256: `42e21b67d82754333a411ba892081e46570ab164d90c3846ca6b2217ce40e376`.
- B113 post-hoc output SHA256: `499c7b0c416f8fd959d50a86c421f321eef8c85a0f86c809ec5f741aab0d249b`.
- `SOURCE_MANIFEST.json` pins the full reviewed local sources. `UPSTREAM_MANIFEST.json` records pinned primary-source URLs and hashes, including unsuccessful path lookups; corrected paths were obtained from the upstream tree. Diffs show only the announced hooks/wrappers in the three ablation source files, apart from BOM normalization.

## B113 independent numerical audit

`check_b113.py` reads completed arrays directly, reconstructs the published frontier configuration and seed lists from their sources, validates B98 contiguous chunk offsets, pinned commit, metadata/mask consistency, all row shapes and finite retained data. It independently computes gains with a log-space prediction/observation/redistribution recurrence, and builds repetition classes with rolling integer contexts rather than the runner's byte slices.

Checked **154 input files**, **2,042 retained windows** of 4,095 bytes (256 for each of seven labels; 250 for dclm_ranked). None of the eight averaged learner-probability arrays needed the inherited 1e-30 clipping. All lpaq1-gain and compressor-difference totals used by Q1/Q2/Q4 are strictly positive on these inputs.

All **1,295 numeric fields** in the submitted main and post-hoc JSONs reproduced within 1e-10. Largest absolute difference: **3.571420936765435e-12**, in a Spearman statistic; no numeric discrepancies. This uses a different mixture recurrence, so differences from rounding/tie order at this scale are unsurprising. Exact counts and pass booleans agree:

| Prediction | Observed count | Required | Result |
|---|---:|---:|---|
| Q1 early gain concentration | 8/8 | 6/8 | pass |
| Q2 early compressor advantage | 4/8 | 6/8 | fail |
| Q3 lower gain on repeat hits | 0/8 | 6/8 | fail |
| Q4 enriched word-start gains | 0/7 | 5/7 | fail |
| Q5 positive gain/difference correlation | 8/8 | 7/8 | pass |

Ranges across the eight labels:

- First 512 positions: **54.6120–88.5661%** of total signed gain beyond lpaq1, at 512/4095 = 12.5031% of positions.
- Their share of paq8px's advantage over lpaq1: **19.2179–27.5882%**. C251's “19–27%” upper endpoint should be about 28% at integer precision.
- Mean gain at repeat hits / whole-label mean gain: **1.5701–13.1914×**, not C251's “2–12×”. Metamath is the low endpoint; dclm is the high endpoint.
- Repeat-hit contribution: **49.5921–103.1684%** of signed total gain. Values over 100% are valid because the complement can lose bits; these are not proportions of positive gain mass.
- Spearman correlation: **0.248515–0.355143**.
- Post-hoc early repeat-hit contribution: **36.5711–74.9632%** of total signed gain. Mean gains on those bytes: **0.677883–1.565337 bpb**.
- Whole-label gain beyond paq8px: **−0.000961672 to +0.000094109 bpb**, for the specified share-0.001 combiner.

Recomputed outputs and full row/seed provenance: `B113_RECOMPUTED.json`, `B113_POSTHOC_RECOMPUTED.json`, `CHECKS.json`, `INPUT_MANIFEST.json`. The B104 L5 summary values also agree for all eight labels to floating-point precision; see `B104_CONSISTENCY.json`.

### What these results establish, and what they do not

1. Q5 is descriptive, not independent evidence that paq8px captures a particular learned mechanism. Both axes contain the same lpaq1 loss. With prior learner weight `a` held fixed, gain equals `log2(a*p_L*2**b_lpaq1 + 1-a)`; its derivative with respect to `b_lpaq1` is nonnegative. The other axis is `b_lpaq1-b_paq`. Shared dependence can contribute positive association. In the actual data weights and predictions also vary; the correlation is not a tautology, but it cannot isolate a mechanism.
2. “Repeat hit” uses the observed current byte to classify whether the earlier continuation was correct. This is legitimate retrospective error analysis. It is not a decision rule available before predicting that byte and does not prove that a neural model implements copying. The byte-class strata likewise condition on the realized byte.
3. Early concentration is consistent with an online-reference cold-start explanation. However, the measured quantity also contains a combiner that resets to equal weights on every window. This audit does not separate reference adaptation, prior learner skill, mixture routing, and corpus composition. Prefer “gain is concentrated in early positions, especially retrospectively successful repeats” to “we established confident copying as the cause.”
4. The post-hoc L1 series is the earlier B104 neutral/masked instrument, not a validated independently smaller lpaq implementation. Preserve that qualification if interpreting those extra columns.
5. These are window/byte diagnostics on previously used corpora and selected released configurations. Freezing the new predicates does not make the corpora fresh heldout data. The five count rules are not significance tests; bootstrap-free byte correlations should not be treated as evidence from millions of independent experimental units.

## B114 audit findings

### Material: the intervention leaves adaptive pathways, with no guaranteed direction of bias

The patch sets a group's `Mixer::add`/`promote` values to zero and its `Mixer::set` context argument to zero while executing the group. It preserves allocations, number of mixer branches, update schedule, and shared state.

Pinned upstream evidence:

- `src/SSE.cpp:286–293` still uses Text.mask, Text.firstLetter, Text.order, WordModel.order and Match fields in text calibration.
- `src/model/RecordModel.cpp:187` reads Match.expectedByte.
- `src/Mixer.hpp:176–181` shows that selecting context zero selects `base+0` within each group's own weight-bank range; it does not remove that range or merge all groups into one context.
- `src/Mixer.cpp:forward/update` computes and updates selected banks on the full surviving input vector. Thus constant-selected branches remain adaptive, even when the selecting group's raw features are zero.
- `src/model/ContextModel.cpp:84–161` dispatches to several specialized paths. B114 wraps the text and generic paths only. Raw-byte alignment alone does not record which model path handled each byte.

These details support a direct-feature/context-selection ablation with surviving indirect routes. They do **not** establish that the measured effect is always a lower bound on total module importance: interactions, redundancies, context routing and changed online learning can increase, reduce, or reverse effects. Replace the frozen protocol's interpretation via an appended clarification, preserving the original: **“Indirect routes remain; the direction of the resulting bias is not established.”**

In particular, a strong K2 would demonstrate performance of a masked full paq8px system retaining its mixer/SSE/state machinery. It would not demonstrate that “normal + match + word alone” suffices or that lpaq1's architecture has been recovered. A D_text null result cannot establish that text-derived state is unnecessary.

### Material: enforce complete-input and S0 acceptance checks

Reviewed `probe/b114_modal.py:120–168` concatenates whichever parts exist and discards commit/metadata at load time. The resumed scorer skips an existing filename without validating provenance. Missing short totals generally cause shape errors, but there is no verified mapping from chunk offset to original row identity; shape equality alone is insufficient protection against stale, misindexed, duplicated or mixed-source parts. This is a missing validation, not a claim that such corruption occurred.

Before accepting B114, validate exact variant/label coverage, chunk offsets and counts, total shape against B88, finite retained values, metadata/alignment correspondence, pinned upstream commit, and recorded patch/protocol identity. Preserve already running output and record provenance in separate audit artifacts if necessary.

S0 currently has the right numerical comparison in its boolean, but is evaluated after label results and does not suppress independent S1–S3 pass booleans on failure. Fail closed scientifically: no accepted S1–S3 unless all eight aligned sets and every retained V0 value match B98. Four smoke windows do not satisfy this all-row gate. No full S0 result existed during this audit.

### Material if masks differ: S3 comparisons need a common population

The declared per-variant retained population is `aligned(V0) ∩ aligned(v)`. The current S3 reduction subtracts aggregate K2 and K2+g means that can use different masks. If all masks are identical, the calculation is properly paired in population; demonstrate and retain that fact. Otherwise preserve the frozen result and add a clearly identified common-row sensitivity/amendment. A shared intersection across all compared additions is needed for an unconfounded ranking across groups. This audit has not observed a mask mismatch.

### Interpretive boundaries for S1–S3

- S1's small realized learner gains under individual drops do not establish that all such components are unnecessary. Redundancy and surviving routes can mask their importance; inspect the descriptive compressor losses as well.
- S2 tests a named masked configuration under a fixed combiner and threshold; it is not a test of a clean three-component compressor.
- S3 is a conditional ranking of additions to K2, not an additive partition of the full compressor's performance or a global ranking of module importance. A “largest” point estimate does not by itself establish separation from the next group; the individual pointwise G intervals do not test paired ranking differences.
- Do not turn the 0.002 threshold into a significance/equivalence threshold. Preserve S0 and all failed original predicates even if subsequent changes are useful.

## Completion and remaining boundary

B113 numerical review is complete. Corrections above concern two rounded ranges and causal interpretation, not the five prespecified outcomes. B114's original protocol and source snapshot are preserved; numerical admission remains pending completed results and source/mask/gate checks. No new experiment or research direction is proposed or launched by this audit.
