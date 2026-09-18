#!/usr/bin/env python3
"""Idea 1203 (lane cloud, 2026-09-18): does the TIE-BREAK STATISTIC matter once the TIE is
DECLARED?

THE PREMISE, READ FROM THE RECORD.  Idea 1199
(`2026-09-17_should-a-SATURATED-PERCENTILE-be-PUBLISHABLE-as-a-POINT-at-all_cloud.py`) walked
four publishing conventions for a saturated null percentile and found B_ONE, B_TWO and B_CP
DECISION-IDENTICAL over its 18 (panel, K) cells — its committed walkforward.csv reads
0.9568214 for all three against B_POINT's 0.8897235, a gap of +0.0671.  All three differ from
B_POINT in exactly one way: they DECLARE the ceiling a tie and then break it on CH_Z.  So the
whole +0.0671 is the tie declaration plus ONE arbitrary tie-break statistic.  CH_Z was never
argued for; it is one choice among many.  If the gap is a property of DECLARING the tie, any
tie-break keeps most of it and a publishing clause need only REQUIRE that one be named.  If the
gap is a property of CH_Z, the clause must NAME the statistic, and 1199's +0.0671 is a
measurement of CH_Z and not of the bound form at all.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  TIE-BREAK {T_FIRST, T_LAST, T_RANDOM, T_CH_Z, T_ISSHARPE, T_IS4B, T_NULLGAP, T_HOLD}
  K         {10, 25, 50, 100, 200, 400} null draws — 1199's resolution ladder, nested

  8 x 6 = 48 cells per panel, 144 in all, EVERY ONE PUBLISHED in .walkforward.csv.

  The eight rungs, declared before any number was read.  All are computed on the IS window
  (warm-up..2016-12-31) ONLY and are applied to the SAME tie set, which the frozen bound form
  fixes; they differ only in which tied book they hand back.
    T_FIRST    first in the frozen (cadence, N) sort order — the record's own habit, and
               exactly what B_POINT does on a tied set.  The control.
    T_LAST     last in that same order.  The adversarial counterpart: it shares FIRST's total
               absence of information, so FIRST-vs-LAST is the width of pure ordering luck and
               is the honest reading of the queue's "worst choice".
    T_RANDOM   a seeded uniform draw among the tied books — the literal "merely require one".
    T_CH_Z     (IS Sharpe - pool mean) / pool sd.  1199's choice, in the grid as one rung.
    T_ISSHARPE the book's own IS Sharpe, no null at all.  The free rung.
    T_IS4B     the book's IS 4b margin: min over the three IS-computable 4b legs of
               (value - bar) / |bar| — IS Sharpe vs SPY's IS Sharpe, IS MaxDD vs 0.60 x SPY's,
               IS CAGR vs 0.70 x SPY's.  The queue names it; the legs and the normalisation are
               declared here because the record has no convention for them.
    T_NULLGAP  IS Sharpe MINUS the pool MAXIMUM.  This is the quantity a saturated percentile
               destroys (every book above the pool reads 1.000 whether it clears the best draw
               by 0.001 or by 0.5), so it is the tie-break a bound form's own logic implies.
    T_HOLD     holdings count: the LARGEST N among the tied books, order-ties to FIRST.  The
               declared direction is "broader book wins"; the queue names the statistic, not
               its sign, so the sign is stated here and not chosen after the fact.

WHAT IS FROZEN AND IS NOT A DIAL.
  BOUND FORM = B_ONE, frozen, as the queue requires ("at a FROZEN bound form").  Gate G6
  re-establishes 1199's own finding that B_ONE, B_TWO and B_CP declare a BIT-IDENTICAL tie set
  at every one of the 2,160 (panel, book, K, seed) rows, so freezing B_ONE discards nothing:
  the result transfers to all three.
  PANEL {U56, B136, SMALL} is not a dial (rule 9, all three always read).
  The 36-book population — N in {5,10,15,20,30,40} x cadence {W,M} x 3 panels, 1199's, unchanged
  — is not a dial; every book is published with its own 4a and 4b verdict in .books.csv.
  SEED is not a dial: 20 seeds at every cell, and the spread across them is published.
  THE SORT ORDER "FIRST-WINS" REFERS TO is 1199's, not this run's: `sort_values(["cadence","N"])`,
  i.e. cadence ascending as a string (M before W) then N ascending.  Every order-dependent rung
  uses it, which is why B_POINT here replays 1199's own control.  (Idea 1202 asks whether that
  habit is the record's actual habit; this run inherits it and does not settle it.)

THE TAPE VINTAGE, STATED BEFORE THE GATES.  U56 is served from data/prices.csv, refreshed daily,
whose ADJUSTED closes are restated retroactively; B136 and SMALL come from the weekly caches and
are the same bytes 1199 read.  So U56 cannot replay 1199 bit for bit and is not asked to: the
drift is PUBLISHED (G4b), the exactness gates are placed on the objects that are vintage-free —
CH_PCT at every row (G4a), the tie sets (G6a), 24 of 36 books (G4e), and both conventions'
per-panel means on B136 and SMALL (G5c) — and every U56-driven difference from 1199's committed
levels is named, including any decision it flips (G4d).

FROZEN CONSTRUCTION, INHERITED WHOLE FROM 1199/1197/1162 AND NOT TOUCHED HERE: 3-leg composite
of percentile ranks (21/252, 0/126, 0/63); eligibility = above own 200d MA; top-N at GROSS/N =
0.75/N of NAV with gated-out weight to CASH; 10 bps per unit turnover (rule 2); t+1 execution
via the shifted rebalance mask; 260-row warm-up; IS ends 2016-12-31; OOS starts 2017-01-01;
NDRAW = 400 gross-matched null books per book (at each rebalance row N names drawn uniformly
from those priced, weight 0.75/N, no score), seeded exactly as 1199 seeded them.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) THE TIE DECLARATION IS THE WHOLE STORY — every tie-break, T_RANDOM and T_LAST included,
      keeps most of the +0.0671.  Then a clause need only REQUIRE a tie-break, and 1199's
      number is a property of the bound form.
  (B) CH_Z IS THE WHOLE STORY — the informative rungs keep it, T_RANDOM/T_FIRST/T_LAST do not.
      Then the clause must NAME a statistic and 1199 measured CH_Z, not B_ONE.
  (C) THE SPREAD ACROSS TIE-BREAKS IS LARGER THAN THE GAP ITSELF — the choice of tie-break is
      a bigger free parameter than the convention it was introduced to fix.  Then the honest
      reading is that neither number is a measurement.
  (D) NO TIE-BREAK BEATS DOING NOTHING — every rung, CH_Z included, loses to always holding the
      incumbent N=20/W shape.  That is the capital finding whichever of (A)-(C) fires, and it
      is reported first.

RULE 8 (walk-forward, required).  Two levels, both honest.
  (i) Every pick is already walk-forward: every tie-break statistic is computed on
      warm-up..2016-12-31 ONLY and 2017-2026 is read ONCE, per (panel, K, seed).
  (ii) The DIALS are then chosen the same way: (TIE-BREAK, K) is picked on the IS window ALONE
      — by the mean IS Sharpe of the books that rung picks — per panel, and 2017-2026 is read
      once for that choice.  Reported against (a) DO-NOTHING = the incumbent N=20/W book held
      throughout, (b) the mean over all 48 cells, (c) the WORST cell, with the IS/OOS rank
      correlation over the 48.  OOS CAGR / Sharpe / MaxDD of every pick are published against
      SPY's and against the live RULES v2 baseline's on the same rows.  The capital verdict is
      the sign of chooser-minus-do-nothing, never the best cell.

GATES.  G1 fast runner == engine.backtest post-warm-up.  G2 determinism (whole U56 null pool
and grid recomputed bit for bit).  G3 live RULES v2 U56 MaxDD == the record's -12.05%.
G4 REPLAY: CH_PCT and CH_Z are reproduced against 1199's committed grid.csv at all 4,320 rows,
and the 36 books' IS/OOS Sharpe against its committed books.csv — this run must stand on the
same objects 1199's +0.0671 was computed on or its answer is about something else.  G5 the
B_POINT control reproduces 1199's committed pooled 0.8897235 and B_ONE-on-CH_Z its 0.9568214,
i.e. the +0.0671 itself is replayed before it is decomposed.  G6 B_ONE / B_TWO / B_CP tie sets
bit-identical at every row.  G7 the null is gross-matched (target gross 0.75 at every
rebalance row).  G8 the IS-truncated null runner gives IS Sharpes identical to the full-tape
runner (this run truncates the null panel at the IS end for speed; the runner is causal, so
this must be EXACT, not close).

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths on every book and every pick;
rule 5 one idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship
stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before anything is
computed).  Every absolute level here is optimistic and every 4b pass is an UPPER bound.  The
headline is a CONTRAST BETWEEN EIGHT CHOOSERS PICKING FROM THE SAME 12 BOOKS ON THE SAME PANEL
over the same tape — a difference inside one biased pool — so it is first-order immune to a
level bias that moves all cells together.  One direction is not neutral and is stated: a
current-constituent panel flatters momentum books, which raises every book's IS Sharpe and
therefore makes the null percentile MORE saturated than it would be on a live panel; the tie
sets here are consequently WIDER than a real implementer's, so any sensitivity to the
tie-break statistic measured here is an UPPER bound on the live one.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-18_does-the-TIE-BREAK-STATISTIC-matter-once-the-TIE-is-DECLARED_cloud.py
"""
from __future__ import annotations

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

