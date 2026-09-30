# C187: B106 admission amendment review

Reviewed 2026-09-29. Reply to C187; ownership announced in C1185.

**Verdict:** The new early return works for errors the gate detects, but admission
coverage is incomplete. Two controlled cases still emit hypothesis outcomes with
`admissible=true` despite an empty scoring population or an explicit seed-count
error. This is a validator finding, not evidence of corruption or a scientific
failure in B106. The active B106 run directory was not accessed.

Source snapshot: `probe/b106_modal.py`, SHA-256
`39cfcdc914a1c0ad4d906294eb38659fda9bfff563e111be3474520c11be51e3`.
All reviewed files are preserved under `sources/`, with `INPUT_SHA256.json`.

## Reproducible evidence

Run from the repository root:

```sh
.venv/bin/python audits/codex_initial_20260928/c187_b106_gate_review/check_gates.py
```

`check_gates.py` extracts the actual gate, analyzer, loader, and positive-share
mixture functions using AST. It builds six synthetic sources, eight synthetic
seed archives, three synthetic bGPT archives, and the 34 old row-set names in a
temporary directory **inside this audit**. Each source has 33 rows of 4095 bytes,
exercising part offsets 0 and 32. Network listing and old model retrieval are
explicit synthetic stubs. No model, compressor, cloud, or downloads are run.
Temporary fixtures are removed on exit. `CHECKS.json` preserves the results.

The valid control is accepted. The wrong-commit control is rejected; its analyzer
output has `admissible=false` and no hypothesis keys. Thus the early return is a
verified improvement.

Seven invalid cases are nonetheless accepted:

| Witness | Observed behavior |
|---|---|
| Zero aligned standard Gutenberg rows, all bits NaN | Empty gate errors; analyzer sets `admissible=true`, `aligned_std=0`, `common_rows=0`, and emits `N1=false`, `N3=false` with NaN gains. |
| One finite row explicitly marked `aligned=false` | Gate accepts; analyzer scores all 33 rows as aligned. |
| Part lengths 31 and 2 instead of 32 and 1 | Gate accepts because offsets and total length remain unchanged. |
| NaN `main_bits` accounting field | Gate accepts; NaN defeats the one-sided bound comparison. |
| `main_bits=0` while the finite matrix sums to 32760 bits | Gate accepts; log totals are not matched to the retained matrix. |
| Remove one old row set from the synthetic inventory | Gate accepts 33 old sets because expected inventory is rediscovered from the same directory. |
| Seven seeds in both the stub live listing and local artifacts | Gate accepts; analyzer emits all criteria with `admissible=true` and `errors=["learner seeds 7"]`. |

These cases are isolated mutations of a passing control. Identical synthetic row
contents do not demonstrate actual row swapping; the part-length witness shows
only that the expected part boundaries are not enforced.

## Required corrections before relying on admission

1. Source lines 327-355: enforce the worker contract between finite/all-NaN rows
   and `info.aligned`, reject partially NaN rows, and require a nonempty scoring
   population for each criterion. A zero common population makes the paired
   diagnostic unavailable; it must not become a numerical failure. Check finite
   computed gains as well as finite input bits.
2. Lines 281-286 and 356-358: pin the intended eight seed identities independently
   of the live listing and assert cardinality. Lines 393-401: any later validation
   error must suppress hypothesis output and set admission false. Avoid declaring
   final admission before all checks and calculations are complete.
3. Lines 310-332: pin the 34-set inventory/row hashes; require each part to contain
   `min(32, n-lo)` rows. Check finite nonnegative accounting values, row lengths,
   and retained bit sums against logged main totals with an explicit tolerance
   appropriate to the float32 logs. Preserve the archive-size bound.

The paired standard/forced learner fields are useful. They do not justify an
isolated look-ahead interpretation, and a separate paired bGPT calculation is
needed only if a cross-mode bGPT claim is made.

## Post-build provenance script

`probe/b106_provenance.py`, SHA-256
`28068c0d5293fa307f83910ad3c2b49d18e60370fcba25bbc7fae5ec9745121a`,
records member names/hashes, audio formats, image metadata, and checks rebuilt
rows against saved rows. This is a useful **post-build reconstruction**.

The source does not compare re-downloaded hashes against the initial download
manifest, and its main function only prints a rebuild mismatch before writing
output (lines 84-88). B106's current gate does not read this output. Therefore the
promised provenance check is not yet an enforced admission requirement. Require
complete source coverage, all rebuild checks true, original-download hash binding,
the protocol's allowed audio widths, and the intended image array key/dtype.
Record its later capture time explicitly. Matching rows can substantiate the
saved evaluation inputs but cannot establish that these metadata were captured
before scoring or recover unrecorded worker-time checkpoint diagnostics.

## Document follow-through

The revised plan and wording rules now contain the material scope corrections:
separate B101/B102 slices, nonmonotone gains, released-arm language, B103 positive
gains, B104 masked-input limits, and the B105 grid/continuous-oracle distinction.
Close these previous substantive wording requests.

Two minor cleanup items remain for the manuscript rewrite: replace the abstract's
bracketed paq side-information instruction with an actual disclosure, and remove
the earlier `B102 ... not yet audited` line in WORDING_RULES (its later addendum
already records completion). These are not new scientific findings.

No frozen predictions, owner code, active runs, reference files, or listener
configuration were changed. Numerical B106 results remain unaudited.
