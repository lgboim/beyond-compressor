# Protocol B106: prospective test of the beyond-paq8px assay on new sources, and paq8px without look-ahead

Frozen before any byte of the new sources is downloaded and before any B106 score exists. Inference and
compression only (Modal); authorized by Ariel ("כן, במקביל ויעיל, אם צריך את הענן תשתמש").

## A. New sources (selected now, never used in this project; public; no terms to accept)

1. gutenberg_en: Project Gutenberg plain texts 2701, 1342 and 84, concatenated in that order
   (https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt).
2. rust_ripgrep: all *.rs files of https://github.com/BurntSushi/ripgrep/archive/refs/tags/14.1.1.tar.gz, sorted by path.
3. js_lodash: all *.js files of https://github.com/lodash/lodash/archive/refs/tags/4.17.21.tar.gz, sorted by path.
4. json_countries: https://raw.githubusercontent.com/mledoze/countries/master/countries.json (bytes pinned by SHA-256
   at download).
5. kmnist_images: raw uint8 pixels of http://codh.rois.ac.jp/kmnist/dataset/kmnist/kmnist-train-imgs.npz (array order).
6. fsdd_audio: all recordings of https://github.com/Jakobovski/free-spoken-digit-dataset/archive/refs/tags/v1.0.10.tar.gz,
   sorted by file name, PCM samples mapped to 8 bits with the benchmark mapping ((s >> 8) + 128) mod 256 for 16-bit
   input (8-bit input kept as is), headers removed.
Each stream is capped at 8 MB, cut into consecutive 4095-byte windows, and 256 windows are drawn without
replacement with numpy seed 1060 (all windows if fewer). Download SHA-256 and file lists are recorded before scoring.

## B. Models and comparators

Learners: E24 (24M, round 8191, the 8 released seeds), as for the Battery 87 sources. paq8px commit c84f576, level -8,
with the Battery 98 logging patch, in two modes: standard, and without block detection (-forcetext for
gutenberg_en, rust_ripgrep, js_lodash, json_countries; -forcebinary for kmnist_images, fsdd_audio). bGPT (Battery 99
weights and scoring): text weights for sources 1-4, image weights for 5, audio weights for 6.

## C. Benchmark without look-ahead

paq8px without block detection on all 34 Battery 88 row sets: -forcetext for dclm, llm_compression_cc,
kolmogorov_text, llm_compression_python, aitdcc_b_c_source, llm_compression_arxiv_math, metamath, hewiki, dewiki,
go_source, python_docs_html, uci_adult; -forcebinary for all others. Learner ensembles as in Battery 98.

## Measure

G = mean[-log2 p_C - bits of M_0.001(x, p_C)] (Battery 100 rule, share 0.001; overhead about 0.001), C a
comparator; realized gain only. Windows are used when the comparator's logged bytes equal the window bytes.

## Predictions

- N1: learners' G beyond standard paq8px <= 0.002 on all four of sources 1-4.
- N2: learners' G beyond paq8px without look-ahead <= 0.002 on all four of sources 1-4.
- N3: bGPT text weights' G beyond standard paq8px >= 0.1 on gutenberg_en.
- N4: learners' G beyond standard paq8px > 0.002 on at least one of kmnist_images and fsdd_audio.
- S1: on the 8 text/code/formal benchmark labels of Battery 104, learners' G beyond paq8px without look-ahead
  <= 0.002 on at least 6 of 8.
Failed predictions are reported. Runner `probe/b106_modal.py` (`build`, then `score`, then `analyze`); output
`runs/battery/battery106.json`.
