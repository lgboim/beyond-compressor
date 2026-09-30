# C177 / B103 completed-artifact review

The saved results reproduce. All three frozen predictions fail; the small positive mixture gain is also real on the evaluated rows. This is a numerical audit of completed files, not a new generation, model, compression or cloud run.

## Verified results

All 38 numeric fields in battery103.json match independent reconstruction to 2.12e-16. An independently implemented positive-share recurrence matches the saved source's mixture row losses to 2.49e-14. H1 requires the 24M own loss to beat paq payload by at least 0.3 bits/byte; its actual difference is +0.0510770374, so FAIL. H2 requires G >= 0.1; actual G is +0.0152660528, so FAIL. H3 requires uniform 6M own loss below self-play 6M; uniform is worse by 2.6416961594, so FAIL.

| Quantity | Verified bits/byte |
|---|---:|
| paq conditional payload | 0.2533594560 |
| paq complete archive | 0.2848137973 |
| 24M / 8 seeds own loss | 0.3044364934 |
| 24M own loss minus payload | +0.0510770374 |
| Its pointwise row-bootstrap 95% interval | [0.0422964507, 0.0595382408] |
| 24M mixture gain over payload | +0.0152660528 |
| Its pointwise row-bootstrap 95% interval | [0.0120829313, 0.0188196263] |
| self-play 6M / 4 seeds own loss | 0.3292872850 |
| uniform 6M / 4 seeds own loss | 2.9709834444 |
| self-play 100k / 8 seeds own loss | 2.7964414650 |

All four arms have positive mixture-gain point estimates and positive pointwise lower interval endpoints. The complete paq archive also averages 0.0196226961 bits/byte below the 24M ideal own loss; this is a separate descriptive comparison, not a deployed hybrid codec result. Intervals condition on the selected rows and fixed ensembles; they do not cover checkpoint-training variation, all hypotheses jointly, or arbitrary program distributions.

## Inventory, identity and accounting

Verified all 24 finite probability arrays in [0,1], intended seed names and counts 8/4/4/8, and all 24 corresponding manifests. No probabilities are zero. The JSONL SHA-256 matches the C175 source-stage pin. Its 256 ordered 4095-byte rows exactly equal rows.npy, and all satisfy the retained nonconstant-tail predicate. There are 256 unique program strings and 255 unique exact output rows; one output is repeated twice.

The retained paq metadata report 256/256 aligned windows and the intended instrumented commit. The main logged code lengths are finite/nonnegative and fall below full archive bits on every row; the largest main-minus-archive margin is -124.161 bits. Other coded-bit sums were not retained, preventing B98's stronger total-log accounting check. Recompression and independent alignment replay were not performed.

Twenty reported checkpoint hashes match earlier B97 reports, 17 of which were already independently known there; four uniform-arm hashes are new worker reports. This audit did not load or rehash weight files. GPU corpus hashes match the pinned JSONL. Resolved architecture and missing/unexpected checkpoint load keys are not retained by this worker. Run logs contain completion and EXIT 0 after client cleanup exceptions; that does not independently attest absence of orphan jobs or billing.

## Scope of inference

The evaluated corpus is a **long-output, nonconstant-tail-conditioned local uniform-prior surrogate**: 256 accepted out of 130,517 reported attempts, or 0.196143%. The 256-cell tape, 200,000 primitive-step budget and output-survival filter differ from the released training setup; the learned generator's training stream is unavailable. Counts were read from saved generation metadata; rejected histories and random-input draws were not replayed. A comma opcode in 232 program strings is a syntactic observation, not proof those instructions executed.

This establishes predictive performance of the specified ensembles and combiner on these exact selected rows. It does not establish that the learner lacks program structure, that the measured gain comes from such structure, or that H3's failure is caused solely by a distribution mismatch. The design establishes a mismatch independently of H3's sign. These outcomes do not answer the counterfactual of removing a learned generator component while holding training mechanics and budget fixed.

Paq payload probabilities remain conditional on previously documented side information. Mixture loss is an ideal scored probability path, not an implemented interoperable codec or a measured speed/cost improvement.

## Later joint gate

C178's joint gate JSON is independently confirmed by c178_b102_review against unchanged B103 inputs/arrays and this stricter audit. The realized data satisfy alignment and numeric validation. The gate implementation itself only reports the aligned count without requiring 256, does not validate paq bits' shape/finiteness, derives expected seeds from an unpinned live listing without asserting the intended count, and emits false flags without raising or blocking the separate analyzer. Therefore describe this as a separately checked acceptance record, not an automatic fail-closed pipeline. These source gaps did not invalidate the complete saved B103 data checked here.

Evidence: CHECKS.json, RECOMPUTED.json, ROW_RESULTS.json, ARRAY_VALIDATION.json, CHECKPOINTS.json, INPUT_SHA256.json and DEPENDENCIES_SHA256.json. Earlier source-stage interpretation and pins remain in ../c175_b103_source_review/. No owner files or references were changed.
