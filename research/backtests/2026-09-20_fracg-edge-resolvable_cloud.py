#!/usr/bin/env python3
"""Idea 2067 (lane cloud, 2026-09-20) — IS THE FRACTION RULE'S CRASH-EXCISED EDGE RESOLVABLE,
or is it a FOUR-ARM POINT ESTIMATE?

THE CLAIM UNDER TEST.  Idea 2026's strongest result is that the LADDER-FREE fraction threshold
`h_t = f * g_t` (FRACG) keeps a POSITIVE turnover-matched-calendar edge on the 2020-crash-EXCISED
tape — mean `x_d_matched_cal` = +0.0377 over its four pre-stated arms (U56/B136 x W/M at
f* = 0.10, t* = 0.16, 10 bps), 4 of 4 positive — where the incumbent CONSTANT threshold
`h = 0.12` (FIXH) goes to -0.0050, 0 of 4.  That is a POINT ESTIMATE on four arms with no
standard error, and idea 2022 found the same matched-calendar sweep resolvable at only 61 of 263
cells.  This run gives the fraction rule's edge the SAME paired moving-block bootstrap and reports
the share of cells whose 95% interval excludes zero.

THE STATISTIC (idea 2026's own construction, re-used verbatim, not re-derived).
    d = Sharpe(book) - Sharpe_matched_cal
where the matched calendar point is a LINEAR interpolation in realised turns/yr along the arm's
own CALENDAR ladder R in {D, W, M, Q} — i.e. with bracketing rungs (A, B) and weight
`w = (tp - tA) / (tB - tA)`,  Sharpe_matched = (1 - w) * Sharpe(A) + w * Sharpe(B).
Under the bootstrap the weight `w` is FROZEN at its full-sample value (it is the turnover match,
not the statistic) and the three return series — book, calendar rung A, calendar rung B — are
resampled on IDENTICAL day blocks, so the difference keeps its pairing.  Clamped cells (book
turnover outside the calendar ladder's range, so `np.interp` pins to an endpoint) are FLAGGED and
reported separately: there the comparand is a single rung and the match is not a match.

TAPES (both, as the idea asks):
    ALL      the whole tape
    XCRASH   2020-02-19 .. 2020-03-23 excised (idea 2022's window, quoted not re-derived)
WINDOWS: OOS (2017-01-01 ..) is the headline — it is the window idea 2026's number is quoted in —
and FULL is reported beside it.

CELLS: panel {U56, B136, SMALL} x trade cadence {W, M} x f {0.02, 0.05, 0.10, 0.15, 0.20, 0.30,
0.50} = 42.  The FIXH incumbent (h = 0.12) and the ASYMG twin are carried at f*/h* as contrast
arms.  Target `t` is FIXED at 0.16 (inherited from the standing memo, not chosen here) and cost at
10 bps for the bootstrap; the 4a/4b census is run at 0/10/25/50 bps.

DIALS.  EXACTLY TWO are tuned, both bootstrap dials, neither a trading dial:
    block length L in {5, 10, 21, 63} trading days   (headline PRE-STATED at 21)
    draws B in {2000, 8000}                          (headline PRE-STATED at 2000; 8000 is a
                                                      draw-count stability read on the headline
                                                      block only)
REPORTED, NOT TUNED: panel, trade cadence, f, cost, tape, window.  The trading book itself has NO
free parameter here: f is laddered and published at every rung, `t` is inherited.

PRE-STATED VERDICT RULES (fixed before the run, never adjusted after):
  V1  RESOLVABLE?  On the XCRASH tape, OOS window, at the headline block L = 21, the share of the
      42 FRACG cells whose 95% paired interval EXCLUDES zero is > 0.50.  Not reached -> the
      +0.0377 is NOT resolvable and is reported as a point estimate, i.e. a KILL of the claim's
      RESOLUTION (not of its sign).
  V2  THE FOUR-ARM CLAIM ITSELF.  Idea 2026's own four pre-stated arms (U56/B136 x W/M, f = 0.10):
      report each arm's interval.  The claim "4 of 4 positive" is certified only if all four
      intervals exclude zero on the same tape and window.
  V3  BLOCK-LADDER STABILITY.  The share in V1 moves by no more than 0.20 across L in
      {5, 10, 21, 63}.  A share that moves more than that is a BLOCK-LENGTH artefact and the
      resolution verdict is reported as unstable.
  V4  FRACG vs FIXH, PAIRED.  The contrast that carries idea 2026's headline is FRACG's edge MINUS
      FIXH's edge on the same tape.  Bootstrap THAT difference directly (same blocks, three legs)
      and report whether it excludes zero.  This is the only test that speaks to "FRACG beats the
      incumbent"; a pair of separately-signed point estimates does not.
  V5  CAPITAL.  Both KEEP paths at EVERY cell against live RULES v2 and SPY, at 0/10/25/50 bps,
      plus the mandatory rule-8 walk-forward (f chosen on 2009-2016 only by four legal IS-only
      choosers, 2017-2026 read once).

PROTOCOL: rule 2 (10 bps headline, weights at close t applied t+1, no leverage, gross <= 1.00);
rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea,
deterministic, standalone); rule 8 (walk-forward); rule 9 (survivorship stated).  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first, per the sprint
brief).  Every CAGR and drawdown LEVEL below is optimistic and both 4b bars are easier here than
on a point-in-time panel.  The bootstrap contrast is same-tape / same-names / same-blocks with
only the refresh trigger moved, so it is first-order immune to that bias; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_fracg-edge-resolvable_cloud.py
"""
from __future__ import annotations

