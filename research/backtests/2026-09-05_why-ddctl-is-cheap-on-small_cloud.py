#!/usr/bin/env python3
"""QUEUE idea 118 — why-the-DD-control-is-cheap-on-small-caps (cloud, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 97 found the book-level DD control prices at 0.16-0.57 on the 439-name panel against
0.58-0.86 on u56/broad, reversing idea 22's headline and making it the CHEAPEST instrument
there.  Is it the deeper control drawdown (-30.8% vs -17%), higher single-name vol, or idea
93's absorbing-state firing more often?  Bears on ideas 22, 74, 93."

The object on trial is a PRICE, and a price is a ratio.  Idea 74's menu quotes it as pp of
CAGR surrendered per pp of MaxDD bought, which is a number in units of the book it was
measured on — so before any of the queue's three mechanisms is tested, the arithmetic has to
be ruled out: a book whose CAGR-to-drawdown exchange rate is low everywhere will price EVERY
instrument low, insurance and de-grossing alike, without anything about the instrument
changing.  Idea 97 already computes that reference (`lever` = the static-gross ladder slope on
the same panel/book/cost), so hypothesis H0 below is testable from the committed CSV and is
declared as having been formed by reading it.

Hypotheses
    H0  UNITS (added here, formed after reading idea 97's committed `lever` column, before any
        new number was computed).  The small panel's cheap price is mostly the panel's own
        cheap lever: rate/lever is much closer across panels than rate is.
    H1  DEPTH (queue).  The control drawdown is -30.8% on small vs ~-17% on u56, and a control
        that falls further gives an instrument more room to buy drawdown cheaply.  Test by
        re-pricing every panel at MATCHED control depth via the static-gross dial.
    H2  SINGLE-NAME VOL (queue).  Test by splitting the small panel into low- and high-vol
        halves and re-pricing inside each.
    H3  FIRING RATE / ABSORBING STATE (queue, idea 93).  Test by measuring episodes, armed-day
        fraction and mean episode length in every cell and correlating them with the price.

Harness.  idea 94's module is IMPORTED, not re-implemented (`targets`, `run`, `price`,
`ladder_slope`, `matched_dd`), so every number is produced by the simulator that generated the
published price list; idea 97's panel construction is reproduced verbatim.  Test A reproduces
idea 97's 36 committed ddctl rows before anything new is read.

Book / arms.  Books V1u (composite/sqrt(vol20), top 5 @ 15%), TOP20 (composite, top 20 @
3.75%), EWall (equal-weight every name at 75% gross); weekly, next-day execution, long-only;
costs 10 and 25 bps.  The DD control: at each weekly rebalance, if net equity through t-1 is
more than D below its running high, hold k x target until the reset condition; `recover` resets
at -D/2, `high` resets at a new high.

Tuned parameters (PROTOCOL rule 4): TWO — D in {0.05,0.08,0.12} and k in {0.50,0.25}.  Reset
is FIXED at `recover` for the sweep; `high` is run only at the published (0.08,0.50) point, as
part of the reproduction.  Panels, books, costs and the walk-forward split are inherited.

Tests
    A  REPRODUCTION of idea 97's committed ddctl rows (rate, dCAGR, dMaxDD), max|diff| printed.
    B  H0 — rate, lever, rate/lever, control Calmar and ladder-dominance in all 18 cells.
    C  H1 — every panel/book re-priced at matched control MaxDD (targets -15/-20/-25/-30%),
       the static-gross multiplier found by bisection on the control.
    D  H2 — the small panel split into low- and high-name-vol halves (median full-sample
       vol20, an in-sample sort used diagnostically and labelled as such), re-priced.
    E  H3 — episodes/yr, armed-day fraction, mean episode length, and their rank correlation
       with the price, pooled and within panel.
    F  PROTOCOL rules 3/4/8 — 4a and 4b for every arm, and a rule-8 walk-forward with (D,k)
       chosen on IS only (u56/broad 2009-2016, small 2010-2016) and the OOS window read once.

Pre-registered predictions (P0 from idea 97's committed CSV; P1-P4 before any new number)
    P0  mean rate/lever is within 0.5 of each other across panels while mean rate differs by
        more than 2x  (i.e. normalisation removes at least half of the panel gap).
    P1  at matched control depth the panel spread in rate falls by more than half.
    P2  inside the small panel the LOW-vol half prices dearer than the high-vol half.
    P3  Spearman(rate, armed-day fraction) < 0 pooled: an instrument that fires more is cheaper.
    P4  no ddctl arm passes 4b on the small panel.

SURVIVORSHIP.  All three panels are current-constituent lists; the small panel's bias is the
largest and one-directional (the delisted, bankrupted and acquired names are missing, and they
are the beaten-down cohort).  Levels on the small panel are overstated.  This run compares
RATIOS measured inside each panel, which is the comparison the bias distorts least, but the
small-panel drawdowns are still shallower than the truth and its prices therefore still
flattered.  Nothing here is quoted as an achievable return.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt and five .csv companions.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import metrics  # noqa: E402

STEM = "2026-09-05_why-ddctl-is-cheap-on-small_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I97_CSV = OUT / "2026-09-05_price-list-tier-bar_B.pricelist.csv"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

IS_END, OOS_START = H.IS_END, H.OOS_START
BOOKS, COSTS, LADDER = H.BOOKS, H.COSTS, H.LADDER
PANELS = ["u56", "broad", "small"]
DS = [0.05, 0.08, 0.12]
KS = [0.50, 0.25]
DEPTHS = [0.15, 0.20, 0.25, 0.30]

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def panel(name):
    """idea 97's construction, verbatim."""
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


