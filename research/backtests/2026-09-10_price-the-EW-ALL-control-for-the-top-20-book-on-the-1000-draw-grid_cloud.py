#!/usr/bin/env python3
"""
IDEA 504 -- price-the-EW-ALL-control-for-the-top-20-book-on-the-1000-draw-grid
==============================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  idea 486 committed 6,000 books carrying both CAND-k and EWall metrics but did not restate
  EWall's halves, so 4a/4b were marked -1 for it.  Re-run the same 1,000 nested draws
  recording EWall H1/H2/OOS, and price the top-20 ranked book against its OWN
  eligible-equal-weight control per draw (dSharpe, dCAGR, dMaxDD) at 0/10/25 bps.  This is
  the de-grossed comparand idea 460 asks the record for, on the largest sub-panel grid it has.
  Max 2 params (cost rung, panel).

WHY THIS ONE MATTERS FOR CAPITAL
---------------------------------
  The standing KEEP-4b candidate (2026-09-04) IS a top-20 equal-weight book with no vol
  scaler.  Its published comparands are SPY and the live book.  Neither of those isolates the
  one thing the rule actually claims: that RANKING the eligible names and holding the best 20
  beats holding ALL of them at the same gross through the same gate.  EWall is that control.
  If dSharpe(CAND20 - EWall) is not reliably positive, the ranking clause is decoration and
  the KEEP is an exposure fact, not a selection fact.

STATED LIMITATION -- PROVENANCE OF "IDEA 486's 1,000 NESTED DRAWS"
------------------------------------------------------------------
  The queue cites idea 486's committed 6,000-book / 1,000-draw grid.  That artefact could not
  be located in research/backtests by any of: filename, a per-row CAND20+EWall header, a
  keep4a == -1 sentinel, or the strings "nested draw" / "747".  The nearest committed relative
  is `2026-09-09_what-n-would-make-the-partial-estimable_C.panels.csv` (960 rows, k=40,
  CAND10/CAND20/EWall/v2/SPY columns, q-stratified IDEA293 blocks) -- a DIFFERENT draw
  construction, so re-running "the same draws" bit-for-bit is not possible from the record.
  This run therefore RE-DERIVES the draw family deterministically and says so: the numbers
  below are a fresh 1,000-draw grid, not a restatement of 486's, and no claim here is
  conditioned on 486's rows.  The k=40 draw width is taken from the record's own committed
  k40 draws so the grid is comparable in shape.  Reported, not hidden.

DESIGN
------
  DRAW      seed s in 0..999 -> a deterministic permutation of the panel's tradable names;
            the sub-panel is its first k=40 names.  NESTED: for fixed s the k-prefixes are
            nested by construction, asserted in G5 across k in {20, 40, 60}.
  BOOKS     on each sub-panel P, all four through the SAME eligibility gate (above the 200d
            MA and vol20 < 0.60, the live cap) so only SELECTION and EXPOSURE differ:
              CAND20 top-20 of P by composite score at a FIXED 0.75/20 per name  (KEEP-4b)
              CAND5  top-5  of P at a fixed 0.75/5 per name
              EWall  EVERY eligible name in P sharing a full gross of 0.75
              EWmg   EVERY eligible name in P, equal weight, at CAND20's OWN gross that day
            CAND-n's fixed per-name weight de-grosses to cash when fewer than n names are
            eligible -- that is the incumbent's own convention (G3), and it means EWall is NOT
            gross-matched to it.  EWmg is, exactly, day by day: it is the control that isolates
            SELECTION alone, and it is reported beside EWall throughout rather than instead of
            it, because idea 311/460's standing complaint is precisely that a "control" which
            differs in exposure prices exposure and calls it signal.  Both are structural
            comparands, not tuned parameters.  Composite score is baseline.score(vol_scale=
            False) and the rank is taken over ALL of the sub-panel's columns -- the KEEP-4b
            candidate is "top-20 equal weight, NO vol scaler" and baseline ranks SPY with the
            rest; G3 pins both conventions against the published row.
  TUNED (2) COST RUNG (0 / 10 / 25 bps) and PANEL (U56 / B136 / SMALL439).
  FIXED     k=40, n in {5,20} structural, gross 0.75, cadence W, warm-up 260, IS/OOS split
            2016-12-31 / 2017-01-01 (PROTOCOL 8), 1,000 draws.  None chosen by outcome.

  EWall's H1/H2/OOS are recorded for every draw, which is exactly the gap the queue names, so
  BOTH KEEP paths are judged for EWall as well as for the ranked books -- no -1 sentinels.

PRE-REGISTERED GATES (printed before any new number is read)
-------------------------------------------------------------
  G1  fast_backtest == engine.backtest @10 bps                                  bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                        bar 0.0
  G3  the standing 2026-09-04 KEEP-4b incumbent re-derived on the FULL U56 panel:
      top-20 equal weight, no vol scaler, published 12.66% / 1.0921 / -18.31%   bar 5e-3
  G4  EWall holds exactly gross 0.75 on every day with an eligible name (it is de-grossed by
      the GATE and never by selection), and EWmg's realised daily gross equals CAND20's
  G5  the draws are actually nested: subpanel(s, 20) subset subpanel(s, 40) subset (s, 60)
  G6  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv is dropped first

SURVIVORSHIP (PROTOCOL 9)
--------------------------
  B136 is today's constituents; SMALL439 is the current sub-$2B screen only (see
  data/SMALL_PANEL_README.md) -- names that were acquired, delisted or grew out of the screen
  are absent, so every level on those two panels is biased upward.  The claim this run makes
  is a WITHIN-DRAW DIFFERENCE (CAND20 minus EWall on the same 40 names over the same days),
  which the same survivorship applies to on both sides and therefore largely differences out;
  the LEVELS are not tradeable estimates and are not offered as such.
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

COSTS = [0.0, 10.0, 25.0]        # TUNED axis 1
FREQ = "W"
BAND0, GROSS0 = 0.03, 0.75
K = 40                           # sub-panel width -- the record's own committed k40 draws
VOLCAP = 0.60                    # the live eligibility cap (G3 pins it against the incumbent)
NS = [5, 20]
DRAWS = 1000
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED0 = 504                      # stated seed, so the grid is reproducible bit-for-bit

# the standing 2026-09-04 KEEP-4b incumbent, as re-derived and published by idea 450
KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ------------------------------------------------------------------------------------------
def fast_backtest(prices, weights, freq=FREQ, cost=10.0):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1) - turn * cost / 1e4, index=idx)


def M0(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def ranked_w(sc, elig, n, gross):
    """Top-n by composite score among eligible names at a FIXED gross/n per name -- the
    incumbent's convention: fewer than n eligible means the book holds cash (G3)."""
    r = sc.where(elig).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def ewall_w(elig, gross):
    """EVERY eligible name in the sub-panel, equal weight, sharing a full gross."""
    sel = elig.astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(gross / k, axis=0).fillna(0.0)


