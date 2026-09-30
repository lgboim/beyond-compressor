"""Realized gain of a byte-level model beyond an off-the-shelf compressor (paq8px or lpaq1), byte by byte.

Given a model's probability of each observed byte on the released evaluation windows, this script mixes it with the
compressor's logged per-byte probabilities in a sequential two-expert fixed-share mixture and reports the realized
gain G = mean over bytes of [-log2 q_t - (-log2 m_t)] in bits per byte (Elboim, 2026). Only numpy is required.

    python beyond_compressor.py list
    python beyond_compressor.py verify --rowset bench__metamath --rows my_rows.npy
    python beyond_compressor.py score  --rowset bench__metamath --probs my_model.npy [--rows my_rows.npy]
                                       [--reference paq8px_standard|paq8px_forced|lpaq1] [--share 0.001]

--probs: float array [n_windows, 4095]; entry [i, t] is the model's probability of byte t of window i given the
one-byte prefix 'O' and bytes 0..t-1 of that window (the benchmark's convention for model inputs; the compressors
were run on the raw 4095-byte windows without the prefix). Probabilities are used as given, without clipping. Windows must be in the
manifest order; --rows (uint8 or int array of the same shape) lets the script check every window's SHA-256.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LN2 = np.log(2.0)


def manifest():
    return json.load(open(HERE / "manifest.json"))


def load_reference(ref, rowset):
    m = manifest()["references"][ref][rowset]
    f = HERE / m["file"]
    if hashlib.sha256(f.read_bytes()).hexdigest() != m["sha256"]:
        raise SystemExit(f"checksum mismatch for {f}")
    z = np.load(f)
    return z["log_loss_bits"].astype(np.float64), z["retained"], z["window_sha256"]


def check_rows(rows, hashes):
    rows = np.asarray(rows)
    if rows.shape != (len(hashes), 4095):
        return [f"shape {rows.shape} != ({len(hashes)}, 4095)"]
    if not np.issubdtype(rows.dtype, np.integer):
        return [f"rows must be an integer array of byte values, got {rows.dtype}"]
    if rows.min() < 0 or rows.max() > 255:
        return ["rows must hold byte values in 0..255"]
    bad = [i for i, r in enumerate(rows) if hashlib.sha256(r.astype(np.uint8).tobytes()).hexdigest() != hashes[i]]
    return [f"{len(bad)} windows differ from the manifest (first: {bad[:5]})"] if bad else []


def fixed_share(p, q, share):
    """Per-window mean code length (bits) of the two-expert fixed-share mixture, equal initial weights,
    redistribution share/2 (identical to the paper's scorer)."""
    n, T = p.shape
    lw = np.full((n, 2), -np.log(2.0))
    bits = np.empty((n, T))
    for t in range(T):
        w = np.exp(lw - lw.max(1, keepdims=True))
        w /= w.sum(1, keepdims=True)
        pk = np.stack([p[:, t], q[:, t]], 1)
        bits[:, t] = -np.log2((w * pk).sum(1))
        l = lw + np.log(np.maximum(pk, 1e-300))
        w = np.exp(l - l.max(1, keepdims=True))
        w = (1 - share) * w / w.sum(1, keepdims=True) + share / 2
        lw = np.log(w)
    return bits.mean(1)


def bayes(p, q):
    """Exact equal-prior Bayesian mixture, from accumulated log-likelihoods (no underflow)."""
    lp = np.cumsum(np.log(p), 1)
    lq = np.cumsum(np.log(q), 1)
    total = np.logaddexp(lp[:, -1], lq[:, -1]) - np.log(2.0)
    return -total / LN2 / p.shape[1]


def bound(share, T=4095):
    return (1 - (T - 1) * np.log2(1 - share / 2)) / T if share > 0 else 1.0 / T


def score(args):
    if not 0 <= args.share < 1:
        raise SystemExit("--share must be in [0, 1); 0 selects the exact Bayesian mixture")
    if args.bootstrap < 1:
        raise SystemExit("--bootstrap must be at least 1")
    bits, retained, hashes = load_reference(args.reference, args.rowset)
    probs = np.load(args.probs).astype(np.float64)
    if probs.shape != bits.shape:
        raise SystemExit(f"--probs shape {probs.shape} != {bits.shape} for {args.rowset}")
    notes = []
    if args.rows:
        errs = check_rows(np.load(args.rows), hashes)
        if errs:
            raise SystemExit("row identity check failed: " + "; ".join(errs))
        notes.append("row identity verified (SHA-256 of every window)")
    else:
        notes.append("row identity NOT verified: pass --rows to check window hashes")
    ok = retained
    if not ok.any():
        raise SystemExit("no retained windows for this row set and reference")
    if not (np.isfinite(probs[ok]).all() and (probs[ok] > 0).all() and (probs[ok] <= 1).all()):
        raise SystemExit("--probs must be finite probabilities in (0, 1] on every retained window (values are used "
                         "as given, without clipping)")
    p = probs[ok]
    q = np.exp2(-bits[ok])
    hq = -np.log2(q).mean(1)
    rng = np.random.default_rng(args.seed)
    out = {"rowset": args.rowset, "reference": args.reference, "retained_windows": int(ok.sum()),
           "windows": int(len(ok)), "model_log_loss": float(-np.log2(p).mean()),
           "reference_log_loss": float(hq.mean()), "notes": notes, "gains": {}}
    def summary(g, s):
        boot = [g[rng.integers(0, len(g), len(g))].mean() for _ in range(args.bootstrap)]
        return {"G": float(g.mean()), "ci95": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
                "worst_case_bound": -float(bound(s))}
    for s in sorted({args.share, 0.01, 0.001} - {0.0}):
        out["gains"][f"fixed_share_{s}"] = summary(hq - fixed_share(p, q, s), s)
    out["gains"]["exact_bayes"] = summary(hq - bayes(p, q), 0.0)
    d0 = float(np.mean(p / q - 1) / LN2)
    out["static_convex_mixture"] = {"derivative_at_zero": d0,
                                    "optimal_weight_is_zero": bool(d0 <= 0),
                                    "note": "one corpus-wide weight; concave objective, so a nonpositive derivative "
                                            "at zero certifies weight 0 as the hindsight optimum over [0, 1]"}
    out["interpretation"] = ("G is realized log-loss reduction under this combiner, relative to the compressor's "
                             "logged probabilities; it is not a measure of information, and intervals are pointwise "
                             "window bootstraps.")
    print(json.dumps(out, indent=1))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    v = sub.add_parser("verify")
    v.add_argument("--rowset", required=True)
    v.add_argument("--rows", required=True)
    v.add_argument("--reference", default="paq8px_standard")
    s = sub.add_parser("score")
    s.add_argument("--rowset", required=True)
    s.add_argument("--probs", required=True)
    s.add_argument("--rows")
    s.add_argument("--reference", default="paq8px_standard", choices=["paq8px_standard", "paq8px_forced", "lpaq1"])
    s.add_argument("--share", type=float, default=0.001)
    s.add_argument("--bootstrap", type=int, default=1000)
    s.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    if a.cmd == "list":
        for ref, sets in manifest()["references"].items():
            print(ref, ":", ", ".join(f"{k} ({v['retained']}/{v['rows']})" for k, v in sets.items()))
    elif a.cmd == "verify":
        _, _, hashes = load_reference(a.reference, a.rowset)
        errs = check_rows(np.load(a.rows), hashes)
        print("OK: all windows match" if not errs else "FAIL: " + "; ".join(errs))
        sys.exit(1 if errs else 0)
    else:
        score(a)


if __name__ == "__main__":
    main()
