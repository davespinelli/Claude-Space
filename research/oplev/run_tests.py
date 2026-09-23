#!/usr/bin/env python3
"""
Operating-leverage study: pre-registered tests.

Reads research/oplev/panel.parquet and research/oplev/cache/returns.parquet
(both written by build_panel.py) and writes:

    research/oplev/results.json          every number, machine-readable
    research/oplev/quintile_returns.csv  monthly returns per quintile / cell + IWM, SPY
    research/oplev/RESULTS.md            plain-English write-up

PRE-REGISTERED DEFINITIONS (fixed before any return was computed; not tuned)
---------------------------------------------------------------------------
Formation: end of June of year t = 2011..2025, fundamentals from frames CY(t-1)
(fiscal year ended <= Feb of year t, see build_panel.py). Holding July t .. June
t+1, monthly returns, annual rebalance. Universe: non-financial (SIC 6000-6999
out), non-utility (4900-4999 out), revenue > $10M, assets > 0, market cap >= $50M.

  H1  OL  = (revenue - operating income) / total assets, CY(t-1). Quintiles.
          Hypothesised winner: Q5 (high OL).
  H2a FCS = a / mean(cost) from OLS cost = a + b*revenue over fiscal years
          t-5..t-1 (>= 4 of 5), clipped to [-1, 1]. Quintiles. Winner: Q5.
  H2b 3x3 independent double sort, FCS terciles x acceleration terciles
          (acceleration = growth(t-1) - growth(t-2)). Winner: HH (high FCS,
          high acceleration). Headline spread: HH minus the equal-weighted
          average of the other 8 cells. Also reported: HH - LH (high vs low FCS
          among accelerating firms) and the difference-in-differences
          (HH - HL) - (LH - LL). Fundamental check: median change in operating
          margin CY t vs CY t-1 by cell.
  H3  among firms with revenue growth(t-1) > 0: quintiles of operating-margin
          change (t-1 minus t-2, percentage points). Winner: Q5 (most expansion).

Breakpoints: quantiles of the signal across priced universe firms (a value
equal to a breakpoint goes to the lower group). Industry-neutral: breakpoints
within 2-digit SIC x year, groups with < 5 firms dropped. Size: breakpoints
within small (< $2B) and large (>= $2B) separately.

Portfolio returns: equal-weighted (primary) = simple average of the members'
returns each month; value-weighted (secondary) = formation market cap grown by
each stock's own return through the previous month (buy and hold).
Spread = winner minus loser, monthly; t-stat = mean / (sd / sqrt(n)).
"X% a year" = difference of the two annualised (compound) returns.

Survivorship scenarios for the headline equal-weighted spreads:
 (a) missing firms excluded; a stock whose price series stops mid-year simply
     drops out after its last month;
 (b) every missing firm-year earns -30% over the holding year (spread evenly
     over 12 months) and a stock whose series stops mid-year earns -30% in the
     month after its last price;
 (c) same with +15%.
"Missing" = passes the fundamentals filters (SIC, revenue, assets, look-ahead
guard) but has no Yahoo price at the formation date, so neither its market cap
nor its return is known. Placed in quintiles with the priced breakpoints.
Reported for all missing firms and for the subset whose last reported public
float (dei:EntityPublicFloat) was >= $50M, a proxy for passing the size filter.

Verdict rule (fixed in advance), applied to the headline EW spread:
  "Yes"   t >= 2.0 in the hypothesised direction AND positive in both halves
          AND industry-neutral spread positive AND positive under (a), (b), (c)
          (both missing-firm sets);
  "Mixed" t >= 2.0 but at least one of those robustness checks fails;
  "No"    t < 2.0 (including the wrong sign); "No (reversed)" if t <= -2.0.
H2b additionally needs the fundamental check (HH shows the largest margin
expansion) for a "Yes".

Price-data error rule (fixed from the return distribution before any portfolio
was computed): see clean_returns().
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
COST = 0.005                     # 0.5% a year trading cost on the "top" portfolio
FIRST_HALF = range(2011, 2018)   # formations 2011-2017
SECOND_HALF = range(2018, 2026)  # formations 2018-2025
SCEN = {"b_minus30": -0.30, "c_plus15": 0.15}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def ann(r: pd.Series) -> float:
    r = r.dropna()
    if len(r) == 0:
        return float("nan")
    return float((1 + r).prod() ** (12 / len(r)) - 1)


def tstat(x: pd.Series) -> float:
    x = x.dropna()
    if len(x) < 3 or x.std(ddof=1) == 0:
        return float("nan")
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def nw_t(x: pd.Series, lags: int = 6) -> float:
    x = x.dropna().to_numpy(float)
    n = len(x)
    if n < 3:
        return float("nan")
    e = x - x.mean()
    s = (e @ e) / n
    for L in range(1, lags + 1):
        s += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / n
    return float(x.mean() / math.sqrt(s / n))


def rnd(x, k=4):
    if x is None:
        return None
    if isinstance(x, (float, np.floating)):
        return None if not np.isfinite(x) else round(float(x), k)
    if isinstance(x, (int, np.integer)):
        return int(x)
    return x


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return rnd(o)


def breakpoints(x: pd.Series, n: int) -> np.ndarray:
    return np.nanquantile(x.to_numpy(float), [k / n for k in range(1, n)])


def bucket(x: pd.Series, bps: np.ndarray) -> pd.Series:
    out = pd.Series(np.nan, index=x.index)
    ok = x.notna()
    v = x[ok].to_numpy(float)
    out[ok] = 1 + (v[:, None] > bps[None, :]).sum(axis=1)
    return out


def sort_groups(df: pd.DataFrame, sig: str, n: int, within: str | None = None,
                min_group: int = 5) -> pd.Series:
    """Group number 1..n per row. Breakpoints come from priced rows (df.in_univ),
    applied to every row (priced and missing). Optional grouping column."""
    out = pd.Series(np.nan, index=df.index)
    for t, d in df.groupby("year"):
        if within is None:
            parts = [(None, d)]
        else:
            parts = list(d.groupby(within))
        for _, g in parts:
            pri = g[g.in_univ & g[sig].notna()]
            if within is not None and len(pri) < min_group:
                continue
            if len(pri) < n:
                continue
            out[g.index] = bucket(g[sig], breakpoints(pri[sig], n))
    return out


# --------------------------------------------------------------------------- #
# returns
# --------------------------------------------------------------------------- #
def clean_returns(R: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Price-data error rule (data integrity, fixed before any portfolio return
    was computed, after listing the extreme months of held stocks):
      1. non-positive prices are invalid (done in build_panel: adj <= 0 -> missing);
      2. a one-month round trip of 10x or more (a return <= -90% followed next
         month by >= +900%, or the reverse) is a bad print: both months missing;
      3. any remaining monthly return above +1,000% is treated as a splice error
         (e.g. a bankrupt company's old shares joined to the new equity, or an
         ADR-ratio change) and set missing. This also drops one known genuine
         month, GameStop in January 2021 (+1,625%); the raw-return robustness
         line in results.json shows whether that matters.
    Returns the cleaned matrix and the number of stock-months changed."""
    A = R.to_numpy(copy=True)
    n_v = 0
    for j in range(A.shape[1]):
        col = A[:, j]
        for i in range(len(col) - 1):
            a, b = col[i], col[i + 1]
            if np.isfinite(a) and np.isfinite(b) and ((a <= -0.9 and b >= 9) or (a >= 9 and b <= -0.9)):
                col[i] = np.nan
                col[i + 1] = np.nan
                n_v += 1
        A[:, j] = col
    big = np.isfinite(A) & (A > 10)
    n_big = int(big.sum())
    A[big] = np.nan
    out = pd.DataFrame(A, index=R.index, columns=R.columns)
    return out, {"v_reversals_removed": n_v, "returns_above_1000pct_removed": n_big}


