#!/usr/bin/env python3
"""QUEUE idea 117 — crisis-depth-as-the-price-denominator (lane B, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 97 found the gate tier prices at 4.108 in the IS window (SPY MaxDD -22.1%) and 0.404
OOS (SPY MaxDD -33.7%), i.e. every drawdown price this project has quoted is a regime reading
in disguise.  Price insurance per pp of MaxDD at MATCHED crisis depth (episode-level, using
idea 62's >10% drawdown episode classification) instead of whole-window MaxDD.  Max 2 params."

What is on trial.  Not a book — a STATISTIC.  Every drawdown price this project has published
(ideas 9, 22, 74, 94, 97, 119) is

    rate = (CAGR_control - CAGR_arm) / (|MaxDD_control| - |MaxDD_arm|)      pp CAGR per pp MaxDD

and its denominator is a WHOLE-WINDOW MaxDD difference.  Whole-window MaxDD is one number
produced by ONE episode — the window's deepest crisis — so the denominator is not a property
of the instrument, it is a property of the sample's worst crash.  A window whose worst crash
is shallow leaves little drawdown to buy, so every instrument looks dear in it; a window
containing 2020 leaves a lot, so everything looks cheap.  That is exactly idea 97's 4.108 ->
0.404, and if it is the whole story then no price in the project is comparable across windows.

The proposed replacement (the thing being tested)
    premium   = the annualised return give-up measured ONLY on CALM days (days outside every
                crisis episode).  This is what the insurance actually costs to carry.
    protect(e)= |MaxDD of the control inside episode e| - |MaxDD of the arm inside episode e|,
                in pp — what the instrument delivered in THAT crisis.
    ep_rate(e)= premium / protect(e)      pp of CAGR/yr paid in calm markets
                                          per pp of drawdown saved in crisis e
    depth-matched price = median ep_rate over the episodes of one DEPTH BIN.

The whole-window rate is (roughly) premium x (calm fraction correction) divided by the
protection delivered in the single deepest episode.  The episode form separates the two, so a
price can be quoted per crisis of a stated depth instead of per sample.

Episodes (idea 62's classification, built here because idea 62 is still Open)
    On SPY over each panel's evaluated slice: dd_t = eq_t / cummax(eq)_t - 1.  A maximal
    underwater run whose trough reaches -theta is an episode, with peak p (last day at the
    high), trough u, recovery v (first day back at the high, else sample end).
    depth = |dd at u| pp;  speed = FAST if p->u <= 60 trading days else SLOW (reported, never
    selected on).  Depth bins: SHALLOW [10,20) pp, DEEP >= 20 pp.
    An episode is IS if its trough <= 2016-12-31, else OOS.

Harness.  This run does NOT re-implement idea 94 or 97.  It imports idea 94's module directly
(`targets`, `run`, `price`, `ladder_slope`, `arm_specs`, `window`, `pass4a`, the gate
definitions) so every whole-window number is produced by the identical simulator, and it
asserts reproduction of idea 97's PUBLISHED headline (u56 gate tier 4.108 IS / 0.404 OOS
against levers 1.002 / 0.616) before anything else runs.  Only the episode layer is new.

Panels (3, all reported): u56 (universe.json, 56), broad (universe_broad.json, 136),
small (data/prices_small.csv.gz, 439 after holding SPY out and dropping the 44 names with
max_1d_move >= 1.0 in data/small_meta.csv — the convention of every small-panel run here).
Books: V1u, TOP20, EWall (idea 94's, ungated, 75% gross).  Costs 10 and 25 bps.
3 panels x 3 books x 2 costs = 18 cells, 17 arms + a 19-point gross ladder each.

Tuned parameters (PROTOCOL rule 4): TWO.
    (1) the episode depth threshold theta — the point is 10% (idea 62's wording); 8% and 15%
        are both run and ALL points reported, so the choice is visible rather than fitted.
    (2) the instrument family (tier) in the walk-forward selector, inherited from idea 94.
Everything else — band width 3%, stop depths 15/25, DD-control 8%/0.5, budgets, the 60-day
speed split, the 10/20 pp depth bins, the 0.10 pp priceability floor — is inherited or fixed
before any number was read, and reported.

Pre-registered predictions (written before any number was read)
    P1  The whole-window price is a regime reading: across windows, log(whole-window price)
        has a strongly NEGATIVE slope on log(window SPY MaxDD).  Idea 97's single pair implies
        a slope near -5.6; anything clearly negative confirms the premise.
    P2  The episode form removes most of it: median |log10(IS price / OOS price)| across arms
        falls by at least 2x going from the whole-window rate to the DEPTH-MATCHED episode
        rate.  This is the pre-registered bar for idea 117's proposal being worth a PROTOCOL
        clause; failing it is a KILL of the proposal, not of the premise.
    P3  Protection scales with crisis depth: pooled across episodes, protect(e) regressed on
        SPY episode depth has a positive slope with t > 2.  If it does, dividing by a
        whole-window MaxDD is literally dividing by a depth, which is the mechanism.
    P4  Sdepth (select on the IS depth-matched episode price) does NOT beat idea 94's S1 by
        much on OOS regret: the object being stabilised is the price's INTERPRETATION, not its
        ranking.  A large win here would be a surprise and would need its own replication.
    P5  No arm is a new 4b pass on all three panels (measurement run; 4a/4b computed and
        reported for every arm anyway, per PROTOCOL rule 4).

Execution realism (PROTOCOL rule 2): idea 94's simulator — weights decided at close t applied
at t+1, weekly rebalance, long-only, no leverage, costs charged inside the loop so the DD
state machine and the stop see NET equity.

SURVIVORSHIP: all three panels are current-constituent lists (idea 54).  Every level is
optimistic and the small panel worst of all, in the direction that FLATTERS gates (it excludes
the beaten-down names a gate would have sold).  Every number here is a within-cell, same-days
delta, which is far less exposed than a level, but no absolute CAGR should be quoted.

Calendar-day index (open idea 38) is unfixed for u56/broad and affects control and arms alike;
the small panel is trading-day indexed, so its window starts later (2011) and its IS window is
2010-2016.  Episode dates are therefore panel-specific and are printed per panel.

Deterministic, standalone.  Imports research/baseline.py and idea 94's module; modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_crisis-depth-as-the-price-denominator_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS, BOOKS, LADDER, PCOST = H.COSTS, H.BOOKS, H.LADDER, H.PCOST

# ---- pre-registered constants (fixed before any number was read) -------------------------
THETAS = [0.08, 0.10, 0.15]     # tuned parameter (1); 0.10 is the point, all reported
THETA0 = 0.10
FAST_DAYS = 60                  # peak->trough trading days: FAST vs SLOW (reported only)
DEPTH_BINS = [(0.0, 20.0, "SHALLOW"), (20.0, 1e9, "DEEP")]   # only boundary is 20 pp
FLOOR_PP = 0.10                 # idea 94's absolute priceability floor, pp of MaxDD
REL_FLOOR = 0.10                # idea 123's relative floor: protect >= 10% of control's depth
PANELS = ["u56", "broad", "small"]

TIER = {}
for g in H.GATES:
    for conv in ("dg", "rw"):
        TIER[f"{g}-{conv}"] = "T1_gate"
TIER["ddctl-8/.5/recover"] = "T3_ddctl"
TIER["ddctl-8/.5/high"] = "T3_ddctl"
TIER["stop15"] = "T4_stop"
TIER["stop25"] = "T4_stop"
TIER["ebud-0.10"] = "X_ebud"
TIER["ebud-0.20"] = "X_ebud"
RULE_TIERS = ["T1_gate", "T3_ddctl", "T4_stop"]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 6000)


# ---------------------------------------------------------------- panels
def panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def margins(r, bars):
    h1, h2 = halves(r)
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=0.60 * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - 0.70 * bars["scagr"])


def ols(x, y):
    """slope, intercept, t(slope), R2, n — plain OLS, finite pairs only."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 3 or np.ptp(x) == 0:
        return dict(slope=np.nan, icept=np.nan, t=np.nan, r2=np.nan, n=n)
    b, a = np.polyfit(x, y, 1)
    yh = a + b * x
    ss = float(((y - yh) ** 2).sum())
    se = np.sqrt(ss / (n - 2) / ((x - x.mean()) ** 2).sum()) if n > 2 else np.nan
    r2 = 1 - ss / float(((y - y.mean()) ** 2).sum()) if np.ptp(y) else np.nan
    return dict(slope=float(b), icept=float(a), t=float(b / se) if se else np.nan, r2=r2, n=n)


