#!/usr/bin/env python3
"""QUEUE idea 93 — absorbing-state-audit-of-every-state-dependent-rule (lane B, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 22 found that any exposure rule whose RE-ENTRY condition is a function of the book's own
equity (new high, recovery to -D/2) is ABSORBING at zero exposure, and near-absorbing at small k.
The project has several such rules on the books (idea 40's book-level DD control, idea 9's
per-name trailing stop, idea 75's conditionally-armed stop). Audit each for the same failure and
propose the general fix: re-entry conditioned on an EXOGENOUS series (SPY's own 200d, breadth)
rather than on the book's equity. Max 2 params."

The claim, stated sharply enough to be falsifiable
--------------------------------------------------
A state-dependent exposure rule has an absorbing state whenever the STATE VARIABLE ITS RE-ENTRY
CONDITION READS IS FROZEN BY THE ACTION THE RULE TAKES.  Book equity is frozen by going to cash;
a name's price and SPY's trend are not.  So the audit is not "endogenous vs exogenous" as such —
it is "does the action stop the clock the re-entry condition is reading".  That distinction makes
a testable prediction the loose wording does not: a PER-NAME stop whose re-entry reads the NAME's
own price is endogenous yet NOT absorbing, because the name keeps trading whether or not we hold
it.  Both families are run so the distinction can be checked rather than asserted.

Families audited (every rule the QUEUE item names)
    DDCTL   idea 22 / idea 40's book-level drawdown control: while the book's own net equity is
            more than D below its running peak, multiply the target book by k.
            reset arms:  high     endogenous, idea 22 as worded — release at a new equity high
                         recover  endogenous — release when the drawdown is shallower than D/2
                         spy200   EXOGENOUS FIX — release when SPY closes above its own 200d MA
                         t8, t26  EXOGENOUS FIX — release after 8 / 26 cut rebalances (calendar)
    STOP    idea 9's per-name trailing stop (exit a name s% below its running high since entry,
            executed the NEXT day, cash until re-entry) and idea 75's conditional arming.
            re-entry arms: free     re-eligible at the next rebalance
                           nhigh    ENDOGENOUS TO THE NAME — blocked until the name's price
                                    exceeds the peak it had when it was stopped
                           bookhigh ENDOGENOUS TO THE BOOK — blocked until the BOOK makes a new
                                    equity high.  This is the pathology transplanted into a
                                    per-name rule and is the arm that tests the sharp claim.
                           spy200   EXOGENOUS FIX
            arming arms:   always / spy_below (idea 75: stop live only while SPY < its own 200d)

Books (pre-chosen, NEVER selected; all reported) and universes — identical to idea 22's run so the
control reproduces its published numbers:
    V1      RULES v1 exactly as live (top-5, /sqrt(vol20), 200d gate, vol20<0.60, 15% each, weekly)
    CAND20  idea 2's standing 4b KEEP-candidate (top-20 of the un-scaled composite, 0.75/20 each)
    EWall   idea 72 / idea 10's `B136/EWall` (equal-weight every eligible name at 75% gross)
    universe.json (56) and universe_broad.json (136); both always reported.

Tuned parameters (PROTOCOL rule 4: at most two), per family:
    DDCTL   D in {4,6,8,10,12,15}%  and  k in {0.00,0.25,0.50,0.75}          -> exactly 2
    STOP    s in {10,15,20,25}%                                              -> exactly 1
RESET / RE-ENTRY / ARMING are ARMS, not tuned parameters: every arm is run and reported in full and
every walk-forward selection is confined INSIDE one arm, so no selection ever spans three dials.
Costs 10 and 25 bps are reported for every point; 10 bps is the PROTOCOL point and the one every
selection uses.  Grid: DDCTL 6 cells x (5 arms x 6 D x 4 k + control) x 2 costs = 1452 points;
STOP 6 cells x (4 re-entry x 2 arming x 4 s + control) x 2 costs = 396 points.  ALL reported.

The control idea 66 made mandatory
-----------------------------------
Gross exposure is an exact, Sharpe-neutral lever, so any rule that spends part of its life at
reduced exposure must be judged against a STATIC book at the same average gross, not against the
un-cut book.  For every cell we run a static-gross ladder m = 0.10..1.00 step 0.05 and report, on
idea 74's axis, the pp of CAGR surrendered per pp of MaxDD bought by the rule vs by the ladder.

Pre-registered predictions (written before any number below was read)
    P1  DDCTL at k=0.00 with an endogenous reset (`high` or `recover`) is EXACTLY absorbing:
        after the first arming it never disarms, in every cell, at every D.  (Analytic: at k=0 the
        book is entirely in cash, so equity is constant, so the drawdown that armed it is frozen
        at a value below both release thresholds.)
    P2  Endogenous resets at k>0 are near-absorbing with cut-episode length rising as k falls.
    P3  The exogenous resets remove absorption entirely (every arming is followed by a disarm)
        without needing k>0.
    P4  Removing absorption does NOT make the instrument worth owning: the exogenous arms still
        surrender more CAGR per pp of MaxDD than the static-gross ladder in the large majority of
        arms, and do not convert a 4b failure into a 4b pass on both universes.
    P5  The per-name stop with `nhigh` re-entry is NOT absorbing (the name keeps trading), while
        the same stop with `bookhigh` re-entry IS near-absorbing — i.e. the frozen-clock reading
        of the claim is right and the endogenous/exogenous reading is wrong.

Walk-forward (PROTOCOL rule 8), selection rules fixed before any OOS number was read
    S1  argmax IS (2009-2016) Sharpe over the tuned grid of that cell+arm, control included.
    S2  4b-aware: among arms clearing the IS-window 4b bars (both IS halves' Sharpe > SPY's, IS
        MaxDD <= 60% of SPY's, IS CAGR >= 70% of SPY's), argmax IS Sharpe; if none clears, the
        selector PICKS NOTHING and that is reported as such.
    Both evaluated untouched on 2017-2026 against the control, RULES v1 and SPY.

Execution realism (PROTOCOL rule 2): weights decided at close t are applied at t+1, weekly
rebalance, long-only, no leverage, costs charged on realised turnover.  Every state machine reads
NET equity / prices through close t-1 at a rebalance; a stop triggered at close t is executed at
t+1.  No look-ahead anywhere.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every
absolute CAGR is optimistic.  This run compares arms sharing a panel and the same days, so the
treatment deltas — which are the result — are far less exposed than the levels.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_absorbing-state-audit_B"
OUT = ROOT / "research" / "backtests"
FREQ, MAX_VOL, GROSS, NCAND = "W", 0.60, 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"

DTRIG = [0.04, 0.06, 0.08, 0.10, 0.12, 0.15]
KCUT = [0.00, 0.25, 0.50, 0.75]
RESETS = ["high", "recover", "spy200", "t8", "t26"]
ENDO_RESETS = {"high", "recover"}
SLEV = [0.10, 0.15, 0.20, 0.25]
REENTRY = ["free", "nhigh", "bookhigh", "spy200"]
ARMING = ["always", "spy_below"]
COSTS = [10, 25]
PCOST = 10
BOOKS = ["V1", "CAND20", "EWall"]
LADDER = np.round(np.arange(0.10, 1.001, 0.05), 2)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def targets(px, book):
    """Target weight matrix at the book's PUBLISHED exposure (multiplier m = 1.0)."""
    if book == "V1":
        return rules_v1_weights(px)
    vol = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = ((vol < MAX_VOL) & (px > px.rolling(200).mean())).fillna(False)
    if book == "EWall":
        e = elig.astype(float)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    return (rank <= NCAND).astype(float) * (GROSS / NCAND)


