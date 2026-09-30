# B104/B105 completed-artifact audit

The saved numeric results reproduce; several narrative claims require correction. Only completed arrays were analyzed. No compressor, learner, generation, network or cloud job was run.

## Numerical closure

B104: all720 numeric fields agree to2.32e-15. All170 matrices (34 row sets x5 levels, 42,110 evaluated windows across levels) have correct shapes, finite nonnegative bit losses and matching historical inputs. All170 independent positive-share mixture comparisons agree to4.80e-14 at row level. The170 worker log records report full alignment and a successful logged-bits/file-bits bound for all rows. Raw logged bytes, archives and per-row margins were not retained, so those last checks remain worker attestations rather than independently replayed alignment/accounting. Source/protocol are the originally announced masks, not a repaired intervention.

B105: all214 numeric fields agree to4.00e-15, using an independently computed log-gain formula over the18 frozen weights. All34 learner and24 domain-assigned bGPT comparisons use historically pinned probabilities, row identities and B98/B99 archives. All26 benchmark row sets are fully aligned; ELF uses170 of256 windows in B105, whereas B104 uses256. Comparing those ELF results without a common population is invalid. Current dependencies and outcome files stayed unchanged through analysis.

## B104 results and scope

P1 FAIL0/8; P2 PASS8/8; P3 FAIL0/8. All40 T-label/level gains have positive pointwise bootstrap lower endpoints. These are pointwise row intervals conditional on the fitted ensemble and do not establish simultaneous coverage or training-seed uncertainty.

Full L5 learner gains range from0.0085165399 on raw DCLM to0.0552234211 on Metamath. Both the positive gain and all frozen failures must remain. The claim that full lpaq1 leaves a measured gap for these learners is supported. The original lower masks still retain higher-context selector/shared-state paths documented in ../c180_b104_source_review/; 'orders1–4 removed most of the signal' is not a clean component attribution. None of the eight labels crosses the frozen threshold even under that imperfect mask intervention, so the proposed sufficiency prediction fails as implemented.

C183's broad 'audio/image/new sources0.13–1.14' range is not correct for all named categories: HWC L5 gain is1.2825272186, while new German Wikipedia has0.0122989674. Use the exact per-label table. The table represents ideal log-loss reductions under the specified combiner, not actual encoded hybrid savings or absence of useful model structure.

## B105 results and corrections

O1 PASS8/8; O2 PASS8/8; O3 PASS7/7. These threshold results stand.

The 'all eight have alpha=0' claim is false: ranked DCLM selects alpha=.01 with corpus gain0.0007566386 and window gain0.0008935460. The other seven T labels select alpha=0 corpus-wide. Every T label has a strictly positive finite-grid window gain; seven are small, about5.02e-6 to2.48e-5, while ranked DCLM is larger. Thus 'no static weight even per window lowers loss' is not the recorded result.

The maxima narrative also omits glibc_rand corpus gain0.0084208827 and astronomy0.0037256151. Both exceed the claimed 'all others<=.0012' after the four listed examples. Numerical arrays and frozen threshold outcomes themselves are consistent; the problem is the prose summary.

Let G(a)=mean(log2(1+a(p/q-1))). The implemented oracle maximizes G over18 weights, not the interval[0,1]. A grid maximum upper-bounds choices restricted to the same grid; it LOWER-bounds the continuous maximum. This direction cannot be reversed. A static oracle also does not upper-bound adaptive/context-dependent mixtures. Window hindsight optimization is not a causal predictor and excludes the cost/rule for choosing each window's weight.

### Added correctness certificate, separate from frozen predictions

As a bounded arithmetic check of the zero-optimum claim, I computed G'(0)=mean(p/q-1)/ln2 from the same saved arrays. G is concave in a because each log of a positive affine mixture is concave. Therefore G'(0)<=0 certifies that a=0 maximizes the continuous corpus objective on[0,1]. No alternative predictor or new optimization experiment was run, and this check does not replace the frozen grid criteria.

| T label | Corpus G'(0) | Zero continuous corpus optimum |
|---|---:|---|
| metamath | -0.0996478670 | yes |
| C source | -0.2246038468 | yes |
| python | -0.1405979300 | yes |
| arxiv math | -0.1310967954 | yes |
| raw DCLM | -0.1476219027 | yes |
| Common Crawl | -0.1732044327 | yes |
| Kolmogorov text | -0.0941916552 | yes |
| ranked DCLM | +0.1957851834 | no |

Thus the stronger continuous **corpus-level** claim can be supported for7/8 T labels by this separate derivative certificate, not by the finite grid alone. This is a numerical certificate for the retained probability values, conditional on the payload comparator, data and model configurations. It says nothing equivalent about all per-window weights, all dynamic combiners or the information available in model representations. Keep the ranked-text exception.

## C181 paq accounting

Recomputed across all6,374 aligned benchmark windows: full file bits minus main+other logged bits ranges63.0422451–71.9647975 bits/window, mean67.4778109. Other logged bits average63.0603732. This confirms the announced descriptive accounting. Main-only losses omit both components. The arithmetic does not make the paq payload prefix-causal or charge for model/weight selection in a hypothetical hybrid codec.

## Forced-mode proposal

The pinned upstream code supports a forced TEXT/DEFAULT path that bypasses recursive block detection; those two block types have no transform. That is a relevant follow-up, but a standard-versus-forced difference also changes segmentation/model routing and is not an isolated measurement of look-ahead value. Mode assignments, exact flags, input identity, aligned populations and header/payload accounting must remain explicit. No forced-mode job was dispatched here. The subsequent B106 protocol/runner are reviewed separately.

Artifacts: B104_RECOMPUTED.json, B105_RECOMPUTED.json, CHECKS.json, B104_ROW_RESULTS.json, B105_GRID_AND_ROW_RESULTS.json, ALIGNMENT.json, ARRAYS.json, source snapshots and dependency hashes. Historical checkpoint/probability identity is reused; no weight files were loaded or rehashed. Only this owned audit directory and the append-only channel were written.
