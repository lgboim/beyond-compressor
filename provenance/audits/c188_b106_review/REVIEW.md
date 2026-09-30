# B106 completed-artifact audit and C189 gate regression

2026-09-29. Reply to C188/C189; ownership announced in C1187.

**Verdict:** The saved numerical results reproduce and all five frozen criteria
pass on their stated retained populations. The seven C1186 admission counterexamples
are now blocked before criterion output. The strengthened admission check was added
after results were read; it is post-outcome validation, not a pre-outcome gate.
The frozen protocol and C186 input hashes remain unchanged.

The strongest additional observation is exact equality of standard/forced retained
per-byte code lengths for all eight old text/code/formal labels and all six new
sources on common rows. This is a check of all recorded byte positions, not merely
similar mean gains. Thus switching to this forced mode does not alter the low
learner gain on the eight tested old labels. It does not establish information
absence, a universal claim about compressors, or an isolated look-ahead effect.

## Numerical and artifact verification

- 111 numeric fields reproduce, maximum absolute difference
  `2.6645352591003757e-15`; no mismatches in the full result, including diagnostics.
- 72 independent positive-share recurrence checks against the retained source
  function, maximum per-window loss difference `2.1760371282653068e-14`.
- 361 B106 paq part files and 361 corresponding completion-log records; exactly
  the expected offsets, row lengths, commit and flags. 11,494 windows across
  new-source modes and the old forced arm, with 11,240 aligned; the only exclusions
  are 254 standard-mode Gutenberg windows.
- All aligned retained matrix sums equal the logged main-bit totals exactly in
  float64. All accounting values are finite/nonnegative and fit within archive
  bits. Aligned flags agree with finite versus all-NaN matrix rows.
- 118 probability arrays checked for shape/range/finiteness: 54 new-source arrays
  and 64 old learner arrays needed for the eight-label criterion. All eight new
  worker-reported learner checkpoint hashes match historical audited identities.
- All six row files and the original provenance manifest match the hashes received
  in C186 before this auditor read outcomes. JSONL equals raw rows; all 48 learner
  corpus hashes/counts match; sampled indices independently reproduce from seed1060.
- Post-build download metadata matches the original manifest; all six reported
  rebuild hashes match saved row bytes. Member counts are 98 Rust, 54 JavaScript,
  and 3000 WAV files. Audio metadata is exclusively 16-bit mono 8kHz; image metadata
  is `arr_0`, `[60000,28,28]`, uint8. This auditor checked the retained records and
  hashes, without independently downloading/rebuilding the original streams.
- Frozen B88 inventory, row hashes, B98 standard-code arrays, and old learner
  probability hashes checked against earlier audit records. Ranked DCLM has 250
  input rows, all aligned; this is not a six-row alignment loss.

## Results with denominators

G is the realized average log-loss reduction from the specified fixed-share
mixture, in bits/byte. Negative G means this mixture incurs a small loss versus
the comparator; it does not prove the learner contains no additional information.

| New source | Standard n | Forced n | Learner standard G | Learner forced G | bGPT forced G |
|---|---:|---:|---:|---:|---:|
| Gutenberg | 2 | 256 | -0.000963012 | -0.000963105 | 1.293814248 |
| ripgrep Rust | 256 | 256 | -0.000739654 | -0.000739654 | 0.330068804 |
| lodash JavaScript | 256 | 256 | -0.000959008 | -0.000959008 | 0.197678435 |
| countries JSON | 256 | 256 | -0.000940510 | -0.000940510 | 0.083706101 |
| KMNIST pixels | 256 | 256 | 0.008531903 | 0.008531903 | -0.000845862 |
| FSDD audio | 256 | 256 | 0.001887240 | 0.001887240 | 0.431968559 |

N1 PASS and N3 PASS use only the **2/256 retained Gutenberg standard rows**.
They are mechanical passes of the frozen criteria on those rows, not persuasive
full-source evidence. Do not silently replace them with forced-mode statistics.
N2 PASS covers all 256 windows in each of the four text-like sources. N4 PASS is
carried by KMNIST; FSDD is positive but below the frozen 0.002 threshold.
S1 PASS 8/8: seven unranked labels have G between -0.000961672 and -0.000885948;
ranked DCLM is +0.000094109. Seven have n=256 and ranked DCLM n=250.

bGPT standard Gutenberg G is 1.302404169 on the two rows. Forced-mode bGPT G on
those **same** two rows is also 1.302404169; the all-256 forced value is 1.293814248.
That difference is a population difference, not a demonstrated mode effect.

`MODE_COMPARISONS.json` verifies exact common-row bit equality for all six new
sources and all eight T labels (2,042 old T windows). Across all 34 old row sets,
26 have exact common-row equality and eight differ; the result is not universal.
The differing sets are protein, two CIFAR layouts, two ESC50 rates, two Speech
Commands rates, and ELF. ELF's standard/forced populations are 170/256.

`GUTENBERG_ALIGNMENT.json` preserves retained row indices 4 and 34, corresponding
to original stream windows 21 and 101. CRLF presence alone does not distinguish
retained from excluded rows; attributing each exclusion to a particular transform
would require the unretained raw logs or another explicitly authorized investigation.

## C189 gate regression

Reviewed runner SHA-256:
`6b75dd0d2399e40a78785bde3e1a09fdbedb90f7b2aa86d2c711562533c6c0bf`.
`check_gate_regressions.py` reuses the seven isolated C1186 witnesses with updated
expected outcomes against this source snapshot. `GATE_REGRESSIONS.json` records:

- Valid control accepted; wrong-commit control rejected with no criteria.
- Zero aligned population is rejected by the post-computation check; no hypothesis
  outcome is emitted, rather than an erroneous scientific FAIL.
- Finite row marked unaligned, incorrect per-part lengths, nonfinite accounting,
  matrix/log sum disagreement, dropped old row-set inventory, and seven-seed
  listing/artifacts all rejected by the initial gate.

These specific defects can close. They are not an exhaustive guarantee for future
runs. The current gate still derives seed names from a live listing, does not pin
the old input hashes, accepts a much looser matrix/log-sum tolerance than needed
for these saved values, and relies on the post-build rebuild boolean without
rechecking its row hash. This audit independently checks those identities/hashes
and exact sums for the completed run. Missing bGPT checkpoint hashes, unexpected-key
diagnostics and worker runtime records remain provenance limitations.

## Scope and reproducibility

The numeric audit uses saved arrays only, with an independent scalar mixture-weight
recurrence and a cross-check against the retained implementation. It starts no
models, compressors, experiments, network jobs or listeners. Output sources and
metadata are snapshotted; larger dependencies are hash-pinned and checked again
after reading. Raw compression archives/logs were not retained, so byte-alignment
claims remain worker assertions corroborated by saved matrix consistency.

```sh
.venv/bin/python audits/codex_initial_20260928/c188_b106_review/audit_saved.py
.venv/bin/python audits/codex_initial_20260928/c188_b106_review/check_gate_regressions.py
```

Evidence: `RECOMPUTED.json`, `CHECKS.json`, `MODE_COMPARISONS.json`,
`PROVENANCE_CHECKS.json`, `ALIGNMENT.json`, `ACCOUNTING.json`, `ROW_RESULTS.json`,
`ARRAYS.json`, `GATE_REGRESSIONS.json`, and input/dependency/output SHA-256 manifests.
No owner source, runs, references, frozen thresholds or previously published audit
artifacts were modified.
