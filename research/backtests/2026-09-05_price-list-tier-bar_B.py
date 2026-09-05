#!/usr/bin/env python3
"""QUEUE idea 97 — price-list-tier-bar (lane B, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 94's tier ordering (per-name gate < static gross lever < book-level DD rule < stop)
survives out of sample while the per-instrument prices do not (median Spearman 0.44, S1
rank-1 in 5/12).  Propose the TIER statement as what PROTOCOL quotes when a drawdown budget
is set, with the numeric price explicitly marked unstable, and re-check the tiers on the
small-cap panel where the 200d gate is known to invert (ideas 38/49/51)."

What is on trial.  Not a book — a SENTENCE that PROTOCOL would quote.  The candidate wording
is idea 94's closing claim, restated as three falsifiable pairwise inequalities on the price
axis of idea 74 (pp of CAGR surrendered per pp of MaxDD bought, same base book, same days):

    C1  per-name gate      <  static gross lever      (a rule beats simply holding less)
    C2  static gross lever <  book-level DD rule      (reacting to your own equity is dearer)
    C3  book-level DD rule <  per-name trailing stop  (the stop is dearest / not insurance)

A sentence is quotable only if it is (i) true in most cells, (ii) more stable out of sample
and across panels than the per-instrument numbers it replaces, and (iii) does not invert on a
panel where the underlying instrument is known to behave differently.  (iii) is the whole
point of the small-cap re-check: ideas 38/49/51 found the 200d gate COSTS 5.4 pp/yr of CAGR at
zero drawdown benefit on the sub-$2B panel, i.e. the leading member of tier 1 is inverted
there.  If C1 survives that, the tier statement is panel-invariant; if it does not, PROTOCOL
must carry a universe clause.

Harness.  This run does NOT re-implement idea 94.  It imports that script's module directly
(`targets`, `run`, `price`, `ladder_slope`, `arm_specs`, the gate definitions) so every number
below is produced by the identical simulator, and asserts reproduction of two published rows
before anything else runs.  Only the panel set, the tier layer and the selectors are new.

Panels (3, all reported)
    u56    research/universe.json         (56 names)   — idea 94's primary
    broad  research/universe_broad.json   (136 names)  — idea 94's second
    small  data/prices_small.csv.gz       (439 names)  — NEW.  SPY held out as benchmark and
           the 44 names with max_1d_move >= 1.0 in data/small_meta.csv dropped, which is the
           convention of every other small-panel run in this project.  Trading-day indexed and
           starting 2010-01-04, so its IS window is 2010-2016, not 2009-2016.

Books (idea 94's, unchanged, all ungated at 75% gross): V1u, TOP20, EWall.
Costs 10 and 25 bps.  3 x 3 x 2 = 18 cells; 17 arms + a 19-point gross ladder per cell.

Tiers (pre-registered mapping, fixed before any number was read)
    T1 per-name gate      g200/band3/abs12/vol60/v1gate, both -dg and -rw conventions (10 arms)
    T2 static gross lever the ladder slope itself — the REFERENCE price, not an arm
    T3 book-level DD rule ddctl-8/.5/recover, ddctl-8/.5/high                          (2 arms)
    T4 per-name stop      stop15, stop25                                               (2 arms)
    (ebud-0.10/0.20 are NOT in the statement — idea 94 showed the entry-only budget is a
     de-grossing in disguise.  Both are still priced and reported, and the claim that they sit
     at the T2 lever price is checked separately.)

Tier price = MEDIAN of the finite arm rates in the tier, in that cell.  An arm that bought
less than 0.10 pp of MaxDD has no meaningful price (idea 94's convention) and is dropped from
the median; a tier with NO priceable arm is "unpriceable" and, pre-registered, ranks LAST —
an instrument that buys no drawdown is not insurance at any price.

Tuned parameters (PROTOCOL rule 4): ONE — the instrument family (equivalently the tier) in
the walk-forward selector.  Every setting inside a family is inherited from idea 94 and
reported, never chosen.

Walk-forward (PROTOCOL rule 8), both selectors fixed before any OOS number was read
    S1     idea 94's: among arms with IS dMaxDD >= 1.0 pp and a finite IS rate, take argmin
           IS rate.  This is the per-instrument price list being used as a price list.
    Stier  among the RULE tiers {T1,T3,T4} take argmin IS tier price; inside that tier take
           the arm at the MEDIAN IS rate (index (n-1)//2 of the sorted eligible arms) — a
           deterministic, deliberately NON-extremal within-tier choice.  T2 is excluded from
           selection because the lever is the reference, not an instrument; whether the picked
           tier's IS price beats the IS lever is reported separately as the "is any rule
           warranted at all" flag.
    Regret = OOS rate of the pick minus OOS rate of the cell's OOS-cheapest eligible arm.
           Lower is better; 0.000 means the selector landed on the OOS-best arm.

Pre-registered predictions (written before any number was read)
    P1  Tier prices are more stable than instrument prices: median cross-window Spearman at
        tier level > idea 94's 0.442 at instrument level, and the same for cross-panel.
    P2  C1 (gate < lever) INVERTS on the small panel — the 200d gate's known inversion there
        (ideas 38/49/51) is strong enough to move the whole tier — while C3 (stop dearest)
        holds on all three panels.
    P3  The stop is unpriceable (dMaxDD <= 0) on the small panel too, in the majority of its
        cells: "a stop is not insurance" is the one clause that needs no universe caveat.
    P4  Stier has lower mean OOS regret than S1, because the tier is the stable object.
    P5  No arm here is a new 4b pass on all three panels (this is a measurement run; 4a/4b are
        computed and reported for every arm anyway, per PROTOCOL rule 4).

Execution realism (PROTOCOL rule 2): idea 94's simulator — weights decided at close t applied
at t+1, weekly rebalance, long-only, no leverage, costs charged inside the loop so the DD
state machine and the stop see NET equity.

SURVIVORSHIP: all three panels are current-constituent lists.  The small panel's bias is the
worst of the three and falls hardest on beaten-down names (idea 54), which is exactly the
cohort a gate excludes — so the small-panel gate price is if anything FLATTERED here.  Every
number in this run is a within-cell delta on matched days, which is far less exposed than a
level, but the small-panel conclusion should be read as a lower bound on the gate's cost.

Calendar-day index (open idea 38) is unfixed for u56/broad and affects both equally; the
small panel is trading-day indexed, which is a further reason its window differs.

Deterministic, standalone.  Imports research/baseline.py and idea 94's module; modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_price-list-tier-bar_B"
I94 = ROOT / "research" / "backtests" / "2026-09-04_drawdown-insurance-price-list_B.py"

# ---- import idea 94's harness unchanged -------------------------------------------------
_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS, BOOKS, LADDER = H.COSTS, H.BOOKS, H.LADDER
PCOST = H.PCOST

TIER = {}
for g in H.GATES:
    for conv in ("dg", "rw"):
        TIER[f"{g}-{conv}"] = "T1_gate"
TIER["ddctl-8/.5/recover"] = "T3_ddctl"
TIER["ddctl-8/.5/high"] = "T3_ddctl"
TIER["stop15"] = "T4_stop"
TIER["stop25"] = "T4_stop"
TIER["ebud-0.10"] = "X_ebud"
TIER["ebud-0.20"] = "X_ebud"
RULE_TIERS = ["T1_gate", "T3_ddctl", "T4_stop"]
ALL_TIERS = ["T1_gate", "T2_lever", "T3_ddctl", "T4_stop"]
CLAIMS = [("C1", "T1_gate", "T2_lever"), ("C2", "T2_lever", "T3_ddctl"),
          ("C3", "T3_ddctl", "T4_stop")]
BIG = 1e9          # rank value for an unpriceable tier: last, pre-registered

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)


# ---------------------------------------------------------------- panels
def panel(name):
    """(px_holdable, spy_returns_series, label).  Books may hold every column of px."""
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        spy = px["SPY"].pct_change().fillna(0.0)
        return px[inv], spy, f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def margins(r, bars):
    h1, h2 = halves(r)
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=0.60 * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - 0.70 * bars["scagr"])


def spearman(a, b):
    return H.spearman(a, b)


# ---------------------------------------------------------------- verification
def verify():
    """Reproduce two PUBLISHED idea 94 rows before trusting anything below."""
    print("=" * 200)
    print("VERIFICATION — reproducing published idea 94 numbers with the imported harness")
    px = load_universe()
    start = px.index[260]
    # engine equivalence of the control
    worst = 0.0
    for b in BOOKS:
        W = H.targets(px, b)
        a = H.run(px, W, bps=PCOST)["r"].loc[start:]
        e = backtest(px, W, cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    print(f"  engine-equivalence (control vs engine.backtest @10bps, u56): max|diff| = {worst:.3e}"
          f"  ({'EXACT' if worst < 1e-12 else 'NOT EXACT — UNSAFE'})")
    # published: EWall + vol60-dg on u56 @10bps = 11.6% / 1.133 / -16.9%, turnover 1.39x
    r = H.run(px, H.targets(px, "EWall", "vol60", "dg"), bps=10.0)["r"].loc[start:]
    m = metrics(r)
    print(f"  EWall+vol60-dg u56 @10bps: CAGR {m['CAGR']:.1%} (pub 11.6%)  "
          f"Sharpe {m['Sharpe']:.3f} (pub 1.133)  MaxDD {m['MaxDD']:.1%} (pub -16.9%)")
    # published: EWall + band3-rw on u56 @10bps = 12.2% / 1.161 / -17.7%
    r2 = H.run(px, H.targets(px, "EWall", "band3", "rw"), bps=10.0)["r"].loc[start:]
    m2 = metrics(r2)
    print(f"  EWall+band3-rw u56 @10bps: CAGR {m2['CAGR']:.1%} (pub 12.2%)  "
          f"Sharpe {m2['Sharpe']:.3f} (pub 1.161)  MaxDD {m2['MaxDD']:.1%} (pub -17.7%)")
    ok = (abs(m["Sharpe"] - 1.133) < 5e-3 and abs(m2["Sharpe"] - 1.161) < 5e-3 and worst < 1e-12)
    print(f"  -> {'REPRODUCED' if ok else 'MISMATCH — read the numbers above before believing this run'}")
    print("=" * 200)
    return ok


# ---------------------------------------------------------------- one panel
def do_panel(pname):
    px, spy_full, label = panel(pname)
    start = px.index[260]
    spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
    bars = bars_of(spy)
    ms = metrics(spy)
    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}

    print("\n" + "=" * 200)
    print(f"PANEL {pname} — {label}: {px.shape[1]} holdable names, "
          f"{px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()} | "
          f"IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"  SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS {bars['soos']:.3f}")
    print(f"  live RULES v1 @10bps: CAGR {metrics(v1_net[10.0])['CAGR']:.2%}  "
          f"Sharpe {metrics(v1_net[10.0])['Sharpe']:.3f}  MaxDD {metrics(v1_net[10.0])['MaxDD']:.2%}")
    print(f"  4b bars: Sharpe > {bars['s1']:.3f}/{bars['s2']:.3f}/{bars['soos']:.3f}, "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")

    rows, rets, ladders = [], {}, {}
    for b in BOOKS:
        for c in COSTS:
            lad = []
            for m_ in LADDER:
                res = H.run(px, H.targets(px, b), m=m_, bps=c)
                r = res["r"].loc[start:]
                mm = metrics(r)
                lad.append(dict(m=m_, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                gross=res["gross"].loc[start:].mean(),
                                TO=res["to"].loc[start:].sum() / mm["Years"],
                                IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"]))
            ladders[(b, c)] = pd.DataFrame(lad)

        for name, kind, kwargs, (g, conv) in H.arm_specs():
            W = H.targets(px, b, g, conv)
            for c in COSTS:
                res = H.run(px, W, bps=c, **kwargs)
                r = res["r"].loc[start:]
                rets[(b, name, c)] = r
                mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
                h1, h2 = halves(r)
                mg = margins(r, bars)
                yr = (1 + r).groupby(r.index.year).prod() - 1
                rows.append(dict(
                    panel=pname, book=b, arm=name, tier=TIER.get(name, "-"), kind=kind, cost=c,
                    CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                    IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    TO=res["to"].loc[start:].sum() / mm["Years"],
                    gross=res["gross"].loc[start:].mean(), stops=res["n_stops"],
                    y2020=yr.get(2020, np.nan), y2022=yr.get(2022, np.nan),
                    m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                    p4b=all(v > 0 for v in mg.values()),
                    f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-",
                    p4a=H.pass4a(r, v1_net[c])))
    df = pd.DataFrame(rows)

    print(f"\nFULL GRID {pname} — {len(df)} arm-points, ALL reported "
          f"(3 books x {len(H.arm_specs())} arms x {len(COSTS)} costs)")
    print(df[["book", "arm", "tier", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
              "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "y2020", "y2022", "p4a", "p4b", "f4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- price list (idea 94's price(), unchanged) ------------------------------------
    out = []
    for b in BOOKS:
        for c in COSTS:
            L = ladders[(b, c)]
            slope = {w: H.ladder_slope(L, f"{p}MaxDD", f"{p}CAGR")
                     for w, p in (("full", ""), ("IS", "IS_"), ("OOS", "OOS_"))}
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in H.arm_specs():
                if name == "control":
                    continue
                ra = rets[(b, name, c)]
                pf = H.price(rc, ra, slope["full"])
                pi = H.price(H.window(rc, "IS"), H.window(ra, "IS"), slope["IS"])
                po = H.price(H.window(rc, "OOS"), H.window(ra, "OOS"), slope["OOS"])
                row = df[(df.book == b) & (df.arm == name) & (df.cost == c)].iloc[0]
                out.append(dict(
                    panel=pname, book=b, cost=c, arm=name, tier=TIER.get(name, "-"), kind=kind,
                    dCAGR=pf["dCAGR"], dMaxDD=pf["dMaxDD"], rate=pf["rate"],
                    lever=slope["full"], IS_lever=slope["IS"], OOS_lever=slope["OOS"],
                    dominated=pf["dominated"], dSharpe=pf["dSharpe"], gross=row.gross, TO=row.TO,
                    IS_rate=pi["rate"], IS_dMaxDD=pi["dMaxDD"],
                    OOS_rate=po["rate"], OOS_dMaxDD=po["dMaxDD"],
                    p4a=row.p4a, p4b=row.p4b))
    P = pd.DataFrame(out)
    print(f"\nPRICE LIST {pname} — pp CAGR surrendered per pp MaxDD bought, vs the SAME base "
          f"book on the SAME days.  `lever` = static-gross reference price in that cell.")
    print(P[["book", "cost", "arm", "tier", "dCAGR", "dMaxDD", "rate", "lever", "dominated",
             "dSharpe", "TO", "IS_rate", "IS_dMaxDD", "OOS_rate", "OOS_dMaxDD", "p4a", "p4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return px, start, df, P, rets, ladders, bars, spy, v1_net


# ---------------------------------------------------------------- tier layer
def tier_prices(P):
    """One row per (panel, book, cost) x window with the 4 tier prices + ordering checks."""
    out = []
    for (pn, b, c), g in P.groupby(["panel", "book", "cost"]):
        for win, rc, lc in (("full", "rate", "lever"), ("IS", "IS_rate", "IS_lever"),
                            ("OOS", "OOS_rate", "OOS_lever")):
            d = dict(panel=pn, book=b, cost=c, window=win)
            d["T2_lever"] = float(g[lc].iloc[0])
            for t in ("T1_gate", "T3_ddctl", "T4_stop", "X_ebud"):
                v = g.loc[g.tier == t, rc]
                fin = v[np.isfinite(v)]
                d[t] = float(fin.median()) if len(fin) else np.nan
                d[f"n_{t}"] = int(len(fin))
            for cid, a, bb in CLAIMS:
                pa = d[a] if np.isfinite(d[a]) else BIG
                pb = d[bb] if np.isfinite(d[bb]) else BIG
                d[cid] = bool(pa < pb) if (pa != BIG or pb != BIG) else np.nan
            ranks = {t: (d[t] if np.isfinite(d[t]) else BIG) for t in ALL_TIERS}
            d["order"] = ">".join(sorted(ranks, key=lambda t: (ranks[t], ALL_TIERS.index(t))))
            d["exact"] = d["order"] == ">".join(ALL_TIERS)
            out.append(d)
    return pd.DataFrame(out)


def stability(P, T):
    """Instrument-level vs tier-level rank stability, cross-window and cross-panel."""
    print("\n" + "=" * 200)
    print("STABILITY — is the TIER more stable than the INSTRUMENT?  (Spearman of price ranks)")
    print("=" * 200)
    inst, tier = [], []
    for (pn, b, c), g in P.groupby(["panel", "book", "cost"]):
        rho_i = spearman(g.IS_rate.values, g.OOS_rate.values)
        ti = T[(T.panel == pn) & (T.book == b) & (T.cost == c)]
        a = ti[ti.window == "IS"][ALL_TIERS].iloc[0].values.astype(float)
        bb = ti[ti.window == "OOS"][ALL_TIERS].iloc[0].values.astype(float)
        a = np.where(np.isfinite(a), a, BIG)
        bb = np.where(np.isfinite(bb), bb, BIG)
        rho_t = spearman(a, bb)
        inst.append(rho_i)
        tier.append(rho_t)
        print(f"  {pn:6s} {b:6s} @{c:.0f}bps   instrument rho {rho_i:+.3f} "
              f"(n={int(np.isfinite(g.IS_rate.values).sum())})   tier rho {rho_t:+.3f} (n=4)")
    inst, tier = np.array(inst, float), np.array(tier, float)
    print(f"\n  IS->OOS median Spearman:  instrument {np.nanmedian(inst):+.3f}   "
          f"tier {np.nanmedian(tier):+.3f}   (idea 94 published 0.442 at instrument level on "
          f"its 12 cells)")
    print(f"  IS->OOS mean   Spearman:  instrument {np.nanmean(inst):+.3f}   "
          f"tier {np.nanmean(tier):+.3f}")

    # cross-panel, full-sample, matched on (book, cost, arm)
    print("\n  CROSS-PANEL (full sample, matched book x cost):")
    ci, ct = [], []
    for pa, pb in (("u56", "broad"), ("u56", "small"), ("broad", "small")):
        for b in BOOKS:
            for c in COSTS:
                x = P[(P.panel == pa) & (P.book == b) & (P.cost == c)].set_index("arm").rate
                y = P[(P.panel == pb) & (P.book == b) & (P.cost == c)].set_index("arm").rate
                j = x.index.intersection(y.index)
                r_i = spearman(x[j].values, y[j].values)
                ta = T[(T.panel == pa) & (T.book == b) & (T.cost == c) & (T.window == "full")][ALL_TIERS].iloc[0].values.astype(float)
                tb = T[(T.panel == pb) & (T.book == b) & (T.cost == c) & (T.window == "full")][ALL_TIERS].iloc[0].values.astype(float)
                r_t = spearman(np.where(np.isfinite(ta), ta, BIG), np.where(np.isfinite(tb), tb, BIG))
                ci.append(r_i)
                ct.append(r_t)
                print(f"    {pa:5s} vs {pb:5s}  {b:6s} @{c:.0f}bps   instrument {r_i:+.3f}   tier {r_t:+.3f}")
    print(f"\n  cross-panel median Spearman: instrument {np.nanmedian(ci):+.3f}   "
          f"tier {np.nanmedian(ct):+.3f}")
    return dict(inst_is_oos=np.nanmedian(inst), tier_is_oos=np.nanmedian(tier),
                inst_cross=np.nanmedian(ci), tier_cross=np.nanmedian(ct))


def claim_table(T):
    print("\n" + "=" * 200)
    print("THE CANDIDATE SENTENCE, CLAUSE BY CLAUSE")
    print("  C1 per-name gate < static gross lever | C2 lever < book-level DD rule | "
          "C3 DD rule < per-name stop")
    print("=" * 200)
    print(T[["panel", "book", "cost", "window", "T1_gate", "T2_lever", "T3_ddctl", "T4_stop",
             "X_ebud", "n_T1_gate", "n_T3_ddctl", "n_T4_stop", "C1", "C2", "C3", "exact", "order"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for win in ("full", "IS", "OOS"):
        sub = T[T.window == win]
        print(f"\n  --- window {win} ---")
        for pn in ("u56", "broad", "small"):
            s = sub[sub.panel == pn]
            bits = "  ".join(f"{cid} {int(s[cid].sum())}/{int(s[cid].notna().sum())}"
                             for cid, _, _ in CLAIMS)
            print(f"    {pn:6s}  {bits}   exact-order {int(s.exact.sum())}/{len(s)}   "
                  f"median tier prices  T1 {s.T1_gate.median():.3f}  T2 {s.T2_lever.median():.3f}"
                  f"  T3 {s.T3_ddctl.median():.3f}  T4 {s.T4_stop.median():.3f}")
        s = sub
        bits = "  ".join(f"{cid} {int(s[cid].sum())}/{int(s[cid].notna().sum())}"
                         for cid, _, _ in CLAIMS)
        print(f"    ALL     {bits}   exact-order {int(s.exact.sum())}/{len(s)}")


# ---------------------------------------------------------------- walk-forward
def walk_forward(P, T, rets, bars_by_panel, spy_by_panel, v1_by_panel):
    print("\n" + "=" * 200)
    print("RULE 8 WALK-FORWARD — family chosen on IS only (u56/broad 2009-2016, small "
          "2010-2016), evaluated untouched on 2017-2026")
    print("  S1    = argmin IS rate over arms (idea 94's price-list selector)")
    print("  Stier = argmin IS tier price over {T1,T3,T4}, then the MEDIAN-IS-rate arm inside it")
    print("=" * 200)
    out = []
    for (pn, b, c), cell in P.groupby(["panel", "book", "cost"]):
        elig = cell[(cell.IS_dMaxDD >= 1.0) & np.isfinite(cell.IS_rate)]
        oos_ranked = cell[np.isfinite(cell.OOS_rate) & (cell.OOS_dMaxDD >= 1.0)] \
            .sort_values("OOS_rate")
        best_oos = float(oos_ranked.OOS_rate.iloc[0]) if len(oos_ranked) else np.nan
        ranked = oos_ranked.arm.tolist()
        spy_o = metrics(spy_by_panel[pn].loc[OOS_START:])
        v1_o = metrics(v1_by_panel[pn][c].loc[OOS_START:])
        ctl_o = metrics(rets[pn][(b, "control", c)].loc[OOS_START:])
        rec = dict(panel=pn, book=b, cost=c, n_elig=len(elig), n_oos=len(ranked),
                   ctl_CAGR=ctl_o["CAGR"], ctl_Sharpe=ctl_o["Sharpe"], ctl_MaxDD=ctl_o["MaxDD"],
                   v1_Sharpe=v1_o["Sharpe"], spy_Sharpe=spy_o["Sharpe"], spy_CAGR=spy_o["CAGR"])
        rec.update(tier_pick="-", tier_IS_price=np.nan,
                   IS_lever=float(cell.IS_lever.iloc[0]), rule_warranted=False)
        picks = {}
        if len(elig):
            picks["S1"] = elig.sort_values("IS_rate").iloc[0].arm
            tp = T[(T.panel == pn) & (T.book == b) & (T.cost == c) & (T.window == "IS")].iloc[0]
            cand = [(t, tp[t] if np.isfinite(tp[t]) else BIG) for t in RULE_TIERS
                    if (elig.tier == t).any()]
            if cand:
                t_pick = sorted(cand, key=lambda z: (z[1], RULE_TIERS.index(z[0])))[0][0]
                inside = elig[elig.tier == t_pick].sort_values("IS_rate")
                picks["Stier"] = inside.iloc[(len(inside) - 1) // 2].arm
                rec["tier_pick"] = t_pick
                rec["tier_IS_price"] = tp[t_pick] if np.isfinite(tp[t_pick]) else np.nan
                rec["IS_lever"] = float(cell.IS_lever.iloc[0])
                rec["rule_warranted"] = bool(rec["tier_IS_price"] < rec["IS_lever"]) \
                    if np.isfinite(rec["tier_IS_price"]) else False
        for tag in ("S1", "Stier"):
            a = picks.get(tag)
            if a is None:
                rec.update({f"{tag}_pick": "NOTHING", f"{tag}_OOSrank": np.nan,
                            f"{tag}_OOSrate": np.nan, f"{tag}_regret": np.nan,
                            f"{tag}_OOS_Sharpe": np.nan, f"{tag}_OOS_CAGR": np.nan,
                            f"{tag}_OOS_MaxDD": np.nan})
                continue
            ro = rets[pn][(b, a, c)].loc[OOS_START:]
            mo = metrics(ro)
            r_oos = cell[cell.arm == a].OOS_rate.iloc[0]
            rec.update({
                f"{tag}_pick": a,
                f"{tag}_OOSrank": (ranked.index(a) + 1) if a in ranked else np.nan,
                f"{tag}_OOSrate": r_oos,
                f"{tag}_regret": (r_oos - best_oos) if np.isfinite(r_oos) and np.isfinite(best_oos) else np.nan,
                f"{tag}_OOS_Sharpe": mo["Sharpe"], f"{tag}_OOS_CAGR": mo["CAGR"],
                f"{tag}_OOS_MaxDD": mo["MaxDD"]})
        out.append(rec)
    W = pd.DataFrame(out)
    cols = ["panel", "book", "cost", "S1_pick", "S1_OOSrank", "S1_OOSrate", "S1_regret",
            "S1_OOS_Sharpe", "tier_pick", "rule_warranted", "Stier_pick", "Stier_OOSrank",
            "Stier_OOSrate", "Stier_regret", "Stier_OOS_Sharpe", "n_oos",
            "ctl_Sharpe", "v1_Sharpe", "spy_Sharpe"]
    print(W[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  OOS regret (rate units; 0 = landed on the OOS-cheapest arm), by panel:")
    for pn in ("u56", "broad", "small", "ALL"):
        s = W if pn == "ALL" else W[W.panel == pn]
        print(f"    {pn:6s}  S1 mean {s.S1_regret.mean():+.3f} median {s.S1_regret.median():+.3f}"
              f"  |  Stier mean {s.Stier_regret.mean():+.3f} median {s.Stier_regret.median():+.3f}"
              f"  |  S1 rank-1 {int((s.S1_OOSrank == 1).sum())}/{len(s)}"
              f"  Stier rank-1 {int((s.Stier_OOSrank == 1).sum())}/{len(s)}"
              f"  |  dOOS Sharpe (Stier-S1) {(s.Stier_OOS_Sharpe - s.S1_OOS_Sharpe).mean():+.3f}")
    return W


# ---------------------------------------------------------------- main
def main():
    ok = verify()
    dfs, Ps, rets_by, bars_by, spy_by, v1_by = [], [], {}, {}, {}, {}
    for pn in ("u56", "broad", "small"):
        px, start, df, P, rets, ladders, bars, spy, v1 = do_panel(pn)
        dfs.append(df)
        Ps.append(P)
        rets_by[pn], bars_by[pn], spy_by[pn], v1_by[pn] = rets, bars, spy, v1
    A = pd.concat(dfs, ignore_index=True)
    P = pd.concat(Ps, ignore_index=True)
    T = tier_prices(P)
    A.to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)
    P.to_csv(ROOT / "research" / "backtests" / f"{STEM}.pricelist.csv", index=False)
    T.to_csv(ROOT / "research" / "backtests" / f"{STEM}.tiers.csv", index=False)

    claim_table(T)
    st = stability(P, T)
    W = walk_forward(P, T, rets_by, bars_by, spy_by, v1_by)
    W.to_csv(ROOT / "research" / "backtests" / f"{STEM}.walkforward.csv", index=False)

    # ---------------- the small-panel re-check, stated on its own ----------------
    print("\n" + "=" * 200)
    print("SMALL-PANEL RE-CHECK (ideas 38/49/51: the 200d gate is INVERTED on sub-$2B names)")
    print("=" * 200)
    for c in COSTS:
        s = P[(P.panel == "small") & (P.cost == c)]
        print(f"\n  --- small @{c:.0f} bps: every arm, all 3 books ---")
        print(s[["book", "arm", "tier", "dCAGR", "dMaxDD", "rate", "lever", "dSharpe", "TO"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for pn in ("u56", "broad", "small"):
        s = P[(P.panel == pn) & (P.cost == PCOST)]
        g200 = s[s.arm.str.startswith("g200")]
        st_ = s[s.arm.str.startswith("stop")]
        print(f"\n  {pn:6s} @10bps: g200 median dCAGR {g200.dCAGR.median():+.2f} pp, "
              f"median dMaxDD {g200.dMaxDD.median():+.2f} pp, median rate "
              f"{g200.rate.median():.3f} (priced {int(np.isfinite(g200.rate).sum())}/{len(g200)});"
              f"  stop median dMaxDD {st_.dMaxDD.median():+.2f} pp "
              f"(priced {int(np.isfinite(st_.rate).sum())}/{len(st_)})")

    # ---------------- prediction scorecard ----------------
    print("\n" + "=" * 200)
    print("PREDICTION SCORECARD")
    print("=" * 200)
    print(f"  P1 tier prices more stable than instrument prices "
          f"(IS->OOS median rho {st['tier_is_oos']:+.3f} vs {st['inst_is_oos']:+.3f}; "
          f"cross-panel {st['tier_cross']:+.3f} vs {st['inst_cross']:+.3f}): "
          f"{'CONFIRMED' if (st['tier_is_oos'] > st['inst_is_oos'] and st['tier_cross'] > st['inst_cross']) else 'NOT CONFIRMED (see both numbers)'}")
    f = T[T.window == "full"]
    c1s = {pn: (int(f[f.panel == pn].C1.sum()), int(f[f.panel == pn].C1.notna().sum()))
           for pn in ("u56", "broad", "small")}
    c3s = {pn: (int(f[f.panel == pn].C3.sum()), int(f[f.panel == pn].C3.notna().sum()))
           for pn in ("u56", "broad", "small")}
    print(f"  P2 C1 (gate<lever) inverts on small while C3 (stop dearest) holds everywhere: "
          f"C1 {c1s}  C3 {c3s}")
    ssm = P[(P.panel == "small") & P.arm.str.startswith("stop")]
    print(f"  P3 the stop buys no drawdown on small too: dMaxDD <= 0 in "
          f"{int((ssm.dMaxDD <= 0).sum())}/{len(ssm)} small-panel stop cells "
          f"(median {ssm.dMaxDD.median():+.2f} pp)")
    print(f"  P4 Stier mean OOS regret {W.Stier_regret.mean():+.3f} vs S1 {W.S1_regret.mean():+.3f}: "
          f"{'CONFIRMED' if W.Stier_regret.mean() < W.S1_regret.mean() else 'REFUTED'}")
    b3 = A[(A.cost == PCOST) & A.p4b].groupby("arm").panel.nunique()
    print(f"  P5 arms passing 4b on ALL THREE panels @10bps: "
          f"{sorted(b3[b3 == 3].index.tolist()) or 'none'}")
    print(f"     arms passing 4b on both large panels @10bps: "
          f"{sorted(set(A[(A.cost==PCOST) & A.p4b & (A.panel=='u56')].arm) & set(A[(A.cost==PCOST) & A.p4b & (A.panel=='broad')].arm)) or 'none'}")
    print(f"     4a passes @10bps by panel: "
          + "; ".join(f"{pn}: {sorted(set(A[(A.cost==PCOST) & A.p4a & (A.panel==pn)].arm)) or 'none'}"
                      for pn in ('u56', 'broad', 'small')))
    print(f"\n  harness verification: {'REPRODUCED idea 94' if ok else 'MISMATCH'}")
    print(f"\nWrote {STEM}.grid.csv, .pricelist.csv, .tiers.csv, .walkforward.csv")


if __name__ == "__main__":
    main()
