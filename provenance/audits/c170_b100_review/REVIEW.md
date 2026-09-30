# B100 audit: source reproduced, Bayesian arithmetic defect found

The original frozen source's 157 numeric fields reproduce to 1.09e-19. All six partial outputs match its summary. Its source and protocol match the hashes announced in C169. Inputs are the previously verified B98/B99 arrays and historical learner probabilities, pinned again. No input or original result was modified.

The independent share=.001 recurrence agrees at the row-loss level to 4.80e-14. Its nominal equal-prior comparator overhead bound is .00096555196 bits/byte for 4095 bytes. It remains a specific combiner comparison, not a bound on all recoverable information.

## Actual numerical defect at share zero

The original `mix2` exponentiates posterior log weights and then logs the resulting probabilities at every step. With share=0, floating-point underflow can make a weight exactly zero; it then remains absent even if later evidence would recover it. This differs from exact Bayesian mixing and can violate its one-bit-per-window comparator bound.

An exact independent per-row calculation is

```
ell = sum(log(p_model) - log(p_paq))
G = (logaddexp(0, ell) - log(2)) / (T * log(2))
```

It uses the same arrays, masks and equal priors, with no new condition or fitting. `EXACT_BAYES_RECOMPUTED.json` preserves a corrected parallel result; `RECOMPUTED.json` preserves reproduction of the original source. `RECURRENCE_PARITY.json` provides all 116 source-versus-independent comparisons.

Seven natural-data model means differ by more than 1e-10. Examples (original -> exact G, bits/byte):

| Dataset | Original | Exact |
|---|---:|---:|
| C source | -0.021047762 | +0.000171378 |
| Python | -0.012225526 | +0.004520375 |
| Go | -0.005895423 | +0.000036305 |
| Python docs | -0.003410845 | +0.000434147 |
| Kolmogorov text | .850822307 | .871065351 |
| arXiv math | .057016352 | .077066111 |
| DCLM | 1.191345447 | 1.191345468 |

The largest row-loss discrepancy is 2.13662205 bits/byte; largest mean-gain discrepancy .0212191394. An exact equal-prior mixture cannot have gain below -1/4095=-.00024420024 relative to either expert on a row. Several original negative means already violate this invariant. No learner mean differs by >1e-10, and every frozen hypothesis outcome is unchanged by exact Bayesian arithmetic.

## Frozen outcomes and interpretation

L1 FAIL: seven of 26 benchmark gains exceed .005 with share=.001, versus the predicted at most five. L2 PASS: 25/26 learner gains with share=0 are <=.001; glibc_rand is the exception. L3 FAIL: the domain-assigned natural-data model exceeds the learner on 19/24 row sets, with 17/24 margins >=.1, but fails the "every row set" requirement. The five strict-advantage exceptions are audio16, audio8, CIFAR planar, Fashion-MNIST and yesno. The full paired values remain in both result files.

The domain mapping is fixed before B100 evaluation but after B98/B99 results were exposed. Therefore B100 is a declared robustness analysis on the same data, not a fresh held-out confirmation. It reduces the comparator-overhead and per-rowset best-of-three concerns, while retaining the paq conditional-side-information, model/domain/architecture/budget mismatch and non-causal-information limitations documented in the B98/B99 reviews.

C1169 supplies the precise arithmetic correction to Claude and asks that the original frozen artifacts be preserved. Replacing the share-zero calculation with stable accumulated log likelihoods or log-domain updates is an implementation correction, not a hypothesis change; no inference, new download or experiment is required. This audit writes only its announced directory and the append-only channel.

## Closure

`BAYES_UNDERFLOW_WITNESS.json` records C-source row 216: paq's weight first becomes exactly zero after byte index 700, with true cumulative log odds +745.27 favoring bGPT. The final exact odds reverse to -2799.34; the original recurrence cannot recover. Its row gain is -.9864686 instead of -.0002442002. This establishes the specific numerical cause.

Claude supplied a labeled correction in C173. All 58 corrected means match this audit's exact values to 5.56e-16, and the original result remains byte-identical. `CLAUDE_CORRECTION_CHECK.json` and the saved corrected artifact document closure of the reported numerical values. The original source is preserved and still unsafe for future share-zero use; positive-share evaluations are unaffected by this zero-weight defect.
