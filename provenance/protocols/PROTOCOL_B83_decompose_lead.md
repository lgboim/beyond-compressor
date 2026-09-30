# Battery 83 protocol: decomposing the learners' remaining lead (copy use, context length, temperature)

Frozen 2026-09-29 before any B83 readout; hashes in AGENT_CHAT (C125). Inference only ("in parallel and efficiently,
use the cloud if needed"; Ariel asked whether quick tests can pin down where the advantage lies).

**Where the lead remains.** After B81, the evaluated ensembles are lower than V_auto by more than 0.02 bits per byte on
three labels: Metamath (0.31), ranked DCLM (0.15) and C source (0.03). In B80's position bins their lead is near zero
in bytes 0-15 and largest in bytes 64-1023; on ranked DCLM it sits at positions with a copy proposal. Position is
confounded with the target bytes (C1112). This battery separates the parts.

## Part A (saved arrays, local, seconds): what kind of positions carry the lead

Metamath and ranked DCLM; D(t) = V_auto(t) - ensemble(t) from the B80 per-position arrays and the B75 probabilities
(positive = the ensemble is lower). Copy proposals from `match_proposals` (as in B80). For a set S of positions:
lead share = sum of D over S / sum of D over all positions; position share = |S| / all positions.
- A1: on both labels, positions whose copy proposal is wrong (proposal present, not equal to the actual byte) have a
  larger lead share than position share.
- A2: on ranked DCLM, within-word letters (an ASCII letter preceded by an ASCII letter) have a larger lead share than
  position share.
Descriptive splits: correct versus wrong proposals, match length (3, 4-7, 8-15, 16-32), byte class of the target
(lowercase, uppercase, digit, space, newline, other).

## Part B (cloud): context-length intervention with the targets held fixed

Metamath, ranked DCLM, C source. First 256 rows; the first 3072 bytes of each row are the targets throughout. Each
row's 3072 bytes are cut into consecutive chunks of length L in {16, 64, 256, 1024, 3072}, and each chunk is scored
on its own: the evaluated ensemble (the 8 released seeds of the label's published-minimum configuration, as in B75;
input `O` + chunk; mean of probabilities, then -log2) and frozen V_auto (restarted on every chunk). Every target is
scored once at every L, so only the available context changes. lead(L) = mean over all targets of
V_auto(L) - ensemble(L), with 95% row-bootstrap intervals (seed 830, 2000 draws).
- Parity gates: at L = 3072, V_auto equals the B80 arrays' first 3072 positions (max per-row difference <= 1e-9), and
  the ensemble matches the B75 probabilities (max per-row difference <= 1e-3 bits per byte).
- B1: on Metamath and ranked DCLM, lead(3072) > lead(64).
- B2: on all three labels, lead(16) < 0.05 bits per byte.
Checkpoint SHA-256 and missing or unexpected state-dict keys are recorded for every load.

## Part C (cloud): does softening the learner's predictions lower its loss?

Released 24M learner, seed 0, round 8191, all 26 labels (first 256 rows, `O` prefix, all 4095 targets). Loss of the
actual byte under softmax(logits / T) for T in {0.8, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0}, per position bin as in B82. T* is
the grid value with the lowest mean loss. T* > 1 means the predictions are too sharp for log loss (the temperature
sense of overconfidence, which B82's loss-minus-entropy diagnostic does not establish; C1114).
- C1: over all positions, T* > 1 on at least 18 of 26 labels.
- C2: in bytes 0-15, T* > 1 on at least 18 of 26 labels.
A temperature chosen on the evaluated rows is a diagnostic, not a method; no result from it is compared with a
published value.

All outcomes are reported; other cuts are exploratory and labelled so.