def ewmg_w(elig, ref):
    """EVERY eligible name, equal weight, at REF's own gross each day -- the exactly
    gross-matched control, so the difference against ref is SELECTION and nothing else."""
    sel = elig.astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(ref.sum(axis=1) / k, axis=0).fillna(0.0)


def keeppaths(m, oos_s, mb, ms, spy_oos):
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > spy_oos)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b)


# ------------------------------------------------------------------------------------------
def load_panels():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL439"] = sm[keep]
    return panels, bad, len(sm.columns) - len(keep)


def tradables(px):
    return [c for c in px.columns if c != "SPY"]


def gates(panels, n_dropped):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]
    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights            : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= g2 == 0.0

    slow = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"]
    fast = fast_backtest(px, w, FREQ, 10.0)
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 fast_backtest == engine.backtest @10 bps            : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    # G3 -- the standing KEEP-4b incumbent: U56 top-20 EW, NO vol scaler, cap OFF
    sc, above, vol20 = score(px, vol_scale=False)
    tr = list(px.columns)                       # baseline ranks SPY with the rest (G3 pins it)
    elig = above[tr] & (vol20[tr] < VOLCAP)
    r = fast_backtest(px[tr], ranked_w(sc[tr], elig, 20, GROSS0), FREQ, 10.0).loc[j:]
    m = M(r)
    d = {k: abs(m[k] - v) for k, v in KEEP4B_INCUMBENT.items()}
    P(f"  G3 2026-09-04 KEEP-4b incumbent (U56 top-20 EW, no vol scaler) re-derived:")
    P(f"     got {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   "
      f"published {KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {max(d.values()):.3e}  "
      f"{'PASS' if max(d.values()) < 5e-3 else 'FAIL'}")
    ok &= max(d.values()) < 5e-3

    # G4 -- EWall over the whole panel is the plain gated equal-weight book, and EWmg is
    #       gross-matched to CAND20 day by day
    wa = ewall_w(elig, GROSS0)
    gsum = wa.sum(axis=1)
    any_el = elig.any(axis=1)
    g4a = float(np.abs(gsum[any_el] - GROSS0).max())
    ref = ranked_w(sc[tr], elig, 20, GROSS0)
    g4b = float(np.abs(ewmg_w(elig, ref).sum(axis=1) - ref.sum(axis=1)).max())
    P(f"  G4 EWall holds exactly gross 0.75 whenever any name is eligible (never de-grossed")
    P(f"     by selection, only by the gate)               : {g4a:.3e}  "
      f"{'PASS' if g4a < 1e-12 else 'FAIL'}")
    P(f"  G4b EWmg gross == CAND20 gross, every day              : {g4b:.3e}  "
      f"{'PASS' if g4b < 1e-12 else 'FAIL'}")
    ok &= (g4a < 1e-12) and (g4b < 1e-12)

    # G5 -- the draws are nested
    rng = np.random.default_rng(SEED0)
    names = tradables(panels["B136"])
    nest = True
    for s in range(20):
        perm = list(np.random.default_rng(SEED0 + s).permutation(names))
        nest &= set(perm[:20]) <= set(perm[:40]) <= set(perm[:60])
    P(f"  G5 draws nested across k in 20/40/60 (20 seeds checked) : "
      f"{'PASS' if nest else 'FAIL'}")
    ok &= nest

    P(f"  G6 SMALL439 dropped {n_dropped} tickers with max_1d_move >= 1.0  : "
      f"{'PASS' if n_dropped == 44 else 'CHECK'}")
    ok &= n_dropped > 0
    P()
    P(f"  GATES A: {'ALL PASS' if ok else 'FAILURE -- results below are not trustworthy'}")
    return ok


