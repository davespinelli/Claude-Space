#!/usr/bin/env python3
"""Idea 650 — is the CORRELATION CUT a pre-registrable SLEEVE-ADMISSION test?   (lane C, 2026-09-10)

QUEUE 650: "idea 618 found the width law's intercept is a sleeve statistic (R^2 0.731 vs 0.184)
whose carrier is CO-MOVEMENT, not drawdown: `sl_corr > 0.5` classifies inert-vs-not 40/40
(AUC 1.000) while the sleeve's own MaxDD reads AUC 0.312.  But the cut was read on the same 10
sleeves that produced it.  Fit the threshold on the IS window alone and test it on sleeve sets the
record has never run (sector ETFs, IG/HY credit, commodity singles, 2- and 3-asset mixes),
reporting whether it admits and rejects out of sample or only in it.  Max 2 params (sleeve set,
threshold)."

WHAT IS ACTUALLY BEING TESTED
  A classifier is only a *test* if it was fittable before the thing it classifies was seen.  618's
  cut fails that twice over: it was read at 0.5 on the SAME ten sleeves whose inertness defined the
  classes, and on the FULL sample, whose second half is the window rule 8 reserves.  This run
  removes both by construction and then asks the only question that matters for a pre-registered
  admission rule — does it hold on sleeves nobody has run, in a window nobody has read?

  H1 (fit)     The cut is fittable on the IS window alone: on the ten TRAIN sleeves, using
               `sl_corr` measured on 2009-2016 and inertness judged on 2009-2016 only, some
               threshold separates the classes.  Falsifiable: sweep the threshold on a 41-point
               ladder and report train-IS accuracy at EVERY point.  If no cut reaches 40/40, the
               published number was a full-sample artefact before any new sleeve is priced.
  H2 (window)  The IS-fitted cut survives the WINDOW change on the sleeves it was fitted on:
               apply tau* to the same ten sleeves and score against 2017-2026 inertness.
  H3 (THE ASK) The IS-fitted cut survives the SLEEVE change: apply the same tau* to 30 sleeves the
               record has never run and score against their OOS inertness.  Reported as a 2x2
               confusion matrix, not an accuracy alone, because a set that is 90% one class can be
               "90% accurate" while never rejecting anything — the queue asks whether it ADMITS
               AND REJECTS, so both cells are reported and a balanced accuracy is printed beside
               the raw one.  AUC of the continuous predictor is reported against 618's own foil
               (the sleeve's standalone MaxDD, which read 0.312 there).
  H4 (KEEP)    Both PROTOCOL 4 paths on every arm-row, and PROTOCOL 8 with (sleeve, f) chosen on
               2009-2016 alone — including two selectors that differ ONLY in whether the IS-fitted
               admission cut is applied.  This is the leg that prices the rule in Sharpe rather
               than in accuracy: a cut can classify perfectly and still move no capital.

AXES AND WHAT IS SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
  The queue names the two tuned parameters and both are swept in full with every point reported:
    P1 SLEEVE SET : 40 sleeves = 618's 10 TRAIN sleeves + 30 TEST sleeves pre-registered by the
                    rule below.  Every sleeve is reported, none is dropped after the fact.
    P2 THRESHOLD  : tau on a uniform 41-point ladder -1.00..1.00 step 0.05; accuracy at every
                    point is printed for train-IS, train-OOS, test-IS and test-OOS.  The ONE
                    value carried into H3 and rule 8 is fitted on TRAIN x IS only.
  Everything else is a REPORTED axis and is never selected on: 2 panels, 2 books, idea 137's
  8-point lambda ladder, 11 f points, 6 cost rungs.

PRE-REGISTRATION OF THE TEST SLEEVE SET (fixed before any label is read)
  SECTOR    every member of universe.json's own `sectors` group with a full 2009 price history
            (XLRE 2015-10 and XLC 2018-06 fail it and are EXCLUDED and named, not silently
            dropped): XLK XLF XLV XLE XLI XLY XLP XLU XLB SMH XBI KRE ITB GDX.
  CREDIT    the three bond sleeves 618 never ran alone: LQD (IG), HYG (HY), TIP.
  COMMOD    the four commodity singles 618 never ran: SLV USO UNG DBC.
  MIX2/MIX3 five 2-asset and four 3-asset mixes spanning the corr range end to end.
  Construction is 618's verbatim (momentum vote x risk parity), so a single-name sleeve is that
  name on its own vote — the same construction, not a different one.

GATES (run before any new number is read)
  G1 the vectorised runner vs `engine.backtest` on the evaluated slice, returns AND turnover.
  G2 the rung identity r(c) = r(0) - turnover*c/1e4 vs a live `engine.backtest(cost_bps=25)`.
  G3 idea 618's committed .fits.csv reproduced cell for cell on all 40 of its cells: a0, mean_w,
     n_empty and sl_corr, to 1e-9.  This is the gate that makes every number below comparable to
     the claim it is testing — the machinery is imported from 618's own file, not re-typed.
  G4 sleeve invariance of base_to at f=0 (the drag axis is the same x-axis for all 40 sleeves).
  G5 the numpy metric core (CAGR/Sharpe/MaxDD) vs `engine.metrics` on a live 10 bps series.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): both panels are current constituents.
  * SMALL439 excluded for 618's reason: it prices no ETF, so 39 of 40 sleeves do not exist on it.
  * The sleeve assets are also INVESTABLE names in both panels (403/613/618's convention), so the
    TOP20 book can hold a sleeve asset on its own account.  Carried, not fixed.
  * INERTNESS IS A 4b LABEL, so it inherits 4b's SPY comparand and its MaxDD bar (idea 321: one
    number off one path).  A cell is INERT when no (lambda, f, rung) point anywhere in its 48-point
    grid passes 4b — it is a property of the whole cell, not of one arm.
  * The OOS label is read on 2017-2026 with OOS SPY bars.  The two windows are not the same test,
    and a class that is empty in one window cannot be scored in it; base rates are printed beside
    every accuracy for exactly that reason.
  * lambda can only LOWER turnover.  Idea 126: t+1 execution, no lag band.
  * 10 train sleeves carry only 2 inert ones, so tau* is an interval, not a point; its full
    admissible interval is printed and the mid-point convention is stated before it is used.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .cells.csv,
.cells_rung.csv, .sleeves.csv, .ladder.csv, .rungfit.csv, .confusion.csv, .walkforward.csv
next to itself.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, compare  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-10_is-the-CORRELATION-CUT-a-pre-registrable-SLEEVE-ADMISSION-test_C"
OUT = ROOT / "research" / "backtests"
I618 = OUT / "2026-09-10_is-the-INTERCEPT-of-the-width-law-a-DEFENSIVE-SLEEVE-statistic_C.py"
I618_FITS = OUT / "2026-09-10_is-the-INTERCEPT-of-the-width-law-a-DEFENSIVE-SLEEVE-statistic_C.fits.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load(I618, "i618")                      # 618's machinery, imported not re-typed
FREQ, GROSS = M.FREQ, M.GROSS
IS_END, OOS_START = M.IS_END, M.OOS_START
PHI, DELTA = M.PHI, M.DELTA
FSTEP, FS = M.FSTEP, M.FS
LAMBDAS, BOOKS, NTOP, PANELS, RUNGS = M.LAMBDAS, M.BOOKS, M.NTOP, M.PANELS, M.RUNGS
fast_bt, smooth, book_weights = M.fast_bt, M.smooth, M.book_weights
sleeve_weights, blend, sleeve_alone = M.sleeve_weights, M.blend, M.sleeve_alone
fmet, fsh, spearman, pass4a = M.fmet, M.fsh, M.spearman, M.pass4a

TRAIN = dict(M.SLEEVES)                      # 618's ten, verbatim
TEST = {
    # --- SECTOR: universe.json's own `sectors` group, full-history members only -------------
    "XLK": ["XLK"], "XLF": ["XLF"], "XLV": ["XLV"], "XLE": ["XLE"], "XLI": ["XLI"],
    "XLY": ["XLY"], "XLP": ["XLP"], "XLU": ["XLU"], "XLB": ["XLB"], "SMH": ["SMH"],
    "XBI": ["XBI"], "KRE": ["KRE"], "ITB": ["ITB"], "GDX": ["GDX"],
    # --- CREDIT ------------------------------------------------------------------------------
    "LQD": ["LQD"], "HYG": ["HYG"], "TIP": ["TIP"],
    # --- COMMODITY singles --------------------------------------------------------------------
    "SLV": ["SLV"], "USO": ["USO"], "UNG": ["UNG"], "DBC": ["DBC"],
    # --- 2-asset mixes -------------------------------------------------------------------------
    "CRED2": ["LQD", "HYG"], "METAL2": ["GLD", "SLV"], "DEFDUR2": ["XLU", "TLT"],
    "DOLCOM2": ["DBC", "UUP"], "BAL2": ["SPY", "TLT"],
    # --- 3-asset mixes -------------------------------------------------------------------------
    "CRED3": ["LQD", "HYG", "TIP"], "COMMOD3": ["GLD", "DBC", "USO"],
    "DEFEQ3": ["XLU", "XLP", "XLV"], "MIX3": ["SHY", "GLD", "SPY"],
}
EXCLUDED_LATE = {"XLRE": "2015-10-08", "XLC": "2018-06-19"}   # named, not silently dropped
GROUP = ({s: "TRAIN" for s in TRAIN} |
         {s: ("SECTOR" if s in ("XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB",
                                "SMH", "XBI", "KRE", "ITB", "GDX")
              else "CREDIT" if s in ("LQD", "HYG", "TIP")
              else "COMMOD" if s in ("SLV", "USO", "UNG", "DBC")
              else "MIX2" if len(TEST[s]) == 2 else "MIX3") for s in TEST})
SLEEVES = {**TRAIN, **TEST}
SLEEVE_ORDER = list(TRAIN) + list(TEST)
TRAIN_SET, TEST_SET = set(TRAIN), set(TEST)

TAUS = [round(-1.0 + 0.05 * i, 2) for i in range(41)]         # P2, uniform, fully enumerated
PUBLISHED_TAU = 0.50                                          # 618's own cut, reported beside tau*

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# classification helpers
# =====================================================================================
def auc(score: np.ndarray, pos: np.ndarray):
    """Mann-Whitney AUC of `score` for the binary `pos`.  Ties counted at 0.5 (the rank form)."""
    score, pos = np.asarray(score, float), np.asarray(pos, bool)
    ok = np.isfinite(score)
    score, pos = score[ok], pos[ok]
    n1, n0 = int(pos.sum()), int((~pos).sum())
    if n1 == 0 or n0 == 0:
        return np.nan
    r = M._rank(score)
    return float((r[pos].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def confusion(pred_inert, actual_inert):
    """(TP, FP, FN, TN) with INERT = the positive class ('reject'); admit = not inert."""
    p, a = np.asarray(pred_inert, bool), np.asarray(actual_inert, bool)
    return (int((p & a).sum()), int((p & ~a).sum()), int((~p & a).sum()), int((~p & ~a).sum()))


def scores(pred_inert, actual_inert):
    tp, fp, fn, tn = confusion(pred_inert, actual_inert)
    n = tp + fp + fn + tn
    acc = (tp + tn) / n if n else np.nan
    tpr = tp / (tp + fn) if (tp + fn) else np.nan          # reject rate on truly inert cells
    tnr = tn / (tn + fp) if (tn + fp) else np.nan          # admit rate on truly live cells
    bal = np.nanmean([tpr, tnr]) if not (np.isnan(tpr) and np.isnan(tnr)) else np.nan
    return dict(TP=tp, FP=fp, FN=fn, TN=tn, n=n, acc=acc, TPR=tpr, TNR=tnr, bal_acc=bal,
                base_inert=(tp + fn) / n if n else np.nan)


def fit_tau(corr, inert):
    """Accuracy-maximising cut on the 41-point ladder, with the full maximising INTERVAL returned.
    Convention (stated before use): tau* = the MIDPOINT of the maximising interval; with only two
    inert train sleeves the maximiser is an interval, and quoting its midpoint is the only choice
    that does not secretly encode which side of the gap the next sleeve should fall on."""
    accs = np.array([scores(np.asarray(corr, float) > t, inert)["acc"] for t in TAUS])
    best = accs.max()
    win = [TAUS[i] for i in range(len(TAUS)) if accs[i] >= best - 1e-12]
    return float(np.median(win)), float(best), (min(win), max(win)), accs


# =====================================================================================
# the grid, one panel at a time
# =====================================================================================
def run_panel(pk, px):
    inv = list(px.columns)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    idx = spy.index
    n = len(idx)
    hF = n // 2
    iIS = int((idx <= pd.Timestamp(IS_END)).sum())
    iOOS = int(np.searchsorted(idx.values, np.datetime64(pd.Timestamp(OOS_START))))
    hIS = iIS // 2
    nO = n - iOOS
    hO = nO // 2
    sv = spy.values

    def bars(a, lo, hi, h):
        s = a[lo:hi]
        cg, _, dd = fmet(s)
        return dict(s1=fsh(s[:h]), s2=fsh(s[h:]), sdd=dd, scagr=cg, sall=fsh(s))

    bF, bI, bO = bars(sv, 0, n, hF), bars(sv, 0, iIS, hIS), bars(sv, iOOS, n, hO)
    v2r, v2t = fast_bt(px, rules_v2_weights(px))
    v2 = {c: (v2r - v2t * c / 1e4).loc[start:] for c in RUNGS}
    v2b = {}
    for c in RUNGS:
        a = v2[c].values
        _, _, d = fmet(a)
        ao = a[iOOS:]
        _, _, do = fmet(ao)
        v2b[c] = (fsh(a[:hF]), fsh(a[hF:]), d, fsh(ao[:hO]), fsh(ao[hO:]), do)

    say(f"\n  panel {pk}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"evaluated from {start.date()}  (n={n}, IS<= {IS_END} -> {iIS} days, OOS from "
        f"{idx[iOOS].date()} -> {nO} days)")
    say(f"    SPY bars  FULL: H1 {bF['s1']:.3f} H2 {bF['s2']:.3f} all {bF['sall']:.3f} "
        f"DD {bF['sdd']:.1%} CAGR {bF['scagr']:.2%}")
    say(f"    SPY bars    IS: H1 {bI['s1']:.3f} H2 {bI['s2']:.3f} DD {bI['sdd']:.1%} "
        f"CAGR {bI['scagr']:.2%}")
    say(f"    SPY bars   OOS: H1 {bO['s1']:.3f} H2 {bO['s2']:.3f} all {bO['sall']:.3f} "
        f"DD {bO['sdd']:.1%} CAGR {bO['scagr']:.2%}")

    missing = [s for s, a in SLEEVES.items() if any(t not in px.columns for t in a)]
    if missing:
        say(f"    sleeves not priced on this panel (EXCLUDED, reported): {missing}")
    sl_names = [s for s in SLEEVE_ORDER if s not in missing]

    # --- the sleeve's OWN behaviour, held alone at GROSS: the PREDICTORS -------------------
    slW = {s: (None if s == "CASH" else sleeve_weights(px, SLEEVES[s])) for s in sl_names}
    top_r = fast_bt(px, book_weights(px, "TOP20", inv))[0].loc[start:]
    tv = top_r.values
    srows = []
    for s in sl_names:
        r = sleeve_alone(px, s, slW[s]).loc[start:]
        rv = r.values
        m, mi = metrics(r), metrics(r.loc[:IS_END])
        qF, qI = np.quantile(tv, 0.05), np.quantile(tv[:iIS], 0.05)
        srows.append(dict(
            panel=pk, sleeve=s, group=GROUP[s], assets="+".join(SLEEVES[s]) or "-",
            sl_corr=float(np.corrcoef(rv, tv)[0, 1]) if rv.std() > 0 else 0.0,
            sl_corr_IS=float(np.corrcoef(rv[:iIS], tv[:iIS])[0, 1]) if rv[:iIS].std() > 0 else 0.0,
            sl_corr_OOS=float(np.corrcoef(rv[iOOS:], tv[iOOS:])[0, 1]) if rv[iOOS:].std() > 0 else 0.0,
            sl_CAGR=m["CAGR"], sl_Sharpe=m["Sharpe"], sl_MaxDD=m["MaxDD"],
            sl_vol=float(r.std() * np.sqrt(252)),
            sl_cush=float(rv[tv <= qF].mean()) * 1e4,
            sl_CAGR_IS=mi["CAGR"], sl_Sharpe_IS=mi["Sharpe"], sl_MaxDD_IS=mi["MaxDD"],
            sl_vol_IS=float(rv[:iIS].std() * np.sqrt(252)),
            sl_cush_IS=float(rv[:iIS][tv[:iIS] <= qI].mean()) * 1e4))
    SS = pd.DataFrame(srows)

    # --- the grid -------------------------------------------------------------------------
    rows = []
    for book in BOOKS:
        raw = book_weights(px, book, inv)
        for lam in LAMBDAS:
            base = smooth(raw, lam)
            r_f0, t_f0 = fast_bt(px, base)
            r_f0, t_f0 = r_f0.loc[start:].values, t_f0.loc[start:].values
            base_to_cell = float(t_f0.sum() / (n / 252))
            for sleeve in sl_names:
                for f in FS:
                    if f == 0.0:
                        r0, t0 = r_f0, t_f0
                    else:
                        rr, tt = fast_bt(px, blend(base, slW[sleeve], f, sleeve))
                        r0, t0 = rr.loc[start:].values, tt.loc[start:].values
                    for c in RUNGS:
                        r = r0 - t0 * c / 1e4
                        cg, sh, dd = fmet(r)
                        h1, h2 = fsh(r[:hF]), fsh(r[hF:])
                        oos = fsh(r[iOOS:])
                        ri, ro = r[:iIS], r[iOOS:]
                        cgi, _, ddi = fmet(ri)
                        cgo, sho, ddo = fmet(ro)
                        # 4b's OOS bar compares the arm's OOS Sharpe with SPY's OWN OOS Sharpe
                        # (618's `soos`), not with SPY's full-sample Sharpe.
                        p4b = (h1 > bF["s1"] and h2 > bF["s2"] and oos > bO["sall"]
                               and DELTA * abs(bF["sdd"]) > abs(dd) and cg > PHI * bF["scagr"])
                        p4bI = (fsh(ri[:hIS]) > bI["s1"] and fsh(ri[hIS:]) > bI["s2"]
                                and DELTA * abs(bI["sdd"]) > abs(ddi) and cgi > PHI * bI["scagr"])
                        p4bO = (fsh(ro[:hO]) > bO["s1"] and fsh(ro[hO:]) > bO["s2"]
                                and DELTA * abs(bO["sdd"]) > abs(ddo) and cgo > PHI * bO["scagr"])
                        b1, b2, bdd, bo1, bo2, bodd = v2b[c]
                        rows.append(dict(
                            panel=pk, book=book, sleeve=sleeve, group=GROUP[sleeve], lam=lam, f=f,
                            cost=c, base_to=base_to_cell, drag=base_to_cell * c / 1e4,
                            arm_to=float(t0.sum() / (n / 252)),
                            CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2, OOSs=oos,
                            pass4b=bool(p4b), IS_pass4b=bool(p4bI), OOS_pass4b=bool(p4bO),
                            pass4a=bool(h1 > b1 and h2 > b2 and dd >= bdd),
                            OOS_pass4a=bool(fsh(ro[:hO]) > bo1 and fsh(ro[hO:]) > bo2
                                            and ddo >= bodd),
                            IS_Sharpe=fsh(ri), IS_CAGR=cgi, IS_MaxDD=ddi,
                            OOS_Sharpe=sho, OOS_CAGR=cgo, OOS_MaxDD=ddo))
    return pd.DataFrame(rows), SS, idx, (bF, bI, bO)


# =====================================================================================
# GATES
# =====================================================================================
def gates(panels, G618):
    say("=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True
    for pk, px in panels.items():
        W = book_weights(px, "TOP20", list(px.columns))
        start = px.index[260]
        r_f, t_f = fast_bt(px, W)
        e0 = backtest(px, W, cost_bps=0.0, freq=FREQ)
        d_r = float((r_f.loc[start:] - e0["returns"].loc[start:]).abs().max())
        d_t = float((t_f.loc[start:] - e0["turnover"].loc[start:]).abs().max())
        e25 = backtest(px, W, cost_bps=25.0, freq=FREQ)
        d_c = float(((r_f - t_f * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G1 {pk:>5}: fast_bt vs engine.backtest   max|dr| {d_r:.3e}   max|dturnover| {d_t:.3e}")
        say(f"  G2 {pk:>5}: rung identity vs live 25 bps max|dr| {d_c:.3e}")
        rr = (r_f - t_f * 10.0 / 1e4).loc[start:]
        cg, sh, dd = fmet(rr.values)
        me = metrics(rr)
        d5 = max(abs(cg - me["CAGR"]), abs(sh - me["Sharpe"]), abs(dd - me["MaxDD"]))
        say(f"  G5 {pk:>5}: numpy metric core vs engine.metrics  max|d| {d5:.3e}")
        ok &= (d_r < 1e-12) and (d_t < 1e-12) and (d_c < 1e-12) and (d5 < 1e-12)
    say(f"  GATES(1,2,5) {'PASS' if ok else 'FAIL'}")
    return ok


def gate3(G, SS, F618):
    """618's committed .fits.csv, cell for cell, on all 40 of its cells."""
    say("  G3 — idea 618's committed fits reproduced on all 40 of ITS cells (a0, mean_w, "
        "n_empty, sl_corr):")
    W = []
    for (pk, bk, sl, lam, c), sub in G[G.sleeve.isin(TRAIN_SET)].groupby(
            ["panel", "book", "sleeve", "lam", "cost"]):
        w = M.window_of(sub)
        W.append(dict(panel=pk, book=bk, sleeve=sl, lam=lam, cost=c, **w))
    W = pd.DataFrame(W)
    mine = []
    for (pk, bk, sl), sub in W.groupby(["panel", "book", "sleeve"]):
        mine.append(dict(panel=pk, book=bk, sleeve=sl,
                         a0=float(sub[sub.cost == 0].w_pts.mean()),
                         mean_w=float(sub.w_pts.mean()), n_empty=int(sub.is_empty.sum())))
    A = pd.DataFrame(mine).merge(SS[["panel", "sleeve", "sl_corr"]].drop_duplicates(),
                                 on=["panel", "sleeve"], how="left")
    B = F618[["panel", "book", "sleeve", "a0", "mean_w", "n_empty", "sl_corr"]]
    J = A.merge(B, on=["panel", "book", "sleeve"], suffixes=("", "_618"))
    d = {k: float((J[k] - J[k + "_618"]).abs().max()) for k in ("a0", "mean_w", "n_empty", "sl_corr")}
    say(f"       n cells matched {len(J)}/40   max|da0| {d['a0']:.3e}   max|dmean_w| "
        f"{d['mean_w']:.3e}   max|dn_empty| {d['n_empty']:.3e}   max|dsl_corr| {d['sl_corr']:.3e}")
    good = len(J) == 40 and max(d.values()) < 1e-9
    say(f"  G3 {'PASS' if good else 'FAIL'}")
    return good, W


