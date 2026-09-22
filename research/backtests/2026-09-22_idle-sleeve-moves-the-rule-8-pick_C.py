#!/usr/bin/env python3
"""Idea 2217 (lane C, 2026-09-22): DOES AN IDLE SLEEVE MOVE *WHICH CELL* RULE 8 REACHES ON THE
2119 BAND x GROSS LADDER?

PREMISE AS FILED.  2119(D) found IS Sharpe moves only 0.0013 across the whole gross dial at
fixed band, so rule 8 resolves BAND and (as filed) "coin-flips" GROSS.  `engine.backtest` pays
exactly 0% on the uninvested residual `1 - sum(w)`, which on this ladder runs from ~25% of NAV
(gross 1.00, band always IN) to ~75% (gross 0.50).  A sleeve that PAYS the idle NAV therefore
changes the IS objective by a DIFFERENT amount in every cell -- the credit scales with
`1 - realised gross` -- so it may make the IS surface see exposure for the first time.

PREMISE UPDATE (honest, before any compute).  2121 (lane cloud, earlier today) retired the
"coin-flip" half: IS Sharpe is MONOTONE in gross 40 of 40 blocks with argmax gross = 1.00 in
40 of 40.  The question that survives is sharper and is the one this run answers: a SHY sleeve
credits the LOW-gross cells most, so does it INVERT that monotonicity and move the pick DOWN
the gross dial -- and if the pick moves, is the moved pick better OOS?

TUNED (2, exactly): BAND c x GROSS g -- the 2119 ladder's own two dials, chosen by rule 8
INSIDE each sleeve arm.  The sleeve fraction phi is a published ARM, reported at every level and
NEVER selected, so the 2-parameter cap holds.  ALL 25 grid points are reported for every arm.
PUBLISHED-NOT-TUNED: panel {U56,B136} x phi arm {NOSLEEVE,0.00,0.25,0.50,0.75,1.00} x weekday
offset d in {0..4} (a NOISE MEASUREMENT; the reported book is always d=0) x cost {0,10,25,50}
bps (headline 10) x window {FULL,IS,OOS}.

DISTINCT FROM 2221 (lane B, same day), which fixed gross at the live 0.75 and tuned (phi, band).
This run holds phi fixed inside an arm and asks whether the sleeve moves the pick ON THE GROSS
DIAL.  Sleeve construction is deliberately IDENTICAL to 2221's so the two are comparable.

Weekly, long-only, no leverage (sleeved total weight is exactly 1.0), t+1 execution, 10 bps
headline.  Rule 8: (c,g) chosen on 2009-2016 IS rows alone; 2017-2026 read ONCE.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

BANDS   = [0.00, 0.02, 0.03, 0.05, 0.08]
GROSSES = [0.50, 0.625, 0.75, 0.875, 1.00]
ARMS    = ["NOSLEEVE", 0.00, 0.25, 0.50, 0.75, 1.00]     # NOSLEEVE = live 0%-cash form
OFFSETS = [0, 1, 2, 3, 4]
COSTS   = [0.0, 10.0, 25.0, 50.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SLUG = "2026-09-22_idle-sleeve-moves-the-rule-8-pick_C"
OUT  = ROOT / "research" / "backtests"

# ---------------------------------------------------------------- book construction
def core_weights(px, c, g):
    """RULES v2 clauses 2-4 exactly: every IN name at g/N, N = names priced that day, gated-out
    weight to CASH (de-gross, never re-spread).  c=0.03, g=0.75 IS baseline.rules_v2_weights."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, c), 0.0)

def sleeved_weights(px, c, g, phi):
    """Core band book + the idle NAV (1 - sum of core weights) held in phi*SPY + (1-phi)*SHY.
    Identical construction to idea 2221 (lane B).  SPY and SHY are also gated universe names, so
    the sleeve ADDS to any core holding in them.  Total weight is exactly 1.0 -> fully invested,
    long-only, no leverage."""
    w = core_weights(px, c, g)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    out = w.copy()
    out["SPY"] = out["SPY"] + idle * phi
    out["SHY"] = out["SHY"] + idle * (1.0 - phi)
    return out

