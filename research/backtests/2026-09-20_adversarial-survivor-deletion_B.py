#!/usr/bin/env python3
"""Idea 2064 (lane B, 2026-09-20) — DOES THE STANDING KEEP-4b CELL SURVIVE *ADVERSARIAL*
(BEST-NAME) DELETION, THE SURVIVORSHIP DIRECTION RANDOM DELETION CANNOT BOUND?

THE DEFECT THIS PRICES.  Idea 2050 (lane C, same day) deleted `k` names UNIFORMLY AT RANDOM from
the standing candidate's panel and found the 4b leg survives 800 of 800 draws.  Its own closing
paragraph states the limit of that result verbatim:

    "random deletion is NOT a point-in-time correction -- it removes survivors at random where
     history removes losers -- so it bounds the verdict's SENSITIVITY to the name set and does
     not de-bias the LEVELS, which stay optimistic on every panel here."

That is the whole residue.  B136 and U56 are CURRENT-constituent lists, so the bias they carry is
DIRECTIONAL: the panel over-includes names that went on to win.  The honest stress is therefore
not a random cut but an ADVERSARIAL one in the survivorship direction -- delete the names the
current-constituent list most plausibly over-includes (the biggest winners) and ask whether the
standing KEEP-4b cell still clears.  Nothing in the record has ever run that direction.

WHAT IS PRICED HERE.  The standing candidate cell (`VOLTGT t = 0.10, DRIFT h = 0.08, trade W,
ENGINE phase, t+1, 10 bps`, idea 2034 / memo `2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md`) is
re-scored on DELETED panels, with the whole book rebuilt on what is left -- the equal-weight
basket, the realised panel vol that drives the gross scalar, the drift trigger and the turnover.

    PANEL        {U56, B136}                  B136 is the candidate's own panel.
    DELETE k     {0, 5, 10, 20, 40}           [dial 1]  k = 0 is the undeleted reference.
    RULE         {BEST, BEST_IS, WORST, RANDOM}   [dial 2]
                   BEST     delete the k names with the HIGHEST full-sample annualised return
                            (the adversarial survivorship direction; uses the whole tape to
                            CHOOSE THE DELETION, which is look-ahead in the STRESS, not in the
                            book -- an upper bound on the bias, stated not hidden).
                   BEST_IS  the same, ranked on 2009-2016 ONLY -- an ex-ante implementable
                            version that reads no out-of-sample return at all.
                   WORST    delete the k LOWEST-return names -- the opposite direction, which
                            bounds the other side and shows the spread the random draw averages.
                   RANDOM   30 seeded draws per (panel, k): idea 2050's own null, re-run here so
                            the adversarial rungs are read against a same-script control band.
    CELL         INHERITED, not tuned here.  No third dial is spent; k and RULE are REPORTED at
                 every rung rather than argmaxed.

RULE 8 (required, run on the deleted panels too).  At every deterministic deleted panel -- and on
the first 8 RANDOM draws of each (panel, k) -- the two inherited dials are re-chosen on 2009-2016
ONLY by the legal IS-only chooser (argmax of the minimum in-sample 4b-leg slack, idea 2034's own)
over the inherited ladder `t in {0.08, 0.10, 0.12, 0.16, 0.20}` x
`h in {0, .01, .02, .03, .05, .08, .12, .16, .20, .25}`, and 2017-2026 is read exactly ONCE.
Reported: OOS CAGR / Sharpe / MaxDD of the REACHED book against live RULES v2 AND SPY, the share
of panels whose reached book clears each path, and where the chooser lands on (t, h).

TWO BARS FOR PATH 4a, BOTH PUBLISHED.  Deleting names moves the book but not SPY, so path 4b's
bar is deletion-invariant by construction.  Path 4a's comparand is not, so both are given at
every panel: the FIXED bar (live RULES v2 on the FULL panel -- the book real capital is actually
running, and therefore the headline) and the MATCHED bar (live RULES v2 rebuilt on the SAME
deleted name set, which isolates the name-set effect from the book effect).

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE HEADLINE.  On B136, does the candidate cell keep 4b (FULL legs AND OOS) under BEST and
      BEST_IS at EVERY k rung?  All 8 rungs -> ROBUST in the survivorship direction: idea 2050's
      800-of-800 is not a random-direction artefact.  A failure at k <= 10 on either rule -> the
      unqualified 4b claim is a WINNER-CONCENTRATION artefact and is KILLED.  Anything in between
      -> PARTIAL, and the run names the rung and the leg where it breaks.
  V2  PATH 4a, same bands, on BOTH bars.  (2054 and 2050 already downgraded 4a twice, both times
      through MaxDD against a 0.43 pp margin; this is the third independent axis.)
  V3  THE BINDING LEG at every failing rung, published as a distribution, never as a verdict.
  V4  REACH (rule 8): does a legal IS-only chooser still find a 4b-clearing book on an
      adversarially deleted panel, and what does it cost OOS?
  V5  DIRECTION ASYMMETRY: BEST vs WORST vs the RANDOM band at matched k.  If the RANDOM band
      does not contain the BEST rung, idea 2050's null is the wrong null for survivorship and the
      run says so.

PROTOCOL: rule 2 (10 bps, weights decided at close t executed at close t+1, no leverage, gross
capped at 1.00); rule 3 (live RULES v2 AND SPY at every cell); rule 4 (both KEEP paths; no more
than 2 tuned parameters -- here k and RULE, both reported at every rung); rule 5 (one idea,
deterministic, standalone); rule 7 (a KILL is a result); rule 8 (IS 2009-2016 chooses, 2017-2026
read exactly once); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

WHAT THIS TEST CANNOT DO (stated, not repaired).  Deleting winners is a BOUND on survivorship
bias, not a correction of it: history does not delete the biggest winners, it fails to list the
losers that were there at the time and are not on the list today.  The two are not the same
operation, and this one has no way to put a delisted 2011 name back.  BEST also chooses its
deletion with the full tape in hand, so its levels are pessimistic by construction -- BEST_IS is
the ex-ante readable version and both are published side by side.  The k ladder is ABSOLUTE, so
k = 40 is 71.4% of U56 and 29.4% of B136: the per-panel shares are NOT deletion-matched and must
not be compared across panels.  SMALL665 is not run here (six committed confirmations that this
family clears 4b 0 of N on small caps; nothing this axis can do moves that).

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_adversarial-survivor-deletion_B.py
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

DATE, SLUG = "2026-09-20", "adversarial-survivor-deletion"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST0, DELAY, TRADE = 10.0, 1, "W"
KS = [5, 10, 20, 40]
RULES = ["BEST", "BEST_IS", "WORST", "RANDOM"]
NRAND = 30                 # seeded RANDOM draws per (panel, k) -- the control band
NRAND_WF = 8               # of those, the ones that also get a rule-8 chooser
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
THRESH = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]
CAND_T, CAND_H = 0.10, 0.08
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0
SEED0 = 20640920

# idea 2034's published candidate, at the full precision of the committed artifact
# research/backtests/2026-09-20_4b-verdict-bar-vs-book_cloud.grid.csv.gz
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
    return [("U56", px56, list(px56.columns)), ("B136", px136, list(px136.columns))]


def ann_return(px, cols, upto=None):
    """Annualised return of each name over the days it is actually priced (its own span).
    `upto` truncates the ranking window (BEST_IS uses 2009-2016 only)."""
    sub = px[cols] if upto is None else px[cols].loc[:upto]
    out = {}
    for c in sub.columns:
        s = sub[c].dropna()
        if len(s) < 252 or s.iloc[0] <= 0:
            out[c] = np.nan                       # too short to rank; never deleted
            continue
        yrs = len(s) / 252.0
        out[c] = (s.iloc[-1] / s.iloc[0]) ** (1.0 / yrs) - 1.0
    return pd.Series(out)


def eq_weight_cols(px, cols):
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


def lag(a, d):
    a = np.asarray(a)
    if not d:
        return a
    pad = np.zeros((d,) + a.shape[1:], dtype=a.dtype) if a.ndim > 1 else np.zeros(d, dtype=a.dtype)
    return np.concatenate([pad, a[:-d]])


# ------------------------------------------------- REFERENCE runners (idea 1799 / 2050, verbatim)
def bt_drift_ref(px_ret, W0, g0, mT, h):
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


class DriftBook:
    """idea 2050's fast factoring of the same book: the held vector is `a * v` with `v` summing
    to 1 and independent of (t, h), so the O(T x N) work is done once per panel.  Gated."""

    def __init__(self, R, W0, mT):
        self.R, self.W0, self.mT = R, W0, mT
        n, _ = R.shape
        V = np.zeros_like(R)
        xV = np.zeros(n)
        xT = np.zeros(n)
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

    def run(self, g0, h):
        W0, mT, V = self.W0, self.mT, self.V
        n = len(self.R)
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
            if mT[i] or i == 0:
                s0 = self.s0[i]
                if s0 > 0:
                    turn[i] = np.abs(W0[i] * g_eff - a * V[i]).sum()
                    a = g_eff * s0
                else:
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


def live_stats(px, cols, st, mT_lagged, R):
    lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
    r0, t0 = bt_hold_ref(R, lag(lw.values, DELAY), mT_lagged)
    r = net(pd.Series(r0, index=px.index), pd.Series(t0, index=px.index), COST0).loc[st:]
    h1, h2 = halves(r)
    return dict(full=mets(r), oos=mets(r.loc[OOS_START:]), h1=h1, h2=h2)


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2064 (lane B, {DATE}) — ADVERSARIAL (best-name) deletion of the standing "
        f"KEEP-4b cell")
    log(f"# cell (INHERITED, not tuned): t={CAND_T}, DRIFT h={CAND_H}, trade {TRADE}, ENGINE "
        f"phase, t+{DELAY}, {COST0:.0f} bps")
    log(f"# DIALS (2): k {KS} (k=0 reference) x RULE {RULES}; RANDOM = {NRAND} seeded draws/rung")
    log(f"# rule 8 at every deterministic deleted panel + first {NRAND_WF} RANDOM draws: ladder "
        f"t {TARGETS} x h {THRESH}; IS <= {IS_END} chooses, OOS >= {OOS_START} read ONCE")

    rows, wf = [], []
    g_fast = 0.0
    g_nref = 0
    g_live = 0.0
    g_cand = np.nan
    g_del, g_gross = [], 0.0
    g_rank = []

    for pname, px, cols in panels():
        st = px.index[WARMUP]
        idx = px.index
        R = np.nan_to_num(px.pct_change().values, nan=0.0)
        mT = lag(np.asarray(rebalance_mask(idx, TRADE).values, bool), DELAY).astype(bool)
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        S = dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                 h1=halves(spy)[0], h2=halves(spy)[1],
                 ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1])
        LVfix = live_stats(px, cols, st, mT, R)

        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        eb = engine_backtest(px, lw, cost_bps=COST0, freq=TRADE)["returns"].loc[st:]
        _r, _t = bt_hold_ref(R, lag(lw.values, DELAY), mT)
        fb = net(pd.Series(_r, index=idx), pd.Series(_t, index=idx), COST0).loc[st:]
        g_live = max(g_live, float(np.abs(eb.values - fb.values).max()))

        ar_full = ann_return(px, cols).dropna().sort_values(ascending=False)
        ar_is = ann_return(px, cols, upto=IS_END).dropna().sort_values(ascending=False)
        g_rank.append(len(ar_full) >= max(KS) and len(ar_is) >= max(KS))

        log(f"\n## {pname}: {len(cols)} held names, {idx[0].date()} -> {idx[-1].date()} "
            f"({len(px)/252:.1f}y); book window from {st.date()}")
        log(f"   LIVE v2 (W, t+1, {COST0:.0f}bps) {LVfix['full']['CAGR']:7.2%} / "
            f"{LVfix['full']['Sharpe']:.4f} / {LVfix['full']['MaxDD']:7.2%}  "
            f"(H1 {LVfix['h1']:.4f} H2 {LVfix['h2']:.4f}; OOS {LVfix['oos']['CAGR']:7.2%} / "
            f"{LVfix['oos']['Sharpe']:.4f} / {LVfix['oos']['MaxDD']:7.2%})")
        log(f"   SPY                        {S['full']['CAGR']:7.2%} / "
            f"{S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:7.2%}  "
            f"(H1 {S['h1']:.4f} H2 {S['h2']:.4f}; OOS {S['oos']['CAGR']:7.2%} / "
            f"{S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:7.2%})")
        log(f"   4b bars: FULL MaxDD >= {DD_CAP*S['full']['MaxDD']:.2%}, "
            f"CAGR >= {CAGR_FLOOR*S['full']['CAGR']:.2%};  OOS MaxDD >= "
            f"{DD_CAP*S['oos']['MaxDD']:.2%}, CAGR >= {CAGR_FLOOR*S['oos']['CAGR']:.2%}")
        log(f"   top-5 by full-sample annualised return: "
            f"{', '.join(f'{c} {v:.1%}' for c, v in ar_full.head(5).items())}")
        log(f"   top-5 by IS (<= {IS_END}) annualised return: "
            f"{', '.join(f'{c} {v:.1%}' for c, v in ar_is.head(5).items())}")

        jobs = [("NONE", 0, 0, list(cols))]
        for k in KS:
            jobs.append(("BEST", k, 0, [c for c in cols if c not in set(ar_full.index[:k])]))
            jobs.append(("BEST_IS", k, 0, [c for c in cols if c not in set(ar_is.index[:k])]))
            jobs.append(("WORST", k, 0, [c for c in cols if c not in set(ar_full.index[-k:])]))
            for d in range(NRAND):
                rng = np.random.default_rng([SEED0, len(cols), k, d])
                drop = set(rng.choice(len(cols), size=k, replace=False).tolist())
                jobs.append(("RANDOM", k, d, [c for j, c in enumerate(cols) if j not in drop]))

        for rule, k, d, keep in jobs:
            g_del.append(len(cols) - len(keep) == k)
            W0 = lag(eq_weight_cols(px, keep).values, DELAY)
            SIG = panel_sigma(px, keep)
            bk = DriftBook(R, W0, mT)
            LVmat = LVfix if k == 0 else live_stats(px, keep, st, mT, R)

            def cell(tgt, h):
                g0 = lag((tgt / SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values, DELAY)
                r0, t0, gs, nref = bk.run(g0, h)
                return (pd.Series(r0, index=idx).loc[st:], pd.Series(t0, index=idx).loc[st:],
                        pd.Series(gs, index=idx).loc[st:], nref)

            r0, t0, gs, nref = cell(CAND_T, CAND_H)
            g_gross = max(g_gross, float(gs.max()))
            row = dict(panel=pname, n_full=len(cols), rule=rule, k=k, draw=d,
                       frac=k / len(cols), n_keep=len(keep),
                       spy_dropped=("SPY" in cols and "SPY" not in keep),
                       turn_py=float(t0.sum() / (len(r0) / 252.0)),
                       refresh_py=nref / (len(px) / 252.0), gross_mean=float(gs.mean()),
                       live_mat_Sharpe=LVmat["full"]["Sharpe"],
                       live_mat_MaxDD=LVmat["full"]["MaxDD"])
            row.update(score(net(r0, t0, COST0), S, LVfix, LVmat))
            rows.append(row)

            if rule == "NONE":
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
                        log(f"   note ({pname}, t={tgt}, h=0): refresh COUNT differs "
                            f"{a[3]} vs {b[3]} — at h = 0 the trigger is a floating-point "
                            f"equality test on the deployed gross and the two runners carry it "
                            f"in different last bits; the BOOK is unaffected.  h = 0 is a ladder "
                            f"rung only; the candidate cell is h = 0.08.")
                if pname == "B136":
                    g_cand = max(abs(row["CAGR"] - PUB_CAND["CAGR"]),
                                 abs(row["Sharpe"] - PUB_CAND["Sharpe"]),
                                 abs(row["MaxDD"] - PUB_CAND["MaxDD"]),
                                 abs(row["oos_CAGR"] - PUB_CAND["oCAGR"]),
                                 abs(row["oos_Sharpe"] - PUB_CAND["oSharpe"]),
                                 abs(row["H1"] - PUB_CAND["H1"]),
                                 abs(row["H2"] - PUB_CAND["H2"]))

            if rule != "RANDOM" or d < NRAND_WF:
                best, cells = None, []
                for tgt in TARGETS:
                    for h in THRESH:
                        rr, tt, _gg, _nr = cell(tgt, h)
                        sc = score(net(rr, tt, COST0), S, LVfix, LVmat)
                        sc.update(target=tgt, h=h)
                        cells.append(sc)
                        if best is None or sc["is_minleg"] > best["is_minleg"]:
                            best = sc
                wf.append(dict(panel=pname, rule=rule, k=k, draw=d, n_keep=len(keep),
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
        log(f"   {pname}: {len([r for r in rows if r['panel']==pname])} books, "
            f"{len([w for w in wf if w['panel']==pname])} rule-8 picks")

    D = pd.DataFrame(rows)
    W = pd.DataFrame(wf)
    D.to_csv(f"{OUT}.books.csv.gz", index=False, compression="gzip")
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------------------ gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(load_universe())/252:.1f}y", ">= 10",
         len(load_universe()) / 252 >= 10)
    gate("G1a fast DriftBook reproduces idea 1799's verbatim loop (returns/turnover/gross)",
         f"max|d| = {g_fast:.3e}", "< 1e-12", g_fast < 1e-12)
    gate("G1b fast DriftBook reproduces its refresh COUNT at every h > 0 cell",
         f"max|d| = {g_nref}", "== 0", g_nref == 0)
    gate("G2 fast live-v2 book reproduces engine.backtest", f"max|d| = {g_live:.3e}",
         "< 1e-12", g_live < 1e-12)
    gate("G3 undeleted B136 reference reproduces idea 2034's published candidate",
         f"max|d| = {g_cand:.3e}", "< 1e-9", bool(g_cand < 1e-9))
    gate("G4 every deletion removed exactly k names", f"{sum(g_del)} of {len(g_del)}", "all",
         all(g_del))
    gate("G5 gross never levered", f"max gross {g_gross:.6f}", "<= 1.0 + 1e-9",
         g_gross <= 1.0 + 1e-9)
    gate("G6 both ranking windows resolve >= max(k) names on every panel",
         f"{sum(g_rank)} of {len(g_rank)}", "all", all(g_rank))
    exp_books = 2 * (1 + len(KS) * (3 + NRAND))
    exp_wf = 2 * (1 + len(KS) * (3 + NRAND_WF))
    gate("G7 census complete", f"{len(D)} books / {len(W)} rule-8 picks",
         f"== {exp_books} / {exp_wf}", len(D) == exp_books and len(W) == exp_wf)
    gate("G8 BEST really deletes winners (mean full CAGR of BEST books < WORST books, B136)",
         f"{D[(D.panel=='B136')&(D.rule=='BEST')].CAGR.mean():.4%} vs "
         f"{D[(D.panel=='B136')&(D.rule=='WORST')].CAGR.mean():.4%}", "BEST < WORST",
         D[(D.panel == 'B136') & (D.rule == 'BEST')].CAGR.mean()
         < D[(D.panel == 'B136') & (D.rule == 'WORST')].CAGR.mean())
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)

    # ------------------------------------------------------------------- V1 / V2 / V3 / V5
    log("\n## V1 / V2 / V3 — THE CANDIDATE CELL UNDER ADVERSARIAL DELETION")
    log("   (t=0.10, h=0.08, W, t+1, 10 bps; RANDOM rows are the mean over "
        f"{NRAND} seeded draws)")
    summ = []
    for pname in D.panel.unique():
        ref = D[(D.panel == pname) & (D.rule == "NONE")].iloc[0]
        log(f"\n   {pname}  reference (k=0): {ref.CAGR:7.2%} / {ref.Sharpe:.4f} / "
            f"{ref.MaxDD:7.2%}  4b {'PASS' if ref.keep4b else 'FAIL'}  "
            f"4a-fix {'PASS' if ref.keep4a_fix else 'FAIL'}  bind {ref.bind}")
        log(f"     {'rule':>8} {'k':>3} {'frac':>6} {'n':>4} {'4b':>6} {'4b_ful':>7} "
            f"{'4b_oos':>7} {'4a_fix':>7} {'4a_mat':>7} {'CAGR':>8} {'Sharpe':>8} "
            f"{'MaxDD':>8} {'L5_CAGR':>9} {'L4_DD':>8} {'binding'}")
        for rule in RULES:
            for k in KS:
                g = D[(D.panel == pname) & (D.rule == rule) & (D.k == k)]
                if not len(g):
                    continue
                bl = g.loc[~g.keep4b, "bind"].value_counts()
                top = f"{bl.index[0]} {bl.iloc[0]}/{len(g)}" if len(bl) else "-"
                log(f"     {rule:>8} {k:>3} {g.frac.iloc[0]:>6.1%} {len(g):>4} "
                    f"{g.keep4b.mean():>6.3f} {g.keep4b_full.mean():>7.3f} "
                    f"{g.keep4b_oos.mean():>7.3f} {g.keep4a_fix.mean():>7.3f} "
                    f"{g.keep4a_mat.mean():>7.3f} {g.CAGR.mean():>8.2%} "
                    f"{g.Sharpe.mean():>8.4f} {g.MaxDD.mean():>8.2%} "
                    f"{g.L5_CAGR.mean():>9.4f} {g.L4_DD.mean():>8.4f} {top}")
                summ.append(dict(panel=pname, rule=rule, k=k, frac=float(g.frac.iloc[0]),
                                 n=len(g), keep4b=float(g.keep4b.mean()),
                                 keep4b_full=float(g.keep4b_full.mean()),
                                 keep4b_oos=float(g.keep4b_oos.mean()),
                                 keep4a_fix=float(g.keep4a_fix.mean()),
                                 keep4a_mat=float(g.keep4a_mat.mean()),
                                 CAGR=float(g.CAGR.mean()), Sharpe=float(g.Sharpe.mean()),
                                 MaxDD=float(g.MaxDD.mean()),
                                 oos_CAGR=float(g.oos_CAGR.mean()),
                                 oos_Sharpe=float(g.oos_Sharpe.mean()),
                                 oos_MaxDD=float(g.oos_MaxDD.mean()),
                                 L5_CAGR=float(g.L5_CAGR.mean()),
                                 L4_DD=float(g.L4_DD.mean()), top_bind=top))
    pd.DataFrame(summ).to_csv(f"{OUT}.summary.csv", index=False)

    log("\n## V5 — DIRECTION ASYMMETRY: is the RANDOM band the right null for survivorship?")
    log(f"     {'panel':>6} {'k':>3} {'BEST Sh':>9} {'BEST_IS':>9} {'WORST':>9} "
        f"{'RAND mean':>10} {'RAND min':>9} {'RAND max':>9} {'BEST inside band?':>18}")
    asym = []
    for pname in D.panel.unique():
        for k in KS:
            sel = D[(D.panel == pname) & (D.k == k)]
            rnd = sel[sel.rule == "RANDOM"].Sharpe
            vals = {r: float(sel[sel.rule == r].Sharpe.iloc[0])
                    for r in ("BEST", "BEST_IS", "WORST")}
            inside = bool(rnd.min() <= vals["BEST"] <= rnd.max())
            log(f"     {pname:>6} {k:>3} {vals['BEST']:>9.4f} {vals['BEST_IS']:>9.4f} "
                f"{vals['WORST']:>9.4f} {rnd.mean():>10.4f} {rnd.min():>9.4f} "
                f"{rnd.max():>9.4f} {str(inside):>18}")
            asym.append(dict(panel=pname, k=k, BEST=vals["BEST"], BEST_IS=vals["BEST_IS"],
                             WORST=vals["WORST"], rand_mean=float(rnd.mean()),
                             rand_min=float(rnd.min()), rand_max=float(rnd.max()),
                             best_inside_random_band=inside))
    pd.DataFrame(asym).to_csv(f"{OUT}.asymmetry.csv", index=False)

    log("\n## V4 — RULE 8: a legal IS-only chooser on the adversarially deleted panels")
    log(f"   ladder t {TARGETS} x h {THRESH}; IS <= {IS_END} picks, OOS >= {OOS_START} read ONCE")
    log(f"     {'panel':>6} {'rule':>8} {'k':>3} {'n':>3} {'reach4b':>8} {'reach4a':>8} "
        f"{'oCAGR':>8} {'oSharpe':>8} {'oMaxDD':>8} {'t=0.10':>7} {'h=0.08':>7} {'cells4b':>8}")
    wsum = []
    for pname in W.panel.unique():
        for rule in ["NONE"] + RULES:
            for k in ([0] if rule == "NONE" else KS):
                g = W[(W.panel == pname) & (W.rule == rule) & (W.k == k)]
                if not len(g):
                    continue
                log(f"     {pname:>6} {rule:>8} {k:>3} {len(g):>3} {g.keep4b.mean():>8.3f} "
                    f"{g.keep4a_fix.mean():>8.3f} {g.oos_CAGR.mean():>8.2%} "
                    f"{g.oos_Sharpe.mean():>8.4f} {g.oos_MaxDD.mean():>8.2%} "
                    f"{(g.pick_t == CAND_T).mean():>7.3f} {(g.pick_h == CAND_H).mean():>7.3f} "
                    f"{g.n_cells_4b.mean():>8.1f}")
                wsum.append(dict(panel=pname, rule=rule, k=k, n=len(g),
                                 reach4b=float(g.keep4b.mean()),
                                 reach4a_fix=float(g.keep4a_fix.mean()),
                                 oos_CAGR=float(g.oos_CAGR.mean()),
                                 oos_Sharpe=float(g.oos_Sharpe.mean()),
                                 oos_MaxDD=float(g.oos_MaxDD.mean()),
                                 pick_t_cand=float((g.pick_t == CAND_T).mean()),
                                 pick_h_cand=float((g.pick_h == CAND_H).mean()),
                                 n_cells_4b=float(g.n_cells_4b.mean()),
                                 spy_oos_Sharpe=float(g.spy_oos_Sharpe.iloc[0]),
                                 spy_oos_CAGR=float(g.spy_oos_CAGR.iloc[0]),
                                 spy_oos_MaxDD=float(g.spy_oos_MaxDD.iloc[0]),
                                 live_oos_Sharpe=float(g.live_fix_oos_Sharpe.iloc[0]),
                                 live_oos_CAGR=float(g.live_fix_oos_CAGR.iloc[0]),
                                 live_oos_MaxDD=float(g.live_fix_oos_MaxDD.iloc[0])))
    pd.DataFrame(wsum).to_csv(f"{OUT}.wf_summary.csv", index=False)

    # ------------------------------------------------------------------------ verdict
    b = D[(D.panel == "B136")]
    adv = b[b.rule.isin(["BEST", "BEST_IS"])]
    n_pass = int(adv.keep4b.sum())
    n_tot = len(adv)
    early = adv[adv.k <= 10]
    log("\n## VERDICT (pre-stated rules)")
    log(f"   V1 B136 adversarial 4b: {n_pass} of {n_tot} rungs keep 4b "
        f"(FULL legs AND OOS); k <= 10 rungs: {int(early.keep4b.sum())} of {len(early)}")
    if n_pass == n_tot:
        v1 = "ROBUST — the 4b pass is not a winner-concentration artefact"
    elif int(early.keep4b.sum()) < len(early):
        v1 = "KILL the unqualified 4b claim — it breaks at k <= 10 in the survivorship direction"
    else:
        brk = adv[~adv.keep4b]
        v1 = ("PARTIAL — breaks first at " +
              ", ".join(f"{r.rule} k={r.k} ({r.bind})" for _, r in brk.head(3).iterrows()))
    log(f"   V1 -> {v1}")
    log(f"   V2 B136 adversarial 4a: fixed bar {int(adv.keep4a_fix.sum())} of {n_tot}, "
        f"matched bar {int(adv.keep4a_mat.sum())} of {n_tot}")
    fb = adv[~adv.keep4b]
    log(f"   V3 binding legs over failing adversarial rungs: "
        f"{dict(fb.bind.value_counts()) if len(fb) else 'none failed'}")
    wb = W[(W.panel == "B136") & (W.rule.isin(["BEST", "BEST_IS"]))]
    log(f"   V4 rule-8 reach on B136 adversarial panels: 4b {int(wb.keep4b.sum())} of {len(wb)}, "
        f"mean OOS {wb.oos_CAGR.mean():.2%} / {wb.oos_Sharpe.mean():.4f} / "
        f"{wb.oos_MaxDD.mean():.2%}")
    A = pd.DataFrame(asym)
    log(f"   V5 BEST inside the RANDOM Sharpe band: "
        f"{int(A.best_inside_random_band.sum())} of {len(A)} (panel, k) rungs")

    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    log(f"\nwrote {OUT}.books.csv.gz / .walkforward.csv / .summary.csv / .asymmetry.csv / "
        f".wf_summary.csv / .gates.csv / .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
