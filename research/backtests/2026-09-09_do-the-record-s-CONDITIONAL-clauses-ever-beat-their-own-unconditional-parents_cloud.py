#!/usr/bin/env python3
"""Idea 317 — DO THE RECORD'S CONDITIONAL CLAUSES EVER BEAT THEIR OWN UNCONDITIONAL PARENTS
   (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number below was read)
    Idea 48's decisive test was not 4a/4b but "does the conditional rule beat BOTH the rules
    it interpolates" (answer 4/16 full-sample, 0/16 on drawdown).  Audit every committed
    conditional / regime-switching book against that bar with its own two parents run at
    MATCHED GROSS.  If conditional clauses systematically fail it, the bar belongs in
    PROTOCOL rule 4 as a precondition for KEEP, ahead of the half-sample tests.

WHAT IS UNDER TEST, and the one honest scoping decision.  The LEADERBOARD's conditional
books are prose rows, not runnable objects: they cannot be re-executed from the markdown.
So this run does NOT claim to re-run "every committed row".  It rebuilds the record's
recurring conditional FORM — "hold book A while a market state is ON, hold book B while it
is OFF" — as a pre-registered menu spanning the clause families the record actually uses
(trend gate, breadth gate, calm/vol gate, momentum gate; concentration switches; cash
de-grossing), and runs every one of them against its own two parents at matched gross on
three panels.  That is a strictly larger and fully reproducible sample than the prose rows,
and the bar it reports is idea 48's, unchanged.

THE MENU (fixed before any number was read)
  FORMS (the parents; each is a complete unconditional book at the SAME gross g=0.75)
      EWALL     equal weight every priced name, gross g
      TOP10     top 10 by the baseline composite score, g/10 each
      TOP20     top 20 by the same score, g/20 each
      MADG      EWALL masked by the per-name 200d +/-3% band, gated weight to CASH
                (this is the live RULES v2 form)
      LOWVOL20  the 20 lowest 20d-realised-vol names, g/20 each
      CASH      zero weights
  STATES (market-level, decided at close t, no look-ahead anywhere: every quantile is an
          EXPANDING quantile with min_periods=252, so the state at t uses only <= t)
      TREND   SPY > its own 200d MA                              (no quantile)
      MOM12   SPY 12-month total return > 0                      (no quantile)
      BREADTH panel fraction above 200d MA > its expanding q-quantile
      CALM    panel equal-weight-index 20d vol < its expanding q-quantile
  CONDITIONAL  C(A,B,S) = A on days S is ON, B on days S is OFF, A != B.
      6 forms -> 30 ordered pairs, x 8 states (TREND, MOM12, BREADTH@3q, CALM@3q)
      = 240 conditional books per panel, on 3 panels = 720, plus 18 parents.
  PANELS  U56 (research/universe.json), B136 (universe_broad.json), SMALL439
      (data/prices_small.csv, the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv
      DROPPED first, leaving 439).  SURVIVORSHIP: the small panel is current constituents
      of the screen only, so its levels are optimistic; it is used here as a THIRD PANEL for
      a parents test that is a WITHIN-panel comparison (conditional vs its own two parents on
      the same names), which survivorship bias does not manufacture.

THE BAR (idea 48's, unchanged).  A conditional book PASSES on a metric only if it beats
BOTH parents on that metric, computed on the same window, same gross, same costs:
      CAGR   C > max(A, B)          Sharpe C > max(A, B)          MaxDD  C > max(A, B)
             (MaxDD is negative; "beats" = less deep)
      ALL3   all three at once.
Reported full-sample, on each half, and on the untouched OOS window.

THE TWO TUNED PARAMETERS (exactly two; every other axis is a REPORTING axis, printed at
every value and never selected on)
    P1  q, the state quantile: ALL of {0.30, 0.50, 0.70} reported; 0.50 is the point value.
    P2  in the RULE 8 selector ONLY, the (pair, state) cell chosen on IS.
  Panel, form, state family, half and metric are reporting axes.

COSTS AND EXECUTION are PROTOCOL's: 10 bps per unit turnover, weights decided at close t
applied at t+1, weekly rebalance, no shorting, no leverage.  Gross is 0.75 for EVERY book
including both parents, so no comparison here is a gross comparison.

RULE 8 (PROTOCOL 8).  Parameters chosen on 2010-2016 ONLY; 2017-01-01.. read ONCE.
    Selector: among conditional books that pass the ALL3 parents bar IN SAMPLE, take the
    highest IS Sharpe.  If none passes ALL3, fall back to the highest IS Sharpe among
    Sharpe-bar passers, and say so.  Report the pick's OOS CAGR / Sharpe / MaxDD against the
    live RULES v2 baseline, RULES v1 and SPY on the same panel, and evaluate BOTH KEEP paths
    (4a beat-the-book, 4b capital-worthy).

GATE  G1  fast_backtest reproduces engine.backtest to < 1e-12 on a real book before any
          menu number is read.

OUTPUTS  .books.csv (every book, every panel, every window), .parents.csv (the bar, every
cell), .grid.csv (pass counts at every q and every metric), .walkforward.csv, .console.txt
"""
import sys, io, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, band_state, rules_v1_weights, rules_v2_weights  # noqa
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STEM = ROOT / "research" / "backtests" / "2026-09-09_do-the-record-s-CONDITIONAL-clauses-ever-beat-their-own-unconditional-parents_cloud"
COST, FREQ, GROSS = 10.0, "W", 0.75
QS = [0.30, 0.50, 0.70]
OOS0 = "2017-01-01"

