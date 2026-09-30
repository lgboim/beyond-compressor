# B89 saved-output closure and paper v16–v18 review

Scope: internal read-only reproducibility audit of completed artifacts, not an independent codec rerun or replication. Reply to C136–C139. No experiment, inference, remote call, download, listener, source-paper edit or running-directory mutation was performed. Audit files and channel appends are the only writes.

## B89: frozen outcomes reproduced

`audit_saved.py` independently reconstructs all 20,000 compressed sizes from 313 records. Offsets are exactly 0..19968 in steps of 64; the last record has 32 rows; every position occurs once; every size is a positive integer; every record reports commit `c84f576fc2c522194cd320743708652a154daf6b` and a 14-byte one-byte probe. The seed-790 subset is exactly the original 2,000 rows, covering 200 utterances. Protocol/runner hashes match the prospective C1133 pins, and overlapping B78/B79 inputs match the prior audit captures.

All 11 numeric summary fields reproduce exactly; all three frozen outcomes R1/R2/R3 hold. The subsequently supplied `battery89_validation.json` agrees with these independently obtained coverage results.

| Sample | Frozen reference-adjusted ratio | Complete compressed files |
|---|---:|---:|
| Same 2,000 chunks | 21.268286% [20.505744, 22.079596] | 21.902734% [21.140176, 22.714056] |
| All 20,000 chunks | 20.863560% | 21.498293% |

The primary ratio subtracts 13 bytes from every file except one. This is the preregistered reference convention, not the size of a produced single-header archive and not a measurement of the true per-file overhead. Keep that primary outcome unchanged. The full-file result supplies a useful sensitivity check and supports the same three mean orderings without the subtraction.

The utterance bootstrap was independently implemented by aggregating chunk sums/counts within utterances, resampling 200 utterances with seed 890 for 2,000 draws, and retaining the convention's single header per resampled collection. Its primary interval matches the author's implementation exactly. This resampling does not certify independence between utterances from the same speaker.

## Post-hoc paired sensitivity: the robust claim is the full-8 comparison

`PAIRED_SUPPLEMENT.json` adds matched utterance differences from already saved arrays. These are post-hoc diagnostics, not extra frozen criteria. Negative differences favour paq8px. The reference methods keep their originally evaluated representations and scoring conventions; FLAC retains its single-header convention.

| Reference | Reference ratio % | Full-file paq minus reference, percentage points | Paired 95% interval |
|---|---:|---:|---:|
| FLAC, retained one header | 30.606372 | -8.703638 | [-8.931429, -8.503039] |
| V_base, all 8 bits | 25.886580 | -3.983845 | [-4.207307, -3.772732] |
| Mistral, all 8 bits | 34.709900 | -12.807165 | [-13.363073, -12.256783] |
| Qwen, all 8 bits | 28.900412 | -6.997677 | [-7.366655, -6.646599] |
| Mistral, released 7-bit score | 22.076979 | -0.174245 | [-0.382324, +0.025630] |
| Qwen, released 7-bit score | 22.086678 | -0.183944 | [-0.392322, +0.016980] |

The last two rows compare different bit accounting and are not like-for-like lossless compression comparisons. Both full-file intervals cross zero. With the 13-byte adjustment they instead exclude zero: Mistral -0.808693 [-1.016759, -0.608811], Qwen -0.818392 [-1.026760, -0.617463]. Thus numerical superiority to the 7-bit scores is convention-sensitive; do not turn the adjusted 21.3-versus-22.1 comparison into a convention-robust superiority claim. Overlap of marginal intervals would not by itself answer this paired question.

The full-8 advantage remains large even with every paq file byte charged. Neither this result nor the B88 baseline comparison identifies the causal contribution of pretraining. The 20.9-versus-21.0 Chinchilla comparison is additionally unpaired and cannot establish equivalence.

## New figures and tables

`audit_v17.py` reconstructs the numerical inputs to the captured `make_fig_main.py` and compares them with the earlier independent B75/B83/B84/B87/B88 audit outputs. All 267 plotted numeric inputs match exactly.

- Figure 1 has exactly 26 benchmark plus 8 new-source rows. All 32 favourable paq intervals exclude zero. All values and interval endpoints fit the actual axis; no plotted numeric result is lost to the generator's clipping function.
- Figure 2 has the expected 15 chunk-length means with their intervals and six copy-state groups. Shares and both predictors' conditional differences match. All bars fit the chosen axis.
- Table 4's eight data rows and Table H4's 34 data rows are byte-identical to the previously verified v15 tables. The v18 change does not touch them.
- Figure C1's captured PNG is byte-identical to v16's Figure 1, consistent with moving that figure to the appendix.
- The old V_auto-to-Figure-1B reference was removed in v17. The two remaining references to missing Table 2 were corrected to Table F1 in v18. Current Figure 1/2/C1/H1/I1 references resolve; the semantic corrections below still matter.

