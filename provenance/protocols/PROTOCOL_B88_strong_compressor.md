# Battery 88 protocol: a strong off-the-shelf context-mixing compressor as a reference

Frozen 2026-09-29 before any compressor output on these rows; hashes in AGENT_CHAT (C133). No training; cloud CPU.
Ariel asked for the fastest way to answer the obvious reviewer question raised by Battery 87 (zlib beat the learners
on 5 of 8 new sources): what does a strong general-purpose compressor do?

**Compressor.** paq8px (github.com/hxim/paq8px, default branch at build time; the commit hash is recorded), built
from source with its CMake release configuration, run at level `-8` with default options on each 4095-byte window
as a separate file named `w`. Code length = 8 x output size / 4095 bits per byte, headers included (primary); the
output size of a 1-byte file is recorded so a header-corrected rate can be reported separately. References on the
same windows: zstd level 19, brotli quality 11, xz (LZMA preset 9 | extreme).

**Rows.** The 26 benchmark labels (first 256 rows, 250 for ranked DCLM, first 4095 bytes; the rows of Batteries
75-86) and the 8 Battery 87 sources (256 windows each), 34 row sets in all, packed as uint8 arrays with hashes.

**Predictions.**
- Q1: paq8px is below the published minimum on at least 18 of 26 labels.
- Q2: paq8px is lower than E24 (Battery 87) on at least 6 of 8 new sources.
- Q3: paq8px is lower than V_match on at least 17 of the 34 row sets.
paq8px was developed by others on public compression corpora, not on these rows; it is an off-the-shelf reference,
not one of our predictors. Row intervals (seed 880) are descriptive. All outcomes are reported.