import sys
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG = "2026-09-20", "fracg-edge-resolvable"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TGT_STAR = 0.16                       # inherited from the standing VOLTGT memo; NOT chosen here
F_GRID = [0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50]
F_STAR, H_STAR = 0.10, 0.12
ASYM_A = 4.0
TRADES = ["W", "M"]
REFRESH = ["D", "W", "M", "Q"]
SIG_L, SIG_D = 20, 0
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
CRASH = ("2020-02-19", "2020-03-23")
BLOCKS = [5, 10, 21, 63]
BLOCK0 = 21                           # PRE-STATED headline block
NBOOT = 2000                          # PRE-STATED headline draw count
NBOOT_HI = 8000                       # draw-count stability read, headline block only
SEED = 2067
V1_BAR, V3_BAR = 0.50, 0.20

# idea 2026's committed numbers this run must reproduce (crash.csv, prestated rows)
PUB_2026 = {
    ("U56", "W"):  dict(turn_py=1.9055279766106716, oos_Sharpe=1.2740996241758344,
                        d=0.050877257108415064, xd=0.03737919623069619),
    ("U56", "M"):  dict(turn_py=1.4167103486197432, oos_Sharpe=1.292833538927014,
                        d=0.06534487283345891, xd=0.02773954554406144),
    ("B136", "W"): dict(turn_py=2.0362177961911314, oos_Sharpe=1.2564287059179386,
                        d=0.06471691669087432, xd=0.046956373925351125),
    ("B136", "M"): dict(turn_py=1.5389941108867085, oos_Sharpe=1.2621199700620631,
                        d=0.0781638610302704, xd=0.0387455230517284),
}
PUB_FIXH_XD = {("U56", "W"): -0.005332156368120566, ("U56", "M"): -0.009327408000150417,
               ("B136", "W"): -0.0025927853907199427, ("B136", "M"): -0.00288977035139526}

_log: list[str] = []
_gates: list[dict] = []


def dseed(*parts):
    """Deterministic per-cell seed (zlib.crc32, NOT hash(): PYTHONHASHSEED must not move a
    published number)."""
    return SEED + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 1000000


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ----------------------------------------------------------------------------- panels
def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    dropped = len([c for c in pxs.columns if c in bad])
    return ([("U56", px56, list(px56.columns)),
             ("B136", px136, list(px136.columns)),
             (f"SMALL{len(small_cols)}", pxs, small_cols)], dropped)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------------------ refresh runners (idea 2026)
def bt_cal(px_ret, W0, g0, mT, mR):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        if mR[i] or i == 0:
            g_eff = g0[i]
            nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif mR[i]:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum()
                cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


def bt_var(px_ret, W0, g0, mT, hup, hdn):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        gh = cur.sum()
        trig = (g0[i] - gh > hup[i]) or (gh - g0[i] > hdn[i])
        if trig or i == 0:
            g_eff = g0[i]
            nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif trig:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum()
                cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


class Book:
    def __init__(self, px, cols, index):
        self.index = index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((1, ew.shape[1])), ew[:-1]])       # decided t, applied t+1
        self.SIG = panel_sigma(px, cols)
        self.masks = {}
        for f in ("D", "W", "M", "Q"):
            m = np.asarray(rebalance_mask(index, f).values, bool)
            self.masks[f] = np.concatenate([[False], m[:-1]])
        self._g = {}

    def g_of(self, tgt):
        if tgt not in self._g:
            g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
            self._g[tgt] = np.concatenate([[0.0], g[:-1]])
        return self._g[tgt]

    def run(self, tgt, T, fam, rung):
        g0 = self.g_of(tgt)
        n = len(self.R)
        if fam == "CAL":
            r, t, gs, nref = bt_cal(self.R, self.W, g0, self.masks[T], self.masks[rung])
        else:
            if fam == "FRACG":
                hu = hd = rung * g0
            elif fam == "ASYMG":
                hu, hd = rung * g0, rung * g0 / ASYM_A
            elif fam == "FIXH":
                hu = hd = np.full(n, rung)
            else:
                raise ValueError(fam)
            r, t, gs, nref = bt_var(self.R, self.W, g0, self.masks[T], hu, hd)
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)


