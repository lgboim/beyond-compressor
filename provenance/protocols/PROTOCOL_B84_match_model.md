# Battery 84 protocol: do standard match-model refinements reproduce the learners' lead? (V_match)

Frozen 2026-09-29 before V_match scored any benchmark label (it was run only on a synthetic word sequence, and with
both refinements off it reproduces V_auto exactly); hashes in AGENT_CHAT (C127). Ariel approved "the decisive test"
("in parallel and efficiently, use the cloud if needed").

**Why.** B83 found that on ranked DCLM the evaluated ensemble's whole lead over V_auto sits at positions where the
copy proposal is correct (0.85 bits per byte there), mostly for matches of 4-7 bytes, while V_auto is lower where
the proposal is wrong. Context-mixing compressors (the PAQ family) decide how far to trust a match with two standard
devices that V_auto lacks: mixer weights selected by the match length, and an adaptive probability map (secondary
estimation) on the match prediction. If these reproduce the lead, the learners' ranked-text advantage is a known
compression technique; if not, it is something else.

**Method (probe/white_box6.py).** V_auto unchanged, plus (gate) one more member of the top-level mixture: a
fixed-share mixture of the same experts whose weight set is chosen by the match state (no proposal, or length 3-4,
5-8, 9-16, 17-32); and (apm) a map indexed by match-length bucket and 24 bins of the stretched final probability of
the proposed byte, initialised to the identity, updated online, and averaged with its input; the other bytes are
rescaled. Same constants. Variants: V_gate (gate only), V_apm (apm only), V_match (both; the primary). All 26 labels,
first 256 rows, all 4095 targets, cloud CPU containers; per-position arrays saved for Metamath, ranked DCLM and
C source.

**Predictions (V_match).**
- M1: on ranked DCLM, V_match is lower than V_auto by at least 0.05 bits per byte.
- M2: on ranked DCLM, at positions with a correct copy proposal, V_match is lower than V_auto by at least 0.2 bits.
- M3: on Metamath, the evaluated ensemble remains lower than V_match by at least 0.15 bits per byte.
- M4: V_match is not higher than V_auto by more than 0.01 bits per byte on at least 22 of 26 labels.

**Reading fixed in advance.** If V_match closes at least half of the ranked-DCLM lead (V_match - ensemble <= 0.075),
we will say the learners' advantage there is largely reproduced by standard match-model machinery; if it closes less
than 0.03 bits per byte of it, we will say it is not. Readouts also include V_match minus the B75 ensemble with row
bootstrap (seed 840), the count of labels below the published minimum, and the copy-state split of B83 Part A.
