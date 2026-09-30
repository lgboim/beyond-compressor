# Provenance

- `protocols/`: every protocol behind Appendices F and G (Batteries 75 to 117), plus the Battery 114 amendment and the
  Battery 115 and 117 correction files. Frozen protocol files are unchanged; corrections are separate files.
- `PROTOCOL_INDEX.json`: for each file in `protocols/`, its full SHA-256, and for the 42 primary protocols the ID and
  agent-written UTC timestamp of the project-log message that first recorded that hash (message bodies are not released). Timestamps are written by the AI agents in the log; they document an internal
  sequence of declared freezes, not an external preregistration. Smoke results seen before freezing, amendments and
  departures are reported in Appendices F and G of the paper.
- `PROTOCOL_INVENTORY_c2002_prerepair.json`: Codex's historical inventory, taken before this folder existed (its
  `in_public` fields and `experiments/` paths describe the earlier package); kept unchanged for the record.
- `audits/`: the audit reports cited in Appendix F.2 (with the two attachments it names) and those for Batteries 113 to
  117, written by Codex (OpenAI), an AI system that reviewed code and recomputed saved results while preserving the
  original experimental artifacts. They are internal checks, not independent replication.

Boundary: this folder releases the protocols and the report texts. The reports' supporting check scripts,
recomputations and intermediate arrays, and the project log itself, are kept by the author and are available on
request. Reproduction from released files is covered by `tool/test_reproduce.py` (Table 1).
