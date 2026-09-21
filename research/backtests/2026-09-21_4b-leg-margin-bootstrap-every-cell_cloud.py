#!/usr/bin/env python3
"""Idea 2042 (lane cloud, 2026-09-21) — IS A 4b PASS RESOLVABLE, OR IS IT A POINT ESTIMATE?
Paired block-bootstrap standard errors on ALL FIVE 4b leg margins, at EVERY CELL of a
pre-registered 36-cell book grid, plus the rule-8-reached cell.

THE QUESTION.  PROTOCOL path 4b is five inequalities against SPY.  The record publishes
thousands of 4b verdicts and, until today, not one of them carried an error bar on the leg
that actually binds.  Lane B's idea 2060 (2026-09-21) put a paired block bootstrap on the five
legs of ONE cell (the standing VOLTGT-DRIFT candidate) and found the CAGR-floor margin
unresolvable at 30 (block, seed) points.  This run asks the POPULATION question 2060 could not:
over a grid of 36 real books, how many of the cells that PASS 4b on the point estimate still
pass once the 95% CI on their BINDING leg has to sit entirely on the passing side — and is the
cell a legal IS-only chooser reaches (PROTOCOL rule 8) one of the survivors?

THE TWO TUNED PARAMETERS (PROTOCOL rule 4; every grid point reported, none hidden):
    P1  B     circular-block length, trading days   {10, 21, 63}
    P2  conf  confidence level                      {0.90, 0.95}
    nboot = 1000 per window, seed 2042, ONE index stream shared by every cell (so cells are
    compared on the same resampled days, and the survival counts below are paired).

REPORTED, NOT TUNED (this is the CELL POPULATION, not a dial being searched):
    panel  {U56 (research/universe.json), B136 (universe_broad.json)}
    band   c {0.00, 0.03, 0.08}      200d MA band, baseline.band_state / rules_v2_weights
    gross  g {0.50, 0.75, 1.00}
    trade  {W, M}
    = 2 x 3 x 3 x 2 = 36 cells, every one published, at 10 bps and t+1 execution.
    The live book (RULES v2: c = 0.03, g = 0.75, W) is cell #14 of this grid by construction,
    so the grid contains the incumbent and is not built around a winner.

BOOTSTRAP CONVENTION (stated because the convention moves the number — ideas 1511 / 2060):
  * PAIRED.  Book and SPY are resampled on the SAME circular-block offsets inside a draw, so
    each margin keeps its day-by-day pairing and the SE is of the CONTRAST, not of two levels.
  * PER-WINDOW.  Each leg is resampled on the window it is READ on (H1 days for L1, H2 for L2,
    2017+ for L3, the whole post-warmup sample for L4/L5).  Blocks are shuffled only inside a
    window, so "half" keeps its meaning.
  * A block bootstrap of a DRAWDOWN breaks the single longest loss run, so L4's SE is
    conservative-to-noisy by construction.  It is reported; the headline survival count is
    driven by L3 and L5, and both are named.
  * The five windows are resampled independently of one another (they are disjoint or nested
    day sets).  That is an assumption, stated, not repaired.

PROTOCOL: rule 2 (10 bps, next-day execution via engine.backtest, no shorting/leverage);
rule 3 (live RULES v2 AND SPY); rule 4 (BOTH KEEP paths at every cell, <= 2 tuned parameters,
all grid points reported); rule 5 (one idea, deterministic, standalone); rule 8 (walk-forward:
the cell is chosen on 2009-2016 ONLY by a pre-registered IS-only chooser, 2017-2026 is read
once, and the pick's OOS legs are bootstrapped); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 and B136 are CURRENT-constituent lists, so every CAGR/MaxDD LEVEL here is
optimistic and both 4b bars are easier than they would be on a point-in-time panel.  The SEs
are same-tape, same-names, paired contrasts and are first-order immune to that bias; the PASS
LEVELS are not.

Runs standalone and offline (committed caches only):
  python research/backtests/2026-09-21_4b-leg-margin-bootstrap-every-cell_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest as engine_backtest                # noqa: E402

DATE, SLUG, LANE = "2026-09-21", "4b-leg-margin-bootstrap-every-cell", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

WARMUP = 260                       # PROTOCOL convention (baseline.compare)
COST_BPS = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BANDS = (0.00, 0.03, 0.08)
GROSSES = (0.50, 0.75, 1.00)
TRADES = ("W", "M")
BLOCKS = (10, 21, 63)              # P1
CONFS = (0.90, 0.95)               # P2
NBOOT, SEED = 1000, 2042
LINES: list[str] = []


def P(s: str = "") -> None:
    print(s)
    LINES.append(s)


# ------------------------------------------------------------------ statistics
def sharpe(r: np.ndarray, axis=-1) -> np.ndarray:
    sd = r.std(axis=axis, ddof=1)
    return np.where(sd > 0, r.mean(axis=axis) / np.where(sd > 0, sd, 1.0) * np.sqrt(252.0), 0.0)


def cagr(r: np.ndarray, axis=-1) -> np.ndarray:
    n = r.shape[axis]
    return np.exp(np.log1p(r).sum(axis=axis) * (252.0 / n)) - 1.0


def maxdd(r: np.ndarray, axis=-1) -> np.ndarray:
    eq = np.cumprod(1.0 + r, axis=axis)
    peak = np.maximum.accumulate(eq, axis=axis)
    return (eq / peak - 1.0).min(axis=axis)          # negative


# ------------------------------------------------------------------ books
def book_returns(px: pd.DataFrame, band: float, gross: float, freq: str) -> pd.Series:
    w = rules_v2_weights(px, band=band, gross=gross)
    res = engine_backtest(px, w, cost_bps=COST_BPS, freq=freq)
    return res["returns"], res["turnover"]


def legs(bk: np.ndarray, sp: np.ndarray, win: dict[str, np.ndarray]) -> dict[str, float]:
    """The five 4b leg margins, positive = passing side."""
    h1, h2, oos, full = win["H1"], win["H2"], win["OOS"], win["FULL"]
    return {
        "L1_H1":  float(sharpe(bk[h1]) - sharpe(sp[h1])),
        "L2_H2":  float(sharpe(bk[h2]) - sharpe(sp[h2])),
        "L3_OOS": float(sharpe(bk[oos]) - sharpe(sp[oos])),
        "L4_DD":  float(0.60 * abs(maxdd(sp[full])) - abs(maxdd(bk[full]))),
        "L5_CAGR": float(cagr(bk[full]) - 0.70 * cagr(sp[full])),
    }


LEGNAMES = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
LEGWIN = {"L1_H1": "H1", "L2_H2": "H2", "L3_OOS": "OOS", "L4_DD": "FULL", "L5_CAGR": "FULL"}


# ------------------------------------------------------------------ bootstrap
def block_index(n: int, B: int, nboot: int, rng: np.random.Generator) -> np.ndarray:
    nb = int(np.ceil(n / B))
    starts = rng.integers(0, n, size=(nboot, nb))
    idx = (starts[:, :, None] + np.arange(B)[None, None, :]) % n
    return idx.reshape(nboot, nb * B)[:, :n].astype(np.int32)


def leg_draws(bk: np.ndarray, sp: np.ndarray, idx: np.ndarray, kind: str) -> np.ndarray:
    b, s = bk[idx], sp[idx]
    if kind == "sharpe":
        return sharpe(b, axis=1) - sharpe(s, axis=1)
    if kind == "dd":
        return 0.60 * np.abs(maxdd(s, axis=1)) - np.abs(maxdd(b, axis=1))
    return cagr(b, axis=1) - 0.70 * cagr(s, axis=1)


LEGKIND = {"L1_H1": "sharpe", "L2_H2": "sharpe", "L3_OOS": "sharpe", "L4_DD": "dd", "L5_CAGR": "cagr"}


def main() -> None:
    P(__doc__.strip())
    P("\n" + "=" * 100)

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    assert panels["U56"].index.equals(panels["B136"].index), "panels must share a trading calendar"
    idx_all = panels["U56"].index
    start = idx_all[WARMUP]
    dates = idx_all[idx_all >= start]
    n = len(dates)
    half = n // 2
    win = {
        "FULL": np.arange(n),
        "H1": np.arange(half),
        "H2": np.arange(half, n),
        "OOS": np.where(dates >= pd.Timestamp(OOS_START))[0],
        "IS": np.where(dates <= pd.Timestamp(IS_END))[0],
    }
    P(f"Sample {dates[0].date()} .. {dates[-1].date()}  n={n} days after {WARMUP}-day warm-up")
    P(f"  H1 {dates[0].date()}..{dates[half-1].date()} ({half})   "
      f"H2 {dates[half].date()}..{dates[-1].date()} ({n-half})   "
      f"IS <= {IS_END} ({len(win['IS'])})   OOS >= {OOS_START} ({len(win['OOS'])})")

    spy = panels["U56"]["SPY"].pct_change().fillna(0.0).loc[start:].to_numpy()
    # live book (RULES v2, weekly) and RULES v1 continuity row, per panel
    base, basev1 = {}, {}
    for pn, px in panels.items():
        base[pn] = engine_backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:].to_numpy()

    # ---------------- every cell
    rows, ret = [], {}
    for pn, px in panels.items():
        for c in BANDS:
            for g in GROSSES:
                for f in TRADES:
                    r, tno = book_returns(px, c, g, f)
                    r = r.loc[start:].to_numpy()
                    key = (pn, c, g, f)
                    ret[key] = r
                    m = legs(r, spy, win)
                    b = base[pn]
                    row = dict(panel=pn, band=c, gross=g, trade=f,
                               CAGR=float(cagr(r[win["FULL"]])), Sharpe=float(sharpe(r[win["FULL"]])),
                               MaxDD=float(maxdd(r[win["FULL"]])),
                               H1=float(sharpe(r[win["H1"]])), H2=float(sharpe(r[win["H2"]])),
                               OOS_CAGR=float(cagr(r[win["OOS"]])), OOS_Sharpe=float(sharpe(r[win["OOS"]])),
                               OOS_MaxDD=float(maxdd(r[win["OOS"]])),
                               IS_Sharpe=float(sharpe(r[win["IS"]])),
                               turn=float(tno.loc[start:].mean() * 252), **m)
                    row["pass4b"] = all(row[k] > 0 for k in LEGNAMES)
                    # 4a: Sharpe > live book in BOTH halves and MaxDD no worse
                    row["pass4a"] = (row["H1"] > sharpe(b[win["H1"]]) and row["H2"] > sharpe(b[win["H2"]])
                                     and row["MaxDD"] >= float(maxdd(b[win["FULL"]])))
                    rows.append(row)
    cells = pd.DataFrame(rows)

    P("\n" + "-" * 100)
    P("SECTION 1 — ALL 36 CELLS, point estimates (10 bps, t+1).  SPY and the live book on the same tape:")
    P(f"  SPY        CAGR {cagr(spy[win['FULL']]):.2%}  Sharpe {sharpe(spy[win['FULL']]):.4f}  "
      f"MaxDD {maxdd(spy[win['FULL']]):.2%}  H1 {sharpe(spy[win['H1']]):.4f}  H2 {sharpe(spy[win['H2']]):.4f}  "
      f"OOS {sharpe(spy[win['OOS']]):.4f} / CAGR {cagr(spy[win['OOS']]):.2%}")
    for pn in panels:
        b = base[pn]
        P(f"  RULES v2 ({pn})  CAGR {cagr(b[win['FULL']]):.2%}  Sharpe {sharpe(b[win['FULL']]):.4f}  "
          f"MaxDD {maxdd(b[win['FULL']]):.2%}  H1 {sharpe(b[win['H1']]):.4f}  H2 {sharpe(b[win['H2']]):.4f}  "
          f"OOS {sharpe(b[win['OOS']]):.4f} / CAGR {cagr(b[win['OOS']]):.2%}")
    P("  4b bars: H1 > SPY H1, H2 > SPY H2, OOS > SPY OOS, |MaxDD| <= 0.60x|SPY|, CAGR >= 0.70x SPY")
    show = cells[["panel", "band", "gross", "trade", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_Sharpe", "turn"] + LEGNAMES + ["pass4a", "pass4b"]]
    P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  POINT-ESTIMATE COUNTS: 4b passes {int(cells.pass4b.sum())} of {len(cells)}; "
      f"4a passes {int(cells.pass4a.sum())} of {len(cells)}; both {int((cells.pass4a & cells.pass4b).sum())}.")

    # ---------------- bootstrap
    rng = np.random.default_rng(SEED)
    P("\n" + "-" * 100)
    P(f"SECTION 2 — PAIRED CIRCULAR-BLOCK BOOTSTRAP, nboot={NBOOT}, seed={SEED}, one index stream per (window, B).")
    boot_rows = []
    for B in BLOCKS:
        idxs = {w: block_index(len(win[w]), B, NBOOT, np.random.default_rng(SEED + B)) for w in ("H1", "H2", "OOS", "FULL")}
        for _, row in cells.iterrows():
            key = (row.panel, row.band, row.gross, row.trade)
            r = ret[key]
            for leg in LEGNAMES:
                w = LEGWIN[leg]
                d = leg_draws(r[win[w]], spy[win[w]], idxs[w], LEGKIND[leg])
                se = float(d.std(ddof=1))
                rec = dict(panel=row.panel, band=row.band, gross=row.gross, trade=row.trade,
                           B=B, leg=leg, margin=float(row[leg]), se=se,
                           t=float(row[leg] / se) if se > 0 else np.nan)
                for cf in CONFS:
                    a = (1.0 - cf) / 2.0
                    rec[f"lo{int(cf*100)}"] = float(np.quantile(d, a))
                    rec[f"hi{int(cf*100)}"] = float(np.quantile(d, 1 - a))
                boot_rows.append(rec)
    bt = pd.DataFrame(boot_rows)
    bt.to_csv(f"{OUT}.legs.csv", index=False)

    P("\n  Per-leg SE (median over the 36 cells) and how many cells' margin exceeds 2 SE, by block length:")
    for B in BLOCKS:
        s = bt[bt.B == B]
        parts = []
        for leg in LEGNAMES:
            x = s[s.leg == leg]
            parts.append(f"{leg} SE {x.se.median():.4f} |t|>2 {int((x.t.abs() > 2).sum())}/{len(x)}")
        P(f"    B={B:>3}d  " + "  ".join(parts))

    # ---------------- survival of the 4b passes
    P("\n" + "-" * 100)
    P("SECTION 3 — DOES A 4b PASS SURVIVE ITS OWN ERROR BAR?")
    P("  BINDING LEG = the passing cell's leg with the smallest bootstrap t (margin / SE).")
    P("  SURVIVES(binding) = that leg's CI lower bound > 0.   SURVIVES(joint) = ALL FIVE CIs' lower bound > 0.")
    surv_rows = []
    passing = cells[cells.pass4b]
    for B in BLOCKS:
        for cf in CONFS:
            lo = f"lo{int(cf*100)}"
            nsurv_b = nsurv_j = 0
            for _, row in passing.iterrows():
                s = bt[(bt.panel == row.panel) & (bt.band == row.band) & (bt.gross == row.gross)
                       & (bt.trade == row.trade) & (bt.B == B)].set_index("leg")
                bind = s.t.idxmin()
                ok_b = s.loc[bind, lo] > 0
                ok_j = bool((s[lo] > 0).all())
                nsurv_b += int(ok_b)
                nsurv_j += int(ok_j)
                surv_rows.append(dict(panel=row.panel, band=row.band, gross=row.gross, trade=row.trade,
                                      B=B, conf=cf, binding=bind, bind_t=float(s.t.min()),
                                      bind_margin=float(s.loc[bind, "margin"]), bind_lo=float(s.loc[bind, lo]),
                                      survives_binding=ok_b, survives_joint=ok_j))
            P(f"    B={B:>3}d  conf={cf:.2f}   binding-leg survivors {nsurv_b}/{len(passing)}   "
              f"all-five survivors {nsurv_j}/{len(passing)}")
    sv = pd.DataFrame(surv_rows)
    sv.to_csv(f"{OUT}.survival.csv", index=False)
    if len(passing):
        P("\n  Which leg BINDS on the passing cells (count over all (B, conf) points):")
        P("    " + sv.binding.value_counts().to_string().replace("\n", "\n    "))
        P("\n  Per-cell detail at B=21, conf=0.95 (the mid grid point; every other point is in the csv):")
        d = sv[(sv.B == 21) & (sv.conf == 0.95)]
        P("    " + d.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    cells.to_csv(f"{OUT}.cells.csv", index=False)

    # ---------------- rule 8
    P("\n" + "-" * 100)
    P("SECTION 4 — RULE 8 WALK-FORWARD.  Cell chosen on 2009-2016 ONLY, 2017-2026 read once.")
    P("  Pre-registered IS-only choosers (both reported; neither is tuned):")
    P("    C1 = max IS Sharpe.   C2 = max IS min-leg margin (the four 4b legs computable in-sample:")
    P("         IS-half1 Sharpe, IS-half2 Sharpe, IS MaxDD cap, IS CAGR floor — OOS is NOT looked at).")
    is_i = win["IS"]
    ih = len(is_i) // 2
    picks = {}
    isrows = []
    for _, row in cells.iterrows():
        key = (row.panel, row.band, row.gross, row.trade)
        r = ret[key][is_i]
        s = spy[is_i]
        m = [float(sharpe(r[:ih]) - sharpe(s[:ih])), float(sharpe(r[ih:]) - sharpe(s[ih:])),
             float(0.60 * abs(maxdd(s)) - abs(maxdd(r))), float(cagr(r) - 0.70 * cagr(s))]
        isrows.append(dict(key=key, panel=row.panel, band=row.band, gross=row.gross, trade=row.trade,
                           IS_Sharpe=float(sharpe(r)), IS_minleg=min(m)))
    isdf = pd.DataFrame(isrows)
    picks["C1"] = isdf.loc[isdf.IS_Sharpe.idxmax()]
    picks["C2"] = isdf.loc[isdf.IS_minleg.idxmax()]
    P(f"  IS window {dates[is_i[0]].date()} .. {dates[is_i[-1]].date()} ({len(is_i)} days).")
    for cn, pk in picks.items():
        P(f"    {cn} picks  panel={pk.panel} band={pk.band:.2f} gross={pk.gross:.2f} trade={pk.trade}  "
          f"(IS Sharpe {pk.IS_Sharpe:.4f}, IS min-leg {pk.IS_minleg:+.4f})")

    oos = win["OOS"]
    P("\n  OOS 2017-2026, read ONCE, for each pick, against the live book and SPY on the same days:")
    P(f"    {'who':<34}{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}")
    P(f"    {'SPY':<34}{cagr(spy[oos]):>9.2%}{sharpe(spy[oos]):>9.4f}{maxdd(spy[oos]):>9.2%}")
    for pn in panels:
        b = base[pn][oos]
        P(f"    {'RULES v2 live (' + pn + ')':<34}{cagr(b):>9.2%}{sharpe(b):>9.4f}{maxdd(b):>9.2%}")
    wf_rows = []
    for cn, pk in picks.items():
        r = ret[pk.key][oos]
        b = base[pk.panel][oos]
        lab = f"{cn} pick {pk.panel} c{pk.band:.2f} g{pk.gross:.2f} {pk.trade}"
        P(f"    {lab:<34}{cagr(r):>9.2%}{sharpe(r):>9.4f}{maxdd(r):>9.2%}")
        full_row = cells[(cells.panel == pk.panel) & (cells.band == pk.band)
                         & (cells.gross == pk.gross) & (cells.trade == pk.trade)].iloc[0]
        # OOS-only 4b legs (halves of the OOS window) + full-sample 4b verdict
        oh = len(oos) // 2
        oos_legs = {
            "O1_H1": float(sharpe(r[:oh]) - sharpe(spy[oos][:oh])),
            "O2_H2": float(sharpe(r[oh:]) - sharpe(spy[oos][oh:])),
            "O3_OOS": float(sharpe(r) - sharpe(spy[oos])),
            "O4_DD": float(0.60 * abs(maxdd(spy[oos])) - abs(maxdd(r))),
            "O5_CAGR": float(cagr(r) - 0.70 * cagr(spy[oos])),
        }
        pass4b_oos = all(v > 0 for v in oos_legs.values())
        pass4a_oos = (sharpe(r[:oh]) > sharpe(b[:oh]) and sharpe(r[oh:]) > sharpe(b[oh:])
                      and maxdd(r) >= maxdd(b))
        P(f"      full-sample 4b {'PASS' if full_row.pass4b else 'FAIL'}   4a {'PASS' if full_row.pass4a else 'FAIL'}   "
          f"| OOS-window 4b {'PASS' if pass4b_oos else 'FAIL'}  4a {'PASS' if pass4a_oos else 'FAIL'}  "
          + "  ".join(f"{k} {v:+.4f}" for k, v in oos_legs.items()))
        # bootstrap the pick's OOS legs at every (B, conf)
        for B in BLOCKS:
            ix = block_index(len(oos), B, NBOOT, np.random.default_rng(SEED + B))
            for k, kind in (("O3_OOS", "sharpe"), ("O4_DD", "dd"), ("O5_CAGR", "cagr")):
                d = leg_draws(r, spy[oos], ix, kind)
                se = float(d.std(ddof=1))
                rec = dict(chooser=cn, panel=pk.panel, band=pk.band, gross=pk.gross, trade=pk.trade,
                           B=B, leg=k, margin=oos_legs[k], se=se, t=oos_legs[k] / se if se else np.nan)
                for cf in CONFS:
                    a = (1 - cf) / 2
                    rec[f"lo{int(cf*100)}"] = float(np.quantile(d, a))
                    rec[f"hi{int(cf*100)}"] = float(np.quantile(d, 1 - a))
                wf_rows.append(rec)
        # is the pick a survivor?
        if bool(full_row.pass4b):
            s = sv[(sv.panel == pk.panel) & (sv.band == pk.band) & (sv.gross == pk.gross) & (sv.trade == pk.trade)]
            P(f"      the rule-8-reached cell IS a full-sample 4b pass; binding-leg survival at the six "
              f"(B, conf) points: {int(s.survives_binding.sum())}/{len(s)}; all-five: {int(s.survives_joint.sum())}/{len(s)}")
        else:
            P("      the rule-8-reached cell is NOT a full-sample 4b pass, so it has no pass to survive.")
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n  Bootstrap of the picks' OOS-window legs (margin / SE / t / 95% CI), all (B) points:")
    P("    " + wf.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    P("\n" + "=" * 100)
    P("Files: " + ", ".join(Path(f"{OUT}.{x}").name for x in ("cells.csv", "legs.csv", "survival.csv", "walkforward.csv", "txt")))
    Path(f"{OUT}.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
