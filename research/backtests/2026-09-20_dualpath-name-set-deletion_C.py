#!/usr/bin/env python3
"""Idea 2050 (lane C, 2026-09-20) — IS THE DUAL-PATH CELL A B136 NAME-SET ACCIDENT?

THE DEFECT THIS PRICES.  Idea 2034 turned up the record's first cell to clear BOTH KEEP paths
(`B136, VOLTGT t = 0.10, DRIFT refresh h = 0.08, trade weekly, 10 bps, t+1`), and idea 2054 then
stress-tested it on cost x delay x phase and left it a KEEP-candidate on path **4b only**
(36 of 36 points) with the 4a leg downgraded to an artefact (8 of 36).  Every one of those 36
points was read on the SAME 136 columns.  The panel is a CURRENT-constituent list, and idea 1749
showed the NAME SET is a REACHABLE axis worth ~43 pp of 4b pass rate on U56.  So the surviving 4b
claim has never been separated from its name set: a rule that needs all 136 survivors is a
survivorship artefact, not a rule.

WHAT IS PRICED HERE.  The candidate cell is re-scored on DELETED panels.  For each panel and each
rung of the deletion ladder, `k` names are removed uniformly at random (without replacement) from
the book's own held-name list, many seeded draws per rung, and the whole book is rebuilt on what
is left — the equal-weight basket, the panel volatility that drives the gross scalar, the drift
trigger and the turnover.  Both KEEP paths are scored at every draw.

    PANEL      {U56, B136, SMALL665}           B136 is the candidate's own panel; the other two
                                               are the record's standing companions.
    DELETE k   {0, 5, 10, 20, 40}              [dial 1]   k = 0 is the undeleted reference.
    DRAWS  D   200 seeded draws per (panel, k) [dial 2]   (k = 0 has exactly one draw: itself)
    CELL       t = 0.10, DRIFT h = 0.08, trade W, ENGINE phase, t+1, 10 bps   — INHERITED, not
               tuned here.  No third dial is spent.

  = 3 x 4 x 200 + 3 = 2,403 rebuilt books at the candidate cell, each scored on both paths.

RULE 8 (required, and run on the deleted panels too).  On a pre-stated subset of S = 15 draws per
(panel, k) — plus the undeleted reference — the two inherited dials are re-chosen on 2009-2016
ONLY by a legal IS-only chooser (argmax of the minimum in-sample 4b-leg slack, idea 2034's own
chooser) over the inherited ladder `t in {0.08, 0.10, 0.12, 0.16, 0.20}` x
`h in {0, .01, .02, .03, .05, .08, .12, .16, .20, .25}`, and 2017-2026 is read exactly ONCE.
That is 3 x 4 x 15 x 50 + 3 x 50 = 9,150 further scored books.  Reported: OOS CAGR / Sharpe /
MaxDD of the REACHED book against live RULES v2 and against SPY, the share of draws whose reached
book clears each path, and how often the chooser still lands on the candidate's own (t, h).

TWO BARS FOR PATH 4a, BOTH PUBLISHED.  Deleting names moves the book but not SPY, so path 4b's
bar is deletion-invariant by construction.  Path 4a's comparand is not, so both readings are
given at every draw: the **FIXED** bar (live RULES v2 on the FULL panel — the book real capital is
actually running, and therefore the headline) and the **MATCHED** bar (live RULES v2 rebuilt on
the same deleted name set — which isolates the name-set effect from the book effect).

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  IS THE 4b PASS A NAME-SET ACCIDENT?  On B136, the share of draws keeping 4b (FULL legs AND
      OOS) at the candidate cell.  >= 0.80 at EVERY k rung -> ROBUST: the cell does not need the
      full 136.  <= 0.40 at k = 10 or below -> NAME-SET ACCIDENT, i.e. a KILL of the unqualified
      cell.  Anything else -> PARTIAL, and the run names the rung where it breaks.
  V2  THE 4a LEG, same bands, on BOTH bars.  (Idea 2054 already downgraded 4a to an artefact of
      the discovery settings; this asks whether the name set is a further one.)
  V3  DOES THE DELETION RUN THROUGH ONE LEG?  Publish the binding-leg distribution over failing
      draws, per panel per k.
  V4  REACH (rule 8).  Share of deleted draws whose legal IS-only chooser lands on a 4b-clearing
      book, against the undeleted reference, plus the chooser's landing distribution over (t, h).

PROTOCOL: rule 2 (10 bps, weights decided at close t executed at close t+1, no leverage, gross
capped at 1.00); rule 3 (live RULES v2 AND SPY at every cell); rule 4 (both KEEP paths, and no
more than 2 tuned parameters — here k and the draw count, both REPORTED at every rung rather than
argmaxed); rule 5 (one idea, deterministic, standalone); rule 7 (a KILL is a result); rule 8 (IS
2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship stated).  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 and B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen
(tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Random deletion is NOT
a point-in-time correction: it removes survivors at random, where history removes the losers.  It
therefore bounds the SENSITIVITY of the verdict to the name set; it does not de-bias the levels,
which stay optimistic on every panel here.  Stated, not repaired.

WHAT THIS TEST CANNOT DO (stated, not repaired).  The deletion ladder is ABSOLUTE (k names), so
the same rung is a 29.4% cut of U56, a 12.1% cut of B136 and a 6.0% cut of SMALL665; the panels
are therefore NOT deletion-matched and the per-panel shares are not directly comparable.  The
realised fraction is published beside every row so the reader can do the comparison the ladder
does not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_dualpath-name-set-deletion_C.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                   # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask         # noqa: E402

DATE, SLUG = "2026-09-20", "dualpath-name-set-deletion"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST0 = 10.0                      # PROTOCOL rule 2 headline
DELAY = 1                         # PROTOCOL rule 2: decided at t, executed at t+1
TRADE = "W"                       # the candidate's cadence
KS = [5, 10, 20, 40]              # dial 1: deletion ladder
NDRAW = 200                       # dial 2: seeded draws per (panel, k)
NWF = 15                          # rule-8 subset: first NWF draws of each (panel, k)
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]                                  # inherited ladder
THRESH = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]      # inherited ladder
CAND_T, CAND_H = 0.10, 0.08
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0
SEED0 = 20500920

# committed numbers the undeleted B136 reference must reproduce, at the full precision of the
# committed artifact (research/backtests/2026-09-20_4b-verdict-bar-vs-book_cloud.grid.csv.gz)
PUB_CAND = dict(CAGR=0.1250962195302867, Sharpe=1.228631477106311,
                MaxDD=-0.1180752235695585, oCAGR=0.1300721924289238,
                oSharpe=1.2927878651902318, H1=1.3171143618077108, H2=1.1414896569837694)

_log: list[str] = []
_gates: list[dict] = []


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


def eq_weight_cols(px, cols):
    """Equal weight over the priced members of `cols`, on px's full column frame."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


