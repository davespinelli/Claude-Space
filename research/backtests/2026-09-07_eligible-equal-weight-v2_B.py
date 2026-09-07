#!/usr/bin/env python3
"""Idea 28 — eligible-equal-weight-v2 (lane B, 2026-09-07).

The Sep-3 recommendation memo's Finding 2: "the eligibility filter is the edge".
Equal-weight EVERY name that is above its 200d average with vol20 < 0.60, gross G,
weekly.  It reported CAGR 10.4% / Sharpe 1.05 / halves 1.07-1.03 at G=0.75 and said
it missed the 4b CAGR floor by 0.23pp.  The queue asked for the proper test:
gross 75/85/100 reported together (no picking), halves, rule-8 OOS, 2020/2022,
turnover, and BTC/ETH excluded vs included at a 5% cap.

Since then RULES v2 went live (2026-09-06) and is the *same family with the vol
filter dropped and a +/-3% band added*.  So this run is also the direct question:
does `vol20 < max_vol` earn its place next to the live book?

Two tuned parameters: gross G and the vol ceiling max_vol.  ALL grid points reported.
Arms (structural, not tuned): crypto EXCL vs INCL-at-5%-cap; cost rungs 10 and 25 bps.
Deterministic, standalone.  Does not modify RULES.md / scan.py / bot.py / baseline.py.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state, EXCLUDE  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 200)
CRYPTO = ["BTC-USD", "ETH-USD"]
WARM = 260                      # skip the 200d warm-up, same convention as baseline.compare
IS_END = "2016-12-31"           # rule 8: parameters chosen on 2009-2016 only
OOS_START = "2017-01-01"
GROSS = [0.75, 0.85, 1.00]
MAXVOL = [0.30, 0.40, 0.50, 0.60, 0.80, 99.0]   # 99.0 == filter OFF
RUNGS = [10, 25]


# ---------------------------------------------------------------- the book
def elig_ew_weights(px, gross=0.75, max_vol=0.60, crypto_cap=None):
    """Equal-weight every eligible name at gross/N of NAV; ineligible weight -> CASH.

    Eligible = priced today AND above its 200d simple average AND vol20 < max_vol.
    crypto_cap=None  -> BTC/ETH never held (weight forced to 0, panel unchanged).
    crypto_cap=0.05  -> BTC/ETH held but capped at 5% NAV each; the weight freed by the
                        cap is re-spread equally over the eligible NON-crypto names.
    """
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = (above & (vol20 < max_vol) & px.notna())
    is_c = pd.Series([c in CRYPTO for c in px.columns], index=px.columns)
    if crypto_cap is None:
        elig = elig & (~is_c)                       # crypto simply not in the book
    n = elig.sum(axis=1).replace(0, np.nan)
    w = elig.astype(float).mul(gross, axis=0).div(n, axis=0)
    if crypto_cap is not None:
        cw = w.loc[:, is_c[is_c].index]
        freed = (cw - cw.clip(upper=crypto_cap)).sum(axis=1)
        w.loc[:, is_c[is_c].index] = cw.clip(upper=crypto_cap)
        nc = (elig & (~is_c)).astype(float)
        w = w + nc.div(nc.sum(axis=1).replace(0, np.nan), axis=0).mul(freed, axis=0).fillna(0.0)
    return w.fillna(0.0)


# ---------------------------------------------------------------- scoring helpers
def slice_metrics(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_stats(res, start, turn_years=None):
    r = res["returns"].loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    t = res["turnover"].loc[start:]
    yrs = m["Years"]
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
               H1=m1["Sharpe"], H2=m2["Sharpe"], TO=t.sum() / yrs)
    ro = r.loc[OOS_START:]
    mo = metrics(ro)
    out.update(oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])
    ri = r.loc[:IS_END]
    out["iSharpe"] = metrics(ri)["Sharpe"]
    for y in (2020, 2022):
        ry = r[r.index.year == y]
        out[f"y{y}"] = (1 + ry).prod() - 1
        eq = (1 + ry).cumprod()
        out[f"dd{y}"] = (eq / eq.cummax() - 1).min()
    return out


def bars_4b(s, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's."""
    return dict(H1=s["H1"] > spy["H1"], H2=s["H2"] > spy["H2"], OOS=s["oSharpe"] > spy["oSharpe"],
                DD=abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]), CAGR=s["CAGR"] >= 0.70 * spy["CAGR"])


