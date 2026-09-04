#!/usr/bin/env python3
"""Idea 19: spy-tlt-gld-riskparity (lane C, 2026-09-04).

Inverse-vol risk parity on SPY / TLT / GLD, monthly rebalance, as a low-turnover
benchmark the live book must beat.

Book RP(L, g):  w_i = g * (1/vol_i) / sum_j (1/vol_j),  vol_i = trailing L-day
realised vol (annualised), rebalanced monthly, held drifting in between.
Exactly 2 tuned parameters: L (vol lookback) and g (gross).  ALL 12 grid points
reported.  Controls (untuned): equal-weight thirds, 60/40 SPY/TLT, SPY, RULES v1.

PROTOCOL: 10 bps per unit turnover, weights at close t applied at t+1 (engine),
full sample + halves, rule-8 walk-forward (params chosen on 2009-2016 only,
evaluated 2017-2026), both KEEP paths 4a and 4b.

Deterministic, standalone:  python3 research/backtests/2026-09-04_spy-tlt-gld-riskparity_C.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, compare, backtest, metrics  # noqa: E402

ASSETS = ["SPY", "TLT", "GLD"]
LOOKBACKS = [20, 60, 120, 252]          # tuned param 1
GROSSES = [0.60, 0.75, 1.00]            # tuned param 2
COST_BPS = 10
IS_END = "2016-12-31"                   # rule 8: parameters chosen on 2009-2016 only
OOS_START = "2017-01-01"

pd.set_option("display.width", 200)


# ---------------------------------------------------------------- weight books
def rp_weights(px, L, g, assets=ASSETS):
    """Inverse-vol risk parity over `assets`, zero everywhere else."""
    sub = px[assets]
    vol = sub.pct_change().rolling(L).std() * np.sqrt(252)
    inv = 1.0 / vol.clip(lower=1e-6)
    inv = inv.where(vol.notna())
    w = inv.div(inv.sum(axis=1), axis=0) * g
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w.fillna(0.0)
    return out


def static_weights(px, wmap):
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    for t, w in wmap.items():
        out[t] = w
    out.iloc[:260] = 0.0          # same warm-up handling as the RP books
    return out


# ---------------------------------------------------------------- measurement
def stats(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def run(px, wfn, freq="M"):
    """Backtest and return the return series (sliced to the common start) + turnover/yr."""
    res = backtest(px, wfn(px), cost_bps=COST_BPS, freq=freq)
    start = px.index[260]
    r = res["returns"].loc[start:]
    to = res["turnover"].loc[start:]
    yrs = len(r) / 252
    return r, to.sum() / yrs


def full_halves_oos(r):
    h = len(r) // 2
    d = stats(r)
    d["H1"] = metrics(r.iloc[:h])["Sharpe"]
    d["H2"] = metrics(r.iloc[h:])["Sharpe"]
    oos = r.loc[OOS_START:]
    o = stats(oos)
    d["oCAGR"], d["oSharpe"], d["oMaxDD"] = o["CAGR"], o["Sharpe"], o["MaxDD"]
    d["isSharpe"] = metrics(r.loc[:IS_END])["Sharpe"]
    return d


def keep_paths(d, base, spy):
    """4a: Sharpe > live rules in BOTH halves and MaxDD no worse than the live rules.
       4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    a = (d["H1"] > base["H1"]) and (d["H2"] > base["H2"]) and (d["MaxDD"] >= base["MaxDD"])
    fails = []
    if d["H1"] <= spy["H1"]: fails.append("H1")
    if d["H2"] <= spy["H2"]: fails.append("H2")
    if d["oSharpe"] <= spy["oSharpe"]: fails.append("OOS")
    if abs(d["MaxDD"]) > 0.60 * abs(spy["MaxDD"]): fails.append("DD")
    if d["CAGR"] < 0.70 * spy["CAGR"]: fails.append("CAGR")
    return a, (len(fails) == 0), ",".join(fails) if fails else "-"


