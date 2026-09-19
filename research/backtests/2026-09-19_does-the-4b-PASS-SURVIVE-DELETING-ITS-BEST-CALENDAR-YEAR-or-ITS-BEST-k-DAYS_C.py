#!/usr/bin/env python3
"""
Idea 1690 (lane C, 2026-09-19) — does the 4b PASS survive DELETING its BEST CALENDAR YEAR
or its BEST k DAYS?

THE DEFECT THIS ATTACKS.  Idea 1590 found the standing 2026-09-04 KEEP-4b candidate robust to
120 bps of cost yet DEAD to one day of execution latency: its 4b margins are thin in ways the
cost axis cannot see.  The cheapest way to see how thin is to take the tape away from it a
piece at a time and ask which leg breaks first, and after how little.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.  The book is NOT rebuilt — positions are
history.  What is deleted is the SCORING WINDOW: a set of days is removed from the daily return
stream of the BOOK, of SPY and of LIVE RULES v2 IDENTICALLY, and all four 4b legs (Sharpe > SPY
in both halves, Sharpe > SPY OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) plus the three
4a legs are recomputed on the surviving days.  Because SPY loses the same days, THE BAR MOVES
WITH THE TAPE — which is the whole point of the idea and the reason a "best day" deletion is
not simply a handicap.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    UNIT {YEAR, DAY_BOOK, DAY_SPY, DAY_ADV} — what a single deletion removes.
        YEAR     a whole calendar year, chosen ADVERSARIALLY (greedy: at each step take the
                 year that most erodes the book's weakest surviving 4b margin).  k = 1 is
                 ALSO published EXHAUSTIVELY over every calendar year in the window.
        DAY_BOOK the k days of largest BOOK return (the classic "missing the best days" cut).
        DAY_SPY  the k days of largest SPY return (the bar's own best days).
        DAY_ADV  greedy adversarial single days — the true "smallest deletion that flips".
    k    0..6 (YEAR), 0..20 (DAY_BOOK / DAY_SPY), 0..10 (DAY_ADV).  EVERY rung published.

NOT DIALS, reported at every rung: PANEL {U56, B136, SMALL} (rule 9); CONVENTION {SPLICE, ZERO};
BAR {MOVES, FROZEN}; the 4a legs; the five 4b margins; the rule-8 halves.

THE CONVENTION PROBLEM, AND WHY TWO ARE PUBLISHED.  Idea 1254 published a method error worth
inheriting: deleting days and concatenating what is left can MANUFACTURE a drawdown that never
happened (its 2019 cut spliced the Q4-2018 and Q1-2020 troughs into -27.24% against a true
-19.13%).  Its fix was DD_SEG — the worst drawdown WITHIN a contiguous surviving segment, never
spanning a cut.  DD_SEG is right for YEAR deletions, which make one long cut.  It is WRONG for
scattered single-day deletions: the book's best days sit inside its deepest drawdowns, so a
splice cuts the drawdown path exactly where it hurts and DD_SEG then flatters the book by
construction.  This run therefore publishes BOTH:
    SPLICE  drop the day from the stream; MaxDD = DD_SEG (1254's convention).  HEADLINE for YEAR.
    ZERO    set that day's return to 0.0 in all three streams; the calendar, the compounding
            path and the drawdown path stay contiguous and the CAGR denominator is unchanged.
            This is the classic missing-the-best-days counterfactual.  HEADLINE for DAY_*.
Neither convention is a dial: every cell is computed and published under both.

THE BAR ARM.  BAR = MOVES is the idea's literal construction (SPY loses the same days).
BAR = FROZEN deletes from the BOOK only and holds SPY's k = 0 bar fixed — the naive read.  The
gap between them is how much of the book's survival is the bar moving rather than the book
holding, and it is published at every rung rather than argued about.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: the 2026-09-04 candidate —
composite legs (21/252, 0/126, 0/63) RAW with NO vol scaler, eligibility = above own 200d MA AND
vol20 < 0.60, top N = 20 equal weight, H = 126 minimum hold, GROSS = 0.75 of NAV with gated-out
weight to CASH, WEEKLY rebalance, 10 bps (rule 2), decide-at-t / apply-at-t+1, 260-row warm-up.

OVERLAP WITH THE COMMITTED RECORD, DECLARED BEFORE ANY NUMBER IS READ (this is not a new
finding and is not claimed as one).  Idea 1254 ran the CALENDAR-YEAR half over the TEN OOS years
2017..2026, exhaustively to k = 5, and found the RETURN side not year-carried and the DRAWDOWN
side carried by 2020 alone.  Idea 1255 ran the NAME half.  The year arm here is run as a
CROSS-RUN GATE against 1254's committed numbers (G3/G4) and as the adversarial-depth framing
1254 did not report; the genuinely unpriced axis, and this run's headline, is the DAY axis.

RULE 8 (walk-forward).  The fragility measure is computed on warm-up..2016-12-31 ONLY and
2017-2026 is read ONCE.  The legal IS-only chooser is over PANEL: trade the panel whose IS book
has the DEEPEST flip-depth (the most deletion-robust IS book) under each unit.  Reported against
(i) the do-nothing anchor (U56, no deletion), (ii) the mean over the three panels, (iii) the
WORST panel, with the IS/OOS rank correlation of flip-depth over the 12 (panel, unit) pairs.
IS has no OOS leg, so the IS 4b test is its four available legs (both IS halves, DD, CAGR) and
the OOS 4b test is the four legs computable on 2017-2026 (both OOS halves, DD, CAGR); this is
stated, not silently substituted.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before
anything is computed).  Every absolute level printed here is optimistic.  A current-constituent
panel is KIND TO THE BEST-DAY CUT in particular: the names a momentum screen piles into are
disproportionately the survivors, so the book's biggest up-days are over-represented relative to
a real tape, and the DAY_BOOK fragility reported here is therefore an UPPER bound on robustness.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_does-the-4b-PASS-SURVIVE-DELETING-ITS-BEST-CALENDAR-YEAR-or-ITS-BEST-k-DAYS_C.py
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

DATE = "2026-09-19"
SLUG = "does-the-4b-PASS-SURVIVE-DELETING-ITS-BEST-CALENDAR-YEAR-or-ITS-BEST-k-DAYS"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75               # the frozen 2026-09-04 book
K_YEAR, K_DAY, K_ADV = 6, 20, 10            # DIAL 2 ranges
UNITS = ["YEAR", "DAY_BOOK", "DAY_SPY", "DAY_ADV"]   # DIAL 1
CONVS = ["SPLICE", "ZERO"]
BARS = ["MOVES", "FROZEN"]
COMMITTED_U56_BOOK = (0.1571, 1.1480, -0.1913)   # 1254/1258 committed anchor triple
COMMITTED_U56_SPY = (0.1506, 0.8815, -0.3372)    # 1254 committed SPY triple
COMMITTED_U56_LIVE = (0.0860, 1.1982, -0.1205)   # 1254 committed LIVE v2 triple
COMMITTED_END = pd.Timestamp("2026-09-16")       # 1254's tape end; ours is 2 sessions longer
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd_plain(r):
    if len(r) < 2:
        return float("nan")
    e = np.cumprod(1.0 + r)
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def mdd_seg(r, keep):
    """1254's DD_SEG: worst drawdown WITHIN a contiguous surviving segment, never spanning a
    cut.  r is the SURVIVING stream; keep is the boolean mask that produced it.  Segment count
    is (number of cuts + 1), so the loop is over a handful of slices, not over days."""
    if len(r) < 2:
        return float("nan")
    ki = np.flatnonzero(np.asarray(keep))
    if len(ki) != len(r):
        return float("nan")
    brk = np.flatnonzero(np.diff(ki) > 1) + 1
    bounds = np.concatenate([[0], brk, [len(r)]])
    worst = 0.0
    for a, b in zip(bounds[:-1], bounds[1:]):
        if b - a < 2:
            continue
        e = np.cumprod(1.0 + r[a:b])
        worst = min(worst, float((e / np.maximum.accumulate(e) - 1.0).min()))
    return worst


def triple(r, keep=None, seg=False):
    r = np.asarray(r, float)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r),
                MaxDD=(mdd_seg(r, keep) if seg else mdd_plain(r)))


# ------------------------------------------------------------------ deletion engine
class Streams:
    """Post-warm-up daily returns of the book, SPY and LIVE RULES v2 on one panel, plus the
    machinery to delete a set of days from all three identically."""

    def __init__(self, idx, book, spy, live):
        self.idx = idx
        self.book, self.spy, self.live = book, spy, live
        self.year = np.asarray(idx.year)
        self.years = sorted(set(self.year.tolist()))
        self.oos = np.asarray(idx >= OOS_START)
        self.is_ = ~self.oos

    def slice(self, sel):
        """Restrict to a sub-window (IS or OOS or FULL) and return a fresh Streams."""
        return Streams(self.idx[sel], self.book[sel], self.spy[sel], self.live[sel])

    # -- evaluation -------------------------------------------------
    def eval(self, keep, conv, bar="MOVES"):
        """Recompute every window for all three streams under one convention.
        keep: boolean mask over self.idx (True = day survives)."""
        if conv == "SPLICE":
            k = keep
            bo, sp, lv = self.book[k], self.spy[k], self.live[k]
            oos = self.oos[k]
            n = len(bo)
            h = n // 2
            seg = True
            kk = keep
            if bar == "FROZEN":
                sp_full = self.spy
                sp_oos = self.oos
                sp_n = len(sp_full)
                sp_h = sp_n // 2
                spy_w = dict(full=triple(sp_full), h1=triple(sp_full[:sp_h]),
                             h2=triple(sp_full[sp_h:]), oos=triple(sp_full[sp_oos]))
            else:
                spy_w = dict(full=triple(sp, kk, True), h1=triple(sp[:h]), h2=triple(sp[h:]),
                             oos=triple(sp[oos]))
            book_w = dict(full=triple(bo, kk, seg), h1=triple(bo[:h]), h2=triple(bo[h:]),
                          oos=triple(bo[oos]))
            live_w = dict(full=triple(lv, kk, seg), h1=triple(lv[:h]), h2=triple(lv[h:]),
                          oos=triple(lv[oos]))
        else:  # ZERO
            z = ~keep
            bo = np.where(z, 0.0, self.book)
            sp = self.spy if bar == "FROZEN" else np.where(z, 0.0, self.spy)
            lv = np.where(z, 0.0, self.live)
            oos = self.oos
            n = len(bo)
            h = n // 2
            book_w = dict(full=triple(bo), h1=triple(bo[:h]), h2=triple(bo[h:]), oos=triple(bo[oos]))
            spy_w = dict(full=triple(sp), h1=triple(sp[:h]), h2=triple(sp[h:]), oos=triple(sp[oos]))
            live_w = dict(full=triple(lv), h1=triple(lv[:h]), h2=triple(lv[h:]), oos=triple(lv[oos]))
        return book_w, spy_w, live_w


def margins_4b(b, s, with_oos=True):
    m = {"H1": b["h1"]["Sharpe"] - s["h1"]["Sharpe"],
         "H2": b["h2"]["Sharpe"] - s["h2"]["Sharpe"],
         "DD": b["full"]["MaxDD"] - DD_CAP * s["full"]["MaxDD"],
         "CAGR": b["full"]["CAGR"] - CAGR_FLOOR * s["full"]["CAGR"]}
    if with_oos:
        m["OOS"] = b["oos"]["Sharpe"] - s["oos"]["Sharpe"]
    return m


def margins_4a(b, l):
    return {"H1": b["h1"]["Sharpe"] - l["h1"]["Sharpe"],
            "H2": b["h2"]["Sharpe"] - l["h2"]["Sharpe"],
            "DD": b["full"]["MaxDD"] - l["full"]["MaxDD"]}


def passes(m):
    return all(v > 0 if k in ("H1", "H2", "OOS") else v >= 0 for k, v in m.items())


def failing(m):
    return ",".join(k for k, v in m.items()
                    if not (v > 0 if k in ("H1", "H2", "OOS") else v >= 0)) or "-"


def weakest_rel(m, m0):
    """min over legs of margin / |anchor margin| — the adversary's objective.  Scale-free, so
    Sharpe-unit and pp-unit legs are comparable; < 0 means that leg has flipped."""
    vals = []
    for k, v in m.items():
        d = abs(m0.get(k, np.nan))
        if not np.isfinite(d) or d < 1e-12:
            d = 1.0
        vals.append(v / d)
    return float(min(vals)) if vals else np.nan


# ------------------------------------------------------------------ panel / book
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        self.invest = invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values          # RAW composite (no vol scaler)
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.elig = self.above & self.volok
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, N=A_N, H=A_H, lag=1):
    """The frozen 2026-09-04 selection frame at GROSS = 1.0 (identical to the committed
    anchor arm of 1258 at CAP = 20, i.e. no cap)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            for c in order:
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = pan.reb[i + 1] if i + 1 < nreb else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_book(pan, Wt, gross=A_G):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
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


