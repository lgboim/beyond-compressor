# Reproducibility

**From the files in this repository and the release assets (seconds, CPU only):**

    cd tool && python test_reproduce.py

reproduces the paper's Table 1 (realized gain of the evaluated self-play ensembles beyond paq8px on the eight text,
code and formal labels, at fixed share 0.01 and 0.001 and for the exact Bayesian mixture) to within 1e-6 bits per
byte (observed maximum difference 1.9e-12), and checks two identities: a model identical to the compressor gains 0,
and a uniform model's gain lies between the deterministic worst-case bound and 0.

**What needs the original release:** the benchmark windows (rebuilt with the original authors' bake scripts and
verified here by SHA-256) and the released model checkpoints, to recompute model probabilities.

**What is not reproduced by this repository:** running paq8px and lpaq1 themselves (the patches are included; the
logged outputs are provided), and the model inference behind the paper's other tables.
