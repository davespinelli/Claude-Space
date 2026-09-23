#!/usr/bin/env python3
"""
H5/H6 data step 2: point-in-time quarterly fundamentals from SEC companyfacts.

Reads quarterly/cache/cf/*.parquet (written by fetch_facts.py) and writes

    quarterly/cache/filings.parquet   one row per original 10-Q / 10-K (the trigger events)
    quarterly/cache/snapshot.parquet  one row per company per June (FCS breakpoint universe)
    quarterly/cache/build_log.json    coverage counts

No returns are computed here.

Rules (see H5_H6_PREREG.md and its Deviations section):
  * Every value is the one from the FIRST filing (10-K/10-Q family, amendments
    included only if they were first) that reported that exact period; its
    filed date is when it becomes usable. Later restatements are never used.
  * Revenue: first total tag present in that first filing, in build_panel.py's
    order (Revenues, RevenueFromContractWithCustomerExcludingAssessedTax,
    SalesRevenueNet, RevenueFromContractWithCustomerIncludingAssessedTax); if none,
    SalesRevenueGoodsNet + SalesRevenueServicesNet. Operating income:
    OperatingIncomeLoss.
  * Quarter = a 75-125 day period. Q4 is usually only reported inside the annual
    figure. Q4 is taken as whichever becomes available first: a directly reported
    3-month value, or FY (first reported, in the 10-K) minus the first-reported
    9-month year-to-date value from the Q3 10-Q, or, when no 9-month value
    exists, FY minus the three first-reported quarters. Available on the later of
    the filing dates used. A derived Q4 revenue <= 0 is discarded.
  * Fixed-cost share (H2a definition): cost = revenue - operating income, OLS
    cost = a + b * revenue over the latest five fiscal years (>= 4 needed),
    FCS = a / mean(cost) clipped to [-1, 1], using annual values first reported
    strictly before the date in question.
"""
from __future__ import annotations

import json
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

from qcommon import (CACHE, CF, OPLEV, OPINC_TAG, PERIODIC, REV_PART_TAGS, REV_TAGS, RPO_TAG,
                     SHARES_STALE_DAYS, TRIGGER, formation_month, last_trading_day)

DAY = np.timedelta64(1, "D")


# --------------------------------------------------------------------------- #
# first-reported tables
# --------------------------------------------------------------------------- #
def prep(f: pd.DataFrame) -> pd.DataFrame:
    f = f[f.form.isin(PERIODIC)].copy()
    for c in ("start", "end", "filed"):
        f[c] = pd.to_datetime(f[c], errors="coerce")
    f = f.dropna(subset=["end", "filed", "val"])
    return f


def first_dur(f: pd.DataFrame, tags: list[str], parts: list[str] | None = None) -> pd.DataFrame:
    """First-reported value per (start, end) duration."""
    d = f[f.tag.isin(tags) & (f.unit == "USD") & f.start.notna()]
    d = d.assign(prio=d.tag.map({t: i for i, t in enumerate(tags)}))[
        ["start", "end", "val", "accn", "filed", "tag", "prio"]]
    if parts:
        p = f[f.tag.isin(parts) & (f.unit == "USD") & f.start.notna()]
        if len(p):
            p = p.drop_duplicates(["tag", "start", "end", "accn"])
            ps = p.groupby(["start", "end", "accn"], as_index=False).agg(val=("val", "sum"),
                                                                        filed=("filed", "min"))
            ps["tag"] = "Goods+Services"
            ps["prio"] = len(tags)
            d = pd.concat([d, ps[d.columns]], ignore_index=True)
    if not len(d):
        return d.assign(dur=pd.Series(dtype="int64"))
    d = d.sort_values(["start", "end", "filed", "prio"]).drop_duplicates(["start", "end"], keep="first")
    d = d.assign(dur=(d.end - d.start).dt.days)
    return d.reset_index(drop=True)


