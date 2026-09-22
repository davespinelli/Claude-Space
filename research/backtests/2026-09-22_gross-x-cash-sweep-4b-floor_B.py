#!/usr/bin/env python3
"""Idea 2304 (lane B, 2026-09-22) — does GROSS 1.00 PLUS the CASH SWEEP clear the 4b CAGR
floor that neither clears alone?

Three standing findings in this record point at the same leg from different sides:
  * idea 2284 — the 4b CAGR floor is the SOLE binding leg in 225 of 240 cells and the 4b
    DD cap binds in 0 of 240, so drawdown is a leg with slack and CAGR is the leg that binds;
  * idea 2294 — routing the live band book's idle cash into SHY buys +0.50 pp of CAGR and
    KILLS 4b alone (0 of 104 cells): the gap at gross 0.75 is 1.48 pp;
  * idea 2119 — every committed 4b PASS in the record sits at GROSS 1.00.
Raising gross spends the slack leg (DD) to relieve the binding one (CAGR); the sweep
relieves the same binding leg through a different channel.  They have never been priced
TOGETHER, and they are not additive: raising gross CONSUMES the idle cash the sweep funds.

TWO TUNED DIALS AND NO MORE: GROSS and SWEEP FRACTION phi.  The sweep INSTRUMENT is fixed
to SHY a priori by idea 2294's duration finding (IEF/TLT fail on drawdown) and is not a
dial.  Panel {U56, B136}, cost rung {0, 10, 25, 50} bps, band 0.03 and cadence W are
REPORTED, never selected on.  Every grid point is printed.  No leverage at any cell:
gross <= 1.00 and phi <= 1.00 means sum(w) <= 1.
Rule 8: both dials chosen on 2009-2016 ONLY, 2017-2026 read ONCE.

Run:  python3 research/backtests/2026-09-22_gross-x-cash-sweep-4b-floor_B.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                              # noqa
from engine import backtest, metrics                                              # noqa

OUT = Path(__file__).with_suffix("")
BAND, FREQ = 0.03, "W"                 # the LIVE book's band and cadence, untouched
LIVE_GROSS = 0.75                      # the shipped book's gross -> the 4a baseline
INSTR = "SHY"                          # fixed a priori (idea 2294), NOT a dial
GROSSES = [0.75, 0.85, 1.00]           # dial 1
PHIS = [0.00, 0.50, 1.00]              # dial 2
COSTS = [0, 10, 25, 50]
LIVE_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"


# ---------------------------------------------------------------- weights -----
def book_weights(px, gross=LIVE_GROSS, phi=0.0, band=BAND, instrument=INSTR):
    """RULES v2 band book at `gross`, with phi of its idle cash swept into `instrument`.

    Zero hindsight: the sleeve weight at t is a deterministic function of the book's own
    weights at t.  phi=1 and gross=1 leaves sum(w) == 1 exactly, so no cell is levered.
    The sleeve is charged the same turnover cost as any other leg (it is an ordinary
    weight column); the MMF variant in section F rebates only its OWN extra turnover.
    """
    w = rules_v2_weights(px, band=band, gross=gross)
    if phi == 0.0:
        return w
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w = w.copy()
    live = px[instrument].notna().astype(float)          # no weight before the ETF prices
    w[instrument] = w[instrument] + phi * idle * live
    return w


# ------------------------------------------------- per-column turnover --------
def backtest_percol(prices, weights, cost_bps=10.0, freq=FREQ):
    """engine.backtest with PER-COLUMN turnover, so the sweep leg's own trading cost can
    be isolated for the MMF variant.  Identical arithmetic to engine.backtest otherwise."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    if freq == "D":
        mask = pd.Series(True, index=prices.index)
    else:
        s = pd.Series(prices.index.to_period(freq), index=prices.index)
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
    """PROTOCOL 4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse than live."""
    return c["H1"] > b["H1"] and c["H2"] > b["H2"] and c["MaxDD"] >= b["MaxDD"]


