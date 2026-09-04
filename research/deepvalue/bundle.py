#!/usr/bin/env python3
"""Pack research/deepvalue/filings/ into filings_bundle.tar.gz for offline agents.

The `raw/` subfolder inside each ticker directory holds the original EDGAR
HTML/XML downloads. They are a local re-fetch cache, are 5-10x the size of the
extracted text, and are useless to a reading agent, so they are excluded.

The archive is rooted at `research/deepvalue/filings/` so that extracting it from
the repository root puts every file back exactly where the scripts expect it.

Usage:
    bundle.py [--out filings_bundle.tar.gz] [--source research/deepvalue/filings]
"""
from __future__ import annotations

import argparse
import os
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DEFAULT_SRC = HERE / "filings"
DEFAULT_OUT = REPO / "filings_bundle.tar.gz"

EXCLUDE_DIRS = {"raw", "__pycache__"}
EXCLUDE_NAMES = {".DS_Store"}


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024 or unit == "GB":
            return f"{n:,.1f} {unit}" if unit != "B" else f"{n:,.0f} B"
        n /= 1024.0
    return f"{n:.1f} GB"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Bundle fetched filings for offline agents.")
    ap.add_argument("--source", default=str(DEFAULT_SRC), help="filings directory to pack")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output tar.gz path")
    args = ap.parse_args(argv)

    src = Path(args.source).resolve()
    out = Path(args.out).resolve()
    if not src.is_dir():
        print(f"! source directory not found: {src}", file=sys.stderr)
        return 2

    # arcname prefix relative to the repo root, so `tar -xzf` from the repo root
    # restores research/deepvalue/filings/... in place
    try:
        prefix = src.relative_to(REPO)
    except ValueError:
        prefix = Path(src.name)

    t0 = time.time()
    n_files = 0
    n_tickers = 0
    raw_skipped = 0
    raw_bytes = 0
    uncompressed = 0

    out.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(out, "w:gz", compresslevel=6) as tar:
        for root, dirs, files in os.walk(src):
            rootp = Path(root)
            # count and prune raw/ before descending
            for d in list(dirs):
                if d in EXCLUDE_DIRS:
                    p = rootp / d
                    for rr, _, ff in os.walk(p):
                        raw_skipped += len(ff)
                        raw_bytes += sum((Path(rr) / f).stat().st_size
                                         for f in ff if (Path(rr) / f).is_file())
                    dirs.remove(d)
            dirs.sort()
            if rootp.parent == src:
                n_tickers += 1
            for name in sorted(files):
                if name in EXCLUDE_NAMES:
                    continue
                p = rootp / name
                if not p.is_file():
                    continue
                arc = prefix / p.relative_to(src)
                tar.add(p, arcname=str(arc))
                n_files += 1
                uncompressed += p.stat().st_size

    size = out.stat().st_size
    ratio = uncompressed / size if size else 0
    print(f"bundled {n_files:,} files from {n_tickers:,} ticker directories")
    print(f"excluded {raw_skipped:,} raw/ files ({human(raw_bytes)})")
    print(f"uncompressed: {human(uncompressed)}  ->  compressed: {human(size)} "
          f"({ratio:.1f}x, {time.time()-t0:.1f}s)")
    print(f"bundle size: {size:,} bytes ({human(size)})")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
