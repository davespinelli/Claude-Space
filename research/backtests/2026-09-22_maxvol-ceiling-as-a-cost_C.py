#!/usr/bin/env python3
"""Idea 1541 (lane C, 2026-09-22): IS THE MAXVOL CEILING ITSELF A COST?

Idea 1534's rule-8 chooser picked the LOOSEST MAXVOL rung (m = 0.80) on BOTH U56 and
B136, and that book beat the frozen BASE on full Sharpe (+0.0334 / +0.0640) and on OOS
on B136 (+0.0626).  The ceiling m = 0.60 is an UNPRICED INHERITANCE: it is a literal
parameter of `baseline.rules_v1_weights` (`max_vol=0.60`), it is carried by the record's
frozen top-N momentum BASE, and it was never laddered in its own right -- 1534 only ever
TIGHTENED it as one device among six.

THIS RUN LADDERS THE CEILING ITSELF, in both directions, on three panels, and asks the
only question that matters for capital: does the ceiling do ANYTHING a plain de-gross
does not?  A ceiling removes names, and removing names removes exposure; if the ceiling
is worth carrying it must beat the SAME book simply scaled down to the SAME realised
mean gross.  If it does not, the ceiling is not a risk control, it is a COST.

CONSTRUCTION
  CEILING RUNG m in {0.45, 0.60, 0.80, 1.00, 1.50, NONE}   (tuned dial 1; ALL published)
  BOOK CARRIER in {V1, BASE20}                             (tuned dial 2; BOTH published)
      V1     = baseline.rules_v1_weights(px, n=5, w=0.15, max_vol=m)  -- the shipped v1
               shape, where the ceiling literally lives.
      BASE20 = the record's frozen momentum anchor: top-20 by 126d momentum among names
               above their 200d MA with vol20 < m, equal weight at gross 0.75 (1534's
               BASE, N and H frozen at the committed values, NOT searched here).
  PANEL    in {U56, B136, SMALL}      reported, not tuned
  CADENCE  in {W, M}                  reported, not tuned
  COST     in {0, 10, 25, 50} bps     reported, not tuned (10 bps is PROTOCOL's binding rung)

  MATCHED-EXPOSURE DE-GROSS TWIN (the anchor, 1534's convention).  For each
  (panel, carrier, cadence) the NO-CEILING book is the reference; the anchor for rung m
  is that reference scaled by a CONSTANT f chosen so its realised mean gross equals rung
  m's, by one Newton correction pass.  The achieved match is published as gate G3.
  PAIRED STATISTIC d_X = X(ceiling book) - X(its matched-exposure twin).

  Costs are applied analytically: every book is run ONCE at 0 bps and the return series
  at cost c is r0 - turnover * c/1e4 (exact, since held weights do not depend on cost).
  Gate G1 checks this against a direct 10 bps backtest to 1e-12.

  Both KEEP paths are evaluated at EVERY grid point, against the live RULES v2 book and
  SPY on the same panel and sample:
    4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's;
        reported on the FULL legs and again with every leg recomputed inside 2017-2026.
  RULE 8: the ceiling is chosen on 2009-2016 IS Sharpe ONLY, and 2017-2026 is read ONCE.

  SURVIVORSHIP: all three panels are current-constituent lists (PROTOCOL rule 9); the
  SMALL panel carries SPY as a joined benchmark column, which the record's books have
  always left investable -- kept unchanged here so the numbers are comparable.

Run: python3 research/backtests/2026-09-22_maxvol-ceiling-as-a-cost_C.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa
from engine import backtest                                              # noqa

STAMP     = "2026-09-22_maxvol-ceiling-as-a-cost_C"
WARMUP    = 260                       # rows skipped, same convention as baseline.compare
OOS_START = pd.Timestamp("2017-01-01")
IS_END    = pd.Timestamp("2016-12-31")
COSTS     = [0, 10, 25, 50]
BIND      = 10                        # PROTOCOL's binding cost rung
CADENCES  = ["W", "M"]
RUNGS     = [0.45, 0.60, 0.80, 1.00, 1.50, np.inf]     # np.inf == NO CEILING
SHIPPED   = 0.60
N_FROZEN, H_FROZEN, GROSS = 20, 126, 0.75              # 1534's frozen BASE, not searched

def rung_label(m):
    return "NONE" if not np.isfinite(m) else f"{m:.2f}"

# ------------------------------------------------------------------ books
def base20_weights(px, maxvol):
    """1534's frozen BASE: top-20 by 126d momentum, above 200d MA, vol20 < maxvol, gross 0.75."""
    mom   = px / px.shift(H_FROZEN) - 1
    ma200 = px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig  = mom.where((px > ma200) & (vol20 < maxvol))
    rank  = elig.rank(axis=1, ascending=False)
    return (rank <= N_FROZEN).astype(float) * (GROSS / N_FROZEN)

