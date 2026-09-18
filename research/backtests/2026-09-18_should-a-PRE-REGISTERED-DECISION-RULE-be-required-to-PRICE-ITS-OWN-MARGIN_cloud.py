#!/usr/bin/env python3
"""Idea 1283 (lane cloud, 2026-09-18) — should a PRE-REGISTERED DECISION RULE be
required to PRICE ITS OWN MARGIN?

Idea 1146's declared capital rule fired KEEP-4b-candidate on a +0.0009 in-sample Sharpe
margin, 16x inside 877's committed 0.0145 seed floor.  This run answers the question with
real books rather than with prose alone:

  CAPITAL LEG   84 real books (3 panels x 7 N x 4 gross), monthly, t+1 execution, 10 bps.
                Every grid point reported.  Both KEEP paths at every cell.  Rule 8: the
                dial is chosen on 2009-2016 in-sample Sharpe alone, 2017-2026 read ONCE.
  MARGIN LEG    For every choice set, the winner-minus-runner-up IS Sharpe margin is
                priced against ITS OWN noise floor (paired moving-block bootstrap, block
                63, B=400, fixed seed) and the OOS payoff of the pick is split by whether
                the margin cleared that floor.
  CENSUS LEG    Mechanical grep of the committed record for pre-declared decision rules
                that state a minimum margin at all.  Regexes printed.

Two tuned parameters only: N and gross.  Nothing else is searched.
Deterministic; run standalone:  python research/backtests/2026-09-18_should-a-PRE-...py
"""
import sys, re
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa: E402

OUT = Path(__file__).with_suffix("")
COST, FREQ, WARM = 10.0, "M", 260
NS = [5, 10, 15, 20, 25, 30, 40]
GROSSES = [0.50, 0.65, 0.80, 1.00]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
pd.set_option("display.width", 200)


# ---------------------------------------------------------------- fast runner
def fast_bt(px, w, cost_bps=COST, freq=FREQ):
    """Bit-for-bit transcription of engine.backtest's loop in numpy (incl. its row-0 /
    first-rebalance NaN).  Gated against engine.backtest below."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); port = np.empty(n); to = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new.copy()
        port[i] = cur @ rets[i] - to[i] * cost_bps / 1e4
        g = cur * (1 + rets[i]); tot = g.sum() + (1 - cur.sum())
        if tot > 0: cur = g / tot
    return pd.Series(port, index=px.index), pd.Series(to, index=px.index)


# ---------------------------------------------------------------- book family
def topn_weights(px, n, gross):
    """Top-n eligible by the v1 composite WITHOUT the vol scaler (the 2026-09-04 KEEP-4b
    book's selector), gross/n per name, gated-out weight to CASH (never re-spread)."""
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def legs(r, spy, v2):
    """Both KEEP paths for one return series against this panel's own SPY and RULES v2."""
    h = len(r) // 2
    rs = dict(CAGR=metrics(r)["CAGR"], S=metrics(r)["Sharpe"], DD=metrics(r)["MaxDD"],
              H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
              OOS_S=metrics(r.loc[OOS_START:])["Sharpe"],
              OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
              OOS_DD=metrics(r.loc[OOS_START:])["MaxDD"],
              IS_S=metrics(r.loc[:IS_END])["Sharpe"])
    hs = len(spy) // 2
    sp = dict(CAGR=metrics(spy)["CAGR"], S=metrics(spy)["Sharpe"], DD=metrics(spy)["MaxDD"],
              H1=metrics(spy.iloc[:hs])["Sharpe"], H2=metrics(spy.iloc[hs:])["Sharpe"],
              OOS_S=metrics(spy.loc[OOS_START:])["Sharpe"])
    hv = len(v2) // 2
    bv = dict(H1=metrics(v2.iloc[:hv])["Sharpe"], H2=metrics(v2.iloc[hv:])["Sharpe"],
              DD=metrics(v2)["MaxDD"])
    rs["p4a"] = bool(rs["H1"] > bv["H1"] and rs["H2"] > bv["H2"] and rs["DD"] >= bv["DD"])
    rs["p4b"] = bool(rs["H1"] > sp["H1"] and rs["H2"] > sp["H2"] and rs["OOS_S"] > sp["OOS_S"]
                     and rs["DD"] >= 0.60 * sp["DD"] and rs["CAGR"] >= 0.70 * sp["CAGR"])
    return rs


# ---------------------------------------------------------------- bootstrap
def sharpe(a):
    sd = a.std(ddof=1)
    return a.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def margin_floor(ra, rb, block=63, B=400, seed=1283):
    """Paired moving-block bootstrap SE of Sharpe(a) - Sharpe(b) on the IS window.
    Blocks are drawn ONCE per replicate and applied to both series (paired), so the SE is
    the noise floor of the MARGIN, not of either Sharpe."""
    a, b = np.asarray(ra), np.asarray(rb)
    n = len(a); nb = int(np.ceil(n / block))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n - block + 1, size=(B, nb))
    off = np.arange(block)
    d = np.empty(B)
    for i in range(B):
        idx = (starts[i][:, None] + off[None, :]).ravel()[:n]
        d[i] = sharpe(a[idx]) - sharpe(b[idx])
    return float(np.nanstd(d, ddof=1))


