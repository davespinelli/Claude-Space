#!/usr/bin/env python3
"""IDEA 518 (cloud) — is the VINTAGE-INERT DD LEG a 2020/2022 artefact?

QUESTION (queue).  Idea 514 measured max |dMaxDD| 0.0000 across nine vintage depths on every panel
and every book, because each book's worst drawdown sits in 2020 or 2022, which makes the DD leg of
BOTH KEEP paths insensitive to the data end.  Test whether the DD leg is therefore decided by TWO
EPISODES rather than by the book: re-run both KEEP paths on samples that EXCLUDE 2020 and 2022 in
turn and report how many published 4a/4b verdicts survive.

WHY IT MATTERS FOR CAPITAL.  PROTOCOL 4a needs "MaxDD no worse than the live rules" and 4b needs
"MaxDD <= 60% of SPY's".  Both are single-number legs read off ONE trough.  If that trough is
always in the same two calendar years, then a KEEP is not a statement about the book, it is a
statement about how the book behaved in Feb-Mar 2020 and Jan-Oct 2022 — two episodes, one of them
a liquidity crash and the other a rates repricing, neither of which is guaranteed to be the shape
of the next one.  That is a live-capital question, not a bookkeeping one.

DESIGN.  The exclusion is done on RETURNS, not on prices: the excluded calendar year's daily
returns are dropped and the equity curve spliced across the gap, so signals, eligibility, holdings
and costs are all computed on the FULL price history exactly as the live book would see them, and
only the SCORING window changes.  Excluding at the price level instead would change the 200d MA
and the 20d vol on both sides of the gap, i.e. would test a different book, not a different
sample.  Every comparand (RULES v2 and SPY) is scored on the identical spliced window.

PARAMETERS — exactly two, every grid point reported, neither tuned on an outcome:
  P1  episode, 4 levels {NONE, drop 2020, drop 2022, drop BOTH}.  Calendar years, as the queue
      words it.  A tighter trough-window variant is NOT swept (it would be a third parameter);
      the trough DATE of every book is published instead so the reader can see what the calendar
      year is standing in for.
  P2  panel, 3 levels {U56, B136, SMALL439} — the record's three named panels.

BOOKS (fixed, not a parameter; the record's standing corpus):
  RULES v2 (the live book), EWall (gated equal weight at gross 0.75), CAND-5, CAND-10,
  CAND-20 (= the 2026-09-04 KEEP 4b construction, top-20 equal weight, NO vol scaler),
  CAND-20-INV (the same book with the live vol scaler restored).
  6 books x 3 panels x 4 episode settings = 72 scored cells, all reported.

LEGS.
  [A] WHERE THE TROUGH IS.  For every (panel, book), the MaxDD trough date and the share of the
      drawdown that the two episodes account for.  This is the queue's premise, tested rather
      than assumed.
  [B] THE RESTATEMENT.  Both KEEP paths on all 72 cells; how many 4a/4b verdicts survive each
      exclusion, and which legs (H1/H2 Sharpe, OOS Sharpe, DD cap, CAGR floor) bind in each.
  [C] RULE 8.  Book chosen on IS 2010-2016 alone (per panel, best IS Sharpe), OOS 2017-2026 read
      ONCE — note the IS window contains NEITHER episode, so the chooser has never seen a crash.
      OOS CAGR / Sharpe / MaxDD against RULES v2 and SPY, with and without the episodes.

REPRODUCTION GATE (recorded, NEVER raising).  The live RULES v2 book on U56 at 10 bps weekly is
published at 8.66% / 1.2056 / -12.05% (idea 415 G2, 2026-09-10 leaderboard).

SURVIVORSHIP (rule 9): all three panels are current constituents; SMALL439 additionally drops the
44 names with max_1d_move >= 1.0.  Exclusion contrasts are within-book and within-panel, so the
bias sits in the LEVELS, not in the survival counts this run reports.

Deterministic, no random draws.  Writes <STEM>.{troughs,cells,legs,walkforward}.csv and
<STEM>.console.txt.  Does not modify RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-11_is-the-VINTAGE-INERT-DD-LEG-a-2020-2022-artefact_cloud"
EPISODES = {"NONE": (), "drop2020": (2020,), "drop2022": (2022,), "dropBOTH": (2020, 2022)}
GROSS = 0.75
COST_BPS, FREQ = 10, "W"
START = "2010-01-01"
OOS_START = "2017-01-01"
MAXVOL = 0.60

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ books
def cand_weights(n, vol_scale, gross=GROSS):
    def f(px):
        cols = [c for c in px.columns if c != "SPY"]
        sub = px[cols]
        s, above, vol20 = score(sub, vol_scale=vol_scale)
        elig = s.where(above & (vol20 < MAXVOL))
        rank = elig.rank(axis=1, ascending=False)
        w = (rank <= n).astype(float)
        held = w.sum(axis=1).replace(0, np.nan)
        w = gross * w.div(held, axis=0).fillna(0.0)
        return w.reindex(columns=px.columns).fillna(0.0)
    return f


def ewall_weights(px, gross=GROSS):
    cols = [c for c in px.columns if c != "SPY"]
    sub = px[cols]
    above = sub > sub.rolling(200).mean()
    vol20 = sub.pct_change().rolling(20).std() * np.sqrt(252)
    e = (above & (vol20 < MAXVOL)).astype(float)
    w = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def v2_on(px):
    return rules_v2_weights(px.drop(columns=["SPY"], errors="ignore")).reindex(
        columns=px.columns).fillna(0.0)


BOOKS = {
    "RULES v2": v2_on,
    "EWall": ewall_weights,
    "CAND-5": cand_weights(5, False),
    "CAND-10": cand_weights(10, False),
    "CAND-20": cand_weights(20, False),
    "CAND-20-INV": cand_weights(20, True),
}


# ------------------------------------------------------------------ scoring
def splice(r, years):
    """Drop the excluded calendar years' daily returns; the equity curve compounds across the gap."""
    if not years:
        return r
    return r[~r.index.year.isin(years)]


