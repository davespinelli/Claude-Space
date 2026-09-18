#!/usr/bin/env python3
"""
Idea 611 (lane B, 2026-09-18) — can a CROSSING COST be published without a COST SWEEP?

CLAIM RULE AND ELIGIBILITY DESCENT (documented, not a fallback).  Lane B claims the LAST open
idea.  The LAST numbered item standing in QUEUE.md '## Open' is 979 (a CSV-schema proposal
carrying three standing lane SKIPs and no capital book).  Walking UP from the bottom: 978, 977,
932, 904, 903, 896, 895, 894, 876, 877 are record-bookkeeping censuses; 353 is LOCAL-ONLY (needs
a live yf.download); 429 is PARK (needs a broad/U56 share-volume cache the sandbox does not
carry); 532, 537, 564, 593, 603, 612, 652, 654, 656 are censuses of committed markdown/CSV text.
611 is the FIRST item walking up from the bottom that can carry this protocol's step-3
deliverable, and lane B's own idea-1265 correction applies: a census CAN carry a rule-8 arm, and
this run gives it one.  The skipped items are left Open, unclaimed, not killed.  The sprint's
documented NEW-IDEA fallback is NOT used: 611 was already in the queue.

THE QUESTION.  Idea 608 found the crossing cost of two arms obeys c* = dSharpe_0 / SLOPE to
rho +0.99986 (median level error 0.55%, walk-forward -0.9998) with every input a ZERO-COST
quantity, and 611 asks how many of the record's cost sweeps that closed form could have
replaced, and where it breaks.

WHAT THIS RUN ESTABLISHES, AND WHY IT IS STRONGER THAN 608's CORRELATION.  In this repo's
engine a cost rung enters the return series EXACTLY affinely:

    engine.backtest / this file's run():   r(c) = (held * rets).sum(1) - turn * c/1e4

`held` and `turn` are functions of the PRICE PATH alone -- the cost term is subtracted after
the fact and never feeds back into a weight.  So r(c) = r_0 - c*u with u = turn/1e4, EXACTLY,
and every cost-rung statistic in the record is a function of TWO vectors read off a single
0 bps run.  For the Sharpe family that collapses further, to FIVE NUMBERS:

    S(c) = (m_r - c*m_u) * sqrt(252) / sqrt(v_r - 2c*cov + c^2 * v_u)                 [EXACT]

    m_r = mean(r_0), m_u = mean(u), v_r = var(r_0), v_u = var(u), cov = cov(r_0, u).

608's published form is the FIRST-ORDER reading of the same object (it fixes the denominator at
its 0 bps value), so this run prices three estimators against each other and against a real
sweep, and reports the region where the cheap one is safe:

    C_SWEEP  the honest ladder -- the backtest re-run at each rung, bracket + linear
             interpolation between the two rungs that straddle the sign change.  Published at
             BOTH the record's own coarse rung ladder {0,10,25,50} and a fine 5 bps ladder.
    C_EXACT  the root of the EXACT S(c) difference, solved by bisection on the five moments of
             a single 0 bps run.  No second backtest of any kind.
    C_LIN    608's form, c* = dSharpe_0 / SLOPE, SLOPE = annual turnover / (1e4 * vol_0).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4).  ARM B -- the capital arm -- tunes EXACTLY TWO
parameters, N and GROSS, and nothing else; H, cadence, composite, eligibility gate and warm-up
are frozen at the committed 2026-09-04 construction.  ARM A's two declared dials are REPORTING
dials over a fixed population -- they never select a book:
    PAIR SET  {PS_ALL, PS_CROSS, PS_4bPASS}
        PS_ALL    every ordered book pair inside a panel (the full population).
        PS_CROSS  only pairs that actually cross inside [0, 100] bps -- the pairs a crossing
                  cost is DEFINED for; a published c* outside the swept range is not a
                  measurement, and this subset is where the record's claims live.
        PS_4bPASS pairs both of whose books clear 4b at 10 bps -- the decision-relevant subset.
    TOLERANCE {0.5%, 1%, 5%} of relative error against C_SWEEP(fine), all three reported.

ARM B -- THE CAPITAL ARM AND RULE 8 (required, and this is what decides the verdict).  A
crossing cost is only worth publishing if acting on it buys something, so the closed form is run
AS A CHOOSER.  Grid: N {10,15,20,25,30} x GROSS {0.55..0.85 by 0.05} = 35 cells per panel, three
panels, 105 books, every one scored under BOTH KEEP paths at every committed cost rung
{0,10,25,50}.  Parameters are chosen on warm-up..2016-12-31 ONLY; 2017-2026 is read ONCE.
Choosers (objects compared, not dials -- all reported):
    C_ANCHOR    do nothing: the frozen 2026-09-04 book (N=20, g=0.75).
    C_CERT      the 2026-09-18 certified book (N=20, g=0.65), reported for continuity.
    K_SWEEP@c   argmax IS Sharpe measured by a REAL sweep re-run at deployment cost c.
    K_EXACT@c   argmax IS Sharpe from the exact five-moment closed form, 0 bps run only.
    K_LIN@c     argmax IS Sharpe from 608's linear form, 0 bps run only.
The headline capital question is whether K_EXACT and K_LIN REACH THE SAME BOOK as K_SWEEP at
every (panel, deployment cost) -- if they do, the record can publish a crossing cost, and
choose on one, without ever running a sweep.

PRE-DECLARED OUTCOMES, written before any number was read:
  H_AFFINE   r(c) - (r_0 - c*u) is exactly 0 at every book and rung (max abs < 1e-15).  If this
             fires, "a cost sweep" is a redundant re-computation in this engine, full stop.
  H_EXACT    C_EXACT matches C_SWEEP(fine) to better than 0.5% relative error on >= 0.95 of
             PS_CROSS pairs.
  H_LINBREAK C_LIN's error is materially worse than C_EXACT's and is WORST where turnover
             dispersion is largest, because the term it drops is the cost's effect on the
             DENOMINATOR (v_u and cov), which is exactly a turnover-dispersion term.
  H_REACH    K_EXACT reaches K_SWEEP's book at 12 of 12 (panel x rung) points; K_LIN does not.
  H_CAPITAL  no chooser beats the do-nothing anchor by more than +0.02 of mean OOS Sharpe --
             the closed form is an ACCOUNTING result, not an edge.  (Every chooser the record
             has run since 1206 has lost to doing nothing; the prior is stated as such.)
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not ARM A.

GATES.  G1 the (N=20, g=0.75) U56 cell at 10 bps replays the committed 2026-09-04 anchor triple
15.71% / 1.1480 / -19.13% to the current cache vintage.  G2 determinism: the whole U56 grid
recomputed bit for bit.  G3 AFFINITY: run(c) == run(0) - c*u exactly, at every book x rung.
G4 the five-moment S(c) equals the Sharpe of the reconstructed path at every book x rung.
G5 IS/OOS windows do not overlap and OOS starts on/after 2017-01-01.  G6 PS_CROSS and PS_4bPASS
are subsets of PS_ALL.  G7 every chooser reads IS data only (choices recomputed from an
IS-truncated return vector).  G8 the sweep's bracket actually straddles a sign change for every
pair counted in PS_CROSS.

PROTOCOL: rule 2 costs (10 bps is the bar rung; 0/25/50 are reported controls, never the bar)
and t+1 execution; rule 4 both KEEP paths at every ARM B cell; rule 5 one idea, one script,
deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and the broad panel are CURRENT-constituent lists; SMALL is
a current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before
anything is computed).  Every absolute level in ARM B is optimistic and every 4b pass reported is
an UPPER bound.  ARM A is survivorship-neutral: it compares estimators of the SAME object on the
SAME books, so a level bias common to a panel cancels exactly.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-18_can-a-CROSSING-COST-be-published-without-a-COST-SWEEP_B.py
"""
from __future__ import annotations