def first_inst(f: pd.DataFrame, tax: str, tag: str, unit: str) -> pd.DataFrame:
    """First-reported value per instant (end date)."""
    d = f[(f.tax == tax) & (f.tag == tag) & (f.unit == unit)][["end", "val", "accn", "filed"]]
    d = d.sort_values(["end", "filed"]).drop_duplicates("end", keep="first")
    return d.reset_index(drop=True)


def quarter_table(fr: pd.DataFrame, positive: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Quarterly series (one row per quarter end) and the annual series."""
    cols = ["start", "end", "val", "filed", "accn", "src", "tag"]
    if not len(fr):
        e = pd.DataFrame(columns=cols)
        return e, pd.DataFrame(columns=["start", "end", "val", "filed", "accn", "tag"])
    q = fr[(fr.dur >= 75) & (fr.dur <= 125)].assign(src="direct")[cols]
    a = fr[(fr.dur >= 340) & (fr.dur <= 380)].sort_values("filed").drop_duplicates("end")
    y9 = fr[(fr.dur >= 230) & (fr.dur <= 300)]
    der = []
    for r in a.itertuples(index=False):
        c = y9[((y9.start - r.start).abs() <= 7 * DAY) & (r.end - y9.end >= 77 * DAY) & (r.end - y9.end <= 125 * DAY)]
        if len(c):
            c = c.sort_values("filed").iloc[0]
            der.append((c.end + DAY, r.end, r.val - c.val, max(r.filed, c.filed), r.accn,
                        "derived_fy_minus_9m", r.tag))
            continue
        chain, s, ok = [], r.start, True
        for k in range(3):
            c = q[((q.start - s).abs() <= 7 * DAY) & (q.end < r.end)]
            if not len(c):
                ok = False
                break
            c = c.sort_values("filed").iloc[0]
            chain.append(c)
            s = c.end + DAY
        if ok and 77 * DAY <= r.end - chain[-1].end <= 125 * DAY:
            der.append((chain[-1].end + DAY, r.end, r.val - sum(c.val for c in chain),
                        max([r.filed] + [c.filed for c in chain]), r.accn, "derived_fy_minus_q1q3", r.tag))
    d = pd.DataFrame(der, columns=cols)
    if positive and len(d):
        d = d[d.val > 0]
    allq = pd.concat([q, d], ignore_index=True) if len(d) else q.copy()
    if not len(allq):
        return pd.DataFrame(columns=cols), a
    allq = allq.sort_values("end").reset_index(drop=True)
    gap = allq.end.diff().dt.days.fillna(999)
    allq["cl"] = (gap > 3).cumsum()
    allq["so"] = (allq.src != "direct").astype(int)
    allq = allq.sort_values(["cl", "filed", "so"]).drop_duplicates("cl", keep="first")
    return allq[cols].sort_values("end").reset_index(drop=True), a


class Series:
    """Quarter (or instant) lookup by end-date window, respecting availability."""

    def __init__(self, t: pd.DataFrame):
        self.t = t.sort_values("end").reset_index(drop=True)
        self.end = self.t.end.to_numpy("datetime64[D]") if len(t) else np.array([], "datetime64[D]")
        self.filed = self.t.filed.to_numpy("datetime64[D]") if len(t) else np.array([], "datetime64[D]")
        self.val = self.t.val.to_numpy(float) if len(t) else np.array([])

    def find(self, lo, hi, avail=None):
        """Index of the latest end in [lo, hi] (dates), available by `avail` (filed <= avail)."""
        i0 = np.searchsorted(self.end, lo, "left")
        i1 = np.searchsorted(self.end, hi, "right")
        for i in range(i1 - 1, i0 - 1, -1):
            if avail is None or self.filed[i] <= avail:
                return i
        return None


class AsOf:
    """Latest-end row among rows filed strictly before a date."""

    def __init__(self, t: pd.DataFrame, basis_col: str):
        t = t.sort_values(["filed", "end"]).reset_index(drop=True)
        self.t = t
        self.filed = t.filed.to_numpy("datetime64[D]") if len(t) else np.array([], "datetime64[D]")
        best, bi, be = [], -1, None
        for i, e in enumerate(t.end.to_numpy("datetime64[D]") if len(t) else []):
            if be is None or e >= be:
                bi, be = i, e
            best.append(bi)
        self.best = np.array(best, int)
        self.basis_col = basis_col

    def at(self, T):
        i = np.searchsorted(self.filed, np.datetime64(T, "D"), "left") - 1
        if i < 0:
            return None
        r = self.t.iloc[self.best[i]]
        return r.val, r[self.basis_col], r.end


def fcs_calc(ann: pd.DataFrame) -> float:
    g = ann.drop_duplicates("end")
    if len(g) < 4:
        return np.nan
    x = g.rev.to_numpy(float)
    yv = g.cost.to_numpy(float)
    if np.var(x) <= 0:
        return np.nan
    b = np.cov(x, yv, bias=True)[0, 1] / np.var(x)
    a = yv.mean() - b * x.mean()
    mc = yv.mean()
    if not np.isfinite(mc) or mc == 0:
        return np.nan
    return float(np.clip(a / mc, -1.0, 1.0))


class FCS:
    def __init__(self, a_rev: pd.DataFrame, a_oi: pd.DataFrame):
        if not len(a_rev) or not len(a_oi):
            self.m = pd.DataFrame(columns=["end", "rev", "cost", "avail"])
        else:
            m = a_rev[["end", "val", "filed"]].rename(columns={"val": "rev", "filed": "f1"}).merge(
                a_oi[["end", "val", "filed"]].rename(columns={"val": "oi", "filed": "f2"}), on="end")
            m["cost"] = m.rev - m.oi
            m["avail"] = m[["f1", "f2"]].max(axis=1)
            self.m = m.dropna(subset=["rev", "cost"]).sort_values("end").reset_index(drop=True)
        self._cache = {}

    def at(self, d) -> float:
        m = self.m[self.m.avail < d]
        if len(m) < 4:
            return np.nan
        key = tuple(m.index)
        if key in self._cache:
            return self._cache[key]
        L = m.end.max()
        w = m[m.end > L - pd.Timedelta(days=1520)]
        v = fcs_calc(w)
        self._cache[key] = v
        return v


# --------------------------------------------------------------------------- #
# per company
# --------------------------------------------------------------------------- #
def process(cik: int):
    try:
        f = pd.read_parquet(CF / f"CIK{cik:010d}.parquet")
        fl = pd.read_parquet(CF / f"CIK{cik:010d}.filings.parquet")
    except FileNotFoundError:
        return None
    f = prep(f)
    ug = f[f.tax == "us-gaap"]
    rev_fr = first_dur(ug, REV_TAGS, REV_PART_TAGS)
    oi_fr = first_dur(ug, [OPINC_TAG])
    q_rev, a_rev = quarter_table(rev_fr, positive=True)
    q_oi, a_oi = quarter_table(oi_fr, positive=False)
    Srev, Soi = Series(q_rev), Series(q_oi)
    assets = first_inst(ug, "us-gaap", "Assets", "USD")
    rpo = first_inst(ug, "us-gaap", RPO_TAG, "USD")
    Srpo = Series(rpo)
    fcs = FCS(a_rev, a_oi)
    ann_rev = AsOf(a_rev.assign(e2=a_rev.end), "e2")
    as_assets = AsOf(assets.assign(e2=assets.end), "e2")
    dei_sh = f[(f.tax == "dei") & (f.tag == "EntityCommonStockSharesOutstanding") & (f.val > 0)][["end", "val", "filed"]]
    as_dei = AsOf(dei_sh.assign(basis=dei_sh.end), "basis")
    gsh = first_inst(ug, "us-gaap", "CommonStockSharesOutstanding", "shares")
    gsh = gsh[gsh.val > 0]
    as_gsh = AsOf(gsh.assign(basis=gsh.filed), "basis")
    w = ug[(ug.tag == "WeightedAverageNumberOfSharesOutstandingBasic") & (ug.unit == "shares") & ug.start.notna()]
    w = w.sort_values(["start", "end", "filed"]).drop_duplicates(["start", "end"])[["end", "val", "filed"]]
    w = w[w.val > 0]
    as_wan = AsOf(w.assign(basis=w.filed), "basis")
    flt = f[(f.tax == "dei") & (f.tag == "EntityPublicFloat")][["end", "val", "filed"]]
    as_flt = AsOf(flt.assign(e2=flt.end), "e2")

    def asof_block(T) -> dict:
        out = {}
        r = ann_rev.at(T)
        out["fy_rev"], out["fy_end"] = (r[0], r[2]) if r else (np.nan, pd.NaT)
        r = as_assets.at(T)
        out["assets"] = r[0] if r else np.nan
        r = as_flt.at(T)
        out["pfloat"] = r[0] if r else np.nan
        for k, ao in (("dei", as_dei), ("gaap", as_gsh), ("wanso", as_wan)):
            r = ao.at(T)
            if r and (T - r[2]).days <= SHARES_STALE_DAYS:
                out[f"sh_{k}"], out[f"sh_{k}_basis"] = r[0], r[1]
            else:
                out[f"sh_{k}"], out[f"sh_{k}_basis"] = np.nan, pd.NaT
        return out

    # period end of each filing: latest duration end among revenue / op income facts, else Assets
    dfacts = ug[ug.tag.isin(REV_TAGS + REV_PART_TAGS + [OPINC_TAG]) & ug.start.notna()]
    pe = dfacts.groupby("accn").end.max()
    pe2 = ug[ug.tag == "Assets"].groupby("accn").end.max()
    fl = fl[fl.form.isin(TRIGGER)].drop_duplicates("accn").copy()
    fl["filed"] = pd.to_datetime(fl.filed, errors="coerce")
    fl = fl.dropna(subset=["filed"])
    rows = []
    for r in fl.itertuples(index=False):
        E = pe.get(r.accn, pe2.get(r.accn, pd.NaT))
        fm = formation_month(r.filed)
        T = last_trading_day(fm.year, fm.month)
        d = dict(cik=cik, accn=r.accn, form=r.form, filed=r.filed, period_end=E, fm=fm, T=T)
        d.update(asof_block(T))
        d["fcs"] = fcs.at(r.filed)
        d.update(signal_fields(E, r.filed, Srev, Soi, Srpo))
        rows.append(d)
    snaps = []
    for Y in range(2010, 2027):
        T = last_trading_day(Y, 6)
        d = dict(cik=cik, year=Y, T=T)
        d.update(asof_block(T))
        d["fcs"] = fcs.at(T)
        snaps.append(d)
    diag = {
        "n_q_rev": len(q_rev), "n_q_rev_derived": int((q_rev.src != "direct").sum()) if len(q_rev) else 0,
        "n_fy_rev": len(a_rev), "n_rpo": len(rpo),
    }
    return rows, snaps, diag


def signal_fields(E, filed, Srev, Soi, Srpo) -> dict:
    out = dict(rev_q0=np.nan, g0=np.nan, g1=np.nan, accel=np.nan, q0_src=None, q0_tag=None,
               margin_q0=np.nan, fwd_margin_chg_pp=np.nan, fwd_rev_growth=np.nan, fwd_growth_chg=np.nan,
               rpo=np.nan, rpo_prev=np.nan, rpo_growth=np.nan, gap=np.nan)
    if pd.isna(E):
        return out
    E = np.datetime64(E, "D")
    av = np.datetime64(filed, "D")
    i0 = Srev.find(E - 3 * DAY, E + 3 * DAY, av)
    if i0 is None:
        return out
    e0 = Srev.end[i0]
    out["rev_q0"] = Srev.val[i0]
    out["q0_src"] = Srev.t.src.iloc[i0]
    out["q0_tag"] = Srev.t.tag.iloc[i0]
    i4 = Srev.find(e0 - 380 * DAY, e0 - 350 * DAY, av)
    if i4 is not None and Srev.val[i4] > 0 and Srev.val[i0] > 0:
        out["g0"] = Srev.val[i0] / Srev.val[i4] - 1
    i1 = Srev.find(e0 - 125 * DAY, e0 - 70 * DAY, av)
    if i1 is not None:
        i5 = Srev.find(Srev.end[i1] - 380 * DAY, Srev.end[i1] - 350 * DAY, av)
        if i5 is not None and Srev.val[i5] > 0 and Srev.val[i1] > 0:
            out["g1"] = Srev.val[i1] / Srev.val[i5] - 1
    out["accel"] = out["g0"] - out["g1"]

    def margin(ir, avail=None):
        if ir is None or not Srev.val[ir] > 0:
            return np.nan
        e = Srev.end[ir]
        io = Soi.find(e - 3 * DAY, e + 3 * DAY, avail)
        if io is None:
            return np.nan
        return Soi.val[io] / Srev.val[ir]

    out["margin_q0"] = margin(i0, av)
    # next reported quarter (fundamental check; its own first-reported values)
    iN = Srev.find(e0 + 70 * DAY, e0 + 125 * DAY)
    if iN is not None:
        iNy = Srev.find(Srev.end[iN] - 380 * DAY, Srev.end[iN] - 350 * DAY)
        if iNy is not None:
            mN, mNy = margin(iN), margin(iNy)
            out["fwd_margin_chg_pp"] = 100 * (mN - mNy)
            if Srev.val[iNy] > 0 and Srev.val[iN] > 0:
                out["fwd_rev_growth"] = Srev.val[iN] / Srev.val[iNy] - 1
                out["fwd_growth_chg"] = out["fwd_rev_growth"] - out["g0"]
    # remaining performance obligations at the quarter end
    ir = Srpo.find(e0 - 3 * DAY, e0 + 3 * DAY, av)
    if ir is not None:
        out["rpo"] = Srpo.val[ir]
        iry = Srpo.find(Srpo.end[ir] - 380 * DAY, Srpo.end[ir] - 350 * DAY, av)
        if iry is not None:
            out["rpo_prev"] = Srpo.val[iry]
            if Srpo.val[iry] > 0:
                out["rpo_growth"] = Srpo.val[ir] / Srpo.val[iry] - 1
                out["gap"] = out["rpo_growth"] - out["g0"]
    return out


def main():
    ciks = sorted(int(p.name[3:13]) for p in CF.glob("CIK*.filings.parquet"))
    print(f"{len(ciks)} companies", flush=True)
    rows, snaps, diag = [], [], []
    with Pool(6) as pool:
        for i, res in enumerate(pool.imap_unordered(process, ciks, chunksize=8), 1):
            if res is None:
                continue
            r, s, d = res
            rows += r
            snaps += s
            diag.append(d)
            if i % 500 == 0:
                print(f"  {i}/{len(ciks)}", flush=True)
    F = pd.DataFrame(rows)
    S = pd.DataFrame(snaps)
    for c in ("q0_src", "q0_tag"):
        F[c] = F[c].astype("string")
    F.to_parquet(CACHE / "filings.parquet", index=False)
    S.to_parquet(CACHE / "snapshot.parquet", index=False)
    D = pd.DataFrame(diag)
    log = {
        "n_companies": len(ciks), "n_trigger_filings": int(len(F)),
        "n_with_period_end": int(F.period_end.notna().sum()),
        "n_with_rev_q0": int(F.rev_q0.notna().sum()), "n_with_accel": int(F.accel.notna().sum()),
        "n_with_fcs": int(F.fcs.notna().sum()), "n_with_rpo": int(F.rpo.notna().sum()),
        "n_with_gap": int(F.gap.notna().sum()),
        "q0_src_counts": F.q0_src.value_counts().to_dict(),
        "q0_tag_counts": F.q0_tag.value_counts().to_dict(),
        "quarters_total": int(D.n_q_rev.sum()), "quarters_q4_derived": int(D.n_q_rev_derived.sum()),
    }
    (CACHE / "build_log.json").write_text(json.dumps(log, indent=1, default=str))
    print(json.dumps(log, indent=1, default=str))


if __name__ == "__main__":
    sys.exit(main())
