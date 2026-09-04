#!/usr/bin/env python3
"""QUEUE idea 88 — selectability-pre-test-across-the-leaderboard (cloud, 2026-09-04).

Question
--------
Idea 87 proposed PROTOCOL clause 8a: before walk-forward-selecting a parameter, report the
grid's in-sample spread in the selection objective and in each binding 4b bar; if the IS
Sharpe spread across the whole grid is under 0.02, or the spread in a binding constraint is
0.00, the parameter is a POLICY DIAL, not an estimate, and rule 8 does not apply to it.

The clause was proposed on two grids (gross, crypto cap).  This run asks the two questions
that decide whether PROTOCOL should carry it:

    (a) Retrospective: across every published n / fraction / gross / band / lookback / cost /
        cadence / hysteresis sweep, which rule-8 conclusions rested on a grid with no
        selectable content?
    (b) Validation (the part with content): does the pre-test PREDICT anything?  If 8a is
        real, the grids it flags should be the grids where rule 8's pick is no better than a
        coin flip out of sample.  If flagged and unflagged grids select equally well, 8a is
        bookkeeping and PROTOCOL should not carry it.

Pre-registered before any number was read
-----------------------------------------
    SKILL(cell)  = OOS Sharpe of rule 8's pick  -  mean OOS Sharpe of the whole grid
                   (i.e. how much better than picking an arm at random; 0 = no skill)
    REGRET(cell) = OOS Sharpe of the pick - the grid's best OOS Sharpe (<= 0)
    rho(cell)    = Spearman(IS Sharpe, OOS Sharpe) across the grid's arms
    8a verdict   = FAIL-objective if IS Sharpe spread < 0.02
                   FAIL-blind     if a BINDING IS 4b bar has statistic spread < 1e-4
                   PASS           otherwise
    H1 (8a has content): mean SKILL and mean rho are materially higher on PASS cells than on
                         FAIL cells, and FAIL cells' SKILL is indistinguishable from 0.
    H0 (8a is bookkeeping): no separation.
Nothing is tuned to make either outcome appear; the 0.02 threshold is idea 87's own and is
NOT re-fitted here (a threshold sensitivity curve is printed instead).

Design (PROTOCOL rules 1-8)
---------------------------
Universes : universe.json (56) and universe_broad.json (136).  SURVIVORSHIP: both are
            current-constituent lists, so absolute CAGRs are optimistic.  This run compares
            SELECTION RULES on common grids, so the bias falls on every arm alike.
Grids     : 11 one-parameter grids re-run from scratch, chosen to cover every sweep family
            the leaderboard has published (the queue names n / gross / cost / cadence):
              N/ranked      n    in {5,10,15,20,30,40}                 idea 2   (KEEP-cand)
              F/fraction    f    in {0.15,0.35,0.45,0.70,0.85,1.00}    idea 46
              GROSS/top20   g    in {0.50..1.00}                       idea 66
              GROSS/EWall   g    in {0.50..1.00}                       idea 66
              BAND/ew-all   band in {0,0.02,0.03,0.05,0.08}            idea 57
              K/lookback    K    in {50,100,200,none}                  idea 55
              COST/top20    bps  in {0,5,10,15,20,25,50}               ideas 45/68
              COST/EWall    bps  in {0,5,10,15,20,25,50}               ideas 45/68
              CADENCE/top20 freq in {D,W,M,Q}                          idea 3
              CADENCE/EWall freq in {D,W,M,Q}                          idea 3
              HYST/top20    k    in {1.00,1.25,1.50,2.00}              ideas 79/86
Params    : exactly 2 tuned -- the grid parameter, and the selection rule (R0 = rule 8 as
            written, R2 = 4b-aware).  ALL grid points are printed.
Books     : CAND-n = top n eligible by the v1 composite WITHOUT /sqrt(vol20), equal weight
            at GROSS/n (the literal published form, cash when E_t < n); EWall = equal-weight
            every eligible name at GROSS.  Eligibility = RULES v1's gate (above the 200d MA,
            vol20 < 0.60) unless the grid varies it.
Execution : weights decided at close t, applied t+1; 10 bps per unit turnover except in the
            COST grids, which are the sweep; weekly except in the CADENCE grids.
Walk-fwd  : rule 8 -- parameters chosen on 2009-2016 (IS) only, evaluated untouched on
            2017-2026 (OOS).  Both KEEP paths (4a, 4b) are evaluated for every arm on the
            full sample and 4b again on the OOS window.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-04_selectability-pre-test_cloud"
COST, FREQ, MAX_VOL, GROSS = 10.0, "W", 0.60, 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SPREAD_MIN = 0.02          # idea 87's pre-registered IS-Sharpe spread floor
BLIND_EPS = 1e-4           # "a constraint's spread is 0.00"

# grid -> the published conclusion that rested on it (for the retrospective table)
PROVENANCE = {
    "N/ranked":      "idea 2: n=20 is the standing 4b KEEP-candidate (rule-8 pick)",
    "F/fraction":    "idea 46: f=0.85 is the fraction arm's rule-8 pick / 4b candidate",
    "GROSS/top20":   "idea 66: gross is not selectable; all picks fail OOS DD",
    "GROSS/EWall":   "idea 66: same, on the unranked book",
    "BAND/ew-all":   "idea 57/87: band book is the most robust object; picks band=0.08",
    "K/lookback":    "idea 55: rule 8 picks K=none on u56, K=200d on broad",
    "COST/top20":    "ideas 45/68: cost breakeven of the standing candidate",
    "COST/EWall":    "ideas 45/68/83: EWall's higher breakeven",
    "CADENCE/top20": "idea 3/65: cadence-insensitivity proposed as a KEEP bar",
    "CADENCE/EWall": "idea 3/65: same, unranked book",
    "HYST/top20":    "idea 86: k=2 cuts turnover 60%, cost-neutral",
}


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, band=0.0, K=200):
    if K <= 0:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(K).mean()
    if band <= 0:
        return (px > ma).fillna(False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def eligible(px, band=0.0, K=200):
    return (vol20(px) < MAX_VOL) & trend(px, band, K)


def w_ranked(px, n=20, g=GROSS, band=0.0, K=200):
    """Literal CAND-n: top n eligible at g/n, cash when fewer than n are eligible."""
    rank = composite(px).where(eligible(px, band, K)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


def w_ewall(px, g=GROSS, band=0.0, K=200):
    e = eligible(px, band, K).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g


def w_frac(px, f=0.85, g=GROSS, band=0.0, K=200):
    """idea 46's fraction book: top ceil(f * E_t) eligible names, equal weight at g/count."""
    elig = eligible(px, band, K)
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    cnt = np.ceil(f * elig.sum(axis=1)).clip(lower=0)
    sel = rank.le(cnt, axis=0) & rank.notna()
    return sel.astype(float).div(cnt.replace(0, np.nan), axis=0).fillna(0.0) * g


