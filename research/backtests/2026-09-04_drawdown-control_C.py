#!/usr/bin/env python3
"""QUEUE idea 22 — drawdown-control (lane C, 2026-09-04).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"v1 with book-level rule: if book drawdown > 8%, halve exposure until new high."

Idea 40 (lane B) already reported this MECHANISM as a KILL, but it did so on a different
book (lane A's no-`/sqrt(vol20)` top-n book), at only three thresholds, at a single cut
depth (halve), with a single reset rule, and — the gap this run exists to close — WITHOUT
the control that idea 66 later made mandatory: **gross exposure is an exact lever with zero
Sharpe content**, so any rule that spends most of its life at reduced exposure is a
de-grossing in disguise and must be judged against a STATIC book at the same average gross,
not against the un-cut book.  Idea 74 then asked for every drawdown instrument to be priced
on one axis: pp of CAGR surrendered per pp of MaxDD bought.  This run does the idea as
worded, on the live book it was written for, and prices it on that axis.

Books (pre-chosen, NEVER selected; all reported)
    V1      RULES v1 exactly as live: top-5 by the composite WITH /sqrt(vol20), 200d gate,
            vol20 < 0.60, fixed 15% per name, weekly.  This is idea 22's literal subject.
    CAND20  idea 2's standing 4b KEEP-candidate: top-20 eligible by the composite WITHOUT
            /sqrt(vol20), equal weight at 0.75/20, cash when E_t < 20.
    EWall   idea 72 / idea 10's `B136/EWall`: equal-weight EVERY eligible name at 75% gross,
            no ranking.  The simplest 4b-passing book the project has.
Universes: universe.json (56 names) and universe_broad.json (136).  Both always reported.

Tuned parameters (PROTOCOL rule 4: at most two).  Exactly two:
    D in {4, 6, 8, 10, 12, 15} %   drawdown trigger (8% is idea 22's literal value)
    k in {0.00, 0.25, 0.50, 0.75}  exposure multiplier while triggered (0.50 = "halve")
RESET is an ARM, not a tuned parameter — both variants are run and reported in full, and the
walk-forward selects WITHIN each reset arm separately so no selection ever spans three dials:
    high     idea 22 as worded: stay cut until the book makes a NEW EQUITY HIGH.
    recover  release when the drawdown has recovered to shallower than D/2.
Costs 5 / 10 / 25 bps are reported for every point; 10 bps is the PROTOCOL point and the
one every selection uses.  6 cells x (48 treated + 1 control) x 3 costs = 882 points, ALL
printed and written to the .grid.csv.

The decisive control (this is the part idea 40 did not run)
-----------------------------------------------------------
For every treated arm we measure its realised average gross exposure and compare it against
a STATIC-gross ladder of the same book on the same days (multiplier m = 0.10..1.00 step
0.05, no drawdown rule at all).  Two numbers come out of that:
    rate_DD     = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)   pp CAGR per pp MaxDD
    rate_gross  = the same ratio along the static ladder in the same cell (OLS slope)
If rate_DD >= rate_gross the drawdown rule is DOMINATED — a constant, parameter-free, path
independent cut buys the same drawdown more cheaply — and the rule has no content beyond
being a slow, state-dependent way of holding less.  Falsified if any arm buys drawdown
materially more cheaply than the static lever AND does so at equal or better Sharpe.

Pre-registered predictions (written before any number below was read)
    P1  The rule is Sharpe-negative in the large majority of arms (idea 40 saw 9/9 worse).
    P2  The `high` reset spends most of its days cut (idea 40: 52-79%), because cutting
        exposure slows the recovery that is required to un-cut it — a de-levering ratchet.
        The `recover` reset should not have that pathology.
    P3  rate_DD >= rate_gross for the large majority of arms (the instrument is dominated).
    P4  No arm converts a 4b failure into a 4b pass on BOTH universes.

Walk-forward (PROTOCOL rule 8), selection rules fixed before any OOS number was read
    S1  argmax IS (2009-2016) Sharpe over the arms of that cell+reset, control included.
    S2  4b-aware: among arms clearing the IS-window 4b bars (both IS halves' Sharpe > SPY's,
        IS MaxDD <= 60% of SPY's IS MaxDD, IS CAGR >= 70% of SPY's IS CAGR), argmax IS
        Sharpe; if none clears, the rule PICKS NOTHING and that is reported as such.
    Both evaluated untouched on 2017-2026 against the control, RULES v1 and SPY.

Execution realism (PROTOCOL rule 2): weights decided at close t are applied at t+1, weekly
rebalance, long-only, no leverage, costs on realised turnover.  The drawdown state machine
reads the book's own NET equity through close t-1 only — no look-ahead.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every
absolute CAGR is optimistic.  This run compares arms sharing a panel and the same days, so
the treatment deltas — which are the result — are far less exposed than the levels.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-04_drawdown-control_C"
FREQ, MAX_VOL, GROSS, NCAND = "W", 0.60, 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DTRIG = [0.04, 0.06, 0.08, 0.10, 0.12, 0.15]
KCUT = [0.00, 0.25, 0.50, 0.75]
RESETS = ["high", "recover"]
COSTS = [5, 10, 25]
PCOST = 10.0
BOOKS = ["V1", "CAND20", "EWall"]
LADDER = np.round(np.arange(0.10, 1.001, 0.05), 2)

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 1200)


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def targets(px, book):
    """Target weight matrix at the book's PUBLISHED exposure (multiplier m = 1.0)."""
    if book == "V1":
        return rules_v1_weights(px)                      # top-5, 15% each, WITH vol scaler
    vol = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = ((vol < MAX_VOL) & (px > px.rolling(200).mean())).fillna(False)
    if book == "EWall":
        e = elig.astype(float)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    return (rank <= NCAND).astype(float) * (GROSS / NCAND)   # literal: cash when E_t < 20