def lag(a, d):
    a = np.asarray(a)
    if not d:
        return a
    pad = np.zeros((d,) + a.shape[1:], dtype=a.dtype) if a.ndim > 1 else np.zeros(d, dtype=a.dtype)
    return np.concatenate([pad, a[:-d]])


# ------------------------------------------------- the REFERENCE runners (idea 1799/2054 verbatim)
def bt_drift_ref(px_ret, W0, g0, mT, h):
    """Idea 1799's drift runner, copied verbatim; used ONLY to gate the fast runner below."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        trig = abs(g0[i] - cur.sum()) > h
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


def bt_hold_ref(px_ret, W0, mT):
    """engine.backtest's hold-and-drift loop on arrays (gross carried by W0 itself)."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    for i in range(n):
        if mT[i] or i == 0:
            new = W0[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn


# ------------------------------------------------------------------- the FAST drift runner
class DriftBook:
    """The same book as `bt_drift_ref`, factored so the O(T x N) work is done ONCE per panel
    and each (t, h) cell costs a scalar pass.

    The held vector is always `a * v` with `v` summing to 1: a TRADE resets `v` to the priced
    equal-weight vector, drift multiplies it by (1 + r) and renormalises, and a gross refresh
    scales `a` only.  So `v` does not depend on `t` or `h` at all and can be precomputed; only
    the scalar `a` and the trigger depend on the dials.  Gated against `bt_drift_ref` below.
    """

    def __init__(self, R, W0, mT):
        self.R, self.W0, self.mT = R, W0, mT
        n, _ = R.shape
        V = np.zeros_like(R)          # PRE-trade direction on each day
        xV = np.zeros(n)              # its same-day return
        xT = np.zeros(n)              # the POST-trade (equal-weight) direction's same-day return
        s0 = W0.sum(axis=1)
        v = np.zeros(R.shape[1])
        for i in range(n):
            V[i] = v
            xV[i] = float(v @ R[i])
            if mT[i] or i == 0:
                v = W0[i] / s0[i] if s0[i] > 0 else np.zeros(R.shape[1])
            xT[i] = float(v @ R[i])
            g = v * (1.0 + R[i])
            t = g.sum()
            v = g / t if t > 0 else v
        self.V, self.xV, self.xT, self.s0 = V, xV, xT, s0
        self.tdays = np.flatnonzero(mT | (np.arange(n) == 0))

    def run(self, g0, h):
        R, W0, mT, V = self.R, self.W0, self.mT, self.V
        n = len(R)
        a = 0.0
        g_eff = g0[0]
        nref = 0
        turn = np.zeros(n)
        gross = np.zeros(n)
        ret = np.zeros(n)
        for i in range(n):
            trig = abs(g0[i] - a) > h
            if trig or i == 0:
                g_eff = g0[i]
                nref += 1
            traded = mT[i] or i == 0
            if traded:
                s0 = self.s0[i]
                if s0 > 0:
                    turn[i] = np.abs(W0[i] * g_eff - a * V[i]).sum()
                    a = g_eff * s0
                else:                                   # nothing priced: target is all-zero
                    turn[i] = a
                    a = 0.0
                x = self.xT[i]
            else:
                if trig and a > 0:
                    turn[i] = abs(g_eff - a)
                    a = g_eff
                x = self.xV[i]
            gross[i] = a
            ret[i] = a * x
            tot = a * (1.0 + x) + (1.0 - a)
            if tot > 0:
                a = a * (1.0 + x) / tot
        return ret, turn, gross, nref


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


def score(r, S, LVfix, LVmat):
    """Score one net return stream on both KEEP paths.  `S` = SPY stats (deletion-invariant),
    `LVfix` = live RULES v2 on the FULL panel, `LVmat` = live RULES v2 on the SAME deleted set."""
    mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
    h1, h2 = halves(r)
    ih1, ih2 = halves(r.loc[:IS_END])
    mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
           "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
           "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
           "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
    bl, nbad = binding(mar)
    k4bf = all(mar[k] > 0 for k in LEGS)
    k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
            and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
            and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
    out = dict(CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
               is_Sharpe=mi["Sharpe"],
               is_minleg=float(min(ih1 - S["ish1"], ih2 - S["ish2"],
                                   mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                                   mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])),
               oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
               **{k: float(v) for k, v in mar.items()},
               bind=bl, n_fail=nbad, keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo))
    for tag, LV in (("fix", LVfix), ("mat", LVmat)):
        out[f"keep4a_{tag}"] = bool(h1 > LV["h1"] and h2 > LV["h2"]
                                    and mf["MaxDD"] >= LV["full"]["MaxDD"])
        out[f"keep4a_oos_{tag}"] = bool(mo["Sharpe"] > LV["oos"]["Sharpe"]
                                        and mo["MaxDD"] >= LV["oos"]["MaxDD"])
    return out


