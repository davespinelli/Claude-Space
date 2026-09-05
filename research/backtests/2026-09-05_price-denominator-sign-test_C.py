#!/usr/bin/env python3
"""QUEUE idea 122 — price-denominators-need-a-sign-test (lane C, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 119 showed idea 97's price denominator (dMaxDD) flips sign between 0 and 10 bps and is
a coin flip across name draws (49/80), so the whole price list is a ratio with an
unmeasurable denominator.  Propose a PROTOCOL rule that no ratio is quoted unless its
denominator's sign survives a stated perturbation, and re-check idea 94's u56/broad price
list under it.  Bears on ideas 22, 74, 94, 97, 117."

What is being audited.  Every drawdown "price" this project has published has the form

    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)   pp CAGR per pp MaxDD

The denominator dMaxDD is a difference of two MAXIMA — a single-day statistic on each leg.
Idea 94 guarded it with an ABSOLUTE floor (quote the rate only if dMaxDD > 0.10 pp).  Idea
119 showed on the small panel that this floor is not a guard at all: the same denominator
changes SIGN between cost rungs and across name draws, so the ratio is a number divided by
something whose sign is not measurable.  This run asks the same question of idea 94's
LARGE-CAP price list (universe.json 56 names and universe_broad.json 136), which is the list
ideas 22/74/94/97/117 actually quote, and turns the answer into a proposed PROTOCOL clause.

THE SIGN TEST (pre-registered before any number below was read)
    A published rate is ADMISSIBLE only if its denominator's sign survives all three
    perturbations, each of which is a NUISANCE dimension the price claim does not depend on:
      D1 cost      dMaxDD > 0 at every cost rung in {0, 5, 10, 25} bps
      D2 window    dMaxDD > 0 in BOTH 2009-2016 and 2017-2026
      D3 panel     dMaxDD > 0 in at least a fraction tau of NDRAW name-subsample draws that
                   delete a fraction q of the panel at random (signals recomputed on the
                   sub-panel, so the book is genuinely re-formed)
    A row that fails any of the three is NOT PRICEABLE: the correct report is the pair
    (dCAGR, dMaxDD) with its instability, never the ratio.

Tuned parameters (PROTOCOL rule 4).  TWO, both of the TEST and neither of any trading rule:
    q    drop fraction in {0.05, 0.10, 0.20}
    tau  sign-agreement threshold in {0.80, 0.90, 0.95, 1.00}
All 12 grid points reported.  q = 0.10, tau = 0.90 is the pre-registered headline (it is
idea 119's own setting, adopted unchanged so that this run cannot pick its own bar).
Everything else — books, arms, universes, cost rungs, the IS/OOS split — is inherited
verbatim from idea 94 and idea 119.

Books / arms / universes: imported from idea 94's script and asserted to reproduce its
published pricelist.csv exactly, so this is an audit of that file and not a re-derivation.
    books   V1u (v1's composite, ungated, top-5 @15%), TOP20 (idea 2's ranking, ungated),
            EWall (equal-weight every name @75% gross)
    arms    5 gates x {de-gross, reweight}, 2 trailing stops, 2 book DD controls,
            2 entry-only turnover budgets  (17 treated arms)
    unis    universe.json(56), universe_broad.json(136)
    costs   published at 10 and 25 bps  ->  192 published rows, of which the finite `rate`
            cells are the ones this run audits.

Walk-forward (PROTOCOL rule 8), fixed before any OOS number was read
    S1  idea 94's own selector, unchanged: in each (universe, book, cost) cell, among arms
        that bought >= 1.0 pp of IS MaxDD, pick the LOWEST IS rate; evaluate untouched on
        2017-2026.
    S2  the same selector restricted to arms whose denominator passes the sign test computed
        on 2009-2016 DATA ONLY (IS cost axis, IS-window bootstrap draws).  The OOS window is
        never consulted by the screen.
    Reported for both: OOS CAGR / Sharpe / MaxDD vs the cell's own control, vs live RULES v1
    and vs SPY, and the OOS sign-agreement of the screen (does an IS-admissible denominator
    stay positive out of sample, and does an inadmissible one not?).

Pre-registered predictions (written before any number was read)
    P1  FEWER THAN HALF of idea 94's published rates are admissible at (q=0.10, tau=0.90).
    P2  The `-rw` gate arms fail far more often than the `-dg` arms: idea 94's own P3 found
        they buy almost no drawdown, so their denominator sits on zero and has no stable sign.
    P3  The COST axis (D1) kills more rows than the panel axis (D3) on these large-cap lists,
        because the panels are big enough for the book to survive a 10% deletion.
    P4  The sign screen does not manufacture a KEEP: no S2 pick passes 4b, and the screen's
        OOS Sharpe is within noise of S1's.  This is a measurement run.

Execution realism (PROTOCOL rule 2): inherited from idea 94 — weekly decision at close t
applied at t+1, long-only, no leverage, costs charged inside the loop so both state machines
see NET equity.  10 bps is the PROTOCOL point.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists.  Every
absolute level below is optimistic.  This run reports only within-cell differences and the
STABILITY of a sign, both of which are far less exposed than levels — but a survivorship-free
panel could still move which rows pass.

Deterministic (seeded), standalone.  Imports research/baseline.py and idea 94's script;
modifies nothing.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location(
    "i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)

STEM = Path(__file__).stem
OUT = BT / STEM
PCOST = 10.0
COST_RUNGS = [0.0, 5.0, 10.0, 25.0]          # D1
PUB_COSTS = [10.0, 25.0]                      # the rungs idea 94 published
IS_END, OOS_START = H.IS_END, H.OOS_START
BOOKS = list(H.BOOKS)
ARMS = [(n, k, kw, sp) for (n, k, kw, sp) in H.arm_specs() if n != "control"]
UNIS = [("universe.json(56)", dict()), ("universe_broad.json", dict(broad=True))]
NDRAW, DROP_FRACS, TAUS, SEED = 40, (0.05, 0.10, 0.20), (0.80, 0.90, 0.95, 1.00), 20260905
Q_STAR, TAU_STAR = 0.10, 0.90                 # pre-registered headline point (idea 119's)
FLOOR = 0.10                                  # idea 94's absolute floor, kept for continuity

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)


def fmt(df):
    return df.to_string(index=False, float_format=lambda x: f"{x:.4f}")


# ---------------------------------------------------------------- cached signal path
def signals(px):
    """The three panel-level signal blocks every arm needs, computed once per panel."""
    return dict(comp=H.composite(px), v20=H.vol20(px), ma=px.rolling(200).mean())


def gmask_c(px, gate, S):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma, v = S["ma"], S["v20"]
    if gate == "g200":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * 1.03, 1.0)
        raw = raw.mask(px < ma * 0.97, 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "abs12":
        return (px > px.shift(252)).fillna(False)
    if gate == "vol60":
        return (v < H.MAX_VOL).fillna(False)
    if gate == "v1gate":
        return ((px > ma) & (v < H.MAX_VOL)).fillna(False)
    raise ValueError(gate)


def targets_c(px, book, S, gate=None, conv="dg"):
    """H.targets with cached signals.  Asserted identical to H.targets on both full panels."""
    def base():
        if book == "EWall":
            e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
            return H.GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        s = S["comp"] / S["v20"].clip(lower=0.08) ** 0.5 if book == "V1u" else S["comp"]
        n, w = (H.NV1, H.WV1) if book == "V1u" else (H.NTOP, H.GROSS / H.NTOP)
        return (s.rank(axis=1, ascending=False) <= n).astype(float) * w

    if gate is None:
        return base()
    g = gmask_c(px, gate, S)
    if conv == "rw":
        if book == "EWall":
            e = g.astype(float)
            return H.GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        s = S["comp"] / S["v20"].clip(lower=0.08) ** 0.5 if book == "V1u" else S["comp"]
        n, w = (H.NV1, H.WV1) if book == "V1u" else (H.NTOP, H.GROSS / H.NTOP)
        return (s.where(g).rank(axis=1, ascending=False) <= n).astype(float) * w
    return base().where(g, 0.0)


# ---------------------------------------------------------------- price primitives
def dpair(rc, ra):
    """(dCAGR, dMaxDD) in pp, and idea 94's rate with its absolute floor."""
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd > FLOOR else np.nan)


