#!/usr/bin/env python3
"""QUEUE idea 6 — defensive-sleeve (cloud lane, 2026-09-04).

Question
--------
Every book the project runs holds 25% cash by construction (75% gross).  Idea 6 asks
whether that cash should stop being cash when the market is broadly broken: when breadth
(% of the universe above its 200d MA) falls below B, move the cash sleeve into the best
of TLT / GLD / SHY by L-day momentum.  If the defensive sleeve is real, it should show up
as drawdown relief in 2020 and 2022 that is not paid for in full elsewhere — which is
exactly what 4b's drawdown cap rewards and what the two standing candidates (idea 2's
top20, idea 57's ew-band3) have the least margin on.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json via load_universe() (56 names), plus the full grid
           re-run on universe_broad.json (136 names).  TLT, GLD and SHY are present in
           both lists.
Books    : (a) RULES v1 live (top-5 risk-adjusted, 15% each) — the idea as written;
           (b) idea 2's 4b KEEP-candidate — top-20 by the v1 composite WITHOUT
               /sqrt(vol20), equal weight 0.75/20, which also runs 25% cash.
Overlay  : breadth E_t = share of panel names (EXCLUDING the three sleeve assets) whose
           close is above their own 200d MA, measured at close t with the rest of the
           weights.  If E_t < B, the residual cash (1 - book gross) goes into
           argmax(L-day return) over {TLT, GLD, SHY}; otherwise it stays cash.
Params   : exactly 2 — B in {30,40,50,60}% and L in {63,126} days = 8 points per book per
           universe, all reported, plus the two grid endpoints as controls: B=0 (never on,
           i.e. the plain book) and B=100 (always on, the unconditional sleeve).
Controls : at the idea's own pre-registered setting (B=40, L=63), three sleeve
           definitions — best-of-3, equal-weight-of-3, SHY-only — so that any gain can be
           attributed to the breadth trigger vs the asset selection vs simply not being
           in cash.  Also a cap-at-25% variant, since the residual cash can exceed 25%
           when fewer than n names are eligible.
Execution: weekly rebalance, weights decided at close t applied at t+1, 10 bps per unit
           turnover on the whole book including the sleeve.
Rule 8   : (B, L) chosen on 2009-2016 only under two selection rules fixed in advance
           (plain IS Sharpe; 4b-aware IS Sharpe subject to the IS 4b bars), evaluated
           untouched on 2017-2026.

SURVIVORSHIP: both lists are current constituents, so absolute CAGRs are optimistic.
The overlay-vs-plain comparison holds names, days and gross fixed and is far less
exposed — the sleeve assets are three ETFs that existed throughout.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

COST = 10
FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
SLEEVE = ["TLT", "GLD", "SHY"]
BS = [30, 40, 50, 60]
LS = [63, 126]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SCRIPT = "research/backtests/2026-09-04_defensive-sleeve_cloud.py"


# ---------------------------------------------------------------- construction
def composite(px):
    """v1's rank blend WITHOUT the /sqrt(vol20) term (idea 2's candidate scorer)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def eligible(px):
    return (px > px.rolling(200).mean()) & (vol20(px) < MAX_VOL)


def book_v1(px):
    return rules_v1_weights(px)


def book_top20(px):
    rank = composite(px).where(eligible(px)).rank(axis=1, ascending=False)
    return (rank <= 20).astype(float) * (GROSS / 20)


BOOKS = {"v1": book_v1, "top20": book_top20}


def breadth(px):
    """% of panel names above their own 200d MA, excluding the three sleeve assets."""
    cols = [c for c in px.columns if c not in SLEEVE]
    a = (px[cols] > px[cols].rolling(200).mean())
    return a.sum(axis=1) / len(cols) * 100.0


def sleeve_weights(px, kind, L):
    """One-hot (or equal-weight) sleeve allocation, per day, on the sleeve assets."""
    s = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    if kind == "shy":
        s["SHY"] = 1.0
        return s
    if kind == "ew3":
        for t in SLEEVE:
            s[t] = 1.0 / 3
        return s
    r = px[SLEEVE] / px[SLEEVE].shift(L) - 1          # L-day momentum, known at close t
    good = r.notna().all(axis=1)
    pick = r.loc[good].idxmax(axis=1)                   # warm-up rows stay in cash
    for t in SLEEVE:
        s.loc[good, t] = (pick == t).astype(float)
    return s


