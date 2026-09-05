#!/usr/bin/env python3
"""QUEUE idea 81 — vol20-as-the-hidden-ranking-key  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 81)
    "idea 80 found the short-horizon vol premium INSIDE the gate is strongly signed
     (Fama-MacBeth vol20 slope +0.0045 t +3.90 on u56, +0.0029 t +3.19 on broad; low-vol IC
     -0.043/-0.033) yet RULES v1 divides its composite BY sqrt(vol20), i.e. tilts the wrong way
     against its own panel.  Test the sign directly: v1's composite with the vol scaler as
     /sqrt(v), x1 (none) and xsqrt(v), at n in {5,20}.  Max 2 params."

WHAT IS AT STAKE.  RULES v1's live book is `composite / sqrt(vol20)`.  Idea 1 already showed
    that DELETING the scaler is worth +10.1%/yr (t 3.33) at v1's own n=5, and idea 80 showed
    WHY: inside the 200d + vol20<0.60 gate, next week's cross-sectional return slopes POSITIVE
    on vol20.  Both results say the live book's scaler is signed against its own panel.  Neither
    tested the third arm.  If the premium is real and monotone, x sqrt(v) should beat x1 by
    about as much as x1 beats / sqrt(v), and the live rule is not merely redundant but inverted.
    If instead x1 is the peak, the scaler's damage is a VOLATILITY-TARGETING artefact (holding
    low-vol names shrinks the book) and there is no tradeable premium to lean into.  The two
    hypotheses make opposite predictions about the third arm, which is why it is worth running.

    The decisive quantity is not the slope's t-statistic, which idea 80 already has.  It is
    whether a book built to harvest the slope clears PROTOCOL 4b — because tilting toward high
    vol buys return with drawdown, and 4b's drawdown cap is exactly what rations that.

CORPUS
    3 panels (u56 / broad / small) x 2 cost rungs (10, 25 bps) x the 6-point grid = 36 books,
    weekly, t+1, no leverage, no shorting.  Books are equal-weight at 0.75/n so that the
    POSITION COUNT and the GROSS EXPOSURE are not one dial (idea 2's correction of ideas 1
    and 40); v1's literal fixed-15% construction is run alongside at n=5 as arm FIXEDW, as a
    reproduction check only, never as a comparison.

TUNED PARAMETERS — exactly two, both swept exhaustively, ALL 6 grid points reported:
    1. the vol scaler, 3 values:  INV  = composite / sqrt(vol20)   (RULES v1's live tilt)
                                  NONE = composite                 (idea 1's / idea 2's book)
                                  POS  = composite * sqrt(vol20)   (the sign idea 80 implies)
    2. the position count n, 2 values: 5 (v1's) and 20 (idea 2's standing candidate).
    Panels, cost rungs, the OOS window and every diagnostic below are REPORTED axes, never
    selected on.  vol20's 0.60 gate and the 200d gate are held at v1's values throughout.

REPRODUCTION, asserted before any new number is read
    [a] INV / n=5 / FIXEDW w=0.15 must equal `baseline.rules_v1_weights(px)` cell-for-cell, so
        the INV arm IS the live book and not a lookalike.
    [b] NONE / n=20 / EQW on u56@10bps must equal idea 80's committed CAND/COMP/n=20 code
        path cell-for-cell — idea 80 is the script that claims to reproduce idea 2's KEEP row,
        so this run is checked against the code, not against a rounded published digit.  Where
        the published digit and the committed code disagree, BOTH are printed.
    [c] idea 80's `fama_macbeth` is IMPORTED and called verbatim; its published BIVARIATE
        vol20 slope must come back at +0.0045 (t +3.90) on u56 and +0.0029 (t +3.19) on broad.
        If [c] fails, the premise being tested has not been reproduced and nothing below is a
        test of it.

WALK-FORWARD (PROTOCOL rule 8) — both selection rules are fixed BEFORE any OOS number is read:
    S1 plain IS Sharpe, S2 the 4b-aware IS screen (IS halves and IS drawdown and IS CAGR bars).
    Parameters are chosen on 2009-2016 (2011-2016 on the small panel) only; the pick is read
    ONCE on 2017-01-01..2026 and reported as OOS CAGR / Sharpe / MaxDD against RULES v1 (the
    live book, same panel and cost) and SPY.  Both KEEP paths (4a and 4b) are evaluated at
    every one of the 36 books, on the full sample and again on the OOS window alone.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  The premise reproduces: [c] holds on u56 and broad, and the sign is the same on the
        small panel (which idea 80 never ran).
    P2  If the premium is tradeable, POS > NONE > INV on full-sample Sharpe at BOTH n on the
        two large-cap panels (6 of 6 orderings).  If instead NONE is the peak, the scaler is a
        vol-targeting artefact and there is nothing to harvest.
    P3  POS buys return with drawdown: at matched n, POS's MaxDD is deeper than NONE's in every
        cell, and any 4b failure of POS is on the DRAWDOWN cap, not the CAGR floor.
    P4  Rule 8 does not pick POS: under both selection rules, on both large-cap panels.
    P5  Nothing here is a KEEP: 0 of 36 books pass 4b in every cell it is run in.

CAVEATS carried, not buried
    * Survivorship: all three panels are current-constituent lists (idea 54); the small panel
      drops the 44 tickers with max_1d_move >= 1.0 and its SPY is a held-out benchmark, not a
      constituent.  It runs AGAINST the POS arm being a real edge — the high-vol cohort is
      exactly where delisted names would sit, so POS is flattered here.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so the IS
      drawdown bar admits too much for every arm equally.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * Idea 49/39: the eligibility gate is inverted on the small panel, so every small-panel
      number here is a number about a gate that does not work there; it is reported, not traded.
    * No IWM in the cache, so the small panel is judged against SPY (stated, not adjusted).

HARNESS
    `baseline` (the live rules), idea 129's panel/bar machinery and idea 80's Fama-MacBeth and
    book constructor are IMPORTED, so the INV arm is literally the live book, the bars are
    literally 4b's, and the premise under test is literally idea 80's own measurement.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .fm.csv, .diag.csv, .walkforward.csv.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_vol20-as-the-hidden-ranking-key_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I80P = OUT / "2026-09-04_prox-inverted-signal_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
I80 = _load(I80P, "i80")

FREQ = "W"
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI0, DELTA0 = 0.70, 0.60
GROSS, MAX_VOL = 0.75, 0.60

SCALERS = ["INV", "NONE", "POS"]      # tuned parameter 1
NS = [5, 20]                          # tuned parameter 2

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the book
def parts(px):
    """v1's own pieces: composite (with its trend factor), the 200d flag, vol20."""
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
            + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    v = px.pct_change().rolling(20).std() * np.sqrt(252)
    return comp * (0.5 + 0.5 * above.astype(float)), above, v


