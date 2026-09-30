# Battery 78 protocol: online training-free prediction on the LibriSpeech setting of "Language Modeling Is Compression"

Frozen 2026-09-29 before any LibriSpeech byte was downloaded or scored; hashes recorded in AGENT_CHAT (C109). Downloads
approved by Ariel ("download in the cloud and start"). No model is trained or run; only fixed online predictors and
classical compressors are scored.

## Target

Delétang et al. (ICLR 2024), Table 1 (arXiv v2, p. 6), LibriSpeech, 2048-byte chunks, raw compression rates:
gzip 38.5, LZMA2 38.2, PNG 37.6, FLAC 30.3, Llama 2 7B 23.1, Chinchilla 1B 24.9, 7B 23.6, 70B 21.0 (%). (The abstract
and README state 16.4% for Chinchilla 70B; we compare with the table and note the difference.)

## Data (rebuilt in the cloud)

The authors use TFDS `librispeech`, `train_clean100`, in dataset order, each utterance converted with
`audioop.bias(audioop.lin2lin(x, 2, 1), 1, 128)`, i.e. byte = ((sample >> 8) + 128) mod 256, split into consecutive
2048-byte chunks per utterance, trailing partial chunk dropped. We cannot reproduce their exact TFDS order (57 GiB
build), so we use a seeded sample of the same distribution: 3 of the 14 Hugging Face `openslr/librispeech_asr`
`clean/train.100` parquet shards chosen with `numpy.random.default_rng(780)`, utterances decoded to int16 with
soundfile, converted and chunked as above, utterances shuffled with `default_rng(781)`, and all chunks of successive
utterances taken until exactly 20,000 chunks (40,960,000 bytes).

## Methods and bit accounting

- Classical, as in the authors' `compress.py`: gzip (`compresslevel=9`), `lzma.compress` (defaults), FLAC via ffmpeg
  (u8, mono, 16 kHz, `-compression_level 12`); each chunk compressed separately, the one-byte-input header length
  subtracted from all but one chunk.
- Online predictors, frozen code, each chunk scored independently from an empty state: V_base (`white_box2`,
  frozen), V_auto (`white_box4`, frozen B77). Code length = sum of -log2 p over the chunk's bytes.
- Three rates for each online predictor: (i) full 8-bit, L8 / (8N), comparable with the classical rows; (ii) the
  released code's convention for language models on audio, where each byte is right-shifted by one bit and the
  7-bit code length is rescaled by 8/7: L7 / (7N), with L7 the predictor's code length on the shifted bytes; (iii) the
  paper's Appendix B convention, (L7 + N) / (8N). Language-model rows also pay about 2-4 bytes of arithmetic-coder
  termination per chunk; we report rates without and with +2 bytes per chunk.
- Uncertainty: 95% bootstrap over utterances (seed 782, 2000 draws), because chunks of an utterance are correlated.

## Predictions

- F1 (data fidelity): on our sample, chunked gzip and LZMA2 rates are within 1.5 points of the published 38.5 and
  38.2. If either fails, the sample is treated as a different distribution and every comparison below is descriptive.
- L1: V_base's full 8-bit rate is below FLAC's published chunked rate, 30.3%.
- L2: under the released code's convention, V_base's rate is below Llama 2 7B's 23.1%.
- L3: under the released code's convention, V_base's rate is below Chinchilla 70B's 21.0%.

All outcomes are reported. V_auto, the appendix convention, the +2-byte overhead and our own FLAC run are reported
descriptively.