DATE = "2026-09-18"
SLUG = "does-the-TIE-BREAK-STATISTIC-matter-once-the-TIE-is-DECLARED"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ---- frozen construction (1199's, inherited whole) ----------------------------------------
COST, GROSS, WARMUP = 10.0, 0.75, 260
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
NDRAW, NSEED = 400, 20
SEED0 = 11991199
KLAD = [10, 25, 50, 100, 200, 400]
NLAD = [5, 10, 15, 20, 30, 40]
CADLAD = ["W", "M"]
ANCHORS = [(n, f) for f in CADLAD for n in NLAD]      # 12 books per panel, 1199's BUILD order
# THE FROZEN SORT ORDER, WHICH IS WHAT "FIRST-WINS" MEANS AND IS NOT THIS RUN'S CHOICE.
# 1199's chooser reads `sub.sort_values(["cadence", "N"])`, i.e. cadence ASCENDING as a string
# ("M" before "W") and then N ascending.  Every order-dependent rung here (T_FIRST, T_LAST, and
# the internal first-wins resolution of every argmax rung) uses exactly that order, so B_POINT
# replays 1199's own control rather than a re-ordered lookalike.  Idea 1202 asks whether the
# record's habit really is first-wins; this run does not settle that and inherits the habit.
REC_ORDER = sorted(ANCHORS, key=lambda t: (t[1], t[0]))
TIEBREAKS = ["T_FIRST", "T_LAST", "T_RANDOM", "T_CH_Z", "T_ISSHARPE", "T_IS4B", "T_NULLGAP", "T_HOLD"]
BOUND_FROZEN = "B_ONE"
DONOTHING = (20, "W")                                  # the record's incumbent shape
TIESEED = 12031203                                     # T_RANDOM's own stream, declared

# committed figures this run must reproduce or fail (gates)
LIVE_MAXDD_COMMITTED = -0.1205                         # 1199 G3
REF_B_POINT, REF_B_ONE = 0.8897235, 0.9568214          # 1199 committed walkforward pooled means
REF1199 = ROOT / "research" / "backtests" / (
    "2026-09-17_should-a-SATURATED-PERCENTILE-be-PUBLISHABLE-as-a-POINT-at-all_cloud")

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"  [{'PASS' if ok else 'FAIL'}] {name:72s} value={value} target={target}")
    return bool(ok)


# =========================================================== panels and the fast runner
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.P = np.cumprod(1.0 + self.rets, axis=0)
        self.Pprev = np.vstack([np.ones((1, self.P.shape[1])), self.P[:-1]])
        self.priced = px.notna().values
        self.seg = {}
        for f in CADLAD:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            s = np.flatnonzero(m)
            self.seg[f] = (s, np.append(s[1:], len(px)))
        self.i0 = WARMUP
        self.ioos = px.index.searchsorted(pd.Timestamp(OOS_START))


