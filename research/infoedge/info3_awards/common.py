"""Shared helpers for INFO-3 (government contract awards nobody announced).

Network etiquette (fixed):
  * SEC EDGAR: at most 2 requests a second from this test (a process-wide lock
    plus a cross-process lock file, so two stages running at once still share
    the budget), User-Agent "Claude Space research dspinjr@gmail.com".
  * USAspending: no key, no published limit; kept to a few requests in flight.
  * Yahoo (yfinance): chunked, sentinel-checked, backed off on empty results.
Everything downloaded is cached under cache/ (gitignored) and reused.
"""
from __future__ import annotations

import datetime as dt
import fcntl
import gzip
import json
import re
import threading
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
DATA = HERE / "data"
for d in (CACHE, DATA):
    d.mkdir(parents=True, exist_ok=True)
ROOT = HERE.parents[2]

SEC_UA = "Claude Space research dspinjr@gmail.com"
SEC_HEADERS = {"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"}
SEC_MIN_INTERVAL = 0.55            # seconds between SEC requests (< 2 per second)
SEC_LOCKFILE = CACHE / ".sec_rate.lock"

USAS = "https://api.usaspending.gov/api/v2"
CONTRACT_TYPES = ["A", "B", "C", "D"]   # BPA call, purchase order, delivery order, definitive contract

_sec_lock = threading.Lock()
_sess = requests.Session()
_usas_lock = threading.Lock()
_usas_last = [0.0]
USAS_MIN_INTERVAL = 0.4   # seconds between USAspending requests from one process:
                          # faster bursts made the API drop most connections (2026-09-26)


def _usas_throttle() -> None:
    with _usas_lock:
        w = USAS_MIN_INTERVAL - (time.time() - _usas_last[0])
        if w > 0:
            time.sleep(w)
        _usas_last[0] = time.time()


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# --------------------------------------------------------------------------- #
# SEC
# --------------------------------------------------------------------------- #
def _sec_throttle() -> None:
    """Process lock + file lock holding the time of the last SEC request."""
    with _sec_lock:
        SEC_LOCKFILE.touch(exist_ok=True)
        with open(SEC_LOCKFILE, "r+") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            try:
                txt = fh.read().strip()
                last = float(txt) if txt else 0.0
                wait = SEC_MIN_INTERVAL - (time.time() - last)
                if wait > 0:
                    time.sleep(wait)
                fh.seek(0)
                fh.truncate()
                fh.write(f"{time.time():.6f}")
                fh.flush()
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)


def sec_json(url: str, cache: Path, tries: int = 6):
    """GET JSON from SEC with a permanent gzip cache. 404 cached as null."""
    if cache.exists():
        with gzip.open(cache, "rt") as fh:
            return json.loads(fh.read())
    cache.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(tries):
        try:
            _sec_throttle()
            r = _sess.get(url, headers=SEC_HEADERS, timeout=90)
            if r.status_code == 404:
                with gzip.open(cache, "wt") as fh:
                    fh.write("null")
                return None
            if r.status_code in (403, 429, 500, 502, 503, 504):
                raise RuntimeError(f"HTTP {r.status_code}")
            r.raise_for_status()
            js = r.json()
            with gzip.open(cache, "wt") as fh:
                fh.write(r.text)
            return js
        except Exception as exc:  # noqa: BLE001
            if attempt == tries - 1:
                log(f"  ! SEC giving up on {url}: {exc}")
                return "FAILED"
            time.sleep(3.0 * (attempt + 1) ** 2)
    return "FAILED"


# --------------------------------------------------------------------------- #
# USAspending
# --------------------------------------------------------------------------- #
def usas_post(path: str, body: dict, tries: int = 25, timeout: int = 240, max_slow: int = 5):
    """POST with retries. USAspending intermittently drops connections without a
    response (seen 2026-09-26 at ~40% of requests, even at 1 request/second);
    those are retried quickly. HTTP errors back off longer."""
    slow = 0
    for attempt in range(tries):
        try:
            _usas_throttle()
            r = _sess.post(f"{USAS}{path}", json=body, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
            if r.status_code == 400:
                return {"__error__": r.text[:500]}
            r.raise_for_status()
            return r.json()
        except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError) as exc:
            if attempt == tries - 1:
                log(f"  ! USAspending giving up on {path}: {exc}")
                return None
            time.sleep(2.0 + attempt * 1.0)
        except Exception as exc:  # noqa: BLE001
            slow += 1
            if attempt == tries - 1 or slow > max_slow:
                log(f"  ! USAspending giving up on {path}: {exc}")
                return {"__timeout__": str(exc)[:200]} if "timed out" in str(exc).lower() else None
            time.sleep(5.0 * slow ** 2)
    return None


