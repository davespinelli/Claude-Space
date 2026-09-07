#!/usr/bin/env python3
"""QUEUE idea 135 — is-a-class-member-just-its-own-ladder-point  (research sprint lane B, 2026-09-07)

QUESTION (pre-registered, from QUEUE.md idea 135)
    Idea 133 (both runs) established that the `4b-defensive` class — an arm clearing 4b's two
    halves-Sharpe bars, its OOS-Sharpe bar and its MaxDD cap and failing ONLY the CAGR floor —
    has members in six of eight books, and that membership is PARTLY manufactured by
    de-grossing: forcing 0.53 mean gross moves TOP20 from 1 member to 34 and TOP40 from 10 to
    52, while V1u/TOP5 join at no gross level and the sleeve books at every one.  A mean-gross
    COLUMN is therefore not enough to separate "the overlay did something" from "the overlay
    only lowered exposure".

    THE EXPLICIT CONTROL this run prices: every arm against ITS OWN BOOK'S STATIC-GROSS LADDER
    POINT AT MATCHED MEAN GROSS — the same book, ungated, no overlay, scaled by a single static
    multiplier m solved so that its mean gross over the same window equals the arm's.  The
    proposal under test: a `4b-defensive` row must BEAT that point to be recorded at all.

TWO FALSIFIABLE HYPOTHESES, both written before any number was read
    H_ladder  (the queue's worry) — a class member is its own ladder point.  Predictions:
              (i) a MINORITY of class members beat their matched ladder point on Sharpe;
              (ii) the matched ladder point is itself `4b-defensive` in most cases;
              (iii) the proposed recording rule therefore deletes most of the class.
    H_instrument — the overlay does something the gross dial cannot.  Predictions: (i) a
              MAJORITY of class members beat their matched ladder point; (ii) the ladder
              points are mostly NOT class members; (iii) the rule is close to free.
    The two make opposite predictions on the same table, so the run cannot be steered.

    NOTE ON THE SIMULATOR, read before the run was designed: `H.run` is NOT linear in the
    static multiplier m (step 4 re-drifts weights against total value INCLUDING cash, and step
    2 clips gross at 1.0), so a ladder point is a genuinely different path from a scaled arm
    and Sharpe is NOT invariant along the ladder.  The linearity check is reported in (0).

HARNESS — imported, not re-implemented
    idea 94  `2026-09-04_drawdown-insurance-price-list_B.py`  : simulator `H.run`, the 17 arms,
             the gates, the windows, `pass4a`, `LADDER`.
    idea 133 `2026-09-05_defensive-class-census_B.py`         : `book_targets` (8 books),
             `bars_win`, `margins_at`, `fails`, `pareto`, the panels.
    Nothing in this file re-types a book, a gate, a bar or a window.

CORPUS (native gross only — the matched-gross CONVENTION axis of idea 133 is replaced by the
        per-arm matched LADDER POINT, which is the control the question actually needs)
    panels  u56 (56), broad (136), small (439, SPY held out)
    books   V1u, TOP5, TOP10, TOP20, TOP40, EWall, SLV25, SLV50   (sleeve books need
            TLT/GLD/DBC/UUP and are not run on the small panel — stated, not hidden)
    arms    idea 94's 17: control, 5 gates x {dg, rw}, 2 stops, 2 DD controls, 2 entry budgets
    costs   10, 25 bps
    => (8 + 8 + 6) books x 17 arms x 2 costs = 748 arm rows, each carrying TWO matched ladder
       points (one solved on the full evaluation window, one solved on the IS window alone so
       the rule-8 screen uses no future information).  Every row is written to .grid.csv.

TUNED PARAMETERS — exactly two, both fully reported
    eps   the margin a class member must beat its ladder point by, in {0.00, 0.05, 0.10, 0.15}
          Sharpe units.  All four reported everywhere.
    stat  the comparison statistic: `sharpe` (Sharpe margin alone) or `dom` (Sharpe margin AND
          MaxDD no worse than the ladder point).  Both reported everywhere.
    Everything else — panels, books, arms, gates, dials, cost rungs, cadence, execution lag,
    window boundaries, 4b's coefficients (phi=0.70, delta=0.60) — is inherited unchanged.

WALK-FORWARD (PROTOCOL rule 8; selectors fixed in writing before any OOS number was read)
    Parameters chosen on 2009-2016 alone, 2017-2026 read once.  Cells pool ALL books within a
    (panel, cost) pair, because "which construction gets picked" is the question.
      S0   argmax IS Sharpe over every arm in the cell (no screen).
      S1   argmax IS Sharpe among arms meeting 4b's IS halves bars, DD cap and CAGR floor.
      S2   the same with the CAGR floor deleted (phi = 0).
      S3   idea 133's class selector: argmax IS Sharpe among IS-window `4b-defensive` arms.
      S3L  THE PROPOSAL: S3 restricted to arms that also beat their own IS-window matched
           ladder point by eps under `stat`.  Reported at every (eps, stat).
    Every pick is evaluated untouched on 2017-2026 against SPY, the LIVE baseline RULES v2,
    RULES v1, and the cell's own ungated control.

BOTH KEEP PATHS on all 748 rows: 4a against RULES v2 (the live book) AND against RULES v1
(continuity with the pre-2026-09-06 record); 4b via idea 129's five re-parameterised bars.

CAVEATS carried, not buried
    - Survivorship (idea 54): three current-constituent panels; absent delistings inflate every
      arm's CAGR and inflate the UNGATED, fully-invested books most — so the ladder control is
      if anything FLATTERED here, which cuts against H_ladder, not for it.
    - Idea 128: the IS window (SPY MaxDD -22.1%) is shallower than the OOS window (-33.7%), so
      the IS-window screens over-admit; this applies identically to S3 and S3L.
    - Idea 38: u56/broad still carry the calendar-day index; it applies identically to an arm
      and to its own ladder point and cancels in the paired comparison this run is about.
    - The gross match is solved by Newton on the mean gross of one window; the achieved gross
      is reported for every row and the worst mismatch is printed.  Where H.run's gross clip
      binds, the match cannot be exact and the row is flagged.
    - MaxDD is one number off one path; the `dom` statistic inherits that fragility.

RUN
    python research/backtests/2026-09-07_is-a-class-member-just-its-own-ladder-point_B.py
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

STEM = "2026-09-07_is-a-class-member-just-its-own-ladder-point_B"
OUT = ROOT / "research" / "backtests"


def _imp(name, fn):
    spec = importlib.util.spec_from_file_location(name, OUT / fn)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _imp("i94", "2026-09-04_drawdown-insurance-price-list_B.py")
C = _imp("i133", "2026-09-05_defensive-class-census_B.py")

FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
BOOKS = C.BOOKS
SLEEVE_BOOKS = C.SLEEVE_BOOKS
PHI0, DELTA0 = C.PHI0, C.DELTA0

EPSS = [0.00, 0.05, 0.10, 0.15]        # tuned parameter 1
STATS = ["sharpe", "dom"]              # tuned parameter 2

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- matched ladder point
def match_ladder(px, Wctl, cost, target_gross, start, which, steps=3):
    """The arm's OWN book, ungated, no overlay, at the single static multiplier m whose mean
    gross over window `which` equals `target_gross`.  Newton on a monotone map; the achieved
    gross is returned so every match is auditable."""
    m = 1.0
    r = g = None
    for _ in range(steps):
        res = H.run(px, Wctl, m=m, bps=cost)
        r = res["r"].loc[start:]
        g = float(H.window(res["gross"].loc[start:], which).mean())
        if g <= 1e-9:
            break
        m = float(np.clip(m * target_gross / g, 0.01, 5.0))
    # final evaluation at the last solved m
    res = H.run(px, Wctl, m=m, bps=cost)
    r = res["r"].loc[start:]
    g = float(H.window(res["gross"].loc[start:], which).mean())
    return r, m, g


def beats(d_sharpe, d_dd, eps, stat):
    """`sharpe`: Sharpe margin > eps.  `dom`: that AND MaxDD no worse than the ladder point."""
    ok = d_sharpe > eps
    if stat == "dom":
        ok = ok & (d_dd >= 0)
    return ok


# ---------------------------------------------------------------- one (panel, book, cost)
def do_cell(pname, px, book, cost, bfull, bIS, start):
    Wctl = C.book_targets(px, book)                      # the ladder's base: ungated book
    rows, rets, lrets = [], {}, {}
    for arm, kind, kw, (gate, conv) in H.arm_specs():
        W = C.book_targets(px, book, gate, conv)
        res = H.run(px, W, bps=cost, **kw)
        r = res["r"].loc[start:]
        gser = res["gross"].loc[start:]
        g_full, g_is = float(gser.mean()), float(H.window(gser, "IS").mean())

        lr_f, m_f, gach_f = match_ladder(px, Wctl, cost, g_full, start, "full")
        lr_i, m_i, gach_i = match_ladder(px, Wctl, cost, g_is, start, "IS")
        rets[arm], lrets[arm] = r, (lr_f, lr_i)

        mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
        lm, lmi = metrics(lr_f), metrics(H.window(lr_i, "IS"))
        lmo = metrics(H.window(lr_f, "OOS"))
        mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
        mgi = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
        lmg = C.margins_at(lr_f, bfull, PHI0, DELTA0, "full")
        lmgi = C.margins_at(lr_i, bIS, PHI0, DELTA0, "IS")
        f, lf = C.fails(mg), C.fails(lmg)
        h1, h2 = H.halves(r)

        rows.append(dict(
            panel=pname, book=book, cost=cost, arm=arm, kind=kind,
            gross=g_full, IS_gross=g_is,
            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            # --- the matched ladder point (full-window match)
            lad_m=m_f, lad_gross=gach_f, lad_gap=abs(gach_f - g_full),
            lad_CAGR=lm["CAGR"], lad_Sharpe=lm["Sharpe"], lad_MaxDD=lm["MaxDD"],
            lad_OOS_Sharpe=lmo["Sharpe"],
            lad_floor_only=(lf == ["CAGR"]), lad_pass4b=(len(lf) == 0),
            lad_fail4b=",".join(lf) or "-",
            d_Sharpe=mm["Sharpe"] - lm["Sharpe"],
            d_MaxDD=abs(lm["MaxDD"]) - abs(mm["MaxDD"]),      # >0 => arm is SHALLOWER
            d_CAGR=mm["CAGR"] - lm["CAGR"],
            d_OOS_Sharpe=mo["Sharpe"] - lmo["Sharpe"],
            # --- the IS-window matched ladder point (used by the prospective screen)
            IS_lad_m=m_i, IS_lad_gross=gach_i, IS_lad_gap=abs(gach_i - g_is),
            IS_lad_Sharpe=lmi["Sharpe"], IS_lad_MaxDD=lmi["MaxDD"],
            IS_d_Sharpe=mi["Sharpe"] - lmi["Sharpe"],
            IS_d_MaxDD=abs(lmi["MaxDD"]) - abs(mi["MaxDD"]),
            IS_lad_floor_only=(C.fails(lmgi) == ["CAGR"]),
            # --- 4b bookkeeping (idea 129/133 definitions verbatim)
            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
            pass4b=(len(f) == 0), fail4b=",".join(f) or "-", n_fail=len(f),
            floor_only=(f == ["CAGR"]),
            IS_floor_only=(C.fails(mgi) == ["CAGR"]),
            IS_admit_phi70=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
            IS_admit_phi00=all(mgi[k] > 0 for k in ("H1", "H2", "DD")),
            TO=float(res["to"].loc[start:].sum() / (len(r) / 252)),
        ))
    D = pd.DataFrame(rows)
    return D, rets, lrets


# ---------------------------------------------------------------- rule 8
def walk_forward(sub, RET, key, spy, v1_net, v2_net, ctl_ret):
    mc = metrics(H.window(ctl_ret, "OOS"))
    ms = metrics(spy.loc[OOS_START:])
    mv1 = metrics(H.window(v1_net, "OOS"))
    mv2 = metrics(H.window(v2_net, "OOS"))
    cands = [("S0", sub, np.nan, "-"),
             ("S1", sub[sub.IS_admit_phi70], np.nan, "-"),
             ("S2", sub[sub.IS_admit_phi00], np.nan, "-"),
             ("S3", sub[sub.IS_floor_only], np.nan, "-")]
    for stat in STATS:
        for eps in EPSS:
            ok = sub.IS_floor_only & beats(sub.IS_d_Sharpe, sub.IS_d_MaxDD, eps, stat)
            cands.append((f"S3L", sub[ok], eps, stat))
    out = []
    order = sub.OOS_Sharpe.rank(ascending=False)
    for s, c, eps, stat in cands:
        base = dict(sel=s, eps=eps, stat=stat, panel=key[0], cost=key[1],
                    n_cell=len(sub),
                    ctl_OOS_Sharpe=mc["Sharpe"], spy_OOS_CAGR=ms["CAGR"],
                    spy_OOS_Sharpe=ms["Sharpe"], spy_OOS_MaxDD=ms["MaxDD"],
                    v1_OOS_Sharpe=mv1["Sharpe"],
                    v2_OOS_CAGR=mv2["CAGR"], v2_OOS_Sharpe=mv2["Sharpe"],
                    v2_OOS_MaxDD=mv2["MaxDD"])
        if not len(c):
            out.append(dict(base, pick="(none)", pick_book="(none)", n_admitted=0,
                            OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                            beat_ctl=np.nan, beat_spy=np.nan, beat_v2=np.nan,
                            oos_rank=np.nan))
            continue
        p = c.loc[c.IS_Sharpe.idxmax()]
        r = H.window(RET[(p["book"], p["arm"])], "OOS")
        m = metrics(r)
        out.append(dict(base, pick=f"{p['book']}/{p['arm']}", pick_book=p["book"],
                        n_admitted=len(c), OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                        OOS_MaxDD=m["MaxDD"],
                        beat_ctl=bool(m["Sharpe"] > mc["Sharpe"]),
                        beat_spy=bool(m["Sharpe"] > ms["Sharpe"]),
                        beat_v2=bool(m["Sharpe"] > mv2["Sharpe"]),
                        oos_rank=float(order.loc[p.name])))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- reproduction gate
def reproduce():
    say("=" * 200)
    say("(0) REPRODUCTION — nothing new is read until these pass")
    px, spy, _ = C.panel("u56")
    start = px.index[260]

    r = H.run(px, C.book_targets(px, "EWall", "vol60", "dg"), bps=10.0)["r"].loc[start:]
    m = metrics(r)
    say(f"    (a) idea 94's EWall+vol60-dg u56@10bps: {m['CAGR']:.3%} / {m['Sharpe']:.3f} / "
        f"{m['MaxDD']:.3%}   published 11.6% / 1.133 / -16.9%   "
        f"{'PASS' if abs(m['Sharpe'] - 1.133) < 5e-4 else 'FAIL'}")
    assert abs(m["Sharpe"] - 1.133) < 5e-4

    W = C.book_targets(px, "EWall")
    a = H.run(px, W, bps=10.0)["r"].loc[start:]
    b = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
    d = float((a - b).abs().max())
    say(f"    (b) H.run vs engine.backtest (EWall, 10bps): max|diff| = {d:.3e}   "
        f"{'PASS' if d < 1e-12 else 'FAIL'}")
    assert d < 1e-12

    # (c) the ladder is NOT a linear rescaling — the control this idea prices is a real path
    r1 = H.run(px, W, m=1.0, bps=10.0)["r"].loc[start:]
    r5 = H.run(px, W, m=0.5, bps=10.0)["r"].loc[start:]
    lin = float((r5 - 0.5 * r1).abs().max())
    say(f"    (c) linearity check  max|r(m=0.5) - 0.5*r(m=1)| = {lin:.3e}  "
        f"Sharpe {metrics(r1)['Sharpe']:.4f} (m=1) vs {metrics(r5)['Sharpe']:.4f} (m=0.5) "
        f"-> the ladder point is a DIFFERENT path, not a rescaling   "
        f"{'PASS' if lin > 1e-9 else 'DEGENERATE (Sharpe would be m-invariant)'}")

    # (d) the matched-ladder solver hits its target
    res = H.run(px, C.book_targets(px, "EWall", "g200", "dg"), bps=10.0)
    tgt = float(res["gross"].loc[start:].mean())
    lr, mm_, gach = match_ladder(px, W, 10.0, tgt, start, "full")
    say(f"    (d) ladder solve: target gross {tgt:.4f} achieved {gach:.4f} at m={mm_:.4f}  "
        f"|gap| {abs(gach - tgt):.2e}   {'PASS' if abs(gach - tgt) < 5e-3 else 'FAIL'}")
    assert abs(gach - tgt) < 5e-3


def reproduce_133(G):
    """The native-gross rows must reproduce idea 133's committed census exactly."""
    ref = pd.read_csv(OUT / "2026-09-05_defensive-class-census_B.grid.csv")
    ref = ref[ref.gross_mode == "native"]
    k = ["panel", "book", "cost", "arm"]
    j = ref.merge(G, on=k, suffixes=("_133", "_135"))
    say(f"    (e) idea 133 native-gross census re-run: {len(j)} of {len(ref)} rows matched")
    worst = 0.0
    for col in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "gross"):
        d = float((j[f"{col}_133"] - j[f"{col}_135"]).abs().max())
        worst = max(worst, d)
        say(f"        max|d {col}| = {d:.3e}")
    nf = int((j["floor_only_133"] != j["floor_only_135"]).sum())
    n4b = int((j["pass4b_133"] != j["pass4b_135"]).sum())
    say(f"        floor_only mismatches {nf}/{len(j)}   pass4b mismatches {n4b}/{len(j)}   "
        f"{'PASS' if nf == 0 and n4b == 0 and worst < 1e-9 else 'FAIL'}")
    return nf, n4b, worst