def dd_series(r):
    eq = (1 + r).cumprod()
    return eq / eq.cummax() - 1


def row_of(r):
    m = metrics(r)
    h = len(r) // 2
    m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o, i = r.loc[OOS_START:], r.loc[:OOS_START]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS_Sharpe=metrics(i)["Sharpe"], OOS_CAGR=metrics(o)["CAGR"],
                OOS_Sharpe=metrics(o)["Sharpe"], OOS_MaxDD=metrics(o)["MaxDD"])


def keep_legs(row, spy, v2):
    """PROTOCOL rule 4, leg by leg, so a flip can be attributed."""
    a_h1, a_h2 = row["H1"] > v2["H1"], row["H2"] > v2["H2"]
    a_dd = row["MaxDD"] >= v2["MaxDD"]
    b_h1, b_h2 = row["H1"] > spy["H1"], row["H2"] > spy["H2"]
    b_oos = row["OOS_Sharpe"] > spy["OOS_Sharpe"]
    b_dd = row["MaxDD"] >= 0.60 * spy["MaxDD"]
    b_cagr = row["CAGR"] >= 0.70 * spy["CAGR"]
    return dict(a_H1=a_h1, a_H2=a_h2, a_DD=a_dd, pass4a=bool(a_h1 and a_h2 and a_dd),
                b_H1=b_h1, b_H2=b_h2, b_OOS=b_oos, b_DD=b_dd, b_CAGR=b_cagr,
                pass4b=bool(b_h1 and b_h2 and b_oos and b_dd and b_cagr))


