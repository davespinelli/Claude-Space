#!/usr/bin/env python3
"""SEC data for the casino nowcast pilot (PREREG.md steps 4 and 7).

Downloads (cached in cache/sec/, never re-downloaded unless --refresh):
  * companyfacts JSON  https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
  * submissions JSON   https://data.sec.gov/submissions/CIK##########.json (+ older shard files)
User-Agent carries dspinjr@gmail.com; requests are throttled to <= ~7.5 per second.

Outputs
  data/financials_q.csv.gz   one row per company x fiscal quarter, values AS FIRST REPORTED:
      revenue, gaming_rev (us-gaap:CasinoRevenue when tagged without dimensions), op_income,
      da (depreciation & amortisation), ebitda = op_income + da (op_income alone when D&A is
      missing; flagged), shares (dei:EntityCommonStockSharesOutstanding, latest cover value),
      and the filing date of the first report.
  data/filings.csv.gz        8-K Item 2.02 filings and 10-Q/10-K filings per company.

"As first reported": for every tag and every (start, end) period the value is taken from the
filing with the earliest `filed` date that carried it (later restatements and re-casts in
comparatives are ignored).  Quarterly values:
  * a 3-month fact (duration 80-100 days) when one exists;
  * otherwise, for Q2/Q3, the difference of first-reported year-to-date facts (6M - 3M, 9M - 6M),
    which is how cash-flow-only items such as D&A are usually available;
  * Q4 = fiscal-year value (duration 350-380 days, from the 10-K) minus the first-reported
    Q1 + Q2 + Q3 values (PREREG step 3 / the brief).  Q4 is only derived when all three are present.
Across tags, the value filed earliest wins (ties: tag priority below); `<item>_tagspread` records how far
the candidate tags disagree for that quarter.  Revenue concept: candidates Revenues,
RevenueFromContractWithCustomerExcludingAssessedTax, RevenueFromContractWithCustomerIncludingAssessedTax,
SalesRevenueNet, SalesRevenueServicesNet (each taken as first reported).  Casino companies before
2018 showed gross revenues less promotional allowances; the tagged `Revenues` total is checked in
run notes against net revenues (see fin_checks in results.json).
D&A concept: first available of DepreciationDepletionAndAmortization, DepreciationAndAmortization,
DepreciationAmortizationAndAccretionNet, CostOfGoodsAndServicesSoldDepreciationAndAmortization,
Depreciation (+ AmortizationOfIntangibleAssets when only Depreciation is tagged).
"""
import gzip, json, sys, time
from pathlib import Path
import pandas as pd
import numpy as np
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "sec"
DATA = ROOT / "data"
UA = {"User-Agent": "ClaudeSpace research dspinjr@gmail.com", "Accept-Encoding": "gzip, deflate"}

# company key -> CIKs (a company can span two registrants).  Verified against EDGAR submissions.
COMPANIES = {
    "PENN": [921738],
    "PNK_OLD": [356213],      # Pinnacle Entertainment before the April 2016 GLPI transaction
    "PNK": [1656239],         # Pinnacle Entertainment OpCo April 2016 - Oct 2018
    "BYD": [906553],
    "ERI_CZR": [1590895],     # Eldorado Resorts, renamed Caesars Entertainment Inc 2020-07-20
    "CZR_OLD": [858339],      # Caesars Entertainment Corp (Harrah's) until 2020-07-20
    "ISLE": [863015],
    "TPCA": [1476246],
    "BALY": [1747079],        # Twin River Worldwide Holdings -> Bally's Corp
    "DDE": [1162556],
    "NYNY": [906780],
    "GDEN": [1071255],        # Lakes Entertainment -> Golden Entertainment
    "RRR": [1653653],
    "MCRI": [907242],
    "CNTY": [911147],
    "FLL": [891482],
    "CHDN": [20212],
    "MGM": [789570],
    "WYNN": [1174922],
    "MNTG": [834162],
    "AFFI": [1499268],
    "CACQ": [1575879],
}

REV_TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet",
            "SalesRevenueServicesNet"]
DA_TAGS = ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
           "DepreciationAmortizationAndAccretionNet",
           "CostOfGoodsAndServicesSoldDepreciationAndAmortization"]
