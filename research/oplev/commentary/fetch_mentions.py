#!/usr/bin/env python
"""
Operating-leverage commentary dataset from SEC EDGAR full-text search (FTS).

What it does
------------
For every (phrase x form) pair it pages through EDGAR FTS hits filed
2010-01-01 .. END_DATE, sliced by calendar quarter (auto-split to month / day if a
slice ever reaches the 10,000-hit retrieval cap), caches every JSON response under
cache/fts/, audits that the slice totals add up, and writes:

  mentions.csv.gz                  one row per (cik, accession, file_date, form, file_name, phrase)
  mentions_by_cik_quarter.csv.gz   firm x calendar-quarter counts per phrase group (+ clean-event counts)
  tone_mentions.csv.gz             same layout, supplementary direction phrases ("improved operating leverage", ...)
  clean_events.csv.gz              recommended clean event: one row per (cik, accession)
  clean_negative_events.csv.gz     the negative-tone counterpart
  fetch_audit.csv                  per (phrase, form, slice): reported total vs unique hits retrieved
  fetch_totals_check.csv           per (phrase, form): sum of slice totals vs full-range / yearly totals

Rerunnable: every request is cached, so a second run makes zero network calls
(use --offline to guarantee that).

    .venv/bin/python research/oplev/commentary/fetch_mentions.py [--offline] [--workers 6]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import re
import sys
import threading
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache" / "fts"
UA = "ClaudeSpace research dspinjr@gmail.com"
BASE = "https://efts.sec.gov/LATEST/search-index"
START_DATE = dt.date(2010, 1, 1)
END_DATE = dt.date(2026, 9, 23)
PAGE = 100            # FTS returns 100 hits per page (fixed server side)
CAP = 10_000          # from+size may not exceed 10,000 (from=10000 -> HTTP 500)
MAX_RPS = 7.5         # stay under SEC's 10 req/s fair-access limit (brief asked <= 8)

# key, exact phrase sent to FTS, phrase group
PHRASES = [
    ("operating_leverage",          "operating leverage",          "ol_any"),
    ("positive_operating_leverage", "positive operating leverage", "ol_positive"),
    ("negative_operating_leverage", "negative operating leverage", "ol_negative"),
    ("operating_deleverage",        "operating deleverage",        "ol_negative"),
    ("incremental_margin",          "incremental margin",          "incremental"),
    ("incremental_margins",         "incremental margins",         "incremental"),
    ("fixed_cost_absorption",       "fixed cost absorption",       "absorption"),
    ("fixed_cost_leverage",         "fixed-cost leverage",         "absorption"),
]
# Supplementary direction cues (NOT part of the brief's six phrase groups; kept in a separate file,
# tone_mentions.csv.gz). Added because "positive operating leverage" turned out to be ~87% bank
# language, and the validation sample showed negatives phrased as "reduced operating leverage".
# Fetched with yearly slices (each is far below the 10,000 cap; the audit checks it).
TONE_PHRASES = [
    ("improved_operating_leverage",   "improved operating leverage",   "tone_pos"),
    ("improving_operating_leverage",  "improving operating leverage",  "tone_pos"),
    ("favorable_operating_leverage",  "favorable operating leverage",  "tone_pos"),
    ("increased_operating_leverage",  "increased operating leverage",  "tone_pos"),
    ("better_operating_leverage",     "better operating leverage",     "tone_pos"),
    ("greater_operating_leverage",    "greater operating leverage",    "tone_pos"),
    ("higher_operating_leverage",     "higher operating leverage",     "tone_pos"),
    ("operating_leverage_on_higher",  "operating leverage on higher",  "tone_pos"),
    ("operating_leverage_from_higher", "operating leverage from higher", "tone_pos"),
    ("reduced_operating_leverage",    "reduced operating leverage",    "tone_neg"),
    ("lower_operating_leverage",      "lower operating leverage",      "tone_neg"),
    ("unfavorable_operating_leverage", "unfavorable operating leverage", "tone_neg"),
    ("less_operating_leverage",       "less operating leverage",       "tone_neg"),
    ("loss_of_operating_leverage",    "loss of operating leverage",    "tone_neg"),
    ("lack_of_operating_leverage",    "lack of operating leverage",    "tone_neg"),
    ("decreased_operating_leverage",  "decreased operating leverage",  "tone_neg"),
    ("operating_leverage_on_lower",   "operating leverage on lower",   "tone_neg"),
]
FORMS = ["8-K", "10-Q", "10-K"]
GROUPS = ["ol_any", "ol_positive", "ol_negative", "incremental", "absorption"]
SPAC_NAME = r"(?i)\b(?:acquisition corp|acquisition co\b|acquisition inc|acquisition ltd|acquisition holdings|merger corp|spac\b|blank check)"


# --------------------------------------------------------------------------- http
class RateLimiter:
    def __init__(self, rps: float):
        self.min_gap = 1.0 / rps
        self.lock = threading.Lock()
        self.next_t = 0.0

    def wait(self):
        with self.lock:
            now = time.monotonic()
            t = max(now, self.next_t)
            self.next_t = t + self.min_gap
        delay = t - time.monotonic()
        if delay > 0:
            time.sleep(delay)


LIMITER = RateLimiter(MAX_RPS)
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
STATS = {"network": 0, "cache": 0, "retries": 0}
STATS_LOCK = threading.Lock()
OFFLINE = False


def _bump(k, n=1):
    with STATS_LOCK:
        STATS[k] += n


def cache_path(phrase_key: str, form: str, start: dt.date, end: dt.date, frm: int) -> Path:
    return CACHE / phrase_key / form.replace("/", "_") / f"{start:%Y%m%d}_{end:%Y%m%d}_{frm:05d}.json"


def fts(phrase: str, phrase_key: str, form: str, start: dt.date, end: dt.date, frm: int = 0) -> dict:
    """One FTS page, cached. Retries with exponential backoff on 429 / 5xx / bad JSON."""
    p = cache_path(phrase_key, form, start, end, frm)
    if p.exists():
        try:
            d = json.loads(p.read_text())
            if "hits" in d:
                _bump("cache")
                return d
        except json.JSONDecodeError:
            pass
    if OFFLINE:
        raise RuntimeError(f"--offline but not cached: {p}")
    q = urllib.parse.quote(f'"{phrase}"')
    url = (f"{BASE}?q={q}&forms={urllib.parse.quote(form)}&dateRange=custom"
           f"&startdt={start:%Y-%m-%d}&enddt={end:%Y-%m-%d}")
    if frm:
        url += f"&from={frm}"
    last = None
    for attempt in range(9):
        LIMITER.wait()
        try:
            r = SESSION.get(url, timeout=60)
            _bump("network")
            if r.status_code == 200:
                d = r.json()
                if "hits" in d:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(json.dumps(d))
                    return d
                last = f"200 without hits: {r.text[:200]}"
            else:
                last = f"HTTP {r.status_code}: {r.text[:200]}"
        except (requests.RequestException, ValueError) as e:
            last = repr(e)
        _bump("retries")
        time.sleep(min(60, 1.5 * 2 ** attempt) + random.random())
    raise RuntimeError(f"FTS failed after retries: {url} :: {last}")


# ------------------------------------------------------------------------ slicing
def quarter_slices(a: dt.date, b: dt.date):
    out, y, q = [], a.year, (a.month - 1) // 3
    while True:
        s = dt.date(y, 3 * q + 1, 1)
        e = (dt.date(y + (q == 3), (3 * q + 3) % 12 + 1, 1) - dt.timedelta(days=1))
        if s > b:
            break
        out.append((max(s, a), min(e, b)))
        q += 1
        if q == 4:
            y, q = y + 1, 0
    return out


def year_slices(a: dt.date, b: dt.date):
    return [(max(dt.date(y, 1, 1), a), min(dt.date(y, 12, 31), b)) for y in range(a.year, b.year + 1)]


def split_slice(a: dt.date, b: dt.date):
    """Split into months if the slice spans more than one month, otherwise halves (days)."""
    if (a.year, a.month) != (b.year, b.month):
        out, cur = [], dt.date(a.year, a.month, 1)
        while cur <= b:
            nxt = dt.date(cur.year + (cur.month == 12), cur.month % 12 + 1, 1)
            out.append((max(cur, a), min(nxt - dt.timedelta(days=1), b)))
            cur = nxt
        return out
    if a == b:
        raise RuntimeError(f"single day {a} still over the {CAP} cap")
    mid = a + (b - a) // 2
    return [(a, mid), (mid + dt.timedelta(days=1), b)]


def fetch_slice(phrase, key, form, a, b, depth=0):
    """Return (list_of_hits, list_of_audit_rows) for one date slice, splitting if capped."""
    d0 = fts(phrase, key, form, a, b, 0)
    tot = d0["hits"]["total"]
    total, rel = int(tot["value"]), tot.get("relation", "eq")
    if rel != "eq" or total >= CAP:
        hits, audit = [], []
        for s, e in split_slice(a, b):
            h, au = fetch_slice(phrase, key, form, s, e, depth + 1)
            hits += h
            audit += au
        return hits, audit
    hits = list(d0["hits"]["hits"])
    for frm in range(PAGE, total, PAGE):
        hits += fts(phrase, key, form, a, b, frm)["hits"]["hits"]
    first_pass = len({h["_id"] for h in hits})
    repaired = False
    # Quirk: FTS pages are sorted by relevance score; with tied scores, from/size paging can
    # return one hit twice and silently skip another. Repair by re-fetching the slice as
    # smaller sub-slices (usually a single page each) and taking the union.
    if first_pass < total and a < b:
        repaired = True
        for s, e in split_slice(a, b):
            h, _ = fetch_slice(phrase, key, form, s, e, depth + 1)
            hits += h
    by_id = {}
    for h in hits:
        by_id.setdefault(h["_id"], h)
    hits = list(by_id.values())
    audit = [dict(phrase_key=key, form=form, start=a.isoformat(), end=b.isoformat(), depth=depth,
                  reported_total=total, relation=rel, unique_ids_first_pass=first_pass, repaired=repaired,
                  hits_returned=len(hits), unique_ids=len(hits))]
    return hits, audit


# ----------------------------------------------------------------------- building
def hit_rows(hit: dict, key: str, phrase: str, group: str, qform: str):
    s = hit["_source"]
    _id = hit["_id"]
    adsh_from_id, _, fname = _id.partition(":")
    ciks = s.get("ciks") or []
    names = s.get("display_names") or []
    sics = s.get("sics") or []
    items = s.get("items") or []
    rows = []
    for i, c in enumerate(ciks):
        rows.append(dict(
            cik=int(c),
            adsh=s.get("adsh") or adsh_from_id,
            file_date=s.get("file_date"),
            form=s.get("form"),
            root_form=";".join(s.get("root_forms") or []) or qform,
            query_form=qform,
            file_name=fname,
            file_type=s.get("file_type"),
            file_description=s.get("file_description"),
            phrase=phrase,
            phrase_key=key,
            phrase_group=group,
            display_name=names[i] if len(names) == len(ciks) else "; ".join(names),
            all_display_names="; ".join(names),
            n_ciks=len(ciks),
            sic=(sics[i] if len(sics) == len(ciks) else (sics[0] if len(sics) == 1 else None)),
            all_sics=";".join(sics),
            items=";".join(items),
            period_ending=s.get("period_ending"),
            biz_state=";".join(s.get("biz_states") or []),
        ))
    return rows


def doc_role(form: str, file_type: str | None, fname: str) -> str:
    ft = (file_type or "").upper().strip()
    fn = fname.lower()
    if ft.startswith("EX-99") or (not ft and re.search(r"ex[-_ ]?99", fn)):
        return "ex99"
    if ft.startswith("EX-13"):
        return "ex13_annual_report"
    if ft.startswith("EX-"):
        return "other_exhibit"
    base = (form or "").upper()
    if ft in (base, base.replace("/A", ""), base + "/A") or ft.startswith(("10-K", "10-Q", "8-K")):
        return "main"
    if re.search(r"ex[-_ ]?99", fn):
        return "ex99"
    return "other"


def cal_quarter(d: pd.Series) -> pd.Series:
    d = pd.to_datetime(d)
    return d.dt.year.astype(str) + "Q" + d.dt.quarter.astype(str)


COLS = ["cik", "adsh", "file_date", "cal_quarter", "year", "query_form", "form", "root_form", "is_amendment",
        "file_name", "file_type", "file_description", "doc_role", "is_ex99", "is_main_doc",
        "is_earnings_8k", "items", "phrase", "phrase_key", "phrase_group", "display_name",
        "all_display_names", "n_ciks", "sic", "sic2", "is_financial", "all_sics", "period_ending",
        "biz_state", "url"]


def prep_rows(rows: list[dict]) -> tuple[pd.DataFrame, int]:
    m = pd.DataFrame(rows)
    n_raw = len(m)
    key_cols = ["cik", "adsh", "file_date", "form", "file_name", "phrase"]
    m = m.drop_duplicates(key_cols).reset_index(drop=True)
    m["doc_role"] = [doc_role(f, t, n) for f, t, n in zip(m["form"], m["file_type"], m["file_name"])]
    m["is_ex99"] = m["doc_role"].eq("ex99")
    m["is_main_doc"] = m["doc_role"].eq("main")
    m["is_amendment"] = m["form"].fillna("").str.endswith("/A")
    m["is_earnings_8k"] = m["root_form"].str.contains("8-K") & m["items"].fillna("").str.split(";").apply(lambda x: "2.02" in x)
    sicnum = pd.to_numeric(m["sic"], errors="coerce")
    m["sic2"] = (sicnum // 100).astype("Int64")
    m["is_financial"] = sicnum.between(6000, 6999)
    m["cal_quarter"] = cal_quarter(m["file_date"])
    m["year"] = pd.to_datetime(m["file_date"]).dt.year
    m["url"] = ("https://www.sec.gov/Archives/edgar/data/" + m["cik"].astype(str) + "/"
                + m["adsh"].str.replace("-", "", regex=False) + "/" + m["file_name"])
    m = m.sort_values(["file_date", "cik", "adsh", "file_name", "phrase_key"]).reset_index(drop=True)
    return m[COLS], n_raw - len(m)


def filing_set(df: pd.DataFrame, mask) -> set:
    d = df[mask]
    return set(zip(d.cik, d.adsh))


def build_outputs(all_rows: list[dict], tone_rows: list[dict]):
    m, dropped = prep_rows(all_rows)
    m.to_csv(HERE / "mentions.csv.gz", index=False)
    print(f"mentions.csv.gz: {len(m):,} rows ({dropped:,} duplicate rows dropped)")
    t, dropped = prep_rows(tone_rows)
    t.to_csv(HERE / "tone_mentions.csv.gz", index=False)
    print(f"tone_mentions.csv.gz: {len(t):,} rows ({dropped:,} duplicate rows dropped)")

    # ---- recommended clean event (see README / precision_sample*.md)
    # A filing (cik, accession) is a clean "management talks up its operating leverage" event when:
    #   * the exact phrase "operating leverage" matched,
    #   * in an 8-K EX-99 exhibit or 8-K main doc, a 10-Q main doc, or a 10-K main doc / EX-13,
    #   * the filing is an original (not an /A amendment),
    #   * the filer's SIC (as reported on the filing) is known and outside 6000-6999,
    #   * the filer name does not look like a SPAC (SPACs with non-6770 SICs slip past the SIC screen),
    #   * and the same filing matched none of the negative phrases ("negative operating leverage",
    #     "operating deleverage", or the supplementary "reduced/lower/unfavorable/... operating leverage").
    #     Those filings form clean_negative_events.csv.gz instead.
    # Columns pos_cue / kicking_in mark the stricter subset with a positive direction word
    # ("improved/favorable/increased/better/greater/higher operating leverage", "operating leverage
    # on/from higher") in the same filing.
    excl = m["sic"].isna() | m["is_financial"] | m["display_name"].str.contains(SPAC_NAME, regex=True)
    ok_doc = ((m.query_form.eq("8-K") & m.doc_role.isin(["ex99", "main"]))
              | (m.query_form.eq("10-Q") & m.doc_role.eq("main"))
              | (m.query_form.eq("10-K") & m.doc_role.isin(["main", "ex13_annual_report"])))
    t_ok = ~t.is_amendment
    neg_set = filing_set(m, m.phrase_group.eq("ol_negative")) | filing_set(t, t.phrase_group.eq("tone_neg") & t_ok)
    pos_mod_set = filing_set(t, t.phrase_group.eq("tone_pos") & t_ok)
    pos_phrase_set = filing_set(m, m.phrase_key.eq("positive_operating_leverage"))
    base = m[m.phrase_key.eq("operating_leverage") & ok_doc & ~m.is_amendment & ~excl].copy()
    base["is_neg"] = [(c, a) in neg_set for c, a in zip(base.cik, base.adsh)]
    base["event_channel"] = base.query_form.map({"8-K": "8-K", "10-Q": "10-Q", "10-K": "10-K"})
    base["is_earnings_release"] = base.is_earnings_8k & base.is_ex99

    def collapse(df):
        out = (df.sort_values(["cik", "adsh", "file_name"])
               .groupby(["cik", "adsh"], as_index=False)
               .agg(file_date=("file_date", "first"), cal_quarter=("cal_quarter", "first"), year=("year", "first"),
                    form=("form", "first"), event_channel=("event_channel", "first"),
                    is_earnings_release=("is_earnings_release", "max"), items=("items", "first"),
                    n_files_matched=("file_name", "nunique"), file_names=("file_name", lambda s: ";".join(s)),
                    display_name=("display_name", "first"), sic=("sic", "first"), sic2=("sic2", "first"),
                    period_ending=("period_ending", "first"), url=("url", "first")))
        out["pos_phrase"] = [(c, a) in pos_phrase_set for c, a in zip(out.cik, out.adsh)]
        out["pos_modifier"] = [(c, a) in pos_mod_set for c, a in zip(out.cik, out.adsh)]
        out["pos_cue"] = out.pos_phrase | out.pos_modifier
        return out.sort_values(["file_date", "cik"]).reset_index(drop=True)

    ev = collapse(base[~base.is_neg])
    ev["kicking_in"] = ev.pos_cue & ev.event_channel.isin(["8-K", "10-Q"])
    ev.to_csv(HERE / "clean_events.csv.gz", index=False)
    negev = collapse(base[base.is_neg])
    negev.to_csv(HERE / "clean_negative_events.csv.gz", index=False)
    print(f"clean_events.csv.gz: {len(ev):,} filings, {ev.cik.nunique():,} CIKs "
          f"(kicking_in subset {int(ev.kicking_in.sum()):,}); clean_negative_events.csv.gz: {len(negev):,} filings")

    # ---- firm x calendar quarter
    # Counts = number of distinct FILINGS (accessions) with >=1 matching file, per phrase group.
    g = m.groupby(["cik", "cal_quarter", "phrase_group"])["adsh"].nunique().unstack("phrase_group")
    g = g.reindex(columns=GROUPS).fillna(0).astype(int)
    p1 = m[m.phrase_group == "ol_any"]
    splits = {
        "ol_any_release": p1[p1.is_earnings_8k & p1.is_ex99],          # 8-K Item 2.02 earnings-release exhibits
        "ol_any_8k_other": p1[p1.root_form.str.contains("8-K") & ~(p1.is_earnings_8k & p1.is_ex99)],
        "ol_any_10q": p1[p1.root_form.str.contains("10-Q")],
        "ol_any_10k": p1[p1.root_form.str.contains("10-K")],
    }
    for name, sub in splits.items():
        g[name] = sub.groupby(["cik", "cal_quarter"])["adsh"].nunique().reindex(g.index).fillna(0).astype(int)
    g["net_tone"] = g["ol_positive"] - g["ol_negative"]
    # supplementary direction cues, restricted to filings that also matched "operating leverage" etc.
    for grp in ["tone_pos", "tone_neg"]:
        g[grp + "_mod"] = (t[t.phrase_group.eq(grp)].groupby(["cik", "cal_quarter"])["adsh"].nunique()
                           .reindex(g.index).fillna(0).astype(int))
    pos_any = pd.concat([m[m.phrase_group.eq("ol_positive")], t[t.phrase_group.eq("tone_pos")]])
    neg_any = pd.concat([m[m.phrase_group.eq("ol_negative")], t[t.phrase_group.eq("tone_neg")]])
    g["net_tone_broad"] = (pos_any.groupby(["cik", "cal_quarter"])["adsh"].nunique().reindex(g.index).fillna(0)
                           - neg_any.groupby(["cik", "cal_quarter"])["adsh"].nunique().reindex(g.index).fillna(0)).astype(int)
    g["ol_clean"] = ev.groupby(["cik", "cal_quarter"])["adsh"].nunique().reindex(g.index).fillna(0).astype(int)
    g["ol_kicking_in"] = (ev[ev.kicking_in].groupby(["cik", "cal_quarter"])["adsh"].nunique()
                          .reindex(g.index).fillna(0).astype(int))
    g["ol_clean_negative"] = negev.groupby(["cik", "cal_quarter"])["adsh"].nunique().reindex(g.index).fillna(0).astype(int)
    g["n_filings_any_phrase"] = m.groupby(["cik", "cal_quarter"])["adsh"].nunique().reindex(g.index)
    g["first_file_date"] = m.groupby(["cik", "cal_quarter"])["file_date"].min().reindex(g.index)
    for grp in ["ol_any", "ol_positive", "ol_negative"]:
        g[f"first_file_date_{grp}"] = (m[m.phrase_group == grp].groupby(["cik", "cal_quarter"])["file_date"].min()
                                       .reindex(g.index))
    g["first_file_date_ol_clean"] = ev.groupby(["cik", "cal_quarter"])["file_date"].min().reindex(g.index)
    g["first_file_date_ol_kicking_in"] = ev[ev.kicking_in].groupby(["cik", "cal_quarter"])["file_date"].min().reindex(g.index)
    g["last_file_date"] = m.groupby(["cik", "cal_quarter"])["file_date"].max().reindex(g.index)
    meta = (m.sort_values("file_date").groupby("cik")
            .agg(display_name=("display_name", "last"), sic=("sic", lambda s: s.dropna().iloc[-1] if s.notna().any() else None)))
    g = g.reset_index().merge(meta, on="cik", how="left")
    sicnum = pd.to_numeric(g["sic"], errors="coerce")
    g["sic2"] = (sicnum // 100).astype("Int64")
    g["is_financial"] = sicnum.between(6000, 6999)
    g = g.sort_values(["cik", "cal_quarter"]).reset_index(drop=True)
    g.to_csv(HERE / "mentions_by_cik_quarter.csv.gz", index=False)
    print(f"mentions_by_cik_quarter.csv.gz: {len(g):,} firm-quarters, {g.cik.nunique():,} CIKs")
    return m, g


# --------------------------------------------------------------------------- main
def main():
    global OFFLINE
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="use cache only, never hit the network")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    OFFLINE = args.offline
    CACHE.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    q_sl, y_sl = quarter_slices(START_DATE, END_DATE), year_slices(START_DATE, END_DATE)
    jobs = ([(k, ph, grp, f, a, b) for (k, ph, grp) in PHRASES for f in FORMS for (a, b) in q_sl]
            + [(k, ph, grp, f, a, b) for (k, ph, grp) in TONE_PHRASES for f in FORMS for (a, b) in y_sl])
    tone_keys = {k for k, _, _ in TONE_PHRASES}
    all_rows, tone_rows, audit = [], [], []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(fetch_slice, ph, k, f, a, b): (k, ph, grp, f, a, b) for (k, ph, grp, f, a, b) in jobs}
        done = 0
        for fut in as_completed(futs):
            k, ph, grp, f, a, b = futs[fut]
            hits, au = fut.result()
            audit += au
            target = tone_rows if k in tone_keys else all_rows
            for h in hits:
                target += hit_rows(h, k, ph, grp, f)
            done += 1
            if done % 200 == 0:
                print(f"  {done}/{len(jobs)} slices  net={STATS['network']} cache={STATS['cache']} "
                      f"retries={STATS['retries']}  {time.time() - t0:.0f}s", flush=True)

    aud = pd.DataFrame(audit).sort_values(["phrase_key", "form", "start"])
    aud["ok"] = (aud.reported_total == aud.unique_ids) & (aud.hits_returned == aud.reported_total)
    aud.to_csv(HERE / "fetch_audit.csv", index=False)

    # ---- totals check: sum of slice totals vs the full-range total (or yearly totals when capped)
    checks = []
    for (k, ph, grp) in PHRASES + TONE_PHRASES:
        for f in FORMS:
            sub = aud[(aud.phrase_key == k) & (aud.form == f)]
            d = fts(ph, k, f, START_DATE, END_DATE, 0)["hits"]["total"]
            row = dict(phrase_key=k, form=f, full_range_total=d["value"], full_range_relation=d["relation"],
                       sum_slice_totals=int(sub.reported_total.sum()), sum_unique_retrieved=int(sub.unique_ids.sum()),
                       slices=len(sub), slices_split_below_base=int((sub.depth > 0).sum()),
                       slices_repaired=int(sub.repaired.sum()), slices_not_ok=int((~sub.ok).sum()))
            if d["relation"] == "eq":
                row["totals_match"] = row["sum_slice_totals"] == d["value"]
            else:  # capped: compare year by year
                mism = 0
                for y in range(START_DATE.year, END_DATE.year + 1):
                    a, b = dt.date(y, 1, 1), min(dt.date(y, 12, 31), END_DATE)
                    yt = fts(ph, k, f, a, b, 0)["hits"]["total"]
                    ys = sub[sub.start.str[:4] == str(y)].reported_total.sum()
                    if yt["relation"] != "eq" or int(yt["value"]) != int(ys):
                        mism += 1
                row["totals_match"] = mism == 0
                row["note"] = f"full range capped at 10,000; checked {END_DATE.year - START_DATE.year + 1} yearly totals, mismatches={mism}"
            checks.append(row)
    chk = pd.DataFrame(checks)
    chk.to_csv(HERE / "fetch_totals_check.csv", index=False)
    print(chk.to_string(index=False))
    print(f"slices audited: {len(aud)}, not ok: {(~aud.ok).sum()}")

    build_outputs(all_rows, tone_rows)
    print(f"done in {time.time() - t0:.0f}s  network={STATS['network']} cache={STATS['cache']} retries={STATS['retries']}")


if __name__ == "__main__":
    main()