def w_hyst(px, k=1.0, n=20, g=GROSS):
    """idea 79/86 rank hysteresis: keep a held name while its rank stays inside top k*n;
    refill freed slots from the best unheld names, holding the count the base book would
    have held.  k = 1.0 reproduces the literal CAND-n book exactly."""
    if k <= 1.0:
        return w_ranked(px, n, g)
    rk = composite(px).where(eligible(px)).rank(axis=1, ascending=False).fillna(np.inf).values
    out = np.zeros_like(rk)
    reb = rebalance_mask(px.index, FREQ).values           # signal rows (decided at close t)
    sel_prev = None
    m = rk.shape[1]
    for i in range(rk.shape[0]):
        if not reb[i]:
            if sel_prev is not None:
                out[i] = sel_prev.astype(float) * (g / n)
            continue
        row = rk[i]
        base = row <= n
        n_target = int(base.sum())
        if n_target == 0 or sel_prev is None:
            sel = base
        else:
            sel = np.zeros(m, dtype=bool)
            kept = np.where(sel_prev & (row <= n * k))[0]
            kept = kept[np.argsort(row[kept], kind="stable")][:n_target]
            sel[kept] = True
            need = n_target - int(sel.sum())
            if need > 0:
                cand = np.where(~sel & np.isfinite(row))[0]
                cand = cand[np.argsort(row[cand], kind="stable")][:need]
                sel[cand] = True
        sel_prev = sel
        out[i] = sel.astype(float) * (g / n)
    return pd.DataFrame(out, index=px.index, columns=px.columns)


# ---------------------------------------------------------------- simulation
def sim(px, W, freq=FREQ):
    """engine.backtest's loop, cost-free, returning turnover so any cost level is one line.

    Verified against engine.backtest(cost_bps=10) in the harness check below."""
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    cur = np.zeros(m)
    held = np.zeros((n, m))
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = tgt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return (pd.Series((held * rets).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index))


