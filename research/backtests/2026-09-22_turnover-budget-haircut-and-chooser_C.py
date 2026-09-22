#!/usr/bin/env python3
"""Idea 2087 (lane C, 2026-09-22) — DOES THE 1795 TURNOVER-BUDGET KEEP-CANDIDATE SURVIVE A
POINT-IN-TIME-SHAPED ADMISSION HAIRCUT AND A SECOND CHOOSER?

THE DEFECT THIS PRICES.  Idea 1795 (lane cloud, 2026-09-22) left the record's newest 4b
KEEP-candidate: `U56, equal-weight, g = clip(t/sigma20, 0, 1) capped at 1.00, MONTHLY trade,
TURNOVER BUDGET B = 5.0 turns/yr, t = 0.12`, FULL 14.07% / 1.251 / -15.90%, OOS 15.40% /
1.357 / -15.90%, reached by the legal IS-only IS_LEGS chooser.  It is robust to cost 0-50 bps,
to one extra day of lag and to both dial neighbours.  Two exposures it was never priced against:

  (1) ADMISSION.  The U56 panel is a CURRENT-constituent 56-name list.  A point-in-time investor
      in 2009 held a DIFFERENT 56 names.  The candidate's whole DD leg has 4.33 pp of margin
      (-15.90% against the -20.23% cap) and its CAGR floor 3.49 pp; neither has ever been
      exposed to the name set moving.
  (2) CHOOSER.  Exactly TWO choosers were run (IS_SHARPE, IS_LEGS) and only ONE reached the
      cell.  A candidate reachable by one chooser out of two is one chooser away from being
      hindsight.

WHAT IS PRICED (two arms, both required).
  ARM A (CELL SURVIVAL).  The PUBLISHED cell is re-priced on random admission haircuts of the
  panel: at each depth `d` the panel drops `round(d * 55)` of its 55 single names (SPY is
  retained in every draw — it is also the benchmark, so dropping it would confound the
  contrast; a reported control at d = 0.20 drops SPY too).  Many independent seeded draws.
  The exposure scalar sigma20 is RE-ESTIMATED on the surviving names, as a real investor on a
  smaller list would.  Reported: the share of draws where the cell still clears 4b FULL+OOS,
  the distribution of both binding margins, and which leg fails when it fails.
  ARM B (CHOOSER REACH).  On EVERY draw the whole (t x B) grid is re-priced and SEVEN legal
  IS-only choosers pick a cell on 2009-2016 rows alone; 2017-2026 is read exactly once
  (PROTOCOL rule 8).  Reported: the share of (draw, chooser) pairs whose pick clears 4b
  FULL+OOS, per chooser and per depth, and how often each chooser lands on the published cell.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  CELL SURVIVAL.  The published cell clears 4b FULL+OOS at 10 bps in MORE THAN HALF of the
      draws at EVERY depth d <= 0.20.  Triggered -> the candidate is admission-robust in level.
  V2  SECOND CHOOSER.  On the UNDAMAGED panel (d = 0), STRICTLY MORE THAN ONE of the seven
      choosers reaches a cell clearing 4b FULL+OOS.  Not triggered -> the candidate is a
      one-chooser artefact.
  V3  JOINT.  Pooled over every (draw, chooser) pair at 10 bps across all haircut depths, the
      4b FULL+OOS share exceeds 0.50.
  V4  BASE RATE.  That joint share exceeds the record's committed zero-signal RAND 4b base rate
      (0.0360 at 10 bps, idea 907 lane B).  Not triggered -> the family is indistinguishable
      from noise and NOTHING here is a capital finding.
  V5  NOT-A-KNIFE-EDGE.  The published cell keeps its 4b verdict under ONE EXTRA DAY of
      execution lag (t+2) in more than half of the draws at d = 0.10.
  CAPITAL.  V1 AND V2 AND V3 AND V4 all triggered -> the 1795 candidate is REAFFIRMED as a
  KEEP-4b candidate under admission haircuts and a widened chooser set, and a memo is written.
  Any one of them failing -> the candidate is DOWNGRADED (PARK), with the exact failing share
  published.  Path 4a is scored at every cell too, against a live RULES v2 recomputed on the
  SAME surviving names (a matched 4a comparison, not the undamaged book's).

DIALS.  EXACTLY TWO are tuned: HAIRCUT DEPTH `d` in {0.05, 0.10, 0.20, 0.30} and the CHOOSER
SET (seven legal IS-only rules).  REPORTED, NOT TUNED: the candidate's own two dials TARGET
`t` in {0.08, 0.10, 0.12, 0.16, 0.20} and BUDGET `B` in {0.5, 1.0, 1.5, 2.0, 3.0, 5.0} (the
1795 ladders, unchanged); COST {0, 10, 25, 50} bps; TRADE cadence M (the candidate's own);
PANEL U56 (the candidate's own) with B136 as a reported replication arm; the sigma convention
FIXED at the standing memo's (L = 20, d = 0).  Every grid point is published (`.grid.csv.gz`).

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00);
rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea,
deterministic, standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP — READ THIS BEFORE THE NUMBERS.  U56 and B136 are CURRENT-constituent lists.  A
RANDOM deletion haircut is a LOWER BOUND on point-in-time damage, not an estimate of it: it
removes winners and losers in the same proportion the current list carries, whereas a true
point-in-time panel would ADD names that later failed or were acquired.  So a candidate that
survives this test has cleared a necessary condition, not a sufficient one, and every CAGR and
drawdown LEVEL below is still optimistic.  This is stated as a limit of the test, not a caveat
to be argued away.  The SPY bars are NOT haircut (SPY buy-and-hold is the same benchmark in
every draw); the live RULES v2 4a comparand IS recomputed on each draw's surviving names.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-22_turnover-budget-haircut-and-chooser_C.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG = "2026-09-22", "turnover-budget-haircut-and-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]              # 1795's ladder, reported not tuned
BUDGETS = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]              # 1795's ladder, reported not tuned
T_TRADE = "M"                                          # the candidate's own trade cadence
PUB_T, PUB_B = 0.12, 5.0                               # THE PUBLISHED CELL
DEPTHS = [0.05, 0.10, 0.20, 0.30]                      # TUNED DIAL 1
NDRAW = {"U56": 100, "B136": 30}                       # draws per depth, per panel
SEED0 = 2087
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SIG_L, SIG_D = 20, 0
WIN = 252                                              # budget accounting window (trading days)
RAND_BASE_RATE = 0.0360                                # idea 907 lane B, committed, 10 bps

# the committed 1795 candidate numbers this run must reproduce at d = 0 (LEADERBOARD 2026-09-22)
PUB_CAND = dict(CAGR=0.1407, Sharpe=1.251, MaxDD=-0.1590, oCAGR=0.1540, oSharpe=1.357,
                oMaxDD=-0.1590)

CHOOSERS = ["IS_SHARPE", "IS_LEGS", "IS_CALMAR", "IS_MINMARG", "IS_CAGRSLACK", "IS_DD",
            "CELL_ALPHA"]

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


# ----------------------------------------------------------------------------- book machinery
def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    """Annualised L-day realised vol of the UNLEVERED equal-weight portfolio of the SURVIVING
    names through close t-d.  (L, d) = (20, 0) is the standing VOLTGT memo's convention."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


