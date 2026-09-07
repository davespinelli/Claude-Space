#!/usr/bin/env python3
"""QUEUE idea 379 — is-the-priceability-floor-the-real-selector (lane B, 2026-09-07).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 124 found the published set shrinks with concentration (u56 [18,12,22,22,24,24] priced
rows at n=3..all) and that this alone manufactures idea 122's non-monotone curve.  Test idea
94's 0.10pp dMaxDD floor directly: sweep it over {0, 0.05, 0.10, 0.25, 0.50} pp and ask
whether ANY published book-level ranking in the record is invariant to it.  Max 2 params."

What is being measured
----------------------
Every quoted price in the record has the form

    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)      pp CAGR per pp MaxDD

and idea 94 declined to publish the row unless its DENOMINATOR cleared an absolute floor,

    published(row)  <=>  dMaxDD > FLOOR,   FLOOR = 0.10 pp                (idea 94's rule)

That floor was never itself priced.  It is a SELECTION RULE applied before every book-level
ordering the record quotes, and idea 124 showed the set it admits shrinks with book
concentration, so the floor could be manufacturing the orderings rather than cleaning them.

This run holds the ENTIRE price grid fixed (idea 124's TOP-n ladder + the off-ladder V1u, on
both panels, at both published cost rungs, with idea 94's 16 instruments) and moves ONLY the
floor.  Nothing in the returns, the books, the arms or the windows changes across the sweep:
by construction the sweep isolates the publication rule.

Three floor-INDEPENDENT quantities are re-used exactly as idea 124 computed them, because
they are functions of the returns and not of the floor:
    D1  sign of dMaxDD across the 4 cost rungs      (grid column, recomputed here)
    D2  sign of dMaxDD in the IS and the OOS window (grid column, recomputed here)
    D3  fraction of panel draws with dMaxDD > 0     (idea 124's committed d3.csv, q = 0.10)
`admissible` = D1 AND D2 AND D3 >= tau is therefore CONSTANT over the sweep; only
`published` moves.  That is the whole design.

Rankings under test (the record's book-level orderings, fixed before any number was read)
    K0  adm_all  per book — admissible share over ALL 32 rows.  CONTROL: invariant by
        construction, reported so the sweep's null is visible.
    K1  adm_pub  per book — idea 124's floor curve, admissible share over PUBLISHED rows.
        This is the statistic idea 124 flagged as conditioned on a shrinking set.
    K2  n*       per panel — idea 124's floor number, smallest ladder rung with adm_pub >= 0.90.
    K3  median published rate per book at 10 bps — "which book buys the cheapest insurance".
    K4  idea 94's ARM MENU — the 16 instruments ordered by median rate over cells, on idea
        94's own 3-book cell set (V1u/TOP20/EWall x 2 panels) and on the 7-book ladder.

Invariance bar, pre-registered before any number was read
    A ranking is INVARIANT iff, over all five floors, the surviving entry set is unchanged AND
    the complete ordering is identical (Spearman = 1.000 against the phi = 0.10 incumbent, zero
    pair inversions, same argmin and argmax).  Spearman, inversion counts, dropout counts and
    argmin/argmax are printed at every floor so any weaker bar can be read off the table.

Pre-registered predictions (written before any number was read)
    P1  K0 is invariant (a construction check on the harness, not a result).
    P2  K1 is NOT invariant on either panel: idea 124's own row counts already move with n, so
        moving the floor should move the curve.
    P3  K4, the ARM menu, IS invariant: idea 94's instruments differ in dMaxDD by whole
        percentage points, far above a 0.50 pp floor, so the menu should not care.
    P4  n* is not invariant on at least one panel.

Tuned parameters (PROTOCOL rule 4): TWO, and neither is chosen on a result.
    phi   the publication floor, in {0.00, 0.05, 0.10, 0.25, 0.50} pp  — THE SUBJECT AXIS,
          all five points reported everywhere; phi = 0.10 is the incumbent, not a choice.
    cost  the published rung, in {10, 25} bps — both reported everywhere.
q = 0.10 and tau = 0.90 (the D3 axis) are inherited UNCHANGED from ideas 119/122/124 and the
1.0 pp reach threshold in selector S1 is inherited UNCHANGED from idea 94; none is swept here.

Rule 8 walk-forward (PROTOCOL rule 8), both legs fixed before any OOS number was read
    W1  The FLOOR CURVE itself: recompute K1/K2 on 2009-2016 only (D1 on IS returns, D3 on IS
        draws, publication on IS dMaxDD — idea 124's IS screen) at every floor, then read the
        2017-2026 curve untouched.  Report n*_IS -> n*_OOS per floor.
    W2  The FLOOR AS A SELECTOR.  In each (uni, book, cost) cell:
          S1 = idea 94's selector — among arms buying >= 1.0 pp of IS MaxDD, the LOWEST IS
               rate.  Its reach filter sits ABOVE every floor tested, so S1 is the control.
          S2 = the FLOOR-ONLY selector — among arms PUBLISHED at phi on IS (IS dMaxDD > phi),
               the LOWEST IS rate.  This is the queue's question made operational: it lets the
               floor, rather than a reach threshold, do the choosing.
        Both picks are evaluated UNTOUCHED on 2017-2026: OOS CAGR / Sharpe / MaxDD against the
        cell's own control book, against the LIVE RULES v2 baseline, against RULES v1 and
        against SPY.  Plus spearman(IS rate, OOS rate) within each cell at each floor: a floor
        that improves the ordering's walk-forward is doing real work; one that does not is a
        publication filter with a selection side-effect.

Both KEEP paths (PROTOCOL rule 4) are evaluated for every arm-point at both published rungs,
and additionally re-read per floor: a 4b-passing arm that the floor refuses to publish is a
capital decision the publication rule is silently making.

Execution realism (PROTOCOL rule 2): idea 94's harness verbatim, inherited through idea 124
(weights at close t applied at t+1, weekly, long-only, no leverage, costs inside the loop).
10 bps is the PROTOCOL point; 0/5/25 bps are the D1 sign-test rungs and 25 bps is published.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every
absolute CAGR here is optimistic.  The subject of this run is which rows a publication rule
admits and how a fixed ordering moves, both of which are far less exposed than a level.

Reproduction gates (all must pass or the results below are unsafe)
    G1  my grid reproduces idea 124's committed grid.csv (dCAGR, dMaxDD, all window columns)
    G2  at phi = 0.10 my published-row counts reproduce idea 124's committed floorcurve.csv,
        i.e. the queue's own u56 [18,12,22,22,24,24]
    G3  at phi = 0.10 my adm_pub curve reproduces idea 124's committed floorcurve.csv
    G4  idea 124's gates carry through (ladder nests idea 94's books; run() == engine.backtest)

Deterministic, standalone, modifies nothing.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

sys.path.insert(0, str(ROOT / "products" / "backtester"))

from engine import metrics  # noqa: E402

BT = ROOT / "research" / "backtests"


def _load(mod, fname):
    spec = importlib.util.spec_from_file_location(mod, BT / fname)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = _load("i94", "2026-09-04_drawdown-insurance-price-list_B.py")
I124 = _load("i124", "2026-09-07_book-size-floor-for-any-quoted-price_B.py")

STEM = Path(__file__).stem
OUT = BT / STEM
PARENT = BT / "2026-09-07_book-size-floor-for-any-quoted-price_B"

FLOORS = [0.00, 0.05, 0.10, 0.25, 0.50]     # THE SUBJECT AXIS (pp of MaxDD)
PHI0 = 0.10                                  # idea 94's incumbent
Q_STAR, TAU_STAR, BAR = I124.Q_STAR, I124.TAU_STAR, I124.BAR
PUB_COSTS = I124.PUB_COSTS
COST_RUNGS = I124.COST_RUNGS
BOOKS = I124.BOOKS
UNIS = I124.UNIS
ARMS = I124.ARMS
I94_BOOKS = ["V1u", "TOP20", "TOPall"]       # idea 94's own three books (TOPall == EWall)
REACH = 1.0                                  # idea 94's reach threshold, inherited
OOS_START = H.OOS_START

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 5000)


def fmt(df):
    return df.to_string(index=False, float_format=lambda x: f"{x:.4f}")


def rate_at(dc, dd, phi):
    """idea 94's price, published only when the denominator clears the floor."""
    return np.where(dd > phi, dc / np.where(dd > phi, dd, np.nan), np.nan)


