#!/usr/bin/env python3
"""QUEUE idea 146 — pin-m-or-let-the-screen-choose   (cloud sprint, 2026-09-05)

PRE-REGISTERED QUESTION (from QUEUE.md idea 146, written before any number below was read)
    Idea 144 found that rule 8's FAMILY screen — the convention that lets the walk-forward
    screen choose the static gross multiplier m as well as the arm — is the FIRST non-inert
    screen the project has (7 of 18 picks moved, against 0 for POINT-4b) and yet buys no
    Sharpe: +1.1pp OOS CAGR for -1.7pp of extra drawdown, -0.003 Sharpe.

    Before any convention lets a screen choose gross, PRICE that trade on idea 74's axis
    (pp of CAGR per pp of MaxDD) against the two instruments the project already prices on
    that axis — the 200d trend gate and plain de-grossing — at MATCHED book and cost, and
    say whether m should be PINNED at the published gross in rule 8.

    A finding that the screen's exchange rate BEATS both references is a KILL of the pinning
    proposal and is reported as such.

WHAT IS NEW HERE (idea 144 measured the move; this run prices it and decides the convention)
    Q1  Reproduce idea 144's Q6 walk-forward exactly, from its own harness, before reading
        anything new.  Its committed picks file is asserted cell by cell.
    Q2  Split the FAMILY screen into its two decisions.  PIN = idea 144's S3 admissibility and
        arm choice, m forced to the published 1.00.  That isolates the m decision: PIN vs
        FAM-hi differ in m and nothing else wherever they pick the same arm.
    Q3  Idea 74's axis.  Per cell, the screen's own exchange rate (OOS pp CAGR gained per pp
        of |MaxDD| given up, PIN -> FAM-hi) against
          (a) the 200d gate's price in that same cell (control -> g200-dg, same axis), and
          (b) the de-grossing LADDER's own slope, fitted on the PIN arm's 25-point gross
              family in that same cell.
        Same panel, same book, same cost, same window in every comparison.
    Q4  Mechanism.  Is Sharpe invariant along the family (so IS Sharpe cannot order m and the
        m choice is made entirely by the IS drawdown cap)?  And is the IS-admissible m larger
        than the OOS-admissible m — i.e. does idea 128's shallow IS window make the screen
        systematically over-gross?
    Q5  Verdict on the convention, plus both KEEP paths on every selector's pick.

TUNED PARAMETERS — exactly two, both swept and fully reported
    1. the m-rule inside the family screen: {point = idea 144's S1 (admissibility and the arm
       ranking both read at m = 1.00), pin = family admissibility with m forced to 1.00,
       hi = max admissible m, lo = min admissible m}.  All four run in every cell, all four
       reported.
    2. the m ceiling m_max in {1.00, 1.30} (idea 131's ladder top / idea 144's no-leverage
       ceiling).  Both run, both reported.
    The 4b bar coefficients are NOT tuned here: phi = 0.70 and delta = 0.60, the published
    values, throughout.  The 25-point m grid is a construction dial swept exhaustively, not a
    tuned parameter, and every point of it is written to the family CSV.

HARNESS
    Idea 94's simulator (`2026-09-04_drawdown-insurance-price-list_B.py`) and idea 144's cell
    builder (`2026-09-05_is-the-ladder-even-a-candidate_C.py`) are IMPORTED, not re-implemented,
    so this run adjudicates exactly the corpus the question was asked about.  Checks run before
    any new number: (a) H.run vs engine.backtest on the ungated EWall u56 book, machine
    precision; (b) idea 94's published EWall+vol60-dg u56@10bps row (11.6% / 1.133 / -16.9%);
    (c) idea 144's committed per-cell picks for S0/S1/S3, cell by cell; (d) idea 144's paired
    aggregates (S1 0.127/1.022/-0.211, S3 0.138/1.019/-0.228).

CORPUS: 3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 17 arms x 2 cost rungs
    = 306 books, each over a 25-point gross family m in {0.10, 0.15, ..., 1.30} = 7,650 runs.
    Weekly rebalance, t+1 execution, 10 bps costs (25 bps rung reported alongside),
    75% target gross at m = 1.00.  IS <= 2016-12-31 chosen on; OOS >= 2017-01-01 read once.

CAVEATS carried forward, stated not buried
  - SURVIVORSHIP (idea 54): all three panels are current-constituent lists.  The small panel is
    a sub-$2B screen run TODAY and back-filled to 2010; tickers with max_1d_move >= 1.0 in
    data/small_meta.csv are dropped first (idea 118).  Delisted names are absent, which
    flatters high-gross settings — i.e. it flatters the FAMILY screen's own direction of
    travel, so a finding against the screen is if anything understated.
  - Idea 128: the IS window's worst SPY drawdown (-22.1%) is shallower than the OOS window's
    (-33.7%), so every IS drawdown cap admits too much.  Q4 measures that directly rather than
    assuming it.
  - Idea 144 Q1: the two `ebud` arms are not pure exposure rescales (an absolute turnover
    budget bites differently at different m), so their family curves are not scale-free.  They
    are kept in the corpus and flagged in every table that uses a family slope.
  - Idea 38 (u56/broad carry a calendar-day index) and idea 126 (t+1 only, no lag band).
  - Q3's matched-DD control is a HINDSIGHT statistic (it reads the OOS drawdown to pick the
    matched ladder point).  It is labelled as such and never used as a selector.
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

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-05_pin-m-or-let-the-screen-choose_cloud"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(OUT / "2026-09-04_drawdown-insurance-price-list_B.py", "i94")
G = _load(OUT / "2026-09-05_is-the-ladder-even-a-candidate_C.py", "i144")

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = G.COSTS
BOOKS = G.BOOKS
PANELS = G.PANELS
MGRID = G.MGRID
PHI0, DELTA0 = G.PHI0, G.DELTA0
MRULES = ["point", "pin", "hi", "lo"]   # tuned parameter 1 (point = idea 144's S1, the incumbent)
MCEILS = [1.00, 1.30]                   # tuned parameter 2
PUBLISHED_M = 1.00
PURE_KINDS = ("ctl", "gate", "stop")    # idea 144 Q1: the scale-free arm kinds

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 3000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def pp(x):
    return 100.0 * x


def rate(dc_pp, dd_pp, floor=0.10):
    """idea 74's axis: pp of CAGR per pp of |MaxDD|.  Undefined below a 0.1pp DD move."""
    return dc_pp / dd_pp if abs(dd_pp) > floor else np.nan


