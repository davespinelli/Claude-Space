#!/usr/bin/env python3
"""Idea 665 -- is the STALENESS TAX a DRAWDOWN tax on every gate family?   (lane C, 2026-09-10)

QUEUE 665: idea 661 priced an L-day-stale band read at -0.218 (U56) and -0.128 (B136) Sharpe and
-9.06 / -11.00 pp MaxDD at L=42, against a band-TRANSFORM failure costing -0.088 / -0.068 Sharpe
and -0.02 / -3.63 pp.  Sweep the same lag ladder across the record's committed gate families
(breadth, vol, trend, momentum) and test whether staleness is always paid in DRAWDOWN rather than
in RETURN.

TWO TUNED PARAMETERS (PROTOCOL 4): gate family x lag.  Gross is reported as a matched-exposure
ladder, never chosen; every grid point is printed.

WHAT IS ACTUALLY TESTED
  Four gate families, each written as the SAME book shape as RULES v2 -- equal weight gross/N over
  the names its gate calls IN, gated-out weight to CASH (de-gross, never re-spread), weekly:
      TREND    per-name 200d MA +/-3% band with hysteresis   (= RULES v2 clause 2; G1 pins this)
      MOM      per-name 12-1 momentum > 0
      VOL      per-name 20d realised vol < 0.60 annualised   (RULES v1's max_vol)
      BREADTH  panel aggregate: share of names above their own 200d MA >= 0.50, broadcast to all
  STALENESS: the gate STATE is read L trading days late (state.shift(L)); the tradable set is
  current (you always know what is priced today).  Only the SIGNAL is stale.  L=0 is each family's
  own control -- the tax is measured WITHIN family, never across.

THE CURRENCY QUESTION, pre-registered before any number is read
  r_CAGR(L) = -(CAGR(L) - CAGR(0)) / CAGR(0)          fractional loss of return
  r_DD(L)   = -(MaxDD(L) - MaxDD(0)) / |MaxDD(0)|     fractional deepening of drawdown
  verdict at a rung: DD_TAX if r_DD > 2*r_CAGR, RETURN_TAX if r_CAGR > 2*r_DD, else MIXED.
  The 2x bar is a REPORTED CONSTANT fixed here, not tuned; both rungs L=42 (661's quoted rung)
  and L=63 (the ladder's end) are reported, and so is the whole ladder.
  SCRAMBLE placebo gives the SATURATED scale of each currency: the same gate read at a large
  random PAST offset (252..1008 days, 12 fixed-seed draws), i.e. a fully de-aligned read.  A tax
  is only interesting relative to what total de-alignment costs.
  Gate WORK is reported beside every tax (off_share = mean share of names gated out, flip = mean
  daily share of names whose state changes) because a gate that never fires cannot go stale.

PROTOCOL: 10 bps (rungs 0/10/25 reported on the rule-8 picks), next-day execution (engine),
freq W, no shorting, no leverage.  Rule 8: (lag, gross) fitted on 2009-2016 IS Sharpe ONLY,
scored on 2017-2026 untouched.  Both KEEP paths evaluated at every grid point.
Panels: U56 (research/universe.json), B136 (universe_broad.json), SMALL484 (data/prices_small).
SURVIVORSHIP: B136 and SMALL484 are CURRENT constituents of their screens -- see
data/SMALL_PANEL_README.md.  No network; committed caches only.

Deterministic, standalone.  Writes .console.txt .grid.csv .tax.csv .placebo.csv .walkforward.csv
.keeppaths.csv .  Modifies nothing (RULES.md, scan.py, bot.py, baseline.py, PROTOCOL.md untouched).
"""
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0
FREQ = "W"
BAND = 0.03                                   # RULES v2 clause 2
MAXVOL = 0.60                                 # RULES v1 max_vol
BREADTH_BAR = 0.50                            # majority of the panel above its own 200d MA
LAGS = [0, 1, 2, 5, 10, 21, 42, 63]           # idea 661's ladder, reproduced exactly
GROSSES = [0.50, 0.75, 1.00]
COSTRUNGS = [0.0, 10.0, 25.0]
FAMILIES = ["TREND", "MOM", "VOL", "BREADTH"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CURRENCY_BAR = 2.0                            # the pre-registered 2x bar
PLACEBO_DRAWS = 12
PLACEBO_LO, PLACEBO_HI = 252, 1008
SEED = 665
RUNGS_REPORTED = [42, 63]

LINES = []


def P(s=""):
    print(s)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# 1.  THE FOUR GATE FAMILIES  (state first, book second)
# ================================================================================================
def gate_state(px, fam):
    """Per-name boolean IN state, decided at close t from data available at close t."""
    if fam == "TREND":
        return band_state(px, BAND)
    if fam == "MOM":
        m = px.shift(21) / px.shift(252) - 1
        return (m > 0).fillna(False)
    if fam == "VOL":
        v = px.pct_change().rolling(20).std() * np.sqrt(252)
        return (v < MAXVOL).fillna(False)
    if fam == "BREADTH":
        above = px > px.rolling(200).mean()
        priced = px.notna()
        share = above.where(priced).sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)
        on = (share >= BREADTH_BAR).fillna(False)
        return pd.DataFrame(np.tile(on.values[:, None], (1, px.shape[1])),
                            index=px.index, columns=px.columns)
    raise ValueError(fam)


