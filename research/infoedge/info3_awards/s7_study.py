#!/usr/bin/env python3
"""Stage 7: the pre-registered event study.

Abnormal return (AR) on day k = stock total return - IWM total return (Yahoo
adjusted closes). CAR = sum of AR over trading days +1..+20 after day 0.
Net CAR = CAR - 0.2% (cost per event). t-statistic: mean net CAR over its
standard error clustered by calendar month of the public date (CR1 small-sample
factor G/(G-1)). Halves: events before / on-or-after the median public date.

Samples (each with the same-company overlap rule: an event whose day 0 falls
within 20 trading days after the day 0 of the previous kept event of the same
company is dropped):
  primary     unannounced (no 8-K within +-5 trading days of the action), >= 2%
  sec_5pct    unannounced, >= 5%
  sec_civ     unannounced, civilian awarding agency only
  info_*      DoD only, announced, all, market-cap floor $50M, BHAR.
Survivorship bounds: every missing-company event (no usable Yahoo price; 2%
screen on public float) is added with CAR -30% or +15%; a priced event whose
price series stops inside the window gets -30% / +15% added on its last day.

Price-data rule (same idea as research/oplev, applied to daily data): a
one-day round trip of 10x or more (<= -90% then >= +900%, or the reverse) is a
bad print, both days set missing; any remaining daily return above +1,000% is
set missing.

Writes results.json and data/event_returns.csv.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import CACHE, DATA, HERE, log

WIN = 20
COST = 0.002
BAR = 2.5
PX = CACHE / "prices"
SCEN = {"minus30": -0.30, "plus15": 0.15,
        # information only: the same annual bounds scaled to a 20-trading-day window
        "minus30_scaled": 0.70 ** (20 / 252) - 1, "plus15_scaled": 1.15 ** (20 / 252) - 1}


def clean_daily(R: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    A = R.to_numpy(copy=True)
    nv = 0
    for j in range(A.shape[1]):
        c = A[:, j]
        ok = np.isfinite(c)
        idx = np.where(ok)[0]
        for a, b in zip(idx[:-1], idx[1:]):
            x, y = c[a], c[b]
            if (x <= -0.9 and y >= 9) or (x >= 9 and y <= -0.9):
                c[a] = np.nan
                c[b] = np.nan
                nv += 1
        A[:, j] = c
    big = np.isfinite(A) & (A > 10)
    nb = int(big.sum())
    A[big] = np.nan
    return pd.DataFrame(A, index=R.index, columns=R.columns), {"round_trips_removed": nv, "above_1000pct_removed": nb}


def load_returns():
    px = pd.read_parquet(PX / "daily.parquet")
    px["date"] = pd.to_datetime(px.date).dt.tz_localize(None).dt.normalize()
    px = px.drop_duplicates(["date", "ticker"], keep="last")
    adj = px.pivot(index="date", columns="ticker", values="adj").sort_index()
    cal = adj["IWM"].dropna().index
    adj = adj.reindex(cal)
    adj = adj.where(adj > 0)
    # carry a price over at most 5 missing trading days (no-trade days in thin stocks)
    adjf = adj.ffill(limit=5)
    R = adjf / adjf.shift(1) - 1
    R, info = clean_daily(R)
    return R, cal, adj, info


def clustered(x: np.ndarray, g: np.ndarray) -> tuple[float, float, int]:
    n = len(x)
    if n < 2:
        return float(np.mean(x)) if n else np.nan, np.nan, n
    m = x.mean()
    e = x - m
    df = pd.DataFrame({"e": e, "g": g}).groupby("g").e.sum()
    G = len(df)
    if G < 2:
        return m, np.nan, G
    v = (G / (G - 1)) * float((df ** 2).sum()) / n ** 2
    return m, np.sqrt(v), G


def stats(D: pd.DataFrame, col: str = "car") -> dict:
    if not len(D):
        return {"n": 0}
    x = D[col].to_numpy(float)
    g = D.public_date.dt.to_period("M").astype(str).to_numpy()
    m, se, G = clustered(x, g)
    net = m - COST
    med = D.public_date.sort_values().iloc[len(D) // 2]
    h1, h2 = D[D.public_date < med], D[D.public_date >= med]
    out = {"n": int(len(D)), "companies": int(D.cik.nunique()), "clusters": G,
           "mean_car": m, "mean_car_net": net, "se_clustered": se,
           "t_gross": m / se if se else np.nan, "t_net": net / se if se else np.nan,
           "median_car": float(np.median(x)), "share_positive": float((x > 0).mean()),
           "plain_t_net": net / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan,
           # information: clustered by company instead of month
           "t_net_company_cluster": (lambda mse: (mse[0] - COST) / mse[1] if mse[1] else np.nan)(
               clustered(x, D.cik.astype(str).to_numpy())),
           "top_company_share": float(D.cik.value_counts(normalize=True).iloc[0]),
           # information: 1% winsorised mean after cost (penny-stock outliers)
           "winsor1_net": float(np.clip(x, np.quantile(x, 0.01), np.quantile(x, 0.99)).mean() - COST) if len(x) > 20 else np.nan,
           "split_date": str(med.date()), "first": str(D.public_date.min().date()),
           "last": str(D.public_date.max().date())}
    for lab, H in (("h1", h1), ("h2", h2)):
        if len(H) >= 2:
            hm, hse, hg = clustered(H[col].to_numpy(float), H.public_date.dt.to_period("M").astype(str).to_numpy())
            out[lab] = {"n": int(len(H)), "mean_car_net": hm - COST, "t_net": (hm - COST) / hse if hse else np.nan,
                        "first": str(H.public_date.min().date()), "last": str(H.public_date.max().date())}
        else:
            out[lab] = {"n": int(len(H))}
    return out


def verdict(s: dict) -> str:
    if not s.get("n"):
        return "No (no events)"
    ok_t = np.isfinite(s.get("t_net", np.nan)) and s["t_net"] >= BAR
    ok_h = all(s.get(h, {}).get("mean_car_net", -1) > 0 for h in ("h1", "h2"))
    return "Yes" if ok_t and ok_h else "No"


def no_overlap(D: pd.DataFrame) -> pd.DataFrame:
    keep = []
    for cik, g in D.sort_values("i0").groupby("cik"):
        last = -10 ** 9
        for idx, r in g.iterrows():
            if r.i0 > last + WIN:
                keep.append(idx)
                last = r.i0
    return D.loc[sorted(keep)]


PLACEBO_K = 5
PLACEBO_SEED = 20260926


def window_car(R, iwm, tk, i0):
    s = R[tk].iloc[i0 + 1:i0 + 1 + WIN]
    b = iwm.iloc[i0 + 1:i0 + 1 + WIN]
    ok = s.notna()
    return float((s - b)[ok].sum()) if ok.any() else np.nan


def placebo(D, Eall, R, iwm, adj, cal):
    """Coordinator-required robustness line (not part of the verdict): for each
    event, PLACEBO_K random trading days of the same company in the same
    calendar year, at least 20 trading days away from any of that company's
    event days (announced or not), with a price on the day and a complete
    window; placebo CAR computed exactly like the event CAR. Returns per-event
    mean placebo CAR (NaN if no placebo day qualifies)."""
    rng = np.random.default_rng(PLACEBO_SEED)
    ev_days = Eall.groupby("cik").i0.apply(lambda s: np.sort(s.to_numpy()))
    years = pd.Series(cal.year, index=np.arange(len(cal)))
    out = []
    for r in D.itertuples():
        tk = r.ticker
        if tk not in R.columns:
            out.append(np.nan)
            continue
        yr = cal[int(r.i0)].year
        pos = years.index[(years == yr).to_numpy()].to_numpy()
        pos = pos[pos + WIN <= len(cal) - 1]
        evs = ev_days.get(r.cik, np.array([]))
        if len(evs):
            far = np.min(np.abs(pos[:, None] - evs[None, :]), axis=1) > WIN
            pos = pos[far]
        has = adj[tk].iloc[pos].notna().to_numpy() if len(pos) else np.array([], bool)
        pos = pos[has]
        if not len(pos):
            out.append(np.nan)
            continue
        pick = rng.choice(pos, size=min(PLACEBO_K, len(pos)), replace=False)
        cs = [window_car(R, iwm, tk, int(i)) for i in pick]
        cs = [c for c in cs if np.isfinite(c)]
        out.append(float(np.mean(cs)) if cs else np.nan)
    return np.array(out, float)


def main():
    R, cal, adj, clean_info = load_returns()
    E = pd.read_parquet(DATA / "events.parquet")
    E = E[E.complete_window].copy()
    iwm = R["IWM"]
    cars, bh, ndays, trunc = [], [], [], []
    for r in E.itertuples():
        tk = r.ticker
        i0 = int(r.i0)
        s = R[tk].iloc[i0 + 1:i0 + 1 + WIN] if tk in R.columns else pd.Series(dtype=float)
        b = iwm.iloc[i0 + 1:i0 + 1 + WIN]
        ok = s.notna()
        ar = (s - b)[ok]
        cars.append(float(ar.sum()) if ok.any() else np.nan)
        bh.append(float((1 + s[ok]).prod() - (1 + b[ok]).prod()) if ok.any() else np.nan)
        ndays.append(int(ok.sum()))
        # series stops inside the window (no later price at all)
        lv = adj[tk].last_valid_index() if tk in adj.columns else None
        trunc.append(bool(lv is not None and lv < cal[min(i0 + WIN, len(cal) - 1)]))
    E["car"] = cars
    E["bhar"] = bh
    E["n_days"] = ndays
    E["truncated"] = trunc
    E = E[E.n_days > 0].copy()
    E.to_csv(DATA / "event_returns.csv", index=False)

    X = pd.read_parquet(DATA / "missing_events.parquet")
    if len(X):
        X = X[X.complete_window].copy()
        X["i0"] = cal.searchsorted(pd.to_datetime(X.day0).astype("datetime64[ns]"), side="right") - 1

    def sample(D, **kw):
        m = pd.Series(True, index=D.index)
        if kw.get("unannounced"):
            m &= ~D.announced
        if kw.get("announced"):
            m &= D.announced
        if "min_ratio" in kw:
            m &= D.max_ratio >= kw["min_ratio"]
        if kw.get("civilian"):
            m &= ~D.dod
        if kw.get("dod"):
            m &= D.dod.astype(bool)
        if "min_mcap" in kw:
            m &= D.mcap >= kw["min_mcap"]
        if "max_mcap" in kw:
            m &= D.mcap < kw["max_mcap"]
        return no_overlap(D[m])

    specs = {
        "primary": dict(unannounced=True),
        "sec_5pct": dict(unannounced=True, min_ratio=0.05),
        "sec_civilian": dict(unannounced=True, civilian=True),
        "info_dod": dict(unannounced=True, dod=True),
        "info_announced": dict(announced=True),
        "info_all_events": dict(),
        "info_mcap_ge_50m": dict(unannounced=True, min_mcap=50e6),
        "info_mcap_lt_50m": dict(unannounced=True, max_mcap=50e6),
        "info_10pct": dict(unannounced=True, min_ratio=0.10),
    }
    res = {"clean_info": clean_info, "samples": {}}
    for k, kw in specs.items():
        D = sample(E, **kw)
        s = stats(D)
        s["bhar"] = stats(D.assign(car=D.bhar))
        s["truncated_windows"] = int(D.truncated.sum())
        if k in ("primary", "sec_5pct", "sec_civilian"):
            s["verdict"] = verdict(s)
        if k in ("primary", "sec_5pct", "sec_civilian", "info_dod", "info_mcap_ge_50m", "info_mcap_lt_50m"):
            # (a) placebo: same companies, random non-event dates in the same calendar year
            pl = placebo(D, E, R, iwm, adj, cal)
            ok = np.isfinite(pl)
            Dp = D[ok].assign(placebo=pl[ok])
            Dp = Dp.assign(diff=Dp.car - Dp.placebo)
            sp = stats(Dp.assign(car=Dp.placebo))
            sd = stats(Dp.assign(car=Dp["diff"] + COST))      # no cost on a difference
            s["placebo"] = {"n_events_with_placebo": int(ok.sum()),
                            "mean_placebo_car_net": sp.get("mean_car_net"), "t_placebo_net": sp.get("t_net"),
                            "mean_event_minus_placebo": sd.get("mean_car_net"), "t_event_minus_placebo": sd.get("t_net"),
                            "h1_diff": sd.get("h1", {}).get("mean_car_net"), "h2_diff": sd.get("h2", {}).get("mean_car_net")}
            # (b) the headline is already measured against IWM only (all events < $2B)
            s["benchmark"] = "IWM (all event companies under $2B); no size-and-industry benchmark was built"
        # survivorship bounds
        Xk = X.copy() if len(X) else X
        if len(Xk):
            if kw.get("unannounced"):
                Xk = Xk[~Xk.announced]
            if kw.get("announced"):
                Xk = Xk[Xk.announced]
            if "min_ratio" in kw:
                Xk = Xk[Xk.max_ratio >= kw["min_ratio"]]
            if kw.get("civilian"):
                Xk = Xk[~Xk.dod]
            if kw.get("dod"):
                Xk = Xk[Xk.dod.astype(bool)]
            if "min_mcap" in kw:
                Xk = Xk[Xk.pfloat >= kw["min_mcap"]]
            if "max_mcap" in kw:
                Xk = Xk[Xk.pfloat < kw["max_mcap"]]
            Xk = no_overlap(Xk)            # same overlap rule as priced events (PREREG E4)
        s["missing_events"] = int(len(Xk)) if len(X) else 0
        s["missing_companies"] = int(Xk.cik.nunique()) if len(X) and len(Xk) else 0
        for lab, v in SCEN.items():
            A = D[["cik", "public_date", "car"]].copy()
            A.loc[D.truncated.to_numpy(), "car"] += v
            if len(X) and len(Xk):
                A = pd.concat([A, pd.DataFrame({"cik": Xk.cik, "public_date": Xk.public_date, "car": v})])
            st = stats(A)
            s[f"bound_{lab}"] = {"n": st["n"], "mean_car_net": st.get("mean_car_net"), "t_net": st.get("t_net")}
        res["samples"][k] = s
        log(f"{k}: n={s['n']} mean net {s.get('mean_car_net', np.nan):+.4f} t={s.get('t_net', np.nan):.2f} "
            f"h1 {s.get('h1', {}).get('mean_car_net', np.nan):+.4f} h2 {s.get('h2', {}).get('mean_car_net', np.nan):+.4f}"
            + (f" -> {s['verdict']}" if 'verdict' in s else ""))
    # counts for the report
    allE = E
    res["counts"] = {
        "events_complete_window": int(len(allE)),
        "dod": int(allE.dod.sum()), "civilian": int((~allE.dod).sum()),
        "announced": int(allE.announced.sum()), "unannounced": int((~allE.announced).sum()),
        "dod_announced": int((allE.dod & allE.announced).sum()),
        "dod_unannounced": int((allE.dod & ~allE.announced).sum()),
        "civ_announced": int((~allE.dod & allE.announced).sum()),
        "civ_unannounced": int((~allE.dod & ~allE.announced).sum()),
        "companies": int(allE.cik.nunique()),
        "missing_events": int(len(X)) if len(X) else 0,
        "missing_companies": int(X.cik.nunique()) if len(X) else 0,
    }
    (HERE / "results.json").write_text(json.dumps(res, indent=2, default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else str(o)))
    log(json.dumps(res["counts"]))


if __name__ == "__main__":
    main()