OI_TAGS = ["OperatingIncomeLoss"]
GAMING_TAGS = ["CasinoRevenue"]

_last = [0.0]


def get(url: str, cache: Path, refresh=False):
    if cache.exists() and not refresh:
        with gzip.open(cache, "rt") as f:
            return json.load(f)
    for attempt in range(6):
        dt = time.time() - _last[0]
        if dt < 0.14:
            time.sleep(0.14 - dt)
        try:
            r = requests.get(url, headers=UA, timeout=60)
            _last[0] = time.time()
            if r.status_code == 200:
                j = r.json()
                cache.parent.mkdir(parents=True, exist_ok=True)
                with gzip.open(cache, "wt") as f:
                    json.dump(j, f)
                return j
            if r.status_code == 404:
                return None
        except Exception as e:  # network hiccup
            print("  retry", url, e, file=sys.stderr)
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed {url}")


def facts_frame(cf: dict, tags: list[str], taxonomy="us-gaap", unit="USD") -> pd.DataFrame:
    rows = []
    g = cf.get("facts", {}).get(taxonomy, {})
    for pri, t in enumerate(tags):   # supplements from filing instances (see INSTANCE_SUPPLEMENT)
        for f in cf.get("_supplement", {}).get(t, []):
            rows.append(dict(tag=t, pri=pri, **f))
    for pri, t in enumerate(tags):
        if t not in g:
            continue
        for f in g[t]["units"].get(unit, []):
            if "start" not in f:
                continue
            rows.append(dict(tag=t, pri=pri, start=f["start"], end=f["end"], val=f["val"],
                             filed=f["filed"], form=f.get("form", ""), accn=f["accn"]))
    if not rows:
        return pd.DataFrame(columns=["tag", "pri", "start", "end", "val", "filed", "form", "accn"])
    df = pd.DataFrame(rows)
    df["start"] = pd.to_datetime(df["start"]); df["end"] = pd.to_datetime(df["end"])
    df["filed"] = pd.to_datetime(df["filed"])
    df["days"] = (df["end"] - df["start"]).dt.days
    # first reported per (tag, start, end)
    df = df.sort_values(["filed", "accn"]).drop_duplicates(["tag", "start", "end"], keep="first")
    return df


def quarterly(df: pd.DataFrame, rule: str = "priority") -> pd.DataFrame:
    """First-reported quarterly values per quarter end, choosing the highest-priority tag that
    yields a value.  For each tag and each candidate quarter end e (in date order):
      1. a 3-month fact (80-100 days) ending at e                               how = 3M
      2. if e is a fiscal-year end: FY fact - (Q1 + Q2 + Q3) already derived   how = FY-Q123
      3. same-start difference: fact(s, e) - fact(s, e') with e - e' = 80-100 days   how = YTDdiff
      4. stub sum: fact(s, x) + fact(x+1, e) spanning 80-100 days (predecessor/successor split,
         e.g. Bally's Q1 2025)                                                  how = stubsum
    Columns: end, start, val, filed, how, tag, pri."""
    out = []
    for tag, d in df.groupby("tag"):
        pri = d["pri"].iloc[0]
        d = d.sort_values("filed")
        ends = sorted(set(d.loc[d.days >= 28, "end"]))
        rec = {}
        for e in ends:
            de = d[d.end == e]
            q3m = de[(de.days >= 80) & (de.days <= 100)]
            if len(q3m):
                r = q3m.iloc[0]
                rec[e] = dict(end=e, start=r.start, val=r.val, filed=r.filed, how="3M", tag=tag, pri=pri)
                continue
            fy = de[(de.days >= 350) & (de.days <= 380)]
            if len(fy):
                r = fy.iloc[0]
                qs = []
                for k in range(1, 4):
                    target = e - pd.DateOffset(months=3 * k)
                    cand = [x for x in rec.values() if abs((x["end"] - target).days) <= 10]
                    if not cand:
                        break
                    qs.append(cand[0])
                if len(qs) == 3 and qs[-1]["start"] >= r.start - pd.Timedelta(days=10):
                    rec[e] = dict(end=e, start=qs[0]["end"] + pd.Timedelta(days=1),
                                  val=r.val - sum(q["val"] for q in qs), filed=r.filed, how="FY-Q123",
                                  tag=tag, pri=pri)
                    continue
            done = False
            for _, a in de[de.days > 100].iterrows():
                b = d[(d.start == a.start) & ((a.end - d.end).dt.days.between(80, 100))]
                if len(b):
                    b = b.iloc[0]
                    rec[e] = dict(end=e, start=b.end + pd.Timedelta(days=1), val=a.val - b.val,
                                  filed=max(a.filed, b.filed), how="YTDdiff", tag=tag, pri=pri)
                    done = True
                    break
            if done:
                continue
            for _, a in de[de.days < 80].iterrows():
                b = d[(d.end == a.start - pd.Timedelta(days=1)) & ((a.end - d.start).dt.days.between(80, 100))]
                if len(b):
                    b = b.iloc[0]
                    rec[e] = dict(end=e, start=b.start, val=a.val + b.val, filed=max(a.filed, b.filed),
                                  how="stubsum", tag=tag, pri=pri)
                    break
        out.extend(rec.values())
    if not out:
        return pd.DataFrame(columns=["end", "start", "val", "filed", "how", "tag", "pri"])
    q = pd.DataFrame(out)
    return q if rule == "__all__" else choose(q, rule)


