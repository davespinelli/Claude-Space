#!/usr/bin/env python3
"""Idea 2022 (lane cloud, 2026-09-20) — IS THE DRIFT TRIGGER'S MATCHED-TURNOVER WIN A
DRAWDOWN-TIMING FACT (ONE EPISODE) OR A DIAL?

THE DEFECT THIS PRICES.  Idea 1799 (lane C, same day) reported that a DRIFT-THRESHOLD refresh
beats its own arm's TURNOVER-MATCHED point on the CALENDAR ladder at 263 of 263 cells at 10 bps
(mean OOS Sharpe +0.0596).  263 of 263 is a suspiciously clean sweep, and 1799's own two
diagnostic tables say why it might be: the win decomposes as +4.07 pp of OOS MaxDD against only
+0.31 pp of OOS CAGR, and its MECHANISM table shows the whole gross gap opening in one quarter
(2020-02-19 -> 2020-03-23: R=Q holds gross at 1.000 while every drift rung cuts to 0.25-0.38).
A dominance carried by one quarter is an EPISODE, not a dial.  1799 also published no standard
error at all: 263 point estimates with no paired SE cannot distinguish 263 independent wins from
one win counted 263 times.

WHAT IS PRICED HERE.  1799's exact corpus is rebuilt (same runners, same panels, same grid, same
turnover-matched interpolation estimator), and then the two missing readings are taken:

  (A) CRASH-EXCISED RE-PRICING.  Every book's daily net return series has the 2020 crash window
      removed and the remainder concatenated; the matched-turnover comparison is then recomputed
      END TO END on the excised tape (turnover per year AND OOS Sharpe both excised, so the pairs
      stay matched on the tape they are scored on).  TWO windows are REPORTED, not tuned:
        CRASH_PT   2020-02-19 -> 2020-03-23  (peak to trough; 1799's own mechanism window)
        CRASH_WIDE 2020-02-19 -> 2020-04-30  (peak through the bulk of the recovery)
  (B) PAIRED BLOCK-BOOTSTRAP SE.  A moving-block bootstrap over OOS trading days, applied to the
      WHOLE 13-cell arm at once so that every cell is resampled on the SAME day blocks (this is
      what makes the difference PAIRED).  On each draw the estimator is recomputed exactly as
      1799 defines it: each calendar rung's Sharpe is re-read on the resampled days, and the
      comparand is the linear interpolation of those Sharpes at the drift book's REALISED
      turnover (turnover is a design quantity of the book, not a property of the draw, so it is
      held fixed).  B = 1000 draws, seed 20260922, block lengths 21 and 63 trading days, both
      REPORTED.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  EPISODE OR DIAL (the idea's own question).  Of the 263 matched pairs at 10 bps, the share
      that still shows d_oos_Sharpe > 0 with the crash excised.  >= 90% under BOTH windows -> the
      dominance is NOT a 2020 episode.  <= 50% under either -> it IS an episode and 1799's
      263-of-263 must be restated as a crash-timing fact.  In between -> PARTIAL, and the run
      reports which arms survive and which do not.
  V2  RESOLUTION.  Share of the 263 whose paired block-bootstrap 95% CI on d_oos_Sharpe EXCLUDES
      zero, and the max/mean |t|.  A sweep with no cell resolvable is a point-estimate sweep.
  V3  DRAWDOWN OR COST.  1799's +4.07 pp OOS MaxDD / +0.31 pp OOS CAGR split, recomputed with the
      crash excised.  If the MaxDD credit collapses and the CAGR credit does not, the trigger is
      buying ONE drawdown; if both collapse, it is buying that quarter outright.
  V4  CAPITAL.  Both KEEP paths are scored at EVERY cell on BOTH tapes (full and crash-excised),
      against live RULES v2 and SPY re-read on the same tape, and rule 8 is run on both: (t, h)
      or (t, R) chosen on 2009-2016 ONLY, 2017-2026 read exactly once.  Any cell clearing 4b FULL
      *and* OOS that a legal IS-only chooser actually REACHES is a KEEP-4b candidate.

DIALS.  NOTHING NEW IS TUNED.  `t` (TARGET) and `h` (THRESHOLD) are idea 1799's two inherited
dials and the only ones a chooser ever spends; the calendar family spends `t` and `R`.  REPORTED,
NOT TUNED: CRASH WINDOW {PT, WIDE}, BLOCK LENGTH {21, 63}, TRADE cadence T in {W, M} (separate
arms), PANEL {U56, B136, SMALL}, COST {0, 10, 25, 50} bps.  Every grid point is published
(`.grid.csv`), every matched pair (`.matched.csv`), every bootstrap summary (`.bootstrap.csv`).

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time
panel.  The DRIFT-vs-CALENDAR contrast is same-tape / same-names / same-grid with only the
refresh TRIGGER moved, so it is first-order immune; the PASS COUNTS are not.  Note also the
2026-09-20 data-vintage finding: the SMALL cache grew 439 -> 665 names, so SMALL-panel counts
here are not comparable with pre-2026-09-20 SMALL numbers.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_drift-win-episode-or-dial_cloud.py
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

DATE, SLUG = "2026-09-20", "drift-win-episode-or-dial"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
TGT_MEMO = 0.16
REFRESH = ["D", "W", "M", "Q"]
THRESH = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]
H_GRID = [h for h in THRESH if h > 0]
TRADES = ["W", "M"]
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
SIG_L, SIG_D = 20, 0

# REPORTED, not tuned
CRASH = {"CRASH_PT":   ("2020-02-19", "2020-03-23"),
         "CRASH_WIDE": ("2020-02-19", "2020-04-30")}
TAPES = ["FULL"] + list(CRASH)
BLOCKS = [21, 63]
NBOOT = 1000
SEED = 20260922

# committed numbers this run must reproduce
PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}
PUB_1799 = dict(n_inside=263, win=263, mean_dS=0.059579, mean_dDD=0.0407, mean_dCAGR=0.0031)

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


def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    """Annualised L-day realised vol of the UNLEVERED equal-weight panel portfolio through close
    t-d.  (L, d) = (20, 0) is the standing memo's convention."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ------------------------------------------------------ the two refresh runners (1799 verbatim)
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