def ew_gross(px, gross):
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    return gross * priced.astype(float).div(n, axis=0).fillna(0.0)


def book(px, fam, lag, gross, state_cache=None, offset=None):
    """The family's book with its gate read `lag` (or `offset`) trading days STALE."""
    st = gate_state(px, fam) if state_cache is None else state_cache
    k = int(offset if offset is not None else lag)
    if k:
        st = st.shift(k).fillna(False).astype(bool)
    return ew_gross(px, gross).where(st & px.notna(), 0.0)


def gate_work(px, st):
    """How hard the gate actually works: mean share of priced names OUT, and mean daily flip rate."""
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    off = 1.0 - (st & priced).sum(axis=1) / n
    flip = (st.astype(int).diff().abs() * priced).sum(axis=1) / n
    return float(off.mean(skipna=True)), float(flip.mean(skipna=True))


# ================================================================================================
# 2.  GATES (pre-registered; nothing is read if these fail)
# ================================================================================================
def gates(panels):
    P()
    P("=" * 100)
    P("(G) GATES")
    P("=" * 100)
    ok = True
    px = panels["U56"]

    w = book(px, "TREND", 0, 0.75)
    w2 = rules_v2_weights(px, band=BAND, gross=0.75)
    dw = float(np.nanmax(np.abs(w.values - w2.values)))
    r1 = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"]
    r2 = backtest(px, w2, cost_bps=COST, freq=FREQ)["returns"]
    dr = float(np.abs(r1 - r2).max())
    g1 = dw < 1e-12 and dr < 1e-12
    P(f"  G1 TREND @ L=0, g=0.75 IS the live book (rules_v2_weights) : max|dW| {dw:.3e}  "
      f"max|dR| {dr:.3e}   {'PASS' if g1 else 'FAIL'}")
    ok &= g1

    b0 = backtest(px, w, cost_bps=0.0, freq=FREQ)
    b25 = backtest(px, w, cost_bps=25.0, freq=FREQ)
    d2 = float(np.abs((b0["returns"] - b0["turnover"] * 25.0 / 1e4) - b25["returns"]).max())
    P(f"  G2 cost-rung identity r(25) = r(0) - turn*25/1e4 : max|d| {d2:.3e}   "
      f"{'PASS' if d2 < 1e-12 else 'FAIL'}")
    ok &= d2 < 1e-12

    # G3 -- the lag channel is a pure shift of the SIGNAL: state(L) equals state(0) shifted, and
    # the book never holds a name that is not priced today.
    g3 = True
    for fam in FAMILIES:
        st = gate_state(px, fam)
        for L in (5, 42):
            lhs = book(px, fam, L, 0.75)
            man = ew_gross(px, 0.75).where(st.shift(L).fillna(False).astype(bool) & px.notna(), 0.0)
            g3 &= float(np.nanmax(np.abs(lhs.values - man.values))) < 1e-15
        w_any = book(px, fam, 63, 0.75)
        g3 &= bool((w_any.values[~px.notna().values] == 0).all())
    P(f"  G3 lag is a pure shift of the gate state, and no unpriced name is ever held : "
      f"{'PASS' if g3 else 'FAIL'}")
    ok &= g3

    # G4 -- every family's gate is non-degenerate on every panel (it fires, and it flips).
    P("  G4 gate WORK at L=0 (a gate that never fires cannot go stale):")
    g4 = True
    for pname, p in panels.items():
        for fam in FAMILIES:
            off, flip = gate_work(p, gate_state(p, fam))
            good = 0.005 < off < 0.995 and flip > 1e-5
            g4 &= good
            P(f"     {pname:8s} {fam:8s} off_share {off:6.3f}  flip/day {flip:8.5f}   "
              f"{'ok' if good else 'DEGENERATE'}")
    P(f"     {'PASS' if g4 else 'FAIL'}")
    ok &= g4

    # G5 -- gross is a pure scaler of the held book (so a gross ladder is an exposure ladder).
    a = book(px, "MOM", 10, 0.50)
    b = book(px, "MOM", 10, 1.00)
    g5 = float(np.nanmax(np.abs(a.values * 2.0 - b.values))) < 1e-15
    P(f"  G5 gross scales the book exactly (0.50*2 == 1.00) : {'PASS' if g5 else 'FAIL'}")
    ok &= g5
    return ok