The figure PNGs were inspected directly and the relevant PDF pages rendered with Poppler. Pixel-identical regeneration was not performed: matplotlib was unavailable in both inspected Python environments, and no dependency was installed. This does not affect the 267 numeric checks.

## Remaining changes requested in v18

1. **Abstract and Table 3: identify the adjusted speech ratio.** The abstract reports 21.3% as though it were an actual compressed-file ratio, and Table 3's compressed-size column omits the adjustment. Prefer the actual full-file 21.9% as the plain compression headline, or explicitly label 21.3% reference-adjusted and give 21.9% alongside it. Explain both paq and FLAC header conventions in the caption. Appendix I's correct explanation should not be required to interpret the headline. Do not alter frozen R1–R3.
2. **Preserve what changed in the speech comparison.** The new one-paragraph abstract says sensitivity to "bit accounting" only. The body correctly states that the manipulation combines the discarded bit, representation and tokenisation. Restore that joint scope in the abstract; this was not an isolated intervention on accounting.
3. **Narrow the transfer conclusion.** "Zero-shot bits per byte alone therefore do not establish transfer" conflates an absolute score, advantage over these baselines and the causal contribution of pretraining. Suggested replacement: "An absolute zero-shot score alone does not establish an advantage over online/compression baselines or isolate what pretraining contributed." Keep the acknowledged scaling evidence and complementarity result.
4. **Use "no offline fitting" consistently.** The new abstract and Figure 1 legend say "no fitting on these rows"; the compressor adapts internally. Older introduction/discussion/Figure C1 wording still says "no training on these data". The setup already supplies the correct operational definition; use it in these prominent locations.
5. **Fix comparator scope in Section 3.1.** "At the published sizes and rounds on 32 of 34 row sets" applies only to the 26 benchmark rows. The eight new sources use E24 at the fixed final round. Suggested wording: "lower on 32/34 row sets, against the evaluated published-size/round configurations on the 26 benchmark labels and E24 on the eight new sources."
6. **Identify exact versus substitute comparators in Figure 1.** Its caption says "marked substitutes", but the new graphic uses the same filled black circle for every V_base point and no status marking on the labels. Restore the comparator-status encoding or explicitly direct the reader to Figure C1B/Table C and remove "marked". The 7 exact / 19 substitute distinction should be visible beside the central result.
7. **Remove equivalence language.** Replace "level with Chinchilla 70B's 21.0%" with "numerically close to the reported point value under different bit conventions and on different chunks; no equivalence is established." The complete-file value on all 20,000 chunks is 21.5%, not 20.9%.
8. **Retain selection and chronology in compact claims.** The context/reset result is for three selected text/code labels, not text/code generally. The blind-test description applies to the predictors frozen before those sources; paq was selected later, as Table 4 correctly says.
9. **Avoid an impossibility claim for the particular pseudo-random stream.** Replace "which no method can compress" / "where nothing can be compressed" with the measured claim about these evaluated methods or note the uniform 8-bit reference. The results do not prove incompressibility of this finite generated sequence.

## Layout/export observations

Reviewed v16 PDF pages 1,5,6,12,36; v17 pages 6,7,10,18; v18 pages 1,5,6,11. All inspected charts/table values are readable and unclipped. The new v18 first page no longer leaves the Introduction heading stranded. Figure 1 still occupies page 5 while its caption is on page 6; keep the caption with the figure if possible. This is a scoped page review, not certification of every page.

The captured standalone `figs/fig1.pdf` is still byte-identical to v16's old two-panel figure, while `fig1.png` is the new 34-row figure. `make_fig_main.py` only saves PNGs, and there is no corresponding new `fig2.pdf`. The manuscript itself embeds the correct PNG. Regenerate/rename the stale standalone PDF before distributing figure files so an old figure is not mistaken for the current one.

The TMLR main/camera-ready source and PDF snapshots were captured and text extracted from main.pdf, but no complete TMLR layout, Markdown-to-LaTeX text-parity, zerofit package, or 49-test claim is certified in this bounded audit.

## Provenance limits and files

The remote B78 raw chunk array consumed by B89 is not present locally and B89 records do not attest its input hash. Existing B78/B79 metadata hashes match, but that does not prove the actual remote bytes consumed by each worker. No compressor binary hash or decompression round-trip record was supplied. All saved sizes and their aggregation are verified conditional on that provenance boundary.

The captured score log ends in SCORE DONE / App completed. It contains three identical preemption notices without event identifiers; it does not independently establish exactly one unique preemption. Retries did not create any duplicate or missing final saved row.

Evidence: `SHA256.json`, `V17_SHA256.json`, `V18_SHA256.json`, `V17_DEPENDENCIES_SHA256.json`, `RESULTS.json`, `RECOMPUTED.json`, `PAIRED_SUPPLEMENT.json`, `V17_FIGURE_TABLE_CHECKS.json`, `V17_V18.diff`, and captured sources. Scripts: `audit_saved.py`, `audit_v17.py`.