def bt_drift(px_ret, W0, g0, mT, h):
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


class Book:
    def __init__(self, px, cols, index):
        self.index = index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((1, ew.shape[1])), ew[:-1]])
        self.SIG = panel_sigma(px, cols)
        self.masks = {}
        for f in ("D", "W", "M", "Q"):
            m = np.asarray(rebalance_mask(index, f).values, bool)
            self.masks[f] = np.concatenate([[False], m[:-1]])

    def g_of(self, tgt):
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        return np.concatenate([[0.0], g[:-1]])

    def run_cal(self, g0, T, R):
        r, t, gs, nref = bt_cal(self.R, self.W, g0, self.masks[T], self.masks[R])
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)

    def run_drift(self, g0, T, h):
        r, t, gs, nref = bt_drift(self.R, self.W, g0, self.masks[T], h)
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


def tape_mask(index, tape):
    """Boolean keep-mask for a tape.  FULL keeps everything; a CRASH_* tape drops the window."""
    if tape == "FULL":
        return np.ones(len(index), bool)
    a, b = CRASH[tape]
    return np.asarray(~((index >= pd.Timestamp(a)) & (index <= pd.Timestamp(b))), bool)


def block_idx(n, L, B, rng):
    """Moving-block bootstrap day indices: (B, n) int array, blocks of length L drawn with
    replacement from all n-L+1 start positions and truncated to exactly n days."""
    nb = int(np.ceil(n / L))
    starts = rng.integers(0, max(n - L + 1, 1), size=(B, nb))
    off = np.arange(L)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(B, nb * L)[:, :n]
    return np.minimum(idx, n - 1)


