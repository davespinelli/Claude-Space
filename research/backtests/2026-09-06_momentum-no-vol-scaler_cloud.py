#!/usr/bin/env python3
"""Idea 29 - "momentum-no-vol-scaler" (cloud, 2026-09-06).

The queue's ask, verbatim
-------------------------
    29. momentum-no-vol-scaler - top-5 and top-10 by 12-1 momentum among eligible
        (no /sqrt(vol) term), 75% and 100% gross; report all; survivorship caveat.
        (Sep 3 IC finding)

RULES v1 ranks on a three-leg composite (12-1, 6m, 3m percentile ranks) DIVIDED by
sqrt(vol20).  Two things are bundled in that: the multi-horizon blend and the vol scaler.
This idea strips both at once - a single 12-1 momentum key, no scaler - so the run has to
separate them or it answers neither question.  It therefore prices FOUR keys on the same
eligible set, same gate, same gross, same cadence:

    M12_1        (px[t-21] / px[t-252] - 1)                    the queue's key
    M12_1_VS     the same key / vol20**0.5                     the scaler as an isolate
    COMP         the RULES v1 three-leg composite, NO scaler   the blend as an isolate
    COMP_VS      the RULES v1 composite WITH the scaler        the incumbent key

`M12_1 - M12_1_VS` and `COMP - COMP_VS` are then the vol-scaler effect measured twice, on
two different keys; `M12_1 - COMP` and `M12_1_VS - COMP_VS` are the blend effect measured
twice, at both scaler settings.  A conclusion that only survives one of the two readings is
reported as key-specific, not as a scaler result.

Gross convention (idea 81, binding)
-----------------------------------
Idea 81 established that the literal `GROSS/n` weight silently de-grosses whenever fewer
than n names are eligible, and that 16 of 21 literal 4b passes in the record die once the
book is gross-normalised.  Both conventions are therefore run for every point and the
REALISED mean gross is reported beside every row:

    LIT   w_i = GROSS / n                for the selected names (invested < GROSS if short)
    NORM  w_i = GROSS / (#selected)      constant realised gross (idea 240's convention)

Cost rungs (idea 260/261, binding)
----------------------------------
Every book is run ONCE at 0 bps and the other rungs are derived exactly as
`r(c) = r(0) - turnover * c / 1e4`, which is an identity of `engine.backtest` because
neither `held` nor `turnover` depends on c.  The identity is asserted against a live
10 bps `backtest()` call and the run aborts if it fails.  Rungs 0 / 10 / 25 are reported
for every point, and every KEY DIFFERENCE is published beside its 0-bps twin with the
share of the magnitude that is the two arms' turnover bill, per idea 261.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. n     in {5, 10}          (the queue names both; both reported)
    2. gross in {0.75, 1.00}     (the queue names both; both reported)
ALL FOUR grid points are reported at every panel, key, convention and rung - 4 x 4 x 2 x 3
x 3 panels = 288 points, plus controls, every one written to `.grid.csv`.  The KEY is the
hypothesis axis, not a tuned parameter; the cost rung is a reported axis.

Walk-forward (PROTOCOL rule 8), fixed with direction before any OOS number was read
    IS = 2009-01-01..2016-12-31 chooses, OOS = 2017-01-01..end evaluates, read once.
    M12_1_FIXED   n=5, gross=0.75, NORM          pre-registered, no selection at all
    M12_1_PICK    (n, gross) = argmax IS Sharpe within the M12_1 key
    ANY_PICK      (key, n, gross, conv) = argmax IS Sharpe over the whole grid
    COMP_VS_FIXED n=5, gross=0.75, NORM          the incumbent key, same treatment
    against RULES v1 OOS and SPY OOS on every panel.  Ideas 110/151/155/229 have found an
    IS chooser losing to doing nothing ten-plus times; M12_1_FIXED is the do-nothing arm
    that claim is tested against here.

Verdicts (both KEEP paths, every point, every rung)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP CAVEAT (the queue asks for it explicitly).  All three panels are CURRENT
constituents: universe.json and universe_broad.json are today's lists, and the small panel
(data/SMALL_PANEL_README.md) is today's sub-$2B screen carried back to 2010.  A momentum
book on a list of known survivors is flattered twice - the names that would have been
delisted are absent, and the ones that are present are disproportionately the ones whose
momentum kept working.  The bias runs TOWARD any momentum arm and hardest on the small
panel, so its levels are upper bounds; the key DIFFERENCES (scaler on/off, blend on/off)
are differences of two books drawn from the same biased list and are far less exposed.
Per instruction the small panel first drops every ticker with `max_1d_move >= 1.0` in
data/small_meta.csv (44 of 483).

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

RUNGS = [0, 10, 25]
PUB_RUNG = 10
NS = [5, 10]
GROSSES = [0.75, 1.00]
KEYS = ["M12_1", "M12_1_VS", "COMP", "COMP_VS"]
CONVS = ["LIT", "NORM"]
MAX_VOL = 0.60
FREQ = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)


def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxs = load_universe(small=True)
    keep = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[keep + ["SPY"]].dropna(how="all").ffill()
    return {"U56": (px56, set(px56.columns)),
            "B136": (px136, set(px136.columns)),
            "SMALL439": (pxs, set(keep))}, len(bad)


def keys_and_gate(px, tradable):
    """The four ranking keys plus the RULES v1 eligibility gate, all on one price panel."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    vs = vol20.clip(lower=0.08) ** 0.5
    k = {"M12_1": mom, "M12_1_VS": mom / vs, "COMP": comp, "COMP_VS": comp / vs}
    elig = above & (vol20 < MAX_VOL) & px.notna()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        elig[drop] = False
    return k, elig


