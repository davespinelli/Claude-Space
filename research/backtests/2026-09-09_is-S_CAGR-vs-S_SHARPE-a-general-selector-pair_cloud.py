#!/usr/bin/env python3
"""Idea 270 — is S_CAGR vs S_SHARPE a general selector pair?

Idea 259 found the two in-sample selectors (pick the arm with the best first-half Sharpe
vs the best first-half CAGR) choose a DIFFERENT arm in 3 of 4 panels on the `n` dial,
worth +2.53 pp/yr of OOS CAGR for -0.0254 of OOS Sharpe.  This runs the identical
selector pair over the record's OTHER swept dials — band, gross, cadence, vol cap,
eligibility quantile — on three panels and at two cost rungs, and asks whether the
n-dial result is a dial fact or a general one.

Rule 8 throughout: both selectors see the FIRST half only; every number reported is on
the untouched SECOND half.  Comparands on the same OOS window: the live RULES v2 book,
RULES v1, SPY, and the do-nothing control for each dial (the record's EWALL: every priced
name equal-weighted at the dial's gross, no dial at all).

Two tuned parameters per arm: the dial value, plus the one companion constant the dial's
book form needs (stated per dial below).  ALL grid points are reported in .arms.csv.
Costs 10 bps headline, 25 bps rung reported beside it; weekly unless the dial is cadence;
weights decided at t applied at t+1 (engine).  No network.
SURVIVORSHIP: broad136 and the sub-$2B panel are current constituents only.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, band_state  # noqa
from engine import backtest, metrics  # noqa

STAMP = "2026-09-09_is-S_CAGR-vs-S_SHARPE-a-general-selector-pair_cloud"
OUT = ROOT / "research" / "backtests"
GROSS = 0.75            # the live book's gross, held fixed except on the gross dial
BAND = 0.03             # the live band, held fixed except on the band dial
COSTS = [10, 25]

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)

# ---------------------------------------------------------------- book forms
def _ew(px, mask, gross):
    e = mask.astype(float).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def w_topn(px, n, gross=GROSS):
    """Composite-ranked top n above the 200d MA, equal weight (companion const: gross)."""
    s, above, vol20 = score(px)
    r = s.where(above).rank(axis=1, ascending=False)
    return _ew(px, r <= n, gross)

def w_band(px, band, gross=GROSS):
    return rules_v2_weights(px, band=band, gross=gross)

def w_gross(px, gross, band=BAND):
    return rules_v2_weights(px, band=band, gross=gross)

def w_volcap(px, cap, gross=GROSS):
    """v1 eligibility legs (above MA200 AND vol20 < cap), equal weight (companion: gross)."""
    s, above, vol20 = score(px)
    return _ew(px, above & (vol20 < cap), gross)

def w_quantile(px, x, gross=GROSS):
    """Top x fraction (by composite) of the names above the MA200, equal weight."""
    s, above, vol20 = score(px)
    el = s.where(above)
    r = el.rank(axis=1, ascending=False, pct=True)
    return _ew(px, r <= x, gross)

def w_ewall(px, gross=GROSS):
    return _ew(px, px.notna(), gross)

DIALS = {
    "n":        (w_topn,     [5, 10, 20, 30, 50],                 "W"),
    "band":     (w_band,     [0.00, 0.01, 0.03, 0.05, 0.08, 0.12], "W"),
    "gross":    (w_gross,    [0.25, 0.50, 0.75, 1.00],            "W"),
    "volcap":   (w_volcap,   [0.30, 0.45, 0.60, 0.90, 9.99],      "W"),
    "quantile": (w_quantile, [0.10, 0.25, 0.50, 0.75, 1.00],      "W"),
    "cadence":  (None,       ["D", "W", "M", "Q"],                None),
}

# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]

def panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

# ---------------------------------------------------------------- helpers
def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]

def mrow(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]

def main():
    t0 = time.time(); arms, cells = [], []
    say(f"# {STAMP}\n")
    for pname, px in panels().items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        say(f"## Panel {pname}: {px.shape[1]-1} names + SPY, {px.index[0].date()}..{px.index[-1].date()}")
        for cost in COSTS:
            base = backtest(px, rules_v2_weights(px), cost_bps=cost, freq="W")["returns"].loc[start:]
            v1 = backtest(px, rules_v1_weights(px), cost_bps=cost, freq="W")["returns"].loc[start:]
            ctl = backtest(px, w_ewall(px), cost_bps=cost, freq="W")["returns"].loc[start:]
            for dname, (fn, vals, freq) in DIALS.items():
                recs = []
                for v in vals:
                    if dname == "cadence":
                        w, f = rules_v2_weights(px, band=BAND, gross=GROSS), v
                    else:
                        w, f = fn(px, v), freq
                    r = backtest(px, w, cost_bps=cost, freq=f)["returns"].loc[start:]
                    is_r, oos_r = halves(r)
                    c_is, s_is, d_is = mrow(is_r); c_o, s_o, d_o = mrow(oos_r)
                    cf, sf, df = mrow(r)
                    recs.append(dict(panel=pname, cost=cost, dial=dname, arm=v,
                                     IS_CAGR=c_is, IS_Sharpe=s_is, IS_MaxDD=d_is,
                                     OOS_CAGR=c_o, OOS_Sharpe=s_o, OOS_MaxDD=d_o,
                                     FULL_CAGR=cf, FULL_Sharpe=sf, FULL_MaxDD=df))
                A = pd.DataFrame(recs)
                # KEEP paths for every arm, judged the protocol way
                mb, ms = metrics(base), metrics(spy)
                b_is, b_oos = halves(base); s_isr, s_oosr = halves(spy)
                A["pass4a"] = ((A.IS_Sharpe > metrics(b_is)["Sharpe"]) & (A.OOS_Sharpe > metrics(b_oos)["Sharpe"])
                               & (A.FULL_MaxDD >= mb["MaxDD"]))
                A["pass4b"] = ((A.IS_Sharpe > metrics(s_isr)["Sharpe"]) & (A.OOS_Sharpe > metrics(s_oosr)["Sharpe"])
                               & (A.FULL_MaxDD >= 0.6 * ms["MaxDD"]) & (A.FULL_CAGR >= 0.7 * ms["CAGR"]))
                arms.append(A)
                # ---- the two IS selectors (first half only)
                i_s = int(A.IS_Sharpe.values.argmax()); i_c = int(A.IS_CAGR.values.argmax())
                i_oracle_s = int(A.OOS_Sharpe.values.argmax()); i_oracle_c = int(A.OOS_CAGR.values.argmax())
                cells.append(dict(panel=pname, cost=cost, dial=dname, n_arms=len(A),
                                  arm_S_SHARPE=A.arm.iloc[i_s], arm_S_CAGR=A.arm.iloc[i_c],
                                  disagree=int(i_s != i_c),
                                  S_SHARPE_OOS_Sharpe=A.OOS_Sharpe.iloc[i_s], S_SHARPE_OOS_CAGR=A.OOS_CAGR.iloc[i_s],
                                  S_SHARPE_OOS_MaxDD=A.OOS_MaxDD.iloc[i_s],
                                  S_CAGR_OOS_Sharpe=A.OOS_Sharpe.iloc[i_c], S_CAGR_OOS_CAGR=A.OOS_CAGR.iloc[i_c],
                                  S_CAGR_OOS_MaxDD=A.OOS_MaxDD.iloc[i_c],
                                  d_OOS_Sharpe=A.OOS_Sharpe.iloc[i_c] - A.OOS_Sharpe.iloc[i_s],
                                  d_OOS_CAGR=A.OOS_CAGR.iloc[i_c] - A.OOS_CAGR.iloc[i_s],
                                  oracle_OOS_Sharpe=A.OOS_Sharpe.iloc[i_oracle_s],
                                  oracle_OOS_CAGR=A.OOS_CAGR.iloc[i_oracle_c],
                                  mean_arm_OOS_Sharpe=A.OOS_Sharpe.mean(), mean_arm_OOS_CAGR=A.OOS_CAGR.mean(),
                                  ctl_OOS_Sharpe=metrics(halves(ctl)[1])["Sharpe"], ctl_OOS_CAGR=metrics(halves(ctl)[1])["CAGR"],
                                  base_OOS_Sharpe=metrics(b_oos)["Sharpe"], base_OOS_CAGR=metrics(b_oos)["CAGR"],
                                  v1_OOS_Sharpe=metrics(halves(v1)[1])["Sharpe"],
                                  spy_OOS_Sharpe=metrics(s_oosr)["Sharpe"], spy_OOS_CAGR=metrics(s_oosr)["CAGR"],
                                  pass4a_arms=int(A.pass4a.sum()), pass4b_arms=int(A.pass4b.sum()),
                                  S_SHARPE_4b=bool(A.pass4b.iloc[i_s]), S_CAGR_4b=bool(A.pass4b.iloc[i_c]),
                                  S_SHARPE_4a=bool(A.pass4a.iloc[i_s]), S_CAGR_4a=bool(A.pass4a.iloc[i_c])))
        say(f"   ... {pname} done at {time.time()-t0:.0f}s")

    ARMS = pd.concat(arms, ignore_index=True); C = pd.DataFrame(cells)
    ARMS.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    C.to_csv(OUT / f"{STAMP}.cells.csv", index=False)

    def tstat(x):
        x = np.asarray(x, float)
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 1 and x.std(ddof=1) > 0 else np.nan

    say(f"\n## Cells: {len(C)} (3 panels x 6 dials x 2 cost rungs), arms {len(ARMS)}")
    say("### Disagreement rate (S_SHARPE vs S_CAGR pick a different arm)")
    say(f"overall {C.disagree.sum()}/{len(C)} = {C.disagree.mean():.1%}   "
        f"@10bps {C[C.cost==10].disagree.sum()}/{len(C[C.cost==10])}   @25bps {C[C.cost==25].disagree.sum()}/{len(C[C.cost==25])}")
    say(C.groupby("dial").disagree.agg(["sum", "count"]).to_string())
    say(C.groupby("panel").disagree.agg(["sum", "count"]).to_string())

    D = C[C.disagree == 1]
    say(f"\n### The trade, on cells where they disagree (n={len(D)})")
    for label, sub in (("all cells", C), ("disagreeing cells", D)):
        if not len(sub): continue
        say(f"{label:20s} d_OOS_CAGR {sub.d_OOS_CAGR.mean()*100:+.2f} pp/yr (t {tstat(sub.d_OOS_CAGR):+.2f}, "
            f"{int((sub.d_OOS_CAGR>0).sum())}/{len(sub)} positive)   "
            f"d_OOS_Sharpe {sub.d_OOS_Sharpe.mean():+.4f} (t {tstat(sub.d_OOS_Sharpe):+.2f}, "
            f"{int((sub.d_OOS_Sharpe>0).sum())}/{len(sub)} positive)")
    say("idea 259's n-dial reading was +2.53 pp/yr OOS CAGR for -0.0254 OOS Sharpe")
    nd = C[C.dial == "n"]
    say(f"n dial here: disagree {nd.disagree.sum()}/{len(nd)}, d_OOS_CAGR {nd.d_OOS_CAGR.mean()*100:+.2f} pp/yr, "
        f"d_OOS_Sharpe {nd.d_OOS_Sharpe.mean():+.4f}")
    say("\nper dial (mean over panels and cost rungs):")
    say(C.groupby("dial")[["disagree", "d_OOS_CAGR", "d_OOS_Sharpe"]].mean().to_string(float_format=lambda x: f"{x:+.4f}"))
    say("per panel:")
    say(C.groupby("panel")[["disagree", "d_OOS_CAGR", "d_OOS_Sharpe"]].mean().to_string(float_format=lambda x: f"{x:+.4f}"))

    say("\n### Do the selectors beat doing nothing? (OOS, median over cells)")
    cmp = pd.DataFrame({
        "S_SHARPE": [C.S_SHARPE_OOS_Sharpe.median(), C.S_SHARPE_OOS_CAGR.median()],
        "S_CAGR": [C.S_CAGR_OOS_Sharpe.median(), C.S_CAGR_OOS_CAGR.median()],
        "mean arm (no selection)": [C.mean_arm_OOS_Sharpe.median(), C.mean_arm_OOS_CAGR.median()],
        "EWALL control": [C.ctl_OOS_Sharpe.median(), C.ctl_OOS_CAGR.median()],
        "RULES v2 (live)": [C.base_OOS_Sharpe.median(), C.base_OOS_CAGR.median()],
        "SPY": [C.spy_OOS_Sharpe.median(), C.spy_OOS_CAGR.median()],
        "oracle (OOS argmax)": [C.oracle_OOS_Sharpe.median(), C.oracle_OOS_CAGR.median()],
    }, index=["OOS_Sharpe", "OOS_CAGR"])
    say(cmp.to_string(float_format=lambda x: f"{x:.4f}"))
    for nm, col in (("S_SHARPE", "S_SHARPE_OOS_Sharpe"), ("S_CAGR", "S_CAGR_OOS_Sharpe")):
        say(f"{nm}: beats mean-arm OOS Sharpe in {int((C[col] > C.mean_arm_OOS_Sharpe).sum())}/{len(C)} cells, "
            f"beats RULES v2 in {int((C[col] > C.base_OOS_Sharpe).sum())}/{len(C)}, "
            f"beats SPY in {int((C[col] > C.spy_OOS_Sharpe).sum())}/{len(C)}")

    say(f"\n### KEEP paths over all {len(ARMS)} arms: 4a {int(ARMS.pass4a.sum())}, 4b {int(ARMS.pass4b.sum())}")
    say(ARMS.groupby(["panel", "cost"])[["pass4a", "pass4b"]].sum().to_string())
    say(f"selected arms: S_SHARPE 4b {int(C.S_SHARPE_4b.sum())}/{len(C)}, "
        f"S_CAGR 4b {int(C.S_CAGR_4b.sum())}/{len(C)}; 4a {int(C.S_SHARPE_4a.sum())}/{int(C.S_CAGR_4a.sum())}")
    if ARMS.pass4b.any():
        say("\n4b-passing arms (all):")
        say(ARMS[ARMS.pass4b][["panel", "cost", "dial", "arm", "FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD",
                               "IS_Sharpe", "OOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nruntime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()
