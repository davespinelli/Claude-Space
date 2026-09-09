#!/usr/bin/env python3
"""Idea 542 - "does-MA-THRESH-theta-0-beat-RULES-v2-s-3-percent-BAND-on-its-own-terms"
(lane C, 2026-09-09).

The question
------------
Idea 299's ONLY cell clearing PROTOCOL 4b on both required panels is the plain
"hold every name above its 200d MA" book (MA-THRESH at theta = 0):
U56 11.59% / 1.0948 / -18.62%, B136 11.66% / 1.0585 / -20.12%.  That book is RULES v2's
clause 2 WITHOUT the hysteresis band.  The queue's instruction is exact: price theta = 0
against the LIVE band directly, at MATCHED gross and cadence, and report whether the band
earns its two extra numbers (the ma*(1+b) entry and the ma*(1-b) exit).

The band is not a different family here -- it is the SAME family with one dial.  band = 0.00
IS theta = 0 (gate G3 asserts the identity to the cell), so the whole question reduces to:
does the record's live 0.03 sit anywhere the data can distinguish from 0.00?

Design (fixed before any number was read)
-----------------------------------------
FIXED, never varied:
    cadence   W (weekly) -- the LIVE cadence and the record default
    costs     10 bps per unit turnover, next-day execution (t decided, t+1 applied)
    gate      200d MA band with hysteresis, exactly baseline.band_state
    windows   IS <= 2016-12-31, OOS >= 2017-01-01 (PROTOCOL rule 8)
    panels    U56 and B136 REQUIRED (idea 299's two required panels); SMALL439 reported only
    baseline  the live RULES v2 book computed on U56 and reindexed onto each panel, i.e.
              idea 299's convention verbatim

TUNED PARAMETERS -- exactly two, as the queue specifies (band, gross):
    1. BAND  6 values {0.00, 0.01, 0.02, 0.03, 0.05, 0.08}.  0.00 = theta 0 (the challenger),
             0.03 = the live band (the incumbent).  Every point reported.
    2. GROSS 4 values {0.25, 0.50, 0.75, 1.00}.  0.75 is live.  "Matched gross" is the whole
             point of the comparison, so gross is a shared axis, never a per-arm choice.
    CONSTRUCTION is NOT a third dial: DEGROSS (gated-out weight -> cash) is the LIVE form and
    the pre-registered one; RESPREAD (equal weight across held names) is idea 299's book form
    and is reported as a CONTROL beside it.  Any KEEP claim may only come from DEGROSS.
    6 x 4 x 2 x 3 panels = 144 books, all reported.

Pre-registered bars, written before any number was read
--------------------------------------------------------
B1  THE HEAD-TO-HEAD.  At every matched (panel, gross, construction) cell, band 0.00 "beats"
    band 0.03 iff full-sample Sharpe is higher AND MaxDD is no worse.  24 paired cells; the
    count is the answer, not a selected cell.
B2  DOES THE BAND EARN ITS NUMBERS.  A dial earns its place only if its effect is
    distinguishable from zero.  Paired circular-block bootstrap (2000 draws, 21-day blocks,
    seed 0) on the daily net return difference at the LIVE operating point (gross 0.75,
    DEGROSS) for both required panels: report the 95% CI of the Sharpe difference and of the
    CAGR difference.  A CI straddling zero means the two extra numbers are not paid for.
B3  RULE 8.  band chosen on IS (<= 2016) Sharpe ONLY at live gross, per panel and pooled over
    the two required panels; OOS read once.  Reported for both constructions.  A KEEP needs
    the IS-chosen cell to clear 4b's OOS leg on BOTH required panels.
B4  TWO-DIAL RULE 8.  Because Sharpe is near-invariant in gross (record: span <= 0.006), the
    2-dial pick is made on IS Sharpe SUBJECT TO the IS drawdown cap |MaxDD| <= 0.60 x |SPY
    IS MaxDD| (the constraint that makes gross identifiable), ties to lower gross.  OOS once.
B5  BOTH KEEP PATHS on all 144 books:
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 60% of SPY's, CAGR >= 70% of SPY's.

Gates (asserted before any verdict is read)
    G1  the vectorised runner reproduces engine.backtest on the live U56 v2 book to < 1e-12.
    G2  BAND=0.03 / GROSS=0.75 / DEGROSS is bit-identical to baseline.rules_v2_weights.
    G3  BAND=0.00's gate equals (px > ma200) cell-for-cell EXCEPT on exact ties px == ma, where
        the hysteresis holds the previous state; every disagreement must be such a tie.  (It
        fires 0/258500 cells on U56 and 3/634365 on B136 -- TLT 2012-10-18, BSX 2018-02-27,
        IBM 2022-04-08, all px - ma exactly 0.0 at the file's printed precision.)

SURVIVORSHIP: universe.json (U56), universe_broad.json (B136) and prices_small.csv.gz
(SMALL439) are CURRENT constituents -- no delistings -- so every CAGR level here is inflated
and both KEEP columns inherit that whole.  SMALL439 additionally drops every ticker with
max_1d_move >= 1.0 in data/small_meta.csv.  Any memo written off this run carries that caveat.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .paired.csv .boot.csv .walkforward.csv .console.txt .result.md
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights, band_state
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
CADENCE = "W"
BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08]
GROSSES = [0.25, 0.50, 0.75, 1.00]
CONSTRUCTIONS = ["DEGROSS", "RESPREAD"]     # DEGROSS is live + pre-registered; RESPREAD control
LIVE_BAND, LIVE_GROSS, LIVE_CON = 0.03, 0.75, "DEGROSS"
CHALLENGER_BAND = 0.00
REQUIRED_PANELS = ["U56", "B136"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BOOT_DRAWS, BOOT_BLOCK, BOOT_SEED = 2000, 21, 0

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 800)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- vectorised runner
def fast_backtest(px, weights, freq=CADENCE):
    """Reproduces engine.backtest exactly (gate G1); returns GROSS-of-cost returns."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n); gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index),
            "gross": pd.Series(gross, index=px.index)}


