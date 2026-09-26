#!/usr/bin/env python3
"""Stage 3: download every contract transaction whose recipient or parent name
contains a chosen search phrase (USAspending custom transaction download, a
limited set of columns, action dates FY2010 onward, awards whose total
obligation is at least $250,000: a single action below that can reach 2% of
market cap only for a company worth less than $12.5M).

Runs alongside stage 2: every few minutes it reads the phrase counts already
cached by stage 2, applies the same choice rule (s2_scan: broad phrase if it
has 1..MAX_BROAD hits, else the core phrase if it has 1..MAX_CORE), and
downloads chosen phrases not yet downloaded, in batches of at most
BATCH_PHRASES phrases and BATCH_ROWS expected rows (OR within a request).
A batch that comes back with 500,000 rows (the API cap) is split and redone.
Stops when stage 2 has finished and nothing is left.

Output: cache/dl/<batch id>.parquet (raw rows) + .json (phrases, row count).
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from common import CACHE, CONTRACT_TYPES, DATA, core_phrase, log, search_phrases, usas_get, usas_post
from s2_scan import MAX_BROAD, MAX_CORE, SCAN, scope

START, END = "2009-10-01", "2026-09-30"
BATCH_ROWS = 300_000          # expected rows from the (unfiltered) stage-2 counts
AWARD_FLOOR = 250_000         # awards whose total obligation is below this are not downloaded
BATCH_PHRASES = 12            # 25-phrase OR queries mostly fail server-side
API_CAP = 500_000
DL = CACHE / "dl"
DL.mkdir(exist_ok=True)
COLS = [
    "contract_transaction_unique_key", "contract_award_unique_key", "award_id_piid",
    "modification_number", "transaction_number", "parent_award_id_piid", "action_date",
    "federal_action_obligation", "awarding_agency_code", "awarding_agency_name",
    "awarding_sub_agency_name", "awarding_office_name", "recipient_uei", "recipient_duns",
    "recipient_name", "recipient_parent_uei", "recipient_parent_duns", "recipient_parent_name",
    "last_modified_date", "action_type_code", "award_type_code", "transaction_description",
]


def cached_count(ph):
    p = SCAN / f"{hashlib.md5(ph.encode()).hexdigest()}.json.gz"
    if not p.exists():
        return None
    with gzip.open(p, "rt") as fh:
        return json.loads(fh.read())["n"]


def chosen_phrases(A) -> tuple[dict, int]:
    """phrase -> expected rows, for aliases whose choice is already determined."""
    out, undecided = {}, 0
    for ps in A.phrases:
        c0 = cached_count(ps[0])
        lim0 = MAX_BROAD if len(ps) > 1 else MAX_CORE
        if c0 is not None and 0 <= c0 <= lim0:
            if c0 > 0:
                out[ps[0]] = c0
            continue
        if c0 is None:
            undecided += 1
            continue
        if len(ps) > 1:
            c1 = cached_count(ps[1])
            if c1 is None:
                undecided += 1
            elif 0 < c1 <= MAX_CORE:
                out[ps[1]] = c1
    return out, undecided


def done_phrases() -> set:
    s = set()
    for m in DL.glob("*.json"):
        if m.name.endswith(".failed.json"):
            s.update(json.loads(m.read_text())["phrases"])
            continue
        js = json.loads(m.read_text())
        if js.get("rows") is not None and not js.get("capped"):
            s.update(js["phrases"])
    return s


def one_batch(phrases: list[str]) -> dict:
    bid = "b" + hashlib.md5("|".join(sorted(phrases)).encode()).hexdigest()[:12]
    out, meta = DL / f"{bid}.parquet", DL / f"{bid}.json"
    if out.exists() and meta.exists():
        return json.loads(meta.read_text())
    body = {"filters": {"award_type_codes": CONTRACT_TYPES,
                        "time_period": [{"start_date": START, "end_date": END}],
                        "recipient_search_text": phrases,
                        "award_amounts": [{"lower_bound": AWARD_FLOOR}]},
            "columns": COLS, "file_format": "csv"}
    for attempt in range(2):
        r = usas_post("/download/transactions/", body)
        if not r or "__error__" in r or "file_name" not in r:
            log(f"  {bid}: request failed {str(r)[:200]}")
            time.sleep(30 * (attempt + 1))
            continue
        fn, url = r["file_name"], r["file_url"]
        t0, st = time.time(), None
        while time.time() - t0 < 5400:
            st = usas_get("/download/status", {"file_name": fn})
            if st and st.get("status") in ("finished", "failed"):
                break
            time.sleep(8)
        if not st or st.get("status") != "finished":
            log(f"  {bid}: status {st and st.get('status')} {st and st.get('message')}")
            time.sleep(30 * (attempt + 1))
            continue
        z = None
        for a2 in range(6):
            try:
                resp = requests.get(url, timeout=1800)
                resp.raise_for_status()
                z = zipfile.ZipFile(io.BytesIO(resp.content))
                break
            except Exception as exc:  # noqa: BLE001
                log(f"  {bid}: fetch error {exc}")
                time.sleep(20 * (a2 + 1))
        if z is None:
            continue
        frames = [pd.read_csv(z.open(n), dtype=str, low_memory=False)
                  for n in z.namelist() if "Contracts_PrimeTransactions" in n]
        df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=COLS)
        df.to_parquet(out, index=False)
        m = {"bid": bid, "phrases": phrases, "rows": len(df), "capped": len(df) >= API_CAP}
        meta.write_text(json.dumps(m))
        log(f"  {bid}: {len(df)} rows ({len(phrases)} phrases){' CAPPED' if m['capped'] else ''}")
        return m
    if len(phrases) > 1:        # a batch the server keeps failing on: split it
        h = len(phrases) // 2
        a, b = one_batch(phrases[:h]), one_batch(phrases[h:])
        return {"bid": bid, "phrases": phrases, "rows": (a.get("rows") or 0) + (b.get("rows") or 0),
                "split": True, "failed": bool(a.get("failed") or b.get("failed"))}
    m = {"bid": bid, "phrases": phrases, "rows": None, "failed": True}
    (DL / f"{bid}.failed.json").write_text(json.dumps(m))
    log(f"  {bid}: FAILED single phrase {phrases}")
    return m


def batches(todo: dict) -> list[list[str]]:
    out, cur, tot = [], [], 0
    for p, n in sorted(todo.items(), key=lambda kv: kv[1]):
        if n > BATCH_ROWS:
            out.append([p])
            continue
        if cur and (tot + n > BATCH_ROWS or len(cur) >= BATCH_PHRASES):
            out.append(cur)
            cur, tot = [], 0
        cur.append(p)
        tot += n
    if cur:
        out.append(cur)
    return out


def direct_todo(A, done: set) -> tuple[list[str], dict]:
    """Phrases for aliases not yet covered, without a count scan (mode 'direct').
    An alias is covered if its broad or core phrase was downloaded already; it
    is skipped if a cached count says its broad phrase (which contains the core)
    has no hits, or its core phrase is too wide."""
    todo, why = [], {"covered": 0, "zero_hits": 0, "too_wide": 0}
    for name, ps, sic in zip(A.name, A.phrases, A.sic):
        cp = core_phrase(name)
        if not cp:
            continue
        if cp in done or ps[0] in done:
            why["covered"] += 1
            continue
        c0 = cached_count(ps[0])
        if c0 == 0:
            why["zero_hits"] += 1
            continue
        cc = cached_count(cp)
        if cc == 0:
            why["zero_hits"] += 1
            continue
        if cc is not None and (cc > MAX_CORE or cc < 0):
            why["too_wide"] += 1
            continue
        todo.append((tier(sic), cp))
    # most contractor-like industries first (only the order of work, not the scope)
    return [c for _, c in sorted(set(todo))], why


TIER1 = [(1500, 1799), (3480, 3489), (3570, 3579), (3660, 3699), (3710, 3799), (3810, 3829),
         (4400, 4599), (4810, 4899), (4950, 4959), (7370, 7389), (8000, 8099), (8700, 8748), (8200, 8299)]


def tier(sic) -> int:
    if sic != sic:
        return 3
    if any(a <= sic <= b for a, b in TIER1):
        return 1
    if 2830 <= sic <= 2836 or 3840 <= sic <= 3851 or 7300 <= sic <= 7369:
        return 3
    return 2


def main_direct(workers: int):
    A = scope()
    A = A.merge(pd.read_csv(DATA / "universe.csv")[["cik", "sic"]], on="cik", how="left")
    A["phrases"] = A.name.map(search_phrases)
    A = A[A.phrases.map(len) > 0]
    todo, why = direct_todo(A, done_phrases())
    log(f"direct mode: {len(todo)} phrases to download; skipped {why}")
    bs = [todo[i:i + BATCH_PHRASES] for i in range(0, len(todo), BATCH_PHRASES)]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(one_batch, bs))
    for r in res:
        if r.get("capped") and len(r["phrases"]) > 1:
            h = len(r["phrases"]) // 2
            for part in (r["phrases"][:h], r["phrases"][h:]):
                one_batch(part)
    todo2, why2 = direct_todo(A, done_phrases())
    log(f"direct mode finished; still not covered: {len(todo2)} phrases")
    pd.DataFrame({"phrase": todo2}).to_csv(DATA / "dl_not_covered.csv", index=False)


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    A = scope()
    A["phrases"] = A.name.map(search_phrases)
    A = A[A.phrases.map(len) > 0]
    while True:
        ch, undecided = chosen_phrases(A)
        done = done_phrases()
        todo = {p: n for p, n in ch.items() if p not in done}
        scan_over = (DATA / "scan.csv").exists()          # written by stage 2 when it finishes
        log(f"chosen {len(ch)}, downloaded {len(done & set(ch))}, to do {len(todo)} "
            f"({sum(todo.values())} rows), undecided aliases {undecided}")
        if not todo:
            if scan_over or undecided == 0:
                break
            time.sleep(120)
            continue
        bs = batches(todo)
        # wait for a decent amount of work unless the scan is over
        if not scan_over and len(bs) < workers and undecided > 200:
            time.sleep(120)
            continue
        with ThreadPoolExecutor(max_workers=workers) as ex:
            res = list(ex.map(one_batch, bs[: max(workers * 2, 1)]))
        for r in res:
            if r.get("capped") and len(r["phrases"]) > 1:
                h = len(r["phrases"]) // 2
                for part in (r["phrases"][:h], r["phrases"][h:]):
                    one_batch(part)
    log("download stage finished")


if __name__ == "__main__":
    if "direct" in sys.argv:
        main_direct(int(sys.argv[1]) if sys.argv[1].isdigit() else 3)
    else:
        main()
