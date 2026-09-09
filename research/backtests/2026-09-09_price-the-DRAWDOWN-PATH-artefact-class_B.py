#!/usr/bin/env python3
"""Idea 321 - price the DRAWDOWN-PATH artefact class (lane B, 2026-09-09).

QUEUE 321: idea 318 found dMaxDD identical to 3 decimals (+0.314 pp) across three
different q settings on U56, i.e. ONE episode set the whole drawdown delta, and
PROTOCOL 4b's DD test turns on exactly that number.  Census the KEEP-path DD margins:
how many 4b passes/failures are decided by a margin smaller than the single worst
episode's contribution?  If most are, 4b's DD cap is a one-episode coin flip and needs
a second drawdown statistic (2nd-worst DD, or time-under-water).

Design (everything pre-registered before any result was read):

  GATES (run first, printed first)
    G1  fast_backtest must reproduce engine.backtest to < 1e-12 on 4 real books.
    G2  episode decomposition identity: max over disjoint underwater episodes == MaxDD
        exactly (0.0) on every book and on SPY.
    G3  the 2nd-worst episode must be a DIFFERENT, DISJOINT episode (no overlap with
        the worst) on every book - otherwise "contribution" is not defined.

  PART 1  REBUILD.  126 books (3 panels x {band gate 4 bands x 3 gross x 2 cadences}
          + {top-n momentum 3 n x 3 gross x 2 cadences}).  For each, on full / H1 / H2 /
          IS(<=2016) / OOS(2017-): CAGR, Sharpe, MaxDD, DD2 (2nd-worst disjoint episode),
          worst-episode contribution c = |DD1| - |DD2|, Ulcer, TUW, and the 4b DD margin
          against that panel's SPY on the same window.
  PART 2  CENSUS the record: every committed CSV that publishes a book MaxDD and a SPY
          MaxDD in the same row -> the record's own distribution of 4b DD margins, read
          against the rebuilt contribution scale.
  PART 3  Is the DD statistic STABLE?  IS->OOS Spearman across books for MaxDD vs DD2 vs
          Ulcer vs TUW; and does swapping the 4b cap onto a second statistic move the
          pass set?
  PART 4  rule-8 walk-forward + both KEEP paths.  2 tuned params (band b, gross g).

Hypotheses (pre-registered):
  H_FLIP  >=25% of rebuilt 4b DD verdicts change when BOTH arms are read on their
          2nd-worst episode instead of their worst.
  H_SAME  the worst episode is the same calendar episode for >=80% of books in a panel.
  H_STAB  IS->OOS Spearman is LOWER for MaxDD than for Ulcer and TUW.
  H_SWAP  swapping MaxDD for Ulcer at the same 0.60 cap changes >=20% of DD verdicts.
  H_REC   >= half the record's published 4b DD margins are smaller than the rebuilt
          median contribution.

Costs 10 bps, next-day execution, no shorting, no leverage (PROTOCOL 2).
"""
import sys, glob, csv, json, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics as engine_metrics  # noqa

OUT = Path(__file__).with_suffix("")
COST = 10.0
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP = 0.60          # PROTOCOL 4b: MaxDD <= 60% of SPY's
CAGR_FLOOR = 0.70      # PROTOCOL 4b: CAGR >= 70% of SPY's


# ---------------------------------------------------------------- fast backtest
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Numpy replica of engine.backtest (same drift, same next-day application,
    same NaN semantics on row 0).  Gated against the engine in G1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    cur = np.zeros(prices.shape[1])
    held = np.empty_like(rets)
    turn = np.empty(n)
    turn[:] = 0.0
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


# ---------------------------------------------------------------- dd statistics
def dd_episodes(r):
    """Disjoint underwater episodes of the equity curve.  Returns (depths, spans) with
    depths <= 0, ordered deepest first; spans are (start_pos, trough_pos, end_pos)."""
    eq = (1.0 + r.fillna(0.0)).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1.0
    under = dd < 0
    out = []
    i = 0
    n = len(dd)
    while i < n:
        if not under[i]:
            i += 1
            continue
        j = i
        while j < n and under[j]:
            j += 1
        seg = dd[i:j]
        t = int(np.argmin(seg))
        out.append((float(seg[t]), (i, i + t, j - 1)))
        i = j
    out.sort(key=lambda x: x[0])
    return [d for d, _ in out], [s for _, s in out], pd.Series(dd, index=r.index)


