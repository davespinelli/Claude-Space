#!/usr/bin/env python3
"""Idea 543 - "is-the-BAND-a-TURNOVER-dial-with-a-free-SHARPE" (cloud, 2026-09-09).

The question
------------
Idea 542 priced ONE band pair (0.00 vs the live 0.03) and found the Sharpe edge straddles
zero on both required panels while the turnover saving is deterministic (1.79 vs 3.15 x/yr,
-43%).  If the band buys turnover and not Sharpe, then the band that SHOULD be live is the
one that maximises NET-OF-COST Sharpe at the cost rung the book actually trades at, and the
live 0.03 is either that argmax or an arbitrary point on a flat ridge.

This run prices the WHOLE band grid on net-of-cost Sharpe at 0 / 10 / 25 / 50 bps and reports
the argmax band per rung, the width of the ridge around it, and whether 0.03 is
distinguishable from the argmax at all.

Design (fixed before any number was read)
-----------------------------------------
FIXED, never varied:
    cadence       W (weekly) -- the LIVE cadence and the record default
    gross         0.75 -- LIVE.  (Idea 542 measured Sharpe gross-invariance to 3 dp on this
                  family; gross is therefore NOT informative for a Sharpe argmax and is held.)
    execution     weights decided at close t, applied at t+1 (PROTOCOL 2)
    gate          200d MA band with hysteresis, exactly baseline.band_state
    windows       IS <= 2016-12-31, OOS >= 2017-01-01 (PROTOCOL rule 8)
    panels        U56 and B136 REQUIRED; SMALL439 reported only
    baseline      the live RULES v2 book computed on U56 and reindexed onto each panel
                  (idea 299 / 542 convention verbatim), plus SPY

TUNED PARAMETERS -- exactly two, as the queue specifies (band, cost rung):
    1. BAND      11 values {0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.12, 0.15}.
                 0.03 is the LIVE incumbent; 0.00 is idea 542's challenger (MA-THRESH theta=0).
    2. COST RUNG 4 values {0, 10, 25, 50} bps per unit turnover.  10 is the PROTOCOL rung and
                 the only one a KEEP may be claimed on; 0/25/50 are the sensitivity ladder.
    CONSTRUCTION is NOT a third dial: DEGROSS (gated-out weight -> cash) is the LIVE form and
    the pre-registered one; RESPREAD is reported as a control.  Any KEEP claim comes from
    DEGROSS at 10 bps only.
    11 bands x 4 rungs x 2 constructions x 3 panels = 264 book-rungs, ALL reported.

Pre-registered bars, written before any number was read
--------------------------------------------------------
B1  THE ARGMAX.  Per (panel, construction, rung): the band maximising full-sample net Sharpe.
    The live 0.03 is "the cost-implied optimum" iff it is the argmax at 10 bps on BOTH
    required panels under DEGROSS.  Reported for every rung either way.
B2  IS THE RIDGE FLAT?  Per (panel, construction, rung): the Sharpe SPAN across the 11 bands,
    and the count of bands within 0.02 Sharpe of the argmax (a ridge tolerance fixed here,
    ~1/3 of the 0.0655 pooled Sharpe SD idea 542 measured across its band axis).  A ridge
    holding >= 5 of 11 bands means the argmax is not a readable number.
B3  IS THE ARGMAX DISTINGUISHABLE FROM THE LIVE BAND?  Paired circular-block bootstrap
    (2000 draws, 21d blocks, seed 0) of the daily net-return Sharpe difference
    (argmax band - live 0.03) at 10 bps, DEGROSS, both required panels.  A CI straddling zero
    means the argmax is a draw, not a dial setting.
B4  THE TURNOVER LEG.  Turnover x/yr by band, and the IMPLIED BREAKEVEN cost rung: the bps at
    which each band's net Sharpe overtakes 0.03's, solved on the two-point line through the
    measured rungs.  This is what "a turnover dial with a free Sharpe" means quantitatively.
B5  RULE 8 (PROTOCOL 8).  Band chosen on IS (<= 2016) net Sharpe ONLY, separately at each cost
    rung, per panel and pooled over the two required panels; OOS (>= 2017) read ONCE.  Report
    OOS CAGR / Sharpe / MaxDD vs the RULES v2 baseline and vs SPY.  A KEEP needs the IS-chosen
    band to clear 4b's OOS leg on BOTH required panels.
B6  BOTH KEEP PATHS on all 264 book-rungs:
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 60% of SPY's, CAGR >= 70% of SPY's.

Gates (asserted before any verdict is read)
    G1  the vectorised runner reproduces engine.backtest on the live U56 v2 book to < 1e-12.
    G2  BAND=0.03 / GROSS=0.75 / DEGROSS is bit-identical to baseline.rules_v2_weights.
    G3  reproduction of idea 542: this run's (band 0.00 - band 0.03) dSharpe at gross 0.75,
        DEGROSS, 10 bps must match idea 542's committed .paired.csv to < 5e-4 on every panel.

SURVIVORSHIP: universe.json (U56), universe_broad.json (B136) and prices_small.csv.gz
(SMALL439) are CURRENT constituents -- no delistings -- so every CAGR level here is inflated
and both KEEP columns inherit that whole.  SMALL439 additionally drops every ticker with
max_1d_move >= 1.0 in data/small_meta.csv.  Any memo written off this run carries that caveat.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .argmax.csv .boot.csv .breakeven.csv .walkforward.csv .console.txt .result.md
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights, band_state
from engine import backtest, metrics, rebalance_mask

CADENCE = "W"
GROSS = 0.75                       # LIVE, held fixed (not a dial)
BANDS = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.12, 0.15]
RUNGS = [0, 10, 25, 50]            # bps per unit turnover; 10 = PROTOCOL
PROTOCOL_RUNG = 10
LIVE_BAND = 0.03
CONSTRUCTIONS = ["DEGROSS", "RESPREAD"]
LIVE_CON = "DEGROSS"
REQUIRED_PANELS = ["U56", "B136"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
RIDGE_TOL = 0.02                   # Sharpe units, fixed a priori (B2)
BOOT_DRAWS, BOOT_BLOCK, BOOT_SEED = 2000, 21, 0
IDEA542 = REPO / "research" / "backtests" / (
    "2026-09-09_does-MA-THRESH-theta-0-beat-RULES-v2-s-3-percent-BAND-on-its-own-terms_C.paired.csv")

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 900)


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
    """Reproduces engine.backtest exactly (gate G1); returns GROSS-of-cost returns + turnover."""
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


def net(res, bps):
    return res["returns0"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- books
def held_mask(px, band):
    return band_state(px, band) & px.notna()


def book(px, band, gross, construction):
    h = held_mask(px, band)
    den = px.notna().sum(axis=1) if construction == "DEGROSS" else h.sum(axis=1)
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


# ---------------------------------------------------------------- bootstrap
def block_boot_diff(ra, rb, draws=BOOT_DRAWS, block=BOOT_BLOCK, seed=BOOT_SEED):
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
    P("Idea 543 is-the-BAND-a-TURNOVER-dial-with-a-free-SHARPE (cloud) | " + Path(__file__).name)
    P("=" * 180)
    P(f"FIXED: cadence {CADENCE} (live), gross {GROSS} (live), next-day execution, "
      f"IS <= {IS_END}, OOS >= {OOS_START}.")
    P(f"DIALS (2): BAND {BANDS} x COST RUNG {RUNGS} bps.")
    P(f"CONSTRUCTION {CONSTRUCTIONS}: DEGROSS is live and pre-registered; RESPREAD is a reported "
      f"control.  KEEP claims only from DEGROSS at {PROTOCOL_RUNG} bps.")
    P(f"Incumbent = band {LIVE_BAND} (RULES v2 clause 2).  Ridge tolerance {RIDGE_TOL} Sharpe (a priori).")
    P("SURVIVORSHIP: all three panels are current constituents; every CAGR level is inflated.")

    PN = panels()

    # ------------------------------------------------------------ gates G1, G2
    P("\n" + "=" * 180)
    P("GATES")
    px_full = load_universe()
    w_live = rules_v2_weights(px_full)
    r_engine = backtest(px_full, w_live, cost_bps=PROTOCOL_RUNG, freq=CADENCE)["returns"]
    fb = fast_backtest(px_full, w_live)
    g1 = float(np.abs(r_engine - net(fb, PROTOCOL_RUNG)).max())
    P(f"  G1 vectorised runner vs engine.backtest on the live U56 v2 book: max abs diff {g1:.3e} "
      f"({'PASS' if g1 < 1e-12 else 'FAIL'})")
    assert g1 < 1e-12, g1

    g2 = float((book(px_full, LIVE_BAND, GROSS, "DEGROSS") - w_live).abs().max().max())
    P(f"  G2 book(band=0.03, gross=0.75, DEGROSS) vs baseline.rules_v2_weights: max abs diff "
      f"{g2:.3e} ({'PASS' if g2 < 1e-15 else 'FAIL'})")
    assert g2 < 1e-15, g2
    flush_log()

    # ------------------------------------------------------------ grid
    live_full = r_engine
    rows, panel_spy, panel_live, ret_cache = [], {}, {}, {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        panel_spy[pname], panel_live[pname] = spy_s, live_s
        P("\n" + "-" * 180)
        P(f"PANEL {pname}: evaluation from {start.date()} ({years:.2f} yrs)"
          f"{'  [REQUIRED]' if pname in REQUIRED_PANELS else '  [reported, not required]'}")
        P(f"  SPY      CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS CAGR {spy_s['oCAGR']:.4f} "
          f"OOS Sharpe {spy_s['oSharpe']:.4f} OOS MaxDD {spy_s['oMaxDD']:.4f}")
        P(f"  RULES v2 CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} "
          f"halves {live_s['H1']:.4f}/{live_s['H2']:.4f} OOS CAGR {live_s['oCAGR']:.4f} "
          f"OOS Sharpe {live_s['oSharpe']:.4f} OOS MaxDD {live_s['oMaxDD']:.4f}")
        P(f"  4b bars: H1>{spy_s['H1']:.4f} H2>{spy_s['H2']:.4f} OOS>{spy_s['oSharpe']:.4f} "
          f"|MaxDD|<={0.60 * abs(spy_s['MaxDD']):.2%} CAGR>={0.70 * spy_s['CAGR']:.2%}")

        for band in BANDS:
            h = held_mask(px, band).loc[start:]
            for con in CONSTRUCTIONS:
                res = fast_backtest(px, book(px, band, GROSS, con))
                turn = res["turnover"].loc[start:]
                for bps in RUNGS:
                    r = net(res, bps).loc[start:]
                    s = stat(r)
                    rows.append(dict(
                        panel=pname, band=band, con=con, bps=bps, gross=GROSS, cad=CADENCE, **s,
                        nheld_mean=float(h.sum(axis=1).mean()),
                        turn_yr=float(turn.sum() / years),
                        pass4a=verdict_4a(s, live_s), pass4b=all(bars_4b(s, spy_s).values()),
                        fail4b=fail_4b(s, spy_s)))
                    ret_cache[(pname, band, con, bps)] = r
        flush_log()

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ------------------------------------------------------------ G3 reproduction of idea 542
    P("\n  G3 reproduction of idea 542's head-to-head (band 0.00 - band 0.03, gross 0.75, "
      "DEGROSS, 10 bps):")
    if IDEA542.exists():
        ref = pd.read_csv(IDEA542)
        ref = ref[(ref.gross == GROSS) & (ref.con == LIVE_CON)]
        worst = 0.0
        for _, rr in ref.iterrows():
            a = G[(G.panel == rr.panel) & (G.band == 0.00) & (G.con == LIVE_CON) & (G.bps == PROTOCOL_RUNG)].iloc[0]
            b = G[(G.panel == rr.panel) & (G.band == LIVE_BAND) & (G.con == LIVE_CON) & (G.bps == PROTOCOL_RUNG)].iloc[0]
            d = a.Sharpe - b.Sharpe
            e = abs(d - rr.dSharpe)
            worst = max(worst, e)
            P(f"     {rr.panel:9s} this run dSharpe {d:+.6f} | idea 542 {rr.dSharpe:+.6f} | "
              f"|diff| {e:.2e}")
        P(f"     max |diff| {worst:.3e} ({'PASS' if worst < 5e-4 else 'FAIL'})")
        assert worst < 5e-4, worst
    else:
        P(f"     SKIPPED: {IDEA542.name} not found")
    flush_log()

    P("\n" + "=" * 180)
    P(f"FULL GRID ({len(G)} book-rungs; every point reported, none selected on)")
    cols = ["band", "con", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "oCAGR", "oSharpe", "oMaxDD", "nheld_mean", "turn_yr", "pass4a", "pass4b", "fail4b"]
    for pname in PN:
        P(f"\n--- {pname} " + "-" * 150)
        P(fmt(G[G.panel == pname][cols].set_index(["con", "bps", "band"]).sort_index()))
    flush_log()

    # ------------------------------------------------------------ B1/B2 argmax + ridge
    P("\n" + "=" * 180)
    P("B1/B2  NET-OF-COST SHARPE BY BAND AND RUNG: argmax band, ridge width, live-band rank")
    am = []
    for pname in PN:
        for con in CONSTRUCTIONS:
            for bps in RUNGS:
                sub = G[(G.panel == pname) & (G.con == con) & (G.bps == bps)].set_index("band")
                sh = sub.Sharpe
                best_band = float(sh.idxmax())
                live_sh = float(sh.loc[LIVE_BAND])
                within = sh[sh >= sh.max() - RIDGE_TOL]
                am.append(dict(
                    panel=pname, con=con, bps=bps, argmax_band=best_band,
                    argmax_Sharpe=float(sh.max()), live_Sharpe=live_sh,
                    d_live_vs_argmax=live_sh - float(sh.max()),
                    live_is_argmax=bool(best_band == LIVE_BAND),
                    live_rank=int(sh.rank(ascending=False).loc[LIVE_BAND]),
                    span=float(sh.max() - sh.min()),
                    n_within_tol=int(len(within)),
                    ridge_lo=float(within.index.min()), ridge_hi=float(within.index.max()),
                    live_in_ridge=bool(LIVE_BAND in set(within.index)),
                    argmax_CAGR=float(sub.CAGR.loc[best_band]),
                    argmax_MaxDD=float(sub.MaxDD.loc[best_band]),
                    argmax_turn=float(sub.turn_yr.loc[best_band]),
                    live_turn=float(sub.turn_yr.loc[LIVE_BAND])))
    A = pd.DataFrame(am)
    A.to_csv(f"{OUT}.argmax.csv", index=False)
    P("\n  net Sharpe surface (rows = band, cols = rung), per panel and construction:")
    for pname in PN:
        for con in CONSTRUCTIONS:
            t = G[(G.panel == pname) & (G.con == con)].pivot_table(
                index="band", columns="bps", values="Sharpe")
            P(f"\n    --- {pname} / {con}")
            P(fmt(t))
    P("\n  argmax / ridge table:")
    P(fmt(A.set_index(["panel", "con", "bps"])))
    liveargmax = A[(A.con == LIVE_CON) & (A.bps == PROTOCOL_RUNG) & (A.panel.isin(REQUIRED_PANELS))]
    P(f"\n  B1: the live band {LIVE_BAND} is the {PROTOCOL_RUNG} bps DEGROSS argmax on "
      f"{int(liveargmax.live_is_argmax.sum())} / {len(liveargmax)} required panels.")
    P(f"  B1 across ALL cells: live band is argmax in {int(A.live_is_argmax.sum())} / {len(A)}.")
    P(f"  B2: mean bands within {RIDGE_TOL} Sharpe of the argmax = {A.n_within_tol.mean():.2f} of "
      f"{len(BANDS)}; live band inside that ridge in {int(A.live_in_ridge.sum())} / {len(A)} cells; "
      f"mean Sharpe span across the band axis {A.span.mean():.4f}.")
    flush_log()

    # ------------------------------------------------------------ B3 bootstrap argmax vs live
    P("\n" + "=" * 180)
    P(f"B3  IS THE ARGMAX DISTINGUISHABLE FROM THE LIVE BAND?  paired circular-block bootstrap "
      f"({BOOT_DRAWS} draws, {BOOT_BLOCK}d blocks, seed {BOOT_SEED}) at {PROTOCOL_RUNG} bps, "
      f"{LIVE_CON}.  Positive = argmax band better.")
    br = []
    for pname in PN:
        row = A[(A.panel == pname) & (A.con == LIVE_CON) & (A.bps == PROTOCOL_RUNG)].iloc[0]
        bb = row.argmax_band
        ra = ret_cache[(pname, bb, LIVE_CON, PROTOCOL_RUNG)]
        rb = ret_cache[(pname, LIVE_BAND, LIVE_CON, PROTOCOL_RUNG)]
        if bb == LIVE_BAND:
            br.append(dict(panel=pname, argmax_band=bb, dSharpe=0.0, boot_lo=0.0, boot_hi=0.0,
                           straddles_0=True, dCAGR_pp=0.0, cagr_lo_pp=0.0, cagr_hi_pp=0.0,
                           prob_argmax_better=np.nan, note="argmax IS the live band"))
            continue
        ds, dc = block_boot_diff(ra, rb)
        lo_s, hi_s = ci(ds); lo_c, hi_c = ci(dc)
        br.append(dict(panel=pname, argmax_band=bb,
                       dSharpe=metrics(ra)["Sharpe"] - metrics(rb)["Sharpe"],
                       boot_lo=lo_s, boot_hi=hi_s, straddles_0=bool(lo_s <= 0 <= hi_s),
                       dCAGR_pp=100 * (metrics(ra)["CAGR"] - metrics(rb)["CAGR"]),
                       cagr_lo_pp=100 * lo_c, cagr_hi_pp=100 * hi_c,
                       prob_argmax_better=float((ds > 0).mean()), note=""))
    B = pd.DataFrame(br).set_index("panel")
    B.to_csv(f"{OUT}.boot.csv")
    P(fmt(B))
    flush_log()

    # ------------------------------------------------------------ B4 turnover + breakeven
    P("\n" + "=" * 180)
    P("B4  THE TURNOVER LEG.  Turnover (x/yr) by band, and the cost rung at which each band's "
      "net Sharpe would overtake the live 0.03 (linear in bps through the 0 and 50 bps points; "
      "'never' = the sign never flips inside 0-200 bps).")
    bk = []
    for pname in PN:
        for con in CONSTRUCTIONS:
            sub = G[(G.panel == pname) & (G.con == con)]
            s0 = sub[sub.bps == 0].set_index("band").Sharpe
            s50 = sub[sub.bps == 50].set_index("band").Sharpe
            turn = sub[sub.bps == 0].set_index("band").turn_yr
            for band in BANDS:
                d0 = s0.loc[band] - s0.loc[LIVE_BAND]
                d50 = s50.loc[band] - s50.loc[LIVE_BAND]
                slope = (d50 - d0) / 50.0
                if band == LIVE_BAND:
                    be = np.nan
                elif slope == 0:
                    be = np.nan
                else:
                    x = -d0 / slope
                    be = x if 0 <= x <= 200 else np.nan
                bk.append(dict(panel=pname, con=con, band=band, turn_yr=float(turn.loc[band]),
                               dturn_vs_live=float(turn.loc[band] - turn.loc[LIVE_BAND]),
                               dSharpe_0bps=float(d0), dSharpe_50bps=float(d50),
                               slope_per_bps=float(slope), breakeven_bps=float(be)))
    K = pd.DataFrame(bk)
    K.to_csv(f"{OUT}.breakeven.csv", index=False)
    for pname in PN:
        P(f"\n--- {pname} " + "-" * 150)
        P(fmt(K[K.panel == pname].drop(columns=["panel"]).set_index(["con", "band"])))
    flush_log()

    # ------------------------------------------------------------ B5 rule 8
    P("\n" + "=" * 180)
    P(f"B5  RULE 8: band chosen on IS (<= {IS_END}) net Sharpe ONLY, separately per cost rung; "
      f"OOS (>= {OOS_START}) read ONCE.")
    P("\n  IS net Sharpe by band (the selection surface), DEGROSS:")
    for pname in list(PN):
        t = G[(G.panel == pname) & (G.con == LIVE_CON)].pivot_table(
            index="band", columns="bps", values="isSharpe")
        P(f"\n    --- {pname} / {LIVE_CON}")
        P(fmt(t))
    pooled = G[(G.con == LIVE_CON) & (G.panel.isin(REQUIRED_PANELS))].pivot_table(
        index="band", columns="bps", values="isSharpe")
    P(f"\n    --- POOLED({','.join(REQUIRED_PANELS)}) / {LIVE_CON}  (mean IS Sharpe)")
    P(fmt(pooled))

    wf = []
    for con in CONSTRUCTIONS:
        for bps in RUNGS:
            # per panel
            for pname in PN:
                sub = G[(G.panel == pname) & (G.con == con) & (G.bps == bps)]
                pick = sub.loc[sub.isSharpe.idxmax()]
                spy, base = panel_spy[pname], panel_live[pname]
                wf.append(dict(mode="perpanel", con=con, bps=bps, panel=pname, band=pick.band,
                               isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                               oMaxDD=pick.oMaxDD, spy_oCAGR=spy["oCAGR"], spy_oSharpe=spy["oSharpe"],
                               spy_oMaxDD=spy["oMaxDD"], base_oCAGR=base["oCAGR"],
                               base_oSharpe=base["oSharpe"], base_oMaxDD=base["oMaxDD"],
                               oos_beats_spy=bool(pick.oSharpe > spy["oSharpe"]),
                               oos_beats_base=bool(pick.oSharpe > base["oSharpe"]),
                               is_live_band=bool(pick.band == LIVE_BAND),
                               pass4b_full=bool(pick.pass4b), fail4b=pick.fail4b))
            # pooled over the required panels
            sub = G[(G.con == con) & (G.bps == bps) & (G.panel.isin(REQUIRED_PANELS))]
            pick_band = float(sub.groupby("band").isSharpe.mean().idxmax())
            for rp in REQUIRED_PANELS:
                r = G[(G.panel == rp) & (G.band == pick_band) & (G.con == con) & (G.bps == bps)].iloc[0]
                spy, base = panel_spy[rp], panel_live[rp]
                wf.append(dict(mode="pooled", con=con, bps=bps, panel=rp, band=pick_band,
                               isSharpe=r.isSharpe, oCAGR=r.oCAGR, oSharpe=r.oSharpe,
                               oMaxDD=r.oMaxDD, spy_oCAGR=spy["oCAGR"], spy_oSharpe=spy["oSharpe"],
                               spy_oMaxDD=spy["oMaxDD"], base_oCAGR=base["oCAGR"],
                               base_oSharpe=base["oSharpe"], base_oMaxDD=base["oMaxDD"],
                               oos_beats_spy=bool(r.oSharpe > spy["oSharpe"]),
                               oos_beats_base=bool(r.oSharpe > base["oSharpe"]),
                               is_live_band=bool(pick_band == LIVE_BAND),
                               pass4b_full=bool(r.pass4b), fail4b=r.fail4b))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n" + fmt(W.set_index(["mode", "con", "bps", "panel"]).sort_index()))
    P(f"\n  rule 8: IS-chosen band equals the live {LIVE_BAND} in {int(W.is_live_band.sum())} / "
      f"{len(W)} (mode, con, rung, panel) cells.")
    P(f"  rule 8 OOS: picks beat SPY in {int(W.oos_beats_spy.sum())} / {len(W)}; beat RULES v2 in "
      f"{int(W.oos_beats_base.sum())} / {len(W)}; clear full-sample 4b in "
      f"{int(W.pass4b_full.sum())} / {len(W)}.")
    flush_log()

    # ------------------------------------------------------------ B6 keep paths
    P("\n" + "=" * 180)
    P("B6  KEEP-PATH SUMMARY (both paths, all book-rungs)")
    P(f"  4a passes: {int(G.pass4a.sum())} / {len(G)}   4b passes: {int(G.pass4b.sum())} / {len(G)}"
      f"   BOTH: {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for pname in PN:
        g = G[G.panel == pname]
        P(f"    {pname:9s} 4a {int(g.pass4a.sum()):3d}/{len(g)}  4b {int(g.pass4b.sum()):3d}/{len(g)}"
          f"   4b by rung: " + " ".join(
              f"{b}bps:{int(g[g.bps == b].pass4b.sum())}/{len(g[g.bps == b])}" for b in RUNGS))
    P("\n  4b fail-bar frequency (all cells): " + ", ".join(
        f"{k}={v}" for k, v in G.fail4b.value_counts().head(12).items()))
    key = ["band", "con", "bps"]
    piv = G[G.panel.isin(REQUIRED_PANELS)].pivot_table(index=key, columns="panel", values="pass4b")
    dual = piv[(piv[REQUIRED_PANELS[0]] == 1) & (piv[REQUIRED_PANELS[1]] == 1)]
    P(f"\n  cells clearing 4b on BOTH required panels: {len(dual)} / {len(piv)}")
    if len(dual):
        P(fmt(dual))
        P("\n  their full rows:")
        for (b, c, r) in dual.index:
            P(fmt(G[(G.band == b) & (G.con == c) & (G.bps == r) &
                    (G.panel.isin(REQUIRED_PANELS))][["panel"] + cols].set_index(["panel", "band"])))
    flush_log()
    P("\nDone.")
    flush_log()


if __name__ == "__main__":
    main()