# ------------------------------------------------------------------------------------------
def run(panels):
    P()
    P("=" * 100)
    P(f"(B) THE GRID -- {DRAWS} nested draws x k={K} x 3 books x 3 cost rungs x "
      f"{len(panels)} panels")
    P("=" * 100)
    rows = []
    for pn, px in panels.items():
        start = px.index[WARM]
        names = tradables(px)
        sc, above, vol20 = score(px, vol_scale=False)
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = M(spy)
        spy_oos = M0(spy.loc[OOS_START:])
        base_all = {c: fast_backtest(px, rules_v2_weights(px, BAND0, GROSS0), FREQ, c).loc[start:]
                    for c in COSTS}
        mb_all = {c: M(v) for c, v in base_all.items()}
        P(f"  {pn}: {len(names)} tradable names   SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / "
          f"{ms['MaxDD']:.2%}  (H1 {ms['H1']:.4f}/H2 {ms['H2']:.4f})  OOS {spy_oos:.4f}")
        P(f"  {pn}: live RULES v2 @10 bps {mb_all[10.0]['CAGR']:.2%} / "
          f"{mb_all[10.0]['Sharpe']:.4f} / {mb_all[10.0]['MaxDD']:.2%}")
        kk = min(K, len(names))
        for s in range(DRAWS):
            sub = list(np.random.default_rng(SEED0 + s).permutation(names))[:kk]
            q = px[sub]
            el = above[sub] & (vol20[sub] < VOLCAP) & q.notna()
            W = {f"CAND{n}": ranked_w(sc[sub], el, n, GROSS0) for n in NS}
            W["EWall"] = ewall_w(el, GROSS0)
            W["EWmg"] = ewmg_w(el, W["CAND20"])
            for cost in COSTS:
                rec = dict(panel=pn, draw=s, k=kk, cost=cost)
                for bk, wt in W.items():
                    r = fast_backtest(q, wt, FREQ, cost).loc[start:]
                    m = M(r)
                    ro = r.loc[OOS_START:]
                    mo = M(ro)
                    p4a, p4b = keeppaths(m, mo["Sharpe"], mb_all[cost], ms, spy_oos)
                    rec.update({f"{bk}_CAGR": m["CAGR"], f"{bk}_Sharpe": m["Sharpe"],
                                f"{bk}_MaxDD": m["MaxDD"], f"{bk}_H1": m["H1"],
                                f"{bk}_H2": m["H2"],
                                f"{bk}_IS_Sharpe": M0(r.loc[:IS_END]),
                                f"{bk}_OOS_CAGR": mo["CAGR"],
                                f"{bk}_OOS_Sharpe": mo["Sharpe"],
                                f"{bk}_OOS_MaxDD": mo["MaxDD"],
                                f"{bk}_keep4a": p4a, f"{bk}_keep4b": p4b})
                rec.update(SPY_Sharpe=ms["Sharpe"], SPY_CAGR=ms["CAGR"], SPY_MaxDD=ms["MaxDD"],
                           SPY_OOS_Sharpe=spy_oos,
                           v2_Sharpe=mb_all[cost]["Sharpe"], v2_MaxDD=mb_all[cost]["MaxDD"],
                           v2_OOS_Sharpe=M0(base_all[cost].loc[OOS_START:]))
                rows.append(rec)
        P(f"  {pn}: {DRAWS} draws done")
    G = pd.DataFrame(rows)
    for a in ("Sharpe", "CAGR", "MaxDD", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "IS_Sharpe"):
        for n in NS:
            G[f"d{n}_{a}"] = G[f"CAND{n}_{a}"] - G[f"EWall_{a}"]
            G[f"m{n}_{a}"] = G[f"CAND{n}_{a}"] - G[f"EWmg_{a}"]
    dump(G, "draws")
    return G


