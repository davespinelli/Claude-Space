#!/usr/bin/env python3
"""Idea 2213 (lane cloud, 2026-09-22): CREDIT THE IDLE NAV AT A T-BILL PROXY ON EVERY
COMMITTED BAND-BOOK CAGR.

`engine.backtest` pays exactly 0% on the uninvested residual `1 - sum(w)`.  The live RULES v2
band book leaves roughly half of NAV there (gross 0.75 x breadth), while its PROTOCOL 4b
comparand SPY is fully invested.  Idea 2119 then killed the whole band x gross ladder on the
CAGR floor ALONE (-1.98 pp U56 FULL / -2.83 pp B136 OOS at the live cell; no de-grossed cell
g <= 0.85 clears 4b at any band on either panel) while the DD margin ran +8.18 pp.  If the
idle NAV earns a T-bill, some unknown part of that shortfall is an accounting convention
rather than a book fact.  This run measures that part, on the WHOLE 2119 ladder.

ARMS (three, one control + two readings of the same sleeved book):
  CASH      the committed form: idle NAV at 0%.  Reproduces 2119 exactly (gate G3).
  SHYFREE   idle NAV swept into SHY, and the sweep itself is FREE (cost charged only on the
            turnover of the non-SHY columns).  This is the pure ACCOUNTING-CONVENTION read.
  SHYTRADED the same book with the sweep's own turnover charged at the run's cost rung.  This
            is the read an actual account would get.

TUNED (2, exactly): band c in {0.00,0.02,0.03,0.05,0.08} x gross g in {0.50,0.60,0.75,0.85,1.00}
-- the 2119 ladder, unchanged.  ALL 25 grid points are reported, on both panels, in all three
windows, at all four cost rungs, for all three arms.
PUBLISHED-NOT-TUNED: panel {U56,B136} x cost {0,10,25,50} bps (headline 10) x window
{FULL,IS,OOS} x weekly offset d in {0,1,2} (a NOISE MEASUREMENT; the reported book is d=0).

Weekly cadence, long-only, no leverage (total weight <= 1.0), t+1 execution, 10 bps headline.
Rule 8: (band, gross) chosen on 2009-2016 IS Sharpe alone, inside each arm; 2017-2026 read ONCE.
Both KEEP paths evaluated on every cell: 4a vs live RULES v2, 4b vs SPY.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

BANDS = [0.00, 0.02, 0.03, 0.05, 0.08]
GROSSES = [0.50, 0.60, 0.75, 0.85, 1.00]
OFFSETS = [0, 1, 2]
COSTS = [0.0, 10.0, 25.0, 50.0]
SLEEVE = "SHY"                       # the T-bill proxy; a member of BOTH panels
IS_END, OOS_START = "2016-12-31", "2017-01-01"
OUT = ROOT / "research" / "backtests"
STEM = "2026-09-22_credit-idle-nav-at-a-tbill-proxy-band-gross-ladder_cloud"


# ---------------------------------------------------------------- book construction
def core_weights(px, c, g):
    """RULES v2 clause 2-4: every name inside the 200d +/-c band at g/N of NAV, N = names
    priced that day; gated-out weight to CASH (de-gross, never re-spread).  At c=0.03, g=0.75
    this is byte-identical to baseline.rules_v2_weights (gate G3)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, c), 0.0)


def sleeved_weights(px, c, g):
    """Core band book + the idle NAV (1 - sum of core weights) held in SHY.  SHY is itself a
    gated universe name, so the sweep ADDS to any core holding in it.  Total weight is exactly
    1.0 on every day the panel prices anything -> fully invested, long-only, no leverage."""
    w = core_weights(px, c, g)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    out = w.copy()
    out[SLEEVE] = out[SLEEVE] + idle
    return out


# ---------------------------------------------------------------- offset-aware runner
def offset_mask(idx, d):
    """Weekly rebalance shifted d trading days EARLIER inside its own week.  d=0 is the last
    trading day of the week (== engine.rebalance_mask(idx,'W'), gate G2).  A week with <= d
    trading days falls back to its earliest day; those weeks are CLIPPED and counted."""
    key = pd.Series(idx.to_period("W"), index=idx)
    mask = pd.Series(False, index=idx); clipped = 0
    for _, grp in key.groupby(key, sort=False):
        days = grp.index
        if len(days) > d:
            pick = days[-(1 + d)]
        else:
            pick = days[0]; clipped += 1
        mask.loc[pick] = True
    return mask, clipped


