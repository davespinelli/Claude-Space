#!/usr/bin/env python3
"""Idea 1613 (lane C, 2026-09-20): is EVERY committed CADENCE claim in the record really a
c-STAR claim that happens to have been QUOTED AT ONE RUNG?

WHY THIS IDEA.  Idea 1586 (lane C, 2026-09-19) established two things that, put together, make
every cadence verdict in this repository suspect.  First, the whole cost axis is EXACT off two
cached rungs: engine.backtest subtracts `turnover * c / 1e4` from the daily return and never
feeds the charge back into position drift, so `r(c) = r_gross - turnover * c / 1e4` reproduces a
fresh engine run to 0.000e+00.  Second, on the frozen anchor's own cell the weekly cadence beats
its quarterly twin by only **c* = 12.4 bps** of cost, with a median c* of 19.2 bps over 72 pairs
and 25 of 58 rivals already ahead at the protocol's 10.  A verdict whose sign turns over inside
a band that narrow is not a fact about cadence; it is a fact about the rung it was quoted at.

PROTOCOL rule 2 binds every backtest to ONE rung (10 bps).  Every cadence verdict in
LEADERBOARD.md and CHANGELOG.md is therefore a point reading of a function of cost, and this run
asks, mechanically, how many of those points sit on a slope steep enough to change sign inside
the range a real book might actually pay.

THE TWO HALVES.

  CENSUS (over the committed record, no prices).  Extract every CADENCE CLAIM from
  research/LEADERBOARD.md and research/CHANGELOG.md under a rule fixed BEFORE the run:

     BROAD  a sentence naming >= 2 DISTINCT cadence tokens from {daily, weekly, monthly,
            quarterly} (or an explicit pair token such as `W->M`, `weekly -> monthly`)
            AND carrying a COMPARATIVE token (beat / better / worse / cost / dominat / win /
            lose / prefer / argmax / invert / faster / slower / outperform / edge / gain /
            Delta / c*).
     STRICT the BROAD subset that also carries an EXPLICIT ORDERED PAIR token, i.e. a claim
            that names the two cadences being compared and the direction between them.

  Each claim is then classified by the cost rungs its own sentence QUOTES:
     POINT_IMPLICIT  no `N bps` anywhere in the sentence -> the protocol's single 10 bps rung
     POINT_EXPLICIT  exactly one distinct rung quoted
     INTERVAL        two or more distinct rungs quoted (a ladder, not a point)
     CSTAR           the sentence names a break-even / c* / crossover cost
  Published in full to `.census.csv`, every extracted sentence, so the classification is
  auditable rather than asserted.  NOISE IS STATED, NOT HIDDEN: the BROAD rule will catch
  sentences where "weekly" means the cache refresh cadence of rule 9 rather than a rebalance;
  that is why the STRICT denominator is carried alongside and why the CSV is complete.

  RE-PRICING (real books, the capital arm).  A cadence corpus is rebuilt from scratch and every
  pairwise cadence verdict in it is re-read as a FUNCTION OF COST rather than a point:

     DIAL 1  CADENCE {D, W, M, Q}                 the thing every censused claim is about
     DIAL 2  CHOOSER COST RUNG {5, 10, 25, 50}    the rung a rule-8 chooser is allowed to quote
                                                  its cadence verdict at.  This is the idea's
                                                  own question turned into a tunable: if the
                                                  rung is not a free parameter, picking it
                                                  cannot change the OOS result.
  AND NO MORE (PROTOCOL rule 4).  Reported axes, never tuned: FRAME {LIVE, INC}, PANEL {U56,
  B136, SMALL} (rule 9), WINDOW {FULL, H1, H2, IS, OOS}, and the published cost ladder
  {0, 5, 10, 25, 50} bps.

  FRAME LIVE = the live RULES v2 shape (`baseline.band_state`, 200d +/-3% hysteresis band, hold
               every IN name at gross/N of NAV with N = names priced that day, gated-out weight
               to CASH, never re-spread), gross 0.75.  Cadence W IS the live book, bit-for-bit.
  FRAME INC  = the frozen 2026-09-04 KEEP-4b incumbent (composite momentum over (21,252)/
               (0,126)/(0,63), N = 20, H = 126-day min hold, 200d MA gate, vol20 < 0.60),
               gross 0.75.  Cadence W IS the committed anchor: 15.80% / 1.1537 / -19.13% full,
               17.32% / 1.1857 OOS.

THE THREE QUESTIONS, STATED BEFORE THE RUN:
  Q1 CENSUS.   What share of committed cadence claims are quoted at a SINGLE rung?
  Q2 c*.       Re-priced as a function of cost, what share of pairwise cadence verdicts FLIP
               sign somewhere inside 5-50 bps?  Published per pair with its exact c*, the
               number of crossings, and the sign at the protocol's binding 10.
  Q3 VERDICT.  Not just the Sharpe ordering but the KEEP VERDICT itself: for each book, over
               what INTERVAL of cost rungs does its 4a / 4b verdict actually hold?  A verdict
               whose interval does not contain the whole 5-50 band is a verdict that should
               never have been quoted as a point.
  Plus the constructive half the idea asks for, answered from Q2/Q3, and rule 8 with 2017-2026
  read EXACTLY ONCE.

WHAT WOULD MAKE THIS A FINDING.  If the flip share inside 5-50 bps is LOW, the record's habit of
quoting one rung is harmless and PROTOCOL rule 2 needs no change; the 1586 headline would then be
a property of one unusually close pair, not of cadence claims generally.  If it is HIGH, then a
large share of the committed cadence record is rung-conditional and rule 2 should require an
interval.  Both outcomes are reported; nothing is tuned until it works.

GATES.  G0 sample >= 10y (rule 1).  G1 fast_run vs `engine.backtest` (returns AND turnover) at
every cadence on every panel.  G2 the DERIVED cost rungs vs fresh engine runs at 25 and 50 bps.
G3 LIVE/W replays `baseline.compare`'s RULES v2 baseline row.  G4 INC/W replays the committed
2026-09-04 anchor.  G5 exactly two tuned parameters.  G6 no chooser reads a row on or after
2017-01-01 (tested on truncated input, not asserted).  G7 every corpus cell published.  G8 no
leverage, no shorting.  G9 the c* solver re-derives 1586's committed headline c* for the anchor's
own W-vs-Q pair.  G10 PUBLISHED: turnover per cell, and the census denominators.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps binding for every verdict, no leverage/shorting);
rule 3 (live RULES v2 baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_every-cadence-claim-as-a-c-star_C.py
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-20", "every-cadence-claim-as-a-c-star"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_MAXVOL, GROSS, BAND = 20, 126, 0.60, 0.75, 0.03
GRID_CAD = ["D", "W", "M", "Q"]
CHOOSE_RUNGS = [5.0, 10.0, 25.0, 50.0]          # DIAL 2
PUB_RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]        # reported axis
BINDING = 10.0                                   # PROTOCOL rule 2
BAND_LO, BAND_HI = 5.0, 50.0                     # the idea's own 5-50 bps question
FRAMES = ["LIVE", "INC"]
ANCHOR_CAD = "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
ANCHOR_INC = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oCAGR=0.1732, oSharpe=1.1857)
CSTAR_1586 = 12.4          # 1586's committed headline: U56 / INC / MAXVOL 0.60, W vs Q
WINDOWS = ["FULL", "H1", "H2", "IS", "OOS"]

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ==================================================================== PART 1: THE CENSUS
CAD_WORDS = {"daily": "D", "weekly": "W", "monthly": "M", "quarterly": "Q"}
PAIR_RE = re.compile(
    r"(?:\b([DWMQ])\s*(?:->|-->|→|>)\s*([DWMQ])\b)"
    r"|(?:\b(daily|weekly|monthly|quarterly)\s*(?:->|-->|→|vs\.?|versus|over|beats?|minus|,\s*not)\s*"
    r"(daily|weekly|monthly|quarterly)\b)"
    r"|(?:\b([DWMQ])\s*(?:vs\.?|versus)\s*([DWMQ])\b)", re.I)
CMP_RE = re.compile(
    r"(beat|better|worse|costs?\b|dominat|wins?\b|loses?\b|prefer|argmax|invert|faster|slower|"
    r"outperform|edge|gain|rebate|Δ|delta|c\*|break-?even|no worse|cheaper|dearer)", re.I)
CSTAR_RE = re.compile(r"(c\*|break-?even|cross-?over|crossing cost)", re.I)
RUNG_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:/\s*\d+(?:\.\d+)?\s*)*bps", re.I)
RUNGS_IN_RE = re.compile(r"(\d+(?:\.\d+)?)")


def sentences(text):
    t = re.sub(r"\s+", " ", text).strip()
    if not t:
        return []
    return [s for s in re.split(r"(?<=[.;:!?])\s+(?=[A-Z0-9*_`(\[])", t) if s]


def quoted_rungs(s):
    """Every distinct cost rung the sentence itself quotes, including `0/10/25/50 bps` ladders."""
    out = []
    for m in RUNG_RE.finditer(s):
        out += [float(x) for x in RUNGS_IN_RE.findall(m.group(0))]
    return sorted(set(out))


def census():
    recs = []
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text()
    for ln in lb.split("\n"):
        if not ln.startswith("| 20"):
            continue
        cells = ln.split("|")
        rid = cells[1].strip() if len(cells) > 1 else "?"
        idea = re.match(r"\s*([0-9]+)", cells[2]) if len(cells) > 2 else None
        recs.append(("LEADERBOARD.md", rid, idea.group(1) if idea else "", ln))
    cl = (ROOT / "research" / "CHANGELOG.md").read_text()
    blocks = re.split(r"\n(?=## )", cl)
    for b in blocks:
        h = b.split("\n", 1)[0]
        d = re.search(r"(20\d\d-\d\d-\d\d)", h)
        i = re.search(r"idea\s+([0-9]+)", h, re.I)
        recs.append(("CHANGELOG.md", d.group(1) if d else "?", i.group(1) if i else "", b))

    rows = []
    for src, rid, idea, text in recs:
        for s in sentences(text):
            toks = {c for w, c in CAD_WORDS.items() if re.search(rf"\b{w}\b", s, re.I)}
            pair = PAIR_RE.search(s)
            if pair:
                toks |= {g.upper()[0] for g in pair.groups() if g}
            if len(toks) < 2 or not CMP_RE.search(s):
                continue
            rg = quoted_rungs(s)
            cst = bool(CSTAR_RE.search(s))
            if cst:
                klass = "CSTAR"
            elif len(rg) >= 2:
                klass = "INTERVAL"
            elif len(rg) == 1:
                klass = "POINT_EXPLICIT"
            else:
                klass = "POINT_IMPLICIT"
            rows.append(dict(source=src, record=rid, idea=idea, strict=bool(pair),
                             cadences="".join(sorted(toks)), n_rungs=len(rg),
                             rungs=";".join(f"{x:g}" for x in rg), klass=klass,
                             covers_5_50=bool(rg and min(rg) <= BAND_LO and max(rg) >= BAND_HI),
                             sentence=s[:400]))
    return pd.DataFrame(rows)


# ==================================================================== PART 2: THE CORPUS
def mech(q):
    """The frozen incumbent's composite: three momentum legs, cross-sectional pct ranks, halved
    below the 200d MA.  Identical in form to baseline.score without the 1/sqrt(vol) scaler."""
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
    def __init__(self, name, px, invest, live_cols):
        self.name, self.px, self.invest, self.live_cols = name, px, invest, live_cols
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.ilive = np.array([cols.index(c) for c in live_cols])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.above, self.vol20 = above, vol20
        self.band = band_state(px[live_cols], BAND).values
        self.lpriced = px[live_cols].notna().values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


def frame_live(pan):
    """Live RULES v2 band shape at GROSS = 1.0, shifted so row t carries the close-(t-1)
    decision -- exactly engine.backtest's `weights.shift(1)` convention."""
    T, M = pan.rets.shape
    e = pan.lpriced.astype(float)
    n = e.sum(axis=1)
    ew = np.nan_to_num(np.divide(e, np.where(n == 0, np.nan, n)[:, None]), nan=0.0)
    w = np.where(pan.band, ew, 0.0)
    W = np.zeros((T, M))
    W[:, pan.ilive] = w
    return np.vstack([np.zeros((1, M)), W[:-1]])