def walkforward(pk, G, cuts, bars):
    """PROTOCOL 8 — (sleeve, f), the queue's OWN two parameters, chosen on 2009-2016 ONLY.
    For each cut, S_ADMIT_* and S_REJECT_* differ from S_ALL in NOTHING but the sleeve set the
    cut leaves standing, so their OOS gap IS that cut's economic value.  Two cuts are carried:
    tau* (fitted here on TRAIN x IS) and 0.50 (618's published cut), because a degenerate tau*
    would otherwise leave the economic leg untested."""
    bO = bars[2]
    wf = []
    sub_p = G[G.panel == pk]
    for (book, lam), sub0 in sub_p.groupby(["book", "lam"]):
        for c in RUNGS:
            sub = sub0[sub0.cost == c]
            pos = sub[sub.f > 0]
            picks = {"S_ALL": pos.loc[pos.IS_Sharpe.idxmax()],
                     "S_CASH": sub[(sub.sleeve == "CASH") & (sub.f > 0)].pipe(
                         lambda d: d.loc[d.IS_Sharpe.idxmax()] if len(d) else None)}
            scr = pos[pos.IS_pass4b]
            picks["S_IS4b"] = (scr.loc[scr.IS_Sharpe.idxmax()] if len(scr)
                               else pos.loc[pos.IS_Sharpe.idxmax()])
            tst = pos[pos.sleeve.isin(TEST_SET)]
            for tag, amap in cuts.items():
                for nm, d in (("", pos), ("TEST", tst)):
                    a = d[[amap[(pk, s)] for s in d.sleeve]]
                    r = d[[not amap[(pk, s)] for s in d.sleeve]]
                    k = (nm + "_") if nm else ""
                    picks[f"S_{k}ADMIT{tag}"] = (a.loc[a.IS_Sharpe.idxmax()] if len(a) else None)
                    picks[f"S_{k}REJECT{tag}"] = (r.loc[r.IS_Sharpe.idxmax()] if len(r) else None)
            for sname, p in picks.items():
                if p is None:
                    continue
                wf.append(dict(panel=pk, book=book, lam=lam, cost=c, selector=sname,
                               f=float(p.f), sleeve=str(p.sleeve), group=str(p.group),
                               OOS_CAGR=float(p.OOS_CAGR), OOS_Sharpe=float(p.OOS_Sharpe),
                               OOS_MaxDD=float(p.OOS_MaxDD),
                               SPY_CAGR=bO["scagr"], SPY_Sharpe=bO["sall"], SPY_MaxDD=bO["sdd"],
                               beats_SPY=bool(p.OOS_Sharpe > bO["sall"]),
                               OOS_4b=bool(p.OOS_pass4b), OOS_4a=bool(p.OOS_pass4a)))
    return pd.DataFrame(wf)