def book(px, c, g, arm):
    return core_weights(px, c, g) if arm == "NOSLEEVE" else sleeved_weights(px, c, g, arm)

# ---------------------------------------------------------------- offset-aware runner
def offset_mask(idx, d):
    """Weekly rebalance shifted d trading days EARLIER inside its own week.  d=0 is the last
    trading day of the week (== engine.rebalance_mask(idx,'W')).  A week with <= d trading days
    falls back to its earliest day -- those weeks are CLIPPED and counted, never silently
    dropped (so d<=2 is the clip-free region on these panels)."""
    key = pd.Series(idx.to_period("W"), index=idx)
    mask = pd.Series(False, index=idx); clipped = 0
    for _, grp in key.groupby(key, sort=False):
        days = grp.index
        if len(days) > d: pick = days[-(1 + d)]
        else: pick = days[0]; clipped += 1
        mask.loc[pick] = True
    return mask, clipped

def run(px_vals, W_vals, m_vals):
    """engine.backtest semantics (decide at t, apply at t+1, drift between rebalances), numpy,
    arbitrary rebalance mask.  Returns GROSS-of-cost returns + turnover, so any cost rung is an
    exact affine re-read: r(c) = r_gross - turnover*c/1e4."""
    rets, wt, m = px_vals, W_vals, m_vals
    n = rets.shape[0]; cur = np.zeros(rets.shape[1]); held = np.zeros_like(rets); to = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return (held * rets).sum(axis=1), to

