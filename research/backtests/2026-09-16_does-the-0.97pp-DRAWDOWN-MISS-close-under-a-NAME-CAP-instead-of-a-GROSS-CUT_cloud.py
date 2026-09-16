#!/usr/bin/env python3
"""Idea 1071 (cloud lane, 2026-09-16) — does the 0.97pp DRAWDOWN MISS close under a NAME CAP
instead of a GROSS CUT?

QUESTION (QUEUE idea 1071, verbatim)
    idea 1064 found de-grossing cannot thread 4b's CAGR floor and the live book's -12.05% DD at
    once (window empty 18 of 18, best miss 0.97 pp on W/H126) because gross scales CAGR and DD
    together one for one.  Test whether a per-name weight cap or an n above 20 — which cut
    drawdown WITHOUT cutting expected return proportionally — closes the same 0.97 pp, and price
    the result against the gross-matched null at the same realised DD.  Max 2 params (n,
    per-name cap).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. N       in {20, 25, 30, 40}.  20 is the incumbent (936/1059/1064/1065's CAND20).
    2. CAPMULT k in {1.00, 1.25, 1.50, 2.00, INF}.  Per-name target weight is
           w_i = min(g / n_sel, k * g / N)
       with the residual held as CASH (never re-spread, never leverage).  k = INF is the
       incumbent construction (re-spread over whatever names are eligible).
    All 4 x 5 = 20 points are reported at every panel, for the book AND for the null.

WHY A CAP IS NOT A GROSS CUT IN DISGUISE — DECLARED BEFORE ANY NUMBER
    (a) ARITHMETIC, stated up front so it cannot be presented later as a finding: in a book that
        always fills all N slots the cap binds NEVER when k >= 1 and binds UNIFORMLY when k < 1,
        and a uniform bind is exactly a gross cut to k*g.  k < 1 is therefore NOT on the ladder:
        it would re-run 1064.  The cap is non-degenerate only through BREADTH — this book's
        eligibility gate (200d MA and vol20 < 0.60) leaves n_sel < N on thin days, and the
        incumbent construction answers that by CONCENTRATING (1/n_sel each).  k pins how far it
        may concentrate; the rest goes to cash.  So the cap is a DE-GROSS THAT ONLY FIRES WHEN
        BREADTH IS THIN, and thin breadth is when drawdowns happen.  That is the refutable claim.
    (b) The N dial cuts drawdown by diversification at UNCHANGED gross, so unlike 1064's ladder it
        is not required to pay for DD with CAGR one for one.  If neither dial closes the gap, the
        0.97 pp miss is a property of the book's returns and not of its weighting.
    (c) GATE G5 measures (a) directly: the k = 1.00 book's realised gross is reported beside the
        incumbent's, and the share of days the cap binds is published.  If that share is ~0 the
        cap dial is INERT and must be reported as inert, not as a null result.

THE TARGET, arithmetic and fixed in advance
    MISS (pp) = max( |MaxDD| - |LIVE_MaxDD| , CAGR_FLOOR*SPY_CAGR - CAGR ) * 100
    i.e. the binding shortfall of the JOINT window 1064 found empty: a drawdown no worse than the
    live book's -12.05% AND a CAGR at or above 70% of SPY's.  MISS <= 0 means the window is open
    at that point.  Reported at every grid point, for FULL, IS and OOS windows.

RULE 8.  Every grid point is scored on IS (2009-2016) alone and read ONCE on OOS (2017-2026).
    Two IS-only choosers (C_ISSHARPE, C_ISDD) pick a point on the first half alone; the OOS
    CAGR/Sharpe/MaxDD of what each picks is reported against the live RULES v2 baseline and SPY.

THE NULL.  Gross-matched, holding-count-matched, min-hold-matched: at every rebalance date the
    null fills its free slots with names drawn uniformly at random from the names PRICED that day
    (no eligibility gate — the record's convention), under the same H = 126 min hold and the same
    cap rule.  The queue asks for the comparison AT THE SAME REALISED DD: each null path is
    scaled by the unique lambda in (0, 1] that makes its |MaxDD| equal the book's, which is exact
    because a gross scale multiplies BOTH the return contribution and the turnover bill by lambda
    (gated, G4).  The published contrast is CAGR at matched drawdown.

    POST-RUN CORRECTION, left beside the declaration rather than replacing it: **G4 FAILS and the
    declaration above is WRONG.**  Weights DRIFT between rebalances and the cash sleeve does not,
    so a book REBUILT at gross lambda*g is not lambda times the book at g.  What the lambda match
    actually builds is the DAILY-REBALANCED blend of the null path with cash, which is a real and
    implementable book but a different one; G4b prices the gap between the two conventions on
    CAGR, Sharpe and MaxDD so the contrast can be read with it in hand.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every level here
    is optimistic, most of all the CAGR floor and the DD cap against SPY, which is a real index.
    Every 4b / 4a count is an UPPER bound.  The book-vs-null contrast is drawn from the same pool
    over the same tape and the bias very largely cancels out of it.
"""
from __future__ import annotations

