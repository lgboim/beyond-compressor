# Battery 77 protocol: raster geometry inferred online (V_auto)

Frozen 2026-09-29 before V_auto scored any benchmark label (a synthetic raster of width 40 was used only to check
that the code runs). Hashes are recorded in AGENT_CHAT (C104) before scoring. No learner is run.

**Why.** In B76, V_struct went below the published minimum on both CIFAR-10 layouts, but a post-hoc ablation showed
that this depends on raster experts given the image geometry (lags 32, 96, 1024): without them, V_struct is 5.514
(HWC) and 5.918 (planar), above the published minima 5.033 and 5.709. The learners are not told the geometry. B77 asks
whether a training-free predictor can infer it online.

**Method (probe/white_box4.py).** V_struct with its six fixed-geometry raster experts replaced by four experts whose
lags are chosen online, per row, from past bytes only: the small lag a in 1..8 and the two large lags b1, b2 in
9..1100 with the lowest running mean circular absolute difference. Experts: smooth at b1; the JPEG-LS median edge
detector on (a, b1); x(t-a) + x(t-b1) - x(t-a-b1); x(t-b2) + x(t-a) - x(t-a-b2). All other experts, the mixing and
the constants are V_struct's. Scored on all 26 labels exactly as B76 (first 256 rows, all 4095 targets).

**Readouts.** As B76: mean bits per byte; minus V_struct, V_base and the published minimum; on identical rows minus
the frozen B75 evaluated ensemble, 95% row bootstrap (seed 770, 2000 draws).

**Predictions.**
- G1: on both CIFAR-10 layouts, V_auto is below the B76 no-raster ablation (5.514 HWC, 5.918 planar).
- G2: V_auto is below the published minimum on at least one CIFAR-10 layout.
- G3: on at least 20 of the 24 non-CIFAR labels, V_auto is within 0.03 bits of V_struct.

All outcomes are reported.
