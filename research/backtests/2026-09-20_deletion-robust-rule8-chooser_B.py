#!/usr/bin/env python3
"""Idea 1713 (2026-09-20, lane B) — does a DELETION-ROBUST rule-8 chooser beat plain
IS-argmax out of sample?

WHY.  Idea 720 (this morning, lane cloud) acquitted the 4a/4b verdicts under a single
calendar-year deletion (2 of 260 / 0 of 260 move) but convicted the CHOOSER: re-fitting
on a year-deleted IS window moves the rule-8 pick at 8 of 12 chooser x panel pairs and the
OOS 4b verdict at 5 of 12, while 44 of 100 perturbed picks clear 4b OOS and 0 of 100 clear
4a.  So the perturbation ensemble CONTAINS passing books that argmax-IS-Sharpe walks past.
Idea 1695 sharpened why one rung matters: 4b is a two-leg gross interval of mean feasible
width 1.11 of 20 rungs.  The constructive question nobody has priced: if the IS window is
re-used to pick a DELETION-ROBUST cell instead of the plain argmax, does that buy anything
OUT OF SAMPLE?

CONSTRUCTION.  Two tuned parameters and no more: band c and gross G.
  c in {NOGATE, 0.00, 0.03, 0.10}          (NOGATE = always invested, no 200d band)
  G in {0.30,0.40,0.50,0.60,0.70,0.80,0.90,1.00}
  -> 32 cells x 3 panels (U56 / B136 / SMALL) = 96 real books, EVERY ONE published in grid.csv.
Weekly cadence, 10 bps per unit turnover, next-day execution (engine).  Costs, cadence and
execution are fixed by PROTOCOL and are NOT dials here.

DELETION CONVENTION (stated once, never varied, same as idea 720).  The book is never
re-run.  It is run once on the full tape and the calendar year is removed from the SCORED
RETURN STREAM.  This isolates "is this pick carried by one year?" from "would the signal
have differed?".

CHOOSERS (the object of study, not tuned parameters).  All see 2009-2016 ONLY.
  A_SHARPE : argmax IS Sharpe                      <- what the record has always used
  R_MEAN   : argmax of the MEAN IS Sharpe over the 8 leave-one-IS-year-out deletions
  R_MIN    : argmax of the WORST-CASE LOYO IS Sharpe
  R_MODAL  : the cell that is argmax most often across the 8 LOYO deletions (ties -> R_MEAN)
Each chooser's pick is read on 2017-2026 EXACTLY ONCE.

REPORTED.  Every grid point (IS/OOS/FULL CAGR, Sharpe, MaxDD, halves), both KEEP paths at
every cell on FULL and on OOS, each chooser's pick and its OOS numbers against the LIVE
RULES v2 baseline and SPY, and the ORACLE cell (best OOS) as the upper bound the choosers
are trying to reach.

SURVIVORSHIP.  universe.json (U56) and universe_broad.json (B136) are CURRENT constituents;
the SMALL panel likewise (see data/SMALL_PANEL_README.md).  Every number below inherits that
bias.  No network: all three panels come from committed caches.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, backtest, metrics  # noqa

OUT = Path(__file__).resolve().parent / "2026-09-20_deletion-robust-rule8-chooser_B"
OUT.mkdir(exist_ok=True)

BANDS = ["NOGATE", 0.00, 0.03, 0.10]
GROSS = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
IS_YEARS = list(range(2009, 2017))
COST, FREQ = 10, "W"

# ---------------------------------------------------------------- book family
def book_weights(px, c, G):
    """Equal-weight every priced name at G/N; if c is a band, gated-out weight goes to CASH
    (de-gross, never re-spread) exactly as live RULES v2 does."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = G * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if c == "NOGATE":
        return ew
    return ew.where(band_state(px, c), 0.0)

# ---------------------------------------------------------------- scoring
def sub(r, lo=None, hi=None):
    return r.loc[lo:hi] if (lo or hi) else r

def m3(r):
    if len(r) < 60: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, H1=np.nan, H2=np.nan)
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

def verdict_4a(bk, base):
    """Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse than RULES v2."""
    return bool(bk["H1"] > base["H1"] and bk["H2"] > base["H2"] and bk["MaxDD"] >= base["MaxDD"])

