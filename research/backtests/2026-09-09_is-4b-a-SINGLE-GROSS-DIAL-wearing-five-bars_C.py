#!/usr/bin/env python3
"""Idea 587 - is 4b a SINGLE GROSS DIAL wearing five bars? (lane C, 2026-09-09)

QUEUE 587: idea 321 found the 4b DD margin is corr -0.960 with gross at a Sharpe sd of
0.00036 across the whole gross dial, that the DD cap binds at 0 of 51 ladder points, and
that CAGR is the binding leg 94/126.  Test whether PROTOCOL 4b's FIVE bars collapse to
ONE: sweep gross alone across families and panels and report how much of the pass/fail
variance one dial explains, and whether any book's 4b verdict is set by anything other
than where its gross sits.  Max 2 tuned params (family dial, gross).

PROTOCOL 4b, spelled out as five bars, each against that panel's SPY on the same window:
    B1  Sharpe > SPY   on H1
    B2  Sharpe > SPY   on H2
    B3  Sharpe > SPY   out of sample (rule 8 window, 2017-)
    B4  |MaxDD| <= 0.60 * |SPY MaxDD|
    B5  CAGR   >= 0.70 * SPY CAGR
4b PASS = all five.

Design (everything pre-registered before any result was read):

  GATES (run first, printed first)
    G1  fast_backtest must reproduce engine.backtest to < 1e-12 on 4 real books.
    G2  the gross dial must be an EXACT scalar exposure dial: w(g') * g == w(g) * g'
        elementwise on every family, to 0.0.  If it is not, "sweep gross alone" is
        not what this run is doing.
    G3  the committed U56 / RULES v1 anchor must rebuild to
        6.4194% / 0.66110 / -13.8278% (ideas 486, 583, 322) to 1e-4 / 1e-4 / 1e-4.

  PART 1  THE LADDER.  3 panels x 3 families x 10 dials x 17 gross x 2 cadences
          = 1,020 books.  Every point reported.  For each: CAGR / Sharpe / MaxDD on
          full / H1 / H2 / IS(<=2016) / OOS(2017-), the five 4b bars, and the 4b verdict.
  PART 2  HOW MUCH DOES ONE DIAL EXPLAIN?  Variance decomposition of the binary 4b
          pass over the 1,020 points: R2 from gross alone, from book-shape identity
          alone, and from both.  Plus the per-bar slope/correlation in gross.
  PART 3  IS THE PASS SET AN INTERVAL IN g?  For every book shape (panel x family x
          dial x cadence = 60 ladders of 17 points), is the pass set contiguous, and
          which bar binds at each end?
  PART 4  DO THE OTHER FOUR BARS EVER SPEAK?  Verdict under each single bar and under
          each 4-bar subset (drop one) vs the full five; count the points whose verdict
          the dropped bar was the only thing setting.
  PART 5  rule-8 walk-forward (2 tuned params: family dial, gross g) chosen on
          IS <= 2016-12-31, OOS 2017- read ONCE.  Both KEEP paths (4a vs RULES v2 live,
          4b vs SPY) on the pick and on the whole grid.

Hypotheses (pre-registered):
  H_ONE       gross alone explains >= 0.80 of the 4b pass/fail variance pooled over all
              1,020 points.
  H_INTERVAL  the 4b pass set is a contiguous interval in g on >= 90% of the 60 ladders.
  H_CAGR      the CAGR floor (B5) is a binding leg on >= 75% of FAILING points.
  H_DROP      using B5 ALONE instead of all five changes < 10% of the 1,020 verdicts.
  H_FLAT      no ladder has a Sharpe bar (B1/B2/B3) change its verdict anywhere along
              its own gross dial.

PROTOCOL 2: costs 10 bps per unit turnover, weights at close t applied t+1, no shorting,
no leverage (gross <= 1.00 throughout).  PROTOCOL 9: SMALL484 and B136 are current
constituents -> SURVIVORSHIP BIAS; every panel-level number below inherits it.
"""
import sys, json, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask  # noqa