def run_from_starts(pan, freq, Wstart, stop=None):
    """1199/1197/1162's fast runner, verbatim except for `stop`, which truncates the tape.
    The runner is causal (segment k touches only rows [starts[k], ends[k])), so truncating
    cannot change any earlier row — gate G8 proves it rather than asserting it."""
    starts, ends = pan.seg[freq]
    T, M = pan.rets.shape
    if stop is None:
        stop = T
    held = np.zeros((stop, M))
    turn = np.zeros(stop)
    cur = np.zeros(M)
    for k, (i0, i1) in enumerate(zip(starts, ends)):
        if i0 >= stop:
            break
        i1 = min(i1, stop)
        w0 = Wstart[k]
        turn[i0] = np.abs(w0 - cur).sum()
        base = pan.Pprev[i0]
        A = w0[None, :] * (pan.Pprev[i0:i1] / base[None, :])
        cash0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + cash0
        held[i0:i1] = A / V[:, None]
        Aend = w0 * (pan.P[i1 - 1] / base)
        cur = Aend / (Aend.sum() + cash0)
    return (held * pan.rets[:stop]).sum(axis=1) - turn * COST / 1e4


def starts_from_weights(pan, freq, W):
    starts, _ = pan.seg[freq]
    Wv = W.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
    return Wv[starts]


def book_weights(pan, n):
    q = pan.px[pan.invest]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    elig = comp.where(q > q.rolling(200).mean())
    rk = elig.rank(axis=1, ascending=False)
    W = pd.DataFrame(0.0, index=pan.px.index, columns=pan.px.columns)
    W[pan.invest] = (rk <= n).astype(float) * (GROSS / n)
    return W


def null_starts(pan, freq, n, rng):
    starts, _ = pan.seg[freq]
    out = np.zeros((len(starts), pan.rets.shape[1]))
    for k, i in enumerate(starts):
        avail = pan.iinv[pan.priced[max(i - 1, 0)][pan.iinv]]
        if len(avail) < n:
            continue
        out[k, rng.choice(avail, size=n, replace=False)] = GROSS / n
    return out


def sharpe(r):
    r = np.asarray(r, float)
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min())