def ordering(vals, keys, ascending=True):
    """Return the ordered tuple of keys with finite values (ties broken by key, so the
    ordering is a deterministic function of the numbers alone)."""
    pairs = [(v, k) for v, k in zip(vals, keys) if np.isfinite(v)]
    pairs.sort(key=lambda t: (t[0] if ascending else -t[0], t[1]))
    return tuple(k for _, k in pairs)


def inversions(o_ref, o_new):
    """Pairs ordered one way in o_ref and the other way in o_new, over their common members."""
    common = [k for k in o_ref if k in o_new]
    ri = {k: i for i, k in enumerate(o_ref)}
    ni = {k: i for i, k in enumerate(o_new)}
    inv = 0
    for i in range(len(common)):
        for j in range(i + 1, len(common)):
            a, b = common[i], common[j]
            if (ri[a] < ri[b]) != (ni[a] < ni[b]):
                inv += 1
    return inv, len(common)


def rank_report(name, panel, phi, o_ref, o_new, v_ref, v_new, keys):
    inv, ncom = inversions(o_ref, o_new)
    sp = H.spearman([v_ref.get(k, np.nan) for k in keys], [v_new.get(k, np.nan) for k in keys])
    return dict(ranking=name, scope=panel, phi=phi, n_entries=len(o_new),
                dropped=len(o_ref) - ncom, added=len([k for k in o_new if k not in o_ref]),
                identical=bool(o_new == o_ref), inversions=inv, spearman=sp,
                argmin=(o_new[0] if o_new else "-"), argmax=(o_new[-1] if o_new else "-"),
                order="|".join(o_new))


