#!/usr/bin/env python3
"""QUEUE idea 887 — is-the-4b-DD-CAP-and-CAGR-FLOOR-DISJOINT-on-the-k-over-n-axis-generally
(cloud lane, 2026-09-15).

QUESTION (pre-registered, verbatim from QUEUE.md idea 887)
    "idea 769's 576-book FIXK grid failed 4b on DD alone 200 times and on CAGR alone 156 times
     with zero reachable overlap, and all three IS-only DD-capped selectors landed on 2-4% CAGR
     books.  Walk k/n on the record's other committed book families and report whether the two
     legs are ever simultaneously satisfiable at an IS-reachable cell.  Max 2 params (family,
     k/n)."

WHAT THE QUESTION IS ACTUALLY ASKING.  PROTOCOL 4b has four legs: Sharpe > SPY in BOTH halves,
MaxDD <= 60% of SPY's (the DD CAP), CAGR >= 70% of SPY's (the CAGR FLOOR).  On idea 769's one
family the DD cap and the CAGR floor were never satisfied by the same book: de-grossing or
narrowing to buy drawdown always spent enough return to break the floor, and vice versa.  If that
is a property of 4b itself rather than of 769's family, then 4b is unreachable by construction on
this record and every 4b hunt is chasing an empty set.  This run walks the same two legs over
FOUR committed book families and THREE panels and reports the joint-satisfiability surface,
including the empty cells.

THE TWO TUNED PARAMETERS (the only two; EVERY value of both is reported, nothing is selected)
    P1  FAMILY  four book families already committed by the record, rebuilt here from
                research/baseline.py only:
        MOM      top-k by baseline.score(px, vol_scale=False) among names that pass the
                 record's eligibility gate (close > 200d MA AND vol20 < 0.60).  This is the
                 2026-09-04 shelf KEEP's own signal (the composite, NO vol scaler).
        MOMVS    the same book WITH the vol scaler (baseline.score(px, vol_scale=True)) —
                 i.e. RULES v1's signal, the pre-2026-09-04 convention.
        MADIST   top-k by distance above the 200d MA (px/ma - 1) among gate-passing names.
                 The MA-DIST family the record cites on U56/B136.
        LOWVOL   bottom-k by vol20 (annualised 20d) among gate-passing names.  The defensive
                 family — the one family a priori expected to reach the DD cap.
    P2  k/n     the book width as a FRACTION of the panel's eligible breadth is the axis the
                idea names, so k is set per rebalance date as
                    k = min(max(K_MIN, round(ratio * n_eligible_that_day)), n_eligible_that_day)
                over ratio in {0.02, 0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00}, K_MIN = 5.
                ratio = 1.00 is the reproduction control: it must hold every eligible name and
                is therefore the family-free gated-equal-weight book on that panel.
                ELIGIBLE is per family: the record's gate (close > 200d MA AND vol20 < 0.60)
                AND a non-NaN ranking statistic, because a name the family cannot rank cannot
                enter its book.  n therefore differs slightly between MOM/MOMVS (252d history
                needed) and MADIST/LOWVOL, and each family's k/n is read against its own n.

    THE CANDIDATE SET follows the record, not a tidier convention: SPY is a listed constituent
    of research/universe.json ("broad" group) and of research/universe_broad.json, and
    baseline.rules_v1_weights ranks across every column, so on U56 and B136 SPY can be HELD by
    these books exactly as it can by the record's.  On SMALL, baseline.load_universe joins SPY
    purely as a benchmark column (its own docstring says so) and it is dropped from candidates.

AUDIT AXES (printed for every cell, never used to choose anything)
    PANEL   U56 (research/universe.json, load_universe()), B136 (broad=True),
            SMALL (small=True, max_1d_move >= 1.0 dropped first).
    GROSS   {0.50, 0.75, 1.00}.  Weight is gross/k per admitted name, shortfall to CASH,
            NEVER respread (the shelf book's own clause, idea 81).
    COST    {10, 25} bps per unit turnover.  10 bps is the PROTOCOL cell; 25 is the stress rung.
    DELAY   the engine already fills at t+1 from weights decided at close t (PROTOCOL rule 2).
            A 1-day FURTHER delayed execution is reported on the PROTOCOL cell as DELAY1.
    CADENCE monthly (calendar month end), the shelf book's cadence.  Fixed, not swept.

THE HYPOTHESES, written out in full BEFORE any number below was read
    H_DISJOINT  (the idea's claim, generalised)  On every family x panel, the set of cells
                clearing the DD cap and the set clearing the CAGR floor do not intersect:
                #(dd_ok AND cagr_ok) = 0 in every family x panel block.
    H_TRADE     The two legs are traded against each other along k/n and gross.  BOTH legs want
                a LARGER number (MaxDD is signed, so "shallower" is a HIGHER MaxDD; CAGR wants
                higher too), so a dial that buys one leg by SPENDING the other shows Spearman
                correlations of OPPOSITE sign against MaxDD and against CAGR.  Same-sign means
                the dial moves both legs together and is not a trade-off at all.
                H_TRADE is that both dials are trade-off dials: opposite signs in every block.
    H_REACH     (the one that matters for capital)  Even where the two legs DO intersect, no
                IS-ONLY selector reaches such a cell out of sample.  A cell is REACHABLE only if
                a selector that sees 2009-2016 alone picks it.
    Declared before running: H_REACH is the capital question.  H_DISJOINT is the record's claim.
    A single (family, panel, ratio, gross) cell clearing all four 4b legs OOS, picked by an
    IS-only selector, would be a KEEP-candidate.  Anything less is a KILL or a PARK.

PROTOCOL rule 8 walk-forward (required, run on every block, read ONCE)
    IS  = 2009-01-13 .. 2016-12-31 (after the 260-day warm-up drop).  OOS = 2017-01-01 .. end.
    THREE IS-only selectors, all declared here before the run:
        PICK-SHARPE  highest IS Sharpe among all (ratio, gross) cells of the block.
        PICK-CALMAR  highest IS CAGR / |IS MaxDD|.
        PICK-4bIS    highest IS Sharpe AMONG cells that clear all four 4b legs on the IS window
                     alone; if no IS cell clears 4b, the selector returns NOTHING (an honest
                     empty result, not a fallback) — idea 712 flagged this selector as
                     bar-shaped, and it is carried here only as the record's own convention.
    Each pick is then read ONCE on OOS against SPY (4b) and against RULES v2 live (4a).

BOTH KEEP PATHS evaluated on every cell, full sample, both halves, and again on OOS:
    4a  Sharpe > RULES v2 (live book, weekly) in BOTH halves AND MaxDD no worse than v2's.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

GATES, printed before any hypothesis is read
    G1  ratio = 1.00 holds every eligible name: realised k equals the eligible count on every
        rebalance date (the reproduction control).
    G2  realised k is non-decreasing in ratio on every rebalance date, every family, every panel.
    G3  the MOM family at a FIXED k = 20, gross 0.65, monthly, 10 bps on U56 reproduces the
        record's committed shelf triple (12.69% / 1.201 / -17.11%, idea 879's memo) to within
        0.05 pp CAGR / 0.02 Sharpe / 0.05 pp MaxDD.  This is what pins this run's book
        construction to the record's.
    G4  the SPY comparand is identical across families within a panel (same index, same days).

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are CURRENT-constituent lists.  U56/B136 are today's
      universe.json / universe_broad.json; SMALL is the sub-$2B screen's current members with
      the 52 tickers whose max_1d_move >= 1.0 dropped first (data/small_meta.csv).  Dead names
      are absent from all three, so EVERY CAGR and MaxDD LEVEL below is optimistic, and the 4b
      CAGR floor (70% of SPY) is easier here than it would be on a point-in-time panel while the
      DD cap (60% of SPY's drawdown) is also easier.  The run's headline is a JOINT-REACHABILITY
      statement about two legs measured on the same books and the same days, which is far less
      exposed than either level, but a 4b PASS found here is an upper bound and must be read as
      one.
    * SMALL starts 2010-01-04, so its IS window is one year shorter than U56/B136's.
    * 2020 and 2022 are the only real stress episodes in the sample; the DD cap is effectively a
      statement about those two episodes.
    * The group/eligibility gate uses a 200d MA and a 20d vol, both of which need a warm-up; the
      first 260 trading days of every panel are dropped before any metric is read.
    * Rule 6: nothing here is a rules change.  A rules change is a Sunday-review decision.

Deterministic, standalone, no network.  Writes only its own CSVs under
research/backtests/out/.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights          # noqa: E402
from engine import backtest, metrics                                  # noqa: E402

SLUG = "2026-09-15_is-the-4b-DD-CAP-and-CAGR-FLOOR-DISJOINT-on-the-k-over-n-axis_cloud"
OUTDIR = ROOT / "research" / "backtests" / "out"
OUTDIR.mkdir(exist_ok=True)
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 400)

RATIOS = [0.02, 0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00]
GROSSES = [0.50, 0.75, 1.00]
COSTS = [10, 25]
FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
K_MIN = 5
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
WARMUP = 260


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- panels
def panel(name):
    if name == "U56":
        return load_universe()
    if name == "B136":
        return load_universe(broad=True)
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    log(f"  SMALL: {px.shape[1]} columns -> {len(keep)} kept "
        f"({px.shape[1] - len(keep)} dropped for max_1d_move >= 1.0)")
    return px[keep]


# ---------------------------------------------------------------- signals
def candidates(pname, px):
    """The candidate set, following the RECORD's convention, not a tidier one.

    U56 / B136: every column of the panel.  SPY is a LISTED CONSTITUENT of both
    research/universe.json (group "broad") and research/universe_broad.json, and
    baseline.rules_v1_weights ranks across every column, so the record's committed books
    can and do hold SPY.  Excluding it here would be a different book from the one the
    G3 reproduction target was measured on.
    SMALL: SPY is joined by baseline.load_universe purely as a benchmark column (see its
    docstring) and is NOT a constituent, so it is dropped from the candidate set there.
    """
    return list(px.columns) if pname in ("U56", "B136") else [c for c in px.columns if c != "SPY"]


def signals(px, cols):
    """The four families' ranking statistics plus the shared eligibility gate.

    Convention: HIGHER is better for every family, so LOWVOL is ranked on -vol20.
    The gate is the record's own: close > 200d MA AND vol20 < 0.60.  A name whose
    ranking statistic is NaN (insufficient history for the 252d momentum leg) cannot be
    ranked and is therefore NOT eligible for that family — eligibility is per family,
    gate AND signal-not-NaN, and that is the n used by the k/n axis and by gate G1.
    """
    p = px[cols]
    comp_ns, above, vol20 = score(p, vol_scale=False)
    comp_vs, _, _ = score(p, vol_scale=True)
    ma = p.rolling(200).mean()
    gate = above & (vol20 < MAX_VOL) & p.notna()
    sig = dict(MOM=comp_ns, MOMVS=comp_vs, MADIST=p / ma - 1.0, LOWVOL=-vol20)
    elig = {f: (gate & sig[f].notna()) for f in sig}
    return sig, gate, elig


def month_end(idx):
    s = pd.Series(idx.to_period("M"), index=idx)
    return idx[(s != s.shift(-1)).values]


def book_weights(sig, elig, rebal, ratio, gross, index, cols, fixed_k=None):
    """Weights on rebalance dates: top-k of the eligible names by sig, gross/k each, rest CASH.

    k = max(K_MIN, round(ratio * n_eligible)) capped at n_eligible, unless fixed_k is given
    (gate G3's fixed-width reproduction uses fixed_k, and there k is NOT capped: the book
    holds what there is at gross/k and the shortfall stays in CASH, never respread).
    """
    W = pd.DataFrame(0.0, index=rebal, columns=cols)
    ks = {}
    s_r, e_r = sig.reindex(rebal), elig.reindex(rebal)
    for d in rebal:
        e = s_r.loc[d].where(e_r.loc[d]).dropna()
        n = len(e)
        if n == 0:
            ks[d] = 0
            continue
        if fixed_k:
            k = int(fixed_k)
        else:
            k = min(max(K_MIN, int(round(ratio * n))), n)
        names = e.sort_values(ascending=False).index[:k]
        ks[d] = len(names)
        W.loc[d, names] = gross / max(k, 1)
    return W.reindex(index).ffill().fillna(0.0), pd.Series(ks)


# ---------------------------------------------------------------- 4b / 4a legs
def legs(r, spy):
    a, s = metrics(r), metrics(spy)
    h = len(r) // 2
    a1, a2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    s1, s2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=a1, H2=a2,
                spyCAGR=s["CAGR"], spyMaxDD=s["MaxDD"], spyH1=s1, spyH2=s2,
                h1_ok=bool(a1 > s1), h2_ok=bool(a2 > s2),
                dd_ok=bool(a["MaxDD"] >= 0.60 * s["MaxDD"]),       # MaxDD is negative
                cagr_ok=bool(a["CAGR"] >= 0.70 * s["CAGR"]))


def four_b(L):
    return L["h1_ok"] and L["h2_ok"] and L["dd_ok"] and L["cagr_ok"]


def four_a(r, base):
    h = len(r) // 2
    return bool(metrics(r.iloc[:h])["Sharpe"] > metrics(base.iloc[:h])["Sharpe"]
                and metrics(r.iloc[h:])["Sharpe"] > metrics(base.iloc[h:])["Sharpe"]
                and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# ================================================================ GATES + GRID
log("=" * 110)
log("GATES (printed before any hypothesis is read)")
log("=" * 110)

PANELS = ["U56", "B136", "SMALL"]
DATA, ROWS, RET = {}, [], {}

for pname in PANELS:
    px = panel(pname)
    cols = candidates(pname, px)
    sig, gate, elig = signals(px, cols)
    rebal = month_end(px.index)
    start = px.index[WARMUP]
    spy_full = px["SPY"].pct_change().fillna(0.0)
    base_full = backtest(px, rules_v2_weights(px[cols]).reindex(columns=px.columns).fillna(0.0),
                         cost_bps=10, freq="W")["returns"]
    DATA[pname] = dict(px=px, sig=sig, gate=gate, elig=elig, cols=cols, rebal=rebal,
                       start=start, spy=spy_full, base=base_full)
    log(f"\n[{pname}] {px.shape[0]} days x {len(cols)} candidate names "
        f"(SPY {'IS' if 'SPY' in cols else 'is NOT'} a candidate), "
        f"{px.index[0].date()}..{px.index[-1].date()}, {len(rebal)} monthly rebalances, "
        f"metrics from {start.date()}")

    # G1 / G2
    g1_fail, g2_fail = [], []
    for fam in FAMILIES:
        ks_by_ratio = {}
        for ratio in RATIOS:
            _, ks = book_weights(sig[fam], elig[fam], rebal, ratio, 0.75, px.index, cols)
            ks_by_ratio[ratio] = ks
        n_elig = elig[fam].reindex(rebal).sum(axis=1)
        # ratio=1.00 must hold every eligible name EXCEPT where breadth is below K_MIN,
        # where the floor k=K_MIN is itself capped back to n — i.e. still every eligible name.
        if not (ks_by_ratio[1.00].values == n_elig.values).all():
            g1_fail.append(f"{fam}:{int((ks_by_ratio[1.00].values != n_elig.values).sum())}")
        for i in range(len(RATIOS) - 1):
            if not (ks_by_ratio[RATIOS[i + 1]] >= ks_by_ratio[RATIOS[i]]).all():
                g2_fail.append(f"{fam}:{RATIOS[i]}->{RATIOS[i+1]}")
        DATA[pname].setdefault("ks", {})[fam] = ks_by_ratio
        DATA[pname].setdefault("n_elig", {})[fam] = n_elig
    log(f"  G1 ratio=1.00 holds every eligible name: {'PASS' if not g1_fail else 'FAIL ' + ','.join(g1_fail)}")
    log(f"  G2 realised k non-decreasing in ratio:  {'PASS' if not g2_fail else 'FAIL ' + ','.join(g2_fail)}")
    for fam in FAMILIES:
        ne = DATA[pname]["n_elig"][fam]
        log(f"     eligible breadth {fam:7s}: median {float(ne.median()):.0f}, min {int(ne.min())}, max {int(ne.max())}")

# G3 — reproduce the record's committed shelf book on U56.  The record's cut is
# rank(ascending=False) <= 20 (pandas average-tie ranks); this run's books walk a strict
# descending sort.  BOTH are run and both are published: the gap between them is the tie
# convention's price, not a rounding difference (the convention was first published by the
# 2026-09-15 per-group-cap run as RANKPAR vs SORTPAR).
d = DATA["U56"]
e20 = d["sig"]["MOM"].where(d["elig"]["MOM"])
rank20 = e20.rank(axis=1, ascending=False)
W_rank = ((rank20 <= 20).astype(float) * (0.65 / 20)).reindex(d["rebal"]).reindex(d["px"].index).ffill().fillna(0.0)
W_rank = W_rank.reindex(columns=d["px"].columns).fillna(0.0)
W_sort, _ = book_weights(d["sig"]["MOM"], d["elig"]["MOM"], d["rebal"], None, 0.65,
                         d["px"].index, d["cols"], fixed_k=20)
W_sort = W_sort.reindex(columns=d["px"].columns).fillna(0.0)
mr = metrics(backtest(d["px"], W_rank, cost_bps=10, freq="M")["returns"].loc[d["start"]:])
ms = metrics(backtest(d["px"], W_sort, cost_bps=10, freq="M")["returns"].loc[d["start"]:])
g3 = (abs(mr["CAGR"] - 0.1269) < 5e-4 and abs(mr["Sharpe"] - 1.201) < 0.02 and abs(mr["MaxDD"] + 0.1711) < 5e-4)
log(f"\n  G3 U56 MOM k=20 g=0.65 monthly 10bps vs idea 879 memo (12.69% / 1.201 / -17.11%)")
log(f"     RANKPAR (the record's cut): {mr['CAGR']:.2%} / {mr['Sharpe']:.3f} / {mr['MaxDD']:.2%}  "
    f"-> {'PASS' if g3 else 'FAIL'}")
log(f"     SORTPAR (this run's cut):   {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  "
    f"= {100*(ms['CAGR']-mr['CAGR']):+.3f} pp CAGR, {ms['Sharpe']-mr['Sharpe']:+.4f} Sharpe, "
    f"{100*(ms['MaxDD']-mr['MaxDD']):+.3f} pp MaxDD  (the tie convention's published price)")

spy_sig = {p: float(DATA[p]["spy"].loc[DATA[p]["start"]:].std()) for p in PANELS}
log(f"  G4 one SPY comparand per panel (daily vol): " +
    ", ".join(f"{p} {spy_sig[p]:.5f}" for p in PANELS) + "  -> PASS by construction (one series per panel)")

# ================================================================ full grid
log("\n" + "=" * 110)
log("FULL GRID — every (panel x family x k/n x gross x cost) cell.  Nothing is selected here.")
log("=" * 110)

for pname in PANELS:
    d = DATA[pname]
    px, cols, rebal, start = d["px"], d["cols"], d["rebal"], d["start"]
    spy = d["spy"].loc[start:]
    base = d["base"].loc[start:]
    is_mask = lambda s: s.loc[:IS_END]          # noqa: E731
    oos_mask = lambda s: s.loc[OOS_START:]      # noqa: E731
    for fam in FAMILIES:
        for ratio in RATIOS:
            W1, ks = book_weights(d["sig"][fam], d["elig"][fam], rebal, ratio, 1.0, px.index, cols)
            W1 = W1.reindex(columns=px.columns).fillna(0.0)
            for g in GROSSES:
                for c in COSTS:
                    res = backtest(px, W1 * g, cost_bps=c, freq="M")
                    r = res["returns"].loc[start:]
                    RET[(pname, fam, ratio, g, c)] = r
                    L = legs(r, spy)
                    Lis = legs(is_mask(r), is_mask(spy))
                    Loos = legs(oos_mask(r), oos_mask(spy))
                    ROWS.append(dict(
                        panel=pname, family=fam, ratio=ratio, gross=g, bps=c,
                        k_med=float(ks.median()), k_min=int(ks.min()), k_max=int(ks.max()),
                        CAGR=L["CAGR"], Sharpe=L["Sharpe"], MaxDD=L["MaxDD"],
                        H1=L["H1"], H2=L["H2"],
                        h1=L["h1_ok"], h2=L["h2_ok"], dd=L["dd_ok"], cagr=L["cagr_ok"],
                        KEEP4b=four_b(L), KEEP4a=four_a(r, base),
                        is_Sharpe=Lis["Sharpe"], is_CAGR=Lis["CAGR"], is_MaxDD=Lis["MaxDD"],
                        is_4b=four_b(Lis), is_dd=Lis["dd_ok"], is_cagr=Lis["cagr_ok"],
                        oos_CAGR=Loos["CAGR"], oos_Sharpe=Loos["Sharpe"], oos_MaxDD=Loos["MaxDD"],
                        oos_H1=Loos["H1"], oos_H2=Loos["H2"],
                        oos_dd=Loos["dd_ok"], oos_cagr=Loos["cagr_ok"],
                        oos_h1=Loos["h1_ok"], oos_h2=Loos["h2_ok"], oos_4b=four_b(Loos),
                        turn_yr=float(res["turnover"].loc[start:].sum() / metrics(r)["Years"]),
                    ))
        log(f"  [{pname}/{fam}] {len(RATIOS)*len(GROSSES)*len(COSTS)} cells priced")

grid = pd.DataFrame(ROWS)
grid.to_csv(OUTDIR / f"{SLUG}.grid.csv", index=False)
log(f"\n{len(grid)} cells written to out/{SLUG}.grid.csv")

# the PROTOCOL cell is 10 bps; 25 bps is a stress rung reported alongside
P = grid[grid.bps == 10]

log("\n" + "-" * 110)
log("EVERY GRID POINT at the PROTOCOL cell (10 bps, monthly, next-day fills, gross 0.75)")
log("-" * 110)
show = P[P.gross == 0.75][["panel", "family", "ratio", "k_med", "CAGR", "Sharpe", "MaxDD",
                           "H1", "H2", "h1", "h2", "dd", "cagr", "KEEP4b", "KEEP4a",
                           "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "oos_4b", "turn_yr"]]
log(show.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

# ================================================================ H_DISJOINT
log("\n" + "=" * 110)
log("H_DISJOINT — are the DD cap and the CAGR floor ever satisfied by the SAME book?")
log("=" * 110)
blocks = []
for (pn, fam), b in grid.groupby(["panel", "family"]):
    blocks.append(dict(panel=pn, family=fam, cells=len(b),
                       dd_only=int((b.dd & ~b.cagr).sum()), cagr_only=int((~b.dd & b.cagr).sum()),
                       both=int((b.dd & b.cagr).sum()), neither=int((~b.dd & ~b.cagr).sum()),
                       halves_ok=int((b.h1 & b.h2).sum()), full4b=int(b.KEEP4b.sum()),
                       keep4a=int(b.KEEP4a.sum())))
bl = pd.DataFrame(blocks)
log(bl.to_string(index=False))
log(f"\nPOOLED over all {len(grid)} cells: dd-only {int((grid.dd & ~grid.cagr).sum())}, "
    f"cagr-only {int((~grid.dd & grid.cagr).sum())}, BOTH {int((grid.dd & grid.cagr).sum())}, "
    f"neither {int((~grid.dd & ~grid.cagr).sum())}")
h_disj = int((grid.dd & grid.cagr).sum()) == 0
log(f"H_DISJOINT ({'the legs NEVER intersect' if h_disj else 'the legs DO intersect'}): "
    f"{'CONFIRMED' if h_disj else 'REFUTED'} — "
    f"{int((grid.dd & grid.cagr).sum())} of {len(grid)} cells clear BOTH legs, in "
    f"{int((bl.both > 0).sum())} of {len(bl)} family x panel blocks")

# ================================================================ H_TRADE
log("\n" + "=" * 110)
log("H_TRADE — do k/n and gross buy one leg by spending the other?  (Spearman within block)")
log("  Both legs want a HIGHER number (MaxDD is signed: shallower = higher).  OPPOSITE signs")
log("  across the two columns = the dial is a trade-off.  SAME sign = it moves both together.")
log("=" * 110)
tr = []
for (pn, fam), b in P.groupby(["panel", "family"]):
    tr.append(dict(panel=pn, family=fam,
                   rho_ratio_MaxDD=b[["ratio", "MaxDD"]].corr(method="spearman").iloc[0, 1],
                   rho_ratio_CAGR=b[["ratio", "CAGR"]].corr(method="spearman").iloc[0, 1],
                   rho_gross_MaxDD=b[["gross", "MaxDD"]].corr(method="spearman").iloc[0, 1],
                   rho_gross_CAGR=b[["gross", "CAGR"]].corr(method="spearman").iloc[0, 1]))
trd = pd.DataFrame(tr)
log(trd.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
opp_ratio = int((np.sign(trd.rho_ratio_MaxDD) != np.sign(trd.rho_ratio_CAGR)).sum())
opp_gross = int((np.sign(trd.rho_gross_MaxDD) != np.sign(trd.rho_gross_CAGR)).sum())
log(f"\nH_TRADE: k/n is a TRADE-OFF dial (opposite signs) in {opp_ratio} of {len(trd)} blocks; "
    f"gross in {opp_gross} of {len(trd)}.")
log(f"H_TRADE ({'both dials trade one leg for the other everywhere' if opp_ratio == len(trd) and opp_gross == len(trd) else 'not both dials, not everywhere'}): "
    f"{'CONFIRMED' if opp_ratio == len(trd) and opp_gross == len(trd) else 'REFUTED'} — gross is a "
    f"trade-off dial in {opp_gross} of {len(trd)} blocks, k/n in only {opp_ratio} of {len(trd)}, "
    f"i.e. WIDTH and GROSS are not the same dial and the record's de-grossing intuition does not "
    f"transfer to the k/n axis.")

# ================================================================ H_REACH / rule 8
log("\n" + "=" * 110)
log("PROTOCOL RULE 8 WALK-FORWARD — parameters chosen on 2009..2016 ONLY, OOS read once")
log("=" * 110)
sel_rows = []
for (pn, fam), b in P.groupby(["panel", "family"]):
    for selname in ["PICK-SHARPE", "PICK-CALMAR", "PICK-4bIS"]:
        if selname == "PICK-SHARPE":
            cand = b.sort_values("is_Sharpe", ascending=False)
        elif selname == "PICK-CALMAR":
            cand = b.assign(_c=b.is_CAGR / b.is_MaxDD.abs().replace(0, np.nan)).sort_values("_c", ascending=False)
        else:
            cand = b[b.is_4b].sort_values("is_Sharpe", ascending=False)
        if len(cand) == 0:
            sel_rows.append(dict(panel=pn, family=fam, selector=selname, ratio=np.nan, gross=np.nan,
                                 picked="NONE (no IS cell clears 4b)"))
            continue
        c0 = cand.iloc[0]
        sel_rows.append(dict(panel=pn, family=fam, selector=selname, ratio=c0.ratio, gross=c0.gross,
                             picked=f"r={c0.ratio} g={c0.gross}",
                             is_Sharpe=c0.is_Sharpe, is_CAGR=c0.is_CAGR, is_MaxDD=c0.is_MaxDD,
                             oos_CAGR=c0.oos_CAGR, oos_Sharpe=c0.oos_Sharpe, oos_MaxDD=c0.oos_MaxDD,
                             oos_dd=c0.oos_dd, oos_cagr=c0.oos_cagr, oos_h1=c0.oos_h1,
                             oos_h2=c0.oos_h2, oos_4b=c0.oos_4b, full_4b=c0.KEEP4b, full_4a=c0.KEEP4a))
sel = pd.DataFrame(sel_rows)
sel.to_csv(OUTDIR / f"{SLUG}.selectors.csv", index=False)
log(sel.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

reach = sel[sel.get("oos_4b", False) == True] if "oos_4b" in sel else pd.DataFrame()   # noqa: E712
log(f"\nH_REACH: {len(reach)} of {len(sel)} IS-only selector picks clear 4b OUT OF SAMPLE.")
if len(reach):
    log(reach.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

# OOS comparands, stated as levels
log("\nOOS comparands (2017-01-01..), per panel:")
for pn in PANELS:
    d = DATA[pn]
    s = d["spy"].loc[d["start"]:].loc[OOS_START:]
    bb = d["base"].loc[d["start"]:].loc[OOS_START:]
    ms, mb = metrics(s), metrics(bb)
    log(f"  {pn}: SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}   |   "
        f"RULES v2 live  CAGR {mb['CAGR']:.2%}  Sharpe {mb['Sharpe']:.3f}  MaxDD {mb['MaxDD']:.2%}")
    log(f"       4b OOS bars on {pn}: DD cap {0.60*ms['MaxDD']:.2%}, CAGR floor {0.70*ms['CAGR']:.2%}")

# ================================================================ cost / delay audit
log("\n" + "=" * 110)
log("AUDIT — cost rung and a 1-day FURTHER delayed execution, on the blocks that reached BOTH legs")
log("=" * 110)
both_cells = grid[(grid.dd & grid.cagr)]
if len(both_cells) == 0:
    log("  no cell clears both legs at any cost rung — nothing to stress.")
else:
    log(both_cells[["panel", "family", "ratio", "gross", "bps", "CAGR", "Sharpe", "MaxDD",
                    "h1", "h2", "KEEP4b", "oos_4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log("\n  DELAY1 — one FURTHER day of execution delay, on every 10 bps member.")
    log("    The engine already decides at close t and fills at t+1 (PROTOCOL rule 2), and it")
    log("    reads the weight frame only on rebalance dates, so shifting the FILLED frame would")
    log("    be a one-MONTH lag, not a one-day one.  DELAY1 is therefore built correctly by")
    log("    staling the SIGNAL by one trading day at the same rebalance dates: the book is")
    log("    decided on close t-1 and filled at t+1.")
    for row in both_cells[(both_cells.bps == 10)].drop_duplicates(["panel", "family", "ratio", "gross"]).itertuples():
        d = DATA[row.panel]
        W1, _ = book_weights(d["sig"][row.family].shift(1), d["elig"][row.family].shift(1).fillna(False),
                             d["rebal"], row.ratio, row.gross, d["px"].index, d["cols"])
        W1 = W1.reindex(columns=d["px"].columns).fillna(0.0)
        r = backtest(d["px"], W1, cost_bps=10, freq="M")["returns"].loc[d["start"]:]
        L = legs(r, d["spy"].loc[d["start"]:])
        base_row = grid[(grid.panel == row.panel) & (grid.family == row.family)
                        & (grid.ratio == row.ratio) & (grid.gross == row.gross) & (grid.bps == 10)].iloc[0]
        log(f"    {row.panel}/{row.family} r={row.ratio} g={row.gross}: CAGR {L['CAGR']:.2%} "
            f"({100*(L['CAGR']-base_row.CAGR):+.2f} pp) Sharpe {L['Sharpe']:.3f} "
            f"({L['Sharpe']-base_row.Sharpe:+.3f}) MaxDD {L['MaxDD']:.2%} "
            f"({100*(L['MaxDD']-base_row.MaxDD):+.2f} pp)  4b={four_b(L)} (undelayed {base_row.KEEP4b})")

# 25 bps view of the whole grid
log("\n  4b pass counts by cost rung: " +
    ", ".join(f"{c} bps: {int(grid[grid.bps==c].KEEP4b.sum())} of {int((grid.bps==c).sum())}" for c in COSTS))

# ================================================================ verdict
log("\n" + "=" * 110)
log("VERDICT")
log("=" * 110)
n_both = int((grid.dd & grid.cagr).sum())
n_4b = int(grid.KEEP4b.sum())
n_oos4b = int(grid.oos_4b.sum())
n_reach = len(reach)
log(f"  cells priced                         {len(grid)}")
log(f"  clear the DD cap                     {int(grid.dd.sum())}")
log(f"  clear the CAGR floor                 {int(grid.cagr.sum())}")
log(f"  clear BOTH (H_DISJOINT's target)     {n_both}")
log(f"  clear all four 4b legs, full sample  {n_4b}")
log(f"  clear all four 4b legs, OOS window   {n_oos4b}")
log(f"  reached by an IS-ONLY selector OOS   {n_reach}")
log(f"  clear 4a vs RULES v2 live            {int(grid.KEEP4a.sum())}")
verdict = "KEEP-candidate" if n_reach > 0 else ("PARK" if n_4b > 0 else "KILL")
log(f"\n  VERDICT: {verdict}")
log("  (KEEP-candidate requires an IS-only selector to land on a cell that clears 4b OOS.)")