def weights(key, elig, n, gross, conv):
    rank = key.where(elig).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    if conv == "LIT":
        return sel * (gross / n)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(gross).fillna(0.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pass4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail4b(r, spy):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    mo, mso = metrics(r.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not mo["Sharpe"] > mso["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def main():
    panels, n_dropped = build_panels()
    rows, series = [], {}

    print("=" * 200)
    print(f"Idea 29 momentum-no-vol-scaler | {SCRIPT} | weekly, next-day execution, rungs {RUNGS} bps")
    print(f"keys {KEYS} | n {NS} | gross {GROSSES} | conventions {CONVS} | "
          f"small panel dropped {n_dropped} tickers with max_1d_move>=1.0")
    print("=" * 200)

    for pname, (px, tradable) in panels.items():
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v1_weights(px), cost_bps=PUB_RUNG, freq=FREQ)["returns"].loc[start:]
        K, elig = keys_and_gate(px, tradable)
        nel = elig[::5].sum(axis=1)
        print(f"\n{pname}: {len(tradable)} tradable, {px.index[0].date()} -> {px.index[-1].date()}, "
              f"eval from {start.date()}, mean eligible {nel.mean():.1f} (p10 {nel.quantile(.10):.0f})")
        series[(pname, "__SPY__")] = spy
        series[(pname, "__BASE__")] = base

        checked = False
        for kname in KEYS:
            for n in NS:
                for g in GROSSES:
                    for conv in CONVS:
                        w = weights(K[kname], elig, n, g, conv)
                        res = backtest(px, w, cost_bps=0.0, freq=FREQ)
                        r0, turn = res["returns"], res["turnover"]
                        if not checked:
                            live = backtest(px, w, cost_bps=float(PUB_RUNG), freq=FREQ)["returns"]
                            err = float(np.max(np.abs((r0 - turn * PUB_RUNG / 1e4) - live)))
                            print(f"  harness identity |derived - live @{PUB_RUNG}bps| max = {err:.3e}")
                            if err > 1e-12:
                                print("!! cost identity failed - aborting."); sys.exit(1)
                            checked = True
                        gr = float(res["weights"].sum(axis=1).loc[start:].mean())
                        years = len(r0.loc[start:]) / 252
                        to_yr = float(turn.loc[start:].sum() / years)
                        for c in RUNGS:
                            r = (r0 - turn * c / 1e4).loc[start:]
                            m, mo = metrics(r), metrics(r.loc[OOS_START:])
                            h1, h2 = half_sharpes(r)
                            f4 = fail4b(r, spy)
                            series[(pname, kname, n, g, conv, c)] = r
                            rows.append(dict(panel=pname, key=kname, n=n, gross=g, conv=conv, cost=c,
                                             CAGR=m["CAGR"], Sharpe=m["Sharpe"], Vol=m["Vol"],
                                             MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                             IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                             OOS_MaxDD=mo["MaxDD"], TO=to_yr, gross_real=gr,
                                             p4a=pass4a(r, base), f4b=f4, p4b=(f4 == "-")))

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    print(f"\n[grid] {len(G)} points written to {STEM}.grid.csv - ALL reported below.")

    # ---------------- controls -------------------------------------------------
    print("\n--- controls (RULES v1 and SPY, per panel, at the published rung) " + "-" * 90)
    ctl = []
    for pname in G["panel"].unique():
        for lab, r in (("RULES v1", series[(pname, "__BASE__")]), ("SPY", series[(pname, "__SPY__")])):
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = half_sharpes(r)
            ctl.append(dict(panel=pname, arm=lab, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                            MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                            OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    C = pd.DataFrame(ctl)
    print(fmt(C.set_index(["panel", "arm"])))

    # ---------------- the queue's four points ----------------------------------
    print("\n--- THE QUEUE'S ASK: top-5 / top-10 by 12-1 momentum, 75% / 100% gross, ALL reported " + "-" * 30)
    q = G[(G.key == "M12_1")]
    print(fmt(q[["panel", "n", "gross", "conv", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "OOS_Sharpe", "TO", "gross_real", "p4a", "p4b", "f4b"]]
              .set_index(["panel", "n", "gross", "conv", "cost"])))

    print("\n--- full grid, every key x n x gross x convention x rung " + "-" * 95)
    print(fmt(G[["panel", "key", "n", "gross", "conv", "cost", "CAGR", "Sharpe", "MaxDD",
                 "H1", "H2", "OOS_Sharpe", "TO", "gross_real", "p4a", "p4b", "f4b"]]
              .set_index(["panel", "key", "n", "gross", "conv", "cost"])))

    # ---------------- the two isolates, with their 0-bps twins ------------------
    print("\n--- ISOLATES: vol scaler and multi-horizon blend, at the published rung and at 0 bps " + "-" * 30)
    idx = G.set_index(["panel", "key", "n", "gross", "conv", "cost"])
    iso_defs = [("SCALER on M12_1", "M12_1_VS", "M12_1"),
                ("SCALER on COMP", "COMP_VS", "COMP"),
                ("BLEND at no-scaler", "COMP", "M12_1"),
                ("BLEND at scaler", "COMP_VS", "M12_1_VS")]
    iso = []
    for lab, a, b in iso_defs:
        for pname in G["panel"].unique():
            for n in NS:
                for g in GROSSES:
                    for conv in CONVS:
                        try:
                            ra = {c: idx.loc[(pname, a, n, g, conv, c)] for c in RUNGS}
                            rb = {c: idx.loc[(pname, b, n, g, conv, c)] for c in RUNGS}
                        except KeyError:
                            continue
                        dS = {c: ra[c]["Sharpe"] - rb[c]["Sharpe"] for c in RUNGS}
                        dC = {c: ra[c]["CAGR"] - rb[c]["CAGR"] for c in RUNGS}
                        share = abs(dS[PUB_RUNG] - dS[0]) / abs(dS[PUB_RUNG]) if dS[PUB_RUNG] else np.nan
                        iso.append(dict(isolate=lab, panel=pname, n=n, gross=g, conv=conv,
                                        dSharpe_0=dS[0], dSharpe_10=dS[PUB_RUNG], dSharpe_25=dS[25],
                                        dCAGR_10=dC[PUB_RUNG], dCAGR_0=dC[0],
                                        dTO=float(ra[0]["TO"] - rb[0]["TO"]), cost_share=share,
                                        maj_cost=bool(np.isfinite(share) and share > 0.5),
                                        flip=bool(np.sign(dS[0]) != np.sign(dS[PUB_RUNG]))))
    I = pd.DataFrame(iso)
    I.to_csv(OUT / f"{STEM}.isolates.csv", index=False)
    print(fmt(I.set_index(["isolate", "panel", "n", "gross", "conv"]), 4))

    def tstat(x):
        x = np.asarray([v for v in x if np.isfinite(v)], float)
        if len(x) < 2:
            return np.nan
        se = x.std(ddof=1) / np.sqrt(len(x))
        return x.mean() / se if se > 0 else np.nan

    print("\nisolate summary (mean over the 12 (panel, n, gross, conv) cells, paired):")
    S = I.groupby("isolate").agg(n_cells=("dSharpe_10", "size"),
                                 dS10_mean=("dSharpe_10", "mean"),
                                 dS10_t=("dSharpe_10", tstat),
                                 dS10_pos=("dSharpe_10", lambda x: int((x > 0).sum())),
                                 dS0_mean=("dSharpe_0", "mean"),
                                 dS0_t=("dSharpe_0", tstat),
                                 dCAGR10_mean=("dCAGR_10", "mean"),
                                 dCAGR10_t=("dCAGR_10", tstat),
                                 dTO_mean=("dTO", "mean"),
                                 median_cost_share=("cost_share", "median"),
                                 majority_cost=("maj_cost", "sum"),
                                 sign_flips=("flip", "sum"))
    print(fmt(S, 4))

    # ---------------- rule 8 ---------------------------------------------------
    print("\n--- PROTOCOL rule 8 walk-forward (IS <= 2016-12-31 chooses, OOS >= 2017 evaluates) " + "-" * 40)
    w8 = []
    for pname in G["panel"].unique():
        sub = G[(G.panel == pname) & (G.cost == PUB_RUNG)]
        m12 = sub[sub.key == "M12_1"]
        sel = {"M12_1_FIXED": ("M12_1", 5, 0.75, "NORM"),
               "COMP_VS_FIXED": ("COMP_VS", 5, 0.75, "NORM")}
        bp = m12.loc[m12["IS_Sharpe"].idxmax()]
        sel["M12_1_PICK"] = (bp["key"], bp["n"], bp["gross"], bp["conv"])
        ap = sub.loc[sub["IS_Sharpe"].idxmax()]
        sel["ANY_PICK"] = (ap["key"], ap["n"], ap["gross"], ap["conv"])
        for lab, spec in sel.items():
            r = series[(pname, spec[0], int(spec[1]), float(spec[2]), spec[3], PUB_RUNG)]
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            w8.append(dict(panel=pname, selector=lab, arm=f"{spec[0]}/n{spec[1]}/g{spec[2]:.2f}/{spec[3]}",
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           p4a=pass4a(r, series[(pname, "__BASE__")]),
                           f4b=fail4b(r, series[(pname, "__SPY__")])))
        for lab, r in (("RULES v1", series[(pname, "__BASE__")]), ("SPY", series[(pname, "__SPY__")])):
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            w8.append(dict(panel=pname, selector=lab, arm="-", CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                           MaxDD=m["MaxDD"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                           OOS_MaxDD=mo["MaxDD"], p4a=np.nan, f4b="-"))
    W = pd.DataFrame(w8)
    W.to_csv(OUT / f"{STEM}.rule8.csv", index=False)
    print(fmt(W.set_index(["panel", "selector"])))
    print("\nOOS mean over panels:")
    print(fmt(W.groupby("selector")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean(), 4))
    pk = W[W.selector == "M12_1_PICK"].set_index("panel")["OOS_Sharpe"]
    fx = W[W.selector == "M12_1_FIXED"].set_index("panel")["OOS_Sharpe"]
    print(f"selection premium (M12_1_PICK - M12_1_FIXED) OOS Sharpe: {(pk - fx).mean():+.4f} mean, "
          f"per panel {dict((pk - fx).round(4))}")

    # ---------------- KEEP paths -----------------------------------------------
    print("\n--- KEEP paths (both, every point) " + "-" * 115)
    print(fmt(G.groupby(["panel", "cost"])[["p4a", "p4b"]].sum()
              .join(G.groupby(["panel", "cost"]).size().to_frame("n")), 0))
    print("\nby key at the published rung:")
    print(fmt(G[G.cost == PUB_RUNG].groupby(["key"])[["p4a", "p4b"]].sum()
              .join(G[G.cost == PUB_RUNG].groupby("key").size().to_frame("n")), 0))
    if G["p4b"].any():
        print("\nevery 4b pass:")
        print(fmt(G[G.p4b][["panel", "key", "n", "gross", "conv", "cost", "CAGR", "Sharpe",
                            "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_MaxDD", "TO", "gross_real"]]
                  .set_index(["panel", "key", "n", "gross", "conv", "cost"])))
    else:
        print("\n4b passes: NONE at any rung.")
    print("\nfailing bars at the published rung (which 4b bar binds):")
    fb = G[G.cost == PUB_RUNG]["f4b"].value_counts()
    print(fb.to_string())

    print("\n" + "=" * 200)
    print("SURVIVORSHIP CAVEAT: all three panels are CURRENT constituents (universe.json, "
          "universe_broad.json, and today's sub-$2B screen carried back to 2010). A momentum book "
          "on a survivor list is flattered twice - delisted names are absent, and the survivors are "
          "disproportionately names whose momentum kept working. Levels are UPPER BOUNDS, hardest on "
          "SMALL439; the scaler and blend ISOLATES are differences of two books drawn from the same "
          "biased list and are far less exposed.")
    print("=" * 200)


if __name__ == "__main__":
    main()
