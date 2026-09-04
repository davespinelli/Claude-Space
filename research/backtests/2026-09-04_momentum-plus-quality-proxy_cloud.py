#!/usr/bin/env python3
"""QUEUE idea 21 — momentum-plus-quality-proxy (cloud, 2026-09-04).

Question (pre-registered, from QUEUE)
------------------------------------
"Among top-10 momentum in broad universe, drop the 3 highest-vol names (vol as quality
proxy). Max 2 params."  i.e. does a short-horizon VOLATILITY screen applied INSIDE an
already-momentum-ranked, already-trend-gated book add anything?

Why this is worth a run even though the prior is bad
----------------------------------------------------
Idea 80/81 measured the sign of the short-horizon vol premium INSIDE the eligibility gate
and found it POSITIVE (Fama-MacBeth vol20 slope +0.0045, t +3.90 on universe.json; +0.0029,
t +3.19 on broad), and idea 1 killed RULES v1's `/sqrt(vol20)` scaler for exactly that
reason.  Idea 21 proposes the same tilt in a blunter form (a hard drop rather than a smooth
divisor).  The pre-registered prediction is therefore that it LOSES, and the informative
output is (a) how much, (b) whether the loss is a Sharpe loss or only a return loss, and
(c) whether the reversed screen — drop the LOWEST-vol names — wins, which is the sign check
that distinguishes "vol has no content here" from "the sign is backwards".

Book (fixed, not tuned; taken from the standing candidate construction)
-----------------------------------------------------------------------
Eligible  = RULES v1's gate, unchanged: price > 200d MA AND vol20 < 0.60.
Rank      = 12-1 momentum (px[t-21]/px[t-252] - 1), the "momentum" the queue item names.
            (A composite-ranked replicate is run as a robustness arm, ROBUST section.)
Select    = top K by momentum, then DROP D names by vol20.
Weights   = equal weight.  TWO gross conventions are reported for every arm because idea 73
            found `GROSS/K` silently de-grosses a book whenever fewer than K names are held,
            and the whole apparent premium of one published result was that artefact:
              MATCHED  w = g / count   (constant gross g; the honest comparison)
              LITERAL  w = g / K       (the naive one; the drop leaks into the gross lever)
Gross     = 0.75, weekly rebalance, long-only, next-day execution, 10 bps (25 bps also run).

Arms
    HI    drop the D HIGHEST-vol20 names of the top K      <- the idea under test
    LO    drop the D LOWEST-vol20 names of the top K       <- SIGN CHECK (control, not tuned)
    CTRL  no drop, but rank-cap at K-D (i.e. top (K-D) by momentum, same gross)
          <- the arm that answers "is the vol screen doing anything a smaller K does not?"
          This is the control idea 21 needs: HI must beat CTRL, not merely beat K, or the
          only content is holding fewer names.

Tuned parameters (PROTOCOL rule 4: at most two).  Exactly two:
    K in {10, 20, 30}                 candidate count before the screen
    d in {0.0, 0.1, 0.2, 0.3, 0.5}    drop FRACTION; D = round(d*K), so the queue's literal
                                      "top-10 drop 3" is (K=10, d=0.3).
All 15 (K,d) points are reported for every arm, universe, gross convention and cost — nothing
is selected for display.  Universes: universe_broad.json (136 names, PRIMARY — the queue item
says "broad universe") and universe.json (56 names, portability).

Walk-forward (PROTOCOL rule 8): parameters chosen on 2009-2016 by IS Sharpe within the HI arm
alone (the idea under test), evaluated untouched on 2017-2026 against RULES v1 and SPY.  The
same selection is run inside CTRL and LO so the OOS comparison is like-for-like.

KEEP paths: both 4a (beat RULES v1 in both halves, MaxDD no worse) and 4b (Sharpe > SPY in
both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) evaluated for every arm.

SURVIVORSHIP: universe.json and universe_broad.json are CURRENT-constituent lists, so every
absolute CAGR/Sharpe here is optimistic in one direction.  This run compares arms on the same
panel and the same days, so the HI-vs-CTRL delta — which is the result — is far less exposed
than the levels.  The bias does have a signed effect on this particular question: a current-
constituent panel over-represents names that survived, and the high-vol names that did NOT
survive are missing, which flatters the LO arm's real-world case and understates the case for
HI.  Read the sign check with that in mind.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-04_momentum-plus-quality-proxy_cloud"
FREQ, MAX_VOL, GROSS = "W", 0.60, 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
KS = [10, 20, 30]
DFRACS = [0.0, 0.1, 0.2, 0.3, 0.5]
COSTS = [10, 25]
PCOST = 10
ARMS = ["HI", "LO", "CTRL"]
CONVS = ["MATCHED", "LITERAL"]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)


# ---------------------------------------------------------------- signals
def signals(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    above = (px > px.rolling(200).mean()).fillna(False)
    elig = (above & (vol20 < MAX_VOL)).fillna(False)
    return mom, comp, vol20, elig


def weights(px, sig, vol20, elig, K, D, arm, conv, g=GROSS):
    """Top-K by `sig` among eligible, then drop D by vol20 (arm HI/LO) or rank-cap (CTRL)."""
    rank = sig.where(elig).rank(axis=1, ascending=False)
    if arm == "CTRL":
        sel = rank <= max(K - D, 1)
        denom_lit = max(K - D, 1)
    else:
        cand = rank <= K
        # rank the candidates by vol20; ascending=False -> 1 = highest vol
        vrank = vol20.where(cand).rank(axis=1, ascending=(arm == "LO"))
        sel = cand & ~(vrank <= D)
        denom_lit = K
    sel = sel.fillna(False)
    cnt = sel.sum(axis=1)
    if conv == "MATCHED":
        w = sel.astype(float).div(cnt.replace(0, np.nan), axis=0).fillna(0.0) * g
    else:
        w = sel.astype(float) * (g / denom_lit)
    return w


# ---------------------------------------------------------------- sim
def run(px, W, cost_bps):
    res = backtest(px, W, cost_bps=cost_bps, freq=FREQ)
    return res["returns"], res["turnover"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def eval4(r, bars, base):
    """(4b pass, failing-bar list, 4a pass) for a return series."""
    h1, h2 = halves(r)
    m = metrics(r)
    oos = metrics(r.loc[OOS_START:])["Sharpe"]
    f = []
    if not h1 > bars["s1"]: f.append("H1")
    if not h2 > bars["s2"]: f.append("H2")
    if not oos > bars["soos"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(bars["sdd"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * bars["scagr"]: f.append("CAGR")
    b1, b2 = halves(base)
    a = bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= metrics(base)["MaxDD"])
    return (not f), (",".join(f) if f else "-"), a


# ---------------------------------------------------------------- per universe
def run_universe(uname, px, out_rows):
    start = px.index[260]
    rows_per_yr = len(px) / ((px.index[-1] - px.index[0]).days / 365.25)
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = bars_of(spy)
    ms = metrics(spy)
    mom, comp, vol20, elig = signals(px)

    base_r = backtest(px, rules_v1_weights(px), cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
    mb = metrics(base_r); b1, b2 = halves(base_r)

    print("\n" + "=" * 210)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"INDEX SANITY: {rows_per_yr:.1f} rows/yr (must be ~252; the calendar-day bug of idea 38 gave ~365)"
          f"  -> {'OK trading-day index' if 240 < rows_per_yr < 260 else 'BAD — results unsafe'}")
    print(f"SPY   CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS {bars['soos']:.3f}")
    print(f"RULES v1 @10bps  CAGR {mb['CAGR']:.2%}  Sharpe {mb['Sharpe']:.3f}  MaxDD {mb['MaxDD']:.2%}  "
          f"halves {b1:.3f}/{b2:.3f}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f}(H1) / {bars['s2']:.3f}(H2) / {bars['soos']:.3f}(OOS), "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    print(f"mean eligible names E_t = {elig.loc[start:].sum(axis=1).mean():.1f}")
    print("=" * 210)

    rows = []
    for conv in CONVS:
        for K in KS:
            for d in DFRACS:
                D = int(round(d * K))
                for arm in ARMS:
                    if D == 0 and arm != "HI":
                        continue                       # d=0: all three arms are identical
                    W = weights(px, mom, vol20, elig, K, D, arm, conv)
                    nheld = (W > 0).sum(axis=1).loc[start:]
                    for c in COSTS:
                        r, to = run(px, W, c)
                        r = r.loc[start:]
                        m = metrics(r); h1, h2 = halves(r)
                        oos = metrics(r.loc[OOS_START:])
                        p4b, fails, p4a = eval4(r, bars, base_r)
                        rows.append(dict(uni=uname, conv=conv, K=K, d=d, D=D, arm=arm, bps=c,
                                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                         H1=h1, H2=h2, oCAGR=oos["CAGR"], oSharpe=oos["Sharpe"],
                                         oMaxDD=oos["MaxDD"],
                                         held=nheld.mean(), gross=W.loc[start:].sum(axis=1).mean(),
                                         turn=to.loc[start:].sum() / metrics(r)["Years"],
                                         p4a=p4a, p4b=p4b, fails=fails))
    df = pd.DataFrame(rows)
    out_rows.append(df)

    for conv in CONVS:
        for c in COSTS:
            sub = df[(df.conv == conv) & (df.bps == c)].copy()
            print(f"\n--- {uname} | gross convention {conv} | {c} bps | ALL grid points ---")
            show = sub[["K", "d", "D", "arm", "held", "gross", "turn", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "oSharpe", "oCAGR", "oMaxDD", "p4a", "p4b", "fails"]]
            print(show.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- the test the queue item actually poses: HI vs CTRL at matched gross and matched size
    print(f"\n--- {uname} | HI minus CTRL (MATCHED gross, {PCOST} bps) — 'does the vol screen "
          f"beat simply holding K-D names?' ---")
    m10 = df[(df.conv == "MATCHED") & (df.bps == PCOST)]
    cmp_rows = []
    for K in KS:
        for d in DFRACS:
            if d == 0:
                continue
            hi = m10[(m10.K == K) & (m10.d == d) & (m10.arm == "HI")].iloc[0]
            ct = m10[(m10.K == K) & (m10.d == d) & (m10.arm == "CTRL")].iloc[0]
            lo = m10[(m10.K == K) & (m10.d == d) & (m10.arm == "LO")].iloc[0]
            cmp_rows.append(dict(K=K, d=d, D=hi.D,
                                 dS_HI_CTRL=hi.Sharpe - ct.Sharpe, dC_HI_CTRL=hi.CAGR - ct.CAGR,
                                 dS_LO_CTRL=lo.Sharpe - ct.Sharpe, dC_LO_CTRL=lo.CAGR - ct.CAGR,
                                 dS_HI_LO=hi.Sharpe - lo.Sharpe, dC_HI_LO=hi.CAGR - lo.CAGR))
    cdf = pd.DataFrame(cmp_rows)
    print(cdf.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    print(f"HI beats CTRL on Sharpe in {int((cdf.dS_HI_CTRL > 0).sum())}/{len(cdf)} cells "
          f"(mean {cdf.dS_HI_CTRL.mean():+.4f}); "
          f"LO beats CTRL in {int((cdf.dS_LO_CTRL > 0).sum())}/{len(cdf)} (mean {cdf.dS_LO_CTRL.mean():+.4f}); "
          f"HI beats LO in {int((cdf.dS_HI_LO > 0).sum())}/{len(cdf)} (mean {cdf.dS_HI_LO.mean():+.4f}).")

    # ---- walk-forward, rule 8
    print(f"\n--- {uname} | WALK-FORWARD (rule 8): params chosen on IS <= {IS_END} inside arm HI, "
          f"MATCHED gross, {PCOST} bps; evaluated on OOS >= {OOS_START} ---")
    is_rows = []
    for K in KS:
        for d in DFRACS:
            D = int(round(d * K))
            W = weights(px, mom, vol20, elig, K, D, "HI", "MATCHED")
            r = run(px, W, PCOST)[0].loc[start:IS_END]
            is_rows.append(dict(K=K, d=d, D=D, isSharpe=metrics(r)["Sharpe"],
                                isCAGR=metrics(r)["CAGR"], isMaxDD=metrics(r)["MaxDD"]))
    isdf = pd.DataFrame(is_rows).sort_values("isSharpe", ascending=False)
    print(isdf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    pick = isdf.iloc[0]
    K8, d8, D8 = int(pick.K), float(pick.d), int(pick.D)
    print(f"IS pick (argmax IS Sharpe; ties -> larger K then smaller d): K={K8} d={d8} D={D8}"
          f"  | IS Sharpe spread over the 15-point grid = {isdf.isSharpe.max()-isdf.isSharpe.min():.3f}")

    oos_rows = []
    spy_o = spy.loc[OOS_START:]
    base_o = base_r.loc[OOS_START:]
    for arm in ARMS:
        Du = D8 if arm != "CTRL" else D8
        W = weights(px, mom, vol20, elig, K8, Du, arm, "MATCHED")
        r = run(px, W, PCOST)[0].loc[start:]
        ro = r.loc[OOS_START:]
        mo = metrics(ro)
        oos_rows.append(dict(what=f"idea21 {arm} K={K8} d={d8}", CAGR=mo["CAGR"],
                             Sharpe=mo["Sharpe"], MaxDD=mo["MaxDD"]))
    for nm, s in (("RULES v1 baseline", base_o), ("SPY", spy_o)):
        mo = metrics(s)
        oos_rows.append(dict(what=nm, CAGR=mo["CAGR"], Sharpe=mo["Sharpe"], MaxDD=mo["MaxDD"]))
    odf = pd.DataFrame(oos_rows).set_index("what")
    print(odf.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- robustness: same test with the v1 COMPOSITE as the ranker instead of raw 12-1
    print(f"\n--- {uname} | ROBUSTNESS: ranker = v1 composite (no vol scaler) instead of raw 12-1 "
          f"momentum, MATCHED gross, {PCOST} bps ---")
    rob = []
    for K in KS:
        for d in DFRACS:
            D = int(round(d * K))
            for arm in ARMS:
                if D == 0 and arm != "HI":
                    continue
                W = weights(px, comp, vol20, elig, K, D, arm, "MATCHED")
                r = run(px, W, PCOST)[0].loc[start:]
                m = metrics(r); h1, h2 = halves(r)
                p4b, fails, p4a = eval4(r, bars, base_r)
                rob.append(dict(K=K, d=d, D=D, arm=arm, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                MaxDD=m["MaxDD"], H1=h1, H2=h2, p4a=p4a, p4b=p4b, fails=fails))
    rdf = pd.DataFrame(rob)
    print(rdf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return df, cdf, (K8, d8, D8), odf


def main():
    out = []
    res = {}
    for uname, px in (("universe_broad.json (136, PRIMARY)", load_universe(broad=True)),
                      ("universe.json (56)", load_universe())):
        res[uname] = run_universe(uname, px, out)
    allrows = pd.concat(out, ignore_index=True)
    allrows.to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)

    print("\n" + "=" * 210)
    print("SUMMARY — idea 21 momentum-plus-quality-proxy")
    print("=" * 210)
    print(f"Total reported grid points: {len(allrows)} "
          f"(2 universes x 2 gross conventions x 2 costs x {len(KS)} K x arms)")
    for uname in res:
        df, cdf, pick, odf = res[uname]
        m10 = df[(df.conv == "MATCHED") & (df.bps == PCOST)]
        print(f"\n{uname}")
        print(f"  4b passes: {int(m10.p4b.sum())}/{len(m10)} at MATCHED/{PCOST}bps; "
              f"4a passes: {int(m10.p4a.sum())}/{len(m10)}")
        print(f"  HI-vs-CTRL mean dSharpe {cdf.dS_HI_CTRL.mean():+.4f} "
              f"({int((cdf.dS_HI_CTRL>0).sum())}/{len(cdf)} positive); "
              f"HI-vs-LO mean dSharpe {cdf.dS_HI_LO.mean():+.4f} "
              f"({int((cdf.dS_HI_LO>0).sum())}/{len(cdf)} positive)")
        print(f"  rule-8 pick K={pick[0]} d={pick[1]}; OOS table above")
    print("\nWritten:", ROOT / "research" / "backtests" / f"{STEM}.grid.csv")


if __name__ == "__main__":
    main()