class Book:
    """Holdings x months table for all formation years."""

    def __init__(self, P: pd.DataFrame, R: pd.DataFrame):
        self.P = P
        rows = []
        for t, d in P[P.in_univ].groupby("year"):
            months = pd.date_range(pd.Timestamp(t, 7, 1), pd.Timestamp(t + 1, 6, 1), freq="MS")
            months = [m for m in months if m in R.index]
            tk = d.ticker
            sub = R.loc[months, [c for c in tk.unique() if c in R.columns]]
            lg = sub.stack(future_stack=True).rename("ret").reset_index()
            lg.columns = ["month", "ticker", "ret"]
            lg = lg.merge(d[["cik", "ticker", "mcap"]].reset_index().rename(columns={"index": "pid"}),
                          on="ticker")
            lg["year"] = t
            rows.append(lg)
        H = pd.concat(rows, ignore_index=True).sort_values(["pid", "month"])
        g = (1 + H.ret.fillna(0.0)).groupby(H.pid).cumprod()
        H["w"] = H.mcap * g.groupby(H.pid).shift(1).fillna(1.0)
        H = H.dropna(subset=["ret"])
        self.H = H
        # months after which a stock's series stops mid-year (for scenarios b/c)
        ended = P[P.in_univ & P.series_ended_in_hold]
        last = H.groupby("pid").month.max()
        dl = []
        for pid, r in ended.iterrows():
            t = r.year
            lm = last.get(pid, pd.Timestamp(t, 6, 1))
            m = (lm + pd.offsets.MonthBegin(1))
            if m <= pd.Timestamp(t + 1, 6, 1):
                dl.append((pid, m))
        self.delist = pd.DataFrame(dl, columns=["pid", "month"])

    def port(self, label: pd.Series, vw: bool = False, scen: float | None = None,
             missing_label: pd.Series | None = None) -> pd.DataFrame:
        """Monthly returns (month x group) for a pid -> group mapping."""
        H = self.H[self.H.pid.isin(label.dropna().index)].copy()
        H["g"] = H.pid.map(label)
        if scen is not None and not vw:
            extra = []
            d = self.delist[self.delist.pid.isin(label.dropna().index)].copy()
            if len(d):
                d["g"] = d.pid.map(label)
                d["ret"] = scen
                extra.append(d[["pid", "month", "g", "ret"]])
            if missing_label is not None:
                ml = missing_label.dropna()
                if len(ml):
                    mr = (1 + scen) ** (1 / 12) - 1
                    yrs = self.P.loc[ml.index, "year"]
                    for t in sorted(yrs.unique()):
                        pids = yrs.index[yrs == t]
                        months = pd.date_range(pd.Timestamp(t, 7, 1), pd.Timestamp(t + 1, 6, 1), freq="MS")
                        months = [m for m in months if m in self.months]
                        e = pd.DataFrame([(p, m) for p in pids for m in months], columns=["pid", "month"])
                        e["g"] = e.pid.map(ml)
                        e["ret"] = mr
                        extra.append(e)
            if extra:
                H = pd.concat([H[["pid", "month", "g", "ret"]]] + extra, ignore_index=True)
        if vw:
            H["wr"] = H.w * H.ret
            s = H.groupby(["month", "g"])[["wr", "w"]].sum()
            out = (s.wr / s.w).unstack("g")
        else:
            out = H.groupby(["month", "g"]).ret.mean().unstack("g")
        return out.sort_index()

    @property
    def months(self):
        return set(self.H.month.unique())


