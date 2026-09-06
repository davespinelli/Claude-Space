#!/usr/bin/env python3
"""Idea 296 - "re-quote-every-de-gross-claim-with-its-constant-leverage-replay"
(lane cloud, 2026-09-06).

QUEUE wording (verbatim)
------------------------
    "idea 290 shows a DEGROSS-vs-RESPREAD contrast is 91.4% cash drag and that the record's
     natural estimator (gap on mean gross) captures only R2 0.573 of it.  Census every published
     de-gross result and attach the zero-parameter constant-leverage replay beside it; report how
     many gate claims survive once the exposure share is removed.  Max 2 params."

The question in one line
------------------------
A de-grossing gate holds less on average.  Holding less is worth drawdown and costs CAGR all by
itself, with no gate and no timing.  So every published claim of the form "the de-grossed gate
book beats X" has a free rider inside it.  The zero-parameter way to take the rider out is the
CONSTANT-LEVERAGE REPLAY: run the comparand at the fixed leverage that reproduces the de-grossed
book's OWN realised mean gross, and ask whether the gate still wins.

Two replays, both zero-parameter (the constant is READ OFF the cell, never fitted)
---------------------------------------------------------------------------------
    REPLAY-EW   c2 * EWall, c2 = mean gross(DG) / mean gross(EWall).  NO gate at all: hold every
                live name, all the time, at the de-grossed book's average exposure.  This is the
                "just hold less" comparand and it removes BOTH the selection and the timing.
    REPLAY-RS   c1 * RESPREAD-twin, c1 = mean gross(DG) / mean gross(RS).  Same names, same
                relative weights, constant leverage: removes the TIMING only, keeps the
                selection.  Idea 290's decomposition comparand, run as an actual costed book.
Both are traded at the cell's own cadence and charged the same 10 bps, so nothing is free.

Corpus - the published de-gross construction space
--------------------------------------------------
Three families, all three of which the record has published de-gross results for:
    MA      hold every name inside the 200d +/- b band, gross/N_live per name, gated-out weight
            to cash (RULES v2's own form).
    MAVOL   the same, additionally requiring vol20 < 0.60.
    TOP20   rank the MA-eligible names by the scan.py composite and hold the top 20 at a FIXED
            gross/20 each - idea 73/240/289's channel, which de-grosses whenever fewer than 20
            names are eligible without ever saying so.
    x 3 panels (SMALL439, U56, B136) x 3 cadences (W, M, Q) x 6 bands = 162 cells.
Each cell is run as DEGROSS, its RESPREAD twin, REPLAY-EW, REPLAY-RS and the full-gross no-filter
control = 648 backtests + 9 controls, at 10 bps and 0 bps (costs are linear in turnover, so one
run serves both rungs exactly).  Plus the LIVE RULES v2 book and its own two replays.

Part A also censuses the record itself: every row of LEADERBOARD.md and every CHANGELOG entry
matching the de-gross token set is counted and classified by declared regex, so the mapping from
"published claims" to "re-run cells" is stated rather than assumed.

Pre-registered hypotheses (bars fixed before any number was read)
-----------------------------------------------------------------
D0  VALIDITY.  (i) The vectorised backtester equals `engine.backtest` to < 1e-12 on returns and
    held gross.  (ii) Each replay's realised mean gross matches its cell's DG mean gross to
    < 0.005.  (iii) The leverage identity r_dg,t == c_t * r_rs,t holds at 0 bps to < 1e-12 on all
    162 pairs.  If (i) or (iii) fails the run is aborted; (ii) is reported per cell and cells
    over the bar are excluded from the census and counted.

D1  DO THE SHARPE CLAIMS SURVIVE?  Incumbent claim rate = share of DG cells with
    Sharpe > full-gross no-filter control (the record's usual comparand).  Survival rate = share
    with Sharpe > REPLAY-EW.  Declared reading: the published de-gross claims are EXPOSURE claims
    if the survival rate is <= 0.50 AND below the incumbent rate.

D2  DOES THE DRAWDOWN CLAIM SURVIVE?  De-grossing is sold as drawdown protection.  Bar: it
    survives if DG's MaxDD is shallower than its exposure-matched REPLAY-EW in >= 2/3 of cells.

D3  THE CAGR PRICE.  Mean dCAGR(DG - REPLAY-EW) and its sign rate; plus the exposure share of the
    DG-minus-control CAGR gap on this wider corpus (idea 290 measured 91.4% on one panel).
    Declared: idea 290's share replicates if the corpus median share is in [0.80, 1.00].

D4  THE KEEP PATHS.  4a and 4b pass counts for DG and for REPLAY-EW.  Declared: the gate adds
    nothing a capital allocator can use if REPLAY-EW passes 4b at least as often as DG.

D5  THE LIVE BOOK.  RULES v2 (universe.json, 200d +/-3%, weekly, 0.75 gross) against its own two
    replays on CAGR / Sharpe / MaxDD / 4b.  This is the claim that matters for real capital.

D6  RULE 8.  (band, cadence) chosen on IS Sharpe (<= 2016-12-31) inside each panel x family arm;
    2017-2026 read once.  OOS DG vs its own replays, the control, SPY and the live book.

Tuned parameters (PROTOCOL rule 4: at most two)
-----------------------------------------------
    band b   in {0.00, 0.02, 0.03, 0.05, 0.08, 0.12}
    cadence  in {W, M, Q}
Reported at EVERY value, selected at none except inside the rule-8 walk-forward.  Panel, family
and construction are REPORTED dimensions.  The replay constants are not parameters: each is the
cell's own realised mean gross ratio.

SURVIVORSHIP: all three panels are CURRENT constituents - prices_small.csv is a screen of today's
sub-$2B names (44 dropped for max_1d_move >= 1.0) and universe(_broad).json are today's large
caps / ETFs; no delistings.  Every headline here is an arm-minus-arm contrast on the SAME names
and days, so the bias very largely cancels out of the DG-minus-replay columns; it does NOT cancel
out of the 4a / 4b columns, which are levels.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
Writes .console.txt, .census.csv, .cells.csv, .record.csv, .walkforward.csv, .result.md.
"""
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, band_state, rules_v2_weights, score
from engine import backtest, metrics, rebalance_mask