def v1_weights(px, maxvol):
    return rules_v1_weights(px, n=5, w=0.15, max_vol=maxvol)

CARRIERS = {"V1": v1_weights, "BASE20": base20_weights}

def elig_count(px, maxvol):
    """Mean number of names passing the 200d-MA + ceiling eligibility test per day."""
    ma200 = px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return ((px > ma200) & (vol20 < maxvol)).sum(axis=1).iloc[WARMUP:].mean()

# ------------------------------------------------------------------ metrics
def _cagr(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    return eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan

def _sharpe(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan

def _maxdd(r):
    eq = (1 + r).cumprod()
    return (eq / eq.cummax() - 1).min()

def legs(r):
    """Full-sample legs + the OOS window's own legs (2017-2026 split in half internally)."""
    h  = len(r) // 2
    o  = r.loc[OOS_START:]
    ho = len(o) // 2
    return dict(CAGR=_cagr(r), Sharpe=_sharpe(r), MaxDD=_maxdd(r),
                H1=_sharpe(r.iloc[:h]), H2=_sharpe(r.iloc[h:]),
                IS_Sharpe=_sharpe(r.loc[:IS_END]), IS_CAGR=_cagr(r.loc[:IS_END]),
                OOS_CAGR=_cagr(o), OOS_Sharpe=_sharpe(o), OOS_MaxDD=_maxdd(o),
                OOS_H1=_sharpe(o.iloc[:ho]), OOS_H2=_sharpe(o.iloc[ho:]))

def keep4a(m, v2):
    return bool(m["H1"] > v2["H1"] and m["H2"] > v2["H2"] and m["MaxDD"] >= v2["MaxDD"])

def keep4b_full(m, spy):
    return bool(m["H1"] > spy["H1"] and m["H2"] > spy["H2"] and m["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and m["MaxDD"] >= 0.60 * spy["MaxDD"] and m["CAGR"] >= 0.70 * spy["CAGR"])

def keep4b_oos(m, spy):
    """Every 4b leg recomputed inside 2017-2026 (the record's 'FULL and OOS' convention)."""
    return bool(m["OOS_H1"] > spy["OOS_H1"] and m["OOS_H2"] > spy["OOS_H2"]
                and m["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and m["OOS_MaxDD"] >= 0.60 * spy["OOS_MaxDD"]
                and m["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])

# ------------------------------------------------------------------ runner
def run0(px, w, start, freq):
    """One 0-bps backtest; returns (r0, turnover, mean realised gross)."""
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return (res["returns"].loc[start:], res["turnover"].loc[start:],
            res["weights"].sum(axis=1).loc[start:].mean())

def at_cost(r0, tno, c):
    return r0 - tno * c / 1e4

def main():
    t0 = time.time()
    gates, rows, wf_rows, inert = [], [], [], []
    panels = {}
    for lbl, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        px = load_universe(**kw)
        start = px.index[WARMUP]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        v2_0, v2_t, _ = run0(px, rules_v2_weights(px), start, "W")   # live book: always weekly
        panels[lbl] = dict(px=px, start=start, spy=spy_r, v2_0=v2_0, v2_t=v2_t)
        print(f"[{lbl}] {px.shape[1]} names  {start.date()}..{px.index[-1].date()}  ({time.time()-t0:.0f}s)")

    # G6: replay the committed RULES v2 acceptance row on U56 weekly 10 bps
    P = panels["U56"]
    v2m = legs(at_cost(P["v2_0"], P["v2_t"], BIND))
    gates.append(dict(gate="G6_rulesv2_replay",
                      detail=f"U56 W 10bps CAGR {v2m['CAGR']:.4%} Sharpe {v2m['Sharpe']:.4f} MaxDD {v2m['MaxDD']:.4%} "
                             f"(RULES.md: 8.66% / 1.2056 / -12.05%)",
                      passed=bool(abs(v2m["CAGR"] - 0.0866) < 5e-4 and abs(v2m["Sharpe"] - 1.2056) < 5e-3
                                  and abs(v2m["MaxDD"] + 0.1205) < 5e-4)))

    # ------------------------------------------------------------ the grid
    store = {}       # (panel, carrier, cadence, rung) -> (r0, tno, gross)
    anc   = {}       # (panel, carrier, cadence, rung) -> (r0, tno, gross)  matched twin
    for lbl, P in panels.items():
        px, start = P["px"], P["start"]
        for cname, fn in CARRIERS.items():
            W = {m: fn(px, m) for m in RUNGS}
            for freq in CADENCES:
                ref0, reft, refg = run0(px, W[np.inf], start, freq)
                store[(lbl, cname, freq, np.inf)] = (ref0, reft, refg)
                anc[(lbl, cname, freq, np.inf)]   = (ref0, reft, refg)   # twin of itself
                for m in RUNGS[:-1]:
                    d0, dt, dg = run0(px, W[m], start, freq)
                    store[(lbl, cname, freq, m)] = (d0, dt, dg)
                    f = dg / refg                                        # Newton pass 1
                    a0, at_, ag = run0(px, W[np.inf] * f, start, freq)
                    if ag > 0:
                        f *= dg / ag                                     # Newton pass 2
                        a0, at_, ag = run0(px, W[np.inf] * f, start, freq)
                    anc[(lbl, cname, freq, m)] = (a0, at_, ag)
                    diff = (W[m] - W[np.inf]).abs().iloc[WARMUP:]
                    inert.append(dict(panel=lbl, carrier=cname, cadence=freq, rung=rung_label(m),
                                      days_identical_to_NONE=float((diff.sum(axis=1) < 1e-12).mean()),
                                      mean_L1_vs_NONE=float(diff.sum(axis=1).mean())))
                    gates.append(dict(gate="G3_exposure_match",
                                      detail=f"{lbl}/{cname}/{freq}/m={rung_label(m)} gross dev {dg:.4f} anc {ag:.4f}",
                                      passed=bool(abs(dg - ag) < 1e-3)))
                print(f"  [{lbl}] {cname:6s} {freq}  gross " +
                      " ".join(f"{rung_label(m)}:{store[(lbl,cname,freq,m)][2]:.3f}" for m in RUNGS) +
                      f"  ({time.time()-t0:.0f}s)")

    # G1: analytic cost reconstruction == direct backtest at 10 bps
    px = panels["U56"]["px"]; start = panels["U56"]["start"]
    direct = backtest(px, CARRIERS["V1"](px, SHIPPED), cost_bps=BIND, freq="W")["returns"].loc[start:]
    recon  = at_cost(*store[("U56", "V1", "W", SHIPPED)][:2], BIND)
    gates.append(dict(gate="G1_cost_reconstruction",
                      detail=f"max |direct - reconstructed| = {float((direct - recon).abs().max()):.3e}",
                      passed=bool((direct - recon).abs().max() < 1e-12)))
    # G2: the NONE rung is the m -> large limit
    big = backtest(px, CARRIERS["V1"](px, 1e9), cost_bps=0.0, freq="W")["returns"].loc[start:]
    gates.append(dict(gate="G2_none_rung_is_the_limit",
                      detail=f"max |m=NONE - m=1e9| = {float((store[('U56','V1','W',np.inf)][0] - big).abs().max()):.3e}",
                      passed=bool((store[("U56", "V1", "W", np.inf)][0] - big).abs().max() < 1e-12)))
    # G4: eligibility is monotone in the ceiling
    for lbl, P in panels.items():
        ec = [elig_count(P["px"], m) for m in RUNGS]
        gates.append(dict(gate="G4_eligibility_monotone",
                          detail=f"{lbl} mean eligible names " + " ".join(f"{rung_label(m)}:{c:.1f}" for m, c in zip(RUNGS, ec)),
                          passed=bool(all(a <= b + 1e-9 for a, b in zip(ec, ec[1:])))))
    # G5: the IS/OOS split is disjoint and 2017-2026 is read once
    r = store[("U56", "V1", "W", SHIPPED)][0]
    gates.append(dict(gate="G5_walkforward_split",
                      detail=f"IS {r.loc[:IS_END].index[0].date()}..{r.loc[:IS_END].index[-1].date()} "
                             f"({len(r.loc[:IS_END])} rows), OOS {r.loc[OOS_START:].index[0].date()}.."
                             f"{r.loc[OOS_START:].index[-1].date()} ({len(r.loc[OOS_START:])} rows)",
                      passed=bool(len(r.loc[:IS_END]) + len(r.loc[OOS_START:]) == len(r))))

    # ------------------------------------------------------------ score every cell
    for (lbl, cname, freq, m), (d0, dt, dg) in store.items():
        P = panels[lbl]
        a0, at_, ag = anc[(lbl, cname, freq, m)]
        spy_m = legs(P["spy"])
        for c in COSTS:
            dm  = legs(at_cost(d0, dt, c))
            am  = legs(at_cost(a0, at_, c))
            v2m = legs(at_cost(P["v2_0"], P["v2_t"], c))
            rows.append(dict(panel=lbl, carrier=cname, cadence=freq, rung=rung_label(m), m=m,
                             cost_bps=c, gross=dg, gross_anc=ag,
                             turnover=float(dt.sum() / (len(dt) / 252)),
                             d_Sharpe=dm["Sharpe"] - am["Sharpe"], d_CAGR=dm["CAGR"] - am["CAGR"],
                             d_MaxDD=dm["MaxDD"] - am["MaxDD"],
                             d_OOS_Sharpe=dm["OOS_Sharpe"] - am["OOS_Sharpe"],
                             keep4a=keep4a(dm, v2m), keep4b=keep4b_full(dm, spy_m),
                             keep4b_oos=keep4b_oos(dm, spy_m),
                             anc_keep4a=keep4a(am, v2m), anc_keep4b=keep4b_full(am, spy_m),
                             **{k: v for k, v in dm.items()},
                             **{f"anc_{k}": v for k, v in am.items()},
                             **{f"spy_{k}": v for k, v in spy_m.items()},
                             **{f"v2_{k}": v for k, v in v2m.items()}))
    df = pd.DataFrame(rows).sort_values(["panel", "carrier", "cadence", "cost_bps", "m"]).reset_index(drop=True)

    # ------------------------------------------------------------ rule 8 walk-forward
    for (lbl, cname, freq, c), g in df.groupby(["panel", "carrier", "cadence", "cost_bps"]):
        g = g.set_index("rung")
        pick    = g["IS_Sharpe"].idxmax()                 # chosen on 2009-2016 ONLY
        oracle  = g["OOS_Sharpe"].idxmax()                # not reachable; reported for the gap
        row = lambda k: g.loc[k]
        wf_rows.append(dict(panel=lbl, carrier=cname, cadence=freq, cost_bps=c,
                            pick=pick, shipped=rung_label(SHIPPED), oracle=oracle,
                            pick_is_shipped=bool(pick == rung_label(SHIPPED)),
                            pick_is_loosest=bool(pick == "NONE"),
                            pick_OOS_Sharpe=row(pick)["OOS_Sharpe"], pick_OOS_CAGR=row(pick)["OOS_CAGR"],
                            pick_OOS_MaxDD=row(pick)["OOS_MaxDD"],
                            ship_OOS_Sharpe=row("0.60")["OOS_Sharpe"], ship_OOS_CAGR=row("0.60")["OOS_CAGR"],
                            ship_OOS_MaxDD=row("0.60")["OOS_MaxDD"],
                            none_OOS_Sharpe=row("NONE")["OOS_Sharpe"], none_OOS_CAGR=row("NONE")["OOS_CAGR"],
                            none_OOS_MaxDD=row("NONE")["OOS_MaxDD"],
                            oracle_OOS_Sharpe=row(oracle)["OOS_Sharpe"],
                            v2_OOS_Sharpe=row(pick)["v2_OOS_Sharpe"], v2_OOS_CAGR=row(pick)["v2_OOS_CAGR"],
                            v2_OOS_MaxDD=row(pick)["v2_OOS_MaxDD"],
                            spy_OOS_Sharpe=row(pick)["spy_OOS_Sharpe"], spy_OOS_CAGR=row(pick)["spy_OOS_CAGR"],
                            spy_OOS_MaxDD=row(pick)["spy_OOS_MaxDD"],
                            pick_keep4a=bool(row(pick)["keep4a"]), pick_keep4b=bool(row(pick)["keep4b"]),
                            pick_keep4b_oos=bool(row(pick)["keep4b_oos"]),
                            ship_keep4b=bool(row("0.60")["keep4b"]),
                            d_pick_minus_ship_OOS_Sharpe=row(pick)["OOS_Sharpe"] - row("0.60")["OOS_Sharpe"],
                            IS_argmax_Sharpe=row(pick)["IS_Sharpe"], IS_ship_Sharpe=row("0.60")["IS_Sharpe"]))
    wf = pd.DataFrame(wf_rows)

    # ------------------------------------------------------------ report
    pd.set_option("display.width", 220, "display.max_columns", 80, "display.max_rows", 400)
    print("\n" + "=" * 110)
    print("ALL GRID POINTS -- ceiling book vs its MATCHED-EXPOSURE de-gross twin "
          f"({len(df)} cells = 3 panels x 2 carriers x 2 cadences x 6 rungs x 4 cost rungs)")
    print("=" * 110)
    show = ["panel", "carrier", "cadence", "cost_bps", "rung", "gross", "turnover", "CAGR", "Sharpe",
            "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "d_Sharpe", "d_CAGR", "d_MaxDD",
            "keep4a", "keep4b", "keep4b_oos"]
    print(df[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n--- THE PAIRED QUESTION: does the ceiling beat a plain de-gross to the SAME exposure? ---")
    dev = df[np.isfinite(df["m"])]
    for c in COSTS:
        s = dev[dev.cost_bps == c]
        print(f"  cost {c:2d} bps  n={len(s):3d}  mean d_Sharpe {s.d_Sharpe.mean():+.4f}  "
              f"median {s.d_Sharpe.median():+.4f}  positive {int((s.d_Sharpe > 0).sum())}/{len(s)}  "
              f"| mean d_CAGR {s.d_CAGR.mean():+.4%}  mean d_MaxDD {s.d_MaxDD.mean():+.4%}  "
              f"DD shallower {int((s.d_MaxDD > 0).sum())}/{len(s)}")
    print("\n  by rung (10 bps, pooled over panel x carrier x cadence):")
    for m in RUNGS[:-1]:
        s = dev[(dev.cost_bps == BIND) & (dev.m == m)]
        print(f"    m={rung_label(m)}  mean d_Sharpe {s.d_Sharpe.mean():+.4f}  positive {int((s.d_Sharpe>0).sum())}/{len(s)}"
              f"  mean d_CAGR {s.d_CAGR.mean():+.4%}  mean d_MaxDD {s.d_MaxDD.mean():+.4%}  mean gross {s.gross.mean():.3f}")
    print("\n  by panel (10 bps):")
    for lbl in panels:
        s = dev[(dev.cost_bps == BIND) & (dev.panel == lbl)]
        print(f"    {lbl:6s} mean d_Sharpe {s.d_Sharpe.mean():+.4f}  positive {int((s.d_Sharpe>0).sum())}/{len(s)}"
              f"  mean d_MaxDD {s.d_MaxDD.mean():+.4%}")

    # ------------------------------------------------------------ pooled paired block bootstrap
    # d_i = Sharpe(ceiling rung i) - Sharpe(its matched-exposure twin), pooled over all 60
    # (panel x carrier x cadence x rung) pairs.  Circular block bootstrap, LB = 65 trading days
    # (~13 weekly rebalance rows), B = 500, THE SAME BLOCKS drawn for every pair in a replicate
    # so cross-book and cross-panel dependence is carried rather than assumed away.
    LB, NBOOT, SEED = 65, 500, 20260922
    keys  = [k for k in store if np.isfinite(k[3])]
    union = panels["U56"]["px"].index
    union = union[union >= panels["U56"]["start"]]
    T     = len(union)
    rng   = np.random.default_rng(SEED)
    nblk  = int(np.ceil(T / LB))
    starts_all = rng.integers(0, T, size=(NBOOT, nblk))
    def _sh_cols(X):
        mu = np.nanmean(X, axis=0) * 252
        sd = np.nanstd(X, axis=0, ddof=1) * np.sqrt(252)
        return np.where(sd > 0, mu / sd, np.nan)
    boot = {}
    for c in COSTS:
        D = np.column_stack([at_cost(*store[k][:2], c).reindex(union).values for k in keys])
        A = np.column_stack([at_cost(*anc[k][:2], c).reindex(union).values for k in keys])
        obs = float(np.nanmean(_sh_cols(D) - _sh_cols(A)))
        bs  = np.empty(NBOOT)
        for b in range(NBOOT):
            idx = (starts_all[b][:, None] + np.arange(LB)[None, :]).ravel()[:T] % T
            bs[b] = np.nanmean(_sh_cols(D[idx]) - _sh_cols(A[idx]))
        boot[c] = (obs, float(bs.std(ddof=1)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))
    print("\n--- POOLED PAIRED TEST (ceiling - matched-exposure de-gross), circular block bootstrap "
          f"LB={LB}d, B={NBOOT}, n=60 pairs ---")
    for c in COSTS:
        o, se, lo, hi = boot[c]
        print(f"  cost {c:2d} bps  pooled d_Sharpe {o:+.4f}  SE {se:.4f}  t {o/se:+.2f}  95% CI [{lo:+.4f}, {hi:+.4f}]")

    print("\n--- IS THE CEILING EVEN BINDING? (weight-identity against the NO-CEILING book) ---")
    idf = pd.DataFrame(inert)
    print(idf.groupby(["panel", "carrier", "rung"])[["days_identical_to_NONE", "mean_L1_vs_NONE"]]
          .mean().to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n--- SHIPPED m=0.60 vs ITS OWN LADDER (full-sample Sharpe, 10 bps) ---")
    for (lbl, cname, freq), g in df[df.cost_bps == BIND].groupby(["panel", "carrier", "cadence"]):
        g = g.set_index("rung")
        sh = g.loc["0.60", "Sharpe"]
        better = [k for k in g.index if g.loc[k, "Sharpe"] > sh]
        bo = [k for k in g.index if g.loc[k, "OOS_Sharpe"] > g.loc["0.60", "OOS_Sharpe"]]
        print(f"  {lbl:6s} {cname:6s} {freq}  shipped Sharpe {sh:.4f} / OOS {g.loc['0.60','OOS_Sharpe']:.4f}"
              f"  | rungs beating it FULL: {len(better)}/5 {better}  OOS: {len(bo)}/5 {bo}")

    print("\n--- KEEP counts over the whole grid ---")
    for c in COSTS:
        s = df[df.cost_bps == c]
        both = s[s.keep4a & s.keep4b]
        print(f"  cost {c:2d} bps: 4a {int(s.keep4a.sum())}/{len(s)}   4b(full) {int(s.keep4b.sum())}/{len(s)}"
              f"   4b(OOS legs) {int(s.keep4b_oos.sum())}/{len(s)}   BOTH(4a,4b) {len(both)}"
              f"   4b FULL+OOS {int((s.keep4b & s.keep4b_oos).sum())}")
    kb = df[df.keep4b & df.keep4b_oos]
    if len(kb):
        print("\n  cells clearing 4b on FULL and OOS legs alike:")
        print(kb[["panel", "carrier", "cadence", "cost_bps", "rung", "CAGR", "Sharpe", "MaxDD",
                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 110)
    print("RULE 8 WALK-FORWARD -- ceiling chosen on 2009-2016 IS SHARPE ONLY; 2017-2026 read ONCE")
    print("=" * 110)
    print(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n  chooser picks the shipped m=0.60 in {int(wf.pick_is_shipped.sum())} of {len(wf)} families; "
          f"picks NO CEILING in {int(wf.pick_is_loosest.sum())}")
    print(f"  picked-minus-shipped OOS Sharpe: mean {wf.d_pick_minus_ship_OOS_Sharpe.mean():+.4f}  "
          f"median {wf.d_pick_minus_ship_OOS_Sharpe.median():+.4f}  "
          f"chooser better in {int((wf.d_pick_minus_ship_OOS_Sharpe > 0).sum())} of {len(wf)}")
    print(f"  mean OOS Sharpe -- picked {wf.pick_OOS_Sharpe.mean():.4f} | shipped {wf.ship_OOS_Sharpe.mean():.4f} | "
          f"no ceiling {wf.none_OOS_Sharpe.mean():.4f} | oracle {wf.oracle_OOS_Sharpe.mean():.4f} | "
          f"RULES v2 {wf.v2_OOS_Sharpe.mean():.4f} | SPY {wf.spy_OOS_Sharpe.mean():.4f}")
    print(f"  mean OOS CAGR  -- picked {wf.pick_OOS_CAGR.mean():.4%} | shipped {wf.ship_OOS_CAGR.mean():.4%} | "
          f"no ceiling {wf.none_OOS_CAGR.mean():.4%} | RULES v2 {wf.v2_OOS_CAGR.mean():.4%} | SPY {wf.spy_OOS_CAGR.mean():.4%}")
    print(f"  mean OOS MaxDD -- picked {wf.pick_OOS_MaxDD.mean():.4%} | shipped {wf.ship_OOS_MaxDD.mean():.4%} | "
          f"no ceiling {wf.none_OOS_MaxDD.mean():.4%} | RULES v2 {wf.v2_OOS_MaxDD.mean():.4%} | SPY {wf.spy_OOS_MaxDD.mean():.4%}")
    print(f"  rule-8-reachable KEEPs: 4a {int(wf.pick_keep4a.sum())}/{len(wf)}  "
          f"4b(full) {int(wf.pick_keep4b.sum())}/{len(wf)}  4b(OOS legs) {int(wf.pick_keep4b_oos.sum())}/{len(wf)}")

    gdf = pd.DataFrame(gates)
    print(f"\nGATES: {int(gdf.passed.sum())} of {len(gdf)} pass")
    print(gdf[~gdf.passed].to_string(index=False) if (~gdf.passed).any() else "  (all pass)")
    print(gdf[gdf.gate != "G3_exposure_match"].to_string(index=False))

    out = ROOT / "research" / "backtests"
    df.to_csv(out / f"{STAMP}.grid.csv", index=False)
    wf.to_csv(out / f"{STAMP}.walkforward.csv", index=False)
    gdf.to_csv(out / f"{STAMP}.gates.csv", index=False)
    idf.to_csv(out / f"{STAMP}.binding.csv", index=False)
    pd.DataFrame([dict(cost_bps=c, pooled_d_Sharpe=boot[c][0], SE=boot[c][1],
                       t=boot[c][0] / boot[c][1], lo95=boot[c][2], hi95=boot[c][3])
                  for c in COSTS]).to_csv(out / f"{STAMP}.bootstrap.csv", index=False)
    print(f"\nwrote {STAMP}.grid.csv ({len(df)} rows), .walkforward.csv ({len(wf)}), .gates.csv ({len(gdf)})"
          f"  [{time.time()-t0:.0f}s]")

if __name__ == "__main__":
    main()
