#!/usr/bin/env python3
"""
Idea 1254 (lane B, 2026-09-17) — is the 2026-09-04 KEEP 4b BOOK's OOS PASS CARRIED BY A
HANDFUL OF YEARS?

THE PREMISE.  The standing 4b candidate (committed 2026-09-04, re-confirmed by 1224 / 1237 /
1239 / 1240 / 1242 / 1243 / 1253 / 1255) states its capital case as ONE out-of-sample number:
U56, OOS 2017-2026 17.16% / 1.1759 / -19.13% against SPY OOS 15.15% / 0.8686 / -33.72%.  That
window holds ONE crash (2020, and 2022) and ONE melt-up (2023-2024).  If the whole OOS pass is
carried by two calendar years, the book is a regime bet the record is pricing as an edge.
This run deletes calendar years from the evaluation window and re-scores BOTH KEEP paths.

WHAT IS DELETED, AND WHAT IS NOT — STATED BEFORE ANY NUMBER IS READ.  The book is NOT rebuilt.
Positions are history; you cannot un-live a year.  What is deleted is the SCORING window: the
days of the deleted calendar years are removed from the daily return stream of the book, of
SPY, and of LIVE RULES v2 IDENTICALLY, and every leg (full / H1 / H2 / OOS) is recomputed by
compounding the surviving days in order.  This is a jackknife of the EVALUATION, which is the
object the 4b verdict is a function of.  Two consequences are stated up front and not hidden:
  (i) MaxDD on a spliced stream can SPAN the splice, and the direction is NOT one-sided as
      this script's first draft asserted: deleting a year can make drawdown look BETTER (its own
      trough is removed) or WORSE (two troughs on either side of the cut concatenate into one
      deeper drawdown that never happened).  The second is what the tape actually does here, so
      the spliced-DD leg is reported BUT NOT TRUSTED, and every DD verdict is published under
      TWO conventions at every grid point:
          DD_SPLICE  the naive one — compound the surviving days end to end (contaminated).
          DD_SEG     the splice-immune one — the worst drawdown WITHIN any contiguous surviving
                     segment, never spanning a cut.  This is the headline DD.
      DD_SEG is a measurement convention, not a third dial: both are computed on every subset
      and both are in the .grid.csv.
  (ii) H1/H2 are the halves of the SURVIVING days, so deleting OOS years moves the half split
      backwards.  Both halves are recomputed, never carried over.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    DELETION COUNT k  {0,1,2,3,4,5} — EXHAUSTIVE over every subset of that size.  Nothing is
                      searched and nothing is chosen: all 638 subsets per panel are published.
    PANEL             {U56, B136, SMALL663} (rule 9).
NOT DIALS, reported at every value: the deletion ARENA {OOS = the 10 years 2017..2026, the
question as asked; IS = the 8 years 2009..2016, the matched control that says whether the OOS
window is unusually fragile or whether EVERY window of this tape is}; the 4a and 4b legs; the
rule-8 windows.  Frozen at the record's construction and re-tuned by nothing here: composite
legs (21/252, 0/126, 0/63), NO vol scaler, above-own-200d and vol20 < 0.60 eligibility, N = 20,
min hold H = 126, GROSS = 0.75 of NAV with gated-out weight to CASH, calendar-weekly rebalance
(= the Monday-execution book, 1253 G9), 10 bps (rule 2), decide-at-t / apply-at-t+1, 260-row
warm-up.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) THE PASS IS BROAD — 4b survives every single-year deletion and the k at which the first
      subset kills it is >= 3, and the OOS Sharpe spread over single-year deletions is under
      0.15.  Then the committed number is a property of the decade, not of two years.
  (B) THE PASS IS YEAR-CARRIED — some SINGLE year's deletion kills 4b (k_first = 1).  Then the
      capital case rests on one year and the committed OOS figure should never be quoted
      without it.
  (C) THE PASS IS FRAGILE BUT NOT SINGLE-YEAR — k_first = 2, i.e. no one year carries it but a
      pair does.  Reported with WHICH pair, since the identity of the pair is the finding.
Whichever lands, the WORST-CASE 4b leg (the leg with the smallest margin, and the leg that
fails first) is reported at every k, because a pass that dies through CAGR is a different
object from one that dies through Sharpe.

RULE 8 (walk-forward), three parts, all reported:
  R8a  THE STANDARD REPORT.  Every grid point IS an out-of-sample report: the book's dials were
       frozen on the pre-2017 record and 2017-2026 is read once.  OOS CAGR / Sharpe / MaxDD for
       book vs LIVE RULES v2 baseline vs SPY is printed at k = 0 and at every deletion.
  R8b  THE MATCHED CONTROL.  The identical jackknife run on the IS arena (2009-2016).  If IS is
       just as fragile, year-carriage is a property of an 8-year sample, not of this book.
  R8c  THE DIAGNOSTIC'S OWN WALK-FORWARD.  The fragility statistic (worst single-year-deletion
       Sharpe drop) is computed on IS ONLY and used to PREDICT the OOS statistic, per panel.
       If IS fragility does not predict OOS fragility, the diagnostic carries no selection
       information and only the direct OOS reading counts.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 8 as
above; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL663 is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
upper bound.  This run's headline is a DIFFERENCE between scorings of the SAME book on the SAME
panel (with and without a year), which is first-order immune to a common level bias; the levels
are not, and 1255 has already priced the panel bias itself.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-17_is-the-2026-09-04-KEEP-4b-BOOK-s-OOS-PASS-CARRIED-BY-A-HANDFUL-OF-YEARS_B.py
"""
from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "is-the-2026-09-04-KEEP-4b-BOOK-s-OOS-PASS-CARRIED-BY-A-HANDFUL-OF-YEARS"
LANE = "B"
OUT = ROOT / "research" / "backtests"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75              # the frozen 2026-09-04 book
KMAX = 5                                   # DIAL 1: deletion count, exhaustive 0..KMAX
OOS_YEARS = list(range(2017, 2027))         # deletion arena OOS (the question as asked)
IS_YEARS = list(range(2009, 2017))          # deletion arena IS  (the matched control)
B4_LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name:<6} {'PASS' if ok else 'FAIL'}  value={value}  target={target}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def mdd_seg(r, keep):
    """Splice-immune MaxDD: worst drawdown inside any CONTIGUOUS run of surviving days, so a
    trough before a cut and a trough after it are never joined into a drawdown that never was.
    `keep` is the boolean survival mask on the ORIGINAL day axis; r is the surviving returns."""
    keep = np.asarray(keep, bool)
    brk = np.flatnonzero(np.diff(np.flatnonzero(keep)) > 1) + 1   # starts of new segments in r
    worst = 0.0
    for a, b in zip(np.append(0, brk), np.append(brk, len(r))):
        if b - a < 2:
            continue
        worst = min(worst, mdd(r[a:b]))
    return float(worst)


