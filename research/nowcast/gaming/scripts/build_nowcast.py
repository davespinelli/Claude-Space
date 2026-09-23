#!/usr/bin/env python3
"""Build the company-quarter nowcast panel (PREREG.md build steps 3, 5, 6, 7).  NO RETURNS HERE:
announcement returns are computed only in run_tests.py, after the Deviations section of PREREG.md
was written.

Inputs
  data/state_<st>.csv.gz        monthly casino revenue by property / region (scripts/state_*.py)
  data/ownership.csv.gz         which company owned which property when (scripts/ownership.py)
  data/property_map.csv.gz      state unit_id -> ownership property (scripts/property_map.py)
  data/financials_q.csv.gz      first-reported quarterly financials (scripts/sec_fetch.py)
  data/filings.csv.gz           8-K Item 2.02 and 10-Q/10-K filing dates (scripts/sec_fetch.py)

Output data/nowcast_panel.csv.gz, one row per company x fiscal quarter with:
  months, ann_date (+ source), coverage, g (same-store covered GGR growth), months used,
  flow-through beta (own, industry median, shrunk), nowcast revenue / EBITDA growth, reported
  growth for q and q-1, the two acceleration signals, last publication date used, and flags.

Two samples are built side by side (see PREREG Deviations):
  'prop'   : property/operator-level state data only (the pre-registered design; carries the verdict)
  'region' : 'prop' plus region-level proxies for Mississippi (county/region), Colorado (town) and
             Nevada (reporting area), where a property's monthly GGR is imputed as unit GGR divided
             by the number of casinos reporting in that unit (secondary sample).
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

PRICED = {  # company -> (Yahoo ticker, first date with a usable price history)
    "PENN": ("PENN", "2011-01-01"), "BYD": ("BYD", "2011-01-01"), "ERI_CZR": ("CZR", "2014-09-22"),
    "BALY": ("BALY", "2024-12-06"), "RRR": ("RRR", "2016-04-27"), "MCRI": ("MCRI", "2011-01-01"),
    "CNTY": ("CNTY", "2011-01-01"), "FLL": ("FLL", "2011-01-01"), "CHDN": ("CHDN", "2011-01-01"),
    "MGM": ("MGM", "2011-01-01"), "WYNN": ("WYNN", "2011-01-01"),
}
NOWCAST_COMPANIES = ["PENN", "PNK_OLD", "PNK", "BYD", "ERI_CZR", "CZR_OLD", "ISLE", "TPCA", "BALY",
                     "DDE", "NYNY", "GDEN", "RRR", "MCRI", "CNTY", "FLL", "CHDN", "MGM", "WYNN",
                     "MNTG", "AFFI"]
REGION_STATES = {"MS", "CO", "NV"}
MIN_Q_OWN = 8          # PREREG step 5
SHRINK = 0.5           # PREREG step 5
COVERAGE_MIN = 0.60    # PREREG build step 3
PUB_DEFAULT_DAYS = 30  # PREREG build step 1: month-end + 30 days when the publication date is unknown
MIN_AVAIL_SHARE = 2 / 3  # point-in-time rule (PREREG Deviation): share of year-ago covered GGR whose
                         # current-month report was public before the announcement


# ----------------------------------------------------------------------------- inputs
def load_states() -> pd.DataFrame:
    frames = []
    for p in sorted(DATA.glob("state_??.csv.gz")):
        d = pd.read_csv(p, dtype={"unit_id": str, "unit": str})
        frames.append(d)
    s = pd.concat(frames, ignore_index=True)
    s = s[s["unit_level"] != "state_total"].copy()
    s["month"] = pd.PeriodIndex(s["month"], freq="M")
    # region units: casino counts missing in a few image-only reports (NV 2020-04/05, 2025-06/07)
    # are carried from the nearest month of the same unit
    s = s.sort_values(["unit_id", "month"])
    s["n_casinos"] = s.groupby("unit_id")["n_casinos"].transform(lambda v: v.ffill().bfill())
    s["pub_date"] = pd.to_datetime(s["pub_date"], errors="coerce")
    s["pub_assumed"] = s["pub_date"].isna()
    s.loc[s["pub_assumed"], "pub_date"] = (s.loc[s["pub_assumed"], "month"].dt.to_timestamp(how="end").dt.normalize()
                                          + pd.Timedelta(days=PUB_DEFAULT_DAYS))
    return s


def quarter_months(qend: pd.Timestamp) -> list:
    """The three calendar months a fiscal quarter covers (52/53-week quarters: the month holding
    most of the quarter's last weeks is the last month)."""
    last = pd.Period(qend, freq="M") if qend.day >= 15 else pd.Period(qend, freq="M") - 1
    return [last - 2, last - 1, last]


def load_fin() -> pd.DataFrame:
    f = pd.read_csv(DATA / "financials_q.csv.gz", parse_dates=["qend", "revenue_filed", "op_income_filed", "da_filed"])
    f = f[f["company"].isin(NOWCAST_COMPANIES)].copy()
    f = f.sort_values(["company", "qend"]).drop_duplicates(["company", "qend"], keep="first")
    f["avail"] = f[["revenue_filed", "op_income_filed", "da_filed"]].max(axis=1)
    # gaming revenue: us-gaap:CasinoRevenue (non-dimensional, companyfacts) where tagged, else the
    # casino/gaming line of the revenue disaggregation read from the filing instances
    # (scripts/gaming_revenue.py), else missing (coverage then uses total revenue)
    gd = DATA / "gaming_rev_dim.csv.gz"
    if gd.exists():
        g = pd.read_csv(gd, parse_dates=["qend"])[["company", "qend", "gaming_rev"]].rename(columns={"gaming_rev": "gaming_rev_dim"})
        g2 = g[g["company"] == "PNK"].copy(); g2["company"] = "PNK_OLD"
        g = pd.concat([g, g2])
        f = f.merge(g, on=["company", "qend"], how="left")
        f["gaming_rev_src"] = np.where(f["gaming_rev"].notna(), "CasinoRevenue", np.where(f["gaming_rev_dim"].notna(), "disaggregation", ""))
        f["gaming_rev"] = f["gaming_rev"].fillna(f["gaming_rev_dim"])
    return f


def announcements(fin: pd.DataFrame) -> pd.DataFrame:
    fil = pd.read_csv(DATA / "filings.csv.gz", parse_dates=["filed"])
    k8 = fil[fil["form"].str.startswith("8-K")]
    per = fil[~fil["form"].str.startswith("8-K")].copy()
    per["report_date"] = pd.to_datetime(per["report_date"], errors="coerce")
    out = []
    for _, r in fin.iterrows():
        c, q = r["company"], r["qend"]
        cand = k8[(k8["company"] == c) & (k8["filed"] > q) & (k8["filed"] <= q + pd.Timedelta(days=100))]
        pq = per[(per["company"] == c) & (per["report_date"].sub(q).abs() <= pd.Timedelta(days=3))
                 & per["form"].isin(["10-Q", "10-K", "10-KT"])]
        pdate = pq["filed"].min() if len(pq) else pd.NaT
        if len(cand):
            a, src = cand["filed"].min(), "8-K 2.02"
            if pd.notna(pdate) and pdate < a:
                a, src = pdate, "10-Q/10-K (before 8-K)"
        elif pd.notna(pdate):
            a, src = pdate, "10-Q/10-K (no 8-K 2.02)"
        else:
            a, src = pd.NaT, ""
        out.append(dict(company=c, qend=q, ann_date=a, ann_source=src))
    return pd.DataFrame(out)


# ----------------------------------------------------------------------------- flow-through
def yoy_pairs(fin: pd.DataFrame) -> pd.DataFrame:
    """Per company-quarter: YoY $ change in revenue and EBITDA (first reported), with the date
    both quarters' figures were public."""
    rows = []
    for c, d in fin.groupby("company"):
        d = d.set_index("qend").sort_index()
        for q in d.index:
            q4 = [x for x in d.index if abs((x - (q - pd.DateOffset(years=1))).days) <= 10]
            if not q4:
                continue
            a, b = d.loc[q], d.loc[q4[0]]
            rows.append(dict(company=c, qend=q, qend_4=q4[0], dR=a["revenue"] - b["revenue"],
                             dE=a["ebitda"] - b["ebitda"], avail=max(a["avail"], b["avail"])))
    return pd.DataFrame(rows).dropna(subset=["dR", "dE"])


def slope(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, float); y = np.asarray(y, float)
    vx = np.var(x)
    return float(np.cov(x, y, bias=True)[0, 1] / vx) if vx > 0 else np.nan


def flow_through(pairs: pd.DataFrame, asof: pd.Timestamp, company: str) -> dict:
    """Own slope (>= 8 quarters reported before `asof`), industry median of own slopes, shrunk beta."""
    avail = pairs[pairs["avail"] < asof]
    own = {}
    for c, d in avail.groupby("company"):
        if len(d) >= MIN_Q_OWN:
            own[c] = slope(d["dR"].values, d["dE"].values)
    ind = float(np.nanmedian(list(own.values()))) if own else np.nan
    b_own = own.get(company, np.nan)
    n_own = int((avail["company"] == company).sum())
    beta = ind if np.isnan(b_own) else SHRINK * b_own + (1 - SHRINK) * ind
    return dict(beta_own=b_own, n_own=n_own, beta_ind=ind, n_ind=len(own), beta=beta,
                beta_src="own+industry" if not np.isnan(b_own) else "industry")


# ----------------------------------------------------------------------------- property GGR by company
def covered_ownership(own: pd.DataFrame) -> pd.DataFrame:
    """Ownership spells that put a property's revenue in the company's reported revenue:
    owned or leased-and-operated, consolidated, not in discontinued operations.  Equity-method JVs
    and management contracts are excluded (their GGR is not in the company's revenue).  Pinnacle's
    rows apply to both of its registrants (PNK_OLD before the April 2016 GLPI deal, PNK after)."""
    o = own.copy()
    o = o[o["relation"].isin(["owned", "leased_operated"]) & (o["consolidated"].astype(str) == "1")
          & (o["discontinued"].astype(str) != "1")].copy()
    pnk = o[o["company"] == "PNK"].copy(); pnk["company"] = "PNK_OLD"
    o = pd.concat([o, pnk], ignore_index=True)
    o["start"] = pd.to_datetime(o["start"].fillna("").replace("", "1900-01-01"))
    o["end"] = pd.to_datetime(o["end"].fillna("").replace("", "2100-01-01"))
    # merge back-to-back spells of the same company and property (e.g. a row split at a stake change)
    rows = []
    for (c, st, pr), g in o.sort_values("start").groupby(["company", "state", "property"]):
        cur = None
        for _, r in g.iterrows():
            if cur is not None and r["start"] <= cur["end"] + pd.Timedelta(days=1):
                cur["end"] = max(cur["end"], r["end"])
            else:
                if cur is not None:
                    rows.append(cur)
                cur = dict(company=c, state=st, property=pr, start=r["start"], end=r["end"])
        rows.append(cur)
    return pd.DataFrame(rows)


def ms_devices() -> pd.DataFrame:
    """Mississippi Gaming Commission device counts per casino-month -> each covered property's share
    of its region's slot machines and tables (used only to impute region-sample GGR)."""
    import re
    p = DATA / "state_ms_devices.csv.gz"
    if not p.exists():
        return pd.DataFrame()
    dv = pd.read_csv(p)
    own = pd.read_csv(DATA / "ownership.csv.gz", dtype=str).fillna("")
    own = own[own["state"] == "MS"]
    stop = {"casino", "hotel", "resort", "spa", "and", "the", "of", "&", "-", "biloxi", "tunica", "casinos"}

    def toks(x):
        return {t for t in re.findall(r"[a-z0-9]+", str(x).lower().replace("'", "")) if t not in stop}
    cand = []
    for _, r in own.iterrows():
        for n in [r["property"]] + [a for a in r["aliases"].split("|") if a]:
            cand.append((r["property"], toks(n), n.lower()))
    mp = {}
    for c in dv["casino"].unique():
        tc = toks(c); best = (0, None)
        for prop, tp, raw in cand:
            if not tc or not tp:
                continue
            sc = len(tc & tp) / min(len(tc), len(tp))
            loc_ok = not (("biloxi" in c.lower()) ^ ("biloxi" in raw)) if ("biloxi" in c.lower() or "biloxi" in raw) else True
            if sc > best[0] and loc_ok:
                best = (sc, prop)
        if best[0] >= 0.99:
            mp[c] = best[1]
    dv["property"] = dv["casino"].map(mp)
    dv["month"] = pd.PeriodIndex(dv["month"], freq="M")
    tot = dv.groupby(["region", "month"])[["slot_units", "table_units"]].transform("sum")
    dv["slot_share"] = dv["slot_units"] / tot["slot_units"]
    dv["table_share"] = dv["table_units"].fillna(0) / tot["table_units"].replace(0, np.nan)
    out = dv.dropna(subset=["property"]).groupby(["property", "month"], as_index=False)[["slot_share", "table_share"]].sum()
    return out


def company_property_months(states: pd.DataFrame, cov: pd.DataFrame, pmap: pd.DataFrame,
                            ms_dev: pd.DataFrame | None = None) -> pd.DataFrame:
    """Rows: company, state, property, unit_id, month, ggr (attributable), measure, pub_date, level.
    Property-level units are attributed in full to the consolidated owner.  Region-level units
    (MS, CO, NV; region sample only) get an imputed property GGR: the unit's GGR divided by the
    number of casinos reporting in it (Mississippi: the unit's slot win times the property's share
    of the region's slot machines plus table win times its share of tables, from the Commission's
    device counts, when the property is matched to them)."""
    x = states.merge(pmap[["state", "unit_id", "property"]], on=["state", "unit_id"], how="inner")
    x = x.merge(cov[["company", "state", "property", "start", "end"]], on=["state", "property"], how="inner")
    ms = x["month"].dt.to_timestamp(how="start"); me = x["month"].dt.to_timestamp(how="end").dt.normalize()
    x = x[(x["start"] <= ms) & (x["end"] >= me)].copy()   # owned for the whole month
    x["level"] = np.where(x["state"].isin(REGION_STATES) | ~x["unit_level"].isin(["property", "operator"]),
                          "region", "prop")
    reg = x["level"] == "region"
    x["impute"] = ""
    x.loc[reg, "impute"] = "equal_share"
    x.loc[reg, "ggr_share"] = x.loc[reg, "ggr"] / x.loc[reg, "n_casinos"]
    # Nevada / Colorado: the property's share of its unit's slot machines and table games, with the
    # property's counts from its owner's 10-K property table (nearest fiscal year) and the unit's
    # counts from the regulator (data/property_devices.csv.gz, n_slot_units / n_table_units).
    pdv_path = DATA / "property_devices.csv.gz"
    if pdv_path.exists() and "n_slot_units" in x.columns:
        pdv_all = pd.read_csv(pdv_path)
        # casinos whose count is printed on a sibling's row (e.g. Cactus Petes + Horseshu, Bronco
        # Billy's + Chamonix, the three Black Hawk casinos): weight 0, the sibling carries the total
        combined = set(zip(pdv_all.loc[pdv_all["note"].fillna("").str.contains("included in the combined figure"), "state"],
                           pdv_all.loc[pdv_all["note"].fillna("").str.contains("included in the combined figure"), "property"]))
        pdv = pdv_all.dropna(subset=["slots"])
        pdv = pdv[pdv["slots"] > 0]
        nvco = x.index[reg & x["state"].isin(["NV", "CO"]) & x["n_slot_units"].notna()]
        look = {}
        for (st, pr), g in pdv.groupby(["state", "property"]):
            look[(st, pr)] = g.sort_values("fiscal_year")[["fiscal_year", "slots", "tables"]].values
        vals, how = [], []
        for i in nvco:
            r = x.loc[i]
            arr = look.get((r["state"], r["property"]))
            if arr is None:
                if (r["state"], r["property"]) in combined:
                    vals.append(0.0); how.append("in_sibling_count")
                else:
                    vals.append(np.nan); how.append("")
                continue
            yr = r["month"].year
            j = int(np.argmin(np.abs(arr[:, 0] - yr)))
            ps, pt = arr[j, 1], arr[j, 2]
            us, ut = r["n_slot_units"], r.get("n_table_units", np.nan)
            sl = r["slots"] if pd.notna(r["slots"]) else r["ggr"]
            tb = r["tables"] if pd.notna(r["tables"]) else 0.0
            v = sl * min(ps / us, 1.0) if us and us > 0 else np.nan
            if pd.notna(v) and pd.notna(pt) and pd.notna(ut) and ut > 0:
                v += tb * min(pt / ut, 1.0)
            elif pd.notna(v) and tb:
                v += tb * min(ps / us, 1.0)
            vals.append(v); how.append("device_share" if pd.notna(v) else "")
        vals = pd.Series(vals, index=nvco); how = pd.Series(how, index=nvco)
        ok = vals.notna()
        x.loc[vals.index[ok], "ggr_share"] = vals[ok]
        x.loc[how.index[ok], "impute"] = "device_share"
    if ms_dev is not None and len(ms_dev):
        md = x[reg & (x["state"] == "MS")].merge(ms_dev, on=["property", "month"], how="left")
        ok = md["slot_share"].notna()
        slots = md["slots"].where(md["slots"].notna(), md["ggr"])
        tables = md["tables"].fillna(0)
        dev = slots * md["slot_share"] + tables * md["table_share"].fillna(md["slot_share"])
        idx = x.index[reg & (x["state"] == "MS")]
        x.loc[idx[ok.values], "ggr_share"] = dev[ok].values
        x.loc[idx[ok.values], "impute"] = "device_share"
    x.loc[reg, "ggr"] = x.loc[reg, "ggr_share"]
    x = x[x["ggr"].notna()]
    x["measure"] = x["measure"].fillna("")
    return x[["company", "state", "property", "unit_id", "month", "ggr", "measure", "pub_date",
              "pub_assumed", "level", "impute", "start", "end"]]


def nowcast_g(cpm: pd.DataFrame, company: str, months: list, asof: pd.Timestamp | None, sample: str):
    """Same-store growth of summed covered GGR over the quarter's months (PREREG build step 6).
    Same-store set: properties the company held (covered spell) from the first day of the
    year-ago quarter to the last day of the current quarter.  g pairs each property-month with
    the same property's month a year earlier; with `asof`, only current months whose state report
    was published before `asof` are used (point-in-time; PREREG Deviation 2)."""
    d = cpm[(cpm["company"] == company)]
    if sample == "prop":
        d = d[d["level"] == "prop"]
    prev = [m - 12 for m in months]
    q_start = prev[0].to_timestamp(how="start"); q_end = months[-1].to_timestamp(how="end").normalize()
    sp = d.drop_duplicates(["property", "start", "end"])
    props = set(sp.loc[(sp["start"] <= q_start) & (sp["end"] >= q_end), "property"])
    if not props:
        return None
    d = d[d["property"].isin(props)]
    cur = d[d["month"].isin(months)]
    old = d[d["month"].isin(prev)]
    if not len(old) or old["ggr"].sum() <= 0:
        return None
    # comparability: Iowa's AGR excludes promotional play from 2026-07 (about -13% mechanically),
    # so Iowa months from 2026-07 are not compared with 2025.  Other label changes in the state
    # files (Mississippi source notes, Nevada months rebuilt from 3-month columns) are the same measure.
    meas_old = dict(zip(zip(old["property"], old["month"] + 12), old["measure"]))
    keep = [(st != "IA") or (meas_old.get((p, m)) == ms)
            for st, p, m, ms in zip(cur["state"], cur["property"], cur["month"], cur["measure"])]
    cur = cur[keep]
    old_total = old["ggr"].sum()
    old_key = dict(zip(zip(old["property"], old["month"] + 12), old["ggr"]))
    cur = cur[[(p, m) in old_key for p, m in zip(cur["property"], cur["month"])]]
    cur_all = cur
    cur_av = cur[cur["pub_date"] < asof] if asof is not None else cur

    def pair_g(c):
        o = sum(old_key[(p, m)] for p, m in zip(c["property"], c["month"]))
        return (c["ggr"].sum() / o - 1 if o > 0 else np.nan), o
    g_all, o_all = pair_g(cur_all)
    g, o_av = pair_g(cur_av)
    used_months = sorted(cur_av["month"].unique())
    return dict(props=len(props), states=",".join(sorted(d["state"].unique())), covered_ggr_4=old_total,
                g_all=g_all, all3_share=o_all / old_total,
                avail_share=o_av / old_total, g=g,
                n_months_used=len(used_months), months_used=",".join(str(m) for m in used_months),
                last_pub=cur_av["pub_date"].max() if len(cur_av) else pd.NaT,
                last_pub_all=cur_all["pub_date"].max() if len(cur_all) else pd.NaT,
                any_pub_assumed=bool(cur_av["pub_assumed"].any()) if len(cur_av) else True,
                region_share=(old.loc[old["level"] == "region", "ggr"].sum() / old_total))


# ----------------------------------------------------------------------------- main
def growth(new, old):
    return (new - old) / abs(old) if (pd.notna(old) and old != 0 and pd.notna(new)) else np.nan


LIVE_ASOF = pd.Timestamp("2026-09-24")   # state reports published up to 2026-09-23 count for the live nowcast


def build() -> pd.DataFrame:
    states = load_states()
    own = pd.read_csv(DATA / "ownership.csv.gz", dtype=str).fillna("")
    cov = covered_ownership(own)
    pmap = pd.read_csv(DATA / "property_map.csv.gz")
    cpm = company_property_months(states, cov, pmap, ms_devices())
    cpm.to_csv(DATA / "company_property_months.csv.gz", index=False)
    fin = load_fin()
    ann = announcements(fin)
    fin = fin.merge(ann, on=["company", "qend"], how="left")
    pairs = yoy_pairs(fin)
    o2 = cov

    def portfolio(c, d):
        x = o2[(o2["company"] == c) & (o2["start"] <= d) & (o2["end"] >= d)]
        return set(zip(x["state"], x["property"]))

    def make_rows(c, d, q, r, live):
        q4 = [x for x in d.index if abs((x - (q - pd.DateOffset(years=1))).days) <= 10]
        q1 = [x for x in d.index if 75 <= (q - x).days <= 105]
        q5 = [x for x in d.index if q1 and abs((x - (q1[0] - pd.DateOffset(years=1))).days) <= 10]
        if not q4:
            return []
        b = d.loc[q4[0]]
        months = quarter_months(q)
        base = dict(company=c, qend=q.date(), months=",".join(str(m) for m in months), live=live,
                    ann_date=r["ann_date"], ann_source=r["ann_source"],
                    rev=r["revenue"], rev_4=b["revenue"], ebitda=r["ebitda"], ebitda_4=b["ebitda"],
                    gaming_rev_4=b.get("gaming_rev", np.nan),
                    ebitda_oi_only=bool(r["ebitda_is_oi_only"] == True) or bool(b["ebitda_is_oi_only"] == True),
                    rev_growth=growth(r["revenue"], b["revenue"]), ebitda_growth=growth(r["ebitda"], b["ebitda"]),
                    portfolio_change=portfolio(c, q) != portfolio(c, q4[0]))
        if q1 and q5:
            a1, a5 = d.loc[q1[0]], d.loc[q5[0]]
            base.update(rev_growth_prev=growth(a1["revenue"], a5["revenue"]),
                        ebitda_growth_prev=growth(a1["ebitda"], a5["ebitda"]))
        else:
            base.update(rev_growth_prev=np.nan, ebitda_growth_prev=np.nan)
        asof = LIVE_ASOF if live else (r["ann_date"] if pd.notna(r["ann_date"]) else None)
        base.update(flow_through(pairs, asof if asof is not None else q + pd.Timedelta(days=45), c))
        gr = base["gaming_rev_4"]
        use_g = pd.notna(gr) and gr > 0
        denom = gr if use_g else base["rev_4"]
        base["coverage_denom"] = "gaming_rev" if use_g else "revenue"
        out = []
        for sample in ["prop", "region"]:
            res = nowcast_g(cpm, c, months, asof, sample)
            row = dict(base, sample=sample)
            if res is None:
                row.update(props=0, coverage=0.0, qualifies=False)
                out.append(row); continue
            row.update(res)
            row["coverage"] = res["covered_ggr_4"] / denom if denom and denom > 0 else np.nan
            g = res["g"]
            row["nc_rev_growth"] = g
            row["nc_rev"] = b["revenue"] * (1 + g) if pd.notna(g) else np.nan
            row["nc_ebitda"] = b["ebitda"] + row["beta"] * b["revenue"] * g if pd.notna(g) else np.nan
            row["nc_ebitda_growth"] = growth(row["nc_ebitda"], b["ebitda"])
            g_all = res["g_all"]   # spec-literal: all three months regardless of publication date
            row["nc_ebitda_growth_all3"] = growth(b["ebitda"] + row["beta"] * b["revenue"] * g_all, b["ebitda"]) if pd.notna(g_all) else np.nan
            row["sig_ebitda"] = row["nc_ebitda_growth"] - base["ebitda_growth_prev"]
            row["sig_rev"] = g - base["rev_growth_prev"] if pd.notna(g) else np.nan
            row["sig_ebitda_all3"] = row["nc_ebitda_growth_all3"] - base["ebitda_growth_prev"]
            ok_cov = bool(pd.notna(row["coverage"]) and row["coverage"] >= COVERAGE_MIN)
            if live:
                row["qualifies"] = bool(ok_cov and pd.notna(row["sig_ebitda"]))
            else:
                row["qualifies"] = bool(ok_cov and res["avail_share"] >= MIN_AVAIL_SHARE
                                        and pd.notna(row["sig_ebitda"]) and pd.notna(r["ann_date"]))
            out.append(row)
        return out

    rows = []
    for c, d in fin.groupby("company"):
        d = d.set_index("qend").sort_index()
        for q in d.index:
            if q >= pd.Timestamp("2013-01-01"):
                rows += make_rows(c, d, q, d.loc[q], live=False)
        # live quarter: the quarter after the last reported one, if it has started state data
        last = d.index.max()
        if last >= pd.Timestamp("2026-03-31"):
            q = (last + pd.offsets.QuarterEnd(1)).normalize()
            r = pd.Series(dict(revenue=np.nan, ebitda=np.nan, ann_date=pd.NaT, ann_source="", ebitda_is_oi_only=False))
            rows += make_rows(c, d, q, r, live=True)
    out = pd.DataFrame(rows)
    out["ticker"] = out["company"].map(lambda c: PRICED.get(c, (None, None))[0])
    out["price_from"] = out["company"].map(lambda c: PRICED.get(c, (None, None))[1])
    out["priced"] = out["ticker"].notna() & (pd.to_datetime(out["ann_date"]) > pd.to_datetime(out["price_from"]) + pd.Timedelta(days=5))
    out[~out["live"]].drop(columns=["live"]).to_csv(DATA / "nowcast_panel.csv.gz", index=False)
    out[out["live"]].drop(columns=["live"]).to_csv(DATA / "nowcast_live_raw.csv.gz", index=False)
    return out


if __name__ == "__main__":
    o = build()
    q = o[o["qualifies"] & ~o["live"]]
    print(q.groupby(["sample", "company"]).size().unstack(0).fillna(0).astype(int).to_string())
    print(o[o["live"]][["company", "sample", "qend", "coverage", "months_used", "g", "nc_ebitda_growth", "sig_ebitda", "qualifies"]].to_string())
