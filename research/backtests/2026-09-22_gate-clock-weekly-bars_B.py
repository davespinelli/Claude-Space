#!/usr/bin/env python3
"""IDEA 2284 (lane B, 2026-09-22) -- does the GATE CLOCK matter?  Compute RULES v2 clause 2 on
WEEKLY BARS instead of daily closes.

THE DEFECT THIS PRICES.  RULES v2 clause 2 computes the 200-DAY moving average and the +/-3%
hysteresis band on DAILY closes.  Clause 5 trades WEEKLY.  The gate is therefore SAMPLED FOUR
TIMES FINER THAN IT IS EVER EXECUTED: a name can cross the upper edge on Monday and the lower
edge on Wednesday, and the book acts on whichever daily state happens to stand at the Friday
close.  Nothing in this record has ever moved the gate's SAMPLING CLOCK -- a grep of all 1,430
committed backtests finds `resample(` in exactly two files, neither of them a gate.

WHY IT IS NOT ANOTHER SIZING DIAL.  The CHANGELOG diagnosis (2026-09-22 entries for ideas 2221
and 948) is that every device the record has priced against the binding 4b CAGR floor -- gross,
leverage, re-spread, concentration, vol-targeting, the idle-NAV sleeve -- slides along ONE
Sharpe ray, buying CAGR with drawdown roughly one for one, because every one of them is a
SIZING dial.  A gate-clock change is not a sizing dial at all: GROSS IS FIXED AT THE LIVE 0.75
throughout this run and never appears as a parameter.  It changes WHICH DAYS are held.

TWO TUNED PARAMETERS AND NO MORE, every grid point reported:
  TUNED 1  L, the weekly moving-average length in WEEKLY BARS: {20, 30, 40, 50, 60}.
           L = 40 weeks is the nearest weekly analogue of the live 200 trading days.
  TUNED 2  c, the band half-width: {0.00, 0.02, 0.03, 0.05, 0.08} -- the Sunday review's own
           robustness ladder for clause 2.  c = 0.03 is the live value.
  => 25 weekly-clock cells per panel.

REPORTED, NEVER SELECTED ON: panel (U56 = research/universe.json, B136 = universe_broad.json),
cost rung {0, 10, 25, 50} bps (headline 10), window {FULL, H1, H2, IS <=2016-12-31,
OOS >=2017-01-01}, and the DAILY-CLOCK CONTROL (the live clause 2, 200d MA) at each of the same
five band widths.  Cadence is weekly (clause 5), execution t+1 (engine), gross 0.75 (clause 4),
gated-out weight goes to CASH and is never re-spread (clause 4, idea 81).

BOTH KEEP PATHS at every grid point -- 4a against the live RULES v2 book, 4b against SPY -- and
PROTOCOL rule 8: dials chosen on 2009-2016 alone, 2017-2026 read exactly once.

SURVIVORSHIP (rule 9), STATED NOT REPAIRED: U56 and B136 are CURRENT-CONSTITUENT lists held
from 2008, so every absolute CAGR level is optimistic and both 4b bars are easier than they
would be on a point-in-time panel.  The weekly-vs-daily CLOCK CONTRAST is same-tape, same-names
and first-order immune to that; the pass COUNTS are not.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest, metrics, rebalance_mask                       # noqa: E402

STEM = Path(__file__).with_suffix("")
GROSS   = 0.75
L_WEEKS = [20, 30, 40, 50, 60]
BANDS   = [0.00, 0.02, 0.03, 0.05, 0.08]
COSTS   = [0, 10, 25, 50]
HEADLINE = 10
IS_END  = pd.Timestamp("2016-12-31")
WARMUP  = 320            # >= 60 weekly bars for every cell; common to every book in the run
OUT = []

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.append(s)

# ---------------------------------------------------------------- gate clocks
def weekly_bars(px):
    """Last close of each ISO week, INDEXED BY THAT WEEK'S REAL LAST TRADING DAY."""
    key = px.index.to_period("W")
    pw = px.groupby(key).last()
    ends = pd.Series(px.index, index=px.index).groupby(key).last()
    pw.index = pd.DatetimeIndex(ends.values)
    return pw

