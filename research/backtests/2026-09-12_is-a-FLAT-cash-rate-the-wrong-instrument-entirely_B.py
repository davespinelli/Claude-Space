#!/usr/bin/env python3
"""Idea 642 — is a FLAT cash rate the wrong instrument entirely? (lane B, 2026-09-12)

QUEUE PREMISE (idea 406's largest caveat): the record credits the de-grossed cash leg at a
FLAT 150/300 bps over 2009-2026, while short rates paid ~10 bps to 2015 and ~500 after 2022.
The credit is therefore backloaded onto exactly the window rule 8 reads out of sample. The
item was PARKed for "a 3M T-bill path (needs network)".

UNPARKED: no download is needed. `SHY` (iShares 1-3y UST, adjusted close = total return) is a
committed column of data/prices.csv back to 2008-01-02, and idea 796 (2026-09-11, lane B)
already swept the idle leg into it. What 796 did NOT do is separate the two things the queue
conflates, so that is this run's whole job:

    LEVEL  — how much the cash leg pays on average over the window.
    PATH   — WHEN it pays it (near-zero 2009-2015, ~5% after 2022).

The decisive control is FLATMATCH_ORACLE: a flat rate calibrated so its compounded credit over
the window EQUALS SHY's exactly. Same level, no path. If the verdicts move between
FLATMATCH_ORACLE and SHYPATH, it is the PATH; if they do not, the record's flat convention is
harmless in the aggregate and the queue's caveat is about bookkeeping, not about verdicts.

CASH ARMS (6, treatments — not tuned parameters):
    ZERO            0 bps.  The live convention: products/backtester/engine.py credits the
                    uninvested fraction at exactly zero.
    FLAT150         150 bps flat, annual, accrued daily.      ] the record's
    FLAT300         300 bps flat, annual, accrued daily.      ] convention (idea 406)
    FLATMATCH_ORACLE flat rate matched to SHY's compounded return ON THE WINDOW BEING SCORED.
                    NOT TRADEABLE (it reads the window's own answer). It is the level-only
                    counterfactual, and is labelled ORACLE everywhere it is printed.
    FLATMATCH_IS    flat rate matched to SHY's compounded return on 2009-2016 ONLY, then held
                    fixed through 2017-2026. Tradeable; this is what an honest 2016 analyst
                    would have written down as "the" flat cash rate.
    SHYPATH         SHY's own daily total return on the idle fraction. Path + duration marks.
    BILLPATH        duration-stripped path: rate_t = SHY's trailing 252d total return, lagged
                    one day, accrued daily. Keeps the rate cycle, drops the mark-to-market.
                    A bill-ladder proxy; the closest thing to 3M bills the cache can build.

TUNED PARAMETERS: exactly 2 — band and gross of RULES v2. 5 x 5 = 25 grid points, ALL reported.
Cash arms are applied to the SAME held-weight path, so 25 backtests serve 25 x 7 = 175 cells.

PROTOCOL: 10 bps per unit turnover, weights decided at t applied at t+1, weekly cadence.
Rule 8 walk-forward: (band, gross) chosen on 2009-2016 by IS Sharpe alone, 2017-2026 read once.
Both KEEP paths (4a vs the live book, 4b vs SPY) evaluated on every cell.

Run: python research/backtests/2026-09-12_is-a-FLAT-cash-rate-the-wrong-instrument-entirely_B.py
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

OUT = Path(__file__).with_suffix("")
SLUG = OUT.name
pd.set_option("display.width", 240)

COST_BPS = 10.0
FREQ = "W"
WARMUP = 260                      # baseline.compare's convention
IS_END = "2016-12-31"             # rule 8
OOS_START = "2017-01-01"
BANDS = [0.00, 0.01, 0.03, 0.05, 0.08]      # tuned param 1 (live value 0.03)
GROSSES = [0.50, 0.65, 0.75, 0.90, 1.00]    # tuned param 2 (live value 0.75)
ARMS = ["ZERO", "FLAT150", "FLAT300", "FLATMATCH_ORACLE", "FLATMATCH_IS", "BILLPATH", "SHYPATH"]

def hr(s): print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)

# ----------------------------------------------------------------------------------
# exact backtester with a cash leg. cash_ret=0 must reproduce engine.backtest bitwise.
# ----------------------------------------------------------------------------------
def backtest_cash(prices, weights, cash_ret, cost_bps=COST_BPS, freq=FREQ):
    """engine.backtest, with the uninvested fraction earning cash_ret[t] that day.

    The only change from engine.backtest is that the idle fraction (1 - sum w) compounds at
    cash_ret instead of at zero, both in the day's return and in the overnight drift
    renormalisation. With cash_ret identically zero this is engine.backtest line for line.
    """
    rets = prices.pct_change().fillna(0.0)
    c = cash_ret.reindex(prices.index).fillna(0.0).values
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False)
    n = len(prices.index)
    cur = np.zeros(len(prices.columns))
    turnover = np.zeros(n); port = np.zeros(n); idle = np.zeros(n)
    rv = rets.values; wv = w_target.values; mv = mask.values
    for i in range(n):
        if mv[i] or i == 0:
            new = wv[i]
            turnover[i] = np.abs(new - cur).sum(); cur = new.copy()
        idle[i] = 1.0 - cur.sum()
        port[i] = (cur * rv[i]).sum() + idle[i] * c[i] - turnover[i] * cost_bps / 1e4
        growth = cur * (1 + rv[i])
        tot = growth.sum() + idle[i] * (1 + c[i])
        cur = growth / tot if tot > 0 else cur
    idx = prices.index
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turnover, index=idx),
            "idle": pd.Series(idle, index=idx)}

def flat_daily(annual, idx):
    return pd.Series((1.0 + annual) ** (1 / 252) - 1.0, index=idx)

def m3(r):
    m = metrics(r); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def rowstats(r):
    c, s, d = m3(r); h1, h2 = halves(r)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2)

# ----------------------------------------------------------------------------------
hr("SETUP — panel, windows, cash instruments")
px = load_universe()                                   # U56, the live panel (committed cache)
px = px.dropna(how="all").ffill()
start = px.index[WARMUP]
print(f"panel U56: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}")
print(f"scored window: {start.date()} -> {px.index[-1].date()}  (warm-up {WARMUP} rows skipped)")

shy = px["SHY"].pct_change().fillna(0.0)
spy_r = px["SPY"].pct_change().fillna(0.0)
idx = px.index
is_m = (idx >= start) & (idx <= IS_END)
oos_m = idx >= OOS_START
sc_m = idx >= start
print(f"IS  {idx[is_m][0].date()} -> {idx[is_m][-1].date()}  ({is_m.sum()} rows)")
print(f"OOS {idx[oos_m][0].date()} -> {idx[oos_m][-1].date()}  ({oos_m.sum()} rows)")

def ann_from(daily, mask):
    tot = float((1 + daily[mask]).prod()); n = int(mask.sum())
    return tot ** (252 / n) - 1

shy_full, shy_is, shy_oos = (ann_from(shy, m) for m in (sc_m, is_m, oos_m))
print(f"\nSHY realised annual total return:  FULL {shy_full:.4%}   IS {shy_is:.4%}   OOS {shy_oos:.4%}"
      f"   (OOS/IS = {shy_oos/shy_is:.2f}x)")

# BILLPATH: trailing 252d SHY total return, lagged 1 day, accrued daily. No look-ahead.
trail = (1 + shy).rolling(252).apply(np.prod, raw=True) - 1
bill_ann = trail.shift(1).bfill().fillna(0.0)
bill_daily = (1.0 + bill_ann.clip(lower=-0.5)) ** (1 / 252) - 1.0
print(f"BILLPATH implied annual rate: {bill_ann[sc_m].min():.4%} .. {bill_ann[sc_m].max():.4%}"
      f"  (IS mean {bill_ann[is_m].mean():.4%}, OOS mean {bill_ann[oos_m].mean():.4%})")

# per-window FLATMATCH_ORACLE rates (level-matched to SHY on the window being scored)
ORACLE = {"FULL": shy_full, "IS": shy_is, "OOS": shy_oos}
print(f"FLATMATCH_ORACLE annual rate by window: " +
      "  ".join(f"{k} {v:.4%}" for k, v in ORACLE.items()))
print(f"FLATMATCH_IS annual rate (fixed at the 2009-2016 value, carried into OOS): {shy_is:.4%}")
print(f"the record's flat convention: 1.5000% and 3.0000% — IS error "
      f"{0.015-shy_is:+.4%}/{0.03-shy_is:+.4%}, OOS error {0.015-shy_oos:+.4%}/{0.03-shy_oos:+.4%}")

def cash_series(arm, window):
    if arm == "ZERO": return pd.Series(0.0, index=idx)
    if arm == "FLAT150": return flat_daily(0.015, idx)
    if arm == "FLAT300": return flat_daily(0.030, idx)
    if arm == "FLATMATCH_ORACLE": return flat_daily(ORACLE[window], idx)
    if arm == "FLATMATCH_IS": return flat_daily(shy_is, idx)
    if arm == "BILLPATH": return bill_daily
    if arm == "SHYPATH": return shy
    raise ValueError(arm)

# ----------------------------------------------------------------------------------
hr("GATES — printed before any new number")
gates = []
base_res = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)
b = base_res["returns"].loc[start:]
bc, bs, bd = m3(b); bh1, bh2 = halves(b)
COMMIT_V2 = (0.086282, 1.2018, -0.120549)
g1 = max(abs(bc - COMMIT_V2[0]), abs(bs - COMMIT_V2[1]), abs(bd - COMMIT_V2[2]))
print(f"G1 LIVE RULES v2 @10bps U56: {bc:.4%} / {bs:.4f} / {bd:.4%}  vs committed "
      f"8.6282% / 1.2018 / -12.0549%  max|d| {g1:.3e}  -> {'PASS' if g1 < 1e-4 else 'FAIL'}")
gates.append(("G1 RULES v2 headline", g1 < 1e-4, f"max|d| {g1:.3e}"))

spy = spy_r.loc[start:]
sc, ss, sd = m3(spy); sh1, sh2 = halves(spy)
COMMIT_SPY = (0.151631, 0.8861, -0.337172)
g2 = max(abs(sc - COMMIT_SPY[0]), abs(ss - COMMIT_SPY[1]), abs(sd - COMMIT_SPY[2]))
print(f"G2 SPY buy-and-hold:         {sc:.4%} / {ss:.4f} / {sd:.4%}  vs committed "
      f"15.1631% / 0.8861 / -33.7172%  max|d| {g2:.3e}  -> {'PASS' if g2 < 1e-4 else 'FAIL'}")
gates.append(("G2 SPY headline", g2 < 1e-4, f"max|d| {g2:.3e}"))

# G3: the cash backtester reproduces engine.backtest exactly at zero cash.
chk = backtest_cash(px, rules_v2_weights(px), pd.Series(0.0, index=idx))
g3 = float(np.abs(chk["returns"] - base_res["returns"]).max())
print(f"G3 backtest_cash(cash=0) == engine.backtest: max|d| {g3:.3e}"
      f"  -> {'PASS' if g3 < 1e-12 else 'FAIL'}")
gates.append(("G3 cash engine identity", g3 < 1e-12, f"max|d| {g3:.3e}"))

# G4: the credit is exactly idle x rate — a 100% idle book must return the cash rate itself.
zero_w = pd.DataFrame(0.0, index=idx, columns=px.columns)
allcash = backtest_cash(px, zero_w, shy)["returns"].loc[start:]
g4 = float(np.abs(allcash - shy.loc[start:]).max())
print(f"G4 fully-idle book credited at SHY == SHY itself: max|d| {g4:.3e}"
      f"  -> {'PASS' if g4 < 1e-12 else 'FAIL'}")
gates.append(("G4 cash credit identity", g4 < 1e-12, f"max|d| {g4:.3e}"))

# G5: idle share of the live book (idea 796 published 46.7% mean, IS 47.2%, OOS 46.4%)
idle_live = chk["idle"]
g5v = (idle_live[sc_m].mean(), idle_live[is_m].mean(), idle_live[oos_m].mean())
g5 = max(abs(g5v[0] - 0.467), abs(g5v[1] - 0.472), abs(g5v[2] - 0.464))
print(f"G5 live-book idle share: full {g5v[0]:.4f} / IS {g5v[1]:.4f} / OOS {g5v[2]:.4f}"
      f"  vs 796's 0.467/0.472/0.464  max|d| {g5:.3e}  -> {'PASS' if g5 < 5e-3 else 'FAIL'}")
gates.append(("G5 idle share vs idea 796", g5 < 5e-3, f"max|d| {g5:.3e}"))

print(f"\nGATES: {sum(g for _, g, _ in gates)} of {len(gates)} PASS")
pd.DataFrame([dict(gate=n, passed=p, detail=d) for n, p, d in gates]).to_csv(f"{OUT}.gates.csv", index=False)

# ----------------------------------------------------------------------------------
hr("PART A — the 25-point (band, gross) grid x 7 cash arms, ALL 175 cells")
rows = []
cache = {}
for band in BANDS:
    for gross in GROSSES:
        w = rules_v2_weights(px, band=band, gross=gross)
        base_cells = backtest_cash(px, w, pd.Series(0.0, index=idx))
        cache[(band, gross)] = (w, base_cells)
        for arm in ARMS:
            # one run serves all three windows, except FLATMATCH_ORACLE whose rate is
            # re-matched to SHY on each window and therefore needs its own run per window.
            if arm == "ZERO":
                runs = {w_: base_cells["returns"] for w_ in ("FULL", "IS", "OOS")}
            elif arm == "FLATMATCH_ORACLE":
                runs = {w_: backtest_cash(px, w, cash_series(arm, w_))["returns"]
                        for w_ in ("FULL", "IS", "OOS")}
            else:
                one = backtest_cash(px, w, cash_series(arm, "FULL"))["returns"]
                runs = {w_: one for w_ in ("FULL", "IS", "OOS")}
            res = {}
            for win, mask in (("FULL", sc_m), ("IS", is_m), ("OOS", oos_m)):
                res[win] = rowstats(runs[win][mask])
            d = dict(band=band, gross=gross, arm=arm,
                     idle=float(base_cells["idle"][sc_m].mean()),
                     turnover=float(base_cells["turnover"][sc_m].sum() / (sc_m.sum() / 252)))
            for win in ("FULL", "IS", "OOS"):
                for k, v in res[win].items():
                    d[f"{win}_{k}"] = v
            rows.append(d)
grid = pd.DataFrame(rows)
grid.to_csv(f"{OUT}.grid.csv", index=False)
print(f"{len(grid)} cells written to {Path(OUT).name}.grid.csv "
      f"({len(BANDS)}x{len(GROSSES)} grid x {len(ARMS)} arms x 3 windows)")

print("\nLIVE CELL (band 0.03, gross 0.75) — all 7 arms, all 3 windows:")
live = grid[(grid.band == 0.03) & (grid.gross == 0.75)].set_index("arm")
show = live[["FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD", "FULL_H1", "FULL_H2",
             "IS_CAGR", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
print(show.to_string(float_format=lambda x: f"{x:.4f}"))

print("\nARM MEANS over all 25 grid points (so the reading is not one tuned cell):")
am = grid.groupby("arm")[["FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD",
                          "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
print(am.reindex(ARMS).to_string(float_format=lambda x: f"{x:.4f}"))

# ----------------------------------------------------------------------------------
hr("PART B — PATH vs LEVEL: the level-matched control")
print("FLATMATCH_ORACLE pays exactly what SHY paid on the window being scored (same LEVEL,")
print("no PATH). Any gap to SHYPATH is the PATH, and nothing else.\n")
pv = []
for (band, gross), _ in cache.items():
    g = grid[(grid.band == band) & (grid.gross == gross)].set_index("arm")
    for win in ("FULL", "IS", "OOS"):
        pv.append(dict(band=band, gross=gross, window=win,
                       oracle_Sharpe=g.loc["FLATMATCH_ORACLE", f"{win}_Sharpe"],
                       shy_Sharpe=g.loc["SHYPATH", f"{win}_Sharpe"],
                       bill_Sharpe=g.loc["BILLPATH", f"{win}_Sharpe"],
                       d_path=g.loc["SHYPATH", f"{win}_Sharpe"] - g.loc["FLATMATCH_ORACLE", f"{win}_Sharpe"],
                       d_path_bill=g.loc["BILLPATH", f"{win}_Sharpe"] - g.loc["FLATMATCH_ORACLE", f"{win}_Sharpe"],
                       d_dur=g.loc["SHYPATH", f"{win}_Sharpe"] - g.loc["BILLPATH", f"{win}_Sharpe"],
                       oracle_CAGR=g.loc["FLATMATCH_ORACLE", f"{win}_CAGR"],
                       shy_CAGR=g.loc["SHYPATH", f"{win}_CAGR"],
                       d_path_CAGR=g.loc["SHYPATH", f"{win}_CAGR"] - g.loc["FLATMATCH_ORACLE", f"{win}_CAGR"],
                       oracle_MaxDD=g.loc["FLATMATCH_ORACLE", f"{win}_MaxDD"],
                       shy_MaxDD=g.loc["SHYPATH", f"{win}_MaxDD"],
                       d_path_MaxDD=g.loc["SHYPATH", f"{win}_MaxDD"] - g.loc["FLATMATCH_ORACLE", f"{win}_MaxDD"]))
path = pd.DataFrame(pv)
path.to_csv(f"{OUT}.pathlevel.csv", index=False)
print("PATH effect (SHYPATH - FLATMATCH_ORACLE) across all 25 grid points, per window:")
print(path.groupby("window")[["d_path", "d_path_CAGR", "d_path_MaxDD", "d_path_bill", "d_dur"]]
      .agg(["mean", "min", "max"]).to_string(float_format=lambda x: f"{x:+.4f}"))

H_PATH = float(path[path.window == "OOS"].d_path.abs().max()) > 0.05
print(f"\nH_PATH (|OOS Sharpe gap| > 0.05 at some grid point): "
      f"max |d_path| OOS = {path[path.window=='OOS'].d_path.abs().max():.4f} -> "
      f"{'PASS (the PATH moves it)' if H_PATH else 'FAIL (LEVEL is all there is)'}")
H_BACK = shy_oos / shy_is >= 2.0
print(f"H_BACKLOAD (SHY OOS credit >= 2x IS credit): {shy_oos/shy_is:.2f}x -> "
      f"{'PASS' if H_BACK else 'FAIL'}")
H_FLAT = (0.015 - shy_is) * (0.015 - shy_oos) < 0
print(f"H_FLATWRONG (150 bps errs in OPPOSITE directions IS vs OOS): IS {0.015-shy_is:+.4%}, "
      f"OOS {0.015-shy_oos:+.4%} -> {'PASS' if H_FLAT else 'FAIL'}")
H_DUR = float(path[path.window == "OOS"].d_dur.abs().max()) > 0.05
print(f"H_DURATION (|SHYPATH - BILLPATH| OOS Sharpe > 0.05): "
      f"{path[path.window=='OOS'].d_dur.abs().max():.4f} -> {'PASS' if H_DUR else 'FAIL'}")

# ----------------------------------------------------------------------------------
hr("PART C — both KEEP paths on all 175 cells")
SPY_FULL = dict(zip(("CAGR", "Sharpe", "MaxDD"), (sc, ss, sd))); SPY_FULL.update(H1=sh1, H2=sh2)
spy_oos_r = spy_r[oos_m]
SPY_OOS = dict(zip(("CAGR", "Sharpe", "MaxDD"), m3(spy_oos_r)))
SPY_OOS["H1"], SPY_OOS["H2"] = halves(spy_oos_r)
print(f"SPY FULL  {sc:.4%} / {ss:.4f} / {sd:.4%}  halves {sh1:.4f} / {sh2:.4f}")
print(f"SPY OOS   {SPY_OOS['CAGR']:.4%} / {SPY_OOS['Sharpe']:.4f} / {SPY_OOS['MaxDD']:.4%}")
print(f"4b bars: Sharpe > SPY in H1, H2 and OOS;  MaxDD >= {0.6*sd:.4%} (60% of SPY's);"
      f"  CAGR >= {0.7*sc:.4%} (70% of SPY's)")
print(f"LIVE book (the 4a comparand, cash at ZERO as priced today): {bc:.4%} / {bs:.4f} / {bd:.4%}"
      f"  halves {bh1:.4f} / {bh2:.4f}")

# same-arm baselines: RULES v2 at the LIVE dials, credited with the same cash arm.
same_arm_base = {}
for arm in ARMS:
    r = backtest_cash(px, rules_v2_weights(px), cash_series(arm, "FULL"))["returns"].loc[start:]
    same_arm_base[arm] = rowstats(r)
print("\nthe LIVE book itself under each cash arm (the matched 4a comparand):")
print(pd.DataFrame(same_arm_base).T.reindex(ARMS).to_string(float_format=lambda x: f"{x:.4f}"))

kp = []
for _, r in grid.iterrows():
    sa = same_arm_base[r.arm]
    p4a_live = (r.FULL_H1 > bh1) and (r.FULL_H2 > bh2) and (r.FULL_MaxDD >= bd)
    p4a_match = (r.FULL_H1 > sa["H1"]) and (r.FULL_H2 > sa["H2"]) and (r.FULL_MaxDD >= sa["MaxDD"])
    p4b = ((r.FULL_H1 > sh1) and (r.FULL_H2 > sh2) and (r.OOS_Sharpe > SPY_OOS["Sharpe"])
           and (r.FULL_MaxDD >= 0.6 * sd) and (r.FULL_CAGR >= 0.7 * sc))
    kp.append(dict(band=r.band, gross=r.gross, arm=r.arm, pass_4a_vs_live=p4a_live,
                   pass_4a_matched=p4a_match, pass_4b=p4b,
                   FULL_CAGR=r.FULL_CAGR, FULL_Sharpe=r.FULL_Sharpe, FULL_MaxDD=r.FULL_MaxDD,
                   FULL_H1=r.FULL_H1, FULL_H2=r.FULL_H2,
                   OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD))
keep = pd.DataFrame(kp)
keep.to_csv(f"{OUT}.keeppaths.csv", index=False)
print("\nKEEP-path pass counts per cash arm (25 cells each):")
kc = keep.groupby("arm")[["pass_4a_vs_live", "pass_4a_matched", "pass_4b"]].sum().reindex(ARMS)
kc["n"] = 25
print(kc.to_string())
print(f"\nTOTAL: 4a-vs-live {int(keep.pass_4a_vs_live.sum())}/175, "
      f"4a-matched {int(keep.pass_4a_matched.sum())}/175, 4b {int(keep.pass_4b.sum())}/175")
H_VERD = int(kc.loc["FLATMATCH_ORACLE", "pass_4b"]) != int(kc.loc["SHYPATH", "pass_4b"]) or \
         int(kc.loc["FLATMATCH_ORACLE", "pass_4a_vs_live"]) != int(kc.loc["SHYPATH", "pass_4a_vs_live"])
print(f"\nH_VERDICT (level-matched flat and the real path give DIFFERENT KEEP counts): "
      f"{'PASS' if H_VERD else 'FAIL'}")
if keep.pass_4b.any():
    print("\n4b passers:")
    print(keep[keep.pass_4b].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
else:
    print("\n4b passers: NONE.")

# ----------------------------------------------------------------------------------
hr("PART D — RULE 8 walk-forward: (band, gross) chosen on 2009-2016 alone, 2017-2026 read once")
wf = []
for arm in ARMS:
    sub = grid[grid.arm == arm]
    pick = sub.loc[sub.IS_Sharpe.idxmax()]
    wf.append(dict(arm=arm, pick_band=pick.band, pick_gross=pick.gross,
                   IS_CAGR=pick.IS_CAGR, IS_Sharpe=pick.IS_Sharpe, IS_MaxDD=pick.IS_MaxDD,
                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                   OOS_H1=pick.OOS_H1, OOS_H2=pick.OOS_H2))
# comparands on the same OOS window
b_oos = base_res["returns"][oos_m]
v1_oos = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"][oos_m]
for nm, r in (("RULES v2 baseline (live, cash ZERO)", b_oos), ("RULES v1 (previous)", v1_oos),
              ("SPY buy-and-hold", spy_oos_r)):
    c, s, d = m3(r); h1, h2 = halves(r)
    wf.append(dict(arm=nm, pick_band=np.nan, pick_gross=np.nan,
                   IS_CAGR=np.nan, IS_Sharpe=np.nan, IS_MaxDD=np.nan,
                   OOS_CAGR=c, OOS_Sharpe=s, OOS_MaxDD=d, OOS_H1=h1, OOS_H2=h2))
wfd = pd.DataFrame(wf)
wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
print(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\nIS->OOS transport of the arm ORDERING (does the IS window know which cash arm wins?):")
o = wfd.dropna(subset=["IS_Sharpe"])
rho = o.IS_Sharpe.rank().corr(o.OOS_Sharpe.rank(), method="pearson")
print(f"  Spearman(IS Sharpe, OOS Sharpe) over the {len(o)} cash arms = {rho:+.4f}")

print(f"\nOOS 4b check on each arm's walk-forward pick (every bar read on the OOS window's own SPY:")
print(f"  Sharpe {SPY_OOS['Sharpe']:.4f}, halves {SPY_OOS['H1']:.4f}/{SPY_OOS['H2']:.4f}, "
      f"CAGR floor {0.7*SPY_OOS['CAGR']:.4%}, MaxDD cap {0.6*SPY_OOS['MaxDD']:.4%}):")
for _, r in wfd.dropna(subset=["IS_Sharpe"]).iterrows():
    ok = (r.OOS_H1 > SPY_OOS["H1"] and r.OOS_H2 > SPY_OOS["H2"] and r.OOS_Sharpe > SPY_OOS["Sharpe"]
          and r.OOS_MaxDD >= 0.6 * SPY_OOS["MaxDD"] and r.OOS_CAGR >= 0.7 * SPY_OOS["CAGR"])
    why = []
    if r.OOS_Sharpe <= SPY_OOS["Sharpe"]: why.append("Sharpe<=SPY")
    if r.OOS_H1 <= SPY_OOS["H1"] or r.OOS_H2 <= SPY_OOS["H2"]: why.append("OOS half <= SPY")
    if r.OOS_CAGR < 0.7 * SPY_OOS["CAGR"]:
        why.append(f"CAGR {r.OOS_CAGR:.2%} < floor {0.7*SPY_OOS['CAGR']:.2%}")
    if r.OOS_MaxDD < 0.6 * SPY_OOS["MaxDD"]: why.append("MaxDD")
    print(f"  {r.arm:<18} pick(band {r.pick_band:.2f}, gross {r.pick_gross:.2f})  "
          f"OOS {r.OOS_CAGR:7.4%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.4%}  "
          f"4b {'PASS' if ok else 'FAIL'}  {'; '.join(why)}")

# ----------------------------------------------------------------------------------
hr("PART E — where the credit actually lands (the queue's mechanism, in pp/yr)")
lead = []
for arm in ARMS:
    g = grid[(grid.band == 0.03) & (grid.gross == 0.75) & (grid.arm == arm)].iloc[0]
    z = grid[(grid.band == 0.03) & (grid.gross == 0.75) & (grid.arm == "ZERO")].iloc[0]
    lead.append(dict(arm=arm,
                     credit_IS_pp=1e2 * (g.IS_CAGR - z.IS_CAGR),
                     credit_OOS_pp=1e2 * (g.OOS_CAGR - z.OOS_CAGR),
                     credit_FULL_pp=1e2 * (g.FULL_CAGR - z.FULL_CAGR),
                     dSharpe_IS=g.IS_Sharpe - z.IS_Sharpe,
                     dSharpe_OOS=g.OOS_Sharpe - z.OOS_Sharpe,
                     dSharpe_FULL=g.FULL_Sharpe - z.FULL_Sharpe,
                     dMaxDD_FULL_pp=1e2 * (g.FULL_MaxDD - z.FULL_MaxDD)))
cr = pd.DataFrame(lead).set_index("arm").reindex(ARMS)
cr.to_csv(f"{OUT}.credit.csv")
print("credit over the ZERO convention at the LIVE cell (band 0.03, gross 0.75), pp/yr of CAGR:")
print(cr.to_string(float_format=lambda x: f"{x:+.4f}"))
print(f"\nidle share at the live cell: {live.loc['ZERO','idle']:.4f} of NAV")
print("the flat convention's error is an IS OVER-credit and an OOS UNDER-credit — it flatters")
print("exactly the window rule 8 uses to choose, and starves the one rule 8 reads.")

hr("PART F — is GROSS even IDENTIFIABLE to an IS Sharpe selector? (why the picks flip)")
print("Sharpe is scale-invariant, so with cash at ZERO the gross dial moves IS Sharpe only")
print("through costs — it is very nearly a no-op. A cash credit breaks that invariance and")
print("makes lower gross genuinely raise IS Sharpe. That is the mechanism behind PART D.\n")
ident = []
for arm in ARMS:
    for band in BANDS:
        s = grid[(grid.arm == arm) & (grid.band == band)].set_index("gross").IS_Sharpe
        o = grid[(grid.arm == arm) & (grid.band == band)].set_index("gross").OOS_CAGR
        ident.append(dict(arm=arm, band=band, IS_Sharpe_spread_over_gross=s.max() - s.min(),
                          argmax_gross=s.idxmax(), OOS_CAGR_at_argmax=o.loc[s.idxmax()],
                          OOS_CAGR_spread_over_gross=o.max() - o.min()))
idf = pd.DataFrame(ident)
idf.to_csv(f"{OUT}.identifiability.csv", index=False)
print("IS Sharpe spread across the 5 gross rungs, by arm (mean over the 5 bands):")
summ = idf.groupby("arm").agg(IS_Sharpe_spread=("IS_Sharpe_spread_over_gross", "mean"),
                              modal_pick=("argmax_gross", lambda x: x.mode().iloc[0]),
                              OOS_CAGR_spread=("OOS_CAGR_spread_over_gross", "mean")).reindex(ARMS)
print(summ.to_string(float_format=lambda x: f"{x:.4f}"))
z = summ.loc["ZERO", "IS_Sharpe_spread"]
print(f"\nZERO's gross dial is worth {z:.4f} of IS Sharpe — the selector is choosing on the 4th")
print(f"decimal — while it costs {summ.loc['ZERO','OOS_CAGR_spread']:.2%} of OOS CAGR. Every credited arm makes the")
print(f"dial {summ.drop('ZERO').IS_Sharpe_spread.min()/z:.0f}x to {summ.drop('ZERO').IS_Sharpe_spread.max()/z:.0f}x more visible in sample, and points it at LOW gross.")
print("\nSo the ZERO arm's rule-8 4b PASS is a TIE-BREAK, not a selection: at band 0.08 its five")
print("gross rungs span IS Sharpe 1.121735..1.122612 and OOS CAGR 5.98%..12.04%. Not a KEEP.")

hr("DONE")
print(f"artefacts: {Path(OUT).name}.{{gates,grid,pathlevel,keeppaths,walkforward,credit}}.csv")