# ================================================================================================
# 3.  METRIC HELPERS  +  PROTOCOL 4
# ================================================================================================
def slice_metrics(r):
    m = metrics(r)
    h = len(r) // 2
    return m["CAGR"], m["Sharpe"], m["MaxDD"], metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pass4b(cagr, dd, h1, h2, oos_sh, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
    return bool(h1 > spy["H1"] and h2 > spy["H2"] and oos_sh > spy["OOS_Sharpe"]
                and dd >= 0.60 * spy["MaxDD"] and cagr >= 0.70 * spy["CAGR"])


def pass4a(dd, h1, h2, base):
    """PROTOCOL 4a: Sharpe > the live rules in BOTH halves, MaxDD no worse."""
    return bool(h1 > base["H1"] and h2 > base["H2"] and dd >= base["MaxDD"])


def refs(px, start):
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    base_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    out = {}
    for nm, r in (("SPY", spy_r), ("V2", base_r)):
        c, s, d, h1, h2 = slice_metrics(r)
        o = metrics(r.loc[OOS_START:])
        out[nm] = dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2, OOS_Sharpe=o["Sharpe"],
                       OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"])
    return out


def run(px, start, w, ref, cost=COST):
    b = backtest(px, w, cost_bps=cost, freq=FREQ)
    r = b["returns"].loc[start:]
    c, s, d, h1, h2 = slice_metrics(r)
    o, im = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    m = metrics(r)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2, Vol=m["Vol"], Calmar=m["Calmar"],
                IS_Sharpe=im["Sharpe"], IS_CAGR=im["CAGR"], IS_MaxDD=im["MaxDD"],
                OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"],
                turn_x_yr=b["turnover"].loc[start:].sum() / (len(r) / 252),
                pass4a=pass4a(d, h1, h2, ref["V2"]),
                pass4b=pass4b(c, d, h1, h2, o["Sharpe"], ref["SPY"]))


# ================================================================================================
# 4.  THE GRID  (family x lag x gross x panel) -- every point reported
# ================================================================================================
def grid_all(panels):
    P()
    P("=" * 100)
    P("(A) THE GRID -- four gate families x eight lags x three grosses, all printed")
    P("=" * 100)
    rows, R = [], {}
    for pname, px in panels.items():
        start = px.index[260]
        ref = refs(px, start)
        R[pname] = ref
        P(f"  --- {pname} ({px.shape[1]} cols, {start.date()} -> {px.index[-1].date()}) ---")
        for nm in ("SPY", "V2"):
            P(f"      {nm:5s} CAGR {ref[nm]['CAGR']:7.2%}  Sharpe {ref[nm]['Sharpe']:.3f}  "
              f"MaxDD {ref[nm]['MaxDD']:7.2%}  H1/H2 {ref[nm]['H1']:.3f}/{ref[nm]['H2']:.3f}  "
              f"OOS Sh {ref[nm]['OOS_Sharpe']:.3f} CAGR {ref[nm]['OOS_CAGR']:7.2%} "
              f"DD {ref[nm]['OOS_MaxDD']:7.2%}")
        for fam in FAMILIES:
            st = gate_state(px, fam)
            off, flip = gate_work(px, st)
            P(f"      {fam} (off_share {off:.3f}, flip/day {flip:.5f}) at g=0.75:")
            for g in GROSSES:
                for L in LAGS:
                    d = run(px, start, book(px, fam, L, g, state_cache=st), R[pname])
                    d.update(panel=pname, family=fam, lag=L, gross=g, cost=COST,
                             off_share=off, flip=flip)
                    rows.append(d)
                    if g == 0.75:
                        P(f"        L={L:>3d}  CAGR {d['CAGR']:7.2%}  Sharpe {d['Sharpe']:.3f}  "
                          f"Vol {d['Vol']:6.2%}  MaxDD {d['MaxDD']:7.2%}  OOS Sh "
                          f"{d['OOS_Sharpe']:.3f}  turn {d['turn_x_yr']:.2f}x/yr  "
                          f"4a {'Y' if d['pass4a'] else 'n'} 4b {'Y' if d['pass4b'] else 'n'}")
        P()
    return pd.DataFrame(rows), R