def boot_sharpe(Rm, idx, chunk=100):
    """Annualised Sharpe of each row of Rm (k, n) on each bootstrap draw in idx (B, n).
    Returns (B, k).  Chunked over draws so the (k, B, n) gather never materialises whole."""
    out = np.empty((idx.shape[0], Rm.shape[0]))
    for a in range(0, idx.shape[0], chunk):
        S = Rm[:, idx[a:a + chunk]]                   # (k, chunk, n)
        mu = S.mean(axis=2)
        sd = S.std(axis=2, ddof=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            out[a:a + chunk] = np.where(sd > 0, mu * np.sqrt(252.0) / sd, np.nan).T
    return out


# ----------------------------------------------------------------------------- run
def main():
    rng = np.random.default_rng(SEED)
    log(f"# Idea 2022 (lane cloud, {DATE}) — is the DRIFT trigger's MATCHED-TURNOVER win a "
        f"DRAWDOWN-TIMING fact or a COST fact?")
    log(f"# nothing new is tuned: t {TARGETS} x [ h {H_GRID} | R {REFRESH} ] are idea 1799's two "
        f"inherited dials.  REPORTED, not tuned: crash window {list(CRASH)}, block {BLOCKS}, "
        f"trade T {TRADES}, panel, cost {COSTS} bps.  sigma FIXED (L={SIG_L}, d={SIG_D}).")
    log(f"# warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}; bootstrap B={NBOOT} seed {SEED}.")
    for k, (a, b) in CRASH.items():
        log(f"#   {k}: {a} -> {b}")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows, brows = [], []
    BASE = {}
    g1r = g1t = g2 = g3 = g4 = g9 = 0.0
    g4n = 0
    excised_days = {}

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        bk = Book(px, cols, px.index)
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")

        # ---- baselines on EVERY tape: live RULES v2 (weekly) and SPY --------------------
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        spy0 = px["SPY"].pct_change().fillna(0.0).loc[st:]
        B = dict(start=st)
        for tape in TAPES:
            km = tape_mask(lr.index, tape)
            spy = spy0[km]
            excised_days[(pname, tape)] = int((~km).sum())
            B[("spy", tape)] = dict(
                full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                h1=halves(spy)[0], h2=halves(spy)[1],
                ish1=halves(spy.loc[:IS_END])[0], ish2=halves(spy.loc[:IS_END])[1])
            for c in COSTS:
                r = net(lr, lt, c)[km]
                B[("live", tape, c)] = dict(
                    full=mets(r), oos=mets(r.loc[OOS_START:]), h1=halves(r)[0], h2=halves(r)[1],
                    turn=float(lt[km].sum() / (len(r) / 252.0)))
        BASE[pname] = B
        for tape in TAPES:
            L, S = B[("live", tape, COST0)], B[("spy", tape)]
            log(f"   [{tape:10s}] LIVE v2 (W,{COST0}bps) {L['full']['CAGR']:.2%}/"
                f"{L['full']['Sharpe']:.4f}/{L['full']['MaxDD']:.2%} "
                f"(OOS {L['oos']['CAGR']:.2%}/{L['oos']['Sharpe']:.4f}/{L['oos']['MaxDD']:.2%})"
                f"   SPY {S['full']['CAGR']:.2%}/{S['full']['Sharpe']:.4f}/{S['full']['MaxDD']:.2%}"
                f" (OOS {S['oos']['CAGR']:.2%}/{S['oos']['Sharpe']:.4f}/{S['oos']['MaxDD']:.2%})"
                f"   [{excised_days[(pname, tape)]} days removed]")

        # ---- G1 / G2: the calendar diagonal is engine.backtest --------------------------
        if pname in ("U56", "B136"):
            Gp = (TGT_MEMO / bk.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
            Wfull = (eq_weight(px, cols).mul(Gp, axis=0)).fillna(0.0)
            a, at, _, _ = bk.run_cal(bk.g_of(TGT_MEMO), "W", "W")
            b = engine_backtest(px, Wfull, cost_bps=0.0, freq="W")
            g1r = max(g1r, float(np.abs(a.values - b["returns"].values).max()))
            g1t = max(g1t, float(np.abs(at.values - b["turnover"].values).max()))
            for c in (10, 25):
                eb = engine_backtest(px, Wfull, cost_bps=float(c), freq="W")["returns"]
                g2 = max(g2, float(np.abs(net(a, at, c).values - eb.values).max()))

        # ---- the grid --------------------------------------------------------------------
        for tgt in TARGETS:
            g0 = bk.g_of(tgt)
            for T in TRADES:
                cells = ([("CAL", Rc, np.nan) for Rc in REFRESH]
                         + [("DRIFT", "h", h) for h in THRESH])
                cal_ref = {}
                keep_oos = {}          # cell -> OOS net@COST0 daily returns, per tape
                for fam, Rc, h in cells:
                    if fam == "CAL":
                        r0, t0, gs, nref = bk.run_cal(g0, T, Rc)
                        label = f"R={Rc}"
                        cal_ref[Rc] = (r0.copy(), t0.copy())
                    else:
                        r0, t0, gs, nref = bk.run_drift(g0, T, h)
                        label = f"h={h:.2f}"
                        if h == 0.0 and "D" in cal_ref:
                            cr, ct = cal_ref["D"]
                            g4 = max(g4, float(np.abs(r0.values - cr.values).max()),
                                     float(np.abs(t0.values - ct.values).max()))
                            g4n += 1
                    r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                    g9 = max(g9, float(gs.max()))
                    for tape in TAPES:
                        km = tape_mask(r0.index, tape)
                        rT, tT, gsT = r0[km], t0[km], gs[km]
                        yrs = len(rT) / 252.0
                        S = B[("spy", tape)]
                        for c in COSTS:
                            r = net(rT, tT, c)
                            if c == COST0:
                                keep_oos[(tape, label)] = r.loc[OOS_START:]
                            mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                            h1, h2 = halves(r)
                            ih1, ih2 = halves(r.loc[:IS_END])
                            mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
                                   "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
                                   "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
                                   "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
                            bl, nbad = binding(mar)
                            LV = B[("live", tape, c)]
                            k4bf = (h1 > S["h1"] and h2 > S["h2"]
                                    and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                                    and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
                            k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                                    and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                    and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                            k4a = (h1 > LV["h1"] and h2 > LV["h2"]
                                   and mf["MaxDD"] >= LV["full"]["MaxDD"])
                            k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"]
                                    and mo["MaxDD"] >= LV["oos"]["MaxDD"])
                            is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
                                       + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
                                       + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
                            rows.append(dict(
                                panel=pname, tape=tape, target=tgt, T_trade=T, family=fam,
                                R_refresh=Rc, h=h, cell=label, cost=c,
                                turn_py=float(tT.sum() / yrs),
                                oos_turn_py=float(tT.loc[OOS_START:].sum()
                                                  / (len(rT.loc[OOS_START:]) / 252.0)),
                                is_turn_py=float(tT.loc[:IS_END].sum()
                                                 / (len(rT.loc[:IS_END]) / 252.0)),
                                refresh_py=nref / (len(px) / 252.0),
                                gross_mean=float(gsT.mean()),
                                gross_mean_is=float(gsT.loc[:IS_END].mean()),
                                gross_max=float(gsT.max()),
                                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                H1=h1, H2=h2,
                                is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                                is_H1=ih1, is_H2=ih2, is_legs=is_legs,
                                is_Calmar=(mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"]
                                           else np.nan),
                                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                                oos_MaxDD=mo["MaxDD"],
                                **{k: float(v) for k, v in mar.items()},
                                bind=bl, n_fail=nbad,
                                keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                                keep4a=k4a, keep4a_oos=k4ao))

                # ---- paired block bootstrap, this arm, both tapes ---------------------
                for tape in TAPES:
                    labels = [f"R={Rc}" for Rc in REFRESH] + [f"h={h:.2f}" for h in H_GRID]
                    Rm = np.vstack([keep_oos[(tape, lb_)].values for lb_ in labels])
                    n = Rm.shape[1]
                    for L in BLOCKS:
                        idx = block_idx(n, L, NBOOT, rng)
                        SH = boot_sharpe(Rm, idx)                       # (B, 13)
                        brows.append(dict(panel=pname, tape=tape, target=tgt, T_trade=T,
                                          block=L, _SH=SH, _labels=labels))
        log(f"   grid done ({len([r for r in rows if r['panel'] == pname])} scored rows)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")

    # -------------------------------------------------------------------- replication gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 bt_cal diagonal == engine.backtest (returns / turnover)",
         f"{g1r:.3e} / {g1t:.3e}", "< 1e-12", max(g1r, g1t) < 1e-12)
    gate("G2 cost identity r(c) = r0 - turn*c/1e4 == fresh engine run at 10/25 bps",
         f"{g2:.3e}", "< 1e-12", g2 < 1e-12)
    for pn, pub in PUB_MEMO.items():
        row = G[(G.panel == pn) & (G.tape == "FULL") & (G.target == TGT_MEMO) & (G.T_trade == "W")
                & (G.family == "CAL") & (G.R_refresh == "W") & (G.cost == COST0)].iloc[0]
        g3 = max(g3, max(abs(row.CAGR - pub["CAGR"]), abs(row.Sharpe - pub["Sharpe"]),
                         abs(row.MaxDD - pub["MaxDD"]), abs(row.oos_CAGR - pub["oCAGR"]),
                         abs(row.oos_Sharpe - pub["oSharpe"])))
    gate("G3 reproduces the standing VOLTGT memo (points 2-4, U56 + B136)",
         f"max|d| = {g3:.3e}", "< 1e-3", g3 < 1e-3)
    gate(f"G4 DRIFT h=0 == CALENDAR R=D, cell by cell ({g4n} cells)",
         f"{g4:.3e}", "< 1e-12", g4 < 1e-12 and g4n == len(TARGETS) * len(TRADES) * len(PS))
    gate("G6 gross never levered", f"max gross {g9:.6f}", "<= 1.0 + 1e-9", g9 <= 1.0 + 1e-9)
    nz = G[(G.family == "DRIFT") & (G.h > 0) & (G.tape == "FULL")]
    gate("G7 the drift ladder actually moves refresh frequency",
         f"refresh/yr {nz.refresh_py.min():.1f} .. {nz.refresh_py.max():.1f}",
         "min < 52 < max", nz.refresh_py.min() < 52 < nz.refresh_py.max())
    for tape in CRASH:
        d = {excised_days[(p, tape)] for p, _, _ in PS}
        gate(f"G8 {tape} removes a non-empty window on every panel", f"{sorted(d)} days",
             "> 0", min(d) > 0)

    # ------------------------------------------------- the matched-turnover estimator, per tape
    log("\n## MATCHED-TURNOVER COMPARISON (1799's estimator, recomputed tape by tape)")
    mrows = []
    for (pn, tape, tg, T, c), sub in G.groupby(["panel", "tape", "target", "T_trade", "cost"]):
        cal = sub[sub.family == "CAL"].sort_values("turn_py")
        x = cal.turn_py.values
        for _, d in sub[(sub.family == "DRIFT") & (sub.h > 0)].iterrows():
            inside = x.min() <= d.turn_py <= x.max()
            mrows.append(dict(
                panel=pn, tape=tape, target=tg, T_trade=T, cost=c, h=d.h, turn_py=d.turn_py,
                cal_turn_lo=x.min(), cal_turn_hi=x.max(), inside_ladder=inside,
                d_oos_Sharpe=d.oos_Sharpe - float(np.interp(d.turn_py, x, cal.oos_Sharpe.values)),
                d_oos_MaxDD=d.oos_MaxDD - float(np.interp(d.turn_py, x, cal.oos_MaxDD.values)),
                d_oos_CAGR=d.oos_CAGR - float(np.interp(d.turn_py, x, cal.oos_CAGR.values)),
                d_full_Sharpe=d.Sharpe - float(np.interp(d.turn_py, x, cal.Sharpe.values)),
                d_full_MaxDD=d.MaxDD - float(np.interp(d.turn_py, x, cal.MaxDD.values))))
    M = pd.DataFrame(mrows)
    M.to_csv(f"{OUT}.matched.csv", index=False)

    F0 = M[(M.tape == "FULL") & (M.cost == COST0) & M.inside_ladder]
    gate("G5 reproduces idea 1799's V2 headline (263 of 263, mean +0.0596)",
         f"{int((F0.d_oos_Sharpe > 0).sum())} of {len(F0)}, mean {F0.d_oos_Sharpe.mean():+.4f}",
         "263 of 263, |d mean| < 1e-3",
         len(F0) == PUB_1799["n_inside"] and int((F0.d_oos_Sharpe > 0).sum()) == PUB_1799["win"]
         and abs(F0.d_oos_Sharpe.mean() - PUB_1799["mean_dS"]) < 1e-3)

    # the SAME 263 pairs, keyed so a tape cannot silently change the population
    KEY = ["panel", "target", "T_trade", "h"]
    base_keys = set(map(tuple, F0[KEY].values))
    log(f"   the 263-pair population is keyed on {KEY}; |keys| = {len(base_keys)}")

    log("\n## V1 — DOES THE WIN SURVIVE OUTSIDE THE 2020 CRASH?")
    v1 = []
    for tape in TAPES:
        t0 = M[(M.tape == tape) & (M.cost == COST0)]
        t0 = t0[[tuple(r) in base_keys for r in t0[KEY].values]]
        w = int((t0.d_oos_Sharpe > 0).sum())
        v1.append(dict(tape=tape, n=len(t0), wins=w, share=w / len(t0),
                       mean_dS=t0.d_oos_Sharpe.mean(), med_dS=t0.d_oos_Sharpe.median(),
                       mean_dDD=t0.d_oos_MaxDD.mean(), mean_dCAGR=t0.d_oos_CAGR.mean(),
                       inside=int(t0.inside_ladder.sum())))
        log(f"   [{tape:10s}] {w}/{len(t0)} = {w/len(t0):.1%} wins; mean dOOS Sharpe "
            f"{t0.d_oos_Sharpe.mean():+.4f} (median {t0.d_oos_Sharpe.median():+.4f}); "
            f"mean dOOS MaxDD {t0.d_oos_MaxDD.mean()*100:+.2f} pp; mean dOOS CAGR "
            f"{t0.d_oos_CAGR.mean()*100:+.2f} pp; still inside the ladder {int(t0.inside_ladder.sum())}/{len(t0)}")
        for (p, T), s in t0.groupby(["panel", "T_trade"]):
            log(f"        {p}/{T}: {int((s.d_oos_Sharpe > 0).sum())}/{len(s)} "
                f"mean {s.d_oos_Sharpe.mean():+.4f}")
    V1 = pd.DataFrame(v1)
    V1.to_csv(f"{OUT}.v1_excision.csv", index=False)
    shares = {r["tape"]: r["share"] for r in v1 if r["tape"] != "FULL"}
    if min(shares.values()) >= 0.90:
        v1_verdict = "NOT-AN-EPISODE"
    elif min(shares.values()) <= 0.50:
        v1_verdict = "EPISODE"
    else:
        v1_verdict = "PARTIAL"
    log(f"   V1 VERDICT: {v1_verdict}  (excised win shares "
        + ", ".join(f"{k} {v:.1%}" for k, v in shares.items()) + ")")

    # ------------------------------------------------------------------ V2: paired bootstrap
    log("\n## V2 — PAIRED MOVING-BLOCK BOOTSTRAP ON THE MATCHED DIFFERENCE")
    boot_out = []
    for b in brows:
        pn, tape, tg, T, L = b["panel"], b["tape"], b["target"], b["T_trade"], b["block"]
        sub = G[(G.panel == pn) & (G.tape == tape) & (G.target == tg) & (G.T_trade == T)
                & (G.cost == COST0)]
        cal = sub[sub.family == "CAL"].sort_values("turn_py")
        order = [f"R={r}" for r in cal.R_refresh.values]
        pos = {lb_: i for i, lb_ in enumerate(b["_labels"])}
        colidx = [pos[o] for o in order]
        x = cal.turn_py.values
        SH = b["_SH"]
        calS = SH[:, colidx]                                    # (B, 4) sorted by turnover
        for h in H_GRID:
            d = sub[(sub.family == "DRIFT") & (np.isclose(sub.h, h))].iloc[0]
            if not (x.min() <= d.turn_py <= x.max()):
                continue
            j = pos[f"h={h:.2f}"]
            w = np.interp(d.turn_py, x, np.arange(len(x)))      # interpolation position
            lo, hi = int(np.floor(w)), min(int(np.floor(w)) + 1, len(x) - 1)
            frac = w - lo
            comp = calS[:, lo] * (1 - frac) + calS[:, hi] * frac
            diff = SH[:, j] - comp
            pt = d.oos_Sharpe - float(np.interp(d.turn_py, x, cal.oos_Sharpe.values))
            se = float(diff.std(ddof=1))
            ql, qh = np.percentile(diff, [2.5, 97.5])
            boot_out.append(dict(panel=pn, tape=tape, target=tg, T_trade=T, h=h, block=L,
                                 point=pt, boot_mean=float(diff.mean()), se=se,
                                 t=pt / se if se > 0 else np.nan,
                                 ci_lo=float(ql), ci_hi=float(qh),
                                 excl0=bool(ql > 0 or qh < 0), pos_share=float((diff > 0).mean())))
    BT = pd.DataFrame(boot_out)
    BT.to_csv(f"{OUT}.bootstrap.csv", index=False)
    for tape in TAPES:
        for L in BLOCKS:
            s = BT[(BT.tape == tape) & (BT.block == L)]
            if not len(s):
                continue
            log(f"   [{tape:10s} block {L:2d}] n={len(s)}  mean point {s.point.mean():+.4f}  "
                f"mean SE {s.se.mean():.4f}  mean |t| {s.t.abs().mean():.2f}  max |t| "
                f"{s.t.abs().max():.2f}  95% CI excludes 0 at {int(s.excl0.sum())}/{len(s)} "
                f"({s.excl0.mean():.1%})  mean P(diff>0) {s.pos_share.mean():.3f}")
    v2_ok = bool(BT[(BT.tape == "FULL")].excl0.mean() > 0.5)
    log(f"   V2 VERDICT: {'RESOLVED' if v2_ok else 'POINT-ESTIMATE ONLY'} on the FULL tape "
        f"({BT[BT.tape == 'FULL'].excl0.mean():.1%} of cells resolvable at 95%)")

    # ------------------------------------------------------------------ V3: DD vs CAGR split
    log("\n## V3 — WHICH LEG CARRIES THE WIN (drawdown timing, or cost/return)?")
    v3 = []
    for tape in TAPES:
        t0 = M[(M.tape == tape) & (M.cost == COST0)]
        t0 = t0[[tuple(r) in base_keys for r in t0[KEY].values]]
        v3.append(dict(tape=tape, mean_dDD_pp=t0.d_oos_MaxDD.mean() * 100,
                       mean_dCAGR_pp=t0.d_oos_CAGR.mean() * 100,
                       dd_win=float((t0.d_oos_MaxDD > 0).mean()),
                       cagr_win=float((t0.d_oos_CAGR > 0).mean()),
                       sharpe_win=float((t0.d_oos_Sharpe > 0).mean())))
        log(f"   [{tape:10s}] dOOS MaxDD {t0.d_oos_MaxDD.mean()*100:+.2f} pp "
            f"(win {float((t0.d_oos_MaxDD > 0).mean()):.1%}) | dOOS CAGR "
            f"{t0.d_oos_CAGR.mean()*100:+.2f} pp (win {float((t0.d_oos_CAGR > 0).mean()):.1%}) | "
            f"dOOS Sharpe win {float((t0.d_oos_Sharpe > 0).mean()):.1%}")
    pd.DataFrame(v3).to_csv(f"{OUT}.v3_legs.csv", index=False)

    # cost ladder: if the win were a COST fact it would grow with bps
    log("   cost ladder (FULL tape, the same 263 keys):")
    for c in COSTS:
        t0 = M[(M.tape == "FULL") & (M.cost == c)]
        t0 = t0[[tuple(r) in base_keys for r in t0[KEY].values]]
        log(f"      {c:2d} bps: wins {int((t0.d_oos_Sharpe > 0).sum())}/{len(t0)}  mean "
            f"{t0.d_oos_Sharpe.mean():+.4f}")

    # ------------------------------------------------------------------- V4 / rule 8: choosers
    log("\n## V4 + RULE 8 — (t, h) or (t, R) chosen on 2009-2016 ONLY; 2017-2026 read once")
    CH = {"C_ISSHARPE": lambda d: d.is_Sharpe,
          "C_ISCALMAR": lambda d: d.is_Calmar,
          "C_ISDD": lambda d: d.is_MaxDD,
          "C_ISLEGS": lambda d: d.is_legs * 1e6 + d.is_Sharpe}
    ch_rows = []
    for (pn, tape, T, c), arm in G.groupby(["panel", "tape", "T_trade", "cost"]):
        for fam in ("CAL", "DRIFT"):
            sub = arm[(arm.family == fam) & ((arm.family == "CAL") | (arm.h > 0))]
            sub = sub.sort_values(["target", "h", "R_refresh"], kind="mergesort")
            for cname, f in CH.items():
                pick = sub.loc[f(sub).astype(float).idxmax()]
                ch_rows.append(dict(panel=pn, tape=tape, T_trade=T, cost=c, family=fam,
                                    chooser=cname, pick_cell=pick.cell, pick_t=pick.target,
                                    oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                                    oos_MaxDD=pick.oos_MaxDD,
                                    keep4b_full=pick.keep4b_full, keep4b_oos=pick.keep4b_oos,
                                    keep4b=pick.keep4b, keep4a=pick.keep4a,
                                    keep4a_oos=pick.keep4a_oos, bind=pick.bind))
    CHd = pd.DataFrame(ch_rows)
    CHd.to_csv(f"{OUT}.choosers.csv", index=False)
    for tape in TAPES:
        s = CHd[(CHd.tape == tape) & (CHd.cost == COST0)]
        log(f"   [{tape:10s}] legal IS-only picks at {COST0} bps: n={len(s)}; 4b FULL+OOS "
            f"{int(s.keep4b.sum())}; 4a {int(s.keep4a.sum())}; by family "
            + "; ".join(f"{f} {int(g.keep4b.sum())}/{len(g)}"
                        for f, g in s.groupby("family")))
    # reachability: does DRIFT reach 4b on strictly more arms than CAL, tape by tape?
    reach = []
    for tape in TAPES:
        s = CHd[(CHd.tape == tape) & (CHd.cost == COST0)]
        a = {f: len({(r.panel, r.T_trade) for _, r in g.iterrows() if r.keep4b})
             for f, g in s.groupby("family")}
        reach.append(dict(tape=tape, CAL_arms=a.get("CAL", 0), DRIFT_arms=a.get("DRIFT", 0)))
        log(f"   [{tape:10s}] arms (panel x trade) where a legal IS pick clears 4b FULL+OOS: "
            f"CAL {a.get('CAL', 0)}/6, DRIFT {a.get('DRIFT', 0)}/6")
    pd.DataFrame(reach).to_csv(f"{OUT}.reach.csv", index=False)

    log("\n## CENSUS (every grid point published in .grid.csv.gz)")
    for tape in TAPES:
        for c in COSTS:
            s = G[(G.tape == tape) & (G.cost == c)]
            log(f"   [{tape:10s}] {c:2d} bps: cells {len(s)}; 4b FULL {int(s.keep4b_full.sum())}, "
                f"4b OOS {int(s.keep4b_oos.sum())}, 4b FULL+OOS {int(s.keep4b.sum())} "
                f"(CAL {int(s[s.family=='CAL'].keep4b.sum())} / "
                f"DRIFT {int(s[s.family=='DRIFT'].keep4b.sum())}); 4a {int(s.keep4a.sum())}, "
                f"4a OOS {int(s.keep4a_oos.sum())}")
    log("   binding 4b leg, FULL tape @10bps: "
        + "; ".join(f"{k} {v}" for k, v in
                    G[(G.tape == "FULL") & (G.cost == COST0)].bind.value_counts().items()))

    GT = pd.DataFrame(_gates)
    GT.to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\n## gates {int(GT.pass_.sum())}/{len(GT)} pass")
    log(f"\n## HEADLINE: V1 {v1_verdict}; V2 "
        f"{'RESOLVED' if v2_ok else 'POINT-ESTIMATE ONLY'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
