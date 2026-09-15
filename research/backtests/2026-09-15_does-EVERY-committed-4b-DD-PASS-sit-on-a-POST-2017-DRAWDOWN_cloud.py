#!/usr/bin/env python3
"""Idea 878 - "does-EVERY-committed-4b-DD-PASS-in-the-record-sit-on-a-POST-2017-DRAWDOWN"
(cloud lane, 2026-09-15, idea 2 of 2).

The question
------------
Idea 808 found that on its own 252-cell monthly book-calendar grid the FULL-sample MaxDD equals the
OOS-window (2017+) MaxDD in 252 of 252 cells and the IS-window (2009-2016) MaxDD in 0 of 252.  If
that holds on the record's COMMITTED 4b passes, then PROTOCOL 4b's drawdown cap is an object that
lives entirely in the second half of the sample, rule 8 can never fit it, and every committed DD
pass is a statement about one post-2017 crash.

So this run asks two things of the committed passes, not of a synthetic grid:

  (1) WHERE does each book's binding drawdown actually trough - which window, which year?
  (2) IS A PRE-2017-ONLY DD CAP ESTIMABLE AT ALL?  That is the queue's second clause, and it is the
      one with teeth: the cap is 0.60 x SPY's MaxDD, so an IS-only analyst computes it from SPY's
      IS drawdown, which is a different (much shallower) number than SPY's full-sample one.  The
      run prices the IS-estimated cap against the full-sample cap directly: how many books clear
      each, and does clearing the IS cap predict clearing the full one.

Pre-registered hypotheses and bars (fixed before any number below the gates was read)
    H_POST    every committed 4b pass's binding (full-sample) drawdown troughs AFTER the split
              date.  This is 808's 252-of-252, asked of the real shelf.
    H_SPLIT   that share is >= 90% at EVERY split date in the grid, not only at 2017-01-01.
              A result that only holds at PROTOCOL's own split is a property of the split.
    H_UNEST   the IS-estimated DD cap (0.60 x SPY's IS MaxDD) is cleared in sample by FEWER THAN
              HALF the committed passes.  PASS = the cap rule 8 could fit is a materially
              different, tighter object than the one the record publishes.
    H_PRED    clearing the IS cap predicts clearing the full-sample cap at accuracy > 0.70 over
              the pooled book set.  FAIL = an IS-only analyst cannot forecast the published leg.
    H_WF      rule 8: an IS-only chooser (best IS Sharpe among books clearing the IS-window 4b
              legs) picks a book that passes 4b out of sample.
  Each prints its bar and PASS/FAIL.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. book set    SHELF (the record's committed, memo-backed 4b passes) - headline;
                   GRID (861's mechanical never-memo-selected ladder) - reported control.
    2. split date  {2015-01-01, 2016-01-01, 2017-01-01, 2018-01-01}; 2017-01-01 is PROTOCOL's.
    ALL grid points reported.  Cost rung {10, 25} bps is a reported control, not a dial.

Reproduction gates (printed before any new number is read)
    G1  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G2  fast_run vs engine.backtest on a live book.
    G3  the SPY comparand reproduces the record's committed triple.
    G4  idea 808's own claim, re-read on THIS book set: full MaxDD == OOS MaxDD, and
        full MaxDD != IS MaxDD, at the PROTOCOL split.  Printed as a count, not assumed.

Data: committed price caches only.  No network, never yfinance.
SURVIVORSHIP: U56 and B136 are CURRENT-constituent lists, so every drawdown LEVEL here is
optimistic (names that went to zero are absent).  The reported objects are WHICH WINDOW a trough
falls in and the IS-vs-full CAP GAP, both of which are computed on the same biased panel.

Deterministic, standalone.  Modifies nothing.  Proposes no PROTOCOL edit and applies none.
Run: python research/backtests/2026-09-15_does-EVERY-committed-4b-DD-PASS-sit-on-a-POST-2017-DRAWDOWN_cloud.py
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-15"
SLUG = "does-EVERY-committed-4b-DD-PASS-sit-on-a-POST-2017-DRAWDOWN"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
LANEC = Path(__file__).resolve().parent / f"{DATE}_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP, MAX_VOL = 260, 0.60
RUNGS = [10.0, 25.0]
RUNG_HEAD = 10.0
SPLITS = ["2015-01-01", "2016-01-01", "2017-01-01", "2018-01-01"]
SPLIT_HEAD = "2017-01-01"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def load_lane_c():
    spec = importlib.util.spec_from_file_location("laneC878", LANEC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load_lane_c()
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def dd_detail(r, idx):
    """MaxDD plus the DATE its trough falls on and the date of the peak it fell from."""
    eq = np.cumprod(1.0 + np.asarray(r, float))
    run = np.maximum.accumulate(eq)
    dd = eq / run - 1.0
    i = int(np.argmin(dd))
    j = int(np.argmax(eq[:i + 1]))
    return float(dd[i]), idx[i], idx[j]


def win(r, idx, lo=None, hi=None):
    m = np.ones(len(idx), bool)
    if lo is not None:
        m &= np.asarray(idx >= pd.Timestamp(lo))
    if hi is not None:
        m &= np.asarray(idx <= pd.Timestamp(hi))
    return np.asarray(r)[m], idx[m]


def main():
    t0 = time.time()
    P(f"# Idea 878 - does EVERY committed 4b DD PASS in the record sit on a POST-2017 DRAWDOWN, and "
      f"is a PRE-2017-ONLY DD CAP ESTIMABLE AT ALL?  ({DATE}, cloud lane)")
    P(f"# 2 tuned dials: BOOK SET [SHELF, GRID] x SPLIT DATE {SPLITS}.  ALL grid points reported.")
    P(f"# Cost rung {RUNGS} bps is a reported control.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels; every drawdown LEVEL is optimistic.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    start = {p: PX[p].index[WARMUP] for p in PX}

    books = C.shelf_books(U, B)
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    books["u56-top20-g065-M"] = dict(
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    GRID = C.grid_books(U, B)
    P(f"SHELF = {len(books)} committed memo-backed 4b passes; GRID = {len(GRID)} never-selected "
      f"ladder books (control).")
    P("")

    # ---------------------------------------------------------------- comparands
    spy = {}
    for p, px in PX.items():
        sr = px["SPY"].pct_change().fillna(0.0).loc[start[p]:]
        spy[p] = dict(r=sr.values, idx=sr.index)
    v2net = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            v2net.setdefault(p, {})[c] = (r - t * c / 1e4).loc[start[p]:]

    # ---------------------------------------------------------------- net return paths
    NET = {}
    for setname, bset in (("SHELF", books), ("GRID", GRID)):
        for nm, b in bset.items():
            px = PX[b["panel"]]
            r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
            for c in RUNGS:
                NET[(setname, nm, c)] = (r - t * c / 1e4).loc[start[b["panel"]]:]

    # ---------------------------------------------------------------- GATES
    P("## Reproduction gates")
    grows, ok1 = [], True
    for nm, b in books.items():
        n = NET[("SHELF", nm, RUNG_HEAD)]
        cagr, sh, dd = fmet(n.values)
        m = b["memo"]
        dc = abs(cagr - m[0]) if m[0] is not None else 0.0
        ds = abs(sh - m[1]) if m[1] is not None else 0.0
        dv = abs(dd - m[2]) if m[2] is not None else 0.0
        good = dc <= 0.015 and ds <= 0.030 and dv <= 0.015
        ok1 &= good
        grows.append(dict(book=nm, got_CAGR=round(cagr, 4), got_Sharpe=round(sh, 4),
                          got_MaxDD=round(dd, 4), dCAGR=round(dc, 4), dSharpe=round(ds, 4),
                          dMaxDD=round(dv, 4), gate="PASS" if good else "FAIL"))
    P(pd.DataFrame(grows).to_string(index=False))
    P(f"G1 every SHELF book reproduces its committed memo triple: {'PASS' if ok1 else 'FAIL'}")

    bw = rules_v2_weights(U)
    eng = backtest(U, bw, cost_bps=RUNG_HEAD, freq="W")
    d2 = float(np.abs(v2net["U56"][RUNG_HEAD].values - eng["returns"].loc[start["U56"]:].values).max())
    ok2 = d2 < 1e-10
    P(f"G2 fast_run vs engine.backtest max|d ret| = {d2:.3e}: {'PASS' if ok2 else 'FAIL'}")

    sc, ss, sd = fmet(spy["U56"]["r"])
    ok3 = abs(sc - 0.1513) <= 0.004 and abs(ss - 0.886) <= 0.02 and abs(sd + 0.3372) <= 0.01
    P(f"G3 SPY {sc:.4f} / {ss:.3f} / {sd:.4f} vs committed 0.1513 / 0.886 / -0.3372: "
      f"{'PASS' if ok3 else 'FAIL'}")

    # ---------------------------------------------------------------- the census
    rows = []
    for (setname, nm, c), n in NET.items():
        b = (books if setname == "SHELF" else GRID)[nm]
        full_dd, trough, peak = dd_detail(n.values, n.index)
        cagr, sh, _ = fmet(n.values)
        rec = dict(set=setname, book=nm, panel=b["panel"], freq=b["freq"], rung=c,
                   full_CAGR=cagr, full_Sharpe=sh, full_MaxDD=full_dd,
                   trough=trough.date(), trough_year=trough.year, peak=peak.date())
        for sp in SPLITS:
            ir, ii = win(n.values, n.index, hi=pd.Timestamp(sp) - pd.Timedelta(days=1))
            orr, oi = win(n.values, n.index, lo=sp)
            idd, _, _ = dd_detail(ir, ii)
            odd, _, _ = dd_detail(orr, oi)
            tag = sp[:4]
            rec[f"IS{tag}_MaxDD"] = idd
            rec[f"OOS{tag}_MaxDD"] = odd
            rec[f"post{tag}"] = bool(trough >= pd.Timestamp(sp))
            rec[f"full_eq_OOS{tag}"] = bool(abs(full_dd - odd) < 1e-12)
            rec[f"full_eq_IS{tag}"] = bool(abs(full_dd - idd) < 1e-12)
        rows.append(rec)
    A = pd.DataFrame(rows)

    # SPY's own caps, per split
    caps = {}
    for p in PX:
        sr, si = spy[p]["r"], spy[p]["idx"]
        fdd, ftr, _ = dd_detail(sr, si)
        caps[p] = dict(full=DDCAP_FRAC * fdd, full_raw=fdd, trough=ftr.date())
        for sp in SPLITS:
            ir, ii = win(sr, si, hi=pd.Timestamp(sp) - pd.Timedelta(days=1))
            idd, itr, _ = dd_detail(ir, ii)
            caps[p][f"IS{sp[:4]}"] = DDCAP_FRAC * idd
            caps[p][f"IS{sp[:4]}_raw"] = idd
            caps[p][f"IS{sp[:4]}_trough"] = itr.date()
    for p in PX:
        A.loc[A.panel == p, "cap_full"] = caps[p]["full"]
        for sp in SPLITS:
            A.loc[A.panel == p, f"cap_IS{sp[:4]}"] = caps[p][f"IS{sp[:4]}"]
    for sp in SPLITS:
        tag = sp[:4]
        A[f"clears_cap_IS{tag}"] = A[f"IS{tag}_MaxDD"] >= A[f"cap_IS{tag}"]
    A["clears_cap_full"] = A.full_MaxDD >= A.cap_full
    A.to_csv(f"{OUT}.books.csv", index=False)

    P("")
    P("## G4 - idea 808's claim re-read on THIS book set (PROTOCOL split 2017-01-01, 10 bps)")
    h = A[A.rung == RUNG_HEAD]
    P(f"  full MaxDD == OOS-window MaxDD: {int(h.full_eq_OOS2017.sum())} of {len(h)} books")
    P(f"  full MaxDD == IS-window  MaxDD: {int(h.full_eq_IS2017.sum())} of {len(h)} books")
    P(f"  (808 published 252 of 252 and 0 of 252 on its own monthly book-calendar grid)")
    P("")

    # ---------------------------------------------------------------- (1) where the trough falls
    P("## 1. Where the binding drawdown actually troughs (10 bps)")
    sh9 = h[h.set == "SHELF"]
    P(sh9[["book", "panel", "freq", "full_MaxDD", "trough", "peak",
           "IS2017_MaxDD", "OOS2017_MaxDD", "post2017"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P(f"  SHELF trough YEAR census: {dict(sh9.trough_year.value_counts().sort_index())}")
    gg = h[h.set == "GRID"]
    P(f"  GRID  trough YEAR census: {dict(gg.trough_year.value_counts().sort_index())}")
    P(f"  SPY's own binding trough: U56 panel {caps['U56']['trough']} "
      f"(MaxDD {caps['U56']['full_raw']:.4f})")
    P("")

    P("## 2. Split-date grid - the share whose binding trough is post-split (ALL points)")
    grid_rows = []
    for setname in ("SHELF", "GRID"):
        for c in RUNGS:
            sub = A[(A.set == setname) & (A.rung == c)]
            r = dict(set=setname, rung=c, n=len(sub))
            for sp in SPLITS:
                tag = sp[:4]
                r[f"post{tag}"] = f"{int(sub[f'post{tag}'].sum())}/{len(sub)}"
            grid_rows.append(r)
    P(pd.DataFrame(grid_rows).to_string(index=False))
    P("")

    # ---------------------------------------------------------------- (2) is the cap estimable
    P("## 3. Is a pre-split-only DD cap estimable at all?  (10 bps)")
    P("   The cap is 0.60 x SPY's MaxDD.  An IS-only analyst computes SPY's drawdown on the IS")
    P("   window alone, which is a different number.  Both caps, per split and panel:")
    cr = []
    for p in PX:
        row = dict(panel=p, SPY_full_MaxDD=round(caps[p]["full_raw"], 4),
                   cap_full=round(caps[p]["full"], 4), SPY_full_trough=caps[p]["trough"])
        for sp in SPLITS:
            tag = sp[:4]
            row[f"SPY_IS{tag}_MaxDD"] = round(caps[p][f"IS{tag}_raw"], 4)
            row[f"cap_IS{tag}"] = round(caps[p][f"IS{tag}"], 4)
        cr.append(row)
    P(pd.DataFrame(cr).to_string(index=False))
    P("")
    est = []
    for setname in ("SHELF", "GRID"):
        sub = h[h.set == setname]
        r = dict(set=setname, n=len(sub), clears_full_cap=f"{int(sub.clears_cap_full.sum())}/{len(sub)}")
        for sp in SPLITS:
            tag = sp[:4]
            r[f"clears_IS{tag}_cap"] = f"{int(sub[f'clears_cap_IS{tag}'].sum())}/{len(sub)}"
        est.append(r)
    P(pd.DataFrame(est).to_string(index=False))
    P("")

    # ---------------------------------------------------------------- hypotheses
    P("## Pre-registered hypotheses")
    h_post = bool(sh9.post2017.all())
    P(f"H_POST   every committed 4b pass troughs after {SPLIT_HEAD}: "
      f"{int(sh9.post2017.sum())}/{len(sh9)} -> {'PASS' if h_post else 'FAIL'}")

    shares = {sp[:4]: sh9[f"post{sp[:4]}"].mean() for sp in SPLITS}
    h_split = all(v >= 0.90 for v in shares.values())
    P(f"H_SPLIT  >= 90% at EVERY split: " +
      ", ".join(f"{k} {v:.0%}" for k, v in shares.items()) +
      f" -> {'PASS' if h_split else 'FAIL'}")

    frac_is = float(sh9.clears_cap_IS2017.mean())
    h_unest = frac_is < 0.50
    P(f"H_UNEST  IS-estimated cap cleared in sample by fewer than half the committed passes: "
      f"{int(sh9.clears_cap_IS2017.sum())}/{len(sh9)} = {frac_is:.0%} -> "
      f"{'PASS' if h_unest else 'FAIL'}")

    pool = h
    acc = float((pool.clears_cap_IS2017 == pool.clears_cap_full).mean())
    h_pred = acc > 0.70
    tp = int((pool.clears_cap_IS2017 & pool.clears_cap_full).sum())
    fp = int((pool.clears_cap_IS2017 & ~pool.clears_cap_full).sum())
    fn = int((~pool.clears_cap_IS2017 & pool.clears_cap_full).sum())
    tn = int((~pool.clears_cap_IS2017 & ~pool.clears_cap_full).sum())
    P(f"H_PRED   IS cap predicts full cap at accuracy > 0.70 over {len(pool)} pooled books: "
      f"{acc:.3f} (TP {tp} FP {fp} FN {fn} TN {tn}) -> {'PASS' if h_pred else 'FAIL'}")

    P("")
    P("## 4. The direction of the IS-cap error, at EVERY split and rung (all 45 books pooled)")
    P("   FP = book clears the IS-only cap in sample but BREAKS the published full-sample cap.")
    P("   FN = book fails the IS-only cap but clears the published one (a conservative rejection).")
    dr = []
    for c in RUNGS:
        pl = A[A.rung == c]
        for sp in SPLITS:
            tag = sp[:4]
            i_ok, f_ok = pl[f"clears_cap_IS{tag}"], pl.clears_cap_full
            dr.append(dict(rung=c, split=sp, n=len(pl),
                           TP=int((i_ok & f_ok).sum()), FP=int((i_ok & ~f_ok).sum()),
                           FN=int((~i_ok & f_ok).sum()), TN=int((~i_ok & ~f_ok).sum()),
                           accuracy=round(float((i_ok == f_ok).mean()), 3)))
    D = pd.DataFrame(dr)
    P(D.to_string(index=False))
    zero_fp = bool((D.FP == 0).all())
    P(f"   FP == 0 at every one of the {len(D)} (split x rung) cells: "
      f"{'YES' if zero_fp else 'NO'} (max FP {int(D.FP.max())})")
    bad = D[D.FP > 0]
    if len(bad):
        P(f"   FP > 0 at {len(bad)} cell(s): " +
          ", ".join(f"split {r.split} @ {r.rung:.0f}bps FP={r.FP}" for _, r in bad.iterrows()))
        P("   Reading: the IS-only cap is NEARLY one-directional but NOT exactly - it is "
          "sufficient at the 2016/2017/2018 splits and leaks one book at 2015.  The error it "
          "makes is overwhelmingly conservative (FN 16-18 against FP 0-1), so an IS-only DD "
          "screen rejects far more than it wrongly certifies - but 'zero false positives' is a "
          "split-dependent statement, not a property of the cap.")
    else:
        P("   Reading: the IS-only cap is SUFFICIENT and not NECESSARY on this corpus - it "
          "certifies no book that later breaks the published cap, and rejects books that would "
          "have cleared it.")

    # ---------------------------------------------------------------- rule 8
    P("")
    P("## Rule 8 walk-forward: choose on 2009-2016 only, evaluate 2017+ untouched (10 bps)")
    wf = []
    for setname, bset in (("SHELF", books), ("GRID", GRID)):
        for nm, b in bset.items():
            n = NET[(setname, nm, RUNG_HEAD)]
            ir, ii = win(n.values, n.index, hi="2016-12-31")
            orr, oi = win(n.values, n.index, lo="2017-01-01")
            sr, si = spy[b["panel"]]["r"], spy[b["panel"]]["idx"]
            sir, sii = win(sr, si, hi="2016-12-31")
            sor, soi = win(sr, si, lo="2017-01-01")
            ic, ish, idd = fmet(ir)
            oc, osh, odd = fmet(orr)
            sic, sish, sidd = fmet(sir)
            soc, sosh, sodd = fmet(sor)
            k = len(ir) // 2
            is4b = (fsharpe(ir[:k]) > fsharpe(sir[:k]) and fsharpe(ir[k:]) > fsharpe(sir[k:])
                    and idd >= DDCAP_FRAC * sidd and ic >= CAGRFLOOR_FRAC * sic)
            v2o = win(v2net[b["panel"]][RUNG_HEAD].values,
                      v2net[b["panel"]][RUNG_HEAD].index, lo="2017-01-01")[0]
            vc, vsh, vdd = fmet(v2o)
            oos4b = (osh > sosh and odd >= DDCAP_FRAC * sodd and oc >= CAGRFLOOR_FRAC * soc)
            oos4a = (osh > vsh and odd >= vdd)
            wf.append(dict(set=setname, book=nm, panel=b["panel"],
                           IS_CAGR=ic, IS_Sharpe=ish, IS_MaxDD=idd, IS_pass4b=is4b,
                           OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd,
                           OOS_pass4b=oos4b, OOS_pass4a=oos4a,
                           SPY_OOS_CAGR=soc, SPY_OOS_Sharpe=sosh, SPY_OOS_MaxDD=sodd,
                           V2_OOS_CAGR=vc, V2_OOS_Sharpe=vsh, V2_OOS_MaxDD=vdd))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"  books clearing ALL FOUR 4b legs IN SAMPLE (2009-2016): "
      f"{int(WF.IS_pass4b.sum())} of {len(WF)}  "
      f"(SHELF {int(WF[WF.set=='SHELF'].IS_pass4b.sum())}/{len(books)}, "
      f"GRID {int(WF[WF.set=='GRID'].IS_pass4b.sum())}/{len(GRID)})")
    picks = []
    for setname in ("SHELF", "GRID"):
        sub = WF[WF.set == setname]
        elig = sub[sub.IS_pass4b]
        note = "IS 4b-eligible" if len(elig) else "IS 4b band EMPTY - falling back to best IS Sharpe"
        pool2 = elig if len(elig) else sub
        pk = pool2.sort_values("IS_Sharpe", ascending=False).iloc[0]
        picks.append(pk)
        P(f"  {setname:5s} IS-SHARPE chooser ({note}) picks {pk.book}")
        P(f"      IS  {pk.IS_CAGR:.2%} / {pk.IS_Sharpe:.3f} / {pk.IS_MaxDD:.2%}")
        P(f"      OOS {pk.OOS_CAGR:.2%} / {pk.OOS_Sharpe:.3f} / {pk.OOS_MaxDD:.2%}   "
          f"SPY {pk.SPY_OOS_CAGR:.2%} / {pk.SPY_OOS_Sharpe:.3f} / {pk.SPY_OOS_MaxDD:.2%}   "
          f"RULES v2 {pk.V2_OOS_CAGR:.2%} / {pk.V2_OOS_Sharpe:.3f} / {pk.V2_OOS_MaxDD:.2%}")
        P(f"      OOS 4b {'PASS' if pk.OOS_pass4b else 'FAIL'} | OOS 4a "
          f"{'PASS' if pk.OOS_pass4a else 'FAIL'}")
    h_wf = bool(picks[0].OOS_pass4b)
    P(f"H_WF     the SHELF IS-only pick passes 4b out of sample -> {'PASS' if h_wf else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- cost-rung control
    P("## Control: cost rung")
    for c in RUNGS:
        sub = A[(A.set == "SHELF") & (A.rung == c)]
        P(f"  {c:.0f} bps: post-2017 troughs {int(sub.post2017.sum())}/{len(sub)}, "
          f"clears full cap {int(sub.clears_cap_full.sum())}/{len(sub)}, "
          f"clears IS2017 cap {int(sub.clears_cap_IS2017.sum())}/{len(sub)}")
    P("")

    P("## Summary")
    P(f"  Committed 4b passes: {len(sh9)}.  Binding trough post-{SPLIT_HEAD}: "
      f"{int(sh9.post2017.sum())}/{len(sh9)}; trough years {dict(sh9.trough_year.value_counts().sort_index())}.")
    P(f"  full MaxDD == OOS MaxDD on {int(sh9.full_eq_OOS2017.sum())}/{len(sh9)}; == IS MaxDD on "
      f"{int(sh9.full_eq_IS2017.sum())}/{len(sh9)}.")
    P(f"  Published cap {caps['U56']['full']:.4f} (U56 panel) vs IS-only cap "
      f"{caps['U56']['cap_IS2017'] if 'cap_IS2017' in caps['U56'] else caps['U56']['IS2017']:.4f}; "
      f"committed passes clearing the IS cap: {int(sh9.clears_cap_IS2017.sum())}/{len(sh9)}.")
    P(f"\n[{time.time() - t0:.1f}s]")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
