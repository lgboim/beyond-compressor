"""Reproduce the paper's Table 1 gains (s = 0.01, 0.001 and exact Bayes) from the released files.

    python test_reproduce.py
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import beyond_compressor as bc  # noqa: E402

# Table 1 of the paper (evaluated ensembles, paq8px standard mode)
EXPECTED = json.load(open(HERE / "expected_table1.json"))


def main():
    man = bc.manifest()
    worst = 0.0
    for rowset, exp in EXPECTED.items():
        bits, retained, _ = bc.load_reference("paq8px_standard", rowset)
        p = np.load(HERE / man["reference_models"][rowset]["file"]).astype(np.float64)
        p = np.clip(p, 1e-30, None)[retained]
        q = np.exp2(-bits[retained])
        hq = -np.log2(q).mean(1)
        got = {"0.01": float((hq - bc.fixed_share(p, q, 0.01)).mean()),
               "0.001": float((hq - bc.fixed_share(p, q, 0.001)).mean()),
               "bayes": float((hq - bc.bayes(p, q)).mean())}
        for k, v in got.items():
            worst = max(worst, abs(v - exp[k]))
        print(rowset, {k: round(v, 6) for k, v in got.items()}, "rows", int(retained.sum()))
    print("max |difference| from the paper:", worst)
    assert worst < 1e-6, worst
    # sanity: a model identical to the compressor gains exactly 0; a uniform model gains >= -bound
    bits, retained, _ = bc.load_reference("paq8px_standard", "bench__metamath")
    q = np.exp2(-bits[retained])
    assert abs((-np.log2(q).mean(1) - bc.fixed_share(q, q, 0.001)).mean()) < 1e-9
    u = np.full_like(q, 1 / 256)
    g = (-np.log2(q).mean(1) - bc.fixed_share(u, q, 0.001)).mean()
    assert -bc.bound(0.001) - 1e-12 <= g <= 0, g
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
