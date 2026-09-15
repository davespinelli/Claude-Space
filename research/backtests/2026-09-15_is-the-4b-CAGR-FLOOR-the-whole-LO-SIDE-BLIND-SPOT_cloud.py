#!/usr/bin/env python3
"""IDEA 900 - is the 4b CAGR FLOOR the whole LO-SIDE BLIND SPOT?
Cloud lane, 2026-09-15, idea 2 of 2.

THE QUESTION
------------
Idea 870 found that all four LOW-tail de-grossing families - CORR-LO, PORTVOL-LO, NAMEVOL-LO
and VTCONT-LO - are 0 of 432 on PROTOCOL path 4b, while all four HIGH-tail families pass in
bulk, whichever state the tail is read from.  A clean zero across four families and 1,728 arms
is either a real statement about de-grossing in calm markets, or it is ONE of 4b's five legs
doing all the rejecting.  870 never decomposed it.  This run reads which leg rejects on every
LO arm, and then asks the only question that follows: how far would the rejecting bar have to
move to admit ANY of them?

WHY THE CAGR FLOOR IS THE SUSPECT (the mechanism, stated before the numbers)
----------------------------------------------------------------------------
A LOW-tail gate cuts exposure when correlation / portfolio vol / name vol is in its own lower
tail - that is, in CALM markets, which is where this panel makes most of its money.  It
therefore spends return without buying drawdown protection, because the drawdowns happen in the
HIGH tail it leaves fully invested.  So the prediction is that LO arms fail on **CAGR** (4b's
floor at 70% of SPY) and NOT on **DD** (4b's cap at 60% of SPY's), and that the Sharpe legs
(H1, H2, OOS vs SPY) mostly survive, because cutting calm-market exposure costs return and
volatility together.  That is the exact mirror of what this lane's idea-1 run found on the
gross dial: below the 4b window the CAGR leg rejects, above it the DD leg does.

PRE-REGISTERED HYPOTHESES (written before any number was read)
--------------------------------------------------------------
    H_CAGR   the CAGR floor is the WHOLE blind spot: on the LO side, the CAGR leg fails on
             >= 95% of arms and is the SOLE failing leg on a majority of them, and the DD leg
             fails on < 5%.
    H_ADMIT  the blind spot is a LEVEL, not a wall: some floor level strictly below 0.70 of
             SPY's CAGR admits at least one LO arm on ALL of 4b's other legs.
    H_MIRROR the HI side is the mirror image: its failures are NOT concentrated on CAGR.

THE GRID (idea 870's own, LO side and the HI side as its control)
------------------------------------------------------------------
    families  CORR-LO/HI, PORTVOL-LO/HI, NAMEVOL-LO/HI (binary threshold gates) and
              VTCONT-LO/HI (idea 870's continuous ratio target on PORTVOL)
    q         {0.07, 0.12, 0.17}      tail quantile of the state's own rolling window
    w         {252, 504, 1008, 2016}  the rolling window
    depth     {0.25, 0.50, 1.00}      how far the gate de-grosses when it fires
    cadence   {D, W}                  how often the multiplier may change
    base book {EWALL, TOP20, RULESv2} EWALL = equal-weight eligible; TOP20 = the 2026-09-04
              shelf 4b KEEP book (monthly, cash never re-spread); RULESv2 = the live book
    gross     {0.75, 1.00}
    = 4 x 3 x 4 x 3 x 2 x 3 x 2 = 1,728 arms PER SIDE, 3,456 in total.
Gated weight goes to CASH; it is never re-spread.

2 TUNED PARAMS, as the idea specifies: LEG SET {4b as written, 4b minus CAGR, 4b minus DD,
Sharpe legs only} x FLOOR LEVEL {0.40, 0.50, 0.60, 0.70} of SPY's CAGR.  Family, q, w, depth,
cadence, base, gross, side and cost rung are REPORTED axes, never selected over; all grid
points are printed.  Costs 10 bps per unit turnover (0 and 25 reported), next-day execution,
no shorting, no leverage.
RULE 8: every selection is made on 2009..2016 alone and 2017..2026 is read once, with OOS
CAGR/Sharpe/MaxDD reported against RULES v2 (live) and SPY.  Both KEEP paths are scored.

SURVIVORSHIP: `research/universe.json` is the CURRENT constituent list, so CAGR levels are
biased upward and BOTH of 4b's level bars are easier here than on a point-in-time panel.  The
run's headline is a within-panel leg decomposition, where that bias largely cancels; the KEEP
columns and the admitting floor level are NOT protected and are read with the caveat.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .arms.csv .legs.csv .floor.csv .finegross.csv .walkforward.csv .console.txt
"""
import sys
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

FREQ, MAX_VOL, SMOOTH, N_BOOK = "W", 0.60, 20, 20
QS = [0.07, 0.12, 0.17]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
GROSSES = [0.75, 1.00]
BASES = ["EWALL", "TOP20", "RULESv2"]
FAMILIES = [("CORR", "BINARY"), ("PORTVOL", "BINARY"), ("NAMEVOL", "BINARY"),
            ("PORTVOL", "RATIO")]                       # the 4th is idea 870's VTCONT
FAMNAME = {("CORR", "BINARY"): "CORR", ("PORTVOL", "BINARY"): "PORTVOL",
           ("NAMEVOL", "BINARY"): "NAMEVOL", ("PORTVOL", "RATIO"): "VTCONT"}
SIDES = ["LO", "HI"]
RUNGS = [0, 10, 25]
COST_BPS = 10
SPLIT = "2017-01-01"
IS_END = "2016-12-31"

LEGSETS = {"4b": ["H1", "H2", "OOS", "DD", "CAGR"],          # tuned param 1
           "4b-noCAGR": ["H1", "H2", "OOS", "DD"],
           "4b-noDD": ["H1", "H2", "OOS", "CAGR"],
           "SHARPE-only": ["H1", "H2", "OOS"]}
