#!/usr/bin/env python3
"""Tests for the casino nowcast pilot (PREREG.md 'Tests'), run AFTER the Deviations section of
PREREG.md was written.  Reads data/nowcast_panel.csv.gz (scripts/build_nowcast.py), prices, shares
and Yahoo EPS estimates; writes results.json and RESULTS.md.

Return windows
  announcement: close of the last trading day BEFORE the 8-K filing date -> close of the first
                trading day AFTER it (covers releases before the open and after the close);
                abnormal = stock minus SPY over the same window (Yahoo adjusted closes).
  drift       : close of the last trading day before the publication date of the latest monthly
                state report used in the nowcast (actual date where known, else month-end + 30 days)
                -> close of the last trading day before the filing date (the start of the
                announcement window).  Dropped when that publication date is not before the window.
Signals are winsorised at the 5th/95th percentiles of the test sample and divided by their SD, so
slopes are in return points per one standard deviation of signal.  t-statistics cluster by calendar
quarter (fiscal quarter end).
"""
import json, math
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SMALL_CAP = 2e9
COVID = (pd.Timestamp("2020-01-01"), pd.Timestamp("2021-06-30"))   # fiscal quarter ends in this range


# ----------------------------------------------------------------------------- prices
class Px:
    def __init__(self):
        p = pd.read_csv(DATA / "prices.csv.gz", parse_dates=["date"])
        self.adj = p.pivot_table(index="date", columns="ticker", values="adj_close")
        self.close = p.pivot_table(index="date", columns="ticker", values="close")
        self.days = self.adj["SPY"].dropna().index
        sp = pd.read_csv(DATA / "splits.csv.gz", parse_dates=["date"])
        self.splits = sp

    def before(self, d):
        i = self.days.searchsorted(pd.Timestamp(d), side="left") - 1
        return self.days[i] if i >= 0 else None

    def after(self, d):
        i = self.days.searchsorted(pd.Timestamp(d), side="right")
        return self.days[i] if i < len(self.days) else None

    def ret(self, t, d0, d1):
        if d0 is None or d1 is None or d1 <= d0 or t not in self.adj:
            return np.nan
        a, b = self.adj.at[d0, t], self.adj.at[d1, t]
        return b / a - 1 if pd.notna(a) and pd.notna(b) and a > 0 else np.nan

    def raw_close(self, t, d):
        c = self.close.at[d, t] if t in self.close and d in self.close.index else np.nan
        f = self.splits[(self.splits["ticker"] == t) & (self.splits["date"] > d)]["ratio"].prod()
        return c * f


def basic_shares() -> pd.DataFrame:
    """Fallback share count when a company has no dei cover-page count in companyfacts (Red Rock):
    us-gaap WeightedAverageNumberOfSharesOutstandingBasic for 3-month periods, by filing date.  For
    Red Rock this is the listed Class A stock only (the Fertitta family's LLC units are excluded).
    Added after the first test run, which left Red Rock out of the size split for lack of a count."""
    import gzip, sys
    sys.path.insert(0, str(ROOT / "scripts"))
    from sec_fetch import COMPANIES
    rows = []
    for comp, ciks in COMPANIES.items():
        for cik in ciks:
            p = ROOT / "cache" / "sec" / "companyfacts" / f"CIK{cik:010d}.json.gz"
            if not p.exists():
                continue
            g = json.load(gzip.open(p, "rt")).get("facts", {}).get("us-gaap", {})
            for f in g.get("WeightedAverageNumberOfSharesOutstandingBasic", {}).get("units", {}).get("shares", []):
                if "start" in f and 80 <= (pd.Timestamp(f["end"]) - pd.Timestamp(f["start"])).days <= 100:
                    rows.append(dict(company=comp, filed=pd.Timestamp(f["filed"]), val=f["val"]))
    return pd.DataFrame(rows)


