#!/usr/bin/env python3
"""Idea 1545 (lane cloud, 2026-09-22): does DE-GROSSING dominate every DEVICE on the
DRAWDOWN axis too?

Idea 1534 priced 90 (device, matched-exposure de-gross) pairs on SHARPE and found the
pooled dMaxDD NEGATIVE (-1.55 pp), i.e. the plain de-gross twin is not merely cheaper but
SHALLOWER.  A pooled mean is one number at one exposure.  This run traces the FULL
(CAGR, MaxDD) frontier of a constant de-gross ladder and places all 90 of 1534's device
books against it, so the record can say whether de-gross is the efficient frontier for
DRAWDOWN as well as for return -- and, where a device sits inside, BY HOW MUCH.

CONSTRUCTION (identical book to 1534, so the two runs are comparable line for line)
  BASE (frozen, the record's 2026-09-04 anchor shape): top-N by H-day momentum among names
  above their 200d MA with vol20 < 0.60, equal weight at gross 0.75, weekly, 10 bps, t+1.
  TUNED PARAMETERS: exactly two, (N, H) = (20, 126), FROZEN at the committed anchor.  They
  are NOT searched here.  Every other axis below is PUBLISHED in full, none is selected.

  LADDER (the frontier): the SAME base book multiplied by a CONSTANT f, f = 0.02 .. 1.00 in
  0.02 steps (50 rungs per panel).  Withdrawn weight goes to CASH.  This is "de-grossing"
  with zero free content -- it knows nothing, times nothing, and costs strictly less
  turnover than the book it scales.
  DEVICES (the comparands): 1534's six families x five rungs x three panels = 90 books --
  BAND, STOP, VOLTGT, MAXVOL, MADIST, SPYFILT -- every one an overlay that WITHDRAWS
  exposure.  Rungs are 1534's, copied verbatim, not re-chosen.

  FRONTIER TEST.  For each device book, the ladder is interpolated to the rung with the
  SAME MaxDD (vertical test: how much CAGR does the device give up at its own drawdown?)
  and to the rung with the SAME CAGR (horizontal test: how much deeper is the device at its
  own return?).  A device is INSIDE the frontier when some ladder rung beats it on BOTH
  axes at once (strict Pareto domination).  The matched-GROSS anchor of 1534 is re-run
  EXACTLY (one extra backtest at the interpolated f) so this run restates 1534's pooled
  dMaxDD on its own ladder rather than assuming it.

  RULE 8.  f (and the device rung) chosen on 2009-2016 ONLY by an IS ruler, 2017-2026 read
  ONCE.  Two rulers published side by side (IS Calmar -- the drawdown-axis ruler this idea
  is about -- and IS Sharpe), plus C_LIVE, the shipped f = 1.00 / no-device control, which
  carries no information at all.

  BOTH KEEP PATHS are evaluated at EVERY published book (4a vs live RULES v2, 4b vs SPY),
  full sample and OOS.

Outputs (beside this file):
  *.frontier.csv    the de-gross ladder, 3 panels x 50 rungs
  *.grid.csv        every published book: ladder, devices, anchors, references
  *.dominance.csv   per device: matched-DD / matched-CAGR / matched-gross gaps
  *.walkforward.csv rule-8 choosers
  *.gates.csv       every asserted gate with its realised value
  *.out.txt         stdout

Run: python3 research/backtests/2026-09-22_degross-frontier-on-the-drawdown-axis_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state   # noqa
from engine import backtest                                                          # noqa

OUT       = Path(__file__).with_suffix("")
N_FROZEN  = 20          # tuned parameter 1 (frozen at the committed 2026-09-04 anchor)
H_FROZEN  = 126         # tuned parameter 2 (frozen at the committed 2026-09-04 anchor)
GROSS     = 0.75
MAXVOL    = 0.60
COST_BPS  = 10          # PROTOCOL rule 2
FREQ      = "W"
WARMUP    = 260         # rows skipped, same convention as baseline.compare
OOS_START = pd.Timestamp("2017-01-01")
IS_END    = pd.Timestamp("2016-12-31")
STOP_FRAC = 0.50        # 1468's committed re-entry fraction, frozen
LADDER    = np.round(np.arange(0.02, 1.0001, 0.02), 4)

# ------------------------------------------------------------------ book construction
def _feat(px):
    mom   = px / px.shift(H_FROZEN) - 1
    ma200 = px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return mom, ma200, vol20

def base_weights(px, maxvol=MAXVOL, madist=0.0, band=None):
    mom, ma200, vol20 = _feat(px)
    above = band_state(px, band) if band is not None else (px > ma200 * (1 + madist))
    elig  = mom.where(above & (vol20 < maxvol))
    rank  = elig.rank(axis=1, ascending=False)
    return (rank <= N_FROZEN).astype(float) * (GROSS / N_FROZEN)

def trailing_stop_mult(eq, depth, frac=STOP_FRAC):
    """Causal 0/1 gross multiplier from the BASE book's own equity (1534's device)."""
    eq = eq.ffill().bfill(); e = eq.values
    m = np.ones(len(e)); peak = e[0]; out = False; trough = np.nan
    for i in range(len(e)):
        if not out:
            peak = max(peak, e[i])
            if e[i] <= peak * (1 - depth): out = True; trough = e[i]
        else:
            trough = min(trough, e[i])
            if e[i] >= trough + frac * (peak - trough): out = False; peak = max(peak, e[i])
        m[i] = 0.0 if out else 1.0
    return pd.Series(m, index=eq.index)

def device_books(px, base_w, base_r, base_eq):
    """1534's 30 device books per panel, rungs copied verbatim."""
    out = {}
    spy = px["SPY"] if "SPY" in px.columns else None
    for c in (0.02, 0.04, 0.06, 0.08, 0.10):
        out[("BAND", f"c={c:.2f}")] = base_weights(px, band=c)
    for d in (0.05, 0.075, 0.10, 0.15, 0.20):
        out[("STOP", f"d={d:.3f}")] = base_w.mul(trailing_stop_mult(base_eq, d), axis=0)
    rv = base_r.rolling(20).std() * np.sqrt(252)
    for v in (0.08, 0.10, 0.12, 0.15, 0.20):
        s = (v / rv.replace(0, np.nan)).clip(upper=1.0).fillna(1.0)
        out[("VOLTGT", f"v={v:.2f}")] = base_w.mul(s.reindex(base_w.index).fillna(1.0), axis=0)
    for m in (0.25, 0.35, 0.45, 0.60, 0.80):
        out[("MAXVOL", f"m={m:.2f}")] = base_weights(px, maxvol=m)
    for k in (0.00, 0.03, 0.06, 0.10, 0.15):
        out[("MADIST", f"k={k:.2f}")] = base_weights(px, madist=k)
    for L in (100, 150, 200, 250, 300):
        ind = (spy > spy.rolling(L).mean()).astype(float) if spy is not None else 1.0
        out[("SPYFILT", f"L={L}")] = base_w.mul(ind, axis=0)
    return out

