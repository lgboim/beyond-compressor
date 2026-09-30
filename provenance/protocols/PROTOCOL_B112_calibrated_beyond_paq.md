# Protocol B112: do temperature-calibrated learners add more beyond paq8px? (saved artifacts only)

Frozen before any B112 number is computed. Saved arrays only: Battery 97 p_cal (online causal temperature
calibration: fixed-share over temperatures 0.7-2.0 per seed, computed from full distributions) and p1, six sizes,
round 8191, 8 seeds; paq8px per-byte bits from B98. No inference or cloud.

Labels (all B97 labels): metamath, aitdcc_b_c_source, dclm_ranked, cifar10_rgb_hwc, mutopia_melody_16th,
musicnet_pcm8, audio_8bit. Measures: G_cal and G_1 for the 8-seed probability ensemble of p_cal and of p1 members,
Battery 100 two-member rule, share 0.001, B98 retained rows. Parity gate: G_1 equals Battery 101 k8_0.001 within
1e-9 on every cell.

Predictions:
- Z1: G_cal <= 0.002 at all six sizes on metamath, aitdcc_b_c_source and dclm_ranked (18 cells).
- Z2: G_cal - G_1 > 0.002 in at most 3 of the 42 cells.
- Z3: on cifar10_rgb_hwc at 24M, |G_cal - G_1| <= 0.005.
Calibration here is one online temperature family; it does not cover every form of miscalibration. Failed
predictions are reported. Runner probe/battery112.py; output runs/battery/battery112.json.
