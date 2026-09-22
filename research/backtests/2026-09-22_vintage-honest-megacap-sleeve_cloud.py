#!/usr/bin/env python3
"""Idea 934 (lane cloud, 2026-09-22): does the SINGLE20 LOOK-AHEAD survive a VINTAGE-HONEST
mega-cap list?

Idea 924 found that 80% of the mega-cap sleeve's edge is NAME SELECTION: `SINGLE20/EW` beats
SPY by +0.3708 of Sharpe in the leg window (2009-01-13 .. 2013-01-07), of which +0.0750 is
weighting/size (RSP, a TRADED equal-weight S&P 500, beats SPY by that much) and the remaining
**+0.2958 is name selection** — and `universe.json:megacap` is the list of the 20 largest US
companies AS OF 2026, held from 2008.  That is an answer key, not a rule.

THIS RUN rebuilds the sleeve from data available at each rebalance and asks how much of the
+0.2958 survives.  The contrast is 924's own: SELECTION(sleeve) = Sharpe(sleeve) - Sharpe(RSP)
in the leg window, RSP carrying the weighting/size channel.

TWO TUNED PARAMETERS (the queue's own), every level reported:
  TUNED 1  RANKING VARIABLE, 4 levels, all computed from prices up to t only:
             MOM12_1   px.shift(21)/px.shift(252) - 1          (12-1 momentum)
             GROWTH3Y  px/px.shift(756) - 1                    (trailing 3y compounding —
                       the price-only proxy for "has BECOME one of the biggest")
             IVOL60    1 / 60d realised vol                    (low-vol)
             TREND200  px / 200d MA - 1                        (trend strength)
  TUNED 2  LIST SIZE k, 4 levels: 10, 20, 30, 40.

REPORTED CONSTANTS (not tuned): gross 0.75, weekly cadence, t+1 execution, 260-day warm-up,
costs 10 bps headline plus 25 and 50, IS/OOS split 2016-12-31 (924's own), windows LEG / FULL /
IS / OOS.  SELECTION POOL, 2 levels, both reported, the first pre-registered as primary:
  POOL100  the 100 SINGLE NAMES of research/universe_broad.json (136 minus its 36 ETFs), each
           eligible only once it has 252 prior closes — the honest arm.
  POOL20   `universe.json:megacap` itself — a DIAGNOSTIC that isolates TIMING inside the answer
           key from the choice of names, not an honest arm.

ARMS: ANSWERKEY20 (924's sleeve, the look-ahead), VINTAGE(rank, k), POOL100EW (no selection at
all), RSP, SPY, the live RULES v2 book, and TWO placebos, because they are not the same null:
  RANDFIX(k)  k names drawn ONCE from the pool eligible at the warm-up date and HELD — the
              like-for-like null for the answer key, which is also a fixed list held from 2008.
  RANDROT(k)  a fresh pseudo-random draw every rebalance — a ROTATING null whose handicap is
              TURNOVER, not selection (idea 1050's finding).  Reported, with its turnover, so
              the two are never confused.
Both are 10 md5 seeds; mean and sd reported.

BOTH KEEP PATHS (4a vs live RULES v2, 4b vs SPY) and PROTOCOL rule 8 (choose the ranking
variable and k on IS only, read OOS untouched) are run on every arm.

SURVIVORSHIP, STATED LOUDLY: the selection POOL is itself a 2026 constituent list.  A
vintage-honest RANKING inside a survivorship-selected pool removes the "which 20 of these are
biggest" answer key but NOT the "which 100 names are still listed and large in 2026" one.  So
every number here is an UPPER BOUND on what a 2009 investor could have had, and the honest
reading is a CEILING: whatever the vintage rule fails to retain, it could not have retained.
RSP and SPY are traded instruments and carry no survivorship bias, which is why the headline
contrast is taken against RSP.
"""
import hashlib, itertools, json, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
GROSS, FREQ, WARMUP = 0.75, "W", 260
KS = [10, 20, 30, 40]
RANKS = ["MOM12_1", "GROWTH3Y", "IVOL60", "TREND200"]
COSTS = [10.0, 25.0, 50.0]
LEG = ("2009-01-13", "2013-01-07")
SPLIT = "2016-12-31"
NSEED = 10


def rank_frame(px, kind):
    if kind == "MOM12_1":  return px.shift(21) / px.shift(252) - 1
    if kind == "GROWTH3Y": return px / px.shift(756) - 1
    if kind == "IVOL60":   return 1.0 / px.pct_change().rolling(60).std().clip(lower=1e-6)
    if kind == "TREND200": return px / px.rolling(200).mean() - 1
    raise ValueError(kind)


def eligible(px, pool):
    """A name is eligible at t once it has 252 prior closes and is priced at t."""
    have = px[pool].notna()
    return have & (have.rolling(252).sum() >= 252)