def m6(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

# ---------------------------------------------------------------- KEEP paths
def keep4a(a, b):
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves AND MaxDD no worse."""
    return bool(a["H1"] > b["H1"] and a["H2"] > b["H2"] and a["MaxDD"] >= b["MaxDD"])

def legs4b(a, s):
    """PROTOCOL 4b: Sharpe > SPY in both halves, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    return dict(H1=bool(a["H1"] > s["H1"]), H2=bool(a["H2"] > s["H2"]),
                DD=bool(a["MaxDD"] >= 0.60 * s["MaxDD"]), CAGR=bool(a["CAGR"] >= 0.70 * s["CAGR"]))

def windows(idx):
    start = idx[260]
    return {"FULL": (start, idx[-1]), "IS": (start, pd.Timestamp(IS_END)),
            "OOS": (pd.Timestamp(OOS_START), idx[-1])}

def armname(a): return "NOSLV" if a == "NOSLEEVE" else f"phi{a:.2f}"
def cellname(c, g): return f"c{c:.2f}_g{g:.3f}"

# ---------------------------------------------------------------- main
def main():
    rows = []; gates = {}
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}

    for pname, px in panels.items():
        idx = px.index; wins = windows(idx)
        print(f"\n=== panel {pname}: {px.shape[1]} names, {idx[0].date()}..{idx[-1].date()} ===", flush=True)
        rets = px.pct_change().fillna(0.0).values

        # ---- gates ---------------------------------------------------------
        m0, clip0 = offset_mask(idx, 0)
        gates[f"G2_{pname}_maskdiff_vs_engine_W"] = int((m0.values != rebalance_mask(idx, "W").values).sum())
        w_live = rules_v2_weights(px, 0.03, 0.75)
        gates[f"G3_{pname}_ladder_centre_is_RULESv2"] = float((core_weights(px, 0.03, 0.75) - w_live).abs().max().max())
        wv = w_live.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
        mv = m0.shift(1, fill_value=False).values
        gr, to = run(rets, wv, mv)
        gr = pd.Series(gr, index=idx); to = pd.Series(to, index=idx)
        eng10 = engine_backtest(px, w_live, cost_bps=10.0, freq="W")["returns"]
        eng25 = engine_backtest(px, w_live, cost_bps=25.0, freq="W")["returns"]
        gates[f"G1_{pname}_runner_vs_engine_10bps"] = float((gr - to * 10.0 / 1e4 - eng10).abs().max())
        gates[f"G4_{pname}_cost_reconstruction_25bps"] = float((gr - to * 25.0 / 1e4 - eng25).abs().max())
        gates[f"G5_{pname}_clipped_weeks_d2"] = offset_mask(idx, 2)[1]
        gates[f"G5_{pname}_clipped_weeks_d4"] = offset_mask(idx, 4)[1]
        # G6: sleeved book is exactly fully invested whenever the panel is priced
        wtest = sleeved_weights(px, 0.03, 0.75, 0.25)
        gates[f"G6_{pname}_sleeved_total_weight_dev"] = float((wtest.sum(axis=1).loc[idx[260]:] - 1.0).abs().max())

        # ---- benchmarks ------------------------------------------------------
        spy = px["SPY"].pct_change().fillna(0.0)
        v1 = engine_backtest(px, rules_v1_weights(px), cost_bps=10.0, freq="W")["returns"]
        bench = {}
        for wn, (a, b) in wins.items():
            bench[("SPY", wn)] = m6(spy.loc[a:b])
            bench[("RULESv2", wn)] = m6(eng10.loc[a:b])
            bench[("RULESv1", wn)] = m6(v1.loc[a:b])
        for (nm, wn), v in bench.items():
            rows.append(dict(panel=pname, arm=nm, band=np.nan, gross=np.nan, offset=0,
                             cost=10.0, window=wn, **v, keep4a=False, keep4b=False,
                             **{f"leg_{x}": False for x in ("H1", "H2", "DD", "CAGR")}))

        # ---- the ladder, every arm ------------------------------------------
        # weights do not depend on the weekday offset, so each of the 150 books is built ONCE
        # and re-run across the five offsets; band_state is cached per band.
        masks = {}
        for d in OFFSETS:
            mk, _ = offset_mask(idx, d)
            masks[d] = mk.shift(1, fill_value=False).values
        st = {c: band_state(px, c) for c in BANDS}
        e = pd.DataFrame(1.0, index=idx, columns=px.columns).where(px.notna(), 0.0)
        nn = e.sum(axis=1).replace(0, np.nan)
        spy_i = list(px.columns).index("SPY"); shy_i = list(px.columns).index("SHY")
        for c in BANDS:
            for g in GROSSES:
                core = (g * e.div(nn, axis=0).fillna(0.0)).where(st[c], 0.0)
                cv = np.array(core.values, dtype=float)
                idle = np.clip(1.0 - cv.sum(axis=1), 0.0, None)
                for arm in ARMS:
                    wv = cv.copy()
                    if arm != "NOSLEEVE":
                        wv[:, spy_i] = wv[:, spy_i] + idle * arm
                        wv[:, shy_i] = wv[:, shy_i] + idle * (1.0 - arm)
                    wv = np.vstack([np.zeros((1, wv.shape[1])), wv[:-1]])   # decide at t, apply t+1
                    for d in OFFSETS:
                        gg, tt = run(rets, wv, masks[d])
                        gg = pd.Series(gg, index=idx); tt = pd.Series(tt, index=idx)
                        for cost in COSTS:
                            r = gg - tt * cost / 1e4
                            for wn, (a, b) in wins.items():
                                mm = m6(r.loc[a:b]); s = bench[("SPY", wn)]; bl = bench[("RULESv2", wn)]
                                lg = legs4b(mm, s)
                                rows.append(dict(panel=pname, arm=armname(arm), band=c, gross=g,
                                                 offset=d, cost=cost, window=wn, **mm,
                                                 keep4a=keep4a(mm, bl), keep4b=all(lg.values()),
                                                 **{f"leg_{k}": v for k, v in lg.items()}))
            print(f"  band c={c} done ({len(rows)} rows)", flush=True)
        # G7: the fast in-loop book build reproduces the reference constructor exactly
        ref = book(px, 0.03, 0.75, 0.25).values
        fast = np.array((0.75 * e.div(nn, axis=0).fillna(0.0)).where(st[0.03], 0.0).values, dtype=float)
        idle_r = np.clip(1.0 - fast.sum(axis=1), 0.0, None)
        fast[:, spy_i] += idle_r * 0.25; fast[:, shy_i] += idle_r * 0.75
        gates[f"G7_{pname}_fastbuild_vs_reference"] = float(np.abs(fast - ref).max())

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{SLUG}.grid.csv.gz", index=False, compression="gzip")
    print("\n=== GATES ===")
    for k, v in gates.items(): print(f"  {k}: {v}")
    print(f"\n{len(df)} published rows -> {SLUG}.grid.csv.gz")
    return df, gates

