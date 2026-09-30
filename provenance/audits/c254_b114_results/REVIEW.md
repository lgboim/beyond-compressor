# C254: completed B114 audit

## Verdict

The completed saved artifacts are numerically admitted. **S0 passes; S1 passes; S2 and S3 fail**, exactly as in the submitted JSON. No numerical correction to that JSON is needed. Two descriptive ranges in the channel message need correction, and its proposed causal conclusion is stronger than the intervention supports.

The supported result is: **Within the full masked paq8px system, retaining direct inputs/routing from normal, match and word leaves nonpositive aggregate learner gain on all eight tested corpora under the specified fixed-share combiner. Removing the text group's direct mixer route also leaves nonpositive gain.** Shared text-derived state and adaptive mixing stages remain; this does not establish that the text model, language-related machinery, or other suppressed modules are dispensable as whole components.

## Artifact and numerical checks

- Submitted summary SHA256: `19b29a40f344ab471b559661966094ea88729f19cac088131863d959ecdb9355`.
- Analyzer SHA256: `cbe3b8d98a64c296122d055f845004f1012700ad3c919755f36fe4aa7ffd7231`, the C253 version whose malformed-input guards were separately verified.
- Exactly **928 expected part files**, covering **29 variants × 8 labels**, with no missing or extra files and correct per-part offsets and lengths. Every part has the pinned upstream commit, float32 arrays of the expected width, and matching metadata. Retained rows have finite nonnegative losses; excluded-row conventions are consistent. All archive sizes are positive integers, and logged main-coder bits fit within reported archive sizes. This is an accounting sanity check, not equality between log-loss and archive size.
- **59,218 variant-windows**: 29 × 2,042. All variants retain all input rows for all eight labels. Seven labels have 256 input windows each; ranked DCLM has 250, all retained. Thus S3's common-row and per-variant-population calculations use exactly the same windows.
- V0 equals B98 at every saved byte position on all **2,042 windows**, maximum absolute difference **0** and identical masks. Reported V0 archive sizes also match B98 for every window.
- Standard/forced equality was independently rechecked on the same completed B98/B106 inputs. Flags and all saved code lengths match the recorded diagnostic; this remains score equivalence, not an observed internal dispatch trace.
- Learner configuration and seed selection use the previously independently reconstructed B113 provenance. Every reused B88/B98/learner input was checked against that audit's hashes; none changed, and no averaged learner probability needed clipping.
- Independently recomputed gains with a log-space predict/observe/redistribute recurrence and recomputed all 2,000-resample window-bootstrap intervals using the recorded seed. **All 1,328 numeric fields** agree within 1e-10; largest absolute difference **9.063930161978817e-17**. All strings, booleans, counts and selected winners also match.
- The input manifest records **1,128 files** used by this audit. Sources, summary and protocols remained unchanged at the final source check.

The launcher log reports three container preemptions and an asynchronous-generator cleanup exception, followed by `B114 SCORE DONE 928` and exit 0. It contains no returned `FAILED` job record. The complete validated output inventory supports completion despite those infrastructure messages; “zero failed returned jobs” should not be expanded to “no execution errors occurred.” The log is preserved in the source snapshot.

## Frozen outcomes and descriptive values

| Test | Observed | Required | Result |
|---|---|---|---|
| S0 | exact V0/B98 equality and equal masks, eight labels | all rows and labels | pass |
| S1 | 14/14 tested single-group drops have G ≤ 0.002 on 8/8 labels | at least 12 drops, each on 6/8 labels | pass |
| S2 | K2 has G > 0.002 on 0/8 labels | at least 6/8 | fail |
| S3 | K2+record gives the largest mean reduction | K2+text largest | fail |

All values below are bits per byte and use the prescribed combiner.

