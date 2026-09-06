#!/usr/bin/env python3
"""QUEUE idea 276 — is-the-gate-a-drawdown-instrument-on-every-panel (cloud, 2026-09-06).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 274 found the ONLY thing RULES v2's 200d band buys that survives matched realised
gross, two turnover-matched gate nulls, both panels and rule 8 is MaxDD (best of 0/60 and
0/20 draws everywhere), while its Sharpe edge is u56-only and IS-absent (2009-2016: v2
1.1043 vs constant-gross 1.1116).  Re-price the band against the record's other de-grossing
instruments (idea 40's ddctl, gross50, the vol gate) on drawdown-per-pp-of-forgone-CAGR at
MATCHED realised gross, and report whether the band is the cheapest drawdown instrument the
project has or merely one of several.  Max 2 params."

The axis.  Idea 94 priced instruments against the static gross lever but at a FIXED base
gross (each arm ran at 0.75 x base and landed wherever its own gate left it), so an arm that
de-grossed harder looked "safer" partly because it held less.  This run removes that channel
outright: every arm's base multiplier m is SOLVED so the arm's realised mean gross equals a
pre-set target G on the window being scored.  At matched G the static lever IS the control
(gross50 is the G=0.50 rung of that ladder, i.e. the reference, not a competitor), and the
price of an instrument is

    price = (CAGR_control - CAGR_arm) / (|MaxDD_control| - |MaxDD_arm|)   pp CAGR per pp MaxDD
    yield = 1 / price                                                    pp MaxDD per pp CAGR

both measured on the SAME panel, the SAME days, the SAME cost rung and now the SAME realised
gross.  An instrument earns a place in RULES only if it buys drawdown MORE CHEAPLY than
simply holding less of the same book; the band is the incumbent (live RULES v2) and this run
asks whether it is the cheapest such instrument or merely one of several.

Book (fixed, never selected).  EWall: equal-weight EVERY priced name, gross 1.0 before m,
weekly, t+1, long-only.  This is RULES v2's book with the gate removed, so the band arm below
is exactly the live book at matched gross.

Panels (all reported, none selected)
    U56     research/universe.json, 56 instruments (the live panel; SPY is a constituent of
            it and RULES v2 holds it, so it is tradable here too)
    B136    research/universe_broad.json, 136 large caps + ETFs
    SMALL439 data/prices_small.csv, sub-$2B names since 2010, minus the 44 with
            max_1d_move >= 1.0 in data/small_meta.csv; SPY joined as benchmark only

Instruments (6 treated, ALL reported, none dropped) — every one in the de-gross (`dg`)
convention, i.e. gated-out weight goes to CASH, because that is the only convention in which
an instrument is comparable to the gross lever:
    static   no rule at all, gross m                     — THE CONTROL (idea 66's exact dial;
             the record's `gross50` is this arm at G=0.50)
    band3    200d MA with a +/-3% hysteresis band        — the LIVE RULES v2 instrument
    g200     plain per-name 200d MA gate
    abs12    absolute momentum, px > px 252d ago
    vol60    vol20 < 0.60                                — v1's other eligibility half
    v1gate   200d AND vol20 < 0.60                       — the whole v1 gate as one instrument
    ddctl8   book DD > 8% -> halve, reset at DD > -4%    — idea 22/40's book-level control

Tuned parameters (PROTOCOL rule 4).  TWO: the instrument family and the target gross G.
Every setting inside a family (band width 3%, vol cap 0.60, DD trigger 8% / cut 0.5) is the
value already published in the record and is NOT re-tuned here.  m is not a tuned parameter:
it is solved by the matching constraint.

Grid, all points reported: G in {0.40, 0.50, 0.60, 0.75} x panel in {U56, B136, SMALL439} x
cost in {10, 25} bps x 7 arms = 168 cells, plus the same grid re-fitted on the IS window for
rule 8.

Pre-registered predictions (written before any number of this run was read)
    P1  At MATCHED realised gross the median price of every gate arm is > 0 but finite, i.e.
        gates still buy some drawdown that pure de-grossing does not — idea 274 found the
        band's MaxDD edge survived matched gross on both panels.
    P2  band3 is NOT uniquely cheapest on every panel: on SMALL439 the 200d family is
        inverted (ideas 38/49/60), so at least one panel ranks a non-trend arm (vol60 or
        ddctl8) first, and the answer to the QUEUE question is "one of several".
    P3  ddctl8 prices close to band3 on U56 (idea 22 measured 1.02 vs the lever's 0.57 before
        gross matching) and is the cheapest arm on the panel where the trend family inverts.
    P4  Several arms have NEGATIVE dd_bought at some G (they add drawdown at matched gross);
        those cells are reported as undefined price, never silently dropped.
    P5  No arm converts a 4b failure into a 4b pass on all three panels (measurement run).

Walk-forward (PROTOCOL rule 8), selection fixed before any OOS number was read
    S1  In each panel x cost x G cell, fit m on 2009-2016 (2010-2016 on SMALL439) only, rank
        arms by IS price among those that bought >= 1.0 pp of IS MaxDD, and pick the LOWEST.
        Evaluate that arm on 2017-2026 untouched, with the IS-fitted m: report OOS CAGR /
        Sharpe / MaxDD vs the matched-gross control, vs the live RULES v2 book on that panel
        and vs SPY, plus its OOS price and OOS rank among the arms of that cell.
    S2  Spearman(IS price, OOS price) across arms within each cell.  A price list is only
        usable if the ORDERING is stable out of sample.

Both KEEP paths are evaluated for every arm at every grid point (4a vs RULES v2 on the same
panel, 4b vs SPY, PROTOCOL rule 4).

Execution realism (PROTOCOL rule 2): weights decided at close t applied at t+1, weekly
rebalance, long-only, no leverage, costs charged inside the loop so the DD state machine sees
NET equity.  10 bps is the PROTOCOL rung; 25 bps reported for every arm.

SURVIVORSHIP: all three panels are current-constituent lists (SMALL439 worst: no delistings,
so its levels are optimistic by an unknown one-directional margin that falls hardest on
beaten-down names — exactly the cohort a trend gate exits).  This run compares arms sharing a
panel, days, cost and realised gross, so the treatment deltas are far less exposed than the
levels; no absolute number from SMALL439 should be quoted as an expected return.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = ROOT / "research" / "backtests" / "2026-09-06_is-the-gate-a-drawdown-instrument-on-every-panel_cloud"
FREQ = "W"
COSTS = [10.0, 25.0]
GROSS_TARGETS = [0.40, 0.50, 0.60, 0.75]
ARMS = ["static", "band3", "g200", "abs12", "vol60", "v1gate", "ddctl8"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MAX_VOL, BAND, DD_TRIG, DD_CUT = 0.60, 0.03, 0.08, 0.5
MATCH_TOL = 0.005   # a cell is UNMATCHED (idea 154's reachability ceiling) if the arm cannot
                    # reach the target gross even at m = 1.0; such cells are reported but are
                    # never used for a price comparison or a rule-8 pick.

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ panels
def build_panels():
    out = {}
    px = load_universe().dropna(how="all").ffill()
    out["U56"] = (px, list(px.columns))                      # SPY is a live constituent here
    pb = load_universe(broad=True)
    out["B136"] = (pb, [c for c in pb.columns if c != "SPY"])
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    stk = [c for c in ps.columns if c != "SPY" and c not in bad]
    ps = ps[stk + ["SPY"]].dropna(how="all").ffill()
    out["SMALL439"] = (ps, stk)
    for k, (p, t) in out.items():
        P(f"  {k:9s} {p.shape[1]:4d} cols, {len(t):4d} tradable, {p.index[0].date()} -> {p.index[-1].date()}")
    P(f"  SMALL439 dropped {len([c for c in ps.columns if c in bad])} names with max_1d_move >= 1.0")
    return out


# ------------------------------------------------------------------ signals / weights
def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def gate_mask(px, arm):
    if arm in ("static", "ddctl8"):
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if arm == "g200":
        return (px > ma).fillna(False)
    if arm == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + BAND), 1.0).mask(px < ma * (1 - BAND), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if arm == "abs12":
        return (px > px.shift(252)).fillna(False)
    if arm == "vol60":
        return (vol20(px) < MAX_VOL).fillna(False)
    if arm == "v1gate":
        return ((px > ma) & (vol20(px) < MAX_VOL)).fillna(False)
    raise ValueError(arm)


def ewall_base(px, tradable):
    """Equal weight every priced tradable name, gross 1.0 (m scales it)."""
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    e[tradable] = px[tradable].notna().astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def arm_targets(px, tradable, arm):
    W = ewall_base(px, tradable)
    return W.where(gate_mask(px, arm).reindex(columns=W.columns, fill_value=True), 0.0)


# ------------------------------------------------------------------ simulator
def run(px, W, m=1.0, ddctl=False, bps=10.0, freq=FREQ):
    """engine.backtest + static gross m + optional book-DD control.  With ddctl off and m=1
    it reproduces engine.backtest exactly (asserted in main)."""
    rets = px.pct_change().fillna(0.0).values
    tgt = (W.reindex(px.index).fillna(0.0).values) * m
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape
    cur = np.zeros(ncol)
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    eq, pk, armed, episodes = 1.0, 1.0, False, 0
    for i in range(nrow):
        if mask[i] and i > 0:                             # weights decided at t-1, applied now
            if ddctl:
                dd = eq / pk - 1.0                        # net equity through close i-1
                if not armed and dd < -DD_TRIG:
                    armed, episodes = True, episodes + 1
                elif armed and dd > -DD_TRIG / 2.0:
                    armed = False
            new = tgt[i - 1] * (DD_CUT if armed else 1.0)
            s = new.sum()
            if s > 1.0:
                new = new / s
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp)
        pk = max(pk, eq)
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r = pd.Series((held * rets).sum(axis=1) - turn * bps / 1e4, index=px.index)
    return dict(r=r, to=pd.Series(turn, index=px.index), gross=pd.Series(gross_s, index=px.index),
                episodes=episodes)


def fit_m(px, W, ddctl, bps, sl, target, tol=5e-4, itmax=8):
    """Solve m so mean realised gross over slice `sl` equals `target`.  Realised gross is
    monotone and near-linear in m, so a damped fixed point converges in 2-4 iterations."""
    m, hist = target, []
    for _ in range(itmax):
        res = run(px, W, m=m, ddctl=ddctl, bps=bps)
        g = float(res["gross"].loc[sl[0]:sl[1]].mean())
        hist.append((m, g))
        if abs(g - target) < tol or g <= 1e-9:
            return m, g, res, hist
        m = min(1.0, m * target / g)
    return m, g, res, hist


# ------------------------------------------------------------------ metrics helpers
def mm(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def price_of(arm_m, ctl_m):
    cost = (ctl_m["CAGR"] - arm_m["CAGR"]) * 100.0
    bought = (abs(ctl_m["MaxDD"]) - abs(arm_m["MaxDD"])) * 100.0
    price = cost / bought if bought > 1e-9 else np.nan
    yld = bought / cost if cost > 1e-9 else np.nan
    return cost, bought, price, yld


def argmin_rows(df):
    """Row-wise idxmin that returns 'none' for all-NaN rows instead of raising."""
    out = []
    for _, row in df.iterrows():
        out.append(row.idxmin() if row.notna().any() else "none")
    return pd.Series(out, index=df.index)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ------------------------------------------------------------------ main
def main():
    P("=" * 118)
    P("idea 276 — is the 200d band the cheapest drawdown instrument, at MATCHED realised gross, on every panel?")
    P("=" * 118)
    panels = build_panels()

    # ---- harness assertion: run() == engine.backtest with every instrument off
    pxa, tra = panels["U56"]
    Wa = ewall_base(pxa, tra)
    sl0 = pxa.index[260]
    ra = run(pxa, Wa, m=1.0, ddctl=False, bps=10.0)["r"].loc[sl0:]
    rb = backtest(pxa, Wa, cost_bps=10.0, freq=FREQ)["returns"].loc[sl0:]
    P(f"\nharness check  max|run - engine.backtest| on the evaluated slice = "
      f"{float((ra - rb).abs().max()):.3e}  (must be ~0)")
    assert float((ra - rb).abs().max()) < 1e-12

    rows, wf_rows, oos_rows = [], [], []
    for pname, (px, trad) in panels.items():
        start = px.index[260]
        full = (start, px.index[-1])
        is_w = (start, pd.Timestamp(IS_END))
        oos_w = (pd.Timestamp(OOS_START), px.index[-1])
        spy = px["SPY"].pct_change().fillna(0.0)
        Wtg = {a: arm_targets(px, trad, a) for a in ARMS}
        # live RULES v2 book on this panel, and SPY, as the two KEEP references
        for bps in COSTS:
            v2 = backtest(px, rules_v2_weights(px), cost_bps=bps, freq=FREQ)["returns"]
            ref = {}
            for wn, w in (("full", full), ("IS", is_w), ("OOS", oos_w)):
                ref[("v2", wn)] = mm(v2.loc[w[0]:w[1]])
                ref[("SPY", wn)] = mm(spy.loc[w[0]:w[1]])
            P("\n" + "=" * 118)
            P(f"PANEL {pname}   cost {bps:.0f} bps   sample {start.date()} -> {px.index[-1].date()}")
            P(f"  reference  RULES v2 (live book on this panel) full {ref[('v2','full')]['CAGR']:.2%} / "
              f"{ref[('v2','full')]['Sharpe']:.4f} / {ref[('v2','full')]['MaxDD']:.2%}   "
              f"SPY {ref[('SPY','full')]['CAGR']:.2%} / {ref[('SPY','full')]['Sharpe']:.4f} / "
              f"{ref[('SPY','full')]['MaxDD']:.2%}")

            for G in GROSS_TARGETS:
                cell = {}
                for wn, w in (("full", full), ("IS", is_w)):
                    fits = {}
                    for a in ARMS:
                        m, g, res, hist = fit_m(px, Wtg[a], a == "ddctl8", bps, w, G)
                        fits[a] = (m, g, res)
                    ctl_w = mm(fits["static"][2]["r"].loc[w[0]:w[1]])
                    for a in ARMS:
                        m, g, res = fits[a]
                        am = mm(res["r"].loc[w[0]:w[1]])
                        cost, bought, price, yld = price_of(am, ctl_w)
                        yrs = len(res["r"].loc[w[0]:w[1]]) / 252
                        rec = dict(panel=pname, bps=bps, G=G, window=wn, arm=a, m=round(m, 4),
                                   realised_gross=round(g, 4), CAGR=am["CAGR"], Sharpe=am["Sharpe"],
                                   MaxDD=am["MaxDD"], H1=am["H1"], H2=am["H2"],
                                   turnover=res["to"].loc[w[0]:w[1]].sum() / yrs,
                                   cost_pp=cost, dd_bought_pp=bought, price=price, yield_=yld,
                                   matched=bool(abs(g - G) <= MATCH_TOL))
                        # KEEP paths, both, on the same window
                        sp, v2r = ref[("SPY", wn)], ref[("v2", wn)]
                        rec["p4a"] = bool(am["H1"] > v2r["H1"] and am["H2"] > v2r["H2"]
                                          and abs(am["MaxDD"]) <= abs(v2r["MaxDD"]))
                        rec["p4b_halves"] = bool(am["H1"] > sp["H1"] and am["H2"] > sp["H2"])
                        rec["p4b_dd"] = bool(abs(am["MaxDD"]) <= 0.60 * abs(sp["MaxDD"]))
                        rec["p4b_cagr"] = bool(am["CAGR"] >= 0.70 * sp["CAGR"])
                        rows.append(rec)
                        if wn == "IS":
                            cell[a] = (m, res)
                    if wn == "full":
                        df = pd.DataFrame([r for r in rows if r["panel"] == pname and r["bps"] == bps
                                           and r["G"] == G and r["window"] == "full"])
                        P(f"\n  G={G:.2f}  FULL SAMPLE, matched realised gross")
                        P(df[["arm", "realised_gross", "m", "matched", "CAGR", "Sharpe", "MaxDD",
                              "H1", "H2", "turnover", "cost_pp", "dd_bought_pp", "price", "yield_",
                              "p4a", "p4b_halves", "p4b_dd", "p4b_cagr"]]
                          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
                        if not df.matched.all():
                            P("        UNMATCHED (cannot reach this gross even at m=1.0, so NOT "
                              "priced): " + ", ".join(df.loc[~df.matched, "arm"]))

                # ---- rule 8: m fitted on IS, arm chosen on IS, evaluated untouched OOS
                oos = {}
                for a in ARMS:
                    m, res = cell[a]
                    oos[a] = mm(res["r"].loc[oos_w[0]:oos_w[1]])
                ctl_o = oos["static"]
                is_tbl = {r["arm"]: r for r in rows if r["panel"] == pname and r["bps"] == bps
                          and r["G"] == G and r["window"] == "IS"}
                spo, v2o = ref[("SPY", "OOS")], ref[("v2", "OOS")]
                for a in ARMS:                      # OOS KEEP-path legs for EVERY arm, not
                    o = oos[a]                      # only the rule-8 pick
                    oos_rows.append(dict(
                        panel=pname, bps=bps, G=G, arm=a, m=cell[a][0],
                        matched=is_tbl[a]["matched"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"],
                        OOS_MaxDD=o["MaxDD"], spy_OOS_Sharpe=spo["Sharpe"], spy_OOS_CAGR=spo["CAGR"],
                        spy_OOS_MaxDD=spo["MaxDD"], v2_OOS_Sharpe=v2o["Sharpe"], v2_OOS_MaxDD=v2o["MaxDD"],
                        oos4b_sharpe=bool(o["Sharpe"] > spo["Sharpe"]),
                        oos4b_dd=bool(abs(o["MaxDD"]) <= 0.60 * abs(spo["MaxDD"])),
                        oos4b_cagr=bool(o["CAGR"] >= 0.70 * spo["CAGR"]),
                        oos4a=bool(o["Sharpe"] > v2o["Sharpe"] and abs(o["MaxDD"]) <= abs(v2o["MaxDD"]))))
                oprice, oyield, obought = {}, {}, {}
                for a in ARMS:
                    c, b, pr, y = price_of(oos[a], ctl_o)
                    oprice[a], oyield[a], obought[a] = pr, y, b
                elig = [a for a in ARMS if a != "static" and is_tbl[a]["matched"]
                        and is_tbl[a]["dd_bought_pp"] >= 1.0 and np.isfinite(is_tbl[a]["price"])]
                pick = min(elig, key=lambda a: is_tbl[a]["price"]) if elig else None
                treated = [a for a in ARMS if a != "static" and is_tbl[a]["matched"]]
                order = sorted([a for a in treated if np.isfinite(oprice[a])], key=lambda a: oprice[a])
                rho = spearman([is_tbl[a]["price"] for a in treated], [oprice[a] for a in treated])
                wf_rows.append(dict(panel=pname, bps=bps, G=G, pick=pick or "none",
                                    is_price=is_tbl[pick]["price"] if pick else np.nan,
                                    oos_price=oprice.get(pick, np.nan),
                                    oos_yield=oyield.get(pick, np.nan),
                                    oos_rank=(order.index(pick) + 1) if pick in order else np.nan,
                                    n_ranked=len(order),
                                    oos_cheapest=order[0] if order else "none",
                                    band3_oos_rank=(order.index("band3") + 1) if "band3" in order else np.nan,
                                    rho_is_oos=rho,
                                    oos_CAGR=oos[pick]["CAGR"] if pick else np.nan,
                                    oos_Sharpe=oos[pick]["Sharpe"] if pick else np.nan,
                                    oos_MaxDD=oos[pick]["MaxDD"] if pick else np.nan,
                                    ctl_oos_CAGR=ctl_o["CAGR"], ctl_oos_Sharpe=ctl_o["Sharpe"],
                                    ctl_oos_MaxDD=ctl_o["MaxDD"],
                                    v2_oos_Sharpe=ref[("v2", "OOS")]["Sharpe"],
                                    v2_oos_MaxDD=ref[("v2", "OOS")]["MaxDD"],
                                    spy_oos_CAGR=ref[("SPY", "OOS")]["CAGR"],
                                    spy_oos_Sharpe=ref[("SPY", "OOS")]["Sharpe"],
                                    spy_oos_MaxDD=ref[("SPY", "OOS")]["MaxDD"],
                                    band3_oos_Sharpe=oos["band3"]["Sharpe"],
                                    band3_oos_MaxDD=oos["band3"]["MaxDD"],
                                    band3_oos_CAGR=oos["band3"]["CAGR"]))
                P(f"\n  G={G:.2f}  rule 8: IS pick = {pick}  (IS price "
                  f"{is_tbl[pick]['price']:.3f})" if pick else f"\n  G={G:.2f}  rule 8: no eligible IS arm")
                P("        OOS price order: " + ", ".join(f"{a}={oprice[a]:.3f}" for a in order)
                  + (f"   | Spearman(IS,OOS price) = {rho:+.3f}" if np.isfinite(rho) else ""))

    grid = pd.DataFrame(rows)
    wf = pd.DataFrame(wf_rows)
    oosdf = pd.DataFrame(oos_rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)
    oosdf.to_csv(f"{STEM}.oos.csv", index=False)

    # ------------------------------------------------------------- summary
    P("\n" + "=" * 118)
    P("SUMMARY 1 — full-sample price (pp CAGR per pp MaxDD bought) at matched realised gross; lower = cheaper")
    P("           (UNMATCHED cells — arm cannot reach that gross at m=1.0 — are blanked, never priced)")
    P("=" * 118)
    f = grid[grid.window == "full"].copy()
    P(f"  unmatched full-sample cells: {int((~f.matched).sum())} of {len(f)}  "
      + ", ".join(f"{p}/{a}" for p, a in f.loc[~f.matched, ["panel", "arm"]].drop_duplicates().values))
    f.loc[~f.matched, ["price", "yield_", "dd_bought_pp", "cost_pp"]] = np.nan
    for bps in COSTS:
        piv = f[f.bps == bps].pivot_table(index=["panel", "G"], columns="arm", values="price")
        P(f"\n  cost {bps:.0f} bps")
        tre0 = [a for a in ARMS if a != "static" and a in piv.columns]
        P(piv[tre0].to_string(float_format=lambda x: f"{x:7.3f}"))
        best = argmin_rows(piv[tre0])
        P("  cheapest arm per cell: " + ", ".join(f"{i[0]}/G{i[1]:.2f}={best.loc[i]}" for i in piv.index))

    P("\n" + "=" * 118)
    P("SUMMARY 2 — pp of MaxDD bought (negative = the arm ADDS drawdown at matched gross)")
    P("=" * 118)
    for bps in COSTS:
        piv = f[f.bps == bps].pivot_table(index=["panel", "G"], columns="arm", values="dd_bought_pp")
        P(f"\n  cost {bps:.0f} bps")
        P(piv[[a for a in ARMS if a != "static"]].to_string(float_format=lambda x: f"{x:7.2f}"))

    P("\n" + "=" * 118)
    P("SUMMARY 3 — rank of each arm by full-sample price within each panel x cost x G cell (1 = cheapest)")
    P("=" * 118)
    tre = [a for a in ARMS if a != "static"]
    rk = (f[f.arm != "static"].pivot_table(index=["panel", "bps", "G"], columns="arm", values="price")
          .rank(axis=1))
    P(rk[tre].to_string(float_format=lambda x: f"{x:4.1f}"))
    P("\n  mean rank by arm (over all panel x cost x G cells, NaN = price undefined there):")
    P("   " + "  ".join(f"{a}={rk[a].mean():.2f}(n={int(rk[a].notna().sum())})" for a in tre))
    cheap = argmin_rows(rk[tre])
    P(f"\n  cells where band3 is strictly cheapest: {int((cheap == 'band3').sum())} of {len(rk)}   by panel: "
      + ", ".join(f"{p}={int((cheap.loc[p] == 'band3').sum())}/{len(cheap.loc[p])}"
                  for p in cheap.index.get_level_values(0).unique()))
    P("  cheapest arm per cell:\n" + cheap.to_string())

    P("\n" + "=" * 118)
    P("SUMMARY 4 — rule 8 walk-forward (m and arm chosen on IS, evaluated untouched OOS)")
    P("=" * 118)
    P(wf[["panel", "bps", "G", "pick", "is_price", "oos_price", "oos_yield", "oos_rank", "n_ranked",
          "oos_cheapest", "band3_oos_rank", "rho_is_oos"]].to_string(index=False,
                                                                     float_format=lambda x: f"{x:.3f}"))
    P(f"\n  IS pick == OOS cheapest in {int((wf['pick'] == wf['oos_cheapest']).sum())} of {len(wf)} cells")
    P(f"  mean Spearman(IS price, OOS price) = {wf.rho_is_oos.mean():+.3f} "
      f"(positive in {int((wf.rho_is_oos > 0).sum())} of {int(wf.rho_is_oos.notna().sum())} cells)")
    P(f"  band3 is the IS pick in {int((wf['pick'] == 'band3').sum())} of {len(wf)} cells; "
      f"the OOS cheapest in {int((wf['oos_cheapest'] == 'band3').sum())}")

    P("\n" + "=" * 118)
    P("SUMMARY 5 — OOS levels of the rule-8 pick vs the matched-gross control, live RULES v2 and SPY")
    P("=" * 118)
    P(wf[["panel", "bps", "G", "pick", "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "ctl_oos_CAGR",
          "ctl_oos_Sharpe", "ctl_oos_MaxDD", "band3_oos_CAGR", "band3_oos_Sharpe", "band3_oos_MaxDD",
          "v2_oos_Sharpe", "v2_oos_MaxDD", "spy_oos_CAGR", "spy_oos_Sharpe", "spy_oos_MaxDD"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 118)
    P("SUMMARY 6 — KEEP paths, full sample, all arms (a cell passes 4b only with halves AND dd AND cagr)")
    P("=" * 118)
    f2 = f.copy()
    f2["p4b"] = f2.p4b_halves & f2.p4b_dd & f2.p4b_cagr
    P(f"  4a passes: {int(f2.p4a.sum())} of {len(f2)} full-sample arm-cells")
    P(f"  4b passes: {int(f2.p4b.sum())} of {len(f2)} full-sample arm-cells")
    if f2.p4b.any():
        P(f2[f2.p4b][["panel", "bps", "G", "arm", "realised_gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if f2.p4a.any():
        P("\n  4a passes:")
        P(f2[f2.p4a][["panel", "bps", "G", "arm", "realised_gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n" + "=" * 118)
    P("SUMMARY 7 — the ONLY admissible KEEP reading: full-sample 4b bars AND the rule-8 OOS bars")
    P("           (OOS numbers use the IS-fitted m, so nothing here is chosen on the OOS window)")
    P("=" * 118)
    j = f2.merge(oosdf, on=["panel", "bps", "G", "arm"], suffixes=("", "_o"))
    j["oos4b"] = j.oos4b_sharpe & j.oos4b_dd & j.oos4b_cagr
    j["KEEP4b"] = j.p4b & j.oos4b
    j["KEEP4a"] = j.p4a & j.oos4a
    P(f"  full-sample 4b passes: {int(j.p4b.sum())};  of those, also passing the OOS 4b bars: "
      f"{int(j.KEEP4b.sum())} of {len(j)} cells")
    P(f"  full-sample 4a passes: {int(j.p4a.sum())};  of those, also passing the OOS 4a bars: "
      f"{int(j.KEEP4a.sum())}")
    cols = ["panel", "bps", "G", "arm", "realised_gross", "matched", "CAGR", "Sharpe", "MaxDD",
            "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "spy_OOS_Sharpe", "spy_OOS_CAGR",
            "spy_OOS_MaxDD", "turnover"]
    if j.KEEP4b.any():
        P("\n  4b KEEP-candidates (full sample AND out of sample):")
        P(j[j.KEEP4b][cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if j.KEEP4a.any():
        P("\n  4a KEEP-candidates (full sample AND out of sample):")
        P(j[j.KEEP4a][cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  every full-sample 4b pass with its OOS legs (pass or fail), for the record:")
    P(j[j.p4b][cols + ["oos4b_sharpe", "oos4b_dd", "oos4b_cagr"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    j.to_csv(f"{STEM}.keep.csv", index=False)

    P("\n  bar failure counts among 4b near-misses (full sample, treated arms only):")
    t2 = f2[f2.arm != "static"]
    P(f"    halves fail {int((~t2.p4b_halves).sum())}, dd fail {int((~t2.p4b_dd).sum())}, "
      f"cagr fail {int((~t2.p4b_cagr).sum())} of {len(t2)}")

    (Path(f"{STEM}.console.txt")).write_text("\n".join(_LOG) + "\n")
    P(f"\nwrote {STEM.name}.grid.csv / .walkforward.csv / .console.txt")
    (Path(f"{STEM}.console.txt")).write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
