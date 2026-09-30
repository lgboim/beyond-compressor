# Independent saved-artifact review: B110, B111, B112

## Verdict

All 778 reported numeric fields independently reproduce, with maximum absolute discrepancy 1.087671619437458e-15 and no mismatches. This verifies the completed saved-array calculations, not a rerun of inference or training. The original B110/B111 admission failure remains a failure; their corrected analysis is admissible only as an explicitly amended/descriptive analysis. B111 additionally has a three-member loss_delta ensemble instead of the protocol's four. B112 satisfies the actual parity gate, with Z1 and Z2 passing and **Z3 failing**.

The audit imported no owner runner, started no model/cloud job, and changed no experiment output, protocol, reference or manuscript. The independent implementation and evidence are in this directory.

## Evidence and coverage

- `audit_saved.py` independently implements the positive-share mixture using probability-space posterior updates, rather than the owner's log-odds implementation. It checks every reported value and criterion against pinned output snapshots.
- B112: all 672 arrays in 48 B97 archives; six sizes, eight seeds, seven labels, raw and calibrated true-byte probabilities. All are finite float32 arrays with expected shapes and probabilities in (0,1].
- B110/B111: all 900 arrays in 75 archives, with complete 12-label key sets and expected seed counts. The manifest has 75 unique checkpoint paths and reported hashes, with matching archive inventory.
- Historical B97 probabilities and B98 bit arrays match prior independent hash pins. Dependencies were rehashed after calculation and remained unchanged.
- Current B75 input sequences and B88 raw rows are byte-identical in content and order for all 13 labels in the union. All corresponding B98 rows are aligned and finite. Ranked DCLM has 250 rows, audio_8bit 240, melody 17; the others have 256, each with 4,095 scored bytes.
- Canonical B111 and B97 raw probabilities are bitwise identical on all **six shared labels** for each of four seeds: 24/24 array comparisons, zero loss difference. Correction to C1201: B97 contains seven labels, but melody is absent from B110/B111; the intersection is six, not seven. The owner's parity loop checked four and omitted audio_8bit and musicnet_pcm8; the independent check covers both omissions.
- Figure 3 endpoint loss parity is within 5.96e-6 for the four cells. This is aggregate numerical agreement, not proof of byte identity with historical inference inputs.

See `CHECKS.json`, `ROWS.json`, `ARRAYS.json`, `DEPENDENCIES_SHA256.json`, and the two `*_RECOMPUTED.json` files. Input and output manifests bind the source/result snapshots and this audit's outputs.

## B112: calibration before seed averaging

This calculation averages the eight separately calibrated members' true-byte probabilities, then applies the same paq mixture with share 0.001. It does not calibrate the final ensemble. B97's finite temperature family is {0.7, 0.8, 0.9, 1, 1.15, 1.35, 1.6, 2}, with its causal per-member adaptation.

| Criterion | Independent result | Outcome |
|---|---|---|
| Z1: calibrated ensemble G <= 0.002 on three text/formal labels at six sizes | 18/18; maximum +0.00002327751877085582 | PASS |
| Z2: G increase > 0.002 in at most three of 42 cells | 0/42 | PASS |
| Z3: absolute HWC 24M G change <= 0.005 | 0.0053344622960226976 | **FAIL** |

For Z3, raw G is 0.014332291893181512 and calibrated G is 0.008997829597158983: calibration reduces the gain. G decreases in 40/42 cells. The calibrated ensemble's own log loss is higher in 40/42 cells; the two exceptions are ranked DCLM at 100k and HWC at 100k. This independently confirms C217's correction of C216's 41/42 count.

All 42 raw-ensemble references to the previously audited B101 calculation are present and reproduce, maximum difference 2.43e-17. The source's optional reference check is not fail-closed when a reference is absent, but no reference is absent in this completed calculation. No rerun is needed to close this particular coverage issue.

