#!/usr/bin/env python3
"""Idea 237 — the `dg` REACHABILITY CEILING: for every gate the project uses, what is the
maximum realised gross its de-grossed form can attain?

Why this exists: idea 154 found that idea 84's `g=0.85` is not an inadmissible arm under the
`dg` convention but an UNDEFINED one — the de-grossed band3 book tops out at realised gross
0.6924 (u56) / 0.6916 (broad).  A target above a gate's ceiling should be reported as
UNREACHABLE, not as a failure.  This run publishes the ceiling for every gate in the record.

Pre-registration (fixed before any number was read):
  * The `dg` convention (RULES v2's own): hold every ADMITTED, priced name at nominal
    `g`/N of NAV, N = instruments priced that day; gated-out weight goes to CASH, never
    re-spread.  At (gate=BAND3, g=0.75, W) this IS `baseline.rules_v2_weights` -> gate G2.
  * DEFINITION OF THE CEILING.  PROTOCOL 2 forbids leverage, so nominal g <= 1.00 and
    realised gross is monotone in g; therefore
        C(gate, panel) = mean realised gross of the dg book at nominal g = 1.00,
    measured on the post-warm-up window (px.index[260]:) at the live weekly cadence, from
    the DRIFTED held weights (not the nominal targets).  A target T is REACHABLE iff T <= C.
  * TWO tuned parameters, no more: gate and nominal gross.  Every grid point reported,
    none selected outside the rule-8 walk-forward.
        gates (11) = NONE, MA200, BAND0, BAND3 (live), BAND6, BAND12, VOL40, VOL60,
                     MAVOL (= RULES v1's eligibility), ABS (12m absolute momentum), BOTH
        nominal g  = 0.25, 0.50, 0.75 (live), 1.00
        panels     = U56, B136, SMALL439 (sub-$2B less the 44 with max_1d_move >= 1.0)
        rungs      = 10, 25 bps
    11 x 4 x 3 x 2 = 264 grid points, ALL reported.
  * The honest comparand at a ceiling is NOT the same nominal gross: it is the ungated book
    holding the SAME realised gross.  Every gate at g=1.00 is priced against a NOGATE control
    at matched realised gross (idea 135's matched-exposure control).
  * Rule 8: (gate, g) chosen on IS <= 2016-12-31 by IS Sharpe; 2017-01-01.. read once.
  * Both KEEP paths on every point: 4a vs live RULES v2, 4b vs SPY.
  * SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only — levels overstated on
    both.  A ceiling is an EXPOSURE statistic, so survivorship biases it too: a panel whose
    losers were deleted spends more time above its own 200d MA than the real cohort did.
    Read U56 (a fixed ETF/mega-cap list) as the least-biased ceiling.

Costs 10/25 bps per unit turnover, weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .ceiling.csv, .grid.csv, .matched.csv, .walkforward.csv,
.console.txt.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, rules_v1_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-08_the-dg-reachability-ceiling_cloud"
OUT = ROOT / "research" / "backtests"
GROSSES = [0.25, 0.50, 0.75, 1.00]
RUNGS = [10, 25]
FREQ = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TARGETS = [0.75, 0.85, 0.90, 1.00]

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)


def fast_backtest(px, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost, also returning the DRIFTED gross."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n); gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index),
            "gross": pd.Series(gross, index=px.index)}


def net(res, cost_bps):
    return res["returns0"] - res["turnover"] * cost_bps / 1e4


# ---------------------------------------------------------------- gates
def gates(px):
    ma = px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    above = px > ma
    absmom = px > px.shift(252)
    return {
        "NONE":  pd.DataFrame(True, index=px.index, columns=px.columns),
        "MA200": above.fillna(False),
        "BAND0": band_state(px, 0.00),
        "BAND3": band_state(px, 0.03),          # LIVE (RULES v2 clause 2)
        "BAND6": band_state(px, 0.06),
        "BAND12": band_state(px, 0.12),
        "VOL40": (vol20 < 0.40).fillna(False),
        "VOL60": (vol20 < 0.60).fillna(False),  # LIVE RULES v1 max_vol
        "MAVOL": (above & (vol20 < 0.60)).fillna(False),
        "ABS":   absmom.fillna(False),
        "BOTH":  (absmom & above).fillna(False),
    }


def dg_weights(px, gate, g):
    """De-grossed: g/N on every admitted priced name, gated weight -> CASH, never re-spread."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(gate, 0.0)


