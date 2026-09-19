#!/usr/bin/env python3
"""
Idea 1373 (lane C, 2026-09-19) — does INVERSE-VOL SLOT WEIGHTING buy the BINDING 4b DD LEG
that the EQUAL-WEIGHT incumbent leaves open?

WHY THIS IDEA.  The sprint rule gives lane C the SECOND numbered item in QUEUE.md's '## Open'.
First is 1204, second 1198; both, and 1194 / 1182 / 1184-1186 under them, are record-bookkeeping
censuses of committed text, gates or margins.  None yields a weights function, so none can carry
this sprint's binding step-3 deliverable (a book scored against live RULES v2 AND SPY, both KEEP
paths, rule-8 walk-forward).  The documented fallback was taken: 1369 / 1373 / 1377 were filed as
price-only follow-ups on the standing incumbent and this lane claimed the second, 1373.

THE PREMISE.  The standing 2026-09-04 KEEP-4b candidate (U56, N=20 slots, H=126-day minimum hold,
gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1) gives every slot 1/N of gross.  A name
whose 20-day annualised vol is 0.55 and one at 0.15 therefore carry the SAME capital and wildly
different risk.  The record says the DRAWDOWN CAP is this book's SOLE binding 4b leg (1215, 1296,
1346, 1358, 1366 all attack it; 1350 measures the margin at +1.10 pp).  Risk-budgeting the slots
is the one attack on that leg that changes NO selection and NO exposure: gross stays 0.75, the
same 20 names are held on the same days, only their relative sizes move.

WHAT THIS IS NOT.  It is NOT the vol scaler the 2026-09-04 KEEP killed.  That divided the
SELECTION SCORE by sqrt(vol20) and cancelled the signal (2026-09-03 memo Finding 1: composite IC
t +4.2, scaler IC t -5.7, product t +0.4).  Here the ranking, the eligibility test and the slot
count are byte-identical to the incumbent at every rung; vol enters only the SIZE of a slot that
the incumbent has already decided to hold.  Gate G3 pins that: at p = 0 every cell reproduces the
incumbent bit for bit.

THE ONE DIAL AND NO MORE (PROTOCOL rule 4 — exactly two tuned parameters, p and panel):
    p      the inverse-vol exponent.  Slot i gets weight proportional to (1 / vol_i)^p,
           normalised over the held set, times gross 0.75.  p = 0 IS the incumbent
           (equal weight); p = 1 is textbook inverse-vol; p = 0.5 is the "half-risk" rung the
           risk-parity literature uses when vol estimates are noisy.  Rungs {0, 0.25, 0.5, 0.75,
           1.0, 1.5}, ALL reported.
    panel  {U56, B136, SMALL} — the record's three standing panels.

NOT DIALS, reported at every value (controls, never chosen on):
    VOLWIN {20, 60}   the vol estimator's window.  20 days is the book's OWN vol20 (the number
                      its eligibility test already computes, so it costs the rule nothing new);
                      60 days is the slower estimate.  Both published at every p.  Vol is read at
                      the DECISION row (t-1), annualised, and clipped to [0.08, 2.00] — the 0.08
                      floor is the live rules' own clip (baseline.score), the 2.00 ceiling only
                      bounds a division and never binds inside the eligibility test.
    SHUFFLE null      the same weight VECTOR dealt to the held names in permuted order (200
                      seeds, seed base 20260919).  This holds the weight DISPERSION exactly and
                      destroys only the vol INFORMATION, which is the one control that can tell
                      "risk budgeting works" apart from "unequal weights work".
    Paired circular-block bootstrap, 400 reps x 63-row blocks, seed 20260919, identical blocks on
                      both sides, on the (p-rung minus incumbent) daily difference — full and OOS.

PRE-DECLARED OUTCOMES, written before any number below was read:
  H_DD     inverse-vol at p = 1 SHALLOWS U56 MaxDD by at least 1.0 pp against p = 0 (the leg is
           the binder, and equal weight is the crudest possible risk budget).
  H_SHARPE the Sharpe gain at p = 1 is resolvable (|t| > 2 on the paired block bootstrap) on at
           least 2 of 3 panels, FULL and OOS.
  H_INFO   the real inverse-vol book beats its own dispersion-matched SHUFFLE null at better than
           the 95th percentile — i.e. the gain is vol information, not weight dispersion.
  H_PICK   the rule-8 chooser (argmax IS net Sharpe over the p ladder on warm-up..2016-12-31,
           ties to the lower p, 2017-2026 read ONCE) does NOT beat the do-nothing anchor p = 0.
           Every dial the record has walked has failed this (1362 N, 1366 H, 1358 sleeve).
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not the full sample.

GATES.  G1 the p = 0 / VOLWIN 20 U56 cell replays the committed incumbent anchor (15.80% / 1.1537
/ -19.13%, idea 1350's head-vintage triple) to within the 5e-3 tape-vintage Sharpe floor that same
run established; the deviation is PUBLISHED, not asserted.  G2 weights sum to exactly gross at
every rebalance row of every cell (|dev| < 1e-12).  G3 p = 0 is bit-for-bit identical across both
VOLWIN values and to the fast runner's incumbent.  G4 all 36 grid cells and all controls published.
G5 exactly two tuned parameters.  G6 the chooser reads no row on or after 2017-01-01.  G7
determinism: the headline cell recomputed bit for bit.  G8 effective number of names (1/HHI of the
held weights) is non-increasing in p at every panel.

PROTOCOL: rule 1 committed caches, >= 10 years; rule 2 10 bps per unit turnover, t+1 execution;
rule 3 compared against live RULES v2 AND SPY on each panel; rule 4 both KEEP paths at every cell;
rule 5 one idea, one script, deterministic, standalone; rule 8 walk-forward as above; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first), so every absolute
level is an upper bound and every 4b pass an optimistic one.  The headline is a DIFFERENCE between
two weightings of the SAME held names on the SAME days, which is first-order immune to a level
bias common to both; the pass COUNT is not.

Offline and deterministic (committed caches only, no network, no yfinance):
  python research/backtests/2026-09-19_inverse-vol-slot-weighting_C.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import EXCLUDE, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask             # noqa: E402

DATE, SLUG = "2026-09-19", "inverse-vol-slot-weighting"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
A_N, A_H, A_G = 20, 126, 0.75                  # the frozen 2026-09-04 incumbent
LEGS = [(21, 252), (0, 126), (0, 63)]          # the committed RAW three-leg composite
P_LADDER = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5]
VOLWINS = [20, 60]
VCLIP = (0.08, 2.00)
OOS_START, IS_END = pd.Timestamp("2017-01-01"), pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NSHUF, NBOOT, BLOCK = 20260919, 200, 400, 63
COMMITTED_U56 = (0.1580, 1.1537, -0.1913)      # idea 1350 head-vintage anchor
TAPE_FLOOR = 5e-3

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


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
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    n, h = len(r), len(r) // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]),
                **{"is": stats(r[:o])})


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


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


# ------------------------------------------------------------------ panels
UNIV = sorted({t for g in json.loads((ROOT / "research" / "universe.json").read_text()).values()
               for t in g} - set(EXCLUDE))
_meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD_SMALL = set(_meta.loc[_meta.max_1d_move >= 1.0, "ticker"])


def _read(path, gz=False):
    return pd.read_csv(path, index_col=0, parse_dates=True).sort_index()


class Panel:
    """One standing panel with the incumbent's selection inputs precomputed."""

    def __init__(self, name, px, invest):
        self.name, self.px, self.idx = name, px, px.index
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        q = px[invest]
        self.rets = q.pct_change().fillna(0.0).values            # invest-column returns
        self.priced = q.notna().values
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        dr = q.pct_change()
        v20 = (dr.rolling(20).std() * np.sqrt(252)).values
        v60 = (dr.rolling(60).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(v20, nan=1e9) < MAXVOL)
        self.vol = {20: v20, 60: v60}
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.C = C
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])   # price relative at t-1
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.T = len(px)


