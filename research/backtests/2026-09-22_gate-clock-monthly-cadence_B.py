#!/usr/bin/env python3
"""IDEA 2276 (lane B, 2026-09-22) -- does the GATE CLOCK matter at the MONTHLY cadence too?

THE DEFECT THIS PRICES.  Idea 182's R6 top-20 book -- the record's standing monthly 4b
candidate -- trades MONTHLY (freq='M') but gates on DAILY bars: its eligibility clause is
`px > px.rolling(200).mean()`, recomputed every session.  The gate is therefore SAMPLED
TWENTY-ONE TIMES FINER THAN IT IS EVER EXECUTED.  Idea 2284 priced exactly this mismatch at
the WEEKLY cadence on the RULES v2 band book and KILLED it (4b 0 of 240, 4a 1 of 240 and only
at 50 bps); idea 2280 then showed independently that the contrast is NOT a turnover rebate --
it is genuinely negative information (INFO_Sharpe < 0 at 180 of 200 cells).

THE QUESTION 2276 ASKS IS THE ONE NEITHER OF THOSE ANSWERED: both of them moved the gate clock
at the FAST trading clock.  If a coarser gate is worth anything, it should be worth MORE at the
SLOW trading clock, where the stale-state window is four times longer -- a name that crosses
the 200d line inside a month is held (or not held) for up to 21 sessions on a state the book
never re-reads.  So the premise is tested DIRECTLY and same-tape: the SAME gate-clock ladder is
priced at BOTH trading cadences, M (this book's live cadence) and W (the 2284 contrast), on the
same panels with the same warm-up, and the M-minus-W difference of the clock contrast IS the
answer to 2276.

WHY IT IS NOT ANOTHER SIZING DIAL.  The CHANGELOG diagnosis is that every device priced against
the binding 4b CAGR floor -- gross, leverage, re-spread, concentration, vol-targeting, stops,
the idle-NAV sleeve -- slides along ONE Sharpe ray, buying CAGR with drawdown roughly one for
one, because every one of them is a SIZING dial.  GROSS IS FIXED AT 0.75 throughout and never
appears as a parameter.  A gate-clock change alters WHICH DAYS are held, at unchanged gross.

TWO TUNED PARAMETERS AND NO MORE, every grid point reported:
  TUNED 1  L, the moving-average length in MONTHLY BARS: {5, 7, 10, 13, 16}.
           L = 10 months (~210 sessions) is the nearest monthly analogue of the live 200 days.
  TUNED 2  c, the band half-width: {0.00, 0.02, 0.03, 0.05, 0.08}.  c = 0.00 is the LIVE
           setting of idea 182's gate (a bare above/below test, no hysteresis).
  => 25 monthly-clock cells per (panel, cadence), plus a 5-cell DAILY-200d control ladder.

REPORTED, NEVER SELECTED ON: panel (U56 = research/universe.json, B136 = universe_broad.json),
TRADING CADENCE {M (live for this book), W}, cost rung {0, 10, 25, 50} bps (headline 10), window
{FULL, H1, H2, IS <= 2016-12-31, OOS >= 2017-01-01}, and the frozen body of idea 182's
hypothesis: signal R6 (126d total return), vol scaler 1/vol20**0.5, the vol20 < 0.60 ceiling,
top n = 20 equal weight, gross 0.75.  ONLY the MA gate's SAMPLING CLOCK moves.  Execution t+1
(engine convention), costs linear in realised turnover.

BOTH KEEP PATHS at every grid point -- 4a against the live RULES v2 book, 4b against SPY -- and
PROTOCOL rule 8: dials chosen on 2009-2016 alone, 2017-2026 read exactly once.

SURVIVORSHIP (rule 9), STATED NOT REPAIRED: U56 and B136 are CURRENT-CONSTITUENT lists held
from 2008, so every absolute CAGR level is optimistic and both 4b bars are easier than they
would be on a point-in-time panel.  The monthly-vs-daily CLOCK CONTRAST is same-tape, same-names
and first-order immune to that; the pass COUNTS are not.

Deterministic, offline, no network.  Outputs .grid.csv / .walkforward.csv / .gates.csv /
.console.txt beside this file.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                      # noqa: E402
from engine import backtest, metrics, rebalance_mask                      # noqa: E402

STEM = Path(__file__).with_suffix("")

# ---- frozen body of idea 182's hypothesis (NOT dials in this run) ----------------
GROSS, NTOP, MAXVOL, PSCALE, RLOOK = 0.75, 20, 0.60, 0.5, 126
# ---- the two tuned dials ---------------------------------------------------------
L_MONTHS = [5, 7, 10, 13, 16]
BANDS    = [0.00, 0.02, 0.03, 0.05, 0.08]
# ---- reported, never selected on -------------------------------------------------
CADENCES = ["M", "W"]
COSTS    = [0, 10, 25, 50]
HEADLINE = 10
PANELS   = ["U56", "B136"]
IS_END   = pd.Timestamp("2016-12-31")
WARMUP   = 380          # >= 16 monthly bars AND >= 252 daily bars, common to every book here
ANCHOR_WARMUP = 260     # idea 182's own convention, used only by the replication gate
ANCHOR_END = pd.Timestamp("2026-09-04")   # idea 182's own last session (its tape, not ours)

OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.append(s)


# ============================================================== gate clocks
def _hysteresis(p, ma, c):
    """IN above ma*(1+c), OUT below ma*(1-c), previous state in between, OUT before the MA
    exists.  At c = 0 this degenerates to the bare `p > ma` test, which is idea 182's gate."""
    raw = pd.DataFrame(np.nan, index=p.index, columns=p.columns)
    raw = raw.mask(p > ma * (1 + c), 1.0).mask(p < ma * (1 - c), 0.0)
    return raw.ffill().fillna(0.0)