# ================================================================= build the price grid
def build():
    G, RET, CTX = [], {}, {}
    for uname, kw in UNIS:
        t0 = time.time()
        px, start, S, spy, bars, rets, g, v1_net, v2_net = I124.build_grid(uname, kw)
        G.append(g)
        RET[uname] = rets
        CTX[uname] = dict(px=px, start=start, spy=spy, bars=bars, v1=v1_net, v2=v2_net,
                          npanel=px.shape[1])
        print(f"[build] {uname}: grid done in {time.time()-t0:.0f}s", flush=True)
    return pd.concat(G, ignore_index=True), RET, CTX


# ================================================================= gates
def gates(G):
    ref = pd.read_csv(f"{PARENT}.grid.csv")
    key = ["uni", "book", "cost", "arm"]
    cols = ["dCAGR", "dMaxDD", "dCAGR_IS", "dMaxDD_IS", "dCAGR_OOS", "dMaxDD_OOS",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"] + \
           [f"dMaxDD@{c:.0f}" for c in COST_RUNGS] + [f"dMaxDD_IS@{c:.0f}" for c in COST_RUNGS]
    m = G[key + cols].merge(ref[key + cols], on=key, suffixes=("", "_ref"))
    worst = max(float((m[c] - m[f"{c}_ref"]).abs().max()) for c in cols)
    print(f"[gate] G1 grid reproduces idea 124's committed grid.csv on {len(m)} rows x "
          f"{len(cols)} cols   max|diff| = {worst:.3e}  ({'PASS' if worst < 1e-9 else 'FAIL'})")
    return worst, m


def gate_floorcurve(C10):
    ref = pd.read_csv(f"{PARENT}.floorcurve.csv")
    m = C10.merge(ref[["uni", "book", "pub", "adm_pub", "adm_all"]], on=["uni", "book"],
                  suffixes=("", "_ref"))
    e_pub = float((m["pub"] - m["pub_ref"]).abs().max())
    e_adm = float(np.nanmax(np.abs(m["adm_pub"].values - m["adm_pub_ref"].values)))
    e_all = float(np.nanmax(np.abs(m["adm_all"].values - m["adm_all_ref"].values)))
    u56 = m[m.uni.str.startswith("universe.json")].sort_values("n")
    print(f"[gate] G2 published-row counts at phi=0.10 vs idea 124   max|diff| = {e_pub:.3e}  "
          f"({'PASS' if e_pub < 1e-9 else 'FAIL'})   u56 ladder = "
          f"{[int(v) for v in u56[u56.ladder].pub.values]}  (queue quotes [18,12,22,22,24,24])")
    print(f"[gate] G3 adm_pub curve at phi=0.10 vs idea 124          max|diff| = {e_adm:.3e}  "
          f"({'PASS' if e_adm < 1e-12 else 'FAIL'})   adm_all max|diff| = {e_all:.3e}")
    return e_pub, e_adm, e_all


# ================================================================= floor sweep machinery
def curve(G, D3, phi, window="full"):
    """(uni, book) admissible / published shares at floor phi.  `admissible` is
    floor-INDEPENDENT (D1 & D2 & D3); only `published` moves with phi."""
    d3 = D3[D3.q == Q_STAR].set_index(["uni", "book", "arm"])
    col = {"full": "frac_pos_full", "IS": "frac_pos_IS", "OOS": "frac_pos_OOS"}[window]
    rows = []
    for r in G.itertuples():
        f = float(d3.loc[(r.uni, r.book, r.arm), col]) if (r.uni, r.book, r.arm) in d3.index else np.nan
        if window == "full":
            ok, dd = bool(r.D1_pass and r.D2_pass and f >= TAU_STAR), r.dMaxDD
        elif window == "IS":
            ok, dd = bool(r.D1_pass_IS and f >= TAU_STAR), r.dMaxDD_IS
        else:
            ok, dd = bool(r.dMaxDD_OOS > 0 and f >= TAU_STAR), r.dMaxDD_OOS
        rows.append(dict(uni=r.uni, book=r.book, n=r.n, ladder=r.ladder, cost=r.cost, arm=r.arm,
                         published=bool(dd > phi), admissible=ok, d3=f))
    A = pd.DataFrame(rows)
    g = A.groupby(["uni", "book", "n", "ladder"])
    C = pd.DataFrame(dict(
        rows=g.size(), adm_all=g.admissible.mean(), pub=g.published.sum(),
        adm_pub=g.apply(lambda d: float(d.admissible[d.published].mean())
                        if d.published.any() else np.nan, include_groups=False),
    )).reset_index().sort_values(["uni", "ladder", "n"], ascending=[True, False, True])
    return A, C


def n_star(C, uni, col="adm_pub"):
    d = C[(C.uni == uni) & C.ladder].sort_values("n")
    for i, (_, r) in enumerate(d.iterrows()):
        if np.isfinite(r[col]) and r[col] >= BAR and bool((d.iloc[i:][col] >= BAR).all()):
            return int(r.n)
    return None


def book_price(G, phi, cost):
    """K3: median published rate per (uni, book) at one cost rung."""
    d = G[G.cost == cost].copy()
    d["rate_phi"] = rate_at(d.dCAGR.values, d.dMaxDD.values, phi)
    return d.groupby(["uni", "book"]).rate_phi.median().reset_index()


def arm_menu(G, phi, cost, books):
    """K4: idea 94's menu — median rate per arm over the (uni, book) cells at one rung."""
    d = G[(G.cost == cost) & (G.book.isin(books))].copy()
    d["rate_phi"] = rate_at(d.dCAGR.values, d.dMaxDD.values, phi)
    return d.groupby("arm").rate_phi.median().reset_index()


# ================================================================= W2: the floor as selector
def selector_table(G, RET, CTX, phi):
    """S1 (idea 94, reach >= 1.0pp) and S2 (floor-only) per (uni, book, cost) cell."""
    out = []
    for uname, _ in UNIS:
        ctx = CTX[uname]
        rets, bars = RET[uname], ctx["bars"]
        spy_oos = ctx["spy"].loc[OOS_START:]
        for book in BOOKS:
            for c in PUB_COSTS:
                d = G[(G.uni == uname) & (G.book == book) & (G.cost == c)].copy()
                d["IS_rate_phi"] = rate_at(d.dCAGR_IS.values, d.dMaxDD_IS.values, phi)
                d["OOS_rate_phi"] = rate_at(d.dCAGR_OOS.values, d.dMaxDD_OOS.values, phi)
                e1 = d[(d.dMaxDD_IS >= REACH) & np.isfinite(d.IS_rate_phi)]
                e2 = d[np.isfinite(d.IS_rate_phi)]
                rec = dict(uni=uname, book=book, n=int(d.n.iloc[0]), cost=c, phi=phi,
                           n_elig_S1=len(e1), n_elig_S2=len(e2),
                           spearman_IS_OOS=H.spearman(d.IS_rate_phi.values, d.OOS_rate_phi.values),
                           n_both=int((np.isfinite(d.IS_rate_phi) & np.isfinite(d.OOS_rate_phi)).sum()),
                           spy_OOS_Sharpe=metrics(spy_oos)["Sharpe"],
                           spy_OOS_CAGR=metrics(spy_oos)["CAGR"],
                           v2_OOS_Sharpe=metrics(ctx["v2"][c].loc[OOS_START:])["Sharpe"],
                           v2_OOS_CAGR=metrics(ctx["v2"][c].loc[OOS_START:])["CAGR"],
                           v1_OOS_Sharpe=metrics(ctx["v1"][c].loc[OOS_START:])["Sharpe"])
                ctl = rets[(book, "control", c)].loc[OOS_START:]
                mc = metrics(ctl)
                rec.update(ctl_OOS_CAGR=mc["CAGR"], ctl_OOS_Sharpe=mc["Sharpe"],
                           ctl_OOS_MaxDD=mc["MaxDD"])
                for tag, e in (("S1", e1), ("S2", e2)):
                    if len(e) == 0:
                        rec.update({f"{tag}_pick": None, f"{tag}_OOS_CAGR": np.nan,
                                    f"{tag}_OOS_Sharpe": np.nan, f"{tag}_OOS_MaxDD": np.nan,
                                    f"{tag}_IS_rate": np.nan, f"{tag}_OOS_rate": np.nan,
                                    f"{tag}_IS_dMaxDD": np.nan})
                        continue
                    p = e.loc[e.IS_rate_phi.idxmin()]
                    r = rets[(book, p.arm, c)].loc[OOS_START:]
                    m = metrics(r)
                    rec.update({f"{tag}_pick": p.arm, f"{tag}_OOS_CAGR": m["CAGR"],
                                f"{tag}_OOS_Sharpe": m["Sharpe"], f"{tag}_OOS_MaxDD": m["MaxDD"],
                                f"{tag}_IS_rate": p.IS_rate_phi, f"{tag}_OOS_rate": p.OOS_rate_phi,
                                f"{tag}_IS_dMaxDD": p.dMaxDD_IS})
                rec["same_pick"] = bool(rec["S1_pick"] == rec["S2_pick"])
                rec["dOOS_S2_minus_S1"] = rec["S2_OOS_Sharpe"] - rec["S1_OOS_Sharpe"]
                out.append(rec)
    return pd.DataFrame(out)


# ================================================================= main
def main():
    t0 = time.time()
    print("=" * 210)
    print("QUEUE idea 379 — is-the-priceability-floor-the-real-selector  (lane B, 2026-09-07)")
    print(f"Floor sweep phi = {FLOORS} pp of MaxDD; incumbent phi = {PHI0} (idea 94).")
    print(f"Grid held FIXED: {len(BOOKS)} books x {len(ARMS)} arms x {len(PUB_COSTS)} published "
          f"rungs x {len(UNIS)} panels = {len(BOOKS)*len(ARMS)*len(PUB_COSTS)*len(UNIS)} rows.")
    print("Only `published` moves with phi; `admissible` (D1&D2&D3) is floor-independent.")
    print(f"D3 inherited from idea 124's committed d3.csv at q={Q_STAR}, tau={TAU_STAR}; "
          f"floor bar for n* = {BAR:.0%}.")
    print("=" * 210)

    G, RET, CTX = build()
    D3 = pd.read_csv(f"{PARENT}.d3.csv")

    print("\n" + "-" * 210)
    print("REPRODUCTION GATES")
    g1, _ = gates(G)
    A10, C10 = curve(G, D3, PHI0, "full")
    g2, g3, g3b = gate_floorcurve(C10)

    # ---------------------------------------------------------------- A. the row census
    print("\n" + "=" * 210)
    print("A. HOW MANY ROWS THE FLOOR ADMITS — published rows per (panel, book) at each phi")
    print("   (32 rows per book = 16 arms x 2 published cost rungs; `admissible` is constant)")
    CUR = {}
    census = []
    for phi in FLOORS:
        A, C = curve(G, D3, phi, "full")
        CUR[phi] = (A, C)
        for _, r in C.iterrows():
            census.append(dict(phi=phi, uni=r.uni, book=r.book, n=r.n, ladder=r.ladder,
                               rows=r.rows, pub=r.pub, adm_all=r.adm_all, adm_pub=r.adm_pub))
    CEN = pd.DataFrame(census)
    for uname, _ in UNIS:
        d = CEN[CEN.uni == uname]
        piv = d.pivot_table(index="phi", columns="book", values="pub").reindex(FLOORS)
        piv = piv[[b for b in BOOKS if b in piv.columns]]
        print(f"\n  [{uname}] published rows by floor:")
        print(piv.to_string(float_format=lambda x: f"{x:.0f}"))
    tot = CEN.groupby("phi").pub.sum()
    print(f"\n  total published rows over both panels: "
          + "  ".join(f"phi={p:.2f}: {int(tot[p])}/448" for p in FLOORS))

    # ---------------------------------------------------------------- B. the rankings
    print("\n" + "=" * 210)
    print("B. THE RANKINGS UNDER THE SWEEP  (bar: identical entry set AND identical ordering "
          "at all five floors)")
    RANKS = []

    def add(name, scope, per_phi_vals, ascending):
        """per_phi_vals: {phi: {key: value}}; ordering ascending or descending."""
        keys = sorted({k for v in per_phi_vals.values() for k in v})
        ords = {p: ordering([per_phi_vals[p].get(k, np.nan) for k in keys], keys, ascending)
                for p in FLOORS}
        for p in FLOORS:
            RANKS.append(rank_report(name, scope, p, ords[PHI0], ords[p],
                                     per_phi_vals[PHI0], per_phi_vals[p], keys))
        return ords

    for uname, _ in UNIS:
        short = "u56" if uname.startswith("universe.json") else "broad"
        # K0 control + K1
        for col, nm, asc in (("adm_all", "K0 adm_all (control)", False),
                             ("adm_pub", "K1 adm_pub (idea 124 floor curve)", False)):
            vals = {}
            for p in FLOORS:
                d = CUR[p][1]
                d = d[d.uni == uname]
                vals[p] = {r.book: r[col] for _, r in d.iterrows()}
            add(nm, short, vals, asc)
        # K3 book price ordering, per rung
        for c in PUB_COSTS:
            vals = {}
            for p in FLOORS:
                bp = book_price(G, p, c)
                bp = bp[bp.uni == uname]
                vals[p] = {r.book: r.rate_phi for _, r in bp.iterrows()}
            add(f"K3 median rate by book @{c:.0f}bps", short, vals, True)

    # K4 arm menus (pooled over panels, as idea 94 published them)
    for label, books in (("idea94 3 books", I94_BOOKS), ("7-book ladder", BOOKS)):
        for c in PUB_COSTS:
            vals = {}
            for p in FLOORS:
                am = arm_menu(G, p, c, books)
                vals[p] = {r.arm: r.rate_phi for _, r in am.iterrows()}
            add(f"K4 arm menu ({label}) @{c:.0f}bps", "pooled", vals, True)

    RK = pd.DataFrame(RANKS)
    print(fmt(RK[["ranking", "scope", "phi", "n_entries", "dropped", "added", "identical",
                  "inversions", "spearman", "argmin", "argmax"]]))

    print("\n  INVARIANCE VERDICT per ranking (identical entry set AND ordering at all 5 floors):")
    ver = []
    for (nm, sc), d in RK.groupby(["ranking", "scope"], sort=False):
        inv = bool(d.identical.all() and (d.dropped == 0).all() and (d.added == 0).all())
        ver.append(dict(ranking=nm, scope=sc, INVARIANT=inv,
                        min_spearman=float(np.nanmin(d.spearman.values)),
                        max_inversions=int(d.inversions.max()),
                        max_dropped=int(d.dropped.max()),
                        argmin_stable=bool(d.argmin.nunique() == 1),
                        argmax_stable=bool(d.argmax.nunique() == 1)))
    VER = pd.DataFrame(ver)
    print(fmt(VER))
    print(f"\n  ANSWER to the queue's question: {int(VER.INVARIANT.sum())} of {len(VER)} "
          f"book-level rankings are invariant to the floor; "
          f"{int(VER.argmin_stable.sum())} of {len(VER)} keep the same argmin.")

    # K2 n*
    print("\n  K2 — idea 124's floor number n* (smallest ladder rung with adm_pub >= "
          f"{BAR:.0%}) at each floor:")
    ns_rows = []
    for p in FLOORS:
        rec = dict(phi=p)
        for uname, _ in UNIS:
            short = "u56" if uname.startswith("universe.json") else "broad"
            rec[f"n*_pub[{short}]"] = n_star(CUR[p][1], uname, "adm_pub")
            rec[f"n*_all[{short}]"] = n_star(CUR[p][1], uname, "adm_all")
        ns_rows.append(rec)
    NS = pd.DataFrame(ns_rows)
    print(NS.to_string(index=False))
    k2_inv = {c: NS[c].nunique(dropna=False) == 1 for c in NS.columns if c != "phi"}
    print(f"  K2 invariant: {k2_inv}")

    # ---------------------------------------------------------------- C. adm_pub detail
    print("\n" + "=" * 210)
    print("C. THE FLOOR CURVE adm_pub AT EVERY FLOOR (the number idea 124 published, re-read)")
    for uname, _ in UNIS:
        piv = CEN[CEN.uni == uname].pivot_table(index="phi", columns="book", values="adm_pub")
        piv = piv.reindex(FLOORS)[[b for b in BOOKS if b in piv.columns]]
        print(f"\n  [{uname}]")
        print(piv.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- D. W1
    print("\n" + "=" * 210)
    print("D. RULE 8 / W1 — the floor curve chosen on 2009-2016 only, then read on 2017-2026")
    w1 = []
    for p in FLOORS:
        _, C_is = curve(G, D3, p, "IS")
        _, C_oos = curve(G, D3, p, "OOS")
        for uname, _ in UNIS:
            short = "u56" if uname.startswith("universe.json") else "broad"
            w1.append(dict(phi=p, uni=short,
                           pub_IS=int(C_is[C_is.uni == uname].pub.sum()),
                           pub_OOS=int(C_oos[C_oos.uni == uname].pub.sum()),
                           n_star_IS=n_star(C_is, uname, "adm_pub"),
                           n_star_OOS=n_star(C_oos, uname, "adm_pub"),
                           n_star_full=n_star(CUR[p][1], uname, "adm_pub"),
                           adm_pub_IS_mean=float(np.nanmean(C_is[C_is.uni == uname].adm_pub)),
                           adm_pub_OOS_mean=float(np.nanmean(C_oos[C_oos.uni == uname].adm_pub))))
    W1 = pd.DataFrame(w1)
    print(fmt(W1))

    # ---------------------------------------------------------------- E. W2
    print("\n" + "=" * 210)
    print("E. RULE 8 / W2 — THE FLOOR AS A SELECTOR")
    print("   S1 = idea 94's selector (IS reach >= 1.0pp, lowest IS rate) — floor sits below it")
    print("   S2 = floor-only selector (published at phi on IS, lowest IS rate)")
    SEL = pd.concat([selector_table(G, RET, CTX, p) for p in FLOORS], ignore_index=True)
    summ = SEL.groupby("phi").agg(
        cells=("book", "size"),
        S1_picks=("S1_pick", lambda s: int(s.notna().sum())),
        S2_picks=("S2_pick", lambda s: int(s.notna().sum())),
        same_pick=("same_pick", "sum"),
        S1_OOS_Sharpe=("S1_OOS_Sharpe", "mean"),
        S2_OOS_Sharpe=("S2_OOS_Sharpe", "mean"),
        S1_OOS_CAGR=("S1_OOS_CAGR", "mean"),
        S2_OOS_CAGR=("S2_OOS_CAGR", "mean"),
        S1_OOS_MaxDD=("S1_OOS_MaxDD", "mean"),
        S2_OOS_MaxDD=("S2_OOS_MaxDD", "mean"),
        ctl_OOS_Sharpe=("ctl_OOS_Sharpe", "mean"),
        ctl_OOS_CAGR=("ctl_OOS_CAGR", "mean"),
        spearman_IS_OOS=("spearman_IS_OOS", "mean"),
        n_elig_S2=("n_elig_S2", "mean"),
    ).reset_index()
    summ["dOOS_S2_minus_S1"] = summ.S2_OOS_Sharpe - summ.S1_OOS_Sharpe
    summ["dOOS_S2_minus_ctl"] = summ.S2_OOS_Sharpe - summ.ctl_OOS_Sharpe
    print(fmt(summ))
    ref = SEL[SEL.phi == PHI0].set_index(["uni", "book", "cost"]).S2_pick
    chg = []
    for p in FLOORS:
        d = SEL[SEL.phi == p].set_index(["uni", "book", "cost"]).S2_pick
        chg.append(dict(phi=p, S2_picks_changed_vs_incumbent=int((d != ref).sum()),
                        of_cells=len(d)))
    print("\n  How many of the 28 cells' S2 picks the floor moves, against the phi=0.10 incumbent:")
    print(fmt(pd.DataFrame(chg)))
    b = SEL.groupby("phi").apply(
        lambda d: pd.Series(dict(
            S1_beats_ctl=int((d.S1_OOS_Sharpe > d.ctl_OOS_Sharpe).sum()),
            S2_beats_ctl=int((d.S2_OOS_Sharpe > d.ctl_OOS_Sharpe).sum()),
            S2_beats_SPY=int((d.S2_OOS_Sharpe > d.spy_OOS_Sharpe).sum()),
            S2_beats_v2=int((d.S2_OOS_Sharpe > d.v2_OOS_Sharpe).sum()),
            cells=len(d))), include_groups=False).reset_index()
    print("\n  OOS Sharpe head-to-heads (count of 28 cells):")
    print(fmt(b))

    # ---------------------------------------------------------------- F. KEEP paths
    print("\n" + "=" * 210)
    print("F. KEEP PATHS (PROTOCOL rule 4) over all arm-points, and what the floor hides")
    g10 = G.copy()
    print(f"  4a vs LIVE RULES v2: {int(g10.p4a_v2.sum())}/{len(g10)} arm-points   "
          f"4a vs RULES v1: {int(g10.p4a_v1.sum())}/{len(g10)}   "
          f"4b: {int(g10.p4b.sum())}/{len(g10)}")
    kp = []
    for p in FLOORS:
        pubmask = g10.dMaxDD > p
        kp.append(dict(phi=p, p4b_total=int(g10.p4b.sum()),
                       p4b_published=int((g10.p4b & pubmask).sum()),
                       p4b_hidden=int((g10.p4b & ~pubmask).sum()),
                       p4a_v2_published=int((g10.p4a_v2 & pubmask).sum()),
                       p4a_v2_hidden=int((g10.p4a_v2 & ~pubmask).sum())))
    KP = pd.DataFrame(kp)
    print("\n  4b/4a passes the publication rule would NOT print, by floor:")
    print(fmt(KP))
    if g10.p4b.any():
        best = g10[g10.p4b].sort_values("OOS_Sharpe", ascending=False).head(6)
        print("\n  best 4b-passing arm-points by OOS Sharpe (informational, none promoted):")
        print(fmt(best[["uni", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                        "OOS_Sharpe", "dMaxDD", "TO"]]))

    # ---------------------------------------------------------------- G2. who moves
    print("\n" + "=" * 210)
    print("H. WHICH ENTRIES THE FLOOR MOVES — max |rank(phi) - rank(0.10)| per entry")
    mv = []
    for (nm, sc), d in RK.groupby(["ranking", "scope"], sort=False):
        pos = {}
        for _, r in d.iterrows():
            for i, k in enumerate(r.order.split("|")):
                pos.setdefault(k, {})[r.phi] = i
        for k, v in pos.items():
            base = v.get(PHI0, np.nan)
            dmax = max(abs(v[p] - base) for p in v) if np.isfinite(base) else np.nan
            mv.append(dict(ranking=nm, scope=sc, entry=k, rank_at_incumbent=base,
                           max_rank_move=dmax,
                           rank_lo=min(v.values()), rank_hi=max(v.values())))
    MV = pd.DataFrame(mv)
    top = MV[MV.max_rank_move > 0].sort_values("max_rank_move", ascending=False)
    print(f"  {len(top)} of {len(MV)} entry-slots move at all; the largest moves:")
    print(fmt(top.head(20)))
    MV.to_csv(f"{OUT}.moves.csv", index=False)

    # ---------------------------------------------------------------- G. predictions
    print("\n" + "=" * 210)
    print("G. PRE-REGISTERED PREDICTIONS")
    k0 = VER[VER.ranking.str.startswith("K0")]
    k1 = VER[VER.ranking.str.startswith("K1")]
    k4 = VER[VER.ranking.str.startswith("K4")]
    print(f"  P1 K0 (control) invariant on both panels -> "
          f"{'CONFIRMED' if bool(k0.INVARIANT.all()) else 'REFUTED'} "
          f"({int(k0.INVARIANT.sum())}/{len(k0)})")
    print(f"  P2 K1 NOT invariant on either panel -> "
          f"{'CONFIRMED' if not bool(k1.INVARIANT.any()) else 'REFUTED'} "
          f"({int(k1.INVARIANT.sum())}/{len(k1)} invariant)")
    print(f"  P3 K4 (arm menu) IS invariant -> "
          f"{'CONFIRMED' if bool(k4.INVARIANT.all()) else 'REFUTED'} "
          f"({int(k4.INVARIANT.sum())}/{len(k4)} invariant, "
          f"min spearman {float(np.nanmin(k4.min_spearman.values)):.4f})")
    p4 = any(not v for v in k2_inv.values())
    print(f"  P4 n* not invariant on at least one panel -> "
          f"{'CONFIRMED' if p4 else 'REFUTED'}  ({k2_inv})")

    # ---------------------------------------------------------------- write
    G.to_csv(f"{OUT}.grid.csv", index=False)
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    RK.to_csv(f"{OUT}.rankings.csv", index=False)
    VER.to_csv(f"{OUT}.invariance.csv", index=False)
    NS.to_csv(f"{OUT}.nstar.csv", index=False)
    W1.to_csv(f"{OUT}.walkforward_floor.csv", index=False)
    SEL.to_csv(f"{OUT}.walkforward.csv", index=False)
    summ.to_csv(f"{OUT}.selector_summary.csv", index=False)
    KP.to_csv(f"{OUT}.keeppaths.csv", index=False)
    print(f"\nWrote {STEM}.{{grid,census,rankings,invariance,nstar,moves,walkforward_floor,"
          f"walkforward,selector_summary,keeppaths}}.csv   total {time.time()-t0:.0f}s")
    print(f"[gate] G1 {g1:.3e}   G2 {g2:.3e}   G3 {g3:.3e} / {g3b:.3e}")


if __name__ == "__main__":
    main()
