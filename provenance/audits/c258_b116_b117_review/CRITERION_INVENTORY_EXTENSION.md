# Verified addition to Appendix F.1: Batteries 113–117

This extends, without rewriting, the B88–B112 inventory in
`audits/codex_initial_20260928/c226_appendix_review/CRITERION_INVENTORY.md`.
Numerical predicate outcomes and admission gates remain separate. B116 is exploratory development, not a
prespecified prediction family. Reused development sources are not newly held-out data.

## Battery 113: five numerical families, two met and three failed

Population: 2,042 retained windows across eight T labels; byte-class Q4 excludes ranked DCLM and uses seven labels.
Gain is relative to lpaq1 with the two-expert mixture at share 0.001. The paired comparator is paq8px's per-byte
code-length advantage over lpaq1, not a second gain measure.

**Q1 PASS:** first 512 positions carry at least 25% of total learner gain beyond lpaq1 on 8/8 labels; need at least
6/8. Observed shares 54.612–88.5661%.

**Q2 FAIL:** first 512 positions carry at least 25% of paq8px's total code-length advantage over lpaq1 on 4/8 labels;
need at least 6/8. Observed shares 19.2179–27.5882%.

**Q3 FAIL:** mean per-byte learner gain at repeat-hit bytes is below its overall mean on 0/8 labels; need at least
6/8. Repeat-hit/overall mean ratios are 1.5701–13.1914.

**Q4 FAIL:** word-start bytes have more than their byte-share of total learner gain on 0/7 labels; need at least 5/7.

**Q5 PASS:** Spearman correlation between per-byte learner gain beyond lpaq1 and paq8px's advantage over lpaq1 is
positive on 8/8 labels; need at least 7/8. Correlations 0.248515–0.355143. The two quantities share the lpaq1 loss
term; this numerical success is not independent evidence of mechanism. Repeat-hit strata also use the observed
next byte; their result is not a causal copy-circuit identification.

Evidence: `c250_protocol_review/REVIEW.md`, B113 recomputation and post-hoc files in that audit directory.

## Battery 114: three numerical families, one met and two failed; one separate gate

Population: 2,042 windows across eight T labels, 29 variants, 928 saved parts. All variants retain the full same
population, so the amended common-row and original pairwise-row computations coincide here.

**S0 gate PASS, not a criterion-family count:** V0 exactly equals B98 in saved per-byte losses and aligned sets on
all eight labels; archive sizes also equal. Standard/forced code-length identity is a diagnostic, not a trace of
which internal route ran.

**S1 PASS:** 14/14 single-group direct-route drops give G <= 0.002 on all 8/8 labels. Requirement: at least 12/14
drops satisfy the threshold on at least 6/8 labels.

**S2 FAIL:** K2 gives G > 0.002 on 0/8 labels; need at least 6/8. Observed K2 G range -0.0009571103 to -0.0008214250.

**S3 FAIL:** the largest mean G reduction from adding one group to K2 is record, approximately 2.4317594e-5;
predicted winner was text, whose reduction is approximately -4.1757032e-6. Eleven additions, each averaged over
the same eight labels.

Admission/interpretation: preserve the pre-outcome amendment and subsequent saved-file checks. Shared Text/Word/
Match state is still computed and reaches SSE; a muted group retains indirect effects, and constant-selected
mixer weight sets remain adaptive. K2 is not a clean lpaq-like core, and no bias direction is established.

Evidence: `c254_b114_results/REVIEW.md`, `RECOMPUTED.json`, `CHECKS.json`.

## Battery 115: five numerical families, one met and four failed; one separate gate

Population: eight primary T labels, 2,042 windows; four previously evaluated B106 secondary corpora, 1,024 windows;
12 variants. The earlier three-window smoke exposed own code length before freezing the G predictions.

**G0 gate PASS, not a criterion-family count:** U0 exactly equals B104 L5 on every primary row, all eight labels.

**P1 PASS:** UA G is below U0 G on 8/8 primary labels; require all eight.

**P2 FAIL:** UA G <= 0.002 on 5/8 primary labels; need at least 6/8.