def frame_inc(pan, reb, N=I_N, H=I_H, m=I_MAXVOL, lag=1):
    """Frozen min-hold momentum selection at GROSS = 1.0, eligibility `above 200d MA and
    vol20 < m`.  Row t already carries the close-(t-1) decision (ts = t - lag)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    elig = pan.above & (pan.vol20 < m)
    pr = pan.priced[:, pan.iinv]
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
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
            k[~(elig[ts] & pr[ts])] = np.inf
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


def run_cell(pan, frame, reb, g=GROSS):
    """Hold g * frame on the schedule, drift between rebalances, de-gross to 0%-yielding cash.
    Returns GROSS-OF-COST daily returns, the turnover path, max realised gross and the gross
    path -- identical semantics to engine.backtest, gated at G1."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max, gsum


# ==================================================================== metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a against the LIVE book at the SAME cost rung; 4b against SPY buy-and-hold (cost-free,
    the record's own convention -- see idea 1490's standing caveat)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def sharpe_at(rg, tu, c):
    return sharpe(rg - tu * c / 1e4)


class SharpeCurve:
    """Sharpe of `rg - tu*c/1e4` as a CLOSED FORM in c, so the dense cost scan costs O(1) per
    rung instead of a re-reduction over the window.  With k = c/1e4,
        mean(x) = m_r - k*m_t ,  var(x) = v_r - 2k*cov + k^2*v_t   (ddof = 0),
    both exact.  Gated against the direct reduction at G11."""

    def __init__(self, rg, tu):
        rg = np.asarray(rg, float)
        tu = np.asarray(tu, float)
        self.n = len(rg)
        self.m_r, self.m_t = rg.mean(), tu.mean()
        dr, dt = rg - self.m_r, tu - self.m_t
        self.v_r = float((dr * dr).mean())
        self.v_t = float((dt * dt).mean())
        self.cov = float((dr * dt).mean())

    def __call__(self, c):
        k = np.asarray(c, float) / 1e4
        mu = self.m_r - k * self.m_t
        var = self.v_r - 2.0 * k * self.cov + k * k * self.v_t
        var = np.where(var > 0, var, np.nan)
        return mu * np.sqrt(252.0) / np.sqrt(var)


