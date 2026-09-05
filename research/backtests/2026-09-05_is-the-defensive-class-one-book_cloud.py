#!/usr/bin/env python3
"""QUEUE idea 133 — is-the-defensive-class-one-book-in-disguise  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 133)
    "idea 129's 11 Pareto-best floor-only KILLs are ALL EWall + a slow trend gate de-grossed to
     cash at ~53% gross, across two panels and both cost rungs.  Test whether the `4b-defensive`
     class has any member that is not that construction: run the same census over the
     leaderboard's ranked and sleeve books at matched gross.  If the class has exactly one
     member, PROTOCOL should name the book, not the class."

    `4b-defensive` (idea 129's proposed PROTOCOL class) = an arm that clears 4b's two halves
    bars, its OOS-Sharpe bar and its drawdown cap, and fails ONLY the CAGR floor.

AUDIT OF THE PREMISE, BEFORE ANY NEW NUMBER (from idea 129's own published .grid.csv)
    The queue's sentence is very slightly overstated by its own source, and this run says so
    first rather than inheriting it: of the 11 Pareto-best floor-only KILLs, **10** are
    EWall + a trend gate in the de-grossing convention, and the 11th is
    `broad / EWall / 25bps / ddctl-8/.5/recover` at 0.661 gross — a book-level drawdown
    control, not a gate.  In the wider floor-only set (27 rows) **26 of 27 are EWall** but only
    **25 of 27 are `dg`**: `g200-rw` and `v1gate-rw` are already there, and one member is
    `TOP20 / ddctl-8/.5/high`.  So the honest form of the queue's claim is "one BOOK", not "one
    construction", and this run tests the book claim on a corpus the book cannot dominate by
    default.  CHECK (b) below re-derives those counts from idea 129's file rather than trusting
    this paragraph.

WHY THE NARROW CORPUS COULD MANUFACTURE THE ANSWER
    Idea 129's corpus is 3 books: V1u (5 names, 0.15 each = 0.75 gross), TOP20 and EWall.  Two of
    the three are concentrated momentum books whose CAGR is far above SPY, so no overlay can push
    them into the floor-only band without also breaching something else; EWall is the only
    diversified book in the corpus.  A class that contains only EWall may therefore be a
    statement about the CORPUS, not about the world.  The fix is to widen the book family along
    the two axes the leaderboard actually publishes — position count and the multi-asset sleeve —
    while holding gross MATCHED at 0.75 so no book wins by simply being smaller.

CORPUS (every book at matched gross 0.75; nothing is invented, all are published constructions)
    EWall     equal-weight every live name                                (idea 129's incumbent)
    V1u       RULES v1 unscaled book, 5 names x 0.15                      (idea 94)
    R5/R10/R20/R40   composite-ranked top-n, 0.75/n each                  (idea 2 family; R20 = TOP20)
    S3-25/S3-50      (1-f) x R20 + f x sleeve(TLT,GLD,UUP), rescaled to 0.75   (ideas 100/104)
    S4-50            (1-f) x R20 + f x sleeve(TLT,GLD,DBC,UUP), rescaled       (idea 100)
    Sleeve books exist on u56 and broad only (the small panel has no TLT/GLD/UUP/DBC).
    INSTRUMENTS: idea 94's 17 arms unchanged — control, 5 gates x {dg, rw}, 2 stops, 2 book
    drawdown controls, 2 entry budgets.  Panels u56 / broad / small.  Costs 10 and 25 bps.
    = 816 arm-rows, every one printed and written to .grid.csv.
    LADDER CONTROL: each book also run at static gross multiplier m in {0.40,0.50,0.60,0.80,1.00}
    (240 rows), because "de-grossed to ~53%" is a hypothesis about EXPOSURE that the ladder tests
    directly: if the class is really an exposure band, the ladder should walk any book into it.

TUNED PARAMETERS — exactly two: position count n in {5,10,20,40} and sleeve fraction f in
    {0.25,0.50}.  All values reported.  Panels, gates, conventions, overlays, cost rungs, the
    ladder and both KEEP paths are reported axes, never selected on.

HARNESS
    Idea 94's script is IMPORTED, not re-implemented (`H.run`, `H.targets`, `H.gate_mask`,
    `H.margins`, `H.pass4a`, `H.arm_specs`, `H.bars_of`), so every number sits on the simulator
    that produced the rows being generalised.  Checks run before any new number is read:
      (a) every book's ungated control vs `engine.backtest` — must be exact;
      (b) idea 129's premise counts re-derived from its .grid.csv;
      (c) idea 94's published `EWall + vol60-dg` u56 @10bps row (11.6% / 1.133 / -16.9%);
      (d) this run's V1u/TOP20/EWall rows must equal idea 129's grid rows arm-for-arm.

WALK-FORWARD (PROTOCOL rule 8; selectors fixed in writing before any OOS number is read)
    S0  argmax IS Sharpe over the whole widened corpus in the (panel, cost) cell.
    S1  argmax IS Sharpe among arms whose IS window alone clears 4b's halves bars, its DD cap
        (delta=0.60) and its CAGR floor (phi=0.70).
    S2  the same with the floor deleted (phi=0.00) — the screen that ADMITS the defensive class.
    Each pick is read once on 2017-2026 against its cell's ungated control, RULES v1 and SPY.
    Idea 129 found S1 = S2 in 18/18 cells on the narrow corpus; if the class is broader than one
    book, the widened corpus is where that equality should break.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  The class is NOT one book: the widened corpus contains at least one 4b-defensive member
        whose book is not EWall.
    P2  But it IS one exposure band: every 4b-defensive member has mean realised gross < 0.70,
        and the ladder control puts at least one non-EWall book into the class by de-grossing
        alone.  (P1 and P2 together mean PROTOCOL should name the exposure, not the book.)
    P3  Among the Pareto-best (Sharpe, MaxDD) members of the class, EWall is still the majority.
    P4  Fewer than 25% of the class's members are matched-gross (`rw`) arms — the de-grossing
        convention is how an arm gets into the class, not which book it is.
    P5  On the widened corpus S1 and S2 pick a different arm in at least one (panel, cost) cell,
        breaking idea 129's 0-of-18.

CAVEATS carried, not buried
    * Survivorship: three current-constituent panels (idea 54); the small panel additionally
      drops the 44 tickers with `max_1d_move >= 1.0` (439 names) and SPY there is a joined
      benchmark, never selectable.  Absent delistings inflate every arm's CAGR and inflate the
      UNGATED books most, so the floor's exclusion of defensive arms is if anything understated.
      No level here is an achievable return.
    * Idea 128: the IS window (SPY MaxDD -22.1%) is shallower than OOS (-33.7%), so an IS-window
      drawdown cap is measured on a window that cannot express deep drawdowns; this biases the
      S1/S2 screens toward admitting too much.
    * Idea 126: every row is quoted at t+1 execution only.
    * Idea 127 (this sprint): a gated row is a joint statement about the gate and about cash, so
      mean gross is reported on every row here and the `dg`/`rw` split is never collapsed.
    * This run cannot promote a candidate — it is a census of a PROTOCOL class.

Deterministic, standalone.  Imports research/baseline.py and idea 94's script; modifies nothing.
Writes .console.txt, .grid.csv, .ladder.csv, .census.csv and .walkforward.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_is-the-defensive-class-one-book_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129_GRID = OUT / "2026-09-05_cagr-floor-calibration_B.grid.csv"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

# idea 129's census machinery is imported too, so "the same census" is literally the same code:
# bars_win / margins_at / fails / pareto_front are used unchanged.
_spec129 = importlib.util.spec_from_file_location("i129", OUT / "2026-09-05_cagr-floor-calibration_B.py")
C = importlib.util.module_from_spec(_spec129)
_spec129.loader.exec_module(C)

FREQ, GROSS, COSTS = H.FREQ, H.GROSS, H.COSTS
IS_END, OOS_START = H.IS_END, H.OOS_START
NS = [5, 10, 20, 40]
FS = [0.25, 0.50]
LADDER_M = [0.40, 0.50, 0.60, 0.80, 1.00]
S3, S4 = ["TLT", "GLD", "UUP"], ["TLT", "GLD", "DBC", "UUP"]
PHI, DELTA = 0.70, 0.60
BAD_MOVE = 1.0

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ books ----
def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """Ideas 100/104's sleeve: momentum vote x risk parity over the diversifier assets."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def ranked(px, n, gate=None, conv="dg"):
    """Composite-ranked top-n at 0.75/n, gate applied in the dg or rw convention."""
    s = H.composite(px)
    g = H.gate_mask(px, gate)
    if gate is not None and conv == "rw":
        s = s.where(g)
    w = (s.rank(axis=1, ascending=False) <= n).astype(float) * (GROSS / n)
    if gate is not None and conv == "dg":
        w = w.where(g, 0.0)
    return w


