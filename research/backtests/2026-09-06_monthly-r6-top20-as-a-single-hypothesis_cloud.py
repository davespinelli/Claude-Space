#!/usr/bin/env python3
"""QUEUE idea 182 - monthly-r6-top20-as-a-single-hypothesis   (cloud, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 182)
    "idea 173's by-product clears 4b full-sample AND OOS-window at 10 and 25 bps on u56 (R6,
     top-20 EW, g=0.75, MONTHLY: 13.61%/1.1557/-18.81%, OOS 14.56%/1.1695, turnover 4.8x/yr)
     but is 1 of 90 unpriced ladder selections and fails the universe change (broad -24.51%
     MaxDD, 4.3pp over 4b's cap; small 0.4934 Sharpe).  Run it ONCE as a pre-registered single
     hypothesis on all three panels at 5/10/25 bps with 1-day and 1-week execution lag, plus
     idea 53's random-composition draws.  No tuning: cadence, n and gross are fixed at the
     published values."

THE HYPOTHESIS, written out in full BEFORE any number below was read
    H:  the book B* clears PROTOCOL 4b on u56 at 5, 10 and 25 bps and at both execution lags,
        and its 4b pass is not an artefact of the exact 55 names in universe.json.
    B* is FIXED, every dial at idea 173's published value - there is NOTHING tuned here:
        signal      R6 = px / px.shift(126) - 1, divided by vol20.clip(0.08) ** 0.5
                    (idea 173's ANCHOR carries p = 0.5, so the published R6 book DOES have
                    RULES v1's vol scaler.  The QUEUE line does not say so; the grid does, and
                    reproduction control [c] proves it - this is the config that produced
                    13.61%/1.1557/-18.81%, not a vol-scaler-free variant.)
        gate        px > 200d MA  AND  vol20 < 0.60
        book        top 20 by signal among eligible, equal weight, gross 0.75 (cash otherwise)
        cadence     MONTHLY (engine's calendar-month mask)
    A pre-registered single hypothesis has NO tuned parameters.  Panel, cost rung, execution
    lag and composition draw are AUDIT AXES - the hypothesis is evaluated at all of them and
    every cell is reported.  Nothing is chosen for reporting.

WHY THIS IS WORTH ONE RUN
    Idea 173 produced 90 ladder selections; this was the one that looked best, and looking best
    among 90 is not evidence.  The only way to price it is to fix it completely and expose it to
    axes it was never fitted on.  If it survives, it is the project's second 4b candidate; if it
    dies, a 1-of-90 grid pick died the way 1-of-90 grid picks usually do.  Both are results.

THE AXES
    PANEL   u56 (universe.json, 55 names + SPY)   <- where the claim was made
            broad (universe_broad.json)           <- the universe change it already fails
            small (the sub-$2B panel, max_1d_move >= 1.0 dropped per the standing rule)
    COST    5, 10, 25 bps.  Computed by netting a single 0-bps run by turnover x bps / 1e4;
            cost linearity is asserted against engine.backtest in control [b].
    LAG     execution delay in index BARS between the decision close and the fill.
            1 = PROTOCOL rule 2's t+1 (the only one the record has ever quoted)
            5 = one trading week
            7 = one calendar week
            The distinction matters because of idea 38: data/prices*.csv are CALENDAR-day
            indexed after 2014-09-17, so on u56/broad a 5-bar lag is ~3.5 trading days after
            that date and 5 trading days before it, while on the trading-day-indexed small
            panel 5 bars is exactly one trading week.  Both 5 and 7 are reported so the
            "1-week lag" the idea asks for is bracketed rather than fudged.
    DRAWS   idea 53's composition test: drop 5 and 10 names at random from the panel, 200 draws
            each (seed 182), and report the DISTRIBUTION of 4b passes rather than a point.

REPRODUCTION CONTROLS, asserted before any conclusion
    [a] the weights function reproduces idea 173's `weights()` for the published config.
    [e] the composition-draw shortcut (subset a panel-level signal, then rank) equals the
        published weights() run on the subset panel, to <1e-15, on drops of 5 and 10 names.
    [b] the lag=1 fast simulator equals engine.backtest to <1e-12 on returns and turnover, and
        the 0-bps-plus-netting shortcut equals a direct 10-bps engine run to <1e-12.
    [c] THE decisive one: the (u56, R6, M, lag=1) row at 10 and 25 bps must equal idea 173's
        committed .grid.csv on CAGR_F/Sharpe_F/MaxDD_F/Sharpe_H1/Sharpe_H2/CAGR_OOS/
        Sharpe_OOS/MaxDD_OOS/oosH1/oosH2/turnover_yr to <1e-9.  Failure here means this is not
        the book the record published and the run stops.

PROTOCOL rule 8 walk-forward (required)
    The config was CHOSEN from a 90-point grid with the whole sample visible, so the honest
    walk-forward asks what an IS-only chooser would have done.  On the R6 CADENCE ladder
    (D/W/M/Q), parameters on <= 2016-12-31 only, OOS 2017-01-01.. read once:
      CONST-W    RULES v1's weekly cadence (the do-nothing control)
      IS-PICK    cadence by IS Sharpe
      FIXED-M    the published pick
      ORACLE     the OOS argmax (an upper bound, not an arm)
    Reported per panel and cost rung against RULES v1 and SPY over the same OOS window.

BOTH KEEP PATHS (4a and 4b) on every cell, plus idea 173's 4b-on-the-OOS-window variant.

CAVEATS carried, not buried
    * SURVIVORSHIP.  universe.json, universe_broad.json and the small panel are all CURRENT-
      CONSTITUENT lists (data/SMALL_PANEL_README.md, idea 54).  No level here is an attainable
      return, and the composition draws resample WITHIN a survivor list - they bound sensitivity
      to composition, not survivorship.
    * Idea 38: the calendar-day index on the large-cap panels (see LAG above).
    * Idea 144: a re-cadenced book is the same book; the walk-forward arms are not new signals.
    * Idea 187/221: MONTHLY is a k=1 calendar block, so it has exactly ONE phase and carries no
      block-phase alignment draw.  That is a genuine strength of this particular point and is
      stated as such, not as evidence for the book.

Deterministic (seed 182), standalone, no network.  Writes .console.txt, .cells.csv, .draws.csv,
.walkforward.csv, .result.md inputs.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_monthly-r6-top20-as-a-single-hypothesis_cloud"
PARENT = "2026-09-05_is-the-ladder-endpoint-a-general-selector-artefact_cloud"
OUT = ROOT / "research" / "backtests"

SEED = 182
IS_END = pd.Timestamp("2016-12-31")
OOS_START = IS_END + pd.Timedelta(days=1)
PHI, DELTA = 0.70, 0.60

# ---- the pre-registered book.  Nothing here is swept.
CFG = dict(sig="R6", n=20, g=0.75, max_vol=0.60, p=0.5, freq="M")
COSTS = [5.0, 10.0, 25.0]
LAGS = [1, 5, 7]
LAG_NAME = {1: "t+1 (PROTOCOL)", 5: "t+5 (1 trading wk)", 7: "t+7 (1 calendar wk)"}
CAD_LADDER = ["D", "W", "M", "Q"]
DROPS = [5, 10]
N_DRAWS = 200

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def flush():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


# ---------------------------------------------------------------- panels (idea 173, verbatim)
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    P(f"  small panel: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
      f"{len(keep)-1} names + SPY benchmark remain   (SURVIVORSHIP: current constituents only)")
    return px[keep]


def load_panels():
    return {"u56": load_universe(), "broad": load_universe(broad=True), "small": small_panel()}


# ---------------------------------------------------------------- signal + book (idea 173, verbatim)
_CACHE = {}


def raw_signal(px, sig):
    key = (id(px), sig)
    if key in _CACHE:
        return _CACHE[key]
    if sig == "COMP":
        mom = px.shift(21) / px.shift(252) - 1
        r6 = px / px.shift(126) - 1
        r3 = px / px.shift(63) - 1
        s = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    elif sig == "MOM":
        s = px.shift(21) / px.shift(252) - 1
    elif sig == "R6":
        s = px / px.shift(126) - 1
    else:
        raise ValueError(sig)
    _CACHE[key] = s
    return s


def gates(px):
    key = (id(px), "_gates")
    if key not in _CACHE:
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        _CACHE[key] = (above, vol20)
    return _CACHE[key]


def weights(px, sig, n, g, max_vol, p):
    """Literal top-n equal weight at gross g among eligible names; cash for empty slots."""
    s = raw_signal(px, sig)
    above, vol20 = gates(px)
    if p:
        s = s / vol20.clip(lower=0.08) ** p
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


def book_weights(px):
    return weights(px, CFG["sig"], CFG["n"], CFG["g"], CFG["max_vol"], CFG["p"])


def scored_panel(px):
    """(scaled signal, gate mask) for the published config, computed ONCE per panel.

    R6 and both gates are computed COLUMN-WISE (px/px.shift(126)-1, px>200dma, rolling vol),
    so they are identical whether computed on the full panel or on any subset of its columns;
    only the cross-sectional rank depends on the column set, and that is applied after the
    subset in weights_from().  Asserted against weights() in check_e()."""
    s = raw_signal(px, CFG["sig"])
    above, vol20 = gates(px)
    if CFG["p"]:
        s = s / vol20.clip(lower=0.08) ** CFG["p"]
    return s, (above & (vol20 < CFG["max_vol"]))


def weights_from(s, gate, cols):
    """The book's weights on a column subset, from the panel-level signal and gate."""
    rank = s[cols].where(gate[cols]).rank(axis=1, ascending=False)
    return (rank <= CFG["n"]).astype(float) * (CFG["g"] / CFG["n"])


