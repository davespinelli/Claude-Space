#!/usr/bin/env python3
"""Idea 272 — hold the ratio fixed DAY BY DAY, not at the median.  (cloud, 2026-09-09)

QUEUE ASK
    Idea 269C's matched-ratio grid set `n = round(r* * median n_elig)` once per panel, but
    n_elig moves 18 -> 48 on U56 and 48 -> 116 on B136 across the sample, so the REALISED
    ratio drifts and `sat_share` (the share of rebalance days on which the ranked book
    already holds every eligible name, i.e. IS EWall) reaches 0.52 at r*=1.  Re-run the
    grid with a time-varying n_t = round(r* * n_elig,t) so the ratio is genuinely held
    fixed, and report whether the NON-MONOTONICITY of the reversal-share curve and the
    PANEL DISAGREEMENT survive.

DESIGN
    Idea 269C's five panels and seven pre-registered ratios, unchanged.  Two constructions:
      FIXED    n = max(1, round(r* * median n_elig on weekly rebalance days))   [269C verbatim]
      DYN      n_t = clip(round(r* * n_elig,t), 1, n_elig,t) recomputed EVERY day
    Everything else is idea 269C's: key = composite WITHOUT the vol scaler, gate =
    above-200d AND vol20 < 0.60, equal weight at gross 0.75, weekly, t+1 execution.
    A cell REVERSES exactly as the parent defines it: sign(dSharpe) != sign(dCAGR) for
    EWall minus FWD, with the parent's own tie bands EPS_S 0.005 / EPS_C 0.0005.

    REPRODUCTION GATE, run before any new number is read: the FIXED arm must return idea
    269C's published reversal-share sequence 0.60 / 0.60 / 0.80 / 0.80 / 0.40 / 0.40 / 0.00
    over r* = 0.05..1.00, its per-panel counts B136 6/7, BSTK100 6/7, U56 4/7, ETF36 2/7,
    SMALL439 0/7, its EWall books (B136 10.7%/1.026/-17.7% OOS 1.019; U56 10.4%/1.049/
    -15.9%) and its KEEP counts (10 bps 4a 6/40, 4b 8/40; 0 bps 4a 3/40, 4b 12/40).

TUNED PARAMETERS (PROTOCOL rule 4: max 2)
    1. construction in {FIXED, DYN}
    2. the target ratio r*
    Panel and cost rung are ENUMERATED reporting axes; every grid point is written to
    .grid.csv and every reversal cell to .reversal.csv.

CONVENTIONS
    10 bps headline per PROTOCOL rule 2, with 0 bps (the parent's diagnostic) and 25 bps
    reported beside it.  Weights decided at close t, applied at t+1 (engine).  Long only,
    no leverage.  PROTOCOL rule 8: r* is chosen on IS 2009-01-01..2016-12-31 alone and the
    OOS window 2017-01-01+ is read once.  Both KEEP paths (4a against the LIVE RULES v2
    book on the same panel, 4b against SPY) are evaluated for every arm.
    SURVIVORSHIP: B136 / BSTK100 / ETF36 are current constituents of universe_broad.json
    and SMALL439 is the 483-name sub-$2B screen with the 44 tickers whose
    `max_1d_move >= 1.0` dropped first (data/small_meta.csv, data/SMALL_PANEL_README.md).
    Every panel is therefore a current-constituent list; the un-ranked EWall side takes the
    full survivorship premium, so the bias runs TOWARD reversals.  No network is used.

Outputs: .grid.csv .reversal.csv .drift.csv .walkforward.csv .console.txt .result.md
"""
from __future__ import annotations
import json, sys, time, warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights            # noqa: E402
from engine import backtest, metrics, rebalance_mask                   # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"

FREQ, MAX_VOL, GROSS, W_FIXED = "W", 0.60, 0.75, 0.15
RATIOS = [0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00]        # 269C's, pre-registered
RUNGS = [0, 10, 25]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
EPS_S, EPS_C = 0.005, 0.0005                               # 269C's tie bands, unchanged
PUB_SHARE = [0.60, 0.60, 0.80, 0.80, 0.40, 0.40, 0.00]     # published FIXED curve
PUB_PANEL = {"B136": 6, "BSTK100": 6, "U56": 4, "ETF36": 2, "SMALL439": 0}