def crossings(rgA, tuA, rgB, tuB, lo=0.0, hi=BAND_HI, step=0.05):
    """Every c in [lo, hi] where Sharpe_B(c) - Sharpe_A(c) changes sign, to 1e-6 bps by
    bisection off a dense scan.  The cost axis is EXACT (G2), so this is not a re-backtest."""
    SA, SB = SharpeCurve(rgA, tuA), SharpeCurve(rgB, tuB)
    grid = np.arange(lo, hi + 1e-9, step)
    f = SB(grid) - SA(grid)
    g = lambda c: float(SB(c) - SA(c))
    xs = []
    for i in range(len(grid) - 1):
        a, b = f[i], f[i + 1]
        if a == 0.0:
            xs.append(float(grid[i]))
        elif a * b < 0:
            x0, x1 = grid[i], grid[i + 1]
            for _ in range(60):
                mid = 0.5 * (x0 + x1)
                if g(mid) * a > 0:
                    x0 = mid
                else:
                    x1 = mid
            xs.append(0.5 * (x0 + x1))
    return xs, grid, f


def runs_of_true(grid, flags):
    """Contiguous [lo, hi] runs of True on the cost grid, as a compact string."""
    out, start = [], None
    for i, v in enumerate(flags):
        if v and start is None:
            start = grid[i]
        if (not v or i == len(flags) - 1) and start is not None:
            end = grid[i] if v else grid[i - 1]
            out.append((float(start), float(end)))
            start = None
    return out


def fmt_runs(rs):
    return "none" if not rs else ";".join(f"[{a:g},{b:g}]" for a, b in rs)


# ==================================================================== choosers (rule 8)
def chooser_sharpe(ispk):
    return max(GRID_CAD, key=lambda c: (ispk[c]["Sharpe"], -GRID_CAD.index(c)))


