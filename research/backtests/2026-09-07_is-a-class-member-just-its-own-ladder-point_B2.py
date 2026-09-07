#!/usr/bin/env python3
"""QUEUE idea 135 — is-a-class-member-just-its-own-ladder-point  (research sprint lane B, 2026-09-07)

QUESTION (pre-registered, from QUEUE.md idea 135, verbatim)
    "idea 133 measured that forcing 0.53 mean gross moves TOP20 from 1 class member to 34 and
     TOP40 from 10 to 52, i.e. de-grossing manufactures membership, while V1u/TOP5 join at no
     gross level and the sleeve books at every one.  A mean-gross column may not be enough to
     separate them.  Test the explicit control: price every class member against its OWN
     book's static-gross ladder point at matched mean gross, and propose that a `4b-defensive`
     row must beat that point to be recorded at all.  Bears on idea 131."

    `4b-defensive` (idea 129's proposed reporting class): an arm that clears 4b's two
    halves-Sharpe bars, its OOS-Sharpe bar and its MaxDD cap, and fails ONLY the CAGR floor.

THE CONTROL THIS RUN ADDS
    For EVERY row of idea 133's u56/broad corpus (not only the members), the arm is priced
    against ITS OWN BOOK, ungated, with no overlay, held at a STATIC gross multiplier m solved
    so that the control's MEAN GROSS over the evaluation slice equals the arm's own achieved
    mean gross.  That is the arm's "own static-gross ladder point": the same book, the same
    panel, the same cost, the same average exposure, and no instrument at all.

TWO FALSIFIABLE HYPOTHESES, both written down before any number was read
    H_ladder (the queue's worry, and idea 133's own caveat) — a `4b-defensive` member is its
             own ladder point in disguise.  Prediction: most members FAIL to beat the matched
             control, and the failure rate is worst in the m53 mode, where gross was forced
             down by the corpus itself rather than by the instrument.
    H_real   — membership carries information beyond exposure.  Prediction: most members beat
             the matched control on the axis the class is about (higher Sharpe at no worse
             drawdown), and the m53 mode is no worse than native.
    The two make opposite predictions on the same table, so the run cannot be steered.

DECISION RULES (all reported at every grid point; D1 is the primary, and is the one the
queue's proposal would write into PROTOCOL)
    D1  dominates      Sharpe > ladder's AND |MaxDD| <= ladder's        (the proposal)
    D2  Sharpe-only    Sharpe > ladder's
    D3  MaxDD-only     |MaxDD| < ladder's
    All three are evaluated at a tolerance of 1e-9 rather than as a bare `>`, and this is a
    finding about the proposal, not a convenience: the ungated `control` arm IS its own matched
    ladder point, so a bare `>` lets 8 rows beat THEMSELVES by 2.2e-16 and enter the record.  A
    per-row dominance bar has to carry an explicit tolerance or it admits its own control.  The
    bare form is kept as `D1_raw` and the gap between them is reported in section (2f).
    D4  matched-DD     idea 94's convention instead of matched gross: interpolate the book's
                       own static-gross ladder (m = 0.10..1.00 step 0.05) to the arm's OWN
                       MaxDD and ask whether the arm's CAGR beats the ladder's there.  This is
                       a DIFFERENT control (matched drawdown, not matched exposure) and is
                       reported beside D1 so the proposal is not judged on one convention.
    D1/D2/D3/D4 are CONVENTIONS, not tuned dials: all four are reported for all 1,632 rows.

TUNED PARAMETERS — exactly two, both inherited from idea 133 and both fully reported
    n  ranked book size    in {5, 10, 20, 40}
    f  sleeve fraction     in {0.25, 0.50}
    Nothing else is tuned.  Books, arms, gates, dials, cadence, execution lag, cost rungs,
    window boundaries, gross-matching targets and 4b's coefficients (phi=0.70, delta=0.60) are
    inherited unchanged from ideas 94/129/133.  The ladder grid is idea 94's published LADDER.

CORPUS
    panels  u56 (56 names), broad (136).  The SMALL panel is EXCLUDED and the exclusion is a
            finding, not a convenience: idea 133's own grid has 0 floor-only rows on the small
            panel out of 612, and idea 136 (2026-09-07, cloud) confirms 0/180 defensive arms
            there.  There is no class member on that panel to price.  Asserted below.
    books   V1u, TOP5, TOP10, TOP20, TOP40, EWall, SLV25, SLV50  (8)
    arms    idea 94's 17: control, 5 gates x {dg, rw}, 2 stops, 2 DD controls, 2 entry budgets
    costs   10, 25 bps      gross modes  native, m53, m75
    => 2 x 8 x 17 x 2 x 3 = 1,632 arm rows, every one written to .grid.csv with its matched
       ladder point beside it.

HARNESS
    Idea 94's simulator (`H.run`) and idea 133's book/gross machinery (`C.book_targets`,
    `C.run_at_gross`, `C.panel`, `C.bars_win`, `C.margins_at`, `C.fails`) are IMPORTED, not
    re-implemented.  The 1,632 member rows are asserted to reproduce idea 133's published grid
    exactly before anything new is read, and the ungated `control` arm is asserted to be its
    OWN matched ladder point to machine precision (the control must price at exactly zero).

WALK-FORWARD (PROTOCOL rule 8; six selectors fixed in writing before any OOS number was read)
    Parameters are chosen on 2009-2016 alone; 2017-2026 is read once.  A cell pools all books
    within a (panel, cost, gross mode) triple, as in idea 133, because "which construction gets
    picked" is the question.
      S0  no screen        argmax IS Sharpe over every arm in the cell (idea 151's do-nothing)
      S1  IS 4b-admissible argmax IS Sharpe among arms clearing 4b's IS bars incl. the floor
      S3  IS floor-only    idea 133's class selector: argmax IS Sharpe among IS-floor-only arms
      S5  THE PROPOSAL     S3 restricted to arms that beat their own IS-window ladder point (D1
                           computed on 2009-2016 alone)
      S6  ladder screen    D1 (IS window) alone, with no class restriction — isolates which of
                           the proposal's two clauses does the work
      S7  the 4a path      argmax IS Sharpe among arms clearing 4a against the LIVE book on
                           2009-2016 alone.  Not part of idea 135's question; it is the honest
                           out-of-sample read on this run's one by-product (see section 7b).
    Every pick is evaluated untouched on 2017-2026 against SPY, the LIVE baseline RULES v2,
    RULES v1 and the cell's own ungated EWall control.

BOTH KEEP PATHS on every one of the 1,632 rows
    4a  halves Sharpe > the LIVE book (RULES v2, live since 2026-09-06) in BOTH halves and
        MaxDD no worse.  Also reported against RULES v1 for continuity with the pre-v2 record.
    4b  the five bars vs SPY (H1, H2, OOS, MaxDD cap 0.60x, CAGR floor 0.70x).

CAVEATS carried, not buried
    - Survivorship (idea 54): current-constituent panels.  It inflates the ungated, fully
      invested LADDER control most, so the control is if anything a HARD test — a member that
      beats it here would beat it by more on a survivorship-free panel.  Stated in that
      direction because it runs against this run's H_ladder finding, not for it.
    - Idea 128: the IS window (SPY MaxDD -22.1%) is shallower than the OOS window (-33.7%), so
      every IS-window drawdown comparison, D1's included, is measured on a ruler that cannot
      express deep drawdowns.  This affects S5 exactly as it affects S1/S3.
    - Gross matching changes CAGR and MaxDD together; a matched-gross ladder point is NOT the
      same instrument as the m=1 book and is never quoted as one.
    - MaxDD is one number off one path; D1's tie-break on |MaxDD| inherits that fragility.
      D2 and D3 are reported precisely so the reader can see how much of D1 rides on it.
    - Idea 38: u56/broad carry the calendar-day index; it applies identically to an arm and to
      its own matched control and cancels in every comparison this run makes.
    - The MEMBER rows keep idea 133's two-step Newton gross solve (so its grid reproduces
      exactly); the LADDER control's solve is iterated to convergence instead, because a
      two-step control prices the ungated `control` arm at 1.3e-07 of Sharpe against itself
      rather than 0.  Achieved gross error is reported for every row and gated below 1e-6.

RUN
    python research/backtests/2026-09-07_is-a-class-member-just-its-own-ladder-point_B2.py
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

STEM = "2026-09-07_is-a-class-member-just-its-own-ladder-point_B2"
OUT = ROOT / "research" / "backtests"


def _imp(name, fn):
    spec = importlib.util.spec_from_file_location(name, OUT / fn)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _imp("i133", "2026-09-05_defensive-class-census_B.py")     # books, gross matching, bars
H = C.H                                                        # idea 94's simulator + arms

FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad"]                                      # small has 0 members (asserted)
BOOKS = C.BOOKS
GROSS_LEVELS = C.GROSS_LEVELS
PHI0, DELTA0 = C.PHI0, C.DELTA0
LADDER = H.LADDER                                              # 0.10 .. 1.00 step 0.05
TOL = 1e-9                                                     # see the D* definitions below

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def pct(k, n):
    return f"{k}/{n} = {(k / n if n else np.nan):.1%}"


# ---------------------------------------------------------------- the matched ladder point
_WCACHE, _LADCACHE, _CTLCACHE = {}, {}, {}


def base_book(pname, px, book):
    """The book, ungated, no overlay — the ladder's shape."""
    k = (pname, book)
    if k not in _WCACHE:
        _WCACHE[k] = C.book_targets(px, book)
    return _WCACHE[k]


