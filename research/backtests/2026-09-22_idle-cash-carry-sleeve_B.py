#!/usr/bin/env python3
"""Idea 2294 (lane B, 2026-09-22) — does parking the band book's IDLE CASH in a T-bill
sleeve clear the 4b CAGR floor?

Every book in this record leaves `1 - sum(w)` earning EXACTLY 0%: engine.backtest drifts
the un-invested residual at a flat `(1 - cur.sum())` with no return attached.  RULES v2
runs at gross 0.75 and de-grosses further whenever the 200d +/-3% band gates a name OUT,
so the live book sits idle in cash a large fraction of every year.  A real account holds
that cash in T-bills.  Idea 2284 found the 4b CAGR floor is the SOLE binding leg in 225 of
240 cells and the DD leg binds in 0 of 240 — the one binding constraint is exactly the one
a carry sleeve relieves.

TWO TUNED DIALS AND NO MORE: carry instrument and phi.  Panel {U56, B136}, cost rung
{0, 10, 25, 50} bps and cadence (W) are REPORTED, never selected.  Every grid point is
printed.  Rule 8: dials chosen on 2009-2016 ONLY, 2017-2026 read ONCE.

Run:  python3 research/backtests/2026-09-22_idle-cash-carry-sleeve_B.py
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights            # noqa
from engine import backtest, metrics                                              # noqa

OUT = Path(__file__).with_suffix("")
BAND, GROSS, FREQ = 0.03, 0.75, "W"          # the LIVE book, untouched
COSTS = [0, 10, 25, 50]
LIVE_COST = 10
INSTR = ["NONE", "SHY", "IEF", "TLT"]
PHIS = [0.00, 0.25, 0.50, 0.75, 1.00]
IS_END, OOS_START = "2016-12-31", "2017-01-01"


# ---------------------------------------------------------------- weights -----
def carry_weights(px, instrument="SHY", phi=1.0, band=BAND, gross=GROSS):
    """RULES v2 band book + phi of its idle cash parked in `instrument`.

    Zero hindsight: the sleeve weight at t is a deterministic function of the book's own
    weights at t.  phi=1 leaves the book fully invested (sum of weights == 1), so there is
    no leverage at any grid point.  The sleeve is charged the same turnover cost as any
    other leg because it is an ordinary weight column.
    """
    w = rules_v2_weights(px, band=band, gross=gross)
    if instrument == "NONE" or phi == 0.0:
        return w
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w = w.copy()
    live = px[instrument].notna().astype(float)          # no weight before the ETF prices
    w[instrument] = w[instrument] + phi * idle * live
    return w



# ------------------------------------------------- per-column turnover --------
def backtest_percol(prices, weights, cost_bps=10.0, freq=FREQ):
    """Exact replica of engine.backtest that also returns PER-COLUMN turnover, so the
    carry sleeve's own trading cost can be isolated.  Verified against engine.backtest."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = pd.Series(True, index=prices.index) if freq == "D" else None
    if mask is None:
        key = prices.index.to_period(freq)
        s = pd.Series(key, index=prices.index)
        mask = s != s.shift(-1)
    mask = mask.shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    tcol = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns)); turnover = pd.Series(0.0, index=prices.index)
    for i in range(len(prices.index)):
        if mask.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            d = np.abs(new - cur)
            tcol.iloc[i] = d; turnover.iloc[i] = d.sum(); cur = new
        held.iloc[i] = cur
        growth = cur * (1 + rets.iloc[i].values)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "turnover": turnover, "tcol": tcol}

# ---------------------------------------------------------------- scoring -----
def legs(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], oCAGR=o["CAGR"], oSharpe=o["Sharpe"], oMaxDD=o["MaxDD"])


def path4a(c, b):
    """Sharpe > live RULES v2 in BOTH halves and MaxDD no worse than live."""
    return c["H1"] > b["H1"] and c["H2"] > b["H2"] and c["MaxDD"] >= b["MaxDD"]


def path4b_full(c, s):
    return (c["H1"] > s["H1"] and c["H2"] > s["H2"]
            and c["MaxDD"] >= 0.60 * s["MaxDD"] and c["CAGR"] >= 0.70 * s["CAGR"])