# ----------------------------------------------------------------------------- metrics
def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def binding(mar):
    bad = [k for k in LEGS if not (mar[k] > 0)]
    return ("|".join(bad) if bad else "none", len(bad))


def excise(s):
    return s[~((s.index >= CRASH[0]) & (s.index <= CRASH[1]))]


# ------------------------------------------------------------------ vectorised bootstrap
def sharpe_rows(X):
    v = X.std(axis=1, ddof=0) * np.sqrt(252.0)
    out = np.full(X.shape[0], np.nan)
    ok = v > 0
    out[ok] = X[ok].mean(axis=1) * 252.0 / v[ok]
    return out


def block_index(n, L, nboot, rng):
    """Circular block bootstrap index matrix (nboot x n): ceil(n/L) blocks, wrapped, truncated."""
    nb = int(np.ceil(n / L))
    starts = rng.integers(0, n, size=(nboot, nb))
    off = np.arange(L)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(nboot, nb * L) % n
    return idx[:, :n]


def interval(obs, draws):
    """SE, bootstrap t, percentile and BASIC (pivotal) 95% intervals for one paired difference.
    The HEADLINE interval is the BASIC one [2*obs - q975, 2*obs - q025]; the percentile interval
    and |t| >= 1.96 are reported beside it."""
    d = draws[np.isfinite(draws)]
    if len(d) < 50:
        return dict(SE=np.nan, t=np.nan, lo=np.nan, hi=np.nan, plo=np.nan, phi=np.nan,
                    excl0=False, excl0_pct=False, excl0_t=False, nb=len(d))
    se = float(d.std(ddof=1))
    qlo, qhi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    plo, phi = 2.0 * obs - qhi, 2.0 * obs - qlo
    tt = float(obs / se) if se > 0 else np.nan
    return dict(SE=se, t=tt, lo=qlo, hi=qhi, plo=plo, phi=phi,
                excl0=bool(plo > 0 or phi < 0),
                excl0_pct=bool(qlo > 0 or qhi < 0),
                excl0_t=bool(np.isfinite(tt) and abs(tt) >= 1.96), nb=len(d))


def matched_weight(tp, cal):
    """(rung A, rung B, weight w, clamped?) for the turnover-matched calendar point.
    cal: list of (turn_py, label) sorted ascending.  Reproduces np.interp exactly."""
    ts = [x for x, _ in cal]
    if tp <= ts[0]:
        return cal[0][1], cal[0][1], 0.0, True
    if tp >= ts[-1]:
        return cal[-1][1], cal[-1][1], 0.0, True
    for i in range(len(cal) - 1):
        if ts[i] <= tp <= ts[i + 1]:
            w = (tp - ts[i]) / (ts[i + 1] - ts[i])
            return cal[i][1], cal[i + 1][1], float(w), False
    raise RuntimeError("bracket not found")


def paired_edge(rb, ra, rB, w, L, nboot, seed):
    """Paired circular-block bootstrap of  Sharpe(book) - [(1-w)Sharpe(A) + w Sharpe(B)].
    All three legs are resampled on the SAME block offsets, so the difference keeps its pairing."""
    rng = np.random.default_rng(seed)
    n = len(rb)
    idx = block_index(n, L, nboot, rng)
    sb = sharpe_rows(rb[idx])
    sa = sharpe_rows(ra[idx])
    sB = sa if rB is ra else sharpe_rows(rB[idx])
    return sb - ((1.0 - w) * sa + w * sB)


def paired_edge_diff(rb1, ra1, rB1, w1, rb2, ra2, rB2, w2, L, nboot, seed):
    """V4: bootstrap  edge(book1) - edge(book2)  on IDENTICAL blocks (all legs paired)."""
    rng = np.random.default_rng(seed)
    n = len(rb1)
    idx = block_index(n, L, nboot, rng)

    def _edge(rb, ra, rB, w):
        sa = sharpe_rows(ra[idx])
        sB = sa if rB is ra else sharpe_rows(rB[idx])
        return sharpe_rows(rb[idx]) - ((1.0 - w) * sa + w * sB)

    return _edge(rb1, ra1, rB1, w1) - _edge(rb2, ra2, rB2, w2)


