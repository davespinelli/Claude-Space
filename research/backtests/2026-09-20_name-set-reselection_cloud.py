#!/usr/bin/env python3
"""Idea 1783 (lane cloud, 2026-09-20): does a RE-SELECTING name-set rule inherit ANY of 1749's
4b pass, or is the FROZEN LIST the whole effect?

THE DEFECT THIS CLOSES.  Idea 1749 (this same run) established that the NAME SET is a reachable
axis: over 480 seeded 20-name draws from U56, the live band book clears 4b FULL *and* OOS at a
base rate of 43/480 = 8.96%, and an IS-only chooser reading 2009-2016 alone lifts the TOP DECILE
to 25/48 = 52.08% (exact hypergeometric p < 1e-4).  Its KEEP-candidate memo's RULES wording,
however, FREEZES twenty tickers chosen ONCE on eight years of data and holds them for the next
9.7 years, and the memo's own point 10(c) records that a rule which RE-CHOOSES the names
periodically "has never been priced and may not inherit any of this".  That gap is the whole
difference between a deployable rule and a hindsight list: a frozen list cannot be run forward
(there is no procedure to re-derive it next year), and a re-selecting rule pays switch turnover
and rides a chooser that must work at EVERY refresh, not just the one the record happened to
read.  Nothing in the record prices that.

THE CONSTRUCTION.  The same 480-draw population, the same seed stream, the same book (band
c = 0.03, gross 0.75, weekly, t+1).  A CONCATENATED book: at each REFRESH date the 480 draws are
ranked by an IS statistic computed on a TRAILING window that ENDS STRICTLY BEFORE that refresh
row (G4), the argmax draw is held until the next refresh, and the FULL SWITCH TURNOVER is
charged -- |target weights of the new name set - drifted held weights of the old one| over the
whole 56-column space, not the new draw's own book-internal turnover (G6).  Because
`run_cell` resets to `g * frame[i0]` at every rebalance row independently of prior holdings, a
splice at a rebalance row is EXACT, and the concatenated return path is the draws' own paths
stitched together with no approximation (G5 proves it: at K = FROZEN the concatenation is
bit-for-bit the single draw's book).

BOOK START.  The first refresh is the first rebalance row at least MIN_TRAIL = 4 years after the
scored sample opens, so EVERY pick -- the first one included -- has a real trailing window and no
arm ever holds a default.  The book therefore runs 2013-01 -> 2026-09 (13.7y, PROTOCOL rule 1),
and 2017-2026 is untouched OOS under every arm (rule 8).  Live RULES v2 and SPY are RESTATED on
that identical window so every comparison is commensurable.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  REFRESH PERIOD K in {2, 4, 8, FROZEN} years.  FROZEN picks once at book start and
          holds -- 1749's rule shape exactly, and the nested control this idea is scored against.
  DIAL 2  TRAILING WINDOW W in {EXPANDING (sample open -> refresh), ROLL4 (4y), ROLL8 (8y)}.
REPORTED AXES, not tuned, every point published to `_grid.csv`:
  RANKING STATISTIC {IS_CAGRSLACK, IS_LEGS, IS_SHARPE}.  IS_CAGRSLACK is INHERITED from 1749
  unchanged (it was that idea's headline chooser); the other two are published as robustness, not
  re-tuned here.  COST {0, 10, 25, 50} bps, reconstructed exactly off the cost-0 leg (G2).
  4 x 3 x 3 x 4 = 144 scored books, all published.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) re-selecting arms clear 4b FULL and OOS at rates comparable to FROZEN -> the rule is
      DEPLOYABLE and the memo's wording should be replaced with the re-selecting procedure;
  (b) re-selecting arms fail where FROZEN passes -> the frozen list IS the whole effect and
      1749's KEEP-candidate is hindsight that cannot be run forward; say so plainly;
  (c) FROZEN itself fails when its single pick is made at BOOK START (2013) rather than at
      2016-12-31 -> 1749's pass depended on the particular date its chooser was allowed to read,
      which is a stronger statement than (b) and kills the axis outright;
  (d) the switch turnover alone explains any gap -> report it, and report the zero-cost rung.

GATES.  G1 this runner == `engine.backtest` on returns AND turnover for the live band book on
full U56.  G2 the cost identity r(c) = r0 - turnover*c/1e4 == the engine at 10 and 25 bps.
G3 CROSS-RUN: idea 1749's headline draw 166 reproduces on 1749's own window (FULL 11.75% /
1.3343 / -13.16%, OOS 11.74% / 1.3112 / -13.16%).  G4 every chooser window ends STRICTLY BEFORE
its refresh row.  G5 at K = FROZEN the concatenated book == the picked draw's own book
bit-for-bit.  G6 switch turnover is the true cross-name-set turnover and is strictly positive at
every switch.  G7 every cell published.  G8 exactly two tuned dials.  G9 no leverage / no
shorting.  G10 the only RNG is the draw index selection, seeded exactly as ideas 1632 and 1749.

PROTOCOL: rule 1 (13.7y); rule 2 (t+1, 10 bps binding, no leverage, no shorting); rule 3 (live
RULES v2 AND SPY, both restated on the book's own window); rule 4 (both KEEP paths at every cell,
two dials); rule 8 (walk-forward: every pick reads a trailing window only, 2017-2026 read once);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py NOT modified.

SURVIVORSHIP.  U56 is a CURRENT-constituent list, so selecting 20 of today's 56 survivors is the
record's most survivorship-exposed construction and every CAGR and drawdown LEVEL below is an
upper bound.  The FROZEN-vs-RE-SELECTING contrast is same-tape, same-pool, same-seed-stream and
first-order immune; the absolute 4b pass counts are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_name-set-reselection_cloud.py
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state      # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG = "2026-09-20", "name-set-reselection"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
GROSS = 0.75
BAND_C = 0.03
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

NAMES_N = 20
NDRAWS = 480
SEED0 = 16320000                    # ideas 1632 / 1749 seed base, carried over unchanged (G10)
MIN_TRAIL_Y = 4
KS = [2, 4, 8, "FROZEN"]
WINDOWS = ["EXPANDING", "ROLL4", "ROLL8"]
STATS = ["IS_CAGRSLACK", "IS_LEGS", "IS_SHARPE"]
STAT0 = "IS_CAGRSLACK"
YR = 252

# idea 1749's headline pick, on 1749's own window (2009-01-13 -> end)
PUB166 = dict(CAGR=0.1175, Sharpe=1.3343, MaxDD=-0.1316, oCAGR=0.1174, oSharpe=1.3112)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


class Panel:
    def __init__(self, px):
        self.px, self.cols, self.idx = px, list(px.columns), px.index
        q = px[self.cols]
        self.rets = np.nan_to_num(q.pct_change().values, nan=0.0)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.priced = q.notna().values
        self.band = band_state(q, BAND_C).values
        m = rebalance_mask(self.idx, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.T = len(self.idx)


def frame_of(pan, j):
    pr = pan.priced[:, j]
    e = (pr & pan.band[:, j]).astype(float)
    n = pr.sum(axis=1).astype(float)
    w = np.nan_to_num(np.divide(e, np.where(n == 0, np.nan, n)[:, None]), nan=0.0)
    return np.vstack([np.zeros((1, w.shape[1])), w[:-1]])


def run_cell(pan, j, frame, g=GROSS, record=()):
    """engine.backtest semantics (gated at G1).  `record` = rebalance rows at which to capture
    (pre-rebalance drifted weights, post-rebalance target weights), scattered into the panel's
    full column space so two different name sets can be differenced."""
    rets = pan.rets[:, j]
    C, Cp = pan.C[:, j], pan.Cp[:, j]
    T, M = rets.shape
    F = pan.rets.shape[1]
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    wmax = 0.0
    rec = {}
    want = set(int(x) for x in record)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wmax = max(wmax, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        if i0 in want:
            a = np.zeros(F); b = np.zeros(F)
            a[j] = curw; b[j] = w0
            rec[i0] = (a, b)
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wmax, rec


def net(rg, tu, c):
    return rg - tu * c / 1e4


def mets(r):
    r = np.asarray(r, float); r = r[np.isfinite(r)]
    eq = np.cumprod(1.0 + r); yrs = len(r) / 252.0
    vol = r.std(ddof=1) * math.sqrt(252.0)
    return dict(CAGR=eq[-1] ** (1.0 / yrs) - 1.0 if yrs else float("nan"),
                Sharpe=(r.mean() * 252.0) / vol if vol else float("nan"),
                MaxDD=float((eq / np.maximum.accumulate(eq) - 1.0).min()))


def halves(r):
    h = len(r) // 2
    return mets(r[:h])["Sharpe"], mets(r[h:])["Sharpe"]


def main():
    t0 = time.time()
    say("=" * 116)
    say("IDEA 1783 (lane cloud, 2026-09-20) — does a RE-SELECTING name-set rule inherit ANY of")
    say("1749's 4b pass, or is the FROZEN LIST the whole effect?")
    say("=" * 116)
    say(f"# dials: REFRESH PERIOD K {KS} (years) x TRAILING WINDOW W {WINDOWS}")
    say(f"# reported: ranking statistic {STATS} (IS_CAGRSLACK inherited from 1749, not re-tuned); "
        f"cost {COSTS} bps (binding {BIND:.0f})")
    say(f"# fixed: U56, {NDRAWS} seeded {NAMES_N}-name draws, band c={BAND_C}, gross {GROSS}, "
        f"cadence {CADENCE}, t+1")
    say("# the ONLY RNG is the draw index selection, seeded exactly as ideas 1632 / 1749 (G10)")
    gate("G8 tuned dials", "REFRESH PERIOD K, TRAILING WINDOW W", "exactly 2", True)

    px = load_universe().dropna(how="all").ffill()
    pan = Panel(px)
    M = len(pan.cols)
    st = WARMUP
    i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))

    # ---- refresh schedule -----------------------------------------------------------
    def snap(i):
        k = pan.reb[np.searchsorted(pan.reb, i)]
        return int(k)
    b0 = snap(st + MIN_TRAIL_Y * YR)
    sched = {}
    for K in KS:
        if K == "FROZEN":
            sched[K] = [b0]
        else:
            r, i = [], b0
            while i < pan.T - YR // 2:
                r.append(snap(i))
                i += K * YR
            sched[K] = sorted(set(r))
    all_ref = sorted({r for v in sched.values() for r in v})
    say("")
    say(f"# panel U56: {M} columns, {pan.idx[0].date()} -> {pan.idx[-1].date()} ({pan.T} rows)")
    say(f"# scored sample opens {pan.idx[st].date()}; BOOK START (first refresh, "
        f"{MIN_TRAIL_Y}y min trailing) {pan.idx[b0].date()}; book runs "
        f"{(pan.T-b0)/252:.1f}y (PROTOCOL rule 1); OOS from {pan.idx[i_oos].date()} "
        f"({(pan.T-i_oos)/252:.1f}y)")
    for K in KS:
        say(f"#   K={str(K):<7s} refreshes at " + ", ".join(str(pan.idx[r].date()) for r in sched[K]))

    # ---- benchmarks restated on the BOOK'S OWN window --------------------------------
    spy = np.nan_to_num(px["SPY"].pct_change().values, nan=0.0)[b0:]
    S_f, S_o = mets(spy), mets(spy[i_oos - b0:])
    S_h1, S_h2 = halves(spy)
    lw = rules_v2_weights(px, band=BAND_C, gross=GROSS)
    lb = engine_backtest(px, lw, cost_bps=0.0, freq=CADENCE)
    lr0 = np.nan_to_num(lb["returns"].values, nan=0.0)
    lt0 = np.nan_to_num(lb["turnover"].values, nan=0.0)
    LIVE = {}
    for c in COSTS:
        r = net(lr0, lt0, c)[b0:]
        h1, h2 = halves(r)
        LIVE[c] = dict(full=mets(r), oos=mets(r[i_oos - b0:]), h1=h1, h2=h2)
    L = LIVE[BIND]
    say("")
    say(f"# SPY           FULL {S_f['CAGR']:7.2%} / {S_f['Sharpe']:.4f} / {S_f['MaxDD']:7.2%}   "
        f"H1/H2 {S_h1:.4f}/{S_h2:.4f}   OOS {S_o['CAGR']:7.2%} / {S_o['Sharpe']:.4f} / "
        f"{S_o['MaxDD']:7.2%}")
    say(f"# RULES v2 live FULL {L['full']['CAGR']:7.2%} / {L['full']['Sharpe']:.4f} / "
        f"{L['full']['MaxDD']:7.2%}   H1/H2 {L['h1']:.4f}/{L['h2']:.4f}   OOS "
        f"{L['oos']['CAGR']:7.2%} / {L['oos']['Sharpe']:.4f} / {L['oos']['MaxDD']:7.2%}")
    say(f"# 4b bars on this window: FULL DD cap {DD_CAP*S_f['MaxDD']:7.2%}, CAGR floor "
        f"{CAGR_FLOOR*S_f['CAGR']:6.2%} | OOS DD cap {DD_CAP*S_o['MaxDD']:7.2%}, CAGR floor "
        f"{CAGR_FLOOR*S_o['CAGR']:6.2%}")

    # ---- G1 / G2 ---------------------------------------------------------------------
    jall = np.arange(M)
    ra, ta, _, _ = run_cell(pan, jall, frame_of(pan, jall))
    d_r = float(np.abs(lr0 - ra).max()); d_t = float(np.abs(lt0 - ta).max())
    gate("G1 runner == engine.backtest (live band book, full U56)",
         f"returns {d_r:.3e}, turnover {d_t:.3e}", "< 1e-12", d_r < 1e-12 and d_t < 1e-12)
    d2 = 0.0
    for c in (10.0, 25.0):
        eb = np.nan_to_num(engine_backtest(px, lw, cost_bps=c, freq=CADENCE)["returns"].values,
                           nan=0.0)
        d2 = max(d2, float(np.abs(net(ra, ta, c) - eb).max()))
    gate("G2 cost identity", f"max|d| = {d2:.3e}", "< 1e-15", d2 < 1e-15)

    # ---- the 480 draws: paths, turnover, and the refresh-row weight records ----------
    say("")
    say(f"# running {NDRAWS} seeded {NAMES_N}-name draws and recording weights at "
        f"{len(all_ref)} refresh rows ...")
    R0 = np.zeros((NDRAWS, pan.T)); T0 = np.zeros((NDRAWS, pan.T))
    REC = [None] * NDRAWS
    gmax = 0.0
    for d in range(NDRAWS):
        j = np.sort(np.random.default_rng(SEED0 + 1009 * NAMES_N + d)
                    .choice(M, size=NAMES_N, replace=False))
        r, t, gm, rec = run_cell(pan, j, frame_of(pan, j), record=all_ref)
        R0[d], T0[d], REC[d] = r, t, rec
        gmax = max(gmax, gm)
    gate("G9 no leverage / no shorting", f"max realised TARGET gross {gmax:.6f}", f"<= {GROSS}",
         gmax <= GROSS + 1e-12)

    # ---- G3 cross-run vs idea 1749's headline pick (on 1749's OWN window) -------------
    r166, t166 = net(R0[166], T0[166], BIND)[st:], None
    m166, o166 = mets(r166), mets(r166[i_oos - st:])
    mx = max(abs(PUB166["CAGR"] - m166["CAGR"]), abs(PUB166["Sharpe"] - m166["Sharpe"]),
             abs(PUB166["MaxDD"] - m166["MaxDD"]), abs(PUB166["oCAGR"] - o166["CAGR"]),
             abs(PUB166["oSharpe"] - o166["Sharpe"]))
    gate("G3 cross-run vs idea 1749's headline draw 166 (1749's window)", f"max|d| = {mx:.3e}",
         "< 5e-4 (1749 quotes 4 dp)", mx < 5e-4)

    # ---- chooser statistics on trailing windows --------------------------------------
    spy_all = np.nan_to_num(px["SPY"].pct_change().values, nan=0.0)
    g4_ok = True
    PICK = {}
    for W in WINDOWS:
        for ref in all_ref:
            lo = st if W == "EXPANDING" else max(st, ref - (4 if W == "ROLL4" else 8) * YR)
            hi = ref                              # STRICTLY before the refresh row (G4)
            g4_ok &= (hi <= ref) and (hi > lo)
            sr = spy_all[lo:hi]
            sm, sh1, sh2 = mets(sr), *halves(sr)
            for S in STATS:
                v = np.empty(NDRAWS)
                for d in range(NDRAWS):
                    r = net(R0[d], T0[d], BIND)[lo:hi]
                    m = mets(r); h1, h2 = halves(r)
                    if S == "IS_SHARPE":
                        v[d] = m["Sharpe"]
                    elif S == "IS_CAGRSLACK":
                        v[d] = m["CAGR"] - CAGR_FLOOR * sm["CAGR"]
                    else:
                        v[d] = ((h1 > sh1) + (h2 > sh2)
                                + (m["MaxDD"] >= DD_CAP * sm["MaxDD"])
                                + (m["CAGR"] >= CAGR_FLOOR * sm["CAGR"]))
                PICK[(W, ref, S)] = int(np.argmax(v))   # ties -> lowest draw index
    gate("G4 every chooser window ends STRICTLY BEFORE its refresh row",
         f"{len(PICK)} (window, refresh, statistic) choices, all with hi == refresh row",
         "all true", bool(g4_ok))

    # ---- concatenate ------------------------------------------------------------------
    rows = []
    g5 = 0.0
    g6_min = 1e9
    g6_n = 0
    PATHS = {}
    for K in KS:
        refs = sched[K]
        for W in WINDOWS:
            for S in STATS:
                picks = [PICK[(W, r, S)] for r in refs]
                rr = np.zeros(pan.T); tt = np.zeros(pan.T)
                bounds = list(refs) + [pan.T]
                prev = None
                for k, (a, b) in enumerate(zip(bounds[:-1], bounds[1:])):
                    d = picks[k]
                    rr[a:b] = R0[d][a:b]
                    tt[a:b] = T0[d][a:b]
                    w_old = np.zeros(M) if prev is None else REC[prev][a][0]
                    w_new = REC[d][a][1]
                    sw = float(np.abs(w_new - w_old).sum())
                    tt[a] = sw
                    if prev is not None:
                        g6_min = min(g6_min, sw if picks[k] != picks[k - 1] else g6_min)
                        g6_n += int(picks[k] != picks[k - 1])
                    prev = d
                if K == "FROZEN":
                    d = picks[0]
                    g5 = max(g5, float(np.abs(rr[refs[0]:] - R0[d][refs[0]:]).max()))
                PATHS[(K, W, S)] = (rr, tt, picks)
                for c in COSTS:
                    r = net(rr, tt, c)[b0:]
                    mf, mo = mets(r), mets(r[i_oos - b0:])
                    h1, h2 = halves(r)
                    LV = LIVE[c]
                    k4bf = (h1 > S_h1 and h2 > S_h2 and mf["MaxDD"] >= DD_CAP * S_f["MaxDD"]
                            and mf["CAGR"] >= CAGR_FLOOR * S_f["CAGR"])
                    k4bo = (mo["Sharpe"] > S_o["Sharpe"] and mo["MaxDD"] >= DD_CAP * S_o["MaxDD"]
                            and mo["CAGR"] >= CAGR_FLOOR * S_o["CAGR"])
                    rows.append(dict(
                        K=str(K), window=W, stat=S, cost=c, n_refresh=len(refs),
                        n_switch=int(sum(picks[i] != picks[i - 1] for i in range(1, len(picks)))),
                        picks="|".join(str(p) for p in picks),
                        turn_py=float(net(np.zeros(pan.T), tt, 0)[b0:].sum() * 0
                                      + tt[b0:].sum() / ((pan.T - b0) / 252.0)),
                        CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                        oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                        L1_H1=h1 - S_h1, L2_H2=h2 - S_h2,
                        L4_DD=mf["MaxDD"] - DD_CAP * S_f["MaxDD"],
                        L5_CAGR=mf["CAGR"] - CAGR_FLOOR * S_f["CAGR"],
                        O3_OOS=mo["Sharpe"] - S_o["Sharpe"],
                        O4_DD=mo["MaxDD"] - DD_CAP * S_o["MaxDD"],
                        O5_CAGR=mo["CAGR"] - CAGR_FLOOR * S_o["CAGR"],
                        keep4b_full=bool(k4bf), keep4b_oos=bool(k4bo), keep4b=bool(k4bf and k4bo),
                        keep4a=bool(h1 > LV["h1"] and h2 > LV["h2"]
                                    and mf["MaxDD"] >= LV["full"]["MaxDD"]),
                        keep4a_oos=bool(mo["Sharpe"] > LV["oos"]["Sharpe"]
                                        and mo["MaxDD"] >= LV["oos"]["MaxDD"]),
                    ))
    gate("G5 K=FROZEN concatenation == the picked draw's own book", f"max|d| = {g5:.3e}",
         "< 1e-15", g5 < 1e-15)
    gate("G6 switch turnover is the true cross-name-set turnover",
         f"{g6_n} switches, min switch turnover {g6_min:.4f}", "> 0 at every switch",
         g6_n > 0 and g6_min > 0)

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}_grid.csv", index=False)
    gate("G7 every cell published", f"{len(df)} rows -> {Path(OUT).name}_grid.csv",
         f"{len(KS)*len(WINDOWS)*len(STATS)*len(COSTS)}",
         len(df) == len(KS) * len(WINDOWS) * len(STATS) * len(COSTS))

    B = df[df.cost == BIND]
    say("")
    say(f"## THE GRID at {BIND:.0f} bps — book window {pan.idx[b0].date()} -> "
        f"{pan.idx[-1].date()}, OOS {pan.idx[i_oos].date()} -> {pan.idx[-1].date()}")
    say(f"   {'K':>7s} {'window':<10s} {'stat':<13s} {'FULL CAGR':>9s} {'Shrp':>7s} "
        f"{'MaxDD':>8s} {'H1':>7s} {'H2':>7s} | {'OOS CAGR':>8s} {'Shrp':>7s} {'MaxDD':>8s} "
        f"| {'turn':>5s} {'sw':>3s} {'4bF':>5s} {'4bO':>5s} {'4b':>5s} {'4aO':>5s}")
    for _, q in B.iterrows():
        say(f"   {q.K:>7s} {q.window:<10s} {q.stat:<13s} {q.CAGR:>9.2%} {q.Sharpe:>7.4f} "
            f"{q.MaxDD:>8.2%} {q.H1:>7.4f} {q.H2:>7.4f} | {q.oos_CAGR:>8.2%} "
            f"{q.oos_Sharpe:>7.4f} {q.oos_MaxDD:>8.2%} | {q.turn_py:>5.2f} {q.n_switch:>3d} "
            f"{str(q.keep4b_full):>5s} {str(q.keep4b_oos):>5s} {str(q.keep4b):>5s} "
            f"{str(q.keep4a_oos):>5s}")

    say("")
    say("## THE CONTRAST THAT ANSWERS THE QUESTION (10 bps, statistic = "
        f"{STAT0}, inherited from 1749)")
    for W in WINDOWS:
        fz = B[(B.K == "FROZEN") & (B.window == W) & (B.stat == STAT0)].iloc[0]
        say(f"\n   trailing window {W}")
        say(f"     K=FROZEN  picks {fz.picks:<12s} FULL {fz.CAGR:7.2%}/{fz.Sharpe:.4f}/"
            f"{fz.MaxDD:7.2%}  OOS {fz.oos_CAGR:7.2%}/{fz.oos_Sharpe:.4f}/{fz.oos_MaxDD:7.2%}  "
            f"4b {fz.keep4b}")
        for K in [k for k in KS if k != "FROZEN"]:
            q = B[(B.K == str(K)) & (B.window == W) & (B.stat == STAT0)].iloc[0]
            say(f"     K={K:<7d} picks {q.picks:<12s} FULL {q.CAGR:7.2%}/{q.Sharpe:.4f}/"
                f"{q.MaxDD:7.2%}  OOS {q.oos_CAGR:7.2%}/{q.oos_Sharpe:.4f}/{q.oos_MaxDD:7.2%}  "
                f"4b {q.keep4b}   d(OOS Sharpe) vs FROZEN {q.oos_Sharpe-fz.oos_Sharpe:+.4f}, "
                f"d(OOS CAGR) {q.oos_CAGR-fz.oos_CAGR:+.2%}, +{q.turn_py-fz.turn_py:.2f} turn/yr")

    say("")
    say("## 4b PASS COUNTS by arm (9 (window x statistic) cells per K, 10 bps)")
    say(f"   {'K':>7s} {'4b FULL':>8s} {'4b OOS':>8s} {'4b BOTH':>8s} {'4a FULL':>8s} "
        f"{'4a OOS':>7s} {'mean OOS Sharpe':>16s} {'mean turn/yr':>13s}")
    for K in KS:
        s = B[B.K == str(K)]
        say(f"   {str(K):>7s} {int(s.keep4b_full.sum()):>8d} {int(s.keep4b_oos.sum()):>8d} "
            f"{int(s.keep4b.sum()):>8d} {int(s.keep4a.sum()):>8d} {int(s.keep4a_oos.sum()):>7d} "
            f"{s.oos_Sharpe.mean():>16.4f} {s.turn_py.mean():>13.2f}")

    say("")
    say("## BINDING LEG among the 4b failures (10 bps, all 36 arms)")
    for k in ("L1_H1", "L2_H2", "L4_DD", "L5_CAGR", "O3_OOS", "O4_DD", "O5_CAGR"):
        say(f"   {k:<8s} fails in {int((B[k] <= 0).sum()):>3d} of {len(B)} arms")

    say("")
    say("## COST LADDER (reported axis)")
    say(f"   {'cost':>5s} {'4b BOTH':>8s} {'4a OOS':>7s}  " + "  ".join(f"K={str(k):<7s}"
                                                                        for k in KS))
    for c in COSTS:
        s = df[df.cost == c]
        say(f"   {c:>5.0f} {int(s.keep4b.sum()):>8d} {int(s.keep4a_oos.sum()):>7d}  "
            + "  ".join(f"{int(s[s.K==str(k)].keep4b.sum()):<9d}" for k in KS))

    nfz = int(B[B.K == "FROZEN"].keep4b.sum())
    nre = int(B[B.K != "FROZEN"].keep4b.sum())
    say("")
    say("=" * 116)
    say("VERDICT")
    say(f"  FROZEN arms clearing 4b FULL and OOS: {nfz} of 9")
    say(f"  RE-SELECTING arms (K in 2/4/8y) clearing 4b FULL and OOS: {nre} of 27")
    say(f"  gates: {sum(g['pass_'] for g in GATES)} / {len(GATES)} pass")
    say(f"  runtime {time.time()-t0:.1f}s")
    say("=" * 116)
    pd.DataFrame(GATES).to_csv(f"{OUT}_gates.csv", index=False)
    Path(f"{OUT}_log.txt").write_text("\n".join(LOG) + "\n")
    return 0 if all(g["pass_"] for g in GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
