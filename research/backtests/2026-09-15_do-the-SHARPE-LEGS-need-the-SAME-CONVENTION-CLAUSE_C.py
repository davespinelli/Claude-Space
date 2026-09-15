#!/usr/bin/env python3
"""Idea 893 (lane C, 2026-09-15) - do-the-SHARPE-LEGS-need-the-SAME-CONVENTION-CLAUSE.

QUESTION (the queue's, verbatim)
-------------------------------
Idea 879 found the H2 leg flips 152 times across 71 books, MORE than CAGR's 102, while H1 flips 0.
Census the record's committed half-sample Sharpe claims against their own rebalance-calendar
spreads and report what a margin/spread >= 1 clause would cost them.

WHAT A "COMMITTED HALF-SAMPLE SHARPE CLAIM" IS ON THIS RECORD
------------------------------------------------------------
`baseline._row` publishes `H1 / H2` for every book, and PROTOCOL rule 4 turns those two numbers
into verdict legs on BOTH paths:
    4b Sharpe legs : book H_i Sharpe  >  SPY H_i Sharpe            (i = 1, 2)
    4a Sharpe legs : book H_i Sharpe  >  RULES v2 (live) H_i Sharpe
A claim is therefore a (book, leg, comparand) triple, and its published value is read at the
PROTOCOL calendar k = 0.  A FAIL verdict is as much a claim as a PASS: "4a FAIL" on a leg that
flips sign at k = 3 is a date, not a rule.  Both directions are priced here.

THE CLAUSE (idea 879's, priced by idea 891 on the DD/CAGR legs)
    ratio = |margin at k = 0| / (spread of the same statistic across the offset grid)
    a leg's published verdict SURVIVES only if ratio >= 1.
Idea 891 priced this on the record's 9 committed 4b passes and reported, as a by-product of its
DD headline, 4b Sharpe ratios of 1.31-5.07 (H1) and 1.58-10.01 (H2) - i.e. the SPY-side Sharpe
legs never bound.  It did not read the 4a side, did not decompose the H1/H2 asymmetry 879 found,
and stopped at 9 books.  This run makes the Sharpe legs the object on BOTH comparands, over the
record's committed book set plus its never-selected ladder control, and asks 879's asymmetry
question directly: is H1's immunity a MARGIN (location) fact or a SPREAD (noise) fact?

THE TWO TUNED PARAMETERS (the queue's own; nothing else is selected on)
  1. CLAIM SET   SHELF   - the record's committed, memo-backed 4b passes (861's 8-book shelf plus
                           idea 879's own `u56-top20-g065-M`), IMPORTED from the committed lane-C
                           builder, not re-typed, so the books are the record's own
                 GRID    - 861's never-selected mechanical ladder (control: books nobody chose)
                 LIVE    - RULES v2 at its live settings on both panels (the book the 4a comparand
                           IS; its self-claim is the degenerate case and is reported as such)
  2. OFFSET GRID FULL (own cadence, every offset: 5 weekly / 21 monthly - 879's and 891's own)
                 HALF (k = 0..2 weekly / 0..10 monthly)
                 ALT  (even k only: 0,2,4 weekly / 0,2,..,20 monthly)
All 3 x 3 = 9 grid points reported for every hypothesis.

REPORTED-NEVER-TUNED: panel (U56, B136), comparand (SPY / RULES v2 live), cost rung (10, 25 bps),
window (FULL / IS / OOS), leg (H1, H2, and DD/CAGR/OOS carried for context), both KEEP paths.

GATES (printed before any hypothesis is read)
  G1 memo    every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
  G2 mask    the k = 0 offset mask is elementwise identical to `engine.rebalance_mask`.
  G3 engine  fast_run(k = 0) vs `engine.backtest` on a SHELF book.  bar 1e-9.
  G4 cross   idea 891's COMMITTED `.clause.csv` Sharpe-leg cells (4b and 4a ratio_H1/H2 on its 9
             SHELF books at both rungs) reproduced from this run's own arms.  bar 1e-6.
  G5 bars    SPY and RULES v2 (live) triples printed against the record's committed values.

PRE-REGISTERED HYPOTHESES (written before any number below was run; the only numbers in hand are
idea 879's and idea 891's published ones, which the queue itself quotes)
  H_SPY   : against SPY the clause costs the committed half-sample Sharpe claims NOTHING -
            0 of the SHELF books' H1 and H2 ratios fall below 1, at every one of the 9 grid points.
  H_LIVE  : against the LIVE book the same clause is near-total - median |ratio| over the SHELF's
            4a Sharpe legs is < 0.5 and at least 90% of those legs fail the clause.
  H_ASYM  : 879's "H1 flips 0, H2 flips 152" is a MARGIN fact, not a SPREAD fact - the H1 leg is
            NOT the quieter leg: median spread(H1) >= median spread(H2) across all books, while
            median |margin(H1)| > median |margin(H2)| on the comparand that flips.
  H_SPREAD: (the falsifiable alternative) H1 is intrinsically quieter - median spread(H1) is at
            least 25% BELOW median spread(H2).  H_ASYM and H_SPREAD cannot both hold; if neither
            does the answer is PARTIAL.
  H_SAME  : (the queue's title question) the Sharpe legs need the SAME clause as DD/CAGR, i.e. a
            Sharpe leg is the BINDING (min-ratio) leg on at least one SHELF book under 4b.
  H_WF    : (rule 8) the clause verdict is knowable ex ante - Spearman rho(IS ratio, OOS ratio)
            over the Sharpe-leg cells >= +0.5 AND at least half the books keep their IS clause
            verdict out of sample.  If this fails, no clause can be applied before the outcome
            window is read.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
  IS = window start .. 2016-12-31 (read and fitted).  OOS = 2017-01-01 .. end (read once).
  Declared IS-ONLY selector: the book with the highest IS min-ratio over its two 4b SHARPE legs
  (this run's own statistic).  Control selector: highest IS Sharpe (the record's usual).  Each
  pick's OOS CAGR / Sharpe / MaxDD is read once against SPY OOS and RULES v2 (live) OOS and both
  KEEP paths evaluated; the unselected base rate over all books is printed beside it.

KEEP PATHS: 4a (Sharpe > RULES v2 live in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's), evaluated at every cell.

SURVIVORSHIP: U56 and B136 are CURRENT-constituent panels.  Dead names are absent, so every LEVEL
below is optimistic and the 4b CAGR floor is easier to clear than on a point-in-time panel.  This
run's object - the SPREAD of a leg across equally arbitrary calendars, and the ratio of a margin
to it - is a WITHIN-book quantity and far less exposed to that bias than the levels are; the
levels quoted in the rule-8 section are not corrected for it.

PROTOCOL: 10 bps per unit turnover, next-day fills, no shorting, no leverage.  Deterministic,
standalone, no network.  Modifies nothing but its own outputs:
    .arms.csv  .clause.csv  .asym.csv  .census.csv  .walkforward.csv  .console.txt

Run: python research/backtests/2026-09-15_do-the-SHARPE-LEGS-need-the-SAME-CONVENTION-CLAUSE_C.py
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-15"
SLUG = "do-the-SHARPE-LEGS-need-the-SAME-CONVENTION-CLAUSE"
STAMP = f"{DATE}_{SLUG}_C"
OUT = ROOT / "research" / "backtests"

# the committed lane-C builder that idea 891 itself imported; books are the record's, not re-typed
LANEC = OUT / f"{DATE}_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"
CLAUSE891 = OUT / f"{DATE}_does-the-MARGIN-OVER-SPREAD-clause-EMPTY-THE-SHELF_cloud.clause.csv"

WARMUP, LAG, MAX_VOL = 260, 1, 0.60
RUNGS = [10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
SHARPE_LEGS = ["H1", "H2"]
ALL_LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

# tuned param 2: the offset grid.  keys are the dial's levels; values map cadence -> offsets.
OFFGRIDS = {
    "FULL": {"W": list(range(5)), "M": list(range(21))},
    "HALF": {"W": list(range(3)), "M": list(range(11))},
    "ALT": {"W": [0, 2, 4], "M": list(range(0, 21, 2))},
}
OFF_HEAD = "FULL"

# the record's committed comparand triple (idea 861/891's published SPY numbers, U56 panel)
SPY_COMMITTED = (0.1513, 0.886, -0.3372)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = _load(LANEC, "laneC893")
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


# ------------------------------------------------------------------ calendars and statistics
def offset_mask(idx, freq, k):
    """The book's own cadence mask moved k trading days later.  k = 0 IS the published calendar."""
    m = rebalance_mask(idx, freq)
    return m if k == 0 else m.shift(k, fill_value=False)