def slope_pp(sub, ccol, dcol):
    """pp CAGR per pp |MaxDD| along a family curve, least squares over its points."""
    x = np.abs(sub[dcol].values) * 100.0
    y = sub[ccol].values * 100.0
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3 or np.ptp(x[ok]) < 1e-9:
        return np.nan
    return float(np.polyfit(x[ok], y[ok], 1)[0])


def matched(sub, target_dd_abs, ccol, dcol):
    """CAGR the family reaches at |MaxDD| = target, linear interpolation on the family curve.
       HINDSIGHT when target comes from an OOS number — labelled everywhere it is used."""
    s = sub.dropna(subset=[ccol, dcol]).copy()
    s["ad"] = s[dcol].abs()
    s = s.sort_values("ad")
    if len(s) < 2 or target_dd_abs < s.ad.iloc[0] or target_dd_abs > s.ad.iloc[-1]:
        return np.nan
    return float(np.interp(target_dd_abs, s.ad.values, s[ccol].values))


# ------------------------------------------------------------------ build the family corpus
def refs():
    """SPY bars, the IS-window bars and RULES v1 per (panel, cost).  No arm is simulated here,
       so it is cheap enough to recompute on the cached path."""
    REF = {}
    for pname in PANELS:
        px, spy, _ = G.panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        REF[pname] = dict(spy=spy, bfull=G.bars_win(spy, "full"), bIS=G.bars_win(spy, "IS"),
                          v1={c: backtest(px, rules_v1_weights(px), cost_bps=c,
                                          freq=FREQ)["returns"].loc[start:] for c in COSTS})
    return REF


