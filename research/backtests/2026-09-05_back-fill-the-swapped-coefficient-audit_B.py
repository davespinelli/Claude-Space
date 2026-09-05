#!/usr/bin/env python3
"""QUEUE idea 200 — back-fill-the-swapped-coefficient-audit  (lane B, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 200)
    "idea 178's AST audit found 3 of 61 `margins_at` call sites pass (0.60, 0.70) into
     (phi, delta), and showed the defect costs idea 165 rather than flattering it.  Re-run the
     OTHER exposed site (idea 168's line 515 OOS read, 352 books) at the published bars and
     report how many of its published 4b/OOS verdicts move.  Cheap; the answer is a number, and
     it closes the exposure idea 176 opened on a different instrument.  Max 2 params."

WHAT THE DEFECT IS, EXACTLY
    `C.margins_at(r, b, phi, delta, which)` (defined in 2026-09-05_cagr-floor-calibration_B.py
    line 164) returns

        DD   = delta * |SPY MaxDD| - |book MaxDD|          -> delta is the DRAWDOWN CAP coefficient
        CAGR = book CAGR - phi * SPY CAGR                  -> phi   is the CAGR FLOOR coefficient

    PROTOCOL rule 4b states "MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's", i.e.

        CORRECT   phi = 0.70, delta = 0.60
        SWAPPED   phi = 0.60, delta = 0.70      <- what idea 168 line 515 passes

    Both swapped coefficients are LOOSER than the ones PROTOCOL states: the CAGR floor drops
    from 70% to 60% of SPY's CAGR, and the drawdown cap rises from 60% to 70% of SPY's.  So the
    correction can only ever REMOVE passes, never add them.  That is an arithmetic fact about the
    two margins and it is ASSERTED here (M1/M2 below), not assumed: if any book flips FAIL->PASS
    the script fails loudly, because that would mean the defect is not what idea 178 described.

    Note the exposed site is the OOS-WINDOW read only.  Idea 168's headline grid (`pass4b`, the
    352-row grid.csv) goes through `H.margins`, which HARD-CODES 0.60/0.70 in the correct roles.
    The full-sample 4b column of idea 168 is therefore NOT exposed, and this script proves that
    by reproducing it bit-for-bit rather than by inspection.

WHAT IS RE-RUN
    Idea 168's corpus is rebuilt in full by importing its module and calling its own
    `weights_k` / `score_k` — 2 panels x 11 exponents x 8 shares x 2 cost rungs = 352 books,
    weekly, t+1, gross 0.75, PROTOCOL costs at the two published rungs.  Nothing about the books
    changes; the ONLY thing this script varies is the (phi, delta) pair fed to the OOS read.

      [A] THE SITE ITSELF — the 16 walk-forward arm-cells (2 panels x 2 costs x 4 arms) that
          line 515 actually evaluated and that idea 168 published in its .walkforward.csv.
          Reproduced under SWAPPED first (must match the committed file's OOS_4b_fail column
          string-for-string), then re-read under CORRECT.
      [B] THE WHOLE CORPUS — the same OOS-window 4b verdict applied to all 352 books, which is
          the "352 books" idea 200 names.  Idea 168 never published this column; it is computed
          here under both coefficient orders so the exposure is bounded for the whole grid, not
          just the 16 cells the site touched.

    The OOS-window failing-bar set is ("H1","H2","DD","CAGR"), idea 168's own convention at line
    517.  The OOS bar is EXCLUDED because inside the OOS window `soos` IS the window's own Sharpe,
    so that margin is identically 0 and would fail every book by construction.  That convention is
    carried verbatim, not re-decided here.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL 25 grid points reported
    1. phi   (CAGR floor coefficient)      {0.50, 0.60, 0.70, 0.80, 0.90}
    2. delta (drawdown cap coefficient)    {0.40, 0.50, 0.60, 0.70, 0.80}
    PROTOCOL's point (0.70, 0.60) and the defect's point (0.60, 0.70) are both interior grid
    points, so the answer is read off a surface rather than from two isolated evaluations.
    Panel, cost rung, exponent k and share m are CARRIED corpus axes inherited from idea 168 and
    are never selected on.

WHAT WOULD MAKE THIS A KEEP
    Nothing.  This is an audit of a published read, not a book: no new weights function exists in
    this script.  Both KEEP paths are nevertheless evaluated and reported over the 352 books
    (rule 4), and rule 8 walk-forward is re-run in full (rule 8), because idea 200's answer is
    precisely "which walk-forward verdicts move".  The expected verdict is KILL-or-confirm on the
    exposure; a documented "no verdict moves" is the success case.

PRE-REGISTERED PREDICTIONS (written before the run)
    P1  Reproduction of idea 168's committed grid.csv is exact (<= 1e-12) on every numeric column.
    P2  The SWAPPED reproduction of the 16 OOS_4b_fail strings matches the committed file 16/16.
    P3  No book anywhere flips FAIL->PASS under the correction (monotone; arithmetic).
    P4  Among the 16 walk-forward arm-cells, at most 4 verdicts move, and every one that moves is
        a DD-bar loss (the DD cap tightens by 0.10*|SPY OOS MaxDD| ~ 2pp, the CAGR floor by
        0.10*SPY OOS CAGR ~ 1.5pp, and idea 168's OOS drawdowns cluster near the cap).
    P5  Idea 168's published headline sentence — "rule 8's IS-chosen k beats k=0 on OOS Sharpe
        4/4 (+0.084) and k=-0.5 loses 0/4 (-0.299) but fails the OOS-window 4b bars 4/4" —
        survives, because the arms it names already fail under the LOOSER bars and correction
        only tightens.
    P6  Over the 352 books the OOS-window 4b pass count falls by more than 10%.

OUTPUTS
    .console.txt   full transcript
    .grid.csv      352 books x both coefficient orders, OOS-window verdicts and margins
    .site.csv      the 16 walk-forward arm-cells, published vs corrected
    .surface.csv   the 25-point (phi, delta) surface
    .walkforward.csv  rule 8, all arms, both orders, vs RULES v1 and SPY
    .repro.csv     the reproduction gate
    .astsweep.csv  re-sweep of every `margins_at` call site in research/backtests
    .result.md     the answer
"""
import ast
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_back-fill-the-swapped-coefficient-audit_B"
OUT = ROOT / "research" / "backtests"
I168P = OUT / "2026-09-05_the-sign-is-the-parameter-not-the-share_cloud.py"
I168_STEM = "2026-09-05_the-sign-is-the-parameter-not-the-share_cloud"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I168 = _load(I168P, "i168")
C, H, I153 = I168.C, I168.H, I168.I153