def path4b_full(c, s):
    return (c["H1"] > s["H1"] and c["H2"] > s["H2"]
            and c["MaxDD"] >= 0.60 * s["MaxDD"] and c["CAGR"] >= 0.70 * s["CAGR"])


def path4b_oos(c, s):
    return (c["oSharpe"] > s["oSharpe"] and c["oMaxDD"] >= 0.60 * s["oMaxDD"]
            and c["oCAGR"] >= 0.70 * s["oCAGR"])


def path4b(c, s):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
    CAGR >= 70% of SPY's.  (MaxDD is negative, so 'no worse than 60% of SPY's' is
    '>= 0.60 * SPY's MaxDD'.)"""
    return path4b_full(c, s) and c["oSharpe"] > s["oSharpe"]


def binding(c, s):
    """Which 4b_FULL leg fails, on the full sample."""
    f = {"CAGR": c["CAGR"] < 0.70 * s["CAGR"], "DD": c["MaxDD"] < 0.60 * s["MaxDD"],
         "H1": not (c["H1"] > s["H1"]), "H2": not (c["H2"] > s["H2"])}
    hit = [k for k, v in f.items() if v]
    if not hit:
        return "PASS"
    return hit[0] + "-alone" if len(hit) == 1 else "joint(" + "+".join(hit) + ")"


# ---------------------------------------------------------------- driver ------
def run_panel(name, px):
    start = px.index[260]                                 # skip warm-up, as baseline.compare
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    spy = legs(spy_r)
    rows = []
    gross_stats = {}
    for g in GROSSES:
        w = rules_v2_weights(px, band=BAND, gross=g)
        gross_stats[g] = (w.loc[start:].sum(axis=1).mean(),
                          (1.0 - w.loc[start:].sum(axis=1)).clip(lower=0).mean())
    for cost in COSTS:
        base = legs(backtest(px, rules_v2_weights(px, band=BAND, gross=LIVE_GROSS),
                             cost_bps=cost, freq=FREQ)["returns"].loc[start:])
        for g in GROSSES:
            for phi in PHIS:
                res = backtest(px, book_weights(px, g, phi), cost_bps=cost, freq=FREQ)
                r = res["returns"].loc[start:]
                c = legs(r)
                c.update(panel=name, cost=cost, gross=g, phi=phi,
                         turnover=res["turnover"].loc[start:].sum() / (len(r) / 252),
                         p4a=path4a(c, base), p4b=path4b(c, spy),
                         p4b_full=path4b_full(c, spy), p4b_oos=path4b_oos(c, spy),
                         bind=binding(c, spy),
                         cagr_gap=c["CAGR"] - 0.70 * spy["CAGR"],
                         dd_slack=c["MaxDD"] - 0.60 * spy["MaxDD"],
                         dCAGR=c["CAGR"] - base["CAGR"], dSharpe=c["Sharpe"] - base["Sharpe"],
                         dMaxDD=c["MaxDD"] - base["MaxDD"])
                rows.append(c)
    return pd.DataFrame(rows), spy, gross_stats


def is_metrics(px, g, phi, cost):
    """Rule 8 chooser inputs: IS window ONLY (warm-up .. 2016-12-31)."""
    start = px.index[260]
    r = backtest(px, book_weights(px, g, phi), cost_bps=cost,
                 freq=FREQ)["returns"].loc[start:IS_END]
    m = metrics(r)
    return m["Sharpe"], m["CAGR"], m["MaxDD"]


