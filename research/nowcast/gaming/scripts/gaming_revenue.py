#!/usr/bin/env python3
"""Gaming (casino) revenue by quarter from the dimensional XBRL of 10-Q/10-K filings, as first
reported.  Needed for the PREREG coverage rule ("reported gaming revenue that quarter, or total
revenue if gaming revenue isn't split out"): after ASC 606 (2018) most casino companies report
gaming revenue as a disaggregation line, which XBRL tags as revenue with a product/service member
(e.g. us-gaap:CasinoMember, byd:GamingMember).  The companyfacts API omits dimensional facts, so the
filing instances are read directly (cache/sec/instances/).

Rule: in each instance, revenue facts (RevenueFromContractWithCustomerExcludingAssessedTax,
Revenues, RevenueFromContractWithCustomerIncludingAssessedTax) whose context has exactly one
dimension, srt:ProductOrServiceAxis (or us-gaap's older ProductOrServiceAxis), with a member whose
name contains 'Gaming' or 'Casino' but not online/interactive/digital/igaming/sports/management/
other/retail/lottery words.  If several members qualify, the one with the largest value (the total
gaming line) is taken.  Quarterly values: 3-month facts; Q4 = FY - 9M YTD from the same filing set.
First reported = earliest filing carrying the quarter.

Output data/gaming_rev_dim.csv.gz: company, qend, gaming_rev, member, tag, accn, filed, how.
"""
import re, sys, time, json
from pathlib import Path
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CACHE = ROOT / "cache" / "sec" / "instances"
UA = {"User-Agent": "ClaudeSpace research dspinjr@gmail.com", "Accept-Encoding": "gzip, deflate"}
_last = [0.0]
TAGS = ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
        "RevenueFromContractWithCustomerIncludingAssessedTax")
BAD = re.compile(r"online|interactive|digital|igaming|sports|management|other|retail|lottery|nongaming|non_gaming|NonGaming|Racing|Hotel|Food|Beverage|Wagering", re.I)
COMPANIES = ["PENN", "PNK", "BYD", "ERI_CZR", "CZR_OLD", "BALY", "RRR", "MCRI", "CNTY", "FLL", "CHDN",
             "MGM", "WYNN", "GDEN", "ISLE", "TPCA", "DDE", "NYNY"]


import threading
_lock = threading.Lock()


def get(url, binary=False):
    for attempt in range(4):
        with _lock:   # global throttle: <= ~7 requests per second across threads
            dt = time.time() - _last[0]
            if dt < 0.14:
                time.sleep(0.14 - dt)
            _last[0] = time.time()
        try:
            r = requests.get(url, headers=UA, timeout=25)
            if r.status_code == 200:
                return r.content if binary else r.json()
            if r.status_code == 404:
                return None
        except Exception:
            pass
        time.sleep(2 * (attempt + 1))
    return None


def primary_docs() -> dict:
    """accession -> primaryDocument, from the cached EDGAR submissions files (scripts/sec_fetch.py)."""
    import gzip
    out = {}
    for f in (ROOT / "cache" / "sec" / "submissions").glob("*.json.gz"):
        j = json.load(gzip.open(f, "rt"))
        r = j["filings"]["recent"] if "filings" in j else j
        for a, d in zip(r.get("accessionNumber", []), r.get("primaryDocument", [])):
            out[a] = d
    return out


PRIMARY = {}


def instance_path(cik: int, accn: str) -> Path | None:
    p = CACHE / f"{accn}.xml"
    if p.exists():
        return p if p.stat().st_size > 0 else None
    base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn.replace('-', '')}/"
    CACHE.mkdir(parents=True, exist_ok=True)
    doc = PRIMARY.get(accn, "")
    b = None
    if doc.endswith(".htm"):   # inline XBRL: the extracted instance is <primary>_htm.xml
        b = get(base + doc[:-4] + "_htm.xml", binary=True)
    if not b:
        idx = get(base + "index.json")
        if idx:
            names = [it["name"] for it in idx["directory"]["item"]]
            cand = [n for n in names if n.endswith("_htm.xml")] or \
                   [n for n in names if n.endswith(".xml") and not re.search(r"_(cal|def|lab|pre)\.xml$", n)
                    and n != "FilingSummary.xml"]
            if cand:
                b = get(base + cand[0], binary=True)
    p.write_bytes(b or b"")
    return p if b else None


