# What Do Zero-Data Self-Play Models Add Beyond an Off-the-Shelf Compressor? A Byte-by-Byte Test

**Ariel Elboim**  
Independent Researcher, Israel  
Corresponding author: lgboim@gmail.com  
ORCID: 0009-0001-1341-366X  
Working Paper, Version 1.0, September 30, 2026  
Code, data and per-byte compressor log losses: https://doi.org/10.5281/zenodo.23058002 (archive); https://github.com/lgboim/beyond-compressor

## Abstract

Self-play pretraining with zero data (Cowsik et al., 2026) trains byte-level transformers with gradient updates
only on the outputs of generated programs, and their zero-shot bits per byte on natural data fall with self-play
compute. We ask what the released models add to a strong existing predictor. As calibration, the off-the-shelf
compressor paq8px, run independently on each benchmark window with every byte of each window's archive counted, is
below the published minimum on 24 of 26 evaluation labels. We then log the probability paq8px assigns to each
observed byte (in its standard mode, conditioned on a block segmentation chosen from the whole window) and combine these probabilities with the learners' in a sequential fixed-share mixture; at the share used in the follow-up tests (s = 0.001), its deterministic
worst-case excess log loss relative to paq8px's logged probabilities is below 0.001 bits per byte on our 4095-byte
windows. On Metamath, C source and
rank-coded web text, the observed mean gain is below 0.002 bits per byte at all six released sizes (100k to 24M
parameters, final checkpoint); on Metamath and raw web text it stays below 0.002 across eight sampled 24M
checkpoints. On all eight benchmark text, code and formal labels, the logged probabilities of the observed bytes
are identical with block detection disabled on common retained rows, and under a protocol frozen before any
download the gain also stays below 0.002 on four new text, code and JSON sources. As a post-hoc diagnostic, the
hindsight-optimal corpus-wide convex mixture assigns zero weight to the learners on seven of these eight labels.
The same combiner realizes gains of about 0.1 to 1.4 bits per byte from a larger, not size-matched, natural-data
byte model on 17 of 24 row sets. Across the evaluated image and audio configurations, the self-play learners'
observed mean gains are at most about 0.02 bits per byte. Although released self-play ensembles have much lower loss than released fixed-prior ensembles on the compared row
sets, with paq8px as the reference the tested combiners extract little additional log-loss reduction from
the self-play learners on text, code and formal data; this quantifies realized complementarity of these predictors
and combiners, not the absence of information beyond paq8px. Post hoc, the first 512 bytes of each window carry 55%
to 89% of the learners' signed gain beyond the simpler compressor lpaq1 on those eight labels, and an lpaq1 variant
developed on already-scored rows and then frozen leaves at most 0.002 bits per byte on five of six further sources
fixed before download (C++ headers: 0.0034). We release paq8px's raw-byte-aligned per-byte log
losses, complete archive sizes, alignment metadata and scoring code.

**A lower zero-shot loss is not the same as a predictive gain beyond a strong compressor.**

**Keywords:** zero-data pretraining; self-play; byte-level language models; lossless compression; context mixing;
forecast combination; evaluation methodology.

## Plain Language Summary

A recent study trained small byte-level models, updating them only on the outputs of computer programs written by
another model,
and these models became better at predicting natural data such as text, images and sound. We ask how much they add
to an existing compressor that uses hand-engineered models, has no neural pretraining and is run separately on each
file. When the compressor
predicts each byte first and the new models' predictions are then mixed in by our specified rule, the additional gain is small on the
text, code and formal-mathematics benchmarks we tested; for these, switching off the compressor's whole-file block
detector does not change its logged losses on the common evaluated windows. This holds in separate checks across
model sizes and across training checkpoints, and on four new text, code and structured-data sources that we chose
before downloading them, even though the self-play models have much lower loss on their own than models trained
without the adaptive generator. An improved version of a simpler compressor, fixed before testing, leaves a similarly small gain on five of six further sources (except the tested C++ headers). On images and sound the gains are modest. A larger model pretrained on natural data
achieves gains of about 0.1 to 1.4 bits per byte on many tested sources under the same rule, so the comparison can
register a substantial improvement, without guaranteeing that it extracts every kind of useful information. We release the
compressor's per-byte log losses and the scoring code so that future byte-level models can be evaluated on the same
windows.

## AI Use Disclosure

Generative AI tools (Anthropic Claude via Claude Code, and OpenAI ChatGPT and Codex) were used to assist with code development,
experimental execution, adversarial review, separate recomputation of the reported numbers from saved artifacts,
literature discovery, and language editing. The author directed the research and formulated the research questions; the study used hashed protocols recorded in the project log (Appendix H); failed gates, post-outcome amendments and exploratory analyses are disclosed in
the manuscript and audit record. AI-assisted recomputation and review are internal checks, not independent replication. The author is responsible
for the final manuscript. Numerical results were checked against saved artifacts and
the documented audit record.


## 1 Introduction

Cowsik et al. (2026) pretrain byte-level transformers with no gradient update on natural data. A learned generator
proposes programs for a small Brainf\*ck-like universal machine, the programs run, and a learner is trained to predict
the bytes they emit. Evaluated zero-shot on natural data (text, code, formal mathematics, audio, images, DNA and more),
the learners' loss in bits per byte falls as self-play compute grows. The authors' key hypothesis is that self-play
discovers generic predictive regularities, "such as copying, recursion, and hierarchical composition", that transfer
because they do not depend on the contingent information of any one dataset; in their Section 4 they propose a
universal-data ansatz to interpret the scaling results. They also report that starting natural-data training from a
self-play checkpoint reaches a given validation loss with fewer natural-data tokens (their Figure 6). We do not test
that pre-pretraining (warm-start) setting; we study the released models' zero-shot predictions.

A zero-shot score says how well a model predicts, but not what its predictions contain that other predictors lack.
Probabilistic prediction and lossless compression are tightly linked: a sequential predictive distribution induces an
ideal code length equal to its log loss, which arithmetic coding attains up to coding and metadata overhead (Witten et
al., 1987; Delétang et al., 2024). Much of the structure in natural byte streams can also be exploited online (Bell et
al., 1989), and copying and repetition in particular are modelled explicitly by context-mixing compressors, which makes
a strong one a natural reference for asking what the learned regularities add. The authors aim at an efficient computable
approximation to universal prediction; universal (Solomonoff) prediction is itself a Bayesian mixture over programs,
and context-mixing compressors are engineered mixtures of many online models, so the question is also whether the learned predictor adds to an engineered mixture of online
predictors. The reported natural-data zero-shot
evaluation includes no compressor, n-gram or in-window adaptive baseline. We therefore ask two questions. The first is calibration: where does an
off-the-shelf compressor, run independently on each evaluation window, sit relative to the published scores? The
second, the subject of this paper, is incremental: after the compressor's predictor has assigned a probability to the
observed byte at each position, do the learners' predictions still lower the log loss when the two are combined? A
learner can be worse than the compressor and still help, if its errors differ; it can be close to it and add little,
if its errors are the same.

**The test** (Figure 1A). A logging-only patch, which leaves paq8px's archive sizes unchanged, records the
probability it assigns to every byte of each retained 4095-byte evaluation window, and we combine these probabilities
with a learner's in a sequential fixed-share mixture. The realized gain G is the mixture's reduction in mean log loss
relative to paq8px's logged probabilities. G is net: at the share s = 0.001 used in the headline follow-ups, its
worst-case excess log loss is below 0.001 bits per byte. In its standard mode paq8px conditions on a block
segmentation chosen from the whole window; we report where this matters. The question is operational: do the
learners realize additional gain once this strong, hand-engineered predictor is available? We do not claim that the
two have comparable priors or computation. paq8px was not our original baseline: we adopted it after earlier results
had shown standard compressors to be competitive (Section 3.1), so the follow-up tests were protocolized before their
outcomes were computed. G measures realized complementarity under a given combiner, not information; a small G does
not show that the learners contain nothing another combiner or another use of the model could extract.

**What we find.** Each experiment designated as prespecified began from a written protocol whose SHA-256 hash was
recorded before scoring; post-hoc diagnostics, analyses of already-seen arrays and amendments (three in Batteries 88 to 112 made after partial output or outcomes were available, and one in Battery 114
made after a four-window smoke test but before the full run's outcomes) are identified separately, and failed predictions are reported with their denominators (Appendices F and G).

1. *Calibration.* paq8px is below the published minimum on 24 of the 26 evaluation labels (Section 3.1).
2. *Text, code and formal data.* The observed mean gain beyond paq8px is below 0.002 bits per byte on Metamath, C
   source and rank-coded web text at all six released sizes (100k to 24M, final checkpoint), on Metamath and raw web
   text at all eight sampled 24M checkpoints, and, under a protocol frozen before any download, on four new text,
   code and JSON sources. As a post-hoc diagnostic, the hindsight-optimal corpus-wide convex mixture assigns zero
   weight to the learners on seven of the eight benchmark text, code and formal labels. Against the weaker, strictly
   sequential compressor lpaq1 the same ensembles realize 0.0085 to 0.0552, so the near-zero result depends on the
   strength of the reference (Section 3.2).
3. *Positive comparison with a natural-data byte model.* The same combiner realizes about 0.1 to 1.4 bits per byte
   from bGPT, a larger (110M), not size-matched byte model trained on natural data, on 17 of 24 row sets (Section 3.3).
4. *What self-play changes.* Released self-play ensembles have 1.0 to 5.5 bits per byte lower loss than released
   fixed-prior ensembles (six row sets, 3M and 6M, final checkpoint), and mixed with our simpler online predictor
   V_match they do realize gains. In an amended, descriptive analysis of the released curriculum learners, the gain
   beyond paq8px rises across generator endpoints on planar CIFAR-10 but stays near its floor on raw web text and
   below 0.002 on all eight text, code and formal labels (Section 3.4).
5. *Images and audio.* The self-play learners' observed mean gains are at most about 0.02 bits per byte; on CIFAR-10
   a benchmark-informed hand-built online predictor realizes more (Section 3.5).
6. *Where the gain beyond a simpler compressor sits.* Post hoc, the first 512 bytes of each window carry 55% to
   89% of the learners' signed gain beyond lpaq1 on the eight text, code and formal labels. An lpaq1 variant
   developed on already-scored rows and then frozen leaves at most 0.002 on five of six further sources fixed
   before download (Section 3.6).

![Figure 1](figs/fig_hero.png)

**Figure 1.** *The test and its main results. (A) For each 4095-byte window, paq8px (standard mode, conditioned on a whole-window block segmentation) and a self-play learner each give a probability for the next byte; a fixed-share mixture (s = 0.001) combines them, and G is the mixture's log-loss reduction relative to paq8px alone. (B) paq8px's archive rate against the learners' published minimum log loss on the 26 labels, an unpaired calibration (Section 3.1). (C) G beyond paq8px of the evaluated self-play ensembles and of bGPT (110M, natural-data pretraining, not size-matched) on 24 row sets with a preassigned domain (Section 3.3). (D) Bits saved per byte by adding the learners, beyond lpaq1 and beyond paq8px, by position: equal-weight mean of the eight text, code and formal labels in log-width bins, post hoc; 55–89% is the per-label signed share of the gain beyond lpaq1 in the first 512 positions (Section 3.6). (E) G beyond the original and the frozen upgraded lpaq1 on six sources fixed before download (Table G1).*

**Scope.** We study one model family (released checkpoints up to 24M parameters), the 26 published evaluation labels, eight earlier project sources and twelve new sources (six in Battery 106 for the main tests, six in Battery 117 for the prospective test of
Section 3.6). Our conclusions concern realized gain under the tested combiners
(fixed-share mixtures, the exact Bayesian mixture and post-hoc static convex-mixture diagnostics); they do not rule out
gains from contextual or learned combiners, from larger self-play models, or from use as a warm start. We do not claim
that zero-data pretraining fails, and we do not evaluate the original paper's in-context tasks. We release paq8px's
raw-byte-aligned per-byte log losses, archive sizes, alignment metadata, the logging patch and the scoring code, so
that future models scored on the same windows can be tested the same way. An earlier version of this study developed
hand-built online predictors as baselines; that material is in Appendix B.


## 2 Setup

**Learners.** The authors' release (Cowsik et al., 2026) contains Llama-style byte transformers at six sizes, from 100k to 24M parameters (context
4096 bytes), with checkpoints every 256 rounds and at round 8191 and eight to ten seeds per size. It also contains a
fixed-prior baseline, trained on outputs of programs sampled from a fixed Solomonoff-style prior over the same program
space rather than from the adaptive generator, at five sizes from 100k to 6M; we evaluate it at 3M and 6M. An ensemble
of K seeds averages its members' probabilities. No gradient update of the learners uses natural data, but the authors
selected hyperparameters with validation loss averaged over DCLM and DNA, which they note introduces limited leakage.

**Benchmark.** Each of up to 256 rows per corpus is the letter `O` followed by a 4095-byte window, scored by the mean of
−log2 of the probability of each actual next byte. Six corpora ship with the release; we rebuilt the other 20 labels
with the authors' bake scripts, and at 100k parameters and round 8191 the released seeds reproduce the published K = 1
and K = 8 values on all 26 labels to within 3 × 10⁻⁵ bits per byte (Appendix A). The *published minimum* of a label is
its smallest value over sizes, rounds and ensemble sizes in the authors' figure data; the *evaluated ensemble* is a
released-seed ensemble at the size and round of that minimum (the published seeds where all are released, otherwise a
marked substitute).

**paq8px and its per-byte probabilities.** We run the open-source context-mixing compressor paq8px at level 8 on each
window as a separate file and report the complete archive size (Section 3.1). For the incremental test, a
logging-only patch records for each coded byte the nominal log loss its main predictor assigns (the sum over the eight
bit predictions of −log2 of the probability of the coded bit); archive sizes are unchanged. A window is *retained*
when the byte sequence coded by the main predictor equals the raw window; each analysis uses retained rows
(accounting details in Appendix D). paq8px also contains hand-written language-specific components, including a text
model with English, French and German stemming rules and language detection; its optional pre-training on an English
word list and its LSTM model were off at our settings. In its standard mode paq8px first scans the whole window to detect blocks of
different types and codes each block with type-specific models, so its probabilities are conditioned on a
segmentation chosen from the whole window. With block detection disabled, the window is coded as one block of a
declared type; this also fixes model routing, so it is not an isolated removal of look-ahead. On the common retained
rows of all eight benchmark text, code and formal labels and of the six new sources of Battery 106, the logged log losses of the
observed bytes are identical in the two modes; on 8 of the other 26 row sets they differ, and we state the mode of
every result there (Appendix D).

> **Definition (realized gain beyond paq8px).** For a window x₁ … x_N (N = 4095), let q_t be paq8px's logged
> probability of x_t and p_t the learner's. A fixed-share mixture with K experts, share s and equal initial weights
> predicts m_t = Σ_k w_{t,k} p_{t,k}. After x_t it sets v_k ∝ w_{t,k} p_{t,k} and w_{t+1,k} = (1 − s) v_k + s/K.
> The realized gain of adding the learner is
>
>   G = (1/N) Σ_t [ −log2 q_t − (−log2 m_t) ],
>
> averaged over a label's retained windows, in bits per byte. For K = 2 the fixed-share mixture assigns prior mass
> ½(1 − s/2)^(N−1) to the expert path that uses paq8px at every position, so its cumulative loss is at most
> −log2[½(1 − s/2)^(N−1)] bits worse than paq8px's and G ≥ −[1 − (N − 1) log2(1 − s/2)]/N, that is, G ≥ −0.00097 at s = 0.001 and G ≥ −0.00748
> at s = 0.01 (conservatively rounded; the exact values are about −0.000966 and −0.007474). This deterministic worst-case excess log loss holds for any learner and any data. G is reported net,
> with no correction. It is relative to paq8px's logged probabilities, not to its archive size.

The share s = 0.01 was fixed before paq8px's per-byte scores were computed; we then added s = 0.001 and the exact
Bayesian mixture (s = 0, G ≥ −1/N ≈ −0.000244). A threshold of 0.002 bits per byte, about twice the s = 0.001 worst
case, was fixed after the benchmark-wide gains had been seen and before the follow-up size, round and new-source
analyses (some final-round cells of the round sweep had been scored earlier); it is an operational threshold for this combiner, not a statistical equivalence bound.