def live_stats(px, cols, st, mT_lagged):
    """Live RULES v2 (band 0.03, gross 0.75, weekly, t+1, 10 bps) on `cols`, fast path."""
    lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
    R = np.nan_to_num(px.pct_change().values, nan=0.0)
    r0, t0 = bt_hold_ref(R, lag(lw.values, DELAY), mT_lagged)
    r = net(pd.Series(r0, index=px.index), pd.Series(t0, index=px.index), COST0).loc[st:]
    h1, h2 = halves(r)
    return dict(full=mets(r), oos=mets(r.loc[OOS_START:]), h1=h1, h2=h2)


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2050 (lane C, {DATE}) — is the DUAL-PATH cell a B136 NAME-SET ACCIDENT?")
    log(f"# under deletion: the idea-2034 cell  t={CAND_T}, DRIFT h={CAND_H}, trade {TRADE}, "
        f"ENGINE phase, t+{DELAY}, {COST0:.0f} bps")
    log(f"# DIALS (2): deletion k {KS} (k=0 reference) x {NDRAW} seeded draws each.")
    log(f"# rule 8 on the first {NWF} draws of every (panel, k): inherited ladder "
        f"t {TARGETS} x h {THRESH}, IS <= {IS_END} chooses, OOS >= {OOS_START} read ONCE.")
    log(f"# BARS: SPY (deletion-invariant) and live RULES v2 on BOTH the FULL panel (fixed, the "
        f"headline) and the SAME deleted name set (matched).")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    draws, wf = [], []
    g_fast = 0.0            # fast runner vs bt_drift_ref (returns / turnover / gross path)
    g_nref = 0              # fast runner vs bt_drift_ref (refresh COUNT, h > 0 cells only)
    g_live = 0.0            # fast live book vs engine.backtest
    g_cand = np.nan         # reproduction of idea 2034's published candidate
    g_del = []              # deletion actually removed k names
    g_gross = 0.0

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        R = np.nan_to_num(px.pct_change().values, nan=0.0)
        idx = px.index
        mT = lag(np.asarray(rebalance_mask(idx, TRADE).values, bool), DELAY).astype(bool)
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        S = dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                 h1=halves(spy)[0], h2=halves(spy)[1],
                 ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1])
        LVfix = live_stats(px, cols, st, mT)

        # gate the fast live book against engine.backtest on the undeleted panel
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        eb = engine_backtest(px, lw, cost_bps=COST0, freq=TRADE)["returns"].loc[st:]
        _r, _t = bt_hold_ref(R, lag(lw.values, DELAY), mT)
        fb = net(pd.Series(_r, index=idx), pd.Series(_t, index=idx), COST0).loc[st:]
        g_live = max(g_live, float(np.abs(eb.values - fb.values).max()))

        log(f"\n## {pname}: {len(cols)} held names, {idx[0].date()} -> {idx[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")
        log(f"   LIVE v2 (W, t+1, {COST0:.0f}bps) {LVfix['full']['CAGR']:7.2%} / "
            f"{LVfix['full']['Sharpe']:.4f} / {LVfix['full']['MaxDD']:7.2%}  "
            f"(H1 {LVfix['h1']:.4f} H2 {LVfix['h2']:.4f}; OOS {LVfix['oos']['CAGR']:7.2%} / "
            f"{LVfix['oos']['Sharpe']:.4f} / {LVfix['oos']['MaxDD']:7.2%})")
        log(f"   SPY                        {S['full']['CAGR']:7.2%} / "
            f"{S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:7.2%}  "
            f"(H1 {S['h1']:.4f} H2 {S['h2']:.4f}; OOS {S['oos']['CAGR']:7.2%} / "
            f"{S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:7.2%})")
        log(f"   4b bars: FULL MaxDD >= {DD_CAP*S['full']['MaxDD']:.2%}, "
            f"CAGR >= {CAGR_FLOOR*S['full']['CAGR']:.2%};  "
            f"OOS MaxDD >= {DD_CAP*S['oos']['MaxDD']:.2%}, "
            f"CAGR >= {CAGR_FLOOR*S['oos']['CAGR']:.2%}")

        for k in [0] + KS:
            ndraw = 1 if k == 0 else NDRAW
            for d in range(ndraw):
                if k == 0:
                    keep = list(cols)
                    spy_dropped = False
                else:
                    rng = np.random.default_rng([SEED0, len(cols), k, d])
                    drop = set(rng.choice(len(cols), size=k, replace=False).tolist())
                    keep = [c for j, c in enumerate(cols) if j not in drop]
                    spy_dropped = "SPY" in cols and "SPY" not in keep
                g_del.append(len(cols) - len(keep) == k)

                W0 = lag(eq_weight_cols(px, keep).values, DELAY)
                SIG = panel_sigma(px, keep)
                bk = DriftBook(R, W0, mT)
                LVmat = LVfix if k == 0 else live_stats(px, keep, st, mT)

                def cell(tgt, h):
                    g0 = lag((tgt / SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values,
                             DELAY)
                    r0, t0, gs, nref = bk.run(g0, h)
                    r0 = pd.Series(r0, index=idx).loc[st:]
                    t0 = pd.Series(t0, index=idx).loc[st:]
                    gs = pd.Series(gs, index=idx).loc[st:]
                    return r0, t0, gs, nref

                r0, t0, gs, nref = cell(CAND_T, CAND_H)
                g_gross = max(g_gross, float(gs.max()))
                row = dict(panel=pname, n_full=len(cols), k=k, frac=k / len(cols), draw=d,
                           n_keep=len(keep), spy_dropped=spy_dropped,
                           turn_py=float(t0.sum() / (len(r0) / 252.0)),
                           refresh_py=nref / (len(px) / 252.0), gross_mean=float(gs.mean()),
                           live_mat_Sharpe=LVmat["full"]["Sharpe"],
                           live_mat_MaxDD=LVmat["full"]["MaxDD"])
                row.update(score(net(r0, t0, COST0), S, LVfix, LVmat))
                draws.append(row)

                if k == 0:
                    # gate: the undeleted B136 reference must reproduce idea 2034 exactly, and
                    # the fast runner must reproduce the verbatim loop at several cells
                    for tgt, h in ((CAND_T, CAND_H), (0.16, 0.0), (0.08, 0.25), (0.20, 0.03)):
                        g0 = lag((tgt / SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values,
                                 DELAY)
                        a = bk.run(g0, h)
                        b = bt_drift_ref(R, W0, g0, mT, h)
                        g_fast = max(g_fast, float(np.abs(np.asarray(a[0]) - b[0]).max()),
                                     float(np.abs(np.asarray(a[1]) - b[1]).max()),
                                     float(np.abs(np.asarray(a[2]) - b[2]).max()))
                        if h > 0:
                            g_nref = max(g_nref, abs(a[3] - b[3]))
                        elif a[3] != b[3]:
                            log(f"   note ({pname}, t={tgt}, h={h}): refresh COUNT differs "
                                f"{a[3]} vs {b[3]} — at h = 0 the trigger is a floating-point "
                                f"equality test on the deployed gross, and the two runners carry "
                                f"it in different last bits.  The BOOK is unaffected (the refresh "
                                f"writes back the same value it already holds): returns, turnover "
                                f"and gross agree to {max(float(np.abs(np.asarray(a[0])-b[0]).max()), float(np.abs(np.asarray(a[1])-b[1]).max())):.2e}. "
                                f"h = 0 is a ladder rung only; the candidate cell is h = 0.08.")
                    if pname == "B136":
                        g_cand = max(abs(row["CAGR"] - PUB_CAND["CAGR"]),
                                     abs(row["Sharpe"] - PUB_CAND["Sharpe"]),
                                     abs(row["MaxDD"] - PUB_CAND["MaxDD"]),
                                     abs(row["oos_CAGR"] - PUB_CAND["oCAGR"]),
                                     abs(row["oos_Sharpe"] - PUB_CAND["oSharpe"]),
                                     abs(row["H1"] - PUB_CAND["H1"]),
                                     abs(row["H2"] - PUB_CAND["H2"]))

                # -------------------------------------------------------- rule 8 on this draw
                if d < (1 if k == 0 else NWF):
                    best, cells = None, []
                    for tgt in TARGETS:
                        for h in THRESH:
                            rr, tt, gg, nr = cell(tgt, h)
                            sc = score(net(rr, tt, COST0), S, LVfix, LVmat)
                            sc.update(target=tgt, h=h)
                            cells.append(sc)
                            if best is None or sc["is_minleg"] > best["is_minleg"]:
                                best = sc
                    wf.append(dict(panel=pname, k=k, draw=d, n_keep=len(keep),
                                   pick_t=best["target"], pick_h=best["h"],
                                   is_minleg=best["is_minleg"],
                                   is_candidate_cell=(best["target"] == CAND_T
                                                      and best["h"] == CAND_H),
                                   n_cells_4b=sum(c["keep4b"] for c in cells),
                                   n_cells_4a_fix=sum(c["keep4a_fix"] for c in cells),
                                   live_fix_oos_Sharpe=LVfix["oos"]["Sharpe"],
                                   live_fix_oos_CAGR=LVfix["oos"]["CAGR"],
                                   live_fix_oos_MaxDD=LVfix["oos"]["MaxDD"],
                                   spy_oos_Sharpe=S["oos"]["Sharpe"],
                                   spy_oos_CAGR=S["oos"]["CAGR"],
                                   spy_oos_MaxDD=S["oos"]["MaxDD"],
                                   **{kk: best[kk] for kk in
                                      ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "oos_CAGR",
                                       "oos_Sharpe", "oos_MaxDD", "bind", "keep4b_full",
                                       "keep4b_oos", "keep4b", "keep4a_fix", "keep4a_oos_fix",
                                       "keep4a_mat")}))
            log(f"   {pname} k={k}: {ndraw} draws done "
                f"({len([r for r in draws if r['panel']==pname and r['k']==k])} rows)")

    D = pd.DataFrame(draws)
    W = pd.DataFrame(wf)
    D.to_csv(f"{OUT}.draws.csv.gz", index=False, compression="gzip")
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------------------ gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1a the fast DriftBook reproduces idea 1799's verbatim loop (returns/turnover/gross)",
         f"max|d| = {g_fast:.3e} over {4*len(PS)} (panel, cell) pairs", "< 1e-12", g_fast < 1e-12)
    gate("G1b the fast DriftBook reproduces its refresh COUNT at every h > 0 cell",
         f"max|d| = {g_nref} over {3*len(PS)} pairs", "== 0", g_nref == 0)
    gate("G2 the fast live-v2 book reproduces engine.backtest",
         f"max|d| = {g_live:.3e} over {len(PS)} panels", "< 1e-12", g_live < 1e-12)
    gate("G3 the undeleted B136 reference reproduces idea 2034's published candidate",
         f"max|d| = {g_cand:.3e}", "< 1e-9", bool(g_cand < 1e-9))
    gate("G4 every deletion draw removed exactly k names",
         f"{sum(g_del)} of {len(g_del)}", "all", all(g_del))
    gate("G5 gross never levered", f"max gross {g_gross:.6f}", "<= 1.0 + 1e-9",
         g_gross <= 1.0 + 1e-9)
    gate("G6 the draw census is complete",
         f"{len(D)} draws / {len(W)} walk-forward picks",
         f"== {len(PS)*(1+len(KS)*NDRAW)} / {len(PS)*(1+len(KS)*NWF)}",
         len(D) == len(PS) * (1 + len(KS) * NDRAW) and len(W) == len(PS) * (1 + len(KS) * NWF))
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)

    # ------------------------------------------------------------------------ V1 / V2 / V3
    log("\n## V1 / V2 — DOES THE CANDIDATE CELL SURVIVE RANDOM NAME DELETION?")
    log("   (share of draws keeping each path at t=0.10, h=0.08, W, t+1, 10 bps)")
    summ = []
    for pname in D.panel.unique():
        ref = D[(D.panel == pname) & (D.k == 0)].iloc[0]
        log(f"\n   {pname} (k=0 reference: {ref.CAGR:7.2%} / {ref.Sharpe:.4f} / {ref.MaxDD:7.2%}"
            f", 4b {'PASS' if ref.keep4b else 'FAIL'}, 4a-fix "
            f"{'PASS' if ref.keep4a_fix else 'FAIL'}, bind {ref.bind})")
        log(f"     {'k':>4} {'frac':>6} {'n':>5} {'4b':>7} {'4b_full':>8} {'4b_oos':>7} "
            f"{'4a_fix':>7} {'4a_mat':>7} {'Sharpe':>8} {'CAGR':>8} {'MaxDD':>8} "
            f"{'L5_CAGR':>9} {'top binding leg'}")
        for k in [0] + KS:
            g = D[(D.panel == pname) & (D.k == k)]
            bl = g.loc[~g.keep4b, "bind"].value_counts()
            top = f"{bl.index[0]} {bl.iloc[0]}/{len(g)}" if len(bl) else "-"
            log(f"     {k:>4} {g.frac.iloc[0]:>6.1%} {len(g):>5} {g.keep4b.mean():>7.3f} "
                f"{g.keep4b_full.mean():>8.3f} {g.keep4b_oos.mean():>7.3f} "
                f"{g.keep4a_fix.mean():>7.3f} {g.keep4a_mat.mean():>7.3f} "
                f"{g.Sharpe.mean():>8.4f} {g.CAGR.mean():>8.2%} {g.MaxDD.mean():>8.2%} "
                f"{g.L5_CAGR.mean():>9.4f} {top}")
            summ.append(dict(panel=pname, k=k, frac=float(g.frac.iloc[0]), n=len(g),
                             keep4b=float(g.keep4b.mean()),
                             keep4b_full=float(g.keep4b_full.mean()),
                             keep4b_oos=float(g.keep4b_oos.mean()),
                             keep4a_fix=float(g.keep4a_fix.mean()),
                             keep4a_mat=float(g.keep4a_mat.mean()),
                             Sharpe=float(g.Sharpe.mean()), Sharpe_sd=float(g.Sharpe.std()),
                             CAGR=float(g.CAGR.mean()), MaxDD=float(g.MaxDD.mean()),
                             turn_py=float(g.turn_py.mean()),
                             **{lg: float(g[lg].mean()) for lg in LEGS},
                             **{f"minmarg_{lg}": float(g[lg].min()) for lg in LEGS},
                             top_bind=top))
    SM = pd.DataFrame(summ)
    SM.to_csv(f"{OUT}.summary.csv", index=False)

    log("\n## V3 — THE BINDING LEG OVER FAILING DRAWS (all panels, all k > 0)")
    fail = D[(D.k > 0) & (~D.keep4b)]
    if len(fail):
        log("     " + "  ".join(f"{a}={b}" for a, b in fail.bind.value_counts().items()))
        for pname in D.panel.unique():
            f2 = fail[fail.panel == pname]
            if len(f2):
                log(f"     {pname}: " + "  ".join(f"{a}={b}"
                                                  for a, b in f2.bind.value_counts().items()))
    else:
        log("     no failing draws at any rung on any panel")
    log("   any-leg fail rates over ALL k>0 draws, per panel:")
    for pname in D.panel.unique():
        g = D[(D.panel == pname) & (D.k > 0)]
        log(f"     {pname}: " + "  ".join(f"{lg} {(g[lg] <= 0).mean():.3f}" for lg in LEGS)
            + f"   OOS-leg fail {1 - g.keep4b_oos.mean():.3f}")

    # SPY-deletion diagnostic: SPY is a HELD name on U56/B136 as well as the benchmark
    log("\n   diagnostic — draws that deleted SPY itself (SPY is a HELD name on U56 and B136,")
    log("   and the benchmark on all three; on SMALL665 it is the benchmark only, never held):")
    for pname, _px, _cols in PS:
        g = D[(D.panel == pname) & (D.k > 0)]
        if "SPY" not in _cols:
            log(f"     {pname}: SPY is not a held name on this panel — nothing to delete")
            continue
        a, b = g[g.spy_dropped], g[~g.spy_dropped]
        log(f"     {pname}: SPY deleted in {len(a)}/{len(g)} draws; 4b share "
            f"{(a.keep4b.mean() if len(a) else float('nan')):.3f} with SPY gone vs "
            f"{(b.keep4b.mean() if len(b) else float('nan')):.3f} with SPY kept")

    # ------------------------------------------------------------------------ V4 (rule 8)
    log("\n## V4 — RULE 8 ON THE DELETED PANELS (IS 2009-2016 chooses t and h; OOS read ONCE)")
    log(f"     {'panel':>8} {'k':>4} {'n':>4} {'4b':>6} {'4b_oos':>7} {'4a_fix':>7} "
         f"{'picks cand':>11} {'oosCAGR':>8} {'oosShrp':>8} {'oosDD':>8}  vs live / SPY OOS")
    wsumm = []
    for pname in W.panel.unique():
        for k in [0] + KS:
            g = W[(W.panel == pname) & (W.k == k)]
            if not len(g):
                continue
            lv, sp = g.iloc[0], g.iloc[0]
            log(f"     {pname:>8} {k:>4} {len(g):>4} {g.keep4b.mean():>6.3f} "
                f"{g.keep4b_oos.mean():>7.3f} {g.keep4a_fix.mean():>7.3f} "
                f"{g.is_candidate_cell.mean():>11.3f} {g.oos_CAGR.mean():>8.2%} "
                f"{g.oos_Sharpe.mean():>8.4f} {g.oos_MaxDD.mean():>8.2%}  "
                f"live {lv.live_fix_oos_CAGR:.2%}/{lv.live_fix_oos_Sharpe:.4f}/"
                f"{lv.live_fix_oos_MaxDD:.2%}  SPY {sp.spy_oos_CAGR:.2%}/"
                f"{sp.spy_oos_Sharpe:.4f}/{sp.spy_oos_MaxDD:.2%}")
            wsumm.append(dict(panel=pname, k=k, n=len(g), keep4b=float(g.keep4b.mean()),
                              keep4b_oos=float(g.keep4b_oos.mean()),
                              keep4a_fix=float(g.keep4a_fix.mean()),
                              picks_candidate=float(g.is_candidate_cell.mean()),
                              oos_CAGR=float(g.oos_CAGR.mean()),
                              oos_Sharpe=float(g.oos_Sharpe.mean()),
                              oos_MaxDD=float(g.oos_MaxDD.mean()),
                              live_oos_Sharpe=float(lv.live_fix_oos_Sharpe),
                              spy_oos_Sharpe=float(sp.spy_oos_Sharpe),
                              n_cells_4b=float(g.n_cells_4b.mean())))
    pd.DataFrame(wsumm).to_csv(f"{OUT}.wf_summary.csv", index=False)
    log("\n   where the IS-only chooser LANDS on the deleted panels (t, h):")
    for pname in W.panel.unique():
        g = W[(W.panel == pname) & (W.k > 0)]
        vc = g.groupby(["pick_t", "pick_h"]).size().sort_values(ascending=False).head(5)
        log(f"     {pname}: " + "  ".join(f"t={a:.2f},h={b:.2f}:{c}" for (a, b), c in vc.items()))

    # ------------------------------------------------------------------------ verdict
    log("\n## VERDICT (against the PRE-STATED bands)")
    b = SM[(SM.panel == "B136") & (SM.k > 0)]
    lo10 = float(b[b.k <= 10].keep4b.min())
    allk = float(b.keep4b.min())
    if allk >= 0.80:
        v1 = "ROBUST — the 4b pass is not a B136 name-set accident at any rung of this ladder"
    elif lo10 <= 0.40:
        v1 = "NAME-SET ACCIDENT — KILL of the unqualified cell"
    else:
        brk = b[b.keep4b < 0.80]
        v1 = ("PARTIAL — breaks at k = "
              + (str(int(brk.k.iloc[0])) if len(brk) else "n/a"))
    log(f"   V1 (4b on B136): min share over k = {allk:.3f} (k<=10: {lo10:.3f})  ->  {v1}")
    a_fix = float(b.keep4a_fix.min())
    a_mat = float(b.keep4a_mat.min())
    v2 = ("ROBUST" if min(a_fix, a_mat) >= 0.80
          else "ARTEFACT" if max(a_fix, a_mat) <= 0.40 else "PARTIAL")
    log(f"   V2 (4a on B136): min share fixed bar {a_fix:.3f}, matched bar {a_mat:.3f}  ->  {v2}")
    log(f"   V1/V2 on the companion panels: "
        + "; ".join(f"{p} 4b min {float(SM[(SM.panel==p)&(SM.k>0)].keep4b.min()):.3f} / "
                    f"4a-fix min {float(SM[(SM.panel==p)&(SM.k>0)].keep4a_fix.min()):.3f}"
                    for p in SM.panel.unique() if p != "B136"))

    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    log(f"\n# wrote {OUT.name}.draws.csv.gz / .summary.csv / .walkforward.csv / "
        f".wf_summary.csv / .gates.csv / .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
