#!/usr/bin/env python3
"""Idea 1269 (lane cloud, 2026-09-18): does a FASTER EXIT GATE buy the DD LEG that every EXPOSURE
DIAL could not?

THE PREMISE, AND WHY THIS AXIS IS DIFFERENT FROM EVERY ONE ALREADY PRICED.  Every mechanism priced
on the standing 2026-09-04 KEEP 4b book moves HOW MUCH is held — 1262's explicit drawdown brake,
1263's portfolio vol target, 1264's inverse-vol slot sizing, 1266's correlation brake, 1267's
defensive rotation, 1268's idle sleeve — and each one loses to a FLAT GROSS CUT at the same mean
exposure.  1271's per-name trailing stop moved WHICH name is held at constant gross.  Nothing has
moved WHEN a name stops being ELIGIBLE, because entry and exit read the SAME 200d moving average:
a name is bought when it is above its 200d MA and is only droppable when it falls below the very
same line.  That symmetry is an inherited convention, not a measurement, and it is the one dial on
this book that changes the SPEED of the exit without changing the size of the book.

THE MECHANISM, EXACTLY.  The ENTRY gate is FROZEN at the committed 200d MA: a name may only be
newly selected when px[t-1] > MA200[t-1] AND vol20[t-1] < 0.60, exactly as the record has it.  The
EXIT gate is dialled separately.  At each weekly decision close t-1, a HELD name is EXPELLED when

    px[t-1, c]  <  MA_{EXIT_MA}[t-1, c] * (1 - EXIT_BAND)

and its slot is refilled at the same rebalance from the same eligible pool by the same ranking, so
the book stays at N names and the exit is NOT an exposure cut (gate G4 proves that rather than
assuming it).  THE EXIT OVERRIDES THE H=126 MINIMUM HOLD, stated plainly because it is the only
reading under which the mechanism has a dose at all: 1066 established that the min hold freezes
the book through exactly the weeks a drawdown is made, so an exit that yields to it would be
measuring the min hold, not the exit.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4), as the queue item words them:
    EXIT_MA    {50, 100, 150, 200} trading days — the moving average the EXIT reads.  200 is the
               entry gate's own length, i.e. the symmetric convention the record inherited.
    EXIT_BAND  {0.00, 0.01, 0.02, 0.03} — how far below that average a held name must close.
  4 x 4 = 16 cells, EVERY ONE PUBLISHED in the .grid.csv, plus a 17th cell:
    ANCHOR     the committed book with NO separate exit gate at all (a held name is droppable only
               by the ranking once its min hold expires).  THE DO-NOTHING CONTROL IS MEASURED, NOT
               ASSUMED, and gate G1 replays it against the committed triple.
  Note that (EXIT_MA=200, EXIT_BAND=0.00) is NOT the anchor: it is the symmetric exit the record's
  convention implies but has never actually run, because the anchor's min hold overrides it.  The
  DIFFERENCE between those two cells is this run's first number.

THE COMPARAND THE TITLE NAMES: THE DE-GROSSING FRONTIER.  The title says "the DD leg that every
EXPOSURE DIAL could not", so the bar is the cheapest known exposure dial, not the anchor.  The
same anchor book, no exit gate, held at GROSS {0.75, 0.65, 0.55, 0.45, 0.35, 0.25} — six points,
no dial, chosen on nothing — gives a (MaxDD, CAGR) exchange rate.  An exit cell BEATS the exposure
dials only if it sits ABOVE that frontier: more CAGR than the flat gross cut that reaches the SAME
MaxDD, read by linear interpolation along the frontier.  Every cell's frontier gap is published.

THE DOSE-MATCHED CONTROL ARM, not a dial, reported at every cell.  The record has established
(931) that churn alone is worth a turnover rebate, so "the faster exit helped" means nothing until
the same amount of churn with NO PRICE INPUT is differenced out:
    RANDOM     expel the SAME NUMBER of held names at the SAME rebalances, chosen uniformly at
               random from the book (3 fixed seeds).  EXIT minus RANDOM is the number this run is
               actually about.  Dose is matched by COUNT and by WEEK, not by identity — the arms'
               books diverge after the first expulsion, as they must.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: ENTRY eligibility = above own 200d
MA AND vol20 < 0.60; RAW three-leg composite (21/252, 0/126, 0/63 percentile ranks, equally
weighted, NO vol scaler); N = 20 slots; H = 126 minimum hold on names the exit does not take;
GROSS = 0.75; WEEKLY decide-Friday / trade-Monday; 10 bps per unit turnover; t+1 execution;
260-row warm-up; equal gross/len(held) slots (the committed RESPREAD fill).

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) INERT — a held name that is below a 50d MA is nearly always already below its 200d MA on
      this book, so the faster gates barely fire and MaxDD moves less than 0.20pp everywhere.
      Then the exit speed is not a free axis at all and the symmetry was never binding.
  (B) THE DD LEG IS BOUGHT AT CONSTANT EXPOSURE — some cell materially improves MaxDD, holds 4b's
      CAGR floor and both half-Sharpe legs, BEATS ITS OWN RANDOM ARM at the same dose, sits ABOVE
      the de-grossing frontier, and rule 8 reaches it.  KEEP-candidate memo with exact RULES
      wording.
  (C) BOUGHT BY CHURN — MaxDD improves but RANDOM at the same dose does as well or better, i.e.
      the price input in the exit is decorative.
  (D) WHIPSAW — the faster exit sells into the dip and the book buys back higher, so drawdown
      and/or Sharpe degrade against doing nothing.
  Not mutually exclusive across panels; whichever fire are reported as they fall, and the capital
  verdict follows rule 8, never the best cell.

RULE 8 (walk-forward, required).  (EXIT_MA, EXIT_BAND) is CHOSEN on warm-up..2016-12-31 by IS
Sharpe ALONE over the 16 exit cells and 2017-2026 is read ONCE, per (panel, arm).  Reported
against the ANCHOR, the cell mean, the worst cell, the best cell (recorded, never promoted) and
the IS/OOS rank correlation.  The capital verdict is the sign of chooser-minus-do-nothing.

GATES.  G1 vintage-pinned replay truncated at 2026-09-16: the U56 ANCHOR must replay the committed
15.7147% / 1.1480 / -19.1276% to 1e-4.  G2 the ANCHOR cell is bit-identical however it is reached.
G3 the mechanism HAS a dose: expulsion counts and the share of rebalances with an expulsion are
published per cell and must be > 0 somewhere, or outcome (A) is declared on the spot.  G4 THE EXIT
IS NOT AN EXPOSURE CUT: realised mean gross at every cell is within 1pp of the anchor's and no
cell's drifted max gross exceeds the anchor's (the anchor itself drifts above 0.75 between weekly
rebalances — 1271 established that, and the bar is the ANCHOR's own drift, not 0.75).  G5
CAUSALITY: the exit flag at decision i recomputed from prices TRUNCATED at i is bit-identical to
the full-sample flag.  G6 MONOTONE DOSE: the expulsion count is non-increasing in EXIT_MA at fixed
band (a longer average is a lower bar to clear) and non-increasing in EXIT_BAND at fixed MA.  G7
the RANDOM arm expels exactly min(the EXIT arm's count, what it holds) at each rebalance — the
dose match is verified, not asserted.  G8 determinism: the U56 grid recomputed bit for bit.  G9
the one-extra-day cache drift against the pinned vintage, published not toleranced.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one idea,
one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists and SMALL is a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before anything is
computed).  Every absolute level is optimistic and every 4b pass an UPPER bound.  A faster exit is
biased AGAINST by this, not for: on a panel of names that all recovered, selling a dip is a
mistake the tape always punishes, so an exit gate that still wins here would be winning against
the bias.  The contrast against RANDOM and against the de-grossing frontier is first-order immune;
the 4b legs are not.
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
SLUG = "does-a-FASTER-EXIT-GATE-buy-the-DD-LEG-that-every-EXPOSURE-DIAL-could-not"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                      # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]
EXIT_MAS = [50, 100, 150, 200]                     # DIAL 1
EXIT_BANDS = [0.00, 0.01, 0.02, 0.03]              # DIAL 2
ANCHOR = (0, -1.0)                                 # the 17th cell: NO separate exit gate
GROSS_LADDER = [0.75, 0.65, 0.55, 0.45, 0.35, 0.25]   # the DE-GROSSING FRONTIER
RAND_SEEDS = [11, 23, 37]
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)
VINTAGE = pd.Timestamp("2026-09-16")
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


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0) if len(r) >= 20 else np.nan


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r),
                Vol=float(np.asarray(r, float).std(ddof=0) * np.sqrt(252)))


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
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), is_=stats(r[:o]), oos=stats(r[o:]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


def cname(ma, band):
    return "ANCHOR" if band < 0 else f"MA{ma}/b{band:.2f}"


class Panel:
    """The committed book's inputs, plus one moving average per EXIT_MA length, computed once."""

    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        self.q = q.values
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)   # smaller = better
        self.ma = {L: q.rolling(L).mean().values for L in sorted(set(EXIT_MAS + [200]))}
        self.above = (self.q > self.ma[200])                    # the FROZEN ENTRY gate
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.elig = self.above & self.volok
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def exit_flags(pan, ma_len, band, ts):
    """A HELD name is expelled when its decision close sits below MA_{ma_len} * (1 - band).
    Read at ts = t - 1 (rule 2).  An unpriced or un-averaged name is never expelled by the gate."""
    p = pan.q[ts]
    m = pan.ma[ma_len][ts]
    ok = np.isfinite(p) & np.isfinite(m)
    return ok & (p < m * (1.0 - band))


