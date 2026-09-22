#!/usr/bin/env python3
"""Idea 2237 (lane C, 2026-09-22) — IS THE EXIT THRESHOLD THE ONLY DIAL THAT SPENDS THE
8.2 pp DRAWDOWN BUDGET?

THE DEFECT THIS PRICES.  The live book (RULES v2: 200d +/-3% band, equal weight, gross 0.75,
weekly, gated-out weight to CASH) carries roughly +8 pp of UNUSED drawdown budget against 4b's
cap (0.60 x SPY MaxDD) and misses 4b's CAGR floor (0.70 x SPY CAGR).  Every device the record
has priced against that floor spends the budget by BUYING MORE OF THE SAME BOOK (gross, 2085's
leverage) or by BUYING A DIFFERENT BOOK (2221's beta sleeve).  Clause 2 of RULES v2 uses ONE
constant for BOTH band edges.  The LOWER edge alone -- the EXIT threshold b_out -- is the only
dial that converts drawdown budget into TIME IN MARKET without adding gross, leverage or a
second asset: a deeper b_out holds a name through shallow dips instead of selling it to cash.

WHAT IS PRICED.  Three ladders, all from the SAME live base point, all scored on every 4b and
4a leg at four cost rungs on two panels:
  ARM A (TUNED)     EXIT EDGE b_out in {0.00 ... 0.30}, entry edge b_in FIXED at the live 0.03,
                    gross FIXED at the live 0.75, no sleeve.  b_out = 0.03 IS the live book.
  ARM B (COMPARAND) GROSS g in {0.75 ... 1.00} with the live symmetric 3% band.  No leverage
                    (PROTOCOL rule 2), so the ladder stops at 1.00.
  ARM C (COMPARAND) 2221's BETA SLEEVE: a fraction phi of idle NAV into SPY, live band, live
                    gross.  phi in {0.00 ... 1.00}.
THE PRICE OF THE TRADE.  For every rung with dCAGR > 0 against the live base, two ratios:
  R_DD  = (-dMaxDD) / dCAGR   -- pp of drawdown surrendered per pp of CAGR bought.  LOWER is
          cheaper.  This is the idea's own question.
  S_EXP = dCAGR / d(mean realised gross) -- pp of CAGR per unit of mean exposure.  STEEPER on
          b_out than on gross is the idea's stated mechanism (b_out moves the SHARE OF DAYS
          held, gross scales return and drawdown together).

DIALS.  EXACTLY ONE is tuned: the EXIT EDGE b_out.  REPORTED, NOT TUNED: gross (arm B's own
ladder), phi (arm C's own ladder), COST in {0, 10, 25, 50} bps, PANEL U56 and B136, cadence W
(the live book's), entry edge b_in = 0.03 (the live book's).  Every grid point is published
to `<stem>.grid.csv`.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1 CHEAPER THAN GROSS.  At 10 bps on U56, FULL sample, the MINIMUM R_DD over arm A's rungs
     is STRICTLY LOWER than the minimum R_DD over arm B's rungs.
  V2 CHEAPEST OF THE THREE.  That same minimum is also strictly lower than arm C's.
  V3 BUDGET SUFFICIENCY.  SOME b_out rung clears BOTH the 4b DD cap AND the 4b CAGR floor in
     the FULL sample at 10 bps -- i.e. the budget is large enough to buy the missing return on
     this dial alone.
  V4 FOUR-b.  SOME b_out rung clears 4b FULL *and* OOS at 10 bps on at least one panel.
  V5 RULE 8.  A LEGAL IS-ONLY chooser (2009-2016 rows only) picks a b_out whose 2017-2026 rows,
     read exactly once, clear 4b OOS.
  CAPITAL.  V3 AND V4 AND V5 -> KEEP-4b candidate and a memo with exact RULES wording.  Any of
  them failing -> KILL or PARK, with the binding leg named.  V1/V2 alone are a MECHANISM result
  (which dial is cheapest), never a capital result: a cheaper dial that still fails the floor
  buys nothing.
  Path 4a is scored at every cell against the live RULES v2 book on the SAME panel and the SAME
  cost rung.

PROTOCOL: rule 2 (10 bps headline, next-day execution, no shorting, no leverage); rule 3 (live
RULES v2 AND SPY); rule 4 (both KEEP paths at every cell, <= 2 tuned parameters); rule 5 (one
idea, deterministic, standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

SURVIVORSHIP (rule 9) -- READ BEFORE THE NUMBERS.  U56 (research/universe.json) and B136
(research/universe_broad.json) are CURRENT-constituent lists.  Every CAGR and drawdown LEVEL
below is optimistic, and a deep b_out is exactly the dial a survivorship-biased panel flatters
most: holding through a dip pays when the name is known to have survived.  The within-tape
CONTRAST between the three ladders does not repair that level, and the b_out result should be
read as an upper bound on the real dial.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-22_exit-threshold-dd-budget_C.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest as engine_backtest                # noqa: E402

DATE, SLUG = "2026-09-22", "exit-threshold-dd-budget"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
FREQ = "W"
B_IN = 0.03                       # the live entry edge, FIXED (not tuned)
B_OUT = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30]   # TUNED DIAL
GROSS = [0.75, 0.80, 0.85, 0.90, 0.95, 1.00]                                  # reported ladder
PHI = [0.00, 0.25, 0.50, 0.75, 1.00]                                          # reported ladder
LIVE_BAND, LIVE_GROSS = 0.03, 0.75
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CHOOSERS = ["IS_SHARPE", "IS_LEGS", "IS_MINMARG", "IS_CAGRSLACK", "IS_CALMAR", "CELL_ALPHA"]

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ------------------------------------------------------------------ books
def band_state_asym(px, b_in, b_out):
    """RULES v2 clause 2 with the two edges SPLIT.  IN above ma*(1+b_in), OUT below
    ma*(1-b_out), previous state in between, OUT before 200 closes exist.  b_in = b_out
    reproduces baseline.band_state exactly."""
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b_in), 1.0).mask(px < ma * (1 - b_out), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def inband_share(px, b_in, b_out):
    """Mean over time of (priced names inside the band) / (priced names) -- the SHARE OF DAYS
    a name is held, which is the quantity b_out is supposed to move.  Reported, not tuned."""
    ok = px.notna()
    st = band_state_asym(px, b_in, b_out) & ok
    return float((st.sum(axis=1) / ok.sum(axis=1).replace(0, np.nan)).mean())


def book(px, b_in, b_out, gross, phi=0.0):
    """The live band book with a split band, a gross dial and 2221's beta sleeve.  Gated-out
    weight goes to CASH (de-gross, never re-spread); phi of the idle NAV is then swept into
    SPY, which ADDS to any core SPY holding (2221's convention, by construction)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(band_state_asym(px, b_in, b_out), 0.0)
    if phi:
        idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
        w = w.copy()
        w["SPY"] = w["SPY"] + phi * idle
    return w


def run(px, w, st):
    r = engine_backtest(px, w, cost_bps=0.0, freq=FREQ)
    return r["returns"].loc[st:], r["turnover"].loc[st:], r["weights"].sum(axis=1).loc[st:]


# ------------------------------------------------------------------ metrics
def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]