def spread_stats(top: pd.Series, bot: pd.Series) -> dict:
    s = (top - bot).dropna()
    yrs = {}
    for m, v in s.items():
        t = m.year if m.month >= 7 else m.year - 1
        yrs.setdefault(t, []).append(m)
    pos = 0
    by_year = {}
    for t, ms in sorted(yrs.items()):
        a = float((1 + top.loc[ms]).prod() - 1)
        b = float((1 + bot.loc[ms]).prod() - 1)
        by_year[t] = a - b
        pos += int(a > b)
    return {
        "ann_top": ann(top.loc[s.index]), "ann_bottom": ann(bot.loc[s.index]),
        "ann_diff": ann(top.loc[s.index]) - ann(bot.loc[s.index]),
        "mean_monthly_x12": float(s.mean() * 12), "t": tstat(s), "t_nw6": nw_t(s),
        "n_months": int(len(s)), "years_positive": pos, "n_years": len(by_year),
        "by_year": by_year,
    }


def half(df: pd.DataFrame, yrs) -> pd.DataFrame:
    keep = [m for m in df.index if (m.year if m.month >= 7 else m.year - 1) in yrs]
    return df.loc[keep]


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    P = pd.read_parquet(HERE / "panel.parquet")
    P = P.reset_index(drop=True)
    R_raw = pd.read_parquet(CACHE / "returns.parquet")
    R_raw.index = pd.to_datetime(R_raw.index)
    R, rinfo = clean_returns(R_raw.drop(columns=[c for c in ("IWM", "SPY") if c in R_raw.columns]))
    bench = R_raw[["IWM", "SPY"]]
    res = {"meta": {"formations": "2011-2025 (end of June)", "holding": "July t - June t+1",
                    "price_error_rule": rinfo}}
    book = Book(P, R)
    book_raw = Book(P, R_raw.drop(columns=[c for c in ("IWM", "SPY") if c in R_raw.columns]))
    # diagnostic: raw returns with only the single largest held monthly return removed
    top1 = book_raw.H.loc[book_raw.H.ret.abs().idxmax()]
    R_raw1 = R_raw.drop(columns=[c for c in ("IWM", "SPY") if c in R_raw.columns]).copy()
    R_raw1.loc[top1.month, top1.ticker] = np.nan
    book_raw1 = Book(P, R_raw1)
    res["meta"]["largest_held_raw_month"] = {"ticker": top1.ticker, "month": str(top1.month.date()),
                                            "raw_return": float(top1.ret)}
    Hc = book.H.set_index(["pid", "month"]).ret
    Hr = book_raw.H.set_index(["pid", "month"]).ret
    gone = Hr.index.difference(Hc.index)
    res["meta"]["held_stock_months_changed_by_rule"] = [
        {"ticker": P.at[pid, "ticker"], "formation": int(P.at[pid, "year"]), "month": str(m.date()),
         "raw_return": float(Hr[(pid, m)])} for pid, m in gone]
    U = P[P.in_univ]
    Pm = P[P.in_univ | P.missing].copy()    # rows that can be sorted (priced universe + missing)

    # ---------------- universe / coverage ----------------
    cov = {}
    for t, d in P.groupby("year"):
        fo = d[d.fund_ok]
        cov[t] = {
            "frames_rows_CY": int(len(d)),
            "late_fye_dropped": int((d.late_fye & d.sic_ok & (d.revenue > 10e6) & (d.assets > 0)).sum()),
            "fund_ok": int(len(fo)),
            "priced": int(fo.priced.sum()),
            "priced_no_shares": int(d.priced_no_shares.sum()),
            "priced_mcap_below_50m": int((fo.priced & (fo.mcap < 50e6)).sum()),
            "universe": int(d.in_univ.sum()),
            "universe_small": int((d.in_univ & (d["size"] == "small")).sum()),
            "universe_large": int((d.in_univ & (d["size"] == "large")).sum()),
            "missing": int(d.missing.sum()),
            "missing_float_ge_50m": int((d.missing & (d.pfloat >= 50e6)).sum()),
            "missing_no_ticker": int((d.missing_reason == "no_ticker").sum()),
            "missing_ticker_no_yahoo": int((d.missing_reason == "ticker_no_yahoo_data").sum()),
            "missing_no_price_at_formation": int((d.missing_reason == "no_price_at_formation").sum()),
            "not_yet_listed_excluded": int(d.not_yet_listed.sum()),
            "universe_hist_ticker": int((d.in_univ & (d.ticker_src == "hist")).sum()),
            "universe_with_opinc": int((d.in_univ & d.opinc.notna()).sum()),
            "series_ended_in_hold": int((d.in_univ & d.series_ended_in_hold).sum()),
        }
        c = cov[t]
        c["missing_share"] = c["missing"] / (c["universe"] + c["missing"]) if c["universe"] + c["missing"] else None
        c["missing_share_float50"] = (c["missing_float_ge_50m"] / (c["universe"] + c["missing_float_ge_50m"])
                                      if c["universe"] else None)
    nu = pd.Series({t: v["universe"] for t, v in cov.items()})
    tot_u = sum(v["universe"] for v in cov.values())
    tot_m = sum(v["missing"] for v in cov.values())
    tot_m50 = sum(v["missing_float_ge_50m"] for v in cov.values())
    res["universe"] = {
        "per_year": cov, "n_min": int(nu.min()), "n_median": float(nu.median()), "n_max": int(nu.max()),
        "missing_share_overall": tot_m / (tot_u + tot_m),
        "missing_share_overall_float50": tot_m50 / (tot_u + tot_m50),
        "firm_years_universe": tot_u, "firm_years_missing": tot_m, "firm_years_missing_float50": tot_m50,
        "distinct_firms_universe": int(U.cik.nunique()),
        "share_source_in_universe": U.shares_src.value_counts().to_dict(),
        "rev_tag_in_universe": U.rev_tag.value_counts().to_dict(),
        "universe_opinc_coverage": float(U.opinc.notna().mean()),
    }
    # market-cap sanity: mcap vs last public float
    rr = (U.pfloat / U.mcap).replace([np.inf, -np.inf], np.nan).dropna()
    res["universe"]["float_to_mcap_ratio"] = {
        "n": int(len(rr)), "median": float(rr.median()),
        "share_gt_2": float((rr > 2).mean()), "share_gt_5": float((rr > 5).mean()),
        "share_lt_0_1": float((rr < 0.1).mean())}

    # ---------------- benchmarks ----------------
    univ_ew = book.port(pd.Series(1, index=U.index)).iloc[:, 0].rename("UNIV_EW")
    months = univ_ew.index
    iwm = bench["IWM"].reindex(months)
    spy = bench["SPY"].reindex(months)
    res["benchmarks"] = {"UNIV_EW_ann": ann(univ_ew), "IWM_ann": ann(iwm), "SPY_ann": ann(spy),
                         "n_months": int(len(months)), "first_month": str(months.min().date()),
                         "last_month": str(months.max().date())}
    ones = pd.Series(1, index=U.index)
    for nm, rr in SCEN.items():
        for lab, msk in (("all_missing", P.missing), ("float50_missing", P.missing & (P.pfloat >= 50e6))):
            e = book.port(ones, scen=rr, missing_label=pd.Series(1, index=P.index[msk]))
            res["benchmarks"][f"UNIV_EW_ann_{nm}_{lab}"] = ann(e[1].reindex(months))
    csv_cols = {"UNIV_EW": univ_ew, "IWM": iwm, "SPY": spy}

    # ---------------- tests ----------------
    tests = {
        "H1_OL": dict(sig="OL", n=5, sample=lambda d: d.OL.notna()),
        "H2a_FCS": dict(sig="FCS", n=5, sample=lambda d: d.FCS.notna()),
        "H3_margin_chg": dict(sig="margin_chg_pp", n=5,
                              sample=lambda d: (d.rev_growth > 0) & d.margin_chg_pp.notna()),
    }
    for name, spec in tests.items():
        sig, n = spec["sig"], spec["n"]
        D = Pm[spec["sample"](Pm)].copy()
        out = {"signal": sig, "n_groups": n}
        q = sort_groups(D, sig, n)
        qU = q[D.in_univ]
        qM = q[D.missing]
        qM50 = q[D.missing & (D.pfloat >= 50e6)]
        ew = book.port(qU)
        vw = book.port(qU, vw=True)
        out["n_firms_per_year"] = D[D.in_univ].groupby("year").size().to_dict()
        out["avg_firms_per_group"] = float(qU.groupby(D.loc[qU.index, "year"]).size().mean() / n)
        out["ew_ann"] = {int(k): ann(ew[k]) for k in ew.columns}
        out["vw_ann"] = {int(k): ann(vw[k]) for k in vw.columns}
        out["ew_spread"] = spread_stats(ew[n], ew[1])
        out["vw_spread"] = spread_stats(vw[n], vw[1])
        # industry neutral
        qi = sort_groups(D, sig, n, within="sic2")
        ewi = book.port(qi[D.in_univ])
        out["ind_neutral_ew_ann"] = {int(k): ann(ewi[k]) for k in ewi.columns}
        out["ind_neutral_ew_spread"] = spread_stats(ewi[n], ewi[1])
        vwi = book.port(qi[D.in_univ], vw=True)
        out["ind_neutral_vw_spread"] = spread_stats(vwi[n], vwi[1])
        # size split
        for sz in ("small", "large"):
            Ds = D[D.in_univ & (D["size"] == sz)]
            qs = sort_groups(Ds, sig, n)
            e = book.port(qs)
            out[f"{sz}_ew_ann"] = {int(k): ann(e[k]) for k in e.columns}
            out[f"{sz}_ew_spread"] = spread_stats(e[n], e[1])
            out[f"{sz}_n_per_year_median"] = float(Ds.groupby("year").size().median())
        # robustness: raw Yahoo returns (no price-error rule)
        er = book_raw.port(qU)
        out["raw_returns_ew_spread"] = spread_stats(er[n], er[1])
        er1 = book_raw1.port(qU)
        out["raw_returns_minus_largest_month_ew_spread"] = spread_stats(er1[n], er1[1])
        # halves
        out["first_half_ew_spread"] = spread_stats(half(ew, FIRST_HALF)[n], half(ew, FIRST_HALF)[1])
        out["second_half_ew_spread"] = spread_stats(half(ew, SECOND_HALF)[n], half(ew, SECOND_HALF)[1])
        # top vs universe / IWM after costs
        top = ew[n] - COST / 12
        out["top_vs"] = top_vs(top, univ_ew, iwm, spy)
        # fundamentals
        out["fundamentals_median_by_group"] = fund_table(D[D.in_univ], qU)
        # survivorship
        out["survivorship"] = survivorship(book, D, q, qU, qM, qM50, n, ew)
        tests_out = out
        res[name] = tests_out
        for k in ew.columns:
            csv_cols[f"{name}_EW_Q{int(k)}"] = ew[k]
        for k in vw.columns:
            csv_cols[f"{name}_VW_Q{int(k)}"] = vw[k]
        csv_cols[f"{name}_EW_Q{n}mQ1"] = ew[n] - ew[1]
        csv_cols[f"{name}_INDNEU_EW_Q{n}mQ1"] = ewi[n] - ewi[1]
        print(f"{name}: EW spread ann {out['ew_spread']['ann_diff']:+.4f} t {out['ew_spread']['t']:+.2f} "
              f"pos {out['ew_spread']['years_positive']}/{out['ew_spread']['n_years']}")

    # ---------------- H2b interaction ----------------
    res["H2b_FCSxAccel"], cols = interaction(Pm, book, univ_ew, iwm, spy, book_raw, book_raw1)
    csv_cols.update(cols)

    # verdicts
    for name in ("H1_OL", "H2a_FCS", "H3_margin_chg", "H2b_FCSxAccel"):
        res[name]["verdict"] = verdict(res[name], name)

    rc = CACHE / "restatement_check.json"
    if rc.exists():
        res["restatement_check"] = json.loads(rc.read_text())
    bl = CACHE / "build_log.json"
    if bl.exists():
        b = json.loads(bl.read_text())
        res["build"] = {k: v for k, v in b.get("panel", {}).items() if not k.endswith("_list")}
        res["build"]["prices"] = b.get("prices")
        res["build"]["hist_tickers"] = b.get("hist")
        res["build"]["submissions"] = {k: v for k, v in b.get("subs", {}).items() if k != "failed"}
    # accession-year diagnostic: how many CY(t-1) revenue values come from a filing made after year t
    U2 = P[P.in_univ].copy()
    yy = pd.to_numeric(U2.rev_accn.str.slice(11, 13), errors="coerce") + 2000
    res["universe"]["share_rev_value_from_filing_after_formation_year"] = float((yy > U2.year).mean())
    fye_lag = (pd.to_datetime(U2.year.astype(str) + "-06-30") - pd.to_datetime(U2.rev_end)).dt.days / 30.44
    res["universe"]["months_fye_to_formation"] = {"min": float(fye_lag.min()), "p5": float(fye_lag.quantile(0.05)),
                                                  "median": float(fye_lag.median())}
    qr = pd.DataFrame(csv_cols)
    qr.index.name = "month"
    qr.to_csv(HERE / "quintile_returns.csv", float_format="%.6f")
    (HERE / "results.json").write_text(json.dumps(clean(res), indent=1))
    write_md(clean(res))
    print("wrote results.json, quintile_returns.csv, RESULTS.md")