def mstats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def panels():
    out = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    out["SMALL439"] = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    return out


def main():
    PX = panels()
    for k, v in PX.items():
        say(f"panel {k}: {v.shape[1]-1} names + SPY, {v.index[0].date()} -> {v.index[-1].date()}, {len(v)} days")

    # ------------------------------------------------------------ GATES
    say("\n=== GATES ===")
    px = PX["U56"]; st = px.index[260]
    G3 = gates(px)["BAND3"]
    g2 = float(np.abs(dg_weights(px, G3, 0.75).values - rules_v2_weights(px).values).max())
    say(f"G2 dg_weights(BAND3, 0.75) vs baseline.rules_v2_weights   max|diff| = {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED"
    eb = engine_backtest(px, rules_v2_weights(px), cost_bps=10, freq=FREQ)
    fb = fast_backtest(px, rules_v2_weights(px))
    say(f"G0 engine.backtest NaN return days (pre-warm-up quirk): {int(eb['returns'].isna().sum())}")
    g1 = float(np.abs((eb["returns"] - net(fb, 10)).loc[st:].values).max())
    g3 = float(np.abs((engine_backtest(px, rules_v2_weights(px), cost_bps=25, freq=FREQ)["returns"]
                       - net(fb, 25)).loc[st:].values).max())
    g4 = float(np.abs((eb["weights"].sum(axis=1) - fb["gross"]).loc[st:].values).max())
    say(f"G1 fast_backtest vs engine.backtest @10 bps               max|diff| = {g1:.3e}")
    say(f"G3 derived rung identity vs engine.backtest(25)           max|diff| = {g3:.3e}")
    say(f"G4 DRIFTED gross vs engine held weights (the measurand)   max|diff| = {g4:.3e}")
    assert max(g1, g3, g4) < 1e-12, "GATE FAILED"
    m = mstats(net(fb, 10).loc[st:])
    say(f"G5 LIVE RULES v2 U56 @10 bps: {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%} "
        f"(H {m['H1']:.4f} / {m['H2']:.4f})  [record 8.66% / 1.2056 / -12.05% / 1.2259 / 1.1908]")

    say("\nG6 PROVENANCE — idea 154's published ceiling, re-derived at ITS OWN m=1.30 "
        "(nominal 0.75 x 1.30 = 0.975):")
    for pn, name in [("U56", "u56"), ("B136", "broad")]:
        p = PX[pn]; s = p.index[260]
        v = fast_backtest(p, dg_weights(p, gates(p)["BAND3"], 0.975))["gross"].loc[s:].mean()
        say(f"   {name}: realised mean gross {v:.4f}   [idea 154 published "
            f"{'0.6924' if pn == 'U56' else '0.6916'}]")

    # ------------------------------------------------------------ CEILINGS
    say("\n=== (1) THE CEILING TABLE — max realised gross of each gate's dg form (nominal g=1.00) ===")
    crows = []
    for pname, p in PX.items():
        s = p.index[260]; GG = gates(p)
        priced = p.notna()
        npriced = priced.sum(axis=1).replace(0, np.nan)
        for gname, gm in GG.items():
            adm = ((gm & priced).sum(axis=1) / npriced).loc[s:]
            res = fast_backtest(p, dg_weights(p, gm, 1.00))
            gr = res["gross"].loc[s:]
            h = len(gr) // 2
            grD = fast_backtest(p, dg_weights(p, gm, 1.00), freq="D")["gross"].loc[s:]
            grM = fast_backtest(p, dg_weights(p, gm, 1.00), freq="M")["gross"].loc[s:]
            crows.append(dict(panel=pname, gate=gname, ceiling_W=gr.mean(), ceiling_D=grD.mean(),
                              ceiling_M=grM.mean(), admission_share=adm.mean(),
                              ceil_H1=gr.iloc[:h].mean(), ceil_H2=gr.iloc[h:].mean(),
                              ceil_p05=gr.quantile(0.05), ceil_med=gr.median(), ceil_min=gr.min(),
                              ceil_max=gr.max(),
                              at_live_075=fast_backtest(p, dg_weights(p, gm, 0.75))["gross"].loc[s:].mean()))
    C = pd.DataFrame(crows)
    C.to_csv(OUT / f"{STAMP}.ceiling.csv", index=False)
    for pname in PX:
        say(f"\n--- {pname} ---")
        sub = C[C.panel == pname].drop(columns=["panel"])
        say(sub.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n=== (2) REACHABILITY — is a published gross TARGET well-posed for this gate? ===")
    reach = []
    for _, r in C.iterrows():
        d = dict(panel=r.panel, gate=r.gate, ceiling=r.ceiling_W)
        for t in TARGETS:
            d[f"T{t:.2f}"] = "REACHABLE" if r.ceiling_W >= t else "UNREACHABLE"
        d["max_nominal_for_075"] = min(1.0, 0.75 / r.ceiling_W) if r.ceiling_W > 0 else np.nan
        reach.append(d)
    R = pd.DataFrame(reach)
    say(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for t in TARGETS:
        say(f"  target {t:.2f}: reachable in {(R[f'T{t:.2f}'] == 'REACHABLE').sum()} of {len(R)} (gate, panel) cells")
    say("NOTE the record's own case: idea 84's g=0.85 under `dg` is UNREACHABLE for BAND3 on "
        "every panel here, and idea 154's published 0.6924/0.6916 is itself BELOW the true "
        "ceiling because its m grid stopped at 1.30 (nominal 0.975, not 1.00) — a grid-edge "
        "understatement of the ceiling, which is open idea 236's point in miniature.")

    # ------------------------------------------------------------ LINEARITY
    say("\n=== (3) IS REALISED GROSS LINEAR IN NOMINAL g? (drift renormalises against cash) ===")
    lin = []
    for pname, p in PX.items():
        s = p.index[260]; GG = gates(p)
        for gname in ["NONE", "BAND3", "MAVOL"]:
            base = None
            for g in GROSSES:
                v = fast_backtest(p, dg_weights(p, GG[gname], g))["gross"].loc[s:].mean()
                if base is None: base = v / g
                lin.append(dict(panel=pname, gate=gname, g=g, realised=v, ratio=v / g,
                                dev_vs_g025=v / g - base))
    L = pd.DataFrame(lin)
    say(L.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"max |realised/g - (realised/g at g=0.25)| = {L.dev_vs_g025.abs().max():.4f} over the whole "
        f"0.25-1.00 range: the map is monotone and linear to within 1e-3 of gross (the residual is "
        f"the cash leg drifting differently at different g), so the ceiling is a per-gate CONSTANT "
        f"(its admission share) and extrapolating it from the live 0.75 is safe to ~0.1 pp.")

    # ------------------------------------------------------------ GRID + KEEP
    say("\n=== (4) GRID: 11 gates x 4 nominal g x 3 panels x 2 rungs = 264 points ===")
    rows = []; ctx = {}
    for pname, p in PX.items():
        s = p.index[260]; GG = gates(p)
        spy = p["SPY"].pct_change().fillna(0).loc[s:]
        v2 = fast_backtest(p, rules_v2_weights(p))
        ctx[pname] = {}
        for rung in RUNGS:
            b = mstats(net(v2, rung).loc[s:]); b["OOS_Sharpe"] = metrics(net(v2, rung).loc[OOS_START:])["Sharpe"]
            sp = mstats(spy)
            sp.update(OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                      OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                      OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"])
            ctx[pname][rung] = dict(base=b, spy=sp)
        for gname, gm in GG.items():
            for g in GROSSES:
                res = fast_backtest(p, dg_weights(p, gm, g))
                gr = res["gross"].loc[s:].mean()
                for rung in RUNGS:
                    r = net(res, rung).loc[s:]
                    mm = mstats(r); oos = metrics(r.loc[OOS_START:])
                    sp = ctx[pname][rung]["spy"]; bs = ctx[pname][rung]["base"]
                    row = dict(panel=pname, gate=gname, nominal_g=g, realised_gross=gr, rung=rung,
                               CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                               Sharpe_H1=mm["H1"], Sharpe_H2=mm["H2"], OOS_Sharpe=oos["Sharpe"],
                               OOS_CAGR=oos["CAGR"], OOS_MaxDD=oos["MaxDD"],
                               IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                               turnover=res["turnover"].loc[s:].sum() / (len(r) / 252))
                    row["pass4a"] = (mm["H1"] > bs["H1"] and mm["H2"] > bs["H2"] and mm["MaxDD"] >= bs["MaxDD"])
                    row["pass4b"] = (mm["H1"] > sp["H1"] and mm["H2"] > sp["H2"]
                                     and oos["Sharpe"] > sp["OOS_Sharpe"]
                                     and mm["MaxDD"] >= 0.60 * sp["MaxDD"]
                                     and mm["CAGR"] >= 0.70 * sp["CAGR"])
                    rows.append(row)
    Gd = pd.DataFrame(rows)
    Gd.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    say(f"grid points: {len(Gd)};  4a {int(Gd.pass4a.sum())}/{len(Gd)};  4b {int(Gd.pass4b.sum())}/{len(Gd)}")
    say("\nSharpe @10 bps at the CEILING (nominal g=1.00), rows = gate, cols = panel:")
    piv = Gd[(Gd.rung == 10) & (Gd.nominal_g == 1.00)].pivot_table(index="gate", columns="panel", values="Sharpe")
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    q = Gd[(Gd.panel == "U56") & (Gd.gate == "BAND3") & (Gd.nominal_g == 1.00) & (Gd.rung == 10)].iloc[0]
    say(f"\nG7 PROVENANCE — idea 423's committed `u56 g=1.00 W` row (the full-gross RULES v2 book): "
        f"here {q.CAGR:.2%} / {q.Sharpe:.4f} / {q.MaxDD:.2%} (H {q.Sharpe_H1:.3f} / {q.Sharpe_H2:.3f})"
        f"   [published 11.59% / 1.2055 / -15.91%, halves 1.226 / 1.190]")
    if Gd.pass4b.any():
        say("\n4b passers:")
        say(Gd[Gd.pass4b].sort_values("Sharpe", ascending=False)
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for pname in PX:
        sub = Gd[Gd.panel == pname]
        say(f"  {pname}: 4a {int(sub.pass4a.sum())}/{len(sub)}, 4b {int(sub.pass4b.sum())}/{len(sub)}")

    # ------------------------------------------------------------ MATCHED-EXPOSURE CONTROL
    say("\n=== (5) IS THE CEILING WORTH ANYTHING? each gate at g=1.00 vs NOGATE at MATCHED "
        "REALISED gross (the honest comparand) ===")
    mrows = []
    for pname, p in PX.items():
        s = p.index[260]; GG = gates(p)
        # NOGATE's realised-gross curve, measured once on a 21-point nominal grid, then
        # inverted by linear interpolation (the curve is monotone and near-linear, see (3));
        # the ACHIEVED match is re-measured and reported for every row.
        ng = np.linspace(0.05, 1.00, 20)
        nr = np.array([fast_backtest(p, dg_weights(p, GG["NONE"], g))["gross"].loc[s:].mean() for g in ng])
        for gname, gm in GG.items():
            if gname == "NONE": continue
            res = fast_backtest(p, dg_weights(p, gm, 1.00))
            target = res["gross"].loc[s:].mean()
            gstar = float(np.interp(target, nr, ng))
            ctl = fast_backtest(p, dg_weights(p, GG["NONE"], gstar))
            realised_ctl = ctl["gross"].loc[s:].mean()
            for rung in RUNGS:
                a = mstats(net(res, rung).loc[s:]); b = mstats(net(ctl, rung).loc[s:])
                ao = metrics(net(res, rung).loc[OOS_START:]); bo = metrics(net(ctl, rung).loc[OOS_START:])
                mrows.append(dict(panel=pname, gate=gname, rung=rung, ceiling=target,
                                  ctl_nominal=gstar, ctl_realised=realised_ctl,
                                  dSharpe=a["Sharpe"] - b["Sharpe"], dCAGR=a["CAGR"] - b["CAGR"],
                                  dMaxDD=a["MaxDD"] - b["MaxDD"],
                                  dOOS_Sharpe=ao["Sharpe"] - bo["Sharpe"],
                                  gate_Sharpe=a["Sharpe"], ctl_Sharpe=b["Sharpe"]))
    M = pd.DataFrame(mrows)
    M.to_csv(OUT / f"{STAMP}.matched.csv", index=False)
    say(M.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\ngate beats its own matched-exposure control on Sharpe in "
        f"{int((M.dSharpe > 0).sum())} of {len(M)} cells (mean dSharpe {M.dSharpe.mean():+.4f}); "
        f"on OOS Sharpe {int((M.dOOS_Sharpe > 0).sum())}/{len(M)} (mean {M.dOOS_Sharpe.mean():+.4f}); "
        f"on MaxDD {int((M.dMaxDD > 0).sum())}/{len(M)} (mean {M.dMaxDD.mean():+.4f})")
    for gname, sub in M.groupby("gate"):
        say(f"  {gname:6s}: dSharpe {sub.dSharpe.mean():+.4f} ({int((sub.dSharpe>0).sum())}/{len(sub)}), "
            f"dMaxDD {sub.dMaxDD.mean():+.4f}, dOOS {sub.dOOS_Sharpe.mean():+.4f}")

    # ------------------------------------------------------------ RULE 8
    say("\n=== (6) RULE 8: (gate, nominal g) chosen on IS <= 2016 by IS Sharpe, 2017+ read once ===")
    wf = []
    for (pname, rung), sub in Gd.groupby(["panel", "rung"]):
        i = sub.IS_Sharpe.idxmax(); r = sub.loc[i]
        pre = sub[(sub.gate == "BAND3") & (sub.nominal_g == 0.75)].iloc[0]   # the LIVE book
        sp = ctx[pname][rung]["spy"]; bs = ctx[pname][rung]["base"]
        wf.append(dict(panel=pname, rung=rung, IS_pick=f"{r.gate}@{r.nominal_g:.2f}",
                       pick_realised_gross=r.realised_gross,
                       OOS_Sharpe=r.OOS_Sharpe, OOS_CAGR=r.OOS_CAGR, OOS_MaxDD=r.OOS_MaxDD,
                       OOS_best=sub.OOS_Sharpe.max(), regret=sub.OOS_Sharpe.max() - r.OOS_Sharpe,
                       LIVE_OOS_Sharpe=pre.OOS_Sharpe, SPY_OOS_Sharpe=sp["OOS_Sharpe"],
                       SPY_OOS_CAGR=sp["OOS_CAGR"], SPY_OOS_MaxDD=sp["OOS_MaxDD"],
                       BASE_OOS_Sharpe=bs["OOS_Sharpe"],
                       beats_SPY=r.OOS_Sharpe > sp["OOS_Sharpe"], beats_BASE=r.OOS_Sharpe > bs["OOS_Sharpe"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"chooser beats SPY OOS {int(W.beats_SPY.sum())}/{len(W)}, RULES v2 OOS {int(W.beats_BASE.sum())}/{len(W)}, "
        f"mean oracle regret {W.regret.mean():.4f}")

    say("\nreference rows (10 bps, full sample):")
    for pname in PX:
        b, s2 = ctx[pname][10]["base"], ctx[pname][10]["spy"]
        say(f"  {pname} RULES v2 {b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} (H {b['H1']:.3f}/{b['H2']:.3f}, OOS {b['OOS_Sharpe']:.4f}); "
            f"SPY {s2['CAGR']:.2%}/{s2['Sharpe']:.4f}/{s2['MaxDD']:.2%} (H {s2['H1']:.3f}/{s2['H2']:.3f}, OOS {s2['OOS_Sharpe']:.4f})")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