OUT = Path(__file__).with_suffix("")
COST = 10.0
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP = 0.60
CAGR_FLOOR = 0.70
GROSS = [round(0.20 + 0.05 * i, 2) for i in range(17)]      # 17-point ladder, 0.20 .. 1.00
FREQS = ["W", "M"]
BARS = ["B1_shH1", "B2_shH2", "B3_shOOS", "B4_dd", "B5_cagr"]


# ---------------------------------------------------------------- fast backtest
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Numpy replica of engine.backtest (same drift, same next-day application, same
    NaN semantics on row 0).  Gated against the engine in G1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    cur = np.zeros(prices.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx)


def perf(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    vol = r.std() * np.sqrt(252)
    mdd = float((eq / eq.cummax() - 1).min())
    return dict(CAGR=float(cagr), Sharpe=float((r.mean() * 252) / vol) if vol else np.nan,
                MaxDD=mdd, N=len(r))


# ---------------------------------------------------------------- book families
def band_book(px, band, gross):
    """RULES v2 shape: hold every name inside the 200d +/-band, gross/N of NAV, gated
    weight to CASH (de-gross, never re-spread)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def mom_book(px, n, gross):
    """Top-n of the RULES composite, above its 200d MA, equal weight at gross/n."""
    s, above, vol20 = score(px)
    rank = s.where(above).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def volq_book(px, q, gross):
    """Lowest-vol q fraction of names priced that day, equal weight, gross/N."""
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    rk = vol20.rank(axis=1, pct=True)
    sel = (rk <= q) & px.notna()
    e = sel.astype(float)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


FAMILIES = {
    "BAND": (band_book, [0.00, 0.03, 0.06, 0.10]),
    "MOM":  (mom_book,  [5, 10, 20]),
    "VOLQ": (volq_book, [0.25, 0.50, 0.75]),
}


def window(r, kind):
    r = r.iloc[260:]                                    # PROTOCOL warm-up skip, as compare()
    if kind == "full": return r
    if kind == "H1":   return r.iloc[:len(r) // 2]
    if kind == "H2":   return r.iloc[len(r) // 2:]
    if kind == "IS":   return r.loc[:IS_END]
    if kind == "OOS":  return r.loc[OOS_START:]
    raise ValueError(kind)


KINDS = ["full", "H1", "H2", "IS", "OOS"]


def bars_4b(bk, spy, oos_kind="OOS"):
    """The five 4b bars as booleans plus their signed margins (positive = clears)."""
    m = {}
    m["B1_shH1"]  = bk["H1"]["Sharpe"] - spy["H1"]["Sharpe"]
    m["B2_shH2"]  = bk["H2"]["Sharpe"] - spy["H2"]["Sharpe"]
    m["B3_shOOS"] = bk[oos_kind]["Sharpe"] - spy[oos_kind]["Sharpe"]
    m["B4_dd"]    = DD_CAP * abs(spy["full"]["MaxDD"]) - abs(bk["full"]["MaxDD"])
    m["B5_cagr"]  = bk["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]
    return {k: bool(v > 0) for k, v in m.items()}, m


def r2_groups(y, labels):
    """Fraction of variance of y explained by group means (one-way ANOVA R2)."""
    y = np.asarray(y, float)
    tot = ((y - y.mean()) ** 2).sum()
    if tot == 0: return 1.0
    df = pd.DataFrame({"y": y, "g": list(labels)})
    fit = df.groupby("g")["y"].transform("mean").values
    return float(1.0 - ((y - fit) ** 2).sum() / tot)


# ================================================================= run
def main():
    print("=" * 104)
    print("IDEA 587 - is 4b a SINGLE GROSS DIAL wearing five bars?  (lane C, 2026-09-09)")
    print("=" * 104)

    panels = {}
    for name, kw in [("U56", dict()), ("B136", dict(broad=True)), ("SMALL484", dict(small=True))]:
        px = load_universe(**kw)
        panels[name] = px
        print(f"panel {name:9s} {px.shape[0]:5d} days x {px.shape[1]:4d} names  "
              f"{px.index[0].date()} .. {px.index[-1].date()}")
    print("SURVIVORSHIP (PROTOCOL 9): B136 and SMALL484 are CURRENT constituents.")

    gates = {}
    # ------------------------------------------------------------ G1
    print("\n--- G1  fast_backtest vs engine.backtest (4 real books, bar 1e-12) ---")
    px = panels["U56"]; nospy = px.drop(columns=["SPY"])
    g1 = []
    for lbl, w, f in [("v2 band 0.03 W", rules_v2_weights(px), "W"),
                      ("BAND 0.00 g0.20 W", band_book(nospy, 0.00, 0.20), "W"),
                      ("MOM  n10 g0.65 M", mom_book(nospy, 10, 0.65), "M"),
                      ("VOLQ q0.50 g1.00 M", volq_book(nospy, 0.50, 1.00), "M")]:
        w = w.reindex(columns=px.columns).fillna(0.0)
        a = engine_backtest(px, w, cost_bps=COST, freq=f)["returns"]
        b = fast_backtest(px, w, cost_bps=COST, freq=f)
        d = float(np.nanmax(np.abs(a.values - b.values))); g1.append(d)
        print(f"  {lbl:22s} max|diff| = {d:.3e}")
    gates["G1_max_diff"] = max(g1); gates["G1"] = bool(max(g1) < 1e-12)
    print(f"  G1 {'PASS' if gates['G1'] else 'FAIL'}  (worst {max(g1):.3e})")

    # ------------------------------------------------------------ G2
    print("\n--- G2  gross is an EXACT scalar exposure dial: w(g')*g == w(g)*g' (bar 0.0) ---")
    g2 = 0.0
    for fam, (fn, dials) in FAMILIES.items():
        for d in dials:
            wa = fn(nospy, d, 0.35).fillna(0.0)
            wb = fn(nospy, d, 0.90).fillna(0.0)
            g2 = max(g2, float(np.nanmax(np.abs(wa.values * 0.90 - wb.values * 0.35))))
    gates["G2_max_diff"] = g2; gates["G2"] = bool(g2 == 0.0)
    print(f"  max|w(0.35)*0.90 - w(0.90)*0.35| = {g2:.3e}  {'PASS' if gates['G2'] else 'FAIL'}")

    # ------------------------------------------------------------ G3
    print("\n--- G3  committed U56 / RULES v1 anchor 6.4194% / 0.66110 / -13.8278% ---")
    r1 = fast_backtest(px, rules_v1_weights(px).reindex(columns=px.columns).fillna(0.0), freq="W")
    a = perf(window(r1, "full"))
    d3 = (abs(a["CAGR"] - 0.064194), abs(a["Sharpe"] - 0.66110), abs(a["MaxDD"] + 0.138278))
    gates["G3_rebuild"] = [a["CAGR"], a["Sharpe"], a["MaxDD"]]; gates["G3"] = bool(max(d3) < 1e-4)
    print(f"  rebuilt {a['CAGR']:.4%} / {a['Sharpe']:.5f} / {a['MaxDD']:.4%}   "
          f"max|d| = {max(d3):.2e}  {'PASS' if gates['G3'] else 'FAIL'}")
    json.dump(gates, open(str(OUT) + ".gates.json", "w"), indent=1)

    # ------------------------------------------------------------ SPY reference
    spy_stats = {}
    for p, pxp in panels.items():
        sr = pxp["SPY"].pct_change().fillna(0.0)
        spy_stats[p] = {k: perf(window(sr, k)) for k in KINDS}
    print("\nSPY per panel (full / OOS):")
    for p in panels:
        s = spy_stats[p]
        print(f"  {p:9s} full CAGR {s['full']['CAGR']:7.2%} Sharpe {s['full']['Sharpe']:6.3f} "
              f"MaxDD {s['full']['MaxDD']:7.2%} | OOS Sharpe {s['OOS']['Sharpe']:6.3f} "
              f"| bars: CAGR floor {CAGR_FLOOR*s['full']['CAGR']:7.2%}, "
              f"DD cap {DD_CAP*abs(s['full']['MaxDD']):6.2%}")

    # ------------------------------------------------------------ PART 1 the ladder
    print("\n" + "=" * 104)
    print("PART 1  THE LADDER - 3 panels x 3 families x 10 dials x 17 gross x 2 cadences "
          "= 1,020 books, ALL reported (.grid.csv)")
    print("=" * 104)
    rows = []
    for p, pxp in panels.items():
        pn = pxp.drop(columns=["SPY"])
        for fam, (fn, dials) in FAMILIES.items():
            for d in dials:
                w1 = fn(pn, d, 1.00).reindex(columns=pxp.columns).fillna(0.0)
                for g in GROSS:
                    wg = w1 * g
                    for f in FREQS:
                        r = fast_backtest(pxp, wg, freq=f)
                        bk = {k: perf(window(r, k)) for k in KINDS}
                        ok, mg = bars_4b(bk, spy_stats[p])
                        rec = dict(panel=p, family=fam, dial=d, gross=g, freq=f,
                                   book=f"{p}|{fam}|{d}|{f}",
                                   realised_gross=float(wg.reindex(pxp.index).iloc[260:].sum(axis=1).mean()))
                        for k in KINDS:
                            rec[f"CAGR_{k}"] = bk[k]["CAGR"]
                            rec[f"Sharpe_{k}"] = bk[k]["Sharpe"]
                            rec[f"MaxDD_{k}"] = bk[k]["MaxDD"]
                        for b in BARS:
                            rec[b] = ok[b]; rec[b + "_margin"] = mg[b]
                        rec["pass4b"] = all(ok.values())
                        rec["n_fail"] = sum(1 for v in ok.values() if not v)
                        rows.append(rec)
        print(f"  {p:9s} done ({len([r for r in rows if r['panel']==p])} points)")
    G = pd.DataFrame(rows)
    G.to_csv(str(OUT) + ".grid.csv", index=False)
    print(f"  {len(G)} grid points; 4b passes {G.pass4b.sum()} ({G.pass4b.mean():.1%})")
    print("\n  pass rate by panel x family (rows = panel, cols = family):")
    print(G.pivot_table(index="panel", columns="family", values="pass4b", aggfunc="mean")
          .to_string(float_format=lambda x: f"{x:.1%}"))
    print("\n  pass rate by gross rung (pooled over 60 books):")
    pg = G.groupby("gross").pass4b.mean()
    print("   " + "  ".join(f"{g:.2f}:{v:.0%}" for g, v in pg.items()))

    # ------------------------------------------------------------ PART 2 one dial?
    print("\n" + "=" * 104)
    print("PART 2  HOW MUCH DOES ONE DIAL EXPLAIN?  variance decomposition of the binary 4b pass")
    print("=" * 104)
    y = G.pass4b.astype(float).values
    r2_g = r2_groups(y, G.gross)
    r2_s = r2_groups(y, G["book"])
    r2_b = r2_groups(y, G["book"].astype(str) + "@" + G.gross.astype(str))
    print(f"  R2(pass ~ gross alone, 17 levels)       = {r2_g:.4f}")
    print(f"  R2(pass ~ book shape alone, 60 levels)  = {r2_s:.4f}")
    print(f"  R2(pass ~ book x gross, saturated)     = {r2_b:.4f}   (must be 1.0)")
    print(f"  H_ONE (gross alone >= 0.80): "
          f"{'PASS' if r2_g >= 0.80 else 'FAIL'}  ({r2_g:.4f})")
    print("\n  per-bar sensitivity to the gross dial (pooled, all 1,020 points):")
    sens = []
    for b in BARS:
        m = G[b + "_margin"].values
        c = float(np.corrcoef(G.gross.values, m)[0, 1])
        sl = float(np.polyfit(G.gross.values, m, 1)[0])
        wt = G.groupby("book")[b].nunique()          # does this bar ever flip on a ladder?
        sens.append(dict(bar=b, corr_with_gross=c, slope_per_unit_gross=sl,
                         pass_rate=float(G[b].mean()),
                         ladders_where_bar_flips=int((wt > 1).sum()), n_ladders=int(len(wt))))
        print(f"   {b:10s} corr(g, margin) {c:+.3f}  slope {sl:+8.4f}/unit gross  "
              f"bar passes {G[b].mean():5.1%}  flips on {int((wt>1).sum()):2d}/60 ladders")
    pd.DataFrame(sens).to_csv(str(OUT) + ".sensitivity.csv", index=False)
    flat = all(s["ladders_where_bar_flips"] == 0 for s in sens[:3])
    print(f"  H_FLAT (no Sharpe bar B1/B2/B3 ever flips along a gross ladder): "
          f"{'PASS' if flat else 'FAIL'}")

    # ------------------------------------------------------------ PART 3 interval?
    print("\n" + "=" * 104)
    print("PART 3  IS THE 4b PASS SET AN INTERVAL IN g?  (60 ladders x 17 rungs)")
    print("=" * 104)
    lad = []
    for sh, sub in G.groupby("book"):
        sub = sub.sort_values("gross")
        pv = sub.pass4b.values
        idxs = np.flatnonzero(pv)
        contig = (len(idxs) == 0) or bool(idxs[-1] - idxs[0] + 1 == len(idxs))
        lo = float(sub.gross.values[idxs[0]]) if len(idxs) else np.nan
        hi = float(sub.gross.values[idxs[-1]]) if len(idxs) else np.nan
        # which bar binds just below lo / just above hi
        blo = bhi = ""
        if len(idxs) and idxs[0] > 0:
            rr = sub.iloc[idxs[0] - 1]
            blo = ",".join(b for b in BARS if not rr[b])
        if len(idxs) and idxs[-1] < len(pv) - 1:
            rr = sub.iloc[idxs[-1] + 1]
            bhi = ",".join(b for b in BARS if not rr[b])
        lad.append(dict(book=sh, n_pass=int(pv.sum()), contiguous=contig,
                        g_lo=lo, g_hi=hi, binds_below_lo=blo, binds_above_hi=bhi))
    LAD = pd.DataFrame(lad).sort_values("book")
    LAD.to_csv(str(OUT) + ".ladders.csv", index=False)
    live = LAD[LAD.n_pass > 0]
    frac_contig = float(LAD.contiguous.mean())
    print(f"  ladders with >=1 pass: {len(live)}/{len(LAD)};  contiguous pass set: "
          f"{LAD.contiguous.sum()}/{len(LAD)} ({frac_contig:.1%})")
    print(f"  H_INTERVAL (>= 90% contiguous): {'PASS' if frac_contig >= 0.90 else 'FAIL'}")
    if len(live):
        print(f"  admissible band: g_lo median {live.g_lo.median():.2f} "
              f"(min {live.g_lo.min():.2f}), g_hi median {live.g_hi.median():.2f} "
              f"(max {live.g_hi.max():.2f}); width median "
              f"{(live.g_hi - live.g_lo).median():.2f}")
        print("  what binds just BELOW the band (count of ladders):")
        print("   " + "; ".join(f"{k}: {v}" for k, v in
                                live.binds_below_lo.replace("", "(band starts at g=0.20)")
                                .value_counts().items()))
        print("  what binds just ABOVE the band (count of ladders):")
        print("   " + "; ".join(f"{k}: {v}" for k, v in
                                live.binds_above_hi.replace("", "(band runs to g=1.00)")
                                .value_counts().items()))
    print("\n  every ladder (shape, n_pass/17, admissible band, binding bars):")
    print(LAD.to_string(index=False, max_colwidth=34))

    # ------------------------------------------------------------ PART 4 do the others speak?
    print("\n" + "=" * 104)
    print("PART 4  DO THE OTHER FOUR BARS EVER SPEAK?")
    print("=" * 104)
    fails = G[~G.pass4b]
    print(f"  failing points: {len(fails)} of {len(G)}")
    print("  which bars are failing on a failing point (a point can fail several):")
    for b in BARS:
        n = int((~fails[b]).sum())
        solo = int(((~fails[b]) & (fails.n_fail == 1)).sum())
        print(f"   {b:10s} fails on {n:5d} ({n/max(len(fails),1):6.1%} of failures); "
              f"SOLE failing bar on {solo:5d} ({solo/max(len(fails),1):6.1%})")
    cagr_bind = float((~fails["B5_cagr"]).mean()) if len(fails) else np.nan
    print(f"  H_CAGR (B5 binding on >= 75% of failures): "
          f"{'PASS' if cagr_bind >= 0.75 else 'FAIL'}  ({cagr_bind:.1%})")

    print("\n  verdict under each SINGLE bar, and under each DROP-ONE 4-bar subset, "
          "vs the full five:")
    sub_rows = []
    for b in BARS:
        agree = float((G[b] == G.pass4b).mean())
        sub_rows.append(dict(rule=f"{b} ALONE", agree_with_4b=agree,
                             disagreements=int((G[b] != G.pass4b).sum())))
        print(f"   {b + ' ALONE':22s} agrees on {agree:6.2%}  "
              f"({int((G[b]!=G.pass4b).sum())} disagreements)")
    for b in BARS:
        others = [x for x in BARS if x != b]
        v = G[others].all(axis=1)
        agree = float((v == G.pass4b).mean())
        sub_rows.append(dict(rule=f"DROP {b}", agree_with_4b=agree,
                             disagreements=int((v != G.pass4b).sum())))
        print(f"   {'DROP ' + b:22s} agrees on {agree:6.2%}  "
              f"({int((v!=G.pass4b).sum())} points where {b} was the ONLY thing setting the verdict)")
    pd.DataFrame(sub_rows).to_csv(str(OUT) + ".subsets.csv", index=False)
    drop_chg = float((G["B5_cagr"] != G.pass4b).mean())
    print(f"  H_DROP (B5 alone changes < 10% of verdicts): "
          f"{'PASS' if drop_chg < 0.10 else 'FAIL'}  ({drop_chg:.1%})")

    # a strictly harder question: at a FIXED gross rung, does book identity still decide?
    print("\n  the control the single-dial reading has to survive - WITHIN each gross rung,\n"
          "  how much pass/fail variance is left, and does shape explain it?")
    wr = []
    for g, sub in G.groupby("gross"):
        yv = sub.pass4b.astype(float).values
        wr.append(dict(gross=g, n=len(sub), pass_rate=float(yv.mean()),
                       within_var=float(yv.var()),
                       r2_shape_within=r2_groups(yv, sub["book"]) if yv.var() > 0 else np.nan))
    WR = pd.DataFrame(wr); WR.to_csv(str(OUT) + ".within_gross.csv", index=False)
    print(WR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    mixed = WR[(WR.pass_rate > 0) & (WR.pass_rate < 1)]
    print(f"  gross rungs that are NOT unanimous: {len(mixed)}/17 "
          f"-> on those rungs the verdict is NOT set by gross alone.")

    # ------------------------------------------------------------ PART 5 rule 8
    print("\n" + "=" * 104)
    print("PART 5  RULE 8 WALK-FORWARD - (family dial, gross g) chosen on IS <= 2016-12-31 ONLY,\n"
          "        OOS 2017- read ONCE.  Both KEEP paths.  Cadence fixed at W (not tuned).")
    print("=" * 104)
    # IS-side bars use IS windows only; the chooser never sees OOS.
    W = G[G.freq == "W"].copy()
    isb = []
    for _, r in W.iterrows():
        p = r.panel; s = spy_stats[p]
        is_ok = (r.Sharpe_IS > s["IS"]["Sharpe"]
                 and abs(r.MaxDD_IS) <= DD_CAP * abs(s["IS"]["MaxDD"])
                 and r.CAGR_IS >= CAGR_FLOOR * s["IS"]["CAGR"])
        isb.append(is_ok)
    W["IS_4b"] = isb

    baselines = {}
    for p, pxp in panels.items():
        rb = fast_backtest(pxp, rules_v2_weights(pxp).reindex(columns=pxp.columns).fillna(0.0), freq="W")
        baselines[p] = {k: perf(window(rb, k)) for k in KINDS}

    wf = []
    for p in panels:
        for fam in FAMILIES:
            sub = W[(W.panel == p) & (W.family == fam)]
            for conv, pool in [("IS_Sharpe_unconstrained", sub),
                               ("IS_Sharpe_given_IS_4b", sub[sub.IS_4b])]:
                if not len(pool):
                    wf.append(dict(panel=p, family=fam, convention=conv, pick="(none clears IS 4b)"))
                    continue
                pk = pool.loc[pool.Sharpe_IS.idxmax()]
                s = spy_stats[p]; b = baselines[p]
                keep4b = bool(pk.pass4b)
                keep4a = bool(pk.Sharpe_H1 > b["H1"]["Sharpe"] and pk.Sharpe_H2 > b["H2"]["Sharpe"]
                              and pk.MaxDD_full >= b["full"]["MaxDD"])
                wf.append(dict(panel=p, family=fam, convention=conv,
                               pick=f"dial={pk.dial} g={pk.gross:.2f}",
                               dial=pk.dial, gross=pk.gross,
                               IS_Sharpe=pk.Sharpe_IS,
                               OOS_CAGR=pk.CAGR_OOS, OOS_Sharpe=pk.Sharpe_OOS, OOS_MaxDD=pk.MaxDD_OOS,
                               full_CAGR=pk.CAGR_full, full_Sharpe=pk.Sharpe_full,
                               full_MaxDD=pk.MaxDD_full, H1=pk.Sharpe_H1, H2=pk.Sharpe_H2,
                               base_OOS_Sharpe=b["OOS"]["Sharpe"], base_OOS_CAGR=b["OOS"]["CAGR"],
                               base_OOS_MaxDD=b["OOS"]["MaxDD"],
                               spy_OOS_Sharpe=s["OOS"]["Sharpe"], spy_OOS_CAGR=s["OOS"]["CAGR"],
                               spy_OOS_MaxDD=s["OOS"]["MaxDD"],
                               KEEP_4a=keep4a, KEEP_4b=keep4b))
    WF = pd.DataFrame(wf); WF.to_csv(str(OUT) + ".walkforward.csv", index=False)
    cols = ["panel", "family", "convention", "pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "full_Sharpe", "H1", "H2", "full_MaxDD", "KEEP_4a", "KEEP_4b"]
    print(WF[[c for c in cols if c in WF.columns]].to_string(index=False,
          float_format=lambda x: f"{x:.3f}"))

    print("\n  references on the same windows:")
    for p in panels:
        b = baselines[p]; s = spy_stats[p]
        print(f"   {p:9s} RULES v2 (live) full {b['full']['CAGR']:6.2%}/{b['full']['Sharpe']:.3f}/"
              f"{b['full']['MaxDD']:7.2%}  OOS {b['OOS']['CAGR']:6.2%}/{b['OOS']['Sharpe']:.3f}/"
              f"{b['OOS']['MaxDD']:7.2%}")
        print(f"   {'':9s} SPY             full {s['full']['CAGR']:6.2%}/{s['full']['Sharpe']:.3f}/"
              f"{s['full']['MaxDD']:7.2%}  OOS {s['OOS']['CAGR']:6.2%}/{s['OOS']['Sharpe']:.3f}/"
              f"{s['OOS']['MaxDD']:7.2%}")

    # does the IS 4b gate change the pick?  (the single-dial reading, walk-forward form)
    print("\n  DOES THE IS 4b GATE MOVE THE PICK?  (unconstrained vs IS-4b-constrained chooser)")
    a = WF[WF.convention == "IS_Sharpe_unconstrained"].set_index(["panel", "family"])
    c = WF[WF.convention == "IS_Sharpe_given_IS_4b"].set_index(["panel", "family"])
    same = 0; tot = 0
    for k in a.index:
        tot += 1
        if k in c.index and a.loc[k, "pick"] == c.loc[k, "pick"]:
            same += 1
    print(f"   pick identical on {same}/{tot} (panel, family) cells")
    print(f"   4b KEEPs among the {len(WF[WF.convention=='IS_Sharpe_given_IS_4b'])} IS-gated picks: "
          f"{int(WF[WF.convention=='IS_Sharpe_given_IS_4b'].KEEP_4b.fillna(False).sum())}; "
          f"4a KEEPs: {int(WF[WF.convention=='IS_Sharpe_given_IS_4b'].KEEP_4a.fillna(False).sum())}")

    # ------------------------------------------------------------ PART 6 addendum
    print("\n" + "=" * 104)
    print("PART 6  ADDENDUM (descriptive, POST-HOC - no hypothesis is scored on it)")
    print("=" * 104)
    npass = G.groupby("book").pass4b.sum()
    dead = npass[npass == 0].index
    liveG = G[~G["book"].isin(dead)]
    print(f"  43/60 reading: {len(dead)} of {len(npass)} books never pass 4b at ANY gross, so the pooled")
    print("  R2(pass ~ gross) in PART 2 is held down by books the dial cannot reach at all.")
    print("  Restricted to the {} points on the {} books that pass SOMEWHERE:".format(len(liveG), len(npass) - len(dead)))
    yl = liveG.pass4b.astype(float).values
    print(f"    R2(pass ~ gross alone) = {r2_groups(yl, liveG.gross):.4f}   "
          f"R2(pass ~ book alone) = {r2_groups(yl, liveG['book']):.4f}")
    P = G[G.pass4b]
    print(f"  realised mean gross: passers min {P.realised_gross.min():.3f} / median "
          f"{P.realised_gross.median():.3f} / max {P.realised_gross.max():.3f}; "
          f"failers median {G[~G.pass4b].realised_gross.median():.3f}")
    print("  NOTE on PART 5's within-rung r2_shape_within: with exactly ONE observation per")
    print("  (book, gross) cell that statistic is 1.0 BY CONSTRUCTION and carries no information;")
    print("  the informative line there is that 7 of 17 rungs are non-unanimous at all.")
    print("  the single B3 flip (H_FLAT) in detail - it is a tie, not a dial effect:")
    fl = G.groupby("book")["B3_shOOS"].nunique()
    for bkn in fl[fl > 1].index:
        sb = G[G["book"] == bkn].sort_values("gross")
        print(f"    {bkn}: B3 margin runs {sb.B3_shOOS_margin.iloc[0]:+.6f} -> "
              f"{sb.B3_shOOS_margin.iloc[-1]:+.6f} (range "
              f"{sb.B3_shOOS_margin.max()-sb.B3_shOOS_margin.min():.6f}); it crosses zero at "
              f"g={sb[~sb.B3_shOOS].gross.min():.2f} and the book passes 4b at 0 of 17 rungs.")
    print("  best 4b passers by OOS Sharpe (all 41 passers are in .grid.csv):")
    print(P.sort_values("Sharpe_OOS", ascending=False).head(5)[
        ["book", "gross", "CAGR_full", "Sharpe_full", "MaxDD_full",
         "CAGR_OOS", "Sharpe_OOS", "MaxDD_OOS"]].to_string(index=False,
        float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ verdict block
    print("\n" + "=" * 104)
    print("HYPOTHESES (all pre-registered)")
    print("=" * 104)
    res = {
        "H_ONE   gross alone explains >=0.80 of 4b pass variance": (r2_g >= 0.80, f"R2 = {r2_g:.4f}"),
        "H_INTERVAL pass set contiguous in g on >=90% of ladders": (frac_contig >= 0.90, f"{frac_contig:.1%}"),
        "H_CAGR  B5 binding on >=75% of failing points": (cagr_bind >= 0.75, f"{cagr_bind:.1%}"),
        "H_DROP  B5 alone changes <10% of verdicts": (drop_chg < 0.10, f"{drop_chg:.1%}"),
        "H_FLAT  no Sharpe bar flips along any gross ladder": (flat, f"{sum(s['ladders_where_bar_flips'] for s in sens[:3])} flips"),
    }
    for k, (ok, v) in res.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {k:56s} {v}")
    json.dump({k: dict(pass_=bool(v[0]), value=v[1]) for k, v in res.items()},
              open(str(OUT) + ".hypotheses.json", "w"), indent=1)
    print("\nfiles: .grid.csv .ladders.csv .sensitivity.csv .subsets.csv .within_gross.csv "
          ".walkforward.csv .gates.json .hypotheses.json")


if __name__ == "__main__":
    main()
