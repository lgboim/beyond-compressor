# Battery 90: descriptive timing of paq8px, V_match and a released learner

Frozen 2026-09-29 before any timing; hash in AGENT_CHAT (C144). Descriptive only, no predictions; a reviewer is
likely to ask how the compute of the reference compressor compares with the learners'.

Measured on cloud machines, wall-clock time per 4095-byte window: (a) paq8px (the B88 commit, level -8, one file per
window, one CPU core) on the first 64 windows of four row sets (ranked DCLM text, 8-bit audio, CIFAR-10 HWC, and the
new ELF source); zlib and LZMA on the same windows for reference; (b) V_match on the same 4 x 64 windows, vectorised
over rows as in all batteries (2 CPU cores), reported as total time / 64; (c) the released 24M learner (seed 0, round
8191) on one NVIDIA A10G GPU, the same 4 x 64 windows with the `O` prefix, batch 8, fp32, after one warm-up batch,
with CUDA synchronisation; an 8-seed ensemble costs eight such passes. Model loading and image build time are excluded
and reported separately. Hardware and software versions are recorded.
