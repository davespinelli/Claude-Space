#!/usr/bin/env python3
"""QUEUE idea 156 — the-CAGR-floor-is-what-kills-small-pools  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 156)
    "idea 78's walk-forward found S1 and S2 both pick the k=20 cell, which has the two highest
     OOS Sharpes in the table (1.105, 1.184) at a third of SPY's drawdown and fails 4b on the
     CAGR floor in 50 of 50 draws, while the k=80 cell passes 46%.  Idea 148 already found the
     CAGR floor doing most of 4b's exclusion work under the no-leverage ceiling.  Test directly
     whether 4b's CAGR floor is a de-grossing artefact: re-run the same 300 sub-panel books at
     the gross that equalises realised vol to SPY's, and report which 4b verdicts flip.
     Max 2 params."

WHAT IS AT STAKE.
    4b's CAGR floor asks a book to earn at least 70% of SPY's CAGR.  A book that runs at 0.75
    gross, holds only trend-eligible names and sits in cash the rest of the time is running far
    less RISK than SPY, so failing a RETURN floor is not by itself evidence that the signal is
    weak — it may only be evidence that the book is small.  If so, the floor is measuring gross
    exposure rather than skill, and every "fails on CAGR" verdict in the project's leaderboard
    is a statement about the risk budget rather than the rule.  That is the artefact reading.

    The other reading is that the floor is doing exactly the job PROTOCOL rule 2 gives it.  No
    leverage is allowed.  If the gross needed to reach SPY's volatility is above 1.00, then the
    book CANNOT be scaled to where its CAGR clears, and the floor is a correct, binding
    statement about what this book can deliver with real capital.  Idea 148 already suspected
    this ("under the no-leverage ceiling").

    The two readings make opposite predictions and are separated by ONE number: the fraction of
    the 300 books whose vol-matching gross exceeds 1.00.  That is why this run reports both the
    UNCAPPED vol match (which answers "is the floor mechanically a gross artefact?") and the
    CAPPED one at g <= 1.00 (which answers "does that matter under PROTOCOL?").

CORPUS — idea 78's Test B, re-run, not approximated
    The B136 panel; k in {20, 40, 80}; 50 fixed random k-name sub-panels per k drawn from
    `np.random.default_rng(SEED_B + k)` with SEED_B = 78_500, i.e. the IDENTICAL sub-panels;
    CAND-n books at n in {5, 20}; 10 bps; weekly; t+1.  That is idea 78's 300 books
    (3 k x 50 draws x 2 n).  k, draw and n are CORPUS axes carried over from idea 78, not
    parameters tuned here.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points written to .grid.csv:
    1. the gross convention, 3 values:
         STATIC  g = 0.75                                  (idea 78's own, the control)
         VM_IS   g = 0.75 * vol(SPY, 2009-2016) / vol(book@0.75, 2009-2016)
                                                           (prospectively implementable)
         VM_FULL g = 0.75 * vol(SPY, full)      / vol(book@0.75, full)
                                                           (LOOK-AHEAD; the pure artefact test)
    2. the leverage ceiling, 2 values:  CAP  g <- min(g, 1.00)   (PROTOCOL rule 2)
                                        RAW  g uncapped          (LEVERED, never a KEEP)
    STATIC is unaffected by the ceiling (0.75 < 1.00) and is run once.

REPRODUCTION, asserted before any new number is read
    [a] The STATIC arm must reproduce idea 78's committed
        `2026-09-05_candidate-count-vs-dispersion_B.gridB.csv` cell-for-cell on CAGR, Sharpe,
        MaxDD, H1, H2 and the 4b failing-bar string, for all 300 books.  If [a] fails, the
        sub-panels are not idea 78's and nothing below is a re-run of idea 78.
    [b] idea 156's premise itself: the k=20/n=20 cell must fail 4b on CAGR in 50 of 50 draws
        and the k=80 cell must pass in about 46%.
    [c] The lever must be accurate: after re-running at the vol-matching g, the achieved
        realised vol must land on SPY's.  Mean |achieved/target - 1| is reported; if it is
        large, the vol match failed and the flip table below is not a clean test.

WALK-FORWARD (PROTOCOL rule 8) — selectors fixed BEFORE any OOS number is read:
    Within each gross arm, and separately at each n: S1 = IS Sharpe argmax over the 150 books;
    S2 = 4b-aware IS screen (IS halves, IS DD cap, IS CAGR floor) then IS Sharpe argmax, with
    an S1 fallback when the screen is empty; S0 = the do-nothing full-B136 control at the same
    gross convention.  Parameters chosen on <= 2016-12-31 only, read ONCE on 2017-01-01..2026.
    OOS CAGR / Sharpe / MaxDD are reported against RULES v1 on B136 (same cost) and SPY.
    VM_FULL's walk-forward is contaminated by construction (its g uses the OOS window) and is
    printed with that label, never used for a verdict.  Only VM_IS + CAP is both implementable
    and PROTOCOL-legal.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a] holds exactly; [b] reproduces idea 78's 50/50 and ~46%.
    P2  The vol-matching gross is ABOVE 1.00 for the large majority of the 300 books, and most
        of all in the small-k cells, because a 5-name trend-filtered book that sits in cash runs
        well under SPY's volatility.
    P3  UNCAPPED: most STATIC "CAGR-only" failures flip to a 4b pass, and the k=20 cell's
        50-of-50 CAGR failure largely disappears.  Mechanically, the floor is a gross artefact.
    P4  CAPPED at 1.00: few flip, because the required gross exceeds the ceiling.  Under
        PROTOCOL rule 2 the CAGR floor is a real bar and idea 148's reading survives.
    P5  Vol matching moves the DRAWDOWN cap the other way: books that gain CAGR lose the DD
        margin, so the net 4b pass count rises far less than the CAGR-flip count alone implies.
    P6  Nothing here is a KEEP.  Any new pass that appears requires leverage PROTOCOL forbids.

CAVEATS carried, not buried
    * Survivorship: B136 is a current-constituent list (idea 54).  Sub-panels drawn from it
      inherit that bias in full, and it flatters every book here equally.
    * VM_FULL uses full-sample volatility, which is LOOK-AHEAD.  It exists to answer the
      mechanical question and is never treated as a tradable rule.
    * Vol matching is not risk matching: equalising realised vol to SPY's does NOT equalise
      drawdown, and 4b's DD cap is the bar that pays for it.  That is measured, not assumed.
    * Idea 144: a re-grossed book is the same book.  No verdict flip here is a new signal.
    * Idea 66's "exact lever" is checked, not assumed — see [c].
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * The k=20/n=20 cell holds every eligible name by construction, so its "selection" is a
      weighting artefact (idea 78 flagged this); it is reported, not read as a selection result.

HARNESS
    Idea 78's committed script is IMPORTED and its `weights_cand`, `eligible_mask`,
    `fail_4a`, `fail_4b`, `half_sharpes` and `build_panels` are called verbatim, so the corpus
    is literally idea 78's corpus and the bars are literally 4b's.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .flips.csv, .lever.csv,
.walkforward.csv.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_the-CAGR-floor-is-what-kills-small-pools_cloud"
OUT = ROOT / "research" / "backtests"
I78P = OUT / "2026-09-05_candidate-count-vs-dispersion_B.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I78 = _load(I78P, "i78")

COST_BPS = I78.COST_BPS          # 10
FREQ = I78.FREQ                  # "W"
GROSS0 = I78.GROSS               # 0.75
KS = I78.KS                      # [20, 40, 80]
N_BOOKS = I78.N_BOOKS            # [5, 20]
N_DRAWS = I78.N_DRAWS_B          # 50
SEED_B = I78.SEED_B              # 78_500
IS_END, OOS_START = I78.IS_END, I78.OOS_START
CAP = 1.00                       # PROTOCOL rule 2: no leverage

ARMS = [("STATIC", "CAP"), ("VM_IS", "CAP"), ("VM_IS", "RAW"),
        ("VM_FULL", "CAP"), ("VM_FULL", "RAW")]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 2000)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def main():
    t0 = time.time()
    say("=" * 210)
    say(f"IDEA 156 — the-CAGR-floor-is-what-kills-small-pools   ({STEM})")
    say("Re-run idea 78's 300 sub-panel books at the gross that equalises realised vol to "
        "SPY's, and report which 4b verdicts flip — capped at 1.00 (PROTOCOL rule 2) and "
        "uncapped (the pure mechanical test).")
    say("PRE-REGISTERED: 2 tuned params (gross convention x 3, leverage ceiling x 2). k, draw "
        "and n are idea 78's corpus axes, carried over unchanged.")
    say("=" * 210)

    panels = I78.build_panels()
    px136, tr136 = panels["B136"]
    start = px136.index[260]
    spy = px136["SPY"].pct_change().fillna(0.0).loc[start:]
    spy_oos = spy.loc[OOS_START:]
    base = backtest(px136, rules_v1_weights(px136), cost_bps=COST_BPS,
                    freq=FREQ)["returns"].loc[start:]
    ms, mb = metrics(spy), metrics(base)
    vol_spy_full = ms["Vol"]
    vol_spy_is = metrics(spy.loc[:IS_END])["Vol"]

    say(f"\n  panel B136: {px136.shape[1]} cols, eval from {start.date()} to "
        f"{px136.index[-1].date()}")
    say(f"  SPY              {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  "
        f"vol {vol_spy_full:.2%}  halves {I78.half_sharpes(spy)[0]:.3f}/"
        f"{I78.half_sharpes(spy)[1]:.3f}  OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    say(f"  RULES v1 on B136 {mb['CAGR']:.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.2%}  "
        f"vol {mb['Vol']:.2%}  OOS Sharpe {metrics(base.loc[OOS_START:])['Sharpe']:.3f}")
    say(f"  4b bars: H1 > {I78.half_sharpes(spy)[0]:.3f}, H2 > "
        f"{I78.half_sharpes(spy)[1]:.3f}, OOS Sharpe > {metrics(spy_oos)['Sharpe']:.3f}, "
        f"MaxDD shallower than {0.60 * abs(ms['MaxDD']):.2%}, CAGR >= {0.70 * ms['CAGR']:.2%}")
    say(f"  SPY realised vol: full {vol_spy_full:.2%}, IS(<= {IS_END}) {vol_spy_is:.2%} "
        f"— these are the vol-match targets")

    names136 = [c for c in px136.columns if c in tr136]
    rows, rets = [], {}

    for k in KS:
        rng = np.random.default_rng(SEED_B + k)
        for d in range(N_DRAWS):
            cols = list(rng.choice(names136, size=k, replace=False))
            keep = list(dict.fromkeys(cols + ["SPY"]))
            p = px136[keep].dropna(how="all").ffill()
            tr = set(cols)
            for nb in N_BOOKS:
                W0 = I78.weights_cand(p, tr, nb, gross=GROSS0)
                r0 = backtest(p, W0, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
                v_full = metrics(r0)["Vol"]
                v_is = metrics(r0.loc[:IS_END])["Vol"]
                greq = {"STATIC": GROSS0,
                        "VM_IS": GROSS0 * vol_spy_is / v_is if v_is > 0 else np.nan,
                        "VM_FULL": GROSS0 * vol_spy_full / v_full if v_full > 0 else np.nan}
                for conv, ceil in ARMS:
                    g = greq[conv]
                    if ceil == "CAP":
                        g = min(g, CAP)
                    if conv == "STATIC":
                        r = r0
                    else:
                        r = backtest(p, I78.weights_cand(p, tr, nb, gross=g),
                                     cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
                    rets[(k, d, nb, conv, ceil)] = r
                    m = metrics(r)
                    mo = metrics(r.loc[OOS_START:])
                    h1, h2 = I78.half_sharpes(r)
                    f4b = I78.fail_4b(r, spy, r.loc[OOS_START:], spy_oos)
                    rows.append(dict(
                        k=k, draw=d, n=nb, conv=conv, ceil=ceil,
                        g_req=greq[conv], g_used=g, levered=(g > CAP + 1e-12),
                        vol=m["Vol"], vol_ratio=m["Vol"] / vol_spy_full,
                        vol_IS=metrics(r.loc[:IS_END])["Vol"],
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        Sharpe_IS=metrics(r.loc[:IS_END])["Sharpe"],
                        CAGR_IS=metrics(r.loc[:IS_END])["CAGR"],
                        MaxDD_IS=metrics(r.loc[:IS_END])["MaxDD"],
                        Sharpe_OOS=mo["Sharpe"], CAGR_OOS=mo["CAGR"], MaxDD_OOS=mo["MaxDD"],
                        f4a=I78.fail_4a(r, base), f4b=f4b,
                        pass4a=(I78.fail_4a(r, base) == "-"), pass4b=(f4b == "-")))
        say(f"  k={k:<3} done  ({time.time() - t0:.0f}s)")

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n  {len(G)} book-arm rows written ({len(G[G.conv == 'STATIC'])} STATIC = idea 78's "
        f"300 books)")

    # ============================================================ [a] reproduction of idea 78
    say("\n" + "=" * 210)
    say("[a] REPRODUCTION — the STATIC arm against idea 78's committed gridB.csv, all 300 books")
    say("=" * 210)
    ref = pd.read_csv(OUT / "2026-09-05_candidate-count-vs-dispersion_B.gridB.csv")
    S = G[G.conv == "STATIC"].set_index(["k", "n", "draw"]).sort_index()
    R = ref.set_index(["k", "n", "draw"]).sort_index()
    ok_a = True
    say(f"    rows: this run {len(S)}, idea 78 {len(R)}; index identical: "
        f"{S.index.equals(R.index)}")
    for c in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "Sharpe_OOS"):
        dmax = float((S[c] - R[c]).abs().max())
        ok_a &= dmax < 1e-9
        say(f"    max|diff| {c:<11} = {dmax:.3e}")
    same = (S["f4b"].astype(str) == R["f4b"].astype(str)).mean()
    ok_a &= same == 1.0
    say(f"    4b failing-bar string identical in {same:.1%} of the 300 books")
    say(f"[a] REPRODUCED EXACTLY: {ok_a}")

    # ============================================================ [b] idea 156's own premise
    say("\n[b] PREMISE — idea 156 says k=20 fails 4b on CAGR in 50/50 and k=80 passes ~46%")
    for k in KS:
        for nb in N_BOOKS:
            s = S.xs((k, nb), level=("k", "n"))
            cagr_fail = s.f4b.astype(str).str.split(",").apply(lambda v: "CAGR" in v).mean()
            say(f"    k={k:<3} n={nb:<3}: 4b pass {(s.f4b == '-').mean():5.1%}   "
                f"CAGR-bar failure {cagr_fail:5.1%}   mean CAGR {s.CAGR.mean():.2%} "
                f"(floor {0.70 * ms['CAGR']:.2%})   mean MaxDD {s.MaxDD.mean():.2%} "
                f"(cap {-0.60 * abs(ms['MaxDD']):.2%})   mean vol {s.vol.mean():.2%} "
                f"(SPY {vol_spy_full:.2%})")

    # ============================================================ [c] the lever's accuracy
    say("\n" + "=" * 210)
    say("[c] LEVER CONTROL — did re-grossing actually land the book on SPY's volatility?")
    say("=" * 210)
    lev = G.groupby(["conv", "ceil"]).agg(
        g_req_med=("g_req", "median"), g_req_min=("g_req", "min"), g_req_max=("g_req", "max"),
        frac_g_over_1=("g_req", lambda s: float((s > CAP).mean())),
        g_used_med=("g_used", "median"),
        vol_ratio_med=("vol_ratio", "median"),
        vol_ratio_mad=("vol_ratio", lambda s: float((s - 1).abs().median())),
        levered=("levered", "sum"), n=("g_req", "size")).reset_index()
    say(lev.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    vm = G[(G.conv == "VM_FULL") & (G.ceil == "RAW")]
    say(f"    VM_FULL/RAW: mean |achieved vol / SPY vol - 1| = "
        f"{float((vm.vol_ratio - 1).abs().mean()):.4f}  "
        f"(if this is small the lever is accurate and the flip table is a clean test)")
    say(f"    FRACTION OF THE 300 BOOKS NEEDING g > 1.00 TO REACH SPY's VOL: "
        f"VM_FULL {float((G[(G.conv == 'VM_FULL') & (G.ceil == 'RAW')].g_req > CAP).mean()):.1%}, "
        f"VM_IS {float((G[(G.conv == 'VM_IS') & (G.ceil == 'RAW')].g_req > CAP).mean()):.1%}")
    G.groupby(["conv", "ceil"]).size()
    lev.to_csv(OUT / f"{STEM}.lever.csv", index=False)

    # ============================================================ the flip table
    say("\n" + "=" * 210)
    say("THE FLIP TABLE — 4b verdict at each gross convention vs the STATIC control, per book")
    say("=" * 210)
    key = ["k", "n", "draw"]
    stat = G[G.conv == "STATIC"].set_index(key)[["pass4b", "f4b", "CAGR", "MaxDD", "Sharpe"]]
    stat.columns = ["s_pass", "s_f4b", "s_CAGR", "s_MaxDD", "s_Sharpe"]
    flips = []
    for conv, ceil in ARMS:
        if conv == "STATIC":
            continue
        a = G[(G.conv == conv) & (G.ceil == ceil)].set_index(key)
        j = a.join(stat)
        k2k = int(((~j.s_pass) & j.pass4b).sum())
        p2f = int((j.s_pass & (~j.pass4b)).sum())
        cagr_only = j[(~j.s_pass) & (j.s_f4b == "CAGR")]
        flips.append(dict(conv=conv, ceil=ceil, n=len(j),
                          pass_STATIC=int(j.s_pass.sum()), pass_arm=int(j.pass4b.sum()),
                          KILL_to_KEEP=k2k, KEEP_to_KILL=p2f, net=k2k - p2f,
                          cagr_only_at_static=len(cagr_only),
                          cagr_only_now_pass=int(cagr_only.pass4b.sum()),
                          cagr_bar_fail_STATIC=int(j.s_f4b.astype(str).str.split(",").apply(
                              lambda v: "CAGR" in v).sum()),
                          cagr_bar_fail_arm=int(j.f4b.astype(str).str.split(",").apply(
                              lambda v: "CAGR" in v).sum()),
                          dd_bar_fail_STATIC=int(j.s_f4b.astype(str).str.split(",").apply(
                              lambda v: "DD" in v).sum()),
                          dd_bar_fail_arm=int(j.f4b.astype(str).str.split(",").apply(
                              lambda v: "DD" in v).sum()),
                          mean_dCAGR=float((j.CAGR - j.s_CAGR).mean()),
                          mean_dMaxDD=float((j.MaxDD - j.s_MaxDD).mean()),
                          mean_dSharpe=float((j.Sharpe - j.s_Sharpe).mean()),
                          levered_rows=int(j.levered.sum())))
    F = pd.DataFrame(flips)
    F.to_csv(OUT / f"{STEM}.flips.csv", index=False)
    say(F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  Reading: `cagr_only_now_pass / cagr_only_at_static` is the artefact fraction — how "
        "many books whose ONLY 4b failure was the CAGR floor clear once the book is scaled to "
        "SPY's risk.  `levered_rows` says how many of those need leverage PROTOCOL rule 2 "
        "forbids.  `dd_bar_fail_arm` is the price: re-grossing buys CAGR with drawdown.")

    say("\n  per-cell 4b pass rate by (k, n) x arm:")
    piv = G.assign(arm=G.conv + "/" + G.ceil).pivot_table(
        index=["k", "n"], columns="arm", values="pass4b", aggfunc="mean")
    say(piv.to_string(float_format=lambda x: f"{x:.2f}"))
    say("\n  per-cell CAGR-bar failure rate by (k, n) x arm:")
    piv2 = G.assign(arm=G.conv + "/" + G.ceil,
                    cf=G.f4b.astype(str).str.split(",").apply(lambda v: "CAGR" in v)).pivot_table(
        index=["k", "n"], columns="arm", values="cf", aggfunc="mean")
    say(piv2.to_string(float_format=lambda x: f"{x:.2f}"))
    say("\n  per-cell DD-bar failure rate by (k, n) x arm:")
    piv3 = G.assign(arm=G.conv + "/" + G.ceil,
                    df_=G.f4b.astype(str).str.split(",").apply(lambda v: "DD" in v)).pivot_table(
        index=["k", "n"], columns="arm", values="df_", aggfunc="mean")
    say(piv3.to_string(float_format=lambda x: f"{x:.2f}"))
    say("\n  4b failing-bar census by arm (a book can fail several bars):")
    cen = []
    for conv, ceil in ARMS:
        a = G[(G.conv == conv) & (G.ceil == ceil)]
        row = dict(arm=f"{conv}/{ceil}", n=len(a), pass4b=int(a.pass4b.sum()),
                   pass4a=int(a.pass4a.sum()))
        for bar in ("H1", "H2", "OOS", "DD", "CAGR"):
            row[bar] = int(a.f4b.astype(str).str.split(",").apply(lambda v: bar in v).sum())
        cen.append(row)
    say(pd.DataFrame(cen).to_string(index=False))

    say("\n  mean book statistics by arm:")
    ms_arm = G.assign(arm=G.conv + "/" + G.ceil).groupby("arm").agg(
        g=("g_used", "mean"), vol=("vol", "mean"), CAGR=("CAGR", "mean"),
        Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "mean"),
        OOS_Sharpe=("Sharpe_OOS", "mean"), OOS_CAGR=("CAGR_OOS", "mean"))
    say(ms_arm.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"  SPY for reference: vol {vol_spy_full:.4f}, CAGR {ms['CAGR']:.4f}, Sharpe "
        f"{ms['Sharpe']:.4f}, MaxDD {ms['MaxDD']:.4f}")

    # ============================================================ rule 8 walk-forward
    say("\n" + "=" * 210)
    say("RULE 8 WALK-FORWARD — sub-panel chosen on <= " + IS_END + " only, read ONCE on "
        + OOS_START + "->")
    say("S1 = IS Sharpe argmax.  S2 = 4b-aware IS screen then IS Sharpe argmax (S1 fallback).  "
        "S0 = do-nothing full-B136 control at the same gross convention.")
    say("VM_FULL's g uses the OOS window: its rows are CONTAMINATED and labelled so.")
    say("=" * 210)
    spy_o = metrics(spy_oos)
    v1_o = metrics(base.loc[OOS_START:])
    bIS = dict(s1=I78.half_sharpes(spy.loc[:IS_END])[0],
               s2=I78.half_sharpes(spy.loc[:IS_END])[1],
               dd=metrics(spy.loc[:IS_END])["MaxDD"], cagr=metrics(spy.loc[:IS_END])["CAGR"])

    def is_admissible(row):
        h1, h2 = I78.half_sharpes(rets[(row.k, row.draw, row.n, row.conv, row.ceil)].loc[:IS_END])
        return (h1 > bIS["s1"] and h2 > bIS["s2"]
                and abs(row.MaxDD_IS) <= 0.60 * abs(bIS["dd"])
                and row.CAGR_IS >= 0.70 * bIS["cagr"])

    wf = []
    for conv, ceil in ARMS:
        A = G[(G.conv == conv) & (G.ceil == ceil)].copy()
        A["IS_adm"] = A.apply(is_admissible, axis=1)
        for nb in N_BOOKS:
            sub = A[A.n == nb]
            # S0 — the do-nothing full-panel control at the same gross convention
            W0 = I78.weights_cand(px136, tr136, nb, gross=GROSS0)
            r0 = backtest(px136, W0, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
            if conv == "STATIC":
                g0 = GROSS0
            elif conv == "VM_IS":
                g0 = GROSS0 * vol_spy_is / metrics(r0.loc[:IS_END])["Vol"]
            else:
                g0 = GROSS0 * vol_spy_full / metrics(r0)["Vol"]
            if ceil == "CAP":
                g0 = min(g0, CAP)
            r_s0 = (r0 if conv == "STATIC" else
                    backtest(px136, I78.weights_cand(px136, tr136, nb, gross=g0),
                             cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:])
            picks = [("S0 do-nothing (full B136)", None, r_s0, g0)]
            s1 = sub.sort_values(["Sharpe_IS", "k"], ascending=[False, True]).iloc[0]
            picks.append(("S1 IS-Sharpe argmax", s1,
                          rets[(s1.k, s1.draw, nb, conv, ceil)], s1.g_used))
            adm = sub[sub.IS_adm]
            s2 = (adm.sort_values(["Sharpe_IS", "k"], ascending=[False, True]).iloc[0]
                  if len(adm) else s1)
            picks.append((f"S2 4b-aware IS screen ({len(adm)} admissible)", s2,
                          rets[(s2.k, s2.draw, nb, conv, ceil)], s2.g_used))
            for lbl, row, r, gg in picks:
                ro = r.loc[OOS_START:]
                mo = metrics(ro)
                f4b = I78.fail_4b(r, spy, ro, spy_oos)
                wf.append(dict(conv=conv, ceil=ceil, n=nb, selector=lbl,
                               contaminated=(conv == "VM_FULL"),
                               k=(int(row.k) if row is not None else -1),
                               draw=(int(row.draw) if row is not None else -1),
                               g_used=gg, levered=bool(gg > CAP + 1e-12),
                               IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                               OOS_MaxDD=mo["MaxDD"],
                               v1_OOS_CAGR=v1_o["CAGR"], v1_OOS_Sharpe=v1_o["Sharpe"],
                               v1_OOS_MaxDD=v1_o["MaxDD"],
                               spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_Sharpe=spy_o["Sharpe"],
                               spy_OOS_MaxDD=spy_o["MaxDD"],
                               d_vs_v1=mo["Sharpe"] - v1_o["Sharpe"],
                               d_vs_spy=mo["Sharpe"] - spy_o["Sharpe"],
                               f4a=I78.fail_4a(r, base), f4b=f4b, pass4b=(f4b == "-")))
                say(f"  {conv:<8}/{ceil:<3} n={nb:<3} {lbl:<38} g={gg:.2f}"
                    f"{' LEVERED' if gg > CAP + 1e-12 else '        '}"
                    f" k={wf[-1]['k']:<3} -> OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/"
                    f"{mo['MaxDD']:.2%} | dSharpe vs v1 {mo['Sharpe'] - v1_o['Sharpe']:+.3f}, "
                    f"vs SPY {mo['Sharpe'] - spy_o['Sharpe']:+.3f} | full-sample 4b "
                    f"{f4b}{'   [CONTAMINATED: g uses OOS vol]' if conv == 'VM_FULL' else ''}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"\n  SPY OOS   {spy_o['CAGR']:.2%}/{spy_o['Sharpe']:.3f}/{spy_o['MaxDD']:.2%}")
    say(f"  RULES v1 OOS on B136  {v1_o['CAGR']:.2%}/{v1_o['Sharpe']:.3f}/{v1_o['MaxDD']:.2%}")

    # ============================================================ census
    say("\n" + "=" * 210)
    say("CENSUS")
    say("=" * 210)
    say(f"  total book-arm rows: {len(G)};  4a passes {int(G.pass4a.sum())};  "
        f"4b passes {int(G.pass4b.sum())}")
    unl = G[~G.levered]
    say(f"  UNLEVERED rows only (PROTOCOL rule 2): {len(unl)};  4a {int(unl.pass4a.sum())};  "
        f"4b {int(unl.pass4b.sum())}")
    say(f"  4b passes that REQUIRE leverage: {int(G[G.levered].pass4b.sum())}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    print(f"\nwrote {STEM}.console.txt/.grid.csv/.flips.csv/.lever.csv/.walkforward.csv "
          f"({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
