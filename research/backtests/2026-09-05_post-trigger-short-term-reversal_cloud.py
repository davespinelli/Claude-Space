#!/usr/bin/env python3
"""Idea 125 — post-trigger-short-term-reversal   (research sprint, cloud lane, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 125)
    Idea 96 measured, as a BY-PRODUCT of killing a per-name trailing stop, that a name which
    has just broken 15%/25% off its trailing high earns +0.57% to +2.21% the NEXT DAY against
    an unconditional +0.06%/day (t +2.70..+10.37 on 4 of 6 book/panel cells, 9/12 overall,
    persisting +1.2..+2.6% over 5 days, 82-4889 events per cell).  That number is why idea 96's
    stop had the wrong sign.  This run asks whether it is a SIGNAL in its own right: buy the
    triggered names, equal weight, hold 1/5/10 days.

    The pre-registered prior AGAINST it (stated in the queue entry, not invented after the
    fact): the events cluster in crashes, so the book is long a falling knife precisely when
    the market is falling; a large mean daily return earned on a handful of violent days is
    not the same object as a Sharpe.  A KILL here is the expected result and is a result.

GRID — exactly TWO tuned parameters, every point reported
    D  in {0.15, 0.25}      trailing-high drawdown that fires the trigger
    H  in {1, 5, 10}        holding period in trading days
    x 3 panels (u56, broad, small) x 4 cost rungs {0, 10, 25, 50} bps x 2 sizing conventions.
    The sizing convention is NOT tuned: both are reported everywhere and rule 8 selects
    within a convention, never across.  6 arms x 2 conv x 4 costs x 3 panels = 144 rows.

CONSTRUCTION
    trigger_t(i)  = ( px/rollmax(px,252) - 1 <= -D )  AND  ( the same was FALSE at t-1 )
                    i.e. a FRESH crossing, so a name in a long grind does not re-fire daily.
    held_t(i)     = a trigger fired for i in [t-H+1, t].
    conv 'dgN10'  = w_i = 0.75 / max(n_t, 10)   -> de-grosses when few names fire (cash rest).
                    The floor 10 is pre-registered, inherited from the project's n>=~10 book
                    size convention, and never swept.
    conv 'rw'     = w_i = 0.75 / n_t            -> always fully invested when anything fired.
    Daily rebalance (freq='D'), weights decided at close t applied at t+1 (engine), long only,
    no leverage, no shorting.  Evaluation starts at px.index[260].  IS <= 2016-12-31,
    OOS >= 2017-01-01.  SPY is the benchmark and is excluded from the tradable set on every
    panel (so is any name the small-panel screen rejects).

CONTROLS (three, all on the identical index and cost rung)
    EWall  — equal-weight every panel name at 75% gross, the project's incumbent simple book.
    RULES v1 — the live paper book, weekly, via baseline.rules_v1_weights.
    SPY    — buy and hold.
    Plus the EVENT STUDY the whole idea rests on, re-measured here as a signal rather than as a
    stop by-product: mean forward 1/5/10-day return after a trigger vs the unconditional mean,
    with event counts, paired t-stats, an IS/OOS split, and a SPY-drawdown-state split that
    tests the queue's own "they cluster in crashes" prior directly.

KEEP PATHS (PROTOCOL rule 4, both evaluated)
    4a: Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
    4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.
RULE 8 walk-forward: (D,H) chosen by IS Sharpe on 2009-2016 alone, evaluated untouched on
    2017-2026 against EWall, RULES v1 and SPY.  Reported for every panel/cost/convention cell.

CAVEATS carried, not buried
    * Survivorship, and it bites THIS idea hardest.  All three panels are current-constituent
      lists; the small panel is the 483-name sub-$2B screen (data/SMALL_PANEL_README.md) and
      names that fell 25% off their high and then went to zero are ABSENT from it by
      construction.  A "buy the crash" signal is exactly the strategy that bias flatters, so
      any positive result here must be discounted and any KILL is, if anything, understated.
    * The small panel additionally drops the 44 tickers with max_1d_move >= 1.0 in
      data/small_meta.csv (bad splits), leaving 439 names, per the sprint's standing rule.
    * Idea 38's calendar-day-index warning is checked, not assumed: this run asserts the loaded
      index carries no weekend rows and no all-flat rows before reading any number (see
      CHECK (a)).  On the current caches it is clean, which matters because a 1-day holding
      period is the construction most exposed to ffilled non-trading rows.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_post-trigger-short-term-reversal_cloud"
OUT = ROOT / "research" / "backtests"

GROSS = 0.75
NFLOOR = 10                        # pre-registered de-gross floor, never swept
LOOKBACK = 252                     # trailing-high window, inherited from idea 96
DS = [0.15, 0.25]                  # tuned parameter 1
HS = [1, 5, 10]                    # tuned parameter 2
CONVS = ["dgN10", "rw"]
COSTS = [0.0, 10.0, 25.0, 50.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HORIZONS = [1, 5, 10]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


# ------------------------------------------------------------------ panels
def panel(which):
    """(prices incl. SPY, list of tradable names).  SPY is benchmark only, never tradable."""
    if which == "u56":
        px = load_universe()
    elif which == "broad":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
        px = px.drop(columns=[c for c in px.columns if c in bad])
    names = [c for c in px.columns if c != "SPY"]
    return px, names


def check_index(px, label):
    """Idea 38's warning, verified rather than assumed."""
    wk = int((px.index.dayofweek >= 5).sum())
    ch = px.pct_change()
    flat = int(((ch.abs() < 1e-12).sum(axis=1) / px.notna().sum(axis=1) > 0.7).sum())
    ok = (wk == 0 and flat == 0)
    print(f"CHECK (a) index {label}: {len(px)} rows, {len(px)/((px.index[-1]-px.index[0]).days/365.25):.1f}/yr, "
          f"weekend rows {wk}, >70%-flat rows {flat}  -> {'TRADING-DAY CLEAN' if ok else 'CALENDAR ARTEFACT PRESENT'}")
    return ok


