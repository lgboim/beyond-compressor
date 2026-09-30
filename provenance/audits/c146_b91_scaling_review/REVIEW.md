# C146-C148: B91 saved-data audit and B92 source review

The B91 numeric output reproduces, but v25 attributes its strongest failure to the wrong fitting procedure. This is a material framing correction before submission. No owner runner was executed or imported; no inference, cloud call, download, training, listener, or modification to runs/refs/manuscript was performed.

## B91 numerical reconstruction

Both frozen B91 hashes in C146 and both B92 hashes in C147 match the pinned copies. `INPUT_SHA256.json` records the inputs. `recompute.py` independently builds a single global Pareto envelope from all eligible tagged raw points, computes log-space OLS through centered covariance, and separately fits the prescribed bounded floor function with SciPy. It does not call the owner runner or its frontier/fit functions.

All checked saved numerical fields agree, maximum scaled discrepancy 4.37e-14; no mismatches. Results are in `RECOMPUTED.json` with the retained points and rung provenance.

- E1 fails: 1/26 prespecified labels, 22 evaluable, 1/22 within 0.10 bits/byte. Pure-law prediction-minus-observation is negative for all 22; median -0.4361387940, range [-0.7099660625, -0.0412431577]. It underpredicts loss, equivalently overpredicts improvement.
- G1 fails: 2/24 require more than 100 times the corpus-specific frontier maximum in the fitted pure law; the median formal inversion is 7.8725525088. E1's failure prevents a supported compute forecast under the frozen rule.
- G2 holds as a fitted-parameter count: 13/24 floors are at least paq's rate. This is not a demonstrated asymptote or impossibility result.
- The floor procedure is within 0.10 on 6/22, with median error -0.1994180971 and range [-0.4457727084, +0.2195060040]. Its errors are negative on 13 and positive on 9, not uniformly optimistic.
- The three descriptive slopes in v25 reproduce: raw DCLM -0.047588 versus smaller-rung -0.070753; Metamath -0.060729 versus -0.138075; ESC-50 -0.013790 versus -0.105387. These are selected descriptive examples, not a separate frozen prediction.

## Required attribution and protocol clarifications

1. **The authors' Figure 1 and Table 2 use the floor law, not the pure log-space law.** The captured `fig1_overview/fig1.py` imports and calls `fit_curve_power_law_with_floor` (call at line 87). `make_latex_table.py` uses the same procedure. `fit_log_power_law` is a diagnostic available in their helper module; that does not make it the fit used in their figure. Replace v25's abstract/intro/Section 3.1 wording attributing the all-22 result to "the paper's own power law", and the appendix's "their Figure 1 law". Attribute the all-22 failure to the tested no-floor diagnostic. Report the actual Figure 1 procedure separately as 6/22 within tolerance with mixed error signs. The stated rule still bars a reliable crossing headline.
2. **Five smaller rungs, not four.** Default construction includes `d64h1L1`, with actual N=65,728, as well as approximately 500k, 1M, 3M and 6M. It contributes retained frontier points on all 26 labels. The abstract's "four smaller model sizes" and protocol/appendix's "500k-24M" do not describe the computation. Preserve the frozen script and protocol, explicitly disclose the description discrepancy, and describe the as-run analysis correctly; do not silently re-freeze or replace outputs.
3. The frozen protocol's threshold is the first actual 24M frontier point, while the runner uses compute strictly beyond the omitted-rung frontier's maximum. Only arithmetic changes the selected subset (15 versus 9 points), and the minimum target and its compute are identical on every evaluable label. Thus the primary E1 result is unchanged by that wording discrepancy. Four labels have no qualifying 24M target: protein, astronomy, DNA and KoLMogorov DNA. Keep both 26 planned and 22 evaluable denominators.
4. "All fits are extrapolations beyond observed compute" is too broad. The pure inversion is already below retained frontier Cmax for atlas float32 (0.4318) and astronomy (0.3425), despite paq being below the observed minimum. Those are within-range curve/observation discrepancies, not actual demonstrated crossings. Say "model-based curve inversions, mostly beyond the retained frontier" and distinguish predictions from observations.
5. G2 cannot establish an irreducible barrier. Five of its 13 favourable-label floor estimates exceed a loss already observed on that same frontier: DNA, KoLMogorov DNA, ESC-50 11 kHz, Speech Commands and Speech Commands 8 kHz. The sixth such floor overall is pseudo-random data, excluded from the 24 paq-favourable labels. This mirrors the earlier B73 fit-quality limitation.

Compute is the released K*N*1536*4096*(round+1) proxy, not total generator/reward FLOPs or wall time. Cmax is corpus-specific maximum retained Pareto compute, not necessarily maximum evaluated compute. The frontier changes checkpoint, ensemble size and model size. Holding out one size is useful, but these results neither falsify observed transfer nor establish that more training cannot help. The 22 labels are not independent replications of a universal scaling theorem.

Suggested scientific wording: "A no-floor power-law diagnostic fitted without the largest model underpredicted its frontier-minimum loss on all 22 evaluable labels. The floor-law procedure used in the released Figure 1 was within 0.10 bits/byte on 6/22, with errors in both directions. These held-out-size checks do not validate an estimate of the compute needed to match the compressor."

## v25 delta and visual check

Every one of v24's 369 table lines is still present; five lines are added for the B91 table including repeated header/separator lines. Section 3.1 fixes the B90 batch-amortized timing wording. The shortened Figure 2 titles fit in the pinned PNG and rendered v25 PDF page 9; the earlier title overlap/clipping is closed. This is a bounded delta/sample check, not full-document certification. The deferred supplement refresh has not been re-audited here.

## B92 source-only boundaries

Both files parse and match the announced freeze. The runner specifies the 2,000 sampled 2048-byte chunks, fixed seeds, paq commit/level, full-file primary sizes, and frozen online implementations. It has not been launched by this audit and no completed B92 output is claimed.

- The `once` calculation subtracts each compressor's one-byte-file size minus one for all but one chunk. This is a reference accounting adjustment, not an observed one-header archive or measured fixed header size; retain the distinction established for B89. Full files are the primary real-code result.
- The source reports intervals only for compressor full-file rates, not online predictors or `once`. Do not imply intervals were supplied for every arm.
- Before accepting completed summaries, validate exactly 2,000 unique chunk indices, expected chunk coverage/lengths and 32 compressor records, all positive file sizes, consistent header references, and 2,000 finite totals per online method. The summary function itself does not enforce those checks.
- Build metadata records archive hash and sampled-byte hash; it does not return the decompressed corpus hash or worker input/binary hashes. It also performs no codec round-trip verification. Source/selected-input provenance is not binary execution attestation.
- Wikipedia-trained model rates are published unpaired references. T2/T3 can supply a balancing case, not establish that language models beat "any general-purpose compressor" or isolate an offline-pretraining effect. Python's default LZMA compression includes its XZ container; state the actual implementation and full-file accounting.

No changes to frozen sources or another run are requested. Fold factual reporting corrections into the already planned manuscript/package update.
