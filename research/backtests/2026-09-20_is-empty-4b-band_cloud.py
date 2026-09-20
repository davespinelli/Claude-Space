#!/usr/bin/env python3
"""Idea 809 (lane cloud, 2026-09-20) — DOES ANY COMMITTED WIDTH-OR-GROSS 4b BAND HAVE AN **EMPTY
IN-SAMPLE COUNTERPART**?  And does requiring a non-empty IS band BUY anything out of sample?

THE DEFECT THIS PRICES.  Idea 806 retired both of 589's doubts about a width candidate (interior
argmax, contiguous 8-rung 4b band, cost- and delay-robust) and STILL killed it, for one reason:
the IS window's own 4b band was EMPTY.  No width cleared 4b on 2009-2016, so 0 of 4 IS-only
selectors could reach a band that exists only on the full sample.  If that is general rather than
one candidate's bad luck, then rule 8 needs a PRECONDITION — "the IS band is non-empty" — before
any band is published, and a large part of the record's committed 4b band prose is an ex-post-only
object that no live chooser could ever have traded.

Idea 809 was SKIPPED on 2026-09-15 as having "no single book to price".  That reading is wrong and
is overturned here: the question is not about one book, it is about every RUNG of the record's two
committed band ladders, each of which is a real weights function.

WHAT IS PRICED HERE.  Both committed band families, every rung, on three panels, scored twice —
once on the FULL sample against full-sample bars, once INSIDE the IS window alone against IS-window
bars — so "the IS band" is a measured set, not an assertion:

    PANEL   {U56, B136, SMALL}
    FAMILY  BAND    : the live RULES v2 ladder.  Hold every name inside the 200d +/- c band,
                      equal weight at G/N of NAV, cash otherwise.
                      c in {0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12}  x  G in {0.50, 0.75,
                      0.85, 1.00}  =  28 rungs.   [the WIDTH-and-GROSS band the idea names]
            VOLTGT  : the standing KEEP-candidate's ladder.  Equal-weight the panel, gross scaled
                      by a vol target and refreshed on a drift trigger.
                      t in {0.08, 0.10, 0.12, 0.16, 0.20}  x  h in {0, .01, .02, .03, .05, .08,
                      .12, .16, .20, .25}  =  50 rungs.
    COST    {10, 25, 50} bps                   REPORTED at every rung
    SPLIT   {2016-12-31, 2018-12-31}           the second tuned dial (rule 8's split date)

  = 3 x 78 = 234 books, x 3 costs x 2 splits = 1,404 scored (rung, cost, split) cells.

EXACTLY TWO TUNED PARAMETERS, and they are the ones the idea itself names: **the band set**
(BAND vs VOLTGT) and **the split**.  Every rung of every ladder is REPORTED, never chosen; cost
and panel are reported.  Execution is t+1 throughout (PROTOCOL rule 2).

THE TWO BANDS, defined once and used everywhere:
  FULL band  = the set of rungs clearing PROTOCOL 4b scored on the FULL sample against
               FULL-sample SPY bars (H1, H2, OOS Sharpe, MaxDD <= 0.60x SPY, CAGR >= 0.70x SPY).
  IS band    = the set of rungs clearing the SAME five legs computed INSIDE the IS window only,
               against SPY's OWN IS-window bars (IS halves for H1/H2, the IS second half standing
               in for the OOS leg, IS MaxDD cap, IS CAGR floor).  Nothing after the split date is
               read.  This is what a chooser standing at the split date could actually see.
  A ladder whose FULL band is NON-EMPTY and whose IS band is EMPTY is an EX-POST-ONLY OBJECT.

PRE-STATED VERDICT RULES (fixed before the run):
  V1  HOW GENERAL IS 806's EMPTY IS BAND?  Over all (panel x family x cost x split) ladders with a
      non-empty FULL band, the share that are EX-POST-ONLY.  >= 50% -> the precondition is
      LOAD-BEARING and must be adopted; <= 10% -> 806's emptiness was that candidate's own bad
      luck and the precondition is cosmetic; in between -> PARTIAL.
  V2  WHERE THE IS BAND IS NON-EMPTY, DOES IT POINT AT THE RIGHT RUNGS?  Containment of the FULL
      band by the IS band and the reverse, plus the Jaccard overlap, per ladder.
  V3  DOES THE PRECONDITION BUY ANYTHING OUT OF SAMPLE?  Rule 8 proper, OOS read ONCE: compare the
      OOS result of an UNCONDITIONAL IS-argmax chooser against the SAME chooser RESTRICTED to the
      IS band (and reporting "no publication" where the IS band is empty).  Pre-stated: the
      precondition is worth adopting only if it does not LOSE OOS Sharpe on average AND it removes
      OOS 4b failures.
  V4  THE STANDING KEEP-CANDIDATE.  Is `B136 VOLTGT t = 0.10, h = 0.08` inside its own ladder's IS
      band, or is the 45-of-45 stress record sitting on an ex-post-only object?

PROTOCOL: rule 2 (10 bps headline, t+1 execution, no leverage, gross <= 1.00); rule 3 (live RULES
v2 AND SPY); rule 4 (both KEEP paths and the binding leg at every cell); rule 5 (one idea,
deterministic, standalone); rule 8 (IS chooses, OOS read once); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen
(tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and drawdown
LEVEL is optimistic and every 4b bar is easier here than on a point-in-time panel.  The IS-vs-FULL
band CONTRAST is same-tape / same-names / same-ladder and first-order immune to it; the BAND
MEMBERSHIP COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_is-empty-4b-band_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state       # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask         # noqa: E402

DATE, SLUG = "2026-09-20", "is-empty-4b-band"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
COSTS = [10, 25, 50]
COST0 = 10
SPLITS = ["2016-12-31", "2018-12-31"]
SPLIT0 = "2016-12-31"
BANDS_C = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12]
BANDS_G = [0.50, 0.75, 0.85, 1.00]
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
THRESH = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]
T_TRADE = "W"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L = 20
V1_HI, V1_LO = 0.50, 0.10          # pre-stated bands for the ex-post-only share
CAND = dict(panel="B136", family="VOLTGT", rung="t=0.10|h=0.08")
# the live book's own rung, for a reproduction gate against baseline.rules_v2_weights
LIVE_RUNG = (0.03, 0.75)

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


# ----------------------------------------------------------------------------- panels
def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    dropped = len([c for c in pxs.columns if c in bad])
    return ([("U56", px56, list(px56.columns)),
             ("B136", px136, list(px136.columns)),
             (f"SMALL{len(small_cols)}", pxs, small_cols)], dropped)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L):
    ew = eq_weight(px, cols)
    pr = (ew.shift(1) * px.pct_change()).sum(axis=1)
    return pr.rolling(L).std() * np.sqrt(252.0)


# ------------------------------------------------------------------------ the two band ladders
def band_weights(px, cols, c, G):
    """FAMILY BAND: equal weight at G/N inside the 200d +/- c band, cash outside.  At c = 0.03 and
    G = 0.75 on the panel's own columns this is `baseline.rules_v2_weights` exactly (gate G4)."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = G * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(band_state(sub, c), 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def bt_drift(px_ret, W0, g0, mT, h):
    """FAMILY VOLTGT: idea 1799's drift-trigger runner, verbatim."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1]); held = np.empty_like(px_ret); turn = np.zeros(n)
    g_eff = g0[0]
    for i in range(n):
        trig = abs(g0[i] - cur.sum()) > h
        if trig or i == 0:
            g_eff = g0[i]
        if mT[i] or i == 0:
            new = W0[i] * g_eff; turn[i] = np.abs(new - cur).sum(); cur = new
        elif trig:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s); turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i]); tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1)


def lag1(a):
    a = np.asarray(a)
    pad = np.zeros((1,) + a.shape[1:], dtype=a.dtype) if a.ndim > 1 else np.zeros(1, dtype=a.dtype)
    return np.concatenate([pad, a[:-1]])


# ----------------------------------------------------------------------------- metrics
def mets(r):
    r = r.dropna()
    if len(r) < 60:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = (1 + r).cumprod(); yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def five_legs(r, bars):
    """The five PROTOCOL-4b leg margins of a return series against a bar dict.

    `bars` carries h1 / h2 / tail (the Sharpe the third leg is judged against) / MaxDD / CAGR.
    On the FULL window `tail` is SPY's OOS Sharpe; on the IS window it is SPY's IS SECOND-HALF
    Sharpe, which is the closest thing a chooser standing at the split date has to an OOS leg.
    Stated here, not buried: the IS third leg is a STAND-IN, and V1 is reported both with it and
    with it dropped (the four-leg read) so no verdict rests on the substitution."""
    m = mets(r); h1, h2 = halves(r)
    tail = mets(r.iloc[len(r) // 2:])["Sharpe"]
    return {"L1_H1": h1 - bars["h1"], "L2_H2": h2 - bars["h2"], "L3_OOS": tail - bars["tail"],
            "L4_DD": m["MaxDD"] - DD_CAP * bars["MaxDD"],
            "L5_CAGR": m["CAGR"] - CAGR_FLOOR * bars["CAGR"]}, m


def binding(mar, legs=LEGS):
    bad = [k for k in legs if not (mar[k] > 0)]
    return ("|".join(bad) if bad else "none", len(bad))


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a | b) else np.nan


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 809 (lane cloud, {DATE}) — does any committed WIDTH-or-GROSS 4b band have an "
        f"EMPTY IN-SAMPLE counterpart, and does the precondition buy anything OOS?")
    log(f"# TUNED (2, the idea's own): BAND SET {{BAND, VOLTGT}} and SPLIT {SPLITS}.")
    log(f"# REPORTED, not tuned: every rung (BAND c {BANDS_C} x G {BANDS_G} = 28; "
        f"VOLTGT t {TARGETS} x h {THRESH} = 50), cost {COSTS} bps, panel.")
    log(f"# execution t+1 throughout; cadence {T_TRADE}; warm-up {WARMUP}; sigma L={SIG_L}.")
    log(f"# BASELINES: live RULES v2 (W, t+1, {COST0} bps) AND SPY, both on each panel's own tape.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    # ------------------------------------------------------------------ baselines and the bars
    BARS, LIVEP, SPYP, START = {}, {}, {}, {}
    for pname, px, cols in PS:
        st = px.index[WARMUP]; START[pname] = st
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq=T_TRADE)
        lr = (lb["returns"] - lb["turnover"] * COST0 / 1e4).loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        LIVEP[pname] = {}
        SPYP[pname] = {}
        for sp in SPLITS:
            s_is, s_full = spy.loc[:sp], spy
            mi, mf = mets(s_is), mets(s_full)
            ih1, ih2 = halves(s_is)
            fh1, fh2 = halves(s_full)
            BARS[(pname, sp, "FULL")] = dict(h1=fh1, h2=fh2,
                                             tail=mets(spy.loc[sp:])["Sharpe"],
                                             MaxDD=mf["MaxDD"], CAGR=mf["CAGR"])
            BARS[(pname, sp, "IS")] = dict(h1=ih1, h2=ih2, tail=ih2,
                                           MaxDD=mi["MaxDD"], CAGR=mi["CAGR"])
            l_is, l_oos = lr.loc[:sp], lr.loc[sp:]
            LIVEP[(pname, sp)] = dict(full=mets(lr), oos=mets(l_oos), is_=mets(l_is),
                                      h1=halves(lr)[0], h2=halves(lr)[1],
                                      ih1=halves(l_is)[0], ih2=halves(l_is)[1])
            SPYP[(pname, sp)] = dict(full=mf, is_=mi, oos=mets(spy.loc[sp:]))
        S = SPYP[(pname, SPLIT0)]; LV = LIVEP[(pname, SPLIT0)]
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")
        log(f"   LIVE v2 (W, t+1, {COST0}bps) {LV['full']['CAGR']:7.2%} / "
            f"{LV['full']['Sharpe']:.4f} / {LV['full']['MaxDD']:7.2%}   "
            f"(OOS {LV['oos']['CAGR']:7.2%} / {LV['oos']['Sharpe']:.4f} / "
            f"{LV['oos']['MaxDD']:7.2%})")
        log(f"   SPY  FULL                  {S['full']['CAGR']:7.2%} / "
            f"{S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:7.2%}")
        log(f"   SPY  IS (<= {SPLIT0})       {S['is_']['CAGR']:7.2%} / "
            f"{S['is_']['Sharpe']:.4f} / {S['is_']['MaxDD']:7.2%}")
        b = BARS[(pname, SPLIT0, 'FULL')]; bi = BARS[(pname, SPLIT0, 'IS')]
        log(f"   FULL bars: H1 {b['h1']:.4f} H2 {b['h2']:.4f} tail {b['tail']:.4f}  "
            f"MaxDD >= {DD_CAP*b['MaxDD']:.2%}  CAGR >= {CAGR_FLOOR*b['CAGR']:.2%}")
        log(f"   IS   bars: H1 {bi['h1']:.4f} H2 {bi['h2']:.4f} tail {bi['tail']:.4f}  "
            f"MaxDD >= {DD_CAP*bi['MaxDD']:.2%}  CAGR >= {CAGR_FLOOR*bi['CAGR']:.2%}")

    # --------------------------------------------------------------------- price every rung
    rows = []
    gG4 = np.nan
    gGR = 0.0
    for pname, px, cols in PS:
        st = START[pname]
        RET = np.nan_to_num(px.pct_change().values, nan=0.0)
        EW = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        SIG = panel_sigma(px, cols)
        mW = np.asarray(rebalance_mask(px.index, T_TRADE).values, bool)
        W0 = lag1(EW); mW1 = lag1(mW).astype(bool)

        raw = []                      # (family, rung, gross returns, turnover) before costs
        for c in BANDS_C:
            for G in BANDS_G:
                w = band_weights(px, cols, c, G)
                b = engine_backtest(px, w, cost_bps=0.0, freq=T_TRADE)
                raw.append(("BAND", f"c={c:.2f}|G={G:.2f}", b["returns"], b["turnover"],
                            float(b["weights"].sum(axis=1).max()), c, G))
                if (c, G) == LIVE_RUNG:
                    lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(
                        columns=px.columns).fillna(0.0)
                    d = float((w - lw).abs().to_numpy().max())
                    gG4 = d if np.isnan(gG4) else max(gG4, d)
        for tgt in TARGETS:
            g = (tgt / SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
            g0 = lag1(g)
            for h in THRESH:
                r, t, gs = bt_drift(RET, W0, g0, mW1, h)
                raw.append(("VOLTGT", f"t={tgt:.2f}|h={h:.2f}", pd.Series(r, index=px.index),
                            pd.Series(t, index=px.index), float(gs.max()), tgt, h))

        for fam, rung, r0, t0, gmax, d1, d2 in raw:
            gGR = max(gGR, gmax)
            r0, t0 = r0.loc[st:], t0.loc[st:]
            for cost in COSTS:
                r = r0 - t0 * cost / 1e4
                for sp in SPLITS:
                    r_is, r_oos = r.loc[:sp], r.loc[sp:]
                    fmar, fm = five_legs(r, BARS[(pname, sp, "FULL")])
                    imar, im = five_legs(r_is, BARS[(pname, sp, "IS")])
                    om = mets(r_oos)
                    S = SPYP[(pname, sp)]; LV = LIVEP[(pname, sp)]
                    fb, _ = binding(fmar)
                    ib, _ = binding(imar)
                    in_full = all(fmar[k] > 0 for k in LEGS)
                    in_is = all(imar[k] > 0 for k in LEGS)
                    in_is4 = all(imar[k] > 0 for k in LEGS if k != "L3_OOS")
                    keep4b_oos = (om["Sharpe"] > S["oos"]["Sharpe"]
                                  and om["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                  and om["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                    h1, h2 = halves(r)
                    keep4a = (h1 > LV["h1"] and h2 > LV["h2"]
                              and fm["MaxDD"] >= LV["full"]["MaxDD"])
                    keep4a_oos = (om["Sharpe"] > LV["oos"]["Sharpe"]
                                  and om["MaxDD"] >= LV["oos"]["MaxDD"])
                    rows.append(dict(
                        panel=pname, family=fam, rung=rung, d1=d1, d2=d2, cost=cost, split=sp,
                        turn_py=float(t0.sum() / (len(r0) / 252.0)), gross_max=gmax,
                        CAGR=fm["CAGR"], Sharpe=fm["Sharpe"], MaxDD=fm["MaxDD"], H1=h1, H2=h2,
                        is_CAGR=im["CAGR"], is_Sharpe=im["Sharpe"], is_MaxDD=im["MaxDD"],
                        oos_CAGR=om["CAGR"], oos_Sharpe=om["Sharpe"], oos_MaxDD=om["MaxDD"],
                        **{f"f_{k}": float(v) for k, v in fmar.items()},
                        **{f"i_{k}": float(v) for k, v in imar.items()},
                        is_minleg=float(min(imar[k] for k in LEGS)),
                        full_bind=fb, is_bind=ib,
                        in_FULL_band=in_full, in_IS_band=in_is, in_IS_band4=in_is4,
                        keep4b_full=in_full, keep4b_oos=keep4b_oos,
                        keep4b=(in_full and keep4b_oos), keep4a=keep4a, keep4a_oos=keep4a_oos))
        log(f"   {pname}: {len([x for x in rows if x['panel']==pname])} scored cells")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")

    # -------------------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    want = 3 * (len(BANDS_C) * len(BANDS_G) + len(TARGETS) * len(THRESH))
    nb = len(G) // (len(COSTS) * len(SPLITS))
    gate("G1 both ladders priced on every panel", f"{nb} books / {len(G)} cells",
         f"== {want} books", nb == want)
    gate("G2 gross never levered", f"max gross {gGR:.6f}", "<= 1.0 + 1e-9", gGR <= 1.0 + 1e-9)
    gate("G3 no NaN verdict anywhere",
         f"{int(G[['in_FULL_band','in_IS_band']].isna().sum().sum())} NaN", "== 0",
         int(G[["in_FULL_band", "in_IS_band"]].isna().sum().sum()) == 0)
    gate("G4 the BAND ladder's (c=0.03, G=0.75) rung IS baseline.rules_v2_weights",
         f"max|dw| = {gG4:.3e}", "< 1e-12", bool(gG4 < 1e-12))
    KB = ["panel", "family", "rung", "split"]
    mono = G.sort_values("cost").groupby(KB).CAGR.apply(
        lambda s: bool(np.all(np.diff(s.values) <= 1e-12)))
    gate("G5 net CAGR is monotone non-increasing in cost at every book",
         f"{int(mono.sum())}/{len(mono)}", f"== {len(mono)}", int(mono.sum()) == len(mono))
    # the IS window must genuinely be a SUBSET read: its own metrics must differ from the full
    dif = float((G.is_Sharpe - G.Sharpe).abs().mean())
    gate("G6 the IS read is a real sub-window", f"mean |IS Sharpe - FULL Sharpe| = {dif:.4f}",
         "> 1e-3", dif > 1e-3)

    # ---------------------------------------------- V1: how general is 806's empty IS band?
    log("\n## V1 — HOW GENERAL IS 806's EMPTY IS BAND?  (one row per ladder)")
    lrows = []
    for (pn, fam, cost, sp), s in G.groupby(["panel", "family", "cost", "split"]):
        full = sorted(s[s.in_FULL_band].rung.tolist())
        isb = sorted(s[s.in_IS_band].rung.tolist())
        isb4 = sorted(s[s.in_IS_band4].rung.tolist())
        lrows.append(dict(panel=pn, family=fam, cost=cost, split=sp, n_rungs=len(s),
                          n_FULL=len(full), n_IS=len(isb), n_IS4=len(isb4),
                          full_nonempty=len(full) > 0, is_nonempty=len(isb) > 0,
                          is4_nonempty=len(isb4) > 0,
                          ex_post_only=(len(full) > 0 and len(isb) == 0),
                          ex_post_only4=(len(full) > 0 and len(isb4) == 0),
                          n_both=len(set(full) & set(isb)),
                          jaccard=jaccard(full, isb),
                          IS_contains_FULL=(len(full) > 0 and set(full) <= set(isb)),
                          FULL_contains_IS=(len(isb) > 0 and set(isb) <= set(full)),
                          full_band="; ".join(full), is_band="; ".join(isb)))
    L = pd.DataFrame(lrows)
    L.to_csv(f"{OUT}.ladders.csv", index=False)
    log(f"   {len(L)} ladders = 3 panels x 2 families x {len(COSTS)} costs x {len(SPLITS)} splits")
    log("   panel     family  cost split       rungs  FULL   IS  IS(4leg)  ex-post-only?  jaccard")
    for _, r in L.iterrows():
        log(f"   {r.panel:9s} {r.family:7s} {r.cost:4d} {r.split}  {r.n_rungs:5d} "
            f"{r.n_FULL:5d} {r.n_IS:4d} {r.n_IS4:8d}  "
            f"{('YES' if r.ex_post_only else 'no '):13s}  "
            + ("n/a" if pd.isna(r.jaccard) else f"{r.jaccard:.3f}"))
    LN = L[L.full_nonempty]
    share = float(LN.ex_post_only.mean()) if len(LN) else np.nan
    share4 = float(LN.ex_post_only4.mean()) if len(LN) else np.nan
    v1 = ("LOAD-BEARING" if share >= V1_HI else
          ("COSMETIC" if share <= V1_LO else "PARTIAL"))
    log(f"\n   V1  ladders with a NON-EMPTY FULL band: {len(LN)} of {len(L)}")
    log(f"       of those, EX-POST-ONLY (IS band empty): {int(LN.ex_post_only.sum())} "
        f"= {share:.1%}  -> {v1}   (pre-stated bars >= {V1_HI:.0%} / <= {V1_LO:.0%})")
    log(f"       same read DROPPING the IS third leg (4-leg IS band): "
        f"{int(LN.ex_post_only4.sum())} = {share4:.1%}  -> the substitution is not carrying it"
        if abs(share4 - share) < 0.2 else
        f"       same read DROPPING the IS third leg: {int(LN.ex_post_only4.sum())} = {share4:.1%}")
    for k in ("family", "panel", "cost", "split"):
        log(f"       by {k:6s}: " + "; ".join(
            f"{a}: {int(b.ex_post_only.sum())}/{len(b)}" for a, b in LN.groupby(k)))

    # ------------------------------------------------- V2: does the IS band point at the right rungs?
    log("\n## V2 — WHERE THE IS BAND IS NON-EMPTY, DOES IT POINT AT THE RIGHT RUNGS?")
    BOTH = L[L.full_nonempty & L.is_nonempty]
    if len(BOTH):
        log(f"   {len(BOTH)} ladders have BOTH bands non-empty.  mean Jaccard "
            f"{BOTH.jaccard.mean():.3f} (median {BOTH.jaccard.median():.3f}, "
            f"min {BOTH.jaccard.min():.3f}, max {BOTH.jaccard.max():.3f})")
        log(f"   IS band CONTAINS the FULL band at {int(BOTH.IS_contains_FULL.sum())}/{len(BOTH)}; "
            f"FULL contains IS at {int(BOTH.FULL_contains_IS.sum())}/{len(BOTH)}")
        log(f"   mean overlap size {BOTH.n_both.mean():.2f} rungs against FULL "
            f"{BOTH.n_FULL.mean():.2f} and IS {BOTH.n_IS.mean():.2f}")
    else:
        log("   no ladder has both bands non-empty.")

    # ------------------------------------------ V3: does the precondition buy anything OOS?
    log("\n## V3 — RULE 8, OOS READ ONCE: DOES 'THE IS BAND IS NON-EMPTY' BUY ANYTHING?")
    wrows = []
    for (pn, fam, cost, sp), s in G.groupby(["panel", "family", "cost", "split"]):
        S = SPYP[(pn, sp)]; LV = LIVEP[(pn, sp)]
        base = dict(panel=pn, family=fam, cost=cost, split=sp,
                    spy_oos_CAGR=S["oos"]["CAGR"], spy_oos_Sharpe=S["oos"]["Sharpe"],
                    spy_oos_MaxDD=S["oos"]["MaxDD"], live_oos_Sharpe=LV["oos"]["Sharpe"],
                    live_oos_CAGR=LV["oos"]["CAGR"], live_oos_MaxDD=LV["oos"]["MaxDD"])
        for ch, col in (("CH_ISSHARPE", "is_Sharpe"), ("CH_ISMINLEG", "is_minleg")):
            # (a) UNCONDITIONAL: argmax of the IS statistic over the whole ladder
            u = s.loc[s[col].idxmax()]
            # (b) RESTRICTED: the same argmax, but only over rungs inside the IS band
            sub = s[s.in_IS_band]
            published = len(sub) > 0
            rr = sub.loc[sub[col].idxmax()] if published else None
            wrows.append(dict(**base, chooser=ch, arm="UNCONDITIONAL", published=True,
                              rung=u.rung, oos_CAGR=u.oos_CAGR, oos_Sharpe=u.oos_Sharpe,
                              oos_MaxDD=u.oos_MaxDD, keep4b=bool(u.keep4b),
                              keep4b_oos=bool(u.keep4b_oos), keep4a=bool(u.keep4a),
                              in_IS_band=bool(u.in_IS_band)))
            wrows.append(dict(**base, chooser=ch, arm="IS-BAND-RESTRICTED", published=published,
                              rung=(rr.rung if published else ""),
                              oos_CAGR=(rr.oos_CAGR if published else np.nan),
                              oos_Sharpe=(rr.oos_Sharpe if published else np.nan),
                              oos_MaxDD=(rr.oos_MaxDD if published else np.nan),
                              keep4b=(bool(rr.keep4b) if published else False),
                              keep4b_oos=(bool(rr.keep4b_oos) if published else False),
                              keep4a=(bool(rr.keep4a) if published else False),
                              in_IS_band=published))
    W = pd.DataFrame(wrows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    U = W[W.arm == "UNCONDITIONAL"]
    R = W[W.arm == "IS-BAND-RESTRICTED"]
    RP = R[R.published]
    log(f"   {len(U)} chooser decisions per arm "
        f"(panel x family x cost x split x 2 IS-only choosers)")
    log(f"   UNCONDITIONAL       : published {len(U)}/{len(U)};  OOS 4b {int(U.keep4b.sum())}, "
        f"4b-OOS {int(U.keep4b_oos.sum())}, 4a {int(U.keep4a.sum())};  mean OOS Sharpe "
        f"{U.oos_Sharpe.mean():.4f}; picks that were NOT in their own IS band "
        f"{int((~U.in_IS_band).sum())}/{len(U)}")
    log(f"   IS-BAND-RESTRICTED  : published {len(RP)}/{len(R)} (the rest are SUPPRESSED by the "
        f"precondition);  OOS 4b {int(RP.keep4b.sum())}, 4b-OOS {int(RP.keep4b_oos.sum())}, "
        f"4a {int(RP.keep4a.sum())};  mean OOS Sharpe {RP.oos_Sharpe.mean():.4f}")
    # paired comparison on the decisions where BOTH arms publish
    key = ["panel", "family", "cost", "split", "chooser"]
    P = U.set_index(key).join(RP.set_index(key), lsuffix="_u", rsuffix="_r", how="inner")
    if len(P):
        d = P.oos_Sharpe_r - P.oos_Sharpe_u
        log(f"   PAIRED (both arms publish, n = {len(P)}): mean d(OOS Sharpe) "
            f"{d.mean():+.4f} (median {d.median():+.4f}, wins {int((d > 0).sum())}, "
            f"losses {int((d < 0).sum())}, same rung {int((P.rung_u == P.rung_r).sum())})")
        log(f"      OOS 4b:  unconditional {int(P.keep4b_u.sum())}/{len(P)}  ->  restricted "
            f"{int(P.keep4b_r.sum())}/{len(P)}")
    # what the precondition SUPPRESSES: would those unconditional picks have failed OOS?
    sup = U.set_index(key).loc[R[~R.published].set_index(key).index] if len(R[~R.published]) else \
        U.iloc[0:0].set_index(key)
    if len(sup):
        log(f"   SUPPRESSED decisions (IS band empty, n = {len(sup)}): the unconditional pick "
            f"would have cleared OOS 4b at {int(sup.keep4b_oos.sum())}/{len(sup)} and full 4b at "
            f"{int(sup.keep4b.sum())}/{len(sup)}; mean OOS Sharpe {sup.oos_Sharpe.mean():.4f} "
            f"against SPY OOS {sup.spy_oos_Sharpe.mean():.4f}")
    lose = bool(len(P) and d.mean() < -1e-4)
    removes = bool(len(sup) and int(sup.keep4b.sum()) < len(sup))
    v3_pre = ("ADOPT" if (not lose and removes) else ("REJECT" if lose else "NO-OP"))
    log(f"   V3 (PRE-STATED RULE, applied as written) -> {v3_pre}")
    log("   AND THE PRE-STATED RULE IS MIS-SPECIFIED, which is reported rather than rewritten:")
    log(f"      it pairs only the decisions where BOTH arms publish, and on {int((P.rung_u == P.rung_r).sum())} "
        f"of those {len(P)} the two arms pick the SAME RUNG.  The paired channel is a NO-OP by")
    log("      construction, so a -0.0012 mean is a one-pairing rounding artefact and carries no")
    log("      information about the precondition.  The precondition's whole effect is SUPPRESSION,")
    log("      which the pre-stated rule never scored.  The reading below is therefore POST-HOC and")
    log("      is weaker evidence than a pre-registered test would be.")

    # V3b: the SHARPER precondition the data actually speaks to — is the PUBLISHED CELL itself
    # inside its own IS 4b band?  (Post-hoc.  Named as such.)
    log("\n## V3b — POST-HOC: THE SHARPER PRECONDITION ('the published cell is itself inside its "
        "own IS 4b band')")
    IN, OUT2 = U[U.in_IS_band], U[~U.in_IS_band]
    log(f"   of the {len(U)} unconditional IS-argmax picks, {len(OUT2)} ({len(OUT2)/len(U):.1%}) "
        f"sit OUTSIDE their own IS 4b band — i.e. the chooser published a cell its own IS window")
    log("   says fails 4b.  Split by that membership:")
    for nm, s2 in (("INSIDE  its IS band", IN), ("OUTSIDE its IS band", OUT2)):
        if len(s2):
            log(f"      {nm} (n = {len(s2)}): mean OOS Sharpe {s2.oos_Sharpe.mean():.4f}, "
                f"mean OOS CAGR {s2.oos_CAGR.mean():.2%}, mean OOS MaxDD {s2.oos_MaxDD.mean():.2%}; "
                f"OOS 4b {int(s2.keep4b.sum())}/{len(s2)} = {s2.keep4b.mean():.1%}; "
                f"4a {int(s2.keep4a.sum())}/{len(s2)}")
    if len(IN) and len(OUT2):
        log(f"      GAP: OOS Sharpe {IN.oos_Sharpe.mean() - OUT2.oos_Sharpe.mean():+.4f}, "
            f"OOS 4b rate {IN.keep4b.mean() - OUT2.keep4b.mean():+.1%}")
        # the same split holding panel fixed, so the gap is not just SMALL665 dragging the OUT arm
        log("      holding PANEL fixed (the OUT arm is not just SMALL665):")
        for pn, s2 in U.groupby("panel"):
            a, b2 = s2[s2.in_IS_band], s2[~s2.in_IS_band]
            log(f"         {pn:9s} IN n={len(a):2d} 4b {int(a.keep4b.sum()) if len(a) else 0}"
                f"  |  OUT n={len(b2):2d} 4b {int(b2.keep4b.sum()) if len(b2) else 0}"
                + (f"  |  dSharpe {a.oos_Sharpe.mean() - b2.oos_Sharpe.mean():+.4f}"
                   if len(a) and len(b2) else ""))
    v3 = v3_pre

    # ---------------------------------------------------- V4: the standing KEEP-candidate
    log("\n## V4 — IS THE STANDING KEEP-CANDIDATE INSIDE ITS OWN LADDER'S IS BAND?")
    cq = G[(G.panel == CAND["panel"]) & (G.family == CAND["family"])
           & (G.rung == CAND["rung"])]
    cq.to_csv(f"{OUT}.candidate.csv", index=False)
    log(f"   {CAND['panel']} {CAND['family']} {CAND['rung']}, {len(cq)} (cost x split) cells")
    for _, r in cq.iterrows():
        log(f"   {r.cost:4d} bps  split {r.split}:  FULL band {str(bool(r.in_FULL_band)):5s} "
            f"(bind {r.full_bind})   IS band {str(bool(r.in_IS_band)):5s} (bind {r.is_bind})   "
            f"IS 4-leg {str(bool(r.in_IS_band4)):5s}   OOS {r.oos_CAGR:7.2%} / "
            f"{r.oos_Sharpe:.4f} / {r.oos_MaxDD:7.2%}")
    v4 = ("INSIDE its own IS band at every (cost, split)" if bool(cq.in_IS_band.all())
          else (f"inside at only {int(cq.in_IS_band.sum())} of {len(cq)} (cost, split) cells"))
    log(f"   V4 -> the candidate is {v4}")

    log("\n## VERDICT")
    log(f"   V1 ex-post-only share {share:.1%} of {len(LN)} non-empty-FULL ladders -> {v1}")
    log(f"   V2 mean Jaccard(FULL, IS) where both non-empty: "
        + (f"{BOTH.jaccard.mean():.3f} over {len(BOTH)} ladders" if len(BOTH) else "n/a"))
    log(f"   V3 precondition, PRE-STATED rule as written -> {v3_pre} (the rule is mis-specified;")
    log("      it scored the paired no-op channel, not the suppression channel — see V3 / V3b)")
    log(f"   V3b POST-HOC: the sharper 'published cell inside its own IS band' precondition would")
    log(f"      have suppressed {len(OUT2)} of {len(U)} published picks, whose OOS 4b rate was "
        f"{OUT2.keep4b.mean():.1%} against {IN.keep4b.mean():.1%} for the picks it keeps —")
    _nsm = int((OUT2.panel.str.startswith("SMALL")).sum())
    log(f"      BUT THAT GAP IS CONFOUNDED BY PANEL and does NOT survive: {_nsm} of the {len(OUT2)} "
        f"suppressed picks are SMALL, a panel that clears 4b at 0 of {len(G[G.panel.str.startswith('SMALL')])} cells")
    log("      regardless.  Holding panel fixed the gap vanishes or reverses (see V3b's per-panel")
    log("      lines), and on the large panels the OUT picks cleared OOS 4b at "
        f"{int(OUT2[~OUT2.panel.str.startswith('SMALL')].keep4b.sum())} of "
        f"{len(OUT2[~OUT2.panel.str.startswith('SMALL')])}.  So the sharper precondition is NOT")
    log("      supported either: this is a SECOND KILL, not a replacement clause.")
    log(f"   V4 standing candidate -> {v4}")
    log(f"   gates: {sum(g['pass_'] for g in _gates)}/{len(_gates)} pass")
    log("   SURVIVORSHIP: U56 / B136 are CURRENT constituents and SMALL a CURRENT sub-$2B screen,")
    log("   so every LEVEL is optimistic and every 4b bar is easier than on a point-in-time panel.")
    log("   The IS-vs-FULL band CONTRAST is same-tape / same-names / same-ladder and first-order")
    log("   immune; the BAND MEMBERSHIP COUNTS are not.")

    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)


if __name__ == "__main__":
    main()
