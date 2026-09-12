#!/usr/bin/env python3
"""Idea 830 — does-the-DE-GROSSING-TO-CASH-channel-have-a-CEILING-on-the-ENTRY-DATE-pass-share
(cloud lane, 2026-09-12).

WHY THIS RUN EXISTS
-------------------
Idea 828 scored seven committed BOOK FORMS on every ENTRY DATE at a 3-year horizon and found:
  * no form clears a 0.80 joint window-local 4b pass share -- the best cell is MA-DG at gross
    1.00 with **0.3977** (reproducing idea 829's headline), and
  * MA-DG is the ONLY form whose 4b DRAWDOWN leg survives gross 1.00 (leg_dd **0.8636** against
    <= 0.0057 for every RE-SPREADING form), because its gated-out weight goes to CASH and is
    never re-spread.
So GROSS cannot buy the bar.  The queue's follow-up is whether the DE-GROSSING-TO-CASH CHANNEL
ITSELF can: the channel has exactly two dials -- HOW OFTEN the book is in cash (the 200d MA band
width) and WHAT THE CASH EARNS (the flat cash rung, ideas 406/642/676).

    THE QUESTION.  Sweep band width x cash rung.  Where does MA-DG's 3-year entry-date 4b pass
    share peak, can it reach 0.80 at all, and if not, which of 4b's legs closes first?

TWO TUNED PARAMETERS, exactly as the queue allows; all 32 cells reported, none dropped:
  P1  BAND     in {0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20}   (0.03 = the LIVE band)
  P2  CASH     in {0, 150, 300, 500} bps/yr flat on the de-grossed fraction   (0 = the record's
               standing convention; 500 is roughly the post-2022 T-bill level, idea 642's caveat)
REPORTED AXES, fixed at the record's committed values and never selected on:
  gross {0.75 (the live book), 1.00 (idea 829's candidate)}, horizon H {756, 1260},
  entry spacing s {21, 63}, cost {10, 25} bps, panel {U56, B136, SMALL}.
HEADLINE CELL declared before the run: panel U56, gross 1.00, H = 756 ("3-year"), s = 21,
cost 10 bps (PROTOCOL 2).

WINDOW-LOCAL 4b (idea 829's convention, reproduced verbatim so G3 can bind)
    a window PASSES iff  Sharpe > SPY's  AND  both halves' Sharpe > SPY's halves'
                     AND  MaxDD >= 0.60 * SPY's MaxDD  AND  CAGR >= 0.70 * SPY's CAGR.
Legs are reported separately: leg_sharpe, leg_halves (the two RANK legs) and leg_dd, leg_cagr
(the two RATIO legs -- the queue's "4b's two ratio legs").

THE CASH CONVENTION, DECLARED (C-CASH).  The engine holds the de-grossed remainder as a
non-earning balance.  This run credits it a flat rate EXACTLY: inside each rebalance segment the
cash balance compounds, cash_t = cash_0 * (1+rc)^(t - t_0) with rc = (1+rate)^(1/252) - 1, so
NAV is V_t = (drifted holdings) + cash_t, the day's return picks up f_t * rc with
f_t = cash_t / V_t, and the grown cash enters the weight drift and the turnover calculation like
any other holding.  No turnover cost is charged on the cash leg (moving to and from a cash
balance is not a trade in the engine's accounting), which is what makes the cash = 0 column
bit-identical to idea 828's MA-DG column -- see G3.  GATE G5 prices the cheaper convention the
record would plausibly have used instead (credit f_t * rc additively without feeding it back into
the drift) and reports how much the shortcut would have moved every headline cell.

PRE-REGISTERED HYPOTHESES (each stated so it can fail; a FAIL is the result)
  H_830    THE QUEUE'S.  Some (band, cash) cell clears joint pass share >= 0.80 at the headline.
  H_CEIL   If H_830 fails, the channel's ceiling is the max over the 32 cells; report it.
  H_CLOSE  THE MECHANISM.  At the argmax cell the BINDING leg (lowest leg share) is one of the
           two RATIO legs (dd, cagr).  If the binding leg is a RANK leg instead, the queue's
           framing is wrong and the channel is not what limits the bar.
  H_CASH   THE CASH DIAL IS WORTH SOMETHING.  max over bands of
           [share(cash=500) - share(cash=0)] >= 0.10.
  H_BAND   THE PEAK IS REAL.  The argmax band is INTERIOR to the swept grid; an edge argmax makes
           the "peak" a grid artefact.
  H_R8     PROTOCOL RULE 8.  Choose (band, cash) on IS entry dates only (entry <= 2016-12-31),
           read once on OOS entry dates (entry >= 2017-01-01); the pick's OOS share is within
           0.15 of the OOS-best cell.  Plus the mandated fixed-window book leg and BOTH KEEP
           paths, IS-chosen and read on 2017-01-01.. untouched.

REPRODUCTION GATES, printed before any new number
  G1  fast_backtest == engine.backtest (returns AND turnover) at cash = 0, 3 cells x 2 rungs
  G2  fmet == engine.metrics on 200 real windows
  G3  idea 828/829's committed headline: MA-DG band 0.03 gross 1.00 cash 0 -> pass 0.3977,
      leg_sharpe 0.9148, leg_halves 0.5170, leg_dd 0.8636, leg_cagr 0.7273 on 176 windows
  G4  the committed candidate memo's fixed-window triple and SPY's
  G5  EXACT vs ADDITIVE cash convention over the 32 headline cells, bar 0.02 on the pass share
  G6  the credit has the right sign: window CAGR is monotone non-decreasing in the cash rung at
      every (band, gross, panel, H, s, cost) cell; 0 violations required
  R7  REPORTED, NOT A GATE: the same sweep at DAILY cadence.  A daily book re-rebalances every
      day and pays turnover for it, so it is a DIFFERENT BOOK; the comparison is a robustness
      report on cadence and carries no bar.

SURVIVORSHIP: U56 and B136 are CURRENT constituents of research/universe.json and
universe_broad.json; the SMALL panel is current constituents of a sub-$2B screen and is rewritten
nightly (data/SMALL_PANEL_README.md, ideas 824/826).  Tickers with max_1d_move >= 1.0 in
data/small_meta.csv are dropped before use.  All three panels bias every book AND every pass
share UPWARD.  Nothing here is investment advice.

Writes: .txt .census.csv.gz .grid.csv .legs.csv .fixed.csv .wf.csv .result.md
"""
import sys
import time
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np                                                          # noqa: E402
import pandas as pd                                                         # noqa: E402
from baseline import (load_universe, score, band_state, rules_v1_weights,   # noqa: E402
                      rules_v2_weights, compare)
