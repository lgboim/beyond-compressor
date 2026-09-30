# B117 corrections, recorded after the results; the frozen protocol and the frozen compressor are unchanged

1. Count. LPAQ_UP=126975 turns on 16 switches (bits 0-11 and 13-16: U1-U5, orders 5/7, word bigram, sparse, SSE by
   match length, indirect, column, initial weights 2.1/N, SSE by previous byte, structure, extra sparse, key), not
   "fifteen" as the protocol text says. The instrument is fixed exactly by the source hash and LPAQ_UP value.
2. The switch 8192 SSE is keyed by the previous byte and the bits of the current byte ((c4 & 0xff) << 8 | c0), not by
   "the last two bytes" as the source comment says.
3. Denominators (Codex C1235): paq8px in standard mode retained 1/256 en_books windows and 255/256 haskell_pandoc
   windows (F and R0 retained all). C3 holds only on reference-specific retained subsets and is uninformative for
   en_books; every en_books window contains CR bytes, which paq8px's text preprocessing changes (descriptive).

## Addendum, 2026-09-29 (C2001 reader review, verified by Codex C1241)

4. Item 3's explanation is withdrawn as unsupported. All 256 book windows contain carriage returns (61 to 140,
   median 82), including the one window standard mode retained (row 76, 83 CRs); the excluded Haskell window (row 214)
   contains no CR (and two non-ASCII bytes). CR presence therefore does not discriminate retained from excluded
   windows, and the causes of the standard-mode exclusions are not identified (a conditional CR-related transform is
   not ruled out). The exclusions, the C3 limitation and C1, C2, C4 are unchanged.