# ================================================================================================
# 5.  THE PLACEBO -- what a FULLY de-aligned read of the same gate costs (the saturated scale)
# ================================================================================================
def placebo(panels):
    P()
    P("=" * 100)
    P("(B) SCRAMBLE PLACEBO -- the same gate read at a large random PAST offset (252..1008 d)")
    P("=" * 100)
    P(f"  {PLACEBO_DRAWS} fixed-seed draws per (panel, family) at g=0.75.  Past offsets only: no")
    P("  future information is ever used.  This is the SATURATED value of each currency.")
    rng = np.random.default_rng(SEED)
    offs = {f: rng.integers(PLACEBO_LO, PLACEBO_HI + 1, PLACEBO_DRAWS) for f in FAMILIES}
    rows = []
    for pname, px in panels.items():
        start = px.index[260]
        ref = refs(px, start)
        for fam in FAMILIES:
            st = gate_state(px, fam)
            base = run(px, start, book(px, fam, 0, 0.75, state_cache=st), ref)
            for o in offs[fam]:
                d = run(px, start, book(px, fam, 0, 0.75, state_cache=st, offset=int(o)), ref)
                rows.append(dict(panel=pname, family=fam, offset=int(o),
                                 dCAGR=d["CAGR"] - base["CAGR"], dSharpe=d["Sharpe"] - base["Sharpe"],
                                 dMaxDD=d["MaxDD"] - base["MaxDD"],
                                 r_CAGR=-(d["CAGR"] - base["CAGR"]) / abs(base["CAGR"]),
                                 r_DD=-(d["MaxDD"] - base["MaxDD"]) / abs(base["MaxDD"])))
    PL = pd.DataFrame(rows)
    agg = PL.groupby(["panel", "family"]).agg(
        n=("offset", "size"), dCAGR=("dCAGR", "mean"), dSharpe=("dSharpe", "mean"),
        dMaxDD=("dMaxDD", "mean"), sd_dCAGR=("dCAGR", "std"), sd_dMaxDD=("dMaxDD", "std"),
        r_CAGR=("r_CAGR", "mean"), r_DD=("r_DD", "mean")).reset_index()
    P()
    for _, r in agg.iterrows():
        cur = ("DD_TAX" if r.r_DD > CURRENCY_BAR * r.r_CAGR else
               "RETURN_TAX" if r.r_CAGR > CURRENCY_BAR * r.r_DD else "MIXED")
        P(f"  {r.panel:8s} {r.family:8s} saturated  dCAGR {r.dCAGR:+7.2%} (sd {r.sd_dCAGR:.2%})  "
          f"dSharpe {r.dSharpe:+.3f}  dMaxDD {r.dMaxDD:+7.2f} pp (sd {r.sd_dMaxDD * 100:.2f})  "
          f"r_CAGR {r.r_CAGR:+.3f} r_DD {r.r_DD:+.3f}  -> {cur}")
    return PL, agg