def usas_get(path: str, params: dict | None = None, tries: int = 25, timeout: int = 120):
    slow = 0
    for attempt in range(tries):
        try:
            _usas_throttle()
            r = _sess.get(f"{USAS}{path}", params=params, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                raise RuntimeError(f"HTTP {r.status_code}")
            r.raise_for_status()
            return r.json()
        except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError) as exc:
            if attempt == tries - 1:
                log(f"  ! USAspending giving up on {path}: {exc}")
                return None
            time.sleep(2.0 + attempt * 1.0)
        except Exception as exc:  # noqa: BLE001
            slow += 1
            if attempt == tries - 1 or slow > 5:
                log(f"  ! USAspending giving up on {path}: {exc}")
                return None
            time.sleep(5.0 * slow ** 2)
    return None


# --------------------------------------------------------------------------- #
# Names
# --------------------------------------------------------------------------- #
LEGAL = {
    "INC", "INCORPORATED", "CORP", "CORPORATION", "CO", "COMPANY", "COS", "COMPANIES",
    "LTD", "LIMITED", "LLC", "LLP", "LP", "PLC", "NV", "SA", "AG", "SE", "HOLDINGS",
    "HOLDING", "HLDGS", "GROUP", "THE", "DE", "DEL", "NEW", "MD", "VA", "NY", "NJ", "CA",
    "TX", "FL", "NV", "OLD", "PA", "MA", "CT", "OH", "MN", "WA", "CO", "INTL",
}
# words too common to identify a company on their own (first token of a core)
GENERIC = {
    "AMERICAN", "AMERICA", "NATIONAL", "UNITED", "GENERAL", "GLOBAL", "INTERNATIONAL",
    "FIRST", "ADVANCED", "APPLIED", "INTEGRATED", "US", "USA", "NORTH", "SOUTH", "EAST",
    "WEST", "NORTHERN", "SOUTHERN", "EASTERN", "WESTERN", "PACIFIC", "ATLANTIC", "CENTRAL",
    "NEW", "STANDARD", "UNIVERSAL", "CONTINENTAL", "INDUSTRIAL", "TECHNOLOGY", "TECHNOLOGIES",
    "SYSTEMS", "SOLUTIONS", "SERVICES", "DATA", "DIGITAL", "SECURITY", "DEFENSE", "HEALTH",
    "MEDICAL", "ENERGY", "POWER", "ENVIRONMENTAL", "ENGINEERING", "CONSTRUCTION", "PREMIER",
    "SUPERIOR", "ALLIED", "PRECISION", "SPECTRUM", "PINNACLE", "SUMMIT", "ALPHA", "OMEGA",
    "APEX", "STAR", "EAGLE", "LIBERTY", "PATRIOT", "FREEDOM", "INDEPENDENCE", "HERITAGE",
    "CAPITAL", "COMMUNITY", "PUBLIC", "ATLAS", "MERIDIAN", "VANGUARD", "SIGMA", "DELTA",
    "ACCESS", "ALLIANCE", "PROFESSIONAL", "QUALITY", "TOTAL", "GREEN", "BLUE", "RED",
    "GOLD", "SILVER", "SUN", "MOUNTAIN", "RIVER", "LAKE", "OCEAN", "BAY", "COASTAL",
    "TRI", "INNOVATIVE", "SMART", "SAFE", "CUSTOM", "MODERN", "NEXT", "NOVA", "ONE",
    "ORION", "PHOENIX", "PIONEER", "PRIME", "PROGRESSIVE", "REGIONAL", "RELIANCE", "ROYAL",
    "SCIENTIFIC", "SELECT", "SOUND", "STRATEGIC", "TRANS", "TRINITY", "UNIVERSITY", "VISION",
    "WORLD", "WORLDWIDE", "CORE", "INTER", "MICRO", "NANO", "BIO", "INFO", "CYBER", "AERO",
    "TELE", "NET", "LINK", "TEAM", "HOME", "LIFE", "CARE", "CITY", "STATE", "COUNTY",
}