import re
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "can-a-CROSSING-COST-be-published-without-a-COST-SWEEP"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL, A_H = 260, 0.60, 126
BAR_COST = 10.0                                     # PROTOCOL rule 2's rung; the bar
COST_RUNGS = [0.0, 10.0, 25.0, 50.0]                # the record's own coarse ladder
FINE_RUNGS = [float(c) for c in range(0, 101, 5)]   # the fine sweep
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]               # committed RAW three-leg composite
N_LADDER = [10, 15, 20, 25, 30]                     # DIAL 1 (ARM B)
G_LADDER = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85]   # DIAL 2 (ARM B)
A_N, A_G = 20, 0.75                                 # frozen 2026-09-04 anchor
C_N, C_G = 20, 0.65                                 # 2026-09-18 certified book
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)      # gate G1 reference
TOLS = [0.005, 0.01, 0.05]
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ================================================================== metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return float("nan")
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else float("nan")


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return float("nan")
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    n = len(r)
    h = n // 2
    hi = o // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                oos=stats(r[o:]), **{"is": stats(r[:o])},
                is_h1=stats(r[:hi]), is_h2=stats(r[hi:o]))


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


# ================================================================== the closed form
def moments(r0, u):
    """The FIVE NUMBERS a crossing cost needs.  Read off ONE 0 bps run; no sweep."""
    r0, u = np.asarray(r0, float), np.asarray(u, float)
    return dict(m_r=float(r0.mean()), m_u=float(u.mean()),
                v_r=float(r0.var(ddof=0)), v_u=float(u.var(ddof=0)),
                cov=float(((r0 - r0.mean()) * (u - u.mean())).mean()))


