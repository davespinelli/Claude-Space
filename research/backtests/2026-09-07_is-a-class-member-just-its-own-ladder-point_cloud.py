#!/usr/bin/env python3
"""Idea 135 — "is-a-class-member-just-its-own-ladder-point" (cloud, 2026-09-07).

QUESTION (QUEUE.md).  Idea 133 measured that forcing 0.53 mean gross moves TOP20 from 1
`4b-defensive` class member to 34 and TOP40 from 10 to 52 — de-grossing MANUFACTURES
membership — while V1u/TOP5 join at no gross level and the sleeve books at every one.  A
mean-gross column may not be enough to separate them.  Test the explicit control: price
every class member against **its OWN book's static-gross ladder point at matched mean
gross**, and propose that a `4b-defensive` row must beat that point to be recorded at all.

THE CLASS (idea 129's, verbatim, via idea 133's own code).  A `4b-defensive` arm clears
4b's halves bars, its OOS-Sharpe bar and its drawdown cap, and fails **only** the CAGR
floor: `fails(margins) == ["CAGR"]`.

WHY THIS IS NOT ARITHMETIC.  A static gross multiplier m scales an arm's exposure without
re-timing it.  Under the closed-form convention (r = m*r0, turn = m*turn0) Sharpe is
EXACTLY invariant in m, so a ladder point can only buy drawdown by giving up CAGR
one-for-one along a fixed Sharpe.  A de-grossing OVERLAY moves Sharpe too.  So the
question has content: does a class member's overlay buy anything a dumb static cut at the
same average exposure does not?  If not, the class is the gross dial wearing 17 names, and
the record's `4b-defensive` rows are ladder points with extra steps.

NOTE the record's ladder point is NOT the closed form: `H.run(px, W, m=...)` re-runs the
engine, whose cash leg drifts, so its Sharpe is only NEARLY invariant.  Both comparands
are therefore priced and reported side by side, and the deviation is MEASURED in [0] (G4),
not assumed:
    LADDER  the record's own convention — the book's `control` arm re-run at the static
            multiplier m that matches the member's realised mean gross (idea 133's
            `run_at_gross`, two Newton steps, achieved gross reported for every row).
    SCALAR  the closed-form control r = a*r0, turn = a*turn0 at a = matched mean gross.

DESIGN.  Corpus = idea 133's, restricted to **native gross** (each arm at its own
exposure), because that is idea 129's reading and the one the class was defined on;
idea 133's m53/m75 rescalings are a different question and including them would confound
the comparand with the treatment.  3 panels x 8 books x 17 arms x 2 cost rungs.

  panels  u56 (universe.json, 56), broad (universe_broad.json, 136), small (the sub-$2B
          panel MINUS the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv,
          439 traded, SPY held out as the benchmark only)
  books   V1u, TOP5, TOP10, TOP20, TOP40, EWall, SLV25, SLV50
  arms    H.arm_specs() — control + 5 gates x 2 conventions + 2 stops + 2 DD controls +
          2 entry budgets
  costs   10 and 25 bps

TUNED PARAMETERS (max 2, PROTOCOL rule 4): (1) ranked book size n in {5,10,20,40},
(2) sleeve fraction f in {0.25,0.50} — idea 133's own two.  Panel, arm, cost rung and
window are CENSUS axes: every level is reported and nothing is selected on outcome.

RULE 8 WALK-FORWARD.  Selectors fixed in writing before any OOS number was read; chosen on
2009-2016 alone, 2017-2026 read once, pooled over all books inside a (panel, cost) cell:
    S0  no screen: argmax IS Sharpe over every arm in the cell.
    S3  idea 133's class selector: argmax IS Sharpe among IS-window class members.
    S5  NEW, the idea's proposal: S3 restricted to members that BEAT their own IS-window
        ladder point.  If the proposal is empty of content S5 == S3 in every cell.

GATES (printed in [0] before any new number).
  G1  this run's native-gross corpus reproduces idea 133's committed `.grid.csv` on every
      shared key and every numeric column.
  G2  the ladder point at m = 1 IS the book's control arm, exactly.
  G3  the matched-gross solve: |achieved mean gross - the member's own| over every member.
  G4  Sharpe invariance of the static gross dial, MEASURED under both conventions.
  G5  the record's standing 2026-09-04 KEEP-4b row (`46 N n=20`; published 12.7% / 1.09 /
      -18.3%, halves 1.09/1.10) rebuilt at fixed n=20 on u56 @10 bps.

CAVEATS carried, not buried.  (1) SURVIVORSHIP: all three panels are CURRENT-CONSTITUENT
lists (universe.json, universe_broad.json, and the sub-$2B screen — see
data/SMALL_PANEL_README.md); absent delistings inflate every arm's CAGR and inflate the
UNGATED, fully-invested books most, so the class's exclusion by a CAGR floor is if
anything understated — and so is a ladder point's CAGR, which is what the class member is
being asked to beat.  broad CONTAINS u56, so they are not two independent samples.
(2) The IS window's SPY MaxDD (-22.1%) is shallower than the OOS window's (-33.7%), so any
IS drawdown cap is measured on a window that cannot express deep drawdowns; this biases
every IS screen toward over-admission, S5 included.  (3) MaxDD is one number off one path;
"beats on drawdown" inherits that fragility.  (4) A matched-gross ladder point is NOT the
same instrument as the member and is never quoted as one.

Deterministic, standalone (imports idea 133's committed census module, which is how that
idea itself reuses ideas 94 and 102).  Modifies nothing.
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
from baseline import load_universe, score                      # noqa: E402
from engine import backtest, metrics                           # noqa: E402

OUT = Path(__file__).with_suffix("")
SLUG = OUT.name
BT = ROOT / "research" / "backtests"


def _imp(name, fn):
    spec = importlib.util.spec_from_file_location(name, BT / fn)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _imp("i133", "2026-09-05_defensive-class-census_B.py")      # class definition + books
H = C.H                                                          # idea 94's simulator + arms

PANELS = ["u56", "broad", "small"]
BOOKS = C.BOOKS
COSTS = C.COSTS
PHI0, DELTA0 = C.PHI0, C.DELTA0
IS_END, OOS_START = H.IS_END, H.OOS_START

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 1200)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def sharpe(r):
    sd = float(np.std(np.asarray(r, float), ddof=1)) * np.sqrt(252.0)
    return (float(np.mean(r)) * 252.0) / sd if sd else np.nan


def solve_ladder(px, Wc, cost, target, start, kw=None):
    """The book's OWN static-gross ladder point at `target` mean gross: the control arm
    re-run at the multiplier m that matches it.  Idea 133's `run_at_gross`, two Newton
    steps; the achieved gross is returned so the match can be audited row by row."""
    kw = kw or {}
    res = H.run(px, Wc, bps=cost, **kw)
    g = float(res["gross"].loc[start:].mean())
    m = 1.0
    for _ in range(3):
        if g <= 1e-9:
            break
        m = float(np.clip(m * target / g, 0.01, 5.0))
        res = H.run(px, Wc, m=m, bps=cost, **kw)
        g = float(res["gross"].loc[start:].mean())
    return res, m, g


def stats_of(r, bfull, bIS):
    mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
    mgi = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
    f = C.fails(mg)
    h1, h2 = H.halves(r)
    return dict(CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                pass4b=(len(f) == 0), fail4b=",".join(f) or "-", n_fail=len(f),
                floor_only=(f == ["CAGR"]),
                IS_floor_only=(C.fails(mgi) == ["CAGR"]))


def main():
    t0 = time.time()
    P(f"# {SLUG}")
    P("# idea 135 — is a `4b-defensive` class member just its OWN book's static-gross")
    P("#            ladder point at matched mean gross?")
    P(f"# corpus: NATIVE gross only | {PANELS} x {len(BOOKS)} books x 17 arms x {COSTS} bps")
    P("# CLASS := fails(4b margins) == ['CAGR'] exactly (idea 129's definition, via idea 133)")
    P("")

    # =============================================================== [0] GATES (part 1)
    P("=" * 150)
    P("[0] GATES")
    gpx = C.panel("u56")[0]
    el = (score(gpx)[1]) & (score(gpx)[2] < 0.60)
    rk = score(gpx, vol_scale=False)[0].where(el).rank(axis=1, ascending=False)
    kf = pd.Series(20.0, index=gpx.index)
    w20 = rk.le(kf, axis=0).astype(float).mul(0.75 / kf, axis=0)
    e20 = backtest(gpx, w20, cost_bps=10, freq="W")["returns"].loc[gpx.index[260]:]
    m20 = metrics(e20)
    h = len(e20) // 2
    P(f"    G5 standing 2026-09-04 KEEP-4b row (`46 N n=20`; published 12.7% / 1.09 / "
      f"-18.3%, halves 1.09/1.10) at fixed n=20: {m20['CAGR']:.2%} / {m20['Sharpe']:.3f} / "
      f"{m20['MaxDD']:.2%} (halves {sharpe(e20.values[:h]):.2f}/{sharpe(e20.values[h:]):.2f})")

    # =============================================================== corpus + the test
    rows, ladders = [], []
    g2 = g3 = 0.0
    g4L = g4S = 0.0
    for pname in PANELS:
        px, spy, plabel = C.panel(pname)
        start = px.index[260]
        v1_net = H.run(px, C.book_targets(px, "V1u"), bps=10.0)["r"].loc[start:]
        bfull = C.bars_win(spy.loc[start:], "full")
        bIS = C.bars_win(spy.loc[start:], "IS")
        sm, si, so = metrics(spy.loc[start:]), metrics(H.window(spy.loc[start:], "IS")), \
            metrics(H.window(spy.loc[start:], "OOS"))
        P("=" * 150)
        P(f"PANEL {pname} ({plabel}) | eval {start.date()} .. {px.index[-1].date()}")
        P(f"    SPY full {sm['CAGR']:.2%} / {sm['Sharpe']:.3f} / {sm['MaxDD']:.2%} | "
          f"IS {si['CAGR']:.2%} / {si['Sharpe']:.3f} | OOS {so['CAGR']:.2%} / "
          f"{so['Sharpe']:.3f} / {so['MaxDD']:.2%} | 4b bars: DD cap "
          f"{DELTA0*abs(bfull['sdd']):.2%}, CAGR floor {PHI0*bfull['scagr']:.2%}")

        for book in BOOKS:
            # the sleeve books need TLT/GLD/DBC/UUP, which the sub-$2B panel does not
            # carry; idea 133 skips them there too (its native grid is 748 rows, not 816,
            # and the 68 missing rows are exactly these 2 books x 17 arms x 2 costs).
            if pname == "small" and book in C.SLEEVE_BOOKS:
                continue
            Wc = C.book_targets(px, book)                       # the book's CONTROL arm
            for cost in COSTS:
                base = H.run(px, Wc, bps=cost)
                base_r = base["r"].loc[start:]
                base_g = float(base["gross"].loc[start:].mean())
                # G2 — the ladder point at m = 1 IS the control arm
                one = H.run(px, Wc, m=1.0, bps=cost)["r"].loc[start:]
                g2 = max(g2, float((one - base_r).abs().max()))

                for arm, kind, kw, (gate, conv) in H.arm_specs():
                    W = C.book_targets(px, book, gate, conv)
                    res = H.run(px, W, bps=cost, **kw)
                    r = res["r"].loc[start:]
                    gross = float(res["gross"].loc[start:].mean())
                    st = stats_of(r, bfull, bIS)
                    row = dict(panel=pname, book=book, cost=cost, arm=arm, kind=kind,
                               gross=gross, pass4a=H.pass4a(r, v1_net),
                               TO=float(res["to"].loc[start:].sum() / (len(r) / 252)), **st)
                    rows.append(row)

                    if not (st["floor_only"] or st["IS_floor_only"]):
                        continue
                    # ---- the test: this arm against its OWN book's ladder point
                    lres, m, gach = solve_ladder(px, Wc, cost, gross, start)
                    lr = lres["r"].loc[start:]
                    g3 = max(g3, abs(gach - gross))
                    lst = stats_of(lr, bfull, bIS)
                    # ---- and against the closed-form SCALAR control at the same a
                    a = gross / base_g if base_g > 0 else np.nan
                    sr = pd.Series(a * base_r.values, index=base_r.index)
                    sst = stats_of(sr, bfull, bIS)
                    g4L = max(g4L, abs(lst["Sharpe"] - metrics(base_r)["Sharpe"]))
                    g4S = max(g4S, abs(sst["Sharpe"] - metrics(base_r)["Sharpe"]))
                    ladders.append(dict(
                        panel=pname, book=book, cost=cost, arm=arm, kind=kind,
                        member_gross=gross, ladder_m=m, ladder_gross=gach,
                        gross_match_err=abs(gach - gross), scalar_a=a,
                        mem_CAGR=st["CAGR"], mem_Sharpe=st["Sharpe"], mem_MaxDD=st["MaxDD"],
                        mem_OOS_Sharpe=st["OOS_Sharpe"], mem_OOS_CAGR=st["OOS_CAGR"],
                        mem_OOS_MaxDD=st["OOS_MaxDD"], mem_IS_Sharpe=st["IS_Sharpe"],
                        mem_floor_only=st["floor_only"], mem_IS_floor_only=st["IS_floor_only"],
                        lad_CAGR=lst["CAGR"], lad_Sharpe=lst["Sharpe"], lad_MaxDD=lst["MaxDD"],
                        lad_OOS_Sharpe=lst["OOS_Sharpe"], lad_OOS_CAGR=lst["OOS_CAGR"],
                        lad_OOS_MaxDD=lst["OOS_MaxDD"], lad_IS_Sharpe=lst["IS_Sharpe"],
                        lad_floor_only=lst["floor_only"], lad_pass4b=lst["pass4b"],
                        lad_fail4b=lst["fail4b"],
                        sca_CAGR=sst["CAGR"], sca_Sharpe=sst["Sharpe"], sca_MaxDD=sst["MaxDD"],
                        sca_OOS_Sharpe=sst["OOS_Sharpe"], sca_floor_only=sst["floor_only"],
                        parent_Sharpe=metrics(base_r)["Sharpe"],
                        parent_CAGR=metrics(base_r)["CAGR"],
                        parent_MaxDD=metrics(base_r)["MaxDD"], parent_gross=base_g))
        P(f"    ...{pname} done at {time.time()-t0:.0f}s")

    G = pd.DataFrame(rows)
    L = pd.DataFrame(ladders)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    L.to_csv(f"{OUT}.ladders.csv", index=False)

    # =============================================================== [0] GATES (part 2)
    P("")
    P("=" * 150)
    ref = pd.read_csv(BT / "2026-09-05_defensive-class-census_B.grid.csv")
    ref = ref[ref.gross_mode == "native"]
    key = ["panel", "book", "cost", "arm"]
    M = ref.merge(G, on=key, suffixes=("_r", "_n"), validate="one_to_one")
    num = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "IS_MaxDD",
           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO"]
    g1 = max(float((M[f"{c}_r"] - M[f"{c}_n"]).abs().max()) for c in num)
    bmis = int((M["floor_only_r"] != M["floor_only_n"]).sum())
    pmis = int((M["pass4b_r"] != M["pass4b_n"]).sum())
    P(f"    G1 native-gross corpus reproduces idea 133's committed .grid.csv on "
      f"{len(M)}/{len(ref)} shared rows and {len(num)} numeric columns: max |d| {g1:.3e}  "
      f"| floor_only mismatches {bmis}  | pass4b mismatches {pmis}")
    assert g1 < 1e-9 and bmis == 0 and pmis == 0, (g1, bmis, pmis)
    P(f"    G2 the ladder point at m = 1 IS the book's control arm: max |d| {g2:.3e}")
    assert g2 < 1e-12, g2
    P(f"    G3 matched-gross solve over {len(L)} members: max |achieved - member| "
      f"{g3:.3e}")
    P(f"    G4 Sharpe invariance of the static gross dial, MEASURED: LADDER (the record's "
      f"re-run convention) max |dSharpe vs the un-scaled control| {g4L:.3e};  SCALAR "
      f"(closed form) {g4S:.3e}")
    P(f"       -> the record's ladder point is only NEARLY Sharpe-invariant; the closed "
      f"form is exactly invariant.  Both are reported below and neither is assumed.")

    # =============================================================== [A] the census
    P("")
    P("=" * 150)
    P("[A] THE CLASS AT NATIVE GROSS")
    cls = G[G.floor_only]
    P(f"    {len(G)} arm-rows | 4a {int(G.pass4a.sum())}/{len(G)} | 4b "
      f"{int(G.pass4b.sum())}/{len(G)} | CLASS (`4b-defensive`) {len(cls)}/{len(G)}")
    P("    class members by panel x book:")
    P(pd.crosstab(cls.panel, cls.book).to_string())

    # =============================================================== [B] the test
    P("")
    P("=" * 150)
    P("[B] THE TEST — every class member against its OWN book's ladder point at matched "
      "mean gross")
    F = L[L.mem_floor_only].copy()
    for tag, sfx in [("LADDER (the record's convention)", "lad"),
                     ("SCALAR (closed form, exactly Sharpe-invariant)", "sca")]:
        F[f"d_Sharpe_{sfx}"] = F["mem_Sharpe"] - F[f"{sfx}_Sharpe"]
        # MaxDD is NEGATIVE, so "the member is shallower" is |ladder| - |member| > 0.
        F[f"d_MaxDD_{sfx}"] = F[f"{sfx}_MaxDD"].abs() - F["mem_MaxDD"].abs()
        F[f"d_CAGR_{sfx}"] = F["mem_CAGR"] - F[f"{sfx}_CAGR"]
        F[f"beats_{sfx}"] = (F[f"d_Sharpe_{sfx}"] > 0) & (F[f"d_MaxDD_{sfx}"] >= 0)
        F[f"beatsS_{sfx}"] = F[f"d_Sharpe_{sfx}"] > 0
    F["d_OOS_Sharpe_lad"] = F["mem_OOS_Sharpe"] - F["lad_OOS_Sharpe"]
    F.to_csv(f"{OUT}.test.csv", index=False)

    P(f"    {len(F)} class members priced against their own ladder point.")
    P("")
    P("    | comparand | beats on Sharpe AND drawdown | beats on Sharpe alone | "
      "mean dSharpe | mean dMaxDD (pp, + = member shallower) | mean dCAGR (pp) |")
    for tag, sfx in [("LADDER", "lad"), ("SCALAR", "sca")]:
        nb, nbs = int(F["beats_" + sfx].sum()), int(F["beatsS_" + sfx].sum())
        ds, dd, dc = (F["d_Sharpe_" + sfx].mean(), 100 * F["d_MaxDD_" + sfx].mean(),
                      100 * F["d_CAGR_" + sfx].mean())
        P(f"    | {tag:6s} | {nb:3d}/{len(F)} ({nb/len(F):.1%}) | {nbs:3d}/{len(F)} "
          f"({nbs/len(F):.1%}) | {ds:+.4f} | {dd:+.2f} | {dc:+.2f} |")
    P("")
    P("    Is the ladder point ITSELF a class member (the queue's 'manufactured "
      f"membership' reading)?  LADDER {int(F.lad_floor_only.sum())}/{len(F)} "
      f"({F.lad_floor_only.mean():.1%}) | SCALAR {int(F.sca_floor_only.sum())}/{len(F)} "
      f"({F.sca_floor_only.mean():.1%}) | the ladder point PASSES full 4b in "
      f"{int(F.lad_pass4b.sum())}/{len(F)}")
    P("")
    P("    by book (LADDER comparand):")
    bb = F.groupby("book").agg(n=("beats_lad", "size"), beats=("beats_lad", "sum"),
                               beatsS=("beatsS_lad", "sum"),
                               dSharpe=("d_Sharpe_lad", "mean"),
                               dMaxDD=("d_MaxDD_lad", "mean"),
                               dCAGR=("d_CAGR_lad", "mean"),
                               lad_in_class=("lad_floor_only", "sum"))
    P(bb.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    P("    by arm kind (LADDER comparand):")
    kk = F.groupby("kind").agg(n=("beats_lad", "size"), beats=("beats_lad", "sum"),
                               beatsS=("beatsS_lad", "sum"),
                               dSharpe=("d_Sharpe_lad", "mean"),
                               dMaxDD=("d_MaxDD_lad", "mean"),
                               dCAGR=("d_CAGR_lad", "mean"))
    P(kk.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    P("    by panel x cost (LADDER comparand):")
    pc = F.groupby(["panel", "cost"]).agg(n=("beats_lad", "size"),
                                          beats=("beats_lad", "sum"),
                                          dSharpe=("d_Sharpe_lad", "mean"),
                                          dOOS=("d_OOS_Sharpe_lad", "mean"))
    P(pc.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    P("    the 12 members with the largest dSharpe against their own ladder point:")
    cols = ["panel", "book", "cost", "arm", "member_gross", "ladder_m", "ladder_gross",
            "mem_CAGR", "mem_Sharpe", "mem_MaxDD", "lad_CAGR", "lad_Sharpe", "lad_MaxDD",
            "d_Sharpe_lad", "d_MaxDD_lad", "mem_OOS_Sharpe", "lad_OOS_Sharpe"]
    P(F.sort_values("d_Sharpe_lad", ascending=False).head(12)[cols]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # =============================================================== [C] the proposal
    P("")
    P("=" * 150)
    P("[C] THE PROPOSED RECORDING RULE — a `4b-defensive` row must BEAT its own ladder "
      "point to be recorded")
    for tag, sfx in [("LADDER", "lad"), ("SCALAR", "sca")]:
        keep = F[F[f"beats_{sfx}"]]
        P(f"    {tag}: the class goes {len(F)} -> {len(keep)} rows "
          f"({len(keep)/max(1,len(F)):.1%} survive), across "
          f"{keep.book.nunique()} of {F.book.nunique()} books and "
          f"{keep.kind.nunique()} of {F.kind.nunique()} arm kinds.")
        if len(keep):
            P(f"        surviving books: {sorted(keep.book.unique())}")
            P(f"        surviving kinds: {sorted(keep.kind.unique())}")

    # =============================================================== [D] rule 8
    P("")
    P("=" * 150)
    P("[D] RULE 8 WALK-FORWARD — selectors fixed in writing, chosen on 2009-2016 only, "
      "2017-2026 read once")
    Lk = L.set_index(["panel", "book", "cost", "arm"])
    wf = []
    for (pname, cost), cell in G.groupby(["panel", "cost"]):
        spy = C.panel(pname)[1]
        px = C.panel(pname)[0]
        start = px.index[260]
        so = metrics(H.window(spy.loc[start:], "OOS"))
        pools = {"S0 no screen": cell,
                 "S3 class (idea 133)": cell[cell.IS_floor_only]}
        s5 = []
        for _, r in cell[cell.IS_floor_only].iterrows():
            k = (r["panel"], r["book"], r["cost"], r["arm"])
            if k in Lk.index:
                q = Lk.loc[k]
                if float(r["IS_Sharpe"]) > float(q["lad_IS_Sharpe"]):
                    s5.append(r)
        pools["S5 class + beats own IS ladder"] = pd.DataFrame(s5)
        for sel, pool in pools.items():
            if len(pool) == 0:
                wf.append(dict(panel=pname, cost=cost, selector=sel, pick="(empty)",
                               n_pool=0, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                               OOS_MaxDD=np.nan, spy_OOS_Sharpe=so["Sharpe"],
                               spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"]))
                continue
            pk = pool.loc[pool.IS_Sharpe.idxmax()]
            wf.append(dict(panel=pname, cost=cost, selector=sel,
                           pick=f"{pk['book']}/{pk['arm']}", n_pool=len(pool),
                           OOS_CAGR=pk["OOS_CAGR"], OOS_Sharpe=pk["OOS_Sharpe"],
                           OOS_MaxDD=pk["OOS_MaxDD"], spy_OOS_Sharpe=so["Sharpe"],
                           spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    for sel, s in W.groupby("selector"):
        ok = s.dropna(subset=["OOS_Sharpe"])
        P(f"    {sel:32s} mean OOS Sharpe {ok.OOS_Sharpe.mean():.4f}  CAGR "
          f"{ok.OOS_CAGR.mean():.2%}  MaxDD {ok.OOS_MaxDD.mean():.2%}  "
          f"(SPY OOS {ok.spy_OOS_Sharpe.mean():.4f} / {ok.spy_OOS_CAGR.mean():.2%} / "
          f"{ok.spy_OOS_MaxDD.mean():.2%})  cells {len(ok)}/{len(s)}")
    a = W[W.selector == "S3 class (idea 133)"].set_index(["panel", "cost"])
    b = W[W.selector == "S5 class + beats own IS ladder"].set_index(["panel", "cost"])
    j = a.join(b, rsuffix="_s5", how="inner").dropna(subset=["OOS_Sharpe", "OOS_Sharpe_s5"])
    P(f"    S5 changes S3's pick in {int((j['pick'] != j['pick_s5']).sum())}/{len(j)} cells; "
      f"paired mean OOS Sharpe S3 {j.OOS_Sharpe.mean():.4f} vs S5 "
      f"{j.OOS_Sharpe_s5.mean():.4f} (delta {j.OOS_Sharpe_s5.mean()-j.OOS_Sharpe.mean():+.4f})")

    # =============================================================== [E] answer
    P("")
    P("=" * 150)
    P("[E] ANSWER")
    P(f"    Class members that BEAT their own book's ladder point (Sharpe up AND drawdown "
      f"no worse): LADDER {int(F.beats_lad.sum())}/{len(F)} "
      f"({F.beats_lad.mean():.1%}), SCALAR {int(F.beats_sca.sum())}/{len(F)} "
      f"({F.beats_sca.mean():.1%}).")
    P(f"    The ladder point is itself in the class in {int(F.lad_floor_only.sum())}/{len(F)} "
      f"cases, and clears FULL 4b in {int(F.lad_pass4b.sum())}/{len(F)}.")
    P(f"    KEEP paths over the whole native corpus: 4a {int(G.pass4a.sum())}/{len(G)}, "
      f"4b {int(G.pass4b.sum())}/{len(G)}.")
    P("")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