def quarterly_all(df: pd.DataFrame) -> pd.DataFrame:
    """All per-tag quarterly candidates (no choice across tags)."""
    return quarterly(df, rule="__all__")


def choose(q: pd.DataFrame, rule: str, anchor: pd.DataFrame | None = None) -> pd.DataFrame:
    """Pick one value per quarter across candidate tags.
    Only candidates from the FIRST filing that reported the quarter are eligible (filed within 7
    days of the earliest candidate), which is what "as first reported" means.  Among those:
      rule 'priority': tag priority order;
      rule 'revenue' : drop values <= 0; if an anchor (operating income + CostsAndExpenses, i.e. net
                       revenue by identity) exists, the candidate closest to it; else the smallest
                       (casino filers before 2018 tagged both gross revenues and net revenues after
                       promotional allowances; the net figure is the smaller one).
    tag_spread = relative disagreement among all candidates (diagnostic)."""
    if not len(q):
        return q
    if rule == "revenue":
        q = q[q["val"] > 0]
    spread = q.groupby("end")["val"].agg(lambda v: (v.max() - v.min()) / max(abs(v).max(), 1))
    first = q.groupby("end")["filed"].transform("min")
    q = q[q["filed"] <= first + pd.Timedelta(days=7)].copy()
    if rule == "revenue":
        if anchor is not None and len(anchor):
            q = q.merge(anchor[["end", "val"]].rename(columns={"val": "anchor"}), on="end", how="left")
        else:
            q["anchor"] = np.nan
        q["dist"] = np.where(q["anchor"].notna(), (q["val"] - q["anchor"]).abs(), q["val"])
        q = q.sort_values(["end", "dist", "pri"])
    else:
        q = q.sort_values(["end", "pri"])
    q = q.drop_duplicates("end", keep="first").drop(columns=[c for c in ("anchor", "dist") if c in q])
    q["tag_spread"] = q["end"].map(spread)
    return q


def fill_identity(target, other, cx, sign, label):
    """Fill quarters missing from `target` with other + sign*CostsAndExpenses (revenue = operating
    income + total operating costs; operating income = revenue - total operating costs)."""
    if not len(other) or not len(cx):
        return target
    have = set(target["end"]) if len(target) else set()
    m = other.merge(cx[["end", "val", "filed"]], on="end", suffixes=("", "_cx"))
    m = m[~m["end"].isin(have)]
    if not len(m):
        return target
    add = pd.DataFrame(dict(end=m["end"], start=m["start"], val=m["val"] + sign * m["val_cx"],
                            filed=m[["filed", "filed_cx"]].max(axis=1), how="identity", tag=label, pri=99))
    return pd.concat([target, add], ignore_index=True).sort_values("end")


def shares_frame(cf: dict) -> pd.DataFrame:
    g = cf.get("facts", {}).get("dei", {})
    rows = []
    for f in g.get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", []):
        rows.append(dict(end=f["end"], val=f["val"], filed=f["filed"], accn=f["accn"]))
    df = pd.DataFrame(rows)
    if len(df):
        df["end"] = pd.to_datetime(df["end"]); df["filed"] = pd.to_datetime(df["filed"])
        # multiple classes on the same cover: sum by accession
        df = df.groupby(["accn", "filed", "end"], as_index=False)["val"].sum()
    return df