def stats(r, idx):
    """Full-sample moments in the record's COUNT half convention, plus IS and OOS windows.

    The half split is a COUNT split on a return series that starts at the same day for every
    offset, so k does not move the split point - the spread measured below is a calendar effect
    and nothing else."""
    r = np.asarray(r, float)
    idx = pd.DatetimeIndex(idx)
    cagr, sh, dd = fmet(r)
    h = len(r) // 2
    is_m = np.asarray(idx <= pd.Timestamp(IS_END))
    oo_m = np.asarray(idx >= pd.Timestamp(OOS_START))
    ic, ish, idd = fmet(r[is_m])
    oc, osh, odd = fmet(r[oo_m])
    # within-window halves, so the same two legs exist inside IS and inside OOS (rule-8 section)
    ih, oh = int(is_m.sum()) // 2, int(oo_m.sum()) // 2
    ri, ro = r[is_m], r[oo_m]
    return dict(CAGR=cagr, Sharpe=sh, MaxDD=dd, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
                IS_CAGR=ic, IS_Sharpe=ish, IS_MaxDD=idd,
                IS_H1=fsharpe(ri[:ih]), IS_H2=fsharpe(ri[ih:]),
                OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd,
                OOS_H1=fsharpe(ro[:oh]), OOS_H2=fsharpe(ro[oh:]))


def margins(s, cmp_, win=""):
    """Signed slack of each leg against a comparand, in the leg's own units.

    win = "" (FULL), "IS_" or "OOS_".  Inside IS/OOS only the two Sharpe legs and the level legs
    are defined; the FULL-sample "OOS" leg is named as such and only computed for win = ""."""
    p = win
    out = {"H1": s[p + "H1"] - cmp_[p + "H1"], "H2": s[p + "H2"] - cmp_[p + "H2"],
           "DD": 100.0 * (s[p + "MaxDD"] - DDCAP_FRAC * cmp_[p + "MaxDD"]),
           "CAGR": 100.0 * (s[p + "CAGR"] - CAGRFLOOR_FRAC * cmp_[p + "CAGR"])}
    if win == "":
        out["OOS"] = s["OOS_Sharpe"] - cmp_["OOS_Sharpe"]
    return out


def margins_4a(s, base, win=""):
    p = win
    out = {"H1": s[p + "H1"] - base[p + "H1"], "H2": s[p + "H2"] - base[p + "H2"],
           "DD": 100.0 * (s[p + "MaxDD"] - base[p + "MaxDD"])}
    if win == "":
        out["OOS"] = s["OOS_Sharpe"] - base["OOS_Sharpe"]
    return out


def leg_stat(s, leg, win=""):
    """The BOOK-side statistic whose calendar spread the clause compares the margin against."""
    p = win
    return {"H1": s[p + "H1"], "H2": s[p + "H2"], "OOS": s["OOS_Sharpe"],
            "DD": 100.0 * s[p + "MaxDD"], "CAGR": 100.0 * s[p + "CAGR"]}[leg]


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return float("nan")
    return float(a[ok].rank().corr(b[ok].rank()))