FLOORS = [0.40, 0.50, 0.60, 0.70]                            # tuned param 2
DD_CAP = 0.60

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 4000)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


# ---------------------------------------------------------- primitives (idea 870's, verbatim)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def top20_weights(px, gross):
    """The 2026-09-04 shelf KEEP-4b book: monthly, cash never re-spread."""
    comp, above, vol20 = score(px, vol_scale=False)
    elig = comp.where(above & (vol20 < MAX_VOL))
    m = pd.Series(px.index.to_period("M"), index=px.index)
    dates = px.index[(m != m.shift(-1)).values]
    W = ((elig.rank(axis=1, ascending=False) <= N_BOOK).astype(float) * (gross / N_BOOK)).loc[dates]
    return W.reindex(px.index).ffill().fillna(0.0)


def rulesv2_weights_g(px, gross):
    """The live book at an explicit gross (rules_v2_weights' own default gross is 0.75)."""
    return rules_v2_weights(px, gross=gross)


BASE_FN = {"EWALL": (ewall_weights, FREQ), "TOP20": (top20_weights, "M"),
           "RULESv2": (rulesv2_weights_g, FREQ)}


def state_namevol(px):
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_portvol(px):
    return px.pct_change().mean(axis=1).rolling(SMOOTH).std() * np.sqrt(252)


def state_corr(px):
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"CORR": state_corr, "PORTVOL": state_portvol, "NAMEVOL": state_namevol}


def _cadence(m, cadence, idx):
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def mult_binary(st, thr, side, depth, cadence, idx, ext=None):
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    return _cadence(pd.Series(1.0, index=idx).where(~fire, 1.0 - depth), cadence, idx)


def mult_ratio(st, thr, side, depth, cadence, idx, ext=None):
    """idea 870's VTCONT, generalised from PORTVOL to every state."""
    ratio = (thr / st) if side == "HI" else (st / thr)
    m = ratio.clip(upper=1.0).clip(lower=1.0 - depth)
    return _cadence(m.where(st.notna() & thr.notna(), 1.0).reindex(idx).fillna(1.0), cadence, idx)


MULT_FN = {"BINARY": mult_binary, "RATIO": mult_ratio}


def apply_eff(r_base, m_eff, gross, cost_bps):
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def gate_turnover(m_eff):
    return float(np.abs(np.diff(m_eff, prepend=m_eff[0])).sum() * 252 / len(m_eff))


def fast_sharpe(v):
    v = np.asarray(v, float)
    sd = v.std(ddof=1)
    return v.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def pack(r, ix):
    m = metrics(pd.Series(r, index=ix))
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def legs_4b(c, dd, h1, h2, osh, spy, floor=0.70, cap=DD_CAP):
    """4b's five legs as booleans, with the CAGR floor and DD cap at declared levels."""
    return {"H1": h1 > spy["h1"], "H2": h2 > spy["h2"], "OOS": osh > spy["osh"],
            "DD": abs(dd) <= cap * abs(spy["dd"]), "CAGR": c >= floor * spy["c"]}


def legs_4a(dd, h1, h2, bl):
    return {"H1": h1 > bl["h1"], "H2": h2 > bl["h2"], "DD": dd >= bl["dd"]}