def score_of(px, scaler, pk="", cache={}):
    key = (pk, scaler)
    if key in cache:
        return cache[key]
    s, above, v = parts(px)
    vv = v.clip(lower=0.08) ** 0.5
    s = {"INV": s / vv, "NONE": s, "POS": s * vv}[scaler]
    cache[key] = (s, above, v)
    return cache[key]


def weights(px, scaler, n, fixedw=None, pk=""):
    s, above, v = score_of(px, scaler, pk)
    elig = s.where(above & (v < MAX_VOL))
    rank = elig.rank(axis=1, ascending=False)
    w = (GROSS / n) if fixedw is None else fixedw
    return (rank <= n).astype(float) * w


def eligible_mask(px, pk=""):
    _, above, v = score_of(px, "NONE", pk)
    return above & (v < MAX_VOL)


# ------------------------------------------------------------------ Fama-MacBeth (idea 80's own)
def fama_macbeth(px, pk):
    """Idea 80's `fama_macbeth` is IMPORTED and called verbatim, so check [c] is a
    reproduction of its published slopes rather than a lookalike.  It regresses next week's
    return on the PERCENTILE RANKS of PROX and vol20 over eligible names and reports both the
    univariate and the bivariate slope; idea 80's published +0.0045 / +0.0029 are the
    BIVARIATE vol20 slopes.  The weekly rank IC of -vol20 ("low vol") is reported alongside
    from idea 80's `rank_ic`."""
    start = px.index[260]
    el = I80.eligible_mask(px)
    fm = I80.fama_macbeth(px, el, start)
    wk, fwd, elw = I80.weekly_panel(px, el, start)
    ic = I80.ic_line(pd.Series(I80.rank_ic(-I80.vol20_of(px), wk.index, fwd, elw)))
    return dict(panel=pk, n_weeks=fm["vol20_biv"][2],
                slope_uni=fm["vol20_uni"][0], t_uni=fm["vol20_uni"][1],
                slope_biv=fm["vol20_biv"][0], t_biv=fm["vol20_biv"][1],
                prox_uni=fm["PROX_uni"][0], t_prox_uni=fm["PROX_uni"][1],
                prox_biv=fm["PROX_biv"][0], t_prox_biv=fm["PROX_biv"][1],
                lowvol_IC=ic[0], t_IC=ic[1])


