"""
Shared SEC EDGAR client for INFO-1.

* One process-wide rate limiter: at most 2 requests a second to any sec.gov host
  (five tests share one IP and SEC's 10-a-second limit; PREREG common rules).
* User-Agent "Claude Space research dspinjr@gmail.com".
* Every response is cached under cache/ (gitignored) and reused, so reruns make
  no network requests once the cache is warm.
"""
from __future__ import annotations

import datetime as dt
import gzip
import json
import random
import threading
import time
import urllib.parse
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
FTS_CACHE = CACHE / "fts"
DOC_CACHE = CACHE / "docs"
IDX_CACHE = CACHE / "full_index"
for d in (CACHE, FTS_CACHE, DOC_CACHE, IDX_CACHE):
    d.mkdir(parents=True, exist_ok=True)

UA = "Claude Space research dspinjr@gmail.com"
MAX_RPS = 2.0
FTS_BASE = "https://efts.sec.gov/LATEST/search-index"
PAGE = 100
CAP = 10_000


class RateLimiter:
    def __init__(self, rps: float):
        self.gap = 1.0 / rps
        self.lock = threading.Lock()
        self.next_t = 0.0

    def wait(self):
        with self.lock:
            now = time.monotonic()
            t = max(now, self.next_t)
            self.next_t = t + self.gap
        d = t - time.monotonic()
        if d > 0:
            time.sleep(d)


LIMITER = RateLimiter(MAX_RPS)
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
STATS = {"network": 0, "cache": 0, "retries": 0, "failed": 0}
_SL = threading.Lock()
OFFLINE = False


def _bump(k):
    with _SL:
        STATS[k] += 1


def get(url: str, tries: int = 8, timeout: int = 90) -> requests.Response | None:
    """Rate-limited GET with retries on 429/5xx. Returns None on 404."""
    last = None
    for attempt in range(tries):
        LIMITER.wait()
        try:
            r = SESSION.get(url, timeout=timeout)
            _bump("network")
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return None
            last = f"HTTP {r.status_code}"
        except requests.RequestException as e:
            last = repr(e)
        _bump("retries")
        time.sleep(min(60, 2 * 2 ** attempt) + random.random())
    _bump("failed")
    raise RuntimeError(f"GET failed: {url} :: {last}")


# --------------------------------------------------------------------------- FTS
def _fts_path(key: str, start: dt.date, end: dt.date, frm: int) -> Path:
    return FTS_CACHE / key / f"{start:%Y%m%d}_{end:%Y%m%d}_{frm:05d}.json.gz"


def fts(q: str, key: str, start: dt.date, end: dt.date, frm: int = 0, forms: str = "10-K") -> dict:
    p = _fts_path(key, start, end, frm)
    if p.exists():
        try:
            with gzip.open(p, "rt") as fh:
                d = json.loads(fh.read())
            if "hits" in d:
                _bump("cache")
                return d
        except Exception:  # noqa: BLE001
            pass
    if OFFLINE:
        raise RuntimeError(f"offline, not cached: {p}")
    url = (f"{FTS_BASE}?q={urllib.parse.quote(q)}&forms={urllib.parse.quote(forms)}&dateRange=custom"
           f"&startdt={start:%Y-%m-%d}&enddt={end:%Y-%m-%d}")
    if frm:
        url += f"&from={frm}"
    for attempt in range(8):
        r = get(url)
        try:
            d = r.json() if r is not None else {}
        except ValueError:
            d = {}
        if "hits" in d:
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix(p.suffix + f".tmp{threading.get_ident()}")
            with gzip.open(tmp, "wt") as fh:
                fh.write(json.dumps(d))
            tmp.replace(p)
            return d
        _bump("retries")
        time.sleep(2 + 2 * attempt)
    raise RuntimeError(f"FTS returned no hits object: {url}")


def year_slices(a: dt.date, b: dt.date):
    return [(max(dt.date(y, 1, 1), a), min(dt.date(y, 12, 31), b)) for y in range(a.year, b.year + 1)]