def bt_budget(px_ret, W0, g0, mT, B):
    """1795's TURNOVER-BUDGETED refresh, copied unchanged.  The refresh TRIGGER is R = D (the
    scalar is re-read whenever it has moved) but a refresh executes only while trailing-`WIN`-day
    realised turnover plus the refresh's own cost stays within the annual budget `B` turns/yr.
    Mandatory trade-cadence re-spreads always execute and are charged against the same budget."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    spent = 0.0
    for i in range(n):
        if i >= WIN:
            spent -= turn[i - WIN]
        if i == 0:
            g_eff = g0[i]
            nref += 1
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            spent += turn[i]
            cur = new
        else:
            if mT[i]:
                new = W0[i] * g0[i]
                c_ref = np.abs(new - cur).sum()
                if spent + c_ref <= B:
                    g_eff = g0[i]
                else:
                    new = W0[i] * g_eff
                    c_ref = np.abs(new - cur).sum()
                turn[i] = c_ref
                spent += c_ref
                cur = new
            elif abs(g0[i] - cur.sum()) > 0.0:
                s = cur.sum()
                if s > 0:
                    new = cur * (g0[i] / s)
                    c_ref = np.abs(new - cur).sum()
                    if spent + c_ref <= B:
                        g_eff = g0[i]
                        turn[i] = c_ref
                        spent += c_ref
                        cur = new
                        nref += 1
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


class Book:
    """One HAIRCUT PANEL.  `cols` is the surviving name set; everything (equal weight, sigma,
    the book) is rebuilt on it.  `delay` = 1 is PROTOCOL rule 2; 2 is the extra-lag stress."""

    def __init__(self, px, cols, delay=1):
        self.index = px.index
        self.delay = delay
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((delay, ew.shape[1])), ew[:-delay]])
        self.SIG = panel_sigma(px, cols)
        m = np.asarray(rebalance_mask(px.index, T_TRADE).values, bool)
        self.mT = np.concatenate([[False], m[:-1]])

    def g_of(self, tgt):
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        return np.concatenate([np.zeros(self.delay), g[:-self.delay]])

    def run(self, tgt, B):
        r, t, gs, nref = bt_budget(self.R, self.W, self.g_of(tgt), self.mT, B)
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


LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]


def binding(mar):
    bad = [k for k in LEGS if not (mar[k] > 0)]
    return ("|".join(bad) if bad else "none", len(bad))


def spy_bars(px, st):
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
    h1, h2 = halves(spy)
    ih1, ih2 = halves(spy.loc[:IS_END])
    return dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                h1=h1, h2=h2, ish1=ih1, ish2=ih2)


def live_bars(px, cols, st):
    """Live RULES v2 on the SAME surviving names — the matched 4a comparand for this draw."""
    lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
    lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
    lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
    out = {}
    for c in COSTS:
        r = net(lr, lt, c)
        h1, h2 = halves(r)
        out[c] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]), h1=h1, h2=h2,
                      turn=float(lt.sum() / (len(lr) / 252.0)))
    return out


def score_cell(r0, t0, gs, st, S, LV):
    """Every 4b / 4a leg at every cost rung for one (t, B) book on one draw."""
    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
    yrs = len(r0) / 252.0
    out = []
    for c in COSTS:
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
        lv = LV[c]
        k4a = (h1 > lv["h1"] and h2 > lv["h2"] and mf["MaxDD"] >= lv["full"]["MaxDD"])
        k4ao = (mo["Sharpe"] > lv["oos"]["Sharpe"] and mo["MaxDD"] >= lv["oos"]["MaxDD"])
        # IS-only quantities: everything a legal chooser is allowed to read
        is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
                   + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
                   + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
        is_minmarg = min(ih1 - S["ish1"], ih2 - S["ish2"],
                         mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                         mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])
        out.append(dict(
            cost=c, turn_py=float(t0.sum() / yrs), gross_mean=float(gs.mean()),
            gross_max=float(gs.max()),
            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
            is_legs=is_legs, is_minmarg=float(is_minmarg),
            is_calmar=float(mi["CAGR"] / abs(mi["MaxDD"])) if mi["MaxDD"] < 0 else np.nan,
            is_cagrslack=float(mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"]),
            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
            **{k: float(v) for k, v in mar.items()},
            bind=bl, n_fail=nbad,
            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
            keep4a=k4a, keep4a_oos=k4ao))
    return out


def pick(sub, chooser):
    """A LEGAL IS-ONLY chooser: it may read only 2009-2016 columns.  Deterministic tie-break on
    (target, budget) ascending, so no chooser can win on ordering luck."""
    s = sub.sort_values(["target", "budget"]).reset_index(drop=True)
    if chooser == "IS_SHARPE":
        key = s.is_Sharpe.values
    elif chooser == "IS_LEGS":
        key = s.is_legs.values * 1e6 + s.is_Sharpe.values
    elif chooser == "IS_CALMAR":
        key = np.nan_to_num(s.is_calmar.values, nan=-1e9)
    elif chooser == "IS_MINMARG":
        key = s.is_minmarg.values
    elif chooser == "IS_CAGRSLACK":
        key = s.is_cagrslack.values
    elif chooser == "IS_DD":
        key = s.is_MaxDD.values                       # shallowest IS drawdown
    elif chooser == "CELL_ALPHA":                     # no-information control
        return s.loc[s.cell.astype(str).sort_values().index[0]]
    else:
        raise ValueError(chooser)
    return s.iloc[int(np.argmax(key))]


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2087 (lane C, {DATE}) — does the 1795 TURNOVER-BUDGET KEEP-candidate survive a "
        f"POINT-IN-TIME-SHAPED ADMISSION HAIRCUT and a SECOND CHOOSER?")
    log(f"# TUNED DIALS (2): HAIRCUT DEPTH d {DEPTHS}; CHOOSER SET {CHOOSERS}.")
    log(f"# REPORTED, NOT TUNED: t {TARGETS} x B {BUDGETS} (1795's own ladders), cost {COSTS} "
        f"bps, trade cadence {T_TRADE}, panel U56 (candidate's own) + B136 (replication), "
        f"sigma FIXED at (L={SIG_L}, d={SIG_D}), budget window {WIN}d, warm-up {WARMUP}, "
        f"IS <= {IS_END}, OOS >= {OOS_START} read ONCE.")
    log(f"# published cell under test: U56, T={T_TRADE}, t={PUB_T}, B={PUB_B}")

    PANELS = [("U56", load_universe().dropna(how="all").ffill()),
              ("B136", load_universe(broad=True).dropna(how="all").ffill())]

    grid_rows, ch_rows, cell_rows = [], [], []
    g_repro = np.nan
    g_gross = 0.0
    g_zero = np.nan
    uniq = {}

    for pname, px in PANELS:
        allc = list(px.columns)
        names = [c for c in allc if c != "SPY"]
        st = px.index[WARMUP]
        S = spy_bars(px, st)
        log(f"\n## {pname}: {len(allc)} columns ({len(names)} single names + SPY), "
            f"{px.index[0].date()} -> {px.index[-1].date()} ({len(px)} rows, "
            f"{len(px)/252:.1f}y); book window from {st.date()}")
        log(f"   SPY bars  FULL {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}   OOS {S['oos']['CAGR']:.2%} / "
            f"{S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:.2%}")
        log(f"   4b bars   DD cap {DD_CAP*S['full']['MaxDD']:.2%} (FULL), "
            f"{DD_CAP*S['oos']['MaxDD']:.2%} (OOS); CAGR floor "
            f"{CAGR_FLOOR*S['full']['CAGR']:.2%} (FULL), "
            f"{CAGR_FLOOR*S['oos']['CAGR']:.2%} (OOS)")

        # ------------------------------------------------- the draw list: d = 0 plus haircuts
        draws = [(0.0, 0, tuple(sorted(allc)), "keepSPY")]
        for d in DEPTHS:
            k = int(round(d * len(names)))
            seen = set()
            for j in range(NDRAW[pname]):
                rng = np.random.default_rng(SEED0 + int(d * 1000) * 1009 + j)
                keep = tuple(sorted(list(rng.choice(names, size=len(names) - k,
                                                    replace=False)) + ["SPY"]))
                seen.add(keep)
                draws.append((d, j, keep, "keepSPY"))
            uniq[(pname, d)] = (len(seen), NDRAW[pname], k)
        # reported control (not a tuned rung): d = 0.20 with SPY itself droppable
        for j in range(NDRAW[pname]):
            d = 0.20
            k = int(round(d * len(allc)))
            rng = np.random.default_rng(SEED0 + 777 * 1009 + j)
            keep = tuple(sorted(rng.choice(allc, size=len(allc) - k, replace=False)))
            draws.append((d, j, keep, "dropSPY"))

        log(f"   {len(draws)} panels to price ({sum(1 for x in draws if x[3]=='keepSPY')} "
            f"keep-SPY incl. the undamaged one, "
            f"{sum(1 for x in draws if x[3]=='dropSPY')} SPY-droppable control)")

        for (d, j, keep, arm) in draws:
            cols = list(keep)
            LV = live_bars(px, cols, st)
            bk = Book(px, cols, delay=1)
            bk2 = Book(px, cols, delay=2)
            per_cost = {c: [] for c in COSTS}
            for tgt in TARGETS:
                for B in BUDGETS:
                    r0, t0, gs, nref = bk.run(tgt, B)
                    g_gross = max(g_gross, float(gs.loc[st:].max()))
                    for row in score_cell(r0, t0, gs, st, S, LV):
                        rec = dict(panel=pname, depth=d, draw=j, arm=arm, n_names=len(cols),
                                   target=tgt, budget=B, cell=f"t={tgt:.2f}|B={B:.1f}",
                                   refresh_py=nref / (len(px) / 252.0), **row)
                        per_cost[row["cost"]].append(rec)
                        grid_rows.append(rec)
            # ---- ARM A: the PUBLISHED cell on this draw, plus its t+2 lag stress
            pubrow = [r for r in per_cost[COST0]
                      if r["target"] == PUB_T and r["budget"] == PUB_B][0]
            r2, t2, gs2, _ = bk2.run(PUB_T, PUB_B)
            s2 = [x for x in score_cell(r2, t2, gs2, st, S, LV) if x["cost"] == COST0][0]
            if d == 0.0:
                g_repro = max(abs(pubrow["CAGR"] - PUB_CAND["CAGR"]),
                              abs(pubrow["Sharpe"] - PUB_CAND["Sharpe"]),
                              abs(pubrow["MaxDD"] - PUB_CAND["MaxDD"]),
                              abs(pubrow["oos_CAGR"] - PUB_CAND["oCAGR"]),
                              abs(pubrow["oos_Sharpe"] - PUB_CAND["oSharpe"]),
                              abs(pubrow["oos_MaxDD"] - PUB_CAND["oMaxDD"])) \
                    if pname == "U56" else g_repro
                if pname == "U56":
                    g_zero = 0.0 if len(cols) == len(allc) else 1.0
            cell_rows.append(dict(panel=pname, depth=d, draw=j, arm=arm, n_names=len(cols),
                                  **{k: pubrow[k] for k in
                                     ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "oos_CAGR",
                                      "oos_Sharpe", "oos_MaxDD", "turn_py", "L1_H1", "L2_H2",
                                      "L3_OOS", "L4_DD", "L5_CAGR", "bind", "n_fail",
                                      "keep4b_full", "keep4b_oos", "keep4b", "keep4a")},
                                  keep4b_t2=s2["keep4b"], oos_Sharpe_t2=s2["oos_Sharpe"],
                                  MaxDD_t2=s2["MaxDD"]))
            # ---- ARM B: seven legal IS-only choosers, 2017-2026 read once
            sub = pd.DataFrame(per_cost[COST0])
            for ch in CHOOSERS:
                p = pick(sub, ch)
                ch_rows.append(dict(panel=pname, depth=d, draw=j, arm=arm, n_names=len(cols),
                                    chooser=ch, cell=p.cell, target=p.target, budget=p.budget,
                                    is_Sharpe=p.is_Sharpe, is_legs=p.is_legs,
                                    CAGR=p.CAGR, Sharpe=p.Sharpe, MaxDD=p.MaxDD,
                                    oos_CAGR=p.oos_CAGR, oos_Sharpe=p.oos_Sharpe,
                                    oos_MaxDD=p.oos_MaxDD, turn_py=p.turn_py,
                                    spy_oos_CAGR=S["oos"]["CAGR"],
                                    spy_oos_Sharpe=S["oos"]["Sharpe"],
                                    spy_oos_MaxDD=S["oos"]["MaxDD"],
                                    live_oos_CAGR=LV[COST0]["oos"]["CAGR"],
                                    live_oos_Sharpe=LV[COST0]["oos"]["Sharpe"],
                                    live_oos_MaxDD=LV[COST0]["oos"]["MaxDD"],
                                    is_published_cell=bool(p.target == PUB_T
                                                           and p.budget == PUB_B),
                                    keep4b_full=p.keep4b_full, keep4b_oos=p.keep4b_oos,
                                    keep4b=p.keep4b, keep4a=p.keep4a, bind=p.bind))
        log(f"   priced {len(draws)} panels x {len(TARGETS)*len(BUDGETS)} cells "
            f"x {len(COSTS)} cost rungs")

    G = pd.DataFrame(grid_rows)
    C = pd.DataFrame(cell_rows)
    W = pd.DataFrame(ch_rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    C.to_csv(f"{OUT}.cellsurvival.csv", index=False)
    W.to_csv(f"{OUT}.choosers.csv", index=False)

    # -------------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PANELS[0][1])/252:.1f}y", ">= 10",
         len(PANELS[0][1]) / 252 >= 10)
    gate("G1 d=0 reproduces the committed 1795 candidate (FULL + OOS, U56 t=0.12 B=5.0)",
         f"max|d| = {g_repro:.3e}", "< 1e-3", g_repro < 1e-3)
    gate("G2 the d=0 draw drops NOTHING (identity haircut)", f"{g_zero:.0f} names dropped",
         "== 0", g_zero == 0.0)
    gate("G3 gross never exceeds 1.00 (no leverage, any draw)", f"{g_gross:.6f}", "<= 1.0",
         g_gross <= 1.0 + 1e-9)
    ok_u = all(v[0] == v[1] for k, v in uniq.items())
    gate("G4 every haircut draw is a DISTINCT name set",
         "; ".join(f"{k[0]} d={k[1]:.2f}: {v[0]}/{v[1]} unique, {v[2]} dropped"
                   for k, v in uniq.items()),
         "all unique", ok_u)
    # G5: the cost identity is exact by construction (net() is applied to one gross run)
    chk = G[(G.panel == "U56") & (G.depth == 0.0) & (G.target == PUB_T) & (G.budget == PUB_B)]
    gate("G5 all four cost rungs scored off ONE gross run (turnover identical across rungs)",
         f"{chk.turn_py.nunique()} distinct turn_py over {len(chk)} rungs", "== 1",
         chk.turn_py.nunique() == 1)

    # ------------------------------------------------ ARM A: cell survival under the haircut
    log("\n## ARM A — DOES THE PUBLISHED CELL SURVIVE THE ADMISSION HAIRCUT?")
    log(f"   (U56, T={T_TRADE}, t={PUB_T}, B={PUB_B}, {COST0} bps, 4b FULL+OOS)")
    for pname in ("U56", "B136"):
        base = C[(C.panel == pname) & (C.depth == 0.0)]
        if len(base):
            b = base.iloc[0]
            log(f"   {pname} d=0.00 (undamaged, n={int(b.n_names)}): FULL {b.CAGR:.2%} / "
                f"{b.Sharpe:.4f} / {b.MaxDD:.2%}   OOS {b.oos_CAGR:.2%} / "
                f"{b.oos_Sharpe:.4f} / {b.oos_MaxDD:.2%}   4b={int(b.keep4b)} "
                f"4a={int(b.keep4a)}  bind={b.bind}")
        for arm in ("keepSPY", "dropSPY"):
            for d in DEPTHS:
                s = C[(C.panel == pname) & (C.depth == d) & (C.arm == arm)]
                if not len(s):
                    continue
                tag = "" if arm == "keepSPY" else "  [SPY-droppable control]"
                log(f"   {pname} d={d:.2f} {arm:<8} n={len(s):3d} draws, "
                    f"{int(s.n_names.iloc[0])} names: 4b FULL+OOS "
                    f"{s.keep4b.mean():.3f} ({int(s.keep4b.sum())}/{len(s)}); "
                    f"4b FULL {s.keep4b_full.mean():.3f}, 4b OOS {s.keep4b_oos.mean():.3f}, "
                    f"4a {s.keep4a.mean():.3f}; CAGR {s.CAGR.mean():.2%} "
                    f"[{s.CAGR.quantile(.05):.2%},{s.CAGR.quantile(.95):.2%}], "
                    f"MaxDD {s.MaxDD.mean():.2%} "
                    f"[{s.MaxDD.quantile(.05):.2%},{s.MaxDD.quantile(.95):.2%}], "
                    f"OOS S {s.oos_Sharpe.mean():.4f}{tag}")
                bc = s[~s.keep4b].bind.value_counts()
                if len(bc):
                    log(f"      failing legs: " + ", ".join(f"{k} x{v}" for k, v in
                                                            bc.items()))
    cu = C[(C.panel == "U56") & (C.arm == "keepSPY") & (C.depth > 0)]
    v1 = all(cu[(cu.depth == d)].keep4b.mean() > 0.5 for d in DEPTHS if d <= 0.20)
    log(f"   V1 (cell clears 4b in > half of draws at EVERY depth d <= 0.20): "
        f"{'TRIGGERED' if v1 else 'NOT TRIGGERED'}")

    # -------------------------------------------- ARM B: rule-8 chooser reach, all seven rules
    log("\n## ARM B — RULE-8 WALK-FORWARD: seven legal IS-only choosers, 2017-2026 read ONCE")
    log("   d = 0.00, the UNDAMAGED panel (this is the 'second chooser' question, V2):")
    for pname in ("U56", "B136"):
        for _, r in W[(W.panel == pname) & (W.depth == 0.0)].iterrows():
            log(f"     {pname:<5} {r.chooser:<13} pick {r.cell:<16} IS S={r.is_Sharpe:.4f} "
                f"legs={int(r.is_legs)}  ->  OOS {r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / "
                f"{r.oos_MaxDD:7.2%}   4b_full={int(r.keep4b_full)} "
                f"4b_oos={int(r.keep4b_oos)} 4b={int(r.keep4b)} 4a={int(r.keep4a)}  "
                f"pub_cell={int(r.is_published_cell)}  bind={r.bind}")
    n_reach = int(W[(W.panel == "U56") & (W.depth == 0.0)].keep4b.sum())
    v2 = n_reach > 1
    log(f"   V2 (> 1 of {len(CHOOSERS)} choosers reaches a 4b FULL+OOS cell on the UNDAMAGED "
        f"U56 panel): {n_reach} reach -> {'TRIGGERED' if v2 else 'NOT TRIGGERED'}")

    log("\n   Under the haircut, per chooser (keep-SPY arms, all depths pooled):")
    for pname in ("U56", "B136"):
        for ch in CHOOSERS:
            s = W[(W.panel == pname) & (W.chooser == ch) & (W.arm == "keepSPY") & (W.depth > 0)]
            if not len(s):
                continue
            log(f"     {pname:<5} {ch:<13} 4b {s.keep4b.mean():.3f} "
                f"({int(s.keep4b.sum())}/{len(s)})  4b_full {s.keep4b_full.mean():.3f}  "
                f"4b_oos {s.keep4b_oos.mean():.3f}  4a {s.keep4a.mean():.3f}  "
                f"lands on the published cell {s.is_published_cell.mean():.3f}  "
                f"mean OOS {s.oos_CAGR.mean():.2%}/{s.oos_Sharpe.mean():.4f}/"
                f"{s.oos_MaxDD.mean():.2%}")
    log("\n   Under the haircut, per depth (U56, keep-SPY, all seven choosers pooled):")
    for d in DEPTHS:
        s = W[(W.panel == "U56") & (W.depth == d) & (W.arm == "keepSPY")]
        log(f"     d={d:.2f}  4b {s.keep4b.mean():.3f} ({int(s.keep4b.sum())}/{len(s)})  "
            f"4a {s.keep4a.mean():.3f}  published-cell rate {s.is_published_cell.mean():.3f}")

    wu = W[(W.panel == "U56") & (W.arm == "keepSPY") & (W.depth > 0)]
    share = float(wu.keep4b.mean())
    v3 = share > 0.50
    v4 = share > RAND_BASE_RATE
    log(f"\n   V3 (pooled (draw, chooser) 4b FULL+OOS share > 0.50): {share:.4f} "
        f"({int(wu.keep4b.sum())}/{len(wu)}) -> {'TRIGGERED' if v3 else 'NOT TRIGGERED'}")
    log(f"   V4 (that share exceeds the committed zero-signal RAND base rate "
        f"{RAND_BASE_RATE:.4f}): -> {'TRIGGERED' if v4 else 'NOT TRIGGERED'}")

    # -------------------------------------------------------------------- V5: extra lag
    log("\n## V5 — ONE EXTRA DAY OF EXECUTION LAG (decided t, applied t+2), published cell")
    for pname in ("U56", "B136"):
        for d in [0.0] + DEPTHS:
            s = C[(C.panel == pname) & (C.depth == d) & (C.arm == "keepSPY")]
            if not len(s):
                continue
            log(f"   {pname} d={d:.2f}: 4b at t+1 {s.keep4b.mean():.3f}, at t+2 "
                f"{s.keep4b_t2.mean():.3f}; keeps its verdict "
                f"{(s.keep4b == s.keep4b_t2).mean():.3f}")
    s10 = C[(C.panel == "U56") & (C.depth == 0.10) & (C.arm == "keepSPY")]
    v5 = bool(s10.keep4b_t2.mean() > 0.5)
    log(f"   V5: {'TRIGGERED' if v5 else 'NOT TRIGGERED'}")

    # -------------------------------------------------------------------- cost ladder
    log("\n## REPORTED, NOT TUNED — THE COST LADDER on the published cell (U56, keep-SPY)")
    gp = G[(G.panel == "U56") & (G.target == PUB_T) & (G.budget == PUB_B) & (G.arm == "keepSPY")]
    for c in COSTS:
        for d in [0.0] + DEPTHS:
            s = gp[(gp.cost == c) & (gp.depth == d)]
            if not len(s):
                continue
            log(f"   {c:>2} bps  d={d:.2f}  4b {s.keep4b.mean():.3f} "
                f"({int(s.keep4b.sum())}/{len(s)})  CAGR {s.CAGR.mean():.2%}  "
                f"MaxDD {s.MaxDD.mean():.2%}  OOS S {s.oos_Sharpe.mean():.4f}")

    # -------------------------------------------------------------------- whole-grid 4b census
    log("\n## WHOLE-GRID 4b / 4a CENSUS at 10 bps (every published cell, every draw)")
    for pname in ("U56", "B136"):
        for d in [0.0] + DEPTHS:
            s = G[(G.panel == pname) & (G.cost == COST0) & (G.depth == d)
                  & (G.arm == "keepSPY")]
            if not len(s):
                continue
            log(f"   {pname} d={d:.2f}: 4b FULL+OOS {s.keep4b.mean():.4f} "
                f"({int(s.keep4b.sum())}/{len(s)} cells), 4a {s.keep4a.mean():.4f}, "
                f"binding leg when it fails: "
                f"{s[~s.keep4b].bind.value_counts().head(3).to_dict()}")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log("\n## VERDICTS")
    log(f"   V1 published cell survives the haircut at every d <= 0.20 ... "
        f"{'YES' if v1 else 'NO'}")
    log(f"   V2 more than one chooser reaches it on the clean panel ..... "
        f"{'YES' if v2 else 'NO'}")
    log(f"   V3 pooled (draw, chooser) 4b share > 0.50 .................. "
        f"{'YES' if v3 else 'NO'}  ({share:.4f})")
    log(f"   V4 that share beats the zero-signal RAND base rate ......... "
        f"{'YES' if v4 else 'NO'}")
    log(f"   V5 the cell keeps its 4b verdict at t+2 .................... "
        f"{'YES' if v5 else 'NO'}")
    cap = v1 and v2 and v3 and v4
    verdict = ("REAFFIRMED as a KEEP-4b candidate" if cap
               else "DOWNGRADED (PARK) - see the failing rule above")
    log(f"   CAPITAL: the 1795 candidate is {verdict} under admission haircuts and a "
        f"widened chooser set.")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