def build():
    F, REF = [], {}
    for pname in PANELS:
        px, spy, desc = G.panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bfull, bIS = G.bars_win(spy, "full"), G.bars_win(spy, "IS")
        mS, mSo = metrics(spy), metrics(spy.loc[OOS_START:])
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY full {mS['CAGR']:.2%} / {mS['Sharpe']:.3f} / {mS['MaxDD']:.2%}   "
            f"OOS {mSo['CAGR']:.2%} / {mSo['Sharpe']:.3f} / {mSo['MaxDD']:.2%}   "
            f"IS-window SPY MaxDD {bIS['sdd']:.2%} CAGR {bIS['scagr']:.2%}")
        v1 = {}
        for c in COSTS:
            v1[c] = backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
        REF[pname] = dict(spy=spy, bfull=bfull, bIS=bIS, v1=v1)
        for book in BOOKS:
            for c in COSTS:
                df, _ = G.do_cell(pname, px, spy, book, c, bfull, bIS, v1[c])
                F.append(df)
                say(f"    ... {pname}/{book}/{c:.0f}bps  {len(df)} rows")
    return pd.concat(F, ignore_index=True), REF


# ------------------------------------------------------------------ selectors
def admissible(sub, which, mmax):
    """IS-window admissible (arm, m) pairs under 4b's IS-readable bars (idea 144's shape:
       both Sharpe halves, the DD cap, the CAGR floor).  'nofloor' drops the CAGR floor."""
    s = sub[sub.m <= mmax + 1e-9]
    ok = (s.IS_m_H1 > 0) & (s.IS_m_H2 > 0) & (s.IS_m_DD > 0)
    if which == "full":
        ok &= (s.IS_m_CAGR > 0)
    return s[ok]


def pick(sub, mrule, mmax, which="full"):
    """arm by argmax IS Sharpe over admissible pairs (the incumbent statistic), then m by rule.

    point : idea 144's S1 — admissibility and the arm ranking are both read at m = 1.00 only.
    pin   : FAMILY admissibility (the screen may see the whole family when ranking arms) but m
            is forced to the published gross.  point vs pin isolates the ADMISSIBILITY change;
            pin vs hi/lo isolates the m CHOICE, which is what idea 146 is about.
    hi/lo : the max / min admissible m for the chosen arm (idea 144's S3 / S5 m-rules).
    If the pinned point is not itself IS-admissible the cell still pins — a pin is a
    convention, not a search — and that is counted in `pin_admissible`.
    """
    A = admissible(sub, which, mmax)
    if mrule == "point":
        A = A[np.isclose(A.m, PUBLISHED_M)]
    if not len(A):
        return None
    arm = A.loc[A.IS_Sharpe.idxmax(), "arm"]
    ms = admissible(sub, which, mmax)
    ms = ms[ms.arm == arm].m.values
    if mrule in ("point", "pin"):
        return arm, PUBLISHED_M, bool(np.any(np.isclose(ms, PUBLISHED_M)))
    return arm, float(ms.max() if mrule == "hi" else ms.min()), True


def oos_of(sub, arm, m_):
    r = sub[(sub.arm == arm) & (np.isclose(sub.m, m_))]
    if not len(r):
        return None
    r = r.iloc[0]
    return dict(OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                OOS_Sharpe_full=r.OOS_Sharpe_full, pass4a=bool(r.pass4a),
                m_H1=r.m_H1, m_H2=r.m_H2, m_OOS=r.m_OOS, m_DD=r.m_DD, m_CAGR=r.m_CAGR,
                gross=r.gross, kind=r.kind)