# ================================================================================================
# 6.  THE CURRENCY OF THE TAX
# ================================================================================================
def tax(G, agg):
    P()
    P("=" * 100)
    P("(C) THE STALENESS TAX AND ITS CURRENCY -- matched gross 0.75, within family")
    P("=" * 100)
    P("  r_CAGR = -dCAGR/|CAGR(0)|   r_DD = -dMaxDD/|MaxDD(0)|   (both: positive = worse)")
    P(f"  verdict at a rung: DD_TAX if r_DD > {CURRENCY_BAR:.0f}x r_CAGR, RETURN_TAX if the "
      f"converse, else MIXED.")
    P()
    rows = []
    S = G[G.gross == 0.75]
    for (pname, fam), s in S.groupby(["panel", "family"]):
        s = s.sort_values("lag")
        b = s[s.lag == 0].iloc[0]
        sat = agg[(agg.panel == pname) & (agg.family == fam)].iloc[0]
        x = s.lag.values / 21.0
        sl_c = float(np.polyfit(x, s.CAGR.values, 1)[0]) if len(s) > 1 else np.nan
        sl_d = float(np.polyfit(x, s.MaxDD.values, 1)[0]) if len(s) > 1 else np.nan
        sl_s = float(np.polyfit(x, s.Sharpe.values, 1)[0]) if len(s) > 1 else np.nan
        for _, r in s.iterrows():
            rc = -(r.CAGR - b.CAGR) / abs(b.CAGR)
            rd = -(r.MaxDD - b.MaxDD) / abs(b.MaxDD)
            cur = ("NONE" if r.lag == 0 else
                   "DD_TAX" if rd > CURRENCY_BAR * rc else
                   "RETURN_TAX" if rc > CURRENCY_BAR * rd else "MIXED")
            rows.append(dict(panel=pname, family=fam, lag=int(r.lag), off_share=r.off_share,
                             flip=r.flip, CAGR=r.CAGR, Sharpe=r.Sharpe, Vol=r.Vol, MaxDD=r.MaxDD,
                             dCAGR=r.CAGR - b.CAGR, dSharpe=r.Sharpe - b.Sharpe,
                             dVol=r.Vol - b.Vol, dMaxDD_pp=(r.MaxDD - b.MaxDD) * 100,
                             r_CAGR=rc, r_DD=rd, currency=cur,
                             frac_sat_CAGR=(r.CAGR - b.CAGR) / sat.dCAGR if sat.dCAGR else np.nan,
                             frac_sat_DD=(r.MaxDD - b.MaxDD) / sat.dMaxDD if sat.dMaxDD else np.nan,
                             slope_CAGR_per21=sl_c, slope_MaxDD_per21=sl_d,
                             slope_Sharpe_per21=sl_s))
    T = pd.DataFrame(rows)
    for pname in T.panel.unique():
        P(f"  --- {pname} ---")
        for fam in FAMILIES:
            s = T[(T.panel == pname) & (T.family == fam)].sort_values("lag")
            b = s.iloc[0]
            P(f"    {fam:8s} L=0: CAGR {b.CAGR:7.2%} Sharpe {b.Sharpe:.3f} MaxDD {b.MaxDD:7.2%}   "
              f"slopes/21d: CAGR {s.iloc[0].slope_CAGR_per21 * 100:+6.3f} pp  "
              f"MaxDD {s.iloc[0].slope_MaxDD_per21 * 100:+6.3f} pp  "
              f"Sharpe {s.iloc[0].slope_Sharpe_per21:+.4f}")
            for _, r in s[s.lag > 0].iterrows():
                P(f"       L={r.lag:>3d}  dCAGR {r.dCAGR * 100:+6.2f} pp  dSharpe {r.dSharpe:+.3f}  "
                  f"dVol {r.dVol * 100:+5.2f} pp  dMaxDD {r.dMaxDD_pp:+6.2f} pp   "
                  f"r_CAGR {r.r_CAGR:+.3f}  r_DD {r.r_DD:+.3f}  {r.currency:10s}  "
                  f"frac of saturated: CAGR {r.frac_sat_CAGR:+.2f} DD {r.frac_sat_DD:+.2f}")
        P()
    P("  CURRENCY TALLY over the 8 lags x 4 families x 3 panels (L>0 only):")
    tal = T[T.lag > 0].groupby("currency").size().sort_values(ascending=False)
    for k, v in tal.items():
        P(f"     {k:10s} {v:3d} / {int(T[T.lag > 0].shape[0])}  ({v / T[T.lag > 0].shape[0]:.1%})")
    P()
    P(f"  AT THE REPORTED RUNGS {RUNGS_REPORTED} (one line per panel x family x rung):")
    hit = T[T.lag.isin(RUNGS_REPORTED)]
    for _, r in hit.sort_values(["lag", "panel", "family"]).iterrows():
        P(f"     L={r.lag:>3d} {r.panel:8s} {r.family:8s} r_CAGR {r.r_CAGR:+.3f}  r_DD {r.r_DD:+.3f}"
          f"  ratio {r.r_DD / r.r_CAGR if r.r_CAGR else np.nan:+8.2f}  {r.currency}")
    n_dd = int((hit.currency == "DD_TAX").sum())
    P(f"\n  DD_TAX at the reported rungs: {n_dd} / {len(hit)}  "
      f"({n_dd / len(hit):.1%})   <-- the queue's claim, priced")
    P("  (a NEGATIVE r means staleness HELPED that currency on that panel/family)")
    return T


