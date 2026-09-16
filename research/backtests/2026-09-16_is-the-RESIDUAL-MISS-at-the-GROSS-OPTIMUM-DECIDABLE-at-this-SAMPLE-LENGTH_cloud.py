#!/usr/bin/env python3
"""Idea 1083 (cloud lane, 2026-09-16) — is the 1.0-1.3pp RESIDUAL MISS at the GROSS OPTIMUM
DECIDABLE at this SAMPLE LENGTH?

QUESTION (QUEUE idea 1083, verbatim)
    idea 1071 reproduced 1064's empty joint window and put its best miss at 1.270 pp (U56,
    g=0.45) and 1.012 pp (B136), both binding on the 4b CAGR floor rather than the DD cap.  On
    this record's own SE work (1012/1042) a margin that size may be inside the tape's resolution.
    Bootstrap the MISS at the gross optimum on both panels, report its 90% interval, and say
    whether "the window is empty" is a claim this tape can carry.  Max 2 params (block length,
    draws).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. BLOCK LENGTH  L in {21, 63, 126, 252} trading days.
    2. DRAWS         D in {200, 1000}.
    All 4 x 2 = 8 cells reported on BOTH panels, for EVERY gross rung.

WHAT IS BEING BOOTSTRAPPED, and why it is a JOINT resample
    MISS(g) = max( |MaxDD_book(g)| - |MaxDD_live| , 0.70*CAGR_SPY - CAGR_book(g) ) * 100
    Every term on the right is measured on the SAME tape: the book at rung g, the LIVE RULES v2
    book, and SPY.  A bootstrap that resampled only the book would hold the two bars fixed and
    understate the interval.  So one circular block index is drawn per replicate and applied to
    ALL series at once — SPY, the live book and every gross rung — which preserves the
    cross-series alignment that the bars depend on and resamples the bars with the book.

WHAT HAD TO BE SAID BEFORE ANY NUMBER
    (a) MaxDD is a PATH functional, not an average.  Block resampling reorders episodes, so the
        DD leg is the leg this method distorts most, and it distorts it in a KNOWN direction:
        reshuffling tends to BREAK long declines, so a bootstrapped |MaxDD| is biased SMALL and
        the DD leg's contribution to MISS is biased DOWN.  That is exactly why the block length
        is a dial and why all four are published: if the interval's verdict moves with L, the
        verdict belongs to the resampling and not to the tape.  Gate G4 measures the bias
        directly (median bootstrapped |MaxDD| against the realised one, per L).
    (b) The CAGR leg is a ratio of two compounded returns and is the leg a block bootstrap
        handles well.  1071 found this is the BINDING leg at the optimum on both panels, which is
        the favourable case for this method — stated in advance, not after the fact.
    (c) DECIDABILITY RULE, fixed before the run: "the window is empty" is DECIDABLE at 90% iff
        the 5th percentile of MISS over the draws is > 0.  If the interval straddles 0 the
        claim is NOT decidable at this sample length and 1064's and 1071's window verdicts are
        reported as UNRESOLVED rather than as established.

RULE 8.  The gross rung is chosen on IS (2009-2016) ALONE by minimising IS MISS, and the OOS
    (2017-2026) MISS, CAGR, Sharpe and MaxDD of that rung are read ONCE, against SPY and against
    the live RULES v2 book.  Both KEEP paths are scored at every rung, full sample and OOS.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels; every level is optimistic
    and the CAGR floor and DD cap are read against SPY, a real index, so every MISS published
    here is a LOWER bound on the true one and every 4b count an UPPER bound.  The bootstrap
    resamples the same inflated tape and cannot correct that: it prices SAMPLING error only.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-RESIDUAL-MISS-at-the-GROSS-OPTIMUM-DECIDABLE-at-this-SAMPLE-LENGTH"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
FREQ = "W"
HOLD = 126
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136"]

GROSSES = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
BLOCKS = [21, 63, 126, 252]      # dial 1
DRAWS = [200, 1000]              # dial 2
SEED = 20260916

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1071_MISS = {"U56": 1.270, "B136": 1.012}       # idea 1071's committed optimum MISS, same day
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[priced[t, young]]
        keep = set(int(c) for c in young)
        need = NTOP - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def miss_from(cagr_book, dd_book, dd_live, cagr_spy):
    return 100.0 * np.maximum(np.abs(dd_book) - np.abs(dd_live), CAGR_FLOOR * cagr_spy - cagr_book)


def cagr_dd(M):
    """Column-wise CAGR and MaxDD of a (T x k) matrix of daily returns."""
    eq = np.cumprod(1.0 + M, axis=0)
    cagr = eq[-1] ** (252.0 / M.shape[0]) - 1.0
    dd = (eq / np.maximum.accumulate(eq, axis=0) - 1.0).min(axis=0)
    return cagr, dd


def circ_idx(rng, T, L, n):
    """Circular block bootstrap index of length T (n = ceil(T/L) blocks)."""
    starts = rng.integers(0, T, size=n)
    off = np.arange(L)
    return ((starts[:, None] + off[None, :]).ravel() % T)[:T]


def main():
    t0 = time.time()
    P(f"# Idea 1083 (cloud lane, {DATE}) — is the RESIDUAL MISS at the GROSS OPTIMUM DECIDABLE "
      f"at this SAMPLE LENGTH?")
    P(f"# 2 tuned dials: BLOCK LENGTH {BLOCKS} x DRAWS {DRAWS}. All 8 cells x 2 panels reported.")
    P(f"# Fixed (NOT dials): CAND20 legs, NTOP {NTOP}, max_vol {MAXVOL}, cost {COST:.0f} bps, "
      f"LAG {LAG}, cadence {FREQ}, min hold {HOLD}; gross ladder {GROSSES} FULLY reported.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) MaxDD is a PATH functional; block resampling breaks long declines, so bootstrapped")
    P("#       |MaxDD| is biased SMALL and the DD leg's share of MISS is biased DOWN. G4 measures")
    P("#       that bias directly, per block length.")
    P("#   (b) 1071 found the CAGR leg BINDING at the optimum on both panels — the leg a block")
    P("#       bootstrap handles WELL. Stated in advance.")
    P("#   (c) DECIDABILITY: 'the window is empty' is DECIDABLE at 90% iff the 5th percentile of")
    P("#       MISS over the draws is > 0. Straddling 0 -> the verdict is UNRESOLVED, not proven.")
    P("")

    ladrows, btrows, gaterows, pickrows, benchrows = [], [], [], [], []
    gates = {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        K = len(px.columns)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        reb = np.flatnonzero(mk)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf

        warm = np.zeros(len(idx), dtype=bool)
        warm[WARMUP:] = True
        oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
        ins = warm & ~oos
        oos_w, ins_w = oos[warm], ins[warm]

        spy = px["SPY"].pct_change().fillna(0.0).values[warm]
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values[warm]

        # the gross ladder: one net-return column per rung, all rebuilt (never scaled — 1071's G4)
        cols = []
        for g in GROSSES:
            W = build(rank_key, elig, priced, reb, HOLD, len(idx), K, g)
            gr, tn = nrun(rets, lagmat(W), np.roll(mk, LAG))
            cols.append((gr - tn * COST / 1e4)[warm])
        BOOK = np.column_stack(cols)                       # (Tw x 10)
        ALL = np.column_stack([spy, live, BOOK])           # (Tw x 12), resampled jointly
        Tw = ALL.shape[0]

        # ---------------- gates --------------------------------------------------------------
        if panel == "U56":
            g75 = BOOK[:, GROSSES.index(0.75)]
            m = fmet(g75)
            d = max(abs(m[0] - A936_WH126[0]), abs(m[1] - A936_WH126[1]), abs(m[2] - A936_WH126[2]))
            gates["G1 CROSS-RUN vs 936 committed W/H126 triple"] = (d, d < 5e-3)
            Wc = build(rank_key, elig, priced, reb, HOLD, len(idx), K, 0.75)
            eng = backtest(px, pd.DataFrame(Wc, index=idx, columns=px.columns),
                           cost_bps=COST, freq=FREQ)["returns"].values[warm]
            d2 = float(np.abs(eng - g75).max())
            gates["G2 fast runner == engine.backtest"] = (d2, d2 < 1e-12)
        sc_, ss_, sd_ = fmet(spy)
        so = fmet(spy[oos_w])
        lc_, ls_, ld_ = fmet(live)
        lo = fmet(live[oos_w])
        d3 = max(abs(so[0] - SPY_OOS_COMMITTED[0]), abs(so[1] - SPY_OOS_COMMITTED[1]),
                 abs(so[2] - SPY_OOS_COMMITTED[2])) if panel == "U56" else 0.0
        if panel == "U56":
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d6 = abs(ld_ - LIVE_MAXDD_COMMITTED)
            gates["G6 live RULES v2 MaxDD == committed -12.05%"] = (d6, d6 < 5e-4)
        benchrows += [dict(panel=panel, series="SPY", CAGR=sc_, Sharpe=ss_, MaxDD=sd_,
                           OOS_CAGR=so[0], OOS_Sharpe=so[1], OOS_MaxDD=so[2]),
                      dict(panel=panel, series="RULESv2", CAGR=lc_, Sharpe=ls_, MaxDD=ld_,
                           OOS_CAGR=lo[0], OOS_Sharpe=lo[1], OOS_MaxDD=lo[2])]
        P(f"## {panel}: {K} cols, {Tw} scored days {idx[WARMUP].date()}..{idx[-1].date()}")
        P(f"   SPY      full {sc_:.2%} / {ss_:.4f} / {sd_:.2%}   OOS {so[0]:.2%} / {so[1]:.4f} / {so[2]:.2%}")
        P(f"   RULES v2 full {lc_:.2%} / {ls_:.4f} / {ld_:.2%}   OOS {lo[0]:.2%} / {lo[1]:.4f} / {lo[2]:.2%}")

        # ---------------- the realised ladder -------------------------------------------------
        h = Tw // 2
        for j, g in enumerate(GROSSES):
            r = BOOK[:, j]
            c, s, dd = fmet(r)
            ic, is_, idd = fmet(r[ins_w])
            oc, os_, odd = fmet(r[oos_w])
            l4b = dict(L_H1=fsharpe(r[:h]) > fsharpe(spy[:h]), L_H2=fsharpe(r[h:]) > fsharpe(spy[h:]),
                       L_OOS=os_ > fmet(spy[oos_w])[1], L_DD=abs(dd) <= DD_CAP * abs(sd_),
                       L_CAGR=c >= CAGR_FLOOR * sc_)
            l4a = dict(A_H1=fsharpe(r[:h]) > fsharpe(live[:h]),
                       A_H2=fsharpe(r[h:]) > fsharpe(live[h:]), A_DD=dd >= ld_)
            l4bo = dict(O_S=os_ > so[1], O_DD=abs(odd) <= DD_CAP * abs(so[2]),
                        O_CAGR=oc >= CAGR_FLOOR * so[0])
            ladrows.append(dict(panel=panel, gross=g, CAGR=c, Sharpe=s, MaxDD=dd,
                                H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
                                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                                MISS=float(miss_from(c, dd, ld_, sc_)),
                                MISS_is=float(miss_from(ic, idd, fmet(live[ins_w])[2], fmet(spy[ins_w])[0])),
                                MISS_oos=float(miss_from(oc, odd, lo[2], so[0])),
                                **l4b, **l4a, **l4bo,
                                pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                                pass4b_oos=all(l4bo.values())))
        lad = pd.DataFrame([r for r in ladrows if r["panel"] == panel])
        gstar = float(lad.loc[lad.MISS.idxmin(), "gross"])
        mstar = float(lad.MISS.min())
        P(f"   realised ladder: MISS* = {mstar:.3f} pp at g* = {gstar:.2f}; "
          f"window open at {int((lad.MISS<=0).sum())} of {len(lad)} rungs")
        if panel in A1071_MISS:
            d7 = abs(mstar - A1071_MISS[panel])
            gates[f"G5 CROSS-RUN 1071's committed optimum MISS ({panel})"] = (d7, d7 < 0.30)

        # ---------------- the bootstrap -------------------------------------------------------
        jstar = GROSSES.index(gstar)
        for L in BLOCKS:
            for D in DRAWS:
                rng = np.random.default_rng(SEED + 7919 * L + 31 * D + (0 if panel == "U56" else 1))
                nblk = int(np.ceil(Tw / L))
                MS = np.empty((D, len(GROSSES)))
                DDb = np.empty((D, len(GROSSES)))
                MSTAR = np.empty(D)
                LEGDD = np.empty(D)
                LEGCG = np.empty(D)
                for d_ in range(D):
                    ii = circ_idx(rng, Tw, L, nblk)
                    S = ALL[ii]
                    cg, dd = cagr_dd(S)
                    spy_c, live_dd = cg[0], dd[1]
                    bc, bd = cg[2:], dd[2:]
                    MS[d_] = miss_from(bc, bd, live_dd, spy_c)
                    DDb[d_] = bd
                    MSTAR[d_] = MS[d_].min()
                    LEGDD[d_] = 100.0 * (abs(bd[jstar]) - abs(live_dd))
                    LEGCG[d_] = 100.0 * (CAGR_FLOOR * spy_c - bc[jstar])
                at = MS[:, jstar]
                btrows.append(dict(
                    panel=panel, block=L, draws=D, gstar=gstar, MISS_realised=mstar,
                    MISS_median=float(np.median(at)),
                    MISS_p05=float(np.percentile(at, 5)), MISS_p95=float(np.percentile(at, 95)),
                    MISS_width=float(np.percentile(at, 95) - np.percentile(at, 5)),
                    P_window_open=float((at <= 0).mean()),
                    decidable_empty=bool(np.percentile(at, 5) > 0),
                    MISTAR_median=float(np.median(MSTAR)),
                    MISTAR_p05=float(np.percentile(MSTAR, 5)),
                    MISTAR_p95=float(np.percentile(MSTAR, 95)),
                    P_any_rung_open=float((MSTAR <= 0).mean()),
                    decidable_empty_anyrung=bool(np.percentile(MSTAR, 5) > 0),
                    legDD_median=float(np.median(LEGDD)), legCAGR_median=float(np.median(LEGCG)),
                    share_DD_binds=float((LEGDD > LEGCG).mean()),
                    dd_bias_pp=float(100 * (np.median(np.abs(DDb[:, jstar])) -
                                            abs(lad.loc[lad.gross == gstar, "MaxDD"].iloc[0])))))
        P(f"   bootstrap done ({time.time()-t0:.0f}s)")

        # ---------------- rule 8 --------------------------------------------------------------
        pick = lad.loc[lad.MISS_is.idxmin()]
        pickrows.append(dict(panel=panel, chooser="C_ISMISS", gross=float(pick.gross),
                             IS_MISS=float(pick.MISS_is), OOS_MISS=float(pick.MISS_oos),
                             OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                             OOS_MaxDD=float(pick.OOS_MaxDD),
                             spy_OOS_CAGR=so[0], spy_OOS_Sharpe=so[1], spy_OOS_MaxDD=so[2],
                             live_OOS_CAGR=lo[0], live_OOS_Sharpe=lo[1], live_OOS_MaxDD=lo[2],
                             full_CAGR=float(pick.CAGR), full_Sharpe=float(pick.Sharpe),
                             full_MaxDD=float(pick.MaxDD), H1=float(pick.H1), H2=float(pick.H2),
                             pass4b=bool(pick.pass4b), pass4b_oos=bool(pick.pass4b_oos),
                             pass4a=bool(pick.pass4a), gstar_full=gstar))

    # ------------------------------------------------------------------ gates FIRST
    P("")
    P("## GATES (printed before any result number)")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: |d| = {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(ok)))
    bt = pd.DataFrame(btrows)
    lad = pd.DataFrame(ladrows)
    pk = pd.DataFrame(pickrows)
    bias = bt.groupby("block").dd_bias_pp.median()
    ok4 = bool((bias < 0).all())
    P(f"   {'PASS' if ok4 else 'FAIL'}  G4 bootstrapped |MaxDD| is biased SMALL as declared: "
      f"median dd bias by block "
      + ", ".join(f"L={int(b)} {v:+.2f} pp" for b, v in bias.items()))
    gaterows.append(dict(gate="G4 bootstrapped |MaxDD| biased SMALL at every block length",
                         value=float(bias.max()), passed=ok4))

    # ------------------------------------------------------------------ results
    P("")
    P("## THE GROSS LADDER (all 10 rungs, both panels)")
    for panel in PANELS:
        s = lad[lad.panel == panel]
        P(f"   --- {panel} ---")
        P("      g     CAGR    Sharpe   MaxDD    MISS   MISS_is  MISS_oos  4b 4a 4bOOS")
        for _, r in s.iterrows():
            P(f"      {r.gross:.2f} {r.CAGR:7.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%} {r.MISS:7.3f} "
              f"{r.MISS_is:8.3f} {r.MISS_oos:9.3f}   {int(r.pass4b)}  {int(r.pass4a)}    "
              f"{int(r.pass4b_oos)}")

    P("")
    P("## THE BOOTSTRAP AT g* (8 cells per panel, ALL reported)")
    for panel in PANELS:
        s = bt[bt.panel == panel]
        P(f"   --- {panel}, g* = {s.gstar.iloc[0]:.2f}, realised MISS {s.MISS_realised.iloc[0]:.3f} pp ---")
        P("      L    D     median   [p05, p95]        width   P(open)  DECIDABLE-EMPTY  ddbias")
        for _, r in s.iterrows():
            P(f"      {int(r.block):3d} {int(r.draws):4d}  {r.MISS_median:7.3f}  "
              f"[{r.MISS_p05:6.3f}, {r.MISS_p95:6.3f}]  {r.MISS_width:6.3f}  {r.P_window_open:6.3f}   "
              f"{str(bool(r.decidable_empty)):>5}          {r.dd_bias_pp:+.2f} pp")
        P(f"      MIN-OVER-RUNGS MISS* (the statistic 1064/1071 actually published):")
        for _, r in s.iterrows():
            P(f"      {int(r.block):3d} {int(r.draws):4d}  {r.MISTAR_median:7.3f}  "
              f"[{r.MISTAR_p05:6.3f}, {r.MISTAR_p95:6.3f}]  "
              f"P(any rung open) {r.P_any_rung_open:6.3f}   DECIDABLE-EMPTY "
              f"{str(bool(r.decidable_empty_anyrung)):>5}")
        P(f"      binding leg at g*: DD binds on {s.share_DD_binds.median():.3f} of draws "
          f"(median legDD {s.legDD_median.median():+.3f} pp vs legCAGR "
          f"{s.legCAGR_median.median():+.3f} pp)")

    P("")
    P("## RULE 8 — gross chosen on IS(2009-2016) MISS alone, OOS(2017-2026) read ONCE")
    for _, r in pk.iterrows():
        P(f"   {r.panel} C_ISMISS: picks g={r.gross:.2f} (full-sample argmin g*={r.gstar_full:.2f}) "
          f"-> OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%}, OOS MISS "
          f"{r.OOS_MISS:.3f} pp | SPY OOS {r.spy_OOS_CAGR:.2%} / {r.spy_OOS_Sharpe:.4f} / "
          f"{r.spy_OOS_MaxDD:.2%} | RULES v2 OOS {r.live_OOS_CAGR:.2%} / {r.live_OOS_Sharpe:.4f} "
          f"/ {r.live_OOS_MaxDD:.2%} | full {r.full_CAGR:.2%} / {r.full_Sharpe:.4f} / "
          f"{r.full_MaxDD:.2%} halves {r.H1:.4f}/{r.H2:.4f} | 4b {r.pass4b} 4b_OOS "
          f"{r.pass4b_oos} 4a {r.pass4a}")

    P("")
    P("## HYPOTHESES (declared before the run, scored as written)")
    H = [
        ("H_DECIDE  the empty-window verdict is DECIDABLE at 90% in EVERY cell",
         bool(bt.decidable_empty.all()),
         f"{int(bt.decidable_empty.sum())} of {len(bt)} cells"),
        ("H_STABLE  the decidability verdict does NOT move with the block length",
         bool(bt.groupby(['panel', 'draws']).decidable_empty.nunique().max() == 1),
         "; ".join(f"{p_}/D={int(d_)}: " + "".join("T" if v else "F" for v in
          gg.sort_values('block').decidable_empty) for (p_, d_), gg in
          bt.groupby(['panel', 'draws']))),
        ("H_WIDTH   the 90% MISS width at g* exceeds the realised MISS itself somewhere",
         bool((bt.MISS_width > bt.MISS_realised).any()),
         f"max width {bt.MISS_width.max():.3f} pp vs realised "
         f"{bt.MISS_realised.min():.3f}-{bt.MISS_realised.max():.3f} pp"),
        ("H_CAGRLEG the CAGR leg binds at g* on a majority of draws (1071's reading)",
         bool(bt.share_DD_binds.median() < 0.5), f"DD binds on {bt.share_DD_binds.median():.3f}"),
        ("H_DRAWS   doubling+ the draws (200 -> 1000) moves no cell's verdict",
         bool(bt.groupby(['panel', 'block']).decidable_empty.nunique().max() == 1),
         "; ".join(f"{p_}/L={int(l_)}: " + "".join("T" if v else "F" for v in
          gg.sort_values('draws').decidable_empty) for (p_, l_), gg in
          bt.groupby(['panel', 'block']))),
        ("H_WF      the IS-only gross pick clears 4b OUT OF SAMPLE on either panel",
         bool(pk.pass4b_oos.any()), f"{int(pk.pass4b_oos.sum())} of {len(pk)} picks"),
    ]
    for n, ok, note in H:
        P(f"   {'PASS' if ok else 'FAIL'}  {n}  [{note}]")

    dump(lad, "ladder"); dump(bt, "bootstrap"); dump(pk, "rule8")
    dump(pd.DataFrame(benchrows), "benchmarks"); dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame([dict(hypothesis=n, passed=bool(o), note=t) for n, o, t in H]), "hypotheses")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