# ---------------------------------------------------------------- analysis
LADDER = [armname(a) for a in ARMS]

def analysis(df):
    L = df[df.arm.isin(LADDER)].copy()
    L["cell"] = [cellname(c, g) for c, g in zip(L.band, L.gross)]
    h = L[(L.offset == 0) & (L.cost == 10.0)]
    B = df[~df.arm.isin(LADDER)]

    print("\n########## ANCHORS (offset d=0, 10 bps) ##########")
    for pan in ["U56", "B136"]:
        for nm in ["SPY", "RULESv2", "RULESv1"]:
            for wn in ["FULL", "IS", "OOS"]:
                x = B[(B.panel == pan) & (B.arm == nm) & (B.window == wn)].iloc[0]
                print(f"  {pan:4s} {nm:8s} {wn:4s}  CAGR {x.CAGR:7.2%}  Sharpe {x.Sharpe:.4f}  "
                      f"MaxDD {x.MaxDD:7.2%}  halves {x.H1:.4f}/{x.H2:.4f}")

    print("\n########## (A) DOES THE IS SURFACE SEE EXPOSURE?  IS Sharpe ACROSS THE GROSS DIAL ##########")
    print("per panel x arm x band: spread = max-min IS Sharpe over the 5 gross rungs; argmax gross")
    seen = []
    for pan in ["U56", "B136"]:
        for arm in LADDER:
            x = h[(h.panel == pan) & (h.arm == arm) & (h.window == "IS")]
            sp, am = [], []
            for c in BANDS:
                y = x[x.band == c].set_index("gross").Sharpe.reindex(GROSSES)
                sp.append(y.max() - y.min()); am.append(y.idxmax())
            seen.append(dict(panel=pan, arm=arm, spread_mean=np.mean(sp), spread_max=np.max(sp),
                             argmax_hi=sum(a == 1.00 for a in am), argmax_lo=sum(a == 0.50 for a in am),
                             argmaxes=am))
            print(f"  {pan:4s} {arm:8s}  spread mean {np.mean(sp):.4f} max {np.max(sp):.4f}  "
                  f"argmax gross per band {[f'{a:.3f}' for a in am]}")
    pd.DataFrame(seen).to_csv(OUT / f"{SLUG}.is_surface.csv", index=False)

    print("\n########## (A2) MONOTONICITY IN GROSS (IS Sharpe), and what the sleeve pays ##########")
    for pan in ["U56", "B136"]:
        for arm in LADDER:
            x = h[(h.panel == pan) & (h.arm == arm) & (h.window == "IS")]
            up = dn = 0
            for c in BANDS:
                y = x[x.band == c].set_index("gross").Sharpe.reindex(GROSSES).values
                d = np.diff(y); up += int((d > 0).all()); dn += int((d < 0).all())
            g = h[(h.panel == pan) & (h.arm == arm) & (h.window == "IS")].groupby("gross")[["CAGR", "Sharpe", "MaxDD"]].mean()
            print(f"  {pan:4s} {arm:8s} monotone-UP {up}/5 bands, monotone-DOWN {dn}/5 | "
                  f"mean IS Sharpe by gross {[f'{v:.3f}' for v in g.Sharpe]}")

    print("\n########## (B) 4a / 4b PASS COUNTS PER ARM (of 25 cells, d=0, 10 bps) ##########")
    for pan in ["U56", "B136"]:
        for wn in ["FULL", "IS", "OOS"]:
            line = []
            for arm in LADDER:
                x = h[(h.panel == pan) & (h.arm == arm) & (h.window == wn)]
                line.append(f"{arm}:4a{int(x.keep4a.sum())}/4b{int(x.keep4b.sum())}")
            f = h[(h.panel == pan) & (h.window == wn) & ~h.keep4b]
            print(f"  {pan:4s} {wn:4s}  " + "  ".join(line) +
                  f"   | binding legs among fails: H1 {(~f.leg_H1).sum()} H2 {(~f.leg_H2).sum()} "
                  f"DD {(~f.leg_DD).sum()} CAGR {(~f.leg_CAGR).sum()}")

    print("\n########## (C) RULE 8: PICK PER ARM (2009-2016 only), DOES IT MOVE, IS IT BETTER OOS? ##########")
    picks = []
    for pan in ["U56", "B136"]:
        for chooser, need4b in (("C1 argmax IS Sharpe", False),
                                ("C2 argmax IS Sharpe among IS-4b passers", True)):
            base_pick = None
            print(f"\n-- {pan} / {chooser} --")
            for arm in LADDER:
                g = h[(h.panel == pan) & (h.arm == arm)]
                pool = g[g.window == "IS"]
                if need4b: pool = pool[pool.keep4b]
                if len(pool) == 0:
                    print(f"   {arm:8s} NO IS PASSER"); picks.append(dict(panel=pan, chooser=chooser, arm=arm, pick=None)); continue
                pk = pool.sort_values("Sharpe", ascending=False).iloc[0].cell
                if arm == "NOSLV": base_pick = pk
                o = g[(g.window == "OOS") & (g.cell == pk)].iloc[0]
                fu = g[(g.window == "FULL") & (g.cell == pk)].iloc[0]
                oo = g[g.window == "OOS"].sort_values("Sharpe", ascending=False).reset_index(drop=True)
                rank = int(oo.index[oo.cell == pk][0]) + 1
                # counterfactual: the cell the NO-SLEEVE arm picked, priced INSIDE this arm
                cf = g[(g.window == "OOS") & (g.cell == base_pick)]
                cf = cf.iloc[0] if len(cf) else None
                moved = (pk != base_pick)
                dS = (o.Sharpe - cf.Sharpe) if cf is not None else np.nan
                dC = (o.CAGR - cf.CAGR) if cf is not None else np.nan
                dD = (o.MaxDD - cf.MaxDD) if cf is not None else np.nan
                off = L[(L.panel == pan) & (L.arm == arm) & (L.cell == pk) & (L.window == "OOS") & (L.cost == 10.0)].sort_values("offset")
                cst = L[(L.panel == pan) & (L.arm == arm) & (L.cell == pk) & (L.window == "OOS") & (L.offset == 0)].sort_values("cost")
                print(f"   {arm:8s} -> {pk}  MOVED={moved}"
                      f"\n            OOS {o.CAGR:7.2%} / {o.Sharpe:.4f} / {o.MaxDD:7.2%}  4b={bool(o.keep4b)} 4a={bool(o.keep4a)}"
                      f"  legs H1={bool(o.leg_H1)} H2={bool(o.leg_H2)} DD={bool(o.leg_DD)} CAGR={bool(o.leg_CAGR)}  OOS rank {rank}/25"
                      f"\n            FULL {fu.CAGR:7.2%} / {fu.Sharpe:.4f} / {fu.MaxDD:7.2%} 4b={bool(fu.keep4b)} halves {fu.H1:.4f}/{fu.H2:.4f}"
                      f"\n            vs the NOSLV-picked cell priced inside this arm ({base_pick}): "
                      f"dSharpe {dS:+.4f}  dCAGR {dC:+.2%}  dMaxDD {dD:+.2%}"
                      f"\n            OOS 4b at offsets 0..4 {list(off.keep4b.astype(int))}; at 0/10/25/50 bps {list(cst.keep4b.astype(int))}")
                picks.append(dict(panel=pan, chooser=chooser, arm=arm, pick=pk, moved=moved,
                                  oos_CAGR=o.CAGR, oos_Sharpe=o.Sharpe, oos_MaxDD=o.MaxDD,
                                  oos_rank=rank, keep4b_oos=bool(o.keep4b), keep4a_oos=bool(o.keep4a),
                                  full_CAGR=fu.CAGR, full_Sharpe=fu.Sharpe, full_MaxDD=fu.MaxDD,
                                  keep4b_full=bool(fu.keep4b), H1=fu.H1, H2=fu.H2,
                                  d_vs_unmoved_Sharpe=dS, d_vs_unmoved_CAGR=dC, d_vs_unmoved_MaxDD=dD,
                                  oos_4b_offsets="".join(map(str, off.keep4b.astype(int))),
                                  oos_4b_costs="".join(map(str, cst.keep4b.astype(int)))))
    P = pd.DataFrame(picks); P.to_csv(OUT / f"{SLUG}.picks.csv", index=False)

    print("\n########## (D) SUMMARY OF THE FILED QUESTION ##########")
    q = P.dropna(subset=["pick"])
    q = q[q.arm != "NOSLV"]
    print(f"  pick MOVED off the no-sleeve cell in {int(q.moved.sum())} of {len(q)} arm x panel x chooser instances")
    mv = q[q.moved]
    if len(mv):
        print(f"  of those moves, the moved pick beats the unmoved counterfactual OOS on Sharpe in "
              f"{int((mv.d_vs_unmoved_Sharpe > 0).sum())} of {len(mv)}; mean dSharpe {mv.d_vs_unmoved_Sharpe.mean():+.4f}, "
              f"mean dCAGR {mv.d_vs_unmoved_CAGR.mean():+.2%}, mean dMaxDD {mv.d_vs_unmoved_MaxDD.mean():+.2%}")
    print(f"  mean OOS rank of the fitted pick within its own arm: {q.oos_rank.mean():.2f} of 25 "
          f"(coin-flip null 13.0)")
    print(f"  4b OOS passes among fitted picks: {int(q.keep4b_oos.sum())} of {len(q)}; "
          f"4b FULL {int(q.keep4b_full.sum())} of {len(q)}; 4a OOS {int(q.keep4a_oos.sum())} of {len(q)}")

    print("\n########## (E) OFFSET SPREAD OF THE BINDING MARGINS (914/2119 clause) ##########")
    for _, r in P.dropna(subset=["pick"]).iterrows():
        pan, arm, pk = r.panel, r.arm, r.pick
        for wn in ["FULL", "OOS"]:
            x = L[(L.panel == pan) & (L.arm == arm) & (L.cell == pk) & (L.window == wn) & (L.cost == 10.0)].set_index("offset").sort_index()
            if 0 not in x.index: continue
            s = df[(df.panel == pan) & (df.arm == "SPY") & (df.window == wn)].iloc[0]
            dd = (x.MaxDD - 0.60 * s.MaxDD) * 100; cg = (x.CAGR - 0.70 * s.CAGR) * 100
            print(f"  {pan:4s} {arm:8s} {pk} {wn:4s}: DD margin {dd.loc[0]:+6.2f} pp (spread {dd.max()-dd.min():.2f}, "
                  f"clip-free d<=2 {dd.loc[:2].max()-dd.loc[:2].min():.2f}) | CAGR margin {cg.loc[0]:+6.2f} pp "
                  f"(spread {cg.max()-cg.min():.2f}, clip-free {cg.loc[:2].max()-cg.loc[:2].min():.2f})")

    print("\n########## (F) HEADLINE TABLES: OOS Sharpe by cell, per arm (d=0, 10 bps) ##########")
    for pan in ["U56", "B136"]:
        for arm in LADDER:
            x = h[(h.panel == pan) & (h.arm == arm) & (h.window == "OOS")]
            print(f"\n-- OOS Sharpe {pan} {arm} (rows band, cols gross) --")
            print(x.pivot_table(index="band", columns="gross", values="Sharpe").round(4).to_string())
            y = h[(h.panel == pan) & (h.arm == arm) & (h.window == "OOS")]
            print(f"-- OOS CAGR {pan} {arm} --")
            print((y.pivot_table(index="band", columns="gross", values="CAGR") * 100).round(2).to_string())
    return P

if __name__ == "__main__":
    df, gates = main()
    P = analysis(df)
