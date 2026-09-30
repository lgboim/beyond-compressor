# B115 corrections (Codex C1230), recorded after the run; the frozen protocol is unchanged

1. U3 selects the mixer weight set by order/match-length state only: 10 states (order 0-4 without a match, 5-9 with
   a match), not 8 as the frozen text says; the original uses 80.
2. lpaq1 is not free of text-specific rules: it has an ASCII word context (A-Z lowered to a-z, a hash of the current
   run of letters, reset on any other byte). It lacks paq8px's dedicated morphology/Text module (stemmers, language
   detection), not all text-specific structure.
3. The constructive route tests an alternative instrument; it does not by itself attribute the original lpaq1/paq8px
   gap to specific paq8px components.
