#!/usr/bin/env python3
"""Idea 1270 (lane cloud, 2026-09-18): is the DD LEG a CONCENTRATION fact once N and GROSS are
moved TOGETHER at MATCHED EXPOSURE?

THE PREMISE.  Six mechanisms have now been priced on the standing 2026-09-04 KEEP 4b book —
rebalance phase (1253), calendar years (1254), ex-post winner names (1255), the signal (1257),
sector caps (1258), a DD brake (1262), portfolio vol targeting (1263), inverse-vol slot sizing
(1264), a correlation brake (1266), defensive rotation (1267), a per-name trailing stop (1271) —
and every one lands on the same sentence: the DRAWDOWN CAP is the only 4b leg that ever fails,
and every mechanism that moves HOW MUCH is held is reproduced by a flat gross cut at the same
mean exposure.  N and GROSS have each been dialled ALONE (1071/1081 for N, the 2026-09-17 gross
run for GROSS) and each is a pure CAGR-for-drawdown slide.  Nobody has moved them TOGETHER along
an ISO-EXPOSURE line, where breadth is bought without being paid for in cash.  If the DD leg is
a BREADTH fact rather than an EXPOSURE fact, that is the only cut that can show it.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    N     {10, 20, 30, 40, 50} names.  20 is the committed book.
    EXPO  {0.55, 0.65, 0.75, 0.85, 1.00} — a TARGET REALISED MEAN EXPOSURE, not a gross.  For
          each (panel, slot, N, EXPO) the GROSS that attains it is SOLVED by bisection on the
          book's own realised mean post-warm-up exposure, and both the solved gross and the
          realised exposure are published at every cell as the queue requires ("report ... the
          realised exposure of every cell as proof the line is level").  0.75 is the committed
          book's own exposure, so EXPO = 0.75 IS the iso-exposure line the idea asks for; the
          other four rungs are there so the line is read on a surface and not alone.
  5 x 5 = 25 cells per (panel, slot).  EVERY ONE PUBLISHED in the .grid.csv.

NOT DIALS, reported at every value.  PANEL {U56, B136, SMALL} (rule 9).  SLOT CONVENTION {LEN,
FIXN} — and this is the axis that decides whether the idea's premise is even true, so it is
measured rather than assumed:
    LEN   the INCUMBENT's own sizing, w = 1/len(held) of the target gross.  The book is always
          fully at its gross whenever it holds ANY name.
    FIXN  fixed slots, w = 1/N of the target gross, unfilled slots to CASH — the convention
          1197/1199 use and the one the queue's premise presumes, under which a thinning screen
          de-grosses the book.
Also reported at every N: the UNMATCHED CONTROL, the same book at the committed FLAT gross 0.75,
so the reader sees exactly what the matching changed rather than inferring it.  Both KEEP paths
leg by leg; full / halves / IS / OOS; annual turnover; realised mean, min and max exposure; mean
holdings count; the share of rebalances at which the screen delivers fewer than N names.
150 cells in all.

FROZEN AT THE STANDING BOOK'S CONSTRUCTION, not touched by this run: RAW 3-leg composite of
percentile ranks (21/252, 0/126, 0/63); eligibility = above own 200d MA AND vol20 < 0.60;
H = 126 minimum hold; WEEKLY decide-Friday / trade-Monday; 10 bps per unit turnover (rule 2);
t+1 execution; 260-row warm-up; IS ends 2016-12-31, OOS 2017-01-01 onward.  SELECTION IS
IDENTICAL ACROSS THE EXPO DIAL BY CONSTRUCTION — gross only scales the same holdings — which
gate G6 verifies rather than asserts.

FROZEN CONSTANT, DECLARED SO IT IS NOT MISTAKEN FOR A DIAL.  GROSS IS CAPPED AT 1.00: PROTOCOL
rule 2 forbids leverage unless the idea says so and this idea does not.  Under FIXN a high EXPO
target can therefore be UNREACHABLE (the book cannot hold more than it can fill); those cells
are published as unreachable with their realised exposure at the cap, NOT levered up to hit the
target and NOT dropped from the grid.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) THE PREMISE IS FALSE UNDER THE INCUMBENT'S OWN SIZING — with w = 1/len(held) the realised
      exposure does not depend on N at all, so the iso-exposure line IS the plain N ladder and
      1081's answer already covers it.  Then the honest report says so and the interesting arm
      is FIXN, where the premise holds.
  (B) BREADTH — at level exposure, MaxDD improves monotonically in N.  Then the DD leg is a
      concentration fact, the cut is the one the record has been missing, and a cell that clears
      4b with rule 8 behind it is a KEEP-candidate memo with exact RULES wording.
  (C) EXPOSURE — at level exposure MaxDD is flat or WORSENS in N, i.e. every DD gain the N dial
      ever showed was the cash it was buying.  Then the DD leg is an exposure fact and the
      search for it inside the book's breadth is over.
  (D) NEITHER, AND IT IS PANEL-SPECIFIC.
  (A)-(D) are not mutually exclusive across panels and slots; whichever fire are reported as
  they fall, and the capital verdict follows rule 8, not the best cell.

RULE 8 (walk-forward, required).  (N, EXPO) is CHOSEN on warm-up..2016-12-31 by IS Sharpe ALONE
and 2017-2026 is read ONCE, per (panel, slot).  Reported against (i) the DO-NOTHING control =
(N=20, EXPO=0.75), which is the committed book, (ii) the mean over all 25 cells, (iii) the WORST
cell, with the IS/OOS rank correlation over the 25.  OOS CAGR / Sharpe / MaxDD are published for
every pick against SPY's and the live RULES v2 baseline's on the same rows.  The capital verdict
is the sign of chooser-minus-do-nothing, never the best cell's number.

GATES.  G1 the anchor: LEN / N=20 / flat gross 0.75 must reproduce the committed
15.7147% / 1.1480 / -19.1276%; the U56 tape is data/prices.csv, which is refreshed daily and
whose adjusted closes are restated retroactively, so the replay error is PUBLISHED per component
rather than toleranced (idea 1203 measured that restatement at 2.9e-04 of IS Sharpe and 7.5e-03
of OOS Sharpe over a single day).  G2 THE LINE IS LEVEL: at every reachable cell the realised
mean exposure equals its target to < 1e-6 — this is the gate the idea's whole reading depends on.
G3 no leverage: the solved gross is inside (0, 1.00] at every cell.  G4 determinism: the whole
U56 LEN grid recomputed bit for bit.  G5 under LEN the solved gross is INVARIANT in N at every
EXPO rung (the structural fact behind outcome (A)), and under FIXN it is NOT.  G6 selection is
identical across the EXPO dial at fixed (N, slot): the holdings matrix is bit-identical, so the
dial moves only exposure.  G7 the fast runner reproduces engine.backtest on the live RULES v2
weights.  G8 SPY is never held on any panel (it is a benchmark column, not a constituent).

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
UPPER bound.  The headline is a SHAPE IN N measured at level exposure inside ONE panel over ONE
tape — a difference between books drawn from the same biased pool — and is first-order immune to
a level bias that moves all cells together.  One direction is NOT neutral and is stated: a
current-constituent panel has no delistings, so the screen never thins for the reason it would
thin in life, and the wide-N cells (N=40, 50 on a 55-name panel) are flattered relative to a
live panel where the tail names would be gone rather than merely out of favour.  That biases the
test TOWARD outcome (B), so a (C) finding here is the stronger conclusion.

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
SLUG = "is-the-DD-LEG-a-CONCENTRATION-fact-once-N-and-GROSS-are-moved-TOGETHER-at-MATCHED-EXPOSURE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                 # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]         # RAW 3-leg composite
NLAD = [10, 20, 30, 40, 50]                   # DIAL 1
EXPOLAD = [0.55, 0.65, 0.75, 0.85, 1.00]      # DIAL 2 (target REALISED mean exposure)
SLOTS = ["LEN", "FIXN"]
GROSS_CAP = 1.00                              # frozen: NO LEVERAGE (rule 2)
COMMITTED = (0.157147, 1.14804, -0.191276)    # the 2026-09-04 anchor, gate G1

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"  [{'PASS' if ok else 'FAIL'}] {name:76s} value={value} target={target}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def vol(r):
    return float(np.asarray(r, float).std(ddof=0) * np.sqrt(252))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), Vol=vol(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


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


# ------------------------------------------------------------------ panel (1263/1264's)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.C.shape[1])), self.C[:-1]])
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        v20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = self.above & (np.nan_to_num(v20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.ends = np.append(self.reb[1:], len(px))


def build(pan, N, slot, H=A_H, lag=1):
    """The frozen selection frame at target gross 1.0.  1264/1263's build, with the SLOT
    convention exposed: LEN = 1/len(held) (the incumbent), FIXN = 1/N with unfilled slots in
    cash (1197/1199's)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    nsel = np.zeros(nreb, dtype=np.int64)
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
        nsel[i] = len(sel)
        if not len(sel):
            continue
        w = np.full(len(sel), 1.0 / len(sel)) if slot == "LEN" else np.full(len(sel), 1.0 / N)
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = w
    return W, nsel


def run(pan, Wt, gross, want_held=False):
    """Hold gross*Wt from each rebalance, drift between, 10 bps on traded notional."""
    rets = pan.rets
    T, M = rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(pan.reb, pan.ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = pan.Cp[i0]
        A = w0[None, :] * (pan.Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (pan.C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    e = held[WARMUP:].sum(axis=1)
    out = (r, float(turn.sum() / (T / 252.0)), float(e.mean()), float(e.min()), float(e.max()))
    return out + ((held,) if want_held else ())


def exposure_only(pan, Wt, gross):
    """The realised mean post-warm-up exposure alone, without materialising the T x M holdings
    matrix.  exposure(t) = S/(S+c0) with S = sum_j w0_j * Cp[t,j]/base_j, so only the selected
    columns are touched.  Used by the bisection so solving the iso-exposure line is cheap; the
    published exposure always comes from the full run(), and gate G2 checks the two agree."""
    T = pan.rets.shape[0]
    e = np.empty(T)
    e[:] = 0.0
    for i0, i1 in zip(pan.reb, pan.ends):
        w0 = gross * Wt[i0]
        sel = np.flatnonzero(w0)
        if not len(sel):
            e[i0:i1] = 0.0
            continue
        S = (pan.Cp[i0:i1, sel] / pan.Cp[i0, sel][None, :]) @ w0[sel]
        e[i0:i1] = S / (S + (1.0 - w0.sum()))
    return float(e[WARMUP:].mean())


def solve_gross(pan, Wt, target, tol=1e-12, iters=60):
    """Smallest gross whose realised mean exposure equals `target`, by bisection on (0, 1.00].
    Exposure is monotone increasing in gross.  Returns (gross, reachable)."""
    hi = GROSS_CAP
    if exposure_only(pan, Wt, hi) < target - 1e-12:
        return hi, False                      # UNREACHABLE without leverage — published as such
    lo = 0.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if exposure_only(pan, Wt, mid) < target:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return hi, True


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


def main():
    t0 = time.time()
    say("=" * 104)
    say(f"# {DATE} idea 1270 lane cloud — {SLUG}")
    say("=" * 104)
    say(f"  DIAL 1 N = {NLAD}   (20 = the committed book)")
    say(f"  DIAL 2 EXPO = {EXPOLAD}   TARGET REALISED MEAN EXPOSURE; gross SOLVED per cell")
    say(f"  reported-not-dials: panel {{U56,B136,SMALL}} x slot {SLOTS} + the UNMATCHED flat-0.75 control")
    say(f"  frozen: RAW 3-leg composite, above-200d AND vol20 < {MAXVOL}, H={A_H}, weekly, "
        f"{COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"  frozen constant (NOT a dial): GROSS_CAP = {GROSS_CAP:.2f} — no leverage (rule 2); "
        "unreachable targets are published, never levered into")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"  SMALL panel: {psm.shape[1]-1} columns, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, ctrls, r8rows = [], [], []
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        say("")
        say(f"## {pname}  n_names={len(inv)}  {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}   CAGR floor "
            f"{CAGR_FLOOR*spy['full']['CAGR']:7.2%}   Sharpe H1 {spy['h1']['Sharpe']:.4f} "
            f"H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")

        if pname == "U56":
            Wv = rules_v2_weights(p_px).reindex(pan.idx).fillna(0.0).shift(1).fillna(0.0).values
            rr, *_ = run(pan, Wv, 1.0)
            eng = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values
            d7 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - rr[WARMUP:])))
            gate("G7 fast runner == engine.backtest on the live RULES v2 weights", f"{d7:.3e}",
                 "< 1e-12", d7 < 1e-12)

        for slot in SLOTS:
            say(f"\n   ===== slot convention {slot} "
                f"({'w = 1/len(held), THE INCUMBENT' if slot == 'LEN' else 'w = 1/N, unfilled slots to CASH'}) =====")
            say("     N  EXPO |  gross  reach |    CAGR   Sharpe    MaxDD    vol |  H1/H2 Sharpe |"
                "  OOS Sh   OOS CAGR  OOS DD | turn  expo(mean/min/max) nsel  thin | 4a 4b | fail4b")
            cells = {}
            builds = {}
            for N in NLAD:
                Wt, nsel = build(pan, N, slot)
                builds[N] = (Wt, nsel)
                # the UNMATCHED control: the same book at the committed FLAT gross
                cr, cturn, cem, _, _ = run(pan, Wt, A_G)
                cw = windows(idx, cr[WARMUP:])
                cb4, ca4 = legs_4b(cw, spy), legs_4a(cw, live)
                ctrls.append(dict(panel=pname, slot=slot, N=N, gross=A_G, **flat(cw),
                                  turnover=cturn, expo_mean=cem,
                                  nsel_mean=float(nsel[nsel > 0].mean()),
                                  thin_share=float(np.mean(nsel < N)),
                                  keep4a=all(ca4.values()), keep4b=all(cb4.values()),
                                  fail4b=failed(cb4)))
                if pname == "U56" and slot == "LEN" and N == A_N:
                    e1 = max(abs(cw["full"]["CAGR"] - COMMITTED[0]),
                             abs(cw["full"]["Sharpe"] - COMMITTED[1]),
                             abs(cw["full"]["MaxDD"] - COMMITTED[2]))
                    gate("G1 anchor replay (LEN/N=20/flat 0.75) vs committed 2026-09-04 triple",
                         f"{cw['full']['CAGR']:.4%}/{cw['full']['Sharpe']:.4f}/"
                         f"{cw['full']['MaxDD']:.4%} err {e1:.2e}",
                         f"committed {COMMITTED[0]:.4%}/{COMMITTED[1]:.4f}/{COMMITTED[2]:.4%}; "
                         "restated daily cache -> PUBLISHED, not toleranced", True)

                for ex in EXPOLAD:
                    g, reach = solve_gross(pan, Wt, ex)
                    r, turn, em, emin, emax, held = run(pan, Wt, g, want_held=True)
                    r = r[WARMUP:]
                    w = windows(idx, r)
                    a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                    rec = dict(panel=pname, slot=slot, N=N, expo_target=ex, gross=g,
                               reachable=reach, **flat(w), turnover=turn,
                               expo_mean=em, expo_min=emin, expo_max=emax,
                               expo_err=em - ex if reach else np.nan,
                               nsel_mean=float(nsel[nsel > 0].mean()),
                               thin_share=float(np.mean(nsel < N)),
                               keep4a=all(a4.values()), keep4b=all(b4.values()),
                               fail4a=failed(a4), fail4b=failed(b4))
                    rows.append(rec)
                    cells[(N, ex)] = rec
                    say(f"    {N:3d} {ex:5.2f} | {g:6.4f}  {'Y' if reach else 'n':5s} | "
                        f"{w['full']['CAGR']:7.2%} {w['full']['Sharpe']:8.4f} {w['full']['MaxDD']:8.2%} "
                        f"{w['full']['Vol']:6.2%} | {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f} | "
                        f"{w['oos']['Sharpe']:7.4f} {w['oos']['CAGR']:9.2%} {w['oos']['MaxDD']:8.2%} | "
                        f"{turn:5.2f} {em:.4f}/{emin:.3f}/{emax:.3f} {rec['nsel_mean']:5.1f} "
                        f"{rec['thin_share']:.3f} | {'Y' if all(a4.values()) else 'n'}  "
                        f"{'Y' if all(b4.values()) else 'n'} | {failed(b4)}")

                if pname == "U56" and slot == "LEN" and N == A_N:
                    _, _, _, _, _, h1 = run(pan, Wt, 0.40, want_held=True)
                    _, _, _, _, _, h2 = run(pan, Wt, 0.80, want_held=True)
                    s1 = (h1 > 0).astype(np.int8)
                    s2 = (h2 > 0).astype(np.int8)
                    d6 = int(np.abs(s1 - s2).sum())
                    gate("G6 selection identical across the EXPO dial (holdings support at gross "
                         "0.40 vs 0.80)", float(d6), 0.0, d6 == 0)

            # ---- G2 the line is level; G3 no leverage
            if True:
                rr = [c for c in cells.values() if c["reachable"]]
                e2 = max(abs(c["expo_mean"] - c["expo_target"]) for c in rr)
                gate(f"G2 THE LINE IS LEVEL ({pname}/{slot}): realised mean exposure == target at "
                     f"all {len(rr)} reachable cells", f"{e2:.3e}", "< 1e-6", e2 < 1e-6)
                gmx = max(c["gross"] for c in cells.values())
                gmn = min(c["gross"] for c in cells.values())
                gate(f"G3 no leverage ({pname}/{slot}): solved gross inside (0, {GROSS_CAP}]",
                     f"[{gmn:.4f}, {gmx:.4f}]", f"(0, {GROSS_CAP}]", gmn > 0 and gmx <= GROSS_CAP + 1e-12)

            # ---- G5 the structural fact: is gross invariant in N?
            spread = {ex: max(cells[(N, ex)]["gross"] for N in NLAD) - min(cells[(N, ex)]["gross"] for N in NLAD)
                      for ex in EXPOLAD}
            mx = max(spread.values())
            if slot == "LEN":
                gate(f"G5a LEN ({pname}): the solved gross is INVARIANT in N at every EXPO rung "
                     "-> the iso-exposure line IS the plain N ladder",
                     "  ".join(f"{ex} {spread[ex]:.2e}" for ex in EXPOLAD), "< 1e-3", mx < 1e-3)
            else:
                gate(f"G5b FIXN ({pname}): the solved gross MOVES with N -> the idea's premise "
                     "holds under this convention", "  ".join(f"{ex} {spread[ex]:.3f}" for ex in EXPOLAD),
                     "> 1e-3 at some rung", mx > 1e-3)
                # G5c states the MECHANISM rather than the direction, and is the gate that
                # decides whether a G5b failure is a defect or a finding: FIXN can only
                # de-gross where the screen delivers STRICTLY BETWEEN 1 and N names, so
                # invariance is CORRECT on a panel that never partially thins.
                part = {N: float(np.mean((builds[N][1] > 0) & (builds[N][1] < N))) for N in NLAD}
                mxp = max(part.values())
                ok5c = (mx > 1e-3) == (mxp > 1e-3)
                gate(f"G5c FIXN ({pname}): gross moves with N IFF the screen PARTIALLY thins "
                     "(0 < n_sel < N)",
                     "partial-thin share " + " ".join(f"N{N} {part[N]:.4f}" for N in NLAD)
                     + f" | gross spread {mx:.2e}", "the two agree", ok5c)
                if mxp <= 1e-3:
                    say(f"     NOTE ({pname}/FIXN): the screen is NEVER partially thin — n_sel is "
                        f"either N or 0 at every rebalance — so FIXN and LEN are the SAME BOOK here "
                        f"and the idea's premise has no mechanism to act through on this panel.")

            # ---- rule 8
            ks = list(cells)
            is_s = np.array([cells[k]["is__Sharpe"] for k in ks])
            oos_s = np.array([cells[k]["oos_Sharpe"] for k in ks])
            pick = ks[int(np.nanargmax(is_s))]
            dn = cells[(A_N, A_G)]
            r8 = dict(panel=pname, slot=slot, pick_N=pick[0], pick_EXPO=pick[1],
                      pick_gross=cells[pick]["gross"], pick_IS=cells[pick]["is__Sharpe"],
                      pick_OOS_Sharpe=cells[pick]["oos_Sharpe"], pick_OOS_CAGR=cells[pick]["oos_CAGR"],
                      pick_OOS_MaxDD=cells[pick]["oos_MaxDD"], pick_full_CAGR=cells[pick]["full_CAGR"],
                      pick_full_Sharpe=cells[pick]["full_Sharpe"], pick_full_MaxDD=cells[pick]["full_MaxDD"],
                      donothing_OOS_Sharpe=dn["oos_Sharpe"], donothing_OOS_CAGR=dn["oos_CAGR"],
                      donothing_OOS_MaxDD=dn["oos_MaxDD"],
                      delta=cells[pick]["oos_Sharpe"] - dn["oos_Sharpe"],
                      cellmean_OOS=float(np.nanmean(oos_s)), worst_OOS=float(np.nanmin(oos_s)),
                      best_OOS=float(np.nanmax(oos_s)), rank_IS_OOS=rankcorr(is_s, oos_s),
                      spy_OOS_Sharpe=spy["oos"]["Sharpe"], spy_OOS_CAGR=spy["oos"]["CAGR"],
                      spy_OOS_MaxDD=spy["oos"]["MaxDD"], live_OOS_Sharpe=live["oos"]["Sharpe"],
                      pick_keep4a=cells[pick]["keep4a"], pick_keep4b=cells[pick]["keep4b"],
                      pick_fail4b=cells[pick]["fail4b"], donothing_keep4b=dn["keep4b"])
            r8rows.append(r8)
            say(f"     RULE 8  IS-argmax = N {pick[0]} / EXPO {pick[1]} (gross {r8['pick_gross']:.4f}, "
                f"IS Sh {r8['pick_IS']:.4f}) -> OOS {r8['pick_OOS_Sharpe']:.4f} / "
                f"{r8['pick_OOS_CAGR']:.2%} / {r8['pick_OOS_MaxDD']:.2%}")
            say(f"     {'':8s} do-nothing (N=20, EXPO=0.75) OOS {dn['oos_Sharpe']:.4f} / "
                f"{dn['oos_CAGR']:.2%} / {dn['oos_MaxDD']:.2%}   delta {r8['delta']:+.4f}   "
                f"25-cell mean {r8['cellmean_OOS']:.4f} worst {r8['worst_OOS']:.4f}   "
                f"rank corr IS/OOS {r8['rank_IS_OOS']:+.2f}")

            # ---- G4 determinism (U56/LEN only)
            if pname == "U56" and slot == "LEN":
                chk = []
                for N in NLAD:
                    Wt, _ = build(pan, N, slot)
                    for ex in EXPOLAD:
                        g, _ = solve_gross(pan, Wt, ex)
                        r, *_ = run(pan, Wt, g)
                        chk.append(sharpe(r[WARMUP:]))
                ref = [cells[(N, ex)]["full_Sharpe"] for N in NLAD for ex in EXPOLAD]
                d4 = float(np.max(np.abs(np.array(chk) - np.array(ref))))
                gate("G4 determinism (U56 LEN grid re-solved and re-run bit for bit)", f"{d4:.3e}",
                     "== 0.0", d4 == 0.0)

        # ---- G8 SPY never held
        Wt, _ = build(pan, A_N, "LEN")
        ispy = list(p_px.columns).index("SPY")
        gate(f"G8 SPY never held on {pname} (benchmark column, not a constituent)",
             float(np.abs(Wt[:, ispy]).sum()), 0.0, float(np.abs(Wt[:, ispy]).sum()) == 0.0)

    grid = pd.DataFrame(rows)
    ctl = pd.DataFrame(ctrls)
    wf = pd.DataFrame(r8rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    ctl.to_csv(f"{OUT}.control.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    # ---------------------------------------------------------------- THE ANSWER
    say("")
    say("=" * 104)
    say("(A) THE ISO-EXPOSURE LINE — the committed 0.75 of realised exposure, walked in N")
    say("=" * 104)
    iso = grid[np.isclose(grid.expo_target, A_G)]
    for pname in grid.panel.unique():
        for slot in SLOTS:
            s = iso[(iso.panel == pname) & (iso.slot == slot)].sort_values("N")
            say(f"   {pname:9s} {slot:4s}  " + "  ".join(
                f"N={int(r.N):<2d} g{r.gross:.3f} DD {r.full_MaxDD:7.2%} CAGR {r.full_CAGR:6.2%} "
                f"Sh {r.full_Sharpe:.4f}" for _, r in s.iterrows()))
            dd = s.full_MaxDD.values
            mono_up = all(dd[i] <= dd[i + 1] for i in range(len(dd) - 1))     # DD improves in N
            mono_dn = all(dd[i] >= dd[i + 1] for i in range(len(dd) - 1))     # DD worsens in N
            say(f"   {'':9s} {'':4s}  d(MaxDD) over the line {(dd[-1]-dd[0])*100:+.2f}pp, argmax at "
                f"N={int(s.N.values[int(np.argmax(dd))])}; monotone improving {mono_up}, "
                f"monotone worsening {mono_dn}; rank corr(N, MaxDD) "
                f"{rankcorr(s.N.values, dd):+.2f}, rank corr(N, CAGR) "
                f"{rankcorr(s.N.values, s.full_CAGR.values):+.2f}")
    say("")
    say("   THE SAME LINE READ AGAINST THE UNMATCHED CONTROL (same N at the committed FLAT 0.75):")
    for pname in grid.panel.unique():
        for slot in SLOTS:
            s = iso[(iso.panel == pname) & (iso.slot == slot)].sort_values("N")
            c = ctl[(ctl.panel == pname) & (ctl.slot == slot)].sort_values("N")
            say(f"   {pname:9s} {slot:4s}  " + "  ".join(
                f"N={int(a.N):<2d} dDD {(a.full_MaxDD-b.full_MaxDD)*100:+5.2f}pp "
                f"dCAGR {(a.full_CAGR-b.full_CAGR)*100:+5.2f}pp"
                for (_, a), (_, b) in zip(s.iterrows(), c.iterrows())))

    say("")
    say("=" * 104)
    say("(B) THE WHOLE SURFACE — is MaxDD a function of EXPOSURE or of N?")
    say("=" * 104)
    for pname in grid.panel.unique():
        for slot in SLOTS:
            s = grid[(grid.panel == pname) & (grid.slot == slot)]
            sp_n = float(np.mean([s[np.isclose(s.expo_target, e)].full_MaxDD.max()
                                  - s[np.isclose(s.expo_target, e)].full_MaxDD.min() for e in EXPOLAD]))
            sp_e = float(np.mean([s[s.N == n].full_MaxDD.max() - s[s.N == n].full_MaxDD.min()
                                  for n in NLAD]))
            say(f"   {pname:9s} {slot:4s}  mean MaxDD spread ACROSS N at fixed exposure "
                f"{sp_n*100:5.2f}pp   ACROSS EXPOSURE at fixed N {sp_e*100:5.2f}pp   "
                f"ratio {sp_e/sp_n if sp_n else float('nan'):5.2f}x")

    say("")
    say("## SUMMARY")
    say(f"   cells {len(grid)} (+{len(ctl)} unmatched controls)   4a {int(grid.keep4a.sum())}   "
        f"4b {int(grid.keep4b.sum())}   unreachable {int((~grid.reachable).sum())}")
    for pname in grid.panel.unique():
        for slot in SLOTS:
            s = grid[(grid.panel == pname) & (grid.slot == slot)]
            say(f"   {pname:9s} {slot:4s} 4a {int(s.keep4a.sum()):2d}/{len(s)}  4b "
                f"{int(s.keep4b.sum()):2d}/{len(s)}   MaxDD {s.full_MaxDD.min():7.2%}.."
                f"{s.full_MaxDD.max():7.2%}   CAGR {s.full_CAGR.min():6.2%}..{s.full_CAGR.max():6.2%}"
                f"   Sharpe {s.full_Sharpe.min():.4f}..{s.full_Sharpe.max():.4f}   4b fails "
                f"{dict(s.fail4b.value_counts())}")
    say(f"   4b CONVERSIONS (the do-nothing cell fails 4b, this one passes):")
    for pname in grid.panel.unique():
        for slot in SLOTS:
            s = grid[(grid.panel == pname) & (grid.slot == slot)]
            dnr = s[(s.N == A_N) & np.isclose(s.expo_target, A_G)].iloc[0]
            conv = s[s.keep4b & (not bool(dnr.keep4b))]
            say(f"      {pname:9s} {slot:4s} do-nothing 4b {'PASS' if dnr.keep4b else 'FAIL('+dnr.fail4b+')'}"
                f"   conversions {len(conv)}"
                + ("".join(f"\n         N={int(r.N)}/EXPO={r.expo_target} g{r.gross:.3f}: "
                           f"{r.full_CAGR:.2%} / {r.full_Sharpe:.4f} / {r.full_MaxDD:.2%}"
                           for _, r in conv.iterrows()) if len(conv) else ""))
    say(f"   RULE 8: delta vs do-nothing {wf.delta.round(4).tolist()}  mean {wf.delta.mean():+.4f}  "
        f"beats do-nothing at {int((wf.delta > 0).sum())} of {len(wf)}")
    say(f"   rule-8 picks clearing a KEEP path: 4a {int(wf.pick_keep4a.sum())} of {len(wf)}, "
        f"4b {int(wf.pick_keep4b.sum())} of {len(wf)}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