def binding(mar):
    bad = [k for k in LEGS if not (mar[k] > 0)]
    return ("|".join(bad) if bad else "none", len(bad))


def spy_bars(px, st):
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
    h1, h2 = halves(spy)
    ih1, ih2 = halves(spy.loc[:IS_END])
    return dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                h1=h1, h2=h2, ish1=ih1, ish2=ih2)


def live_bars(px, st):
    lw = rules_v2_weights(px, LIVE_BAND, LIVE_GROSS)
    lr, lt, _ = run(px, lw, st)
    out = {}
    for c in COSTS:
        r = net(lr, lt, c)
        h1, h2 = halves(r)
        out[c] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]), is_=mets(r.loc[:IS_END]),
                      h1=h1, h2=h2, turn=float(lt.sum() / (len(lr) / 252.0)))
    return out


def score(r0, t0, gs, S, LV, inband=np.nan, **tags):
    """Every 4b / 4a leg at every cost rung for one book."""
    yrs = len(r0) / 252.0
    rows = []
    for c in COSTS:
        r = net(r0, t0, c)
        mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
        h1, h2 = halves(r)
        ih1, ih2 = halves(r.loc[:IS_END])
        mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
               "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
               "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
               "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
        bl, nbad = binding(mar)
        k4bf = (h1 > S["h1"] and h2 > S["h2"]
                and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
        k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
        k4bi = (ih1 > S["ish1"] and ih2 > S["ish2"]
                and mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"]
                and mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"])
        lv = LV[c]
        k4a = (h1 > lv["h1"] and h2 > lv["h2"] and mf["MaxDD"] >= lv["full"]["MaxDD"])
        k4ao = (mo["Sharpe"] > lv["oos"]["Sharpe"] and mo["MaxDD"] >= lv["oos"]["MaxDD"])
        is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
                   + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
                   + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
        is_minmarg = min(ih1 - S["ish1"], ih2 - S["ish2"],
                         mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                         mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])
        rows.append(dict(**tags, cost=c,
                         turn_py=float(t0.sum() / yrs),
                         gross_mean=float(gs.mean()), gross_max=float(gs.max()),
                         inband=inband,
                         CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                         is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                         is_legs=is_legs, is_minmarg=float(is_minmarg),
                         is_calmar=float(mi["CAGR"] / abs(mi["MaxDD"])) if mi["MaxDD"] < 0 else np.nan,
                         is_cagrslack=float(mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"]),
                         oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                         **{k: float(v) for k, v in mar.items()},
                         bind=bl, n_fail=nbad,
                         keep4b_full=k4bf, keep4b_oos=k4bo, keep4b_is=k4bi,
                         keep4b=(k4bf and k4bo), keep4a=k4a, keep4a_oos=k4ao))
    return rows


def pick(sub, chooser):
    """LEGAL IS-ONLY chooser: reads 2009-2016 columns only.  Deterministic tie-break on the
    dial ascending, so no chooser wins on ordering luck."""
    s = sub.sort_values("dial").reset_index(drop=True)
    if chooser == "IS_SHARPE":
        key = s.is_Sharpe.values
    elif chooser == "IS_LEGS":
        key = s.is_legs.values * 1e6 + s.is_Sharpe.values
    elif chooser == "IS_MINMARG":
        key = s.is_minmarg.values
    elif chooser == "IS_CAGRSLACK":
        key = s.is_cagrslack.values
    elif chooser == "IS_CALMAR":
        key = np.nan_to_num(s.is_calmar.values, nan=-1e9)
    elif chooser == "CELL_ALPHA":                 # no-information control: lowest dial
        key = -s.dial.values
    else:
        raise ValueError(chooser)
    return s.iloc[int(np.argmax(key))]


# ------------------------------------------------------------------ main
def main():
    frames, summary = [], []
    panels = {}
    for pname, kw in (("U56", {}), ("B136", dict(broad=True))):
        px = load_universe(**kw).dropna(how="all").ffill()
        st = px.index[WARMUP]
        log(f"\n================ PANEL {pname}: {px.shape[1]} columns, "
            f"{px.index[0].date()} -> {px.index[-1].date()}, scored from {st.date()}")
        S, LV = spy_bars(px, st), live_bars(px, st)
        panels[pname] = dict(px=px, st=st, S=S, LV=LV)
        lv = LV[COST0]
        log(f"  SPY  FULL {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:.2%}"
            f"   OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:.2%}")
        log(f"  4b bars: FULL DD cap {DD_CAP * S['full']['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR * S['full']['CAGR']:.2%};  OOS DD cap {DD_CAP * S['oos']['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR * S['oos']['CAGR']:.2%}")
        log(f"  LIVE RULES v2 @{COST0}bps  FULL {lv['full']['CAGR']:.2%} / {lv['full']['Sharpe']:.4f}"
            f" / {lv['full']['MaxDD']:.2%}   OOS {lv['oos']['CAGR']:.2%} / {lv['oos']['Sharpe']:.4f}"
            f" / {lv['oos']['MaxDD']:.2%}   turn {lv['turn']:.2f}/yr")
        log(f"  LIVE unused DD budget FULL {100 * (lv['full']['MaxDD'] - DD_CAP * S['full']['MaxDD']):+.2f} pp;"
            f"  CAGR-floor margin FULL {100 * (lv['full']['CAGR'] - CAGR_FLOOR * S['full']['CAGR']):+.2f} pp,"
            f"  OOS {100 * (lv['oos']['CAGR'] - CAGR_FLOOR * S['oos']['CAGR']):+.2f} pp")

        for arm, ladder in (("A_bout", B_OUT), ("B_gross", GROSS), ("C_sleeve", PHI)):
            for v in ladder:
                if arm == "A_bout":
                    w = book(px, B_IN, v, LIVE_GROSS)
                elif arm == "B_gross":
                    w = book(px, LIVE_BAND, LIVE_BAND, v)
                else:
                    w = book(px, LIVE_BAND, LIVE_BAND, LIVE_GROSS, phi=v)
                r0, t0, gs = run(px, w, st)
                ib = (inband_share(px, B_IN, v) if arm == "A_bout"
                      else inband_share(px, LIVE_BAND, LIVE_BAND))
                frames += score(r0, t0, gs, S, LV, inband=ib, panel=pname, arm=arm, dial=v)

    grid = pd.DataFrame(frames)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    log(f"\nGRID: {len(grid)} rows -> {Path(OUT).name}.grid.csv")

    # ---------------- ladders printed in full (PROTOCOL: report ALL grid points)
    for pname in panels:
        for arm in ("A_bout", "B_gross", "C_sleeve"):
            g = grid[(grid.panel == pname) & (grid.arm == arm) & (grid.cost == COST0)]
            log(f"\n--- {pname} / {arm} @ {COST0} bps (FULL | OOS), all rungs")
            log("   dial   meanG inband  turn/y |    CAGR  Sharpe   MaxDD "
                "|  oCAGR oSharpe   oMaxDD | 4bF 4bO  4a | binding")
            for _, r in g.iterrows():
                log(f"  {r.dial:5.2f}  {r.gross_mean:5.3f} {100*r.inband:5.1f}% {r.turn_py:6.2f} "
                    f"| {100*r.CAGR:6.2f} {r.Sharpe:7.4f} {100*r.MaxDD:7.2f} "
                    f"| {100*r.oos_CAGR:6.2f} {r.oos_Sharpe:7.4f} {100*r.oos_MaxDD:8.2f} "
                    f"| {int(r.keep4b_full)}   {int(r.keep4b_oos)}   {int(r.keep4a)} | {r.bind}")

    # ---------------- THE PRICE OF THE TRADE (V1, V2)
    log("\n================ THE PRICE OF THE TRADE (FULL sample, %d bps)" % COST0)
    log("  R_DD  = pp of MaxDD surrendered per pp of CAGR bought vs the live base (LOWER = cheaper)")
    log("  S_EXP = pp of CAGR bought per unit of mean realised gross (HIGHER = steeper)")
    price = {}
    for pname in panels:
        base = grid[(grid.panel == pname) & (grid.arm == "A_bout") & (grid.dial == LIVE_BAND)
                    & (grid.cost == COST0)].iloc[0]
        log(f"\n  {pname} base (= live book, b_out {LIVE_BAND}): CAGR {100*base.CAGR:.2f}%, "
            f"MaxDD {100*base.MaxDD:.2f}%, meanG {base.gross_mean:.3f}")
        for arm in ("A_bout", "B_gross", "C_sleeve"):
            g = grid[(grid.panel == pname) & (grid.arm == arm) & (grid.cost == COST0)]
            best, rows = np.inf, []
            for _, r in g.iterrows():
                dC = 100 * (r.CAGR - base.CAGR)
                dD = 100 * (r.MaxDD - base.MaxDD)
                dG = r.gross_mean - base.gross_mean
                if dC <= 1e-9:
                    continue
                rdd = (-dD) / dC
                sexp = dC / dG if abs(dG) > 1e-9 else np.inf
                rows.append((r.dial, dC, dD, rdd, sexp))
                best = min(best, rdd)
            price[(pname, arm)] = best
            log(f"    {arm}: rungs buying CAGR = {len(rows)}"
                + ("" if rows else "   (none: this dial buys no CAGR from the base)"))
            for d, dC, dD, rdd, sexp in rows:
                log(f"      dial {d:5.2f}  dCAGR {dC:+6.2f} pp  dMaxDD {dD:+6.2f} pp  "
                    f"R_DD {rdd:6.2f}  S_EXP {sexp:8.2f}")
            log(f"    -> min R_DD ({arm}) = " + (f"{best:.3f}" if np.isfinite(best) else "n/a"))

    v1 = gate("V1 b_out cheaper than GROSS (U56, min R_DD)",
              f"A={price[('U56','A_bout')]:.3f} vs B={price[('U56','B_gross')]:.3f}",
              "A < B", price[("U56", "A_bout")] < price[("U56", "B_gross")])
    v2 = gate("V2 b_out cheapest of the three (U56, min R_DD)",
              f"A={price[('U56','A_bout')]:.3f} vs C={price[('U56','C_sleeve')]:.3f}",
              "A < B and A < C",
              v1 and price[("U56", "A_bout")] < price[("U56", "C_sleeve")])

    # ---------------- V3 budget sufficiency, V4 4b
    a10 = grid[(grid.arm == "A_bout") & (grid.cost == COST0)]
    v3n = a10[(a10.L4_DD > 0) & (a10.L5_CAGR > 0)]
    v3 = gate("V3 budget sufficiency (a b_out rung clears the FULL DD cap AND CAGR floor)",
              f"{len(v3n)} of {len(a10)} (panel,rung) cells"
              + ("" if v3n.empty else "; " + ", ".join(f"{r.panel}/b_out={r.dial}"
                                                       for _, r in v3n.iterrows())),
              ">= 1 cell", len(v3n) > 0)
    v4n = a10[a10.keep4b]
    v4 = gate("V4 4b FULL+OOS on some b_out rung",
              f"{len(v4n)} of {len(a10)} cells"
              + ("" if v4n.empty else "; " + ", ".join(f"{r.panel}/b_out={r.dial}"
                                                       for _, r in v4n.iterrows())),
              ">= 1 cell", len(v4n) > 0)
    log("\n  Binding-leg census over arm A at %d bps (which leg kills each rung, FULL):" % COST0)
    for k, v in a10.bind.value_counts().items():
        log(f"    {v:3d}  {k}")

    # ---------------- V5 RULE 8 walk-forward: IS 2009-2016 chooses, OOS read once
    log("\n================ RULE 8 WALK-FORWARD (IS 2009-2016 chooses b_out; 2017-2026 read once)")
    wf = []
    for pname in panels:
        for c in COSTS:
            sub = grid[(grid.panel == pname) & (grid.arm == "A_bout") & (grid.cost == c)]
            for ch in CHOOSERS:
                p = pick(sub, ch)
                wf.append(dict(panel=pname, cost=c, chooser=ch, b_out=p.dial,
                               is_Sharpe=p.is_Sharpe, is_CAGR=p.is_CAGR, is_MaxDD=p.is_MaxDD,
                               oos_CAGR=p.oos_CAGR, oos_Sharpe=p.oos_Sharpe,
                               oos_MaxDD=p.oos_MaxDD, keep4b_oos=bool(p.keep4b_oos),
                               keep4b=bool(p.keep4b), keep4a_oos=bool(p.keep4a_oos),
                               bind=p.bind))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for pname in panels:
        S, LV = panels[pname]["S"], panels[pname]["LV"]
        log(f"\n  {pname}  (SPY OOS {100*S['oos']['CAGR']:.2f}% / {S['oos']['Sharpe']:.4f} / "
            f"{100*S['oos']['MaxDD']:.2f}%; live OOS {100*LV[COST0]['oos']['CAGR']:.2f}% / "
            f"{LV[COST0]['oos']['Sharpe']:.4f} / {100*LV[COST0]['oos']['MaxDD']:.2f}%)")
        log("    cost  chooser         pick   isSharpe |  oCAGR oSharpe   oMaxDD | 4bOOS 4bFULL 4aOOS")
        for _, r in W[W.panel == pname].iterrows():
            log(f"    {r.cost:4d}  {r.chooser:13s} {r.b_out:5.2f}  {r.is_Sharpe:8.4f} "
                f"| {100*r.oos_CAGR:6.2f} {r.oos_Sharpe:7.4f} {100*r.oos_MaxDD:8.2f} "
                f"|   {int(r.keep4b_oos)}      {int(r.keep4b)}     {int(r.keep4a_oos)}")
    real = W[(W.chooser != "CELL_ALPHA") & (W.cost == COST0)]
    v5 = gate("V5 rule 8 (a legal IS-only chooser's pick clears 4b OOS at %d bps)" % COST0,
              f"{int(real.keep4b_oos.sum())} of {len(real)} (panel,chooser) pairs",
              ">= 1", bool(real.keep4b_oos.any()))

    # ---------------- POST-HOC DIAGNOSTIC (declared post-hoc: NOT one of the pre-stated gates)
    log("\n================ POST-HOC DOMINANCE DIAGNOSTIC (not a pre-stated gate; added after")
    log("  the ladders were read, and reported as such).  A b_out cell is a NEW capital finding")
    log("  only if no cell on a COMPARAND ladder beats it on every axis at once.  D = a comparand")
    log("  cell with CAGR, Sharpe and MaxDD all >= the b_out cell's, in BOTH the FULL and the OOS")
    log("  window, at %d bps." % COST0)
    dom_rows = []
    for pname in panels:
      for cc in COSTS:
        a = grid[(grid.panel == pname) & (grid.arm == "A_bout") & (grid.cost == cc)
                 & grid.keep4b]
        if a.empty:
            log(f"  {pname} @{cc}bps: no b_out rung clears 4b FULL+OOS -- nothing to dominate.")
            continue
        for _, r in a.iterrows():
            others = grid[(grid.panel == pname) & (grid.arm != "A_bout") & (grid.cost == cc)]
            d = others[(others.CAGR >= r.CAGR) & (others.Sharpe >= r.Sharpe)
                       & (others.MaxDD >= r.MaxDD) & (others.oos_CAGR >= r.oos_CAGR)
                       & (others.oos_Sharpe >= r.oos_Sharpe) & (others.oos_MaxDD >= r.oos_MaxDD)]
            log(f"  {pname} @{cc}bps / b_out={r.dial:.2f}  (FULL {100*r.CAGR:.2f}/{r.Sharpe:.4f}/"
                f"{100*r.MaxDD:.2f}  OOS {100*r.oos_CAGR:.2f}/{r.oos_Sharpe:.4f}/"
                f"{100*r.oos_MaxDD:.2f}):  dominated by {len(d)} comparand cell(s)")
            for _, q in d.iterrows():
                log(f"      <- {q.arm} dial {q.dial:.2f}: FULL {100*q.CAGR:.2f}/{q.Sharpe:.4f}/"
                    f"{100*q.MaxDD:.2f}  OOS {100*q.oos_CAGR:.2f}/{q.oos_Sharpe:.4f}/"
                    f"{100*q.oos_MaxDD:.2f}   4b={int(q.keep4b)}")
            dom_rows.append(dict(panel=pname, cost=cc, b_out=r.dial, n_dom=len(d)))
    D = pd.DataFrame(dom_rows)
    dominated = (not D.empty) and bool((D[D.cost == COST0].n_dom > 0).all()) and (D.cost == COST0).any()
    undom = D[D.n_dom == 0] if not D.empty else D
    log(f"  -> at the {COST0} bps headline rung, every 4b-clearing b_out cell is dominated: {dominated}")
    log(f"  -> across ALL cost rungs, UNDOMINATED 4b-clearing b_out cells: {len(undom)}"
        + ("" if undom.empty else "; " + ", ".join(f"{r.panel}@{r.cost}bps/b_out={r.b_out:.2f}"
                                                   for _, r in undom.iterrows())))

    # cost robustness of the 4b-clearing b_out cells and of their dominators
    log("\n  COST ROBUSTNESS of every 4b FULL+OOS cell on any ladder (0/10/25/50 bps):")
    for pname in panels:
        for arm in ("A_bout", "B_gross", "C_sleeve"):
            for d in sorted(grid[(grid.panel == pname) & (grid.arm == arm)].dial.unique()):
                sub = grid[(grid.panel == pname) & (grid.arm == arm) & (grid.dial == d)]
                ok = sub.set_index("cost").keep4b
                if ok.any():
                    log(f"    {pname}/{arm}/{d:.2f}: 4b at "
                        + ", ".join(f"{c}bps={int(ok[c])}" for c in COSTS))

    # ---------------- verdict
    capital = v3 and v4 and v5
    log("\n================ VERDICT")
    log(f"  V1 cheaper-than-gross      : {'PASS' if v1 else 'FAIL'}")
    log(f"  V2 cheapest-of-three       : {'PASS' if v2 else 'FAIL'}")
    log(f"  V3 budget sufficiency      : {'PASS' if v3 else 'FAIL'}")
    log(f"  V4 4b FULL+OOS             : {'PASS' if v4 else 'FAIL'}")
    log(f"  V5 rule 8 chooser reaches  : {'PASS' if v5 else 'FAIL'}")
    verdict = "KEEP-4b candidate" if capital else ("PARK" if (v1 and v4) else "KILL")
    if capital and dominated:
        verdict = "PARK (4b reached but every b_out cell is DOMINATED by a comparand dial)"
    log(f"  MECHANISM (V1/V2): b_out is {'the cheapest' if v2 else ('cheaper than gross' if v1 else 'NOT cheaper')} dial.")
    log(f"  CAPITAL  (V3+V4+V5): {'REACHED' if capital else 'NOT REACHED'}")
    log(f"  POST-HOC dominance   : {'every 4b b_out cell is dominated' if dominated else 'not dominated'}")
    log(f"  VERDICT              : {verdict}")
    log("  THE IDEA'S OWN QUESTION ('is the EXIT THRESHOLD the ONLY dial that spends the budget'):")
    log("  ANSWERED = NO at the %d bps headline rung." % COST0 if (not v1)
        else "  ANSWERED = qualified yes.")
    if not undom.empty:
        log("  QUALIFICATION (post-hoc, stated): b_out IS the only dial reaching 4b at the cost")
        log("  rungs listed above -- a deep exit edge cuts turnover, so it outlives the gross")
        log("  ladder as costs rise.  That is a COST-RUNG fact, not the headline verdict.")

    # ---------------- leaderboard rows
    rows = []
    for pname in panels:
        S, LV = panels[pname]["S"], panels[pname]["LV"]
        a = grid[(grid.panel == pname) & (grid.arm == "A_bout") & (grid.cost == COST0)]
        # the best rung by FULL Sharpe, and the rule-8 pick of IS_SHARPE, both reported
        b = a.loc[a.Sharpe.idxmax()]
        p = pick(a, "IS_SHARPE")
        tags = [("best-FULL-Sharpe", b), ("rule8-IS_SHARPE", p)]
        k = a[a.keep4b]
        if not k.empty:
            tags.append(("4b-cell-DOMINATED-by-gross", k.loc[k.Sharpe.idxmax()]))
        tags.append(("rule8-IS_LEGS", pick(a, "IS_LEGS")))
        for tag, r in tags:
            rows.append(f"| {DATE} | 2237 {SLUG} [{pname}/{tag} b_out={r.dial:.2f}] | "
                        f"{r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | {r.H1:.2f} / {r.H2:.2f} | "
                        f"{LV[COST0]['full']['Sharpe']:.2f} ({LV[COST0]['h1']:.2f}/{LV[COST0]['h2']:.2f}) | "
                        f"{'KEEP-4b' if r.keep4b else ('4bFULL-only' if r.keep4b_full else 'KILL')} "
                        f"(OOS {r.oos_CAGR:.1%}/{r.oos_Sharpe:.2f}/{r.oos_MaxDD:.1%}; SPY OOS "
                        f"{S['oos']['CAGR']:.1%}/{S['oos']['Sharpe']:.2f}/{S['oos']['MaxDD']:.1%}; "
                        f"bind {r.bind}) | {DATE}_{SLUG}_C.py |")
    log("\nLEADERBOARD rows:")
    for r in rows:
        log(r)

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    print(f"\nwrote {Path(OUT).name}.{{grid,walkforward,gates}}.csv and .log.txt")


if __name__ == "__main__":
    main()
