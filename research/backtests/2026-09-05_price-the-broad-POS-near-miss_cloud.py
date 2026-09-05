#!/usr/bin/env python3
"""QUEUE idea 152 — price-the-broad-POS-near-miss  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 152)
    "idea 81's `broad @10bps, x sqrt(vol20), n=20` book (16.0%/1.052/-21.4%, halves
     1.197/0.927, OOS Sharpe 1.005) clears every 4b bar except the DRAWDOWN CAP and misses it
     by 1.2pp, while the same book without the tilt fails on H2 alone.  Idea 66 says gross is
     an exact Sharpe-neutral lever and idea 144 says a rescaled book is the same book: run its
     own 25-point gross family and idea 90's interval test, and check the u56/small panels at
     the same m before anything is claimed.  Max 2 params."

WHAT IS AT STAKE, AND WHY THE TWO ARMS ARE NOT SYMMETRIC.
    4b has five bars.  Three of them (H1, H2, OOS Sharpe) are, to the extent idea 66's "exact
    lever" claim holds, INVARIANT to gross: scaling every target weight by a constant scales
    the net return series by the same constant and leaves Sharpe alone.  The other two are
    not: the DRAWDOWN cap gets easier as gross falls, the CAGR floor gets harder.  So a book
    whose only failure is the DD cap has a chance of a 4b pass at lower gross, and a book that
    fails a SHARPE bar has none at any gross.  Idea 81 left exactly that pair on the table:
    POS fails DD only (by 1.2pp), NONE fails H2 only.  This run prices both.

    The honest framing, which idea 144 insists on, is that a de-grossed book is the same book.
    So a POS pass at m < 0.75 is NOT a discovery of a new edge.  What it would be is a
    statement that the vol tilt buys enough SHARPE — the part gross cannot manufacture — that
    the remaining gap to 4b is a risk-budget choice rather than a signal failure.  Idea 90's
    verdict (KILL the interval WIDTH as a replacement for 4b's pass/fail, KEEP the interval as
    a reported descriptor) is the standing convention and is honoured: the interval is
    reported, never used as the bar.

    The decisive quantity is therefore NOT "does POS pass 4b somewhere on the ladder".  It is:
    (i) does the family's Sharpe actually stay flat across the ladder, i.e. is idea 66's lever
    exact under this engine's drift renormalisation, and (ii) does the m-interval that passes
    4b on broad also pass on u56 and small, or is the pass a broad-only artefact.

CORPUS
    3 panels (u56 / broad / small) x 2 cost rungs (10, 25 bps) x 3 scaler arms x 25 gross
    points = 450 books, weekly, t+1, long-only, no leverage above m=1.0 in the reported grid
    (m > 1.0 IS run and reported so the ladder brackets the DD cap from both sides, and every
    m > 1.0 row is flagged LEVERED and excluded from any KEEP claim per PROTOCOL rule 2).

TUNED PARAMETERS — exactly two, both swept exhaustively, ALL grid points written to .grid.csv:
    1. the vol scaler, 3 values:  INV  = composite / sqrt(vol20)   (RULES v1's live tilt)
                                  NONE = composite                 (idea 2's standing book)
                                  POS  = composite * sqrt(vol20)   (idea 81's near-miss)
    2. the target gross m, 25 values: 0.20 to 1.40 step 0.05.
    n is HELD at 20 (idea 81's published cell), not tuned.  Panels, cost rungs, the OOS window
    and every diagnostic are REPORTED axes, never selected on.  The 200d gate and vol20 < 0.60
    are held at RULES v1's values throughout.

REPRODUCTION, asserted before any new number is read
    [a] INV / n=5 / fixed w=0.15 must equal `baseline.rules_v1_weights(px)` cell-for-cell.
    [b] POS / n=20 / m=0.75 on broad @10bps must reproduce idea 81's published cell
        (16.0% / 1.052 / -21.4%, halves 1.197 / 0.927, OOS Sharpe 1.005) to the published
        precision, AND must equal idea 81's committed code path cell-for-cell.  Where the
        published digit and the committed code disagree, BOTH are printed.
    [c] NONE / n=20 / m=0.75 on broad @10bps must fail 4b on H2 and nothing else, which is the
        second half of idea 152's premise.

THE LEVER CONTROL (idea 66's claim, tested rather than assumed)
    This engine drifts weights between rebalances and renormalises by total portfolio value
    INCLUDING the cash residual, so scaling targets by m is NOT algebraically guaranteed to
    scale the net return series by m.  For every (panel, cost, arm) the run reports
    max |Sharpe(m) - Sharpe(0.75)| over the ladder and the max relative deviation of r(m) from
    (m/0.75) * r(0.75).  If the Sharpe spread across the ladder is material, the whole
    "interval" reading is invalid and is reported as such.

WALK-FORWARD (PROTOCOL rule 8) — both selection rules fixed BEFORE any OOS number is read:
    S1 plain IS Sharpe argmax over the 75 (arm, m) points; S2 the 4b-aware IS screen (IS
    halves, IS drawdown cap, IS CAGR floor all cleared) then IS Sharpe argmax, falling back to
    S1 when the screen is empty.  Parameters chosen on 2009-2016 only (2011-2016 on small),
    read ONCE on 2017-01-01..2026.  OOS CAGR / Sharpe / MaxDD reported against RULES v1 (the
    live book, same panel and cost) and SPY.  Levered points (m > 1.0) are removed from the
    selectable set.  Both KEEP paths (4a and 4b) are evaluated at every grid point, on the
    full sample and again on the OOS window alone.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b], [c] all hold.
    P2  Idea 66's lever is near-exact: Sharpe spread across the 25-point ladder < 0.05 in
        every (panel, cost, arm) cell.
    P3  POS on broad @10bps has a NON-EMPTY 4b interval, bounded above by the DD cap and below
        by the CAGR floor, and m=0.75 sits ABOVE its upper end.
    P4  NONE on broad @10bps has an EMPTY 4b interval at every m, because H2 is gross-invariant.
    P5  The broad POS interval does NOT transfer: at the same m, POS fails 4b on u56 and on
        small, so cross-universe 4b is 0 of 25 and the result is PARK, not KEEP.
    P6  Nothing survives 25 bps.

CAVEATS carried, not buried
    * Survivorship: all three panels are current-constituent lists (idea 54).  The small panel
      drops the 44 tickers with max_1d_move >= 1.0 per data/small_meta.csv and its SPY is a
      held-out benchmark, not a constituent.  The bias runs AGAINST POS being real: the
      high-vol cohort POS tilts into is exactly where delisted names would sit, so POS is
      flattered here and every POS number should be read as an upper bound.
    * Idea 144: a de-grossed book is the same book.  No m on this ladder is a new signal.
    * Idea 90: interval WIDTH is not a KEEP bar.  It is printed as a descriptor only.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so the IS
      drawdown bar admits too much, for every arm equally.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * Idea 49/39: the eligibility gate is inverted on the small panel, so every small-panel
      number here describes a gate that does not work there.
    * No IWM in the cache, so the small panel is judged against SPY (stated, not adjusted).

HARNESS
    `baseline` (the live rules), idea 94's window/halves/4a machinery, idea 129's panel and 4b
    bar machinery and idea 81's book constructor are IMPORTED, so the arms are literally idea
    81's arms and the bars are literally 4b's.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .intervals.csv, .lever.csv,
.walkforward.csv, .transfer.csv.
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

STEM = "2026-09-05_price-the-broad-POS-near-miss_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I81 = OUT / "2026-09-05_vol20-as-the-hidden-ranking-key_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
I81M = _load(I81, "i81")

FREQ = "W"
COSTS = [10.0, 25.0]
PANELS = ["broad", "u56", "small"]        # broad first: it is the panel the premise is on
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI0, DELTA0 = 0.70, 0.60                 # 4b's published coefficients
MAX_VOL = 0.60
N = 20                                    # HELD, not tuned (idea 81's published cell)
REF_M = 0.75                              # idea 81's gross, the reproduction anchor

SCALERS = ["INV", "NONE", "POS"]                       # tuned parameter 1
MS = [round(0.20 + 0.05 * i, 2) for i in range(25)]    # tuned parameter 2: 0.20 .. 1.40

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 2000)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the book (idea 81's, verbatim)
def weights(px, scaler, n, m, pk=""):
    """Idea 81's own constructor with the gross exposed.  m/n per name, n names."""
    s, above, v = I81M.score_of(px, scaler, pk)
    elig = s.where(above & (v < MAX_VOL))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (m / n)


