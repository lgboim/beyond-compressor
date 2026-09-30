# B97 independent completed-artifact audit

## Verdict

The announced protocol and runner hashes match. All 630 numerical fields checked across the main result and post-hoc temperature table reproduce, maximum absolute error 1.24e-14. All three frozen outcomes pass: D1 7/7, D2 5/7, D3 median -0.0469457213. This is verification of the saved probabilities and their analysis, plus source review, not an independent GPU replay.

## Inputs, gate and provenance

48 archives contain exactly the expected 672 arrays (p1 and pcal for seven labels in each of eight seeds and six sizes), total 2,206,265,697 bytes. Every array is finite, positive, at most one and has the expected float32 shape. All input hashes and row counts match historical records. DCLM-ranked has 250 rows, audio has 240, melody only 17, and the other four labels 256; do not describe all as 256-row results.

All 81 expected saved-B75 comparisons pass: maximum absolute difference of label means 0.00000979614 bits/byte; maximum row difference 0.00012283549. The stored 'mean_abs' field is abs(mean difference), not mean(abs(row difference)); a supplemental calculation of the latter also passes the mean threshold, max 0.00001473030. Historical B75 probability and V_match array identities match. Archive/dependency hashes were checked again after reconstruction and remained unchanged.

All 48 checkpoint metadata records have unique SHA-256 values and expected paths. Twenty hashes match previously independently pinned checkpoints. Twenty-eight are new worker-reported hashes and were not independently re-downloaded or rehashed from weights in this audit. Worker metadata names both NVIDIA A10 and A10G; summed worker-reported duration is 1,402.3 seconds, which is not measured end-to-end wall time or a bill. The saved local log ends with RUN DONE, app completed and EXIT 0 after an aclose exception. This supports local completion, not an independent guarantee of no orphan jobs or actual billing.

The worker follows predict-before-update calibration, resets mixture state by row and normalizes the full vocabulary at each temperature. The code matches the reference's loading pattern, including strict=False. Resolved architecture config contents, missing/unexpected load-key results and per-temperature probability trajectories were not retained in the result. Saved p1/pcal log losses match their reported diagnostics within 2.46e-10; pcal's full recurrence cannot be independently replayed from per-temperature aggregate losses alone. These are reproducibility limits, not observed numerical mismatches. Do not launch new inference to close them without applicable authorization.

## Frozen outcomes

D1: Spearman correlations of size with eight-seed gain are 1.0 for Metamath, C source and MusicNet; 0.8857143 for ranked text; 0.9428571 for CIFAR and 8-bit audio; 0.8285714 for melody. All exceed the frozen 0.8 threshold. This is rank association across the measured six sizes, not monotonic improvement at every step or a power law. Fixed rounds do not hold compute constant across sizes. G2/G4 use the first seed subsets, whereas G1 averages all individual seeds.

D2: eight nominal-3M models exceed mean single-24M complementarity on 5/7. The exceptions are CIFAR and MusicNet. The release's parameter counts give 24,135,680 versus 24,255,488, ratio 0.99506058: approximately matched parameter budget, not exact equality. The authors' proxy already counts ensemble members; this does not establish a new general compute frontier, equal measured latency, full training FLOPs or equal cost.

D3: all seven operational ratios are negative, range -0.1560382 to -0.0106193, median -0.0469457. The tested online temperature calibration slightly lowers single-seed complementarity with V_match. It also lowers G8 on all seven labels. Negative values are signed contrasts, not negative causal 'fractions explained'.

## Post-hoc diagnostics and interpretation

At 24M the configured online calibrator improves mean single-model own loss by 0.0465341–0.0922441 bits/byte; averaging eight improves it by 0.5511690–0.9586483. The post-hoc finite-grid best-fixed-temperature table reproduces as well. These are useful descriptive checks showing that the intervention does improve its own log-loss objective, while substantially less than averaging.

However own-model loss and complementarity with V_match are different objectives. Improvement on the first does not certify that the calibration procedure is optimal for the second or that all calibration effects have been removed. The result concerns this finite temperature grid, online share setting and comparator; replace 'any temperature correction' or an unqualified exclusion of temperature miscalibration with 'this specified temperature-calibration family does not account for the observed ensemble advantage'. Conditional/context-dependent calibration and other diversity effects remain possible. No unique knowledge, semantic understanding or causal pretraining mechanism is identified.

B97 adds an eight-seed size comparison; it does not repair, replace or overturn the frozen single-seed B93 P2 failure. It also covers only one of B93's two MusicNet representations. Keep both results, with their different estimands. The seven labels and fixed released seeds are the studied set; no seed-resampling or population-level uncertainty for the size correlation or D2 counts is supplied.

## Scope

Outputs: RECOMPUTED.json, POSTHOC_RECOMPUTED.json, CHECKS.json, CHECKPOINTS.json, ARCHIVES.json, OWN_LOSS.json, GATE_MEAN_ABS_ROWS.json, DEPENDENCIES_SHA256.json and pinned source/results. Original 2.2 GB archives were read and hashed in place, not duplicated or altered. Only audit and channel files were written. No inference, cloud/API call, download, listener, new task or run-directory write.
