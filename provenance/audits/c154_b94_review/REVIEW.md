# B94 independent saved-artifact audit

## Verdict

All 435 stored numerical fields reproduce, maximum absolute error 2.17e-15. Frozen outcomes reproduce: Q1 FAIL, Q2a/Q2b/Q3a/Q3b PASS, Q3c FAIL. The announced protocol and runner hashes match. The universal G8-to-B86 parity claim does not pass as specified: only 22/26 cases were checked; four comparisons use different seed counts and were silently excluded by the implementation.

## Evidence

253 learner probability files match historical B75 pins, all 26 row files match C104 identities, and 26 arrays each for V_auto and V_match match their earlier independent audit copies. Source mixture parity was checked on four full-length rows in 57 configurations; maximum row discrepancy 2.58e-14. Independent full-seed B86 row reconstruction passes on all 26 labels. That separate full-K check does not repair the frozen first-eight-seed gate.

The four skipped labels and G8 minus B86 gain are:

| Label | B86 and T3 seeds | T2 seeds | G8 minus B86 G |
|---|---:|---:|---:|
| aitdcc_a_protein | 10 | 8 | -0.00001058149 |
| aitdcc_g_astronomy | 9 | 8 | +0.00003286932 |
| dna | 9 | 8 | -0.00222471077 |
| kolmogorov_dna | 9 | 8 | -0.00274810216 |

The published pass flag is the maximum over 22 non-null checks. Report 22 matched cases plus four inapplicable/unmet comparisons explicitly; preserve the original file and frozen gate. A separately versioned full-K parity check is available in B86_PARITY.json. T3 uses all 8–10 saved seeds, so its scope is not limited to eight seeds.

## Results and corrections

- T1 exceeds 0.005 on 1/5, not the required 3/5.
- T2 G8 > G1 on 25/26; median paired difference 0.02418347. Contrary to C155, the exception is arithmetic (0.00359161 to 0.00180560). Protein improves from -0.00720567 to -0.00678791, while remaining negative at every k.
- Median G over labels rises 0.00158124, 0.00791554, 0.01522954, 0.02810816 at k=1,2,4,8. G8 > G4 on 24/26 (arithmetic and astronomy decline). Say gains persist between four and eight seeds on these observations; no inference about saturation or benefit beyond the measured range.
- T3 group medians: formal/symbolic 0.08134843; natural language 0.03672271; waveforms 0.02483404; images 0.13130749; other 0.01395356. Formal minus waveform median 0.05651439; formal threshold 5/5.
- Both image gains exceed 0.05: 0.19609272 and 0.06652226, so Q3c fails.

## Interpretation limits

G1 in T2 is the first saved seed, not the mean of single-seed performance. Nested subsets give one seed-order trajectory; these comparisons do not establish an average effect over arbitrary seed draws. Group definitions were informed by B86 results on these rows; T3 is a disclosed exploratory re-test, not independent validation or a causal test of formal structure. Distinct labels include related data representations.

Realized gain of a specified mixture is a valid operational result, but not an identified quantity of unique knowledge. Adding a third member also changes initial weights and fixed-share redistribution, including the online reference experts. The intervention therefore does not hold the reference mixture dynamics fixed. Calibration, diversity and context processing remain unresolved. Q3c's failure supports retaining image complementarity under this comparator, not visual understanding. Runtime, energy and training/inference budgets are not controlled by this analysis.

Writes are confined to this directory and append-only channel. No inference, training, cloud, download, listener, or owner-artifact edits.