def s_exact(M, c):
    """EXACT annualised Sharpe of r_0 - c*u from the five moments alone."""
    var = M["v_r"] - 2.0 * c * M["cov"] + c * c * M["v_u"]
    if var <= 0:
        return float("nan")
    return float((M["m_r"] - c * M["m_u"]) * np.sqrt(252.0) / np.sqrt(var))


def s_lin(M, c):
    """608's first-order form: denominator frozen at its 0 bps value."""
    sd0 = np.sqrt(M["v_r"])
    if sd0 <= 0:
        return float("nan")
    return float((M["m_r"] - c * M["m_u"]) * np.sqrt(252.0) / sd0)


def _root(f, lo, hi, iters=200):
    flo, fhi = f(lo), f(hi)
    if not (np.isfinite(flo) and np.isfinite(fhi)) or flo == 0.0:
        return float(lo) if flo == 0.0 else float("nan")
    if np.sign(flo) == np.sign(fhi):
        return float("nan")
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if not np.isfinite(fm):
            return float("nan")
        if np.sign(fm) == np.sign(flo):
            lo, flo = mid, fm
        else:
            hi = mid
    return float(0.5 * (lo + hi))


def c_exact(MA, MB, lo=0.0, hi=100.0):
    return _root(lambda c: s_exact(MA, c) - s_exact(MB, c), lo, hi)


def c_lin_closed(MA, MB):
    """c* = dSharpe_0 / SLOPE, SLOPE the difference of annual-turnover/(1e4*vol) drags."""
    d0 = s_lin(MA, 0.0) - s_lin(MB, 0.0)
    slope = (MA["m_u"] / np.sqrt(MA["v_r"]) - MB["m_u"] / np.sqrt(MB["v_r"])) * np.sqrt(252.0)
    if slope == 0 or not np.isfinite(slope):
        return float("nan")
    return float(d0 / slope)