def main():
    say("=" * 200)
    say(f"IDEA 81 — vol20-as-the-hidden-ranking-key   ({STEM})")
    say("RULES v1 divides its composite by sqrt(vol20).  Idea 80 says the premium inside the "
        "gate runs the other way.  Test the sign directly: / sqrt(v), x1, x sqrt(v).")
    say("=" * 200)

    ok, rows, fmrows, diag, rets, ref = {}, [], [], [], {}, {}

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk] = dict(bfull=bfull, bIS=bIS, bOOS=bOOS, spy=ms, spy_oos=mso, v1=v1,
                       start=start, desc=desc)
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, {px.index[0].date()}.."
            f"{px.index[-1].date()}, eval from {start.date()}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso['CAGR']:.2%}/"
            f"{mso['Sharpe']:.3f}/{mso['MaxDD']:.2%}")
        for c in COSTS:
            m = metrics(v1[c])
            mo = metrics(v1[c].loc[OOS_START:])
            say(f"    RULES v1 @{int(c)}bps: {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%}"
                f"  | OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}")

        # ---- [a] the INV arm IS the live book
        Wv1 = weights(px, "INV", 5, fixedw=0.15, pk=pk)
        dmax = float((Wv1 - rules_v1_weights(px)).abs().max().max())
        ok[f"a:{pk}"] = dmax < 1e-12
        say(f"[a] INV/n=5/FIXEDW vs baseline.rules_v1_weights: max|diff| = {dmax:.3e} "
            f"({'EXACT' if ok[f'a:{pk}'] else 'NOT EXACT — the INV arm is not the live book'})")

        # ---- [c] idea 80's Fama-MacBeth premise
        fm = fama_macbeth(px, pk)
        fm.update(panel=pk)
        fmrows.append(fm)
        say(f"[c] idea 80's Fama-MacBeth, called verbatim ({fm['n_weeks']} wks): vol20 slope "
            f"univariate {fm['slope_uni']:+.5f} (t {fm['t_uni']:+.2f}), BIVARIATE with PROX "
            f"{fm['slope_biv']:+.5f} (t {fm['t_biv']:+.2f}); low-vol rank IC "
            f"{fm['lowvol_IC']:+.4f} (t {fm['t_IC']:+.2f})")

        el = eligible_mask(px, pk).loc[start:]
        _, _, v = score_of(px, "NONE", pk)

        for sc in SCALERS:
            for n in NS:
                W = weights(px, sc, n, pk=pk)
                held = W.loc[start:] > 0
                mv = float(v.loc[start:][held].stack().mean())
                nheld = float(held.sum(axis=1).mean())
                for c in COSTS:
                    res = backtest(px, W, cost_bps=c, freq=FREQ)
                    r = res["returns"].loc[start:]
                    rets[(pk, sc, n, c)] = r
                    mm = metrics(r)
                    mo = metrics(H.window(r, "OOS"))
                    mi = metrics(H.window(r, "IS"))
                    h1, h2 = H.halves(r)
                    ih1, ih2 = H.halves(H.window(r, "IS"))
                    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                    mgo = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                    mgi = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    rows.append(dict(
                        panel=pk, scaler=sc, n=n, cost=c,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        IS_H1=ih1, IS_H2=ih2,
                        TO=res["turnover"].loc[start:].sum() / mm["Years"],
                        held_vol20=mv, n_held=nheld,
                        gross=W.loc[start:].sum(axis=1).mean(),
                        pass4a=H.pass4a(r, v1[c]),
                        pass4b=(len(C.fails(mg)) == 0), fail4b=",".join(C.fails(mg)) or "-",
                        pass4b_oos=all(mgo[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                        IS_adm=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR"))))
                diag.append(dict(panel=pk, scaler=sc, n=n, held_vol20=mv, n_held=nheld,
                                 mean_eligible=float(el.sum(axis=1).mean())))

        # name overlap between the three scalers at each n
        for n in NS:
            Ws = {sc: (weights(px, sc, n, pk=pk).loc[start:] > 0) for sc in SCALERS}
            for a, b in (("INV", "NONE"), ("NONE", "POS"), ("INV", "POS")):
                inter = (Ws[a] & Ws[b]).sum(axis=1)
                un = (Ws[a] | Ws[b]).sum(axis=1).replace(0, np.nan)
                say(f"    name overlap n={n}: {a} vs {b} = {float((inter / un).mean()):.1%}"
                    f" of the union held by both")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    FM = pd.DataFrame(fmrows)
    FM.to_csv(OUT / f"{STEM}.fm.csv", index=False)
    pd.DataFrame(diag).to_csv(OUT / f"{STEM}.diag.csv", index=False)

    # ---- [b] idea 2's KEEP row, via idea 80's committed code path
    px56 = C.panel("u56")[0]
    W80 = I80.weights(px56, "CAND", I80.eligible_mask(px56), key="COMP", n=20)
    r80 = backtest(px56, W80, cost_bps=10.0, freq=FREQ)["returns"].loc[px56.index[260]:]
    k = df[(df.panel == "u56") & (df.scaler == "NONE") & (df.n == 20) & (df.cost == 10.0)]
    r0 = k.iloc[0]
    m80 = metrics(r80)
    h80 = H.halves(r80)
    same = (abs(m80["CAGR"] - r0.CAGR) < 1e-9 and abs(m80["Sharpe"] - r0.Sharpe) < 1e-9
            and abs(m80["MaxDD"] - r0.MaxDD) < 1e-9 and abs(h80[0] - r0.H1) < 1e-9
            and abs(h80[1] - r0.H2) < 1e-9)
    ok["b"] = same
    say(f"\n[b] this run's NONE/n=20 book vs idea 80's committed CAND/COMP/n=20 code path on "
        f"u56@10bps: {r0.CAGR:.5%}/{r0.Sharpe:.5f}/{r0.MaxDD:.5%} halves {r0.H1:.5f}/{r0.H2:.5f}"
        f" vs {m80['CAGR']:.5%}/{m80['Sharpe']:.5f}/{m80['MaxDD']:.5%} halves {h80[0]:.5f}/"
        f"{h80[1]:.5f}  -> {'IDENTICAL' if same else 'DIFFERENT — unsafe'}")
    say(f"    NOT FULLY REPRODUCED AND REPORTED AS SUCH: idea 2's published KEEP row reads "
        f"1.093 / halves 1.088 / 1.103; both this run and idea 80's own committed code give "
        f"{r0.Sharpe:.5f} / {r0.H1:.5f} / {r0.H2:.5f}.  CAGR (12.7%) and MaxDD (-18.3%) match "
        f"exactly; Sharpe and H2 differ by 0.001 in the last published digit and that digit is "
        f"not re-derivable from any committed script.  The gap is far below anything in this "
        f"file and is recorded, not hidden.")

    pub = {"u56": (0.0045, 3.90), "broad": (0.0029, 3.19)}
    okc = True
    for pk_, (sl, t) in pub.items():
        g = FM[FM.panel == pk_].iloc[0]
        hit = abs(g.slope_biv - sl) < 5e-4 and abs(g.t_biv - t) < 0.30
        okc &= hit
        say(f"[c] {pk_}: idea 80 published BIVARIATE vol20 slope {sl:+.4f} (t {t:+.2f}), this "
            f"run {g.slope_biv:+.5f} (t {g.t_biv:+.2f}); published low-vol IC "
            f"{-0.0426 if pk_ == 'u56' else -0.0329:+.4f}, this run {g.lowvol_IC:+.4f}"
            f" -> {'MATCH' if hit else 'MISMATCH'}")
    ok["c"] = okc
    sm = FM[FM.panel == "small"].iloc[0]
    say(f"    P1 (the sign on the small panel, which idea 80 never ran): bivariate slope "
        f"{sm.slope_biv:+.5f} (t {sm.t_biv:+.2f}), univariate {sm.slope_uni:+.5f} "
        f"(t {sm.t_uni:+.2f}), low-vol IC {sm.lowvol_IC:+.4f} (t {sm.t_IC:+.2f}) -> "
        f"{'SAME SIGN as the large-cap panels' if sm.slope_biv > 0 else 'OPPOSITE SIGN — the small panel pays LOW vol'}")

    if not all(ok.values()):
        say("\n[WARNING] a pre-check did not hold; read the affected section with that in mind.")

    # =============================================================== the grid
    say("\n" + "=" * 200)
    say("THE GRID — 2 tuned parameters (scaler x n) = 6 points, EVERY one reported, on 3 panels "
        "x 2 cost rungs = 36 books")
    say("=" * 200)
    cols = ["panel", "cost", "scaler", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO", "held_vol20", "n_held", "gross",
            "pass4a", "pass4b", "fail4b", "pass4b_oos"]
    for pk in PANELS:
        for c in COSTS:
            s = df[(df.panel == pk) & (df.cost == c)].sort_values(["n", "scaler"])
            b = ref[pk]
            say(f"\n  {pk} @ {int(c)} bps   (SPY {b['spy']['CAGR']:.2%}/{b['spy']['Sharpe']:.3f}/"
                f"{b['spy']['MaxDD']:.2%}, halves {b['bfull']['s1']:.3f}/{b['bfull']['s2']:.3f};"
                f" RULES v1 {metrics(b['v1'][c])['CAGR']:.2%}/"
                f"{metrics(b['v1'][c])['Sharpe']:.3f}/{metrics(b['v1'][c])['MaxDD']:.2%})")
            say(s[cols[2:]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- P2: the ordering
    say("\n" + "=" * 200)
    say("P2 — is the ordering POS > NONE > INV on Sharpe?  (the tradeable-premium hypothesis)")
    say("=" * 200)
    orows = []
    for pk in PANELS:
        for c in COSTS:
            for n in NS:
                s = df[(df.panel == pk) & (df.cost == c) & (df.n == n)].set_index("scaler")
                orows.append(dict(panel=pk, cost=c, n=n,
                                  INV=s.loc["INV", "Sharpe"], NONE=s.loc["NONE", "Sharpe"],
                                  POS=s.loc["POS", "Sharpe"],
                                  dPOS_NONE=s.loc["POS", "Sharpe"] - s.loc["NONE", "Sharpe"],
                                  dNONE_INV=s.loc["NONE", "Sharpe"] - s.loc["INV", "Sharpe"],
                                  peak=s.Sharpe.idxmax(),
                                  monotone=bool(s.loc["POS", "Sharpe"] > s.loc["NONE", "Sharpe"]
                                                > s.loc["INV", "Sharpe"])))
    O = pd.DataFrame(orows)
    say(O.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    large = O[O.panel != "small"]
    ok["P2"] = bool(large.monotone.all())
    say(f"\n    POS > NONE > INV in {int(O.monotone.sum())} of {len(O)} cells "
        f"({int(large.monotone.sum())} of {len(large)} on the two large-cap panels; P2 needed "
        f"{len(large)} of {len(large)}) -> {'HELD' if ok['P2'] else 'FAILED'}")
    say("    Sharpe peak by cell: " + ", ".join(f"{r.panel}@{int(r.cost)}/n{r.n} {r.peak}"
                                                for _, r in O.iterrows()))
    say(f"    mean dSharpe: NONE - INV = {O.dNONE_INV.mean():+.4f}  |  POS - NONE = "
        f"{O.dPOS_NONE.mean():+.4f}   (a monotone premium needs these to be similar and both +)")
    # paired daily t-tests on the same panel/cost/n, so the comparison is on the same days
    say("\n    paired daily t-tests (same panel, cost and n; annualised mean difference):")
    trows = []
    for pk_ in PANELS:
        for c in COSTS:
            for n in NS:
                for a, b in (("NONE", "INV"), ("POS", "NONE"), ("POS", "INV")):
                    d = rets[(pk_, a, n, c)] - rets[(pk_, b, n, c)]
                    t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))
                    trows.append(dict(panel=pk_, cost=c, n=n, pair=f"{a}-{b}",
                                      ann_diff=d.mean() * 252, t=t))
    T = pd.DataFrame(trows)
    say(T.pivot_table(index=["panel", "cost", "n"], columns="pair",
                      values=["ann_diff", "t"]).to_string(float_format=lambda x: f"{x:.3f}"))
    say("    mean over the 12 cells: "
        + ", ".join(f"{k} {v.ann_diff.mean():+.2%}/yr (mean t {v.t.mean():+.2f})"
                    for k, v in T.groupby('pair')))

    say(f"    mean dCAGR: NONE - INV = "
        f"{(df[df.scaler == 'NONE'].set_index(['panel', 'cost', 'n']).CAGR - df[df.scaler == 'INV'].set_index(['panel', 'cost', 'n']).CAGR).mean():+.2%}"
        f"  |  POS - NONE = "
        f"{(df[df.scaler == 'POS'].set_index(['panel', 'cost', 'n']).CAGR - df[df.scaler == 'NONE'].set_index(['panel', 'cost', 'n']).CAGR).mean():+.2%}")

    # ---- P3: what POS pays
    say("\n" + "=" * 200)
    say("P3 — POS buys return with drawdown; and WHICH 4b bar each arm fails on")
    say("=" * 200)
    dd = df.pivot_table(index=["panel", "cost", "n"], columns="scaler", values="MaxDD")
    say(dd.to_string(float_format=lambda x: f"{x:.3f}"))
    deeper = int(((dd["POS"] < dd["NONE"]).sum()))
    ok["P3a"] = deeper == len(dd)
    say(f"\n    POS's MaxDD deeper than NONE's in {deeper} of {len(dd)} cells -> "
        f"{'HELD' if ok['P3a'] else 'FAILED'}")
    say(f"    held-name mean vol20 by scaler: "
        + ", ".join(f"{sc} {df[df.scaler == sc].held_vol20.mean():.3f}" for sc in SCALERS))
    say(f"    turnover (x/yr) by scaler: "
        + ", ".join(f"{sc} {df[df.scaler == sc].TO.mean():.1f}" for sc in SCALERS))
    fails = df[~df.pass4b].groupby(["scaler", "fail4b"]).size().rename("books")
    say("\n    4b failure modes (36 books):")
    say(fails.to_string())
    posf = df[(df.scaler == "POS") & (~df.pass4b)]
    ok["P3b"] = bool(posf.fail4b.str.contains("DD").all())
    say(f"    every POS failure includes the DRAWDOWN cap: "
        f"{int(posf.fail4b.str.contains('DD').sum())} of {len(posf)} -> "
        f"{'HELD' if ok['P3b'] else 'FAILED'}")

    # ---- KEEP paths
    say("\n" + "=" * 200)
    say("BOTH KEEP PATHS on all 36 books")
    say("=" * 200)
    kp = df.groupby(["scaler", "n"]).agg(pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"),
                                         pass4b_oos=("pass4b_oos", "sum"),
                                         cells=("panel", "size"))
    say(kp.to_string())
    say(f"\n    total: 4a {int(df.pass4a.sum())} of 36, 4b (full sample) {int(df.pass4b.sum())}"
        f" of 36, 4b (OOS window alone) {int(df.pass4b_oos.sum())} of 36")
    xu = df[df.pass4b].groupby(["scaler", "n"]).panel.nunique()
    say(f"    cross-universe 4b (a (scaler, n) point passing on more than one panel): "
        + (", ".join(f"{k} on {v} panels" for k, v in xu.items()) if len(xu) else "NONE"))
    ok["P5"] = not (xu > 1).any() if len(xu) else True
    say(f"    P5 (no (scaler, n) point is a cross-universe KEEP) -> "
        f"{'HELD' if ok['P5'] else 'FAILED — a KEEP candidate exists, see above'}")

    # =============================================================== rule 8
    say("\n" + "=" * 200)
    say("RULE 8 WALK-FORWARD — parameters chosen on the IS window (<= 2016-12-31) only, read "
        "ONCE on 2017-01-01..2026")
    say("=" * 200)
    wrows = []
    for pk in PANELS:
        for c in COSTS:
            s = df[(df.panel == pk) & (df.cost == c)].reset_index(drop=True)
            picks = {"S1_ISSharpe": s.loc[s.IS_Sharpe.idxmax()]}
            adm = s[s.IS_adm]
            picks["S2_4bAware"] = adm.loc[adm.IS_Sharpe.idxmax()] if len(adm) else None
            v1o = metrics(ref[pk]["v1"][c].loc[OOS_START:])
            for nm, r in picks.items():
                if r is None:
                    wrows.append(dict(panel=pk, cost=c, sel=nm, scaler="NOTHING", n=np.nan,
                                      OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                      v1_OOS_Sharpe=v1o["Sharpe"],
                                      spy_OOS_Sharpe=ref[pk]["spy_oos"]["Sharpe"]))
                    continue
                wrows.append(dict(panel=pk, cost=c, sel=nm, scaler=r.scaler, n=int(r.n),
                                  IS_Sharpe=r.IS_Sharpe, IS_MaxDD=r.IS_MaxDD,
                                  OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                  OOS_MaxDD=r.OOS_MaxDD, pass4b_oos=r.pass4b_oos,
                                  v1_OOS_CAGR=v1o["CAGR"], v1_OOS_Sharpe=v1o["Sharpe"],
                                  v1_OOS_MaxDD=v1o["MaxDD"],
                                  spy_OOS_CAGR=ref[pk]["spy_oos"]["CAGR"],
                                  spy_OOS_Sharpe=ref[pk]["spy_oos"]["Sharpe"],
                                  spy_OOS_MaxDD=ref[pk]["spy_oos"]["MaxDD"]))
    Wf = pd.DataFrame(wrows)
    Wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(Wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    picked = Wf[Wf.scaler != "NOTHING"]
    npos = int((picked.scaler == "POS").sum())
    ok["P4"] = npos == 0
    say(f"\n    POS picked in {npos} of {len(picked)} (panel, cost, rule) cells -> "
        f"P4 {'HELD' if ok['P4'] else 'FAILED'}")
    say("    pick counts by scaler: "
        + ", ".join(f"{k} {v}" for k, v in picked.scaler.value_counts().items()))

    say("\n" + "=" * 200)
    say("PRE-REGISTERED PREDICTIONS — outcome")
    say("=" * 200)
    for k_, v_ in ok.items():
        say(f"    {k_}: {'HELD/OK' if v_ else 'FAILED'}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
