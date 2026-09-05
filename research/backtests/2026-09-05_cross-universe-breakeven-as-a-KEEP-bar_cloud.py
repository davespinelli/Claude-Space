#!/usr/bin/env python3
"""QUEUE idea 82 — cross-universe-breakeven-as-a-KEEP-bar  (research sprint, cloud, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 82)
    Idea 11 found that idea 2's standing 4b KEEP survives CROSS-UNIVERSE 4b (passing on
    universe.json AND universe_broad.json) only to 5 bps — breakeven 7.5 bps, EWall 10.5 —
    while PROTOCOL rule 2 assumes 10, and that the walk-forward spread on that breakeven is
    +26 / -13.5 bps.  Idea 82 re-runs the same 0.5 bp breakeven curve on EVERY standing
    candidate and asks what numeric bar RULES should state.

      Q1  The curve.  For every book, the largest cost at which it still passes 4b on u56,
          on broad, and on BOTH (the cross-universe breakeven), on a 0.5 bp grid 0..30.
          Is the pass set actually an interval in cost, or does it have holes?
      Q2  Which of 4b's five bars fails first as cost rises?  (A breakeven set by the CAGR
          floor is a return bar; one set by a Sharpe bar is a different animal.)
      Q3  Rule 8 walk-forward: measure the breakeven on 2009-2016 ONLY, then measure it on
          2017-2026 untouched, and report the spread per book.  Idea 11's +26 / -13.5 is the
          number under test.  An IS breakeven that does not predict the OOS one cannot be a
          pre-registered bar.
      Q4  The proposed bar.  Sweep a candidate cost bar C* and report how many books survive
          at each, crossed with 4b's two coefficients — every grid point printed.
      Q5  Both KEEP paths at the two published cost rungs (10 and 25 bps): OOS CAGR / Sharpe /
          MaxDD for every candidate against RULES v1 and SPY on both universes.

    A finding that the breakeven is not predictable out of sample is a KILL of the proposal as
    a BAR and is reported as one.  Rule 7: nothing is tuned until it works.

STANDING CANDIDATES — the mapping, stated rather than assumed
    The leaderboard is prose and does not uniquely pin each candidate's gate or its de-gross
    convention, so this run evaluates a 4-book x 9-arm grid (the ungated control plus 4 gates x
    {dg, rw}) that CONTAINS every reading, and names the mapping instead of assuming one:
      idea 2   `TOP20 + v1gate`   composite top-20 at 75%/20 among names passing the RULES v1
                                  gate.  Idea 81 calls the literal CAND-n a book that de-grosses
                                  when fewer than n names are eligible, so BOTH conventions are
                                  reported (`-dg`, `-rw`) and neither is asserted to be it.
      idea 46  `FRAC85 + v1gate`  breadth-adaptive count: k_t = round(0.85 x eligible_t), equal
                                  weight 75%/k_t.  Full-gross by construction, so its dg and rw
                                  forms COINCIDE and only one is run.  Stated, not hidden.
      idea 57  `EWall + band3`    equal-weight all names, 3% band around the 200d MA.  Idea 91's
                                  changelog names `band3-rw` as the published form; `band3-dg` is
                                  reported beside it because the first draft of this run assumed
                                  dg and got a different answer — the convention is load-bearing.
      idea 72  `EWall + control`  equal-weight all names, NO gate, no ranking, no vol scaler.
                                  The prose ("no ranking, no vol scaler, no universe choice")
                                  does not settle whether idea 10's B136/EWall was gated, so
                                  `EWall + v1gate-dg` and `EWall + vol60-dg` (the incumbent
                                  cross-universe passer of ideas 94/127/133) are reported beside
                                  it and no single row is claimed to BE idea 72.
    V1u (RULES v1's own 5-name book, ungrossed) is carried as the live-rules reference.

TUNED PARAMETERS — exactly two (4b's coefficients, as in ideas 131/144/148)
    phi    CAGR floor   in {0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00}   (0.70 published)
    delta  MaxDD cap    in {0.40, 0.50, 0.60, 0.70, 0.80, 1.00}         (0.60 published)
    COST is not a tuned parameter: it is the axis under adjudication, swept exhaustively at
    0.5 bp from 0 to 30 and reported in full.  Gross is pinned at the published 75%.

GRID  2 panels x 32 (book, arm) pairs x 61 cost points = 3,904 backtests.  Weekly, t+1.
      IS <= 2016-12-31, OOS >= 2017-01-01.

CAVEATS carried, not buried
    - SURVIVORSHIP: u56 and broad are current-constituent lists (idea 54).  The small panel is
      deliberately NOT used here: idea 82 is a cross-LARGE-CAP-universe question and no book
      in the corpus has ever passed 4b on the small panel.
    - Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so IS breakevens
      are biased UP.  Q3 measures that bias rather than assuming it away.
    - Idea 38: u56/broad are on a calendar-day index (weekend rows ffilled).
    - A 10 bps cost is charged per unit of turnover both ways; no spread/impact model.
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

STEM = "2026-09-05_cross-universe-breakeven-as-a-KEEP-bar_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
PANELS = ["u56", "broad"]
BOOKS = ["V1u", "TOP20", "EWall", "FRAC85"]
ARMS = ([("control", None)]
        + [(f"{g}-{c}", g, c) for g in ("v1gate", "band3", "vol60", "g200")
           for c in ("dg", "rw")])
ARMS = [(a[0], a[1], (a[2] if len(a) > 2 else "dg")) for a in ARMS]
FRAC = 0.85                                                # idea 46/47's published fraction

COSTS = [round(x, 1) for x in np.arange(0.0, 30.001, 0.5)]  # the 0.5 bp curve, 61 points
CBARS = [0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 20.0, 25.0, 30.0]

PHIS = [0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
DELTAS = [0.40, 0.50, 0.60, 0.70, 0.80, 1.00]
PHI0, DELTA0 = 0.70, 0.60
BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARS_W = ("H1", "H2", "DD", "CAGR")                        # inside a single window

NAMED = {("TOP20", "v1gate-dg"): "idea 2  CAND-n20 (dg)",
         ("TOP20", "v1gate-rw"): "idea 2  CAND-n20 (rw)",
         ("FRAC85", "v1gate-dg"): "idea 46 fraction f=0.85",
         ("EWall", "band3-rw"): "idea 57 ew-all + 3% band (rw, as published)",
         ("EWall", "band3-dg"): "idea 57 ew-all + 3% band (dg reading)",
         ("EWall", "control"): "idea 72 ew-all (ungated reading)",
         ("EWall", "v1gate-dg"): "idea 72 ew-all (gated reading)",
         ("EWall", "vol60-dg"): "incumbent EWall + vol60-dg"}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 3000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


_PCACHE = {}


def panel(name):
    if name not in _PCACHE:
        px = load_universe() if name == "u56" else load_universe(broad=True)
        _PCACHE[name] = (px, px["SPY"].pct_change().fillna(0.0),
                         "universe.json(56)" if name == "u56" else "universe_broad.json(136)")
    return _PCACHE[name]


def frac_targets(px, gate, f=FRAC):
    """Idea 46's breadth-adaptive count: hold the top round(f x eligible_t) eligible names,
       equal weight at GROSS / k_t.  Full gross by construction (stated in the header)."""
    g = H.gate_mask(px, gate)
    s = H.composite(px).where(g)
    k = (g.sum(axis=1) * f).round().clip(lower=1)
    rank = s.rank(axis=1, ascending=False)
    sel = rank.le(k, axis=0) & g
    return sel.astype(float).mul(GROSS / k, axis=0).fillna(0.0)


def targets_of(px, book, gate, conv="dg"):
    """conv='dg' sends gated-out names to CASH; conv='rw' rebuilds the book at full gross among
       the gated-in names only.  The FRAC85 book is full-gross by construction, so its two
       conventions coincide and only the 'dg' label is carried (stated, not hidden)."""
    if book == "FRAC85":
        return frac_targets(px, gate)
    return H.targets(px, book, gate, conv)


def bars_win(spy, which):
    if which == "full":
        s1, s2 = H.halves(spy)
        m = metrics(spy)
        return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                    soos=metrics(spy.loc[OOS_START:])["Sharpe"])
    w = H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=m["Sharpe"])


def stats_win(r, which):
    w = r if which == "full" else H.window(r, which)
    m = metrics(w)
    h1, h2 = H.halves(w)
    oos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS=oos)


def margins(st, b, phi, delta):
    return dict(H1=st["H1"] - b["s1"], H2=st["H2"] - b["s2"], OOS=st["OOS"] - b["soos"],
                DD=delta * abs(b["sdd"]) - abs(st["MaxDD"]),
                CAGR=st["CAGR"] - phi * b["scagr"])


def build():
    rows = []
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        B = {w: bars_win(spy, w) for w in ("full", "IS", "OOS")}
        say(f"\n--- PANEL {pname}: {desc} | eval from {start.date()} | SPY full "
            f"{B['full']['scagr']:.2%}/{metrics(spy)['Sharpe']:.3f}/{B['full']['sdd']:.2%}  "
            f"halves {B['full']['s1']:.3f}/{B['full']['s2']:.3f}  OOS {B['full']['soos']:.3f}")
        say(f"    IS SPY CAGR {B['IS']['scagr']:.2%} MaxDD {B['IS']['sdd']:.2%} | "
            f"OOS SPY CAGR {B['OOS']['scagr']:.2%} MaxDD {B['OOS']['sdd']:.2%}")
        V1W = rules_v1_weights(px)
        V1 = {c: backtest(px, V1W, cost_bps=c, freq=FREQ)["returns"].loc[start:] for c in COSTS}
        for book in BOOKS:
            for arm, gate, conv in ARMS:
                if book == "FRAC85" and conv == "rw":
                    continue          # identical to its dg twin by construction
                W = targets_of(px, book, gate, conv)
                for c in COSTS:
                    r = H.run(px, W, m=1.0, bps=c)["r"].loc[start:]
                    d = dict(panel=pname, book=book, arm=arm, cost=c,
                             pass4a=H.pass4a(r, V1[c]))
                    for w in ("full", "IS", "OOS"):
                        st = stats_win(r, w)
                        mg = margins(st, B[w], PHI0, DELTA0)
                        d[f"{w}_CAGR"], d[f"{w}_Sharpe"], d[f"{w}_MaxDD"] = (
                            st["CAGR"], st["Sharpe"], st["MaxDD"])
                        for k in BARS5:
                            d[f"{w}_m_{k}"] = mg[k]
                        for k, key in (("s1", "b_s1"), ("s2", "b_s2"), ("soos", "b_soos"),
                                       ("sdd", "b_sdd"), ("scagr", "b_scagr")):
                            d[f"{w}_{key}"] = B[w][k]
                        d[f"{w}_H1"], d[f"{w}_H2"], d[f"{w}_OOSs"] = st["H1"], st["H2"], st["OOS"]
                    rows.append(d)
            say(f"    {pname}/{book}: {len(rows)} rows")
    return pd.DataFrame(rows)


def ok_frame(F, phi, delta, w):
    keys = BARS5 if w == "full" else BARS_W
    out = {}
    out["H1"] = F[f"{w}_H1"] - F[f"{w}_b_s1"] > 0
    out["H2"] = F[f"{w}_H2"] - F[f"{w}_b_s2"] > 0
    out["OOS"] = F[f"{w}_OOSs"] - F[f"{w}_b_soos"] > 0
    out["DD"] = delta * F[f"{w}_b_sdd"].abs() - F[f"{w}_MaxDD"].abs() > 0
    out["CAGR"] = F[f"{w}_CAGR"] - phi * F[f"{w}_b_scagr"] > 0
    D = pd.DataFrame(out, index=F.index)
    return D, list(keys)


def breakevens(F, phi=PHI0, delta=DELTA0, w="full"):
    """Per (panel, book, arm): max cost still passing, plus a contiguity check."""
    D, keys = ok_frame(F, phi, delta, w)
    G = F[["panel", "book", "arm", "cost"]].copy()
    G["ok"] = D[keys].all(axis=1).values
    rows = []
    for (p, b, a), d in G.groupby(["panel", "book", "arm"], sort=False):
        d = d.sort_values("cost")
        o = d.ok.values
        if not o.any():
            rows.append(dict(panel=p, book=b, arm=a, be=np.nan, n_ok=0, contiguous=np.nan,
                             holes=np.nan))
            continue
        idx = np.flatnonzero(o)
        rows.append(dict(panel=p, book=b, arm=a, be=float(d.cost.values[idx.max()]),
                         n_ok=int(o.sum()),
                         contiguous=bool(idx.max() - idx.min() + 1 == len(idx)),
                         holes=int(idx.max() - idx.min() + 1 - len(idx))))
    return pd.DataFrame(rows)


def cross(BE):
    """Cross-universe breakeven = min over the two panels (NaN if either never passes)."""
    piv = BE.pivot_table(index=["book", "arm"], columns="panel", values="be", dropna=False)
    piv["cross"] = piv.min(axis=1, skipna=False)
    piv["named"] = [NAMED.get((b, a), "") for b, a in piv.index]
    return piv


def main():
    say("=" * 200)
    say("IDEA 82 — cross-universe-breakeven-as-a-KEEP-bar.  Under adjudication: what COST a "
        "KEEP must survive on BOTH large-cap universes, as a number RULES can state.")
    nbook = len(PANELS) * (3 * len(ARMS) + (1 + (len(ARMS) - 1) // 2))
    say(f"grid = {len(PANELS)} panels x {len(BOOKS)} books x up to {len(ARMS)} arms "
        f"(5 gates x dg/rw + the ungated control; FRAC85 is full-gross so its rw twin is "
        f"identical and is not re-run) x {len(COSTS)} cost points "
        f"({COSTS[0]}..{COSTS[-1]} bps by 0.5) = {nbook*len(COSTS)} backtests")
    say(f"bars: CAGR >= {PHI0} x SPY, MaxDD <= {DELTA0} x |SPY|, both halves and OOS Sharpe > SPY. "
        f"gross pinned at {GROSS:.0%}.  IS <= {IS_END}, OOS >= {OOS_START}.")
    say("=" * 200)

    F = build()
    say(f"\nframe: {len(F)} rows")

    # ---------------------------------------------------------------- harness check
    px56, _, _ = panel("u56")
    s56 = px56.index[260]
    ew = H.targets(px56, "EWall")
    a = H.run(px56, ew, bps=PCOST)["r"].loc[s56:]
    b = backtest(px56, ew, cost_bps=PCOST, freq=FREQ)["returns"].loc[s56:]
    say(f"\nharness check: H.run vs engine.backtest, ungated EWall u56, max|diff| = "
        f"{float((a-b).abs().max()):.3e}")
    pub = F[(F.panel == "u56") & (F.book == "EWall") & (F.arm == "vol60-dg") & (F.cost == 10.0)]
    say(f"idea 94's published EWall+vol60-dg u56@10bps: {pub.full_CAGR.iloc[0]:.3%} / "
        f"{pub.full_Sharpe.iloc[0]:.3f} / {pub.full_MaxDD.iloc[0]:.3%}  "
        f"(published 11.587% / 1.133 / -16.884%)")

    # ---------------------------------------------------------------- Q1 the curve
    say("\n" + "=" * 200)
    say("Q1  THE 0.5 bp BREAKEVEN CURVE (full sample, published bars).  be = highest cost still "
        "passing 4b; NaN = never passes, even at 0 bps.")
    BE = breakevens(F)
    X = cross(BE)
    say("\n" + X.to_string(float_format=lambda x: f"{x:.1f}"))
    nc = BE[BE.n_ok > 0]
    say(f"\n  contiguity of the passing cost set: {int(nc.contiguous.sum())} of {len(nc)} "
        f"(book, arm, panel) triples are contiguous; total interior holes {int(nc.holes.sum())}")
    say("\n  THE FOUR STANDING CANDIDATES (cross-universe breakeven, bps):")
    for k, nm in NAMED.items():
        if k in X.index:
            r = X.loc[k]
            say(f"    {nm:34s}  u56 {r['u56']!s:>5}  broad {r['broad']!s:>5}  "
                f"cross {r['cross']!s:>5}")
    say(f"\n  idea 11's claim: idea 2's candidate breakeven 7.5 bps, EWall 10.5 bps "
        f"(cross-universe 4b survives to 5 bps).")

    # ---------------------------------------------------------------- Q2 binding bar
    say("\n" + "=" * 200)
    say("Q2  WHICH BAR FAILS FIRST AS COST RISES?  Evaluated at the first cost point ABOVE each "
        "book's own breakeven (the failure that sets it).")
    D, keys = ok_frame(F, PHI0, DELTA0, "full")
    FF = F.copy()
    for k in BARS5:
        FF[f"ok_{k}"] = D[k].values
    rows = []
    for (p, b, ar), d in FF.groupby(["panel", "book", "arm"], sort=False):
        d = d.sort_values("cost")
        be = BE[(BE.panel == p) & (BE.book == b) & (BE.arm == ar)].be.iloc[0]
        if not np.isfinite(be):
            first = d.iloc[0]           # fails even at 0 bps
            tag = "fails at 0bps"
        else:
            nxt = d[d.cost > be]
            if len(nxt) == 0:
                rows.append(dict(panel=p, book=b, arm=ar, at=">30bps", **{k: "" for k in BARS5}))
                continue
            first, tag = nxt.iloc[0], f"{nxt.iloc[0].cost:.1f}bps"
        rows.append(dict(panel=p, book=b, arm=ar, at=tag,
                         **{k: ("ok" if first[f"ok_{k}"] else "FAIL") for k in BARS5}))
    Q2 = pd.DataFrame(rows)
    say(Q2.to_string(index=False))
    fails = {k: int((Q2[k] == "FAIL").sum()) for k in BARS5}
    say(f"\n  count of first-failing bars over the {len(Q2)} triples: {fails}")

    # ---------------------------------------------------------------- Q3 walk-forward
    say("\n" + "=" * 200)
    say("Q3  RULE 8 WALK-FORWARD ON THE BREAKEVEN — measured on 2009-2016 only, then on "
        "2017-2026 untouched.  The spread is the number a pre-registered bar would have to "
        "tolerate.")
    BEi, BEo = breakevens(F, w="IS"), breakevens(F, w="OOS")
    Xi, Xo = cross(BEi), cross(BEo)
    J = pd.DataFrame(dict(IS=Xi["cross"], OOS=Xo["cross"], full=X["cross"],
                          named=X["named"]))
    J["spread"] = J.OOS - J.IS
    say("\n  cross-universe breakeven by window (bps):")
    say(J.to_string(float_format=lambda x: f"{x:.1f}"))
    both = J.dropna(subset=["IS", "OOS"])
    if len(both) >= 3:
        say(f"\n  over the {len(both)} books measurable in BOTH windows: "
            f"mean spread {both.spread.mean():+.1f} bps, median {both.spread.median():+.1f}, "
            f"range {both.spread.min():+.1f} .. {both.spread.max():+.1f}; "
            f"Spearman(IS, OOS) = {H.spearman(both.IS.values, both.OOS.values):+.3f}")
        say(f"  IS breakeven exceeds OOS in {int((both.spread < 0).sum())} of {len(both)} books "
            f"(idea 128 predicts the shallow IS window flatters every book)")
    say("\n  per-panel breakevens by window (bps):")
    PW = (BEi.set_index(["panel", "book", "arm"]).be.rename("IS")
          .to_frame().join(BEo.set_index(["panel", "book", "arm"]).be.rename("OOS"))
          .join(BE.set_index(["panel", "book", "arm"]).be.rename("full")))
    PW["spread"] = PW.OOS - PW.IS
    say(PW.to_string(float_format=lambda x: f"{x:.1f}"))

    # ---------------------------------------------------------------- Q4 the proposed bar
    say("\n" + "=" * 200)
    say(f"Q4  THE PROPOSED BAR.  How many of the {X.shape[0]} books hold "
        f"cross-universe 4b to at least C* bps, at every (phi, delta)?  "
        f"{len(PHIS)}x{len(DELTAS)}x{len(CBARS)} = {len(PHIS)*len(DELTAS)*len(CBARS)} points, "
        f"all reported.")
    rows = []
    for phi in PHIS:
        for delta in DELTAS:
            xx = cross(breakevens(F, phi, delta))["cross"]
            for cb in CBARS:
                rows.append(dict(phi=phi, delta=delta, Cstar=cb,
                                 n_survive=int((xx >= cb - 1e-9).sum())))
    Q4 = pd.DataFrame(rows)
    say(Q4.pivot_table(index=["phi", "delta"], columns="Cstar", values="n_survive").to_string())
    pub_row = Q4[(Q4.phi == PHI0) & (Q4.delta == DELTA0)]
    say(f"\n  at the published bars, books surviving to C*: "
        + ", ".join(f"{int(r.Cstar)}bps:{int(r.n_survive)}" for r in pub_row.itertuples()))

    # ---------------------------------------------------------------- Q5 both KEEP paths
    say("\n" + "=" * 200)
    say("Q5  BOTH KEEP PATHS AT THE PUBLISHED COST RUNGS.  OOS (2017-2026) numbers, per panel.")
    for c in (10.0, 25.0):
        say(f"\n  --- {c:.0f} bps ---")
        sub = F[F.cost == c].copy()
        sub["named"] = [NAMED.get((b, a), "") for b, a in zip(sub.book, sub.arm)]
        D5, _ = ok_frame(sub, PHI0, DELTA0, "full")
        sub["pass4b"] = D5[list(BARS5)].all(axis=1).values
        cols = ["panel", "book", "arm", "named", "full_CAGR", "full_Sharpe", "full_MaxDD",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b"]
        say(sub[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        for pname in PANELS:
            px, spy, _ = panel(pname)
            start = px.index[260]
            sm = metrics(H.window(spy.loc[start:], "OOS"))
            v1 = backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
            vm = metrics(H.window(v1, "OOS"))
            say(f"    {pname} OOS reference: SPY {sm['CAGR']:.2%}/{sm['Sharpe']:.3f}/"
                f"{sm['MaxDD']:.2%}   RULES v1 {vm['CAGR']:.2%}/{vm['Sharpe']:.3f}/{vm['MaxDD']:.2%}")

    # ---------------------------------------------------------------- verdict
    say("\n" + "=" * 200)
    say("VERDICT")
    say(f"  Q1: cross-universe breakevens (bps) — "
        + "; ".join(f"{nm}: {X.loc[k, 'cross']}" for k, nm in NAMED.items() if k in X.index))
    say(f"  Q2: first-failing bar counts {fails}")
    if len(both) >= 3:
        say(f"  Q3: IS->OOS breakeven spread mean {both.spread.mean():+.1f} bps "
            f"(range {both.spread.min():+.1f}..{both.spread.max():+.1f}), "
            f"Spearman {H.spearman(both.IS.values, both.OOS.values):+.3f}")
    say("  NO NEW BOOK IS PROPOSED.  This run re-prices existing candidate books on a cost axis.")

    F.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False, compression="gzip")
    BE.to_csv(OUT / f"{STEM}.breakevens.csv", index=False)
    X.to_csv(OUT / f"{STEM}.cross.csv")
    Q2.to_csv(OUT / f"{STEM}.binding_bar.csv", index=False)
    J.to_csv(OUT / f"{STEM}.walkforward.csv")
    PW.to_csv(OUT / f"{STEM}.walkforward_panel.csv")
    Q4.to_csv(OUT / f"{STEM}.bargrid.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say("\nwrote: .grid.csv.gz .breakevens.csv .cross.csv .binding_bar.csv .walkforward.csv "
        ".walkforward_panel.csv .bargrid.csv .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
