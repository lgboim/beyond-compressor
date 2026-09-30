# C256: B115 completed-result audit

## Verdict

The submitted results reproduce. **G0 passes. P1 passes; P2, P3, P4 and P5 fail.** No numeric correction to `battery115.json` is needed.

The constructive result is useful but bounded: the complete modified lpaq1 has lower standalone mean code length than the evaluated learner ensemble on every tested row set, as the original lpaq1 already did. Nonzero initial mixer weights greatly reduce the learner's incremental gain in this instrument. The full set of changes does **not** meet the frozen criterion for removing that gain across primary or secondary corpora; JSON countries retains a clear positive gain.

## Identity and admission

- Submitted output SHA256: `d870b93dfa1b05ad510b85495a55c845326b4932ce3e14605ea7d597aef27d77`.
- Frozen protocol remains `5c002a5d22ec840e9944d9e019c355924418d4333dc87eda60d9f62ace33ea34`.
- Runner remains `a779e4ad48a79d80764f792346ba4c4373250f067b254c0243eb8174edcd4ffe`; C++ source remains `41c261e94b9906a1db6ccd90f6bbdcb8e76856051332fac75a25e96800f0a1e0`.
- The separately recorded post-run correction correctly states ten active U3 contexts, the retained ASCII word heuristic, and the constructive rather than attributional interpretation. It does not alter the code or frozen predicates.
- Exactly **144 expected arrays**, 12 variants × 12 row sets, and **144 matching successful completion-log records** with exit 0. Every saved array has expected float32 dtype, input-matching shape, finite nonnegative code lengths, and the expected row count. No row is excluded.
- **3,066 input windows**, or **36,792 variant-windows**: 2,042 primary and 1,024 secondary. All variant masks and common populations coincide. Ranked DCLM contains 250 input windows; every other row set contains 256.
- G0 reproduces exactly on every byte of all eight primary U0 arrays versus B104 L5: maximum difference **0**, no NaN rows.
- Primary configuration/seed identities and reused input hashes agree with the independently reconstructed B113 audit. Secondary seed files are exactly seeds 40354564–40354571. Their probabilities have valid ranges and shapes; corpus hashes and sequence counts match the B106 manifest, JSONL rows equal the saved byte rows, and available previous audit hashes agree. No averaged learner probability required clipping.
- The independent manifest records **241 input files**. All pinned protocol, source, log and result snapshots remained unchanged through the audit.

The experiment runner does not enforce all these admission checks itself; this completed-artifact audit supplies the missing validations for this particular run. It does not certify the runner against arbitrary future malformed data.

## Independent numerical recomputation

Recomputed H, G, G_512, all 2,000-resample window-bootstrap intervals, all primary/secondary counts and rankings, using a separate log-space prediction/observation/redistribution recurrence. **All 773 numeric fields** agree within 1e-10; maximum absolute difference **8.881784197001252e-16**. All nonnumeric outputs match as well.

| Predicate | Observed | Required | Verdict |
|---|---|---|---|
| P1: UA reduces G versus U0 | 8/8 primary labels | 8/8 | pass |
| P2: UA G ≤ 0.002 | 5/8 primary labels | 6/8 | fail |
| P3: early reduction ≥ 70% of total reduction | 5/8 primary labels | 6/8 | fail |
| P4: largest mean single-upgrade G reduction | U1 | U2 | fail |
| P5: UA G ≤ 0.002 on secondary sources | 1/4 | 3/4 | fail |

Primary UA gains exceeding the threshold are metamath **0.0041601361**, C source **0.0022838862**, and ranked DCLM **0.0036330006** bpb. The fraction of total gain reduction attributable arithmetically to the first 512 positions ranges **0.4445419–0.8796869**. This is a signed loss decomposition, not an isolated causal contribution of early context.

Mean single-upgrade reduction of G across the eight primary labels:

| Change | Mean reduction, bpb |
|---|---:|
| U1, nonzero initial weights | 0.0216973081 |
| U5, higher early learning rate | 0.0124736545 |
| U3, fewer selected mixer contexts | 0.0119656279 |
| U2, shared match confidence across previous bytes | 0.0015533971 |
| U4, extra order-0 input | 0.0014837224 |