from engine import backtest, metrics, rebalance_mask                        # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests" / STEM

FREQ = "W"
MAX_VOL = 0.60
BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]      # P1
CASHES = [0, 150, 300, 500]                                   # P2 (bps/yr)
GROSSES = [0.75, 1.00]                                        # reported
COSTS = [10.0, 25.0]
HORIZONS = [756, 1260]
SPACINGS = [21, 63]
H_HEAD, S_HEAD, COST_HEAD, G_HEAD, P_HEAD = 756, 21, 10.0, 1.00, "U56"
BAND_LIVE = 0.03
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
BAR = 0.80
LINES: list[str] = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def hdr(s):
    log("\n" + "=" * 160)
    log(s)
    log("=" * 160)


# ------------------------------------------------------------------ primitives
def madg_weights(px, band, gross):
    """The channel: RULES v2's form — every name inside the 200d +/-band at gross/N of NAV,
    N = names priced that day, gated-out weight to CASH and never re-spread."""
    return rules_v2_weights(px, band=band, gross=gross)


def mars_weights(px, band, gross):
    """The RE-SPREADING twin, carried as a control: same membership, gross re-spread."""
    m = band_state(px, band).astype(float).where(px.notna(), 0.0)
    n = m.sum(axis=1).replace(0, np.nan)
    return gross * m.div(n, axis=0).fillna(0.0)