**P3 FAIL:** the first-512-position contribution to the U0-to-UA gain reduction is at least 70% of its full-window
reduction on 5/8 primary labels; need at least 6/8. Fractions range 0.4445419–0.8796869.

**P4 FAIL:** largest mean primary G reduction among the five single upgrades is U1, 0.0216973 bits/byte;
predicted winner was U2, whose reduction is 0.00155340. The other reductions are U5 0.0124737, U3 0.0119656,
U4 0.00148372. Interactions preclude treating this ordering as universal additive importance.

**P5 FAIL:** UA G <= 0.002 on 1/4 secondary corpora; need at least 3/4. Rust's 0.0020193854 is strictly above the
threshold; do not round it into a pass. These four sources were previously evaluated, not newly unseen corpora.

Corrections separately recorded after results: U3 has ten active contexts, not eight; lpaq1 has an ASCII word
heuristic; this constructive compressor comparison is not an attribution of the original paq/lpaq gap.

Evidence: `c256_b115_results/REVIEW.md`, `RECOMPUTED.json`, `CHECKS.json`.

## Battery 116: exploratory development, no numerical prediction families

Eighteen recorded completed configurations on the same 12 development row sets; no prespecified success count.
UP126975 is the only recorded variant with G <= 0.002 on all 12. The ledger does not timestamp or hash each
attempt/source revision and does not record failed attempts before successful scoring. Do not count 18 development
variants as 18 confirmations. The selected configuration enables 16 switches, including explicit text/structure
heuristics. It was frozen for B117.

Evidence: `DEVELOPMENT_CHECKS.json`, `DEVELOPMENT_SELECTION.json` in this directory.

## Battery 117: four numerical families met, with a material C3 population qualification

Six sources fixed in the posted protocol: four have 256 windows, Flask RST has 129 and Linguist YAML has 35,
for 1,188 windows. F and R0 retain every window. Eight E24 seed/checkpoint identities and corpus hashes checked.
F is the frozen selected B116 compressor; R0 is original lpaq1. All gains use fixed share 0.001.

**C1 PASS:** G beyond F <= 0.002 on 5/6 sources; need n-1 = 5. The C++ JSON source fails individually:
G = 0.0034421853, pointwise window-bootstrap 95% CI [0.0025625262, 0.0045183625]. Keep this exception.

**C2 PASS:** F mean own code length is below the evaluated learner ensemble on all 6/6 full sources; require six.

**C3 numerical predicate PASS on retained subsets only:** G beyond standard-mode paq8px <= 0.002 on all 6/6
reference-specific subsets; require six. Those subsets contain 256 C++ windows, **1/256 books**, **255/256 Haskell**,
256 Java, 129 RST, and 35 YAML. This is uninformative for the books source and is not full-source or matched-
population confirmation against F/R0. The point interval for books is a one-observation bootstrap artifact.

**C4 PASS:** G beyond R0 > 0.002 on all 6/6 full sources; need ceil(2n/3) = 4.

Admission: all 122 reported numeric fields reproduce independently. The production scorer's missing guards were
supplied in post-completion artifact checks. The archive filename lists promised by the protocol are absent from
the original provenance, which records download hashes/counts and selected indices. Any later reconstruction must
be labelled as such. No reference-mode replacement was made for excluded windows.

Evidence: `CONFIRMATION_CHECKS.json`, `CONFIRMATION_DETAILS.json`, `CONFIRMATION_RECOMPUTED.json` in this directory.

## Count reconciliation for F.0

B113–B117 add **17 numerical criterion families: 8 met and 9 failed**, with B116 exploratory and S0/G0 counted
separately as gates. Added to the existing B88–B112 84 = 52 met + 25 failed + 7 amended/descriptive, the extended
inventory is **101 = 60 met + 34 failed + 7 amended/descriptive**. These are neither independent confirmations nor
60 unqualified protocol-compliant passes. In particular, preserve B117 C3's subset qualification and all earlier
admission/amendment qualifications. If the old count is retained, explicitly label its scope B88–B112 rather than
silently describing it as the complete B88–B117 inventory.