Interpretation: per-member calibration and ensembling are not interchangeable operations. The observed worsening after averaging calibrated members does not contradict an earlier improvement in mean individual-member loss. "Over-hedging" is a possible explanation, not an identified mechanism from saved true-byte probabilities. No ensemble-level calibration or exhaustive calibration family was tested. Z1/Z2 are threshold results, not statistical equivalence or proof of absent predictive information. Preserve Z3 FAIL and the exposed-data status.

## B110/B111: admission and seed count

The original frozen shape gate required [256,4095] arrays. Its 150 errors are precisely two shorter labels across 75 checkpoints, and `battery110_gate_as_specified.json` reports inadmissible. The analyzer nevertheless printed criteria before correction. The later shape change to the B98 row counts is therefore a **post-outcome admission amendment**. All reported cell values and criteria are identical in original and corrected outputs.

The independent inventory and current input identity checks support interpreting the shape issue as a specification error. They do not make the original gate pass or restore an unamended prespecified analysis. Keep the original output and failure, state the amendment explicitly, and label amended/descriptive conclusions accordingly.

B110 has six curriculum arms with eight seeds each. B111 has four seeds in canonical, signed, shuffle, last_step, negate and uniform, but only three in loss_delta. The primary paper's Table 5 footnote explains that a loss_delta seed stopped at round 2587 and the published ensemble excludes it. That explains availability; it does not satisfy the B111 protocol's four-seed specification. No current hub inventory was independently retrieved in this audit.

W1 and W3 include the unequal-K arm and must disclose it. W2 uses only canonical, negate and uniform, all K=4, so its specified seed contrast is unaffected; the common shape-gate amendment still applies. Do not relabel all seven B111 arms as E4. Neither another cloud run nor deletion of the failed gate is needed.

## Recomputed B110/B111 outcomes

| Battery | Criterion | Independent result |
|---|---|---|
| B110 | C1 | PASS, 48/48 at or below 0.002; required 46 |
| B110 | C2 | PASS, both image layouts have endpoint G above G0 |
| B110 | C3 | PASS, planar curriculum-rank Spearman 1.0 |
| B110 | C4 | PASS, 7/8 text/formal labels with G range <= 0.001; ranked DCLM is the exception |
| B111 | W1 | PASS on observed counts, 56/56; required 54, including the K=3 arm |
| B111 | W2 | PASS, 4/4 canonical contrasts against negate/uniform |
| B111 | W3 | PASS on observed counts, HWC own-loss/G Spearman -0.8928571428571429 |

B110 planar G increases approximately from -0.00093 through 0.00005, 0.00062, 0.00156 and 0.00200 to 0.00264. HWC increases from approximately -0.00095 to 0.00447. DCLM own loss changes markedly (8.184, 5.963, 5.043, 4.829, 4.841, 4.947), while G stays near -0.00096. Audio/MusicNet gains are positive from T256. These are descriptive trajectories for released 1M curriculum learners; a curriculum endpoint denotes the endpoint of the 16-snapshot generating corpus, not a matched learner training checkpoint.

In B111, positive image G occurs only for canonical (approximately 0.0078 HWC and 0.0048 planar) and signed (approximately 0.0025 each); the other five arms are at or below zero on both layouts. The association between own loss and incremental gain is verified, but it is not a universal reward mechanism or identification of training-derived unique information. W1/W3 also retain the unequal ensemble-size limitation.

## Remaining provenance and interpretation limits

Worker checkpoint SHA values are recorded but were not independently redownloaded. The saved metadata does not fully capture resolved model configuration, strict=False load-key diagnostics, or a complete binding of executed source and input bytes. B97's per-temperature/full-distribution trajectories were not saved, so the original pcal generation cannot be independently replayed from pcal alone. This audit validates their pinned provenance and downstream calculation, not every inference step.

The paq conditional-payload, side-information and fixed-combiner limitations from earlier reviews remain. No claims about current cloud billing, orphan jobs, production deployment, inference reproducibility or manuscript readiness follow from this saved-artifact review.
