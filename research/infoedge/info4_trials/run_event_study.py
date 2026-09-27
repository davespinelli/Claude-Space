"""Step 6: event study. Abnormal return over trading days +1 to +20 after the posting date.

Primary: quiet events (no 8-K/6-K in the primary window), company under $5B at day 0.
AR = buy-and-hold return of the stock minus buy-and-hold return of its size-and-industry
benchmark (PREREG deviation 7). t clustered by calendar month of the posting date.
Writes results.json and data/event_returns.csv.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DRUG_SIC = {2833, 2834, 2835, 2836, 8731}
BANDS = [0, 3e8, 1e9, 5e9, np.inf]
WIN = 20
COST = 0.002
K_PLACEBO = 5


# --------------------------------------------------------------------------- prices
def load_prices():
    """Trading calendar, cleaned daily total returns, split-adjusted closes, and for each
    ticker the product of split ratios strictly after each date (to put an old share count
    on today's split basis)."""
    px = pd.read_pickle(HERE / "cache/prices_daily.pkl")
    px["date"] = pd.to_datetime(px.date)
    adj = px.pivot(index="date", columns="ticker", values="adj").sort_index()
    close = px.pivot(index="date", columns="ticker", values="close").sort_index()
    split = px.pivot(index="date", columns="ticker", values="split").sort_index().fillna(0.0)
    T = adj.index[adj["SPY"].notna()]
    adj, close, split = adj.loc[T], close.loc[T], split.loc[T]
    adj = adj.where(adj > 0); close = close.where(close > 0)
    k = split.replace(0.0, 1.0)
    after = k[::-1].cumprod()[::-1].shift(-1).fillna(1.0)   # product of split ratios strictly after t
    R = adj.pct_change(fill_method=None)
    R = clean(R)
    return T, R, close, after


def clean(R):
    A = R.to_numpy(copy=True); n = 0
    for j in range(A.shape[1]):
        col = A[:, j]
        idx = np.where(~np.isnan(col))[0]
        for a, b in zip(idx, idx[1:]):
            if (col[a] <= -0.9 and col[b] >= 9) or (col[a] >= 9 and col[b] <= -0.9):
                col[a] = col[b] = np.nan; n += 2
        big = col > 10
        n += int(np.nansum(big)); col[big] = np.nan
    print("bad-print rule removed", n, "daily returns")
    return pd.DataFrame(A, index=R.index, columns=R.columns)


# --------------------------------------------------------------------------- sizes
def share_series():
    """Share counts by company: the XBRL cover-page count (dei, as of the cover date) where the
    company has one, otherwise us-gaap/ifrs counts dated at filing (those are usually restated
    for splits that happened before the filing)."""
    sh = pd.read_csv(HERE / "cache/shares.csv", names=["cik", "filed", "end", "val", "src"])
    sh = sh[sh.val > 0].drop_duplicates()
    has_dei = set(sh.loc[sh.src == "dei", "cik"])
    sh = sh[(sh.src == "dei") | ~sh.cik.isin(has_dei)]
    pri = {"dei": 0, "gaap_out": 1, "gaap_wab": 2, "ifrs_wab": 3}
    sh["p"] = sh.src.map(pri)
    # several share classes on one cover -> sum within (cik, filed, end, src)
    sh = sh.groupby(["cik", "filed", "end", "src", "p"], as_index=False).val.sum()
    # per filing keep the preferred source and the latest as-of date
    sh = sh.sort_values(["cik", "filed", "p", "end"], ascending=[True, True, True, False]).drop_duplicates(["cik", "filed"], keep="first")
    sh["asof"] = np.where(sh.src == "dei", sh.end, sh.filed)
    sh["filed"] = pd.to_datetime(sh["filed"]); sh["asof"] = pd.to_datetime(sh["asof"])
    return {c: g[["filed", "asof", "val"]].reset_index(drop=True) for c, g in sh.groupby("cik")}


# 10-K filers whose US security is an ADS (checked by hand: BeiGene/BeOne, 1 ADS = 13 shares)
DOMESTIC_ADS = {1651308}


def ads_ratios():
    """ADS per ordinary share (PREREG deviation 6): Yahoo's current market value / (latest XBRL
    ordinary shares x current ADS price), used for foreign issuers when it is below 1/1.5 (one
    ADS = several shares) and for the hand-checked 10-K filers that trade as ADSs. A ratio above
    1.5, and any gap for other 10-K filers, mostly reflects shares issued since the last XBRL
    count (e.g. Canadian or Israeli companies listed directly), so it is not applied."""
    f = HERE / "cache/ads_ratio.csv"
    if not f.exists(): return {}
    a = pd.read_csv(f).dropna(subset=["q"])
    comp = pd.read_csv(HERE / "data/sponsor_companies_priced.csv")
    foreign = set(comp.loc[comp.foreign.astype(bool), "cik"])
    out = {}
    for c, q in zip(a.cik, a.q):
        if c in foreign and q < 1 / 1.5:
            out[c] = float(q)
        elif c in DOMESTIC_ADS:
            out[c] = float(q)
    return out


def mcap_panel(T, close, after, comp, shares):
    """Market value per company per trading day: latest filed share count, put on today's
    split basis, x split-adjusted close x ADS ratio (foreign issuers)."""
    out = {}
    ratio = ads_ratios()
    foreign = set(comp.loc[comp.foreign.astype(bool), "cik"])
    for r in comp.itertuples():
        t = r.ticker
        if not isinstance(t, str) or t not in close.columns or r.cik not in shares: continue
        g = shares[r.cik].copy()
        pos = T.searchsorted(g["asof"].values, side="right") - 1
        fac = np.where(pos >= 0, after[t].values[np.clip(pos, 0, None)], after[t].values[0])
        if r.cik in foreign or ratio.get(r.cik, 1.0) != 1.0:
            # Yahoo records ADS-ratio changes as splits of the ADS price; ordinary share counts
            # are not affected, so they are not re-based. The current ADS ratio does the rest.
            fac = np.ones(len(g))
        g["adj"] = g.val.values * fac
        # unit errors in the XBRL feed (e.g. a cover count reported x1000): on today's split
        # basis a share count cannot be 20x the company's recent count, or below 1/1000 of it
        ref = g.sort_values("filed").adj.tail(3).median()
        g = g[(g.adj <= 20 * ref) & (g.adj >= ref / 1000)]
        s = g.groupby("filed").adj.last().sort_index()
        s_daily = s.reindex(s.index.union(T)).ffill().reindex(T)
        out[r.cik] = s_daily * close[t] * ratio.get(r.cik, 1.0)
    return pd.DataFrame(out)


# --------------------------------------------------------------------------- benchmark
def benchmarks(T, R, comp, MV):
    """Daily equal-weighted return by (industry group, size band), band set at previous month-end.
    Returns sums and counts so the event firm can be left out."""
    tick = comp.set_index("cik").ticker
    grp = comp.set_index("cik").sic.fillna(0).astype(int).isin(DRUG_SIC).map({True: "drug", False: "other"})
    ciks = [c for c in MV.columns if tick.get(c) in R.columns]
    me = MV[ciks].resample("ME").last()
    me.index = me.index + pd.Timedelta(days=1)                   # month-end value applies from the next day
    band_m = me.apply(lambda col: pd.cut(col, BANDS, labels=False))
    band_d = band_m.reindex(band_m.index.union(T)).ffill().reindex(T)  # month label forward
    rets = pd.DataFrame({c: R[tick[c]] for c in ciks})
    sums, cnts = {}, {}
    for g in ("drug", "other"):
        for b in range(4):
            cols = [c for c in ciks if grp[c] == g]
            m = (band_d[cols] == b) & rets[cols].notna()
            sums[(g, b)] = rets[cols].where(m).sum(axis=1)
            cnts[(g, b)] = m.sum(axis=1)
    return sums, cnts, band_d, grp, rets


# --------------------------------------------------------------------------- stats
def clustered_t(x, clusters):
    x = np.asarray(x, float); n = len(x)
    if n < 2: return np.nan, np.nan
    m = x.mean(); d = pd.Series(x - m).groupby(np.asarray(clusters)).sum()
    G = len(d)
    if G < 2: return m, np.nan
    se = np.sqrt(G / (G - 1) * (d ** 2).sum()) / n
    return m, m / se


def summarize(df, col="ar"):
    df = df.dropna(subset=[col]).sort_values("post_date")
    if len(df) == 0: return {"n": 0}
    m, t = clustered_t(df[col], df.month)
    half = df.post_date.iloc[len(df) // 2]
    h1, h2 = df[df.post_date < half], df[df.post_date >= half]
    m1, t1 = clustered_t(h1[col], h1.month); m2, t2 = clustered_t(h2[col], h2.month)
    return {"n": int(len(df)), "n_companies": int(df.cik.nunique()), "n_months": int(df.month.nunique()),
            "mean": m, "t_clustered": t, "median": float(df[col].median()),
            "share_negative": float((df[col] < 0).mean()),
            "half1": {"n": int(len(h1)), "mean": m1, "t": t1, "to": str(h1.post_date.max())},
            "half2": {"n": int(len(h2)), "mean": m2, "t": t2, "from": str(h2.post_date.min())},
            "mean_after_cost_short": -(m) - COST}


def verdict(s):
    ok = (s.get("n", 0) > 0 and s["t_clustered"] <= -2.5 and s["half1"]["mean"] < 0 and s["half2"]["mean"] < 0)
    return "Yes" if ok else "No"


# --------------------------------------------------------------------------- main
def main():
    T, R, close, after = load_prices()
    raw = close
    comp = pd.read_csv(HERE / "data/sponsor_companies_priced.csv")
    shares = share_series()
    MV = mcap_panel(T, close, after, comp, shares)
    sums, cnts, band_d, grp, rets = benchmarks(T, R, comp, MV)
    G = (1 + rets.fillna(0)).cumprod()                          # peer wealth index (flat when not trading)
    GRP = np.array([grp[c] for c in rets.columns]); COLS = np.array(rets.columns)
    Rn = rets.to_numpy(); Gn = G.to_numpy(); Bn = band_d[list(rets.columns)].to_numpy()
    tick = comp.set_index("cik").ticker.to_dict()
    hist = pd.read_csv(HERE / "cache/sec_names_hist.csv")
    active = hist.groupby("cik").agg(first=("first", "min"), last=("last", "max"))
    fl = pd.read_csv(HERE / "cache/float.csv", names=["cik", "filed", "end", "val", "unit"])
    fl = fl[(fl.unit == "USD") & (fl.val > 0)].sort_values("filed")

    C = pd.read_csv(HERE / "data/changes_mapped.csv")
    C = C[C.post_date.notna()]

    def aggregate(Csub, k8col="k8_primary"):
        ev = (Csub.groupby(["cik", "post_date"])
                 .agg(types=("type", lambda x: "|".join(sorted(set(x)))), n_trials=("nct", "nunique"),
                      k8=(k8col, "any"), ncts=("nct", lambda x: "|".join(sorted(set(x)))))
                 .reset_index())
        return ev

    def etf(name, i0):
        return float(np.nanprod(1 + R[name].iloc[i0 + 1:i0 + 1 + WIN].values) - 1)

    def measure(cik, t, i0, mcap):
        """Stock buy-and-hold return over days +1..+20 and four benchmarks:
        bh    - primary: mean of the other cell members' own compound returns over the window
                (industry group x size band at the start; members must trade on day +1);
        daily - robustness: compound of the daily equal-weighted cell average (rebalanced);
        etf   - IWM (under $2B) or SPY alone;  xbi - XBI alone."""
        r = R[t].iloc[i0 + 1:i0 + 1 + WIN]
        stock = float(np.nanprod(1 + r.values) - 1)
        small = np.isnan(mcap) or mcap < 2e9
        etf_ret = etf("IWM" if small else "SPY", i0)
        g = grp.get(cik, "other")
        b = pd.cut([mcap], BANDS, labels=False)[0] if not np.isnan(mcap) else 0
        m = (GRP == g) & (Bn[i0 + 1] == b) & ~np.isnan(Rn[i0 + 1]) & (COLS != cik)
        if m.sum() >= 10:
            bh = float(np.mean(Gn[i0 + WIN, m] / Gn[i0, m] - 1))
        else:
            bh = etf_ret
        own_band = band_d[cik].iloc[i0 + 1:i0 + 1 + WIN] if cik in band_d.columns else pd.Series(np.nan, index=r.index)
        bm = []
        for k, d in enumerate(r.index):
            s_, n_ = sums[(g, b)].loc[d], cnts[(g, b)].loc[d]
            if own_band.iloc[k] == b and not np.isnan(r.iloc[k]):
                s_, n_ = s_ - r.iloc[k], n_ - 1
            bm.append(s_ / n_ if n_ >= 10 else R["IWM" if small else "SPY"].loc[d])
        daily = float(np.nanprod(1 + np.array(bm, float)) - 1)
        return {"n_ret_days": int(r.notna().sum()), "ret": stock, "n_peers": int(m.sum()),
                "bench": bh, "ar": stock - bh, "ar_daily_rebal": stock - daily,
                "ar_iwmspy": stock - etf_ret, "ar_xbi": stock - etf("XBI", i0)}

    def event_returns(ev):
        rows = []
        for e in ev.itertuples():
            pd0 = pd.Timestamp(e.post_date)
            i0 = T.searchsorted(pd0, side="right") - 1          # day 0: last trading day on/before posting date
            rec = {"cik": e.cik, "post_date": e.post_date, "types": e.types, "n_trials": e.n_trials,
                   "k8": e.k8, "ncts": e.ncts, "month": e.post_date[:7], "i0": int(i0)}
            t = tick.get(e.cik)
            priced = (isinstance(t, str) and t in R.columns and i0 + WIN < len(T)
                      and not np.isnan(raw[t].iloc[max(i0 - 5, 0):i0 + 1]).all())
            a = active.loc[e.cik] if e.cik in active.index else None
            listed_filer = a is not None and a["first"] <= e.post_date <= (pd.Timestamp(a["last"]) + pd.DateOffset(months=15)).strftime("%Y-%m-%d")
            if i0 + WIN >= len(T):
                rec["status"] = "too_recent"; rows.append(rec); continue
            if priced and R[t].iloc[i0 + 1:i0 + 1 + WIN].notna().sum() == 0:
                priced = False                                   # no trades at all in the window
            if priced:
                mv = MV[e.cik].iloc[max(i0 - 5, 0):i0 + 1].dropna() if e.cik in MV.columns else pd.Series(dtype=float)
                rec["mcap"] = float(mv.iloc[-1]) if len(mv) else np.nan
                rec["mcap_src"] = "shares_x_price" if len(mv) else "none"
                if np.isnan(rec["mcap"]):                        # no XBRL share count: public float instead
                    f = fl[(fl.cik == e.cik) & (fl.filed <= e.post_date)]
                    if len(f): rec["mcap"], rec["mcap_src"] = float(f.val.iloc[-1]), "float"
                rec.update(measure(e.cik, t, i0, rec["mcap"]))
                rec["status"] = "priced"
            elif listed_filer:
                f = fl[(fl.cik == e.cik) & (fl.filed <= e.post_date)]
                rec["mcap"] = float(f.val.iloc[-1]) if len(f) else np.nan
                rec["status"] = "missing"
            else:
                rec["status"] = "not_listed"
            rows.append(rec)
        return pd.DataFrame(rows)

    out = {}
    ev_all = aggregate(C)
    E = event_returns(ev_all)
    E.to_csv(HERE / "data/event_returns.csv", index=False)

    def primary_set(E, cap=5e9):
        q = E[(~E.k8) & (E.status == "priced") & (E.mcap < cap)]
        return q

    P = primary_set(E)
    out["primary"] = summarize(P)
    out["primary"]["verdict"] = verdict(out["primary"])
    out["counts"] = {
        "company_date_events_all": int(len(E)),
        "status": E.status.value_counts().to_dict(),
        "with_8k_in_window": int(E.k8.sum()),
        "priced_quiet_any_size": int(((~E.k8) & (E.status == "priced")).sum()),
        "priced_quiet_under_5b": int(len(P)),
        "priced_quiet_5b_or_more": int(((~E.k8) & (E.status == "priced") & (E.mcap >= 5e9)).sum()),
        "priced_quiet_no_mcap": int(((~E.k8) & (E.status == "priced") & E.mcap.isna()).sum()),
    }
    out["by_type"] = {}
    for ty in ("status", "delay", "cut"):
        out["by_type"][ty] = summarize(P[P.types.str.contains(ty)])
    out["by_type"]["status_terminated_etc_only"] = summarize(P[P.types == "status"])
    # secondaries
    C23 = C[C.phase23]
    E23 = event_returns(aggregate(C23))
    out["secondary_phase23"] = summarize(primary_set(E23))
    out["secondary_under_1b"] = summarize(primary_set(E, cap=1e9))
    # robustness
    out["robust_literal_8k_window"] = summarize(primary_set(event_returns(aggregate(C, "k8_literal"))))
    out["robust_daily_rebalanced_benchmark"] = summarize(P, "ar_daily_rebal")
    out["robust_iwm_spy_benchmark"] = summarize(P, "ar_iwmspy")
    out["robust_xbi_benchmark"] = summarize(P, "ar_xbi")
    out["robust_raw_return"] = summarize(P, "ret")
    foreign = set(comp.loc[comp.foreign.astype(bool), "cik"])
    out["robust_ex_foreign_issuers"] = summarize(P[~P.cik.isin(foreign)])
    out["robust_including_8k_events"] = summarize(E[(E.status == "priced") & (E.mcap < 5e9)])
    out["robust_8k_events_only"] = summarize(E[(E.k8) & (E.status == "priced") & (E.mcap < 5e9)])
    # placebo (required by the coordinator after INFO-5): the same companies on random
    # non-event dates in the same calendar year, same sample rules, same benchmarks
    rng = np.random.default_rng(20260926)
    ev_pos = E.groupby("cik").i0.apply(lambda x: np.sort(x.values)).to_dict()
    year_of = np.array([d.year for d in T])
    pl_rows = []
    for e in P.itertuples():
        t = tick[e.cik]; y = int(e.post_date[:4])
        cand = np.where(year_of == y)[0]
        cand = cand[cand + WIN < len(T)]
        own = ev_pos.get(e.cik, np.array([]))
        if len(own):
            dist = np.min(np.abs(cand[:, None] - own[None, :]), axis=1)
            cand = cand[dist > WIN]
        cand = cand[~np.isnan(raw[t].values[cand])]
        if e.cik in MV.columns:
            mvv = MV[e.cik].values[cand]
            cand = cand[~np.isnan(mvv) & (mvv < 5e9)]
        if len(cand) == 0: continue
        pick = rng.choice(cand, size=min(K_PLACEBO, len(cand)), replace=False)
        vals = [measure(e.cik, t, int(i), float(MV[e.cik].values[i]) if e.cik in MV.columns else e.mcap) for i in pick]
        row = {"cik": e.cik, "post_date": e.post_date, "month": e.month, "n_placebo": len(vals)}
        for col in ("ar", "ar_iwmspy", "ar_xbi", "ar_daily_rebal"):
            pm = float(np.nanmean([v[col] for v in vals]))
            row["placebo_" + col] = pm
            row["diff_" + col] = getattr(e, col) - pm
        pl_rows.append(row)
    PL = pd.DataFrame(pl_rows)
    PL.to_csv(HERE / "data/placebo.csv", index=False)
    out["placebo"] = {"K": K_PLACEBO, "n_events_with_placebo": int(len(PL))}
    for col in ("ar", "ar_iwmspy", "ar_xbi", "ar_daily_rebal"):
        out["placebo"]["placebo_mean_" + col] = summarize(PL, "placebo_" + col)
        out["placebo"]["event_minus_placebo_" + col] = summarize(PL, "diff_" + col)

    # missing-company bounds
    M = E[(~E.k8) & (E.status == "missing") & ((E.mcap < 5e9) | E.mcap.isna())].copy()
    # Trials of sponsors with no Yahoo price at all were downloaded only in part (a random
    # sample, PREREG deviation 10): their events are weighted up by 1 / (fraction downloaded).
    U = pd.read_csv(HERE / "data/trials_universe.csv")
    done = {p.name[:-8] for p in (HERE / "cache/hist_list").glob("*.json.gz")}
    unp = U[~U.priced_sponsor.astype(bool)]
    frac = float(unp.nct.isin(done).mean()) if len(unp) else 1.0
    priced_ciks = set(comp.loc[comp.ticker.notna(), "cik"])
    M["w"] = np.where(M.cik.isin(priced_ciks), 1.0, 1.0 / max(frac, 1e-9))
    n_eff = float(M.w.sum())
    out["missing"] = {"n_missing_events": int(len(M)), "n_missing_companies": int(M.cik.nunique()),
                      "unpriced_trials_fraction_downloaded": frac,
                      "n_missing_events_scaled": n_eff,
                      "share_of_would_be_sample": n_eff / (n_eff + len(P)) if n_eff + len(P) else None}
    for lab, val in (("minus30", -0.30), ("plus15", 0.15)):
        x = np.concatenate([P.ar.values, np.full(len(M), val)])
        w = np.concatenate([np.ones(len(P)), M.w.values])
        cl = np.concatenate([P.month.values, M.month.values])
        m = float(np.sum(w * x) / np.sum(w))
        d = pd.Series(w * (x - m)).groupby(cl).sum()
        se = np.sqrt(len(d) / (len(d) - 1) * (d ** 2).sum()) / np.sum(w)
        out["missing"][lab] = {"mean": m, "t_clustered": m / se, "n_weighted": float(np.sum(w))}
    # yearly
    P2 = P.assign(year=P.post_date.str[:4])
    out["by_year"] = {y: {"n": int(len(g)), "mean": float(g.ar.mean())} for y, g in P2.groupby("year")}
    json.dump(out, open(HERE / "results.json", "w"), indent=2, default=float)
    print(json.dumps(out["primary"], indent=2, default=float))
    print(json.dumps(out["counts"], indent=2, default=float))


if __name__ == "__main__":
    main()