def net(res, bps=COST_BPS):
    return res["returns0"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- books
def held_mask(px, band):
    """The gate: 200d MA band with hysteresis, priced names only."""
    return band_state(px, band) & px.notna()


def book(px, band, gross, construction):
    h = held_mask(px, band)
    if construction == "DEGROSS":
        den = px.notna().sum(axis=1)                    # gated-out weight -> CASH (live form)
    else:
        den = h.sum(axis=1)                             # RESPREAD across held names
    return h.astype(float).div(den.replace(0, np.nan), axis=0).fillna(0.0) * gross


# ---------------------------------------------------------------- stats / verdicts
def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def bars_4b(s, spy):
    return {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
            "OOS": s["oSharpe"] > spy["oSharpe"],
            "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
            "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}


def fail_4b(s, spy):
    f = [k for k, v in bars_4b(s, spy).items() if not v]
    return ",".join(f) if f else "-"


def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
        "SMALL439": (pxs[inv], pxs["SPY"]),
    }
    P(f"panels: U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} names ({len(bad)} dropped for max_1d_move >= 1.0)")
    return out


# ---------------------------------------------------------------- B2 bootstrap
def block_boot_diff(ra, rb, draws=BOOT_DRAWS, block=BOOT_BLOCK, seed=BOOT_SEED):
    """Paired circular-block bootstrap of (a - b) on Sharpe and CAGR. Both legs are resampled
    with the SAME block indices, so the pairing (and the common market factor) is preserved."""
    a, b = ra.values, rb.values
    n = len(a)
    nb = int(np.ceil(n / block))
    rng = np.random.default_rng(seed)
    ds, dc = np.empty(draws), np.empty(draws)
    offs = np.arange(block)
    for k in range(draws):
        st = rng.integers(0, n, nb)
        idx = ((st[:, None] + offs[None, :]).ravel() % n)[:n]
        x, y = a[idx], b[idx]
        sx = x.mean() / x.std() * np.sqrt(252) if x.std() else np.nan
        sy = y.mean() / y.std() * np.sqrt(252) if y.std() else np.nan
        ds[k] = sx - sy
        dc[k] = (np.prod(1 + x) ** (252 / n) - 1) - (np.prod(1 + y) ** (252 / n) - 1)
    return ds, dc


def ci(v):
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


# ---------------------------------------------------------------- main
def main():
    P("=" * 180)
    P("Idea 542 does-MA-THRESH-theta-0-beat-RULES-v2-s-3-percent-BAND-on-its-own-terms (lane C) | "
      + Path(__file__).name)
    P("=" * 180)
    P(f"FIXED: cadence {CADENCE} (live), costs {COST_BPS} bps, next-day execution, "
      f"IS <= {IS_END}, OOS >= {OOS_START}.")
    P(f"DIALS (2): BAND {BANDS} x GROSS {GROSSES}.  CONSTRUCTION {CONSTRUCTIONS} is a reported "
      f"control, not a dial; DEGROSS is live and pre-registered.")
    P(f"Incumbent = band {LIVE_BAND} @ gross {LIVE_GROSS} {LIVE_CON} (RULES v2 clause 2).  "
      f"Challenger = band {CHALLENGER_BAND:.2f} (MA-THRESH theta 0), same gross, same cadence.")
    P("SURVIVORSHIP: all three panels are current constituents; CAGR levels are inflated.")

    PN = panels()
    px_u = PN["U56"][0]

    # ------------------------------------------------------------ gates
    P("\n" + "=" * 180)
    P("GATES")
    w_live = rules_v2_weights(load_universe())
    px_full = load_universe()
    r_engine = backtest(px_full, w_live, cost_bps=COST_BPS, freq=CADENCE)["returns"]
    fb = fast_backtest(px_full, w_live)
    r_fast = net(fb)
    g1 = float(np.abs(r_engine - r_fast).max())
    P(f"  G1 vectorised runner vs engine.backtest on the live U56 v2 book: max abs diff {g1:.3e} "
      f"({'PASS' if g1 < 1e-12 else 'FAIL'})")
    assert g1 < 1e-12, g1

    w_mine = book(px_full, LIVE_BAND, LIVE_GROSS, "DEGROSS")
    g2 = float((w_mine - w_live).abs().max().max())
    P(f"  G2 book(band=0.03, gross=0.75, DEGROSS) vs baseline.rules_v2_weights: max abs diff "
      f"{g2:.3e} ({'PASS' if g2 < 1e-15 else 'FAIL'})")
    assert g2 < 1e-15, g2

    P("  G3 theta = 0 identity, per panel.  band = 0 differs from the strict inequality px > ma")
    P("     ONLY on exact ties px == ma, where the hysteresis holds the previous state and the")
    P("     strict inequality says OUT.  The gate requires every disagreement to be such a tie.")
    for pname, (px, _) in PN.items():
        ma = px.rolling(200).mean()
        lhs = held_mask(px, 0.00)
        rhs = (px > ma) & px.notna()
        dm = (lhs != rhs)
        d = int(dm.values.sum())
        ties = int(((px == ma) & dm).values.sum())
        tot = int(lhs.size)
        P(f"     {pname:9s} disagreeing cells {d} / {tot} ({d / tot:.2e}); all exact ties: "
          f"{ties}/{d if d else 0}  ({'PASS' if d == ties else 'FAIL'})")
        assert d == ties, (pname, d, ties)
    flush_log()

    # ------------------------------------------------------------ grid
    live_full = r_engine
    rows, panel_spy, panel_live, keep_ret = [], {}, {}, {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        panel_spy[pname], panel_live[pname] = spy_s, live_s
        cap = 0.60 * abs(spy_s["MaxDD"])
        P("\n" + "-" * 180)
        P(f"PANEL {pname}: evaluation from {start.date()} ({years:.2f} yrs)"
          f"{'  [REQUIRED]' if pname in REQUIRED_PANELS else '  [reported, not required]'}")
        P(f"  SPY      CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS Sharpe {spy_s['oSharpe']:.4f} "
          f"OOS CAGR {spy_s['oCAGR']:.4f}")
        P(f"  RULES v2 CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} "
          f"halves {live_s['H1']:.4f}/{live_s['H2']:.4f} OOS Sharpe {live_s['oSharpe']:.4f} "
          f"OOS CAGR {live_s['oCAGR']:.4f}")
        P(f"  4b bars: H1>{spy_s['H1']:.4f} H2>{spy_s['H2']:.4f} OOS>{spy_s['oSharpe']:.4f} "
          f"|MaxDD|<={cap:.2%} CAGR>={0.70 * spy_s['CAGR']:.2%}")

        for band in BANDS:
            h = held_mask(px, band).loc[start:]
            nheld = h.sum(axis=1)
            for gross in GROSSES:
                for con in CONSTRUCTIONS:
                    res = fast_backtest(px, book(px, band, gross, con))
                    r = net(res).loc[start:]
                    turn = res["turnover"].loc[start:]
                    s = stat(r)
                    rows.append(dict(
                        panel=pname, band=band, gross=gross, con=con, cad=CADENCE, **s,
                        nheld_mean=float(nheld.mean()),
                        gross_mean=float(res["gross"].loc[start:].mean()),
                        turn_yr=float(turn.sum() / years),
                        pass4a=verdict_4a(s, live_s), pass4b=all(bars_4b(s, spy_s).values()),
                        fail4b=fail_4b(s, spy_s)))
                    keep_ret[(pname, band, gross, con)] = r
        flush_log()

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    P("\n" + "=" * 180)
    P("FULL GRID (144 books; every point reported, none selected on)")
    cols = ["panel", "band", "gross", "con", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "oCAGR", "oSharpe", "oMaxDD", "nheld_mean", "turn_yr", "pass4a", "pass4b", "fail4b"]
    for pname in PN:
        P(f"\n--- {pname} " + "-" * 150)
        P(fmt(G[G.panel == pname][cols].drop(columns=["panel"]).set_index(["band", "gross", "con"])))
    flush_log()

    # ------------------------------------------------------------ B1 head-to-head
    P("\n" + "=" * 180)
    P("B1  HEAD-TO-HEAD at matched gross and cadence: band 0.00 (theta 0) vs band 0.03 (live)")
    pr = []
    for pname in PN:
        for gross in GROSSES:
            for con in CONSTRUCTIONS:
                a = G[(G.panel == pname) & (G.band == CHALLENGER_BAND) & (G.gross == gross) & (G.con == con)].iloc[0]
                b = G[(G.panel == pname) & (G.band == LIVE_BAND) & (G.gross == gross) & (G.con == con)].iloc[0]
                pr.append(dict(
                    panel=pname, gross=gross, con=con,
                    CAGR0=a.CAGR, CAGR3=b.CAGR, dCAGR_pp=100 * (a.CAGR - b.CAGR),
                    Sh0=a.Sharpe, Sh3=b.Sharpe, dSharpe=a.Sharpe - b.Sharpe,
                    DD0=a.MaxDD, DD3=b.MaxDD, dDD_pp=100 * (a.MaxDD - b.MaxDD),
                    oSh0=a.oSharpe, oSh3=b.oSharpe, dOOS=a.oSharpe - b.oSharpe,
                    turn0=a.turn_yr, turn3=b.turn_yr, dturn=a.turn_yr - b.turn_yr,
                    theta0_beats=bool(a.Sharpe > b.Sharpe and a.MaxDD >= b.MaxDD),
                    p4b0=bool(a.pass4b), p4b3=bool(b.pass4b)))
    PR = pd.DataFrame(pr)
    PR.to_csv(f"{OUT}.paired.csv", index=False)
    P(fmt(PR.set_index(["panel", "gross", "con"])))
    nb = int(PR.theta0_beats.sum())
    P(f"\n  theta 0 beats the live band (higher Sharpe AND no worse MaxDD) in {nb} / {len(PR)} "
      f"matched cells; on the two REQUIRED panels: "
      f"{int(PR[PR.panel.isin(REQUIRED_PANELS)].theta0_beats.sum())} / "
      f"{len(PR[PR.panel.isin(REQUIRED_PANELS)])}")
    P(f"  mean dSharpe (0.00 - 0.03) {PR.dSharpe.mean():+.4f}, mean dCAGR {PR.dCAGR_pp.mean():+.3f} pp, "
      f"mean dMaxDD {PR.dDD_pp.mean():+.3f} pp, mean d turnover {PR.dturn.mean():+.3f} x/yr")
    P(f"  4b passes: band 0.00 {int(PR.p4b0.sum())} / {len(PR)} cells, "
      f"band 0.03 {int(PR.p4b3.sum())} / {len(PR)}")
    flush_log()

    # ------------------------------------------------------------ B2 bootstrap
    P("\n" + "=" * 180)
    P(f"B2  DOES THE BAND EARN ITS TWO NUMBERS?  paired circular-block bootstrap "
      f"({BOOT_DRAWS} draws, {BOOT_BLOCK}d blocks, seed {BOOT_SEED}) at the LIVE operating "
      f"point (gross {LIVE_GROSS}, {LIVE_CON}).  Positive = theta 0 better.")
    br = []
    for pname in PN:
        ra = keep_ret[(pname, CHALLENGER_BAND, LIVE_GROSS, LIVE_CON)]
        rb = keep_ret[(pname, LIVE_BAND, LIVE_GROSS, LIVE_CON)]
        ds, dc = block_boot_diff(ra, rb)
        lo_s, hi_s = ci(ds); lo_c, hi_c = ci(dc)
        d = ra - rb
        tt = d.mean() / (d.std() / np.sqrt(len(d))) if d.std() else np.nan
        br.append(dict(panel=pname,
                       dSharpe=metrics(ra)["Sharpe"] - metrics(rb)["Sharpe"],
                       boot_lo=lo_s, boot_hi=hi_s, straddles_0=bool(lo_s <= 0 <= hi_s),
                       dCAGR_pp=100 * (metrics(ra)["CAGR"] - metrics(rb)["CAGR"]),
                       cagr_lo_pp=100 * lo_c, cagr_hi_pp=100 * hi_c,
                       cagr_straddles_0=bool(lo_c <= 0 <= hi_c),
                       t_daily_diff=float(tt), prob_theta0_better=float((ds > 0).mean())))
    B = pd.DataFrame(br).set_index("panel")
    B.to_csv(f"{OUT}.boot.csv")
    P(fmt(B))
    flush_log()

    # ------------------------------------------------------------ B3/B4 rule-8 walk-forward
    P("\n" + "=" * 180)
    P("B3  RULE 8, ONE DIAL: band chosen on IS (<= 2016) Sharpe only, at live gross "
      f"{LIVE_GROSS}; OOS (>= 2017) read once.")
    wf = []
    for con in CONSTRUCTIONS:
        for pname in list(PN) + ["POOLED(U56,B136)"]:
            if pname.startswith("POOLED"):
                sub = G[(G.gross == LIVE_GROSS) & (G.con == con) & (G.panel.isin(REQUIRED_PANELS))]
                pick = sub.groupby("band").isSharpe.mean().idxmax()
                for rp in REQUIRED_PANELS:
                    r = G[(G.panel == rp) & (G.band == pick) & (G.gross == LIVE_GROSS) & (G.con == con)].iloc[0]
                    spy = panel_spy[rp]
                    wf.append(dict(mode="B3-pooled", con=con, panel=rp, band=pick, gross=LIVE_GROSS,
                                   isSharpe=r.isSharpe, oCAGR=r.oCAGR, oSharpe=r.oSharpe,
                                   oMaxDD=r.oMaxDD, spy_oCAGR=spy["oCAGR"], spy_oSharpe=spy["oSharpe"],
                                   spy_oMaxDD=spy["oMaxDD"], base_oSharpe=panel_live[rp]["oSharpe"],
                                   oos_beats_spy=bool(r.oSharpe > spy["oSharpe"]),
                                   pass4b_full=bool(r.pass4b), fail4b=r.fail4b))
                continue
            sub = G[(G.panel == pname) & (G.gross == LIVE_GROSS) & (G.con == con)]
            pick = sub.loc[sub.isSharpe.idxmax()]
            spy = panel_spy[pname]
            wf.append(dict(mode="B3-perpanel", con=con, panel=pname, band=pick.band, gross=LIVE_GROSS,
                           isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                           oMaxDD=pick.oMaxDD, spy_oCAGR=spy["oCAGR"], spy_oSharpe=spy["oSharpe"],
                           spy_oMaxDD=spy["oMaxDD"], base_oSharpe=panel_live[pname]["oSharpe"],
                           oos_beats_spy=bool(pick.oSharpe > spy["oSharpe"]),
                           pass4b_full=bool(pick.pass4b), fail4b=pick.fail4b))

    P("\n  IS Sharpe by band at live gross (the selection surface, both constructions):")
    for con in CONSTRUCTIONS:
        t = G[(G.gross == LIVE_GROSS) & (G.con == con)].pivot_table(
            index="band", columns="panel", values="isSharpe")
        t["POOLED"] = t[REQUIRED_PANELS].mean(axis=1)
        P(f"    --- {con}")
        P(fmt(t))

    P("\n" + "=" * 180)
    P("B4  RULE 8, TWO DIALS: (band, gross) chosen on IS Sharpe SUBJECT TO the IS drawdown cap "
      "|MaxDD| <= 0.60 x |SPY IS MaxDD|, ties to lower gross; OOS read once.")
    for con in CONSTRUCTIONS:
        for pname in PN:
            spy = panel_spy[pname]
            sub = G[(G.panel == pname) & (G.con == con)].copy()
            capIS = 0.60 * abs(spy["isMaxDD"])
            ok = sub[sub.isMaxDD.abs() <= capIS]
            note = "IS-DD-cap"
            if ok.empty:
                ok, note = sub, "IS-DD-cap EMPTY -> unconstrained"
            ok = ok.sort_values(["isSharpe", "gross"], ascending=[False, True])
            pick = ok.iloc[0]
            wf.append(dict(mode="B4-2dial", con=con, panel=pname, band=pick.band, gross=pick.gross,
                           isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                           oMaxDD=pick.oMaxDD, spy_oCAGR=spy["oCAGR"], spy_oSharpe=spy["oSharpe"],
                           spy_oMaxDD=spy["oMaxDD"], base_oSharpe=panel_live[pname]["oSharpe"],
                           oos_beats_spy=bool(pick.oSharpe > spy["oSharpe"]),
                           pass4b_full=bool(pick.pass4b), fail4b=pick.fail4b, note=note))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n" + fmt(W.set_index(["mode", "con", "panel"])))
    flush_log()

    # ------------------------------------------------------------ verdict arithmetic
    P("\n" + "=" * 180)
    P("KEEP-PATH SUMMARY")
    P(f"  4a passes: {int(G.pass4a.sum())} / {len(G)}   4b passes: {int(G.pass4b.sum())} / {len(G)}"
      f"   BOTH: {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for pname in PN:
        g = G[G.panel == pname]
        P(f"    {pname:9s} 4a {int(g.pass4a.sum()):2d}/{len(g)}  4b {int(g.pass4b.sum()):2d}/{len(g)}"
          f"   4b by band: " + " ".join(
              f"{b:.2f}:{int(g[g.band == b].pass4b.sum())}/{len(g[g.band == b])}" for b in BANDS))
    both = G[G.pass4b]
    if len(both):
        P("\n  every 4b passer:")
        P(fmt(both[cols]))
    # cells passing 4b on BOTH required panels at the same (band, gross, con)
    key = ["band", "gross", "con"]
    piv = G[G.panel.isin(REQUIRED_PANELS)].pivot_table(index=key, columns="panel", values="pass4b")
    dual = piv[(piv[REQUIRED_PANELS[0]] == 1) & (piv[REQUIRED_PANELS[1]] == 1)]
    P(f"\n  cells clearing 4b on BOTH required panels: {len(dual)} / {len(piv)}")
    if len(dual):
        P(fmt(dual))
    flush_log()
    P("\nDone.")
    flush_log()


if __name__ == "__main__":
    main()