OUT = Path(__file__).with_suffix("")
COST_BPS = 10
GROSS = 0.75
MAX_VOL = 0.60
NTOP = 20
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]
CADENCES = ["W", "M", "Q"]
FAMILIES = ["MA", "MAVOL", "TOP20"]
PANELS = ["SMALL439", "U56", "B136"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

TOL_ENGINE = 1e-12
TOL_IDENT = 1e-12
TOL_MATCH = 0.005          # realised mean gross matching bar for a replay

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 700)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def flush():
    OUT.with_suffix(".console.txt").write_text("\n".join(_lines) + "\n")


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


# ------------------------------------------------------------------ backtester
def cad_mask(idx, cad):
    return rebalance_mask(idx, cad)


def fast_backtest(prices, weights, cad="W"):
    """Vectorised equivalent of engine.backtest; returns 0-bps returns, turnover and held gross."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad).shift(1, fill_value=False).values.copy()
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
    return dict(r0=pd.Series((held * rets).sum(axis=1), index=idx),
                turn=pd.Series(turn, index=idx),
                gross=pd.Series(held.sum(axis=1), index=idx))


# ------------------------------------------------------------------ books
def live_mask(px):
    return px.notna() & px.shift(1).notna()


def elig_mask(px, family, band):
    g = band_state(px, band) & live_mask(px)
    if family == "MAVOL":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        g = g & (vol20 < MAX_VOL)
    return g


def weights_of(px, family, band, construction):
    """DEGROSS: gated-out weight goes to cash.  RESPREAD: the same names always at full gross."""
    g = elig_mask(px, family, band)
    if family == "TOP20":
        s, _, _ = score(px, vol_scale=True)
        sel = s.where(g).rank(axis=1, ascending=False) <= NTOP
        sel = sel & g
        if construction == "DEGROSS":
            return sel.astype(float) * (GROSS / NTOP)          # fixed gross/n -> de-grosses
        k = sel.sum(axis=1).clip(lower=1)
        return sel.astype(float).div(k, axis=0) * GROSS
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def control_weights(px):
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


# ------------------------------------------------------------------ stats
def stat(r):
    m = metrics(r)
    h = len(r) // 2
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isSharpe=mi["Sharpe"], oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                oMaxDD=mo["MaxDD"])


def fail_4b(s, spy_s):
    t = {"H1": s["H1"] > spy_s["H1"], "H2": s["H2"] > spy_s["H2"],
         "OOS": s["oSharpe"] > spy_s["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy_s["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def cagr_of(r):
    return metrics(r)["CAGR"]


# ------------------------------------------------------------------ part A: the record census
DG_TOKEN = re.compile(r"de-gross|degross|de-grossed|\bdg\b", re.I)
CLAIM = re.compile(r"beat|wins|better|survives|buys|worth|outperform|>", re.I)
KEEPW = re.compile(r"\b4a\b|\b4b\b|KEEP", re.I)


def record_census():
    rows = [l for l in (REPO / "research" / "LEADERBOARD.md").read_text().split("\n")
            if l.startswith("| 2")]
    ents = [l for l in (REPO / "research" / "CHANGELOG.md").read_text().split("\n")
            if l.startswith("- 20")]
    lb = [l for l in rows if DG_TOKEN.search(l)]
    cl = [l for l in ents if DG_TOKEN.search(l)]
    out = pd.DataFrame([
        dict(source="LEADERBOARD.md", total=len(rows), de_gross=len(lb),
             with_comparative_claim=sum(bool(CLAIM.search(l)) for l in lb),
             touching_a_KEEP_path=sum(bool(KEEPW.search(l)) for l in lb)),
        dict(source="CHANGELOG.md", total=len(ents), de_gross=len(cl),
             with_comparative_claim=sum(bool(CLAIM.search(l)) for l in cl),
             touching_a_KEEP_path=sum(bool(KEEPW.search(l)) for l in cl)),
    ])
    fam = pd.DataFrame([dict(token=t, leaderboard=sum(bool(re.search(t, l, re.I)) for l in lb),
                             changelog=sum(bool(re.search(t, l, re.I)) for l in cl))
                        for t in ["SMALL|sub-\\$2B", "U56|universe.json", "B136|broad",
                                  "\\bMA\\b|200d", "MAVOL|vol20", "TOP\\s?20|n=20|top-20",
                                  "RESPREAD|respread", "RULES v2|live book"]])
    return out, fam, lb, cl


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P("=" * 175)
    P(f"IDEA 296 - re-quote-every-de-gross-claim-with-its-constant-leverage-replay "
      f"(lane cloud, {pd.Timestamp.today().date()})")
    P("=" * 175)
    P("A de-grossing gate holds less on average, and holding less buys drawdown and costs CAGR by")
    P("itself.  Every published de-gross claim therefore carries a free rider.  This run attaches")
    P("the zero-parameter CONSTANT-LEVERAGE REPLAY - the comparand run at the de-grossed book's")
    P("own realised mean gross - to every cell of the published de-gross construction space and")
    P("counts how many gate claims survive.")
    P(f"Costs {COST_BPS} bps (plus a 0-bps rung), gross {GROSS}, next-day execution, no shorting, "
      f"no leverage.")

    # ---------------- part A
    P("\n" + "-" * 175)
    P("PART A - CENSUS OF THE RECORD ITSELF (declared regexes; a mapping, not a semantic reading)")
    P("-" * 175)
    ca, fam, lb, cl = record_census()
    P(fmt(ca.set_index("source")))
    P("\nwhat those de-gross rows/entries mention (token counts, rows can match several):")
    P(fmt(fam.set_index("token")))
    pd.DataFrame(dict(source=["LEADERBOARD"] * len(lb) + ["CHANGELOG"] * len(cl),
                      line=[l[:400] for l in lb + cl])).to_csv(
        OUT.with_suffix(".record.csv"), index=False)
    P(f"\nThe re-run corpus below covers the three panels, the three construction families and the")
    P(f"two dials those rows name, plus the live book: {len(PANELS)} x {len(FAMILIES)} x "
      f"{len(CADENCES)} x {len(BANDS)} = {len(PANELS)*len(FAMILIES)*len(CADENCES)*len(BANDS)} "
      f"cells.  Rows that quote a construction outside it (sleeves, stops, ddctl, blends) are NOT")
    P("re-run here and are reported as the un-mapped remainder, not silently counted as survivors.")

    # ---------------- panels
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    PX = {"SMALL439": (pxs[inv], pxs["SPY"]),
          "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
          "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"])}
    starts = {k: v[0].index[260] for k, v in PX.items()}
    P(f"\npanels: SMALL439 {PX['SMALL439'][0].shape[1]} names ({len(bad)} dropped for "
      f"max_1d_move >= 1.0), U56 {PX['U56'][0].shape[1]}, B136 {PX['B136'][0].shape[1]}")
    for k in PANELS:
        P(f"  {k}: evaluated {starts[k].date()} .. {PX[k][0].index[-1].date()} "
          f"({len(PX[k][0].loc[starts[k]:]) / 252:.2f} yrs)")

    # ---------------- D0(i) engine equivalence
    eq = 0.0
    for k in PANELS:
        px = PX[k][0]
        for fmly in FAMILIES:
            w = weights_of(px, fmly, 0.03, "DEGROSS")
            f = fast_backtest(px, w, "W")
            e = backtest(px, w, cost_bps=COST_BPS, freq="W")
            eq = max(eq, float(((f["r0"] - f["turn"] * COST_BPS / 1e4) - e["returns"]).abs().max()),
                     float((f["gross"] - e["weights"].sum(axis=1)).abs().max()))
    P(f"\n  D0(i) vectorised backtester vs engine.backtest, 9 books: max |diff| {eq:.3e} "
      f"(bar {TOL_ENGINE:g}) -> {'HOLDS' if eq < TOL_ENGINE else 'FAILS'}")
    if eq >= TOL_ENGINE:
        P("!! aborting."); flush(); sys.exit(1)

    # ---------------- references
    ctrl, ctrl_g, spy_stat = {}, {}, {}
    for k in PANELS:
        px, spy = PX[k]
        st = starts[k]
        for cad in CADENCES:
            f = fast_backtest(px, control_weights(px), cad)
            ctrl[(k, cad)] = stat((f["r0"] - f["turn"] * COST_BPS / 1e4).loc[st:])
            ctrl_g[(k, cad)] = float(f["gross"].loc[st:].mean())
        spy_stat[k] = stat(spy.pct_change().fillna(0.0).loc[st:])
    px_u = load_universe()
    live_w = rules_v2_weights(px_u)
    live_f = fast_backtest(px_u[[c for c in px_u.columns]], live_w, "W")
    live_s = stat(backtest(px_u, live_w, cost_bps=COST_BPS, freq="W")["returns"].loc[starts["U56"]:])
    P("\nREFERENCE BOOKS")
    ref = {f"CONTROL EWall {k} {c} (full gross, no filter)": ctrl[(k, c)]
           for k in PANELS for c in CADENCES}
    ref["RULES v2 (LIVE BOOK, 4a comparand)"] = live_s
    for k in PANELS:
        ref[f"SPY on {k} window (4b comparand)"] = spy_stat[k]
    P(fmt(pd.DataFrame(ref).T))

    # ---------------- the grid
    P("\n" + "-" * 175)
    P(f"THE CENSUS - {len(PANELS)*len(FAMILIES)*len(CADENCES)*len(BANDS)} cells x 4 books "
      f"(DEGROSS, RESPREAD twin, REPLAY-EW, REPLAY-RS) + controls")
    P("-" * 175)
    rows, ident = [], 0.0
    for k in PANELS:
        px, _ = PX[k]
        st = starts[k]
        years = len(px.loc[st:]) / 252
        cw = control_weights(px)
        for fmly in FAMILIES:
            for b in BANDS:
                w_dg = weights_of(px, fmly, b, "DEGROSS")
                w_rs = weights_of(px, fmly, b, "RESPREAD")
                for cad in CADENCES:
                    f_dg = fast_backtest(px, w_dg, cad)
                    f_rs = fast_backtest(px, w_rs, cad)
                    g_dg = f_dg["gross"].loc[st:]
                    g_rs = f_rs["gross"].loc[st:]
                    r0 = {"DG": f_dg["r0"].loc[st:], "RS": f_rs["r0"].loc[st:]}
                    c_t = (g_dg / g_rs.replace(0, np.nan)).fillna(0.0)
                    ident = max(ident, float((r0["DG"] - c_t * r0["RS"]).abs().max()))
                    mg_dg, mg_rs = float(g_dg.mean()), float(g_rs.mean())
                    c1 = mg_dg / mg_rs
                    c2 = mg_dg / ctrl_g[(k, cad)]
                    f_re_rs = fast_backtest(px, w_rs * c1, cad)
                    f_re_ew = fast_backtest(px, cw * c2, cad)
                    books = {"DG": f_dg, "RS": f_rs, "REPLAY-RS": f_re_rs, "REPLAY-EW": f_re_ew}
                    S, R10 = {}, {}
                    for nm, f in books.items():
                        R10[nm] = (f["r0"] - f["turn"] * COST_BPS / 1e4).loc[st:]
                        S[nm] = stat(R10[nm])
                    mg = {nm: float(f["gross"].loc[st:].mean()) for nm, f in books.items()}
                    match_rs = abs(mg["REPLAY-RS"] - mg_dg)
                    match_ew = abs(mg["REPLAY-EW"] - mg_dg)
                    ctl = ctrl[(k, cad)]
                    # idea 290's exposure share of the DG-minus-CONTROL 0-bps CAGR gap
                    r0_ctrl = fast_backtest(px, cw, cad)["r0"].loc[st:]
                    gap0 = 100 * (cagr_of(r0["DG"]) - cagr_of(r0_ctrl))
                    pred0 = 100 * (cagr_of((mg_dg / ctrl_g[(k, cad)]) * r0_ctrl) - cagr_of(r0_ctrl))
                    rows.append(dict(
                        panel=k, family=fmly, band=b, cad=cad,
                        mg_dg=mg_dg, mg_rs=mg_rs, mg_ctrl=ctrl_g[(k, cad)], c1=c1, c2=c2,
                        match_rs=match_rs, match_ew=match_ew,
                        dg_CAGR=S["DG"]["CAGR"], dg_Sharpe=S["DG"]["Sharpe"],
                        dg_MaxDD=S["DG"]["MaxDD"], dg_H1=S["DG"]["H1"], dg_H2=S["DG"]["H2"],
                        dg_isSharpe=S["DG"]["isSharpe"], dg_oCAGR=S["DG"]["oCAGR"],
                        dg_oSharpe=S["DG"]["oSharpe"], dg_oMaxDD=S["DG"]["oMaxDD"],
                        rs_Sharpe=S["RS"]["Sharpe"], rs_CAGR=S["RS"]["CAGR"],
                        rers_CAGR=S["REPLAY-RS"]["CAGR"], rers_Sharpe=S["REPLAY-RS"]["Sharpe"],
                        rers_MaxDD=S["REPLAY-RS"]["MaxDD"],
                        reew_CAGR=S["REPLAY-EW"]["CAGR"], reew_Sharpe=S["REPLAY-EW"]["Sharpe"],
                        reew_MaxDD=S["REPLAY-EW"]["MaxDD"], reew_H1=S["REPLAY-EW"]["H1"],
                        reew_H2=S["REPLAY-EW"]["H2"], reew_isSharpe=S["REPLAY-EW"]["isSharpe"],
                        reew_oCAGR=S["REPLAY-EW"]["oCAGR"], reew_oSharpe=S["REPLAY-EW"]["oSharpe"],
                        reew_oMaxDD=S["REPLAY-EW"]["oMaxDD"],
                        ctrl_Sharpe=ctl["Sharpe"], ctrl_CAGR=ctl["CAGR"], ctrl_MaxDD=ctl["MaxDD"],
                        gap0_pp=gap0, pred0_pp=pred0,
                        share=(pred0 / gap0) if abs(gap0) > 1e-12 else np.nan,
                        turn_dg=f_dg["turn"].loc[st:].sum() / years,
                        turn_reew=f_re_ew["turn"].loc[st:].sum() / years,
                        K1_beats_ctrl=bool(S["DG"]["Sharpe"] > ctl["Sharpe"]),
                        K2_beats_replay_ew=bool(S["DG"]["Sharpe"] > S["REPLAY-EW"]["Sharpe"]),
                        K5_beats_replay_rs=bool(S["DG"]["Sharpe"] > S["REPLAY-RS"]["Sharpe"]),
                        K3_dd_beats_replay=bool(S["DG"]["MaxDD"] > S["REPLAY-EW"]["MaxDD"]),
                        K4_cagr_beats_replay=bool(S["DG"]["CAGR"] >= S["REPLAY-EW"]["CAGR"]),
                        dg_4a=verdict_4a(S["DG"], live_s), reew_4a=verdict_4a(S["REPLAY-EW"], live_s),
                        dg_4b=fail_4b(S["DG"], spy_stat[k]) == "-",
                        reew_4b=fail_4b(S["REPLAY-EW"], spy_stat[k]) == "-",
                        dg_f4b=fail_4b(S["DG"], spy_stat[k]),
                        reew_f4b=fail_4b(S["REPLAY-EW"], spy_stat[k])))
        P(f"  {k} done ({time.time() - t0:.0f}s)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT.with_suffix(".cells.csv"), index=False)

    P(f"\n  D0(iii) identity r_dg,t == c_t*r_rs,t at 0 bps on {len(G)} pairs: worst {ident:.3e} "
      f"(bar {TOL_IDENT:g}) -> {'HOLDS' if ident < TOL_IDENT else 'FAILS'}")
    if ident >= TOL_IDENT:
        P("!! aborting."); flush(); sys.exit(1)
    over = G[(G.match_ew > TOL_MATCH) | (G.match_rs > TOL_MATCH)]
    P(f"  D0(ii) replay mean-gross matching: worst |diff| EW {G.match_ew.max():.5f}, "
      f"RS {G.match_rs.max():.5f} (bar {TOL_MATCH}); cells over the bar: {len(over)} of {len(G)}")
    if len(over):
        P(fmt(over[["panel", "family", "band", "cad", "mg_dg", "match_ew", "match_rs"]]))
    Gv = G[(G.match_ew <= TOL_MATCH) & (G.match_rs <= TOL_MATCH)].copy()
    P(f"  census runs on the {len(Gv)} cells that clear D0(ii).")

    # ---------------- D1
    P("\n" + "-" * 175)
    P("D1 - DO THE SHARPE CLAIMS SURVIVE THE REPLAY?")
    P("-" * 175)
    def rate(df, col):
        return float(df[col].mean())
    tab = Gv.groupby(["panel", "family"]).agg(
        n=("K1_beats_ctrl", "size"),
        beats_full_gross_control=("K1_beats_ctrl", "mean"),
        beats_REPLAY_EW=("K2_beats_replay_ew", "mean"),
        beats_REPLAY_RS=("K5_beats_replay_rs", "mean"),
        mean_dSharpe_vs_ctrl=("dg_Sharpe", "mean")).round(4)
    tab["mean_dSharpe_vs_ctrl"] = (Gv.groupby(["panel", "family"])
                                   .apply(lambda d: (d.dg_Sharpe - d.ctrl_Sharpe).mean(),
                                          include_groups=False).round(4))
    tab["mean_dSharpe_vs_replay"] = (Gv.groupby(["panel", "family"])
                                     .apply(lambda d: (d.dg_Sharpe - d.reew_Sharpe).mean(),
                                            include_groups=False).round(4))
    P(fmt(tab))
    r1, r2, r5 = rate(Gv, "K1_beats_ctrl"), rate(Gv, "K2_beats_replay_ew"), rate(Gv, "K5_beats_replay_rs")
    P(f"\nPOOLED: DG beats the full-gross control on Sharpe in {int(Gv.K1_beats_ctrl.sum())}/{len(Gv)} "
      f"({r1:.3f}); beats REPLAY-EW in {int(Gv.K2_beats_replay_ew.sum())}/{len(Gv)} ({r2:.3f}); "
      f"beats REPLAY-RS in {int(Gv.K5_beats_replay_rs.sum())}/{len(Gv)} ({r5:.3f})")
    P(f"mean dSharpe vs control {(Gv.dg_Sharpe - Gv.ctrl_Sharpe).mean():+.4f}, "
      f"vs REPLAY-EW {(Gv.dg_Sharpe - Gv.reew_Sharpe).mean():+.4f}, "
      f"vs REPLAY-RS {(Gv.dg_Sharpe - Gv.rers_Sharpe).mean():+.4f}")
    d1 = (r2 <= 0.50) and (r2 < r1)
    P(f"D1: survival rate {r2:.3f} vs incumbent {r1:.3f} -> "
      f"{'the published de-gross Sharpe claims are EXPOSURE claims' if d1 else 'claims survive the replay'}")

    # ---------------- D2
    P("\n" + "-" * 175)
    P("D2 - DOES THE DRAWDOWN CLAIM SURVIVE?  (DG MaxDD vs its exposure-matched REPLAY-EW)")
    P("-" * 175)
    dd = Gv.groupby(["panel", "family"]).apply(
        lambda d: pd.Series(dict(n=len(d), dg_shallower=d.K3_dd_beats_replay.mean(),
                                 mean_dg_MaxDD=d.dg_MaxDD.mean(),
                                 mean_replay_MaxDD=d.reew_MaxDD.mean(),
                                 mean_gap_pp=100 * (d.dg_MaxDD - d.reew_MaxDD).mean())),
        include_groups=False)
    P(fmt(dd))
    r3 = rate(Gv, "K3_dd_beats_replay")
    P(f"D2: DG is shallower than its exposure-matched replay in {int(Gv.K3_dd_beats_replay.sum())}/"
      f"{len(Gv)} cells ({r3:.3f}); mean MaxDD {Gv.dg_MaxDD.mean():.2%} vs "
      f"{Gv.reew_MaxDD.mean():.2%} -> "
      f"{'the drawdown claim SURVIVES' if r3 >= 2/3 else 'the drawdown claim does NOT survive'}")

    # ---------------- D3
    P("\n" + "-" * 175)
    P("D3 - THE CAGR PRICE, AND IDEA 290'S EXPOSURE SHARE ON THIS CORPUS")
    P("-" * 175)
    cg = Gv.groupby(["panel", "family"]).apply(
        lambda d: pd.Series(dict(n=len(d),
                                 mean_dCAGR_pp=100 * (d.dg_CAGR - d.reew_CAGR).mean(),
                                 pos_rate=d.K4_cagr_beats_replay.mean(),
                                 median_share=d.share.median(),
                                 mean_gap0_pp=d.gap0_pp.mean(),
                                 mean_pred0_pp=d.pred0_pp.mean())), include_groups=False)
    P(fmt(cg))
    med = float(Gv.share.median())
    P(f"D3: mean dCAGR(DG - REPLAY-EW) {100 * (Gv.dg_CAGR - Gv.reew_CAGR).mean():+.3f} pp/yr, "
      f"positive in {int(Gv.K4_cagr_beats_replay.sum())}/{len(Gv)}; corpus median exposure share "
      f"of the DG-minus-control gap {med:.4f} (idea 290: 0.914) -> "
      f"{'REPLICATES' if 0.80 <= med <= 1.00 else 'does NOT replicate the 0.80-1.00 band'}")

    # ---------------- D4
    P("\n" + "-" * 175)
    P("D4 - THE KEEP PATHS: DG vs its zero-parameter replay")
    P("-" * 175)
    kp = Gv.groupby(["panel", "family"]).apply(
        lambda d: pd.Series(dict(n=len(d), dg_4a=d.dg_4a.sum(), replay_4a=d.reew_4a.sum(),
                                 dg_4b=d.dg_4b.sum(), replay_4b=d.reew_4b.sum())),
        include_groups=False)
    P(fmt(kp))
    P(f"POOLED: 4a DG {int(Gv.dg_4a.sum())}/{len(Gv)} vs REPLAY-EW {int(Gv.reew_4a.sum())}/{len(Gv)}; "
      f"4b DG {int(Gv.dg_4b.sum())}/{len(Gv)} vs REPLAY-EW {int(Gv.reew_4b.sum())}/{len(Gv)}")
    P("\n4b failure reasons, DG:")
    P(fmt(Gv.dg_f4b.value_counts().to_frame("n")))
    P("4b failure reasons, REPLAY-EW:")
    P(fmt(Gv.reew_f4b.value_counts().to_frame("n")))
    if Gv.dg_4b.any():
        P("\nDG cells passing 4b:")
        P(fmt(Gv[Gv.dg_4b].set_index(["panel", "family", "cad", "band"])
              [["dg_CAGR", "dg_Sharpe", "dg_MaxDD", "dg_H1", "dg_H2", "dg_oSharpe",
                "reew_Sharpe", "reew_MaxDD", "reew_4b"]]))
    if Gv.reew_4b.any():
        P("\nREPLAY-EW cells passing 4b (the zero-parameter comparand):")
        P(fmt(Gv[Gv.reew_4b].set_index(["panel", "family", "cad", "band"])
              [["reew_CAGR", "reew_Sharpe", "reew_MaxDD", "reew_H1", "reew_H2", "reew_oSharpe",
                "mg_dg", "dg_4b"]].drop_duplicates()))
    d4 = int(Gv.reew_4b.sum()) >= int(Gv.dg_4b.sum())
    P(f"D4: {'the gate adds NOTHING to the KEEP paths' if d4 else 'the gate adds KEEP-path cells the replay does not'}")

    # ---------------- D5 the live book
    P("\n" + "-" * 175)
    P("D5 - THE LIVE BOOK (RULES v2) AGAINST ITS OWN CONSTANT-LEVERAGE REPLAYS")
    P("-" * 175)
    st = starts["U56"]
    pxu = PX["U56"][0]
    lw = rules_v2_weights(px_u)[pxu.columns]
    f_live = fast_backtest(pxu, lw, "W")
    mg_live = float(f_live["gross"].loc[st:].mean())
    g = elig_mask(pxu, "MA", 0.03)
    k_ = g.sum(axis=1).clip(lower=1)
    w_rs_live = g.astype(float).div(k_, axis=0) * GROSS
    f_rs_live = fast_backtest(pxu, w_rs_live, "W")
    c1 = mg_live / float(f_rs_live["gross"].loc[st:].mean())
    c2 = mg_live / ctrl_g[("U56", "W")]
    f_re_rs = fast_backtest(pxu, w_rs_live * c1, "W")
    f_re_ew = fast_backtest(pxu, control_weights(pxu) * c2, "W")
    live_tab, live_rows = {}, {}
    for nm, f in (("RULES v2 (live)", f_live), ("RESPREAD twin", f_rs_live),
                  ("REPLAY-RS (const leverage, same names)", f_re_rs),
                  ("REPLAY-EW (const leverage, NO gate)", f_re_ew)):
        r = (f["r0"] - f["turn"] * COST_BPS / 1e4).loc[st:]
        s = stat(r)
        s["mean_gross"] = float(f["gross"].loc[st:].mean())
        s["turn_yr"] = f["turn"].loc[st:].sum() / (len(r) / 252)
        s["4b"] = fail_4b(s, spy_stat["U56"])
        live_rows[nm] = s
    live_rows["SPY"] = {**spy_stat["U56"], "mean_gross": 1.0, "turn_yr": 0.0,
                        "4b": fail_4b(spy_stat["U56"], spy_stat["U56"])}
    LT = pd.DataFrame(live_rows).T
    P(fmt(LT[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD",
              "mean_gross", "turn_yr"]]))
    P("4b: " + " | ".join(f"{k}: {v['4b']}" for k, v in live_rows.items()))
    dl = LT.loc["RULES v2 (live)"]
    dr = LT.loc["REPLAY-EW (const leverage, NO gate)"]
    P(f"D5: the live book at mean gross {mg_live:.4f} vs a NO-GATE book held at the same constant "
      f"leverage: dSharpe {dl.Sharpe - dr.Sharpe:+.4f}, dCAGR "
      f"{100 * (dl.CAGR - dr.CAGR):+.3f} pp/yr, dMaxDD {100 * (dl.MaxDD - dr.MaxDD):+.2f} pp "
      f"(positive = live book shallower)")

    # ---------------- D6 walk-forward
    P("\n" + "-" * 175)
    P("D6 - RULE 8 WALK-FORWARD: (band, cadence) chosen on IS Sharpe inside each panel x family")
    P("arm; 2017-2026 read once.  The replay is re-selected by ITS OWN IS Sharpe, so both sides")
    P("get the same freedom.")
    P("-" * 175)
    wf = []
    for k in PANELS:
        for fmly in FAMILIES:
            s = Gv[(Gv.panel == k) & (Gv.family == fmly)]
            if not len(s):
                continue
            pdg = s.loc[s.dg_isSharpe.idxmax()]
            pre = s.loc[s.reew_isSharpe.idxmax()]
            wf.append(dict(panel=k, family=fmly,
                           dg_band=pdg.band, dg_cad=pdg.cad, dg_oCAGR=pdg.dg_oCAGR,
                           dg_oSharpe=pdg.dg_oSharpe, dg_oMaxDD=pdg.dg_oMaxDD,
                           replay_band=pre.band, replay_cad=pre.cad,
                           replay_oCAGR=pre.reew_oCAGR, replay_oSharpe=pre.reew_oSharpe,
                           replay_oMaxDD=pre.reew_oMaxDD,
                           ctrl_oSharpe=ctrl[(k, pdg.cad)]["oSharpe"],
                           spy_oSharpe=spy_stat[k]["oSharpe"], live_oSharpe=live_s["oSharpe"],
                           dg_beats_replay=bool(pdg.dg_oSharpe > pre.reew_oSharpe),
                           dg_beats_spy=bool(pdg.dg_oSharpe > spy_stat[k]["oSharpe"]),
                           dg_beats_live=bool(pdg.dg_oSharpe > live_s["oSharpe"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    P(fmt(WF.set_index(["panel", "family"])))
    P(f"\nOOS: the IS-chosen de-gross arm beats its own IS-chosen replay in "
      f"{int(WF.dg_beats_replay.sum())}/{len(WF)} arms, SPY in {int(WF.dg_beats_spy.sum())}/{len(WF)}, "
      f"the live book in {int(WF.dg_beats_live.sum())}/{len(WF)}")
    P(f"mean OOS Sharpe: de-gross {WF.dg_oSharpe.mean():.4f} vs replay {WF.replay_oSharpe.mean():.4f} "
      f"(delta {WF.dg_oSharpe.mean() - WF.replay_oSharpe.mean():+.4f}); "
      f"mean OOS CAGR {WF.dg_oCAGR.mean():.2%} vs {WF.replay_oCAGR.mean():.2%}")

    # ---------------- census table + summary
    Gv.to_csv(OUT.with_suffix(".census.csv"), index=False)
    P("\n" + "=" * 175)
    P("SUMMARY")
    P("=" * 175)
    sm = pd.DataFrame([
        dict(test="D1 Sharpe claims survive the replay", bar="rate > 0.50",
             result=f"{r2:.3f} (incumbent vs control {r1:.3f})",
             reading="exposure claims" if d1 else "claims survive"),
        dict(test="D2 drawdown claim survives", bar=">= 2/3 of cells",
             result=f"{r3:.3f}", reading="survives" if r3 >= 2 / 3 else "does NOT survive"),
        dict(test="D3 exposure share replicates idea 290", bar="median in [0.80, 1.00]",
             result=f"{med:.4f}", reading="replicates" if 0.80 <= med <= 1.00 else "does not"),
        dict(test="D4 replay passes 4b at least as often", bar="replay >= DG",
             result=f"DG {int(Gv.dg_4b.sum())} vs replay {int(Gv.reew_4b.sum())}",
             reading="gate adds nothing" if d4 else "gate adds cells"),
        dict(test="D6 IS-chosen DG beats IS-chosen replay OOS", bar=">= 5/9 arms",
             result=f"{int(WF.dg_beats_replay.sum())}/{len(WF)}",
             reading="survives OOS" if WF.dg_beats_replay.sum() >= 5 else "does NOT survive OOS"),
    ])
    P(fmt(sm.set_index("test")))
    P(f"runtime {time.time() - t0:.0f}s")
    flush()


if __name__ == "__main__":
    main()