def add_returns(df: pd.DataFrame, px: Px) -> pd.DataFrame:
    sh = pd.read_csv(DATA / "shares_out.csv.gz", parse_dates=["filed"])
    sb = basic_shares()
    out = []
    for _, r in df.iterrows():
        a = pd.Timestamp(r["ann_date"])
        t0, t1 = px.before(a), px.after(a)
        rs, rm = px.ret(r["ticker"], t0, t1), px.ret("SPY", t0, t1)
        lp = pd.Timestamp(r["last_pub"]) if pd.notna(r.get("last_pub")) else None
        d0 = px.before(lp) if lp is not None else None
        if d0 is not None and t0 is not None and d0 < t0:
            ds, dm = px.ret(r["ticker"], d0, t0), px.ret("SPY", d0, t0)
        else:
            ds = dm = np.nan
        s = sh[(sh["company"] == r["company"]) & (sh["filed"] < a)].sort_values("filed")
        shares = s["val"].iloc[-1] if len(s) else np.nan
        shares_src = "cover page" if len(s) else ""
        if not len(s):
            b = sb[(sb["company"] == r["company"]) & (sb["filed"] < a)].sort_values("filed")
            if len(b):
                shares, shares_src = b["val"].iloc[-1], "weighted basic"
        mcap = shares * px.raw_close(r["ticker"], t0) if t0 is not None else np.nan
        out.append(dict(ann_t0=t0, ann_t1=t1, ret_stock=rs, ret_spy=rm, abn=rs - rm,
                        drift_t0=d0, drift_abn=ds - dm, drift_days=(t0 - d0).days if (d0 is not None and t0 is not None) else np.nan,
                        shares=shares, shares_src=shares_src, mcap=mcap))
    return pd.concat([df.reset_index(drop=True), pd.DataFrame(out)], axis=1)


# ----------------------------------------------------------------------------- statistics
def winsor_std(x: pd.Series):
    lo, hi = x.quantile(0.05), x.quantile(0.95)
    w = x.clip(lo, hi)
    return w / w.std(ddof=1), dict(p5=float(lo), p95=float(hi), sd=float(w.std(ddof=1)))


def ols_cluster(y, z, groups):
    X = sm.add_constant(np.asarray(z, float))
    y = np.asarray(y, float)
    g = pd.factorize(pd.Series(groups).astype(str))[0]
    m = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": g})
    return dict(slope=float(m.params[1]), t=float(m.tvalues[1]), se=float(m.bse[1]),
                intercept=float(m.params[0]), n=int(len(y)), clusters=int(len(set(g))),
                r2=float(m.rsquared))


def regression_test(d: pd.DataFrame, ycol: str, zcol: str, halves=True) -> dict:
    """Pooled OLS of ycol (in %) on the standardised signal zcol, t clustered by calendar quarter.
    zcol was winsorised and standardised once on the full test sample (see main)."""
    d = d.dropna(subset=[ycol, zcol]).sort_values("ann_date").reset_index(drop=True)
    if len(d) < 10:
        return dict(n=int(len(d)), note="too few observations")
    res = ols_cluster(d[ycol].values * 100, d[zcol].values, d["qend"].values)
    res["companies"] = int(d["company"].nunique())
    res["first_ann"] = str(pd.Timestamp(d["ann_date"].min()).date()); res["last_ann"] = str(pd.Timestamp(d["ann_date"].max()).date())
    res["mean_y"] = float(d[ycol].mean() * 100)
    if halves:
        mid = len(d) // 2
        h = []
        for part in (d.iloc[:mid], d.iloc[mid:]):
            if len(part) >= 5 and part[zcol].std() > 0:
                rr = ols_cluster(part[ycol].values * 100, part[zcol].values, part["qend"].values)
                rr["from"] = str(pd.Timestamp(part["ann_date"].min()).date()); rr["to"] = str(pd.Timestamp(part["ann_date"].max()).date())
                h.append(rr)
            else:
                h.append(dict(n=int(len(part)), slope=float("nan")))
        res["halves"] = h
        res["positive_both_halves"] = bool(all(x.get("slope", float("nan")) > 0 for x in h))
    return res


def corr_block(x: pd.Series, y: pd.Series) -> dict:
    m = x.notna() & y.notna() & np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 5:
        return dict(n=int(len(x)))
    xw = x.clip(x.quantile(0.05), x.quantile(0.95)); yw = y.clip(y.quantile(0.05), y.quantile(0.95))
    return dict(n=int(len(x)), pearson=float(np.corrcoef(x, y)[0, 1]),
                pearson_winsor=float(np.corrcoef(xw, yw)[0, 1]),
                spearman=float(stats.spearmanr(x, y).statistic),
                mae=float((x - y).abs().mean()), median_ae=float((x - y).abs().median()),
                mean_error=float((x - y).mean()))