def stats(r, keep=None):
    d = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    d["MaxDD_seg"] = mdd_seg(r, keep) if keep is not None else d["MaxDD"]
    return d


def rankcorr(a, b):
    """Spearman rank correlation without scipy (average ranks, then Pearson)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def flat(w, pre=""):
    o = {}
    for k in ("full", "h1", "h2", "oos"):
        for m in ("CAGR", "Sharpe", "MaxDD", "MaxDD_seg"):
            o[f"{pre}{k}_{m}"] = w[k][m]
    return o


# ------------------------------------------------------------------ the frozen book
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, reb, N=A_N, H=A_H, lag=1):
    """Selection frame at GROSS = 1.0; row t is the APPLICATION-time weight (decided t-lag)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, reb, gross=A_G):
    """Hold gross*Wt from each rebalance date, drift between, 10 bps on traded notional."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(reb, np.append(reb[1:], T)):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


# ------------------------------------------------------------------ KEEP paths
def legs_4a(book, live, ddk="MaxDD_seg"):
    return dict(H1=book["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=book["full"][ddk] >= live["full"][ddk])


def legs_4b(book, spy, ddk="MaxDD_seg"):
    """4b under the SPLICE-IMMUNE drawdown by default (ddk='MaxDD_seg'); pass ddk='MaxDD'
    for the naive spliced convention. Both are published at every grid point."""
    return dict(H1=book["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=book["full"][ddk] >= DD_CAP * spy["full"][ddk],
                CAGR=book["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def margins_4b(book, spy, ddk="MaxDD_seg"):
    """Signed slack on each 4b leg; > 0 means the leg passes. Comparable across legs only
    in SIGN, not in units — Sharpe legs are Sharpe points, DD/CAGR are return fractions."""
    return dict(H1=book["h1"]["Sharpe"] - spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] - spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] - spy["oos"]["Sharpe"],
                DD=book["full"][ddk] - DD_CAP * spy["full"][ddk],
                CAGR=book["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"])


def windows(idx, r, keep=None):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    if keep is None:
        keep = np.ones(n, bool)
    kk = np.flatnonzero(np.asarray(keep, bool))          # original-axis positions of survivors
    def sub(a, b):
        m = np.zeros(len(keep), bool)
        m[kk[a:b]] = True
        return stats(r[a:b], m)
    return dict(full=sub(0, n), h1=sub(0, h), h2=sub(h, n), oos=sub(o, n), is_=sub(0, o))


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1254 lane {LANE} — {SLUG}")
    say("# frozen book: composite(21/252,0/126,0/63), NO vol scaler, above-200d & vol20<0.60,")
    say(f"# N={A_N}, H={A_H}, GROSS={A_G}, cash for gated-out weight, {COST:.0f} bps, t+1, calendar-W")
    say("# DIALS: k = deletion count 0..5 (EXHAUSTIVE subsets) x PANEL {U56,B136,SMALL}. "
        "ARENA {OOS 2017-26, IS 2009-16} reported at both values, not a dial.")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append(("B136", pb, [c for c in pb.columns if c != "SPY"]))
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in ps.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {ps.shape[1]-1} names, {len(bad & set(ps.columns))} dropped "
        f"for max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", ps, inv_s))

    rows, r8rows, killrows = [], [], []

    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        yr = idx.year.values

        r_book = run(pan, build(pan, pan.reb), pan.reb)[WARMUP:]
        r_spy = pan.spy[WARMUP:]
        r_live = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]

        say(f"\n{'='*104}\n## PANEL {pname}   window {idx[0].date()}..{idx[-1].date()}   "
            f"n_days={len(idx)}")

        def score(delete):
            """Re-score book / live / SPY on the surviving days after deleting calendar years."""
            m = ~np.isin(yr, list(delete)) if delete else np.ones(len(yr), bool)
            i2 = idx[m]
            bk, lv, sp = (windows(i2, r_book[m], m), windows(i2, r_live[m], m),
                          windows(i2, r_spy[m], m))
            a, b = legs_4a(bk, lv), legs_4b(bk, sp)            # DD_SEG (headline)
            bn = legs_4b(bk, sp, ddk="MaxDD")                  # naive spliced DD (published)
            return bk, lv, sp, a, b, margins_4b(bk, sp), int(m.sum()), bn

        # ---------------- k = 0, the committed reading (R8a standard report)
        bk0, lv0, sp0, a0, b0, m0, n0, bn0 = score(())
        say(f"   SPY        full {sp0['full']['CAGR']:7.2%} / {sp0['full']['Sharpe']:.4f} / "
            f"{sp0['full']['MaxDD']:7.2%}   halves {sp0['h1']['Sharpe']:.4f}/{sp0['h2']['Sharpe']:.4f}"
            f"   OOS {sp0['oos']['CAGR']:7.2%} / {sp0['oos']['Sharpe']:.4f} / {sp0['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2    full {lv0['full']['CAGR']:7.2%} / {lv0['full']['Sharpe']:.4f} / "
            f"{lv0['full']['MaxDD']:7.2%}   halves {lv0['h1']['Sharpe']:.4f}/{lv0['h2']['Sharpe']:.4f}"
            f"   OOS {lv0['oos']['CAGR']:7.2%} / {lv0['oos']['Sharpe']:.4f} / {lv0['oos']['MaxDD']:7.2%}")
        say(f"   BOOK k=0   full {bk0['full']['CAGR']:7.2%} / {bk0['full']['Sharpe']:.4f} / "
            f"{bk0['full']['MaxDD']:7.2%}   halves {bk0['h1']['Sharpe']:.4f}/{bk0['h2']['Sharpe']:.4f}"
            f"   OOS {bk0['oos']['CAGR']:7.2%} / {bk0['oos']['Sharpe']:.4f} / {bk0['oos']['MaxDD']:7.2%}")
        say("   (at k=0 nothing is deleted, so DD_SEG == DD_SPLICE by construction: "
            f"{bk0['full']['MaxDD_seg']:7.2%} == {bk0['full']['MaxDD']:7.2%})")
        say(f"   k=0 verdicts: 4a={all(a0.values())} {a0}   4b={all(b0.values())} {b0}")
        say(f"   k=0 4b margins: " + "  ".join(f"{k}{m0[k]:+.4f}" for k in B4_LEGS)
            + f"   4b DD cap {DD_CAP*sp0['full']['MaxDD']:7.2%}  CAGR floor {CAGR_FLOOR*sp0['full']['CAGR']:7.2%}")

        if pname == "U56":
            gate("G1", f"{bk0['oos']['CAGR']:.4f}/{bk0['oos']['Sharpe']:.4f}/{bk0['oos']['MaxDD']:.4f}",
                 "0.1716/1.1759/-0.1913 +/- 0.005",
                 abs(bk0["oos"]["CAGR"] - 0.1716) < 5e-3 and abs(bk0["oos"]["Sharpe"] - 1.1759) < 5e-3
                 and abs(bk0["oos"]["MaxDD"] + 0.1913) < 5e-3)
            gate("G2", f"{sp0['oos']['CAGR']:.4f}/{sp0['oos']['Sharpe']:.4f}/{sp0['oos']['MaxDD']:.4f}",
                 "0.1515/0.8686/-0.3372 +/- 0.005",
                 abs(sp0["oos"]["CAGR"] - 0.1515) < 5e-3 and abs(sp0["oos"]["Sharpe"] - 0.8686) < 5e-3
                 and abs(sp0["oos"]["MaxDD"] + 0.3372) < 5e-3)
            gate("G3", f"{lv0['full']['MaxDD']:.4f}", "live v2 -0.1205 +/- 0.005",
                 abs(lv0["full"]["MaxDD"] + 0.1205) < 5e-3)
            gate("G4", f"4b(k=0)={all(b0.values())}", "True (the committed pass replays)",
                 all(b0.values()))

        # ---------------- the two arenas
        for arena, years in (("OOS", OOS_YEARS), ("IS", IS_YEARS)):
            say(f"\n   --- ARENA {arena}: deleting from {years[0]}..{years[-1]} "
                f"({len(years)} years) ---")
            per_k = {}
            first_kill_4b = None
            first_kill_4a = None
            for k in range(0, KMAX + 1):
                if k > len(years):
                    break
                cells = []
                for combo in itertools.combinations(years, k):
                    bk, lv, sp, a, b, mg, nd, bn = score(combo)
                    p4a, p4b, p4b_naive = all(a.values()), all(b.values()), all(bn.values())
                    cells.append(dict(combo=combo, bk=bk, sp=sp, a=a, b=b, mg=mg, p4a=p4a,
                                      p4b=p4b, p4bn=p4b_naive))
                    rows.append(dict(panel=pname, arena=arena, k=k,
                                     deleted="+".join(str(y) for y in combo) or "NONE",
                                     n_days=nd, **flat(bk), **flat(sp, "spy_"),
                                     **{f"a_{x}": v for x, v in a.items()},
                                     **{f"b_{x}": v for x, v in b.items()},
                                     **{f"marg_{x}": mg[x] for x in B4_LEGS},
                                     **{f"bnaive_{x}": v for x, v in bn.items()},
                                     pass4a=p4a, pass4b=p4b, pass4b_spliceDD=p4b_naive,
                                     fail4b_legs="+".join(x for x in B4_LEGS if not b[x]) or "NONE",
                                     fail4b_spliceDD_legs="+".join(x for x in B4_LEGS if not bn[x]) or "NONE"))
                    if not p4b and first_kill_4b is None:
                        first_kill_4b = (k, combo, dict(b))
                    if not p4a and first_kill_4a is None:
                        first_kill_4a = (k, combo, dict(a))
                per_k[k] = cells
                n_pass = sum(c["p4b"] for c in cells)
                n_pass_n = sum(c["p4bn"] for c in cells)
                n_pass_a = sum(c["p4a"] for c in cells)
                so = np.array([c["bk"]["oos"]["Sharpe"] for c in cells])
                sf = np.array([c["bk"]["full"]["Sharpe"] for c in cells])
                co = np.array([c["bk"]["full"]["CAGR"] for c in cells])
                # worst-case 4b leg at this k = the leg with the smallest minimum margin
                worst_leg = min(B4_LEGS, key=lambda x: min(c["mg"][x] for c in cells))
                worst_val = min(min(c["mg"][x] for c in cells) for x in [worst_leg])
                say(f"   k={k}  subsets {len(cells):4d}   4b PASS {n_pass:4d}/{len(cells):<4d} "
                    f"(spliced-DD convention {n_pass_n:4d}/{len(cells):<4d})   "
                    f"4a PASS {n_pass_a:4d}/{len(cells):<4d}   book OOS Sharpe "
                    f"{so.min():.4f}..{so.max():.4f} (spread {so.max()-so.min():.4f})   "
                    f"full Sharpe {sf.min():.4f}..{sf.max():.4f}   full CAGR {co.min():6.2%}..{co.max():6.2%}"
                    f"   TIGHTEST 4b LEG = {worst_leg} (min margin {worst_val:+.4f})")
                if k == 1:
                    for c in sorted(cells, key=lambda c: c["bk"]["oos"]["Sharpe"]):
                        y = c["combo"][0]
                        say(f"        drop {y}: full {c['bk']['full']['CAGR']:7.2%} / "
                            f"{c['bk']['full']['Sharpe']:.4f} / DDseg {c['bk']['full']['MaxDD_seg']:7.2%} "
                            f"(spliced {c['bk']['full']['MaxDD']:7.2%})  "
                            f"halves {c['bk']['h1']['Sharpe']:.4f}/{c['bk']['h2']['Sharpe']:.4f}  "
                            f"OOS {c['bk']['oos']['CAGR']:7.2%} / {c['bk']['oos']['Sharpe']:.4f} / "
                            f"{c['bk']['oos']['MaxDD_seg']:7.2%}  SPY OOS Sh {c['sp']['oos']['Sharpe']:.4f}  "
                            f"4a={c['p4a']} 4b={c['p4b']} (spliced-DD {c['p4bn']})  fails: "
                            f"{'+'.join(x for x in B4_LEGS if not c['b'][x]) or 'NONE'}")
                if n_pass < len(cells):
                    bad_cells = [c for c in cells if not c["p4b"]]
                    from collections import Counter
                    cnt = Counter(x for c in bad_cells for x in B4_LEGS if not c["b"][x])
                    yc = Counter(y for c in bad_cells for y in c["combo"])
                    say(f"        of the {len(bad_cells)} FAILING subsets, legs that fail: "
                        f"{dict(cnt)};  years most often present: "
                        f"{[f'{y}x{n}' for y, n in yc.most_common(4)]}")

            kf = first_kill_4b[0] if first_kill_4b else None
            say(f"   ARENA {arena}: FIRST k at which ANY subset kills 4b = "
                f"{kf if kf is not None else f'>{KMAX} (never within k<={KMAX})'}"
                + (f"   via {first_kill_4b[1]} failing "
                   f"{[x for x in B4_LEGS if not first_kill_4b[2][x]]}" if first_kill_4b else ""))
            # k at which the pass dies for EVERY subset of that size
            k_all = next((k for k in sorted(per_k) if k > 0
                          and not any(c["p4b"] for c in per_k[k])), None)
            say(f"   ARENA {arena}: FIRST k at which EVERY subset kills 4b = "
                f"{k_all if k_all is not None else f'>{KMAX}'}")
            killrows.append(dict(panel=pname, arena=arena, k_first_any_4b=kf,
                                 k_first_all_4b=k_all,
                                 k_first_any_4a=first_kill_4a[0] if first_kill_4a else None,
                                 first_kill_set="+".join(str(y) for y in first_kill_4b[1])
                                 if first_kill_4b else "",
                                 k1_oos_sharpe_spread=float(
                                     max(c["bk"]["oos"]["Sharpe"] for c in per_k[1])
                                     - min(c["bk"]["oos"]["Sharpe"] for c in per_k[1])),
                                 k1_worst_year=min(per_k[1], key=lambda c: c["bk"]["oos"]["Sharpe"])["combo"][0],
                                 k1_worst_oos_sharpe=float(
                                     min(c["bk"]["oos"]["Sharpe"] for c in per_k[1])),
                                 k1_n_pass_4b=int(sum(c["p4b"] for c in per_k[1])),
                                 k1_n_pass_4b_spliceDD=int(sum(c["p4bn"] for c in per_k[1])),
                                 k_first_any_4b_spliceDD=next(
                                     (k for k in sorted(per_k) if any(not c["p4bn"] for c in per_k[k])),
                                     None),
                                 k1_n=len(per_k[1])))
            if arena == "OOS":
                oos_frag = float(bk0["oos"]["Sharpe"] - min(c["bk"]["oos"]["Sharpe"] for c in per_k[1]))
                oos_k1 = {c["combo"][0]: c["bk"]["oos"]["Sharpe"] for c in per_k[1]}
            else:
                is_frag = float(bk0["is_"]["Sharpe"]
                                - min(stats(r_book[~np.isin(yr, [c["combo"][0]])
                                                   & (yr < 2017)])["Sharpe"] for c in per_k[1]))
                is_k1 = {c["combo"][0]: stats(r_book[~np.isin(yr, [c["combo"][0]]) & (yr < 2017)])["Sharpe"]
                         for c in per_k[1]}

        # ---------------- R8b / R8c
        say(f"\n   RULE 8b  {pname}: worst single-year-deletion Sharpe DROP — "
            f"IS arena {is_frag:+.4f} (from IS Sharpe {bk0['is_']['Sharpe']:.4f}) vs "
            f"OOS arena {oos_frag:+.4f} (from OOS Sharpe {bk0['oos']['Sharpe']:.4f})   "
            f"ratio OOS/IS {oos_frag/is_frag if is_frag else float('nan'):+.3f}")
        say(f"   RULE 8c  {pname}: IS-window year fragility ranking predicts OOS? "
            f"IS per-year worst = {min(is_k1, key=is_k1.get)}, OOS per-year worst = "
            f"{min(oos_k1, key=oos_k1.get)}  (different windows, disjoint year sets — "
            f"the IS ranking cannot name an OOS year, so the diagnostic is NOT transferable "
            f"and only the direct OOS reading counts)")
        r8rows.append(dict(panel=pname, is_sharpe=bk0["is_"]["Sharpe"], oos_sharpe=bk0["oos"]["Sharpe"],
                           oos_cagr=bk0["oos"]["CAGR"], oos_mdd=bk0["oos"]["MaxDD"],
                           spy_oos_sharpe=sp0["oos"]["Sharpe"], spy_oos_cagr=sp0["oos"]["CAGR"],
                           spy_oos_mdd=sp0["oos"]["MaxDD"], live_oos_sharpe=lv0["oos"]["Sharpe"],
                           live_oos_cagr=lv0["oos"]["CAGR"], live_oos_mdd=lv0["oos"]["MaxDD"],
                           is_worst_drop=is_frag, oos_worst_drop=oos_frag,
                           is_worst_year=min(is_k1, key=is_k1.get),
                           oos_worst_year=min(oos_k1, key=oos_k1.get),
                           is_oos_frag_ratio=oos_frag / is_frag if is_frag else float("nan")))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{DATE}_{SLUG}_{LANE}.grid.csv", index=False)
    pd.DataFrame(r8rows).to_csv(OUT / f"{DATE}_{SLUG}_{LANE}.walkforward.csv", index=False)
    pd.DataFrame(killrows).to_csv(OUT / f"{DATE}_{SLUG}_{LANE}.kill.csv", index=False)
    pd.DataFrame(GATES).to_csv(OUT / f"{DATE}_{SLUG}_{LANE}.gates.csv", index=False)

    say(f"\n{'='*104}\n## SUMMARY — all {len(df)} grid points published in .grid.csv")
    say(pd.DataFrame(killrows).to_string(index=False))
    say(f"\n## GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
    say(f"\nran in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