def run(px, W, mask, sleeve_col):
    """engine.backtest semantics (decide at t, apply at t+1, drift between rebalances),
    numpy-fast, with an arbitrary rebalance mask.  Returns GROSS-of-cost returns plus TWO
    turnover series -- all columns, and all columns EXCEPT the sleeve -- and the daily idle
    (uninvested) share, so every cost rung and both cost conventions are exact affine
    re-reads: r(c) = r_gross - turnover * c / 1e4."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    m = mask.shift(1, fill_value=False).values
    j = px.columns.get_loc(sleeve_col)
    n, k = rets.shape
    cur = np.zeros(k); held = np.zeros_like(rets)
    to_all = np.zeros(n); to_ex = np.zeros(n); idle = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            d = np.abs(new - cur)
            to_all[i] = d.sum(); to_ex[i] = d.sum() - d[j]
            cur = new.copy()
        held[i] = cur
        idle[i] = 1.0 - cur.sum()
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    gr = pd.Series((held * rets).sum(axis=1), index=px.index)
    return (gr, pd.Series(to_all, index=px.index), pd.Series(to_ex, index=px.index),
            pd.Series(idle, index=px.index))


def m6(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# ---------------------------------------------------------------- KEEP paths
def keep4a(a, b):
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves AND MaxDD no worse than the live rules."""
    return bool(a["H1"] > b["H1"] and a["H2"] > b["H2"] and a["MaxDD"] >= b["MaxDD"])


def legs4b(a, s):
    """PROTOCOL 4b legs against SPY in the SAME window."""
    return dict(H1=bool(a["H1"] > s["H1"]), H2=bool(a["H2"] > s["H2"]),
                DD=bool(a["MaxDD"] >= 0.60 * s["MaxDD"]), CAGR=bool(a["CAGR"] >= 0.70 * s["CAGR"]))


def windows(idx):
    start = idx[260]                                     # skip the 200d warm-up
    return {"FULL": (start, idx[-1]),
            "IS": (start, pd.Timestamp(IS_END)),
            "OOS": (pd.Timestamp(OOS_START), idx[-1])}