# every corpus axis is inherited from idea 168 verbatim -- nothing is re-chosen here
FREQ, GROSS = I168.FREQ, I168.GROSS
PANELS, KS, SHARES, COSTS = I168.PANELS, I168.KS, I168.SHARES, I168.COSTS
OOS_START, IS_END = I168.OOS_START, I168.IS_END
K_LIVE = I168.K_LIVE

# the two tuned parameters
PHIS = [0.50, 0.60, 0.70, 0.80, 0.90]      # CAGR floor coefficient
DELTAS = [0.40, 0.50, 0.60, 0.70, 0.80]    # drawdown cap coefficient
PUBLISHED = (0.60, 0.70)                   # (phi, delta) as idea 168 line 515 passes them
CORRECT = (0.70, 0.60)                     # (phi, delta) as PROTOCOL rule 4b states them
OOS_BARS = ("H1", "H2", "DD", "CAGR")      # idea 168 line 517's convention, verbatim

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def oos_fail(r, bars_oos, phi, delta):
    """Idea 168 line 515-517's read, with the coefficient pair exposed."""
    mg = C.margins_at(r, bars_oos, phi, delta, which="OOS")
    fb = [b for b in OOS_BARS if mg[b] <= 0]
    return ("|".join(fb) if fb else "(none)"), mg


