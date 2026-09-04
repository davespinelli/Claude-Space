#!/usr/bin/env python3
"""Idea 10 - "sector-only-universe": run the book on ETFs only (drop the single stocks).

The question
------------
research/universe.json is 56 names: 36 ETFs (8 broad + 16 sector/industry + 12
bond/FX/commodity) and 20 mega-cap single stocks.  The queued hypothesis is that dropping
the single stocks removes idiosyncratic risk without removing the momentum edge, so the
book should keep most of its return with a smaller drawdown.

Two reasons this is worth a run beyond the hypothesis itself:

  (a) It is the cheapest available answer to idea 53 (universe fragility).  Every 4b
      candidate the project has produced passes only on the exact 56-name list it was
      fitted on; ideas 2, 46 and 55 all die or wobble when the universe changes.  The ETF
      subset is the SAME 36 tickers in universe.json and in universe_broad.json, so an
      ETF-only book is composition-invariant across the project's two large-cap lists by
      construction, not by luck.  If it clears 4b there, the cross-universe test that has
      killed everything else is passed trivially - the interesting question becomes
      whether it clears the bars at all.

  (b) Survivorship bias falls almost entirely on the single-stock leg.  The 20 mega-caps
      are in the file because they won; SPY/XLK/TLT are index products that would be in
      any 2009-vintage list.  An ETF-only result is the least survivorship-flattered
      number this project can produce on large caps, so it is worth knowing even if it is
      worse.

Panels (parameter 1 of 2) - all reported, none picked on its own result
    U56     universe.json, all 56 names ex-crypto ............... incumbent control
    ETF36   universe.json ETFs only (broad + sectors + bonds/fx/commod)
    ETF24   broad + sector ETFs only ......................... the idea as literally queued
    STK20   universe.json mega-cap single stocks only ......... the COMPLEMENT control
    B136    universe_broad.json, all names ................... second incumbent control
    BSTK100 universe_broad.json single stocks only ........... broad complement
SPY is a constituent of every panel that contains it by definition (it is in
universe.json's "broad" group); in the two stock-only panels it is joined as a
benchmark column only and is NOT tradable.

Book constructions - structural variants, not tuned choices, all reported
    v1     RULES v1 exactly as live: top 5 eligible by the composite WITH /sqrt(vol20),
           15% each.  One row per panel.
    CAND   idea 2's standing 4b KEEP-candidate: top-n eligible equal-weight at 75% gross,
           composite WITHOUT /sqrt(vol20).  n is parameter 2.
    EWall  equal-weight ALL eligible names at 75% gross, no ranking.  The project's
           standard "is the ranking doing anything" control.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (the idea itself)     2. n in {5, 10, 20} for the CAND construction
The 200d / vol20 < 0.60 eligibility filter, 75% gross, weekly rebalancing, 10 bps costs
and next-day execution are RULES v1's own and are held fixed everywhere.

Grid = 6 panels x (1 v1 + 3 CAND n + 1 EWall) = 30 points, ALL reported.

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number was read
    S1 (Sharpe):   over the CAND points, the (panel, n) with the highest 2009-2016 Sharpe;
                   ties -> fewer names, then smaller n.
    S2 (4b-aware): the same, restricted to points whose in-sample MaxDD is within 60% of
                   SPY's in-sample MaxDD.  "none" if nothing qualifies.
    Also reported: the best-n-within-each-panel selection, so the universe choice and the
    position-count choice can be audited separately.
Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Harness sanity: the script reproduces idea 2's published KEEP row (U56 / CAND / n=20 ->
12.7% / 1.093 / -18.3%) and the RULES v1 row before any new number is reported.

Survivorship: current constituents of both lists, one-directional.  The ETF-vs-stock
comparison is the point of the run and is EXPOSED to it in the direction that makes an
ETF win conservative and an ETF loss ambiguous; stated again in the result memo.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS = [5, 10, 20]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 200)


# ---------------------------------------------------------------- panels
def build_panels():
    """(name -> (px, tradable_columns)) for the six panels."""
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    broad_g = [t for t in U["broad"] if t not in crypto]
    sect_g = [t for t in U["sectors"] if t not in crypto]
    bfc_g = [t for t in U["bonds_fx_commod"] if t not in crypto]
    stk_g = [t for t in U["megacap"] if t not in crypto]

    px56 = load_universe()                      # 56 names ex-crypto
    px136 = load_universe(broad=True)

    etf36 = broad_g + sect_g + bfc_g
    etf24 = broad_g + sect_g
    # broad-list ETFs = the same instruments where present; its stock leg is the complement
    b_etf = [t for t in px136.columns if t in set(etf36)]
    b_stk = [t for t in px136.columns if t not in set(etf36)]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    panels = {
        "U56":     sub(px56, list(px56.columns)),
        "ETF36":   sub(px56, etf36),
        "ETF24":   sub(px56, etf24),
        "STK20":   sub(px56, stk_g, tradable=stk_g),        # SPY joined as benchmark only
        "B136":    sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),       # SPY joined as benchmark only
    }
    return panels, dict(etf36=etf36, etf24=etf24, stk20=stk_g, b_etf=b_etf, b_stk=b_stk)


# ---------------------------------------------------------------- book construction
def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = above & (vol20 < MAX_VOL)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m = m.copy()
        m[drop] = False
    return m


def weights(px, tradable, kind, n=None):
    """kind in {'v1', 'CAND', 'EWall'}; scoring is done on the panel's own columns."""
    if kind == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(eligible_mask(px, tradable)).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    elig = eligible_mask(px, tradable)
    if kind == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def paired_t(a, b):
    """Paired daily t-stat and annualised mean difference of two aligned return series."""
    d = (a - b).dropna()
    if d.std() == 0 or len(d) < 3:
        return 0.0, 0.0
    return d.mean() / (d.std() / np.sqrt(len(d))), d.mean() * 252


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main
def main():
    panels, groups = build_panels()

    print("=" * 170)
    print(f"Idea 10 sector-only-universe (lane C) | {SCRIPT} | {COST_BPS} bps, weekly, next-day execution")
    print("=" * 170)

    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr; the calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    print("\nPanels:")
    for k, (p, tr) in panels.items():
        print(f"  {k:<8} {len(tr):>3} tradable ({p.shape[1]} cols incl. benchmark) "
              f"{p.index[0].date()} -> {p.index[-1].date()}")
    print(f"\nETF subset identical in both lists? universe.json ETFs = {len(groups['etf36'])}, "
          f"present in universe_broad.json = {len(groups['b_etf'])}, "
          f"symmetric difference = {sorted(set(groups['etf36']) ^ set(groups['b_etf']))}")

    # common evaluation window: warm-up skip on the primary panel, applied to all
    start = px56.index[260]
    spy = px56["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms = metrics(spy)
    print(f"\nEval sample: {start.date()} -> {px56.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"SPY: CAGR {ms['CAGR']:.1%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}  "
          f"halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  "
          f"| 4b bars: Sharpe > halves & OOS {metrics(spy_oos)['Sharpe']:.3f}, "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.1%}, CAGR >= {0.70*ms['CAGR']:.2%}")

    base_v1 = backtest(px56, rules_v1_weights(px56), cost_bps=COST_BPS,
                       freq=FREQ)["returns"].loc[start:]
    mb = metrics(base_v1)
    print(f"RULES v1 (U56, live rules): CAGR {mb['CAGR']:.1%}  Sharpe {mb['Sharpe']:.3f}  "
          f"MaxDD {mb['MaxDD']:.1%}  halves {half_sharpes(base_v1)[0]:.3f}/{half_sharpes(base_v1)[1]:.3f}")

    # ---- harness sanity: reproduce idea 2's published KEEP row
    chk = backtest(px56, weights(px56, panels["U56"][1], "CAND", 20),
                   cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    mc = metrics(chk)
    print(f"\nHARNESS CHECK vs idea 2's published KEEP row (12.7% / 1.093 / -18.3%, halves 1.088/1.103):")
    print(f"  reproduced: {mc['CAGR']:.1%} / {mc['Sharpe']:.3f} / {mc['MaxDD']:.1%}, "
          f"halves {half_sharpes(chk)[0]:.3f}/{half_sharpes(chk)[1]:.3f}")

    # ---- the grid
    rows, series = [], {}
    for pname, (px, tradable) in panels.items():
        elig = eligible_mask(px, tradable).loc[start:]
        ec = elig.sum(axis=1)
        arms = [("v1", None), ("EWall", None)] + [("CAND", n) for n in NS]
        for kind, n in arms:
            w = weights(px, tradable, kind, n)
            res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
            r = res["returns"].reindex(px56.index).fillna(0.0).loc[start:]
            to = res["turnover"].reindex(px56.index).fillna(0.0).loc[start:]
            held = res["weights"].reindex(px56.index).fillna(0.0).loc[start:]
            m = metrics(r)
            h1, h2 = half_sharpes(r)
            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
            m_is, m_oos = metrics(r_is), metrics(r_oos)
            key = f"{pname}/{kind}" + (f"-n{n}" if n else "")
            series[key] = r
            rows.append(dict(
                point=key, panel=pname, kind=kind, n=(n if n else np.nan),
                names=len(tradable),
                CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=h1, H2=h2,
                IS_Sharpe=m_is["Sharpe"], IS_MaxDD=m_is["MaxDD"],
                OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                turn=to.sum() / m["Years"], gross=held.sum(axis=1).mean(),
                elig=ec.mean(),
                p4a=verdict_4a(r, base_v1),
                f4b=fail_4b(r, spy, r_oos, spy_oos),
            ))
    df = pd.DataFrame(rows).set_index("point")
    df["p4b"] = df["f4b"] == "-"

    print("\n" + "=" * 170)
    print("FULL GRID - 30 points, all reported (f4b lists which of 4b's five tests fail)")
    print("=" * 170)
    cols = ["panel", "kind", "n", "names", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turn", "gross", "elig", "p4a", "p4b", "f4b"]
    print(fmt(df[cols]))
    print(f"\n4b passes: {int(df['p4b'].sum())} of {len(df)}   |   "
          f"4a passes: {int(df['p4a'].sum())} of {len(df)}")

    # ---- the hypothesis, stated as a measurement: does dropping stocks cut risk?
    print("\n" + "=" * 170)
    print("HYPOTHESIS TEST - 'less idiosyncratic risk': ETF panels vs their full-list control,")
    print("matched construction, same days, same gross. dRet = annualised paired mean, t = paired daily t.")
    print("=" * 170)
    hyp = []
    for ctrl, tests in (("U56", ["ETF36", "ETF24", "STK20"]),
                        ("B136", ["ETF36", "ETF24", "BSTK100"])):
        for kind, n in [("v1", None), ("EWall", None)] + [("CAND", x) for x in NS]:
            suff = f"{kind}" + (f"-n{n}" if n else "")
            b = series[f"{ctrl}/{suff}"]
            for t in tests:
                a = series[f"{t}/{suff}"]
                tt, dr = paired_t(a, b)
                ma, mbk = metrics(a), metrics(b)
                hyp.append(dict(control=ctrl, test=t, book=suff,
                                dCAGR=ma["CAGR"] - mbk["CAGR"], dVol=ma["Vol"] - mbk["Vol"],
                                dMaxDD=ma["MaxDD"] - mbk["MaxDD"],
                                dSharpe=ma["Sharpe"] - mbk["Sharpe"],
                                dRet_ann=dr, t=tt,
                                corr=a.corr(b)))
    hdf = pd.DataFrame(hyp)
    print(fmt(hdf.set_index(["control", "test", "book"])))
    for t in ["ETF36", "ETF24", "STK20", "BSTK100"]:
        s = hdf[hdf.test == t]
        print(f"  {t:<8} vs its control: dVol < 0 in {(s.dVol < 0).sum()}/{len(s)}, "
              f"dMaxDD > 0 (shallower) in {(s.dMaxDD > 0).sum()}/{len(s)}, "
              f"dSharpe > 0 in {(s.dSharpe > 0).sum()}/{len(s)}, "
              f"mean dRet {s.dRet_ann.mean():+.2%}/yr, t range [{s.t.min():+.2f}, {s.t.max():+.2f}]")

    # ---- calendar-year detail for the panels that matter
    print("\n" + "=" * 170)
    print("CALENDAR YEARS (CAND n=20 book per panel, plus SPY and live v1)")
    print("=" * 170)
    yr = pd.DataFrame({k: series[f"{k}/CAND-n20"] for k in panels})
    yr["SPY"] = spy
    yr["v1_live"] = base_v1
    print(fmt(yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1) * 100))

    # ---- walk-forward, rule 8
    print("\n" + "=" * 170)
    print("WALK-FORWARD (rule 8): parameters chosen on 2009-2016, evaluated on 2017-2026")
    print("=" * 170)
    cand = df[df.kind == "CAND"].copy()
    cand["key"] = list(zip(cand.names, cand.n))
    cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"In-sample SPY: Sharpe {metrics(spy_is)['Sharpe']:.3f}, MaxDD {metrics(spy_is)['MaxDD']:.1%} "
          f"-> S2 admits IS MaxDD shallower than {-cap:.1%}")
    print("\nIn-sample table (the only numbers either rule may look at):")
    print(fmt(cand[["panel", "n", "IS_Sharpe", "IS_MaxDD"]]))

    def pick(sub, label):
        if sub.empty:
            print(f"  {label}: none qualify"); return None
        s = sub.sort_values(["IS_Sharpe", "names", "n"], ascending=[False, True, True])
        p = s.index[0]
        row = df.loc[p]
        print(f"  {label}: {p}  ->  OOS CAGR {row.OOS_CAGR:.1%}  Sharpe {row.OOS_Sharpe:.3f}  "
              f"MaxDD {row.OOS_MaxDD:.1%}")
        return p

    oos_bars = (f"OOS bars: Sharpe > SPY {metrics(spy_oos)['Sharpe']:.3f}, "
                f"MaxDD <= {0.60*abs(metrics(spy_oos)['MaxDD']):.1%}, "
                f"CAGR >= {0.70*metrics(spy_oos)['CAGR']:.2%}  "
                f"(SPY OOS {metrics(spy_oos)['CAGR']:.1%}/{metrics(spy_oos)['Sharpe']:.3f}/"
                f"{metrics(spy_oos)['MaxDD']:.1%}; v1 OOS "
                f"{metrics(base_v1.loc[OOS_START:])['CAGR']:.1%}/"
                f"{metrics(base_v1.loc[OOS_START:])['Sharpe']:.3f}/"
                f"{metrics(base_v1.loc[OOS_START:])['MaxDD']:.1%})")
    print("\n" + oos_bars)
    print("\nGlobal selection (panel AND n chosen in-sample):")
    s1 = pick(cand, "S1 plain-Sharpe ")
    s2 = pick(cand[cand.IS_MaxDD >= -cap], "S2 4b-aware    ")
    for p in [s1, s2]:
        if p:
            row = df.loc[p]
            ok = (row.OOS_Sharpe > metrics(spy_oos)["Sharpe"]
                  and abs(row.OOS_MaxDD) <= 0.60 * abs(metrics(spy_oos)["MaxDD"])
                  and row.OOS_CAGR >= 0.70 * metrics(spy_oos)["CAGR"])
            print(f"    {p}: clears all three OOS 4b bars? {ok}")

    print("\nPer-panel selection (n chosen in-sample within each panel):")
    for pn in panels:
        sub = cand[cand.panel == pn]
        pick(sub, f"  {pn:<8} S1")
        pick(sub[sub.IS_MaxDD >= -cap], f"  {pn:<8} S2")

    # ---- Spearman: does in-sample rank predict out-of-sample rank at all?
    rho = cand["IS_Sharpe"].rank().corr(cand["OOS_Sharpe"].rank(), method="pearson")
    rho_dd = cand["IS_MaxDD"].rank().corr(cand["OOS_MaxDD"].rank(), method="pearson")
    print(f"\nSpearman(IS Sharpe, OOS Sharpe) over the {len(cand)} CAND points = {rho:+.3f}; "
          f"Spearman(IS MaxDD, OOS MaxDD) = {rho_dd:+.3f}")

    # ---- leaderboard rows
    print("\n" + "=" * 170)
    print("LEADERBOARD rows")
    print("=" * 170)
    for p in ["ETF24/CAND-n10", "ETF36/CAND-n10", "ETF24/CAND-n20", "ETF36/CAND-n20",
              "STK20/CAND-n10", "U56/CAND-n20"]:
        r = df.loc[p]
        v = "KEEP-candidate(4b)" if r.p4b else ("KEEP-candidate(4a)" if r.p4a else "KILL")
        print(f"| 2026-09-04 | idea10 {p} | {r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | "
              f"{r.H1:.2f} / {r.H2:.2f} | {mb['Sharpe']:.2f} ({half_sharpes(base_v1)[0]:.2f}/"
              f"{half_sharpes(base_v1)[1]:.2f}) | {v} | {SCRIPT} |")

    df.to_csv(REPO / "research" / "backtests" / f"{SCRIPT[:-3]}.grid.csv")
    print(f"\nGrid written to research/backtests/{SCRIPT[:-3]}.grid.csv")


if __name__ == "__main__":
    main()
