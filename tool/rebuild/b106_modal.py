"""Battery 106: prospective new sources and paq8px without look-ahead. Protocol
experiments/PROTOCOL_B106_prospective_sources.md.

    .venv-modal/bin/modal run probe/b106_modal.py::build      # download + windows (cloud CPU)
    .venv-modal/bin/modal run probe/b106_modal.py::score      # paq8px (2 modes), E24, bGPT
    .venv/bin/python -m probe.b106_modal analyze
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SC = ROOT / "refs/official/scoring"
OUT = ROOT / "runs/battery/b106"
COMMIT = "c84f576fc2c522194cd320743708652a154daf6b"
SOURCES = ("gutenberg_en", "rust_ripgrep", "js_lodash", "json_countries", "kmnist_images", "fsdd_audio")
TEXTLIKE_NEW = ("gutenberg_en", "rust_ripgrep", "js_lodash", "json_countries")
FORCETEXT = {"dclm", "llm_compression_cc", "kolmogorov_text", "llm_compression_python", "aitdcc_b_c_source",
             "llm_compression_arxiv_math", "metamath", "hewiki", "dewiki", "go_source", "python_docs_html", "uci_adult",
             *TEXTLIKE_NEW}
BGPT_W = {"gutenberg_en": "text", "rust_ripgrep": "text", "js_lodash": "text", "json_countries": "text",
          "kmnist_images": "image", "fsdd_audio": "audio"}
WIN, NWIN, CAP, SEED = 4095, 256, 8 * 1024 * 1024, 1060
sys.path.insert(0, str(ROOT))

try:
    import modal
    app = modal.App("b106-prospective")
    cpu_image = modal.Image.debian_slim(python_version="3.11").pip_install("numpy")

    @app.function(image=cpu_image, cpu=2.0, memory=8192, timeout=3600)
    def build_source(src: str):
        import hashlib
        import tarfile
        import urllib.request
        import wave
        import numpy as np
        prov = {"downloads": []}

        def get(url):
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research; byte-level evaluation)"})
            data = urllib.request.urlopen(req, timeout=300).read()
            prov["downloads"].append({"url": url, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
            return data

        def tar_files(url, ext):
            tf = tarfile.open(fileobj=io.BytesIO(get(url)), mode="r:gz")
            mem = sorted((m for m in tf.getmembers() if m.isfile() and m.name.endswith(ext)), key=lambda m: m.name)
            prov["n_files"] = len(mem)
            return [(m.name, tf.extractfile(m).read()) for m in mem]
        if src == "gutenberg_en":
            stream = b"".join(get(f"https://www.gutenberg.org/cache/epub/{i}/pg{i}.txt") for i in (2701, 1342, 84))
        elif src == "rust_ripgrep":
            stream = b"".join(d for _, d in tar_files("https://github.com/BurntSushi/ripgrep/archive/refs/tags/14.1.1.tar.gz", ".rs"))
        elif src == "js_lodash":
            stream = b"".join(d for _, d in tar_files("https://github.com/lodash/lodash/archive/refs/tags/4.17.21.tar.gz", ".js"))
        elif src == "json_countries":
            stream = get("https://raw.githubusercontent.com/mledoze/countries/master/countries.json")
        elif src == "kmnist_images":
            z = np.load(io.BytesIO(get("http://codh.rois.ac.jp/kmnist/dataset/kmnist/kmnist-train-imgs.npz")))
            stream = z[z.files[0]].astype(np.uint8).tobytes()
        elif src == "fsdd_audio":
            parts = []
            for _, d in tar_files("https://github.com/Jakobovski/free-spoken-digit-dataset/archive/refs/tags/v1.0.10.tar.gz", ".wav"):
                w = wave.open(io.BytesIO(d))
                raw = w.readframes(w.getnframes())
                if w.getsampwidth() == 2:
                    s = np.frombuffer(raw, "<i2").astype(np.int32)
                    parts.append((((s >> 8) + 128) % 256).astype(np.uint8).tobytes())
                else:
                    parts.append(raw)
            stream = b"".join(parts)
        else:
            raise ValueError(src)
        prov["stream_bytes"] = len(stream)
        stream = stream[:CAP]
        n = len(stream) // WIN
        idx = np.random.default_rng(SEED).choice(n, min(NWIN, n), replace=False)
        idx.sort()
        rows = np.frombuffer(stream, np.uint8)[: n * WIN].reshape(n, WIN)[idx]
        prov.update({"capped_bytes": len(stream), "n_windows_total": int(n), "window_index": idx.tolist()})
        buf = io.BytesIO()
        np.save(buf, rows)
        return {"rows": buf.getvalue(), "prov": prov}

    @app.local_entrypoint()
    def build():
        import numpy as np
        (OUT / "rows").mkdir(parents=True, exist_ok=True)
        (OUT / "data").mkdir(parents=True, exist_ok=True)
        prov = {}
        for src, r in zip(SOURCES, build_source.map(SOURCES)):
            rows = np.load(io.BytesIO(r["rows"]))
            np.save(OUT / "rows" / f"new__{src}.npy", rows)
            with open(OUT / "data" / f"{src}.jsonl", "w") as f:
                for row in rows:
                    f.write(json.dumps({"sequence": row.tolist()}) + "\n")
            prov[src] = r["prov"]
            print(src, rows.shape, r["prov"]["stream_bytes"], flush=True)
        json.dump(prov, open(OUT / "provenance.json", "w"), indent=1)
        print("B106 BUILD DONE", flush=True)

    paq_image = (modal.Image.debian_slim(python_version="3.11")
                 .apt_install("git", "build-essential", "cmake", "zlib1g-dev")
                 .run_commands("git clone https://github.com/hxim/paq8px.git /paq",
                               f"cd /paq && git checkout {COMMIT} && git rev-parse HEAD > /paq/COMMIT")
                 .pip_install("numpy")
                 .add_local_file(ROOT / "probe/b98_paq/Encoder.cpp", "/tmp/Encoder.cpp", copy=True)
                 .run_commands("cp /tmp/Encoder.cpp /paq/src/Encoder.cpp",
                               "cd /paq && mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j8")
                 .add_local_dir(ROOT / "runs/battery/b88/rows", "/rows_b88")
                 .add_local_dir(OUT / "rows", "/rows_new"))

    @app.function(image=paq_image, cpu=1.0, memory=4096, timeout=3600)
    def paq_job(name: str, lo: int, mode: str):
        import glob
        import os
        import subprocess
        import tempfile
        import numpy as np
        paq = sorted([p for p in glob.glob("/paq/build/paq8px*") if not p.endswith((".o", ".a", ".cmake"))], key=len)[0]
        d = "/rows_new" if os.path.exists(f"/rows_new/{name}.npy") else "/rows_b88"
        X = np.load(f"{d}/{name}.npy")[lo:lo + 32]
        lab = name.split("__", 1)[1]
        flag = [] if mode == "std" else (["-forcetext"] if lab in FORCETEXT else ["-forcebinary"])
        wd = tempfile.mkdtemp()
        bits = np.full(X.shape, np.nan, np.float32)
        info = []
        for i, r in enumerate(X):
            for f in glob.glob(f"{wd}/w*") + glob.glob(f"{wd}/log.bin"):
                os.remove(f)
            open(f"{wd}/w", "wb").write(bytes(r))
            subprocess.run([paq, "-8", *flag, "w"], cwd=wd, check=True, capture_output=True,
                           env={**os.environ, "PAQ_BITLOG": f"{wd}/log.bin"})
            size = os.path.getsize(glob.glob(f"{wd}/w.paq8px*")[0])
            rec = np.fromfile(f"{wd}/log.bin", dtype=np.dtype([("main", "u1"), ("c", "u1"), ("b", "<f4")]))
            m = rec[rec["main"] == 1]
            aligned = len(m) == len(r) and bool((m["c"] == r).all())
            if aligned:
                bits[i] = m["b"]
            info.append({"size": size, "aligned": aligned, "main_bits": float(m["b"].astype(np.float64).sum()),
                         "other_bits": float(rec["b"][rec["main"] == 0].astype(np.float64).sum())})
        buf = io.BytesIO()
        np.save(buf, bits)
        return {"bits": buf.getvalue(), "info": info, "commit": open("/paq/COMMIT").read().strip(), "flag": flag}

    gpu_image = (modal.Image.debian_slim(python_version="3.11")
                 .pip_install("torch", "numpy", "huggingface_hub", "transformers==4.44.2")
                 .add_local_dir(SC / "src", "/scoring/src")
                 .add_local_file(SC / "score_from_hf.py", "/scoring/score_from_hf.py")
                 .add_local_dir(OUT / "data", "/data_new")
                 .add_local_dir(OUT / "rows", "/rows_new"))
    hf_cache = modal.Volume.from_name("b75-hf-cache", create_if_missing=True)
    bgpt_vol = modal.Volume.from_name("b99-bgpt-weights", create_if_missing=True)

    @app.function(image=gpu_image, gpu="A10G", timeout=3600, volumes={"/root/.cache/huggingface": hf_cache})
    def learner_job(seed: str):
        import hashlib
        import numpy as np
        sys.path.insert(0, "/scoring")
        import score_from_hf as S
        from huggingface_hub import hf_hub_download
        corpora, prov = S.load_corpora(Path("/data_new"), list(SOURCES), 256, "cuda")
        rel = f"24M/{seed}/learner_8191.pth"
        local = Path(hf_hub_download(repo_id=S.REPO, filename=rel))
        p = S.seed_probs(local, S.model_arch("ladder", "24M", rel), corpora, "cuda", 16)
        hf_cache.commit()
        buf = io.BytesIO()
        np.savez_compressed(buf, **{s: p[s].astype(np.float32) for s in SOURCES})
        return {"bytes": buf.getvalue(), "sha256": hashlib.sha256(local.read_bytes()).hexdigest(), "corpora": prov}

    @app.function(image=gpu_image, gpu="A10G", timeout=3600, volumes={"/w": bgpt_vol})
    def bgpt_job(weight: str, names: list):
        import numpy as np
        import torch
        import torch.nn.functional as F
        from huggingface_hub import hf_hub_download
        from transformers import GPT2Config, GPT2LMHeadModel, GPT2Model
        PATCH, PLEN, HID = 16, 512, 768
        files = {"text": ("weights-text.pth", "txt"), "image": ("weights-image.pth", "bmp"), "audio": ("weights-audio.pth", "wav")}
        pc = GPT2Config(num_hidden_layers=12, max_length=PLEN, max_position_embeddings=PLEN, hidden_size=HID,
                        n_head=HID // 64, vocab_size=1)
        bc = GPT2Config(num_hidden_layers=3, max_length=PATCH + 1, max_position_embeddings=PATCH + 1, hidden_size=HID,
                        n_head=HID // 64, vocab_size=257)

        class M(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.patch_level_decoder = torch.nn.Module()
                self.patch_level_decoder.patch_embedding = torch.nn.Linear(PATCH * 257, HID)
                self.patch_level_decoder.base = GPT2Model(pc)
                self.byte_level_decoder = torch.nn.Module()
                self.byte_level_decoder.base = GPT2LMHeadModel(bc)
        m = M()
        path = hf_hub_download(repo_id="sander-wood/bgpt", filename=files[weight][0], cache_dir="/w", local_files_only=True)
        missing, _ = m.load_state_dict(torch.load(path, map_location="cpu", weights_only=False)["model"], strict=False)
        m = m.eval().cuda()
        ext = list(files[weight][1].encode()) + [256] * (PATCH - len(files[weight][1]))
        out = {}
        with torch.inference_mode():
            for n in names:
                X = np.load(f"/rows_new/new__{n}.npy").astype(np.int64)
                ps = []
                for lo in range(0, len(X), 8):
                    x = X[lo:lo + 8]
                    b = len(x)
                    seq = np.concatenate([np.tile(ext, (b, 1)), x, np.full((b, 1), 256)], 1)
                    pt = torch.tensor(seq, device="cuda").reshape(b, -1, PATCH)
                    oh = F.one_hot(pt, 257).float().reshape(b, -1, PATCH * 257)
                    enc = m.patch_level_decoder.base(inputs_embeds=m.patch_level_decoder.patch_embedding(oh))
                    enc = enc["last_hidden_state"][:, :-1].reshape(-1, HID)
                    tgt = pt[:, 1:].reshape(-1, PATCH)
                    emb = F.embedding(tgt, m.byte_level_decoder.base.transformer.wte.weight)
                    lg = m.byte_level_decoder.base(inputs_embeds=torch.cat([enc.unsqueeze(1), emb[:, :-1]], 1)).logits.float()[..., :256]
                    p = torch.log_softmax(lg, -1).gather(-1, tgt.clamp(max=255).unsqueeze(-1)).squeeze(-1).exp().reshape(b, -1)[:, :x.shape[1]]
                    ps.append(p.cpu().numpy().astype(np.float32))
                out[n] = np.concatenate(ps)
        buf = io.BytesIO()
        np.savez_compressed(buf, **out)
        return {"bytes": buf.getvalue(), "missing": list(missing)}

    @app.local_entrypoint()
    def score():
        import numpy as np
        from huggingface_hub import list_repo_files
        import re
        files = list_repo_files("nourya-cohen/solomonoff-paper")
        seeds = sorted({m.group(1) for f in files if (m := re.match(r"24M/(seed-\d+)/learner_8191\.pth$", f))})[:8]
        assert len(seeds) == 8
        (OUT / "paq").mkdir(parents=True, exist_ok=True)
        (OUT / "learners").mkdir(parents=True, exist_ok=True)
        (OUT / "bgpt").mkdir(parents=True, exist_ok=True)
        new = [f"new__{s}" for s in SOURCES]
        b88 = sorted(p.stem for p in (ROOT / "runs/battery/b88/rows").glob("*.npy"))
        pj = [(n, lo, "std") for n in new for lo in range(0, len(np.load(OUT / "rows" / f"{n}.npy")), 32)]
        pj += [(n, lo, "forced") for n in new for lo in range(0, len(np.load(OUT / "rows" / f"{n}.npy")), 32)]
        pj += [(n, lo, "forced") for n in b88 for lo in range(0, len(np.load(ROOT / "runs/battery/b88/rows" / f"{n}.npy")), 32)]
        pj = [j for j in pj if not (OUT / "paq" / f"{j[2]}__{j[0]}__{j[1]:03d}.npz").exists()]
        print(len(pj), "paq jobs", flush=True)
        man = {"learners": {}, "bgpt": {}}
        for (s, r) in zip(seeds, learner_job.map(seeds)):
            (OUT / "learners" / f"{s}.npz").write_bytes(r["bytes"])
            man["learners"][s] = {"sha256": r["sha256"], "corpora": r["corpora"]}
            print("learner", s, flush=True)
        groups = {}
        for s, w in BGPT_W.items():
            groups.setdefault(w, []).append(s)
        for (w, ns), r in zip(groups.items(), bgpt_job.starmap(groups.items())):
            (OUT / "bgpt" / f"{w}.npz").write_bytes(r["bytes"])
            man["bgpt"][w] = {"names": ns, "missing": r["missing"]}
            print("bgpt", w, ns, flush=True)
        json.dump(man, open(OUT / "manifest.json", "w"), indent=1)
        for (n, lo, mode), r in zip(pj, paq_job.starmap(pj)):
            b = np.load(io.BytesIO(r["bits"]))
            f = OUT / "paq" / f"{mode}__{n}__{lo:03d}.npz"
            np.savez_compressed(f.with_suffix(".tmp.npz"), bits=b, info=json.dumps(r["info"]), commit=r["commit"],
                                flag=json.dumps(r["flag"]))
            f.with_suffix(".tmp.npz").rename(f)
            print("paq", mode, n, lo, sum(i["aligned"] for i in r["info"]), flush=True)
        print("B106 SCORE DONE", flush=True)
except ImportError:
    pass


def load_paq(mode, name):
    import numpy as np
    parts = sorted((OUT / "paq").glob(f"{mode}__{name}__*.npz"))
    zs = [np.load(f) for f in parts]
    return (np.concatenate([z["bits"] for z in zs]), sum((json.loads(str(z["info"])) for z in zs), []),
            {str(z["commit"]) for z in zs}, {str(z["flag"]) for z in zs})


B88_NAMES = sorted(["bench__" + l for l in ("aitdcc_a_protein", "aitdcc_b_c_source", "aitdcc_d_glibc_rand",
    "aitdcc_e_atlas_float32", "aitdcc_g_astronomy", "arithmetic", "audio_16bit", "audio_8bit", "cifar10_rgb_hwc",
    "cifar10_rgb_planar", "dclm", "dclm_ranked", "dna", "esc50_pcm8", "esc50_pcm8_11khz", "kolmogorov_dna",
    "kolmogorov_text", "llm_compression_arxiv_math", "llm_compression_cc", "llm_compression_python", "metamath",
    "musicnet_pcm8", "musicnet_pcm8_11khz", "mutopia_melody_16th", "speech_commands_pcm8", "speech_commands_pcm8_8khz")]
    + ["new__" + s for s in ("dewiki", "elf_x86_64", "fashion_mnist", "go_source", "hewiki", "python_docs_html",
                             "uci_adult", "yesno_pcm16")])


def gates():
    """Fail-closed admission checks (C1184). Returns a list of errors; empty means admissible."""
    import hashlib
    import numpy as np
    from huggingface_hub import list_repo_files
    import re
    errs = []
    files = list_repo_files("nourya-cohen/solomonoff-paper")
    seeds = sorted({m.group(1) for f in files if (m := re.match(r"24M/(seed-\d+)/learner_8191\.pth$", f))})[:8]
    if len(seeds) != 8:
        errs.append(f"expected 8 release seeds, found {len(seeds)}")
    man = json.load(open(OUT / "manifest.json"))
    got = sorted(f.stem for f in (OUT / "learners").glob("seed-*.npz"))
    if got != seeds or sorted(man["learners"]) != seeds:
        errs.append(f"learner seeds {got} / manifest {sorted(man['learners'])} != {seeds}")
    rows = {s: np.load(OUT / "rows" / f"new__{s}.npy") for s in SOURCES}
    for s in SOURCES:
        J = np.array([json.loads(l)["sequence"] for l in open(OUT / "data" / f"{s}.jsonl") if l.strip()], dtype=np.uint8)
        if J.shape != rows[s].shape or not (J == rows[s]).all():
            errs.append(f"{s}: jsonl rows != npy rows")
        h = hashlib.sha256((OUT / "data" / f"{s}.jsonl").read_bytes()).hexdigest()
        for sd, v in man["learners"].items():
            if v["corpora"][s]["sha256"] != h:
                errs.append(f"{s}/{sd}: learner corpus hash differs from current jsonl")
    for sd in got:
        z = np.load(OUT / "learners" / f"{sd}.npz")
        for s in SOURCES:
            a = z[s]
            if a.shape != rows[s].shape or not np.isfinite(a).all() or a.min() < 0 or a.max() > 1:
                errs.append(f"learner {sd}/{s}: shape/range")
    for w in ("text", "image", "audio"):
        if man["bgpt"].get(w, {}).get("missing") != []:
            errs.append(f"bgpt {w}: missing keys {man['bgpt'].get(w, {}).get('missing')}")
        z = np.load(OUT / "bgpt" / f"{w}.npz")
        for s in [k for k, v in BGPT_W.items() if v == w]:
            a = z[s]
            if a.shape != rows[s].shape or not np.isfinite(a).all() or a.min() < 0 or a.max() > 1:
                errs.append(f"bgpt {w}/{s}: shape/range")
    b88 = sorted(p.stem for p in (ROOT / "runs/battery/b88/rows").glob("*.npy"))
    if b88 != B88_NAMES:
        errs.append(f"B88 inventory {len(b88)} != pinned {len(B88_NAMES)}")
    pp = OUT / "provenance_post.json"
    if not pp.exists():
        errs.append("provenance_post.json missing")
    else:
        post, pre = json.load(open(pp)), json.load(open(OUT / "provenance.json"))
        for s in SOURCES:
            if s not in post or not post[s].get("rebuild_equals_saved_rows"):
                errs.append(f"{s}: rebuild missing or mismatched")
            elif [d["sha256"] for d in post[s]["downloads"]] != [d["sha256"] for d in pre[s]["downloads"]]:
                errs.append(f"{s}: download hashes differ from build manifest")
        if post.get("fsdd_audio", {}).get("wav_formats") != {"width2_ch1_rate8000": 3000}:
            errs.append("fsdd formats not as specified")
        if post.get("kmnist_images", {}).get("npz") != {"keys": ["arr_0"], "shape": [60000, 28, 28], "dtype": "uint8"}:
            errs.append("kmnist array metadata unexpected")
    inv = [("std", f"new__{s}", len(rows[s])) for s in SOURCES] + [("forced", f"new__{s}", len(rows[s])) for s in SOURCES]
    inv += [("forced", n, len(np.load(ROOT / "runs/battery/b88/rows" / f"{n}.npy"))) for n in b88]
    for mode, name, n in inv:
        parts = sorted((OUT / "paq").glob(f"{mode}__{name}__*.npz"))
        los = sorted(int(f.stem.rsplit("__", 1)[1]) for f in parts)
        if los != list(range(0, n, 32)):
            errs.append(f"paq {mode}/{name}: parts {los}")
            continue
        lab = name.split("__", 1)[1]
        want = [] if mode == "std" else (["-forcetext"] if lab in FORCETEXT else ["-forcebinary"])
        for f in parts:
            z = np.load(f)
            info = json.loads(str(z["info"]))
            lo = int(f.stem.rsplit("__", 1)[1])
            if len(info) != min(32, n - lo):
                errs.append(f"paq {mode}/{name}/{f.stem}: {len(info)} rows, expected {min(32, n - lo)}")
            bb = z["bits"]
            for k, i in enumerate(info):
                row = bb[k] if k < len(bb) else None
                fin = row is not None and bool(np.isfinite(row).all())
                allnan = row is not None and bool(np.isnan(row).all())
                if i["aligned"] != fin or not (fin or allnan):
                    errs.append(f"paq {mode}/{name}/{f.stem}#{k}: aligned flag vs row finiteness")
                if not (np.isfinite(i["main_bits"]) and np.isfinite(i["other_bits"]) and i["main_bits"] >= 0 and i["other_bits"] >= 0):
                    errs.append(f"paq {mode}/{name}/{f.stem}#{k}: accounting not finite/nonnegative")
                if fin and abs(float(row.astype(np.float64).sum()) - i["main_bits"]) > 1e-3 * max(1.0, i["main_bits"]):
                    errs.append(f"paq {mode}/{name}/{f.stem}#{k}: matrix sum != logged main bits")
            if str(z["commit"]) != COMMIT or json.loads(str(z["flag"])) != want:
                errs.append(f"paq {mode}/{name}/{f.stem}: commit/flag")
            b = z["bits"]
            if b.shape[0] != len(info) or b.shape[1] != 4095:
                errs.append(f"paq {mode}/{name}/{f.stem}: shape")
            if any(i["main_bits"] + i["other_bits"] > 8 * i["size"] + 1e-6 for i in info):
                errs.append(f"paq {mode}/{name}/{f.stem}: logged bits exceed file bits")
            fin = b[~np.isnan(b).any(1)]
            if len(fin) and (not np.isfinite(fin).all() or fin.min() < 0):
                errs.append(f"paq {mode}/{name}/{f.stem}: bits range")
    return errs


def analyze():
    import numpy as np
    from probe.battery100 import mix2
    from probe.battery75 import P
    from probe.battery94 import config
    from probe.battery104 import T
    res, errs = {"new": {}, "bench_forced": {}}, []
    errs += gates()                                         # C1184: criteria only if every gate passes
    if errs:
        res["errors"], res["admissible"] = errs, False
        print("GATE FAIL", json.dumps(errs[:20], indent=1))
        json.dump(res, open(ROOT / "runs/battery/battery106.json", "w"), indent=1)
        return
    res["admissible"] = True

    def G(p, bits):
        ok = ~np.isnan(bits).any(1)
        q = np.exp2(-bits[ok].astype(np.float64))
        return float((-np.log2(q).mean(1) - mix2(p[ok], q, 0.001)).mean()), int(ok.sum())
    lp = [np.load(f) for f in sorted((OUT / "learners").glob("seed-*.npz"))]
    if len(lp) != 8:
        errs.append(f"learner seeds {len(lp)}")
    bg = {w: np.load(OUT / "bgpt" / f"{w}.npz") for w in ("text", "image", "audio")}
    for s in SOURCES:
        X = np.load(OUT / "rows" / f"new__{s}.npy")
        pe = np.clip(np.mean([z[s].astype(np.float64) for z in lp], 0), 1e-30, None)
        pb = np.clip(bg[BGPT_W[s]][s].astype(np.float64), 1e-30, None)
        r = {"windows": int(len(X))}
        for mode in ("std", "forced"):
            bits, info, commits, flags = load_paq(mode, f"new__{s}")
            if len(info) != len(X) or commits != {COMMIT}:
                errs.append(f"{s}/{mode}: rows {len(info)} commits {commits}")
            r[f"G_learners_{mode}"], r[f"aligned_{mode}"] = G(pe, bits)
            r[f"G_bgpt_{mode}"], _ = G(pb, bits)
            r[f"paq_{mode}_bits"] = float(np.nanmean(bits))
        bs, _, _, _ = load_paq("std", f"new__{s}")
        bf, _, _, _ = load_paq("forced", f"new__{s}")
        common = ~np.isnan(bs).any(1) & ~np.isnan(bf).any(1)
        r["common_rows"] = int(common.sum())
        for mode, bb in (("std", bs), ("forced", bf)):
            bb2 = bb.copy()
            bb2[~common] = np.nan
            r[f"G_learners_{mode}_common"], _ = G(pe, bb2)
        r["E_learners"] = float(-np.log2(pe).mean())
        r["E_bgpt"] = float(-np.log2(pb).mean())
        res["new"][s] = r
        print(s, json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
    for lab in T:
        bits, info, commits, flags = load_paq("forced", f"bench__{lab}")
        size, rnd, sds = config(lab)
        pe = np.clip(np.mean([P(size, rnd, lab, sd) for sd in sds], 0), 1e-30, None)
        g, n = G(pe, bits)
        res["bench_forced"][lab] = {"G_learners_forced": g, "aligned": n, "paq_forced_bits": float(np.nanmean(bits)),
                                    "flags": sorted(flags)}
        print("bench forced", lab, round(g, 4), n, flush=True)
    N = res["new"]
    for s, r in N.items():
        for k in ("aligned_std", "aligned_forced"):
            if r[k] < 1:
                errs.append(f"{s}: empty population {k}")
        for k, v in r.items():
            if isinstance(v, float) and not np.isfinite(v):
                errs.append(f"{s}: non-finite {k}")
    for lab, r in res["bench_forced"].items():
        if r["aligned"] < 1 or not np.isfinite(r["G_learners_forced"]):
            errs.append(f"bench {lab}: empty population or non-finite gain")
    res["errors"] = errs
    if errs:
        res["admissible"] = False
        print("POST-COMPUTATION VALIDATION FAIL", errs[:10])
        json.dump(res, open(ROOT / "runs/battery/battery106.json", "w"), indent=1)
        return
    res["small_populations"] = {s: r["aligned_std"] for s, r in N.items() if r["aligned_std"] < 32}
    res["N1"] = all(N[s]["G_learners_std"] <= 0.002 for s in TEXTLIKE_NEW)
    res["N2"] = all(N[s]["G_learners_forced"] <= 0.002 for s in TEXTLIKE_NEW)
    res["N3"] = N["gutenberg_en"]["G_bgpt_std"] >= 0.1
    res["N4"] = any(N[s]["G_learners_std"] > 0.002 for s in ("kmnist_images", "fsdd_audio"))
    res["S1"] = {"count": int(sum(v["G_learners_forced"] <= 0.002 for v in res["bench_forced"].values())), "need": 6}
    res["S1"]["pass"] = res["S1"]["count"] >= 6
    print(json.dumps({k: res[k] for k in ("errors", "N1", "N2", "N3", "N4", "S1")}, indent=1))
    json.dump(res, open(ROOT / "runs/battery/battery106.json", "w"), indent=1)


if __name__ == "__main__":
    if sys.argv[1:] == ["analyze"]:
        analyze()
