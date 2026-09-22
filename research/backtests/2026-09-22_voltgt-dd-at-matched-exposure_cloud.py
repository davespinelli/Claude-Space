#!/usr/bin/env python3
"""Idea 1537 (lane cloud, 2026-09-22): is VOL-TARGETING the ONE device that BUYS
DRAWDOWN at MATCHED EXPOSURE?

Idea 1534 pooled six device families against their own matched-exposure de-gross twins
and found VOLTGT the only family with a POSITIVE pooled dMaxDD (+0.97 pp, against BAND
-0.56, MADIST -0.54, MAXVOL -0.53, SPYFILT -1.40, STOP -7.23) while paying -0.56 pp/yr of
CAGR.  That finding rests on FIVE rungs on one cadence.  This run re-cuts VOLTGT alone on
a FINER ladder, bootstraps the dMaxDD with the same LB = 65 blocks, and asks the question
the queue line actually poses: does ANY rung clear 4b OUT OF SAMPLE while its own anchor
does not?

CONSTRUCTION (frozen from 1534 so the numbers are commensurable)
  BASE: top-N by H-day momentum among names above their 200d MA with vol20 < 0.60, equal
  weight at gross 0.75, weekly, t+1.  (N, H) = (20, 126), FROZEN at the committed anchor,
  not searched here.
  DEVICE VOLTGT(v): base weights multiplied by min(1, v / rv_t), rv_t = 20d realised vol of
  the BASE book's own returns, annualised.  Causal: decided at close t, applied at t+1 by
  the engine.
  ANCHOR: the SAME base book scaled by a CONSTANT k chosen so its REALISED mean gross
  equals the device's realised mean gross (Newton corrections; achieved match = gate G1).

  TUNED PARAMETERS: exactly two, VOL TARGET v and PANEL.  Cost rung and cadence are
  REPORTED, not tuned, and every grid point is published.

  LADDER: v in 0.06 .. 0.30 step 0.02 (13 rungs) -- finer and wider than 1534's five.
  PANELS: U56, B136, SMALL (survivorship-screened, see below).
  COSTS:  0 / 10 / 25 / 50 bps, reconstructed EXACTLY from each book's own zero-cost
          return and turnover series (the engine never feeds cost back into positions),
          verified against a direct engine run as gate G2.

  PAIRED STATISTIC  d = stat(device) - stat(anchor) for Sharpe / CAGR / MaxDD, with an SE
  from a CIRCULAR BLOCK BOOTSTRAP (LB = 65 trading days, B = 500), the SAME blocks drawn
  for every book and every panel in a replicate so cross-book dependence is carried.

  RULE 8: v chosen on the FIRST HALF only (IS = ... 2016-12-31), evaluated on 2017-2026,
  which is read ONCE at the end.

SURVIVORSHIP CAVEAT: the SMALL panel is CURRENT constituents of a sub-$2B screen (see
data/SMALL_PANEL_README.md).  It is survivorship-biased upward and its absolute levels are
not investable; it is used here only as a THIRD panel for the direction of the effect.
Tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped first.

Run: python3 research/backtests/2026-09-22_voltgt-dd-at-matched-exposure_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                      # noqa
from engine import backtest                                               # noqa

SEED      = 20260922
N_FROZEN  = 20
H_FROZEN  = 126
GROSS     = 0.75
MAXVOL    = 0.60
FREQ      = "W"
WARMUP    = 260
OOS_START = pd.Timestamp("2017-01-01")
IS_END    = pd.Timestamp("2016-12-31")
LB        = 65
NBOOT     = 500
COSTS     = [0, 10, 25, 50]
HEADLINE  = 10                       # PROTOCOL rule 2's binding rung
LADDER    = [round(0.06 + 0.02 * i, 2) for i in range(13)]
L1534     = [0.08, 0.10, 0.12, 0.15, 0.20]     # 1534's own five rungs, for gate G3
OUT       = ROOT / "research" / "backtests" / "2026-09-22_voltgt-dd-at-matched-exposure_cloud"

# ---------------------------------------------------------------- panels
def panels():
    out = {}
    out["U56"]  = load_universe()
    out["B136"] = load_universe(broad=True)
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    out["SMALL"] = px[keep]
    return out

# ---------------------------------------------------------------- books
def base_weights(px):
    mom   = px / px.shift(H_FROZEN) - 1
    ma200 = px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig  = mom.where((px > ma200) & (vol20 < MAXVOL))
    rank  = elig.rank(axis=1, ascending=False)
    return (rank <= N_FROZEN).astype(float) * (GROSS / N_FROZEN)

def run0(px, w):
    """Backtest at ZERO cost; returns (gross-of-cost returns, turnover, mean realised gross),
    all truncated at the warm-up row.  Any cost rung is r0 - turnover * bps/1e4 exactly."""
    res   = backtest(px, w, cost_bps=0.0, freq=FREQ)
    start = px.index[WARMUP]
    return (res["returns"].loc[start:], res["turnover"].loc[start:],
            res["weights"].sum(axis=1).loc[start:].mean())

def at_cost(r0, to, bps):
    return r0 - to * bps / 1e4

def voltgt_scalar(base_r, index, v):
    rv = base_r.rolling(20).std() * np.sqrt(252)
    s  = (v / rv.replace(0, np.nan)).clip(upper=1.0)
    return s.reindex(index).fillna(1.0)

def matched_anchor(px, base_w, g_target, k0, iters=2):
    """Base book scaled by a constant k so realised mean gross == g_target."""
    k = k0
    for _ in range(iters):
        r0, to, g = run0(px, base_w * k)
        if g <= 0: break
        k = k * g_target / g
    r0, to, g = run0(px, base_w * k)
    return r0, to, g, k

# ---------------------------------------------------------------- metrics
def sharpe(r): s = r.std(); return r.mean() * 252 / (s * np.sqrt(252)) if s > 0 else np.nan
def maxdd(r):  e = (1 + r).cumprod(); return (e / e.cummax() - 1).min()
def cagr(r):   e = (1 + r).cumprod(); return e.iloc[-1] ** (252 / len(r)) - 1

def full_metrics(r):
    h = len(r) // 2
    o = r.loc[OOS_START:]
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]),
                OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o))

def keep_paths(m, base_m, spy_m):
    """4a: Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse.
       4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    a = (m["H1"] > base_m["H1"]) and (m["H2"] > base_m["H2"]) and (m["MaxDD"] >= base_m["MaxDD"])
    b = (m["H1"] > spy_m["H1"]) and (m["H2"] > spy_m["H2"]) and (m["OOS_Sharpe"] > spy_m["OOS_Sharpe"]) \
        and (m["MaxDD"] >= 0.60 * spy_m["MaxDD"]) and (m["CAGR"] >= 0.70 * spy_m["CAGR"])
    return a, b