# ---------------------------------------------------------------- episodes (idea 62)
def spy_episodes(spy, theta):
    """Maximal underwater runs of SPY whose trough reaches -theta.  Returns a DataFrame."""
    eq = (1 + spy).cumprod()
    dd = eq / eq.cummax() - 1
    idx = dd.index
    under = (dd < -1e-12).values
    eps, i, n = [], 0, len(dd)
    while i < n:
        if not under[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and under[j + 1]:
            j += 1
        seg = dd.iloc[i:j + 1]
        depth = -float(seg.min()) * 100.0
        if depth >= theta * 100.0:
            p = idx[i - 1] if i > 0 else idx[0]
            u = seg.idxmin()
            recovered = (j + 1) < n
            v = idx[j + 1] if recovered else idx[n - 1]
            ip, iu, iv = idx.get_loc(p), idx.get_loc(u), idx.get_loc(v)
            eps.append(dict(peak=p, trough=u, recov=v, depth=depth,
                            dur_pt=int(iu - ip), dur_pr=int(iv - ip),
                            speed="FAST" if (iu - ip) <= FAST_DAYS else "SLOW",
                            bin=next(b for lo, hi, b in DEPTH_BINS if lo <= depth < hi),
                            window="IS" if u <= pd.Timestamp(IS_END) else "OOS",
                            recovered=recovered))
        i = j + 1
    E = pd.DataFrame(eps)
    if len(E):
        E["eid"] = [f"E{k+1}" for k in range(len(E))]
    return E


def calm_mask(index, E):
    """True on days OUTSIDE every episode [peak, recovery]."""
    m = pd.Series(True, index=index)
    for _, e in E.iterrows():
        m.loc[e.peak:e.recov] = False
    return m


def ann(r):
    """Geometric annualised return of a (possibly non-contiguous) day subset, 252 d/yr."""
    r = r.dropna()
    if len(r) < 21:
        return np.nan
    tot = float((1 + r).prod())
    if tot <= 0:
        return np.nan
    return tot ** (252.0 / len(r)) - 1.0


def win_maxdd(r, a, b):
    """MaxDD (negative fraction) of a return series inside [a, b], peak reset at a."""
    s = r.loc[a:b]
    if len(s) < 2:
        return 0.0
    eq = (1 + s).cumprod()
    return float((eq / eq.cummax() - 1).min())


# ---------------------------------------------------------------- verification
def verify(u56_tiers):
    """Reproduce idea 97's published headline before trusting anything below."""
    print("=" * 200)
    print("VERIFICATION — reproducing idea 94's simulator and idea 97's PUBLISHED headline")
    px = load_universe()
    start = px.index[260]
    worst = 0.0
    for b in BOOKS:
        W = H.targets(px, b)
        a = H.run(px, W, bps=PCOST)["r"].loc[start:]
        e = backtest(px, W, cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    print(f"  engine-equivalence (control vs engine.backtest @10bps, u56): max|diff| = {worst:.3e}"
          f"  ({'EXACT' if worst < 1e-12 else 'NOT EXACT — UNSAFE'})")
    r = H.run(px, H.targets(px, "EWall", "vol60", "dg"), bps=10.0)["r"].loc[start:]
    m = metrics(r)
    print(f"  idea 94 EWall+vol60-dg u56 @10bps: CAGR {m['CAGR']:.1%} (pub 11.6%)  "
          f"Sharpe {m['Sharpe']:.3f} (pub 1.133)  MaxDD {m['MaxDD']:.1%} (pub -16.9%)")
    ok_94 = abs(m["Sharpe"] - 1.133) < 5e-3 and worst < 1e-12
    got = {}
    for win, pub_t1, pub_t2 in (("IS", 4.108, 1.002), ("OOS", 0.404, 0.616)):
        s = u56_tiers[u56_tiers.window == win]
        got[win] = (float(s.T1_gate.median()), float(s.T2_lever.median()))
        print(f"  idea 97 u56 {win:3s} median tier price: T1_gate {got[win][0]:.3f} "
              f"(pub {pub_t1:.3f})   T2_lever {got[win][1]:.3f} (pub {pub_t2:.3f})")
    ok_97 = (abs(got["IS"][0] - 4.108) < 5e-3 and abs(got["IS"][1] - 1.002) < 5e-3
             and abs(got["OOS"][0] - 0.404) < 5e-3 and abs(got["OOS"][1] - 0.616) < 5e-3)
    print(f"  -> idea 94 harness {'REPRODUCED' if ok_94 else 'MISMATCH'}; "
          f"idea 97 headline {'REPRODUCED' if ok_97 else 'MISMATCH'}")
    print("=" * 200)
    return ok_94 and ok_97


# ---------------------------------------------------------------- one panel
def do_panel(pname):
    px, spy_full, label = panel(pname)
    start = px.index[260]
    spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
    bars = bars_of(spy)
    ms = metrics(spy)
    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}

    print("\n" + "=" * 200)
    print(f"PANEL {pname} — {label}: {px.shape[1]} holdable names, {px.index[0].date()} -> "
          f"{px.index[-1].date()} | eval from {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"  SPY CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS {bars['soos']:.3f}   |  "
          f"SPY MaxDD IS {metrics(spy.loc[:IS_END])['MaxDD']:.2%}  "
          f"OOS {metrics(spy.loc[OOS_START:])['MaxDD']:.2%}")
    print(f"  4b bars: Sharpe > {bars['s1']:.3f}/{bars['s2']:.3f}/{bars['soos']:.3f}, "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")

    # ---- episodes, all three thetas -----------------------------------------------------
    EPS = {}
    for th in THETAS:
        E = spy_episodes(spy, th)
        E.insert(0, "panel", pname)
        E.insert(1, "theta", th)
        EPS[th] = E
    E0 = EPS[THETA0]
    print(f"\n  SPY DRAWDOWN EPISODES on this panel's slice (theta = {THETA0:.0%}; "
          f"{len(E0)} episodes)")
    print(E0[["eid", "peak", "trough", "recov", "depth", "dur_pt", "dur_pr", "speed", "bin",
              "window", "recovered"]].to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    for th in THETAS:
        e = EPS[th]
        print(f"    theta {th:.0%}: {len(e)} episodes  "
              f"(IS {int((e.window=='IS').sum())} / OOS {int((e.window=='OOS').sum())}; "
              f"SHALLOW {int((e.bin=='SHALLOW').sum())} / DEEP {int((e.bin=='DEEP').sum())}; "
              f"calm days {int(calm_mask(spy.index, e).sum())}/{len(spy)})")

    # ---- simulate every arm + gross ladder ----------------------------------------------
    rows, rets, ladders = [], {}, {}
    for b in BOOKS:
        for c in COSTS:
            lad = []
            for m_ in LADDER:
                res = H.run(px, H.targets(px, b), m=m_, bps=c)
                r = res["r"].loc[start:]
                mm = metrics(r)
                lad.append(dict(m=m_, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"]))
            ladders[(b, c)] = pd.DataFrame(lad)
        for name, kind, kwargs, (g, conv) in H.arm_specs():
            W = H.targets(px, b, g, conv)
            for c in COSTS:
                res = H.run(px, W, bps=c, **kwargs)
                r = res["r"].loc[start:]
                rets[(b, name, c)] = r
                mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
                h1, h2 = halves(r)
                mg = margins(r, bars)
                rows.append(dict(
                    panel=pname, book=b, arm=name, tier=TIER.get(name, "-"), kind=kind, cost=c,
                    CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                    IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    TO=res["to"].loc[start:].sum() / mm["Years"],
                    gross=res["gross"].loc[start:].mean(),
                    m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                    p4b=all(v > 0 for v in mg.values()),
                    f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-",
                    p4a=H.pass4a(r, v1_net[c])))
    df = pd.DataFrame(rows)

    # ---- whole-window price list (idea 94's price(), unchanged) -------------------------
    out = []
    for b in BOOKS:
        for c in COSTS:
            L = ladders[(b, c)]
            slope = {w: H.ladder_slope(L, f"{p}MaxDD", f"{p}CAGR")
                     for w, p in (("full", ""), ("IS", "IS_"), ("OOS", "OOS_"))}
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in H.arm_specs():
                if name == "control":
                    continue
                ra = rets[(b, name, c)]
                pf = H.price(rc, ra, slope["full"])
                pi = H.price(H.window(rc, "IS"), H.window(ra, "IS"), slope["IS"])
                po = H.price(H.window(rc, "OOS"), H.window(ra, "OOS"), slope["OOS"])
                out.append(dict(
                    panel=pname, book=b, cost=c, arm=name, tier=TIER.get(name, "-"), kind=kind,
                    dCAGR=pf["dCAGR"], dMaxDD=pf["dMaxDD"], rate=pf["rate"], lever=slope["full"],
                    IS_lever=slope["IS"], OOS_lever=slope["OOS"], dSharpe=pf["dSharpe"],
                    IS_rate=pi["rate"], IS_dMaxDD=pi["dMaxDD"],
                    OOS_rate=po["rate"], OOS_dMaxDD=po["dMaxDD"]))
    P = pd.DataFrame(out)

    print(f"\nWHOLE-WINDOW PRICE LIST {pname} — idea 94's statistic, unchanged "
          f"({len(P)} arm-points, ALL reported)")
    print(P[["book", "cost", "arm", "tier", "dCAGR", "dMaxDD", "rate", "lever", "dSharpe",
             "IS_rate", "IS_dMaxDD", "OOS_rate", "OOS_dMaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- episode-level price ------------------------------------------------------------
    ep_rows = []
    for th in THETAS:
        E = EPS[th]
        if not len(E):
            continue
        cm = calm_mask(spy.index, E)
        for b in BOOKS:
            for c in COSTS:
                rc = rets[(b, "control", c)]
                ann_c = ann(rc[cm])
                for name, kind, _, _ in H.arm_specs():
                    if name == "control":
                        continue
                    ra = rets[(b, name, c)]
                    prem = (ann_c - ann(ra[cm])) * 100.0        # pp/yr paid on calm days
                    for _, e in E.iterrows():
                        ddc = abs(win_maxdd(rc, e.peak, e.trough)) * 100.0
                        dda = abs(win_maxdd(ra, e.peak, e.trough)) * 100.0
                        prot = ddc - dda
                        ok_abs = prot > FLOOR_PP
                        ok_rel = prot >= REL_FLOOR * ddc and prot > 0
                        ep_rows.append(dict(
                            panel=pname, theta=th, book=b, cost=c, arm=name,
                            tier=TIER.get(name, "-"), eid=e.eid, window=e.window, bin=e.bin,
                            speed=e.speed, depth=e.depth, dur_pt=e.dur_pt,
                            premium=prem, ctl_dd=ddc, arm_dd=dda, protect=prot,
                            prot_rel=prot / ddc if ddc > 0 else np.nan,
                            ep_rate=prem / prot if ok_abs else np.nan,
                            ep_rate_rel=prem / prot if ok_rel else np.nan))
    EP = pd.DataFrame(ep_rows)
    return dict(pname=pname, px=px, start=start, spy=spy, bars=bars, v1=v1_net,
                df=df, P=P, EP=EP, EPS=EPS, rets=rets)


# ---------------------------------------------------------------- analysis
def regime_reading(R):
    """P1: is the whole-window price a function of the window's own crisis depth?"""
    print("\n" + "=" * 200)
    print("P1 — IS THE WHOLE-WINDOW PRICE A REGIME READING?  log(price) vs log(window SPY MaxDD)")
    print("=" * 200)
    pts = []
    for pn, d in R.items():
        spy = d["spy"]
        depths = {"IS": abs(metrics(spy.loc[:IS_END])["MaxDD"]) * 100.0,
                  "OOS": abs(metrics(spy.loc[OOS_START:])["MaxDD"]) * 100.0,
                  "full": abs(metrics(spy)["MaxDD"]) * 100.0}
        for (b, c), g in d["P"].groupby(["book", "cost"]):
            for win, col in (("IS", "IS_rate"), ("OOS", "OOS_rate"), ("full", "rate")):
                v = g[col].values.astype(float)
                v = v[np.isfinite(v) & (v > 0)]
                if len(v) < 2:
                    continue
                pts.append(dict(panel=pn, book=b, cost=c, window=win, depth=depths[win],
                                med_price=float(np.median(v)), n=len(v)))
    D = pd.DataFrame(pts)
    print(D.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for scope in ["ALL"] + PANELS:
        s = D if scope == "ALL" else D[D.panel == scope]
        f = ols(np.log(s.depth.values), np.log(s.med_price.values))
        print(f"  {scope:6s}  slope {f['slope']:+.3f}  t {f['t']:+.2f}  R2 {f['r2']:.3f}  n {f['n']}"
              f"   (negative slope = deeper crisis in the window -> cheaper-looking insurance)")
    isr = D[D.window == "IS"].set_index(["panel", "book", "cost"]).med_price
    oor = D[D.window == "OOS"].set_index(["panel", "book", "cost"]).med_price
    j = isr.index.intersection(oor.index)
    ratio = (isr[j] / oor[j]).values
    print(f"\n  IS/OOS median-price ratio across the {len(j)} cells: median {np.median(ratio):.2f}x "
          f"(min {ratio.min():.2f}x, max {ratio.max():.2f}x).  Idea 97's published pair is 10.2x.")
    return D


def stability(R):
    """P2: does the episode form travel between windows better than the whole-window rate?"""
    print("\n" + "=" * 200)
    print("P2 — CROSS-WINDOW STABILITY OF THE PRICE (|log10(IS price / OOS price)|, per arm)")
    print("  whole  = idea 94/97's rate      ep_all = median episode rate over that window's")
    print("  episodes            ep_match = median over that window's episodes IN ONE DEPTH BIN")
    print("=" * 200)
    rows = []
    for pn, d in R.items():
        EP = d["EP"]
        EP = EP[EP.theta == THETA0]
        for (b, c, arm), g in EP.groupby(["book", "cost", "arm"]):
            w = d["P"][(d["P"].book == b) & (d["P"].cost == c) & (d["P"].arm == arm)].iloc[0]
            rec = dict(panel=pn, book=b, cost=c, arm=arm, tier=TIER.get(arm, "-"),
                       whole_IS=w.IS_rate, whole_OOS=w.OOS_rate)
            for tag, sub in (("ep_all", g), ("ep_match", g[g.bin == "SHALLOW"])):
                for win in ("IS", "OOS"):
                    v = sub[(sub.window == win)].ep_rate.values.astype(float)
                    v = v[np.isfinite(v)]
                    rec[f"{tag}_{win}"] = float(np.median(v)) if len(v) else np.nan
            for tag in ("whole", "ep_all", "ep_match"):
                a, bb = rec[f"{tag}_IS"], rec[f"{tag}_OOS"]
                rec[f"{tag}_lr"] = (abs(np.log10(a / bb)) if np.isfinite(a) and np.isfinite(bb)
                                    and a > 0 and bb > 0 else np.nan)
            rows.append(rec)
    S = pd.DataFrame(rows)
    print(S.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  median |log10(IS/OOS)| — lower is more portable between windows "
          "(0.30 = a 2x swing, 1.00 = 10x):")
    summary = {}
    for scope in ["ALL"] + PANELS:
        s = S if scope == "ALL" else S[S.panel == scope]
        vals = {t: float(np.nanmedian(s[f"{t}_lr"])) for t in ("whole", "ep_all", "ep_match")}
        ns = {t: int(np.isfinite(s[f"{t}_lr"]).sum()) for t in ("whole", "ep_all", "ep_match")}
        summary[scope] = vals
        print(f"    {scope:6s}  whole {vals['whole']:.3f} (n={ns['whole']})   "
              f"ep_all {vals['ep_all']:.3f} (n={ns['ep_all']})   "
              f"ep_match {vals['ep_match']:.3f} (n={ns['ep_match']})")
    a = summary["ALL"]
    ok = np.isfinite(a["ep_match"]) and np.isfinite(a["whole"]) and a["ep_match"] <= a["whole"] / 2
    print(f"\n  P2 pre-registered bar (ep_match <= whole/2 on ALL): "
          f"{a['ep_match']:.3f} vs {a['whole']/2:.3f} -> {'CONFIRMED' if ok else 'NOT CONFIRMED'}")
    # paired sign test, arm by arm
    m = S.dropna(subset=["whole_lr", "ep_match_lr"])
    print(f"  paired, arm by arm: ep_match more portable than whole in "
          f"{int((m.ep_match_lr < m.whole_lr).sum())}/{len(m)} arms")
    return S, ok


def depth_scaling(R):
    """P3: protection scales with the crisis's depth — the mechanism behind P1."""
    print("\n" + "=" * 200)
    print("P3 — DOES PROTECTION SCALE WITH CRISIS DEPTH?  protect(e) ~ SPY depth(e), pooled")
    print("=" * 200)
    EP = pd.concat([d["EP"] for d in R.values()], ignore_index=True)
    E0 = EP[EP.theta == THETA0]
    f = ols(E0.depth.values, E0.protect.values)
    print(f"  ALL arms      slope {f['slope']:+.4f} pp protection per pp of SPY depth  "
          f"t {f['t']:+.2f}  R2 {f['r2']:.3f}  n {f['n']}")
    for t in ("T1_gate", "T3_ddctl", "T4_stop", "X_ebud"):
        s = E0[E0.tier == t]
        ft = ols(s.depth.values, s.protect.values)
        print(f"  {t:10s}   slope {ft['slope']:+.4f}  t {ft['t']:+.2f}  R2 {ft['r2']:.3f}  n {ft['n']}")
    print("\n  Mean protection and price by depth bin x window (theta 10%, all panels/books/costs):")
    g = E0.groupby(["bin", "window"]).agg(
        n=("protect", "size"), mean_depth=("depth", "mean"), mean_ctl_dd=("ctl_dd", "mean"),
        mean_protect=("protect", "mean"), mean_prot_rel=("prot_rel", "mean"),
        med_ep_rate=("ep_rate", "median"), priced=("ep_rate", lambda v: int(np.isfinite(v).sum())))
    print(g.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  By speed (reported, never selected on):")
    g2 = E0.groupby(["speed", "window"]).agg(
        n=("protect", "size"), mean_depth=("depth", "mean"), mean_dur=("dur_pt", "mean"),
        mean_protect=("protect", "mean"), med_ep_rate=("ep_rate", "median"))
    print(g2.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  Per-episode summary across every arm (theta 10%):")
    g3 = E0.groupby(["panel", "eid", "window", "bin", "speed"]).agg(
        depth=("depth", "first"), dur_pt=("dur_pt", "first"), mean_ctl_dd=("ctl_dd", "mean"),
        mean_protect=("protect", "mean"), med_ep_rate=("ep_rate", "median"),
        priced=("ep_rate", lambda v: int(np.isfinite(v).sum())), n=("protect", "size"))
    print(g3.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  THETA SENSITIVITY (tuned parameter 1 — all points reported):")
    for th in THETAS:
        s = EP[EP.theta == th]
        print(f"    theta {th:.0%}: {s.eid.nunique()} episode ids, {len(s)} arm-episodes, "
              f"median protect {s.protect.median():+.3f} pp, median ep_rate "
              f"{s.ep_rate.median():.3f}, priced {int(np.isfinite(s.ep_rate).sum())}/{len(s)} "
              f"(abs floor)  {int(np.isfinite(s.ep_rate_rel).sum())}/{len(s)} (relative floor)")
    return E0


def walk_forward(R, S):
    """PROTOCOL rule 8.  S1 = idea 94's IS whole-window price.  Sdepth = IS episode price."""
    print("\n" + "=" * 200)
    print("RULE 8 WALK-FORWARD — selection on IS only (u56/broad 2009-2016, small 2010-2016), "
          "evaluated untouched on 2017-2026")
    print("  S1     = argmin IS whole-window rate, among arms with IS dMaxDD >= 1.0 pp "
          "(idea 94's selector)")
    print("  Sdepth = argmin IS depth-matched episode price (median ep_rate over IS SHALLOW "
          "episodes), among arms with median IS protect >= 1.0 pp")
    print("=" * 200)
    out = []
    for pn, d in R.items():
        P, EP, rets = d["P"], d["EP"][d["EP"].theta == THETA0], d["rets"]
        spy_o = metrics(d["spy"].loc[OOS_START:])
        for (b, c), cell in P.groupby(["book", "cost"]):
            v1_o = metrics(d["v1"][c].loc[OOS_START:])
            ctl_o = metrics(rets[(b, "control", c)].loc[OOS_START:])
            oos_ranked = cell[np.isfinite(cell.OOS_rate) & (cell.OOS_dMaxDD >= 1.0)] \
                .sort_values("OOS_rate")
            best = float(oos_ranked.OOS_rate.iloc[0]) if len(oos_ranked) else np.nan
            ranked = oos_ranked.arm.tolist()
            rec = dict(panel=pn, book=b, cost=c, n_oos=len(ranked),
                       ctl_CAGR=ctl_o["CAGR"], ctl_Sharpe=ctl_o["Sharpe"], ctl_MaxDD=ctl_o["MaxDD"],
                       v1_Sharpe=v1_o["Sharpe"], v1_CAGR=v1_o["CAGR"],
                       spy_Sharpe=spy_o["Sharpe"], spy_CAGR=spy_o["CAGR"], spy_MaxDD=spy_o["MaxDD"])
            picks = {}
            e1 = cell[(cell.IS_dMaxDD >= 1.0) & np.isfinite(cell.IS_rate)]
            if len(e1):
                picks["S1"] = e1.sort_values("IS_rate").iloc[0].arm
            sub = EP[(EP.book == b) & (EP.cost == c) & (EP.window == "IS") & (EP.bin == "SHALLOW")]
            if len(sub):
                agg = sub.groupby("arm").agg(prot=("protect", "median"),
                                             rate=("ep_rate", "median")).dropna()
                agg = agg[agg.prot >= 1.0]
                if len(agg):
                    picks["Sdepth"] = agg.sort_values("rate").index[0]
            for tag in ("S1", "Sdepth"):
                a = picks.get(tag)
                if a is None:
                    rec.update({f"{tag}_pick": "NOTHING", f"{tag}_OOSrank": np.nan,
                                f"{tag}_OOSrate": np.nan, f"{tag}_regret": np.nan,
                                f"{tag}_OOS_CAGR": np.nan, f"{tag}_OOS_Sharpe": np.nan,
                                f"{tag}_OOS_MaxDD": np.nan, f"{tag}_p4a": False,
                                f"{tag}_p4b": False})
                    continue
                ro = rets[(b, a, c)].loc[OOS_START:]
                mo = metrics(ro)
                rr = float(cell[cell.arm == a].OOS_rate.iloc[0])
                gr = d["df"]
                grow = gr[(gr.book == b) & (gr.cost == c) & (gr.arm == a)].iloc[0]
                rec.update({f"{tag}_pick": a,
                            f"{tag}_OOSrank": (ranked.index(a) + 1) if a in ranked else np.nan,
                            f"{tag}_OOSrate": rr,
                            f"{tag}_regret": (rr - best) if np.isfinite(rr) and np.isfinite(best) else np.nan,
                            f"{tag}_OOS_CAGR": mo["CAGR"], f"{tag}_OOS_Sharpe": mo["Sharpe"],
                            f"{tag}_OOS_MaxDD": mo["MaxDD"], f"{tag}_p4a": bool(grow.p4a),
                            f"{tag}_p4b": bool(grow.p4b)})
            rec["same_pick"] = rec["S1_pick"] == rec["Sdepth_pick"]
            out.append(rec)
    W = pd.DataFrame(out)
    print(W[["panel", "book", "cost", "S1_pick", "S1_OOSrank", "S1_OOSrate", "S1_regret",
             "S1_OOS_CAGR", "S1_OOS_Sharpe", "S1_OOS_MaxDD", "Sdepth_pick", "Sdepth_OOSrank",
             "Sdepth_OOSrate", "Sdepth_regret", "Sdepth_OOS_CAGR", "Sdepth_OOS_Sharpe",
             "Sdepth_OOS_MaxDD", "same_pick", "ctl_Sharpe", "v1_Sharpe", "spy_Sharpe"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  OOS regret (whole-window rate units; 0 = landed on the OOS-cheapest arm):")
    for pn in ["ALL"] + PANELS:
        s = W if pn == "ALL" else W[W.panel == pn]
        print(f"    {pn:6s}  S1 mean {s.S1_regret.mean():+.3f} median {s.S1_regret.median():+.3f}"
              f"  |  Sdepth mean {s.Sdepth_regret.mean():+.3f} median {s.Sdepth_regret.median():+.3f}"
              f"  |  rank-1 S1 {int((s.S1_OOSrank == 1).sum())}/{len(s)} "
              f"Sdepth {int((s.Sdepth_OOSrank == 1).sum())}/{len(s)}"
              f"  |  same pick {int(s.same_pick.sum())}/{len(s)}"
              f"  |  dOOS Sharpe (Sdepth-S1) {(s.Sdepth_OOS_Sharpe - s.S1_OOS_Sharpe).mean():+.3f}")
    print("\n  OOS of the picks vs the benchmarks (mean across the 18 cells):")
    for tag in ("S1", "Sdepth"):
        print(f"    {tag:7s} OOS CAGR {W[f'{tag}_OOS_CAGR'].mean():.2%}  "
              f"Sharpe {W[f'{tag}_OOS_Sharpe'].mean():.3f}  MaxDD {W[f'{tag}_OOS_MaxDD'].mean():.2%}"
              f"   |  4a {int(W[f'{tag}_p4a'].sum())}/{len(W)}  4b {int(W[f'{tag}_p4b'].sum())}/{len(W)}")
    print(f"    control OOS CAGR {W.ctl_CAGR.mean():.2%}  Sharpe {W.ctl_Sharpe.mean():.3f}  "
          f"MaxDD {W.ctl_MaxDD.mean():.2%}")
    print(f"    RULES v1 OOS CAGR {W.v1_CAGR.mean():.2%}  Sharpe {W.v1_Sharpe.mean():.3f}")
    print(f"    SPY      OOS CAGR {W.spy_CAGR.mean():.2%}  Sharpe {W.spy_Sharpe.mean():.3f}  "
          f"MaxDD {W.spy_MaxDD.mean():.2%}")
    return W


# ---------------------------------------------------------------- main
def main():
    R = {}
    for pn in PANELS:
        R[pn] = do_panel(pn)

    A = pd.concat([d["df"] for d in R.values()], ignore_index=True)
    P = pd.concat([d["P"] for d in R.values()], ignore_index=True)
    EP = pd.concat([d["EP"] for d in R.values()], ignore_index=True)
    E = pd.concat([e for d in R.values() for e in d["EPS"].values()], ignore_index=True)

    # idea 97's tier table on u56, for the verification anchor
    tp = []
    for (b, c), g in P[P.panel == "u56"].groupby(["book", "cost"]):
        for win, rc, lc in (("full", "rate", "lever"), ("IS", "IS_rate", "IS_lever"),
                            ("OOS", "OOS_rate", "OOS_lever")):
            v = g.loc[g.tier == "T1_gate", rc]
            v = v[np.isfinite(v)]
            tp.append(dict(book=b, cost=c, window=win, T2_lever=float(g[lc].iloc[0]),
                           T1_gate=float(v.median()) if len(v) else np.nan))
    ok = verify(pd.DataFrame(tp))

    print("\nFULL GRID — every arm-point, ALL reported "
          f"({len(A)} rows = 3 panels x 3 books x {len(H.arm_specs())} arms x {len(COSTS)} costs)")
    print(A[["panel", "book", "arm", "tier", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "p4a", "p4b", "f4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    D = regime_reading(R)
    S, p2ok = stability(R)
    E0 = depth_scaling(R)
    W = walk_forward(R, S)

    for name, obj in (("grid", A), ("pricelist", P), ("episodes", E), ("epprice", EP),
                      ("stability", S), ("regime", D), ("walkforward", W)):
        obj.to_csv(OUT / f"{STEM}.{name}.csv", index=False)

    # ---------------- KEEP paths ----------------
    print("\n" + "=" * 200)
    print("KEEP PATHS 4a AND 4b — every arm, both paths, all reported")
    print("=" * 200)
    for c in COSTS:
        s = A[A.cost == c]
        print(f"  @{c:.0f} bps  4a passes: " + "; ".join(
            f"{pn}: {sorted(set(s[(s.panel==pn) & s.p4a].arm)) or 'none'}" for pn in PANELS))
        print(f"  @{c:.0f} bps  4b passes: " + "; ".join(
            f"{pn}: {sorted(set(s[(s.panel==pn) & s.p4b].arm)) or 'none'}" for pn in PANELS))
    b3 = A[(A.cost == PCOST) & A.p4b].groupby("arm").panel.nunique()
    print(f"  arms passing 4b on ALL THREE panels @10bps: {sorted(b3[b3 == 3].index) or 'none'}")
    print(f"  binding 4b constraint counts @10bps: "
          f"{A[(A.cost==PCOST) & ~A.p4b].f4b.value_counts().head(8).to_dict()}")

    # ---------------- scorecard ----------------
    print("\n" + "=" * 200)
    print("PREDICTION SCORECARD")
    print("=" * 200)
    f_all = ols(np.log(D.depth.values), np.log(D.med_price.values))
    print(f"  P1 whole-window price is a regime reading: log-log slope {f_all['slope']:+.3f} "
          f"(t {f_all['t']:+.2f}, R2 {f_all['r2']:.3f}, n {f_all['n']}) -> "
          f"{'CONFIRMED' if (f_all['slope'] < 0 and abs(f_all['t']) > 2) else 'NOT CONFIRMED'}")
    print(f"  P2 depth-matched episode price at least 2x more portable across windows -> "
          f"{'CONFIRMED' if p2ok else 'NOT CONFIRMED'}")
    f3 = ols(E0.depth.values, E0.protect.values)
    print(f"  P3 protection scales with depth: slope {f3['slope']:+.4f} t {f3['t']:+.2f} -> "
          f"{'CONFIRMED' if (f3['slope'] > 0 and f3['t'] > 2) else 'NOT CONFIRMED'}")
    dreg = W.Sdepth_regret.mean() - W.S1_regret.mean()
    print(f"  P4 Sdepth does not materially beat S1: mean regret Sdepth {W.Sdepth_regret.mean():+.3f}"
          f" vs S1 {W.S1_regret.mean():+.3f} (diff {dreg:+.3f}), same pick "
          f"{int(W.same_pick.sum())}/{len(W)} -> "
          f"{'CONFIRMED (no material win)' if dreg > -0.10 else 'REFUTED (Sdepth wins)'}")
    print(f"  P5 arms passing 4b on all three panels @10bps: {sorted(b3[b3 == 3].index) or 'none'} -> "
          f"{'CONFIRMED' if not len(b3[b3 == 3]) else 'REFUTED'}")
    print(f"\n  harness verification: {'REPRODUCED idea 94 + idea 97' if ok else 'MISMATCH — do not cite'}")
    print(f"\nWrote {STEM}.{{grid,pricelist,episodes,epprice,stability,regime,walkforward}}.csv")


if __name__ == "__main__":
    main()
