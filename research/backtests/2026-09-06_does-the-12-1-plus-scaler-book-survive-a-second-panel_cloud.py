#!/usr/bin/env python3
"""Idea 264 - "does-the-12-1-plus-scaler-book-survive-a-second-panel" (cloud, 2026-09-06).

The queue's ask, verbatim
-------------------------
    264. does-the-12-1-plus-scaler-book-survive-a-second-panel - idea 29 PARKed
        `U56 / M12_1_VS / n=10 / g=0.75 / NORM` (12-1 momentum with the /sqrt(vol)
        scaler): 14.9%/1.058/-19.4%, halves 1.044/1.080, OOS 1.106, clears 4b at 0 and
        10 bps on U56 but fails at 25 bps on H1 and on B136 by 0.86pp of drawdown and on
        SMALL439 outright. Idea 29 also found the 3-leg blend is a strict -0.12 Sharpe /
        -3.8 pp CAGR negative against the 12-1 leg alone in 24/24 cells, so this arm is
        the incumbent key with its worst leg deleted. Put it through idea 72's
        cross-universe bar (2 panels x 3 cadences x 2 conventions x 3 rungs) and idea
        65's cadence-insensitivity bar before it is anything; report the 0-bps twin
        beside every difference per idea 261. Max 2 params. (2026-09-06)

What is actually new here
-------------------------
Idea 29 priced this arm at ONE cadence (weekly).  Its panel axis is therefore already
published and is NOT the open question; the open axis is CADENCE, because idea 65 proposed
cadence-insensitivity as a pre-registered robustness bar and idea 3 found the cadence dial
moves 4b verdicts (ew-band3 dSharpe -0.03..+0.00 across D/W/M, top20 +0.11, RULES v1 +0.30).
This run therefore re-prices the PARKED POINT on the full cross-universe bar:

    3 panels (U56, B136, SMALL439) x 3 cadences (D, W, M) x 2 conventions (LIT, NORM)
    x 3 cost rungs (0, 10, 25 bps)

and reports the panel axis alongside so the two failures the queue already names (B136
drawdown, 25 bps H1) are re-derived rather than assumed.

The no-scaler twin `M12_1` is carried through every cell as the scaler ISOLATE, so the
cadence reading is available both with and without the term the arm is named for.

PRE-REGISTERED POINT (fixed before any number was read, no selection):
    key M12_1_VS, n=10, gross=0.75, conv NORM, cadence W  -- exactly idea 29's parked arm.

Gross convention (idea 81, binding)
-----------------------------------
    LIT   w_i = GROSS / n            (silently de-grosses when fewer than n are eligible)
    NORM  w_i = GROSS / #selected    (constant realised gross)
Realised mean gross is reported beside every row.

Cost rungs (idea 260/261, binding)
----------------------------------
Every book is run ONCE at 0 bps and the other rungs are derived exactly as
`r(c) = r(0) - turnover * c / 1e4`, an identity of `engine.backtest` because neither
`held` nor `turnover` depends on c.  The identity is asserted against a live 10 bps
`backtest()` call and the run aborts if it fails.  EVERY difference below is published
beside its 0-bps twin with the share of its magnitude that is the two arms' turnover bill.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. n     in {5, 10}
    2. gross in {0.75, 1.00}
ALL grid points are reported (3 panels x 2 keys x 3 cadences x 2 conventions x 2 n x
2 gross x 3 rungs = 432 rows, written to `.grid.csv`).  Cadence, convention, panel and
cost rung are REPORTED axes, not tuned parameters: nothing is picked on them.

Walk-forward (PROTOCOL rule 8), fixed with direction before any OOS number was read
    IS = start..2016-12-31 chooses, OOS = 2017-01-01..end evaluates, read once.
    PARKED_FIXED  the pre-registered point above           (the do-nothing arm)
    CADENCE_PICK  cadence = argmax IS Sharpe, arm otherwise fixed
    ARM_PICK      (n, gross, conv, cadence) = argmax IS Sharpe within M12_1_VS
    ANY_PICK      the same argmax over both keys
    against RULES v1 OOS and SPY OOS on every panel.

Verdicts (both KEEP paths, every point, every rung)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.
The RULES v1 baseline is run at its LIVE cadence (weekly) against every cadence of the
idea, because 4a is a comparison against the live book, not against a re-cadenced twin.

SURVIVORSHIP CAVEAT.  All three panels are CURRENT constituents: universe.json and
universe_broad.json are today's lists, and the small panel (data/SMALL_PANEL_README.md)
is today's sub-$2B screen carried back to 2010.  A momentum book on a survivor list is
flattered twice - the names that would have been delisted are absent, and the survivors
are disproportionately the ones whose momentum kept working.  The bias runs TOWARD every
arm here and hardest on SMALL439, so all LEVELS (and therefore every 4b pass) are upper
bounds.  The cadence and scaler DIFFERENCES are differences of two books drawn from the
same biased list and are far less exposed.  Per instruction the small panel first drops
every ticker with `max_1d_move >= 1.0` in data/small_meta.csv.

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v1_weights
from engine import backtest, metrics

RUNGS = [0, 10, 25]
PUB_RUNG = 10
NS = [5, 10]
GROSSES = [0.75, 1.00]
KEYS = ["M12_1_VS", "M12_1"]
CONVS = ["LIT", "NORM"]
CADENCES = ["D", "W", "M"]
MAX_VOL = 0.60
BASE_FREQ = "W"                      # the live book's cadence
PARKED = ("M12_1_VS", 10, 0.75, "NORM", "W")
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 1000)


def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxs = load_universe(small=True)
    keep = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[keep + ["SPY"]].dropna(how="all").ffill()
    return {"U56": (px56, set(px56.columns) - {"SPY"} | {"SPY"}),
            "B136": (px136, set(px136.columns)),
            "SMALL439": (pxs, set(keep))}, len(bad)


def keys_and_gate(px, tradable):
    """The 12-1 key with and without the /sqrt(vol20) scaler, plus the RULES v1 gate."""
    mom = px.shift(21) / px.shift(252) - 1
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    vs = vol20.clip(lower=0.08) ** 0.5
    k = {"M12_1": mom, "M12_1_VS": mom / vs}
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


def margins4b(r, spy):
    """Signed slack on each 4b bar (positive = passing), in Sharpe units / pp."""
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    mo, mso = metrics(r.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
    return dict(mH1=h1 - s1, mH2=h2 - s2, mOOS=mo["Sharpe"] - mso["Sharpe"],
                mDD_pp=100 * (0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"])),
                mCAGR_pp=100 * (m["CAGR"] - 0.70 * ms["CAGR"]))


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 2:
        return np.nan
    se = x.std(ddof=1) / np.sqrt(len(x))
    return x.mean() / se if se > 0 else np.nan


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def main():
    panels, n_dropped = build_panels()
    rows, series = [], {}

    print("=" * 210)
    print(f"Idea 264 does-the-12-1-plus-scaler-book-survive-a-second-panel | {SCRIPT}")
    print(f"pre-registered parked point: key={PARKED[0]} n={PARKED[1]} gross={PARKED[2]} "
          f"conv={PARKED[3]} cadence={PARKED[4]} | next-day execution, rungs {RUNGS} bps")
    print(f"panels U56/B136/SMALL439 x cadences {CADENCES} x conventions {CONVS} x keys {KEYS} "
          f"x n {NS} x gross {GROSSES} | small panel dropped {n_dropped} tickers with max_1d_move>=1.0")
    print("=" * 210)

    for pname, (px, tradable) in panels.items():
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v1_weights(px), cost_bps=PUB_RUNG, freq=BASE_FREQ)["returns"].loc[start:]
        K, elig = keys_and_gate(px, tradable)
        nel = elig[::5].sum(axis=1)
        print(f"\n{pname}: {len([t for t in tradable if t != 'SPY'])} tradable, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}, "
              f"mean eligible {nel.mean():.1f} (p10 {nel.quantile(.10):.0f})", flush=True)
        series[(pname, "__SPY__")] = spy
        series[(pname, "__BASE__")] = base

        checked = False
        for kname in KEYS:
            for cad in CADENCES:
                for n in NS:
                    for g in GROSSES:
                        for conv in CONVS:
                            w = weights(K[kname], elig, n, g, conv)
                            res = backtest(px, w, cost_bps=0.0, freq=cad)
                            r0, turn = res["returns"], res["turnover"]
                            if not checked:
                                live = backtest(px, w, cost_bps=float(PUB_RUNG), freq=cad)["returns"]
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
                                series[(pname, kname, cad, n, g, conv, c)] = r
                                rows.append(dict(panel=pname, key=kname, cad=cad, n=n, gross=g,
                                                 conv=conv, cost=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                                 Vol=m["Vol"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                                 IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                                 OOS_MaxDD=mo["MaxDD"], TO=to_yr, gross_real=gr,
                                                 p4a=pass4a(r, base), f4b=f4, p4b=(f4 == "-"),
                                                 **margins4b(r, spy)))
            print(f"  {kname}: {len(CADENCES) * len(NS) * len(GROSSES) * len(CONVS)} books priced", flush=True)

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    print(f"\n[grid] {len(G)} points written to {STEM}.grid.csv - ALL reported below.")

    # ---------------- controls -------------------------------------------------
    print("\n--- controls (RULES v1 weekly @10bps, and SPY, per panel) " + "-" * 100)
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

    # ---------------- the parked point on the cross-universe bar ---------------
    kp, npk, gpk, cvpk, cadpk = PARKED
    P = G[(G.key == kp) & (G.n == npk) & (G.gross == gpk)]
    print("\n--- THE PARKED ARM on idea 72's cross-universe bar: 3 panels x 3 cadences x 2 conv x 3 rungs "
          + "-" * 20)
    print(fmt(P[["panel", "cad", "conv", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "OOS_Sharpe", "TO", "gross_real", "p4a", "p4b", "f4b"]]
              .set_index(["panel", "cad", "conv", "cost"])))
    print("\n4b bar margins for the same cells (positive = passing; DD/CAGR in pp):")
    print(fmt(P[["panel", "cad", "conv", "cost", "mH1", "mH2", "mOOS", "mDD_pp", "mCAGR_pp", "f4b"]]
              .set_index(["panel", "cad", "conv", "cost"]), 4))
    print("\n4b pass counts for the parked arm, by panel x rung (of 6 cadence x convention cells):")
    print(fmt(P.groupby(["panel", "cost"])[["p4a", "p4b"]].sum()
              .join(P.groupby(["panel", "cost"]).size().to_frame("cells")), 0))

    print(f"\nthe single pre-registered cell ({kp}/n{npk}/g{gpk}/{cvpk}/{cadpk}), all panels and rungs:")
    one = P[(P.conv == cvpk) & (P.cad == cadpk)]
    print(fmt(one[["panel", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
                   "OOS_MaxDD", "TO", "gross_real", "p4a", "p4b", "f4b"]].set_index(["panel", "cost"])))

    # ---------------- idea 65's cadence-insensitivity bar ----------------------
    print("\n--- idea 65's CADENCE-INSENSITIVITY bar (spread of Sharpe across D/W/M, one row per book) "
          + "-" * 25)
    cad_rows = []
    grp = G.groupby(["panel", "key", "n", "gross", "conv", "cost"])
    for kk, sub in grp:
        s = sub.set_index("cad")
        if not set(CADENCES) <= set(s.index):
            continue
        sh = s.loc[CADENCES, "Sharpe"]
        cg = s.loc[CADENCES, "CAGR"]
        dd = s.loc[CADENCES, "MaxDD"]
        p4 = s.loc[CADENCES, "p4b"]
        cad_rows.append(dict(panel=kk[0], key=kk[1], n=kk[2], gross=kk[3], conv=kk[4], cost=kk[5],
                             S_D=sh["D"], S_W=sh["W"], S_M=sh["M"],
                             dS_MW=sh["M"] - sh["W"], dS_DW=sh["D"] - sh["W"],
                             spread=float(sh.max() - sh.min()),
                             dCAGR_MW=cg["M"] - cg["W"], dDD_MW=dd["M"] - dd["W"],
                             n4b=int(p4.sum()), stable4b=bool(p4.nunique() == 1)))
    CD = pd.DataFrame(cad_rows)
    CD.to_csv(OUT / f"{STEM}.cadence.csv", index=False)
    print(fmt(CD.set_index(["panel", "key", "n", "gross", "conv", "cost"]), 4))
    print("\ncadence-insensitivity summary (mean |spread| and 4b stability), by key x panel x rung:")
    print(fmt(CD.groupby(["key", "panel", "cost"]).agg(
        mean_spread=("spread", "mean"), max_spread=("spread", "max"),
        mean_dS_MW=("dS_MW", "mean"), mean_dS_DW=("dS_DW", "mean"),
        cells=("spread", "size"), stable4b=("stable4b", "sum"), any4b=("n4b", lambda x: int((x > 0).sum()))), 4))
    pk_cd = CD[(CD.key == kp) & (CD.n == npk) & (CD.gross == gpk) & (CD.conv == cvpk)]
    print(f"\nthe parked arm's own cadence row ({kp}/n{npk}/g{gpk}/{cvpk}):")
    print(fmt(pk_cd.set_index(["panel", "cost"])[["S_D", "S_W", "S_M", "dS_MW", "dS_DW", "spread",
                                                  "dCAGR_MW", "dDD_MW", "n4b", "stable4b"]], 4))
    print("\nidea 3's reference band: ew-band3 passed cadence-insensitivity at dSharpe -0.03..+0.00; "
          "top20 swung +0.11 and RULES v1 +0.30 (both judged cadence-SENSITIVE).")

    # ---------------- differences with their 0-bps twins (idea 261) ------------
    print("\n--- every difference beside its 0-bps twin (idea 261) " + "-" * 100)
    idx = G.set_index(["panel", "key", "cad", "n", "gross", "conv", "cost"])
    diffs = []
    def add(lab, a, b):
        try:
            ra = {c: idx.loc[a + (c,)] for c in RUNGS}
            rb = {c: idx.loc[b + (c,)] for c in RUNGS}
        except KeyError:
            return
        dS = {c: ra[c]["Sharpe"] - rb[c]["Sharpe"] for c in RUNGS}
        share = abs(dS[PUB_RUNG] - dS[0]) / abs(dS[PUB_RUNG]) if dS[PUB_RUNG] else np.nan
        diffs.append(dict(difference=lab, panel=a[0], key=a[1], n=a[3], gross=a[4], conv=a[5],
                          dSharpe_0=dS[0], dSharpe_10=dS[PUB_RUNG], dSharpe_25=dS[25],
                          dCAGR_10=ra[PUB_RUNG]["CAGR"] - rb[PUB_RUNG]["CAGR"],
                          dCAGR_0=ra[0]["CAGR"] - rb[0]["CAGR"],
                          dTO=float(ra[0]["TO"] - rb[0]["TO"]),
                          TO_ratio=float(ra[0]["TO"] / rb[0]["TO"]) if rb[0]["TO"] else np.nan,
                          cost_share=share, maj_cost=bool(np.isfinite(share) and share > 0.5),
                          flip=bool(np.sign(dS[0]) != np.sign(dS[PUB_RUNG]))))

    for pname in G["panel"].unique():
        for n in NS:
            for g in GROSSES:
                for conv in CONVS:
                    for kname in KEYS:
                        add("CADENCE M vs W", (pname, kname, "M", n, g, conv), (pname, kname, "W", n, g, conv))
                        add("CADENCE D vs W", (pname, kname, "D", n, g, conv), (pname, kname, "W", n, g, conv))
                    for cad in CADENCES:
                        add("SCALER (VS vs plain)", (pname, "M12_1_VS", cad, n, g, conv),
                            (pname, "M12_1", cad, n, g, conv))
    D = pd.DataFrame(diffs)
    D.to_csv(OUT / f"{STEM}.diffs.csv", index=False)
    print(fmt(D.groupby("difference").agg(
        cells=("dSharpe_10", "size"), dS10_mean=("dSharpe_10", "mean"), dS10_t=("dSharpe_10", tstat),
        dS10_pos=("dSharpe_10", lambda x: int((x > 0).sum())),
        dS0_mean=("dSharpe_0", "mean"), dS0_t=("dSharpe_0", tstat),
        dCAGR10_mean=("dCAGR_10", "mean"), dTO_mean=("dTO", "mean"),
        median_TO_ratio=("TO_ratio", "median"), median_cost_share=("cost_share", "median"),
        majority_cost=("maj_cost", "sum"), sign_flips=("flip", "sum")), 4))
    print("\nper-panel breakdown of the same differences:")
    print(fmt(D.groupby(["difference", "panel"]).agg(
        cells=("dSharpe_10", "size"), dS0_mean=("dSharpe_0", "mean"),
        dS10_mean=("dSharpe_10", "mean"), dS25_mean=("dSharpe_25", "mean"),
        dCAGR10_mean=("dCAGR_10", "mean"), dTO_mean=("dTO", "mean")), 4))

    # ---------------- full grid ------------------------------------------------
    print("\n--- FULL GRID, every panel x key x cadence x n x gross x convention x rung " + "-" * 60)
    print(fmt(G[["panel", "key", "cad", "n", "gross", "conv", "cost", "CAGR", "Sharpe", "MaxDD",
                 "H1", "H2", "OOS_Sharpe", "TO", "gross_real", "p4a", "p4b", "f4b"]]
              .set_index(["panel", "key", "cad", "n", "gross", "conv", "cost"])))

    # ---------------- rule 8 ---------------------------------------------------
    print("\n--- PROTOCOL rule 8 walk-forward (IS <= 2016-12-31 chooses, OOS >= 2017 evaluates) " + "-" * 50)
    w8 = []
    for pname in G["panel"].unique():
        sub = G[(G.panel == pname) & (G.cost == PUB_RUNG)]
        sel = {"PARKED_FIXED": (kp, cadpk, npk, gpk, cvpk)}
        cadsub = sub[(sub.key == kp) & (sub.n == npk) & (sub.gross == gpk) & (sub.conv == cvpk)]
        cp = cadsub.loc[cadsub["IS_Sharpe"].idxmax()]
        sel["CADENCE_PICK"] = (cp["key"], cp["cad"], cp["n"], cp["gross"], cp["conv"])
        arm = sub[sub.key == kp]
        ap = arm.loc[arm["IS_Sharpe"].idxmax()]
        sel["ARM_PICK"] = (ap["key"], ap["cad"], ap["n"], ap["gross"], ap["conv"])
        yp = sub.loc[sub["IS_Sharpe"].idxmax()]
        sel["ANY_PICK"] = (yp["key"], yp["cad"], yp["n"], yp["gross"], yp["conv"])
        for lab, spec in sel.items():
            r = series[(pname, spec[0], spec[1], int(spec[2]), float(spec[3]), spec[4], PUB_RUNG)]
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            mg = margins4b(r, series[(pname, "__SPY__")])
            w8.append(dict(panel=pname, selector=lab,
                           arm=f"{spec[0]}/{spec[1]}/n{spec[2]}/g{float(spec[3]):.2f}/{spec[4]}",
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           p4a=pass4a(r, series[(pname, "__BASE__")]),
                           f4b=fail4b(r, series[(pname, "__SPY__")]), mOOS=mg["mOOS"]))
        for lab, r in (("RULES v1", series[(pname, "__BASE__")]), ("SPY", series[(pname, "__SPY__")])):
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            w8.append(dict(panel=pname, selector=lab, arm="-", CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                           MaxDD=m["MaxDD"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                           OOS_MaxDD=mo["MaxDD"], p4a=np.nan, f4b="-", mOOS=np.nan))
    W = pd.DataFrame(w8)
    W.to_csv(OUT / f"{STEM}.rule8.csv", index=False)
    print(fmt(W.set_index(["panel", "selector"])))
    print("\nOOS mean over panels:")
    print(fmt(W.groupby("selector")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean(), 4))
    for lab in ("CADENCE_PICK", "ARM_PICK", "ANY_PICK"):
        a = W[W.selector == lab].set_index("panel")["OOS_Sharpe"]
        b = W[W.selector == "PARKED_FIXED"].set_index("panel")["OOS_Sharpe"]
        print(f"selection premium ({lab} - PARKED_FIXED) OOS Sharpe: {(a - b).mean():+.4f} mean, "
              f"per panel {dict((a - b).round(4))}")

    # ---------------- KEEP paths -----------------------------------------------
    print("\n--- KEEP paths (both, every point) " + "-" * 120)
    print(fmt(G.groupby(["panel", "cost"])[["p4a", "p4b"]].sum()
              .join(G.groupby(["panel", "cost"]).size().to_frame("n")), 0))
    print("\nby key x cadence at the published rung:")
    sub = G[G.cost == PUB_RUNG]
    print(fmt(sub.groupby(["key", "cad"])[["p4a", "p4b"]].sum()
              .join(sub.groupby(["key", "cad"]).size().to_frame("n")), 0))
    if G["p4b"].any():
        print("\nevery 4b pass in the grid:")
        print(fmt(G[G.p4b][["panel", "key", "cad", "n", "gross", "conv", "cost", "CAGR", "Sharpe",
                            "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_MaxDD", "TO", "gross_real"]]
                  .set_index(["panel", "key", "cad", "n", "gross", "conv", "cost"])))
    else:
        print("\n4b passes: NONE at any rung.")
    print("\nfailing 4b bars at the published rung:")
    print(G[G.cost == PUB_RUNG]["f4b"].value_counts().to_string())
    print("\nfailing 4b bars for the parked arm only, all rungs:")
    print(P["f4b"].value_counts().to_string())

    print("\n" + "=" * 210)
    print("SURVIVORSHIP CAVEAT: all three panels are CURRENT constituents (universe.json, "
          "universe_broad.json, and today's sub-$2B screen carried back to 2010). A momentum book on a "
          "survivor list is flattered twice - delisted names are absent, and the survivors are "
          "disproportionately names whose momentum kept working. LEVELS (and every 4b pass) are UPPER "
          "BOUNDS, hardest on SMALL439; the cadence and scaler DIFFERENCES are differences of two books "
          "drawn from the same biased list and are far less exposed.")
    print("=" * 210)


if __name__ == "__main__":
    main()