# ---------------------------------------------------------------- main
def main():
    px = load_universe()
    assert all(a in px.columns for a in ASSETS), "SPY/TLT/GLD must be in universe.json"
    print(f"panel {px.shape[0]} rows x {px.shape[1]} cols, {px.index[0].date()} .. {px.index[-1].date()}")
    print(f"weekend rows in index: {(px.index.dayofweek >= 5).sum()}  (idea 38 fix check)")
    start = px.index[260]
    print(f"eval window {start.date()} .. {px.index[-1].date()};  IS <= {IS_END}, OOS >= {OOS_START}\n")

    # reference books -------------------------------------------------------
    ref = {}
    r_base, to_base = run(px, rules_v1_weights, freq="W")     # live rules, weekly (as in compare())
    ref["RULES v1 (live)"] = (full_halves_oos(r_base), to_base)
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    ref["SPY buy&hold"] = (full_halves_oos(spy_r), 0.0)
    r_ew, to_ew = run(px, lambda p: rp_weights_ew(p))
    ref["EW thirds (control)"] = (full_halves_oos(r_ew), to_ew)
    r_6040, to_6040 = run(px, lambda p: static_weights(p, {"SPY": 0.60, "TLT": 0.40}))
    ref["60/40 SPY-TLT (control)"] = (full_halves_oos(r_6040), to_6040)

    base = ref["RULES v1 (live)"][0]
    spy = ref["SPY buy&hold"][0]

    # sanity: reproduce baseline.compare()'s baseline numbers exactly ---------
    chk = compare("RP(60,1.00) [compare() cross-check]", lambda p: rp_weights(p, 60, 1.00), px,
                  freq="M", baseline_freq="W", cost_bps=COST_BPS)
    print()

    # the grid --------------------------------------------------------------
    rows = []
    for L in LOOKBACKS:
        for g in GROSSES:
            r, to = run(px, lambda p, L=L, g=g: rp_weights(p, L, g))
            d = full_halves_oos(r)
            p4a, p4b, fails = keep_paths(d, base, spy)
            rows.append(dict(book=f"RP L={L:3d} g={g:.2f}", L=L, g=g, **d,
                             turn=to, p4a=p4a, p4b=p4b, fails=fails))

    grid = pd.DataFrame(rows)

    def show(df, cols=None):
        cols = cols or ["book", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                        "oCAGR", "oSharpe", "oMaxDD", "turn", "p4a", "p4b", "fails"]
        v = df[cols].copy()
        for c in ("CAGR", "MaxDD", "oCAGR", "oMaxDD"):
            if c in v: v[c] = v[c].map(lambda x: f"{x:.1%}")
        for c in ("Sharpe", "H1", "H2", "oSharpe", "turn"):
            if c in v: v[c] = v[c].map(lambda x: f"{x:.3f}")
        print(v.to_string(index=False))

    print("=" * 118)
    print("REFERENCE BOOKS (full sample; oXXX = out-of-sample 2017+; turn = turnover/yr)")
    print("=" * 118)
    refdf = pd.DataFrame([dict(book=k, **v[0], turn=v[1]) for k, v in ref.items()])
    show(refdf, ["book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "turn"])

    print("\n" + "=" * 118)
    print("ALL 12 GRID POINTS (2 tuned params: L, g) — nothing withheld")
    print("=" * 118)
    show(grid)

    # rule 8 walk-forward ---------------------------------------------------
    print("\n" + "=" * 118)
    print(f"RULE 8 WALK-FORWARD — params chosen on {start.date()}..{IS_END} by IS Sharpe, evaluated {OOS_START}+")
    print("=" * 118)
    isr = grid.sort_values("isSharpe", ascending=False)
    print(isr[["book", "isSharpe"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    pick = isr.iloc[0]
    print(f"\nrule-8 selection: {pick['book']}  (IS Sharpe {pick['isSharpe']:.3f})")

    oos_tbl = pd.DataFrame([
        dict(book=f"SELECTED {pick['book']}", CAGR=pick["oCAGR"], Sharpe=pick["oSharpe"], MaxDD=pick["oMaxDD"]),
        dict(book="RULES v1 (live) OOS", CAGR=base["oCAGR"], Sharpe=base["oSharpe"], MaxDD=base["oMaxDD"]),
        dict(book="SPY OOS", CAGR=spy["oCAGR"], Sharpe=spy["oSharpe"], MaxDD=spy["oMaxDD"]),
    ])
    print()
    print(oos_tbl.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    rho = grid["isSharpe"].rank().corr(grid["oSharpe"].rank())     # Spearman without scipy
    print(f"\nSpearman(IS Sharpe, OOS Sharpe) across the 12 grid points: {rho:.3f}")

    # verdict ---------------------------------------------------------------
    n4a, n4b = int(grid["p4a"].sum()), int(grid["p4b"].sum())
    print("\n" + "=" * 118)
    print(f"KEEP path 4a passes: {n4a}/12    KEEP path 4b passes: {n4b}/12")
    print(f"4b bars from SPY: H1>{spy['H1']:.3f}  H2>{spy['H2']:.3f}  OOS>{spy['oSharpe']:.3f}  "
          f"MaxDD>={0.60 * spy['MaxDD']:.1%}  CAGR>={0.70 * spy['CAGR']:.1%}")
    print(f"4a bars from RULES v1: H1>{base['H1']:.3f}  H2>{base['H2']:.3f}  MaxDD>={base['MaxDD']:.1%}")
    fc = grid["fails"].value_counts()
    print("\n4b failure modes across the grid:")
    print(fc.to_string())

    # diagnostic A: the two 4b bars as a gross interval ----------------------
    # Sharpe is flat in g (idea 66), so g is a pure lever: CAGR rises with g and so
    # does MaxDD.  Solve for the g that meets each 4b bar at the best L and show
    # whether the interval is non-empty.  g > 1 is LEVERAGE, forbidden by PROTOCOL
    # rule 2 for this idea — reported only to locate the bar, never as a candidate.
    print("\n" + "=" * 118)
    print("DIAGNOSTIC A — 4b as a gross interval at L=60 (g>1.00 is leverage: NOT a candidate under rule 2)")
    print("=" * 118)
    dd_cap, cagr_floor = 0.60 * abs(spy["MaxDD"]), 0.70 * spy["CAGR"]
    drows = []
    for g in [0.40, 0.50, 0.55, 0.60, 0.75, 0.90, 1.00, 1.10, 1.25, 1.40]:
        r, to = run(px, lambda p, g=g: rp_weights(p, 60, g))
        d = full_halves_oos(r)
        a4, b4, _ = keep_paths(d, base, spy)
        drows.append(dict(g=g, CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"], turn=to,
                          DDok=abs(d["MaxDD"]) <= dd_cap, CAGRok=d["CAGR"] >= cagr_floor,
                          p4a=a4, p4b=b4, leverage=g > 1.0))
    dg = pd.DataFrame(drows)
    print(dg.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\n4b needs |MaxDD| <= {dd_cap:.1%} AND CAGR >= {cagr_floor:.1%} simultaneously.")
    ok = dg[dg["DDok"] & dg["CAGRok"]]
    print(f"grosses meeting BOTH: {list(ok['g']) if len(ok) else 'NONE — the interval is empty'}")
    a4g = list(dg[dg["p4a"]]["g"])
    print(f"grosses passing 4a: {a4g if a4g else 'NONE'}  <- 4a has no CAGR bar, so de-grossing buys the pass")
    if a4g:
        w = dg[dg["p4a"]].iloc[-1]
        print(f"  loosest 4a pass g={w['g']:.2f}: CAGR {w['CAGR']:.1%} vs live book {base['CAGR']:.1%} "
              f"— it passes 4a while earning LESS money than the book it replaces.")

    # diagnostic B: matched-drawdown comparison against the live book --------
    print("\n" + "=" * 118)
    print("DIAGNOSTIC B — at the live book's own drawdown, what does 23.6x/yr of turnover buy?")
    print("=" * 118)
    tgt = abs(base["MaxDD"])
    cand = dg.assign(err=(dg["MaxDD"].abs() - tgt).abs()).sort_values("err").iloc[0]
    r, to = run(px, lambda p, g=float(cand["g"]): rp_weights(p, 60, g))
    dm = full_halves_oos(r)
    mt = pd.DataFrame([
        dict(book=f"RP L=60 g={cand['g']:.2f} (DD-matched)", CAGR=dm["CAGR"], Sharpe=dm["Sharpe"],
             MaxDD=dm["MaxDD"], H1=dm["H1"], H2=dm["H2"], oSharpe=dm["oSharpe"], turn=to),
        dict(book="RULES v1 (live)", CAGR=base["CAGR"], Sharpe=base["Sharpe"], MaxDD=base["MaxDD"],
             H1=base["H1"], H2=base["H2"], oSharpe=base["oSharpe"], turn=ref["RULES v1 (live)"][1]),
    ])
    print(mt.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # diagnostic C: annual returns ------------------------------------------
    print("\n" + "=" * 118)
    print("DIAGNOSTIC C — calendar-year returns (%)")
    print("=" * 118)
    r75, _ = run(px, lambda p: rp_weights(p, 60, 0.75))
    ann = pd.DataFrame({
        "RP L=60 g=0.75": r75, "RULES v1": r_base, "SPY": spy_r,
    }).groupby(lambda d: d.year).apply(lambda x: (1 + x).prod() - 1) * 100
    print(ann.to_string(float_format=lambda x: f"{x:6.1f}"))

    # leaderboard rows ------------------------------------------------------
    print("\n" + "=" * 118)
    print("LEADERBOARD rows")
    print("=" * 118)
    script = Path(__file__).name
    today = pd.Timestamp("2026-09-04").date()
    for _, x in grid.iterrows():
        v = ("4a-pass, " if x["p4a"] else "") + ("4b-pass" if x["p4b"] else f"4b-fail({x['fails']})")
        print(f"| {today} | 19 {x['book']} | {x['CAGR']:.1%} | {x['Sharpe']:.2f} | {x['MaxDD']:.1%} | "
              f"{x['H1']:.2f} / {x['H2']:.2f} | {base['Sharpe']:.2f} ({base['H1']:.2f}/{base['H2']:.2f}) | "
              f"{v} | {script} |")
    for k in ("EW thirds (control)", "60/40 SPY-TLT (control)"):
        d = ref[k][0]
        a, b, f = keep_paths(d, base, spy)
        v = ("4a-pass, " if a else "") + ("4b-pass" if b else f"4b-fail({f})")
        print(f"| {today} | 19 {k} | {d['CAGR']:.1%} | {d['Sharpe']:.2f} | {d['MaxDD']:.1%} | "
              f"{d['H1']:.2f} / {d['H2']:.2f} | {base['Sharpe']:.2f} ({base['H1']:.2f}/{base['H2']:.2f}) | "
              f"{v} | {script} |")

    return grid, ref


def rp_weights_ew(px):
    return static_weights(px, {a: 1.0 / len(ASSETS) for a in ASSETS})


if __name__ == "__main__":
    main()