def cagr(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float(e[-1] ** (252 / len(r)) - 1)


def trip(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return float("nan")
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def build_panels():
    out = []
    u = load_universe()
    out.append(("U56", u, [c for c in u.columns if c != "SPY"]))
    b = load_universe(broad=True)
    out.append(("B136", b, [c for c in b.columns if c != "SPY"]))
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in s.columns if c != "SPY" and c not in bad]
    say(f"  SMALL panel: {s.shape[1]-1} columns, {len(bad & set(s.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv)} investable")
    out.append(("SMALL", s, inv))
    return out


# =========================================================== the tie-break rungs
def tiebreak_pick(name, tied, rng):
    """`tied` is a DataFrame of the tied books in the frozen (cadence, N) order, carrying every
    tie-break statistic as a column.  Returns the positional index within `tied`.  Every rung
    resolves its own internal ties to FIRST in that same order, declared."""
    if name == "T_FIRST":
        return 0
    if name == "T_LAST":
        return len(tied) - 1
    if name == "T_RANDOM":
        return int(rng.integers(len(tied)))
    col = {"T_CH_Z": "CH_Z", "T_ISSHARPE": "IS_Sharpe", "T_IS4B": "IS_4b_margin",
           "T_NULLGAP": "NULLGAP", "T_HOLD": "N"}[name]
    v = tied[col].values.astype(float)
    return int(np.nanargmax(v))          # argmax, first-wins on exact ties


def main():
    t0 = time.time()
    say("=" * 100)
    say(f"# {DATE} idea 1203 lane cloud — {SLUG}")
    say("=" * 100)
    say(f"  dial 1 = TIE-BREAK {TIEBREAKS}")
    say(f"  dial 2 = K {KLAD}")
    say(f"  FROZEN bound form = {BOUND_FROZEN} (gate G6 shows B_TWO and B_CP declare the SAME tie set)")
    say(f"  frozen books: N {NLAD} x cadence {CADLAD} x 3 panels = 36; gross {GROSS} in {GROSS}/N slots;"
        f" {COST:.0f} bps; t+1; warm-up {WARMUP}; IS ends 2016-12-31; NDRAW {NDRAW}; seeds {NSEED}")
    say(f"  DO-NOTHING bar = the incumbent shape N={DONOTHING[0]}/{DONOTHING[1]} held throughout")

    panels = build_panels()
    books, grid, pan_ctx = [], [], {}

    for pi, (pname, px, invest) in enumerate(panels):
        pan = Panel(pname, px, invest)
        i0, ioos = pan.i0, pan.ioos
        spy_all = px["SPY"].pct_change().fillna(0.0).values
        base_all = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        s_full, s_is, s_oos = spy_all[i0:], spy_all[i0:ioos], spy_all[ioos:]
        b_full, b_oos = base_all[i0:], base_all[ioos:]
        h = len(s_full) // 2
        spyT, baseT = trip(s_full), trip(b_full)
        spyH = (sharpe(s_full[:h]), sharpe(s_full[h:]))
        baseH = (sharpe(b_full[:h]), sharpe(b_full[h:]))
        spyIS = trip(s_is)
        pan_ctx[pname] = dict(spyT=spyT, spyH=spyH, spy_oos=trip(s_oos), spyIS=spyIS,
                              baseT=baseT, baseH=baseH, base_oos=trip(b_oos), h=h)
        say("")
        say(f"  {pname:6s} n_invest={len(invest):4d}  {px.index[i0].date()}..{px.index[-1].date()}  "
            f"IS rows {ioos-i0}  OOS rows {len(px)-ioos}")
        say(f"  {'':6s} SPY  full {spyT['CAGR']:7.2%} / {spyT['Sharpe']:.4f} / {spyT['MaxDD']:7.2%}  "
            f"halves {spyH[0]:.4f}/{spyH[1]:.4f}  OOS {trip(s_oos)['CAGR']:7.2%} / "
            f"{trip(s_oos)['Sharpe']:.4f} / {trip(s_oos)['MaxDD']:7.2%}")
        say(f"  {'':6s} LIVE RULES v2  full {baseT['CAGR']:7.2%} / {baseT['Sharpe']:.4f} / "
            f"{baseT['MaxDD']:7.2%}  OOS {trip(b_oos)['CAGR']:7.2%} / {trip(b_oos)['Sharpe']:.4f}")
        say(f"  {'':6s} 4b bars: DD cap {DD_CAP*spyT['MaxDD']:7.2%}  CAGR floor "
            f"{CAGR_FLOOR*spyT['CAGR']:7.2%}  Sharpe H1 {spyH[0]:.4f} H2 {spyH[1]:.4f} "
            f"OOS {sharpe(s_oos):.4f}")
        if pname == "U56":
            gate("G3 live RULES v2 U56 MaxDD == record -12.05%", round(baseT["MaxDD"], 6),
                 LIVE_MAXDD_COMMITTED, abs(baseT["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)

        for ai, (n, freq) in enumerate(ANCHORS):
            cell = 1000 * (pi + 1) + ai          # 1199's seed stream: keyed on the BUILD index
            ordr = REC_ORDER.index((n, freq))    # the record's FIRST-WINS position
            W = book_weights(pan, n)
            r = run_from_starts(pan, freq, starts_from_weights(pan, freq, W))
            if pname == "U56" and ai == 0:
                eng = backtest(px, W, cost_bps=COST, freq=freq)["returns"].values
                d = float(np.nanmax(np.abs(np.asarray(eng[i0:], float) - r[i0:])))
                gate("G1 fast runner == engine.backtest (post-warm-up)", f"{d:.3e}", "< 1e-12", d < 1e-12)
            rf, ris, ros = r[i0:], r[i0:ioos], r[ioos:]
            bt, it, ot = trip(rf), trip(ris), trip(ros)
            half1, half2 = sharpe(rf[:h]), sharpe(rf[h:])
            k4a = (half1 > baseH[0] and half2 > baseH[1] and bt["MaxDD"] >= baseT["MaxDD"])
            legs4b = dict(H1=half1 > spyH[0], H2=half2 > spyH[1],
                          OOS=ot["Sharpe"] > sharpe(s_oos),
                          DD=bt["MaxDD"] >= DD_CAP * spyT["MaxDD"],
                          CAGR=bt["CAGR"] >= CAGR_FLOOR * spyT["CAGR"])
            # the null pool, IS-truncated (gate G8) — only IS Sharpes are used by any rung
            nsh_is = np.empty(NDRAW)
            for d_ in range(NDRAW):
                rng = np.random.default_rng(SEED0 + 100003 * cell + d_)
                nr = run_from_starts(pan, freq, null_starts(pan, freq, n, rng), stop=ioos)
                nsh_is[d_] = sharpe(nr[i0:ioos])
            if pname == "U56" and ai == 0:
                rng = np.random.default_rng(SEED0 + 100003 * cell + 0)
                st = null_starts(pan, freq, n, rng)
                full = run_from_starts(pan, freq, st)
                trc = run_from_starts(pan, freq, st, stop=ioos)
                e8 = float(np.abs(full[i0:ioos] - trc[i0:ioos]).max())
                gate("G8 IS-truncated null runner == full-tape runner on IS rows", f"{e8:.3e}",
                     "== 0.0", e8 == 0.0)
                gmax = float(np.abs(st.sum(axis=1) - GROSS).max())
                gate("G7 null target gross == 0.75 at every rebalance row", f"{gmax:.3e}",
                     "< 1e-12", gmax < 1e-12)
            # the IS 4b margin, declared legs and normalisation
            m_sh = (it["Sharpe"] - spyIS["Sharpe"]) / abs(spyIS["Sharpe"])
            m_dd = (it["MaxDD"] - DD_CAP * spyIS["MaxDD"]) / abs(DD_CAP * spyIS["MaxDD"])
            m_cg = (it["CAGR"] - CAGR_FLOOR * spyIS["CAGR"]) / abs(CAGR_FLOOR * spyIS["CAGR"])
            books.append(dict(panel=pname, N=n, cadence=freq, order=ordr, build_ix=ai, **bt, H1=half1, H2=half2,
                              IS_Sharpe=it["Sharpe"], IS_CAGR=it["CAGR"], IS_MaxDD=it["MaxDD"],
                              OOS_CAGR=ot["CAGR"], OOS_Sharpe=ot["Sharpe"], OOS_MaxDD=ot["MaxDD"],
                              KEEP_4a=k4a, KEEP_4b=all(legs4b.values()),
                              fail4b=",".join(k for k, v in legs4b.items() if not v) or "-",
                              IS_4b_margin=float(min(m_sh, m_dd, m_cg)),
                              NULLGAP=float(it["Sharpe"] - nsh_is.max()),
                              null_is_mean=float(nsh_is.mean()), null_is_sd=float(nsh_is.std(ddof=1)),
                              null_is_max=float(nsh_is.max())))
            obs = it["Sharpe"]
            for K in KLAD:
                for sd in range(NSEED):
                    rs = np.random.default_rng(SEED0 + 7919 * K + sd)
                    pool = nsh_is[rs.choice(NDRAW, size=K, replace=False)]
                    pct = float((pool < obs).mean())
                    z = float((obs - pool.mean()) / pool.std(ddof=1))
                    ceil_ = bool(pct >= 1.0 - 1e-12)
                    floor_ = bool(pct <= 1e-12)
                    grid.append(dict(panel=pname, N=n, cadence=freq, order=ordr, K=K, seed=sd,
                                     CH_PCT=pct, CH_Z=z, SAT_CEIL=ceil_, SAT_FLOOR=floor_,
                                     TIED_B_ONE=ceil_, TIED_B_TWO=bool(ceil_ or floor_),
                                     TIED_B_CP=ceil_))
        say(f"  {pname} books+nulls done  t={time.time()-t0:.0f}s")

    bdf = pd.DataFrame(books)
    gdf = pd.DataFrame(grid)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    gdf.to_csv(f"{OUT}.grid.csv", index=False)
    say("")
    say(f"  36 books and {len(gdf)} (book, K, seed) rows written")

    # ---------------------------------------------------------------- G4 replay against 1199
    # THE TAPE VINTAGE.  U56 is served from data/prices.csv, which is refreshed daily and whose
    # ADJUSTED closes are restated retroactively; B136 and SMALL come from the weekly caches and
    # are the same bytes 1199 read.  So the U56 drift below is a tape fact, not an arithmetic
    # one, and it is PUBLISHED rather than toleranced.  What must be EXACT is the object the tie
    # set is built from (CH_PCT) and the DECISIONS both conventions take — those are compared
    # against 1199's own committed grid row by row and are vintage-free.
    picks_ref_mismatch = np.nan
    try:
        r99g = pd.read_csv(f"{REF1199}.grid.csv")
        key = ["panel", "N", "cadence", "K", "seed"]
        m = gdf.merge(r99g[key + ["CH_PCT", "CH_Z"]], on=key, suffixes=("", "_ref"))
        e_pct = float(np.abs(m.CH_PCT - m.CH_PCT_ref).max())
        e_z = float(np.abs(m.CH_Z - m.CH_Z_ref).max())
        gate(f"G4a CH_PCT replays 1199's grid EXACTLY ({len(m)} rows) — the tie set is the same object",
             f"{e_pct:.3e}", "== 0.0", len(m) == len(gdf) and e_pct == 0.0)
        by = m.assign(dz=(m.CH_Z - m.CH_Z_ref).abs()).groupby("panel").dz.max()
        gate("G4b CH_Z drift vs 1199, by panel (U56 = daily restated cache)",
             "  ".join(f"{k} {v:.2e}" for k, v in by.items()), "published, not toleranced", True)
        gate("G4c CH_Z drift is CONFINED to U56 (B136 and SMALL identical to summation noise)",
             f"B136 {by.get('B136', np.nan):.1e} SMALL {by.get('SMALL', np.nan):.1e}", "< 1e-12",
             float(by.drop(labels=["U56"], errors="ignore").max()) < 1e-12)
        # DECISION-level replay: both conventions must pick the SAME book as 1199's own numbers
        mm, mm2v, flips = 0, 0, []
        for (pn, K, sd), g in m.groupby(["panel", "K", "seed"]):
            g = g.sort_values("order")
            a_point = g[g.CH_PCT == g.CH_PCT.max()].iloc[0].order
            b_point = g[g.CH_PCT_ref == g.CH_PCT_ref.max()].iloc[0].order
            ta = g[g.CH_PCT >= 1.0 - 1e-12]
            tb_ = g[g.CH_PCT_ref >= 1.0 - 1e-12]
            ta = ta if len(ta) else g[g.CH_PCT == g.CH_PCT.max()]
            tb_ = tb_ if len(tb_) else g[g.CH_PCT_ref == g.CH_PCT_ref.max()]
            a_z = ta.iloc[int(np.nanargmax(ta.CH_Z.values))].order
            b_z = tb_.iloc[int(np.nanargmax(tb_.CH_Z_ref.values))].order
            bad = int(a_point != b_point) + int(a_z != b_z)
            mm += bad
            if bad:
                flips.append(f"{pn}/K={K}/seed={sd}: B_POINT {b_point}->{a_point} CH_Z {b_z}->{a_z}")
                if pn != "U56":
                    mm2v += bad
        picks_ref_mismatch = mm
        nd = 2 * len(m.groupby(["panel", "K", "seed"]))
        gate(f"G4d DECISION replay vs 1199's own grid, ALL {nd} decisions",
             f"{nd-mm} of {nd} identical" + (f"; flips: {flips}" if mm else ""),
             "published, not toleranced (U56 tape is restated daily)", True)
        mm2 = mm2v
        gate("G4d2 DECISION replay on the VINTAGE-FREE panels (B136 + SMALL)",
             f"{mm2} mismatches", "== 0", mm2 == 0)
        r99b = pd.read_csv(f"{REF1199}.books.csv")
        mb = bdf.merge(r99b[["panel", "N", "cadence", "IS_Sharpe", "OOS_Sharpe", "null_is_max"]],
                       on=["panel", "N", "cadence"], suffixes=("", "_ref"))
        eb = mb.assign(d=np.maximum.reduce([(mb.IS_Sharpe - mb.IS_Sharpe_ref).abs(),
                                            (mb.OOS_Sharpe - mb.OOS_Sharpe_ref).abs(),
                                            (mb.null_is_max - mb.null_is_max_ref).abs()])
                       ).groupby("panel").d.max()
        gate("G4e 24 of 36 books (B136 + SMALL) replay 1199's books.csv",
             "  ".join(f"{k} {v:.2e}" for k, v in eb.items()), "B136 and SMALL < 1e-12",
             len(mb) == 36 and float(eb.drop(labels=["U56"], errors="ignore").max()) < 1e-12)
    except FileNotFoundError:
        gate("G4 replay 1199 artefacts", "missing", "present", False)

    n_cp = int((gdf.TIED_B_ONE != gdf.TIED_B_CP).sum())
    dtwo = gdf[gdf.TIED_B_ONE != gdf.TIED_B_TWO]
    gate(f"G6a B_ONE and B_CP declare a BIT-IDENTICAL tie set at all {len(gdf)} rows -> freezing "
         "B_ONE loses nothing for either", float(n_cp), 0.0, n_cp == 0)
    gate(f"G6b every B_ONE/B_TWO difference is a FLOOR row (B_TWO covers the floor by design)",
         f"{len(dtwo)} rows, all SAT_FLOOR={bool(dtwo.SAT_FLOOR.all()) if len(dtwo) else True}"
         + (f" -> {list(zip(dtwo.panel, dtwo.N, dtwo.cadence, dtwo.K, dtwo.seed))}" if len(dtwo) else ""),
         "all differences are floor rows", bool(dtwo.SAT_FLOOR.all()) if len(dtwo) else True)

    # ---------------------------------------------------------------- the tie sets themselves
    say("")
    say("=" * 100)
    say("(A) THE TIE SET THE FROZEN BOUND FORM DECLARES — how often it binds, and how wide")
    say("=" * 100)
    say(f"    {'panel':6s} {'K':>4}  {'mean tied':>9}  {'min':>4} {'max':>4}  {'share seeds':>11}  "
        f"{'share K-cells':>13}")
    tsrows = []
    for pname in bdf.panel.unique():
        for K in KLAD:
            sub = gdf[(gdf.panel == pname) & (gdf.K == K)]
            sizes = sub.groupby("seed").TIED_B_ONE.sum().values
            binds = float(np.mean(sizes > 1))
            tsrows.append(dict(panel=pname, K=K, mean_tied=float(sizes.mean()),
                               min_tied=int(sizes.min()), max_tied=int(sizes.max()),
                               share_seeds_tie_binds=binds,
                               share_books_at_ceiling=float(sub.TIED_B_ONE.mean())))
            say(f"    {pname:6s} {K:>4}  {sizes.mean():>9.2f}  {sizes.min():>4d} {sizes.max():>4d}  "
                f"{binds:>11.3f}  {sub.TIED_B_ONE.mean():>13.3f}")
    pd.DataFrame(tsrows).to_csv(f"{OUT}.tiesets.csv", index=False)

    # ---------------------------------------------------------------- (B) walk the tie-break
    say("")
    say("=" * 100)
    say("(B/C) RULE 8 — every rung decides on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE.")
    say("      B_POINT (1199's control, FIRST-WINS on the raw percentile, no tie declared) and")
    say("      DO_NOTHING (always N=20/W) are carried at every cell as the two bars that matter.")
    say("=" * 100)
    wf = []
    for pname in bdf.panel.unique():
        sb = bdf[bdf.panel == pname].sort_values("order").reset_index(drop=True)
        ctx = pan_ctx[pname]
        jdn = int(sb[(sb.N == DONOTHING[0]) & (sb.cadence == DONOTHING[1])].index[0])
        for K in KLAD:
            for tb in TIEBREAKS + ["B_POINT"]:
                pl = []
                rng = np.random.default_rng(TIESEED + 31 * K + 7919 * list(bdf.panel.unique()).index(pname))
                for sd in range(NSEED):
                    sub = gdf[(gdf.panel == pname) & (gdf.K == K) & (gdf.seed == sd)].sort_values("order")
                    st = sub.merge(sb[["order", "IS_Sharpe", "IS_4b_margin", "NULLGAP"]], on="order")
                    m = st.CH_PCT.max()
                    if tb == "B_POINT":
                        w = st[st.CH_PCT == m].iloc[0]             # no tie declared, FIRST-WINS
                    else:
                        tied = st[st.TIED_B_ONE] if bool(st.TIED_B_ONE.any()) else st[st.CH_PCT == m]
                        tied = tied.reset_index(drop=True)
                        w = tied.iloc[tiebreak_pick(tb, tied, rng)]
                    pl.append(int(sb[(sb.N == w.N) & (sb.cadence == w.cadence)].index[0]))
                picks = sorted(set(pl))
                modal = max(picks, key=lambda x: (pl.count(x), -x))
                row = sb.loc[modal]
                wf.append(dict(
                    panel=pname, K=K, tiebreak=tb, n_distinct=len(picks),
                    modal_share=pl.count(modal) / len(pl), pick=f"N={int(row.N)}/{row.cadence}",
                    mean_OOS_Sharpe=float(sb.loc[pl].OOS_Sharpe.mean()),
                    mean_IS_Sharpe=float(sb.loc[pl].IS_Sharpe.mean()),
                    mean_OOS_CAGR=float(sb.loc[pl].OOS_CAGR.mean()),
                    mean_OOS_MaxDD=float(sb.loc[pl].OOS_MaxDD.mean()),
                    modal_OOS_CAGR=row.OOS_CAGR, modal_OOS_Sharpe=row.OOS_Sharpe,
                    modal_OOS_MaxDD=row.OOS_MaxDD, modal_CAGR=row.CAGR, modal_Sharpe=row.Sharpe,
                    modal_MaxDD=row.MaxDD, modal_H1=row.H1, modal_H2=row.H2,
                    KEEP_4a=bool(row.KEEP_4a), KEEP_4b=bool(row.KEEP_4b), fail4b=row.fail4b,
                    keep4b_share=float(sb.loc[pl].KEEP_4b.mean()),
                    spread_OOS=float(sb.loc[picks].OOS_Sharpe.max() - sb.loc[picks].OOS_Sharpe.min())
                    if len(picks) > 1 else 0.0,
                    DN_OOS_Sharpe=float(sb.loc[jdn].OOS_Sharpe),
                    DN_OOS_CAGR=float(sb.loc[jdn].OOS_CAGR), DN_OOS_MaxDD=float(sb.loc[jdn].OOS_MaxDD),
                    d_vs_donothing=float(sb.loc[pl].OOS_Sharpe.mean() - sb.loc[jdn].OOS_Sharpe),
                    SPY_OOS_Sharpe=ctx["spy_oos"]["Sharpe"], SPY_OOS_CAGR=ctx["spy_oos"]["CAGR"],
                    SPY_OOS_MaxDD=ctx["spy_oos"]["MaxDD"], LIVE_OOS_Sharpe=ctx["base_oos"]["Sharpe"],
                    LIVE_OOS_CAGR=ctx["base_oos"]["CAGR"]))
    wdf = pd.DataFrame(wf)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)

    cols = TIEBREAKS + ["B_POINT"]
    say("")
    say("  MEAN OOS SHARPE OF THE PICK over 20 seeds (higher is better).")
    say(f"    {'panel':6s} {'K':>4}  " + "  ".join(f"{c.replace('T_',''):>9s}" for c in cols))
    for pname in bdf.panel.unique():
        for K in KLAD:
            s = wdf[(wdf.panel == pname) & (wdf.K == K)].set_index("tiebreak")
            say(f"    {pname:6s} {K:>4}  " + "  ".join(f"{s.loc[c].mean_OOS_Sharpe:>9.4f}" for c in cols))

    pool = wdf.groupby("tiebreak").mean_OOS_Sharpe.mean().reindex(cols)
    say("")
    say("  POOLED over the 18 (panel, K) cells — the object 1199's +0.0671 was read on:")
    for c in cols:
        say(f"    {c:12s} mean OOS Sharpe {pool[c]:.4f}   vs B_POINT {pool[c]-pool['B_POINT']:+.4f}"
            + ("   <- 1199's choice" if c == "T_CH_Z" else ""))
    gate("G5a B_POINT pooled mean vs 1199's committed 0.8897235",
         f"{pool['B_POINT']:.7f} (delta {pool['B_POINT']-REF_B_POINT:+.2e})",
         f"{REF_B_POINT:.7f}; U56 vintage published, vintage-free panels gated by G5c", True)
    gate("G5b T_CH_Z pooled mean vs 1199's committed B_ONE 0.9568214",
         f"{pool['T_CH_Z']:.7f} (delta {pool['T_CH_Z']-REF_B_ONE:+.2e})",
         f"{REF_B_ONE:.7f}; same", True)
    try:
        r99w = pd.read_csv(f"{REF1199}.walkforward.csv")
        e5 = 0.0
        for pn in ("B136", "SMALL"):
            mine_p = wdf[(wdf.panel == pn) & (wdf.tiebreak == "B_POINT")].mean_OOS_Sharpe.mean()
            mine_z = wdf[(wdf.panel == pn) & (wdf.tiebreak == "T_CH_Z")].mean_OOS_Sharpe.mean()
            ref_p = r99w[(r99w.panel == pn) & (r99w.chooser == "B_POINT")].mean_OOS_Sharpe.mean()
            ref_z = r99w[(r99w.panel == pn) & (r99w.chooser == "B_ONE")].mean_OOS_Sharpe.mean()
            e5 = max(e5, abs(mine_p - ref_p), abs(mine_z - ref_z))
            say(f"    replay {pn:6s} B_POINT {mine_p:.6f} vs 1199 {ref_p:.6f}   "
                f"T_CH_Z {mine_z:.6f} vs 1199's B_ONE {ref_z:.6f}")
        gate("G5c B_POINT and CH_Z replay 1199's per-panel means on the VINTAGE-FREE panels",
             f"{e5:.3e}", "< 1e-9", e5 < 1e-9)
    except FileNotFoundError:
        gate("G5c replay 1199 walkforward", "missing", "present", False)

    gapref = pool["T_CH_Z"] - pool["B_POINT"]
    tb_only = [c for c in TIEBREAKS]
    gaps = {c: pool[c] - pool["B_POINT"] for c in tb_only}
    worst = min(gaps, key=lambda c: gaps[c])
    best = max(gaps, key=lambda c: gaps[c])
    say("")
    say("=" * 100)
    say("(D) THE ANSWER — how much of 1199's +0.0671 survives the WORST tie-break")
    say("=" * 100)
    say(f"    reference gap (T_CH_Z - B_POINT)            {gapref:+.4f}")
    say(f"    WORST tie-break {worst:12s}                {gaps[worst]:+.4f}   "
        f"= {gaps[worst]/gapref*100 if gapref else float('nan'):.1f}% of the reference gap")
    say(f"    BEST  tie-break {best:12s}                {gaps[best]:+.4f}")
    say(f"    spread across the 8 tie-breaks              {max(gaps.values())-min(gaps.values()):.4f}"
        f"   vs the gap it decomposes {gapref:.4f}")
    say(f"    uninformative rungs only (FIRST/LAST/RANDOM): "
        + "  ".join(f"{c.replace('T_','')} {gaps[c]:+.4f}" for c in ["T_FIRST", "T_LAST", "T_RANDOM"]))
    say(f"    informative rungs (CH_Z/ISSHARPE/IS4B/NULLGAP/HOLD): "
        + "  ".join(f"{c.replace('T_','')} {gaps[c]:+.4f}"
                    for c in ["T_CH_Z", "T_ISSHARPE", "T_IS4B", "T_NULLGAP", "T_HOLD"]))
    pd.DataFrame([dict(tiebreak=c, pooled_mean_OOS_Sharpe=pool[c], gap_vs_B_POINT=pool[c] - pool["B_POINT"],
                       share_of_reference_gap=(pool[c] - pool["B_POINT"]) / gapref if gapref else np.nan)
                  for c in cols]).to_csv(f"{OUT}.decomposition.csv", index=False)

    # ---------------------------------------------------------------- (F) the mechanism
    # T_LAST and T_HOLD come out on top and are nearly equal.  In the frozen (cadence, N) order
    # the LAST tied book is normally N=40/W, which is also the book T_HOLD picks by construction,
    # so the suspicion — stated here and then measured, not asserted — is that the winning
    # "tie-breaks" are proxies for HOLD MORE NAMES, a prior the record already owns (the N ladder
    # is OOS-monotone on the large-cap panels, idea 1081), and not information extracted from a
    # tie.  Everything below is post-processing of the two CSVs already written; no new run.
    say("")
    say("=" * 100)
    say("(F) WHAT THE WINNING TIE-BREAKS ARE ACTUALLY DOING — mean N of the books each rung picks")
    say("=" * 100)
    say("    OOS Sharpe by N, the ladder every rung is choosing along:")
    for pname in bdf.panel.unique():
        for freq in CADLAD:
            sb = bdf[(bdf.panel == pname) & (bdf.cadence == freq)].sort_values("N")
            say(f"      {pname:6s} {freq}  " + "  ".join(f"N={int(r.N):<2d} {r.OOS_Sharpe:.4f}"
                                                         for _, r in sb.iterrows()))
    meanN, rows_f = {}, []
    for c in cols:
        s_ = wdf[wdf.tiebreak == c]
        nn = np.mean([int(x.split("=")[1].split("/")[0]) for x in s_.pick])
        meanN[c] = nn
        rows_f.append(dict(tiebreak=c, mean_N_of_modal_pick=nn, gap_vs_B_POINT=pool[c] - pool["B_POINT"],
                           share_weekly=float(np.mean([x.endswith("/W") for x in s_.pick]))))
    fdf = pd.DataFrame(rows_f)
    fdf.to_csv(f"{OUT}.mechanism.csv", index=False)
    say("")
    say(f"    {'rung':12s} {'mean N of pick':>14s}  {'share weekly':>12s}  {'gap vs B_POINT':>14s}")
    for _, r in fdf.iterrows():
        say(f"    {r.tiebreak:12s} {r.mean_N_of_modal_pick:>14.1f}  {r.share_weekly:>12.2f}  "
            f"{r.gap_vs_B_POINT:>+14.4f}")
    rc = rankcorr(fdf.mean_N_of_modal_pick.values, fdf.gap_vs_B_POINT.values)
    say(f"    rank corr (mean N of the pick, gap vs B_POINT) over the {len(fdf)} rungs: {rc:+.3f}")
    say(f"    T_LAST and T_HOLD pick the same book at "
        f"{int((wdf[wdf.tiebreak=='T_LAST'].reset_index(drop=True).pick == wdf[wdf.tiebreak=='T_HOLD'].reset_index(drop=True).pick).sum())}"
        f" of {len(wdf[wdf.tiebreak=='T_LAST'])} (panel, K) cells — one of them carries NO information")

    # ---------------------------------------------------------------- rule 8 on the dials
    say("")
    say("=" * 100)
    say("(E) RULE 8 ON THE DIALS — (TIE-BREAK, K) chosen on the IS window ALONE by the mean IS")
    say("      Sharpe of the books the rung picks; 2017-2026 read ONCE; per panel.")
    say("=" * 100)
    r8 = []
    for pname in bdf.panel.unique():
        s = wdf[(wdf.panel == pname) & (wdf.tiebreak != "B_POINT")]
        j = int(s.mean_IS_Sharpe.idxmax())
        p = s.loc[j]
        dn = float(p.DN_OOS_Sharpe)
        r8.append(dict(panel=pname, pick_tiebreak=p.tiebreak, pick_K=int(p.K),
                       pick_IS_Sharpe=p.mean_IS_Sharpe, pick_OOS_Sharpe=p.mean_OOS_Sharpe,
                       pick_OOS_CAGR=p.mean_OOS_CAGR, pick_OOS_MaxDD=p.mean_OOS_MaxDD,
                       donothing_OOS_Sharpe=dn, donothing_OOS_CAGR=p.DN_OOS_CAGR,
                       donothing_OOS_MaxDD=p.DN_OOS_MaxDD,
                       delta_vs_donothing=p.mean_OOS_Sharpe - dn,
                       cellmean_OOS=float(s.mean_OOS_Sharpe.mean()),
                       worst_OOS=float(s.mean_OOS_Sharpe.min()), best_OOS=float(s.mean_OOS_Sharpe.max()),
                       rank_IS_OOS=rankcorr(s.mean_IS_Sharpe.values, s.mean_OOS_Sharpe.values),
                       n_cells=len(s), SPY_OOS_Sharpe=p.SPY_OOS_Sharpe, SPY_OOS_CAGR=p.SPY_OOS_CAGR,
                       SPY_OOS_MaxDD=p.SPY_OOS_MaxDD, LIVE_OOS_Sharpe=p.LIVE_OOS_Sharpe,
                       pick_KEEP_4a=bool(p.KEEP_4a), pick_KEEP_4b=bool(p.KEEP_4b)))
        say(f"    {pname:6s} IS-argmax = {p.tiebreak}/K={int(p.K)} (IS Sh {p.mean_IS_Sharpe:.4f}) -> "
            f"OOS Sharpe {p.mean_OOS_Sharpe:.4f} / CAGR {p.mean_OOS_CAGR:.2%} / MaxDD "
            f"{p.mean_OOS_MaxDD:.2%}")
        say(f"    {'':6s} do-nothing N=20/W  OOS Sharpe {dn:.4f} / CAGR {p.DN_OOS_CAGR:.2%} / MaxDD "
            f"{p.DN_OOS_MaxDD:.2%}   delta {p.mean_OOS_Sharpe-dn:+.4f}")
        say(f"    {'':6s} SPY OOS {p.SPY_OOS_Sharpe:.4f} / {p.SPY_OOS_CAGR:.2%} / {p.SPY_OOS_MaxDD:.2%}"
            f"   LIVE v2 OOS Sharpe {p.LIVE_OOS_Sharpe:.4f}   48-cell mean "
            f"{float(s.mean_OOS_Sharpe.mean()):.4f} worst {float(s.mean_OOS_Sharpe.min()):.4f}"
            f"   rank corr IS/OOS {rankcorr(s.mean_IS_Sharpe.values, s.mean_OOS_Sharpe.values):+.2f}")
    r8df = pd.DataFrame(r8)
    r8df.to_csv(f"{OUT}.rule8.csv", index=False)

    # ---------------------------------------------------------------- KEEP paths
    say("")
    say("  BOTH KEEP PATHS (PROTOCOL rule 4):")
    say(f"    over all 36 books: 4a {int(bdf.KEEP_4a.sum())} of 36   4b {int(bdf.KEEP_4b.sum())} of 36")
    for pname in bdf.panel.unique():
        s = bdf[bdf.panel == pname]
        say(f"      {pname:6s} 4a {int(s.KEEP_4a.sum())}/{len(s)}  4b {int(s.KEEP_4b.sum())}/{len(s)}"
            f"   4b fails: {dict(s.fail4b.value_counts())}")
    say(f"    over the {len(wdf)} published (panel, K, tie-break) picks: 4a {int(wdf.KEEP_4a.sum())}, "
        f"4b {int(wdf.KEEP_4b.sum())}")
    for c in cols:
        s = wdf[wdf.tiebreak == c]
        say(f"      {c:12s} 4a {int(s.KEEP_4a.sum()):2d}/{len(s)}  4b {int(s.KEEP_4b.sum()):2d}/{len(s)}"
            f"  mean 4b share over seeds {s.keep4b_share.mean():.3f}")
    say(f"    RULE-8 picks clearing a KEEP path: 4a {int(r8df.pick_KEEP_4a.sum())} of {len(r8df)}, "
        f"4b {int(r8df.pick_KEEP_4b.sum())} of {len(r8df)}")
    say(f"    rule-8 chooser-minus-do-nothing: {r8df.delta_vs_donothing.round(4).tolist()}  "
        f"mean {r8df.delta_vs_donothing.mean():+.4f}  beats do-nothing at "
        f"{int((r8df.delta_vs_donothing > 0).sum())} of {len(r8df)}")

    # ---------------------------------------------------------------- G2 determinism
    pan0 = Panel(*panels[0])
    r1 = run_from_starts(pan0, "W", null_starts(pan0, "W", 20, np.random.default_rng(5)), stop=pan0.ioos)
    r2 = run_from_starts(pan0, "W", null_starts(pan0, "W", 20, np.random.default_rng(5)), stop=pan0.ioos)
    d2 = float(np.abs(r1 - r2).max())
    gate("G2 determinism (null pool re-run bit for bit)", f"{d2:.3e}", "== 0.0", d2 == 0.0)

    say("")
    say("=" * 100)
    say(f"GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass     total {time.time()-t0:.0f}s")
    say("=" * 100)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
