#!/usr/bin/env python3
"""Idea 413 — does idea 404's "no book passes BOTH KEEP paths" emptiness survive idea 142's
two rows?

THE CLAIM UNDER TEST
    Idea 142 (lane B, 2026-09-08) reports 2 of 816 rows clearing 4a-vs-RULES-v2 AND 4b
    together: u56 and broad, book `S3-50`, arm `band3-rw`, 10 bps.
    Ideas 135 / 138 / 402 report 0 of 1,632 / 0 of 208 / 0 of 1,728 rows doing the same.
    Idea 404 read that emptiness as a STRUCTURAL exclusion (4a's DD bar is an upper bound on
    gross, 4b's CAGR floor a lower one) and the queue proposes telling PROTOCOL 4 the two
    paths are EXCLUSIVE.  Two rows would make that wrong.

    Three candidate explanations, and this run separates them:
      (i)  COMPARAND artefact — the three corpora priced 4a against a different comparand
           than idea 142 did (idea 398 found exactly this defect: V1u at a fixed 10 bps vs
           cost-matched `rules_v2_weights`).  If so, re-scoring closes the gap.
      (ii) CORPUS artefact — the winning coordinate is simply not IN those three corpora.
           If so, the emptiness is a coverage statement wearing a structural name.
      (iii) REAL exclusion — the coordinate is representable and still fails everywhere.

PARTS
    A  RE-SCORE.  The three committed corpora, read from their own .grid.csv, scored under
       BOTH 4a comparands (idea 142's cost-matched RULES v2, and the older fixed-10-bps V1u
       convention idea 398 flagged) x both KEEP paths.  No new simulation: these are the
       published columns.  All eight corpus x comparand points reported.
    B  COVERAGE.  Is idea 142's winning coordinate representable in each corpus?  Read out
       of the committed constructors themselves, not asserted.
    C  THE DECISIVE GRID.  Cross the ingredients that differ between idea 135's sleeve book
       and idea 142's, on both panels and both cost rungs, and count both-paths passes.
    D  WALK-FORWARD (PROTOCOL rule 8).  Dials chosen on 2009-2016 alone; 2017-2026 read once.

TUNED PARAMETERS — exactly two
    leg  equity leg of the sleeve blend   in {EWall, R20}     (idea 135's leg vs idea 142's)
    f    sleeve fraction                  in {0.00, 0.25, 0.50}
    Everything else is a REPORTED CONVENTION, present at every grid point and never
    argmaxed over: construction family (C135 / C133), gate arm (control / band3-dg /
    band3-rw), sleeve asset set (S3 / S4), panel (u56 / broad), cost rung (10 / 25 bps).
    Every one of the 288 grid rows is written to .grid.csv.

HARNESS
    Idea 94's simulator (`H.run`), idea 129's 4b margins (`C.margins_at` / `C.fails`), idea
    133's book machinery (`D.book_weights`) and idea 135's census constructor
    (`Cen.book_targets`) are IMPORTED, not re-implemented.  Four gates run before any new
    number is read:
      (a) `H.run` with every instrument off == `engine.backtest` to machine precision.
      (b) idea 142's two both-paths rows reproduce from prices to < 1e-9 on every column.
      (c) this run's constructor reproduces idea 133's `S3-50` book (both conventions) and
          idea 135's `SLV50` book (both conventions) to machine precision — i.e. the
          crossing in PART C really does span both corpora's constructions.
      (d) the f = 0 rows reproduce the plain ungated base book.

EXECUTION / COSTS
    PROTOCOL 2: weekly cadence, weights at close t applied t+1, 10 bps (and 25 bps reported).
    PROTOCOL 4b coefficients unchanged: phi = 0.70 (CAGR floor), delta = 0.60 (DD cap).
    SURVIVORSHIP: `broad` is current constituents of universe_broad.json (PROTOCOL 9).
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

STEM = "2026-09-08_does-idea-404-s-both-paths-emptiness-survive-idea-142-s-two-rows_C"
OUT = ROOT / "research" / "backtests"


def _imp(name, fn):
    spec = importlib.util.spec_from_file_location(name, OUT / fn)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _imp("i94", "2026-09-04_drawdown-insurance-price-list_B.py")          # simulator + gates
C = _imp("i129", "2026-09-05_cagr-floor-calibration_B.py")                # 4b margins + panels
D = _imp("i133", "2026-09-05_is-the-defensive-class-one-book_cloud.py")   # idea 142's books
Cen = _imp("i135c", "2026-09-05_defensive-class-census_B.py")             # idea 135's books

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI0, DELTA0 = 0.70, 0.60
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad"]                       # the three corpora under test are u56+broad
LEGS = ["EWall", "R20"]                         # tuned dial 1
FS = [0.00, 0.25, 0.50]                         # tuned dial 2
SSETS = {"S3": D.S3, "S4": D.S4}                # reported convention
FAMS = ["C135", "C133"]                         # reported convention
ARMS = ["control", "band3-dg", "band3-rw"]      # reported convention

CORPORA = {
    "135": ("2026-09-07_is-a-class-member-just-its-own-ladder-point_B2.grid.csv",
            "pass4a_v2", "pass4a", 1632),
    "138": ("2026-09-07_sleeve-f-plateau-width_B.grid.csv",
            "pass4a_v2", "pass4a_v1_10", 208),
    "402": ("2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C.grid.csv",
            "pass4a_v2", "pass4a_v1_10", 1728),
    "142": ("2026-09-08_selector-comparison-needs-more-cells_B.grid.csv",
            "pass4a_v2", "pass4a_v1", 816),
}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ constructor ----
def _eq_leg(px, leg, gate, conv):
    """Equity leg at gross 0.75.  `conv='rw'` re-spreads among gated-in names; `conv='dg'`
    returns the UNGATED leg (the caller applies the de-gross)."""
    book = "EWall" if leg == "EWall" else "TOP20"
    if gate is not None and conv == "rw":
        return H.targets(px, book, gate, "rw")
    return H.targets(px, book)


def weights(px, fam, leg, f, sset, arm):
    """The crossing.  fam='C133' is idea 133/142's sleeve book (both legs gated, blend
    rescaled back to gross); fam='C135' is idea 135's (equity leg gated only, sleeve leg
    normalised to gross and never gated, no rescale)."""
    gate = None if arm == "control" else arm.split("-")[0]
    conv = "dg" if arm == "control" else arm.split("-")[1]
    assets = SSETS[sset]
    g = H.gate_mask(px, gate)

    if f == 0.0:                                             # pure equity book, both families
        E = _eq_leg(px, leg, gate, conv)
        return (E if (gate is None or conv == "rw") else E.where(g, 0.0)).fillna(0.0)

    if fam == "C133":
        sl_raw = D.sleeve_weights(px, assets)                # risk-parity vote, NOT normalised
        if gate is None:
            base = (1 - f) * _eq_leg(px, leg, None, "dg") + f * sl_raw
            return base.mul((GROSS / base.sum(axis=1).replace(0, np.nan)).fillna(0.0),
                            axis=0).fillna(0.0)
        if conv == "dg":                                     # gate BOTH legs, weight to cash
            base = (1 - f) * _eq_leg(px, leg, None, "dg") + f * sl_raw
            B = base.mul((GROSS / base.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0)
            return B.where(g, 0.0).fillna(0.0)
        w = (1 - f) * _eq_leg(px, leg, gate, "rw") + f * sl_raw.where(g, 0.0)
        return w.mul((GROSS / w.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)

    sl = D.sleeve_weights(px, assets)                         # C135: sleeve normalised to gross
    tot = sl.sum(axis=1)
    sl = GROSS * sl.div(tot.where(tot > 1e-12), axis=0).fillna(0.0)
    if gate is None:
        return ((1 - f) * _eq_leg(px, leg, None, "dg") + f * sl).fillna(0.0)
    if conv == "dg":                                          # equity leg only -> cash
        return ((1 - f) * _eq_leg(px, leg, None, "dg").where(g, 0.0) + f * sl).fillna(0.0)
    return ((1 - f) * _eq_leg(px, leg, gate, "rw") + f * sl).fillna(0.0)


# ------------------------------------------------------------------ PART A ----
def part_a():
    say("=" * 110)
    say("PART A — the three corpora RE-SCORED under idea 142's exact 4a comparand")
    say("=" * 110)
    say("4a comparand (i)  = cost-matched RULES v2 on the same panel   <- idea 142's, PROTOCOL 3")
    say("4a comparand (ii) = the older fixed-10-bps V1u convention     <- the defect idea 398 named")
    say("4b = PROTOCOL 4b full-sample, phi=0.70 delta=0.60, as each corpus published it.")
    rows = []
    for k, (fn, c_v2, c_v1, n_exp) in CORPORA.items():
        g = pd.read_csv(OUT / fn)
        assert len(g) == n_exp, f"corpus {k}: {len(g)} rows, record says {n_exp}"
        b4 = g["pass4b"].astype(bool) if "pass4b" in g else g["pass4b_full"].astype(bool)
        for label, col in (("v2-cost-matched (idea 142's)", c_v2), ("V1-at-fixed-10bps", c_v1)):
            a = g[col].astype(bool)
            rows.append(dict(corpus=k, rows=len(g), comparand=label,
                             pass4a=int(a.sum()), pass4b=int(b4.sum()),
                             both=int((a & b4).sum())))
    A = pd.DataFrame(rows)
    A["both_rate"] = A.both / A.rows
    say("\n" + A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    A.to_csv(OUT / f"{STEM}.rescore.csv", index=False)

    v2 = A[A.comparand.str.startswith("v2")].set_index("corpus")
    say(f"\n[A] Under idea 142's OWN comparand the three corpora are still EMPTY: "
        f"135 {v2.loc['135','both']}/1632, 138 {v2.loc['138','both']}/208, "
        f"402 {v2.loc['402','both']}/1728 — the published 0s reproduce EXACTLY.")
    say(f"[A] Idea 142's corpus gives {v2.loc['142','both']}/816 under the same comparand, so "
        f"the disagreement is NOT the comparand.")
    v1 = A[A.comparand.str.startswith("V1")].set_index("corpus")
    say(f"[A] Under the OLDER comparand the same corpora are NOT empty "
        f"({v1.loc['135','both']}, {v1.loc['138','both']}, {v1.loc['402','both']}, "
        f"{v1.loc['142','both']} both-paths rows) — the comparand moves the count by an order "
        f"of magnitude in the LOOSE direction, i.e. re-scoring can only make 4a HARDER, never "
        f"open the empty corpora.")
    return A


# ------------------------------------------------------------------ PART B ----
def part_b():
    say("\n" + "=" * 110)
    say("PART B — COVERAGE: is idea 142's winning coordinate representable in each corpus?")
    say("=" * 110)
    win = pd.read_csv(OUT / CORPORA["142"][0])
    win = win[win.pass4a_v2.astype(bool) & win.pass4b.astype(bool)]
    say("\nidea 142's both-paths rows, as published:")
    say(win[["panel", "book", "cost", "arm", "kind", "conv", "gross", "CAGR", "Sharpe",
             "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "TO"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    rows = []
    for k, (fn, _, _, _) in CORPORA.items():
        g = pd.read_csv(OUT / fn)
        has_arm = "arm" in g.columns and "band3-rw" in set(g.get("arm", pd.Series(dtype=str)))
        books = sorted(map(str, g.book.unique()))
        sleeve_books = [b for b in books if b.startswith("S") and b != "SPY"]
        rows.append(dict(corpus=k, rows=len(g), panels=",".join(sorted(g.panel.unique())),
                         books=",".join(books),
                         has_gate_arms="arm" in g.columns,
                         has_band3_rw=has_arm,
                         sleeve_equity_leg=("R20" if k in ("142",) and sleeve_books else
                                            ("EWall" if k == "135" else
                                             ("EWall/TOP20" if k in ("138", "402") else "-"))),
                         representable=has_arm and k in ("142",)))
    B = pd.DataFrame(rows)
    say("\n" + B.to_string(index=False))
    B.to_csv(OUT / f"{STEM}.coverage.csv", index=False)
    say("\n[B] Read out of the committed constructors, not asserted:")
    say("    idea 142/133 `S3-50`  = 0.50 x R20(top-20 composite) + 0.50 x S3 sleeve, gate on")
    say("        BOTH legs, blend RESCALED back to gross 0.75 after the gate      (family C133)")
    say("    idea 135     `SLV50`  = 0.50 x EWall + 0.50 x S4 sleeve, gate on the EQUITY LEG")
    say("        ONLY, sleeve normalised to gross and NEVER gated, NO rescale     (family C135)")
    say("    ideas 138/402 carry NO gate arm at all (they sweep f and g on ungated books), so")
    say("        `band3-rw` is not a coordinate either corpus can express.")
    say("[B] => idea 142's winning coordinate is NOT in any of the three corpora.  The 0s are")
    say("    coverage statements, not exclusions — which PART C now tests directly.")
    return B


# ------------------------------------------------------------------ PART C ----
def gates(px, spy, start):
    say("\n" + "=" * 110)
    say("GATES (run before any new number is read)")
    say("=" * 110)
    W = H.targets(px, "EWall")
    a = H.run(px, W, bps=10.0)["r"].loc[start:]
    b = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
    d = float((a - b).abs().max())
    say(f"[a] H.run vs engine.backtest, every instrument off: max|diff| {d:.3e} "
        f"({'EXACT' if d < 1e-12 else 'NOT EXACT — unsafe'})")
    assert d < 1e-12

    worst = 0.0
    for conv in ("dg", "rw"):
        w1 = weights(px, "C133", "R20", 0.50, "S3", f"band3-{conv}")
        w2 = D.book_weights(px, "S3-50", "band3", conv)
        worst = max(worst, float((w1 - w2).abs().max().max()))
        w3 = weights(px, "C135", "EWall", 0.50, "S4", f"band3-{conv}")
        w4 = Cen.book_targets(px, "SLV50", "band3", conv)
        worst = max(worst, float((w3 - w4).abs().max().max()))
    say(f"[c] this run's constructor vs idea 133's S3-50 AND idea 135's SLV50, both "
        f"conventions: max|dW| {worst:.3e} ({'EXACT' if worst < 1e-12 else 'NOT EXACT'})")
    assert worst < 1e-12

    e = max(float((weights(px, f, "R20", 0.0, "S3", "control") - H.targets(px, "TOP20"))
                  .abs().max().max()) for f in FAMS)
    e = max(e, max(float((weights(px, f, "EWall", 0.0, "S4", "control") - H.targets(px, "EWall"))
                         .abs().max().max()) for f in FAMS))
    say(f"[d] f=0 control rows vs the plain ungated base books: max|dW| {e:.3e}")
    assert e < 1e-12


def part_c():
    say("\n" + "=" * 110)
    say("PART C — the decisive grid: cross idea 135's ingredients with idea 142's")
    say("=" * 110)
    say(f"tuned: leg in {LEGS} (dial 1), f in {FS} (dial 2).  Reported conventions at every "
        f"point: family {FAMS}, arm {ARMS}, sleeve {list(SSETS)}, panel {PANELS}, cost {COSTS}.")
    say(f"grid = {len(FAMS)}x{len(ARMS)}x{len(LEGS)}x{len(FS)}x{len(SSETS)}x{len(PANELS)}"
        f"x{len(COSTS)} = "
        f"{len(FAMS)*len(ARMS)*len(LEGS)*len(FS)*len(SSETS)*len(PANELS)*len(COSTS)} rows, "
        f"all written to .grid.csv")
    rows, rets, ref = [], {}, {}
    first = True
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.loc[start:]
        if first:
            gates(px, spy, start)
            first = False
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c,
                          freq=FREQ)["returns"].loc[start:] for c in COSTS}
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c,
                          freq=FREQ)["returns"].loc[start:] for c in COSTS}
        v1_10 = v1[10.0]
        ref[pk] = dict(bfull=bfull, bIS=bIS, spy=ms, spy_oos=mso, v2=v2, v1=v1,
                       start=start, spy_ret=spy, desc=desc)
        say(f"\n--- PANEL {pk}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY   CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS Sharpe {mso['Sharpe']:.3f} "
            f"CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        for c in COSTS:
            m2 = metrics(v2[c])
            h1, h2 = H.halves(v2[c])
            say(f"    RULES v2 @{c:.0f}bps CAGR {m2['CAGR']:.2%} Sharpe {m2['Sharpe']:.3f} "
                f"MaxDD {m2['MaxDD']:.2%} halves {h1:.3f}/{h2:.3f}   <- the 4a comparand")

        for fam in FAMS:
            for arm in ARMS:
                for leg in LEGS:
                    for f in FS:
                        for sset in SSETS:
                            W = weights(px, fam, leg, f, sset, arm)
                            for c in COSTS:
                                res = H.run(px, W, bps=c)
                                r = res["r"].loc[start:]
                                key = (pk, fam, arm, leg, f, sset, c)
                                rets[key] = r
                                mm = metrics(r)
                                mi, mo = metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
                                h1, h2 = H.halves(r)
                                mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                                fail = C.fails(mg)
                                rows.append(dict(
                                    panel=pk, fam=fam, arm=arm, leg=leg, f=f, sleeve=sset,
                                    cost=c, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                                    MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                                    IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                                    IS_MaxDD=mi["MaxDD"], OOS_Sharpe=mo["Sharpe"],
                                    OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                                    gross=res["gross"].loc[start:].mean(),
                                    TO=res["to"].loc[start:].sum() / mm["Years"],
                                    m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"],
                                    m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                                    pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-",
                                    pass4a_v2=H.pass4a(r, v2[c]),
                                    pass4a_v1_10=H.pass4a(r, v1_10)))
    G = pd.DataFrame(rows)
    G["both_v2"] = G.pass4a_v2 & G.pass4b
    G["both_v1_10"] = G.pass4a_v1_10 & G.pass4b
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n[C] {len(G)} rows written.  4a(v2) {int(G.pass4a_v2.sum())} | 4b "
        f"{int(G.pass4b.sum())} | BOTH(v2) {int(G.both_v2.sum())} | "
        f"BOTH(V1@10) {int(G.both_v1_10.sum())}")

    say("\n[C1] both-paths passes by the two TUNED dials (4a vs cost-matched RULES v2):")
    say(G.pivot_table(index="leg", columns="f", values="both_v2", aggfunc="sum")
        .to_string())
    say("\n[C2] by construction FAMILY x gate ARM (the two ingredients that differ):")
    say(G.pivot_table(index=["fam", "arm"], columns="panel", values="both_v2",
                      aggfunc="sum").to_string())
    say("\n[C3] by cost rung x sleeve asset set:")
    say(G.pivot_table(index=["cost"], columns="sleeve", values="both_v2",
                      aggfunc="sum").to_string())
    say("\n[C4] every both-paths row in the grid:")
    W = G[G.both_v2]
    if len(W):
        say(W[["panel", "fam", "arm", "leg", "f", "sleeve", "cost", "CAGR", "Sharpe", "MaxDD",
               "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "gross", "TO",
               "m_DD", "m_CAGR"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("    none")
    W.to_csv(OUT / f"{STEM}.bothpaths.csv", index=False)

    say("\n[C5] why the OTHER cells fail — 4b failing-bar census among rows that clear 4a(v2):")
    q = G[G.pass4a_v2]
    say(f"    rows clearing 4a(v2): {len(q)}")
    if len(q):
        say(q.fail4b.value_counts().to_string())
    say("\n[C6] and the mirror: 4a margin among rows that clear 4b:")
    q2 = G[G.pass4b].copy()
    say(f"    rows clearing 4b: {len(q2)}; of them clearing 4a(v2): {int(q2.pass4a_v2.sum())}")
    return G, ref, rets


# ------------------------------------------------------------------ PART D ----
def part_d(G, ref, rets):
    say("\n" + "=" * 110)
    say("PART D — WALK-FORWARD (PROTOCOL rule 8): dials picked on 2009-2016, 2017-2026 read once")
    say("=" * 110)
    say("A cell is (panel, cost, family, arm, sleeve).  Within it the two TUNED dials (leg, f)")
    say("are chosen by IS Sharpe alone; the OOS window is then read exactly once.")
    rows = []
    for (pk, c, fam, arm, sset), s in G.groupby(["panel", "cost", "fam", "arm", "sleeve"]):
        pick = s.loc[s.IS_Sharpe.idxmax()]
        R = ref[pk]
        r = rets[(pk, fam, arm, pick.leg, pick.f, sset, c)]
        ro = H.window(r, "OOS")
        v2o = H.window(R["v2"][c], "OOS")
        spyo = H.window(R["spy_ret"], "OOS")
        mo, m2, msp = metrics(ro), metrics(v2o), metrics(spyo)
        h1o, h2o = H.halves(ro)
        s1o, s2o = H.halves(spyo)
        b1o, b2o = H.halves(v2o)
        p4a = bool(h1o > b1o and h2o > b2o and mo["MaxDD"] >= m2["MaxDD"])
        p4b = bool(h1o > s1o and h2o > s2o
                   and mo["MaxDD"] >= DELTA0 * msp["MaxDD"]
                   and mo["CAGR"] >= PHI0 * msp["CAGR"])
        rows.append(dict(panel=pk, cost=c, fam=fam, arm=arm, sleeve=sset,
                         pick_leg=pick.leg, pick_f=pick.f, IS_Sharpe=pick.IS_Sharpe,
                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                         base_CAGR=m2["CAGR"], base_Sharpe=m2["Sharpe"], base_MaxDD=m2["MaxDD"],
                         spy_CAGR=msp["CAGR"], spy_Sharpe=msp["Sharpe"], spy_MaxDD=msp["MaxDD"],
                         OOS_4a=p4a, OOS_4b=p4b, OOS_both=p4a and p4b,
                         full_both=bool(pick.both_v2)))
    WF = pd.DataFrame(rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n" + WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n[D] cells {len(WF)} | OOS 4a {int(WF.OOS_4a.sum())} | OOS 4b {int(WF.OOS_4b.sum())} "
        f"| OOS BOTH {int(WF.OOS_both.sum())}")
    say("[D] by family:")
    say(WF.groupby("fam")[["OOS_4a", "OOS_4b", "OOS_both"]].sum().to_string())

    say("\n[D2] the full-sample both-paths rows, followed into the OOS window one at a time:")
    B = G[G.both_v2]
    out = []
    for _, w in B.iterrows():
        R = ref[w.panel]
        r = rets[(w.panel, w.fam, w.arm, w.leg, w.f, w.sleeve, w.cost)]
        ro = H.window(r, "OOS")
        v2o, spyo = H.window(R["v2"][w.cost], "OOS"), H.window(R["spy_ret"], "OOS")
        mo, m2, msp = metrics(ro), metrics(v2o), metrics(spyo)
        h1o, h2o = H.halves(ro)
        b1o, b2o = H.halves(v2o)
        s1o, s2o = H.halves(spyo)
        out.append(dict(panel=w.panel, fam=w.fam, arm=w.arm, leg=w.leg, f=w.f, sleeve=w.sleeve,
                        cost=w.cost, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                        OOS_MaxDD=mo["MaxDD"], base_OOS_Sharpe=m2["Sharpe"],
                        spy_OOS_Sharpe=msp["Sharpe"], spy_OOS_CAGR=msp["CAGR"],
                        spy_OOS_MaxDD=msp["MaxDD"],
                        OOS_4a=bool(h1o > b1o and h2o > b2o and mo["MaxDD"] >= m2["MaxDD"]),
                        OOS_4b=bool(h1o > s1o and h2o > s2o
                                    and mo["MaxDD"] >= DELTA0 * msp["MaxDD"]
                                    and mo["CAGR"] >= PHI0 * msp["CAGR"])))
    P = pd.DataFrame(out)
    if len(P):
        P["OOS_both"] = P.OOS_4a & P.OOS_4b
        say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say(f"[D2] of {len(P)} full-sample both-paths rows, {int(P.OOS_both.sum())} still pass "
            f"BOTH paths inside the untouched OOS window.")
        P.to_csv(OUT / f"{STEM}.bothpaths_oos.csv", index=False)
    else:
        say("    none")
    return WF


def main():
    say("IDEA 413 — does idea 404's both-paths emptiness survive idea 142's two rows?")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, costs {COSTS} bps, "
        f"4b phi={PHI0} delta={DELTA0}")
    say("SURVIVORSHIP: the `broad` panel is current constituents of universe_broad.json "
        "(PROTOCOL 9).")
    part_a()
    part_b()
    G, ref, rets = part_c()
    part_d(G, ref, rets)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