# ================================================================================================
# 7.  PROTOCOL RULE 8  -- (lag, gross) fitted on 2009-2016 only
# ================================================================================================
def walkforward(panels, G, R):
    P()
    P("=" * 100)
    P("(D) PROTOCOL RULE 8 -- fit (lag, gross) on 2009-2016 by IS Sharpe, score 2017-2026 untouched")
    P("=" * 100)
    rows = []
    for pname, px in panels.items():
        start = px.index[260]
        ref = R[pname]
        P(f"  --- {pname} ---   SPY OOS Sh {ref['SPY']['OOS_Sharpe']:.3f} CAGR "
          f"{ref['SPY']['OOS_CAGR']:7.2%} DD {ref['SPY']['OOS_MaxDD']:7.2%} | "
          f"V2 OOS Sh {ref['V2']['OOS_Sharpe']:.3f} CAGR {ref['V2']['OOS_CAGR']:7.2%} DD "
          f"{ref['V2']['OOS_MaxDD']:7.2%}")
        for fam in FAMILIES:
            s = G[(G.panel == pname) & (G.family == fam)]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            st = gate_state(px, fam)
            rung = {}
            for c in COSTRUNGS:
                d = run(px, start, book(px, fam, int(pick.lag), pick.gross, state_cache=st), ref, cost=c)
                rung[c] = d
            rows.append(dict(panel=pname, family=fam, pick_lag=int(pick.lag), pick_gross=pick.gross,
                             IS_Sharpe=pick.IS_Sharpe,
                             OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                             OOS_MaxDD=pick.OOS_MaxDD,
                             fresh_OOS_Sharpe=float(s[(s.lag == 0) & (s.gross == pick.gross)].OOS_Sharpe.iloc[0]),
                             fresh_OOS_CAGR=float(s[(s.lag == 0) & (s.gross == pick.gross)].OOS_CAGR.iloc[0]),
                             fresh_OOS_MaxDD=float(s[(s.lag == 0) & (s.gross == pick.gross)].OOS_MaxDD.iloc[0]),
                             SPY_OOS_Sharpe=ref["SPY"]["OOS_Sharpe"], SPY_OOS_CAGR=ref["SPY"]["OOS_CAGR"],
                             SPY_OOS_MaxDD=ref["SPY"]["OOS_MaxDD"],
                             V2_OOS_Sharpe=ref["V2"]["OOS_Sharpe"], V2_OOS_CAGR=ref["V2"]["OOS_CAGR"],
                             V2_OOS_MaxDD=ref["V2"]["OOS_MaxDD"], V2_MaxDD=ref["V2"]["MaxDD"],
                             beats_SPY=bool(pick.OOS_Sharpe > ref["SPY"]["OOS_Sharpe"]),
                             beats_V2=bool(pick.OOS_Sharpe > ref["V2"]["OOS_Sharpe"]),
                             full_4a=bool(pick.pass4a), full_4b=bool(pick.pass4b),
                             p4a_0=rung[0.0]["pass4a"], p4a_10=rung[10.0]["pass4a"],
                             p4a_25=rung[25.0]["pass4a"],
                             p4b_0=rung[0.0]["pass4b"], p4b_10=rung[10.0]["pass4b"],
                             p4b_25=rung[25.0]["pass4b"],
                             OOS_Sharpe_0=rung[0.0]["OOS_Sharpe"], OOS_Sharpe_25=rung[25.0]["OOS_Sharpe"]))
            r = rows[-1]
            P(f"    {fam:8s} pick L={r['pick_lag']:>3d} g={r['pick_gross']:.2f} (IS Sh "
              f"{r['IS_Sharpe']:.3f}) -> OOS CAGR {r['OOS_CAGR']:7.2%} Sharpe {r['OOS_Sharpe']:.3f} "
              f"MaxDD {r['OOS_MaxDD']:7.2%} | FRESH same g: CAGR {r['fresh_OOS_CAGR']:7.2%} Sh "
              f"{r['fresh_OOS_Sharpe']:.3f} DD {r['fresh_OOS_MaxDD']:7.2%} | "
              f"4a {'Y' if r['full_4a'] else 'n'} 4b {'Y' if r['full_4b'] else 'n'}  "
              f"4b@0/10/25 {int(r['p4b_0'])}/{int(r['p4b_10'])}/{int(r['p4b_25'])}")
        P()
    return pd.DataFrame(rows)