def net(r0, to, bps):
    return r0 - to * bps / 1e4


# ---------------------------------------------------------------- metric helpers
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars4b(r, spy):
    """4b's three absolute bars measured on ONE window -> list of failures."""
    c, s, dd = m3(r)
    sc, ss, sdd = m3(spy)
    bad = []
    if s <= ss: bad.append("Sh")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4b_full(r, spy):
    c, s, dd = m3(r); h1, h2 = halves(r)
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"]; so = metrics(spy.loc[OOS_START:])["Sharpe"]
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if o <= so: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m3(r); h1, h2 = halves(r)
    _, _, bdd = m3(base); b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def spearman(a, b):
    a, b = pd.Series(a), pd.Series(b)
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(np.corrcoef(a.rank(), b.rank())[0, 1])


# ---------------------------------------------------------------- grids
def build_grids(px):
    """(grid name, [(param label, cost_bps, freq, cost-free returns, turnover)])."""
    G = []
    G.append(("N/ranked", [(f"n={n}", COST, FREQ, w_ranked(px, n)) for n in (5, 10, 15, 20, 30, 40)]))
    G.append(("F/fraction", [(f"f={f:.2f}", COST, FREQ, w_frac(px, f))
                             for f in (0.15, 0.35, 0.45, 0.70, 0.85, 1.00)]))
    GG = (0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00)
    G.append(("GROSS/top20", [(f"g={g:.2f}", COST, FREQ, w_ranked(px, 20, g)) for g in GG]))
    G.append(("GROSS/EWall", [(f"g={g:.2f}", COST, FREQ, w_ewall(px, g)) for g in GG]))
    G.append(("BAND/ew-all", [(f"b={b:.2f}", COST, FREQ, w_ewall(px, GROSS, b))
                              for b in (0.00, 0.02, 0.03, 0.05, 0.08)]))
    G.append(("K/lookback", [(f"K={K if K else 'none'}", COST, FREQ, w_ranked(px, 20, GROSS, 0.0, K))
                             for K in (50, 100, 200, 0)]))
    CB = (0, 5, 10, 15, 20, 25, 50)
    w20, wew = w_ranked(px, 20), w_ewall(px)
    G.append(("COST/top20", [(f"c={c}bp", c, FREQ, w20) for c in CB]))
    G.append(("COST/EWall", [(f"c={c}bp", c, FREQ, wew) for c in CB]))
    G.append(("CADENCE/top20", [(f"freq={f}", COST, f, w20) for f in ("D", "W", "M", "Q")]))
    G.append(("CADENCE/EWall", [(f"freq={f}", COST, f, wew) for f in ("D", "W", "M", "Q")]))
    G.append(("HYST/top20", [(f"k={k:.2f}", COST, FREQ, w_hyst(px, k)) for k in (1.00, 1.25, 1.50, 2.00)]))
    return G