def overlay(book_fn, B, L, kind="best3", cap=None):
    """Book + defensive sleeve on the residual cash whenever breadth < B."""
    def f(px):
        w = book_fn(px)
        if B <= 0:
            return w
        cash = (1.0 - w.sum(axis=1)).clip(lower=0.0)
        if cap is not None:
            cash = cash.clip(upper=cap)
        on = (breadth(px) < B).astype(float)
        return w + sleeve_weights(px, kind, L).mul(cash * on, axis=0)
    return f


# ---------------------------------------------------------------- metrics
def m(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, s, dd = m(r); h1, h2 = halves(r)
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m(r); h1, h2 = halves(r)
    _, _, bdd = m(base); b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def run(px, fn, start, cost=COST):
    res = backtest(px, fn(px), cost_bps=cost, freq=FREQ)
    r = res["returns"].loc[start:]
    return r, res["turnover"].loc[start:].sum() / (len(r) / 252)


# ---------------------------------------------------------------- one universe
def sweep(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    sc, ss, sdd = m(spy); s1, s2 = halves(spy)
    _, ss_o, _ = m(spy.loc[OOS_START:])

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — results not comparable. Aborting.")

    print(f"\n{'=' * 126}")
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
          f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    print(f"SPY {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} OOS Sharpe {ss_o:.3f}  |  "
          f"RULES v1 {m(base)[0]:.1%}/{m(base)[1]:.3f}/{m(base)[2]:.1%}")
    print(f"4b bars: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{ss_o:.3f}  MaxDD>={0.60 * sdd:.1%}  "
          f"CAGR>={0.70 * sc:.1%}")
    print("=" * 126)

    # how often would the trigger be on, and what does it pick?
    E = breadth(px).loc[start:]
    print(f"\nBreadth E_t (share of {px.shape[1] - len(SLEEVE)} non-sleeve names above 200d): "
          f"mean {E.mean():.1f}%  median {E.median():.1f}%  min {E.min():.1f}%  max {E.max():.1f}%")
    for B in BS:
        on = (E < B)
        yr = on.groupby(on.index.year).mean()
        worst = ", ".join(f"{y} {v:.0%}" for y, v in yr.sort_values(ascending=False).head(4).items())
        print(f"  B={B}%  days on {on.mean():6.1%}   most-on years: {worst}")
    for L in LS:
        s = sleeve_weights(px, "best3", L).loc[start:]
        share = {t: s[t].mean() for t in SLEEVE}
        print(f"  L={L}d sleeve pick share (all days): " +
              "  ".join(f"{t} {v:.0%}" for t, v in share.items()))

    grid, rows = {}, []
    for bk, bfn in BOOKS.items():
        print(f"\n--- book = {bk} ---")
        print(f"{'B':<5}{'L':<6}{'CAGR':>7}{'Sharpe':>8}{'MaxDD':>8}   {'H1':>5}/{'H2':>5}"
              f"{'OOS':>7}{'turn':>7}   verdict")
        print("-" * 126)
        for B in [0] + BS + [100]:
            for L in ([63] if B == 0 else LS):          # B=0 is the plain book; L is inert
                r, t = run(px, overlay(bfn, B, L), start)
                grid[(bk, B, L)] = (r, t)
                oos = m(r.loc[OOS_START:])[1]
                a, b = fail4a(r, base), fail4b(r, spy, oos, ss_o)
                v = ("KEEP 4a" if not a else "KILL 4a") + " / " + \
                    ("KEEP 4b" if not b else "KILL 4b (" + ",".join(b) + ")")
                c, s_, dd = m(r); h1, h2 = halves(r)
                lbl = "plain" if B == 0 else ("always" if B == 100 else f"{B}%")
                print(f"{lbl:<5}{L:<6}{c:7.1%}{s_:8.3f}{dd:8.1%}   {h1:5.3f}/{h2:5.3f}"
                      f"{oos:7.3f}{t:7.1f}x   {v}")
                rows.append((f"6 {tag} {bk} B={lbl} L={L}", c, s_, dd, h1, h2, oos, t, v))

        # overlay contribution at matched book: arm minus plain
        pc, ps, pdd = m(grid[(bk, 0, 63)][0])
        print(f"\n  Overlay contribution vs the plain {bk} book "
              f"({pc:.1%}/{ps:.3f}/{pdd:.1%}), and paired t on the daily difference:")
        for B in BS + [100]:
            for L in LS:
                r = grid[(bk, B, L)][0]
                c, s_, dd = m(r)
                d = (r - grid[(bk, 0, 63)][0]).dropna()
                t = d.mean() / d.std() * np.sqrt(len(d)) if d.std() > 0 else np.nan
                print(f"    B={B if B < 100 else 'always':<7} L={L:<4} "
                      f"{100 * (c - pc):+6.2f}pp CAGR  {s_ - ps:+.3f} Sharpe  "
                      f"{100 * (dd - pdd):+6.2f}pp MaxDD   diff {d.mean() * 252:+6.2%}/yr  t {t:+5.2f}")

        # what is the trigger worth vs the asset choice vs simply not holding cash?
        print(f"\n  Sleeve-definition controls at the idea's own setting (B=40, L=63), book {bk}:")
        for kind in ("best3", "ew3", "shy"):
            r, t = run(px, overlay(bfn, 40, 63, kind=kind), start)
            c, s_, dd = m(r); h1, h2 = halves(r)
            print(f"    sleeve={kind:<6} {c:6.1%} / {s_:.3f} / {dd:6.1%}  halves {h1:.3f}/{h2:.3f}  "
                  f"turn {t:.1f}x")
            rows.append((f"6 {tag} {bk} B=40 L=63 sleeve={kind} [ctrl]", c, s_, dd, h1, h2,
                         m(r.loc[OOS_START:])[1], t, "-"))
        r, t = run(px, overlay(bfn, 40, 63, cap=0.25), start)
        c, s_, dd = m(r); h1, h2 = halves(r)
        print(f"    cash capped at 25%   {c:6.1%} / {s_:.3f} / {dd:6.1%}  turn {t:.1f}x")
        rows.append((f"6 {tag} {bk} B=40 L=63 cash-cap-25% [ctrl]", c, s_, dd, h1, h2,
                     m(r.loc[OOS_START:])[1], t, "-"))

    return dict(grid=grid, rows=rows, spy=spy, base=base, start=start, ss_o=ss_o)


def walk_forward(res, tag):
    """PROTOCOL rule 8: choose (B, L) on 2009-2016, evaluate untouched on 2017-2026."""
    grid, spy, base = res["grid"], res["spy"], res["base"]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    sc_i, ss_i, sdd_i = m(spy_is)
    sc_o, ss_o, sdd_o = m(spy_oos)
    print(f"\nWalk-forward ({tag}): IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"  IS 4b bars: Sharpe>{ss_i:.3f}  MaxDD>={0.60 * sdd_i:.1%}  CAGR>={0.70 * sc_i:.1%}")
    print(f"  OOS SPY {sc_o:.1%}/{ss_o:.3f}/{sdd_o:.1%}  |  RULES v1 "
          f"{m(base.loc[OOS_START:])[0]:.1%}/{m(base.loc[OOS_START:])[1]:.3f}/"
          f"{m(base.loc[OOS_START:])[2]:.1%}")
    out = []
    for bk in BOOKS:
        cand = []
        for (b_, B, L), (r, t) in grid.items():
            if b_ != bk:
                continue
            c, s_, dd = m(r.loc[:IS_END])
            cand.append(dict(key=(B, L), sh=s_, cagr=c, dd=dd))
        for c in sorted(cand, key=lambda x: -x["sh"])[:4]:
            print(f"  IS  {bk:<6} B={c['key'][0]:<4} L={c['key'][1]:<4} Sharpe {c['sh']:6.3f}  "
                  f"CAGR {c['cagr']:6.1%}  MaxDD {c['dd']:6.1%}")
        picks = {"plain-Sharpe": max(cand, key=lambda x: x["sh"])["key"]}
        ok = [c for c in cand if c["sh"] > ss_i and c["dd"] >= 0.60 * sdd_i
              and c["cagr"] >= 0.70 * sc_i]
        picks["4b-aware"] = max(ok, key=lambda x: x["sh"])["key"] if ok else None
        for rule, key in picks.items():
            if key is None:
                print(f"  OOS {bk} pick[{rule}]: NOTHING — no in-sample point met the 4b bars")
                out.append((f"6 {tag} {bk} walk-forward {rule}: picks NOTHING", None))
                continue
            c, s_, dd = m(grid[(bk, key[0], key[1])][0].loc[OOS_START:])
            flag = "beats SPY OOS" if s_ > ss_o else "loses to SPY OOS"
            pass4b = "clears" if (s_ > ss_o and dd >= 0.60 * sdd_o and c >= 0.70 * sc_o) else "misses"
            sel = "plain book" if key[0] == 0 else f"B={key[0]} L={key[1]}"
            print(f"  OOS {bk} pick[{rule}] = {sel}: {c:.1%}/{s_:.3f}/{dd:.1%}  "
                  f"({flag}; {pass4b} the OOS 4b bars)")
            out.append((f"6 {tag} {bk} walk-forward {rule}: {sel} OOS", (c, s_, dd, flag)))
    return out


def years(res, tag):
    print(f"\nCalendar-year returns ({tag}) — plain book vs B=40/L=63 overlay, vs SPY:")
    spy = res["spy"]
    d = {"SPY": spy.groupby(spy.index.year).apply(lambda x: (1 + x).prod() - 1)}
    for bk in BOOKS:
        for B, lbl in ((0, "plain"), (40, "B40")):
            r = res["grid"][(bk, B, 63)][0]
            d[f"{bk}-{lbl}"] = r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
    print(pd.DataFrame(d).to_string(float_format=lambda x: f"{x:+.1%}"))


# ---------------------------------------------------------------- main
def main():
    print("=" * 126)
    print(f"Idea 6 defensive-sleeve (cloud) | {SCRIPT}")
    print("Grid: B in {30,40,50,60}% x L in {63,126}d = 8 points per book per universe, "
          "plus B=0 (plain) and B=100 (always) controls. 2 tuned params. All points reported.")
    print("=" * 126)

    px = load_universe()

    # ---- harness sanity: the plain top20 book must reproduce idea 2's KEEP row
    start = px.index[260]
    r20, _ = run(px, book_top20, start)
    c, s_, dd = m(r20); h1, h2 = halves(r20)
    print(f"\nHARNESS CHECK  plain top20 -> {c:.1%}/{s_:.3f}/{dd:.1%} halves {h1:.3f}/{h2:.3f}"
          f"   (idea 2's KEEP row: 12.7%/1.093/-18.3%, halves 1.088/1.103)")
    ok = abs(c - 0.127) < 0.002 and abs(s_ - 1.093) < 0.01 and abs(dd + 0.183) < 0.005
    print(f"HARNESS CHECK  {'PASS' if ok else '*** MISMATCH ***'}")

    main_res = sweep(px, "universe.json")
    wf_main = walk_forward(main_res, "universe.json")
    years(main_res, "universe.json")

    pxb = load_universe(broad=True)
    broad_res = sweep(pxb, "universe_broad.json")
    wf_broad = walk_forward(broad_res, "universe_broad.json")
    years(broad_res, "universe_broad.json")

    # ---- leaderboard
    bl = m(main_res["base"]); b1, b2 = halves(main_res["base"])
    print("\nLEADERBOARD rows:")
    for tagrows in (main_res["rows"], broad_res["rows"]):
        for lbl, c, s_, dd, h1, h2, oos, t, v in tagrows:
            print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
                  f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {v} | {SCRIPT} |")
    for lbl, r in [("6 SPY buy & hold (universe.json sample) - reference", main_res["spy"]),
                   ("6 RULES v1 live (universe.json) - baseline", main_res["base"])]:
        c, s_, dd = m(r); h1, h2 = halves(r)
        print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | {h1:.2f} / {h2:.2f} | "
              f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | - | {SCRIPT} |")
    for lbl, v in wf_main + wf_broad:
        if v is None:
            print(f"| 2026-09-04 | {lbl} | - | - | - | - / - | {bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | "
                  f"no IS point met the 4b bars | {SCRIPT} |")
        else:
            c, s_, dd, flag = v
            print(f"| 2026-09-04 | {lbl} | {c:.1%} | {s_:.2f} | {dd:.1%} | - / - | "
                  f"{bl[1]:.2f} ({b1:.2f}/{b2:.2f}) | {flag} | {SCRIPT} |")


if __name__ == "__main__":
    main()
