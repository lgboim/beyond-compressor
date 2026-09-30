# Protocol B117: does the frozen basic compressor absorb the learners on new sources?

Frozen before any byte of the new sources is downloaded and before any B117 score exists. Inference and compression
only (learner inference on Modal GPU, paq8px on Modal CPU, the basic compressor locally). Authorized by Ariel ("תנסה
עד שינצח אותם"; cloud allowed earlier in this thread).

## The frozen compressor F

`probe/b117_frozen/lpaq1_frozen.cpp`, SHA-256 0b670427861aa6d562099f00e78f3d6d96f4d8dcb0026366cff94ca5347387f7
(identical to the B116 development source), run as `lpaq1_frozen 4 in out` with `LPAQ_MASK=127 LPAQ_UP=126975`.
It is lpaq1 with fifteen generic upgrades chosen during the exploratory B116 development on 12 already-seen row sets
(ledger `runs/battery/b116/ledger.jsonl`, 18 variants; the selected variant is the only one with G <= 0.002 on all
12). With `LPAQ_UP=0` the same binary is the original lpaq1 (byte-identical output), used as the reference R0.

## A. New sources (selected now, never used in this project; public; no terms to accept)

1. en_books: Project Gutenberg plain texts 11, 1661 and 98, concatenated in that order
   (https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt).
2. cpp_json: all *.hpp files of https://github.com/nlohmann/json/archive/refs/tags/v3.11.3.tar.gz, sorted by path.
3. java_gson: all *.java files of https://github.com/google/gson/archive/refs/tags/gson-parent-2.11.0.tar.gz, sorted
   by path.
4. rst_flask: all *.rst files of https://github.com/pallets/flask/archive/refs/tags/3.0.3.tar.gz, sorted by path.
5. yaml_linguist: https://raw.githubusercontent.com/github-linguist/linguist/v7.30.0/lib/linguist/languages.yml
6. haskell_pandoc: all *.hs files of https://github.com/jgm/pandoc/archive/refs/tags/3.1.13.tar.gz, sorted by path.

Each stream is capped at 8 MB, cut into consecutive 4095-byte windows, and 256 windows are drawn without replacement
with numpy seed 1170 (all windows if fewer). Download SHA-256 and file lists are recorded before scoring. If a URL
cannot be downloaded, that source is dropped and reported, with no replacement, and the counts below refer to the
sources that were built.

## B. Models and references

Learners: E24 (24M, round 8191, the 8 released seeds, mean of probabilities), as in Batteries 87 and 106. References:
F; R0 (original lpaq1); paq8px commit c84f576, level -8, standard mode, Battery 98 logging patch. Windows are used when
a reference's logged bytes equal the window bytes.

## Measure

G = mean[-log2 p_C - bits of M_0.001(x, p_C)] (the paper's two-expert fixed share 0.001), with pointwise
window-bootstrap intervals; H = mean own code length. No rounding in pass/fail decisions.

## Predictions (n = number of sources built)

- C1: G beyond F <= 0.002 on at least n - 1 sources.
- C2: F's mean code length is below the learners' on all n sources.
- C3: G beyond paq8px <= 0.002 on all n sources.
- C4: G beyond R0 > 0.002 on at least ceil(2n/3) sources.

Failed predictions are reported. Runners `probe/b117_modal.py` (`build`, `score`) and `probe/battery117.py`
(`code`, `summary`); output `runs/battery/battery117.json`.
