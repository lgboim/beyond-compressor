# B114 amendment 1 (clarifications from Codex C1222/C1223), recorded before any B114 outcome was computed

The frozen protocol (PROTOCOL_B114_paq8px_ablation.md, sha256 d0bc759d...58f2) is unchanged. Only the 4-window smoke
test (V0 max |diff| vs B98 = 0; D_normal and K2 differ) had been seen; the 928-job run was in progress and unread.

1. Interpretation. A neutral-mode drop removes a group's direct mixer inputs and its weight-set routing inside the
   complete adaptive compressor; it does not delete a self-contained module. The final SSE stage (SSE.cpp) still reads
   Text (mask, first letter, order), WordModel order and Match state when those groups are muted, and Mixer::set(0,
   range) keeps one adaptive weight set for the surviving inputs. K2 is therefore "paq8px with only the normal, match
   and word groups feeding the mixer directly", not a clean lpaq1-like compressor. The frozen sentence "this biases the
   test toward understating a group's importance" is withdrawn: indirect routes remain and the direction of bias is
   not established.
2. Scorer. Parts are validated before use (offsets 0, 64, ... contiguous; total rows equal the Battery 88 rows; one
   commit, c84f576; 4095 columns). S0 is computed first over all rows of all eight labels, and S1-S3 are reported as
   inadmissible if S0 fails.
3. S3 is computed on common paired rows (retained in V0, K2 and all eleven K2+g variants); the per-variant-rows
   version is reported as a sensitivity.
4. Active path. Whether windows ran on a wrapped path (ContextModelText or ContextModelGeneric) is checked with the
   Battery 106 standard/forced identity: forced mode was -forcetext (text path) for the seven ASCII labels and
   -forcebinary (generic path) for dclm_ranked; a label is on the wrapped path if its Battery 98 standard-mode code
   lengths equal the forced-mode ones on every common retained byte. A label where this fails is flagged.
