#!/usr/bin/env python3
"""Idea 2026 (lane C, 2026-09-20) — CAN THE DRIFT THRESHOLD BE SET WITHOUT THE IS WINDOW?

THE DEFECT THIS PRICES.  Idea 1799's KEEP-4b candidate re-reads the exposure scalar
`g_t = clip(t / sigma20_panel, 0, 1)` only when the book's HELD gross has drifted from it by more
than a CONSTANT `h` (its cell: U56, t = 0.16, h = 0.12, monthly re-spread, OOS 16.36% / 1.2810 /
-18.16%).  Its own memo point 7 names the weakness: the legal IS-only chooser walks to the LAZIEST
rung of whatever `h` ladder it is given (18 of 24 picks on the top two rungs), so lengthening the
ladder from 0.12 to 0.25 moves the pick and drops the U56 weekly arm from PASS to FAIL.  What 1799
certified is the TRIGGER, not the number.  A constant `h` is also dimensionally odd: 0.12 of gross
means one thing when `g_t` sits at 0.95 and quite another when a vol spike has driven it to 0.20.

THE FIX TESTED HERE.  Three LADDER-FREE thresholds that spend NO in-sample statistic because they
are set by the scalar's own scale, re-read every day:

    SDMULT   h_t = k * SD_20(g_t)          (a fixed multiple of the scalar's own 20-day SD)
    FRACG    h_t = f * g_t                 (a fixed FRACTION of the scalar in force)
    ASYMG    h_up = f * g_t, h_dn = f * g_t / 4   (two-sided: TIGHT on the way DOWN, LOOSE up)

plus ASYMH (`h_up = h`, `h_dn = h / 4`), the asymmetric twin of the incumbent constant, so that the
asymmetry can be read at a FIXED base as well as a scale-free one.  The incumbent FIXH ladder and
the whole CALENDAR ladder `R in {D,W,M,Q}` are the comparands, priced on the same tape, the same
names, the same trade cadence.  `SDMULT k = 0`, `FRACG f = 0` and `FIXH h = 0` all reproduce
`R = D` exactly (gate G4).

PRE-STATED CONSTANTS (fixed HERE, before the run; never adjusted afterwards).  The headline arm
spends ZERO in-sample statistics:

    SDMULT  k* = 1.0        one SD of the scalar's own recent motion
    FRACG   f* = 0.10       re-read when the book's exposure is a tenth off its target
    ASYMG   f* = 0.10       same, with the 4:1 down/up ratio
    ASYMH   h* = 0.12       the standing memo's own constant, with the 4:1 ratio
    target  t* = 0.16       INHERITED from the standing VOLTGT memo; not chosen this run

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION (ZERO-IS REACH).  At 10 bps and t = t*, over the 6 arms (panel x
      trade cadence), at least one LADDER-FREE family's PRE-STATED constant clears 4b FULL *and*
      OOS on AT LEAST AS MANY arms as the incumbent FIXH family's legal IS-only picks do (best over
      the four choosers, i.e. generous to the incumbent).  Not triggered -> the ladder-free fix is
      KILLED as a repair for 1799's point 7.
  V2  SCALE INVARIANCE.  Across the 15 (panel x target) cells at each trade cadence, a pre-stated
      ladder-free threshold's realised REFRESH RATE has a strictly smaller coefficient of variation
      than fixed `h = 0.12`'s.  This is the mechanical content of "scale-free".
  V3  LADDER-LENGTH IMMUNITY.  1799's defect, measured: truncate each family's ladder to its first
      FOUR rungs and report the share of (arm x chooser) pairs whose PICK moves and whose OOS 4b
      VERDICT moves.  The pre-stated arm is immune by construction (0 by definition), which is
      reported for contrast and is not scored as a win.
  V4  ASYMMETRY.  At the same base scale, the asymmetric families (ASYMH vs FIXH, ASYMG vs FRACG)
      clear 4b on at least as many arms as their symmetric twins AND cut gross at least as deep
      through the 2020 crash at no more turnover.
  V5  CAPITAL.  Both KEEP paths are scored at EVERY cell.  Any cell clearing 4b FULL *and* OOS that
      is PRE-STATED (zero IS spend) or reached by a legal IS-only chooser is a KEEP-4b candidate;
      per idea 2022's committed caveat every such cell is additionally re-read on the 2020-crash-
      excised tape (2020-02-19 .. 2020-03-23) and that caveat is restated, not re-derived.

DIALS.  EXACTLY TWO are tuned, and only ever within one family: TARGET `t` x the family's own scale
rung (`h` for FIXH/ASYMH, `k` for SDMULT, `f` for FRACG/ASYMG, `R` for CAL).  No chooser ever
selects across families, across panels, across trade cadence or across cost.  The 4:1 asymmetry
ratio is PRE-STATED, not tuned.  REPORTED, NOT TUNED: TRADE cadence `T in {W, M}` (separate arms),
PANEL {U56, B136, SMALL}, COST {0, 10, 25, 50} bps.  The sigma convention is FIXED at the standing
memo's (L = 20, d = 0).  Every grid point is published (`.grid.csv.gz`).

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.
The THRESHOLD-RULE contrast is same-tape / same-names / same-grid with only the refresh trigger
moved, so it is first-order immune; the PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_ladder-free-drift-threshold_C.py
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

DATE, SLUG = "2026-09-20", "ladder-free-drift-threshold"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_STAR = 0.16                       # inherited from the standing VOLTGT memo
TRADES = ["W", "M"]
REFRESH = ["D", "W", "M", "Q"]
H_GRID = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]   # h = 0 is the G4 gate cell
K_GRID = [0.0, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0]                     # k = 0 is the G4 gate cell
F_GRID = [0.0, 0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50]               # f = 0 is the G4 gate cell
ASYM_A = 4.0                          # PRE-STATED down/up ratio, not tuned
K_STAR, F_STAR, H_STAR = 1.0, 0.10, 0.12
SD_L = 20
SIG_L, SIG_D = 20, 0
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
CRASH = ("2020-02-19", "2020-03-23")          # idea 2022's window, quoted not re-derived
TRUNC_N = 4                                   # V3 short-ladder length

FAMS = {"CAL": REFRESH, "FIXH": H_GRID, "ASYMH": [h for h in H_GRID if h > 0],
        "SDMULT": K_GRID, "FRACG": F_GRID, "ASYMG": [f for f in F_GRID if f > 0]}
LADDER_FREE = ["SDMULT", "FRACG", "ASYMG"]
PRESTATED = {"SDMULT": K_STAR, "FRACG": F_STAR, "ASYMG": F_STAR, "ASYMH": H_STAR}

# committed numbers this run must reproduce
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}
PUB_1799 = dict(CAGR=0.156208, Sharpe=1.24509, MaxDD=-0.181592,        # U56 t=.16 h=.12 T=M 10bps
                oCAGR=0.16359, oSharpe=1.28099, oMaxDD=-0.181592)

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
    return ([("U56", px56, [c for c in px56.columns]),
             ("B136", px136, [c for c in px136.columns]),
             (f"SMALL{len(small_cols)}", pxs, small_cols)], dropped)


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio through close
    t-d.  (L, d) = (20, 0) is the standing memo's convention (idea 1771 owns that surface)."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------------------ the two refresh runners
def bt_cal(px_ret, W0, g0, mT, mR):
    """CALENDAR refresh (idea 1767's two-schedule construction, verbatim).  `g_eff` is re-read on
    refresh days only; trade days re-spread the names to the scalar in force."""
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
    """DRIFT refresh with a TWO-SIDED, possibly TIME-VARYING threshold.  The scalar is re-read on
    day i iff the book's actual total exposure entering day i is more than `hup[i]` BELOW `g0[i]`
    (the book must gross UP) or more than `hdn[i]` ABOVE it (the book must gross DOWN).
    hup == hdn == 0 fires every day, i.e. R = D (gate G4); hup == hdn == h is 1799's `bt_drift`."""
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
    """Pre-shifted arrays for one panel, so every (t, T, family, rung) run is a single loop."""

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
        self._g, self._sd = {}, {}

    def g_of(self, tgt):
        if tgt not in self._g:
            g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
            self._g[tgt] = np.concatenate([[0.0], g[:-1]])
            # SD of the scalar's own recent motion, computed on the ALREADY-LAGGED scalar
            self._sd[tgt] = (pd.Series(self._g[tgt]).rolling(SD_L).std()
                             .fillna(0.0).values)
        return self._g[tgt]

    def sd_of(self, tgt):
        self.g_of(tgt)
        return self._sd[tgt]

    def thresholds(self, tgt, fam, rung):
        g0, n = self.g_of(tgt), len(self.R)
        if fam == "FIXH":
            return np.full(n, rung), np.full(n, rung)
        if fam == "ASYMH":
            return np.full(n, rung), np.full(n, rung / ASYM_A)
        if fam == "SDMULT":
            v = rung * self.sd_of(tgt)
            return v, v
        if fam == "FRACG":
            v = rung * g0
            return v, v
        if fam == "ASYMG":
            return rung * g0, rung * g0 / ASYM_A
        raise ValueError(fam)

    def run(self, tgt, T, fam, rung):
        g0 = self.g_of(tgt)
        if fam == "CAL":
            r, t, gs, nref = bt_cal(self.R, self.W, g0, self.masks[T], self.masks[rung])
        else:
            hu, hd = self.thresholds(tgt, fam, rung)
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


def cell_label(fam, rung):
    if fam == "CAL":
        return f"R={rung}"
    return {"FIXH": "h", "ASYMH": "hup", "SDMULT": "k", "FRACG": "f", "ASYMG": "f"}[fam] \
        + f"={rung:g}"


def score_cell(r0, t0, gs, nref, c, S, LV, nyears, st):
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
        cost=c, turn_py=float(t0.sum() / nyears),
        is_turn_py=float(t0.loc[:IS_END].sum() / (len(isr) / 252.0)),
        refresh_py=nref / (len(r0) / 252.0),
        gross_mean=float(gs.mean()), gross_mean_is=float(gs.loc[:IS_END].mean()),
        gross_min=float(gs.min()), gross_max=float(gs.max()),
        gross_crash_min=float(gs.loc[CRASH[0]:CRASH[1]].min()) if len(gs.loc[CRASH[0]:CRASH[1]])
        else np.nan,
        CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
        is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
        is_H1=ih1, is_H2=ih2, is_legs=is_legs,
        is_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
        oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
        **{k: float(v) for k, v in mar.items()},
        bind=bl, n_fail=nbad,
        keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
        keep4a=k4a, keep4a_oos=k4ao)


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2026 (lane C, {DATE}) — can the DRIFT THRESHOLD be set WITHOUT the IS window?")
    log(f"# families: CAL {REFRESH} | FIXH {H_GRID} | ASYMH (4:1) | SDMULT {K_GRID} | "
        f"FRACG {F_GRID} | ASYMG (4:1)")
    log(f"# tuned dials (2, within a family): TARGET t {TARGETS} x the family's own scale rung.  "
        f"reported, not tuned: TRADE T {TRADES}, PANEL, COST {COSTS} bps, asymmetry ratio "
        f"{ASYM_A:g}:1.  sigma FIXED at (L={SIG_L}, d={SIG_D}).")
    log(f"# PRE-STATED zero-IS constants: k*={K_STAR}, f*={F_STAR}, ASYMH h*={H_STAR}, "
        f"t*={TGT_STAR} (inherited).  warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows, BASE, BOOKS = [], {}, {}
    g1r = g1t = g2 = g3 = g4 = g5 = g9 = 0.0
    g4n = 0

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
        B = dict(start=st,
                 spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                          h1=halves(spy)[0], h2=halves(spy)[1],
                          ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1],
                                 turn=float(lt.sum() / (len(lr) / 252.0)))
        BASE[pname] = B
        L, S = B[f"live{COST0}"], B["spy"]
        log(f"   LIVE RULES v2 (W, {COST0}bps) {L['full']['CAGR']:.2%} / {L['full']['Sharpe']:.4f}"
            f" / {L['full']['MaxDD']:.2%}  (OOS {L['oos']['CAGR']:.2%} / {L['oos']['Sharpe']:.4f}"
            f" / {L['oos']['MaxDD']:.2%}), {L['turn']:.2f} turns/yr")
        log(f"   SPY                      {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}  (OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%})")

        # ---- G1 / G2: the calendar diagonal is engine.backtest --------------------------
        if pname in ("U56", "B136"):
            Gp = (TGT_STAR / bk.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            Wfull = (eq_weight(px, cols).mul(Gp, axis=0)).fillna(0.0)
            a, at, _, _ = bk.run(TGT_STAR, "W", "CAL", "W")
            b = engine_backtest(px, Wfull, cost_bps=0.0, freq="W")
            g1r = max(g1r, float(np.abs(a.values - b["returns"].values).max()))
            g1t = max(g1t, float(np.abs(at.values - b["turnover"].values).max()))
            for c in (10, 25):
                eb = engine_backtest(px, Wfull, cost_bps=float(c), freq="W")["returns"]
                g2 = max(g2, float(np.abs(net(a, at, c).values - eb.values).max()))

        # ---- the grid -------------------------------------------------------------------
        for tgt in TARGETS:
            for T in TRADES:
                cal_D = None
                for fam, ladder in FAMS.items():
                    for rung in ladder:
                        r0, t0, gs, nref = bk.run(tgt, T, fam, rung)
                        if fam == "CAL" and rung == "D":
                            cal_D = (r0.copy(), t0.copy())
                        if rung == 0.0 and fam in ("FIXH", "SDMULT", "FRACG") \
                                and cal_D is not None:
                            g4 = max(g4, float(np.abs(r0.values - cal_D[0].values).max()),
                                     float(np.abs(t0.values - cal_D[1].values).max()))
                            g4n += 1
                        r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                        g9 = max(g9, float(gs.max()))
                        nyears = len(r0) / 252.0
                        for c in COSTS:
                            m = score_cell(r0, t0, gs, nref, c, S, B[f"live{c}"], nyears, st)
                            rows.append(dict(panel=pname, target=tgt, T_trade=T, family=fam,
                                             rung=rung, cell=cell_label(fam, rung), **m))
        log(f"   grid done ({len([r for r in rows if r['panel'] == pname])} scored rows)")

    G = pd.DataFrame(rows)
    G["rung_f"] = pd.to_numeric(G["rung"], errors="coerce")
    G.to_csv(f"{OUT}.grid.csv.gz", index=False)
    log(f"\n# grid: {len(G)} scored rows ({len(G)//len(COSTS)} cells x {len(COSTS)} cost rungs)")

    # -------------------------------------------------------------------- replication gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(BOOKS['U56'][1])/252:.1f}y", ">= 10",
         len(BOOKS["U56"][1]) / 252 >= 10)
    gate("G1 bt_cal diagonal == engine.backtest (returns / turnover)",
         f"{g1r:.3e} / {g1t:.3e}", "< 1e-12", max(g1r, g1t) < 1e-12)
    gate("G2 cost identity r(c) = r0 - turn*c/1e4 == fresh engine run at 10/25 bps",
         f"{g2:.3e}", "< 1e-12", g2 < 1e-12)
    for pn, pub in PUB_MEMO.items():
        row = G[(G.panel == pn) & (G.target == TGT_STAR) & (G.T_trade == "W")
                & (G.family == "CAL") & (G.rung == "W") & (G.cost == COST0)].iloc[0]
        g3 = max(g3, max(abs(row.CAGR - pub["CAGR"]), abs(row.Sharpe - pub["Sharpe"]),
                         abs(row.MaxDD - pub["MaxDD"]), abs(row.oos_CAGR - pub["oCAGR"]),
                         abs(row.oos_Sharpe - pub["oSharpe"])))
    gate("G3 reproduces the standing VOLTGT memo (points 2-4, U56 + B136)",
         f"max|d| = {g3:.3e}", "< 1e-3", g3 < 1e-3)
    n_expect = len(TARGETS) * len(TRADES) * len(BOOKS) * 3
    gate(f"G4 zero-rung cells (FIXH h=0, SDMULT k=0, FRACG f=0) == CALENDAR R=D ({g4n} cells)",
         f"{g4:.3e}", "< 1e-12", g4 < 1e-12 and g4n == n_expect)
    k = G[(G.panel == "U56") & (G.target == 0.16) & (G.T_trade == "M") & (G.family == "FIXH")
          & (G.rung_f == 0.12) & (G.cost == COST0)].iloc[0]
    g5 = max(abs(k.CAGR - PUB_1799["CAGR"]), abs(k.Sharpe - PUB_1799["Sharpe"]),
             abs(k.MaxDD - PUB_1799["MaxDD"]), abs(k.oos_CAGR - PUB_1799["oCAGR"]),
             abs(k.oos_Sharpe - PUB_1799["oSharpe"]), abs(k.oos_MaxDD - PUB_1799["oMaxDD"]))
    gate("G5 reproduces idea 1799's KEEP-4b cell (U56 t=0.16 h=0.12 T=M, 10 bps)",
         f"max|d| = {g5:.3e}", "< 1e-4", g5 < 1e-4)
    gate("G6 gross never levered", f"max gross {g9:.6f}", "<= 1.0 + 1e-9", g9 <= 1.0 + 1e-9)
    lf = G[(G.family.isin(LADDER_FREE)) & (G.rung_f > 0)]
    gate("G7 the ladder-free thresholds actually move refresh frequency",
         f"refresh/yr {lf.refresh_py.min():.1f} .. {lf.refresh_py.max():.1f}",
         "min < 52 < max", lf.refresh_py.min() < 52 < lf.refresh_py.max())
    a_sym = G[(G.family == "FIXH") & (G.rung_f > 0)].set_index(
        ["panel", "target", "T_trade", "rung_f", "cost"]).refresh_py
    a_asy = G[(G.family == "ASYMH")].set_index(
        ["panel", "target", "T_trade", "rung_f", "cost"]).refresh_py
    j = pd.concat([a_sym.rename("sym"), a_asy.rename("asym")], axis=1).dropna()
    gate("G8 the 4:1 asymmetric trigger refreshes at least as often as its symmetric twin",
         f"{(j.asym >= j.sym - 1e-9).mean():.3f} of {len(j)} pairs", "== 1.000",
         bool((j.asym >= j.sym - 1e-9).all()))

    # ------------------------------------------------------------- V1: the PRE-STATED arm
    log(f"\n## V1 — ZERO-IS REACH at t = t* = {TGT_STAR}, {COST0} bps, 6 arms (panel x T)")
    ps_rows = []
    for pname, (bk, px, cols, st) in BOOKS.items():
        for T in TRADES:
            for fam, rung in PRESTATED.items():
                d = G[(G.panel == pname) & (G.target == TGT_STAR) & (G.T_trade == T)
                      & (G.family == fam) & (G.rung_f == rung) & (G.cost == COST0)].iloc[0]
                ps_rows.append(dict(panel=pname, T_trade=T, family=fam, rung=rung,
                                    zero_IS=fam in LADDER_FREE, **{
                    k2: d[k2] for k2 in ("cell", "turn_py", "refresh_py", "gross_mean",
                                         "gross_crash_min", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                         "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "bind",
                                         "keep4b_full", "keep4b_oos", "keep4b", "keep4a")}))
            # incumbent constant for contrast
            d = G[(G.panel == pname) & (G.target == TGT_STAR) & (G.T_trade == T)
                  & (G.family == "FIXH") & (G.rung_f == H_STAR) & (G.cost == COST0)].iloc[0]
            ps_rows.append(dict(panel=pname, T_trade=T, family="FIXH", rung=H_STAR, zero_IS=False,
                                **{k2: d[k2] for k2 in ("cell", "turn_py", "refresh_py",
                                                        "gross_mean", "gross_crash_min", "CAGR",
                                                        "Sharpe", "MaxDD", "H1", "H2", "oos_CAGR",
                                                        "oos_Sharpe", "oos_MaxDD", "bind",
                                                        "keep4b_full", "keep4b_oos", "keep4b",
                                                        "keep4a")}))
    P = pd.DataFrame(ps_rows)
    P.to_csv(f"{OUT}.prestated.csv", index=False)
    for fam, s in P.groupby("family"):
        log(f"   {fam:7s} {'(zero IS)' if fam in LADDER_FREE else '(inherited constant)':22s} "
            f"4b FULL+OOS on {int(s.keep4b.sum())} of {len(s)} arms; 4a {int(s.keep4a.sum())}; "
            f"mean {s.turn_py.mean():.2f} turns/yr, {s.refresh_py.mean():.0f} refreshes/yr")
    for _, r in P[P.keep4b].iterrows():
        log(f"      4b PASS: {r.panel} T={r.T_trade} {r.family} {r.cell}  full {r.CAGR:.2%} / "
            f"{r.Sharpe:.4f} / {r.MaxDD:.2%}  OOS {r.oos_CAGR:.2%} / {r.oos_Sharpe:.4f} / "
            f"{r.oos_MaxDD:.2%}  ({r.turn_py:.2f} turns/yr)")

    # ------------------------------------------------------------------- rule 8: the choosers
    log(f"\n## RULE 8 — (t, rung) chosen on 2009-{IS_END[:4]} ONLY; {OOS_START[:4]}-2026 read once")
    CH = {"C_ISSHARPE": lambda d: d.is_Sharpe,
          "C_ISCALMAR": lambda d: d.is_Calmar,
          "C_ISDD": lambda d: d.is_MaxDD,
          "C_ISLEGS": lambda d: d.is_legs * 1e6 + d.is_Sharpe}
    ch_rows = []
    for (pn, T, c), arm in G.groupby(["panel", "T_trade", "cost"]):
        for fam in FAMS:
            sub = arm[arm.family == fam]
            if fam != "CAL":
                sub = sub[sub.rung_f > 0]                 # a zero rung is not a dial setting
            sub = sub.sort_values(["target", "rung"], key=lambda s: s.astype(str),
                                  kind="mergesort")
            rungs = sorted(sub.rung_f.dropna().unique()) if fam != "CAL" else REFRESH
            short = set(rungs[:TRUNC_N]) if fam != "CAL" else set(REFRESH[:TRUNC_N])
            for cname, f in CH.items():
                for lad, tag in ((sub, "full"),
                                 (sub[sub.rung_f.isin(short)] if fam != "CAL" else sub, "short")):
                    if not len(lad):
                        continue
                    pick = lad.loc[f(lad).idxmax()]
                    ch_rows.append(dict(panel=pn, T_trade=T, cost=c, family=fam, chooser=cname,
                                        ladder=tag, target=pick.target, rung=pick.rung,
                                        cell=pick.cell, turn_py=pick.turn_py,
                                        refresh_py=pick.refresh_py,
                                        CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD,
                                        H1=pick.H1, H2=pick.H2, oos_CAGR=pick.oos_CAGR,
                                        oos_Sharpe=pick.oos_Sharpe, oos_MaxDD=pick.oos_MaxDD,
                                        bind=pick.bind, keep4b_full=pick.keep4b_full,
                                        keep4b_oos=pick.keep4b_oos, keep4b=pick.keep4b,
                                        keep4a=pick.keep4a))
    C = pd.DataFrame(ch_rows)
    C.to_csv(f"{OUT}.choosers.csv", index=False)
    C0 = C[(C.cost == COST0) & (C.ladder == "full")]
    log(f"   picks at {COST0} bps, FULL ladder ({len(C0)} = 6 arms x {len(FAMS)} families x "
        f"{len(CH)} choosers):")
    for fam, s in C0.groupby("family"):
        arms4b = s.groupby("chooser").keep4b.sum()
        log(f"   {fam:7s} 4b FULL+OOS on {int(arms4b.max())} of 6 arms at its BEST chooser "
            f"({arms4b.idxmax()}); mean over choosers {arms4b.mean():.2f}; "
            f"4a {int(s.keep4a.sum())} of {len(s)}")
    best_fixh = int(C0[C0.family == "FIXH"].groupby("chooser").keep4b.sum().max())
    ps_best = {fam: int(P[(P.family == fam)].keep4b.sum()) for fam in PRESTATED}
    v1 = max(ps_best[f] for f in LADDER_FREE) >= best_fixh
    log(f"   V1: best LADDER-FREE pre-stated constant reaches "
        f"{max(ps_best[f] for f in LADDER_FREE)} of 6 arms (zero IS spend) vs FIXH's best "
        f"IS-only chooser {best_fixh} of 6  ->  {'TRIGGERED' if v1 else 'NOT triggered'}")

    # ------------------------------------------------------------------ V2: scale invariance
    log("\n## V2 — SCALE INVARIANCE of the realised refresh rate across (panel x target)")
    inv_rows = []
    for fam, rung in list(PRESTATED.items()) + [("FIXH", H_STAR)]:
        for T in TRADES:
            s = G[(G.family == fam) & (G.rung_f == rung) & (G.T_trade == T) & (G.cost == COST0)]
            inv_rows.append(dict(family=fam, rung=rung, T_trade=T, n=len(s),
                                 refresh_mean=s.refresh_py.mean(), refresh_sd=s.refresh_py.std(),
                                 refresh_cv=s.refresh_py.std() / s.refresh_py.mean(),
                                 turn_cv=s.turn_py.std() / s.turn_py.mean(),
                                 gross_cv=s.gross_mean.std() / s.gross_mean.mean()))
    IV = pd.DataFrame(inv_rows)
    IV.to_csv(f"{OUT}.invariance.csv", index=False)
    log(IV.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    fix_cv = IV[(IV.family == "FIXH")].set_index("T_trade").refresh_cv
    v2 = {}
    for fam in LADDER_FREE:
        cv = IV[IV.family == fam].set_index("T_trade").refresh_cv
        v2[fam] = bool((cv < fix_cv).all())
        log(f"   V2 {fam}: refresh CV {cv.to_dict()} vs FIXH h={H_STAR} {fix_cv.to_dict()} -> "
            f"{'TRIGGERED' if v2[fam] else 'NOT triggered'}")

    # -------------------------------------------------------------- V3: ladder-length immunity
    log(f"\n## V3 — LADDER-LENGTH FRAGILITY (full ladder vs its first {TRUNC_N} rungs)")
    frag_rows = []
    for (pn, T, c, fam, cname), s in C.groupby(["panel", "T_trade", "cost", "family", "chooser"]):
        if len(s) != 2:
            continue
        full = s[s.ladder == "full"].iloc[0]
        shrt = s[s.ladder == "short"].iloc[0]
        frag_rows.append(dict(panel=pn, T_trade=T, cost=c, family=fam, chooser=cname,
                              pick_full=f"t={full.target} {full.cell}",
                              pick_short=f"t={shrt.target} {shrt.cell}",
                              pick_moved=(full.target != shrt.target or full.cell != shrt.cell),
                              verdict_moved=bool(full.keep4b != shrt.keep4b),
                              d_oos_Sharpe=full.oos_Sharpe - shrt.oos_Sharpe))
    F = pd.DataFrame(frag_rows)
    F.to_csv(f"{OUT}.fragility.csv", index=False)
    F0 = F[(F.cost == COST0) & (F.family != "CAL")]
    for fam, s in F0.groupby("family"):
        log(f"   {fam:7s} pick moves on {int(s.pick_moved.sum())} of {len(s)} (arm x chooser) "
            f"pairs; OOS 4b verdict moves on {int(s.verdict_moved.sum())}")
    log(f"   PRE-STATED constants: pick moves on 0 of {len(P)} by construction (no ladder is read)")

    # ------------------------------------------------------------------------- V4: asymmetry
    log("\n## V4 — ASYMMETRY (4:1 tight-DOWN / loose-UP) against its symmetric twin")
    asym_rows = []
    for sym, asy in (("FIXH", "ASYMH"), ("FRACG", "ASYMG")):
        a = G[(G.family == asy) & (G.cost == COST0)].set_index(
            ["panel", "target", "T_trade", "rung_f"])
        b = G[(G.family == sym) & (G.cost == COST0) & (G.rung_f > 0)].set_index(
            ["panel", "target", "T_trade", "rung_f"])
        idx = a.index.intersection(b.index)
        a, b = a.loc[idx], b.loc[idx]
        asym_rows.append(dict(
            pair=f"{asy} vs {sym}", n=len(idx),
            keep4b_asym=int(a.keep4b.sum()), keep4b_sym=int(b.keep4b.sum()),
            keep4a_asym=int(a.keep4a.sum()), keep4a_sym=int(b.keep4a.sum()),
            d_oos_Sharpe=float((a.oos_Sharpe - b.oos_Sharpe).mean()),
            win_oos_Sharpe=float((a.oos_Sharpe > b.oos_Sharpe).mean()),
            d_oos_MaxDD_pp=float((a.oos_MaxDD - b.oos_MaxDD).mean() * 100),
            d_oos_CAGR_pp=float((a.oos_CAGR - b.oos_CAGR).mean() * 100),
            d_turn_py=float((a.turn_py - b.turn_py).mean()),
            d_crash_gross=float((a.gross_crash_min - b.gross_crash_min).mean())))
    A = pd.DataFrame(asym_rows)
    A.to_csv(f"{OUT}.asymmetry.csv", index=False)
    log(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    v4 = bool((A.keep4b_asym >= A.keep4b_sym).all() and (A.d_crash_gross <= 1e-9).all())
    log(f"   V4 -> {'TRIGGERED' if v4 else 'NOT triggered'} "
        f"(asymmetric clears 4b at least as often AND cuts gross at least as deep in the crash)")

    # ---------------------------------------------- V5: capital, matched calendar + crash tape
    log("\n## V5 — CAPITAL: turnover-matched calendar comparand and the crash-excised tape")
    heads = []
    for _, r in P[P.keep4b].iterrows():
        heads.append((r.panel, TGT_STAR, r.T_trade, r.family, r.rung, "prestated"))
    for _, r in C0[C0.keep4b & (C0.family != "CAL")].iterrows():
        heads.append((r.panel, r.target, r.T_trade, r.family, float(r.rung), "chooser"))
    heads = sorted(set(heads))
    log(f"   {len(heads)} distinct 4b FULL+OOS headline cells to re-read")
    crash_rows = []
    for pn, tg, T, fam, rung, how in heads:
        bk, px, cols, st = BOOKS[pn]
        S = BASE[pn]["spy"]
        r0, t0, gs, nref = bk.run(tg, T, fam, rung)
        r0, t0 = r0.loc[st:], t0.loc[st:]
        r = net(r0, t0, COST0)
        # matched point on this arm's own calendar ladder
        cal = G[(G.panel == pn) & (G.target == tg) & (G.T_trade == T) & (G.family == "CAL")
                & (G.cost == COST0)].sort_values("turn_py")
        tp = float(t0.sum() / (len(r0) / 252.0))
        d_match = float(G[(G.panel == pn) & (G.target == tg) & (G.T_trade == T)
                          & (G.family == fam) & (G.rung_f == rung)
                          & (G.cost == COST0)].iloc[0].oos_Sharpe
                        - np.interp(tp, cal.turn_py.values, cal.oos_Sharpe.values))
        keep = ~((r.index >= CRASH[0]) & (r.index <= CRASH[1]))
        rx = r[keep]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        spx = spy[~((spy.index >= CRASH[0]) & (spy.index <= CRASH[1]))]
        mo, mox = mets(r.loc[OOS_START:]), mets(rx.loc[OOS_START:])
        so, sox = mets(spy.loc[OOS_START:]), mets(spx.loc[OOS_START:])
        calx = []
        for Rc in REFRESH:
            cr, ct, _, _ = bk.run(tg, T, "CAL", Rc)
            cr, ct = cr.loc[st:], ct.loc[st:]
            crx = net(cr, ct, COST0)
            crx = crx[~((crx.index >= CRASH[0]) & (crx.index <= CRASH[1]))]
            calx.append((float(ct.sum() / (len(cr) / 252.0)),
                         mets(crx.loc[OOS_START:])["Sharpe"]))
        calx.sort()
        d_match_x = mox["Sharpe"] - float(np.interp(tp, [x for x, _ in calx],
                                                    [y for _, y in calx]))
        crash_rows.append(dict(panel=pn, target=tg, T_trade=T, family=fam, rung=rung, how=how,
                               turn_py=tp, oos_Sharpe=mo["Sharpe"], oos_CAGR=mo["CAGR"],
                               oos_MaxDD=mo["MaxDD"], spy_oos_Sharpe=so["Sharpe"],
                               spy_oos_MaxDD=so["MaxDD"],
                               d_matched_cal=d_match,
                               x_oos_Sharpe=mox["Sharpe"], x_oos_CAGR=mox["CAGR"],
                               x_oos_MaxDD=mox["MaxDD"], x_spy_oos_Sharpe=sox["Sharpe"],
                               x_spy_oos_MaxDD=sox["MaxDD"],
                               x_d_matched_cal=d_match_x,
                               x_keep4b_oos=(mox["Sharpe"] > sox["Sharpe"]
                                             and mox["MaxDD"] >= DD_CAP * sox["MaxDD"]
                                             and mox["CAGR"] >= CAGR_FLOOR * mets(
                                                 spx.loc[OOS_START:])["CAGR"])))
    X = pd.DataFrame(crash_rows)
    X.to_csv(f"{OUT}.crash.csv", index=False)
    if len(X):
        log(X[["panel", "target", "T_trade", "family", "rung", "how", "turn_py", "oos_Sharpe",
               "d_matched_cal", "x_oos_Sharpe", "x_d_matched_cal", "x_keep4b_oos"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------------ 4b / 4a census
    log("\n## CENSUS — both KEEP paths at every cell (all grid points published)")
    cen = (G.groupby(["family", "cost"])
             .agg(cells=("keep4b", "size"), keep4b_full=("keep4b_full", "sum"),
                  keep4b_oos=("keep4b_oos", "sum"), keep4b=("keep4b", "sum"),
                  keep4a=("keep4a", "sum")).reset_index())
    cen.to_csv(f"{OUT}.census.csv", index=False)
    log(cen.to_string(index=False))
    log("   binding leg at 4b failures ({}bps): ".format(COST0)
        + "; ".join(f"{k} {v}" for k, v in
                    G[(G.cost == COST0) & ~G.keep4b_full].bind.value_counts().head(6).items()))

    gdf = pd.DataFrame(_gates)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\n# gates: {int(gdf.pass_.sum())}/{len(gdf)} pass")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    return G, P, C, F, A, X, IV, cen


if __name__ == "__main__":
    main()