def bars_4a(s, base):
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves and MaxDD no worse."""
    return dict(H1=s["H1"] > base["H1"], H2=s["H2"] > base["H2"], DD=s["MaxDD"] >= base["MaxDD"])


# ---------------------------------------------------------------- run
def main():
    px_all = load_universe(exclude=set())          # 58 cols: U56 + BTC-USD + ETH-USD
    px_u56 = load_universe()                       # the record's U56 panel
    start = px_all.index[WARM]
    print(f"panel {px_all.shape} {px_all.index[0].date()}..{px_all.index[-1].date()}  "
          f"scored from {start.date()}  (U56 {px_u56.shape})")
    print(f"crypto first valid: " + ", ".join(f"{c} {px_all[c].first_valid_index().date()}" for c in CRYPTO))

    # ---- comparands, per cost rung
    spy_r = px_all["SPY"].pct_change().fillna(0.0)
    ref = {}
    for c in RUNGS:
        ref[c] = dict(
            v2=full_stats(backtest(px_u56, rules_v2_weights(px_u56), cost_bps=c, freq="W"), start),
            v1=full_stats(backtest(px_u56, rules_v1_weights(px_u56), cost_bps=c, freq="W"), start),
            spy=full_stats({"returns": spy_r, "turnover": pd.Series(0.0, index=spy_r.index)}, start),
        )
    r = ref[10]
    print("\n=== comparands (10 bps) ===")
    print(pd.DataFrame({k: {a: r[k][a] for a in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "TO")}
                        for k in ("v2", "v1", "spy")}).T.to_string(float_format=lambda x: f"{x:.4f}"))
    spy = r["spy"]
    print(f"\n4b bars (from SPY, this sample): H1>{spy['H1']:.4f} H2>{spy['H2']:.4f} "
          f"OOS>{spy['oSharpe']:.4f} |MaxDD|<={0.60*abs(spy['MaxDD']):.4%} CAGR>={0.70*spy['CAGR']:.4%}")

    # ---- GATE 1: reproduce the Sep-3 memo's Finding 2 headline (G=0.75, max_vol=0.60, EXCL)
    g1 = full_stats(backtest(px_all, elig_ew_weights(px_all, 0.75, 0.60, None), cost_bps=10, freq="W"), start)
    print("\n=== GATE 1: memo Finding 2 (G=0.75, max_vol=0.60, crypto EXCL) ===")
    print(f"  published CAGR 10.4%  Sharpe 1.05  halves 1.07 / 1.03  (memo sample ended 2026-09-03)")
    print(f"  here      CAGR {g1['CAGR']:.4%}  Sharpe {g1['Sharpe']:.4f}  halves {g1['H1']:.4f} / {g1['H2']:.4f}"
          f"  MaxDD {g1['MaxDD']:.4%}  turnover {g1['TO']:.2f}x/yr")
    print(f"  memo: 'misses the 4b CAGR floor by 0.23pp' -> here floor {0.70*spy['CAGR']:.4%}, "
          f"miss {100*(0.70*spy['CAGR'] - g1['CAGR']):+.2f}pp")
    print(f"  memo: 'one third of the turnover' of v1 -> here {g1['TO']/r['v1']['TO']:.3f} of v1's {r['v1']['TO']:.2f}x")

    # ---- GATE 2: the EXCL arm on the 58-col panel must equal the same book on U56
    a58 = backtest(px_all, elig_ew_weights(px_all, 0.75, 0.60, None), cost_bps=10, freq="W")["returns"].loc[start:]
    a56 = backtest(px_u56, elig_ew_weights(px_u56, 0.75, 0.60, None), cost_bps=10, freq="W")["returns"].loc[start:]
    print(f"\n=== GATE 2: EXCL arm panel-invariance  max|d daily return| = {(a58-a56).abs().max():.3e} ===")

    # ---- GATE 3: max_vol=99 + gross=0.75 must equal rules_v2_weights with band=0.00 modulo the
    #      band; check instead that it equals a hand-built raw-MA equal-weight book.
    ma_ew = (px_all.drop(columns=CRYPTO) > px_all.drop(columns=CRYPTO).rolling(200).mean())
    ma_ew = ma_ew.astype(float).mul(0.75).div(ma_ew.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w99 = elig_ew_weights(px_all, 0.75, 99.0, None)
    print(f"=== GATE 3: max_vol=OFF == raw 200d equal-weight  max|dw| = "
          f"{(w99.drop(columns=CRYPTO) - ma_ew).abs().max().max():.3e} ===")

    # ---- the grid
    rows = []
    for cap, arm in ((None, "EXCL"), (0.05, "INCL5")):
        for g in GROSS:
            for mv in MAXVOL:
                w = elig_ew_weights(px_all, g, mv, cap)
                for c in RUNGS:
                    s = full_stats(backtest(px_all, w, cost_bps=c, freq="W"), start)
                    s.update(arm=arm, G=g, max_vol=mv, bps=c)
                    b4b = bars_4b(s, ref[c]["spy"]); b4a = bars_4a(s, ref[c]["v2"])
                    s["p4b"] = all(b4b.values()); s["p4a"] = all(b4a.values())
                    s["fail4b"] = ",".join(k for k, v in b4b.items() if not v) or "-"
                    rows.append(s)
    G = pd.DataFrame(rows)
    cols = ["arm", "G", "max_vol", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "oCAGR", "oSharpe", "oMaxDD", "TO", "y2020", "y2022", "p4a", "p4b", "fail4b"]
    print(f"\n=== FULL GRID: {len(G)} points (2 arms x {len(GROSS)} gross x {len(MAXVOL)} max_vol x {len(RUNGS)} rungs) ===")
    with pd.option_context("display.max_rows", 300):
        print(G[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print(f"\nKEEP paths over all {len(G)} points: 4a {int(G.p4a.sum())}/{len(G)}   4b {int(G.p4b.sum())}/{len(G)}")
    for c in RUNGS:
        s = G[G.bps == c]
        print(f"  {c:>2} bps: 4a {int(s.p4a.sum())}/{len(s)}  4b {int(s.p4b.sum())}/{len(s)}")
    print("  4b first-failing bars (10 bps):")
    print(G[G.bps == 10].fail4b.value_counts().to_string())
    print("\n  the three gross values asked for, at max_vol=0.60, 10 bps, both arms:")
    ask = G[(G.bps == 10) & (G.max_vol == 0.60)]
    print(ask[["arm", "G", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "TO", "p4a", "p4b", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- does the vol filter earn its place?  paired, filter ON vs OFF
    print("\n=== the vol filter, paired against max_vol=OFF at the same (arm, G, rung) ===")
    off = G[G.max_vol == 99.0].set_index(["arm", "G", "bps"])
    on = G[G.max_vol != 99.0]
    d = on.join(off[["Sharpe", "CAGR", "MaxDD", "oSharpe"]].add_prefix("off_"), on=["arm", "G", "bps"])
    d["dSharpe"] = d.Sharpe - d.off_Sharpe; d["dCAGR"] = d.CAGR - d.off_CAGR
    d["dMaxDD"] = d.MaxDD - d.off_MaxDD; d["doSharpe"] = d.oSharpe - d.off_oSharpe
    print(d.groupby("max_vol")[["dSharpe", "dCAGR", "dMaxDD", "doSharpe"]].mean()
          .to_string(float_format=lambda x: f"{x:+.4f}"))
    print(f"  filter beats OFF on Sharpe in {int((d.dSharpe>0).sum())}/{len(d)} paired points; "
          f"on OOS Sharpe in {int((d.doSharpe>0).sum())}/{len(d)}; "
          f"on MaxDD in {int((d.dMaxDD>0).sum())}/{len(d)}")

    # ---- crypto arm, paired
    print("\n=== crypto at a 5% cap, paired against EXCL at the same (G, max_vol, rung) ===")
    e = G[G.arm == "EXCL"].set_index(["G", "max_vol", "bps"])
    i = G[G.arm == "INCL5"].join(e[["Sharpe", "CAGR", "MaxDD", "oSharpe", "TO"]].add_prefix("ex_"),
                                 on=["G", "max_vol", "bps"])
    i["dSharpe"] = i.Sharpe - i.ex_Sharpe; i["dCAGR"] = i.CAGR - i.ex_CAGR
    i["dMaxDD"] = i.MaxDD - i.ex_MaxDD; i["dTO"] = i.TO - i.ex_TO
    print(i[["dSharpe", "dCAGR", "dMaxDD", "dTO"]].mean().to_string(float_format=lambda x: f"{x:+.4f}"))
    print(f"  INCL5 beats EXCL on Sharpe {int((i.dSharpe>0).sum())}/{len(i)}, "
          f"CAGR {int((i.dCAGR>0).sum())}/{len(i)}, MaxDD {int((i.dMaxDD>0).sum())}/{len(i)}")

    # ---- RULE 8 walk-forward: pick (G, max_vol) on 2009-2016 by IS Sharpe, read OOS once
    print("\n=== RULE 8 walk-forward: (G, max_vol) chosen on 2009-2016 IS Sharpe, 2017-2026 read once ===")
    wf = []
    for arm in ("EXCL", "INCL5"):
        for c in RUNGS:
            sub = G[(G.arm == arm) & (G.bps == c)]
            pick = sub.loc[sub.iSharpe.idxmax()]
            best = sub.loc[sub.oSharpe.idxmax()]
            wf.append(dict(arm=arm, bps=c, pick_G=pick.G, pick_mv=pick.max_vol, IS=pick.iSharpe,
                           oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                           base_oSharpe=ref[c]["v2"]["oSharpe"], spy_oSharpe=ref[c]["spy"]["oSharpe"],
                           oos_best_G=best.G, oos_best_mv=best.max_vol, oos_best_S=best.oSharpe,
                           regret=best.oSharpe - pick.oSharpe))
    W = pd.DataFrame(wf)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"  chooser regret vs the OOS-best cell: mean {W.regret.mean():+.4f} Sharpe, max {W.regret.max():+.4f}")
    print(f"  picked book vs RULES v2 OOS: {(W.oSharpe - W.base_oSharpe).mean():+.4f} mean OOS Sharpe")
    print(f"  picked book vs SPY OOS:      {(W.oSharpe - W.spy_oSharpe).mean():+.4f} mean OOS Sharpe")

    # ---- RULE 8, variant B: the MEMO'S OWN pre-stated selection rule, applied IN-SAMPLE only
    #      "G chosen ONLY from idea 28's three reported values by 'smallest G whose MaxDD <= 60%
    #       of SPY's and CAGR >= 70% of SPY's'; if none, keep 75%" -- at max_vol=0.60, its value.
    print("\n=== RULE 8 variant B: the memo's pre-stated G rule, evaluated on 2009-2016 only ===")
    is_rows = []
    for cap, arm in ((None, "EXCL"), (0.05, "INCL5")):
        for g in GROSS:
            w = elig_ew_weights(px_all, g, 0.60, cap)
            for c in RUNGS:
                rr = backtest(px_all, w, cost_bps=c, freq="W")["returns"].loc[start:IS_END]
                cg, sh, dd = slice_metrics(rr)
                is_rows.append(dict(arm=arm, G=g, bps=c, isCAGR=cg, isSharpe=sh, isMaxDD=dd))
    ISd = pd.DataFrame(is_rows)
    for c in RUNGS:
        spy_is = metrics(spy_r.loc[start:IS_END])
        ISd.loc[ISd.bps == c, "ok"] = (
            (ISd.isMaxDD.abs() <= 0.60 * abs(spy_is["MaxDD"])) & (ISd.isCAGR >= 0.70 * spy_is["CAGR"]))
    print(f"  IS SPY (2009-{IS_END[:4]}): CAGR {spy_is['CAGR']:.4%} MaxDD {spy_is['MaxDD']:.4%} "
          f"-> IS bars CAGR>={0.70*spy_is['CAGR']:.4%} |DD|<={0.60*abs(spy_is['MaxDD']):.4%}")
    print(ISd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for arm in ("EXCL", "INCL5"):
        for c in RUNGS:
            s = ISd[(ISd.arm == arm) & (ISd.bps == c)].sort_values("G")
            pick = s[s.ok].G.min() if s.ok.any() else 0.75
            oos = G[(G.arm == arm) & (G.bps == c) & (G.G == pick) & (G.max_vol == 0.60)].iloc[0]
            print(f"  {arm:>5} {c:>2}bps -> memo rule picks G={pick:.2f}  |  OOS CAGR {oos.oCAGR:.4%} "
                  f"Sharpe {oos.oSharpe:.4f} MaxDD {oos.oMaxDD:.4%}  |  full-sample 4b {'PASS' if oos.p4b else 'FAIL ('+oos.fail4b+')'}"
                  f"  4a {'PASS' if oos.p4a else 'FAIL'}")

    # ---- RULE 8, variant C: IS-Sharpe chooser CONSTRAINED by the IS drawdown bar
    print("\n=== RULE 8 variant C: max IS Sharpe subject to the IS drawdown bar being met ===")
    isdd = {}
    for cap, arm in ((None, "EXCL"), (0.05, "INCL5")):
        for g in GROSS:
            for mv in MAXVOL:
                w = elig_ew_weights(px_all, g, mv, cap)
                for c in RUNGS:
                    rr = backtest(px_all, w, cost_bps=c, freq="W")["returns"].loc[start:IS_END]
                    isdd[(arm, g, mv, c)] = metrics(rr)["MaxDD"]
    G["isMaxDD"] = [isdd[(r.arm, r.G, r.max_vol, r.bps)] for r in G.itertuples()]
    G["isDDok"] = G.isMaxDD.abs() <= 0.60 * abs(spy_is["MaxDD"])
    for arm in ("EXCL", "INCL5"):
        for c in RUNGS:
            sub = G[(G.arm == arm) & (G.bps == c) & G.isDDok]
            if not len(sub):
                print(f"  {arm:>5} {c:>2}bps -> no cell meets the IS DD bar"); continue
            p = sub.loc[sub.iSharpe.idxmax()]
            print(f"  {arm:>5} {c:>2}bps -> G={p.G:.2f} max_vol={p.max_vol:.2f} (IS Sharpe {p.iSharpe:.4f}, "
                  f"{int(sub.isDDok.sum())}/{len(G[(G.arm==arm)&(G.bps==c)])} cells eligible) | OOS CAGR {p.oCAGR:.4%} "
                  f"Sharpe {p.oSharpe:.4f} MaxDD {p.oMaxDD:.4%} | full 4b {'PASS' if p.p4b else 'FAIL ('+p.fail4b+')'} "
                  f"4a {'PASS' if p.p4a else 'FAIL'} | v2 OOS {ref[c]['v2']['oSharpe']:.4f} SPY OOS {ref[c]['spy']['oSharpe']:.4f}")

    # ---- head-to-head: is any 4b pass actually better than the LIVE book?
    print("\n=== the 14 (10 bps) 4b passes vs the LIVE RULES v2 book ===")
    v2 = ref[10]["v2"]
    print(f"  RULES v2: CAGR {v2['CAGR']:.4%} Sharpe {v2['Sharpe']:.4f} MaxDD {v2['MaxDD']:.4%} "
          f"halves {v2['H1']:.4f}/{v2['H2']:.4f} OOS {v2['oSharpe']:.4f} TO {v2['TO']:.2f}x  "
          f"-> its own 4b: {'PASS' if all(bars_4b(v2, spy).values()) else 'FAIL (' + ','.join(k for k,v in bars_4b(v2,spy).items() if not v) + ')'}")
    p = G[(G.bps == 10) & G.p4b].copy()
    p["dS_v2"] = p.Sharpe - v2["Sharpe"]; p["dCAGR_v2"] = p.CAGR - v2["CAGR"]
    p["dDD_v2"] = p.MaxDD - v2["MaxDD"]; p["doS_v2"] = p.oSharpe - v2["oSharpe"]
    print(p[["arm", "G", "max_vol", "CAGR", "Sharpe", "MaxDD", "oSharpe", "dS_v2", "dCAGR_v2", "dDD_v2", "doS_v2"]]
          .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    print(f"  4b passes beating v2 on Sharpe: {int((p.dS_v2>0).sum())}/{len(p)}; on OOS Sharpe "
          f"{int((p.doS_v2>0).sum())}/{len(p)}; on MaxDD {int((p.dDD_v2>0).sum())}/{len(p)}; "
          f"on CAGR {int((p.dCAGR_v2>0).sum())}/{len(p)}")

    # ---- stress years, headline cells
    print("\n=== 2020 / 2022, at max_vol=0.60 and OFF, 10 bps ===")
    st = G[(G.bps == 10) & (G.max_vol.isin([0.60, 99.0]))]
    print(st[["arm", "G", "max_vol", "y2020", "dd2020", "y2022", "dd2022"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for k in ("v2", "v1", "spy"):
        s = ref[10][k]
        print(f"  {k:>3}: 2020 {s['y2020']:+.2%} (dd {s['dd2020']:.2%})   2022 {s['y2022']:+.2%} (dd {s['dd2022']:.2%})")

    out = ROOT / "research" / "backtests" / "2026-09-07_eligible-equal-weight-v2_B.csv"
    G[cols + ["iSharpe", "dd2020", "dd2022", "Vol"]].to_csv(out, index=False)
    print(f"\nwrote {out.relative_to(ROOT)}")
    return G, W, ref


if __name__ == "__main__":
    main()
