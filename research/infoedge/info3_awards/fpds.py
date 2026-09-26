"""FPDS ATOM feed lookups: the record-keeping dates of one contract action.

For each transaction we ask FPDS (public ATOM feed) for the record with the
same PIID, modification number and referenced IDV PIID, and read
signedDate, createdDate, approvedDate and lastModifiedDate. Cached per query.
"""
from __future__ import annotations

import gzip
import hashlib
import re
import threading
import time
import urllib.parse

import requests

from common import CACHE, SEC_UA, log

FP = CACHE / "fpds"
FP.mkdir(exist_ok=True)
_lock = threading.Lock()
_last = [0.0]
MIN_INTERVAL = 0.35
_sess = requests.Session()


def _throttle():
    with _lock:
        w = MIN_INTERVAL - (time.time() - _last[0])
        if w > 0:
            time.sleep(w)
        _last[0] = time.time()


def _q(v: str) -> str:
    return '"' + str(v).replace('"', "") + '"'


def fetch(piid: str, mod: str, ref_idv: str | None, agency: str | None = None) -> str | None:
    parts = [f"PIID:{_q(piid)}", f"MODIFICATION_NUMBER:{_q(mod)}"]
    if ref_idv:
        parts.append(f"REF_IDV_PIID:{_q(ref_idv)}")
    q = " ".join(parts)
    key = hashlib.md5(q.encode()).hexdigest()
    p = FP / f"{key}.xml.gz"
    if p.exists():
        with gzip.open(p, "rt") as fh:
            return fh.read()
    url = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=" + urllib.parse.quote(q)
    for attempt in range(5):
        try:
            _throttle()
            r = _sess.get(url, headers={"User-Agent": SEC_UA}, timeout=90)
            if r.status_code in (429, 500, 502, 503, 504):
                raise RuntimeError(f"HTTP {r.status_code}")
            r.raise_for_status()
            with gzip.open(p, "wt") as fh:
                fh.write(r.text)
            return r.text
        except Exception as exc:  # noqa: BLE001
            if attempt == 4:
                log(f"  ! FPDS giving up: {q}: {exc}")
                return None
            time.sleep(5 * (attempt + 1) ** 2)
    return None


_TAG = {k: re.compile(rf"<ns1:{k}>([^<]*)</ns1:{k}>") for k in (
    "signedDate", "createdDate", "approvedDate", "lastModifiedDate", "obligatedAmount", "modNumber",
    "PIID", "ultimateParentUEIName", "vendorName", "transactionNumber")}


def parse(xml: str) -> list[dict]:
    """One dict per <entry>."""
    out = []
    for e in xml.split("<entry>")[1:]:
        d = {}
        for k, rx in _TAG.items():
            m = rx.findall(e)
            if m:
                # award-level PIID comes first; modNumber too (IDV reference block follows)
                d[k] = m[0]
        agency = re.search(r'<ns1:agencyID name="([^"]*)">([^<]*)</ns1:agencyID>', e)
        d["agencyID"] = agency.group(2) if agency else None
        out.append(d)
    return out
