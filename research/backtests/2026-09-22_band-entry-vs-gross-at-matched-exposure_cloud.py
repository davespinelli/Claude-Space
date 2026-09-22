#!/usr/bin/env python3
"""Idea 2233 (lane cloud, 2026-09-22): does the BAND ENTRY THRESHOLD alone move TIME IN MARKET
more cheaply than GROSS does?

2119 found the 4b verdict on the live RULES v2 family turns entirely on GROSS, but gross is a
SIZING dial: it scales return and drawdown together, so buying the missing CAGR on gross also
buys the drawdown that fails the 4b cap.  The band's ENTRY edge b_in is a different kind of
dial: at fixed gross it changes only the SHARE OF DAYS a name is held.  If dCAGR per unit of
MEAN REALISED EXPOSURE is steeper on b_in than on gross, the book's missing return is cheaper
to buy on the band than on the size.

THE TEST IS AN EXACTLY MATCHED-EXPOSURE ONE, and it is exact rather than interpolated because
mean realised exposure is LINEAR in gross at a fixed band: holding gross g with band b gives
mean exposure g * occ(b), where occ(b) is the band's occupancy.  So for every b_in rung we can
SOLVE for the gross twin g* = E(b_in) / occ(b=0.03) that spends the same average capital, and
run that twin as a real book.  Every pair in the output is therefore a like-for-like contrast
at the same time-in-market, differing only in WHICH dial bought it.

TWO TUNED PARAMETERS (the queue's own), every grid point reported:
  TUNED 1  b_in, the band's ENTRY edge, 13 rungs: -0.02 .. +0.20.  The EXIT edge is held at
           RULES v2's own 0.03 throughout, so this is not idea 2241's asymmetric-band search
           (which KILLed the two-edge grid); it is a ONE-edge move against a fixed comparand.
           b_in > -0.03 is required for the hysteresis to stay well-formed (entry threshold
           must sit above the exit threshold), which is why the loose end stops at -0.02.
  TUNED 2  gross g, 6 rungs 0.25 .. 1.50 at the v2 band 0.03 (the GROSS arm), plus the 13
           SOLVED twins g* = E(b_in)/occ(0.03) (the MATCHED arm).

REPORTED CONSTANTS (not tuned): weekly cadence (v2's own), t+1 execution, 10 bps headline cost
with 25 and 50 bps reported beside it, 260-row warm-up, IS/OOS split 2016-12-31, equal weight
across in-band names with gated-out weight going to CASH (never re-spread) — RULES v2 clause 2.

PANELS: U56 (research/universe.json), B136 (universe_broad.json), SMALL (sub-$2B, 719 cached
names less the 54 with max_1d_move >= 1.0 in data/small_meta.csv, leaving 665 investable; SPY
joined as BENCHMARK ONLY and excluded from the book).

SURVIVORSHIP, STATED: all three panels are CURRENT-CONSTITUENT lists.  U56 and B136 are the
2026 universe files held from 2008; SMALL is the current sub-$2B screen held from 2010.  Every
level here is an UPPER BOUND on what a 2009/2010 investor could have had.  SPY is a traded
instrument and carries no such bias, which is why the 4b bar is taken against it.

BOTH KEEP PATHS at every grid point (4a vs the live RULES v2 book, 4b vs SPY) and PROTOCOL
rule 8 (dials chosen on the first half only, second half read once, untouched).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
FREQ, WARMUP, BOUT, GBASE = "W", 260, 0.03, 0.75
COSTS = [10.0, 25.0, 50.0]
BINS = [-0.02, -0.01, 0.00, 0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.11, 0.14, 0.17, 0.20]
GROSSES = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50]
SPLIT = "2016-12-31"


# ---------------------------------------------------------------- panels
def panels():
    u = load_universe()
    b = load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in s.columns if c != "SPY" and c not in bad]
    print(f"SMALL: {s.shape[1]-1} cached names, dropped {len(bad & set(s.columns))} with "
          f"max_1d_move >= 1.0, {len(keep)} investable (+SPY as benchmark only)")
    return {"U56": (u, [c for c in u.columns]),
            "B136": (b, [c for c in b.columns]),
            "SMALL": (s, keep)}


# ---------------------------------------------------------------- books
def band_state_asym(px, b_in, b_out=BOUT):
    """IN above ma*(1+b_in), OUT below ma*(1-b_out), previous state in between, OUT before
    200 closes exist.  b_in = b_out = 0.03 reproduces baseline.band_state exactly."""
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b_in), 1.0).mask(px < ma * (1 - b_out), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def band_weights(px, cols, b_in, gross, b_out=BOUT):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    ew = ew.where(band_state_asym(sub, b_in, b_out), 0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def run(px, w, start):
    """One backtest; returns (mean realised exposure, {cost: net return series})."""
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    gross_r = res["returns"].loc[start:]
    to = res["turnover"].loc[start:]
    exp = res["weights"].loc[start:].sum(axis=1).mean()
    return exp, {c: gross_r - to * c / 1e4 for c in COSTS}, to.sum() / (len(to) / 252)


# ---------------------------------------------------------------- scoring
def legs(r, spy, base, split=SPLIT):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    s, s1, s2 = metrics(spy), metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    b, b1, b2 = metrics(base), metrics(base.iloc[:h]), metrics(base.iloc[h:])
    o, so = metrics(r.loc[split:]), metrics(spy.loc[split:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
             OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
             SPY_CAGR=s["CAGR"], SPY_Sharpe=s["Sharpe"], SPY_MaxDD=s["MaxDD"],
             SPY_H1=s1["Sharpe"], SPY_H2=s2["Sharpe"],
             SPY_OOS_CAGR=so["CAGR"], SPY_OOS_Sharpe=so["Sharpe"], SPY_OOS_MaxDD=so["MaxDD"],
             BASE_Sharpe=b["Sharpe"], BASE_MaxDD=b["MaxDD"], BASE_H1=b1["Sharpe"], BASE_H2=b2["Sharpe"])
    # 4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse than live
    d["p4a"] = bool(d["H1"] > d["BASE_H1"] and d["H2"] > d["BASE_H2"] and d["MaxDD"] >= d["BASE_MaxDD"])
    # 4b legs
    L = {"H1": d["H1"] > d["SPY_H1"], "H2": d["H2"] > d["SPY_H2"],
         "OOS": d["OOS_Sharpe"] > d["SPY_OOS_Sharpe"],
         "DD": d["MaxDD"] >= 0.60 * d["SPY_MaxDD"],          # MaxDD are negative
         "CAGR": d["CAGR"] >= 0.70 * d["SPY_CAGR"]}
    d.update({f"L_{k}": bool(v) for k, v in L.items()})
    d["p4b"] = bool(all(L.values()))
    d["bind"] = ",".join(k for k, v in L.items() if not v) or "-"
    # 4b read entirely on the OOS window (the rule-8 reading)
    Lo = {"OOS_S": d["OOS_Sharpe"] > d["SPY_OOS_Sharpe"],
          "OOS_DD": d["OOS_MaxDD"] >= 0.60 * d["SPY_OOS_MaxDD"],
          "OOS_CG": d["OOS_CAGR"] >= 0.70 * d["SPY_OOS_CAGR"]}
    d["p4b_oos"] = bool(all(Lo.values()))
    d["bind_oos"] = ",".join(k for k, v in Lo.items() if not v) or "-"
    return d


# ---------------------------------------------------------------- main
def main():
    rows = []
    SER = {}          # (panel, arm, b_in, gross) -> 10 bps net return series, cached for rule 8
    BASE = {}         # panel -> 10 bps live RULES v2 return series
    for pname, (px, cols) in PANELS.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        _, base_c, _ = run(px, rules_v2_weights(px), start)
        BASE[pname] = base_c[10.0]
        # occupancy of the v2 band at gross 1.0 -> the exact linear scale for the twins
        occ, _, _ = run(px, band_weights(px, cols, BOUT, 1.0), start)
        print(f"\n=== {pname}  n={len(cols)}  {start.date()}..{px.index[-1].date()}  "
              f"occ(b=0.03,g=1.0) = {occ:.4f}")

        arms = [("GROSS", BOUT, g) for g in GROSSES]
        # b_in arm at the live gross, then its exactly matched gross twin
        for b_in in BINS:
            e, _, _ = run(px, band_weights(px, cols, b_in, GBASE), start)
            arms.append(("BIN", b_in, GBASE))
            arms.append(("MATCH", BOUT, min(max(e / occ, 0.02), 3.0)))
        seen = set()
        for arm, b_in, g in arms:
            key = (arm, round(b_in, 4), round(g, 6))
            if key in seen:
                continue
            seen.add(key)
            exp, rc, turn = run(px, band_weights(px, cols, b_in, g), start)
            SER[(pname, arm, round(b_in, 4), round(g, 6))] = rc[10.0]
            for c in COSTS:
                d = legs(rc[c], spy, base_c[c])
                d.update(panel=pname, arm=arm, b_in=b_in, gross=g, cost=c, exposure=exp, turnover=turn)
                rows.append(d)
            d10 = [r for r in rows if r["panel"] == pname and r["arm"] == arm
                   and r["b_in"] == b_in and r["gross"] == g and r["cost"] == 10.0][0]
            print(f"  {arm:6s} b_in={b_in:+.2f} g={g:.4f} exp={exp:.4f} turn={turn:5.2f}x | "
                  f"CAGR {d10['CAGR']:7.2%} Sh {d10['Sharpe']:.4f} DD {d10['MaxDD']:7.2%} "
                  f"H1/H2 {d10['H1']:.3f}/{d10['H2']:.3f} OOS {d10['OOS_CAGR']:6.2%}/"
                  f"{d10['OOS_Sharpe']:.3f}/{d10['OOS_MaxDD']:7.2%} | 4a={int(d10['p4a'])} "
                  f"4b={int(d10['p4b'])}({d10['bind']}) 4bOOS={int(d10['p4b_oos'])}({d10['bind_oos']})")

    df = pd.DataFrame(rows)
    df.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"\n{len(df)} grid points -> {OUT.name}.grid.csv")

    # ---------------- the idea's own statistic: dCAGR per unit of mean exposure
    print("\n=== SLOPE dCAGR / d(mean exposure), OLS over each arm's own rungs, 10 bps ===")
    sl = []
    for pname in df.panel.unique():
        for arm in ("GROSS", "BIN"):
            a = df[(df.panel == pname) & (df.arm == arm) & (df.cost == 10.0)].sort_values("exposure")
            for win, cy, xk in (("FULL", "CAGR", "exposure"), ("OOS", "OOS_CAGR", "exposure")):
                b1, b0 = np.polyfit(a[xk].values, a[cy].values, 1)
                rr = np.corrcoef(a[xk].values, a[cy].values)[0, 1]
                sl.append(dict(panel=pname, arm=arm, window=win, slope=b1, intercept=b0, r=rr,
                               exp_lo=a[xk].min(), exp_hi=a[xk].max(), n=len(a)))
                print(f"  {pname:6s} {arm:6s} {win:4s}  slope {b1:+8.4f} CAGR/unit-exposure  "
                      f"r={rr:+.3f}  exposure span [{a[xk].min():.3f}, {a[xk].max():.3f}]  n={len(a)}")
    pd.DataFrame(sl).to_csv(OUT.with_suffix(".slopes.csv"), index=False)

    # ---------------- exactly matched pairs: BIN rung vs its solved gross twin
    print("\n=== MATCHED-EXPOSURE PAIRS (BIN b_in @ g=0.75  vs  GROSS g* @ b=0.03), 10 bps ===")
    pr = []
    for pname in df.panel.unique():
        occ = df[(df.panel == pname) & (df.arm == "MATCH")]
        for b_in in BINS:
            a = df[(df.panel == pname) & (df.arm == "BIN") & (df.b_in == b_in) & (df.cost == 10.0)]
            if a.empty:
                continue
            a = a.iloc[0]
            cand = df[(df.panel == pname) & (df.arm == "MATCH") & (df.cost == 10.0)]
            j = (cand.exposure - a.exposure).abs().idxmin()
            m = df.loc[j]
            row = dict(panel=pname, b_in=b_in, exp_bin=a.exposure, exp_match=m.exposure,
                       g_star=m.gross, dCAGR=a.CAGR - m.CAGR, dSharpe=a.Sharpe - m.Sharpe,
                       dMaxDD=a.MaxDD - m.MaxDD, dOOS_CAGR=a.OOS_CAGR - m.OOS_CAGR,
                       dOOS_Sharpe=a.OOS_Sharpe - m.OOS_Sharpe, dOOS_MaxDD=a.OOS_MaxDD - m.OOS_MaxDD,
                       dTurnover=a.turnover - m.turnover,
                       bin_4b=int(a.p4b), match_4b=int(m.p4b), bin_4a=int(a.p4a), match_4a=int(m.p4a))
            pr.append(row)
            print(f"  {pname:6s} b_in={b_in:+.2f} exp {a.exposure:.4f} vs g*={m.gross:.4f} "
                  f"exp {m.exposure:.4f} | dCAGR {row['dCAGR']:+7.2%} dSharpe {row['dSharpe']:+.4f} "
                  f"dMaxDD {row['dMaxDD']:+7.2%} | dOOS_CAGR {row['dOOS_CAGR']:+7.2%} "
                  f"dOOS_Sh {row['dOOS_Sharpe']:+.4f} | dTurn {row['dTurnover']:+5.2f}x | "
                  f"4b bin/match {row['bin_4b']}/{row['match_4b']}")
    pdf = pd.DataFrame(pr)
    pdf.to_csv(OUT.with_suffix(".pairs.csv"), index=False)
    if len(pdf):
        print("\n  BIN beats its matched GROSS twin on full CAGR: "
              f"{int((pdf.dCAGR > 0).sum())} of {len(pdf)}; on OOS CAGR "
              f"{int((pdf.dOOS_CAGR > 0).sum())} of {len(pdf)}; on full Sharpe "
              f"{int((pdf.dSharpe > 0).sum())} of {len(pdf)}; on MaxDD (less deep) "
              f"{int((pdf.dMaxDD > 0).sum())} of {len(pdf)}")
        print(pdf.groupby("panel")[["dCAGR", "dSharpe", "dMaxDD", "dOOS_CAGR", "dOOS_Sharpe", "dTurnover"]]
              .median().to_string(float_format=lambda x: f"{x:+.4f}"))

    # ---------------- PROTOCOL rule 8: choose on the first half, read the second once
    print("\n=== RULE 8 WALK-FORWARD: dial chosen on IS (first half) by IS Sharpe @10 bps, "
          "OOS (second half) read once ===")
    wf = []
    for pname in df.panel.unique():
        px, cols = PANELS[pname]
        start = px.index[WARMUP]
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[start:]
        h = len(spy_full) // 2
        is_idx, oos_idx = spy_full.index[:h], spy_full.index[h:]
        for arm in ("GROSS", "BIN", "MATCH"):
            a = df[(df.panel == pname) & (df.arm == arm) & (df.cost == 10.0)]
            if a.empty:
                continue
            # IS Sharpe must be recomputed per book on the IS window
            best, bestv = None, -9e9
            for _, r in a.iterrows():
                ser = SER[(pname, arm, round(r.b_in, 4), round(r.gross, 6))]
                v = metrics(ser.loc[is_idx])["Sharpe"]
                if v > bestv:
                    bestv, best = v, r
            ser = SER[(pname, "GROSS" if arm == "GROSS" else arm, round(best.b_in, 4), round(best.gross, 6))]
            ro, so = ser.loc[oos_idx], spy_full.loc[oos_idx]
            bo = BASE[pname].loc[oos_idx]
            mo, ms, mb = metrics(ro), metrics(so), metrics(bo)
            row = dict(panel=pname, arm=arm, pick_b_in=best.b_in, pick_gross=best.gross,
                       IS_Sharpe=bestv, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       SPY_OOS_CAGR=ms["CAGR"], SPY_OOS_Sharpe=ms["Sharpe"], SPY_OOS_MaxDD=ms["MaxDD"],
                       BASE_OOS_CAGR=mb["CAGR"], BASE_OOS_Sharpe=mb["Sharpe"], BASE_OOS_MaxDD=mb["MaxDD"])
            row["OOS_4b"] = int(mo["Sharpe"] > ms["Sharpe"] and mo["MaxDD"] >= 0.60 * ms["MaxDD"]
                                and mo["CAGR"] >= 0.70 * ms["CAGR"])
            row["OOS_4a"] = int(mo["Sharpe"] > mb["Sharpe"] and mo["MaxDD"] >= mb["MaxDD"])
            wf.append(row)
            print(f"  {pname:6s} {arm:6s} pick b_in={best.b_in:+.2f} g={best.gross:.4f} "
                  f"(IS Sh {bestv:.4f}) -> OOS {mo['CAGR']:6.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:7.2%} "
                  f"| SPY OOS {ms['CAGR']:6.2%}/{ms['Sharpe']:.4f}/{ms['MaxDD']:7.2%} "
                  f"| v2 OOS {mb['CAGR']:6.2%}/{mb['Sharpe']:.4f}/{mb['MaxDD']:7.2%} "
                  f"| 4bOOS={row['OOS_4b']} 4aOOS={row['OOS_4a']}")
    pd.DataFrame(wf).to_csv(OUT.with_suffix(".walkforward.csv"), index=False)

    print("\n=== KEEP-PATH CENSUS over all grid points ===")
    for c in COSTS:
        s = df[df.cost == c]
        print(f"  {c:4.0f} bps: 4a {int(s.p4a.sum())} of {len(s)}   4b(full) {int(s.p4b.sum())} of {len(s)}"
              f"   4b(OOS-only) {int(s.p4b_oos.sum())} of {len(s)}")
    fails = df[(df.cost == 10.0) & (~df.p4b)]
    if len(fails):
        print("  4b binding legs at 10 bps:",
              {k: int(sum(k in b.split(",") for b in fails.bind)) for k in ("H1", "H2", "OOS", "DD", "CAGR")})


PANELS = {}
if __name__ == "__main__":
    PANELS = panels()
    main()