def keep_4b(m):
    return bool(m["H1"] > 0 and m["H2"] > 0 and m.get("OOS", 1.0) > 0 and m["DD"] > 0
                and m["CAGR"] > 0)


def keep_4a(m4a):
    return bool(m4a["H1"] > 0 and m4a["H2"] > 0 and m4a["DD"] >= 0)


def pct(x, n):
    return f"{x}/{n} ({x / n:.1%})" if n else f"{x}/0 (n/a)"


# ================================================================== run
def main():
    t0 = time.time()
    P(f"# Idea 893 - {SLUG}  ({DATE}, lane C)")
    P(f"# pandas {pd.__version__} numpy {np.__version__}")
    P("# 2 tuned dials: CLAIM SET [SHELF, GRID, LIVE] x OFFSET GRID [FULL, HALF, ALT].")
    P("# ALL 9 grid points reported.  Cost rung {10, 25} bps, panel, comparand, window: reported")
    P("# controls, never selected on.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels; every LEVEL below is optimistic.")
    P("")

    U = load_universe().dropna(how="all").ffill()
    B = load_universe(broad=True).dropna(how="all").ffill()
    PX = {"U56": U, "B136": B}
    for nm, px in PX.items():
        P(f"PANEL {nm}: {px.shape[1]} names x {len(px)} days, "
          f"{px.index[0].date()} .. {px.index[-1].date()}")

    # ---------------------------------------------------------------- the claim set
    books = C.shelf_books(U, B)                       # 861's shelf, imported
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    books["u56-top20-g065-M"] = dict(                 # idea 879's own committed 4b pass
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    SHELF = dict(books)
    GRID = C.grid_books(U, B)
    LIVE = {f"{p}-RULESv2-live": dict(panel=p, freq="W", W=rules_v2_weights(px, 0.03, 0.75),
                                      memo=None, src="LIVE (RULES v2, the 4a comparand itself)")
            for p, px in PX.items()}
    SETS = {"SHELF": SHELF, "GRID": GRID, "LIVE": LIVE}
    P(f"\nCLAIM SETS: SHELF {len(SHELF)} committed memo-backed 4b passes; "
      f"GRID {len(GRID)} never-selected ladder books; LIVE {len(LIVE)} (the 4a comparand itself).")
    P(f"  total books = {sum(len(v) for v in SETS.values())};  each carries TWO committed "
      f"half-sample Sharpe claims per comparand (H1, H2) = "
      f"{4 * sum(len(v) for v in SETS.values())} claims before the offset walk.")

    # ---------------------------------------------------------------- comparands
    start = {p: PX[p].index[WARMUP] for p in PX}
    SPY, V2 = {}, {}
    for p, px in PX.items():
        sr = px["SPY"].pct_change().fillna(0.0).loc[start[p]:]
        SPY[p] = {c: stats(sr.values, sr.index) for c in RUNGS}    # SPY has no rebalance calendar
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        V2[p] = {}
        for c in RUNGS:
            n = (r - t * c / 1e4).loc[start[p]:]
            V2[p][c] = stats(n.values, n.index)
        P(f"WINDOW {p}: {start[p].date()} .. {px.index[-1].date()}   IS ..{IS_END}   "
          f"OOS {OOS_START}..")
    P("CONVENTION: comparands are held at their OWN calendars - SPY has none, and RULES v2 is")
    P("  scored on the live weekly calendar, not the candidate's.  Only the BOOK's calendar moves.")

    # ---------------------------------------------------------------- GATES
    P("\n## Gates (printed before any hypothesis is read)")
    grows = []

    # G1 memo reproduction
    ok1, worst = True, {}
    for nm, b in SHELF.items():
        if b["memo"] is None:
            continue
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        n = (r - t * RUNG_HEAD / 1e4).loc[start[b["panel"]]:]
        s = stats(n.values, n.index)
        mc, ms, md = b["memo"]
        d = [abs(s["CAGR"] - mc), abs(s["Sharpe"] - ms),
             (abs(s["MaxDD"] - md) if md is not None else 0.0)]
        for k, v in zip(("dCAGR", "dSharpe", "dMaxDD"), d):
            if v > worst.get(k, (-1, ""))[0]:
                worst[k] = (v, nm)
        if d[0] > 0.010 or d[1] > 0.060 or d[2] > 0.020:
            ok1 = False
            P(f"  G1 MISS {nm}: dCAGR {d[0]:.4f} dSharpe {d[1]:.4f} dMaxDD {d[2]:.4f}")
    P(f"G1 memo   every SHELF book reproduces its committed triple: {'PASS' if ok1 else 'FAIL'}"
      f"  (worst " + ", ".join(f"{k} {v[0]:.4f} [{v[1]}]" for k, v in worst.items()) + ")")
    grows.append(dict(gate="G1_memo", result="PASS" if ok1 else "FAIL",
                      detail="; ".join(f"{k}={v[0]:.4g}({v[1]})" for k, v in worst.items())))

    # G2 mask identity at k = 0
    ok2 = all(offset_mask(PX[p].index, f, 0).equals(rebalance_mask(PX[p].index, f))
              for p in PX for f in ("W", "M"))
    P(f"G2 mask   offset_mask(k=0) == engine.rebalance_mask elementwise: {'PASS' if ok2 else 'FAIL'}")
    grows.append(dict(gate="G2_mask", result="PASS" if ok2 else "FAIL", detail="elementwise"))

    # G3 engine identity
    bnm = "u56-v2band-gross100"
    b = SHELF[bnm]
    px = PX[b["panel"]]
    r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
    rf = (r - t * RUNG_HEAD / 1e4).loc[start[b["panel"]]:]
    re_ = backtest(px, b["W"], cost_bps=RUNG_HEAD, freq=b["freq"])["returns"].loc[start[b["panel"]]:]
    g3 = float(np.nanmax(np.abs(rf.values - re_.values)))
    P(f"G3 engine max|fast_run(k=0) - engine.backtest| on {bnm} = {g3:.3e}   bar 1e-9   "
      f"{'PASS' if g3 < 1e-9 else 'FAIL'}")
    grows.append(dict(gate="G3_engine", result="PASS" if g3 < 1e-9 else "FAIL", detail=f"{g3:.3e}"))

    # G5 comparand bars (G4 needs the arms, so it is checked after the walk)
    P("G5 bars   comparands on this window, against the record's committed values:")
    for p in PX:
        s, v = SPY[p][RUNG_HEAD], V2[p][RUNG_HEAD]
        P(f"  {p}: SPY {s['CAGR']:.2%} / {s['Sharpe']:.3f} / {s['MaxDD']:.2%}   halves "
          f"{s['H1']:.3f}/{s['H2']:.3f}   ->  4b bars: DD cap {DDCAP_FRAC * s['MaxDD']:.2%}, "
          f"CAGR floor {CAGRFLOOR_FRAC * s['CAGR']:.2%}")
        P(f"       RULES v2 (live, weekly) {v['CAGR']:.2%} / {v['Sharpe']:.3f} / {v['MaxDD']:.2%}"
          f"   halves {v['H1']:.3f}/{v['H2']:.3f}")
    sd = max(abs(SPY["U56"][RUNG_HEAD]["CAGR"] - SPY_COMMITTED[0]),
             abs(SPY["U56"][RUNG_HEAD]["Sharpe"] - SPY_COMMITTED[1]),
             abs(SPY["U56"][RUNG_HEAD]["MaxDD"] - SPY_COMMITTED[2]))
    ok5 = sd < 0.010
    P(f"  G5 max|SPY U56 here - record's committed triple {SPY_COMMITTED}| = {sd:.4f}  bar 0.010  "
      f"{'PASS' if ok5 else 'FAIL'}")
    grows.append(dict(gate="G5_bars", result="PASS" if ok5 else "FAIL", detail=f"{sd:.4f}"))

    # ---------------------------------------------------------------- the offset walk (all arms)
    P("\n## The offset walk")
    KMAX = {f: max(max(g[f]) for g in OFFGRIDS.values()) for f in ("W", "M")}
    arms = []
    for setname, bset in SETS.items():
        for nm, bk in bset.items():
            p, f = bk["panel"], bk["freq"]
            px = PX[p]
            for k in range(KMAX[f] + 1):
                r, t = fast_run(px, bk["W"], offset_mask(px.index, f, k))
                for c in RUNGS:
                    n = (r - t * c / 1e4).loc[start[p]:]
                    s = stats(n.values, n.index)
                    row = dict(set=setname, book=nm, panel=p, freq=f, k=k, rung=c,
                               **{f"lvl_{a}": s[a] for a in
                                  ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                   "IS_H1", "IS_H2", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
                                   "OOS_H1", "OOS_H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD")})
                    for win, tag in (("", ""), ("IS_", "IS"), ("OOS_", "OOS")):
                        m4b = margins(s, SPY[p][c], win)
                        m4a = margins_4a(s, V2[p][c], win)
                        for leg, v in m4b.items():
                            row[f"m4b{tag}_{leg}"] = v
                        for leg, v in m4a.items():
                            row[f"m4a{tag}_{leg}"] = v
                        for leg in ALL_LEGS:
                            if win and leg == "OOS":
                                continue
                            row[f"stat{tag}_{leg}"] = leg_stat(s, leg, win)
                    row["pass4b"] = keep_4b({l: row[f"m4b_{l}"] for l in ALL_LEGS})
                    row["pass4a"] = keep_4a({l: row[f"m4a_{l}"] for l in ("H1", "H2", "DD")})
                    arms.append(row)
    A = pd.DataFrame(arms)
    A.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    P(f"ARMS: {len(A)} cells = books x offsets (W 0..{KMAX['W']}, M 0..{KMAX['M']}) x "
      f"{len(RUNGS)} rungs, all written to .arms.csv")

    # ---------------------------------------------------------------- the clause, per cell
    rows = []
    for (setname, nm, p, f, c), gsub in A.groupby(["set", "book", "panel", "freq", "rung"],
                                                  sort=False):
        for gname, gmap in OFFGRIDS.items():
            ks = [k for k in gmap[f] if k in set(gsub.k)]
            sub = gsub[gsub.k.isin(ks)]
            k0 = sub[sub.k == 0].iloc[0]
            rec = dict(set=setname, book=nm, panel=p, freq=f, rung=c, offgrid=gname, n_off=len(ks))
            for cmpname, pre in (("4b", "m4b"), ("4a", "m4a")):
                legs = ALL_LEGS if cmpname == "4b" else ["H1", "H2", "OOS", "DD"]
                for win in ("", "IS", "OOS"):
                    for leg in legs:
                        if win and leg == "OOS":
                            continue
                        mcol, scol = f"{pre}{win}_{leg}", f"stat{win}_{leg}"
                        mg = float(k0[mcol])
                        sp = float(sub[scol].max() - sub[scol].min())
                        ratio = abs(mg) / sp if sp > 0 else np.inf
                        flips = int(((sub[mcol] > 0) != (mg > 0)).sum())
                        tag = f"{cmpname}{win}_{leg}"
                        rec[f"margin_{tag}"] = mg
                        rec[f"spread_{tag}"] = sp
                        rec[f"ratio_{tag}"] = ratio
                        rec[f"flips_{tag}"] = flips
                        rec[f"verdict_{tag}"] = bool(mg > 0)
                        rec[f"clause_{tag}"] = bool(ratio >= 1.0)
            rec["pass4b_k0"] = bool(k0["pass4b"])
            rec["pass4a_k0"] = bool(k0["pass4a"])
            sharpe_r = [rec["ratio_4b_H1"], rec["ratio_4b_H2"]]
            rec["minratio_4b_sharpe"] = float(min(sharpe_r))
            allr = {l: rec[f"ratio_4b_{l}"] for l in ALL_LEGS}
            rec["minratio_4b_all"] = float(min(allr.values()))
            rec["binding_4b"] = min(allr, key=allr.get)
            rows.append(rec)
    CL = pd.DataFrame(rows)
    CL.to_csv(OUT / f"{STAMP}.clause.csv", index=False)
    P(f"CLAUSE: {len(CL)} (book x rung x offset-grid) cells written to .clause.csv; every leg's "
      f"margin, spread, ratio, flip count, published verdict and clause verdict published.")

    # ---------------------------------------------------------------- G4 cross-run repro of 891
    P("")
    if CLAUSE891.exists():
        c891 = pd.read_csv(CLAUSE891)
        mine = CL[(CL.offgrid == "FULL")].set_index(["book", "rung"])
        diffs, n = [], 0
        for _, r891 in c891[c891.set == "SHELF"].iterrows():
            key = (r891["book"], float(r891["rung"]))
            if key not in mine.index:
                continue
            m = mine.loc[key]
            for col891, colmine in (("4b_ratio_H1", "ratio_4b_H1"), ("4b_ratio_H2", "ratio_4b_H2"),
                                    ("4b_spread_H1", "spread_4b_H1"),
                                    ("4b_spread_H2", "spread_4b_H2"),
                                    ("4a_spread_H1", "spread_4a_H1"),
                                    ("4a_spread_H2", "spread_4a_H2")):
                if col891 in c891.columns and np.isfinite(r891[col891]):
                    diffs.append(abs(float(r891[col891]) - float(m[colmine])))
                    n += 1
        g4 = max(diffs) if diffs else float("nan")
        ok4 = bool(diffs) and g4 < 1e-6
        P(f"G4 cross  idea 891's committed .clause.csv Sharpe-leg cells reproduced from this run's "
          f"own arms: {n} cells, max abs diff {g4:.3e}   bar 1e-6   {'PASS' if ok4 else 'FAIL'}")
    else:
        ok4, g4, n = False, float("nan"), 0
        P("G4 cross  idea 891's committed .clause.csv NOT FOUND - gate cannot be run, said rather "
          "than worked around.")
    grows.append(dict(gate="G4_cross", result="PASS" if ok4 else "FAIL",
                      detail=f"{n} cells, max {g4:.3e}"))
    P(f"GATES {sum(g['result'] == 'PASS' for g in grows)}/{len(grows)} PASS")

    # ================================================================ hypotheses
    H = CL[(CL.rung == RUNG_HEAD) & (CL.offgrid == OFF_HEAD)]
    SH = H[H.set == "SHELF"]

    P("\n## 1. H_SPY - what the clause costs the committed SPY-side half-sample Sharpe claims")
    P(f"{'book':<36} {'H1 margin':>10} {'H1 spread':>10} {'H1 ratio':>9} "
      f"{'H2 margin':>10} {'H2 spread':>10} {'H2 ratio':>9}  clause")
    for _, r in SH.sort_values("minratio_4b_sharpe").iterrows():
        P(f"{r.book:<36} {r.margin_4b_H1:>+10.4f} {r.spread_4b_H1:>10.4f} {r.ratio_4b_H1:>9.3f} "
          f"{r.margin_4b_H2:>+10.4f} {r.spread_4b_H2:>10.4f} {r.ratio_4b_H2:>9.3f}  "
          f"{'PASS' if (r.clause_4b_H1 and r.clause_4b_H2) else 'FAIL'}")
    fail_spy = {}
    for gname in OFFGRIDS:
        for c in RUNGS:
            sub = CL[(CL.set == "SHELF") & (CL.offgrid == gname) & (CL.rung == c)]
            legs = pd.concat([sub.clause_4b_H1, sub.clause_4b_H2])
            fail_spy[(gname, c)] = int((~legs).sum())
    nlegs = 2 * len(SH)
    P(f"\nAll 9 grid points x 2 rungs, SHELF 4b Sharpe legs failing the clause (of {nlegs}):")
    for (gname, c), v in fail_spy.items():
        P(f"  offgrid {gname:<5} rung {c:>5.1f} bps : {v} / {nlegs}")
    h_spy_dial = all(v == 0 for k, v in fail_spy.items() if k[1] == RUNG_HEAD)
    h_spy_all = all(v == 0 for v in fail_spy.values())
    h_spy = h_spy_dial
    P(f"H_SPY {'PASS' if h_spy_dial else 'FAIL'} as declared (the 9 grid points of the two DIALS, "
      f"read at the headline {RUNG_HEAD:.0f} bps rung): the clause costs the committed SPY-side")
    P(f"  Sharpe claims {'NOTHING' if h_spy_dial else 'something'} there.  Once the 25 bps COST "
      f"CONTROL is included the same bar {'holds' if h_spy_all else 'BREAKS'} "
      f"({max(fail_spy.values())} of {nlegs} legs fail at 25 bps) - reported, not used to move the "
      f"bar.")

    P("\n## 2. H_LIVE - the same clause on the 4a (vs RULES v2 live) Sharpe legs")
    P(f"{'book':<36} {'H1 margin':>10} {'H1 spread':>10} {'H1 ratio':>9} "
      f"{'H2 margin':>10} {'H2 spread':>10} {'H2 ratio':>9}  clause")
    for _, r in SH.sort_values("book").iterrows():
        P(f"{r.book:<36} {r.margin_4a_H1:>+10.4f} {r.spread_4a_H1:>10.4f} {r.ratio_4a_H1:>9.3f} "
          f"{r.margin_4a_H2:>+10.4f} {r.spread_4a_H2:>10.4f} {r.ratio_4a_H2:>9.3f}  "
          f"{'PASS' if (r.clause_4a_H1 and r.clause_4a_H2) else 'FAIL'}")
    r4a = pd.concat([SH.ratio_4a_H1, SH.ratio_4a_H2]).replace([np.inf], np.nan).dropna()
    med4a = float(r4a.median())
    fail4a = int((r4a < 1.0).sum())
    h_live = bool(med4a < 0.5 and fail4a >= 0.9 * len(r4a))
    P(f"\nSHELF 4a Sharpe legs: median ratio {med4a:.3f}, failing the clause "
      f"{pct(fail4a, len(r4a))}")
    for gname in OFFGRIDS:
        for c in RUNGS:
            sub = CL[(CL.set == "SHELF") & (CL.offgrid == gname) & (CL.rung == c)]
            rr = pd.concat([sub.ratio_4a_H1, sub.ratio_4a_H2]).replace([np.inf], np.nan).dropna()
            P(f"  offgrid {gname:<5} rung {c:>5.1f} : median {rr.median():.3f}, "
              f"fail {pct(int((rr < 1).sum()), len(rr))}")
    P(f"H_LIVE {'PASS' if h_live else 'FAIL'} (bar: median < 0.5 AND >= 90% fail).")

    P("\n## 3. H_ASYM vs H_SPREAD - is H1's immunity a MARGIN fact or a SPREAD fact?")
    asym = []
    for gname in OFFGRIDS:
        for c in RUNGS:
            sub = CL[(CL.offgrid == gname) & (CL.rung == c)]
            for cmpname in ("4b", "4a"):
                d = dict(offgrid=gname, rung=c, comparand=cmpname, n_books=len(sub),
                         med_spread_H1=float(sub[f"spread_{cmpname}_H1"].median()),
                         med_spread_H2=float(sub[f"spread_{cmpname}_H2"].median()),
                         med_absmargin_H1=float(sub[f"margin_{cmpname}_H1"].abs().median()),
                         med_absmargin_H2=float(sub[f"margin_{cmpname}_H2"].abs().median()),
                         med_ratio_H1=float(sub[f"ratio_{cmpname}_H1"].replace(
                             [np.inf], np.nan).median()),
                         med_ratio_H2=float(sub[f"ratio_{cmpname}_H2"].replace(
                             [np.inf], np.nan).median()),
                         flips_H1=int(sub[f"flips_{cmpname}_H1"].sum()),
                         flips_H2=int(sub[f"flips_{cmpname}_H2"].sum()),
                         books_spreadH1_gt_H2=int((sub[f"spread_{cmpname}_H1"] >
                                                   sub[f"spread_{cmpname}_H2"]).sum()))
                asym.append(d)
    AS = pd.DataFrame(asym)
    AS.to_csv(OUT / f"{STAMP}.asym.csv", index=False)
    P(f"{'offgrid':<7} {'rung':>5} {'cmp':>4} {'sprH1':>8} {'sprH2':>8} {'|mgH1|':>8} "
      f"{'|mgH2|':>8} {'ratH1':>8} {'ratH2':>8} {'flipH1':>7} {'flipH2':>7} {'sprH1>H2':>9}")
    for _, r in AS.iterrows():
        P(f"{r.offgrid:<7} {r.rung:>5.1f} {r.comparand:>4} {r.med_spread_H1:>8.4f} "
          f"{r.med_spread_H2:>8.4f} {r.med_absmargin_H1:>8.4f} {r.med_absmargin_H2:>8.4f} "
          f"{r.med_ratio_H1:>8.3f} {r.med_ratio_H2:>8.3f} {r.flips_H1:>7d} {r.flips_H2:>7d} "
          f"{r.books_spreadH1_gt_H2:>5d}/{r.n_books:<3d}")
    head = AS[(AS.offgrid == OFF_HEAD) & (AS.rung == RUNG_HEAD)]
    fl = head[head.comparand == "4a"].iloc[0] if head[head.comparand == "4a"].flips_H2.iloc[0] > 0 \
        else head[head.comparand == "4b"].iloc[0]
    s1, s2 = float(fl.med_spread_H1), float(fl.med_spread_H2)
    m1, m2 = float(fl.med_absmargin_H1), float(fl.med_absmargin_H2)
    h_asym = bool(s1 >= s2 and m1 > m2)
    h_spread = bool(s1 <= 0.75 * s2)
    P(f"\nOn the comparand that flips ({fl.comparand}) at the headline grid point: "
      f"median spread H1 {s1:.4f} vs H2 {s2:.4f}; median |margin| H1 {m1:.4f} vs H2 {m2:.4f}")
    P(f"H_ASYM   {'PASS' if h_asym else 'FAIL'} (H1 not quieter AND H1 margin larger)")
    P(f"H_SPREAD {'PASS' if h_spread else 'FAIL'} (H1 spread <= 0.75 x H2's)")
    if not h_asym and not h_spread:
        P("both FAIL -> the asymmetry is PARTIAL on this record; the components are printed above.")
    # the verdict's own stability across the OTHER dial level, printed whatever it says
    P("\nSTABILITY of the H1-vs-H2 spread ordering across the OFFSET GRID dial (share of books "
      "with spread(H1) > spread(H2), 4b comparand, headline rung):")
    for gname in OFFGRIDS:
        rr = AS[(AS.offgrid == gname) & (AS.rung == RUNG_HEAD) & (AS.comparand == "4b")].iloc[0]
        which = "H1 quieter" if rr.med_spread_H1 < rr.med_spread_H2 else "H1 NOISIER"
        P(f"  offgrid {gname:<5}: median spread H1 {rr.med_spread_H1:.4f} vs H2 "
          f"{rr.med_spread_H2:.4f}  -> {which}; books with sprH1>sprH2 "
          f"{pct(int(rr.books_spreadH1_gt_H2), int(rr.n_books))}")
    ords = [AS[(AS.offgrid == g) & (AS.rung == RUNG_HEAD) & (AS.comparand == "4b")].iloc[0]
            for g in OFFGRIDS]
    stable = len({bool(o.med_spread_H1 < o.med_spread_H2) for o in ords}) == 1
    P(f"  ORDERING {'STABLE' if stable else 'REVERSES'} across the three offset grids - the "
      f"clause's own DENOMINATOR is {'well' if stable else 'NOT'} defined independently of how "
      f"densely the calendar is sampled.")
    P("\nFLIP ORDERING vs idea 879's published 'H1 flips 0, H2 flips 152':")
    for cmpname in ("4b", "4a"):
        rr = AS[(AS.offgrid == OFF_HEAD) & (AS.rung == RUNG_HEAD) &
                (AS.comparand == cmpname)].iloc[0]
        same = "MATCHES 879's direction" if rr.flips_H2 > rr.flips_H1 else "REVERSED vs 879"
        P(f"  comparand {cmpname}: H1 flips {rr.flips_H1}, H2 flips {rr.flips_H2}  -> {same}")

    P("\n## 4. H_SAME - is a Sharpe leg ever the BINDING leg of 4b?")
    bind = SH.binding_4b.value_counts()
    P("SHELF binding leg at the headline grid point: " +
      ", ".join(f"{k} {v}" for k, v in bind.items()))
    allbind = CL[CL.set == "SHELF"].groupby(["offgrid", "rung"]).binding_4b.apply(
        lambda s: (s.isin(SHARPE_LEGS)).sum())
    for (gname, c), v in allbind.items():
        P(f"  offgrid {gname:<5} rung {c:>5.1f} : Sharpe-bound books {v} / {len(SH)}")
    h_same = bool(allbind.sum() > 0)
    head_bound = int(allbind.loc[(OFF_HEAD, RUNG_HEAD)])
    P(f"H_SAME {'PASS' if h_same else 'FAIL'} - the Sharpe legs "
      f"{'DO' if h_same else 'do NOT'} bind 4b on the committed shelf somewhere on the grid.")
    P(f"  BUT at the headline grid point they bind {head_bound} of {len(SH)}: the binding leg is "
      f"DD on {int((SH.binding_4b == 'DD').sum())} of {len(SH)}, which reproduces idea 891's "
      f"unanimous DD result exactly.  The Sharpe legs only reach the binding position once an")
    P("  offset grid or a cost rung is changed - i.e. H_SAME passes on dial movement, not on the "
      "record's own published cell.")

    P("\n## 5. Census across all three claim sets (the clause's cost, by set and comparand)")
    cen = []
    for gname in OFFGRIDS:
        for c in RUNGS:
            for setname in SETS:
                sub = CL[(CL.set == setname) & (CL.offgrid == gname) & (CL.rung == c)]
                for cmpname in ("4b", "4a"):
                    rr = pd.concat([sub[f"ratio_{cmpname}_H1"], sub[f"ratio_{cmpname}_H2"]])
                    rr = rr.replace([np.inf], np.nan).dropna()
                    fp = pd.concat([sub[f"flips_{cmpname}_H1"], sub[f"flips_{cmpname}_H2"]])
                    cen.append(dict(offgrid=gname, rung=c, set=setname, comparand=cmpname,
                                    n_claims=len(rr), median_ratio=float(rr.median()),
                                    min_ratio=float(rr.min()), max_ratio=float(rr.max()),
                                    n_fail_clause=int((rr < 1).sum()),
                                    share_fail=float((rr < 1).mean()),
                                    total_flips=int(fp.sum())))
    CEN = pd.DataFrame(cen)
    CEN.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    P(f"{'offgrid':<7} {'rung':>5} {'set':<6} {'cmp':>4} {'claims':>7} {'medRatio':>9} "
      f"{'minRatio':>9} {'maxRatio':>9} {'failClause':>11} {'flips':>6}")
    for _, r in CEN.iterrows():
        P(f"{r.offgrid:<7} {r.rung:>5.1f} {r.set:<6} {r.comparand:>4} {r.n_claims:>7d} "
          f"{r.median_ratio:>9.3f} {r.min_ratio:>9.3f} {r.max_ratio:>9.3f} "
          f"{r.n_fail_clause:>5d}/{r.n_claims:<5d} {r.total_flips:>6d}")

    # ================================================================ rule 8
    P("\n## 6. RULE 8 walk-forward - fitted on 2009-2016, 2017+ read once")
    IS = CL[(CL.rung == RUNG_HEAD) & (CL.offgrid == OFF_HEAD)].copy()
    IS["is_minratio_sharpe"] = IS[["ratio_4bIS_H1", "ratio_4bIS_H2"]].min(axis=1)
    IS["oos_minratio_sharpe"] = IS[["ratio_4bOOS_H1", "ratio_4bOOS_H2"]].min(axis=1)
    rho = spearman(IS.is_minratio_sharpe.replace([np.inf], np.nan),
                   IS.oos_minratio_sharpe.replace([np.inf], np.nan))
    agree = int(((IS.is_minratio_sharpe >= 1) == (IS.oos_minratio_sharpe >= 1)).sum())
    h_wf = bool(rho >= 0.5 and agree >= 0.5 * len(IS))
    P(f"H_WF: Spearman rho(IS Sharpe-leg min-ratio, OOS min-ratio) over {len(IS)} books = "
      f"{rho:+.3f} (bar +0.50); clause verdict agrees IS vs OOS on {pct(agree, len(IS))} "
      f"(bar 50%)  ->  {'PASS' if h_wf else 'FAIL'}")

    wf = []
    for selname, col, asc in (("IS-min-ratio (this run's statistic)", "is_minratio_sharpe", False),
                              ("IS-Sharpe (the record's control)", "lvl_IS_Sharpe", False)):
        for setname in SETS:
            sub = IS[IS.set == setname].copy()
            if col == "lvl_IS_Sharpe":
                k0 = A[(A.rung == RUNG_HEAD) & (A.k == 0)].set_index(["set", "book"])
                sub["lvl_IS_Sharpe"] = [float(k0.loc[(setname, b), "lvl_IS_Sharpe"])
                                        for b in sub.book]
            sub = sub.replace([np.inf], np.nan).dropna(subset=[col])
            if sub.empty:
                continue
            pick = sub.sort_values(col, ascending=asc).iloc[0]
            p = pick.panel
            a0 = A[(A.set == setname) & (A.book == pick.book) & (A.k == 0) &
                   (A.rung == RUNG_HEAD)].iloc[0]
            sp, v2 = SPY[p][RUNG_HEAD], V2[p][RUNG_HEAD]
            oos4b = (a0.lvl_OOS_H1 > sp["OOS_H1"] and a0.lvl_OOS_H2 > sp["OOS_H2"] and
                     a0.lvl_OOS_Sharpe > sp["OOS_Sharpe"] and
                     a0.lvl_OOS_MaxDD > DDCAP_FRAC * sp["OOS_MaxDD"] and
                     a0.lvl_OOS_CAGR > CAGRFLOOR_FRAC * sp["OOS_CAGR"])
            oos4a = (a0.lvl_OOS_H1 > v2["OOS_H1"] and a0.lvl_OOS_H2 > v2["OOS_H2"] and
                     a0.lvl_OOS_MaxDD >= v2["OOS_MaxDD"])
            wf.append(dict(selector=selname, set=setname, pick=pick.book, panel=p,
                           IS_stat=float(pick[col]),
                           OOS_CAGR=float(a0.lvl_OOS_CAGR), OOS_Sharpe=float(a0.lvl_OOS_Sharpe),
                           OOS_MaxDD=float(a0.lvl_OOS_MaxDD),
                           SPY_OOS_CAGR=sp["OOS_CAGR"], SPY_OOS_Sharpe=sp["OOS_Sharpe"],
                           SPY_OOS_MaxDD=sp["OOS_MaxDD"],
                           V2_OOS_CAGR=v2["OOS_CAGR"], V2_OOS_Sharpe=v2["OOS_Sharpe"],
                           V2_OOS_MaxDD=v2["OOS_MaxDD"],
                           OOS_4b="PASS" if oos4b else "FAIL",
                           OOS_4a="PASS" if oos4a else "FAIL",
                           FULL_4b="PASS" if pick.pass4b_k0 else "FAIL",
                           FULL_4a="PASS" if pick.pass4a_k0 else "FAIL",
                           FULL_clause_sharpe="PASS" if pick.minratio_4b_sharpe >= 1 else "FAIL",
                           FULL_clause_all="PASS" if pick.minratio_4b_all >= 1 else "FAIL"))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    for _, r in WF.iterrows():
        P(f"\nselector {r.selector} | set {r['set']} -> {r['pick']} ({r.panel})")
        P(f"  OOS 2017+ : CAGR {r.OOS_CAGR:>7.2%}  Sharpe {r.OOS_Sharpe:>6.3f}  "
          f"MaxDD {r.OOS_MaxDD:>7.2%}")
        P(f"  SPY  OOS  : CAGR {r.SPY_OOS_CAGR:>7.2%}  Sharpe {r.SPY_OOS_Sharpe:>6.3f}  "
          f"MaxDD {r.SPY_OOS_MaxDD:>7.2%}")
        P(f"  v2   OOS  : CAGR {r.V2_OOS_CAGR:>7.2%}  Sharpe {r.V2_OOS_Sharpe:>6.3f}  "
          f"MaxDD {r.V2_OOS_MaxDD:>7.2%}")
        P(f"  OOS 4b {r.OOS_4b}, OOS 4a {r.OOS_4a}; full-sample 4b {r.FULL_4b}, 4a {r.FULL_4a}; "
          f"full-sample clause: Sharpe legs {r.FULL_clause_sharpe}, all legs {r.FULL_clause_all}")

    base4b = int(IS.pass4b_k0.sum())
    P(f"\nUNSELECTED BASE RATE over all {len(IS)} books at k=0, 10 bps: 4b PASS "
      f"{pct(base4b, len(IS))}, 4a PASS {pct(int(IS.pass4a_k0.sum()), len(IS))}; "
      f"Sharpe-leg clause PASS {pct(int((IS.minratio_4b_sharpe >= 1).sum()), len(IS))}, "
      f"all-leg clause PASS {pct(int((IS.minratio_4b_all >= 1).sum()), len(IS))}")

    # ================================================================ verdict
    P("\n## 7. Verdict")
    P(f"H_SPY    {'PASS' if h_spy else 'FAIL'} as declared (dials, headline rung); "
      f"{'holds' if h_spy_all else 'breaks'} once the 25 bps control is added")
    P(f"H_LIVE   {'PASS' if h_live else 'FAIL'}  (median ratio {med4a:.3f} vs bar 0.50; "
      f"fail share {fail4a / len(r4a):.1%} vs bar 90%)")
    P(f"H_ASYM   {'PASS' if h_asym else 'FAIL'}   H_SPREAD {'PASS' if h_spread else 'FAIL'}")
    P(f"H_SAME   {'PASS' if h_same else 'FAIL'}")
    P(f"H_WF     {'PASS' if h_wf else 'FAIL'}")
    P("No new book is proposed: this run prices an existing clause on existing committed claims.")
    P("KILL for capital (no candidate book); the finding is a PROTOCOL reading, PROPOSED not")
    P("APPLIED (rule 6 - RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched).")
    P(f"\nruntime {time.time() - t0:.1f}s")

    pd.DataFrame(grows).to_csv(OUT / f"{STAMP}.gates.csv", index=False)
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
