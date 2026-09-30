# Battery 79 protocol: does the 7-bit convention flatter language models on speech?

Frozen 2026-09-29 before any language model scored LibriSpeech; hashes recorded in AGENT_CHAT (C115) before running.
Inference only, on cloud GPUs (Ariel: "in parallel and efficiently, use the cloud if needed").

## Question

Delétang et al. (2024) score language models on audio after right-shifting every byte by one bit and rescale the
7-bit code length by 8/7 (released code), while FLAC codes all 8 bits. B78 measured, for our training-free
predictors, that the 8-bit rate is 3.2 points above the 7-bit convention on LibriSpeech. B79 measures the same gap
for open 7B language models, so that the effect of the convention on language models is measured instead of assumed.

## Models and data

- Mistral-7B-v0.1 (Apache-2.0, ungated; SentencePiece with byte fallback, the tokenizer family closest to Llama 2)
  and Qwen2.5-7B (Apache-2.0, ungated; byte-level BPE). bf16 weights, fp32 log-softmax.
- 2,000 chunks drawn without replacement from the 20,000 B78 chunks with `numpy.random.default_rng(790)`.
- 7-bit text: each byte b becomes the character chr(b >> 1) (0-127, ASCII). 8-bit text: chr(b) (0-255, Latin-1).
  Both maps are bijective. Each chunk is tokenised without special tokens and preceded by the model's BOS token
  (Mistral `<s>`; Qwen `<|endoftext|>`). Code length = sum of -log2 p(token) over the chunk's tokens. The fraction of
  chunks whose tokens decode back to exactly the input text is recorded.

## Readouts

Per model: L7/(7N) (the released code's convention), L8/(8N) (all 8 bits), (L7 + N)/(8N) (the paper's Appendix B
convention), the difference L8/(8N) - L7/(7N), and V_base's same three rates on the same 2,000 chunks (from B78),
with 95% bootstrap intervals over utterances (seed 792, 2000 draws).

## Predictions

- H1: for both models, the all-8-bit rate exceeds the 7-bit-convention rate by at least 2 points.
- H2 (pipeline sanity, not a claim about Llama 2): Mistral-7B's 7-bit-convention rate is within 3 points of the
  published Llama 2 7B value, 23.1%.

All outcomes are reported.