def ladder_point(pname, px, book, cost, target_gross, start):
    """Same book, no instrument, held at the static gross multiplier m whose MEAN gross over
    the evaluation slice equals `target_gross`.

    Idea 133 used TWO Newton steps to hit its 0.53 / 0.75 targets, which leaves a ~2e-5
    residual in achieved gross.  That residual is harmless for a corpus row but NOT for this
    run's control: the ungated `control` arm must be its OWN matched ladder point exactly, and
    a two-step solve prices it at 1.3e-07 of Sharpe instead of 0.  The solve is therefore
    iterated to convergence (|g - target| <= 1e-12, at most 8 steps) so the self-identity gate
    below passes at machine precision and no comparison in this run rides on solver slop.
    The MEMBER rows still use idea 133's two-step solve unchanged, so its grid reproduces.
    Cached on the rounded target so the 1,632 rows cost ~19 solves per (panel, book, cost)."""
    key = (pname, book, cost, round(float(target_gross), 8))
    if key in _CTLCACHE:
        return _CTLCACHE[key]
    W = base_book(pname, px, book)
    m = 1.0
    res = H.run(px, W, m=m, bps=cost)
    g = float(res["gross"].loc[start:].mean())
    for _ in range(8):
        if g <= 1e-9 or abs(g - target_gross) <= 1e-12:
            break
        m = float(np.clip(m * target_gross / g, 0.02, 5.0))
        res = H.run(px, W, m=m, bps=cost)
        g = float(res["gross"].loc[start:].mean())
    out = (res["r"].loc[start:], m, g)
    _CTLCACHE[key] = out
    return out