# ------------------------------------------------------------------ signal
def triggers(px, names, D):
    """Fresh crossing below -D off the trailing 252d high."""
    p = px[names]
    dd = p / p.rolling(LOOKBACK).max() - 1.0
    below = (dd <= -D).fillna(False)
    return below & ~below.shift(1, fill_value=False)


def book(trig, H, conv):
    held = trig.rolling(H, min_periods=1).max().fillna(0.0) > 0.5
    n = held.sum(axis=1)
    if conv == "rw":
        den = n.replace(0, np.nan)
    else:
        den = n.clip(lower=NFLOOR).replace(0, np.nan)
    return held.astype(float).div(den, axis=0).fillna(0.0) * GROSS


def ewall(px, names):
    e = pd.DataFrame(1.0, index=px.index, columns=names).where(px[names].notna(), 0.0)
    return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


# ------------------------------------------------------------------ costs without re-running
def run_all_costs(px, W, freq, start):
    """engine.backtest charges cost outside the compounding loop, so one run serves every rung."""
    res = backtest(px, W.reindex(columns=px.columns).fillna(0.0), cost_bps=0.0, freq=freq)
    g, to = res["returns"].loc[start:], res["turnover"].loc[start:]
    return {c: g - to * c / 1e4 for c in COSTS}, float(to.sum() / (len(g) / 252.0)), res["weights"].loc[start:]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, soos=metrics(spy.loc[OOS_START:])["Sharpe"],
                dd=0.60 * abs(m["MaxDD"]), cagr=0.70 * m["CAGR"])


def stats(r, bars, v1r):
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    h1, h2 = halves(r)
    marg = dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=bars["dd"] - abs(m["MaxDD"]), CAGR=m["CAGR"] - bars["cagr"])
    fail = [k for k in ("H1", "H2", "OOS", "DD", "CAGR") if marg[k] <= 0]
    vh1, vh2 = halves(v1r)
    p4a = (h1 > vh1) and (h2 > vh2) and (m["MaxDD"] >= metrics(v1r)["MaxDD"])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                pass4a=bool(p4a), pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-")


