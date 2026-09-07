#!/usr/bin/env python3
"""Idea 360 (cloud, 2026-09-07): price-the-U56-EWALL-MA-band-at-b=0.12-on-its-own.

QUESTION (queue text): idea 359's by-product -- hold every U56 name inside the 200d
+/-12% band at g/N, g=0.75, weekly -- clears 4b at 10 bps (CAGR 14.0%, Sharpe 1.226,
MaxDD -19.4%, H1 1.261 / H2 1.205, OOS 1.266 vs SPY 0.882) on only 1.93x/yr turnover,
but fails 4a and was measured INSIDE a census, not priced.  "Sweep b in
{0.08,0.12,0.16,0.20,0.25} x gross and run the breakeven c*; the band ladder is monotone
in b out to the widest point tested, so idea 240/256's grid-edge flag applies and must
be cleared first.  Max 2 params (b, gross)."

THE BOOK (fixed, never tuned)
-----------------------------
  keep_t = baseline.band_state(px, b) & px.notna()        (b = 0 -> the hard 200d gate)
  weekly rebalance (freq='W'), weights decided at close t applied at t+1 (engine),
  costs charged on realised turnover, warm-up 260 rows dropped.
Two WEIGHTING CONVENTIONS are carried side by side as a REPORTED axis (not a tuned
parameter -- both are printed at every grid point):
  RESPREAD  w_t = g / k_t on every kept name, k_t = |keep_t|.  Gross is always g while
            anything is in band.  This is idea 359's MAB-EWALL, the convention the
            queue's headline number was measured under.
  DEGROSS   w_t = g / N_t on every kept name, N_t = names PRICED that day.  Gated-out
            weight goes to cash and is never re-spread.  This is RULES v2's own
            convention (baseline.rules_v2_weights), gated equal to it at 0.000e+00.
The DEGROSS arm makes this idea a ONE-DIAL test of the LIVE rules: RULES v2 is exactly
DEGROSS at b = 0.03, g = 0.75, so the b ladder answers "should the live band be wider?"
directly, and the RESPREAD/DEGROSS pair prices the convention against it.

TUNED PARAMETERS: exactly 2.
  b in {0.00, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30, 0.40, 0.50, 0.70}
  g in {0.50, 0.60, 0.75, 0.85, 1.00}
Everything else (panel, weighting convention, cost rung, cadence) is a REPORTED axis:
every point printed and written to <slug>.grid.csv.

WHY THE b GRID RUNS TO 0.70.  The queue stops at 0.25 and flags idea 240/256: a dial
argmax read off a grid whose curve is still monotone at the widest point tested is a
grid EDGE, not an optimum, and is not reportable.  b is bounded above in a knowable way
-- band_state's hysteresis needs px > ma*(1+b) to ever enter, so as b grows the book
enters later, holds longer and eventually holds nothing -- so the curve MUST turn over
and the grid can be pushed until it does.  Section [B] reports, for every (panel, g),
whether the Sharpe argmax is INTERIOR or on an edge.

BREAKEVEN c* (section [C]).  engine.backtest's held weights and turnover do not depend
on cost_bps, so net returns are EXACTLY r(c) = r0 - tau*c/1e4 for any rung c and every
statistic below is derived from ONE 0-bps run per cell (gated at 0.000e+00 in [0]).
Three breakevens, all by bisection on c in [0, 600] bps:
  c*_abs  net Sharpe = 0
  c*_spy  net Sharpe = SPY's Sharpe over the same window   (SPY pays no turnover)
  c*_4b   the largest c at which ALL FIVE 4b bars still pass (0 if it fails at 0 bps)
c*_4b is the number that matters for capital: it says how much execution slippage the
KEEP survives.

PANELS (reported axis, not tuned): U56 (research/universe.json, the idea's own panel),
B136 (universe_broad.json) and SMALL439 (data/prices_small.csv, 44 tickers with
max_1d_move >= 1.0 dropped per data/small_meta.csv, leaving 439 names + SPY).  SURVIVORSHIP: B136 and SMALL are
CURRENT constituents of their screens -- both panels are survivorship-biased upward and
no number from them is a live expectation.  U56 carries the same caveat more weakly.

RULE 8 (section [E]).  (b, g) chosen on 2008-2016 by IS Sharpe at 10 bps, then 2017-2026
read ONCE.  Reported against: the b=0/g=0.75 do-nothing parent, the OOS-best cell
(regret), RULES v2 (live baseline) and SPY, with OOS CAGR / Sharpe / MaxDD for each.

KEEP paths: 4a (vs RULES v2) and 4b (vs SPY) at EVERY grid point and every rung.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_price-the-U56-EWALL-MA-band-at-b012-on-its-own_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, band_state, rules_v2_weights, rules_v1_weights  # noqa
from engine import backtest, metrics, rebalance_mask  # noqa

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)

SLUG = "2026-09-07_price-the-U56-EWALL-MA-band-at-b012-on-its-own_cloud"
OUT = ROOT / "research" / "backtests" / SLUG

FREQ = "W"
WARMUP = 260
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"

BS = [0.00, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30, 0.40, 0.50, 0.70]
GS = [0.50, 0.60, 0.75, 0.85, 1.00]
CONVS = ["RESPREAD", "DEGROSS"]             # reported axis, not tuned
PARENT = ("RESPREAD", 0.00, 0.75)           # the do-nothing hard-gate book
HEADLINE = ("RESPREAD", 0.12, 0.75)         # idea 359's committed cell
LIVE = ("DEGROSS", 0.03, 0.75)              # RULES v2 itself, inside the grid


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 "
          f"-> {len(keep) - 1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- book
def selection(px, b, drop_spy):
    keep = (band_state(px, b) if b > 0 else (px > px.rolling(200).mean())) & px.notna()
    if drop_spy and "SPY" in px.columns:
        keep = keep.copy(); keep["SPY"] = False
    return keep


def weights_from(sel, g, conv, priced):
    """RESPREAD: g/k_t over the kept names.  DEGROSS: g/N_t, N_t = names priced that day,
    so gated-out weight falls to cash and is never re-spread (RULES v2's convention)."""
    s = sel.astype(float)
    den = (s.sum(axis=1) if conv == "RESPREAD" else priced).replace(0, np.nan)
    return g * s.div(den, axis=0).fillna(0.0)


def fast_backtest(px, w, freq=FREQ):
    """Vectorised-loop clone of engine.backtest at 0 bps (gated in [0])."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT)
    cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * 0.0
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series((held > 1e-12).sum(axis=1), index=idx),
            pd.Series(held.sum(axis=1), index=idx))


# ---------------------------------------------------------------- stats / bars
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy, use_oos=True):
    """PROTOCOL rule 4b.  use_oos=False drops the OOS bar, which is undefined when the
    series IS the in-sample window (used only by the 4b-aware IS chooser in [E])."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    d = {"H1": h1 - s1, "H2": h2 - s2,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    if use_oos:
        d["OOS"] = (metrics(r.loc[OOS_START:])["Sharpe"] -
                    metrics(spy.loc[OOS_START:])["Sharpe"])
    f = [k for k, v in d.items() if not (v >= 0)]
    return (not f), d, f


def bars_4a(r, base):
    m, mb = metrics(r), metrics(base)
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": m["MaxDD"] - mb["MaxDD"]}
    f = [k for k, v in d.items() if not (v > 0 if k != "DD" else v >= 0)]
    return (not f), d, f


def bisect(fn, lo=0.0, hi=600.0, tol=1e-4):
    """Largest c in [lo,hi] with fn(c) True; fn monotone decreasing in truth."""
    if not fn(lo):
        return 0.0
    if fn(hi):
        return float("inf")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if fn(mid): lo = mid
        else: hi = mid
        if hi - lo < tol: break
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- [0] gates
def gate_engine(px, drop_spy):
    """fast_backtest must equal engine.backtest, and derived rungs must equal direct runs."""
    priced = px.notna().sum(axis=1)
    w = weights_from(selection(px, 0.12, drop_spy), 0.75, "RESPREAD", priced)
    r0, t0, _, _ = fast_backtest(px, w)
    ref = backtest(px, w, cost_bps=0, freq=FREQ)
    e1 = float(np.abs(r0 - ref["returns"]).max())
    e2 = float(np.abs(t0 - ref["turnover"]).max())
    ref25 = backtest(px, w, cost_bps=25, freq=FREQ)["returns"]
    e3 = float(np.abs((r0 - t0 * 25 / 1e4) - ref25).max())
    print(f"  G1 fast_backtest vs engine.backtest: returns {e1:.3e}  turnover {e2:.3e}")
    print(f"  G2 derived 25-bps rung vs direct backtest(cost_bps=25): {e3:.3e}")
    assert max(e1, e2, e3) < 1e-12, "engine gate failed"


def gate_degross(px):
    """The DEGROSS arm at (b, g) must BE baseline.rules_v2_weights(px, b, g)."""
    priced = px.notna().sum(axis=1)
    err = 0.0
    for b, g in [(0.03, 0.75), (0.12, 0.75), (0.20, 1.00)]:
        mine = weights_from(selection(px, b, False), g, "DEGROSS", priced)
        ref = rules_v2_weights(px, band=b, gross=g)
        err = max(err, float(np.abs(mine - ref).max().max()))
    print(f"  G3 DEGROSS arm == baseline.rules_v2_weights on 3 (b,g) cells: {err:.3e}")
    assert err < 1e-15, "de-gross gate failed"


def gate_reproduce(grid):
    """Reproduce idea 359's committed U56 MAB-EWALL rows at g=0.75."""
    f = ROOT / "research" / "backtests" / \
        "2026-09-07_census-how-many-band-rows-are-CONCENTRATION-changes_C.grid.csv"
    if not f.exists():
        print("  G3 idea 359 grid.csv not found -- reproduction gate SKIPPED"); return
    ref = pd.read_csv(f)
    ref = ref[(ref.family == "MAB-EWALL") & (ref.panel == "U56")].set_index("dial")
    mine = grid[(grid.panel == "U56") & (grid.g == 0.75) &
                (grid.conv == "RESPREAD")].set_index("b")
    cols = ["names", "turnover", "CAGR_10", "Sharpe_10", "MaxDD_10", "H1_10", "H2_10",
            "OOS_Sharpe_10"]
    common = [d for d in ref.index if d in mine.index]
    err = max(float(np.abs(ref.loc[common, c].values - mine.loc[common, c].values).max())
              for c in cols)
    print(f"  G4 reproduces idea 359's {len(common)} committed U56 MAB-EWALL rows "
          f"on {len(cols)} columns: max abs err {err:.3e}")
    assert err < 1e-9, "reproduction gate failed"


# ---------------------------------------------------------------- [A] sweep
def run_panel(name, px, drop_spy):
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    v2r, v2t = v2["returns"].loc[start:], v2["turnover"].loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)
    v1r, v1t = v1["returns"].loc[start:], v1["turnover"].loc[start:]

    rows, series = [], {}
    priced = px.notna().sum(axis=1)
    if drop_spy and "SPY" in px.columns:
        priced = priced - px["SPY"].notna().astype(int)
    sels = {b: selection(px, b, drop_spy) for b in BS}
    for conv in CONVS:
      for b in BS:
        for g in GS:
            r0, t0, nh, gr = fast_backtest(px, weights_from(sels[b], g, conv, priced))
            r0, t0, nh, gr = r0.loc[start:], t0.loc[start:], nh.loc[start:], gr.loc[start:]
            yrs = len(r0) / 252.0
            rec = dict(panel=name, conv=conv, b=b, g=g, names=float(nh.mean()),
                       gross=float(gr.mean()), turnover=float(t0.sum()) / yrs,
                       days_empty=float((nh == 0).mean()))
            for c in COSTS:
                r = r0 - t0 * c / 1e4
                m = metrics(r); h1, h2 = hs(r); mo = metrics(r.loc[OOS_START:])
                ok4b, d4b, f4b = bars_4b(r, spy)
                ok4a, d4a, f4a = bars_4a(r, v2r - v2t * c / 1e4)
                if rec["names"] <= 0 or not np.isfinite(m["Sharpe"]):
                    ok4a = ok4b = False; f4a = f4b = ["DEGENERATE"]
                rec.update({f"CAGR_{c}": m["CAGR"], f"Sharpe_{c}": m["Sharpe"],
                            f"MaxDD_{c}": m["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                            f"OOS_Sharpe_{c}": mo["Sharpe"], f"OOS_CAGR_{c}": mo["CAGR"],
                            f"OOS_MaxDD_{c}": mo["MaxDD"],
                            f"p4a_{c}": ok4a, f"f4a_{c}": ",".join(f4a),
                            f"p4b_{c}": ok4b, f"f4b_{c}": ",".join(f4b),
                            f"m4b_DD_{c}": d4b["DD"], f"m4b_CAGR_{c}": d4b["CAGR"],
                            f"m4b_H2_{c}": d4b["H2"], f"m4b_OOS_{c}": d4b["OOS"]})
            # ---- breakeven c*
            spy_S = metrics(spy)["Sharpe"]
            rec["cstar_abs"] = bisect(lambda c: metrics(r0 - t0 * c / 1e4)["Sharpe"] > 0)
            rec["cstar_spy"] = bisect(lambda c: metrics(r0 - t0 * c / 1e4)["Sharpe"] > spy_S)
            rec["cstar_4b"] = bisect(lambda c: bars_4b(r0 - t0 * c / 1e4, spy)[0])
            rows.append(rec)
            series[(name, conv, b, g)] = (r0, t0)
            print(f"    {name:9s} {conv:8s} b={b:<5g} g={g:<4g} names={rec['names']:6.2f} "
                  f"T={rec['turnover']:5.2f}x S10={rec['Sharpe_10']:+.4f} "
                  f"DD10={rec['MaxDD_10']:+.3f} 4a={rec['p4a_10']} 4b={rec['p4b_10']} "
                  f"c*4b={rec['cstar_4b']:.1f}")
    ms = metrics(spy); s1, s2 = hs(spy); mso = metrics(spy.loc[OOS_START:])
    ctx = dict(panel=name, start=str(start.date()), end=str(px.index[-1].date()),
               ncols=px.shape[1], nrows=len(px.loc[start:]),
               spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
               spy_H1=s1, spy_H2=s2, spy_OOS_Sharpe=mso["Sharpe"],
               spy_OOS_CAGR=mso["CAGR"], spy_OOS_MaxDD=mso["MaxDD"])
    for tag, (rr, tt) in (("v2", (v2r, v2t)), ("v1", (v1r, v1t))):
        for c in COSTS:
            r = rr - tt * c / 1e4
            m = metrics(r); h1, h2 = hs(r); mo = metrics(r.loc[OOS_START:])
            ctx.update({f"{tag}_{c}_CAGR": m["CAGR"], f"{tag}_{c}_Sharpe": m["Sharpe"],
                        f"{tag}_{c}_MaxDD": m["MaxDD"], f"{tag}_{c}_H1": h1,
                        f"{tag}_{c}_H2": h2, f"{tag}_{c}_OOS_Sharpe": mo["Sharpe"],
                        f"{tag}_{c}_OOS_CAGR": mo["CAGR"], f"{tag}_{c}_OOS_MaxDD": mo["MaxDD"]})
    series[(name, "CTL", "SPY", 0)] = (spy, spy * 0.0)
    series[(name, "CTL", "V2", 0)] = (v2r, v2t)
    return pd.DataFrame(rows), ctx, series


# ---------------------------------------------------------------- [B] grid-edge test
def edge_table(grid):
    out = []
    for (panel, conv, g), sub in grid.groupby(["panel", "conv", "g"]):
        sub = sub.sort_values("b")
        for c in COSTS:
            s = sub[f"Sharpe_{c}"].values
            bb = sub["b"].values
            i = int(np.nanargmax(s))
            # monotone check on the tail: is the last step still up?
            out.append(dict(panel=panel, conv=conv, g=g, bps=c, b_argmax=bb[i],
                            S_argmax=s[i], interior=bool(0 < i < len(bb) - 1),
                            edge="LOW" if i == 0 else ("HIGH" if i == len(bb) - 1 else ""),
                            last_step=s[-1] - s[-2], step_at_025=s[list(bb).index(0.25)] -
                            s[list(bb).index(0.20)],
                            S_at_012=s[list(bb).index(0.12)],
                            S_at_max_b=s[-1], drop_from_peak=s[i] - s[-1]))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- [E] rule 8
def walkforward(grid, series, ctx):
    rows = []
    for panel in grid.panel.unique():
        spy_r, _ = series[(panel, "CTL", "SPY", 0)]
        v2r, v2t = series[(panel, "CTL", "V2", 0)]
        for c in COSTS:
            IS, OOSs = {}, {}
            for conv in CONVS:
                for b in BS:
                    for g in GS:
                        r0, t0 = series[(panel, conv, b, g)]
                        r = r0 - t0 * c / 1e4
                        IS[(conv, b, g)] = metrics(r.loc[:IS_END])["Sharpe"]
                        OOSs[(conv, b, g)] = metrics(r.loc[OOS_START:])["Sharpe"]
            fin = lambda d, k: (d[k] if np.isfinite(d[k]) else -9e9)
            pick = max(IS, key=lambda k: fin(IS, k))
            best = max(OOSs, key=lambda k: fin(OOSs, k))
            # the 4b-aware chooser: best IS Sharpe among cells clearing 4b's four
            # IN-SAMPLE-computable bars (H1, H2, DD, CAGR; OOS is undefined in-sample)
            adm = [k for k in IS if bars_4b(
                (series[(panel, k[0], k[1], k[2])][0] -
                 series[(panel, k[0], k[1], k[2])][1] * c / 1e4).loc[:IS_END],
                spy_r.loc[:IS_END], use_oos=False)[0]]
            pick4b = max(adm, key=lambda k: fin(IS, k)) if adm else None
            arms = [("IS-pick", pick), ("OOS-best", best), ("parent b=0", PARENT),
                    ("headline b=0.12", HEADLINE), ("RULES v2 cell", LIVE)]
            if pick4b: arms.insert(1, ("IS-pick 4b-aware", pick4b))
            for tag, key in arms:
                r0, t0 = series[(panel, key[0], key[1], key[2])]
                o = (r0 - t0 * c / 1e4).loc[OOS_START:]
                m = metrics(o)
                rows.append(dict(panel=panel, bps=c, arm=tag, conv=key[0], b=key[1],
                                 g=key[2], IS_Sharpe=IS[key], OOS_Sharpe=m["Sharpe"],
                                 OOS_CAGR=m["CAGR"], OOS_MaxDD=m["MaxDD"],
                                 regret=OOSs[best] - m["Sharpe"]))
            for tag, (rr, tt) in (("RULES v2 (live)", (v2r, v2t)),
                                  ("SPY", (spy_r, spy_r * 0))):
                o = (rr - tt * c / 1e4).loc[OOS_START:]
                m = metrics(o)
                rows.append(dict(panel=panel, bps=c, arm=tag, conv="", b=np.nan, g=np.nan,
                                 IS_Sharpe=metrics((rr - tt * c / 1e4).loc[:IS_END])["Sharpe"],
                                 OOS_Sharpe=m["Sharpe"], OOS_CAGR=m["CAGR"],
                                 OOS_MaxDD=m["MaxDD"], regret=np.nan))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- main
def main():
    print("=" * 116)
    print("IDEA 360 - price the U56 EWALL MA band at b=0.12 on its own (b x gross, "
          "breakeven c*, grid-edge)")
    print("=" * 116)
    print(f"Book: hold every in-band name at g/k_t, weekly, next-day execution, "
          f"warm-up {WARMUP} rows.")
    print(f"Tuned axes (2): b in {BS}\n                g in {GS}")
    print(f"Reported axes: convention {CONVS}, panel {{U56,B136,SMALL439}}, "
          f"cost rung {COSTS} bps + continuous c*.\n")

    panels = [("U56", load_universe(), False),
              ("B136", load_universe(broad=True), False),
              ("SMALL439", small_panel(), True)]

    print("\n[0] GATES")
    gate_engine(panels[0][1], False)
    gate_degross(panels[0][1])

    grids, ctxs, series = [], [], {}
    for nm, px, ds in panels:
        print(f"\n[A] SWEEP {nm}  ({px.shape[1]} cols, {px.index[0].date()} -> "
              f"{px.index[-1].date()})")
        g_, c_, s_ = run_panel(nm, px, ds)
        grids.append(g_); ctxs.append(c_); series.update(s_)
    grid = pd.concat(grids, ignore_index=True)
    ctx = pd.DataFrame(ctxs)
    gate_reproduce(grid)

    OUTg = OUT.with_suffix("")
    grid.to_csv(f"{OUTg}.grid.csv", index=False)
    ctx.to_csv(f"{OUTg}.ctx.csv", index=False)

    print("\n" + "=" * 116)
    print("[CTX] panel context (SPY and the live baselines over each panel's own window)")
    print(ctx[["panel", "start", "end", "ncols", "spy_CAGR", "spy_Sharpe", "spy_MaxDD",
               "spy_H1", "spy_H2", "spy_OOS_Sharpe", "v2_10_Sharpe", "v2_10_CAGR",
               "v2_10_MaxDD", "v2_10_H1", "v2_10_H2", "v2_10_OOS_Sharpe"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 116)
    print("[A] FULL GRID at 10 bps (every point; the .grid.csv carries 0 and 25 bps too)")
    for panel in grid.panel.unique():
        for conv in CONVS:
            s = grid[(grid.panel == panel) & (grid.conv == conv)]
            print(f"\n  -- {panel} / {conv} --")
            for col in ("Sharpe_10", "CAGR_10", "MaxDD_10"):
                print(f"  {col}")
                print(s.pivot(index="b", columns="g", values=col)
                      .to_string(float_format=lambda x: f"{x:.4f}"))
            print("  mean names / realised gross / turnover x per yr (at g=0.75)")
            print(s[s.g == 0.75][["b", "names", "gross", "turnover", "days_empty"]]
                  .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 116)
    print("[B] GRID-EDGE TEST (idea 240/256): is the b argmax INTERIOR?")
    et = edge_table(grid)
    et.to_csv(f"{OUTg}.edge.csv", index=False)
    print(et.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    n_int = int(et.interior.sum())
    print(f"\n  INTERIOR argmax in {n_int} of {len(et)} (panel x g x rung) cells; "
          f"edges: {et[~et.interior].edge.value_counts().to_dict()}")

    print("\n" + "=" * 116)
    print("[C] BREAKEVEN c* (bps) -- net Sharpe = 0, = SPY, and the last rung 4b survives")
    for panel in grid.panel.unique():
        for conv in CONVS:
            s = grid[(grid.panel == panel) & (grid.conv == conv)]
            print(f"\n  -- {panel} / {conv} --  c*_4b")
            print(s.pivot(index="b", columns="g", values="cstar_4b")
                  .to_string(float_format=lambda x: f"{x:.1f}"))
            print("  c*_spy")
            print(s.pivot(index="b", columns="g", values="cstar_spy")
                  .to_string(float_format=lambda x: f"{x:.1f}"))

    print("\n" + "=" * 116)
    print("[D] KEEP PATHS at every grid point x rung")
    kp = []
    for c in COSTS:
        for panel in grid.panel.unique():
            for conv in CONVS:
                s = grid[(grid.panel == panel) & (grid.conv == conv)]
                kp.append(dict(panel=panel, conv=conv, bps=c, n_cells=len(s),
                               pass4a=int(s[f"p4a_{c}"].sum()),
                               pass4b=int(s[f"p4b_{c}"].sum()),
                               top_fail4b=s[f"f4b_{c}"].replace("", np.nan).dropna()
                               .str.split(",").explode().value_counts().to_dict()))
    kpd = pd.DataFrame(kp)
    kpd.to_csv(f"{OUTg}.keeppaths.csv", index=False)
    print(kpd.to_string(index=False))
    for c in COSTS:
        w = grid[grid[f"p4b_{c}"]]
        print(f"\n  4b PASSES at {c} bps ({len(w)}):")
        if len(w):
            print(w[["panel", "conv", "b", "g", f"CAGR_{c}", f"Sharpe_{c}", f"MaxDD_{c}",
                     f"H1_{c}", f"H2_{c}", f"OOS_Sharpe_{c}", "turnover", "cstar_4b"]]
                  .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n  4a PASSES at any rung: "
          f"{int(sum(grid[f'p4a_{c}'].sum() for c in COSTS))} of {len(grid) * len(COSTS)}")

    print("\n" + "=" * 116)
    print("[E] RULE 8 WALK-FORWARD -- (b,g) chosen on IS <= 2016, read once on 2017-2026")
    wf = walkforward(grid, series, ctx)
    wf.to_csv(f"{OUTg}.walkforward.csv", index=False)
    print(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 116)
    print("[F] THE THREE CELLS THAT MATTER, U56, all rungs")
    for tag, key in (("headline  RESPREAD b=0.12 g=0.75", HEADLINE),
                     ("live cell DEGROSS  b=0.03 g=0.75 (== RULES v2)", LIVE),
                     ("one dial  DEGROSS  b=0.12 g=0.75", ("DEGROSS", 0.12, 0.75)),
                     ("parent    RESPREAD b=0.00 g=0.75", PARENT)):
        h = grid[(grid.panel == "U56") & (grid.conv == key[0]) & (grid.b == key[1]) &
                 (grid.g == key[2])].iloc[0]
        print(f"\n  {tag}")
        for c in COSTS:
            print(f"    {c:2d} bps: CAGR {h[f'CAGR_{c}']:.4f}  Sharpe {h[f'Sharpe_{c}']:.4f}"
                  f"  MaxDD {h[f'MaxDD_{c}']:.4f}  H1 {h[f'H1_{c}']:.4f}  "
                  f"H2 {h[f'H2_{c}']:.4f}  OOS {h[f'OOS_Sharpe_{c}']:.4f}  "
                  f"4a {h[f'p4a_{c}']}  4b {h[f'p4b_{c}']}"
                  f"{'' if h[f'p4b_{c}'] else '  fail=' + str(h[f'f4b_{c}'])}")
        print(f"    turnover {h['turnover']:.3f}x/yr  mean names {h['names']:.2f}  "
              f"realised gross {h['gross']:.4f}  c*_4b {h['cstar_4b']:.1f} bps  "
              f"c*_spy {h['cstar_spy']:.1f} bps  c*_abs {h['cstar_abs']:.1f} bps")

    print("\n  CONVENTION DELTA (DEGROSS minus RESPREAD) at 10 bps, g=0.75, every panel x b:")
    piv = grid[grid.g == 0.75].pivot_table(index=["panel", "b"], columns="conv",
                                           values=["Sharpe_10", "CAGR_10", "MaxDD_10"])
    for col in ("Sharpe_10", "CAGR_10", "MaxDD_10"):
        piv[(col, "d")] = piv[(col, "DEGROSS")] - piv[(col, "RESPREAD")]
    print(piv.sort_index(axis=1).to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nWrote:", f"{OUTg}.grid.csv", f"{OUTg}.edge.csv", f"{OUTg}.keeppaths.csv",
          f"{OUTg}.walkforward.csv", f"{OUTg}.ctx.csv", sep="\n  ")


if __name__ == "__main__":
    main()