# ------------------------------------------------------------------ metrics
def sharpe(r):  return r.mean() * 252 / (r.std() * np.sqrt(252)) if r.std() > 0 else np.nan
def maxdd(r):   e = (1 + r).cumprod(); return float((e / e.cummax() - 1).min())
def cagr(r):    e = (1 + r).cumprod(); return float(e.iloc[-1] ** (252 / len(r)) - 1)

def full_metrics(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]),
                IS_CAGR=cagr(r.loc[:IS_END]), IS_Sharpe=sharpe(r.loc[:IS_END]),
                IS_MaxDD=maxdd(r.loc[:IS_END]),
                OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                OOS_MaxDD=maxdd(r.loc[OOS_START:]))

def keep_paths(m, v2, spy):
    """4a: Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse.
       4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.
       4b_OOS: the same five legs read on 2017-2026 alone."""
    a = (m["H1"] > v2["H1"]) and (m["H2"] > v2["H2"]) and (m["MaxDD"] >= v2["MaxDD"])
    b = (m["H1"] > spy["H1"]) and (m["H2"] > spy["H2"]) and (m["OOS_Sharpe"] > spy["OOS_Sharpe"]) \
        and (m["MaxDD"] >= 0.60 * spy["MaxDD"]) and (m["CAGR"] >= 0.70 * spy["CAGR"])
    b_oos = (m["OOS_Sharpe"] > spy["OOS_Sharpe"]) and (m["OOS_MaxDD"] >= 0.60 * spy["OOS_MaxDD"]) \
        and (m["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])
    return a, b, b_oos

def run(px, w, start):
    res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    return res["returns"].loc[start:], float(res["weights"].sum(axis=1).loc[start:].mean())

def interp(xs, ys, x):
    """Linear interpolation of y at x on a ladder sorted by x ascending; NaN outside."""
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    o = np.argsort(xs); xs, ys = xs[o], ys[o]
    if not (xs[0] <= x <= xs[-1]): return np.nan
    return float(np.interp(x, xs, ys))


# ------------------------------------------------------------------ addendum
def addendum(GD=None, FR=None, DM=None, say=print):
    """Second read of the SAME published books, no new backtest:
       (a) identity rungs -- device books that ARE the un-overlaid BASE book, whose paired
           difference is 0 BY CONSTRUCTION and which shrink any pooled mean toward zero;
       (b) the frontier test re-run on the OOS window (2017-2026) ALONE, so the run can say
           whether a device sitting outside the frontier stays outside out of sample."""
    if GD is None:
        GD = pd.read_csv(f"{OUT}.grid.csv"); FR = pd.read_csv(f"{OUT}.frontier.csv")
        DM = pd.read_csv(f"{OUT}.dominance.csv")
    ident = []
    for _, r in DM.iterrows():
        top = FR[FR.panel == r.panel].sort_values("f").iloc[-1]
        ident.append(abs(r.dev_CAGR - top.CAGR) < 1e-12 and abs(r.dev_MaxDD - top.MaxDD) < 1e-12)
    DM = DM.assign(identity=ident)
    say("\n================ ADDENDUM (a): IDENTITY RUNGS ================")
    say(f"device books that ARE the BASE book (paired d == 0 by construction): "
        f"{int(DM.identity.sum())} of {len(DM)}")
    say(DM[DM.identity].groupby('family').size().to_string())
    nd = DM[~DM.identity]
    say(f"ex-identity: dominated {int(nd.dominated.sum())} of {len(nd)} ({nd.dominated.mean():.1%})")
    for c, u in (("d_Sharpe_matchedgross", 1.0), ("d_CAGR_matchedgross", 100.0),
                 ("d_MaxDD_matchedgross", 100.0)):
        a, b = DM[c].dropna() * u, nd[c].dropna() * u
        say(f"  {c:24s} all n{len(a)} mean {a.mean():+.4f} | ex-identity n{len(b)} "
            f"mean {b.mean():+.4f} median {b.median():+.4f} share>0 {(b>0).mean():.1%}")
    unm = DM[DM.vertical_CAGR_gap.isna()]
    say(f"\nUNMATCHABLE on the vertical (device MaxDD DEEPER than the un-overlaid BASE book "
        f"it overlays, so no ladder rung reaches it): {len(unm)} of {len(DM)}; "
        f"of which strictly dominated anyway: {int(unm.dominated.sum())}")
    say(unm.groupby('family').size().to_string())

    say("\n================ ADDENDUM (b): THE SAME TEST ON 2017-2026 ALONE ================")
    rows = []
    for _, r in DM.iterrows():
        L = FR[FR.panel == r.panel]
        dc, dd = None, None
        dev = GD[(GD.panel == r.panel) & (GD.family == r.family) & (GD.rung == r.rung)]
        if not len(dev): continue
        dev = dev.iloc[0]
        v = interp(L["OOS_MaxDD"].values, L["OOS_CAGR"].values, dev.OOS_MaxDD)
        cand = L[L["OOS_CAGR"] >= dev.OOS_CAGR]
        h = float(cand["OOS_MaxDD"].max()) if len(cand) else np.nan
        better = L[(L.OOS_CAGR > dev.OOS_CAGR) & (L.OOS_MaxDD > dev.OOS_MaxDD)]
        rows.append(dict(panel=r.panel, family=r.family, rung=r.rung, identity=r.identity,
                         oos_vertical_CAGR_gap=dev.OOS_CAGR - v,
                         oos_horizontal_MaxDD_gap=dev.OOS_MaxDD - h,
                         oos_dominated=bool(len(better))))
    O = pd.DataFrame(rows); O.to_csv(f"{OUT}.oos_frontier.csv", index=False)
    say(f"OOS strictly dominated: {int(O.oos_dominated.sum())} of {len(O)} "
        f"({O.oos_dominated.mean():.1%})   [full sample: {int(DM.dominated.sum())} of {len(DM)}]")
    say(O.groupby('family').oos_dominated.agg(['sum', 'count', 'mean']).to_string())
    say(O.groupby('panel').oos_dominated.agg(['sum', 'count', 'mean']).to_string())
    agree = (O.oos_dominated.values == DM.dominated.values[:len(O)])
    say(f"full-sample and OOS verdicts AGREE on {agree.sum()} of {len(O)} books ({agree.mean():.1%})")
    v = O.oos_vertical_CAGR_gap.dropna() * 100
    say(f"OOS vertical gap: n {len(v)} mean {v.mean():+.2f} median {v.median():+.2f} "
        f"share<0 {(v<0).mean():.1%}")
    say("\nOOS vertical gap by family (pp/yr):")
    say(O.groupby('family').oos_vertical_CAGR_gap.agg(
        n='count', mean=lambda s: s.mean() * 100, median=lambda s: s.median() * 100,
        share_neg=lambda s: (s < 0).mean()).to_string(float_format=lambda x: f"{x:+.3f}"))
    say("\nVOLTGT, the one family outside the frontier -- full sample vs OOS, cell by cell:")
    m = DM[DM.family == 'VOLTGT'][['panel', 'rung', 'vertical_CAGR_gap', 'horizontal_MaxDD_gap',
                                   'dominated']].merge(
        O[O.family == 'VOLTGT'][['panel', 'rung', 'oos_vertical_CAGR_gap',
                                 'oos_horizontal_MaxDD_gap', 'oos_dominated']],
        on=['panel', 'rung'])
    say(m.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    return O

# ------------------------------------------------------------------ main
def main():
    t0 = time.time(); log = []
    def say(s):
        print(s, flush=True); log.append(str(s))

    say("IDEA 1545 -- de-gross (CAGR, MaxDD) frontier vs 1534's 90 device books")
    say(f"BASE frozen at N={N_FROZEN}, H={H_FROZEN}, gross={GROSS}, maxvol={MAXVOL}, "
        f"freq={FREQ}, cost={COST_BPS} bps, t+1.  Ladder f = {LADDER[0]}..{LADDER[-1]} "
        f"step 0.02 ({len(LADDER)} rungs).")

    grid, front, dom, gates, wf = [], [], [], [], []

    for lbl, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        px = load_universe(**kw)
        if lbl == "SMALL":                      # brief: drop blow-up rows before anything else
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad  = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
            keep = [c for c in px.columns if c == "SPY" or c not in bad]
            gates.append(dict(panel=lbl, gate="G0_small_blowups_dropped",
                              value=px.shape[1] - len(keep), expect=">0", ok=px.shape[1] > len(keep)))
            px = px[keep]
        start = px.index[WARMUP]
        bw    = base_weights(px)
        bres  = backtest(px, bw, cost_bps=COST_BPS, freq=FREQ)
        base_r = bres["returns"].loc[start:]
        base_g = float(bres["weights"].sum(axis=1).loc[start:].mean())
        spy_r  = px["SPY"].pct_change().fillna(0).loc[start:]
        v2_r   = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        v1_r   = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        spy_m, v2_m, v1_m = full_metrics(spy_r), full_metrics(v2_r), full_metrics(v1_r)
        say(f"\n[{lbl}] {px.shape[1]} cols  {start.date()}..{px.index[-1].date()}  "
            f"base gross {base_g:.4f}  ({time.time()-t0:.0f}s)")

        for nm, m in (("SPY", spy_m), ("RULESv2_live", v2_m), ("RULESv1", v1_m)):
            a, b, bo = keep_paths(m, v2_m, spy_m)
            grid.append(dict(panel=lbl, family="REF", rung=nm, f=np.nan, gross=np.nan,
                             keep4a=a, keep4b=b, keep4b_oos=bo, **m))

        # ---------------- the de-gross ladder (the frontier) --------------------
        lad = []
        for f in LADDER:
            r, g = run(px, bw * f, start)
            m = full_metrics(r); a, b, bo = keep_paths(m, v2_m, spy_m)
            row = dict(panel=lbl, f=float(f), gross=g, **m)
            lad.append(row); front.append(row)
            grid.append(dict(panel=lbl, family="DEGROSS", rung=f"f={f:.2f}", f=float(f),
                             gross=g, keep4a=a, keep4b=b, keep4b_oos=bo, **m))
        L = pd.DataFrame(lad).sort_values("f").reset_index(drop=True)
        say(f"  ladder done ({time.time()-t0:.0f}s).  f=1.00 -> CAGR {L.CAGR.iloc[-1]:.2%} "
            f"MaxDD {L.MaxDD.iloc[-1]:.2%} Sharpe {L.Sharpe.iloc[-1]:.4f}")

        # gates on the ladder's shape
        dmdd = np.diff(L["MaxDD"].values)          # expect <= 0: deeper as f rises
        dcag = np.diff(L["CAGR"].values)
        dgro = np.diff(L["gross"].values)
        gates += [dict(panel=lbl, gate="G1_MaxDD_monotone_deeper_in_f",
                       value=float(dmdd.max()), expect="<=0", ok=bool(dmdd.max() <= 1e-12)),
                  dict(panel=lbl, gate="G2_gross_monotone_in_f",
                       value=float(dgro.min()), expect=">0", ok=bool(dgro.min() > 0)),
                  dict(panel=lbl, gate="G3_CAGR_monotone_in_f_(reported_not_required)",
                       value=float(dcag.min()), expect="report", ok=True),
                  dict(panel=lbl, gate="G4_ladder_top_is_base",
                       value=float(abs(L["gross"].iloc[-1] - base_g)), expect="~0",
                       ok=bool(abs(L["gross"].iloc[-1] - base_g) < 1e-9))]

        # ---------------- the 90 device books, against the frontier -------------
        books = device_books(px, bw, base_r, bres["equity"])
        for (fam, rung), w in books.items():
            dr, dg = run(px, w, start)
            dm = full_metrics(dr); a, b, bo = keep_paths(dm, v2_m, spy_m)
            grid.append(dict(panel=lbl, family=fam, rung=rung, f=np.nan, gross=dg,
                             keep4a=a, keep4b=b, keep4b_oos=bo, **dm))

            # (i) matched-GROSS anchor, run EXACTLY at the interpolated f (1534's contrast)
            f_star = interp(L["gross"].values, L["f"].values, dg)
            if np.isnan(f_star):
                ar, ag, am = None, np.nan, {k: np.nan for k in dm}
            else:
                ar, ag = run(px, bw * float(f_star), start); am = full_metrics(ar)
                grid.append(dict(panel=lbl, family="ANCHOR", rung=f"{fam}:{rung}",
                                 f=float(f_star), gross=ag,
                                 **dict(zip(["keep4a", "keep4b", "keep4b_oos"],
                                            keep_paths(am, v2_m, spy_m))), **am))
            # (ii) matched-MaxDD: what CAGR does the frontier pay at the device's own DD?
            cagr_at_dd = interp(L["MaxDD"].values, L["CAGR"].values, dm["MaxDD"])
            # (iii) matched-CAGR: how deep is the frontier at the device's own return?
            dd_at_cagr = interp(L["CAGR"].values, L["MaxDD"].values, dm["CAGR"]) \
                if L["CAGR"].is_monotonic_increasing else np.nan
            if np.isnan(dd_at_cagr):                 # CAGR need not be monotone in f -> use the
                cand = L[L["CAGR"] >= dm["CAGR"]]    # SHALLOWEST rung that matches or beats it
                dd_at_cagr = float(cand["MaxDD"].max()) if len(cand) else np.nan
            # (iv) strict Pareto domination by ANY ladder rung
            better = L[(L["CAGR"] > dm["CAGR"]) & (L["MaxDD"] > dm["MaxDD"])]
            dom.append(dict(panel=lbl, family=fam, rung=rung, gross_dev=dg, gross_anc=ag,
                            f_star=f_star,
                            dev_CAGR=dm["CAGR"], dev_MaxDD=dm["MaxDD"], dev_Sharpe=dm["Sharpe"],
                            anc_CAGR=am["CAGR"], anc_MaxDD=am["MaxDD"], anc_Sharpe=am["Sharpe"],
                            d_Sharpe_matchedgross=dm["Sharpe"] - am["Sharpe"],
                            d_CAGR_matchedgross=dm["CAGR"] - am["CAGR"],
                            d_MaxDD_matchedgross=dm["MaxDD"] - am["MaxDD"],
                            frontier_CAGR_at_dev_MaxDD=cagr_at_dd,
                            vertical_CAGR_gap=dm["CAGR"] - cagr_at_dd,
                            frontier_MaxDD_at_dev_CAGR=dd_at_cagr,
                            horizontal_MaxDD_gap=dm["MaxDD"] - dd_at_cagr,
                            dominated=bool(len(better)),
                            n_dominating_rungs=int(len(better))))
        say(f"  30 device books + anchors done ({time.time()-t0:.0f}s)")

        # ---------------- rule 8: choose on 2009-2016, read 2017-2026 ONCE -------
        G = pd.DataFrame([g for g in grid if g["panel"] == lbl])
        pools = {"DEGROSS_LADDER": G[G.family == "DEGROSS"],
                 "DEVICES": G[G.family.isin(["BAND", "STOP", "VOLTGT", "MAXVOL", "MADIST", "SPYFILT"])]}
        for pool_name, P in pools.items():
            for ruler in ("IS_Sharpe", "IS_CALMAR"):
                key = P["IS_Sharpe"] if ruler == "IS_Sharpe" else P["IS_CAGR"] / P["IS_MaxDD"].abs()
                pick = P.loc[key.idxmax()]
                wf.append(dict(panel=lbl, pool=pool_name, ruler=ruler,
                               pick=f"{pick.family}:{pick.rung}", gross=pick.gross,
                               IS_Sharpe=pick.IS_Sharpe, IS_CAGR=pick.IS_CAGR, IS_MaxDD=pick.IS_MaxDD,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD, keep4b=pick.keep4b, keep4b_oos=pick.keep4b_oos))
        live = G[(G.family == "DEGROSS") & (G.rung == "f=1.00")].iloc[0]
        for nm, m in (("C_LIVE_f1.00", live), ("SPY", G[G.rung == "SPY"].iloc[0]),
                      ("RULESv2_live", G[G.rung == "RULESv2_live"].iloc[0])):
            wf.append(dict(panel=lbl, pool="CONTROL", ruler="none", pick=nm, gross=m.gross,
                           IS_Sharpe=m.IS_Sharpe, IS_CAGR=m.IS_CAGR, IS_MaxDD=m.IS_MaxDD,
                           OOS_CAGR=m.OOS_CAGR, OOS_Sharpe=m.OOS_Sharpe, OOS_MaxDD=m.OOS_MaxDD,
                           keep4b=m.keep4b, keep4b_oos=m.keep4b_oos))

    # ------------------------------------------------------------------ report
    GD = pd.DataFrame(grid); FR = pd.DataFrame(front); DM = pd.DataFrame(dom)
    WF = pd.DataFrame(wf);   GA = pd.DataFrame(gates)
    GD.to_csv(f"{OUT}.grid.csv", index=False)
    FR.to_csv(f"{OUT}.frontier.csv", index=False)
    DM.to_csv(f"{OUT}.dominance.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    GA.to_csv(f"{OUT}.gates.csv", index=False)

    say("\n================ GATES ================")
    say(GA.to_string(index=False))

    say("\n================ THE FRONTIER (de-gross ladder, selected rungs) ================")
    sel = FR[FR.f.isin([0.10, 0.25, 0.50, 0.75, 1.00])]
    say(sel[["panel", "f", "gross", "CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe",
             "OOS_MaxDD"]].to_string(index=False,
             float_format=lambda x: f"{x:.4f}"))

    say("\n================ DOMINANCE: how many of the 90 sit INSIDE the frontier ================")
    say(f"devices priced: {len(DM)}  (expect 90)")
    say(f"STRICTLY DOMINATED by at least one ladder rung (better CAGR *and* shallower MaxDD): "
        f"{int(DM.dominated.sum())} of {len(DM)}  ({DM.dominated.mean():.1%})")
    say("\nby panel:")
    say(DM.groupby("panel").dominated.agg(["sum", "count", "mean"]).to_string())
    say("\nby family:")
    say(DM.groupby("family").dominated.agg(["sum", "count", "mean"]).to_string())
    say("\nVERTICAL gap (device CAGR minus frontier CAGR at the device's OWN MaxDD; "
        "negative = inside the frontier), pp/yr:")
    v = DM["vertical_CAGR_gap"].dropna() * 100
    say(f"  n {len(v)}  mean {v.mean():+.2f}  median {v.median():+.2f}  "
        f"min {v.min():+.2f}  max {v.max():+.2f}  share<0 {(v < 0).mean():.1%}")
    say(DM.groupby("family")["vertical_CAGR_gap"].agg(
        n="count", mean=lambda s: s.mean() * 100, median=lambda s: s.median() * 100,
        worst=lambda s: s.min() * 100, best=lambda s: s.max() * 100).to_string(
        float_format=lambda x: f"{x:+.2f}"))
    say("\nHORIZONTAL gap (device MaxDD minus frontier MaxDD at the device's OWN CAGR; "
        "negative = device is DEEPER for the same return), pp:")
    h = DM["horizontal_MaxDD_gap"].dropna() * 100
    say(f"  n {len(h)}  mean {h.mean():+.2f}  median {h.median():+.2f}  "
        f"min {h.min():+.2f}  max {h.max():+.2f}  share<0 {(h < 0).mean():.1%}")
    say("\n1534 RESTATED on this ladder (matched-GROSS anchor, exact re-run):")
    for c, u in (("d_Sharpe_matchedgross", 1.0), ("d_CAGR_matchedgross", 100.0),
                 ("d_MaxDD_matchedgross", 100.0)):
        s = DM[c].dropna() * u
        say(f"  {c:26s} mean {s.mean():+.4f}  median {s.median():+.4f}  "
            f"share>0 {(s > 0).mean():.1%}  n {len(s)}")

    say("\n================ KEEP PATHS over every published book ================")
    say(f"books published: {len(GD)}")
    say(GD.groupby("family")[["keep4a", "keep4b", "keep4b_oos"]].sum().to_string())
    k4a = GD[GD.keep4a & (GD.family != "REF")]
    k4b = GD[GD.keep4b & GD.keep4b_oos & (GD.family != "REF")]
    say(f"\n4a passers: {len(k4a)}   4b passers (FULL and OOS): {len(k4b)}")
    if len(k4b):
        say(k4b[["panel", "family", "rung", "gross", "CAGR", "Sharpe", "MaxDD",
                 "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
                 index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n================ RULE 8 (chosen on 2009-2016, 2017-2026 read ONCE) ================")
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    piv = WF[WF.pool != "CONTROL"].pivot_table(index=["panel", "ruler"], columns="pool",
                                               values="OOS_Sharpe")
    if {"DEGROSS_LADDER", "DEVICES"} <= set(piv.columns):
        piv["degross_minus_device"] = piv["DEGROSS_LADDER"] - piv["DEVICES"]
        say("\nOOS Sharpe, de-gross chooser minus device chooser (positive = the frontier wins):")
        say(piv.to_string(float_format=lambda x: f"{x:+.4f}"))
        say(f"  de-gross wins {int((piv['degross_minus_device'] > 0).sum())} of {len(piv)} "
            f"(panel x ruler) families; mean {piv['degross_minus_device'].mean():+.4f}")

    addendum(GD, FR, DM, say)

    say(f"\ndone in {time.time()-t0:.0f}s")
    Path(f"{OUT}.out.txt").write_text("\n".join(log) + "\n")

if __name__ == "__main__":
    if "--addendum" in sys.argv:          # re-read of the committed CSVs, no backtest
        addendum()
    else:
        main()
