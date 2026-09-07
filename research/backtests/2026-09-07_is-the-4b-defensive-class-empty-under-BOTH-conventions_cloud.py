#!/usr/bin/env python3
"""QUEUE idea 397 — is-the-4b-defensive-class-empty-under-BOTH-conventions  (cloud, 2026-09-07)

QUESTION (pre-registered, from QUEUE.md idea 397, verbatim)
    "idea 135 (_B2) found the class survives its own matched-GROSS ladder point in 12.2% of 531
     members but its matched-DRAWDOWN ladder point (idea 94's convention) in 58.9%, on the same
     rows.  Intersect them: report how many members beat BOTH controls, and whether the 4.8x
     convention gap is one book, one arm kind or uniform.  If the intersection is near-empty the
     class should be deleted, not amended.  Max 2 params."

    `4b-defensive` (idea 129's proposed reporting class): an arm that clears 4b's two
    halves-Sharpe bars, its OOS-Sharpe bar and its MaxDD cap, and fails ONLY the CAGR floor.

WHAT THIS RUN ADDS TO IDEA 135
    Idea 135 (_B2) computed D1 (matched GROSS) and D4 (matched DRAWDOWN) on the same 1,632 rows
    but never crossed them, and never computed D4 on the IS window, so the matched-drawdown
    convention has never been walked forward.  This run
      (a) rebuilds the whole 1,632-row corpus FROM SOURCE with _B2's own harness and asserts it
          against the committed grid before reading anything new,
      (b) computes the 2x2 intersection D1 x D4 over the 531 members and decomposes the
          convention gap by panel, book, arm kind, cost rung and gross mode,
      (c) computes D4_IS (the matched-drawdown bar on 2009-2016 alone) so rule 8 can be run on
          the matched-DD convention and on the intersection, which idea 135 could not do,
      (d) measures WHY the two conventions disagree, on the mechanism the ladder makes visible:
          the ladder multiplier m each convention selects for the same arm.

TWO FALSIFIABLE HYPOTHESES, written down before any new number was read
    H_empty  (the queue's stated worry) — the two conventions are near-disjoint tests, so the
             intersection is near-empty (<= 5% of members) and the class as recorded should be
             DELETED, not amended.  Prediction: BOTH-rate << min(12.2%, 58.9%) x 1, i.e. the
             D1 survivors are NOT mostly inside D4.
    H_nested — the conventions are the same test at different strictness: matched-gross is the
             harder one, so its survivors are a SUBSET of the matched-drawdown survivors and the
             intersection is ~12.2% of members (~65 rows).  The class then has a non-empty core
             and should be AMENDED with a stated convention, not deleted.
    They make opposite predictions on the same 2x2 table, so the run cannot be steered.

    Note both hypotheses are about the CROSS.  D1 = 12.2% and D4 = 58.9% are inputs, reproduced
    here as gates, not findings of this run.

DECISION RULES (conventions, not tuned dials; every one reported for all 1,632 rows)
    D1  matched GROSS      Sharpe > ladder's AND |MaxDD| <= ladder's, at the ladder point whose
                           MEAN GROSS equals the arm's own  (idea 135's proposal)
    D4  matched DRAWDOWN   CAGR > the static-gross ladder's CAGR interpolated to the arm's own
                           MaxDD  (idea 94's convention)
    BOTH = D1 & D4         the queue's deliverable
    D4_IS / D1_IS          the same two bars computed on 2009-2016 alone, for rule 8
    All carry idea 135's 1e-9 tolerance, for the reason idea 135 gives: the ungated `control`
    arm IS its own ladder point and a bare `>` lets it beat itself by 2.2e-16.
    D4 is UNDEFINED (NaN) when the arm's MaxDD falls outside its own ladder's drawdown range;
    undefined rows are counted separately and never silently scored as failures.

TUNED PARAMETERS — exactly two, both inherited from ideas 133/135, both fully reported
    n  ranked book size    in {5, 10, 20, 40}
    f  sleeve fraction     in {0.25, 0.50}
    Nothing else is tuned.  Books, arms, gates, cadence, execution lag, cost rungs, window
    boundaries, gross-matching targets, the ladder grid and 4b's coefficients (phi=0.70,
    delta=0.60) are inherited unchanged from ideas 94/129/133/135.

CORPUS (identical to idea 135 _B2, so the gate is meaningful)
    panels  u56 (56), broad (136).  SMALL excluded: idea 133 has 0 floor-only rows of 612 there
            and idea 136 confirms 0/180 — there is no member on that panel to price.  Asserted.
    books   V1u, TOP5, TOP10, TOP20, TOP40, EWall, SLV25, SLV50
    arms    idea 94's 17: control, 5 gates x {dg, rw}, 2 stops, 2 DD controls, 2 entry budgets
    costs   10, 25 bps     gross modes  native, m53, m75
    => 1,632 arm rows, all written to .grid.csv.

WALK-FORWARD (PROTOCOL rule 8; selectors fixed in writing before any OOS number was read)
    Parameters chosen on 2009-2016 alone; 2017-2026 read once.  A cell pools all books within a
    (panel, cost, gross mode) triple, as in ideas 133/135.
      S0  no screen            argmax IS Sharpe over every arm (idea 151's do-nothing)
      S3  IS floor-only        idea 133's class selector
      S5  S3 + D1_IS           idea 135's proposal (matched GROSS)
      S8  S3 + D4_IS           the matched-DRAWDOWN convention, never walked forward before
      S9  S3 + D1_IS + D4_IS   THE INTERSECTION — this run's deliverable as a selector
      S6  D1_IS alone          isolates the ladder screen from the class restriction
      S10 D4_IS alone          the same for the matched-DD convention
    Every pick is evaluated untouched on 2017-2026 against SPY, the LIVE baseline (RULES v2),
    RULES v1 and the cell's own ungated EWall control.

BOTH KEEP PATHS on every one of the 1,632 rows
    4a  Sharpe > the LIVE book (RULES v2) in BOTH halves and MaxDD no worse.  RULES v1 reported
        beside it for continuity with the pre-2026-09-06 record.
    4b  the five bars vs SPY (H1, H2, OOS, MaxDD cap 0.60x, CAGR floor 0.70x).

CAVEATS carried, not buried
    - Survivorship (idea 54): current-constituent panels.  It inflates the ungated, fully
      invested LADDER control most, so both controls are if anything HARD tests — which runs
      against this run's likely finding, not for it.
    - Idea 128: the IS window (SPY MaxDD -22.1%) cannot express deep drawdowns, so D1_IS and
      D4_IS are both measured on a short ruler.  This is why rule 8 is reported for BOTH
      conventions and their cross rather than for one.
    - MaxDD is one number off one path.  D1 tie-breaks on it and D4 is defined entirely by it,
      so the two conventions inherit that fragility differently — the point of the cross.
    - Matched-gross and matched-drawdown ladder points are NOT the same instrument as the m=1
      book and are never quoted as one.
    - Idea 38: u56/broad carry the calendar-day index; it applies identically to an arm and to
      both of its controls and cancels in every comparison made here.

RUN
    python research/backtests/2026-09-07_is-the-4b-defensive-class-empty-under-BOTH-conventions_cloud.py
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

STEM = "2026-09-07_is-the-4b-defensive-class-empty-under-BOTH-conventions_cloud"
OUT = ROOT / "research" / "backtests"
REF_GRID = OUT / "2026-09-07_is-a-class-member-just-its-own-ladder-point_B2.grid.csv"


def _imp(name, fn):
    spec = importlib.util.spec_from_file_location(name, OUT / fn)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


B = _imp("i135B2", "2026-09-07_is-a-class-member-just-its-own-ladder-point_B2.py")
C = B.C                                     # idea 133: books, gross matching, 4b bars
H = B.H                                     # idea 94: simulator, arms, ladder, matched_dd

FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = B.COSTS
PANELS = B.PANELS
BOOKS = C.BOOKS
GROSS_LEVELS = C.GROSS_LEVELS
PHI0, DELTA0 = C.PHI0, C.DELTA0
LADDER = H.LADDER
TOL = B.TOL

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", 4000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def pct(k, n):
    return f"{k}/{n} = {(k / n if n else np.nan):.1%}"


# ---------------------------------------------------------------- IS-window ladder (new)
_ISLAD = {}


def is_ladder(pname, px, book, cost, start):
    """The same static-gross ladder idea 94 uses, but with metrics computed on the IS window
    (2009-2016) instead of the full sample, so the matched-DRAWDOWN bar can be evaluated with
    2017-2026 untouched.  Same book, same grid of m, same simulator."""
    key = (pname, book, cost)
    if key in _ISLAD:
        return _ISLAD[key]
    W = B.base_book(pname, px, book)
    rows = []
    for m in LADDER:
        r = H.run(px, W, m=float(m), bps=cost)["r"].loc[start:]
        mi = metrics(H.window(r, "IS"))
        rows.append(dict(m=float(m), CAGR=mi["CAGR"], Sharpe=mi["Sharpe"], MaxDD=mi["MaxDD"]))
    L = pd.DataFrame(rows)
    _ISLAD[key] = L
    return L


def ladder_m_at_dd(L, target_dd):
    """The ladder multiplier m whose MaxDD equals the arm's, by the same linear interpolation
    idea 94's matched_dd uses on CAGR.  Reported so the two conventions can be compared on the
    one axis they share: which point of the same ladder each one picks."""
    d = L.sort_values("MaxDD", key=lambda s: s.abs())
    x = d["MaxDD"].abs().values * 100.0
    y = d["m"].values
    t = abs(target_dd) * 100.0
    if t < x[0] or t > x[-1]:
        return np.nan
    return float(np.interp(t, x, y))


# ---------------------------------------------------------------- the corpus
def build():
    GR, WF = [], []
    SPYREF = {}
    for pname in PANELS:
        px, spy, desc = C.panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        mo = metrics(spy.loc[OOS_START:])
        SPYREF[pname] = dict(desc=desc, **bfull, oos_cagr=mo["CAGR"], oos_dd=mo["MaxDD"],
                             oos_sharpe=mo["Sharpe"])
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY full CAGR {bfull['scagr']:.2%} MaxDD {bfull['sdd']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} OOS Sharpe {bfull['soos']:.3f} | 4b bars: "
            f"CAGR >= {PHI0 * bfull['scagr']:.2%}/yr, MaxDD >= {-DELTA0 * abs(bfull['sdd']):.2%}")

        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        for c in COSTS:
            mv2, mv1 = metrics(v2[c]), metrics(v1[c])
            say(f"    live RULES v2 @{int(c)}bps: {mv2['CAGR']:.2%} / {mv2['Sharpe']:.3f} / "
                f"{mv2['MaxDD']:.2%}   RULES v1: {mv1['CAGR']:.2%} / {mv1['Sharpe']:.3f} / "
                f"{mv1['MaxDD']:.2%}")

        for glabel, gtarget in GROSS_LEVELS.items():
            for c in COSTS:
                RET, cellrows = {}, []
                for book in BOOKS:
                    D, rets, _ = B.do_cell(pname, px, spy, book, c, glabel, gtarget,
                                           bfull, bIS, v1[c], v2[c], start)
                    # ---- the new columns: the matched-DRAWDOWN bar on the IS window, and the
                    #      ladder multiplier each convention selects.
                    LI = is_ladder(pname, px, book, c, start)
                    LF = B.static_ladder(pname, px, book, c, start)
                    d4is, m_at_dd, m_at_dd_is = [], [], []
                    for _, row in D.iterrows():
                        cis = H.matched_dd(LI, row["IS_MaxDD"])
                        d4is.append(bool(np.isfinite(cis)
                                         and row["IS_CAGR"] * 100.0 - cis > TOL))
                        m_at_dd.append(ladder_m_at_dd(LF, row["MaxDD"]))
                        m_at_dd_is.append(ladder_m_at_dd(LI, row["IS_MaxDD"]))
                    D["D4_IS"] = d4is
                    D["lad_CAGR_at_matchedDD_IS"] = [H.matched_dd(LI, r) for r in D["IS_MaxDD"]]
                    D["lad_m_at_matchedDD"] = m_at_dd
                    D["lad_m_at_matchedDD_IS"] = m_at_dd_is
                    D["D4_defined"] = np.isfinite(D["lad_CAGR_at_matchedDD"].values)
                    D["D4_IS_defined"] = np.isfinite(D["lad_CAGR_at_matchedDD_IS"].values)
                    cellrows.append(D)
                    for a, r in rets.items():
                        RET[(book, a)] = r
                CD = pd.concat(cellrows, ignore_index=True)
                GR.append(CD)
                WF.append(walk_forward(CD, RET, (pname, c, glabel), spy, v1[c], v2[c],
                                       RET[("EWall", "control")]))
                fo = CD[CD.floor_only]
                say(f"    {pname:5s} gross={glabel:6s} {int(c):2d}bps: {len(CD):3d} arms | "
                    f"4b {int(CD.pass4b.sum()):3d} | 4a(v2) {int(CD.pass4a_v2.sum()):3d} | "
                    f"members {len(fo):3d} | D1 {int(fo.D1.sum()):3d} | D4 {int(fo.D4.sum()):3d} "
                    f"| BOTH {int((fo.D1 & fo.D4).sum()):3d}")
    G = pd.concat(GR, ignore_index=True)
    G["constr"] = G.apply(C.construction, axis=1)
    G["BOTH"] = G.D1 & G.D4
    G["EITHER"] = G.D1 | G.D4
    G["BOTH_IS"] = G.D1_IS & G.D4_IS
    return G, pd.concat(WF, ignore_index=True), SPYREF


# ---------------------------------------------------------------- rule 8
def walk_forward(sub, RET, key, spy, v1_net, v2_net, ctl_ret):
    mc = metrics(H.window(ctl_ret, "OOS"))
    ms = metrics(spy.loc[OOS_START:])
    mv1 = metrics(H.window(v1_net, "OOS"))
    mv2 = metrics(H.window(v2_net, "OOS"))
    cand = {
        "S0": sub,
        "S3": sub[sub.IS_floor_only],
        "S5": sub[sub.IS_floor_only & sub.D1_IS],
        "S8": sub[sub.IS_floor_only & sub.D4_IS],
        "S9": sub[sub.IS_floor_only & sub.D1_IS & sub.D4_IS],
        "S6": sub[sub.D1_IS],
        "S10": sub[sub.D4_IS],
    }
    out = []
    order = sub.OOS_Sharpe.rank(ascending=False)
    for s, c in cand.items():
        base = dict(sel=s, panel=key[0], cost=key[1], gross_mode=key[2],
                    ctl_OOS_Sharpe=mc["Sharpe"], spy_OOS_Sharpe=ms["Sharpe"],
                    spy_OOS_CAGR=ms["CAGR"], spy_OOS_MaxDD=ms["MaxDD"],
                    v1_OOS_Sharpe=mv1["Sharpe"], v2_OOS_Sharpe=mv2["Sharpe"],
                    v2_OOS_CAGR=mv2["CAGR"], v2_OOS_MaxDD=mv2["MaxDD"])
        if not len(c):
            out.append(dict(base, pick="(none)", pick_book="(none)", n_admitted=0,
                            OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                            beat_ctl=np.nan, beat_spy=np.nan, beat_v2=np.nan, oos_rank=np.nan))
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


# ---------------------------------------------------------------- gate: rebuild == idea 135
NUMCOLS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "IS_MaxDD",
           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "m", "TO",
           "lad_Sharpe", "lad_CAGR", "lad_MaxDD", "lad_m", "lad_gross",
           "dSharpe", "dCAGR", "dMaxDD", "lad_CAGR_at_matchedDD"]
BOOLCOLS = ["pass4b", "floor_only", "IS_floor_only", "pass4a", "pass4a_v2", "pass4a_v2_IS",
            "D1", "D2", "D3", "D4", "D1_IS", "D1_OOS", "D1_raw", "lad_pass4b"]
KEY = ["panel", "book", "cost", "gross_mode", "arm"]


def gate_reproduce(G):
    say("\n" + "=" * 200)
    say("(0) REPRODUCTION GATE — this run's corpus against idea 135 _B2's COMMITTED grid "
        "(nothing new is read until this passes)")
    if not REF_GRID.exists():
        say(f"    !! reference grid missing: {REF_GRID.name}")
        raise SystemExit(2)
    R = pd.read_csv(REF_GRID)
    a = G.set_index(KEY).sort_index()
    b = R.set_index(KEY).sort_index()
    say(f"    rows: this run {len(a)}, committed {len(b)}")
    assert len(a) == len(b) == 1632, (len(a), len(b))
    assert (a.index == b.index).all(), "row identity differs"
    worst = {}
    for c in NUMCOLS:
        d = (a[c].astype(float) - b[c].astype(float)).abs()
        worst[c] = float(np.nanmax(d.values))
    say("    max |diff| by column: " + "  ".join(f"{k} {v:.2e}" for k, v in worst.items()))
    bad = {c: int((a[c].astype(bool) != b[c].astype(bool)).sum()) for c in BOOLCOLS}
    say("    boolean mismatches: " + "  ".join(f"{k} {v}" for k, v in bad.items()))
    ok = max(worst.values()) < 1e-9 and max(bad.values()) == 0
    say(f"    GATE {'PASS' if ok else 'FAIL'} — 1,632/1,632 rows, max|diff| "
        f"{max(worst.values()):.2e}, {sum(bad.values())} boolean mismatches")
    if not ok:
        raise SystemExit(3)
    # idea 135's published headline numbers, re-asserted on this run's own rebuild
    M = G[G.floor_only]
    say(f"    idea 135 headlines re-derived: members {len(M)} (published 531), "
        f"D1 {M.D1.mean():.1%} (12.2%), D2 {M.D2.mean():.1%} (19.8%), "
        f"D3-or-tie {(M.dMaxDD >= -TOL).mean():.1%} (77.4%), D4 {M.D4.mean():.1%} (58.9%)")
    # self-identity: the ungated control is its own matched-gross ladder point
    ctl = G[G.arm == "control"]
    say(f"    self-identity gate ({len(ctl)} control rows): max|dSharpe| "
        f"{ctl.dSharpe.abs().max():.2e}  max|dCAGR| {ctl.dCAGR.abs().max():.2e}  "
        f"max|dMaxDD| {ctl.dMaxDD.abs().max():.2e}")
    say(f"    SMALL panel exclusion asserted by idea 133 (0 floor-only of 612) and idea 136 "
        f"(0/180): this corpus is u56 + broad only, {len(G)} rows")
    return R


# ---------------------------------------------------------------- the deliverable
def cross(M):
    say("\n" + "=" * 200)
    say("(1) THE INTERSECTION — the queue's deliverable.  Members = 4b-defensive rows "
        "(floor-only), n = %d" % len(M))
    n = len(M)
    d1, d4 = M.D1.values, M.D4.values
    both = int((d1 & d4).sum())
    d1o = int((d1 & ~d4).sum())
    d4o = int((~d1 & d4).sum())
    nei = int((~d1 & ~d4).sum())
    say("\n    2x2, both conventions on the SAME rows:")
    say(f"      {'':22s} {'D4 pass (matched DD)':>22s} {'D4 fail':>10s} {'total':>8s}")
    say(f"      {'D1 pass (matched gross)':22s} {both:>22d} {d1o:>10d} {both + d1o:>8d}")
    say(f"      {'D1 fail':22s} {d4o:>22d} {nei:>10d} {d4o + nei:>8d}")
    say(f"      {'total':22s} {both + d4o:>22d} {d1o + nei:>10d} {n:>8d}")
    say(f"\n    BOTH  {pct(both, n)}      EITHER {pct(both + d1o + d4o, n)}      "
        f"NEITHER {pct(nei, n)}")
    say(f"    D1 (matched gross) {pct(int(d1.sum()), n)}      "
        f"D4 (matched drawdown) {pct(int(d4.sum()), n)}      ratio "
        f"{(d4.sum() / d1.sum() if d1.sum() else np.nan):.2f}x")
    say(f"    NESTING: of the {int(d1.sum())} D1 survivors, {both} ({both / max(d1.sum(), 1):.1%})"
        f" also clear D4 — D1 is {'' if d1o == 0 else 'NOT '}a subset of D4 "
        f"({d1o} exceptions)")
    und = int((~M.D4_defined).sum())
    say(f"    D4 UNDEFINED (arm MaxDD outside its own ladder's range): {pct(und, n)} — these are "
        f"scored as D4 fail above; on defined rows only, D4 = "
        f"{pct(int(M[M.D4_defined].D4.sum()), int(M.D4_defined.sum()))}")
    phi = np.nan
    if (both + d1o) and (both + d4o) and (d4o + nei) and (d1o + nei):
        phi = (both * nei - d1o * d4o) / np.sqrt(float((both + d1o) * (both + d4o) *
                                                       (d4o + nei) * (d1o + nei)))
    say(f"    phi(D1, D4) = {phi:.4f}   (0 = the two conventions are independent tests of the "
        f"same rows)")
    exp_indep = (d1.mean() * d4.mean()) * n
    say(f"    BOTH under independence would be {exp_indep:.1f} rows ({d1.mean() * d4.mean():.1%});"
        f" observed {both}")
    return dict(n=n, both=both, d1_only=d1o, d4_only=d4o, neither=nei, phi=phi)


def gap_decomposition(M):
    say("\n" + "=" * 200)
    say("(2) IS THE CONVENTION GAP ONE BOOK, ONE ARM KIND, OR UNIFORM?")
    say("    The gap is the set of rows the drawdown convention admits and the gross convention "
        "does not (D4 & ~D1).  For each factor: the member count, both rates, the gap in pp and "
        "the share of ALL gap rows the level carries.")
    gaprows = M.D4 & ~M.D1
    tot_gap = int(gaprows.sum())
    tabs = {}
    for fac in ["panel", "book", "kind", "cost", "gross_mode"]:
        rows = []
        for lvl, g in M.groupby(fac):
            rows.append(dict(level=lvl, n=len(g), D1=g.D1.mean(), D4=g.D4.mean(),
                             BOTH=(g.D1 & g.D4).mean(), gap_pp=100 * (g.D4.mean() - g.D1.mean()),
                             gap_rows=int((g.D4 & ~g.D1).sum()),
                             share_of_gap=(int((g.D4 & ~g.D1).sum()) / tot_gap
                                           if tot_gap else np.nan),
                             share_of_members=len(g) / len(M)))
        T = pd.DataFrame(rows).sort_values("gap_pp", ascending=False)
        T["lift"] = T.share_of_gap / T.share_of_members
        tabs[fac] = T
        say(f"\n    by {fac.upper()} (all levels reported):")
        say(T.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"\n    TOTAL gap rows (D4 & ~D1): {pct(tot_gap, len(M))}")
    say("    UNIFORMITY TEST — the gap is 'one book' or 'one arm kind' only if deleting that "
        "level collapses it.  Leave-one-level-out on the pooled gap rate:")
    base_gap = 100 * (M.D4.mean() - M.D1.mean())
    for fac in ["book", "kind", "panel", "gross_mode", "cost"]:
        outs = []
        for lvl, g in M.groupby(fac):
            rest = M[M[fac] != lvl]
            outs.append((lvl, 100 * (rest.D4.mean() - rest.D1.mean())))
        outs.sort(key=lambda t: t[1])
        say(f"      drop one {fac:11s}: pooled gap {base_gap:.1f} pp -> range "
            f"[{outs[0][1]:.1f} ({outs[0][0]}), {outs[-1][1]:.1f} ({outs[-1][0]})]  "
            f"| worst single deletion removes {base_gap - outs[0][1]:.1f} pp of it")
    say("    Per-level gap SIGN: a uniform gap has the same sign everywhere.")
    for fac in ["book", "kind", "panel", "gross_mode", "cost"]:
        T = tabs[fac]
        say(f"      {fac:11s}: {int((T.gap_pp > 0).sum())}/{len(T)} levels positive, "
            f"min {T.gap_pp.min():.1f} pp, max {T.gap_pp.max():.1f} pp, "
            f"spread {T.gap_pp.max() - T.gap_pp.min():.1f} pp")
    return tabs, tot_gap


def mechanism(M):
    say("\n" + "=" * 200)
    say("(3) MECHANISM — the two conventions pick DIFFERENT points of the same ladder")
    say("    Matched GROSS pins the control's mean exposure to the arm's (lad_m).  Matched "
        "DRAWDOWN pins the control's MaxDD to the arm's (lad_m_at_matchedDD).  If the arms are "
        "systematically shallower than their matched-gross control, the drawdown convention "
        "must de-gross the control further, which costs it CAGR — and that, not any property "
        "of the instrument, is what admits the extra rows.")
    d = M.dropna(subset=["lad_m_at_matchedDD"])
    say(f"    rows with both multipliers defined: {len(d)} of {len(M)}")
    say(f"    mean ladder m at matched GROSS    {d.lad_m.mean():.4f}")
    say(f"    mean ladder m at matched DRAWDOWN {d.lad_m_at_matchedDD.mean():.4f}   "
        f"(difference {d.lad_m_at_matchedDD.mean() - d.lad_m.mean():+.4f})")
    say(f"    the control is de-grossed further under the DD convention in "
        f"{pct(int((d.lad_m_at_matchedDD < d.lad_m - 1e-9).sum()), len(d))} of rows")
    say(f"    mean dMaxDD (arm shallower than its matched-gross control, pp) "
        f"{100 * M.dMaxDD.mean():+.2f}   mean dCAGR {100 * M.dCAGR.mean():+.2f} pp   "
        f"mean dSharpe {M.dSharpe.mean():+.4f}")
    g = d[d.D4 & ~d.D1]
    o = d[d.D1 & d.D4]
    say(f"    gap rows (D4 & ~D1, n={len(g)}): mean m_DD - m_gross "
        f"{(g.lad_m_at_matchedDD - g.lad_m).mean():+.4f}, mean dSharpe {g.dSharpe.mean():+.4f}, "
        f"mean dMaxDD {100 * g.dMaxDD.mean():+.2f} pp")
    say(f"    BOTH rows            (n={len(o)}): mean m_DD - m_gross "
        f"{(o.lad_m_at_matchedDD - o.lad_m).mean():+.4f}, mean dSharpe {o.dSharpe.mean():+.4f}, "
        f"mean dMaxDD {100 * o.dMaxDD.mean():+.2f} pp")
    say("    MATERIALITY of the intersection (how far past the bar the survivors sit):")
    for lab, s in [("dSharpe (matched gross)", o.dSharpe),
                   ("dCAGR at matched DD, pp", o.dCAGR_matchedDD)]:
        if len(s):
            say(f"      BOTH rows {lab:26s}: median {s.median():+.4f}  "
                f"max {s.max():+.4f}  >0.01 {int((s > 0.01).sum())}  >0.05 "
                f"{int((s > 0.05).sum())}  >0.10 {int((s > 0.10).sum())}")


def keep_paths(G, SPYREF):
    say("\n" + "=" * 200)
    say("(4) BOTH KEEP PATHS on all %d rows" % len(G))
    say(f"    4a vs the LIVE book (RULES v2): {pct(int(G.pass4a_v2.sum()), len(G))}   "
        f"(vs RULES v1, for continuity: {pct(int(G.pass4a.sum()), len(G))})")
    say(f"    4b vs SPY: {pct(int(G.pass4b.sum()), len(G))}")
    say(f"    rows passing BOTH 4a(v2) and 4b: {int((G.pass4a_v2 & G.pass4b).sum())}")
    if G.pass4a_v2.any():
        A = G[G.pass4a_v2].sort_values("Sharpe", ascending=False)
        say("    4a(v2) rows, best 8 by Sharpe:")
        say(A.head(8)[["panel", "book", "arm", "cost", "gross_mode", "CAGR", "Sharpe", "MaxDD",
                       "H1", "H2", "OOS_Sharpe", "D1", "D4", "BOTH"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    if G.pass4b.any():
        Bf = G[G.pass4b]
        say(f"    of the {len(Bf)} 4b passers: D1 {pct(int(Bf.D1.sum()), len(Bf))}, "
            f"D4 {pct(int(Bf.D4.sum()), len(Bf))}, BOTH {pct(int(Bf.BOTH.sum()), len(Bf))}")
        say("    4b passers, best 8 by Sharpe:")
        say(Bf.sort_values("Sharpe", ascending=False).head(8)
            [["panel", "book", "arm", "cost", "gross_mode", "CAGR", "Sharpe", "MaxDD", "H1",
              "H2", "OOS_Sharpe", "D1", "D4", "BOTH"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for p, s in SPYREF.items():
        say(f"    SPY {p}: full {s['scagr']:.2%} / MaxDD {s['sdd']:.2%} / halves "
            f"{s['s1']:.3f}/{s['s2']:.3f} | OOS {s['oos_cagr']:.2%} / {s['oos_sharpe']:.3f} / "
            f"{s['oos_dd']:.2%}")


def rule8(W):
    say("\n" + "=" * 200)
    say("(5) RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 alone, 2017-2026 read once")
    say("    12 cells (2 panels x 2 cost rungs x 3 gross modes); a cell pools all 8 books.")
    rows = []
    for s, g in W.groupby("sel", sort=False):
        pk = g.dropna(subset=["OOS_Sharpe"])
        rows.append(dict(sel=s, cells_with_pick=len(pk), mean_admitted=g.n_admitted.mean(),
                         OOS_Sharpe=pk.OOS_Sharpe.mean(), OOS_CAGR=pk.OOS_CAGR.mean(),
                         OOS_MaxDD=pk.OOS_MaxDD.mean(),
                         beats_SPY=int(pk.beat_spy.sum()), beats_v2=int(pk.beat_v2.sum()),
                         beats_ctl=int(pk.beat_ctl.sum()),
                         mean_oos_rank=pk.oos_rank.mean()))
    T = pd.DataFrame(rows)
    say(T.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"\n    SPY OOS Sharpe {W.spy_OOS_Sharpe.mean():.3f} (CAGR {W.spy_OOS_CAGR.mean():.2%}, "
        f"MaxDD {W.spy_OOS_MaxDD.mean():.2%}); RULES v2 OOS Sharpe by panel: " +
        ", ".join(f"{p} {g.v2_OOS_Sharpe.mean():.3f}" for p, g in W.groupby("panel")))
    say("\n    PAIRED against idea 133's class selector S3, on the cells where BOTH pick "
        "(this is the test that matters: does adding a convention change a decision?):")
    piv = W.pivot_table(index=["panel", "cost", "gross_mode"], columns="sel",
                        values=["OOS_Sharpe", "pick"], aggfunc="first")
    for s in ["S5", "S8", "S9", "S6", "S10"]:
        a = piv[("OOS_Sharpe", "S3")]
        b = piv[("OOS_Sharpe", s)]
        pa, pb = piv[("pick", "S3")], piv[("pick", s)]
        ok = a.notna() & b.notna()
        moved = int((pa[ok] != pb[ok]).sum())
        better = int((b[ok] > a[ok] + 1e-12).sum())
        worse = int((b[ok] < a[ok] - 1e-12).sum())
        abst = int((a.notna() & b.isna()).sum())
        say(f"      {s:4s} vs S3: both pick in {int(ok.sum()):2d}/12 cells | picks moved "
            f"{moved:2d} | mean dOOS Sharpe {(b[ok] - a[ok]).mean():+.4f} | better {better} "
            f"worse {worse} tied {int(ok.sum()) - better - worse} | abstains where S3 picks "
            f"{abst}")
    say("\n    per-cell detail:")
    say(W[["sel", "panel", "cost", "gross_mode", "n_admitted", "pick", "OOS_CAGR", "OOS_Sharpe",
           "OOS_MaxDD", "beat_spy", "beat_v2"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return T


def main():
    say("=" * 200)
    say("IDEA 397 — is the `4b-defensive` class empty under BOTH conventions?")
    say("corpus: 2 panels x 8 books x 17 arms x 2 cost rungs x 3 gross modes = 1,632 rows, "
        "each priced against its own book's matched-GROSS ladder point (D1) AND its own book's "
        "matched-DRAWDOWN ladder point (D4)")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, 4b bars phi={PHI0} delta={DELTA0}, "
        f"tolerance {TOL:g}")
    say("tuned: n in [5,10,20,40] (ranked size), f in [0.25,0.50] (sleeve fraction). All grid "
        "points reported.  D1/D4 are conventions, not dials.")
    say("H_empty: intersection <= 5% of members -> DELETE the class.  H_nested: D1 survivors "
        "are a subset of D4 and the intersection is ~12% -> AMEND with a stated convention.")
    say("=" * 200)

    G, W, SPYREF = build()
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    gate_reproduce(G)

    M = G[G.floor_only].copy()
    M.to_csv(OUT / f"{STEM}.members.csv", index=False)
    stats = cross(M)
    tabs, tot_gap = gap_decomposition(M)
    pd.concat([t.assign(factor=f) for f, t in tabs.items()]).to_csv(
        OUT / f"{STEM}.gap_by_factor.csv", index=False)
    mechanism(M)
    keep_paths(G, SPYREF)
    T = rule8(W)
    T.to_csv(OUT / f"{STEM}.selectors.csv", index=False)

    say("\n" + "=" * 200)
    say("(6) VERDICT")
    rate = stats["both"] / stats["n"]
    say(f"    BOTH = {stats['both']} of {stats['n']} members ({rate:.1%}).")
    if rate <= 0.05:
        say("    H_empty HOLDS: the intersection is near-empty. The queue's stated consequence "
            "is that the class should be DELETED, not amended.")
    else:
        say("    H_empty FAILS on its own 5% bar: the intersection is not empty.")
    if stats["d1_only"] == 0:
        say("    H_nested HOLDS on nesting: every matched-GROSS survivor also clears the "
            "matched-DRAWDOWN bar.")
    else:
        say(f"    H_nested FAILS on nesting: {stats['d1_only']} matched-GROSS survivors fail the "
            "matched-DRAWDOWN bar, so the conventions are not ordered by strictness.")
    say("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