# ------------------------------------------------------------------ deletion ladders
def year_masks(st, years):
    m = np.ones(len(st.idx), bool)
    for y in years:
        m &= st.year != y
    return m


def ladder_rows(st, unit, conv, bar, panel, arena, kmax, m0_cache):
    """Walk k = 0..kmax under one (unit, conv, bar) and return one row per rung plus the
    ordered deletion path."""
    rows = []
    n = len(st.idx)
    keep = np.ones(n, bool)
    chosen: list = []
    with_oos = arena == "FULL"
    b0, s0, l0 = st.eval(np.ones(n, bool), conv, bar)
    m0 = margins_4b(b0, s0, with_oos)
    a0 = margins_4a(b0, l0)
    m0_cache[(panel, unit, conv, bar, arena)] = m0

    if unit == "DAY_BOOK":
        order = list(np.argsort(-st.book))
    elif unit == "DAY_SPY":
        order = list(np.argsort(-st.spy))
    else:
        order = None

    for k in range(kmax + 1):
        if k > 0:
            if unit == "YEAR":
                best, bestv = None, np.inf
                for y in st.years:
                    if y in chosen:
                        continue
                    trial = keep & (st.year != y)
                    if trial.sum() < 300:
                        continue
                    b, s, l = st.eval(trial, conv, bar)
                    v = weakest_rel(margins_4b(b, s, with_oos), m0)
                    if v < bestv:
                        best, bestv = y, v
                if best is None:
                    break
                chosen.append(best)
                keep = keep & (st.year != best)
            elif unit == "DAY_ADV":
                cand = np.flatnonzero(keep)
                best, bestv = None, np.inf
                for c in cand:
                    keep[c] = False
                    b, s, l = st.eval(keep, conv, bar)
                    v = weakest_rel(margins_4b(b, s, with_oos), m0)
                    keep[c] = True
                    if v < bestv:
                        best, bestv = int(c), v
                if best is None:
                    break
                chosen.append(str(st.idx[best].date()))
                keep[best] = False
            else:
                d = order[k - 1]
                chosen.append(str(st.idx[d].date()))
                keep[d] = False
        b, s, l = st.eval(keep, conv, bar)
        m4b = margins_4b(b, s, with_oos)
        m4a = margins_4a(b, l)
        rows.append(dict(
            panel=panel, arena=arena, unit=unit, conv=conv, bar=bar, k=k,
            n_days=int(keep.sum()), deleted=("|".join(str(x) for x in chosen) if chosen else "-"),
            book_CAGR=b["full"]["CAGR"], book_Sharpe=b["full"]["Sharpe"], book_MaxDD=b["full"]["MaxDD"],
            book_H1=b["h1"]["Sharpe"], book_H2=b["h2"]["Sharpe"],
            book_oCAGR=b["oos"]["CAGR"], book_oSharpe=b["oos"]["Sharpe"], book_oMaxDD=b["oos"]["MaxDD"],
            spy_CAGR=s["full"]["CAGR"], spy_Sharpe=s["full"]["Sharpe"], spy_MaxDD=s["full"]["MaxDD"],
            spy_H1=s["h1"]["Sharpe"], spy_H2=s["h2"]["Sharpe"], spy_oSharpe=s["oos"]["Sharpe"],
            live_CAGR=l["full"]["CAGR"], live_Sharpe=l["full"]["Sharpe"], live_MaxDD=l["full"]["MaxDD"],
            live_H1=l["h1"]["Sharpe"], live_H2=l["h2"]["Sharpe"], live_oSharpe=l["oos"]["Sharpe"],
            **{f"m4b_{kk}": v for kk, v in m4b.items()},
            **{f"m4a_{kk}": v for kk, v in m4a.items()},
            pass_4b=passes(m4b), fail_4b=failing(m4b),
            pass_4a=passes(m4a), fail_4a=failing(m4a),
            weakest_rel=weakest_rel(m4b, m0)))
    return rows