# ---------------------------------------------------------------- one universe
def run_universe(px, tag, out):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    yrs = len(spy) / 252

    print("\n" + "=" * 146)
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()}")
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    print(f"  SPY  full {sc:6.1%}/{ss:.3f}/{sdd:7.1%}  halves {s1:.3f}/{s2:.3f}"
          f"   IS {m3(spy_is)[0]:.1%}/{m3(spy_is)[1]:.3f}/{m3(spy_is)[2]:.1%}"
          f"   OOS {m3(spy_oos)[0]:.1%}/{m3(spy_oos)[1]:.3f}/{m3(spy_oos)[2]:.1%}")
    bc, bs, bdd = m3(base); b1, b2 = halves(base)
    print(f"  v1   full {bc:6.1%}/{bs:.3f}/{bdd:7.1%}  halves {b1:.3f}/{b2:.3f}"
          f"   OOS {m3(base.loc[OOS_START:])[0]:.1%}/{m3(base.loc[OOS_START:])[1]:.3f}"
          f"/{m3(base.loc[OOS_START:])[2]:.1%}   (4a reference)")
    print(f"  IS  4b bars: Sharpe > {m3(spy_is)[1]:.3f}, MaxDD >= {0.60*m3(spy_is)[2]:.1%}, "
          f"CAGR >= {0.70*m3(spy_is)[0]:.1%}")
    print("=" * 146)

    cells = []
    for gname, arms in build_grids(px):
        recs = []
        cache = {}
        for lab, bps, freq, W in arms:
            key = (id(W), freq)
            if key not in cache:
                cache[key] = sim(px, W, freq)
            r0, to = cache[key]
            r = net(r0, to, bps).loc[start:]
            c, s, dd = m3(r); h1, h2 = halves(r)
            ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
            ic, isr, idd = m3(ris); oc, osr, odd = m3(roos)
            recs.append(dict(
                grid=gname, param=lab, CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2,
                turn=to.loc[start:].sum() / yrs,
                IS_CAGR=ic, IS_Sharpe=isr, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=osr, OOS_MaxDD=odd,
                is4b=",".join(bars4b(ris, spy_is)) or "PASS",
                f4b=",".join(fail4b_full(r, spy)) or "PASS",
                f4a=",".join(fail4a(r, base)) or "PASS",
                oos4b=",".join(bars4b(roos, spy_oos)) or "PASS"))
        d = pd.DataFrame(recs)

        # ---- 8a pre-test -------------------------------------------------
        sp_sh = d.IS_Sharpe.max() - d.IS_Sharpe.min()
        sp_dd = d.IS_MaxDD.max() - d.IS_MaxDD.min()
        sp_cg = d.IS_CAGR.max() - d.IS_CAGR.min()
        # a bar BINDS in-sample when it excludes some arms but not all
        binding, blind = [], []
        for bar, spread in (("Sh", sp_sh), ("DD", sp_dd), ("CAGR", sp_cg)):
            hits = d.is4b.str.contains(bar).sum()
            if 0 < hits < len(d):
                binding.append(f"{bar}({spread:.4f})")
                if spread < BLIND_EPS:
                    blind.append(bar)
        why = []
        if sp_sh < SPREAD_MIN: why.append("objective")
        if blind: why.append("blind:" + "+".join(blind))
        verdict8a = "PASS" if not why else "FAIL(" + ",".join(why) + ")"

        # ---- selection rules --------------------------------------------
        i0 = int(d.IS_Sharpe.idxmax())
        feas = d[(d.IS_MaxDD >= 0.60 * m3(spy_is)[2]) & (d.IS_CAGR >= 0.70 * m3(spy_is)[0])]
        i2 = int(feas.IS_Sharpe.idxmax()) if len(feas) else None
        best = d.OOS_Sharpe.max()
        mean_oos = d.OOS_Sharpe.mean()
        skill = d.OOS_Sharpe[i0] - mean_oos
        regret = d.OOS_Sharpe[i0] - best
        rho = spearman(d.IS_Sharpe, d.OOS_Sharpe)

        print(f"\n[{tag}] grid {gname}    8a: {verdict8a}   "
              f"IS Sharpe spread {sp_sh:.4f}  binding {'; '.join(binding) or 'none'}   "
              f"({PROVENANCE[gname]})")
        print(f"  {'param':>9}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'H1':>7}{'H2':>7}{'turn':>7}"
              f"{'ISsh':>8}{'ISdd':>8}{'OOSsh':>8}{'OOSdd':>8}  {'4a':<8}{'4b full':<14}{'4b OOS':<10}")
        for j, row in d.iterrows():
            mark = ("  <-R0" if j == i0 else "") + ("  <-R2" if j == i2 else "")
            print(f"  {row.param:>9}{row.CAGR:8.1%}{row.Sharpe:8.3f}{row.MaxDD:8.1%}{row.H1:7.3f}"
                  f"{row.H2:7.3f}{row.turn:7.1f}{row.IS_Sharpe:8.3f}{row.IS_MaxDD:8.1%}"
                  f"{row.OOS_Sharpe:8.3f}{row.OOS_MaxDD:8.1%}  {row.f4a:<8}{row.f4b:<14}"
                  f"{row.oos4b:<10}{mark}")
        print(f"  R0 (rule 8) picks {d.param[i0]:>9}: OOS {d.OOS_CAGR[i0]:.1%}/{d.OOS_Sharpe[i0]:.3f}"
              f"/{d.OOS_MaxDD[i0]:.1%}   grid OOS-best {best:.3f} ({d.param[d.OOS_Sharpe.idxmax()]})"
              f"   mean {mean_oos:.3f}   SKILL {skill:+.3f}   REGRET {regret:+.3f}   rho {rho:+.3f}")
        if i2 is None:
            print("  R2 (4b-aware): INFEASIBLE - no arm meets the IS drawdown cap and CAGR floor")
        else:
            print(f"  R2 (4b-aware) picks {d.param[i2]:>9}: OOS {d.OOS_CAGR[i2]:.1%}/"
                  f"{d.OOS_Sharpe[i2]:.3f}/{d.OOS_MaxDD[i2]:.1%}")

        # ---- consequence of the pick, on the objective and on RISK ------
        sp_oos_sh = d.OOS_Sharpe.max() - d.OOS_Sharpe.min()
        sp_oos_dd = d.OOS_MaxDD.max() - d.OOS_MaxDD.min()
        print(f"  consequence of the choice: OOS Sharpe spread {sp_oos_sh:.3f}, "
              f"OOS MaxDD spread {sp_oos_dd:.1%}, R0's OOS MaxDD {d.OOS_MaxDD[i0]:.1%} "
              f"(grid {d.OOS_MaxDD.min():.1%}..{d.OOS_MaxDD.max():.1%})")

        cells.append(dict(universe=tag, grid=gname, n_arms=len(d), a8=verdict8a,
                          sp_IS_Sharpe=sp_sh, sp_IS_MaxDD=sp_dd, sp_IS_CAGR=sp_cg,
                          sp_OOS_Sharpe=sp_oos_sh, sp_OOS_MaxDD=sp_oos_dd,
                          R0_OOS_MaxDD=d.OOS_MaxDD[i0],
                          binding="; ".join(binding) or "none",
                          R0=d.param[i0], R0_OOS=d.OOS_Sharpe[i0], best_OOS=best,
                          mean_OOS=mean_oos, skill=skill, regret=regret, rho=rho,
                          R2=(d.param[i2] if i2 is not None else "INFEASIBLE"),
                          R2_OOS=(d.OOS_Sharpe[i2] if i2 is not None else np.nan),
                          n_4b_full=(d.f4b == "PASS").sum(), n_4a=(d.f4a == "PASS").sum(),
                          prov=PROVENANCE[gname]))
        out.append(d)
    return cells