def _hysteresis(p, ma, c):
    raw = pd.DataFrame(np.nan, index=p.index, columns=p.columns)
    raw = raw.mask(p > ma * (1 + c), 1.0).mask(p < ma * (1 - c), 0.0)
    return raw.ffill().fillna(0.0)

def state_weekly(px, L, c):
    """RULES v2 clause 2 with the MA and the band computed on WEEKLY BARS.  The state set at a
    week's last close is carried through the following week (decided at t, engine applies t+1)."""
    pw = weekly_bars(px)
    st = _hysteresis(pw, pw.rolling(L).mean(), c)
    return st.reindex(px.index).ffill().fillna(0.0) > 0.5

def state_daily(px, c, n=200):
    """The live clause 2: n-day MA on DAILY closes."""
    return _hysteresis(px, px.rolling(n).mean(), c) > 0.5

def wts(px, st):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(st, 0.0)

# ---------------------------------------------------------------- scoring
def win(r, tag):
    if tag == "FULL": return r
    if tag == "H1":   return r.iloc[: len(r) // 2]
    if tag == "H2":   return r.iloc[len(r) // 2:]
    if tag == "IS":   return r.loc[:IS_END]
    if tag == "OOS":  return r.loc[IS_END + pd.Timedelta(days=1):]
    raise ValueError(tag)

def net(gross_ret, turn, bps):
    return gross_ret - turn * bps / 1e4

def run_book(px, w, start):
    """One engine call per book; every cost rung reconstructed exactly from the turnover series."""
    res = backtest(px, w, cost_bps=HEADLINE, freq="W")
    r10, turn = res["returns"].loc[start:], res["turnover"].loc[start:]
    gross_ret = r10 + turn * HEADLINE / 1e4          # exact: costs are linear in bps
    yrs = len(r10) / 252
    return dict(gross=gross_ret, turn=turn, ann_turn=turn.sum() / yrs)

def legs(r, spy_m, base_m, tag):
    """4a (vs live RULES v2) and 4b (vs SPY) legs for one window."""
    m = metrics(r)
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])
    s = spy_m[tag]
    out["L_SH"]   = m["Sharpe"] > s["Sharpe"]
    out["L_DD"]   = m["MaxDD"] >= 0.60 * s["MaxDD"]        # MaxDD is negative
    out["L_CAGR"] = m["CAGR"]  >= 0.70 * s["CAGR"]
    return out

