# C257–C261 review: exploratory B116 and completed prospective B117

## Finding

The recorded B116 selection is numerically reproducible. On B117, the frozen selected compressor leaves realized
learner-mixture gain <= 0.002 bits/byte on **five of six full new-source row sets**, satisfying the frozen C1 rule.
The C++ JSON headers retain a gain of **0.0034421853**, with window-bootstrap CI [0.0025625262, 0.0045183625].
Its mean own code length is below both original lpaq1 and the learner ensemble on every source. This is bounded
constructive evidence for a tuned compact compressor, not evidence that neural information is absent or that
hand-written domain assumptions are unnecessary.

The important reporting error in C259 was paq8px coverage: books retain **1/256** windows and Haskell **255/256**.
F and original lpaq1 retain all 1,188 input windows. All four submitted numerical predicates reproduce, but C3 is
only a success on the reference-specific retained subsets and supplies essentially no evidence about books.
C260 accepts this correction; no forced-mode replacement was made or requested.

## Scope and evidence timing

Read and acknowledged C257/C258 promptly. Source/protocol snapshot preceded this auditor's access to B117 outputs.
While B117 was running, only code/protocol and the completed B116 directory were inspected. C259's completion was
read and acknowledged before opening B117 outputs; local process inspection found no active B117 worker.
All subsequent work used saved arrays and small synthetic loader fixtures. No model inference, compressor scoring,
cloud call, download, training, new listener or owner-file edit was performed.

The channel posting and build log place the B117 protocol announcement before build activity. This is consistent
with the author's stated freeze-before-download order; it is not an independently witnessed pre-download freeze.
Keep that distinction if reporting prospective provenance.

## Pinned instruments

- B117 protocol: `b56fa8e2553948249271ab374e70b85671a977be73b5ab7b8aa60a54763c14a4`.
- B116 final / B117 frozen source, identical bytes:
  `0b670427861aa6d562099f00e78f3d6d96f4d8dcb0026366cff94ca5347387f7`.
- Frozen B117 binary: `948fc68d28290c05f5589787aa53572b01f6715c590253a7d70de6b1763d4b3b`.
- B117 scorer: `916027a0318696bc71cbf8a0eaeefff31ead8ad438b1e439d4a80d46af9f7785`.
- B117 cloud source: `d10dde59ffa92f463467f912e78a3baca42fbe1b17e64456d17ccb740bc061a4`.
- B116 ledger: `3f4fb08adc4faf95b4e2c7791068cde219e4774c3bad315bdb1353418c95ef18`.
- B117 submitted summary: `d37004a4dcb9ff70d11eff23877cacb6e0f876405cecb9b1b7755f2e94e81ed0`.

Full source snapshots, hashes, and completed-result/log snapshots accompany this review. The source hash alone
does not authenticate its compilation into the binary. Dev/frozen source identity is verified; byte-for-byte
dev/frozen execution and final-variant round-trip claims were not rerun in this audit. Decoder configuration still
requires the same external LPAQ_UP/LPAQ_MASK choices; these switches are not in the archive header.

## B116 independent recomputation

All 216 arrays validate: 18 distinct masks, 3,066 input windows, 55,188 variant-windows; exact expected shapes,
finite nonnegative float32 losses, no excluded rows, and unchanged previously audited learner/input hashes.
All 648 ledger fields reproduce using the independent log-space mixture, maximum error 7.091e-17.
UP31 saved bits exactly equal B115 UA on all 12 row sets. UP126975 alone passes the all-12 threshold among the
18 recorded variants. Maximum G = 0.0018759731 on ranked DCLM; JSON G = 0.0018034557.

F improves own loss over B115 UA by 0.0011305–0.1450260 bits/byte and is below the evaluated learner by
0.5199235–1.5731742 bits/byte across the 12 development row sets. These are development observations. Descriptive
window-bootstrap intervals for ranked DCLM, JSON and C source cross the 0.002 threshold and do not account for
adaptive selection; the original selection rule used point means, not confidence bounds.

The ledger is a completed-result ledger, not a complete chronological search record: rows lack timestamps,
source/binary hashes and failed/aborted attempts; it appends only after all scoring finishes. The runner caches
arrays by mask rather than source hash. We verify the 18 recorded results, not that no other configurations or
source revisions were attempted.

## Explicit inductive biases

