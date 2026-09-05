#!/usr/bin/env python3
"""QUEUE idea 101 — fixed-gross-S4-blend (cloud, 2026-09-05), with queue idea 104
(fold-drop-DBC-into-101) folded in as its pre-registered SECOND ARM.

Question (as worded in QUEUE.md)
--------------------------------
101: "idea 100's `top20 + 50% S4 at g=1.00` clears 4b on BOTH universes (11.8%/1.149/-14.2%
and 12.2%/1.063/-15.6%) but the exposure target was a diagnostic, not a pre-registered
parameter, and the arm was never cost-laddered.  Re-run it with g FIXED at 1.00 ex ante, the
full 5/10/15/20/25 bps ladder, and idea 65's cadence-insensitivity bar (D/W/M).  Max 2 params
(f, cost).  Blocks adoption."

104: "...Add [`top20 + 50% sleeve(TLT,GLD,UUP)` at g=1.00] as a SECOND pre-registered arm of
idea 101's fixed-g run rather than opening a third study; same cost ladder, same cadence bar."

What is being fixed ex ante (NOT selected on any statistic in this run)
----------------------------------------------------------------------
  g = 1.00                the gross convention.  Fully invested, no leverage.  Declared here
                          before any number is computed; the natural-gross convention is run
                          ONLY as a reported control and is never eligible for the verdict.
  book = top20            idea 2's standing 4b KEEP: equal-weight the top 20 eligible names by
                          the unscaled composite, gross-normalised to g.
  sleeve arms             S4 = {TLT,GLD,DBC,UUP} (idea 100) and S3 = {TLT,GLD,UUP} (idea 104).
                          Both pre-registered; both reported at every point.
  sleeve construction     idea 18 variant B verbatim: trend vote in {0,1/3,2/3,1} on the signs
                          of {12-1, 6m, 3m} x inverse-60d-vol risk parity, row-normalised.
  f* = 0.50               the queue's headline fraction.
  cadence bar (idea 65)   |dSharpe| across D/W/M <= 0.05 for the arm at f*, on both universes.

TUNED (2, per PROTOCOL rule 4)
------------------------------
  f    in {0.00, 0.25, 0.50, 0.75, 1.00}
  cost in {5, 10, 15, 20, 25} bps
ALL grid points are printed and written to .grid.csv.  Nothing is hidden.

CONTROLS (reported, never selected on): universe in {u56, broad}, cadence in {D,W,M},
gross convention in {g1.00 (the pre-registered one), natural}, arm in {S4, S3}.

Rule 8 (walk-forward, required): f chosen on 2009-2016 by IS Sharpe alone, per
(universe, arm, cadence, convention, cost); 2017-2026 evaluated untouched.  OOS CAGR/Sharpe/
MaxDD reported against RULES v1 and SPY over the same OOS window.

KEEP paths, both evaluated (PROTOCOL rule 4):
  4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
  4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
      CAGR >= 70% of SPY's.

SURVIVORSHIP: both equity panels are current constituents of their lists, so equity levels are
biased up; the sleeve is ETFs and is not exposed.  The bias hits the arm, the f=0 anchor and
RULES v1 identically, so the f-contrast is clean; the absolute 4b pass is not.

COST NOTE: engine.backtest applies costs as `gross_returns - turnover * bps/1e4` and the
holdings path does not depend on bps, so each weight matrix is run ONCE at 0 bps and every
rung of the ladder derived exactly.  Asserted against a direct 10 bps run at start-up.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return rows.
It hits every arm, the baseline and SPY identically; absolute Sharpe levels wait on idea 38.

Deterministic, standalone:
    python research/backtests/2026-09-05_fixed-gross-S4-blend_cloud.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

# ---- pre-registered constants -------------------------------------------------
G_FIXED = 1.00                      # THE fix this idea is about
BOOK_GROSS = 0.75                   # idea 2's book gross, before the g renormalisation
F_GRID = [0.00, 0.25, 0.50, 0.75, 1.00]
F_STAR = 0.50
COST_LADDER = (5, 10, 15, 20, 25)
COST_BPS = 10                       # PROTOCOL rule 2 headline
CADENCES = ("D", "W", "M")
CADENCE_BAR = 0.05                  # idea 65: |dSharpe| across cadences must not exceed this
ARMS = {"S4": ["TLT", "GLD", "DBC", "UUP"], "S3": ["TLT", "GLD", "UUP"]}
CONVENTIONS = ("g1.00", "natural")  # g1.00 is pre-registered; natural is a control
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
IS_END = "2016-12-31"
SPLIT = "2017-01-01"
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- sleeve (idea 18 variant B)
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
    sub = px[assets]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


# ---------------------------------------------------------------- equity book (idea 2)
def book_top20(px, n=20):
    s, above, vol20 = score(px, vol_scale=False)
    rank = s.where(above & (vol20 < 0.60)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (BOOK_GROSS / n)


def blend(E, S, f, conv):
    """conv='natural' -> (1-f)E + fS as-is; conv='g1.00' -> the same rescaled to gross G_FIXED."""
    w = (1 - f) * E + f * S
    if conv == "natural":
        return w
    g = w.sum(axis=1)
    return w.mul((G_FIXED / g.where(g > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- helpers
def run0(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=run0.freq)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def net(gr, to, bps):
    return gr - to * bps / 1e4


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    ic, is_, _ = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                IS_CAGR=ic, IS_Sharpe=is_,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"]
                and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"]
                and row["CAGR"] >= 0.70 * spy["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main
def main():
    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}

    # cost-linearity assertion — the whole ladder derivation rests on it
    px0 = universes["u56"]
    st0 = px0.index[260]
    run0.freq = "W"
    w0 = book_top20(px0)
    gr0, to0 = run0(px0, w0, st0)
    direct = backtest(px0, w0, cost_bps=COST_BPS, freq="W")["returns"].loc[st0:]
    err = float((net(gr0, to0, COST_BPS) - direct).abs().max())
    print(f"[check] cost linearity max |derived - direct| at {COST_BPS} bps = {err:.2e}")
    assert err < 1e-12, "cost is not linear in this engine — ladder derivation invalid"
    print(f"[pre-registered] g = {G_FIXED:.2f} (fixed ex ante) · arms {list(ARMS)} · "
          f"f* = {F_STAR:.2f} · cost ladder {COST_LADDER} bps · cadences {CADENCES}\n")

    records, refs = [], {}
    for tag, px in universes.items():
        start = px.index[260]
        print("=" * 120)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> "
              f"{px.index[-1].date()} | eval from {start.date()}")
        for arm, assets in ARMS.items():
            missing = [t for t in assets if t not in px.columns]
            if missing:
                raise SystemExit(f"missing sleeve tickers in {tag}: {missing}")

        # references, per cadence for the baseline (SPY has no cadence)
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        run0.freq = "W"
        bgr, bto = run0(px, rules_v1_weights(px), start)
        base = full_row(net(bgr, bto, COST_BPS))
        refs[tag] = (base, spy, bgr, bto)
        print("\nReference rows (same days, RULES v1 at its live weekly cadence, 10 bps):")
        print(fmt(pd.DataFrame({"RULES v1 baseline": base, "SPY": spy}).T))
        print(f"4b bars: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / "
              f"OOS {spy['OOS_Sharpe']:.3f} · MaxDD >= {0.60 * spy['MaxDD']:.1%} · "
              f"CAGR >= {0.70 * spy['CAGR']:.2%}")

        E = book_top20(px)
        for cad in CADENCES:
            run0.freq = cad
            for arm, assets in ARMS.items():
                S = sleeve_weights(px, assets)
                for conv in CONVENTIONS:
                    for f in F_GRID:
                        w = blend(E, S, f, conv)
                        gr, to = run0(px, w, start)
                        gross = float(w.loc[start:].sum(axis=1).mean())
                        turn = float(to.sum() / (len(gr) / 252))
                        for bps in COST_LADDER:
                            row = full_row(net(gr, to, bps))
                            row.update(universe=tag, cadence=cad, arm=arm, conv=conv, f=f,
                                       cost_bps=bps, Gross=gross, Turn_yr=turn)
                            row["4a"] = keep_4a(row, base)
                            row["4b"] = keep_4b(row, spy)
                            records.append(row)
    G = pd.DataFrame(records)
    cols = ["universe", "cadence", "arm", "conv", "f", "cost_bps", "Gross", "Turn_yr",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a", "4b"]
    G = G[cols]
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"\n[grid] {len(G)} points written to {OUT.name}.grid.csv")

    # ------------------------------------------------------------ (1) the full grid, printed
    print("\n" + "=" * 120)
    print("### (1) FULL GRID at the pre-registered convention g=1.00, weekly cadence")
    print("Every f x every cost rung, both arms, both universes.  Nothing selected yet.\n")
    for tag in universes:
        for arm in ARMS:
            sub = G[(G.universe == tag) & (G.cadence == "W") & (G.arm == arm) & (G.conv == "g1.00")]
            piv = sub.pivot_table(index="f", columns="cost_bps",
                                  values=["CAGR", "Sharpe", "MaxDD"])
            print(f"--- {tag} | arm={arm} | conv=g1.00 | cadence=W  (f=0 is the pure top20 book)")
            print(fmt(piv))
            print()

    # ------------------------------------------------------------ (2) the headline arm
    print("=" * 120)
    print(f"### (2) THE PRE-REGISTERED ARM: top20 + {F_STAR:.0%} sleeve at g={G_FIXED:.2f}")
    print("Cost ladder, both arms, both universes, weekly.  4a/4b flags at every rung.\n")
    head = G[(G.f == F_STAR) & (G.conv == "g1.00") & (G.cadence == "W")]
    print(fmt(head.set_index(["universe", "arm", "cost_bps"])[
        ["Gross", "Turn_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a", "4b"]]))
    print("\nCross-universe 4b (must pass on BOTH universes at the same rung):")
    x4b, x4a = [], []
    for arm in ARMS:
        for bps in COST_LADDER:
            s = head[(head.arm == arm) & (head.cost_bps == bps)]
            x4b.append(dict(arm=arm, cost_bps=bps,
                            u56=bool(s[s.universe == "u56"]["4b"].iloc[0]),
                            broad=bool(s[s.universe == "broad"]["4b"].iloc[0])))
            x4a.append(dict(arm=arm, cost_bps=bps,
                            u56=bool(s[s.universe == "u56"]["4a"].iloc[0]),
                            broad=bool(s[s.universe == "broad"]["4a"].iloc[0])))
    X4B = pd.DataFrame(x4b)
    X4B["both"] = X4B.u56 & X4B.broad
    X4A = pd.DataFrame(x4a)
    X4A["both"] = X4A.u56 & X4A.broad
    print("4b:\n" + X4B.set_index(["arm", "cost_bps"]).to_string())
    print("\n4a:\n" + X4A.set_index(["arm", "cost_bps"]).to_string())
    for arm in ARMS:
        ok = X4B[(X4B.arm == arm) & X4B.both]["cost_bps"]
        print(f"  arm {arm}: cross-universe 4b holds to "
              f"{int(ok.max()) if len(ok) else 'NONE'} bps")
    X4B.to_csv(OUT.with_suffix(".costladder.csv"), index=False)

    # which 4b bar binds first, rung by rung
    print("\nWhich 4b bar binds, at the headline arm (u56 / broad, g=1.00, W):")
    bind = []
    for _, r in head.iterrows():
        _, spy, _, _ = refs[r["universe"]]
        fails = []
        if not r["H1"] > spy["H1"]: fails.append("H1")
        if not r["H2"] > spy["H2"]: fails.append("H2")
        if not r["OOS_Sharpe"] > spy["OOS_Sharpe"]: fails.append("OOS")
        if not r["MaxDD"] >= 0.60 * spy["MaxDD"]: fails.append("MaxDD")
        if not r["CAGR"] >= 0.70 * spy["CAGR"]: fails.append("CAGR")
        bind.append(dict(universe=r["universe"], arm=r["arm"], cost_bps=r["cost_bps"],
                         binding=",".join(fails) if fails else "-- pass --",
                         CAGR_margin_pp=100 * (r["CAGR"] - 0.70 * spy["CAGR"]),
                         DD_margin_pp=100 * (r["MaxDD"] - 0.60 * spy["MaxDD"]),
                         H2_margin=r["H2"] - spy["H2"], OOS_margin=r["OOS_Sharpe"] - spy["OOS_Sharpe"]))
    B = pd.DataFrame(bind)
    print(fmt(B.set_index(["universe", "arm", "cost_bps"])))

    # ------------------------------------------------------------ (3) cadence bar (idea 65)
    print("\n" + "=" * 120)
    print(f"### (3) CADENCE-INSENSITIVITY BAR (idea 65): |dSharpe| across D/W/M <= {CADENCE_BAR}")
    print(f"At the pre-registered arm (f={F_STAR:.2f}, g={G_FIXED:.2f}, {COST_BPS} bps), "
          "and for the f=0 book as a control.\n")
    cad_rows = []
    for tag in universes:
        for arm in ARMS:
            for f in (0.00, F_STAR):
                sub = G[(G.universe == tag) & (G.arm == arm) & (G.conv == "g1.00")
                        & (G.f == f) & (G.cost_bps == COST_BPS)].set_index("cadence")
                sh = sub["Sharpe"].reindex(list(CADENCES))
                cg = sub["CAGR"].reindex(list(CADENCES))
                dd = sub["MaxDD"].reindex(list(CADENCES))
                spread = float(sh.max() - sh.min())
                cad_rows.append(dict(universe=tag, arm=arm, f=f,
                                     Sharpe_D=sh["D"], Sharpe_W=sh["W"], Sharpe_M=sh["M"],
                                     spread=spread, passes_bar=spread <= CADENCE_BAR,
                                     CAGR_D=cg["D"], CAGR_W=cg["W"], CAGR_M=cg["M"],
                                     MaxDD_D=dd["D"], MaxDD_W=dd["W"], MaxDD_M=dd["M"]))
    C = pd.DataFrame(cad_rows)
    C.to_csv(OUT.with_suffix(".cadence.csv"), index=False)
    print(fmt(C.set_index(["universe", "arm", "f"])))
    for arm in ARMS:
        s = C[(C.arm == arm) & (C.f == F_STAR)]
        print(f"  arm {arm} at f={F_STAR}: cadence bar passed in "
              f"{int(s.passes_bar.sum())}/{len(s)} universes "
              f"(max spread {s.spread.max():.3f})")

    # 4b under each cadence, at 10 bps — does the pass itself survive D and M?
    print(f"\n4b at f={F_STAR:.2f}, g=1.00, {COST_BPS} bps, under each cadence:")
    cc = G[(G.f == F_STAR) & (G.conv == "g1.00") & (G.cost_bps == COST_BPS)]
    print(cc.pivot_table(index=["arm", "universe"], columns="cadence", values="4b").to_string())

    # ------------------------------------------------------------ (4) rule 8
    print("\n" + "=" * 120)
    print("### (4) PROTOCOL rule 8 — f chosen on 2009-2016 IS Sharpe, 2017-2026 untouched")
    print("g is NOT selected: it is fixed at 1.00 ex ante.  Only f is chosen.\n")
    wf = []
    for (tag, cad, arm, conv, bps), sub in G.groupby(
            ["universe", "cadence", "arm", "conv", "cost_bps"], sort=False):
        pick = sub.loc[sub["IS_Sharpe"].idxmax()]
        anch = sub[sub.f == 0.0].iloc[0]
        base, spy, bgr, bto = refs[tag]
        base_c = full_row(net(bgr, bto, bps))
        wf.append(dict(universe=tag, cadence=cad, arm=arm, conv=conv, cost_bps=bps,
                       f_star=pick["f"], IS_Sharpe=pick["IS_Sharpe"],
                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                       OOS_MaxDD=pick["OOS_MaxDD"],
                       anchor_OOS_Sharpe=anch["OOS_Sharpe"], anchor_OOS_CAGR=anch["OOS_CAGR"],
                       base_OOS_Sharpe=base_c["OOS_Sharpe"], base_OOS_CAGR=base_c["OOS_CAGR"],
                       spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                       spy_OOS_MaxDD=spy["OOS_MaxDD"],
                       best_OOS=sub["OOS_Sharpe"].max(),
                       regret=pick["OOS_Sharpe"] - sub["OOS_Sharpe"].max(),
                       full_4b=bool(pick["4b"]), full_4a=bool(pick["4a"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print("Pre-registered convention (g=1.00), all cadences and cost rungs:")
    print(fmt(WF[WF.conv == "g1.00"].set_index(["universe", "cadence", "arm", "cost_bps"])[
        ["f_star", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "anchor_OOS_Sharpe", "base_OOS_Sharpe", "spy_OOS_Sharpe", "regret", "full_4b"]]))
    W1 = WF[WF.conv == "g1.00"]
    print(f"\nrule 8 picks f={F_STAR} in {int((W1.f_star == F_STAR).sum())}/{len(W1)} cells; "
          f"f=0 in {int((W1.f_star == 0).sum())}; mean regret {W1.regret.mean():+.3f}")
    print(f"OOS Sharpe of the pick beats its f=0 anchor in "
          f"{int((W1.OOS_Sharpe > W1.anchor_OOS_Sharpe).sum())}/{len(W1)}, "
          f"SPY in {int((W1.OOS_Sharpe > W1.spy_OOS_Sharpe).sum())}/{len(W1)}, "
          f"RULES v1 in {int((W1.OOS_Sharpe > W1.base_OOS_Sharpe).sum())}/{len(W1)}")
    print(f"OOS CAGR of the pick >= 70% of SPY's OOS CAGR in "
          f"{int((W1.OOS_CAGR >= 0.70 * W1.spy_OOS_CAGR).sum())}/{len(W1)} cells")

    print("\nControl — the same table under the NATURAL gross convention (never the verdict):")
    print(fmt(WF[WF.conv == "natural"].set_index(["universe", "cadence", "arm", "cost_bps"])[
        ["f_star", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "spy_OOS_Sharpe", "full_4b"]]))

    # ------------------------------------------------------------ (5) OOS-only 4b
    print("\n" + "=" * 120)
    print("### (5) OOS-ONLY VIEW of the pre-registered arm (2017-2026), g=1.00, weekly")
    print("The numbers a reader would have got holding the arm from 2017 with f fixed at 0.50.\n")
    oo = []
    for tag in universes:
        base, spy, bgr, bto = refs[tag]
        for arm in ARMS:
            for bps in COST_LADDER:
                r = G[(G.universe == tag) & (G.arm == arm) & (G.conv == "g1.00")
                      & (G.cadence == "W") & (G.f == F_STAR) & (G.cost_bps == bps)].iloc[0]
                bc = full_row(net(bgr, bto, bps))
                oo.append(dict(universe=tag, arm=arm, cost_bps=bps,
                               OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                               OOS_MaxDD=r["OOS_MaxDD"],
                               base_OOS_CAGR=bc["OOS_CAGR"], base_OOS_Sharpe=bc["OOS_Sharpe"],
                               base_OOS_MaxDD=bc["OOS_MaxDD"],
                               spy_OOS_CAGR=spy["OOS_CAGR"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                               spy_OOS_MaxDD=spy["OOS_MaxDD"]))
    OO = pd.DataFrame(oo)
    OO.to_csv(OUT.with_suffix(".oos.csv"), index=False)
    print(fmt(OO.set_index(["universe", "arm", "cost_bps"])))

    # ------------------------------------------------------------ (6) verdict inputs
    print("\n" + "=" * 120)
    print("### (6) VERDICT INPUTS (all at the pre-registered g=1.00, f=0.50)")
    for arm in ARMS:
        ok10 = X4B[(X4B.arm == arm) & (X4B.cost_bps == 10)]["both"].iloc[0]
        maxok = X4B[(X4B.arm == arm) & X4B.both]["cost_bps"]
        cadok = C[(C.arm == arm) & (C.f == F_STAR)]
        r8 = W1[(W1.arm == arm) & (W1.cost_bps == 10) & (W1.cadence == "W")]
        print(f"  {arm}: cross-universe 4b at 10 bps = {bool(ok10)}; holds to "
              f"{int(maxok.max()) if len(maxok) else 'NONE'} bps; "
              f"cadence bar {int(cadok.passes_bar.sum())}/{len(cadok)} "
              f"(max spread {cadok.spread.max():.3f}); "
              f"rule-8 f* at 10bps/W = {sorted(set(r8.f_star))}; "
              f"4a at 10 bps = {sorted(set(head[(head.arm == arm) & (head.cost_bps == 10)]['4a']))}")
    print("\nDone.")


if __name__ == "__main__":
    main()
