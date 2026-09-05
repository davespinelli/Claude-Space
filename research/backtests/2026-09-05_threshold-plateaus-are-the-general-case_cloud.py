#!/usr/bin/env python3
"""IDEA 128 — are threshold PLATEAUS the general case?   (cloud, 2026-09-05)

PRE-REGISTERED QUESTION (from QUEUE, written before any number here was read)
    Idea 95 found the vol20 threshold's Sharpe surface spans only 0.009-0.074 over its whole
    published range, with the UNGATED control sitting INSIDE that range in 7 of 8 cells, and
    rule 8 picking opposite endpoints on the two universes (rho -0.70 vs +0.94).  Ideas 66
    (gross) and 84/90 (the gross interval) found the same shape on a different dial.

    Test whether it is GENERAL: for every constant in the standing candidate books
    (band width, position count n, gross, vol threshold, trend lookback K) measure
      (i)   the Sharpe RANGE over the constant's published sweep,
      (ii)  where the NO-INSTRUMENT control sits inside that range,
      (iii) whether rule 8's IS-chosen value beats the control out of sample,
    and propose that PROTOCOL quote the plateau width beside every adopted constant.

TUNED PARAMETERS: none for the measurement — every dial point of every published sweep is
reported.  Rule 8 then chooses ONE value per dial on the IS window only (2009-2016) and reads
2017-2026 once; that is the single tuned parameter, and its control is fixed in advance.

DIALS (5 constants x their published sweeps; the control is stated, not chosen)
    band   b in {0,2,3,5,8}%              published by idea 57/59   control = no gate
    n      in {3,5,10,20,40,all}          published by idea 124/2   control = all (no ranking)
    gross  g in 0.10..1.00 step 0.05      published by idea 66/84   control = 1.00 (no de-grossing)
    vol    v in {0.30..1.20, none}        published by idea 95      control = none (no vol gate)
    K      in {50,100,150,200,250,300}d   the 200d constant itself  control = no gate

CELLS: 3 panels (u56, broad, small) x 2 base books (EWall, TOP20) x 2 cost rungs (10, 25 bps),
weekly, t+1, 75% target gross.  Every number is net.

HARNESS: idea 94's simulator (`run`, validated against engine.backtest to machine precision) is
IMPORTED.  The gate builders here are parameterised versions of idea 94's fixed `gate_mask`;
the script asserts they reproduce idea 94's fixed gates exactly at the published constants
(band 3%, K=200, vol 0.60) before any new number is read.

CAVEATS carried forward, stated not buried:
  - SURVIVORSHIP (idea 54): all three panels are current-constituent lists.  The small panel is a
    sub-$2B screen run TODAY and back-filled to 2010; tickers with max_1d_move >= 1.0 in
    data/small_meta.csv are dropped first (idea 118).  Delisted and acquired names are absent,
    which flatters ungated, full-gross, wide-book settings — i.e. it flatters the CONTROL end of
    every dial here, so a finding that the control sits inside the range is if anything overstated.
  - Idea 38: u56/broad still carry the calendar-day index (BTC-driven weekend rows).
  - Idea 126: t+1 execution only, no lag band.
  - Sharpe RANGE is a within-cell statistic; it is not comparable across panels with different
    return levels, so every table is reported per cell and only counted, never pooled by value.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_threshold-plateaus-are-the-general-case_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
BASE = ["EWall", "TOP20"]
PHI0, DELTA0 = 0.70, 0.60

BANDS = [0.0, 2.0, 3.0, 5.0, 8.0]
NS = [3, 5, 10, 20, 40, "all"]
GROSSES = [float(x) for x in np.round(np.arange(0.10, 1.001, 0.05), 2)]
VOLS = [0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 1.20, np.inf]
KS = [50, 100, 150, 200, 250, 300]
PUBLISHED = {"band": 3.0, "n": 20, "gross": 0.75, "vol": 0.60, "K": 200}
CONTROL = {"band": "nogate", "n": "all", "gross": 1.00, "vol": np.inf, "K": "nogate"}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 2000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ---------------------------------------------------------------- parameterised gates
def ma_gate(px, K):
    return (px > px.rolling(K).mean()).fillna(False)


def band_gate(px, b, K=200):
    """b=0 is the plain K-day MA gate; b>0 is idea 57's sticky +/- b% band."""
    ma = px.rolling(K).mean()
    if b <= 0:
        return (px > ma).fillna(False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b / 100.0), 1.0)
    raw = raw.mask(px < ma * (1 - b / 100.0), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def vol_gate(px, v):
    if not np.isfinite(v):
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    return (H.vol20(px) < v).fillna(False)


def book_weights(px, book, n=None):
    """EWall = equal-weight every name at GROSS.  TOP20 = top-n by idea 94's composite.
       n='all' collapses the ranked book onto EWall, which is the n dial's own control."""
    if book == "EWall" or n == "all":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    nn = H.NTOP if n is None else int(n)
    rank = H.composite(px).rank(axis=1, ascending=False)
    return (rank <= nn).astype(float) * (GROSS / nn)


def weights_for(px, book, dial, val):
    """The de-gross convention (gated-out names -> cash), which is what every standing
       candidate book uses.  Returns (weights, static-gross multiplier m)."""
    W, m = book_weights(px, book), 1.0
    if dial == "band":
        g = band_gate(px, float(val)) if val != "nogate" else None
    elif dial == "K":
        g = ma_gate(px, int(val)) if val != "nogate" else None
    elif dial == "vol":
        g = vol_gate(px, float(val))
    elif dial == "n":
        W, g = book_weights(px, book, val), None
    elif dial == "gross":
        g, m = None, float(val)
    else:
        raise ValueError(dial)
    if g is not None:
        W = W.where(g, 0.0)
    return W, m


DIALS = {"band": BANDS + ["nogate"], "n": NS, "gross": GROSSES,
         "vol": VOLS, "K": KS + ["nogate"]}


def lab(v):
    return "none" if (isinstance(v, float) and not np.isfinite(v)) else str(v)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(pd.Series(a[ok]).rank(), pd.Series(b[ok]).rank())[0, 1])


def panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    inv = [c for c in px.columns if c != "SPY" and c not in bad]
    return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"


# ---------------------------------------------------------------- main
def main():
    say("=" * 190)
    say("IDEA 128 — is the threshold PLATEAU the general case?  5 constants x their published "
        "sweeps x 3 panels x 2 books x 2 cost rungs.")
    say(f"IS <= {IS_END}, OOS >= {OOS_START}.  Weekly, t+1, {GROSS:.0%} target gross, de-gross "
        f"convention.  4b bars: CAGR >= {PHI0} x SPY, MaxDD <= {DELTA0} x |SPY|, Sharpe > SPY in "
        f"both halves AND OOS.")
    say(f"dials: band {BANDS}+nogate | n {NS} | gross {len(GROSSES)} pts 0.10-1.00 | vol {[lab(v) for v in VOLS]} | K {KS}+nogate")
    say(f"published constants {PUBLISHED};  no-instrument controls { {k: lab(v) for k, v in CONTROL.items()} }")
    say("=" * 190)

    rows, WFR = [], []
    REF = {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bars = H.bars_of(spy)
        mS, mSo = metrics(spy), metrics(spy.loc[OOS_START:])
        say(f"\n--- PANEL {pname}: {desc} | eval {start.date()} -> {px.index[-1].date()}")
        say(f"    SPY  full {mS['CAGR']:.2%} / {mS['Sharpe']:.3f} / {mS['MaxDD']:.2%}  halves "
            f"{bars['s1']:.3f}/{bars['s2']:.3f}   OOS {mSo['CAGR']:.2%} / {mSo['Sharpe']:.3f} / {mSo['MaxDD']:.2%}")
        v1 = {}
        for c in COSTS:
            v1[c] = backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
            m1, m1o = metrics(v1[c]), metrics(H.window(v1[c], "OOS"))
            say(f"    RULES v1 @{c:.0f}bps  full {m1['CAGR']:.2%} / {m1['Sharpe']:.3f} / {m1['MaxDD']:.2%}  "
                f"halves {H.halves(v1[c])[0]:.3f}/{H.halves(v1[c])[1]:.3f}   OOS {m1o['CAGR']:.2%} / "
                f"{m1o['Sharpe']:.3f} / {m1o['MaxDD']:.2%}")
        REF[pname] = dict(spy=spy, bars=bars, mS=mS, mSo=mSo, v1=v1)

        # reproduction: the parameterised gates must equal idea 94's fixed ones at the constants
        if pname == "u56":
            chk = [("band3", band_gate(px, 3.0)), ("g200", ma_gate(px, 200)), ("vol60", vol_gate(px, 0.60))]
            for nm, g in chk:
                d = int((g != H.gate_mask(px, nm)).sum().sum())
                say(f"    GATE REPRODUCTION {nm}: {d} differing cells -> {'PASS' if d == 0 else 'FAIL'}")

        for book in BASE:
            for c in COSTS:
                for dial, vals in DIALS.items():
                    if dial == "n" and book != "TOP20":
                        continue                     # the n dial is the ranked book's own dial
                    for v in vals:
                        W, m = weights_for(px, book, dial, v)
                        r = H.run(px, W, m=m, bps=c)["r"].loc[start:]
                        mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
                        h1, h2 = H.halves(r)
                        mg = H.margins(r, bars)
                        rows.append(dict(
                            panel=pname, book=book, cost=c, dial=dial, val=lab(v),
                            is_control=(lab(v) == lab(CONTROL[dial])),
                            is_published=(lab(v) == lab(PUBLISHED[dial])),
                            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                            OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                            pass4a=H.pass4a(r, v1[c]),
                            pass4b=bool(all(mg[k] > 0 for k in ("H1", "H2", "OOS", "DD", "CAGR")))))
                say(f"    ... {pname}/{book}/{c:.0f}bps done")
    G = pd.DataFrame(rows)

    # ---------------------------------------------------------- per (cell, dial) plateau statistics
    say("\n" + "=" * 190)
    say("PLATEAU TABLE — one row per (panel, book, cost, dial).  'ctl pctile' is where the "
        "no-instrument control sits inside the sweep's own Sharpe distribution (0 = worst, 1 = best).")
    P = []
    for (pn, bk, c, dl), d in G.groupby(["panel", "book", "cost", "dial"]):
        s = d.Sharpe
        ctl = d[d.is_control]
        pub = d[d.is_published]
        swp = d[~d.is_control]                       # the instrument's own range, control excluded
        cs = float(ctl.Sharpe.iloc[0]) if len(ctl) else np.nan
        ps = float(pub.Sharpe.iloc[0]) if len(pub) else np.nan
        # rule 8: choose on IS only, read OOS once
        isp = d.loc[d.IS_Sharpe.idxmax()]
        oosbest = d.loc[d.OOS_Sharpe.idxmax()]
        P.append(dict(panel=pn, book=bk, cost=c, dial=dl, pts=len(d),
                      S_min=s.min(), S_max=s.max(), S_range=s.max() - s.min(),
                      sweep_range=(swp.Sharpe.max() - swp.Sharpe.min()) if len(swp) else np.nan,
                      ctl_Sharpe=cs, pub_Sharpe=ps,
                      ctl_pctile=float((s < cs).mean()) if np.isfinite(cs) else np.nan,
                      ctl_inside=bool(np.isfinite(cs) and swp.Sharpe.min() < cs < swp.Sharpe.max()),
                      pub_beats_ctl=bool(np.isfinite(cs) and np.isfinite(ps) and ps > cs),
                      plateau_frac=float((s >= s.max() - 0.05).mean()),
                      argmax_full=str(d.loc[s.idxmax(), "val"]),
                      IS_pick=str(isp["val"]), IS_pick_OOS_Sharpe=isp["OOS_Sharpe"],
                      IS_pick_OOS_CAGR=isp["OOS_CAGR"], IS_pick_OOS_MaxDD=isp["OOS_MaxDD"],
                      ctl_OOS_Sharpe=float(ctl.OOS_Sharpe.iloc[0]) if len(ctl) else np.nan,
                      ctl_OOS_CAGR=float(ctl.OOS_CAGR.iloc[0]) if len(ctl) else np.nan,
                      ctl_OOS_MaxDD=float(ctl.OOS_MaxDD.iloc[0]) if len(ctl) else np.nan,
                      OOS_best_val=str(oosbest["val"]), OOS_best_Sharpe=oosbest["OOS_Sharpe"],
                      rho_IS_OOS=spearman(d.IS_Sharpe, d.OOS_Sharpe),
                      pass4a=int(d.pass4a.sum()), pass4b=int(d.pass4b.sum())))
    PT = pd.DataFrame(P)
    PT["sel_premium"] = PT.IS_pick_OOS_Sharpe - PT.ctl_OOS_Sharpe
    PT["regret"] = PT.OOS_best_Sharpe - PT.IS_pick_OOS_Sharpe
    show = ["panel", "book", "cost", "dial", "pts", "S_min", "S_max", "S_range", "ctl_Sharpe",
            "ctl_pctile", "ctl_inside", "pub_Sharpe", "pub_beats_ctl", "plateau_frac",
            "argmax_full", "IS_pick", "rho_IS_OOS", "sel_premium", "regret", "pass4a", "pass4b"]
    say(PT[show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------- Q1 the headline count
    say("\n" + "=" * 190)
    say("Q1 — IS THE PLATEAU GENERAL?  (idea 95 found the control inside the range in 7 of 8 cells "
        "on ONE dial)")
    say(f"  control strictly inside its own dial's sweep range: {int(PT.ctl_inside.sum())} of {len(PT)} "
        f"(panel, book, cost, dial) rows")
    for dl, d in PT.groupby("dial"):
        say(f"    {dl:6s}  inside {int(d.ctl_inside.sum())}/{len(d)}   Sharpe range median "
            f"{d.S_range.median():.3f} (min {d.S_range.min():.3f}, max {d.S_range.max():.3f})   "
            f"control percentile median {d.ctl_pctile.median():.2f}   published beats control "
            f"{int(d.pub_beats_ctl.sum())}/{len(d)}")
    say(f"\n  published constant beats its own no-instrument control, full-sample Sharpe: "
        f"{int(PT.pub_beats_ctl.sum())} of {len(PT)}")
    say(f"  median Sharpe range across all {len(PT)} dial-cells: {PT.S_range.median():.3f}   "
        f"(idea 95's vol-dial reference: 0.009-0.074)")
    say(f"  median fraction of a dial's points within 0.05 Sharpe of its own best: "
        f"{PT.plateau_frac.median():.2f}")

    # ---------------------------------------------------------- Q2 rule 8
    say("\n" + "=" * 190)
    say("Q2 — RULE 8.  Value chosen by argmax IS Sharpe (2009-2016) ONLY; OOS 2017-2026 read once.")
    say(f"  mean selection premium (OOS Sharpe of the IS pick MINUS OOS Sharpe of the control): "
        f"{PT.sel_premium.mean():+.4f}   median {PT.sel_premium.median():+.4f}   "
        f"positive in {int((PT.sel_premium > 0).sum())} of {int(PT.sel_premium.notna().sum())} dial-cells")
    say(f"  mean OOS regret vs the OOS-best value on the same dial: {PT.regret.mean():.4f}")
    say(f"  Spearman(IS Sharpe, OOS Sharpe) within a dial: median {PT.rho_IS_OOS.median():+.3f}, "
        f"negative in {int((PT.rho_IS_OOS < 0).sum())} of {len(PT)}  "
        f"(idea 95's vol dial: -0.70 on one universe, +0.94 on the other)")
    for dl, d in PT.groupby("dial"):
        say(f"    {dl:6s}  sel premium {d.sel_premium.mean():+.4f}  ({int((d.sel_premium>0).sum())}/{len(d)} +ve)  "
            f"rho median {d.rho_IS_OOS.median():+.3f}  IS picks: {sorted(set(d.IS_pick))}")
    say("\n  OOS of the IS pick vs the control vs SPY vs RULES v1, averaged over the dial-cells of each dial:")
    ref = []
    for pn in PANELS:
        r = REF[pn]
        for c in COSTS:
            m1o = metrics(H.window(r["v1"][c], "OOS"))
            ref.append(dict(panel=pn, cost=c, SPY_OOS_CAGR=r["mSo"]["CAGR"], SPY_OOS_Sharpe=r["mSo"]["Sharpe"],
                            SPY_OOS_MaxDD=r["mSo"]["MaxDD"], v1_OOS_CAGR=m1o["CAGR"],
                            v1_OOS_Sharpe=m1o["Sharpe"], v1_OOS_MaxDD=m1o["MaxDD"]))
    RF = pd.DataFrame(ref)
    say(PT.groupby("dial")[["IS_pick_OOS_CAGR", "IS_pick_OOS_Sharpe", "IS_pick_OOS_MaxDD",
                            "ctl_OOS_CAGR", "ctl_OOS_Sharpe", "ctl_OOS_MaxDD"]]
        .mean().to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  references (per panel/cost):")
    say(RF.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------- Q3 does plateau width predict anything
    say("\n" + "=" * 190)
    say("Q3 — DOES THE PLATEAU WIDTH PREDICT WHETHER TUNING THE CONSTANT PAYS?")
    ok = PT.sel_premium.notna() & PT.S_range.notna()
    say(f"  Spearman(Sharpe range, |selection premium|) = {spearman(PT.S_range[ok], PT.sel_premium[ok].abs()):+.3f}"
        f"   n={int(ok.sum())}")
    say(f"  Spearman(Sharpe range, selection premium)   = {spearman(PT.S_range[ok], PT.sel_premium[ok]):+.3f}")
    say(f"  Spearman(Sharpe range, OOS regret)          = {spearman(PT.S_range[ok], PT.regret[ok]):+.3f}")
    nar, wid = PT[ok & (PT.S_range >= PT.S_range.median())], PT[ok & (PT.S_range < PT.S_range.median())]
    say(f"  narrow-plateau half (range >= median {PT.S_range.median():.3f}): mean premium "
        f"{nar.sel_premium.mean():+.4f} ({int((nar.sel_premium>0).sum())}/{len(nar)} +ve), regret {nar.regret.mean():.3f}")
    say(f"  wide-plateau   half (range <  median):        mean premium "
        f"{wid.sel_premium.mean():+.4f} ({int((wid.sel_premium>0).sum())}/{len(wid)} +ve), regret {wid.regret.mean():.3f}")

    # ---------------------------------------------------------- both KEEP paths
    say("\n" + "=" * 190)
    say("BOTH KEEP PATHS over all dial points (no new book is proposed; these are the standing books)")
    say(f"  4a: {int(G.pass4a.sum())} of {len(G)} dial points   4b: {int(G.pass4b.sum())} of {len(G)}")
    say(f"  4b passes at the PUBLISHED constant: {int(G[G.is_published].pass4b.sum())} of {int(G.is_published.sum())};"
        f"  at the CONTROL: {int(G[G.is_control].pass4b.sum())} of {int(G.is_control.sum())}")
    kb = G[G.pass4b]
    if len(kb):
        say("  every 4b-passing dial point:")
        say(kb[["panel", "book", "cost", "dial", "val", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4a"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        for (pn, bk, c, dl), d in kb.groupby(["panel", "book", "cost", "dial"]):
            sub = G[(G.panel == pn) & (G.book == bk) & (G.cost == c) & (G.dial == dl)]
            say(f"    4b-passing WIDTH  {pn}/{bk}/{c:.0f}bps/{dl}: {len(d)} of {len(sub)} points pass "
                f"-> values {sorted(d.val.tolist())}")

    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    PT.to_csv(OUT / f"{STEM}.plateaus.csv", index=False)
    RF.to_csv(OUT / f"{STEM}.references.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.[grid|plateaus|references].csv + .console.txt")


if __name__ == "__main__":
    main()
