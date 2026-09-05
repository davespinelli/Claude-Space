#!/usr/bin/env python3
"""QUEUE idea 102 — which-asset-carries-S4 (lane C, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"Idea 100's diversifier is 4 assets in a sample where 2009-2021 is a falling-rate regime and
its single materially positive year (2022) is the year its duration vote went short.  Drop
each of TLT/GLD/DBC/UUP in turn (and run TLT-only) at f=0.50 on both universes: is the sleeve
a diversifier or is it TLT?  Max 2 params."

Idea 100 (PARK, strong) found that S4 = {TLT,GLD,DBC,UUP} at the idea-18 trend-vote x
inverse-vol construction is 5.1x more convex than the 9-asset S9 sleeve, is rule-8 selectable
(f=0.50 picked in 8/8 cells) and, re-grossed to g=1.00, clears 4b on BOTH universes
(u56 11.8%/1.149/-14.2%; broad 12.2%/1.063/-15.6%).  Its own caveat is that the sample is a
falling-rate regime.  If the sleeve is really a duration bet, then
  (a) dropping TLT should collapse the benefit, and
  (b) TLT-only should reproduce most of it,
and the 4b pass should be read as an artefact of 2009-2021 rates.  If instead the benefit
survives every single-asset deletion, the sleeve is a genuine multi-asset diversifier and the
2022 year is a coincidence of sign, not the source of the edge.

Design (PROTOCOL rules 1-9)
---------------------------
Panels      : `load_universe()` (56) and `load_universe(broad=True)` (136).  All four sleeve
              assets are present in both.  SURVIVORSHIP: current constituents; equity levels
              biased up.  The sleeve's assets are ETFs and are not exposed to this.
TUNED (2)   : sleeve composition in {S4, noTLT, noGLD, noDBC, noUUP, TLTonly}  x
              f in {0.00, 0.25, 0.50, 0.75, 1.00}.  The queue pre-registers f=0.50 as the
              headline; the full f-grid is reported so nothing is hidden, and rule 8 selects
              over the joint 6x5 surface.  ALL 240 grid points are written to .grid.csv.
CONTROLS    : book in {top20 (idea 2's standing KEEP / idea 100's arm), ewall (idea 10)},
              universe in {u56, broad}, gross convention in {natural, g=1.00}, cost in
              {5,10,15,20,25} bps.  Reported, never selected on.
              g=1.00 is fully invested, NOT leverage; it is the convention under which idea
              100's arm passes 4b and idea 101 is re-running it, so it must appear here or
              this run cannot speak to the candidate that matters.
Sleeve      : idea 18 variant B verbatim, restricted to the variant's assets: vote in
              {0,1/3,2/3,1} on the signs of {12-1, 6m, 3m} times inverse-60d-vol risk parity,
              row-normalised to 1.0.  Lookbacks, gate, cadence (W) and the 0.75 book gross are
              held at the incumbents' values.
Rule 8      : (sleeve, f) chosen on 2009-2016 by IS Sharpe, 2017-2026 evaluated untouched, per
              (universe, book, convention).  OOS CAGR/Sharpe/MaxDD reported vs RULES v1 and SPY.
Regime      : pre-registered split at 2022-01-01 (falling-rate 2009-2021 vs rising 2022-2026),
              plus per-year asset-level attribution inside the sleeve.

COST NOTE: engine.backtest applies costs as `gross_returns - turnover * bps/1e4` with the
holdings path independent of bps, so this script runs each weight matrix ONCE at 0 bps and
derives every rung of the ladder exactly.  Asserted against a direct 10 bps run at start-up.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return rows.
It hits every arm, the baseline and SPY identically — cross-arm comparisons are
apples-to-apples; absolute Sharpe levels wait on idea 38.

Deterministic, standalone:
    python research/backtests/2026-09-05_which-asset-carries-S4_C.py
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
COST_LADDER = (5, 10, 15, 20, 25)
FREQ = "W"
GROSS = 0.75
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
F_STAR = 0.50                      # pre-registered headline (queue wording)
SPLIT = "2017-01-01"               # rule 8 OOS start
IS_END = "2016-12-31"
REGIME_SPLIT = "2022-01-01"        # pre-registered falling- vs rising-rate boundary
S4 = ["TLT", "GLD", "DBC", "UUP"]
SLEEVES = {
    "S4": S4,                                    # control — idea 100's sleeve verbatim
    "noTLT": ["GLD", "DBC", "UUP"],
    "noGLD": ["TLT", "DBC", "UUP"],
    "noDBC": ["TLT", "GLD", "UUP"],
    "noUUP": ["TLT", "GLD", "DBC"],
    "TLTonly": ["TLT"],
}
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- sleeve construction
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
    """idea 18 variant B, restricted to `assets`; zero everywhere else."""
    sub = px[assets]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


# ---------------------------------------------------------------- equity books
def book_top20(px, n=20):
    s, above, vol20 = score(px, vol_scale=False)
    rank = s.where(above & (vol20 < 0.60)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def book_ewall(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = (above & (vol20 < 0.60) & s.notna()).astype(float)
    k = elig.sum(axis=1)
    return elig.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


BOOKS = {"top20": book_top20, "ewall": book_ewall}


def blend(E, S, f, conv):
    """conv='natural' -> (1-f)E + fS as-is; conv='g1.00' -> the same rescaled to 1.0 gross."""
    w = (1 - f) * E + f * S
    if conv == "natural":
        return w
    g = w.sum(axis=1)
    return w.mul((1.0 / g.where(g > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- run / metrics helpers
def run(px, w, start):
    """One backtest at 0 bps; returns (gross returns, turnover) so any cost is exact."""
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def net(gr, to, bps=COST_BPS):
    return gr - to * bps / 1e4


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    _, i_s, _ = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
    fc, fs, fd = stats(r.loc[:"2021-12-31"])
    rc, rs, rd = stats(r.loc[REGIME_SPLIT:])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2, IS_Sharpe=i_s,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                FALL_CAGR=fc, FALL_Sharpe=fs, FALL_MaxDD=fd,
                RISE_CAGR=rc, RISE_Sharpe=rs, RISE_MaxDD=rd)


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main
def main():
    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}

    # -- cost-linearity assertion (the whole run depends on it)
    px0 = universes["u56"]
    st0 = px0.index[260]
    w0 = book_top20(px0)
    gr0, to0 = run(px0, w0, st0)
    direct = backtest(px0, w0, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[st0:]
    err = float((net(gr0, to0) - direct).abs().max())
    print(f"[check] cost linearity max |derived - direct| at {COST_BPS} bps = {err:.2e}")
    assert err < 1e-12, "cost is not linear in this engine — ladder derivation invalid"

    records, refs, cache = [], {}, {}
    for tag, px in universes.items():
        start = px.index[260]
        print("=" * 118)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> "
              f"{px.index[-1].date()} | eval from {start.date()}")
        missing = [t for t in S4 if t not in px.columns]
        if missing:
            raise SystemExit(f"missing sleeve tickers in {tag}: {missing}")

        bgr, bto = run(px, rules_v1_weights(px), start)
        base = full_row(net(bgr, bto))
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        refs[tag] = (base, spy)
        print("\nReference rows (same days, same costs):")
        print(fmt(pd.DataFrame({"RULES v1 baseline": base, "SPY": spy}).T))
        print(f"\n4b bars: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / OOS "
              f"{spy['OOS_Sharpe']:.3f} · MaxDD >= {0.60 * spy['MaxDD']:.1%} · "
              f"CAGR >= {0.70 * spy['CAGR']:.2%}")

        for bname, bfn in BOOKS.items():
            E = bfn(px)
            for conv in ("natural", "g1.00"):
                for sname, assets in SLEEVES.items():
                    rows = []
                    for f in FGRID:
                        w = blend(E, sleeve_weights(px, assets), f, conv)
                        gr, to = run(px, w, start)
                        cache[(tag, bname, conv, sname, f)] = (gr, to)
                        r = net(gr, to)
                        row = full_row(r)
                        row["Turn/yr"] = to.sum() / (len(r) / 252)
                        row["Gross"] = w.loc[start:].sum(axis=1).mean()
                        row["4a"] = keep_4a(row, base)
                        row["4b"] = keep_4b(row, spy)
                        rows.append(dict(universe=tag, book=bname, conv=conv, sleeve=sname, f=f, **row))
                        records.append(rows[-1])
                    df = pd.DataFrame(rows).set_index("f")[
                        ["Gross", "Turn/yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a", "4b"]]
                    print(f"\n--- {tag} | book={bname} | conv={conv} | sleeve={sname} "
                          f"(f=0 pure book, f=1 pure sleeve)")
                    print(fmt(df))
    G = pd.DataFrame(records)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)

    # ---------------------------------------------------------- (1) the sleeves themselves
    print("\n" + "=" * 118)
    print("### (1) THE SLEEVES STANDALONE — is TLT the sleeve?")
    print("Each variant run alone (f=1.00, no equity book), plus its correlation to the books.\n")
    sa, cr = [], []
    for tag, px in universes.items():
        start = px.index[260]
        cols = {"SPY": px["SPY"].pct_change().fillna(0).loc[start:]}
        for sname, assets in SLEEVES.items():
            gr, to = cache[(tag, "top20", "natural", sname, 1.00)]
            r = net(gr, to)
            cols[sname] = r
            row = full_row(r)
            row.update(universe=tag, sleeve=sname, assets="+".join(assets),
                       Turn_yr=to.sum() / (len(r) / 252))
            sa.append(row)
        for bname in BOOKS:
            gr, to = cache[(tag, bname, "natural", "S4", 0.00)]
            cols[bname] = net(gr, to)
        C = pd.DataFrame(cols).corr()
        print(f"--- {tag}: standalone sleeve variants")
        print(fmt(pd.DataFrame([s for s in sa if s["universe"] == tag]).set_index("sleeve")[
            ["assets", "CAGR", "Sharpe", "MaxDD", "FALL_CAGR", "FALL_Sharpe", "RISE_CAGR",
             "RISE_Sharpe", "Turn_yr"]]))
        print(f"\n--- {tag}: daily-return correlations")
        print(fmt(C))
        for sname in SLEEVES:
            for bname in list(BOOKS) + ["SPY"]:
                cr.append(dict(universe=tag, sleeve=sname, book=bname, corr=C.loc[sname, bname]))
        print()
    SA = pd.DataFrame(sa)
    SA.to_csv(OUT.with_suffix(".standalone.csv"), index=False)
    CR = pd.DataFrame(cr)
    CR.to_csv(OUT.with_suffix(".correlation.csv"), index=False)
    print("Sleeve-to-book correlation by variant (min..max over books x universes):")
    print(fmt(CR[CR.book != "SPY"].groupby("sleeve")["corr"].agg(["min", "max", "mean"])))

    # ---------------------------------------------------------- (2) the deletion test
    print("\n" + "=" * 118)
    print(f"### (2) THE DELETION TEST at the pre-registered f={F_STAR:.2f}")
    print("dSharpe = Sharpe(blend) - Sharpe(book alone, same convention).")
    print("If the sleeve is TLT: noTLT collapses toward 0 and TLTonly reproduces S4.")
    print("If it is diversification: every deletion keeps most of S4's dSharpe.\n")
    dl = []
    for tag in universes:
        for bname in BOOKS:
            for conv in ("natural", "g1.00"):
                anchor = full_row(net(*cache[(tag, bname, conv, "S4", 0.00)]))
                for sname in SLEEVES:
                    row = full_row(net(*cache[(tag, bname, conv, sname, F_STAR)]))
                    dl.append(dict(universe=tag, book=bname, conv=conv, sleeve=sname,
                                   CAGR=row["CAGR"], Sharpe=row["Sharpe"], MaxDD=row["MaxDD"],
                                   dSharpe=row["Sharpe"] - anchor["Sharpe"],
                                   dCAGR=row["CAGR"] - anchor["CAGR"],
                                   dMaxDD=row["MaxDD"] - anchor["MaxDD"],
                                   OOS_Sharpe=row["OOS_Sharpe"],
                                   RISE_Sharpe=row["RISE_Sharpe"], FALL_Sharpe=row["FALL_Sharpe"]))
    DL = pd.DataFrame(dl)
    DL.to_csv(OUT.with_suffix(".deletion.csv"), index=False)
    print(fmt(DL.set_index(["universe", "book", "conv", "sleeve"])))
    piv = DL.pivot_table(index=["universe", "book", "conv"], columns="sleeve", values="dSharpe")
    piv = piv[["S4", "noTLT", "noGLD", "noDBC", "noUUP", "TLTonly"]]
    print("\ndSharpe vs the same book alone, by variant (columns) and cell (rows):")
    print(fmt(piv))
    print("\nRetention of S4's dSharpe when one asset is deleted (variant / S4):")
    ret = piv.div(piv["S4"], axis=0)
    print(fmt(ret))
    print(f"\nmean dSharpe: " + ", ".join(f"{s} {piv[s].mean():+.3f}" for s in piv.columns))
    print(f"cells where dSharpe > 0: " + ", ".join(f"{s} {int((piv[s] > 0).sum())}/{len(piv)}"
                                                   for s in piv.columns))

    # ---------------------------------------------------------- (3) rate regime
    print("\n" + "=" * 118)
    print(f"### (3) RATE REGIME — falling 2009-2021 vs rising {REGIME_SPLIT[:4]}-2026")
    print("The queue's suspicion: the sleeve's value is a duration bet in a falling-rate sample.")
    print(f"Table: dSharpe vs the book alone within each regime, f={F_STAR:.2f}.\n")
    rg = []
    for tag in universes:
        for bname in BOOKS:
            for conv in ("natural", "g1.00"):
                a = full_row(net(*cache[(tag, bname, conv, "S4", 0.00)]))
                for sname in SLEEVES:
                    row = full_row(net(*cache[(tag, bname, conv, sname, F_STAR)]))
                    rg.append(dict(universe=tag, book=bname, conv=conv, sleeve=sname,
                                   dS_fall=row["FALL_Sharpe"] - a["FALL_Sharpe"],
                                   dS_rise=row["RISE_Sharpe"] - a["RISE_Sharpe"],
                                   dC_fall=row["FALL_CAGR"] - a["FALL_CAGR"],
                                   dC_rise=row["RISE_CAGR"] - a["RISE_CAGR"],
                                   dDD_rise=row["RISE_MaxDD"] - a["RISE_MaxDD"]))
    RG = pd.DataFrame(rg)
    RG.to_csv(OUT.with_suffix(".regime.csv"), index=False)
    print(fmt(RG.pivot_table(index=["universe", "book", "conv"], columns="sleeve",
                             values=["dS_fall", "dS_rise"])))
    print("\nmean by variant:")
    print(fmt(RG.groupby("sleeve")[["dS_fall", "dS_rise", "dC_fall", "dC_rise", "dDD_rise"]].mean()))

    # ---------------------------------------------------------- (4) inside the sleeve
    print("\n" + "=" * 118)
    print("### (4) INSIDE S4 — per-asset weight and return contribution, by year (u56)")
    print("contribution_a = sum_t w_a(t-1) * ret_a(t), compounding ignored (additive attribution).\n")
    px = universes["u56"]
    start = px.index[260]
    S = sleeve_weights(px, S4)
    W = S.shift(1).loc[start:, S4]
    R = px.pct_change().fillna(0).loc[start:, S4]
    contrib = (W * R)
    yr = contrib.groupby(lambda d: d.year).sum()
    yr["sleeve total"] = yr.sum(axis=1)
    wbar = W.groupby(lambda d: d.year).mean()
    print("Return contribution by asset and year:")
    print(yr.to_string(float_format=lambda x: f"{x:+.2%}"))
    print("\nMean weight by asset and year:")
    print(wbar.to_string(float_format=lambda x: f"{x:.2f}"))
    tot = contrib.sum()
    print("\nFull-sample contribution: " + ", ".join(f"{a} {tot[a]:+.1%}" for a in S4) +
          f" | total {tot.sum():+.1%} | TLT share {tot['TLT'] / tot.sum():.1%}")
    yr.to_csv(OUT.with_suffix(".attribution.csv"))

    # 2022 duration-vote check the queue asks about explicitly
    v = _vote_mom(px[S4]).loc["2022-01-01":"2022-12-31", "TLT"]
    print(f"\n2022 TLT trend vote: mean {v.mean():.2f}, days at 0 (fully short-duration) "
          f"{int((v == 0).sum())}/{len(v)}; 2022 TLT contribution {yr.loc[2022, 'TLT']:+.2%}")

    # ---------------------------------------------------------- (5) rule 8
    print("\n" + "=" * 118)
    print("### (5) PROTOCOL rule 8 — (sleeve, f) chosen on 2009-2016 IS Sharpe, 2017-2026 untouched\n")
    wf = []
    for (tag, bname, conv), sub in G.groupby(["universe", "book", "conv"], sort=False):
        pick = sub.loc[sub["IS_Sharpe"].idxmax()]
        anch = sub[(sub.f == 0.0) & (sub.sleeve == "S4")].iloc[0]
        base, spy = refs[tag]
        wf.append(dict(universe=tag, book=bname, conv=conv, sleeve_star=pick["sleeve"],
                       f_star=pick["f"], IS_Sharpe=pick["IS_Sharpe"],
                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                       OOS_MaxDD=pick["OOS_MaxDD"],
                       anchor_OOS_Sharpe=anch["OOS_Sharpe"], base_OOS_Sharpe=base["OOS_Sharpe"],
                       spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                       spy_OOS_MaxDD=spy["OOS_MaxDD"],
                       best_OOS=sub["OOS_Sharpe"].max(), regret=pick["OOS_Sharpe"] - sub["OOS_Sharpe"].max(),
                       full_4b=bool(pick["4b"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print(fmt(WF.set_index(["universe", "book", "conv"])))
    print(f"\nrule 8 picks TLTonly in {int((WF.sleeve_star == 'TLTonly').sum())}/{len(WF)} cells, "
          f"S4 in {int((WF.sleeve_star == 'S4').sum())}/{len(WF)}, "
          f"f=0 (no sleeve) in {int((WF.f_star == 0).sum())}/{len(WF)}; "
          f"mean regret {WF.regret.mean():+.3f}")
    print(f"OOS Sharpe of the rule-8 pick beats its no-sleeve anchor in "
          f"{int((WF.OOS_Sharpe > WF.anchor_OOS_Sharpe).sum())}/{len(WF)} cells, "
          f"beats SPY in {int((WF.OOS_Sharpe > WF.spy_OOS_Sharpe).sum())}/{len(WF)}, "
          f"beats RULES v1 in {int((WF.OOS_Sharpe > WF.base_OOS_Sharpe).sum())}/{len(WF)}")

    # per-variant walk-forward at f fixed to the pre-registered 0.50 (f not selected)
    print("\nRule-8 OOS at the pre-registered f=0.50, by variant (no selection at all):")
    sub = G[(G.f == F_STAR)].pivot_table(index=["universe", "book", "conv"], columns="sleeve",
                                         values="OOS_Sharpe")
    print(fmt(sub[["S4", "noTLT", "noGLD", "noDBC", "noUUP", "TLTonly"]]))

    # ---------------------------------------------------------- (6) census
    print("\n" + "=" * 118)
    print(f"### (6) CENSUS over all {len(G)} points: 4a {int(G['4a'].sum())}, 4b {int(G['4b'].sum())}")
    inner = G[(G.f > 0) & (G.f < 1)]
    print(f"Interior points: {len(inner)}, 4a {int(inner['4a'].sum())}, 4b {int(inner['4b'].sum())}")
    print(fmt(inner.groupby("sleeve")[["4a", "4b"]].sum().astype(int)))
    if int(inner["4b"].sum()):
        print("\nInterior points passing 4b:")
        print(fmt(inner[inner["4b"]].set_index(["universe", "book", "conv", "sleeve", "f"])[
            ["Gross", "Turn/yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "4a"]]))
        k = inner[inner["4b"]].groupby(["book", "conv", "sleeve", "f"]).size()
        print("\n(book, conv, sleeve, f) cells passing 4b on BOTH universes:")
        print(k[k == 2] if (k == 2).any() else "  none")

    # ---------------------------------------------------------- (7) cost ladder
    print("\n" + "=" * 118)
    print(f"### (7) COST LADDER at f={F_STAR:.2f}, book=top20 (control, exact by cost linearity)\n")
    ld = []
    for tag in universes:
        base, spy = refs[tag]
        for conv in ("natural", "g1.00"):
            for sname in SLEEVES:
                gr, to = cache[(tag, "top20", conv, sname, F_STAR)]
                for c in COST_LADDER:
                    row = full_row(net(gr, to, c))
                    ld.append(dict(universe=tag, conv=conv, sleeve=sname, cost_bps=c,
                                   CAGR=row["CAGR"], Sharpe=row["Sharpe"], MaxDD=row["MaxDD"],
                                   H1=row["H1"], H2=row["H2"], OOS_Sharpe=row["OOS_Sharpe"],
                                   **{"4b": keep_4b(row, spy)}))
    LD = pd.DataFrame(ld)
    LD.to_csv(OUT.with_suffix(".costladder.csv"), index=False)
    print(fmt(LD.pivot_table(index=["universe", "conv", "sleeve"], columns="cost_bps",
                             values=["Sharpe", "CAGR"])))
    print("\n4b passes on the ladder (count over universe x conv, max 4 per cell):")
    print(fmt(LD.pivot_table(index="sleeve", columns="cost_bps", values="4b", aggfunc="sum")))
    xu = LD.groupby(["conv", "sleeve", "cost_bps"])["4b"].sum()
    print("\n(conv, sleeve, cost) cells passing 4b on BOTH universes:")
    print(xu[xu == 2] if (xu == 2).any() else "  none")

    print(f"\nWritten: {OUT.name}.grid.csv / .standalone.csv / .correlation.csv / .deletion.csv "
          f"/ .regime.csv / .attribution.csv / .walkforward.csv / .costladder.csv")


if __name__ == "__main__":
    main()