def book_weights(px, book, gate=None, conv="dg"):
    """Every book in the widened corpus, at MATCHED gross 0.75 before any gate is applied."""
    if book in ("EWall", "V1u", "TOP20"):
        return H.targets(px, book, gate, conv)                 # idea 94/129, unchanged
    if book.startswith("R"):
        return ranked(px, int(book[1:]), gate, conv)
    if book.startswith("S"):                                    # sleeve blend, rescaled to GROSS
        assets = S3 if book.startswith("S3") else S4
        f = int(book.split("-")[1]) / 100.0
        base = (1 - f) * ranked(px, 20) + f * sleeve_weights(px, assets)     # ungated blend
        B = base.mul((GROSS / base.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0)
        if gate is None:
            return B.fillna(0.0)
        gm = H.gate_mask(px, gate)
        if conv == "dg":
            return B.where(gm, 0.0).fillna(0.0)                 # gated-out weight goes to CASH
        w = (1 - f) * ranked(px, 20, gate, "rw") + f * sleeve_weights(px, assets).where(gm, 0.0)
        return w.mul((GROSS / w.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)
    raise ValueError(book)


def books_for(panel, px):
    b = ["EWall", "V1u"] + [f"R{n}" for n in NS]
    if all(t in px.columns for t in S4):
        b += [f"S3-{int(f*100)}" for f in FS] + ["S4-50"]
    return b


def panel_px(name):
    """Idea 129's construction verbatim: SPY is a selectable constituent on u56/broad and is
    HELD OUT of the small panel, where it is only the benchmark return series."""
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= BAD_MOVE, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0)
    px = load_universe(broad=(name == "broad"))
    return px, px["SPY"].pct_change().fillna(0.0)


# ------------------------------------------------------------------ main ----
def main():
    # ---- (b) audit of the queue's premise against idea 129's own file ----
    say("[b] PREMISE AUDIT — idea 129's published grid, re-derived here")
    g129 = pd.read_csv(I129_GRID)
    fo = g129[g129.floor_only]
    pb = g129[g129.floor_only & g129.pareto]
    say(f"    floor-only rows: {len(fo)} of {len(g129)}; Pareto-best floor-only: {len(pb)}")
    say(f"    Pareto-best by book: {dict(pb.book.value_counts())}; by arm kind: "
        f"{dict(pb.kind.value_counts())}; gross {pb.gross.min():.3f}..{pb.gross.max():.3f} "
        f"(mean {pb.gross.mean():.3f})")
    say(f"    Pareto-best that are NOT 'EWall + gate + dg': "
        f"{[f'{r.panel}/{r.book}/{r.cost:.0f}bps/{r.arm}' for r in pb.itertuples() if not (r.book == 'EWall' and r.kind == 'gate' and r.arm.endswith('-dg'))]}")
    say(f"    all floor-only by book: {dict(fo.book.value_counts())}; by convention: "
        f"dg {int(fo.arm.str.endswith('-dg').sum())}, rw {int(fo.arm.str.endswith('-rw').sum())}, "
        f"other {int((~fo.arm.str.endswith(('-dg', '-rw'))).sum())}")

    rows, lrows, rets = [], [], {}
    ref = {}
    for pk in ("u56", "broad", "small"):
        px, spy_full = panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bars, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        ms = metrics(spy)
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        BK = books_for(pk, px)
        ref[pk] = dict(bars=bars, spy=ms, v1=v1, start=start, books=BK)
        say(f"\n[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()} | books: {', '.join(BK)}")
        say(f"    SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {bars['s1']:.3f}/{bars['s2']:.3f} OOS {bars['soos']:.3f} | 4b bars: MaxDD <= "
            f"{DELTA*abs(ms['MaxDD']):.2%}, CAGR >= {PHI*ms['CAGR']:.2%}")
        worst = 0.0
        for b in BK:
            W = book_weights(px, b)
            a = H.run(px, W, bps=10.0)["r"].loc[start:]
            e = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
            worst = max(worst, float((a - e).abs().max()))
        say(f"[a] engine-equivalence over {len(BK)} ungated books: max|diff| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — unsafe'})")

        for b in BK:
            for name, kind, kwargs, (gt, conv) in H.arm_specs():
                W = book_weights(px, b, gt, conv)
                for c in COSTS:
                    res = H.run(px, W, bps=c, **kwargs)
                    r = res["r"].loc[start:]
                    rets[(pk, b, name, c)] = r
                    mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
                    h1, h2 = H.halves(r)
                    mg = C.margins_at(r, bars, PHI, DELTA, "full")
                    ismg = C.margins_at(r, bIS, PHI, DELTA, "IS")
                    fail = C.fails(mg)
                    rows.append(dict(
                        panel=pk, book=b, arm=name, kind=kind, conv=("rw" if name.endswith("-rw")
                                                                     else "dg" if name.endswith("-dg") else "-"),
                        cost=c, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        gross=res["gross"].loc[start:].mean(),
                        TO=res["to"].loc[start:].sum() / mm["Years"],
                        m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                        IS_m_H1=ismg["H1"], IS_m_H2=ismg["H2"], IS_m_DD=ismg["DD"], IS_m_CAGR=ismg["CAGR"],
                        pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-", n_fail=len(fail),
                        floor_only=(fail == ["CAGR"]), pass4a=H.pass4a(r, v1[c])))
            for m_ in LADDER_M:                     # ladder control: pure de-grossing, no rule
                for c in COSTS:
                    res = H.run(px, book_weights(px, b), m=m_, bps=c)
                    r = res["r"].loc[start:]
                    mm = metrics(r)
                    mg = C.margins_at(r, bars, PHI, DELTA, "full")
                    fail = C.fails(mg)
                    lrows.append(dict(panel=pk, book=b, m=m_, cost=c, CAGR=mm["CAGR"],
                                      Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                      gross=res["gross"].loc[start:].mean(),
                                      OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                      pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-",
                                      floor_only=(fail == ["CAGR"])))

    df = pd.DataFrame(rows)
    lad = pd.DataFrame(lrows)

    # Pareto frontier on (Sharpe, MaxDD) within each (panel, cost) cell, over the whole corpus
    df["pareto"] = False
    for (pk, c), s in df.groupby(["panel", "cost"]):
        df.loc[s.index, "pareto"] = C.pareto_front(s)           # idea 129's own function
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)

    # ---- (d) reproduction of idea 129's rows ----
    df["book129"] = df.book.replace({"R20": "TOP20"})           # R20 IS idea 94's TOP20 book
    j = df.merge(g129.rename(columns={"book": "book129"}), on=["panel", "book129", "cost", "arm"],
                 suffixes=("", "_129"))
    diffs = {k: float((j[k] - j[f"{k}_129"]).abs().max()) for k in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe")}
    say(f"\n[d] reproduction of idea 129's 306 rows on the shared books: {len(j)} matched rows, "
        f"max|diff| " + " ".join(f"{k} {v:.2e}" for k, v in diffs.items()))
    v = df[(df.panel == "u56") & (df.book == "EWall") & (df.arm == "vol60-dg") & (df.cost == 10.0)].iloc[0]
    say(f"[c] idea 94's published EWall+vol60-dg u56 @10bps 11.6%/1.133/-16.9% -> this run "
        f"{v.CAGR:.1%}/{v.Sharpe:.3f}/{v.MaxDD:.1%}")

    say(f"\n[GRID] {len(df)} arm-rows, ALL reported")
    cols = ["panel", "book", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "gross", "TO", "pass4a", "pass4b", "fail4b", "floor_only", "pareto"]
    with pd.option_context("display.width", 260, "display.max_rows", None):
        say(df[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        say(f"\n[LADDER] {len(lad)} static-gross control rows, ALL reported")
        say(lad.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- the census ----
    D = df[df.floor_only]
    say(f"\n[CENSUS] 4b-defensive (clears halves, OOS and the DD cap; fails ONLY the CAGR floor): "
        f"{len(D)} of {len(df)} arm-rows ({len(D)/len(df):.1%}); 4b passes {int(df.pass4b.sum())}, "
        f"4a passes {int(df.pass4a.sum())}")
    say(f"[CENSUS] by book: {dict(D.book.value_counts())}")
    say(f"[CENSUS] by panel: {dict(D.panel.value_counts())} | by cost: {dict(D.cost.value_counts())}")
    say(f"[CENSUS] by overlay kind: {dict(D.kind.value_counts())} | by convention: "
        f"{dict(D.conv.value_counts())}")
    say(f"[CENSUS] gross of the class: min {D.gross.min():.3f} p25 {D.gross.quantile(.25):.3f} "
        f"median {D.gross.median():.3f} p75 {D.gross.quantile(.75):.3f} max {D.gross.max():.3f}; "
        f"non-class arms median {df[~df.floor_only].gross.median():.3f}")
    nonE = D[D.book != "EWall"]
    say(f"[CENSUS] members that are NOT EWall: {len(nonE)} of {len(D)}")
    if len(nonE):
        with pd.option_context("display.width", 260, "display.max_rows", None):
            say(nonE[["panel", "book", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe",
                      "gross", "m_CAGR", "pareto"]].to_string(index=False,
                                                              float_format=lambda x: f"{x:.3f}"))
    say(f"[CENSUS] members that are NOT 'EWall + gate + dg': "
        f"{int((~((D.book == 'EWall') & (D.kind == 'gate') & (D.conv == 'dg'))).sum())} of {len(D)}")
    PB = D[D.pareto]
    say(f"[CENSUS] Pareto-best (Sharpe, MaxDD) members within their (panel, cost) cell: {len(PB)}; "
        f"by book {dict(PB.book.value_counts())}")
    if len(PB):
        with pd.option_context("display.width", 260, "display.max_rows", None):
            say(PB[["panel", "book", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "gross",
                    "m_CAGR"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"[CENSUS] distinct (book, arm) constructions in the class: "
        f"{len(D.groupby(['book', 'arm']))} -> "
        f"{sorted({f'{b}+{a}' for b, a in zip(D.book, D.arm)})}")

    # ladder: does pure de-grossing put a non-EWall book into the class?
    LD = lad[lad.floor_only]
    say(f"\n[LADDER CENSUS] static-gross rows in the class: {len(LD)} of {len(lad)}; by book "
        f"{dict(LD.book.value_counts())}; gross {LD.gross.min():.3f}..{LD.gross.max():.3f}")
    say(f"[LADDER CENSUS] non-EWall books the ladder walks into the class: "
        f"{sorted(set(LD[LD.book != 'EWall'].book))}")

    # ---- rule 8 walk-forward on the widened corpus ----
    say("\n[RULE 8] S0 (no screen) / S1 (IS 4b screen WITH the floor) / S2 (floor deleted), "
        "argmax IS Sharpe per (panel, cost) cell over the whole widened corpus; OOS read once.")
    wrows = []
    for (pk, c), s in df.groupby(["panel", "cost"]):
        bars, ms = ref[pk]["bars"], ref[pk]["spy"]
        v1r = ref[pk]["v1"][c]
        ctl = s[(s.book == "EWall") & (s.arm == "control")].iloc[0]
        scr = (s.IS_m_H1 > 0) & (s.IS_m_H2 > 0) & (s.IS_m_DD > 0)
        sel = {"S0": s, "S1": s[scr & (s.IS_m_CAGR > 0)], "S2": s[scr]}
        for k, cand in sel.items():
            if not len(cand):
                wrows.append(dict(sel=k, panel=pk, cost=c, pick="(none admitted)", n_admitted=0))
                continue
            p = cand.loc[cand.IS_Sharpe.idxmax()]
            wrows.append(dict(sel=k, panel=pk, cost=c, pick=f"{p.book}/{p.arm}", n_admitted=len(cand),
                              defensive=bool(p.floor_only), gross=p.gross,
                              OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                              beat_ctl=p.OOS_Sharpe > ctl.OOS_Sharpe, beat_spy=p.OOS_Sharpe > bars["soos"],
                              beat_v1=p.OOS_Sharpe > metrics(v1r.loc[OOS_START:])["Sharpe"],
                              spy_OOS_Sharpe=bars["soos"], ctl_OOS_Sharpe=ctl.OOS_Sharpe))
    wf = pd.DataFrame(wrows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    with pd.option_context("display.width", 260, "display.max_rows", None):
        say(wf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    piv = wf.pivot_table(index=["panel", "cost"], columns="sel", values="pick", aggfunc="first")
    ndiff = int((piv.get("S1") != piv.get("S2")).sum())
    say(f"[RULE 8] S1 != S2 in {ndiff} of {len(piv)} cells; S0 != S1 in "
        f"{int((piv.get('S0') != piv.get('S1')).sum())}. Mean OOS Sharpe: "
        + ", ".join(f"{k} {v:.3f}" for k, v in wf.groupby('sel').OOS_Sharpe.mean().items()))
    say(f"[RULE 8] picks that are themselves 4b-defensive: "
        + ", ".join(f"{k} {int(v.sum())}/{len(v)}" for k, v in wf.groupby('sel').defensive))

    # ---- census csv ----
    D.to_csv(OUT / f"{STEM}.census.csv", index=False)

    # ---- predictions ----
    say("\n[P] PRE-REGISTERED PREDICTIONS, scored")
    say(f"   P1 the class has a non-EWall member: {len(nonE)} -> {'HELD' if len(nonE) else 'FAILED'}")
    p2a = bool(len(D)) and float(D.gross.max()) < 0.70
    p2b = bool(len(set(LD[LD.book != 'EWall'].book)))
    say(f"   P2 every member has gross < 0.70 ({'yes' if p2a else f'no, max {D.gross.max():.3f}'}) "
        f"AND the ladder walks a non-EWall book into the class ({'yes' if p2b else 'no'}) -> "
        f"{'HELD' if (p2a and p2b) else 'FAILED'}")
    p3 = (len(PB) and PB.book.value_counts().idxmax() == "EWall"
          and PB.book.value_counts().max() > len(PB) / 2)
    say(f"   P3 EWall is the majority of Pareto-best members: "
        f"{dict(PB.book.value_counts()) if len(PB) else 'none'} -> {'HELD' if p3 else 'FAILED'}")
    rwshare = float((D.conv == "rw").mean()) if len(D) else np.nan
    say(f"   P4 < 25% of members are matched-gross (rw): {rwshare:.0%} -> "
        f"{'HELD' if rwshare < 0.25 else 'FAILED'}")
    say(f"   P5 S1 != S2 in >= 1 cell: {ndiff} -> {'HELD' if ndiff >= 1 else 'FAILED'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
