# Protocol B99: a natural-data yardstick (bGPT)

Frozen before any B99 output exists. Inference only, on Modal GPUs, of the released bGPT weights (Wu et al.,
2024, "Beyond Language Models: Byte Models are Digital World Simulators"; Hugging Face `sander-wood/bgpt`, MIT
license): `weights-text.pth` (Wikipedia, extension txt), `weights-image.pth` (ImageNet, bmp) and
`weights-audio.pth` (LibriSpeech, wav). Downloaded to a Modal volume only; SHA-256 recorded.

## Scoring

Each window of the 34 Battery 88 row sets is presented in bGPT's own file format: a first patch holding the
extension bytes padded with 256, then the 4095 window bytes padded with 256 to 4096; the patch decoder's
feature for patch j predicts the 16 bytes of patch j+1 through the byte decoder (the model's own training
factorization). The probability of each true byte is renormalized over the 256 byte values (the end/padding
symbol excluded, since every window continues). Parameter loading follows the released inference script
(GPT2 configurations as released); missing parameter names must be empty.

Caveats fixed now: bGPT has about 110M parameters (4-5 times the largest self-play learner) and a different
architecture; our windows lack file headers (BMP, WAV) that bGPT saw in training; Wikipedia may overlap web
text. B99 is a yardstick, not a matched comparison.

## Measures

M: Battery 94 fixed-share rule. For each row set, with the learners' ensemble as in Battery 98:
G_selfplay = M(V_auto, V_match) - M(ensemble, V_auto, V_match); G_bgpt_w likewise with bGPT weight w in place of
the ensemble; G_bgpt_best = max over the three weights. ratio = G_selfplay / G_bgpt_best where G_bgpt_best > 0.01.

## Gate and predictions

- Gate: text weights' own loss on dclm below 2.5 bits per byte, and no missing parameter names.
- Y1: on the four natural-text labels (dclm, dclm_ranked, llm_compression_cc, kolmogorov_text) G_bgpt_text is at
  least 10 times G_selfplay on all four.
- Y2: the median ratio over structured sources {elf_x86_64, uci_adult, cifar10_rgb_hwc, cifar10_rgb_planar,
  fashion_mnist} exceeds the median ratio over natural text {the four text labels, hewiki, dewiki}.

Failed predictions are reported. Runner `probe/b99_modal.py` (`score`, then `analyze`); output
`runs/battery/battery99.json`.
