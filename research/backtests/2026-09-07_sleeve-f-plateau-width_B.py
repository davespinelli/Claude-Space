#!/usr/bin/env python3
"""QUEUE idea 138 — sleeve-f-plateau-width   (lane B, 2026-09-07).

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 138, written before any number here
was read)
    "idea 134's 4b pass count peaks at f=0.15-0.20 on both panels and both cost rungs and the
     two 4b margins move monotonically and in opposite directions across f.  Apply idea 128's
     plateau test to this dial before any f is written into RULES: measure the Sharpe range
     over the published f sweep and where the no-sleeve control sits inside it."

WHY IT MATTERS NOW
    Idea 139 (2026-09-07, cloud) filed a 4b KEEP-candidate whose ONLY tuned constant is this
    dial: `EWall + 25% S3 sleeve`, 0.75 gross, weekly.  Its memo asserts (point 6) that f is
    "not knife-edged" because the 4b-PASSING WINDOW is f = 0.10-0.25 (u56) / 0.20-0.25 (broad).
    That is a pass-count statement, not idea 128's plateau test.  Idea 128's own verdict was
    that the Sharpe plateau is GENERAL and that the control usually sits ABOVE the whole dial
    (34 of 54 cells), and — its finding 3 — that Sharpe is the WRONG axis because these
    constants are adopted for the DRAWDOWN bar.  This run therefore measures the f dial on
    BOTH axes, in idea 128's own columns, before f = 0.25 can be written into RULES.

WHAT IS BEING TESTED (three questions, fixed in advance)
    Q1  SHARPE PLATEAU (the queue's literal ask).  Per cell: the Sharpe range over the
        published f sweep, the percentile of the no-sleeve control (f = 0) inside it, whether
        the control is inside / above / below, the fraction of points within 0.05 Sharpe of
        the cell's best (idea 128's `plateau_frac`), and whether the candidate's f = 0.25
        beats the control.
    Q2  THE AXIS THE DIAL IS ADOPTED FOR (idea 128's finding 3, carried forward).  The same
        three statistics on MaxDD and on the 4b margin-min (the worst of 4b's five bars, in
        its own units), because a sleeve fraction is adopted for the drawdown cap and the
        CAGR floor, not for Sharpe.
    Q3  RULE 8 (PROTOCOL 8).  Choose ONE f per cell on 2009-2016 alone under two selectors
        fixed in writing before any OOS number was read, then read 2017-2026 ONCE:
          S0  argmax IS Sharpe over the f sweep (no screen)
          S1  argmax IS Sharpe among f whose IS window clears 4b's four IS-evaluable bars
              (H1, H2, DD cap, CAGR floor, all measured inside the IS window)
        Both are scored against the f = 0 control and against SPY, paired per cell.

CORPUS (every point reported; nothing is selected on except the two tuned parameters)
    f            0.00 (the NO-SLEEVE CONTROL) + the PUBLISHED sweep {0.05,0.10,0.15,0.20,0.25,
                 0.50} + three ADDED points {0.30,0.35,0.40} that close idea 134's gap between
                 0.25 and 0.50 + three EDGE-PROBE points {0.60,0.75,1.00}.  f = 1.00 is the
                 PURE SLEEVE (no equity leg at all), so the dial is bounded by construction and
                 the grid-edge flag of ideas 240/256/328 cannot apply to the reported argmax.
                 Statistics are reported for THREE scopes separately — `pub` (the queue's own
                 grid), `ext` (+0.30/0.35/0.40) and `all` (+ the edge probe) — so the queue's
                 literal question is answered on the queue's own sweep and nothing else.
    sleeve set   S3 = TLT/GLD/UUP  and  S4 = TLT/GLD/DBC/UUP   (idea 133/134's two sets)
    base book    EWall (idea 139's candidate) and TOP20 (idea 134's R20) — both reported
    panels       u56 (research/universe.json) and broad (universe_broad.json).  The small
                 panel has no TLT/GLD/DBC/UUP, so a sleeve book cannot exist there; idea 136
                 owns that panel and this run does not pretend to answer it.
    costs        10 and 25 bps, both reported on every row.
    = 2 panels x 2 books x 2 sleeve sets x 2 costs = 16 cells x 13 f-points = 208 arm-rows.

TUNED PARAMETERS — exactly two, per PROTOCOL 4: the sleeve fraction f (13 values, ALL
    reported) and the sleeve asset set (S3 / S4, both reported).  Panels, base books, cost
    rungs, both selectors and both KEEP paths are reported axes and are never selected on.

BOOK CONSTRUCTION (idea 134's, verbatim, so the f=0.25/f=0.50 rows are comparable to the
record rather than a re-description):
    raw = (1-f) * base_book + f * sleeve(assets);  book = raw * (0.75 / sum(raw)) per day.
    sleeve(assets) = momentum-vote x risk-parity (ideas 100/104), vote over {12-1m, 6m, 3m}.
    At f = 0 this is the ungated base book at 0.75 gross exactly — the control is the book
    itself, not a re-scaled variant.

KEEP PATHS (PROTOCOL 4, both evaluated on every row)
    4a  vs the LIVE book, `baseline.rules_v2_weights` (PROTOCOL 3), COST-MATCHED (the arm's
        own rung).  Idea 398 is open on exactly this comparand; this run states its choice
        rather than leaving it implicit, and also reports the count against RULES v1 at a
        fixed 10 bps so both conventions in the record are visible.
    4b  Sharpe > SPY in both halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of
        SPY's, all on the same panel and the same evaluated slice.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  The Sharpe range over the published f sweep is SMALL (< 0.10 in most cells) — idea
        128 found a median range of 0.091 across five other dials.
    P2  The no-sleeve control does NOT sit above the whole dial on EWall cells (idea 139's
        candidate beats its own control on Sharpe), i.e. this dial is one of idea 128's
        minority cells.  If the control sits above the dial anywhere, it should be TOP20.
    P3  On MaxDD the control is the DEEPEST point of the dial (idea 128 found this in 41 of
        54 cells for the drawdown instruments), so the f dial's real content is the DD axis.
    P4  Rule 8's S1 picks f in the 0.15-0.25 region in most cells, matching idea 139's 7-of-8.
    P5  4b pass counts peak in the interior of the sweep and fall at f = 0.50 (the CAGR
        floor binds), reproducing idea 134's peak rather than moving it.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): both panels are current constituents.  Absent delistings inflate
      the EQUITY leg more than the ETF sleeve, so every statistic here is biased in favour of
      LOW f — i.e. in favour of the no-sleeve control.  A finding that the control sits high
      on the dial is therefore overstated, and a finding that the sleeve wins is understated.
    * Idea 128's own caveat: the IS window's SPY MaxDD is shallower than the OOS window's, so
      an IS drawdown cap is measured on a window that cannot express a deep drawdown; S1 is
      biased toward admitting too much.  Reported, not corrected.
    * Idea 126: t+1 execution only, no lag band.  Idea 38: u56/broad carry the calendar-day
      index.  Idea 127: mean realised gross is printed on every row.
    * Sharpe RANGE is a within-cell statistic and is never pooled by value across panels.
    * MaxDD is one number off one path; the 4b DD cap turns on exactly that number (idea 321).
    * The sleeve legs are three or four ETFs over one macro regime (idea 139 risk (a)); a
      plateau in f says nothing about a sample in which all legs are dead at once.

HARNESS: idea 94's simulator (`H.run`, `H.targets`, `H.halves`, `H.pass4a`) is IMPORTED and
asserted against engine.backtest before any new number is read.  Idea 134's sleeve builder is
re-implemented here and asserted to reproduce idea 134's committed .grid.csv rows at f=0.50 /
f=0.25 on the shared (panel, cost) cells.  Deterministic, standalone.  Modifies nothing.
Writes .console.txt, .grid.csv, .plateaus.csv, .walkforward.csv, .keeppaths.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-07_sleeve-f-plateau-width_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I134_GRID = OUT / "2026-09-05_sleeve-f-that-clears-the-floor_cloud.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PHI, DELTA = 0.70, 0.60                       # 4b CAGR floor / DD cap fractions of SPY
PUBLISHED_FS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.50]
ADDED_FS = [0.30, 0.35, 0.40]
EDGE_FS = [0.60, 0.75, 1.00]                  # closes the grid edge: f=1.00 is the pure sleeve
FS = [0.0] + sorted(PUBLISHED_FS + ADDED_FS + EDGE_FS)  # tuned parameter 1 — ALL reported
SLEEVES = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"]}  # tuned param 2
BOOKS = ["EWall", "TOP20"]
PANELS = ["u56", "broad"]
CAND_F = 0.25                                 # idea 139's candidate value — reported, not chosen
PLATEAU_EPS = 0.05                            # idea 128's own tolerance, unchanged

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ books ----
def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """Ideas 100/104's sleeve, verbatim from ideas 133/134: momentum vote x risk parity."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def blend(px, base_W, sl_W, f):
    """(1-f) * base + f * sleeve, rescaled to GROSS per day.  f=0 returns the base book."""
    if f == 0.0:
        return base_W
    raw = (1 - f) * base_W + f * sl_W
    return raw.mul((GROSS / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


# ------------------------------------------------------------------ metrics --
def win(r, which):
    return r.loc[:IS_END] if which == "IS" else (r.loc[OOS_START:] if which == "OOS" else r)


def bars_win(spy, which):
    """4b's bars computed inside one window.  'full' uses PROTOCOL's halves of the full slice;
    'IS' uses halves of the IS window (the only halves an IS-only screen can see)."""
    s = win(spy, which)
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    """4b bar margins in each bar's own units.  Positive = clears."""
    s = win(r, which)
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def pass4b(mg):
    return bool(all(v > 0 for v in mg.values()))


# ------------------------------------------------------------------ main -----
def main():
    say(f"IDEA 138 — sleeve-f PLATEAU WIDTH (lane B).  {len(FS)} f-points x 2 panels x "
        f"{len(BOOKS)} books x {len(SLEEVES)} sleeve sets x {len(COSTS)} cost rungs = "
        f"{len(FS)*2*len(BOOKS)*len(SLEEVES)*len(COSTS)} arm-rows.")
    say(f"f sweep: published {PUBLISHED_FS} + added {ADDED_FS} + edge probe {EDGE_FS} "
        f"(f=1.00 is the pure sleeve, so the dial is bounded) + control f=0.00.  "
        f"Plateau tolerance {PLATEAU_EPS} (idea 128's).  Costs {COSTS} bps, weekly, t+1, "
        f"gross {GROSS}.")

    rows, rets, ref = [], {}, {}

    for pk in PANELS:
        px = load_universe(broad=(pk == "broad"))
        missing = [t for t in SLEEVES["S4"] if t not in px.columns]
        if missing:
            raise RuntimeError(f"{pk} lacks {missing}")
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        b_full, b_is = bars_win(spy, "full"), bars_win(spy, "IS")
        ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        ref[pk] = dict(bfull=b_full, bIS=b_is, spy=ms, spy_oos=mo, start=start)
        say(f"\n[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {b_full['s1']:.3f}/{b_full['s2']:.3f}; OOS Sharpe {mo['Sharpe']:.3f} "
            f"CAGR {mo['CAGR']:.2%} MaxDD {mo['MaxDD']:.2%}")
        say(f"    4b bars (full slice): H1>{b_full['s1']:.3f} H2>{b_full['s2']:.3f} "
            f"OOS>{b_full['soos']:.3f} MaxDD>={-DELTA*abs(b_full['sdd']):.2%} "
            f"CAGR>={PHI*b_full['scagr']:.2%}")

        # ---- live baselines, cost-matched (PROTOCOL 3) -----------------------
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk]["v2"], ref[pk]["v1"] = v2, v1
        for c in COSTS:
            m2, m1 = metrics(v2[c]), metrics(v1[c])
            h2, h1 = H.halves(v2[c]), H.halves(v1[c])
            say(f"    RULES v2 @{c:.0f}bps {m2['CAGR']:.2%}/{m2['Sharpe']:.3f}/{m2['MaxDD']:.2%} "
                f"halves {h2[0]:.3f}/{h2[1]:.3f} | v1 @{c:.0f}bps "
                f"{m1['CAGR']:.2%}/{m1['Sharpe']:.3f}/{m1['MaxDD']:.2%} halves {h1[0]:.3f}/{h1[1]:.3f}")

        # ---- gate (a): H.run with every instrument off == engine.backtest ----
        Wchk = H.targets(px, "EWall")
        a = H.run(px, Wchk, bps=10.0, freq=FREQ)["r"].loc[start:]
        b = backtest(px, Wchk, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
        say(f"    [gate a] H.run vs engine.backtest on EWall: max|d| {float((a-b).abs().max()):.3e}")
        assert float((a - b).abs().max()) < 1e-12

        base_W = {bk: H.targets(px, bk) for bk in BOOKS}
        sl_W = {sk: sleeve_weights(px, av) for sk, av in SLEEVES.items()}

        for bk in BOOKS:
            for sk in SLEEVES:
                for f in FS:
                    W = blend(px, base_W[bk], sl_W[sk], f)
                    for c in COSTS:
                        out = H.run(px, W, bps=c, freq=FREQ)
                        r = out["r"].loc[start:]
                        key = (pk, bk, sk, c, f)
                        rets[key] = r
                        m, mI, mO = metrics(r), metrics(win(r, "IS")), metrics(r.loc[OOS_START:])
                        h1, h2 = H.halves(r)
                        mgf, mgi = margins(r, b_full, "full"), margins(r, b_is, "IS")
                        rows.append(dict(
                            panel=pk, book=bk, sleeve=sk, cost=c, f=f,
                            published=(f in PUBLISHED_FS or f == 0.0),
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            IS_Sharpe=mI["Sharpe"], IS_CAGR=mI["CAGR"], IS_MaxDD=mI["MaxDD"],
                            OOS_Sharpe=mO["Sharpe"], OOS_CAGR=mO["CAGR"], OOS_MaxDD=mO["MaxDD"],
                            gross=float(out["gross"].loc[start:].mean()),
                            turnover=float(out["to"].loc[start:].sum() / (len(r) / 252)),
                            m_H1=mgf["H1"], m_H2=mgf["H2"], m_OOS=mgf["OOS"], m_DD=mgf["DD"],
                            m_CAGR=mgf["CAGR"], m_min=min(mgf.values()), pass4b=pass4b(mgf),
                            IS_m_min=min(mgi.values()), IS_pass4b=pass4b(mgi),
                            pass4a_v2=H.pass4a(r, v2[c]),
                            pass4a_v1_10=H.pass4a(r, v1[10.0]),
                        ))

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---- gate (b): reproduce idea 134's committed rows -----------------------
    say("\n[gate b] REPRODUCTION of idea 134's committed .grid.csv (its ungated `control` arm, "
        "TOP20 base = its R20 book, shared f values)")
    if I134_GRID.exists():
        g134 = pd.read_csv(I134_GRID)
        g = g134[(g134.arm == "control")].copy()
        g["sleeve"] = np.where(g.book.str.startswith("S3"), "S3",
                               np.where(g.book.str.startswith("S4"), "S4", "R20"))
        g["f"] = np.where(g.book == "R20", 0.0,
                          pd.to_numeric(g.book.str.split("-").str[-1], errors="coerce") / 100.0)
        mine = G[G.book == "TOP20"].copy()
        cmp_rows = []
        for _, q in g.iterrows():
            if q.sleeve == "R20":
                cand = mine[(mine.panel == q.panel) & (mine.cost == q.cost) & (mine.f == 0.0)]
                cand = cand.drop_duplicates(subset=["panel", "cost", "f"])
            else:
                cand = mine[(mine.panel == q.panel) & (mine.cost == q.cost) &
                            (mine.sleeve == q.sleeve) & (np.isclose(mine.f, q.f))]
            if len(cand) != 1:
                continue
            k = cand.iloc[0]
            cmp_rows.append(dict(panel=q.panel, book=q.book, cost=q.cost,
                                 dS=k.Sharpe - q.Sharpe, dC=k.CAGR - q.CAGR,
                                 dD=k.MaxDD - q.MaxDD))
        R = pd.DataFrame(cmp_rows)
        if len(R):
            say(f"    matched {len(R)} committed rows; max|dSharpe| {R.dS.abs().max():.3e}  "
                f"max|dCAGR| {R.dC.abs().max():.3e}  max|dMaxDD| {R.dD.abs().max():.3e}")
            assert R.dS.abs().max() < 1e-9, "idea 134 reproduction FAILED"
        else:
            say("    no comparable rows matched — reproduction NOT established")
    else:
        say("    idea 134 grid missing — reproduction NOT established")

    # ---- full grid ----------------------------------------------------------
    say("\nFULL GRID (208 arm-rows).  `published` marks the queue's own sweep; f=0.00 is the "
        "no-sleeve control.")
    cols = ["panel", "book", "sleeve", "cost", "f", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "gross", "turnover", "m_min", "pass4b",
            "pass4a_v2"]
    for pk in PANELS:
        for bk in BOOKS:
            say(f"\n--- {pk} / {bk} ---")
            say(G[(G.panel == pk) & (G.book == bk)][cols].to_string(
                index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- Q1/Q2: the plateau table ------------------------------------------
    say("\n" + "=" * 110)
    say("Q1/Q2 — PLATEAU TABLE, idea 128's columns, one row per (panel, book, sleeve, cost, "
        "scope, axis).")
    say("  scope 'pub' = the queue's published sweep only {0.05..0.25, 0.50}; 'ext' adds "
        "{0.30,0.35,0.40}.  The control f=0 is NOT part of the sweep — it is the reference "
        "whose percentile inside the sweep's range is reported.")
    say("  ctl_pctile = share of swept points the control BEATS on that axis (1.00 = control "
        "above every setting of the dial).  ctl_inside = strictly between min and max.")
    say("  AXES: Sharpe (the queue's literal ask), MaxDD (|dd|, lower is better -> scored as "
        "-|dd| so higher is better), m_min (the worst of 4b's five bar margins).")

    prows = []
    for (pk, bk, sk, c), sub in G.groupby(["panel", "book", "sleeve", "cost"]):
        sub = sub.sort_values("f")
        ctl = sub[sub.f == 0.0].iloc[0]
        for scope, fs in (("pub", PUBLISHED_FS), ("ext", PUBLISHED_FS + ADDED_FS),
                          ("all", PUBLISHED_FS + ADDED_FS + EDGE_FS)):
            s = sub[sub.f.isin(fs)].sort_values("f")
            for axis, col, sign in (("Sharpe", "Sharpe", 1.0), ("MaxDD", "MaxDD", 1.0),
                                    ("m_min", "m_min", 1.0)):
                v = sign * s[col].values                 # MaxDD is negative: higher = shallower
                cv = sign * ctl[col]
                cand = s[np.isclose(s.f, CAND_F)]
                prows.append(dict(
                    panel=pk, book=bk, sleeve=sk, cost=c, scope=scope, axis=axis, pts=len(v),
                    v_min=float(v.min()), v_max=float(v.max()),
                    v_range=float(v.max() - v.min()),
                    ctl=float(cv), ctl_pctile=float((cv > v).mean()),
                    ctl_inside=bool(v.min() < cv < v.max()),
                    ctl_above_all=bool(cv >= v.max()), ctl_below_all=bool(cv <= v.min()),
                    cand_f=CAND_F, cand_v=float(sign * cand[col].iloc[0]) if len(cand) else np.nan,
                    cand_beats_ctl=bool(len(cand) and (sign * cand[col].iloc[0]) > cv),
                    plateau_frac=float((v >= v.max() - PLATEAU_EPS).mean()) if axis == "Sharpe"
                    else np.nan,
                    argmax_f=float(s.f.values[int(np.argmax(v))]),
                ))
    P = pd.DataFrame(prows)
    P.to_csv(OUT / f"{STEM}.plateaus.csv", index=False)

    for axis in ("Sharpe", "MaxDD", "m_min"):
        for scope in ("pub", "ext", "all"):
            A = P[(P.axis == axis) & (P.scope == scope)]
            say(f"\n[{axis} / {scope}]  {len(A)} cells")
            say(A[["panel", "book", "sleeve", "cost", "pts", "v_min", "v_max", "v_range", "ctl",
                   "ctl_pctile", "ctl_inside", "ctl_above_all", "ctl_below_all", "cand_v",
                   "cand_beats_ctl", "plateau_frac", "argmax_f"]].to_string(
                index=False, float_format=lambda x: f"{x:.4f}"))
            say(f"  SUMMARY {axis}/{scope}: control ABOVE all {int(A.ctl_above_all.sum())} / "
                f"INSIDE {int(A.ctl_inside.sum())} / BELOW all {int(A.ctl_below_all.sum())} "
                f"of {len(A)}; median range {A.v_range.median():.4f}; median ctl pctile "
                f"{A.ctl_pctile.median():.2f}; f=0.25 beats control in "
                f"{int(A.cand_beats_ctl.sum())}/{len(A)}")
            if axis == "Sharpe":
                say(f"  median plateau_frac (share of points within {PLATEAU_EPS} of the cell's "
                    f"best): {A.plateau_frac.median():.2f}")

    # ---- the queue's literal sentence, answered ----------------------------
    say("\n" + "-" * 110)
    say("THE QUEUE'S LITERAL QUESTION — Sharpe range over the PUBLISHED f sweep, and where the "
        "no-sleeve control sits inside it:")
    A = P[(P.axis == "Sharpe") & (P.scope == "pub")]
    say(f"  Sharpe range per cell: min {A.v_range.min():.4f}  median {A.v_range.median():.4f}  "
        f"max {A.v_range.max():.4f}")
    say(f"  control ABOVE the whole sweep in {int(A.ctl_above_all.sum())} of {len(A)} cells; "
        f"strictly INSIDE in {int(A.ctl_inside.sum())}; BELOW all in {int(A.ctl_below_all.sum())}")
    say(f"  idea 128's reference (5 other dials, 54 cells): above 34 / inside 15 / below 5, "
        f"median range 0.091, median ctl pctile 0.86")
    for bk in BOOKS:
        Ab = A[A.book == bk]
        say(f"    {bk}: above {int(Ab.ctl_above_all.sum())} / inside {int(Ab.ctl_inside.sum())} "
            f"/ below {int(Ab.ctl_below_all.sum())} of {len(Ab)}; median ctl pctile "
            f"{Ab.ctl_pctile.median():.2f}; median range {Ab.v_range.median():.4f}")

    # ---- 4b pass counts by f (idea 134's peak, re-read) --------------------
    say("\n" + "-" * 110)
    say("4b PASS COUNT BY f (idea 134 reported a peak at f=0.15-0.20; this run's corpus is a "
        "different book set, so this is a re-reading of the SHAPE, not of its counts)")
    piv = G.pivot_table(index="f", columns="book", values="pass4b", aggfunc="sum")
    piv["all"] = G.groupby("f").pass4b.sum()
    piv["n_cells"] = G.groupby("f").size()
    say(piv.to_string())
    say("4a (vs LIVE RULES v2, cost-matched — PROTOCOL 3): " + str(int(G.pass4a_v2.sum())) +
        f" of {len(G)};  4a (vs RULES v1 @ fixed 10 bps, the record's older convention): "
        f"{int(G.pass4a_v1_10.sum())} of {len(G)}  [idea 398 is open on this comparand]")
    both = G[(G.pass4b) & (G.pass4a_v2)]
    say(f"both paths: {len(both)} of {len(G)}")

    # ---- Q3: rule 8 ---------------------------------------------------------
    say("\n" + "=" * 110)
    say("Q3 — RULE 8 WALK-FORWARD.  f chosen on 2009-2016 ONLY, 2017-2026 read once.  "
        "S0 = argmax IS Sharpe over the swept f (control f=0 excluded from the pick — the "
        "question is which f, and the control is the thing the pick must beat).  "
        "S1 = the same among f whose IS window clears 4b's four IS-evaluable bars.")
    wrows = []
    for (pk, bk, sk, c), sub in G.groupby(["panel", "book", "sleeve", "cost"]):
        ctl = sub[sub.f == 0.0].iloc[0]
        swept = sub[sub.f > 0.0]
        for scope, fs in (("pub", PUBLISHED_FS), ("ext", PUBLISHED_FS + ADDED_FS),
                          ("all", PUBLISHED_FS + ADDED_FS + EDGE_FS)):
            s = swept[swept.f.isin(fs)]
            for sel in ("S0", "S1"):
                pool = s if sel == "S0" else s[s.IS_pass4b]
                if not len(pool):
                    wrows.append(dict(panel=pk, book=bk, sleeve=sk, cost=c, scope=scope,
                                      selector=sel, pick=np.nan, abstain=True))
                    continue
                p = pool.loc[pool.IS_Sharpe.idxmax()]
                wrows.append(dict(
                    panel=pk, book=bk, sleeve=sk, cost=c, scope=scope, selector=sel,
                    pick=p.f, abstain=False, n_admitted=len(pool),
                    IS_Sharpe=p.IS_Sharpe, OOS_Sharpe=p.OOS_Sharpe, OOS_CAGR=p.OOS_CAGR,
                    OOS_MaxDD=p.OOS_MaxDD,
                    ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                    ctl_OOS_MaxDD=ctl.OOS_MaxDD,
                    spy_OOS_Sharpe=ref[pk]["spy_oos"]["Sharpe"],
                    spy_OOS_CAGR=ref[pk]["spy_oos"]["CAGR"],
                    spy_OOS_MaxDD=ref[pk]["spy_oos"]["MaxDD"],
                    premium=p.OOS_Sharpe - ctl.OOS_Sharpe,
                    vs_spy=p.OOS_Sharpe - ref[pk]["spy_oos"]["Sharpe"],
                    oos4b_DD=(DELTA * abs(ref[pk]["spy_oos"]["MaxDD"]) - abs(p.OOS_MaxDD)) > 0,
                    oos4b_CAGR=(p.OOS_CAGR - PHI * ref[pk]["spy_oos"]["CAGR"]) > 0,
                    oos4b_Sharpe=(p.OOS_Sharpe - ref[pk]["spy_oos"]["Sharpe"]) > 0,
                    best_OOS_f=float(s.loc[s.OOS_Sharpe.idxmax()].f),
                    best_OOS_Sharpe=float(s.OOS_Sharpe.max()),
                    rho_IS_OOS=H.spearman(s.IS_Sharpe.values, s.OOS_Sharpe.values),
                ))
    Wf = pd.DataFrame(wrows)
    Wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(Wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for scope in ("pub", "ext", "all"):
        for sel in ("S0", "S1"):
            A = Wf[(Wf.scope == scope) & (Wf.selector == sel) & (~Wf.abstain)]
            ab = int(((Wf.scope == scope) & (Wf.selector == sel) & (Wf.abstain)).sum())
            if not len(A):
                say(f"  [{sel}/{scope}] abstains in all cells")
                continue
            say(f"\n  [{sel}/{scope}] picks in {len(A)} cells (abstains {ab}); picks "
                f"{sorted(A.pick.unique())}; modal f {A.pick.mode().tolist()}")
            say(f"    mean OOS Sharpe {A.OOS_Sharpe.mean():.4f} vs control {A.ctl_OOS_Sharpe.mean():.4f} "
                f"vs SPY {A.spy_OOS_Sharpe.mean():.4f}; mean premium over control "
                f"{A.premium.mean():+.4f} (positive in {int((A.premium>0).sum())}/{len(A)})")
            bs, bd, bc = (A.oos4b_Sharpe.astype(bool), A.oos4b_DD.astype(bool),
                          A.oos4b_CAGR.astype(bool))
            say(f"    OOS 4b bars cleared by the pick: Sharpe>SPY {int(bs.sum())}/{len(A)}, "
                f"DD cap {int(bd.sum())}/{len(A)}, CAGR floor {int(bc.sum())}/{len(A)}; "
                f"all three {int((bs & bd & bc).sum())}/{len(A)}")
            say(f"    IS->OOS rank agreement across f (Spearman, per cell): median "
                f"{A.rho_IS_OOS.median():.3f}; the OOS-best f is the pick in "
                f"{int((A.pick == A.best_OOS_f).sum())}/{len(A)} cells; regret (OOS best minus "
                f"pick) mean {float((A.best_OOS_Sharpe - A.OOS_Sharpe).mean()):+.4f}")

    # ---- KEEP paths, headline rows -----------------------------------------
    say("\n" + "=" * 110)
    say("KEEP PATHS — every row that clears 4b, and the candidate row idea 139 filed.")
    K = G[G.pass4b].sort_values(["panel", "book", "sleeve", "cost", "f"])
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(K[cols + ["m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}") if len(K) else "  none")
    cand = G[(G.book == "EWall") & (G.sleeve == "S3") & (np.isclose(G.f, CAND_F))]
    say("\nIdea 139's candidate rows (EWall + S3 at f=0.25), re-derived here:")
    say(cand[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ctlrows = G[(G.book == "EWall") & (G.sleeve == "S3") & (G.f == 0.0)]
    say("Its no-sleeve control (EWall, f=0.00):")
    say(ctlrows[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- predictions scored -------------------------------------------------
    say("\n" + "=" * 110)
    say("PRE-REGISTERED PREDICTIONS, scored")
    As = P[(P.axis == "Sharpe") & (P.scope == "pub")]
    say(f"  P1 Sharpe range < 0.10 in most cells: {int((As.v_range < 0.10).sum())}/{len(As)} -> "
        f"{'HELD' if (As.v_range < 0.10).mean() > 0.5 else 'FAILED'}")
    Ae = As[As.book == "EWall"]
    At = As[As.book == "TOP20"]
    say(f"  P2 control not above the whole dial on EWall: EWall above-all "
        f"{int(Ae.ctl_above_all.sum())}/{len(Ae)}, TOP20 above-all {int(At.ctl_above_all.sum())}"
        f"/{len(At)} -> {'HELD' if Ae.ctl_above_all.sum() < At.ctl_above_all.sum() or Ae.ctl_above_all.sum()==0 else 'FAILED'}")
    Ad = P[(P.axis == "MaxDD") & (P.scope == "pub")]
    say(f"  P3 control is the DEEPEST point on MaxDD: below-all "
        f"{int(Ad.ctl_below_all.sum())}/{len(Ad)} -> "
        f"{'HELD' if Ad.ctl_below_all.mean() > 0.5 else 'FAILED'}")
    A1 = Wf[(Wf.selector == "S1") & (Wf.scope == "pub") & (~Wf.abstain)]
    inreg = int(A1.pick.between(0.15, 0.25).sum()) if len(A1) else 0
    say(f"  P4 rule 8's S1 picks f in 0.15-0.25 in most cells: {inreg}/{len(A1)} -> "
        f"{'HELD' if len(A1) and inreg/len(A1) > 0.5 else 'FAILED'}")
    pc = G.groupby("f").pass4b.sum()
    say(f"  P5 4b pass count peaks in the interior and falls at f=0.50: counts by f "
        f"{pc.to_dict()} -> "
        f"{'HELD' if pc.idxmax() not in (0.0, 0.50) and pc.get(0.50, 0) < pc.max() else 'FAILED'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.[grid|plateaus|walkforward|keeppaths].csv + .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