def submissions(cik: int, refresh=False) -> pd.DataFrame:
    j = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json",
            CACHE / "submissions" / f"CIK{cik:010d}.json.gz", refresh)
    frames = [j["filings"]["recent"]]
    for fl in j["filings"].get("files", []):
        s = get(f"https://data.sec.gov/submissions/{fl['name']}", CACHE / "submissions" / (fl["name"] + ".gz"), refresh)
        frames.append(s)
    rows = []
    for f in frames:
        n = len(f["form"])
        for i in range(n):
            rows.append(dict(form=f["form"][i], filed=f["filingDate"][i], accn=f["accessionNumber"][i],
                             items=(f.get("items") or [""] * n)[i] or "",
                             report_date=(f.get("reportDate") or [""] * n)[i] or "",
                             acceptance=(f.get("acceptanceDateTime") or [""] * n)[i] or ""))
    return pd.DataFrame(rows)


# Filings whose XBRL is missing from companyfacts (checked 2026-09-23): read the instance directly.
# MCRI's Q2 2026 10-Q (filed 2026-07-28) is absent from the companyfacts API.
INSTANCE_SUPPLEMENT = {"MCRI": [("0001104659-26-087556", "mcri-20260630x10q_htm.xml")]}


def instance_facts(cik: int, accn: str, fname: str) -> pd.DataFrame:
    """Non-dimensional us-gaap facts from one filing's XBRL instance, in facts_frame() form."""
    import re
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn.replace('-', '')}/{fname}"
    cache = CACHE / "instances" / fname
    if not cache.exists():
        dt = time.time() - _last[0]
        if dt < 0.14:
            time.sleep(0.14 - dt)
        r = requests.get(url, headers=UA, timeout=60); _last[0] = time.time()
        r.raise_for_status()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(r.content)
    x = cache.read_text(errors="ignore")
    ctx = {}
    for m in re.finditer(r'<(?:xbrli:)?context id="([^"]+)">(.*?)</(?:xbrli:)?context>', x, re.S):
        body = m.group(2)
        if "xbrldi:explicitMember" in body or "typedMember" in body:
            continue
        st = re.search(r"<(?:xbrli:)?startDate>([^<]+)", body); en = re.search(r"<(?:xbrli:)?endDate>([^<]+)", body)
        if st and en:
            ctx[m.group(1)] = (st.group(1), en.group(1))
    filed = None
    rows = []
    for m in re.finditer(r'<us-gaap:(\w+)\b[^>]*contextRef="([^"]+)"[^>]*>([^<]*)</us-gaap:\1>', x):
        tag, c, v = m.groups()
        if c in ctx:
            try:
                rows.append(dict(tag=tag, start=ctx[c][0], end=ctx[c][1], val=float(v), accn=accn))
            except ValueError:
                pass
    return pd.DataFrame(rows)