def flip_depth(rows):
    """Smallest k at which 4b fails; NaN (reported as kmax+1 'survived') if it never does.
    A return of 0 means the book NEVER PASSED on that panel/arena — there is no pass to lose —
    and is reported as NO_PASS_AT_K0, never as a fragility result."""
    for r in rows:
        if not r["pass_4b"]:
            return r["k"]
    return np.nan


def status(d, kmax):
    if not np.isfinite(d):
        return f"SURVIVED_>{kmax}"
    if d == 0:
        return "NO_PASS_AT_K0"
    return f"FLIPPED_AT_{int(d)}"


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1690 lane C — {SLUG}")
    say("# frozen book: composite(21/252,0/126,0/63) RAW, NO vol scaler, gate = above 200d MA AND")
    say(f"# vol20 < {MAXVOL}, N={A_N}, H={A_H}, GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 unit = {UNITS}   DIAL 2 k = 0..{K_YEAR} (YEAR) / 0..{K_DAY} (DAY_BOOK,DAY_SPY) / 0..{K_ADV} (DAY_ADV)")
    say(f"# published, NOT dials: PANEL, CONVENTION {CONVS}, BAR {BARS}, arena FULL/IS/OOS")
    say("# the deletion is applied to BOOK, SPY and LIVE v2 IDENTICALLY under BAR=MOVES (the idea's")
    say("# construction: the bar moves with the tape); BAR=FROZEN deletes from the BOOK only.")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append(("B136", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, depth_rows, r8rows, yr1_rows, overlap_rows = [], [], [], [], []
    m0_cache: dict = {}
    streams: dict = {}

    for name, p_px, inv in panels:
        pan = Panel(name, p_px, inv)
        idx = pan.idx[WARMUP:]
        W = build(pan)
        rb = run_book(pan, W)[WARMUP:]
        rs = pan.spy[WARMUP:]
        rl = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        st = Streams(idx, rb, rs, rl)
        streams[name] = st

        b0 = triple(rb); s0 = triple(rs); l0 = triple(rl)
        o = st.oos
        bo0, so0, lo0 = triple(rb[o]), triple(rs[o]), triple(rl[o])
        say(f"\n## {name}  n_days={len(idx)}  n_names={len(inv)}  window {idx[0].date()}..{idx[-1].date()}")
        say(f"   BOOK    full {b0['CAGR']:7.2%} / {b0['Sharpe']:.4f} / {b0['MaxDD']:7.2%}"
            f"   OOS {bo0['CAGR']:7.2%} / {bo0['Sharpe']:.4f} / {bo0['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {l0['CAGR']:7.2%} / {l0['Sharpe']:.4f} / {l0['MaxDD']:7.2%}"
            f"   OOS {lo0['CAGR']:7.2%} / {lo0['Sharpe']:.4f} / {lo0['MaxDD']:7.2%}")
        say(f"   SPY     full {s0['CAGR']:7.2%} / {s0['Sharpe']:.4f} / {s0['MaxDD']:7.2%}"
            f"   OOS {so0['CAGR']:7.2%} / {so0['Sharpe']:.4f} / {so0['MaxDD']:7.2%}")
        if name == "U56":
            cw = np.asarray(idx <= COMMITTED_END)
            b0c, s0c, l0c = triple(rb[cw]), triple(rs[cw]), triple(rl[cw])
            say(f"   [committed window {idx[0].date()}..{COMMITTED_END.date()}, {int(cw.sum())} days — "
                f"1254's own tape; ours runs {len(idx)-int(cw.sum())} sessions longer]")
            say(f"   BOOK/SPY/LIVE on that window: "
                f"{b0c['CAGR']:.4f}/{b0c['Sharpe']:.4f}/{b0c['MaxDD']:.4f}  "
                f"{s0c['CAGR']:.4f}/{s0c['Sharpe']:.4f}/{s0c['MaxDD']:.4f}  "
                f"{l0c['CAGR']:.4f}/{l0c['Sharpe']:.4f}/{l0c['MaxDD']:.4f}")
            gate("G1b book replays committed U56 triple ON 1254's OWN WINDOW",
                 f"{b0c['CAGR']:.4f}/{b0c['Sharpe']:.4f}/{b0c['MaxDD']:.4f}",
                 "/".join(f"{v:.4f}" for v in COMMITTED_U56_BOOK),
                 all(abs(a - b) < 5e-3 for a, b in zip(
                     (b0c["CAGR"], b0c["Sharpe"], b0c["MaxDD"]), COMMITTED_U56_BOOK)))
            gate("G1 book replays committed U56 triple",
                 f"{b0['CAGR']:.4f}/{b0['Sharpe']:.4f}/{b0['MaxDD']:.4f}",
                 "/".join(f"{v:.4f}" for v in COMMITTED_U56_BOOK),
                 all(abs(a - b) < 5e-3 for a, b in zip(
                     (b0["CAGR"], b0["Sharpe"], b0["MaxDD"]), COMMITTED_U56_BOOK)))
            gate("G2 SPY replays 1254's committed U56 SPY triple",
                 f"{s0['CAGR']:.4f}/{s0['Sharpe']:.4f}/{s0['MaxDD']:.4f}",
                 "/".join(f"{v:.4f}" for v in COMMITTED_U56_SPY),
                 all(abs(a - b) < 5e-3 for a, b in zip(
                     (s0["CAGR"], s0["Sharpe"], s0["MaxDD"]), COMMITTED_U56_SPY)))
            gate("G3 LIVE v2 replays 1254's committed U56 triple",
                 f"{l0['CAGR']:.4f}/{l0['Sharpe']:.4f}/{l0['MaxDD']:.4f}",
                 "/".join(f"{v:.4f}" for v in COMMITTED_U56_LIVE),
                 all(abs(a - b) < 5e-3 for a, b in zip(
                     (l0["CAGR"], l0["Sharpe"], l0["MaxDD"]), COMMITTED_U56_LIVE)))

        # ---------------- the ladders (arena FULL)
        for unit in UNITS:
            kmax = K_YEAR if unit == "YEAR" else (K_ADV if unit == "DAY_ADV" else K_DAY)
            combos = [("ZERO", "MOVES")] if unit == "DAY_ADV" else \
                     [(c, b) for c in CONVS for b in BARS]
            for conv, bar in combos:
                rr = ladder_rows(st, unit, conv, bar, name, "FULL", kmax, m0_cache)
                rows.extend(rr)
                d = flip_depth(rr)
                depth_rows.append(dict(panel=name, arena="FULL", unit=unit, conv=conv, bar=bar,
                                       kmax=kmax, flip_k=d, status=status(d, kmax),
                                       survived=bool(not np.isfinite(d)),
                                       first_leg=next((r["fail_4b"] for r in rr if not r["pass_4b"]), "-"),
                                       path=next((r["deleted"] for r in rr if not r["pass_4b"]), "-")))
                hd = "HEADLINE" if ((unit == "YEAR" and conv == "SPLICE" and bar == "MOVES")
                                    or (unit != "YEAR" and conv == "ZERO" and bar == "MOVES")) else "        "
                fr = next((r for r in rr if not r["pass_4b"]), None)
                say(f"   {hd} {unit:<9} {conv:<6} BAR={bar:<6} {status(d, kmax):<15}"
                    f" leg(s) {(fr['fail_4b'] if fr else '-'):<12}"
                    f" deleted: {(fr['deleted'] if fr else '-')[:64]}")

        # ---------------- exhaustive single-year read (headline convention)
        for y in st.years:
            keep = st.year != y
            if keep.sum() < 300:
                continue
            b, s, l = st.eval(keep, "SPLICE", "MOVES")
            m = margins_4b(b, s, True)
            yr1_rows.append(dict(panel=name, year=y, n_days=int(keep.sum()),
                                 book_Sharpe=b["full"]["Sharpe"], book_MaxDD=b["full"]["MaxDD"],
                                 book_CAGR=b["full"]["CAGR"], spy_Sharpe=s["full"]["Sharpe"],
                                 **{f"m4b_{k}": v for k, v in m.items()},
                                 pass_4b=passes(m), fail_4b=failing(m),
                                 pass_4a=passes(margins_4a(b, l))))
        ob = np.argsort(-st.book)[:K_DAY]
        os_ = np.argsort(-st.spy)[:K_DAY]
        wb = np.argsort(st.book)[:K_DAY]
        ws = np.argsort(st.spy)[:K_DAY]
        say(f"   TOP-{K_DAY} DAY OVERLAP book vs SPY: best {len(set(ob.tolist()) & set(os_.tolist()))}"
            f"/{K_DAY}, worst {len(set(wb.tolist()) & set(ws.tolist()))}/{K_DAY}"
            f"   |  book's single best day {st.idx[ob[0]].date()} ({st.book[ob[0]]:+.2%},"
            f" SPY {st.spy[ob[0]]:+.2%})"
            f"  SPY's single worst day {st.idx[ws[0]].date()} (SPY {st.spy[ws[0]]:+.2%},"
            f" book {st.book[ws[0]]:+.2%})")
        overlap_rows.append(dict(panel=name, top_best_overlap=int(len(set(ob.tolist()) & set(os_.tolist()))),
                                 top_worst_overlap=int(len(set(wb.tolist()) & set(ws.tolist()))),
                                 k=K_DAY, book_best_day=str(st.idx[ob[0]].date()),
                                 book_best_ret=float(st.book[ob[0]]), spy_on_that_day=float(st.spy[ob[0]]),
                                 spy_worst_day=str(st.idx[ws[0]].date()), spy_worst_ret=float(st.spy[ws[0]]),
                                 book_on_that_day=float(st.book[ws[0]])))
        np_ = [r for r in yr1_rows if r["panel"] == name]
        say(f"   exhaustive k=1 YEAR (SPLICE/DD_SEG, BAR=MOVES): {sum(r['pass_4b'] for r in np_)}"
            f" of {len(np_)} single-year deletions keep the 4b pass")

    # ---------------- 1254 cross-run gate: k=1 over the TEN OOS years, U56
    st = streams["U56"]
    oos_years = [y for y in st.years if y >= 2017]
    ok = 0
    for y in oos_years:
        keep = st.year != y
        b, s, l = st.eval(keep, "SPLICE", "MOVES")
        if passes(margins_4b(b, s, True)):
            ok += 1
    gate("G4 1254 cross-run: k=1 over the 10 OOS years on U56",
         f"{ok} of {len(oos_years)} pass", "9 of 10 pass",
         ok == 9 and len(oos_years) == 10)

    # ---------------- RULE 8 walk-forward
    say("\n## RULE 8 — fragility measured on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE")
    say("   IS 4b legs = both IS halves + DD + CAGR (no OOS leg exists inside IS);")
    say("   OOS 4b legs = both OOS halves + DD + CAGR, computed on 2017-2026 alone.")
    is_depth, oos_depth = {}, {}
    for name, stf in streams.items():
        st_is = stf.slice(stf.is_)
        st_oos = stf.slice(stf.oos)
        for unit in UNITS:
            kmax = K_YEAR if unit == "YEAR" else (K_ADV if unit == "DAY_ADV" else K_DAY)
            conv = "SPLICE" if unit == "YEAR" else "ZERO"
            ri = ladder_rows(st_is, unit, conv, "MOVES", name, "IS", kmax, m0_cache)
            ro = ladder_rows(st_oos, unit, conv, "MOVES", name, "OOS", kmax, m0_cache)
            rows.extend(ri); rows.extend(ro)
            di, do = flip_depth(ri), flip_depth(ro)
            is_depth[(name, unit)] = kmax + 1 if not np.isfinite(di) else di
            oos_depth[(name, unit)] = kmax + 1 if not np.isfinite(do) else do
            for arena, rr, d in (("IS", ri, di), ("OOS", ro, do)):
                depth_rows.append(dict(panel=name, arena=arena, unit=unit, conv=conv, bar="MOVES",
                                       kmax=kmax, flip_k=d, status=status(d, kmax),
                                       survived=bool(not np.isfinite(d)),
                                       first_leg=next((r["fail_4b"] for r in rr if not r["pass_4b"]), "-"),
                                       path=next((r["deleted"] for r in rr if not r["pass_4b"]), "-")))
            say(f"   {name:<9} {unit:<9} IS {status(di, kmax):<15}"
                f" (leg {next((r['fail_4b'] for r in ri if not r['pass_4b']), '-'):<12})"
                f"   OOS {status(do, kmax):<15}"
                f" (leg {next((r['fail_4b'] for r in ro if not r['pass_4b']), '-'):<12})")

    a = [is_depth[k] for k in sorted(is_depth)]
    b = [oos_depth[k] for k in sorted(oos_depth)]
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    rc = float(np.corrcoef(ra, rb)[0, 1]) if np.std(ra) > 0 and np.std(rb) > 0 else float("nan")
    say(f"   IS/OOS flip-depth rank correlation over the {len(a)} (panel,unit) pairs: {rc:+.4f}")

    anchor = "U56"
    for unit in UNITS:
        pick = max(streams, key=lambda p: (is_depth[(p, unit)], -list(streams).index(p)))
        for who, pname in (("IS-CHOSEN", pick), ("ANCHOR (do nothing)", anchor)):
            stf = streams[pname]
            o = stf.oos
            bo, so, lo = triple(stf.book[o]), triple(stf.spy[o]), triple(stf.live[o])
            r8rows.append(dict(unit=unit, arm=who, panel=pname,
                               is_flip=is_depth[(pname, unit)], oos_flip=oos_depth[(pname, unit)],
                               oos_book_CAGR=bo["CAGR"], oos_book_Sharpe=bo["Sharpe"], oos_book_MaxDD=bo["MaxDD"],
                               oos_live_CAGR=lo["CAGR"], oos_live_Sharpe=lo["Sharpe"], oos_live_MaxDD=lo["MaxDD"],
                               oos_spy_CAGR=so["CAGR"], oos_spy_Sharpe=so["Sharpe"], oos_spy_MaxDD=so["MaxDD"],
                               d_vs_live=bo["Sharpe"] - lo["Sharpe"], d_vs_spy=bo["Sharpe"] - so["Sharpe"]))
        mean_flip = float(np.mean([oos_depth[(p, unit)] for p in streams]))
        worst = min(streams, key=lambda p: oos_depth[(p, unit)])
        r8rows.append(dict(unit=unit, arm="MEAN over panels", panel="-",
                           is_flip=float(np.mean([is_depth[(p, unit)] for p in streams])),
                           oos_flip=mean_flip))
        r8rows.append(dict(unit=unit, arm="WORST panel", panel=worst,
                           is_flip=is_depth[(worst, unit)], oos_flip=oos_depth[(worst, unit)]))
        say(f"   {unit:<9} IS-only chooser picks {pick:<9} (IS flip {is_depth[(pick,unit)]});"
            f" its OOS flip {oos_depth[(pick,unit)]}  vs anchor U56 OOS flip {oos_depth[(anchor,unit)]}"
            f"  vs mean {mean_flip:.2f}  vs worst panel {worst} ({oos_depth[(worst,unit)]})")

    say("\n## THE DD LEG IS THE ONLY LEG THAT EVER FLIPS — the mechanism, U56, BAR=MOVES")
    say(f"   {'unit':<9} {'conv':<6} {'k':>3} | {'book MaxDD':>10} {'0.60*SPY':>10} {'DD margin':>10}"
        f" | {'H1 mgn':>7} {'H2 mgn':>7} {'OOS mgn':>7} {'CAGR mgn':>8} | 4b")
    gg = pd.DataFrame(rows)
    for unit, conv in (("YEAR", "SPLICE"), ("DAY_ADV", "ZERO"), ("DAY_BOOK", "ZERO"), ("DAY_SPY", "ZERO")):
        sub = gg[(gg.panel == "U56") & (gg.arena == "FULL") & (gg.bar == "MOVES")
                 & (gg.unit == unit) & (gg.conv == conv)]
        for _, r in sub.iterrows():
            if r["k"] > 3 and not (unit == "DAY_BOOK" and r["k"] in (8, 9)) and not (
                    unit == "DAY_SPY" and r["k"] in (6, 7)):
                continue
            say(f"   {unit:<9} {conv:<6} {int(r['k']):>3} | {r['book_MaxDD']:>10.2%}"
                f" {DD_CAP*r['spy_MaxDD']:>10.2%} {r['m4b_DD']:>+10.4f}"
                f" | {r['m4b_H1']:>+7.4f} {r['m4b_H2']:>+7.4f} {r['m4b_OOS']:>+7.4f}"
                f" {r['m4b_CAGR']:>+8.4f} | {'PASS' if r['pass_4b'] else 'FAIL ' + r['fail_4b']}")

    say("\n## RULE 8 OOS TRIPLES (2017-2026, k = 0, read once)")
    for name, stf in streams.items():
        o = stf.oos
        bo, so, lo = triple(stf.book[o]), triple(stf.spy[o]), triple(stf.live[o])
        say(f"   {name:<9} BOOK {bo['CAGR']:7.2%}/{bo['Sharpe']:.4f}/{bo['MaxDD']:7.2%}"
            f"   LIVE v2 {lo['CAGR']:7.2%}/{lo['Sharpe']:.4f}/{lo['MaxDD']:7.2%}"
            f"   SPY {so['CAGR']:7.2%}/{so['Sharpe']:.4f}/{so['MaxDD']:7.2%}")

    # ---------------- outputs
    gdf = pd.DataFrame(rows)
    gdf.to_csv(f"{STEM}.grid.csv", index=False)
    pd.DataFrame(depth_rows).to_csv(f"{STEM}.depth.csv", index=False)
    pd.DataFrame(yr1_rows).to_csv(f"{STEM}.years.csv", index=False)
    pd.DataFrame(overlap_rows).to_csv(f"{STEM}.overlap.csv", index=False)
    pd.DataFrame(r8rows).to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    n4a = int(gdf.pass_4a.sum()); n4b = int(gdf.pass_4b.sum())
    say(f"\n## CORPUS: {len(gdf)} grid points published — 4a passes {n4a}, 4b passes {n4b}")
    say(f"## GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
    say(f"## {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