# ---------------------------------------------------------------- simulation
def run(px, W, m=1.0, D=None, k=1.0, reset="high", bps=PCOST):
    """One arm, costs applied inside the loop so the drawdown state machine sees NET equity.

    D=None -> no drawdown rule (the control / static-gross ladder).  Otherwise: at each
    rebalance the target is multiplied by k while the state machine is ARMED.  ARM when the
    book's net equity through the PREVIOUS close is more than D below its running peak;
    DISARM at a new equity high (`high`) or when the drawdown is shallower than D/2
    (`recover`).  The peak tracks the realised equity of THIS arm, as a live rule would.
    """
    rets = px.pct_change().fillna(0.0).values
    tgt_all = (W.reindex(px.index).fillna(0.0) * m).values
    mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
    n, ncol = rets.shape
    cur = np.zeros(ncol)
    held = np.zeros((n, ncol))
    turn = np.zeros(n)
    gross_s = np.zeros(n)
    cut = np.zeros(n, dtype=bool)
    eq, peak, armed, episodes = 1.0, 1.0, False, 0
    for i in range(n):
        if mask[i] and i > 0:
            if D is not None:
                dd = eq / peak - 1.0                      # equity through close i-1
                if not armed and dd < -D:
                    armed, episodes = True, episodes + 1
                elif armed and (dd >= 0.0 if reset == "high" else dd > -D / 2.0):
                    armed = False
            new = tgt_all[i - 1] * (k if armed else 1.0)
            s = new.sum()
            if s > 1.0:
                new = new / s
            turn[i] = np.abs(new - cur).sum()
            cur = new
        cut[i] = armed
        held[i] = cur
        gross_s[i] = cur.sum()
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp)
        peak = max(peak, eq)
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r = pd.Series((held * rets).sum(axis=1), index=px.index) - pd.Series(turn, index=px.index) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=px.index), gross=pd.Series(gross_s, index=px.index),
                cut=pd.Series(cut, index=px.index), episodes=episodes)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy, oos=True):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if oos else np.nan)


