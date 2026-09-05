#!/usr/bin/env python3
"""QUEUE idea 100 — sleeve-with-a-real-diversifier (lane B, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"idea 26's sleeve is 0.63-0.82 correlated with the equity books because 5 of its 9 assets
are equity ETFs.  Re-run the f-grid with the sleeve restricted to TLT/GLD/DBC/UUP (the
non-equity four) at the same inverse-vol risk parity: does a genuinely lower correlation
buy the same Sharpe convexity at less CAGR?"

Two claims to separate, because the queue line conflates them:
  (A) does dropping SPY/QQQ/IWM/EFA/EEM actually lower the sleeve-to-book correlation?
  (B) if it does, does the LOWER correlation buy convexity — dSharpe(f) above the linear
      interpolation of the parts — at a smaller CAGR toll than idea 26's 9-asset sleeve?
(A) is a property of the sleeve; (B) is the mechanism claim.  A sleeve can be less
correlated AND buy less convexity, because convexity depends on the sleeve's own Sharpe
as well as on its correlation:  d(Sharpe_blend)/df at f=0 is governed by
(Sharpe_S - rho * Sharpe_E) * sigma_S / sigma_E, so a sleeve that is less correlated but
also much worse standalone can be the inferior diversifier.  Both terms are measured.

Design (PROTOCOL rules 1-9)
---------------------------
Panels    : `baseline.load_universe()` (56 names) and `load_universe(broad=True)` (136).
            All 9 macro ETFs present in both from 2008-01-02.  SURVIVORSHIP: both lists
            are CURRENT constituents, so every level here is biased upward.
Sleeves   : S9 — idea 26's sleeve verbatim (SPY QQQ IWM EFA EEM TLT GLD DBC UUP).  CONTROL.
            S4 — the idea's sleeve: TLT GLD DBC UUP only.
            IDENTICAL construction otherwise (idea 18 variant B): vote in {0,1/3,2/3,1} on
            the signs of {12-1, 6m, 3m} momentum times inverse-60d-vol risk parity,
            normalised to gross 1.0 within the sleeve.
Books E   : v1 (RULES v1 live, top-5 risk-adjusted, 75% gross), top20 (idea 2's standing
            4b KEEP-candidate, no vol scaler, 75% gross), ewall (idea 10's EWall, 75%).
Blend     : natural   w = (1-f)*E + f*S      (gross drifts with f)
            matched   the same, rescaled per row to E's own gross that day.
            Both REPORTED, not chosen (ideas 66/84: gross is an exact lever with ~zero
            Sharpe content, so the natural blend confounds the mix with a gross change on
            4b's CAGR and MaxDD bars).
Tuned     : exactly 2 — f in {0.00,0.25,0.50,0.75,1.00} and the sleeve in {S9,S4}.
            Book, universe and convention are REPORTED dimensions, not selected over.
            Sleeve lookbacks (252/126/63, 60d vol), the gate (200d, vol20<0.60), gross
            (75%), cadence (weekly) and costs (10 bps) are all held at incumbent values.
            Grid = 5 f x 2 sleeves x 3 books x 2 universes x 2 conventions = 120 points,
            ALL reported.  f=0.00 is the shared control (pure book, sleeve-independent);
            f=1.00 is each sleeve standalone.
Execution : weekly, weights decided at close t applied at t+1 (engine), 10 bps per unit
            turnover, long only, no leverage.
Rule 8    : f chosen on 2009-2016 by IS Sharpe, 2017-2026 evaluated untouched, per
            (universe, book, convention, sleeve); OOS vs the RULES v1 baseline and SPY on
            the same days.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are CALENDAR-day indexed after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return rows.
That deflates daily vol identically for every arm here including the baseline and SPY, so
cross-arm comparisons are apples-to-apples; absolute Sharpe levels are not trustworthy
until idea 38 lands.

Deterministic, standalone:
    python research/backtests/2026-09-05_sleeve-with-a-real-diversifier_B.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
GROSS = 0.75
MACRO9 = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
MACRO4 = ["TLT", "GLD", "DBC", "UUP"]
SLEEVES = {"S9": MACRO9, "S4": MACRO4}
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
SPLIT = "2017-01-01"
IS_END = "2016-12-31"
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- sleeve (idea 18 B)
def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """macro-trend-ensemble variant B on `assets`; zero everywhere else."""
    sub = px[assets]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


# ---------------------------------------------------------------- equity books
def book_v1(px):
    return rules_v1_weights(px)


def book_top20(px, n=20):
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def book_ewall(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = (above & (vol20 < 0.60) & s.notna()).astype(float)
    k = elig.sum(axis=1)
    return elig.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


BOOKS = {"v1": book_v1, "top20": book_top20, "ewall": book_ewall}


def blend(E, S, f, matched):
    w = (1 - f) * E + f * S
    if not matched:
        return w
    gE, gW = E.sum(axis=1), w.sum(axis=1)
    scale = (gE / gW.where(gW > 1e-12)).fillna(0.0)
    return w.mul(scale, axis=0)


# ---------------------------------------------------------------- metrics helpers
def stats(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"])


def full_row(r):
    h = len(r) // 2
    a, b, c = stats(r), stats(r.iloc[:h]), stats(r.iloc[h:])
    o, i = stats(r.loc[SPLIT:]), stats(r.loc[:IS_END])
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], Vol=a["Vol"],
                H1=b["Sharpe"], H2=c["Sharpe"],
                IS_Sharpe=i["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"],
                OOS_MaxDD=o["MaxDD"])


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"]
                and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"]          # both negative
                and row["CAGR"] >= 0.70 * spy["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main
def run_universe(tag, px, records):
    start = px.index[260]
    print("=" * 108)
    print(f"### UNIVERSE {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}"
          f"  | eval from {start.date()}")

    base_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    base, spy = full_row(base_r), full_row(spy_r)
    print("\nReference rows (same days, same costs):")
    print(fmt(pd.DataFrame({"RULES v1 baseline": base, "SPY": spy}).T))
    print(f"\n4b bars on this window: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / "
          f"OOS {spy['OOS_Sharpe']:.3f} · MaxDD >= {0.60*spy['MaxDD']:.1%} · CAGR >= {0.70*spy['CAGR']:.2%}")

    S = {k: sleeve_weights(px, a) for k, a in SLEEVES.items()}

    print("\n--- Standalone sleeves (f=1.00, gross 100% within the sleeve)")
    srows = {}
    for k, w in S.items():
        r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        srows[f"{k} ({len(SLEEVES[k])} assets)"] = full_row(r)
    print(fmt(pd.DataFrame(srows).T))

    for bname, bfn in BOOKS.items():
        E = bfn(px)
        for sname in SLEEVES:
            for matched in (False, True):
                conv = "matched" if matched else "natural"
                rows = []
                for f in FGRID:
                    w = blend(E, S[sname], f, matched)
                    res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
                    r = res["returns"].loc[start:]
                    row = full_row(r)
                    row["Turn/yr"] = res["turnover"].loc[start:].sum() / (len(r) / 252)
                    row["Gross"] = w.loc[start:].sum(axis=1).mean()
                    row["4a"] = keep_4a(row, base)
                    row["4b"] = keep_4b(row, spy)
                    rows.append(dict(universe=tag, book=bname, sleeve=sname, conv=conv, f=f, **row))
                    records.append(rows[-1])
                df = pd.DataFrame(rows).set_index("f")[
                    ["Gross", "Turn/yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                     "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a", "4b"]]
                print(f"\n--- {tag} | book={bname} | sleeve={sname} | blend={conv} | "
                      f"f = sleeve fraction (f=0 pure book, f=1 pure sleeve)")
                print(fmt(df))
    return base, spy


def correlations(tag, px):
    """Claim (A): does dropping the 5 equity ETFs actually lower the correlation?"""
    start = px.index[260]
    cols = {}
    for k, a in SLEEVES.items():
        cols[k] = backtest(px, sleeve_weights(px, a), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    for bname, bfn in BOOKS.items():
        cols[bname] = backtest(px, bfn(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    cols["SPY"] = px["SPY"].pct_change().fillna(0).loc[start:]
    C = pd.DataFrame(cols).corr()
    print(f"--- {tag}: daily-return correlation")
    print(fmt(C))
    sub = C.loc[list(SLEEVES), list(BOOKS) + ["SPY"]]
    print(f"    S9 vs books/SPY: [{sub.loc['S9'].min():.3f}, {sub.loc['S9'].max():.3f}]   "
          f"S4 vs books/SPY: [{sub.loc['S4'].min():.3f}, {sub.loc['S4'].max():.3f}]")
    out = []
    for k in SLEEVES:
        for c in list(BOOKS) + ["SPY"]:
            out.append(dict(universe=tag, sleeve=k, book=c, corr=C.loc[k, c]))
    return pd.DataFrame(out)


def main():
    panels = [("u56", load_universe()), ("broad", load_universe(broad=True))]
    records, refs = [], {}
    for tag, px in panels:
        refs[tag] = run_universe(tag, px, records)
    G = pd.DataFrame(records)
    OUT.with_suffix(".grid.csv").write_text(G.to_csv(index=False))

    # ------------------------------------------------- claim (A): correlation
    print("\n" + "=" * 108)
    print("### CLAIM (A) — is S4 genuinely the less correlated sleeve?\n")
    CORR = pd.concat([correlations(tag, px) for tag, px in panels], ignore_index=True)
    OUT.with_suffix(".correlations.csv").write_text(CORR.to_csv(index=False))
    piv = CORR.pivot_table(index=["universe", "book"], columns="sleeve", values="corr")
    piv["S4 - S9"] = piv["S4"] - piv["S9"]
    print("\nPer (universe, book):")
    print(fmt(piv))
    print(f"\nS4 lower in {int((piv['S4 - S9'] < 0).sum())}/{len(piv)} cells; "
          f"mean gap {piv['S4 - S9'].mean():+.3f}")

    # ------------------------------------------------- claim (B): convexity
    print("\n" + "=" * 108)
    print("### CLAIM (B) — Sharpe convexity, and what it costs in CAGR")
    print("dSharpe(f) = Sharpe(blend) - [(1-f)*Sharpe(f=0) + f*Sharpe(f=1)]  ; >0 = real diversification")
    print("dCAGR(f)   = CAGR(blend) - CAGR(f=0)                              ; the toll paid")
    print("rate       = dSharpe / (-dCAGR in pp)                             ; Sharpe bought per pp of CAGR\n")
    dv = []
    for (tag, bname, sname, conv), sub in G.groupby(["universe", "book", "sleeve", "conv"], sort=False):
        s = sub.set_index("f")["Sharpe"]
        c = sub.set_index("f")["CAGR"]
        for f in FGRID[1:-1]:
            lin = (1 - f) * s[0.0] + f * s[1.0]
            dc_pp = (c[f] - c[0.0]) * 100
            dv.append(dict(universe=tag, book=bname, sleeve=sname, conv=conv, f=f,
                           Sharpe=s[f], lin=lin, dSharpe=s[f] - lin,
                           dCAGR_pp=dc_pp,
                           rate=(s[f] - lin) / (-dc_pp) if dc_pp < 0 else np.nan))
    D = pd.DataFrame(dv)
    OUT.with_suffix(".diversification.csv").write_text(D.to_csv(index=False))
    print(fmt(D.set_index(["universe", "book", "sleeve", "conv", "f"])))
    print("\nBy sleeve:")
    summ = D.groupby("sleeve").agg(
        n=("dSharpe", "size"), dSharpe_mean=("dSharpe", "mean"), dSharpe_med=("dSharpe", "median"),
        dSharpe_min=("dSharpe", "min"), dSharpe_max=("dSharpe", "max"),
        pos=("dSharpe", lambda x: int((x > 0).sum())),
        dCAGR_pp_mean=("dCAGR_pp", "mean"), rate_med=("rate", "median"))
    print(fmt(summ))
    # paired, cell by cell (same universe/book/conv/f): S4 vs S9
    P = D.pivot_table(index=["universe", "book", "conv", "f"], columns="sleeve",
                      values=["dSharpe", "dCAGR_pp", "rate"])
    pair = pd.DataFrame({
        "dSharpe_S9": P[("dSharpe", "S9")], "dSharpe_S4": P[("dSharpe", "S4")],
        "conv_gap": P[("dSharpe", "S4")] - P[("dSharpe", "S9")],
        "dCAGR_S9": P[("dCAGR_pp", "S9")], "dCAGR_S4": P[("dCAGR_pp", "S4")],
        "toll_gap": P[("dCAGR_pp", "S4")] - P[("dCAGR_pp", "S9")],
        "rate_S9": P[("rate", "S9")], "rate_S4": P[("rate", "S4")]})
    print("\nPaired S4-vs-S9 in the same cell (conv_gap>0 = S4 buys MORE convexity; "
          "toll_gap>0 = S4 costs LESS CAGR):")
    print(fmt(pair))
    print(f"\nS4 convexity > S9 in {int((pair['conv_gap'] > 0).sum())}/{len(pair)} cells "
          f"(mean {pair['conv_gap'].mean():+.3f}); "
          f"S4 toll smaller in {int((pair['toll_gap'] > 0).sum())}/{len(pair)} "
          f"(mean {pair['toll_gap'].mean():+.2f} pp); "
          f"S4 rate > S9 in {int((pair['rate_S4'] > pair['rate_S9']).sum())}/{len(pair)}")
    OUT.with_suffix(".paired.csv").write_text(pair.to_csv())

    # ------------------------------------------------- rule 8
    print("\n" + "=" * 108)
    print("### PROTOCOL rule 8 — f chosen on 2009-2016 by IS Sharpe, 2017-2026 untouched\n")
    wf = []
    for (tag, bname, sname, conv), sub in G.groupby(["universe", "book", "sleeve", "conv"], sort=False):
        pick = sub.loc[sub["IS_Sharpe"].idxmax()]
        base, spy = refs[tag]
        wf.append(dict(universe=tag, book=bname, sleeve=sname, conv=conv, f_star=pick["f"],
                       IS_Sharpe=pick["IS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"],
                       OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                       base_OOS_Sharpe=base["OOS_Sharpe"], base_OOS_CAGR=base["OOS_CAGR"],
                       base_OOS_MaxDD=base["OOS_MaxDD"],
                       spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                       spy_OOS_MaxDD=spy["OOS_MaxDD"],
                       beats_base=bool(pick["OOS_Sharpe"] > base["OOS_Sharpe"]),
                       beats_spy=bool(pick["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                       full_4a=bool(pick["4a"]), full_4b=bool(pick["4b"])))
    W = pd.DataFrame(wf)
    print(fmt(W.set_index(["universe", "book", "sleeve", "conv"])))
    OUT.with_suffix(".walkforward.csv").write_text(W.to_csv(index=False))
    print(f"\nf* = 0.00 (the selector refuses the sleeve) in {int((W['f_star'] == 0).sum())}/{len(W)} cells; "
          f"beats baseline OOS in {int(W['beats_base'].sum())}/{len(W)}; "
          f"beats SPY OOS in {int(W['beats_spy'].sum())}/{len(W)}")
    print("\nIS vs OOS Sharpe monotonicity in f (idea 99's question, measured here for both sleeves):")
    mono = []
    for (tag, bname, sname, conv), sub in G.groupby(["universe", "book", "sleeve", "conv"], sort=False):
        s = sub.sort_values("f")
        mono.append(dict(universe=tag, book=bname, sleeve=sname, conv=conv,
                         IS_slope=np.polyfit(s["f"], s["IS_Sharpe"], 1)[0],
                         OOS_slope=np.polyfit(s["f"], s["OOS_Sharpe"], 1)[0]))
    M = pd.DataFrame(mono)
    print(fmt(M.groupby("sleeve")[["IS_slope", "OOS_slope"]].agg(["mean", "min", "max"])))

    # ------------------------------------------------- census
    print("\n" + "=" * 108)
    n4a, n4b = int(G["4a"].sum()), int(G["4b"].sum())
    print(f"### CENSUS over all {len(G)} grid points: 4a passes {n4a}, 4b passes {n4b}")
    if n4a or n4b:
        print(fmt(G[G["4a"] | G["4b"]].set_index(["universe", "book", "sleeve", "conv", "f"])[
            ["Gross", "Turn/yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "4a", "4b"]]))
    inner = G[(G["f"] > 0) & (G["f"] < 1)]
    print(f"\nInterior points only (the idea itself, f in {FGRID[1:-1]}): {len(inner)} points, "
          f"4a {int(inner['4a'].sum())}, 4b {int(inner['4b'].sum())}")
    for sname in SLEEVES:
        sub = inner[inner["sleeve"] == sname]
        print(f"  sleeve {sname}: {len(sub)} interior points, 4a {int(sub['4a'].sum())}, "
              f"4b {int(sub['4b'].sum())}")

    # cross-universe 4b: the bar idea 26's by-product had to clear
    print("\nCross-universe 4b (same book/sleeve/conv/f passing on BOTH universes):")
    cu = G[G["4b"]].groupby(["book", "sleeve", "conv", "f"]).size()
    cu = cu[cu == 2]
    print("  " + (", ".join(f"{b}/{s}/{c}/f={f}" for (b, s, c, f) in cu.index) if len(cu) else "none"))

    # ------------------------------------------------- year attribution
    print("\n" + "=" * 108)
    print("### Calendar-year returns — where does each sleeve pay? (top20 book, f=0.25 natural)\n")
    for tag, px in panels:
        start = px.index[260]
        E = book_top20(px)
        cols = {"top20 (f=0)": backtest(px, E, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]}
        for k, a in SLEEVES.items():
            S = sleeve_weights(px, a)
            cols[f"top20 +25% {k}"] = backtest(px, blend(E, S, 0.25, False),
                                               cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
            cols[f"{k} alone"] = backtest(px, S, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        cols["SPY"] = px["SPY"].pct_change().fillna(0).loc[start:]
        Y = pd.DataFrame(cols).groupby(lambda d: d.year).apply(lambda x: (1 + x).prod() - 1)
        Y["S9 effect"] = Y["top20 +25% S9"] - Y["top20 (f=0)"]
        Y["S4 effect"] = Y["top20 +25% S4"] - Y["top20 (f=0)"]
        print(f"--- {tag}")
        print(Y.to_string(float_format=lambda x: f"{x:+.1%}"))
        print(f"    S9 effect positive in {int((Y['S9 effect'] > 0).sum())}/{len(Y)} years; "
              f"S4 effect positive in {int((Y['S4 effect'] > 0).sum())}/{len(Y)} years")
        print()

    # ------------------------------------------------- cost ladder
    print("=" * 108)
    print("### Cost sensitivity (control, not a tuned parameter): top20 + f=0.25, both sleeves,")
    print("    BOTH conventions — the cross-universe 4b passes live in `matched`.\n")
    ladder = []
    for tag, px in panels:
        start = px.index[260]
        E = book_top20(px)
        spy = full_row(px["SPY"].pct_change().fillna(0).loc[start:])
        for c in (5, 10, 15, 20, 25):
            for sname, a in SLEEVES.items():
                S = sleeve_weights(px, a)
                for matched in (False, True):
                    for f in (0.00, 0.25):
                        r = backtest(px, blend(E, S, f, matched),
                                     cost_bps=c, freq=FREQ)["returns"].loc[start:]
                        row = full_row(r)
                        ladder.append(dict(universe=tag, sleeve=sname,
                                           conv="matched" if matched else "natural",
                                           cost_bps=c, f=f,
                                           CAGR=row["CAGR"], Sharpe=row["Sharpe"], MaxDD=row["MaxDD"],
                                           H1=row["H1"], H2=row["H2"], OOS_Sharpe=row["OOS_Sharpe"],
                                           **{"4b": keep_4b(row, spy)}))
    L = pd.DataFrame(ladder)
    print(fmt(L.set_index(["universe", "sleeve", "conv", "cost_bps", "f"])))
    OUT.with_suffix(".costladder.csv").write_text(L.to_csv(index=False))
    for tag in ("u56", "broad"):
        for sname in SLEEVES:
            sub = L[(L.universe == tag) & (L.sleeve == sname) & (L.conv == "matched") & (L.f == 0.25)]
            ok = sub[sub["4b"]]["cost_bps"]
            print(f"    {tag}/top20/{sname}/matched/f=0.25 passes 4b up to "
                  f"{int(ok.max()) if len(ok) else 'never'} bps")

    # ------------------------------------------------- one-year dependence (idea 98's question)
    print("\n" + "=" * 108)
    print("### One-year dependence — idea 26's by-product was killed as a KEEP because its whole")
    print("    effect was 2022.  Same test on the S4 candidate: delete 2022 and re-measure.\n")
    loyo = []
    for tag, px in panels:
        start = px.index[260]
        E = book_top20(px)
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        arms = {"top20 f=0": backtest(px, E, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]}
        for sname, a in SLEEVES.items():
            S = sleeve_weights(px, a)
            arms[f"top20 +25% {sname} matched"] = backtest(
                px, blend(E, S, 0.25, True), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        arms["SPY"] = spy_r
        for nm, r in arms.items():
            keep_idx = r.index.year != 2022
            loyo.append(dict(universe=tag, arm=nm,
                             Sharpe_full=metrics(r)["Sharpe"],
                             Sharpe_ex22=metrics(r[keep_idx])["Sharpe"],
                             dSharpe=metrics(r[keep_idx])["Sharpe"] - metrics(r)["Sharpe"],
                             CAGR_full=metrics(r)["CAGR"],
                             CAGR_ex22=metrics(r[keep_idx])["CAGR"]))
    LY = pd.DataFrame(loyo)
    print(fmt(LY.set_index(["universe", "arm"])))
    OUT.with_suffix(".ex2022.csv").write_text(LY.to_csv(index=False))
    for tag in ("u56", "broad"):
        s = LY[LY.universe == tag].set_index("arm")
        for sname in SLEEVES:
            arm = f"top20 +25% {sname} matched"
            print(f"    {tag}: {sname} Sharpe edge over the f=0 book "
                  f"full {s.loc[arm,'Sharpe_full'] - s.loc['top20 f=0','Sharpe_full']:+.3f} -> "
                  f"ex-2022 {s.loc[arm,'Sharpe_ex22'] - s.loc['top20 f=0','Sharpe_ex22']:+.3f}")

    print(f"\nGrids written: {OUT.name}.grid.csv / .correlations.csv / .diversification.csv / "
          f".paired.csv / .walkforward.csv / .costladder.csv")


if __name__ == "__main__":
    main()
