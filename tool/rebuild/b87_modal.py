"""Battery 87: blind test on eight byte sources never examined in this project.
Protocol experiments/PROTOCOL_B87_heldout_sources.md.

    .venv-modal/bin/modal run probe/b87_modal.py::build      # download sources in the cloud, build rows (volume)
    .venv-modal/bin/modal run probe/b87_modal.py::score      # methods (CPU) and 24M learners (GPU), in parallel
    .venv/bin/python -m probe.b87_modal summary
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs/battery/b87"
SC = ROOT / "refs/official/scoring"
SOURCES = ("hewiki", "dewiki", "go_source", "fashion_mnist", "elf_x86_64", "uci_adult", "yesno_pcm16",
           "python_docs_html")
CAP, W, NROW = 8_388_608, 4095, 256
ROUNDS = (768, 1024, 1536, 5120, 5376, 5888, 6144, 8191)
SEEDS = tuple(f"seed-{40354564 + i}" for i in range(8))
METHODS = ("V_base", "V_auto", "V_match", "zlib", "lzma")
SHARE = 0.01
sys.path.insert(0, str(ROOT))

try:
    import modal
    build_image = modal.Image.debian_slim(python_version="3.11").pip_install("numpy", "pyarrow", "huggingface_hub")
    cpu_image = (modal.Image.debian_slim(python_version="3.11").pip_install("numpy")
                 .add_local_file(ROOT / "probe/__init__.py", "/root/probe/__init__.py")
                 .add_local_file(ROOT / "probe/white_box.py", "/root/probe/white_box.py")
                 .add_local_file(ROOT / "probe/white_box2.py", "/root/probe/white_box2.py")
                 .add_local_file(ROOT / "probe/white_box4.py", "/root/probe/white_box4.py")
                 .add_local_file(ROOT / "probe/white_box6.py", "/root/probe/white_box6.py"))
    gpu_image = (modal.Image.debian_slim(python_version="3.11").pip_install("torch", "numpy", "huggingface_hub")
                 .add_local_dir(SC / "src", "/scoring/src")
                 .add_local_file(SC / "score_from_hf.py", "/scoring/score_from_hf.py"))
    app = modal.App("b87-heldout")
    vol = modal.Volume.from_name("b87-heldout", create_if_missing=True)
    hf_cache = modal.Volume.from_name("b75-hf-cache", create_if_missing=True)

    def _get(url):
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research; byte-baselines)"})
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.read()

    def _docs(src):
        """(list of document bytes, provenance dict) for one source, exactly as the protocol specifies."""
        import gzip
        import hashlib
        import os
        import tarfile
        import wave
        import zipfile
        sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
        if src in ("hewiki", "dewiki"):
            import pyarrow.parquet as pq
            from huggingface_hub import hf_hub_download, list_repo_files
            cfg = "20231101." + src[:2]
            files = sorted(f for f in list_repo_files("wikimedia/wikipedia", repo_type="dataset")
                           if f.startswith(cfg + "/") and f.endswith(".parquet"))
            path = hf_hub_download("wikimedia/wikipedia", files[0], repo_type="dataset")
            raw = open(path, "rb").read()
            docs = [t.encode("utf-8") for t in pq.read_table(path, columns=["text"]).column("text").to_pylist()]
            return docs, {"file": files[0], "sha256": sha(raw)}
        if src == "go_source":
            raw = _get("https://go.dev/dl/go1.22.5.src.tar.gz")
            tf = tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz")
            mem = sorted((m for m in tf.getmembers() if m.isfile() and m.name.startswith("go/src/")
                          and m.name.endswith(".go")), key=lambda m: m.name)
            return [tf.extractfile(m).read() for m in mem], {"url": "go1.22.5.src.tar.gz", "sha256": sha(raw)}
        if src == "fashion_mnist":
            raw = _get("http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz")
            d = gzip.decompress(raw)[16:]
            return [d[i:i + 784] for i in range(0, len(d), 784)], {"url": "train-images-idx3-ubyte.gz", "sha256": sha(raw)}
        if src == "elf_x86_64":
            paths = []
            for root in ("/usr/bin", "/usr/lib/x86_64-linux-gnu"):
                for dp, _, fns in os.walk(root):
                    for fn in fns:
                        p = os.path.join(dp, fn)
                        if os.path.isfile(p) and not os.path.islink(p):
                            with open(p, "rb") as f:
                                if f.read(4) == b"\x7fELF":
                                    paths.append(p)
            paths.sort()
            docs = [open(p, "rb").read() for p in paths]
            return docs, {"n_files": len(paths), "sha256_concat": sha(b"".join(docs))}
        if src == "uci_adult":
            raw = _get("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data")
            return [ln + b"\n" for ln in raw.split(b"\n") if ln.strip()], {"url": "adult.data", "sha256": sha(raw)}
        if src == "yesno_pcm16":
            raw = _get("https://www.openslr.org/resources/1/waves_yesno.tar.gz")
            tf = tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz")
            docs, widths = [], set()
            for m in sorted((m for m in tf.getmembers() if m.isfile() and m.name.endswith(".wav")), key=lambda m: m.name):
                w = wave.open(io.BytesIO(tf.extractfile(m).read()))
                widths.add((w.getsampwidth(), w.getnchannels(), w.getframerate()))
                docs.append(w.readframes(w.getnframes()))
            return docs, {"url": "waves_yesno.tar.gz", "sha256": sha(raw), "formats": sorted(widths)}
        if src == "python_docs_html":
            raw = _get("https://docs.python.org/3.12/archives/python-3.12-docs-html.zip")
            zf = zipfile.ZipFile(io.BytesIO(raw))
            names = sorted(n for n in zf.namelist() if n.endswith(".html"))
            return [zf.read(n) for n in names], {"url": "python-3.12-docs-html.zip", "sha256": sha(raw)}
        raise ValueError(src)

    @app.function(image=build_image, cpu=4.0, memory=32768, timeout=3600, volumes={"/vol": vol})
    def build_source(src: str):
        import hashlib
        import numpy as np
        try:
            docs, prov = _docs(src)
        except Exception as e:                                    # dropped and reported, never replaced
            return {"source": src, "dropped": repr(e)}
        order = np.random.default_rng(870).permutation(len(docs))
        buf, n = [], 0
        for j in order:
            buf.append(docs[j])
            n += len(docs[j])
            if n >= CAP:
                break
        stream = b"".join(buf)[:CAP]
        step = (len(stream) - W) // (NROW - 1)
        X = np.stack([np.frombuffer(stream[i * step:i * step + W], np.uint8) for i in range(NROW)])
        Path("/vol/rows").mkdir(parents=True, exist_ok=True)
        np.save(f"/vol/rows/{src}.npy", X)
        vol.commit()
        return {"source": src, **prov, "n_docs": len(docs), "stream_bytes": len(stream), "step": int(step),
                "rows_sha256": hashlib.sha256(X.tobytes()).hexdigest()}

    @app.function(image=cpu_image, cpu=2.0, memory=16384, timeout=7200, volumes={"/vol": vol})
    def method_job(src: str, method: str):
        import importlib
        import lzma
        import zlib
        import numpy as np
        sys.path.insert(0, "/root")
        X = np.load(f"/vol/rows/{src}.npy").astype(np.int64)
        buf = io.BytesIO()
        if method in ("zlib", "lzma"):
            f = (lambda b: zlib.compress(b, 9)) if method == "zlib" else (lambda b: lzma.compress(b, preset=9))
            np.save(buf, np.array([8 * len(f(bytes(r.astype(np.uint8)))) / r.size for r in X]))
            return buf.getvalue()
        from probe.white_box import match_proposals
        prop, mlen = match_proposals(X)
        if method == "V_base":
            Wm = importlib.reload(importlib.import_module("probe.white_box2"))
            bits, _ = Wm.run(X, prop, mlen, Wm.VARIANTS["V_base"])
        elif method == "V_auto":
            Wm = importlib.reload(importlib.import_module("probe.white_box4"))
            bits, _ = Wm.run(X, prop, mlen)
        else:
            Wm = importlib.reload(importlib.import_module("probe.white_box6"))
            bits, _ = Wm.run(X, prop, mlen, gate=True, apm=True)
        np.save(buf, np.asarray(bits, np.float64).reshape(len(X), -1).astype(np.float32))
        return buf.getvalue()

    @app.function(image=gpu_image, gpu="A10G", timeout=3600,
                  volumes={"/vol": vol, "/root/.cache/huggingface": hf_cache})
    def learner_round(rnd: int, sources: list):
        import hashlib
        import numpy as np
        import torch
        sys.path.insert(0, "/scoring")
        import score_from_hf as S
        from huggingface_hub import hf_hub_download
        data = {s: torch.from_numpy(np.concatenate([np.full((NROW, 1), ord("O")),
                                                    np.load(f"/vol/rows/{s}.npy").astype(np.int64)], 1)).cuda()
                for s in sources}
        psum = {s: torch.zeros((NROW, W), dtype=torch.float64, device="cuda") for s in sources}
        per_seed, meta = {s: {} for s in sources}, []
        for sd in SEEDS:
            hf_path = f"24M/{sd}/learner_{rnd:04d}.pth"
            local = Path(hf_hub_download(repo_id=S.REPO, filename=hf_path))
            model = S.ProgramLanguageModel(**S.model_arch("ladder", "24M", hf_path))
            blob = torch.load(local, map_location="cpu", weights_only=False)
            r = model.load_state_dict(blob.get("learner_state_dict", blob.get("model_state_dict", blob)), strict=False)
            meta.append({"checkpoint": hf_path, "sha256": hashlib.sha256(local.read_bytes()).hexdigest(),
                         "missing_keys": list(r.missing_keys), "unexpected_keys": list(r.unexpected_keys)})
            model.eval().cuda()
            for m in model.modules():
                if hasattr(m, "_kernel_ok"):
                    m._kernel_ok = False
            with torch.inference_mode():
                for s in sources:
                    for lo in range(0, NROW, 8):
                        b = data[s][lo:lo + 8]
                        out = model(b[:, :-1])
                        lp = torch.log_softmax((out[0] if isinstance(out, tuple) else out).float(), -1)
                        p = lp.gather(-1, b[:, 1:, None])[..., 0].exp()
                        psum[s][lo:lo + 8] += p.double()
                        per_seed[s].setdefault(sd, []).extend((-torch.log2(p.clamp_min(1e-30))).mean(1).tolist())
            del model
            torch.cuda.empty_cache()
        hf_cache.commit()
        res = {"meta": meta, "torch": str(torch.__version__), "gpu": torch.cuda.get_device_name(0), "sources": {}}
        for s in sources:
            pe = (psum[s] / len(SEEDS)).clamp_min(1e-30).cpu().numpy()
            d = {"ens_row_bits": (-np.log2(pe)).mean(1).tolist(), "per_seed_row_bits": per_seed[s]}
            if rnd == 8191:
                b = io.BytesIO()
                np.save(b, pe.astype(np.float32))
                d["ens_probs"] = b.getvalue()
            res["sources"][s] = d
        return res

    @app.local_entrypoint()
    def build():
        OUT.mkdir(parents=True, exist_ok=True)
        prov = list(build_source.map(SOURCES))
        json.dump(prov, open(OUT / "build.json", "w"), indent=1)
        for p in prov:
            print(p, flush=True)
        print("BUILD DONE", flush=True)

    @app.local_entrypoint()
    def score():
        import numpy as np
        prov = json.load(open(OUT / "build.json"))
        srcs = [p["source"] for p in prov if "dropped" not in p]
        (OUT / "methods").mkdir(parents=True, exist_ok=True)
        (OUT / "learners").mkdir(parents=True, exist_ok=True)
        mjobs = [(s, m) for s in srcs for m in METHODS]
        mfut = [method_job.spawn(s, m) for s, m in mjobs]
        for rnd, r in zip(ROUNDS, learner_round.map(ROUNDS, kwargs={"sources": srcs})):
            for s, d in r["sources"].items():
                if "ens_probs" in d:
                    (OUT / "learners" / f"E24_probs__{s}.npy").write_bytes(d.pop("ens_probs"))
            json.dump(r, open(OUT / "learners" / f"r{rnd}.json", "w"))
            print("learners", rnd, flush=True)
        for (s, m), f in zip(mjobs, mfut):
            (OUT / "methods" / f"{m}__{s}.npy").write_bytes(f.get())
        print("SCORE DONE", flush=True)
except ImportError:
    pass


def summary():
    import numpy as np
    from probe.battery75 import ci
    prov = json.load(open(OUT / "build.json"))
    srcs = [p["source"] for p in prov if "dropped" not in p]
    res = {"dropped": [p for p in prov if "dropped" in p], "sources": {}}
    h = {"H1": 0, "H2": 0, "H3": 0, "H4": 0}
    for s in srcs:
        M = {m: np.load(OUT / "methods" / f"{m}__{s}.npy").astype(np.float64) for m in METHODS}
        rows = {m: (v.mean(1) if v.ndim == 2 else v) for m, v in M.items()}
        L = {r: np.array(json.load(open(OUT / "learners" / f"r{r}.json"))["sources"][s]["ens_row_bits"]) for r in ROUNDS}
        e24 = L[8191]
        best_r = min(ROUNDS, key=lambda r: L[r].mean())
        pe = np.load(OUT / "learners" / f"E24_probs__{s}.npy").astype(np.float64)
        pv = np.exp2(-M["V_match"])
        assert pe.shape == pv.shape == (NROW, W) and np.isfinite(pv).all()
        lw = np.full((NROW, 2), np.log(0.5))
        cb = np.empty((NROW, W))
        for t in range(W):
            w = np.exp(lw - lw.max(1, keepdims=True))
            w /= w.sum(1, keepdims=True)
            pk = np.stack([pe[:, t], pv[:, t]], 1)
            cb[:, t] = -np.log2((w * pk).sum(1))
            lw = lw + np.log(np.maximum(pk, 1e-300))
            w = np.exp(lw - lw.max(1, keepdims=True))
            w = (1 - SHARE) * w / w.sum(1, keepdims=True) + SHARE / 2
            lw = np.log(w)
        c_mix = cb.mean(1)
        better = min(e24.mean(), rows["V_match"].mean())
        r = res["sources"][s] = {m: float(v.mean()) for m, v in rows.items()}
        r.update({"E24": float(e24.mean()), "best24": float(L[best_r].mean()), "best24_round": best_r,
                  "all_rounds": {str(k): float(v.mean()) for k, v in L.items()}, "C_mix": float(c_mix.mean()),
                  "V_base_minus_E24": float((rows["V_base"] - e24).mean()), "ci_V_base_E24": ci(rows["V_base"] - e24, 871),
                  "V_match_minus_E24": float((rows["V_match"] - e24).mean()), "ci_V_match_E24": ci(rows["V_match"] - e24, 871),
                  "V_match_minus_best24": float((rows["V_match"] - L[best_r]).mean()),
                  "ci_V_match_best24": ci(rows["V_match"] - L[best_r], 871),
                  "C_mix_minus_better": float(c_mix.mean() - better)})
        h["H1"] += r["V_base_minus_E24"] < 0
        h["H2"] += r["V_match_minus_E24"] < 0
        h["H3"] += r["V_match_minus_best24"] < 0
        h["H4"] += r["C_mix_minus_better"] <= -0.02
        print(f"{s:18s} zlib {r['zlib']:.3f} lzma {r['lzma']:.3f} V_base {r['V_base']:.3f} V_auto {r['V_auto']:.3f} "
              f"V_match {r['V_match']:.3f} | E24 {r['E24']:.3f} best24 {r['best24']:.3f} (r{best_r}) | C_mix {r['C_mix']:.3f}")
    n = len(srcs)
    res["n_sources"] = n
    res["H1"] = {"count": int(h["H1"]), "pass": bool(h["H1"] >= 5)}
    res["H2"] = {"count": int(h["H2"]), "pass": bool(h["H2"] >= 6)}
    res["H3"] = {"count": int(h["H3"]), "pass": bool(h["H3"] >= 5)}
    res["H4"] = {"count": int(h["H4"]), "pass": bool(h["H4"] >= 5)}
    print({k: res[k] for k in ("n_sources", "H1", "H2", "H3", "H4")}, "dropped", res["dropped"])
    json.dump(res, open(ROOT / "runs/battery/battery87.json", "w"), indent=1)


if __name__ == "__main__" and "summary" in sys.argv:
    summary()