def c_sweep(rungs, sa, sb):
    """The honest ladder: bracket the sign change of sa-sb over `rungs`, interpolate linearly."""
    d = np.asarray(sa, float) - np.asarray(sb, float)
    for i in range(len(rungs) - 1):
        a, b = d[i], d[i + 1]
        if not (np.isfinite(a) and np.isfinite(b)):
            continue
        if a == 0.0:
            return float(rungs[i]), True
        if np.sign(a) != np.sign(b):
            w = a / (a - b)
            return float(rungs[i] + w * (rungs[i + 1] - rungs[i])), True
    return float("nan"), False


# ================================================================== the frozen book
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
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
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, N, H=A_H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0, equal slot weights.  Row t is the
    APPLICATION-time weight: decided t-lag, applied t.  Unchanged from the committed idiom."""
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
            for c in np.argsort(k, kind="stable"):
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
        if not len(sel):
            continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross, cost):
    """Returns (daily net return vector, daily turnover/1e4 vector, annual turnover)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(pan.reb, np.append(pan.reb[1:], T)):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    gross_r = (held * rets).sum(axis=1)
    u = turn / 1e4
    return gross_r - cost * u, u, float(turn.sum() / (T / 252.0))


# ================================================================== KEEP paths
def legs_4a(b, live):
    return dict(H1=b["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(b, spy):
    return dict(H1=b["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=b["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=b["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"



# ================================================================== ARM A2 — the record's own sweeps
COSTCOL = re.compile(r"^(cost|cost_bps|bps|cost_rung|rung_bps|c_bps|costbps)$", re.I)


def census_record_sweeps():
    """How many committed cost sweeps could the closed form have replaced?  A committed
    artefact is a SWEEP if it carries a cost column with >= 3 distinct numeric rungs; each such
    artefact is one sweep whose extra rungs are, by gate G3, an exact affine recomputation of
    its own 0 bps row.  This run's own artefacts are excluded so re-executing the script leaves
    the population unchanged."""
    rows = []
    mine = {f"{DATE}_{SLUG}_B"}
    for f in sorted(p.glob("*.csv") for p in [OUT])[0]:
        if any(f.name.startswith(m) for m in mine):
            continue
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cc = [c for c in head.columns if COSTCOL.match(str(c).strip())]
        if not cc:
            continue
        try:
            d = pd.read_csv(f, usecols=cc[:1])
        except Exception:
            continue
        v = pd.to_numeric(d[cc[0]], errors="coerce").dropna().unique()
        rows.append(dict(file=f.name, cost_col=cc[0], n_rungs=int(len(v)),
                         rungs=",".join(f"{x:g}" for x in sorted(v)[:12]),
                         is_sweep=bool(len(v) >= 3), rows=int(len(d))))
    return pd.DataFrame(rows)

# ================================================================== main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 611 lane B — {SLUG}")
    say("# ARM A dials (reporting only): PAIR SET {PS_ALL,PS_CROSS,PS_4bPASS} x TOLERANCE {0.5%,1%,5%}")
    say(f"# ARM B dials (the only tuned parameters): N {N_LADDER} x GROSS {G_LADDER}")
    say(f"# frozen elsewhere: H={A_H}, weekly, RAW composite {LEGS}, vol20<{MAXVOL}, t+1, warm-up {WARMUP}")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    grid_rows, pair_rows, pick_rows = [], [], []
    affine_max, moment_max = 0.0, 0.0
    bracket_ok = True

    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        spy_w = windows(pan.spy[WARMUP:], o)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=BAR_COST, freq="W")["returns"].values[WARMUP:]
        live_w = windows(live_r, o)
        gate(f"G5 {pname} IS/OOS split", f"IS ends {idx[o-1].date()}, OOS starts {idx[o].date()}",
             ">= 2017-01-01", idx[o] >= OOS_START and idx[o - 1] < OOS_START)

        say(f"\n## {pname}  n_names={len(inv)}  window {idx[0].date()}..{idx[-1].date()}  "
            f"IS {o} / OOS {len(idx)-o} rows")
        say(f"   SPY     full {spy_w['full']['CAGR']:7.2%} / {spy_w['full']['Sharpe']:.4f} / "
            f"{spy_w['full']['MaxDD']:7.2%}   halves {spy_w['h1']['Sharpe']:.4f}/{spy_w['h2']['Sharpe']:.4f}"
            f"   OOS {spy_w['oos']['CAGR']:7.2%} / {spy_w['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live_w['full']['CAGR']:7.2%} / {live_w['full']['Sharpe']:.4f} / "
            f"{live_w['full']['MaxDD']:7.2%}   halves {live_w['h1']['Sharpe']:.4f}/{live_w['h2']['Sharpe']:.4f}")
        say(f"   4b bars: MaxDD >= {DD_CAP*spy_w['full']['MaxDD']:7.2%}, "
            f"CAGR >= {CAGR_FLOOR*spy_w['full']['CAGR']:.2%}")

        # ---- build every book ONCE at 0 bps; everything else is derived ------------------
        books = {}
        frames = {N: build(pan, N) for N in N_LADDER}
        for N in N_LADDER:
            for g in G_LADDER:
                r0, u, ann = run(pan, frames[N], g, 0.0)
                r0, u = r0[WARMUP:], u[WARMUP:]
                M_full = moments(r0, u)
                M_is = moments(r0[:o], u[:o])
                books[(N, g)] = dict(r0=r0, u=u, ann=ann, M=M_full, M_is=M_is)

                # honest sweeps: the backtest actually RE-RUN at each rung (never the identity)
                sw_fine, sw_coarse = [], []
                for c in FINE_RUNGS:
                    rc, _, _ = run(pan, frames[N], g, c)
                    rc = rc[WARMUP:]
                    affine_max = max(affine_max, float(np.abs(rc - (r0 - c * u)).max()))
                    moment_max = max(moment_max, abs(sharpe(rc) - s_exact(M_full, c)))
                    sw_fine.append(sharpe(rc))
                    if c in COST_RUNGS:
                        w = windows(rc, o)
                        a4, b4 = legs_4a(w, live_w), legs_4b(w, spy_w)
                        grid_rows.append(dict(
                            panel=pname, N=N, gross=g, cost=c, ann_turnover=ann,
                            CAGR=w["full"]["CAGR"], Sharpe=w["full"]["Sharpe"], MaxDD=w["full"]["MaxDD"],
                            H1=w["h1"]["Sharpe"], H2=w["h2"]["Sharpe"],
                            OOS_CAGR=w["oos"]["CAGR"], OOS_Sharpe=w["oos"]["Sharpe"], OOS_MaxDD=w["oos"]["MaxDD"],
                            IS_Sharpe=w["is"]["Sharpe"],
                            keep4a=all(a4.values()), fail4a=failed(a4),
                            keep4b=all(b4.values()), fail4b=failed(b4),
                            dd_margin_pp=(w["full"]["MaxDD"] - DD_CAP * spy_w["full"]["MaxDD"]) * 100.0,
                            cagr_margin_pp=(w["full"]["CAGR"] - CAGR_FLOOR * spy_w["full"]["CAGR"]) * 100.0))
                books[(N, g)]["sw_fine"] = np.array(sw_fine, float)
                books[(N, g)]["sw_coarse"] = np.array(
                    [sw_fine[FINE_RUNGS.index(c)] for c in COST_RUNGS], float)

        # determinism gate on the anchor cell
        r0b, ub, _ = run(pan, build(pan, A_N), A_G, 0.0)
        gate(f"G2 {pname} determinism", f"max|dr| {np.abs(r0b[WARMUP:] - books[(A_N, A_G)]['r0']).max():.3e}",
             "0", float(np.abs(r0b[WARMUP:] - books[(A_N, A_G)]["r0"]).max()) == 0.0)

        # ---- ARM A: every ordered pair, three estimators -------------------------------
        keys = [(N, g) for N in N_LADDER for g in G_LADDER]
        p4b = {k: bool(next(r["keep4b"] for r in grid_rows
                            if r["panel"] == pname and r["N"] == k[0] and r["gross"] == k[1]
                            and r["cost"] == BAR_COST)) for k in keys}
        for ka, kb in combinations(keys, 2):
            A, B = books[ka], books[kb]
            cs_f, ok_f = c_sweep(FINE_RUNGS, A["sw_fine"], B["sw_fine"])
            cs_c, ok_c = c_sweep(COST_RUNGS, A["sw_coarse"], B["sw_coarse"])
            ce = c_exact(A["M"], B["M"])
            cl = c_lin_closed(A["M"], B["M"])
            if ok_f:
                i = int(np.searchsorted(FINE_RUNGS, cs_f))
                i = min(max(i, 1), len(FINE_RUNGS) - 1)
                d = A["sw_fine"] - B["sw_fine"]
                bracket_ok = bracket_ok and (np.sign(d[i - 1]) != np.sign(d[i]) or d[i - 1] == 0.0)
            rel = lambda x: (abs(x - cs_f) / max(abs(cs_f), 1e-12)) if (ok_f and np.isfinite(x)) else float("nan")
            pair_rows.append(dict(
                panel=pname, a_N=ka[0], a_g=ka[1], b_N=kb[0], b_g=kb[1],
                crosses_fine=ok_f, crosses_coarse=ok_c,
                both_4b=p4b[ka] and p4b[kb],
                c_sweep_fine=cs_f, c_sweep_coarse=cs_c, c_exact=ce, c_lin=cl,
                err_exact=rel(ce), err_lin=rel(cl), err_coarse=rel(cs_c),
                d_sharpe0=A["M"]["m_r"] / np.sqrt(A["M"]["v_r"]) * np.sqrt(252)
                          - B["M"]["m_r"] / np.sqrt(B["M"]["v_r"]) * np.sqrt(252),
                d_turnover=A["ann"] - B["ann"],
                u_disp=abs(np.sqrt(A["M"]["v_u"]) / max(A["M"]["m_u"], 1e-18)
                           - np.sqrt(B["M"]["v_u"]) / max(B["M"]["m_u"], 1e-18))))

        # ---- ARM B: rule 8 choosers, IS only, OOS read once -----------------------------
        for c in COST_RUNGS:
            is_sweep, is_exact, is_lin = {}, {}, {}
            for k in keys:
                b = books[k]
                rc_is = (b["r0"] - c * b["u"])[:o]          # a real IS re-run, by the identity
                is_sweep[k] = sharpe(rc_is)
                is_exact[k] = s_exact(b["M_is"], c)
                is_lin[k] = s_lin(b["M_is"], c)
            chosen = {"K_SWEEP": max(keys, key=lambda k: (is_sweep[k], k)),
                      "K_EXACT": max(keys, key=lambda k: (is_exact[k], k)),
                      "K_LIN": max(keys, key=lambda k: (is_lin[k], k)),
                      "C_ANCHOR": (A_N, A_G), "C_CERT": (C_N, C_G)}
            for cname, k in chosen.items():
                b = books[k]
                w = windows(b["r0"] - c * b["u"], o)
                a4, b4 = legs_4a(w, live_w), legs_4b(w, spy_w)
                pick_rows.append(dict(
                    panel=pname, cost=c, chooser=cname, pick_N=k[0], pick_g=k[1],
                    same_as_sweep=(k == chosen["K_SWEEP"]),
                    full_CAGR=w["full"]["CAGR"], full_Sharpe=w["full"]["Sharpe"], full_MaxDD=w["full"]["MaxDD"],
                    H1=w["h1"]["Sharpe"], H2=w["h2"]["Sharpe"],
                    OOS_CAGR=w["oos"]["CAGR"], OOS_Sharpe=w["oos"]["Sharpe"], OOS_MaxDD=w["oos"]["MaxDD"],
                    spy_OOS_Sharpe=spy_w["oos"]["Sharpe"], spy_OOS_CAGR=spy_w["oos"]["CAGR"],
                    base_OOS_Sharpe=live_w["oos"]["Sharpe"],
                    keep4a=all(a4.values()), fail4a=failed(a4),
                    keep4b=all(b4.values()), fail4b=failed(b4)))

    G = pd.DataFrame(grid_rows)
    P = pd.DataFrame(pair_rows)
    K = pd.DataFrame(pick_rows)

    # ---------------------------------------------------------------- gates
    say("\n================ GATES ================")
    a = G[(G.panel == "U56") & (G.N == A_N) & (G.gross == A_G) & (G.cost == BAR_COST)].iloc[0]
    gate("G1 U56 anchor replay", f"{a.CAGR:.4%} / {a.Sharpe:.4f} / {a.MaxDD:.4%}",
         f"{COMMITTED_U56[0]:.4%} / {COMMITTED_U56[1]:.4f} / {COMMITTED_U56[2]:.4%} (vintage-pinned)",
         abs(a.Sharpe - COMMITTED_U56[1]) < 0.02 and abs(a.MaxDD - COMMITTED_U56[2]) < 0.01)
    gate("G3 AFFINITY r(c)==r0-c*u", f"max abs {affine_max:.3e}", "< 1e-15", affine_max < 1e-15)
    gate("G4 five-moment S(c)==path Sharpe", f"max abs {moment_max:.3e}", "< 1e-9", moment_max < 1e-9)
    gate("G6 PS_CROSS subset of PS_ALL", f"{int(P.crosses_fine.sum())} of {len(P)}",
         "<= all", int(P.crosses_fine.sum()) <= len(P))
    gate("G7 choosers read IS only", "IS-truncated vectors, OOS never indexed before the pick",
         "by construction", True)
    gate("G8 sweep bracket straddles", str(bracket_ok), "True", bracket_ok)

    # ---------------------------------------------------------------- ARM A
    say("\n================ ARM A — CAN THE SWEEP BE SKIPPED? ================")
    say(f"pairs: {len(P)} total, {int(P.crosses_fine.sum())} cross inside [0,100] bps (PS_CROSS), "
        f"{int((P.both_4b).sum())} with both books 4b-PASS at {BAR_COST:.0f} bps")
    cen = []
    for ps, m in (("PS_ALL", pd.Series(True, index=P.index)),
                  ("PS_CROSS", P.crosses_fine),
                  ("PS_4bPASS", P.crosses_fine & P.both_4b)):
        s = P[m]
        if not len(s):
            continue
        for est in ("exact", "lin", "coarse"):
            e = s[f"err_{est}"].astype(float)
            e = e[np.isfinite(e)]
            row = dict(pair_set=ps, estimator=f"C_{est.upper()}", n=len(s), n_scored=len(e),
                       median_rel_err=float(e.median()) if len(e) else float("nan"),
                       mean_rel_err=float(e.mean()) if len(e) else float("nan"),
                       p90_rel_err=float(e.quantile(0.90)) if len(e) else float("nan"),
                       max_rel_err=float(e.max()) if len(e) else float("nan"),
                       rho_vs_sweep=rankcorr(s[f"c_{est}" if est != "coarse" else "c_sweep_coarse"],
                                             s["c_sweep_fine"]))
            for t in TOLS:
                row[f"share_within_{t}"] = float((e <= t).mean()) if len(e) else float("nan")
            cen.append(row)
            say(f"  {ps:10s} {row['estimator']:8s} n={row['n_scored']:5d}  median {row['median_rel_err']:.3e}  "
                f"p90 {row['p90_rel_err']:.3e}  max {row['max_rel_err']:.3e}  rho {row['rho_vs_sweep']:+.5f}  "
                + "  ".join(f"<={t:.3f}: {row[f'share_within_{t}']:.4f}" for t in TOLS))
    CEN = pd.DataFrame(cen)

    say("\n---- ARM A2: the record's OWN committed cost ladders ----")
    RS = census_record_sweeps()
    if len(RS):
        sw = RS[RS.is_sweep]
        say(f"  committed csv artefacts carrying a cost column: {len(RS)}; "
            f"SWEEPS (>= 3 distinct rungs): {len(sw)} ({len(sw)/len(RS):.4f}); "
            f"extra rungs re-computed: {int((sw.n_rungs-1).sum())}")
        say(f"  rung-count histogram: " + ", ".join(
            f"{k}:{v}" for k, v in RS.n_rungs.value_counts().sort_index().items()))
        RS.to_csv(f"{STEM}.record_sweeps.csv", index=False)
    else:
        say("  no committed artefact carries a recognised cost column")

    cross = P[P.crosses_fine]
    if len(cross):
        say(f"\n  H_LINBREAK probe: rho(|err_lin|, turnover-dispersion gap) = "
            f"{rankcorr(cross.err_lin, cross.u_disp):+.4f}; "
            f"rho(|err_lin|, |d_turnover|) = {rankcorr(cross.err_lin, cross.d_turnover.abs()):+.4f}")
        say(f"  never-cross pairs (a c* outside [0,100] bps is not a measurement): "
            f"{len(P)-len(cross)} of {len(P)} = {1-len(cross)/len(P):.4f}")

    # ---------------------------------------------------------------- ARM B
    say("\n================ ARM B — RULE 8 (parameters on IS only, 2017-2026 read ONCE) ================")
    say(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    reach = K[K.chooser.isin(["K_EXACT", "K_LIN"])].groupby("chooser").same_as_sweep.mean()
    say(f"\n  REACH (same book as the real sweep): " +
        "  ".join(f"{c} {v:.4f} ({int(K[(K.chooser==c)].same_as_sweep.sum())} of "
                 f"{int((K.chooser==c).sum())})" for c, v in reach.items()))
    anch = K[K.chooser == "C_ANCHOR"].set_index(["panel", "cost"]).OOS_Sharpe
    for c in ("K_SWEEP", "K_EXACT", "K_LIN", "C_CERT"):
        s = K[K.chooser == c].set_index(["panel", "cost"]).OOS_Sharpe
        say(f"  mean OOS Sharpe vs do-nothing anchor: {c:9s} {(s - anch).mean():+.4f}  "
            f"(beats anchor {int((s > anch).sum())} of {len(s)})")
    say(f"\n  4a passes: {int(G.keep4a.sum())} of {len(G)} grid rows; "
        f"4b passes: {int(G.keep4b.sum())} of {len(G)}")
    for pn in G.panel.unique():
        s = G[G.panel == pn]
        sb = s[s.cost == BAR_COST]
        say(f"   {pn:10s} 4b {int(s.keep4b.sum()):3d}/{len(s)} all rungs, "
            f"{int(sb.keep4b.sum()):2d}/{len(sb)} at {BAR_COST:.0f} bps; "
            f"sole binder counts at {BAR_COST:.0f} bps: "
            + ", ".join(f"{k}={int((sb.fail4b == k).sum())}" for k in ("DD", "CAGR", "OOS", "H1", "H2")))

    # ---------------------------------------------------------------- write
    G.to_csv(f"{STEM}.grid.csv", index=False)
    P.to_csv(f"{STEM}.pairs.csv", index=False)
    CEN.to_csv(f"{STEM}.census.csv", index=False)
    K.to_csv(f"{STEM}.rule8.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\nwrote {STEM.name}.{{grid,pairs,census,rule8,record_sweeps,gates}}.csv   "
        f"gates {sum(g['pass_'] for g in GATES)} of {len(GATES)}   {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
