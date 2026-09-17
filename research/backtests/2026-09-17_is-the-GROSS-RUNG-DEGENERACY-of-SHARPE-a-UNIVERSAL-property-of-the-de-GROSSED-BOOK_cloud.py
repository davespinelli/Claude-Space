#!/usr/bin/env python3
"""Idea 1189 (cloud lane, 2026-09-17, idea 1 of 2): is the GROSS-RUNG DEGENERACY of
SHARPE a UNIVERSAL property of the de-GROSSED book?

QUESTION. Idea 1158's rule-8 leg found U56's Sharpe runs 1.1389 -> 1.1397 across gross
0.50 -> 0.75 (spread 8e-04 over a 1.5x change in gross), and 11 of its 16 4b passers
were that one book re-read at different gross. Is that a property of that one cell, or
of every de-grossed long-only book with a 0%-return cash sleeve?

TWO DIALS AND NO MORE (rule 4):
    dial 1 = GROSS RUNG  g in {0.30,0.40,0.50,0.60,0.70,0.75,0.85,1.00}   (8 rungs)
    dial 2 = ANCHOR      (N, cadence) in {(20,W),(12,W),(30,W),(10,M),(20,M)}  (5)
NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four statistics
(Sharpe, CAGR, MaxDD, turnover); the 4a and 4b legs; the three rule-8 choosers.
=> 3 x 5 x 8 = 120 books, EVERY ONE PUBLISHED in the .grid.csv.

BOOK CONSTRUCTION, frozen at the 2026-09-04 KEEP-4b candidate's: composite score
(12-1 momentum + 6m + 3m, cross-sectional percentile ranks), NO vol scaler, eligibility
= close above its own 200d MA, top-N equal weight at g/N of NAV, gated-out weight to
CASH at 0%. Costs 10 bps per unit turnover, weights decided at close t applied at t+1
(PROTOCOL rules 2 and 3).

Run:  python3 research/backtests/2026-09-17_is-the-GROSS-RUNG-DEGENERACY-...-_cloud.py
"""
import sys, json, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics                  # noqa: E402

OUT   = Path(__file__).with_suffix("")
COST  = 10.0
GROSS = [0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00]
ANCHORS = [(20, "W"), (12, "W"), (30, "W"), (10, "M"), (20, "M")]
OOS_START = "2017-01-01"          # rule 8: choose on <2017, evaluate 2017-2026 untouched
WARMUP = 260