def top_vs(top, univ_ew, iwm, spy) -> dict:
    out = {}
    for nm, b in (("univ_ew", univ_ew), ("iwm", iwm), ("spy", spy)):
        d = (top - b).dropna()
        out[nm] = {"ann_top_net": ann(top.loc[d.index]), "ann_bench": ann(b.loc[d.index]),
                   "ann_excess": ann(top.loc[d.index]) - ann(b.loc[d.index]), "t": tstat(d),
                   "n_months": int(len(d))}
    return out


def fund_table(D: pd.DataFrame, g: pd.Series) -> dict:
    d = D.assign(g=g)
    out = {}
    for k, x in d.groupby("g"):
        out[int(k)] = {
            "fwd_margin_chg_pp": float(x.fwd_margin_chg_pp.median()),
            "fwd_rev_growth": float(x.fwd_rev_growth.median()),
            "fwd_growth_chg": float(x.fwd_growth_chg.median()),
            "n_with_fwd": int(x.fwd_margin_chg_pp.notna().sum()),
            "median_signal_mcap": float(x.mcap.median()),
        }
    return out


def survivorship(book, D, q, qU, qM, qM50, n, ew) -> dict:
    out = {}
    cnt = pd.DataFrame({"q": q, "missing": D.missing, "year": D.year, "f50": D.missing & (D.pfloat >= 50e6),
                        "univ": D.in_univ}).dropna(subset=["q"])
    by_q = {}
    for k, x in cnt.groupby("q"):
        by_q[int(k)] = {"universe": int(x.univ.sum()), "missing": int(x.missing.sum()),
                        "missing_share": float(x.missing.sum() / (x.univ.sum() + x.missing.sum())),
                        "missing_float50": int(x.f50.sum()),
                        "missing_share_float50": float(x.f50.sum() / (x.univ.sum() + x.f50.sum()))}
    out["by_group"] = by_q
    by_yq = {}
    for (t, k), x in cnt.groupby(["year", "q"]):
        by_yq.setdefault(int(t), {})[int(k)] = {"universe": int(x.univ.sum()), "missing": int(x.missing.sum())}
    out["by_year_group"] = by_yq
    out["missing_share_top"] = by_q[n]["missing_share"] if n in by_q else None
    out["missing_share_bottom"] = by_q[1]["missing_share"] if 1 in by_q else None
    sc = {"a_excluded": spread_stats(ew[n], ew[1])}
    for nm, r in SCEN.items():
        for lab, ml in (("all_missing", qM), ("float50_missing", qM50)):
            e = book.port(qU, scen=r, missing_label=ml)
            sc[f"{nm}_{lab}"] = spread_stats(e[n], e[1])
    out["scenarios_ew_spread"] = sc
    return out