# ================================================================== main
def main():
    P("=" * 100)
    P("IDEA 518 (cloud) — is the VINTAGE-INERT DD LEG a 2020/2022 artefact?")
    P("=" * 100)

    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    pxs = load_universe(start=START, small=True, with_spy=True)
    pxs = pxs[[c for c in pxs.columns if c == "SPY" or c not in bad]]
    panels = {"U56": load_universe(start=START),
              "B136": load_universe(start=START, broad=True),
              "SMALL439": pxs}
    P(f"\npanels: " + "  ".join(f"{k} k={len([c for c in v.columns if c != 'SPY'])}"
                                for k, v in panels.items())
      + f"   ({len(bad)} small names dropped by max_1d_move >= 1.0)")
    P(f"window {START} .. {panels['U56'].index[-1].date()}   costs {COST_BPS} bps   cadence {FREQ}"
      f"   gross {GROSS}   books {len(BOOKS)}   episodes {list(EPISODES)}")
    P("\nEXCLUSION IS ON RETURNS, NOT PRICES: signals, eligibility, holdings and costs are computed")
    P("on the FULL price history; only the scoring window changes, and every comparand (RULES v2,")
    P("SPY) is scored on the identical spliced window.")

    # -------- run every book once per panel; the four episode settings re-score the SAME returns
    rets = {}
    for pname, px in panels.items():
        st = px.index[260]
        rets[(pname, "SPY")] = px["SPY"].pct_change().fillna(0).loc[st:]
        for bname, fn in BOOKS.items():
            rets[(pname, bname)] = backtest(px, fn(px), cost_bps=COST_BPS,
                                            freq=FREQ)["returns"].loc[st:]
        P(f"  ran {len(BOOKS)} books on {pname} ({len(rets[(pname, 'SPY')])} days from {st.date()})")

    # -------- gate
    g = metrics(rets[("U56", "RULES v2")])
    P("\n" + "-" * 100)
    P("REPRODUCTION GATE (recorded, non-raising)")
    P("-" * 100)
    P(f"  live RULES v2 on U56 @10bps weekly: {g['CAGR']:.2%} / {g['Sharpe']:.4f} / {g['MaxDD']:.2%}"
      f"   (idea 415 G2 published 8.66% / 1.2056 / -12.05%)")

    # ---------------- LEG A: where the trough is
    P("\n" + "=" * 100)
    P("LEG A — WHERE THE TROUGH IS (the queue's premise, tested not assumed)")
    P("=" * 100)
    trows = []
    for (pname, bname), r in rets.items():
        d = dd_series(r)
        t = d.idxmin()
        peak = (1 + r).cumprod().loc[:t].idxmax()
        # the second-deepest trough OUTSIDE 2020 and 2022, i.e. what the DD leg falls back on
        out = d[~d.index.year.isin((2020, 2022))]
        trows.append(dict(panel=pname, book=bname, MaxDD=d.min(), trough=t.date(),
                          trough_year=t.year, peak=peak.date(),
                          MaxDD_ex_2020_2022=splice(r, (2020, 2022)).pipe(dd_series).min(),
                          worst_day_outside=out.min() if len(out) else np.nan))
    tr = pd.DataFrame(trows)
    tr.to_csv(f"{OUT}/{STEM}.troughs.csv", index=False)
    P("\n" + tr[["panel", "book", "MaxDD", "trough", "peak", "MaxDD_ex_2020_2022"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    yc = tr.trough_year.value_counts().sort_index()
    P(f"\n  trough year counts over all {len(tr)} (panel, book) series: "
      + "  ".join(f"{y}:{c}" for y, c in yc.items()))
    in2 = int(tr.trough_year.isin((2020, 2022)).sum())
    P(f"  PREMISE: {in2} of {len(tr)} worst drawdowns sit in 2020 or 2022 "
      f"({in2 / len(tr):.1%}) — idea 514 assumed all of them.")
    P(f"  mean MaxDD {tr.MaxDD.mean():.4f} -> {tr.MaxDD_ex_2020_2022.mean():.4f} when BOTH years "
      f"are excluded (mean shallowing {tr.MaxDD_ex_2020_2022.mean() - tr.MaxDD.mean():+.4f}, "
      f"{(tr.MaxDD_ex_2020_2022 / tr.MaxDD).mean():.1%} of the original depth retained)")

    # ---------------- LEG B: the restatement
    P("\n" + "=" * 100)
    P("LEG B — BOTH KEEP PATHS ON EVERY EPISODE SETTING (72 cells, all reported)")
    P("=" * 100)
    crows = []
    for pname in panels:
        for ep, yrs in EPISODES.items():
            spy = row_of(splice(rets[(pname, "SPY")], yrs))
            v2 = row_of(splice(rets[(pname, "RULES v2")], yrs))
            for bname in BOOKS:
                row = row_of(splice(rets[(pname, bname)], yrs))
                legs = keep_legs(row, spy, v2)
                crows.append(dict(panel=pname, episode=ep, book=bname, **row, **legs,
                                  spy_Sharpe=spy["Sharpe"], spy_CAGR=spy["CAGR"],
                                  spy_MaxDD=spy["MaxDD"], spy_H1=spy["H1"], spy_H2=spy["H2"],
                                  spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                                  spy_OOS_MaxDD=spy["OOS_MaxDD"],
                                  v2_Sharpe=v2["Sharpe"], v2_MaxDD=v2["MaxDD"], v2_H1=v2["H1"],
                                  v2_H2=v2["H2"], v2_OOS_Sharpe=v2["OOS_Sharpe"],
                                  v2_OOS_CAGR=v2["OOS_CAGR"], v2_OOS_MaxDD=v2["OOS_MaxDD"]))
    ce = pd.DataFrame(crows)
    ce.to_csv(f"{OUT}/{STEM}.cells.csv", index=False)

    P("\n  MaxDD by (panel, book) x episode:")
    P(ce.pivot_table(index=["panel", "book"], columns="episode", values="MaxDD")
      [list(EPISODES)].to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  SPY's own MaxDD (the 4b cap's denominator) by panel x episode:")
    P(ce.groupby(["panel", "episode"]).spy_MaxDD.first().unstack()[list(EPISODES)]
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  the 4b DD cap itself (0.60 x SPY MaxDD):")
    P((0.60 * ce.groupby(["panel", "episode"]).spy_MaxDD.first().unstack()[list(EPISODES)])
      .to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n  KEEP verdicts by panel x episode (out of 6 books each):")
    tab = ce.groupby(["panel", "episode"])[["pass4a", "pass4b"]].sum().unstack()
    P(tab.to_string())
    P(f"\n  TOTALS over all {len(ce)} cells: 4a {int(ce.pass4a.sum())}   4b {int(ce.pass4b.sum())}")
    for ep in EPISODES:
        s = ce[ce.episode == ep]
        P(f"    {ep:9s}  4a {int(s.pass4a.sum())}/{len(s)}   4b {int(s.pass4b.sum())}/{len(s)}")

    P("\n  VERDICT SURVIVAL — every (panel, book) whose NONE verdict is a pass, tracked across "
      "the exclusions:")
    base = ce[ce.episode == "NONE"].set_index(["panel", "book"])
    surv = []
    for (pn, bn), b in base.iterrows():
        r = dict(panel=pn, book=bn, base4a=bool(b.pass4a), base4b=bool(b.pass4b))
        for ep in EPISODES:
            c = ce[(ce.panel == pn) & (ce.book == bn) & (ce.episode == ep)].iloc[0]
            r[f"4a_{ep}"] = bool(c.pass4a)
            r[f"4b_{ep}"] = bool(c.pass4b)
        surv.append(r)
    sv = pd.DataFrame(surv)
    P(sv.to_string(index=False))
    p4b = sv[sv.base4b]
    p4a = sv[sv.base4a]
    P(f"\n  published-equivalent passes at episode NONE: 4a {len(p4a)}, 4b {len(p4b)}")
    for ep in EPISODES:
        if ep == "NONE":
            continue
        P(f"    {ep:9s}  4a survives {int(p4a[f'4a_{ep}'].sum()) if len(p4a) else 0}/{len(p4a)}   "
          f"4b survives {int(p4b[f'4b_{ep}'].sum()) if len(p4b) else 0}/{len(p4b)}"
          f"   NEW passes 4a {int(sv[~sv.base4a][f'4a_{ep}'].sum())} "
          f"4b {int(sv[~sv.base4b][f'4b_{ep}'].sum())}")

    P("\n  WHICH LEG BINDS — count of cells FAILING each leg, by episode:")
    legcols = ["a_H1", "a_H2", "a_DD", "b_H1", "b_H2", "b_OOS", "b_DD", "b_CAGR"]
    fails = ce.groupby("episode")[legcols].apply(lambda d: (~d.astype(bool)).sum())
    P(fails.loc[list(EPISODES)].to_string())
    fails.to_csv(f"{OUT}/{STEM}.legs.csv")
    P("\n  the DD legs in isolation (how often the DD leg ALONE is what fails a 4b):")
    for ep in EPISODES:
        s = ce[ce.episode == ep]
        only_dd = s[(~s.b_DD.astype(bool)) & s.b_H1.astype(bool) & s.b_H2.astype(bool)
                    & s.b_OOS.astype(bool) & s.b_CAGR.astype(bool)]
        P(f"    {ep:9s}  4b failed by the DD cap ALONE: {len(only_dd)}/{len(s)};  "
          f"DD cap failed at all: {int((~s.b_DD.astype(bool)).sum())};  "
          f"CAGR floor failed: {int((~s.b_CAGR.astype(bool)).sum())}")

    # ---------------- LEG C: rule 8
    P("\n" + "=" * 100)
    P("LEG C — RULE 8: book chosen on IS 2010-2016 ONLY (a window with NEITHER episode in it),")
    P("         OOS 2017-2026 read ONCE, then re-scored with the episodes excluded")
    P("=" * 100)
    wrows = []
    for pname in panels:
        iss = ce[(ce.panel == pname) & (ce.episode == "NONE")].set_index("book").IS_Sharpe
        pick = iss.idxmax()
        for ep, yrs in EPISODES.items():
            sel = splice(rets[(pname, pick)].loc[OOS_START:], yrs)
            v2o = splice(rets[(pname, "RULES v2")].loc[OOS_START:], yrs)
            spo = splice(rets[(pname, "SPY")].loc[OOS_START:], yrs)
            m, mv, ms = metrics(sel), metrics(v2o), metrics(spo)
            wrows.append(dict(panel=pname, episode=ep, pick=pick, IS_Sharpe=iss.max(),
                              OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                              v2_OOS_CAGR=mv["CAGR"], v2_OOS_Sharpe=mv["Sharpe"],
                              v2_OOS_MaxDD=mv["MaxDD"], spy_OOS_CAGR=ms["CAGR"],
                              spy_OOS_Sharpe=ms["Sharpe"], spy_OOS_MaxDD=ms["MaxDD"]))
    wf = pd.DataFrame(wrows)
    wf["vs_v2"] = wf.OOS_Sharpe - wf.v2_OOS_Sharpe
    wf["vs_spy"] = wf.OOS_Sharpe - wf.spy_OOS_Sharpe
    wf.to_csv(f"{OUT}/{STEM}.walkforward.csv", index=False)
    P("\n" + wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  the IS window 2010-2016 contains NEITHER excluded episode, so the rule-8 chooser has")
    P(f"  never seen a crash; its picks are {dict(zip(wf.panel, wf.pick))}")
    for ep in EPISODES:
        s = wf[wf.episode == ep]
        P(f"    {ep:9s} pooled OOS: pick {s.OOS_CAGR.mean():7.2%} / {s.OOS_Sharpe.mean():6.3f} / "
          f"{s.OOS_MaxDD.mean():7.2%}   RULES v2 {s.v2_OOS_CAGR.mean():7.2%} / "
          f"{s.v2_OOS_Sharpe.mean():6.3f} / {s.v2_OOS_MaxDD.mean():7.2%}   SPY "
          f"{s.spy_OOS_CAGR.mean():7.2%} / {s.spy_OOS_Sharpe.mean():6.3f} / "
          f"{s.spy_OOS_MaxDD.mean():7.2%}   beats v2 {int((s.vs_v2 > 0).sum())}/{len(s)}  "
          f"beats SPY {int((s.vs_spy > 0).sum())}/{len(s)}")

    P("\n" + "=" * 100)
    P("SURVIVORSHIP (rule 9): all three panels are current constituents; SMALL439 drops the 44")
    P("names with max_1d_move >= 1.0.  Exclusion contrasts are within-book and within-panel, so")
    P("the bias sits in the LEVELS, not in the survival counts this run reports.")
    P("=" * 100)

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