def binom(hits: int, n: int) -> float:
    return float(stats.binomtest(hits, n, 0.5).pvalue) if n else np.nan


# ----------------------------------------------------------------------------- main
def main():
    panel = pd.read_csv(DATA / "nowcast_panel.csv.gz", parse_dates=["qend", "ann_date", "last_pub"])
    px = Px()
    R = dict(generated=str(pd.Timestamp.today().date()))
    results = {}
    tables = {}
    for sample in ["prop", "region"]:
        P = panel[(panel["sample"] == sample)]
        Q = P[P["qualifies"]].copy()
        # ---------------- accuracy (all qualifying company-quarters, priced or not)
        acc = dict(
            all=dict(rev=corr_block(Q["nc_rev_growth"], Q["rev_growth"]),
                     ebitda=corr_block(Q["nc_ebitda_growth"], Q["ebitda_growth"]),
                     companies=int(Q["company"].nunique()), n=int(len(Q))),
            no_portfolio_change=dict(
                rev=corr_block(Q.loc[~Q["portfolio_change"], "nc_rev_growth"], Q.loc[~Q["portfolio_change"], "rev_growth"]),
                ebitda=corr_block(Q.loc[~Q["portfolio_change"], "nc_ebitda_growth"], Q.loc[~Q["portfolio_change"], "ebitda_growth"])),
            ex_covid=dict(
                rev=corr_block(Q.loc[~Q["qend"].between(*COVID), "nc_rev_growth"], Q.loc[~Q["qend"].between(*COVID), "rev_growth"]),
                ebitda=corr_block(Q.loc[~Q["qend"].between(*COVID), "nc_ebitda_growth"], Q.loc[~Q["qend"].between(*COVID), "ebitda_growth"])),
        )
        # naive benchmark: last quarter's reported growth as the forecast of this quarter's
        npc = Q[~Q["portfolio_change"]]
        npx = npc[~npc["qend"].between(*COVID)]
        acc["naive_benchmark"] = dict(
            note="forecast = last quarter's reported YoY growth (the pre-registered 'more of the same' baseline)",
            all=dict(rev=corr_block(Q["rev_growth_prev"], Q["rev_growth"]), ebitda=corr_block(Q["ebitda_growth_prev"], Q["ebitda_growth"])),
            no_portfolio_change=dict(rev=corr_block(npc["rev_growth_prev"], npc["rev_growth"]), ebitda=corr_block(npc["ebitda_growth_prev"], npc["ebitda_growth"])),
            no_portfolio_change_ex_covid=dict(rev=corr_block(npx["rev_growth_prev"], npx["rev_growth"]), ebitda=corr_block(npx["ebitda_growth_prev"], npx["ebitda_growth"])))
        acc["no_portfolio_change_ex_covid"] = dict(rev=corr_block(npx["nc_rev_growth"], npx["rev_growth"]),
                                                   ebitda=corr_block(npx["nc_ebitda_growth"], npx["ebitda_growth"]))
        by_co = {}
        for c, d in Q.groupby("company"):
            by_co[c] = dict(n=int(len(d)), rev=corr_block(d["nc_rev_growth"], d["rev_growth"]),
                            ebitda=corr_block(d["nc_ebitda_growth"], d["ebitda_growth"]),
                            coverage_median=float(d["coverage"].median()),
                            first=str(d["qend"].min().date()), last=str(d["qend"].max().date()),
                            priced=bool(d["priced"].any()))
        acc["by_company"] = by_co
        # ---------------- tests (priced)
        T = Q[Q["priced"]].copy()
        T = add_returns(T, px)
        T = T[T["abn"].notna()].copy()
        T["small"] = T["mcap"] < SMALL_CAP
        wins = {}
        for sc, zc in [("sig_ebitda", "z_ebitda"), ("sig_rev", "z_rev"), ("sig_ebitda_all3", "z_all3")]:
            m = T[sc].notna()
            T.loc[m, zc], wins[sc] = winsor_std(T.loc[m, sc])
        tables[sample] = T
        res = dict(n=int(len(T)), companies=sorted(T["company"].unique().tolist()),
                   quarters=int(T["qend"].nunique()),
                   states=sorted(set(",".join(T["states"].dropna()).split(",")) - {""}),
                   years=f"{T['ann_date'].min().year}-{T['ann_date'].max().year}" if len(T) else "")
        res["accuracy_test_sample"] = dict(rev=corr_block(T["nc_rev_growth"], T["rev_growth"]),
                                           ebitda=corr_block(T["nc_ebitda_growth"], T["ebitda_growth"]))
        res["winsor"] = wins
        res["primary"] = regression_test(T, "abn", "z_ebitda")
        res["drift"] = regression_test(T, "drift_abn", "z_ebitda")
        res["revenue_only"] = regression_test(T, "abn", "z_rev")
        res["all3_months_spec_literal"] = regression_test(T, "abn", "z_all3")
        res["ex_covid"] = regression_test(T[~T["qend"].between(*COVID)], "abn", "z_ebitda")
        res["small_caps"] = regression_test(T[T["small"]], "abn", "z_ebitda", halves=False)
        res["larger"] = regression_test(T[~T["small"] & T["mcap"].notna()], "abn", "z_ebitda", halves=False)
        res["small_caps_drift"] = regression_test(T[T["small"]], "drift_abn", "z_ebitda", halves=False)
        res["larger_drift"] = regression_test(T[~T["small"] & T["mcap"].notna()], "drift_abn", "z_ebitda", halves=False)
        res["small_caps_revenue_only"] = regression_test(T[T["small"]], "abn", "z_rev", halves=False)
        res["larger_revenue_only"] = regression_test(T[~T["small"] & T["mcap"].notna()], "abn", "z_rev", halves=False)
        res["by_company"] = {c: dict(n=int(len(d)), mean_abn=float(d["abn"].mean() * 100),
                                     corr_sig_abn=float(d[["sig_ebitda", "abn"]].corr().iloc[0, 1]) if len(d) > 2 else None,
                                     small_share=float(d["small"].mean()))
                             for c, d in T.groupby("company")}
        # ---------------- analyst estimates (Yahoo consensus EPS)
        eps = pd.read_csv(DATA / "eps_surprise.csv.gz", parse_dates=["earn_date"])
        hits = n = 0; rows = []
        for _, r in T.iterrows():
            e = eps[(eps["ticker"] == r["ticker"]) & ((eps["earn_date"] - r["ann_date"]).abs() <= pd.Timedelta(days=4))]
            e = e.dropna(subset=["eps_est", "eps_rep"])
            if not len(e):
                continue
            surprise = e["eps_rep"].iloc[0] - e["eps_est"].iloc[0]
            if surprise == 0 or r["sig_ebitda"] == 0 or pd.isna(r["sig_ebitda"]):
                continue
            n += 1; h = int(np.sign(surprise) == np.sign(r["sig_ebitda"])); hits += h
            rows.append(dict(company=r["company"], qend=str(r["qend"].date()), surprise=surprise, sig=r["sig_ebitda"], hit=h, small=bool(r["small"])))
        er = pd.DataFrame(rows)
        res["analyst"] = dict(source="Yahoo Finance earnings calendar via yfinance (consensus EPS estimate vs reported adjusted EPS)",
                              n=n, hits=hits, hit_rate=hits / n if n else None, binom_p=binom(hits, n),
                              small=dict(n=int(er["small"].sum()) if len(er) else 0,
                                         hit_rate=float(er.loc[er["small"], "hit"].mean()) if len(er) and er["small"].any() else None,
                                         binom_p=binom(int(er.loc[er["small"], "hit"].sum()), int(er["small"].sum())) if len(er) else None),
                              larger=dict(n=int((~er["small"]).sum()) if len(er) else 0,
                                          hit_rate=float(er.loc[~er["small"], "hit"].mean()) if len(er) and (~er["small"]).any() else None,
                                          binom_p=binom(int(er.loc[~er["small"], "hit"].sum()), int((~er["small"]).sum())) if len(er) else None))
        res["accuracy_all_qualifying"] = acc
        results[sample] = res
        T.to_csv(DATA / f"test_sample_{sample}.csv.gz", index=False)
    R["samples"] = results
    p = results["prop"]["primary"]
    R["verdict"] = "Yes" if (p.get("t", 0) >= 2.0 and p.get("positive_both_halves")) else "No"
    (ROOT / "results.json").write_text(json.dumps(R, indent=1, default=str))
    return R, tables


if __name__ == "__main__":
    R, _ = main()
    print(json.dumps({k: R["samples"][k]["primary"] for k in R["samples"]}, indent=1, default=str)[:3000])
    print("VERDICT", R["verdict"])