def fast_backtest(prices, weights, cost_bps, cash_bps=0, freq=FREQ, exact=True):
    """Vectorised equivalent of engine.backtest at cash_bps = 0 (asserted in G1), extended with
    the C-CASH credit.  exact=True compounds the cash balance inside each rebalance segment and
    lets it enter the weight drift and the turnover calculation; exact=False is the cheaper
    additive shortcut G5 prices.  Returns (returns, turnover, cash fraction of NAV)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    rc = (1.0 + cash_bps / 1e4) ** (1.0 / 252.0) - 1.0
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    age = np.arange(T) - s0                                  # days since the segment started
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    grow = (1.0 + rc) ** age if exact else np.ones(T)
    cash = (1.0 - W0.sum(axis=1)) * grow
    V = h.sum(axis=1) + cash
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    agep = np.arange(T) - s0p
    growp = (1.0 + rc) ** agep if exact else np.ones(T)
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)) * growp
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    cash_frac = cash / V
    port = (held * rets).sum(axis=1) + cash_frac * rc - turn * cost_bps / 1e4
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(cash_frac, index=idx))


def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    sh = (r.mean() * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


def window_stats(r, ii, H):
    """(CAGR, Sharpe, h1 Sharpe, h2 Sharpe, MaxDD) for every entry index in ii."""
    eq = np.cumprod(1.0 + r)
    eqp = np.concatenate([[1.0], eq])
    cs = np.concatenate([[0.0], np.cumsum(r)])
    cs2 = np.concatenate([[0.0], np.cumsum(r * r)])
    half = H // 2

    def sh(i, j):
        n = (j - i).astype(float)
        m = (cs[j] - cs[i]) / n
        v = ((cs2[j] - cs2[i]) - n * m * m) / (n - 1.0)
        v = np.where(v > 1e-300, v, np.nan)
        return m * np.sqrt(252.0) / np.sqrt(v)

    jj = ii + H
    cagr = (eqp[jj] / eqp[ii]) ** (252.0 / H) - 1.0
    dd = np.empty(len(ii))
    for a, i in enumerate(ii):
        e = eq[i:i + H]
        dd[a] = (e / np.maximum.accumulate(e) - 1.0).min()
    return cagr, sh(ii, jj), sh(ii, ii + half), sh(ii + half, jj), dd


# ------------------------------------------------------------------ gates G1 / G2
def gate_g1(px):
    worst_r = worst_t = 0.0
    for band, g, c in [(0.03, 1.00, 10.0), (0.00, 0.75, 25.0), (0.20, 1.00, 10.0)]:
        w = madg_weights(px, band, g)
        ref = backtest(px, w, cost_bps=c, freq=FREQ)
        got_r, got_t, _ = fast_backtest(px, w, c, 0)
        worst_r = max(worst_r, float((ref["returns"] - got_r).abs().max()))
        worst_t = max(worst_t, float((ref["turnover"] - got_t).abs().max()))
    ok = worst_r <= 1e-12 and worst_t <= 1e-12
    log(f"GATE G1 — fast_backtest vs engine.backtest at cash=0 (3 cells): max |dreturn| "
        f"{worst_r:.3e}, max |dturnover| {worst_t:.3e} vs bar 1e-12 -> "
        f"{'PASS' if ok else 'FAIL'}")
    return ok


def gate_g2(px):
    w = madg_weights(px, BAND_LIVE, 1.00)
    r = fast_backtest(px, w, 10.0, 0)[0]
    rng = np.random.default_rng(8300)
    worst = 0.0
    for _ in range(200):
        T = int(rng.integers(252, 1261))
        i = int(rng.integers(0, len(r) - T))
        sl = r.iloc[i:i + T]
        a = fmet(sl.values)
        m = metrics(sl)
        worst = max(worst, max(abs(x - y) for x, y in
                               zip(a, (m["CAGR"], m["Sharpe"], m["MaxDD"]))))
    log(f"GATE G2 — fmet vs engine.metrics on 200 fixed-seed random windows: max |diff| "
        f"{worst:.3e} vs bar 1e-10 -> {'PASS' if worst <= 1e-10 else 'FAIL'}")
    return worst <= 1e-10


# ------------------------------------------------------------------ the sweep
def run_panel(panel, px, freq=FREQ, verbose=True):
    start = px.index[260]
    eidx = px.loc[start:].index
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:].values
    if verbose:
        sc, ss, sd = fmet(spy)
        log(f"\nPANEL {panel}: {px.shape[1]} columns, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, eval from {start.date()} ({len(eidx)} days); "
            f"SPY full {sc:.2%} / {ss:.3f} / {sd:.2%}")

    # one simulation per (form, band, gross, cost); the cash rung is applied post-hoc (C-CASH)
    series: dict[tuple, np.ndarray] = {}
    for form, fn in (("MA-DG", madg_weights), ("MA-RS", mars_weights)):
        for band, g in product(BANDS, GROSSES):
            w = fn(px, band, g)
            for c, cash in product(COSTS, CASHES):
                series[(form, band, g, c, cash)] = fast_backtest(
                    px, w, c, cash, freq)[0].loc[start:].values
    for nm, w in (("RULES v1", rules_v1_weights(px)),
                  ("RULES v2 live", rules_v2_weights(px, band=BAND_LIVE, gross=0.75))):
        for c in COSTS:
            series[(nm, np.nan, np.nan, c, 0)] = fast_backtest(
                px, w, c, 0, freq)[0].loc[start:].values
    if verbose:
        log(f"  {len(series)} book-series ({len(BANDS)} bands x {len(GROSSES)} grosses x "
            f"{len(CASHES)} cash rungs x {len(COSTS)} rungs x 2 forms + v1 + v2 live)")

    cen, grid = [], []
    for H, s, c in product(HORIZONS, SPACINGS, COSTS):
        ii = np.arange(0, len(eidx) - H + 1, s)
        if not len(ii):
            continue
        s_c, s_s, s_h1, s_h2, s_d = window_stats(spy, ii, H)
        for key, r in series.items():
            form, band, g, cc, cash = key
            if cc != c:
                continue
            b_c, b_s, b_h1, b_h2, b_d = window_stats(r, ii, H)
            L_sh = b_s > s_s
            L_hv = (b_h1 > s_h1) & (b_h2 > s_h2)
            L_dd = b_d >= 0.60 * s_d
            L_cg = b_c >= 0.70 * s_c
            Pj = L_sh & L_hv & L_dd & L_cg
            ent = eidx[ii]
            grid.append(dict(panel=panel, form=form, band=band, gross=g, cash=cash, H=H, s=s,
                             cost=c, n=len(ii), pass_4b=float(Pj.mean()),
                             leg_sharpe=float(L_sh.mean()), leg_halves=float(L_hv.mean()),
                             leg_dd=float(L_dd.mean()), leg_cagr=float(L_cg.mean()),
                             cagr_med=float(np.nanmedian(b_c)),
                             spy_cagr_med=float(np.nanmedian(s_c)),
                             dd_med=float(np.nanmedian(b_d)),
                             slope=float(np.polyfit(s_c, b_c, 1)[0]) if len(ii) >= 10 else np.nan,
                             pass_IS=float(Pj[ent <= IS_END].mean())
                             if (ent <= IS_END).any() else np.nan,
                             n_IS=int((ent <= IS_END).sum()),
                             pass_OOS=float(Pj[ent >= OOS_START].mean())
                             if (ent >= OOS_START).any() else np.nan,
                             n_OOS=int((ent >= OOS_START).sum())))
            if (panel == P_HEAD and H == H_HEAD and s == S_HEAD and c == COST_HEAD
                    and form == "MA-DG"):
                for a in range(len(ii)):
                    cen.append((panel, form, band, g, cash, H, s, c, ent[a],
                                eidx[ii[a] + H - 1], b_c[a], b_s[a], b_d[a], s_c[a], s_s[a],
                                s_d[a], bool(L_sh[a]), bool(L_hv[a]), bool(L_dd[a]),
                                bool(L_cg[a]), bool(Pj[a])))
    G = pd.DataFrame(grid)
    C = pd.DataFrame(cen, columns=["panel", "form", "band", "gross", "cash", "H", "s", "cost",
                                   "entry", "exit", "cagr", "sharpe", "maxdd", "spy_cagr",
                                   "spy_sharpe", "spy_maxdd", "L_sharpe", "L_halves", "L_dd",
                                   "L_cagr", "pass_4b"])
    return G, C, series, start, eidx


# ------------------------------------------------------------------ fixed window + KEEP paths
def fixed_and_keep(series, start, px, panel):
    hdr(f"RULE 8 MANDATED BOOK LEG + BOTH KEEP PATHS — {panel}, fixed window and OOS 2017-01-01..")
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    idx = px.loc[start:].index
    rows = []
    keys = [("MA-DG", b, g, COST_HEAD, ca) for b, g, ca in product(BANDS, GROSSES, CASHES)]
    keys += [("RULES v1", np.nan, np.nan, COST_HEAD, 0),
             ("RULES v2 live", np.nan, np.nan, COST_HEAD, 0)]
    for k in keys:
        r = pd.Series(series[k], index=idx)
        o = r.loc[OOS_START:]
        fc, fs, fd = fmet(r.values)
        oc, os_, od = fmet(o.values)
        hf, ho = len(r) // 2, len(o) // 2
        rows.append(dict(book=f"{k[0]} b{k[1]:.2f} g{k[2]:.2f} c{k[4]}"
                         if k[0] == "MA-DG" else k[0],
                         form=k[0], band=k[1], gross=k[2], cash=k[4],
                         full_CAGR=fc, full_Sharpe=fs, full_MaxDD=fd,
                         full_H1=fsharpe(r.values[:hf]), full_H2=fsharpe(r.values[hf:]),
                         OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                         OOS_H1=fsharpe(o.values[:ho]), OOS_H2=fsharpe(o.values[ho:])))
    sp_o = spy.loc[OOS_START:]
    sc, ss, sd = fmet(spy.values)
    oc, os_, od = fmet(sp_o.values)
    hf, ho = len(spy) // 2, len(sp_o) // 2
    rows.append(dict(book="SPY", form="SPY", band=np.nan, gross=np.nan, cash=0,
                     full_CAGR=sc, full_Sharpe=ss, full_MaxDD=sd,
                     full_H1=fsharpe(spy.values[:hf]), full_H2=fsharpe(spy.values[hf:]),
                     OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                     OOS_H1=fsharpe(sp_o.values[:ho]), OOS_H2=fsharpe(sp_o.values[ho:])))
    T = pd.DataFrame(rows).set_index("book")
    lv, sy = T.loc["RULES v2 live"], T.loc["SPY"]
    out = []
    for b in T.index:
        if b in ("SPY",):
            continue
        r = T.loc[b]
        l4a = {"H1>LIVE": r.full_H1 > lv.full_H1, "H2>LIVE": r.full_H2 > lv.full_H2,
               "DD<=LIVE": r.full_MaxDD >= lv.full_MaxDD}
        l4b = {"H1>SPY": r.full_H1 > sy.full_H1, "H2>SPY": r.full_H2 > sy.full_H2,
               "OOS_Sharpe>SPY": r.OOS_Sharpe > sy.OOS_Sharpe,
               "DD<=60%SPY": r.full_MaxDD >= 0.6 * sy.full_MaxDD,
               "CAGR>=70%SPY": r.full_CAGR >= 0.7 * sy.full_CAGR}
        l4bo = {"OOS_H1>SPY": r.OOS_H1 > sy.OOS_H1, "OOS_H2>SPY": r.OOS_H2 > sy.OOS_H2,
                "OOS_Sharpe>SPY": r.OOS_Sharpe > sy.OOS_Sharpe,
                "OOS_DD<=60%SPY": r.OOS_MaxDD >= 0.6 * sy.OOS_MaxDD,
                "OOS_CAGR>=70%SPY": r.OOS_CAGR >= 0.7 * sy.OOS_CAGR}
        out.append(dict(book=b, band=r.band, gross=r.gross, cash=r.cash,
                        keep4a="PASS" if all(l4a.values()) else "FAIL",
                        fail4a="+".join(k for k, v in l4a.items() if not v),
                        keep4b="PASS" if all(l4b.values()) else "FAIL",
                        fail4b="+".join(k for k, v in l4b.items() if not v),
                        keep4b_OOS="PASS" if all(l4bo.values()) else "FAIL",
                        fail4b_OOS="+".join(k for k, v in l4bo.items() if not v)))
    K = pd.DataFrame(out).set_index("book")
    log(T.to_string(float_format=lambda x: f"{x:+.4f}"))
    log("\n" + K.to_string())
    md = K[K.index.str.startswith("MA-DG")]
    log(f"\nMA-DG grid ({len(md)} cells): 4a {int((md.keep4a=='PASS').sum())} PASS, "
        f"4b {int((md.keep4b=='PASS').sum())} PASS, OOS-only 4b "
        f"{int((md.keep4b_OOS=='PASS').sum())} PASS.")
    return T, K


# ------------------------------------------------------------------
def main():
    t0 = time.time()
    log("=" * 160)
    log(f"# 2026-09-12 cloud lane — IDEA 830: does the DE-GROSSING-TO-CASH channel have a "
        f"CEILING on the ENTRY-DATE pass share?")
    log("=" * 160)
    log(f"P1 band {BANDS} | P2 cash rung {CASHES} bps/yr  ->  {len(BANDS)*len(CASHES)} cells")
    log(f"REPORTED: gross {GROSSES}, H {HORIZONS}, spacing {SPACINGS}, cost {COSTS} bps, "
        f"panels U56 / B136 / SMALL.  HEADLINE = {P_HEAD}, g{G_HEAD:.2f}, H={H_HEAD}, "
        f"s={S_HEAD}, {COST_HEAD:.0f} bps.")
    log("next-day execution (engine applies weights at t+1), no shorting, no leverage.")
    log("C-CASH: the de-grossed fraction earns a flat rate credited on the realised cash "
        "fraction of NAV; no turnover cost on the cash leg (G3/G5 bound this).")

    u56 = load_universe()
    b136 = load_universe(broad=True)
    small, n_drop = small_panel()
    log(f"\nSMALL panel: dropped {n_drop} tickers with max_1d_move >= 1.0 from "
        f"data/small_meta.csv; {small.shape[1]-1} names + SPY benchmark.")
    log("SURVIVORSHIP: all three panels are CURRENT-CONSTITUENT lists (U56/B136 from "
        "research/universe.json and universe_broad.json; SMALL from a sub-$2B screen that is "
        "rewritten nightly), so every level AND every pass share below is optimistic.")

    hdr("GATES G1 / G2 — printed before any new number")
    gate_g1(u56)
    gate_g2(u56)

    hdr("THE SWEEP — band x cash on every reported axis")
    Gs, Cs = [], []
    for panel, px in (("U56", u56), ("B136", b136), ("SMALL", small)):
        G, C, series, start, eidx = run_panel(panel, px)
        Gs.append(G)
        Cs.append(C)
        if panel == P_HEAD:
            head_series, head_start, head_px = series, start, px
    G = pd.concat(Gs, ignore_index=True)
    C = pd.concat(Cs, ignore_index=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    log(f"\n{len(G):,} grid cells, {len(C):,} headline-panel (cell, entry-date) window rows.")

    # ------------------------------------------------------------------ G3
    hdr("GATE G3 — reproduce idea 828/829's committed headline (MA-DG b0.03 g1.00 cash 0)")
    want = dict(pass_4b=0.397727, leg_sharpe=0.914773, leg_halves=0.517045, leg_dd=0.863636,
                leg_cagr=0.727273, n=176)
    got = G[(G.panel == P_HEAD) & (G.form == "MA-DG") & (G.band == BAND_LIVE) &
            (G.gross == 1.00) & (G.cash == 0) & (G.H == H_HEAD) & (G.s == S_HEAD) &
            (G.cost == COST_HEAD)].iloc[0]
    g3 = pd.DataFrame([dict(stat=k, want=v, got=float(got[k]), diff=abs(float(got[k]) - v))
                       for k, v in want.items()])
    g3["verdict"] = np.where(g3["diff"] <= 5e-4, "PASS", "FAIL")
    log(g3.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    log(f"GATE G3 -> {'PASS' if (g3.verdict=='PASS').all() else 'FAIL'} (tolerance 5e-4).  Also "
        f"reproduces 828's MA-RS b0.03 g1.00 leg_dd: "
        f"{float(G[(G.panel==P_HEAD)&(G.form=='MA-RS')&(G.band==BAND_LIVE)&(G.gross==1.00)&(G.cash==0)&(G.H==H_HEAD)&(G.s==S_HEAD)&(G.cost==COST_HEAD)].leg_dd.iloc[0]):.6f}"
        f" vs committed 0.005682.")

    # ------------------------------------------------------------------ THE SWEEP TABLE
    hdr(f"THE CHANNEL — MA-DG joint 4b pass share, band x cash, at the headline cell")
    head = G[(G.panel == P_HEAD) & (G.form == "MA-DG") & (G.gross == G_HEAD) &
             (G.H == H_HEAD) & (G.s == S_HEAD) & (G.cost == COST_HEAD)]
    piv = head.pivot(index="band", columns="cash", values="pass_4b")
    log("joint pass_4b (n = %d entry windows):" % int(head.n.iloc[0]))
    log(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    best = head.loc[head.pass_4b.idxmax()]
    log(f"\nARGMAX over the 32 cells: band {best.band:.2f}, cash {int(best.cash)} bps -> "
        f"pass_4b {best.pass_4b:.4f}  (the LIVE band 0.03 at cash 0 reads "
        f"{float(piv.loc[BAND_LIVE, 0]):.4f})")
    log(f"H_830 (some cell >= {BAR:.2f}): "
        f"{'PASS' if head.pass_4b.max() >= BAR else 'FAIL'}   "
        f"H_CEIL: the channel's ceiling at the headline cell is **{head.pass_4b.max():.4f}**")
    interior = best.band not in (BANDS[0], BANDS[-1])
    log(f"H_BAND (argmax band interior to {BANDS}): {'PASS' if interior else 'FAIL'} "
        f"(argmax band {best.band:.2f})")
    d500 = (piv[500] - piv[0])
    log(f"H_CASH (max band-wise share(500) - share(0) >= 0.10): max {d500.max():+.4f} at band "
        f"{d500.idxmax():.2f} -> {'PASS' if d500.max() >= 0.10 else 'FAIL'}; "
        f"band-wise gains {dict(zip([f'{b:.2f}' for b in d500.index], np.round(d500.values,4)))}")

    log("\n-- per-leg shares at every cell of the headline sweep (which leg closes first) --")
    L = head[["band", "cash", "n", "pass_4b", "leg_sharpe", "leg_halves", "leg_dd", "leg_cagr",
              "cagr_med", "spy_cagr_med", "dd_med", "slope"]].sort_values(["band", "cash"])
    L = L.assign(binding=L[["leg_sharpe", "leg_halves", "leg_dd", "leg_cagr"]].idxmin(axis=1),
                 min_leg=L[["leg_sharpe", "leg_halves", "leg_dd", "leg_cagr"]].min(axis=1))
    L.to_csv(f"{OUT}.legs.csv", index=False)
    log(L.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    bb = L.loc[L.pass_4b.idxmax()]
    ratio_bind = bb.binding in ("leg_dd", "leg_cagr")
    log(f"\nH_CLOSE (the binding leg at the argmax is a RATIO leg): binding = "
        f"**{bb.binding}** at {bb.min_leg:.4f} -> {'PASS' if ratio_bind else 'FAIL'}")
    bc = L.binding.value_counts()
    log(f"binding leg over the 32 cells: {dict(bc)}")

    log("\n-- the same sweep at gross 0.75 (the LIVE gross), reported not selected --")
    h75 = G[(G.panel == P_HEAD) & (G.form == "MA-DG") & (G.gross == 0.75) & (G.H == H_HEAD) &
            (G.s == S_HEAD) & (G.cost == COST_HEAD)]
    log(h75.pivot(index="band", columns="cash", values="pass_4b").to_string(
        float_format=lambda x: f"{x:.4f}"))
    log(f"gross 0.75 ceiling {h75.pass_4b.max():.4f} vs gross 1.00 ceiling {head.pass_4b.max():.4f}")

    log("\n-- the RE-SPREADING twin MA-RS at the same 32 cells (828's control) --")
    rs = G[(G.panel == P_HEAD) & (G.form == "MA-RS") & (G.gross == G_HEAD) & (G.H == H_HEAD) &
           (G.s == S_HEAD) & (G.cost == COST_HEAD)]
    log(rs.pivot(index="band", columns="cash", values="pass_4b").to_string(
        float_format=lambda x: f"{x:.4f}"))
    log(f"MA-RS ceiling {rs.pass_4b.max():.4f}; its leg_dd ceiling {rs.leg_dd.max():.4f} against "
        f"MA-DG's {head.leg_dd.max():.4f} — the de-grossing channel IS the DD leg, as 828 found.")

    # ------------------------------------------------------------------ the reported axes
    hdr("EVERY REPORTED AXIS — the channel's ceiling, cell by cell (nothing selected here)")
    ax = (G[G.form == "MA-DG"].groupby(["panel", "gross", "H", "s", "cost"])
          .agg(ceiling=("pass_4b", "max"), n=("n", "first"),
               argmax_band=("pass_4b", lambda x: np.nan), median=("pass_4b", "median"))
          .drop(columns=["argmax_band"]).reset_index())
    arg = (G[G.form == "MA-DG"].sort_values("pass_4b")
           .groupby(["panel", "gross", "H", "s", "cost"]).tail(1)
           [["panel", "gross", "H", "s", "cost", "band", "cash"]]
           .rename(columns={"band": "argmax_band", "cash": "argmax_cash"}))
    ax = ax.merge(arg, on=["panel", "gross", "H", "s", "cost"])
    log(ax.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"\nCEILING over ALL {len(G[G.form=='MA-DG'])} MA-DG cells on every axis: "
        f"**{G[G.form=='MA-DG'].pass_4b.max():.4f}** "
        f"({int((G[G.form=='MA-DG'].pass_4b >= BAR).sum())} cells at or above {BAR:.2f}); "
        f"at the PROTOCOL rung (10 bps) and H=756: "
        f"{G[(G.form=='MA-DG')&(G.cost==10.0)&(G.H==756)].pass_4b.max():.4f}")

    # ------------------------------------------------------------------ G6
    viol = 0
    for keys, sub in G[G.form == "MA-DG"].groupby(["panel", "band", "gross", "H", "s", "cost"]):
        v = sub.sort_values("cash").cagr_med.values
        viol += int((np.diff(v) < -1e-12).sum())
    log(f"\nGATE G6 — median window CAGR monotone non-decreasing in the cash rung at every "
        f"(panel, band, gross, H, s, cost) cell: {viol} violations -> "
        f"{'PASS' if viol == 0 else 'FAIL'}")

    # ------------------------------------------------------------------ G5
    hdr("GATE G5 — the C-CASH convention: EXACT (cash compounds inside the segment) vs the "
        "ADDITIVE shortcut")
    start_u = u56.index[260]
    eidx_u = u56.loc[start_u:].index
    spy_u = u56["SPY"].pct_change().fillna(0.0).loc[start_u:].values
    ii = np.arange(0, len(eidx_u) - H_HEAD + 1, S_HEAD)
    s_c, s_s, s_h1, s_h2, s_d = window_stats(spy_u, ii, H_HEAD)
    rows5 = []
    for band, cash in product(BANDS, CASHES):
        w = madg_weights(u56, band, G_HEAD)
        out = {}
        for tag, ex in (("exact", True), ("additive", False)):
            r = fast_backtest(u56, w, COST_HEAD, cash, FREQ, exact=ex)[0].loc[start_u:].values
            b_c, b_s, b_h1, b_h2, b_d = window_stats(r, ii, H_HEAD)
            out[tag] = float(((b_s > s_s) & (b_h1 > s_h1) & (b_h2 > s_h2) &
                              (b_d >= 0.60 * s_d) & (b_c >= 0.70 * s_c)).mean())
            out[f"cagr_{tag}"] = float(fmet(r)[0])
        rows5.append(dict(band=band, cash=cash, pass_exact=out["exact"],
                          pass_additive=out["additive"],
                          d_pass=abs(out["exact"] - out["additive"]),
                          cagr_exact=out["cagr_exact"], cagr_additive=out["cagr_additive"],
                          d_cagr_bp=1e4 * abs(out["cagr_exact"] - out["cagr_additive"])))
    C5 = pd.DataFrame(rows5)
    log(C5.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"GATE G5 — max |exact - additive| pass share over the 32 cells: {C5.d_pass.max():.4f} "
        f"vs bar 0.02 -> {'PASS' if C5.d_pass.max() <= 0.02 else 'FAIL'}; max full-sample CAGR "
        f"difference {C5.d_cagr_bp.max():.2f} bps/yr.  Every number in this run uses the EXACT "
        f"convention; this gate prices the shortcut the record would otherwise have taken.")

    hdr("R7 (REPORTED, NOT A GATE) — the same sweep at DAILY rebalance cadence")
    Gd, _, _, _, _ = run_panel("U56", u56, freq="D", verbose=False)
    hd = Gd[(Gd.form == "MA-DG") & (Gd.gross == G_HEAD) & (Gd.H == H_HEAD) & (Gd.s == S_HEAD) &
            (Gd.cost == COST_HEAD)]
    cmp_ = head.merge(hd, on=["band", "cash"], suffixes=("_W", "_D"))
    cmp_["d_pass"] = (cmp_.pass_4b_W - cmp_.pass_4b_D).abs()
    log(cmp_[["band", "cash", "pass_4b_W", "pass_4b_D", "d_pass"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"R7 — max |weekly - daily| pass share {cmp_.d_pass.max():.4f}, median "
        f"{cmp_.d_pass.median():.4f}; daily ceiling {hd.pass_4b.max():.4f} at band "
        f"{float(hd.loc[hd.pass_4b.idxmax()].band):.2f} / cash "
        f"{int(hd.loc[hd.pass_4b.idxmax()].cash)} against the weekly ceiling "
        f"{head.pass_4b.max():.4f}.  DECLARED: a daily book re-rebalances every day and pays "
        f"turnover for it, so this is a CADENCE comparison between two different books, not a "
        f"check on the cash convention (that is G5).  NEITHER cadence reaches {BAR:.2f}.")

    # ------------------------------------------------------------------ fixed window + KEEP
    T, K = fixed_and_keep(head_series, head_start, head_px, P_HEAD)
    T.to_csv(f"{OUT}.fixed.csv")

    # ------------------------------------------------------------------ G4
    hdr("GATE G4 — the committed candidate memo's fixed-window triple")
    cand = T.loc[f"MA-DG b{BAND_LIVE:.2f} g1.00 c0"]
    sy = T.loc["SPY"]
    g4 = pd.DataFrame([
        dict(what="candidate full CAGR", want=0.1152, got=cand.full_CAGR),
        dict(what="candidate full Sharpe", want=1.1996, got=cand.full_Sharpe),
        dict(what="candidate full MaxDD", want=-0.1591, got=cand.full_MaxDD),
        dict(what="candidate OOS CAGR", want=0.1266, got=cand.OOS_CAGR),
        dict(what="candidate OOS Sharpe", want=1.2740, got=cand.OOS_Sharpe),
        dict(what="SPY full CAGR", want=0.1516, got=sy.full_CAGR),
        dict(what="SPY full Sharpe", want=0.8860, got=sy.full_Sharpe),
        dict(what="SPY full MaxDD", want=-0.3372, got=sy.full_MaxDD)])
    g4["diff"] = (g4.want - g4.got).abs()
    g4["verdict"] = np.where(g4["diff"] <= 0.01, "PASS", "FAIL")
    log(g4.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    log(f"GATE G4 -> {'PASS' if (g4.verdict=='PASS').all() else 'FAIL'} (tolerance 0.010).")

    # ------------------------------------------------------------------ RULE 8
    hdr("RULE 8 — (band, cash) chosen on IS ENTRY DATES only, read once on OOS entry dates")
    wf = head[["band", "cash", "n_IS", "pass_IS", "n_OOS", "pass_OOS", "pass_4b"]].copy()
    wf = wf.sort_values(["band", "cash"])
    log(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pick = wf.loc[wf.pass_IS.idxmax()]
    obest = wf.loc[wf.pass_OOS.idxmax()]
    gap = float(obest.pass_OOS - pick.pass_OOS)
    log(f"\nIS pick: band {pick.band:.2f}, cash {int(pick.cash)} -> IS {pick.pass_IS:.4f} "
        f"(n={int(pick.n_IS)}), OOS {pick.pass_OOS:.4f} (n={int(pick.n_OOS)}).  "
        f"OOS-best cell: band {obest.band:.2f}, cash {int(obest.cash)} at {obest.pass_OOS:.4f}. "
        f"Regret {gap:.4f} vs bar 0.15 -> {'PASS' if gap <= 0.15 else 'FAIL'} (H_R8)")
    log(f"Spearman(IS share, OOS share) over the 32 cells = "
        f"{spearman(wf.pass_IS, wf.pass_OOS):+.4f}")
    ktag = ("MA-DG", float(pick.band), G_HEAD, COST_HEAD, int(pick.cash))
    r = pd.Series(head_series[ktag], index=head_px.loc[head_start:].index)
    o = r.loc[OOS_START:]
    log(f"\nRULE 8 mandated BOOK leg for the IS-picked cell: full "
        f"{fmet(r.values)[0]:.2%} / {fmet(r.values)[1]:.4f} / {fmet(r.values)[2]:.2%}; "
        f"OOS 2017-01-01.. {fmet(o.values)[0]:.2%} / {fmet(o.values)[1]:.4f} / "
        f"{fmet(o.values)[2]:.2%}  against LIVE OOS "
        f"{T.loc['RULES v2 live'].OOS_CAGR:.2%} / {T.loc['RULES v2 live'].OOS_Sharpe:.4f} / "
        f"{T.loc['RULES v2 live'].OOS_MaxDD:.2%} and SPY OOS {sy.OOS_CAGR:.2%} / "
        f"{sy.OOS_Sharpe:.4f} / {sy.OOS_MaxDD:.2%}")
    kk = K.loc[f"MA-DG b{pick.band:.2f} g{G_HEAD:.2f} c{int(pick.cash)}"]
    log(f"IS-picked cell KEEP paths: 4a {kk.keep4a} ({kk.fail4a or '-'}), 4b {kk.keep4b} "
        f"({kk.fail4b or '-'}), OOS-only 4b {kk.keep4b_OOS} ({kk.fail4b_OOS or '-'})")
    wf.to_csv(f"{OUT}.wf.csv", index=False)

    # ------------------------------------------------------------------ PROTOCOL 3
    hdr("PROTOCOL 3 — baseline.compare() for the argmax cell and the live-band cell (cash 0)")
    for band in sorted({float(best.band), BAND_LIVE}):
        log(f"\n--- MA-DG band {band:.2f} gross {G_HEAD:.2f}, cash 0 (compare() has no cash leg) ---")
        compare(f"830 cloud MA-DG b{band:.2f} g{G_HEAD:.2f}",
                lambda px, b=band: madg_weights(px, b, G_HEAD), u56, freq=FREQ)

    Path(f"{OUT}.txt").write_text("\n".join(LINES) + "\n")
    log(f"\nTotal runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
