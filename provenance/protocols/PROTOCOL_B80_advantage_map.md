# Battery 80 protocol: where exactly do the learned models lead? (position and copy decomposition)

Frozen 2026-09-29 before any per-position readout was computed; hashes recorded in AGENT_CHAT (C118). Inference only
(Ariel: "in parallel and efficiently, use the cloud if needed"). Descriptive decomposition of already frozen methods;
no method is changed.

## Part A: self-play benchmark (26 labels, identical rows)

- Per-position code lengths (bits) for frozen V_base (`white_box2`, V_base) and frozen V_auto (`white_box4`), scored
  exactly as before (first 256 rows, all 4095 targets, no prefix), plus the copy indicator m(t) = 1 if the frozen
  copy expert has a proposal at t (an earlier occurrence of a suffix of length >= 3), from `match_proposals`.
- Per-position code lengths of the frozen B75 evaluated ensemble (the seeds of the frozen B75 readout).
- D(t) = method(t) - ensemble(t), averaged over rows. Position bins: [0, 16), [16, 64), [64, 256), [256, 1024),
  [1024, 4095). Copy split: mean D over positions with m = 1 and with m = 0.
- Predictions (V_auto against the ensemble):
  - A1: on at least 22 of 26 labels, mean D is higher in [0, 256) than in [1024, 4095): the learned models' relative
    advantage is concentrated early in the window, before in-sequence statistics accumulate.
  - A2: in [1024, 4095), V_auto has lower mean bits per byte than the ensemble on at least 20 of 26 labels.
  - A3: on at least 18 of 26 labels, mean D is higher at positions without a copy proposal (m = 0) than with one.
- Row-bootstrap intervals (seed 800, 2000 draws) for the early-minus-late contrast per label.

## Part B: speech (the same 2,000 LibriSpeech chunks as B79)

- Per-token log probabilities of Mistral-7B and Qwen2.5-7B (same revisions and text maps as B79), attributed to the
  chunk position of each token's last character; per-position code lengths of V_base on the same chunks and maps.
- Position bins: [0, 16), [16, 64), [64, 256), [256, 1024), [1024, 2048); rates per bin under the released-code
  convention (7-bit) and with all 8 bits.
- Prediction B1: under the 7-bit convention, each language model's rate minus V_base's rate is lower (more in the
  model's favour) in [0, 256) than in [1024, 2048).

All outcomes are reported; any other cut is exploratory and labelled so.