# ---------------------------------------------------------------- fast runner
def fast_backtest(px, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (gated in G1). Loops over rebalance
    SEGMENTS instead of days, so the 120-book grid is tractable on the 663-name panel."""
    rets = px.pct_change().fillna(0.0).values
    idx  = px.index
    W    = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, M = rets.shape
    P     = np.cumprod(1.0 + rets, axis=0)
    Pprev = np.vstack([np.ones((1, M)), P[:-1]])          # Pprev[i] = P[i-1]
    held  = np.zeros((T, M)); turn = np.zeros(T)
    starts = np.flatnonzero(mask); ends = np.append(starts[1:], T)
    cur = np.zeros(M)
    for i0, i1 in zip(starts, ends):
        w0 = W[i0]
        turn[i0] = np.abs(w0 - cur).sum()
        base = Pprev[i0]
        A = w0[None, :] * (Pprev[i0:i1] / base[None, :])
        cash0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + cash0
        held[i0:i1] = A / V[:, None]
        Aend = w0 * (P[i1 - 1] / base)
        cur  = Aend / (Aend.sum() + cash0)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)

# ---------------------------------------------------------------- book weights
def composite_rank(px, invest):
    """Cross-sectional composite (scan.py's, vol_scale OFF) restricted to `invest`."""
    q = px[invest]
    mom = q.shift(21) / q.shift(252) - 1
    r6  = q / q.shift(126) - 1
    r3  = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = q > q.rolling(200).mean()
    elig = comp.where(above)
    return elig.rank(axis=1, ascending=False), q.columns

def book_weights(rank, cols, px, n, gross):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w[cols] = (rank <= n).astype(float) * (gross / n)
    return w

# ---------------------------------------------------------------- stats
def stat(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]

def legs_4b(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's."""
    h = len(r) // 2
    sh1, sh2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    b1, b2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    L = dict(
        L_H1=sh1 > b1, L_H2=sh2 > b2,
        L_OOS=metrics(ro)["Sharpe"] > metrics(so)["Sharpe"],
        L_DD=abs(metrics(r)["MaxDD"]) <= 0.60 * abs(metrics(spy)["MaxDD"]),
        L_CAGR=metrics(r)["CAGR"] >= 0.70 * metrics(spy)["CAGR"],
    )
    L["PASS_4b"] = all(L.values())
    return L

def legs_4a(r, base):
    h = len(r) // 2
    ok = (metrics(r.iloc[:h])["Sharpe"] > metrics(base.iloc[:h])["Sharpe"]
          and metrics(r.iloc[h:])["Sharpe"] > metrics(base.iloc[h:])["Sharpe"]
          and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])
    return ok

# ---------------------------------------------------------------- panels
def panels():
    P = {}
    u = load_universe()
    P["U56"] = (u, [c for c in u.columns])
    b = load_universe(broad=True)
    P["B136"] = (b, [c for c in b.columns])
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in s.columns if c != "SPY" and c not in bad]
    s = s[keep + ["SPY"]]
    P["SMALL"] = (s, keep)                       # SPY is the benchmark, NOT investable
    print(f"panels: U56 {u.shape}, B136 {b.shape}, SMALL {s.shape} "
          f"(dropped {len(bad)} max_1d_move>=1.0 names, {len(keep)} investable)")
    return P

# ---------------------------------------------------------------- main
def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    P = panels()
    gates, rows, spreads = [], [], []

    # ---- G1: fast runner == engine.backtest on a live cell -------------------
    px0, inv0 = P["U56"]
    rk0, cl0 = composite_rank(px0, inv0)
    w0 = book_weights(rk0, cl0, px0, 20, 0.75)
    r_fast, _ = fast_backtest(px0, w0, COST, "W")
    r_eng = backtest(px0, w0, cost_bps=COST, freq="W")["returns"]
    g1 = float(np.abs(r_fast - r_eng).max())
    gates.append(("G1 fast runner == engine.backtest (max abs diff)", g1, g1 < 1e-12))

    # ---- G2: determinism ----------------------------------------------------
    r_fast2, _ = fast_backtest(px0, w0, COST, "W")
    g2 = float(np.abs(r_fast - r_fast2).max())
    gates.append(("G2 determinism (max abs diff)", g2, g2 == 0.0))

    # ---- G3: exact-scaling identity is NOT assumed (1177's finding) ---------
    #  the weight identity W(g) == g*W(1) holds by construction; the RETURN path
    #  identity r(g) == g*r(1) must NOT, because the cash sleeve compounds.
    wA = book_weights(rk0, cl0, px0, 20, 0.30)
    rA, _ = fast_backtest(px0, wA, COST, "W")
    wB = book_weights(rk0, cl0, px0, 20, 1.00)
    rB, _ = fast_backtest(px0, wB, COST, "W")
    g3 = float(np.abs(rA - 0.30 * rB).max())
    gates.append(("G3 cash sleeve breaks r(g)==g*r(1) (max abs dev, >0 expected)",
                  g3, g3 > 0.0))

    # ---- G4: live RULES v2 baseline reproduces ------------------------------
    rv2 = backtest(px0, rules_v2_weights(px0), cost_bps=COST, freq="W")["returns"]
    g4 = float(metrics(rv2.loc[px0.index[WARMUP]:])["MaxDD"])
    gates.append(("G4 live RULES v2 U56 MaxDD (record: -12.05%)", g4, abs(g4 + 0.1205) < 0.01))

    # ---- the grid -----------------------------------------------------------
    bench, live = {}, {}
    for pname, (px, inv) in P.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        lv = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[start:]
        bench[pname], live[pname] = spy, lv
        c, s, d = stat(spy); co, so_, do = stat(spy.loc[OOS_START:])
        lc, ls, ld = stat(lv)
        print(f"\n[{pname}] SPY {c:.2%}/{s:.4f}/{d:.2%}  OOS {co:.2%}/{so_:.4f}  |  "
              f"RULES v2 live {lc:.2%}/{ls:.4f}/{ld:.2%}")

        for (n, freq) in ANCHORS:
            rank, cols = composite_rank(px, inv)
            cell = []
            for g in GROSS:
                w = book_weights(rank, cols, px, n, g)
                r, t = fast_backtest(px, w, COST, freq)
                r = r.loc[start:]; t = t.loc[start:]
                cg, sh, dd = stat(r)
                ro = r.loc[OOS_START:]
                cgo, sho, ddo = stat(ro)
                L = legs_4b(r, spy)
                rec = dict(panel=pname, n=n, cadence=freq, gross=g,
                           CAGR=cg, Sharpe=sh, MaxDD=dd,
                           H1=metrics(r.iloc[:len(r)//2])["Sharpe"],
                           H2=metrics(r.iloc[len(r)//2:])["Sharpe"],
                           OOS_CAGR=cgo, OOS_Sharpe=sho, OOS_MaxDD=ddo,
                           turnover=t.sum() / (len(r) / 252),
                           IS_Sharpe=metrics(r.loc[:OOS_START])["Sharpe"],
                           IS_CAGR=metrics(r.loc[:OOS_START])["CAGR"],
                           IS_MaxDD=metrics(r.loc[:OOS_START])["MaxDD"],
                           PASS_4a=legs_4a(r, lv), **L)
                rows.append(rec); cell.append(rec)
            c_df = pd.DataFrame(cell)
            sp = dict(panel=pname, n=n, cadence=freq,
                      Sharpe_spread=c_df.Sharpe.max() - c_df.Sharpe.min(),
                      Sharpe_rel=(c_df.Sharpe.max() - c_df.Sharpe.min()) / abs(c_df.Sharpe.mean()),
                      CAGR_spread=c_df.CAGR.max() - c_df.CAGR.min(),
                      CAGR_rel=(c_df.CAGR.max() - c_df.CAGR.min()) / abs(c_df.CAGR.mean()),
                      MaxDD_spread=c_df.MaxDD.max() - c_df.MaxDD.min(),
                      MaxDD_rel=(c_df.MaxDD.max() - c_df.MaxDD.min()) / abs(c_df.MaxDD.mean()),
                      turn_rel=(c_df.turnover.max() - c_df.turnover.min()) / abs(c_df.turnover.mean()),
                      OOS_Sharpe_spread=c_df.OOS_Sharpe.max() - c_df.OOS_Sharpe.min(),
                      n_4b=int(c_df.PASS_4b.sum()), n_4a=int(c_df.PASS_4a.sum()))
            spreads.append(sp)
            print(f"  {pname:5s} N={n:<3d} {freq}  Sharpe spread {sp['Sharpe_spread']:.5f} "
                  f"({sp['Sharpe_rel']:.4%} of mean)  CAGR {sp['CAGR_rel']:.2%}  "
                  f"MaxDD {sp['MaxDD_rel']:.2%}  4b {sp['n_4b']}/8  4a {sp['n_4a']}/8")

    grid = pd.DataFrame(rows); spr = pd.DataFrame(spreads)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    spr.to_csv(f"{OUT}.spreads.csv", index=False)

    # ---- G5: the gross dial IS live on the statistics it is supposed to move -
    g5 = float(spr.CAGR_rel.min())
    gates.append(("G5 gross dial moves CAGR at every cell (min rel spread)", g5, g5 > 0.10))
    # ---- G6: monotone |MaxDD| in gross (calibration premise) ----------------
    mono = []
    for (p, n, f), sub in grid.groupby(["panel", "n", "cadence"]):
        sub = sub.sort_values("gross")
        mono.append(bool((np.diff(-sub.MaxDD.values) >= -1e-12).all()))
    g6 = float(np.mean(mono))
    gates.append(("G6 |MaxDD| non-decreasing in gross (share of cells)", g6, g6 == 1.0))

    # ---------------------------------------------------------------- headline
    print("\n" + "=" * 78)
    print("(A) THE RUNG SPREAD DISTRIBUTION — 15 (panel, anchor) cells, 8 gross rungs each")
    print("=" * 78)
    for col, lab in [("Sharpe_rel", "Sharpe"), ("CAGR_rel", "CAGR"),
                     ("MaxDD_rel", "MaxDD"), ("turn_rel", "turnover")]:
        v = spr[col]
        print(f"  {lab:9s} relative rung spread  median {v.median():.4%}  "
              f"min {v.min():.4%}  max {v.max():.4%}")
    amp = spr.CAGR_rel / spr.Sharpe_rel
    print(f"\n  CAGR/Sharpe spread ratio: median {amp.median():.1f}x  "
          f"min {amp.min():.1f}x  max {amp.max():.1f}x")
    print(f"  Sharpe rung spread < 0.01 absolute at {int((spr.Sharpe_spread < 0.01).sum())} "
          f"of {len(spr)} cells;  < 0.05 at {int((spr.Sharpe_spread < 0.05).sum())} of {len(spr)}")
    print(f"  UNIVERSAL? max absolute Sharpe rung spread over all 15 cells = "
          f"{spr.Sharpe_spread.max():.5f} (cell "
          f"{spr.loc[spr.Sharpe_spread.idxmax(), ['panel','n','cadence']].to_dict()})")

    print("\n" + "=" * 78)
    print("(B) WHAT A 4b PASS AT A NEW GROSS RUNG ACTUALLY IS")
    print("=" * 78)
    p4b = grid[grid.PASS_4b]
    print(f"  4b full+OOS passes: {len(p4b)} of {len(grid)} books;  4a: {int(grid.PASS_4a.sum())} of {len(grid)}")
    if len(p4b):
        d = p4b.groupby(["panel", "n", "cadence"]).size()
        print(f"  DISTINCT (panel, anchor) cells behind them: {len(d)}")
        print(d.to_string())
        print("\n  per-leg failure counts over all 120 books:")
        for L in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
            print(f"    {L:7s} fails {int((~grid[L]).sum()):3d} of {len(grid)}")
        print("\n  passers (panel,n,cadence,gross -> CAGR/Sharpe/MaxDD, OOS):")
        for _, r in p4b.iterrows():
            print(f"    {r.panel:5s} N={r.n:<3d} {r.cadence} g={r.gross:.2f}  "
                  f"{r.CAGR:.2%}/{r.Sharpe:.4f}/{r.MaxDD:.2%}  "
                  f"halves {r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}")

    # ---------------------------------------------------------------- rule 8
    print("\n" + "=" * 78)
    print("(C) RULE 8 WALK-FORWARD — choose on <2017, read 2017-2026 ONCE")
    print("=" * 78)
    picks = []
    for pname in P:
        sub = grid[grid.panel == pname].copy()
        spy, lv = bench[pname], live[pname]
        so = metrics(spy.loc[OOS_START:])["Sharpe"]
        lo = metrics(lv.loc[OOS_START:])["Sharpe"]
        chs = {
            "CH_ISSHARPE (both dials free)": sub.loc[sub.IS_Sharpe.idxmax()],
            "CH_ISCALMAR (both dials free)": sub.loc[(sub.IS_CAGR / sub.IS_MaxDD.abs()).idxmax()],
            "CH_FIXG75 (anchor only, gross frozen 0.75)":
                sub[sub.gross == 0.75].loc[sub[sub.gross == 0.75].IS_Sharpe.idxmax()],
        }
        for cname, pk in chs.items():
            picks.append(dict(panel=pname, chooser=cname, n=pk.n, cadence=pk.cadence,
                              gross=pk.gross, IS_Sharpe=pk.IS_Sharpe,
                              OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                              OOS_MaxDD=pk.OOS_MaxDD, SPY_OOS_Sharpe=so,
                              LIVE_OOS_Sharpe=lo, beats_SPY_OOS=pk.OOS_Sharpe > so,
                              PASS_4b=pk.PASS_4b, PASS_4a=pk.PASS_4a))
            print(f"  {pname:5s} {cname:44s} -> N={pk.n:<3d} {pk.cadence} g={pk.gross:.2f}  "
                  f"OOS {pk.OOS_CAGR:.2%}/{pk.OOS_Sharpe:.4f}/{pk.OOS_MaxDD:.2%}  "
                  f"(SPY OOS {so:.4f}, LIVE OOS {lo:.4f})  4b={pk.PASS_4b} 4a={pk.PASS_4a}")
    pk = pd.DataFrame(picks); pk.to_csv(f"{OUT}.picks.csv", index=False)
    print(f"\n  picks beating SPY OOS: {int(pk.beats_SPY_OOS.sum())} of {len(pk)};  "
          f"4b {int(pk.PASS_4b.sum())} of {len(pk)};  4a {int(pk.PASS_4a.sum())} of {len(pk)}")
    # does the gross dial change the pick at all?
    same = 0
    for pname in P:
        a = pk[(pk.panel == pname) & (pk.chooser.str.startswith("CH_ISSHARPE"))].iloc[0]
        b = pk[(pk.panel == pname) & (pk.chooser.str.startswith("CH_FIXG75"))].iloc[0]
        same += int((a.n == b.n) and (a.cadence == b.cadence))
        print(f"  {pname:5s} freeing the gross dial moves the ANCHOR: "
              f"{'NO' if (a.n == b.n and a.cadence == b.cadence) else 'YES'};  "
              f"OOS Sharpe {a.OOS_Sharpe:.4f} (free) vs {b.OOS_Sharpe:.4f} (frozen), "
              f"delta {a.OOS_Sharpe - b.OOS_Sharpe:+.4f}")
    print(f"  anchor unchanged by freeing gross at {same} of {len(P)} panels")

    # ---------------------------------------------------------------- gates
    print("\n" + "=" * 78)
    print("GATES")
    print("=" * 78)
    for name, val, ok in gates:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val:.6g}")
    pd.DataFrame([dict(gate=n, value=v, passed=o) for n, v, o in gates]).to_csv(
        f"{OUT}.gates.csv", index=False)
    print(f"\n  {sum(o for _, _, o in gates)} of {len(gates)} gates pass")
    print("\nSURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the "
          "current output of a sub-$2B screen less the documented max_1d_move>=1.0 exclusion. "
          "Every CAGR and drawdown LEVEL is optimistic and every 4a/4b count is an UPPER bound. "
          "The bias largely cancels out of a RUNG SPREAD, which ranks one construction against "
          "itself on one tape, but it does NOT cancel out of the rule-8 OOS levels.")

if __name__ == "__main__":
    main()
