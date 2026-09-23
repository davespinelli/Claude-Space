#!/usr/bin/env python3
"""
H5 / H6 pre-registered tests (see ../H5_H6_PREREG.md, including its Deviations
section, which was written before any return below was computed).

Inputs (all read-only):
    quarterly/cache/filings.parquet, snapshot.parquet   (build_quarterly.py)
    ../cache/prices/monthly_long.parquet                  Yahoo monthly prices (annual study's cache)
    ../cache/returns.parquet                              only to verify the return matrix
    ../cache/tickers.parquet, hist_tickers.parquet, subs.parquet, company_tickers.json.gz
    ../panel.parquet                                      only for the historical-ticker clash rule
Outputs:
    quarterly/results_quarterly.json, quarterly/RESULTS_QUARTERLY.md (via md_quarterly.py)

Run:  .venv/bin/python research/oplev/quarterly/run_quarterly.py [--stage signals|all]
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from qcommon import (CACHE, HERE, HIST_FLOAT_BAND, LARGE, LAST_COMPLETE_MONTH, MCAP_MIN, MCAP_RATIO_BAND,
                     OPLEV, REV_MIN, FY_STALE_DAYS)

sys.path.insert(0, str(OPLEV))
from run_tests import ann, clean, clean_returns, nw_t, tstat  # noqa: E402  (read-only reuse)
from build_panel import clean_ticker  # noqa: E402

COST = 0.005
SCEN = {"b_minus30": -0.30, "c_plus15": 0.15}
MIN_BP = 10            # a monthly breakpoint needs at least this many priced filers with the measure
TOP = 0.70             # top 30%


# --------------------------------------------------------------------------- #
# prices and returns
# --------------------------------------------------------------------------- #
def load_prices():
    px = pd.read_parquet(OPLEV / "cache" / "prices" / "monthly_long.parquet")
    px["date"] = pd.to_datetime(px["date"]).dt.to_period("M").dt.to_timestamp()
    px = px.drop_duplicates(["date", "ticker"], keep="last")
    close = px.pivot(index="date", columns="ticker", values="close").sort_index()
    adj = px.pivot(index="date", columns="ticker", values="adj").sort_index()
    adj = adj.where(adj > 0)
    close = close.where(close > 0)
    split = px.pivot(index="date", columns="ticker", values="split").sort_index().fillna(0.0)
    ret = adj / adj.shift(1) - 1
    keep = ret.index <= LAST_COMPLETE_MONTH
    ret, adj, close = ret[keep], adj[keep], close[keep]
    bench = ret[["IWM", "SPY"]].copy()
    R_raw = ret.drop(columns=["IWM", "SPY"])
    R, rinfo = clean_returns(R_raw)
    # verify against the annual study's matrix (same tickers, same months)
    R0 = pd.read_parquet(OPLEV / "cache" / "returns.parquet")
    R0.index = pd.to_datetime(R0.index)
    R0 = R0[R0.index <= LAST_COMPLETE_MONTH].drop(columns=["IWM", "SPY"])
    cc = [c for c in R0.columns if c in R_raw.columns]
    a, b = R_raw.loc[R0.index, cc].to_numpy(), R0[cc].to_numpy()
    same = np.isclose(a, b, equal_nan=True, atol=1e-10)
    rinfo["check_vs_annual_returns_parquet"] = {"n_tickers": len(cc), "share_cells_identical": float(same.mean())}
    recs = {}
    nz = split.stack()
    nz = nz[(nz > 0) & (nz != 1.0)]
    for (m, t), k in nz.items():
        recs.setdefault(t, []).append((m, float(k)))
    first_valid = adj.apply(lambda s: s.first_valid_index())
    last_valid = adj.apply(lambda s: s.last_valid_index())
    return dict(R=R, R_raw=R_raw, bench=bench, close=close, adj=adj, splits=recs,
                first_valid=first_valid, last_valid=last_valid, rinfo=rinfo)


# --------------------------------------------------------------------------- #
# tickers, pricing, universe
# --------------------------------------------------------------------------- #
def ticker_setup():
    tmap = pd.read_parquet(OPLEV / "cache" / "tickers.parquet")
    ct_tk = set(tmap.loc[tmap.ticker_src == "company_tickers", "ticker"])
    tmap = tmap[~((tmap.ticker_src == "submissions") & tmap.ticker.isin(ct_tk))]
    h = pd.read_parquet(OPLEV / "cache" / "hist_tickers.parquet").dropna(subset=["hist_ticker"])
    h = h[~h.index.isin(tmap.index)]
    h = h.rename(columns={"hist_ticker": "ticker"})[["ticker"]].assign(ticker_src="hist")
    tmap = pd.concat([tmap, h])
    with gzip.open(OPLEV / "cache" / "company_tickers.json.gz", "rt") as fh:
        js = json.loads(fh.read())
    holder = {}
    for r in js.values():
        c = clean_ticker(str(r["ticker"]))
        if c and c not in holder:
            holder[c] = int(r["cik_str"])
    P = pd.read_parquet(OPLEV / "panel.parquet", columns=["cik", "year"])
    filers = {int(y): set(g.cik) for y, g in P.groupby("year")}
    return tmap, holder, filers


def form_year(m: pd.Timestamp) -> int:
    return m.year if m.month >= 7 else m.year - 1


def price_month(D: pd.DataFrame, month: pd.Timestamp, PX: dict, holder: dict, filers: dict) -> pd.DataFrame:
    """Universe / missing classification for the rows of one formation month.
    D has cik, ticker, ticker_src, fy_rev, fy_end, assets, pfloat, sh_* columns, T."""
    D = D.copy()
    T = D["T"].iloc[0]
    D["fund_ok"] = (D.fy_rev > REV_MIN) & (D.assets > 0) & ((T - D.fy_end).dt.days <= FY_STALE_DAYS)
    # historical symbol not used while its current holder (another company) is filing
    fy = min(max(form_year(month), min(filers)), max(filers))
    fs = filers[fy]
    ish = D.ticker_src == "hist"
    clash = ish & D.apply(lambda r: isinstance(r.ticker, str) and r.ticker in holder
                          and holder[r.ticker] != r.cik and holder[r.ticker] in fs, axis=1)
    D.loc[clash, ["ticker", "ticker_src"]] = [None, None]
    cand = D[D.fund_ok & D.ticker.notna()]
    dd = cand[cand.ticker.duplicated(keep=False)]
    drop = dd[dd.ticker_src == "hist"].index.tolist()
    rest = dd.drop(index=drop)
    drop += rest[rest.ticker.duplicated(keep=False)].index.tolist()
    D.loc[drop, ["ticker", "ticker_src"]] = [None, None]
    close, adj = PX["close"], PX["adj"]
    tk = D.ticker
    has = tk.isin(adj.columns)
    c_f = pd.Series(np.nan, index=D.index)
    a_f = pd.Series(np.nan, index=D.index)
    if month in adj.index and has.any():
        idx = D.index[has]
        c_f.loc[idx] = close.loc[month, tk[idx]].to_numpy()
        a_f.loc[idx] = adj.loc[month, tk[idx]].to_numpy()
    D["price"] = c_f
    D["priced"] = a_f.notna() & c_f.notna() & (c_f > 0)
    # shares: first source in priority order passing the checks of build_panel.py
    D["mcap"] = np.nan
    D["shares_src"] = None
    base = np.maximum(D.fy_rev.fillna(0), D.assets.fillna(0))
    for i in D.index[D.priced & D.fund_ok]:
        t = tk[i]
        cands = []
        for k in ("dei", "gaap", "wanso"):
            v, bd = D.at[i, f"sh_{k}"], D.at[i, f"sh_{k}_basis"]
            if not (np.isfinite(v) and v > 0) or pd.isna(bd):
                continue
            bm = pd.Timestamp(bd).to_period("M").to_timestamp()
            f = 1.0
            for m, r in PX["splits"].get(t, []):
                if m > bm:
                    f *= r
            cands.append((k, v * f))
        cons = [any(j != a and abs(math.log(c[1] / d[1])) <= math.log(3.0) for j, d in enumerate(cands))
                for a, c in enumerate(cands)]
        anyc = any(cons)
        for a, (k, sb) in enumerate(cands):
            mc = sb * D.at[i, "price"]
            ratio = mc / base[i] if base[i] > 0 else np.nan
            if MCAP_RATIO_BAND[0] <= ratio <= MCAP_RATIO_BAND[1] and (cons[a] or not anyc):
                D.at[i, "mcap"] = mc
                D.at[i, "shares_src"] = k
                break
    fr = D.pfloat / D.mcap
    bad_hist = (D.ticker_src == "hist") & D.priced & ~fr.between(*HIST_FLOAT_BAND)
    D.loc[bad_hist, "priced"] = False
    D.loc[bad_hist, "mcap"] = np.nan
    D["in_univ"] = D.fund_ok & D.priced & (D.mcap >= MCAP_MIN)
    fv = pd.to_datetime(PX["first_valid"].reindex(tk.fillna("")).to_numpy())
    D["not_yet_listed"] = D.fund_ok & ~D.priced & has & (pd.Series(fv, index=D.index) > month)
    D["missing"] = D.fund_ok & ~D.priced & ~D.not_yet_listed
    D["priced_no_shares"] = D.fund_ok & D.priced & D.mcap.isna()
    D["size"] = np.where(D.mcap >= LARGE, "large", np.where(D.mcap.notna(), "small", None))
    return D


def build_cohorts(PX, stage_log):
    tmap, holder, filers = ticker_setup()
    subs = pd.read_parquet(OPLEV / "cache" / "subs.parquet")
    F = pd.read_parquet(CACHE / "filings.parquet")
    F = F[(F.fm >= pd.Timestamp("2009-01-01")) & (F.fm < LAST_COMPLETE_MONTH)]
    F = F.sort_values(["cik", "fm", "period_end", "filed"]).drop_duplicates(["cik", "fm"], keep="last")
    F = F.join(tmap, on="cik").join(subs[["sic"]], on="cik")
    F["sic2"] = F.sic // 100
    S = pd.read_parquet(CACHE / "snapshot.parquet")
    S = S.join(tmap, on="cik").join(subs[["sic"]], on="cik")
    S["fm"] = pd.to_datetime(S.year.astype(str) + "-06-01")
    S = S[S.fm <= LAST_COMPLETE_MONTH]
    out = []
    for m, g in F.groupby("fm"):
        out.append(price_month(g, m, PX, holder, filers))
    C = pd.concat(out)
    snaps = []
    for m, g in S.groupby("fm"):
        snaps.append(price_month(g, m, PX, holder, filers))
    S = pd.concat(snaps)
    # FCS breakpoints: 70th percentile of the June universe of formation year t,
    # applied to formation months July t .. June t+1
    su = S[S.in_univ & S.fcs.notna()]
    fcs_bp = su.groupby("year").fcs.quantile(TOP)
    stage_log["fcs_breakpoints"] = {int(k): float(v) for k, v in fcs_bp.items()}
    stage_log["fcs_universe_n"] = su.groupby("year").size().astype(int).to_dict()
    stage_log["june_universe_n"] = S[S.in_univ].groupby("year").size().astype(int).to_dict()
    C["fyear"] = C.fm.map(form_year)
    C["fcs_bp"] = C.fyear.map(fcs_bp)
    C["fcs_top"] = C.fcs > C.fcs_bp
    # H5 signal
    C["accel_bp"] = np.nan
    C["gap_bp"] = np.nan
    for m, g in C.groupby("fm"):
        u = g[g.in_univ & g.accel.notna()]
        if len(u) >= MIN_BP:
            C.loc[g.index, "accel_bp"] = np.nanquantile(u.accel, TOP)
        u = g[g.in_univ & g.rpo.notna() & g.gap.notna()]
        if len(u) >= MIN_BP:
            C.loc[g.index, "gap_bp"] = np.nanquantile(u.gap, TOP)
    C["sig5"] = C.fcs_top & (C.accel > C.accel_bp) & (C.accel > 0)
    C["rpo_rep"] = C.rpo.notna()
    C["sig6"] = C.rpo_rep & C.fcs_top & (C.gap > C.gap_bp) & (C.gap > 0)
    # evaluable (extra, not pre-registered): signal could be computed at all
    C["eval5"] = C.fcs.notna() & C.fcs_bp.notna() & C.accel.notna() & C.accel_bp.notna()
    C["eval6"] = C.rpo_rep & C.fcs.notna() & C.fcs_bp.notna() & C.gap.notna() & C.gap_bp.notna()
    return C.reset_index(drop=True), S


# --------------------------------------------------------------------------- #
# portfolios
# --------------------------------------------------------------------------- #
class Holdings:
    """Long table: one row per (cohort row, held month) for K up to 6."""

    def __init__(self, C: pd.DataFrame, R: pd.DataFrame, PX: dict, kmax: int = 6):
        rows = []
        months = R.index
        pos = {m: i for i, m in enumerate(months)}
        Cp = C[C.in_univ].copy()
        for m, g in Cp.groupby("fm"):
            if m not in pos:
                continue
            i0 = pos[m]
            hm = months[i0 + 1: i0 + 1 + kmax]
            if not len(hm):
                continue
            tk = g.ticker
            sub = R.loc[hm, tk.to_numpy()]
            sub.columns = g.index
            lg = sub.stack(future_stack=True).rename("ret").reset_index()
            lg.columns = ["month", "row", "ret"]
            lg["h"] = lg.month.map(pos) - i0
            rows.append(lg)
        H = pd.concat(rows, ignore_index=True)
        H["fm"] = H.row.map(C.fm)
        H = H.sort_values(["row", "month"])
        g = (1 + H.ret.fillna(0.0)).groupby(H.row).cumprod()
        H["w"] = H.row.map(C.mcap) * g.groupby(H.row).shift(1).fillna(1.0)
        # delisting: series stops before the end of the hold
        lv = PX["last_valid"]
        self.last_valid = C.ticker.map(lambda t: lv.get(t, pd.NaT) if isinstance(t, str) else pd.NaT)
        self.H_all = H
        self.H = H.dropna(subset=["ret"])
        self.C = C
        self.months = months
        self.pos = pos

    def extra(self, rows: pd.Index, K: int, s: float, missing_rows: pd.Index) -> pd.DataFrame:
        """Scenario rows: delisting return s in the month after the last held month,
        and (1+s)^(1/12)-1 a month for missing companies."""
        C = self.C
        out = []
        H = self.H[self.H.row.isin(rows) & (self.H.h <= K)]
        last_h = H.groupby("row").month.max()
        for r in rows:
            m0 = C.at[r, "fm"]
            if m0 not in self.pos:
                continue
            i0 = self.pos[m0]
            end_i = min(i0 + K, len(self.months) - 1)
            lv = self.last_valid.get(r, pd.NaT)
            if pd.isna(lv) or lv >= self.months[end_i]:
                continue
            lm = last_h.get(r, m0)
            j = self.pos.get(lm, i0) + 1
            if j <= end_i and j <= len(self.months) - 1:
                out.append((r, self.months[j], s, j - i0))
        mr = (1 + s) ** (1 / 12) - 1
        for r in missing_rows:
            m0 = C.at[r, "fm"]
            if m0 not in self.pos:
                continue
            i0 = self.pos[m0]
            for h in range(1, K + 1):
                if i0 + h < len(self.months):
                    out.append((r, self.months[i0 + h], mr, h))
        return pd.DataFrame(out, columns=["row", "month", "ret", "h"])

    def port(self, groups: dict[str, pd.Index], K: int = 3, vw: bool = False, scen: float | None = None,
             missing: dict[str, pd.Index] | None = None, raw: pd.DataFrame | None = None) -> pd.DataFrame:
        """Jegadeesh-Titman monthly returns: each month the average of the cohorts formed in
        the previous K months; each cohort equal- (or value-) weighted within itself."""
        cols = {}
        for name, rows in groups.items():
            H = self.H if raw is None else raw
            H = H[H.row.isin(rows) & (H.h <= K)][["row", "month", "ret", "h", "w"]]
            if scen is not None and not vw:
                e = self.extra(rows, K, scen, (missing or {}).get(name, pd.Index([])))
                if len(e):
                    H = pd.concat([H[["row", "month", "ret", "h"]], e], ignore_index=True)
            H = H.assign(fm=H.row.map(self.C.fm))
            if vw:
                H = H.assign(wr=H.w * H.ret)
                s = H.groupby(["fm", "month"])[["wr", "w"]].sum()
                coh = (s.wr / s.w).rename("r").reset_index()
            else:
                coh = H.groupby(["fm", "month"]).ret.mean().rename("r").reset_index()
            cols[name] = coh.groupby("month").r.mean()
        return pd.DataFrame(cols).sort_index()

    def matched(self, sig: pd.Index, ctl: pd.Index, K: int = 3) -> pd.DataFrame:
        """Signal stock vs control stocks in the same size tercile x 2-digit SIC cell of its cohort."""
        C = self.C
        rows = sig.union(ctl)
        cell = pd.Series(index=rows, dtype=object)
        for m, g in C.loc[rows].groupby("fm"):
            bp = np.nanquantile(g.mcap.to_numpy(float), [1 / 3, 2 / 3])
            terc = 1 + (g.mcap.to_numpy(float)[:, None] > bp[None, :]).sum(axis=1)
            cell.loc[g.index] = [f"{m.date()}|{t}|{s}" for t, s in zip(terc, g.sic2)]
        H = self.H[self.H.row.isin(rows) & (self.H.h <= K)][["row", "month", "ret"]].copy()
        H["cell"] = H.row.map(cell)
        H["fm"] = H.row.map(C.fm)
        H["is_sig"] = H.row.isin(sig)
        cm = H[~H.is_sig].groupby(["cell", "month"]).ret.mean().rename("cret")
        S = H[H.is_sig].join(cm, on=["cell", "month"]).dropna(subset=["cret"])
        coh = S.groupby(["fm", "month"])[["ret", "cret"]].mean().reset_index()
        out = coh.groupby("month")[["ret", "cret"]].mean()
        out.columns = ["sig", "ctl"]
        n_matched = int(S.row.nunique())
        return out, n_matched


# --------------------------------------------------------------------------- #
# statistics
# --------------------------------------------------------------------------- #
def sstats(top: pd.Series, bot: pd.Series) -> dict:
    s = (top - bot).dropna()
    if len(s) < 3:
        return {"n_months": int(len(s))}
    t_, b_ = top.loc[s.index], bot.loc[s.index]
    by_year = {}
    for y in sorted(set(s.index.year)):
        ms = s.index[s.index.year == y]
        by_year[int(y)] = float((1 + t_.loc[ms]).prod() - (1 + b_.loc[ms]).prod())
    return {
        "ann_top": ann(t_), "ann_bottom": ann(b_), "ann_diff": ann(t_) - ann(b_),
        "mean_monthly_x12": float(s.mean() * 12), "t": tstat(s), "t_nw6": nw_t(s, 6),
        "n_months": int(len(s)), "first_month": str(s.index.min().date()), "last_month": str(s.index.max().date()),
        "years_positive": int(sum(v > 0 for v in by_year.values())), "n_years": len(by_year),
        "by_year": by_year,
    }


def halves(top, bot):
    s = (top - bot).dropna()
    n = len(s) // 2
    a, b = s.index[:n], s.index[n:]
    return sstats(top.loc[a], bot.loc[a]), sstats(top.loc[b], bot.loc[b])


def top_vs(top, univ, bench):
    out = {}
    for nm, b in (("univ_ew", univ), ("iwm", bench["IWM"]), ("spy", bench["SPY"])):
        d = (top - b).dropna()
        out[nm] = {"ann_top_net": ann(top.loc[d.index]), "ann_bench": ann(b.loc[d.index]),
                   "ann_excess": ann(top.loc[d.index]) - ann(b.loc[d.index]), "t": tstat(d), "t_nw6": nw_t(d),
                   "n_months": int(len(d))}
    return out


def fund_check(C: pd.DataFrame, sig: pd.Index, ctl: pd.Index) -> dict:
    d = C.loc[sig.union(ctl)].assign(g=lambda x: np.where(x.index.isin(sig), "signal", "control"))
    tab = {}
    for g, x in d.groupby("g"):
        tab[g] = {"fwd_margin_chg_pp_median": float(x.fwd_margin_chg_pp.median()),
                  "fwd_rev_growth_median": float(x.fwd_rev_growth.median()),
                  "fwd_growth_chg_median": float(x.fwd_growth_chg.median()),
                  "cur_rev_growth_median": float(x.g0.median()),
                  "n": int(len(x)), "n_with_fwd": int(x.fwd_margin_chg_pp.notna().sum())}
    yr = {}
    for y, x in d.groupby(d.fm.dt.year):
        a = x[x.g == "signal"].fwd_margin_chg_pp.dropna()
        b = x[x.g == "control"].fwd_margin_chg_pp.dropna()
        if len(a) and len(b):
            yr[int(y)] = float(a.median() - b.median())
    ys = pd.Series(yr)
    diff = tab.get("signal", {}).get("fwd_margin_chg_pp_median", np.nan) - \
        tab.get("control", {}).get("fwd_margin_chg_pp_median", np.nan)
    return {"table": tab, "signal_minus_control_median_pp": float(diff),
            "by_year": yr, "by_year_mean": float(ys.mean()) if len(ys) else None,
            "by_year_t": tstat(ys) if len(ys) >= 3 else None,
            "years_signal_above": int((ys > 0).sum()), "n_years": int(len(ys)),
            "mechanism_present": bool(diff > 0)}


# --------------------------------------------------------------------------- #
# one test
# --------------------------------------------------------------------------- #
def run_test(name: str, C: pd.DataFrame, HD: Holdings, HD_raw: Holdings, PX: dict, univ: pd.Series,
             sig_col: str, sample: pd.Series, eval_col: str) -> dict:
    U = C.in_univ
    sig = C.index[U & sample & C[sig_col]]
    ctl = C.index[U & sample & ~C[sig_col]]
    msig = C.index[C.missing & sample & C[sig_col]]
    mctl = C.index[C.missing & sample & ~C[sig_col]]
    f50 = C.pfloat >= MCAP_MIN
    out = {"n_signal_filings": int(len(sig)), "n_control_filings": int(len(ctl))}
    ew = HD.port({"sig": sig, "ctl": ctl}, K=3)
    head = sstats(ew.sig, ew.ctl)
    out["ew"] = head
    out["verdict"] = "Yes" if head.get("t_nw6", -9) >= 2.0 else "No"
    h1, h2 = halves(ew.sig, ew.ctl)
    out["first_half"], out["second_half"] = h1, h2
    for sz in ("small", "large"):
        e = HD.port({"sig": sig[C.loc[sig, "size"] == sz], "ctl": ctl[C.loc[ctl, "size"] == sz]}, K=3)
        out[f"{sz}_ew"] = sstats(e.sig, e.ctl)
    mt, nm = HD.matched(sig, ctl, K=3)
    out["matched_size_sic2"] = sstats(mt.sig, mt.ctl)
    out["matched_size_sic2"]["n_signal_filings_matched"] = nm
    vw = HD.port({"sig": sig, "ctl": ctl}, K=3, vw=True)
    out["vw"] = sstats(vw.sig, vw.ctl)
    for K in (1, 6):
        e = HD.port({"sig": sig, "ctl": ctl}, K=K)
        out[f"hold_{K}m_ew"] = sstats(e.sig, e.ctl)
    er = HD_raw.port({"sig": sig, "ctl": ctl}, K=3)
    out["raw_returns_ew"] = sstats(er.sig, er.ctl)
    ctl_e = ctl[C.loc[ctl, eval_col]]
    e = HD.port({"sig": sig, "ctl": ctl_e}, K=3)
    out["extra_control_evaluable_only"] = sstats(e.sig, e.ctl)
    out["top_vs"] = top_vs(ew.sig - COST / 12, univ, PX["bench"])
    # survivorship
    sc = {"a_excluded": head}
    for nm_, s in SCEN.items():
        for lab, ms, mc in (("all_missing", msig, mctl), ("float50_missing", msig[f50[msig]], mctl[f50[mctl]])):
            e = HD.port({"sig": sig, "ctl": ctl}, K=3, scen=s, missing={"sig": ms, "ctl": mc})
            sc[f"{nm_}_{lab}"] = sstats(e.sig, e.ctl)
    out["survivorship"] = {
        "missing_share_signal": float(len(msig) / (len(msig) + len(sig))) if len(sig) else None,
        "missing_share_control": float(len(mctl) / (len(mctl) + len(ctl))) if len(ctl) else None,
        "missing_share_signal_float50": float(f50[msig].sum() / (f50[msig].sum() + len(sig))) if len(sig) else None,
        "missing_share_control_float50": float(f50[mctl].sum() / (f50[mctl].sum() + len(ctl))) if len(ctl) else None,
        "n_missing_signal": int(len(msig)), "n_missing_control": int(len(mctl)),
        "scenarios_ew": sc}
    # counts
    held = HD.H[HD.H.row.isin(sig) & (HD.H.h <= 3)]
    per_month = held.groupby("month").row.apply(lambda r: C.loc[r, "cik"].nunique())
    per_cohort = C.loc[sig].groupby("fm").size()
    ctl_month = HD.H[HD.H.row.isin(ctl) & (HD.H.h <= 3)].groupby("month").row.apply(
        lambda r: C.loc[r, "cik"].nunique())
    months = ew.dropna().index
    pm = per_month.reindex(months).fillna(0)
    out["counts"] = {
        "signal_held_per_month": {str(k.date()): int(v) for k, v in pm.items()},
        "signal_held_median": float(pm.median()), "signal_held_min": int(pm.min()), "signal_held_max": int(pm.max()),
        "months_with_fewer_than_30_signal_held": int((pm < 30).sum()), "n_months": int(len(pm)),
        "signal_new_per_cohort": {str(k.date()): int(v) for k, v in per_cohort.items()},
        "control_held_median": float(ctl_month.reindex(months).median()),
        "signal_distinct_companies": int(C.loc[sig, "cik"].nunique()),
    }
    out["fundamental_check"] = fund_check(C, sig, ctl)
    out["_series"] = ew
    return out


def coverage(C: pd.DataFrame) -> dict:
    out = {}
    for y, g in C.groupby(C.fm.dt.year):
        fo = g[g.fund_ok]
        out[int(y)] = {
            "filer_months_fund_ok": int(len(fo)), "universe": int(g.in_univ.sum()),
            "missing": int(g.missing.sum()), "missing_float50": int((g.missing & (g.pfloat >= MCAP_MIN)).sum()),
            "not_yet_listed": int(g.not_yet_listed.sum()), "priced_no_shares": int(g.priced_no_shares.sum()),
            "priced_below_50m": int((fo.priced & (fo.mcap < MCAP_MIN)).sum()),
            "universe_with_accel": int((g.in_univ & g.accel.notna()).sum()),
            "universe_with_fcs": int((g.in_univ & g.fcs.notna()).sum()),
            "universe_rpo_reporters": int((g.in_univ & g.rpo_rep).sum()),
            "universe_rpo_distinct_companies": int(g[g.in_univ & g.rpo_rep].cik.nunique()),
            "all_rpo_distinct_companies": int(g[g.fund_ok & g.rpo_rep].cik.nunique()),
            "universe_with_gap": int((g.in_univ & g.gap.notna()).sum()),
            "signal_H5": int((g.in_univ & g.sig5).sum()), "signal_H6": int((g.in_univ & g.sig6).sum()),
        }
        c = out[int(y)]
        c["missing_share"] = c["missing"] / (c["universe"] + c["missing"]) if c["universe"] + c["missing"] else None
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["signals", "all"])
    a = ap.parse_args(argv)
    PX = load_prices()
    res = {"meta": {"returns_through": str(LAST_COMPLETE_MONTH.date()), "price_error_rule": PX["rinfo"]}}
    C, S = build_cohorts(PX, res["meta"])
    res["coverage_by_calendar_year"] = coverage(C)
    bl = CACHE / "build_log.json"
    if bl.exists():
        res["build"] = json.loads(bl.read_text())
    if a.stage == "signals":
        print(json.dumps(clean({k: v for k, v in res.items()}), indent=1, default=str)[:6000])
        C.to_parquet(CACHE / "cohorts.parquet", index=False)
        return
    HD = Holdings(C, PX["R"], PX)
    HD_raw = Holdings(C, PX["R_raw"], PX)
    allu = C.index[C.in_univ]
    univ = HD.port({"u": allu}, K=3).u
    res["benchmarks"] = {"UNIV_EW_JT3_ann": ann(univ), "IWM_ann": ann(PX["bench"].IWM.reindex(univ.index)),
                         "SPY_ann": ann(PX["bench"].SPY.reindex(univ.index)),
                         "first_month": str(univ.index.min().date()), "last_month": str(univ.index.max().date())}
    everyone = pd.Series(True, index=C.index)
    res["H5"] = run_test("H5", C, HD, HD_raw, PX, univ, "sig5", everyone, "eval5")
    res["H6"] = run_test("H6", C, HD, HD_raw, PX, univ, "sig6", C.rpo_rep, "eval6")
    series = {}
    for k in ("H5", "H6"):
        s = res[k].pop("_series")
        series[f"{k}_signal"] = s.sig
        series[f"{k}_control"] = s.ctl
    series["UNIV_EW_JT3"] = univ
    pd.DataFrame(series).to_csv(HERE / "monthly_returns_quarterly.csv", float_format="%.6f")
    C.to_parquet(CACHE / "cohorts.parquet", index=False)
    (HERE / "results_quarterly.json").write_text(json.dumps(clean(res), indent=1, default=str))
    try:
        from md_quarterly import render
    except ImportError:
        render = None
    if render:
        (HERE / "RESULTS_QUARTERLY.md").write_text(render(json.loads((HERE / "results_quarterly.json").read_text())))
    for k in ("H5", "H6"):
        e = res[k]["ew"]
        print(f"{k}: {res[k]['verdict']}  sig {e['ann_top']:.4f} ctl {e['ann_bottom']:.4f} "
              f"diff {e['ann_diff']:+.4f}  NW t {e['t_nw6']:+.2f}  t {e['t']:+.2f}  "
              f"years {e['years_positive']}/{e['n_years']}")


if __name__ == "__main__":
    main()