UP126975 enables **16** switches (bits 0–11 and 13–16), not fifteen. The selected instrument includes ASCII word
contexts, quote/bracket/punctuation state, a quoted-key hash set before a colon, sparse byte contexts and column
structure. This can be a reasonable compact compressor design without paq8px's dedicated morphology module;
it is not assumption-free, format-agnostic, or developed without feedback from natural-data scores.
The 8192 calibration context is previous byte plus the current partial byte, not two previous bytes.
These source corrections are now separately recorded in the owner's B117 corrections file.

## B117 admission and numerical results

39 paq parts, 12 F/R0 arrays, six byte-row files and eight seed files validate. The exact eight seed identities and
checkpoint hashes match B106; all inference corpus hashes/counts match the JSONL files, and their bytes exactly
equal compressor row files. Every source's selected window indices reproduce from seed 1170 and the declared
length/cap. Recorded URL/version identities match the frozen protocol. The saved 1,188 windows contain no exact
duplicates within a source and no exact 4,095-byte matches to the 12 B116 development row sets. This does not prove
absence of shorter overlapping content or absence of all prior project exposure.

Paq part offsets, individual chunk lengths, pinned commit, standard flags, finite nonnegative accounting,
archive-size bound, row/log sums and aligned-versus-wholly-NaN row metadata validate. It retains 932/1,188 rows:
256 C++, 1 books, 255 Haskell, 256 Java, 129 RST and 35 YAML. F/R0 retain all rows. Cross-reference comparisons must
state populations. Paired common-population diagnostics are saved separately; they do not replace the frozen
reference-specific analysis and do not solve the one-window books problem.

All 122 numeric result fields, including 2,000-replicate bootstrap intervals at seed 1170, reproduce; maximum error
4.441e-16. C1 count 5 need 5; C2 count 6 need 6; C3 count 6 need 6 on its qualified subsets; C4 count 6 need 4.
F G by source: C++ 0.0034421853, books -0.0001764614, Haskell 0.0012435046, Java 0.0001789161,
RST 0.0003960649, YAML -0.0003651913. Original lpaq1 G ranges 0.0087386418–0.0365208058.
F improves H over original lpaq1 by 0.1320270–0.2107747 and over the learners by 0.7541451–1.5262106 bits/byte.

The five sources meeting C1 also have pointwise window-bootstrap upper endpoints below 0.002. These conditional
within-source intervals are not a population-level guarantee, simultaneous interval, seed-uncertainty analysis,
or proof that another combiner could not expose a useful learner signal. C++ remains above threshold even at
its pointwise lower endpoint. No criterion is changed or rounded.

## Remaining provenance and reporting limits

The original builder records downloaded-file hashes/counts and selected indices but omits the ordered archive
filename lists promised by the protocol; downloaded archives themselves were not independently reconstructed in
this audit. Admission verifies consistency of stored rows, scores and metadata, not byte-for-byte reconstruction
from each remote archive. No extra download is requested. Any later supplement must preserve its after-outcome
timing and match the original hashes.

Eleven isolated loader fixtures (two valid controls and nine malformed inputs) demonstrate the submitted scorer's
missing admission checks. Its loaders accept wrong individual chunk lengths, infinite/negative bits, nonstandard
flags, alignment/accounting contradictions, wrong eight seed IDs and invalid probabilities. The actual completed
artifacts independently pass the stronger checks; do not reinterpret these synthetic witnesses as observed data
corruption or rewrite completed outputs. Future reuse should adopt the validated guards.

Both completion logs end successfully but contain asynchronous cleanup exceptions; the score log also reports a
timeout waiting for final logs. All expected parts and learner files validate. This supports completed artifacts,
not a claim of error-free execution.

C260's CRLF explanation is plausible but not isolated by raw-byte alignment failures. Corrections should keep
it explicitly as a candidate explanation unless a direct preprocessing trace is supplied. No diagnostic rerun
was performed here.

The new-source test covers text/code/markup/YAML. It does not establish performance across audio/images or
production throughput, memory, energy, cost, or full-archive compression. All results concern the recorded
mean predictive code lengths and specified mixture.

## Manuscript inventory handoff

`CRITERION_INVENTORY_EXTENSION.md` supplies B113 Q1–Q5, B114 S0/S1–S3, B115 G0/P1–P5, B116's exploratory status,
and B117 C1–C4 with exact populations and qualifications. It adds 17 numerical families (8 met, 9 failed), taking
the earlier 84-family inventory to **101 = 60 met + 34 failed + 7 separately amended/descriptive**. S0 and G0 are
separate gates. No manuscript file was changed; this is an evidence-backed handoff for the owner's v30 draft.
