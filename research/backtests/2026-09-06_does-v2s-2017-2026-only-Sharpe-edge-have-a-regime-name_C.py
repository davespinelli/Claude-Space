#!/usr/bin/env python3
"""Idea 278 — does v2's 2017-2026-only Sharpe edge have a regime name?  (lane C, 2026-09-06)

Parent: idea 274 (lane C).  It found that RULES v2's Sharpe advantage over a MATCHED
constant-gross control does not exist in 2009-2016 (v2 1.1043 vs CG 1.1116) and is a
2017-2026 statistic.  The question this script answers: is that IS/OOS gap a change in
the GATE's BEHAVIOUR (it does something different, conditional on regime) or a change in
the WINDOW's CRASH CONTENT (the same conditional behaviour, met with more of the days it
pays in)?  That is idea 111/257's denominator question, asked of the live book.

Method
------
d_t = r_V2,t - r_CG(g*),t, the daily return difference against the realised-gross-matched
constant-gross control.  Classify every day by an SPY-only regime label known at t:

  A  state200    SPY above / below its own 200d MA                       (2 buckets)
  B  voltercile  SPY 20d realised vol, terciles                          (3 buckets)
  C  ddbucket    SPY drawdown from running max: 0-5 / 5-10 / 10-20 / 20+ (4 buckets)

Then, per axis:
  Q1  the conditional table: bucket share, mean d (pp/yr), t, V2 and CG conditional
      Sharpe and V2's realised gross, computed separately in IS and OOS.
  Q2  SHIFT-SHARE of the OOS-minus-IS gap in mean d:
        D = SUM_b (w_b^O - w_b^I) m_b^I     MIX        (window crash content)
          + SUM_b  w_b^I (m_b^O - m_b^I)    BEHAVIOUR  (the gate itself)
          + SUM_b (w_b^O - w_b^I)(m_b^O - m_b^I)  INTERACTION.
  Q3  the SHARPE gap, which is not additive, by REWEIGHTING: recompute the OOS Sharpe of
      each arm with day weights that restore the IS bucket composition ("OOS at IS crash
      content"), and the mirror (IS at OOS content).  If the OOS edge collapses under IS
      weights, the edge is window content; if it survives, it is the gate.
  Q4  regime-conditional ARMS: apply the gate only when the day's bucket is in S, hold
      constant gross g otherwise.  Every bucket of every axis is one arm; all reported.
  Q5  rule 8 walk-forward: selectors see 2009-2016 only, 2017-2026 read once.  Both KEEP
      paths (4a vs the live book, 4b vs SPY) evaluated on every arm and every ladder rung.

Tuned parameters: TWO — the control/arm base gross g (full ladder 0.20..1.00 reported) and
the arming set S (every single bucket of every axis reported).  The vol-tercile breakpoints
are NOT tuned: they are pre-registered from IS days and the full-sample variant is reported
beside them as a sensitivity, not chosen between.

Costs 10 bps (0 bps rung reported beside it, idea 262), weekly cadence, next-day execution.
Panels: u56 (live) and broad B136 (survivorship: current constituents only, rule 9).
Deterministic, standalone:
    python research/backtests/2026-09-06_does-v2s-2017-2026-only-Sharpe-edge-have-a-regime-name_C.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
BAND, NOMINAL_GROSS, FREQ = 0.03, 0.75, "W"
RUNGS = (0, 10)
GROSS_LADDER = [round(x, 3) for x in np.arange(0.20, 1.001, 0.05)]
WARMUP = 260
DD_EDGES = [0.0, 0.05, 0.10, 0.20, 1.01]            # pre-registered, not swept
DD_NAMES = ["dd0-5", "dd5-10", "dd10-20", "dd20+"]


# ------------------------------------------------------------------ books
def ew_priced(px):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def cg_weights(px, g):
    """No gate, constant nominal gross g."""
    return ew_priced(px) * g


def regime_arm_weights(px, armed, g=NOMINAL_GROSS):
    """Gate applied only on days where `armed` (a boolean Series on px.index) is True;
    constant gross g on every other day.  armed is SPY-derived and known at t."""
    ew = ew_priced(px) * g
    gate = band_state(px, BAND)
    eff = gate.where(armed.reindex(px.index).fillna(False), True)   # un-armed days: hold all
    return ew.where(eff, 0.0)


# ------------------------------------------------------------------ regimes
def spy_regimes(px, is_slice):
    """SPY-only labels, each known with data through t.  Returns a DataFrame of labels and
    a dict of the tercile breakpoints actually used."""
    spy = px["SPY"]
    ma200 = spy.rolling(200).mean()
    vol20 = spy.pct_change().rolling(20).std() * np.sqrt(252)
    dd = (spy / spy.cummax() - 1.0).abs()

    out = pd.DataFrame(index=px.index)
    out["state200"] = np.where(spy > ma200, "above200", "below200")
    out.loc[ma200.isna(), "state200"] = np.nan
    out["ddbucket"] = pd.cut(dd, DD_EDGES, labels=DD_NAMES, right=False, include_lowest=True).astype(object)

    cuts = {}
    for tag, src in (("IS", vol20.loc[is_slice[0]:is_slice[1]]), ("FULL", vol20)):
        q1, q2 = float(src.quantile(1 / 3)), float(src.quantile(2 / 3))
        cuts[tag] = (q1, q2)
        col = f"voltercile_{tag}"
        out[col] = np.where(vol20 <= q1, "volLO", np.where(vol20 <= q2, "volMID", "volHI"))
        out.loc[vol20.isna(), col] = np.nan
    return out, cuts


# ------------------------------------------------------------------ stats
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def wsharpe(r, w=None):
    """Annualised Sharpe of daily returns r, optionally with day weights w (>=0)."""
    r = r.astype(float)
    if w is None:
        w = pd.Series(1.0, index=r.index)
    w = w.reindex(r.index).fillna(0.0)
    s = w.sum()
    if s <= 0:
        return np.nan
    mu = float((w * r).sum() / s)
    var = float((w * (r - mu) ** 2).sum() / s)
    sd = np.sqrt(var)
    return (mu * 252) / (sd * np.sqrt(252)) if sd > 0 else np.nan


def ann_mean_pp(r):
    return float(r.mean()) * 252 * 100


def tstat(x):
    x = x.dropna()
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 and x.std(ddof=1) > 0 else np.nan


def fail4b(r, spy):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fail4a(r, base_r):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base_r)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base_r)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def run(px, w, bps, start):
    res = backtest(px, w, cost_bps=bps, freq=FREQ)
    return (res["returns"].loc[start:], res["weights"].sum(axis=1).loc[start:],
            res["turnover"].loc[start:])


def summarise(arm, name, r, gross, turn, base_r, spy, **extra):
    h1, h2 = half_sharpes(r)
    m, mi, mo = metrics(r), metrics(r.loc[IS_START:IS_END]), metrics(r.loc[OOS_START:])
    return dict(arm=arm, name=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                Vol=m["Vol"], H1=h1, H2=h2,
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                gross_mean=float(gross.mean()),
                gross_mean_IS=float(gross.loc[IS_START:IS_END].mean()),
                gross_mean_OOS=float(gross.loc[OOS_START:].mean()),
                turnover=float(turn.sum() / (len(turn) / 252)),
                f4a=fail4a(r, base_r), f4b=fail4b(r, spy), **extra)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


# ------------------------------------------------------------------ per-panel engine
def build(px, panel, verbose=True):
    """Run every arm on one panel at both cost rungs.  Returns (grid, series, regimes, cuts)."""
    start = px.index[WARMUP]
    reg, cuts = spy_regimes(px, (IS_START, IS_END))
    reg = reg.loc[start:]
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    rows, series = [], {}

    axes = {"state200": ["above200", "below200"],
            "voltercile_IS": ["volLO", "volMID", "volHI"],
            "voltercile_FULL": ["volLO", "volMID", "volHI"],
            "ddbucket": DD_NAMES}

    for bps in RUNGS:
        base_r, base_g, base_t = run(px, rules_v2_weights(px, BAND, NOMINAL_GROSS), bps, start)
        series[(bps, "V2")] = base_r
        rows.append(dict(panel=panel, bps=bps, family="LIVE",
                         **summarise("V2", "RULES v2 (live)", base_r, base_g, base_t, base_r, spy_r)))
        sm, smi, smo = metrics(spy_r), metrics(spy_r.loc[IS_START:IS_END]), metrics(spy_r.loc[OOS_START:])
        s1, s2 = half_sharpes(spy_r)
        rows.append(dict(panel=panel, bps=bps, family="BENCH", arm="SPY", name="SPY",
                         CAGR=sm["CAGR"], Sharpe=sm["Sharpe"], MaxDD=sm["MaxDD"], Vol=sm["Vol"],
                         H1=s1, H2=s2, IS_CAGR=smi["CAGR"], IS_Sharpe=smi["Sharpe"], IS_MaxDD=smi["MaxDD"],
                         OOS_CAGR=smo["CAGR"], OOS_Sharpe=smo["Sharpe"], OOS_MaxDD=smo["MaxDD"],
                         gross_mean=1.0, gross_mean_IS=1.0, gross_mean_OOS=1.0, turnover=0.0,
                         f4a=fail4a(spy_r, base_r), f4b="-"))

        for g in GROSS_LADDER:                                   # tuned param 1, all rungs
            r, gr, tu = run(px, cg_weights(px, g), bps, start)
            rows.append(dict(panel=panel, bps=bps, family="CG", g=g,
                             **summarise("CG", f"CG g={g:.2f}", r, gr, tu, base_r, spy_r)))
            series[(bps, f"CG{g:.2f}")] = r

        for axis, buckets in axes.items():                       # tuned param 2, all buckets
            if axis == "voltercile_FULL":
                continue                                          # sensitivity axis, no arms
            for b in buckets:
                armed = (reg[axis] == b).reindex(px.index).fillna(False)
                r, gr, tu = run(px, regime_arm_weights(px, armed, NOMINAL_GROSS), bps, start)
                rows.append(dict(panel=panel, bps=bps, family="ARM", axis=axis, bucket=b,
                                 armed_share=float(armed.loc[start:].mean()),
                                 armed_share_IS=float(armed.loc[IS_START:IS_END].mean()),
                                 armed_share_OOS=float(armed.loc[OOS_START:].mean()),
                                 **summarise("ARM", f"gate only in {b}", r, gr, tu, base_r, spy_r)))
                series[(bps, f"ARM:{axis}:{b}")] = r
        if verbose:
            print(f"  [{panel} @{bps}bps] {len(rows)} rows so far", flush=True)
    return pd.DataFrame(rows), series, reg, cuts, base_g


# ------------------------------------------------------------------ main
def main():
    pd.set_option("display.width", 260)
    print("=" * 104)
    print("Idea 278 — does v2's 2017-2026-only Sharpe edge have a regime name?  (lane C, 2026-09-06)")
    print("=" * 104)

    allgrid, allcond, alldec, allrw, allwf, allch = [], [], [], [], [], []

    for panel, px in (("u56", load_universe()), ("broad", load_universe(broad=True))):
        start = px.index[WARMUP]
        print(f"\n### panel {panel}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
              f"evaluated from {start.date()}")
        grid, series, reg, cuts, v2_gross = build(px, panel)
        allgrid.append(grid)
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]

        # ---- matched control: the ladder rung whose REALISED gross matches v2's
        lad10 = grid[(grid.bps == 10) & (grid.family == "CG")]
        v210 = grid[(grid.bps == 10) & (grid.family == "LIVE")].iloc[0]
        gstar = float(lad10.loc[(lad10.gross_mean - v210.gross_mean).abs().idxmin()].g)
        gstar_IS = float(lad10.loc[(lad10.gross_mean_IS - v210.gross_mean_IS).abs().idxmin()].g)
        print(f"\nv2 realised gross {v210.gross_mean:.4f} (IS {v210.gross_mean_IS:.4f}, "
              f"OOS {v210.gross_mean_OOS:.4f}) -> matched rung g*={gstar:.2f}, IS-matched g*_IS={gstar_IS:.2f}")
        print(f"vol-tercile breakpoints: IS {cuts['IS'][0]:.4f}/{cuts['IS'][1]:.4f}   "
              f"FULL {cuts['FULL'][0]:.4f}/{cuts['FULL'][1]:.4f}")

        print("\n" + "-" * 104)
        print(f"Q0  [{panel}] THE GAP BEING EXPLAINED — v2 vs CG(g*) by window, every ladder rung reported")
        print("-" * 104)
        for bps in RUNGS:
            lad = grid[(grid.bps == bps) & (grid.family == "CG")].set_index("g")
            v2 = grid[(grid.bps == bps) & (grid.family == "LIVE")].iloc[0]
            print(f"\n  --- {panel} @{bps}bps  CG ladder")
            print(fmt(lad[["gross_mean", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                           "IS_Sharpe", "OOS_Sharpe", "OOS_CAGR", "turnover", "f4a", "f4b"]]))
            cg = lad.loc[gstar]
            print(f"  v2 : gross {v2.gross_mean:.4f} Sharpe {v2.Sharpe:.4f} IS {v2.IS_Sharpe:.4f} "
                  f"OOS {v2.OOS_Sharpe:.4f} CAGR {v2.CAGR:.4f} MaxDD {v2.MaxDD:.4f} 4a[{v2.f4a}] 4b[{v2.f4b}]")
            print(f"  dSharpe(V2-CG g*={gstar:.2f}): FULL {v2.Sharpe-cg.Sharpe:+.4f}   "
                  f"IS {v2.IS_Sharpe-cg.IS_Sharpe:+.4f}   OOS {v2.OOS_Sharpe-cg.OOS_Sharpe:+.4f}   "
                  f"(IS->OOS swing {(v2.OOS_Sharpe-cg.OOS_Sharpe)-(v2.IS_Sharpe-cg.IS_Sharpe):+.4f})")

        # ---- the difference series at 10 bps, and its regime table
        rv2, rcg = series[(10, "V2")], series[(10, f"CG{gstar:.2f}")]
        d = (rv2 - rcg).dropna()
        gross_v2 = v2_gross

        print("\n" + "-" * 104)
        print(f"Q1  [{panel}] CONDITIONAL TABLE — d = r(V2) - r(CG g*={gstar:.2f}) @10bps, by regime and window")
        print("-" * 104)
        for axis in ("state200", "voltercile_IS", "voltercile_FULL", "ddbucket"):
            rows = []
            for win, sl in (("IS", slice(IS_START, IS_END)), ("OOS", slice(OOS_START, None)),
                            ("FULL", slice(None, None))):
                dd_ = d.loc[sl]; lab = reg[axis].reindex(dd_.index)
                for b in [x for x in pd.unique(reg[axis].dropna()) if isinstance(x, str)]:
                    m = lab == b
                    if m.sum() < 5:
                        rows.append(dict(window=win, bucket=b, n=int(m.sum()))); continue
                    dv = dd_[m]
                    rows.append(dict(window=win, bucket=b, n=int(m.sum()), share=float(m.mean()),
                                     d_pp_yr=ann_mean_pp(dv), t=tstat(dv),
                                     V2_Sharpe_cond=wsharpe(rv2.loc[sl][m]),
                                     CG_Sharpe_cond=wsharpe(rcg.loc[sl][m]),
                                     V2_gross=float(gross_v2.loc[sl][m].mean()),
                                     SPY_pp_yr=ann_mean_pp(spy_r.loc[sl][m])))
            T = pd.DataFrame(rows)
            T.insert(0, "axis", axis); T.insert(0, "panel", panel)
            allcond.append(T)
            print(f"\n  --- axis {axis}")
            print(fmt(T.drop(columns=["panel", "axis"]).set_index(["window", "bucket"])))

        # ---- Q2 shift-share
        print("\n" + "-" * 104)
        print(f"Q2  [{panel}] SHIFT-SHARE of the OOS-minus-IS gap in mean d (pp/yr)")
        print("      MIX = window crash content;  BEHAVIOUR = the gate;  INTERACTION = the cross term")
        print("-" * 104)
        dec_rows = []
        for axis in ("state200", "voltercile_IS", "voltercile_FULL", "ddbucket"):
            di, do = d.loc[IS_START:IS_END], d.loc[OOS_START:]
            li, lo = reg[axis].reindex(di.index), reg[axis].reindex(do.index)
            bs = [x for x in pd.unique(reg[axis].dropna()) if isinstance(x, str)]
            wI = np.array([float((li == b).mean()) for b in bs])
            wO = np.array([float((lo == b).mean()) for b in bs])
            mI = np.array([float(di[li == b].mean()) if (li == b).sum() else 0.0 for b in bs])
            mO = np.array([float(do[lo == b].mean()) if (lo == b).sum() else 0.0 for b in bs])
            tot = (wO * mO).sum() - (wI * mI).sum()
            mix = ((wO - wI) * mI).sum(); beh = (wI * (mO - mI)).sum(); inter = ((wO - wI) * (mO - mI)).sum()
            k = 252 * 100
            dec_rows.append(dict(panel=panel, axis=axis, gap_pp_yr=tot * k, MIX_pp_yr=mix * k,
                                 BEHAVIOUR_pp_yr=beh * k, INTERACTION_pp_yr=inter * k,
                                 MIX_share=mix / tot if tot else np.nan,
                                 BEHAVIOUR_share=beh / tot if tot else np.nan,
                                 INTERACTION_share=inter / tot if tot else np.nan))
        D = pd.DataFrame(dec_rows); alldec.append(D)
        print(fmt(D.set_index(["panel", "axis"])))

        # ---- Q3 reweighted Sharpe
        print("\n" + "-" * 104)
        print(f"Q3  [{panel}] THE SHARPE GAP, REWEIGHTED — OOS days re-weighted to IS bucket composition")
        print("      (and the mirror).  dSharpe = V2 - CG(g*).  If the OOS edge collapses under IS")
        print("      weights the edge is WINDOW CONTENT; if it survives it is the GATE.")
        print("-" * 104)
        rw_rows = []
        for axis in ("state200", "voltercile_IS", "voltercile_FULL", "ddbucket"):
            di_idx, do_idx = d.loc[IS_START:IS_END].index, d.loc[OOS_START:].index
            li, lo = reg[axis].reindex(di_idx), reg[axis].reindex(do_idx)
            bs = [x for x in pd.unique(reg[axis].dropna()) if isinstance(x, str)]
            wI = {b: float((li == b).mean()) for b in bs}
            wO = {b: float((lo == b).mean()) for b in bs}
            # OOS days weighted so bucket shares equal IS shares
            wt_o = lo.map(lambda b: (wI.get(b, 0.0) / wO[b]) if wO.get(b, 0.0) > 0 else 0.0).astype(float)
            wt_i = li.map(lambda b: (wO.get(b, 0.0) / wI[b]) if wI.get(b, 0.0) > 0 else 0.0).astype(float)
            row = dict(panel=panel, axis=axis)
            row["IS_dSharpe"] = wsharpe(rv2.loc[di_idx]) - wsharpe(rcg.loc[di_idx])
            row["OOS_dSharpe"] = wsharpe(rv2.loc[do_idx]) - wsharpe(rcg.loc[do_idx])
            row["OOS_at_IS_content"] = wsharpe(rv2.loc[do_idx], wt_o) - wsharpe(rcg.loc[do_idx], wt_o)
            row["IS_at_OOS_content"] = wsharpe(rv2.loc[di_idx], wt_i) - wsharpe(rcg.loc[di_idx], wt_i)
            row["raw_gap"] = row["OOS_dSharpe"] - row["IS_dSharpe"]
            row["gap_left_after_reweight"] = row["OOS_at_IS_content"] - row["IS_dSharpe"]
            row["content_share_of_gap"] = (1 - row["gap_left_after_reweight"] / row["raw_gap"]) if row["raw_gap"] else np.nan
            row["V2_OOS_S"] = wsharpe(rv2.loc[do_idx]); row["V2_OOSatIS_S"] = wsharpe(rv2.loc[do_idx], wt_o)
            row["CG_OOS_S"] = wsharpe(rcg.loc[do_idx]); row["CG_OOSatIS_S"] = wsharpe(rcg.loc[do_idx], wt_o)
            # Kish effective sample size of the reweighting: how much of the OOS window is left
            row["ESS_OOS_at_IS"] = float(wt_o.sum() ** 2 / (wt_o ** 2).sum()) if (wt_o ** 2).sum() else np.nan
            row["ESS_frac"] = row["ESS_OOS_at_IS"] / len(do_idx)
            rw_rows.append(row)
        R = pd.DataFrame(rw_rows); allrw.append(R)
        print(fmt(R.set_index(["panel", "axis"])))

        # ---- Q3b: Sharpe is mean/vol — which of the two moves?
        print("\n" + "-" * 104)
        print(f"Q3b [{panel}] MEAN vs VOL CHANNEL — Sharpe = mean/vol, so the swing has two sources.")
        print("      Counterfactuals hold one window's means (or vols) fixed and swap the other.")
        print("-" * 104)
        ch = []
        for win, sl in (("IS", slice(IS_START, IS_END)), ("OOS", slice(OOS_START, None))):
            a, b = rv2.loc[sl], rcg.loc[sl]
            ch.append(dict(panel=panel, window=win,
                           V2_mean_pp_yr=ann_mean_pp(a), CG_mean_pp_yr=ann_mean_pp(b),
                           d_mean_pp_yr=ann_mean_pp(a) - ann_mean_pp(b),
                           V2_vol=float(a.std() * np.sqrt(252)), CG_vol=float(b.std() * np.sqrt(252)),
                           vol_ratio=float(a.std() / b.std()),
                           V2_S=wsharpe(a), CG_S=wsharpe(b), dS=wsharpe(a) - wsharpe(b)))
        C = pd.DataFrame(ch)
        print(fmt(C.set_index(["panel", "window"])))
        i, o = C.iloc[0], C.iloc[1]
        k = 100.0
        dS_IS, dS_OOS = i.dS, o.dS
        dS_meanswap = (o.V2_mean_pp_yr / k) / i.V2_vol - (o.CG_mean_pp_yr / k) / i.CG_vol   # OOS means, IS vols
        dS_volswap = (i.V2_mean_pp_yr / k) / o.V2_vol - (i.CG_mean_pp_yr / k) / o.CG_vol    # IS means, OOS vols
        print(f"\n  dSharpe IS {dS_IS:+.4f} -> OOS {dS_OOS:+.4f}   swing {dS_OOS-dS_IS:+.4f}")
        print(f"    MEAN channel  (OOS means, IS vols):  dSharpe {dS_meanswap:+.4f}  -> moves the swing by "
              f"{dS_meanswap-dS_IS:+.4f} ({(dS_meanswap-dS_IS)/(dS_OOS-dS_IS):+.1%} of it)")
        print(f"    VOL  channel  (IS means, OOS vols):  dSharpe {dS_volswap:+.4f}  -> moves the swing by "
              f"{dS_volswap-dS_IS:+.4f} ({(dS_volswap-dS_IS)/(dS_OOS-dS_IS):+.1%} of it)")
        print(f"    vol(V2)/vol(CG): IS {i.vol_ratio:.4f} -> OOS {o.vol_ratio:.4f} "
              f"({100*(o.vol_ratio-i.vol_ratio):+.2f} pp of relative vol)")
        C["dS_meanswap"] = dS_meanswap; C["dS_volswap"] = dS_volswap
        allch.append(C)

        # ---- Q4 arms, gross-matched to the ladder by realised gross
        print("\n" + "-" * 104)
        print(f"Q4  [{panel}] REGIME-CONDITIONAL ARMS (gate only inside the bucket, CG gross elsewhere)")
        print("      Each arm quoted against the ladder rung matching ITS OWN realised gross (idea 244).")
        print("-" * 104)
        for bps in RUNGS:
            lad = grid[(grid.bps == bps) & (grid.family == "CG")]
            arms = grid[(grid.bps == bps) & (grid.family == "ARM")].copy()
            v2 = grid[(grid.bps == bps) & (grid.family == "LIVE")].iloc[0]
            mrow = arms.gross_mean.apply(lambda gm: lad.loc[(lad.gross_mean - gm).abs().idxmin()])
            arms["match_g"] = mrow.g.values
            arms["dS_vs_matchedCG"] = arms.Sharpe.values - mrow.Sharpe.values
            arms["dOOS_vs_matchedCG"] = arms.OOS_Sharpe.values - mrow.OOS_Sharpe.values
            arms["dS_vs_V2"] = arms.Sharpe.values - v2.Sharpe
            print(f"\n  --- {panel} @{bps}bps   (v2: S {v2.Sharpe:.4f} IS {v2.IS_Sharpe:.4f} "
                  f"OOS {v2.OOS_Sharpe:.4f} gross {v2.gross_mean:.4f})")
            print(fmt(arms.set_index(["axis", "bucket"])[
                ["armed_share", "armed_share_IS", "armed_share_OOS", "gross_mean", "CAGR", "Sharpe",
                 "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe", "match_g", "dS_vs_matchedCG",
                 "dOOS_vs_matchedCG", "turnover", "f4a", "f4b"]]))
            arms.to_csv(OUT.with_name(f"{OUT.name}_{panel}_{bps}bps_arms.csv"), index=False)

        # ---- Q5 rule-8 walk-forward
        print("\n" + "-" * 104)
        print(f"Q5  [{panel}] RULE 8 WALK-FORWARD — selectors read 2009-2016 only; 2017-2026 read once")
        print("-" * 104)
        wf = []
        for bps in RUNGS:
            sl = grid[grid.bps == bps]
            v2 = sl[sl.family == "LIVE"].iloc[0]
            spy = sl[sl.family == "BENCH"].iloc[0]
            lad = sl[sl.family == "CG"]; arms = sl[sl.family == "ARM"]
            picks = [("do-nothing V2", v2),
                     ("CG IS-argmax g", lad.loc[lad.IS_Sharpe.idxmax()]),
                     ("CG IS-gross-matched", lad.loc[(lad.gross_mean_IS - v2.gross_mean_IS).abs().idxmin()]),
                     ("ARM IS-argmax (any axis)", arms.loc[arms.IS_Sharpe.idxmax()])]
            for axis in sorted(arms.axis.unique()):
                a = arms[arms.axis == axis]
                picks.append((f"ARM IS-argmax {axis}", a.loc[a.IS_Sharpe.idxmax()]))
            cand = pd.concat([sl[sl.family == "LIVE"], lad, arms])
            picks.append(("chooser over ALL", cand.loc[cand.IS_Sharpe.astype(float).idxmax()]))
            picks.append(("SPY", spy))
            for label, p in picks:
                wf.append(dict(panel=panel, bps=bps, selector=label, pick=p["name"],
                               IS_Sharpe=p.IS_Sharpe, IS_CAGR=p.IS_CAGR,
                               OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                               f4a=p.f4a, f4b=p.f4b))
        W = pd.DataFrame(wf); allwf.append(W)
        print(fmt(W.set_index(["panel", "bps", "selector"])))

        # ---- KEEP census on this panel
        cen = grid[grid.family != "BENCH"].groupby(["bps", "family"]).agg(
            n=("Sharpe", "size"), pass4a=("f4a", lambda s: (s == "-").sum()),
            pass4b=("f4b", lambda s: (s == "-").sum()), mean_Sharpe=("Sharpe", "mean"),
            mean_OOS=("OOS_Sharpe", "mean"))
        print(f"\n  KEEP census [{panel}]:")
        print(fmt(cen))

    G = pd.concat([g for g in allgrid if len(g)], ignore_index=True)
    G.to_csv(OUT.with_name(OUT.name + "_grid.csv"), index=False)
    pd.concat(allcond, ignore_index=True).to_csv(OUT.with_name(OUT.name + "_conditional.csv"), index=False)
    pd.concat(alldec, ignore_index=True).to_csv(OUT.with_name(OUT.name + "_decomposition.csv"), index=False)
    pd.concat(allrw, ignore_index=True).to_csv(OUT.with_name(OUT.name + "_reweight.csv"), index=False)
    pd.concat(allch, ignore_index=True).to_csv(OUT.with_name(OUT.name + "_channel.csv"), index=False)
    pd.concat([w for w in allwf if len(w)], ignore_index=True).to_csv(
        OUT.with_name(OUT.name + "_walkforward.csv"), index=False)

    print("\n" + "=" * 104)
    print("TOTAL KEEP census over every non-benchmark row, both panels, both rungs")
    print("=" * 104)
    nb = G[G.family != "BENCH"]
    print(fmt(nb.groupby(["panel", "bps", "family"]).agg(
        n=("Sharpe", "size"), pass4a=("f4a", lambda s: (s == "-").sum()),
        pass4b=("f4b", lambda s: (s == "-").sum()))))
    print(f"\nTOTAL: 4a {int((nb.f4a=='-').sum())} / {len(nb)},  4b {int((nb.f4b=='-').sum())} / {len(nb)}")
    if (nb.f4b == "-").any():
        print("\n4b PASSING ROWS:")
        print(fmt(nb[nb.f4b == "-"][["panel", "bps", "family", "name", "CAGR", "Sharpe", "MaxDD",
                                     "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "gross_mean", "turnover"]]))
    if (nb.f4a == "-").any():
        print("\n4a PASSING ROWS:")
        print(fmt(nb[nb.f4a == "-"][["panel", "bps", "family", "name", "CAGR", "Sharpe", "MaxDD",
                                     "H1", "H2", "OOS_Sharpe", "gross_mean", "turnover"]]))
    print(f"\nWrote {OUT.name}_{{grid,conditional,decomposition,reweight,channel,walkforward}}.csv")


if __name__ == "__main__":
    main()