def parse(p: Path) -> pd.DataFrame:
    x = p.read_text(errors="ignore")
    ctx = {}
    for m in re.finditer(r'<(?:xbrli:)?context id="([^"]+)">(.*?)</(?:xbrli:)?context>', x, re.S):
        body = m.group(2)
        mem = re.findall(r'<xbrldi:explicitMember dimension="([^"]+)">([^<]+)</xbrldi:explicitMember>', body)
        if len(mem) != 1 or "ProductOrServiceAxis" not in mem[0][0]:
            continue
        st = re.search(r"<(?:xbrli:)?startDate>([^<]+)", body); en = re.search(r"<(?:xbrli:)?endDate>([^<]+)", body)
        if st and en:
            ctx[m.group(1)] = (st.group(1), en.group(1), mem[0][1])
    rows = []
    for m in re.finditer(r'<us-gaap:(\w+)\b([^>]*)>([^<]*)</us-gaap:\1>', x):
        tag, attrs, v = m.groups()
        if tag not in TAGS:
            continue
        c = re.search(r'contextRef="([^"]+)"', attrs)
        if not c or c.group(1) not in ctx:
            continue
        st, en, mem = ctx[c.group(1)]
        name = mem.split(":")[-1]
        if not re.search(r"gaming|casino", name, re.I) or BAD.search(name):
            continue
        try:
            rows.append(dict(tag=tag, start=st, end=en, member=mem, val=float(v)))
        except ValueError:
            pass
    return pd.DataFrame(rows)


def main():
    fil = pd.read_csv(DATA / "filings.csv.gz", parse_dates=["filed"])
    fil = fil[fil["form"].isin(["10-Q", "10-K"]) & (fil["filed"] >= "2018-01-01") & fil["company"].isin(COMPANIES)]
    PRIMARY.update(primary_docs())
    from concurrent.futures import ThreadPoolExecutor
    jobs = list(fil.sort_values("filed").itertuples())
    with ThreadPoolExecutor(4) as ex:
        paths = list(ex.map(lambda f: instance_path(int(f.cik), f.accn), jobs))
    facts = []
    for f, p in zip(jobs, paths):
        if p is None:
            continue
        d = parse(p)
        if len(d):
            d["company"] = f.company; d["accn"] = f.accn; d["filed"] = f.filed
            facts.append(d)
    F = pd.concat(facts, ignore_index=True)
    F["start"] = pd.to_datetime(F["start"]); F["end"] = pd.to_datetime(F["end"])
    F["days"] = (F["end"] - F["start"]).dt.days
    # one value per (company, filing, period): the largest qualifying member (the total gaming line)
    F = F.sort_values("val", ascending=False).drop_duplicates(["company", "accn", "start", "end"])
    # first reported per (company, period)
    F = F.sort_values("filed").drop_duplicates(["company", "start", "end"], keep="first")
    out = []
    for c, d in F.groupby("company"):
        q3 = d[d["days"].between(80, 100)]
        for _, r in q3.iterrows():
            out.append(dict(company=c, qend=r["end"].date(), gaming_rev=r["val"], member=r["member"], tag=r["tag"],
                            accn=r["accn"], filed=r["filed"].date(), how="3M"))
        have = set(q3["end"])
        for _, r in d[d["days"].between(350, 380)].iterrows():
            if r["end"] in have:
                continue
            ytd = d[(d["start"] == r["start"]) & ((r["end"] - d["end"]).dt.days.between(80, 100))]
            if len(ytd):
                y = ytd.iloc[0]
                out.append(dict(company=c, qend=r["end"].date(), gaming_rev=r["val"] - y["val"], member=r["member"],
                                tag=r["tag"], accn=r["accn"], filed=r["filed"].date(), how="FY-9M"))
    o = pd.DataFrame(out).sort_values(["company", "qend"])
    o.to_csv(DATA / "gaming_rev_dim.csv.gz", index=False)
    print(o.groupby("company").agg(n=("qend", "size"), first=("qend", "min"), last=("qend", "max"),
                                   members=("member", lambda s: ",".join(sorted(set(m.split(':')[-1] for m in s))))).to_string())


if __name__ == "__main__":
    main()