# ================================================================================================
def main():
    t0 = time.time()
    P(f"Idea 665 -- is the STALENESS TAX a DRAWDOWN tax on every gate family?  (lane C, "
      f"{pd.Timestamp.today().date()})")
    P(f"PROTOCOL: {COST:.0f} bps, next-day execution, freq {FREQ}, rule 8 IS <= {IS_END} / "
      f"OOS >= {OOS_START}.  2 params: gate family x lag.")
    P(f"Families {FAMILIES}   lags {LAGS}   gross ladder {GROSSES}   cost rungs {COSTRUNGS}")

    panels = {"U56": load_universe(),
              "B136": load_universe(broad=True),
              "SMALL484": load_universe(small=True)}
    for k, v in panels.items():
        P(f"  panel {k:9s} {v.shape[0]} days x {v.shape[1]} cols  "
          f"{v.index[0].date()} -> {v.index[-1].date()}")
    P("  SURVIVORSHIP: B136 and SMALL484 are CURRENT constituents of their screens.")

    if not gates(panels):
        P("\nGATES FAILED -- stopping before any new number is read.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return

    G, R = grid_all(panels)
    PL, agg = placebo(panels)
    T = tax(G, agg)
    W = walkforward(panels, G, R)

    P()
    P("=" * 100)
    P("(E) KEEP PATHS -- PROTOCOL 4a and 4b at every grid point")
    P("=" * 100)
    kp = G.groupby(["panel", "family"]).agg(points=("pass4a", "size"), p4a=("pass4a", "sum"),
                                            p4b=("pass4b", "sum")).reset_index()
    kp["both"] = [int(((G.panel == r.panel) & (G.family == r.family) & G.pass4a & G.pass4b).sum())
                  for _, r in kp.iterrows()]
    P(kp.to_string(index=False))
    P(f"\n  TOTAL: 4a {int(G.pass4a.sum())}/{len(G)}   4b {int(G.pass4b.sum())}/{len(G)}   "
      f"BOTH {int((G.pass4a & G.pass4b).sum())}/{len(G)}")
    if int(G.pass4b.sum()):
        P("  4b passers by gross: " + ", ".join(
            f"g={g:.2f}: {int(G[(G.gross == g) & G.pass4b].shape[0])}" for g in GROSSES))
        P("  4b passers by lag:   " + ", ".join(
            f"L={L}: {int(G[(G.lag == L) & G.pass4b].shape[0])}" for L in LAGS))
    P(f"  rule-8 picks clearing 4b at 0/10/25 bps: {int(W.p4b_0.sum())}/{int(W.p4b_10.sum())}/"
      f"{int(W.p4b_25.sum())} of {len(W)};  4a at 10 bps: {int(W.p4a_10.sum())}/{len(W)}")
    P(f"  rule-8 picks beating SPY OOS Sharpe: {int(W.beats_SPY.sum())}/{len(W)};  "
      f"beating the live book: {int(W.beats_V2.sum())}/{len(W)}")
    P(f"  rule-8 picks whose IS-chosen lag is NOT 0 (staleness chosen by the fitter): "
      f"{int((W.pick_lag != 0).sum())}/{len(W)}")

    P()
    P("=" * 100)
    P("OUTPUTS")
    P("=" * 100)
    dump(G, "grid")
    dump(T, "tax")
    dump(PL, "placebo")
    dump(agg, "placebo_agg")
    dump(W, "walkforward")
    dump(kp, "keeppaths")
    P(f"\ntotal {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
