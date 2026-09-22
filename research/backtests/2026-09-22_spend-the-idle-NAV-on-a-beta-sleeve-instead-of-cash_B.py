#!/usr/bin/env python3
"""Idea 2221 (lane B, 2026-09-22): SPEND THE IDLE NAV ON A BETA SLEEVE INSTEAD OF CASH.

The 2026-09-22 CHANGELOG diagnosis (idea 2119) leaves the live RULES v2 band book failing
PROTOCOL 4b on the CAGR floor ALONE (-1.98 pp U56 FULL, -2.83 pp B136 OOS) while its
drawdown margin is +8.18 / +7.99 pp -- 4.5x outside its own weekday scheduling noise -- and
(B) no de-grossed cell clears 4b anywhere on the band x gross grid for exactly that reason.

Every device the record has priced spends that unspent drawdown budget by buying MORE OF THE
SAME BOOK (gross, leverage, re-spread, concentration, VOLTGT), which slides along one Sharpe
ray.  This run tests the untested direction: the book's IDLE NAV -- everything `engine.backtest`
currently pays 0% on, which is `1 - sum(w)` and runs near half of NAV -- is held in a BENCH
sleeve of `phi*SPY + (1-phi)*SHY`, so the book is always fully invested.

  phi = 0.00 : a pure T-bill-sweep accounting fix (idle NAV in SHY).  No beta added.
  phi = 1.00 : idle NAV fully in market beta.

TUNED (2, exactly): phi in {0.00,0.25,0.50,0.75,1.00} x band c in {0.00,0.02,0.03,0.05,0.08}.
Gross is FIXED at the live 0.75 and is NOT a third dial.  ALL 25 grid points are reported.
PUBLISHED-NOT-TUNED: panel {U56,B136} x offset d in {0..4} (a NOISE MEASUREMENT; the reported
book is always d=0) x cost {0,10,25,50} bps (headline 10) x window {FULL,IS,OOS}.
Control arm NOSLEEVE per band = the live book form (idle NAV in 0% cash).

Weekly, long-only, no leverage (total weight is exactly 1.0), t+1 execution, 10 bps headline.
Rule 8: (phi,c) chosen on 2009-2016 IS Sharpe alone; 2017-2026 read ONCE.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

PHIS  = [0.00, 0.25, 0.50, 0.75, 1.00]
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08]
OFFSETS = [0, 1, 2, 3, 4]
COSTS = [0.0, 10.0, 25.0, 50.0]
GROSS = 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
OUT = ROOT / "research" / "backtests"

# ---------------------------------------------------------------- book construction
def core_weights(px, c, gross=GROSS):
    """RULES v2 clause 2-4 exactly: every IN name at gross/N, N = names priced that day,
    gated-out weight to cash.  At c=0.03, gross=0.75 this IS baseline.rules_v2_weights."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, c), 0.0)

def sleeved_weights(px, c, phi, gross=GROSS):
    """Core band book + the idle NAV (1 - sum of core weights) held in phi*SPY + (1-phi)*SHY.
    SPY and SHY are also gated universe names, so the sleeve ADDS to any core holding in them.
    Total weight is exactly 1.0 -> fully invested, long-only, no leverage."""
    w = core_weights(px, c, gross)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    out = w.copy()
    out["SPY"] = out["SPY"] + idle * phi
    out["SHY"] = out["SHY"] + idle * (1.0 - phi)
    return out

# ---------------------------------------------------------------- offset-aware runner
def offset_mask(idx, d):
    """Weekly rebalance shifted d trading days EARLIER inside its own week.  d=0 is the last
    trading day of the week (== engine.rebalance_mask(idx,'W')).  A week with <= d trading days
    cannot carry the offset and falls back to its earliest day -- those weeks are CLIPPED and
    counted, never silently dropped."""
    key = pd.Series(idx.to_period("W"), index=idx)
    mask = pd.Series(False, index=idx); clipped = 0
    for _, grp in key.groupby(key, sort=False):
        days = grp.index
        if len(days) > d: pick = days[-(1 + d)]
        else: pick = days[0]; clipped += 1
        mask.loc[pick] = True
    return mask, clipped