def main():
    T0 = time.time()
    say("=" * 100)
    say("IDEA 650 — is the CORRELATION CUT a pre-registrable SLEEVE-ADMISSION test?   (lane C)")
    say("=" * 100)
    say(f"tuned parameter 1 (SLEEVE SET): {len(TRAIN)} TRAIN (618's, verbatim) + {len(TEST)} TEST "
        f"(never run) = {len(SLEEVES)} sleeves — all reported")
    say(f"   TRAIN: {list(TRAIN)}")
    for g in ("SECTOR", "CREDIT", "COMMOD", "MIX2", "MIX3"):
        say(f"   TEST {g:>6}: {[s for s in TEST if GROUP[s] == g]}")
    say(f"   EXCLUDED for short history (named, not dropped silently): {EXCLUDED_LATE}")
    say(f"tuned parameter 2 (THRESHOLD) : tau on {len(TAUS)} points {TAUS[0]}..{TAUS[-1]} step 0.05"
        f" — every point reported; the carried tau* is fitted on TRAIN x IS ONLY")
    say(f"reported axes: panels {PANELS}; books {BOOKS}; lambda {LAMBDAS}; f {FS}; rungs {RUNGS} bps")
    say(f"weekly, t+1, gross {GROSS}; IS <= {IS_END}, OOS >= {OOS_START}; 4b CAGR floor {PHI} x SPY,"
        f" DD cap {DELTA} x SPY")
    say("INERT (the label) = no (lambda, f, rung) point in the cell's 48-point grid passes 4b.")

    panels = {"u56": load_universe(), "broad": load_universe(broad=True)}
    if not gates(panels, None):
        say("\n*** GATES FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1

    say()
    say("=" * 100)
    say(f"THE GRID (2 panels x 2 books x {len(SLEEVES)} sleeves x {len(LAMBDAS)} lambdas x "
        f"{len(FS)} f, read at {len(RUNGS)} rungs)")
    say("=" * 100)
    G, SSl, WFl, BARS, IDX = [], [], [], {}, {}
    for pk in PANELS:
        g, ss, idx, bars = run_panel(pk, panels[pk])
        G.append(g)
        SSl.append(ss)
        BARS[pk] = bars
        IDX[pk] = idx
        say(f"    {pk}: {len(g)} arm-rows, {time.time() - T0:.0f}s elapsed")
    G = pd.concat(G, ignore_index=True)
    SS = pd.concat(SSl, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    SS.to_csv(OUT / f"{STEM}.sleeves.csv", index=False)
    nsim = G[["panel", "book", "sleeve", "lam", "f"]].drop_duplicates().shape[0]
    say(f"\n  {len(G)} arm-rows ({nsim} weight paths x {len(RUNGS)} rungs).")

    # --- G3 / G4 ----------------------------------------------------------------------------
    F618 = pd.read_csv(I618_FITS)
    g3, _ = gate3(G, SS, F618)
    piv = G[G.f == 0].pivot_table(index=["panel", "book", "lam"], columns="sleeve", values="base_to")
    dmax = float((piv.max(axis=1) - piv.min(axis=1)).abs().max())
    say(f"  G4 base_to at f=0 is sleeve-invariant across all {len(SLEEVES)} sleeves: max spread "
        f"{dmax:.3e} ({'PASS' if dmax < 1e-12 else 'FAIL'})")
    if not (g3 and dmax < 1e-12):
        say("\n*** GATES FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1

    # --- the CELLS: predictor + the three labels ----------------------------------------------
    lab = G.groupby(["panel", "book", "sleeve"]).agg(
        n4b_IS=("IS_pass4b", "sum"), n4b_OOS=("OOS_pass4b", "sum"), n4b_full=("pass4b", "sum"),
        n4a_full=("pass4a", "sum"), n_pts=("pass4b", "size")).reset_index()
    for w in ("IS", "OOS", "full"):
        lab[f"inert_{w}"] = lab[f"n4b_{w}"] == 0
    C = lab.merge(SS, on=["panel", "sleeve"], how="left")
    C["split"] = np.where(C.sleeve.isin(TRAIN_SET), "TRAIN", "TEST")
    C.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    say()
    say("-" * 100)
    say("THE CELLS — predictor (IS-window corr to the panel's TOP20 book) and the three labels")
    say("-" * 100)
    show = ["split", "group", "panel", "book", "sleeve", "sl_corr_IS", "sl_corr", "sl_corr_OOS",
            "sl_MaxDD_IS", "inert_IS", "inert_OOS", "inert_full", "n4b_IS", "n4b_OOS", "n4b_full"]
    say(C.sort_values(["split", "group", "sleeve", "panel", "book"])[show]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say()
    for sp in ("TRAIN", "TEST"):
        s = C[C.split == sp]
        say(f"  {sp:>5} base rates over {len(s)} cells: inert_IS {int(s.inert_IS.sum())} "
            f"({s.inert_IS.mean():.1%})   inert_OOS {int(s.inert_OOS.sum())} "
            f"({s.inert_OOS.mean():.1%})   inert_full {int(s.inert_full.sum())} "
            f"({s.inert_full.mean():.1%})")

    # --- the same cells, RUNG BY RUNG (the pooled label pools over 6 rungs; a rung-wise label
    # --- gives the IS fit its best chance of finding a positive class at all) ------------------
    labc = G.groupby(["panel", "book", "sleeve", "cost"]).agg(
        n4b_IS=("IS_pass4b", "sum"), n4b_OOS=("OOS_pass4b", "sum"),
        n4b_full=("pass4b", "sum")).reset_index()
    for w in ("IS", "OOS", "full"):
        labc[f"inert_{w}"] = labc[f"n4b_{w}"] == 0
    CR = labc.merge(SS[["panel", "sleeve", "group", "sl_corr_IS", "sl_corr", "sl_MaxDD_IS"]],
                    on=["panel", "sleeve"], how="left")
    CR["split"] = np.where(CR.sleeve.isin(TRAIN_SET), "TRAIN", "TEST")
    CR.to_csv(OUT / f"{STEM}.cells_rung.csv", index=False)

    # --- H1: fit the cut on TRAIN x IS ONLY, every ladder point reported ----------------------
    say()
    say("-" * 100)
    say("H1 — FIT: the threshold ladder, accuracy at EVERY point (P2 fully enumerated)")
    say("-" * 100)
    TR = C[C.split == "TRAIN"]
    TE = C[C.split == "TEST"]
    tau_star, acc_fit, span, accs_tr_is = fit_tau(TR.sl_corr_IS.values, TR.inert_IS.values)
    lad = []
    say(f"  {'tau':>6} {'TRAIN-IS':>9} {'TRAIN-OOS':>10} {'TEST-IS':>8} {'TEST-OOS':>9} "
        f"{'TEST-OOS bal':>13} {'TEST-OOS TP/FP/FN/TN':>22}")
    for t in TAUS:
        row = dict(tau=t)
        for nm, d, lb in (("TRAIN_IS", TR, "inert_IS"), ("TRAIN_OOS", TR, "inert_OOS"),
                          ("TEST_IS", TE, "inert_IS"), ("TEST_OOS", TE, "inert_OOS"),
                          ("TEST_full", TE, "inert_full")):
            s = scores(d.sl_corr_IS.values > t, d[lb].values)
            row[f"acc_{nm}"] = s["acc"]
            row[f"bal_{nm}"] = s["bal_acc"]
            if nm == "TEST_OOS":
                row.update({f"TEST_OOS_{k}": s[k] for k in ("TP", "FP", "FN", "TN")})
        lad.append(row)
        say(f"  {t:>+6.2f} {row['acc_TRAIN_IS']:>9.3f} {row['acc_TRAIN_OOS']:>10.3f} "
            f"{row['acc_TEST_IS']:>8.3f} {row['acc_TEST_OOS']:>9.3f} {row['bal_TEST_OOS']:>13.3f} "
            f"{row['TEST_OOS_TP']:>6}/{row['TEST_OOS_FP']}/{row['TEST_OOS_FN']}/{row['TEST_OOS_TN']}")
    LAD = pd.DataFrame(lad)
    LAD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    say(f"\n  TRAIN x IS maximiser: accuracy {acc_fit:.3f} over the interval "
        f"[{span[0]:+.2f}, {span[1]:+.2f}] -> tau* = {tau_star:+.3f} (midpoint convention, "
        f"stated above).  618's published cut is {PUBLISHED_TAU:+.2f}.")
    say(f"  The gap the interval sits in: max sl_corr_IS among LIVE train cells "
        f"{TR[~TR.inert_IS].sl_corr_IS.max():+.4f}; min among INERT train cells "
        f"{TR[TR.inert_IS].sl_corr_IS.min():+.4f}.")
    say(f"  AUC on TRAIN x IS (the fit itself): sl_corr_IS "
        f"{auc(TR.sl_corr_IS.values, TR.inert_IS.values):.3f}   "
        f"sl_MaxDD_IS {auc(TR.sl_MaxDD_IS.values, TR.inert_IS.values):.3f} (618's foil)")

    # --- H2 / H3: the 2x2 of (which sleeves) x (which window) ---------------------------------
    say()
    say("-" * 100)
    say("H2 / H3 — the SAME tau*, scored on the 2x2 of sleeves x window.  INERT = positive class")
    say("  ('reject'); admit = not inert.  TPR = share of truly-inert cells rejected; TNR = share")
    say("  of truly-live cells admitted.  A rule that only ever admits has TPR 0 whatever its acc.")
    say("-" * 100)
    conf = []
    say(f"  {'sleeves':>7} {'window':>7} {'n':>4} {'inert':>6} {'acc':>6} {'bal':>6} {'TPR':>6} "
        f"{'TNR':>6} {'TP':>4} {'FP':>4} {'FN':>4} {'TN':>4} {'AUC corr':>9} {'AUC MaxDD':>10}")
    for sp, d in (("TRAIN", TR), ("TEST", TE)):
        for w in ("IS", "OOS", "full"):
            s = scores(d.sl_corr_IS.values > tau_star, d[f"inert_{w}"].values)
            a1 = auc(d.sl_corr_IS.values, d[f"inert_{w}"].values)
            a2 = auc(d.sl_MaxDD_IS.values, d[f"inert_{w}"].values)
            conf.append(dict(split=sp, window=w, tau=tau_star, **s, auc_corr=a1, auc_maxdd=a2))
            say(f"  {sp:>7} {w:>7} {s['n']:>4} {s['base_inert']:>6.2f} {s['acc']:>6.3f} "
                f"{s['bal_acc']:>6.3f} {s['TPR']:>6.3f} {s['TNR']:>6.3f} {s['TP']:>4} {s['FP']:>4} "
                f"{s['FN']:>4} {s['TN']:>4} {a1:>9.3f} {a2:>10.3f}")
    say(f"\n  the same table at 618's PUBLISHED cut {PUBLISHED_TAU:+.2f} (not fitted here):")
    for sp, d in (("TRAIN", TR), ("TEST", TE)):
        for w in ("IS", "OOS", "full"):
            s = scores(d.sl_corr_IS.values > PUBLISHED_TAU, d[f"inert_{w}"].values)
            conf.append(dict(split=sp, window=w, tau=PUBLISHED_TAU, **s,
                             auc_corr=auc(d.sl_corr_IS.values, d[f"inert_{w}"].values),
                             auc_maxdd=auc(d.sl_MaxDD_IS.values, d[f"inert_{w}"].values)))
            say(f"  {sp:>7} {w:>7} {s['n']:>4} {s['base_inert']:>6.2f} {s['acc']:>6.3f} "
                f"{s['bal_acc']:>6.3f} {s['TPR']:>6.3f} {s['TNR']:>6.3f} {s['TP']:>4} {s['FP']:>4} "
                f"{s['FN']:>4} {s['TN']:>4}")
    CONF = pd.DataFrame(conf)
    CONF.to_csv(OUT / f"{STEM}.confusion.csv", index=False)

    say()
    say("  TEST x OOS errors, named (the cells the rule gets wrong is the whole content of H3):")
    TE2 = TE.assign(pred_inert=TE.sl_corr_IS.values > tau_star)
    err = TE2[TE2.pred_inert != TE2.inert_OOS]
    if len(err) == 0:
        say("    none.")
    else:
        say("    " + err[["group", "panel", "book", "sleeve", "sl_corr_IS", "pred_inert",
                          "inert_OOS", "n4b_OOS"]]
            .sort_values(["group", "sleeve"]).to_string(index=False,
                                                        float_format=lambda x: f"{x:.4f}")
            .replace("\n", "\n    "))
    say()
    say("  by TEST group (does the rule work on some sleeve families and not others?):")
    say(f"  {'group':>8} {'n':>4} {'inertOOS':>9} {'acc':>6} {'bal':>6} {'TPR':>6} {'TNR':>6}")
    for g, d in TE.groupby("group"):
        s = scores(d.sl_corr_IS.values > tau_star, d.inert_OOS.values)
        say(f"  {g:>8} {s['n']:>4} {s['base_inert']:>9.2f} {s['acc']:>6.3f} {s['bal_acc']:>6.3f} "
            f"{s['TPR']:>6.3f} {s['TNR']:>6.3f}")

    say()
    say("  STABILITY OF THE PREDICTOR ITSELF — is the sleeve's corr the same number in the two")
    say("  windows?  (a cut cannot be pre-registrable if its input drifts across the boundary)")
    U = SS.drop_duplicates(subset=["panel", "sleeve"])
    say(f"    rho(sl_corr_IS, sl_corr_OOS) over {len(U)} (panel, sleeve) pairs: "
        f"{spearman(U.sl_corr_IS.values, U.sl_corr_OOS.values):+.4f}   "
        f"max |IS - OOS| {float((U.sl_corr_IS - U.sl_corr_OOS).abs().max()):.4f}   "
        f"mean |IS - OOS| {float((U.sl_corr_IS - U.sl_corr_OOS).abs().mean()):.4f}")
    flip = U[((U.sl_corr_IS > tau_star) != (U.sl_corr_OOS > tau_star))]
    say(f"    (panel, sleeve) pairs whose SIDE of tau* changes between windows: {len(flip)} of "
        f"{len(U)}" + (("  -> " + ", ".join(f"{r.panel}/{r.sleeve}" for r in flip.itertuples()))
                       if len(flip) else ""))

    # --- H1b: the same fit RUNG BY RUNG ------------------------------------------------------
    say()
    say("-" * 100)
    say("H1b — the same fit RUNG BY RUNG.  The pooled label calls a cell inert only if it is")
    say("empty at all six rungs at once; a rung-wise label is the weakest form of the class and")
    say("so the fit's best chance of being IDENTIFIED on the IS window.")
    say("-" * 100)
    say(f"  {'rung':>5} {'TRAIN-IS inert':>15} {'identified':>11} {'fit acc':>8} "
        f"{'tau* interval':>20} "
        f"{'tau*':>7} {'TEST-OOS inert':>15} {'acc':>6} {'bal':>6} {'TPR':>6} {'TNR':>6} "
        f"{'AUC':>6} {'acc@0.50':>9} {'bal@0.50':>9}")
    rungrows = []
    for c in RUNGS:
        tr = CR[(CR.split == "TRAIN") & (CR.cost == c)]
        te = CR[(CR.split == "TEST") & (CR.cost == c)]
        nin = int(tr.inert_IS.sum())
        ident = 0 < nin < len(tr)
        t_c, a_c, sp_c, _ = fit_tau(tr.sl_corr_IS.values, tr.inert_IS.values)
        s_c = scores(te.sl_corr_IS.values > t_c, te.inert_OOS.values)
        s_p = scores(te.sl_corr_IS.values > PUBLISHED_TAU, te.inert_OOS.values)
        a_auc = auc(te.sl_corr_IS.values, te.inert_OOS.values)
        rungrows.append(dict(cost=c, train_IS_inert=nin, identified=ident, tau_lo=sp_c[0],
                             tau_hi=sp_c[1], tau_star=t_c, train_IS_acc=a_c,
                             test_OOS_inert=int(te.inert_OOS.sum()), **{f"tau_{k}": s_c[k] for k in
                             ("acc", "bal_acc", "TPR", "TNR", "TP", "FP", "FN", "TN")},
                             auc_corr=a_auc,
                             **{f"pub_{k}": s_p[k] for k in ("acc", "bal_acc", "TPR", "TNR")}))
        say(f"  {c:>5.0f} {str(nin) + '/' + str(len(tr)):>15} {str(ident):>11} {a_c:>8.3f} "
            f"{'[' + f'{sp_c[0]:+.2f}' + ',' + f'{sp_c[1]:+.2f}' + ']':>20} "
            f"{t_c:>+7.3f} {str(int(te.inert_OOS.sum())) + '/' + str(len(te)):>15} {s_c['acc']:>6.3f} "
            f"{s_c['bal_acc']:>6.3f} {s_c['TPR']:>6.3f} {s_c['TNR']:>6.3f} {a_auc:>6.3f} "
            f"{s_p['acc']:>9.3f} {s_p['bal_acc']:>9.3f}")
    RR = pd.DataFrame(rungrows)
    RR.to_csv(OUT / f"{STEM}.rungfit.csv", index=False)
    say(f"  IDENTIFIED = the TRAIN x IS label has BOTH classes at that rung; where it does not, "
        f"tau* is whatever the ladder's top end is and the cut is a no-op by construction.")
    say(f"  rungs at which the IS fit is identified: {int(RR.identified.sum())} of {len(RR)}")

    # --- KEEP paths -------------------------------------------------------------------------
    say()
    say("-" * 100)
    say("KEEP PATHS (PROTOCOL 4) — both, on EVERY arm-row")
    say("-" * 100)
    say(f"  4a (vs live RULES v2, cost-matched): {int(G.pass4a.sum())} / {len(G)}")
    say(f"  4b (vs SPY, all five bars)         : {int(G.pass4b.sum())} / {len(G)}")
    say(f"  BOTH                               : {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for c in RUNGS:
        s = G[G.cost == c]
        say(f"    @{c:>4.0f} bps: 4a {int(s.pass4a.sum()):>5}  4b {int(s.pass4b.sum()):>5}  "
            f"BOTH {int((s.pass4a & s.pass4b).sum()):>4}   of {len(s)}")
    say("  4b passes at PROTOCOL's own 10 bps rung, by sleeve GROUP:")
    s10 = G[G.cost == 10]
    for g, sub in s10.groupby("group"):
        say(f"    {g:>6}: 4b {int(sub.pass4b.sum()):>5} / {len(sub):>5}   "
            f"4a {int(sub.pass4a.sum()):>3}   BOTH {int((sub.pass4a & sub.pass4b).sum()):>3}")

    # --- rule 8 ------------------------------------------------------------------------------
    say()
    say("-" * 100)
    say("RULE 8 (PROTOCOL 8) — (sleeve, f) chosen on 2009-2016 ONLY, 2017-2026 read once.")
    say("S_ADMIT / S_REJECT differ from S_ALL in NOTHING but the sleeve set the IS-fitted cut")
    say("leaves standing, so their OOS gap is the cut's value in Sharpe rather than in accuracy.")
    say("-" * 100)
    U0 = SS.drop_duplicates(subset=["panel", "sleeve"])
    cuts = {"": {(r.panel, r.sleeve): bool(r.sl_corr_IS <= tau_star) for r in U0.itertuples()},
            "50": {(r.panel, r.sleeve): bool(r.sl_corr_IS <= PUBLISHED_TAU)
                   for r in U0.itertuples()}}
    say(f"  cut tau* = {tau_star:+.3f} admits "
        f"{sum(cuts[''].values())}/{len(cuts[''])} (panel, sleeve) pairs;  "
        f"cut {PUBLISHED_TAU:+.2f} admits {sum(cuts['50'].values())}/{len(cuts['50'])}.")
    for pk in PANELS:
        WFl.append(walkforward(pk, G, cuts, BARS[pk]))
    WF = pd.concat(WFl, ignore_index=True)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.groupby("selector").agg(
        picks=("f", "size"), median_f=("f", "median"),
        modal_sleeve=("sleeve", lambda s: s.mode().iloc[0]),
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), beats_SPY=("beats_SPY", "sum"),
        OOS_4b=("OOS_4b", "sum"), OOS_4a=("OOS_4a", "sum")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    say()
    for pk in PANELS:
        s = WF[(WF.panel == pk) & (WF.cost == 10)]
        say(f"  {pk:>6} @10 bps  SPY OOS: CAGR {s.SPY_CAGR.iloc[0]:.2%}  Sharpe "
            f"{s.SPY_Sharpe.iloc[0]:.3f}  MaxDD {s.SPY_MaxDD.iloc[0]:.1%}")
        for sn, g in s.groupby("selector"):
            say(f"          {sn:>14}: OOS CAGR {g.OOS_CAGR.mean():.2%}  Sharpe "
                f"{g.OOS_Sharpe.mean():.3f}  MaxDD {g.OOS_MaxDD.mean():.1%}  "
                f"4b {int(g.OOS_4b.sum())}/{len(g)}  4a {int(g.OOS_4a.sum())}/{len(g)}  "
                f"sleeves {sorted(set(g.sleeve))[:6]}")
    say()
    say("  PAIRED (same panel/book/lambda/rung) OOS Sharpe difference, ADMIT minus REJECT —")
    say("  the cut's economic value, sign test over the paired cells:")
    for tag, a, b in (("tau* all sleeves", "S_ADMIT", "S_REJECT"),
                      ("tau* test sleeves", "S_TEST_ADMIT", "S_TEST_REJECT"),
                      ("tau* admit vs all", "S_ADMIT", "S_ALL"),
                      ("0.50 all sleeves", "S_ADMIT50", "S_REJECT50"),
                      ("0.50 test sleeves", "S_TEST_ADMIT50", "S_TEST_REJECT50"),
                      ("0.50 admit vs all", "S_ADMIT50", "S_ALL"),
                      ("0.50 admit vs CASH", "S_ADMIT50", "S_CASH")):
        A = WF[WF.selector == a].set_index(["panel", "book", "lam", "cost"]).OOS_Sharpe
        B = WF[WF.selector == b].set_index(["panel", "book", "lam", "cost"]).OOS_Sharpe
        j = pd.concat([A.rename("a"), B.rename("b")], axis=1).dropna()
        d = j.a - j.b
        say(f"    {tag:>21}: n {len(d):>3}  mean {d.mean():+.4f}  median {d.median():+.4f}  "
            f"a>b {int((d > 0).sum())}/{len(d)}  max {d.max():+.4f}  min {d.min():+.4f}")

    # --- PROTOCOL 3 reference arm ------------------------------------------------------------
    say()
    say("-" * 100)
    say("PROTOCOL 3 — a pre-registered reference arm through baseline.compare (u56, TOP20,")
    say("the modal S_TEST_ADMIT sleeve at 10 bps, f = 0.25, lambda = 1.00).  Reported, not chosen.")
    say("-" * 100)
    modal = WF[(WF.selector == "S_TEST_ADMIT50") & (WF.cost == 10) & (WF.panel == "u56")].sleeve
    ref_sleeve = modal.mode().iloc[0] if len(modal) else "LQD"
    pxu = panels["u56"]
    slw = sleeve_weights(pxu, SLEEVES[ref_sleeve])
    ref = compare(f"650 ref: u56 TOP20 + {ref_sleeve} f=0.25",
                  lambda p: blend(book_weights(p, "TOP20", list(p.columns)), slw, 0.25, ref_sleeve),
                  pxu, freq=FREQ, cost_bps=10)
    for ln in ref["table"].to_string(float_format=lambda x: f"{x:.3f}").split("\n"):
        LOG.append(ln)
    LOG.append("Verdict (4a): " + ref["verdict"])

    say()
    say("=" * 100)
    say(f"done in {time.time() - T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