# ------------------------------------------------------------------ main
def main():
    say("=" * 200)
    say("IDEA 146 — PIN m, OR LET THE SCREEN CHOOSE IT?  Pricing rule 8's FAMILY screen on "
        "idea 74's axis against the 200d gate and de-grossing, at matched book and cost.")
    say(f"    corpus 3 panels x {len(BOOKS)} books x 17 arms x {len(COSTS)} cost rungs x "
        f"{len(MGRID)} gross points = {3*len(BOOKS)*17*len(COSTS)*len(MGRID)} runs.  "
        f"IS <= {IS_END} chosen on, OOS >= {OOS_START} read once.")
    say(f"    m-rules {MRULES} x m ceilings {MCEILS};  4b bars fixed at published "
        f"phi={PHI0}, delta={DELTA0}.")
    say("=" * 200)

    # ---------------- harness reproduction, before any new number
    px0, spy0, _ = G.panel("u56")
    W0 = H.targets(px0, "EWall", None)
    a = H.run(px0, W0, m=1.0, bps=PCOST)["r"]
    b = backtest(px0, W0, cost_bps=PCOST, freq=FREQ)["returns"]
    d = float((a - b).abs().max())
    say(f"\nCHECK (a) H.run vs engine.backtest, ungated EWall u56: max|diff| = {d:.3e} "
        f"-> {'PASS' if d < 1e-12 else 'FAIL'}")
    assert d < 1e-12

    FAM = OUT / f"{STEM}.family.csv.gz"
    if FAM.exists():
        say(f"\nCORPUS CACHE: reading the already-simulated family grid from {FAM.name} "
            f"(delete it to force a full re-simulation; the two paths are identical by "
            f"construction — the cache is written by this same script).")
        F = pd.read_csv(FAM)
        REF = refs()
    else:
        F, REF = build()
    F = F.reset_index(drop=True)
    n_at1 = int((np.isclose(F.m, 1.00)).sum())
    exp = len(PANELS) * len(BOOKS) * len(COSTS) * 17
    say(f"\nCORPUS: {len(F)} family rows; {n_at1} books at the published m=1.00 "
        f"-> {'PASS' if n_at1 == exp else 'FAIL'} (expected {exp}; idea 144's full corpus is 306)")
    assert n_at1 == exp

    chk = F[(F.panel == "u56") & (F.book == "EWall") & (F.cost == 10.0) &
            (F.arm == "vol60-dg") & (np.isclose(F.m, 1.00))].iloc[0]
    ok94 = (abs(chk.CAGR - 0.116) < 6e-4 and abs(chk.Sharpe - 1.133) < 6e-4
            and abs(chk.MaxDD + 0.169) < 6e-4)
    say(f"CHECK (b) idea 94's published EWall+vol60-dg u56@10bps: {chk.CAGR:.3%} / "
        f"{chk.Sharpe:.3f} / {chk.MaxDD:.3%}  (published 11.6% / 1.133 / -16.9%) "
        f"-> {'PASS' if ok94 else 'FAIL'}")
    assert ok94

    F.to_csv(OUT / f"{STEM}.family.csv.gz", index=False, compression="gzip")

    # ---------------- Q1: reproduce idea 144's Q6 picks cell by cell
    say("\n" + "=" * 200)
    say("Q1 — REPRODUCTION OF IDEA 144's RULE-8 WALK-FORWARD (nothing new is read until this passes)")
    cells = [(p, bk, c) for p in PANELS for bk in BOOKS for c in COSTS]
    rep = []
    for pname, book, c in cells:
        sub = F[(F.panel == pname) & (F.book == book) & (F.cost == c)]
        at1 = sub[np.isclose(sub.m, 1.00)]
        s0 = at1.loc[at1.IS_Sharpe.idxmax(), "arm"]
        p1 = pick(sub, "point", 1.00)                     # == idea 144's S1 (POINT-4b)
        p3 = pick(sub, "hi", 1.30)                        # == idea 144's S3 (FAMILY-4b)
        rep.append(dict(panel=pname, book=book, cost=c,
                        S0=f"{s0}@1.00",
                        S1=("-" if p1 is None else f"{p1[0]}@1.00"),
                        S3=("-" if p3 is None else f"{p3[0]}@{p3[1]:.2f}")))
    R = pd.DataFrame(rep)
    pf = OUT / "2026-09-05_is-the-ladder-even-a-candidate_C.picks.csv"
    if pf.exists():
        P144 = pd.read_csv(pf)
        cols = [c for c in ("S0", "S1", "S2", "S3") if c in P144.columns]
        M = R.merge(P144, on=["panel", "book", "cost"], suffixes=("", "_144"))
        bad, checked = 0, []
        for c_ in ("S0", "S1", "S3"):
            if c_ + "_144" in M.columns:
                norm = {"-": "(none)", "": "(none)", "nan": "(none)"}
                x = M[c_].fillna("(none)").astype(str).str.strip().replace(norm)
                y = M[c_ + "_144"].fillna("(none)").astype(str).str.strip().replace(norm)
                diff = int((x != y).sum())
                bad += diff
                checked.append(f"{c_}: {diff}")
                for _, rr in M[x != y].iterrows():
                    say(f"    DIFF {rr.panel}/{rr.book}/{rr.cost}: {c_} here="
                        f"{rr[c_]!r} idea144={rr[c_ + '_144']!r}")
        say(f"  committed picks file found ({len(P144)} cells, cols {cols}); differing "
            f"cells vs this run [{'; '.join(checked)}]: {bad} of {3*len(M)} "
            f"-> {'PASS' if bad == 0 else 'FAIL'}")
        assert bad == 0, "idea 144's published walk-forward picks did not reproduce"
    say(R.to_string(index=False))

    # ---------------- Q2: the two decisions, split
    say("\n" + "=" * 200)
    say("Q2 — SPLITTING THE FAMILY SCREEN.  Same admissibility, same arm statistic; only the "
        "m-rule differs.  'pin' = the published gross 1.00.")
    W = []
    for pname, book, c in cells:
        sub = F[(F.panel == pname) & (F.book == book) & (F.cost == c)]
        spy = REF[pname]["spy"]
        mso = metrics(spy.loc[OOS_START:])
        mv = metrics(H.window(REF[pname]["v1"][c], "OOS"))
        for mmax in MCEILS:
            for mr in MRULES:
                pk = pick(sub, mr, mmax)
                base = dict(panel=pname, book=book, cost=c, mmax=mmax, mrule=mr,
                            spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
                            spy_OOS_MaxDD=mso["MaxDD"], v1_OOS_Sharpe=mv["Sharpe"])
                if pk is None:
                    W.append(dict(base, arm="(none)", m=np.nan, pin_admissible=np.nan))
                    continue
                arm, m_, pin_ok = pk
                o = oos_of(sub, arm, m_)
                W.append(dict(base, arm=arm, m=m_, pin_admissible=pin_ok, **o))
    WF = pd.DataFrame(W)
    WF["beat_spy"] = WF.OOS_Sharpe > WF.spy_OOS_Sharpe
    WF["beat_v1"] = WF.OOS_Sharpe > WF.v1_OOS_Sharpe
    WF["pass4b_full"] = (WF.m_H1 > 0) & (WF.m_H2 > 0) & (WF.m_OOS > 0) & (WF.m_DD > 0) & (WF.m_CAGR > 0)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    def agg(D, label):
        A = D[D.arm != "(none)"].groupby(["mmax", "mrule"]).agg(
            cells=("arm", "size"), mean_m=("m", "mean"),
            OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
            OOS_MaxDD=("OOS_MaxDD", "mean"), beat_SPY=("beat_spy", "sum"),
            beat_v1=("beat_v1", "sum"), pass4a=("pass4a", "sum"), pass4b=("pass4b_full", "sum"))
        say(f"\n  {label}")
        say(A.to_string(float_format=lambda x: f"{x:.3f}"))
        return A

    agg(WF, "ALL 18 CELLS (a rule with fewer cells is abstaining, not losing):")
    entered = WF[WF.arm != "(none)"].groupby(["panel", "book", "cost"]).size()
    paired = set(entered[entered == len(MCEILS) * len(MRULES)].index)
    say(f"\n  paired cells (every m-rule at every ceiling enters): {len(paired)} of 18 "
        f"-> {sorted(paired)}")
    PW = WF[WF.set_index(['panel', 'book', 'cost']).index.isin(paired)]
    A = agg(PW, f"PAIRED on the {len(paired)} cells:")
    # CHECK (d): idea 144's published paired aggregates for S1 (= point/pin) and S3 (= hi@1.30)
    for (mm, mr), exp, lbl in (((1.00, "point"), (0.127, 1.022, -0.211), "idea 144 S1"),
                               ((1.30, "hi"), (0.138, 1.019, -0.228), "idea 144 S3")):
        got = (A.loc[(mm, mr), "OOS_CAGR"], A.loc[(mm, mr), "OOS_Sharpe"],
               A.loc[(mm, mr), "OOS_MaxDD"])
        ok = all(abs(a - b) < 6e-4 for a, b in zip(got, exp))
        say(f"  CHECK (d) {lbl} == this run's {mr}@m_max{mm:.2f}: "
            f"{got[0]:.3f} / {got[1]:.3f} / {got[2]:.3f}  vs published "
            f"{exp[0]:.3f} / {exp[1]:.3f} / {exp[2]:.3f} -> {'PASS' if ok else 'FAIL'}")
        assert ok

    say("\n  per-cell picks (arm@m), by m ceiling:")
    for mmax in MCEILS:
        T = WF[WF.mmax == mmax].copy()
        T["pk"] = np.where(T.arm == "(none)", "-", T.arm + "@" + T.m.map(lambda v: f"{v:.2f}"))
        say(f"\n    m_max = {mmax:.2f}")
        say(T.pivot_table(index=["panel", "book", "cost"], columns="mrule", values="pk",
                          aggfunc="first").to_string())

    # ---------------- Q3: idea 74's axis
    say("\n" + "=" * 200)
    say("Q3 — THE PRICE OF LETTING THE SCREEN CHOOSE m, ON IDEA 74's AXIS "
        "(pp of CAGR per pp of |MaxDD|), AT MATCHED BOOK AND COST.")
    say("    screen_rate  = OOS CAGR gained per pp of |MaxDD| given up, going pin -> hi.")
    say("    ladder_slope = the same rate available by simply turning the gross dial on the "
        "PINNED arm's own 25-point family (OOS window; IS-window slope also shown).")
    say("    g200_price   = the 200d gate's price in the same cell: pp CAGR surrendered per pp "
        "of |MaxDD| bought, control@1.00 -> g200-dg@1.00, OOS window.")
    say("    A screen whose rate does NOT beat the ladder slope is buying nothing a dial "
        "cannot buy, and it is spending drawdown budget without a mandate.")
    PR = []
    for pname, book, c in cells:
        sub = F[(F.panel == pname) & (F.book == book) & (F.cost == c)]
        for mmax in MCEILS:
            p_pin, p_hi = pick(sub, "pin", mmax), pick(sub, "hi", mmax)
            if p_pin is None or p_hi is None:
                continue
            a_pin, m_pin, pin_ok = p_pin
            a_hi, m_hi = p_hi[0], p_hi[1]
            o_pin, o_hi = oos_of(sub, a_pin, m_pin), oos_of(sub, a_hi, m_hi)
            fam = sub[sub.arm == a_pin].sort_values("m")
            dC = pp(o_hi["OOS_CAGR"] - o_pin["OOS_CAGR"])
            dD = pp(abs(o_hi["OOS_MaxDD"]) - abs(o_pin["OOS_MaxDD"]))
            ctl = sub[(sub.arm == "control") & (np.isclose(sub.m, 1.00))]
            g2 = sub[(sub.arm == "g200-dg") & (np.isclose(sub.m, 1.00))]
            gdc = gdd = np.nan
            if len(ctl) and len(g2):
                gdc = pp(ctl.OOS_CAGR.iloc[0] - g2.OOS_CAGR.iloc[0])
                gdd = pp(abs(ctl.OOS_MaxDD.iloc[0]) - abs(g2.OOS_MaxDD.iloc[0]))
            mt = matched(fam, abs(o_hi["OOS_MaxDD"]), "OOS_CAGR", "OOS_MaxDD")
            p_pt = pick(sub, "point", mmax)
            fam_pt = sub[sub.arm == p_pt[0]].sort_values("m") if p_pt else fam
            mt_pt = matched(fam_pt, abs(o_hi["OOS_MaxDD"]), "OOS_CAGR", "OOS_MaxDD")
            PR.append(dict(
                panel=pname, book=book, cost=c, mmax=mmax, arm_pin=a_pin, arm_hi=a_hi,
                same_arm=(a_pin == a_hi), m_hi=m_hi, pin_admissible=pin_ok,
                dCAGR_pp=dC, dMaxDD_pp=dD, screen_rate=rate(dC, dD),
                dSharpe=o_hi["OOS_Sharpe"] - o_pin["OOS_Sharpe"],
                ladder_slope_OOS=slope_pp(fam, "OOS_CAGR", "OOS_MaxDD"),
                ladder_slope_IS=slope_pp(fam, "IS_CAGR", "IS_MaxDD"),
                g200_price=rate(gdc, gdd), g200_dDD_pp=gdd,
                matched_ladder_CAGR_pp=pp(mt) if np.isfinite(mt) else np.nan,
                hi_CAGR_pp=pp(o_hi["OOS_CAGR"]),
                matched_minus_hi_pp=(pp(mt) - pp(o_hi["OOS_CAGR"])) if np.isfinite(mt) else np.nan,
                arm_point=(p_pt[0] if p_pt else "(none)"),
                matchedPOINT_minus_hi_pp=((pp(mt_pt) - pp(o_hi["OOS_CAGR"]))
                                          if np.isfinite(mt_pt) else np.nan),
                fam_scale_free=(fam.kind.iloc[0] in PURE_KINDS)))
    PRD = pd.DataFrame(PR)
    PRD.to_csv(OUT / f"{STEM}.price.csv", index=False)
    show = ["panel", "book", "cost", "mmax", "arm_point", "arm_pin", "arm_hi", "same_arm", "m_hi",
            "dCAGR_pp", "dMaxDD_pp", "screen_rate", "dSharpe", "ladder_slope_OOS",
            "ladder_slope_IS", "g200_price", "matchedPOINT_minus_hi_pp", "fam_scale_free"]
    say("\n" + PRD[show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    moved = PRD[PRD.dMaxDD_pp.abs() > 0.10]
    if len(moved):
        beat_lad = int((moved.screen_rate > moved.ladder_slope_OOS).sum())
        beat_lad_is = int((moved.screen_rate > moved.ladder_slope_IS).sum())
        beat_g2 = int((moved.screen_rate > moved.g200_price).sum())
        say(f"\n  rows where the m-move actually shifts drawdown (> 0.1pp): {len(moved)}")
        say(f"    screen rate beats the OOS ladder slope in {beat_lad}/{len(moved)};  "
            f"the IS ladder slope in {beat_lad_is}/{len(moved)};  "
            f"the 200d gate's price in {beat_g2}/{len(moved)}")
        say(f"    median screen rate {moved.screen_rate.median():.3f} pp/pp   vs  median OOS "
            f"ladder slope {moved.ladder_slope_OOS.median():.3f}   vs  median g200 price "
            f"{moved.g200_price.median():.3f}")
        say(f"    mean OOS Sharpe change from the m-move: {moved.dSharpe.mean():+.4f}  "
            f"(cells improved: {int((moved.dSharpe > 0).sum())}/{len(moved)})")
        ident = int(moved.same_arm.sum())
        say(f"    IDENTITY, stated not hidden: in {ident}/{len(moved)} of these rows the screen "
            f"keeps the arm and moves only m, so its exchange rate IS the ladder's own local "
            f"slope by construction — the screen is the dial, wearing a screen's clothes.  The "
            f"matched-DD control on that same arm is therefore trivially 0.000 and is reported "
            f"only for completeness (mean {moved.matched_minus_hi_pp.mean():+.3f} pp).")
        mp = moved.matchedPOINT_minus_hi_pp.dropna()
        if len(mp):
            say(f"    HINDSIGHT matched-DD control against the INCUMBENT (point) arm's own "
                f"ladder: {mp.mean():+.3f} pp of CAGR at the screen pick's OOS drawdown "
                f"(positive = the incumbent arm's dial dominates the screen's pick); "
                f"dominates in {int((mp > 0).sum())}/{len(mp)}")

    # ---------------- Q4: mechanism
    say("\n" + "=" * 200)
    say("Q4 — MECHANISM.  (i) Sharpe along a book's own gross family; (ii) the IS-admissible m "
        "against the OOS-admissible m.")
    inv = F.groupby(["panel", "book", "cost", "arm", "kind"]).agg(
        sharpe_range=("Sharpe", lambda s: s.max() - s.min()),
        is_sharpe_range=("IS_Sharpe", lambda s: s.max() - s.min()),
        cagr_mono=("CAGR", lambda s: bool(np.all(np.diff(s.values) >= -1e-12)))).reset_index()
    say("\n  (i) within-family Sharpe RANGE over the 25 gross points, by arm kind "
        "(the screen ranks arms on IS Sharpe, so a small range means IS Sharpe cannot order m):")
    say(inv.groupby("kind").agg(books=("arm", "size"),
                                med_full_range=("sharpe_range", "median"),
                                max_full_range=("sharpe_range", "max"),
                                med_IS_range=("is_sharpe_range", "median"),
                                max_IS_range=("is_sharpe_range", "max"),
                                CAGR_monotone=("cagr_mono", "sum")
                                ).to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  (ii) the m the IS window admits vs the m the OOS window would have admitted, for "
        "the PINNED arm of every entering cell (idea 128: the IS window's crash is shallower, "
        "so an IS drawdown cap admits too much):")
    MM = []
    for pname, book, c in cells:
        sub = F[(F.panel == pname) & (F.book == book) & (F.cost == c)]
        p_pin = pick(sub, "pin", 1.30)
        if p_pin is None:
            continue
        arm = p_pin[0]
        fam = sub[sub.arm == arm]
        bO = REF[pname]["bfull"]
        okI = fam[(fam.IS_m_H1 > 0) & (fam.IS_m_H2 > 0) & (fam.IS_m_DD > 0) & (fam.IS_m_CAGR > 0)]
        cap_o = DELTA0 * abs(metrics(REF[pname]["spy"].loc[OOS_START:])["MaxDD"])
        flo_o = PHI0 * metrics(REF[pname]["spy"].loc[OOS_START:])["CAGR"]
        okO = fam[(fam.OOS_MaxDD.abs() < cap_o) & (fam.OOS_CAGR > flo_o) &
                  (fam.OOS_Sharpe > bO["soos"])]
        MM.append(dict(panel=pname, book=book, cost=c, arm=arm,
                       m_IS_max=float(okI.m.max()) if len(okI) else np.nan,
                       m_OOS_max=float(okO.m.max()) if len(okO) else np.nan,
                       n_IS=len(okI), n_OOS=len(okO)))
    MMD = pd.DataFrame(MM)
    if len(MMD):
        MMD["IS_minus_OOS"] = MMD.m_IS_max - MMD.m_OOS_max
        say(MMD.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        v = MMD.IS_minus_OOS.dropna()
        say(f"\n    IS-admissible m exceeds OOS-admissible m in {int((v > 0).sum())}/{len(v)} "
            f"cells; mean gap {v.mean():+.3f}, median {v.median():+.3f}")

    # ---------------- Q5: verdict
    say("\n" + "=" * 200)
    say("Q5 — BOTH KEEP PATHS ON EVERY SELECTOR'S PICK, AND THE VERDICT ON THE CONVENTION.")
    K = WF[WF.arm != "(none)"].groupby(["mmax", "mrule"]).agg(
        cells=("arm", "size"), pass4a=("pass4a", "sum"), pass4b=("pass4b_full", "sum"),
        beat_SPY_OOS=("beat_spy", "sum"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"))
    say(K.to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  (4a = beats RULES v1 on both Sharpe halves with no worse MaxDD, same panel/cost; "
        "4b = all five bars on the full sample at the published phi/delta.)")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.family.csv.gz / .walkforward.csv / .price.csv / .console.txt")


if __name__ == "__main__":
    main()