def _split(a: dt.date, b: dt.date):
    if (a.year, a.month) != (b.year, b.month):
        out, cur = [], dt.date(a.year, a.month, 1)
        while cur <= b:
            nxt = dt.date(cur.year + (cur.month == 12), cur.month % 12 + 1, 1)
            out.append((max(cur, a), min(nxt - dt.timedelta(days=1), b)))
            cur = nxt
        return out
    if a == b:
        raise RuntimeError("single day over cap")
    mid = a + (b - a) // 2
    return [(a, mid), (mid + dt.timedelta(days=1), b)]


def fts_all(q: str, key: str, a: dt.date, b: dt.date, forms: str = "10-K") -> tuple[list, list]:
    """All hits for a query over [a, b], splitting slices that reach the 10k cap
    and repairing the relevance-tie paging quirk (see oplev fetch_mentions.py)."""
    d0 = fts(q, key, a, b, 0, forms)
    tot = d0["hits"]["total"]
    total, rel = int(tot["value"]), tot.get("relation", "eq")
    if rel != "eq" or total >= CAP:
        hits, audit = [], []
        for s, e in _split(a, b):
            h, au = fts_all(q, key, s, e, forms)
            hits += h
            audit += au
        return hits, audit
    if total > PAGE and (b - a).days > 366:
        # several pages over several years: query year by year instead (most years then fit
        # on one page, which avoids the relevance-tie paging quirk and its costly repair)
        hits, audit = [], []
        for s_, e_ in year_slices(a, b):
            h, au = fts_all(q, key, s_, e_, forms)
            hits += h
            audit += au
        return hits, audit
    hits = list(d0["hits"]["hits"])
    for frm in range(PAGE, total, PAGE):
        hits += fts(q, key, a, b, frm, forms)["hits"]["hits"]
    first = len({h["_id"] for h in hits})
    repaired = False
    if first < total and a < b:
        repaired = True
        for s, e in _split(a, b):
            h, _ = fts_all(q, key, s, e, forms)
            hits += h
    by = {}
    for h in hits:
        by.setdefault(h["_id"], h)
    hits = list(by.values())
    return hits, [dict(key=key, start=str(a), end=str(b), total=total, unique=len(hits), repaired=repaired)]


# --------------------------------------------------------------------------- documents
def doc_url(cik: int, adsh: str, fname: str) -> str:
    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{adsh.replace('-', '')}/{fname}"


def doc_path(adsh: str, fname: str) -> Path:
    a = adsh.replace("-", "")
    return DOC_CACHE / a[:10] / f"{a}_{fname}.gz"


def _decode(b: bytes) -> str:
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("cp1252", errors="replace")


def fetch_doc(cik: int, adsh: str, fname: str) -> str | None:
    """Raw document text (HTML or txt), gzip-cached. None if 404."""
    p = doc_path(adsh, fname)
    if p.exists():
        try:
            with gzip.open(p, "rb") as fh:
                b = fh.read()
            _bump("cache")
            return None if b == b"__404__" else _decode(b)
        except (EOFError, OSError):
            p.unlink()          # truncated by an interrupted write: fetch again
    if OFFLINE:
        return None
    r = get(doc_url(cik, adsh, fname))
    p.parent.mkdir(parents=True, exist_ok=True)
    b = b"__404__" if r is None else r.content
    tmp = p.with_suffix(p.suffix + f".tmp{threading.get_ident()}")
    with gzip.open(tmp, "wb", compresslevel=6) as fh:
        fh.write(b)
    tmp.replace(p)
    return None if r is None else _decode(b)


def full_index(year: int, qtr: int) -> str:
    """EDGAR full-index form.idx for one quarter (all filings: form, company, CIK, date)."""
    p = IDX_CACHE / f"form_{year}Q{qtr}.idx.gz"
    if p.exists():
        with gzip.open(p, "rt", encoding="latin-1") as fh:
            return fh.read()
    r = get(f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{qtr}/form.idx", timeout=180)
    txt = r.content.decode("latin-1") if r is not None else ""
    with gzip.open(p, "wt", encoding="latin-1") as fh:
        fh.write(txt)
    return txt
