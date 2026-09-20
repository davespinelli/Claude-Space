#!/usr/bin/env python3
"""Idea 2042 (lane cloud, 2026-09-20) — IS THE STANDING KEEP-4b MARGIN RESOLVABLE, OR IS IT A
POINT ESTIMATE?

THE DEFECT THIS PRICES.  PROTOCOL rule 4b is five inequalities against SPY — H1 Sharpe, H2
Sharpe, OOS Sharpe, MaxDD <= 0.60x SPY's, CAGR >= 0.70x SPY's — and the record has decided every
capital verdict it has ever issued by reading those five as POINT ESTIMATES.  Not one committed
4b pass carries a standard error on its own legs.  Idea 2022 (this lane, earlier today) showed
what that costs: 1799's "263 of 263" matched-turnover dominance is 24 trading days wide, and a
paired block bootstrap resolves only 61 of the 263 cells at 95%.  That bootstrap was applied to a
book-vs-book contrast.  This run applies the same discipline to the thing capital is actually
allocated on: the book-vs-SPY 4b margin itself.

THE CONSTRUCTION.  The book family is idea 1799's, inherited UNCHANGED and never re-tuned:
equal-weight panel at `gross_t = min(1, t / sigma20_t)`, refreshed either on a CALENDAR
(`R in {D,W,M,Q}`) or on a DRIFT THRESHOLD (`|g_t - gross_held_t| > h`), traded weekly or monthly,
decided at close t and applied at t+1.  Every one of the 420 cells is scored on both KEEP paths at
4 cost rungs (point estimates, `.grid.csv.gz`), and then each of the five 4b legs is given a
PAIRED MOVING-BLOCK BOOTSTRAP in which the BOOK and SPY are resampled on the SAME day blocks, so
the difference is a genuine paired statistic and the common market factor is differenced out.

  Segments are resampled independently, each with its own shared index: FULL (for L4 MaxDD and L5
  CAGR), H1 and H2 (for L1 and L2), OOS (for L3 and for the 4b-OOS legs).  Resampling within a
  segment rather than across the whole tape is what keeps "first half" meaning the first half of
  the sample rather than a blend of eras.  MaxDD on a resampled path is the drawdown of a
  resampled return path, not of the realised one; that is the standard block-bootstrap reading of
  a path statistic and it is flagged wherever it is used.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  RESOLVABLE 4b (FULL).  Of the cells that PASS 4b FULL on point estimates at 10 bps, the
      share whose BINDING (narrowest) leg has its entire two-sided CI on the passing side.  A cell
      that passes only on the point estimate is a POINT-ESTIMATE PASS, not a capital verdict.
  V2  RESOLVABLE 4b (OOS).  The same for the three OOS legs, on the rule-8 out-of-sample window.
  V3  THE REACHED CELL.  Whether the cell a legal IS-only chooser actually lands on (rule 8:
      (t,h) or (t,R) chosen on 2009-2016 alone, 2017-2026 read exactly once) is itself resolvable.
      This is the only cell that could ever carry real capital.
  V4  CAPITAL.  Both KEEP paths at every cell, at 0/10/25/50 bps, point AND resolved.  A cell is
      reported KEEP-4b-RESOLVED only if it passes 4b FULL and OOS on point estimates AND every
      one of its five legs is resolvable at the headline setting.

DIALS.  EXACTLY TWO are tuned, and NEITHER EVER SELECTS A BOOK: BLOCK LENGTH and CONFIDENCE LEVEL.
The book family's own dials (`t`, and `h` or `R`) are idea 1799's, inherited; the rule-8 chooser
spends them exactly as 1799 did.  REPORTED, NOT TUNED: TRADE cadence T in {W,M}, PANEL {U56, B136,
SMALL}, COST {0,10,25,50} bps.  Every grid point is published (`.grid.csv.gz`), every bootstrap
cell (`.legs.csv.gz`), every chooser pick (`.choosers.csv`).  Headline setting is stated up front:
BLOCK = 21 trading days, CONFIDENCE = 95%.

PROTOCOL: rule 2 (10 bps headline, next-day execution, no leverage, gross capped at 1.00); rule 3
(live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time panel.
A bootstrap resamples the tape it is given; it CANNOT put a confidence interval on survivorship,
so a resolvable margin here is still a margin measured on a favourable panel.  SMALL-panel numbers
are not comparable with pre-2026-09-20 SMALL results (the cache grew 439 -> 665 names).

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_4b-margin-resolvable_cloud.py
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

DATE, SLUG = "2026-09-20", "4b-margin-resolvable"
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
OOS_LEGS = ["O1_SHARPE", "O2_DD", "O3_CAGR"]
SIG_L, SIG_D = 20, 0

# the two tuned dials (neither ever selects a book); headline stated up front
BLOCKS = [21, 63]
CONFS = [0.90, 0.95, 0.99]
BLOCK0, CONF0 = 21, 0.95
NBOOT = 500
NBOOT_DEEP = 2000
SEED = 20260924
CHUNK = 10

PUB_MEMO = {"U56":  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
            "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}
PUB_1799_KEEP = dict(panel="U56", T="M", t=0.16, cell="h=0.12",
                     oCAGR=0.1636, oSharpe=1.2810, oMaxDD=-0.1816)

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
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


# ----------------------------------------------- the two refresh runners (idea 1799, unchanged)
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


# --------------------------------------------------------------------------- the bootstrap
def block_idx(n, L, B, rng):
    """Moving-block bootstrap day indices, (B, n)."""
    nb = int(np.ceil(n / L))
    starts = rng.integers(0, max(n - L + 1, 1), size=(B, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(B, nb * L)[:, :n]
    return np.minimum(idx, n - 1)


def boot_sharpe(Rm, idx, chunk=CHUNK):
    """(k, n) returns x (B, n) draws -> (B, k) annualised Sharpe."""
    out = np.empty((idx.shape[0], Rm.shape[0]))
    for a in range(0, idx.shape[0], chunk):
        S = Rm[:, idx[a:a + chunk]]
        mu = S.mean(axis=2)
        sd = S.std(axis=2, ddof=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            out[a:a + chunk] = np.where(sd > 0, mu * np.sqrt(252.0) / sd, np.nan).T
    return out


def boot_cagr_dd(Rm, idx, chunk=CHUNK):
    """(k, n) returns x (B, n) draws -> two (B, k) arrays: CAGR and MaxDD of the resampled path."""
    B, n = idx.shape
    yrs = n / 252.0
    cg = np.empty((B, Rm.shape[0]))
    dd = np.empty((B, Rm.shape[0]))
    for a in range(0, B, chunk):
        S = Rm[:, idx[a:a + chunk]]
        eq = np.cumprod(1.0 + S, axis=2)
        cg[a:a + chunk] = (eq[:, :, -1] ** (1.0 / yrs) - 1.0).T
        dd[a:a + chunk] = (eq / np.maximum.accumulate(eq, axis=2) - 1.0).min(axis=2).T
    return cg, dd


# ----------------------------------------------------------------------------- run
def main():
    rng = np.random.default_rng(SEED)
    log(f"# Idea 2042 (lane cloud, {DATE}) — is the standing KEEP-4b MARGIN resolvable, or a "
        f"point estimate?")
    log(f"# tuned dials (2, neither ever selects a book): BLOCK {BLOCKS}, CONFIDENCE {CONFS}.  "
        f"HEADLINE block {BLOCK0}, confidence {CONF0:.0%}.")
    log(f"# book family inherited from idea 1799, NOT re-tuned: t {TARGETS} x [ h {H_GRID} | "
        f"R {REFRESH} ], trade T {TRADES}.  REPORTED: panel, cost {COSTS} bps.")
    log(f"# warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}; B={NBOOT} (deep {NBOOT_DEEP}), "
        f"seed {SEED}.  Book and SPY resampled on the SAME blocks, segment by segment.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0")

    rows, leg_rows = [], []
    g1r = g1t = g2 = g3 = g4 = g9 = 0.0
    g4n = 0
    gPAIR = []
    deep_store = {}

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        bk = Book(px, cols, px.index)
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")

        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        S = dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]))
        S["h1"], S["h2"] = halves(spy)
        S["ish1"], S["ish2"] = halves(spy.loc[:IS_END])
        LIVE = {}
        for c in COSTS:
            r = net(lr, lt, c)
            LIVE[c] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                           h1=halves(r)[0], h2=halves(r)[1])
        log(f"   LIVE RULES v2 (W,{COST0}bps) {LIVE[COST0]['full']['CAGR']:.2%} / "
            f"{LIVE[COST0]['full']['Sharpe']:.4f} / {LIVE[COST0]['full']['MaxDD']:.2%}  "
            f"(OOS {LIVE[COST0]['oos']['CAGR']:.2%} / {LIVE[COST0]['oos']['Sharpe']:.4f} / "
            f"{LIVE[COST0]['oos']['MaxDD']:.2%})")
        log(f"   SPY                       {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}  (OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%});  4b bars: DD cap {DD_CAP*S['full']['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*S['full']['CAGR']:.2%}")

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

        # ------------------------------------------------------------------- the grid
        series10 = {}                 # (target, T, cell) -> net@10bps daily returns
        for tgt in TARGETS:
            g0 = bk.g_of(tgt)
            for T in TRADES:
                cells = ([("CAL", Rc, np.nan) for Rc in REFRESH]
                         + [("DRIFT", "h", h) for h in THRESH])
                cal_ref = {}
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
                    yrs = len(r0) / 252.0
                    for c in COSTS:
                        r = net(r0, t0, c)
                        if c == COST0:
                            series10[(tgt, T, label)] = r
                        mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                        h1, h2 = halves(r)
                        ih1, ih2 = halves(r.loc[:IS_END])
                        mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
                               "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
                               "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
                               "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
                        omar = {"O1_SHARPE": mo["Sharpe"] - S["oos"]["Sharpe"],
                                "O2_DD": mo["MaxDD"] - DD_CAP * S["oos"]["MaxDD"],
                                "O3_CAGR": mo["CAGR"] - CAGR_FLOOR * S["oos"]["CAGR"]}
                        bl, nbad = binding(mar)
                        LV = LIVE[c]
                        k4bf = all(v > 0 for v in mar.values())
                        k4bo = all(v > 0 for v in omar.values())
                        k4a = (h1 > LV["h1"] and h2 > LV["h2"]
                               and mf["MaxDD"] >= LV["full"]["MaxDD"])
                        k4ao = (mo["Sharpe"] > LV["oos"]["Sharpe"]
                                and mo["MaxDD"] >= LV["oos"]["MaxDD"])
                        is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
                                   + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
                                   + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
                        rows.append(dict(
                            panel=pname, target=tgt, T_trade=T, family=fam, R_refresh=Rc, h=h,
                            cell=label, cost=c, turn_py=float(t0.sum() / yrs),
                            refresh_py=nref / (len(px) / 252.0), gross_mean=float(gs.mean()),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                            is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                            is_H1=ih1, is_H2=ih2, is_legs=is_legs,
                            is_Calmar=(mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan),
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            **{k: float(v) for k, v in mar.items()},
                            **{k: float(v) for k, v in omar.items()},
                            bind=bl, n_fail=nbad, keep4b_full=k4bf, keep4b_oos=k4bo,
                            keep4b=(k4bf and k4bo), keep4a=k4a, keep4a_oos=k4ao))
        log(f"   grid done ({len([r for r in rows if r['panel'] == pname])} scored rows)")

        # ------------------------------------------- paired block bootstrap on the 4b legs
        keys = list(series10)
        Rm = np.vstack([series10[k].values for k in keys])              # (130, n)
        sv = spy.values
        n = Rm.shape[1]
        half = n // 2
        segs = {"FULL": np.arange(n), "H1": np.arange(half), "H2": np.arange(half, n),
                "OOS": np.where(spy.index >= pd.Timestamp(OOS_START))[0]}
        for L in BLOCKS:
            draws = {sg: block_idx(len(ii), L, NBOOT, rng) for sg, ii in segs.items()}
            bs = {}
            for sg, ii in segs.items():
                Rs, Ss = Rm[:, ii], sv[ii][None, :]
                idx = draws[sg]
                bs[(sg, "SH")] = boot_sharpe(Rs, idx) - boot_sharpe(Ss, idx)
                if sg in ("FULL", "OOS"):
                    cg_b, dd_b = boot_cagr_dd(Rs, idx)
                    cg_s, dd_s = boot_cagr_dd(Ss, idx)
                    bs[(sg, "CG")] = cg_b - CAGR_FLOOR * cg_s
                    bs[(sg, "DD")] = dd_b - DD_CAP * dd_s
            legmap = {"L1_H1": ("H1", "SH"), "L2_H2": ("H2", "SH"), "L3_OOS": ("OOS", "SH"),
                      "L4_DD": ("FULL", "DD"), "L5_CAGR": ("FULL", "CG"),
                      "O1_SHARPE": ("OOS", "SH"), "O2_DD": ("OOS", "DD"),
                      "O3_CAGR": ("OOS", "CG")}
            for j, (tgt, T, label) in enumerate(keys):
                pt = next(r for r in rows if r["panel"] == pname and r["target"] == tgt
                          and r["T_trade"] == T and r["cell"] == label and r["cost"] == COST0)
                rec = dict(panel=pname, target=tgt, T_trade=T, cell=label, block=L)
                for leg, (sg, kind) in legmap.items():
                    d = bs[(sg, kind)][:, j]
                    rec[f"{leg}_pt"] = pt[leg]
                    rec[f"{leg}_se"] = float(d.std(ddof=1))
                    rec[f"{leg}_pgt0"] = float((d > 0).mean())
                    for cf in CONFS:
                        a = (1 - cf) / 2 * 100
                        lo, hi = np.percentile(d, [a, 100 - a])
                        rec[f"{leg}_lo{int(cf*100)}"] = float(lo)
                        rec[f"{leg}_hi{int(cf*100)}"] = float(hi)
                leg_rows.append(rec)
                if L == BLOCK0:
                    deep_store[(pname, tgt, T, label)] = None
            # G-PAIR: the SPY leg must be identical across cells of one draw (true pairing)
            gPAIR.append(float(np.abs(bs[("FULL", "SH")][:, 0] - bs[("FULL", "SH")][:, 1]
                                      - (boot_sharpe(Rm[:1, segs["FULL"]], draws["FULL"])[:, 0]
                                         - boot_sharpe(Rm[1:2, segs["FULL"]],
                                                       draws["FULL"])[:, 0])).max()))
        log(f"   bootstrap done ({len(keys)} cells x {len(BLOCKS)} block lengths x {NBOOT} draws)")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    LG = pd.DataFrame(leg_rows)
    LG.to_csv(f"{OUT}.legs.csv.gz", index=False, compression="gzip")

    # ------------------------------------------------------------------------ gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 bt_cal diagonal == engine.backtest (returns / turnover)",
         f"{g1r:.3e} / {g1t:.3e}", "< 1e-12", max(g1r, g1t) < 1e-12)
    gate("G2 cost identity r(c) = r0 - turn*c/1e4 == fresh engine run at 10/25 bps",
         f"{g2:.3e}", "< 1e-12", g2 < 1e-12)
    for pn, pub in PUB_MEMO.items():
        row = G[(G.panel == pn) & (G.target == TGT_MEMO) & (G.T_trade == "W")
                & (G.family == "CAL") & (G.R_refresh == "W") & (G.cost == COST0)].iloc[0]
        g3 = max(g3, max(abs(row.CAGR - pub["CAGR"]), abs(row.Sharpe - pub["Sharpe"]),
                         abs(row.MaxDD - pub["MaxDD"]), abs(row.oos_CAGR - pub["oCAGR"]),
                         abs(row.oos_Sharpe - pub["oSharpe"])))
    gate("G3 reproduces the standing VOLTGT memo (points 2-4, U56 + B136)",
         f"max|d| = {g3:.3e}", "< 1e-3", g3 < 1e-3)
    gate(f"G4 DRIFT h=0 == CALENDAR R=D, cell by cell ({g4n} cells)", f"{g4:.3e}", "< 1e-12",
         g4 < 1e-12 and g4n == len(TARGETS) * len(TRADES) * len(PS))
    kp = G[(G.panel == PUB_1799_KEEP["panel"]) & (G.target == PUB_1799_KEEP["t"])
           & (G.T_trade == PUB_1799_KEEP["T"]) & (G.cell == PUB_1799_KEEP["cell"])
           & (G.cost == COST0)].iloc[0]
    g5 = max(abs(kp.oos_CAGR - PUB_1799_KEEP["oCAGR"]),
             abs(kp.oos_Sharpe - PUB_1799_KEEP["oSharpe"]),
             abs(kp.oos_MaxDD - PUB_1799_KEEP["oMaxDD"]))
    gate("G5 reproduces the standing KEEP-4b cell (U56, T=M, t=0.16, h=0.12)",
         f"max|d| = {g5:.3e}", "< 1e-3", g5 < 1e-3)
    gate("G6 gross never levered", f"max gross {g9:.6f}", "<= 1.0 + 1e-9", g9 <= 1.0 + 1e-9)
    gate("G7 the bootstrap is PAIRED (the shared SPY leg cancels in a cell-vs-cell difference)",
         f"max|d| = {max(gPAIR):.3e}", "< 1e-12", max(gPAIR) < 1e-12)
    ok_se = float(LG[[f"{lg}_se" for lg in LEGS]].min().min())
    gate("G8 every leg has a non-degenerate bootstrap SE", f"min SE {ok_se:.3e}", "> 0", ok_se > 0)

    # ------------------------------------------------------------------ V1 / V2: resolvability
    def resolved(df, legs, cf):
        """A cell is resolved iff EVERY leg's (1-cf) two-sided CI lies entirely above zero."""
        m = np.ones(len(df), bool)
        for lg in legs:
            m &= (df[f"{lg}_lo{int(cf*100)}"].values > 0)
        return m

    M = G[G.cost == COST0].merge(LG, on=["panel", "target", "T_trade", "cell"],
                                 suffixes=("", "_b"))
    M.to_csv(f"{OUT}.merged.csv.gz", index=False, compression="gzip")

    log("\n## V1 / V2 — HOW MANY 4b PASSES SURVIVE A PAIRED SE?")
    summ = []
    for L in BLOCKS:
        for cf in CONFS:
            s = M[M.block == L]
            pf, po = s.keep4b_full.values, s.keep4b_oos.values
            rf, ro = resolved(s, LEGS, cf), resolved(s, OOS_LEGS, cf)
            both_pt = pf & po
            both_rs = both_pt & rf & ro
            summ.append(dict(block=L, conf=cf, cells=len(s), pass4b_full=int(pf.sum()),
                             resolved_full=int((pf & rf).sum()), pass4b_oos=int(po.sum()),
                             resolved_oos=int((po & ro).sum()),
                             pass_both=int(both_pt.sum()), resolved_both=int(both_rs.sum())))
            star = "  <-- HEADLINE" if (L == BLOCK0 and cf == CONF0) else ""
            log(f"   block {L:2d}, {cf:.0%}: 4b FULL {int(pf.sum())}/{len(s)} point -> "
                f"**{int((pf & rf).sum())} resolved**; 4b OOS {int(po.sum())} -> "
                f"{int((po & ro).sum())}; 4b FULL+OOS {int(both_pt.sum())} -> "
                f"**{int(both_rs.sum())} resolved**{star}")
    SM = pd.DataFrame(summ)
    SM.to_csv(f"{OUT}.resolvable.csv", index=False)

    s0 = M[M.block == BLOCK0]
    log(f"\n   which leg is unresolvable (block {BLOCK0}, {CONF0:.0%}, among the "
        f"{int(s0.keep4b_full.sum())} point-passing 4b FULL cells):")
    p0 = s0[s0.keep4b_full]
    for lg in LEGS:
        bad = int((p0[f"{lg}_lo{int(CONF0*100)}"] <= 0).sum())
        log(f"      {lg:9s} CI covers 0 at {bad}/{len(p0)}  (mean point {p0[f'{lg}_pt'].mean():+.4f},"
            f" mean SE {p0[f'{lg}_se'].mean():.4f}, mean t "
            f"{(p0[f'{lg}_pt'] / p0[f'{lg}_se']).mean():+.2f})")
    # --- the DD leg is a PATH statistic; a moving-block resample is a biased estimator for it,
    #     so the "all five legs" count is decomposed and the bias is measured, not asserted.
    log(f"\n   DECOMPOSITION — the four NON-PATH legs (L1, L2, L3, L5) alone:")
    nondd = [lg for lg in LEGS if lg != "L4_DD"]
    dec = []
    for L in BLOCKS:
        for cf in CONFS:
            s = M[M.block == L]
            p = s[s.keep4b_full]
            r4 = np.ones(len(p), bool)
            for lg in nondd:
                r4 &= (p[f"{lg}_lo{int(cf*100)}"].values > 0)
            po = s[s.keep4b_oos]
            ro = np.ones(len(po), bool)
            for lg in ("O1_SHARPE", "O3_CAGR"):
                ro &= (po[f"{lg}_lo{int(cf*100)}"].values > 0)
            dec.append(dict(block=L, conf=cf, n4b_full=len(p), resolved_nonDD=int(r4.sum()),
                            n4b_oos=len(po), resolved_oos_nonDD=int(ro.sum())))
            log(f"      block {L:2d}, {cf:.0%}: {int(r4.sum())}/{len(p)} ({r4.mean():.1%}) of the "
                f"4b-FULL passes resolve on all four non-path legs; OOS {int(ro.sum())}/{len(po)} "
                f"({ro.mean():.1%}) on its two non-path legs")
    pd.DataFrame(dec).to_csv(f"{OUT}.nonpath.csv", index=False)

    log(f"\n   BIAS DIAGNOSTIC — is the block bootstrap centred on the point estimate?"
        f"  (block {BLOCK0}, {CONF0:.0%} CI midpoint vs point, over the {int(s0.keep4b_full.sum())} "
        f"passing cells)")
    bias = []
    pp = s0[s0.keep4b_full]
    for lg in LEGS:
        mid = (pp[f"{lg}_lo{int(CONF0*100)}"] + pp[f"{lg}_hi{int(CONF0*100)}"]) / 2
        sh = float(mid.mean() - pp[f"{lg}_pt"].mean())
        rel = sh / float(pp[f"{lg}_pt"].mean()) if float(pp[f"{lg}_pt"].mean()) else np.nan
        bias.append(dict(leg=lg, point=float(pp[f"{lg}_pt"].mean()), ci_mid=float(mid.mean()),
                         shift=sh, shift_rel=rel))
        log(f"      {lg:9s} point {pp[f'{lg}_pt'].mean():+.4f}  CI-mid {mid.mean():+.4f}  "
            f"shift {sh:+.4f}  ({rel:+.1%} of the point margin)")
    BI = pd.DataFrame(bias)
    BI.to_csv(f"{OUT}.bias.csv", index=False)
    dd_rel = float(BI.loc[BI.leg == "L4_DD", "shift_rel"].iloc[0])
    oth = float(BI.loc[BI.leg != "L4_DD", "shift_rel"].abs().max())
    gate("G9 the path-statistic bias is confined to the DD leg",
         f"L4_DD {dd_rel:+.1%} vs max |shift| on the four non-path legs {oth:.1%}",
         "|DD shift| > 5x the largest non-path shift", abs(dd_rel) > 5 * oth)

    log("   by panel (4b FULL point -> resolved): " + "; ".join(
        f"{p} {int(g.keep4b_full.sum())} -> {int((g.keep4b_full.values & resolved(g, LEGS, CONF0)).sum())}"
        for p, g in s0.groupby("panel")))

    # ------------------------------------------------------- V3 / V4: rule 8 and the reached cell
    log(f"\n## V3 + V4 — RULE 8: (t,h) or (t,R) chosen on 2009-2016 ONLY; 2017-2026 read once")
    CH = {"C_ISSHARPE": lambda d: d.is_Sharpe, "C_ISCALMAR": lambda d: d.is_Calmar,
          "C_ISDD": lambda d: d.is_MaxDD,
          "C_ISLEGS": lambda d: d.is_legs * 1e6 + d.is_Sharpe}
    ch_rows = []
    for (pn, T, c), arm in G.groupby(["panel", "T_trade", "cost"]):
        for fam in ("CAL", "DRIFT"):
            sub = arm[(arm.family == fam) & ((arm.family == "CAL") | (arm.h > 0))]
            sub = sub.sort_values(["target", "h", "R_refresh"], kind="mergesort")
            for cname, f in CH.items():
                pk = sub.loc[f(sub).astype(float).idxmax()]
                rec = dict(panel=pn, T_trade=T, cost=c, family=fam, chooser=cname,
                           pick_cell=pk.cell, pick_t=pk.target, CAGR=pk.CAGR, Sharpe=pk.Sharpe,
                           MaxDD=pk.MaxDD, H1=pk.H1, H2=pk.H2, oos_CAGR=pk.oos_CAGR,
                           oos_Sharpe=pk.oos_Sharpe, oos_MaxDD=pk.oos_MaxDD,
                           keep4b_full=pk.keep4b_full, keep4b_oos=pk.keep4b_oos,
                           keep4b=pk.keep4b, keep4a=pk.keep4a, keep4a_oos=pk.keep4a_oos,
                           bind=pk.bind)
                if c == COST0:
                    b = s0[(s0.panel == pn) & (s0.T_trade == T) & (s0.target == pk.target)
                           & (s0.cell == pk.cell)]
                    if len(b):
                        b = b.iloc[0]
                        rec["resolved_full"] = bool(all(
                            b[f"{lg}_lo{int(CONF0*100)}"] > 0 for lg in LEGS))
                        rec["resolved_oos"] = bool(all(
                            b[f"{lg}_lo{int(CONF0*100)}"] > 0 for lg in OOS_LEGS))
                        rec["worst_leg"] = min(LEGS, key=lambda lg: b[f"{lg}_pt"] / b[f"{lg}_se"])
                        rec["worst_t"] = float(min(b[f"{lg}_pt"] / b[f"{lg}_se"] for lg in LEGS))
                ch_rows.append(rec)
    CHd = pd.DataFrame(ch_rows)
    CHd.to_csv(f"{OUT}.choosers.csv", index=False)
    c0 = CHd[CHd.cost == COST0]
    log(f"   legal IS-only picks at {COST0} bps: n={len(c0)}; 4b FULL+OOS {int(c0.keep4b.sum())} "
        f"(point); RESOLVED at {CONF0:.0%} "
        f"{int((c0.keep4b & c0.resolved_full.fillna(False) & c0.resolved_oos.fillna(False)).sum())}"
        f"; 4a {int(c0.keep4a.sum())}")
    rp = c0[c0.keep4b]
    if len(rp):
        log("   every reached 4b cell, with its weakest leg:")
        for _, r in rp.iterrows():
            log(f"      {r.panel}/{r.T_trade} {r.chooser} {r.pick_cell} t={r.pick_t}: "
                f"OOS {r.oos_CAGR:.2%}/{r.oos_Sharpe:.4f}/{r.oos_MaxDD:.2%}  "
                f"weakest leg {r.worst_leg} t={r.worst_t:+.2f}  "
                f"resolved FULL {bool(r.resolved_full)} / OOS {bool(r.resolved_oos)}")

    # ---- the standing KEEP cell, deep bootstrap -------------------------------------------
    log(f"\n## THE STANDING KEEP-4b CELL — deep paired bootstrap (B={NBOOT_DEEP}, block {BLOCK0})")
    pn, T, tg, cl = (PUB_1799_KEEP["panel"], PUB_1799_KEEP["T"], PUB_1799_KEEP["t"],
                     PUB_1799_KEEP["cell"])
    px = dict((p, x) for p, x, _ in PS)[pn]
    cols = dict((p, c) for p, _, c in PS)[pn]
    st = px.index[WARMUP]
    bkq = Book(px, cols, px.index)
    r0, t0, _, _ = bkq.run_drift(bkq.g_of(tg), T, float(cl.split("=")[1]))
    rq = net(r0.loc[st:], t0.loc[st:], COST0)
    sq = px["SPY"].pct_change().fillna(0.0).loc[st:]
    nq = len(rq)
    halfq = nq // 2
    segq = {"FULL": np.arange(nq), "H1": np.arange(halfq), "H2": np.arange(halfq, nq),
            "OOS": np.where(sq.index >= pd.Timestamp(OOS_START))[0]}
    deep = {}
    for sg, ii in segq.items():
        idx = block_idx(len(ii), BLOCK0, NBOOT_DEEP, rng)
        Rs = rq.values[ii][None, :]
        Ss = sq.values[ii][None, :]
        deep[(sg, "SH")] = (boot_sharpe(Rs, idx) - boot_sharpe(Ss, idx))[:, 0]
        if sg in ("FULL", "OOS"):
            cb, db = boot_cagr_dd(Rs, idx)
            cs, ds = boot_cagr_dd(Ss, idx)
            deep[(sg, "CG")] = (cb - CAGR_FLOOR * cs)[:, 0]
            deep[(sg, "DD")] = (db - DD_CAP * ds)[:, 0]
    legmap = {"L1_H1": ("H1", "SH"), "L2_H2": ("H2", "SH"), "L3_OOS": ("OOS", "SH"),
              "L4_DD": ("FULL", "DD"), "L5_CAGR": ("FULL", "CG"),
              "O2_DD": ("OOS", "DD"), "O3_CAGR": ("OOS", "CG")}
    drows = []
    for lg, (sg, kind) in legmap.items():
        d = deep[(sg, kind)]
        pt = float(kp[lg]) if lg in kp.index else np.nan
        se = float(d.std(ddof=1))
        rec = dict(leg=lg, point=pt, se=se, t=pt / se if se else np.nan,
                   p_gt0=float((d > 0).mean()))
        for cf in CONFS:
            a = (1 - cf) / 2 * 100
            lo, hi = np.percentile(d, [a, 100 - a])
            rec[f"lo{int(cf*100)}"] = float(lo)
            rec[f"hi{int(cf*100)}"] = float(hi)
        drows.append(rec)
        log(f"   {lg:9s} point {pt:+.4f}  SE {se:.4f}  t {pt/se if se else np.nan:+.2f}  "
            f"P(>0) {float((d > 0).mean()):.3f}  "
            + "  ".join(f"{int(cf*100)}% [{rec[f'lo{int(cf*100)}']:+.4f}, "
                        f"{rec[f'hi{int(cf*100)}']:+.4f}]" for cf in CONFS))
    DP = pd.DataFrame(drows)
    DP.to_csv(f"{OUT}.deep.csv", index=False)
    weak = DP.loc[DP.t.idxmin()]
    log(f"   WEAKEST LEG: {weak.leg} at t = {weak.t:+.2f}; the cell is "
        f"{'RESOLVED' if (DP[DP.leg.isin(LEGS)][f'lo{int(CONF0*100)}'] > 0).all() else 'NOT RESOLVED'}"
        f" at {CONF0:.0%} on the FULL legs")

    # ----------------------------------------------------------------------------- census
    log("\n## CENSUS (every grid point published in .grid.csv.gz)")
    for c in COSTS:
        s = G[G.cost == c]
        log(f"   {c:2d} bps: cells {len(s)}; 4b FULL {int(s.keep4b_full.sum())}, 4b OOS "
            f"{int(s.keep4b_oos.sum())}, 4b FULL+OOS {int(s.keep4b.sum())} "
            f"(CAL {int(s[s.family=='CAL'].keep4b.sum())} / "
            f"DRIFT {int(s[s.family=='DRIFT'].keep4b.sum())}); 4a {int(s.keep4a.sum())}, "
            f"4a OOS {int(s.keep4a_oos.sum())}")
    log("   binding 4b leg @10bps: " + "; ".join(
        f"{k} {v}" for k, v in G[G.cost == COST0].bind.value_counts().items()))

    GT = pd.DataFrame(_gates)
    GT.to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\n## gates {int(GT.pass_.sum())}/{len(GT)} pass")
    hl = SM[(SM.block == BLOCK0) & (SM.conf == CONF0)].iloc[0]
    log(f"\n## HEADLINE: at block {BLOCK0} / {CONF0:.0%}, {hl.pass4b_full} of 420 cells pass 4b "
        f"FULL on point estimates and {hl.resolved_full} are resolvable; 4b FULL+OOS "
        f"{hl.pass_both} -> {hl.resolved_both}.")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
