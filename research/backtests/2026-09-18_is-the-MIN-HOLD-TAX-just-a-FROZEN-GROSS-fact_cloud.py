#!/usr/bin/env python3
"""Idea 1066 (lane cloud, 2026-09-18): is the MIN-HOLD TAX just a FROZEN-GROSS fact?

THE PREMISE.  The committed 2026-09-04 KEEP 4b book carries a MINIMUM HOLD of H=126 trading
days: a name entered into the book cannot be released until it is that old, whatever the score
or the eligibility gate later say.  Idea 1065 measured what that constraint costs in drawdown
and found the tax tracks the RETAINED BUCKET'S WEIGHT SHARE (rho +0.7519) and not its loss
concentration (CONC 0.91-1.14, inside its own null).  Read on 1065's own committed arms the tax
is large: U56 / CAND20 / weekly, MaxDD runs -18.31% at H=0 and -25.69% at H=63, i.e. 7.4pp of
drawdown bought for +2.2pp of CAGR — the "7 pp" 1066's queue text names.  (That figure is a
MaxDD DIFFERENCE between 1065's committed BOOK_H0 and BOOK_HARD rows; 1065's own `tax_pp`
column tops out at 4.81 and is a different statistic.  Provenance published, not assumed —
gate G0.)

THE QUESTION, AND WHY IT MATTERS FOR CAPITAL.  A min hold does two things at once.  It freezes
WEIGHT (a fraction of NAV stops responding to the signal at all) and it freezes PARTICULAR
NAMES (the ones the score wanted to drop — losers on their way down, the names that make a
drawdown).  If the whole tax is the first channel, it is a pure EXPOSURE/STALENESS fact and any
mechanism that freezes the same share of the book buys the same drawdown, whoever it freezes;
if it is the second, the tax is SELECTION and the constraint is actively holding the wrong
names through the trough.  These imply opposite repairs — shrink the frozen share (a gross
dial) versus release on a condition (1065's R_GATE) — so the record cannot price either until
it knows which channel it is paying for.

THE CONTROL (the queue's own wording).  A RANDOM-FREEZE book: at every rebalance a fraction f
of the CURRENT holdings, chosen uniformly at random with NO score and NO age input, is retained
regardless of what the score or the gate say; the remaining slots are refilled by the score
exactly as the real book refills them.  Everything else is bit-identical to the real book.  At
matched frozen share the random book pays the pure exposure channel and nothing else, so

    tax(REAL at H)  -  tax(RANDOM at f = the share H actually freezes)

is the selection channel, measured directly and with no model.

TWO CONSTRUCTION NOTES, BOTH ADDED AFTER THE FIRST PASS AND SAID SO PLAINLY.
  (i) N=20 slots make the attainable frozen shares a 0.05 lattice, so a plain round() cannot
      match an arbitrary s(H) and, worse, collides two REAL rungs onto ONE control (it did:
      H=63 and H=126 shared a matched arm on B135 and SMALL in the first pass).  The retained
      count is therefore drawn with STOCHASTIC ROUNDING — floor(f*n) plus a Bernoulli on the
      fraction — which is unbiased (E[nk] = f*n exactly) and deterministic per seed.  Gate G7
      checks the matching this is for.
  (ii) THE f=1.00 CELL IS NOT A CANDIDATE AND IS FLAGGED AS AN ARTEFACT.  Freezing 100% of the
      book freezes the names the score picked in the first warm-up week and holds them for
      seventeen years — on a CURRENT-CONSTITUENT panel that is a buy-and-hold of twenty names
      already known to have survived to 2026, which is exactly the bias rule 9 warns about, and
      it is not implementable out of sample at any date.  It is run and published (it is the
      f dial's endpoint and the record should see what it does), but a KEEP can never rest on
      it.  Rule 8 is therefore reported BOTH ways: C_ALL over the pre-declared pool and C_ALLx
      over the pool with the frozen-forever cell removed.  This distinction was written after
      the first pass showed the IS-argmax landing on that cell.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    MIN_HOLD H  {0, 5, 21, 63, 126, 252} trading days.  H=0 is EXACTLY the no-constraint book
                and H=126 is EXACTLY the committed 2026-09-04 book, so both controls are
                measured rather than assumed.
    FROZEN SHARE f  {0.00, 0.20, 0.40, 0.60, 0.80, 1.00} for the RANDOM arm, PLUS the MATCHED
                value f = s(H) read off each REAL rung (not a free choice: it is determined by
                the REAL arm it is matched to).
EVERY grid point is published in the .grid.csv.  The random arm is a distribution, not a point:
SEEDS_GRID=5 seeds at each f rung and SEEDS_MATCH=8 at each matched share, with the mean, the
standard error across seeds and the min/max all reported — a single seed would be an anecdote.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths leg by
leg; full / halves / IS / OOS CAGR, Sharpe, MaxDD, vol; annual turnover; the realised frozen
weight share; and the FORCED share — the fraction of retained weight the score would NOT have
picked that week, which is the mechanism's own dose and separates the two arms even at equal f.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: universe eligibility = above own
200d MA AND vol20 < 0.60; RAW three-leg composite (21/252, 0/126, 0/63 percentile ranks); N=20
slots; GROSS=0.75 of NAV; WEEKLY decide-Friday / trade-Monday; 10 bps per unit turnover; t+1
execution; 260-row warm-up; equal 1/len(held) slots.  The dials touch WHICH names are retained
and HOW MANY — never the cost model, the cadence, the gate or the sizing.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) PURE EXPOSURE — the random book at matched share reproduces the REAL arm's drawdown tax
      (and its CAGR gain) inside the seed SE.  Then the min hold buys nothing selection-wise and
      the tax is a frozen-gross fact: the repair is a share dial, and 1065's rho +0.7519 is the
      whole story.
  (B) SELECTION COSTS — REAL is WORSE than matched RANDOM in drawdown: the constraint holds the
      names the score wanted out, and a release condition (R_GATE) is the repair, not a share.
  (C) SELECTION PAYS — REAL is BETTER than matched RANDOM: age is information (the retained
      bucket is the 12-1 continuation 1068 asks about) and freezing at random is strictly worse.
  (D) NO TAX on this construction — the weekly N=20 book's MaxDD is flat in H, and the 7.4pp is
      a property of 1065's cadence/mechanism set, not of min holds.
  These are not exclusive across panels; whichever fire are reported as they fall.

RULE 8 (walk-forward, required).  Parameters are chosen on warm-up..2016-12-31 by IS Sharpe
ALONE and 2017-2026 is read ONCE, per panel, for three choosers: C_H over the 6 REAL rungs,
C_F over the 6 RANDOM rungs (seed 0), C_ALL over the pooled 12.  Each is reported against (i)
the committed anchor H=126, (ii) the do-nothing H=0, (iii) the cell mean and the worst cell,
with the IS/OOS rank correlation.  The capital verdict is the sign of chooser-minus-anchor,
never the best cell's number.

GATES.  G0 the 7pp provenance above is re-read from 1065's committed arms.csv.  G1 vintage-
pinned replay: truncated at 2026-09-16, U56 REAL H=126 must replay the committed 15.7147% /
1.14804 / -19.1276% to 1e-4.  G2 REAL H=0 and RANDOM f=0.00 are BIT-IDENTICAL (two spellings
of the same book) and f=0.00 is seed-invariant.  G3 the realised frozen share is monotone
non-decreasing in H (REAL) and in f (RANDOM).  G4 RANDOM f=1.00 freezes everything: turnover
falls to the forced-replacement floor.  G5 determinism: the whole U56 grid recomputed bit for
bit.  G6 the one-extra-day cache drift is published, not toleranced.  G7 the matched arm is
matched: |s(RANDOM at f=s(H)) - s(H)| is published per rung.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated below.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
UPPER bound.  The headline is a DIFFERENCE between two retention rules applied to the same
panel with the same gate, the same cadence and the same sizing, which is first-order immune to
a level bias that moves both arms together.  One direction is NOT neutral and is stated: a
current-constituent panel cannot contain the names a min hold would have ridden to delisting,
so the REAL arm's drawdown tax measured here is a LOWER bound on the live one, and outcome (A)
— "freezing at random is as bad as freezing by age" — is the reading this bias flatters least.

Runs standalone and offline (committed price caches only).
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
SLUG = "is-the-MIN-HOLD-TAX-just-a-FROZEN-GROSS-fact"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                    # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]            # RAW three-leg composite
HOLDS = [0, 5, 21, 63, 126, 252]                 # DIAL 1
FSHARES = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]   # DIAL 2
SEEDS_GRID, SEEDS_MATCH = 5, 8
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)   # gate G1 (1263's committed anchor)
VINTAGE = pd.Timestamp("2026-09-16")
ARMS_1065 = ROOT / "research" / "backtests" / (
    "2026-09-16_does-the-MIN-HOLD-DRAWDOWN-TAX-fall-on-the-NAMES-the-SCORE-WANTED-TO-DROP_C.arms.csv")
_LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
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
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def vol(r):
    return float(np.asarray(r, float).std(ddof=0) * np.sqrt(252))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), Vol=vol(r))


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


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ------------------------------------------------------------------ panel
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
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
        self.key = np.where(np.isfinite(comp), -comp, np.inf)      # smaller = better
        self.above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = self.above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, mode, H=A_H, f=0.0, seed=0, N=A_N, lag=1):
    """Selection frame at GROSS=1.0.

    mode 'REAL'   : retain every holding younger than H (the record's min hold).
    mode 'RANDOM' : retain round(f * len(holdings)) of the CURRENT holdings drawn uniformly at
                    random, with no score and no age input.
    Both retain only PRICED names; freed slots are refilled from the top of the score among
    eligible names.  Returns (W, diag) with the realised frozen and forced weight shares.
    """
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)      # entry row of each held name, -1 = not held
    pr = pan.priced[:, pan.iinv]
    key = pan.key
    nreb = len(pan.reb)
    rng = np.random.default_rng(1_000_003 * seed + 7)
    fr_num = fr_den = fo_num = ent_num = 0.0
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held):
            held = held[pr[t, held]]
        if mode == "REAL":
            keep = held[(t - cur[held]) < H] if len(held) else held
        else:
            # STOCHASTIC ROUNDING: N=20 slots make the attainable frozen shares a 0.05 lattice,
            # so a plain round() cannot match an arbitrary s(H) (and collides two REAL rungs onto
            # one control).  floor + Bernoulli(frac) is unbiased: E[nk] = f * len(held) exactly.
            x = f * len(held)
            nk = int(np.floor(x)) + int(rng.random() < (x - np.floor(x)))
            nk = min(max(nk, 0), len(held))
            keep = rng.choice(held, size=nk, replace=False) if nk else held[:0]
        keep = [int(c) for c in keep]
        # what the score alone would have picked this week (for the FORCED share diagnostic)
        k0 = key[ts].copy()
        k0[~(pan.elig[ts] & pr[ts])] = np.inf
        order0 = np.argsort(k0, kind="stable")
        want = set(int(c) for c in order0[:N] if np.isfinite(k0[int(c)]))
        need = N - len(keep)
        take = []
        if need > 0:
            k = k0.copy()
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[int(c)]):
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
        if t >= WARMUP:
            fr_num += len(keep) / len(sel)
            fo_num += sum(1 for c in keep if c not in want) / len(sel)
            ent_num += len(take)
            fr_den += 1.0
        w = np.full(len(sel), 1.0 / len(sel))
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = w
    d = max(fr_den, 1.0)
    yrs = max((T - WARMUP) / 252.0, 1e-9)
    return W, dict(frozen_share=fr_num / d, forced_share=fo_num / d, name_entries_yr=ent_num / yrs)


def run(pan, Wt, gross=A_G):
    """Hold gross*Wt from each rebalance, drift between, 10 bps on traded notional."""
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
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0))


# ------------------------------------------------------------------ KEEP paths
def legs_4a(bk, live):
    return dict(H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def cell(pan, idx, spy, live, mode, H, f, seed):
    Wt, diag = build(pan, mode, H=H, f=f, seed=seed)
    r, turn = run(pan, Wt)
    w = windows(idx, r[WARMUP:])
    a4, b4 = legs_4a(w, live), legs_4b(w, spy)
    return dict(panel=pan.name, arm=mode, H=H, f=f, seed=seed, **flat(w), turnover=turn,
                **diag, keep4a=all(a4.values()), keep4b=all(b4.values()),
                fail4a=failed(a4), fail4b=failed(b4))


def agg(cells, keys=("full_CAGR", "full_Sharpe", "full_MaxDD", "oos_Sharpe", "is__Sharpe",
                     "turnover", "frozen_share", "forced_share", "name_entries_yr")):
    out = {}
    for k in keys:
        v = np.array([c[k] for c in cells], float)
        out[k] = float(v.mean())
        out[k + "_se"] = float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0
        out[k + "_min"], out[k + "_max"] = float(v.min()), float(v.max())
    out["keep4b_n"] = int(sum(c["keep4b"] for c in cells))
    out["keep4a_n"] = int(sum(c["keep4a"] for c in cells))
    out["n_seeds"] = len(cells)
    return out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1066 lane cloud — {SLUG}")
    say(f"# frozen book: RAW 3-leg composite, gate = above 200d MA AND vol20 < {MAXVOL}, N={A_N}, "
        f"GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}, equal 1/len(held) slots")
    say(f"# DIAL 1 MIN_HOLD H = {HOLDS}  (H=0 no constraint, H={A_H} the committed 2026-09-04 book)")
    say(f"# DIAL 2 FROZEN SHARE f = {FSHARES} + the MATCHED f = s(H) at every REAL rung")
    say(f"# RANDOM arm seeds: {SEEDS_GRID} on the f grid, {SEEDS_MATCH} on the matched shares")
    say("# reported-not-dials: panel {U56,B136,SMALL}; both KEEP paths; full/halves/IS/OOS; "
        "turnover; realised frozen share; FORCED share")

    # ---- G0: the 7pp provenance
    try:
        a65 = pd.read_csv(ARMS_1065)
        q = a65[(a65.panel == "U56") & (a65.mech == "CAND20") & (a65.freq == "W")]
        h0 = q[(q.kind == "BOOK_H0")].MaxDD.iloc[0]
        h63 = q[(q.kind == "BOOK_HARD") & (q.hold == 63)].MaxDD.iloc[0]
        h126 = q[(q.kind == "BOOK_HARD") & (q.hold == 126)].MaxDD.iloc[0]
        gate("G0 the '7 pp' is 1065's committed MaxDD difference (U56/CAND20/W, H=0 vs H=63)",
             f"H0 {h0:.4%}, H63 {h63:.4%} -> tax {(h0-h63)*100:.2f}pp; H126 {h126:.4%}",
             "a MaxDD DIFFERENCE in 1065's arms.csv, ~7pp", abs((h0 - h63) * 100 - 7.4) < 0.5)
        REPLAY_1065 = (float(h0), float(h63), float(h126))
    except Exception as e:                                           # pragma: no cover
        gate("G0 the '7 pp' provenance", f"unreadable: {e}", "1065 arms.csv present", False)
        REPLAY_1065 = None

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, match_rows, r8rows = [], [], []
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}   CAGR floor "
            f"{CAGR_FLOOR*spy['full']['CAGR']:7.2%}   Sharpe bars H1 {spy['h1']['Sharpe']:.4f} "
            f"H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")

        say("\n   arm     H     f | seeds |    CAGR   Sharpe    MaxDD |  H1/H2 Sharpe |  OOS Sh |"
            " turn | frozen forced | 4a 4b | fail4b")
        real = {}
        for H in HOLDS:
            c = cell(pan, idx, spy, live, "REAL", H, 0.0, 0)
            rows.append(c)
            real[H] = c
            say(f"   REAL  {H:4d}     - |   1   | {c['full_CAGR']:7.2%} {c['full_Sharpe']:8.4f} "
                f"{c['full_MaxDD']:8.2%} | {c['h1_Sharpe']:.4f}/{c['h2_Sharpe']:.4f} | "
                f"{c['oos_Sharpe']:7.4f} | {c['turnover']:4.2f} | {c['frozen_share']:6.3f} "
                f"{c['forced_share']:6.3f} | {'Y' if c['keep4a'] else 'n'}  "
                f"{'Y' if c['keep4b'] else 'n'} | {c['fail4b']}")
        rand = {}
        for f in FSHARES:
            cs = [cell(pan, idx, spy, live, "RANDOM", 0, f, s) for s in range(SEEDS_GRID)]
            rows.extend(cs)
            a = agg(cs)
            rand[f] = a
            say(f"   RAND     -  {f:4.2f} |  {SEEDS_GRID}    | {a['full_CAGR']:7.2%} "
                f"{a['full_Sharpe']:8.4f} {a['full_MaxDD']:8.2%} | "
                f"{np.mean([c['h1_Sharpe'] for c in cs]):.4f}/"
                f"{np.mean([c['h2_Sharpe'] for c in cs]):.4f} | {a['oos_Sharpe']:7.4f} | "
                f"{a['turnover']:4.2f} | {a['frozen_share']:6.3f} {a['forced_share']:6.3f} | "
                f"{a['keep4a_n']}/{SEEDS_GRID} {a['keep4b_n']}/{SEEDS_GRID} | "
                f"SE(MaxDD) {a['full_MaxDD_se']*100:.2f}pp SE(Sh) {a['full_Sharpe_se']:.4f}")

        # ---- the headline: matched-share random control at every REAL rung
        say("\n   MATCHED CONTROL (RANDOM at f = the share each REAL rung actually freezes; "
            f"{SEEDS_MATCH} seeds):")
        say("     H | s(H)  | REAL   CAGR/Sharpe/MaxDD   | RANDOM(mean+-SE)          | "
            "SELECTION CHANNEL = REAL - RANDOM")
        base = real[0]
        for H in HOLDS[1:]:
            s = real[H]["frozen_share"]
            cs = [cell(pan, idx, spy, live, "RANDOM", 0, s, 100 + k) for k in range(SEEDS_MATCH)]
            rows.extend(cs)
            a = agg(cs)
            d_dd = real[H]["full_MaxDD"] - a["full_MaxDD"]
            d_cg = real[H]["full_CAGR"] - a["full_CAGR"]
            d_sh = real[H]["full_Sharpe"] - a["full_Sharpe"]
            z = d_dd / a["full_MaxDD_se"] if a["full_MaxDD_se"] > 0 else np.nan
            mr = dict(panel=pname, H=H, s_H=s, s_RAND=a["frozen_share"],
                      match_err=abs(a["frozen_share"] - s),
                      real_CAGR=real[H]["full_CAGR"], real_Sharpe=real[H]["full_Sharpe"],
                      real_MaxDD=real[H]["full_MaxDD"], real_oos=real[H]["oos_Sharpe"],
                      real_turn=real[H]["turnover"], real_forced=real[H]["forced_share"],
                      rand_CAGR=a["full_CAGR"], rand_Sharpe=a["full_Sharpe"],
                      rand_MaxDD=a["full_MaxDD"], rand_oos=a["oos_Sharpe"],
                      rand_turn=a["turnover"], rand_forced=a["forced_share"],
                      rand_MaxDD_se=a["full_MaxDD_se"], rand_Sharpe_se=a["full_Sharpe_se"],
                      rand_CAGR_se=a["full_CAGR_se"],
                      tax_real_pp=(base["full_MaxDD"] - real[H]["full_MaxDD"]) * 100,
                      tax_rand_pp=(base["full_MaxDD"] - a["full_MaxDD"]) * 100,
                      d_CAGR=d_cg, d_Sharpe=d_sh, d_MaxDD=d_dd, z_MaxDD=z,
                      d_oos=real[H]["oos_Sharpe"] - a["oos_Sharpe"],
                      real_keep4b=real[H]["keep4b"], rand_keep4b_n=a["keep4b_n"])
            match_rows.append(mr)
            say(f"   {H:4d} | {s:5.3f} | {real[H]['full_CAGR']:6.2%} {real[H]['full_Sharpe']:7.4f} "
                f"{real[H]['full_MaxDD']:7.2%} | {a['full_CAGR']:6.2%} {a['full_Sharpe']:7.4f} "
                f"{a['full_MaxDD']:7.2%} +-{a['full_MaxDD_se']*100:.2f}pp | CAGR {d_cg*100:+5.2f}pp "
                f"Sharpe {d_sh:+.4f} MaxDD {d_dd*100:+5.2f}pp (z {z:+5.2f}) OOS {mr['d_oos']:+.4f}"
                f" | tax REAL {mr['tax_real_pp']:+5.2f}pp vs RANDOM {mr['tax_rand_pp']:+5.2f}pp"
                f" | forced {real[H]['forced_share']:.3f} vs {a['forced_share']:.3f}")

        # ---- gates
        if pname == "U56":
            q = p_px.loc[:VINTAGE]
            vpan = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
            Wv, _ = build(vpan, "REAL", H=A_H)
            rv, _ = run(vpan, Wv)
            tv = stats(rv[WARMUP:])
            err = max(abs(tv["CAGR"] - COMMITTED_U56[0]), abs(tv["Sharpe"] - COMMITTED_U56[1]),
                      abs(tv["MaxDD"] - COMMITTED_U56[2]))
            gate(f"G1 vintage-pinned replay (U56 REAL H={A_H} @ {VINTAGE.date()})",
                 f"{tv['CAGR']:.4%}/{tv['Sharpe']:.4f}/{tv['MaxDD']:.4%} err {err:.2e}",
                 f"committed {COMMITTED_U56[0]:.4%}/{COMMITTED_U56[1]:.4f}/{COMMITTED_U56[2]:.4%}, "
                 "err < 1e-4", err < 1e-4)
            gate("G6 one-extra-day cache drift (U56 REAL H=126)",
                 f"CAGR {real[A_H]['full_CAGR']-tv['CAGR']:+.4%}  "
                 f"Sharpe {real[A_H]['full_Sharpe']-tv['Sharpe']:+.4f}  "
                 f"MaxDD {(real[A_H]['full_MaxDD']-tv['MaxDD'])*100:+.4f}pp",
                 "published, not toleranced", True)
            if REPLAY_1065 is not None:
                e65 = max(abs(real[0]["full_MaxDD"] - REPLAY_1065[0]),
                          abs(real[63]["full_MaxDD"] - REPLAY_1065[1]),
                          abs(real[126]["full_MaxDD"] - REPLAY_1065[2]))
                gate("G8 1065's committed MaxDD ladder replays on this construction (U56 W, H=0/63/126)",
                     f"{real[0]['full_MaxDD']:.4%}/{real[63]['full_MaxDD']:.4%}/"
                     f"{real[126]['full_MaxDD']:.4%} vs 1065 {REPLAY_1065[0]:.4%}/"
                     f"{REPLAY_1065[1]:.4%}/{REPLAY_1065[2]:.4%}, max err {e65*100:.3f}pp",
                     "< 0.5pp (one extra cache day + any construction difference)", e65 < 0.005)
            g2cs = [c for c in rows if c["panel"] == pname and c["arm"] == "RANDOM" and c["f"] == 0.0]
            d0 = max(abs(c["full_Sharpe"] - real[0]["full_Sharpe"]) for c in g2cs)
            gate("G2 RANDOM f=0.00 IS the REAL H=0 book, at every seed", f"{d0:.3e}", "== 0.0", d0 == 0.0)
            fs = [real[H]["frozen_share"] for H in HOLDS]
            fr = [rand[f]["frozen_share"] for f in FSHARES]
            gate("G3 realised frozen share monotone non-decreasing in H and in f",
                 "H " + "<".join(f"{x:.3f}" for x in fs) + " | f " + "<".join(f"{x:.3f}" for x in fr),
                 "both non-decreasing",
                 all(fs[i] <= fs[i + 1] + 1e-12 for i in range(len(fs) - 1))
                 and all(fr[i] <= fr[i + 1] + 1e-12 for i in range(len(fr) - 1)))
            ne1 = np.mean([c["name_entries_yr"] for c in rows
                           if c["panel"] == pname and c["arm"] == "RANDOM" and c["f"] == 1.0])
            ne0 = np.mean([c["name_entries_yr"] for c in rows
                           if c["panel"] == pname and c["arm"] == "RANDOM" and c["f"] == 0.0])
            gate("G4 RANDOM f=1.00 freezes the NAME SET (entries/yr; weight turnover keeps a "
                 "weekly re-equalisation floor, published not gated)",
                 f"{ne1:.2f} entries/yr vs f=0 {ne0:.2f}; weight turnover "
                 f"{rand[1.0]['turnover']:.3f}/yr vs {rand[0.0]['turnover']:.3f}/yr",
                 "entries/yr < 5% of the f=0 rate", ne1 < 0.05 * ne0)
        mx = max(r["match_err"] for r in match_rows if r["panel"] == pname)
        gate(f"G7 the matched arm is matched ({pname})", f"max |s(RAND)-s(H)| {mx:.4f}",
             "< 0.02", mx < 0.02)

        # ---- rule 8
        pool_real = [(("REAL", H), real[H]) for H in HOLDS]
        pool_rand = [(("RAND", f), [c for c in rows if c["panel"] == pname and c["arm"] == "RANDOM"
                                    and c["f"] == f and c["seed"] == 0][0]) for f in FSHARES]
        anchor, nothing = real[A_H], real[0]
        pool_rand_impl = [(k, c) for k, c in pool_rand if k[1] < 1.0]
        for cname, pool in (("C_H", pool_real), ("C_F", pool_rand), ("C_ALL", pool_real + pool_rand),
                            ("C_ALLx", pool_real + pool_rand_impl)):
            ks = [k for k, _ in pool]
            iss = np.array([c["is__Sharpe"] for _, c in pool])
            oos = np.array([c["oos_Sharpe"] for _, c in pool])
            j = int(np.nanargmax(iss))
            pk = pool[j][1]
            r8 = dict(panel=pname, chooser=cname, pick=str(ks[j]), pick_IS=pk["is__Sharpe"],
                      pick_OOS=pk["oos_Sharpe"], pick_OOS_CAGR=pk["oos_CAGR"],
                      pick_OOS_MaxDD=pk["oos_MaxDD"], anchor_OOS=anchor["oos_Sharpe"],
                      nothing_OOS=nothing["oos_Sharpe"],
                      d_vs_anchor=pk["oos_Sharpe"] - anchor["oos_Sharpe"],
                      d_vs_nothing=pk["oos_Sharpe"] - nothing["oos_Sharpe"],
                      cellmean_OOS=float(np.nanmean(oos)), worst_OOS=float(np.nanmin(oos)),
                      best_OOS=float(np.nanmax(oos)), rank_IS_OOS=rankcorr(iss, oos),
                      spy_OOS=spy["oos"]["Sharpe"], live_OOS=live["oos"]["Sharpe"],
                      pick_keep4a=pk["keep4a"], pick_keep4b=pk["keep4b"],
                      anchor_keep4b=anchor["keep4b"])
            r8rows.append(r8)
            say(f"   RULE 8 {cname:5s} IS-argmax = {str(ks[j]):12s} (IS Sh {r8['pick_IS']:.4f}) -> OOS "
                f"{r8['pick_OOS']:.4f}  vs anchor H=126 {r8['anchor_OOS']:.4f} "
                f"({r8['d_vs_anchor']:+.4f})  vs H=0 {r8['nothing_OOS']:.4f} "
                f"({r8['d_vs_nothing']:+.4f})  cellmean {r8['cellmean_OOS']:.4f} worst "
                f"{r8['worst_OOS']:.4f}  rank corr {r8['rank_IS_OOS']:+.2f}")

    grid = pd.DataFrame(rows)
    mt = pd.DataFrame(match_rows)
    wf = pd.DataFrame(r8rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    mt.to_csv(f"{STEM}.matched.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)

    # ---- G5 determinism (U56 REAL ladder + one random cell, recomputed)
    pan = Panel("U56", panels[0][1], panels[0][2])
    chk = []
    for H in HOLDS:
        W, _ = build(pan, "REAL", H=H)
        chk.append(sharpe(run(pan, W)[0][WARMUP:]))
    W, _ = build(pan, "RANDOM", f=0.6, seed=3)
    chk.append(sharpe(run(pan, W)[0][WARMUP:]))
    ref = [grid[(grid.panel == "U56") & (grid.arm == "REAL") & (grid.H == H)].full_Sharpe.iloc[0]
           for H in HOLDS]
    ref.append(grid[(grid.panel == "U56") & (grid.arm == "RANDOM") & (grid.f == 0.6)
                    & (grid.seed == 3)].full_Sharpe.iloc[0])
    dd = float(np.max(np.abs(np.array(chk) - np.array(ref))))
    gate("G5 determinism (U56 REAL ladder + RANDOM f=0.6 seed 3 re-run)", f"{dd:.3e}", "== 0.0", dd == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    # ---- summary
    say("\n## SUMMARY")
    say(f"   cells {len(grid)} ({int((grid.arm=='REAL').sum())} REAL, {int((grid.arm=='RANDOM').sum())} "
        f"RANDOM)   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for pname in grid.panel.unique():
        g = grid[grid.panel == pname]
        say(f"   {pname:9s} 4b {int(g.keep4b.sum()):3d}/{len(g)}   MaxDD "
            f"{g.full_MaxDD.min():7.2%}..{g.full_MaxDD.max():7.2%}   CAGR "
            f"{g.full_CAGR.min():6.2%}..{g.full_CAGR.max():6.2%}   Sharpe "
            f"{g.full_Sharpe.min():.4f}..{g.full_Sharpe.max():.4f}")
    say("\n   THE ANSWER — SELECTION CHANNEL (REAL minus matched-share RANDOM), per panel:")
    for pname in mt.panel.unique():
        m = mt[mt.panel == pname]
        say(f"   {pname:9s} n={len(m)}  d_MaxDD {m.d_MaxDD.mean()*100:+5.2f}pp "
            f"(REAL worse at {int((m.d_MaxDD<0).sum())}/{len(m)}, |z|>2 at "
            f"{int((m.z_MaxDD.abs()>2).sum())}/{len(m)})  d_CAGR {m.d_CAGR.mean()*100:+5.2f}pp "
            f"(>0 at {int((m.d_CAGR>0).sum())}/{len(m)})  d_Sharpe {m.d_Sharpe.mean():+.4f}  "
            f"d_OOS {m.d_oos.mean():+.4f}  tax REAL {m.tax_real_pp.mean():+5.2f}pp vs RANDOM "
            f"{m.tax_rand_pp.mean():+5.2f}pp  forced {m.real_forced.mean():.3f} vs {m.rand_forced.mean():.3f}")
    say(f"   POOLED over {len(mt)} matched rungs: d_MaxDD {mt.d_MaxDD.mean()*100:+.2f}pp "
        f"(REAL worse at {int((mt.d_MaxDD<0).sum())}/{len(mt)}), d_CAGR {mt.d_CAGR.mean()*100:+.2f}pp "
        f"(>0 at {int((mt.d_CAGR>0).sum())}/{len(mt)}), d_Sharpe {mt.d_Sharpe.mean():+.4f} "
        f"(>0 at {int((mt.d_Sharpe>0).sum())}/{len(mt)}), d_OOS {mt.d_oos.mean():+.4f} "
        f"(>0 at {int((mt.d_oos>0).sum())}/{len(mt)})")
    say(f"   share of the REAL drawdown tax reproduced by RANDOM at matched share: "
        f"{', '.join(f'{p}: ' + (f'{mt[mt.panel==p].tax_rand_pp.sum()/mt[mt.panel==p].tax_real_pp.sum():.2f}' if abs(mt[mt.panel==p].tax_real_pp.sum())>1e-9 else 'n/a') for p in mt.panel.unique())}")
    say(f"\n   RULE 8 chooser-minus-anchor: {wf.d_vs_anchor.round(4).tolist()}  mean "
        f"{wf.d_vs_anchor.mean():+.4f}  beats the committed anchor at "
        f"{int((wf.d_vs_anchor>0).sum())} of {len(wf)}")
    say(f"   RULE 8 chooser-minus-do-nothing(H=0): mean {wf.d_vs_nothing.mean():+.4f}  "
        f"positive at {int((wf.d_vs_nothing>0).sum())} of {len(wf)}   "
        f"IS/OOS rank corr mean {wf.rank_IS_OOS.mean():+.3f}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
