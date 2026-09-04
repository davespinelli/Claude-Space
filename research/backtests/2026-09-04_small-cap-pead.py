#!/usr/bin/env python3
"""Idea 31 — post-earnings-announcement drift (PEAD) with the announcement-day return as
the surprise proxy (Chan, Jegadeesh & Lakonishok 1996).

Universe: research/universe_broad.json (136 names, current constituents -> survivorship bias).
NOTE: the brief calls this "small-cap PEAD", but universe_broad.json is liquid US LARGE caps
plus ~30 ETFs. There is no small-cap single-name data in this repo, so what is actually tested
here is large-cap PEAD. CJL's effect is strongest in small caps, so this is a conservative
(and different) test of the same mechanism. Stated up front, not buried.

Events: 8-K filings whose `items` field contains 2.02 (Results of Operations), from EDGAR,
cached to data/earnings_dates.csv by research/fetch_earnings_dates.py.

Signal (filing-time ambiguity): EDGAR gives a filing DATE, not a filing TIME, so we do not
know whether the market reacted on day t or day t+1. As the brief specifies, we approximate by
taking whichever of the two candidate 1-day abnormal returns has the larger absolute value:
    W_t   = r(close[t-1] -> close[t])    - SPY same window   (filed pre-close)
    W_t1  = r(close[t]   -> close[t+1])  - SPY same window   (filed post-close)
    surprise = W_t if |W_t| >= |W_t1| else W_t1
The union of those two windows is the close[t-1]->close[t+1] 2-day abnormal return, which is
reported as a sensitivity ("2day" surprise mode). Both are known by close[t+1]; cohorts are
formed at the weekly rebalance on/after t+1 and the engine applies weights the NEXT day, so
there is no look-ahead either way.

Portfolio: each week, rank all announcements whose reaction window completed in the last 5
trading days; go long the top tercile (or top quintile) equal-weight; hold H trading days.
Overlapping cohorts, equal weight across every open slot, gross 100%, weekly rebalance, 10 bps.

Grid (4 points, 2 tuned parameters): cut in {tercile, quintile} x hold in {40, 60}.

Run:  .venv/bin/python research/backtests/2026-09-04_small-cap-pead.py
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask          # noqa: E402

COST_BPS = 10.0
EVENTS = ROOT / "data" / "earnings_dates.csv"
DEDUP_DAYS = 20      # collapse multiple 2.02 8-Ks for the same quarter (some issuers file 2+)


# ---------------------------------------------------------------- events + surprise
def load_events(px, dedup_days=DEDUP_DAYS):
    """Map each 8-K/2.02 filing date onto the trading-day grid. Returns a DataFrame with
    columns ticker, filing_date, t (positional index of the event day)."""
    ev = pd.read_csv(EVENTS, parse_dates=["filing_date"])
    idx = px.index
    have = [c for c in px.columns if px[c].notna().sum() > 500]
    ev = ev[ev.ticker.isin(have)].copy()
    # event day t = first trading day on/after the filing date
    pos = idx.searchsorted(ev.filing_date.values, side="left")
    ev["t"] = pos
    ev = ev[(ev.t >= 1) & (ev.t <= len(idx) - 2)]
    ev = ev.sort_values(["ticker", "t"]).drop_duplicates(["ticker", "t"])
    # de-duplicate: within a ticker, drop any event within `dedup_days` of the previous kept one
    keep, last = [], {}
    for tk, t in zip(ev.ticker.values, ev.t.values):
        if tk in last and t - last[tk] < dedup_days:
            keep.append(False)
        else:
            keep.append(True); last[tk] = t
    ev = ev[np.array(keep)].reset_index(drop=True)
    ev["event_date"] = idx[ev.t.values]
    return ev


def add_surprise(ev, px, mode="maxabs"):
    """Abnormal (SPY-adjusted) announcement return. mode: 'maxabs' | '2day' | 't' | 't1'."""
    idx = px.index
    spy = px["SPY"]
    out = np.full(len(ev), np.nan)
    for i, (tk, t) in enumerate(zip(ev.ticker.values, ev.t.values)):
        s = px[tk]
        p_m1, p_0, p_1 = s.iloc[t - 1], s.iloc[t], s.iloc[t + 1]
        b_m1, b_0, b_1 = spy.iloc[t - 1], spy.iloc[t], spy.iloc[t + 1]
        if not np.isfinite([p_m1, p_0, p_1, b_m1, b_0, b_1]).all():
            continue
        w_t = (p_0 / p_m1 - 1) - (b_0 / b_m1 - 1)
        w_t1 = (p_1 / p_0 - 1) - (b_1 / b_0 - 1)
        if mode == "maxabs":
            out[i] = w_t if abs(w_t) >= abs(w_t1) else w_t1
        elif mode == "2day":
            out[i] = (p_1 / p_m1 - 1) - (b_1 / b_m1 - 1)
        elif mode == "t":
            out[i] = w_t
        else:
            out[i] = w_t1
    ev = ev.copy()
    ev["car"] = out
    ev["ready"] = ev.t + 1                    # signal fully known at close of t+1
    return ev.dropna(subset=["car"]).reset_index(drop=True)


# ---------------------------------------------------------------- weights
def pead_weights(px, ev, cut="tercile", hold=60, lookback=5, gross=1.0):
    """Weekly cohorts of the top-`cut` announcements of the last `lookback` trading days,
    each held `hold` trading days; equal weight across all open slots, gross 100%."""
    lo, hi = {"tercile": (2 / 3, 1.0), "quintile": (0.8, 1.0),
              "all": (0.0, 1.0), "bottom": (0.0, 1 / 3), "mid": (1 / 3, 2 / 3)}[cut]
    idx = px.index
    rb = np.flatnonzero(rebalance_mask(idx, "W").values)      # positional rebalance days
    ready = ev.ready.values
    rows, when = [], []
    cohorts = []                                              # (formed_pos, [tickers])
    n_sel, n_cons = 0, 0
    for d in rb:
        sel = ev[(ready > d - lookback) & (ready <= d)]
        if len(sel) >= 3:
            n_cons += len(sel)
            a, b_ = sel.car.quantile(lo), sel.car.quantile(hi)
            win = sel[(sel.car >= a) & (sel.car <= b_)]
            if len(win):
                cohorts.append((d, list(win.ticker.values)))
                n_sel += len(win)
        cohorts = [(f, tk) for f, tk in cohorts if d - f < hold]
        slots = [t for _, tk in cohorts for t in tk]
        w = pd.Series(0.0, index=px.columns)
        if slots:
            share = gross / len(slots)
            for t in slots:
                w[t] += share
        rows.append(w.values); when.append(idx[d])
    # weights are only ever read by the engine on rebalance rows; ffill whole rows between them
    W = pd.DataFrame(rows, index=pd.DatetimeIndex(when), columns=px.columns)
    W = W.reindex(idx).ffill().fillna(0.0)
    return W, n_sel, n_cons, len(rb)


# ---------------------------------------------------------------- metrics helpers
def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def fmt(d):
    return (f"{d['CAGR']:.1%} | {d['Vol']:.1%} | {d['Sharpe']:.2f} | {d['MaxDD']:.1%} | "
            f"{d['H1']:.2f} / {d['H2']:.2f}")


def main():
    px = load_universe(broad=True)
    px = px.loc[:, px.notna().sum() > 500]
    print(f"panel {px.shape[0]} rows x {px.shape[1]} cols  {px.index[0].date()} -> {px.index[-1].date()}")

    ev_raw = load_events(px)
    print(f"8-K/2.02 events on the trading grid after {DEDUP_DAYS}d dedup: {len(ev_raw)} "
          f"across {ev_raw.ticker.nunique()} tickers "
          f"({ev_raw.event_date.min().date()} -> {ev_raw.event_date.max().date()})")

    ev = add_surprise(ev_raw, px, "maxabs")
    ev2 = add_surprise(ev_raw, px, "2day")
    print(f"events with a usable surprise: {len(ev)}   "
          f"mean |CAR| {ev.car.abs().mean():.2%}  sd {ev.car.std():.2%}")

    start = px.index[max(260, px.index.searchsorted(pd.Timestamp('2012-01-03')))]
    spy = px["SPY"].pct_change().fillna(0.0)
    base = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq="W")["returns"]

    grid = [(c, h) for c in ("tercile", "quintile") for h in (40, 60)]
    runs, first = {}, None
    for cut, hold in grid:
        W, n_sel, n_cons, n_rb = pead_weights(px, ev, cut, hold)
        res = backtest(px, W, cost_bps=COST_BPS, freq="W")
        live = W.sum(axis=1) > 0
        s0 = px.index[np.flatnonzero(live.values)[0]]
        first = s0 if first is None else max(first, s0)
        runs[(cut, hold)] = dict(r=res["returns"], turn=res["turnover"], W=W,
                                 n_sel=n_sel, n_cons=n_cons, s0=s0,
                                 avg_names=(W > 0).sum(axis=1)[live].mean())
    # controls (diagnostics, not grid points): the same machinery with the sort removed /
    # reversed, plus the literal 2-day-window surprise at the base config.
    for lab, evx, cut, hold in [("CONTROL all-announcers", ev, "all", 60),
                                ("CONTROL bottom-tercile", ev, "bottom", 60),
                                ("CONTROL mid-tercile", ev, "mid", 60),
                                ("SENS tercile 2day-CAR", ev2, "tercile", 60)]:
        Wc, _, _, _ = pead_weights(px, evx, cut, hold)
        rc = backtest(px, Wc, cost_bps=COST_BPS, freq="W")
        live = Wc.sum(axis=1) > 0
        runs[(lab, hold)] = dict(r=rc["returns"], turn=rc["turnover"], W=Wc, n_sel=0, n_cons=0,
                                 s0=px.index[np.flatnonzero(live.values)[0]],
                                 avg_names=(Wc > 0).sum(axis=1)[live].mean())

    smp = max(first, start)
    print(f"\ncommon sample: {smp.date()} -> {px.index[-1].date()}")
    print("\n## Full sample")
    print("| variant | CAGR | Vol | Sharpe | MaxDD | H1 / H2 | avg names | turnover |")
    print("|---|---|---|---|---|---|---|---|")
    rows = {}
    for k, v in runs.items():
        r = v["r"].loc[smp:]
        rows[k] = stats(r)
        tn = (v["turn"].loc[smp:].sum() / (len(r) / 252)) if v["turn"] is not None else np.nan
        print(f"| {k[0]} h={k[1]} | {fmt(rows[k])} | {v['avg_names']:.0f} | {tn:.1f}x |")
    for nm, r in (("RULES v1 baseline (broad)", base.loc[smp:]), ("SPY", spy.loc[smp:])):
        rows[nm] = stats(r)
        print(f"| {nm} | {fmt(rows[nm])} | — | — |")

    # ---- walk-forward, PROTOCOL rule 8 (shortened windows for this sample)
    IS = (smp, pd.Timestamp("2018-12-31")); OOS = (pd.Timestamp("2019-01-01"), px.index[-1])
    print(f"\n## Walk-forward  IS {IS[0].date()}–{IS[1].date()}  /  OOS {OOS[0].date()}–{OOS[1].date()}")
    print("Selection rule (pre-stated): highest IS Sharpe on the 4-point grid; ties -> wider cut, then shorter hold.")
    print("| variant | IS CAGR | IS Sharpe | IS MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD |")
    print("|---|---|---|---|---|---|---|")
    wf = {}
    for k in list(grid) + [("RULES v1 baseline (broad)", ""), ("SPY", "")]:
        r = (runs[k]["r"] if k in runs else (base if k[0].startswith("RULES") else spy))
        i, o = stats(r.loc[IS[0]:IS[1]]), stats(r.loc[OOS[0]:OOS[1]])
        wf[k] = (i, o)
        lab = f"{k[0]} h={k[1]}" if k[1] != "" else k[0]
        print(f"| {lab} | {i['CAGR']:.1%} | {i['Sharpe']:.2f} | {i['MaxDD']:.1%} | "
              f"{o['CAGR']:.1%} | {o['Sharpe']:.2f} | {o['MaxDD']:.1%} |")
    order = {"tercile": 0, "quintile": 1}
    pick = max(grid, key=lambda k: (round(wf[k][0]["Sharpe"], 6), -order[k[0]], -k[1]))
    print(f"\nIS pick -> {pick[0]} h={pick[1]}   OOS Sharpe {wf[pick][1]['Sharpe']:.2f} "
          f"vs baseline {wf[('RULES v1 baseline (broad)','')][1]['Sharpe']:.2f} "
          f"vs SPY {wf[('SPY','')][1]['Sharpe']:.2f}")

    # ---- KEEP tests
    b, s = rows["RULES v1 baseline (broad)"], rows["SPY"]
    print("\n## KEEP tests (PROTOCOL rule 4)")
    print("| variant | 4a H1>b | 4a H2>b | 4a DD | 4a | 4b H1>SPY | 4b H2>SPY | 4b OOS | 4b DD<=60% | 4b CAGR>=70% | 4b |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    verdicts = {}
    for k in grid:
        d = rows[k]
        a1, a2, a3 = d["H1"] > b["H1"], d["H2"] > b["H2"], d["MaxDD"] >= b["MaxDD"]
        oos_ok = wf[k][1]["Sharpe"] > wf[("SPY", "")][1]["Sharpe"]
        b1, b2 = d["H1"] > s["H1"], d["H2"] > s["H2"]
        b4, b5 = d["MaxDD"] >= 0.6 * s["MaxDD"], d["CAGR"] >= 0.7 * s["CAGR"]
        A, B = all([a1, a2, a3]), all([b1, b2, oos_ok, b4, b5])
        verdicts[k] = "KEEP-candidate" if (A or B) else "KILL"
        y = lambda x: "pass" if x else "FAIL"
        print(f"| {k[0]} h={k[1]} | {y(a1)} | {y(a2)} | {y(a3)} | {y(A)} | {y(b1)} | {y(b2)} | "
              f"{y(oos_ok)} | {y(b4)} | {y(b5)} | {y(B)} |")

    print("\n## LEADERBOARD rows")
    today = "2026-09-04"
    for k in grid:
        d = rows[k]
        print(f"| {today} | pead-{k[0]}-h{k[1]} | {d['CAGR']:.1%} | {d['Sharpe']:.2f} | "
              f"{d['MaxDD']:.1%} | {d['H1']:.2f} / {d['H2']:.2f} | "
              f"{b['Sharpe']:.2f} ({b['H1']:.2f}/{b['H2']:.2f}) | {verdicts[k]} | "
              f"research/backtests/2026-09-04_small-cap-pead.py |")

    # ---- extra diagnostics: does the surprise sort do anything at all?
    print("\n## Diagnostic: mean forward abnormal return by surprise tercile (event study)")
    idx = px.index
    for hz in (20, 40, 60):
        rec = []
        for tk, t, car in zip(ev.ticker.values, ev.t.values, ev.car.values):
            e, f = t + 1, min(t + 1 + hz, len(idx) - 1)
            p0, p1 = px[tk].iloc[e], px[tk].iloc[f]
            b0, b1 = px["SPY"].iloc[e], px["SPY"].iloc[f]
            if np.isfinite([p0, p1, b0, b1]).all():
                rec.append((car, (p1 / p0 - 1) - (b1 / b0 - 1)))
        d = pd.DataFrame(rec, columns=["car", "fwd"])
        d["ter"] = pd.qcut(d.car, 3, labels=["low", "mid", "high"])
        g = d.groupby("ter", observed=True).fwd.agg(["mean", "std", "count"])
        sp = g.loc["high", "mean"] - g.loc["low", "mean"]
        se = np.sqrt(g.loc["high", "std"] ** 2 / g.loc["high", "count"] +
                     g.loc["low", "std"] ** 2 / g.loc["low", "count"])
        print(f"  h={hz:2d}d  low {g.loc['low','mean']:+.2%}  mid {g.loc['mid','mean']:+.2%}  "
              f"high {g.loc['high','mean']:+.2%}  high-low {sp:+.2%}  t={sp/se:+.2f}  (n={len(d)})")
    print("\n(These are OVERLAPPING event windows, so the t-stats are optimistic; treat them as"
          " an upper bound on significance.)")


if __name__ == "__main__":
    main()
