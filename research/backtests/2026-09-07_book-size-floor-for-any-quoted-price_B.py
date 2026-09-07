#!/usr/bin/env python3
"""QUEUE idea 124 — book-size-floor-for-any-quoted-price (lane B, 2026-09-07).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 122 found that ALL 24 panel-axis and ALL 5 cost-axis sign failures in idea 94's price
list are the 5-name V1u book (16/41 admissible) while the 56-name EWall book is 47/48.
Derive the floor directly: price the same instruments on top-n books with n in
{3,5,10,20,40,all} and find the n at which the denominator's sign becomes stable.  The answer
is a number PROTOCOL can state instead of '~20 names'.  Max 2 params."

What is being measured
----------------------
Every quoted price in the record has the form

    rate = (CAGR_ctl - CAGR_arm) / (|MaxDD_ctl| - |MaxDD_arm|)      pp CAGR per pp MaxDD

and is meaningless the moment its DENOMINATOR dMaxDD can change sign under a nuisance
perturbation.  Idea 122 pre-registered the three-axis sign test and found the failures live
almost entirely in the 5-name book.  It could not say WHERE the floor is, because its book
axis had three points that differ in more than one way at once (V1u is 5 names AND vol-scaled
AND 15% flat weights; TOP20 is 20 names, plain composite; EWall is every name, no ranking).

This run replaces that confounded axis with a single-family LADDER: TOP-n, plain composite,
ungated, equal weight GROSS/n, n in {3, 5, 10, 20, 40, all}.  n=20 IS idea 94's TOP20 and
n=all IS its EWall, so the ladder nests two of its three books exactly (asserted below).
V1u is carried as a SEVENTH, OFF-LADDER book so that "5 names" (TOP5, same 15% weights, same
gross) can be separated from "5 names AND a vol scaler" (V1u).  That contrast is the direct
test of idea 122's attribution.

Tuned parameters (PROTOCOL rule 4): TWO, both inherited, neither chosen here.
    q    the panel-draw drop fraction, in {0.05, 0.10, 0.20}
    tau  the fraction of draws whose denominator must stay positive, in {0.80,0.90,0.95,1.00}
Headline (q, tau) = (0.10, 0.90), adopted UNCHANGED from ideas 119/122 so this run cannot
pick its own bar.  All 12 grid points are reported for every rung of the ladder.
n is the SUBJECT axis, not a tuned parameter: all 6 rungs (+V1u) are reported everywhere and
nothing is selected on a result.

The floor bar, pre-registered before any number was read: n* = the smallest rung of the
ladder at which >= 90% of that rung's published rates are admissible under all three axes.
The whole curve is printed so any other bar can be read off it.

Pre-registered predictions (written before any number was read)
    P1  The admissible share is MONOTONE non-decreasing in n on both panels.
    P2  The floor sits between 10 and 20 names, i.e. PROTOCOL's informal "~20 names" is
        conservative but roughly right.
    P3  TOP5 is MORE stable than V1u at the same name count and the same gross, i.e. idea
        122's failure address is the name COUNT, not the vol scaler.
    P4  The floor is an absolute NAME COUNT, not a share of the panel: the same n* is reached
        on u56 (56 names) and broad (136).  If P4 fails, PROTOCOL cannot state a number.

Rule 8 walk-forward (PROTOCOL rule 8), both legs fixed before any OOS number was read
    W1  The FLOOR itself: recompute the screen on 2009-2016 ONLY (D1 on IS returns, D3 on
        IS-window draws; D2 has no IS-only form, per idea 122) and read n*_IS.  Then read the
        2017-2026 curve untouched and report n*_OOS.  A floor that only exists in-sample is
        not a PROTOCOL number.
    W2  The PRICE LIST at each rung: in each (uni, n, cost) cell, S1 = idea 94's selector
        (among arms buying >= 1.0 pp of IS MaxDD, the LOWEST IS rate).  Evaluate that arm
        untouched on 2017-2026: OOS CAGR / Sharpe / MaxDD vs the cell control, vs the LIVE
        RULES v2 baseline, vs RULES v1 and vs SPY.  Plus spearman(IS rate, OOS rate) within
        each cell: a price list whose ORDERING re-shuffles out of sample is not a price list,
        whatever its denominator does.

Both KEEP paths (PROTOCOL rule 4) are evaluated for every arm-point at both published rungs.

Execution realism (PROTOCOL rule 2): idea 94's harness verbatim (weights at close t applied
at t+1, weekly, long-only, no leverage, costs charged inside the loop).  10 bps is the
PROTOCOL point; 0/5/25 bps are the sign-test rungs and 25 bps is published alongside 10.

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every
absolute CAGR here is optimistic.  The subject of this run is the SIGN of a difference
between two arms sharing a panel and the same days, which is far less exposed than a level.

Deterministic (seed below), standalone, modifies nothing.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location(
    "i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)

STEM = Path(__file__).stem
OUT = BT / STEM
PCOST = 10.0
COST_RUNGS = [0.0, 5.0, 10.0, 25.0]           # D1 axis
PUB_COSTS = [10.0, 25.0]                      # the rungs idea 94 published
IS_END, OOS_START = H.IS_END, H.OOS_START
FLOOR = 0.10                                  # idea 94's absolute dMaxDD floor for a price
LADDER = [3, 5, 10, 20, 40, "all"]            # the SUBJECT axis
BOOKS = [f"TOP{n}" for n in LADDER[:-1]] + ["TOPall", "V1u"]   # V1u is OFF-ladder
ARMS = [(n, k, kw, sp) for (n, k, kw, sp) in H.arm_specs() if n != "control"]
UNIS = [("universe.json(56)", dict()), ("universe_broad.json", dict(broad=True))]
NDRAW, DROP_FRACS, TAUS, SEED = 40, (0.05, 0.10, 0.20), (0.80, 0.90, 0.95, 1.00), 20260907
Q_STAR, TAU_STAR = 0.10, 0.90                 # pre-registered headline (idea 119/122's)
BAR = 0.90                                    # pre-registered floor bar

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 4000)


def fmt(df):
    return df.to_string(index=False, float_format=lambda x: f"{x:.4f}")


def book_n(book):
    """Name count of a ladder rung; None for 'all' and for the off-ladder V1u (5)."""
    if book == "TOPall":
        return None
    if book == "V1u":
        return H.NV1
    return int(book[3:])


# ---------------------------------------------------------------- cached signal path
def signals(px):
    return dict(comp=H.composite(px), v20=H.vol20(px))


def targets_n(px, book, S, gate=None, conv="dg"):
    """The TOP-n ladder (plus the off-ladder V1u), with idea 94's two gate conventions.

    TOP{n} : plain composite, top-n, equal weight GROSS/n, ungated base.
    TOPall : every priced name at GROSS/N  (= idea 94's EWall, asserted).
    V1u    : composite / sqrt(vol20), top-5 at 15%  (= idea 94's V1u, asserted).
    """
    def score():
        return S["comp"] / S["v20"].clip(lower=0.08) ** 0.5 if book == "V1u" else S["comp"]

    def nw():
        if book == "V1u":
            return H.NV1, H.WV1
        n = book_n(book)
        return n, H.GROSS / n

    def base():
        if book == "TOPall":
            e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
            return H.GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        n, w = nw()
        return (score().rank(axis=1, ascending=False) <= n).astype(float) * w

    if gate is None:
        return base()
    g = H.gate_mask(px, gate)
    if conv == "rw":
        if book == "TOPall":
            e = g.astype(float)
            return H.GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        n, w = nw()
        return (score().where(g).rank(axis=1, ascending=False) <= n).astype(float) * w
    return base().where(g, 0.0)


# ---------------------------------------------------------------- price primitives
def dpair(rc, ra):
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd > FLOOR else np.nan)


def win(r, w):
    return r if w == "full" else (r.loc[:IS_END] if w == "IS" else r.loc[OOS_START:])


# ---------------------------------------------------------------- reproduction gates
def gates(uname, px, S, start):
    g = []

    # G1  the ladder NESTS idea 94's books exactly
    worst20 = worstall = worstv1 = 0.0
    for gate in [None] + H.GATES:
        for conv in (("dg",) if gate is None else ("dg", "rw")):
            worst20 = max(worst20, float((targets_n(px, "TOP20", S, gate, conv).fillna(0.0)
                                          - H.targets(px, "TOP20", gate, conv).fillna(0.0))
                                         .abs().to_numpy().max()))
            worstv1 = max(worstv1, float((targets_n(px, "V1u", S, gate, conv).fillna(0.0)
                                          - H.targets(px, "V1u", gate, conv).fillna(0.0))
                                         .abs().to_numpy().max()))
            a = targets_n(px, "TOPall", S, gate, conv).fillna(0.0).loc[start:]
            e = H.targets(px, "EWall", gate, conv).fillna(0.0).loc[start:]
            worstall = max(worstall, float((a - e).abs().to_numpy().max()))
    g += [("G1a TOP20 targets == idea 94 TOP20", worst20, 1e-15),
          ("G1b TOPall targets == idea 94 EWall (eval slice)", worstall, 1e-15),
          ("G1c V1u targets == idea 94 V1u", worstv1, 1e-15)]

    # G2  the harness with every instrument off IS engine.backtest
    worst = 0.0
    for b in BOOKS:
        W = targets_n(px, b, S)
        a = H.run(px, W, bps=PCOST)["r"].loc[start:]
        e = backtest(px, W, cost_bps=PCOST, freq=H.FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    g.append(("G2 control run() == engine.backtest", worst, 1e-12))
    return g


def gate_pricelist(uname, px, S, start):
    """G3: reproduce idea 94's COMMITTED pricelist rows for the two nested books."""
    pl = pd.read_csv(BT / "2026-09-04_drawdown-insurance-price-list_B.pricelist.csv")
    pl = pl[(pl.uni == uname) & (pl.book.isin(["TOP20", "EWall"]))]
    mine, ok = [], 0
    for b, mb in (("TOP20", "TOP20"), ("TOPall", "EWall")):
        for c in PUB_COSTS:
            rc = H.run(px, targets_n(px, b, S), bps=c)["r"].loc[start:]
            for name, kind, kwargs, (gt, conv) in ARMS:
                ra = H.run(px, targets_n(px, b, S, gt, conv), bps=c, **kwargs)["r"].loc[start:]
                dc, dd, rt = dpair(rc, ra)
                ref = pl[(pl.book == mb) & (pl.cost == c) & (pl.arm == name)]
                if len(ref) != 1:
                    continue
                r0 = ref.iloc[0]
                mine.append(dict(uni=uname, book=b, ref_book=mb, cost=c, arm=name,
                                 dCAGR=dc, dMaxDD=dd, rate=rt,
                                 ref_dCAGR=r0.dCAGR, ref_dMaxDD=r0.dMaxDD, ref_rate=r0.rate,
                                 e_dCAGR=abs(dc - r0.dCAGR), e_dMaxDD=abs(dd - r0.dMaxDD),
                                 e_rate=(abs(rt - r0.rate) if np.isfinite(rt) and np.isfinite(r0.rate)
                                         else (0.0 if (not np.isfinite(rt)) and (not np.isfinite(r0.rate)) else np.inf))))
                ok += 1
    R = pd.DataFrame(mine)
    return R, ok


# ---------------------------------------------------------------- main grid (D1, D2)
def build_grid(uname, kw):
    px = H.load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    S = signals(px)

    print("\n" + "=" * 210)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    ms = metrics(spy)
    print(f"SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f} OOS {bars['soos']:.3f}")
    print("=" * 210)

    for label, val, tol in gates(uname, px, S, start):
        print(f"[gate] {label:52s} max|diff| = {val:.3e}  "
              f"({'PASS' if val < tol else 'FAIL — results below are unsafe'})")

    v2 = backtest(px, rules_v2_weights(px), cost_bps=PCOST, freq=H.FREQ)["returns"].loc[start:]
    m2 = metrics(v2)
    print(f"[gate] LIVE RULES v2 @10bps on this panel: CAGR {m2['CAGR']:.2%} "
          f"Sharpe {m2['Sharpe']:.4f} MaxDD {m2['MaxDD']:.2%} "
          f"halves {H.halves(v2)[0]:.4f}/{H.halves(v2)[1]:.4f}"
          + ("   (u56 reference: 8.66% / 1.2056 / -12.05%, 1.2259/1.1908)"
             if uname.startswith("universe.json") else ""))

    v2_net = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
              for c in PUB_COSTS}
    v1_net = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
              for c in PUB_COSTS}

    rets, tinfo = {}, {}
    for b in BOOKS:
        for name, kind, kwargs, (gt, conv) in H.arm_specs():
            W = targets_n(px, b, S, gt, conv)
            tinfo[(b, name)] = dict(names=float((W.loc[start:] > 0).sum(axis=1).mean()),
                                    tgt_gross=float(W.loc[start:].sum(axis=1).mean()))
            for c in COST_RUNGS:
                res = H.run(px, W, bps=c, **kwargs)
                rets[(b, name, c)] = res["r"].loc[start:]
                if c == PCOST:
                    tinfo[(b, name)]["gross"] = float(res["gross"].loc[start:].mean())
                    tinfo[(b, name)]["TO"] = float(res["to"].loc[start:].sum()
                                                   / metrics(res["r"].loc[start:])["Years"])

    rows = []
    for b in BOOKS:
        for c in PUB_COSTS:
            rc = rets[(b, "control", c)]
            for name, kind, _, _ in ARMS:
                ra = rets[(b, name, c)]
                dc, dd, rate = dpair(rc, ra)
                rec = dict(uni=uname, npanel=px.shape[1], book=b, n=book_n(b) or px.shape[1],
                           ladder=(b != "V1u"), cost=c, arm=name, kind=kind,
                           dCAGR=dc, dMaxDD=dd, rate=rate, published=bool(np.isfinite(rate)))
                for cc in COST_RUNGS:
                    _, dd_c, _ = dpair(rets[(b, "control", cc)], rets[(b, name, cc)])
                    rec[f"dMaxDD@{cc:.0f}"] = dd_c
                    _, dd_ci, _ = dpair(win(rets[(b, "control", cc)], "IS"),
                                        win(rets[(b, name, cc)], "IS"))
                    rec[f"dMaxDD_IS@{cc:.0f}"] = dd_ci
                for w in ("IS", "OOS"):
                    dcw, ddw, rw_ = dpair(win(rc, w), win(ra, w))
                    rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dcw, ddw, rw_
                ma_, mc_ = metrics(ra), metrics(rc)
                mg = H.margins(ra, bars)
                rec.update(CAGR=ma_["CAGR"], Sharpe=ma_["Sharpe"], MaxDD=ma_["MaxDD"],
                           H1=H.halves(ra)[0], H2=H.halves(ra)[1],
                           OOS_CAGR=metrics(win(ra, "OOS"))["CAGR"],
                           OOS_Sharpe=metrics(win(ra, "OOS"))["Sharpe"],
                           OOS_MaxDD=metrics(win(ra, "OOS"))["MaxDD"],
                           ctl_CAGR=mc_["CAGR"], ctl_MaxDD=mc_["MaxDD"], ctl_Sharpe=mc_["Sharpe"],
                           names=tinfo[(b, name)]["names"], gross=tinfo[(b, name)]["gross"],
                           TO=tinfo[(b, name)]["TO"],
                           p4a_v2=H.pass4a(ra, v2_net[c]), p4a_v1=H.pass4a(ra, v1_net[c]),
                           p4b=all(v > 0 for v in mg.values()),
                           f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-",
                           **{f"m_{k}": v for k, v in mg.items()})
                rows.append(rec)
    G = pd.DataFrame(rows)
    G["D1_pass"] = np.all([G[f"dMaxDD@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    G["D2_pass"] = (G.dMaxDD_IS > 0) & (G.dMaxDD_OOS > 0)
    G["D1_pass_IS"] = np.all([G[f"dMaxDD_IS@{c:.0f}"] > 0 for c in COST_RUNGS], axis=0)
    return px, start, S, spy, bars, rets, G, v1_net, v2_net


# ---------------------------------------------------------------- D3 bootstrap
def bootstrap(uname, px, start):
    """Name-subsample draws.  Signals are recomputed on each sub-panel, so each book is
    genuinely re-formed at its own n (idea 119/122's convention: draw uniform over columns)."""
    rng = np.random.default_rng(SEED)
    ncol = px.shape[1]
    out, t0 = [], time.time()
    for q in DROP_FRACS:
        k = int(round(ncol * (1 - q)))
        for d in range(NDRAW):
            keep = sorted(rng.choice(ncol, size=k, replace=False))
            sub = px.iloc[:, keep]
            Ss = signals(sub)
            for b in BOOKS:
                rc = H.run(sub, targets_n(sub, b, Ss), bps=PCOST)["r"].loc[start:]
                for name, kind, kwargs, (gt, conv) in ARMS:
                    ra = H.run(sub, targets_n(sub, b, Ss, gt, conv), bps=PCOST,
                               **kwargs)["r"].loc[start:]
                    rec = dict(uni=uname, q=q, draw=d, nkeep=k, book=b, arm=name)
                    for w in ("full", "IS", "OOS"):
                        dc, dd, rt = dpair(win(rc, w), win(ra, w))
                        rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dc, dd, rt
                    out.append(rec)
        print(f"    [{uname}] q={q:.2f}: {NDRAW} draws x {len(BOOKS)} books done "
              f"({time.time()-t0:.0f}s elapsed)", flush=True)
    return pd.DataFrame(out)


def d3_table(B):
    g = B.groupby(["uni", "q", "book", "arm"])
    return pd.DataFrame(dict(
        frac_pos_full=g.dMaxDD_full.apply(lambda s: float((s > 0).mean())),
        frac_pos_IS=g.dMaxDD_IS.apply(lambda s: float((s > 0).mean())),
        frac_pos_OOS=g.dMaxDD_OOS.apply(lambda s: float((s > 0).mean())),
        frac_priceable=g.rate_full.apply(lambda s: float(s.notna().mean())),
        dMaxDD_med=g.dMaxDD_full.median(), dCAGR_med=g.dCAGR_full.median(),
        rate_med=g.rate_full.median(),
    )).reset_index()


# ---------------------------------------------------------------- the floor curve
def floor_curve(G, D3, q, tau, window="full"):
    """Admissible share by (uni, book).  window='full' uses D1+D2+D3(full);
    'IS' uses the IS-only screen (D1 on IS returns + D3 on IS draws — no D2, per idea 122);
    'OOS' uses D1 at the PROTOCOL rung on OOS returns + D3 on OOS draws."""
    d3 = D3[D3.q == q].set_index(["uni", "book", "arm"])
    col = {"full": "frac_pos_full", "IS": "frac_pos_IS", "OOS": "frac_pos_OOS"}[window]
    rows = []
    for _, r in G.iterrows():
        key = (r.uni, r.book, r.arm)
        f = float(d3.loc[key, col]) if key in d3.index else np.nan
        if window == "full":
            ok = bool(r.D1_pass and r.D2_pass and f >= tau)
            pub = bool(r.published)
        elif window == "IS":
            ok = bool(r.D1_pass_IS and f >= tau)
            pub = bool(np.isfinite(r.rate_IS))
        else:
            ok = bool(r.dMaxDD_OOS > 0 and f >= tau)
            pub = bool(np.isfinite(r.rate_OOS))
        rows.append(dict(uni=r.uni, book=r.book, n=r.n, ladder=r.ladder, cost=r.cost,
                         arm=r.arm, published=pub, admissible=ok, d3=f))
    A = pd.DataFrame(rows)
    g = A.groupby(["uni", "book", "n", "ladder"])
    C = pd.DataFrame(dict(
        rows=g.size(),
        adm_all=g.admissible.mean(),
        pub=g.published.sum(),
        adm_pub=g.apply(lambda d: float(d.admissible[d.published].mean())
                        if d.published.any() else np.nan, include_groups=False),
    )).reset_index().sort_values(["uni", "ladder", "n"], ascending=[True, False, True])
    return A, C


def n_star(C, uni, bar=BAR, col="adm_pub"):
    """Smallest LADDER rung whose share >= bar (rungs above it must also hold)."""
    d = C[(C.uni == uni) & (C.ladder)].sort_values("n")
    for i, (_, r) in enumerate(d.iterrows()):
        if np.isfinite(r[col]) and r[col] >= bar and bool((d.iloc[i:][col] >= bar).all()):
            return int(r.n)
    return None


# ---------------------------------------------------------------- walk-forward W2
def walk_forward(G, rets_by_uni, extra_by_uni):
    out = []
    for (uname, b, c), cell in G.groupby(["uni", "book", "cost"]):
        rets = rets_by_uni[uname]
        elig = cell[(cell.dMaxDD_IS >= 1.0) & np.isfinite(cell.rate_IS)]
        pick = elig.sort_values("rate_IS").iloc[0].arm if len(elig) else None
        ro = win(rets[(b, "control", c)], "OOS")
        mc = metrics(ro)
        rec = dict(uni=uname, book=b, n=int(cell.n.iloc[0]), ladder=bool(cell.ladder.iloc[0]),
                   cost=c, pick=pick, n_elig=len(elig),
                   ctl_OOS_CAGR=mc["CAGR"], ctl_OOS_Sharpe=mc["Sharpe"], ctl_OOS_MaxDD=mc["MaxDD"])
        if pick is not None:
            ra = win(rets[(b, pick, c)], "OOS")
            ma = metrics(ra)
            dc, dd, rt = dpair(ro, ra)
            rec.update(OOS_CAGR=ma["CAGR"], OOS_Sharpe=ma["Sharpe"], OOS_MaxDD=ma["MaxDD"],
                       IS_rate=float(cell[cell.arm == pick].rate_IS.iloc[0]),
                       OOS_rate=rt, OOS_dMaxDD=dd)
            r_is = cell.set_index("arm").rate_IS
            r_oos = cell.set_index("arm").rate_OOS
            rec["spearman_IS_OOS"] = H.spearman(r_is.values, r_oos.values)
            rec["n_both"] = int((np.isfinite(r_is.values) & np.isfinite(r_oos.values)).sum())
        ex = extra_by_uni[uname]
        rec.update(spy_OOS_Sharpe=ex["spy"], v2_OOS_Sharpe=ex["v2"], v1_OOS_Sharpe=ex["v1"],
                   spy_OOS_CAGR=ex["spy_c"], v2_OOS_CAGR=ex["v2_c"])
        out.append(rec)
    return pd.DataFrame(out)


# ---------------------------------------------------------------- main
def main():
    t_start = time.time()
    print("=" * 210)
    print("IDEA 124 — book-size-floor-for-any-quoted-price (lane B, 2026-09-07)")
    print(f"Ladder n in {LADDER} (plain composite, equal weight GROSS/n, ungated base) "
          f"+ OFF-LADDER V1u (5 names, vol-scaled, 15% each).")
    print(f"{len(ARMS)} treated arms x {len(PUB_COSTS)} published rungs x {len(BOOKS)} books "
          f"x {len(UNIS)} universes.  Sign axes: D1 cost {COST_RUNGS}, D2 window IS/OOS, "
          f"D3 panel {NDRAW} draws x q in {DROP_FRACS} (seed {SEED}), tau in {TAUS}.")
    print(f"Headline (q,tau) = ({Q_STAR},{TAU_STAR}) inherited from idea 119/122; "
          f"floor bar = {BAR:.0%} of published rows admissible.  ALL 12 grid points reported.")
    print("=" * 210)

    G_all, D3_all, rets_by_uni, extra_by_uni, repro = [], [], {}, {}, []
    for uname, kw in UNIS:
        px, start, S, spy, bars, rets, G, v1_net, v2_net = build_grid(uname, kw)
        R, nrep = gate_pricelist(uname, px, S, start)
        if len(R):
            print(f"[gate] G3 idea 94 committed pricelist reproduction ({nrep} rows, "
                  f"books TOP20+EWall): max|d dCAGR| {R.e_dCAGR.max():.2e}  "
                  f"max|d dMaxDD| {R.e_dMaxDD.max():.2e}  max|d rate| {R.e_rate.max():.2e}  "
                  f"({'PASS' if max(R.e_dCAGR.max(), R.e_dMaxDD.max(), R.e_rate.max()) < 1e-10 else 'FAIL'})")
            repro.append(R)
        G_all.append(G)
        rets_by_uni[uname] = rets
        extra_by_uni[uname] = dict(
            spy=metrics(win(spy, "OOS"))["Sharpe"], spy_c=metrics(win(spy, "OOS"))["CAGR"],
            v2=metrics(win(v2_net[PCOST], "OOS"))["Sharpe"],
            v2_c=metrics(win(v2_net[PCOST], "OOS"))["CAGR"],
            v1=metrics(win(v1_net[PCOST], "OOS"))["Sharpe"])
        print(f"\n[D3] {uname}: {len(DROP_FRACS)*NDRAW} draws x {len(BOOKS)} books x "
              f"{len(ARMS)} arms ...", flush=True)
        D3_all.append(bootstrap(uname, px, start))

    G = pd.concat(G_all, ignore_index=True)
    B = pd.concat(D3_all, ignore_index=True)
    D3 = d3_table(B)
    if repro:
        pd.concat(repro, ignore_index=True).to_csv(f"{OUT}.reproduction.csv", index=False)

    # ---------------- A. the full grid
    print("\n" + "=" * 210)
    print(f"A. FULL GRID — {len(G)} arm-points, ALL reported "
          f"({len(BOOKS)} books x {len(ARMS)} arms x {len(PUB_COSTS)} rungs x {len(UNIS)} unis)")
    print(fmt(G[["uni", "book", "n", "cost", "arm", "names", "gross", "TO", "CAGR", "Sharpe",
                 "MaxDD", "dCAGR", "dMaxDD", "rate", "dMaxDD_IS", "dMaxDD_OOS",
                 "D1_pass", "D2_pass", "p4a_v2", "p4b", "f4b"]]))

    # ---------------- B. the floor curve at the headline
    A, C = floor_curve(G, D3, Q_STAR, TAU_STAR, "full")
    print("\n" + "=" * 210)
    print(f"B. THE FLOOR CURVE at the headline (q={Q_STAR}, tau={TAU_STAR}) — "
          f"admissible = D1(cost) AND D2(window) AND D3(panel)")
    print(fmt(C))
    for uname, _ in UNIS:
        ns_p = n_star(C, uname, BAR, "adm_pub")
        ns_a = n_star(C, uname, BAR, "adm_all")
        print(f"  n* [{uname}] at bar {BAR:.0%}: published rows -> "
              f"{ns_p if ns_p else 'NOT REACHED on the ladder'};  all rows -> "
              f"{ns_a if ns_a else 'NOT REACHED on the ladder'}")

    # ---------------- C. all 12 grid points of the two tuned params
    print("\n" + "=" * 210)
    print("C. ALL 12 (q, tau) GRID POINTS — admissible share of PUBLISHED rows by rung, "
          "and the implied n*")
    grid_rows = []
    for q in DROP_FRACS:
        for tau in TAUS:
            _, Cq = floor_curve(G, D3, q, tau, "full")
            for uname, _ in UNIS:
                d = Cq[Cq.uni == uname]
                rec = dict(q=q, tau=tau, uni=uname,
                           n_star_pub=n_star(Cq, uname, BAR, "adm_pub"),
                           n_star_all=n_star(Cq, uname, BAR, "adm_all"))
                for _, r in d.iterrows():
                    rec[r.book] = r.adm_pub
                grid_rows.append(rec)
    GP = pd.DataFrame(grid_rows)
    print(fmt(GP))
    GP.to_csv(f"{OUT}.paramgrid.csv", index=False)

    # ---------------- D. P3 — is it the count or the vol scaler?
    print("\n" + "=" * 210)
    print("D. P3 — TOP5 vs V1u (same 5 names, same 15% weights, same gross; V1u adds the "
          "vol scaler)")
    P3 = C[C.book.isin(["TOP5", "V1u", "TOP3", "TOP10"])].copy()
    print(fmt(P3))
    med = D3[D3.q == Q_STAR].groupby(["uni", "book"]).frac_pos_full.median().reset_index()
    print("\n  median draw-level frac_pos_full by book (q=%.2f):" % Q_STAR)
    print(fmt(med))

    # ---------------- E. rule 8 W1 — the floor out of sample
    print("\n" + "=" * 210)
    print("E. RULE 8 / W1 — the FLOOR chosen on 2009-2016 only, then read on 2017-2026")
    _, C_is = floor_curve(G, D3, Q_STAR, TAU_STAR, "IS")
    _, C_oos = floor_curve(G, D3, Q_STAR, TAU_STAR, "OOS")
    W1 = C_is.merge(C_oos, on=["uni", "book", "n", "ladder"], suffixes=("_IS", "_OOS"))
    W1 = W1.merge(C[["uni", "book", "adm_pub", "adm_all"]], on=["uni", "book"])
    W1 = W1.rename(columns={"adm_pub": "adm_pub_full", "adm_all": "adm_all_full"})
    print(fmt(W1[["uni", "book", "n", "ladder", "pub_IS", "adm_pub_IS", "adm_all_IS",
                  "pub_OOS", "adm_pub_OOS", "adm_all_OOS", "adm_pub_full"]]))
    for uname, _ in UNIS:
        a = n_star(C_is, uname, BAR, "adm_pub")
        b_ = n_star(C_oos, uname, BAR, "adm_pub")
        print(f"  [{uname}] n*_IS = {a if a else 'NOT REACHED'}   ->   "
              f"n*_OOS = {b_ if b_ else 'NOT REACHED'}   "
              f"(n*_full = {n_star(C, uname, BAR, 'adm_pub')})")
    W1.to_csv(f"{OUT}.walkforward_floor.csv", index=False)

    # ---------------- F. rule 8 W2 — the price list at each rung, OOS
    print("\n" + "=" * 210)
    print("F. RULE 8 / W2 — idea 94's selector S1 inside each rung; OOS read once")
    Wf = walk_forward(G, rets_by_uni, extra_by_uni)
    print(fmt(Wf[["uni", "book", "n", "cost", "pick", "n_elig", "IS_rate", "OOS_rate",
                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "ctl_OOS_Sharpe", "ctl_OOS_CAGR",
                  "v2_OOS_Sharpe", "spy_OOS_Sharpe", "spy_OOS_CAGR", "spearman_IS_OOS",
                  "n_both"]]))
    print("\n  mean over cells by rung (ladder rungs only):")
    lad = Wf[Wf.ladder]
    print(fmt(lad.groupby(["n"]).agg(cells=("pick", "size"),
                                     OOS_Sharpe=("OOS_Sharpe", "mean"),
                                     OOS_CAGR=("OOS_CAGR", "mean"),
                                     OOS_MaxDD=("OOS_MaxDD", "mean"),
                                     ctl_OOS_Sharpe=("ctl_OOS_Sharpe", "mean"),
                                     spearman=("spearman_IS_OOS", "mean")).reset_index()))
    print(f"\n  V1u (off-ladder) rows: mean OOS Sharpe "
          f"{Wf[~Wf.ladder].OOS_Sharpe.mean():.4f}, mean spearman "
          f"{Wf[~Wf.ladder].spearman_IS_OOS.mean():.4f}")
    Wf.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---------------- G. both KEEP paths
    print("\n" + "=" * 210)
    print("G. BOTH KEEP PATHS (PROTOCOL rule 4) over all arm-points")
    K = G.groupby(["uni", "book", "n", "cost"]).agg(
        rows=("arm", "size"), p4a_v2=("p4a_v2", "sum"), p4a_v1=("p4a_v1", "sum"),
        p4b=("p4b", "sum")).reset_index()
    print(fmt(K))
    print(f"\n  TOTAL: 4a (vs LIVE RULES v2) {int(G.p4a_v2.sum())}/{len(G)};  "
          f"4a (vs RULES v1, idea 94's comparand) {int(G.p4a_v1.sum())}/{len(G)};  "
          f"4b {int(G.p4b.sum())}/{len(G)}")
    if G.p4b.any():
        print("\n  every 4b pass:")
        print(fmt(G[G.p4b][["uni", "book", "n", "cost", "arm", "CAGR", "Sharpe", "MaxDD",
                            "H1", "H2", "OOS_Sharpe", "m_H1", "m_H2", "m_OOS", "m_DD",
                            "m_CAGR", "D1_pass", "D2_pass"]]))
        adm = A.set_index(["uni", "book", "arm", "cost"]).admissible
        q4 = G[G.p4b].copy()
        q4["quotable"] = [bool(adm.get((r.uni, r.book, r.arm, r.cost), False))
                          for _, r in q4.iterrows()]
        print(f"\n  of the {len(q4)} 4b passes, {int(q4.quotable.sum())} have a QUOTABLE price "
              f"(denominator admissible on all three axes)")

    # ---------------- H. prediction scorecard
    print("\n" + "=" * 210)
    print("H. PREDICTION SCORECARD")
    mono = []
    for uname, _ in UNIS:
        d = C[(C.uni == uname) & C.ladder].sort_values("n")
        v = d.adm_pub.values
        mono.append(bool(np.all(np.diff(v[np.isfinite(v)]) >= -1e-12)))
        print(f"  P1 [{uname}] curve (n={list(d.n)}): "
              f"{[round(float(x),3) for x in v]}  monotone: {mono[-1]}")
    print(f"  P1 monotone on both panels: {'CONFIRMED' if all(mono) else 'REFUTED'}")
    ns = {u: n_star(C, u, BAR, "adm_pub") for u, _ in UNIS}
    p2 = all(v is not None and 10 <= v <= 20 for v in ns.values())
    print(f"  P2 floor in [10, 20]: n* = {ns}  ({'CONFIRMED' if p2 else 'REFUTED'})")
    for uname, _ in UNIS:
        t5 = C[(C.uni == uname) & (C.book == "TOP5")].iloc[0]
        v1 = C[(C.uni == uname) & (C.book == "V1u")].iloc[0]
        print(f"  P3 [{uname}] TOP5 adm_pub {t5.adm_pub:.3f} ({int(t5.pub)} pub) vs "
              f"V1u {v1.adm_pub:.3f} ({int(v1.pub)} pub) -> "
              f"{'CONFIRMED' if t5.adm_pub > v1.adm_pub else 'REFUTED'}")
    p4 = len(set(ns.values())) == 1 and None not in ns.values()
    print(f"  P4 same n* on both panels (an absolute count, not a share): "
          f"{'CONFIRMED' if p4 else 'REFUTED'} — {ns}")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    B.to_csv(f"{OUT}.draws.csv", index=False)
    D3.to_csv(f"{OUT}.d3.csv", index=False)
    A.to_csv(f"{OUT}.signtest.csv", index=False)
    C.to_csv(f"{OUT}.floorcurve.csv", index=False)
    print(f"\nWrote {STEM}.{{grid,draws,d3,signtest,floorcurve,paramgrid,walkforward,"
          f"walkforward_floor,reproduction}}.csv   total {time.time()-t_start:.0f}s")


if __name__ == "__main__":
    main()