U1 reduces G versus U0 on all eight primary labels and alone reaches the 0.002 threshold on 5/8. This is a measured effect of a concrete change in this codec, and a better supported explanation of this run than the original prediction that U2 would dominate.

In the full-UA leave-one-out comparison, removing U1 has the largest **mean** penalty, **0.0024498864 bpb**. It is the largest penalty on seven labels; ranked DCLM is the exception, where removing U5 hurts most. Removing U2 slightly improves mean G by **0.0000205346**, although U2 alone improves on U0. These conditional comparisons show why effects should not be treated as additive or globally ordered.

## Secondary results and threshold precision

| Source | UA G, bpb | Pointwise 95% window-bootstrap interval |
|---|---:|---|
| Gutenberg | −0.0004293869 | [−0.0005169539, −0.0003170757] |
| ripgrep Rust | 0.0020193854 | [0.0012636275, 0.0030074073] |
| lodash JavaScript | 0.0025944093 | [0.0017512445, 0.0035531576] |
| JSON countries | 0.0261107326 | [0.0250310782, 0.0271931447] |

Rust is just above 0.002, so rounding to 0.0020 must not turn the frozen failure into a pass. Its interval crosses the threshold, as does lodash's; the point-estimate count is a protocol rule, not a claim of sharp statistical separation. JSON countries retains a materially larger positive gain, and the broad secondary criterion fails. These intervals are pointwise window-bootstrap summaries, not simultaneous guarantees over independent corpora.

The secondary corpora were previously evaluated in B106. Preserve that exposure; “held out from choosing these B115 changes,” if true, is narrower than newly unseen evaluation data.

## Standalone superiority and incremental gain are different results

All 12 variants, including U0, have lower H than the evaluated learner ensemble on **all 12 row sets**. U0's advantage ranges **0.3003753–1.4664608 bpb**; UA's advantage ranges **0.4070416–1.5695875 bpb**. These are corpus-mean nominal log-loss comparisons under the stated conditions, not throughput, cost, or full-archive benchmarks.

UA lowers its own H versus U0 by **1.36237–6.91543%** across the 12 row sets. Thus it is a better standalone predictor in these comparisons while still leaving complementary learner gain in several corpora. This is not contradictory: a predictor can have lower average loss and still benefit from another predictor on selected portions of the stream.

The most accurate response to “a basic compressor that beats them” is therefore that the original codec already wins the measured standalone comparison; the new result concerns reducing the remaining complementary gain. Claiming that the upgrades fully absorb the learners across the tested sources would contradict P2 and P5.

## Codec-correctness validation

After the owner's worker process had finished, ran a bounded correctness regression using the pinned existing binary, without generating new research scores: all **12 variants × 3 deterministic fixtures = 36** exact compression/decompression round trips succeeded. Fixtures were empty input, three repetitions of all 256 byte values, and a 4095-byte ASCII repetition. The nonempty cases cross the early-rate boundary; all leave-one-out variants are included. Encoder and decoder were given the same predetermined mask and memory option.

Only owned temporary files were written and they were removed automatically. No experiment input, source or result directory was modified. `ROUNDTRIP.json` records input/output hashes, mask and binary hash; `check_roundtrip.py` reproduces the check. This validates these cases, not every possible file, architecture or compiler. The archive still requires externally agreed LPAQ_UP because the variant is not recorded in its header.

## Scientific scope and artifacts

This constructed codec lacks paq8px's dedicated morphology/Text module, but it retains ASCII word structure, an adaptive mixer and probability calibration. Its successful reductions cannot identify which original paq8px pathways caused B114's result. The source corrections are retained as a post-run addendum; the four failed prespecified predictions remain failures.

Evidence: `check_results.py`, `RECOMPUTED.json`, `CHECKS.json`, `DESCRIPTIVE.json`, `SUMMARY_CHECKS.json`, `PER_WINDOW.json`, input/source manifests, and the round-trip artifacts. Saved-data audit and the bounded codec correctness check completed successfully. No training, learner inference, cloud job, new benchmark score, or research-direction change was introduced.