def win(r, w):
    return r if w == "full" else (r.loc[:IS_END] if w == "IS" else r.loc[OOS_START:])


# ---------------------------------------------------------------- main grid (D1, D2)
def build_grid(uname, kw):
    px = H.load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    S = signals(px)

    # ---- reproduction guard: the cached path must equal idea 94's targets() exactly
    worst_t = 0.0
    for b in BOOKS:
        for g in [None] + H.GATES:
            for conv in (("dg",) if g is None else ("dg", "rw")):
                a = targets_c(px, b, S, g, conv).fillna(0.0)
                e = H.targets(px, b, g, conv).fillna(0.0)
                worst_t = max(worst_t, float((a - e).abs().to_numpy().max()))
    print(f"[check] cached targets vs idea 94 targets(): max|diff| = {worst_t:.3e} "
          f"({'EXACT' if worst_t < 1e-15 else 'NOT EXACT — unsafe'})")

    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
              for c in PUB_COSTS}
    rets = {}
    for b in BOOKS:
        for name, kind, kwargs, (g, conv) in H.arm_specs():
            W = targets_c(px, b, S, g, conv)
            for c in COST_RUNGS:
                rets[(b, name, c)] = H.run(px, W, bps=c, **kwargs)["r"].loc[start:]

    rows = []
    for b in BOOKS:
        for c in PUB_COSTS:
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in ARMS:
                ra = rets[(b, name, c)]
                dc, dd, rate = dpair(rc, ra)
                rec = dict(uni=uname, book=b, cost=c, arm=name, kind=kind,
                           dCAGR=dc, dMaxDD=dd, rate=rate,
                           published=bool(np.isfinite(rate)))
                for cc in COST_RUNGS:                              # D1 (full and IS-only)
                    _, dd_c, _ = dpair(rets[(b, "control", cc)], rets[(b, name, cc)])
                    rec[f"dMaxDD@{cc:.0f}"] = dd_c
                    _, dd_ci, _ = dpair(win(rets[(b, "control", cc)], "IS"),
                                        win(rets[(b, name, cc)], "IS"))
                    rec[f"dMaxDD_IS@{cc:.0f}"] = dd_ci
                for w in ("IS", "OOS"):                            # D2
                    dcw, ddw, rw_ = dpair(win(rc, w), win(ra, w))
                    rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dcw, ddw, rw_
                ma_, mc_ = metrics(ra), metrics(rc)
                mg = H.margins(ra, bars)
                rec.update(CAGR=ma_["CAGR"], Sharpe=ma_["Sharpe"], MaxDD=ma_["MaxDD"],
                           ctl_MaxDD=mc_["MaxDD"], ctl_CAGR=mc_["CAGR"],
                           p4a=H.pass4a(ra, v1_net[c]),
                           p4b=all(v > 0 for v in mg.values()),
                           f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-")
                rows.append(rec)
    G = pd.DataFrame(rows)
    G["D1_pass"] = np.all([G[f"dMaxDD@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    G["D2_pass"] = (G.dMaxDD_IS > 0) & (G.dMaxDD_OOS > 0)
    # IS-only cost axis: the walk-forward screen may never look at the OOS window, so D2 has
    # no IS-only form and the IS screen is D1(IS returns) AND D3(IS-window draws).
    G["D1_pass_IS_only"] = np.all([G[f"dMaxDD_IS@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    return px, start, S, spy, bars, v1_net, rets, G


# ---------------------------------------------------------------- D3 bootstrap
def bootstrap(uname, px, S_full, start):
    """Name-subsample draws.  Signals are recomputed on each sub-panel, so the book is
    genuinely re-formed; the draw is uniform over ALL panel columns (idea 119's convention)."""
    rng = np.random.default_rng(SEED)
    ncol = px.shape[1]
    out = []
    t0 = time.time()
    for q in DROP_FRACS:
        k = int(round(ncol * (1 - q)))
        for d in range(NDRAW):
            keep = sorted(rng.choice(ncol, size=k, replace=False))
            sub = px.iloc[:, keep]
            Ss = signals(sub)
            for b in BOOKS:
                rc = H.run(sub, targets_c(sub, b, Ss), bps=PCOST)["r"].loc[start:]
                for name, kind, kwargs, (g, conv) in ARMS:
                    ra = H.run(sub, targets_c(sub, b, Ss, g, conv), bps=PCOST,
                               **kwargs)["r"].loc[start:]
                    rec = dict(uni=uname, q=q, draw=d, book=b, arm=name)
                    for w in ("full", "IS", "OOS"):
                        dc, dd, rt = dpair(win(rc, w), win(ra, w))
                        rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dc, dd, rt
                    out.append(rec)
        print(f"    [{uname}] q={q:.2f}: {NDRAW} draws done ({time.time()-t0:.0f}s elapsed)",
              flush=True)
    return pd.DataFrame(out)


def d3_table(B):
    """Per (uni, q, book, arm): fraction of draws with dMaxDD > 0, full / IS / OOS."""
    g = B.groupby(["uni", "q", "book", "arm"])
    return pd.DataFrame(dict(
        frac_pos_full=g.dMaxDD_full.apply(lambda s: float((s > 0).mean())),
        frac_pos_IS=g.dMaxDD_IS.apply(lambda s: float((s > 0).mean())),
        frac_pos_OOS=g.dMaxDD_OOS.apply(lambda s: float((s > 0).mean())),
        frac_priceable=g.rate_full.apply(lambda s: float(s.notna().mean())),
        rate_q25=g.rate_full.quantile(0.25), rate_med=g.rate_full.median(),
        rate_q75=g.rate_full.quantile(0.75),
        dMaxDD_med=g.dMaxDD_full.median(), dCAGR_med=g.dCAGR_full.median(),
    )).reset_index()


# ---------------------------------------------------------------- walk-forward
def walk_forward(G, D3, rets_by_uni, v1_by_uni, spy_by_uni):
    """S1 = idea 94's selector.  S2 = the same selector after the IS-ONLY sign screen."""
    out = []
    for (uname, b, c), cell in G.groupby(["uni", "book", "cost"]):
        rets, v1_net, spy = rets_by_uni[uname], v1_by_uni[uname], spy_by_uni[uname]
        ctl_o = metrics(rets[(b, "control", c)].loc[OOS_START:])
        v1_o = metrics(v1_net[c].loc[OOS_START:])
        spy_o = metrics(spy.loc[OOS_START:])
        base = cell[(cell.dMaxDD_IS >= 1.0) & np.isfinite(cell.rate_IS)]
        for q in DROP_FRACS:
            for tau in TAUS:
                d3 = D3[(D3.uni == uname) & (D3.q == q) & (D3.book == b)] \
                    .set_index("arm").frac_pos_IS
                for sel, sub in (("S1", base),
                                 ("S2", base[base.arm.map(lambda a: d3.get(a, 0.0) >= tau)
                                             & base.D1_pass_IS_only])):
                    if sel == "S1" and (q, tau) != (DROP_FRACS[0], TAUS[0]):
                        continue                    # S1 does not depend on (q, tau)
                    rec = dict(uni=uname, book=b, cost=c, q=q, tau=tau, selector=sel,
                               ctl_OOS_CAGR=ctl_o["CAGR"], ctl_OOS_Sharpe=ctl_o["Sharpe"],
                               ctl_OOS_MaxDD=ctl_o["MaxDD"],
                               v1_OOS_CAGR=v1_o["CAGR"], v1_OOS_Sharpe=v1_o["Sharpe"],
                               spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_Sharpe=spy_o["Sharpe"],
                               spy_OOS_MaxDD=spy_o["MaxDD"], n_eligible=len(sub))
                    if sub.empty:
                        rec.update(pick="NOTHING ADMISSIBLE", IS_rate=np.nan, OOS_rate=np.nan,
                                   OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                   p4a=False, p4b=False)
                    else:
                        pk = sub.sort_values("rate_IS").iloc[0]
                        ro = rets[(b, pk.arm, c)].loc[OOS_START:]
                        mo = metrics(ro)
                        rec.update(pick=pk.arm, IS_rate=pk.rate_IS, OOS_rate=pk.rate_OOS,
                                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                   OOS_MaxDD=mo["MaxDD"], p4a=bool(pk.p4a), p4b=bool(pk.p4b))
                    out.append(rec)
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    print(__doc__.split("Deterministic")[0])
    print("=" * 210)
    print(f"PRE-REGISTERED: sign test D1 costs {COST_RUNGS} bps | D2 windows IS/OOS | "
          f"D3 {NDRAW} draws x q in {DROP_FRACS} (seed {SEED}), tau in {TAUS}; "
          f"headline (q,tau) = ({Q_STAR}, {TAU_STAR})")
    print("=" * 210)

    grids, boots, rets_by, v1_by, spy_by = [], [], {}, {}, {}
    for uname, kw in UNIS:
        print(f"\n### {uname}")
        px, start, S, spy, bars, v1_net, rets, G = build_grid(uname, kw)
        rets_by[uname], v1_by[uname], spy_by[uname] = rets, v1_net, spy
        ms = metrics(spy)
        print(f"    {px.shape[1]} names {px.index[0].date()}->{px.index[-1].date()} | eval from "
              f"{start.date()} | SPY {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} "
              f"halves {bars['s1']:.3f}/{bars['s2']:.3f} OOS {bars['soos']:.3f}")
        grids.append(G)
        print(f"    D3 bootstrap: {len(DROP_FRACS)} x {NDRAW} draws x {len(BOOKS)} books x "
              f"{len(ARMS)} arms ...", flush=True)
        boots.append(bootstrap(uname, px, S, start))
    G = pd.concat(grids, ignore_index=True)
    B = pd.concat(boots, ignore_index=True)
    D3 = d3_table(B)

    # ------------------------------------------------ A. reproduction of idea 94's pricelist
    print("\n" + "=" * 210)
    print("A. REPRODUCTION — this run's (dCAGR, dMaxDD, rate) vs idea 94's published pricelist.csv")
    P94 = pd.read_csv(BT / "2026-09-04_drawdown-insurance-price-list_B.pricelist.csv")
    m = G.merge(P94[["uni", "book", "cost", "arm", "dCAGR", "dMaxDD", "rate"]],
                on=["uni", "book", "cost", "arm"], suffixes=("", "_94"))
    rep = {c: float(np.nanmax(np.abs(m[c] - m[f"{c}_94"]))) for c in ("dCAGR", "dMaxDD", "rate")}
    nan_agree = int((m.rate.isna() == m.rate_94.isna()).sum())
    print(f"    matched rows {len(m)} of {len(P94)} published | max|diff| " +
          "  ".join(f"{k} {v:.2e}" for k, v in rep.items()) +
          f" | NaN-pattern agreement {nan_agree}/{len(m)} "
          f"({'EXACT' if max(rep.values()) < 1e-9 and nan_agree == len(m) else 'MISMATCH — unsafe'})")
    pd.DataFrame([dict(metric=k, max_abs_diff=v) for k, v in rep.items()] +
                 [dict(metric="nan_pattern_agree", max_abs_diff=nan_agree - len(m))]) \
        .to_csv(f"{OUT}.reproduction.csv", index=False)

    # ------------------------------------------------ B. the three axes, row by row
    d3s = D3[(D3.q == Q_STAR)].set_index(["uni", "book", "arm"])
    G["D3_frac_full"] = [d3s.frac_pos_full.get((u, b, a), np.nan)
                         for u, b, a in zip(G.uni, G.book, G.arm)]
    G["D3_frac_IS"] = [d3s.frac_pos_IS.get((u, b, a), np.nan)
                       for u, b, a in zip(G.uni, G.book, G.arm)]
    G["D3_frac_OOS"] = [d3s.frac_pos_OOS.get((u, b, a), np.nan)
                        for u, b, a in zip(G.uni, G.book, G.arm)]
    G["D3_pass"] = G.D3_frac_full >= TAU_STAR
    G["ADMISSIBLE"] = G.D1_pass & G.D2_pass & G.D3_pass

    pub = G[G.published].copy()
    print("\n" + "=" * 210)
    print(f"B. THE PRICE LIST UNDER THE SIGN TEST — {len(G)} rows, {len(pub)} carry a PUBLISHED "
          f"rate (idea 94's dMaxDD > {FLOOR} pp floor).  Headline (q,tau)=({Q_STAR},{TAU_STAR}).")
    print(fmt(G[["uni", "book", "cost", "arm", "dCAGR", "dMaxDD", "rate", "published",
                 "dMaxDD@0", "dMaxDD@5", "dMaxDD@10", "dMaxDD@25", "D1_pass",
                 "dMaxDD_IS", "dMaxDD_OOS", "D2_pass", "D3_frac_full", "D3_pass",
                 "ADMISSIBLE", "p4a", "p4b"]]))

    print("\n--- SURVIVAL of the PUBLISHED rates (the rows ideas 22/74/94/97/117 quote) ---")
    surv = pd.DataFrame([dict(
        axis=nm, n_pub=len(pub), n_pass=int(pub[col].sum()),
        frac=float(pub[col].mean()))
        for nm, col in (("D1 cost {0,5,10,25} bps", "D1_pass"),
                        ("D2 window IS and OOS", "D2_pass"),
                        (f"D3 panel q={Q_STAR} tau={TAU_STAR}", "D3_pass"),
                        ("ALL THREE (admissible)", "ADMISSIBLE"))])
    print(fmt(surv))
    print("\n--- by universe / book / arm family ---")
    for key in ("uni", "book", "kind"):
        t = pub.groupby(key).agg(n_pub=("rate", "size"), D1=("D1_pass", "sum"),
                                 D2=("D2_pass", "sum"), D3=("D3_pass", "sum"),
                                 admissible=("ADMISSIBLE", "sum")).reset_index()
        print(fmt(t))
    pub["conv"] = np.where(pub.arm.str.endswith("-rw"), "rw",
                           np.where(pub.arm.str.endswith("-dg"), "dg", "n/a"))
    print(fmt(pub.groupby("conv").agg(n_pub=("rate", "size"), D1=("D1_pass", "sum"),
                                      D2=("D2_pass", "sum"), D3=("D3_pass", "sum"),
                                      admissible=("ADMISSIBLE", "sum"),
                                      med_dMaxDD=("dMaxDD", "median")).reset_index()))
    print("\n--- the admissible rows, in full (this is the price list that survives) ---")
    A = pub[pub.ADMISSIBLE]
    print(fmt(A[["uni", "book", "cost", "arm", "dCAGR", "dMaxDD", "rate", "D3_frac_full",
                 "rate_IS", "rate_OOS", "p4a", "p4b"]]) if len(A) else "    (none)")

    # ------------------------------------------------ C. the (q, tau) grid, all 12 points
    print("\n" + "=" * 210)
    print("C. ALL 12 GRID POINTS — how many of the 192 rows / of the published rates are "
          "admissible at each (q, tau).  No point was chosen after the fact.")
    gp = []
    for q in DROP_FRACS:
        dd = D3[D3.q == q].set_index(["uni", "book", "arm"]).frac_pos_full
        f = np.array([dd.get((u, b, a), np.nan) for u, b, a in zip(G.uni, G.book, G.arm)])
        for tau in TAUS:
            ok = G.D1_pass & G.D2_pass & (f >= tau)
            gp.append(dict(q=q, tau=tau, n_rows=len(G), admissible_rows=int(ok.sum()),
                           n_published=int(G.published.sum()),
                           admissible_published=int((ok & G.published).sum()),
                           frac_published=float((ok & G.published).sum() / G.published.sum()),
                           u56=int((ok & G.published & (G.uni == UNIS[0][0])).sum()),
                           broad=int((ok & G.published & (G.uni == UNIS[1][0])).sum())))
    GP = pd.DataFrame(gp)
    print(fmt(GP))

    # ------------------------------------------------ D. walk-forward
    print("\n" + "=" * 210)
    print("D. RULE 8 WALK-FORWARD — the screen is computed on 2009-2016 ONLY (IS cost axis, "
          "IS-window draws); 2017-2026 is untouched.")
    print("    IS screen = D1 on IS returns (all four cost rungs) AND D3 on IS-window draws. "
          "D2 has no IS-only form and is not used by the screen.")
    Wf = walk_forward(G, D3, rets_by, v1_by, spy_by)
    print(fmt(Wf[["uni", "book", "cost", "selector", "q", "tau", "n_eligible", "pick",
                  "IS_rate", "OOS_rate", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                  "ctl_OOS_Sharpe", "v1_OOS_Sharpe", "spy_OOS_Sharpe", "p4a", "p4b"]]))
    s1 = Wf[Wf.selector == "S1"]
    print(f"\n    S1 (idea 94's selector, no screen): {len(s1)} cells, mean OOS Sharpe "
          f"{s1.OOS_Sharpe.mean():.3f}, picks {sorted(set(s1.pick))}")
    for q in DROP_FRACS:
        for tau in TAUS:
            s2 = Wf[(Wf.selector == "S2") & (Wf.q == q) & (Wf.tau == tau)]
            nn = int((s2.pick == "NOTHING ADMISSIBLE").sum())
            print(f"    S2 q={q:.2f} tau={tau:.2f}: mean OOS Sharpe "
                  f"{s2.OOS_Sharpe.mean():.3f} over {len(s2)-nn} cells with a pick, "
                  f"{nn} cells with NOTHING ADMISSIBLE, picks "
                  f"{sorted(set(s2[s2.pick != 'NOTHING ADMISSIBLE'].pick))}")

    print("\n--- does an IS-admissible denominator stay positive OUT OF SAMPLE? "
          "(the screen's only real claim) ---")
    ver = []
    for q in DROP_FRACS:
        dd_is = D3[D3.q == q].set_index(["uni", "book", "arm"]).frac_pos_IS
        f_is = np.array([dd_is.get((u, b, a), np.nan) for u, b, a in zip(G.uni, G.book, G.arm)])
        for tau in TAUS:
            scr = G.D1_pass_IS_only & (f_is >= tau)
            for lab, sel in (("IS-admissible", scr), ("IS-rejected", ~scr)):
                sub = G[sel & G.published]
                ver.append(dict(q=q, tau=tau, group=lab, n=len(sub),
                                frac_OOS_dMaxDD_pos=float((sub.dMaxDD_OOS > 0).mean())
                                if len(sub) else np.nan,
                                frac_OOS_priceable=float(np.isfinite(sub.rate_OOS).mean())
                                if len(sub) else np.nan,
                                median_OOS_rate=float(sub.rate_OOS.median()) if len(sub) else np.nan))
    V = pd.DataFrame(ver)
    print(fmt(V))

    # ------------------------------------------------ E. KEEP paths
    print("\n" + "=" * 210)
    print("E. PROTOCOL rule 4, BOTH KEEP PATHS — every arm-point in the audited grid @10/25 bps")
    k = G[G.cost.isin(PUB_COSTS)]
    print(f"    4a passes: {int(k.p4a.sum())} of {len(k)}   |   4b passes: {int(k.p4b.sum())} "
          f"of {len(k)}")
    if k.p4b.any():
        print(fmt(k[k.p4b][["uni", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD",
                            "ADMISSIBLE", "rate"]]))
    print(f"    of the ADMISSIBLE published rows: 4a {int(A.p4a.sum())}/{len(A)}, "
          f"4b {int(A.p4b.sum())}/{len(A)}")

    # ------------------------------------------------ F. scorecard
    print("\n" + "=" * 210)
    print("F. PREDICTION SCORECARD")
    fr = float(pub.ADMISSIBLE.mean())
    print(f"  P1 fewer than half of published rates admissible at ({Q_STAR},{TAU_STAR}): "
          f"{int(pub.ADMISSIBLE.sum())}/{len(pub)} = {fr:.1%} "
          f"({'CONFIRMED' if fr < 0.5 else 'REFUTED'})")
    rw = pub[pub.conv == "rw"]; dg = pub[pub.conv == "dg"]
    print(f"  P2 -rw fails more than -dg: admissible rw {int(rw.ADMISSIBLE.sum())}/{len(rw)} "
          f"vs dg {int(dg.ADMISSIBLE.sum())}/{len(dg)} "
          f"({'CONFIRMED' if rw.ADMISSIBLE.mean() < dg.ADMISSIBLE.mean() else 'REFUTED'})")
    n1, n3 = int((~pub.D1_pass).sum()), int((~pub.D3_pass).sum())
    print(f"  P3 cost axis kills more than panel axis: D1 failures {n1}, D3 failures {n3} "
          f"({'CONFIRMED' if n1 > n3 else 'REFUTED'})")
    s2any = Wf[(Wf.selector == "S2") & (Wf.pick != "NOTHING ADMISSIBLE")]
    print(f"  P4 no S2 pick passes 4b: {int(s2any.p4b.sum())} of {len(s2any)} picks pass 4b "
          f"({'CONFIRMED' if not s2any.p4b.any() else 'REFUTED'}); "
          f"mean OOS Sharpe S1 {s1.OOS_Sharpe.mean():.3f} vs S2@headline "
          f"{Wf[(Wf.selector=='S2')&(Wf.q==Q_STAR)&(Wf.tau==TAU_STAR)].OOS_Sharpe.mean():.3f}")

    G.to_csv(f"{OUT}.signtest.csv", index=False)
    B.to_csv(f"{OUT}.bootstrap.csv", index=False)
    D3.to_csv(f"{OUT}.d3.csv", index=False)
    GP.to_csv(f"{OUT}.grid.csv", index=False)
    Wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    V.to_csv(f"{OUT}.oossign.csv", index=False)
    surv.to_csv(f"{OUT}.survival.csv", index=False)
    print(f"\nWrote {STEM}.{{signtest,bootstrap,d3,grid,walkforward,oossign,survival,"
          f"reproduction}}.csv")


if __name__ == "__main__":
    main()