def verdict_4b(bk, spy, oos_sharpe, oos_spy_sharpe):
    """Sharpe > SPY in BOTH halves of the window AND out of sample (rule 8),
    MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    return bool(bk["H1"] > spy["H1"] and bk["H2"] > spy["H2"]
                and oos_sharpe > oos_spy_sharpe
                and bk["MaxDD"] >= 0.60 * spy["MaxDD"]          # MaxDD is negative
                and bk["CAGR"] >= 0.70 * spy["CAGR"])

def loyo_sharpes(r_is):
    """Leave-one-IS-calendar-year-out Sharpes of an IS return stream (book never re-run)."""
    out = {}
    for y in IS_YEARS:
        keep = r_is[r_is.index.year != y]
        out[y] = metrics(keep)["Sharpe"] if len(keep) > 60 else np.nan
    return out

# ---------------------------------------------------------------- run
PANELS = [("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))]
grid_rows, pick_rows, gate_log = [], [], []

for pname, kw in PANELS:
    px = load_universe(**kw)
    start = px.index[260]                                    # skip 200d warm-up, as compare() does
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    base_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]

    win = {"FULL": (None, None), "IS": (None, IS_END), "OOS": (OOS_START, None)}
    spy_m = {w: m3(sub(spy_r, *win[w])) for w in win}
    base_m = {w: m3(sub(base_r, *win[w])) for w in win}
    gate_log.append(f"{pname}: sample {start.date()}..{px.index[-1].date()} N={px.shape[1]-1}+SPY | "
                    f"RULES v2 FULL {base_m['FULL']['CAGR']:.2%}/{base_m['FULL']['Sharpe']:.4f}/{base_m['FULL']['MaxDD']:.2%} | "
                    f"SPY FULL {spy_m['FULL']['CAGR']:.2%}/{spy_m['FULL']['Sharpe']:.4f}/{spy_m['FULL']['MaxDD']:.2%}")

    cells = {}
    for c in BANDS:
        for G in GROSS:
            r = backtest(px, book_weights(px, c, G), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            mm = {w: m3(sub(r, *win[w])) for w in win}
            lo = loyo_sharpes(sub(r, *win["IS"]))
            cells[(c, G)] = dict(r=r, m=mm, loyo=lo)
            row = dict(panel=pname, band=str(c), gross=G,
                       IS_Sharpe=mm["IS"]["Sharpe"],
                       loyo_mean=float(np.nanmean(list(lo.values()))),
                       loyo_min=float(np.nanmin(list(lo.values()))),
                       loyo_sd=float(np.nanstd(list(lo.values()))))
            for w in ("FULL", "OOS"):
                row[f"{w}_CAGR"] = mm[w]["CAGR"]; row[f"{w}_Sharpe"] = mm[w]["Sharpe"]
                row[f"{w}_MaxDD"] = mm[w]["MaxDD"]; row[f"{w}_H1"] = mm[w]["H1"]; row[f"{w}_H2"] = mm[w]["H2"]
                row[f"{w}_4a"] = verdict_4a(mm[w], base_m[w])
                row[f"{w}_4b"] = verdict_4b(mm[w], spy_m[w], mm["OOS"]["Sharpe"], spy_m["OOS"]["Sharpe"])
            grid_rows.append(row)

    # ------------------------------------------------ choosers, IS window ONLY
    keys = list(cells)
    def argmax_by(f):
        vals = [f(cells[k]) for k in keys]
        return keys[int(np.nanargmax(vals))]

    picks = {}
    picks["A_SHARPE"] = argmax_by(lambda d: d["m"]["IS"]["Sharpe"])
    picks["R_MEAN"] = argmax_by(lambda d: np.nanmean(list(d["loyo"].values())))
    picks["R_MIN"] = argmax_by(lambda d: np.nanmin(list(d["loyo"].values())))
    votes = {}
    for y in IS_YEARS:
        w = keys[int(np.nanargmax([cells[k]["loyo"][y] for k in keys]))]
        votes[w] = votes.get(w, 0) + 1
    top = max(votes.values())
    tied = [k for k, v in votes.items() if v == top]
    picks["R_MODAL"] = tied[0] if len(tied) == 1 else max(
        tied, key=lambda k: np.nanmean(list(cells[k]["loyo"].values())))
    # oracle: best OOS Sharpe, published as the upper bound the choosers aim at (never a pick)
    picks["ORACLE_OOS"] = argmax_by(lambda d: d["m"]["OOS"]["Sharpe"])

    for cname, k in picks.items():
        mm = cells[k]["m"]
        pick_rows.append(dict(
            panel=pname, chooser=cname, band=str(k[0]), gross=k[1],
            IS_Sharpe=mm["IS"]["Sharpe"],
            loyo_mean=float(np.nanmean(list(cells[k]["loyo"].values()))),
            loyo_min=float(np.nanmin(list(cells[k]["loyo"].values()))),
            n_argmax_years=votes.get(k, 0),
            OOS_CAGR=mm["OOS"]["CAGR"], OOS_Sharpe=mm["OOS"]["Sharpe"], OOS_MaxDD=mm["OOS"]["MaxDD"],
            OOS_4a=verdict_4a(mm["OOS"], base_m["OOS"]),
            OOS_4b=verdict_4b(mm["OOS"], spy_m["OOS"], mm["OOS"]["Sharpe"], spy_m["OOS"]["Sharpe"]),
            FULL_CAGR=mm["FULL"]["CAGR"], FULL_Sharpe=mm["FULL"]["Sharpe"], FULL_MaxDD=mm["FULL"]["MaxDD"],
            FULL_4a=verdict_4a(mm["FULL"], base_m["FULL"]),
            FULL_4b=verdict_4b(mm["FULL"], spy_m["FULL"], mm["OOS"]["Sharpe"], spy_m["OOS"]["Sharpe"]),
            base_OOS_Sharpe=base_m["OOS"]["Sharpe"], base_OOS_MaxDD=base_m["OOS"]["MaxDD"],
            spy_OOS_CAGR=spy_m["OOS"]["CAGR"], spy_OOS_Sharpe=spy_m["OOS"]["Sharpe"], spy_OOS_MaxDD=spy_m["OOS"]["MaxDD"],
        ))

grid = pd.DataFrame(grid_rows); picks_df = pd.DataFrame(pick_rows)
grid.to_csv(OUT / "grid.csv", index=False)
picks_df.to_csv(OUT / "picks.csv", index=False)

pd.set_option("display.width", 240, "display.max_columns", 50)
print("=" * 110); print("GATES / panel context"); print("=" * 110)
for g in gate_log: print(" ", g)

print("\n" + "=" * 110); print("ALL 96 GRID POINTS (IS chooser objectives + FULL/OOS verdicts)"); print("=" * 110)
show = ["panel", "band", "gross", "IS_Sharpe", "loyo_mean", "loyo_min", "loyo_sd",
        "FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD", "FULL_4a", "FULL_4b",
        "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_4a", "OOS_4b"]
print(grid[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\n" + "=" * 110); print("RULE 8 — each chooser fitted on 2009-2016 only, 2017-2026 read ONCE"); print("=" * 110)
print(picks_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\n" + "=" * 110); print("HEADLINE"); print("=" * 110)
for pname, _ in PANELS:
    sl = picks_df[picks_df.panel == pname].set_index("chooser")
    a = sl.loc["A_SHARPE"]
    for cname in ("R_MEAN", "R_MIN", "R_MODAL"):
        r = sl.loc[cname]
        same = (r.band == a.band) and (r.gross == a.gross)
        print(f"  {pname:5s} {cname:8s} pick=({r.band},{r.gross:.2f}) vs A_SHARPE=({a.band},{a.gross:.2f})"
              f" {'SAME CELL' if same else 'DIFFERENT'} | dOOS_Sharpe {r.OOS_Sharpe - a.OOS_Sharpe:+.4f}"
              f" | 4b OOS {int(a.OOS_4b)}->{int(r.OOS_4b)}")
    o = sl.loc["ORACLE_OOS"]
    print(f"  {pname:5s} ORACLE   pick=({o.band},{o.gross:.2f}) OOS Sharpe {o.OOS_Sharpe:.4f}"
          f" (A_SHARPE leaves {o.OOS_Sharpe - a.OOS_Sharpe:.4f} on the table) | 4b OOS {int(o.OOS_4b)}")

nA = int(picks_df[picks_df.chooser == "A_SHARPE"].OOS_4b.sum())
nR = {c: int(picks_df[picks_df.chooser == c].OOS_4b.sum()) for c in ("R_MEAN", "R_MIN", "R_MODAL")}
moved = int(sum(
    not ((picks_df[(picks_df.panel == p) & (picks_df.chooser == c)].iloc[0].band ==
          picks_df[(picks_df.panel == p) & (picks_df.chooser == "A_SHARPE")].iloc[0].band) and
         (picks_df[(picks_df.panel == p) & (picks_df.chooser == c)].iloc[0].gross ==
          picks_df[(picks_df.panel == p) & (picks_df.chooser == "A_SHARPE")].iloc[0].gross))
    for p, _ in PANELS for c in ("R_MEAN", "R_MIN", "R_MODAL")))
print(f"\n  cells moved by robustness: {moved} of 9 (3 panels x 3 robust choosers)")
print(f"  4b OOS passes: A_SHARPE {nA}/3, " + ", ".join(f"{c} {v}/3" for c, v in nR.items()))
print(f"  4a OOS passes: " + ", ".join(
    f"{c} {int(picks_df[picks_df.chooser==c].OOS_4a.sum())}/3" for c in ("A_SHARPE", "R_MEAN", "R_MIN", "R_MODAL")))
print(f"  grid-wide: FULL 4a {int(grid.FULL_4a.sum())}/96, FULL 4b {int(grid.FULL_4b.sum())}/96, "
      f"OOS 4a {int(grid.OOS_4a.sum())}/96, OOS 4b {int(grid.OOS_4b.sum())}/96")
print(f"\n  wrote {OUT/'grid.csv'} and {OUT/'picks.csv'}")

# ---------------------------------------------------------------- why: resolution of the IS surface
print("\n" + "=" * 110)
print("WHY — the IS objective surface's own resolution (this is what decides the answer)")
print("=" * 110)
res_rows = []
for pname, _ in PANELS:
    g = grid[grid.panel == pname]
    # (a) how flat is the IS objective ALONG the gross ladder, within a band family?
    for c in BANDS:
        f = g[g.band == str(c)]
        res_rows.append(dict(panel=pname, band=str(c), axis="G 0.30->1.00",
                             IS_spread=f.IS_Sharpe.max() - f.IS_Sharpe.min(),
                             loyo_sd=f.loyo_sd.mean(),
                             ratio=(f.IS_Sharpe.max() - f.IS_Sharpe.min()) / f.loyo_sd.mean(),
                             OOS_MaxDD_spread=f.OOS_MaxDD.max() - f.OOS_MaxDD.min(),
                             OOS_CAGR_spread=f.OOS_CAGR.max() - f.OOS_CAGR.min()))
    # (b) argmax margin over the runner-up CELL vs that cell's own deletion SD
    s = g.sort_values("IS_Sharpe", ascending=False)
    top, run = s.iloc[0], s.iloc[1]
    res_rows.append(dict(panel=pname, band="*argmax vs runner-up*", axis=f"({top.band},{top.gross:.2f}) vs ({run.band},{run.gross:.2f})",
                         IS_spread=top.IS_Sharpe - run.IS_Sharpe, loyo_sd=top.loyo_sd,
                         ratio=(top.IS_Sharpe - run.IS_Sharpe) / top.loyo_sd,
                         OOS_MaxDD_spread=np.nan, OOS_CAGR_spread=np.nan))
    # (c) argmax margin over the best cell in a DIFFERENT band family
    other = g[g.band != top.band].sort_values("IS_Sharpe", ascending=False).iloc[0]
    res_rows.append(dict(panel=pname, band="*argmax vs best OTHER band*", axis=f"({top.band}) vs ({other.band})",
                         IS_spread=top.IS_Sharpe - other.IS_Sharpe, loyo_sd=top.loyo_sd,
                         ratio=(top.IS_Sharpe - other.IS_Sharpe) / top.loyo_sd,
                         OOS_MaxDD_spread=np.nan, OOS_CAGR_spread=np.nan))
res = pd.DataFrame(res_rows)
res.to_csv(OUT / "resolution.csv", index=False)
print(res.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

print("\n  loyo_mean vs plain IS Sharpe, over all 96 cells: "
      f"max |diff| = {float((grid.loyo_mean - grid.IS_Sharpe).abs().max()):.4f}, "
      f"mean |diff| = {float((grid.loyo_mean - grid.IS_Sharpe).abs().mean()):.4f} "
      "  <- R_MEAN is arithmetically the SAME chooser as A_SHARPE at this window length")
print(f"  IS-argmax gross rung: " + ", ".join(
    f"{p}={picks_df[(picks_df.panel==p)&(picks_df.chooser=='A_SHARPE')].iloc[0].gross:.2f}" for p, _ in PANELS)
    + " | ORACLE_OOS gross rung: " + ", ".join(
    f"{p}={picks_df[(picks_df.panel==p)&(picks_df.chooser=='ORACLE_OOS')].iloc[0].gross:.2f}" for p, _ in PANELS))
agree = picks_df[picks_df.chooser == "A_SHARPE"][["panel", "n_argmax_years"]]
print("  LOYO years whose own argmax equals the undeleted argmax (of 8): " +
      ", ".join(f"{r.panel}={int(r.n_argmax_years)}" for r in agree.itertuples()))