# ---------------------------------------------------------------- main
def main():
    rows = []; gates = {}
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}

    for pname, px in panels.items():
        idx = px.index; wins = windows(idx)
        print(f"\n=== panel {pname}: {px.shape[1]} names, {idx[0].date()}..{idx[-1].date()} ===")

        m0, clip0 = offset_mask(idx, 0)
        gates[f"G1_{pname}_maskdiff_vs_engine_W"] = int((m0.values != rebalance_mask(idx, "W").values).sum())
        w_live = rules_v2_weights(px, 0.03, 0.75)
        gates[f"G2_{pname}_core_vs_rules_v2"] = float((core_weights(px, 0.03, 0.75) - w_live).abs().max().max())
        gr, ta, te, idle = run(px, w_live, m0, SLEEVE)
        eng10 = engine_backtest(px, w_live, cost_bps=10.0, freq="W")["returns"]
        eng25 = engine_backtest(px, w_live, cost_bps=25.0, freq="W")["returns"]
        gates[f"G3_{pname}_runner_vs_engine_10bps"] = float((gr - ta * 10.0 / 1e4 - eng10).abs().max())
        gates[f"G3_{pname}_runner_vs_engine_25bps"] = float((gr - ta * 25.0 / 1e4 - eng25).abs().max())
        gates[f"G4_{pname}_clipped_weeks_d2"] = offset_mask(idx, 2)[1]
        # G5: with SHY's own return zeroed, the sleeved book must collapse onto the CASH book.
        pz = px.copy(); pz[SLEEVE] = 1.0
        gz_core = run(pz, core_weights(px, 0.03, 0.75), m0, SLEEVE)[0]
        gz_slv = run(pz, sleeved_weights(px, 0.03, 0.75), m0, SLEEVE)[0]
        gates[f"G5_{pname}_flat_sleeve_collapse"] = float((gz_core - gz_slv).abs().max())

        spy = px["SPY"].pct_change().fillna(0.0)
        shy = px[SLEEVE].pct_change().fillna(0.0)
        bench = {}
        for wn, (a, b) in wins.items():
            bench[("SPY", wn)] = m6(spy.loc[a:b])
            bench[("RULESv2", wn)] = m6(eng10.loc[a:b])
            bench[("SHY", wn)] = m6(shy.loc[a:b])
        for (nm, wn), v in bench.items():
            rows.append(dict(panel=pname, arm=nm, band=np.nan, gross=np.nan, offset=0, cost=10.0,
                             window=wn, idle=np.nan, turn=np.nan, **v, keep4a=False, keep4b=False,
                             **{f"leg_{x}": False for x in ("H1", "H2", "DD", "CAGR")}))

        for d in OFFSETS:
            mk, _ = offset_mask(idx, d)
            for c in BANDS:
                for g in GROSSES:
                    gc, tac, _, idlec = run(px, core_weights(px, c, g), mk, SLEEVE)
                    gs, tas, tes, idles = run(px, sleeved_weights(px, c, g), mk, SLEEVE)
                    arms = {"CASH": (gc, tac, idlec), "SHYFREE": (gs, tes, idles),
                            "SHYTRADED": (gs, tas, idles)}
                    for arm, (gg, tt, ii) in arms.items():
                        for cost in COSTS:
                            r = gg - tt * cost / 1e4
                            for wn, (a, b) in wins.items():
                                mm = m6(r.loc[a:b]); s = bench[("SPY", wn)]; bl = bench[("RULESv2", wn)]
                                lg = legs4b(mm, s)
                                rows.append(dict(panel=pname, arm=arm, band=c, gross=g, offset=d,
                                                 cost=cost, window=wn,
                                                 idle=float(ii.loc[a:b].mean()),
                                                 turn=float(tt.loc[a:b].sum() / (len(tt.loc[a:b]) / 252)),
                                                 **mm, keep4a=keep4a(mm, bl), keep4b=all(lg.values()),
                                                 **{f"leg_{k}": v for k, v in lg.items()}))
            print(f"  offset d={d} done ({len(rows)} rows)")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{STEM}.csv.gz", index=False, compression="gzip")
    print("\n=== GATES ===")
    for k, v in gates.items():
        print(f"  {k}: {v}")
    print(f"\n{len(df)} published rows -> {STEM}.csv.gz")
    return df, gates


# ---------------------------------------------------------------- analysis
def cell(r):
    return f"c={r.band:.2f}|g={r.gross:.2f}"


