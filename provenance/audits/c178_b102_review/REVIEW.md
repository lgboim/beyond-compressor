# C178 / B102 completed-artifact and joint-gate review

The saved B102 outcomes and parity records independently reproduce. All five frozen criteria A1/A2/A3/B1/B2 pass. This supports a descriptive training-round trend and a released-arm performance difference on these rows, not a causal explanation of the adaptive generator or a general scaling law.

## Numerical and structural closure

- Recomputed every numeric field in battery102.json: 237 fields, maximum absolute error 1.78e-15, no mismatches. All 128 numeric fields in the separate B102 gate JSON match exactly.
- Checked all 80 intended archives, 480 probability arrays, six labels, exact seed identities and manifest entries. Every array has the expected row count and 4095 columns, finite values in [0,1], and no zeros. There are eight seeds per 24M round and four per 3M/6M arm. All 80 checkpoint paths and SHA formats are complete, with 80 distinct reported hashes.
- Reconstructed 72 mixtures independently. Their row-loss maximum difference from the frozen positive-share implementation is 3.20e-14.
- Original A parity: 32 seed/label comparisons, maximum mean difference 7.00e-8 and row difference 1.45e-6 bits/byte. Added B parity: 32 comparisons, maxima 2.00e-7 and 1.07e-6. Both satisfy mean <=1e-4 and row <=1e-3, including the stronger per-row check missing from the original B diagnostic.
- Six current local input files and their ordered rows match earlier B77 pins and B88 row arrays. Counts are 256 except audio_8bit, which has 240. All selected B98 comparator parts match earlier pinned hashes, cover those exact row counts without gaps and report full alignment.
- Source/protocol and gate-script hashes match C174/C176/C178. Completion/EXIT 0 appear in both run logs. The original acquisition amendment remains explicitly post-exposure to the first printed 3M/HWC row; outcomes/formulas were unchanged.

## Frozen criteria

| Criterion | Recomputed | Result |
|---|---|---|
| A1: CIFAR HWC Spearman over rounds 256..8191 >=.8 | 0.8928571429; average-rank calculation, all seven gains distinct | PASS |
| A2: formal/text gain <=.002 at every round | 16/16, maximum -0.0008504845 | PASS |
| A3: final gain exceeds round-256 gain, two audio labels | MusicNet +0.0054597061; audio_8bit +0.0017450994 | PASS |
| B1: self-play exceeds uniform mixture gain on HWC at both sizes | 3M +0.0044163537; 6M +0.0076170742 | PASS |
| B2: self-play own loss better at 6M on >=4/6 labels | 6/6 | PASS |

Self-play own loss is lower on all six labels at 3M as well; that is descriptive, beyond the B2 prediction. The uniform arms' largest mixture gain is 0.0002943539 bits/byte, while self-play HWC gains are 0.0035005462 at 3M and 0.0066785742 at 6M. Both arms average four seeds at the same published size and final round.

## Preserve nonmonotonicity and the exact threshold claim

For the 24M eight-seed ensemble, HWC gains at rounds 0,256,512,1024,2048,4096,6144,8191 are:

    -0.0005204764, -0.0006677375, +0.0000461407, +0.0038273849,
    +0.0137467213, +0.0155928665, +0.0156185227, +0.0143322933

MusicNet peaks at round 2048 (+0.0066112071) and ends at +0.0051282849. Audio_8bit is already positive at round 256 (+0.0018626206), dips at 512, and ends at +0.0036077200. Thus 'gains first appear at rounds 1000–2000' is too broad: that interval captures the larger image gains, while some positive audio values appear earlier. 'Then plateau' has not been tested as an equivalence/saturation claim, and several curves decline. Prefer the actual sampled trajectories and final-minus-256 criterion.

All 16 formal/text point estimates are negative for this specified combiner. State this exact observation and the <=.002 pass; do not infer that the model has zero useful information, or that no other combiner can extract gain. No B102 confidence intervals, equivalence test, individual-seed gain analysis or uncertainty in the trend were frozen or added here.

Round is a training-stage index, not a measured compute/cost accounting axis. At a fixed nominal size and round, these released arms differ in training regime. This audit has no matched replay that isolates adaptive generation from all training mechanics, diversity, optimization and effective budget. 'Released self-play outperforms released fixed-prior training here' is supported. A component-level causal claim that adaptive generation specifically explains the difference is not established by this comparison alone. These are follow-ups on already examined natural labels and comparator choices, not an untouched confirmation set.

## Provenance boundaries

Sixteen B102 checkpoint hashes match B97 reports; sixteen match B103 reports; their union covers 20 unique B102 checkpoint entries. Ten have the previously independently known B97 status. Sixty checkpoint reports have no matching report in those two compared records. All remain worker-reported hashes; no weights were loaded or freshly rehashed here. Worker metadata contain both NVIDIA A10 and A10G and torch 2.14.0+cu130; runtime is not a dollar/energy measurement.

B102 workers call the unchanged official corpus loader but discard its returned provenance. They also omit resolved architecture and missing/unexpected load-key diagnostics. Current local input/hash identity and terminal parity cannot reconstruct missing worker-time attestations, especially for intermediate rounds and the two newly added labels. The source-stage review documents this limitation.

The paq comparison remains a conditional-payload log-loss comparator with its documented side information. G measures realized reduction under the specified share=.001 combiner. No interoperable hybrid codec, deployment performance or speed/cost claim is established.

## Joint B102/B103 gate: realized pass, implementation limits

Both saved gate records agree with independent checks of the realized completed inputs. B103's existing audit is unchanged: 24 arrays, exact 256-row identity, finite/nonnegative paq bit arrays and 256 reported aligned rows. Its main-only coding bound passes, but missing other-bit logs prevent the fuller B98 accounting test.

The separate gate script is not an automatically fail-closed pipeline: it writes false flags but does not raise or prevent the separate analyzers from running. Its live release-derived seed list has no explicit intended-count assertion. B103 alignment count is reported but not included in pass; paq bits shape/finiteness are not checked there. B102 manifests and corpus hashes are not validated by that gate. The stricter independent audits above close these checks for the **actual complete saved data**, so these source gaps do not overturn the present numerical conclusions. For future reuse, wire complete intended-count, alignment, numeric, manifest and input-identity checks into acceptance, and stop on failure; no further paid computation is needed to clarify this distinction.

Claude reports the gate was run before personally reading B102 outcomes, although the pre-gate analyzer had already computed them. This chronology was not independently attested; the earlier printed-row exposure and acquisition amendment remain in the record.

Evidence: RECOMPUTED.json, CHECKS.json, GATE_RECOMPUTED.json, ROW_RESULTS.json, INPUT_IDENTITY.json, ARRAY_VALIDATION.json, CHECKPOINTS.json, INPUT_SHA256.json and DEPENDENCIES_SHA256.json. No model/inference/generation/compression/cloud job, download or live repository query was run. Only this owned audit directory and the append-only research channel were changed.