**Static mixture diagnostic.** For one label, the static mixture (1 − α) q_t + α p_t with a single weight α for all
its windows has, at α = 0, derivative mean(p_t/q_t − 1)/ln 2 of its mean gain. The mean gain is concave in α, so a
negative derivative at α = 0 certifies that α = 0 is the hindsight-optimal weight over [0, 1]. This is a post-hoc
diagnostic on already-scored arrays; it says nothing about per-window, dynamic or contextual weights.

**Learners in each analysis.** Benchmark-wide analyses use each label's evaluated ensemble; the size sweep, at round
8191, the eight seeds and their ensemble; the round sweep, the eight-seed 24M ensemble at rounds 0 to 8191; the new
sources, E24, the eight-seed 24M ensemble at round 8191, fixed in advance (coverage of every analysis in Appendix D).

**A natural-data byte model.** bGPT (Wu et al., 2024) is a 110M-parameter byte transformer (4.5 times one 24M learner)
with three released single-modality checkpoints (text, images, audio), each pretrained by next-byte prediction on
format-preserving files. Its context covers each window; we extract per-byte probabilities as in the released code
(Appendix D). Each label was assigned the weights of its domain before the low-overhead analysis of Section 3.2 and,
for the new sources, before any score. bGPT differs from the learners in size, architecture and training data, and
our windows are headerless and can start mid-file, so it serves as a positive comparison, not a matched control.

**Uncertainty and protocols.** Intervals are 95% percentile bootstraps over windows, conditional on the fixed models
and windows; they are pointwise and descriptive, not simultaneous. Each prespecified experiment had a protocol with
numerical predictions whose SHA-256 hash was recorded before its outcomes were computed; a failed gate makes an
outcome inadmissible rather than a pass or fail. Post-hoc diagnostics, gate corrections and amendments are identified
separately, and all protocols, hashes and corrections are listed in Appendices F and G.


## 3 Results

### 3.1 Calibration: an off-the-shelf compressor against the published minimum

Under a protocol frozen before any output (Battery 88), we ran paq8px on every window of the 26 benchmark labels and
of eight earlier new sources, each window as a separate file with its header counted. paq8px was developed by others,
with hand-engineered models for text, images, audio and executables, and was not tuned on these rows; it is not a
matched compute, prior or information-access control for the learners. It was not our original baseline: an earlier
blind test on eight new sources had shown, prospectively, that the prespecified zlib reference was lower than the
learners on 5 of 8, and we then adopted paq8px as a stronger reference, so its results on those sources are
retrospective.