def ew_weights(sel, cols, index, gross=GROSS):
    w = pd.DataFrame(0.0, index=index, columns=cols)
    n = sel.sum(axis=1).replace(0, np.nan)
    w[sel.columns] = (sel.astype(float)).div(n, axis=0).fillna(0.0) * gross
    return w


def topk_sel(px, pool, kind, k):
    el = eligible(px, pool)
    r = rank_frame(px[pool], kind).where(el)
    rk = r.rank(axis=1, ascending=False, na_option="bottom")
    return (rk <= k) & el


def rand_sel(px, pool, k, seed):
    """ROTATING placebo: a fresh pseudo-random draw every day, md5-seeded.  Its handicap is
    turnover (idea 1050), which is why RANDFIX below exists alongside it."""
    el = eligible(px, pool)
    rs = np.random.RandomState(int(hashlib.md5(f"934-{seed}-{k}".encode()).hexdigest()[:8], 16))
    noise = pd.DataFrame(rs.rand(len(px), len(pool)), index=px.index, columns=pool)
    rk = noise.where(el).rank(axis=1, ascending=False, na_option="bottom")
    return (rk <= k) & el


def randfix_sel(px, pool, k, seed, asof):
    """FIXED placebo: draw k names ONCE from the pool eligible at `asof` and hold them — the
    like-for-like null for a hand-picked list held from 2008."""
    el = eligible(px, pool)
    avail = [c for c in pool if bool(el.loc[asof, c])]
    rs = np.random.RandomState(int(hashlib.md5(f"934fix-{seed}-{k}".encode()).hexdigest()[:8], 16))
    pick = list(rs.choice(avail, size=min(k, len(avail)), replace=False))
    sel = pd.DataFrame(False, index=px.index, columns=pool)
    sel[pick] = px[pick].notna()
    return sel & el


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def windows(r):
    return {"FULL": r, "LEG": r.loc[LEG[0]:LEG[1]], "IS": r.loc[:SPLIT], "OOS": r.loc[SPLIT:].iloc[1:]}


def run(px, w, cost):
    return backtest(px, w, cost_bps=cost, freq=FREQ)


def turn_yr(res, start):
    t = res["turnover"].loc[start:]
    return float(t.sum() / (len(t) / 252))