# ------------------------------------------------------------------------------------------
def price(G):
    P()
    P("=" * 100)
    P("(C) THE PRICE OF THE RANKING CLAUSE -- CAND20 minus its OWN EWall control, per draw")
    P("=" * 100)
    for cost in COSTS:
        P()
        P(f"  --- cost {cost:.0f} bps " + "-" * 70)
        z = G[G.cost == cost]
        t = (z.groupby("panel")
              .agg(n=("d20_Sharpe", "size"),
                   dS_mean=("d20_Sharpe", "mean"), dS_med=("d20_Sharpe", "median"),
                   dS_sd=("d20_Sharpe", "std"), win=("d20_Sharpe", lambda x: float((x > 0).mean())),
                   dC_mean=("d20_CAGR", "mean"), dC_med=("d20_CAGR", "median"),
                   dD_mean=("d20_MaxDD", "mean"), dD_med=("d20_MaxDD", "median"),
                   dSo_mean=("d20_OOS_Sharpe", "mean"), dSo_med=("d20_OOS_Sharpe", "median"),
                   win_oos=("d20_OOS_Sharpe", lambda x: float((x > 0).mean()))))
        t["t_stat"] = t.dS_mean / (t.dS_sd / np.sqrt(t.n))
        P(t.to_string(float_format=lambda x: f"{x:.4f}"))
    P()
    P("  --- THE DECISIVE LEG: CAND20 minus EWmg, its EXACTLY GROSS-MATCHED control ---")
    P("  (same names eligible, same gate, same gross every day -- the only difference is that")
    P("   CAND20 ranks and EWmg does not, so this delta is SELECTION with exposure removed)")
    for cost in COSTS:
        z = G[G.cost == cost]
        t = (z.groupby("panel")
              .agg(n=("m20_Sharpe", "size"), dS_mean=("m20_Sharpe", "mean"),
                   dS_med=("m20_Sharpe", "median"), dS_sd=("m20_Sharpe", "std"),
                   win=("m20_Sharpe", lambda x: float((x > 0).mean())),
                   dC_med=("m20_CAGR", "median"), dD_med=("m20_MaxDD", "median"),
                   dSo_med=("m20_OOS_Sharpe", "median"),
                   win_oos=("m20_OOS_Sharpe", lambda x: float((x > 0).mean()))))
        t["t_stat"] = t.dS_mean / (t.dS_sd / np.sqrt(t.n))
        P(f"    cost {cost:.0f} bps")
        P(t.to_string(float_format=lambda x: f"{x:.4f}"))
    P()
    P("  EXPOSURE vs SELECTION, decomposed at 10 bps (median over 1,000 draws):")
    z = G[G.cost == 10.0]
    for pn, g in z.groupby("panel"):
        tot = g.d20_Sharpe.median()
        sel = g.m20_Sharpe.median()
        P(f"    {pn:<9} CAND20 - EWall {tot:+.4f}  =  SELECTION (vs EWmg) {sel:+.4f}  +  "
          f"EXPOSURE (EWmg - EWall) {tot - sel:+.4f}")
    P()
    P("  the same for CAND5 (a narrower book against the SAME control):")
    for cost in COSTS:
        z = G[G.cost == cost]
        t = z.groupby("panel").agg(dS_med=("d5_Sharpe", "median"),
                                   win=("d5_Sharpe", lambda x: float((x > 0).mean())),
                                   dC_med=("d5_CAGR", "median"), dD_med=("d5_MaxDD", "median"),
                                   dSo_med=("d5_OOS_Sharpe", "median"))
        P(f"    cost {cost:>4.0f} bps  " +
          "   ".join(f"{p}: dS {r.dS_med:+.4f} win {r.win:.3f} dCAGR {r.dC_med:+.4f} "
                     f"dDD {r.dD_med:+.4f} dOOS {r.dSo_med:+.4f}" for p, r in t.iterrows()))
    S = []
    for cost in COSTS:
        for pn, z in G[G.cost == cost].groupby("panel"):
            for n in NS:
                d = z[f"d{n}_Sharpe"]
                S.append(dict(panel=pn, cost=cost, n=n, N=len(d), mean=d.mean(),
                              median=d.median(), sd=d.std(), win=float((d > 0).mean()),
                              t=d.mean() / (d.std() / np.sqrt(len(d))),
                              p05=d.quantile(0.05), p95=d.quantile(0.95),
                              dCAGR=z[f"d{n}_CAGR"].median(),
                              dMaxDD=z[f"d{n}_MaxDD"].median(),
                              dOOS=z[f"d{n}_OOS_Sharpe"].median(),
                              win_OOS=float((z[f"d{n}_OOS_Sharpe"] > 0).mean()),
                              mg_mean=z[f"m{n}_Sharpe"].mean(),
                              mg_median=z[f"m{n}_Sharpe"].median(),
                              mg_win=float((z[f"m{n}_Sharpe"] > 0).mean()),
                              mg_t=z[f"m{n}_Sharpe"].mean()
                              / (z[f"m{n}_Sharpe"].std() / np.sqrt(len(z))),
                              mg_dCAGR=z[f"m{n}_CAGR"].median(),
                              mg_dMaxDD=z[f"m{n}_MaxDD"].median(),
                              mg_dOOS=z[f"m{n}_OOS_Sharpe"].median(),
                              mg_win_OOS=float((z[f"m{n}_OOS_Sharpe"] > 0).mean())))
    SS = pd.DataFrame(S)
    dump(SS, "summary")
    return SS


