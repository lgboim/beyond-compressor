"""verify_manifest.py: SHA-256 inventory of every tracked file in this repository.

    python verify_manifest.py --write   # regenerate public_manifest.json
    python verify_manifest.py --check   # verify every file against it (exit 1 on any mismatch)

Uses `git ls-files` when available so that ignored and untracked files are excluded; otherwise walks the tree,
skipping .git, caches and virtual environments. The manifest itself is excluded from the inventory.
"""
import argparse, hashlib, json, os, subprocess, sys

MANIFEST = "public_manifest.json"
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache"}


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files", "-z"], check=True, capture_output=True).stdout
        files = [f.decode() for f in out.split(b"\0") if f]
        if files:
            return sorted(f for f in files if f != MANIFEST and os.path.isfile(f))
    except Exception:
        pass
    files = []
    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            p = os.path.relpath(os.path.join(root, n), ".")
            if p != MANIFEST and not n.endswith((".pyc", ".DS_Store")):
                files.append(p)
    return sorted(files)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    files = tracked_files()
    current = {f: {"sha256": sha256(f), "bytes": os.path.getsize(f)} for f in files}
    if a.write:
        json.dump({"algorithm": "sha256", "files": len(current), "entries": current}, open(MANIFEST, "w"), indent=1)
        print(f"wrote {MANIFEST}: {len(current)} files")
        return
    ref = json.load(open(MANIFEST))["entries"]
    missing = sorted(set(ref) - set(current)); extra = sorted(set(current) - set(ref))
    changed = sorted(f for f in set(ref) & set(current) if ref[f]["sha256"] != current[f]["sha256"])
    for label, items in (("missing", missing), ("untracked-by-manifest", extra), ("changed", changed)):
        for f in items:
            print(f"{label}: {f}")
    ok = not (missing or extra or changed)
    print(f"{'OK' if ok else 'FAIL'}: {len(current)} files checked against {MANIFEST}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