def static_ladder(pname, px, book, cost, start):
    """idea 94's static-gross ladder for this book: m over LADDER, full-sample CAGR/MaxDD.
    Used only for the matched-DRAWDOWN convention D4."""
    key = (pname, book, cost)
    if key in _LADCACHE:
        return _LADCACHE[key]
    W = base_book(pname, px, book)
    rows = []
    for m in LADDER:
        r = H.run(px, W, m=float(m), bps=cost)["r"].loc[start:]
        mm = metrics(r)
        rows.append(dict(m=float(m), CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"]))
    L = pd.DataFrame(rows)
    _LADCACHE[key] = L
    return L


def win_metrics(r, which):
    m = metrics(H.window(r, which))
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


# ---------------------------------------------------------------- one (panel, book, cost, gross)
def do_cell(pname, px, spy, book, cost, glabel, gtarget, bfull, bIS, v1_net, v2_net, start):
    rows, rets, ctl_rets = [], {}, {}
    for arm, kind, kw, (gate, conv) in H.arm_specs():
        W = C.book_targets(px, book, gate, conv)
        res, m, gach = C.run_at_gross(px, W, kw, cost, gtarget, start)
        r = res["r"].loc[start:]
        rets[arm] = r

        # ---- the control the queue asks for: this book's own static-gross ladder point
        lr, lm, lg = ladder_point(pname, px, book, cost, gach, start)
        ctl_rets[arm] = lr

        mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
        lmm, lmi, lmo = metrics(lr), metrics(H.window(lr, "IS")), metrics(H.window(lr, "OOS"))
        mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
        mgi = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
        lg_full = C.margins_at(lr, bfull, PHI0, DELTA0, "full")
        f = C.fails(mg)
        lf = C.fails(lg_full)
        h1, h2 = H.halves(r)
        lh1, lh2 = H.halves(lr)

        # ---- decision rules.  TOL exists because a bare `>` is not a well-posed bar here:
        # the ungated `control` arm IS its own ladder point, and floating point lets it beat
        # itself by 2.2e-16.  D*_raw keeps the bare form so the artefact can be counted.
        dS, dDD = mm["Sharpe"] - lmm["Sharpe"], abs(lmm["MaxDD"]) - abs(mm["MaxDD"])
        d1_raw = bool(dS > 0 and dDD >= 0)
        d1 = bool(dS > TOL and dDD >= -TOL)
        d2 = bool(dS > TOL)
        d3 = bool(dDD > TOL)
        dSi = mi["Sharpe"] - lmi["Sharpe"]
        dSo = mo["Sharpe"] - lmo["Sharpe"]
        d1_is = bool(dSi > TOL and abs(lmi["MaxDD"]) - abs(mi["MaxDD"]) >= -TOL)
        d1_oos = bool(dSo > TOL and abs(lmo["MaxDD"]) - abs(mo["MaxDD"]) >= -TOL)

        # ---- D4: idea 94's matched-DRAWDOWN convention on the same book's ladder
        L = static_ladder(pname, px, book, cost, start)
        cagr_md = H.matched_dd(L, mm["MaxDD"])
        d4 = bool(np.isfinite(cagr_md) and mm["CAGR"] * 100.0 - cagr_md > TOL)

        rows.append(dict(
            panel=pname, book=book, cost=cost, gross_mode=glabel, arm=arm, kind=kind,
            m=m, gross=gach,
            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
            IS_m_H1=mgi["H1"], IS_m_H2=mgi["H2"], IS_m_DD=mgi["DD"], IS_m_CAGR=mgi["CAGR"],
            pass4b=(len(f) == 0), fail4b=",".join(f) or "-", n_fail=len(f),
            floor_only=(f == ["CAGR"]),
            IS_floor_only=(C.fails(mgi) == ["CAGR"]),
            IS_admit_phi70=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
            IS_admit_phi00=all(mgi[k] > 0 for k in ("H1", "H2", "DD")),
            pass4a=H.pass4a(r, v1_net), pass4a_v2=H.pass4a(r, v2_net),
            pass4a_v2_IS=H.pass4a(H.window(r, "IS"), H.window(v2_net, "IS")),
            pass4a_v2_OOS=H.pass4a(H.window(r, "OOS"), H.window(v2_net, "OOS")),
            TO=float(res["to"].loc[start:].sum() / (len(r) / 252)),
            # ---- the matched ladder point
            lad_m=lm, lad_gross=lg, gross_err=abs(lg - gach),
            lad_CAGR=lmm["CAGR"], lad_Sharpe=lmm["Sharpe"], lad_MaxDD=lmm["MaxDD"],
            lad_H1=lh1, lad_H2=lh2, lad_OOS_Sharpe=lmo["Sharpe"],
            lad_IS_Sharpe=lmi["Sharpe"], lad_IS_MaxDD=lmi["MaxDD"],
            lad_OOS_CAGR=lmo["CAGR"], lad_OOS_MaxDD=lmo["MaxDD"],
            lad_pass4b=(len(lf) == 0), lad_floor_only=(lf == ["CAGR"]),
            lad_fail4b=",".join(lf) or "-",
            dSharpe=mm["Sharpe"] - lmm["Sharpe"], dCAGR=mm["CAGR"] - lmm["CAGR"],
            dMaxDD=abs(lmm["MaxDD"]) - abs(mm["MaxDD"]),      # >0 = arm is shallower
            dSharpe_IS=mi["Sharpe"] - lmi["Sharpe"], dSharpe_OOS=mo["Sharpe"] - lmo["Sharpe"],
            D1=d1, D2=d2, D3=d3, D4=d4, D1_IS=d1_is, D1_OOS=d1_oos, D1_raw=d1_raw,
            lad_CAGR_at_matchedDD=cagr_md,
            dCAGR_matchedDD=(mm["CAGR"] * 100.0 - cagr_md) if np.isfinite(cagr_md) else np.nan,
        ))
    return pd.DataFrame(rows), rets, ctl_rets


# ---------------------------------------------------------------- rule 8
def walk_forward(sub, RET, key, spy, v1_net, v2_net, ctl_ret):
    mc = metrics(H.window(ctl_ret, "OOS"))
    ms = metrics(spy.loc[OOS_START:])
    mv1 = metrics(H.window(v1_net, "OOS"))
    mv2 = metrics(H.window(v2_net, "OOS"))
    cand = {
        "S0": sub,
        "S1": sub[sub.IS_admit_phi70],
        "S3": sub[sub.IS_floor_only],
        "S5": sub[sub.IS_floor_only & sub.D1_IS],
        "S6": sub[sub.D1_IS],
        "S7": sub[sub.pass4a_v2_IS],          # the 4a path, chosen on the IS window alone
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


# ---------------------------------------------------------------- reproduction gate
def reproduce(px, start):
    say("\n" + "=" * 200)
    say("(0) REPRODUCTION — nothing new is read until these pass")
    W = C.book_targets(px, "EWall", "vol60", "dg")
    r = H.run(px, W, bps=10.0)["r"].loc[start:]
    m = metrics(r)
    say(f"    (a) idea 94's EWall+vol60-dg u56@10bps: {m['CAGR']:.3%} / {m['Sharpe']:.3f} / "
        f"{m['MaxDD']:.3%}   published 11.6% / 1.133 / -16.9%   "
        f"{'PASS' if abs(m['Sharpe'] - 1.133) < 5e-4 else 'FAIL'}")
    assert abs(m["Sharpe"] - 1.133) < 5e-4

    ref = pd.read_csv(OUT / "2026-09-05_defensive-class-census_B.grid.csv")
    sm = ref[ref.panel == "small"]
    say(f"    (b) idea 133's SMALL panel: {len(sm)} rows, floor-only "
        f"{int(sm.floor_only.sum())}  -> the small panel is excluded because it has no class "
        f"member to price   {'PASS' if int(sm.floor_only.sum()) == 0 else 'FAIL'}")
    assert int(sm.floor_only.sum()) == 0
    return ref


def reproduce_133(G, ref):
    say("\n" + "=" * 200)
    say("(0c) REPRODUCTION OF IDEA 133's GRID — every one of this run's 1,632 member rows is a "
        "row of its 2,244")
    k = ["panel", "book", "cost", "gross_mode", "arm"]
    j = ref.merge(G, on=k, suffixes=("_133", "_135"))
    say(f"    matched {len(j)} of {len(G)} rows on {k}")
    worst = 0.0
    for col in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "IS_Sharpe", "gross", "m"):
        d = float((j[f"{col}_133"] - j[f"{col}_135"]).abs().max())
        worst = max(worst, d)
        say(f"      max|d {col}| = {d:.3e}")
    nf = int((j["floor_only_133"] != j["floor_only_135"]).sum())
    n4b = int((j["pass4b_133"] != j["pass4b_135"]).sum())
    n4a = int((j["pass4a_133"] != j["pass4a_135"]).sum())
    say(f"      floor_only mismatches {nf}/{len(j)}   pass4b {n4b}/{len(j)}   "
        f"pass4a(v1) {n4a}/{len(j)}   max|diff| {worst:.3e}   "
        f"{'PASS' if nf == 0 and n4b == 0 and n4a == 0 and worst < 1e-9 else 'FAIL'}")
    assert nf == 0 and n4b == 0 and n4a == 0 and worst < 1e-9 and len(j) == len(G)


# ---------------------------------------------------------------- main
def main():
    say("=" * 200)
    say("IDEA 135 — is a `4b-defensive` class member just its own book's static-gross ladder "
        "point?")
    say(f"corpus: panels {PANELS} x books {BOOKS} x 17 arms x costs {COSTS} bps x gross "
        f"{list(GROSS_LEVELS)}  =  1,632 rows, each priced against its OWN matched-gross "
        f"ladder point")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, 4b bars phi={PHI0} delta={DELTA0}")
    say("tuned: n in [5,10,20,40] (ranked size), f in [0.25,0.50] (sleeve fraction). "
        "All grid points reported.  D1..D4 are conventions, not dials.")
    say("=" * 200)

    px0, spy0, _ = C.panel("u56")
    ref = reproduce(px0, px0.index[260])

    GR, WF = [], []
    SPYREF = {}
    for pname in PANELS:
        px, spy, desc = C.panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        mo = metrics(spy.loc[OOS_START:])
        SPYREF[pname] = dict(desc=desc, **bfull, oos_cagr=mo["CAGR"], oos_dd=mo["MaxDD"])
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY full CAGR {bfull['scagr']:.2%} MaxDD {bfull['sdd']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} OOS Sharpe {bfull['soos']:.3f} | bars: CAGR "
            f">= {PHI0 * bfull['scagr']:.2%}/yr, MaxDD >= {-DELTA0 * abs(bfull['sdd']):.2%}")

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
                ctl_of = {}
                for book in BOOKS:
                    D, rets, ctls = do_cell(pname, px, spy, book, c, glabel, gtarget,
                                            bfull, bIS, v1[c], v2[c], start)
                    cellrows.append(D)
                    for a, r in rets.items():
                        RET[(book, a)] = r
                    for a, r in ctls.items():
                        ctl_of[(book, a)] = r
                CD = pd.concat(cellrows, ignore_index=True)
                GR.append(CD)
                wf = walk_forward(CD, RET, (pname, c, glabel), spy, v1[c], v2[c],
                                  RET[("EWall", "control")])
                WF.append(wf)
                fo = CD[CD.floor_only]
                say(f"    {pname:5s} gross={glabel:6s} {int(c):2d}bps: {len(CD):3d} arms | "
                    f"4b {int(CD.pass4b.sum()):3d} | 4a(v2) {int(CD.pass4a_v2.sum()):3d} | "
                    f"floor-only {len(fo):3d} | of those D1 {int(fo.D1.sum()):3d} | "
                    f"mean gross-match err {CD.gross_err.mean():.2e}")

    G = pd.concat(GR, ignore_index=True)
    W = pd.concat(WF, ignore_index=True)
    G["constr"] = G.apply(C.construction, axis=1)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    reproduce_133(G, ref)

    # ---------------------------------------------------------------- (0d) control identity
    say("\n" + "=" * 200)
    say("(0d) SELF-IDENTITY GATE — the ungated `control` arm IS its own ladder point, so it "
        "must price at exactly zero")
    ctl = G[G.arm == "control"]
    worst = float(ctl.dSharpe.abs().max()), float(ctl.dCAGR.abs().max()), float(ctl.dMaxDD.abs().max())
    say(f"    {len(ctl)} control rows: max|dSharpe| {worst[0]:.3e}  max|dCAGR| {worst[1]:.3e}  "
        f"max|dMaxDD| {worst[2]:.3e}   {'PASS' if max(worst) < 1e-10 else 'FAIL'}")
    assert max(worst) < 1e-10
    gerr = float(G.gross_err.max())
    say(f"    matched-gross solve: max achieved-gross error over all {len(G)} rows = "
        f"{gerr:.3e}   {'PASS' if gerr < 1e-6 else 'FAIL'}"
        f"   (cache granularity: targets are keyed to 1e-8)")
    assert gerr < 1e-6

    # ---------------------------------------------------------------- (1) the census recap
    say("\n" + "=" * 200)
    say("(1) THE CLASS AS IDEA 133 LEFT IT (u56 + broad only)")
    FO = G[G.floor_only]
    say(f"    rows {len(G)}   4b passes {int(G.pass4b.sum())}   4a passes vs RULES v2 "
        f"{int(G.pass4a_v2.sum())}   (vs RULES v1 {int(G.pass4a.sum())})   "
        f"`4b-defensive` members {len(FO)}")
    say("\n    members by book x gross mode:")
    say(pd.crosstab(FO.book, FO.gross_mode).to_string())
    say("\n    members by panel x cost:")
    say(pd.crosstab(FO.panel, FO.cost).to_string())

    # ---------------------------------------------------------------- (2) THE CONTROL
    say("\n" + "=" * 200)
    say("(2) THE CONTROL — every member priced against its OWN book's static-gross ladder "
        "point at matched mean gross")
    say("    D1 dominates (Sharpe > ladder AND |MaxDD| <= ladder)  ..  the queue's proposal")
    say("    D2 Sharpe > ladder      D3 |MaxDD| < ladder      D4 CAGR > ladder at matched "
        "DRAWDOWN (idea 94's convention)")
    n = len(FO)
    for d in ("D1", "D2", "D3", "D4"):
        say(f"    members passing {d}: {pct(int(FO[d].sum()), n)}")
    say(f"\n    ALL 1,632 rows for comparison (members and non-members alike):")
    for d in ("D1", "D2", "D3", "D4"):
        say(f"      all rows passing {d}: {pct(int(G[d].sum()), len(G))}   "
            f"non-members {pct(int(G[~G.floor_only][d].sum()), len(G) - n)}")

    say("\n    (2a) members passing D1, by gross mode  [H_ladder predicts m53 worst]:")
    t = FO.groupby("gross_mode").agg(members=("D1", "size"), D1=("D1", "sum"),
                                     D2=("D2", "sum"), D3=("D3", "sum"), D4=("D4", "sum"),
                                     mean_dSharpe=("dSharpe", "mean"),
                                     mean_dMaxDD_pp=("dMaxDD", lambda s: 100 * s.mean()))
    t["D1_rate"] = t.D1 / t.members
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n    (2b) members passing D1, by book:")
    t = FO.groupby("book").agg(members=("D1", "size"), D1=("D1", "sum"), D2=("D2", "sum"),
                               D3=("D3", "sum"), D4=("D4", "sum"),
                               mean_dSharpe=("dSharpe", "mean"))
    t["D1_rate"] = t.D1 / t.members
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n    (2c) members passing D1, by panel x cost:")
    t = FO.groupby(["panel", "cost"]).agg(members=("D1", "size"), D1=("D1", "sum"),
                                          D4=("D4", "sum"), mean_dSharpe=("dSharpe", "mean"))
    t["D1_rate"] = t.D1 / t.members
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n    (2d) members passing D1, by arm kind:")
    t = FO.groupby("kind").agg(members=("D1", "size"), D1=("D1", "sum"), D4=("D4", "sum"),
                               mean_dSharpe=("dSharpe", "mean"))
    t["D1_rate"] = t.D1 / t.members
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n    (2e) the two clauses of D1 separately, on members:")
    say(f"      Sharpe > ladder                {pct(int(FO.D2.sum()), n)}")
    say(f"      |MaxDD| <= ladder              {pct(int((FO.dMaxDD >= 0).sum()), n)}")
    say(f"      both (D1)                      {pct(int(FO.D1.sum()), n)}")
    say(f"      neither                        {pct(int((~FO.D2 & (FO.dMaxDD < 0)).sum()), n)}")
    say(f"      mean dSharpe {FO.dSharpe.mean():+.4f}   median {FO.dSharpe.median():+.4f}   "
        f"mean dMaxDD {100 * FO.dMaxDD.mean():+.2f}pp   mean dCAGR "
        f"{100 * FO.dCAGR.mean():+.2f}pp")

    say("\n    (2f) THE TOLERANCE, and how much of the survival is numerical noise:")
    noise = G[G.D1_raw & ~G.D1]
    say(f"      rows passing the BARE `>` form but not at tol {TOL:g}: {len(noise)} of "
        f"{int(G.D1_raw.sum())}  — all of them ungated `control` arms beating THEMSELVES "
        f"(max dSharpe {noise.dSharpe.abs().max():.2e})" if len(noise) else
        f"      rows passing the bare `>` but not at tol {TOL:g}: 0")
    say(f"      members: D1_raw {int(FO.D1_raw.sum())} -> D1 {int(FO.D1.sum())}")
    for thr in (0.01, 0.05, 0.10):
        say(f"      members beating their ladder point by more than {thr:.2f} of Sharpe "
            f"(and no worse on MaxDD): {pct(int((FO.D1 & (FO.dSharpe > thr)).sum()), n)}")

    # ---------------------------------------------------------------- (3) is the ladder point itself in the class?
    say("\n" + "=" * 200)
    say("(3) WHAT THE MATCHED LADDER POINT ITSELF IS — if the ladder point is already "
        "`4b-defensive`, the member adds nothing but a name")
    say(f"    matched ladder point is itself floor-only:  {pct(int(FO.lad_floor_only.sum()), n)}")
    say(f"    matched ladder point passes 4b outright:    {pct(int(FO.lad_pass4b.sum()), n)}")
    say(f"    ladder point fails 4b on more bars than the member: "
        f"{pct(int((FO.lad_fail4b.str.count(',') > 0).sum()), n)}")
    say("\n    ladder-point status by gross mode:")
    say(pd.crosstab(FO.gross_mode, FO.lad_fail4b).to_string())

    # ---------------------------------------------------------------- (4) the proposal's bite
    say("\n" + "=" * 200)
    say("(4) THE PROPOSAL'S BITE — `a 4b-defensive row must beat its own ladder point to be "
        "recorded at all`")
    surv = FO[FO.D1]
    say(f"    class as recorded today: {n} rows.  Under the proposal: {len(surv)} rows "
        f"({len(surv) / n:.1%}).  Delisted: {n - len(surv)}.")
    say("\n    surviving members by book x gross mode:")
    say((pd.crosstab(surv.book, surv.gross_mode).to_string() if len(surv) else "    (none)"))
    if len(surv):
        say("\n    the survivors (all of them, sorted by dSharpe):")
        cols = ["panel", "book", "arm", "cost", "gross_mode", "gross", "CAGR", "Sharpe",
                "MaxDD", "H1", "H2", "OOS_Sharpe", "lad_Sharpe", "lad_MaxDD", "dSharpe",
                "dMaxDD", "D4", "TO"]
        say(surv.sort_values("dSharpe", ascending=False)[cols].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n    idea 133's HEADLINE members re-priced (its existence proof and its Pareto-best "
        "constructions):")
    hl = FO[FO.book.isin(["SLV25", "SLV50", "EWall"]) & (FO.gross_mode == "native")]
    if len(hl):
        cols = ["panel", "book", "arm", "cost", "gross", "CAGR", "Sharpe", "MaxDD",
                "lad_Sharpe", "lad_MaxDD", "dSharpe", "dMaxDD", "D1", "D4"]
        say(hl.sort_values("Sharpe", ascending=False).head(20)[cols].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n    (4b) does the proposal touch 4b PASSERS too?  (same control applied to rows that "
        "clear all five bars)")
    P = G[G.pass4b]
    say(f"      4b passers {len(P)};  D1 {pct(int(P.D1.sum()), len(P))};  "
        f"D4 {pct(int(P.D4.sum()), len(P))}")
    if len(P):
        say(P.groupby("gross_mode").agg(passers=("D1", "size"), D1=("D1", "sum"),
                                        D4=("D4", "sum")).to_string())

    # ---------------------------------------------------------------- (5) idea 131 read
    say("\n" + "=" * 200)
    say("(5) BEARS ON IDEA 131 — is `beat your own ladder point` the gross bar idea 131 could "
        "not find?")
    say("    idea 131 asked for a MINIMUM MEAN GROSS bar that admits the Pareto-best defensive "
        "books and empties the ladder.  D1 is a different shape: it is per-row and needs no "
        "gross threshold at all.  The test it must pass is the same one: does it separate the "
        "class from the ladder?")
    say(f"      ladder points themselves (the `control` arm, all gross modes): "
        f"{len(ctl)} rows, floor-only {int(ctl.floor_only.sum())}, and by construction D1 "
        f"{int(ctl.D1.sum())} — the bar empties the ladder EXACTLY (a ladder point can never "
        f"beat itself).")
    say(f"      of idea 133's {n} members, D1 keeps {int(FO.D1.sum())} and drops "
        f"{n - int(FO.D1.sum())}.")
    sp = H.spearman(FO.gross.values, FO.dSharpe.values)
    say(f"      spearman(mean gross, dSharpe) over members = {sp:+.3f}  "
        f"(idea 131's axis vs this one)")

    # ---------------------------------------------------------------- (6) rule 8
    say("\n" + "=" * 200)
    say("(6) RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 only, 2017-2026 read once")
    say("    S0 no screen | S1 IS-4b-admissible | S3 IS floor-only (idea 133) | "
        "S5 = S3 + beats own IS ladder point (THE PROPOSAL) | S6 = ladder screen alone | "
        "S7 = IS-4a vs the LIVE book (the by-product, section 7b)")
    cols = ["panel", "cost", "gross_mode", "sel", "n_admitted", "pick", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "spy_OOS_Sharpe", "v2_OOS_Sharpe", "beat_spy",
            "beat_v2", "beat_ctl", "oos_rank"]
    say(W[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n    (6a) selector summary over the 12 cells:")
    t = W.groupby("sel").agg(cells_with_a_pick=("OOS_Sharpe", lambda s: int(s.notna().sum())),
                             mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                             mean_OOS_CAGR=("OOS_CAGR", "mean"),
                             mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
                             beat_spy=("beat_spy", "sum"), beat_v2=("beat_v2", "sum"),
                             beat_ctl=("beat_ctl", "sum"),
                             mean_admitted=("n_admitted", "mean"))
    say(t.to_string(float_format=lambda x: f"{x:.3f}"))
    say(f"    SPY OOS Sharpe by panel: " +
        ", ".join(f"{p} {W[W.panel == p].spy_OOS_Sharpe.iloc[0]:.3f}" for p in PANELS))

    say("\n    (6b) PAIRED — does the proposal (S5) change idea 133's pick (S3), and does it "
        "help?  Only cells where BOTH have a pick.")
    piv = W.pivot_table(index=["panel", "cost", "gross_mode"], columns="sel",
                        values="OOS_Sharpe")
    pk = W.pivot_table(index=["panel", "cost", "gross_mode"], columns="sel", values="pick",
                       aggfunc="first")
    both = piv[["S3", "S5"]].dropna()
    moved = int((pk.loc[both.index, "S3"] != pk.loc[both.index, "S5"]).sum())
    say(f"      cells with both picks: {len(both)};  picks that MOVED: {moved}")
    if len(both):
        d = both.S5 - both.S3
        say(f"      mean paired OOS Sharpe S5 - S3 = {d.mean():+.4f}  "
            f"(S5 better in {int((d > 0).sum())}, worse in {int((d < 0).sum())}, "
            f"tied in {int((d == 0).sum())})")
    say(f"      cells where S3 has a pick but S5 does not (the proposal abstains): "
        f"{int((piv.S3.notna() & piv.S5.isna()).sum())} of {int(piv.S3.notna().sum())}")
    for a, b in (("S5", "S0"), ("S3", "S0"), ("S6", "S0"), ("S1", "S0")):
        p2 = piv[[a, b]].dropna()
        if len(p2):
            d = p2[a] - p2[b]
            say(f"      paired {a} - {b}: n {len(p2)}  mean {d.mean():+.4f}  "
                f"wins {int((d > 0).sum())}/{len(p2)}")

    # ---------------------------------------------------------------- (7) KEEP paths
    say("\n" + "=" * 200)
    say("(7) BOTH KEEP PATHS ON ALL 1,632 ROWS")
    say(f"    4a (beat the LIVE book, RULES v2): {pct(int(G.pass4a_v2.sum()), len(G))}   "
        f"[against RULES v1 for continuity: {pct(int(G.pass4a.sum()), len(G))}]")
    say(f"    4b (capital-worthy vs SPY):        {pct(int(G.pass4b.sum()), len(G))}")
    say(pd.crosstab([G.panel, G.cost], [G.gross_mode, G.pass4b]).to_string())
    both_paths = G[G.pass4b & G.pass4a_v2]
    say(f"\n    rows passing BOTH 4a(v2) and 4b: {len(both_paths)}")
    if len(both_paths):
        cols = ["panel", "book", "arm", "cost", "gross_mode", "gross", "CAGR", "Sharpe",
                "MaxDD", "H1", "H2", "OOS_Sharpe", "D1", "D4", "TO"]
        say(both_paths.sort_values("Sharpe", ascending=False).head(25)[cols].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n    (7b) THE 4a PATH AGAINST THE LIVE BOOK — a by-product, and new only because the "
        "live baseline changed: idea 133's corpus was scored against RULES v1, and v2 went "
        "live on 2026-09-06.  Nothing here is a new instrument.")
    A = G[G.pass4a_v2]
    say(f"      rows clearing 4a vs RULES v2: {len(A)} of {len(G)}   "
        f"(by panel: {A.groupby('panel').size().to_dict()})")
    if len(A):
        cols = ["panel", "book", "arm", "cost", "gross_mode", "gross", "CAGR", "Sharpe",
                "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4b",
                "fail4b", "D1", "TO"]
        say(A.sort_values("Sharpe", ascending=False)[cols].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
        say(f"      of these, ALSO passing 4b: {int(A.pass4b.sum())};  also beating their own "
            f"ladder point (D1): {int(A.D1.sum())};  4b failing bars: "
            f"{A.fail4b.value_counts().to_dict()}")
    say("\n      RULE 8 ON THE 4a PATH (selector S7 in the table above): the arm is chosen by IS "
        "Sharpe among the arms that clear 4a against RULES v2 on 2009-2016 ALONE, and read "
        "once on 2017-2026.")
    s7 = W[W.sel == "S7"]
    cols7 = ["panel", "cost", "gross_mode", "n_admitted", "pick", "OOS_CAGR", "OOS_Sharpe",
             "OOS_MaxDD", "v2_OOS_Sharpe", "v2_OOS_CAGR", "v2_OOS_MaxDD", "spy_OOS_Sharpe",
             "beat_v2", "beat_spy"]
    say(s7[cols7].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    ok = s7.dropna(subset=["OOS_Sharpe"])
    say(f"      S7 has a pick in {len(ok)} of 12 cells;  beats RULES v2 OOS in "
        f"{int(ok.beat_v2.sum())};  beats SPY OOS in {int(ok.beat_spy.sum())};  mean OOS "
        f"Sharpe {ok.OOS_Sharpe.mean():.3f} vs v2 {ok.v2_OOS_Sharpe.mean():.3f}, SPY "
        f"{ok.spy_OOS_Sharpe.mean():.3f}")
    say(f"      full-sample 4a passers that ALSO hold on the OOS window alone "
        f"(pass4a_v2_OOS): {int(A.pass4a_v2_OOS.sum()) if len(A) else 0} of {len(A)}")

    say("\n    best 4b passers that ALSO beat their own ladder point (D1) — the only rows the "
        "proposal would let anyone quote:")
    q = G[G.pass4b & G.D1]
    if len(q):
        cols = ["panel", "book", "arm", "cost", "gross_mode", "gross", "CAGR", "Sharpe",
                "MaxDD", "H1", "H2", "OOS_Sharpe", "lad_Sharpe", "dSharpe", "dMaxDD", "TO"]
        say(q.sort_values("Sharpe", ascending=False).head(20)[cols].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
    else:
        say("      (none)")

    # ---------------------------------------------------------------- (8) verdict
    say("\n" + "=" * 200)
    say("(8) VERDICT")
    r_d1 = int(FO.D1.sum()) / n
    say(f"    H_ladder predicted: most members fail the control, worst in m53.")
    say(f"    H_real   predicted: most members beat it, m53 no worse.")
    rates = FO.groupby("gross_mode").D1.mean().to_dict()
    say(f"    measured: overall D1 {r_d1:.1%};  by gross mode " +
        ", ".join(f"{k} {v:.1%}" for k, v in rates.items()))
    say(f"    D4 (matched drawdown instead of matched gross): {FO.D4.mean():.1%}")
    say("=" * 200)

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nWrote {STEM}.grid.csv ({len(G)} rows), {STEM}.walkforward.csv ({len(W)} rows), "
          f"{STEM}.console.txt")


if __name__ == "__main__":
    main()