def interaction(Pm, book, univ_ew, iwm, spy, book_raw, book_raw1):
    D = Pm[Pm.FCS.notna() & Pm.accel.notna()].copy()
    f = sort_groups(D, "FCS", 3)
    a = sort_groups(D, "accel", 3)
    cell = (f * 10 + a)            # 11..33, FCS first digit, accel second
    cU, cM = cell[D.in_univ], cell[D.missing]
    cM50 = cell[D.missing & (D.pfloat >= 50e6)]
    ew = book.port(cU)
    vw = book.port(cU, vw=True)
    others = [c for c in ew.columns if c != 33]
    rest = ew[others].mean(axis=1)
    out = {"cells": "FCS tercile (1=low,3=high) x 10 + acceleration tercile",
           "n_firms_per_year": D[D.in_univ].groupby("year").size().to_dict()}
    out["ew_ann"] = {int(k): ann(ew[k]) for k in ew.columns}
    out["vw_ann"] = {int(k): ann(vw[k]) for k in vw.columns}
    out["ew_HH_minus_rest"] = spread_stats(ew[33], rest)
    out["vw_HH_minus_rest"] = spread_stats(vw[33], vw[[c for c in vw.columns if c != 33]].mean(axis=1))
    out["ew_HH_minus_LH"] = spread_stats(ew[33], ew[13])
    er = book_raw.port(cU)
    out["raw_returns_ew_HH_minus_rest"] = spread_stats(er[33], er[[c for c in er.columns if c != 33]].mean(axis=1))
    er1 = book_raw1.port(cU)
    out["raw_returns_minus_largest_month_ew_HH_minus_rest"] = spread_stats(
        er1[33], er1[[c for c in er1.columns if c != 33]].mean(axis=1))
    did = (ew[33] - ew[31]) - (ew[13] - ew[11])
    out["ew_DiD"] = {"mean_monthly_x12": float(did.mean() * 12), "t": tstat(did), "t_nw6": nw_t(did),
                     "n_months": int(did.notna().sum())}
    # industry neutral
    fi = sort_groups(D, "FCS", 3, within="sic2")
    ai = sort_groups(D, "accel", 3, within="sic2")
    ci = (fi * 10 + ai)[D.in_univ]
    ewi = book.port(ci)
    out["ind_neutral_ew_ann"] = {int(k): ann(ewi[k]) for k in ewi.columns}
    out["ind_neutral_ew_HH_minus_rest"] = spread_stats(ewi[33], ewi[[c for c in ewi.columns if c != 33]].mean(axis=1))
    for sz in ("small", "large"):
        Ds = D[D.in_univ & (D["size"] == sz)]
        cs = sort_groups(Ds, "FCS", 3) * 10 + sort_groups(Ds, "accel", 3)
        e = book.port(cs)
        out[f"{sz}_ew_ann"] = {int(k): ann(e[k]) for k in e.columns}
        out[f"{sz}_ew_HH_minus_rest"] = spread_stats(e[33], e[[c for c in e.columns if c != 33]].mean(axis=1))
    out["first_half_ew_HH_minus_rest"] = spread_stats(half(ew, FIRST_HALF)[33], half(rest.to_frame(0), FIRST_HALF)[0])
    out["second_half_ew_HH_minus_rest"] = spread_stats(half(ew, SECOND_HALF)[33], half(rest.to_frame(0), SECOND_HALF)[0])
    out["top_vs"] = top_vs(ew[33] - COST / 12, univ_ew, iwm, spy)
    # fundamental check
    fu = D[D.in_univ].assign(c=cU)
    ft = fund_table(D[D.in_univ], cU)
    out["fundamentals_median_by_cell"] = ft
    hh = fu[fu.c == 33]
    ot = fu[(fu.c != 33) & fu.c.notna()]
    yr = []
    for t in sorted(fu.year.unique()):
        h = hh[hh.year == t].fwd_margin_chg_pp.dropna()
        o = ot[ot.year == t].fwd_margin_chg_pp.dropna()
        if len(h) and len(o):
            yr.append(h.median() - o.median())
    yr = pd.Series(yr)
    med = {k: v["fwd_margin_chg_pp"] for k, v in ft.items()}
    out["fundamental_check"] = {
        "HH_median_fwd_margin_chg_pp": float(hh.fwd_margin_chg_pp.median()),
        "others_median_fwd_margin_chg_pp": float(ot.fwd_margin_chg_pp.median()),
        "HH_minus_others_by_year_mean": float(yr.mean()), "HH_minus_others_by_year_t": tstat(yr),
        "years_HH_above_others": int((yr > 0).sum()), "n_years": int(len(yr)),
        "HH_rank_among_9_cells": int(pd.Series(med).rank(ascending=False)[33]),
        "DiD_fwd_margin_chg_pp": float((med[33] - med[31]) - (med[13] - med[11])),
    }
    # survivorship
    cnt = pd.DataFrame({"c": cell, "missing": D.missing, "univ": D.in_univ,
                        "f50": D.missing & (D.pfloat >= 50e6)}).dropna(subset=["c"])
    by_c = {}
    for k, x in cnt.groupby("c"):
        by_c[int(k)] = {"universe": int(x.univ.sum()), "missing": int(x.missing.sum()),
                        "missing_share": float(x.missing.sum() / (x.univ.sum() + x.missing.sum())),
                        "missing_share_float50": float(x.f50.sum() / (x.univ.sum() + x.f50.sum()))}
    sc = {"a_excluded": out["ew_HH_minus_rest"]}
    for nm, r in SCEN.items():
        for lab, ml in (("all_missing", cM), ("float50_missing", cM50)):
            e = book.port(cU, scen=r, missing_label=ml)
            sc[f"{nm}_{lab}"] = spread_stats(e[33], e[[c for c in e.columns if c != 33]].mean(axis=1))
    out["survivorship"] = {"by_group": by_c, "missing_share_top": by_c[33]["missing_share"],
                           "missing_share_bottom": float(np.mean([v["missing_share"] for k, v in by_c.items() if k != 33])),
                           "scenarios_ew_spread": sc}
    cols = {f"H2b_EW_cell{int(k)}": ew[k] for k in ew.columns}
    cols["H2b_EW_HHmRest"] = ew[33] - rest
    return out, cols


