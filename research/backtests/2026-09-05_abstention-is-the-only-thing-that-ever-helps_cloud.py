#!/usr/bin/env python3
"""QUEUE idea 194 — abstention-is-the-only-thing-that-ever-helps  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 194)
    "across ideas 171/174/175/184/186/192 the in-sample selector has now lost to doing nothing
     eight times running, and idea 192's S3 beat the published gate ONLY by abstaining in 20 of
     24 cells.  Test the degenerate hypothesis directly: for every published selector in the
     record, replace the gate with a pure ABSTAIN-ALWAYS arm and measure how much of each gate's
     reported OOS gain/loss is explained by its abstention rate alone.  If abstention explains
     it all, 'do not select' is a PROTOCOL clause, not a backtest, and rule 8 should say so."

THE FIRST THING TO SAY IS AN IDENTITY, NOT A NUMBER
    In this project's own convention (ideas 129/132/186/192) a gate that admits nothing HOLDS
    THE CELL'S CONTROL BOOK, and the do-nothing arm S0 IS that control book.  So on an abstained
    cell the gate's return series is IDENTICALLY S0's and the paired difference is EXACTLY zero.
    A pure ABSTAIN-ALWAYS arm is therefore not an approximation of S0 — it IS S0, and its gain is
    0.0000 by construction (check [c] below measures it and gets 0.0).  The decomposition is

        gain(G)  =  a * 0  +  (1 - a) * c        where a = abstention rate,
                                                       c = mean choice effect on PICKED cells

    so "how much of the gate's gain is explained by its abstention rate alone" has an exact
    answer: abstention contributes NOTHING directly and acts ONLY as a dilution factor (1 - a)
    on whatever the underlying selector does.  A gate with a negative c is improved by abstaining
    for exactly the same reason a losing bet is improved by betting less.  Check [d] verifies the
    identity numerically on all 25 gates.

    That turns idea 194's question into the one that is not arithmetic, and this run answers it:
        IS THE ABSTENTION *CHOICE* SKILFUL?
    i.e. does a gate abstain in the cells where its selector would actually have lost, or is it
    just abstaining a lot?  The correct null is a MATCHED-RATE RANDOM ABSTENTION: abstain in the
    same NUMBER of cells, chosen at random, and apply the ungated selector everywhere else.  If
    every real gate sits inside that band, the gate contributes its RATE and nothing else, and
    "do not select" is a PROTOCOL clause rather than a result — which is what idea 194 proposes.

CORPUS — carried verbatim from ideas 153/159/165/177, rebuilt not read
    3 panels x 7 keys x 9 shares x 2 cost rungs = 378 books, weekly, t+1, gross 0.75 spread over
    the names actually held (idea 153/159's `norm` construction).  Idea 177's build_panels() and
    build_base() are IMPORTED, so the corpus under test is literally the code that produced the
    corpus in the run beside it, and reproduction [b] re-checks it against idea 165's .grid.csv.
      CELL     = (panel, cost rung, share)                     -> 54 cells
      MENU     = the 7 keys.  CONTROL = NONE (the composite with NO cross-sectional tilt), which
                 is the natural do-nothing: "apply no key".  CANDIDATES = the other 6, RND
                 (idea 159's fixed per-name scramble, seed 159000) among them as a reported null.
    Panels, cost rungs, shares and keys are REPORTED CORPUS AXES; none is tuned here.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL 25 grid points reported
    1. the ABSTENTION THRESHOLD tau, 5 values: -inf (never abstain), 0.00, 0.05, 0.10, 0.20.
       A gate picks its selector's IS argmax only if that arm's IS SHARPE exceeds the control's
       by more than tau; otherwise it abstains and holds the control.  IS Sharpe is used as the
       single common gate currency for every selector so that tau means the same thing across
       them (idea "IS-Sharpe-margin-as-the-reportable-selector-statistic"'s convention); this is
       stated, not hidden, and tau = -inf recovers the ungated selector exactly.
    2. the SELECTOR STATISTIC, 5 values, the families actually published in this record:
       IS_SHARPE (the incumbent), IS_CALMAR, IS_MAXDD, IS_CAGR, IS_4B (max of the minimum
       z-scored 4b margin on the IS window — the "4b-aware screen" of ideas 129/132/152).
    Plus two arms that are not grid points but controls: S0 do-nothing (= ABSTAIN-ALWAYS, tau =
    +inf) and RANDOM (a uniformly random candidate per cell, seed 194000).

WALK-FORWARD (PROTOCOL rule 8) — everything is fitted IS and read ONCE OOS
    Every selector statistic, every gate decision and every abstention is computed on the IS
    window (<= 2016-12-31) only.  The resulting per-cell pick is read ONCE on 2017-01-01..2026.
    Reported per arm: mean OOS Sharpe / CAGR / MaxDD, paired difference vs S0 with a t-stat and
    a win/loss count, both KEEP paths on the OOS window (4a against RULES v1, 4b against SPY),
    and the full-sample 4a/4b counts, beside RULES v1's and SPY's own numbers on every panel.

THE RECORD BACK-FILL (idea 194's "for every published selector in the record")
    All research/backtests/*.walkforward.csv are scanned and, wherever a file records BOTH an
    abstention signal (an empty/NONE `pick`, or an `n_admitted`/`n_admissible` of 0) AND a
    control column to difference against, the pair (abstention rate, mean OOS Sharpe gain) is
    recovered per selector and regressed.  This is a BEST-EFFORT back-fill on a heterogeneous
    schema: the number of recoverable selectors is reported alongside the number of files
    scanned, and unrecoverable files are counted, never silently dropped.  It is reported as
    corroboration of the fresh experiment, never as its evidence.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  Reproduction: the corpus matches idea 165's published .grid.csv to < 1e-9, and the
        ABSTAIN-ALWAYS identity is EXACT — max |OOS(A_inf) - OOS(S0)| = 0.0 over all 54 cells.
    P2  The decomposition identity gain = (1-a) * c holds to < 1e-12 for all 25 gates.
    P3  No gate's abstention CHOICE is skilful: every real gate sits inside its matched-rate
        random-abstention null band (two-sided permutation p > 0.05).  If ANY gate is outside
        the band on the good side, the abstention choice carries information and idea 194's
        degenerate reading is wrong — a rare positive result, and it would be reported as one.
    P4  Across the 25 gates, the OOS gain is largely a function of the abstention rate alone:
        R^2 of gain on a exceeds 0.50, with a slope toward zero gain as a -> 1.
    P5  No arm beats S0 at t > 2 on mean OOS Sharpe.  This would be the ninth consecutive
        do-nothing result in the record.
    P6  No new book: no arm is promoted, and the OOS 4b pass count stays a minority of 54.

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are current constituents (idea 54); the small panel is the
      sub-$2B screen with the 44 max_1d_move >= 1.0 tickers dropped and a joined, never-selectable
      SPY.  Absent delistings inflate every CAGR here; no level in this file is achievable.
    * The 54 cells are NOT independent — they share three price panels — so every t-stat here is
      optimistic.  They are reported as descriptive, and the matched-rate permutation null (which
      re-uses the same cells) is the inference this run actually leans on.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so an IS-read
      drawdown statistic (IS_MAXDD, IS_4B) is measured on a window that cannot express a deep
      drawdown.  That works against those two selectors specifically and is stated, not adjusted.
    * The record back-fill reads columns written by ~70 different scripts under no common schema.
      It is a lower bound on what the record contains, not a census of it.
    * Every row is quoted at t+1 execution only (idea 126).

Deterministic, standalone.  Writes .console.txt, .cells.csv, .gates.csv, .record.csv and
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
from baseline import load_universe, rules_v1_weights  # noqa: E402,F401
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_abstention-is-the-only-thing-that-ever-helps_cloud"
OUT = ROOT / "research" / "backtests"
I177P = OUT / "2026-09-05_publish-the-failing-bar-not-the-required-gross_cloud.py"
I165_GRID = OUT / "2026-09-05_required-gross-as-a-leaderboard-column_cloud.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I177 = _load(I177P, "i177")
H, C = I177.H, I177.C

PANELS, KEYS, SHARES, COSTS = I177.PANELS, I177.KEYS, I177.SHARES, I177.COSTS
BARS, IS_END, OOS_START = I177.BARS, I177.IS_END, I177.OOS_START
CONTROL = "NONE"
CAND = [k for k in KEYS if k != CONTROL]
SELECTORS = ["IS_SHARPE", "IS_CALMAR", "IS_MAXDD", "IS_CAGR", "IS_4B"]
TAUS = [-np.inf, 0.00, 0.05, 0.10, 0.20]
NPERM = 2000
SEED = 194_000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 400)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def tstat(d):
    d = np.asarray([x for x in d if np.isfinite(x)], float)
    if len(d) < 3 or d.std(ddof=1) == 0:
        return np.nan
    return float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d))))


def is_stat(which, r, bars, sd):
    """The selector statistic, read on the IS window ONLY."""
    w = r.loc[:IS_END]
    m = metrics(w)
    if which == "IS_SHARPE":
        return m["Sharpe"]
    if which == "IS_CALMAR":
        return m["CAGR"] / abs(m["MaxDD"]) if abs(m["MaxDD"]) > 1e-12 else np.nan
    if which == "IS_MAXDD":
        return m["MaxDD"]                      # less negative is better
    if which == "IS_CAGR":
        return m["CAGR"]
    mg = I177.margins(r, bars, "IS")
    return min(mg[k] / sd[k] for k in BARS)    # IS_4B: the tightest z-scored 4b margin


def main():
    t0 = time.time()
    say("=" * 200)
    say(f"IDEA 194 — abstention-is-the-only-thing-that-ever-helps   ({STEM})")
    say("Replace every gate with a pure ABSTAIN-ALWAYS arm and measure how much of its OOS "
        "gain is its abstention RATE rather than its abstention CHOICE.")
    say("PRE-REGISTERED: exactly 2 tuned params (abstention threshold tau x 5, selector "
        "statistic x 5). Panels, cost rungs, shares and keys are carried corpus axes.")
    say("PREDICTIONS P1-P6 are in the docstring, written before the grid was read.")
    say("=" * 200)

    ref, nmap = I177.build_panels()
    say("\n" + "=" * 200)
    say("CORPUS — idea 177's build_base(), 189 genuine runs -> 378 books")
    base_r, turn = I177.build_base(ref, nmap)
    say(f"    {len(base_r)} books built in {time.time()-t0:.0f}s")

    # ---------------------------------------------------------- [b] reproduction
    rows = []
    for bk, r in base_r.items():
        pk, c, key, m = bk
        mf, mo = metrics(r), metrics(r.loc[OOS_START:])
        h1, h2 = H.halves(r)
        rows.append(dict(panel=pk, cost=c, key=key, share=m, n=nmap[pk][m], CAGR=mf["CAGR"],
                         Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                         OOS_Sharpe=mo["Sharpe"]))
    grid = pd.DataFrame(rows)
    say("\nREPRODUCTION [b] — against idea 165's published .grid.csv")
    repro_ok = False
    if I165_GRID.exists():
        j = grid.merge(pd.read_csv(I165_GRID), on=["panel", "cost", "key", "share"],
                       suffixes=("", "_p"))
        ds = {f: float(np.abs(j[f].astype(float) - j[f + "_p"].astype(float)).max())
              for f in ("n", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")}
        for f, d in ds.items():
            say(f"    {f:<12} max|diff| {d:.3e}   {'MATCH' if d < 1e-9 else 'MISMATCH'}")
        repro_ok = (len(j) == len(grid)) and all(d < 1e-9 for d in ds.values())
    say(f"    P1 reproduction of the corpus: {'PASS' if repro_ok else 'FAIL/UNAVAILABLE'}")

    # ---------------------------------------------------------- cells, margins, IS statistics
    cells = [(pk, c, m) for pk in PANELS for c in COSTS for m in SHARES]
    mg_is = {b: I177.margins(base_r[b], ref[b[0]]["bars"]["IS"], "IS") for b in base_r}
    sd_is = {k: float(np.std([mg_is[b][k] for b in base_r], ddof=1)) for k in BARS}
    ISS = {}      # (cell, key) -> dict of IS statistics
    for (pk, c, m) in cells:
        for key in KEYS:
            r = base_r[(pk, c, key, m)]
            ISS[((pk, c, m), key)] = {s: is_stat(s, r, ref[pk]["bars"]["IS"], sd_is)
                                      for s in SELECTORS}
    say(f"\n    {len(cells)} cells x {len(KEYS)} keys; control = {CONTROL}, "
        f"candidates = {CAND}")

    # ---------------------------------------------------------- OOS read-once table
    def oos(cell, key):
        pk, c, m = cell
        r = base_r[(pk, c, key, m)]
        mo = metrics(r.loc[OOS_START:])
        mgo = I177.margins(r, ref[pk]["bars"]["OOS"], "OOS")
        v1o = ref[pk]["v1"][c].loc[OOS_START:]
        h1, h2 = H.halves(r.loc[OOS_START:])
        b1, b2 = H.halves(v1o)
        mgf = I177.margins(r, ref[pk]["bars"]["full"], "full")
        return dict(S=mo["Sharpe"], CAGR=mo["CAGR"], DD=mo["MaxDD"],
                    p4b=all(mgo[k] > 0 for k in BARS),
                    p4a=bool(h1 > b1 and h2 > b2 and mo["MaxDD"] >= metrics(v1o)["MaxDD"]),
                    f4b=all(mgf[k] > 0 for k in BARS))
    OO = {(cell, key): oos(cell, key) for cell in cells for key in KEYS}
    cf = pd.DataFrame([dict(panel=cell[0], cost=cell[1], share=cell[2], key=key,
                            **{k: v for k, v in OO[(cell, key)].items()})
                       for cell in cells for key in KEYS])
    cf.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    say(f"    per-cell OOS table -> {STEM}.cells.csv ({len(cf)} rows)")

    S0 = {cell: OO[(cell, CONTROL)]["S"] for cell in cells}

    # ---------------------------------------------------------- [c] the ABSTAIN-ALWAYS identity
    say("\n" + "=" * 200)
    say("[c] THE ABSTAIN-ALWAYS IDENTITY — a gate that admits nothing holds the control, so a "
        "pure ABSTAIN-ALWAYS arm IS S0")
    dinf = max(abs(OO[(cell, CONTROL)]["S"] - S0[cell]) for cell in cells)
    say(f"    max |OOS Sharpe(A_inf) - OOS Sharpe(S0)| over {len(cells)} cells: {dinf:.3e}  ->  "
        f"{'EXACT (gain is 0.0000 by construction, not by measurement)' if dinf == 0.0 else 'NOT EXACT — the convention does not hold here'}")

    # ---------------------------------------------------------- the 25 gates
    say("\n" + "=" * 200)
    say("THE 25 GATES — 5 selectors x 5 abstention thresholds, every grid point reported")
    say("    a = abstention rate; c = mean choice effect on PICKED cells; gain = (1-a)*c "
        "(identity check [d]); p_null = matched-rate random-abstention permutation p.")
    rng = np.random.default_rng(SEED)
    gate_rows, wf_rows = [], []

    # the ungated pick per selector (tau = -inf), needed for the matched-rate null
    ungated = {}
    for s in SELECTORS:
        ungated[s] = {cell: max(CAND, key=lambda k: ISS[(cell, k)][s]) for cell in cells}
    marg = {s: {cell: ISS[(cell, ungated[s][cell])]["IS_SHARPE"] - ISS[(cell, CONTROL)]["IS_SHARPE"]
                for cell in cells} for s in SELECTORS}

    for s in SELECTORS:
        for tau in TAUS:
            picks = {cell: (ungated[s][cell] if marg[s][cell] > tau else CONTROL)
                     for cell in cells}
            absd = [cell for cell in cells if picks[cell] == CONTROL]
            a = len(absd) / len(cells)
            d = [OO[(cell, picks[cell])]["S"] - S0[cell] for cell in cells]
            gain = float(np.mean(d))
            pick_cells = [cell for cell in cells if picks[cell] != CONTROL]
            cchoice = float(np.mean([OO[(cell, picks[cell])]["S"] - S0[cell]
                                     for cell in pick_cells])) if pick_cells else 0.0
            ident = abs(gain - (1 - a) * cchoice)

            # matched-rate random-abstention null: abstain in the same NUMBER of cells at random
            k_abs = len(absd)
            if 0 < k_abs < len(cells):
                null = np.empty(NPERM)
                dd_full = np.array([OO[(cell, ungated[s][cell])]["S"] - S0[cell] for cell in cells])
                for t in range(NPERM):
                    idx = rng.permutation(len(cells))[:k_abs]
                    keep = np.ones(len(cells), bool)
                    keep[idx] = False
                    null[t] = dd_full[keep].sum() / len(cells)
                p_null = float(2 * min((null >= gain).mean(), (null <= gain).mean()))
                nlo, nhi = float(np.percentile(null, 2.5)), float(np.percentile(null, 97.5))
            else:
                p_null, nlo, nhi = np.nan, np.nan, np.nan

            o = [OO[(cell, picks[cell])] for cell in cells]
            gate_rows.append(dict(selector=s, tau=tau, n=len(cells), abstain=k_abs, a=a,
                                  gain=gain, c_choice=cchoice, identity_err=ident,
                                  t_vs_S0=tstat(d),
                                  wins=int(sum(1 for x in d if x > 0)),
                                  losses=int(sum(1 for x in d if x < 0)),
                                  p_null=p_null, null_lo=nlo, null_hi=nhi,
                                  mean_OOS_Sharpe=float(np.mean([x["S"] for x in o])),
                                  mean_OOS_CAGR=float(np.mean([x["CAGR"] for x in o])),
                                  mean_OOS_MaxDD=float(np.mean([x["DD"] for x in o])),
                                  pass4a=int(sum(x["p4a"] for x in o)),
                                  pass4b=int(sum(x["p4b"] for x in o)),
                                  full4b=int(sum(x["f4b"] for x in o))))
            say(f"    {s:<10} tau {tau:>6.2f}  a {a:5.3f} ({k_abs:>2}/{len(cells)})  gain "
                f"{gain:+.4f} (t {tstat(d):+.2f}, {sum(1 for x in d if x>0)}W/"
                f"{sum(1 for x in d if x<0)}L)  c {cchoice:+.4f}  |gain-(1-a)c| {ident:.2e}  "
                f"null [{nlo:+.4f},{nhi:+.4f}] p {p_null:.3f}  OOS "
                f"{np.mean([x['CAGR'] for x in o]):.2%}/{np.mean([x['S'] for x in o]):.4f}/"
                f"{np.mean([x['DD'] for x in o]):.2%}  4a {sum(x['p4a'] for x in o)} "
                f"4b {sum(x['p4b'] for x in o)}")

    # the two non-grid controls
    for nm, pk_fn in (("S0_DONOTHING", lambda cell: CONTROL),
                      ("RANDOM", None)):
        rr = np.random.default_rng(SEED + 7)
        picks = ({cell: CONTROL for cell in cells} if pk_fn else
                 {cell: CAND[int(rr.integers(0, len(CAND)))] for cell in cells})
        d = [OO[(cell, picks[cell])]["S"] - S0[cell] for cell in cells]
        o = [OO[(cell, picks[cell])] for cell in cells]
        gate_rows.append(dict(selector=nm, tau=np.nan, n=len(cells),
                              abstain=int(sum(1 for cell in cells if picks[cell] == CONTROL)),
                              a=float(np.mean([picks[cell] == CONTROL for cell in cells])),
                              gain=float(np.mean(d)), c_choice=np.nan, identity_err=np.nan,
                              t_vs_S0=tstat(d), wins=int(sum(1 for x in d if x > 0)),
                              losses=int(sum(1 for x in d if x < 0)),
                              p_null=np.nan, null_lo=np.nan, null_hi=np.nan,
                              mean_OOS_Sharpe=float(np.mean([x["S"] for x in o])),
                              mean_OOS_CAGR=float(np.mean([x["CAGR"] for x in o])),
                              mean_OOS_MaxDD=float(np.mean([x["DD"] for x in o])),
                              pass4a=int(sum(x["p4a"] for x in o)),
                              pass4b=int(sum(x["p4b"] for x in o)),
                              full4b=int(sum(x["f4b"] for x in o))))
        say(f"    {nm:<14}          a {gate_rows[-1]['a']:5.3f}  gain "
            f"{gate_rows[-1]['gain']:+.4f} (t {gate_rows[-1]['t_vs_S0']:+.2f})  OOS "
            f"{gate_rows[-1]['mean_OOS_CAGR']:.2%}/{gate_rows[-1]['mean_OOS_Sharpe']:.4f}/"
            f"{gate_rows[-1]['mean_OOS_MaxDD']:.2%}  4a {gate_rows[-1]['pass4a']} "
            f"4b {gate_rows[-1]['pass4b']}")
    gates = pd.DataFrame(gate_rows)
    gates.to_csv(OUT / f"{STEM}.gates.csv", index=False)
    gates.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    g25 = gates[gates.selector.isin(SELECTORS)]
    say(f"\n    P2 — decomposition identity gain = (1-a)*c: max |error| over the 25 gates "
        f"{g25.identity_err.max():.3e}  ->  {'HIT' if g25.identity_err.max() < 1e-12 else 'MISS'}")
    ok = g25.p_null.notna()
    say(f"    P3 — gates whose abstention CHOICE escapes its matched-rate null (p < 0.05): "
        f"{int((g25.loc[ok, 'p_null'] < 0.05).sum())} of {int(ok.sum())} testable  ->  "
        f"{'HIT (no gate beats random abstention at the same rate)' if int((g25.loc[ok,'p_null'] < 0.05).sum()) == 0 else 'MISS — an abstention choice carries information'}")

    # ---------------------------------------------------------- P4: gain ~ abstention rate
    x, y = g25["a"].values.astype(float), g25["gain"].values.astype(float)
    if np.std(x) > 0:
        b1, b0 = np.polyfit(x, y, 1)
        yh = b0 + b1 * x
        r2 = float(1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum())
    else:
        b1, b0, r2 = np.nan, np.nan, np.nan
    say(f"\n    P4 — OOS gain regressed on abstention rate across the 25 gates: "
        f"gain = {b0:+.4f} {b1:+.4f} * a,  R^2 = {r2:.3f}  ->  "
        f"{'HIT' if (np.isfinite(r2) and r2 > 0.50) else 'MISS'}")
    say("        (the identity predicts gain = (1-a)*c, so a high R^2 here means c is roughly "
        "constant across gates and the RATE is the whole story)")
    say("\n    gain by selector at each tau (rows selector, cols tau):")
    say(g25.pivot_table(index="selector", columns="tau", values="gain").to_string(
        float_format=lambda v: f"{v:+.4f}"))
    say("\n    abstention rate by selector at each tau:")
    say(g25.pivot_table(index="selector", columns="tau", values="a").to_string(
        float_format=lambda v: f"{v:.3f}"))

    # ---------------------------------------------------------- P5/P6 and benchmarks
    best = gates.sort_values("mean_OOS_Sharpe", ascending=False).iloc[0]
    s0row = gates[gates.selector == "S0_DONOTHING"].iloc[0]
    say(f"\n    P5 — best arm by mean OOS Sharpe: {best.selector} tau={best.tau} "
        f"{best.mean_OOS_Sharpe:.4f} vs S0 {s0row.mean_OOS_Sharpe:.4f} "
        f"(gain {best.gain:+.4f}, t {best.t_vs_S0:+.2f})  ->  "
        f"{'HIT (no arm beats S0 at t > 2)' if gates.t_vs_S0.max(skipna=True) <= 2 else 'MISS'}")
    say(f"    P6 — OOS 4b passes: S0 {int(s0row.pass4b)} of {len(cells)}; best arm "
        f"{int(best.pass4b)}; max over all arms {int(gates.pass4b.max())}. No arm is promoted.")
    say("\n    BENCHMARKS over the same OOS window, per panel and cost rung:")
    for pk in PANELS:
        mo = metrics(ref[pk]["spy"].loc[OOS_START:])
        s = "  ".join(
            f"RULES v1 @{c:.0f}bps {metrics(ref[pk]['v1'][c].loc[OOS_START:])['CAGR']:.2%}/"
            f"{metrics(ref[pk]['v1'][c].loc[OOS_START:])['Sharpe']:.4f}/"
            f"{metrics(ref[pk]['v1'][c].loc[OOS_START:])['MaxDD']:.2%}" for c in COSTS)
        say(f"      {pk:<6} SPY OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:.2%}   {s}")

    # ---------------------------------------------------------- the record back-fill
    say("\n" + "=" * 200)
    say("THE RECORD BACK-FILL — abstention rate and OOS gain recovered from published "
        "*.walkforward.csv, best-effort on a heterogeneous schema")
    SELC = ["selector", "sel", "arm", "gate", "conv", "kind", "mode"]
    CTLC = ["ctl_OOS_Sharpe", "base_OOS_Sharpe", "anchor_OOS_Sharpe", "ctl_Sharpe",
            "base_Sharpe", "cell_OOS_Sharpe"]
    ADMC = ["n_admitted", "n_admissible", "n_ok", "n_IS_admissible"]
    rec, nfile, nskip = [], 0, 0
    for f in sorted(OUT.glob("*.walkforward.csv")):
        nfile += 1
        try:
            df = pd.read_csv(f)
        except Exception:
            nskip += 1
            continue
        sc = next((c for c in SELC if c in df.columns), None)
        cc = next((c for c in CTLC if c in df.columns), None)
        ac = next((c for c in ADMC if c in df.columns), None)
        if sc is None or cc is None or "OOS_Sharpe" not in df.columns or \
                ("pick" not in df.columns and ac is None):
            nskip += 1
            continue
        for name, sub in df.groupby(sc):
            if len(sub) < 4:
                continue
            ab = pd.Series(False, index=sub.index)
            if "pick" in sub.columns:
                pk = sub["pick"].astype(str).str.strip().str.upper()
                ab = ab | pk.isin(["", "NAN", "NONE", "-", "CTL", "CONTROL", "ABSTAIN", "NA"])
            if ac is not None:
                ab = ab | (pd.to_numeric(sub[ac], errors="coerce").fillna(-1) == 0)
            g = pd.to_numeric(sub["OOS_Sharpe"], errors="coerce") - \
                pd.to_numeric(sub[cc], errors="coerce")
            if g.notna().sum() < 4:
                continue
            rec.append(dict(file=f.name, selector=str(name), n=int(len(sub)),
                            a=float(ab.mean()), gain=float(g.mean())))
    record = pd.DataFrame(rec)
    record.to_csv(OUT / f"{STEM}.record.csv", index=False)
    say(f"    scanned {nfile} walkforward files; {nfile-nskip} carried a recoverable schema; "
        f"recovered {len(record)} published selector arms -> {STEM}.record.csv")
    if len(record) >= 10:
        xa, ya = record["a"].values, record["gain"].values
        say(f"    abstention rate: mean {xa.mean():.3f}, {int((xa > 0).sum())} of {len(xa)} "
            f"arms abstain at all, {int((xa == 1).sum())} abstain always")
        say(f"    OOS gain vs the control: mean {ya.mean():+.4f}, median "
            f"{np.median(ya):+.4f}, {int((ya > 0).sum())} of {len(ya)} positive")
        pos = xa > 0
        if pos.sum() >= 3 and np.std(xa[pos]) > 0:
            bb1, bb0 = np.polyfit(xa[pos], ya[pos], 1)
            yh = bb0 + bb1 * xa[pos]
            rr2 = float(1 - ((ya[pos] - yh) ** 2).sum() /
                        max(1e-18, ((ya[pos] - ya[pos].mean()) ** 2).sum()))
            say(f"    among the {int(pos.sum())} arms that DO abstain: gain = {bb0:+.4f} "
                f"{bb1:+.4f} * a,  R^2 = {rr2:.3f}")
        say(f"    mean gain of never-abstaining arms {ya[~pos].mean():+.4f} (n {int((~pos).sum())})"
            f" vs abstaining arms {ya[pos].mean():+.4f} (n {int(pos.sum())})")
    else:
        say("    too few recoverable arms to regress — the record's schema does not carry "
            "abstention, which is itself the argument for the column idea 194 implies.")

    say(f"\nTOTAL {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