def norm_tokens(name: str) -> list[str]:
    """Upper-case tokens, '&' -> AND, punctuation dropped, SEC '/DE/' tags dropped."""
    s = (name or "").upper()
    s = re.sub(r"/[A-Z]{2,3}/?", " ", s)          # SEC state tags like /DE/, /NEW/
    s = s.replace("&", " AND ")
    s = re.sub(r"\bL\.?\s?L\.?\s?C\.?", " LLC ", s)
    s = re.sub(r"\bL\.?\s?P\.?(?=\s|$)", " LP ", s)
    s = re.sub(r"\bN\.?\s?V\.?(?=\s|$)", " NV ", s)
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    return [t for t in s.split() if t]


def core(name: str) -> str:
    """Name without legal-form / holding words (leading THE, trailing INC, CORP ...)."""
    t = norm_tokens(name)
    while t and t[0] == "THE":
        t = t[1:]
    while t and t[-1] in LEGAL:
        t = t[:-1]
    # drop legal words anywhere after the first two tokens? no: keep interior words
    return " ".join(t)


def distinctive(c: str) -> bool:
    """A core that can be used as a prefix: non-generic first token of >= 3
    characters, or at least 3 tokens."""
    t = c.split()
    if not t:
        return False
    if len(t) >= 3:
        return True
    return len(t[0]) >= 3 and t[0] not in GENERIC and not t[0].isdigit()


LEGAL_FORM = {"INC", "CORP", "CORPORATION", "CO", "COMPANY", "LTD", "LIMITED", "LLC", "LP", "PLC",
              "NV", "SA", "AG", "SE", "INCORPORATED", "THE", "L P", "N V"}


def core_phrase(name: str) -> str:
    """Download phrase for stage 3 (no count scan): the SEC name without SEC
    state tags, trailing legal-form words and a trailing HOLDING(S)/GROUP, as
    long as at least 6 letters/digits remain ('ENGILITY HOLDINGS' -> 'ENGILITY',
    'DLH HOLDINGS' stays). Punctuation is kept as SEC writes it."""
    ps = search_phrases(name)
    if not ps:
        return ""
    c = ps[-1]
    t = c.split()
    while len(t) > 1 and re.sub(r"[^A-Z0-9]", "", t[-1]) in ("HOLDINGS", "HOLDING", "GROUP", "COMPANIES", "HLDGS"):
        cand = " ".join(t[:-1]).rstrip(",.;: ")
        if len(re.sub(r"[^A-Z0-9]", "", cand)) < 6:
            break
        t = cand.split()
    return " ".join(t).rstrip(",.;: ")


def search_phrases(name: str) -> list[str]:
    """Phrases for USAspending recipient_search_text, broadest first.

    The API does a case-insensitive *substring* match on recipient and parent
    names, with punctuation taken literally ('&' is not 'AND', 'NCI, INC' is not
    'NCI INC'). Two phrases per name:
      broad - the first word, if it has >= 4 letters/digits and is not a common
              word (e.g. KRATOS, VECTRUS, ENGILITY);
      core  - the name as SEC spells it, minus SEC state tags and trailing
              legal-form words and punctuation (e.g. 'KRATOS DEFENSE & SECURITY
              SOLUTIONS', 'DLH HOLDINGS'); if that leaves fewer than 6 letters,
              the next legal-form word is put back ('VSE CORP', 'NCI, INC').
    """
    s = (name or "").upper()
    s = re.sub(r"\s*/[A-Z]{2,5}/?\s*$", " ", s)
    s = re.sub(r"\s+/[A-Z]{2,5}/?", " ", s)
    toks = s.split()
    while toks and toks[0] == "THE":
        toks = toks[1:]
    if not toks:
        return []
    kept = list(toks)
    stripped = []
    while kept and re.sub(r"[^A-Z0-9]", "", kept[-1]) in LEGAL_FORM:
        stripped.insert(0, kept.pop())
    if not kept:
        kept, stripped = toks, []
    core_raw = " ".join(kept).rstrip(",.;: ")
    if len(re.sub(r"[^A-Z0-9]", "", core_raw)) < 6 and stripped:
        core_raw = (" ".join(kept) + " " + stripped[0]).rstrip(",.;: ")
    out = []
    first = toks[0].rstrip(",.")
    alnum = re.sub(r"[^A-Z0-9]", "", first)
    if (len(alnum) >= 4 and alnum == first and alnum not in GENERIC and not alnum.isdigit()
            and alnum not in LEGAL_FORM and first != core_raw):
        out.append(first)
    out.append(core_raw)
    return [p for p in dict.fromkeys(out) if len(re.sub(r"[^A-Z0-9]", "", p)) >= 3]