- Single-drop G range: approximately **−0.000961851 to +0.000091855**.
- K2 G range: **−0.000957110 to −0.000821425**. No positive whole-label realized gain in any of the eight labels.
- S3 mean reduction: **K2+record +0.0000243175938476**, **K2+text −0.0000041757032341**. All eleven absolute reductions are below 0.00003. The rank remains the failed prespecified outcome; the small magnitude is a descriptive observation, not a reason to relabel the failure.
- K0 exceeds 0.002 on **3/8** labels: metamath **0.0055443232**, C source **0.0027339003**, Python **0.0020438829**. Python's result is just above the threshold; rounding it to 0.0020 must not change the count.
- K1 exceeds 0.002 on **1/8** labels: metamath **0.0034512716**.
- K2 increases compressor loss versus V0 by **0.000553022–0.065561900**, despite leaving incremental learner gain nonpositive. Equal small G is not equal compression performance.

### Corrections to C254 prose

1. **K0's H penalty over V0 is 0.062546769–0.315462649**, not 0.06–0.28. Metamath supplies the maximum; rounded range is about 0.06–0.32.
2. **D_text's H penalty is 0.009426819–0.014541246 on the seven unranked text/code/formal labels**. Ranked DCLM instead improves slightly: **−0.000781970**. Thus “raises H by 0.007–0.015” is not the all-eight-label result. D_text G is nonpositive on all eight, ranging **−0.000961851 to −0.000297344**.

## Interpretation boundary

The relevant intervention is **direct mixer inputs and weight-set routing muted while the complete adaptive system continues running**. It is neither a standalone order-n/match/word compressor nor whole-module deletion. In the generic path, PAQ_KEEP also mutes linear/similarity/exe direct routes; the 14 single drops are the prespecified tested groups, not every mechanism in paq8px.

The earlier pinned source inspection remains decisive:

- `TextModel.cpp:410–411,544` writes shared text state, including a model-order statistic after its context calculations.
- `SSE.cpp:286–293` consumes Text.mask, firstLetter and order, as well as WordModel.order and Match state.
- These calculations are not removed by the direct text-route mask. Constant-selected mixer banks also remain adaptive on surviving inputs.

Consequently, **“no single paq8px group is needed”** should become **“none of the 14 tested direct-route suppressions restored G above the prespecified threshold on these corpora.”**

Likewise, **“therefore the difference lies in the basic components, not the language-specific text model”** is not established. The experiment distinguishes a direct route from a whole system that retains indirect routes; it does not isolate basic-component engineering from shared text-derived state, calibration, or mixing. The narrower result weakens the hypothesis that the direct text-to-mixer route alone is necessary for the observed small incremental gain. It leaves the source of the lpaq1/paq8px difference unresolved.

For this two-expert share-0.001 mixture on length 4095, the reference-following path yields a worst-case gain bound near **−0.000965552**. The K2 gains lie near that bound. This explains the descriptive “near the floor” terminology, but does not prove information absence, statistical equivalence, or a lack of useful signals under other combiners. The 0.002 cutoff is the frozen decision threshold, not a universal significance bound.

Suggested result sentence:

> On all eight tested corpora, the specified masked paq8px configuration with direct normal, match and word inputs leaves no positive aggregate gain from the evaluated learners under the fixed-share combiner. Suppressing the direct text-group route also does not restore appreciable gain. Because shared text-derived state and adaptive mixing stages remain active, these results do not isolate which complete components explain the difference from lpaq1.

## Artifacts and scope

`check_results.py`, `RECOMPUTED.json`, `PER_WINDOW.json`, `CHECKS.json`, `DESCRIPTIVE_RANGES.json`, `INPUT_MANIFEST.json`, and `SOURCE_MANIFEST.json` retain the evidence. The first checker invocation had a syntax error in a dictionary key and stopped before execution; after that was corrected, the complete checker succeeded. No experiment source, frozen protocol, reference material or run output was changed. No training, inference, compressor execution, download, or cloud job was started by this audit.

This is verification of the saved completed results and documented instrument. It does not independently attest the remote compiler/environment or every group-specific worker environment variable, which are not embedded in the part files. The S0 identity check, preserved patch hashes and recorded worker source provide the available provenance; no stronger execution attestation is claimed.
