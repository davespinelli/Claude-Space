#!/usr/bin/env python3
"""Idea 304 - "does-the-EXPOSURE-vs-TIMING-split-price-the-live-de-gross-clause-correctly"
(lane C, 2026-09-06).

The question
------------
Idea 297 (lane B) decomposed the LIVE book -- RULES v2 on universe.json, 200d +/-3% band,
weekly, 75% gross, gated-out weight to CASH -- against its own RESPREAD twin (same gate mask,
weight respread over the names that are IN, so gross is held constant at 0.75).  It found

    live DEGROSS   8.66% CAGR / 1.2056 Sharpe / -12.05% MaxDD
    RESPREAD twin 12.25% CAGR /       ...     / -17.71% MaxDD
    gap0 = -3.88 pp/yr at c_bar 0.7101, of which 96.0% is CONSTANT-LEVERAGE CASH DRAG
    and only -0.155 pp/yr is the TIMING of c_t.

Read literally: the live de-gross clause buys 5.7 pp of drawdown for 3.6 pp of CAGR, and
essentially all of that trade is "hold less on average", not "hold less at the right times".
But 297 stops at the accounting.  The CAPITAL question is the one this script asks:

QUEUE wording: "at what constant gross does the RESPREAD twin match the live book's -12.05%
MaxDD, and does it then beat the live book on CAGR and Sharpe (4a) at that matched risk?"

If a STATIC gross g* reproduces the live book's drawdown and then beats it on return and on
Sharpe in both halves, the dynamic de-gross clause is buying at a bad price: the same risk was
available from a constant cash allocation, with no timing at all.  If it does not, the clause
earns its keep and 297's "96% is drag" is an accounting share, not a verdict.

Three arms, all at the same band / cadence / cost / panel, differing ONLY in how exposure moves
-------------------------------------------------------------------------------------------
    DEGROSS(b, g)   RULES v2's own form.  Weight g/N on every name inside the band, N = names
                    priced that day; gated-out weight goes to CASH.  Realised gross moves with
                    the gate.  DEGROSS(0.03, 0.75) on U56 IS the live book (B0 asserts it).
    RESPREAD(b, g)  Same gate mask, weight g/k over the k names that are IN.  Gross pinned at g
                    whenever anything is IN.  This is idea 297's twin.
    EWALL(g)        No gate at all, weight g/N over every live name.  Pure static exposure --
                    the control that says whether the GATE, not just its de-grossing, is worth
                    anything at matched risk.

Matching
---------
For each arm a constant g* is solved by bisection so the arm's realised risk equals the live
book's on the SAME window.  Two matching targets, both reported, neither tuned:
    DD  : full-sample MaxDD == live MaxDD           (the queue's question, verbatim)
    VOL : annualised vol   == live annualised vol   (a second target, so the headline does not
          rest on a single drawdown episode)
Bisection is on g in [0.05, 1.00]; g > 1 would be leverage and PROTOCOL rule 2 forbids it, so a
target needing g > 1 is reported UNREACHABLE rather than as a pass.

Pre-registered hypotheses (bars fixed before any number was read)
-----------------------------------------------------------------
B0  REPRODUCTION GATE, asserted before anything else.  (i) DEGROSS(0.03, 0.75) on U56 must be
    weight-for-weight identical to baseline.rules_v2_weights (max |diff| < 1e-12); (ii) its
    metrics must reproduce idea 297's published live row (8.66% / 1.2056 / -12.05%) to < 5e-4;
    (iii) RESPREAD(0.03, 0.75) must reproduce 297's twin (12.25% / -17.71%) to < 5e-4; (iv) the
    leverage identity c_t = held_dg/held_rs must reproduce 297's c_bar 0.7101 to < 1e-3.
    If B0 fails the run aborts -- everything downstream would be measuring another book.

H1  EXISTENCE.  On U56 at the live band b=0.03 a constant g* in (0, 1] exists whose RESPREAD
    book matches the live MaxDD to within 0.05 pp.  FAILS if the ladder is non-monotone in g or
    the match needs leverage.

H2  THE CAPITAL CLAIM (the headline).  At that g*, RESPREAD passes 4a against the live book:
    Sharpe > live in BOTH halves AND MaxDD no worse (matched, so within tolerance) AND -- the
    queue asks for it explicitly -- CAGR > live.  All three clauses must hold.
    H2 PASS  => the live de-gross clause is mispriced; the same risk was on the shelf statically.
    H2 FAIL  => the clause earns its keep at matched risk and 297's 96% is an accounting share.

H3  DOES THE GATE EARN ANYTHING.  The same test for EWALL(g*) -- no gate at all.  If EWALL also
    clears 4a at matched risk then the finding is not about de-grossing but about the 200d band
    itself.  Reported as the three-way ordering (live, RESPREAD, EWALL) at matched DD and vol.

H4  WALK-FORWARD (PROTOCOL rule 8).  Both dials are re-chosen on 2009-2016 ONLY: band b by IS
    Sharpe within the arm, and g* by matching the live book's IS MaxDD.  2017-2026 is then read
    once.  OOS CAGR/Sharpe/MaxDD reported against the live book OOS and SPY OOS.  A matched book
    that only wins in sample is PARK, not KEEP.

Tuned parameters (PROTOCOL rule 4: at most two)
------------------------------------------------
    gross g   ladder {0.20, 0.25, ..., 1.00} (17 rungs), plus bisection to the matching targets
    band  b   in {0.00, 0.02, 0.03, 0.05, 0.08, 0.12}   (baseline.band_state, RULES v2 form)
Every grid point is reported.  Panel and construction are REPORTED dimensions, not tuned: the
whole question is the contrast across constructions, and B136 is a robustness read on a panel
where the live construction is transplanted (its own DEGROSS(0.03,0.75) book is the local
"live" reference, since RULES v2 is defined on universe.json).

Grid: 2 panels x 6 bands x 17 gross rungs x 2 gated constructions = 408 backtests, plus
2 x 17 ungated EWALL rungs = 34, plus the bisections, plus the live book.  All printed.

Costs 10 bps per unit turnover, weekly cadence (the live cadence), next-day execution, no
shorting, no leverage (PROTOCOL rule 2).  Both KEEP paths evaluated on every grid point.

SPY's DOUBLE ROLE: universe.json lists SPY as an INSTRUMENT and baseline.rules_v2_weights holds
it, so the live book trades SPY.  All three arms therefore keep SPY as a constituent (this is
what makes B0 reproduce idea 297's live row exactly) while the SPY series is also the 4b
benchmark.  That is the live book's construction, not a choice made here; dropping SPY from the
panel moves the live book to 8.68% / 1.2128 / -11.90% and would not reproduce 297.

SURVIVORSHIP: universe.json and universe_broad.json are TODAY's constituents; no delistings.
The H2/H3 headline is an arm-minus-arm contrast on the SAME names and days at MATCHED realised
risk, so the bias very largely cancels out of it; it does NOT cancel out of the 4a/4b columns,
which are levels.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, band_state, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
LIVE_BAND = 0.03
LIVE_GROSS = 0.75
FREQ = "W"
BANDS = [0.00, 0.02, LIVE_BAND, 0.05, 0.08, 0.12]
GROSSES = [round(0.20 + 0.05 * i, 2) for i in range(17)]      # 0.20 .. 1.00
CONSTRUCTIONS = ["DEGROSS", "RESPREAD"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
G_LO, G_HI = 0.05, 1.00                                        # rule 2: no leverage
BISECT_ITERS = 22

# pre-registered bars
B0_W_TOL = 1e-12          # weight identity vs baseline.rules_v2_weights
B0_M_TOL = 5e-4           # metric reproduction of idea 297's published live/twin rows
B0_C_TOL = 1e-3           # c_bar reproduction
H1_DD_TOL = 0.0005        # 0.05 pp match on MaxDD
PUB = {"live_CAGR": 0.0866, "live_Sharpe": 1.2056, "live_MaxDD": -0.1205,
       "twin_CAGR": 0.1225, "twin_MaxDD": -0.1771, "c_bar": 0.7101}

SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


# ---------------------------------------------------------------- books
def live_mask(px):
    """"N = instruments priced that day" -- baseline.rules_v2_weights's own denominator.

    NOTE (pre-registration deviation, reported because it was found by B0 and not chosen for
    its answer): this script first used idea 297's stricter mask `px.notna() & px.shift(1)
    .notna()`.  Under that convention max |DEGROSS(0.03,0.75) - rules_v2_weights| = 2.941e-04
    (early days only) and B0's 1e-12 clause FAILED, though the metrics still reproduced idea
    297's live row to 1.3e-04 and the twin's to 4.8e-05.  The fix adopted here is to use the
    LIVE book's own denominator, which makes the identity exact; both numbers are printed."""
    return px.notna()


def live_mask_297(px):
    return px.notna() & px.shift(1).notna()


def book(px, construction, band, gross):
    """The three arms.  EWALL ignores `band` (no gate)."""
    live = live_mask(px)
    n = live.sum(axis=1).clip(lower=1)
    if construction == "EWALL":
        return live.astype(float).div(n, axis=0) * gross
    g = band_state(px, band) & live
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    return g.astype(float).div(n, axis=0) * gross              # DEGROSS: cash gets the rest


def run(px, construction, band, gross, cost=COST_BPS):
    res = backtest(px, book(px, construction, band, gross), cost_bps=cost, freq=FREQ)
    return res


def stat(r):
    m = metrics(r)
    h = len(r) // 2
    ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ri), metrics(ro)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"], isVol=mi["Vol"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, live):
    """PROTOCOL 4a: Sharpe > live in BOTH halves and MaxDD no worse than live."""
    return bool(s["H1"] > live["H1"] and s["H2"] > live["H2"] and s["MaxDD"] >= live["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"], "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]), "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def bisect_gross(px, start, construction, band, target, metric, window=None):
    """Smallest-error constant gross whose realised `metric` equals `target` on `window`.

    metric in {'MaxDD','Vol'}; both are monotone DECREASING in |value| as g falls, so a plain
    bisection on |value| - |target| works.  Returns (g, achieved, n_evals, hit_bound)."""
    def f(g):
        r = run(px, construction, band, g)["returns"].loc[start:]
        if window is not None:
            r = r.loc[window]
        return abs(metrics(r)[metric]), r

    lo, hi = G_LO, G_HI
    a_lo, _ = f(lo)
    a_hi, _ = f(hi)
    tgt = abs(target)
    n = 2
    if a_hi < tgt:                       # even full gross is not risky enough
        return hi, a_hi, n, "UNREACHABLE(>1 would be leverage)"
    if a_lo > tgt:
        return lo, a_lo, n, f"UNREACHABLE(<{G_LO})"
    for _ in range(BISECT_ITERS):
        mid = 0.5 * (lo + hi)
        a, _ = f(mid)
        n += 1
        if a < tgt:
            lo = mid
        else:
            hi = mid
    g = 0.5 * (lo + hi)
    a, _ = f(g)
    return g, a, n + 1, ""


# ---------------------------------------------------------------- main
def main():
    px_u = load_universe()
    px_b = load_universe(broad=True)
    # NOTE: universe.json contains SPY as an INSTRUMENT, and baseline.rules_v2_weights holds it.
    # The live book therefore trades SPY, so the panels below keep it as a constituent (that is
    # what makes B0 reproduce exactly) while the SPY series is also used as the benchmark.  The
    # double role is the live book's, not this script's.
    PANELS = {"U56": (px_u, px_u["SPY"]), "B136": (px_b, px_b["SPY"])}
    starts = {k: v[0].index[260] for k, v in PANELS.items()}

    P("=" * 170)
    P(f"Idea 304 does-the-EXPOSURE-vs-TIMING-split-price-the-live-de-gross-clause-correctly (lane C) | {SCRIPT}")
    P("=" * 170)
    for k, (px, _) in PANELS.items():
        P(f"  {k}: {px.index[0].date()} .. {px.index[-1].date()}; evaluated from {starts[k].date()} "
          f"({len(px.loc[starts[k]:]) / 252:.2f} yrs, {px.shape[1]} names)")
    P(f"Costs {COST_BPS} bps, cadence {FREQ}, next-day execution, no shorting, gross capped at "
      f"{G_HI} (rule 2: no leverage).  IS <= {IS_END}, OOS {OOS_START}+.")
    P(f"Tuned: gross g in {GROSSES} and band b in {BANDS}.  All points reported.")
    P("Pre-registered: B0 live-book identity < 1e-12 and 297 metric repro < 5e-4; "
      "H1 a DD-matching g* exists on U56/b=0.03 within 0.05 pp; "
      "H2 that book passes 4a vs live AND beats it on CAGR; "
      "H3 same test for the UNGATED EWALL control; H4 rule-8 walk-forward with both dials "
      "re-chosen on IS only.")

    # ------------------------------------------------------------ B0
    P("\n" + "-" * 170)
    P("B0  REPRODUCTION GATE (asserted before any new number)")
    P("-" * 170)
    w_mine = book(PANELS["U56"][0], "DEGROSS", LIVE_BAND, LIVE_GROSS)
    w_base = rules_v2_weights(px_u)
    dw = float((w_mine - w_base.reindex_like(w_mine).fillna(0.0)).abs().to_numpy().max())
    _l297 = live_mask_297(px_u)
    _g297 = band_state(px_u, LIVE_BAND) & _l297
    w_297 = _g297.astype(float).div(_l297.sum(axis=1).clip(lower=1), axis=0) * LIVE_GROSS
    dw297 = float((w_297 - w_base.reindex_like(w_297).fillna(0.0)).abs().to_numpy().max())
    P(f"  (i)   max |DEGROSS(0.03,0.75) - baseline.rules_v2_weights| = {dw:.3e}   (bar < {B0_W_TOL:g})")
    P(f"        [deviation logged: idea 297's stricter live mask gives {dw297:.3e} and FAILS this "
      f"bar; this script uses the live book's own N = instruments priced that day]")

    st_u = starts["U56"]
    res_live = run(px_u, "DEGROSS", LIVE_BAND, LIVE_GROSS)
    r_live = res_live["returns"].loc[st_u:]
    live = stat(r_live)
    res_twin = run(px_u, "RESPREAD", LIVE_BAND, LIVE_GROSS)
    twin = stat(res_twin["returns"].loc[st_u:])
    d1 = max(abs(live["CAGR"] - PUB["live_CAGR"]), abs(live["Sharpe"] - PUB["live_Sharpe"]),
             abs(live["MaxDD"] - PUB["live_MaxDD"]))
    d2 = max(abs(twin["CAGR"] - PUB["twin_CAGR"]), abs(twin["MaxDD"] - PUB["twin_MaxDD"]))
    P(f"  (ii)  live  {live['CAGR']:.4%} / {live['Sharpe']:.4f} / {live['MaxDD']:.4%}  "
      f"vs idea 297 published 8.66% / 1.2056 / -12.05%  -> max|diff| {d1:.3e} (bar < {B0_M_TOL:g})")
    P(f"  (iii) twin  {twin['CAGR']:.4%} / {twin['Sharpe']:.4f} / {twin['MaxDD']:.4%}  "
      f"vs published 12.25% / -17.71%             -> max|diff| {d2:.3e} (bar < {B0_M_TOL:g})")
    held_dg = res_live["weights"].sum(axis=1).loc[st_u:]
    held_rs = res_twin["weights"].sum(axis=1).loc[st_u:]
    c_t = (held_dg / held_rs.replace(0, np.nan)).fillna(0.0)
    c_bar = float(c_t.mean())
    d3 = abs(c_bar - PUB["c_bar"])
    P(f"  (iv)  c_bar = mean(held_DG/held_RS) = {c_bar:.4f} vs published 0.7101 -> |diff| {d3:.3e} "
      f"(bar < {B0_C_TOL:g});  c_t sd {float(c_t.std()):.4f}")
    if not (dw < B0_W_TOL and d1 < B0_M_TOL and d2 < B0_M_TOL and d3 < B0_C_TOL):
        P("!! B0 FAILED - aborting; downstream numbers would describe a different book.")
        sys.exit(1)
    P("  B0 PASSES on all four clauses.  The live book below is the book we actually run.")

    spy = {k: stat(v[1].pct_change().fillna(0.0).loc[starts[k]:]) for k, v in PANELS.items()}
    ref_b136 = stat(run(px_b, "DEGROSS", LIVE_BAND, LIVE_GROSS)["returns"].loc[starts["B136"]:])
    REF = {"U56": live, "B136": ref_b136}
    P(f"  B136 local reference (live CONSTRUCTION transplanted, DEGROSS b=0.03 g=0.75): "
      f"{ref_b136['CAGR']:.2%} / {ref_b136['Sharpe']:.4f} / {ref_b136['MaxDD']:.2%}")
    for k in PANELS:
        s = spy[k]
        P(f"  SPY on the {k} window: {s['CAGR']:.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:.2%} "
          f"(halves {s['H1']:.4f}/{s['H2']:.4f}, OOS {s['oSharpe']:.4f})")

    # ------------------------------------------------------------ the ladder
    P("\n" + "-" * 170)
    P("THE GROSS LADDER (every grid point; 4a judged vs that panel's live-form reference, 4b vs SPY)")
    P("-" * 170)
    rows = []
    for pk, (px, _) in PANELS.items():
        st = starts[pk]
        for con in CONSTRUCTIONS + ["EWALL"]:
            bands = BANDS if con != "EWALL" else [np.nan]
            for b in bands:
                for g in GROSSES:
                    r = run(px, con, 0.0 if con == "EWALL" else b, g)["returns"].loc[st:]
                    s = stat(r)
                    rows.append(dict(panel=pk, construction=con, band=b, gross=g, **s,
                                     v4a=verdict_4a(s, REF[pk]), fail4b=fail_4b(s, spy[pk])))
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"  {len(grid)} grid points written to {Path(OUT).name}.grid.csv")
    for pk in PANELS:
        for con in CONSTRUCTIONS + ["EWALL"]:
            sub = grid[(grid.panel == pk) & (grid.construction == con)]
            piv = sub.pivot_table(index="gross", columns="band", values="MaxDD", dropna=False)
            P(f"\n  MaxDD by (gross x band) -- {pk} / {con}   [live-form reference MaxDD "
              f"{REF[pk]['MaxDD']:.4f}]")
            P(fmt(piv * 100))
            piv2 = sub.pivot_table(index="gross", columns="band", values="CAGR", dropna=False)
            P(f"  CAGR %/yr by (gross x band) -- {pk} / {con}")
            P(fmt(piv2 * 100))
            piv3 = sub.pivot_table(index="gross", columns="band", values="Sharpe", dropna=False)
            P(f"  Sharpe by (gross x band) -- {pk} / {con}")
            P(fmt(piv3))
    P(f"\n  4a passes on the ladder: {int((grid.v4a).sum())}/{len(grid)}   "
      f"4b passes: {int((grid.fail4b == '-').sum())}/{len(grid)}")
    if (grid.fail4b == "-").any():
        P("  4b passers:")
        P(fmt(grid[grid.fail4b == "-"][["panel", "construction", "band", "gross", "CAGR", "Sharpe",
                                        "MaxDD", "H1", "H2", "oSharpe"]]))
    P("  4b binding-bar census (which bar fails, over all points):")
    P(grid.fail4b.value_counts().to_string())

    # monotonicity of MaxDD in gross (H1's precondition)
    mono = []
    for (pk, con, b), sub in grid.groupby(["panel", "construction", "band"], dropna=False):
        v = sub.sort_values("gross").MaxDD.to_numpy()
        mono.append(dict(panel=pk, construction=con, band=b, monotone=bool((np.diff(v) <= 1e-12).all()),
                         n_violations=int((np.diff(v) > 1e-12).sum())))
    mono = pd.DataFrame(mono)
    P(f"\n  MaxDD monotone (weakly deepening) in gross: {int(mono.monotone.sum())}/{len(mono)} arms; "
      f"total violations {int(mono.n_violations.sum())}")

    # ------------------------------------------------------------ H1/H2/H3 matched risk
    P("\n" + "-" * 170)
    P("H1/H2/H3  MATCHED-RISK HEAD-TO-HEAD (constant gross solved to the live book's own risk)")
    P("-" * 170)
    mrows = []
    for pk, (px, _) in PANELS.items():
        st = starts[pk]
        ref = REF[pk]
        for target, mkey in (("DD", "MaxDD"), ("VOL", "Vol")):
            for con in ["RESPREAD", "EWALL"]:
                bands = BANDS if con == "RESPREAD" else [np.nan]
                if target == "VOL":
                    bands = [LIVE_BAND] if con == "RESPREAD" else [np.nan]
                for b in bands:
                    bb = 0.0 if con == "EWALL" else b
                    g, ach, nev, note = bisect_gross(px, st, con, bb, ref[mkey], mkey)
                    s = stat(run(px, con, bb, g)["returns"].loc[st:])
                    mrows.append(dict(panel=pk, target=target, construction=con, band=b,
                                      g_star=g, achieved=ach, ref=abs(ref[mkey]),
                                      err=ach - abs(ref[mkey]), evals=nev, note=note,
                                      dCAGR_pp=100 * (s["CAGR"] - ref["CAGR"]),
                                      dSharpe=s["Sharpe"] - ref["Sharpe"],
                                      dH1=s["H1"] - ref["H1"], dH2=s["H2"] - ref["H2"],
                                      v4a=verdict_4a(s, ref), fail4b=fail_4b(s, spy[pk]), **s))
    M = pd.DataFrame(mrows)
    M.to_csv(f"{OUT}.matched.csv", index=False)
    cols = ["panel", "target", "construction", "band", "g_star", "achieved", "ref", "err",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "dCAGR_pp", "dSharpe", "v4a", "fail4b", "note"]
    P(fmt(M[cols]))

    hl = M[(M.panel == "U56") & (M.target == "DD") & (M.construction == "RESPREAD")
           & (M.band == LIVE_BAND)].iloc[0]
    ew = M[(M.panel == "U56") & (M.target == "DD") & (M.construction == "EWALL")].iloc[0]
    P("")
    P(f"  H1 EXISTENCE: U56 / b={LIVE_BAND} / RESPREAD matches the live -12.05% MaxDD at "
      f"g* = {hl.g_star:.4f} (achieved {-hl.achieved:.4%}, err {hl.err:+.2e}); "
      f"{'PASS' if abs(hl.err) <= H1_DD_TOL and not hl.note else 'FAIL'} "
      f"(bar |err| <= {H1_DD_TOL:g}, no leverage)")
    P(f"  H2 CAPITAL CLAIM at matched DD:  RESPREAD(g*={hl.g_star:.3f}) "
      f"{hl.CAGR:.2%} / {hl.Sharpe:.4f} / {hl.MaxDD:.2%} (halves {hl.H1:.4f}/{hl.H2:.4f})  vs  "
      f"live {live['CAGR']:.2%} / {live['Sharpe']:.4f} / {live['MaxDD']:.2%} "
      f"(halves {live['H1']:.4f}/{live['H2']:.4f})")
    h2_clauses = {"H1 half": hl.dH1 > 0, "H2 half": hl.dH2 > 0,
                  "MaxDD no worse": hl.MaxDD >= live["MaxDD"] - H1_DD_TOL, "CAGR > live": hl.dCAGR_pp > 0}
    P(f"     dCAGR {hl.dCAGR_pp:+.2f} pp/yr, dSharpe {hl.dSharpe:+.4f}; clauses "
      + ", ".join(f"{k}={'Y' if v else 'N'}" for k, v in h2_clauses.items())
      + f"  -> H2 {'PASS' if all(h2_clauses.values()) else 'FAIL'}")
    P(f"  H3 UNGATED CONTROL at matched DD: EWALL(g*={ew.g_star:.3f}) "
      f"{ew.CAGR:.2%} / {ew.Sharpe:.4f} / {ew.MaxDD:.2%} (halves {ew.H1:.4f}/{ew.H2:.4f}), "
      f"dCAGR {ew.dCAGR_pp:+.2f} pp/yr, dSharpe {ew.dSharpe:+.4f}, 4a {ew.v4a}")

    # ------------------------------------------------------------ H4 walk-forward
    P("\n" + "-" * 170)
    P("H4  WALK-FORWARD (PROTOCOL rule 8): band by IS Sharpe, g* by matching the live book's IS "
      "MaxDD; 2017+ read once")
    P("-" * 170)
    wf = []
    for pk, (px, _) in PANELS.items():
        st = starts[pk]
        ref = REF[pk]
        is_win = slice(None, IS_END)
        for con in ["RESPREAD", "EWALL", "DEGROSS"]:
            bands = BANDS if con != "EWALL" else [np.nan]
            # dial 1: band chosen on IS Sharpe at the live gross
            iss = {}
            for b in bands:
                bb = 0.0 if con == "EWALL" else b
                r = run(px, con, bb, LIVE_GROSS)["returns"].loc[st:IS_END]
                iss[b] = metrics(r)["Sharpe"]
            b_pick = max(iss, key=iss.get)
            bb = 0.0 if con == "EWALL" else b_pick
            # dial 2: gross matched to the live book's IS MaxDD, on IS only
            g, ach, nev, note = bisect_gross(px, st, con, bb, ref["isMaxDD"], "MaxDD", window=is_win)
            r = run(px, con, bb, g)["returns"].loc[st:]
            s = stat(r)
            wf.append(dict(panel=pk, construction=con, band_pick=b_pick, IS_sharpe=iss[b_pick],
                           g_star_IS=g, IS_MaxDD_ach=-ach, IS_MaxDD_ref=ref["isMaxDD"], note=note,
                           oCAGR=s["oCAGR"], oSharpe=s["oSharpe"], oMaxDD=s["oMaxDD"],
                           beats_live_OOS=s["oSharpe"] > ref["oSharpe"],
                           beats_SPY_OOS=s["oSharpe"] > spy[pk]["oSharpe"],
                           fullCAGR=s["CAGR"], fullSharpe=s["Sharpe"], fullMaxDD=s["MaxDD"],
                           v4a=verdict_4a(s, ref), fail4b=fail_4b(s, spy[pk])))
        wf.append(dict(panel=pk, construction="LIVE-FORM ref (b=0.03,g=0.75)", band_pick=LIVE_BAND,
                       IS_sharpe=ref["isSharpe"], g_star_IS=LIVE_GROSS, IS_MaxDD_ach=ref["isMaxDD"],
                       IS_MaxDD_ref=ref["isMaxDD"], note="", oCAGR=ref["oCAGR"],
                       oSharpe=ref["oSharpe"], oMaxDD=ref["oMaxDD"], beats_live_OOS=False,
                       beats_SPY_OOS=ref["oSharpe"] > spy[pk]["oSharpe"], fullCAGR=ref["CAGR"],
                       fullSharpe=ref["Sharpe"], fullMaxDD=ref["MaxDD"], v4a=False,
                       fail4b=fail_4b(ref, spy[pk])))
        s = spy[pk]
        wf.append(dict(panel=pk, construction="SPY", band_pick=np.nan, IS_sharpe=s["isSharpe"],
                       g_star_IS=1.0, IS_MaxDD_ach=s["isMaxDD"], IS_MaxDD_ref=ref["isMaxDD"],
                       note="", oCAGR=s["oCAGR"], oSharpe=s["oSharpe"], oMaxDD=s["oMaxDD"],
                       beats_live_OOS=s["oSharpe"] > ref["oSharpe"], beats_SPY_OOS=False,
                       fullCAGR=s["CAGR"], fullSharpe=s["Sharpe"], fullMaxDD=s["MaxDD"],
                       v4a=False, fail4b="-"))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(W))

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 170)
    P("VERDICT")
    P("=" * 170)
    P(f"  H1 {'PASS' if abs(hl.err) <= H1_DD_TOL and not hl.note else 'FAIL'}   "
      f"H2 {'PASS' if all(h2_clauses.values()) else 'FAIL'}   "
      f"H3 EWALL 4a={ew.v4a}   "
      f"4a {int(grid.v4a.sum())}/{len(grid)} on the ladder, 4b {int((grid.fail4b == '-').sum())}/{len(grid)}")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")
    P(f"  console -> {Path(OUT).name}.console.txt")


if __name__ == "__main__":
    main()