_log: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan, np.nan
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    r = np.corrcoef(rx, ry)[0, 1]
    n = len(x)
    t = r * np.sqrt((n - 2) / max(1e-12, 1 - r ** 2)) if abs(r) < 1 else np.inf
    return float(r), float(t)


# ============================================================== panels (269C's five)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])          # ALWAYS dropped first
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56": sub(px56, list(px56.columns)),
        "B136": sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL439": sub(pxs, s_stk, tradable=s_stk),
        "ETF36": sub(px136, etf36, tradable=etf36),
    }


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


# ============================================================== books
def weights(px, tradable, arm, n=None, ratio=None):
    """arm in {EWall, v1, FWD (fixed n), FWDDYN (time-varying n_t = round(ratio*n_elig_t))}."""
    elig = eligible_mask(px, tradable)
    if arm == "v1":
        s = score(px, vol_scale=True)[0]
        return (s.where(elig).rank(axis=1, ascending=False) <= 5).astype(float) * W_FIXED
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        key = score(px, vol_scale=False)[0]
        rank = key.where(elig).rank(axis=1, ascending=False)
        if arm == "FWD":
            sel = (rank <= n).astype(float)
        elif arm == "FWDDYN":
            ne = elig.sum(axis=1)
            n_t = np.rint(ratio * ne.to_numpy()).astype(float)
            n_t = np.clip(n_t, 1.0, np.maximum(1.0, ne.to_numpy()))
            sel = rank.le(pd.Series(n_t, index=px.index), axis=0).astype(float)
        else:
            raise ValueError(arm)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def v4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# ============================================================== grid