def monthly_bars(px):
    """Last close of each calendar month, INDEXED BY THAT MONTH'S REAL LAST TRADING DAY."""
    key = px.index.to_period("M")
    pm = px.groupby(key).last()
    ends = pd.Series(px.index, index=px.index).groupby(key).last()
    pm.index = pd.DatetimeIndex(ends.values)
    return pm


def state_monthly(px, L, c):
    """The MA gate with the average and the band computed on MONTHLY BARS.  The state set at a
    month's last close is carried through the following month (decided at t, filled t+1)."""
    pm = monthly_bars(px)
    st = _hysteresis(pm, pm.rolling(L).mean(), c)
    return st.reindex(px.index).ffill().fillna(0.0) > 0.5


def state_daily(px, c, n=200):
    """The LIVE gate: n-day MA on DAILY closes.  c = 0.00 is idea 182's literal clause."""
    return _hysteresis(px, px.rolling(n).mean(), c) > 0.5


# ============================================================== the book
def components(px):
    """Idea 182's frozen signal and vol pieces.  The `above` gate is supplied separately."""
    r6 = px / px.shift(RLOOK) - 1
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return r6, vol20


def hyp_weights(r6, vol20, gate):
    """Idea 182's weights(): literal top-n equal weight at gross g among eligible names,
    with `gate` standing in for the shipped above-200dma clause."""
    s = r6 / vol20.clip(lower=0.08) ** PSCALE
    elig = s.where(gate & (vol20 < MAXVOL))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= NTOP).astype(float) * (GROSS / NTOP)


# ============================================================== simulator
def sim_fast(rets, w, mask):
    """Exact numpy restatement of engine.backtest's loop (gate G0 proves it, at 0.0).
    Returns COST-FREE returns and the realised turnover series; cost rungs are applied
    afterwards by the linear turnover identity (gate G5)."""
    n, k = rets.shape
    cur = np.zeros(k)
    held = np.empty((n, k))
    trn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = w[i]
            trn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (held * rets).sum(axis=1), trn


def run_book(px, W, freq, start):
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    w = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    r, t = sim_fast(rets, w, mask)
    r = pd.Series(r, index=idx).loc[start:]
    t = pd.Series(t, index=idx).loc[start:]
    return dict(gross=r, turn=t, ann_turn=t.sum() / (len(r) / 252))


def net(gross_ret, turn, bps):
    return gross_ret - turn * bps / 1e4


