#!/usr/bin/env python3
"""Idea 2109 (lane cloud, 2026-09-22) — IS THE CHOOSER SPREAD A GENERAL PROPERTY OF THE
RECORD'S GRIDS, OR SPECIFIC TO THE TURNOVER-BUDGET FAMILY?

WHERE THIS COMES FROM.  Idea 2087 (2026-09-22, lane C) ran SEVEN legal IS-only choosers over ONE
family's grid (the turnover-budget (target t x budget B) grid) and measured a per-chooser 4b
FULL+OOS reach of IS_LEGS 0.785 / IS_MINMARG 0.708 / IS_SHARPE 0.680 / IS_CAGRSLACK 0.578 /
IS_CALMAR 0.458 / IS_DD 0.058 / CELL_ALPHA 0.005 — a 157x spread between the best and the worst
legal rule ON THE SAME GRID.  Every rule-8 verdict the record has ever published was reached with
ONE chooser and published without a spread beside it.  If 2087's spread is a property of GRIDS
rather than of that one family, then every committed 'N of M arms clear 4b under a legal IS-only
chooser' in this record carries an unreported selection width of the same order.

THE QUESTION.  Re-run the SAME seven choosers over SIX OTHER families' grids and publish
(a) the per-family per-chooser reach, (b) the per-family best/worst spread, (c) the share of
grid instances on which the seven legal rules DISAGREE about the 4b verdict, and (d) whether the
chooser RANKING travels between families at all.

WHAT IS PRICED.  Six families, each a fresh 2-D grid, all price-only, priced from scratch on the
committed caches (no prose is harvested):
    BAND    200d-MA band with hysteresis: band in {0.00,0.03,0.05,0.08,0.12} x gross
            {0.25,0.50,0.75,1.00}                                             = 20 cells
    MOM     composite-momentum shelf: width k in {5,10,20,40,ALL} x gross {...} = 20 cells
    MADIST  distance-to-200d-MA shelf: same axes                                = 20 cells
    VOLTGT  vol-target scaler on the band-0.03 book: target in
            {0.06,0.08,0.10,0.12,0.15} x vol lookback {20,60,120}               = 15 cells
    DRIFT   drift-threshold refresh of that scaler: target in {0.06,0.08,0.10,0.12}
            x drift threshold h in {0.02,0.04,0.08,0.16}                        = 16 cells
    STOP    per-name trailing stop: stop depth H in {0.10,0.15,0.20,0.30} x gross {...}
                                                                                = 16 cells
  = 107 cells per (panel x cadence).  Panels U56 / B136; cadences W / M; fills t+1; costs
  {0,10,25,50} bps derived EXACTLY from the cost-0 run and its own turnover series (gate G3).
  A GRID INSTANCE is one (family, panel, cadence, cost) = 96 instances, 107 cells each.

THE TWO TUNED DIALS (and no more).
  DIAL 1 — FAMILY SET: the six families above.
  DIAL 2 — CHOOSER SET: the seven legal IS-only rules of idea 2087, verbatim
           (IS_SHARPE, IS_LEGS, IS_CALMAR, IS_MINMARG, IS_CAGRSLACK, IS_DD, CELL_ALPHA).
REPORTED, NOT TUNED: panel, cadence, cost rung.  EVERY grid point is published
(`*.cells.csv`, 1,712 rows) and so is every pick (`*.picks.csv`, 672 rows).

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after).
  V1  GENERALITY.  The MEDIAN over the six families of the per-family best/worst reach ratio
      (Laplace-smoothed so a zero denominator stays finite) is >= 10.  Triggered -> the chooser
      spread is a property of the record's GRIDS, not of the turnover-budget family.
  V2  VERDICT WIDTH.  On MORE THAN 25% of the 96 instances the seven legal choosers do NOT
      agree on the 4b FULL+OOS verdict.  Triggered -> a single-chooser verdict in this record
      carries unreported selection width.
  V3  PORTABILITY.  Mean pairwise Spearman rho of the per-chooser reach vectors ACROSS families
      is >= +0.50.  Triggered -> a dominant chooser exists and the record could name one.
  V4  CAPITAL.  At least one chooser pick clears 4b FULL+OOS at the protocol 10 bps rung.

PROTOCOL: rule 2 (10 bps, t+1 fills, no shorting, no leverage — gate G1 caps gross at 1.00);
rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every pick, <= 2 tuned dials);
rule 5 (one idea, deterministic, standalone); rule 8 (dials chosen on 2009-2016, 2017-2026 read
ONCE); rule 9 (survivorship stated).  RULES.md / scan.py / bot.py / baseline.py NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists, so every CAGR and MaxDD
LEVEL below is optimistic and both 4b bars are easier than on a point-in-time panel.  The object
this run measures is a CONTRAST BETWEEN CHOOSERS on one and the same grid and tape, so it is
first-order immune to the bias; the 4b pass COUNTS are not.

Run:  python research/backtests/2026-09-22_chooser-spread-across-families_cloud.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state, score      # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask              # noqa: E402

DATE, SLUG = "2026-09-22", "chooser-spread-across-families"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

PANELS = ["U56", "B136"]
CADENCES = ["W", "M"]
COSTS = [0, 10, 25, 50]
PROTOCOL_COST = 10
CHOOSERS = ["IS_SHARPE", "IS_LEGS", "IS_CALMAR", "IS_MINMARG", "IS_CAGRSLACK", "IS_DD",
            "CELL_ALPHA"]
FAMILIES = ["BAND", "MOM", "MADIST", "VOLTGT", "DRIFT", "STOP"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
WIDTHS = [5, 10, 20, 40, "ALL"]
BANDS = [0.00, 0.03, 0.05, 0.08, 0.12]
VT_TARGETS = [0.06, 0.08, 0.10, 0.12, 0.15]
VT_LOOKBACKS = [20, 60, 120]
DR_TARGETS = [0.06, 0.08, 0.10, 0.12]
DR_H = [0.02, 0.04, 0.08, 0.16]
STOPS = [0.10, 0.15, 0.20, 0.30]

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
MAX_VOL = 0.60
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]

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


# --------------------------------------------------------------------------- metrics helpers
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


# --------------------------------------------------------------------------- panels / signals
def panel(name):
    px = (load_universe() if name == "U56" else load_universe(broad=True))
    return px.dropna(how="all").ffill()


def base_signals(px):
    """Everything the six families read, computed once per panel."""
    comp_ns, above, vol20 = score(px, vol_scale=False)
    gate_ = above & (vol20 < MAX_VOL) & px.notna()
    madist = px / px.rolling(200).mean() - 1.0
    stop_ref = px.rolling(252, min_periods=60).max()
    return dict(MOM=comp_ns, MADIST=madist, gate=gate_, px=px, stop_ref=stop_ref)


def eq_weights(elig, gross):
    n = elig.sum(axis=1).replace(0, np.nan)
    return elig.astype(float).div(n, axis=0).fillna(0.0) * gross


def topk_weights(sig, elig, k, gross):
    if k == "ALL":
        return eq_weights(elig, gross)
    # method="first" breaks ties by column order: EXACTLY k names, never k+ties, so a book's
    # target gross can never exceed `gross` (protocol rule 2, gate G1).
    rank = sig.where(elig).rank(axis=1, ascending=False, method="first")
    return (rank <= k).astype(float) * (gross / k)


def proxy_vol(px, elig, lookback):
    """Causal vol estimate of the equal-weight ELIGIBLE book, from prices alone: the
    cross-sectional mean daily return of yesterday's eligible names, trailing std, annualised,
    shifted one day so the value is known at the decision close."""
    r = px.pct_change()
    e = elig.shift(1).fillna(False)
    br = (r.where(e)).mean(axis=1).fillna(0.0)
    return (br.rolling(lookback, min_periods=max(10, lookback // 2)).std()
            * np.sqrt(252.0)).shift(1)


def drift_scaler(raw, idx, freq, h):
    """Refresh the exposure scalar only when it has drifted more than h from the held one."""
    mask = rebalance_mask(idx, freq)
    out = pd.Series(np.nan, index=idx)
    cur = np.nan
    rv = raw.values
    mv = mask.values
    for i in range(len(idx)):
        if mv[i]:
            x = rv[i]
            if np.isfinite(x) and (not np.isfinite(cur) or abs(x - cur) > h):
                cur = x
        out.iloc[i] = cur
    return out.ffill().fillna(0.0)


def family_cells(fam):
    if fam == "BAND":
        return [dict(a=b, b=g) for b in BANDS for g in GROSSES]
    if fam in ("MOM", "MADIST"):
        return [dict(a=k, b=g) for k in WIDTHS for g in GROSSES]
    if fam == "VOLTGT":
        return [dict(a=t, b=lb) for t in VT_TARGETS for lb in VT_LOOKBACKS]
    if fam == "DRIFT":
        return [dict(a=t, b=h) for t in DR_TARGETS for h in DR_H]
    if fam == "STOP":
        return [dict(a=H, b=g) for H in STOPS for g in GROSSES]
    raise ValueError(fam)


def build_weights(fam, cell, S, freq):
    """One cell's DAILY target-weight frame.  The engine samples it on the cadence mask and
    fills at t+1, so no value here may use a close after its own date."""
    px, g = S["px"], S["gate"]
    a, b = cell["a"], cell["b"]
    if fam == "BAND":
        return eq_weights(band_state(px, a) & px.notna(), b)
    if fam in ("MOM", "MADIST"):
        return topk_weights(S[fam], g & S[fam].notna(), a, b)
    if fam in ("VOLTGT", "DRIFT"):
        elig = band_state(px, 0.03) & px.notna()
        base = eq_weights(elig, 1.00)
        if fam == "VOLTGT":
            v = proxy_vol(px, elig, b)
            s = (a / v).clip(upper=1.0).fillna(0.0)
        else:
            v = proxy_vol(px, elig, 60)
            s = drift_scaler((a / v).clip(upper=1.0), px.index, freq, b)
        return base.mul(s, axis=0).fillna(0.0)
    if fam == "STOP":
        elig = (px >= (1.0 - a) * S["stop_ref"]) & px.notna()
        return eq_weights(elig, b)
    raise ValueError(fam)


# --------------------------------------------------------------------------- scoring / choosers
def score_cell(r0, t0, st, S, LV):
    """Every 4b / 4a leg at every cost rung for one cell.  Same leg algebra as ideas 2087/2083."""
    r0, t0 = r0.loc[st:], t0.loc[st:]
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
        is_legs = (int(ih1 > S["ish1"]) + int(ih2 > S["ish2"])
                   + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
                   + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"]))
        is_minmarg = min(ih1 - S["ish1"], ih2 - S["ish2"],
                         mi["MaxDD"] - DD_CAP * S["is_"]["MaxDD"],
                         mi["CAGR"] - CAGR_FLOOR * S["is_"]["CAGR"])
        out.append(dict(
            cost=c, CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
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
    """A LEGAL IS-ONLY chooser: reads 2009-2016 columns only.  Deterministic tie-break on the
    cell label ascending, so no rule can win on ordering luck."""
    s = sub.sort_values("cell").reset_index(drop=True)
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
        key = s.is_MaxDD.values
    elif chooser == "CELL_ALPHA":                     # no-information control
        return s.iloc[0]
    else:
        raise ValueError(chooser)
    return s.iloc[int(np.argmax(np.nan_to_num(key, nan=-1e18)))]


def spearman(a, b):
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    if np.std(ra) == 0 or np.std(rb) == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# --------------------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2109 (lane cloud, {DATE}) — is the CHOOSER SPREAD a GENERAL property of the "
        f"record's GRIDS or specific to the TURNOVER-BUDGET family?")
    log(f"# TUNED DIALS (2): FAMILY SET {FAMILIES}; CHOOSER SET {CHOOSERS}.")
    log(f"# reported, not tuned: PANEL {PANELS} x CADENCE {CADENCES} x COST {COSTS} bps.  "
        f"107 cells per (panel x cadence); fills t+1; IS {'<='+IS_END}, OOS {OOS_START}+ read "
        f"ONCE.")
    log(f"# COMPARAND (committed, idea 2087, NOT recomputed here): per-chooser 4b FULL+OOS reach "
        f"IS_LEGS 0.785 / IS_MINMARG 0.708 / IS_SHARPE 0.680 / IS_CAGRSLACK 0.578 / IS_CALMAR "
        f"0.458 / IS_DD 0.058 / CELL_ALPHA 0.005 -> spread 157x.")

    cells, g_gross, g_cost_err = [], 0.0, 0.0
    for pname in PANELS:
        px = panel(pname)
        st = px.index[WARMUP]
        S0 = base_signals(px)
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        h1s, h2s = halves(spy)
        ih1s, ih2s = halves(spy.loc[:IS_END])
        SPY = dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                   h1=h1s, h2=h2s, ish1=ih1s, ish2=ih2s)
        log(f"\n## {pname}: {px.shape[1]} cols, {len(px)} rows ({len(px)/252:.1f}y), book from "
            f"{st.date()}")
        log(f"   SPY FULL {SPY['full']['CAGR']:.2%}/{SPY['full']['Sharpe']:.3f}/"
            f"{SPY['full']['MaxDD']:.2%} (H1 {h1s:.3f} H2 {h2s:.3f});  SPY OOS "
            f"{SPY['oos']['CAGR']:.2%}/{SPY['oos']['Sharpe']:.3f}/{SPY['oos']['MaxDD']:.2%}"
            f"  ->  4b OOS bars: DD {DD_CAP*SPY['oos']['MaxDD']:.2%}, CAGR "
            f"{CAGR_FLOOR*SPY['oos']['CAGR']:.2%}")

        lb = engine_backtest(px, rules_v2_weights(px, 0.03, 0.75), cost_bps=0.0, freq="W")
        lr0, lt0 = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        LV = {}
        for c in COSTS:
            r = net(lr0, lt0, c)
            a1, a2 = halves(r)
            LV[c] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]), h1=a1, h2=a2)
        log(f"   RULES v2 live @10bps FULL {LV[10]['full']['CAGR']:.2%}/"
            f"{LV[10]['full']['Sharpe']:.3f}/{LV[10]['full']['MaxDD']:.2%};  OOS "
            f"{LV[10]['oos']['CAGR']:.2%}/{LV[10]['oos']['Sharpe']:.3f}/"
            f"{LV[10]['oos']['MaxDD']:.2%}")

        for freq in CADENCES:
            for fam in FAMILIES:
                for cell in family_cells(fam):
                    W = build_weights(fam, cell, S0, freq).reindex(columns=px.columns).fillna(0.0)
                    res = engine_backtest(px, W, cost_bps=0.0, freq=freq)
                    g_gross = max(g_gross, float(res["weights"].sum(axis=1).max()))
                    label = f"{cell['a']}|{cell['b']}"
                    for row in score_cell(res["returns"], res["turnover"], st, SPY, LV):
                        cells.append(dict(panel=pname, cadence=freq, family=fam, cell=label,
                                          a=str(cell["a"]), b=str(cell["b"]), **row))
                log(f"   {pname} {freq} {fam}: {len(family_cells(fam))} cells priced")

        # G3 — the derived cost rungs must equal a direct engine run at that cost_bps
        Wc = build_weights("BAND", dict(a=0.03, b=0.75), S0, "W").reindex(
            columns=px.columns).fillna(0.0)
        d0 = engine_backtest(px, Wc, cost_bps=0.0, freq="W")
        d10 = engine_backtest(px, Wc, cost_bps=10.0, freq="W")
        g_cost_err = max(g_cost_err, float(np.abs(
            net(d0["returns"], d0["turnover"], 10).values - d10["returns"].values).max()))

    C = pd.DataFrame(cells)
    C.to_csv(f"{OUT}.cells.csv", index=False)
    log(f"\n{len(C)} grid rows written to {Path(OUT).name}.cells.csv "
        f"({C.cell.nunique()} distinct cell labels, {len(FAMILIES)} families)")

    gate("G1 no leverage (max gross over every cell)", f"{g_gross:.4f}", "<= 1.0001",
         g_gross <= 1.0001)
    gate("G3 derived cost rung == direct engine cost_bps (max |diff|)", f"{g_cost_err:.3e}",
         "< 1e-12", g_cost_err < 1e-12)
    gate("G2 IS/OOS windows disjoint and exhaustive", f"{IS_END} | {OOS_START}", "no overlap",
         pd.Timestamp(IS_END) < pd.Timestamp(OOS_START))

    # ---------------------------------------------------------------- rule 8: choose IS, read OOS
    log("\n## RULE 8 — dials picked on 2009-2016 rows ONLY; 2017-2026 read ONCE.  "
        "96 instances x 7 choosers = 672 picks, all published.")
    picks = []
    for (pname, freq, fam, c), sub in C.groupby(["panel", "cadence", "family", "cost"]):
        for ch in CHOOSERS:
            p = pick(sub, ch)
            picks.append(dict(panel=pname, cadence=freq, family=fam, cost=c, chooser=ch,
                              cell=p.cell, oos_CAGR=p.oos_CAGR, oos_Sharpe=p.oos_Sharpe,
                              oos_MaxDD=p.oos_MaxDD, CAGR=p.CAGR, Sharpe=p.Sharpe,
                              MaxDD=p.MaxDD, H1=p.H1, H2=p.H2, bind=p.bind,
                              keep4b_full=bool(p.keep4b_full), keep4b_oos=bool(p.keep4b_oos),
                              keep4b=bool(p.keep4b), keep4a=bool(p.keep4a),
                              keep4a_oos=bool(p.keep4a_oos)))
    P = pd.DataFrame(picks)
    P.to_csv(f"{OUT}.picks.csv", index=False)

    # V1 — per-family per-chooser reach and spread
    log("\n### per-family per-chooser 4b FULL+OOS reach (share of that family's 16 instances)")
    reach = P.pivot_table(index="family", columns="chooser", values="keep4b", aggfunc="mean")
    reach = reach[CHOOSERS]
    log(reach.to_string(float_format=lambda x: f"{x:.3f}"))
    n_inst = P.groupby("family").size() / len(CHOOSERS)
    ratios = {}
    for fam in FAMILIES:
        k = P[P.family == fam].groupby("chooser").keep4b.sum().reindex(CHOOSERS)
        n = int(n_inst[fam])
        sm = (k + 0.5) / (n + 1.0)                       # Laplace so a 0 denominator stays finite
        ratios[fam] = float(sm.max() / sm.min())
        log(f"   {fam:7s} n={n:2d}  best {k.idxmax()} {int(k.max())}/{n}  worst {k.idxmin()} "
            f"{int(k.min())}/{n}   smoothed best/worst ratio {ratios[fam]:.2f}")
    med_ratio = float(np.median(list(ratios.values())))
    v1 = gate("V1 GENERALITY: median per-family smoothed best/worst reach ratio",
              f"{med_ratio:.2f}", ">= 10", med_ratio >= 10)

    # V2 — verdict width
    agree = P.groupby(["panel", "cadence", "family", "cost"]).keep4b.nunique()
    split = float((agree > 1).mean())
    log(f"\n### verdict width: {int((agree>1).sum())} of {len(agree)} instances have the seven "
        f"legal choosers DISAGREEING on the 4b FULL+OOS verdict ({split:.1%})")
    sp = P.groupby(["panel", "cadence", "family", "cost"]).oos_Sharpe.agg(["min", "max"])
    sp["spread"] = sp["max"] - sp["min"]
    log(f"    OOS Sharpe spread across the seven picks, per instance: median "
        f"{sp.spread.median():.4f}, mean {sp.spread.mean():.4f}, max {sp.spread.max():.4f}")
    log("    per family (median OOS-Sharpe spread across choosers):")
    fs = P.groupby(["family", "panel", "cadence", "cost"]).oos_Sharpe.agg(["min", "max"])
    fs["spread"] = fs["max"] - fs["min"]
    for fam in FAMILIES:
        log(f"      {fam:7s} {fs.loc[fam].spread.median():.4f}  "
            f"(max {fs.loc[fam].spread.max():.4f})")
    v2 = gate("V2 VERDICT WIDTH: share of instances where the seven choosers disagree on 4b",
              f"{split:.3f}", "> 0.25", split > 0.25)

    # V3 — portability of the chooser ranking across families
    R = reach.T[FAMILIES]
    rhos = [spearman(R[f1].values, R[f2].values) for f1, f2 in itertools.combinations(FAMILIES, 2)]
    rho_mean = float(np.nanmean(rhos))
    log(f"\n### chooser-ranking portability: {len(rhos)} pairwise Spearman rho over the seven "
        f"choosers' reach vectors, mean {rho_mean:+.3f}, "
        f"min {np.nanmin(rhos):+.3f}, max {np.nanmax(rhos):+.3f}")
    pooled = P.groupby("chooser").keep4b.mean().reindex(CHOOSERS).sort_values(ascending=False)
    log("    pooled over all 96 instances: "
        + " / ".join(f"{k} {v:.3f}" for k, v in pooled.items()))
    v3 = gate("V3 PORTABILITY: mean pairwise Spearman rho of per-chooser reach across families",
              f"{rho_mean:+.3f}", ">= +0.50", rho_mean >= 0.50)

    # V4 — capital arm at the protocol rung
    prot = P[P.cost == PROTOCOL_COST]
    win = prot[prot.keep4b]
    log(f"\n### CAPITAL ARM at the protocol {PROTOCOL_COST} bps rung: "
        f"{len(win)} of {len(prot)} picks clear 4b FULL+OOS; "
        f"{int(prot.keep4a.sum())} clear 4a FULL; {int(prot.keep4a_oos.sum())} clear 4a OOS.")
    if len(win):
        log(win.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        log("    (none — every pick at 10 bps fails at least one 4b leg)")
        log("    binding-leg census over the 42 protocol-rung picks: "
            + " / ".join(f"{k}:{v}" for k, v in prot.bind.value_counts().items()))
    v4 = gate("V4 CAPITAL: at least one 10 bps chooser pick clears 4b FULL+OOS",
              f"{len(win)}", ">= 1", len(win) >= 1)

    # whole-grid base rate, so the chooser reach has a denominator
    log(f"\n### whole-grid 4b FULL+OOS base rate (every cell, not just picks): "
        f"{C[C.cost==PROTOCOL_COST].keep4b.mean():.4f} at 10 bps; "
        + " / ".join(f"{c}bps {C[C.cost==c].keep4b.mean():.4f}" for c in COSTS))
    log("    binding leg over ALL failing cells at 10 bps: "
        + " / ".join(f"{k}:{v}" for k, v in
                     C[(C.cost == PROTOCOL_COST) & (~C.keep4b)].bind.value_counts()
                     .head(6).items()))

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\n## VERDICT  V1 {'YES' if v1 else 'NO'} (spread general) | V2 "
        f"{'YES' if v2 else 'NO'} (verdict width) | V3 {'YES' if v3 else 'NO'} (portable "
        f"ranking) | V4 {'YES' if v4 else 'NO'} (capital)")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