def armed_stats(cut, r):
    """H3 measurables from the run's armed-state series."""
    c = cut.reindex(r.index).fillna(False).astype(bool)
    yrs = len(c) / 252
    starts = int((c & ~c.shift(1, fill_value=False)).sum())
    lens = []
    run_len = 0
    for v in c.values:
        if v:
            run_len += 1
        elif run_len:
            lens.append(run_len)
            run_len = 0
    if run_len:
        lens.append(run_len)
    return dict(armed_frac=float(c.mean()), episodes_yr=starts / yrs,
                mean_ep_days=float(np.mean(lens)) if lens else 0.0,
                max_ep_days=float(np.max(lens)) if lens else 0.0,
                ends_armed=bool(c.iloc[-1]))


def main():
    say(f"[setup] panels {PANELS} | books {BOOKS} | costs {COSTS} | D {DS} | k {KS} "
        f"| reset=recover (sweep) + high (reproduction only)")

    data, prices, ladders, cells, rets = {}, {}, {}, [], {}
    for pn in PANELS:
        px, spy, label = panel(pn)
        prices[pn] = (px, spy, label)
        say(f"[panel] {pn}: {label} {px.shape} {px.index[0].date()} -> {px.index[-1].date()}")

    # ------------------------------------------------ main cells: control, ladder, arms ----
    for pn in PANELS:
        px, spy, _ = prices[pn]
        v1 = H.run(px, rules_v1_weights(px.drop(columns=["SPY"], errors="ignore"))
                   .reindex(columns=px.columns).fillna(0.0))["r"]
        for b in BOOKS:
            W = H.targets(px, b)
            for c in COSTS:
                ctl = H.run(px, W, bps=c)
                start = px.index[260]
                rc = ctl["r"].loc[start:]
                lad = []
                for m_ in LADDER:
                    rm = H.run(px, W, m=float(m_), bps=c)["r"].loc[start:]
                    mm = metrics(rm)
                    lad.append(dict(m=m_, CAGR=mm["CAGR"], MaxDD=mm["MaxDD"], Sharpe=mm["Sharpe"]))
                L = pd.DataFrame(lad)
                ladders[(pn, b, c)] = L
                lever = H.ladder_slope(L)
                mc = metrics(rc)
                bars = H.bars_of(spy.loc[start:])
                base = v1.loc[start:]
                for D in DS:
                    for k in KS:
                        for reset in (["recover", "high"] if (D == 0.08 and k == 0.50) else ["recover"]):
                            a = H.run(px, W, D=D, k=k, reset=reset, bps=c)
                            ra = a["r"].loc[start:]
                            p = H.price(rc, ra, lever)
                            ma = metrics(ra)
                            h1, h2 = H.halves(ra)
                            mo = metrics(ra.loc[OOS_START:])
                            mi = metrics(ra.loc[:IS_END])
                            row = dict(panel=pn, book=b, cost=c, D=D, k=k, reset=reset,
                                       CAGR=ma["CAGR"], Sharpe=ma["Sharpe"], MaxDD=ma["MaxDD"],
                                       H1=h1, H2=h2, IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                       ctl_CAGR=mc["CAGR"], ctl_MaxDD=mc["MaxDD"],
                                       ctl_Calmar=mc["CAGR"] / abs(mc["MaxDD"]),
                                       lever=lever, **p,
                                       matched_ladder_CAGR=H.matched_dd(L, ma["MaxDD"]),
                                       episodes=a["episodes"], **armed_stats(a["cut"], ra),
                                       gross=float(a["gross"].loc[start:].mean()),
                                       pass4a=H.pass4a(ra, base),
                                       **{f"m_{kk}": vv for kk, vv in H.margins(ra, bars).items()})
                            row["rate_over_lever"] = row["rate"] / lever if lever else np.nan
                            row["ladder_beats_arm"] = (np.isfinite(row["matched_ladder_CAGR"])
                                                       and row["matched_ladder_CAGR"] > ma["CAGR"])
                            row["pass4b"] = bool(row["m_H1"] > 0 and row["m_H2"] > 0 and row["m_OOS"] > 0
                                                 and row["m_DD"] > 0 and row["m_CAGR"] > 0)
                            cells.append(row)
                            rets[(pn, b, c, D, k, reset)] = ra
    G = pd.DataFrame(cells)
    G.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    say(f"\n[grid] {len(G)} arm-points written to {STEM}.cells.csv "
        f"({len(PANELS)} panels x {len(BOOKS)} books x {len(COSTS)} costs x "
        f"[{len(DS)}x{len(KS)} recover + 1 high]) | 4a {int(G.pass4a.sum())} | 4b {int(G.pass4b.sum())}")

    # ---------------------------------------------------------------- A: reproduction ----
    say("\n[A] REPRODUCTION of idea 97's committed ddctl rows (D=0.08, k=0.50):")
    ref = pd.read_csv(I97_CSV)
    ref = ref[ref.arm.str.startswith("ddctl")].copy()
    ref["reset"] = ref.arm.str.split("/").str[-1]
    mine = G[(G.D == 0.08) & (G.k == 0.50)]
    diffs = []
    for _, x in ref.iterrows():
        m = mine[(mine.panel == x.panel) & (mine.book == x.book) & (mine.cost == x.cost)
                 & (mine.reset == x.reset)]
        if len(m) != 1:
            say(f"    MISSING {x.panel}/{x.book}/{x.cost}/{x.reset}")
            continue
        m = m.iloc[0]
        diffs.append(dict(panel=x.panel, book=x.book, cost=x.cost, reset=x.reset,
                          d_rate=abs(m.rate - x.rate) if np.isfinite(x.rate) else np.nan,
                          d_dCAGR=abs(m.dCAGR - x.dCAGR), d_dMaxDD=abs(m.dMaxDD - x.dMaxDD),
                          d_lever=abs(m.lever - x.lever)))
    Dd = pd.DataFrame(diffs)
    Dd.to_csv(OUT / f"{STEM}.reproduction.csv", index=False)
    say(f"    {len(Dd)} rows matched | max|d rate| {Dd.d_rate.max():.3e} | "
        f"max|d dCAGR| {Dd.d_dCAGR.max():.3e} | max|d dMaxDD| {Dd.d_dMaxDD.max():.3e} | "
        f"max|d lever| {Dd.d_lever.max():.3e}")

    # ---------------------------------------------------------------- B: H0 units ----
    say("\n[B] H0 — is the cheap price a cheap LEVER?  (all 18 cells at the published D/k, "
        "reset=recover)")
    say(f"    {'panel':>6} {'book':>6} {'cost':>5} {'ctlCAGR':>8} {'ctlDD':>7} {'Calmar':>7} "
        f"{'lever':>6} {'rate':>6} {'r/lev':>6} {'ladder>arm':>10}")
    pub = G[(G.D == 0.08) & (G.k == 0.50) & (G.reset == "recover")]
    for _, x in pub.iterrows():
        say(f"    {x.panel:>6} {x.book:>6} {x.cost:>5.0f} {x.ctl_CAGR:>8.2%} {x.ctl_MaxDD:>7.1%} "
            f"{x.ctl_Calmar:>7.3f} {x.lever:>6.3f} {x.rate:>6.3f} {x.rate_over_lever:>6.3f} "
            f"{str(x.ladder_beats_arm):>10}")
    say("    panel means over ALL sweep arms (D x k, reset=recover):")
    sw = G[G.reset == "recover"]
    for pn in PANELS:
        s = sw[sw.panel == pn]
        say(f"      {pn:>6}: rate {s.rate.mean():.3f} (min {s.rate.min():.3f} max {s.rate.max():.3f}) "
            f"| lever {s.lever.mean():.3f} | rate/lever {s.rate_over_lever.mean():.3f} "
            f"| ctl Calmar {s.ctl_Calmar.mean():.3f} | ladder beats arm in "
            f"{int(s.ladder_beats_arm.sum())}/{len(s)}")
    r_ratio = sw.groupby("panel").rate.mean()
    n_ratio = sw.groupby("panel").rate_over_lever.mean()
    say(f"    panel spread: rate max/min = {r_ratio.max()/r_ratio.min():.2f}x ; "
        f"rate/lever max/min = {n_ratio.max()/n_ratio.min():.2f}x ; "
        f"Spearman(rate, lever) over {len(sw)} arms = {H.spearman(sw.rate, sw.lever):.3f} ; "
        f"Spearman(rate, ctl Calmar) = {H.spearman(sw.rate, sw.ctl_Calmar):.3f}")

    # ---------------------------------------------------------------- C: H1 depth ----
    say("\n[C] H1 — every panel re-priced at MATCHED control drawdown (static-gross bisection "
        "on the control; the arm runs at the same gross)")
    say(f"    {'panel':>6} {'book':>6} {'targetDD':>9} {'m':>6} {'ctlDD':>7} {'ctlCAGR':>8} "
        f"{'lever':>6} {'rate':>6} {'r/lev':>6}")
    drows = []
    for pn in PANELS:
        px, spy, _ = prices[pn]
        start = px.index[260]
        for b in BOOKS:
            W = H.targets(px, b)
            L = ladders[(pn, b, 10.0)]
            for tgt in DEPTHS:
                lo, hi = 0.05, 1.0
                m_ = np.nan
                base_dd = abs(metrics(H.run(px, W, m=1.0, bps=10.0)["r"].loc[start:])["MaxDD"])
                if base_dd < tgt:
                    drows.append(dict(panel=pn, book=b, target_dd=tgt, m=np.nan, note="unreachable"))
                    continue
                for _ in range(14):
                    m_ = 0.5 * (lo + hi)
                    dd = abs(metrics(H.run(px, W, m=m_, bps=10.0)["r"].loc[start:])["MaxDD"])
                    if dd > tgt:
                        hi = m_
                    else:
                        lo = m_
                rc = H.run(px, W, m=m_, bps=10.0)["r"].loc[start:]
                ra = H.run(px, W, m=m_, D=0.08, k=0.50, reset="recover", bps=10.0)["r"].loc[start:]
                # lever at this gross: slope of the ladder BELOW m_ (scaling further down)
                lad2 = []
                for f in (0.25, 0.50, 0.75, 1.00):
                    rm = H.run(px, W, m=m_ * f, bps=10.0)["r"].loc[start:]
                    mm = metrics(rm)
                    lad2.append(dict(m=m_ * f, CAGR=mm["CAGR"], MaxDD=mm["MaxDD"]))
                lev2 = H.ladder_slope(pd.DataFrame(lad2))
                p = H.price(rc, ra, lev2)
                mc = metrics(rc)
                row = dict(panel=pn, book=b, target_dd=tgt, m=m_, ctl_MaxDD=mc["MaxDD"],
                           ctl_CAGR=mc["CAGR"], lever=lev2, **p,
                           rate_over_lever=p["rate"] / lev2 if lev2 else np.nan, note="")
                drows.append(row)
                say(f"    {pn:>6} {b:>6} {tgt:>9.0%} {m_:>6.3f} {mc['MaxDD']:>7.1%} "
                    f"{mc['CAGR']:>8.2%} {lev2:>6.3f} "
                    f"{p['rate'] if np.isfinite(p['rate']) else float('nan'):>6.3f} "
                    f"{row['rate_over_lever'] if np.isfinite(row['rate_over_lever']) else float('nan'):>6.3f}")
    DM = pd.DataFrame(drows)
    DM.to_csv(OUT / f"{STEM}.depthmatched.csv", index=False)
    ok = DM[DM.note == ""].dropna(subset=["rate"])
    if len(ok):
        say("    matched-depth panel means (pooled over books and depth targets):")
        for pn in PANELS:
            s = ok[ok.panel == pn]
            if len(s):
                say(f"      {pn:>6}: rate {s.rate.mean():.3f} over {len(s)} points | "
                    f"lever {s.lever.mean():.3f} | rate/lever {s.rate_over_lever.mean():.3f}")
        md_rate = ok.groupby("panel").rate.mean()
        say(f"    matched-depth spread: rate max/min = {md_rate.max()/md_rate.min():.2f}x "
            f"(unmatched {r_ratio.max()/r_ratio.min():.2f}x) | cheapest panel unmatched "
            f"'{r_ratio.idxmin()}' -> matched '{md_rate.idxmin()}'")

    # ---------------------------------------------------------------- D: H2 name vol ----
    say("\n[D] H2 — small panel split by single-name vol (median full-sample vol20; an "
        "in-sample sort, diagnostic only)")
    pxs, spys, _ = prices["small"]
    nv = H.vol20(pxs).mean()
    med = nv.median()
    halves_ = {"lowvol": [c for c in pxs.columns if nv[c] <= med],
               "highvol": [c for c in pxs.columns if nv[c] > med]}
    say(f"    small panel median name vol20 {med:.3f} | "
        f"low half n={len(halves_['lowvol'])} mean vol {nv[halves_['lowvol']].mean():.3f} | "
        f"high half n={len(halves_['highvol'])} mean vol {nv[halves_['highvol']].mean():.3f}")
    for pn in ("u56", "broad"):
        px_, _, _ = prices[pn]
        say(f"    reference: {pn} mean name vol20 {H.vol20(px_).mean().mean():.3f}")
    vrows = []
    say(f"    {'half':>8} {'book':>6} {'ctlCAGR':>8} {'ctlDD':>7} {'lever':>6} {'rate':>6} {'r/lev':>6}")
    for hn, cols in halves_.items():
        sub = pxs[cols]
        start = sub.index[260]
        for b in BOOKS:
            W = H.targets(sub, b)
            rc = H.run(sub, W, bps=10.0)["r"].loc[start:]
            lad = []
            for m_ in LADDER:
                mv = metrics(H.run(sub, W, m=float(m_), bps=10.0)["r"].loc[start:])
                lad.append(dict(m=m_, CAGR=mv["CAGR"], MaxDD=mv["MaxDD"]))
            lev = H.ladder_slope(pd.DataFrame(lad))
            ra = H.run(sub, W, D=0.08, k=0.50, reset="recover", bps=10.0)["r"].loc[start:]
            p = H.price(rc, ra, lev)
            mc = metrics(rc)
            v = dict(half=hn, book=b, n_names=len(cols), mean_name_vol=float(nv[cols].mean()),
                     ctl_CAGR=mc["CAGR"], ctl_MaxDD=mc["MaxDD"], lever=lev, **p,
                     rate_over_lever=p["rate"] / lev if lev else np.nan)
            vrows.append(v)
            say(f"    {hn:>8} {b:>6} {mc['CAGR']:>8.2%} {mc['MaxDD']:>7.1%} {lev:>6.3f} "
                f"{p['rate']:>6.3f} {v['rate_over_lever']:>6.3f}")
    V = pd.DataFrame(vrows)
    V.to_csv(OUT / f"{STEM}.volsplit.csv", index=False)

    # ---------------------------------------------------------------- E: H3 firing ----
    say("\n[E] H3 — firing / absorbing state (sweep arms, reset=recover)")
    say(f"    {'panel':>6}: {'armed%':>7} {'eps/yr':>7} {'mean ep d':>9} {'max ep d':>8} "
        f"{'ends armed':>10} {'rate':>6}")
    for pn in PANELS:
        s = sw[sw.panel == pn]
        say(f"    {pn:>6}: {100*s.armed_frac.mean():>6.1f}% {s.episodes_yr.mean():>7.2f} "
            f"{s.mean_ep_days.mean():>9.1f} {s.max_ep_days.max():>8.0f} "
            f"{int(s.ends_armed.sum()):>4}/{len(s):<5} {s.rate.mean():>6.3f}")
    say(f"    pooled Spearman(rate, armed_frac) = {H.spearman(sw.rate, sw.armed_frac):.3f} | "
        f"(rate, episodes/yr) = {H.spearman(sw.rate, sw.episodes_yr):.3f} | "
        f"(rate, mean episode days) = {H.spearman(sw.rate, sw.mean_ep_days):.3f}")
    for pn in PANELS:
        s = sw[sw.panel == pn]
        say(f"      within {pn:>6}: Spearman(rate, armed_frac) = {H.spearman(s.rate, s.armed_frac):.3f} "
            f"| (rate/lever, armed_frac) = {H.spearman(s.rate_over_lever, s.armed_frac):.3f}")

    # ---------------------------------------------------------------- F: protocol ----
    say("\n[F] PROTOCOL rule 8 walk-forward — (D,k) chosen on IS by IS Sharpe, per panel/book/cost; "
        "OOS read once")
    say(f"    {'panel':>6} {'book':>6} {'cost':>5} {'pick':>12} {'IS Shrp':>8} {'OOS CAGR':>9} "
        f"{'OOS Shrp':>9} {'OOS DD':>8} {'ctl OOS Shrp':>12} {'SPY OOS Shrp':>12} {'4a':>5} {'4b':>5}")
    wrows = []
    for pn in PANELS:
        px, spy, _ = prices[pn]
        start = px.index[260]
        spy_o = metrics(spy.loc[OOS_START:])
        for b in BOOKS:
            W = H.targets(px, b)
            for c in COSTS:
                ctl_o = metrics(H.run(px, W, bps=c)["r"].loc[OOS_START:])
                f = sw[(sw.panel == pn) & (sw.book == b) & (sw.cost == c)]
                p = f.loc[f.IS_Sharpe.idxmax()]
                say(f"    {pn:>6} {b:>6} {c:>5.0f} {'D=%.2f k=%.2f' % (p.D, p.k):>12} "
                    f"{p.IS_Sharpe:>8.3f} {p.OOS_CAGR:>9.2%} {p.OOS_Sharpe:>9.3f} {p.OOS_MaxDD:>8.1%} "
                    f"{ctl_o['Sharpe']:>12.3f} {spy_o['Sharpe']:>12.3f} {str(p.pass4a):>5} {str(p.pass4b):>5}")
                wrows.append(dict(panel=pn, book=b, cost=c, D=p.D, k=p.k, IS_Sharpe=p.IS_Sharpe,
                                  OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                                  ctl_OOS_Sharpe=ctl_o["Sharpe"], ctl_OOS_CAGR=ctl_o["CAGR"],
                                  SPY_OOS_Sharpe=spy_o["Sharpe"], SPY_OOS_CAGR=spy_o["CAGR"],
                                  pass4a=p.pass4a, pass4b=p.pass4b))
    pd.DataFrame(wrows).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- predictions ----
    say("\n[P] pre-registered predictions vs outcome")
    say(f"    P0 normalisation removes >= half the panel gap: rate spread {r_ratio.max()/r_ratio.min():.2f}x "
        f"-> rate/lever spread {n_ratio.max()/n_ratio.min():.2f}x -> "
        f"{'CONFIRMED' if (n_ratio.max()/n_ratio.min()) <= 0.5*(r_ratio.max()/r_ratio.min()) else 'REFUTED'}")
    say(f"       [supplementary, NOT the pre-registered test] spread measured as excess over 1.0: "
        f"{(r_ratio.max()/r_ratio.min())-1:.2f} -> {(n_ratio.max()/n_ratio.min())-1:.2f} "
        f"({100*(1-((n_ratio.max()/n_ratio.min())-1)/((r_ratio.max()/r_ratio.min())-1)):.0f}% removed)")
    if len(ok):
        say(f"    P1 matched-depth spread falls by >half: {md_rate.max()/md_rate.min():.2f}x vs "
            f"{r_ratio.max()/r_ratio.min():.2f}x -> "
            f"{'CONFIRMED' if (md_rate.max()/md_rate.min()) <= 0.5*(r_ratio.max()/r_ratio.min()) else 'REFUTED'}"
            f" | but the ORDERING inverts: cheapest panel unmatched '{r_ratio.idxmin()}', "
            f"matched '{md_rate.idxmin()}' (small rate {r_ratio['small']:.3f} -> {md_rate['small']:.3f})")
    lo_, hi_ = V[V.half == "lowvol"].rate.mean(), V[V.half == "highvol"].rate.mean()
    say(f"    P2 low-vol half dearer: {lo_:.3f} vs high-vol {hi_:.3f} -> "
        f"{'CONFIRMED' if lo_ > hi_ else 'REFUTED'}"
        f" | lever-normalised r/lev {V[V.half=='lowvol'].rate_over_lever.mean():.3f} vs "
        f"{V[V.half=='highvol'].rate_over_lever.mean():.3f} (reported, not the pre-registered test)")
    sp = H.spearman(sw.rate, sw.armed_frac)
    say(f"    P3 Spearman(rate, armed_frac) < 0: {sp:.3f} -> {'CONFIRMED' if sp < 0 else 'REFUTED'}")
    n4b = int(G[(G.panel == 'small')].pass4b.sum())
    say(f"    P4 no small-panel 4b pass: {n4b} -> {'CONFIRMED' if n4b == 0 else 'REFUTED'}"
        f" | 4b passes elsewhere: " + ", ".join(
            f"{x.panel}/{x.book}/{x.cost:.0f}bp D={x.D:.2f} k={x.k:.2f}"
            for _, x in G[G.pass4b].iterrows()) or " none")
    say(f"    [decisive control] the static-gross ladder beats the DD arm at MATCHED drawdown in "
        f"{int(G[G.reset=='recover'].ladder_beats_arm.sum())}/{len(G[G.reset=='recover'])} sweep arms "
        f"(small {int(sw[sw.panel=='small'].ladder_beats_arm.sum())}/{len(sw[sw.panel=='small'])}): "
        f"cheap is not the same as worth buying.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
