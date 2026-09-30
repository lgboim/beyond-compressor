# Battery 87 protocol: a blind test on byte sources never examined in this project

Frozen 2026-09-29 before any byte of these sources was downloaded or looked at; hashes in AGENT_CHAT (C131).
Inference only, on cloud machines (Ariel: "yes, in parallel and efficiently, use the cloud if needed", in reply to
"run the blind test on new sources?").

**Why.** V_struct, V_auto and V_match were designed after inspecting the benchmark's gaps, so their benchmark
counts are diagnostics, not held-out results (reviewers' main objection). This battery scores the frozen methods and
the released learners on eight new sources, chosen and fixed here before any of them was seen.

**Sources (downloaded in the cloud; hashes recorded).**
1. `hewiki`: Hebrew Wikipedia, first parquet shard of `wikimedia/wikipedia` config `20231101.he` (field `text`,
   UTF-8).
2. `dewiki`: German Wikipedia, first parquet shard of `20231101.de`.
3. `go_source`: every `.go` file under `src/` of the Go 1.22.5 source release (go.dev/dl/go1.22.5.src.tar.gz).
4. `fashion_mnist`: Fashion-MNIST training images (`train-images-idx3-ubyte.gz`), 784-byte images, header removed.
5. `elf_x86_64`: ELF files (magic 0x7F 'E' 'L' 'F') under /usr/bin and /usr/lib/x86_64-linux-gnu of the image this battery builds
   (Modal debian_slim, Python 3.11), as bytes.
6. `uci_adult`: UCI Adult `adult.data` (CSV), each line one document.
7. `yesno_pcm16`: OpenSLR SLR1 "yes/no" recordings (waves_yesno.tar.gz), 16-bit PCM samples of each WAV file
   (little-endian bytes, header removed).
8. `python_docs_html`: HTML files of the Python 3.12 documentation archive (docs.python.org/3.12/archives/
   python-3.12-docs-html.zip).
If a source cannot be fetched as specified, it is dropped and reported; none is replaced.

**Rows.** Each source's documents (article, file, image, CSV line or recording) are shuffled with
`numpy.random.default_rng(870)` and concatenated until the stream reaches 8,388,608 bytes, then truncated to that length (or all documents, if
fewer bytes exist).
256 windows of 4095 bytes start at offsets i * floor((len - 4095) / 255), i = 0..255. Every method and learner scores
these rows exactly as the benchmark rows (learners with the `O` prefix).

**Methods.** Frozen V_base (primary; the only predictor fixed before the benchmark gaps were known), V_auto and
V_match; zlib level 9 and LZMA as references. Learners (authors' code, cloud GPUs): the 8 released 24M seeds at
round 8191 as a probability ensemble (E24, fixed in advance), and the 8-seed 24M ensembles at rounds 768, 1024, 1536,
5120, 5376, 5888 and 6144 (the configurations of the benchmark's published minima). "Best-24M" is the lowest of the
eight on each source, selected on these rows, which favours the learners. C_mix: the B86 online mixture of E24 and
V_match (nothing fitted).

**Predictions.**
- H1 (primary): V_base is lower than E24 on at least 5 of 8 sources.
- H2: V_match is lower than E24 on at least 6 of 8 sources.
- H3: V_match is lower than Best-24M on at least 5 of 8 sources.
- H4: C_mix is lower than the better of E24 and V_match by at least 0.02 bits per byte on at least 5 of 8 sources.
Readouts: bits per byte per source, paired differences with row-bootstrap intervals (seed 871, 2000 draws), and
checkpoint hashes. All outcomes are reported.