# ------------------------------------------------------------------ event study
def event_study(px, names, spy, D, label):
    """The statistic idea 96 reported, re-measured as a signal.  No costs: diagnostic only."""
    p = px[names]
    ret = p.pct_change()
    trig = triggers(px, names, D)
    spy_dd = px["SPY"] / px["SPY"].cummax() - 1.0
    crash = (spy_dd <= -0.10)
    rows = []
    for h in HORIZONS:
        fwd = (p.shift(-h) / p - 1.0)                       # decided at t, earned t+1..t+h
        fwd = fwd.where(trig)
        uncond = (p.shift(-h) / p - 1.0)
        for seg, msk in (("full", pd.Series(True, index=px.index)),
                         ("IS", px.index <= IS_END), ("OOS", px.index >= OOS_START),
                         ("SPYdd<=-10%", crash), ("SPYdd>-10%", ~crash)):
            msk = pd.Series(np.asarray(msk), index=px.index)
            v = fwd[msk].stack().dropna()
            u = uncond[msk].stack().dropna()
            if len(v) < 20:
                continue
            t = float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))) if v.std(ddof=1) > 0 else np.nan
            rows.append(dict(panel=label, D=D, h=h, seg=seg, n_events=int(len(v)),
                             mean_pct=100 * float(v.mean()), uncond_pct=100 * float(u.mean()),
                             excess_pct=100 * float(v.mean() - u.mean()), t=t,
                             hit=float((v > 0).mean()), per_day_pct=100 * float(v.mean()) / h))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ one panel