def main():
    pd.set_option("display.width", 240)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    report = []

    def say(s=""):
        print(s); report.append(s)

    say("=" * 118)
    say("IDEA 2304 — GROSS x CASH-SWEEP AGAINST THE 4b CAGR FLOOR (lane B, 2026-09-22)")
    say(f"book: RULES v2 band={BAND} freq={FREQ}; dials = (GROSS {GROSSES}, PHI {PHIS}); "
        f"sweep instrument fixed {INSTR}")
    say(f"costs {COSTS} bps REPORTED not selected; 4a baseline = the SHIPPED book "
        f"(gross {LIVE_GROSS}, phi 0) at the same rung")
    say("=" * 118)

    all_rows, spys = [], {}
    for name, px in panels.items():
        df, spy, gs = run_panel(name, px)
        all_rows.append(df); spys[name] = spy
        say()
        say(f"--- PANEL {name}  ({px.shape[1]} columns, {px.index[0].date()}..{px.index[-1].date()}) ---")
        for g in GROSSES:
            say(f"  gross {g:.2f}: realised MEAN GROSS {gs[g][0]:.4f}  =>  mean IDLE CASH "
                f"{gs[g][1]:.4f} of NAV (the capital the sweep can fund)")
        say(f"  SPY: CAGR {spy['CAGR']:.4%} Sharpe {spy['Sharpe']:.4f} MaxDD {spy['MaxDD']:.4%} "
            f"halves {spy['H1']:.4f}/{spy['H2']:.4f} | OOS {spy['oCAGR']:.4%}/{spy['oSharpe']:.4f}/{spy['oMaxDD']:.4%}")
        say(f"  4b bars: FULL CAGR floor {0.70*spy['CAGR']:.4%}  DD cap {0.60*spy['MaxDD']:.4%} "
            f"| OOS floor {0.70*spy['oCAGR']:.4%}  cap {0.60*spy['oMaxDD']:.4%}")
        say()
        say("  ALL GRID POINTS (every gross x phi x cost rung, nothing withheld):")
        show = df[["cost", "gross", "phi", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                   "oCAGR", "oSharpe", "oMaxDD", "turnover", "cagr_gap", "dd_slack",
                   "p4a", "p4b_full", "p4b_oos", "p4b", "bind"]].copy()
        for c in ["CAGR", "MaxDD", "oCAGR", "oMaxDD", "cagr_gap", "dd_slack"]:
            show[c] = (show[c] * 100).round(4)
        for c in ["Sharpe", "H1", "H2", "oSharpe", "turnover"]:
            show[c] = show[c].round(4)
        say(show.to_string(index=False))

    df = pd.concat(all_rows, ignore_index=True)
    df.to_csv(str(OUT) + ".grid.csv", index=False)

    # ------------------------------------------------- A) the two channels ----
    say()
    say("=" * 118)
    say("A) THE TWO CHANNELS AT THE LIVE 10 bps RUNG — are they additive?")
    say("   marginal GROSS  = (gross 1.00, phi) minus (gross 0.75, phi)")
    say("   marginal SWEEP  = (gross, phi 1.00) minus (gross, phi 0.00)")
    say("=" * 118)
    chan = []
    for name in panels:
        d = df[(df.panel == name) & (df.cost == LIVE_COST)].set_index(["gross", "phi"])
        base = d.loc[(LIVE_GROSS, 0.00)]
        joint = d.loc[(1.00, 1.00)]
        g_only = d.loc[(1.00, 0.00)]
        s_only = d.loc[(LIVE_GROSS, 1.00)]
        mg = (g_only["CAGR"] - base["CAGR"]) * 100
        ms = (s_only["CAGR"] - base["CAGR"]) * 100
        mj = (joint["CAGR"] - base["CAGR"]) * 100
        chan.append(dict(panel=name, gross_only_pp=mg, sweep_only_pp=ms, joint_pp=mj,
                         sum_of_parts_pp=mg + ms, interaction_pp=mj - mg - ms,
                         floor_gap_pp=-base["cagr_gap"] * 100,
                         joint_gap_pp=-joint["cagr_gap"] * 100))
        say(f"  {name}: shipped book CAGR {base['CAGR']:.4%}, 4b floor gap {-base['cagr_gap']*100:+.4f} pp")
        say(f"    GROSS alone  (1.00, phi 0.00): {mg:+.4f} pp CAGR   MaxDD {g_only['MaxDD']:.4%} "
            f"(slack {g_only['dd_slack']*100:+.4f} pp)   4b_FULL {g_only['p4b_full']}")
        say(f"    SWEEP alone  (0.75, phi 1.00): {ms:+.4f} pp CAGR   MaxDD {s_only['MaxDD']:.4%} "
            f"(slack {s_only['dd_slack']*100:+.4f} pp)   4b_FULL {s_only['p4b_full']}")
        say(f"    JOINT        (1.00, phi 1.00): {mj:+.4f} pp CAGR   MaxDD {joint['MaxDD']:.4%} "
            f"(slack {joint['dd_slack']*100:+.4f} pp)   4b_FULL {joint['p4b_full']}  "
            f"4b_OOS {joint['p4b_oos']}  4a {joint['p4a']}")
        say(f"    sum of parts {mg+ms:+.4f} pp vs joint {mj:+.4f} pp  =>  INTERACTION "
            f"{mj-mg-ms:+.4f} pp   remaining floor gap {-joint['cagr_gap']*100:+.4f} pp")
    pd.DataFrame(chan).to_csv(str(OUT) + ".channels.csv", index=False)

    # ------------------------------------------------- B) KEEP-path census ----
    say()
    say("=" * 118)
    say("B) KEEP-PATH CENSUS OVER EVERY GRID POINT")
    say("=" * 118)
    say(f"  cells {len(df)}:  4a PASS {int(df.p4a.sum())}   4b(FULL+OOS-Sharpe) PASS "
        f"{int(df.p4b.sum())}   4b_FULL {int(df.p4b_full.sum())}   4b_OOS {int(df.p4b_oos.sum())}")
    for name in panels:
        d = df[df.panel == name]
        say(f"  {name}: 4a {int(d.p4a.sum())}/{len(d)}  4b {int(d.p4b.sum())}/{len(d)}  "
            f"4b_FULL {int(d.p4b_full.sum())}/{len(d)}  4b_OOS {int(d.p4b_oos.sum())}/{len(d)}")
    say()
    say("  BINDING LEG of every 4b_FULL FAIL:")
    say("    " + df.bind.value_counts().to_string().replace("\n", "\n    "))
    say()
    say("  4a PASS cells (gross, phi, cost, panel):")
    pas = df[df.p4a]
    if len(pas):
        for _, c in pas.iterrows():
            say(f"    {c['panel']} cost {c['cost']:>2} bps  gross {c['gross']:.2f} phi {c['phi']:.2f}  "
                f"CAGR {c['CAGR']:.4%} Sharpe {c['Sharpe']:.4f} MaxDD {c['MaxDD']:.4%} "
                f"halves {c['H1']:.4f}/{c['H2']:.4f}")
    else:
        say("    NONE")
    say()
    say("  4b_FULL PASS cells:")
    pbs = df[df.p4b_full]
    if len(pbs):
        for _, c in pbs.iterrows():
            say(f"    {c['panel']} cost {c['cost']:>2} bps  gross {c['gross']:.2f} phi {c['phi']:.2f}  "
                f"CAGR {c['CAGR']:.4%} Sharpe {c['Sharpe']:.4f} MaxDD {c['MaxDD']:.4%} "
                f"halves {c['H1']:.4f}/{c['H2']:.4f}  4b_OOS {c['p4b_oos']}  4b(both) {c['p4b']}")
    else:
        say("    NONE")

    # ------------------------------------------------- C) rule 8 --------------
    say()
    say("=" * 118)
    say("C) RULE 8 WALK-FORWARD — BOTH DIALS CHOSEN ON 2009-2016 ONLY, 2017-2026 READ ONCE")
    say("=" * 118)
    cells = [(g, p) for g in GROSSES for p in PHIS]
    wf = []
    for name, px in panels.items():
        s = spys[name]
        iss = {k: is_metrics(px, k[0], k[1], LIVE_COST) for k in cells}
        say(f"  --- {name} ---")
        say("    IS (2009-2016) Sharpe by cell: " +
            "  ".join(f"g{g:.2f}/p{p:.2f}:{iss[(g,p)][0]:.4f}" for g, p in cells))
        say("    IS (2009-2016) CAGR   by cell: " +
            "  ".join(f"g{g:.2f}/p{p:.2f}:{iss[(g,p)][1]:.2%}" for g, p in cells))
        spy_is = metrics(px["SPY"].pct_change().fillna(0).loc[px.index[260]:IS_END])
        pick = max(iss, key=lambda k: iss[k][0])                       # C_ISSHARPE
        ok = [k for k in cells if iss[k][1] >= 0.70 * spy_is["CAGR"]
              and iss[k][2] >= 0.60 * spy_is["MaxDD"] and iss[k][0] > spy_is["Sharpe"]]
        pick4b = max(ok, key=lambda k: iss[k][1]) if ok else None      # C_IS4b: best IS CAGR among IS-4b cells
        zero = (1.00, 1.00)          # zero-parameter default: fully invested, all idle cash swept
        ship = (LIVE_GROSS, 0.00)    # the shipped book
        for label, k in [("C_ISSHARPE", pick), ("C_IS4b", pick4b),
                         ("C_ZERO (no fitting)", zero), ("SHIPPED BOOK", ship)]:
            if k is None:
                say(f"    {label}: UNDEFINED — no cell clears 4b in sample")
                wf.append(dict(panel=name, chooser=label, pick=None))
                continue
            c = df[(df.panel == name) & (df.cost == LIVE_COST) & (df.gross == k[0])
                   & (df.phi == k[1])].iloc[0]
            say(f"    {label}: picks gross {k[0]:.2f} / phi {k[1]:.2f} (IS Sharpe {iss[k][0]:.4f}) -> "
                f"OOS 2017-2026 {c['oCAGR']:.4%} / {c['oSharpe']:.4f} / {c['oMaxDD']:.4%}   "
                f"4b_OOS {c['p4b_oos']}   4a(FULL) {c['p4a']}")
            wf.append(dict(panel=name, chooser=label, gross=k[0], phi=k[1],
                           is_sharpe=iss[k][0], oCAGR=c["oCAGR"], oSharpe=c["oSharpe"],
                           oMaxDD=c["oMaxDD"], p4b_oos=bool(c["p4b_oos"]), p4a=bool(c["p4a"])))
        say(f"    SPY OOS: {s['oCAGR']:.4%} / {s['oSharpe']:.4f} / {s['oMaxDD']:.4%}   "
            f"(4b OOS bars: CAGR >= {0.70*s['oCAGR']:.4%}, MaxDD >= {0.60*s['oMaxDD']:.4%}, "
            f"Sharpe > {s['oSharpe']:.4f})")
    pd.DataFrame(wf).to_csv(str(OUT) + ".walkforward.csv", index=False)

    # ------------------------------------------------- D) MMF variant ---------
    say()
    say("=" * 118)
    say("D) MMF-SWEEP VARIANT — the sweep leg's OWN extra turnover rebated to 0 bps")
    say("   A real account sweeps cash into a money-market fund and pays ~nothing to do it.")
    say("   The grid above charges the sweep a full round trip like any equity leg, so those")
    say("   rows are a LOWER BOUND.  Here the book pays its stated rung and only the SWEEP")
    say("   column's EXTRA turnover (full book minus the same-gross phi=0 book) is rebated.")
    say("=" * 118)
    mmf = []
    for name, px in panels.items():
        s = spys[name]
        start = px.index[260]
        base = legs(backtest(px, rules_v2_weights(px, band=BAND, gross=LIVE_GROSS),
                             cost_bps=LIVE_COST, freq=FREQ)["returns"].loc[start:])
        for g in GROSSES:
            w0 = rules_v2_weights(px, band=BAND, gross=g)
            t0 = backtest_percol(px, w0, cost_bps=LIVE_COST)["tcol"][INSTR]
            for phi in [p for p in PHIS if p > 0]:
                res = backtest_percol(px, book_weights(px, g, phi), cost_bps=LIVE_COST)
                extra = (res["tcol"][INSTR] - t0).clip(lower=0.0)
                r = (res["returns"] + extra * LIVE_COST / 1e4).loc[start:]
                c = legs(r)
                c.update(panel=name, gross=g, phi=phi, p4a=path4a(c, base),
                         p4b_full=path4b_full(c, s), p4b_oos=path4b_oos(c, s),
                         p4b=path4b(c, s), bind=binding(c, s),
                         cagr_gap=c["CAGR"] - 0.70 * s["CAGR"])
                mmf.append(c)
                say(f"  {name} gross {g:.2f} phi {phi:.2f}: CAGR {c['CAGR']:.4%} "
                    f"Sharpe {c['Sharpe']:.4f} MaxDD {c['MaxDD']:.4%} halves "
                    f"{c['H1']:.4f}/{c['H2']:.4f} | OOS {c['oCAGR']:.4%}/{c['oSharpe']:.4f}/"
                    f"{c['oMaxDD']:.4%} | 4a {c['p4a']} 4b_FULL {c['p4b_full']} "
                    f"4b_OOS {c['p4b_oos']} | floor gap {-c['cagr_gap']*100:+.4f} pp  [{c['bind']}]")
    mdf = pd.DataFrame(mmf)
    mdf.to_csv(str(OUT) + ".mmf.csv", index=False)
    say(f"  MMF variant census: cells {len(mdf)}  4a {int(mdf.p4a.sum())}  "
        f"4b_FULL {int(mdf.p4b_full.sum())}  4b_OOS {int(mdf.p4b_oos.sum())}  "
        f"4b(both) {int(mdf.p4b.sum())}")

    # ------------------------------------------------- E) how far short -------
    say()
    say("=" * 118)
    say("E) HOW FAR SHORT IS THE BEST CELL ON EVERY 4b LEG?  (live 10 bps rung)")
    say("=" * 118)
    for name in panels:
        s = spys[name]
        d = df[(df.panel == name) & (df.cost == LIVE_COST)]
        best = d.loc[d.CAGR.idxmax()]
        say(f"  {name} best-CAGR cell: gross {best['gross']:.2f} phi {best['phi']:.2f}")
        say(f"    CAGR   {best['CAGR']:.4%}  vs floor {0.70*s['CAGR']:.4%}   -> "
            f"{best['cagr_gap']*100:+.4f} pp   {'CLEARS' if best['cagr_gap']>=0 else 'SHORT'}")
        say(f"    MaxDD  {best['MaxDD']:.4%}  vs cap   {0.60*s['MaxDD']:.4%}   -> "
            f"{best['dd_slack']*100:+.4f} pp slack")
        say(f"    H1     {best['H1']:.4f}   vs SPY {s['H1']:.4f}   "
            f"{'OK' if best['H1']>s['H1'] else 'FAIL'}")
        say(f"    H2     {best['H2']:.4f}   vs SPY {s['H2']:.4f}   "
            f"{'OK' if best['H2']>s['H2'] else 'FAIL'}")
        say(f"    OOS Sharpe {best['oSharpe']:.4f} vs SPY {s['oSharpe']:.4f}   "
            f"{'OK' if best['oSharpe']>s['oSharpe'] else 'FAIL'}")

    Path(str(OUT) + ".console.txt").write_text("\n".join(report) + "\n")
    print(f"\nwrote {OUT}.grid.csv / .channels.csv / .walkforward.csv / .mmf.csv / .console.txt")


if __name__ == "__main__":
    main()