def verdict(r: dict, name: str) -> dict:
    if name == "H2b_FCSxAccel":
        head = r["ew_HH_minus_rest"]
        halves = [r["first_half_ew_HH_minus_rest"], r["second_half_ew_HH_minus_rest"]]
        ind = r["ind_neutral_ew_HH_minus_rest"]
    else:
        head = r["ew_spread"]
        halves = [r["first_half_ew_spread"], r["second_half_ew_spread"]]
        ind = r["ind_neutral_ew_spread"]
    t = head["t"]
    checks = {
        "t_ge_2": bool(t >= 2.0),
        "both_halves_positive": all(h["mean_monthly_x12"] > 0 for h in halves),
        "industry_neutral_positive": bool(ind["mean_monthly_x12"] > 0),
        "all_survivorship_scenarios_positive": all(
            v["mean_monthly_x12"] > 0 for v in r["survivorship"]["scenarios_ew_spread"].values()),
    }
    if name == "H2b_FCSxAccel":
        checks["fundamental_HH_largest_margin_expansion"] = r["fundamental_check"]["HH_rank_among_9_cells"] == 1
    if t <= -2.0:
        v = "No (reversed)"
    elif t < 2.0:
        v = "No"
    elif all(checks.values()):
        v = "Yes"
    else:
        v = "Mixed"
    return {"verdict": v, "checks": checks}


# --------------------------------------------------------------------------- #
# RESULTS.md
# --------------------------------------------------------------------------- #
def pct(x, d=1, sign=False):
    if x is None:
        return "n/a"
    return f"{x*100:+.{d}f}%" if sign else f"{x*100:.{d}f}%"


def write_md(r: dict) -> None:
    from md_writer import render  # kept separate so the prose can be edited without touching the maths
    (HERE / "RESULTS.md").write_text(render(r))


if __name__ == "__main__":
    main()