def do_panel(which):
    px, names = panel(which)
    print("\n" + "=" * 200)
    print(f"PANEL {which}: {len(names)} tradable names + SPY benchmark | "
          f"{px.index[0].date()} -> {px.index[-1].date()}")
    check_index(px, which)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = bars_of(spy)
    ms = metrics(spy)
    print(f"eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY   CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS {bars['soos']:.3f}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f}(H1)/{bars['s2']:.3f}(H2)/{bars['soos']:.3f}(OOS), "
          f"MaxDD <= {bars['dd']:.2%}, CAGR >= {bars['cagr']:.2%}")

    # ---- event study
    ev = pd.concat([event_study(px, names, spy, D, which) for D in DS], ignore_index=True)
    print(f"\nEVENT STUDY {which} — forward return after a FRESH break of -D off the 252d high "
          f"(no costs, diagnostic)")
    print(ev.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- controls
    v1W = rules_v1_weights(px)                     # the live book, weekly, panel-native
    v1, v1_to, _ = run_all_costs(px, v1W, "W", start)
    ewW = ewall(px, names)
    ew, ew_to, _ = run_all_costs(px, ewW, "W", start)
    for c in (10.0,):
        print(f"controls @{c:.0f}bps: RULES v1 CAGR {metrics(v1[c])['CAGR']:.2%} Sharpe {metrics(v1[c])['Sharpe']:.3f} "
              f"MaxDD {metrics(v1[c])['MaxDD']:.2%} | EWall CAGR {metrics(ew[c])['CAGR']:.2%} "
              f"Sharpe {metrics(ew[c])['Sharpe']:.3f} MaxDD {metrics(ew[c])['MaxDD']:.2%}")

    rows, rets = [], {}
    for c in COSTS:
        for nm, r, to in (("EWall", ew[c], ew_to), ("RULESv1", v1[c], v1_to)):
            rows.append(dict(panel=which, cost=c, D=np.nan, H=np.nan, conv=nm, turn=to,
                             gross=np.nan, nheld=np.nan, **stats(r, bars, v1[c])))
    for D in DS:
        trig = triggers(px, names, D)
        ev_per_yr = float(trig.sum().sum() / (len(px.loc[start:]) / 252.0))
        for H in HS:
            for conv in CONVS:
                W = book(trig, H, conv)
                nets, to, held = run_all_costs(px, W, "D", start)
                gross_mean = float(held.sum(axis=1).mean())
                nheld = float((held > 1e-12).sum(axis=1).mean())
                for c in COSTS:
                    rets[(D, H, conv, c)] = nets[c]
                    rows.append(dict(panel=which, cost=c, D=D, H=H, conv=conv, turn=to,
                                     gross=gross_mean, nheld=nheld, ev_yr=ev_per_yr,
                                     **stats(nets[c], bars, v1[c])))
    df = pd.DataFrame(rows)
    cols = ["cost", "D", "H", "conv", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
            "OOS_CAGR", "OOS_MaxDD", "turn", "gross", "nheld", "pass4a", "pass4b", "fail4b"]
    print(f"\nGRID {which} — ALL {len(df)} rows (2 D x 3 H x 2 conv x 4 costs + 8 control rows)")
    print(df[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- rule 8
    print(f"\nRULE 8 WALK-FORWARD {which} — (D,H) chosen on IS Sharpe (<= {IS_END}) only, "
          f"evaluated untouched on {OOS_START}+")
    wf = []
    for c in COSTS:
        for conv in CONVS:
            cell = df[(df.cost == c) & (df.conv == conv)]
            if cell.empty:
                continue
            p = cell.sort_values("IS_Sharpe", ascending=False).iloc[0]
            ro = rets[(p.D, p.H, conv, c)].loc[OOS_START:]
            mo = metrics(ro)
            eo, vo, so = (metrics(ew[c].loc[OOS_START:]), metrics(v1[c].loc[OOS_START:]),
                          metrics(spy.loc[OOS_START:]))
            wf.append(dict(panel=which, cost=c, conv=conv, pick=f"D={p.D:.2f}/H={int(p.H)}",
                           IS_Sharpe=p.IS_Sharpe, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                           OOS_MaxDD=mo["MaxDD"],
                           OOS_rank=int((cell.OOS_Sharpe > mo["Sharpe"]).sum()) + 1, n_arms=len(cell),
                           beat_EWall=bool(mo["Sharpe"] > eo["Sharpe"]),
                           beat_v1=bool(mo["Sharpe"] > vo["Sharpe"]),
                           beat_SPY=bool(mo["Sharpe"] > so["Sharpe"]),
                           ew_CAGR=eo["CAGR"], ew_Sharpe=eo["Sharpe"], ew_MaxDD=eo["MaxDD"],
                           v1_CAGR=vo["CAGR"], v1_Sharpe=vo["Sharpe"], v1_MaxDD=vo["MaxDD"],
                           spy_CAGR=so["CAGR"], spy_Sharpe=so["Sharpe"], spy_MaxDD=so["MaxDD"]))
    W = pd.DataFrame(wf)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return df, W, ev


def main():
    print(__doc__)
    D, Wf, E = [], [], []
    for which in ("u56", "broad", "small"):
        d, w, e = do_panel(which)
        D.append(d); Wf.append(w); E.append(e)
    D = pd.concat(D, ignore_index=True); Wf = pd.concat(Wf, ignore_index=True)
    E = pd.concat(E, ignore_index=True)
    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    Wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    E.to_csv(OUT / f"{STEM}.eventstudy.csv", index=False)

    g = D[D.conv.isin(CONVS)]
    print("\n" + "=" * 200)
    print("SUMMARY")
    print(f"4b passes: {int(g.pass4b.sum())} of {len(g)} arm-rows.  "
          f"4a passes: {int(g.pass4a.sum())} of {len(g)}.")
    print(f"controls: EWall 4b {int(D[D.conv=='EWall'].pass4b.sum())}/{len(D[D.conv=='EWall'])}, "
          f"RULESv1 4b {int(D[D.conv=='RULESv1'].pass4b.sum())}/{len(D[D.conv=='RULESv1'])}")
    print("\nBEST arm by Sharpe in every (panel, cost, conv) cell — is any of them competitive?")
    b = (g.sort_values("Sharpe", ascending=False)
           .groupby(["panel", "cost", "conv"], as_index=False).first())
    print(b[["panel", "cost", "conv", "D", "H", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_Sharpe", "turn", "gross", "pass4a", "pass4b", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\nEVENT STUDY vs PORTFOLIO — the crash-clustering prior, per panel/D (h=1, full):")
    e1 = E[(E.h == 1)]
    for (pn, dd), s in e1.groupby(["panel", "D"]):
        f = s.set_index("seg")
        def cell(k, col):
            return f.loc[k, col] if k in f.index else np.nan
        print(f"  {pn:5s} D={dd:.2f}: full {cell('full','mean_pct'):+.3f}% (t {cell('full','t'):+.2f}, "
              f"n {int(cell('full','n_events'))})  |  in SPY dd<=-10%: {cell('SPYdd<=-10%','mean_pct'):+.3f}% "
              f"(n {int(cell('SPYdd<=-10%','n_events')) if not np.isnan(cell('SPYdd<=-10%','n_events')) else 0})  |  "
              f"outside: {cell('SPYdd>-10%','mean_pct'):+.3f}%  |  IS {cell('IS','mean_pct'):+.3f}% "
              f"vs OOS {cell('OOS','mean_pct'):+.3f}%")
    print("=" * 200)


if __name__ == "__main__":
    main()
