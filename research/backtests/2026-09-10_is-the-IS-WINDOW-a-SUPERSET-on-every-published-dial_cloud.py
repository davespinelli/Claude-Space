#!/usr/bin/env python3
"""QUEUE idea 614 — is-the-IS-WINDOW-a-SUPERSET-on-every-published-dial  (cloud, 2026-09-10)

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 614, written before any number below
was read)
    "idea 403 found the IS 4b window CONTAINS the full-sample window in 215/346 cells and its
     lower edge sits at or below the full one in 344/346, so an IS-screened dial systematically
     admits values the full sample rejects.  Test whether the same nesting holds on the record's
     other tuned dials (band, gross, K, n, vol) and whether a one-step inward margin repairs it.
     Max 2 params (dial, margin)."

WHY IT MATTERS
    Rule 8 forces every KEEP-candidate to choose its dial on the IS window alone.  If the IS
    4b-passing SET is systematically a SUPERSET of the full-sample one, then the rule-8 screen
    is not conservative — it is permissive, and every published "chosen on 2009-2016" constant
    was drawn from a menu that contains values the whole sample rejects.  Idea 403 measured that
    on ONE dial (the sleeve fraction f).  If the nesting is a property of the SCREEN it must
    reappear on every dial; if it is a property of f, the record's other dials are clean and
    403's finding does not generalise.  Either answer changes how a rule-8 pick is read.

THE MECHANISM AT ISSUE (stated before the design, because it drives the classification)
    The IS screen sees FOUR of the five 4b bars (H1, H2, DD, CAGR computed inside 2009-2016);
    the OOS bar is invisible to it by construction.  A four-bar screen on a SHORTER window is
    permissive for two separate reasons that this run separates:
      (a) MISSING BAR   — the OOS Sharpe bar cannot bind, so any value that fails full-4b on
                          the OOS bar ALONE is admitted by IS and rejected by full.
      (b) WINDOW NOISE  — the four shared bars are noisier on 8 years than on 17, so the IS
                          pass set is wider even where the same bars are what bind.
    Decomposing every false admit into (a) and (b) is the transferable part of this run: if the
    over-admission is (a), a margin cannot repair it — no amount of shrinking recovers a bar the
    screen cannot see.  If it is (b), a margin is the right instrument and the only question is
    how many steps.  This is stated as a prediction below and reported either way.

WHAT IS SWEPT (every point published in the .grid.csv; nothing is selected on but the two
tuned parameters)
    dials      band, n, gross, vol, K — idea 401's five ordered dials, IMPORTED verbatim from
               its committed script (`weights_for`, `DIALS`, `ADOPTED`, `CONTROL`), so the
               parameterisation is the record's, not this file's.  The off-dial controls
               ("nogate", "all", vol=none) are NOT interpolated into the ordered sweep — they
               are labels, not values — but each is run once per cell as the ABSTAIN comparand.
                 band  0, 2, 3, 5, 8 (%)            adopted 3
                 n     3, 5, 10, 20, 40             adopted 20
                 gross 0.10 .. 1.00 step 0.05 (19)  adopted 0.75
                 vol   0.30 .. 1.20 (7)             adopted 0.60
                 K     50, 100, 150, 200, 250, 300  adopted 200
    panels     u56 (universe.json), broad136 (universe_broad.json), SMALL439 (prices_small with
               data/small_meta.csv max_1d_move >= 1.0 dropped, idea 118; SPY held out).
    books      EWall and TOP20 (idea 401's two).
    costs      10 and 25 bps, both reported.
    = 42 ordered points x 2 books x 3 panels x 2 rungs + 5 controls x 2 x 3 x 2 = 564 runs.

DEGENERACY GATE (G3): the n dial does not exist on EWall — `book_weights` ignores n for that
    book — so the (EWall, n) cells are run anyway and ASSERTED identical across all five values.
    They are then excluded from every census rate rather than padding it with 6 free "windows".

WINDOW DEFINITION (idea 403's, so the numbers are comparable)
    A window is the HULL [lo, hi] of the dial values that pass on that window: full-sample 4b
    (five bars) for the full window, IS-window 4b (the four bars the IS screen can see) for the
    IS window.  Containment is hull containment: IS_lo <= full_lo AND IS_hi >= full_hi, over
    cells where BOTH hulls are non-empty — exactly the 346-cell denominator idea 403 published.
    The pass SET is published beside the hull so a non-contiguous set cannot hide inside it.

THE MARGIN (the queue's proposed repair, and the second tuned parameter)
    m steps inward on each side, in GRID-INDEX space: [lo_i + m, hi_i - m].  m in {0, 1, 2}.
    m = 0 is the unrepaired rule-8 screen.  An IS hull narrower than 2m + 1 points shrinks to
    EMPTY and the cell ABSTAINS to its dial's off-dial control, which is the record's own
    convention (idea 401's S1) and is run for every cell so the abstain arm is a real backtest,
    never an assumption.

TUNED PARAMETERS: exactly two, per PROTOCOL 4 — the DIAL (5 values) and the MARGIN (3 values).
    Panels, books, cost rungs, both KEEP paths and both selectors are REPORTED AXES, never
    selected on.  All 15 (dial, margin) grid points are published.

RULE 8 (PROTOCOL 8, required): the dial value is chosen on 2009-2016 ALONE — the highest
    IS-window Sharpe inside the margin-shrunk IS hull, a selector fixed before any OOS number
    was read — and 2017-2026 is then read ONCE.  OOS CAGR/Sharpe/MaxDD are reported against the
    LIVE RULES v2 book (cost-matched, PROTOCOL 3), RULES v1 (continuity) and SPY, per panel and
    rung.  The rule-8 question this idea owns is whether the MARGIN pays: does a screen that
    admits fewer values out of sample pick better out of sample?

KEEP PATHS (PROTOCOL 4, evaluated on EVERY arm row and on every rule-8 pick)
    4a  Sharpe > `baseline.rules_v2_weights` in BOTH halves and MaxDD no worse, cost-matched.
    4b  Sharpe > SPY in both halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of
        SPY's.
    Both are reported; neither is assumed.

GATES (all must print PASS before any new statistic is read)
    G1  idea 403's committed `.windows.csv` reproduces its two published rates EXACTLY off the
        file itself: 215/346 containment and 344/346 lower-edge.  This is the premise check.
    G2  the imported harness `H.run` equals `engine.backtest` with every instrument off.
    G3  the (EWall, n) degeneracy above.
    G4  IS and OOS windows are disjoint and exhaustive over the evaluated slice.

PRE-REGISTERED PREDICTIONS (written before the main grid was read)
    P1  Containment will be MUCH lower than f's 62.1% on the coarse dials (band, n, K, vol),
        because a 5-6 point grid cannot express a hull relation finely; the LOWER-EDGE rate is
        the statistic that will generalise, not containment.
    P2  The over-admission will be dominated by mechanism (a), the missing OOS bar — so the
        margin will NOT repair it, and m = 1 will cost more coverage than it buys in precision.
    P3  gross, the only fine grid here (19 points), is the dial where the margin has room to
        work and is where any repair will show up if one exists.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): all three panels are current-constituent lists; the small panel is
      a screen run TODAY and back-filled, with idea 118's max_1d_move filter applied first (idea
      627: that filter is itself terminal-dated and conservative on this panel).
    * The record's GROSS DIAL is a MULTIPLIER on a book already built at GROSS = 0.75, so dial
      value g realises 0.75g of gross.  Carried verbatim from idea 401 so the numbers are
      comparable; stated here because the label is not the exposure.
    * The IS screen sees four bars, not five.  That is the record's convention (idea 401's
      `margins_win`), and mechanism (a) above is its direct consequence, not a defect of this run.
    * MaxDD is one number off one path and the 4b DD cap turns on exactly that number (idea 321).
    * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
    * A hull is not a set.  Both are published; every rate below is computed on the hull, which
      is idea 403's convention, and the set-vs-hull disagreement rate is reported beside it.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .windows.csv,
.census.csv, .walkforward.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-10_is-the-IS-WINDOW-a-SUPERSET-on-every-published-dial_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I401 = OUT / "2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.py"
I403_WIN = OUT / "2026-09-10_is-the-4b-window-a-TURNOVER-COST-fact-about-the-ranked-book_B.windows.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I401, "i401")

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
PANELS = ["u56", "broad", "small"]
BOOKS = ["EWall", "TOP20"]
COSTS = [10.0, 25.0]
DIALS = ["band", "n", "gross", "vol", "K"]
MARGINS = [0, 1, 2]
BARS4 = ["H1", "H2", "DD", "CAGR"]
BARS5 = BARS4 + ["OOS"]

# ordered dial values only: off-dial controls are labels, not positions on the dial
ORDERED = {d: [v for v in C.DIALS[d] if not (isinstance(v, str) and v in C.OFF_DIAL)
               and not (isinstance(v, float) and not np.isfinite(v))] for d in DIALS}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def lab(v):
    return "none" if (isinstance(v, float) and not np.isfinite(v)) else str(v)


def rate(k, n):
    return f"{k}/{n} = {k / n:.1%}" if n else f"{k}/0 = n/a"


# ================================================================== main
def main():
    say("=" * 190)
    say("IDEA 614 — is the IS 4b WINDOW a SUPERSET of the full-sample window on EVERY published "
        "dial, and does a one-step inward MARGIN repair it?  (cloud)")
    say(f"5 dials x 2 books x 3 panels x 2 rungs.  IS <= {IS_END}, OOS >= {OOS_START}.  Weekly, "
        f"t+1, book gross {GROSS:.0%}, de-gross.  4b full = 5 bars; 4b IS = the 4 bars an IS "
        f"screen can see.")
    say("=" * 190)

    # ---------------------------------------------------------------- G1: idea 403's premise
    w403 = pd.read_csv(I403_WIN)
    b = w403[(~w403["is_empty"]) & (w403["IS_n_pass"] > 0)
             & w403["f_lo"].notna() & w403["IS_lo"].notna()]
    c403 = int(((b["IS_lo"] <= b["f_lo"] + 1e-12) & (b["IS_hi"] >= b["f_hi"] - 1e-12)).sum())
    l403 = int((b["IS_lo"] <= b["f_lo"] + 1e-12).sum())
    ok = (len(b) == 346 and c403 == 215 and l403 == 344)
    say(f"\n[G1] idea 403 committed windows: both-non-empty {len(b)} (published 346), "
        f"containment {c403} (215), lower-edge {l403} (344) -> {'PASS' if ok else 'FAIL'}")
    say(f"     f-dial reference rates: containment {c403 / len(b):.1%}, lower-edge {l403 / len(b):.1%}")
    if not ok:
        raise SystemExit("G1 failed — idea 403's premise does not reproduce off its own file")

    grid, wins, wf = [], [], []
    for pname in PANELS:
        px, spy, desc = C.panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        fbars, ibars = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        mS = metrics(spy)
        mSo = metrics(spy.loc[OOS_START:])
        say(f"\n{'-' * 190}\nPANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"  SPY full {mS['CAGR']:7.2%} / {mS['Sharpe']:.4f} / {mS['MaxDD']:7.2%}  halves "
            f"{fbars['s1']:.4f}/{fbars['s2']:.4f}  |  IS halves {ibars['s1']:.4f}/{ibars['s2']:.4f} "
            f"IS DD {ibars['sdd']:7.2%} IS CAGR {ibars['scagr']:7.2%}  |  OOS {mSo['CAGR']:7.2%} / "
            f"{mSo['Sharpe']:.4f} / {mSo['MaxDD']:7.2%}")

        if pname == "u56":
            Wc = H.targets(px, "EWall")
            a = H.run(px, Wc, bps=10.0)["r"].loc[start:]
            e = backtest(px, Wc, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
            d = float((a - e).abs().max())
            say(f"  [G2] H.run vs engine.backtest (EWall, 10bps): max|d| {d:.3e} -> "
                f"{'PASS' if d < 1e-12 else 'FAIL'}")
            isl, ol = spy.loc[:IS_END], spy.loc[OOS_START:]
            say(f"  [G4] IS {isl.index[0].date()}..{isl.index[-1].date()} ({len(isl)}) / OOS "
                f"{ol.index[0].date()}..{ol.index[-1].date()} ({len(ol)}); overlap "
                f"{len(isl.index.intersection(ol.index))}, union {len(isl) + len(ol)} vs {len(spy)} "
                f"-> {'PASS' if len(isl.index.intersection(ol.index)) == 0 and len(isl) + len(ol) == len(spy) else 'FAIL'}")

        base_r, v1_r = {}, {}
        for c in COSTS:
            base_r[c] = H.run(px, rules_v2_weights(px), bps=c)["r"].loc[start:]
            v1_r[c] = H.run(px, rules_v1_weights(px), bps=c)["r"].loc[start:]
            mb, mo = metrics(base_r[c]), metrics(base_r[c].loc[OOS_START:])
            say(f"  RULES v2 @{c:.0f}bps  full {mb['CAGR']:7.2%} / {mb['Sharpe']:.4f} / "
                f"{mb['MaxDD']:7.2%}   OOS {mo['CAGR']:7.2%} / {mo['Sharpe']:.4f} / {mo['MaxDD']:7.2%}")

        for book in BOOKS:
            for c in COSTS:
                for dial in DIALS:
                    vals = ORDERED[dial] + [C.CONTROL[dial]]
                    cell = []
                    for gi, v in enumerate(vals):
                        W, m = C.weights_for(px, book, dial, v)
                        r = H.run(px, W, m=m, bps=c)["r"].loc[start:]
                        fm = C.margins_win(r, fbars, "full")
                        im = C.margins_win(r, ibars, "IS")
                        mf, mo = metrics(r), metrics(r.loc[OOS_START:])
                        mi = metrics(r.loc[:IS_END])
                        is_ctrl = (gi == len(vals) - 1)
                        row = dict(panel=pname, book=book, cost=c, dial=dial, value=lab(v),
                                   gidx=(-1 if is_ctrl else gi), is_control=is_ctrl,
                                   adopted=(not is_ctrl and v == C.ADOPTED[dial]),
                                   CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                   IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                   pass4a=H.pass4a(r, base_r[c]))
                        for k in BARS5:
                            row["f_" + k] = fm[k]
                        for k in BARS4:
                            row["i_" + k] = im[k]
                        row["pass_full"] = bool(all(fm[k] > 0 for k in BARS5))
                        row["pass_IS"] = bool(all(im[k] > 0 for k in BARS4))
                        # decomposition of a false admit: which bars would have to bind
                        row["only_OOS_fails"] = bool(fm["OOS"] <= 0 and all(fm[k] > 0 for k in BARS4))
                        cell.append(row)
                        grid.append(row)

                    d = pd.DataFrame(cell)
                    o = d[~d["is_control"]].reset_index(drop=True)
                    if book == "EWall" and dial == "n":
                        span = float(o[["CAGR", "Sharpe", "MaxDD"]].std().max())
                        say(f"  [G3] ({pname},{book},{c:.0f}bps,n) degeneracy: max sd over the 5 "
                            f"values {span:.3e} -> {'PASS' if span < 1e-12 else 'FAIL'}")

                    fi = list(np.flatnonzero(o["pass_full"].values))
                    ii = list(np.flatnonzero(o["pass_IS"].values))
                    wr = dict(panel=pname, book=book, cost=c, dial=dial, npts=len(o),
                              degenerate=(book == "EWall" and dial == "n"),
                              f_n=len(fi), i_n=len(ii),
                              f_lo=(min(fi) if fi else np.nan), f_hi=(max(fi) if fi else np.nan),
                              i_lo=(min(ii) if ii else np.nan), i_hi=(max(ii) if ii else np.nan),
                              f_vals="|".join(o["value"][fi]), i_vals="|".join(o["value"][ii]),
                              f_contig=(len(fi) == (max(fi) - min(fi) + 1) if fi else np.nan),
                              i_contig=(len(ii) == (max(ii) - min(ii) + 1) if ii else np.nan),
                              set_contain=(set(fi) <= set(ii) if (fi and ii) else np.nan))
                    wins.append(wr)

    G = pd.DataFrame(grid)
    Wd = pd.DataFrame(wins)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    Wd.to_csv(OUT / f"{STEM}.windows.csv", index=False)
    say(f"\n{'=' * 190}\nGRID: {len(G)} arm rows ({int((~G['is_control']).sum())} ordered + "
        f"{int(G['is_control'].sum())} controls), {len(Wd)} cells "
        f"({int((~Wd['degenerate']).sum())} non-degenerate).  All published in .grid.csv / "
        f".windows.csv.")

    # ---------------------------------------------------------------- A1: the nesting census
    say(f"\n{'=' * 190}\nA1  THE NESTING CENSUS — does the IS window CONTAIN the full-sample window?")
    N = Wd[~Wd["degenerate"]].copy()
    both = N[(N["f_n"] > 0) & (N["i_n"] > 0)].copy()
    both["contain"] = (both["i_lo"] <= both["f_lo"]) & (both["i_hi"] >= both["f_hi"])
    both["loedge"] = both["i_lo"] <= both["f_lo"]
    both["wider"] = both["i_n"] >= both["f_n"]
    say(f"  cells with BOTH windows non-empty: {len(both)} of {len(N)}  "
        f"(full empty {int((N['f_n'] == 0).sum())}, IS empty {int((N['i_n'] == 0).sum())})")
    say(f"  CONTAINMENT   {rate(int(both['contain'].sum()), len(both))}   "
        f"[idea 403 on f: {c403}/{len(b)} = {c403 / len(b):.1%}]")
    say(f"  LOWER EDGE    {rate(int(both['loedge'].sum()), len(both))}   "
        f"[idea 403 on f: {l403}/{len(b)} = {l403 / len(b):.1%}]")
    say(f"  IS SET WIDER  {rate(int(both['wider'].sum()), len(both))}")
    per = both.groupby("dial").agg(cells=("contain", "size"), contain=("contain", "sum"),
                                   loedge=("loedge", "sum"), wider=("wider", "sum"),
                                   f_n=("f_n", "mean"), i_n=("i_n", "mean"))
    per["contain%"] = per["contain"] / per["cells"]
    per["loedge%"] = per["loedge"] / per["cells"]
    say("\n  per dial:")
    say(per.to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  per panel x rung:")
    pp = both.groupby(["panel", "cost"]).agg(cells=("contain", "size"), contain=("contain", "sum"),
                                             loedge=("loedge", "sum"))
    say(pp.to_string())
    ncont = int(((~N["f_contig"].fillna(True)) | (~N["i_contig"].fillna(True))).sum())
    say(f"\n  hull-vs-set: {ncont} of {len(N)} cells have a NON-CONTIGUOUS pass set, so the hull "
        f"overstates that cell's window.  Every set is published in .windows.csv.")
    say(f"  SET containment (IS pass SET superset of the full pass SET, the strict form the hull "
        f"overstates): {rate(int(both['set_contain'].sum()), len(both))}")

    say("\n  THE 12 CELLS IN FULL (grid indices; every value in .windows.csv):")
    say(both[["panel", "book", "cost", "dial", "f_n", "f_lo", "f_hi", "i_n", "i_lo", "i_hi",
              "contain", "set_contain", "loedge", "f_vals", "i_vals"]].to_string(index=False))

    # exact binomial read of the lower-edge break against idea 403's published rate
    from math import comb
    p403 = l403 / len(b)
    k = int(both["loedge"].sum())
    n = len(both)
    pv = sum(comb(n, j) * p403 ** j * (1 - p403) ** (n - j) for j in range(0, k + 1))
    say(f"\n  LOWER-EDGE break, exact binomial: P(X <= {k} | n = {n}, p = {p403:.4f}) = {pv:.3e}.")
    say(f"  WHY THE DENOMINATOR IS THIN, stated not hidden: the FULL 4b window is EMPTY in "
        f"{int((N['f_n'] == 0).sum())} of {len(N)} cells and the IS window in "
        f"{int((N['i_n'] == 0).sum())} — on these five dials the book mostly fails 4b EVERYWHERE, "
        f"so only {n} cells can carry a nesting relation at all.")
    say(both.groupby("dial")[["contain", "set_contain", "loedge"]].sum().to_string())
    say("\n  empty-window rate per dial (full / IS, of 12 cells each, 6 for n):")
    emp = N.groupby("dial").agg(cells=("f_n", "size"), full_empty=("f_n", lambda s: int((s == 0).sum())),
                                IS_empty=("i_n", lambda s: int((s == 0).sum())))
    say(emp.to_string())

    # ---------------------------------------------------------------- A2: over-admission + margin
    say(f"\n{'=' * 190}\nA2  OVER-ADMISSION AND THE MARGIN — all 15 (dial, margin) grid points")
    cen = []
    for dial in DIALS:
        for m in MARGINS:
            adm = fa = fa_oosonly = tot_full = cov = 0
            cells = emptied = 0
            for _, w in N[N["dial"] == dial].iterrows():
                sub = G[(G["panel"] == w["panel"]) & (G["book"] == w["book"])
                        & (G["cost"] == w["cost"]) & (G["dial"] == dial) & (~G["is_control"])]
                sub = sub.sort_values("gidx")
                pf = sub["pass_full"].values
                oo = sub["only_OOS_fails"].values
                cells += 1
                tot_full += int(pf.sum())
                if w["i_n"] == 0:
                    emptied += 1
                    continue
                lo, hi = int(w["i_lo"]) + m, int(w["i_hi"]) - m
                if lo > hi:
                    emptied += 1
                    continue
                sel = np.zeros(len(pf), bool)
                sel[lo:hi + 1] = True
                adm += int(sel.sum())
                fa += int((sel & ~pf).sum())
                fa_oosonly += int((sel & ~pf & oo).sum())
                cov += int((sel & pf).sum())
            cen.append(dict(dial=dial, margin=m, cells=cells, emptied=emptied, admitted=adm,
                            false_admits=fa, fa_rate=(fa / adm if adm else np.nan),
                            fa_only_OOS_bar=fa_oosonly,
                            fa_share_missing_bar=(fa_oosonly / fa if fa else np.nan),
                            full_passers=tot_full, covered=cov,
                            coverage=(cov / tot_full if tot_full else np.nan)))
    CEN = pd.DataFrame(cen)
    CEN.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say(CEN.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    pool = CEN.groupby("margin").agg(admitted=("admitted", "sum"), false_admits=("false_admits", "sum"),
                                     fa_only_OOS_bar=("fa_only_OOS_bar", "sum"),
                                     covered=("covered", "sum"), full_passers=("full_passers", "sum"),
                                     emptied=("emptied", "sum"))
    pool["fa_rate"] = pool["false_admits"] / pool["admitted"]
    pool["share_missing_bar"] = pool["fa_only_OOS_bar"] / pool["false_admits"]
    pool["coverage"] = pool["covered"] / pool["full_passers"]
    say("\n  POOLED over the five dials:")
    say(pool.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- A3: rule 8
    say(f"\n{'=' * 190}\nA3  RULE 8 — dial chosen on 2009-2016 alone (max IS-window Sharpe inside the "
        f"margin-shrunk IS hull; abstain to the control when empty), 2017-2026 read ONCE")
    for pname in PANELS:
        px, spy, _ = C.panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        sO = metrics(spy.loc[OOS_START:])
        for c in COSTS:
            bO = metrics(H.run(px, rules_v2_weights(px), bps=c)["r"].loc[start:].loc[OOS_START:])
            vO = metrics(H.run(px, rules_v1_weights(px), bps=c)["r"].loc[start:].loc[OOS_START:])
            for book in BOOKS:
                for dial in DIALS:
                    if book == "EWall" and dial == "n":
                        continue
                    w = N[(N["panel"] == pname) & (N["book"] == book) & (N["cost"] == c)
                          & (N["dial"] == dial)].iloc[0]
                    sub = G[(G["panel"] == pname) & (G["book"] == book) & (G["cost"] == c)
                            & (G["dial"] == dial)].sort_values("gidx")
                    ordr = sub[~sub["is_control"]].reset_index(drop=True)
                    ctrl = sub[sub["is_control"]].iloc[0]
                    for m in MARGINS:
                        abst = True
                        pick = ctrl
                        if w["i_n"] > 0:
                            lo, hi = int(w["i_lo"]) + m, int(w["i_hi"]) - m
                            if lo <= hi:
                                cand = ordr.iloc[lo:hi + 1]
                                pick = cand.loc[cand["IS_Sharpe"].idxmax()]
                                abst = False
                        wf.append(dict(panel=pname, book=book, cost=c, dial=dial, margin=m,
                                       pick=pick["value"], abstained=abst,
                                       is_adopted=bool(pick["adopted"]),
                                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                                       OOS_MaxDD=pick["OOS_MaxDD"],
                                       base_OOS_Sharpe=bO["Sharpe"], base_OOS_CAGR=bO["CAGR"],
                                       base_OOS_MaxDD=bO["MaxDD"],
                                       v1_OOS_Sharpe=vO["Sharpe"], spy_OOS_Sharpe=sO["Sharpe"],
                                       spy_OOS_CAGR=sO["CAGR"], spy_OOS_MaxDD=sO["MaxDD"],
                                       beat_SPY_oos=bool(pick["OOS_Sharpe"] > sO["Sharpe"]),
                                       beat_base_oos=bool(pick["OOS_Sharpe"] > bO["Sharpe"]),
                                       pass4a=bool(pick["pass4a"]), pass4b=bool(pick["pass_full"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    s = WF.groupby("margin").agg(picks=("pick", "size"), abstained=("abstained", "sum"),
                                 adopted=("is_adopted", "sum"),
                                 OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                                 OOS_MaxDD=("OOS_MaxDD", "mean"),
                                 beat_SPY=("beat_SPY_oos", "sum"), beat_base=("beat_base_oos", "sum"),
                                 p4a=("pass4a", "sum"), p4b=("pass4b", "sum"))
    say(s.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"\n  comparands (mean over the 9 book x dial cells per panel x rung): SPY OOS Sharpe "
        f"{WF['spy_OOS_Sharpe'].mean():.4f}, RULES v2 {WF['base_OOS_Sharpe'].mean():.4f}, "
        f"RULES v1 {WF['v1_OOS_Sharpe'].mean():.4f}")
    say("\n  per dial x margin (mean OOS Sharpe of the pick):")
    say(WF.pivot_table(index="dial", columns="margin", values="OOS_Sharpe", aggfunc="mean")
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  per panel x margin (mean OOS Sharpe of the pick, SPY in brackets):")
    for pn in PANELS:
        sp = WF[WF["panel"] == pn]
        row = " ".join(f"m{m} {sp[sp['margin'] == m]['OOS_Sharpe'].mean():.4f}" for m in MARGINS)
        say(f"    {pn:6s} {row}   [SPY {sp['spy_OOS_Sharpe'].iloc[0]:.4f}, "
            f"RULES v2 {sp['base_OOS_Sharpe'].mean():.4f}]")

    # ---------------------------------------------------------------- KEEP paths
    say(f"\n{'=' * 190}\nKEEP PATHS on every arm row: 4a {int(G['pass4a'].sum())}/{len(G)}, "
        f"4b {int(G['pass_full'].sum())}/{len(G)}.  On the {len(WF)} rule-8 picks: "
        f"4a {int(WF['pass4a'].sum())}, 4b {int(WF['pass4b'].sum())}.")
    k = G[G["pass_full"] & G["pass4a"]]
    if len(k):
        say("  arms passing BOTH paths:")
        say(k[["panel", "book", "cost", "dial", "value", "CAGR", "Sharpe", "MaxDD",
               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("  no arm passes both paths.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
