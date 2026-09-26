#!/usr/bin/env python3
"""
INFO-1 step 4: the pre-registered monthly customer-momentum test.

Reads data/links.csv, data/filings.csv, data/suppliers.csv (build_links.py), Yahoo monthly
prices (prices.py: oplev cache + ours), research/oplev/panel.parquet (market caps, SIC
and the size-and-industry benchmark universe), and writes
  results.json               every number
  data/monthly_spreads.csv   monthly quintile returns and spreads
  data/panel_supplier_months.csv.gz   one row per supplier x formation month

Definitions (PREREG.md, including Deviations, fixed before this file first ran):
  formation date   last business day of month t, t = 2010-01 .. 2026-07
  active filing    the supplier's latest original 10-K filed strictly before the
                   formation date and at most 15 months before it
  links            listed customers named at >= 10% in that filing (links.csv)
  signal           equal-weighted mean month-t return of the distinct linked customer
                   tickers that have a listed price series that month
  ranked set       suppliers with a signal and a Yahoo price at the end of month t
  quintiles        breakpoints = 20/40/60/80th percentiles of the signal across the
                   ranked set (a value on a breakpoint goes to the lower group); months
                   with fewer than 25 ranked suppliers are skipped
  return           supplier month-(t+1) total return minus its size-and-industry
                   benchmark (EW return of research/oplev universe firms in the same
                   June size quintile x Fama-French-12 industry, the supplier itself
                   excluded, >= 5 firms); fallback IWM (< $2B or unknown) / SPY
  spread           EW top fifth minus EW bottom fifth, month t+1, less 0.5%/12 a month
  primary          NW(6) t >= 2.5 on the net spread and positive in both halves
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OPLEV = HERE.parents[1] / "oplev"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(OPLEV))
import prices  # noqa: E402
from run_tests import clean_returns, nw_t, tstat, ann  # noqa: E402  (research/oplev, read-only)

DATA = HERE / "data"
COST_M = 0.005 / 12
FIRST_FORM = pd.Timestamp("2010-01-01")
LAST_FORM = pd.Timestamp("2026-07-01")     # holding month 2026-08 is the last complete month
MAX_AGE_DAYS = 456                          # 15 months
MIN_RANKED = 25
SCEN = {"b_minus30": -0.30, "c_plus15": 0.15}


def ff12(sic) -> str:
    try:
        s = int(sic)
    except (TypeError, ValueError):
        return "Unknown"
    r = lambda a, b: a <= s <= b  # noqa: E731
    if r(100, 999) or r(2000, 2399) or r(2700, 2749) or r(2770, 2799) or r(3100, 3199) or r(3940, 3989):
        return "NoDur"
    if r(2500, 2519) or r(2590, 2599) or r(3630, 3659) or r(3710, 3711) or s == 3714 or s == 3716 or \
            r(3750, 3751) or s == 3792 or r(3900, 3939) or r(3990, 3999):
        return "Durbl"
    if r(2520, 2589) or r(2600, 2699) or r(2750, 2769) or r(3000, 3099) or r(3200, 3569) or r(3580, 3629) or \
            r(3700, 3709) or r(3712, 3713) or s == 3715 or r(3717, 3749) or r(3752, 3791) or r(3793, 3799) or \
            r(3830, 3839) or r(3860, 3899):
        return "Manuf"
    if r(1200, 1399) or r(2900, 2999):
        return "Enrgy"
    if r(2800, 2829) or r(2840, 2899):
        return "Chems"
    if r(3570, 3579) or r(3660, 3692) or r(3694, 3699) or r(3810, 3829) or r(7370, 7379):
        return "BusEq"
    if r(4800, 4899):
        return "Telcm"
    if r(4900, 4949):
        return "Utils"
    if r(5000, 5999) or r(7200, 7299) or r(7600, 7699):
        return "Shops"
    if r(2830, 2839) or s == 3693 or r(3840, 3859) or r(8000, 8099):
        return "Hlth"
    if r(6000, 6999):
        return "Money"
    return "Other"


def month_end_bday(m: pd.Timestamp) -> pd.Timestamp:
    """Last weekday of the month that starts at m (holidays ignored)."""
    return pd.offsets.BMonthEnd().rollforward(m)


def formation_year(m: pd.Timestamp) -> int:
    """oplev formation year whose July..June holding window contains month m."""
    return m.year if m.month >= 7 else m.year - 1


# --------------------------------------------------------------------------- inputs
def load_inputs():
    L = pd.read_csv(DATA / "links.csv", parse_dates=["file_date"])
    F = pd.read_csv(DATA / "filings.csv", parse_dates=["date"])
    S = pd.read_csv(DATA / "suppliers.csv")
    # every link filing must be in the filing list (full-index); add any the index missed
    lf = L.drop_duplicates("adsh")[["supplier_cik", "adsh", "file_date"]].rename(
        columns={"supplier_cik": "cik", "file_date": "date"})
    add = lf[~lf.adsh.isin(F.adsh)]
    F = pd.concat([F[["cik", "adsh", "date"]], add], ignore_index=True).drop_duplicates("adsh")
    return L, F, S


def active_filings(F: pd.DataFrame, months: list) -> pd.DataFrame:
    """(cik, month) -> adsh of the latest 10-K filed strictly before the formation date."""
    out = []
    F = F.sort_values(["cik", "date"])
    for cik, g in F.groupby("cik"):
        d = g.date.to_numpy()
        a = g.adsh.to_numpy()
        for m in months:
            fd = np.datetime64(month_end_bday(m))
            k = np.searchsorted(d, fd, side="left") - 1   # strictly before
            if k < 0:
                continue
            age = (fd - d[k]).astype("timedelta64[D]").astype(int)
            if age <= MAX_AGE_DAYS:
                out.append((cik, m, a[k], pd.Timestamp(d[k])))
    return pd.DataFrame(out, columns=["cik", "month", "adsh", "filed"])


def customer_return(ret: pd.DataFrame, windows_json: str, m: pd.Timestamp):
    for tk, a, b in json.loads(windows_json):
        if a is not None and m < pd.Timestamp(a):
            continue
        if b is not None and m > pd.Timestamp(b):
            continue
        if tk in ret.columns:
            v = ret.at[m, tk] if m in ret.index else np.nan
            return tk, v
        return tk, np.nan
    return None, np.nan


# --------------------------------------------------------------------------- market caps
def mcap_table(P: pd.DataFrame, close: pd.DataFrame, ciks: set, tick: dict, months: list) -> pd.DataFrame:
    """Supplier market cap at the end of each month: oplev June market cap (validated share
    count x June close) rolled with the split-adjusted close; the June t value serves
    July t .. June t+1, and June 2011 serves 2010-01 .. 2011-06."""
    Pm = P[P.cik.isin(ciks) & P.mcap.notna() & P.priced].copy()
    rows = []
    for cik, g in Pm.groupby("cik"):
        tk = tick.get(cik)
        if tk is None or tk not in close.columns:
            continue
        g = g.set_index("year")
        c = close[tk]
        for m in months:
            fy = max(formation_year(m), 2011)
            if fy not in g.index:
                continue
            jm = pd.Timestamp(fy, 6, 1)
            if g.at[fy, "ticker"] != tk or jm not in c.index or not np.isfinite(c.get(jm, np.nan)):
                continue
            cm = c.get(m, np.nan)
            if np.isfinite(cm):
                rows.append((cik, m, g.at[fy, "mcap"] * cm / c[jm], g.at[fy, "mcap"]))
    return pd.DataFrame(rows, columns=["cik", "month", "mcap", "mcap_june"])


# --------------------------------------------------------------------------- benchmark
class Benchmark:
    def __init__(self, P: pd.DataFrame, R: pd.DataFrame, bench: pd.DataFrame):
        self.R, self.bench = R, bench
        U = P[P.in_univ & P.ticker.isin(R.columns)].copy()
        U["ind"] = U.sic.map(ff12)
        U["szq"] = np.nan
        self.bps = {}
        for t, g in U.groupby("year"):
            bp = np.nanquantile(g.mcap.to_numpy(float), [0.2, 0.4, 0.6, 0.8])
            self.bps[t] = bp
            U.loc[g.index, "szq"] = 1 + (g.mcap.to_numpy(float)[:, None] > bp[None, :]).sum(axis=1)
        self.U = U
        # cell sums and counts per holding month
        rows = []
        for t, g in U.groupby("year"):
            months = [m for m in pd.date_range(pd.Timestamp(t, 7, 1), pd.Timestamp(t + 1, 6, 1), freq="MS")
                      if m in R.index]
            sub = R.loc[months, g.ticker.unique()]
            lg = sub.stack().rename("ret").reset_index()
            lg.columns = ["month", "ticker", "ret"]
            lg = lg.merge(g[["ticker", "cik", "szq", "ind"]].drop_duplicates("ticker"), on="ticker")
            rows.append(lg)
        self.H = pd.concat(rows, ignore_index=True)
        c = self.H.groupby(["month", "szq", "ind"]).ret.agg(["sum", "count"])
        self.cell = {k: (v["sum"], v["count"]) for k, v in c.iterrows()}
        self.own = self.H.drop_duplicates(["month", "cik"]).set_index(["month", "cik"]).ret.to_dict()

    def size_q(self, fy: int, mcap_june: float):
        bp = self.bps.get(fy)
        if bp is None or not np.isfinite(mcap_june):
            return np.nan
        return 1 + int((mcap_june > bp).sum())

    def get(self, m, cik, fy, mcap_june, mcap_now, ind):
        """(benchmark return in month m, source)"""
        q = self.size_q(fy, mcap_june)
        if np.isfinite(q) and ind not in ("Unknown", "Money", "Utils"):
            key = (m, float(q), ind)
            if key in self.cell:
                s, n = self.cell[key]
                own = self.own.get((m, cik), np.nan)
                if np.isfinite(own):
                    s, n = s - own, n - 1
                if n >= 5:
                    return s / n, "cell"
        small = (not np.isfinite(mcap_now)) or mcap_now < 2e9
        return self.bench.at[m, "IWM" if small else "SPY"], ("IWM" if small else "SPY")


# --------------------------------------------------------------------------- portfolio maths
def breakpoints(x: np.ndarray, n=5):
    return np.nanquantile(x, [k / n for k in range(1, n)])


def bucket(x, bp):
    return 1 + (np.asarray(x, float)[:, None] > bp[None, :]).sum(axis=1)


def spread_stats(s: pd.Series, top: pd.Series | None = None, bot: pd.Series | None = None) -> dict:
    s = s.dropna()
    out = {"n_months": int(len(s)), "mean_monthly": float(s.mean()) if len(s) else None,
           "mean_x12": float(s.mean() * 12) if len(s) else None, "t_nw6": nw_t(s), "t": tstat(s),
           "ann_compound": ann(s), "share_months_positive": float((s > 0).mean()) if len(s) else None}
    yrs = s.groupby(s.index.year).apply(lambda x: (1 + x).prod() - 1)
    out["years_positive"] = int((yrs > 0).sum())
    out["n_years"] = int(len(yrs))
    out["by_year"] = {int(k): float(v) for k, v in yrs.items()}
    return out


def run_sort(D: pd.DataFrame, col: str, weight: str | None = None, scen: float | None = None) -> pd.DataFrame:
    """D: supplier-month rows with 'q' (1..5), 'hold' month, return column `col`.
    Scenario rows (missing suppliers / ended series) carry col = NaN and flags."""
    X = D.copy()
    if scen is not None:
        mr = (1 + scen) ** (1 / 12) - 1
        X.loc[X.missing, col] = mr
        X.loc[X.ended, col] = scen
    X = X[X[col].notna() & X.q.notna()]
    if weight:
        X = X[X[weight].notna() & (X[weight] > 0)]
        X["wr"] = X[col] * X[weight]
        s = X.groupby(["hold", "q"])[["wr", weight]].sum()
        out = (s.wr / s[weight]).unstack("q")
    else:
        out = X.groupby(["hold", "q"])[col].mean().unstack("q")
    return out.sort_index()


def main():
    L, F, S = load_inputs()
    months = list(pd.date_range(FIRST_FORM, LAST_FORM, freq="MS"))
    res = {"meta": {"formation_months": f"{months[0]:%Y-%m} .. {months[-1]:%Y-%m}",
                    "holding_months": f"{months[0] + pd.offsets.MonthBegin(1):%Y-%m} .. "
                                      f"{months[-1] + pd.offsets.MonthBegin(1):%Y-%m}"}}
    # ---------------- prices
    tick = S.dropna(subset=["ticker"]).set_index("supplier_cik").ticker.to_dict()
    cust_t = set()
    for w in L.cust_windows.unique():
        for tk, a, b in json.loads(w):
            cust_t.add(tk)
    P = pd.read_parquet(OPLEV / "panel.parquet")
    univ_t = set(P.loc[P.in_univ, "ticker"].dropna())
    need = sorted(set(tick.values()) | cust_t | univ_t | {"IWM", "SPY"})
    res["meta"]["yahoo_fetch"] = prices.ensure(need)
    px = prices.load(need)
    ret_raw, close = prices.monthly_returns(px)
    bench = ret_raw[["IWM", "SPY"]]
    R, rinfo = clean_returns(ret_raw.drop(columns=["IWM", "SPY"]))
    res["meta"]["price_error_rule"] = rinfo
    last_px = ret_raw.index.max()
    res["meta"]["last_price_month"] = str(last_px.date())

    # ---------------- supplier x formation month
    act = active_filings(F, months)
    act = act[act.cik.isin(L.supplier_cik.unique())]
    LL = L[["adsh", "cid", "cust_ticker", "cust_windows", "pct"]]
    X = act.merge(LL, on="adsh", how="inner")          # latest filing named >= 1 alias customer
    rows = []
    cr_cache = {}
    for r in X.itertuples(index=False):
        key = (r.cust_windows, r.month)
        if key not in cr_cache:
            cr_cache[key] = customer_return(ret_raw, r.cust_windows, r.month)
        tk, v = cr_cache[key]
        rows.append((r.cik, r.month, r.adsh, r.filed, r.cid, tk, r.pct, v))
    LM = pd.DataFrame(rows, columns=["cik", "month", "adsh", "filed", "cid", "cust_tk", "pct", "cust_ret"])
    LM["cust_listed"] = LM.cust_tk.notna() & LM.cust_ret.notna()
    res["links_monthly"] = {
        "supplier_link_months": int(len(LM)),
        "with_listed_priced_customer": int(LM.cust_listed.sum()),
        "customer_not_listed_or_no_price_by_cid": LM[~LM.cust_listed].cid.value_counts().head(25).to_dict(),
    }
    LM.to_csv(DATA / "link_months.csv.gz", index=False)

    def signal(lm):
        g = lm[lm.cust_listed].drop_duplicates(["cik", "month", "cust_tk"])
        return g.groupby(["cik", "month"]).agg(signal=("cust_ret", "mean"), n_cust=("cust_tk", "nunique"),
                                               max_pct=("pct", "max")).reset_index()
    SIG = signal(LM)
    SIG20 = signal(LM[LM.pct >= 20])

    # ---------------- supplier attributes per month
    mc = mcap_table(P, close, set(SIG.cik), tick, months)
    sic = S.set_index("supplier_cik").sic.to_dict()
    psic = P.sort_values("year").drop_duplicates("cik", keep="last").set_index("cik").sic.to_dict()
    B = Benchmark(P, R, bench)
    Pj = P[P.mcap.notna() & P.priced]
    junecap = dict(zip(zip(Pj.cik, Pj.year), Pj.mcap))

    def attach(sig: pd.DataFrame) -> pd.DataFrame:
        D = sig.merge(mc, on=["cik", "month"], how="left")
        D["hold"] = D.month + pd.offsets.MonthBegin(1)
        D["ticker"] = D.cik.map(tick)
        D["ind"] = [ff12(psic.get(c, sic.get(c))) for c in D.cik]
        pt, rt = [], []
        for c, m, h, t in zip(D.cik, D.month, D.hold, D.ticker):
            if isinstance(t, str) and t in close.columns:
                pt.append(close.at[m, t] if m in close.index else np.nan)
                rt.append(R.at[h, t] if (h in R.index and t in R.columns) else np.nan)
            else:
                pt.append(np.nan)
                rt.append(np.nan)
        D["price_t"] = pt
        D["ret"] = rt
        D["priced"] = np.isfinite(D.price_t)
        D["missing"] = ~D.priced
        D["ended"] = D.priced & D.ret.isna() & (D.hold <= last_px)
        br, bs = [], []
        for c, h, m, mn, ind in zip(D.cik, D.hold, D.month, D.mcap, D.ind):
            mj = junecap.get((c, formation_year(h)), np.nan)
            if h not in bench.index:
                br.append(np.nan)
                bs.append(None)
                continue
            fy = formation_year(h)
            if fy < 2011:
                small = (not np.isfinite(mn)) or mn < 2e9
                br.append(bench.at[h, "IWM" if small else "SPY"])
                bs.append("IWM" if small else "SPY")
                continue
            v, s_ = B.get(h, c, fy, mj, mn, ind)
            br.append(v)
            bs.append(s_)
        D["bench"] = br
        D["bench_src"] = bs
        D["abn"] = D.ret - D.bench
        D = D[D.hold <= last_px]
        return D

    D = attach(SIG)
    D20 = attach(SIG20)
    D.to_csv(DATA / "panel_supplier_months.csv.gz", index=False)

    def assign_q(D, mask=None):
        D = D.copy()
        D["q"] = np.nan
        nr = {}
        for m, g in D.groupby("month"):
            base = g[g.priced] if mask is None else g[g.priced & mask(g)]
            elig = g.index if mask is None else g.index[mask(g)]
            if len(base) < MIN_RANKED:
                nr[m] = len(base)
                continue
            bp = breakpoints(base.signal.to_numpy(float))
            D.loc[elig, "q"] = bucket(D.loc[elig, "signal"], bp)
        return D, nr

    out = {}
    Dq, skipped = assign_q(D)
    res["sample"] = {
        "suppliers_with_links": int(L.supplier_cik.nunique()),
        "links_total": int(len(L)), "link_filings": int(L.adsh.nunique()),
        "suppliers_ever_ranked": int(Dq[Dq.priced & Dq.q.notna()].cik.nunique()),
        "suppliers_ever_signal": int(Dq.cik.nunique()),
        "supplier_months_ranked": int((Dq.priced & Dq.q.notna()).sum()),
        "months_skipped_lt_25": {str(k.date()): int(v) for k, v in skipped.items()},
        "ranked_per_month": Dq[Dq.priced & Dq.q.notna()].groupby("month").size().describe().to_dict(),
        "missing_supplier_months": int(Dq.missing.sum()),
        "missing_share": float(Dq.missing.mean()),
        "suppliers_never_priced": int((~Dq.groupby("cik").priced.any()).sum()),
        "ended_supplier_months": int(Dq.ended.sum()),
        "bench_src": Dq[Dq.priced].bench_src.value_counts().to_dict(),
        "n_customers_per_ranked_supplier_month": Dq[Dq.priced & Dq.q.notna()].n_cust.value_counts().to_dict(),
        "distinct_customer_tickers_used": int(LM[LM.cust_listed].cust_tk.nunique()),
        "links_used_in_ranking": int(LM[LM.cust_listed].merge(Dq[Dq.priced & Dq.q.notna()][["cik", "month"]],
                                                              on=["cik", "month"]).drop_duplicates(["adsh", "cid"]).shape[0]),
    }
    # excluded for lack of prices
    nev = Dq.groupby("cik").agg(priced_any=("priced", "any"), months=("month", "size")).reset_index()
    nev = nev[~nev.priced_any].merge(S[["supplier_cik", "name", "ticker", "ticker_src"]],
                                     left_on="cik", right_on="supplier_cik", how="left")
    nev[["cik", "name", "ticker", "ticker_src", "months"]].to_csv(DATA / "excluded_suppliers_no_price.csv", index=False)

    def full(Dq_, col="abn", weight=None, label=""):
        ew = run_sort(Dq_, col, weight=weight)
        sp = (ew[5] - ew[1]) - COST_M
        r = {"quintile_mean_monthly_x12": {int(k): float(ew[k].mean() * 12) for k in ew.columns},
             "spread_net": spread_stats(sp), "spread_gross": spread_stats(ew[5] - ew[1])}
        idx = sp.dropna().index
        half = idx[len(idx) // 2] if len(idx) else None
        r["half_split_first_month_of_second_half"] = str(half.date()) if half is not None else None
        r["first_half"] = spread_stats(sp[sp.index < half])
        r["second_half"] = spread_stats(sp[sp.index >= half])
        return r, ew, sp

    prim, ew, sp = full(Dq)
    out["primary_ew_abn"] = prim
    out["raw_returns_ew"] = full(Dq, col="ret")[0]
    for nm, sc in SCEN.items():
        e = run_sort(Dq.assign(missing=Dq.missing & Dq.q.notna()), "abn", scen=sc)
        s2 = (e[5] - e[1]) - COST_M
        out[f"scenario_{nm}"] = spread_stats(s2)
    # secondaries
    Ds, _ = assign_q(D, mask=lambda g: g.mcap < 2e9)
    out["small_lt_2b_ew_abn"] = full(Ds)[0]
    out["value_weighted_abn"] = full(Dq, weight="mcap")[0]
    D20q, _ = assign_q(D20)
    out["share_ge_20_ew_abn"] = full(D20q)[0]
    # information only
    Dl, _ = assign_q(D, mask=lambda g: g.mcap >= 2e9)
    out["info_large_ge_2b_ew_abn"] = full(Dl)[0]
    # information only, added after the first run (post hoc): suppliers that share a customer tie on
    # the signal; the pre-specified rule sends ties on a breakpoint to the lower fifth. Alternative:
    # average percentile ranks, fifth = ceil(5 x rank).
    Da = D.copy()
    Da["q"] = np.nan
    for m, g in Da.groupby("month"):
        pr = g[g.priced]
        if len(pr) < MIN_RANKED:
            continue
        rk = pr.signal.rank(pct=True, method="average")
        Da.loc[pr.index, "q"] = np.ceil(rk * 5).clip(1, 5)
    out["info_posthoc_ties_average_rank"] = full(Da)[0]
    t = prim["spread_net"]["t_nw6"]
    h1, h2 = prim["first_half"]["mean_monthly"], prim["second_half"]["mean_monthly"]
    out["verdict"] = {"t_nw6": t, "t_ge_2_5": bool(t >= 2.5), "first_half_positive": bool(h1 > 0),
                      "second_half_positive": bool(h2 > 0),
                      "answer": "Yes" if (t >= 2.5 and h1 > 0 and h2 > 0) else "No"}
    res["tests"] = out
    ms = pd.DataFrame({f"Q{int(k)}": ew[k] for k in ew.columns})
    ms["spread_net"] = sp
    ms.index.name = "hold_month"
    ms.to_csv(DATA / "monthly_spreads.csv", float_format="%.6f")
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=lambda o: None if isinstance(o, float) and not math.isfinite(o) else str(o)))
    print(json.dumps(out["verdict"], indent=1))
    print(json.dumps({k: (v.get("spread_net", v) if isinstance(v, dict) else v) for k, v in out.items() if k != "verdict"},
                     indent=1, default=str)[:4000])


if __name__ == "__main__":
    main()