def dd_stats(r):
    depths, spans, dd = dd_episodes(r)
    d1 = depths[0] if depths else 0.0
    d2 = depths[1] if len(depths) > 1 else 0.0
    under = (dd < 0).values
    # longest underwater run
    best = run = 0
    for u in under:
        run = run + 1 if u else 0
        best = max(best, run)
    return dict(MaxDD=d1, DD2=d2, contrib_pp=(abs(d1) - abs(d2)) * 100,
                Ulcer=float(np.sqrt((dd.values ** 2).mean())),
                TUW=best / len(dd) if len(dd) else np.nan,
                n_ep=len(depths),
                worst_year=int(r.index[spans[0][1]].year) if spans else -1,
                worst_span=spans[0] if spans else None)


def spearman(a, b):
    """Rank correlation, no scipy dependency."""
    return float(pd.Series(a).rank().corr(pd.Series(b).rank()))


def perf(r):
    r = r.dropna()
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    vol = r.std() * np.sqrt(252)
    d = dd_stats(r)
    d.update(CAGR=cagr, Sharpe=(r.mean() * 252) / vol if vol else np.nan, N=len(r))
    return d


# ---------------------------------------------------------------- book family
def band_book(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def mom_book(px, n, gross):
    s, above, vol20 = score(px)
    elig = s.where(above)
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


BANDS = [0.00, 0.03, 0.06, 0.10]
GROSS = [0.50, 0.75, 1.00]
NS = [5, 10, 20]
FREQS = ["W", "M"]


def build_grid(px, panel, spy):
    rows = []
    for f in FREQS:
        for g in GROSS:
            for b in BANDS:
                w = band_book(px.drop(columns=["SPY"], errors="ignore"), b, g)
                r = fast_backtest(px, w.reindex(columns=px.columns).fillna(0.0), freq=f)
                rows.append(dict(panel=panel, family="BAND", dial=b, gross=g, freq=f, ret=r))
            for n in NS:
                w = mom_book(px.drop(columns=["SPY"], errors="ignore"), n, g)
                r = fast_backtest(px, w.reindex(columns=px.columns).fillna(0.0), freq=f)
                rows.append(dict(panel=panel, family="MOM", dial=n, gross=g, freq=f, ret=r))
    return rows


# ================================================================= run
def main():
    print("=" * 100)
    print("IDEA 321 - price the DRAWDOWN-PATH artefact class (lane B, 2026-09-09)")
    print("=" * 100)

    panels = {}
    for name, kw in [("U56", dict()), ("B136", dict(broad=True)), ("SMALL484", dict(small=True))]:
        px = load_universe(**kw)
        panels[name] = px
        print(f"panel {name:9s} {px.shape[0]:5d} days x {px.shape[1]:4d} names  "
              f"{px.index[0].date()} .. {px.index[-1].date()}")

    # ------------------------------------------------------------ G1
    print("\n--- G1  fast_backtest vs engine.backtest (4 real books) ---")
    g1 = []
    px = panels["U56"]
    for lbl, w, f in [("v2 band 0.03 W", rules_v2_weights(px), "W"),
                      ("band 0.00 g1.00 W", band_book(px.drop(columns=['SPY']), 0.00, 1.00), "W"),
                      ("mom n5 g0.75 M", mom_book(px.drop(columns=['SPY']), 5, 0.75), "M"),
                      ("band 0.10 g0.50 M", band_book(px.drop(columns=['SPY']), 0.10, 0.50), "M")]:
        w = w.reindex(columns=px.columns).fillna(0.0)
        a = engine_backtest(px, w, cost_bps=COST, freq=f)["returns"]
        b = fast_backtest(px, w, cost_bps=COST, freq=f)
        d = float(np.nanmax(np.abs(a.values - b.values)))
        g1.append(d)
        print(f"  {lbl:22s} max|diff| = {d:.3e}")
    G1 = max(g1) < 1e-12
    print(f"  G1 {'PASS' if G1 else 'FAIL'} (bar 1e-12, worst {max(g1):.3e})")

    # ------------------------------------------------------------ build all books
    print("\n--- building the 126-book grid ---")
    books = []
    for name, px in panels.items():
        books += build_grid(px, name, px["SPY"])
    print(f"  {len(books)} books built")

    spy_ret = {n: px["SPY"].pct_change().fillna(0.0) for n, px in panels.items()}

    def window(r, kind, panel):
        r = r.iloc[260:]                       # PROTOCOL warm-up skip, as in compare()
        if kind == "full":  return r
        if kind == "H1":    return r.iloc[:len(r) // 2]
        if kind == "H2":    return r.iloc[len(r) // 2:]
        if kind == "IS":    return r.loc[:IS_END]
        if kind == "OOS":   return r.loc[OOS_START:]

    KINDS = ["full", "H1", "H2", "IS", "OOS"]
    spy_stats = {}
    for p in panels:
        for k in KINDS:
            spy_stats[(p, k)] = perf(window(spy_ret[p], k, p))

    # ------------------------------------------------------------ G2 / G3
    print("\n--- G2  episode identity  /  G3  disjoint 2nd-worst ---")
    g2 = 0.0; g3 = True
    series = [(window(bk["ret"], k, bk["panel"]).dropna(), True) for bk in books for k in KINDS]
    series += [(window(spy_ret[p], k, p).dropna(), False) for p in panels for k in KINDS]
    for r, is_book in series:
        depths, spans, _ = dd_episodes(r)
        eq = (1 + r).cumprod()
        g2 = max(g2, abs(min(depths) - float((eq / eq.cummax() - 1).min())))
        if is_book and len(spans) > 1:
            a, b2 = spans[0], spans[1]
            if not (a[2] < b2[0] or b2[2] < a[0]):
                g3 = False
    G2 = g2 == 0.0
    print(f"  G2 max|episode-max - MaxDD| = {g2:.3e}  {'PASS' if G2 else 'FAIL'} (bar exactly 0.0)")
    print(f"  G3 worst and 2nd-worst episodes disjoint on every book: {'PASS' if g3 else 'FAIL'}")

    # ------------------------------------------------------------ PART 1 table
    print("\n" + "=" * 100)
    print("PART 1  REBUILD - every grid point (full table committed to .grid.csv)")
    print("=" * 100)
    rows = []
    for bk in books:
        rec = dict(panel=bk["panel"], family=bk["family"], dial=bk["dial"],
                   gross=bk["gross"], freq=bk["freq"])
        for k in KINDS:
            m = perf(window(bk["ret"], k, bk["panel"]))
            s = spy_stats[(bk["panel"], k)]
            rec[f"{k}_CAGR"] = m["CAGR"]; rec[f"{k}_Sharpe"] = m["Sharpe"]
            rec[f"{k}_MaxDD"] = m["MaxDD"]; rec[f"{k}_DD2"] = m["DD2"]
            rec[f"{k}_contrib_pp"] = m["contrib_pp"]; rec[f"{k}_Ulcer"] = m["Ulcer"]
            rec[f"{k}_TUW"] = m["TUW"]; rec[f"{k}_nep"] = m["n_ep"]
            rec[f"{k}_worstyear"] = m["worst_year"]
            rec[f"{k}_spy_MaxDD"] = s["MaxDD"]; rec[f"{k}_spy_DD2"] = s["DD2"]
            rec[f"{k}_spy_Ulcer"] = s["Ulcer"]; rec[f"{k}_spy_TUW"] = s["TUW"]
            rec[f"{k}_spy_worstyear"] = s["worst_year"]
            # 4b DD margin in pp: positive = passes the cap
            rec[f"{k}_margin_pp"] = (DD_CAP * abs(s["MaxDD"]) - abs(m["MaxDD"])) * 100
            rec[f"{k}_margin2_pp"] = (DD_CAP * abs(s["DD2"]) - abs(m["DD2"])) * 100
            rec[f"{k}_ddpass"] = rec[f"{k}_margin_pp"] >= 0
            rec[f"{k}_ddpass2"] = rec[f"{k}_margin2_pp"] >= 0
            rec[f"{k}_ulcpass"] = (DD_CAP * s["Ulcer"] - m["Ulcer"]) >= 0
            rec[f"{k}_tuwpass"] = (DD_CAP * s["TUW"] - m["TUW"]) >= 0
        rows.append(rec)
    G = pd.DataFrame(rows)
    G.to_csv(str(OUT) + ".grid.csv", index=False)
    print(f"  {len(G)} books x {len(KINDS)} windows written to {Path(str(OUT) + '.grid.csv').name}")

    print("\n  worst-episode CONTRIBUTION c = |MaxDD| - |DD2|, in pp, by panel (full sample):")
    for p in panels:
        sub = G[G.panel == p]
        s = spy_stats[(p, "full")]
        print(f"    {p:9s} books: median {sub.full_contrib_pp.median():6.2f}  "
              f"IQR [{sub.full_contrib_pp.quantile(.25):5.2f}, {sub.full_contrib_pp.quantile(.75):5.2f}]  "
              f"max {sub.full_contrib_pp.max():6.2f}   |  SPY c = "
              f"{(abs(s['MaxDD'])-abs(s['DD2']))*100:6.2f} pp "
              f"(MaxDD {s['MaxDD']:.2%} in {s['worst_year']}, DD2 {s['DD2']:.2%})")
    med_c = float(G.full_contrib_pp.median())
    print(f"\n  POOLED median contribution c = {med_c:.2f} pp  <- the scale everything is read against")

    print("\n  4b DD margin |0.60*SPY_MaxDD| - |MaxDD| (pp, full sample), by panel:")
    for p in panels:
        sub = G[G.panel == p]
        print(f"    {p:9s} median {sub.full_margin_pp.median():7.2f}  "
              f"pass {int(sub.full_ddpass.sum()):2d}/{len(sub)}  "
              f"|margin| < c on {int((sub.full_margin_pp.abs() < sub.full_contrib_pp).sum()):2d}/{len(sub)}")

    # ------------------------------------------------------------ H_FLIP
    print("\n" + "=" * 100)
    print("H_FLIP  - does the 4b DD verdict change when BOTH arms are read on their 2nd-worst episode?")
    print("=" * 100)
    for k in KINDS:
        flip = (G[f"{k}_ddpass"] != G[f"{k}_ddpass2"])
        thin = (G[f"{k}_margin_pp"].abs() < G[f"{k}_contrib_pp"])
        print(f"  {k:5s}  DD-pass {int(G[f'{k}_ddpass'].sum()):3d}/{len(G)}   "
              f"2nd-worst-episode pass {int(G[f'{k}_ddpass2'].sum()):3d}/{len(G)}   "
              f"VERDICT FLIPS {int(flip.sum()):3d}/{len(G)} = {flip.mean():.1%}   "
              f"|margin| < c on {thin.mean():.1%}")
    flip_full = (G.full_ddpass != G.full_ddpass2).mean()
    H_FLIP = flip_full >= 0.25
    print(f"\n  H_FLIP ({'HOLDS' if H_FLIP else 'FAILS'}): full-sample flip rate {flip_full:.1%} vs a 25% bar")

    # ------------------------------------------------------------ H_SAME
    print("\n" + "=" * 100)
    print("H_SAME  - is one calendar episode setting every book's MaxDD?")
    print("=" * 100)
    for p in panels:
        for k in ["full", "IS", "OOS"]:
            sub = G[G.panel == p]
            vc = sub[f"{k}_worstyear"].value_counts()
            top = vc.index[0]; share = vc.iloc[0] / len(sub)
            spy_y = spy_stats[(p, k)]["worst_year"]
            print(f"  {p:9s} {k:4s}  modal worst-episode year {top}  on {share:.0%} of books "
                  f"({dict(vc.head(3))})   SPY's own: {spy_y}")
    shares = []
    for p in panels:
        sub = G[G.panel == p]
        shares.append(sub.full_worstyear.value_counts().iloc[0] / len(sub))
    H_SAME = min(shares) >= 0.80
    print(f"\n  H_SAME ({'HOLDS' if H_SAME else 'FAILS'}): min panel concentration {min(shares):.0%} vs an 80% bar")

    # ------------------------------------------------------------ PART 3 stability + swap
    print("\n" + "=" * 100)
    print("PART 3  - IS->OOS stability of each drawdown statistic, and the swap test")
    print("=" * 100)
    print("  Spearman rank correlation across books, IS(<=2016) vs OOS(2017-):")
    stab = {}
    for stat in ["MaxDD", "DD2", "Ulcer", "TUW", "Sharpe", "CAGR"]:
        per = []
        for p in panels:
            sub = G[G.panel == p]
            per.append(spearman(sub[f"IS_{stat}"].values, sub[f"OOS_{stat}"].values))
        stab[stat] = per
        print(f"    {stat:7s}  U56 {per[0]:+.3f}   B136 {per[1]:+.3f}   SMALL484 {per[2]:+.3f}   "
              f"mean {np.mean(per):+.3f}")
    H_STAB = np.mean(stab["MaxDD"]) < min(np.mean(stab["Ulcer"]), np.mean(stab["TUW"]))
    print(f"\n  H_STAB ({'HOLDS' if H_STAB else 'FAILS'}): MaxDD mean {np.mean(stab['MaxDD']):+.3f} vs "
          f"Ulcer {np.mean(stab['Ulcer']):+.3f} / TUW {np.mean(stab['TUW']):+.3f}")

    print("\n  SWAP: same 0.60 cap, different statistic (full sample):")
    for alt in ["ulcpass", "tuwpass", "ddpass2"]:
        ch = (G["full_ddpass"] != G[f"full_{alt}"])
        print(f"    MaxDD -> {alt:8s}  pass {int(G[f'full_{alt}'].sum()):3d}/{len(G)}  "
              f"verdict changes {int(ch.sum()):3d}/{len(G)} = {ch.mean():.1%}")
    H_SWAP = (G.full_ddpass != G.full_ulcpass).mean() >= 0.20
    print(f"  H_SWAP ({'HOLDS' if H_SWAP else 'FAILS'}): Ulcer swap changes "
          f"{(G.full_ddpass != G.full_ulcpass).mean():.1%} vs a 20% bar")

    # how often does the DD leg BIND at all in a full 4b verdict?
    print("\n  Which 4b leg BINDS (full sample, each book vs its panel's SPY):")
    for p in panels:
        sub = G[G.panel == p]; s = spy_stats[(p, "full")]
        s1, s2 = spy_stats[(p, "H1")], spy_stats[(p, "H2")]
        so = spy_stats[(p, "OOS")]
        legH1 = sub.H1_Sharpe > s1["Sharpe"]; legH2 = sub.H2_Sharpe > s2["Sharpe"]
        legOOS = sub.OOS_Sharpe > so["Sharpe"]
        legDD = sub.full_ddpass
        legC = sub.full_CAGR >= CAGR_FLOOR * s["CAGR"]
        allp = legH1 & legH2 & legOOS & legDD & legC
        print(f"    {p:9s} n={len(sub):3d}  fail H1 {int((~legH1).sum()):3d}  H2 {int((~legH2).sum()):3d}  "
              f"OOS {int((~legOOS).sum()):3d}  DD {int((~legDD).sum()):3d}  CAGR {int((~legC).sum()):3d}  "
              f"-> 4b PASS {int(allp.sum()):3d}")
        G.loc[sub.index, "fb_pass"] = allp
        G.loc[sub.index, "fb_pass_alt"] = legH1 & legH2 & legOOS & sub.full_ulcpass & legC
    ch4b = (G.fb_pass != G.fb_pass_alt)
    print(f"    full 4b verdict with the Ulcer cap instead: changes {int(ch4b.sum())}/{len(G)} = {ch4b.mean():.1%}")

    # ------------------------------------------------------------ PART 2 record census
    print("\n" + "=" * 100)
    print("PART 2  CENSUS - the record's own published 4b DD margins")
    print("=" * 100)
    cen = census_record(med_c)
    cen.to_csv(str(OUT) + ".census.csv.gz", index=False, compression="gzip")   # 112k rows, gzipped
    if len(cen):
        cen.groupby("file").agg(
            n=("margin_pp", "size"),
            med_abs_margin_pp=("margin_pp", lambda s: s.abs().median()),
            share_lt_c=("margin_pp", lambda s: (s.abs() < med_c).mean()),
            share_lt_1pp=("margin_pp", lambda s: (s.abs() < 1.0).mean()),
            share_pass=("margin_pp", lambda s: (s >= 0).mean()),
            median_spy_dd=("spy_dd", "median"),
        ).reset_index().to_csv(str(OUT) + ".census_byfile.csv", index=False)

    # ------------------------------------------------------------ PART 4 walk-forward
    print("\n" + "=" * 100)
    print("PART 4  rule-8 walk-forward (2 tuned params: band b, gross g) + both KEEP paths")
    print("=" * 100)
    wf = []
    for p in panels:
        sub = G[(G.panel == p) & (G.family == "BAND") & (G.freq == "W")].copy()
        sIS = spy_stats[(p, "IS")]; sOOS = spy_stats[(p, "OOS")]
        for lbl, gate in [("MaxDD cap", sub.IS_MaxDD.abs() <= DD_CAP * abs(sIS["MaxDD"])),
                          ("Ulcer cap", sub.IS_Ulcer <= DD_CAP * sIS["Ulcer"]),
                          ("no DD gate", pd.Series(True, index=sub.index))]:
            elig = sub[gate]
            if not len(elig):
                print(f"  {p:9s} {lbl:11s}  no eligible book IS"); continue
            pick = elig.loc[elig.IS_Sharpe.idxmax()]
            wf.append(dict(panel=p, gate=lbl, band=pick.dial, gross=pick.gross,
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           OOS_Ulcer=pick.OOS_Ulcer,
                           spy_OOS_CAGR=sOOS["CAGR"], spy_OOS_Sharpe=sOOS["Sharpe"],
                           spy_OOS_MaxDD=sOOS["MaxDD"]))
            print(f"  {p:9s} {lbl:11s} -> band {pick.dial:.2f} gross {pick.gross:.2f}  "
                  f"OOS CAGR {pick.OOS_CAGR:7.2%} Sharpe {pick.OOS_Sharpe:6.3f} MaxDD {pick.OOS_MaxDD:7.2%}  "
                  f"| SPY OOS {sOOS['CAGR']:.2%}/{sOOS['Sharpe']:.3f}/{sOOS['MaxDD']:.2%}")
    W = pd.DataFrame(wf)
    W.to_csv(str(OUT) + ".walkforward.csv", index=False)

    # RULES v2 live baseline on each panel, same windows
    print("\n  RULES v2 (live baseline) on the same windows:")
    base = {}
    for p, px in panels.items():
        r = fast_backtest(px, rules_v2_weights(px).reindex(columns=px.columns).fillna(0.0), freq="W")
        base[p] = {k: perf(window(r, k, p)) for k in KINDS}
        b = base[p]
        print(f"    {p:9s} full {b['full']['CAGR']:6.2%}/{b['full']['Sharpe']:.3f}/{b['full']['MaxDD']:7.2%}  "
              f"H1 {b['H1']['Sharpe']:.3f} H2 {b['H2']['Sharpe']:.3f}  "
              f"OOS {b['OOS']['CAGR']:6.2%}/{b['OOS']['Sharpe']:.3f}/{b['OOS']['MaxDD']:7.2%}")
        s = spy_stats[(p, "full")]
        print(f"    {'SPY':9s} full {s['CAGR']:6.2%}/{s['Sharpe']:.3f}/{s['MaxDD']:7.2%}  "
              f"H1 {spy_stats[(p,'H1')]['Sharpe']:.3f} H2 {spy_stats[(p,'H2')]['Sharpe']:.3f}  "
              f"OOS {spy_stats[(p,'OOS')]['CAGR']:6.2%}/{spy_stats[(p,'OOS')]['Sharpe']:.3f}/"
              f"{spy_stats[(p,'OOS')]['MaxDD']:7.2%}")

    print("\n  BOTH KEEP PATHS on all 126 books:")
    n4a = 0
    for p in panels:
        sub = G[G.panel == p]; b = base[p]
        a = (sub.H1_Sharpe > b["H1"]["Sharpe"]) & (sub.H2_Sharpe > b["H2"]["Sharpe"]) & \
            (sub.full_MaxDD >= b["full"]["MaxDD"])
        G.loc[sub.index, "fa_pass"] = a
        n4a += int(a.sum())
        print(f"    {p:9s} 4a {int(a.sum()):3d}/{len(sub)}   4b {int(G.loc[sub.index,'fb_pass'].sum()):3d}/{len(sub)}   "
              f"BOTH {int((a & G.loc[sub.index,'fb_pass']).sum()):3d}/{len(sub)}")
    print(f"    TOTAL     4a {n4a}/{len(G)}   4b {int(G.fb_pass.sum())}/{len(G)}   "
          f"BOTH {int((G.fa_pass & G.fb_pass).sum())}/{len(G)}")

    # the walk-forward picks judged on both paths, OOS read once
    print("\n  The rule-8 picks judged on both KEEP paths (OOS read once):")
    for _, w in W.iterrows():
        p = w.panel; b = base[p]; sOOS = spy_stats[(p, "OOS")]
        row = G[(G.panel == p) & (G.family == "BAND") & (G.freq == "W") &
                (G.dial == w.band) & (G.gross == w.gross)].iloc[0]
        a4 = row.H1_Sharpe > b["H1"]["Sharpe"] and row.H2_Sharpe > b["H2"]["Sharpe"] and \
             row.full_MaxDD >= b["full"]["MaxDD"]
        print(f"    {p:9s} {w.gate:11s} band {w.band:.2f}/g {w.gross:.2f}  4a {a4}  4b {bool(row.fb_pass)}  "
              f"(OOS Sharpe {row.OOS_Sharpe:.3f} vs v2 {b['OOS']['Sharpe']:.3f} vs SPY {sOOS['Sharpe']:.3f}; "
              f"DD margin {row.full_margin_pp:+.2f} pp, own contribution {row.full_contrib_pp:.2f} pp)")

    G.to_csv(str(OUT) + ".grid.csv", index=False)

    # ------------------------------------------------------------ PART 5 idea 311 ladder
    print("\n" + "=" * 100)
    print("PART 5  idea 311's standing proposal - 17-point gross ladder on every 4b passer the")
    print("        rule-8 chooser lands on, plus the DD margin along the ladder")
    print("=" * 100)
    lad = []
    for p, b_ in [("U56", 0.10), ("B136", 0.10), ("SMALL484", 0.10)]:
        px = panels[p]
        sf, s1, s2, so = (spy_stats[(p, k)] for k in ("full", "H1", "H2", "OOS"))
        bl = base[p]
        print(f"  {p} band {b_:.2f} weekly, gross 0.20 -> 1.00 in 17 steps:")
        for g in np.round(np.linspace(0.20, 1.00, 17), 3):
            w = band_book(px.drop(columns=["SPY"], errors="ignore"), b_, float(g))
            r = fast_backtest(px, w.reindex(columns=px.columns).fillna(0.0), freq="W")
            m = {k: perf(window(r, k, p)) for k in KINDS}
            legs = dict(H1=m["H1"]["Sharpe"] > s1["Sharpe"], H2=m["H2"]["Sharpe"] > s2["Sharpe"],
                        OOS=m["OOS"]["Sharpe"] > so["Sharpe"],
                        DD=abs(m["full"]["MaxDD"]) <= DD_CAP * abs(sf["MaxDD"]),
                        CAGR=m["full"]["CAGR"] >= CAGR_FLOOR * sf["CAGR"])
            ok = all(legs.values())
            a4 = (m["H1"]["Sharpe"] > bl["H1"]["Sharpe"] and m["H2"]["Sharpe"] > bl["H2"]["Sharpe"]
                  and m["full"]["MaxDD"] >= bl["full"]["MaxDD"])
            marg = (DD_CAP * abs(sf["MaxDD"]) - abs(m["full"]["MaxDD"])) * 100
            lad.append(dict(panel=p, band=b_, gross=float(g), full_CAGR=m["full"]["CAGR"],
                            full_Sharpe=m["full"]["Sharpe"], full_MaxDD=m["full"]["MaxDD"],
                            H1=m["H1"]["Sharpe"], H2=m["H2"]["Sharpe"], OOS_Sharpe=m["OOS"]["Sharpe"],
                            OOS_CAGR=m["OOS"]["CAGR"], OOS_MaxDD=m["OOS"]["MaxDD"],
                            margin_pp=marg, contrib_pp=m["full"]["contrib_pp"],
                            fb=ok, fa=a4, **{f"leg_{k}": v for k, v in legs.items()}))
            print(f"    g={g:.3f}  CAGR {m['full']['CAGR']:6.2%} Sh {m['full']['Sharpe']:.3f} "
                  f"DD {m['full']['MaxDD']:7.2%}  OOS {m['OOS']['CAGR']:6.2%}/{m['OOS']['Sharpe']:.3f}  "
                  f"DDmargin {marg:+6.2f} pp (own c {m['full']['contrib_pp']:5.2f})  "
                  f"4b {'PASS' if ok else 'fail:' + ','.join(k for k, v in legs.items() if not v):<14s} "
                  f"4a {a4}")
        sub = [x for x in lad if x["panel"] == p]
        band_pts = [x["gross"] for x in sub if x["fb"]]
        print(f"    -> 4b admissible band: {len(band_pts)}/17 points"
              + (f" [{min(band_pts):.3f}, {max(band_pts):.3f}]"
                 f" contiguous={len(band_pts) == 1 + round((max(band_pts)-min(band_pts))/0.05)}"
                 if band_pts else " (none)"))
    pd.DataFrame(lad).to_csv(str(OUT) + ".ladder.csv", index=False)

    # ------------------------------------------------------------ verdict
    print("\n" + "=" * 100)
    print("PRE-REGISTERED HYPOTHESES")
    print("=" * 100)
    print(f"  G1 {'PASS' if G1 else 'FAIL'}   G2 {'PASS' if G2 else 'FAIL'}   G3 {'PASS' if g3 else 'FAIL'}")
    print(f"  H_FLIP  {'HOLDS' if H_FLIP else 'FAILS'}   ({flip_full:.1%} vs 25%)")
    print(f"  H_SAME  {'HOLDS' if H_SAME else 'FAILS'}   ({min(shares):.0%} vs 80%)")
    print(f"  H_STAB  {'HOLDS' if H_STAB else 'FAILS'}")
    print(f"  H_SWAP  {'HOLDS' if H_SWAP else 'FAILS'}")
    json.dump(dict(G1=bool(G1), G2=bool(G2), G3=bool(g3), H_FLIP=bool(H_FLIP),
                   H_SAME=bool(H_SAME), H_STAB=bool(H_STAB), H_SWAP=bool(H_SWAP),
                   flip_full=float(flip_full), med_c=med_c,
                   stab={k: [float(x) for x in v] for k, v in stab.items()}),
              open(str(OUT) + ".gates.json", "w"), indent=1)


# ---------------------------------------------------------------- record census
def census_record(med_c):
    """Every committed CSV that publishes a book MaxDD and a SPY MaxDD in the same row."""
    files = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv")))
    recs = []
    used_files = 0
    for f in files:
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        cols = list(df.columns)
        low = {c: c.lower() for c in cols}
        spycols = [c for c in cols if "maxdd" in low[c] and "spy" in low[c]]
        if not spycols:
            continue
        bookcols = [c for c in cols if "maxdd" in low[c] and "spy" not in low[c]
                    and not any(t in low[c] for t in ("v1_", "v2_", "ctl", "base", "d_", "dmaxdd", "delta"))]
        if not bookcols:
            continue
        hit = False
        for bc in bookcols:
            oos = "oos" in low[bc]
            cand = [c for c in spycols if ("oos" in low[c]) == oos] or spycols
            sc = cand[0]
            a = pd.to_numeric(df[bc], errors="coerce")
            b = pd.to_numeric(df[sc], errors="coerce")
            m = a.notna() & b.notna() & (b != 0)
            if not m.any():
                continue
            a, b = a[m].abs(), b[m].abs()
            a = a.where(a <= 1.5, a / 100.0)          # some files publish pp, some fractions
            b = b.where(b <= 1.5, b / 100.0)
            marg = (0.60 * b - a) * 100
            for v, bb in zip(marg.values, b.values):
                recs.append(dict(file=Path(f).name, book_col=bc, spy_col=sc,
                                 margin_pp=float(v), spy_dd=float(bb)))
            hit = True
        used_files += hit
    C = pd.DataFrame(recs)
    if not len(C):
        print("  no paired rows found")
        return C
    print(f"  {len(C):,} paired (book MaxDD, SPY MaxDD) rows in {used_files} committed CSVs "
          f"({C.file.nunique()} distinct files)")
    passing = C.margin_pp >= 0
    print(f"  published 4b DD-cap verdicts: PASS {int(passing.sum()):,} ({passing.mean():.1%})  "
          f"FAIL {int((~passing).sum()):,}")
    print(f"  |margin| distribution (pp): median {C.margin_pp.abs().median():.2f}  "
          f"p25 {C.margin_pp.abs().quantile(.25):.2f}  p75 {C.margin_pp.abs().quantile(.75):.2f}  "
          f"max {C.margin_pp.abs().max():.1f}")
    for lbl, thr in [("rebuilt MEDIAN contribution", med_c),
                     ("1.00 pp", 1.0), ("2.00 pp", 2.0), ("5.00 pp", 5.0)]:
        sh = (C.margin_pp.abs() < thr).mean()
        shf = C[C.margin_pp.abs() < thr].file.nunique()
        print(f"    |margin| < {thr:5.2f} pp ({lbl:28s}): {sh:6.1%} of rows, touching {shf} files")
    # file-clustered: one median margin per file, so one huge file cannot carry the number
    per_file = C.groupby("file").margin_pp.apply(lambda s: s.abs().median())
    print(f"  FILE-CLUSTERED (one median |margin| per file, n={len(per_file)}): "
          f"share below the rebuilt median contribution {(per_file < med_c).mean():.1%}, "
          f"below 1 pp {(per_file < 1.0).mean():.1%}, median {per_file.median():.2f} pp")
    H_REC = (per_file < med_c).mean() >= 0.50
    print(f"  H_REC ({'HOLDS' if H_REC else 'FAILS'}): file-clustered share below c "
          f"{(per_file < med_c).mean():.1%} vs a 50% bar")
    return C


if __name__ == "__main__":
    main()
