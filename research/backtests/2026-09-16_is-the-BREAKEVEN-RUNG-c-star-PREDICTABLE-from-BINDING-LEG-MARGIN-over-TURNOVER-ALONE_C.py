#!/usr/bin/env python3
"""Idea 1097 (lane C, 2026-09-16) — is the BREAKEVEN RUNG c* PREDICTABLE from BINDING-LEG
MARGIN over TURNOVER ALONE?

QUESTION (QUEUE idea 1097, verbatim)
    idea 1094 solved c* exactly on a 201-rung ladder for 54 cells and found Spearman(c*,
    turnover) only -0.65, because the binding leg decides: a DD-bound cell is nearly
    cost-immune (8-42x less |MaxDD| than CAGR moved per 50 bps) while a Sharpe-bound one is
    not.  Fit c* ~ margin/turnover per leg and report whether one closed form replaces the
    ladder.  Max 2 params (leg, fit form).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials, both named by the queue:
      LEG  in {L_H1, L_H2, L_OOS, L_DD, L_CAGR, O_S, O_DD, O_CAGR}  (8)
      FORM in {F_RAW, F_UNIT, F_K1, F_KLEG}                          (4)
    ALL 32 (leg, form) points are published, plus the derived CONJUNCTION reading.
    FROZEN, and NOT dials: 1082/1086/1094's N ladder {5,8,10,12,15,20,25,30,40} x H
    {21,63,126} = 27 cells per panel, 54 in all, every one reported; cap INF; CAND20 legs;
    max_vol 0.60; gross 0.75; weekly cadence; LAG 1; warm-up 260; IS end 2016-12-31; the 4b
    constants 0.60 / 0.70.  COST IS NOT A DIAL (PROTOCOL rule 2 fixes it at 10 bps): it is
    the axis whose breakeven this run tries to predict, and nothing is ever selected on it.

THE OBJECT BEING PREDICTED
    engine.backtest computes r(c) = g - tn*c/1e4 with neither g nor tn depending on c, so one
    run per cell yields the whole ladder EXACTLY (gate G1).  For leg L with statistic x_L and
    bar b_L, the margin is m_L(c) = x_L(c) - b_L and the TRUE per-leg breakeven c*_L is the
    largest rung on the 0..200 bps 1-bp ladder at which m_L >= 0 (contiguity from 0 recorded
    at every point).  The CONJUNCTION c* of 1094 is min_L c*_L; G7 checks that identity.

THE FOUR FORMS (the second dial), all predicting c*_L in bps
    F_RAW   chat = 1e4 * m_L(0) / tn_L                      <- the queue's LITERAL proposal,
                                                               no fitted parameter at all.
    F_UNIT  analytic unit conversion, still NO fitted parameter.  Cost enters as an annual
            drag d = tn*c/1e4, so: CAGR legs 1e4*m/tn (identical to F_RAW); Sharpe legs
            1e4*m*sigma_L/tn_L (S ~ (mu-d)/sigma); DD legs 1e4*m/(tn_L*dt_L) where dt_L is
            the length IN YEARS of the book's own peak-to-trough episode at 0 bps.
    F_K1    chat = k * F_RAW, ONE global k.
    F_KLEG  chat = k_L * F_RAW, ONE k per leg  <- the queue's "per leg" fit.
    EVERY k is fitted on U56 ALONE (median of c*_true / chat_RAW over U56's fit points).
    B136 is a PURE HOLD-OUT: no B136 number enters any fit.

DECLARED BEFORE ANY NUMBER (hypotheses.csv records each with its pre-registered prediction)
    H_RAW      the queue's literal margin/turnover form lands within PROTOCOL's own 10 bps
               rung at >= half the (cell, leg) points.  PREDICTED FAIL: the Sharpe and DD
               legs are not in CAGR units, so a unit-free ratio cannot be right for them.
    H_UNIT     the parameter-free unit conversion reaches median |err| <= 10 bps on ALL 8
               legs.  PREDICTED PASS on CAGR and Sharpe legs, UNCERTAIN on DD.
    H_LINEAR   each leg is near-linear in c: the breakeven implied by the slope measured on
               0->10 bps alone lands within 5 bps of the true ladder value at every cell.
    H_ONEFORM  THE HEADLINE.  One form replaces the ladder: median |err| <= 5 bps on every
               leg AND ZERO 4b verdict flips at 10 / 25 / 50 bps on the HOLD-OUT panel.
    H_MIN      c*(conjunction) == min_L c*_L exactly at every cell where it is defined.
    H_BINDING  the closed form names the correct BINDING leg at >= 80% of cells.
    H_RHO      1094's Spearman(c*, turnover) = -0.65 reproduces AND is a statement about the
               cells that HAVE a finite c*, not about 54.  PREDICTED: it is unresolved.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level is
    optimistic, every 4b/4a count is an UPPER bound, and every breakeven rung c* -- true or
    predicted -- is an UPPER bound on the cost a real book of this kind could have paid.
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

DATE = "2026-09-16"
SLUG = "is-the-BREAKEVEN-RUNG-c-star-PREDICTABLE-from-BINDING-LEG-MARGIN-over-TURNOVER-ALONE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ, CAPNAME = 0.75, "W", "INF"
MOMLEGS = [(21, 252), (0, 126), (0, 63)]
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]
HS = [21, 63, 126]
PANELS = ["U56", "B136"]
FITPANEL = "U56"                      # k fitted here ONLY; B136 never enters a fit
CFINE = np.arange(0.0, 200.5, 1.0)    # 201 rungs, 1094's ladder verbatim
RUNGS = [10.0, 25.0, 50.0]            # verdict rungs (PROTOCOL's, plus 1094's two)
PROTOCOL_RUNG = 10.0
FULL_LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
OOS_LEGS = ["O_S", "O_DD", "O_CAGR"]
ALL_LEGS = FULL_LEGS + OOS_LEGS
FORMS = ["F_RAW", "F_UNIT", "F_K1", "F_KLEG"]

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
C1094 = Path(__file__).resolve().parent / (
    "2026-09-16_does-the-U56-n12-H21-CANDIDATE-survive-25-and-50-bps_C.breakeven.csv")
D1094 = Path(__file__).resolve().parent / (
    "2026-09-16_does-the-U56-n12-H21-CANDIDATE-survive-25-and-50-bps_C.diagnostics.csv")
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------------------------------ mechanics (1094's, verbatim)
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def fvol(r):
    return float(np.asarray(r, float).std(ddof=1) * np.sqrt(252.0))


def dd_years(r):
    """Length in YEARS of the peak-to-trough episode that realises MaxDD (F_UNIT's dt_L)."""
    eq = np.cumprod(1.0 + np.asarray(r, float))
    pk = np.maximum.accumulate(eq)
    i = int((eq / pk - 1.0).argmin())
    j = int(np.argmax(eq[: i + 1] >= pk[i] - 1e-15))
    return max((i - j) / 252.0, 1.0 / 252.0)


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def mech(px):
    parts = []
    for skip, look in MOMLEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel = []
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[priced[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        nsel.append(len(sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W, np.array(nsel)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def margins(b, sb):
    """Each 4b leg's margin IN ITS OWN UNITS.  >= 0 means the leg passes."""
    return {"L_H1": b["H1"] - sb["H1"],
            "L_H2": b["H2"] - sb["H2"],
            "L_OOS": b["OOS_Sharpe"] - sb["OOS_Sharpe"],
            "L_DD": DD_CAP * abs(sb["MaxDD"]) - abs(b["MaxDD"]),
            "L_CAGR": b["CAGR"] - CAGR_FLOOR * sb["CAGR"],
            "O_S": b["OOS_Sharpe"] - sb["OOS_Sharpe"],
            "O_DD": DD_CAP * abs(sb["OOS_MaxDD"]) - abs(b["OOS_MaxDD"]),
            "O_CAGR": b["OOS_CAGR"] - CAGR_FLOOR * sb["OOS_CAGR"]}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def cstar_from_margin(mvec):
    """(c*, contiguous, dead_at_0) from a margin array over CFINE.  c* = last rung with m >= 0,
    counting only the run that starts at 0 bps.  NaN if it already fails at 0 bps."""
    ok = np.asarray(mvec) >= 0.0
    if not ok[0]:
        return np.nan, True, True
    run = int(np.argmin(ok)) if (~ok).any() else len(ok)
    contiguous = bool(ok[:run].all() and not ok[run:].any())
    return float(CFINE[run - 1]), contiguous, False


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none); average ranks for ties."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    a, b = a[m], b[m]
    if len(a) < 3:
        return np.nan
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def ann_turn(tn, mask, ):
    n = int(mask.sum())
    return float(tn[mask].sum() / (n / 252.0)) if n else np.nan


def main():
    t0 = time.time()
    P(f"# Idea 1097 (lane C, {DATE}) — is the BREAKEVEN RUNG c* PREDICTABLE from BINDING-LEG")
    P("#   MARGIN over TURNOVER ALONE?")
    P(f"# TWO DIALS, both the queue's: LEG {ALL_LEGS} x FORM {FORMS} = 32 points, ALL published.")
    P(f"# FROZEN (not dials): N {NS} x H {HS} = 54 cells, all reported; cap {CAPNAME}; CAND20 legs")
    P(f"#   {MOMLEGS}; max_vol {MAXVOL}; gross {GROSS0}; cadence {FREQ}; LAG {LAG}; warm-up")
    P(f"#   {WARMUP}; IS end {IS_END}; 4b constants {DD_CAP}/{CAGR_FLOOR}.  COST is NOT a dial.")
    P(f"# k IS FITTED ON {FITPANEL} ALONE.  B136 is a pure hold-out — no B136 number enters a fit.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_RAW      margin/turnover alone lands within 10 bps at >= half the points.  PREDICTED")
    P("#              FAIL (Sharpe and DD legs are not in CAGR units).")
    P("#   H_UNIT     the parameter-free unit conversion reaches median |err| <= 10 bps on all 8")
    P("#              legs.  PREDICTED PASS on CAGR/Sharpe, UNCERTAIN on DD.")
    P("#   H_LINEAR   the 0->10 bps slope alone puts c* within 5 bps at EVERY cell.")
    P("#   H_ONEFORM  HEADLINE — one form replaces the ladder: median |err| <= 5 bps on every leg")
    P("#              AND zero 4b verdict flips at 10/25/50 bps on the HOLD-OUT panel.")
    P("#   H_MIN      conjunction c* == min_L c*_L exactly wherever defined.")
    P("#   H_BINDING  the closed form names the true binding leg at >= 80% of cells.")
    P("#   H_RHO      1094's rho(c*, turnover) = -0.65 reproduces, and is a statement about the")
    P("#              cells that HAVE a finite c*, not about 54.  PREDICTED: unresolved.")
    P("")

    gates, cellrows, ladderrows, benchrows, picks, diagrows = {}, [], [], [], [], []
    panel_store = {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        warm, ins, oos = windows(idx)
        h = int(warm.sum()) // 2
        wi = np.flatnonzero(warm)
        h1m = np.zeros(T, dtype=bool); h1m[wi[:h]] = True
        h2m = np.zeros(T, dtype=bool); h2m[wi[h:]] = True
        WIN = {"L_H1": h1m, "L_H2": h2m, "L_OOS": oos, "L_DD": warm, "L_CAGR": warm,
               "O_S": oos, "O_DD": oos, "O_CAGR": oos}
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)
        yrs = warm.sum() / 252.0

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live0 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        live_g, live_tn = live0["returns"].values, live0["turnover"].values
        lb10 = blocks(live_g - live_tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)
        panel_store[panel] = dict(sb=sb, lb10=lb10, yrs=yrs)

        P(f"## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalances, {yrs:.2f} scored years")
        P(f"   SPY (uncharged 4b bar)  full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}"
          f"  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2 @10 bps  full {lb10['CAGR']:.2%} / {lb10['Sharpe']:.4f} / {lb10['MaxDD']:.2%}"
          f"  OOS {lb10['OOS_CAGR']:.2%} / {lb10['OOS_Sharpe']:.4f} / {lb10['OOS_MaxDD']:.2%}")
        benchrows.append(dict(panel=panel, series="SPY", **sb))
        benchrows.append(dict(panel=panel, series="RULESv2@10bps", **lb10))

        if panel == "U56":
            W20, _ = build(rank_key, elig, priced, reb, 20, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            g20, t20 = nrun(rets, lagmat(W20), mkl)
            for cg, nm in ((0.0, "G1"), (10.0, "G1b"), (25.0, "G1c")):
                eng = backtest(px, wdf, cost_bps=cg, freq=FREQ)["returns"].values
                d = float(np.abs((g20 - t20 * cg / 1e4)[WARMUP:] - eng[WARMUP:]).max())
                gates[f"{nm} r(c)=g-tn*c/1e4 == engine.backtest at {cg:.0f} bps (U56 N=20 H=126)"] = (d, d < 1e-12)
            m = fmet((g20 - t20 * PROTOCOL_RUNG / 1e4)[warm])
            d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082/1094 committed U56 W/H126 N=20 triple @10 bps"] = (d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d4 = abs(lb10["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G4 live RULES v2 MaxDD @10 bps == committed -12.05%"] = (d4, d4 < 5e-4)

        # ---------------------------------------------------------------- the 54-cell ladder
        for N in NS:
            for H in HS:
                W, nsel = build(rank_key, elig, priced, reb, N, H, T, K, GROSS0)
                g, tn = nrun(rets, lagmat(W), mkl)
                turn = ann_turn(tn, warm)
                M = {L: np.empty(len(CFINE)) for L in ALL_LEGS}
                isleg = np.empty((len(CFINE), 3))
                for j, c in enumerate(CFINE):
                    b = blocks(g - tn * c / 1e4, warm, ins, oos)
                    mm = margins(b, sb)
                    for L in ALL_LEGS:
                        M[L][j] = mm[L]
                    isleg[j] = [b["IS_Sharpe"] - sb["IS_Sharpe"],
                                DD_CAP * abs(sb["IS_MaxDD"]) - abs(b["IS_MaxDD"]),
                                b["IS_CAGR"] - CAGR_FLOOR * sb["IS_CAGR"]]
                b50 = blocks(g - tn * 50.0 / 1e4, warm, ins, oos)
                b0 = blocks(g, warm, ins, oos)
                b10 = blocks(g - tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)
                lb = blocks(live_g - live_tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)
                l4a = legs_4a(b10, lb)
                row = dict(panel=panel, N=N, H=H, cap=CAPNAME, mean_nsel=float(nsel.mean()),
                           turnover=turn, CAGR0=b0["CAGR"], Sharpe0=b0["Sharpe"], MaxDD0=b0["MaxDD"],
                           CAGR10=b10["CAGR"], Sharpe10=b10["Sharpe"], MaxDD10=b10["MaxDD"],
                           OOS_CAGR10=b10["OOS_CAGR"], OOS_Sharpe10=b10["OOS_Sharpe"],
                           OOS_MaxDD10=b10["OOS_MaxDD"], IS_Sharpe10=b10["IS_Sharpe"],
                           IS_CAGR10=b10["IS_CAGR"], IS_MaxDD10=b10["IS_MaxDD"],
                           H1_10=b10["H1"], H2_10=b10["H2"], **l4a,
                           pass4a=all(l4a.values()),
                           d50_CAGR_pp=100.0 * (b0["CAGR"] - b50["CAGR"]),
                           d50_DD_pp=100.0 * (abs(b50["MaxDD"]) - abs(b0["MaxDD"])))
                # per-leg truths and the raw ingredients of every closed form
                for L in ALL_LEGS:
                    cs, contig, dead = cstar_from_margin(M[L])
                    w = WIN[L]
                    tnL = ann_turn(tn, w)
                    rr = (g - tn * 0.0 / 1e4)[w]
                    sig = fvol(rr)
                    dt = dd_years(rr)
                    # slope of the margin over the ladder, and over 0->10 bps only (H_LINEAR)
                    slope_full = float((M[L][0] - M[L][-1]) / (CFINE[-1] - CFINE[0]))
                    slope_10 = float((M[L][0] - M[L][10]) / 10.0)
                    row[f"cstar_{L}"] = cs
                    row[f"contig_{L}"] = contig
                    row[f"dead0_{L}"] = dead
                    row[f"m0_{L}"] = float(M[L][0])
                    row[f"tn_{L}"] = tnL
                    row[f"sig_{L}"] = sig
                    row[f"dt_{L}"] = dt
                    row[f"slope_{L}"] = slope_full
                    row[f"slope10_{L}"] = slope_10
                    for c in RUNGS:
                        row[f"true_{L}_{int(c)}"] = bool(M[L][int(c)] >= 0.0)
                    ladderrows.append(dict(panel=panel, N=N, H=H, leg=L, cstar_true=cs,
                                           contiguous=contig, dead_at_0=dead, m0=float(M[L][0]),
                                           turnover_leg=tnL, vol_leg=sig, dd_years=dt,
                                           slope_per_bp_full=slope_full, slope_per_bp_0to10=slope_10,
                                           m_at_10=float(M[L][10]), m_at_25=float(M[L][25]),
                                           m_at_50=float(M[L][50])))
                # conjunction c* (1094's object) for the full and OOS readings
                for nm, LS in (("full", FULL_LEGS), ("oos", OOS_LEGS)):
                    allm = np.min(np.vstack([M[L] for L in LS]), axis=0)
                    cs, contig, dead = cstar_from_margin(allm)
                    row[f"cstar_{nm}"] = cs
                    row[f"contig_{nm}"] = contig
                    j = int(np.clip((cs + 1) if cs == cs else 0, 0, len(CFINE) - 1))
                    row[f"binding_{nm}"] = ",".join(L for L in LS if M[L][j] < 0.0) or "none<=200bps"
                isc = np.min(isleg, axis=1)
                cs_is, _, _ = cstar_from_margin(isc)
                row["cstar_IS"] = cs_is
                # IS-ONLY ingredients for the honest closed-form chooser (no OOS number enters)
                tn_is = ann_turn(tn, ins)
                r_is = g[ins]
                sig_is, dt_is = fvol(r_is), dd_years(r_is)
                m_S, m_DD, m_C = float(isleg[0][0]), float(isleg[0][1]), float(isleg[0][2])
                pS = 1e4 * m_S * sig_is / tn_is
                pDD = 1e4 * m_DD / (tn_is * dt_is)
                pC = 1e4 * m_C / tn_is
                row["IS_tn"] = tn_is
                row["IS_vol"] = sig_is
                row["IS_ddyears"] = dt_is
                row["pred_IS_S"], row["pred_IS_DD"], row["pred_IS_CAGR"] = pS, pDD, pC
                row["cstar_IS_pred"] = float(min(pS, pDD, pC))
                cellrows.append(row)
                P(f"   N={N:2d} H={H:3d} turn {turn:5.2f}x/yr  c*_full "
                  f"{row['cstar_full'] if row['cstar_full'] == row['cstar_full'] else float('nan'):6.1f}"
                  f"  c*_oos {row['cstar_oos'] if row['cstar_oos'] == row['cstar_oos'] else float('nan'):6.1f}"
                  f"  binding {row['binding_full']:<10s}  ({time.time()-t0:.0f}s)")

    cells = pd.DataFrame(cellrows)
    lad = pd.DataFrame(ladderrows)

    # ------------------------------------------------------------------ remaining gates
    if C1094.exists():
        c94 = pd.read_csv(C1094)
        j = cells.merge(c94, on=["panel", "N", "H"], suffixes=("", "_94"))
        dt = float(np.abs(j.turnover - j.turnover_94).max())
        gates["G5a reproduces 1094's 54 committed turnover values"] = (dt, dt < 1e-9)
        for nm, col in (("full", "cstar_full_bps"), ("oos", "cstar_oos_bps")):
            a, b = j[f"cstar_{nm}"].values, j[col].values
            bad = int((~((np.isnan(a) & np.isnan(b)) | (a == b))).sum())
            gates[f"G5{'b' if nm == 'full' else 'c'} reproduces 1094's 54 committed c*_{nm} "
                  f"values EXACTLY"] = (float(bad), bad == 0)
            gates[f"G5{'b' if nm == 'full' else 'c'}2 and its finite count"] = (
                float(np.isfinite(b).sum()), int(np.isfinite(a).sum()) == int(np.isfinite(b).sum()))
    else:
        gates["G5 1094's committed breakeven.csv present"] = (0.0, False)
    bad = 0
    for _, r in cells.iterrows():
        mn = np.nanmin([r[f"cstar_{L}"] for L in FULL_LEGS]) if not any(
            r[f"dead0_{L}"] for L in FULL_LEGS) else np.nan
        cj = r["cstar_full"]
        if (cj != cj) and (mn != mn):
            continue
        if not (cj == mn):
            bad += 1
    gates["G7 conjunction c* == min over per-leg c* at every cell (H_MIN)"] = (float(bad), bad == 0)
    ncontig = int((~lad.contiguous).sum())
    gates["G8 every per-leg pass set is an INTERVAL from 0 bps"] = (float(ncontig), ncontig == 0)
    spread = float(lad[lad.cstar_true.notna()].cstar_true.max() - lad[lad.cstar_true.notna()].cstar_true.min())
    gates["G9 the c* axis is LIVE (spread of finite per-leg c* >= 10 bps)"] = (spread, spread >= 10.0)
    if D1094.exists():
        d94 = pd.read_csv(D1094)
        d94 = d94[d94.diag == "D1_leg_rates"]
        worst = 0.0
        for _, r in d94.iterrows():
            s_ = cells[(cells.panel == r.panel) & (cells.H == int(float(r.H)))]
            worst = max(worst, abs(float(s_.d50_CAGR_pp.mean()) - float(r.a)),
                        abs(float(s_.d50_DD_pp.mean()) - float(r.b)))
        gates["G6 reproduces 1094's six committed D1 slice means (0->50 bps)"] = (worst, worst < 1e-9)
    else:
        gates["G6 1094's committed diagnostics.csv present"] = (0.0, False)

    P("")
    P("## GATES (printed before any result number)")
    for k, (v, ok) in gates.items():
        P(f"   [{'PASS' if ok else 'FAIL'}] {k}: {v:.6g}")
    npass = sum(1 for _, (_, ok) in gates.items() if ok)
    P(f"   GATES {npass} of {len(gates)} PASS")
    dump(pd.DataFrame([dict(gate=k, value=v, passed=ok) for k, (v, ok) in gates.items()]), "gates")

    # ------------------------------------------------------------------ D1: the fit population
    P("")
    P("## D1 — HOW MANY CELLS EVEN HAVE A BREAKEVEN (the population any fit can use)")
    for nm in ("full", "oos"):
        f = cells[f"cstar_{nm}"]
        P(f"   conjunction c*_{nm}: FINITE at {int(f.notna().sum())} of {len(cells)} cells "
          f"(U56 {int(cells[cells.panel=='U56'][f'cstar_{nm}'].notna().sum())}/27, "
          f"B136 {int(cells[cells.panel=='B136'][f'cstar_{nm}'].notna().sum())}/27); "
          f"the other {int(f.isna().sum())} FAIL 4b at 0 bps and have NO breakeven at all")
    for L in ALL_LEGS:
        s = lad[lad.leg == L]
        P(f"   leg {L:7s}: passes at 0 bps at {int(s.cstar_true.notna().sum()):2d} of 54 cells; "
          f"finite c* median {s.cstar_true.median():6.1f} bps, max {s.cstar_true.max():6.1f}, "
          f"censored at 200 bps: {int((s.cstar_true >= CFINE[-1]).sum())}")
        diagrows.append(dict(diag="D1_population", leg=L, n_alive=int(s.cstar_true.notna().sum()),
                             median_cstar=float(s.cstar_true.median()),
                             n_censored=int((s.cstar_true >= CFINE[-1]).sum())))

    # ------------------------------------------------------------------ the four forms
    def predict(form, leg, m0, tn, sig, dt, kmap):
        if not np.isfinite(tn) or tn <= 0:
            return np.nan
        raw = 1e4 * m0 / tn
        if form == "F_RAW":
            return raw
        if form == "F_UNIT":
            if leg in ("L_H1", "L_H2", "L_OOS", "O_S"):
                return 1e4 * m0 * sig / tn
            if leg in ("L_DD", "O_DD"):
                return 1e4 * m0 / (tn * dt)
            return raw
        return kmap.get(leg if form == "F_KLEG" else "_ALL", np.nan) * raw

    # k fitted on the FIT PANEL only, over points with a finite c* and a positive RAW prediction
    fit = lad[(lad.panel == FITPANEL) & lad.cstar_true.notna() & (lad.cstar_true < CFINE[-1])].copy()
    fit["raw"] = 1e4 * fit.m0 / fit.turnover_leg
    fit = fit[fit.raw > 0]
    kmap = {"_ALL": float(np.median(fit.cstar_true / fit.raw)) if len(fit) else np.nan}
    for L in ALL_LEGS:
        s = fit[fit.leg == L]
        kmap[L] = float(np.median(s.cstar_true / s.raw)) if len(s) else kmap["_ALL"]
    P("")
    P(f"## THE FITTED CONSTANTS (median c*_true / c*_RAW on {FITPANEL} ONLY, "
      f"{len(fit)} points; B136 never enters)")
    P(f"   F_K1  k = {kmap['_ALL']:.6g}")
    for L in ALL_LEGS:
        s = fit[fit.leg == L]
        P(f"   F_KLEG k[{L:7s}] = {kmap[L]:12.6g}   (fitted on {len(s):2d} {FITPANEL} points)")

    lad["cstar_true_cens"] = lad.cstar_true
    for form in FORMS:
        lad[f"pred_{form}"] = [predict(form, r.leg, r.m0, r.turnover_leg, r.vol_leg, r.dd_years, kmap)
                               for r in lad.itertuples()]
    lad["pred_SLOPE10"] = [(r.m0 / r.slope_per_bp_0to10) if r.slope_per_bp_0to10 > 0 else np.nan
                           for r in lad.itertuples()]
    dump(lad, "ladder")

    # ------------------------------------------------------------------ scoring, per (leg, form)
    P("")
    P("## THE 32 PUBLISHED (LEG, FORM) POINTS — error against the TRUE ladder, in bps")
    P("   ERR set = points with a finite, uncensored true c*.  VERDICT set = all 54 cells "
      "(a negative prediction correctly says 'fails at 0 bps').")
    P(f"   {'leg':8s} {'form':8s} {'nfit':>4s} {'medErr':>9s} {'medAbs':>9s} {'p90Abs':>9s} "
      f"{'rho':>6s} {'<=5bp':>6s} {'<=10bp':>7s} {'flips@10/25/50':>16s} {'HOLDOUT flips':>14s}")
    scorerows = []
    for L in ALL_LEGS:
        for form in FORMS:
            s = lad[(lad.leg == L)].copy()
            e = s[s.cstar_true.notna() & (s.cstar_true < CFINE[-1]) & s[f"pred_{form}"].notna()]
            err = (e[f"pred_{form}"] - e.cstar_true).values
            rho = spearman(e[f"pred_{form}"].values, e.cstar_true.values)
            flips, hflips = {}, {}
            for c in RUNGS:
                tp = (s.cstar_true.notna()) & (s.cstar_true >= c)
                pp = s[f"pred_{form}"] >= c
                flips[c] = int((tp.values != pp.values).sum())
                ho = s.panel != FITPANEL
                hflips[c] = int((tp.values[ho.values] != pp.values[ho.values]).sum())
            r = dict(leg=L, form=form, n_err=len(e),
                     med_err=float(np.median(err)) if len(err) else np.nan,
                     med_abs=float(np.median(np.abs(err))) if len(err) else np.nan,
                     p90_abs=float(np.percentile(np.abs(err), 90)) if len(err) else np.nan,
                     spearman=rho,
                     share_5bp=float(np.mean(np.abs(err) <= 5.0)) if len(err) else np.nan,
                     share_10bp=float(np.mean(np.abs(err) <= 10.0)) if len(err) else np.nan,
                     flips_10=flips[10.0], flips_25=flips[25.0], flips_50=flips[50.0],
                     flips_total=sum(flips.values()),
                     holdout_flips_10=hflips[10.0], holdout_flips_25=hflips[25.0],
                     holdout_flips_50=hflips[50.0], holdout_flips_total=sum(hflips.values()))
            scorerows.append(r)
            P(f"   {L:8s} {form:8s} {r['n_err']:4d} {r['med_err']:9.2f} {r['med_abs']:9.2f} "
              f"{r['p90_abs']:9.2f} {r['spearman'] if r['spearman']==r['spearman'] else float('nan'):6.2f} "
              f"{r['share_5bp']:6.2f} {r['share_10bp']:7.2f} "
              f"{flips[10.0]:4d}/{flips[25.0]:3d}/{flips[50.0]:3d}{'':4s} "
              f"{sum(hflips.values()):14d}")
    sc = pd.DataFrame(scorerows)
    dump(sc, "scores")

    # ------------------------------------------------------------------ conjunction level
    P("")
    P("## THE CONJUNCTION — does a closed form REPLACE 1094's ladder?")
    conj = []
    for form in FORMS:
        pr = lad.pivot_table(index=["panel", "N", "H"], columns="leg", values=f"pred_{form}")
        tr = cells.set_index(["panel", "N", "H"])
        for nm, LS in (("full", FULL_LEGS), ("oos", OOS_LEGS)):
            pmin = pr[LS].min(axis=1)
            true = tr[f"cstar_{nm}"]
            ix = pmin.index
            t = true.reindex(ix)
            both = t.notna() & (t < CFINE[-1]) & pmin.notna()
            err = (pmin[both] - t[both]).values
            # binding leg agreement, on cells where the conjunction is alive
            agree = 0
            live = 0
            for key in ix[both.values]:
                truebind = set(str(tr.loc[key, f"binding_{nm}"]).split(","))
                predbind = {pr.loc[key, LS].idxmin()}
                live += 1
                agree += int(bool(truebind & predbind))
            fl = {}
            for c in RUNGS:
                tp = (t.notna()) & (t >= c)
                pp = pmin >= c
                fl[c] = int((tp.values != pp.values).sum())
            row = dict(form=form, reading=nm, n=int(both.sum()),
                       med_err=float(np.median(err)) if len(err) else np.nan,
                       med_abs=float(np.median(np.abs(err))) if len(err) else np.nan,
                       max_abs=float(np.max(np.abs(err))) if len(err) else np.nan,
                       binding_agree=(agree / live if live else np.nan), n_live=live,
                       flips_10=fl[10.0], flips_25=fl[25.0], flips_50=fl[50.0],
                       flips_total=sum(fl.values()))
            conj.append(row)
            P(f"   {form:8s} {nm:5s}  n={row['n']:2d}  medErr {row['med_err']:8.2f}  medAbs "
              f"{row['med_abs']:8.2f}  maxAbs {row['max_abs']:9.2f}  binding-leg agreement "
              f"{row['binding_agree']:.2f} ({agree}/{live})  verdict flips 10/25/50 "
              f"{fl[10.0]:2d}/{fl[25.0]:2d}/{fl[50.0]:2d} of 54")
    cj = pd.DataFrame(conj)
    dump(cj, "conjunction")

    # ------------------------------------------------------------------ D2 linearity, D3 slopes
    P("")
    P("## D2 — IS EACH LEG LINEAR IN THE COST RUNG? (H_LINEAR)")
    for L in ALL_LEGS:
        s = lad[(lad.leg == L) & lad.cstar_true.notna() & (lad.cstar_true < CFINE[-1])]
        if not len(s):
            P(f"   {L:7s}: no uncensored point")
            continue
        e = (s.pred_SLOPE10 - s.cstar_true).abs()
        curv = (s.slope_per_bp_0to10 / s.slope_per_bp_full).replace([np.inf, -np.inf], np.nan)
        P(f"   {L:7s}: |c*(0->10bps slope) - c*_true| median {e.median():7.2f} bps, max "
          f"{e.max():8.2f};  slope ratio (0-10 / 0-200) median {curv.median():6.3f}  n={len(s)}")
        diagrows.append(dict(diag="D2_linearity", leg=L, median_abs_err_bps=float(e.median()),
                             max_abs_err_bps=float(e.max()), median_slope_ratio=float(curv.median()),
                             n=len(s)))

    P("")
    P("## D3 — THE IMPLIED PER-BP SLOPES, AVERAGED OVER THE WHOLE 0-200 bps LADDER")
    P("   (1094's D1 ratio is taken over 0-50 bps; D3b below reproduces it on its own span.  The")
    P("   two spans disagree ONLY because the DD leg is the non-linear one — see D2.)")
    P("   NOTE: L_OOS and O_S are the SAME statistic (OOS Sharpe vs SPY's) under two names in")
    P("   the record's leg vocabulary, so their rows are identical by construction.")
    for L in ALL_LEGS:
        s = lad[lad.leg == L]
        P(f"   {L:7s}: margin lost per bp of cost — median {s.slope_per_bp_full.median():.6g}, "
          f"range [{s.slope_per_bp_full.min():.6g}, {s.slope_per_bp_full.max():.6g}] "
          f"(units of the leg)")
        diagrows.append(dict(diag="D3_slope", leg=L, median_slope_per_bp=float(s.slope_per_bp_full.median()),
                             min_slope=float(s.slope_per_bp_full.min()),
                             max_slope=float(s.slope_per_bp_full.max())))
    for panel in PANELS:
        a = lad[(lad.panel == panel) & (lad.leg == "L_CAGR")].set_index(["N", "H"]).slope_per_bp_full
        b = lad[(lad.panel == panel) & (lad.leg == "L_DD")].set_index(["N", "H"]).slope_per_bp_full
        rr = (a / b).replace([np.inf, -np.inf], np.nan).dropna()
        P(f"   {panel}: CAGR slope / DD slope per bp over 0-200 — median {rr.median():.2f}x, "
          f"range [{rr.min():.2f}, {rr.max():.2f}]")
        diagrows.append(dict(diag="D3_cagr_over_dd", leg=panel, median_slope_per_bp=float(rr.median()),
                             min_slope=float(rr.min()), max_slope=float(rr.max())))

    P("")
    P("## D3b — 1094's '8-42x' IS A RATIO OF SLICE MEANS, RE-READ PER CELL")
    for panel in PANELS:
        for H in HS:
            s_ = cells[(cells.panel == panel) & (cells.H == H)]
            rom = float(s_.d50_CAGR_pp.mean() / s_.d50_DD_pp.mean())
            per = (s_.d50_CAGR_pp / s_.d50_DD_pp).replace([np.inf, -np.inf], np.nan).dropna()
            P(f"   {panel:4s} H={H:3d}: ratio of MEANS {rom:6.2f}x (1094's figure)   per-cell median "
              f"{per.median():6.2f}x, range [{per.min():.2f}, {per.max():.2f}], "
              f"{int((per < 1).sum())} of {len(per)} cells BELOW 1x")
            diagrows.append(dict(diag="D3b_ratio", leg=f"{panel}_H{H}", ratio_of_means=rom,
                                 median_per_cell=float(per.median()), min_per_cell=float(per.min()),
                                 max_per_cell=float(per.max()), n_below_1x=int((per < 1).sum()), n=len(per)))
    allper = (cells.d50_CAGR_pp / cells.d50_DD_pp).replace([np.inf, -np.inf], np.nan).dropna()
    P(f"   ALL 54 cells: per-cell ratio median {allper.median():.2f}x, range "
      f"[{allper.min():.2f}, {allper.max():.2f}], {int((allper < 1).sum())} BELOW 1x "
      f"(i.e. cost moves |MaxDD| MORE than CAGR there)")

    P("")
    P("## POST-HOC (labelled, fitted on nothing) — WHAT THE FITTED CONSTANTS TURN OUT TO BE")
    fitc = cells[cells.panel == FITPANEL]
    for L in ("L_H1", "L_H2", "L_OOS", "O_S"):
        med_sig = float(lad[(lad.panel == FITPANEL) & (lad.leg == L)].vol_leg.median())
        P(f"   k[{L:6s}] = {kmap[L]:.4f}  vs the {FITPANEL} median book VOL over that leg's own "
          f"window = {med_sig:.4f}  (ratio {kmap[L]/med_sig:.3f})")
    med_c = float((1.0 + fitc.CAGR0).median())
    for L in ("L_CAGR", "O_CAGR"):
        P(f"   k[{L:6s}] = {kmap[L]:.4f}  vs 1/(1 + median book CAGR at 0 bps) = {1.0/med_c:.4f}  "
          f"(ratio {kmap[L]*med_c:.3f})   — compounding, not a free parameter")
    for L in ("L_DD", "O_DD"):
        med_dt = float(lad[(lad.panel == FITPANEL) & (lad.leg == L)].dd_years.median())
        P(f"   k[{L:6s}] = {kmap[L]:.4f}  vs 1/(median drawdown-episode length {med_dt:.3f} yr) = "
          f"{1.0/med_dt:.4f}  (ratio {kmap[L]*med_dt:.3f})   — the ONE leg the identity misses")

    # ------------------------------------------------------------------ D4: 1094's rho
    P("")
    P("## D4 — 1094's rho(c*, turnover) = -0.65, AND WHAT IT IS A STATEMENT ABOUT")
    rng = np.random.default_rng(10971097)
    for nm in ("full", "oos"):
        s = cells[cells[f"cstar_{nm}"].notna()]
        if len(s) > 2:
            r = spearman(s[f"cstar_{nm}"].values, s.turnover.values)
            bs = []
            for _ in range(2000):
                i = rng.integers(0, len(s), len(s))
                x, y = s[f"cstar_{nm}"].values[i], s.turnover.values[i]
                v = spearman(x, y)
                if v == v:
                    bs.append(v)
            lo, hi = (np.percentile(bs, [5, 95]) if bs else (np.nan, np.nan))
            P(f"   {nm:5s}: rho = {r:+.4f} over the {len(s)} cells WITH a finite c* "
              f"(of 54); 2,000-rep bootstrap 90% interval [{lo:+.3f}, {hi:+.3f}]")
            diagrows.append(dict(diag="D4_rho", leg=nm, n=len(s), rho=r, lo90=float(lo), hi90=float(hi)))
    dump(pd.DataFrame(diagrows), "diagnostics")

    # ------------------------------------------------------------------ hypotheses
    P("")
    P("## HYPOTHESES (each as declared before any number)")
    hyp = []

    def H(name, pred, verdict, evidence):
        hyp.append(dict(hypothesis=name, pre_registered=pred, verdict=verdict, evidence=evidence))
        P(f"   {name:10s} {verdict:9s} — {evidence}")

    raw = sc[sc.form == "F_RAW"]
    share10 = float(np.nansum(raw.share_10bp * raw.n_err) / max(raw.n_err.sum(), 1))
    # verdict always refers to the CLAIM; pre_registered records what was predicted for it
    H("H_RAW", "predicted REFUTED (units)", "REFUTED" if share10 < 0.5 else "SUPPORTED",
      f"margin/turnover alone lands within 10 bps at {share10:.1%} of the "
      f"{int(raw.n_err.sum())} scorable (cell, leg) points")
    unit = sc[sc.form == "F_UNIT"]
    nbad = int((unit.med_abs > 10.0).sum())
    H("H_UNIT", "PASS on CAGR/Sharpe", "SUPPORTED" if nbad == 0 else "REFUTED",
      f"F_UNIT median |err| exceeds 10 bps on {nbad} of {len(unit)} legs "
      f"(worst {unit.med_abs.max():.2f} bps on {unit.loc[unit.med_abs.idxmax(),'leg']})")
    d2 = pd.DataFrame([d for d in diagrows if d["diag"] == "D2_linearity"])
    H("H_LINEAR", "within 5 bps everywhere",
      "SUPPORTED" if float(d2.max_abs_err_bps.max()) <= 5.0 else "REFUTED",
      f"worst |c*(0-10 slope) - c*_true| over all legs = {float(d2.max_abs_err_bps.max()):.2f} bps; "
      f"median over legs {float(d2.median_abs_err_bps.median()):.2f}")
    best = sc.sort_values(["med_abs"]).groupby("form").med_abs.max().sort_values()
    winner = best.index[0]
    w = sc[sc.form == winner]
    hold = cj[(cj.form == winner)]
    ok = bool((w.med_abs <= 5.0).all()) and int(w.holdout_flips_total.sum()) == 0
    H("H_ONEFORM", "one form replaces the ladder", "SUPPORTED" if ok else "REFUTED",
      f"best form {winner}: worst per-leg median |err| {float(w.med_abs.max()):.2f} bps "
      f"(bar 5), hold-out verdict flips {int(w.holdout_flips_total.sum())} (bar 0); "
      f"conjunction max |err| {float(hold.max_abs.max()):.2f} bps")
    gmin = gates["G7 conjunction c* == min over per-leg c* at every cell (H_MIN)"]
    H("H_MIN", "exact everywhere", "SUPPORTED" if gmin[1] else "REFUTED",
      f"{int(gmin[0])} cells where the conjunction c* differs from min over per-leg c*")
    ba = float(cj[cj.form == winner].binding_agree.mean())
    H("H_BINDING", ">= 80% of cells", "SUPPORTED" if ba >= 0.80 else "REFUTED",
      f"{winner} names the true binding leg at {ba:.1%} of live cells")
    d4 = pd.DataFrame([d for d in diagrows if d["diag"] == "D4_rho"])
    f4 = d4[d4.leg == "full"].iloc[0]
    unres = bool(f4.lo90 * f4.hi90 <= 0) or (f4.hi90 - f4.lo90) > 0.5
    H("H_RHO", "reproduces but unresolved", "SUPPORTED" if unres else "REFUTED",
      f"rho {f4.rho:+.4f} on n={int(f4.n)} of 54 cells, 90% interval "
      f"[{f4.lo90:+.3f}, {f4.hi90:+.3f}], width {float(f4.hi90-f4.lo90):.3f}")
    hy = pd.DataFrame(hyp)
    dump(hy, "hypotheses")
    P(f"   HYPOTHESES {int((hy.verdict=='SUPPORTED').sum())} of {len(hy)} SUPPORTED")

    # ------------------------------------------------------------------ RULE 8 + both KEEP paths
    P("")
    P("## RULE 8 WALK-FORWARD — cell chosen on IS 2009-2016 ONLY, OOS 2017-2026 read ONCE")
    P("   Three declared choosers.  C_CSTARPRED is THIS run's closed form used as a chooser:")
    P("   the cell with the largest PREDICTED IS cost headroom.  Regret is against the OOS-best")
    P("   cell of the same panel.")
    P("   C_CSTARPRED uses F_UNIT (the PARAMETER-FREE form) applied to IS-WINDOW margins,")
    P("   IS-window turnover, IS-window vol and the IS-window drawdown episode ONLY.  No")
    P("   out-of-sample number and no fitted constant enters it.")
    okp = cells[cells.cstar_IS.notna() & (cells.cstar_IS < CFINE[-1])]
    if len(okp):
        e = (okp.cstar_IS_pred - okp.cstar_IS).abs()
        P(f"   IS-only form vs IS-only truth: median |err| {e.median():.2f} bps, max {e.max():.2f}, "
          f"within 10 bps at {float((e <= 10).mean()):.0%} of {len(okp)} cells with a finite IS c*")
        diagrows.append(dict(diag="D5_IS_form", leg="all", median_abs_err_bps=float(e.median()),
                             max_abs_err_bps=float(e.max()), n=len(okp)))
    for panel in PANELS:
        st = panel_store[panel]
        sb, lb10 = st["sb"], st["lb10"]
        gp = cells[cells.panel == panel].copy()
        gp["pred_headroom"] = gp.cstar_IS_pred
        oos_best = gp.OOS_Sharpe10.max()
        for cname, key in [("C_ISSHARPE", "IS_Sharpe10"), ("C_CSTARTRUE", "cstar_IS"),
                           ("C_CSTARPRED", "pred_headroom")]:
            g2 = gp[gp[key].notna()]
            if not len(g2):
                P(f"   {panel} {cname}: no cell has a finite {key} — NO PICK")
                picks.append(dict(panel=panel, chooser=cname, N=-1, H=-1, note=f"no finite {key}"))
                continue
            pk = g2.sort_values(key, ascending=False).iloc[0]
            o_s = bool(pk.OOS_Sharpe10 > sb["OOS_Sharpe"])
            o_dd = bool(abs(pk.OOS_MaxDD10) <= DD_CAP * abs(sb["OOS_MaxDD"]))
            o_c = bool(pk.OOS_CAGR10 >= CAGR_FLOOR * sb["OOS_CAGR"])
            p4b = bool(pk.H1_10 > sb["H1"] and pk.H2_10 > sb["H2"] and o_s
                       and abs(pk.MaxDD10) <= DD_CAP * abs(sb["MaxDD"])
                       and pk.CAGR10 >= CAGR_FLOOR * sb["CAGR"])
            picks.append(dict(panel=panel, chooser=cname, N=int(pk.N), H=int(pk.H),
                              key=key, key_value=float(pk[key]),
                              OOS_CAGR=float(pk.OOS_CAGR10), OOS_Sharpe=float(pk.OOS_Sharpe10),
                              OOS_MaxDD=float(pk.OOS_MaxDD10), full_CAGR=float(pk.CAGR10),
                              full_Sharpe=float(pk.Sharpe10), full_MaxDD=float(pk.MaxDD10),
                              spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                              spy_OOS_MaxDD=sb["OOS_MaxDD"], live_OOS_CAGR=lb10["OOS_CAGR"],
                              live_OOS_Sharpe=lb10["OOS_Sharpe"], live_OOS_MaxDD=lb10["OOS_MaxDD"],
                              O_S=o_s, O_DD=o_dd, O_CAGR=o_c, pass4b_oos=bool(o_s and o_dd and o_c),
                              pass4b_full=p4b, pass4a=bool(pk.pass4a),
                              regret_oos_sharpe=float(oos_best - pk.OOS_Sharpe10)))
            P(f"   {panel} {cname:12s} picks N={int(pk.N):2d} H={int(pk.H):3d}  OOS "
              f"{pk.OOS_CAGR10:7.2%} / {pk.OOS_Sharpe10:.4f} / {pk.OOS_MaxDD10:7.2%}   "
              f"4b OOS legs S/DD/CAGR {int(o_s)}/{int(o_dd)}/{int(o_c)} -> "
              f"{'PASS' if (o_s and o_dd and o_c) else 'FAIL'}   4b full "
              f"{'PASS' if p4b else 'FAIL'}   4a {'PASS' if pk.pass4a else 'FAIL'}   regret "
              f"{oos_best - pk.OOS_Sharpe10:+.4f}")
        P(f"   {panel} bars: SPY OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%};  RULES v2 @10 bps OOS {lb10['OOS_CAGR']:.2%} / "
          f"{lb10['OOS_Sharpe']:.4f} / {lb10['OOS_MaxDD']:.2%}")
    pk = pd.DataFrame(picks)
    dump(pk, "picks")

    n4b_full = int(cells.cstar_full.notna().sum())
    n4b_oos = int(cells.cstar_oos.notna().sum())
    n4a = int(cells.pass4a.sum())
    P("")
    P(f"## BOTH KEEP PATHS at PROTOCOL's 10 bps, over all {len(cells)} cells")
    P(f"   4b FULL  {int(((cells.cstar_full.notna()) & (cells.cstar_full >= PROTOCOL_RUNG)).sum())}"
      f" of {len(cells)}   (pass at 0 bps: {n4b_full})")
    P(f"   4b OOS   {int(((cells.cstar_oos.notna()) & (cells.cstar_oos >= PROTOCOL_RUNG)).sum())}"
      f" of {len(cells)}   (pass at 0 bps: {n4b_oos})")
    P(f"   4a       {n4a} of {len(cells)}")
    P("   NOTHING IS PROPOSED AS CAPITAL by this run: it measures a PREDICTOR of a published")
    P("   column, not a book.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.")

    dump(cells, "cells")
    dump(pd.DataFrame(benchrows), "benchmarks")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