# ---------------------------------------------------------------- panels
def get_panels():
    out = {}
    out["U56"] = load_universe()
    out["B136"] = load_universe(broad=True)
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in ps.columns if c == "SPY" or c not in bad]
    print(f"SMALL: dropped {len(ps.columns) - len(keep)} tickers with max_1d_move >= 1.0 "
          f"(data/small_meta.csv); {len(keep) - 1} names + SPY benchmark remain")
    out["SMALL"] = ps[keep]
    return out


def main():
    panels = get_panels()

    # ---- GATE G1: fast runner == engine.backtest, post-warm-up
    print("\n=== GATE G1 — fast runner vs engine.backtest (post-warm-up) ===")
    for pn, n, g in [("U56", 20, 0.65), ("B136", 10, 1.00)]:
        px = panels[pn]; w = topn_weights(px, n, g)
        e = engine_backtest(px, w, cost_bps=COST, freq=FREQ)
        f, ft = fast_bt(px, w)
        s = px.index[WARM]
        dr = float((e["returns"].loc[s:] - f.loc[s:]).abs().max())
        dt = float((e["turnover"].loc[s:] - ft.loc[s:]).abs().max())
        print(f"  {pn} N={n} g={g:.2f}: max|d returns| {dr:.3e}   max|d turnover| {dt:.3e}")
        assert dr < 1e-12 and dt < 1e-12, "fast runner does not reproduce engine.backtest"

    # ---- benchmarks per panel
    bench = {}
    for pn, px in panels.items():
        s = px.index[WARM]
        v2, _ = fast_bt(px, rules_v2_weights(px), freq="W")
        spy = px["SPY"].pct_change().fillna(0.0).loc[s:]
        bench[pn] = (spy, v2.loc[s:])
        c, sh, dd = stats(spy); print(f"\n{pn} SPY   CAGR {c:.2%} Sharpe {sh:.4f} MaxDD {dd:.2%} "
                                     f"| OOS Sharpe {metrics(spy.loc[OOS_START:])['Sharpe']:.4f}")
        c, sh, dd = stats(v2.loc[s:]); print(f"{pn} RULESv2 CAGR {c:.2%} Sharpe {sh:.4f} MaxDD {dd:.2%} "
                                            f"| OOS Sharpe {metrics(v2.loc[s:].loc[OOS_START:])['Sharpe']:.4f}")

    # ---- CAPITAL LEG: every grid point
    rows, series = [], {}
    for pn, px in panels.items():
        s = px.index[WARM]; spy, v2 = bench[pn]
        for n in NS:
            for g in GROSSES:
                r, to = fast_bt(px, topn_weights(px, n, g))
                r = r.loc[s:]; series[(pn, n, g)] = r
                d = legs(r, spy, v2)
                d.update(panel=pn, N=n, gross=g, turn=float(to.loc[s:].sum() / (len(r) / 252)))
                rows.append(d)
    grid = pd.DataFrame(rows)[["panel", "N", "gross", "CAGR", "S", "DD", "H1", "H2",
                               "IS_S", "OOS_S", "OOS_CAGR", "OOS_DD", "turn", "p4a", "p4b"]]
    grid.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print("\n=== CAPITAL LEG — ALL 84 GRID POINTS (monthly, t+1, 10 bps) ===")
    print(grid.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n4a passes: {int(grid.p4a.sum())} of {len(grid)}   "
          f"4b passes (full+OOS legs): {int(grid.p4b.sum())} of {len(grid)}")
    for pn in panels:
        sub = grid[grid.panel == pn]
        print(f"   {pn}: 4a {int(sub.p4a.sum())}/{len(sub)}, 4b {int(sub.p4b.sum())}/{len(sub)}")

    # ---- MARGIN LEG (rule 8: choose on IS, read OOS once)
    sets = []
    for pn in panels:
        for g in GROSSES: sets.append((f"{pn}|gross={g:.2f}|dial=N", [(pn, n, g) for n in NS]))
        for n in NS: sets.append((f"{pn}|N={n}|dial=gross", [(pn, n, g) for g in GROSSES]))
    mrows = []
    for label, keys in sets:
        pn = keys[0][0]; spy, _ = bench[pn]
        iss = {k: metrics(series[k].loc[:IS_END])["Sharpe"] for k in keys}
        order = sorted(keys, key=lambda k: -iss[k])
        win, run = order[0], order[1]
        margin = iss[win] - iss[run]
        se = margin_floor(series[win].loc[:IS_END].values, series[run].loc[:IS_END].values)
        oos = {k: metrics(series[k].loc[OOS_START:])["Sharpe"] for k in keys}
        anchor = float(np.mean([oos[k] for k in keys]))
        mem = pd.DataFrame({str(k): series[k].loc[OOS_START:] for k in keys})
        cm = mem.corr().values
        corr_mean = float((cm.sum() - len(keys)) / (len(keys) * (len(keys) - 1)))
        mrows.append(dict(choice_set=label, winner=f"N={win[1]},g={win[2]:.2f}",
                          runner=f"N={run[1]},g={run[2]:.2f}", IS_margin=margin, floor_SE=se,
                          z=margin / se if se > 0 else np.nan,
                          OOS_win=oos[win], OOS_run=oos[run], OOS_anchor=anchor,
                          gain_vs_anchor=oos[win] - anchor, gain_vs_runner=oos[win] - oos[run],
                          IS_spread=max(iss.values()) - min(iss.values()), corr_mean=corr_mean,
                          dial="N" if label.endswith("dial=N") else "gross",
                          OOS_SPY=metrics(spy.loc[OOS_START:])["Sharpe"],
                          beats_SPY_OOS=bool(oos[win] > metrics(spy.loc[OOS_START:])["Sharpe"])))
    mg = pd.DataFrame(mrows)
    mg.to_csv(OUT.with_suffix(".margins.csv"), index=False)
    print("\n=== MARGIN LEG — every choice set, margin priced against its own floor ===")
    print(mg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n--- does the margin carry OOS information? ---")
    for lo, hi, name in [(-np.inf, 1.0, "z < 1 (inside floor)"), (1.0, 2.0, "1 <= z < 2"),
                         (2.0, np.inf, "z >= 2 (clears floor)")]:
        sub = mg[(mg.z >= lo) & (mg.z < hi)]
        if len(sub) == 0: print(f"  {name:22s} n=0"); continue
        print(f"  {name:22s} n={len(sub):3d}  mean gain vs anchor {sub.gain_vs_anchor.mean():+.4f}"
              f"  vs runner-up {sub.gain_vs_runner.mean():+.4f}"
              f"  beats SPY OOS {int(sub.beats_SPY_OOS.sum())}/{len(sub)}")
    ok = mg.dropna(subset=["z"])
    print(f"  rho(z, gain vs anchor)   = {ok.z.corr(ok.gain_vs_anchor):+.4f}  (n={len(ok)})")
    print(f"  rho(IS margin, gain)     = {ok.IS_margin.corr(ok.gain_vs_anchor):+.4f}")
    print(f"  median floor SE          = {ok.floor_SE.median():.4f}   "
          f"median |IS margin| = {ok.IS_margin.median():.4f}")
    print(f"  choice sets whose winning margin is INSIDE its own 1-SE floor: "
          f"{int((ok.z < 1).sum())} of {len(ok)}")
    print(f"  IS-pick beats the do-nothing anchor OOS in {int((mg.gain_vs_anchor > 0).sum())} "
          f"of {len(mg)} sets; beats SPY OOS in {int(mg.beats_SPY_OOS.sum())} of {len(mg)}")

    print("\n--- is the decisive group a DEGENERATE ladder? (record's 1214/1223 defect) ---")
    for dl in ("N", "gross"):
        sub = mg[mg.dial == dl]
        print(f"  dial={dl:5s} n={len(sub):2d}  mean IS Sharpe spread {sub.IS_spread.mean():.4f}"
              f"  mean pairwise OOS corr {sub.corr_mean.mean():.4f}"
              f"  mean z {sub.z.mean():.2f}  mean gain vs anchor {sub.gain_vs_anchor.mean():+.4f}")
    print("\n--- the margin gate AS A DEPLOYABLE CHOOSER (rule 8, OOS read once) ---")
    for thr in (0.0, 1.0, 2.0):
        g = [(r.OOS_win if r.z >= thr else r.OOS_anchor) for r in mg.itertuples()]
        n_fire = int((mg.z >= thr).sum())
        print(f"  gate z >= {thr:.1f}: fires {n_fire:2d}/{len(mg)} sets, mean OOS Sharpe {np.mean(g):.4f}")
    print(f"  do-nothing anchor (hold the whole choice set): mean OOS Sharpe {mg.OOS_anchor.mean():.4f}")
    print(f"  always take the IS-max pick:                   mean OOS Sharpe {mg.OOS_win.mean():.4f}")
    print(f"  panel SPY OOS Sharpe, set-weighted:            {mg.OOS_SPY.mean():.4f}")

    # ---- CENSUS LEG
    print("\n=== CENSUS LEG — committed pre-declared decision rules that state a margin ===")
    DECL = re.compile(r"pre-?(declar|register|stat)|declared (capital )?rule|decision rule", re.I)
    MARG = re.compile(r"(minimum|min\.?|at least|no less than|threshold|floor|margin)"
                      r"[^.\n]{0,80}(margin|Sharpe|difference|spread|SE\b)"
                      r"|margin of at least|by (at least )?[0-9]*\.[0-9]{3,}", re.I)
    files = [ROOT / "research" / "LEADERBOARD.md"] + sorted((ROOT / "research" / "backtests").glob("*.memo.md"))
    units = hits = withm = 0
    examples = []
    for f in files:
        for ln in f.read_text(errors="ignore").split("\n"):
            if not ln.strip(): continue
            units += 1
            if DECL.search(ln):
                hits += 1
                if MARG.search(ln):
                    withm += 1
                    if len(examples) < 5: examples.append(f"{f.name}: {ln.strip()[:150]}")
    print(f"  files scanned: {len(files)} (LEADERBOARD.md + {len(files)-1} memos)")
    print(f"  non-blank lines: {units}")
    print(f"  lines naming a pre-declared / decision rule: {hits}")
    print(f"  of those, lines ALSO naming a minimum margin / floor: {withm} "
          f"({withm/hits:.1%} of {hits})" if hits else "")
    for e in examples: print("   e.g. " + e)
    print("  regexes (reproducible):")
    print("    DECL =", DECL.pattern)
    print("    MARG =", MARG.pattern)

    with open(OUT.with_suffix(".census.txt"), "w") as fh:
        fh.write(f"files={len(files)} lines={units} decl={hits} decl_with_margin={withm}\n")
    print("\nWrote:", OUT.with_suffix(".grid.csv").name, OUT.with_suffix(".margins.csv").name)


if __name__ == "__main__":
    main()