def score_cell(r0, t0, gs, nref, c, S, LV, nyears):
    r = net(r0, t0, c)
    mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
    h1, h2 = halves(r)
    ih1, ih2 = halves(r.loc[:IS_END])
    mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
           "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
           "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
           "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
    bl, nbad = binding(mar)
    k4bf = (h1 > S["h1"] and h2 > S["h2"]
            and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
            and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
    k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
            and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
            and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
    k4a = (h1 > LV["h1"] and h2 > LV["h2"] and mf["MaxDD"] >= LV["full"]["MaxDD"])
    k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"] and mo["MaxDD"] >= LV["oos"]["MaxDD"])
    is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
               + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
               + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
    isr = r.loc[:IS_END]
    return dict(
        is_legs=is_legs,
        cost=c, turn_py=float(t0.sum() / nyears),
        is_turn_py=float(t0.loc[:IS_END].sum() / (len(isr) / 252.0)),
        refresh_py=nref / (len(r0) / 252.0), gross_mean=float(gs.mean()),
        gross_crash_min=float(gs.loc[CRASH[0]:CRASH[1]].min())
        if len(gs.loc[CRASH[0]:CRASH[1]]) else np.nan,
        CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
        is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"], is_H1=ih1, is_H2=ih2,
        is_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
        oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
        **{k: float(v) for k, v in mar.items()},
        bind=bl, n_fail=nbad,
        keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
        keep4a=k4a, keep4a_oos=k4ao)


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2067 (lane cloud, {DATE}) — is the FRACTION RULE's crash-excised edge RESOLVABLE?")
    log(f"# statistic: Sharpe(book) - turnover-matched CALENDAR interp over R {REFRESH}, "
        f"paired circular-block bootstrap, weight w frozen at the full-sample turnover match.")
    log(f"# tuned dials (2, both bootstrap): block L {BLOCKS} (headline {BLOCK0}), draws "
        f"{NBOOT} (headline) / {NBOOT_HI} (stability).  seed {SEED}.")
    log(f"# reported, not tuned: panel, trade cadence {TRADES}, f {F_GRID}, cost {COSTS} bps, "
        f"tape (ALL / XCRASH {CRASH[0]}..{CRASH[1]}), window (FULL / OOS >= {OOS_START}).")
    log(f"# t FIXED at {TGT_STAR} (inherited).  sigma (L={SIG_L}, d={SIG_D}).  warm-up {WARMUP}.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0 (sprint brief)")

    rows, boot_rows, arm_rows, BASE, BOOKS, SER = [], [], [], {}, {}, {}

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        bk = Book(px, cols, px.index)
        BOOKS[pname] = (bk, px, cols, st)
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")

        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        B = dict(start=st, spy_r=spy,
                 spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]),
                          is_=mets(spy.loc[:IS_END]), h1=halves(spy)[0], h2=halves(spy)[1],
                          ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1],
                                 turn=float(lt.sum() / (len(lr) / 252.0)))
        BASE[pname] = B
        L0, S = B[f"live{COST0}"], B["spy"]
        log(f"   LIVE RULES v2 (W, {COST0}bps) {L0['full']['CAGR']:.2%} / "
            f"{L0['full']['Sharpe']:.4f} / {L0['full']['MaxDD']:.2%}  (OOS "
            f"{L0['oos']['CAGR']:.2%} / {L0['oos']['Sharpe']:.4f} / {L0['oos']['MaxDD']:.2%}), "
            f"{L0['turn']:.2f} turns/yr")
        log(f"   SPY                      {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}  (OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%})")

        for T in TRADES:
            # calendar ladder for this arm (the comparand curve)
            for Rc in REFRESH:
                r0, t0, gs, nref = bk.run(TGT_STAR, T, "CAL", Rc)
                r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                ny = len(r0) / 252.0
                SER[(pname, T, "CAL", Rc)] = net(r0, t0, COST0)
                for c in COSTS:
                    rows.append(dict(panel=pname, T_trade=T, family="CAL", rung=Rc,
                                     **score_cell(r0, t0, gs, nref, c, S, B[f"live{c}"], ny)))
            for fam, ladder in (("FRACG", F_GRID), ("ASYMG", [F_STAR]), ("FIXH", [H_STAR])):
                for rung in ladder:
                    r0, t0, gs, nref = bk.run(TGT_STAR, T, fam, rung)
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    ny = len(r0) / 252.0
                    SER[(pname, T, fam, rung)] = net(r0, t0, COST0)
                    for c in COSTS:
                        rows.append(dict(panel=pname, T_trade=T, family=fam, rung=rung,
                                         **score_cell(r0, t0, gs, nref, c, S, B[f"live{c}"], ny)))
        log(f"   books run ({len([r for r in rows if r['panel'] == pname]) // len(COSTS)} cells)")

    G = pd.DataFrame(rows)
    G["rung_f"] = pd.to_numeric(G["rung"], errors="coerce")
    G.to_csv(f"{OUT}.grid.csv.gz", index=False)
    log(f"\n# grid: {len(G)} scored rows ({len(G)//len(COSTS)} cells x {len(COSTS)} cost rungs)")

    # ------------------------------------------------------- the edge point estimates + bootstrap
    log("\n## EDGE + PAIRED BLOCK BOOTSTRAP (all cells, both tapes, both windows, 4 blocks)")
    for pname, (bk, px, cols, st) in BOOKS.items():
        for T in TRADES:
            cal_all = sorted((float(G[(G.panel == pname) & (G.T_trade == T) & (G.family == "CAL")
                                      & (G.rung == Rc) & (G.cost == COST0)].iloc[0].turn_py), Rc)
                             for Rc in REFRESH)
            for fam, ladder in (("FRACG", F_GRID), ("ASYMG", [F_STAR]), ("FIXH", [H_STAR])):
                for rung in ladder:
                    row = G[(G.panel == pname) & (G.T_trade == T) & (G.family == fam)
                            & (G.rung_f == rung) & (G.cost == COST0)].iloc[0]
                    tp = float(row.turn_py)
                    A, Bq, w, clamped = matched_weight(tp, cal_all)
                    rb_all = SER[(pname, T, fam, rung)]
                    ra_all, rB_all = SER[(pname, T, "CAL", A)], SER[(pname, T, "CAL", Bq)]
                    for tape in ("ALL", "XCRASH"):
                        f_ = (lambda s: s) if tape == "ALL" else excise
                        for win in ("FULL", "OOS"):
                            sl = (lambda s: s) if win == "FULL" else (lambda s: s.loc[OOS_START:])
                            sb_, sa_, sB_ = f_(sl(rb_all)), f_(sl(ra_all)), f_(sl(rB_all))
                            rb, ra, rB = sb_.values, sa_.values, sB_.values
                            rBx = ra if Bq == A else rB
                            obs = float(sharpe_rows(rb[None, :])[0]
                                        - ((1 - w) * sharpe_rows(ra[None, :])[0]
                                           + w * sharpe_rows(rBx[None, :])[0]))
                            # idea 2026's own convention (pandas ddof=1) for the reproduction
                            # gates; the BOOTSTRAP-consistent estimate above uses ddof=0, and the
                            # two differ only in the last few 1e-5 (reported at G2a).
                            obs_pub = float(mets(sb_)["Sharpe"]
                                            - ((1 - w) * mets(sa_)["Sharpe"]
                                               + w * mets(sB_ if Bq != A else sa_)["Sharpe"]))
                            for L in BLOCKS:
                                dr = paired_edge(rb, ra, rBx, w, L, NBOOT,
                                                 dseed(pname, T, fam, rung, tape, win, L))
                                iv = interval(obs, dr)
                                boot_rows.append(dict(panel=pname, T_trade=T, family=fam,
                                                      rung=rung, tape=tape, window=win, block=L,
                                                      nboot=NBOOT, turn_py=tp, calA=A, calB=Bq,
                                                      w=w, clamped=clamped, edge=obs,
                                                      edge_pub=obs_pub, **iv))
                            if True:   # draw-count stability at the headline block
                                dr = paired_edge(rb, ra, rBx, w, BLOCK0, NBOOT_HI,
                                                 dseed('hi', pname, T, fam, rung, tape, win))
                                iv = interval(obs, dr)
                                boot_rows.append(dict(panel=pname, T_trade=T, family=fam,
                                                      rung=rung, tape=tape, window=win,
                                                      block=BLOCK0, nboot=NBOOT_HI, turn_py=tp,
                                                      calA=A, calB=Bq, w=w, clamped=clamped,
                                                      edge=obs, edge_pub=obs_pub, **iv))
        log(f"   {pname} bootstrapped")

    BT = pd.DataFrame(boot_rows)
    BT.to_csv(f"{OUT}.bootstrap.csv.gz", index=False)
    log(f"# bootstrap rows: {len(BT)}")

    # ------------------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(BOOKS['U56'][1])/252:.1f}y", ">= 10",
         len(BOOKS["U56"][1]) / 252 >= 10)
    g1 = 0.0
    for (pn, T), pub in PUB_2026.items():
        r = G[(G.panel == pn) & (G.T_trade == T) & (G.family == "FRACG")
              & (G.rung_f == F_STAR) & (G.cost == COST0)].iloc[0]
        g1 = max(g1, abs(r.turn_py - pub["turn_py"]), abs(r.oos_Sharpe - pub["oos_Sharpe"]))
    gate("G1 reproduces idea 2026's FRACG f=0.10 cells (turnover, OOS Sharpe)",
         f"max|d| = {g1:.3e}", "< 1e-9", g1 < 1e-9)
    g2 = g2x = 0.0
    for (pn, T), pub in PUB_2026.items():
        e = BT[(BT.panel == pn) & (BT.T_trade == T) & (BT.family == "FRACG")
               & (BT.rung == F_STAR) & (BT.window == "OOS") & (BT.block == BLOCK0)
               & (BT.nboot == NBOOT)]
        g2 = max(g2, abs(float(e[e.tape == "ALL"].edge_pub.iloc[0]) - pub["d"]))
        g2x = max(g2x, abs(float(e[e.tape == "XCRASH"].edge_pub.iloc[0]) - pub["xd"]))
    gate("G2 reproduces idea 2026's matched-calendar edge, ALL tape (d_matched_cal)",
         f"max|d| = {g2:.3e}", "< 1e-9", g2 < 1e-9)
    gate("G3 reproduces idea 2026's matched-calendar edge, XCRASH tape (x_d_matched_cal)",
         f"max|d| = {g2x:.3e}", "< 1e-9", g2x < 1e-9)
    g4 = 0.0
    for (pn, T), xd in PUB_FIXH_XD.items():
        e = BT[(BT.panel == pn) & (BT.T_trade == T) & (BT.family == "FIXH")
               & (BT.tape == "XCRASH") & (BT.window == "OOS") & (BT.block == BLOCK0)
               & (BT.nboot == NBOOT)].iloc[0]
        g4 = max(g4, abs(float(e.edge_pub) - xd))
    gate("G4 reproduces idea 2026's incumbent FIXH h=0.12 XCRASH edges",
         f"max|d| = {g4:.3e}", "< 1e-9", g4 < 1e-9)
    gate("G2a bootstrap-consistent (ddof=0) vs published (ddof=1) Sharpe convention",
         f"max|d| = {float((BT.edge - BT.edge_pub).abs().max()):.3e}", "< 1e-3",
         float((BT.edge - BT.edge_pub).abs().max()) < 1e-3)
    gate("G5 gross never levered", f"max gross_mean {G.gross_mean.max():.6f}", "<= 1.0",
         G.gross_mean.max() <= 1.0 + 1e-9)
    nb = BT[(BT.nboot == NBOOT)].groupby(["panel", "T_trade", "family", "rung"]).size()
    gate("G6 every cell bootstrapped on every (tape x window x block)",
         f"{nb.min()} .. {nb.max()} rows/cell", f"== {2*2*len(BLOCKS)}",
         int(nb.min()) == int(nb.max()) == 2 * 2 * len(BLOCKS))
    cl = BT[(BT.family == "FRACG") & (BT.nboot == NBOOT) & (BT.block == BLOCK0)
            & (BT.tape == "XCRASH") & (BT.window == "OOS")]
    gate("G7 clamped (un-matchable) cells flagged, not silently scored",
         f"{int(cl.clamped.sum())} of {len(cl)} FRACG headline cells clamped", "reported",
         True)

    # ------------------------------------------------------------------------ V1: resolution
    log("\n## V1 — is the edge RESOLVABLE?  (share of cells whose 95% BASIC interval excludes 0)")
    res_rows = []
    for tape in ("ALL", "XCRASH"):
        for win in ("FULL", "OOS"):
            for L in BLOCKS:
                sub = BT[(BT.family == "FRACG") & (BT.tape == tape) & (BT.window == win)
                         & (BT.block == L) & (BT.nboot == NBOOT)]
                subm = sub[~sub.clamped]
                res_rows.append(dict(tape=tape, window=win, block=L, cells=len(sub),
                                     matched_cells=len(subm),
                                     mean_edge=float(sub.edge.mean()),
                                     pos=float((sub.edge > 0).mean()),
                                     share_excl0=float(sub.excl0.mean()),
                                     share_excl0_matched=float(subm.excl0.mean()) if len(subm)
                                     else np.nan,
                                     share_excl0_pct=float(sub.excl0_pct.mean()),
                                     share_excl0_t=float(sub.excl0_t.mean()),
                                     mean_SE=float(sub.SE.mean()),
                                     mean_absT=float(sub.t.abs().mean())))
    RES = pd.DataFrame(res_rows)
    RES.to_csv(f"{OUT}.resolution.csv", index=False)
    log(RES.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    head = RES[(RES.tape == "XCRASH") & (RES.window == "OOS") & (RES.block == BLOCK0)].iloc[0]
    v1 = bool(head.share_excl0 > V1_BAR)
    log(f"   V1 headline (XCRASH / OOS / block {BLOCK0}): {head.share_excl0:.3f} of "
        f"{int(head.cells)} cells resolvable, mean edge {head.mean_edge:+.4f}, mean SE "
        f"{head.mean_SE:.4f}  ->  {'TRIGGERED' if v1 else 'NOT triggered'} (bar > {V1_BAR})")

    # --------------------------------------------------------------- V2: the four-arm claim
    log("\n## V2 — idea 2026's OWN four pre-stated arms (f = 0.10), interval by interval")
    for (pn, T) in PUB_2026:
        for fam in ("FRACG", "FIXH"):
            rung = F_STAR if fam == "FRACG" else H_STAR
            for tape in ("ALL", "XCRASH"):
                e = BT[(BT.panel == pn) & (BT.T_trade == T) & (BT.family == fam)
                       & (BT.rung == rung) & (BT.tape == tape) & (BT.window == "OOS")
                       & (BT.block == BLOCK0) & (BT.nboot == NBOOT)].iloc[0]
                arm_rows.append(dict(panel=pn, T_trade=T, family=fam, rung=rung, tape=tape,
                                     turn_py=e.turn_py, calA=e.calA, calB=e.calB, w=e.w,
                                     clamped=e.clamped, edge=e.edge, SE=e.SE, t=e.t,
                                     lo95=e.plo, hi95=e.phi, excl0=e.excl0,
                                     excl0_pct=e.excl0_pct))
    ARM = pd.DataFrame(arm_rows)
    ARM.to_csv(f"{OUT}.arms.csv", index=False)
    log(ARM.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    fr_x = ARM[(ARM.family == "FRACG") & (ARM.tape == "XCRASH")]
    v2 = bool(fr_x.excl0.all())
    log(f"   the committed claim: mean XCRASH edge {fr_x.edge.mean():+.4f} "
        f"(2026 published +0.0377), {int((fr_x.edge > 0).sum())} of {len(fr_x)} positive; "
        f"{int(fr_x.excl0.sum())} of {len(fr_x)} RESOLVABLE  ->  V2 "
        f"{'TRIGGERED' if v2 else 'NOT triggered'}")
    fx_x = ARM[(ARM.family == "FIXH") & (ARM.tape == "XCRASH")]
    log(f"   incumbent FIXH h={H_STAR}: mean XCRASH edge {fx_x.edge.mean():+.4f} "
        f"(2026 published -0.0050), {int((fx_x.edge > 0).sum())} of {len(fx_x)} positive; "
        f"{int(fx_x.excl0.sum())} of {len(fx_x)} resolvable")

    # ------------------------------------------------------------ V3: block-ladder stability
    sh = RES[(RES.tape == "XCRASH") & (RES.window == "OOS")].set_index("block").share_excl0
    span = float(sh.max() - sh.min())
    v3 = bool(span <= V3_BAR)
    log(f"\n## V3 — block-ladder stability of the V1 share: "
        + ", ".join(f"L={b}: {v:.3f}" for b, v in sh.items())
        + f"  span {span:.3f}  ->  {'TRIGGERED' if v3 else 'NOT triggered'} (bar <= {V3_BAR})")
    st8 = BT[(BT.nboot == NBOOT_HI) & (BT.family == "FRACG") & (BT.tape == "XCRASH")
             & (BT.window == "OOS")]
    st2 = BT[(BT.nboot == NBOOT) & (BT.family == "FRACG") & (BT.tape == "XCRASH")
             & (BT.window == "OOS") & (BT.block == BLOCK0)]
    log(f"   draw-count read: share_excl0 {st2.excl0.mean():.3f} at B={NBOOT} vs "
        f"{st8.excl0.mean():.3f} at B={NBOOT_HI}; mean SE {st2.SE.mean():.4f} vs "
        f"{st8.SE.mean():.4f}")

    # ------------------------------------------------------- V4: FRACG minus FIXH, paired
    log("\n## V4 — FRACG(f=0.10) edge MINUS FIXH(h=0.12) edge, PAIRED on identical blocks")
    v4_rows = []
    for pname, (bk, px, cols, st) in BOOKS.items():
        for T in TRADES:
            cal_all = sorted((float(G[(G.panel == pname) & (G.T_trade == T) & (G.family == "CAL")
                                      & (G.rung == Rc) & (G.cost == COST0)].iloc[0].turn_py), Rc)
                             for Rc in REFRESH)
            leg = {}
            for fam, rung in (("FRACG", F_STAR), ("FIXH", H_STAR)):
                row = G[(G.panel == pname) & (G.T_trade == T) & (G.family == fam)
                        & (G.rung_f == rung) & (G.cost == COST0)].iloc[0]
                A, Bq, w, clamped = matched_weight(float(row.turn_py), cal_all)
                leg[fam] = (SER[(pname, T, fam, rung)], SER[(pname, T, "CAL", A)],
                            SER[(pname, T, "CAL", Bq)], w, clamped)
            for tape in ("ALL", "XCRASH"):
                f_ = (lambda s: s) if tape == "ALL" else excise
                rb1, ra1, rB1, w1, c1 = [f_(x.loc[OOS_START:]).values if isinstance(x, pd.Series)
                                         else x for x in leg["FRACG"]]
                rb2, ra2, rB2, w2, c2 = [f_(x.loc[OOS_START:]).values if isinstance(x, pd.Series)
                                         else x for x in leg["FIXH"]]
                e1 = float(sharpe_rows(rb1[None, :])[0] - ((1 - w1) * sharpe_rows(ra1[None, :])[0]
                                                           + w1 * sharpe_rows(rB1[None, :])[0]))
                e2 = float(sharpe_rows(rb2[None, :])[0] - ((1 - w2) * sharpe_rows(ra2[None, :])[0]
                                                           + w2 * sharpe_rows(rB2[None, :])[0]))
                obs = e1 - e2
                for L in BLOCKS:
                    dr = paired_edge_diff(rb1, ra1, rB1, w1, rb2, ra2, rB2, w2, L, NBOOT,
                                          dseed('v4', pname, T, tape, L))
                    iv = interval(obs, dr)
                    v4_rows.append(dict(panel=pname, T_trade=T, tape=tape, block=L,
                                        edge_FRACG=e1, edge_FIXH=e2, diff=obs,
                                        clamped=bool(c1 or c2), **iv))
    V4 = pd.DataFrame(v4_rows)
    V4.to_csv(f"{OUT}.fracg_vs_fixh.csv", index=False)
    log(V4[V4.block == BLOCK0].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    h4 = V4[(V4.tape == "XCRASH") & (V4.block == BLOCK0)]
    v4v = bool(h4.excl0.all() and (h4["diff"] > 0).all())
    log(f"   XCRASH / block {BLOCK0}: mean diff {h4['diff'].mean():+.4f}, "
        f"{int((h4['diff'] > 0).sum())} of {len(h4)} positive, {int(h4.excl0.sum())} of {len(h4)} "
        f"resolvable  ->  V4 {'TRIGGERED' if v4v else 'NOT triggered'}")

    # --------------------------------------------------- V5: both KEEP paths + rule-8 walk-forward
    log("\n## V5 — CAPITAL: both KEEP paths at every cell, all cost rungs")
    cen = (G[G.family == "FRACG"].groupby(["cost"])
           .agg(cells=("keep4b", "size"), keep4b_full=("keep4b_full", "sum"),
                keep4b_oos=("keep4b_oos", "sum"), keep4b=("keep4b", "sum"),
                keep4a=("keep4a", "sum"), keep4a_oos=("keep4a_oos", "sum")).reset_index())
    cen.to_csv(f"{OUT}.census.csv", index=False)
    log("FRACG family:\n" + cen.to_string(index=False))
    log("   binding leg at 4b-FULL failures (10 bps): "
        + "; ".join(f"{k} {v}" for k, v in
                    G[(G.cost == COST0) & (G.family == "FRACG") & ~G.keep4b_full]
                    .bind.value_counts().head(6).items()))

    log(f"\n## RULE 8 — f chosen on 2009-{IS_END[:4]} ONLY, {OOS_START[:4]}-2026 read once")
    wf_rows = []
    CHOOSERS = {"C_ISSHARPE": "is_Sharpe", "C_ISCALMAR": "is_Calmar",
                "C_ISLEGS": None, "C_ISDD": "is_MaxDD"}
    for pname in BOOKS:
        S, LV = BASE[pname]["spy"], BASE[pname][f"live{COST0}"]
        for T in TRADES:
            sub = G[(G.panel == pname) & (G.T_trade == T) & (G.family == "FRACG")
                    & (G.cost == COST0)].copy()
            for ch, col in CHOOSERS.items():
                if ch == "C_ISLEGS":                 # most IS 4b legs cleared, IS Sharpe breaks ties
                    key = sub.is_legs + sub.is_Sharpe / 1e6
                    pick = sub.loc[key.idxmax()]
                else:
                    pick = sub.loc[sub[col].idxmax()]
                wf_rows.append(dict(panel=pname, T_trade=T, chooser=ch, pick_f=pick.rung,
                                    is_Sharpe=pick.is_Sharpe, is_legs=pick.is_legs, oos_CAGR=pick.oos_CAGR,
                                    oos_Sharpe=pick.oos_Sharpe, oos_MaxDD=pick.oos_MaxDD,
                                    spy_oos_CAGR=S["oos"]["CAGR"], spy_oos_Sharpe=S["oos"]["Sharpe"],
                                    spy_oos_MaxDD=S["oos"]["MaxDD"],
                                    live_oos_CAGR=LV["oos"]["CAGR"],
                                    live_oos_Sharpe=LV["oos"]["Sharpe"],
                                    live_oos_MaxDD=LV["oos"]["MaxDD"],
                                    keep4b_full=pick.keep4b_full, keep4b_oos=pick.keep4b_oos,
                                    keep4b=pick.keep4b, keep4a=pick.keep4a,
                                    keep4a_oos=pick.keep4a_oos, bind=pick.bind))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    log(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"   rule-8 picks clearing 4b FULL+OOS: {int(WF.keep4b.sum())} of {len(WF)}; "
        f"4a: {int(WF.keep4a.sum())} of {len(WF)}")

    # the pre-stated (zero-IS) arm's own capital read, for the memo
    ps = G[(G.family == "FRACG") & (G.rung_f == F_STAR) & (G.cost == COST0)]
    log("\n## the PRE-STATED arm (f = 0.10), 10 bps, both KEEP paths")
    log(ps[["panel", "T_trade", "turn_py", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oos_CAGR",
            "oos_Sharpe", "oos_MaxDD", "bind", "keep4b_full", "keep4b_oos", "keep4b", "keep4a"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    gdf = pd.DataFrame(_gates)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\n# gates: {int(gdf.pass_.sum())}/{len(gdf)} pass")
    log(f"\n# VERDICTS: V1 {'TRIGGERED' if v1 else 'NOT'} | V2 {'TRIGGERED' if v2 else 'NOT'} | "
        f"V3 {'TRIGGERED' if v3 else 'NOT'} | V4 {'TRIGGERED' if v4v else 'NOT'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    return G, BT, RES, ARM, V4, WF


if __name__ == "__main__":
    main()