import hashlib
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
SLUG = "does-the-0.97pp-DRAWDOWN-MISS-close-under-a-NAME-CAP-instead-of-a-GROSS-CUT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
HOLD = 126
LEGS = [(21, 252), (0, 126), (0, 63)]          # CAND20, 936/1064's construction
NSEED = 20

NS = [20, 25, 30, 40]                           # dial 1
CAPS = [1.00, 1.25, 1.50, 2.00, np.inf]         # dial 2
GROSSES_1064 = [0.75, 0.65, 0.55, 0.45, 0.35]   # 1064's ladder, REPRODUCED not tuned

PANELS = ["U56", "B136"]

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)    # idea 936 grid.csv U56/CAND20/W/H126/0.75/10bps
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ---------------------------------------------------------------- fast runner (gated vs engine)
def nrun(rets, wt, mk):
    """Net-of-nothing GROSS portfolio returns and turnover; cost applied by the caller.
    Construction copied from idea 936/1064's cloud scripts so the runs are comparable."""
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
    return (held * rets).sum(axis=1), turn, held


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


def maxdd(r):
    eq = np.cumprod(1.0 + np.asarray(r, float))
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    """936/1064's selection score (higher = better) and the eligibility gate. No vol scaler."""
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, cap, H, T, K, gross):
    """Target weights under MIN HOLD H, slot count N and per-name cap multiple `cap`.
    w_i = min(gross/n_sel, cap*gross/N); residual -> CASH.  Also returns, per rebalance date,
    the count of filled slots and the realised target gross."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb, gross_by_reb = [], []
    per_cap = cap * gross / N if np.isfinite(cap) else np.inf
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
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
        nsel_by_reb.append(len(sel))
        if len(sel):
            w = min(gross / len(sel), per_cap)
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = w
            gross_by_reb.append(w * len(sel))
        else:
            gross_by_reb.append(0.0)
    return W, np.array(nsel_by_reb), np.array(gross_by_reb)


def build_null(rng, priced, reb, N, cap, H, T, K, gross):
    """Same machinery, random ranks, NO eligibility gate (the record's convention)."""
    rank_key = rng.random((T, K))
    elig = np.ones((T, K), dtype=bool)
    return build(rank_key, elig, priced, reb, N, cap, H, T, K, gross)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def miss_pp(cagr, dd, live_dd, spy_cagr):
    """The binding shortfall of 1064's empty window, in percentage points. <= 0 -> window open."""
    return 100.0 * max(abs(dd) - abs(live_dd), CAGR_FLOOR * spy_cagr - cagr)


def lam_for_dd(r, target_dd, lo=1e-4, hi=1.0, it=60):
    """lambda in (0,1] with |MaxDD(lambda*r)| = |target_dd|.  |MaxDD| is monotone in lambda."""
    if abs(maxdd(r)) <= abs(target_dd):
        return None                      # null already drier than the book; reported, not clipped
    a, b = lo, hi
    for _ in range(it):
        m = 0.5 * (a + b)
        if abs(maxdd(m * r)) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def main():
    t0 = time.time()
    P(f"# Idea 1071 (cloud lane, {DATE}) — does the 0.97pp DRAWDOWN MISS close under a NAME CAP "
      f"instead of a GROSS CUT?")
    P(f"# 2 tuned dials: N {NS} x CAPMULT {CAPS}. ALL 20 points reported, book AND null.")
    P(f"# Fixed (NOT dials): CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, cost "
      f"{COST:.0f} bps, LAG {LAG}, cadence {FREQ}, min hold {HOLD}, canonical period-end dates.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) cap k<1 IS a gross cut (uniform bind) and is therefore NOT on the ladder;")
    P("#       k>=1 binds only through BREADTH (n_sel < N), i.e. it de-grosses exactly when the")
    P("#       eligibility gate thins out.  If the bind share is ~0 the dial is INERT and is")
    P("#       reported inert (gate G5), not as a null result.")
    P("#   (b) the N dial cuts DD by diversification at UNCHANGED gross, so it is not forced to")
    P("#       pay for drawdown with CAGR one for one the way 1064's gross ladder is.")
    P("#   (c) MISS = max(|MaxDD|-|live|, 0.70*SPY_CAGR - CAGR) in pp; MISS<=0 = window open.")
    P("")

    rows, nullrows, gaterows, ladderrows = [], [], [], []
    picks, benchrows = [], []
    gates = {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136"))
        px = px.dropna(how="all").ffill()
        idx = px.index
        K = len(px.columns)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)      # ascending sort = best first
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        P(f"## {panel}: {K} columns, {len(idx)} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates")
        P(f"   SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2   full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  "
          f"halves {lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb), dict(panel=panel, series="RULESv2", **lb)]
        live_dd = lb["MaxDD"]

        # ---- GATES ---------------------------------------------------------------------------
        if panel == "U56":
            W, _, _ = build(rank_key, elig, priced, reb, 20, np.inf, HOLD, len(idx), K, GROSS0)
            wdf = pd.DataFrame(W, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            g, tn, _ = nrun(rets, lagmat(W), np.roll(mk, LAG))
            fast = g - tn * COST / 1e4
            d1 = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N20, k=INF)"] = (d1, d1 < 1e-12)
            m = fmet(fast[warm])
            d2 = max(abs(m[0] - A936_WH126[0]), abs(m[1] - A936_WH126[1]), abs(m[2] - A936_WH126[2]))
            gates["G2 CROSS-RUN vs 936 committed W/H126 triple"] = (d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            # G4: a gross scale multiplies net returns exactly -> the lambda match is exact
            W2, _, _ = build(rank_key, elig, priced, reb, 20, np.inf, HOLD, len(idx), K, 0.5 * GROSS0)
            g2, t2, _ = nrun(rets, lagmat(W2), np.roll(mk, LAG))
            r_rebuilt, r_scaled = (g2 - t2 * COST / 1e4)[warm], (0.5 * fast)[warm]
            d4 = float(np.abs(r_rebuilt - r_scaled).max())
            gates["G4 net returns scale EXACTLY with gross (lambda match is exact)"] = (d4, d4 < 1e-15)
            mr, ms = fmet(r_rebuilt), fmet(r_scaled)
            P(f"   G4b PRICING THE G4 FAILURE at g=0.375: REBUILT {mr[0]:.4%}/{mr[1]:.4f}/{mr[2]:.4%} "
              f"vs CASH-BLEND {ms[0]:.4%}/{ms[1]:.4f}/{ms[2]:.4%}  -> dCAGR {100*(ms[0]-mr[0]):+.3f} pp, "
              f"dMaxDD {100*(ms[2]-mr[2]):+.3f} pp, dSharpe {ms[1]-mr[1]:+.4f}")
            gates["G4b |dMaxDD| REBUILT vs CASH-BLEND at g=0.375 (pp)"] = (
                abs(100 * (ms[2] - mr[2])), abs(100 * (ms[2] - mr[2])) < 1.0)
            d5 = abs(live_dd - LIVE_MAXDD_COMMITTED)
            gates["G6 live RULES v2 MaxDD == committed -12.05%"] = (d5, d5 < 5e-4)

        # ---- the 20-point grid ----------------------------------------------------------------
        for N in NS:
            for cap in CAPS:
                W, nsel, grs = build(rank_key, elig, priced, reb, N, cap, HOLD, len(idx), K, GROSS0)
                g, tn, _ = nrun(rets, lagmat(W), np.roll(mk, LAG))
                r = g - tn * COST / 1e4
                b = blocks(r, warm, ins, oos)
                l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                capname = "INF" if not np.isfinite(cap) else f"{cap:.2f}"
                row = dict(panel=panel, N=N, cap=capname,
                           bind_share=float((grs < GROSS0 - 1e-12).mean()),
                           mean_gross=float(grs.mean()), mean_nsel=float(nsel.mean()),
                           turnover=float(tn[warm].sum() / (warm.sum() / 252.0)), **b,
                           MISS_full=miss_pp(b["CAGR"], b["MaxDD"], live_dd, sb["CAGR"]),
                           MISS_is=miss_pp(b["IS_CAGR"], b["IS_MaxDD"], lb["IS_MaxDD"], sb["IS_CAGR"]),
                           MISS_oos=miss_pp(b["OOS_CAGR"], b["OOS_MaxDD"], lb["OOS_MaxDD"], sb["OOS_CAGR"]),
                           **l4b, **l4a, **l4bo,
                           pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                           pass4b_oos=all(l4bo.values()))
                row["pass4b_full_and_oos"] = row["pass4b"] and row["pass4b_oos"]
                rows.append(row)

                # ---- gross-matched null at the SAME realised DD -------------------------------
                bc, nc, lams = [], 0, []
                for s in range(NSEED):
                    rng = np.random.default_rng(mdseed(panel, N, capname, s))
                    Wn, _, _ = build_null(rng, priced, reb, N, cap, HOLD, len(idx), K, GROSS0)
                    gn, tnn, _ = nrun(rets, lagmat(Wn), np.roll(mk, LAG))
                    rn = (gn - tnn * COST / 1e4)[warm]
                    lam = lam_for_dd(rn, b["MaxDD"])
                    if lam is None:
                        nc += 1
                        bc.append(fmet(rn)[0])      # already inside the book's DD; no scaling
                        lams.append(1.0)
                    else:
                        bc.append(fmet(lam * rn)[0])
                        lams.append(lam)
                bc = np.array(bc)
                nullrows.append(dict(panel=panel, N=N, cap=capname, seeds=NSEED,
                                     book_CAGR=b["CAGR"], book_MaxDD=b["MaxDD"],
                                     null_ddmatched_CAGR_median=float(np.median(bc)),
                                     null_ddmatched_CAGR_p90=float(np.percentile(bc, 90)),
                                     null_ddmatched_CAGR_max=float(bc.max()),
                                     null_lambda_median=float(np.median(lams)),
                                     null_already_drier=nc,
                                     book_pct_of_null=float((bc < b["CAGR"]).mean())))

        # ---- 1064's GROSS ladder, reproduced at the incumbent N=20/k=INF ---------------------
        for gr in GROSSES_1064:
            W, _, _ = build(rank_key, elig, priced, reb, 20, np.inf, HOLD, len(idx), K, gr)
            g, tn, _ = nrun(rets, lagmat(W), np.roll(mk, LAG))
            r = g - tn * COST / 1e4
            b = blocks(r, warm, ins, oos)
            ladderrows.append(dict(panel=panel, dial="GROSS", value=gr, **b,
                                   MISS_full=miss_pp(b["CAGR"], b["MaxDD"], live_dd, sb["CAGR"]),
                                   **legs_4b(b, sb), **legs_4a(b, lb),
                                   pass4b=all(legs_4b(b, sb).values()),
                                   pass4a=all(legs_4a(b, lb).values())))

        # ---- RULE 8: IS-only choosers over the 20 points, OOS read once ----------------------
        gp = pd.DataFrame([r for r in rows if r["panel"] == panel])
        for cname, key, asc in [("C_ISSHARPE", "IS_Sharpe", False), ("C_ISDD", "IS_MaxDD", False)]:
            pick = gp.sort_values(key, ascending=asc).iloc[0]
            picks.append(dict(panel=panel, chooser=cname, N=int(pick["N"]), cap=pick["cap"],
                              IS_Sharpe=pick["IS_Sharpe"], IS_MaxDD=pick["IS_MaxDD"],
                              OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                              OOS_MaxDD=pick["OOS_MaxDD"],
                              spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                              spy_OOS_MaxDD=sb["OOS_MaxDD"],
                              live_OOS_CAGR=lb["OOS_CAGR"], live_OOS_Sharpe=lb["OOS_Sharpe"],
                              live_OOS_MaxDD=lb["OOS_MaxDD"],
                              O_S=pick["O_S"], O_DD=pick["O_DD"], O_CAGR=pick["O_CAGR"],
                              pass4b_oos=bool(pick["pass4b_oos"]),
                              pass4b_full=bool(pick["pass4b"]), pass4a=bool(pick["pass4a"]),
                              MISS_oos=pick["MISS_oos"], MISS_full=pick["MISS_full"]))
        P(f"   grid done  ({time.time()-t0:.0f}s)")

    # ------------------------------------------------------------------ gates, printed FIRST
    P("")
    P("## GATES (printed before any result number)")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: |d| = {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(ok)))
    grid = pd.DataFrame(rows)
    nul = pd.DataFrame(nullrows)
    lad = pd.DataFrame(ladderrows)
    pk = pd.DataFrame(picks)
    bn = pd.DataFrame(benchrows)
    # G5: is the cap dial inert?
    u = grid[grid.panel == "U56"]
    bind = u[u.cap == "1.00"]["bind_share"].max()
    gaterows.append(dict(gate="G5 cap dial is LIVE (k=1.00 binds on >5% of rebalance dates, U56)",
                         value=float(bind), passed=bool(bind > 0.05)))
    P(f"   {'PASS' if bind > 0.05 else 'FAIL'}  G5 cap dial is LIVE: k=1.00 binds on "
      f"{bind:.1%} of U56 rebalance dates")

    # ------------------------------------------------------------------ results
    P("")
    P("## 1064's GROSS ladder, reproduced (N=20, k=INF) — the miss it reported")
    for panel in PANELS:
        s = lad[lad.panel == panel]
        P(f"   {panel}: min MISS over the 5 rungs = {s.MISS_full.min():.3f} pp "
          f"at gross {s.loc[s.MISS_full.idxmin(),'value']:.2f}; window open at "
          f"{int((s.MISS_full<=0).sum())} of {len(s)} rungs")
        for _, r in s.iterrows():
            P(f"      g={r.value:.2f}  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  "
              f"MISS {r.MISS_full:6.3f} pp   4b {r.pass4b}  4a {r.pass4a}")

    P("")
    P("## THE 20-POINT GRID (all points, both panels)")
    for panel in PANELS:
        s = grid[grid.panel == panel]
        P(f"   --- {panel} ---")
        P("      N  cap   bind%  gross  nsel   CAGR    Sharpe   MaxDD    turn   MISS_pp  4b  4a  4bOOS")
        for _, r in s.iterrows():
            P(f"      {int(r.N):2d} {r.cap:>4}  {r.bind_share:5.1%} {r.mean_gross:6.3f} "
              f"{r.mean_nsel:5.1f} {r.CAGR:7.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%} "
              f"{r.turnover:6.2f} {r.MISS_full:8.3f}   {int(r.pass4b)}   {int(r.pass4a)}    "
              f"{int(r.pass4b_oos)}")
        P(f"      min MISS_full {s.MISS_full.min():.3f} pp at N={int(s.loc[s.MISS_full.idxmin(),'N'])} "
          f"cap={s.loc[s.MISS_full.idxmin(),'cap']};  window open at "
          f"{int((s.MISS_full<=0).sum())} of {len(s)} points")
        P(f"      4b full {int(s.pass4b.sum())}/{len(s)}   4b OOS {int(s.pass4b_oos.sum())}/{len(s)}"
          f"   4a {int(s.pass4a.sum())}/{len(s)}")

    P("")
    P("## THE NULL AT THE SAME REALISED DRAWDOWN (book CAGR vs the gross-matched null's, "
      f"{NSEED} seeds/point)")
    for panel in PANELS:
        s = nul[nul.panel == panel]
        P(f"   {panel}: median book percentile in its own DD-matched null = "
          f"{s.book_pct_of_null.median():.3f}; book above the null MEDIAN at "
          f"{int((s.book_CAGR > s.null_ddmatched_CAGR_median).sum())} of {len(s)} points; "
          f"median lambda {s.null_lambda_median.median():.3f}")
        worst = s.loc[s.book_pct_of_null.idxmin()]
        best = s.loc[s.book_pct_of_null.idxmax()]
        P(f"      weakest N={int(worst.N)}/{worst.cap}: book {worst.book_CAGR:.2%} vs null median "
          f"{worst.null_ddmatched_CAGR_median:.2%} (pct {worst.book_pct_of_null:.2f})")
        P(f"      strongest N={int(best.N)}/{best.cap}: book {best.book_CAGR:.2%} vs null median "
          f"{best.null_ddmatched_CAGR_median:.2%} (pct {best.book_pct_of_null:.2f})")

    P("")
    P("## RULE 8 — IS(2009-2016)-only choosers over the 20 points, OOS(2017-2026) read ONCE")
    for _, r in pk.iterrows():
        P(f"   {r.panel} {r.chooser}: picks N={r.N} cap={r.cap} -> OOS {r.OOS_CAGR:.2%} / "
          f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%}  | SPY OOS {r.spy_OOS_CAGR:.2%} / "
          f"{r.spy_OOS_Sharpe:.4f} / {r.spy_OOS_MaxDD:.2%} | RULES v2 OOS {r.live_OOS_CAGR:.2%} / "
          f"{r.live_OOS_Sharpe:.4f} / {r.live_OOS_MaxDD:.2%} | 4b_OOS {r.pass4b_oos} "
          f"(O_S {r.O_S} O_DD {r.O_DD} O_CAGR {r.O_CAGR}) 4b_full {r.pass4b_full} 4a {r.pass4a} "
          f"MISS_oos {r.MISS_oos:.3f} pp")

    P("")
    P("## HYPOTHESES (declared before the run, scored as written)")
    u, b136 = grid[grid.panel == "U56"], grid[grid.panel == "B136"]
    lu = lad[lad.panel == "U56"]
    H = []
    H.append(("H_CLOSE  some (N, cap) point opens 1064's joint window (MISS_full <= 0)",
              bool((grid.MISS_full <= 0).any()),
              f"min MISS_full U56 {u.MISS_full.min():.3f} pp, B136 {b136.MISS_full.min():.3f} pp"))
    H.append(("H_BETTER the best (N, cap) MISS beats the best GROSS-ladder MISS on U56",
              bool(u.MISS_full.min() < lu.MISS_full.min()),
              f"{u.MISS_full.min():.3f} vs {lu.MISS_full.min():.3f} pp"))
    H.append(("H_NDIAL  MISS is monotone DECREASING in N at cap=INF (diversification cuts DD)",
              bool(list(u[u.cap == 'INF'].sort_values('N').MISS_full) ==
                   sorted(u[u.cap == 'INF'].MISS_full, reverse=True)),
              " -> ".join(f"{v:.3f}" for v in u[u.cap == 'INF'].sort_values('N').MISS_full)))
    H.append(("H_CAPLIVE the cap dial moves MaxDD by >= 0.5 pp somewhere on U56",
              bool(100 * (u.groupby('N').MaxDD.max() - u.groupby('N').MaxDD.min()).max() >= 0.5),
              f"max within-N MaxDD spread {100*(u.groupby('N').MaxDD.max()-u.groupby('N').MaxDD.min()).max():.3f} pp"))
    H.append(("H_NULL   the book beats its DD-matched null's MEDIAN CAGR at >= 75% of points",
              bool((nul.book_CAGR > nul.null_ddmatched_CAGR_median).mean() >= 0.75),
              f"{(nul.book_CAGR > nul.null_ddmatched_CAGR_median).mean():.3f}"))
    H.append(("H_WF     >= 1 rule-8 pick clears 4b OUT OF SAMPLE",
              bool(pk.pass4b_oos.any()), f"{int(pk.pass4b_oos.sum())} of {len(pk)} picks"))
    H.append(("H_4A     no point clears 4a (the DD leg is a book fact, not a weighting fact)",
              bool(not grid.pass4a.any()), f"{int(grid.pass4a.sum())} of {len(grid)} points pass 4a"))
    for name, ok, note in H:
        P(f"   {'PASS' if ok else 'FAIL'}  {name}  [{note}]")

    dump(grid, "grid"); dump(nul, "null"); dump(lad, "ladder"); dump(pk, "rule8")
    dump(bn, "benchmarks"); dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame([dict(hypothesis=n, passed=bool(o), note=t) for n, o, t in H]), "hypotheses")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