def margins(r, bars):
    """The five 4b margins in natural units.  Positive = cleared."""
    h1, h2 = halves(r)
    m = metrics(r)
    mo = metrics(r.loc[OOS_START:])
    return dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=0.60 * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - 0.70 * bars["scagr"])


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# ---------------------------------------------------------------- one universe
def do_universe(uname, kw):
    px = load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = bars_of(spy)
    ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
    W = {b: targets(px, b) for b in BOOKS}

    print("\n" + "=" * 210)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS Sharpe {bars['soos']:.3f}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f} (H1) / {bars['s2']:.3f} (H2) / {bars['soos']:.3f} (OOS), "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    print("=" * 210)

    # ---- harness sanity: the control must reproduce engine.backtest to machine precision
    worst = 0.0
    for b in BOOKS:
        a = run(px, W[b], D=None, bps=PCOST)["r"].loc[start:]
        e = backtest(px, W[b], cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    print(f"ENGINE-EQUIVALENCE (control vs engine.backtest at {PCOST:.0f} bps): max|diff| = {worst:.3e} "
          f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — results below are unsafe'})")

    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}

    # ---- all arms
    arms, rows = {}, []
    for b in BOOKS:
        for c in COSTS:
            ctl = run(px, W[b], D=None, bps=c)
            specs = [("ctl", None, 1.0, "-")] + [("dd", D, k, rs) for rs in RESETS
                                                 for D in DTRIG for k in KCUT]
            for kind, D, k, rs in specs:
                res = ctl if kind == "ctl" else run(px, W[b], D=D, k=k, reset=rs, bps=c)
                r = res["r"].loc[start:]
                if c == PCOST:
                    arms[(b, D, k, rs)] = r
                m, mo = metrics(r), metrics(r.loc[OOS_START:])
                h1, h2 = halves(r)
                mg = margins(r, bars)
                yrs = m["Years"]
                yr = (1 + r).groupby(r.index.year).prod() - 1
                rows.append(dict(
                    uni=uname, book=b, cost=c, arm=("control" if kind == "ctl" else
                                                    f"D{D:.0%}/k{k:.2f}/{rs}"),
                    D=(np.nan if D is None else D), k=k, reset=rs,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                    H1=h1, H2=h2,
                    IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    TO=res["to"].loc[start:].sum() / yrs,
                    gross=res["gross"].loc[start:].mean(),
                    cut_days=res["cut"].loc[start:].mean(), episodes=res["episodes"],
                    y2020=yr.get(2020, np.nan), y2022=yr.get(2022, np.nan),
                    m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                    p4b=all(v > 0 for v in mg.values()),
                    f4b=",".join([kk for kk, v in mg.items() if not v > 0]) or "-",
                    p4a=pass4a(r, v1_net[c])))
    df = pd.DataFrame(rows)

    # ---- static-gross ladder (the decisive control)
    lad = []
    for b in BOOKS:
        for m_ in LADDER:
            res = run(px, W[b], m=m_, D=None, bps=PCOST)
            r = res["r"].loc[start:]
            mm = metrics(r)
            h1, h2 = halves(r)
            mg = margins(r, bars)
            lad.append(dict(uni=uname, book=b, m=m_, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                            MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                            OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                            gross=res["gross"].loc[start:].mean(),
                            TO=res["to"].loc[start:].sum() / mm["Years"],
                            p4b=all(v > 0 for v in mg.values())))
    L = pd.DataFrame(lad)

    print(f"\nFULL GRID {uname} — {len(df)} points, ALL reported "
          f"(3 books x [1 control + {len(RESETS)*len(DTRIG)*len(KCUT)} treated] x {len(COSTS)} costs)")
    cols = ["book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "cut_days", "episodes",
            "y2020", "y2022", "p4a", "p4b", "f4b"]
    print(df.sort_values(["book", "cost", "reset", "D", "k"])[cols].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))

    print(f"\nSTATIC-GROSS LADDER {uname} — {len(L)} points, ALL reported (no drawdown rule)")
    print(L.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return px, df, L, bars, spy, v1_net, arms


# ---------------------------------------------------------------- analysis
def exchange_rates(df, L, uname):
    """pp of CAGR surrendered per pp of MaxDD bought, DD rule vs the static gross lever."""
    at = df[(df.cost == PCOST)]
    out, slopes = [], {}
    for b in BOOKS:
        lad = L[L.book == b].sort_values("m")
        x = lad.MaxDD.abs().values * 100.0
        y = lad.CAGR.values * 100.0
        slopes[b] = float(np.polyfit(x, y, 1)[0])       # pp CAGR gained per pp MaxDD accepted
        c0 = at[(at.book == b) & (at.arm == "control")].iloc[0]
        for _, r in at[(at.book == b) & (at.arm != "control")].iterrows():
            dcagr = (c0.CAGR - r.CAGR) * 100.0           # pp of CAGR given up
            ddd = (abs(c0.MaxDD) - abs(r.MaxDD)) * 100.0  # pp of MaxDD bought
            # nearest static-gross point at the SAME realised average gross
            j = (lad.gross - r.gross).abs().idxmin()
            mg = lad.loc[j]
            out.append(dict(uni=uname, book=b, arm=r.arm, reset=r.reset, D=r.D, k=r.k,
                            dCAGR=dcagr, dMaxDD=ddd,
                            rate_DD=(dcagr / ddd if ddd > 1e-9 else np.nan),
                            rate_gross=slopes[b], dominated=(dcagr / ddd >= slopes[b]) if ddd > 1e-9 else True,
                            dSharpe=r.Sharpe - c0.Sharpe,
                            gross=r.gross, gm_m=mg.m, gm_gross=mg.gross,
                            gm_CAGR=mg.CAGR, gm_MaxDD=mg.MaxDD, gm_Sharpe=mg.Sharpe,
                            vs_gm_CAGR=r.CAGR - mg.CAGR, vs_gm_MaxDD=abs(mg.MaxDD) - abs(r.MaxDD),
                            vs_gm_Sharpe=r.Sharpe - mg.Sharpe,
                            p4b=r.p4b, ctl_p4b=c0.p4b))
    return pd.DataFrame(out), slopes


def walk_forward(uname, arms, bars, spy, v1_net):
    """Rule 8.  Selection WITHIN each reset arm (2 tuned params), control always eligible."""
    is_bars = bars_of(spy.loc[:IS_END], oos=False)
    recs = []
    for (b, D, k, rs), r in arms.items():
        ris = r.loc[:IS_END]
        m = metrics(ris)
        h1, h2 = halves(ris)
        recs.append(dict(book=b, D=D, k=k, reset=rs,
                         arm=("control" if D is None else f"D{D:.0%}/k{k:.2f}/{rs}"),
                         IS_Sharpe=m["Sharpe"],
                         i_H1=h1 - is_bars["s1"], i_H2=h2 - is_bars["s2"],
                         i_DD=0.60 * abs(is_bars["sdd"]) - abs(m["MaxDD"]),
                         i_CAGR=m["CAGR"] - 0.70 * is_bars["scagr"]))
    I = pd.DataFrame(recs)
    spy_o, v1_o = metrics(spy.loc[OOS_START:]), metrics(v1_net[PCOST].loc[OOS_START:])
    rows = []
    for b in BOOKS:
        for rs in RESETS:
            pool = I[(I.book == b) & ((I.reset == rs) | (I.D.isna()))]
            ctl = I[(I.book == b) & (I.D.isna())].iloc[0]
            s1 = pool.sort_values(["IS_Sharpe", "D", "k"], ascending=[False, False, False]).iloc[0]
            ok = pool[(pool.i_H1 > 0) & (pool.i_H2 > 0) & (pool.i_DD > 0) & (pool.i_CAGR > 0)]
            s2 = (ok.sort_values(["IS_Sharpe", "D", "k"], ascending=[False, False, False]).iloc[0]
                  if len(ok) else None)
            for lbl, sel in (("CTL", ctl), ("S1", s1), ("S2", s2)):
                if sel is None:
                    rows.append(dict(uni=uname, book=b, reset=rs, rule=lbl, arm="PICKS NOTHING",
                                     IS_Sharpe=np.nan, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                                     OOS_MaxDD=np.nan))
                    continue
                key = (b, (None if pd.isna(sel.D) else sel.D), sel.k, ("-" if pd.isna(sel.D) else rs))
                oos = arms[key].loc[OOS_START:]
                mo = metrics(oos)
                rows.append(dict(uni=uname, book=b, reset=rs, rule=lbl, arm=sel.arm,
                                 IS_Sharpe=sel.IS_Sharpe, OOS_CAGR=mo["CAGR"],
                                 OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    Wf = pd.DataFrame(rows)
    print(f"\n--- WALK-FORWARD (rule 8) {uname}: (D,k) chosen on 2009-2016 only, 2017-2026 "
          f"untouched, {PCOST:.0f} bps ---")
    print(f"  OOS references: SPY {spy_o['CAGR']:.2%}/{spy_o['Sharpe']:.3f}/{spy_o['MaxDD']:.2%}"
          f"   RULES v1 {v1_o['CAGR']:.2%}/{v1_o['Sharpe']:.3f}/{v1_o['MaxDD']:.2%}"
          f"   OOS 4b bars: Sharpe > {spy_o['Sharpe']:.3f}, MaxDD <= {0.60*abs(spy_o['MaxDD']):.2%},"
          f" CAGR >= {0.70*spy_o['CAGR']:.2%}")
    print(Wf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return Wf


# ---------------------------------------------------------------- main
def main():
    D_all, L_all, X_all, W_all = [], [], [], []
    slope_tab = {}
    for uname, kw in (("universe.json(56)", {}), ("universe_broad.json", dict(broad=True))):
        px, df, L, bars, spy, v1_net, arms = do_universe(uname, kw)
        X, slopes = exchange_rates(df, L, uname)
        slope_tab[uname] = slopes
        print(f"\n--- EXCHANGE RATE {uname}: pp CAGR surrendered per pp MaxDD bought "
              f"({PCOST:.0f} bps).  ALL {len(X)} treated arms ---")
        print("  static-gross lever slope (pp CAGR per pp MaxDD, OLS over the ladder): "
              + "  ".join(f"{b} {slopes[b]:.3f}" for b in BOOKS))
        print(X.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        Wf = walk_forward(uname, arms, bars, spy, v1_net)
        D_all.append(df); L_all.append(L); X_all.append(X); W_all.append(Wf)

    D = pd.concat(D_all, ignore_index=True)
    L = pd.concat(L_all, ignore_index=True)
    X = pd.concat(X_all, ignore_index=True)
    Wf = pd.concat(W_all, ignore_index=True)
    out = ROOT / "research" / "backtests"
    D.to_csv(out / f"{STEM}.grid.csv", index=False)
    L.to_csv(out / f"{STEM}.ladder.csv", index=False)
    X.to_csv(out / f"{STEM}.rates.csv", index=False)

    print("\n" + "=" * 210)
    print("ANSWER — idea 22 as worded, and the four pre-registered predictions")
    print("=" * 210)

    at = D[D.cost == PCOST]
    tre = at[at.arm != "control"]

    print("\nA0. The LITERAL idea 22 rule (D=8%, k=0.50, reset=new high) vs its own control, 10 bps")
    for u in D.uni.unique():
        for b in BOOKS:
            c0 = at[(at.uni == u) & (at.book == b) & (at.arm == "control")].iloc[0]
            a = at[(at.uni == u) & (at.book == b) & (at.arm == "D8%/k0.50/high")].iloc[0]
            print(f"  {u:20s} {b:7s} rule {a.CAGR:6.2%}/{a.Sharpe:.3f}/{a.MaxDD:7.2%}"
                  f"  ctl {c0.CAGR:6.2%}/{c0.Sharpe:.3f}/{c0.MaxDD:7.2%}"
                  f"  dSharpe {a.Sharpe-c0.Sharpe:+.3f}  dCAGR {a.CAGR-c0.CAGR:+.2%}"
                  f"  dMaxDD {abs(c0.MaxDD)-abs(a.MaxDD):+.2%}  days cut {a.cut_days:.1%}"
                  f"  episodes {a.episodes:.0f}  4b {'PASS' if a.p4b else 'fail:'+a.f4b}")

    print("\nA1. P1 — is the rule Sharpe-negative?  (treated arms vs their own cell control, 10 bps)")
    worse = 0
    for u in D.uni.unique():
        for b in BOOKS:
            c0 = at[(at.uni == u) & (at.book == b) & (at.arm == "control")].iloc[0]
            g = tre[(tre.uni == u) & (tre.book == b)]
            w = int((g.Sharpe < c0.Sharpe).sum())
            worse += w
            print(f"  {u:20s} {b:7s} arms worse on Sharpe: {w:3d}/{len(g)}   "
                  f"best dSharpe {(g.Sharpe-c0.Sharpe).max():+.3f} at "
                  f"{g.loc[(g.Sharpe-c0.Sharpe).idxmax()].arm:16s}   "
                  f"median dSharpe {(g.Sharpe-c0.Sharpe).median():+.3f}")
    print(f"  P1 {'HOLDS' if worse > 0.5*len(tre) else 'FALSIFIED'}: {worse}/{len(tre)} treated arms "
          f"lose Sharpe against their control")

    print("\nA2. P2 — the de-levering ratchet: share of days spent cut, by reset rule")
    print(tre.groupby(["uni", "book", "reset"]).cut_days.agg(["min", "median", "max"]).to_string(
        float_format=lambda x: f"{x:.1%}"))
    hi = tre[tre.reset == "high"].cut_days.median()
    re = tre[tre.reset == "recover"].cut_days.median()
    print(f"  median days cut: high {hi:.1%}  recover {re:.1%}  -> P2 "
          f"{'HOLDS' if hi > 0.40 and re < hi else 'FALSIFIED'}")

    print("\nA3. P3 — is the instrument dominated by a static gross cut?")
    print(f"  arms where rate_DD >= rate_gross (dominated): {int(X.dominated.sum())}/{len(X)}")
    print("  head-to-head against the SAME average gross held statically (vs_gm_*):")
    print(X.groupby(["uni", "book"])[["vs_gm_CAGR", "vs_gm_MaxDD", "vs_gm_Sharpe"]].agg(
        ["mean", "max"]).to_string(float_format=lambda x: f"{x:.4f}"))
    beat = X[(X.vs_gm_Sharpe > 0) & (X.vs_gm_MaxDD > 0)]
    print(f"  arms beating the matched static book on BOTH Sharpe and MaxDD: {len(beat)}/{len(X)}")
    if len(beat):
        print(beat.sort_values("vs_gm_Sharpe", ascending=False).head(15).to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"  P3 {'HOLDS' if X.dominated.mean() > 0.5 else 'FALSIFIED'}")

    print("\nA4. P4 — does any arm CONVERT a 4b failure to a 4b pass on BOTH universes?")
    piv = at.pivot_table(index=["book", "arm"], columns="uni", values="p4b", aggfunc="first")
    piv["both"] = piv.all(axis=1)
    print(piv.to_string())
    ctl_both = {b: bool(piv.loc[(b, "control"), "both"]) for b in BOOKS}
    conv = [(b, a) for (b, a) in piv.index if a != "control" and piv.loc[(b, a), "both"]
            and not ctl_both[b]]
    print(f"  controls passing 4b on both universes: {ctl_both}")
    print(f"  treated arms passing 4b on BOTH universes: "
          f"{int(piv.loc[[i for i in piv.index if i[1] != 'control'], 'both'].sum())}")
    print(f"  CONVERSIONS (control fails both-universe 4b, arm passes): {conv if conv else 'none'}"
          f"  -> P4 {'HOLDS' if not conv else 'FALSIFIED'}")

    print("\nA5. 4a and 4b census over the full grid, by cost")
    print(D.groupby(["uni", "cost"])[["p4a", "p4b"]].sum().to_string())
    print("  (control rows included; see the grid for which)")

    print("\nA6. Bear-market shape — 2020 and 2022 by arm (10 bps), the only place the rule can pay")
    yr = at.pivot_table(index=["uni", "book", "arm"], values=["y2020", "y2022", "MaxDD", "Sharpe"])
    print(yr.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\nA7. Walk-forward head-to-head, both universes")
    print(Wf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    pv = Wf.pivot_table(index=["uni", "book", "reset"], columns="rule", values="OOS_Sharpe")
    for c in ("S1", "S2"):
        if c in pv:
            pv[f"{c}-CTL"] = pv[c] - pv["CTL"]
    print(pv.to_string(float_format=lambda x: f"{x:.3f}"))
    print(f"  mean OOS Sharpe — CTL {pv['CTL'].mean():.3f}"
          + (f"  S1 {pv['S1'].mean():.3f}" if "S1" in pv else "")
          + (f"  S2 {pv['S2'].mean():.3f}" if "S2" in pv else ""))
    nsel = Wf[(Wf.rule != "CTL") & (Wf.arm != "control") & (Wf.arm != "PICKS NOTHING")]
    print(f"  selections that chose a DRAWDOWN RULE over the control: {len(nsel)} of "
          f"{len(Wf[Wf.rule != 'CTL'])}")
    if len(nsel):
        print(nsel.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\nA8. Static-gross ladder slopes (pp CAGR per pp MaxDD) — the price to beat")
    print(pd.DataFrame(slope_tab).to_string(float_format=lambda x: f"{x:.3f}"))
    print("\nGrid -> %s.grid.csv | ladder -> %s.ladder.csv | rates -> %s.rates.csv" % (STEM, STEM, STEM))
    print("LEADERBOARD rows are written by hand from this console into the .result.md.")


if __name__ == "__main__":
    main()