def analysis(df):
    L = df[df.arm.isin(["CASH", "SHYFREE", "SHYTRADED"])].copy()
    L["cell"] = L.apply(cell, axis=1)
    h = L[(L.offset == 0) & (L.cost == 10.0)]

    print("\n########## A. THE LADDER, ALL 25 GRID POINTS, offset d=0, 10 bps ##########")
    for pan in ["U56", "B136"]:
        for wn in ["FULL", "IS", "OOS"]:
            x = h[(h.panel == pan) & (h.window == wn)]
            for arm in ["CASH", "SHYFREE", "SHYTRADED"]:
                t = x[x.arm == arm].pivot_table(index="band", columns="gross", values="CAGR") * 100
                print(f"\n-- CAGR %% {pan} {wn} arm={arm} (rows band, cols gross) --")
                print(t.round(2).to_string())
            for v in ("Sharpe", "MaxDD"):
                for arm in ["CASH", "SHYFREE"]:
                    t = x[x.arm == arm].pivot_table(index="band", columns="gross", values=v)
                    print(f"\n-- {v} {pan} {wn} arm={arm} --")
                    print((t * 100 if v == "MaxDD" else t).round(3).to_string())
            for arm in ["CASH", "SHYFREE", "SHYTRADED"]:
                y = x[x.arm == arm]
                print(f"   {arm}: 4a passers {sorted(y[y.keep4a].cell)} | 4b passers {sorted(y[y.keep4b].cell)}")
                f = y[~y.keep4b]
                print(f"      binding legs among {len(f)} fails: H1 {(~f.leg_H1).sum()} H2 {(~f.leg_H2).sum()} "
                      f"DD {(~f.leg_DD).sum()} CAGR {(~f.leg_CAGR).sum()}")

    print("\n########## B. HOW MUCH OF THE CAGR SHORTFALL IS THE CONVENTION? ##########")
    print("  shortfall = 0.70*SPY CAGR - book CAGR (pp, >0 means the 4b CAGR floor BINDS)")
    print("  credit    = SHYFREE CAGR - CASH CAGR (pp)      share = credit / shortfall")
    for pan in ["U56", "B136"]:
        for wn in ["FULL", "OOS"]:
            s = df[(df.panel == pan) & (df.arm == "SPY") & (df.window == wn)].iloc[0]
            x = h[(h.panel == pan) & (h.window == wn)]
            ca = x[x.arm == "CASH"].set_index("cell"); fr = x[x.arm == "SHYFREE"].set_index("cell")
            tr = x[x.arm == "SHYTRADED"].set_index("cell")
            short = (0.70 * s.CAGR - ca.CAGR) * 100
            cred = (fr.CAGR - ca.CAGR) * 100
            credt = (tr.CAGR - ca.CAGR) * 100
            tab = pd.DataFrame({"idle%": ca.idle * 100, "shortfall_pp": short, "free_credit_pp": cred,
                                "traded_credit_pp": credt, "share_free": cred / short,
                                "closes_gap": fr.CAGR >= 0.70 * s.CAGR})
            tab = tab.sort_values("shortfall_pp")
            print(f"\n-- {pan} {wn} (SPY CAGR {s.CAGR:.2%}, floor {0.70*s.CAGR:.2%}) --")
            print(tab.round(3).to_string())
            print(f"   cells whose shortfall the FREE sweep closes: {int(tab.closes_gap.sum())} of {len(tab)}"
                  f" | median share of shortfall closed {tab.share_free.median():.3f}"
                  f" | max {tab.share_free.max():.3f}")

    print("\n########## C. THE LIVE CELL (band 0.03 / gross 0.75), every window and cost rung ##########")
    for pan in ["U56", "B136"]:
        x = L[(L.panel == pan) & (L.cell == "c=0.03|g=0.75") & (L.offset == 0)]
        for wn in ["FULL", "IS", "OOS"]:
            for arm in ["CASH", "SHYFREE", "SHYTRADED"]:
                y = x[(x.window == wn) & (x.arm == arm)].sort_values("cost")
                print(f"{pan} {wn} {arm:9s} CAGR " + " ".join(f"{v:.2%}" for v in y.CAGR) +
                      " | Sharpe " + " ".join(f"{v:.4f}" for v in y.Sharpe) +
                      " | MaxDD " + " ".join(f"{v:.2%}" for v in y.MaxDD) +
                      f" | turn/yr {y.turn.iloc[0]:.2f} | 4a " + "".join(str(int(v)) for v in y.keep4a) +
                      " 4b " + "".join(str(int(v)) for v in y.keep4b))

    print("\n########## D. RULE 8 (band, gross chosen on 2009-2016 IS Sharpe ONLY; 2017-2026 read once) ##########")
    for pan in ["U56", "B136"]:
        s_oos = df[(df.panel == pan) & (df.arm == "SPY") & (df.window == "OOS")].iloc[0]
        s_full = df[(df.panel == pan) & (df.arm == "SPY") & (df.window == "FULL")].iloc[0]
        b_oos = df[(df.panel == pan) & (df.arm == "RULESv2") & (df.window == "OOS")].iloc[0]
        print(f"\n-- {pan} comparands: SPY OOS {s_oos.CAGR:.2%}/{s_oos.Sharpe:.4f}/{s_oos.MaxDD:.2%} "
              f"(H1 {s_oos.H1:.3f} H2 {s_oos.H2:.3f}); RULES v2 OOS {b_oos.CAGR:.2%}/{b_oos.Sharpe:.4f}/{b_oos.MaxDD:.2%} "
              f"(H1 {b_oos.H1:.3f} H2 {b_oos.H2:.3f}); SPY FULL {s_full.CAGR:.2%}/{s_full.Sharpe:.4f}/{s_full.MaxDD:.2%}")
        for arm in ["CASH", "SHYFREE", "SHYTRADED"]:
            g = h[(h.panel == pan) & (h.arm == arm)]
            isw = g[g.window == "IS"]
            for label, pool in (("C1 habitual argmax IS Sharpe", isw),
                                ("C2 argmax IS Sharpe among IS-4b passers", isw[isw.keep4b])):
                if len(pool) == 0:
                    print(f"   {arm:9s} {label}: NO IS 4b PASSER -> unreachable"); continue
                pick = pool.sort_values("Sharpe", ascending=False).iloc[0].cell
                o = g[(g.window == "OOS") & (g.cell == pick)].iloc[0]
                fu = g[(g.window == "FULL") & (g.cell == pick)].iloc[0]
                off = L[(L.panel == pan) & (L.arm == arm) & (L.cell == pick) & (L.window == "OOS") & (L.cost == 10.0)].sort_values("offset")
                cst = L[(L.panel == pan) & (L.arm == arm) & (L.cell == pick) & (L.window == "OOS") & (L.offset == 0)].sort_values("cost")
                print(f"   {arm:9s} {label} -> {pick}")
                print(f"      OOS  {o.CAGR:.2%} / {o.Sharpe:.4f} / {o.MaxDD:.2%}  (H1 {o.H1:.3f} H2 {o.H2:.3f})"
                      f"  4b={o.keep4b} 4a={o.keep4a} legs H1={o.leg_H1} H2={o.leg_H2} DD={o.leg_DD} CAGR={o.leg_CAGR}")
                print(f"      FULL {fu.CAGR:.2%} / {fu.Sharpe:.4f} / {fu.MaxDD:.2%} (H1 {fu.H1:.3f} H2 {fu.H2:.3f}) 4b={fu.keep4b} 4a={fu.keep4a}")
                print(f"      OOS 4b at offsets {list(off.offset)} = {list(off.keep4b.astype(int))};"
                      f" at 0/10/25/50 bps = {list(cst.keep4b.astype(int))}")

    print("\n########## E. DOES THE SWEEP MOVE ANY VERDICT? (all windows, all cost rungs, d=0) ##########")
    for pan in ["U56", "B136"]:
        for wn in ["FULL", "IS", "OOS"]:
            for cost in COSTS:
                x = L[(L.panel == pan) & (L.window == wn) & (L.cost == cost) & (L.offset == 0)]
                n = {a: (int(x[(x.arm == a)].keep4b.sum()), int(x[(x.arm == a)].keep4a.sum())) for a in
                     ["CASH", "SHYFREE", "SHYTRADED"]}
                print(f"{pan} {wn:4s} {cost:5.1f} bps  4b/4a of 25: CASH {n['CASH']}  "
                      f"SHYFREE {n['SHYFREE']}  SHYTRADED {n['SHYTRADED']}")

    print("\n########## F. THE SWEEP'S OWN COST: turnover and what it eats ##########")
    for pan in ["U56", "B136"]:
        x = h[(h.panel == pan) & (h.window == "FULL")]
        for arm in ["CASH", "SHYFREE", "SHYTRADED"]:
            y = x[x.arm == arm].set_index("cell").sort_index()
            print(f"{pan} {arm:9s} turnover/yr median {y.turn.median():.2f} "
                  f"(min {y.turn.min():.2f} max {y.turn.max():.2f})")
        ca = x[x.arm == "CASH"].set_index("cell"); fr = x[x.arm == "SHYFREE"].set_index("cell")
        tr = x[x.arm == "SHYTRADED"].set_index("cell")
        print(f"{pan} FULL: free credit mean {((fr.CAGR-ca.CAGR)*100).mean():+.3f} pp, "
              f"traded credit mean {((tr.CAGR-ca.CAGR)*100).mean():+.3f} pp, "
              f"sweep cost mean {((fr.CAGR-tr.CAGR)*100).mean():.3f} pp "
              f"({((fr.CAGR-tr.CAGR)/(fr.CAGR-ca.CAGR)).mean():.1%} of the credit)")

    print("\n########## G. OFFSET SPREAD of the live cell's CAGR credit (scheduling noise) ##########")
    for pan in ["U56", "B136"]:
        for wn in ["FULL", "OOS"]:
            x = L[(L.panel == pan) & (L.cell == "c=0.03|g=0.75") & (L.window == wn) & (L.cost == 10.0)]
            ca = x[x.arm == "CASH"].set_index("offset").sort_index()
            fr = x[x.arm == "SHYFREE"].set_index("offset").sort_index()
            cr = (fr.CAGR - ca.CAGR) * 100
            print(f"{pan} {wn}: free credit at d=0,1,2 = {[f'{v:+.3f}' for v in cr]} pp "
                  f"(spread {cr.max()-cr.min():.3f} pp)")


if __name__ == "__main__":
    df, gates = main()
    analysis(df)