def main():
    t0 = time.time()
    say("=" * 200)
    say(f"IDEA 200 — back-fill-the-swapped-coefficient-audit   ({STEM})")
    say("Re-run idea 168's line-515 OOS read at the bars PROTOCOL actually states, and count how "
        "many published 4b/OOS verdicts move.")
    say(f"PUBLISHED (defect): phi={PUBLISHED[0]:.2f} delta={PUBLISHED[1]:.2f}   -> CAGR floor "
        f"{PUBLISHED[0]:.0%} of SPY, DD cap {PUBLISHED[1]:.0%} of SPY   [BOTH LOOSER]")
    say(f"CORRECT (PROTOCOL): phi={CORRECT[0]:.2f} delta={CORRECT[1]:.2f}   -> CAGR floor "
        f"{CORRECT[0]:.0%} of SPY, DD cap {CORRECT[1]:.0%} of SPY")
    say("Exactly 2 tuned params: phi x 5, delta x 5 = 25 points, all reported.  Panel, cost, k "
        "and share are carried corpus axes from idea 168, never selected on.")
    say("=" * 200)

    # ------------------------------------------------------------------ panels / references
    ref = {}
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        el = I153.eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        bars = dict(full=C.bars_win(spy, "full"), IS=C.bars_win(spy, "IS"),
                    OOS=C.bars_win(spy, "OOS"))
        ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        ref[pk] = dict(px=px, start=start, spy=spy, bars=bars, n_elig=n_elig, desc=desc,
                       nmap={m: max(2, int(round(m * n_elig))) for m in SHARES},
                       spy_m=ms, spy_oos=mo)
        b = bars["OOS"]
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
            f"{px.index[-1].date()}, mean weekly eligible {n_elig:.1f}")
        say(f"    SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.4f}/{ms['MaxDD']:.2%}  |  "
            f"SPY OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:.2%}")
        say(f"    OOS-window 4b bars   H1 > {b['s1']:.4f}   H2 > {b['s2']:.4f}")
        say(f"      DD cap    PUBLISHED |MaxDD| <= {PUBLISHED[1]*abs(b['sdd']):.2%}   "
            f"CORRECT |MaxDD| <= {CORRECT[1]*abs(b['sdd']):.2%}   "
            f"(tightens by {0.10*abs(b['sdd']):.2%})")
        say(f"      CAGR floor PUBLISHED CAGR >= {PUBLISHED[0]*b['scagr']:.2%}   "
            f"CORRECT CAGR >= {CORRECT[0]*b['scagr']:.2%}   "
            f"(tightens by {0.10*b['scagr']:.2%})")

    # ------------------------------------------------------------------ rebuild the 352 books
    say("\n" + "=" * 200)
    say("REBUILDING IDEA 168's CORPUS (352 books) — its own weights_k/score_k, imported")
    say("=" * 200)
    RET, V1, rows = {}, {}, []
    for pk in PANELS:
        R = ref[pk]
        px, start = R["px"], R["start"]
        for cost in COSTS:
            V1[(pk, cost)] = backtest(px, rules_v1_weights(px), cost_bps=cost,
                                      freq=FREQ)["returns"].loc[start:]
            for k in KS:
                for m in SHARES:
                    n = R["nmap"][m]
                    res = backtest(px, I168.weights_k(px, k, n, pk), cost_bps=cost, freq=FREQ)
                    r = res["returns"].loc[start:]
                    RET[(pk, cost, k, m)] = r
                    mm, mo = metrics(r), metrics(r.loc[OOS_START:])
                    h1, h2 = H.halves(r)
                    mgf = H.margins(r, R["bars"]["full"])
                    fb = [b for b in ("H1", "H2", "OOS", "DD", "CAGR") if mgf[b] <= 0]
                    fp, mgp = oos_fail(r, R["bars"]["OOS"], *PUBLISHED)
                    fc, mgc = oos_fail(r, R["bars"]["OOS"], *CORRECT)
                    rows.append(dict(
                        panel=pk, cost=cost, k=k, share=m, n=n,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        IS_CAGR=metrics(H.window(r, "IS"))["CAGR"],
                        IS_Sharpe=metrics(H.window(r, "IS"))["Sharpe"],
                        turnover=float(res["turnover"].loc[start:].sum() / (len(r) / 252.0)),
                        pass4a=H.pass4a(r, V1[(pk, cost)]), pass4b=(len(fb) == 0),
                        failing="|".join(fb),
                        oosw_fail_pub=fp, oosw_pass_pub=(fp == "(none)"),
                        oosw_fail_cor=fc, oosw_pass_cor=(fc == "(none)"),
                        mg_DD_pub=mgp["DD"], mg_CAGR_pub=mgp["CAGR"],
                        mg_DD_cor=mgc["DD"], mg_CAGR_cor=mgc["CAGR"],
                        mg_H1=mgp["H1"], mg_H2=mgp["H2"]))
        say(f"  {pk}: {len(KS)*len(SHARES)*len(COSTS)} books done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ------------------------------------------------------------------ reproduction gate
    say("\n" + "=" * 200)
    say("REPRODUCTION GATE (asserted before any new number is read)")
    say("=" * 200)
    rep = []
    key = ["panel", "cost", "k", "share"]
    p168 = OUT / f"{I168_STEM}.grid.csv"
    A = pd.read_csv(p168)
    B = G.merge(A, on=key, suffixes=("_new", "_old"), validate="one_to_one")
    say(f"  [a] idea 168 grid.csv: matched {len(B)} of {len(A)} published rows on {key}")
    worst = 0.0
    for col in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                "IS_CAGR", "IS_Sharpe", "turnover"]:
        d = float(np.nanmax(np.abs(B[f"{col}_new"].values - B[f"{col}_old"].values)))
        worst = max(worst, d)
        rep.append(dict(check="[a] idea168 grid 352 books", field=col, n=len(B), maxabsdiff=d,
                        verdict="MATCH" if d < 1e-12 else "MISMATCH"))
        say(f"      {col:<12s} n={len(B):3d}  maxabsdiff {d:.3e}  "
            f"{'MATCH' if d < 1e-12 else 'MISMATCH'}")
    for col in ["pass4a", "pass4b", "failing"]:
        # `failing` is the empty string for a 4b passer and round-trips through CSV as NaN, so
        # both sides are normalised before comparison; otherwise 47 identical empty cells read
        # as 47 mismatches.
        eq = int((B[f"{col}_new"].fillna("").astype(str)
                  == B[f"{col}_old"].fillna("").astype(str)).sum())
        rep.append(dict(check="[a] idea168 grid 352 books", field=col, n=len(B),
                        maxabsdiff=np.nan,
                        verdict=f"{eq}/{len(B)} identical"))
        say(f"      {col:<12s} n={len(B):3d}  identical {eq}/{len(B)}")
    assert len(B) == 352 and worst < 1e-12, "idea 168 corpus did not reproduce"
    say(f"  [a] VERDICT: reproduced, worst numeric gap {worst:.3e}   "
        "(the full-sample pass4b column is NOT exposed — it goes through H.margins, which "
        "hard-codes the correct roles)")

    # ------------------------------------------------------------------ [A] the site itself
    say("\n" + "=" * 200)
    say("[A] THE EXPOSED SITE — idea 168 line 515, the 16 walk-forward arm-cells")
    say("=" * 200)
    wf_pub = pd.read_csv(OUT / f"{I168_STEM}.walkforward.csv")
    srows = []
    for pk in PANELS:
        R = ref[pk]
        so = metrics(R["spy"].loc[OOS_START:])
        for cost in COSTS:
            v1o = metrics(V1[(pk, cost)].loc[OOS_START:])
            IS = G[(G.panel == pk) & (G.cost == cost)]
            m_star = float(IS[IS.k == 0.0].sort_values("IS_Sharpe").iloc[-1].share)
            isc = IS[IS.share == m_star].set_index("k").IS_CAGR
            k_star = float((isc - isc.loc[0.0]).idxmax())
            best = IS.sort_values("IS_Sharpe").iloc[-1]
            arms = {"A_LIVE": (K_LIVE, m_star), "A_ZERO": (0.0, m_star),
                    "A_ISK": (k_star, m_star),
                    "A_ISKS": (float(best.k), float(best.share))}
            say(f"\n  [{pk} @ {cost:.0f}bps]  IS share m*={m_star:.2f} (n={R['nmap'][m_star]}), "
                f"IS exponent k*={k_star:+.2f}, joint IS argmax (k {best.k:+.2f}, m {best.share:.2f})")
            for aname, (k, m) in arms.items():
                r = RET[(pk, cost, k, m)]
                mo = metrics(r.loc[OOS_START:])
                fp, mgp = oos_fail(r, R["bars"]["OOS"], *PUBLISHED)
                fc, mgc = oos_fail(r, R["bars"]["OOS"], *CORRECT)
                srows.append(dict(panel=pk, cost=cost, arm=aname, k=k, share=m,
                                  n=R["nmap"][m], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"],
                                  fail_pub=fp, pass_pub=(fp == "(none)"),
                                  fail_cor=fc, pass_cor=(fc == "(none)"),
                                  moved=(fp != fc), verdict_moved=((fp == "(none)") != (fc == "(none)")),
                                  mg_DD_pub=mgp["DD"], mg_DD_cor=mgc["DD"],
                                  mg_CAGR_pub=mgp["CAGR"], mg_CAGR_cor=mgc["CAGR"],
                                  v1_OOS_CAGR=v1o["CAGR"], v1_OOS_Sharpe=v1o["Sharpe"],
                                  v1_OOS_MaxDD=v1o["MaxDD"], spy_OOS_CAGR=so["CAGR"],
                                  spy_OOS_Sharpe=so["Sharpe"], spy_OOS_MaxDD=so["MaxDD"]))
                say(f"      {aname:<7s} k={k:+.2f} m={m:.2f}  OOS {mo['CAGR']:7.2%}/"
                    f"{mo['Sharpe']:.4f}/{mo['MaxDD']:7.2%}   PUBLISHED fails [{fp:<14s}] -> "
                    f"CORRECT fails [{fc:<14s}]   {'** MOVED **' if fp != fc else ''}")
            say(f"      {'RULES v1':<7s} {'':17s}  OOS {v1o['CAGR']:7.2%}/{v1o['Sharpe']:.4f}/"
                f"{v1o['MaxDD']:7.2%}")
            say(f"      {'SPY':<7s} {'':17s}  OOS {so['CAGR']:7.2%}/{so['Sharpe']:.4f}/"
                f"{so['MaxDD']:7.2%}")
    S = pd.DataFrame(srows)
    S.to_csv(OUT / f"{STEM}.site.csv", index=False)

    # reproduce the published fail strings under SWAPPED
    M = S.merge(wf_pub[["panel", "cost", "arm", "OOS_4b_fail", "OOS_Sharpe"]],
                on=["panel", "cost", "arm"], suffixes=("", "_pubfile"), validate="one_to_one")
    same = int((M.fail_pub == M.OOS_4b_fail).sum())
    dsh = float(np.nanmax(np.abs(M.OOS_Sharpe.values - M.OOS_Sharpe_pubfile.values)))
    rep.append(dict(check="[b] idea168 walkforward OOS_4b_fail under SWAPPED", field="string",
                    n=len(M), maxabsdiff=np.nan, verdict=f"{same}/{len(M)} identical"))
    rep.append(dict(check="[b] idea168 walkforward OOS_Sharpe", field="OOS_Sharpe", n=len(M),
                    maxabsdiff=dsh, verdict="MATCH" if dsh < 1e-12 else "MISMATCH"))
    say(f"\n  [b] REPRODUCTION OF THE SITE: {same}/{len(M)} published OOS_4b_fail strings "
        f"reproduced exactly under the SWAPPED pair; OOS Sharpe gap {dsh:.3e}")
    assert same == len(M) == 16 and dsh < 1e-12, "line 515 not reproduced"

    nmv = int(S.moved.sum())
    nvv = int(S.verdict_moved.sum())
    say(f"\n  ANSWER [A]: of the {len(S)} arm-cells the site evaluated, the FAILING-BAR SET moves "
        f"in {nmv}, and the PASS/FAIL VERDICT moves in {nvv}.")
    say(f"    published pass count {int(S.pass_pub.sum())}/{len(S)}   ->   corrected "
        f"{int(S.pass_cor.sum())}/{len(S)}")
    if nmv:
        say("\n  the arm-cells whose failing-bar set moves:")
        say(S[S.moved][["panel", "cost", "arm", "k", "share", "OOS_CAGR", "OOS_Sharpe",
                        "OOS_MaxDD", "fail_pub", "fail_cor", "verdict_moved"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ M1/M2 monotonicity
    say("\n" + "=" * 200)
    say("MONOTONICITY ASSERTIONS (the correction can only REMOVE passes)")
    say("=" * 200)
    m1 = int(((G.mg_DD_cor - G.mg_DD_pub) > 1e-15).sum())
    m2 = int(((G.mg_CAGR_cor - G.mg_CAGR_pub) > 1e-15).sum())
    say(f"  M1  books where the CORRECT DD margin exceeds the PUBLISHED one:   {m1} / {len(G)} "
        f"(expected 0; the cap tightens by 0.10*|SPY OOS MaxDD|)")
    say(f"  M2  books where the CORRECT CAGR margin exceeds the PUBLISHED one: {m2} / {len(G)} "
        f"(expected 0; the floor tightens by 0.10*SPY OOS CAGR)")
    flip_up = int((G.oosw_pass_cor & ~G.oosw_pass_pub).sum())
    say(f"  M3  books flipping FAIL -> PASS under the correction:               {flip_up} / "
        f"{len(G)} (must be 0)")
    assert m1 == 0 and m2 == 0 and flip_up == 0, "correction is not monotone — audit premise wrong"
    rep.append(dict(check="[c] monotonicity M1/M2/M3", field="counts", n=len(G),
                    maxabsdiff=np.nan, verdict=f"{m1}/{m2}/{flip_up} all zero"))
    say("  VERDICT: the defect is strictly PERMISSIVE.  Every verdict it can move, it moved in "
        "the direction of admitting a book that PROTOCOL's bars reject.")

    # ------------------------------------------------------------------ [B] the whole corpus
    say("\n" + "=" * 200)
    say("[B] THE WHOLE CORPUS — the same OOS-window read applied to all 352 books")
    say("=" * 200)
    npub, ncor = int(G.oosw_pass_pub.sum()), int(G.oosw_pass_cor.sum())
    nmoved = int((G.oosw_fail_pub != G.oosw_fail_cor).sum())
    nverd = int((G.oosw_pass_pub != G.oosw_pass_cor).sum())
    say(f"  OOS-window 4b passes:  PUBLISHED {npub}/352 ({npub/352:.1%})   ->   CORRECT "
        f"{ncor}/352 ({ncor/352:.1%})    change {ncor-npub:+d} ({(ncor-npub)/max(npub,1):+.1%})")
    say(f"  failing-bar set moves in {nmoved}/352 books; the PASS/FAIL verdict moves in "
        f"{nverd}/352 ({nverd/352:.1%})")
    say("\n  OOS-window 4b passes by panel x cost (PUBLISHED -> CORRECT):")
    for pk in PANELS:
        for cost in COSTS:
            sub = G[(G.panel == pk) & (G.cost == cost)]
            say(f"      {pk:<6s} @{cost:>5.1f}bps   {int(sub.oosw_pass_pub.sum()):3d} -> "
                f"{int(sub.oosw_pass_cor.sum()):3d}   of {len(sub)}   "
                f"(verdict moves {int((sub.oosw_pass_pub != sub.oosw_pass_cor).sum())})")
    say("\n  which bar does the correction newly bind on (among books whose verdict moved)?")
    mv = G[G.oosw_pass_pub & ~G.oosw_pass_cor]
    if len(mv):
        for b in OOS_BARS:
            kk = int(mv.oosw_fail_cor.str.contains(b).sum())
            say(f"      {b:>4s}  {kk:4d} / {len(mv)}  ({kk/len(mv):.1%})")
        say("\n  the books whose OOS-window verdict moves:")
        say(mv[["panel", "cost", "k", "share", "n", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                "oosw_fail_cor", "pass4b"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  by exponent k (PUBLISHED -> CORRECT OOS-window passes, pooled over panel/cost/share):")
    t = G.groupby("k")[["oosw_pass_pub", "oosw_pass_cor"]].sum().astype(int)
    t["delta"] = t.oosw_pass_cor - t.oosw_pass_pub
    say(t.to_string())

    # ------------------------------------------------------------------ (phi, delta) surface
    say("\n" + "=" * 200)
    say("THE TWO TUNED PARAMETERS — all 25 (phi, delta) grid points reported")
    say("=" * 200)
    surf = []
    for phi in PHIS:
        for delta in DELTAS:
            c352 = 0
            for pk in PANELS:
                Rb = ref[pk]["bars"]["OOS"]
                for cost in COSTS:
                    for k in KS:
                        for m in SHARES:
                            f, _ = oos_fail(RET[(pk, cost, k, m)], Rb, phi, delta)
                            c352 += (f == "(none)")
            c16 = 0
            for _, row in S.iterrows():
                f, _ = oos_fail(RET[(row.panel, row.cost, row.k, row.share)],
                                ref[row.panel]["bars"]["OOS"], phi, delta)
                c16 += (f == "(none)")
            tag = ("PROTOCOL" if (phi, delta) == CORRECT else
                   ("DEFECT" if (phi, delta) == PUBLISHED else ""))
            surf.append(dict(phi=phi, delta=delta, pass_352=c352, pass_16=c16, point=tag))
    SF = pd.DataFrame(surf)
    SF.to_csv(OUT / f"{STEM}.surface.csv", index=False)
    say("  OOS-window 4b passes out of 352 books  (rows = phi/CAGR floor, cols = delta/DD cap):")
    say(SF.pivot(index="phi", columns="delta", values="pass_352").to_string())
    say("\n  OOS-window 4b passes out of the 16 site arm-cells:")
    say(SF.pivot(index="phi", columns="delta", values="pass_16").to_string())
    say(f"\n  DEFECT   (phi {PUBLISHED[0]:.2f}, delta {PUBLISHED[1]:.2f}): "
        f"{int(SF[(SF.phi==PUBLISHED[0])&(SF.delta==PUBLISHED[1])].pass_352.iloc[0])}/352, "
        f"{int(SF[(SF.phi==PUBLISHED[0])&(SF.delta==PUBLISHED[1])].pass_16.iloc[0])}/16")
    say(f"  PROTOCOL (phi {CORRECT[0]:.2f}, delta {CORRECT[1]:.2f}): "
        f"{int(SF[(SF.phi==CORRECT[0])&(SF.delta==CORRECT[1])].pass_352.iloc[0])}/352, "
        f"{int(SF[(SF.phi==CORRECT[0])&(SF.delta==CORRECT[1])].pass_16.iloc[0])}/16")
    say(f"  surface range over the 25 points: {int(SF.pass_352.min())}..{int(SF.pass_352.max())} "
        f"of 352.  The defect's displacement is "
        f"{int(SF[(SF.phi==PUBLISHED[0])&(SF.delta==PUBLISHED[1])].pass_352.iloc[0]) - int(SF[(SF.phi==CORRECT[0])&(SF.delta==CORRECT[1])].pass_352.iloc[0]):+d} "
        f"books against a full-surface span of "
        f"{int(SF.pass_352.max()-SF.pass_352.min())}.")

    # ------------------------------------------------------------------ both KEEP paths
    say("\n" + "=" * 200)
    say("BOTH KEEP PATHS over the 352 books (PROTOCOL rule 4)")
    say("=" * 200)
    say(f"  4a (beat the live book):  {int(G.pass4a.sum())} / {len(G)}")
    say(f"  4b (capital-worthy, FULL-SAMPLE, via H.margins — NOT exposed to the defect):  "
        f"{int(G.pass4b.sum())} / {len(G)}")
    say(f"  4b on the OOS WINDOW (the exposed read):  PUBLISHED {npub} / {len(G)}  ->  CORRECT "
        f"{ncor} / {len(G)}")
    say("\n  full-sample 4b passes by cost x k:")
    say(G.groupby(["cost", "k"]).pass4b.sum().unstack(0).to_string())
    say("\n  books passing BOTH the full-sample 4b AND the corrected OOS-window 4b:")
    both = G[G.pass4b & G.oosw_pass_cor]
    say(f"      {len(both)} of {len(G)}"
        + ("" if len(both) == 0 else ""))
    if len(both):
        say(both[["panel", "cost", "k", "share", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    bothp = G[G.pass4b & G.oosw_pass_pub]
    say(f"      under the DEFECT's bars that count was {len(bothp)}  "
        f"({len(bothp)-len(both):+d} books were admitted by the defect)")

    # ------------------------------------------------------------------ rule 8 walk-forward
    say("\n" + "=" * 200)
    say("WALK-FORWARD (PROTOCOL rule 8) — everything chosen on 2009-2016 only, read ONCE on "
        "2017-2026.  Arms are idea 168's, verbatim.")
    say("=" * 200)
    z = S[S.arm == "A_ZERO"].set_index(["panel", "cost"]).OOS_Sharpe
    say("\n  Mean OOS by arm over the 4 (panel x cost) cells:")
    say(S.groupby("arm")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))
    for a in ("A_LIVE", "A_ISK", "A_ISKS"):
        d = S[S.arm == a].set_index(["panel", "cost"]).OOS_Sharpe - z
        say(f"      {a} - A_ZERO on OOS Sharpe: mean {d.mean():+.4f}, wins "
            f"{int((d > 0).sum())}/{len(d)}")
    say("\n  benchmarks (OOS 2017-2026):")
    say(S.groupby(["panel", "cost"])[["v1_OOS_CAGR", "v1_OOS_Sharpe", "v1_OOS_MaxDD",
                                      "spy_OOS_CAGR", "spy_OOS_Sharpe", "spy_OOS_MaxDD"]]
        .first().to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  OOS-window 4b verdict per arm, PUBLISHED -> CORRECT:")
    for a in ("A_LIVE", "A_ZERO", "A_ISK", "A_ISKS"):
        sa = S[S.arm == a]
        say(f"      {a:<7s} clears  PUBLISHED {int(sa.pass_pub.sum())}/4   CORRECT "
            f"{int(sa.pass_cor.sum())}/4   (fails: pub "
            f"{', '.join(sa.fail_pub)} | cor {', '.join(sa.fail_cor)})")
    S.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    say("\n  IDEA 168's PUBLISHED HEADLINE SENTENCE, re-read at PROTOCOL's bars:")
    isk = S[S.arm == "A_ISK"].set_index(["panel", "cost"])
    live = S[S.arm == "A_LIVE"].set_index(["panel", "cost"])
    d_isk = (isk.OOS_Sharpe - z)
    d_live = (live.OOS_Sharpe - z)
    say(f"      'IS-chosen k beats k=0 on OOS Sharpe 4/4 (+0.084)'   -> "
        f"{int((d_isk > 0).sum())}/4 ({d_isk.mean():+.4f})   "
        f"{'UNCHANGED' if int((d_isk > 0).sum()) == 4 else 'MOVED'}")
    say(f"      'k=-0.5 loses 0/4 (-0.299)'                          -> wins "
        f"{int((d_live > 0).sum())}/4 ({d_live.mean():+.4f})   "
        f"{'UNCHANGED' if int((d_live > 0).sum()) == 0 else 'MOVED'}")
    say(f"      'but fails the OOS-window 4b bars 4/4'               -> A_ISK fails "
        f"{4-int(isk.pass_cor.sum())}/4 at PROTOCOL's bars   "
        f"{'UNCHANGED' if int(isk.pass_cor.sum()) == 0 else 'MOVED'}")

    # ------------------------------------------------------------------ AST re-sweep
    say("\n" + "=" * 200)
    say("AST RE-SWEEP — every `margins_at` call site in research/backtests, re-audited today")
    say("=" * 200)
    arows = []
    for f in sorted(OUT.glob("*.py")):
        try:
            tree = ast.parse(f.read_text())
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            nm = fn.attr if isinstance(fn, ast.Attribute) else (
                fn.id if isinstance(fn, ast.Name) else None)
            if nm != "margins_at":
                continue
            pos = [a for a in node.args]
            phi = delta = None
            if len(pos) >= 4:
                for i, tgt in ((2, "phi"), (3, "delta")):
                    v = pos[i]
                    val = v.value if isinstance(v, ast.Constant) else None
                    if tgt == "phi":
                        phi = val
                    else:
                        delta = val
            for kw in node.keywords:
                if kw.arg == "phi" and isinstance(kw.value, ast.Constant):
                    phi = kw.value.value
                if kw.arg == "delta" and isinstance(kw.value, ast.Constant):
                    delta = kw.value.value
            lit = isinstance(phi, (int, float)) and isinstance(delta, (int, float))
            status = ("SWAPPED" if lit and abs(phi - 0.60) < 1e-9 and abs(delta - 0.70) < 1e-9
                      else ("CORRECT" if lit and abs(phi - 0.70) < 1e-9
                            and abs(delta - 0.60) < 1e-9
                            else ("SWEPT/NON-LITERAL" if not lit else "OTHER-LITERAL")))
            arows.append(dict(file=f.name, line=node.lineno, phi=phi, delta=delta, status=status))
    AS = pd.DataFrame(arows)
    AS.to_csv(OUT / f"{STEM}.astsweep.csv", index=False)
    say(f"  {len(AS)} `margins_at` call sites across {AS.file.nunique()} scripts")
    say(AS.status.value_counts().to_string())
    sw = AS[AS.status == "SWAPPED"]
    say(f"\n  SWAPPED sites ({len(sw)}):")
    say(sw[["file", "line", "phi", "delta"]].to_string(index=False))
    say("  (this script's own two literal pairs are swept constants, tagged OTHER-LITERAL/"
        "SWEPT and excluded from the defect count by construction — it passes both orders "
        "deliberately.)")

    pd.DataFrame(rep).to_csv(OUT / f"{STEM}.repro.csv", index=False)

    # ------------------------------------------------------------------ predictions
    say("\n" + "=" * 200)
    say("PRE-REGISTERED PREDICTIONS")
    say("=" * 200)
    p1 = worst < 1e-12
    p2 = (same == 16)
    p3 = (flip_up == 0)
    # P4 is pre-registered ON THE 16 ARM-CELLS ("Among the 16 walk-forward arm-cells..."), so it
    # is scored on S, not on the 352-book corpus.  The corpus-level version of the same clause is
    # reported beside it, unscored, because it is NOT what was pre-registered.
    smv = S[S.pass_pub & ~S.pass_cor]
    p4 = (nvv <= 4) and (len(smv) == 0 or bool(smv.fail_cor.str.contains("DD").all()))
    p4c = (len(mv) == 0 or bool(mv.oosw_fail_cor.str.contains("DD").all()))
    p5 = (int((d_isk > 0).sum()) == 4 and int((d_live > 0).sum()) == 0
          and int(isk.pass_cor.sum()) == 0)
    p6 = (npub > 0) and ((npub - ncor) / npub > 0.10)
    for nm2, ok, txt in [
            ("P1", p1, f"grid reproduces exactly ({worst:.2e})"),
            ("P2", p2, f"16 published fail-strings reproduce under SWAPPED ({same}/16)"),
            ("P3", p3, f"no FAIL->PASS flip ({flip_up})"),
            ("P4", p4, f"<=4 of the 16 SITE verdicts move and every mover's newly-bound bar is "
                       f"DD ({nvv} moved, {len(smv)} pass->fail)"),
            ("P5", p5, "idea 168's headline sentence survives verbatim"),
            ("P6", p6, f"corpus OOS-window pass count falls >10% ({npub}->{ncor})")]:
        say(f"  {nm2}  {'HIT ' if ok else 'MISS'}  {txt}")
    say(f"  (unscored, not pre-registered: the same 'all movers are DD' clause read on the 352-"
        f"book corpus instead of the 16 site cells is {'TRUE' if p4c else 'FALSE'} — "
        f"{int(mv.oosw_fail_cor.str.contains('DD').sum())} of {len(mv)} movers bind on DD, "
        f"{int(mv.oosw_fail_cor.str.contains('CAGR').sum())} on CAGR.)")

    say("\n" + "=" * 200)
    say(f"done in {time.time()-t0:.0f}s")
    say("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