def main(refresh=False):
    fin_rows, fil_rows = [], []
    for comp, ciks in COMPANIES.items():
        for cik in ciks:
            print(comp, cik, flush=True)
            cf = get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json",
                     CACHE / "companyfacts" / f"CIK{cik:010d}.json.gz", refresh)
            if cf is None:
                print("  no companyfacts"); continue
            if comp in INSTANCE_SUPPLEMENT:
                fil_c = submissions(cik, refresh)
                sup = {}
                for accn, fname in INSTANCE_SUPPLEMENT[comp]:
                    fd = fil_c.loc[fil_c["accn"] == accn, "filed"]
                    form = fil_c.loc[fil_c["accn"] == accn, "form"]
                    inst = instance_facts(cik, accn, fname)
                    for _, r in inst.iterrows():
                        sup.setdefault(r["tag"], []).append(dict(start=r["start"], end=r["end"], val=r["val"],
                                                                filed=fd.iloc[0], form=form.iloc[0], accn=accn))
                cf["_supplement"] = sup
            parts = {}
            for name, tags in [("op_income", OI_TAGS), ("da", DA_TAGS), ("gaming_rev", GAMING_TAGS)]:
                parts[name] = quarterly(facts_frame(cf, tags))
            cx0 = quarterly(facts_frame(cf, ["CostsAndExpenses", "OperatingExpenses"]))
            anchor = None
            if len(cx0) and len(parts["op_income"]):
                anchor = parts["op_income"][["end", "val"]].merge(cx0[["end", "val"]], on="end")
                anchor = pd.DataFrame(dict(end=anchor["end"], val=anchor["val_x"] + anchor["val_y"]))
            rv = facts_frame(cf, REV_TAGS)
            parts["revenue"] = choose(quarterly_all(rv), "revenue", anchor) if len(rv) else quarterly(rv)
            # D&A fallback: Depreciation (+ AmortizationOfIntangibleAssets)
            dep = quarterly(facts_frame(cf, ["Depreciation"]))
            amo = quarterly(facts_frame(cf, ["AmortizationOfIntangibleAssets"]))
            if len(dep):
                dep = dep.merge(amo[["end", "val"]].rename(columns={"val": "amo"}), on="end", how="left")
                dep["val"] = dep["val"] + dep["amo"].fillna(0)
                dep["tag"] = "Depreciation(+AmortizationOfIntangibleAssets)"
                have = set(parts["da"]["end"]) if len(parts["da"]) else set()
                extra = dep[~dep["end"].isin(have)]
                parts["da"] = pd.concat([parts["da"], extra[parts["da"].columns.intersection(extra.columns)]], ignore_index=True)
            cx = quarterly(facts_frame(cf, ["CostsAndExpenses", "OperatingExpenses"]))
            parts["revenue"] = fill_identity(parts["revenue"], parts["op_income"], cx, sign=+1, label="OI+CostsAndExpenses")
            parts["op_income"] = fill_identity(parts["op_income"], parts["revenue"], cx, sign=-1, label="Revenue-CostsAndExpenses")
            ends = sorted(set().union(*[set(p["end"]) for p in parts.values() if len(p)]))
            sh = shares_frame(cf)
            for e in ends:
                row = dict(company=comp, cik=cik, qend=e.date())
                for name, p in parts.items():
                    m = p[p["end"] == e]
                    if len(m):
                        row[name] = float(m["val"].iloc[0]); row[name + "_how"] = m["how"].iloc[0]
                        row[name + "_tag"] = m["tag"].iloc[0]; row[name + "_filed"] = m["filed"].iloc[0].date()
                        if "tag_spread" in m:
                            row[name + "_tagspread"] = m["tag_spread"].iloc[0]
                fin_rows.append(row)
            subs = submissions(cik, refresh)
            subs["company"] = comp; subs["cik"] = cik
            keep = subs[(subs.form.str.startswith("8-K") & subs["items"].str.contains("2.02", regex=False)) |
                        subs.form.isin(["10-Q", "10-K", "10-Q/A", "10-K/A", "10-KT"])]
            fil_rows.append(keep)
            if len(sh):
                sh2 = sh.copy(); sh2["company"] = comp; sh2["cik"] = cik
                sh2.to_csv(CACHE / f"shares_{comp}_{cik}.csv", index=False)
    fin = pd.DataFrame(fin_rows)
    fin["ebitda"] = fin["op_income"] + fin["da"]
    fin["ebitda_is_oi_only"] = fin["da"].isna() & fin["op_income"].notna()
    fin.loc[fin["ebitda_is_oi_only"], "ebitda"] = fin.loc[fin["ebitda_is_oi_only"], "op_income"]
    fin = fin.sort_values(["company", "qend"])
    DATA.mkdir(exist_ok=True)
    fin.to_csv(DATA / "financials_q.csv.gz", index=False)
    fil = pd.concat(fil_rows, ignore_index=True)
    fil.to_csv(DATA / "filings.csv.gz", index=False)
    # shares: combine
    shs = [pd.read_csv(p) for p in CACHE.glob("shares_*.csv")]
    if shs:
        pd.concat(shs, ignore_index=True).to_csv(DATA / "shares_out.csv.gz", index=False)
    print("financial rows", len(fin), "filings", len(fil))


if __name__ == "__main__":
    main(refresh="--refresh" in sys.argv)