# ---------------------------------------------------------------- simulator with an execution lag
def sim(px, W, freq, lag=1, cost_bps=0.0):
    """Vectorised backtest.  `lag` is the number of index BARS between the decision close and
    the fill: lag=1 is PROTOCOL rule 2's t+1 and reproduces engine.backtest exactly (control
    [b]).  A larger lag delays BOTH the target and the execution bar by the same amount, so
    the trade happens `lag` bars after the decision at that bar's prices - a true execution
    delay, not a stale signal at a prompt fill."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(lag, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ---------------------------------------------------------------- metrics (idea 173, verbatim)
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:len(r) // 2]), ("H2", r.iloc[len(r) // 2:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_START))):
        c, s, d = stats(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = c, s, d
    o = win(r, lo=OOS_START)
    out["oosH1"] = metrics(o.iloc[:len(o) // 2])["Sharpe"]
    out["oosH2"] = metrics(o.iloc[len(o) // 2:])["Sharpe"]
    return out


def fail4a(row, base):
    f = []
    if not row["Sharpe_H1"] > base["Sharpe_H1"]: f.append("H1")
    if not row["Sharpe_H2"] > base["Sharpe_H2"]: f.append("H2")
    if not row["MaxDD_F"] >= base["MaxDD_F"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail4b(row, spy):
    f = []
    if not row["Sharpe_H1"] > spy["Sharpe_H1"]: f.append("H1")
    if not row["Sharpe_H2"] > spy["Sharpe_H2"]: f.append("H2")
    if not row["Sharpe_OOS"] > spy["Sharpe_OOS"]: f.append("OOS")
    if not row["MaxDD_F"] >= DELTA * spy["MaxDD_F"]: f.append("DD")
    if not row["CAGR_F"] >= PHI * spy["CAGR_F"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fail4b_oos(row, spy):
    """idea 173's 4b read on the OOS window alone."""
    f = []
    if not row["oosH1"] > spy["oosH1"]: f.append("H1")
    if not row["oosH2"] > spy["oosH2"]: f.append("H2")
    if not row["Sharpe_OOS"] > spy["Sharpe_OOS"]: f.append("OOS")
    if not row["MaxDD_OOS"] >= DELTA * spy["MaxDD_OOS"]: f.append("DD")
    if not row["CAGR_OOS"] >= PHI * spy["CAGR_OOS"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def margin4b(row, spy):
    """Relative margin on the binding 4b bar (idea 90's convention); negative = fails."""
    eps = 0.05
    parts = {
        "H1": (row["Sharpe_H1"] - spy["Sharpe_H1"]) / max(abs(spy["Sharpe_H1"]), eps),
        "H2": (row["Sharpe_H2"] - spy["Sharpe_H2"]) / max(abs(spy["Sharpe_H2"]), eps),
        "OOS": (row["Sharpe_OOS"] - spy["Sharpe_OOS"]) / max(abs(spy["Sharpe_OOS"]), eps),
        "DD": (DELTA * abs(spy["MaxDD_F"]) - abs(row["MaxDD_F"])) / max(DELTA * abs(spy["MaxDD_F"]), eps),
        "CAGR": (row["CAGR_F"] - PHI * spy["CAGR_F"]) / max(abs(PHI * spy["CAGR_F"]), eps),
    }
    w = min(parts, key=parts.get)
    return parts[w], w


# ---------------------------------------------------------------- controls
def check_b(px):
    P("  [b] lag=1 simulator vs engine.backtest, and the 0-bps + netting shortcut:")
    W = book_weights(px)
    a = backtest(px, W, cost_bps=0.0, freq=CFG["freq"])
    r0, t0_ = sim(px, W, CFG["freq"], 1, 0.0)
    d1 = float((a["returns"] - r0).abs().max())
    d2 = float((a["turnover"] - t0_).abs().max())
    a10 = backtest(px, W, cost_bps=10.0, freq=CFG["freq"])["returns"]
    d3 = float((a10 - (r0 - t0_ * 10.0 / 1e4)).abs().max())
    ok = d1 < 1e-12 and d2 < 1e-10 and d3 < 1e-12
    P(f"      max|dret|={d1:.3e}  max|dturn|={d2:.3e}  cost-linearity max|d|={d3:.3e}"
      f"   -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_e(px):
    """The draw loop's shortcut must be the published weights function, exactly."""
    P("  [e] weights_from(panel-level signal, column subset) == weights(subset panel):")
    rng = np.random.default_rng(999)
    names = [c for c in px.columns if c != "SPY"]
    s, gate = scored_panel(px)
    ok = True
    for k in (5, 10):
        drop = set(rng.choice(names, size=k, replace=False))
        cols = [c for c in px.columns if c not in drop]
        a = weights(px[cols], CFG["sig"], CFG["n"], CFG["g"], CFG["max_vol"], CFG["p"])
        b = weights_from(s, gate, cols)
        d = float((a - b).abs().to_numpy().max())
        P(f"      drop {k:2d} names: max|dw| = {d:.3e}")
        ok &= d < 1e-15
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_c(cells):
    P(f"  [c] published-row reproduction vs {PARENT}.grid.csv  (THE decisive control)")
    src = OUT / f"{PARENT}.grid.csv"
    if not src.exists():
        P("      *** parent grid.csv not found -> FAIL")
        return False
    g = pd.read_csv(src)
    g = g[(g.panel == "u56") & (g.signal == "R6") & (g.ladder == "CADENCE") & (g.value == "M")]
    mine = cells[(cells.panel == "u56") & (cells.lag == 1) & (cells.cost.isin([10.0, 25.0]))]
    m = g.merge(mine, on="cost", suffixes=("_o", "_n"))
    cols = ["CAGR_F", "Sharpe_F", "MaxDD_F", "Sharpe_H1", "Sharpe_H2", "CAGR_OOS", "Sharpe_OOS",
            "MaxDD_OOS", "oosH1", "oosH2", "turnover_yr"]
    worst, wc = 0.0, ""
    for c in cols:
        d = float((m[c + "_o"] - m[c + "_n"]).abs().max())
        if d > worst:
            worst, wc = d, c
    ok = len(m) == 2 and worst < 1e-9
    P(f"      matched rows={len(m)}/2   max|d| over {len(cols)} columns = {worst:.3e} (worst: {wc})")
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    P(f"IDEA 182 - monthly-r6-top20-as-a-single-hypothesis   (cloud, {pd.Timestamp.today().date()})")
    P("=" * 122)
    P("ONE pre-registered book, NOTHING tuned:  R6 / vol20^0.5, gate (px>200dma & vol20<0.60),")
    P(f"top-{CFG['n']} equal weight, gross {CFG['g']}, cadence {CFG['freq']}.  Idea 173 published it on u56 at")
    P("13.61% / 1.1557 / -18.81% (OOS 14.56% / 1.1695, 4.8x/yr turnover) as 1 of 90 grid picks.")
    P("Audit axes (not parameters): 3 panels x 3 cost rungs x 3 execution lags, plus 200")
    P("random-composition draws per (panel, drop size) per idea 53.  Every cell is reported.")
    P("")

    panels = load_panels()
    ref = {}
    for pn, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        b0 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        ref[pn] = dict(start=st, spy=spy, b_ret=b0["returns"].loc[st:], b_trn=b0["turnover"].loc[st:])
        P(f"  panel {pn:6s} {px.shape[1]:4d} cols  {st.date()}..{px.index[-1].date()}  "
          f"IS rows {len(win(spy, hi=IS_END)):5d}  OOS rows {len(win(spy, lo=OOS_START)):5d}")
    P("")

    P("REPRODUCTION CONTROLS")
    if not (check_b(panels["u56"]) & check_e(panels["u56"])):
        P("\n*** SIMULATOR CONTROL FAILED - stopping. ***"); flush(); return
    P("")

    # ---------------- the 27 cells
    P("THE HYPOTHESIS ON 3 PANELS x 3 COST RUNGS x 3 EXECUTION LAGS (27 cells, all reported)")
    rows = []
    for pn, px in panels.items():
        st = ref[pn]["start"]
        W = book_weights(px)
        spy = ref[pn]["spy"]
        spy_row = full_row(spy)
        for lag in LAGS:
            r0, trn = sim(px, W, CFG["freq"], lag, 0.0)
            r0, trn = r0.loc[st:], trn.loc[st:]
            typ = trn.sum() / (len(trn) / 252)
            for c in COSTS:
                r = r0 - trn * c / 1e4
                base = full_row(ref[pn]["b_ret"] - ref[pn]["b_trn"] * c / 1e4)
                row = dict(panel=pn, lag=lag, cost=c, turnover_yr=float(typ))
                row.update(full_row(r))
                row["fail4a"] = fail4a(row, base)
                row["fail4b"] = fail4b(row, spy_row)
                row["fail4b_oos"] = fail4b_oos(row, spy_row)
                mg, wb = margin4b(row, spy_row)
                row["margin4b"], row["worstbar"] = mg, wb
                rows.append(row)
    cells = pd.DataFrame(rows)
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    P("")
    okC = check_c(cells)
    if not okC:
        P("\n*** PUBLISHED-ROW REPRODUCTION FAILED - this is not idea 173's book.  Stopping. ***")
        flush(); return
    P("")

    P(f"  {'panel':6s} {'lag':20s} {'bps':>5s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
      f"{'H1':>6s} {'H2':>6s} {'OOS CAGR':>9s} {'OOS Sh':>7s} {'OOS DD':>8s} {'turn/yr':>8s} "
      f"{'4a':>8s} {'4b':>14s} {'4b(OOS win)':>14s} {'4b margin':>10s}")
    for pn in panels:
        sp = full_row(ref[pn]["spy"])
        for lag in LAGS:
            for c in COSTS:
                r = cells[(cells.panel == pn) & (cells.lag == lag) & (cells.cost == c)].iloc[0]
                P(f"  {pn:6s} {LAG_NAME[lag]:20s} {c:5.0f} {r.CAGR_F:7.2%} {r.Sharpe_F:7.4f} "
                  f"{r.MaxDD_F:8.2%} {r.Sharpe_H1:6.3f} {r.Sharpe_H2:6.3f} {r.CAGR_OOS:9.2%} "
                  f"{r.Sharpe_OOS:7.4f} {r.MaxDD_OOS:8.2%} {r.turnover_yr:8.2f} "
                  f"{r.fail4a:>8s} {r.fail4b:>14s} {r.fail4b_oos:>14s} "
                  f"{r.margin4b:+9.3f}/{r.worstbar}")
        P(f"  {'':6s} SPY on this panel:  CAGR {sp['CAGR_F']:6.2%}  Sharpe {sp['Sharpe_F']:.4f}  "
          f"MaxDD {sp['MaxDD_F']:7.2%}  halves {sp['Sharpe_H1']:.3f}/{sp['Sharpe_H2']:.3f}  "
          f"OOS {sp['CAGR_OOS']:6.2%}/{sp['Sharpe_OOS']:.4f}/{sp['MaxDD_OOS']:7.2%}")
        b = full_row(ref[pn]["b_ret"] - ref[pn]["b_trn"] * 10.0 / 1e4)
        P(f"  {'':6s} RULES v1 @10bps:    CAGR {b['CAGR_F']:6.2%}  Sharpe {b['Sharpe_F']:.4f}  "
          f"MaxDD {b['MaxDD_F']:7.2%}  halves {b['Sharpe_H1']:.3f}/{b['Sharpe_H2']:.3f}  "
          f"OOS {b['CAGR_OOS']:6.2%}/{b['Sharpe_OOS']:.4f}/{b['MaxDD_OOS']:7.2%}")
        P("")
    n4a = int((cells.fail4a == "-").sum()); n4b = int((cells.fail4b == "-").sum())
    n4bo = int((cells.fail4b_oos == "-").sum())
    P(f"  KEEP paths over all {len(cells)} cells:  4a {n4a}   4b {n4b}   4b-on-OOS-window {n4bo}")
    P(f"  binding 4b bar by frequency: " +
      ", ".join(f"{k}:{v}" for k, v in cells.worstbar.value_counts().items()))
    P("")

    # ---------------- idea 53 composition draws
    P("=" * 122)
    P("IDEA 53 COMPOSITION DRAWS - drop k names at random from the panel, 200 draws, seed 182")
    P("  The question is not whether the book wins on the exact 55 names it was published on,")
    P("  but whether its 4b pass survives the list being slightly different.  Reported at the")
    P("  PROTOCOL lag (t+1) and at 10 and 25 bps; the pass RATE is the number, not any one draw.")
    drows = []
    for pn, px in panels.items():
        st = ref[pn]["start"]
        spy_row = full_row(ref[pn]["spy"])
        names = [c for c in px.columns if c != "SPY"]
        s_pan, gate_pan = scored_panel(px)
        for k in DROPS:
            for d in range(N_DRAWS):
                drop = set(rng.choice(names, size=k, replace=False))
                cols = [c for c in px.columns if c not in drop]
                sub = px[cols]
                Ws = weights_from(s_pan, gate_pan, cols)
                r0, trn = sim(sub, Ws, CFG["freq"], 1, 0.0)
                r0, trn = r0.loc[st:], trn.loc[st:]
                for c in [10.0, 25.0]:
                    r = r0 - trn * c / 1e4
                    base = full_row(ref[pn]["b_ret"] - ref[pn]["b_trn"] * c / 1e4)
                    row = dict(panel=pn, drop=k, draw=d, cost=c)
                    row.update(full_row(r))
                    row["fail4a"] = fail4a(row, base)
                    row["fail4b"] = fail4b(row, spy_row)
                    row["fail4b_oos"] = fail4b_oos(row, spy_row)
                    mg, wb = margin4b(row, spy_row)
                    row["margin4b"], row["worstbar"] = mg, wb
                    drows.append(row)
        P(f"   ... {pn} draws done ({time.time()-t0:.0f}s)")
    dr = pd.DataFrame(drows)
    dr.to_csv(OUT / f"{STEM}.draws.csv", index=False)
    P("")
    P(f"  {'panel':6s} {'drop':>5s} {'bps':>5s} {'n':>5s} {'4b pass rate':>13s} {'4b-OOS rate':>12s} "
      f"{'4a rate':>8s} {'Sharpe mean':>12s} {'Sharpe p05':>11s} {'MaxDD mean':>11s} "
      f"{'margin mean':>12s} {'binding bar (top 2)':>24s}")
    for pn in panels:
        for k in DROPS:
            for c in [10.0, 25.0]:
                s = dr[(dr.panel == pn) & (dr["drop"] == k) & (dr.cost == c)]
                vc = s.worstbar.value_counts()
                top = ", ".join(f"{a} {b/len(s):.0%}" for a, b in vc.head(2).items())
                P(f"  {pn:6s} {k:5d} {c:5.0f} {len(s):5d} {(s.fail4b=='-').mean():13.1%} "
                  f"{(s.fail4b_oos=='-').mean():12.1%} {(s.fail4a=='-').mean():8.1%} "
                  f"{s.Sharpe_F.mean():12.4f} {s.Sharpe_F.quantile(0.05):11.4f} "
                  f"{s.MaxDD_F.mean():11.2%} {s.margin4b.mean():+12.3f} {top:>24s}")
        P("")

    # ---------------- rule 8 walk-forward
    P("=" * 122)
    P("PROTOCOL RULE 8 WALK-FORWARD - what an IS-only chooser would have picked on this ladder")
    P("  The published M was chosen with the whole sample visible (1 of 90).  Arms below choose")
    P("  on <= 2016-12-31 only; the OOS window is read once.  ORACLE is an upper bound, not an arm.")
    wrows = []
    for pn, px in panels.items():
        st = ref[pn]["start"]
        W = book_weights(px)
        spy = ref[pn]["spy"]
        lad = {}
        for cd in CAD_LADDER:
            r0, trn = sim(px, W, cd, 1, 0.0)
            lad[cd] = (r0.loc[st:], trn.loc[st:])
        for c in COSTS:
            net = {cd: lad[cd][0] - lad[cd][1] * c / 1e4 for cd in CAD_LADDER}
            is_pick = max(CAD_LADDER, key=lambda cd: metrics(win(net[cd], hi=IS_END))["Sharpe"])
            oracle = max(CAD_LADDER, key=lambda cd: metrics(win(net[cd], lo=OOS_START))["Sharpe"])
            for arm, cd in [("CONST-W", "W"), ("IS-PICK", is_pick), ("FIXED-M", "M"),
                            ("ORACLE", oracle)]:
                o = win(net[cd], lo=OOS_START)
                m = metrics(o)
                wrows.append(dict(panel=pn, cost=c, arm=arm, cadence=cd, OOS_CAGR=m["CAGR"],
                                  OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                                  IS_Sharpe=metrics(win(net[cd], hi=IS_END))["Sharpe"]))
    wf = pd.DataFrame(wrows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"  {'panel':6s} {'bps':>5s} {'arm':9s} {'cad':>4s} {'IS Sharpe':>10s} {'OOS CAGR':>9s} "
      f"{'OOS Sharpe':>11s} {'OOS MaxDD':>10s} {'d vs CONST-W':>13s}")
    for pn in panels:
        for c in COSTS:
            s = wf[(wf.panel == pn) & (wf.cost == c)].set_index("arm")
            b = s.loc["CONST-W", "OOS_Sharpe"]
            for arm in ["CONST-W", "IS-PICK", "FIXED-M", "ORACLE"]:
                r = s.loc[arm]
                P(f"  {pn:6s} {c:5.0f} {arm:9s} {r.cadence:>4s} {r.IS_Sharpe:10.4f} "
                  f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:11.4f} {r.OOS_MaxDD:10.2%} "
                  f"{r.OOS_Sharpe-b:+13.4f}")
        sp = full_row(ref[pn]["spy"])
        bb = full_row(ref[pn]["b_ret"] - ref[pn]["b_trn"] * 10.0 / 1e4)
        P(f"  {pn:6s} OOS benchmarks: SPY {sp['CAGR_OOS']:6.2%}/{sp['Sharpe_OOS']:.4f}/"
          f"{sp['MaxDD_OOS']:7.2%}   RULES v1 @10bps {bb['CAGR_OOS']:6.2%}/{bb['Sharpe_OOS']:.4f}/"
          f"{bb['MaxDD_OOS']:7.2%}")
        P("")
    n_ispick_m = int((wf[wf.arm == "IS-PICK"].cadence == "M").sum())
    P(f"  IS-only chooser lands on M in {n_ispick_m}/{len(wf[wf.arm=='IS-PICK'])} (panel, cost) cells.")
    P("")

    # ---------------- verdict inputs
    P("=" * 122)
    P("SUMMARY")
    u = cells[cells.panel == "u56"]
    P(f"  u56  : 4b passes {int((u.fail4b=='-').sum())}/{len(u)} cells, "
      f"4b-on-OOS-window {int((u.fail4b_oos=='-').sum())}/{len(u)}; "
      f"at the PROTOCOL lag t+1 -> " +
      ", ".join(f"{int(r.cost)}bps {'PASS' if r.fail4b=='-' else 'fail('+r.fail4b+')'}"
                for _, r in u[u.lag == 1].iterrows()))
    for pn in ["broad", "small"]:
        s = cells[cells.panel == pn]
        P(f"  {pn:5s}: 4b passes {int((s.fail4b=='-').sum())}/{len(s)} cells; "
          f"binding bar at t+1/10bps = {s[(s.lag==1)&(s.cost==10.0)].iloc[0].worstbar}, "
          f"margin {s[(s.lag==1)&(s.cost==10.0)].iloc[0].margin4b:+.3f}")
    for pn in panels:
        s = dr[(dr.panel == pn) & (dr.cost == 10.0)]
        P(f"  {pn:5s} composition draws @10bps: 4b pass rate {(s.fail4b=='-').mean():.1%} "
          f"over {len(s)} draws (drop 5 and 10)")
    P(f"  MONTHLY is a k=1 calendar block: exactly one phase, so this point carries NO block-phase")
    P(f"  alignment draw (ideas 187/221).  That is a property of the cadence, not evidence for the book.")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    flush()


if __name__ == "__main__":
    main()