def run_grid(panels):
    rows, cache, drift = [], {}, []
    for pname, (px, tr) in panels.items():
        t0 = time.time()
        elig = eligible_mask(px, tr)
        rmask = rebalance_mask(px.index, FREQ)
        start = px.index[260]
        nel_reb = elig[rmask.values].sum(axis=1).loc[start:]        # weekly rebalance days
        ne_med = float(nel_reb.median())
        spy = px["SPY"].pct_change().fillna(0)
        ne_all = elig.sum(axis=1)

        arms = [("EWall", None, np.nan, "-"), ("v1", None, np.nan, "-")]
        for rt in RATIOS:
            arms.append(("FWD", int(max(1, round(rt * ne_med))), rt, "FIXED"))
            arms.append(("FWDDYN", None, rt, "DYN"))

        # ---- realised-ratio drift diagnostics on rebalance days
        for rt in RATIOS:
            nfix = int(max(1, round(rt * ne_med)))
            ne_r = nel_reb
            r_fix = nfix / ne_r
            n_dyn = np.clip(np.rint(rt * ne_all.loc[start:]), 1, np.maximum(1, ne_all.loc[start:]))
            n_dyn = n_dyn[rmask.loc[start:].values]
            r_dyn = n_dyn / ne_r
            drift.append(dict(panel=pname, r_target=rt, n_elig_med=ne_med,
                              n_elig_p10=float(ne_r.quantile(.10)), n_elig_p90=float(ne_r.quantile(.90)),
                              n_fixed=nfix,
                              FIXED_r_mean=float(r_fix.mean()), FIXED_r_sd=float(r_fix.std()),
                              FIXED_r_p10=float(r_fix.quantile(.10)), FIXED_r_p90=float(r_fix.quantile(.90)),
                              FIXED_sat=float((ne_r <= nfix).mean()),
                              DYN_r_mean=float(r_dyn.mean()), DYN_r_sd=float(r_dyn.std()),
                              DYN_r_p10=float(r_dyn.quantile(.10)), DYN_r_p90=float(r_dyn.quantile(.90)),
                              DYN_sat=float((n_dyn >= ne_r).mean()),
                              DYN_n_min=float(n_dyn.min()), DYN_n_max=float(n_dyn.max())))

        for arm, n, rt, cons in arms:
            w = weights(px, tr, arm, n=n, ratio=rt)
            wr = w.loc[start:]
            for bps in RUNGS:
                res = backtest(px, w, cost_bps=bps, freq=FREQ)
                r = res["returns"].loc[start:]
                sp = spy.loc[start:]
                r_is, r_oos = r.loc[IS_START:IS_END], r.loc[OOS_START:]
                sp_is, sp_oos = sp.loc[IS_START:IS_END], sp.loc[OOS_START:]
                mm, mo, mi = metrics(r), metrics(r_oos), metrics(r_is)
                h1, h2 = half_sharpes(r)
                held = (wr > 0).sum(axis=1)[rmask.loc[start:].values]
                if arm == "FWD":
                    sat = float((nel_reb <= n).mean())
                elif arm == "FWDDYN":
                    nd = np.clip(np.rint(rt * ne_all.loc[start:]), 1,
                                 np.maximum(1, ne_all.loc[start:]))[rmask.loc[start:].values]
                    sat = float((nd >= nel_reb).mean())
                else:
                    sat = np.nan
                cache[(pname, arm, rt, bps)] = dict(r=r, sp=sp, r_oos=r_oos, sp_oos=sp_oos)
                rows.append(dict(
                    panel=pname, arm=arm, cons=cons, r_target=rt, bps=bps,
                    n=(n if n else np.nan), n_elig_med=ne_med,
                    r_real=float((held / nel_reb).mean()), held_mean=float(held.mean()),
                    held_min=float(held.min()), held_max=float(held.max()), sat_share=sat,
                    CAGR=mm["CAGR"], Vol=mm["Vol"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                    H1=h1, H2=h2,
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    turn=float(res["turnover"].loc[start:].sum() / (len(r) / 252)),
                    gross=float(wr.sum(axis=1).mean()),
                    SPY_CAGR=metrics(sp)["CAGR"], SPY_Sharpe=metrics(sp)["Sharpe"],
                    SPY_MaxDD=metrics(sp)["MaxDD"], SPY_OOS_Sharpe=metrics(sp_oos)["Sharpe"]))
        # ---- KEEP paths: 4a against the LIVE RULES v2 book, 4b against SPY
        for bps in RUNGS:
            base_v2 = backtest(px, rules_v2_weights(px), cost_bps=bps,
                               freq=FREQ)["returns"].loc[start:]
            cache[(pname, "RULESv2", np.nan, bps)] = dict(r=base_v2)
            for i, rr in enumerate(rows):
                if rr["panel"] != pname or rr["bps"] != bps:
                    continue
                c = cache[(pname, rr["arm"], rr["r_target"], bps)]
                rows[i]["p4a"] = v4a(c["r"], base_v2)
                rows[i]["p4a_v1"] = v4a(c["r"], cache[(pname, "v1", np.nan, bps)]["r"])
                rows[i]["f4b"] = fail4b(c["r"], c["sp"], c["r_oos"], c["sp_oos"])
                rows[i]["p4b"] = (rows[i]["f4b"] == "-")
        P(f"  {pname:<10} {px.shape[0]}x{px.shape[1]} tradable {len(tr):>3} "
          f"n_elig med {ne_med:6.1f} p10/p90 {nel_reb.quantile(.10):.0f}/{nel_reb.quantile(.90):.0f}"
          f"  {time.time() - t0:6.1f}s")
    return pd.DataFrame(rows), pd.DataFrame(drift), cache


# ============================================================== reversal
def reversal_table(grid, bps, cons, window=""):
    S, C = f"{window}Sharpe", f"{window}CAGR"
    arm = "FWD" if cons == "FIXED" else "FWDDYN"
    g = grid[grid.bps == bps]
    out = []
    for pname, d in g.groupby("panel"):
        ew = d[d.arm == "EWall"].iloc[0]
        for _, f in d[d.arm == arm].sort_values("r_target").iterrows():
            dS, dC = ew[S] - f[S], ew[C] - f[C]
            out.append(dict(panel=pname, cons=cons, bps=bps, r_target=f.r_target,
                            r_real=f.r_real, sat_share=f.sat_share, held_mean=f.held_mean,
                            S_ew=ew[S], S_fwd=f[S], C_ew=ew[C], C_fwd=f[C], dS=dS, dC=dC,
                            rev=bool((np.sign(dS) != np.sign(dC)) and abs(dS) > EPS_S
                                     and abs(dC) > EPS_C),
                            ew_wins_S=bool(dS > EPS_S), ew_wins_C=bool(dC > EPS_C),
                            turn_fwd=f.turn, turn_ew=ew.turn))
    return pd.DataFrame(out)


def share_curve(t):
    return t.groupby("r_target").rev.mean()


def n_turns(seq):
    """Direction changes in a sequence (the parent's 'rises before it falls' shape)."""
    d = [np.sign(b - a) for a, b in zip(seq[:-1], seq[1:]) if b != a]
    return sum(1 for a, b in zip(d[:-1], d[1:]) if a != b)


# ============================================================== rule 8
def rule8(grid, cache, panels):
    """r* chosen on the IS window only (per construction), OOS read once.
    Selector = the IS-argmax OOS-blind rule the parent used: pick the r* whose FWD book has
    the best IS Sharpe, pooled equal-weight over the five panels."""
    out = []
    for cons, arm in (("FIXED", "FWD"), ("DYN", "FWDDYN")):
        g = grid[(grid.bps == 10) & (grid.arm == arm)]
        pooled_is = g.groupby("r_target").IS_Sharpe.mean()
        r_star = float(pooled_is.idxmax())
        rets = {}
        for pname in panels:
            rets[pname] = cache[(pname, arm, r_star, 10)]["r"]
        # equal-weight pooled book across panels (the parent's pooling)
        idx = sorted(set().union(*[set(r.index) for r in rets.values()]))
        pooled = pd.concat([r.reindex(idx).fillna(0.0) for r in rets.values()], axis=1).mean(axis=1)
        m, mo = metrics(pooled), metrics(pooled.loc[OOS_START:])
        h1, h2 = half_sharpes(pooled)
        out.append(dict(book=f"{cons} r*={r_star:.2f} (IS-argmax)", CAGR=m["CAGR"],
                        Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    # comparands, pooled the same way
    for nm, key in (("EWall (do nothing)", "EWall"), ("RULES v1", "v1"), ("RULES v2 (live)", "RULESv2")):
        rr = []
        for pname in panels:
            rr.append(cache[(pname, key, np.nan, 10)]["r"])
        idx = sorted(set().union(*[set(r.index) for r in rr]))
        pooled = pd.concat([r.reindex(idx).fillna(0.0) for r in rr], axis=1).mean(axis=1)
        m, mo = metrics(pooled), metrics(pooled.loc[OOS_START:])
        h1, h2 = half_sharpes(pooled)
        out.append(dict(book=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                        OOS_MaxDD=mo["MaxDD"]))
    sp = []
    for pname, (px, _) in panels.items():
        s = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        sp.append(s)
    idx = sorted(set().union(*[set(s.index) for s in sp]))
    pooled = pd.concat([s.reindex(idx).fillna(0.0) for s in sp], axis=1).mean(axis=1)
    m, mo = metrics(pooled), metrics(pooled.loc[OOS_START:])
    h1, h2 = half_sharpes(pooled)
    out.append(dict(book="SPY (pooled calendars)", CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                    MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                    OOS_Sharpe=mo["OOS_Sharpe"] if "OOS_Sharpe" in mo else mo["Sharpe"],
                    OOS_MaxDD=mo["MaxDD"]))
    return pd.DataFrame(out)


# ============================================================== main
def main():
    t0 = time.time()
    P(f"# {STEM}")
    P("Idea 272 — hold r = n/n_elig fixed DAY BY DAY instead of at the panel median.\n")
    panels = build_panels()
    P("## Grid")
    grid, drift, cache = run_grid(panels)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    drift.to_csv(OUT / f"{STEM}.drift.csv", index=False)
    P(f"\ngrid.csv rows {len(grid)} (all grid points), {time.time() - t0:.0f}s\n")

    rev = pd.concat([reversal_table(grid, b, c)
                     for b in RUNGS for c in ("FIXED", "DYN")], ignore_index=True)
    rev_is = pd.concat([reversal_table(grid, 10, c, "IS_") for c in ("FIXED", "DYN")],
                       ignore_index=True).assign(window="IS")
    rev_oos = pd.concat([reversal_table(grid, 10, c, "OOS_") for c in ("FIXED", "DYN")],
                        ignore_index=True).assign(window="OOS")
    pd.concat([rev.assign(window="FULL"), rev_is, rev_oos],
              ignore_index=True).to_csv(OUT / f"{STEM}.reversal.csv", index=False)

    # -------------------------------------------------- reproduction gate
    P("## REPRODUCTION GATE (FIXED arm must equal idea 269C)")
    fx = rev[(rev.cons == "FIXED") & (rev.bps == 10)]
    cur = share_curve(fx)
    P("  share by r*  here     " + " / ".join(f"{v:.2f}" for v in cur.values))
    P("  share by r*  269C     " + " / ".join(f"{v:.2f}" for v in PUB_SHARE))
    ok_curve = np.allclose(cur.values, PUB_SHARE, atol=1e-9)
    pc = fx.groupby("panel").rev.sum().astype(int)
    P("  per-panel    here     " + ", ".join(f"{k} {int(v)}/7" for k, v in pc.items()))
    P("  per-panel    269C     " + ", ".join(f"{k} {v}/7" for k, v in PUB_PANEL.items()))
    ok_panel = all(int(pc.get(k, -1)) == v for k, v in PUB_PANEL.items())
    for pn, want in (("B136", (0.107, 1.026, -0.177, 1.019)), ("U56", (0.104, 1.049, -0.159, None))):
        e = grid[(grid.panel == pn) & (grid.arm == "EWall") & (grid.bps == 10)].iloc[0]
        P(f"  {pn}/EWall here {e.CAGR:.4f}/{e.Sharpe:.4f}/{e.MaxDD:.4f} OOS {e.OOS_Sharpe:.4f}"
          f"   269C {want[0]}/{want[1]}/{want[2]} OOS {want[3]}")
    for bps, w4a, w4b in ((10, 6, 8), (0, 3, 12)):
        s = grid[(grid.bps == bps) & (grid.cons.isin(["FIXED", "-"]))]
        s = s[s.arm.isin(["EWall", "v1", "FWD"])]
        P(f"  KEEP counts @{bps:>2} bps: 4a {int(s.p4a_v1.sum())}/{len(s)} (vs v1, the parent's"
          f" comparand)  4b {int(s.p4b.sum())}/{len(s)}   269C 4a {w4a}/40 4b {w4b}/40")
    P(f"  GATE: curve {'PASS' if ok_curve else 'FAIL'}, per-panel {'PASS' if ok_panel else 'FAIL'}")

    # -------------------------------------------------- the two questions
    P("\n## Q1 — does the NON-MONOTONICITY survive the day-by-day fix?  (10 bps)")
    tab = []
    for bps in RUNGS:
        for cons in ("FIXED", "DYN"):
            t = rev[(rev.cons == cons) & (rev.bps == bps)]
            c = share_curve(t)
            rho, tt = spearman(t.r_target, t.rev.astype(float))
            t1 = t[t.r_target < 1.0]
            rho1, tt1 = spearman(t1.r_target, t1.rev.astype(float))
            tab.append(dict(bps=bps, cons=cons, cells=len(t), rev=int(t.rev.sum()),
                            **{f"r{r:.2f}": c.get(r, np.nan) for r in RATIOS},
                            turns=n_turns(list(c.values)),
                            spearman=rho, t=tt, spearman_no_r1=rho1, t_no_r1=tt1))
    tab = pd.DataFrame(tab)
    P(fmt(tab))

    P("\n## Q2 — does the PANEL DISAGREEMENT survive?  (counts out of 7 ratios)")
    pt = rev[rev.bps == 10].pivot_table(index="panel", columns="cons", values="rev",
                                        aggfunc="sum").astype(int)
    pt["FIXED_269C"] = pd.Series(PUB_PANEL)
    P(fmt(pt, 0))
    for cons in ("FIXED", "DYN"):
        t = rev[(rev.cons == cons) & (rev.bps == 10)]
        both = t.groupby("r_target").rev.agg(["sum", "count"])
        rows_split = int(((both["sum"] > 0) & (both["sum"] < both["count"])).sum())
        P(f"  {cons}: rows where the five panels DISAGREE (0<share<1): {rows_split}/7"
          f"   [269C published 6/7]")

    P("\n## Realised-ratio drift, the queue's own premise")
    P(fmt(drift[["panel", "r_target", "n_elig_med", "n_elig_p10", "n_elig_p90", "n_fixed",
                 "FIXED_r_mean", "FIXED_r_sd", "FIXED_sat", "DYN_r_mean", "DYN_r_sd",
                 "DYN_sat", "DYN_n_min", "DYN_n_max"]]))
    P(f"\n  mean realised-ratio sd:  FIXED {drift.FIXED_r_sd.mean():.4f}   "
      f"DYN {drift.DYN_r_sd.mean():.4f}")
    P(f"  max sat_share:           FIXED {drift.FIXED_sat.max():.4f}   "
      f"DYN {drift.DYN_sat.max():.4f}")

    P("\n## Cell-by-cell agreement between the two constructions (10 bps, 35 cells)")
    j = rev[(rev.bps == 10) & (rev.cons == "FIXED")].merge(
        rev[(rev.bps == 10) & (rev.cons == "DYN")], on=["panel", "r_target"],
        suffixes=("_fx", "_dy"))
    P(f"  agree on the reversal flag: {int((j.rev_fx == j.rev_dy).sum())}/{len(j)}")
    flips = j[j.rev_fx != j.rev_dy][["panel", "r_target", "rev_fx", "rev_dy", "dS_fx",
                                     "dS_dy", "dC_fx", "dC_dy", "sat_share_fx", "sat_share_dy"]]
    if len(flips):
        P(fmt(flips))

    # -------------------------------------------------- rule 8
    P("\n## PROTOCOL rule 8 walk-forward (r* chosen on IS 2009-2016, OOS 2017+ read once)")
    wf = rule8(grid, cache, panels)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(wf))
    P("\n  Reversal share measured separately in each window (10 bps):")
    w = pd.concat([rev_is, rev_oos], ignore_index=True)
    P(fmt(w.pivot_table(index="r_target", columns=["cons", "window"], values="rev")))

    # -------------------------------------------------- KEEP paths
    P("\n## KEEP paths, every grid point")
    for bps in RUNGS:
        for cons in ("FIXED", "DYN"):
            s = grid[(grid.bps == bps) & (grid.cons == cons)]
            P(f"  {cons:<5} @{bps:>2} bps: 4a(v2) {int(s.p4a.sum())}/{len(s)}   "
              f"4a(v1) {int(s.p4a_v1.sum())}/{len(s)}   4b {int(s.p4b.sum())}/{len(s)}")
    k = grid[grid.p4b & (grid.bps == 10)]
    P(f"\n  4b passers @10 bps ({len(k)}):")
    if len(k):
        P(fmt(k[["panel", "arm", "cons", "r_target", "n", "held_mean", "CAGR", "Sharpe",
                 "MaxDD", "H1", "H2", "OOS_Sharpe", "turn"]]))
    ka = grid[grid.p4a & (grid.bps == 10)]
    P(f"\n  4a passers vs the LIVE RULES v2 book @10 bps ({len(ka)}):")
    if len(ka):
        P(fmt(ka[["panel", "arm", "cons", "r_target", "n", "CAGR", "Sharpe", "MaxDD",
                  "H1", "H2", "OOS_Sharpe"]]))
    P("\n  binding 4b bar over all failures @10 bps:")
    fails = grid[(grid.bps == 10) & (~grid.p4b)].f4b.str.split(",").explode()
    P(fmt(fails.value_counts().rename("cells").to_frame(), 0))

    P(f"\nDone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