# ---------------------------------------------------------------- main
def main():
    pd.set_option("display.width", 200)
    px = load_universe()
    pxb = load_universe(broad=True)

    print("HARNESS SANITY (must reproduce published rows before any new number is read)")
    r = net(*sim(px, w_ranked(px, 20)), COST).loc[px.index[260]:]
    c, s, dd = m3(r); h1, h2 = halves(r)
    print(f"  idea 2  u56 CAND20 : {c:.1%}/{s:.3f}/{dd:.1%} halves {h1:.3f}/{h2:.3f}"
          f"   (published 12.7%/1.093/-18.3%, 1.088/1.103)")
    e = backtest(px, w_ranked(px, 20), cost_bps=COST, freq=FREQ)["returns"].loc[px.index[260]:]
    print(f"  sim vs engine.backtest max |dr| = {float((r - e).abs().max()):.2e}")
    rb = net(*sim(pxb, w_ewall(pxb)), COST).loc[pxb.index[260]:]
    c, s, dd = m3(rb); h1, h2 = halves(rb)
    print(f"  idea 10 B136/EWall : {c:.1%}/{s:.3f}/{dd:.1%} halves {h1:.3f}/{h2:.3f}"
          f"   (published 10.7%/1.027/-17.7%, 1.146/0.917)")

    arms, cells = [], []
    cells += run_universe(px, "u56", arms)
    cells += run_universe(pxb, "broad", arms)

    C = pd.DataFrame(cells)
    A = pd.concat(arms, ignore_index=True)
    A.to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)
    C.to_csv(ROOT / "research" / "backtests" / f"{STEM}.cells.csv", index=False)

    print("\n" + "=" * 146)
    print("RETROSPECTIVE: 8a pre-test applied to every published sweep family")
    print("=" * 146)
    print(f"{'universe':<7}{'grid':<15}{'arms':>5}{'8a':<24}{'ISsh spread':>12}{'binding bars':>26}"
          f"{'R0 pick':>10}{'OOSsh':>8}{'best':>7}{'SKILL':>8}{'REGRET':>8}{'rho':>7}")
    for _, r_ in C.iterrows():
        print(f"{r_.universe:<7}{r_.grid:<15}{r_.n_arms:>5}{r_.a8:<24}{r_.sp_IS_Sharpe:12.4f}"
              f"{r_.binding:>26}{r_.R0:>10}{r_.R0_OOS:8.3f}{r_.best_OOS:7.3f}{r_.skill:+8.3f}"
              f"{r_.regret:+8.3f}{r_.rho:+7.3f}")

    print("\nVALIDATION (pre-registered): does the 8a flag predict selection quality?")
    C["pass8a"] = C.a8 == "PASS"
    for lab, sub in (("8a PASS", C[C.pass8a]), ("8a FAIL", C[~C.pass8a])):
        if not len(sub):
            continue
        t = sub.skill.mean() / (sub.skill.std(ddof=1) / np.sqrt(len(sub))) if len(sub) > 1 else np.nan
        print(f"  {lab:<9} n={len(sub):<3} mean SKILL {sub.skill.mean():+.3f} (t {t:+.2f})"
              f"  mean REGRET {sub.regret.mean():+.3f}  mean rho {sub.rho.mean():+.3f}"
              f"  SKILL>0 in {int((sub.skill > 0).sum())}/{len(sub)}"
              f"  pick=OOS-best in {int((sub.regret >= -1e-9).sum())}/{len(sub)}")
    ok = C[C.pass8a]; bad = C[~C.pass8a]
    if len(ok) and len(bad):
        print(f"  separation: dSKILL {ok.skill.mean() - bad.skill.mean():+.3f}, "
              f"drho {ok.rho.mean() - bad.rho.mean():+.3f}")

    print("\n  threshold sensitivity of the 0.02 IS-Sharpe rule (reported, NOT tuned):")
    print(f"    {'thr':>6}{'nPASS':>7}{'skill(PASS)':>13}{'skill(FAIL)':>13}{'rho(PASS)':>11}{'rho(FAIL)':>11}")
    for thr in (0.005, 0.01, 0.02, 0.05, 0.10, 0.20):
        p = C[C.sp_IS_Sharpe >= thr]; f = C[C.sp_IS_Sharpe < thr]
        print(f"    {thr:6.3f}{len(p):7d}{(p.skill.mean() if len(p) else np.nan):13.3f}"
              f"{(f.skill.mean() if len(f) else np.nan):13.3f}"
              f"{(p.rho.mean() if len(p) else np.nan):11.3f}"
              f"{(f.rho.mean() if len(f) else np.nan):11.3f}")

    print("\n  DOES A SMALL OBJECTIVE SPREAD PREDICT A BAD SELECTION?  (the pre-test's whole claim)")
    print(f"    Spearman(IS Sharpe spread, REGRET) over {len(C)} cells = "
          f"{spearman(C.sp_IS_Sharpe, C.regret):+.3f}   "
          f"(8a predicts NEGATIVE: less spread -> worse regret)")
    print(f"    Spearman(IS Sharpe spread, SKILL)  = {spearman(C.sp_IS_Sharpe, C.skill):+.3f}")
    print(f"    worst 4 selections by REGRET: " + ", ".join(
        f"{r_.universe}/{r_.grid} {r_.regret:+.3f} [{r_.a8}]"
        for _, r_ in C.nsmallest(4, "regret").iterrows()))

    print("\n  RISK CONSEQUENCE of a noise-determined pick (what 8a is actually protecting):")
    print(f"    {'universe':<7}{'grid':<15}{'8a':<20}{'ISsh spread':>12}{'OOSsh spread':>13}"
          f"{'OOSdd spread':>13}{'R0 OOSdd':>10}")
    for _, r_ in C.iterrows():
        print(f"    {r_.universe:<7}{r_.grid:<15}{r_.a8:<20}{r_.sp_IS_Sharpe:12.4f}"
              f"{r_.sp_OOS_Sharpe:13.3f}{r_.sp_OOS_MaxDD:13.1%}{r_.R0_OOS_MaxDD:10.1%}")
    for lab, sub in (("8a PASS", C[C.pass8a]), ("8a FAIL", C[~C.pass8a])):
        if len(sub):
            print(f"    {lab}: mean OOS Sharpe spread {sub.sp_OOS_Sharpe.mean():.3f}, "
                  f"mean OOS MaxDD spread {sub.sp_OOS_MaxDD.mean():.1%}")

    print("\n  which published conclusions rested on a non-selectable grid:")
    for _, r_ in C[~C.pass8a].iterrows():
        print(f"    {r_.universe:<6}{r_.grid:<15}{r_.a8:<24}{r_.prov}")

    print("\nLEADERBOARD rows written by hand from the tables above; "
          f"full grid -> {STEM}.grid.csv, cells -> {STEM}.cells.csv")


if __name__ == "__main__":
    main()
