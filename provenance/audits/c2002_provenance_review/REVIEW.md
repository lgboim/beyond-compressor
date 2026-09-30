# C2002 provenance proposal and C269 trim review

2026-09-29. Ownership C1246. This review inventories local staged files and
checks selected log messages. It does not approve a new appendix, rebuild a
release, publish the channel, authorize compute or verify provider billing.

## Confirmed material gap: the staged supplement is behind the manuscript

Appendix F.2 currently says “audit records are in the supplement.” The inspected
stage directory and ZIP have the same 149 file paths. Their 20 protocol files
comprise the paired-suite protocol, a B75 amendment, and the 18 primary protocols
B75–B92. They contain none of the 24 primary protocols B93–B115 and B117.
B116 is exploratory and must not be assigned a nonexistent frozen protocol.

All 42 main protocol files referenced across F/G exist locally, their complete
SHA-256 values match the printed prefixes, and their full hashes are found in
the channel. The 18 primary protocols present in the ZIP match the local hashes.
`PROTOCOL_INVENTORY.json` supplies each full hash, path, package presence and
the first full-hash message reference. The file explicitly labels timestamps
as agent-written, not external preregistration evidence.

All **17 distinct Markdown audit reports directly named in F.2** exist locally;
none is in the ZIP/stage or current public repository. These are a minimum
cited-report count, not the total number of required audit attachments. The
adjunct parity/correction/check JSONs, amendments and later G reports also need
coverage in a complete package. The public repository has none of the 42 main
protocol files or these 17 reports. Its passing 30-file hash manifest certifies
integrity of its listed files, not completeness against the manuscript.

This is a real staged-package availability gap. It does not change an
experimental result and does not imply that missing records do not exist.
Before an external release, align F.2's availability statement with a verified
package inventory. A process appendix can be decided separately. C2002's
suggestion to include reports and check files is useful, but a usable evidence
bundle should also index the cited amendments, original/corrected outputs,
recomputation scripts and input-hash records needed to interpret those reports.
No bundle was copied into the public tree in this review.

## Process account: supported points and needed limits

The selected announcement dates in C2002 agree with the channel messages:

| Stage | Message | Agent-written UTC |
|---|---|---|
| B75 protocol | C094 | 2026-09-29 07:18:44 |
| B87 fresh-source protocol | C131 | 2026-09-29 10:38:04 |
| B88 compressor comparison | C133 | 2026-09-29 11:04:27 |
| B93 complementarity scaling test | C152 | 2026-09-29 13:28:32 |
| B98/B99 protocols | C164 | 2026-09-29 14:01:02 |
| B100 low-overhead combiner test | C169 | 2026-09-29 14:14:53 |
| B106 fresh-source protocol | C184 | 2026-09-29 15:05:28 |
| B110–B112 protocols | C215 | 2026-09-29 16:18:53 |
| B113/B114 protocols | C250 | 2026-09-29 18:19:35 |
| B115 protocol | C255 | 2026-09-29 18:45:19 |
| B116 exploratory declaration | C257 | 2026-09-29 18:50:56 |
| B117 prospective protocol | C258 | 2026-09-29 18:58:33 |

These are announcement records, not verified start/completion times or a proof
that no output had previously been seen. The first-full-hash ledger similarly
records an observed mention rather than certifying a freeze. Preserve B100's
adaptation after B98, B114's later amendment, B115's prior own-loss smoke and
B116's exploratory status. Full hashes authenticate content, not time. A later
deposit cannot authenticate earlier freeze times. A local append-only convention
is not an externally enforced append-only history.

At the end of the agent-written 19:47 minute, the log has 263 Claude and 249 Codex
entries, matching C2002's 512. This is a disposable snapshot count, not a count
of experiments, independent reviewers or distinct scientific confirmations.
The same speaker labels cover more than one session; C2001 explicitly describes
a second Claude session. Battery numbers likewise do not imply 117 training
runs, independent experiments, or one uninterrupted two-day study. First log
entry/date and paper access dates alone cannot establish the whole project's
start or compute duration.

Two proposal phrases need narrowing:

- **“Only B106 and B117 are fresh-source tests”** is correct only for that
  follow-up scope. B87 was also fixed before new-source download (C131), and
  is already described in the current Appendix B. Do not erase it when
  describing the whole project.
- **“G first defined at B93”** should be “B93 tests scaling of gain beyond
  V_match.” B86 already defines the fixed-share learner/reference mixture
  and its complementarity criterion (protocol lines 11–21). B93's own message
  explicitly refers back to the B86 mixture. This review does not claim the
  first historical occurrence of a variable name.

The current paper concerns inference/compression and saved-array analyses.
The broader project also contains earlier local training and tape/head studies,
as the older combined draft explains. Thus “no self-play training” must be
scoped to the current paper's evaluated released models, not the entire
research history. Earlier-stage numeric IDs are a scope/indexing issue; they
are not evidence by themselves of selectively hidden failures. A retrospective
table may document the evolution, but cannot convert exposed-data development
into preregistered confirmation.

The proposed roles are consistent with the disclosed internal workflow, but
“Codex audited read-only” should mean no edits to owner scientific runs/source:
Codex also wrote audit scripts, reports and channel infrastructure, and made
bounded verification fixtures. Clarify that AI-assisted audit/recomputation is
internal checking, not independent replication. There is no need to imply
separate human auditors from message counts or audit-folder names.

Hardware/cloud descriptions have documentary support in the project notes and
runner records, not a new hardware-utilization or billing audit here. The log
explicitly attributes USD 0.82 to an author-reported **B75-only** provider
readout and says later cloud work is excluded. Do not supply that as total
study cost or infer a total from it. I did not inspect an account or verify
the proposal's exact FINDINGS heading counts, all pre-B75 predictions, or a
project-wide runtime/cost total.

## C269 is closed within the already reviewed scope

Its caption and discussion changes were already captured by C1245. The new
White sentence preserves the data-snooping attribution and separation of
prespecified/post-hoc analyses and sources fixed before download. All 15
outreach blockquotes still match the assembled manuscript after whitespace
normalization. No numerical rerun or new claim review is needed for that trim.

## Evidence and scope

`check_coverage.py`, `CHECKS.json`, `PROTOCOL_INVENTORY.json`,
`AUDIT_AVAILABILITY.json`, `PACKAGE_PATHS.json`, `CHRONOLOGY_MESSAGES.json`,
`SOURCE_MANIFEST.json` and snapshots under `sources/`. The chronology messages
are preserved locally as audit evidence; this is not permission to publish
the raw channel. The optional Appendix H decision remains Ariel's. The
staged-package completeness finding is independently actionable within the
owner's release preparation, with no new scientific experiment required.
