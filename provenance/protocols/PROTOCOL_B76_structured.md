# Battery 76 protocol: a training-free mixture with multi-byte structure (V_struct)

Frozen 2026-09-29, before V_struct scored any benchmark label (only a synthetic 16-bit sine was used, to check that
the code runs). Its sha256 and the script's are recorded in AGENT_CHAT (C102) before scoring. Inference-free: no
learner is run; this battery scores a fixed online predictor only.

## Why

On five labels the published minima and the released-checkpoint ensembles have lower bits per byte than every tested
method (B75 C2): CIFAR-10 in both layouts, 16-bit audio, float32 atlas and astronomy. V_base and V_all treat bytes as
symbols, while these data are multi-byte numbers or raster images. B76 asks how much of those gaps a training-free
predictor that knows only generic formats can close. This is post hoc with respect to the observed gaps, and
16-bit audio was already used to develop V_all; the other four gap labels have never been scored by any lag-structured
predictor.

## Method (probe/white_box3.py, fixed before scoring)

V_struct = the 12 V_all experts + 14 generic experts chosen from format knowledge only: phase-conditioned byte counts
(periods 3 and 4); circular smoothness at lags 3, 4, 32 and 96; four 16-bit sample predictors (little- and big-endian,
most- and least-significant byte; order-2 fixed linear prediction, as in FLAC); the JPEG-LS median edge detector for
the two CIFAR raster layouts (left/above lags 1/32 and 3/96); an interleaved-channel difference (lag 3) and a
plane difference (lag 1024). Mixing: Bayesian fixed-share weights kept separately per phase t mod P for P in
{1, 2, 3, 4}, and a top-level fixed-share mixture over the four. Constants as V_base (prior 0.05, share 0.01). The
same predictor, unchanged, is scored on all 26 labels (first 256 rows, all 4095 targets, no `O` prefix), locally or on
cloud CPU containers (the hardware does not enter the computation).

## Readouts

Per label: V_struct mean bits per byte; minus V_base; minus the published minimum; and, on identical rows, minus the
B75 evaluated ensemble (frozen B75 readout: exact / fallback / substitute), with a 95% row bootstrap (seed 760,
2000 draws).

## Predictions

- S1: V_struct is below V_base on all five gap labels.
- S2: on 16-bit audio, V_struct closes at least half of V_base's gap to the published minimum (V_base 6.540,
  minimum 4.933).
- S3: on CIFAR-10 (HWC), the largest gap, V_struct stays above the published minimum.
- S4 (no general harm): on at least 19 of the other 21 labels, V_struct is below V_base or within 0.02 bits of it.

Every outcome is reported, including failed predictions. Anything else is exploratory and labelled so.