def build(pan, arm, ma_len, band, seed=0, counts=None, N=A_N, H=A_H, lag=1):
    """The committed selection with a SEPARATELY DIALLED EXIT.  arm EXIT expels held names on the
    exit gate; arm RANDOM expels the SAME COUNT at the SAME rebalance (passed in `counts`) with no
    price input.  band < 0 means NO exit gate at all (the committed ANCHOR)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    S = np.zeros((T, M))
    NSL = np.zeros(T)
    entry = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    out_counts = np.zeros(nreb, dtype=np.int64)
    held_counts = np.zeros(nreb, dtype=np.int64)
    rng = np.random.default_rng(7_919 * seed + 13)
    weeks = expel_weeks = expel_tot = 0.0
    holdlen: list[float] = []
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(entry >= 0)
        if len(held):
            held = held[pr[t, held]]
        held_counts[i] = len(held)
        # --- the EXIT rule ---
        expel: list[int] = []
        if arm == "EXIT":
            if band >= 0 and len(held):
                f = exit_flags(pan, ma_len, band, ts)
                expel = [int(c) for c in held if f[c]]
        else:
            want = min(int(counts[i]) if counts is not None else 0, len(held))
            if want > 0:
                expel = [int(c) for c in rng.choice(held, size=want, replace=False)]
        out_counts[i] = len(expel)
        for c in expel:
            holdlen.append(float(t - entry[c]))
            entry[c] = -1
        # --- the committed selection, on what is left; the ENTRY gate is FROZEN ---
        held = np.flatnonzero(entry >= 0)
        if len(held):
            held = held[pr[t, held]]
        keep = [int(c) for c in held[(t - entry[held]) < H]] if len(held) else []
        k = pan.key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        for c in keep:
            k[c] = np.inf
        take, need = [], N - len(keep)
        for c in np.argsort(k, kind="stable"):
            if need == 0 or not np.isfinite(k[int(c)]):
                break
            take.append(int(c))
            need -= 1
        was = entry.copy()
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = entry[c]
        for c in take:
            new[c] = t                       # the min-hold clock restarts (COMMITTED behaviour)
        entry = new
        sel = keep + take
        if t >= WARMUP:
            weeks += 1.0
            if expel:
                expel_weeks += 1.0
                expel_tot += len(expel)
        if not sel:
            continue
        stop_i = pan.reb[i + 1] if i + 1 < nreb else T
        S[t:stop_i, pan.iinv[np.array(sel)]] = 1.0
        NSL[t:stop_i] = len(sel)
    d = max(weeks, 1.0)
    diag = dict(expel_week_share=expel_weeks / d, expel_per_year=expel_tot / (d / 52.0),
                expel_total=expel_tot, held_counts=held_counts,
                mean_expelled_hold=float(np.mean(holdlen)) if holdlen else 0.0)
    return S, NSL, out_counts, diag


def run(pan, S, NSL, gross=A_G):
    """The committed RESPREAD fill: gross/len(held) per held name, 10 bps on traded notional,
    drift between rebalances."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        n = NSL[i0]
        if n <= 0:
            curw = np.zeros(M)
            continue
        per = gross / n
        w0 = per * S[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    expo = held[WARMUP:].sum(axis=1)
    return r, float(turn.sum() / (T / 252.0)), float(expo.mean()), float(expo.max())


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


def frontier_cagr(front, dd):
    """CAGR the FLAT GROSS CUT delivers at MaxDD `dd`, by linear interpolation along the frontier.
    Returns nan outside the frontier's own MaxDD range (never extrapolated)."""
    pts = sorted(front, key=lambda x: x[0])          # (MaxDD, CAGR), MaxDD negative
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if dd < xs[0] or dd > xs[-1]:
        return float("nan")          # DEEPER (or shallower) than the frontier's own range
    return float(np.interp(dd, xs, ys))


def main():
    t0 = time.time()
    say(f"# {DATE} idea 1269 lane cloud — {SLUG}")
    say(f"# frozen book: RAW 3-leg composite, ENTRY gate = above 200d MA AND vol20 < {MAXVOL}, "
        f"N={A_N}, H={A_H} (the EXIT overrides it), GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 EXIT_MA = {EXIT_MAS}   DIAL 2 EXIT_BAND = {EXIT_BANDS}   + the ANCHOR (no exit gate)")
    say(f"# dose-matched control arm (not a dial): RANDOM over seeds {RAND_SEEDS}")
    say(f"# comparand: the DE-GROSSING FRONTIER, anchor at GROSS {GROSS_LADDER}")
    say("# THE EXIT REFILLS THE FREED SLOT, SO IT IS NOT AN EXPOSURE CUT — G4 proves it rather than assuming it")
    say("# (EXIT_MA=200, band=0.00) is NOT the anchor: it is the symmetric exit the record's convention "
        "implies but has never run, because the min hold overrides it.")

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

    rows: list[dict] = []
    r8rows: list[dict] = []
    frows: list[dict] = []
    dose_rows: list[dict] = []

    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"{idx[0].date()}..{idx[-1].date()}  n_rebalances={len(pan.reb)}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}   CAGR floor "
            f"{CAGR_FLOOR*spy['full']['CAGR']:7.2%}   Sharpe bars H1 {spy['h1']['Sharpe']:.4f} "
            f"H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")

        # ---- the DE-GROSSING FRONTIER: the exposure dials' own exchange rate ----
        Sa, NSLa, cnt_a, diag_a = build(pan, "EXIT", *ANCHOR)
        front = []
        for g in GROSS_LADDER:
            rg, tg, gmg, _ = run(pan, Sa, NSLa, gross=g)
            wg = windows(idx, rg[WARMUP:])
            front.append((wg["full"]["MaxDD"], wg["full"]["CAGR"]))
            b4 = legs_4b(wg, spy)
            frows.append(dict(panel=pname, gross=g, CAGR=wg["full"]["CAGR"],
                              Sharpe=wg["full"]["Sharpe"], MaxDD=wg["full"]["MaxDD"],
                              OOS_Sharpe=wg["oos"]["Sharpe"], turnover=tg, gross_mean=gmg,
                              pass4b=all(b4.values()), fail4b=failed(b4)))
        say(f"   DE-GROSSING FRONTIER (anchor at each gross): "
            + "  ".join(f"g{g:.2f} {d:.2%}/{c:.2%}" for (d, c), g in zip(front, GROSS_LADDER)))

        # ---- the EXIT arm first: it defines the dose the control must match ----
        cells: dict = {}
        counts_by_cell: dict = {}
        ra, ta, gma, gxa = run(pan, Sa, NSLa)
        wa = windows(idx, ra[WARMUP:])
        cells[("EXIT",) + ANCHOR + (0,)] = (wa, ta, gma, gxa, diag_a)
        counts_by_cell[ANCHOR] = cnt_a
        for ma_len in EXIT_MAS:
            for band in EXIT_BANDS:
                S, NSL, cnt, diag = build(pan, "EXIT", ma_len, band)
                r, turn, gm, gx = run(pan, S, NSL)
                cells[("EXIT", ma_len, band, 0)] = (windows(idx, r[WARMUP:]), turn, gm, gx, diag)
                counts_by_cell[(ma_len, band)] = cnt
                dose_rows.append(dict(panel=pname, EXIT_MA=ma_len, EXIT_BAND=band,
                                      **{k: v for k, v in diag.items() if k != "held_counts"},
                                      expel_weeks_pct=100 * diag["expel_week_share"]))

        # ---- the dose-matched RANDOM arm ----
        dose_err = 0
        for ma_len in EXIT_MAS:
            for band in EXIT_BANDS:
                for sd in RAND_SEEDS:
                    S, NSL, cnt, diag = build(pan, "RANDOM", ma_len, band, seed=sd,
                                              counts=counts_by_cell[(ma_len, band)])
                    r, turn, gm, gx = run(pan, S, NSL)
                    cells[("RANDOM", ma_len, band, sd)] = (windows(idx, r[WARMUP:]), turn, gm, gx, diag)
                    tgt = counts_by_cell[(ma_len, band)]
                    want = np.minimum(tgt, diag["held_counts"])   # the legal case: fewer names held
                    dose_err = max(dose_err, int(np.abs(cnt - want).max()))

        # ---------- the grid, printed in full ----------
        say(f"   {'cell':>13} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} {'OOS_S':>7} "
            f"{'turn':>6} {'exp/yr':>7} {'gross':>6} {'4a':>3} {'4b':>3} {'fail4b':>12} "
            f"{'dCAGRvFRONT':>12} {'RND_S':>7} {'RND_DD':>8}")
        order = [ANCHOR] + [(m, b) for m in EXIT_MAS for b in EXIT_BANDS]
        for ma_len, band in order:
            w, turn, gm, gx, diag = cells[("EXIT", ma_len, band, 0)]
            a4a, a4b = legs_4a(w, live), legs_4b(w, spy)
            fc = frontier_cagr(front, w["full"]["MaxDD"])
            gapc = w["full"]["CAGR"] - fc
            rs = [cells[("RANDOM", ma_len, band, s)][0] for s in RAND_SEEDS] if band >= 0 else []
            rS = float(np.mean([x["full"]["Sharpe"] for x in rs])) if rs else float("nan")
            rD = float(np.mean([x["full"]["MaxDD"] for x in rs])) if rs else float("nan")
            say(f"   {cname(ma_len, band):>13} {w['full']['CAGR']:>8.2%} {w['full']['Sharpe']:>8.4f} "
                f"{w['full']['MaxDD']:>8.2%} {w['h1']['Sharpe']:>7.4f} {w['h2']['Sharpe']:>7.4f} "
                f"{w['oos']['Sharpe']:>7.4f} {turn:>6.2f} {diag['expel_per_year']:>7.2f} {gm:>6.4f} "
                f"{'Y' if all(a4a.values()) else 'n':>3} {'Y' if all(a4b.values()) else 'n':>3} "
                f"{failed(a4b):>12} "
                f"{('  DEEPER-THAN' if not np.isfinite(gapc) else f'{100*gapc:>11.2f}p'):>12} "
                f"{rS:>7.4f} {rD:>8.2%}")
            rows.append(dict(panel=pname, cell=cname(ma_len, band), anchor=(band < 0),
                             EXIT_MA=(None if band < 0 else ma_len),
                             EXIT_BAND=(None if band < 0 else band),
                             turnover=turn, gross_mean=gm, gross_max=gx,
                             expel_per_year=diag["expel_per_year"],
                             expel_week_pct=100 * diag["expel_week_share"],
                             mean_expelled_hold=diag["mean_expelled_hold"],
                             frontier_CAGR_at_same_MaxDD=fc, CAGR_minus_frontier_pp=100 * gapc,
                             deeper_than_frontier_range=bool(
                                 not np.isfinite(fc) and w["full"]["MaxDD"] < min(d for d, _ in front)),
                             rand_Sharpe=rS, rand_MaxDD=rD,
                             exit_minus_rand_Sharpe=w["full"]["Sharpe"] - rS,
                             exit_minus_rand_MaxDD_pp=100 * (w["full"]["MaxDD"] - rD),
                             pass4a=all(a4a.values()), fail4a=failed(a4a),
                             pass4b=all(a4b.values()), fail4b=failed(a4b), **flat(w)))

        # ---------- GATES ----------
        if pname == "U56":
            vpx = p_px.loc[:VINTAGE]
            vpan = Panel("U56v", vpx, inv)
            Sv, NSLv, _, _ = build(vpan, "EXIT", *ANCHOR)
            rv, _, _, _ = run(vpan, Sv, NSLv)
            wv = windows(vpan.idx[WARMUP:], rv[WARMUP:])
            err = max(abs(wv["full"]["CAGR"] - COMMITTED_U56[0]),
                      abs(wv["full"]["Sharpe"] - COMMITTED_U56[1]),
                      abs(wv["full"]["MaxDD"] - COMMITTED_U56[2]))
            gate("G1 vintage replay of committed anchor", f"maxerr {err:.3e} "
                 f"({wv['full']['CAGR']:.4%}/{wv['full']['Sharpe']:.4f}/{wv['full']['MaxDD']:.4%})",
                 "<= 1e-4", err <= 1e-4)
            # G5 causality: the exit flag recomputed on TRUNCATED prices
            bad5 = 0
            for i in range(WARMUP, len(pan.reb), 37):
                t = pan.reb[i]
                ts = max(t - 1, 0)
                sub = Panel("trunc", p_px.iloc[:ts + 1], inv)
                for ma_len in EXIT_MAS:
                    for band in EXIT_BANDS:
                        a = exit_flags(pan, ma_len, band, ts)
                        b = exit_flags(sub, ma_len, band, ts)
                        bad5 += int((a != b).sum())
            gate("G5 causality (exit flag on truncated prices)", f"{bad5} flag mismatches",
                 "0", bad5 == 0)
            S2, NSL2, _, _ = build(pan, "EXIT", *ANCHOR)
            r2, _, _, _ = run(pan, S2, NSL2)
            w2 = windows(idx, r2[WARMUP:])
            gate("G8 determinism (U56 anchor recomputed)",
                 f"dSharpe {abs(w2['full']['Sharpe']-wa['full']['Sharpe']):.3e}", "== 0",
                 w2["full"]["Sharpe"] == wa["full"]["Sharpe"])
            gate("G9 cache drift vs pinned vintage",
                 f"{len(pan.idx)-len(vpan.idx)} extra trading days (tape ends {pan.idx[-1].date()})",
                 "published, not toleranced", True)

        S3, NSL3, _, _ = build(pan, "EXIT", *ANCHOR)
        r3, _, _, _ = run(pan, S3, NSL3)
        w3 = windows(idx, r3[WARMUP:])
        gate(f"G2 anchor identity [{pname}]",
             f"dSharpe {abs(w3['full']['Sharpe']-wa['full']['Sharpe']):.3e}", "== 0",
             w3["full"]["Sharpe"] == wa["full"]["Sharpe"])

        tot = sum(cells[("EXIT", m, b, 0)][4]["expel_total"] for m in EXIT_MAS for b in EXIT_BANDS)
        gate(f"G3 the exit HAS a dose [{pname}]",
             f"{tot:.0f} expulsions over 16 cells; anchor expels "
             f"{cells[('EXIT',)+ANCHOR+(0,)][4]['expel_total']:.0f}", "> 0 / == 0",
             tot > 0 and cells[("EXIT",) + ANCHOR + (0,)][4]["expel_total"] == 0)

        gmax_bad = [(cname(m, b), cells[("EXIT", m, b, 0)][2], cells[("EXIT", m, b, 0)][3])
                    for m in EXIT_MAS for b in EXIT_BANDS
                    if abs(cells[("EXIT", m, b, 0)][2] - gma) > 0.01 or cells[("EXIT", m, b, 0)][3] > gxa + 1e-12]
        gate(f"G4 the exit is NOT an exposure cut [{pname}]",
             f"{len(gmax_bad)} of 16 cells off the anchor's exposure "
             f"(anchor mean {gma:.4f}, max {gxa:.4f}): {gmax_bad[:2]}",
             "0 cells", not gmax_bad)

        mono_ma = all(cells[("EXIT", EXIT_MAS[i], b, 0)][4]["expel_total"]
                      >= cells[("EXIT", EXIT_MAS[i + 1], b, 0)][4]["expel_total"]
                      for b in EXIT_BANDS for i in range(len(EXIT_MAS) - 1))
        mono_b = all(cells[("EXIT", m, EXIT_BANDS[i], 0)][4]["expel_total"]
                     >= cells[("EXIT", m, EXIT_BANDS[i + 1], 0)][4]["expel_total"]
                     for m in EXIT_MAS for i in range(len(EXIT_BANDS) - 1))
        gate(f"G6 monotone dose [{pname}]",
             f"expulsions fall with EXIT_MA: {mono_ma}; fall with EXIT_BAND: {mono_b}",
             "both True", mono_ma and mono_b)

        gate(f"G7 RANDOM dose match [{pname}]",
             f"max |RANDOM count - min(EXIT count, names held)| = {dose_err}",
             "0 (the dose match is verified, not asserted)", dose_err == 0)

        # ---------- RULE 8 ----------
        grid = [(m, b) for m in EXIT_MAS for b in EXIT_BANDS]
        iss = [cells[("EXIT", m, b, 0)][0]["is_"]["Sharpe"] for m, b in grid]
        oos = [cells[("EXIT", m, b, 0)][0]["oos"]["Sharpe"] for m, b in grid]
        pick = grid[int(np.nanargmax(iss))]
        pw = cells[("EXIT",) + pick + (0,)][0]
        best = grid[int(np.nanargmax(oos))]
        worst = grid[int(np.nanargmin(oos))]
        p4b = legs_4b(pw, spy)
        say(f"\n   RULE 8 [{pname}] IS-Sharpe chooser over {len(grid)} exit cells -> "
            f"{cname(*pick)}  IS {cells[('EXIT',)+pick+(0,)][0]['is_']['Sharpe']:.4f}")
        say(f"      chosen  OOS {pw['oos']['CAGR']:7.2%} / {pw['oos']['Sharpe']:.4f} / "
            f"{pw['oos']['MaxDD']:7.2%}   4b {'PASS' if all(p4b.values()) else 'FAIL(' + failed(p4b) + ')'}")
        say(f"      anchor  OOS {wa['oos']['CAGR']:7.2%} / {wa['oos']['Sharpe']:.4f} / "
            f"{wa['oos']['MaxDD']:7.2%}")
        say(f"      chooser minus do-nothing (OOS Sharpe) = {pw['oos']['Sharpe']-wa['oos']['Sharpe']:+.4f}")
        say(f"      cell mean OOS {np.nanmean(oos):.4f}   best (recorded, NOT promoted) "
            f"{cname(*best)} {cells[('EXIT',)+best+(0,)][0]['oos']['Sharpe']:.4f}   "
            f"worst {cname(*worst)} {cells[('EXIT',)+worst+(0,)][0]['oos']['Sharpe']:.4f}")
        say(f"      IS/OOS rank correlation over the grid = {rankcorr(iss, oos):.4f}")
        r8rows.append(dict(panel=pname, pick=cname(*pick), pick_MA=pick[0], pick_BAND=pick[1],
                           IS_Sharpe=cells[("EXIT",) + pick + (0,)][0]["is_"]["Sharpe"],
                           OOS_Sharpe=pw["oos"]["Sharpe"], OOS_CAGR=pw["oos"]["CAGR"],
                           OOS_MaxDD=pw["oos"]["MaxDD"], pass4b=all(p4b.values()), fail4b=failed(p4b),
                           anchor_OOS_Sharpe=wa["oos"]["Sharpe"], anchor_OOS_CAGR=wa["oos"]["CAGR"],
                           anchor_OOS_MaxDD=wa["oos"]["MaxDD"],
                           chooser_minus_donothing=pw["oos"]["Sharpe"] - wa["oos"]["Sharpe"],
                           cell_mean_OOS=float(np.nanmean(oos)), best=cname(*best),
                           best_OOS_Sharpe=cells[("EXIT",) + best + (0,)][0]["oos"]["Sharpe"],
                           worst_OOS_Sharpe=cells[("EXIT",) + worst + (0,)][0]["oos"]["Sharpe"],
                           spy_OOS_Sharpe=spy["oos"]["Sharpe"], rank_corr=rankcorr(iss, oos)))

        # ---------- the two headline contrasts ----------
        sub = [r for r in rows if r["panel"] == pname and not r["anchor"]]
        above = [r for r in sub if np.isfinite(r["CAGR_minus_frontier_pp"])
                 and r["CAGR_minus_frontier_pp"] > 0]
        beats = [r for r in sub if np.isfinite(r["exit_minus_rand_Sharpe"])
                 and r["exit_minus_rand_Sharpe"] > 0]
        ddb = [r for r in sub if np.isfinite(r["exit_minus_rand_MaxDD_pp"])
               and r["exit_minus_rand_MaxDD_pp"] > 0]
        say(f"   CONTRASTS [{pname}]: ABOVE the de-grossing frontier at {len(above)} of {len(sub)} cells; "
            f"beats its own RANDOM arm on Sharpe at {len(beats)} of {len(sub)}, on MaxDD at {len(ddb)} of {len(sub)}")
        sh = max(sub, key=lambda r: r["full_MaxDD"])      # SHALLOWEST drawdown among the exit cells
        deep = sum(1 for r in sub if r["deeper_than_frontier_range"])
        say(f"      anchor {wa['full']['MaxDD']:.2%} / {wa['full']['CAGR']:.2%} -> SHALLOWEST exit cell "
            f"{sh['cell']} {sh['full_MaxDD']:.2%} / {sh['full_CAGR']:.2%} "
            f"({100*(sh['full_MaxDD']-wa['full']['MaxDD']):+.2f}pp of MaxDD for "
            f"{100*(sh['full_CAGR']-wa['full']['CAGR']):+.2f}pp of CAGR); "
            f"{deep} of {len(sub)} cells draw down DEEPER than the anchor at full gross, i.e. off the "
            f"frontier's range entirely")

    # ---------------- outputs ----------------
    g = pd.DataFrame(rows)
    g.to_csv(f"{STEM}.grid.csv", index=False)
    pd.DataFrame(r8rows).to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(frows).to_csv(f"{STEM}.frontier.csv", index=False)
    pd.DataFrame(dose_rows).to_csv(f"{STEM}.dose.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    ex = g[~g.anchor]
    say(f"\n## SUMMARY  {len(g)} cells ({len(ex)} exit cells + {int(g.anchor.sum())} anchors), "
        f"{len(panels)} panels")
    say(f"   4a passes: {int(g.pass4a.sum())} of {len(g)}    4b passes: {int(g.pass4b.sum())} of {len(g)}")
    for p in g.panel.unique():
        s = g[g.panel == p]
        say(f"   {p:>10}: 4a {int(s.pass4a.sum())}/{len(s)}   4b {int(s.pass4b.sum())}/{len(s)}")
    fails = [x for r in g[~g.pass4b].fail4b for x in r.split(",") if x != "-"]
    say(f"   4b leg failure counts over {len(g)-int(g.pass4b.sum())} failing cells: "
        f"{pd.Series(fails).value_counts().to_dict()}")
    say(f"   ABOVE the de-grossing frontier: {int((ex.CAGR_minus_frontier_pp > 0).sum())} of {len(ex)} exit cells "
        f"({int(ex.deeper_than_frontier_range.sum())} of them draw down deeper than the anchor at full gross, "
        f"so the frontier cannot even reach them)")
    say(f"   beats its own RANDOM arm on Sharpe: {int((ex.exit_minus_rand_Sharpe > 0).sum())} of {len(ex)}; "
        f"on MaxDD: {int((ex.exit_minus_rand_MaxDD_pp > 0).sum())} of {len(ex)}")
    npass, nt = int(pd.DataFrame(GATES).pass_.sum()), len(GATES)
    say(f"   GATES {npass} of {nt} PASS   elapsed {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