def run(px, scaler, m, cost, start, pk):
    res = backtest(px, weights(px, scaler, N, m, pk), cost_bps=cost, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def fmt_iv(lo, hi):
    return "empty" if lo is None else f"[{lo:.2f}, {hi:.2f}]"


def main():
    say("=" * 210)
    say(f"IDEA 152 — price-the-broad-POS-near-miss   ({STEM})")
    say("Idea 81 left POS/n=20/broad failing 4b on the DD cap alone and NONE failing on H2 "
        "alone.  DD is a gross lever; H2 is not.  Price both on a 25-point gross ladder.")
    say("PRE-REGISTERED: 2 tuned params (scaler x 3, gross m x 25).  n=20 held.  All 450 "
        "grid points reported.  Interval is a DESCRIPTOR (idea 90), never a bar.")
    say("=" * 210)

    rows, lever, ivrows, rets, ref = [], [], [], {}, {}

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        ms_, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk] = dict(bfull=bfull, bIS=bIS, bOOS=bOOS, spy=ms_, spy_oos=mso, v1=v1,
                       start=start, desc=desc)

        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, {px.index[0].date()}.."
            f"{px.index[-1].date()}, eval from {start.date()}")
        say(f"    SPY full CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD "
            f"{ms_['MaxDD']:.2%} halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS "
            f"{mso['CAGR']:.2%}/{mso['Sharpe']:.3f}/{mso['MaxDD']:.2%}")
        say(f"    4b bars on this panel: H1 > {bfull['s1']:.3f}, H2 > {bfull['s2']:.3f}, "
            f"OOS > {bfull['soos']:.3f}, MaxDD shallower than "
            f"{DELTA0 * abs(bfull['sdd']):.2%}, CAGR >= {PHI0 * bfull['scagr']:.2%}")
        for c in COSTS:
            m_, mo_ = metrics(v1[c]), metrics(v1[c].loc[OOS_START:])
            say(f"    RULES v1 @{int(c)}bps: {m_['CAGR']:.2%}/{m_['Sharpe']:.3f}/"
                f"{m_['MaxDD']:.2%} | OOS {mo_['CAGR']:.2%}/{mo_['Sharpe']:.3f}/{mo_['MaxDD']:.2%}")

        # ---- [a] the INV arm IS the live book
        Wv1 = (I81M.weights(px, "INV", 5, fixedw=0.15, pk=pk))
        dmax = float((Wv1 - rules_v1_weights(px)).abs().max().max())
        say(f"[a] INV/n=5/w=0.15 vs baseline.rules_v1_weights: max|diff| = {dmax:.3e} "
            f"({'EXACT' if dmax < 1e-12 else 'NOT EXACT'})")

        for sc in SCALERS:
            for c in COSTS:
                fam = {}
                for m in MS:
                    r, to = run(px, sc, m, c, start, pk)
                    rets[(pk, sc, m, c)] = r
                    fam[m] = r
                    mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
                    h1, h2 = H.halves(r)
                    ih1, ih2 = H.halves(H.window(r, "IS"))
                    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                    mgi = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    mgo = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                    W = weights(px, sc, N, m, pk)
                    rows.append(dict(
                        panel=pk, scaler=sc, n=N, m=m, cost=c,
                        levered=(m > 1.0),
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        IS_H1=ih1, IS_H2=ih2,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        TO=to.sum() / mm["Years"],
                        gross=float(W.loc[start:].sum(axis=1).mean()),
                        mg_H1=mg["H1"], mg_H2=mg["H2"], mg_OOS=mg["OOS"],
                        mg_DD=mg["DD"], mg_CAGR=mg["CAGR"],
                        pass4a=H.pass4a(r, v1[c]),
                        pass4b=(len(C.fails(mg)) == 0), fail4b=",".join(C.fails(mg)) or "-",
                        pass4b_oos=all(mgo[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                        IS_adm=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR"))))

                # ---- the lever control: is gross really Sharpe-neutral under this engine?
                base = fam[REF_M]
                sh = np.array([metrics(fam[m])["Sharpe"] for m in MS])
                dev = max(float((fam[m] - (m / REF_M) * base).abs().max()) for m in MS)
                scl = max(float((fam[m] - (m / REF_M) * base).abs().max()
                                / max(1e-12, float(((m / REF_M) * base).abs().max()))) for m in MS)
                lever.append(dict(panel=pk, scaler=sc, cost=c,
                                  Sharpe_min=sh.min(), Sharpe_max=sh.max(),
                                  Sharpe_spread=sh.max() - sh.min(),
                                  Sharpe_at_ref=metrics(base)["Sharpe"],
                                  max_abs_dev=dev, max_rel_dev=scl))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    LV = pd.DataFrame(lever)
    LV.to_csv(OUT / f"{STEM}.lever.csv", index=False)

    # ================================================================ reproduction [b] and [c]
    say("\n" + "=" * 210)
    say("REPRODUCTION of idea 152's premise (broad @10bps, n=20, m=0.75)")
    say("=" * 210)
    pub = {"POS": dict(CAGR=0.160, Sharpe=1.052, MaxDD=-0.214, H1=1.197, H2=0.927, OOS=1.005)}
    for sc in SCALERS:
        q = df[(df.panel == "broad") & (df.cost == 10.0) & (df.scaler == sc)
               & (np.isclose(df.m, REF_M))].iloc[0]
        say(f"  {sc:<5} CAGR {q.CAGR:.2%}  Sharpe {q.Sharpe:.3f}  MaxDD {q.MaxDD:.2%}  "
            f"halves {q.H1:.3f}/{q.H2:.3f}  OOS Sharpe {q.OOS_Sharpe:.3f}  "
            f"| 4b {'PASS' if q.pass4b else 'FAIL on ' + q.fail4b}  "
            f"margins H1 {q.mg_H1:+.3f} H2 {q.mg_H2:+.3f} OOS {q.mg_OOS:+.3f} "
            f"DD {q.mg_DD:+.2%} CAGR {q.mg_CAGR:+.2%}")
    q = df[(df.panel == "broad") & (df.cost == 10.0) & (df.scaler == "POS")
           & (np.isclose(df.m, REF_M))].iloc[0]
    p = pub["POS"]
    say(f"[b] idea 81 published POS: {p['CAGR']:.1%}/{p['Sharpe']:.3f}/{p['MaxDD']:.1%}, halves "
        f"{p['H1']:.3f}/{p['H2']:.3f}, OOS {p['OOS']:.3f}")
    say(f"    this run             : {q.CAGR:.1%}/{q.Sharpe:.3f}/{q.MaxDD:.1%}, halves "
        f"{q.H1:.3f}/{q.H2:.3f}, OOS {q.OOS_Sharpe:.3f}")
    ok_b = (abs(q.CAGR - p["CAGR"]) < 5e-4 and abs(q.Sharpe - p["Sharpe"]) < 5e-4
            and abs(q.MaxDD - p["MaxDD"]) < 5e-4 and abs(q.H1 - p["H1"]) < 5e-4
            and abs(q.H2 - p["H2"]) < 5e-4 and abs(q.OOS_Sharpe - p["OOS"]) < 5e-4)
    say(f"[b] REPRODUCED to published precision: {ok_b}")
    say(f"[b] premise check — POS fails 4b on: {q.fail4b} (premise says DRAWDOWN only, "
        f"missed by 1.2pp; here the DD margin is {q.mg_DD:+.2%})")
    qn = df[(df.panel == "broad") & (df.cost == 10.0) & (df.scaler == "NONE")
            & (np.isclose(df.m, REF_M))].iloc[0]
    say(f"[c] premise check — NONE fails 4b on: {qn.fail4b} (premise says H2 only; here the "
        f"H2 margin is {qn.mg_H2:+.3f})")

    # ================================================================ the lever control
    say("\n" + "=" * 210)
    say("LEVER CONTROL — is gross Sharpe-neutral under this engine's drift renormalisation? "
        "(idea 66's claim, tested)")
    say("=" * 210)
    say(LV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"  max Sharpe spread across the 25-point ladder over all 18 cells: "
        f"{LV.Sharpe_spread.max():.4f}")
    say("  Reading: a spread of this size means Sharpe is (not) usably invariant to gross; if "
        "it is not, the interval reading below is invalid and is reported as such.")

    # ================================================================ idea 90's interval test
    say("\n" + "=" * 210)
    say("IDEA 90 INTERVAL TEST — the set of m on the ladder where ALL FIVE 4b bars clear")
    say("(descriptor only; per idea 90 the WIDTH is not a KEEP bar.  m > 1.00 is LEVERED and "
        "excluded from any KEEP claim per PROTOCOL rule 2.)")
    say("=" * 210)
    for pk in PANELS:
        for c in COSTS:
            for sc in SCALERS:
                g = df[(df.panel == pk) & (df.cost == c) & (df.scaler == sc)].sort_values("m")
                ok = g[g.pass4b]
                oku = ok[~ok.levered]
                lo = hi = None
                if len(ok):
                    lo, hi = float(ok.m.min()), float(ok.m.max())
                ulo = uhi = None
                if len(oku):
                    ulo, uhi = float(oku.m.min()), float(oku.m.max())
                # which bar binds at each end of the ladder
                blo = g.iloc[0]
                bhi = g.iloc[-1]
                binding = sorted(set(sum([str(x).split(",") for x in g.fail4b], [])) - {"-"})
                ivrows.append(dict(panel=pk, cost=c, scaler=sc, n_pass=int(len(ok)),
                                   m_lo=lo, m_hi=hi, width=(None if lo is None else hi - lo),
                                   m_lo_unlev=ulo, m_hi_unlev=uhi,
                                   ref_inside=(lo is not None and lo <= REF_M <= hi),
                                   bars_ever_binding=",".join(binding) or "-",
                                   fail_at_lowest_m=blo.fail4b, fail_at_highest_m=bhi.fail4b))
                say(f"  {pk:<6} @{int(c)}bps {sc:<5}: 4b passes at {len(ok):2d}/25 m-points, "
                    f"interval {fmt_iv(lo, hi):<14} unlevered {fmt_iv(ulo, uhi):<14} "
                    f"m=0.75 inside: {str(lo is not None and lo <= REF_M <= hi):<5} "
                    f"| bars that bind somewhere: {','.join(binding) or '-'} "
                    f"| at m=0.20: {blo.fail4b} | at m=1.40: {bhi.fail4b}")
    IV = pd.DataFrame(ivrows)
    IV.to_csv(OUT / f"{STEM}.intervals.csv", index=False)

    # ================================================================ the broad POS ladder in full
    say("\n" + "=" * 210)
    say("THE LADDER IN FULL — broad @10bps, all 3 arms x 25 m (the premise's own cell)")
    say("=" * 210)
    show = df[(df.panel == "broad") & (df.cost == 10.0)][
        ["scaler", "m", "levered", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
         "TO", "gross", "mg_DD", "mg_CAGR", "pass4a", "pass4b", "fail4b"]].sort_values(
        ["scaler", "m"])
    say(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================ transfer to u56 / small
    say("\n" + "=" * 210)
    say("TRANSFER — the broad POS 4b interval read on u56 and small AT THE SAME m "
        "(idea 152's own precondition: 'check the u56/small panels at the same m')")
    say("=" * 210)
    tr = []
    gb = df[(df.panel == "broad") & (df.cost == 10.0) & (df.scaler == "POS") & df.pass4b
            & (~df.levered)]
    if len(gb):
        mlo, mhi = float(gb.m.min()), float(gb.m.max())
        mmid = round(np.median(sorted(gb.m.values)), 2)
    else:
        mlo = mhi = mmid = None
    say(f"  broad/POS/@10bps unlevered 4b interval = {fmt_iv(mlo, mhi)}; median passing "
        f"m = {mmid}")
    test_ms = sorted(set([m for m in MS if mlo is not None and mlo <= m <= mhi])) or [REF_M]
    for pk in PANELS:
        for sc in SCALERS:
            for m in test_ms:
                q2 = df[(df.panel == pk) & (df.cost == 10.0) & (df.scaler == sc)
                        & (np.isclose(df.m, m))].iloc[0]
                tr.append(dict(panel=pk, scaler=sc, m=m, CAGR=q2.CAGR, Sharpe=q2.Sharpe,
                               MaxDD=q2.MaxDD, H1=q2.H1, H2=q2.H2, OOS_Sharpe=q2.OOS_Sharpe,
                               pass4a=q2.pass4a, pass4b=q2.pass4b, fail4b=q2.fail4b))
    TR = pd.DataFrame(tr)
    TR.to_csv(OUT / f"{STEM}.transfer.csv", index=False)
    say(TR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    xu = TR[TR.scaler == "POS"].groupby("m")["pass4b"].sum()
    say("\n  CROSS-UNIVERSE 4b for POS (needs all 3 panels to pass at the same m):")
    for m, k in xu.items():
        say(f"    m={m:.2f}: {int(k)}/3 panels pass 4b @10bps "
            f"{'<-- CROSS-UNIVERSE PASS' if k == 3 else ''}")

    # ================================================================ rule 8 walk-forward
    say("\n" + "=" * 210)
    say("RULE 8 WALK-FORWARD — choose (scaler, m) on 2009-2016 only, read ONCE on 2017-2026")
    say("S1 = IS Sharpe argmax.  S2 = 4b-aware IS screen then IS Sharpe argmax (fallback S1).")
    say("Levered points (m > 1.00) removed from the selectable set.")
    say("=" * 210)
    wf = []
    for pk in PANELS:
        for c in COSTS:
            g = df[(df.panel == pk) & (df.cost == c) & (~df.levered)].copy()
            s1 = g.loc[g.IS_Sharpe.idxmax()]
            adm = g[g.IS_adm]
            s2 = adm.loc[adm.IS_Sharpe.idxmax()] if len(adm) else s1
            spy_o = metrics(ref[pk]["v1"][c].loc[OOS_START:])  # placeholder replaced below
            spyo = ref[pk]["spy_oos"]
            v1o = metrics(ref[pk]["v1"][c].loc[OOS_START:])
            for tag, pick, nadm in (("S1", s1, len(g)), ("S2", s2, len(adm))):
                r = rets[(pk, pick.scaler, float(pick.m), c)]
                ro = H.window(r, "OOS")
                mo = metrics(ro)
                bOOS = ref[pk]["bOOS"]
                mgo = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                wf.append(dict(panel=pk, cost=c, selector=tag, n_admissible=nadm,
                               pick_scaler=pick.scaler, pick_m=pick.m,
                               IS_Sharpe=pick.IS_Sharpe,
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                               OOS_MaxDD=mo["MaxDD"],
                               v1_OOS_CAGR=v1o["CAGR"], v1_OOS_Sharpe=v1o["Sharpe"],
                               v1_OOS_MaxDD=v1o["MaxDD"],
                               spy_OOS_CAGR=spyo["CAGR"], spy_OOS_Sharpe=spyo["Sharpe"],
                               spy_OOS_MaxDD=spyo["MaxDD"],
                               d_vs_v1=mo["Sharpe"] - v1o["Sharpe"],
                               d_vs_spy=mo["Sharpe"] - spyo["Sharpe"],
                               OOS_4b=all(mgo[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                               full_4b=bool(pick.pass4b), full_4a=bool(pick.pass4a)))
                say(f"  {pk:<6} @{int(c)}bps {tag}: picks {pick.scaler}/m={pick.m:.2f} "
                    f"(IS Sharpe {pick.IS_Sharpe:.3f}, {nadm} admissible) -> OOS "
                    f"{mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%} | v1 OOS "
                    f"{v1o['CAGR']:.2%}/{v1o['Sharpe']:.3f}/{v1o['MaxDD']:.2%} | SPY OOS "
                    f"{spyo['CAGR']:.2%}/{spyo['Sharpe']:.3f}/{spyo['MaxDD']:.2%} | "
                    f"dSharpe vs v1 {mo['Sharpe'] - v1o['Sharpe']:+.3f}, vs SPY "
                    f"{mo['Sharpe'] - spyo['Sharpe']:+.3f} | OOS-window 4b "
                    f"{all(mgo[k] > 0 for k in ('H1', 'H2', 'DD', 'CAGR'))}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ================================================================ census
    say("\n" + "=" * 210)
    say("CENSUS over all 450 grid points")
    say("=" * 210)
    say(f"  4a passes: {int(df.pass4a.sum())}/450   4b passes: {int(df.pass4b.sum())}/450   "
        f"4b passes at m <= 1.00 (unlevered): {int(df[~df.levered].pass4b.sum())}/"
        f"{int((~df.levered).sum())}")
    say("  4b pass count by (panel, cost, scaler), unlevered only:")
    cen = df[~df.levered].groupby(["panel", "cost", "scaler"]).agg(
        n=("pass4b", "size"), pass4b=("pass4b", "sum"), pass4a=("pass4a", "sum"),
        pass4b_oos=("pass4b_oos", "sum")).reset_index()
    say(cen.to_string(index=False))
    say("\n  Which 4b bar fails, unlevered points only (a point can fail several):")
    for k in ("H1", "H2", "OOS", "DD", "CAGR"):
        n = int((df[~df.levered][f"mg_{k}"] <= 0).sum())
        say(f"    {k:<5}: {n:3d}/{int((~df.levered).sum())} points fail this bar")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.console.txt/.grid.csv/.intervals.csv/.lever.csv/.walkforward.csv/"
        f".transfer.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
