# Protocol B114: which parts of paq8px make the learners' realized gain vanish

Frozen before any B114 number is computed. Inference only (no training); Modal CPU containers.

## Instrument

paq8px commit c84f576 with the Battery 98 logging-only `Encoder.cpp` and the B114 ablation patch
(`probe/b114_paq/`): `Mixer.cpp` gains a neutral mode in which mixer inputs are 0 (in the input and promoted layers)
and weight-set selections are 0; `ContextModelText.cpp` and `ContextModelGeneric.cpp` wrap each model group's mixing
call so that the group runs in neutral mode when dropped (environment `PAQ_DROP=a,b` drops the listed groups;
`PAQ_KEEP=a,b` drops every group not listed). Groups on the text path: normal (order-n contexts, including its
post-mixer contexts), match, sparsematch, sparsebit, sparse, xml, nest, chart, record, chargroup, text, word,
indirect, dmc; the generic path also has linear, similarity and exe (and lstm, off at these settings). A dropped
group still updates its own state, and components that read shared state (the final SSE stage and RecordModel read
the match state) still see it, so a drop removes only the group's direct contribution to the mixer; this biases the
test toward understating a group's importance. Standard mode, level 8 (`-8`), as Battery 98; one process per window.

## Variants

V0 full (no group dropped); D_g, each of the 14 text-path groups dropped alone; K0 keep normal; K1 keep normal and
match; K2 keep normal, match and word (the lpaq1-like core); K2+g for each of the other 11 text-path groups.

## Rows and measures

All Battery 88 rows of the eight labels T (metamath, aitdcc_b_c_source, llm_compression_python,
llm_compression_arxiv_math, dclm, llm_compression_cc, kolmogorov_text, dclm_ranked). For each variant v and label:
rows aligned (logged main-coder bytes equal the raw window) in both V0 and v; H_v = mean per-byte code length; G_v =
the learners' realized gain beyond v (evaluated ensemble, Battery 98 configuration; two-expert fixed share 0.001,
the paper's scorer); pointwise window-bootstrap intervals.

## Gate

S0: on every row aligned in both, V0's per-byte code lengths equal Battery 98's exactly (maximum absolute difference
0), and the aligned row sets are equal. If S0 fails, B114 is inadmissible.

## Predictions

- S1: for at least 12 of the 14 single-group drops D_g, G <= 0.002 on at least 6 of 8 labels.
- S2: K2 gives G > 0.002 on at least 6 of 8 labels.
- S3: among the 11 single additions K2+g, the text group gives the largest reduction of G relative to K2, averaged
  over the 8 labels.

Everything else (K0, K1, changes in H) is descriptive. Failed predictions are reported. Runner `probe/b114_modal.py`;
output `runs/battery/battery114.json`.