def spy_trend(px):
    """SPY above its own 200d MA, as a boolean array aligned to px.index (the exogenous series)."""
    s = px["SPY"]
    return (s > s.rolling(200).mean()).fillna(False).values


# ---------------------------------------------------------------- DDCTL family
def run_ddctl(px, W, spy_up, m=1.0, D=None, k=1.0, reset="high", bps=PCOST):
    """Book-level drawdown control.  D=None -> the control / static-gross ladder point.

    ARM at a rebalance when the book's own NET equity through close t-1 is more than D below its
    running peak.  DISARM per the reset arm, also read through close t-1:
        high     new equity high            (endogenous; frozen by the action when k=0)
        recover  drawdown shallower than D/2 (endogenous; frozen by the action when k=0)
        spy200   SPY above its own 200d MA   (exogenous; never frozen by the action)
        t8/t26   after 8 / 26 cut rebalances (exogenous calendar; never frozen)
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
    eq, peak, armed = 1.0, 1.0, False
    arms = disarms = 0
    cut_rebals = 0                     # rebalances spent armed, for the calendar resets
    first_arm = -1
    ep_lens, cur_ep = [], 0
    for i in range(n):
        if mask[i] and i > 0:
            if D is not None:
                dd = eq / peak - 1.0
                if not armed:
                    if dd < -D:
                        armed, arms, cut_rebals, cur_ep = True, arms + 1, 0, 0
                        if first_arm < 0:
                            first_arm = i
                else:
                    if reset == "high":
                        rel = dd >= 0.0
                    elif reset == "recover":
                        rel = dd > -D / 2.0
                    elif reset == "spy200":
                        rel = bool(spy_up[i - 1])
                    else:
                        rel = cur_ep >= int(reset[1:])
                    if rel:
                        armed, disarms = False, disarms + 1
                        ep_lens.append(cur_ep)
                if armed:
                    cur_ep += 1
                    cut_rebals += 1
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
    if armed:
        ep_lens.append(cur_ep)
    r = pd.Series((held * rets).sum(axis=1), index=px.index) - pd.Series(turn, index=px.index) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=px.index), gross=pd.Series(gross_s, index=px.index),
                cut=pd.Series(cut, index=px.index), arms=arms, disarms=disarms,
                ep_mean=(float(np.mean(ep_lens)) if ep_lens else np.nan),
                ep_max=(int(np.max(ep_lens)) if ep_lens else 0),
                first_arm=first_arm, terminal_cut=bool(armed))


# ---------------------------------------------------------------- STOP family
def run_stop(px, W, spy_up, s=None, reentry="free", arming="always", bps=PCOST):
    """idea 9's per-name trailing stop, with idea 75's conditional arming.

    s=None -> the control (no stop).  A name held with weight>0 has its running high tracked from
    entry; when its close at t is more than s below that high (and the stop is armed at t) the name
    is SOLD AT t+1 and its cash sits idle until the re-entry arm releases it at a rebalance:
        free      released at the next rebalance
        nhigh     released when the name's price exceeds the peak it had when stopped
                  (endogenous TO THE NAME — but the name keeps trading, so the clock never stops)
        bookhigh  released when the BOOK makes a new equity high
                  (endogenous TO THE BOOK — the clock stops whenever the book is fully stopped out)
        spy200    released when SPY closes above its own 200d MA (exogenous)
    arming: `always`, or idea 75's `spy_below` (stop live only while SPY < its own 200d).
    """
    prices = px.values
    rets = px.pct_change().fillna(0.0).values
    tgt_all = W.reindex(px.index).fillna(0.0).values
    mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
    n, ncol = rets.shape
    cur = np.zeros(ncol)
    held = np.zeros((n, ncol))
    turn = np.zeros(n)
    gross_s = np.zeros(n)
    blocked = np.zeros(ncol, dtype=bool)
    block_ref = np.zeros(ncol)
    pending = np.zeros(ncol, dtype=bool)
    npeak = np.zeros(ncol)
    eq, peak = 1.0, 1.0
    fires = releases = 0
    blocked_days = 0
    zero_days = 0
    block_start = np.zeros(ncol, dtype=int)
    blk_lens = []
    for i in range(n):
        if s is not None and pending.any() and not mask[i]:
            # execute yesterday's stop today (t+1), outside the weekly rebalance
            turn[i] += float(cur[pending].sum())
            cur = cur.copy()
            cur[pending] = 0.0
            pending[:] = False
        if mask[i] and i > 0:
            if s is not None:
                pending[:] = False
                if blocked.any():
                    if reentry == "free":
                        rel = blocked.copy()
                    elif reentry == "nhigh":
                        rel = blocked & (prices[i - 1] > block_ref)
                    elif reentry == "bookhigh":
                        rel = blocked & (eq >= peak - 1e-15)
                    else:
                        rel = blocked & bool(spy_up[i - 1])
                    if rel.any():
                        for j in np.flatnonzero(rel):
                            blk_lens.append(i - block_start[j])
                        releases += int(rel.sum())
                        blocked[rel] = False
            new = tgt_all[i - 1].copy()
            if s is not None:
                new[blocked] = 0.0
            tot = new.sum()
            if tot > 1.0:
                new = new / tot
            turn[i] += np.abs(new - cur).sum()
            newly = (new > 0) & (cur <= 0)
            npeak[newly] = prices[i][newly]
            npeak[new <= 0] = 0.0
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        if s is not None:
            blocked_days += int(blocked.sum() > 0)
            if cur.sum() <= 1e-12:
                zero_days += 1
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp)
        peak = max(peak, eq)
        growth = cur * (1 + rets[i])
        tt = growth.sum() + (1 - cur.sum())
        cur = growth / tt if tt > 0 else cur
        if s is not None:
            live = cur > 1e-12
            npeak[live] = np.maximum(npeak[live], prices[i][live])
            armed_now = True if arming == "always" else (not bool(spy_up[i]))
            if armed_now:
                hit = live & (npeak > 0) & (prices[i] < (1.0 - s) * npeak)
                if hit.any():
                    pending[hit] = True
                    blocked[hit] = True
                    block_ref[hit] = npeak[hit]
                    block_start[hit] = i
                    fires += int(hit.sum())
    r = pd.Series((held * rets).sum(axis=1), index=px.index) - pd.Series(turn, index=px.index) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=px.index), gross=pd.Series(gross_s, index=px.index),
                fires=fires, releases=releases, blocked_days=blocked_days, zero_days=zero_days,
                blk_mean=(float(np.mean(blk_lens)) if blk_lens else np.nan),
                terminal_blocked=int(blocked.sum()))


# ---------------------------------------------------------------- metrics glue
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


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def is_bars(spy):
    isp = spy.loc[:IS_END]
    h = len(isp) // 2
    m = metrics(isp)
    return dict(s1=metrics(isp.iloc[:h])["Sharpe"], s2=metrics(isp.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"])


def is_pass4b(r, ib):
    isp = r.loc[:IS_END]
    h = len(isp) // 2
    m = metrics(isp)
    return bool(metrics(isp.iloc[:h])["Sharpe"] > ib["s1"] and metrics(isp.iloc[h:])["Sharpe"] > ib["s2"]
                and abs(m["MaxDD"]) <= 0.60 * abs(ib["sdd"]) and m["CAGR"] >= 0.70 * ib["scagr"])


def base_row(r, prefix=""):
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    h1, h2 = halves(r)
    return {prefix + "CAGR": m["CAGR"], prefix + "Sharpe": m["Sharpe"], prefix + "MaxDD": m["MaxDD"],
            prefix + "H1": h1, prefix + "H2": h2,
            prefix + "IS_Sharpe": metrics(r.loc[:IS_END])["Sharpe"],
            prefix + "OOS_CAGR": mo["CAGR"], prefix + "OOS_Sharpe": mo["Sharpe"],
            prefix + "OOS_MaxDD": mo["MaxDD"]}


# ---------------------------------------------------------------- driver
def do_universe(uname, kw, rows_dd, rows_st, rows_lad, rows_wf):
    px = load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_up = spy_trend(px)
    bars, ib = bars_of(spy), is_bars(spy)
    ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
    W = {b: targets(px, b) for b in BOOKS}

    print("\n" + "=" * 200)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f} | OOS {mso['CAGR']:.2%}/{bars['soos']:.3f}/{mso['MaxDD']:.2%}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f}/{bars['s2']:.3f}/{bars['soos']:.3f} (H1/H2/OOS), "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    print("=" * 200)

    # ---- harness sanity: both controls must reproduce engine.backtest to machine precision
    worst = 0.0
    for b in BOOKS:
        e = backtest(px, W[b], cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
        for f in (run_ddctl(px, W[b], spy_up, D=None, bps=PCOST)["r"],
                  run_stop(px, W[b], spy_up, s=None, bps=PCOST)["r"]):
            worst = max(worst, float((f.loc[start:] - e).abs().max()))
    print(f"ENGINE-EQUIVALENCE (both controls vs engine.backtest @ {PCOST} bps): max|diff| = {worst:.3e} "
          f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — results below are unsafe'})")

    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
    for c in COSTS:
        m = metrics(v1_net[c])
        mo = metrics(v1_net[c].loc[OOS_START:])
        print(f"RULES v1 @ {c}bps: CAGR {m['CAGR']:.2%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:.2%}"
              f" | OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}")

    arms_pcost = {}
    for b in BOOKS:
        for c in COSTS:
            # ---- static-gross ladder (the idea-66 control), same cell, no state rule at all
            lad = []
            for m_ in LADDER:
                res = run_ddctl(px, W[b], spy_up, m=m_, D=None, bps=c)
                r = res["r"].loc[start:]
                mm = metrics(r)
                lad.append(dict(uni=uname, book=b, cost=c, m=m_, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                                MaxDD=mm["MaxDD"], gross=res["gross"].loc[start:].mean()))
            lad = pd.DataFrame(lad)
            rows_lad.extend(lad.to_dict("records"))
            sl = np.polyfit(lad["MaxDD"].abs(), lad["CAGR"], 1)[0]   # pp CAGR per pp MaxDD
            ctl = run_ddctl(px, W[b], spy_up, D=None, bps=c)
            rc = ctl["r"].loc[start:]
            mc = metrics(rc)

            # ---- DDCTL grid
            for reset in ["-"] + RESETS:
                specs = [(None, 1.0)] if reset == "-" else [(D, k) for D in DTRIG for k in KCUT]
                for D, k in specs:
                    res = ctl if D is None else run_ddctl(px, W[b], spy_up, D=D, k=k, reset=reset, bps=c)
                    r = res["r"].loc[start:]
                    m = metrics(r)
                    mg = margins(r, bars)
                    dd_gain = abs(mc["MaxDD"]) - abs(m["MaxDD"])
                    row = dict(uni=uname, book=b, cost=c, family="DDCTL", reset=reset,
                               arm=("control" if D is None else f"D{D:.0%}/k{k:.2f}/{reset}"),
                               D=(np.nan if D is None else D), k=k,
                               n_arm=res["arms"], n_disarm=res["disarms"], ep_mean=res["ep_mean"],
                               ep_max=res["ep_max"], terminal_cut=res["terminal_cut"],
                               absorbed=bool(res["arms"] > 0 and res["disarms"] == 0),
                               cut_days=res["cut"].loc[start:].mean(),
                               gross=res["gross"].loc[start:].mean(),
                               TO=res["to"].loc[start:].sum() / m["Years"],
                               dSharpe=m["Sharpe"] - mc["Sharpe"], dd_gain=dd_gain,
                               rate_DD=((mc["CAGR"] - m["CAGR"]) / dd_gain if dd_gain > 1e-9 else np.nan),
                               rate_gross=sl,
                               m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                               p4b=all(v > 0 for v in mg.values()),
                               f4b=",".join([kk for kk, v in mg.items() if not v > 0]) or "-",
                               p4a=pass4a(r, v1_net[c]), IS4b=is_pass4b(r, ib))
                    row.update(base_row(r))
                    rows_dd.append(row)
                    if c == PCOST:
                        arms_pcost[("DDCTL", b, reset, D, k)] = r

            # ---- STOP grid
            for reent in ["-"] + REENTRY:
                for arming in (["-"] if reent == "-" else ARMING):
                    for s_ in ([None] if reent == "-" else SLEV):
                        res = (run_stop(px, W[b], spy_up, s=None, bps=c) if s_ is None
                               else run_stop(px, W[b], spy_up, s=s_, reentry=reent, arming=arming, bps=c))
                        r = res["r"].loc[start:]
                        m = metrics(r)
                        mg = margins(r, bars)
                        dd_gain = abs(mc["MaxDD"]) - abs(m["MaxDD"])
                        row = dict(uni=uname, book=b, cost=c, family="STOP", reentry=reent, arming=arming,
                                   arm=("control" if s_ is None else f"s{s_:.0%}/{reent}/{arming}"),
                                   s=(np.nan if s_ is None else s_),
                                   fires=res["fires"], releases=res["releases"],
                                   blk_mean=res["blk_mean"], terminal_blocked=res["terminal_blocked"],
                                   blocked_day_frac=res["blocked_days"] / len(px),
                                   zero_day_frac=res["zero_days"] / len(px),
                                   stuck=bool(res["fires"] > 0 and res["releases"] < res["fires"]),
                                   gross=res["gross"].loc[start:].mean(),
                                   TO=res["to"].loc[start:].sum() / m["Years"],
                                   dSharpe=m["Sharpe"] - mc["Sharpe"], dd_gain=dd_gain,
                                   rate_DD=((mc["CAGR"] - m["CAGR"]) / dd_gain if dd_gain > 1e-9 else np.nan),
                                   rate_gross=sl,
                                   m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                                   p4b=all(v > 0 for v in mg.values()),
                                   f4b=",".join([kk for kk, v in mg.items() if not v > 0]) or "-",
                                   p4a=pass4a(r, v1_net[c]), IS4b=is_pass4b(r, ib))
                        row.update(base_row(r))
                        rows_st.append(row)
                        if c == PCOST:
                            arms_pcost[("STOP", b, reent, arming, s_)] = r
            print(f"  {uname:6s} {b:7s} @{c:2d}bps: ladder slope {sl:.3f} pp/pp | "
                  f"control {mc['CAGR']:.2%}/{mc['Sharpe']:.3f}/{mc['MaxDD']:.2%}", flush=True)

    # ---- walk-forward (rule 8): selection inside one arm, on IS only, OOS read once
    for b in BOOKS:
        ctl_r = arms_pcost[("DDCTL", b, "-", None, 1.0)]
        for reset in RESETS:
            grid = [(D, k) for D in DTRIG for k in KCUT]
            cand = {(D, k): arms_pcost[("DDCTL", b, reset, D, k)] for D, k in grid}
            cand[("control", "-")] = ctl_r
            rows_wf.append(_wf("DDCTL", uname, b, reset, cand, ctl_r, v1_net[PCOST], spy, ib))
        for reent in REENTRY:
            for arming in ARMING:
                cand = {(s_,): arms_pcost[("STOP", b, reent, arming, s_)] for s_ in SLEV}
                cand[("control",)] = arms_pcost[("STOP", b, "-", "-", None)]
                rows_wf.append(_wf("STOP", uname, b, f"{reent}/{arming}", cand,
                                   arms_pcost[("STOP", b, "-", "-", None)], v1_net[PCOST], spy, ib))
    return dict(uni=uname, spy=spy, v1=v1_net[PCOST])


def _wf(family, uname, book, arm, cand, ctl_r, v1_r, spy, ib):
    iss = {kk: metrics(v.loc[:IS_END])["Sharpe"] for kk, v in cand.items()}
    s1 = max(iss, key=lambda kk: iss[kk])
    ok = [kk for kk, v in cand.items() if is_pass4b(v, ib)]
    s2 = max(ok, key=lambda kk: iss[kk]) if ok else None
    out = dict(family=family, uni=uname, book=book, arm=arm,
               S1_pick=str(s1), S1_IS=iss[s1],
               S2_pick=(str(s2) if s2 else "NOTHING"), n_IS4b=len(ok))
    for tag, kk in (("S1", s1), ("S2", s2)):
        if kk is None:
            out.update({f"{tag}_OOS_CAGR": np.nan, f"{tag}_OOS_Sharpe": np.nan, f"{tag}_OOS_MaxDD": np.nan})
        else:
            m = metrics(cand[kk].loc[OOS_START:])
            out.update({f"{tag}_OOS_CAGR": m["CAGR"], f"{tag}_OOS_Sharpe": m["Sharpe"], f"{tag}_OOS_MaxDD": m["MaxDD"]})
    for tag, r in (("CTL", ctl_r), ("V1", v1_r), ("SPY", spy)):
        m = metrics(r.loc[OOS_START:])
        out.update({f"{tag}_OOS_CAGR": m["CAGR"], f"{tag}_OOS_Sharpe": m["Sharpe"], f"{tag}_OOS_MaxDD": m["MaxDD"]})
    out["S1_moved"] = str(s1) not in ("('control', '-')", "('control',)")
    return out


def main():
    t0 = time.time()
    rows_dd, rows_st, rows_lad, rows_wf = [], [], [], []
    for uname, kw in (("u56", {}), ("broad", dict(broad=True))):
        do_universe(uname, kw, rows_dd, rows_st, rows_lad, rows_wf)
    dd = pd.DataFrame(rows_dd)
    st = pd.DataFrame(rows_st)
    lad = pd.DataFrame(rows_lad)
    wf = pd.DataFrame(rows_wf)
    dd.to_csv(OUT / f"{STEM}.ddctl.csv", index=False)
    st.to_csv(OUT / f"{STEM}.stop.csv", index=False)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    treated = dd[dd["reset"] != "-"]
    st_t = st[st["reentry"] != "-"]
    print("\n" + "#" * 200)
    print(f"# GRID: DDCTL {len(dd)} points ({len(treated)} treated), STOP {len(st)} ({len(st_t)} treated), "
          f"ladder {len(lad)}, walk-forward {len(wf)}.  ALL reported in the CSVs.")
    print("#" * 200)

    # ---------------- P1 / P2 / P3: the absorbing audit
    print("\n### P1 — DDCTL at k=0.00: is an ENDOGENOUS reset exactly absorbing?  "
          "(absorbed = armed at least once and NEVER disarmed)")
    a = treated[treated["k"] == 0.0]
    piv = a.pivot_table(index="reset", values=["absorbed", "n_arm", "n_disarm", "cut_days", "terminal_cut"],
                        aggfunc="mean")
    piv["n_cells"] = a.groupby("reset").size()
    piv["absorbed_n"] = a.groupby("reset")["absorbed"].sum()
    print(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    for reset in RESETS:
        sub = a[a["reset"] == reset]
        print(f"  k=0.00 {reset:8s}: absorbed {int(sub['absorbed'].sum())}/{len(sub)}, "
              f"mean arms {sub['n_arm'].mean():.2f}, mean disarms {sub['n_disarm'].mean():.2f}, "
              f"mean cut-days {sub['cut_days'].mean():.1%}, terminal-cut {int(sub['terminal_cut'].sum())}/{len(sub)}")

    print("\n### P2 — near-absorption: mean cut-episode length (rebalances) by reset x k, all 6 cells x 2 costs")
    ep = treated.pivot_table(index="k", columns="reset", values="ep_mean", aggfunc="mean")
    print(ep.to_string(float_format=lambda x: f"{x:.1f}"))
    print("    cut-day fraction:")
    print(treated.pivot_table(index="k", columns="reset", values="cut_days",
                              aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n### P3 — do the exogenous resets remove absorption?  absorbed count by reset (all k, all cells)")
    tab = treated.groupby("reset").agg(n=("absorbed", "size"), absorbed=("absorbed", "sum"),
                                       terminal_cut=("terminal_cut", "sum"),
                                       escape=("n_disarm", "sum"), armings=("n_arm", "sum"))
    tab["escape_rate"] = tab["escape"] / tab["armings"].replace(0, np.nan)
    print(tab.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n### P5 — the sharp claim: per-name STOP, is the clock frozen by the action?")
    tab2 = st_t.groupby("reentry").agg(n=("stuck", "size"), stuck=("stuck", "sum"),
                                       fires=("fires", "mean"), releases=("releases", "mean"),
                                       blk_mean_days=("blk_mean", "mean"),
                                       terminal_blocked=("terminal_blocked", "mean"),
                                       zero_day_frac=("zero_day_frac", "mean"),
                                       gross=("gross", "mean"))
    tab2["release_rate"] = tab2["releases"] / tab2["fires"]
    print(tab2.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---------------- P4: is the de-absorbed instrument worth owning?
    print("\n### P4a — Sharpe vs the arm's own control, by family/arm (10 and 25 bps, both universes)")
    for lbl, frame, key in (("DDCTL", treated, "reset"), ("STOP", st_t, "reentry")):
        g = frame.groupby(key).agg(n=("dSharpe", "size"), worse=("dSharpe", lambda x: int((x < 0).sum())),
                                   mean_dSharpe=("dSharpe", "mean"), best=("dSharpe", "max"),
                                   mean_ddgain=("dd_gain", "mean"))
        print(f"  {lbl}:")
        print(g.to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n### P4b — idea 74's axis: pp CAGR surrendered per pp MaxDD bought, rule vs the static-gross ladder")
    for lbl, frame, key in (("DDCTL", treated, "reset"), ("STOP", st_t, "reentry")):
        f = frame.dropna(subset=["rate_DD"]).copy()
        f["dominated"] = f["rate_DD"] >= f["rate_gross"]
        g = f.groupby(key).agg(n=("rate_DD", "size"), med_rate_DD=("rate_DD", "median"),
                               med_rate_gross=("rate_gross", "median"),
                               dominated=("dominated", "sum"))
        g["dominated_frac"] = g["dominated"] / g["n"]
        print(f"  {lbl}:")
        print(g.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n### P4c — KEEP paths.  4b passes and 4a passes by arm (control shown for reference)")
    for lbl, frame, key, ctlmask in (("DDCTL", dd, "reset", dd["reset"] == "-"),
                                     ("STOP", st, "reentry", st["reentry"] == "-")):
        g = frame.groupby(key).agg(n=("p4b", "size"), p4b=("p4b", "sum"), p4a=("p4a", "sum"))
        print(f"  {lbl}:")
        print(g.to_string())
        ctl = frame[ctlmask]
        print(f"    control rows: {len(ctl)}, 4b {int(ctl['p4b'].sum())}, 4a {int(ctl['p4a'].sum())}")
    both = []
    for frame, key in ((treated, "reset"), (st_t, "reentry")):
        p = frame[frame["p4b"]]
        for (b, arm), sub in p.groupby(["book", key]):
            if set(sub["uni"]) == {"u56", "broad"}:
                both.append((frame is treated and "DDCTL" or "STOP", b, arm, len(sub)))
    print(f"\n  arms passing 4b on BOTH universes: {len(both)} -> {both}")

    print("\n### 4b-passing detail (every treated arm that passes, all cells)")
    cols = ["uni", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "gross", "p4a"]
    p = pd.concat([treated[treated["p4b"]][cols], st_t[st_t["p4b"]][cols]])
    print(p.to_string(index=False, float_format=lambda x: f"{x:.3f}") if len(p) else "  (none)")

    # ---------------- rule 8
    print("\n### PROTOCOL rule 8 — walk-forward, params chosen on 2009-2016 only, OOS 2017-2026 read once")
    wfc = ["family", "uni", "book", "arm", "S1_pick", "S1_moved", "S1_OOS_CAGR", "S1_OOS_Sharpe", "S1_OOS_MaxDD",
           "CTL_OOS_Sharpe", "S2_pick", "S2_OOS_Sharpe", "V1_OOS_Sharpe", "SPY_OOS_Sharpe"]
    print(wf[wfc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    wf["S1_vs_ctl"] = wf["S1_OOS_Sharpe"] - wf["CTL_OOS_Sharpe"]
    wf["S1_vs_spy"] = wf["S1_OOS_Sharpe"] - wf["SPY_OOS_Sharpe"]
    print("\n  aggregate by family x arm:")
    print(wf.groupby(["family", "arm"]).agg(
        n=("S1_vs_ctl", "size"), moved=("S1_moved", "sum"),
        mean_S1_vs_ctl=("S1_vs_ctl", "mean"), beat_ctl=("S1_vs_ctl", lambda x: int((x > 0).sum())),
        mean_S1_vs_spy=("S1_vs_spy", "mean"), beat_spy=("S1_vs_spy", lambda x: int((x > 0).sum())),
        S2_nothing=("S2_pick", lambda x: int((x == "NOTHING").sum())),
    ).to_string(float_format=lambda x: f"{x:.3f}"))
    print(f"\n  OVERALL: S1 moves off the control in {int(wf['S1_moved'].sum())} of {len(wf)} selections; "
          f"mean OOS Sharpe vs control {wf['S1_vs_ctl'].mean():+.4f} "
          f"(beats control in {int((wf['S1_vs_ctl'] > 0).sum())}); "
          f"mean vs SPY {wf['S1_vs_spy'].mean():+.4f} (beats SPY in {int((wf['S1_vs_spy'] > 0).sum())})")

    print(f"\nDone in {time.time() - t0:.0f}s.  CSVs: {STEM}.{{ddctl,stop,ladder,walkforward}}.csv")


if __name__ == "__main__":
    main()