def path4b_oos(c, s):
    return (c["oSharpe"] > s["oSharpe"] and c["oMaxDD"] >= 0.60 * s["oMaxDD"]
            and c["oCAGR"] >= 0.70 * s["oCAGR"])


def path4b(c, s):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.  (MaxDD is negative, so '<= 60% of SPY's' is '>= 0.60*SPY')."""
    return path4b_full(c, s) and c["oSharpe"] > s["oSharpe"]


# ---------------------------------------------------------------- driver ------
def run_panel(name, px):
    start = px.index[260]                                 # skip warm-up, as baseline.compare
    rows, series = [], {}

    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    spy = legs(spy_r)
    base_w = rules_v2_weights(px, band=BAND, gross=GROSS)
    v1_w = rules_v1_weights(px)

    mean_gross = base_w.loc[start:].sum(axis=1).mean()
    idle_mean = (1.0 - base_w.loc[start:].sum(axis=1)).clip(lower=0).mean()

    for cost in COSTS:
        b_r = backtest(px, base_w, cost_bps=cost, freq=FREQ)["returns"].loc[start:]
        base = legs(b_r)
        if cost == LIVE_COST:
            series["RULES v2 (live)"] = b_r
            series["SPY"] = spy_r
            series["RULES v1"] = backtest(px, v1_w, cost_bps=cost, freq=FREQ)["returns"].loc[start:]
        for ins in INSTR:
            for phi in PHIS:
                if ins == "NONE" and phi != 0.0:
                    continue                              # control is a single cell
                if ins != "NONE" and phi == 0.0:
                    continue                              # identical to the control
                res = backtest(px, carry_weights(px, ins, phi), cost_bps=cost, freq=FREQ)
                r = res["returns"].loc[start:]
                c = legs(r)
                c.update(panel=name, cost=cost, instr=ins, phi=phi,
                         turnover=res["turnover"].loc[start:].sum() / (len(r) / 252),
                         p4a=path4a(c, base), p4b=path4b(c, spy),
                         p4b_full=path4b_full(c, spy), p4b_oos=path4b_oos(c, spy),
                         dCAGR=c["CAGR"] - base["CAGR"], dSharpe=c["Sharpe"] - base["Sharpe"],
                         dMaxDD=c["MaxDD"] - base["MaxDD"])
                rows.append(c)
                if cost == LIVE_COST:
                    series[f"{ins} phi={phi:.2f}"] = r
    return pd.DataFrame(rows), spy, series, mean_gross, idle_mean


def is_metrics(px, ins, phi, cost):
    """Rule 8 chooser inputs: IS window ONLY (warm-up .. 2016-12-31)."""
    start = px.index[260]
    r = backtest(px, carry_weights(px, ins, phi), cost_bps=cost,
                 freq=FREQ)["returns"].loc[start:IS_END]
    m = metrics(r)
    return m["Sharpe"], m["CAGR"], m["MaxDD"]


def main():
    pd.set_option("display.width", 200)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    all_rows, report = [], []

    def say(s=""):
        print(s); report.append(s)

    say("=" * 110)
    say("IDEA 2294 — IDLE-CASH CARRY SLEEVE ON THE LIVE RULES v2 BAND BOOK (lane B, 2026-09-22)")
    say(f"book: band={BAND} gross={GROSS} freq={FREQ}; dials = (carry instrument, phi); "
        f"costs {COSTS} bps REPORTED not selected")
    say("=" * 110)

    spys, seriess = {}, {}
    for name, px in panels.items():
        df, spy, series, mg, idle = run_panel(name, px)
        all_rows.append(df); spys[name] = spy; seriess[name] = series
        say()
        say(f"--- PANEL {name}  ({px.shape[1]} columns, {px.index[0].date()}..{px.index[-1].date()}) ---")
        say(f"live book mean gross {mg:.4f}  =>  mean IDLE CASH {idle:.4f} of NAV "
            f"(the capital the sleeve funds)")
        say(f"SPY: CAGR {spy['CAGR']:.4%} Sharpe {spy['Sharpe']:.4f} MaxDD {spy['MaxDD']:.4%} "
            f"halves {spy['H1']:.4f}/{spy['H2']:.4f} | OOS {spy['oCAGR']:.4%}/{spy['oSharpe']:.4f}/{spy['oMaxDD']:.4%}")
        say(f"4b bars on this panel: CAGR floor {0.70*spy['CAGR']:.4%}  DD cap {0.60*spy['MaxDD']:.4%} "
            f"| OOS floor {0.70*spy['oCAGR']:.4%} cap {0.60*spy['oMaxDD']:.4%}")
        say()
        say("ALL GRID POINTS (every cell, every cost rung):")
        show = df[["cost", "instr", "phi", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "oCAGR", "oSharpe", "oMaxDD", "turnover", "dCAGR", "p4a", "p4b_full",
                   "p4b_oos", "p4b"]].copy()
        for c in ["CAGR", "MaxDD", "oCAGR", "oMaxDD", "dCAGR"]:
            show[c] = (show[c] * 100).round(4)
        for c in ["Sharpe", "H1", "H2", "oSharpe", "turnover"]:
            show[c] = show[c].round(4)
        say(show.to_string(index=False))

    df = pd.concat(all_rows, ignore_index=True)
    df.to_csv(str(OUT) + ".grid.csv", index=False)

    # ---------------------------------------------------------- headline ------
    say()
    say("=" * 110)
    say("A) WHAT THE SLEEVE IS WORTH (live 10 bps rung, phi=1.00, vs the phi=0 control)")
    say("=" * 110)
    for name in panels:
        ctl = df[(df.panel == name) & (df.cost == LIVE_COST) & (df.instr == "NONE")].iloc[0]
        say(f"  {name} control (idle cash at 0%): CAGR {ctl['CAGR']:.4%} Sharpe {ctl['Sharpe']:.4f} "
            f"MaxDD {ctl['MaxDD']:.4%} halves {ctl['H1']:.4f}/{ctl['H2']:.4f} | "
            f"OOS {ctl['oCAGR']:.4%}/{ctl['oSharpe']:.4f}/{ctl['oMaxDD']:.4%}")
        for ins in ["SHY", "IEF", "TLT"]:
            c = df[(df.panel == name) & (df.cost == LIVE_COST) & (df.instr == ins)
                   & (df.phi == 1.00)].iloc[0]
            say(f"    {ins} phi=1.00: dCAGR {c['dCAGR']*100:+.4f}pp  dSharpe {c['dSharpe']:+.4f}  "
                f"dMaxDD {c['dMaxDD']*100:+.4f}pp  turnover {c['turnover']:.4f}x/yr  "
                f"4a {c['p4a']}  4b_FULL {c['p4b_full']}  4b_OOS {c['p4b_oos']}")

    say()
    say("=" * 110)
    say("B) KEEP-PATH CENSUS OVER EVERY GRID POINT")
    say("=" * 110)
    say(f"  cells: {len(df)}   4a PASS {int(df.p4a.sum())}   4b(FULL+OOS-Sharpe) PASS {int(df.p4b.sum())}"
        f"   4b_FULL {int(df.p4b_full.sum())}   4b_OOS {int(df.p4b_oos.sum())}")
    for name in panels:
        d = df[df.panel == name]
        say(f"  {name}: 4a {int(d.p4a.sum())}/{len(d)}  4b {int(d.p4b.sum())}/{len(d)}  "
            f"4b_FULL {int(d.p4b_full.sum())}/{len(d)}  4b_OOS {int(d.p4b_oos.sum())}/{len(d)}")

    # which 4b leg binds, on the FULL sample, at every cell
    say()
    say("  BINDING LEG on every 4b_FULL FAIL (CAGR floor / DD cap / H1 / H2):")
    for name in panels:
        s = spys[name]
        d = df[df.panel == name]
        cnt = dict(CAGR=0, DD=0, H1=0, H2=0, joint=0, pass_=0)
        for _, c in d.iterrows():
            f = [c["CAGR"] < 0.70 * s["CAGR"], c["MaxDD"] < 0.60 * s["MaxDD"],
                 not (c["H1"] > s["H1"]), not (c["H2"] > s["H2"])]
            if not any(f):
                cnt["pass_"] += 1
            elif sum(f) > 1:
                cnt["joint"] += 1
            else:
                cnt[["CAGR", "DD", "H1", "H2"][f.index(True)]] += 1
        say(f"    {name}: PASS {cnt['pass_']}  CAGR-alone {cnt['CAGR']}  DD-alone {cnt['DD']}  "
            f"H1-alone {cnt['H1']}  H2-alone {cnt['H2']}  joint {cnt['joint']}")

    # ---- FLIP CENSUS: does the sleeve flip a 4b FAIL to a PASS at a matched cell? ----
    say()
    say("  FLIP CENSUS (each sleeve cell against its OWN (panel, cost) control):")
    flips = []
    for name in panels:
        for cost in COSTS:
            ctl = df[(df.panel == name) & (df.cost == cost) & (df.instr == "NONE")].iloc[0]
            for _, c in df[(df.panel == name) & (df.cost == cost) & (df.instr != "NONE")].iterrows():
                for leg, k in [("4b_FULL", "p4b_full"), ("4b_OOS", "p4b_oos"), ("4a", "p4a")]:
                    if c[k] and not ctl[k]:
                        flips.append((name, cost, c["instr"], c["phi"], leg, "FAIL->PASS"))
                    if ctl[k] and not c[k]:
                        flips.append((name, cost, c["instr"], c["phi"], leg, "PASS->FAIL"))
    if flips:
        for f in flips:
            say(f"    {f}")
    else:
        say("    NONE — no cell on the grid flips any KEEP leg in either direction.")
    say(f"    total flips: {len(flips)}  (FAIL->PASS {sum(1 for f in flips if f[5]=='FAIL->PASS')}, "
        f"PASS->FAIL {sum(1 for f in flips if f[5]=='PASS->FAIL')})")

    # ---------------------------------------------------------- regime --------
    say()
    say("=" * 110)
    say("C) IS THE SLEEVE A 2022-2026 RATE-REGIME DRAW?  (SHY's own carry, by calendar year)")
    say("=" * 110)
    px = panels["U56"]
    shy = px["SHY"].loc[px.index[260]:]
    yr = shy.resample("YE").last().pct_change().dropna()
    say("  SHY calendar-year total return: " + "  ".join(f"{i.year}:{v:+.2%}" for i, v in yr.items()))
    say(f"  SHY CAGR 2009-2016 {(shy.loc[:IS_END].iloc[-1]/shy.iloc[0])**(252/len(shy.loc[:IS_END]))-1:.4%}"
        f"   2017-2026 {(shy.iloc[-1]/shy.loc[OOS_START:].iloc[0])**(252/len(shy.loc[OOS_START:]))-1:.4%}")
    for name in panels:
        d = df[(df.panel == name) & (df.cost == LIVE_COST) & (df.instr == "SHY") & (df.phi == 1.00)]
        c = d.iloc[0]
        ctl = df[(df.panel == name) & (df.cost == LIVE_COST) & (df.instr == "NONE")].iloc[0]
        say(f"  {name} SHY phi=1.00 minus control: dCAGR FULL {c['dCAGR']*100:+.4f}pp   "
            f"dCAGR OOS {(c['oCAGR']-ctl['oCAGR'])*100:+.4f}pp   "
            f"dCAGR IS-half {(c['H1']-ctl['H1']):+.4f} (Sharpe H1)")

    # ---------------------------------------------------------- rule 8 --------
    say()
    say("=" * 110)
    say("D) RULE 8 WALK-FORWARD — dials chosen on 2009-2016 ONLY, 2017-2026 READ ONCE")
    say("=" * 110)
    cells = [(i, p) for i in INSTR for p in PHIS
             if (i == "NONE" and p == 0.0) or (i != "NONE" and p > 0.0)]
    for name, px in panels.items():
        s = spys[name]
        iss = {(i, p): is_metrics(px, i, p, LIVE_COST) for i, p in cells}
        say(f"  --- {name} ---")
        say("    IS (2009-2016) Sharpe by cell: " +
            "  ".join(f"{i}/{p:.2f}:{v[0]:.4f}" for (i, p), v in sorted(iss.items())))
        # C_ISSHARPE
        pick = max(iss, key=lambda k: iss[k][0])
        # C_IS4b: argmax IS Sharpe among cells clearing 4b IN SAMPLE
        spy_is = metrics(px["SPY"].pct_change().fillna(0).loc[px.index[260]:IS_END])
        ok = [k for k in cells if iss[k][1] >= 0.70 * spy_is["CAGR"]
              and iss[k][2] >= 0.60 * spy_is["MaxDD"] and iss[k][0] > spy_is["Sharpe"]]
        pick4b = max(ok, key=lambda k: iss[k][0]) if ok else None
        zero = ("SHY", 1.00)          # zero-parameter default: park ALL idle cash in T-bills
        for label, k in [("C_ISSHARPE", pick), ("C_IS4b", pick4b), ("C_ZERO (no fitting)", zero)]:
            if k is None:
                say(f"    {label}: UNDEFINED — no cell clears 4b in sample")
                continue
            c = df[(df.panel == name) & (df.cost == LIVE_COST) & (df.instr == k[0])
                   & (df.phi == (0.0 if k[0] == "NONE" else k[1]))].iloc[0]
            say(f"    {label}: picks {k[0]}/phi={k[1]:.2f} (IS Sharpe {iss[k][0]:.4f}) -> "
                f"OOS 2017-2026 {c['oCAGR']:.4%} / {c['oSharpe']:.4f} / {c['oMaxDD']:.4%}   "
                f"4b_OOS {c['p4b_oos']}  4a {c['p4a']}")
        ctl = df[(df.panel == name) & (df.cost == LIVE_COST) & (df.instr == "NONE")].iloc[0]
        say(f"    SHIPPED DEFAULT (no sleeve): OOS {ctl['oCAGR']:.4%} / {ctl['oSharpe']:.4f} / "
            f"{ctl['oMaxDD']:.4%}   4b_OOS {ctl['p4b_oos']}")
        say(f"    SPY OOS: {s['oCAGR']:.4%} / {s['oSharpe']:.4f} / {s['oMaxDD']:.4%}  "
            f"(4b OOS bars: CAGR >= {0.70*s['oCAGR']:.4%}, MaxDD >= {0.60*s['oMaxDD']:.4%})")


    # ------------------------------------------------- E) MMF-sweep variant ---
    say()
    say("=" * 110)
    say("E) MMF-SWEEP VARIANT — the sleeve's OWN turnover rebated to 0 bps")
    say("   A real account sweeps idle cash into a money-market fund and pays nothing to do it;")
    say("   the grid above charges the sleeve a full 10-50 bps round trip like any equity leg,")
    say("   so those rows are a LOWER BOUND.  Here the book still pays its stated rung and the")
    say("   sleeve column's EXTRA turnover (full book minus band book, same column) is rebated.")
    say("=" * 110)
    for name, px in panels.items():
        s = spys[name]
        start = px.index[260]
        w_book = rules_v2_weights(px, band=BAND, gross=GROSS)
        for cost in COSTS:
            base_r = backtest(px, w_book, cost_bps=cost, freq=FREQ)["returns"].loc[start:]
            base = legs(base_r)
            bk = backtest_percol(px, w_book, cost_bps=cost)
            for ins in ["SHY", "IEF"]:
                w_full = carry_weights(px, ins, 1.00)
                fl = backtest_percol(px, w_full, cost_bps=cost)
                extra = (fl["tcol"][ins] - bk["tcol"][ins]).abs().loc[start:]
                r = fl["returns"].loc[start:] + extra * cost / 1e4
                c = legs(r)
                say(f"  {name} {ins} phi=1.00 @ book {cost} bps / sleeve 0 bps: "
                    f"{c['CAGR']:.4%} / {c['Sharpe']:.4f} / {c['MaxDD']:.4%}  "
                    f"halves {c['H1']:.4f}/{c['H2']:.4f}  OOS {c['oCAGR']:.4%}/{c['oSharpe']:.4f}/{c['oMaxDD']:.4%}  "
                    f"| 4a {path4a(c, base)}  4b_FULL {path4b_full(c, s)}  4b_OOS {path4b_oos(c, s)}  "
                    f"| rebate {extra.sum()*cost/1e4/(len(r)/252)*100:.4f} pp/yr")

    Path(str(OUT) + ".console.txt").write_text("\n".join(report) + "\n")
    print(f"\nwrote {OUT}.grid.csv and {OUT}.console.txt")


if __name__ == "__main__":
    main()