def main():
    px = load_universe(broad=True)
    B = json.loads((ROOT / "research" / "universe_broad.json").read_text())
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    POOL100 = sorted(set(B) - etfs)
    POOL20 = sorted(U["megacap"])
    POOLS = {"POOL100": POOL100, "POOL20": POOL20}
    start = px.index[WARMUP]
    idx, cols = px.index, px.columns

    # ---------------- references
    refs, refturn = {}, {}
    for cost in COSTS:
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        rsp = px["RSP"].pct_change().fillna(0.0).loc[start:]
        live = run(px, rules_v2_weights(px), cost)["returns"].loc[start:]
        ak = ew_weights(pd.DataFrame(True, index=idx, columns=POOL20).where(px[POOL20].notna(), False), cols, idx)
        akr = run(px, ak, cost)["returns"].loc[start:]
        p100 = ew_weights(eligible(px, POOL100), cols, idx)
        p100r = run(px, p100, cost)["returns"].loc[start:]
        refs[cost] = dict(SPY=spy, RSP=rsp, LIVE=live, ANSWERKEY20=akr, POOL100EW=p100r)
        refturn[(cost, "ANSWERKEY20")] = turn_yr(run(px, ak, cost), start)
        refturn[(cost, "POOL100EW")] = turn_yr(run(px, p100, cost), start)
        refturn[(cost, "LIVE")] = turn_yr(run(px, rules_v2_weights(px), cost), start)

    # ---------------- gates
    gates = []
    sel_ak = pd.DataFrame(True, index=idx, columns=POOL20).where(px[POOL20].notna(), False)
    w_ak = ew_weights(sel_ak, cols, idx)
    gates.append(dict(gate="G1 pool partition: 136 = 100 singles + 36 ETFs",
                      value=float(len(POOL100) + len(set(B) & etfs)), ok=len(POOL100) == 100 and len(set(B) & etfs) == 36))
    gates.append(dict(gate="G2 ANSWERKEY20 == universe.json:megacap, 20 names", value=float(len(POOL20)), ok=len(POOL20) == 20))
    gates.append(dict(gate="G3 max gross of any sleeve target", value=float(w_ak.sum(axis=1).max()), ok=w_ak.sum(axis=1).max() <= GROSS + 1e-12))
    s = topk_sel(px, POOL100, "MOM12_1", 20)
    gates.append(dict(gate="G4 top-k selects exactly k once warm (median count)", value=float(s.loc[start:].sum(axis=1).median()), ok=s.loc[start:].sum(axis=1).median() == 20))
    r_ = rank_frame(px[POOL100], "MOM12_1")
    gates.append(dict(gate="G5 ranking uses no same-day price (corr of MOM with same-day return)",
                      value=float(np.nan_to_num(np.corrcoef(r_["AAPL"].loc[start:].fillna(0), px["AAPL"].pct_change().loc[start:].fillna(0))[0, 1])), ok=True))
    lk = {k: stats(v.loc[LEG[0]:LEG[1]]) for k, v in refs[10.0].items()}
    gates.append(dict(gate="G6 CROSS-RUN 924 leg window: SINGLE20/EW - SPY (published +0.3708)",
                      value=float(lk["ANSWERKEY20"]["Sharpe"] - lk["SPY"]["Sharpe"]), ok=True))
    gates.append(dict(gate="G7 CROSS-RUN 924 leg window: RSP - SPY (published +0.0750)",
                      value=float(lk["RSP"]["Sharpe"] - lk["SPY"]["Sharpe"]), ok=True))
    gates.append(dict(gate="G8 CROSS-RUN 924 leg window: SELECTION = SINGLE20 - RSP (published +0.2958)",
                      value=float(lk["ANSWERKEY20"]["Sharpe"] - lk["RSP"]["Sharpe"]), ok=True))
    gates.append(dict(gate="G9 leg window length in days (924: 1003)", value=float(len(refs[10.0]["SPY"].loc[LEG[0]:LEG[1]])), ok=True))
    gates.append(dict(gate="G10 eligible pool size at the leg window start (POOL100)",
                      value=float(eligible(px, POOL100).loc[LEG[0]].sum()), ok=True))
    gates.append(dict(gate="G11 eligible pool size at the last date (POOL100)",
                      value=float(eligible(px, POOL100).iloc[-1].sum()), ok=True))
    G = pd.DataFrame(gates); G.to_csv(f"{OUT}.gates.csv", index=False)
    print("=== GATES (pre-registered, printed before any hypothesis) ===")
    print(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"{int(G.ok.sum())} of {len(G)} structural gates PASS; G5-G11 are readings, printed not barred\n")

    # ---------------- grid
    rows = []

    def emit(arm, pool, rank, k, cost, r, seed=np.nan, turn=np.nan):
        d = {}
        for wname, rr in windows(r).items():
            s = stats(rr)
            d.update({f"{wname}_{a}": s[a] for a in ("CAGR", "Sharpe", "MaxDD")})
            if wname == "FULL":
                d.update(H1=s["H1"], H2=s["H2"])
        ref = refs[cost]
        rs = {w: stats(v) for w, v in windows(ref["RSP"]).items()}
        sp = {w: stats(v) for w, v in windows(ref["SPY"]).items()}
        lv = {w: stats(v) for w, v in windows(ref["LIVE"]).items()}
        d["SEL_LEG"] = d["LEG_Sharpe"] - rs["LEG"]["Sharpe"]
        d["SEL_FULL"] = d["FULL_Sharpe"] - rs["FULL"]["Sharpe"]
        d["SEL_OOS"] = d["OOS_Sharpe"] - rs["OOS"]["Sharpe"]
        d["keep4a"] = bool(d["H1"] > lv["FULL"]["H1"] and d["H2"] > lv["FULL"]["H2"] and d["FULL_MaxDD"] >= lv["FULL"]["MaxDD"])
        d["keep4b"] = bool(d["H1"] > sp["FULL"]["H1"] and d["H2"] > sp["FULL"]["H2"]
                           and d["OOS_Sharpe"] > sp["OOS"]["Sharpe"]
                           and d["FULL_MaxDD"] >= 0.60 * sp["FULL"]["MaxDD"]
                           and d["FULL_CAGR"] >= 0.70 * sp["FULL"]["CAGR"])
        rows.append(dict(arm=arm, pool=pool, rank=rank, k=k, cost_bps=cost, seed=seed, turn_yr=turn, **d))

    for cost in COSTS:
        for lab, r in refs[cost].items():
            emit("REFERENCE", "", lab, np.nan, cost, r, turn=refturn.get((cost, lab), np.nan))
        for pool_name, pool in POOLS.items():
            for rank, k in itertools.product(RANKS, KS):
                if pool_name == "POOL20" and k >= 20:
                    continue                       # k >= |pool| is the answer key itself
                w = ew_weights(topk_sel(px, pool, rank, k), cols, idx)
                res = run(px, w, cost)
                emit("VINTAGE", pool_name, rank, k, cost, res["returns"].loc[start:], turn=turn_yr(res, start))
        print(f"cost {cost:g} bps: vintage arms done")

    for k in KS:                                    # placebos, 10 bps only
        for seed in range(NSEED):
            w = ew_weights(randfix_sel(px, POOL100, k, seed, start), cols, idx)
            res = run(px, w, 10.0)
            emit("RANDFIX", "POOL100", "RANDFIX", k, 10.0, res["returns"].loc[start:], seed=seed, turn=turn_yr(res, start))
            w = ew_weights(rand_sel(px, POOL100, k, seed), cols, idx)
            res = run(px, w, 10.0)
            emit("RANDROT", "POOL100", "RANDROT", k, 10.0, res["returns"].loc[start:], seed=seed, turn=turn_yr(res, start))
    print("placebo arms done")

    D = pd.DataFrame(rows); D.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------- rule 8: choose (rank, k) on IS only
    wf = []
    for cost in COSTS:
        for pool_name in POOLS:
            cand = D[(D.arm == "VINTAGE") & (D.pool == pool_name) & (D.cost_bps == cost)]
            if not len(cand): continue
            pick = cand.loc[cand.IS_Sharpe.idxmax()]
            ref = refs[cost]
            wf.append(dict(pool=pool_name, cost_bps=cost, pick_rank=pick["rank"], pick_k=pick["k"],
                           IS_Sharpe=pick["IS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                           OOS_MaxDD=pick["OOS_MaxDD"], SEL_OOS=pick["SEL_OOS"],
                           ak_OOS_Sharpe=stats(windows(ref["ANSWERKEY20"])["OOS"])["Sharpe"],
                           ak_SEL_OOS=stats(windows(ref["ANSWERKEY20"])["OOS"])["Sharpe"] - stats(windows(ref["RSP"])["OOS"])["Sharpe"],
                           rsp_OOS_Sharpe=stats(windows(ref["RSP"])["OOS"])["Sharpe"],
                           spy_OOS_Sharpe=stats(windows(ref["SPY"])["OOS"])["Sharpe"],
                           live_OOS_Sharpe=stats(windows(ref["LIVE"])["OOS"])["Sharpe"],
                           spy_OOS_CAGR=stats(windows(ref["SPY"])["OOS"])["CAGR"],
                           live_OOS_CAGR=stats(windows(ref["LIVE"])["OOS"])["CAGR"],
                           keep4a=pick["keep4a"], keep4b=pick["keep4b"]))
    WF = pd.DataFrame(wf); WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    c = ["arm", "pool", "rank", "k", "turn_yr", "FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD", "H1", "H2",
         "LEG_Sharpe", "SEL_LEG", "IS_Sharpe", "OOS_Sharpe", "SEL_OOS", "keep4a", "keep4b"]
    print("\n=== REFERENCES, 10 bps ===")
    print(D[(D.arm == "REFERENCE") & (D.cost_bps == 10)][c].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n=== VINTAGE GRID, 10 bps, every level reported ===")
    print(D[(D.arm == "VINTAGE") & (D.cost_bps == 10)][c].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n=== VINTAGE GRID, 25 and 50 bps ===")
    print(D[(D.arm == "VINTAGE") & (D.cost_bps != 10)][["cost_bps"] + c].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for placebo in ("RANDFIX", "RANDROT"):
        print(f"\n=== PLACEBO {placebo} (POOL100, 10 bps): mean / sd over 10 md5 seeds ===")
        R = D[D.arm == placebo].groupby("k")[["LEG_Sharpe", "SEL_LEG", "FULL_Sharpe", "OOS_Sharpe", "SEL_OOS", "turn_yr"]].agg(["mean", "std"])
        print(R.to_string(float_format=lambda x: f"{x:.4f}"))
    print("\n=== RETENTION of 924's +0.2958 selection edge (LEG window, 10 bps) ===")
    ak = D[(D.arm == "REFERENCE") & (D["rank"] == "ANSWERKEY20") & (D.cost_bps == 10)].iloc[0]
    print(f"ANSWERKEY20 SEL_LEG = {ak.SEL_LEG:+.4f}  (924 published +0.2958)")
    v = D[(D.arm == "VINTAGE") & (D.cost_bps == 10)].copy()
    v["retention"] = v.SEL_LEG / ak.SEL_LEG
    print(v[["pool", "rank", "k", "SEL_LEG", "retention", "SEL_FULL", "SEL_OOS"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n=== RULE 8 WALK-FORWARD (rank and k chosen on IS only) ===")
    print(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n=== KEEP counts (VINTAGE arms) ===")
    print(D[D.arm == "VINTAGE"].groupby(["pool", "cost_bps"])[["keep4a", "keep4b"]].sum().to_string())
    print("\n=== ANSWERKEY20 as a book, every cost ===")
    print(D[(D.arm == "REFERENCE") & (D["rank"].isin(["ANSWERKEY20", "SPY", "RSP", "LIVE", "POOL100EW"]))][["rank", "cost_bps"] + c[4:]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()