paq8px's archive rate is below the published minimum on 24 of 26 labels; the exceptions are pseudo-random bytes (8.044
against 8.006, where a uniform code costs 8.000) and arithmetic progressions (0.064 against 0.049). On identical rows
it is lower than the evaluated ensembles on the same 24 labels, by 1.1 to 1.3 bits per byte on the raw web-text,
Common Crawl, arXiv, C and Python labels, 0.65 on rank-coded web text, 0.95 on Metamath and 0.42 on CIFAR-10 in HWC
layout. Two choices favor the learners here: each published minimum is selected on the evaluation data across sizes,
rounds and ensemble sizes, and paq8px is charged its full per-window archive overhead (about 0.032 bits per byte). The
authors' no-natural-data arm pretrained on sampled probabilistic context-free grammars, which they find stronger than
self-play on text and code, also has best values above paq8px's archive rates in an unpaired comparison with their
figure data (for example 3.744 against 3.104 on raw web text); its checkpoints are not released. An archive rate and a
log loss are not the same object, and two benchmark sources themselves come from compression benchmarks (C source
and the KoLMogorov Test's DNA), so these absolute comparisons do not by themselves establish a predictive advantage;
nor do they negate the original transfer or scaling evidence. Two held-out-size fit checks, our no-floor power-law
diagnostic and the floor-form procedure used in the authors' Figure 1, did not validate a reliable forecast of the
compute at which the learners would reach paq8px (Appendix C). The rest of this section asks a question that does not
depend on which method scores lower: whether the learners' predictions lower the log loss once paq8px's are available.

### 3.2 The beyond-compressor test

**Benchmark-wide.** With the share fixed in advance at s = 0.01 (Battery 98), we predicted that the evaluated
ensembles would realize G > 0.01 on at least 8 of 26 labels; only 1 did. Because the worst-case cost at s = 0.01 is
0.0075 bits per byte, we repeated the analysis at s = 0.001 and with the exact Bayesian mixture (Battery 100,
exploratory). At s = 0.001 the mean gain is small and negative on all twelve row sets assigned the text domain, between
approximately −0.00096 and −0.00082, against a worst-case excess loss of about 0.00097 (Table 1). The largest gains are
on CIFAR-10 in HWC layout (0.0186), atlas float32 (0.0123) and arithmetic (0.0107). With the exact Bayesian mixture, G
is within 10⁻⁶ of its worst-case value −1/N ≈ −0.000244 on 31 of the 34 row sets; because that mixture retains the
full likelihood history, this does not exclude complementarity confined to later positions, which fixed share is
better placed to realize.

**By size.** At round 8191 (Battery 101; Figure 2A, C), the eight-seed ensemble's own loss on Metamath falls from 6.09
to 2.89 bits per byte from 100k to 24M parameters, against paq8px's 1.86, and on C source from 6.38 to 3.50, against
2.06. G stays between −0.00096 and −0.00084 on Metamath and C source and between −0.00053 and +0.00031 on rank-coded
web text, for the eight-seed ensemble and for the mean single-seed gain; no ensemble gain exceeds the frozen 0.002
threshold in these 18 cells (prediction Z1 held). On CIFAR-10 (HWC) the gain grows from −0.0005 at 100k to 0.0143 at
24M, with a dip from 1M to 3M.

**By round.** For the eight-seed 24M ensemble at eight checkpoints (Battery 102; Figure 2B, D), the own loss on
Metamath falls from 7.90 bits per byte at round 0 to 2.84 at round 1024 and ends at 2.89, and on raw web text from
8.29 to 4.43 at round 512, ending at 4.71. G is negative at all 16 of these points (largest −0.00085; prediction A2
held). Image and audio gains appear at different rounds: 8-bit audio is positive by round 256 and MusicNet by round
512; on CIFAR-10 (HWC) larger gains emerge at rounds 1024 to 2048 and peak at 6144 (0.0156). We do not claim
monotonicity or a plateau, and rounds are not a measure of training cost.

![Figure 2](figs/fig_beyond_paq.png)

**Figure 2.** *Own loss and realized gain beyond paq8px. (A) Eight-seed own loss by released size at round 8191; dashed lines, paq8px's per-byte log loss on the same rows. (B) The same for the eight-seed 24M ensemble along self-play rounds (web text is raw DCLM). (C, D) Realized gain G beyond paq8px (s = 0.001) for the same ensembles; the shaded band spans the combiner's deterministic worst-case bound to zero. (E) Positive comparison: G of bGPT (orange, 110M parameters, natural data, not size-matched) and of the evaluated self-play ensembles (black) on each row set with a preassigned bGPT domain.*

**New sources, prospectively.** Before downloading any byte, we froze a protocol naming four text, code and JSON
sources new to this project (English books from Project Gutenberg, 2026; Rust source of ripgrep, BurntSushi, 2024; JavaScript source of lodash,
lodash contributors, 2021; and a JSON country dataset, mledoze, 2026), an image source (KMNIST; Clanuwat et al., 2018)
and an audio source (FSDD; Jackson et al., 2018), with E24 as the learner
(Battery 106). With block detection disabled, all 256 windows of each source are retained, and G is −0.00096,
−0.00074, −0.00096 and −0.00094 on the four text-like sources, below 0.002 as predicted (N2); in standard mode only 2
of 256 Gutenberg windows are retained, and the standard-mode prediction N1 held on the retained rows. On KMNIST G is
0.0085 (N4 held); on FSDD it is 0.0019. We do not establish that these sources are unseen by bGPT.

**Static mixture.** The fixed-share mixture's dynamic weights could hide a gain that a constant weight would realize.
The hindsight-optimal corpus-wide convex mixture assigns exactly zero weight to the evaluated ensemble on seven of the
eight benchmark text, code and formal labels, where the derivative certificate of Section 2 is negative (−0.2246 to
−0.0942). On rank-coded web text the derivative is +0.1958 and the grid optimum, α = 0.01, realizes 0.00076 bits per
byte (Battery 105). A separate weight per window from the tested 18-point grid yields mean gains below 0.0009 on all
eight labels; this is not a bound on individual windows (one rank-coded window reaches 0.0035).

**A weaker, strictly sequential reference.** lpaq1 (Mahoney, 2007) is a smaller context-mixing compressor that codes
each byte from past bytes only. On the eight benchmark text, code and formal labels its log loss is 0.22 to 0.50 bits
per byte above paq8px's, and the same ensembles, mixed in the same way, realize 0.0085 to 0.0552 beyond it, with all
pointwise 95% lower endpoints positive (Battery 104). The near-zero gain beyond paq8px is therefore specific to the stronger reference, not a property of the combining
procedure alone; Section 3.6 examines where the gain beyond lpaq1 sits and how far a stronger lpaq1 variant reduces it.

**Calibrated members.** Online temperature calibration of each member before averaging did not reveal hidden text or
formal gains: G stays below 0.002 on Metamath, C source and rank-coded web text at all six sizes, and the prediction
that it would change the CIFAR-10 (HWC, 24M) gain by at most 0.005 failed because calibration lowered it (Battery
112; Appendix F.6).

**Table 1.** *Realized gain G (bits per byte) of the evaluated ensemble beyond paq8px on the eight benchmark text, code and formal labels (standard mode; 250 retained windows for rank-coded web text and 256 for each other label, 2,042 in total). Worst-case values, approximately: −0.007474 (s = 0.01), −0.000966 (s = 0.001), −0.000244 (exact Bayes). The archive rate counts every byte of each window's archive; the log loss is the mean of paq8px's logged per-byte log losses.*

| Label | Ensemble (size, round, K) | Published minimum | paq8px archive | paq8px log loss | G, s = 0.01 | G, s = 0.001 | G, exact Bayes |
|---|---|---:|---:|---:|---:|---:|---:|
| Metamath | 24M, 1024, 8 | 2.827 | 1.893 | 1.860 | -0.00708 | -0.00094 | -0.00024 |
| C source | 24M, 768, 8 | 3.269 | 2.096 | 2.063 | -0.00716 | -0.00094 | -0.00024 |
| Python | 24M, 768, 8 | 2.928 | 1.836 | 1.803 | -0.00717 | -0.00096 | -0.00024 |
| arXiv math | 24M, 768, 8 | 3.489 | 2.292 | 2.259 | -0.00724 | -0.00096 | -0.00024 |
| Web text (raw) | 24M, 768, 8 | 4.396 | 3.104 | 3.071 | -0.00725 | -0.00096 | -0.00024 |
| Common Crawl | 24M, 768, 8 | 4.122 | 2.816 | 2.783 | -0.00724 | -0.00096 | -0.00024 |
| KoLMogorov text | 24M, 768, 8 | 4.031 | 2.776 | 2.743 | -0.00713 | -0.00089 | -0.00024 |
| Web text (rank-coded) | 24M, 768, 8 | 3.857 | 3.219 | 3.188 | -0.00457 | +0.00009 | -0.00024 |

### 3.3 A positive comparison: a natural-data byte model

A small G could also mean that the test cannot register gains from any byte model on these data. With the same
combiner and s = 0.001, bGPT realizes gains between 0.11 and 1.36 bits per byte on 17 of the 24 row sets of the
benchmark-wide analysis with a preassigned domain (standard mode), for example 1.36 on Common Crawl text, 1.31 on raw
web text, 0.50 on arXiv mathematics, 0.28 on C source and 0.82 on CIFAR-10 in HWC layout; in the separate forced-mode
evaluation of the new sources it realizes 1.29 on Gutenberg books. It realizes little or none on Metamath (−0.0007), planar CIFAR-10, Fashion-MNIST, the shipped 8- and 16-bit audio
and the yes/no speech source, and 0.13 to 0.27 on the ESC-50, Speech Commands and MusicNet row sets. Our prediction that bGPT's gain would exceed the learners' on
every domain row set (L3) failed, for example on 8-bit audio (learners 0.0042, bGPT −0.0003). bGPT differs from the
learners in size, architecture and data, a format mismatch on our headerless image and audio windows is an untested
possibility, and its Wikipedia training text may overlap our web-text windows. The comparison shows that the test can
register large realized gains; it does not show that natural-data training is their source. For context only, the
authors' released Figure 6 data give final validation losses of about 1.48 to 1.52 bits per byte on their own DCLM
split for the same 24.4M architecture trained on natural text (not evaluated on our windows).

### 3.4 What self-play changes, and complementarity with a simpler predictor

**Self-play against the fixed prior.** At 3M and 6M parameters and round 8191, four-seed ensembles of the released
self-play arm have lower loss than those of the released fixed-prior arm on all 12 comparisons (six row sets), by 1.0
to 5.5 bits per byte (Battery 102, part B; Table E1). Beyond paq8px, the fixed-prior ensembles realize between −0.00097
and +0.00029 (positive only on 8-bit audio), while the self-play ensembles realize small positive gains on the four
image and audio row sets (0.0015 to 0.0067) and none on Metamath or raw web text. This compares released training arms at equal rounds, not a component-level causal test of the adaptive generator:
the released figure code lists pools of 1,536 programs per round for self-play and 2,048 and 1,024 for the fixed-prior
arm at 3M and 6M, consistent with the batch sizes the authors tune at each scale, so equal rounds are not equal numbers
of training tokens (their Figure 2 compares compute-optimal frontiers).

**Generator progress and reward.** Two further released families of 1M learners allow a closer look (Batteries 110 and
111). Their protocols were frozen before scoring, but an array-shape gate in both was misspecified for the two corpora
with 250 and 240 rows and was corrected after the outcomes were printed, and one reward arm (loss_delta) has three
released seeds instead of the specified four and is included in the counts below; we report these as amended,
descriptive analyses. The curriculum learners, evaluated at learner round 4095, are trained from scratch on corpora
sampled from the generator up to successive training endpoints (G0, the untrained generator, then T = 256 to 4096); at
the four cells compared, our ensemble scores agree with the K = 8 columns of the authors' released Figure 3 data to
within 6 × 10⁻⁶ bits per byte. On raw web text the eight-seed ensemble loss falls from 8.18 bits per byte at G0 to 4.83
at T1024 and is 4.95 at T4096, while G beyond paq8px stays at −0.00096 at every endpoint; on all eight text, code and
formal labels G stays below 0.002 at every endpoint (48 of 48). On planar CIFAR-10, G rises at every endpoint, from
−0.00093 to 0.00264 (HWC: −0.00095 to 0.00447). Among seven reward arms at 1M and round 8191 (the canonical reward, five
ablations and the fixed prior), G on the text, code and formal labels stays below 0.002 (56 of 56); on CIFAR-10 only
the canonical and signed rewards realize positive gains (HWC 0.0078 and 0.0025), and lower own loss goes with higher
gain across arms (Spearman −0.89 on HWC). These are descriptive associations across released training runs.

**Complementarity with a simpler online predictor.** The result depends on the reference. Mixed by the same
fixed-share rule at s = 0.01 with V_match, our frozen hand-built online predictor (Appendix B), the learners do add
realized gain: on Metamath the evaluated 24M ensemble adds 0.249 bits per byte to V_match (Battery 94), while it
realizes −0.00708 against paq8px at the same share. Against V_match the gain at round 8191 is larger at 24M than at
100k on 8 of 8 labels (Battery 93; the six-size MusicNet trend prediction failed), and larger for eight seeds than for
one on 25 of 26 labels with nested seed subsets (median gains 0.0016 at k = 1 and 0.0281 at k = 8; the exception is
arithmetic). Ensembles of seed-only variants likewise reach lower held-out loss in data-constrained web-text
pretraining (Kim et al., 2026). The ensemble advantage persists when a uniform expert is added (median ratio 0.933 over
23 eligible labels; Battery 95), and one temperature-calibration family recovers 0.047 to 0.092 bits per byte of own
loss against 0.55 to 0.96 from ensembling (Battery 97), so this calibration family does not account for it; whether it
reflects knowledge or calibration is not identified.

### 3.5 Images and audio, and failed predictions

The learners' largest gains beyond paq8px are on images. Our prediction that they would concentrate at bytes that
continue an arithmetic progression of earlier values failed on all three of its criteria (Battery 107); post hoc, much
of the signed net gain is realized at bytes that differ by more than 32 from the corresponding earlier byte, an
outcome-conditioned accounting, not a mechanism. Two knowledge-free hedgers mixed with paq8px in the same way, a
uniform distribution and causal order-0 counts (the Krichevsky–Trofimov estimator; Krichevsky and Trofimov, 1981), realize less than the learners on
all four image row sets (Battery 108), although other hedging or calibration schemes are not excluded. On CIFAR-10, our
frozen, benchmark-informed hand-built predictor V_auto realizes more beyond paq8px than the learners in both layouts
(0.0479 against 0.0186 in HWC layout, 0.0909 against 0.0072 in planar layout; Battery 109), so these learner gains are
not uniquely achieved by self-play there; the two layouts come from one dataset. On Fashion-MNIST the learners realize
0.0084 and V_auto 0.0016, and the learners still realize 0.0072 once V_auto is in the mixture (realized-combiner
accounting, not shared or unique information).

Across Batteries 88 to 112, 84 prespecified numerical criterion families were recorded: 52 met their predicates, 25
failed (24 through Battery 109 and the calibration prediction of Battery 112), and 7 belong to the amended, descriptive
Batteries 110 and 111. The 25 are failed criterion families on the recorded, explicitly qualified analyses, not an
error rate. They include larger gains beyond paq8px than observed, bGPT above the learners on every domain row set, and
an advantage of the learners over paq8px on a local program-output surrogate of the machine (Battery 103: 24M loss
0.304 against paq8px's 0.253, gain beyond paq8px 0.0153). Appendix F lists every criterion with its definition, result and population, and separately every gate failure,
amendment and correction. The follow-ups of Section 3.6 add 17 more, 8 met and 9 failed (Appendix G).

### 3.6 Where the gain beyond a simpler compressor appears, and how it shrinks

These follow-ups were run after the results above and are of four kinds: post-hoc analyses of saved arrays,
prespecified interventions on already-scored rows, exploratory development, and one prospective test (Appendix G lists protocols, hashes and every failed prediction).

On the eight benchmark text, code and formal labels, the learners realize 0.0085 to 0.0552 bits per byte beyond
lpaq1. The first 512 positions of each window (12.5% of bytes) carry 55% to 89% of this signed gain, and in a
post-hoc breakdown, early bytes that an earlier 8-byte repeat in the window predicts correctly carry 37% to 75% of it
(Battery 113). Beyond paq8px, the mean per-byte gain is negative in every position stratum on seven of the labels;
on rank-coded web text it is positive only in the first 64 positions. The gain beyond lpaq1 therefore sits where an
online compressor has seen least of the window; this locates it but does not identify a mechanism. Within paq8px,
suppressing the direct mixer inputs of any one of its 14 text-path model groups, including the text model with its
hand-written English, French and German morphology, leaves the gain at or below 0.002 on all eight labels, as does keeping the direct inputs of only the order-n, match
and word groups (Battery 114). Suppressed groups still reach paq8px's final SSE stage
through shared state, so this does not show that any group is dispensable.

We then modified lpaq1 itself. Of five prespecified changes, each tested alone on the same labels, initializing the mixer's input weights at 0.3 rather than 0 gave the largest mean reduction, to at most 0.002 on
five of the eight
(Battery 115); this is consistent with making lpaq1's own predictions influential earlier in each window. Exploratory
development on the 12 row sets already scored (Battery 116; 18 logged variants) then produced an lpaq1 variant with
16 switches from standard context-mixing practice, some of them text-specific (more contexts; quote, bracket and key
contexts; two additional SSE stages; balanced initial weights), which leaves at most 0.002 on all 12. Frozen and tested once on
six further text, code and markup sources fixed before download (Battery 117, Table G1), it leaves at most 0.002 on
five and 0.0034 on C++ headers, whereas the original lpaq1 leaves 0.009 to 0.037 on all six. Under this test, much of
the learners' realized gain relative to the original lpaq1 is thus reproduced by hand-engineered online context mixing.


## 4 Discussion

**What the test shows.** Self-play clearly helps the learners on their own: on the six row sets tested at 3M and 6M,
the released self-play ensembles have much lower loss than the fixed-prior ensembles, and against the simpler V_match
reference they realize positive and sometimes much larger gains. Beyond paq8px, however, their gains stay below 0.002 bits per byte on three text and formal labels at all six sizes,
on two at eight sampled checkpoints and on four prospective sources; separately, a natural-data byte model realizes
about 0.1 to 1.4 beyond paq8px on 17 of 24 assigned-domain row sets. Beyond the weaker lpaq1 they realize 0.0085 to 0.0552,
most of it early in each window, and a frozen, upgraded lpaq1 variant leaves at most 0.002 on five of six further
sources. Zero-shot bits per byte and realized gain beyond a strong compressor therefore answer different questions:
the first ranks predictors, the second asks whether a predictor's errors differ usefully from a reference's. They can
disagree.

**A hypothesis for the pattern.** The generator is rewarded with an absolute, AdamW-preconditioned alignment between
the learner's gradient on a program's output and its parameter movement since an earlier checkpoint; the authors
interpret this as concentrating the generator on the frontier of what the learner can learn and relate it to
learning- and compression-progress rewards (Schmidhuber, 2009). Such a reward may favor structure that a byte learner
acquires quickly from short programs, such as counts, repetitions, periodic patterns, arithmetic continuation and
copying, much of which context-mixing compressors model explicitly. Of the generator's training-history records
that the authors' detector assigns to five recognized sequence families, 97.6% are arithmetic progressions modulo 256
(the released data behind their Table 1); this is conditioned on the detector and is not the share of all outputs,
and such progressions also appear early under the uniform prior. Section 3.6 locates the text gain beyond a simpler
compressor early in each window, where an online compressor has seen little. We have not tested the hypothesis directly: our
prediction that the image gains would concentrate at arithmetic continuations failed (Section 3.5), and a direct test
would score paq8px on the generator's own outputs across rounds. In the authors' universal-data ansatz, self-play can
improve natural-data loss only through universal predictive structure, since the learners' gradient updates contain
no natural-data bytes. The authors present the tabula-rasa setting as a controlled experiment for isolating such
structure, not as a replacement for natural data (their Section 6). Our results add an observable to that account: on the tested text, code and formal streams,
whatever the released learners acquire realizes little log-loss reduction beyond paq8px under our combiners, while on
images and audio it realizes a small amount. This is a complementary observable, not the causal test the authors call
for; whether larger self-play models realize more is open and directly testable with the released log losses.

**Epiplexity and the curriculum.** The authors use a prequential-style proxy for epiplexity (Finzi et al., 2026) to
measure how much structure a bounded learner extracts from generator outputs, report higher estimated epiplexity for
later generator checkpoints, and describe it and zero-shot loss as improving steadily.
In our post-hoc reading of their released curriculum data (Appendix F.5), the estimated epiplexity keeps rising from
generator endpoint 1024 to 4096, while the loss of the 1M learners on raw web text is higher at endpoint 4096 than at 1024, both for the eight-seed
(K = 8) ensemble and in the four-seed means plotted by the authors; on planar CIFAR-10 it keeps falling. Finzi et al. note that higher epiplexity does not guarantee better
performance on a specific task, and that a learner can raise it by acquiring an in-context Markov-estimation strategy
absent from the generating process. Epiplexity measures how much structure a learner absorbs, not whether its
predictions realize gain beyond a given compressor. For the latter, the released curriculum learners give a descriptive answer (Section 3.4): raw-web-text loss falls
from 8.18 to 4.83 bits per byte with no gain beyond the compressor, while on planar CIFAR-10 the gain rises at every
endpoint.

**What would count as progress.** A zero-data model that realizes a gain clearly above the combiner's worst-case
cost beyond paq8px, on text or code sources fixed before evaluation, would provide prospective evidence of a realized
reduction in log loss beyond this compressor under the specified combiner; the worst-case bound controls
excess loss and is not a significance threshold. Once a new model has been scored on identical byte windows with the same prefix, retention and
normalization, combining its saved probabilities with the released compressor log losses is cheap. We suggest
reporting this gain next to zero-shot bits per byte, with a positive comparison such as a natural-data model.

**Images and audio.** Where the learners' remaining image gain comes from is open: it did not concentrate at
arithmetic continuations as predicted, it is not reproduced by two knowledge-free hedgers, much of it is realized at
bytes with large value changes, and on CIFAR-10 a benchmark-informed hand-built predictor realizes more.

**Limitations.** We study one model family up to 24M parameters, released checkpoints only, and 4095-byte windows. The
combiners are simple (fixed share, the exact Bayesian mixture and post-hoc static weights); contextual or learned
combiners, or features of the learners rather than their output probabilities, may extract more, and we make no claim
about the information the learners contain. paq8px in standard mode conditions on a whole-window segmentation, which
leaves the logged probabilities unchanged on the common retained rows of the text, code and formal labels but not on
8 of the other 26 row sets. paq8px is heavily hand-engineered in the public compression ecosystem; we have not
established whether its design history was influenced by these or closely related corpora. Twenty of the 26 labels
were rebuilt with the authors' scripts and checked at the aggregate level only. bGPT is not a matched control, and the
authors' grammar-pretrained arm, stronger than self-play on text and code in their figure data, is not released.
Several analyses reuse arrays we had already seen; the prospective confirmations are Battery 106 for the tests
against paq8px and Battery 117 for the frozen lpaq1 variant of Section 3.6, which was itself developed on
already-scored rows. Finally, zero-shot prediction is one use of the learners: the authors report that starting natural-data training from a self-play checkpoint reaches a given validation loss with
fewer natural-data tokens; the gap narrows considerably by convergence, and by design the comparison does not count the
self-play compute, which the authors treat as a one-time cost amortized across downstream runs (their Figure 6 and
Appendix A.2). Our test does not address that use.


## 5 Related work

**Synthetic and universal pretraining.** Grau-Moya et al. (2024) meta-train sequence models on outputs of random
programs for a Brainf\*ck variant; the models beat a loose Solomonoff upper bound on held-out program outputs and
transfer modestly to Chomsky-hierarchy tasks and variable-order Markov sources relative to a uniform predictor, while
models trained directly on Markov sources match the Bayes-optimal context-tree weighting predictor; no natural data or general-purpose compressor is evaluated.
Bloem (2025) pretrains on iterated random computation and finds zero-shot loss on enwik8, JavaScript and Linux source
well below an in-window Markov model of order 0 to 5 tuned per dataset, the closest precedent to our calibration,
without a compressor comparison. Procedural pretraining instils structure that helps fine-tuning on algorithmic tasks
(Shinnick et al., 2025), and front-loading a small share of procedural data speeds later pretraining on natural
language, code and informal mathematics (Jiang et al., 2026). Cowsik et al. (2026) add a generator trained by
self-play with a learning-progress reward, in the tradition of intrinsic motivation by learning and compression
progress (Schmidhuber, 2009), and use a prequential-style proxy for epiplexity (Finzi et al., 2026) to check that
later generator checkpoints yield corpora from which a fixed 1M learner absorbs more structure; Finzi et al. define
epiplexity through a time-bounded two-part code, recommend the prequential estimate only for crude ranking, and do not
discuss classical compressors. Of two unreviewed independent reports on the released checkpoints, one studies
arithmetic heads (aujurd22, 2026); the other reports that an in-window order-0 counter beats single released learners
on text and DNA (Maverick-Ansh, 2026).

**Prediction as compression.** Delétang et al. (2024) turn language models into compressors by arithmetic coding and
compare them with gzip, LZMA2, PNG and FLAC on 2048-byte chunks; several large text-trained models beat PNG and FLAC on
raw rate but not once their parameters are counted, while small enwik8-trained transformers expand image and audio
data. Heurtel-Depeiges et al. (2025) find that byte transformers of up to about 20M parameters with a 4096-byte
context beat standard codecs on out-of-distribution data of the modalities they were trained on but transfer weakly to
unseen ones, and report no emergence of universal compression at that scale; they also compare with Bellard's
adaptive online transformer (NNCP), with roughly tied results. Neither study uses a context-mixing compressor as the
reference or asks the incremental question. Online neural and context-mixing hybrids such as cmix (Knoll, 2013) and
NNCP (Bellard, 2021) can improve compression on particular text benchmarks, but adapt to the stream being compressed
and are not zero-shot; separately, bGPT (Wu et al., 2024), pretrained offline on natural data, realizes large gains
under our combiner, so a small realized gain beyond paq8px is not inevitable for a neural model. For simple binary
sources, how much training data a learned coder needs to beat a universal source coder has been bounded (Høst-Madsen,
2021).

**Incremental predictive value.** Combining forecasts can beat each (Bates and Granger, 1969); in language modelling,
interpolating models of different kinds exposes their complementarity (Mikolov et al., 2011); and a forecast is said
to encompass another when the optimal combination puts all weight on it (Chong and Hendry, 1986; Harvey et al., 1998).
In machine learning, whether two models make the same errors has been measured as error consistency (Geirhos et al.,
2020). Our realized gain G is a sequential empirical log-loss diagnostic inspired by this literature: when the weight
stays on the compressor, the question is whether the compressor encompasses the learner within the tested
combination class, and the static-weight certificate of Section 2 asks this for one constant weight on this finite
corpus, not as a population encompassing test. Mixing neural predictors with context models is established practice
in compression, in PAQ8 (Knoll and de Freitas, 2012), cmix, paq8px (Mahoney and paq8px contributors, 2026) and hybrid
neural compressors (Schmidhuber and Heil, 1996; Goyal et al., 2021; Mao et al., 2022); we use it only as a measurement.

**Online prediction and context mixing.** The mixtures here are prediction with expert advice (Cesa-Bianchi and
Lugosi, 2006) under the fixed-share rule for tracking the best expert (Herbster and Warmuth, 1998); with equal initial
weights, the Bayesian mixture's cumulative log-loss regret to the best fixed expert is at most log2 K bits (Vovk, 1990;
Haussler et al., 1998; Hutter, 2003). This is the lineage of universal sequential prediction (Feder et al., 1992) and
adaptive text compression (Cleary and Witten, 1984; Willems et al., 1995); paq8px and lpaq1 (Mahoney, 2007) descend
from the PAQ family of context-mixing compressors (Mahoney, 2005). Baselines developed after inspecting a benchmark
raise the data-snooping problem familiar from forecasting (White, 2000); hence our separation of prespecified from
post-hoc analyses and our sources fixed before download.


## Appendix A. Benchmark, rows and comparators

**Labels.** The benchmark has 26 evaluation labels. Six ship with the release: arithmetic progressions, 8-bit and
16-bit audio, rank-coded web text, DNA and melody. We rebuilt the other 20 with the authors' bake scripts, run
unchanged, from the AITDCC benchmark data (protein, C source, pseudo-random bytes, float32 atlas, astronomy), the
llm-compression benchmark of Huang et al. (2024) (arXiv mathematics, Common Crawl, Python), the enwik9 and DNA
streams of the KoLMogorov Test (Yoran et al., 2025), Metamath (Megill and Wheeler, 2019), raw DCLM (Li et al.,
2024), ESC-50 (Piczak, 2015), Speech Commands (Warden, 2018), CIFAR-10 (Krizhevsky, 2009) and MusicNet (Thickstun et
al., 2017). Our rebuilt arithmetic file is byte-identical to the shipped one.

Several labels share sources. KoLMogorov DNA is the shipped DNA with each byte XOR 4. Raw DCLM partly overlaps the
rank-coded text, which relabels bytes by frequency rank: the first 25 rows of the two correspond under one injective
byte map. ESC-50, Speech Commands and MusicNet each appear at two sampling rates with the same recordings, and
CIFAR-10 appears in two pixel layouts.

**Rows.** Each row is the letter `O` followed by a 4095-byte window, scored at context 4096. We use the first 256
rows of each label, fewer where a corpus has fewer (Table A1), 6,374 rows in all. Appendix B of Cowsik et al. (2026)
describes 255-byte records at context 256; the released bake scripts produce 4095-byte windows, and these reproduce
the published values.

**Reproduction.** At 100k parameters and round 8191, all eight seeds behind the published values are released.
Scored on our rows, they reproduce the published K = 1 and K = 8 values on all 26 labels; the largest absolute
difference over the 52 values is below 3 × 10⁻⁵ bits per byte (Battery 75). This checks aggregate scores, not row
bytes.

**Published minimum.** For each label, the published minimum is the smallest value over sizes, rounds 0 to 8191
and ensemble sizes K = 1 to 14 in the authors' figure data file, 1,490 aggregate settings per label. A K-model
ensemble averages its members' probabilities, and each published per-K value averages the loss over seed subsets.
Per-row values are not released, so comparisons with the published minimum have no row-level interval.

**Evaluated ensembles.** The evaluated ensemble uses released seeds at the size and round of the published minimum,
on identical rows (Battery 75). Seven are exact reconstructions from the eight released 24M seeds, within 2 × 10⁻⁴
bits per byte of the published value. The other 19 are marked substitutes. Where the published ensemble had nine or
eleven 24M seeds, the substitute uses the eight released seeds. Where it had eight seeds at 3M or 100k, nine or ten
seeds are released and the eight used were not recorded; the substitute then uses all released seeds, a frozen
fallback adopted because several eight-seed subsets matched the published DNA value within 0.002. Each substitute's
mean is within 0.03 bits per byte of the published minimum. A substitute is not a reconstruction, and its
row-bootstrap intervals do not cover the missing or unidentified seeds.

**Table A1.** *Rows, published minimum (bits per byte; size, round, K) and evaluated ensemble per label.*

| Label | Corpus | Rows | Published minimum | Evaluated ensemble |
|---|---|---:|---|---|
| Web text (rank-coded) | shipped | 250 | 3.857 (24M, 768, 11) | substitute, 8 seeds |
| Web text (raw DCLM) | rebuilt | 256 | 4.396 (24M, 768, 11) | substitute, 8 seeds |
| KoLMogorov text (enwik9) | rebuilt | 256 | 4.031 (24M, 768, 11) | substitute, 8 seeds |
| Common Crawl | rebuilt | 256 | 4.122 (24M, 768, 11) | substitute, 8 seeds |
| arXiv math | rebuilt | 256 | 3.489 (24M, 768, 11) | substitute, 8 seeds |
| Python | rebuilt | 256 | 2.928 (24M, 768, 11) | substitute, 8 seeds |
| C source | rebuilt | 256 | 3.269 (24M, 768, 11) | substitute, 8 seeds |
| Metamath | rebuilt | 256 | 2.827 (24M, 1024, 11) | substitute, 8 seeds |
| DNA | shipped | 256 | 2.159 (3M, 4608, 8) | substitute, all 9 seeds |
| KoLMogorov DNA | rebuilt | 256 | 2.133 (3M, 4096, 8) | substitute, all 9 seeds |
| Protein | rebuilt | 256 | 4.966 (100k, 6144, 8) | substitute, all 10 seeds |
| 8-bit audio | shipped | 240 | 2.142 (24M, 5888, 8) | exact, 8 seeds |
| ESC-50 | rebuilt | 256 | 1.851 (24M, 5120, 9) | substitute, 8 seeds |
| ESC-50, 11 kHz | rebuilt | 256 | 2.676 (24M, 5120, 9) | substitute, 8 seeds |
| Speech Commands | rebuilt | 256 | 1.947 (24M, 5120, 9) | substitute, 8 seeds |
| Speech Commands, 8 kHz | rebuilt | 256 | 2.076 (24M, 5120, 9) | substitute, 8 seeds |
| 16-bit audio | shipped | 244 | 4.933 (24M, 5376, 8) | exact, 8 seeds |
| Melody | shipped | 17 | 1.813 (24M, 5376, 8) | exact, 8 seeds |
| MusicNet | rebuilt | 256 | 1.904 (24M, 1536, 11) | substitute, 8 seeds |
| MusicNet, 11 kHz | rebuilt | 256 | 2.970 (24M, 5120, 9) | substitute, 8 seeds |
| CIFAR-10 (HWC) | rebuilt | 256 | 5.033 (24M, 5376, 8) | exact, 8 seeds |
| CIFAR-10 (planar) | rebuilt | 256 | 5.709 (24M, 5120, 9) | substitute, 8 seeds |
| Arithmetic progressions | shipped | 256 | 0.049 (24M, 5888, 8) | exact, 8 seeds |
| float32 atlas | rebuilt | 247 | 6.336 (24M, 5376, 8) | exact, 8 seeds |
| Astronomy | rebuilt | 256 | 2.384 (3M, 5632, 8) | substitute, all 9 seeds |
| Pseudo-random bytes | rebuilt | 256 | 8.006 (24M, 6144, 8) | exact, 8 seeds |

## Appendix B. Hand-built online predictors

Before adopting paq8px as the reference, this study developed its own online predictors and tested them in
Batteries 75 to 87 (Table B1). V_match is the reference of the complementarity analyses of Section 3.4 (Batteries 93
to 97), and V_auto is the hand-built image comparison of Section 3.5 (Battery 109).

**Common rules.** Each row is scored from an empty state, left to right, without the `O` prefix. Every expert
predicts the next byte from earlier bytes of the window only, and all state is updated after each byte. No
parameters are trained offline, but the designs were informed by the benchmark, as stated below. Experts are
combined by a Bayesian fixed-share mixture (Herbster and Warmuth, 1998): from uniform initial weights, each weight is
multiplied by its expert's probability of the observed byte, renormalized and mixed with uniform weights at share
0.01.

**V_base** mixes six experts: order-0 and order-1 byte counters (prior 0.05 per value); "hold", with probability 0.9
on the previous byte; a smooth step, a discrete Laplace distribution on the byte circle centred on the previous byte,
with a running scale; a constant-step extrapolation, the same distribution centred on 2x(t−1) − x(t−2); and a copy
expert, which proposes the byte that followed the most recent earlier occurrence of the longest current suffix of 3
to 32 bytes, with confidence equal to the running hit rate of earlier proposals in its match-length bucket. The
expert library was selected on five development corpora (arithmetic, 8-bit audio, rank-coded text, DNA and melody).
All definitions and constants were then frozen in code before any other source was scored.

**V_struct and V_auto.** V_struct (Battery 76) starts from a 12-expert extension of V_base, developed partly on the
development corpora and on 16-bit audio. It adds fourteen experts chosen from format knowledge after four gap domains
were known (CIFAR-10, 16-bit audio, float32 atlas and astronomy data): phase-conditioned byte counts, smoothness at
fixed lags, 16-bit sample predictors, the JPEG-LS median edge detector for two raster geometries, and channel and
plane differences, with weights kept per phase t mod P, for P = 1 to 4. V_auto (Battery 77) replaces V_struct's
six fixed-geometry raster experts with four whose lags are chosen online, per row: a short lag in 1 to 8 and two long
lags in 9 to 1100, those with the lowest running mean circular absolute difference |x(t) − x(t−L)|. V_auto has no offline parameter
training, but it is benchmark-informed: its experts and search ranges were designed after inspecting the benchmark
formats. It was frozen before it scored any benchmark label. An audit found a scale-update defect in the frozen code:
it skips the scale update of the four online-lag experts whenever a valid predicted centre is negative. A versioned
correction, run after the frozen readout, changes no label mean by more than 0.00111 bits per byte (CIFAR-10 in HWC
layout: 5.055 frozen, 5.056 corrected) and no reported count. We keep the original implementation, with the defect,
in Battery 109 and in V_match.

**V_match** (Battery 84) is V_auto, unchanged, plus a match-state-conditioned gate and an adaptive probability map.
Both were designed after the remaining text and code gaps to the learners had been observed, and V_match was frozen
before it scored any benchmark label. The gate adds to the top-level mixture a fixed-share mixture (share 0.01) of the
same experts with a separate weight vector for each of five match states: no copy proposal, or a longest match of
3–4, 5–8, 9–16 or 17–32 bytes. The map re-estimates the probability p of a proposed byte from hit counts kept in 24
bins of ln(p/(1 − p)) for each match-length bucket; the byte receives the average of p and the bin's hit rate, and
the other bytes are rescaled. Two implementation details are kept as frozen: the effective top-level switching rate
is 0.0125 rather than 0.01, and the map is the identity only at bin centres.

**Earlier results.** V_base, V_auto and V_match are below the published minimum on 17, 20 and 22 of the 26 labels;
all three were designed using this suite. Battery 87 fixed the eight earlier sources of the main text before any
byte was downloaded (Hebrew and German Wikipedia, Wikimedia Foundation, 2026; Go source code, The Go Authors, 2026; Fashion-MNIST, Xiao
et al., 2017; ELF executables; the UCI Adult CSV table, Becker and Kohavi, 1996; 16-bit yes/no speech, OpenSLR, 2026;
and Python HTML documentation, Python Software Foundation, 2026; 256 windows each); there V_match was lower than E24 on 6
and V_base on 3. paq8px is lower than V_match on 29 of 34 row sets (Battery 88). Batteries 78 and 79 used LibriSpeech (Panayotov et
al., 2015).

**Table B1.** *Earlier batteries and their frozen predictions (protocol hashes in Appendix F.0). Declared amendments and post-hoc analyses within these batteries are not listed.*

| Battery | Content | Frozen predictions |
|---|---|---|
| 75 | Reproduction; V_base and released checkpoints at the published minima; MusicNet | A1, A2, B1, C1, C2, D1, D2 held; C3 failed |
| 76 | V_struct | S1, S2 held; S3, S4 failed |
| 77 | V_auto | G1, G2 held; G3 failed |
| 78 | Standard compressors, V_base and V_auto on LibriSpeech chunks | F1, L1, L2 held; L3 failed |
| 79 | Two open 7B language models on LibriSpeech | H1, H2 held |
| 80 | Per-position comparison of V_base and V_auto with the evaluated ensembles, and of language models on LibriSpeech | A2 held; A1, A3, B1 failed |
| 81 | V_ctx: V_auto plus k-byte context counts, k = 2, 3, 4, 6 | K1, K3 held; K2 failed |
| 82 | Released learners' loss and entropy by position, five sizes, seed 0 | L1, L2 held; L3 failed |
| 83 | Remaining lead of the ensembles over V_auto | C1, C2 held; B1, B2 numerical predicates met, but the original part-B gate (V_auto parity within 1e-9) failed on all 3 labels (6.42e-9 to 7.54e-9), so B1 and B2 are descriptive readouts with a separate storage-precision check; A2 held but uninformative (protocol design error); A1 failed |
| 84 | V_match | M1, M2, M4 held; M3 failed |
| 85 | V_word: V_match plus two word-context experts | W3 held; W1, W2 failed |
| 86 | Online mixture of each evaluated ensemble with V_match | X2 held; X1, X3 failed |
| 87 | Eight sources fixed before download; learner E24 | H2, H3, H4 held; H1 failed |

## Appendix C. Scaling-fit checks

Battery 91 asked whether the published scaling trend supports a forecast of the self-play compute at which the
learners would reach paq8px's archive rate P (Battery 88, full files). It used saved data under a protocol frozen
before any fit.

**Data and fits.** For each label we built the published compute frontier with the authors' `compute_frontier`
(default options) from their `frontier_traj_perk.json`, with their compute proxy C = K × N × 1536 × 4096 ×
(round + 1). The frontier uses six rungs, 100k to 24M parameters, so the five smaller sizes, including N = 65,728 at
the 100k rung, enter the fit. With the authors' helper functions we fitted our no-floor power-law diagnostic,
loss = A·C^(−α) in log space, and the floor-form procedure used in the authors' Figure 1 and Table 2,
loss = E + A·C^(−α). The protocol text gave the range as 500k to 24M and wrongly called the no-floor form the
paper's Figure 1 law.

**Held-out rung.** Both forms were fitted without the 24M rung and used to predict the minimum loss of the 24M part
of the full frontier. Four labels (protein, astronomy, DNA and KoLMogorov DNA) have no such points, leaving 22 of 26
evaluable. The protocol's and the runner's definitions of the 24M part select 15 and 9 points on arithmetic but give
identical targets on every evaluable label. For our no-floor diagnostic, prediction minus observation has median
−0.436 bits per byte (range −0.71 to −0.04) and is negative on 22 of 22: it predicts lower loss than observed. For the
floor form the median is −0.199; it is within 0.10 on 6 of 22, negative on 13 and positive on 9. E1, that the
no-floor fit would be within 0.10 on at least 13 of 26 labels, failed: 1 of 26 planned, 22 evaluable.

**Crossings.** With fits to the full frontier, on the 24 labels where P is below the published minimum, G1 predicted
that the no-floor fit reaches P only beyond 100 times the largest frontier compute Cmax on at least 13. It failed: 2
of 24. The no-floor curve crosses P below Cmax on float32 atlas (0.4318 Cmax) and astronomy (0.3425 Cmax), although
the observed frontier stays above P there. G2, that the fitted floor is at or above P on at least 12, held: 13 of 24.
On five of these (DNA, KoLMogorov DNA, ESC-50 at 11 kHz and both Speech Commands labels) the floor lies above losses
already observed, so these floors do not establish a barrier.

**Reading.** Because E1 failed, we report no compute multiple, as fixed in advance. These checks do not validate a
compressor-crossing compute forecast. They do not refute observed transfer or the observed fall in loss with
self-play compute.

## Appendix D. Setup details

**Compressor accounting.** paq8px (commit c84f576) is run at level 8 with default options. The logged value is the
nominal log loss of the main predictor, before the arithmetic coder's clamping and integer rounding, so it is not
exactly the physical coder bits. On the 6,374 retained windows of the original benchmark in standard mode, file size
minus all logged bits (main predictor plus the separately coded metadata) is 63.04 to 71.96 bits per window (mean
67.48); the metadata alone average 63.06 bits. A window is retained when the main-predictor byte sequence equals the
raw window in length, values and order. The flags used with block detection disabled are `-forcetext` for seven text,
code and formal labels and the four new text-like sources, and `-forcebinary` for rank-coded web text and all other
sets. The mode identity covers 2,042 common windows on the eight text, code and formal labels; for Gutenberg only 2
standard-mode windows are retained, so there the identity rests on 2 rows. The row sets whose logged log losses differ
between modes are protein, both CIFAR-10 layouts, both ESC-50 and both Speech Commands rates, and ELF (170 of 256
standard-mode windows retained).

**bGPT extraction.** The released checkpoints were pretrained on Wikipedia text, 32 × 32 ImageNet images as BMP files
and one-second 8 kHz 8-bit LibriSpeech WAV files, including their headers and subject to context-length cropping.
bGPT predicts bytes in 16-byte patches with a context of 512 patches (8,192 bytes). As in the released code, we
prepend a file-extension patch; each byte is conditioned on all earlier patches and the earlier bytes of its own
patch, and we drop the end-of-patch token and renormalize over the 256 byte values. The domain weights were assigned
before the low-overhead recomputation but after an earlier three-variant bGPT analysis had been seen.

**Protocol history.** The original gate implementations were not uniformly fail-closed: one acquisition amendment
followed a printed row (Battery 102's fixed-prior comparison, part B), one gate hardening followed the outcomes (the
new-source battery), and one array-shape gate was corrected after the outcomes were printed (Batteries 110 and 111,
reported as amended, descriptive analyses); the completed inputs passed stronger independent checks (Appendix F.2).
The LibriSpeech battery in Appendix F resamples its 200 utterances rather than windows.

**Table D1.** *Coverage of the main analyses (earlier diagnostics are in Appendix F). "Benchmark" = the 26 published labels; "earlier sources" = eight sources added in an earlier blind test; "new sources" = six sources fixed before download; "further sources" = six more, fixed before download for Battery 117. Retained rows per row set are in Appendices F and G.*

| Analysis (battery) | Learners | Row sets | paq8px mode |
|---|---|---|---|
| Calibration (88) | published minima and evaluated ensembles (26 benchmark); E24 (8 earlier) | 26 benchmark + 8 earlier | archive, standard |
| Benchmark-wide G (98, 100) | evaluated ensembles; E24 on earlier sources | 34 | standard |
| Size sweep (101) | 8 seeds and their ensemble, six sizes, round 8191 | 3 text/formal + 4 image/audio labels | standard |
| Round sweep (102 A) | 24M eight-seed ensemble, eight rounds | 2 text/formal + 4 image/audio labels | standard |
| Fixed prior (102 B) | four-seed ensembles of both arms, 3M and 6M, round 8191 | 2 text/formal + 4 image/audio labels | standard |
| Static mixture (105) | evaluated ensembles; E24 on earlier sources; bGPT on 24 domain row sets | 34 (certificate on the 8 text/code/formal) | standard |
| lpaq1 reference (104) | evaluated ensembles; E24 | 34 | lpaq1 (sequential) |
| New sources (106) | E24; evaluated ensembles for the mode comparison | 6 new sources, 256 windows each (standard-mode Gutenberg retains 2); 8 benchmark text/code/formal labels | forced and standard |
| Natural-data model (99) | bGPT, all three released weights | 34 | not applicable (reference: mixture of V_auto and V_match) |
| Natural-data model (100) | bGPT, preassigned domain weights | 24 row sets with a domain | standard |
| Natural-data model (106) | bGPT, preassigned domain weights | 6 new sources | forced and standard |
| Image analyses (107-109) | evaluated ensembles; E24 | CIFAR-10 (two layouts), Fashion-MNIST, KMNIST | standard |
| Curriculum (110, amended) | 1M, eight seeds, six generator endpoints, round 4095 | 8 text/code/formal + 4 image/audio labels | standard |
| Reward arms (111, amended) | 1M, four seeds (three for one arm), seven arms, round 8191 | same 12 labels | standard |
| Calibrated members (112) | eight seeds, six sizes, round 8191, online temperature calibration | 3 text/formal + 4 image/audio labels | standard |
| Gain location (113) | evaluated ensembles | 8 benchmark text/code/formal labels | standard; lpaq1 |
| paq8px suppressions (114) | evaluated ensembles | same 8 labels | standard; 29 variants including intact paq8px |
| lpaq1 variants (115, 116) | evaluated ensembles; E24 | same 8 labels + 4 new text sources of Battery 106 | lpaq1 and its variants |
| Frozen lpaq1 variant (117) | E24 | 6 further sources | standard (Gutenberg retains 1); lpaq1 and frozen variant |

## Appendix E. Self-play and fixed-prior ensembles

**Table E1.** *Four-seed ensembles at round 8191: own loss and realized gain G beyond paq8px (s = 0.001), bits per byte.*

| Row set | Size | Self-play loss | Fixed-prior loss | Loss gap | G, self-play | G, fixed prior |
|---|---|---:|---:|---:|---:|---:|
| CIFAR-10 (HWC) | 3M | 5.591 | 7.479 | 1.887 | +0.00350 | −0.00092 |
| CIFAR-10 (planar) | 3M | 6.032 | 7.490 | 1.458 | +0.00307 | −0.00093 |
| MusicNet | 3M | 2.476 | 4.530 | 2.054 | +0.00466 | −0.00093 |
| 8-bit audio | 3M | 2.380 | 3.400 | 1.020 | +0.00303 | +0.00029 |
| Metamath | 3M | 3.260 | 7.107 | 3.848 | −0.00092 | −0.00097 |
| Web text (raw) | 3M | 5.043 | 7.278 | 2.236 | −0.00096 | −0.00096 |
| CIFAR-10 (HWC) | 6M | 5.354 | 7.786 | 2.432 | +0.00668 | −0.00094 |
| CIFAR-10 (planar) | 6M | 5.996 | 7.803 | 1.807 | +0.00150 | −0.00090 |
| MusicNet | 6M | 2.255 | 7.789 | 5.535 | +0.00366 | −0.00097 |
| 8-bit audio | 6M | 2.330 | 4.028 | 1.698 | +0.00256 | +0.00028 |
| Metamath | 6M | 3.218 | 7.384 | 4.166 | −0.00094 | −0.00097 |
| Web text (raw) | 6M | 5.223 | 7.760 | 2.537 | −0.00096 | −0.00096 |


## Appendix F. Protocols, criteria, amendments and moved details

**F.0 Summary.** The rewrite-stage batteries used in Sections 3.1 to 3.5 (Batteries 88 to 112; earlier batteries
behind V_base, V_auto and V_match are listed in Appendix B) contain 84 prespecified numerical criterion families: 52
met their numerical predicates, 25 failed, and 7 (Batteries 110 and 111) are reported separately as amended,
descriptive outcomes. Battery 90 is descriptive only. The 25 are failed numerical criterion families on the recorded,
explicitly qualified analyses; the 52 are not 52 unqualified, fully protocol-compliant or independent confirmations,
because several batteries reuse exposed data and some carry the gate, seed or implementation deviations listed in
F.2. Numerical outcomes (F.1) and gate or admission status (F.2) are recorded separately. Batteries 113 to 117 (Appendix G)
add 17 numerical criterion families, 8 met and 9 failed, bringing the total to 101: 60 met, 34 failed and 7 amended;
their gates (Battery 114 S0, Battery 115 G0) are counted separately. Protocol files and the first 16 hex digits of their SHA-256 hashes, recorded in the project log (Appendix H) before
scoring
(Batteries 75 to 87 are the earlier batteries of Appendix B):

| Battery | Protocol | SHA-256 (prefix) |
|---|---|---|
| 75  |  PROTOCOL\_B75\_frontier\_rescore.md  |  7f73b4cef5e85a04 |
| 76  |  PROTOCOL\_B76\_structured.md  |  d6c9e4b749f8f383 |
| 77  |  PROTOCOL\_B77\_auto\_geometry.md  |  c18c78dc72260a05 |
| 78  |  PROTOCOL\_B78\_librispeech.md  |  f5707b998008740a |
| 79  |  PROTOCOL\_B79\_llm\_bits.md  |  812670e1d3254ae7 |
| 80  |  PROTOCOL\_B80\_advantage\_map.md  |  95849665f72d5861 |
| 81  |  PROTOCOL\_B81\_context.md  |  aac6e353b28782cc |
| 82  |  PROTOCOL\_B82\_learner\_positions.md  |  0d86db3e5e2089e8 |
| 83  |  PROTOCOL\_B83\_decompose\_lead.md  |  049b29e8edd97c25 |
| 84  |  PROTOCOL\_B84\_match\_model.md  |  6069bf64640c499e |
| 85  |  PROTOCOL\_B85\_word\_model.md  |  0c4f085f661a3860 |
| 86  |  PROTOCOL\_B86\_combination.md  |  ba3d035ca5e498a6 |
| 87  |  PROTOCOL\_B87\_heldout\_sources.md  |  25e55cf48d53c620 |
| 88  |  PROTOCOL\_B88\_strong\_compressor.md  |  83bf3bbb0e68c720 |
| 89  |  PROTOCOL\_B89\_paq\_librispeech.md  |  cdf764bde0c78de2 |
| 90  |  PROTOCOL\_B90\_timing.md  |  a88c0e58a134babe |
| 91  |  PROTOCOL\_B91\_scaling\_gap.md  |  bbe8d6dbb11a663a |
| 92  |  PROTOCOL\_B92\_enwik9.md  |  0a558b59a2f88241 |
| 93  |  PROTOCOL\_B93\_scale\_complementarity.md  |  4cdd875a06e93ece |
| 94  |  PROTOCOL\_B94\_what\_grows\_the\_signal.md  |  bf3261a1787a0f4f |
| 95  |  PROTOCOL\_B95\_calibration\_vs\_knowledge.md  |  67265fa68d48c727 |
| 96  |  PROTOCOL\_B96\_sharpen\_signal.md  |  e33c43caf46cdfff |
| 97  |  PROTOCOL\_B97\_size\_seed\_temperature\_grid.md  |  aff77ab4098368cd |
| 98  |  PROTOCOL\_B98\_paq\_per\_byte.md  |  487dd86c0db8b7bc |
| 99  |  PROTOCOL\_B99\_natural\_data\_yardstick.md  |  0810fce3b2d9031d |
| 100  |  PROTOCOL\_B100\_low\_overhead\_combiners.md  |  4296842653ab5464 |
| 101  |  PROTOCOL\_B101\_gain\_beyond\_paq\_by\_size.md  |  0221ec2fe7ac9398 |
| 102  |  PROTOCOL\_B102\_compute\_axis\_and\_fixed\_prior.md  |  64c46f385a97a56c |
| 103  |  PROTOCOL\_B103\_in\_domain.md  |  259b2d0838c258ab |
| 104  |  PROTOCOL\_B104\_peeling\_ladder.md  |  1aa4fa028c90c79a |
| 105  |  PROTOCOL\_B105\_oracle\_mixture.md  |  b7ec39bbee6f01fc |
| 106  |  PROTOCOL\_B106\_prospective\_sources.md  |  0ab49e7bf2fa4c0d |
| 107  |  PROTOCOL\_B107\_where\_image\_gain\_lives.md  |  32b17ae30e97077c |
| 108  |  PROTOCOL\_B108\_hedging\_vs\_knowledge.md  |  2c29fe7efb0997f5 |
| 109  |  PROTOCOL\_B109\_is\_the\_image\_residual\_special.md  |  2134f8405b3a208b |
| 110  |  PROTOCOL\_B110\_curriculum\_beyond\_paq.md  |  db4a8b673198a549 |
| 111  |  PROTOCOL\_B111\_reward\_arms\_beyond\_paq.md  |  4e75f1432548803c |
| 112  |  PROTOCOL\_B112\_calibrated\_beyond\_paq.md  |  4bf3620944a58f3a |

**F.1 Criterion inventory.** Definitions are transcribed from the frozen protocols; interpretive sentences in those
protocols are not endorsed here. Measures differ between batteries; in particular, the G of Batteries 93 to 97 is
not the paper's default gain beyond paq8px. Legend (M is the fixed-share mixture of the named experts; V is V_match):

- Batteries 93, 94 (T2), 96 (S3) and 97: G = V − M(learner, V), the gain beyond V_match at share 0.01.
- Batteries 94 (T3) and 96 (S1, S2): G_both = M(V_auto, V_match) − M(learner, V_auto, V_match), what the learners add
  beyond both hand-built predictors, share 0.01; g is its per-byte value.
- Battery 94 (T1): X = M(early, V_match) − M(early, late, V_match), what a late-round checkpoint adds to an early one.
- Battery 95: F = M(u, V) − M(learner, u, V) with u the uniform distribution (the gain with a probability floor);
  R = (F_8 − F_1)/(G_8 − G_1) per label with G_8 − G_1 > 0.005; subscripts 1 and 8 are single seeds and eight-seed
  ensembles.
- Battery 96 (S2): r_close (r_open) = mean g on closing (opening) delimiters ) ] } (( [ {) divided by mean g on all
  bytes; depth is the running bracket count within the window.
- Groups (Batteries 94 and 98): F = formal and symbolic (Metamath, C, Python, arXiv mathematics, melody); N = natural
  text; W = raw waveforms; I = images; O = other.
- Battery 98 also reports G_both as defined above, for comparison. Battery 99: G_selfplay = M(V_auto, V_match) −
  M(ensemble, V_auto, V_match) and G_bgpt likewise with bGPT in place of the ensemble (share 0.01); its Y1 and Y2
  use these quantities, not the gain beyond paq8px.
- Otherwise, from Battery 98 onward: G_paq = G beyond paq8px as defined in Section 2 (share stated per battery).

Numerical predicate outcomes are separate from admission/gate status. B94/B95 need the documented gate/seed qualifications. B110/B111 are amended/descriptive. Definitions are transcribed from frozen protocols; historical interpretation claims in those protocols are not endorsed.

**Battery 88.**

**Q1: PASS.** paq8px is below the published minimum on at least 18 of 26 labels.
Observed: {"count": 24}.
Population: 26 labels/row sets. Rule: count >= 18.

**Q2: PASS.** paq8px is lower than E24 (Battery 87) on at least 6 of 8 new sources.
Observed: {"count": 8}.
Population: 8 labels/row sets. Rule: count >= 6.

**Q3: PASS.** paq8px is lower than V_match on at least 17 of the 34 row sets.
Observed: {"count": 29}.
Population: 34 labels/row sets. Rule: count >= 17.

**Battery 89.**

**R1: PASS.** paq8px is below FLAC (30.6%).
Observed: {"paq_adjusted_percent": 21.2682861328125, "flac_header_once": 30.6063720703125}.
Population: same 2,000 chunks, 200 utterances; reference-adjusted primary. Rule: paq < each stated reference.

**R2: PASS.** paq8px is below V_base with all 8 bits (25.9%).
Observed: {"paq_adjusted_percent": 21.2682861328125, "V_base_full8": 25.886579755337515}.
Population: same 2,000 chunks, 200 utterances; reference-adjusted primary. Rule: paq < each stated reference.

**R3: PASS.** paq8px is below both open 7B language models with all 8 bits (Mistral-7B 34.7%, Qwen2.5-7B 28.9%).
Observed: {"paq_adjusted_percent": 21.2682861328125, "mistral_full8": 34.70989951703437, "qwen_full8": 28.90041152586936}.
Population: same 2,000 chunks, 200 utterances; reference-adjusted primary. Rule: paq < each stated reference.

**Battery 91.**

**E1: FAIL.** the pure power law fitted without the 24M rung predicts the 24M part of the frontier (its minimum loss) within 0.10 bits per byte on at least 13 of 26 labels.
Observed: {"count": 1, "need": 13, "planned_denominator": 26, "evaluable": 22}.
Population: 22 evaluable of 26 planned labels. Rule: count >= 13.

**G1: FAIL.** under the pure power law fitted to the full frontier, reaching paq8px requires more than 100 x Cmax on at least 13 of the 24 labels where paq8px is below the published minimum.
Observed: {"count": 2, "need": 13, "planned_denominator": 24, "evaluable": 24}.
Population: 24 favourable labels. Rule: count >= 13.

**G2: PASS.** under the floor law fitted to the full frontier, the fitted floor E is at or above P on at least 12 of those 24.
Observed: {"count": 13, "need": 12, "planned_denominator": 24, "evaluable": 24}.
Population: 24 favourable labels. Rule: count >= 12.

**Battery 92.**

**T1: PASS.** gzip is within 1.5 points of the published 48.1%.
Observed: {"gzip_full_percent": 49.221435546875, "difference_percentage_points": 1.1214355468749992}.
Population: 2,000 chunks; sanity criterion. Rule: absolute difference from 48.1% <= 1.5 percentage points.

**T2: PASS.** paq8px (full files) is above both Llama 2 7B (8.9%) and Chinchilla 70B (8.3%).
Observed: {"paq_full_percent": 38.7243896484375, "published_percent": [8.9, 8.3]}.
Population: 2,000 chunks; two unpaired published references. Rule: paq > both references.

**T3: PASS.** paq8px (full files) is above the enwik8-trained Transformer 3.2M (17.0%).
Observed: {"paq_full_percent": 38.7243896484375, "published_percent": 17}.
Population: 2,000 chunks; one unpaired published reference. Rule: paq > 17%.

**Battery 93.**

**P1: PASS.** G(24M) - G(100k) > 0 on at least 6 of the 8 S labels.
Observed: {"count": 8, "need": 6, "pass": true}.
Population: 8 size-comparison labels. Rule: count >= 6.

**P3: PASS.** at positions 0-15, E(24M) < E(100k) on at least 6 of the 8 S labels (a better prior at the start of a window, where no in-window statistics exist yet).
Observed: {"count": 6, "need": 6, "pass": true}.
Population: 8 size-comparison labels. Rule: count >= 6.

**P4: FAIL.** at positions 0-15, E(24M) < V on at least 6 of the 8 S labels.
Observed: {"count": 3, "need": 6, "pass": false}.
Population: 8 size-comparison labels. Rule: count >= 6.

**P5: FAIL.** G(24M) - G(100k) is larger on positions 256-4094 than on positions 0-15 on at least 5 of 8 labels (growth mostly where context exists).
Observed: {"count": 3, "need": 5, "pass": false}.
Population: 8 size-comparison labels. Rule: count >= 5.

**P2: FAIL.** in L, Spearman correlation between size and G is at least 0.8 on both MusicNet labels.
Observed: {"musicnet_pcm8": 0.6571428571428573, "musicnet_pcm8_11khz": 0.6571428571428573}.
Population: 2 MusicNet labels, six sizes, one seed. Rule: both Spearman >= 0.8.

**Battery 94.**

**Q1: FAIL.** X >= 0.005 on at least 3 of the 5 labels.
Observed: {"count": 1, "need": 3}.
Population: 5 labels. Rule: count >= 3.

**Q2a: PASS.** G_8 > G_1 on at least 22 of 26 labels.
Observed: {"count": 25, "of": 26, "need": 22}.
Population: 26 labels. Rule: count >= 22.

**Q3b: PASS.** G_both > 0.02 on at least 4 of the 5 F labels.
Observed: {"count": 5, "need": 4}.
Population: 5 labels. Rule: count >= 4.

**Q2b: PASS.** the median over labels of G_8 - G_1 is at least 0.01 bits per byte.
Observed: {"median_G8_minus_G1": 0.024183470619999134, "need": 0.01}.
Population: 26 labels. Rule: median gain difference >= 0.01.

**Q3a: PASS.** median G_both over F exceeds the median over W by at least 0.03 bits per byte.
Observed: {"F_minus_W": 0.05651438789616886, "need": 0.03}.
Population: 5 formal/symbolic versus 8 waveform labels. Rule: difference between group medians >= 0.03.

**Q3c: FAIL.** G_both < 0.05 on both image labels (the image gain relative to V_match is mostly structure V_auto has).
Observed: {"cifar10_rgb_hwc": 0.19609271794345096, "cifar10_rgb_planar": 0.06652226065541056}.
Population: 2 CIFAR layouts. Rule: both gains < 0.05.

**Battery 95.**

**C1: PASS.** the median of R over eligible labels is at least 0.5 (most of the seed effect is not near-zero overconfidence).
Observed: {"median_R": 0.9334311914479091, "n": 23, "need": 0.5}.
Population: 23 eligible labels. Rule: median ratio >= 0.5.

**C2: PASS.** F_8 > F_1 on at least 22 of 26 labels.
Observed: {"count": 25, "need": 22}.
Population: 26 labels. Rule: count >= 22.

**C3: PASS.** the median over labels of the share of the first-seed-to-ensemble gain from bytes with p_s0(true) < 0.01 is below 0.5.
Observed: {"median_low_share": 0.2776668650390183, "n": 25, "need_below": 0.5}.
Population: 25 labels; arithmetic excluded for nonpositive total gain. Rule: median signed low-mask contribution ratio < 0.5.

**Battery 96.**

**S1a: PASS.** min(G_both of go_source, python_docs_html) > max(G_both of hewiki, dewiki).
Observed: {"code_min": 0.06525237092663795, "text_max": 0.029013239507751757}.
Population: 2 code/markup vs 2 natural-text sources. Rule: code minimum > natural-text maximum.

**S1b: PASS.** mean G_both over code/markup minus G_both of yesno_pcm16 >= 0.03 bits per byte.
Observed: {"diff": 0.10995609993282465, "pass": true}.
Population: 2 code/markup sources versus yesno waveform. Rule: mean code gain minus waveform gain >= 0.03.

**S1c: PASS.** G_both of fashion_mnist > 0.02.
Observed: {"fashion_mnist": 0.3077293793199475, "pass": true}.
Population: Fashion-MNIST. Rule: gain > 0.02.

**S2a: FAIL.** r_close >= 2 on at least 3 of the 5 labels.
Observed: {"count": 1, "need": 3, "pass": false}.
Population: 5 formal/code labels. Rule: count >= 3.

**S2b: PASS.** mean g on closing bytes with depth before >= 2 exceeds that with depth before = 1 on at least 3 of 5.
Observed: {"count": 4, "need": 3, "pass": true}.
Population: 5 formal/code labels. Rule: count >= 3.

**S2c: PASS.** r_close > r_open on at least 3 of 5.
Observed: {"count": 3, "need": 3, "pass": true}.
Population: 5 formal/code labels. Rule: count >= 3.

**S3a: FAIL.** G(8) - G(4) >= G(4) - G(2) on at least half of the eligible labels (no diminishing return in log k within 1..8).
Observed: {"count": 8, "eligible": 17, "pass": false}.
Population: 17 eligible of 26 labels. Rule: at least half of eligible labels, i.e. >= 9/17.

**Battery 97.**

**D1: PASS.** Spearman correlation between size and G_8 >= 0.8 on at least 5 of 7 labels.
Observed: {"spearman": {"metamath": 1.0, "aitdcc_b_c_source": 1.0, "dclm_ranked": 0.8857142857142858, "cifar10_rgb_hwc": 0.942857142857143, "mutopia_melody_16th": 0.8285714285714287, "musicnet_pcm8": 1.0, "audio_8bit": 0.942857142857143}, "count": 7, "need": 5}.
Population: 7 labels, six sizes. Rule: Spearman >= 0.8 on >= 5/7 labels.

**D2: PASS.** G_8(3M) > G_1(24M) on at least 4 of 7 labels (8 x 3M = 24M parameters; the authors' compute proxy counts ensemble members).
Observed: {"G8_3M_minus_G1_24M": {"metamath": 0.0566634165103887, "aitdcc_b_c_source": 0.023234575678947655, "dclm_ranked": 0.020584835799140333, "cifar10_rgb_hwc": -0.009491725300211695, "mutopia_melody_16th": 0.04412039289907002, "musicnet_pcm8": -0.0010609359848533784, "audio_8bit": 0.0049068120564587925}, "count": 5, "need": 4}.
Population: 7 labels. Rule: G8(3M) > mean G1(24M) on >= 4/7 labels.

**D3: PASS.** share = (G_1cal - G_1) / (G_8 - G_1), where G_1cal uses p_cal. The median share over labels with G_8 - G_1 > 0.005 is below 0.5 (temperature calibration explains less than half of the seed effect).
Observed: {"share": {"metamath": -0.04694572134478872, "aitdcc_b_c_source": -0.05952497950115091, "dclm_ranked": -0.03586121985779623, "cifar10_rgb_hwc": -0.010619262259377918, "mutopia_melody_16th": -0.03157945462610317, "musicnet_pcm8": -0.15603820567471766, "audio_8bit": -0.05078737579833638}, "median": -0.04694572134478872}.
Population: 7 eligible labels. Rule: median operational calibration share < 0.5.

**Battery 98.**

**R1: FAIL.** G_paq > 0.01 bits per byte on at least 8 of 26 labels.
Observed: {"count": 1, "need": 8}.
Population: 26 benchmark labels. Rule: count >= 8.

**R3: PASS.** G_paq <= G_both on at least 22 of 26 labels (paq8px leaves less for the learners to add than our two predictors).
Observed: {"count": 24, "need": 22}.
Population: 26 benchmark labels. Rule: count >= 22.

**R2: FAIL.** the median G_paq over group F exceeds the median over group W by more than 0.005.
Observed: {"F_minus_W": -0.0064589977579808736, "need": 0.005}.
Population: 5 formal/symbolic versus 8 waveform labels. Rule: difference between group medians > 0.005.

**Battery 99.**

**Y1: FAIL.** on the four natural-text labels (dclm, dclm_ranked, llm_compression_cc, kolmogorov_text) G_bgpt_text is at least 10 times G_selfplay on all four.
Observed: {"count": 3, "need": 4}.
Population: 4 designated text labels; ranked DCLM grouping error preserved. Rule: all four bGPT-text gains >= 10 times self-play gain.

**Y2: PASS.** the median ratio over structured sources {elf_x86_64, uci_adult, cifar10_rgb_hwc, cifar10_rgb_planar, fashion_mnist} exceeds the median ratio over natural text {the four text labels, hewiki, dewiki}.
Observed: {"median_ratio_structured": 0.44925008887851464, "median_ratio_natural_text": 0.017575134018775546, "pass": true}.
Population: 5/5 structured and 5/6 natural-text eligible; ranked DCLM excluded by G_bgpt_best > 0.01. Rule: structured median ratio > natural-text median ratio.

**Battery 100.**

**L1: FAIL.** for the learners with s = 0.001, G_paq > 0.005 on at most 5 of the 26 benchmark labels.
Observed: {"count": 7, "at_most": 5}.
Population: 26 benchmark labels. Rule: no more than 5 gains > 0.005 at share0.001.

**L2: PASS.** for the learners with s = 0, G_paq <= 0.001 on at least 18 of the 26 benchmark labels.
Observed: {"count": 25, "need": 18}.
Population: 26 benchmark labels. Rule: at least 18 gains <= 0.001 under corrected exact Bayes.

**L3: FAIL.** on every row set with a bGPT domain, G_paq(bGPT, 0.001) exceeds G_paq(learners, 0.001), and by at least 0.1 bits per byte on at least 15 of the 24 such row sets.
Observed: {"all_exceed": false, "count_ge_0.1": 17, "n_domain": 24, "need": 15, "strict_advantages": 19, "advantages_at_least_0.1": 17}.
Population: 24 assigned-domain row sets. Rule: strict superiority on all24 AND advantage >= 0.1 on at least15.

**Battery 101.**

**Z1: PASS.** on metamath, aitdcc_b_c_source and dclm_ranked, G_paq <= 0.002 at every one of the 6 sizes (18 cells).
Observed: {"max": 0.00030664296312577833, "count_le_0.002": 18, "cells": 18}.
Population: 3 text/formal labels x6 sizes =18 ensemble cells. Rule: all gains <= 0.002.

**Z2: PASS.** on cifar10_rgb_hwc, G_paq at 24M exceeds G_paq at 100k by at least 0.005, and the Spearman correlation between size and G_paq is at least 0.8.
Observed: {"diff_24M_100k": 0.014842434041547564, "spearman": 0.942857142857143}.
Population: HWC at6 sizes. Rule: endpoint difference >= 0.005 AND Spearman >= 0.8.

**Z3: PASS.** on musicnet_pcm8 and audio_8bit, G_paq at 24M exceeds G_paq at 100k (both labels).
Observed: {"musicnet_pcm8": 0.004544534610712943, "audio_8bit": 0.002047378480220241}.
Population: 2 audio labels. Rule: both 24M-minus100k gains > 0.

**Battery 102.**

**A1: PASS.** on cifar10_rgb_hwc, Spearman(round, G_paq) >= 0.8 over rounds 256..8191 (8 seeds).
Observed: {"spearman": 0.8928571428571429, "pass": true}.
Population: HWC at7 nonzero sampled rounds256..8191. Rule: Spearman >= 0.8.

**A2: PASS.** on metamath and dclm, G_paq <= 0.002 at every round, 0..8191 (16 cells).
Observed: {"max": -0.0008504844636632459, "count_le": 16, "pass": true}.
Population: 2 text/formal labels x8 sampled rounds =16 cells. Rule: all gains <= 0.002.

**A3: PASS.** on musicnet_pcm8 and audio_8bit, G_paq at round 8191 exceeds G_paq at round 256 (both labels).
Observed: {"musicnet_pcm8": 0.005459706074549889, "audio_8bit": 0.0017450993664266526, "pass": true}.
Population: 2 audio labels. Rule: both specified gain differences > 0.

**B1: PASS.** on cifar10_rgb_hwc, G_paq of the self-play 4-seed average exceeds that of the fixed-prior 4-seed average at both 3M and 6M.
Observed: {"3M": 0.004416353731895362, "6M": 0.0076170742296170196, "pass": true}.
Population: HWC at3M and6M. Rule: both specified gain differences > 0.

**B2: PASS.** at 6M, the self-play 4-seed average has lower own loss E than the fixed-prior average on at least 4 of the 6 labels.
Observed: {"count": 6, "need": 4, "pass": true}.
Population: 6 labels at6M. Rule: own-loss superiority on >= 4/6 labels.

**Battery 103.**

**H1: FAIL.** the self-play 24M ensemble's own loss is below paq8px by at least 0.3 bits per byte.
Observed: {"E_minus_paq_24M": 0.05107703738410971, "pass": false}.
Population: 256 local-surrogate windows. Rule: learner minus paq loss <= -0.3.

**H2: FAIL.** G_paq of the self-play 24M ensemble is at least 0.1 bits per byte (versus about zero on natural text, Battery 101).
Observed: {"G_paq_24M": 0.01526605282594799, "pass": false}.
Population: same256 local-surrogate windows. Rule: gain >= 0.1.

**H3: FAIL.** the fixed-prior 6M ensemble has lower own loss than the self-play 6M ensemble on these uniform-prior outputs.
Observed: {"uniform_minus_selfplay_6M": 2.641696159378529, "pass": false}.
Population: same256 local-surrogate windows. Rule: fixed-prior minus self-play own loss < 0.

**Battery 104.**

**P1: FAIL.** G_L5 <= 0.002 on at least 6 of the 8 T labels.
Observed: {"count": 0, "need": 6}.
Population: 8 labels. Rule: count >= 6.

**P2: PASS.** G_L1 > 0.02 on at least 6 of the 8 T labels.
Observed: {"count": 8, "need": 6}.
Population: 8 labels. Rule: count >= 6.

**P3: FAIL.** the lowest level with G_L <= 0.002 is at or below L4 (word context not needed) for at least 5 of the 8 T labels.
Observed: {"count": 0, "need": 5}.
Population: 8 labels. Rule: count >= 5.

**Battery 105.**

**O1: PASS.** learners' corpus oracle O_c <= 0.002 on at least 6 of the 8 T labels.
Observed: {"count": 8, "need": 6}.
Population: 8 labels. Rule: count >= 6.

**O2: PASS.** learners' window oracle O_w <= 0.005 on at least 6 of the 8 T labels.
Observed: {"count": 8, "need": 6}.
Population: 8 labels. Rule: count >= 6.

**O3: PASS.** bGPT's corpus oracle exceeds the learners' on every one of the 7 T labels that have a bGPT domain.
Observed: {"count": 7, "of": 7}.
Population: 7 labels. Rule: count >= 7.

**Battery 106.**

**N1: PASS.** learners' G beyond standard paq8px <= 0.002 on all four of sources 1-4.
Observed: {"gutenberg_en": -0.0009630117329404442, "rust_ripgrep": -0.000739653558126291, "js_lodash": -0.0009590081474207175, "json_countries": -0.0009405095043396344}.
Population: 4 sources; standard Gutenberg2 retained rows versus256 forced; others256. Rule: all4 learner gains <= 0.002.

**N2: PASS.** learners' G beyond paq8px without look-ahead <= 0.002 on all four of sources 1-4.
Observed: {"gutenberg_en": -0.0009631053758645588, "rust_ripgrep": -0.000739653558126291, "js_lodash": -0.0009590081474207175, "json_countries": -0.0009405095043396344}.
Population: 4 sources; standard Gutenberg2 retained rows versus256 forced; others256. Rule: all4 learner gains <= 0.002.

**N3: PASS.** bGPT text weights' G beyond standard paq8px >= 0.1 on gutenberg_en.
Observed: {"G_bgpt_std": 1.3024041687837065}.
Population: Gutenberg standard mode:2/256 retained windows. Rule: gain >= 0.1.

**N4: PASS.** learners' G beyond standard paq8px > 0.002 on at least one of kmnist_images and fsdd_audio.
Observed: {"kmnist_images": 0.008531902636661738, "fsdd_audio": 0.0018872399117360445}.
Population: 2 new image/audio sources,256rows each;1/2 exceeds threshold. Rule: gain > 0.002 on at least1 of2.

**S1: PASS.** on the 8 text/code/formal benchmark labels of Battery 104, learners' G beyond paq8px without look-ahead <= 0.002 on at least 6 of 8.
Observed: {"count": 8, "need": 6, "pass": true}.
Population: 8 old text/code/formal labels;2,042 windows. Rule: at least6/8 gains <= 0.002.

**Battery 107.**

**W1: FAIL.** on cifar10_rgb_hwc, mean g over A bytes is at least 2 times the mean g over O bytes.
Observed: {"A_over_O": 0.6191996984404581, "pass": false}.
Population: HWC signed class means. Rule: A/O ratio >= 2.

**W2: FAIL.** the share of total gain carried by A bytes exceeds the A share of bytes by a factor of at least 1.5 on at least 3 of the 4 image row sets.
Observed: {"count": 0, "need": 3, "pass": false}.
Population: 4 image row sets. Rule: count >= 3/4.

**W3: FAIL.** mean g over K bytes is below mean g over A bytes on at least 3 of the 4 row sets.
Observed: {"count": 2, "need": 3, "pass": false}.
Population: 4 image row sets. Rule: count >= 3/4.

**Battery 108.**

**K1: PASS.** G_learners > max(G_U, G_Z) on at least 3 of the 4 image row sets (the learners give more than flat or frequency hedging).
Observed: {"count": 4, "need": 3, "pass": true}.
Population: 4 image row sets. Rule: count >= 3/4.

**K2: FAIL.** at big-jump bytes, the median learner probability of the true byte exceeds 4/256 on at least 3 of the 4 sets (more specific than a flat hedge).
Observed: {"count": 0, "need": 3, "pass": false}.
Population: 4 image row sets. Rule: count >= 3/4.

**K3: FAIL.** at big-jump bytes, the median learner probability of the true byte exceeds the median paq8px probability on at least 3 of the 4 sets.
Observed: {"count": 0, "need": 3, "pass": false}.
Population: 4 image row sets. Rule: count >= 3/4.

**Battery 109.**

**R1: PASS.** G_V >= 0.5 G_L on at least 2 of the 3 sets (a hand-built online predictor realizes comparable gain).
Observed: {"count": 2, "need": 2, "pass": true}.
Population: 3 image row sets:2CIFAR layouts andFashion-MNIST. Rule: count >= 2/3.

**R2: PASS.** G_L|V <= 0.5 G_L on at least 2 of the 3 sets (at least half of the learners' residual is shared with V_auto).
Observed: {"count": 2, "need": 2, "pass": true}.
Population: 3 image row sets:2CIFAR layouts andFashion-MNIST. Rule: count >= 2/3.

**Battery 110.**

**C1: amended/descriptive.** G <= 0.002 in at least 46 of the 48 cells (6 arms x 8 T labels).
Observed: {"count": 48, "need": 46, "of": 48, "pass": true}.
Population: 48 arm-label cells. Rule: count >= 46.

**C4: amended/descriptive.** on at least 7 of the 8 T labels, max minus min of G over the six arms is <= 0.001.
Observed: {"count": 7, "need": 7, "pass": true}.
Population: 8 labels. Rule: count >= 7.

**C2: amended/descriptive.** on both CIFAR-10 layouts, G(T4096) > G(G0).
Observed: {"values": [true, true], "pass": true}.
Population: 2 layouts. Rule: both endpoint gains exceed G0.

**C3: amended/descriptive.** on cifar10_rgb_planar, Spearman(T, G) over the six arms (G0 as T = 0) >= 0.8.
Observed: {"spearman": 1.0, "pass": true}.
Population: planarCIFAR across6 arms. Rule: Spearman >= 0.8.

**Battery 111.**

**W1: amended/descriptive.** G <= 0.002 in at least 54 of the 56 cells (7 arms x 8 T labels).
Observed: {"count": 56, "need": 54, "of": 56, "pass": true}.
Population: 56 arm-label cells. Rule: count >=54.

**W2: amended/descriptive.** on both CIFAR-10 layouts, the canonical arm's G exceeds both the negate and the uniform arm's G (4 comparisons, all must hold).
Observed: {"values": [true, true, true, true], "pass": true}.
Population: 4 canonical-versus-negate/uniform comparisons, allK4. Rule: all4 strict advantages.

**W3: amended/descriptive.** on cifar10_rgb_hwc, Spearman(own loss E4, G) across the 7 arms <= -0.6.
Observed: {"spearman": -0.8928571428571429, "pass": true}.
Population: 7 arms; loss_delta K3, othersK4. Rule: Spearman <= -0.6.

**Battery 112.**

**Z1: PASS.** G_cal <= 0.002 at all six sizes on metamath, aitdcc_b_c_source and dclm_ranked (18 cells).
Observed: {"count": 18, "need": 18, "pass": true}.
Population: 18 cells. Rule: all18 gains <= 0.002.

**Z2: PASS.** G_cal - G_1 > 0.002 in at most 3 of the 42 cells.
Observed: {"count": 0, "max": 3, "of": 42, "pass": true}.
Population: 42 cells. Rule: at most3 increases > 0.002.

**Z3: FAIL.** on cifar10_rgb_hwc at 24M, |G_cal - G_1| <= 0.005.
Observed: {"abs_diff": 0.0053344622960226976, "pass": false}.
Population: HWC24M. Rule: absolute calibrated-minus-raw gain <= 0.005.

**F.2 Gates, amendments and corrections.** All original outputs are preserved; the audit records, written by Codex (an
AI system; Appendix H), are released with the paper.

| Battery | Gate, amendment or correction (audit record) |
|---|---|
| B89 | Primary13-byte reference adjustment is an accounting convention; full-file sizes are a separate sensitivity. c135_b89_source_review/completed/REVIEW.md. |
| B91 | The frozen protocol mislabels the no-floor fit as the paper's Figure1 procedure. Correct attribution separately; do not alter the protocol or the failed thresholds. Four labels lack held-out24M targets, leaving22/26 evaluable. c146_b91_scaling_review/REVIEW.md. |
| B94 | Original universal G8-to-B86 parity is not26/26:22 matched cases checked, four unequal-seed comparisons skipped/unmet. Full-K parity separately verified all26, but does not repair a first-eight gate. T3 uses8–10 seeds. c154_b94_review/REVIEW.md, B86_PARITY.json. |
| B95 | Actual all-K ensembles have10 protein seeds,9 astronomy/DNA/Kolmogorov-DNA,8 elsewhere, versus the stated eight. Preserve as-implemented values with the deviation, rather than claim exact-eight compliance. C3 uses25 labels. c156_b95_review/REVIEW.md. |
| B97 | All81 saved-B75 parity comparisons pass. The source's mean_abs field is abs(mean difference); the independent mean(abs(row difference)) check also passes. Saved calibration trajectories limit inference reproducibility. c162_b97_review/REVIEW.md. |
| B98 | Byte alignment and archive-size/accounting checks; retain per-label populations, including170/256 ELF standard rows. Recorded compressor conditional-payload interpretation remains. c166_b98_review/REVIEW.md. |
| B99 | Missing load keys absent, unexpected keys explained as the30 causal-mask buffers. Ranked-DCLM group assignment error remains Y1FAIL; report Y2 eligible denominators. c168_b99_review/REVIEW.md. |
| B100 | Original share-zero implementation loses an expert after numerical underflow and can violate the exact-Bayes comparator bound. Preserve original output plus versioned log-space correction; numerical values changed, frozen L1/L2/L3 outcomes did not. c170_b100_review/REVIEW.md and CLAUDE_CORRECTION_CHECK.json. |
| B102 | Acquisition amendment for the two unavailable saved labels followed a printed row. Later complete saved-input/parity checks pass but do not retroactively establish pre-outcome gate execution. c174_b102_source_review/C176_AMENDMENT_REVIEW.md, c178_b102_review/REVIEW.md. |
| B103 | Local conditioned program-output surrogate is not the authors' training distribution; subsequent joint gate records do not erase execution/metadata limits. All three failed criteria remain. c177_b103_review/REVIEW.md, c178_b102_review/REVIEW.md. |
| B104/B105 | Masked lpaq contexts retain selector/shared state; preserve failed mask predictions without clean ablation claims. B105's continuous derivative certificate is a separate post-hoc check; frozen grid unchanged. c183_b104_b105_review/REVIEW.md. |
| B106 | Admission hardening followed observed outcomes; seven concrete bad-input cases were later rejected, completed actual inputs independently checked. Standard Gutenberg2/256 versus forced256/256. c187_b106_gate_review/REVIEW.md, c188_b106_review/REVIEW.md. |
| B108/B109 | Withdraw the invalid protocol interpretation of failed K2 as evidence that hedging suffices. Keep V_auto's benchmark-informed design and original scale-update defect; no silent repaired predictor substitution. c193_b108_review/REVIEW.md, c195_b109_front_review/REVIEW.md. |
| B110/B111 | Original150 shape errors, original inadmissible record, post-outcome row-count amendment, unchanged numerical criteria, loss_delta K3, four-cell Figure3 aggregate parity, all6x4 canonical/B97 array checks. c215_followup_review/REVIEW.md. |
| B112 | All42 parity references present and matching, despite optional-check source weakness. Z3FAIL remains; member calibration precedes averaging. c215_followup_review/REVIEW.md. |

**F.3 lpaq1 masking.** We also ran lpaq1 with groups of its model inputs masked. Because masked contexts still select
mixer weights and share hash state, those variants are not clean smaller compressors; only the full lpaq1 is
interpretable. Two of the three frozen predictions of Battery 104 failed (P1, P3).

**F.4 Details of Section 3.5.**

**Outputs of the program machine.** On outputs of our reimplementation of the paper's machine (a long-output,
nonconstant-tail-conditioned local uniform-prior surrogate, 0.196% of sampled programs accepted; Battery 103), the
24M self-play ensemble's loss is 0.304 bits per byte against paq8px's 0.253 per-byte log loss (0.285 archive
rate), and it realizes a small positive gain of 0.0153 [0.0121, 0.0188] beyond paq8px. We had predicted that the learners would be at least 0.3 bits per byte below paq8px on this local program-output surrogate (H1), that their gain would be at
least 0.1 (H2), and that the fixed-prior 6M ensemble would have lower loss than the self-play 6M ensemble on these
uniform-prior outputs (H3); all three failed, the last by a wide margin (2.971 against 0.329). A small gain on this
surrogate does not show that the learners carry no program structure, and the surrogate is not the authors'
training distribution.

**Where the image gains lie.** The learners' largest gains beyond paq8px are on images (Section 3.2). We
predicted that they would concentrate at bytes that continue an arithmetic progression of earlier values, a
hypothesis motivated by the authors' finding that the recognized generator sequences are mostly arithmetic
progressions; this failed on all three criteria (W1 ratio 0.6192
against a predicted 2; W2 0 of 4; W3 2 of 4; Battery 107). Post hoc, and conditioned on the realized byte, a large
share of the net gain falls at bytes whose value differs by more than 32 from the byte s positions earlier (s = 3 in HWC layout and 1 otherwise; image
and plane boundaries are not masked) (36% and 23% of the
full-window net gain on the two CIFAR-10 layouts, 89% on Fashion-MNIST and KMNIST); these are outcome-conditioned
accounting classes, not features known before the byte. Two knowledge-free hedgers mixed with paq8px in the same
way, a uniform distribution and causal order-0 counts, realize less than the learners on all four image row sets
(K1 held; Battery 108), so the learners' image gain is not reproduced by these hedgers; this does not exclude
every hedging or calibration scheme. The predictions that the learners' median probability of the true byte at large jumps exceeds 4/256 (K2) and
exceeds paq8px's median there (K3) both failed, on each of the 4 row sets.

**A hand-built predictor on the same images.** V_auto, our frozen hand-built online predictor with no offline parameter training (its design was informed by the
benchmark formats, and its original implementation, including a disclosed scale-update defect, is used unchanged;
Appendix B), was mixed with paq8px in the
same way (Battery 109). On CIFAR-10 it realizes 0.0479 bits per byte in HWC layout and 0.0909 in planar layout,
against 0.0186 and 0.0072 for the learners; with paq8px, V_auto and the learners all in one mixture, the learners
add 0.0056 and 0.0002. The two layouts come from one dataset. On Fashion-MNIST V_auto realizes 0.0016 and the
learners 0.0084, and the learners still add 0.0072 once V_auto is included. These are realized-combiner
accounting: moving from two to three experts changes the initial weights and share redistribution, so the
differences do not measure information shared by, or unique to, either predictor. They show that the learners'
image gains beyond paq8px are not uniquely achieved by self-play on the tested CIFAR-10 layouts; they do not show
that any competent predictor would suffice.

**Failed predictions.** Across Batteries 91 to 109, 24 frozen predictions failed and are reported with
their denominators in Appendix F, among them: larger gains beyond paq8px than observed (B98 R1: 1 of 26 labels
above 0.01, predicted at least 8); at most 5 benchmark labels above 0.005 at s = 0.001 (B100 L1: 7 of 26); bGPT
above the learners on every domain row set (B100 L3); bGPT's complementarity at least 10 times the learners' on all four designated text-group labels (B99 Y1: 3 of 4,
failing on rank-coded web text, which we had grouped as natural text in error); an advantage over paq8px on a local program-output surrogate (B103 H1 to H3); image-gain location (B107 W1 to W3) and
learner confidence at large jumps (B108 K2, K3). The predictions of the size sweep, the round sweep and the
fixed-prior comparison (B101, B102), the static mixture (B105), the new sources (B106) and the hand-built image
comparison (B109) held.

**F.5 Post-hoc reading of the authors' Figure 3 data.** Source: the released
`figures/fig3_curriculum_value/data/plotted_values.csv` (columns `epiplexity_mean`, `dclm_ensemble_K8`,
`cifar10_rgb_planar_ensemble_K8`), read after the incremental-test results were known. Endpoints 1024 / 2048 / 4096:
estimated epiplexity (mean over eight seeds, nats × learner rounds) 444.573 / 767.249 / 1705.051, the last mean
including one outlying seed; eight-seed ensemble loss on raw web text 4.82929 / 4.84064 / 4.94678; on planar CIFAR-10
6.28662 / 6.18204 / 6.12245. The published panel plots means over the 70 four-seed subsets (columns `dclm_subset_mean` and
`cifar10_rgb_planar_subset_mean`): 5.2047 / 5.1851 / 5.2804 on raw web text and 6.4719 / 6.3468 / 6.3224 on planar
CIFAR-10, so on raw web text the plotted mean is also higher at T4096 than at T1024 (after a slight dip at T2048), while
on planar CIFAR-10 it falls at every endpoint; elsewhere we quote the K8 columns.

**F.6 Calibrated members (Battery 112).** We tested whether online calibration of the members reveals additional gain. We calibrated each member online
(a fixed-share mixture of the same model at temperatures 0.7 to 2.0, computed from full distributions) before
probability averaging (Battery 112, on arrays scored earlier). G of the calibrated eight-seed ensembles stays below
0.002 on Metamath, C source and rank-coded web text at all six sizes (18 of 18), and calibration raises G by more
than 0.002 in none of the 42 size-label cells. On CIFAR-10 in HWC layout at 24M it lowers G from 0.0143 to 0.0090, which failed our
prediction of a change of at most 0.005. The calibrated-member ensembles also have higher own loss than the raw ones
in 40 of 42 cells. This calibrates members before averaging; calibration of the ensemble itself was not tested.

## Appendix G. The gain beyond a simpler compressor (Batteries 113 to 117)

All five batteries were run after the main results. Batteries 113, 114, 115 and 117 had protocols with numerical
predictions whose SHA-256 was recorded before their outcomes (prefixes 0cb606c9, d0bc759d with amendment 206b8f73,
5c002a5d and b56fa8e2); Battery 116 was declared exploratory, and its 18 completed variant scores are logged (not a
timestamped record of every attempt). Learners are the evaluated ensembles on the eight benchmark text, code and
formal labels (Metamath, C source, Python, arXiv mathematics, raw and Common Crawl web text, KoLMogorov text,
rank-coded web text) and E24 on new sources. G uses the s = 0.001 mixture of the main text; a code length is the mean
of the logged per-byte log losses, not an archive size.

**G.1 Battery 113 (per-byte strata of saved arrays).** Q1, that the first 512 positions carry at least 25% of the
signed gain beyond lpaq1 on at least 6 of 8 labels, held on 8 of 8 (54.6% to 88.6%). Q2, the same for paq8px's
advantage over lpaq1, failed (4 of 8; 19% to 28%), although per byte that advantage is 1.7 to 2.7 times larger in the first 512 positions than after them. Q3, that repeat-hit bytes carry less than average gain on at least 6 of 8, failed in the opposite direction (0 of 8; 1.6 to 13.2
times the label mean). Q4, that word-start bytes are over-represented on at least 5 of 7 ASCII labels, failed (0 of 7). Q5, a positive rank correlation between the gain beyond lpaq1 and paq8px's advantage over lpaq1 on at least 7 of 8,
held (8 of 8; 0.25 to 0.36), but both
quantities contain lpaq1's code length, so it is not independent evidence. Post hoc, early repeat hits (positions
below 512 whose byte an earlier 8-byte repeat predicts) carry 36.6% to 75.0% of the total signed gain beyond lpaq1
over whole windows; repeat hits are defined with the observed byte, and the mixture's weights restart in every
window. Beyond paq8px, the mean per-byte gain in the four position strata (below 64, 64 to 511, 512 to 2047, 2048 and
above) lies between −0.0162 and −0.0005 on seven labels; on rank-coded web text it is +0.0487 below position 64 (+0.38 in positions 0 to 15) and between −0.0007 and −0.0005
elsewhere. Over whole windows it stays at or below 0.002 on all eight.

**G.2 Battery 114 (suppressing paq8px model groups).** A logging paq8px (commit c84f576) with a neutral mode: while a
suppressed group mixes, its mixer inputs and weight-set selections are 0. With nothing suppressed, the per-byte code
lengths equal Battery 98's on all 2,042 windows (gate S0). S1, that at least 12 of the 14 single suppressions leave
G <= 0.002 on at least 6 of 8 labels, held (14 of 14, on all 8). S2, that keeping the direct inputs of only the order-n, match and word groups gives G > 0.002 on at least 6 of 8,
failed (0 of 8). S3, that the text model is the most useful addition to
that core, failed; no addition changed G by more than 3 × 10⁻⁵. Keeping the direct inputs of only the order-n group gives G above 0.002 on 3 of 8 (at most 0.0055). An amendment
recorded after a four-window smoke test but before the full run's outcomes were read withdrew a claim about the direction of
bias: suppressed groups remain visible to the SSE stage and RecordModel through shared state.

**G.3 Battery 115 (five changes to lpaq1).** U1 mixer weights start at 0.3 (lpaq1: 0); U2 match confidence not split
by previous byte; U3 weight set chosen by order and match state only (10 sets instead of 80); U4 an order-0 input; U5
mixer learning rate tripled for the first 512 bytes. Every variant is a complete compressor (round trips verified), and with no change the per-byte code lengths equal
Battery 104's on all 2,042 windows (gate G0); a three-window smoke test had shown own code lengths, not G, before the protocol was frozen. P1, that all five together
lower G on all 8 labels, held. P2, that they give G <= 0.002 on at least 6 of 8, failed (5 of 8). P3, that at least
70% of the reduction comes from the first 512 positions on at least 6 of 8, failed (5 of 8). P4, that U2 is the most
useful single change, failed: U1 was (mean reduction 0.0217). P5, G <= 0.002 on at least 3 of the 4 previously
evaluated Battery 106 text sources, failed (1 of 4; JSON 0.026). Every variant, including the original lpaq1, has a
lower mean code length than the learners on all 12 row sets.

**G.4 Battery 116 (exploratory development).** On the 12 row sets of Battery 115 we added context-mixing techniques to
the five changes: orders 5 and 7, a word-bigram context, sparse contexts, SSE keyed by match length and by the
previous byte, indirect contexts, column contexts, a structure context (quote state, bracket depth, last
punctuation), a key context (the last quoted string before a colon) and initial weights 2.1/N for N mixer inputs. A second mixer selected by the partial byte lowered G on 9 of the 12 row sets but raised the largest G (0.0074 to
0.0084) and was not retained. Of 18 logged variants, one (16
switches) left G <= 0.002 on all 12 (maximum 0.0019, rank-coded web text); it was frozen before Battery 117 (926 lines of C++; source SHA-256 prefix 0b670427).

**G.5 Battery 117 (prospective test of the frozen variant).** Six sources never used before, fixed before download:
Project Gutenberg texts 11, 1661 and 98; C++ headers of nlohmann/json 3.11.3; Java files of gson 2.11.0;
reStructuredText of Flask 3.0.3; Linguist's languages.yml (v7.30.0); and Haskell files of pandoc 3.1.13 (Table G1).
C1, that G beyond the frozen variant is at most 0.002 on at least 5 of 6, held. C2, that its code length is below the
learners' on all six, held. C3, that G beyond paq8px is at most 0.002 on all six, held on the windows paq8px retained, but its standard mode retained only 1 of 256 book windows and 255 of 256
Haskell windows, so C3 is uninformative for the books. All 256 book windows contain carriage returns, including the
retained one, and the excluded Haskell window contains none; the causes of these exclusions are not identified. C4, that G beyond the original
lpaq1 exceeds 0.002 on at least 4, held (6 of 6). The frozen variant's source is released with the paper.

**Table G1.** *Battery 117: own code length (bits per byte) and realized gain G of the learners (E24) beyond the original lpaq1 and beyond the frozen variant (95% window-bootstrap interval), on six sources fixed before download.*

| Source | Windows | Learners | lpaq1 | Frozen variant | G beyond lpaq1 | G beyond frozen variant |
|---|---|---|---|---|---|---|
| Books (Gutenberg) | 256 | 4.675 | 3.286 | 3.149 | 0.0087 | −0.0002 [−0.0004, 0.0001] |
| C++ headers | 256 | 2.380 | 1.677 | 1.512 | 0.0365 | 0.0034 [0.0026, 0.0045] |
| Java | 256 | 3.063 | 2.132 | 1.959 | 0.0237 | 0.0002 [−0.00004, 0.0004] |
| Haskell | 256 | 3.138 | 2.297 | 2.137 | 0.0301 | 0.0012 [0.0007, 0.0019] |
| reStructuredText | 129 | 4.303 | 2.983 | 2.851 | 0.0164 | 0.0004 [−0.00002, 0.0008] |
| YAML | 35 | 2.344 | 1.801 | 1.590 | 0.0234 | −0.0004 [−0.0006, −0.0001] |

## Appendix H. How the study was made

The author directed the work and authorized its scope and cloud use. Claude (Anthropic) wrote the code, ran the
experiments and drafted the text; Codex (OpenAI) reviewed code and recomputed saved results, preserving the original
experimental artifacts; ChatGPT sessions reviewed manuscript versions supplied by the author. The project log is an append-only file
of numbered messages between Claude and Codex, kept by the author, in which protocol hashes and declared freezes were recorded; its timestamps are written by the
agents and document an internal sequence, not an external preregistration, and smoke results seen before freezing,
amendments and departures are reported in Appendices F and G.
The study ran on 28 and 29 September 2026. Earlier work in the same project (Batteries 1 to 74: a reproduction of the
self-play pipeline including small local self-play training runs, probes of the released learners, and the start of
the hand-built predictors of Appendix B) is outside the counts of Appendices F and G. Scoring and analyses used an
Apple M4 laptop (16 GB) and Modal cloud CPU and GPU containers; the project's metered Modal usage for September 2026, as reported by Modal on 30 September 2026, was about US$20,
covered by free credits. The release includes every protocol with its full SHA-256 and, for the 42 primary protocols, the ID and
agent-written timestamp of the log message that first recorded it, and the audit
reports cited in Appendix F; their supporting files and the log itself are available on request.


## References

- aujurd22 (2026). selfplay-paper-analysis. GitHub repository, github.com/aujurd22/selfplay-paper-analysis (inspected 2026-09-29).
- Bates, J. M., and Granger, C. W. J. (1969). The combination of forecasts. Operational Research Quarterly, 20(4):451–468.
- Becker, B., and Kohavi, R. (1996). Adult. UCI Machine Learning Repository. doi:10.24432/C5XW20.
- Bell, T., Witten, I. H., and Cleary, J. G. (1989). Modeling for text compression. ACM Computing Surveys, 21(4):557–591. doi:10.1145/76894.76896.
- Bellard, F. (2021). NNCP v2: lossless data compression with transformer. Technical report, bellard.org/nncp/nncp_v2.pdf.
- Bloem, P. (2025). Universal pre-training by iterated random computation. arXiv:2506.20057.
- BurntSushi (2024). ripgrep 14.1.1. Software, github.com/BurntSushi/ripgrep, tag 14.1.1 (accessed 2026-09-29).
- Cesa-Bianchi, N., and Lugosi, G. (2006). Prediction, Learning, and Games. Cambridge University Press.
- Chong, Y. Y., and Hendry, D. F. (1986). Econometric evaluation of linear macro-economic models. Review of Economic Studies, 53(4):671–690.
- Clanuwat, T., Bober-Irizar, M., Kitamoto, A., Lamb, A., Yamamoto, K., and Ha, D. (2018). Deep learning for classical Japanese literature. arXiv:1812.01718.
- Cleary, J. G., and Witten, I. H. (1984). Data compression using adaptive coding and partial string matching. IEEE Transactions on Communications, 32(4):396–402.
- Cowsik, A., Dolev, K., Li, M. Y., De Luca, G. B., Cohen, N., Goodman, N. D., and Levine, Y. (2026). Self-play pretraining with zero data. arXiv:2609.30063. Code: github.com/acowsik/self_play_pretraining; released checkpoints: huggingface.co/nourya-cohen/solomonoff-paper.
- Delétang, G., et al. (2024). Language modeling is compression. ICLR 2024.
- Feder, M., Merhav, N., and Gutman, M. (1992). Universal prediction of individual sequences. IEEE Transactions on Information Theory, 38(4):1258–1270.
- Finzi, M., et al. (2026). From entropy to epiplexity: rethinking information for computationally bounded intelligence. arXiv:2601.03220.
- Geirhos, R., Meding, K., and Wichmann, F. A. (2020). Beyond accuracy: quantifying trial-by-trial behaviour of CNNs and humans by measuring error consistency. NeurIPS 2020. arXiv:2006.16736.
- Goyal, M., Tatwawadi, K., Chandak, S., and Ochoa, I. (2021). DZip: improved general-purpose lossless compression based on novel neural network modeling. Data Compression Conference (DCC 2021).
- Grau-Moya, J., et al. (2024). Learning universal predictors. ICML 2024, PMLR 235:16178–16205.
- Harvey, D. I., Leybourne, S. J., and Newbold, P. (1998). Tests for forecast encompassing. Journal of Business & Economic Statistics, 16(2):254–259.
- Haussler, D., Kivinen, J., and Warmuth, M. K. (1998). Sequential prediction of individual sequences under general loss functions. IEEE Transactions on Information Theory, 44(5):1906–1925. doi:10.1109/18.705569.
- Herbster, M., and Warmuth, M. K. (1998). Tracking the best expert. Machine Learning, 32(2):151–178.
- Heurtel-Depeiges, D., Ruoss, A., Veness, J., and Genewein, T. (2025). Compression via pre-trained transformers: a study on byte-level multimodal data. ICML 2025, PMLR 267:23120–23135.
- Huang, Y., Zhang, J., Shan, Z., and He, J. (2024). Compression represents intelligence linearly. COLM 2024. arXiv:2404.09937.
- Hutter, M. (2003). Convergence and loss bounds for Bayesian sequence prediction. IEEE Transactions on Information Theory, 49(8):2061–2067. doi:10.1109/TIT.2003.814488.
- Høst-Madsen, A. (2021). Bounds for learning lossless source coding. IEEE International Symposium on Information Theory (ISIT 2021). doi:10.1109/ISIT45174.2021.9517758.
- Jackson, Z., et al. (2018). Free Spoken Digit Dataset, v1.0.10. github.com/Jakobovski/free-spoken-digit-dataset (accessed 2026-09-29).
- Jiang, L., Shinnick, Z., van den Hengel, A., Saratchandran, H., and Teney, D. (2026). Procedural pretraining: warming up language models with abstract data. ICML 2026. arXiv:2601.21725.
- Kim, K., Kotha, S., Liang, P., and Hashimoto, T. (2026). Pre-training under infinite compute. ICLR 2026. arXiv:2509.14786.
- Knoll, B. (2013). cmix. Software, github.com/byronknoll/cmix (development since December 2013; current version accessed 2026-09-29).
- Knoll, B., and de Freitas, N. (2012). A machine learning perspective on predictive coding with PAQ8. Data Compression Conference (DCC 2012).
- Krichevsky, R. E., and Trofimov, V. K. (1981). The performance of universal encoding. IEEE Transactions on Information Theory, 27(2):199–207. doi:10.1109/TIT.1981.1056331.
- Krizhevsky, A. (2009). Learning multiple layers of features from tiny images. Technical report, University of Toronto.
- Li, J., et al. (2024). DataComp-LM: in search of the next generation of training sets for language models. NeurIPS 2024 Datasets and Benchmarks. arXiv:2406.11794.
- lodash contributors (2021). lodash 4.17.21. Software, github.com/lodash/lodash, tag 4.17.21 (accessed 2026-09-29).
- Mahoney, M. (2007). lpaq1. Software, mattmahoney.net/dc (accessed 2026-09-29).
- Mahoney, M. V. (2005). Adaptive weighing of context models for lossless data compression. Technical Report CS-2005-16, Florida Institute of Technology.
- Mahoney, M., and paq8px contributors (2026). paq8px. Software, github.com/hxim/paq8px, commit c84f576fc2c522194cd320743708652a154daf6b (accessed 2026-09-29).
- Mao, Y., Cui, Y., Kuo, T.-W., and Xue, C. J. (2022). TRACE: a fast transformer-based general-purpose lossless compressor. Proceedings of the ACM Web Conference 2022.
- Maverick-Ansh (2026). self-play-pretraining-zero-data. GitHub repository, github.com/Maverick-Ansh/self-play-pretraining-zero-data (inspected 2026-09-28).
- Megill, N. D., and Wheeler, D. A. (2019). Metamath: A Computer Language for Mathematical Proofs. Lulu Press.
- Mikolov, T., Deoras, A., Kombrink, S., Burget, L., and Černocký, J. (2011). Empirical evaluation and combination of advanced language modeling techniques. Interspeech 2011. doi:10.21437/Interspeech.2011-242.
- mledoze (2026). countries. Dataset, github.com/mledoze/countries, countries.json pinned by SHA-256 (accessed 2026-09-29).
- OpenSLR (2026). YESNO corpus, SLR1, openslr.org/1 (accessed 2026-09-29).
- Panayotov, V., Chen, G., Povey, D., and Khudanpur, S. (2015). Librispeech: an ASR corpus based on public domain audio books. ICASSP 2015.
- Piczak, K. J. (2015). ESC: dataset for environmental sound classification. ACM Multimedia 2015.
- Project Gutenberg (2026). eBooks 2701, 1342 and 84, plain text, gutenberg.org (accessed 2026-09-29).
- Python Software Foundation (2026). Python 3.12 documentation, HTML archive, docs.python.org/3.12/archives (accessed 2026-09-29).
- Schmidhuber, J. (2009). Driven by compression progress: a simple principle explains essential aspects of subjective beauty, novelty, surprise, interestingness, attention, curiosity, creativity, art, science, music, jokes. In Anticipatory Behavior in Adaptive Learning Systems, LNCS 5499, 48–76. Springer. doi:10.1007/978-3-642-02565-5_4.
- Schmidhuber, J., and Heil, S. (1996). Sequential neural text compression. IEEE Transactions on Neural Networks, 7(1):142–146.
- Shinnick, Z., Jiang, L., Saratchandran, H., van den Hengel, A., and Teney, D. (2025). Transformers pretrained on procedural data contain modular structures for algorithmic reasoning. arXiv:2505.22308.
- The Go Authors (2026). Go 1.22.5 source release, go.dev/dl/go1.22.5.src.tar.gz (accessed 2026-09-29).
- Thickstun, J., Harchaoui, Z., and Kakade, S. (2017). Learning features of music from scratch. ICLR 2017.
- Vovk, V. (1990). Aggregating strategies. Proceedings of the Third Annual Workshop on Computational Learning Theory (COLT 1990), 371–386.
- Warden, P. (2018). Speech Commands: a dataset for limited-vocabulary speech recognition. arXiv:1804.03209.
- White, H. (2000). A reality check for data snooping. Econometrica, 68(5):1097–1126.
- Wikimedia Foundation (2026). Wikipedia dumps of 1 November 2023 (Hebrew and German), via the Hugging Face dataset wikimedia/wikipedia (accessed 2026-09-29).
- Willems, F. M. J., Shtarkov, Y. M., and Tjalkens, T. J. (1995). The context-tree weighting method: basic properties. IEEE Transactions on Information Theory, 41(3):653–664.
- Witten, I. H., Neal, R. M., and Cleary, J. G. (1987). Arithmetic coding for data compression. Communications of the ACM, 30(6):520–540. doi:10.1145/214762.214771.
- Wu, S., Tan, X., Wang, Z., Wang, R., Li, X., and Sun, M. (2024). Beyond language models: byte models are digital world simulators. arXiv:2402.19155.
- Xiao, H., Rasul, K., and Vollgraf, R. (2017). Fashion-MNIST: a novel image dataset for benchmarking machine learning algorithms. arXiv:1708.07747.
- Yoran, O., Zheng, K., Gloeckle, F., Gehring, J., Synnaeve, G., and Cohen, T. (2025). The KoLMogorov Test: compression by code generation. ICLR 2025. arXiv:2503.13992.