def run(px, W, mask):
    """engine.backtest semantics (decide at t, apply at t+1, drift between rebalances),
    numpy-fast, with an arbitrary rebalance mask.  Returns GROSS-of-cost returns + turnover,
    so any cost rung is an exact affine re-read: r(c) = r_gross - turnover*c/1e4."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    m = mask.shift(1, fill_value=False).values
    n = len(px); cur = np.zeros(px.shape[1]); held = np.zeros_like(rets); to = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    gr = pd.Series((held * rets).sum(axis=1), index=px.index)
    return gr, pd.Series(to, index=px.index)

def m6(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

# ---------------------------------------------------------------- KEEP paths
def keep4a(a, b):
    return bool(a["H1"] > b["H1"] and a["H2"] > b["H2"] and a["MaxDD"] >= b["MaxDD"])

def legs4b(a, s):
    return dict(H1=bool(a["H1"] > s["H1"]), H2=bool(a["H2"] > s["H2"]),
                DD=bool(a["MaxDD"] >= 0.60 * s["MaxDD"]), CAGR=bool(a["CAGR"] >= 0.70 * s["CAGR"]))

def keep4b(a, s):
    return all(legs4b(a, s).values())

# ---------------------------------------------------------------- main
def windows(idx):
    start = idx[260]
    return {"FULL": (start, idx[-1]),
            "IS":   (start, pd.Timestamp(IS_END)),
            "OOS":  (pd.Timestamp(OOS_START), idx[-1])}

def main():
    rows = []; gates = {}
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}

    for pname, px in panels.items():
        idx = px.index
        wins = windows(idx)
        print(f"\n=== panel {pname}: {px.shape[1]} names, {idx[0].date()}..{idx[-1].date()} ===")

        # ---- gates -------------------------------------------------------
        m0, clip0 = offset_mask(idx, 0)
        gates[f"G2_{pname}_maskdiff"] = int((m0.values != rebalance_mask(idx, "W").values).sum())
        w_live = rules_v2_weights(px, 0.03, GROSS)
        gates[f"G3_{pname}_core_vs_rulesv2"] = float((core_weights(px, 0.03) - w_live).abs().max().max())
        gr, to = run(px, w_live, m0)
        eng = engine_backtest(px, w_live, cost_bps=10.0, freq="W")["returns"]
        gates[f"G1_{pname}_runner_vs_engine"] = float((gr - to * 10.0 / 1e4 - eng).abs().max())
        eng25 = engine_backtest(px, w_live, cost_bps=25.0, freq="W")["returns"]
        gates[f"G4_{pname}_cost_reconstruction"] = float((gr - to * 25.0 / 1e4 - eng25).abs().max())
        gates[f"G5_{pname}_clipped_weeks_d4"] = offset_mask(idx, 4)[1]
        gates[f"G5_{pname}_clipped_weeks_d2"] = offset_mask(idx, 2)[1]

        # ---- benchmarks ---------------------------------------------------
        spy = px["SPY"].pct_change().fillna(0.0)
        v1 = engine_backtest(px, rules_v1_weights(px), cost_bps=10.0, freq="W")["returns"]
        bench = {}
        for wn, (a, b) in wins.items():
            bench[("SPY", wn)] = m6(spy.loc[a:b])
            bench[("RULESv2", wn)] = m6(eng.loc[a:b])
            bench[("RULESv1", wn)] = m6(v1.loc[a:b])
        for k, v in bench.items():
            rows.append(dict(panel=pname, arm=k[0], phi=np.nan, band=np.nan, offset=0,
                             cost=10.0, window=k[1], **v, keep4a=False, keep4b=False,
                             **{f"leg_{x}": False for x in ("H1", "H2", "DD", "CAGR")}))

        # ---- the ladder ----------------------------------------------------
        for d in OFFSETS:
            mk, _ = offset_mask(idx, d)
            arms = [("NOSLEEVE", np.nan, c, core_weights(px, c)) for c in BANDS]
            arms += [("SLEEVE", phi, c, sleeved_weights(px, c, phi)) for phi in PHIS for c in BANDS]
            for arm, phi, c, W in arms:
                g, t_ = run(px, W, mk)
                for cost in COSTS:
                    r = g - t_ * cost / 1e4
                    for wn, (a, b) in wins.items():
                        mm = m6(r.loc[a:b]); s = bench[("SPY", wn)]; bl = bench[("RULESv2", wn)]
                        lg = legs4b(mm, s)
                        rows.append(dict(panel=pname, arm=arm, phi=phi, band=c, offset=d,
                                         cost=cost, window=wn, **mm,
                                         keep4a=keep4a(mm, bl), keep4b=all(lg.values()),
                                         **{f"leg_{k}": v for k, v in lg.items()}))
            print(f"  offset d={d} done ({len(rows)} rows)")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "2026-09-22_spend-the-idle-NAV-on-a-beta-sleeve-instead-of-cash_B.csv.gz",
              index=False, compression="gzip")
    print("\n=== GATES ===")
    for k, v in gates.items(): print(f"  {k}: {v}")
    print(f"\n{len(df)} published rows")
    return df, gates

# ---------------------------------------------------------------- analysis
def cellname(r):
    return f"phi={r.phi:.2f}|c={r.band:.2f}" if r.arm == "SLEEVE" else f"NOSLV|c={r.band:.2f}"

def analysis(df):
    L = df[df.arm.isin(["SLEEVE", "NOSLEEVE"])].copy(); L["cell"] = L.apply(cellname, axis=1)
    h = L[(L.offset == 0) & (L.cost == 10.0)]
    print("\n########## HEADLINE (offset d=0, 10 bps) ##########")
    for pan in ["U56", "B136"]:
        for wn in ["FULL", "IS", "OOS"]:
            x = h[(h.panel == pan) & (h.window == wn)]
            for v in ("CAGR", "Sharpe", "MaxDD"):
                t = x[x.arm == "SLEEVE"].pivot_table(index="band", columns="phi", values=v)
                t["NOSLEEVE"] = x[x.arm == "NOSLEEVE"].set_index("band")[v]
                print(f"\n-- {v} {pan} {wn} (cols = phi; NOSLEEVE = live 0%-cash form) --")
                print((t * 100 if v != "Sharpe" else t).round(3).to_string())
            print(f"   4a passers: {sorted(x[x.keep4a].cell)}")
            print(f"   4b passers: {sorted(x[x.keep4b].cell)}")
            f = x[~x.keep4b]
            print(f"   binding legs among fails: H1 {(~f.leg_H1).sum()} H2 {(~f.leg_H2).sum()} "
                  f"DD {(~f.leg_DD).sum()} CAGR {(~f.leg_CAGR).sum()}")

    print("\n########## RULE 8 (parameters chosen on 2009-2016 only; 2017-2026 read once) ##########")
    for pan in ["U56", "B136"]:
        g = h[h.panel == pan]
        for label, pool in (("C1 habitual: argmax IS Sharpe", g[g.window == "IS"]),
                            ("C2 legal IS-only: argmax IS Sharpe among IS-4b passers",
                             g[(g.window == "IS") & g.keep4b])):
            if len(pool) == 0:
                print(f"{pan} {label}: NO IS PASSER"); continue
            pick = pool.sort_values("Sharpe", ascending=False).iloc[0].cell
            o = g[(g.window == "OOS") & (g.cell == pick)].iloc[0]
            fu = g[(g.window == "FULL") & (g.cell == pick)].iloc[0]
            off = L[(L.panel == pan) & (L.cell == pick) & (L.window == "OOS") & (L.cost == 10.0)].sort_values("offset")
            cst = L[(L.panel == pan) & (L.cell == pick) & (L.window == "OOS") & (L.offset == 0)].sort_values("cost")
            print(f"{pan} {label} -> {pick}")
            print(f"    OOS  {o.CAGR:.2%} / {o.Sharpe:.4f} / {o.MaxDD:.2%}  4b={o.keep4b} 4a={o.keep4a}"
                  f"  legs H1={o.leg_H1} H2={o.leg_H2} DD={o.leg_DD} CAGR={o.leg_CAGR}")
            print(f"    FULL {fu.CAGR:.2%} / {fu.Sharpe:.4f} / {fu.MaxDD:.2%} 4b={fu.keep4b}")
            print(f"    OOS 4b at offsets 0..4 = {list(off.keep4b.astype(int))}; at 0/10/25/50 bps = {list(cst.keep4b.astype(int))}")

    print("\n########## MONOTONICITY IN phi (mean over the 5 bands) ##########")
    for pan in ["U56", "B136"]:
        for wn in ["IS", "OOS"]:
            g = h[(h.panel == pan) & (h.window == wn) & (h.arm == "SLEEVE")].groupby("phi")[["Sharpe", "CAGR", "MaxDD"]].mean()
            print(f"{pan} {wn}: IS-objective Sharpe {[f'{v:.3f}' for v in g.Sharpe]} | "
                  f"deciding leg CAGR {[f'{v:.2%}' for v in g.CAGR]} | MaxDD {[f'{v:.2%}' for v in g.MaxDD]}")

    print("\n########## ROBUSTNESS of the phi=0 T-BILL SWEEP on the LIVE band (4a, offset x cost) ##########")
    for pan in ["U56", "B136"]:
        x = L[(L.panel == pan) & (L.cell == "phi=0.00|c=0.03")]
        print(f"-- {pan} 4a --"); print(x.pivot_table(index=["window", "cost"], columns="offset", values="keep4a").astype(int).to_string())

    print("\n########## OFFSET SPREAD of the binding margins (the 914/2119 clause) ##########")
    for pan, cell in (("U56", "phi=0.25|c=0.03"), ("U56", "phi=0.25|c=0.02"),
                      ("B136", "phi=0.25|c=0.08"), ("U56", "phi=0.00|c=0.03"), ("B136", "phi=0.00|c=0.03")):
        for wn in ["FULL", "OOS"]:
            x = L[(L.panel == pan) & (L.cell == cell) & (L.window == wn) & (L.cost == 10.0)].set_index("offset").sort_index()
            s = df[(df.panel == pan) & (df.arm == "SPY") & (df.window == wn)].iloc[0]
            dd = (x.MaxDD - 0.60 * s.MaxDD) * 100; cg = (x.CAGR - 0.70 * s.CAGR) * 100
            print(f"{pan} {cell} {wn}: 4b at d=0..4 {list(x.keep4b.astype(int))} | "
                  f"DD margin {dd.loc[0]:+.2f} pp vs spread {dd.max()-dd.min():.2f} (clip-free d<=2: {dd.loc[:2].max()-dd.loc[:2].min():.2f}) | "
                  f"CAGR margin {cg.loc[0]:+.2f} pp vs spread {cg.max()-cg.min():.2f} (clip-free: {cg.loc[:2].max()-cg.loc[:2].min():.2f})")

if __name__ == "__main__":
    df, gates = main()
    analysis(df)