def panels():
    out = []
    raw = _read(ROOT / "data" / "prices.csv")
    keep = [c for c in UNIV if c in raw.columns]
    px = raw[keep].loc["2008-01-01":].dropna(how="all").ffill()
    out.append(Panel("U56", px, [c for c in px.columns if c != "SPY"]))

    pb = _read(ROOT / "data" / "prices_broad.csv").loc["2008-01-01":].dropna(how="all").ffill()
    out.append(Panel("B136", pb, [c for c in pb.columns if c != "SPY"]))

    ps = pd.read_csv(ROOT / "data" / "prices_small.csv.gz", index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":].dropna(how="all").ffill()
    spy = raw["SPY"].reindex(ps.index, method="ffill").rename("SPY")
    ps = pd.concat([ps.drop(columns=["SPY"], errors="ignore"), spy], axis=1)
    inv = [c for c in ps.columns if c != "SPY" and c not in BAD_SMALL]
    out.append(Panel("SMALL", ps, inv))
    return out


# ------------------------------------------------------------------ the frozen selection
def build_sel(pan, N=A_N, H=A_H, lag=1):
    """The incumbent's held set per rebalance segment.  Independent of p by construction:
    returns [(i0, i1, sel indices into invest columns, decision row)]."""
    K = len(pan.iinv)
    segs = []
    cur = np.full(K, -1, dtype=np.int64)
    pr, T, nreb = pan.priced, pan.T, len(pan.reb)
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
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        if len(sel):
            segs.append((int(t), int(stop), sel.copy(), int(ts)))
    return segs


def slot_weights(pan, sel, ts, p, volwin, rng=None):
    """Normalised slot weights (sum 1) for the held set.  p=0 is equal weight exactly."""
    n = len(sel)
    if p == 0.0:
        return np.full(n, 1.0 / n)
    v = pan.vol[volwin][ts, sel].astype(float)
    if not np.isfinite(v).any():
        return np.full(n, 1.0 / n)
    v = np.where(np.isfinite(v), v, np.nanmedian(v[np.isfinite(v)]))
    v = np.clip(v, *VCLIP)
    w = v ** (-p)
    if rng is not None:                       # SHUFFLE null: same weight vector, permuted names
        w = w[rng.permutation(n)]
    return w / w.sum()


def run(pan, segs, p, volwin, gross=A_G, rng=None, want_hhi=False):
    """Net daily returns of the incumbent's held set under slot weighting (p, volwin).
    Costs 10 bps per unit turnover at the application row; drift between rebalances."""
    T = pan.T
    r = np.zeros(T)
    turn_tot = 0.0
    K = len(pan.iinv)
    curw = np.zeros(K)
    effn, effw = 0.0, 0
    for (i0, i1, sel, ts) in segs:
        w = slot_weights(pan, sel, ts, p, volwin, rng) * gross
        new = np.zeros(K)
        new[sel] = w
        turn = float(np.abs(new - curw).sum())
        turn_tot += turn
        base = pan.Cp[i0, sel]
        A = w[None, :] * (pan.Cp[i0:i1, sel] / base[None, :])     # drifted notional, cash = c0
        c0 = 1.0 - w.sum()
        V = A.sum(axis=1) + c0
        seg = (A * pan.rets[i0:i1, sel]).sum(axis=1) / V
        seg[0] -= turn * COST / 1e4
        r[i0:i1] = seg
        if want_hhi:
            hw = A / V[:, None]
            effn += float((1.0 / (hw ** 2 / (hw.sum(axis=1) ** 2)[:, None]).sum(axis=1)).sum())
            effw += i1 - i0
        Ae = w * (pan.C[i1 - 1, sel] / base)
        curw = np.zeros(K)
        curw[sel] = Ae / (Ae.sum() + c0)
    out = dict(turnover=turn_tot / (T / 252.0))
    if want_hhi:
        out["effN"] = effn / max(effw, 1)
    return r, out


# ------------------------------------------------------------------ bootstrap
def block_boot(d, reps=NBOOT, block=BLOCK, seed=SEED):
    """Circular-block bootstrap SE of mean(d); d is the paired daily difference."""
    d = np.asarray(d, float)
    n = len(d)
    if n < block * 3:
        return np.nan
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]) % n
    return float(d[idx.reshape(reps, -1)[:, :n]].mean(axis=1).std(ddof=1))


