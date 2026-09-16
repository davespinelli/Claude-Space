#!/usr/bin/env python3
"""Idea 1096 (cloud lane, 2026-09-16) — is RULE-8 REACHABILITY a COST-RUNG object across the
record's COMMITTED PICKS?

QUESTION (QUEUE idea 1096, verbatim; note QUEUE carries TWO lines numbered 1096 — defect 932 —
and this is the rule-8-reachability one)
    idea 1094 found the U56 n=12/H=21 cell survives to 63 bps while the IS-only Sharpe chooser
    that REACHES it switches away at 15 bps, i.e. what a procedure can select is ~5x more
    cost-fragile than what the cell delivers.  Re-run the record's committed rule-8 picks at
    0/10/25/50 bps and report how many stated PICKS (not numbers) move, and at which rung.
    Max 2 params (claim set, cost rung).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: CLAIM SET {CORE, WIDE} x COST RUNG {0, 10, 25, 50}, 8 cells, ALL
    published.  CORE is the four ladder families the record's committed rule-8 runs actually
    walked (N, H, GROSS, CADENCE) on both panels = 8 ladders; WIDE adds the joint (N,H) grid,
    the book family and the max_vol ladder = 14 ladders.  COST IS NOT A DIAL THE BOOK CAN
    CHOOSE: it is PROTOCOL rule 2's execution assumption, walked here with NOTHING selected on
    it — every chooser is re-run separately at each rung and only ever sees the cost its own
    book pays.  The CHOOSER axis {C_ISSHARPE, C_ISDD, C_ISCAGR} is REPORTED at every cell and
    never fitted on: the headline is C_ISSHARPE, the record's own default, fixed before the run.

THE OBJECT BEING COUNTED
    A "committed PICK" is (ladder, chooser) -> one rung, chosen on IS 2009-2016 ALONE.  A pick
    MOVES at rung c if that identity differs from the identity the same chooser states at
    PROTOCOL's 10 bps.  MOVE RUNG = the first c on a 0..200 bps 1-bp ladder at which it differs.
    That is a statement about PICKS, not about numbers: every number moves at every rung.

THE COST LADDER IS EXACT RATHER THAN RE-RUN
    `engine.backtest` computes r = (held*rets).sum(1) - turnover*c/1e4, and neither `held` nor
    `turnover` depends on c (selection reads prices, not the book's own net path).  So one run
    per cell yields the WHOLE ladder exactly: r(c) = g - tn*c/1e4.  G1/G1b/G1c check this
    against `engine.backtest` at 10/25/50 bps to machine precision, which is what licenses the
    201-rung fine ladder used for both the MOVE RUNG and each cell's breakeven rung c*.

DECLARED BEFORE ANY NUMBER
    (a) The queue's premise, inherited from 1094: a PROCEDURE is far more cost-fragile than the
        CELL it reaches.  SIGNATURE, declared as a bar: median(c* of the 10-bps pick) is at
        least 3x median(MOVE RUNG) over the CORE ladders, and a majority of CORE picks move at
        or below 25 bps (H_5X, H_MOVE).
    (b) The RIVAL reading, named in advance so the result cannot be read only one way: within a
        ladder, cost is very nearly a COMMON shift (turnover spread across rungs is small next
        to the IS-Sharpe spread), so picks are cost-STABLE and 1094's 15-bps switch was a
        property of one near-tied pair, not of procedures in general.  SIGNATURE: few or no
        CORE picks move by 50 bps, and the ladders that do move are exactly the ones with the
        widest turnover spread (H_TURNSPREAD).
    (c) A third outcome named in advance: picks may FLICKER (move, return, move again), in which
        case "the rung at which the pick moves" is not a well-defined object at all and the
        honest report is the flicker count, not a rung (H_ABSORB).
    (d) MECHANISM check: if cost is what moves picks, picks must move toward LOWER turnover.
        A pick that moves toward HIGHER turnover as the rung rises is noise, not cost (H_DIR).
    (e) BENCHMARK ASYMMETRY (the record's open idea 1063): 4b's bar is SPY, which pays no
        turnover at any rung, so raising the rung is a one-sided handicap on the VERDICT legs.
        The headline keeps PROTOCOL's convention; nothing in the PICK half depends on it,
        because a chooser never sees SPY.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here
    is optimistic, every 4b/4a count an UPPER bound, and every breakeven rung c* an UPPER bound
    on the cost a real book of this kind could have paid.  The PICK-move half is a contrast
    between two selections over the same inflated tape and the bias very largely cancels out of
    it; it does NOT cancel out of the 4b legs, which are measured against SPY, a real index.
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
SLUG = "is-RULE-8-REACHABILITY-a-COST-RUNG-object-across-the-record-s-COMMITTED-PICKS"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]      # CAND20 legs, 936/1064/1071/1082/1086/1094's build
CAPNAME = "INF"

CS = [0.0, 10.0, 25.0, 50.0]               # dial 2 — the queue's own rungs
CFINE = np.arange(0.0, 200.5, 1.0)         # 201 rungs, for MOVE RUNG and c*
PROTOCOL_RUNG = 10.0
PANELS = ["U56", "B136"]
CHOOSERS = [("C_ISSHARPE", "IS_Sharpe"), ("C_ISDD", "IS_MaxDD"), ("C_ISCAGR", "IS_CAGR")]

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]    # 1082/1086/1094's ladder verbatim
HS = [21, 63, 126, 252]                    # 1086's hold ladder (+252, published in 1083's family)
GS = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]   # 1083's 10-rung ladder
CADS = ["D", "W", "M", "Q"]                # 930/931's cadence ladder
MVS = [0.40, 0.50, 0.60, 0.80, 9.99]       # max_vol ladder (9.99 == no vol gate)
BOOKS = ["TOP5", "TOP10", "TOP20", "EWELIG", "BAND03"]              # 930's family, rebuilt here

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)          # 936/1071/1082/1094, U56 N=20 H=126, 10 bps
A1086_CAND = dict(CAGR=0.1679622583830449, Sharpe=1.162499076998433,
                  MaxDD=-0.19477561065817217)         # 1086/1094, U56 N=12 H=21, 10 bps
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1094_CSTAR = 63.0                                    # 1094: c* of the U56 N=12/H=21 cell, L_H1
A1094_SWITCH = 15.0                                   # 1094: the rung at which its chooser left
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


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px, max_vol=MAXVOL):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < max_vol)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """Target weights under MIN HOLD H and slot count N, cap = INF (1082/1086/1094's build)."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
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
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def build_ewelig(elig, priced, reb, T, K, gross):
    """EWELIG: equal weight over EVERY eligible priced name at each rebalance, gross/|elig|."""
    W = np.zeros((T, K))
    for i, t in enumerate(reb):
        sel = np.flatnonzero(elig[t] & priced[t])
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


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


def cstar(g, tn, warm, ins, oos, sb):
    """Largest rung on the 201-rung ladder at which the cell still clears 4b FULL, plus the
    first failing rung, the leg that fails there, and whether the pass set is an interval."""
    ok = []
    for c in CFINE:
        ok.append(all(legs_4b(blocks(g - tn * c / 1e4, warm, ins, oos), sb).values()))
    ok = np.array(ok)
    if not ok[0]:
        return (np.nan, 0.0, "fails at 0 bps", True)
    run = int(np.argmin(ok)) if (~ok).any() else len(ok)
    c_s = float(CFINE[run - 1])
    c_f = float(CFINE[run]) if run < len(ok) else np.nan
    interval = bool(ok[:run].all() and not ok[run:].any())
    if run < len(ok):
        bad = ",".join(k for k, v in legs_4b(blocks(g - tn * CFINE[run] / 1e4, warm, ins, oos),
                                            sb).items() if not v)
    else:
        bad = "none within 200 bps"
    return (c_s, c_f, bad, interval)


# ---------------------------------------------------------------- IS statistics on a fine ladder
def is_stats_fine(g, tn, ins):
    """IS Sharpe / MaxDD / CAGR for one cell at every rung of CFINE (vectorised over rungs)."""
    gi, ti = g[ins], tn[ins]
    R = gi[None, :] - ti[None, :] * (CFINE[:, None] / 1e4)      # (rungs, days)
    mu = R.mean(axis=1) * 252.0
    sd = R.std(axis=1, ddof=1) * np.sqrt(252.0)
    eq = np.cumprod(1.0 + R, axis=1)
    cagr = eq[:, -1] ** (252.0 / R.shape[1]) - 1.0
    dd = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
    return dict(IS_Sharpe=mu / sd, IS_MaxDD=dd, IS_CAGR=cagr)


def main():
    t0 = time.time()
    P(f"# Idea 1096 (cloud lane, {DATE}) — is RULE-8 REACHABILITY a COST-RUNG object across the")
    P("#   record's COMMITTED PICKS?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {{CORE, WIDE}} x COST RUNG {CS} = 8 cells,")
    P("#   ALL published.  CORE = the four ladder families the record's rule-8 runs walked")
    P("#   (N, H, GROSS, CADENCE) on both panels = 8 ladders.  WIDE = CORE + joint (N,H) grid +")
    P("#   book family + max_vol ladder = 14 ladders.  COST is NOT a dial the book can choose.")
    P("#   CHOOSER {C_ISSHARPE, C_ISDD, C_ISCAGR} is REPORTED at every cell and never fitted on;")
    P("#   the headline chooser is C_ISSHARPE, the record's default, fixed before the run.")
    P(f"# FROZEN: cap {CAPNAME}, CAND20 legs {LEGS}, gross {GROSS0} (except the GROSS ladder),")
    P(f"#   max_vol {MAXVOL} (except the max_vol ladder), cadence {FREQ} (except the CADENCE")
    P(f"#   ladder), LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, min hold 126 unless dialled.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) QUEUE/1094 premise — a PROCEDURE is ~5x more cost-fragile than the CELL it")
    P(f"#       reaches.  BARS: median c*(10-bps pick) >= 3x median MOVE RUNG (H_5X); a majority")
    P("#       of CORE picks move at or below 25 bps (H_MOVE).")
    P("#   (b) RIVAL — cost is nearly a COMMON shift inside a ladder, so picks are cost-STABLE")
    P("#       and 1094's switch was one near-tied pair (H_TURNSPREAD: movers are exactly the")
    P("#       widest-turnover-spread ladders).")
    P("#   (c) NAMED IN ADVANCE — picks may FLICKER, in which case 'the rung at which the pick")
    P("#       moves' is not a well-defined object and the honest report is a flicker count.")
    P("#   (d) MECHANISM — if cost moves picks, picks move toward LOWER turnover (H_DIR).")
    P("#   (e) 4b's bar is SPY, which pays no turnover: a one-sided handicap on the VERDICT legs")
    P("#       only.  No chooser ever sees SPY, so the PICK half does not depend on it.")
    P("")

    CORE_L = ("L_N", "L_H", "L_G", "L_CAD")

    def cset(l):
        return "CORE" if l in CORE_L else ("DIAG" if l == "L_NH94" else "WIDE")

    cells, gaterows, benchrows = [], [], []
    gates = {}
    store = {}          # (panel, ladder, rung) -> (g, tn)
    ladder_rungs = {}   # (panel, ladder) -> [rungs in build order]
    live_by_panel, spy_by_panel = {}, {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        yrs = warm.sum() / 252.0
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        masks = {f: rebalance_mask(idx, f).values for f in CADS}
        rebs = {f: np.flatnonzero(masks[f]) for f in CADS}
        mkl = {f: np.roll(masks[f], LAG) for f in CADS}

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        spy_by_panel[panel] = sb
        live0 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        live_g, live_tn = live0["returns"].values, live0["turnover"].values
        live_by_panel[panel] = (live_g, live_tn)
        lb10 = blocks(live_g - live_tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)

        P(f"## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{yrs:.2f} scored years")
        P(f"   SPY (uncharged, PROTOCOL 4b bar)  full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / "
          f"{sb['MaxDD']:.2%}  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   4b bars: DD cap {DD_CAP*abs(sb['MaxDD']):.2%} full / "
          f"{DD_CAP*abs(sb['OOS_MaxDD']):.2%} OOS;  CAGR floor {CAGR_FLOOR*sb['CAGR']:.2%} full "
          f"/ {CAGR_FLOOR*sb['OOS_CAGR']:.2%} OOS")
        benchrows.append(dict(panel=panel, series="SPY", cost_bps=np.nan, turnover=0.0, **sb))
        for c in CS:
            lbc = blocks(live_g - live_tn * c / 1e4, warm, ins, oos)
            benchrows.append(dict(panel=panel, series="RULESv2", cost_bps=c,
                                  turnover=float(live_tn[warm].sum() / yrs), **lbc))
            P(f"   RULES v2 @ {c:5.1f} bps  full {lbc['CAGR']:.2%} / {lbc['Sharpe']:.4f} / "
              f"{lbc['MaxDD']:.2%}  OOS {lbc['OOS_CAGR']:.2%} / {lbc['OOS_Sharpe']:.4f} / "
              f"{lbc['OOS_MaxDD']:.2%}")

        # ---------------- the ladders -------------------------------------------------------
        def add(ladder, rung, W, cad="W", claimset="CORE"):
            g, tn = nrun(rets, lagmat(W), mkl[cad])
            store[(panel, ladder, rung)] = (g, tn)
            ladder_rungs.setdefault((panel, ladder), []).append(rung)
            b = blocks(g - tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)
            turn = float(tn[warm].sum() / yrs)
            row = dict(panel=panel, ladder=ladder, rung=str(rung), claimset=claimset,
                       cadence=cad, turnover=turn)
            for c in CS:
                bc = blocks(g - tn * c / 1e4, warm, ins, oos)
                lbc = blocks(live_g - live_tn * c / 1e4, warm, ins, oos)
                l4b, l4a, l4o = legs_4b(bc, sb), legs_4a(bc, lbc), legs_4b_oos(bc, sb)
                row[f"CAGR_{int(c)}"] = bc["CAGR"]
                row[f"Sharpe_{int(c)}"] = bc["Sharpe"]
                row[f"MaxDD_{int(c)}"] = bc["MaxDD"]
                row[f"OOS_Sharpe_{int(c)}"] = bc["OOS_Sharpe"]
                row[f"pass4b_{int(c)}"] = all(l4b.values())
                row[f"pass4a_{int(c)}"] = all(l4a.values())
                row[f"pass4b_oos_{int(c)}"] = all(l4o.values())
            row.update({f"b10_{k}": v for k, v in b.items()})
            cells.append(row)
            return g, tn

        # CORE 1: N ladder at H=126 (1071/1082/1094)
        for N in NS:
            add("L_N", N, build(rank_key, elig, priced, rebs["W"], N, 126, T, K, GROSS0))
        # CORE 2: H ladder at N=12 (1086)
        for H in HS:
            add("L_H", H, build(rank_key, elig, priced, rebs["W"], 12, H, T, K, GROSS0))
        # CORE 3: GROSS ladder at N=20/H=126 (1083)
        for G in GS:
            add("L_G", G, build(rank_key, elig, priced, rebs["W"], 20, 126, T, K, G))
        # CORE 4: CADENCE ladder at N=20/H=126 (930/931)
        for f in CADS:
            add("L_CAD", f, build(rank_key, elig, priced, rebs[f], 20, 126, T, K, GROSS0), cad=f)
        P(f"   CORE ladders built ({time.time()-t0:.0f}s)")

        # WIDE 1: joint (N, H) grid (1094's 27 cells, +H=252)
        for N in NS:
            for H in HS:
                add("L_NH", f"{N}/{H}", build(rank_key, elig, priced, rebs["W"], N, H, T, K,
                                              GROSS0), claimset="WIDE")
        # WIDE 2: book family (930's set, rebuilt here — NOT byte-identical to 930)
        for bk in BOOKS:
            if bk.startswith("TOP"):
                W = build(rank_key, elig, priced, rebs["W"], int(bk[3:]), 126, T, K, GROSS0)
            elif bk == "EWELIG":
                W = build_ewelig(elig, priced, rebs["W"], T, K, GROSS0)
            else:
                W = rules_v2_weights(px).values
            add("L_BOOK", bk, W, claimset="WIDE")
        # WIDE 3: max_vol ladder at N=20/H=126
        for mv in MVS:
            _, el = mech(px, mv)
            add("L_MV", mv, build(rank_key, el, priced, rebs["W"], 20, 126, T, K, GROSS0),
                claimset="WIDE")
        # DIAG (labelled post-hoc, excluded from every CORE/WIDE count): 1094's EXACT joint
        # grid, H in {21, 63, 126} only, so this run's switch rung is comparable to its 15 bps.
        for N in NS:
            for H in (21, 63, 126):
                r = f"{N}/{H}"
                store[(panel, "L_NH94", r)] = store[(panel, "L_NH", r)]
                ladder_rungs.setdefault((panel, "L_NH94"), []).append(r)
        P(f"   WIDE ladders built ({time.time()-t0:.0f}s)")

        # ---------------- gates -------------------------------------------------------------
        if panel == "U56":
            W20 = build(rank_key, elig, priced, rebs["W"], 20, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            g20, t20 = nrun(rets, lagmat(W20), mkl["W"])
            for cg, gname in ((10.0, "G1"), (25.0, "G1b"), (50.0, "G1c")):
                eng = backtest(px, wdf, cost_bps=cg, freq=FREQ)["returns"].values
                d = float(np.abs((g20 - t20 * cg / 1e4)[WARMUP:] - eng[WARMUP:]).max())
                gates[f"{gname} r(c)=g-tn*c/1e4 == engine.backtest at {cg:.0f} bps (U56 N=20 "
                      f"H=126)"] = (d, d < 1e-12)
            m = fmet((g20 - t20 * PROTOCOL_RUNG / 1e4)[warm])
            d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082/1094's committed U56 W/H126 N=20 triple @ 10 bps"] \
                = (d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            gc, tc = store[("U56", "L_NH", "12/21")]
            bc = blocks(gc - tc * PROTOCOL_RUNG / 1e4, warm, ins, oos)
            d4 = max(abs(bc[k] - v) for k, v in A1086_CAND.items())
            gates["G4 CROSS-RUN 1086/1094's committed U56 N=12 H=21 candidate triple @ 10 bps"] \
                = (d4, d4 < 5e-4)
            cs = cstar(gc, tc, warm, ins, oos, sb)
            d4b = abs(cs[0] - A1094_CSTAR)
            gates["G4b CROSS-RUN 1094's committed c* = 63 bps for that cell"] = (d4b, d4b <= 1.0)
            d5 = abs(lb10["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G5 live RULES v2 MaxDD @ 10 bps == committed -12.05%"] = (d5, d5 < 5e-4)
            a = np.random.default_rng(mdseed(panel, 1)).random(8)
            b_ = np.random.default_rng(mdseed(panel, 1)).random(8)
            gates["G7 determinism of the seed recipe"] = (float(np.abs(a - b_).max()), True)

    # ------------------------------------------------------------------ PICKS on the fine ladder
    P("")
    P("# ---- RULE 8: every ladder's IS-only chooser re-run at EVERY rung, OOS read ONCE ----")
    pickrows, moverows = [], []
    fine_cache = {}
    for (panel, ladder), rungs in ladder_rungs.items():
        warm, ins, oos = fine_cache.get(panel, (None, None, None))
        if warm is None:
            idxp = load_universe(broad=(panel == "B136")).dropna(how="all").ffill().index
            warm, ins, oos = windows(idxp)
            fine_cache[panel] = (warm, ins, oos)
        sb = spy_by_panel[panel]
        live_g, live_tn = live_by_panel[panel]
        S = {r: is_stats_fine(*store[(panel, ladder, r)], ins) for r in rungs}
        for cname, key in CHOOSERS:
            M = np.array([S[r][key] for r in rungs])            # (rungs, fine)
            best = np.argmax(M, axis=0)                          # argmax per fine rung
            pick_at = [rungs[i] for i in best]
            p10 = pick_at[int(np.where(CFINE == PROTOCOL_RUNG)[0][0])]
            diff = np.array([p != p10 for p in pick_at])
            move_rung = float(CFINE[np.argmax(diff)]) if diff.any() else np.nan
            COARSE94 = [0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100]
            cm = [c for c in COARSE94 if pick_at[c] != p10]
            move_rung_coarse = float(min(cm)) if cm else np.nan
            flicks = int((np.array(pick_at[1:]) != np.array(pick_at[:-1])).sum())
            absorbing = bool(diff[np.argmax(diff):].all()) if diff.any() else True
            g10, t10 = store[(panel, ladder, p10)]
            cs = cstar(g10, t10, warm, ins, oos, sb)
            turn_path = [float(store[(panel, ladder, p)][1][warm].sum()) for p in pick_at]
            dir_ok = bool(np.all(np.diff(np.array(turn_path)) <= 1e-9))
            moverows.append(dict(panel=panel, ladder=ladder, chooser=cname,
                                 claimset=cset(ladder),
                                 pick_at_10=str(p10), n_rungs=len(rungs),
                                 move_rung_bps=move_rung,
                                 move_rung_on_1094s_coarse_ladder_bps=move_rung_coarse,
                                 moves_within_200=bool(diff.any()),
                                 pick_at_0=str(pick_at[0]), pick_at_25=str(pick_at[25]),
                                 pick_at_50=str(pick_at[50]), pick_at_100=str(pick_at[100]),
                                 pick_at_200=str(pick_at[200]),
                                 n_distinct_picks=len(set(pick_at)), flickers=flicks,
                                 absorbing=absorbing, turnover_non_increasing=dir_ok,
                                 cstar_of_10pick_bps=cs[0], cstar_first_fail_bps=cs[1],
                                 cstar_failing_leg=cs[2],
                                 ratio_cstar_over_move=(cs[0] / move_rung
                                                        if move_rung == move_rung and move_rung > 0
                                                        else np.nan)))
            for c in CS:
                i = int(np.where(CFINE == c)[0][0])
                r = pick_at[i]
                g, tn = store[(panel, ladder, r)]
                b = blocks(g - tn * c / 1e4, warm, ins, oos)
                lbc = blocks(live_g - live_tn * c / 1e4, warm, ins, oos)
                l4b, l4a, l4o = legs_4b(b, sb), legs_4a(b, lbc), legs_4b_oos(b, sb)
                pickrows.append(dict(panel=panel, ladder=ladder, chooser=cname, cost_bps=c,
                                     claimset=cset(ladder), pick=str(r), moved_vs_10=bool(str(r) != str(p10)),
                                     turnover=float(tn[warm].sum() /
                                                    (warm.sum() / 252.0)), **b, **l4b, **l4a,
                                     **l4o, pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                                     pass4b_oos=all(l4o.values()),
                                     spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                                     spy_OOS_MaxDD=sb["OOS_MaxDD"],
                                     live_OOS_Sharpe=lbc["OOS_Sharpe"],
                                     live_OOS_CAGR=lbc["OOS_CAGR"],
                                     live_OOS_MaxDD=lbc["OOS_MaxDD"]))
        P(f"   {panel} {ladder:7s} ({len(rungs)} rungs) done  ({time.time()-t0:.0f}s)")

    cellsdf, pk, mv = pd.DataFrame(cells), pd.DataFrame(pickrows), pd.DataFrame(moverows)

    # ------------------------------------------------------------------ remaining gates
    mono = 0.0
    for _, s in cellsdf.iterrows():
        v = [s[f"CAGR_{int(c)}"] for c in CS]
        mono = max(mono, float(max(0.0, np.max(np.diff(v)))))
    gates["G6 CAGR non-increasing in the cost rung at every cell"] = (mono, mono <= 0.0)
    spread = float((cellsdf.CAGR_0 - cellsdf.CAGR_50).max())
    gates["G8 the cost axis is LIVE (max CAGR spread 0->50 bps >= 1 pp)"] = (spread, spread >= 0.01)
    tspread = float(cellsdf.groupby(["panel", "ladder"]).turnover.apply(lambda x: x.max() - x.min()).max())
    gates["G9 the turnover spread within ladders is LIVE (>= 1x/yr somewhere)"] = (
        tspread, tspread >= 1.0)

    P("")
    P("# ---- GATES (printed before any result number) ----")
    ok = 0
    for k, (d, good) in gates.items():
        P(f"   {'PASS' if good else 'FAIL'}  {k}: {d:.3e}")
        gaterows.append(dict(gate=k, value=d, passed=bool(good)))
        ok += bool(good)
    P(f"   {ok} of {len(gates)} gates pass")

    # ------------------------------------------------------------------ the answer
    P("")
    P("# ---- HOW MANY PICKS MOVE, AND AT WHICH RUNG ----")
    hyp = []
    for cs_ in ("CORE", "WIDE", "ALL"):
        sub = mv[mv.claimset != "DIAG"] if cs_ == "ALL" else mv[mv.claimset == cs_]
        for cname, _ in CHOOSERS:
            s = sub[sub.chooser == cname]
            n = len(s)
            for c in CS:
                col = {0.0: "pick_at_0", 10.0: "pick_at_10", 25.0: "pick_at_25",
                       50.0: "pick_at_50"}[c]
                movd = int((s[col] != s.pick_at_10).sum())
                P(f"   {cs_:4s} {cname:11s}  @{c:5.1f} bps  picks moved vs 10 bps: "
                  f"{movd}/{n}  ({movd/n:.1%})")
    P("")
    for cname, _ in CHOOSERS:
        s = mv[(mv.chooser == cname)]
        for cs_ in ("CORE", "WIDE"):
            t = s[s.claimset == cs_]
            mr = t.move_rung_bps.dropna()
            P(f"   {cs_} {cname}: {len(mr)}/{len(t)} ladders move within 200 bps; MOVE RUNG "
              f"median {mr.median() if len(mr) else float('nan'):.0f} bps, min "
              f"{mr.min() if len(mr) else float('nan'):.0f}, max "
              f"{mr.max() if len(mr) else float('nan'):.0f}; median c*(10-pick) "
              f"{t.cstar_of_10pick_bps.median():.0f} bps; median ratio "
              f"{t.ratio_cstar_over_move.median():.2f}x")

    P("")
    P("# ---- D1 (labelled diagnostic): 1094's EXACT joint (N,H) grid, H in {21,63,126} ----")
    for panel in PANELS:
        d = mv[(mv.panel == panel) & (mv.ladder == "L_NH94") & (mv.chooser == "C_ISSHARPE")]
        if len(d):
            r = d.iloc[0]
            P(f"   {panel}: pick @10 bps {r.pick_at_10}; first differing rung on a 1-bp ladder "
              f"{r.move_rung_bps} bps -> {r.pick_at_25 if r.move_rung_bps==r.move_rung_bps else '-'}"
              f" ; on 1094's PUBLISHED coarse ladder "
              f"{r.move_rung_on_1094s_coarse_ladder_bps} bps (1094 states 15)")
    P("")
    P("# ---- D2 (labelled diagnostic): is the reachability question even ASKABLE? ----")
    nd = mv[mv.claimset != "DIAG"]
    und = int(nd.cstar_of_10pick_bps.isna().sum())
    P(f"   c*(10-bps pick) is UNDEFINED — the pick already fails 4b at 0 bps — for {und} of "
      f"{len(nd)} (panel, ladder, chooser) picks ({und/len(nd):.1%}).  For those the phrase "
      f"'the procedure is more cost-fragile than the cell' has no referent at any rung.")

    P("")
    P("# ---- D3 (labelled diagnostic): the SAME cell sits in all four CORE ladders ----")
    P("#   The anchor is 936/1071/1082/1094's W / H=126 / N=20 / gross 0.75 book — a rung of the")
    P("#   N ladder (20), the H ladder (126), the GROSS ladder (0.75) AND the CADENCE ladder (W).")
    ANCHOR = {"L_N": "20", "L_H": "126", "L_G": "0.75", "L_CAD": "W"}
    anch = []
    for panel in PANELS:
        for c in CS:
            hit = [l for l, r in ANCHOR.items() if len(pk[(pk.panel == panel) & (pk.ladder == l)
                   & (pk.chooser == "C_ISSHARPE") & (pk.cost_bps == c) & (pk["pick"] == r)])]
            miss = {l: pk[(pk.panel == panel) & (pk.ladder == l) &
                          (pk.chooser == "C_ISSHARPE") & (pk.cost_bps == c)]["pick"].iloc[0]
                    for l in ANCHOR if l not in hit}
            P(f"   {panel} @{c:5.1f} bps: C_ISSHARPE reaches the anchor from {len(hit)} of 4 "
              f"CORE ladders {sorted(hit)}; the other ladders pick {miss}")
            anch.append(dict(panel=panel, cost_bps=c, reached_from=len(hit),
                             ladders=";".join(sorted(hit)),
                             others=";".join(f"{k}={v}" for k, v in miss.items())))
    dump(pd.DataFrame(anch), "anchor")

    P("")
    P("# ---- D4 (labelled diagnostic): is a PICK RESOLVED, as opposed to merely STABLE? ----")
    P("#   Margin = IS Sharpe of the 10-bps pick minus the runner-up's, on the same ladder.")
    P("#   The bar is the record's own committed seed-noise floor, idea 877: 0.0145 of Sharpe.")
    SEEDFLOOR = 0.0145
    mrows = []
    for (p_, l_), s_ in cellsdf.groupby(["panel", "ladder"]):
        if l_ == "L_NH94":
            continue
        s_ = s_.sort_values("b10_IS_Sharpe", ascending=False)
        marg = float(s_.iloc[0].b10_IS_Sharpe - s_.iloc[1].b10_IS_Sharpe)
        spr = float(s_.b10_IS_Sharpe.max() - s_.b10_IS_Sharpe.min())
        mrows.append(dict(panel=p_, ladder=l_, claimset=cset(l_), pick=str(s_.iloc[0]["rung"]),
                          runner_up=str(s_.iloc[1]["rung"]), IS_Sharpe_margin=marg,
                          IS_Sharpe_spread=spr, above_877_seed_floor=bool(marg > SEEDFLOOR)))
    md = pd.DataFrame(mrows)
    for _, r in md.iterrows():
        P(f"   {r.panel:4s} {r.ladder:7s} pick {r['pick']:>6s} over {r.runner_up:>6s}: margin "
          f"{r.IS_Sharpe_margin:.4f} of IS Sharpe (ladder spread {r.IS_Sharpe_spread:.4f})  "
          f"{'ABOVE' if r.above_877_seed_floor else 'BELOW'} 877's 0.0145 floor")
    P(f"   {int((~md.above_877_seed_floor).sum())} of {len(md)} picks are decided by LESS than "
      f"the record's own seed-noise floor.")
    dump(md, "margins")

    core = mv[(mv.claimset == "CORE") & (mv.chooser == "C_ISSHARPE")]
    n_core = len(core)
    moved25 = int((core.pick_at_25 != core.pick_at_10).sum())
    h_move = moved25 > n_core / 2.0
    mrm = core.move_rung_bps.dropna().median()
    csm = core.cstar_of_10pick_bps.median()
    h_5x = bool(csm >= 3.0 * mrm) if mrm == mrm and mrm > 0 else False
    med_ratio = float(core.ratio_cstar_over_move.median())
    n_ratio = int(core.ratio_cstar_over_move.notna().sum())
    P("")
    P(f"   H_5X, BOTH statistics: ratio of medians {csm:.0f}/{mrm:.0f} = "
      f"{csm/mrm if mrm else float('nan'):.2f}x (the declared bar reads this one); median of "
      f"per-ladder ratios {med_ratio:.2f}x over the {n_ratio} of {n_core} CORE picks where BOTH "
      f"quantities are defined.")
    h_absorb = bool(core.absorbing.all())
    h_dir = bool(core.turnover_non_increasing.all())
    tsp = cellsdf.groupby(["panel", "ladder"]).turnover.apply(lambda x: x.max() - x.min())
    movers = set(zip(core[core.moves_within_200].panel, core[core.moves_within_200].ladder))
    rank = tsp.sort_values(ascending=False)
    top_spread = set(rank.index[:max(1, len(movers))])
    h_tsp = bool(movers == top_spread) if movers else False
    hyp += [dict(hypothesis="H_MOVE: a majority of CORE C_ISSHARPE picks move by 25 bps",
                 declared="majority", observed=f"{moved25}/{n_core}", passed=bool(h_move)),
            dict(hypothesis="H_5X: median c*(10-bps pick) >= 3x median MOVE RUNG (CORE)",
                 declared=">=3x", observed=f"ratio-of-medians {csm:.0f}/{mrm:.0f} = "
                 f"{csm/mrm if mrm else float('nan'):.2f}x; median-of-ratios {med_ratio:.2f}x "
                 f"over {n_ratio}/{n_core} defined", passed=h_5x),
            dict(hypothesis="H_ABSORB: once a CORE pick moves it never returns",
                 declared="absorbing", observed=f"{int(core.absorbing.sum())}/{n_core}",
                 passed=h_absorb),
            dict(hypothesis="H_DIR: CORE picks move toward LOWER turnover as the rung rises",
                 declared="non-increasing", observed=f"{int(core.turnover_non_increasing.sum())}"
                 f"/{n_core}", passed=h_dir),
            dict(hypothesis="H_TURNSPREAD: the movers are exactly the widest-turnover-spread "
                            "ladders", declared="set equality",
                 observed=f"movers {sorted(movers)}", passed=h_tsp)]

    # verdict movement: how many (ladder, chooser, panel) picks change their 4b/4a verdict
    vch = []
    for (p_, l_, c_), s in pk.groupby(["panel", "ladder", "chooser"]):
        s = s.sort_values("cost_bps")
        vch.append(dict(panel=p_, ladder=l_, chooser=c_,
                        ident_moves=int((s["pick"] != s[s.cost_bps == 10]["pick"].iloc[0]).sum()),
                        v4b_changes=int(s.pass4b.nunique() > 1),
                        v4b_oos_changes=int(s.pass4b_oos.nunique() > 1),
                        v4a_changes=int(s.pass4a.nunique() > 1)))
    vdf = pd.DataFrame(vch)
    P("")
    P(f"   VERDICTS vs IDENTITIES over {{0,10,25,50}} bps ({len(vdf)} (panel,ladder,chooser) "
      f"picks): identity moves in {int((vdf.ident_moves>0).sum())}, 4b-full verdict changes in "
      f"{int(vdf.v4b_changes.sum())}, 4b-OOS in {int(vdf.v4b_oos_changes.sum())}, 4a in "
      f"{int(vdf.v4a_changes.sum())}")
    hyp.append(dict(hypothesis="H_VERDICT: more picks change 4b VERDICT than change IDENTITY "
                               "across 0..50 bps", declared="verdict > identity",
                    observed=f"{int(vdf.v4b_changes.sum())} vs {int((vdf.ident_moves>0).sum())}",
                    passed=bool(vdf.v4b_changes.sum() > (vdf.ident_moves > 0).sum())))

    P("")
    P("# ---- RULE 8 WALK-FORWARD: the picks' OOS record, and BOTH KEEP paths ----")
    for panel in PANELS:
        sb = spy_by_panel[panel]
        P(f"   {panel} SPY OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%}")
        for c in CS:
            s = pk[(pk.panel == panel) & (pk.cost_bps == c) & (pk.chooser == "C_ISSHARPE")]
            P(f"     @{c:5.1f} bps: 4b full {int(s.pass4b.sum())}/{len(s)}, 4b OOS "
              f"{int(s.pass4b_oos.sum())}/{len(s)}, 4a {int(s.pass4a.sum())}/{len(s)}")
            for _, r in s[s.pass4b_oos].iterrows():
                P(f"       4b-OOS PASS  {r.ladder} pick {r['pick']}  OOS {r.OOS_CAGR:.2%} / "
                  f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%}  full {r.CAGR:.2%} / {r.Sharpe:.4f} "
                  f"/ {r.MaxDD:.2%} halves {r.H1:.3f}/{r.H2:.3f}  4b-full {r.pass4b}")
    P(f"   ALL-cell 4b full/OOS/4a counts over {len(cellsdf)} cells x 4 rungs:")
    for c in CS:
        P(f"     @{c:5.1f} bps  4b {int(cellsdf[f'pass4b_{int(c)}'].sum())}/{len(cellsdf)}  "
          f"4b-OOS {int(cellsdf[f'pass4b_oos_{int(c)}'].sum())}/{len(cellsdf)}  "
          f"4a {int(cellsdf[f'pass4a_{int(c)}'].sum())}/{len(cellsdf)}")

    P("")
    P("# ---- HYPOTHESES ----")
    for h in hyp:
        P(f"   {'PASS' if h['passed'] else 'FAIL'}  {h['hypothesis']}  [declared "
          f"{h['declared']}; observed {h['observed']}]")

    dump(cellsdf, "cells")
    dump(pk, "picks")
    dump(mv, "moves")
    dump(vdf, "verdicts")
    dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame(hyp), "hypotheses")
    dump(pd.DataFrame(benchrows), "benchmarks")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