# ---------------------------------------------------------------- main
def main():
    say("=" * 200)
    say("IDEA 135 — is a `4b-defensive` class member just its own book's ladder point?")
    say(f"corpus: panels {PANELS} x books {BOOKS} (sleeve books u56/broad only) x 17 arms x "
        f"costs {COSTS} bps, NATIVE gross; each arm paired with its OWN book's ungated "
        f"static-gross ladder point at matched mean gross (full-window and IS-window matches).")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1.  Bars: CAGR >= {PHI0} x SPY, "
        f"MaxDD <= {DELTA0} x |SPY|.")
    say(f"tuned: eps in {EPSS} (Sharpe margin over the ladder point), stat in {STATS}.  "
        f"All grid points reported.")
    say("=" * 200)

    reproduce()

    GR, WF = [], []
    for pname in PANELS:
        px, spy, desc = C.panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        books = [b for b in BOOKS if not (pname == "small" and b in SLEEVE_BOOKS)]
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()} | "
            f"books {books}")
        say(f"    SPY full CAGR {bfull['scagr']:.2%} MaxDD {bfull['sdd']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} OOS Sharpe {bfull['soos']:.3f}")

        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c,
                          freq=FREQ)["returns"].loc[start:] for c in COSTS}
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c,
                          freq=FREQ)["returns"].loc[start:] for c in COSTS}
        for c in COSTS:
            RET, cellD = {}, []
            for book in books:
                D, rets, _ = do_cell(pname, px, book, c, bfull, bIS, start)
                for a, r in rets.items():
                    RET[(book, a)] = r
                cellD.append(D)
            sub = pd.concat(cellD, ignore_index=True)
            sub["pass4a_v1"] = [H.pass4a(RET[(b, a)], v1[c])
                                for b, a in zip(sub.book, sub.arm)]
            sub["pass4a_v2"] = [H.pass4a(RET[(b, a)], v2[c])
                                for b, a in zip(sub.book, sub.arm)]
            # cross-book Pareto front within the (panel, cost) cell
            sub["pareto"] = C.pareto(sub)
            GR.append(sub)
            WF.append(walk_forward(sub, RET, (pname, c), spy, v1[c], v2[c],
                                   RET[("EWall", "control")]))
            say(f"    [{pname} @{c:.0f}bps] {len(sub)} arm rows | class members "
                f"{int(sub.floor_only.sum())} | 4b {int(sub.pass4b.sum())} | "
                f"4a(v2) {int(sub.pass4a_v2.sum())} | 4a(v1) {int(sub.pass4a_v1.sum())}")

    G = pd.concat(GR, ignore_index=True)
    W = pd.concat(WF, ignore_index=True)

    say("\n" + "=" * 200)
    say("(0b) REPRODUCTION of idea 133's committed native-gross census")
    reproduce_133(G)
    say(f"    ladder match quality: worst |achieved - target| gross, full-window "
        f"{G.lad_gap.max():.2e}, IS-window {G.IS_lad_gap.max():.2e}; "
        f"rows worse than 5e-3: {int((G.lad_gap > 5e-3).sum())} / {len(G)}")

    # ------------------------------------------------------------ (1) the headline
    say("\n" + "=" * 200)
    say("(1) THE CONTROL — does a class member beat its own book's matched ladder point?")
    cls = G[G.floor_only]
    say(f"    class members (`4b-defensive`, full window): {len(cls)} of {len(G)} rows "
        f"({len(cls)/len(G):.1%})")
    say(f"    their matched ladder point is ITSELF `4b-defensive` in "
        f"{int(cls.lad_floor_only.sum())} of {len(cls)} cases "
        f"({cls.lad_floor_only.mean():.1%})  <- H_ladder predicts MOST")
    say(f"    mean d_Sharpe {cls.d_Sharpe.mean():+.4f}  median {cls.d_Sharpe.median():+.4f}  "
        f"mean d_MaxDD {cls.d_MaxDD.mean():+.2%}  mean d_CAGR {cls.d_CAGR.mean():+.2%}  "
        f"mean d_OOS_Sharpe {cls.d_OOS_Sharpe.mean():+.4f}")
    rows = []
    for stat in STATS:
        for eps in EPSS:
            b_all = beats(G.d_Sharpe, G.d_MaxDD, eps, stat)
            b_cls = beats(cls.d_Sharpe, cls.d_MaxDD, eps, stat)
            par = cls[cls.pareto]
            b_par = beats(par.d_Sharpe, par.d_MaxDD, eps, stat)
            rows.append(dict(stat=stat, eps=eps,
                             all_rows=f"{int(b_all.sum())}/{len(G)}",
                             all_pct=b_all.mean(),
                             class_rows=f"{int(b_cls.sum())}/{len(cls)}",
                             class_pct=b_cls.mean(),
                             pareto_class=f"{int(b_par.sum())}/{len(par)}",
                             pareto_pct=b_par.mean() if len(par) else np.nan))
    T1 = pd.DataFrame(rows)
    say("\n    SURVIVAL of the proposed recording rule (a `4b-defensive` row must beat its own "
        "matched ladder point):")
    say(T1.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n    by book (class members only, stat=sharpe eps=0.00):")
    b0 = beats(cls.d_Sharpe, cls.d_MaxDD, 0.0, "sharpe")
    t = cls.assign(beat=b0).groupby("book").apply(lambda d: pd.Series(dict(
        n=len(d), beat=int(d.beat.sum()), pct=d.beat.mean(),
        mean_d_Sharpe=d.d_Sharpe.mean(), mean_gross=d.gross.mean(),
        lad_is_class=d.lad_floor_only.mean())), include_groups=False)
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n    by panel x cost (class members only, stat=sharpe eps=0.00):")
    t = cls.assign(beat=b0).groupby(["panel", "cost"]).apply(lambda d: pd.Series(dict(
        n=len(d), beat=int(d.beat.sum()), pct=d.beat.mean(),
        mean_d_Sharpe=d.d_Sharpe.mean(), lad_is_class=d.lad_floor_only.mean())),
        include_groups=False)
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n    by arm kind (class members only, stat=sharpe eps=0.00):")
    t = cls.assign(beat=b0).groupby("kind").apply(lambda d: pd.Series(dict(
        n=len(d), beat=int(d.beat.sum()), pct=d.beat.mean(),
        mean_d_Sharpe=d.d_Sharpe.mean(), mean_gross=d.gross.mean())), include_groups=False)
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n    is the margin just the gross dial?  Spearman over class members:")
    say(f"        rho(gross, d_Sharpe)  = {H.spearman(cls.gross, cls.d_Sharpe):+.3f}")
    say(f"        rho(gross, Sharpe)    = {H.spearman(cls.gross, cls.Sharpe):+.3f}")
    say(f"        rho(d_Sharpe, d_OOS_Sharpe) = "
        f"{H.spearman(cls.d_Sharpe, cls.d_OOS_Sharpe):+.3f}   (does an IS win persist?)")

    say("\n    the 20 class members with the LARGEST margin over their own ladder point:")
    cols = ["panel", "book", "arm", "cost", "gross", "Sharpe", "lad_Sharpe", "d_Sharpe",
            "MaxDD", "lad_MaxDD", "d_MaxDD", "CAGR", "d_CAGR", "OOS_Sharpe", "d_OOS_Sharpe",
            "lad_floor_only"]
    say(cls.sort_values("d_Sharpe", ascending=False).head(20)[cols]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n    the 10 class members with the WORST margin (these the rule deletes first):")
    say(cls.sort_values("d_Sharpe").head(10)[cols]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------ (2) the ladder's own class
    say("\n" + "=" * 200)
    say("(2) THE LADDER POINTS THEMSELVES — is `4b-defensive` a property of de-grossing?")
    say(f"    matched ladder points that are `4b-defensive`: "
        f"{int(G.lad_floor_only.sum())} of {len(G)} ({G.lad_floor_only.mean():.1%})")
    say(f"    matched ladder points that PASS 4b outright: "
        f"{int(G.lad_pass4b.sum())} of {len(G)} ({G.lad_pass4b.mean():.1%})")
    x = pd.crosstab(G.floor_only, G.lad_floor_only)
    say("\n    arm class membership (rows) vs its matched ladder point's (cols):")
    say(x.to_string())
    say(f"\n    arms in the class whose ladder point is NOT: {int((G.floor_only & ~G.lad_floor_only).sum())}"
        f"   |   ladder points in the class whose arm is NOT: "
        f"{int((~G.floor_only & G.lad_floor_only).sum())}")
    say("\n    ladder-point class rate by book (pure de-grossing, no overlay at all):")
    say(G.groupby("book").apply(lambda d: pd.Series(dict(
        n=len(d), lad_class=d.lad_floor_only.mean(), arm_class=d.floor_only.mean(),
        mean_lad_m=d.lad_m.mean())), include_groups=False)
        .to_string(float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------ (3) rule 8
    say("\n" + "=" * 200)
    say("(3) RULE 8 WALK-FORWARD — parameters chosen on 2009-2016, 2017-2026 read once")
    say("    cells pool ALL books within a (panel, cost) pair; S3L is the proposed screen.")
    cols = ["panel", "cost", "sel", "eps", "stat", "n_admitted", "pick", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "beat_spy", "beat_v2", "beat_ctl", "oos_rank"]
    say(W[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n    selector summary (means over the 6 panel x cost cells):")
    su = W.groupby(["sel", "eps", "stat"], dropna=False).apply(lambda d: pd.Series(dict(
        cells=len(d), picks=int(d["pick"].ne("(none)").sum()),
        n_admitted=d.n_admitted.mean(),
        OOS_CAGR=d.OOS_CAGR.mean(), OOS_Sharpe=d.OOS_Sharpe.mean(),
        OOS_MaxDD=d.OOS_MaxDD.mean(),
        beat_spy=d.beat_spy.sum(), beat_v2=d.beat_v2.sum(), beat_ctl=d.beat_ctl.sum(),
        mean_rank=d.oos_rank.mean())), include_groups=False)
    say(su.to_string(float_format=lambda x: f"{x:.3f}"))
    ref = W[W.sel == "S0"]
    say(f"\n    references (means over cells): SPY OOS {ref.spy_OOS_CAGR.mean():.2%} / "
        f"{ref.spy_OOS_Sharpe.mean():.3f} / {ref.spy_OOS_MaxDD.mean():.2%} | "
        f"RULES v2 (live) OOS {ref.v2_OOS_CAGR.mean():.2%} / {ref.v2_OOS_Sharpe.mean():.3f} / "
        f"{ref.v2_OOS_MaxDD.mean():.2%} | RULES v1 OOS Sharpe {ref.v1_OOS_Sharpe.mean():.3f} | "
        f"ungated EWall control OOS Sharpe {ref.ctl_OOS_Sharpe.mean():.3f}")

    say("\n    PAIRED: does the ladder screen change S3's pick, and does it help?")
    s3 = W[W.sel == "S3"].set_index(["panel", "cost"])
    prows = []
    for stat in STATS:
        for eps in EPSS:
            s3l = W[(W.sel == "S3L") & (W.stat == stat) & (W.eps == eps)].set_index(
                ["panel", "cost"])
            j = s3.join(s3l, rsuffix="_L")
            moved = int((j["pick"] != j["pick_L"]).sum())
            d = (j["OOS_Sharpe_L"] - j["OOS_Sharpe"])
            prows.append(dict(stat=stat, eps=eps, cells=len(j), picks_moved=moved,
                              empty_cells=int((j["pick_L"] == "(none)").sum()),
                              mean_d_OOS_Sharpe=d.mean(), min_d=d.min(), max_d=d.max()))
    P = pd.DataFrame(prows)
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ (4) KEEP paths
    say("\n" + "=" * 200)
    say("(4) BOTH KEEP PATHS on all rows")
    say(f"    4a vs RULES v2 (live): {int(G.pass4a_v2.sum())} of {len(G)}")
    say(f"    4a vs RULES v1 (continuity): {int(G.pass4a_v1.sum())} of {len(G)}")
    say(f"    4b: {int(G.pass4b.sum())} of {len(G)}")
    if G.pass4b.any():
        say(G[G.pass4b].groupby(["panel", "book"]).size().to_string())
        k = G[G.pass4b].sort_values("Sharpe", ascending=False).head(12)
        say("\n    best 4b passes (and whether each beats its OWN matched ladder point):")
        say(k[["panel", "book", "arm", "cost", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "OOS_Sharpe", "lad_Sharpe", "d_Sharpe", "d_MaxDD", "lad_pass4b", "TO"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        nat = G[G.panel.isin(["u56", "broad"])]
        srv = (nat.groupby(["book", "arm"]).pass4b.sum() == 4)
        say("\n    cross-cell survivors (4b in all four u56/broad x 10/25bps cells): "
            + (", ".join(f"{b}/{a}" for (b, a), v in srv.items() if v) or "(none)"))
    if G.pass4a_v2.any():
        say("\n    4a(v2) passes:")
        say(G[G.pass4a_v2].groupby(["panel", "book"]).size().to_string())

    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    T1.to_csv(OUT / f"{STEM}.survival.csv", index=False)
    P.to_csv(OUT / f"{STEM}.paired.csv", index=False)
    say(f"\nWrote {STEM}.{{grid,walkforward,survival,paired}}.csv and .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