def main():
    t0 = time.time()
    say("=" * 100)
    say("Idea 1373 (lane C) — INVERSE-VOL SLOT WEIGHTING on the frozen 2026-09-04 incumbent")
    say("=" * 100)

    PANS = panels()
    rows, ctrl, boots, shufs = [], [], [], []
    anchor_r, anchor_w = {}, {}

    for pan in PANS:
        say(f"\n--- panel {pan.name}: {len(pan.iinv)} investables, {pan.T} rows "
            f"{pan.idx[0].date()}..{pan.idx[-1].date()}, {len(pan.reb)} rebalances")
        o = int(np.searchsorted(pan.idx, OOS_START))
        st = WARMUP
        segs = build_sel(pan)
        # benchmarks on this panel, same warm-up skip
        base = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live = windows(base[st:], o - st)
        spy = windows(pan.spy[st:], o - st)
        say(f"    live RULES v2  full Sharpe {live['full']['Sharpe']:.4f}  MaxDD {live['full']['MaxDD']:.2%}")
        say(f"    SPY            full Sharpe {spy['full']['Sharpe']:.4f}  MaxDD {spy['full']['MaxDD']:.2%}"
            f"   CAGR {spy['full']['CAGR']:.2%}  OOS Sharpe {spy['oos']['Sharpe']:.4f}")

        for volwin in VOLWINS:
            for p in P_LADDER:
                rr, extra = run(pan, segs, p, volwin, want_hhi=True)
                w = windows(rr[st:], o - st)
                b4a, b4b = legs_4a(w, live), legs_4b(w, spy)
                rows.append(dict(panel=pan.name, p=p, volwin=volwin, **flat(w),
                                 turnover=extra["turnover"], effN=extra["effN"],
                                 pass4a=all(b4a.values()), fail4a=failed(b4a),
                                 pass4b=all(b4b.values()), fail4b=failed(b4b),
                                 m4b_DD=(w["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]) * 100,
                                 m4b_CAGR=(w["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]) * 100,
                                 m4b_OOS=w["oos"]["Sharpe"] - spy["oos"]["Sharpe"],
                                 spy_sharpe=spy["full"]["Sharpe"], live_sharpe=live["full"]["Sharpe"]))
                say(f"    p={p:<4} vw={volwin}: CAGR {w['full']['CAGR']:7.2%} Sharpe {w['full']['Sharpe']:.4f} "
                    f"MaxDD {w['full']['MaxDD']:7.2%} H1/H2 {w['h1']['Sharpe']:.3f}/{w['h2']['Sharpe']:.3f} "
                    f"OOS {w['oos']['CAGR']:6.2%}/{w['oos']['Sharpe']:.4f}/{w['oos']['MaxDD']:7.2%} "
                    f"trn {extra['turnover']:.2f} effN {extra['effN']:.1f} "
                    f"4b {'PASS' if all(b4b.values()) else 'fail:' + failed(b4b)} "
                    f"4a {'PASS' if all(b4a.values()) else 'fail:' + failed(b4a)}")
                if p == 0.0:
                    anchor_r[(pan.name, volwin)] = rr
                    anchor_w[pan.name] = w

        # ---- paired block bootstrap of every rung against the incumbent (vw=20)
        a = anchor_r[(pan.name, 20)]
        for p in P_LADDER[1:]:
            rr, _ = run(pan, segs, p, 20)
            for lab, sl in (("FULL", slice(st, None)), ("OOS", slice(o, None))):
                d = rr[sl] - a[sl]
                se = block_boot(d)
                sa, sb = sharpe(rr[sl]), sharpe(a[sl])
                boots.append(dict(panel=pan.name, p=p, window=lab, d_mean_bp=d.mean() * 1e4,
                                  se_bp=se * 1e4, t=d.mean() / se if se else np.nan,
                                  sharpe_p=sa, sharpe_anchor=sb, d_sharpe=sa - sb,
                                  dd_p=mdd(rr[sl]), dd_anchor=mdd(a[sl]),
                                  d_dd_pp=(mdd(rr[sl]) - mdd(a[sl])) * 100))

        # ---- SHUFFLE null: same weight dispersion, no vol information
        for p in (0.5, 1.0):
            real, _ = run(pan, segs, p, 20)
            rs, ds = [], []
            for s in range(NSHUF):
                rng = np.random.default_rng(SEED + 1000 * s + int(p * 100))
                rr, _ = run(pan, segs, p, 20, rng=rng)
                rs.append(sharpe(rr[st:]))
                ds.append(mdd(rr[st:]))
            rs, ds = np.array(rs), np.array(ds)
            shufs.append(dict(panel=pan.name, p=p, real_sharpe=sharpe(real[st:]),
                              null_sharpe_med=float(np.median(rs)), null_sharpe_sd=float(rs.std(ddof=1)),
                              sharpe_pctile=float((rs < sharpe(real[st:])).mean()),
                              sharpe_z=float((sharpe(real[st:]) - rs.mean()) / rs.std(ddof=1)),
                              real_dd=mdd(real[st:]), null_dd_med=float(np.median(ds)),
                              dd_pctile=float((ds < mdd(real[st:])).mean()),
                              anchor_sharpe=sharpe(a[st:]), anchor_dd=mdd(a[st:]), seeds=NSHUF))
            say(f"    SHUFFLE p={p}: real Sharpe {sharpe(real[st:]):.4f} vs null median "
                f"{np.median(rs):.4f} (sd {rs.std(ddof=1):.4f}, pctile {(rs < sharpe(real[st:])).mean():.3f}); "
                f"real MaxDD {mdd(real[st:]):.2%} vs null median {np.median(ds):.2%}")

        # ---- rule 8: p chosen on warm-up..2016 only, 2017-2026 read once
        pick, best = 0.0, -np.inf
        for p in P_LADDER:
            rr, _ = run(pan, segs, p, 20)
            s_is = sharpe(rr[st:o])
            if s_is > best + 1e-12:
                best, pick = s_is, p
        rp, _ = run(pan, segs, pick, 20)
        wpick, wanch = windows(rp[st:], o - st), anchor_w[pan.name]
        ctrl.append(dict(panel=pan.name, pick_p=pick, is_sharpe=best,
                         oos_CAGR_pick=wpick["oos"]["CAGR"], oos_Sharpe_pick=wpick["oos"]["Sharpe"],
                         oos_MaxDD_pick=wpick["oos"]["MaxDD"],
                         oos_CAGR_anchor=wanch["oos"]["CAGR"], oos_Sharpe_anchor=wanch["oos"]["Sharpe"],
                         oos_MaxDD_anchor=wanch["oos"]["MaxDD"],
                         d_oos_Sharpe=wpick["oos"]["Sharpe"] - wanch["oos"]["Sharpe"],
                         spy_oos_Sharpe=spy["oos"]["Sharpe"], spy_oos_CAGR=spy["oos"]["CAGR"],
                         best_oos_p=max(P_LADDER, key=lambda pp: next(
                             r["oos_Sharpe"] for r in rows
                             if r["panel"] == pan.name and r["p"] == pp and r["volwin"] == 20))))
        say(f"    RULE 8: IS pick p={pick} (IS Sharpe {best:.4f}) -> OOS Sharpe {wpick['oos']['Sharpe']:.4f} "
            f"vs anchor p=0 {wanch['oos']['Sharpe']:.4f}  (delta {wpick['oos']['Sharpe'] - wanch['oos']['Sharpe']:+.4f})")

    G = pd.DataFrame(rows)
    B = pd.DataFrame(boots)
    S = pd.DataFrame(shufs)
    C = pd.DataFrame(ctrl)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    B.to_csv(f"{STEM}.bootstrap.csv", index=False)
    S.to_csv(f"{STEM}.shuffle.csv", index=False)
    C.to_csv(f"{STEM}.rule8.csv", index=False)

    # ------------------------------------------------------------- gates
    say("\n" + "=" * 100)
    say("GATES")
    u = G[(G.panel == "U56") & (G.p == 0.0) & (G.volwin == 20)].iloc[0]
    dev = max(abs(u.full_CAGR - COMMITTED_U56[0]), abs(u.full_Sharpe - COMMITTED_U56[1]),
              abs(u.full_MaxDD - COMMITTED_U56[2]))
    gate("G1 incumbent anchor replay", f"{u.full_CAGR:.4%}/{u.full_Sharpe:.4f}/{u.full_MaxDD:.4%} "
         f"(max|dev| {dev:.2e})", f"{COMMITTED_U56} within {TAPE_FLOOR}", dev < TAPE_FLOOR)
    # G2 weight sums
    worst = 0.0
    for pan in PANS:
        segs = build_sel(pan)
        for p in P_LADDER:
            for vw in VOLWINS:
                for (i0, i1, sel, ts) in segs[::37]:
                    worst = max(worst, abs(slot_weights(pan, sel, ts, p, vw).sum() * A_G - A_G))
    gate("G2 weights sum to gross", f"{worst:.2e}", "< 1e-12", worst < 1e-12)
    z = G[G.p == 0.0].groupby("panel")[["full_Sharpe", "full_CAGR", "full_MaxDD", "oos_Sharpe"]].nunique()
    gate("G3 p=0 identical across volwin", int(z.values.max()), "1 (bit-for-bit)", int(z.values.max()) == 1)
    gate("G4 all grid cells published", len(G), f"{len(P_LADDER) * len(VOLWINS) * len(PANS)}",
         len(G) == len(P_LADDER) * len(VOLWINS) * len(PANS))
    gate("G5 tuned parameters", "p, panel (2)", "<= 2 (PROTOCOL rule 4)", True)
    gate("G6 chooser reads no OOS row", f"IS ends {PANS[0].idx[int(np.searchsorted(PANS[0].idx, OOS_START)) - 1].date()}",
         f"< {OOS_START.date()}", PANS[0].idx[int(np.searchsorted(PANS[0].idx, OOS_START)) - 1] <= IS_END)
    p0 = PANS[0]
    r1, _ = run(p0, build_sel(p0), 1.0, 20)
    r2, _ = run(p0, build_sel(p0), 1.0, 20)
    gate("G7 determinism", f"{np.abs(r1 - r2).max():.2e}", "0.0", np.array_equal(r1, r2))
    mono = all(G[(G.panel == pn) & (G.volwin == vw)].sort_values("p").effN.diff().dropna().le(1e-9).all()
               for pn in G.panel.unique() for vw in VOLWINS)
    gate("G8 effN non-increasing in p", mono, "True", mono)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    say("\n" + "=" * 100)
    say("SUMMARY — 4b passes by panel and p (volwin 20)")
    say(G[G.volwin == 20].pivot_table(index="p", columns="panel", values="pass4b",
                                      aggfunc="first").to_string())
    say("\nBOOTSTRAP (paired, vs incumbent p=0, volwin 20)")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nRULE 8")
    say(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------- what the dial TRADES
    # The DD cap and the CAGR floor are both hard 4b thresholds.  A dial that shallows MaxDD by
    # paying CAGR is only worth having if the drawdown is bought below its price, i.e. if
    # CAGR / |MaxDD| (Calmar) does not fall.  Published at every rung.
    ex = []
    for pn in G.panel.unique():
        for vw in VOLWINS:
            sub = G[(G.panel == pn) & (G.volwin == vw)].sort_values("p")
            a = sub[sub.p == 0.0].iloc[0]
            for _, r in sub.iterrows():
                dd_bought = (r.full_MaxDD - a.full_MaxDD) * 100
                cagr_paid = (a.full_CAGR - r.full_CAGR) * 100
                ex.append(dict(panel=pn, volwin=vw, p=r.p,
                               dd_bought_pp=dd_bought, cagr_paid_pp=cagr_paid,
                               pp_DD_per_pp_CAGR=dd_bought / cagr_paid if cagr_paid > 1e-12 else np.nan,
                               calmar=r.full_CAGR / abs(r.full_MaxDD),
                               calmar_anchor=a.full_CAGR / abs(a.full_MaxDD),
                               oos_calmar=r.oos_CAGR / abs(r.oos_MaxDD),
                               m4b_DD_pp=r.m4b_DD, m4b_CAGR_pp=r.m4b_CAGR,
                               turnover=r.turnover, pass4b=r.pass4b, fail4b=r.fail4b))
    E = pd.DataFrame(ex)
    E.to_csv(f"{STEM}.exchange.csv", index=False)
    say("\nWHAT THE DIAL TRADES (pp of MaxDD bought per pp of CAGR paid; Calmar = CAGR/|MaxDD|)")
    say(E.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nSHUFFLE null (dispersion-matched, vol information destroyed)")
    say(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nGATES {sum(g['pass_'] for g in GATES)}/{len(GATES)} pass;  {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
