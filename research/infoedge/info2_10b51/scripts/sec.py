"""Shared SEC client for INFO-2: <= 2 requests/second (cross-process file lock), cached to ../cache/."""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import random
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = ROOT / "cache"
UA = "Claude Space research dspinjr@gmail.com"
MIN_GAP = 0.55  # seconds between requests -> < 2 req/s for this test, shared across processes
LOCKFILE = CACHE / ".rate.lock"
STAMP = CACHE / ".rate.stamp"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
STATS = {"net": 0, "cache": 0, "retry": 0}


def _wait():
    CACHE.mkdir(parents=True, exist_ok=True)
    with open(LOCKFILE, "a+") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            last = float(STAMP.read_text()) if STAMP.exists() else 0.0
        except ValueError:
            last = 0.0
        now = time.time()
        if now - last < MIN_GAP:
            time.sleep(MIN_GAP - (now - last))
        STAMP.write_text(repr(time.time()))
        fcntl.flock(lf, fcntl.LOCK_UN)


def cpath(url: str, sub: str, ext: str) -> Path:
    h = hashlib.sha1(url.encode()).hexdigest()
    return CACHE / sub / h[:2] / f"{h}{ext}"


def get(url: str, sub: str = "misc", ext: str = ".bin", offline: bool = False, tries: int = 8,
        ok404: bool = False) -> bytes | None:
    p = cpath(url, sub, ext)
    if p.exists():
        STATS["cache"] += 1
        return p.read_bytes()
    if ok404 and p.with_suffix(p.suffix + ".404").exists():
        return None
    if offline:
        return None
    last = None
    for a in range(tries):
        _wait()
        try:
            r = SESSION.get(url, timeout=90)
            STATS["net"] += 1
            if r.status_code == 200:
                p.parent.mkdir(parents=True, exist_ok=True)
                tmp = p.with_suffix(p.suffix + ".tmp")
                tmp.write_bytes(r.content)
                os.replace(tmp, p)
                return r.content
            if r.status_code == 404 and ok404:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.with_suffix(p.suffix + ".404").write_text("404")
                return None
            last = f"HTTP {r.status_code}: {r.text[:150]}"
        except requests.RequestException as e:
            last = repr(e)
        STATS["retry"] += 1
        time.sleep(min(60, 2 * 2 ** a) + random.random())
    raise RuntimeError(f"GET failed: {url} :: {last}")


def get_json(url: str, sub: str = "json", **kw):
    b = get(url, sub, ".json", **kw)
    return None if b is None else json.loads(b)