# ============================================================== scoring
def win(r, tag):
    if tag == "FULL": return r
    if tag == "H1":   return r.iloc[: len(r) // 2]
    if tag == "H2":   return r.iloc[len(r) // 2:]
    if tag == "IS":   return r.loc[:IS_END]
    if tag == "OOS":  return r.loc[IS_END + pd.Timedelta(days=1):]
    raise ValueError(tag)


TAGS = ("FULL", "H1", "H2", "IS", "OOS")


def legs(r, spy_m, tag):
    m = metrics(r)
    s = spy_m[tag]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                L_SH=bool(m["Sharpe"] > s["Sharpe"]),
                L_DD=bool(m["MaxDD"] >= 0.60 * s["MaxDD"]),        # MaxDD is negative
                L_CAGR=bool(m["CAGR"] >= 0.70 * s["CAGR"]))


# ============================================================== main
def main():
    t0 = time.time()
    gates, grid, wf = [], [], []

    for panel in PANELS:
        px = load_universe() if panel == "U56" else load_universe(broad=True)
        start = px.index[WARMUP]
        log(f"\n{'='*112}\nPANEL {panel}: {px.shape[1]} names, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, scored from {start.date()} (common {WARMUP}-row warm-up)")
        r6, vol20 = components(px)

        # ---------------------------------------------------------- GATES
        # G0  the numpy simulator IS engine.backtest
        w_probe = hyp_weights(r6, vol20, state_daily(px, 0.00))
        for f in ("M", "W"):
            e = backtest(px, w_probe, cost_bps=0.0, freq=f)
            bk = run_book(px, w_probe, f, px.index[0])
            g0r = float((bk["gross"] - e["returns"]).abs().max())
            g0t = float((bk["turn"] - e["turnover"]).abs().max())
            gates.append(dict(panel=panel, gate=f"G0 sim_fast == engine.backtest (freq={f}), max|dret|+|dturn|",
                              value=f"{g0r:.3e} / {g0t:.3e}", ok=(g0r < 1e-12 and g0t < 1e-12)))

        # G1  the DAILY c=0.00 control IS idea 182's literal clause -> replay its published
        #     13.61% / 1.1557 / -18.81% (FULL) and 14.56% / 1.1695 (OOS) at its OWN warm-up
        #     (px.index[260]) ON ITS OWN TAPE.  The committed cache has grown 9 sessions since
        #     2026-09-06 (182's sample ended 2026-09-04, this one ends 2026-09-18), so the tape
        #     is truncated to 182's last session for the EXACT replay; G1b then publishes the
        #     same book on the CURRENT tape so the drift the 9 extra sessions cause is on the
        #     record rather than hidden inside a tolerance.
        if panel == "U56":
            pxa = px.loc[:ANCHOR_END]
            a = run_book(pxa, hyp_weights(*components(pxa), state_daily(pxa, 0.00)), "M",
                         pxa.index[ANCHOR_WARMUP])
            ar = net(a["gross"], a["turn"], 10)
            mf, mo = metrics(ar), metrics(win(ar, "OOS"))
            ok = (abs(mf["CAGR"] - 0.1361) < 5e-4 and abs(mf["Sharpe"] - 1.1557) < 5e-4
                  and abs(mf["MaxDD"] + 0.1881) < 5e-4 and abs(mo["CAGR"] - 0.1456) < 5e-4
                  and abs(mo["Sharpe"] - 1.1695) < 5e-4)
            gates.append(dict(panel=panel,
                              gate=f"G1 DAILY c=0 control == idea 182's published anchor @10bps (tape cut at {ANCHOR_END.date()})",
                              value=f"{mf['CAGR']:.4%} / {mf['Sharpe']:.4f} / {mf['MaxDD']:.4%} | OOS {mo['CAGR']:.4%} / {mo['Sharpe']:.4f}"
                                    f"  [published 13.61% / 1.1557 / -18.81% | 14.56% / 1.1695]",
                              ok=bool(ok)))
            b = run_book(px, w_probe, "M", px.index[ANCHOR_WARMUP])
            br = net(b["gross"], b["turn"], 10)
            nf, no = metrics(br), metrics(win(br, "OOS"))
            gates.append(dict(panel=panel,
                              gate="G1b same book on the CURRENT tape (9 sessions longer) -- drift published, not hidden",
                              value=f"{nf['CAGR']:.4%} / {nf['Sharpe']:.4f} / {nf['MaxDD']:.4%} | OOS {no['CAGR']:.4%} / {no['Sharpe']:.4f}"
                                    f"  [dCAGR {nf['CAGR']-mf['CAGR']:+.4%}, dSharpe {nf['Sharpe']-mf['Sharpe']:+.4f}]",
                              ok=(abs(nf["Sharpe"] - mf["Sharpe"]) < 5e-3)))

        # G2  monthly bar ends ARE engine.rebalance_mask(idx,'M')
        me = monthly_bars(px).index
        mt = px.index[rebalance_mask(px.index, "M").values]
        g2 = int(len(set(me) ^ set(mt)))
        gates.append(dict(panel=panel, gate="G2 monthly bar ends == engine.rebalance_mask('M')",
                          value=g2, ok=g2 == 0))

        # G3a  no look-ahead: at a month-end the state equals the state recomputed from a tape
        #      TRUNCATED at that same date.  (Truncating MID-month is not a valid test: the
        #      partial month becomes a complete bar, making the truncated state MORE current.)
        stm = state_monthly(px, 10, 0.03)
        g3a = 0.0
        for d in me[[50, 90, 130, 170]]:
            tr = state_monthly(px.loc[:d], 10, 0.03).iloc[-1]
            g3a = max(g3a, float((tr.astype(float) - stm.loc[d].astype(float)).abs().max()))
        gates.append(dict(panel=panel, gate="G3a monthly state at a month-end == truncated-tape state",
                          value=g3a, ok=g3a == 0.0))
        # G3b  the state is CONSTANT between month-ends
        chg = stm.ne(stm.shift()).any(axis=1)
        g3b = int(chg.loc[~stm.index.isin(me)].iloc[1:].sum())
        gates.append(dict(panel=panel, gate="G3b state changes only on month-end rows",
                          value=g3b, ok=g3b == 0))

        # ---------------------------------------------------------- baseline + SPY
        w_live = rules_v2_weights(px, 0.03, GROSS)
        base = run_book(px, w_live, "W", start)
        chk = backtest(px, w_live, cost_bps=25, freq="W")["returns"].loc[start:]
        g5 = float((net(base["gross"], base["turn"], 25) - chk).abs().max())
        gates.append(dict(panel=panel, gate="G5 cost reconstruction == engine.backtest(25bps)",
                          value=f"{g5:.3e}", ok=g5 < 1e-12))

        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        nIS, nOOS = len(win(spy, "IS")), len(win(spy, "OOS"))
        gates.append(dict(panel=panel, gate="G6 IS + OOS == total sessions (exact partition)",
                          value=f"{nIS} + {nOOS} = {nIS + nOOS} vs {len(spy)}", ok=nIS + nOOS == len(spy)))

        spy_m = {t: metrics(win(spy, t)) for t in TAGS}
        base_m = {b: {t: metrics(win(net(base["gross"], base["turn"], b), t)) for t in TAGS} for b in COSTS}
        bm = base_m[HEADLINE]
        log(f"  SPY        FULL {spy_m['FULL']['CAGR']:7.2%} / {spy_m['FULL']['Sharpe']:.4f} / {spy_m['FULL']['MaxDD']:7.2%}"
            f"  (H1 {spy_m['H1']['Sharpe']:.4f} H2 {spy_m['H2']['Sharpe']:.4f})"
            f"  IS {spy_m['IS']['Sharpe']:.4f}  OOS {spy_m['OOS']['CAGR']:7.2%} / {spy_m['OOS']['Sharpe']:.4f} / {spy_m['OOS']['MaxDD']:7.2%}")
        log(f"  LIVE v2    FULL {bm['FULL']['CAGR']:7.2%} / {bm['FULL']['Sharpe']:.4f} / {bm['FULL']['MaxDD']:7.2%}"
            f"  (H1 {bm['H1']['Sharpe']:.4f} H2 {bm['H2']['Sharpe']:.4f})"
            f"  IS {bm['IS']['Sharpe']:.4f}  OOS {bm['OOS']['CAGR']:7.2%} / {bm['OOS']['Sharpe']:.4f} / {bm['OOS']['MaxDD']:7.2%}"
            f"  turnover {base['ann_turn']:.4f}x/yr   [4b floor {0.70*spy_m['FULL']['CAGR']:.2%}, cap {0.60*spy_m['FULL']['MaxDD']:.2%}]")

        # ---------------------------------------------------------- BOOKS
        states = {}
        for c in BANDS:
            states[("DAILY", 200, c)] = state_daily(px, c)
        for L in L_MONTHS:
            for c in BANDS:
                states[("MONTHLY", L, c)] = state_monthly(px, L, c)
        wmats = {k: hyp_weights(r6, vol20, st) for k, st in states.items()}

        for (clock, L, c), W in wmats.items():
            for freq in CADENCES:
                bk = run_book(px, W, freq, start)
                for bps in COSTS:
                    r = net(bk["gross"], bk["turn"], bps)
                    cell = {t: legs(win(r, t), spy_m, t) for t in TAGS}
                    bwin = base_m[bps]
                    p4a = bool(cell["H1"]["Sharpe"] > bwin["H1"]["Sharpe"]
                               and cell["H2"]["Sharpe"] > bwin["H2"]["Sharpe"]
                               and cell["FULL"]["MaxDD"] >= bwin["FULL"]["MaxDD"])
                    p4b = {}
                    for t in ("FULL", "IS", "OOS"):
                        ok = cell[t]["L_SH"] and cell[t]["L_DD"] and cell[t]["L_CAGR"]
                        if t == "FULL":
                            ok = ok and cell["H1"]["L_SH"] and cell["H2"]["L_SH"]
                        p4b[t] = bool(ok)
                    row = dict(panel=panel, clock=clock, L=L, band=c, cadence=freq, bps=bps,
                               ann_turnover=bk["ann_turn"], pass4a=p4a,
                               pass4b_FULL=p4b["FULL"], pass4b_IS=p4b["IS"], pass4b_OOS=p4b["OOS"],
                               base_Sharpe_FULL=bwin["FULL"]["Sharpe"], base_Sharpe_H1=bwin["H1"]["Sharpe"],
                               base_Sharpe_H2=bwin["H2"]["Sharpe"], base_MaxDD_FULL=bwin["FULL"]["MaxDD"],
                               base_CAGR_OOS=bwin["OOS"]["CAGR"], base_Sharpe_OOS=bwin["OOS"]["Sharpe"],
                               base_MaxDD_OOS=bwin["OOS"]["MaxDD"],
                               spy_CAGR_FULL=spy_m["FULL"]["CAGR"], spy_Sharpe_FULL=spy_m["FULL"]["Sharpe"],
                               spy_MaxDD_FULL=spy_m["FULL"]["MaxDD"], spy_CAGR_OOS=spy_m["OOS"]["CAGR"],
                               spy_Sharpe_OOS=spy_m["OOS"]["Sharpe"], spy_MaxDD_OOS=spy_m["OOS"]["MaxDD"])
                    for t in TAGS:
                        row[f"CAGR_{t}"], row[f"Sharpe_{t}"], row[f"MaxDD_{t}"] = \
                            cell[t]["CAGR"], cell[t]["Sharpe"], cell[t]["MaxDD"]
                    for t in ("FULL", "IS", "OOS"):
                        row[f"legSH_{t}"], row[f"legDD_{t}"], row[f"legCAGR_{t}"] = \
                            cell[t]["L_SH"], cell[t]["L_DD"], cell[t]["L_CAGR"]
                    grid.append(row)

        # ---------------------------------------------------------- headline tables
        for freq in CADENCES:
            log(f"\n  ALL {len(BANDS)*(len(L_MONTHS)+1)} GRID POINTS -- panel {panel}, cadence {freq}, "
                f"{HEADLINE} bps   (4a vs live RULES v2, 4b vs SPY)")
            log("  clock    L    c    turn |     FULL CAGR  Sharpe     DD |      OOS CAGR  Sharpe     DD | 4a 4bF 4bI 4bO")
            for (clock, L, c) in sorted(states, key=lambda k: (k[0], k[1], k[2])):
                g = next(x for x in grid if x["panel"] == panel and x["clock"] == clock and x["L"] == L
                         and x["band"] == c and x["cadence"] == freq and x["bps"] == HEADLINE)
                log(f"  {clock:7s} {L:3d} {c:5.2f} {g['ann_turnover']:6.2f} |"
                    f" {g['CAGR_FULL']:9.2%} {g['Sharpe_FULL']:7.4f} {g['MaxDD_FULL']:7.2%} |"
                    f" {g['CAGR_OOS']:9.2%} {g['Sharpe_OOS']:7.4f} {g['MaxDD_OOS']:7.2%} |"
                    f" {'Y' if g['pass4a'] else '.':>2} {'Y' if g['pass4b_FULL'] else '.':>3}"
                    f" {'Y' if g['pass4b_IS'] else '.':>3} {'Y' if g['pass4b_OOS'] else '.':>3}")

        # ---------------------------------------------------------- RULE 8
        for freq in CADENCES:
            for bps in COSTS:
                cells = [x for x in grid if x["panel"] == panel and x["cadence"] == freq
                         and x["bps"] == bps and x["clock"] == "MONTHLY"]
                dctl = [x for x in grid if x["panel"] == panel and x["cadence"] == freq
                        and x["bps"] == bps and x["clock"] == "DAILY"]
                inc = next(x for x in dctl if x["band"] == 0.00)     # idea 182 as shipped
                legal = [x for x in cells if x["pass4b_IS"]]
                picks = {
                    "C_SHARPE  argmax IS Sharpe, MONTHLY clock": max(cells, key=lambda x: x["Sharpe_IS"]),
                    "C_4B      argmax IS Sharpe among IS-4b passers, MONTHLY clock":
                        (max(legal, key=lambda x: x["Sharpe_IS"]) if legal else None),
                    "C_DAILY   argmax IS Sharpe on the DAILY control ladder (band only)":
                        max(dctl, key=lambda x: x["Sharpe_IS"]),
                    "C_LIVE    the shipped gate (DAILY 200d, c=0.00), zero parameters": inc,
                    "C_ORACLE  argmax OOS Sharpe over ALL cells (illegal, upper bound)":
                        max(cells + dctl, key=lambda x: x["Sharpe_OOS"]),
                }
                for nm, ch in picks.items():
                    d = dict(panel=panel, cadence=freq, bps=bps, chooser=nm)
                    if ch is None:
                        d.update(pick=None, note="no cell passes 4b in sample -> undefined")
                    else:
                        d.update(clock=ch["clock"], L=ch["L"], band=ch["band"],
                                 IS_Sharpe=ch["Sharpe_IS"], OOS_CAGR=ch["CAGR_OOS"],
                                 OOS_Sharpe=ch["Sharpe_OOS"], OOS_MaxDD=ch["MaxDD_OOS"],
                                 ann_turnover=ch["ann_turnover"], pass4a=ch["pass4a"],
                                 pass4b_OOS=ch["pass4b_OOS"], pass4b_FULL=ch["pass4b_FULL"],
                                 inc_OOS_Sharpe=inc["Sharpe_OOS"], inc_OOS_CAGR=inc["CAGR_OOS"],
                                 inc_OOS_MaxDD=inc["MaxDD_OOS"],
                                 beats_incumbent_OOS=bool(ch["Sharpe_OOS"] > inc["Sharpe_OOS"]),
                                 live_OOS_Sharpe=ch["base_Sharpe_OOS"], live_OOS_CAGR=ch["base_CAGR_OOS"],
                                 live_OOS_MaxDD=ch["base_MaxDD_OOS"], spy_OOS_Sharpe=ch["spy_Sharpe_OOS"],
                                 spy_OOS_CAGR=ch["spy_CAGR_OOS"], spy_OOS_MaxDD=ch["spy_MaxDD_OOS"])
                    wf.append(d)

        log(f"\n  RULE 8 -- dials chosen on IS (<= {IS_END.date()}) ONLY, 2017-2026 read ONCE   [panel {panel}]")
        for freq in CADENCES:
            for bps in COSTS:
                log(f"   cadence {freq} @{bps:2d}bps:")
                for d in [x for x in wf if x["panel"] == panel and x["cadence"] == freq and x["bps"] == bps]:
                    if d.get("pick", 0) is None:
                        log(f"     {d['chooser']:62s} UNDEFINED ({d['note']})"); continue
                    log(f"     {d['chooser']:62s} -> {d['clock']:7s} L={d['L']:3d} c={d['band']:.2f} "
                        f"| IS Sh {d['IS_Sharpe']:.4f} | OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / "
                        f"{d['OOS_MaxDD']:7.2%} | 4a {'Y' if d['pass4a'] else '.'} 4bOOS "
                        f"{'Y' if d['pass4b_OOS'] else '.'} | beats shipped gate OOS: "
                        f"{'YES' if d['beats_incumbent_OOS'] else 'no'}")

    G, W = pd.DataFrame(grid), pd.DataFrame(wf)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    W.to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(gates).to_csv(f"{STEM}.gates.csv", index=False)

    # ================================================================ summaries
    log(f"\n{'='*112}\nGATES  ({sum(1 for g in gates if g['ok'])} of {len(gates)} pass)")
    for g in gates:
        log(f"  {g['panel']:5s} {g['gate']:68s} {g['value']}  ok={g['ok']}")

    h = G[G.bps == HEADLINE]
    log(f"\n{'='*112}\nTHE QUESTION 2276 ASKS: is the CLOCK CONTRAST BIGGER AT THE SLOW TRADING CLOCK?")
    log("  d = (MONTHLY gate clock) - (DAILY 200d control) at the SAME band c, averaged over the 5 bands.")
    log("  panel  L    | cadence M: dCAGR_F  dSharpe_F   dDD_F  dTurn | cadence W: dCAGR_F  dSharpe_F   dDD_F  dTurn | M-minus-W dSharpe_F  dSharpe_OOS")
    prem = []
    for panel in PANELS:
        for L in L_MONTHS:
            r = {}
            for freq in CADENCES:
                d = h[(h.panel == panel) & (h.cadence == freq) & (h.clock == "DAILY")].set_index("band")
                s = h[(h.panel == panel) & (h.cadence == freq) & (h.clock == "MONTHLY") & (h.L == L)].set_index("band")
                r[freq] = dict(dC=(s.CAGR_FULL - d.CAGR_FULL).mean(), dS=(s.Sharpe_FULL - d.Sharpe_FULL).mean(),
                               dD=(s.MaxDD_FULL - d.MaxDD_FULL).mean(), dT=(s.ann_turnover - d.ann_turnover).mean(),
                               dSo=(s.Sharpe_OOS - d.Sharpe_OOS).mean())
            log(f"  {panel:5s} {L:3d}  |            {r['M']['dC']:+7.2%}   {r['M']['dS']:+8.4f} {r['M']['dD']:+7.2%} {r['M']['dT']:+6.2f}x"
                f" |            {r['W']['dC']:+7.2%}   {r['W']['dS']:+8.4f} {r['W']['dD']:+7.2%} {r['W']['dT']:+6.2f}x"
                f" |            {r['M']['dS'] - r['W']['dS']:+8.4f}     {r['M']['dSo'] - r['W']['dSo']:+8.4f}")
            prem.append(dict(panel=panel, L=L, dS_M=r["M"]["dS"], dS_W=r["W"]["dS"],
                             dSo_M=r["M"]["dSo"], dSo_W=r["W"]["dSo"]))
    P = pd.DataFrame(prem)
    log(f"\n  PREMISE TEST (2276's own claim: the coarser gate should be worth MORE at cadence M than at W)")
    log(f"    mean dSharpe_FULL  at cadence M {P.dS_M.mean():+.4f}   at cadence W {P.dS_W.mean():+.4f}   M-W {P.dS_M.mean()-P.dS_W.mean():+.4f}")
    log(f"    mean dSharpe_OOS   at cadence M {P.dSo_M.mean():+.4f}   at cadence W {P.dSo_W.mean():+.4f}   M-W {P.dSo_M.mean()-P.dSo_W.mean():+.4f}")
    log(f"    M beats W (dSharpe_FULL) at {int((P.dS_M > P.dS_W).sum())} of {len(P)} (panel, L) rungs; "
        f"OOS at {int((P.dSo_M > P.dSo_W).sum())} of {len(P)}")
    log(f"    the MONTHLY clock beats its own DAILY control at all: dSharpe_FULL > 0 at "
        f"{int((P.dS_M > 0).sum())} of {len(P)} rungs at cadence M, {int((P.dS_W > 0).sum())} of {len(P)} at cadence W")

    log(f"\n{'='*112}\nPASS COUNTS over all {len(G)} published rows "
        f"({len(PANELS)} panels x {len(CADENCES)} cadences x 30 cells x {len(COSTS)} cost rungs)")
    for clock in ("DAILY", "MONTHLY"):
        for freq in CADENCES:
            s = G[(G.clock == clock) & (G.cadence == freq)]
            log(f"  {clock:7s} cadence {freq}  n={len(s):4d} | 4a {int(s.pass4a.sum()):4d} | 4b FULL {int(s.pass4b_FULL.sum()):4d}"
                f"  4b IS {int(s.pass4b_IS.sum()):4d}  4b OOS {int(s.pass4b_OOS.sum()):4d}"
                f"  4b FULL+OOS {int((s.pass4b_FULL & s.pass4b_OOS).sum()):4d}"
                f"  BOTH(4a & 4b FULL & 4b OOS) {int((s.pass4a & s.pass4b_FULL & s.pass4b_OOS).sum()):4d}")
    log(f"  TOTAL                n={len(G):4d} | 4a {int(G.pass4a.sum()):4d} | 4b FULL {int(G.pass4b_FULL.sum()):4d}"
        f"  4b OOS {int(G.pass4b_OOS.sum()):4d}  4b FULL+OOS {int((G.pass4b_FULL & G.pass4b_OOS).sum()):4d}"
        f"  BOTH {int((G.pass4a & G.pass4b_FULL & G.pass4b_OOS).sum()):4d}")

    f = G[~G.pass4b_FULL]
    log(f"\n  BINDING LEG over the {len(f)} 4b-FULL FAILs: "
        f"CAGR-only {int((~f.legCAGR_FULL & f.legDD_FULL & f.legSH_FULL).sum())}, "
        f"DD-only {int((f.legCAGR_FULL & ~f.legDD_FULL & f.legSH_FULL).sum())}, "
        f"Sharpe-only {int((f.legCAGR_FULL & f.legDD_FULL & ~f.legSH_FULL).sum())}, "
        f"joint {int(((~f.legCAGR_FULL).astype(int) + (~f.legDD_FULL).astype(int) + (~f.legSH_FULL).astype(int) > 1).sum())}")

    log("\n  4b FULL+OOS PASSERS (every one, with its clock)")
    pp = G[G.pass4b_FULL & G.pass4b_OOS]
    if len(pp) == 0: log("    none")
    for _, r in pp.iterrows():
        log(f"    {r.panel:5s} {r.clock:7s} L={int(r.L):3d} c={r.band:.2f} {r.cadence} @{int(r.bps):2d}bps  "
            f"FULL {r.CAGR_FULL:.2%} / {r.Sharpe_FULL:.4f} / {r.MaxDD_FULL:.2%} (H1 {r.Sharpe_H1:.4f} H2 {r.Sharpe_H2:.4f})  "
            f"OOS {r.CAGR_OOS:.2%} / {r.Sharpe_OOS:.4f} / {r.MaxDD_OOS:.2%}  turn {r.ann_turnover:.2f}x  4a {r.pass4a}")

    log("\n  4a PASSERS")
    ap = G[G.pass4a]
    if len(ap) == 0: log("    none")
    for _, r in ap.iterrows():
        log(f"    {r.panel:5s} {r.clock:7s} L={int(r.L):3d} c={r.band:.2f} {r.cadence} @{int(r.bps):2d}bps  "
            f"FULL {r.CAGR_FULL:.2%} / {r.Sharpe_FULL:.4f} / {r.MaxDD_FULL:.2%} (H1 {r.Sharpe_H1:.4f} vs "
            f"{r.base_Sharpe_H1:.4f}, H2 {r.Sharpe_H2:.4f} vs {r.base_Sharpe_H2:.4f}, DD vs {r.base_MaxDD_FULL:.2%})  "
            f"OOS {r.CAGR_OOS:.2%} / {r.Sharpe_OOS:.4f} / {r.MaxDD_OOS:.2%}  4b OOS {r.pass4b_OOS}")

    log("\n  NEAREST-ANALOGUE CONTRAST: MONTHLY L=10 (the monthly twin of the live 200d gate) at the LIVE band c=0.00")
    for panel in PANELS:
        for freq in CADENCES:
            for bps in COSTS:
                a = G[(G.panel == panel) & (G.clock == "MONTHLY") & (G.L == 10) & (G.band == 0.00)
                      & (G.cadence == freq) & (G.bps == bps)].iloc[0]
                b = G[(G.panel == panel) & (G.clock == "DAILY") & (G.band == 0.00)
                      & (G.cadence == freq) & (G.bps == bps)].iloc[0]
                log(f"    {panel:5s} {freq} @{bps:2d}bps  dCAGR_F {a.CAGR_FULL-b.CAGR_FULL:+.2%}  "
                    f"dSharpe_F {a.Sharpe_FULL-b.Sharpe_FULL:+.4f}  dMaxDD_F {a.MaxDD_FULL-b.MaxDD_FULL:+.2%}  "
                    f"dSharpe_H1 {a.Sharpe_H1-b.Sharpe_H1:+.4f}  dSharpe_H2 {a.Sharpe_H2-b.Sharpe_H2:+.4f}  "
                    f"dCAGR_OOS {a.CAGR_OOS-b.CAGR_OOS:+.2%}  dSharpe_OOS {a.Sharpe_OOS-b.Sharpe_OOS:+.4f}  "
                    f"dTurn {a.ann_turnover-b.ann_turnover:+.2f}x")

    # ---- does the CLOCK buy a 4b pass, or does it only inherit idea 182's? --------------
    log(f"\n{'='*112}\nMATCHED-PAIR 4b: does the MONTHLY clock pass MORE OFTEN than its OWN daily control?")
    log("  Each MONTHLY cell is paired with the DAILY control at the SAME (panel, cadence, cost, band).")
    pair = []
    for _, r in G[G.clock == "MONTHLY"].iterrows():
        d = G[(G.panel == r.panel) & (G.clock == "DAILY") & (G.cadence == r.cadence)
              & (G.bps == r.bps) & (G.band == r.band)].iloc[0]
        pair.append(dict(panel=r.panel, cadence=r.cadence, bps=r.bps, L=r.L, band=r.band,
                         mo=bool(r.pass4b_FULL and r.pass4b_OOS), da=bool(d.pass4b_FULL and d.pass4b_OOS),
                         dS=r.Sharpe_FULL - d.Sharpe_FULL, dSo=r.Sharpe_OOS - d.Sharpe_OOS,
                         dDD=r.MaxDD_FULL - d.MaxDD_FULL, dC=r.CAGR_FULL - d.CAGR_FULL))
    P2 = pd.DataFrame(pair)
    for cad in CADENCES:
        s = P2[P2.cadence == cad]
        gain = int((s.mo & ~s.da).sum()); loss = int((~s.mo & s.da).sum())
        log(f"  cadence {cad}: monthly-clock 4b FULL+OOS {int(s.mo.sum()):3d}/{len(s)}, its paired daily control "
            f"{int(s.da.sum()):3d}/{len(s)} | clock CREATES a pass {gain:3d}, DESTROYS one {loss:3d} "
            f"| mean dSharpe_FULL {s.dS.mean():+.4f} (>0 at {int((s.dS>0).sum())}/{len(s)}), "
            f"dSharpe_OOS {s.dSo.mean():+.4f} (>0 at {int((s.dSo>0).sum())}/{len(s)}), "
            f"dMaxDD {s.dDD.mean():+.2%} (shallower at {int((s.dDD>0).sum())}/{len(s)})")
    s = P2
    log(f"  POOLED  : creates {int((s.mo & ~s.da).sum())}, destroys {int((~s.mo & s.da).sum())} of {len(s)} pairs; "
        f"mean dSharpe_FULL {s.dS.mean():+.4f}, dSharpe_OOS {s.dSo.mean():+.4f}, dCAGR {s.dC.mean():+.2%}, dMaxDD {s.dDD.mean():+.2%}")
    P2.to_csv(f"{STEM}.pairs.csv", index=False)

    # ---- the ONE thing the clock does buy, and whether rule 8 can reach it ----------------
    log(f"\n{'='*112}\nDRAWDOWN CENSUS: MONTHLY-clock cells that are SHALLOWER than the shipped gate at NO Sharpe cost")
    log("  (same panel, cadence and cost rung; the shipped gate is DAILY 200d c=0.00, idea 182 as it trades)")
    win_cells = []
    for _, r in G[G.clock == "MONTHLY"].iterrows():
        inc = G[(G.panel == r.panel) & (G.clock == "DAILY") & (G.band == 0.00)
                & (G.cadence == r.cadence) & (G.bps == r.bps)].iloc[0]
        if r.MaxDD_FULL > inc.MaxDD_FULL and r.Sharpe_FULL >= inc.Sharpe_FULL:
            win_cells.append(dict(panel=r.panel, cadence=r.cadence, bps=int(r.bps), L=int(r.L), band=r.band,
                                  CAGR=r.CAGR_FULL, Sharpe=r.Sharpe_FULL, MaxDD=r.MaxDD_FULL,
                                  H1=r.Sharpe_H1, H2=r.Sharpe_H2, OOS_CAGR=r.CAGR_OOS,
                                  OOS_Sharpe=r.Sharpe_OOS, OOS_MaxDD=r.MaxDD_OOS, turn=r.ann_turnover,
                                  dDD=r.MaxDD_FULL - inc.MaxDD_FULL, dS=r.Sharpe_FULL - inc.Sharpe_FULL,
                                  dC=r.CAGR_FULL - inc.CAGR_FULL, dSo=r.Sharpe_OOS - inc.Sharpe_OOS,
                                  dDDo=r.MaxDD_OOS - inc.MaxDD_OOS,
                                  p4b=bool(r.pass4b_FULL and r.pass4b_OOS), p4a=bool(r.pass4a)))
    log(f"  {len(win_cells)} of {int((G.clock=='MONTHLY').sum())} monthly-clock cells are shallower at no Sharpe cost.")
    for w in win_cells:
        log(f"    {w['panel']:5s} {w['cadence']} @{w['bps']:2d}bps L={w['L']:3d} c={w['band']:.2f}  "
            f"FULL {w['CAGR']:.2%} / {w['Sharpe']:.4f} / {w['MaxDD']:.2%} (H1 {w['H1']:.4f} H2 {w['H2']:.4f})  "
            f"OOS {w['OOS_CAGR']:.2%} / {w['OOS_Sharpe']:.4f} / {w['OOS_MaxDD']:.2%}  turn {w['turn']:.2f}x  "
            f"| vs shipped dDD {w['dDD']*100:+.2f}pp dSharpe {w['dS']:+.4f} dCAGR {w['dC']*100:+.2f}pp "
            f"dSharpe_OOS {w['dSo']:+.4f} dMaxDD_OOS {w['dDDo']*100:+.2f}pp | 4b {w['p4b']} 4a {w['p4a']}")
    if win_cells:
        pd.DataFrame(win_cells).to_csv(f"{STEM}.ddcells.csv", index=False)
        log("\n  4b MARGINS of the DD-improving cells that actually CLEAR 4b (FULL+OOS), vs the shipped gate")
        for w in sorted([x for x in win_cells if x["p4b"]], key=lambda x: -x["dDD"])[:8]:
            r = G[(G.panel == w["panel"]) & (G.clock == "MONTHLY") & (G.L == w["L"]) & (G.band == w["band"])
                  & (G.cadence == w["cadence"]) & (G.bps == w["bps"])].iloc[0]
            log(f"    {w['panel']:5s} {w['cadence']} @{w['bps']:2d}bps L={w['L']:3d} c={w['band']:.2f}  "
                f"CAGR floor {0.70*r.spy_CAGR_FULL:.2%} -> margin {(r.CAGR_FULL - 0.70*r.spy_CAGR_FULL)*100:+.2f}pp | "
                f"DD cap {0.60*r.spy_MaxDD_FULL:.2%} -> margin {(r.MaxDD_FULL - 0.60*r.spy_MaxDD_FULL)*100:+.2f}pp | "
                f"OOS floor margin {(r.CAGR_OOS - 0.70*r.spy_CAGR_OOS)*100:+.2f}pp, cap margin "
                f"{(r.MaxDD_OOS - 0.60*r.spy_MaxDD_OOS)*100:+.2f}pp | Sharpe vs SPY FULL {r.Sharpe_FULL-r.spy_Sharpe_FULL:+.4f}, "
                f"OOS {r.Sharpe_OOS-r.spy_Sharpe_OOS:+.4f}")
        log("  RULE-8 REACHABILITY of each of those cells (is any legal IS-only chooser picking it?):")
        for w in win_cells:
            hits = [d["chooser"] for d in wf
                    if d["panel"] == w["panel"] and d["cadence"] == w["cadence"] and d["bps"] == w["bps"]
                    and d.get("clock") == "MONTHLY" and d.get("L") == w["L"] and d.get("band") == w["band"]
                    and not d["chooser"].startswith("C_ORACLE")]
            log(f"    {w['panel']:5s} {w['cadence']} @{w['bps']:2d}bps L={w['L']:3d} c={w['band']:.2f}  "
                f"reached by {len(hits)} of 4 legal choosers" + (f": {'; '.join(x.split()[0] for x in hits)}" if hits else ""))

    log("\n  RULE-8 SCOREBOARD over all 16 (panel, cadence, cost) families")
    Wd = W[W.pick.isna() if "pick" in W.columns else W.index >= 0]
    for nm in W.chooser.unique():
        s = W[(W.chooser == nm)]
        d = s.dropna(subset=["OOS_Sharpe"])
        log(f"    {nm:62s} defined {len(d):2d}/{len(s):2d} | mean OOS Sharpe {d.OOS_Sharpe.mean():.4f} "
            f"CAGR {d.OOS_CAGR.mean():7.2%} MaxDD {d.OOS_MaxDD.mean():7.2%} | picks MONTHLY "
            f"{int((d.clock == 'MONTHLY').sum()):2d}/{len(d):2d} | beats shipped gate OOS "
            f"{int(d.beats_incumbent_OOS.sum()):2d}/{len(d):2d} | 4b OOS {int(d.pass4b_OOS.sum()):2d}/{len(d):2d} "
            f"| 4a {int(d.pass4a.sum()):2d}/{len(d):2d}")

    log(f"\nwall clock {time.time()-t0:.1f}s; rows {len(G)}; gates {sum(1 for g in gates if g['ok'])}/{len(gates)}")
    Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