def keeps(G):
    P()
    P("=" * 100)
    P("(D) BOTH KEEP PATHS FOR ALL THREE BOOKS -- EWall's halves restated, no -1 sentinels")
    P("=" * 100)
    rows = []
    for (pn, cost), z in G.groupby(["panel", "cost"]):
        for bk in ["CAND5", "CAND20", "EWall", "EWmg"]:
            rows.append(dict(panel=pn, cost=cost, book=bk, n=len(z),
                             keep4a=int(z[f"{bk}_keep4a"].sum()),
                             keep4b=int(z[f"{bk}_keep4b"].sum()),
                             both=int((z[f"{bk}_keep4a"] & z[f"{bk}_keep4b"]).sum()),
                             rate4b=float(z[f"{bk}_keep4b"].mean())))
    K = pd.DataFrame(rows)
    P(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(K, "keeppaths")
    P()
    P("  4b pass RATE, CAND20 vs its own EWall control (the number the queue asks for):")
    for cost in COSTS:
        z = K[K.cost == cost]
        for pn in sorted(z.panel.unique()):
            a = z[(z.panel == pn) & (z.book == "CAND20")].rate4b.iloc[0]
            b = z[(z.panel == pn) & (z.book == "EWall")].rate4b.iloc[0]
            c5 = z[(z.panel == pn) & (z.book == "CAND5")].rate4b.iloc[0]
            P(f"    {cost:>4.0f} bps  {pn:<9} CAND20 {a:.4f}   EWall {b:.4f}   "
              f"CAND5 {c5:.4f}   CAND20-EWall {a - b:+.4f}")
    return K


def rule8(G):
    P()
    P("=" * 100)
    P("(E) RULE 8 -- choose the book on 2009-2016 IS Sharpe, score 2017-2026 untouched")
    P("=" * 100)
    books = ["CAND5", "CAND20", "EWall", "EWmg"]
    rows = []
    for (pn, cost), z in G.groupby(["panel", "cost"]):
        iss = z[[f"{b}_IS_Sharpe" for b in books]].values
        pick = np.array(books)[np.argmax(iss, axis=1)]
        oos = np.array([z[f"{b}_OOS_Sharpe"].values for b in books]).T
        chosen = oos[np.arange(len(z)), np.argmax(iss, axis=1)]
        always_ew = z["EWall_OOS_Sharpe"].values
        always_mg = z["EWmg_OOS_Sharpe"].values
        always_20 = z["CAND20_OOS_Sharpe"].values
        oracle = oos.max(axis=1)
        rows.append(dict(panel=pn, cost=cost, n=len(z),
                         pick_CAND5=float((pick == "CAND5").mean()),
                         pick_CAND20=float((pick == "CAND20").mean()),
                         pick_EWall=float((pick == "EWall").mean()),
                         pick_EWmg=float((pick == "EWmg").mean()),
                         chosen_OOS=chosen.mean(), alwaysEW_OOS=always_ew.mean(),
                         alwaysEWmg_OOS=always_mg.mean(),
                         always20_OOS=always_20.mean(), oracle_OOS=oracle.mean(),
                         regret=float((oracle - chosen).mean()),
                         beats_EW=float((chosen > always_ew).mean()),
                         SPY_OOS=z.SPY_OOS_Sharpe.iloc[0], v2_OOS=z.v2_OOS_Sharpe.iloc[0]))
    W = pd.DataFrame(rows)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(W, "walkforward")
    P()
    P("  reading: 'chosen_OOS' is the IS chooser's realised OOS Sharpe; 'alwaysEW_OOS' is the")
    P("  zero-decision control that never ranks anything.  If the chooser does not beat it,")
    P("  the record's ranking clause is not paying for its own selection step.")
    return W


def main():
    P("=" * 100)
    P("IDEA 504 -- price the EW-ALL control for the top-20 book on the 1,000-draw grid")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   costs {COSTS}   k={K}   "
      f"draws={DRAWS}   seed={SEED0}   IS<= {IS_END}   OOS >= {OOS_START}")
    P("=" * 100)
    panels, bad, ndrop = load_panels()
    for k, v in panels.items():
        P(f"  {k}: {v.shape[1]} columns  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"({len(v)} rows)")
    P("  SURVIVORSHIP (PROTOCOL 9): B136 and SMALL439 are today's constituents only -- levels")
    P("  biased up.  The headline is a WITHIN-DRAW difference, which differences most of it out.")
    P()
    ok = gates(panels, ndrop)
    G = run(panels)
    SS = price(G)
    KP = keeps(G)
    W = rule8(G)
    P()
    P("=" * 100)
    P("(F) SUMMARY")
    P("=" * 100)
    z = SS[(SS.cost == 10.0) & (SS.n == 20)]
    for _, r in z.iterrows():
        P(f"  {r.panel:<9} @10 bps  CAND20 - EWall  dSharpe median {r['median']:+.4f} "
          f"mean {r['mean']:+.4f} (t {r.t:+.2f}, win {r.win:.3f}, N {int(r.N)})   "
          f"dCAGR {r.dCAGR:+.4f}  dMaxDD {r.dMaxDD:+.4f}  dOOS {r.dOOS:+.4f} "
          f"(win {r.win_OOS:.3f})")
        P(f"  {'':<9}          CAND20 - EWmg   dSharpe median {r.mg_median:+.4f} "
          f"mean {r.mg_mean:+.4f} (t {r.mg_t:+.2f}, win {r.mg_win:.3f})   "
          f"dCAGR {r.mg_dCAGR:+.4f}  dMaxDD {r.mg_dMaxDD:+.4f}  dOOS {r.mg_dOOS:+.4f} "
          f"(win {r.mg_win_OOS:.3f})")
    P(f"  GATES: {'PASS' if ok else 'FAIL'}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