tee = io.StringIO()
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); tee.write(s + "\n")

# ------------------------------------------------------------------ runner
def fast_backtest(prices, weights, cost_bps=COST, freq=FREQ):
    """Vectorised equivalent of engine.backtest (asserted in G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(index=idx, columns=prices.columns).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1) - turn * cost_bps / 1e4, index=idx)

# ------------------------------------------------------------------ panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"   SMALL panel: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> "
        f"{len([c for c in keep if c != 'SPY'])} names + SPY")
    return px[keep]

def panels():
    """panel -> (prices, tradable constituents)."""
    u, b, s = load_universe(), load_universe(broad=True), small_panel()
    return {"U56": (u, list(u.columns)), "B136": (b, list(b.columns)),
            "SMALL439": (s, [c for c in s.columns if c != "SPY"])}

# ------------------------------------------------------------------- books
def const_forms(px, tradable, g=GROSS):
    """The six unconditional parents, all at the SAME gross.

    `tradable` is the panel's own constituent list: on U56 and B136 SPY IS a constituent
    (it is in universe.json / universe_broad.json and the record's books hold it), on
    SMALL439 it is a benchmark column only and is excluded."""
    names = list(tradable)
    P = px[names]
    priced = P.notna()
    ew = priced.astype(float)
    ew = g * ew.div(ew.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    s, above, vol20 = score(P, vol_scale=True)
    def topn(n):
        rk = s.rank(axis=1, ascending=False)
        return (rk <= n).astype(float) * (g / n)
    lv = vol20.rank(axis=1, ascending=True)
    lowvol20 = (lv <= 20).astype(float) * (g / 20)
    madg = ew.where(band_state(P, 0.03), 0.0)
    out = {"EWALL": ew, "TOP10": topn(10), "TOP20": topn(20), "MADG": madg,
           "LOWVOL20": lowvol20, "CASH": ew * 0.0}
    return {k: v.reindex(columns=names).fillna(0.0) for k, v in out.items()}, P

def states(px, P):
    """Market-level states decided at close t.  Expanding quantiles: no look-ahead."""
    spy = px["SPY"]
    out = {}
    out["TREND"] = (spy > spy.rolling(200).mean()).fillna(False)
    out["MOM12"] = ((spy / spy.shift(252) - 1) > 0).fillna(False)
    br = (P > P.rolling(200).mean()).sum(axis=1) / P.notna().sum(axis=1).replace(0, np.nan)
    ewret = P.pct_change().mean(axis=1)
    vol = ewret.rolling(20).std() * np.sqrt(252)
    for q in QS:
        bq = br.expanding(min_periods=252).quantile(q)
        vq = vol.expanding(min_periods=252).quantile(q)
        out[f"BREADTH{int(q*100)}"] = (br > bq).fillna(False)
        out[f"CALM{int(q*100)}"] = (vol < vq).fillna(False)
    return out

def windows(r, start):
    r = r.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = r.loc[OOS0:]; i = r.loc[:"2016-12-31"]
    mo, mi = metrics(o), metrics(i)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])

# =========================================================================== run
say("=" * 100)
say("IDEA 317 — conditional clauses vs their own two unconditional parents, matched gross 0.75")
say(f"           10 bps, weekly, next-day execution; OOS window {OOS0}..")
say("=" * 100)

PX = panels()

# ---- G1
g1px = PX["U56"][0]
g1w = rules_v2_weights(g1px)
a = engine_backtest(g1px, g1w, cost_bps=COST, freq=FREQ)["returns"]
b = fast_backtest(g1px, g1w)
d = float((a - b).abs().max())
say(f"G1 fast_backtest vs engine.backtest on RULES v2 / U56: max |diff| = {d:.3e}")
assert d < 1e-12, "G1 FAILED"

book_rows, par_rows = [], []
for pname, (px, trad) in PX.items():
    forms, P = const_forms(px, trad)
    ST = states(px, P)
    start = px.index[260]
    say(f"\n--- {pname}: {P.shape[1]} names, {px.index[0].date()}..{px.index[-1].date()}, "
        f"eval from {start.date()}; {len(forms)} parents x {len(ST)} states")
    ret = {}
    for f, w in forms.items():
        ret[f] = fast_backtest(px, w)
        book_rows.append(dict(panel=pname, book=f, kind="parent", pair="", state="", **windows(ret[f], start)))
    spy = px["SPY"].pct_change().fillna(0)
    for nm, r in [("SPY", spy), ("RULESv2", fast_backtest(px, rules_v2_weights(px))),
                  ("RULESv1", fast_backtest(px, rules_v1_weights(px)))]:
        ret[nm] = r
        book_rows.append(dict(panel=pname, book=nm, kind="reference", pair="", state="", **windows(r, start)))
    fnames = list(forms)
    for A in fnames:
        for B in fnames:
            if A == B: continue
            for sn, s in ST.items():
                m = s.reindex(px.index).fillna(False)
                w = forms[A].where(m, 0.0) + forms[B].where(~m, 0.0)
                r = fast_backtest(px, w)
                mw = windows(r, start)
                book_rows.append(dict(panel=pname, book=f"{A}|{B}@{sn}", kind="conditional",
                                      pair=f"{A}|{B}", state=sn, **mw))
                pa, pb = windows(ret[A], start), windows(ret[B], start)
                row = dict(panel=pname, pair=f"{A}|{B}", A=A, B=B, state=sn,
                           q=(int(sn[-2:]) / 100 if sn.startswith(("BREADTH", "CALM")) else np.nan),
                           on_frac=float(m.loc[start:].mean()))
                for win, ks in [("FULL", ("CAGR", "Sharpe", "MaxDD")),
                                ("IS", ("IS_CAGR", "IS_Sharpe", "IS_MaxDD")),
                                ("OOS", ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"))]:
                    for k, lab in zip(ks, ("CAGR", "Sharpe", "MaxDD")):
                        row[f"{win}_{lab}_C"] = mw[k]
                        row[f"{win}_{lab}_pmax"] = max(pa[k], pb[k])
                        row[f"{win}_{lab}_beats"] = bool(mw[k] > max(pa[k], pb[k]))
                    row[f"{win}_ALL3"] = bool(row[f"{win}_CAGR_beats"] and row[f"{win}_Sharpe_beats"]
                                              and row[f"{win}_MaxDD_beats"])
                row["H1_beats"] = bool(mw["H1"] > max(pa["H1"], pb["H1"]))
                row["H2_beats"] = bool(mw["H2"] > max(pa["H2"], pb["H2"]))
                par_rows.append(row)
books = pd.DataFrame(book_rows); par = pd.DataFrame(par_rows)

# ---------------------------------------------------------------- THE BAR
say("\n" + "=" * 100)
say("IDEA 48's BAR — a conditional book must beat BOTH its parents.  All grid points.")
say("=" * 100)
say(f"{len(par)} conditional books ({par.panel.nunique()} panels x {par.pair.nunique()} ordered pairs "
    f"x {par.state.nunique()} states)")
def block(d, lab):
    say(f"\n{lab}  (n={len(d)})")
    for win in ("FULL", "IS", "OOS"):
        cs = [f"{win}_{k}_beats" for k in ("CAGR", "Sharpe", "MaxDD")]
        say(f"   {win:4s}  CAGR {d[cs[0]].sum():4d}/{len(d)} = {d[cs[0]].mean():6.1%}   "
            f"Sharpe {d[cs[1]].sum():4d}/{len(d)} = {d[cs[1]].mean():6.1%}   "
            f"MaxDD {d[cs[2]].sum():4d}/{len(d)} = {d[cs[2]].mean():6.1%}   "
            f"ALL3 {d[f'{win}_ALL3'].sum():4d}/{len(d)} = {d[f'{win}_ALL3'].mean():6.1%}")
    say(f"   HALVES  H1 {d.H1_beats.sum():4d}/{len(d)} = {d.H1_beats.mean():6.1%}   "
        f"H2 {d.H2_beats.sum():4d}/{len(d)} = {d.H2_beats.mean():6.1%}   "
        f"BOTH {(d.H1_beats & d.H2_beats).sum():4d} = {(d.H1_beats & d.H2_beats).mean():6.1%}")
block(par, "ALL PANELS POOLED")
for p, d in par.groupby("panel"): block(d, f"PANEL {p}")
say("\nBY STATE FAMILY (reporting axis, never selected on):")
for s, d in par.groupby("state"):
    say(f"   {s:10s} n={len(d):3d}  ON {d.on_frac.mean():5.1%}  FULL CAGR {d.FULL_CAGR_beats.mean():6.1%}  "
        f"Sharpe {d.FULL_Sharpe_beats.mean():6.1%}  MaxDD {d.FULL_MaxDD_beats.mean():6.1%}  "
        f"ALL3 {d.FULL_ALL3.mean():6.1%}  OOS ALL3 {d.OOS_ALL3.mean():6.1%}")
say("\nBY q, THE ONE SWEPT PARAMETER (all points; 0.50 is the point value):")
for q, d in par[par.q.notna()].groupby("q"):
    say(f"   q={q:.2f}  n={len(d):3d}  FULL ALL3 {d.FULL_ALL3.mean():6.1%}  Sharpe {d.FULL_Sharpe_beats.mean():6.1%}  "
        f"MaxDD {d.FULL_MaxDD_beats.mean():6.1%}  OOS ALL3 {d.OOS_ALL3.mean():6.1%}")
say("   (states with no q: TREND, MOM12) "
    f"n={len(par[par.q.isna()])}  FULL ALL3 {par[par.q.isna()].FULL_ALL3.mean():6.1%}  "
    f"OOS ALL3 {par[par.q.isna()].OOS_ALL3.mean():6.1%}")
say("\nBY PAIR — the ten pairs with the highest FULL ALL3 rate:")
pv = par.groupby("pair").agg(n=("FULL_ALL3", "size"), full_all3=("FULL_ALL3", "mean"),
                             oos_all3=("OOS_ALL3", "mean"), sharpe=("FULL_Sharpe_beats", "mean"),
                             maxdd=("FULL_MaxDD_beats", "mean")).sort_values("full_all3", ascending=False)
say(pv.head(10).to_string(float_format=lambda x: f"{x:.3f}"))
say("\nTRANSPORT: of the FULL-sample ALL3 passers, how many also pass ALL3 out of sample?")
fp = par[par.FULL_ALL3]
say(f"   FULL ALL3 passers {len(fp)};  of those OOS ALL3 {int(fp.OOS_ALL3.sum())} "
    f"({fp.OOS_ALL3.mean() if len(fp) else float('nan'):.1%});  IS ALL3 passers {int(par.IS_ALL3.sum())}, "
    f"of those OOS ALL3 {int(par[par.IS_ALL3].OOS_ALL3.sum())} "
    f"({par[par.IS_ALL3].OOS_ALL3.mean() if par.IS_ALL3.any() else float('nan'):.1%})")

# ------------------------------------------------------------- RULE 8
say("\n" + "=" * 100)
say("RULE 8 — (pair, state) chosen on IS 2010-2016 ONLY, OOS 2017-2026 read ONCE")
say("=" * 100)
wf_rows = []
for pname, d in par.groupby("panel"):
    cand = d[d.IS_ALL3]
    how = "IS ALL3 passers"
    if cand.empty:
        cand = d[d.IS_Sharpe_beats]; how = "IS Sharpe-bar passers (no IS ALL3 passer existed)"
    if cand.empty:
        cand = d; how = "ALL conditional books (no IS bar passer of any kind existed)"
    pick = cand.sort_values("IS_Sharpe_C", ascending=False).iloc[0]
    bk = books[(books.panel == pname) & (books.book == f"{pick.pair}@{pick.state}")].iloc[0]
    ref = {r.book: r for _, r in books[(books.panel == pname) & (books.kind == "reference")].iterrows()}
    v2, spy = ref["RULESv2"], ref["SPY"]
    p4a = (bk.H1 > v2.H1) and (bk.H2 > v2.H2) and (bk.MaxDD >= v2.MaxDD)
    p4b = ((bk.H1 > spy.H1) and (bk.H2 > spy.H2) and (bk.OOS_Sharpe > spy.OOS_Sharpe)
           and (bk.MaxDD >= 0.60 * spy.MaxDD) and (bk.CAGR >= 0.70 * spy.CAGR))
    say(f"\n{pname}: selector = {how}; IS pick = {pick.pair}@{pick.state} "
        f"(IS Sharpe {pick.IS_Sharpe_C:.3f}, IS ALL3 {bool(pick.IS_ALL3)})")
    say(f"   FULL CAGR {bk.CAGR:7.2%}  Sharpe {bk.Sharpe:6.3f}  MaxDD {bk.MaxDD:7.2%}  "
        f"H1/H2 {bk.H1:.3f}/{bk.H2:.3f}  (state ON {pick.on_frac:.1%} of days)")
    say(f"   IS   CAGR {bk.IS_CAGR:7.2%}  Sharpe {bk.IS_Sharpe:6.3f}  MaxDD {bk.IS_MaxDD:7.2%}")
    say(f"   OOS  CAGR {bk.OOS_CAGR:7.2%}  Sharpe {bk.OOS_Sharpe:6.3f}  MaxDD {bk.OOS_MaxDD:7.2%}   "
        f"(pick's OOS ALL3 vs its own parents: {bool(pick.OOS_ALL3)})")
    for nm in ("RULESv2", "RULESv1", "SPY"):
        r = ref[nm]
        say(f"   {nm:8s} OOS CAGR {r.OOS_CAGR:7.2%}  Sharpe {r.OOS_Sharpe:6.3f}  MaxDD {r.OOS_MaxDD:7.2%} | "
            f"FULL CAGR {r.CAGR:7.2%} Sharpe {r.Sharpe:6.3f} MaxDD {r.MaxDD:7.2%} H1/H2 {r.H1:.3f}/{r.H2:.3f}")
    say(f"   KEEP PATHS on the IS pick — 4a {p4a}  |  4b {p4b}  "
        f"(H1 {bk.H1:.3f}>{spy.H1:.3f}={bk.H1>spy.H1}, H2 {bk.H2:.3f}>{spy.H2:.3f}={bk.H2>spy.H2}, "
        f"OOS {bk.OOS_Sharpe:.3f}>{spy.OOS_Sharpe:.3f}={bk.OOS_Sharpe>spy.OOS_Sharpe}, "
        f"DD {bk.MaxDD:.3f} vs {0.6*spy.MaxDD:.3f}={bk.MaxDD>=0.6*spy.MaxDD}, "
        f"CAGR {bk.CAGR:.3f} vs {0.7*spy.CAGR:.3f}={bk.CAGR>=0.7*spy.CAGR})")
    wf_rows.append(dict(panel=pname, selector=how, pick=f"{pick.pair}@{pick.state}",
                        IS_ALL3=bool(pick.IS_ALL3), OOS_ALL3=bool(pick.OOS_ALL3),
                        IS_CAGR=bk.IS_CAGR, IS_Sharpe=bk.IS_Sharpe, IS_MaxDD=bk.IS_MaxDD,
                        OOS_CAGR=bk.OOS_CAGR, OOS_Sharpe=bk.OOS_Sharpe, OOS_MaxDD=bk.OOS_MaxDD,
                        FULL_CAGR=bk.CAGR, FULL_Sharpe=bk.Sharpe, FULL_MaxDD=bk.MaxDD, H1=bk.H1, H2=bk.H2,
                        spy_OOS_Sharpe=spy.OOS_Sharpe, spy_OOS_CAGR=spy.OOS_CAGR, spy_OOS_MaxDD=spy.OOS_MaxDD,
                        v2_OOS_Sharpe=v2.OOS_Sharpe, v2_OOS_CAGR=v2.OOS_CAGR, v2_OOS_MaxDD=v2.OOS_MaxDD,
                        pass4a=p4a, pass4b=p4b))

# --------------------------------------------------- KEEP paths, whole menu
say("\nKEEP paths over the WHOLE menu (all 720 conditional books + 18 parents), for the record:")
kp = []
for pname, d in books.groupby("panel"):
    ref = {r.book: r for _, r in d[d.kind == "reference"].iterrows()}
    v2, spy = ref["RULESv2"], ref["SPY"]
    dd = d[d.kind.isin(["conditional", "parent"])]
    a4 = (dd.H1 > v2.H1) & (dd.H2 > v2.H2) & (dd.MaxDD >= v2.MaxDD)
    b4 = ((dd.H1 > spy.H1) & (dd.H2 > spy.H2) & (dd.OOS_Sharpe > spy.OOS_Sharpe)
          & (dd.MaxDD >= 0.60 * spy.MaxDD) & (dd.CAGR >= 0.70 * spy.CAGR))
    say(f"   {pname:9s} 4a {int(a4.sum()):3d}/{len(dd)}   4b {int(b4.sum()):3d}/{len(dd)}   "
        f"BOTH {int((a4&b4).sum()):3d}/{len(dd)}")
    kp.append(dict(panel=pname, n=len(dd), pass4a=int(a4.sum()), pass4b=int(b4.sum()), both=int((a4 & b4).sum())))

books.to_csv(STEM.with_suffix(".books.csv"), index=False)
par.to_csv(STEM.with_suffix(".parents.csv"), index=False)
pd.DataFrame(kp).to_csv(STEM.with_suffix(".grid.csv"), index=False)
pd.DataFrame(wf_rows).to_csv(STEM.with_suffix(".walkforward.csv"), index=False)
STEM.with_suffix(".console.txt").write_text(tee.getvalue())
print("wrote", STEM.name + ".{books,parents,grid,walkforward}.csv/.console.txt")