def chooser_memo(ispk, dd_bar, cagr_bar, anchor):
    ok = [c for c in GRID_CAD if ispk[c]["MaxDD"] >= dd_bar and ispk[c]["CAGR"] >= cagr_bar]
    if not ok:
        return anchor, True
    return min(ok, key=lambda c: (ispk[c]["turn"], GRID_CAD.index(c))), False


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1613 (lane C, 2026-09-20) — is EVERY committed CADENCE claim a c-STAR claim that")
    say("happens to have been QUOTED AT ONE RUNG?  Census the record, then re-price the whole")
    say("cost axis EXACTLY and ask what share of cadence verdicts flip inside 5-50 bps.")
    say(f"DIALS: CADENCE {GRID_CAD}  x  CHOOSER COST RUNG {CHOOSE_RUNGS} bps.  Nothing else tuned.")
    say(f"REPORTED AXES: FRAME {FRAMES} x PANEL [U56, B136, SMALL] x WINDOW {WINDOWS} x "
        f"published rungs {PUB_RUNGS} bps.")
    say("=" * 118)

    # ---------------------------------------------------------------- PART 1
    say("\n" + "=" * 118)
    say("PART 1 / Q1 — CENSUS OF COMMITTED CADENCE CLAIMS (LEADERBOARD.md + CHANGELOG.md)")
    say("=" * 118)
    CEN = census()
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    nB, nS = len(CEN), int(CEN.strict.sum())
    say(f"  BROAD rule: {nB} cadence-comparison sentences.  STRICT (explicit ordered pair): {nS}.")
    for name, sub in (("BROAD", CEN), ("STRICT", CEN[CEN.strict])):
        vc = sub.klass.value_counts().to_dict()
        pt = int(vc.get("POINT_IMPLICIT", 0) + vc.get("POINT_EXPLICIT", 0))
        say(f"    {name:<6} n={len(sub):<5} POINT_IMPLICIT {vc.get('POINT_IMPLICIT',0):<5} "
            f"POINT_EXPLICIT {vc.get('POINT_EXPLICIT',0):<4} INTERVAL {vc.get('INTERVAL',0):<4} "
            f"CSTAR {vc.get('CSTAR',0):<4} -> quoted at ONE rung: {pt}/{len(sub)} "
            f"({pt/max(len(sub),1):.1%})")
        say(f"    {name:<6} claims whose own quoted ladder SPANS the whole {BAND_LO:g}-{BAND_HI:g} "
            f"bps band: {int(sub.covers_5_50.sum())} of {len(sub)} "
            f"({sub.covers_5_50.mean() if len(sub) else 0:.1%})")
    say(f"  By source: " + ", ".join(f"{k} {v}" for k, v in CEN.source.value_counts().items()))
    publish("Q1 census denominators", f"BROAD {nB}, STRICT {nS}, "
            f"one-rung share BROAD {(CEN.klass.isin(['POINT_IMPLICIT','POINT_EXPLICIT'])).mean():.4f}")
    say("  NOISE, stated: the BROAD rule cannot tell a REBALANCE cadence from rule 9's WEEKLY "
        "cache refresh or a 'monthly' return series; every extracted sentence is in .census.csv "
        "so the reader can re-classify.  The STRICT denominator carries the claims that name "
        "both cadences and a direction.")

    # ---------------------------------------------------------------- PART 2
    say("\n" + "=" * 118)
    say("PART 2 — THE CADENCE CORPUS (24 books = 2 frames x 3 panels x 4 cadences)")
    say("=" * 118)
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} of {len(pxS.columns)-1} priced names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"], list(pxU.columns)),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"], list(pxB.columns)),
              Panel("SMALL", pxS, inv, inv)]
    say("  COLUMN SETS, stated not glossed: on U56 and B136 the LIVE frame trades the SAME column "
        "set as the committed `baseline.rules_v2_weights` (SPY included, because it is a universe "
        "constituent there).  On SMALL, SPY is a joined BENCHMARK, not a constituent.")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every LEVEL below is an UPPER BOUND.  What "
        "survives the bias is the CONTRAST between cadences on the same names and the same days, "
        "and above all the SHAPE of that contrast in cost, which is arithmetic on one tape.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G5 exactly two tuned parameters",
         f"CADENCE {len(GRID_CAD)} x CHOOSER RUNG {len(CHOOSE_RUNGS)}", "2 dials",
         len(GRID_CAD) == 4 and len(CHOOSE_RUNGS) == 4)

    say("\n  [G1/G2] fast_run vs engine.backtest (returns AND turnover), every cadence, every panel")
    d1r = d1t = d2 = 0.0
    for pan in panels:
        wlive = (rules_v2_weights(pan.px[pan.live_cols], gross=GROSS)
                 .reindex(pan.idx).fillna(0.0).reindex(columns=pan.px.columns).fillna(0.0))
        fl = frame_live(pan)
        for cad in GRID_CAD:
            reb = pan.reb_rows(cad)
            rg, tu, _, _ = run_cell(pan, fl, reb)
            for c in (10.0, 25.0, 50.0):
                eng = backtest(pan.px, wlive, cost_bps=c, freq=cad)
                dev = float(np.max(np.abs((rg - tu * c / 1e4) - eng["returns"].values)))
                if c == 10.0:
                    d1r = max(d1r, dev)
                    d1t = max(d1t, float(np.max(np.abs(tu - eng["turnover"].values))))
                else:
                    d2 = max(d2, dev)
    gate("G1 fast_run vs engine.backtest, RETURNS at 10 bps (max |dev| over 12 panel x cadence runs)",
         f"{d1r:.3e}", "< 1e-12", d1r < 1e-12)
    gate("G1b fast_run vs engine.backtest, TURNOVER (max |dev|)", f"{d1t:.3e}", "< 1e-12", d1t < 1e-12)
    gate("G2 DERIVED 25 and 50 bps rungs vs FRESH engine runs (max |dev| over 24 comparisons)",
         f"{d2:.3e}", "< 1e-12", d2 < 1e-12)

    # G11: the closed-form Sharpe(c) must equal the direct reduction, or every c* is fiction
    rng = np.random.default_rng(0)
    dmax = 0.0
    _pan = panels[0]
    _fl = frame_live(_pan)
    _rg, _tu, _, _ = run_cell(_pan, _fl, _pan.reb_rows("W"))
    _sc = SharpeCurve(_rg[WARMUP:], _tu[WARMUP:])
    for c in list(np.linspace(0.0, BAND_HI, 41)) + list(rng.uniform(0, BAND_HI, 20)):
        dmax = max(dmax, abs(float(_sc(c)) - sharpe_at(_rg[WARMUP:], _tu[WARMUP:], c)))
    gate("G11 closed-form Sharpe(c) vs the direct reduction (61 rungs)", f"{dmax:.3e}",
         "< 1e-12", dmax < 1e-12)

    grid, wsum_global = [], 0.0
    RG, TU, BARS = {}, {}, {}
    g3 = {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        h = (T - WARMUP) // 2
        WIN = {"FULL": slice(WARMUP, T), "H1": slice(WARMUP, WARMUP + h),
               "H2": slice(WARMUP + h, T), "IS": slice(WARMUP, i_oos), "OOS": slice(i_oos, T)}
        bars = dict(i_oos=i_oos, win=WIN,
                    spy={w: bmpack(pan.spy[s]) for w, s in WIN.items()}, live={})
        for c in PUB_RUNGS:
            lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=c, freq="W")["returns"].values
            bars["live"][c] = {w: bmpack(lr[s]) for w, s in WIN.items()}
            if c == BINDING:
                g3[pan.name] = bars["live"][c]["FULL"]
        BARS[pan.name] = bars
        sp = bars["spy"]["FULL"]
        say(f"\n  [{pan.name}]  SPY FULL {sp['CAGR']:.2%} / {sp['Sharpe']:.4f} / {sp['MaxDD']:.2%}  "
            f"|  4b bars: DD cap {DD_CAP*sp['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*sp['CAGR']:.2%}")
        spo = bars["spy"]["OOS"]
        say(f"           SPY OOS  {spo['CAGR']:.2%} / {spo['Sharpe']:.4f} / {spo['MaxDD']:.2%}  |  "
            f"OOS bars: DD cap {DD_CAP*spo['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spo['CAGR']:.2%}")
        L = bars["live"][BINDING]["FULL"]
        say(f"           RULES v2 live @10bps  {L['CAGR']:.2%} / {L['Sharpe']:.4f} / {L['MaxDD']:.2%}"
            f"  H1/H2 {L['H1']:.3f}/{L['H2']:.3f}  (OOS {bars['live'][BINDING]['OOS']['Sharpe']:.4f})")

        fl = frame_live(pan)
        for fr in FRAMES:
            for cad in GRID_CAD:
                reb = pan.reb_rows(cad)
                fm = fl if fr == "LIVE" else frame_inc(pan, reb)
                rg, tu, ws, gs = run_cell(pan, fm, reb)
                RG[(pan.name, fr, cad)] = rg
                TU[(pan.name, fr, cad)] = tu
                wsum_global = max(wsum_global, ws)
                yrs = (T - WARMUP) / 252.0
                nheld = float(np.mean((fm[WARMUP:] > 0).sum(axis=1)))
                for c in PUB_RUNGS:
                    r = rg - tu * c / 1e4
                    row = dict(panel=pan.name, frame=fr, cadence=cad, cost_bps=c,
                               turnover_yr=float(tu[WARMUP:].sum() / yrs),
                               drag_bpyr=float(tu[WARMUP:].sum() / yrs) * c,
                               mean_gross=float(np.mean(gs[WARMUP:])), mean_names=nheld,
                               is_anchor=bool(cad == ANCHOR_CAD))
                    for w, s in WIN.items():
                        m = triple(r[s])
                        row[f"{w}_CAGR"], row[f"{w}_Sharpe"], row[f"{w}_MaxDD"] = \
                            m["CAGR"], m["Sharpe"], m["MaxDD"]
                    k4a, k4b, _, h1, h2, legs = keep_paths(r[WIN["FULL"]], bars["spy"]["FULL"],
                                                           bars["live"][c]["FULL"])
                    k4aO, k4bO, _, _, _, legsO = keep_paths(r[WIN["OOS"]], bars["spy"]["OOS"],
                                                             bars["live"][c]["OOS"])
                    row.update(H1=h1, H2=h2, keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO,
                               keep4b_oos=k4bO, leg_H1=legs["H1"], leg_H2=legs["H2"],
                               leg_DD=legs["DD"], leg_CAGR=legs["CAGR"], oleg_H1=legsO["H1"],
                               oleg_H2=legsO["H2"], oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"])
                    grid.append(row)
        say(f"    [{pan.name}] 8 books x {len(PUB_RUNGS)} published rungs done "
            f"({time.time()-t0:.0f}s elapsed)")

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G7 every corpus cell published", f"{len(G)} rows in {Path(OUT).name}.grid.csv",
         f"{3*2*4*len(PUB_RUNGS)} = 3 panels x 2 frames x 4 cadences x {len(PUB_RUNGS)} rungs",
         len(G) == 3 * 2 * 4 * len(PUB_RUNGS))
    gate("G8 no leverage, no shorting (max realised target gross)", f"{wsum_global:.4f}",
         f"<= {GROSS:.4f}", wsum_global <= GROSS + 1e-12)

    lv = G[(G.panel == "U56") & (G.frame == "LIVE") & (G.cadence == "W") &
           (G.cost_bps == BINDING)].iloc[0]
    b = g3["U56"]
    d3 = max(abs(lv["FULL_CAGR"] - b["CAGR"]), abs(lv["FULL_Sharpe"] - b["Sharpe"]),
             abs(lv["FULL_MaxDD"] - b["MaxDD"]))
    gate("G3 LIVE/W on U56 replays baseline.compare's RULES v2 row", f"{d3:.3e}",
         "< 1e-12 (it IS the same book)", d3 < 1e-12)
    ic = G[(G.panel == "U56") & (G.frame == "INC") & (G.cadence == "W") &
           (G.cost_bps == BINDING)].iloc[0]
    d4 = max(abs(ic["FULL_CAGR"] - ANCHOR_INC["CAGR"]), abs(ic["FULL_Sharpe"] - ANCHOR_INC["Sharpe"]),
             abs(ic["FULL_MaxDD"] - ANCHOR_INC["MaxDD"]), abs(ic["OOS_CAGR"] - ANCHOR_INC["oCAGR"]),
             abs(ic["OOS_Sharpe"] - ANCHOR_INC["oSharpe"]))
    gate("G4 INC/W on U56 replays the committed 2026-09-04 anchor", f"{d4:.3e}",
         "< 5e-4 (committed to 4 dp)", d4 < 5e-4)

    # ---------------------------------------------------------------- PART 3 / Q2
    say("\n" + "=" * 118)
    say(f"PART 3 / Q2 — EVERY PAIRWISE CADENCE VERDICT RE-PRICED AS A FUNCTION OF COST.")
    say(f"      A verdict is sign(Sharpe_B(c) - Sharpe_A(c)).  It is quoted at {BINDING:g} bps.")
    say(f"      It FLIPS if that sign differs anywhere in [{BAND_LO:g}, {BAND_HI:g}] bps.")
    say("=" * 118)
    PAIRS = [(a, b) for i, a in enumerate(GRID_CAD) for b in GRID_CAD[i + 1:]]
    cs = []
    for pan in panels:
        WIN = BARS[pan.name]["win"]
        for fr in FRAMES:
            for (A, B) in PAIRS:
                for w in WINDOWS:
                    s = WIN[w]
                    rgA, tuA = RG[(pan.name, fr, A)][s], TU[(pan.name, fr, A)][s]
                    rgB, tuB = RG[(pan.name, fr, B)][s], TU[(pan.name, fr, B)][s]
                    xs, grid_c, f = crossings(rgA, tuA, rgB, tuB)
                    d10 = sharpe_at(rgB, tuB, BINDING) - sharpe_at(rgA, tuA, BINDING)
                    inb = (grid_c >= BAND_LO) & (grid_c <= BAND_HI)
                    flip = bool(np.any(np.sign(f[inb]) * np.sign(d10) < 0))
                    xs_in = [x for x in xs if BAND_LO <= x <= BAND_HI]
                    cs.append(dict(panel=pan.name, frame=fr, window=w, pair=f"{A}v{B}",
                                   dS_at_10=d10, verdict_at_10=("B" if d10 > 0 else "A"),
                                   n_crossings_0_50=len(xs),
                                   cstar_first=(xs[0] if xs else np.nan),
                                   cstar_in_band=(xs_in[0] if xs_in else np.nan),
                                   flips_in_5_50=flip,
                                   dS_at_5=sharpe_at(rgB, tuB, 5.0) - sharpe_at(rgA, tuA, 5.0),
                                   dS_at_50=sharpe_at(rgB, tuB, 50.0) - sharpe_at(rgA, tuA, 50.0),
                                   abs_dS_at_10=abs(d10)))
    CS = pd.DataFrame(cs)
    CS.to_csv(f"{OUT}.cstar.csv", index=False)
    say(f"  {len(CS)} pair-readings = 3 panels x 2 frames x {len(PAIRS)} cadence pairs x "
        f"{len(WINDOWS)} windows.  ALL published to .cstar.csv")
    fl_all = CS.flips_in_5_50.mean()
    say(f"\n  ANSWER Q2: {int(CS.flips_in_5_50.sum())} of {len(CS)} cadence verdicts ({fl_all:.1%}) "
        f"FLIP SIGN somewhere inside {BAND_LO:g}-{BAND_HI:g} bps.")
    say(f"    {int(CS.n_crossings_0_50.gt(0).sum())} of {len(CS)} have at least one crossing in "
        f"0-{BAND_HI:g} bps; {int(CS.n_crossings_0_50.gt(1).sum())} have MORE THAN ONE "
        f"(a non-monotone verdict in cost).")
    fin = CS.dropna(subset=["cstar_in_band"])
    if len(fin):
        say(f"    Among the {len(fin)} with a c* inside the band: median c* "
            f"{fin.cstar_in_band.median():.1f} bps (IQR {fin.cstar_in_band.quantile(.25):.1f}-"
            f"{fin.cstar_in_band.quantile(.75):.1f}).")
    for w in WINDOWS:
        s = CS[CS.window == w]
        say(f"    by window {w:<5}: flips {int(s.flips_in_5_50.sum()):>3} of {len(s)} "
            f"({s.flips_in_5_50.mean():.1%})   median |dS@10| {s.abs_dS_at_10.median():.4f}")
    for fr in FRAMES:
        s = CS[CS.frame == fr]
        say(f"    by frame  {fr:<5}: flips {int(s.flips_in_5_50.sum()):>3} of {len(s)} "
            f"({s.flips_in_5_50.mean():.1%})")
    for pn in ["U56", "B136", "SMALL"]:
        s = CS[CS.panel == pn]
        say(f"    by panel  {pn:<5}: flips {int(s.flips_in_5_50.sum()):>3} of {len(s)} "
            f"({s.flips_in_5_50.mean():.1%})")
    for pr in [f"{a}v{b}" for a, b in PAIRS]:
        s = CS[CS.pair == pr]
        say(f"    by pair   {pr:<5}: flips {int(s.flips_in_5_50.sum()):>3} of {len(s)} "
            f"({s.flips_in_5_50.mean():.1%})   median c* in band "
            f"{s.cstar_in_band.median() if s.cstar_in_band.notna().any() else float('nan'):.1f}")

    hl = CS[(CS.panel == "U56") & (CS.frame == "INC") & (CS.window == "FULL") & (CS.pair == "WvQ")]
    ok9 = False
    if len(hl):
        h = hl.iloc[0]
        got = h.cstar_first
        ok9 = bool(np.isfinite(got) and abs(got - CSTAR_1586) <= 0.15)
        say(f"\n  THE 1586 HEADLINE PAIR, re-derived here: U56 / INC / FULL, W vs Q -> "
            f"c* = {got:.2f} bps (1586 committed {CSTAR_1586:g}).")
    gate("G9 c* solver re-derives 1586's committed headline c* (U56/INC/FULL, W vs Q)",
         f"{hl.iloc[0].cstar_first:.3f} vs {CSTAR_1586:g}" if len(hl) else "missing",
         f"|dev| <= 0.15 bps", ok9)

    # ---------------------------------------------------------------- PART 4 / Q3
    say("\n" + "=" * 118)
    say("PART 4 / Q3 — THE KEEP VERDICT ITSELF AS AN INTERVAL OF COST RUNGS, not a point.")
    say(f"      For every book, the set of c in [0, {BAND_HI:g}] bps where 4a / 4b actually hold.")
    say("=" * 118)
    cgrid = np.arange(0.0, BAND_HI + 1e-9, 0.25)
    iv = []
    for pan in panels:
        WIN, bars = BARS[pan.name]["win"], BARS[pan.name]
        # live baseline as a function of c, exactly: one engine run at 0 bps + its turnover path
        l0 = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=0.0, freq="W")
        lrg, ltu = l0["returns"].values, l0["turnover"].values
        LIVEC = {}
        for c in cgrid:
            lr = lrg - ltu * c / 1e4
            LIVEC[float(c)] = (bmpack(lr[WIN["FULL"]]), bmpack(lr[WIN["OOS"]]))
        for fr in FRAMES:
            for cad in GRID_CAD:
                rg, tu = RG[(pan.name, fr, cad)], TU[(pan.name, fr, cad)]
                f4a = np.zeros(len(cgrid), bool)
                f4b = np.zeros(len(cgrid), bool)
                f4bO = np.zeros(len(cgrid), bool)
                for i, c in enumerate(cgrid):
                    r = rg - tu * c / 1e4
                    liveF, liveO = LIVEC[float(c)]
                    a, b_, _, _, _, _ = keep_paths(r[WIN["FULL"]], bars["spy"]["FULL"], liveF)
                    _, bo, _, _, _, _ = keep_paths(r[WIN["OOS"]], bars["spy"]["OOS"], liveO)
                    f4a[i], f4b[i], f4bO[i] = a, b_, bo
                both = f4b & f4bO
                iv.append(dict(panel=pan.name, frame=fr, cadence=cad,
                               n4a=int(f4a.sum()), n4b=int(f4b.sum()), n4b_oos=int(f4bO.sum()),
                               iv_4a=fmt_runs(runs_of_true(cgrid, f4a)),
                               iv_4b=fmt_runs(runs_of_true(cgrid, f4b)),
                               iv_4b_oos=fmt_runs(runs_of_true(cgrid, f4bO)),
                               iv_4b_both=fmt_runs(runs_of_true(cgrid, both)),
                               holds_whole_band_4b=bool(
                                   np.all(both[(cgrid >= BAND_LO) & (cgrid <= BAND_HI)])),
                               empty_4b=bool(both.sum() == 0),
                               verdict_at_10_4b=bool(both[np.argmin(np.abs(cgrid - BINDING))])))
    IV = pd.DataFrame(iv)
    IV.to_csv(f"{OUT}.verdict_interval.csv", index=False)
    mixed = IV[(~IV.empty_4b) & (~IV.holds_whole_band_4b)]
    say(f"  {len(IV)} books.  4b (FULL and OOS) is EMPTY over the whole 0-{BAND_HI:g} band for "
        f"{int(IV.empty_4b.sum())}, holds over the ENTIRE {BAND_LO:g}-{BAND_HI:g} band for "
        f"{int(IV.holds_whole_band_4b.sum())}, and is RUNG-CONDITIONAL for {len(mixed)}.")
    say(f"  Of the {int(IV.verdict_at_10_4b.sum())} books that PASS 4b at the protocol's "
        f"{BINDING:g} bps, {int((IV.verdict_at_10_4b & ~IV.holds_whole_band_4b).sum())} would "
        f"FAIL somewhere inside {BAND_LO:g}-{BAND_HI:g}.")
    for _, r in IV[IV.verdict_at_10_4b].iterrows():
        say(f"    4b@10 PASSER  {r.panel:<6} {r.frame:<5} {r.cadence}  4b FULL&OOS holds on "
            f"{r.iv_4b_both}{'   (whole band)' if r.holds_whole_band_4b else '   <== RUNG-CONDITIONAL'}")
    say(f"  4a: {int((IV.n4a>0).sum())} of {len(IV)} books clear 4a at ANY rung in the band; "
        f"intervals in .verdict_interval.csv")

    # ---------------------------------------------------------------- PART 5: rule 8
    say("\n" + "=" * 118)
    say("PART 5 — RULE 8 WALK-FORWARD.  Dials (cadence, and the RUNG the chooser quotes it at)")
    say("      fitted on warm-up..2016-12-31 ONLY; 2017-2026 READ ONCE.  Every OOS number below")
    say(f"      is scored at the protocol's binding {BINDING:g} bps regardless of the rung the")
    say("      chooser was allowed to use, because rule 2 binds the VERDICT, not the search.")
    say("=" * 118)
    wf = []
    for pan in panels:
        bars, WIN = BARS[pan.name], BARS[pan.name]["win"]
        i_oos = bars["i_oos"]
        spyO, liveO = bars["spy"]["OOS"], bars["live"][BINDING]["OOS"]
        for fr in FRAMES:
            for cc in CHOOSE_RUNGS:
                ispk = {}
                for cad in GRID_CAD:
                    rg, tu = RG[(pan.name, fr, cad)], TU[(pan.name, fr, cad)]
                    r = (rg - tu * cc / 1e4)[WIN["IS"]]
                    ispk[cad] = dict(Sharpe=sharpe(r), CAGR=cagr(r), MaxDD=mdd(r),
                                     turn=float(tu[WIN["IS"]].sum()))
                dd_bar = DD_CAP * bars["spy"]["IS"]["MaxDD"]
                cagr_bar = CAGR_FLOOR * bars["spy"]["IS"]["CAGR"]
                picks = {"C_SHARPE": (chooser_sharpe(ispk), False),
                         "C_MEMO": chooser_memo(ispk, dd_bar, cagr_bar, ANCHOR_CAD),
                         "C_ANCHOR": (ANCHOR_CAD, False)}
                for nm, (pk, fell) in picks.items():
                    r = (RG[(pan.name, fr, pk)] - TU[(pan.name, fr, pk)] * BINDING / 1e4)
                    ra = (RG[(pan.name, fr, ANCHOR_CAD)] -
                          TU[(pan.name, fr, ANCHOR_CAD)] * BINDING / 1e4)
                    k4aO, k4bO, mo, _, _, _ = keep_paths(r[WIN["OOS"]], spyO, liveO)
                    wf.append(dict(panel=pan.name, frame=fr, chooser_rung=cc, chooser=nm,
                                   pick=pk, fellback=fell, oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                   oMaxDD=mo["MaxDD"],
                                   d_vs_anchor=mo["Sharpe"] - sharpe(ra[WIN["OOS"]]),
                                   d_vs_live=mo["Sharpe"] - liveO["Sharpe"],
                                   d_vs_spy=mo["Sharpe"] - spyO["Sharpe"],
                                   keep4a_oos=k4aO, keep4b_oos=k4bO))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for nm in ["C_SHARPE", "C_MEMO", "C_ANCHOR"]:
        s = W[W.chooser == nm]
        say(f"    POOLED {nm:<9} ({len(s)} cells): mean OOS Sharpe {s.oSharpe.mean():.4f}, "
            f"mean dS vs anchor {s.d_vs_anchor.mean():+.4f}, beats live RULES v2 in "
            f"{int((s.d_vs_live>0).sum())} of {len(s)}, beats SPY in {int((s.d_vs_spy>0).sum())}, "
            f"4b_oos {int(s.keep4b_oos.sum())}, 4a_oos {int(s.keep4a_oos.sum())}")
    say("\n    DOES THE CHOOSER'S RUNG CHANGE ITS PICK?  (the idea's question as a tunable)")
    nchg = 0
    for pan in panels:
        for fr in FRAMES:
            for nm in ["C_SHARPE", "C_MEMO"]:
                s = W[(W.panel == pan.name) & (W.frame == fr) & (W.chooser == nm)]
                pk = {int(r.chooser_rung): r.pick for _, r in s.iterrows()}
                chg = len(set(pk.values())) > 1
                nchg += int(chg)
                say(f"      {pan.name:<6} {fr:<5} {nm:<9} picks " +
                    " ".join(f"@{k}bps={v}" for k, v in sorted(pk.items())) +
                    ("   <== RUNG-DEPENDENT" if chg else "   stable"))
    say(f"    {nchg} of 12 (panel x frame x chooser) groups change their IS pick with the rung.")
    best = W[W.chooser != "C_ANCHOR"].sort_values("oSharpe", ascending=False)
    say(f"\n    Best IS-only pick OOS: {best.iloc[0].panel} {best.iloc[0].frame} "
        f"{best.iloc[0].chooser}@{best.iloc[0].chooser_rung:g}bps -> {best.iloc[0]['pick']}  "
        f"OOS {best.iloc[0].oCAGR:.2%} / {best.iloc[0].oSharpe:.4f} / {best.iloc[0].oMaxDD:.2%}")
    anc = W[W.chooser == "C_ANCHOR"]
    say(f"    C_ANCHOR (choose nothing, stay weekly) OOS by panel/frame: " + ", ".join(
        f"{r.panel}/{r.frame} {r.oSharpe:.4f}" for _, r in
        anc.drop_duplicates(["panel", "frame"]).iterrows()))

    say("\n  [G6] re-fitting every chooser on IS returns TRUNCATED at 2016-12-31 must give the "
        "identical pick.")
    same = True
    for pan in panels:
        i_oos, WIN = BARS[pan.name]["i_oos"], BARS[pan.name]["win"]
        for fr in FRAMES:
            for cc in CHOOSE_RUNGS:
                a, b_ = {}, {}
                for cad in GRID_CAD:
                    rg, tu = RG[(pan.name, fr, cad)], TU[(pan.name, fr, cad)]
                    full = (rg - tu * cc / 1e4)[WIN["IS"]]
                    trunc = (rg[:i_oos] - tu[:i_oos] * cc / 1e4)[WARMUP:]
                    a[cad] = dict(Sharpe=sharpe(full), CAGR=cagr(full), MaxDD=mdd(full),
                                  turn=float(tu[WIN["IS"]].sum()))
                    b_[cad] = dict(Sharpe=sharpe(trunc), CAGR=cagr(trunc), MaxDD=mdd(trunc),
                                   turn=float(tu[:i_oos][WARMUP:].sum()))
                same &= chooser_sharpe(a) == chooser_sharpe(b_)
    gate("G6 choosers read no row on or after 2017-01-01 (truncated re-fit gives identical picks)",
         same, "True", same)
    say("  OOS start row per panel: " + ", ".join(
        f"{p.name} {p.idx[BARS[p.name]['i_oos']].date()}" for p in panels))

    for pan in panels:
        s = G[(G.panel == pan.name) & (G.cost_bps == BINDING)]
        for fr in FRAMES:
            publish(f"G10 turnover x/yr by cadence, {pan.name} {fr}",
                    ", ".join(f"{cd} {s[(s.cadence==cd)&(s.frame==fr)].turnover_yr.mean():.2f}"
                              for cd in GRID_CAD))

    # ---------------------------------------------------------------- the constructive half
    say("\n" + "=" * 118)
    say("THE CONSTRUCTIVE HALF — SHOULD PROTOCOL RULE 2 QUOTE A CADENCE VERDICT AS AN INTERVAL?")
    say("=" * 118)
    say(f"  Census:      {nB} BROAD / {nS} STRICT committed cadence claims; "
        f"{(CEN.klass.isin(['POINT_IMPLICIT','POINT_EXPLICIT'])).mean():.1%} of them are quoted at "
        f"a SINGLE cost rung.")
    say(f"  Re-pricing:  {fl_all:.1%} of {len(CS)} pairwise cadence verdicts flip sign inside "
        f"{BAND_LO:g}-{BAND_HI:g} bps.")
    say(f"  Verdicts:    {len(mixed)} of {len(IV)} books have a RUNG-CONDITIONAL 4b verdict.")
    say(f"  Rule 8:      {nchg} of 12 chooser groups change their pick with the rung they quote.")

    GT = pd.DataFrame(GATES)
    GT.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  GATES: {int(GT.pass_.sum())} of {len(GT)} pass/published.")
    say(f"  Wrote .census.csv ({len(CEN)}), .grid.csv ({len(G)}), .cstar.csv ({len(CS)}), "
        f".verdict_interval.csv ({len(IV)}), .walkforward.csv ({len(W)}), .gates.csv, .log.txt")
    say(f"  Elapsed {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