def keep_4b_oos(m, spy_m):
    """4b restricted to the OOS leg alone (rule 8's own window), for the queue's question."""
    return (m["OOS_Sharpe"] > spy_m["OOS_Sharpe"]) and (m["OOS_MaxDD"] >= 0.60 * spy_m["OOS_MaxDD"]) \
        and (m["OOS_CAGR"] >= 0.70 * spy_m["OOS_CAGR"])

# ---------------------------------------------------------------- bootstrap
def block_starts(rng, n, nb):
    return rng.integers(0, n, size=(NBOOT, nb))

def boot_paired(dev_r, anc_r, starts, n):
    """Circular-block bootstrap of the PAIRED differences in Sharpe / CAGR / MaxDD."""
    dv, av = dev_r.values, anc_r.values
    nb = starts.shape[1]
    out = np.empty((NBOOT, 3))
    idx_base = np.arange(LB)
    for b in range(NBOOT):
        idx = ((starts[b][:, None] + idx_base[None, :]).ravel() % n)[:n]
        d, a = dv[idx], av[idx]
        sd = d.std(); sa = a.std()
        s_d = d.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan
        s_a = a.mean() * 252 / (sa * np.sqrt(252)) if sa > 0 else np.nan
        ed = np.cumprod(1 + d); ea = np.cumprod(1 + a)
        c_d = ed[-1] ** (252 / n) - 1; c_a = ea[-1] ** (252 / n) - 1
        m_d = (ed / np.maximum.accumulate(ed) - 1).min()
        m_a = (ea / np.maximum.accumulate(ea) - 1).min()
        out[b] = (s_d - s_a, c_d - c_a, m_d - m_a)
    return out

# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    P = panels()
    grid, gates, boots, wf = [], [], [], []

    # ---- per-panel comparands
    store = {}
    for pname, px in P.items():
        base_w = base_weights(px)
        b_r0, b_to, b_g = run0(px, base_w)
        start = px.index[WARMUP]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        v2_r0, v2_to = v2["returns"].loc[start:], v2["turnover"].loc[start:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        store[pname] = dict(px=px, base_w=base_w, b_r0=b_r0, b_to=b_to, b_g=b_g,
                            v2_r0=v2_r0, v2_to=v2_to, spy=spy, start=start)
        print(f"[{pname}] rows={len(b_r0)} {start.date()}..{px.index[-1].date()} "
              f"base mean gross={b_g:.4f}  ({time.time()-t0:.0f}s)")

    # ---- gate G2: cost reconstruction is exact
    for pname in P:
        s = store[pname]
        direct = backtest(s["px"], s["base_w"], cost_bps=HEADLINE, freq=FREQ)["returns"].loc[s["start"]:]
        err = float(np.abs(direct.values - at_cost(s["b_r0"], s["b_to"], HEADLINE).values).max())
        gates.append(dict(gate="G2_cost_reconstruction", panel=pname, value=err, tol=1e-12,
                          ok=bool(err < 1e-12)))
        print(f"  G2 {pname}: cost reconstruction max err {err:.3e}")

    # ---- the ladder
    n_common = None
    for pname in P:
        s = store[pname]
        px, base_w = s["px"], s["base_w"]
        base_r10 = at_cost(s["b_r0"], s["b_to"], HEADLINE)          # frozen convention
        for v in sorted(set(LADDER) | set(L1534)):
            sc = voltgt_scalar(base_r10, base_w.index, v)
            d_r0, d_to, d_g = run0(px, base_w.mul(sc, axis=0))
            a_r0, a_to, a_g, k = matched_anchor(px, base_w, d_g, k0=d_g / s["b_g"])
            gates.append(dict(gate="G1_gross_match", panel=pname, value=abs(d_g - a_g),
                              tol=5e-4, ok=bool(abs(d_g - a_g) < 5e-4), v=v))
            for c in COSTS:
                dr, ar = at_cost(d_r0, d_to, c), at_cost(a_r0, a_to, c)
                b_r, v2_r = at_cost(s["b_r0"], s["b_to"], c), at_cost(s["v2_r0"], s["v2_to"], c)
                md, ma, mb, mv2 = full_metrics(dr), full_metrics(ar), full_metrics(b_r), full_metrics(v2_r)
                msp = full_metrics(s["spy"])
                d4a, d4b = keep_paths(md, mv2, msp)
                a4a, a4b = keep_paths(ma, mv2, msp)
                row = dict(panel=pname, v=v, cost_bps=c, k_anchor=k,
                           dev_gross=d_g, anc_gross=a_g, base_gross=s["b_g"],
                           dev_turnover=float(d_to.sum() / (len(dr) / 252)),
                           anc_turnover=float(a_to.sum() / (len(ar) / 252)),
                           in_1534_ladder=v in L1534, in_fine_ladder=v in LADDER)
                for pre, m in (("dev", md), ("anc", ma), ("base", mb), ("v2", mv2), ("spy", msp)):
                    for kk, vv in m.items(): row[f"{pre}_{kk}"] = vv
                row.update(dev_4a=d4a, dev_4b=d4b, anc_4a=a4a, anc_4b=a4b,
                           dev_4b_oos=keep_4b_oos(md, msp), anc_4b_oos=keep_4b_oos(ma, msp),
                           dSharpe=md["Sharpe"] - ma["Sharpe"], dCAGR=md["CAGR"] - ma["CAGR"],
                           dMaxDD=md["MaxDD"] - ma["MaxDD"],
                           dOOS_Sharpe=md["OOS_Sharpe"] - ma["OOS_Sharpe"],
                           dOOS_MaxDD=md["OOS_MaxDD"] - ma["OOS_MaxDD"])
                grid.append(row)
            store.setdefault("series", {})[(pname, v)] = (d_r0, d_to, a_r0, a_to)
            if n_common is None: n_common = len(d_r0)
        print(f"[{pname}] ladder done ({time.time()-t0:.0f}s)")

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---- gate G4: an unbinding target reproduces the base book
    for pname in P:
        s = store[pname]
        sc = voltgt_scalar(at_cost(s["b_r0"], s["b_to"], HEADLINE), s["base_w"].index, 9.99)
        r0, to, g = run0(s["px"], s["base_w"].mul(sc, axis=0))
        err = float(np.abs(r0.values - s["b_r0"].values).max())
        gates.append(dict(gate="G4_unbinding_target_is_base", panel=pname, value=err, tol=1e-12,
                          ok=bool(err < 1e-12)))
        print(f"  G4 {pname}: v=9.99 vs base max err {err:.3e}")

    # ---- bootstrap on the headline rung set (shared blocks across books and panels)
    SER = store["series"]
    pairs = {k: (at_cost(v[0], v[1], HEADLINE), at_cost(v[2], v[3], HEADLINE)) for k, v in SER.items()}
    n  = min(len(a) for a, _ in pairs.values())
    nb = int(np.ceil(n / LB))
    starts = block_starts(rng, n, nb)
    for (pname, v), (dr, ar) in pairs.items():
        B = boot_paired(dr.iloc[-n:], ar.iloc[-n:], starts, n)
        rowpt = G[(G.panel == pname) & (G.v == v) & (G.cost_bps == HEADLINE)].iloc[0]
        se_dd = B[:, 2].std()
        boots.append(dict(panel=pname, v=v,
                          dSharpe=rowpt["dSharpe"], se_dSharpe=B[:, 0].std(),
                          dCAGR=rowpt["dCAGR"],     se_dCAGR=B[:, 1].std(),
                          dMaxDD=rowpt["dMaxDD"],   se_dMaxDD=se_dd,
                          t_dMaxDD=rowpt["dMaxDD"] / se_dd if se_dd > 0 else np.nan,
                          lo_dMaxDD=np.percentile(B[:, 2], 2.5), hi_dMaxDD=np.percentile(B[:, 2], 97.5),
                          lo_dSharpe=np.percentile(B[:, 0], 2.5), hi_dSharpe=np.percentile(B[:, 0], 97.5)))
    Bdf = pd.DataFrame(boots).sort_values(["panel", "v"])
    Bdf.to_csv(f"{OUT}.bootstrap.csv", index=False)

    # ---- gate G3: 1534's pooled VOLTGT dMaxDD on its own five rungs
    sub = G[(G.cost_bps == HEADLINE) & (G.in_1534_ladder)]
    g3 = float(sub["dMaxDD"].mean() * 100)
    gates.append(dict(gate="G3_1534_pooled_dMaxDD_pp", panel="POOLED", value=g3, tol=None,
                      ok=bool(g3 > 0), note="1534 published +0.97 pp on the same five rungs"))
    print(f"  G3 pooled dMaxDD on 1534's five rungs @10bps: {g3:+.2f} pp (1534 published +0.97 pp)")

    # ---- RULE 8 (2017-2026 read ONCE): v chosen on the FIRST HALF only, per cost rung
    for pname in P:
        s_ = store[pname]
        msp = full_metrics(s_["spy"])
        for c in COSTS:
            best_v, best_is = None, -np.inf
            for v in LADDER:
                d_r0, d_to, a_r0, a_to = SER[(pname, v)]
                sv = sharpe(at_cost(d_r0, d_to, c).loc[:IS_END])
                if sv > best_is: best_is, best_v = sv, v
            d_r0, d_to, a_r0, a_to = SER[(pname, best_v)]
            dr, ar = at_cost(d_r0, d_to, c), at_cost(a_r0, a_to, c)
            md, ma = full_metrics(dr), full_metrics(ar)
            mv2 = full_metrics(at_cost(s_["v2_r0"], s_["v2_to"], c))
            mb  = full_metrics(at_cost(s_["b_r0"], s_["b_to"], c))
            k4a, k4b = keep_paths(md, mv2, msp)
            wf.append(dict(panel=pname, cost_bps=c, chosen_v=best_v, IS_Sharpe=best_is,
                           FULL_CAGR=md["CAGR"], FULL_Sharpe=md["Sharpe"], FULL_MaxDD=md["MaxDD"],
                           H1=md["H1"], H2=md["H2"],
                           OOS_CAGR=md["OOS_CAGR"], OOS_Sharpe=md["OOS_Sharpe"], OOS_MaxDD=md["OOS_MaxDD"],
                           anc_OOS_CAGR=ma["OOS_CAGR"], anc_OOS_Sharpe=ma["OOS_Sharpe"], anc_OOS_MaxDD=ma["OOS_MaxDD"],
                           base_OOS_Sharpe=mb["OOS_Sharpe"], base_OOS_MaxDD=mb["OOS_MaxDD"],
                           v2_OOS_CAGR=mv2["OOS_CAGR"], v2_OOS_Sharpe=mv2["OOS_Sharpe"], v2_OOS_MaxDD=mv2["OOS_MaxDD"],
                           spy_OOS_CAGR=msp["OOS_CAGR"], spy_OOS_Sharpe=msp["OOS_Sharpe"], spy_OOS_MaxDD=msp["OOS_MaxDD"],
                           dev_4a=k4a, dev_4b=k4b, dev_4b_oos=keep_4b_oos(md, msp),
                           anc_4b_oos=keep_4b_oos(ma, msp)))
    W = pd.DataFrame(wf); W.to_csv(f"{OUT}.walkforward.csv", index=False)
    Gt = pd.DataFrame(gates); Gt.to_csv(f"{OUT}.gates.csv", index=False)

    # ---- summary
    fine = G[G.in_fine_ladder]
    print("\n=== GRID:", len(G), "published cells;", len(fine), "on the fine ladder ===")
    print("\n-- dMaxDD (device minus matched anchor, pp) by panel x cost, fine ladder --")
    print((fine.pivot_table(index="panel", columns="cost_bps", values="dMaxDD") * 100).round(3).to_string())
    print("\n-- dSharpe / dCAGR(pp) pooled by cost --")
    print(fine.groupby("cost_bps")[["dSharpe", "dCAGR", "dMaxDD"]].mean().to_string())
    print("\n-- KEEP counts on the fine ladder --")
    print(fine.groupby(["panel", "cost_bps"])[["dev_4a", "dev_4b", "anc_4a", "anc_4b",
                                               "dev_4b_oos", "anc_4b_oos"]].sum().to_string())
    print("\nTHE QUEUE'S QUESTION -- rungs clearing 4b-OOS where their OWN anchor does not:")
    q = fine[(fine.dev_4b_oos) & (~fine.anc_4b_oos)]
    print(f"  {len(q)} of {len(fine)} cells" + ("" if len(q) == 0 else ""))
    if len(q): print(q[["panel", "v", "cost_bps", "dev_OOS_CAGR", "dev_OOS_Sharpe",
                        "dev_OOS_MaxDD", "anc_OOS_Sharpe", "anc_OOS_MaxDD"]].to_string(index=False))
    print("\n  reverse (anchor clears, device does not):",
          int(((~fine.dev_4b_oos) & (fine.anc_4b_oos)).sum()))
    print("\n-- BOOTSTRAP, headline 10 bps --")
    print(Bdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n-- RULE 8 (v chosen on ... 2016 only; 2017-2026 read once) --")
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n-- GATES --"); print(Gt.to_string(index=False))
    print(f"\ndone in {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