# ---------------------------------------------------------------- main
def main():
    gates, grid, wf = [], [], []
    for panel, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        start = px.index[WARMUP]
        log(f"\n{'='*100}\nPANEL {panel}: {px.shape[1]} names, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, scored from {start.date()} (common {WARMUP}-row warm-up)")

        # ---- GATES -------------------------------------------------------
        w_live = rules_v2_weights(px, 0.03, GROSS)
        g1 = float((wts(px, state_daily(px, 0.03)) - w_live).abs().max().max())
        gates.append(dict(panel=panel, gate="G1 daily-200d control == baseline.rules_v2_weights",
                          value=g1, ok=g1 < 1e-12))

        wk_ends = weekly_bars(px).index
        mask_true = px.index[rebalance_mask(px.index, "W").values]
        g2 = int(len(set(wk_ends) ^ set(mask_true)))
        gates.append(dict(panel=panel, gate="G2 weekly bar ends == engine.rebalance_mask(W)",
                          value=g2, ok=g2 == 0))

        # G3a no look-ahead: at a WEEK-END date the state must equal the state recomputed from a
        # tape TRUNCATED at that same date.  (Truncating MID-week is NOT a valid test: the partial
        # week becomes a complete bar and the truncated state is then MORE current, not future.)
        stw = state_weekly(px, 40, 0.03)
        g3a = 0.0
        for d in wk_ends[[200, 400, 600, 800]]:
            trunc = state_weekly(px.loc[:d], 40, 0.03).iloc[-1]
            g3a = max(g3a, float((trunc.astype(float) - stw.loc[d].astype(float)).abs().max()))
        gates.append(dict(panel=panel, gate="G3a weekly state at a week-end == truncated-tape state",
                          value=g3a, ok=g3a == 0.0))
        # G3b the state is CONSTANT between week-ends, i.e. the daily index carries no information
        # beyond the last completed weekly bar.
        chg = stw.ne(stw.shift()).any(axis=1)
        g3b = int(chg.loc[~stw.index.isin(wk_ends)].iloc[1:].sum())
        gates.append(dict(panel=panel, gate="G3b state changes only on week-end rows (mid-week changes)",
                          value=g3b, ok=g3b == 0))

        base = run_book(px, w_live, start)
        chk = backtest(px, w_live, cost_bps=25, freq="W")["returns"].loc[start:]
        g4 = float((net(base["gross"], base["turn"], 25) - chk).abs().max())
        gates.append(dict(panel=panel, gate="G4 cost reconstruction == engine.backtest(25bps)",
                          value=g4, ok=g4 < 1e-12))

        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_r = net(base["gross"], base["turn"], HEADLINE)
        m_oos = metrics(win(base_r, "OOS"))
        gates.append(dict(panel=panel, gate="G5 live-book OOS vs the committed 7.85%/1.1017/-12.24% (a B136 triple)",
                          value=f"{m_oos['CAGR']:.4%} / {m_oos['Sharpe']:.4f} / {m_oos['MaxDD']:.4%}",
                          ok=(abs(m_oos['CAGR'] - 0.0785) < 5e-4 and abs(m_oos['Sharpe'] - 1.1017) < 5e-4
                              and abs(m_oos['MaxDD'] + 0.1224) < 5e-4)))

        spy_m  = {t: metrics(win(spy, t)) for t in ("FULL", "H1", "H2", "IS", "OOS")}
        base_m = {t: metrics(win(base_r, t)) for t in ("FULL", "H1", "H2", "IS", "OOS")}
        log(f"  SPY   FULL {spy_m['FULL']['CAGR']:7.2%} / {spy_m['FULL']['Sharpe']:.4f} / {spy_m['FULL']['MaxDD']:7.2%}"
            f"   IS {spy_m['IS']['CAGR']:7.2%} / {spy_m['IS']['Sharpe']:.4f} / {spy_m['IS']['MaxDD']:7.2%}"
            f"   OOS {spy_m['OOS']['CAGR']:7.2%} / {spy_m['OOS']['Sharpe']:.4f} / {spy_m['OOS']['MaxDD']:7.2%}")
        log(f"  LIVE  FULL {base_m['FULL']['CAGR']:7.2%} / {base_m['FULL']['Sharpe']:.4f} / {base_m['FULL']['MaxDD']:7.2%}"
            f"   IS {base_m['IS']['CAGR']:7.2%} / {base_m['IS']['Sharpe']:.4f} / {base_m['IS']['MaxDD']:7.2%}"
            f"   OOS {base_m['OOS']['CAGR']:7.2%} / {base_m['OOS']['Sharpe']:.4f} / {base_m['OOS']['MaxDD']:7.2%}"
            f"   turnover {base['ann_turn']:.4f}x/yr")

        # ---- BOOKS -------------------------------------------------------
        books = {}
        for c in BANDS:
            books[("DAILY", 200, c)] = run_book(px, wts(px, state_daily(px, c)), start)
        for L in L_WEEKS:
            for c in BANDS:
                books[("WEEKLY", L, c)] = run_book(px, wts(px, state_weekly(px, L, c)), start)

        for (clock, L, c), bk in books.items():
            for bps in COSTS:
                r = net(bk["gross"], bk["turn"], bps)
                bwin = {t: metrics(win(net(base["gross"], base["turn"], bps), t))
                        for t in ("FULL", "H1", "H2", "IS", "OOS")}
                cell = {t: legs(win(r, t), spy_m, bwin, t) for t in ("FULL", "H1", "H2", "IS", "OOS")}
                # 4a: Sharpe > live in BOTH halves and MaxDD no worse than live (full sample)
                p4a = (cell["H1"]["Sharpe"] > bwin["H1"]["Sharpe"]
                       and cell["H2"]["Sharpe"] > bwin["H2"]["Sharpe"]
                       and cell["FULL"]["MaxDD"] >= bwin["FULL"]["MaxDD"])
                # 4b per window; FULL additionally requires Sharpe > SPY in BOTH halves
                p4b = {}
                for t in ("FULL", "IS", "OOS"):
                    ok = cell[t]["L_SH"] and cell[t]["L_DD"] and cell[t]["L_CAGR"]
                    if t == "FULL":
                        ok = ok and cell["H1"]["L_SH"] and cell["H2"]["L_SH"]
                    p4b[t] = bool(ok)
                row = dict(panel=panel, clock=clock, L=L, band=c, bps=bps,
                           ann_turnover=bk["ann_turn"], pass4a=p4a,
                           pass4b_FULL=p4b["FULL"], pass4b_IS=p4b["IS"], pass4b_OOS=p4b["OOS"])
                for t in ("FULL", "H1", "H2", "IS", "OOS"):
                    row[f"CAGR_{t}"]   = cell[t]["CAGR"]
                    row[f"Sharpe_{t}"] = cell[t]["Sharpe"]
                    row[f"MaxDD_{t}"]  = cell[t]["MaxDD"]
                for t in ("FULL", "IS", "OOS"):
                    row[f"legSH_{t}"], row[f"legDD_{t}"], row[f"legCAGR_{t}"] = \
                        cell[t]["L_SH"], cell[t]["L_DD"], cell[t]["L_CAGR"]
                grid.append(row)

        # ---- headline table ------------------------------------------------
        log(f"\n  ALL {len(BANDS)*(len(L_WEEKS)+1)} GRID POINTS at {HEADLINE} bps "
            f"(CAGR / Sharpe / MaxDD; FULL | IS | OOS; 4a, 4b FULL/IS/OOS)")
        log("  clock   L    c     turn |      FULL CAGR  Sh     DD |       IS CAGR  Sh     DD |"
            "      OOS CAGR  Sh     DD | 4a 4bF 4bI 4bO")
        for (clock, L, c) in sorted(books, key=lambda k: (k[0], k[1], k[2])):
            g = next(x for x in grid if x["panel"] == panel and x["clock"] == clock
                     and x["L"] == L and x["band"] == c and x["bps"] == HEADLINE)
            log(f"  {clock:6s} {L:3d} {c:5.2f} {g['ann_turnover']:6.2f} |"
                f" {g['CAGR_FULL']:9.2%} {g['Sharpe_FULL']:6.3f} {g['MaxDD_FULL']:7.2%} |"
                f" {g['CAGR_IS']:9.2%} {g['Sharpe_IS']:6.3f} {g['MaxDD_IS']:7.2%} |"
                f" {g['CAGR_OOS']:9.2%} {g['Sharpe_OOS']:6.3f} {g['MaxDD_OOS']:7.2%} |"
                f" {'Y' if g['pass4a'] else '.':>2}"
                f" {'Y' if g['pass4b_FULL'] else '.':>3} {'Y' if g['pass4b_IS'] else '.':>3}"
                f" {'Y' if g['pass4b_OOS'] else '.':>3}")

        # ---- RULE 8: choose on IS only, read OOS once ----------------------
        cells = [x for x in grid if x["panel"] == panel and x["clock"] == "WEEKLY" and x["bps"] == HEADLINE]
        c1 = max(cells, key=lambda x: x["Sharpe_IS"])
        legal = [x for x in cells if x["pass4b_IS"]]
        c2 = max(legal, key=lambda x: x["Sharpe_IS"]) if legal else None
        dctl = [x for x in grid if x["panel"] == panel and x["clock"] == "DAILY" and x["bps"] == HEADLINE]
        c0 = max(dctl, key=lambda x: x["Sharpe_IS"])
        for nm, ch in (("C1 argmax IS Sharpe (habitual, WEEKLY clock)", c1),
                       ("C2 argmax IS Sharpe among IS-4b passers (WEEKLY clock)", c2),
                       ("C0 argmax IS Sharpe on the DAILY control ladder", c0)):
            if ch is None:
                log(f"\n  RULE 8 {nm}: NO CELL PASSES 4b IN SAMPLE -> chooser undefined")
                wf.append(dict(panel=panel, chooser=nm, pick=None)); continue
            log(f"\n  RULE 8 {nm}: picks L={ch['L']} c={ch['band']} "
                f"(IS Sharpe {ch['Sharpe_IS']:.4f}) -> OOS {ch['CAGR_OOS']:.2%} / "
                f"{ch['Sharpe_OOS']:.4f} / {ch['MaxDD_OOS']:.2%} vs SPY OOS "
                f"{spy_m['OOS']['CAGR']:.2%} / {spy_m['OOS']['Sharpe']:.4f} / {spy_m['OOS']['MaxDD']:.2%}"
                f" vs LIVE OOS {base_m['OOS']['CAGR']:.2%} / {base_m['OOS']['Sharpe']:.4f} / "
                f"{base_m['OOS']['MaxDD']:.2%} | 4a {ch['pass4a']} 4b OOS {ch['pass4b_OOS']}")
            wf.append(dict(panel=panel, chooser=nm, clock=ch["clock"], L=ch["L"], band=ch["band"],
                           IS_Sharpe=ch["Sharpe_IS"], OOS_CAGR=ch["CAGR_OOS"],
                           OOS_Sharpe=ch["Sharpe_OOS"], OOS_MaxDD=ch["MaxDD_OOS"],
                           pass4a=ch["pass4a"], pass4b_OOS=ch["pass4b_OOS"],
                           spy_OOS_CAGR=spy_m["OOS"]["CAGR"], spy_OOS_Sharpe=spy_m["OOS"]["Sharpe"],
                           spy_OOS_MaxDD=spy_m["OOS"]["MaxDD"],
                           live_OOS_CAGR=base_m["OOS"]["CAGR"], live_OOS_Sharpe=base_m["OOS"]["Sharpe"],
                           live_OOS_MaxDD=base_m["OOS"]["MaxDD"]))

    G, W = pd.DataFrame(grid), pd.DataFrame(wf)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    W.to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(gates).to_csv(f"{STEM}.gates.csv", index=False)

    log(f"\n{'='*100}\nGATES")
    for g in gates: log(f"  {g['panel']:5s} {g['gate']:62s} {g['value']}  ok={g['ok']}")

    log(f"\nMATCHED CLOCK CONTRAST at {HEADLINE} bps (WEEKLY L vs the DAILY control at the SAME band c)")
    h = G[G.bps == HEADLINE]
    for panel in ("U56", "B136"):
        d = h[(h.panel == panel) & (h.clock == "DAILY")].set_index("band")
        w = h[(h.panel == panel) & (h.clock == "WEEKLY")]
        for L in L_WEEKS:
            s = w[w.L == L].set_index("band")
            log(f"  {panel:5s} L={L:3d}  dCAGR_FULL {(s.CAGR_FULL - d.CAGR_FULL).mean():+7.2%}"
                f"  dSharpe_FULL {(s.Sharpe_FULL - d.Sharpe_FULL).mean():+7.4f}"
                f"  dMaxDD_FULL {(s.MaxDD_FULL - d.MaxDD_FULL).mean():+7.2%}"
                f"  dTurn {(s.ann_turnover - d.ann_turnover).mean():+6.2f}x"
                f"  dCAGR_OOS {(s.CAGR_OOS - d.CAGR_OOS).mean():+7.2%}"
                f"  dSharpe_OOS {(s.Sharpe_OOS - d.Sharpe_OOS).mean():+7.4f}")

    log(f"\nPASS COUNTS over all {len(G)} published rows (2 panels x 30 cells x 4 cost rungs)")
    for clock in ("DAILY", "WEEKLY"):
        s = G[G.clock == clock]
        log(f"  {clock:6s} n={len(s):4d}  4a {int(s.pass4a.sum()):4d}  4b FULL {int(s.pass4b_FULL.sum()):4d}"
            f"  4b IS {int(s.pass4b_IS.sum()):4d}  4b OOS {int(s.pass4b_OOS.sum()):4d}"
            f"  BOTH(4a & 4b FULL & 4b OOS) {int((s.pass4a & s.pass4b_FULL & s.pass4b_OOS).sum()):4d}")
    log("\n4a PASSERS (the only KEEP path either clock reaches on this grid)")
    ap = G[G.pass4a]
    if len(ap) == 0:
        log("  none")
    for _, r in ap.iterrows():
        log(f"  {r.panel:5s} {r.clock:6s} L={int(r.L):3d} c={r.band:.2f} @{int(r.bps):2d}bps  "
            f"FULL {r.CAGR_FULL:.2%} / {r.Sharpe_FULL:.4f} / {r.MaxDD_FULL:.2%}  "
            f"H1 {r.Sharpe_H1:.4f} H2 {r.Sharpe_H2:.4f}  OOS {r.CAGR_OOS:.2%} / {r.Sharpe_OOS:.4f} / "
            f"{r.MaxDD_OOS:.2%}  turnover {r.ann_turnover:.2f}x/yr  4b OOS {r.pass4b_OOS}")

    log("\nNEAREST-ANALOGUE CONTRAST: WEEKLY L=40 c=0.03 (the weekly twin of the live gate) vs the LIVE book")
    for panel in ("U56", "B136"):
        for bps in COSTS:
            a = G[(G.panel == panel) & (G.clock == "WEEKLY") & (G.L == 40) & (G.band == 0.03) & (G.bps == bps)].iloc[0]
            b = G[(G.panel == panel) & (G.clock == "DAILY") & (G.band == 0.03) & (G.bps == bps)].iloc[0]
            log(f"  {panel:5s} @{bps:2d}bps  dCAGR_FULL {a.CAGR_FULL-b.CAGR_FULL:+.2%}  "
                f"dSharpe_FULL {a.Sharpe_FULL-b.Sharpe_FULL:+.4f}  dMaxDD_FULL {a.MaxDD_FULL-b.MaxDD_FULL:+.2%}  "
                f"dSharpe_H1 {a.Sharpe_H1-b.Sharpe_H1:+.4f}  dSharpe_H2 {a.Sharpe_H2-b.Sharpe_H2:+.4f}  "
                f"dCAGR_OOS {a.CAGR_OOS-b.CAGR_OOS:+.2%}  dSharpe_OOS {a.Sharpe_OOS-b.Sharpe_OOS:+.4f}  "
                f"dTurn {a.ann_turnover-b.ann_turnover:+.2f}x")

    fails = G[~G.pass4b_FULL]
    log(f"  binding leg over the {len(fails)} 4b-FULL FAILs: "
        f"CAGR-only {int((~fails.legCAGR_FULL & fails.legDD_FULL & fails.legSH_FULL).sum())}, "
        f"DD-only {int((fails.legCAGR_FULL & ~fails.legDD_FULL & fails.legSH_FULL).sum())}, "
        f"Sharpe-only {int((fails.legCAGR_FULL & fails.legDD_FULL & ~fails.legSH_FULL).sum())}, "
        f"joint {int(((~fails.legCAGR_FULL).astype(int) + (~fails.legDD_FULL).astype(int) + (~fails.legSH_FULL).astype(int) > 1).sum())}")

    Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")
    print(f"\nwrote {STEM.name}.grid.csv / .walkforward.csv / .gates.csv / .console.txt")

if __name__ == "__main__":
    main()