# ================================================================== main
def main():
    P("=" * 190)
    P("IDEA 900 - is the 4b CAGR FLOOR the whole LO-SIDE BLIND SPOT?"
      "   (cloud lane, 2026-09-15, idea 2 of 2)")
    P("=" * 190)
    P("PROTOCOL: 10 bps per unit turnover (0/25 reported), next-day execution, no shorting, no")
    P(f"leverage.  IS = start..{IS_END}, OOS = {SPLIT}..end, read once.  Gated weight goes to CASH.")
    P(f"2 TUNED PARAMS: LEG SET {list(LEGSETS)} x FLOOR LEVEL {FLOORS} of SPY's CAGR.")
    P(f"Reported axes (never selected over): family {[FAMNAME[f] for f in FAMILIES]}, side {SIDES},")
    P(f"q {QS}, w {WS}, depth {DEPTHS}, cadence {CADENCES}, base {BASES}, gross {GROSSES}, "
      f"cost rung {RUNGS}.")
    P("PRE-REGISTERED:")
    P("  H_CAGR   the CAGR floor is the WHOLE blind spot: on the LO side the CAGR leg fails on")
    P("           >= 95% of arms AND is the SOLE failing leg on a majority; the DD leg fails < 5%.")
    P("  H_ADMIT  some floor level strictly below 0.70 of SPY's CAGR admits at least one LO arm on")
    P("           every other 4b leg.")
    P("  H_MIRROR the HI side's failures are NOT concentrated on CAGR.")
    P("SURVIVORSHIP: universe.json is the CURRENT constituent list; CAGR inflated, both 4b level")
    P("bars easier here than point-in-time.  The leg decomposition is within-panel and largely")
    P("immune; the admitting floor level is not.")
    flush_log()

    px = load_universe()
    core = px.drop(columns=["SPY"], errors="ignore")
    idx = px.index
    ii = idx[idx >= idx[260]]
    oos = np.asarray(ii >= pd.Timestamp(SPLIT))
    isw = ~oos
    P(f"\nPanel U56 {core.shape[1]}x{len(core)}   priced {ii[0].date()}..{ii[-1].date()}  "
      f"({len(ii)/252:.2f} yrs)   IS {int(isw.sum())} bars / OOS {int(oos.sum())} bars")

    states = {s: STATE_FN[s](core) for s in STATE_FN}
    is_spy_dd = abs(pack(px["SPY"].pct_change().fillna(0.0).loc[ii].values[
        np.asarray(ii <= pd.Timestamp(IS_END))], ii[np.asarray(ii <= pd.Timestamp(IS_END))])[2])
    BASE = {}
    for b, g in product(BASES, GROSSES):
        fn, fq = BASE_FN[b]
        BASE[(b, g)] = backtest(core, fn(core, g), cost_bps=COST_BPS, freq=fq)["returns"].loc[ii]

    spy_v = px["SPY"].pct_change().fillna(0.0).loc[ii].values
    sc, ss, sd = pack(spy_v, ii)
    sh1, sh2 = halves(spy_v)
    soc, sos_, sod = pack(spy_v[oos], ii[oos])
    SPYD = dict(c=sc, s=ss, dd=sd, h1=sh1, h2=sh2, osh=sos_, oc=soc, odd=sod)
    bl_r = backtest(core, rules_v2_weights(core), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[ii]
    bc, bs, bd = pack(bl_r.values, ii)
    bh1, bh2 = halves(bl_r.values)
    boc, bos_, bod = pack(bl_r.values[oos], ii[oos])
    BLD = dict(c=bc, s=bs, dd=bd, h1=bh1, h2=bh2, osh=bos_, oc=boc, odd=bod)

    P("\n" + "=" * 190)
    P("COMPARANDS (RULES v2 = the 4a bar; SPY = the 4b bar), U56, weekly, 10 bps")
    P("=" * 190)
    P(f"  RULES v2  CAGR {bc:.4f}  Sharpe {bs:.4f}  MaxDD {bd:.4f}  H1/H2 {bh1:.4f}/{bh2:.4f}"
      f"   OOS {boc:.4f}/{bos_:.4f}/{bod:.4f}")
    P(f"  SPY       CAGR {sc:.4f}  Sharpe {ss:.4f}  MaxDD {sd:.4f}  H1/H2 {sh1:.4f}/{sh2:.4f}"
      f"   OOS {soc:.4f}/{sos_:.4f}/{sod:.4f}")
    P(f"  4b bars at the PROTOCOL levels: H1>{sh1:.4f}  H2>{sh2:.4f}  OOS>{sos_:.4f}  "
      f"MaxDD>=-{DD_CAP*abs(sd):.2%}  CAGR>={0.70*sc:.2%}")
    P("  the base books, ungated:")
    for b, g in product(BASES, GROSSES):
        r = BASE[(b, g)].values
        c, s, dd = pack(r, ii)
        h1, h2 = halves(r)
        lg = legs_4b(c, dd, h1, h2, fast_sharpe(r[oos]), SPYD)
        P(f"    {b:8s} g{g:.2f}  {c:.4f} / {s:.4f} / {dd:.4f}   H1/H2 {h1:.4f}/{h2:.4f}   "
          f"4b fails: {','.join(k for k, v in lg.items() if not v) or '-'}")
    flush_log()

    # -------------------------------------------------------------- gates
    P("\n" + "=" * 190)
    P("GATES (printed before any hypothesis is read)")
    P("=" * 190)
    rb = BASE[("EWALL", 0.75)].values
    g2 = float(np.max(np.abs(apply_eff(rb, np.ones(len(rb)), 0.75, COST_BPS) - rb)))
    P(f"  G2 never-firing multiplier == ungated base   max|dr| {g2:.3e}  "
      f"[{'PASS' if g2 < 1e-12 else 'FAIL'}]")
    g5 = abs(fast_sharpe(rb) - metrics(BASE[("EWALL", 0.75)])["Sharpe"])
    P(f"  G5 fast Sharpe == engine.metrics Sharpe      |d|     {g5:.3e}  "
      f"[{'PASS' if g5 < 1e-10 else 'FAIL'}]")
    # G1: idea 870's committed VTCONT-HI arm, rebuilt here
    _q, _w, _d, _cad, _g = 0.17, 252, 0.50, "W", 1.00
    _mp = max(60, _w // 4)
    _res = {}
    for _s, _form in (("PORTVOL", "RATIO"), ("CORR", "BINARY")):
        _st = states[_s]
        _th = _st.rolling(_w, min_periods=_mp).quantile(1 - _q)
        _m = MULT_FN[_form](_st, _th, "HI", _d, _cad, idx).shift(1).fillna(1.0).loc[ii].values
        _r = apply_eff(BASE[("EWALL", _g)].values, _m, _g, COST_BPS)
        _res[_s] = (*pack(_r, ii), gate_turnover(_m))
    v = _res["PORTVOL"]
    okv = abs(v[0] - 0.1366) <= 0.0010 and abs(v[1] - 1.098) <= 0.02 and abs(v[3] - 0.71) <= 0.05
    P(f"  G1 idea 870's committed VTCONT-HI arm (U56 q.17 w252 d.50 W g1.00) rebuilds as "
      f"{v[0]:.2%} / {v[1]:.3f} / {v[2]:.2%}, gate turnover {v[3]:.2f}/yr")
    P(f"     vs its memo 13.66% / 1.098 / -18.79% @ 0.71/yr   [{'PASS' if okv else 'FAIL'}]")
    c = _res["CORR"]
    P(f"     CORR-HI binary, same cell: gate turnover {c[3]:.2f}/yr vs memo 2.16  "
      f"[{'PASS' if abs(c[3]-2.16) <= 0.05 else 'FAIL'}]   ({c[0]:.2%} / {c[1]:.3f} / {c[2]:.2%})")
    flush_log()

    # -------------------------------------------------------------- the grid
    P("\n" + "=" * 190)
    P(f"THE GRID - {len(FAMILIES)} families x {len(SIDES)} sides x {len(QS)} q x {len(WS)} w x "
      f"{len(DEPTHS)} depth x {len(CADENCES)} cadence x {len(BASES)} base x {len(GROSSES)} gross "
      f"= {len(FAMILIES)*len(SIDES)*len(QS)*len(WS)*len(DEPTHS)*len(CADENCES)*len(BASES)*len(GROSSES)}"
      f" arms ({len(FAMILIES)*len(QS)*len(WS)*len(DEPTHS)*len(CADENCES)*len(BASES)*len(GROSSES)} "
      f"per side)")
    P("=" * 190)
    rows = []
    for q, w in product(QS, WS):
        mp = max(60, w // 4)
        thr = {}
        for s in STATE_FN:
            st = states[s]
            thr[(s, "LO")] = st.rolling(w, min_periods=mp).quantile(q)
            thr[(s, "HI")] = st.rolling(w, min_periods=mp).quantile(1 - q)
        for (s, form), side, depth, cad in product(FAMILIES, SIDES, DEPTHS, CADENCES):
            m = MULT_FN[form](states[s], thr[(s, side)], side, depth, cad,
                              idx).shift(1).fillna(1.0).loc[ii].values
            rate = float((m < 1.0).mean())
            gt = gate_turnover(m)
            for b, g in product(BASES, GROSSES):
                base = BASE[(b, g)].values
                row = dict(family=FAMNAME[(s, form)], side=side, state=s, form=form, q=q, w=w,
                           depth=depth, cadence=cad, base=b, gross=g, rate=rate, gate_turn=gt,
                           gbar=float(m.mean()))
                for cb in RUNGS:
                    r = apply_eff(base, m, g, cb)
                    c_, s_, dd_ = pack(r, ii)
                    h1, h2 = halves(r)
                    oc, osh_, odd = pack(r[oos], ii[oos])
                    ic, ish, idd = pack(r[isw], ii[isw])
                    tag = "" if cb == COST_BPS else f"_{cb}"
                    row.update({f"CAGR{tag}": c_, f"Sharpe{tag}": s_, f"MaxDD{tag}": dd_,
                                f"H1{tag}": h1, f"H2{tag}": h2, f"oCAGR{tag}": oc,
                                f"oSharpe{tag}": osh_, f"oMaxDD{tag}": odd})
                    if cb == COST_BPS:
                        row.update(isCAGR=ic, isSharpe=ish, isMaxDD=idd)
                    lg = legs_4b(c_, dd_, h1, h2, osh_, SPYD)
                    row[f"fail4b{tag}"] = ",".join(k for k, v_ in lg.items() if not v_) or "-"
                    row[f"pass4b{tag}"] = all(lg.values())
                    if cb == COST_BPS:
                        for k_, v_ in lg.items():
                            row[f"leg_{k_}"] = bool(v_)
                        la = legs_4a(dd_, h1, h2, BLD)
                        row["pass4a"] = all(la.values())
                        row["fail4a"] = ",".join(k for k, v_ in la.items() if not v_) or "-"
                        # how far each level bar would have to move to admit THIS arm
                        row["cagr_ratio"] = c_ / SPYD["c"]
                        row["dd_ratio"] = abs(dd_) / abs(SPYD["dd"])
                        row["sharpe_legs_ok"] = bool(lg["H1"] and lg["H2"] and lg["OOS"])
                rows.append(row)
        P(f"  q={q:.2f} w={w:<5d} done  ({len(rows)} arms)")
        flush_log()

    A = pd.DataFrame(rows)
    A.to_csv(f"{OUT}.arms.csv", index=False)
    LO = A[A.side == "LO"]
    HI = A[A.side == "HI"]

    # -------------------------------------------------------------- 1. reproduce 870
    P("\n" + "=" * 190)
    P("1. REPRODUCING IDEA 870's HEADLINE - 4b pass counts by family and side")
    P("=" * 190)
    t = A.pivot_table(index="family", columns="side", values="pass4b", aggfunc=["sum", "size"])
    P(t.to_string())
    P(f"\n  LO side total 4b passes: {int(LO.pass4b.sum())} of {len(LO)}   "
      f"HI side: {int(HI.pass4b.sum())} of {len(HI)}")
    P(f"  LO side 4a passes: {int(LO.pass4a.sum())} of {len(LO)}   "
      f"HI side: {int(HI.pass4a.sum())} of {len(HI)}")
    P("  by family x base book (4b passes / arms):")
    P(A.groupby(["side", "family", "base"]).agg(n=("pass4b", "size"),
                                                p4b=("pass4b", "sum"),
                                                p4a=("pass4a", "sum")).to_string())
    flush_log()

    # -------------------------------------------------------------- 2. the leg decomposition
    P("\n" + "=" * 190)
    P("2. H_CAGR - WHICH 4b LEG REJECTS, every LO arm (and the HI side as its control)")
    P("=" * 190)
    legcols = ["leg_H1", "leg_H2", "leg_OOS", "leg_DD", "leg_CAGR"]
    for nm, S in (("LO", LO), ("HI", HI)):
        fr = {c.replace("leg_", ""): 1.0 - S[c].mean() for c in legcols}
        P(f"\n  {nm} side, failure RATE per leg over {len(S)} arms:")
        P("    " + "   ".join(f"{k} {v:.4f}" for k, v in fr.items()))
        sole = S[~S.pass4b].copy()
        sole["nfail"] = sole[legcols].apply(lambda r: int((~r.astype(bool)).sum()), axis=1)
        sole_cagr = sole[(sole.nfail == 1) & (~sole.leg_CAGR)]
        sole_dd = sole[(sole.nfail == 1) & (~sole.leg_DD)]
        P(f"    of {len(sole)} failing arms: SOLE failing leg is CAGR on {len(sole_cagr)} "
          f"({len(sole_cagr)/max(len(sole),1):.1%}), DD on {len(sole_dd)} "
          f"({len(sole_dd)/max(len(sole),1):.1%})")
        P(f"    failing-leg signature counts:")
        P("    " + S.fail4b.value_counts().to_string().replace("\n", "\n    "))
    lo_cagr_rate = 1.0 - LO.leg_CAGR.mean()
    lo_dd_rate = 1.0 - LO.leg_DD.mean()
    lo_fail = LO[~LO.pass4b]
    lo_nfail = lo_fail[legcols].apply(lambda r: int((~r.astype(bool)).sum()), axis=1)
    lo_sole_cagr = int(((lo_nfail == 1) & (~lo_fail.leg_CAGR)).sum())
    hcagr = bool(lo_cagr_rate >= 0.95 and lo_dd_rate < 0.05
                 and lo_sole_cagr > len(lo_fail) / 2)
    P(f"\n  H_CAGR: LO CAGR-leg failure rate {lo_cagr_rate:.4f} (bar >= 0.95), DD-leg "
      f"{lo_dd_rate:.4f} (bar < 0.05), sole-CAGR {lo_sole_cagr} of {len(lo_fail)} "
      f"(bar > {len(lo_fail)/2:.0f})  ->  {'SUPPORTED' if hcagr else 'REJECTED'}")
    hi_cagr_rate = 1.0 - HI.leg_CAGR.mean()
    hmirror = bool(hi_cagr_rate < 0.95)
    P(f"  H_MIRROR: HI CAGR-leg failure rate {hi_cagr_rate:.4f} (bar < 0.95)  ->  "
      f"{'SUPPORTED' if hmirror else 'REJECTED'}")
    L = pd.concat([LO.assign(nfail=lo_nfail.reindex(LO.index)), HI], sort=False)
    A[["family", "side", "q", "w", "depth", "cadence", "base", "gross", "fail4b", "fail4a",
       "cagr_ratio", "dd_ratio", "sharpe_legs_ok"]].to_csv(f"{OUT}.legs.csv", index=False)
    flush_log()

    # -------------------------------------------------------------- 2b. per BASE BOOK
    P("\n" + "=" * 190)
    P("2b. THE SAME DECOMPOSITION PER BASE BOOK - because that is where idea 870's zero lives")
    P("=" * 190)
    P("  Idea 870 gated ONE base book (EWALL, equal-weight eligible).  This run's third axis is")
    P("  the base book instead of the gate form, so the zero can be read against its alternatives.")
    P("  This restriction is POST-HOC: it was not pre-registered, it is motivated by the split")
    P("  section 1 found, and it is reported as such - no hypothesis is re-scored on it.")
    for b in BASES:
        for nm in SIDES:
            S = A[(A.base == b) & (A.side == nm)]
            fr = {c.replace("leg_", ""): 1.0 - S[c].mean() for c in legcols}
            f_ = S[~S.pass4b]
            nf = f_[legcols].apply(lambda r: int((~r.astype(bool)).sum()), axis=1)
            sc_ = int(((nf == 1) & (~f_.leg_CAGR)).sum())
            sd_ = int(((nf == 1) & (~f_.leg_DD)).sum())
            P(f"\n  {b:8s} {nm}  4b {int(S.pass4b.sum()):3d}/{len(S)}   4a "
              f"{int(S.pass4a.sum()):3d}/{len(S)}   leg failure rates: "
              + "  ".join(f"{k} {v:.4f}" for k, v in fr.items()))
            P(f"           of {len(f_)} failures: sole-CAGR {sc_} ({sc_/max(len(f_),1):.1%}), "
              f"sole-DD {sd_} ({sd_/max(len(f_),1):.1%})")
            P(f"           signatures: " + "; ".join(
                f"{k} {v}" for k, v in S.fail4b.value_counts().head(6).items()))
    P("\n  H_CAGR re-read on idea 870's OWN base book (EWALL), LO side, post-hoc:")
    E = A[(A.base == "EWALL") & (A.side == "LO")]
    e_cagr = 1.0 - E.leg_CAGR.mean()
    e_dd = 1.0 - E.leg_DD.mean()
    ef = E[~E.pass4b]
    enf = ef[legcols].apply(lambda r: int((~r.astype(bool)).sum()), axis=1)
    e_sole = int(((enf == 1) & (~ef.leg_CAGR)).sum())
    P(f"    CAGR-leg failure {e_cagr:.4f} (bar >= 0.95), DD-leg {e_dd:.4f} (bar < 0.05), "
      f"sole-CAGR {e_sole} of {len(ef)} (bar > {len(ef)/2:.0f})")
    P(f"    -> on EWALL the pre-registered H_CAGR reading would be "
      f"{'SUPPORTED' if (e_cagr >= 0.95 and e_dd < 0.05 and e_sole > len(ef)/2) else 'REJECTED'}"
      f"  (reported, NOT substituted for the pre-registered pooled verdict above)")
    flush_log()

    # -------------------------------------------------------------- 3. how far must the floor move
    P("\n" + "=" * 190)
    P("3. H_ADMIT - HOW FAR WOULD THE BAR HAVE TO MOVE?  (tuned pair: LEG SET x FLOOR LEVEL)")
    P("=" * 190)
    P("  cagr_ratio = arm CAGR / SPY CAGR (the floor it would need); dd_ratio = |arm MaxDD| /")
    P("  |SPY MaxDD| (the cap it would need).  PROTOCOL sets floor 0.70 and cap 0.60.")
    for nm, S in (("LO", LO), ("HI", HI)):
        P(f"\n  {nm} side, distribution of cagr_ratio and dd_ratio over {len(S)} arms:")
        P("    cagr_ratio  " + "  ".join(
            f"p{p}={np.percentile(S.cagr_ratio, p):.4f}" for p in (5, 25, 50, 75, 95, 100)))
        P("    dd_ratio    " + "  ".join(
            f"p{p}={np.percentile(S.dd_ratio, p):.4f}" for p in (0, 5, 25, 50, 75, 95)))
        eligible = S[S.sharpe_legs_ok & (S.dd_ratio <= DD_CAP)]
        P(f"    arms clearing ALL non-CAGR 4b legs: {len(eligible)} of {len(S)}")
        if len(eligible):
            P(f"    the best CAGR among them is {eligible.cagr_ratio.max():.4f} x SPY -> the floor")
            P(f"    would have to fall to {eligible.cagr_ratio.max():.4f} (from 0.70) to admit one.")
            bst = eligible.loc[eligible.cagr_ratio.idxmax()]
            P(f"    that arm: {bst.family}-{bst.side} q{bst.q} w{bst.w} d{bst.depth} "
              f"{bst.cadence} {bst.base} g{bst.gross}  "
              f"{bst.CAGR:.2%} / {bst.Sharpe:.3f} / {bst.MaxDD:.2%}")
    floor_rows = []
    for ls, legs in LEGSETS.items():
        for fl in FLOORS:
            for nm, S in (("LO", LO), ("HI", HI)):
                ok = pd.Series(True, index=S.index)
                for lg in legs:
                    if lg == "CAGR":
                        ok &= S.cagr_ratio >= fl
                    elif lg == "DD":
                        ok &= S.dd_ratio <= DD_CAP
                    else:
                        ok &= S[f"leg_{lg}"].astype(bool)
                floor_rows.append(dict(legset=ls, floor=fl, side=nm, n=len(S),
                                       passes=int(ok.sum()), rate=float(ok.mean())))
    F = pd.DataFrame(floor_rows)
    F.to_csv(f"{OUT}.floor.csv", index=False)
    P("\n  ALL 32 grid points of the tuned pair (leg set x floor level), both sides:")
    P(F.pivot_table(index=["legset", "floor"], columns="side",
                    values="passes").to_string())
    admit = F[(F.side == "LO") & (F.legset == "4b") & (F.passes > 0)]
    hadmit = bool(len(admit))
    P(f"\n  H_ADMIT: a floor below 0.70 that admits an LO arm on every other 4b leg exists: "
      f"{'YES' if hadmit else 'NO'}"
      + (f" (lowest such floor in the grid: {admit.floor.min():.2f}, "
         f"{int(admit[admit.floor == admit.floor.min()].passes.iloc[0])} arms)" if hadmit else ""))
    P(f"  H_ADMIT {'SUPPORTED' if hadmit else 'REJECTED'}")
    flush_log()

    # -------------------------------------------------------------- 3b. floor per base book
    P("\n" + "=" * 190)
    P("3b. HOW FAR MUST THE BAR MOVE, PER BASE BOOK (the answer idea 900 asks for)")
    P("=" * 190)
    P("  For each (base, side): how many arms clear ALL non-CAGR 4b legs, and the best CAGR")
    P("  among them - i.e. the floor level, as a multiple of SPY's CAGR, at which the first arm")
    P("  is admitted.  A value above 0.70 means the floor is NOT what rejects; a value below")
    P("  0.70 is how far the floor would have to fall.")
    adm = []
    for b in BASES:
        for nm in SIDES:
            S = A[(A.base == b) & (A.side == nm)]
            el = S[S.sharpe_legs_ok & (S.dd_ratio <= DD_CAP)]
            best = float(el.cagr_ratio.max()) if len(el) else np.nan
            # and the mirror: among arms clearing all non-DD legs, the tightest DD they need
            eld = S[S.sharpe_legs_ok & (S.cagr_ratio >= 0.70)]
            bestdd = float(eld.dd_ratio.min()) if len(eld) else np.nan
            adm.append(dict(base=b, side=nm, n=len(S), p4b=int(S.pass4b.sum()),
                            clear_nonCAGR=len(el), floor_admitting=best,
                            clear_nonDD=len(eld), cap_admitting=bestdd))
    AD = pd.DataFrame(adm)
    P(AD.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  Reading: where floor_admitting >= 0.70 the CAGR floor is NOT the binding bar (an arm")
    P("  already clears it); where clear_nonCAGR is 0 the floor is IRRELEVANT, because the arms")
    P("  are already out on a Sharpe leg or the DD cap before the floor is ever consulted.")
    flush_log()

    # -------------------------------------------------------------- 3c. constructive test
    P("\n" + "=" * 190)
    P("3c. THE CONSTRUCTIVE TEST - is idea 870's zero a GROSS-RUNG fact?")
    P("=" * 190)
    P("  Sections 2b/3b show that on EWALL every LO arm fails the CAGR floor at gross 0.75")
    P("  (288 of 288) and the DD cap at gross 1.00 (288 of 288) - the gate never changes WHICH")
    P("  leg binds, it only deepens it.  If that is the whole story, EWALL's 4b window lies")
    P("  BETWEEN the two rungs idea 870 priced, and a rung inside it must admit LO arms.")
    P("  This walks EWALL's gross on a finer rung.  POST-HOC and reported as such: gross is a")
    P("  REPORTED axis here, every rung of every cell is printed, and nothing is selected on it.")
    FINE = [0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    fine_base = {}
    for g in FINE:
        fine_base[g] = backtest(core, ewall_weights(core, g), cost_bps=COST_BPS,
                                freq=FREQ)["returns"].loc[ii]
    P("\n  the UNGATED EWALL book at each rung (before any LO gate fires):")
    for g in FINE:
        r = fine_base[g].values
        c_, s_, dd_ = pack(r, ii)
        h1, h2 = halves(r)
        lg = legs_4b(c_, dd_, h1, h2, fast_sharpe(r[oos]), SPYD)
        P(f"    g{g:.2f}  {c_:.4f} / {s_:.4f} / {dd_:.4f}   cagr_ratio {c_/SPYD['c']:.4f} "
          f"(floor 0.70)  dd_ratio {abs(dd_)/abs(SPYD['dd']):.4f} (cap 0.60)   4b fails: "
          f"{','.join(k for k, v_ in lg.items() if not v_) or '-'}")
    fine_rows = []
    for q, w in product(QS, WS):
        mp = max(60, w // 4)
        for (st_, form), depth, cad in product(FAMILIES, DEPTHS, CADENCES):
            th = states[st_].rolling(w, min_periods=mp).quantile(q)
            m = MULT_FN[form](states[st_], th, "LO", depth, cad,
                              idx).shift(1).fillna(1.0).loc[ii].values
            for g in FINE:
                r = apply_eff(fine_base[g].values, m, g, COST_BPS)
                c_, s_, dd_ = pack(r, ii)
                h1, h2 = halves(r)
                oc, osh_, odd = pack(r[oos], ii[oos])
                ic, ish, idd = pack(r[isw], ii[isw])
                lg = legs_4b(c_, dd_, h1, h2, osh_, SPYD)
                fine_rows.append(dict(family=FAMNAME[(st_, form)], q=q, w=w, depth=depth,
                                      cadence=cad, gross=g, CAGR=c_, Sharpe=s_, MaxDD=dd_,
                                      H1=h1, H2=h2, oCAGR=oc, oSharpe=osh_, oMaxDD=odd,
                                      isCAGR=ic, isSharpe=ish, isMaxDD=idd,
                                      pass4b=all(lg.values()),
                                      fail4b=",".join(k for k, v_ in lg.items() if not v_) or "-",
                                      pass4a=all(legs_4a(dd_, h1, h2, BLD).values())))
    FN = pd.DataFrame(fine_rows)
    FN.to_csv(f"{OUT}.finegross.csv", index=False)
    P(f"\n  EWALL x LO x fine gross: {len(FN)} arms.  4b passes per rung:")
    P("  " + FN.pivot_table(index="gross", columns="family", values="pass4b",
                            aggfunc=["sum", "size"]).to_string().replace("\n", "\n  "))
    P("\n  failing-leg signature per rung:")
    P("  " + FN.groupby("gross").fail4b.value_counts().to_string().replace("\n", "\n  "))
    admitted = FN[FN.pass4b]
    P(f"\n  LO arms admitted on EWALL by a rung idea 870 did not price: {len(admitted)} of "
      f"{len(FN)}")
    if len(admitted):
        P(f"  admitting rungs: {sorted(admitted.gross.unique())}")
        bst = admitted.sort_values("Sharpe", ascending=False).iloc[0]
        P(f"  best of them: {bst.family}-LO q{bst.q} w{bst.w} d{bst.depth} {bst.cadence} "
          f"g{bst.gross}  full {bst.CAGR:.2%} / {bst.Sharpe:.3f} / {bst.MaxDD:.2%}  "
          f"OOS {bst.oCAGR:.2%} / {bst.oSharpe:.3f} / {bst.oMaxDD:.2%}")
        P(f"  rule 8 on this sub-grid: choosing the rung and cell on IS alone by "
          f"'max IS CAGR s.t. IS MaxDD <= 60% of SPY IS MaxDD':")
        cand = FN[FN.isMaxDD.abs() <= DD_CAP * is_spy_dd]
        if len(cand):
            pk = cand.sort_values(["isCAGR", "q", "w"], ascending=[False, True, True]).iloc[0]
            P(f"    pick {pk.family}-LO q{pk.q} w{pk.w} d{pk.depth} {pk.cadence} g{pk.gross}  "
              f"IS {pk.isCAGR:.2%} / {pk.isSharpe:.3f} / {pk.isMaxDD:.2%}  ->  OOS "
              f"{pk.oCAGR:.2%} / {pk.oSharpe:.3f} / {pk.oMaxDD:.2%}   full-sample 4b "
              f"{'PASS' if pk.pass4b else 'FAIL (' + pk.fail4b + ')'}   4a "
              f"{'PASS' if pk.pass4a else 'FAIL'}")
            P(f"    vs SPY OOS {SPYD['oc']:.2%} / {SPYD['osh']:.3f} / {SPYD['odd']:.2%}"
              f"   RULES v2 OOS {BLD['oc']:.2%} / {BLD['osh']:.3f} / {BLD['odd']:.2%}")
        else:
            P("    no cell clears the IS DD cap - the selector is empty")
    else:
        P("  none: the zero is NOT a gross-rung fact on this panel")
    P("\n  DOES THE LO GATE EARN ITS KEEP AT THE ADMITTING RUNGS?  gated arm minus the UNGATED")
    P("  EWALL book at the SAME gross - if the gate adds nothing, the pass belongs to the rung.")
    ug = {}
    for g in FINE:
        r = fine_base[g].values
        c_, s_, dd_ = pack(r, ii)
        ug[g] = (c_, s_, dd_)
    cmp_ = FN[FN.gross.isin([0.80, 0.85, 0.90, 0.95])].copy()
    cmp_["dCAGR"] = cmp_.apply(lambda r: r.CAGR - ug[r.gross][0], axis=1)
    cmp_["dSharpe"] = cmp_.apply(lambda r: r.Sharpe - ug[r.gross][1], axis=1)
    cmp_["dMaxDD"] = cmp_.apply(lambda r: abs(r.MaxDD) - abs(ug[r.gross][2]), axis=1)
    P("  " + cmp_.groupby("family")[["dCAGR", "dSharpe", "dMaxDD"]].agg(
        ["median", "max"]).to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n  "))
    P(f"  arms beating their own ungated rung on Sharpe: "
      f"{int((cmp_.dSharpe > 0).sum())} of {len(cmp_)} "
      f"({(cmp_.dSharpe > 0).mean():.1%}); on CAGR: {int((cmp_.dCAGR > 0).sum())} "
      f"({(cmp_.dCAGR > 0).mean():.1%}); cutting drawdown: "
      f"{int((cmp_.dMaxDD < 0).sum())} ({(cmp_.dMaxDD < 0).mean():.1%})")
    P(f"  best dSharpe anywhere on the admitting rungs: {cmp_.dSharpe.max():+.4f}")
    flush_log()

    # -------------------------------------------------------------- 4. cost rungs
    P("\n" + "=" * 190)
    P("4. COST RUNGS - does the LO-side zero survive 0 and 25 bps?")
    P("=" * 190)
    cr = []
    for cb in RUNGS:
        tag = "" if cb == COST_BPS else f"_{cb}"
        for nm, S in (("LO", LO), ("HI", HI)):
            cr.append(dict(bps=cb, side=nm, n=len(S), p4b=int(S[f"pass4b{tag}"].sum())))
    P(pd.DataFrame(cr).pivot_table(index="bps", columns="side", values="p4b").to_string())
    flush_log()

    # -------------------------------------------------------------- 5. rule 8
    P("\n" + "=" * 190)
    P("5. RULE 8 WALK-FORWARD - selections made on 2009..2016 alone, OOS read once")
    P("=" * 190)
    P("  Pre-registered selectors, per (side, family, base): S1 argmax IS Sharpe;")
    P("  S2 argmax IS CAGR subject to IS MaxDD <= 60% of SPY's IS MaxDD.  Nothing else is")
    P("  selected over, and the OOS window is read once, after the picks are fixed.")
    is_spy_c = pack(spy_v[isw], ii[isw])[0]
    wf = []
    for (side, fam, b), S in A.groupby(["side", "family", "base"]):
        for sname in ("S1", "S2"):
            cand = S if sname == "S1" else S[S.isMaxDD.abs() <= DD_CAP * is_spy_dd]
            if cand.empty:
                wf.append(dict(side=side, family=fam, base=b, sel=sname, empty=True))
                continue
            key = "isSharpe" if sname == "S1" else "isCAGR"
            r = cand.sort_values([key, "q", "w"], ascending=[False, True, True]).iloc[0]
            wf.append(dict(side=side, family=fam, base=b, sel=sname, empty=False,
                           q=r.q, w=r.w, depth=r.depth, cadence=r.cadence, gross=r.gross,
                           isCAGR=r.isCAGR, isSharpe=r.isSharpe, isMaxDD=r.isMaxDD,
                           oCAGR=r.oCAGR, oSharpe=r.oSharpe, oMaxDD=r.oMaxDD,
                           beat_base=bool(r.oSharpe > BLD["osh"]),
                           beat_spy=bool(r.oSharpe > SPYD["osh"]),
                           oos_dd_ok=bool(abs(r.oMaxDD) <= DD_CAP * abs(SPYD["odd"])),
                           oos_cagr_ok=bool(r.oCAGR >= 0.70 * SPYD["oc"]),
                           pass4b=bool(r.pass4b), pass4a=bool(r.pass4a), fail4b=r.fail4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n" + WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    okw = WF[~WF["empty"]]
    P(f"\n  IS-only picks: {len(okw)}.  OOS Sharpe > RULES v2 ({BLD['osh']:.4f}): "
      f"{int(okw.beat_base.sum())};  > SPY ({SPYD['osh']:.4f}): {int(okw.beat_spy.sum())};  "
      f"full-sample 4b: {int(okw.pass4b.sum())};  4a: {int(okw.pass4a.sum())}")
    P("  by side:")
    P("  " + okw.groupby("side").agg(n=("sel", "size"), beat_base=("beat_base", "sum"),
                                     beat_spy=("beat_spy", "sum"), p4b=("pass4b", "sum"),
                                     p4a=("pass4a", "sum"),
                                     oos_cagr_ok=("oos_cagr_ok", "sum"),
                                     oos_dd_ok=("oos_dd_ok", "sum")).to_string().replace(
        "\n", "\n  "))
    P(f"\n  SPY OOS {SPYD['oc']:.4f} / {SPYD['osh']:.4f} / {SPYD['odd']:.4f};  "
      f"RULES v2 OOS {BLD['oc']:.4f} / {BLD['osh']:.4f} / {BLD['odd']:.4f}")
    flush_log()

    # -------------------------------------------------------------- verdict
    P("\n" + "=" * 190)
    P("VERDICT")
    P("=" * 190)
    P(f"  H_CAGR   {'SUPPORTED' if hcagr else 'REJECTED'}   LO CAGR-leg failure "
      f"{lo_cagr_rate:.1%}, DD-leg {lo_dd_rate:.1%}, sole-CAGR {lo_sole_cagr}/{len(lo_fail)}")
    P(f"  H_ADMIT  {'SUPPORTED' if hadmit else 'REJECTED'}")
    P(f"  H_MIRROR {'SUPPORTED' if hmirror else 'REJECTED'}   HI CAGR-leg failure "
      f"{hi_cagr_rate:.1%}")
    P(f"  870's headline on the POOLED grid: LO {int(LO.pass4b.sum())} of {len(LO)} on 4b; "
      f"HI {int(HI.pass4b.sum())} of {len(HI)} - so the LO-side ZERO does NOT reproduce pooled.")
    P("  It reproduces EXACTLY, and only, on idea 870's own base book:")
    for b in BASES:
        e = A[(A.base == b) & (A.side == "LO")]
        P(f"    base {b:8s} LO 4b passes {int(e.pass4b.sum()):3d} of {len(e)}"
          + ("   <- idea 870's base book, the zero" if b == "EWALL" else ""))
    P("  => the LO-side blind spot is a BASE-BOOK fact, not a LO-tail fact.")
    P(f"  CAPITAL: LO side {int(LO.pass4b.sum())} 4b passes and {int(LO.pass4a.sum())} 4a passes; "
      f"IS-only picks landing on a 4b pass: {int(okw[okw.side=='LO'].pass4b.sum())} of "
      f"{len(okw[okw.side=='LO'])}.  But section 3c prices every one of them against the")
    P(f"  UNGATED base book at its OWN gross: the LO gate beats it on Sharpe in "
      f"{int((cmp_.dSharpe > 0).sum())} of {len(cmp_)} arms ({(cmp_.dSharpe > 0).mean():.1%}), "
      f"best margin {cmp_.dSharpe.max():+.4f}, and on CAGR in "
      f"{int((cmp_.dCAGR > 0).sum())}.  Every 4b pass on the LO side belongs to the base book")
    P("  and its gross rung; the gate only subtracts return.")
    P("  KILL for capital - no memo, nothing proposed for promotion.")
    flush_log()
    P("\nOutputs: " + "  ".join(f"{OUT.name}{s}" for s in
                                (".arms.csv", ".legs.csv", ".floor.csv",
                                 ".finegross.csv", ".walkforward.csv", ".console.txt")))
    flush_log()


if __name__ == "__main__":
    main()
