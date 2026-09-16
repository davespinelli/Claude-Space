#!/usr/bin/env python3
"""Idea 1094 (lane C, 2026-09-16) — does the U56 n=12 / H=21 CANDIDATE survive 25 and 50 bps?

QUESTION (QUEUE idea 1094, verbatim)
    idea 1086's rule-8-reachable 4b pass turns over 7.19x/yr against 3.04x/yr for the same n at
    H=126, so it is 2.4x as cost-exposed as the incumbent hold and was priced at 10 bps only.
    Re-price the whole (n, H) grid at 10/25/50 bps and report at which rung the pass dies.
    Max 2 params (cost rung, H).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    The book's CHOOSABLE dials are exactly TWO and they are 1082/1086's: N in
    {5, 8, 10, 12, 15, 20, 25, 30, 40} and H in {21, 63, 126} — 27 cells per panel, 54 in total,
    ALL published.  COST IS NOT A DIAL THE BOOK CAN CHOOSE.  It is the execution assumption
    PROTOCOL rule 2 fixes at 10 bps; this run walks it and NOTHING is ever selected on it: every
    rung is published for every cell, the rule-8 choosers are re-run SEPARATELY at each rung
    (each chooser only ever sees the cost its own book actually pays), and the verdict is quoted
    at the harshest rung the queue asked for, not at the friendliest.

THE COST LADDER, AND WHY IT IS EXACT RATHER THAN RE-RUN
    `engine.backtest` computes  r = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4  and
    neither `held` nor `turnover` depends on cost (the selection reads prices, not the book's own
    net path).  So one run per cell yields the WHOLE cost ladder exactly: r(c) = g - tn * c/1e4.
    Gates G1b and G1c check this against `engine.backtest` at 25 and 50 bps to machine precision,
    which is what licenses the 201-rung fine ladder (0..200 bps in 1 bp steps) used to solve for
    each cell's BREAKEVEN rung c* — the largest c at which the cell still clears 4b.
    Published rungs: 0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100 bps.

DECLARED BEFORE ANY NUMBER
    (a) The queue's premise: the candidate is 2.4x as cost-exposed as the H=126 book at the same
        n, so it should die FIRST as the rung rises.  SIGNATURE: c*(N=12, H=21) < c*(N=12, H=126)
        on U56, and the IS-only choosers move to LONGER holds as cost rises.
    (b) The rival reading: at 10 bps the candidate's binding leg was DRAWDOWN (+0.753 pp of
        margin), not CAGR, and cost hits CAGR far harder than it hits |MaxDD|.  If the candidate
        dies on L_CAGR while its DD margin is untouched, the cost rung and the sample length are
        two INDEPENDENT reasons not to promote it, not one.
    (c) A third outcome named in advance so it cannot be read as either: the whole GRID may die
        at the same rung (every cell failing L_CAGR within a few bps of the others), in which
        case the rung is a statement about the FAMILY's turnover level and says nothing about
        H = 21 in particular.
    (d) BENCHMARK ASYMMETRY, stated up front (the record's open idea 1063).  PROTOCOL's 4b bar is
        SPY buy-and-hold, which pays no turnover at any rung, so raising the rung is a ONE-SIDED
        handicap.  The headline keeps PROTOCOL's convention.  A labelled post-run diagnostic
        (D3) re-reads every rung against a SPY charged the BOOK's own turnover at the same rung —
        the opposite extreme — so the true answer is bracketed rather than asserted.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here is
    optimistic, every 4b/4a count is an UPPER bound, and every breakeven rung c* is an UPPER bound
    on the cost a real book of this kind could have paid.
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
SLUG = "does-the-U56-n12-H21-CANDIDATE-survive-25-and-50-bps"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]          # CAND20, 936/1064/1071/1082/1086's construction
CAPNAME = "INF"                                 # frozen, NOT a dial

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]         # dial 1 — 1082/1086's ladder verbatim
HS = [21, 63, 126]                              # dial 2 — the min hold
CS = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 75.0, 100.0]   # execution axis
CFINE = np.arange(0.0, 200.5, 1.0)              # for the breakeven rung c*
PROTOCOL_RUNG = 10.0
NSEED_NULL = 40                                 # diagnostic null at the candidate cell only
PANELS = ["U56", "B136"]

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)                  # 936/1071/1082, N=20 H=126, 10 bps
A1086_CAND = dict(CAGR=0.1679622583830449, Sharpe=1.162499076998433,
                  MaxDD=-0.19477561065817217, OOS_CAGR=0.17568436699087275,
                  OOS_Sharpe=1.142623045544897, OOS_MaxDD=-0.19477561065817217)
A1086_TURN_H21, A1086_TURN_H126 = 7.19, 3.04                  # 1086 memo, N=12
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
    """1082/1086's recipe verbatim, so the diagnostic null draws are the SAME objects."""
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


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """Target weights under MIN HOLD H and slot count N, cap = INF.  1082/1086's build()."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb = []
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
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W, np.array(nsel_by_reb)


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


def cstar(g, tn, warm, ins, oos, sb, which="full"):
    """Largest rung (bps) on the 0..200 fine ladder at which the cell still clears 4b, plus the
    FIRST rung at which it fails and the leg that fails there.  Returns (c_star, c_first_fail,
    first_failing_legs, is_interval) — is_interval is False if the pass set is not contiguous
    from 0, which would mean 'breakeven rung' is not a well-defined object for that cell."""
    ok = []
    for c in CFINE:
        b = blocks(g - tn * c / 1e4, warm, ins, oos)
        L = legs_4b(b, sb) if which == "full" else legs_4b_oos(b, sb)
        ok.append(all(L.values()))
    ok = np.array(ok)
    if not ok[0]:
        return (np.nan, 0.0, "fails at 0 bps", True)
    run = int(np.argmin(ok)) if (~ok).any() else len(ok)   # first False
    c_s = float(CFINE[run - 1])
    c_f = float(CFINE[run]) if run < len(ok) else np.nan
    interval = bool(ok[:run].all() and not ok[run:].any())
    if run < len(ok):
        b = blocks(g - tn * CFINE[run] / 1e4, warm, ins, oos)
        L = legs_4b(b, sb) if which == "full" else legs_4b_oos(b, sb)
        bad = ",".join(k for k, v in L.items() if not v)
    else:
        bad = "none within 200 bps"
    return (c_s, c_f, bad, interval)


def main():
    t0 = time.time()
    P(f"# Idea 1094 (lane C, {DATE}) — does the U56 n=12 / H=21 CANDIDATE survive 25 and 50 bps?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): N {NS} x H {HS} = 27 cells per panel, 54 total, ALL")
    P(f"#   published.  COST is NOT a dial the book can choose: it is PROTOCOL rule 2's execution")
    P(f"#   assumption, walked over {CS} bps with NOTHING selected on it (the rule-8 choosers are")
    P(f"#   re-run separately at every rung and each sees only the cost its own book pays).")
    P(f"# FROZEN: cap {CAPNAME}, CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, LAG {LAG},")
    P(f"#   cadence {FREQ}, warm-up {WARMUP}, IS end {IS_END}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) QUEUE's premise — the candidate is 2.4x as cost-exposed as H=126 at the same n and")
    P("#       should die FIRST.  SIGNATURE: c*(12,21) < c*(12,126) and the IS choosers move to")
    P("#       LONGER holds as the rung rises.")
    P("#   (b) RIVAL — at 10 bps the binding leg was DRAWDOWN (+0.753 pp), and cost hits CAGR far")
    P("#       harder than |MaxDD|.  If it dies on L_CAGR with its DD margin intact, the rung and")
    P("#       the sample length are TWO independent reasons not to promote, not one.")
    P("#   (c) NAMED IN ADVANCE so it cannot be read as either: the whole GRID may die within a")
    P("#       few bps of itself, making the rung a FAMILY-turnover fact and not an H=21 fact.")
    P("#   (d) The 4b bar is SPY, which pays no turnover at any rung — a ONE-SIDED handicap.")
    P("#       Headline keeps PROTOCOL's convention; diagnostic D3 brackets it with the opposite")
    P("#       extreme (SPY charged the BOOK's own turnover at the same rung).")
    P("")

    rows, gaterows, picks, benchrows, cstarrows, nullrows = [], [], [], [], [], []
    gates = {}
    live_by_panel, spy_by_panel = {}, {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        K = len(px.columns)
        T = len(idx)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)
        yrs = warm.sum() / 252.0

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)          # PROTOCOL convention: SPY pays no turnover
        spy_by_panel[panel] = (spy, sb)
        live0 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        live_g = live0["returns"].values
        live_tn = live0["turnover"].values
        live_by_panel[panel] = (live_g, live_tn)
        lb10 = blocks(live_g - live_tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)

        P(f"## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates, {yrs:.2f} scored years")
        P(f"   SPY (uncharged, PROTOCOL 4b bar)  full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / "
          f"{sb['MaxDD']:.2%}  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   4b bars: DD cap {DD_CAP*abs(sb['MaxDD']):.2%} full / "
          f"{DD_CAP*abs(sb['OOS_MaxDD']):.2%} OOS;  CAGR floor {CAGR_FLOOR*sb['CAGR']:.2%} full / "
          f"{CAGR_FLOOR*sb['OOS_CAGR']:.2%} OOS")
        benchrows.append(dict(panel=panel, series="SPY", cost_bps=np.nan, turnover=0.0, **sb))
        for c in CS:
            lbc = blocks(live_g - live_tn * c / 1e4, warm, ins, oos)
            benchrows.append(dict(panel=panel, series="RULESv2", cost_bps=c,
                                  turnover=float(live_tn[warm].sum() / yrs), **lbc))
            P(f"   RULES v2 @ {c:5.1f} bps  full {lbc['CAGR']:.2%} / {lbc['Sharpe']:.4f} / "
              f"{lbc['MaxDD']:.2%}  OOS {lbc['OOS_CAGR']:.2%} / {lbc['OOS_Sharpe']:.4f} / "
              f"{lbc['OOS_MaxDD']:.2%}")

        # ---- GATES -----------------------------------------------------------------------
        if panel == "U56":
            W20, _ = build(rank_key, elig, priced, reb, 20, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            g20, t20 = nrun(rets, lagmat(W20), mkl)
            for cg, gname in ((10.0, "G1"), (25.0, "G1b"), (50.0, "G1c")):
                eng = backtest(px, wdf, cost_bps=cg, freq=FREQ)["returns"].values
                d = float(np.abs((g20 - t20 * cg / 1e4)[WARMUP:] - eng[WARMUP:]).max())
                gates[f"{gname} r(c)=g-tn*c/1e4 == engine.backtest at {cg:.0f} bps "
                      f"(U56 N=20 H=126)"] = (d, d < 1e-12)
            m = fmet((g20 - t20 * PROTOCOL_RUNG / 1e4)[warm])
            d2 = max(abs(m[0] - A936_WH126[0]), abs(m[1] - A936_WH126[1]), abs(m[2] - A936_WH126[2]))
            gates["G2 CROSS-RUN vs 936/1071/1082's committed W/H126 N=20 triple @ 10 bps"] = (
                d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d5 = abs(lb10["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G5 live RULES v2 MaxDD @ 10 bps == committed -12.05%"] = (d5, d5 < 5e-4)
            rng_a = np.random.default_rng(mdseed(panel, 12, CAPNAME, 0)).random((T, K))
            rng_b = np.random.default_rng(mdseed(panel, 12, CAPNAME, 0)).random((T, K))
            d7 = float(np.abs(rng_a - rng_b).max())
            gates["G7 the diagnostic null's seed recipe is deterministic"] = (d7, d7 == 0.0)

        # ---- the grid --------------------------------------------------------------------
        for N in NS:
            for H in HS:
                W, nsel = build(rank_key, elig, priced, reb, N, H, T, K, GROSS0)
                g, tn = nrun(rets, lagmat(W), mkl)
                turn = float(tn[warm].sum() / yrs)
                if panel == "U56" and N == 12 and H == 21:
                    b10 = blocks(g - tn * PROTOCOL_RUNG / 1e4, warm, ins, oos)
                    d4 = max(abs(b10[k] - v) for k, v in A1086_CAND.items())
                    gates["G4 CROSS-RUN 1086's committed U56 N=12 H=21 candidate "
                          "(full + OOS triples) @ 10 bps"] = (d4, d4 < 5e-4)
                    d4b = abs(turn - A1086_TURN_H21)
                    gates["G4b CROSS-RUN 1086's committed candidate turnover 7.19x/yr"] = (
                        d4b, d4b < 5e-3)
                    cand_g, cand_tn = g, tn
                if panel == "U56" and N == 12 and H == 126:
                    d4c = abs(turn - A1086_TURN_H126)
                    gates["G4c CROSS-RUN 1086's committed N=12 H=126 turnover 3.04x/yr"] = (
                        d4c, d4c < 5e-3)
                for c in CS:
                    b = blocks(g - tn * c / 1e4, warm, ins, oos)
                    lbc = blocks(live_g - live_tn * c / 1e4, warm, ins, oos)
                    l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lbc), legs_4b_oos(b, sb)
                    rows.append(dict(panel=panel, N=N, H=H, cost_bps=c, cap=CAPNAME,
                                     mean_nsel=float(nsel.mean()), turnover=turn,
                                     drag_pp=100.0 * turn * c / 1e4, **b, **l4b, **l4a, **l4bo,
                                     pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                                     pass4b_oos=all(l4bo.values()),
                                     dd_margin_pp=100.0 * (DD_CAP * abs(sb["MaxDD"]) - abs(b["MaxDD"])),
                                     cagr_margin_pp=100.0 * (b["CAGR"] - CAGR_FLOOR * sb["CAGR"])))
                cs_f = cstar(g, tn, warm, ins, oos, sb, "full")
                cs_o = cstar(g, tn, warm, ins, oos, sb, "oos")
                cstarrows.append(dict(panel=panel, N=N, H=H, turnover=turn,
                                      cstar_full_bps=cs_f[0], first_fail_full_bps=cs_f[1],
                                      failing_legs_full=cs_f[2], interval_full=cs_f[3],
                                      cstar_oos_bps=cs_o[0], first_fail_oos_bps=cs_o[1],
                                      failing_legs_oos=cs_o[2], interval_oos=cs_o[3]))
                P(f"   N={N:2d} H={H:3d}  turn {turn:5.2f}x/yr  CAGR @0/10/25/50 "
                  + " ".join(f"{fmet((g - tn*c/1e4)[warm])[0]:7.2%}" for c in (0, 10, 25, 50))
                  + f"   c*_full {cs_f[0] if cs_f[0]==cs_f[0] else float('nan'):6.1f} bps "
                    f"({cs_f[2]})  ({time.time()-t0:.0f}s)")

        # ---- RULE 8: IS-only choosers pick (N, H) jointly AT EACH RUNG, OOS read ONCE ------
        gp = pd.DataFrame([r for r in rows if r["panel"] == panel])
        for c in CS:
            gc = gp[gp.cost_bps == c]
            lbc = blocks(live_g - live_tn * c / 1e4, warm, ins, oos)
            for cname, key in [("C_ISSHARPE", "IS_Sharpe"), ("C_ISDD", "IS_MaxDD"),
                               ("C_ISCAGR", "IS_CAGR")]:
                pick = gc.sort_values(key, ascending=False).iloc[0]
                picks.append(dict(panel=panel, cost_bps=c, chooser=cname,
                                  N=int(pick["N"]), H=int(pick["H"]), turnover=pick["turnover"],
                                  IS_Sharpe=pick["IS_Sharpe"], IS_MaxDD=pick["IS_MaxDD"],
                                  IS_CAGR=pick["IS_CAGR"],
                                  OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                                  OOS_MaxDD=pick["OOS_MaxDD"], full_CAGR=pick["CAGR"],
                                  full_Sharpe=pick["Sharpe"], full_MaxDD=pick["MaxDD"],
                                  H1=pick["H1"], H2=pick["H2"],
                                  spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                                  spy_OOS_MaxDD=sb["OOS_MaxDD"],
                                  live_OOS_CAGR=lbc["OOS_CAGR"], live_OOS_Sharpe=lbc["OOS_Sharpe"],
                                  live_OOS_MaxDD=lbc["OOS_MaxDD"],
                                  O_S=bool(pick["O_S"]), O_DD=bool(pick["O_DD"]),
                                  O_CAGR=bool(pick["O_CAGR"]),
                                  pass4b_oos=bool(pick["pass4b_oos"]),
                                  pass4b_full=bool(pick["pass4b"]), pass4a=bool(pick["pass4a"])))

        # ---- diagnostic null at the candidate cell (U56 N=12 H=21) ------------------------
        if panel == "U56":
            for s in range(NSEED_NULL):
                rk = np.random.default_rng(mdseed(panel, 12, CAPNAME, s)).random((T, K))
                Wn, _ = build(rk, np.ones((T, K), dtype=bool), priced, reb, 12, 21, T, K, GROSS0)
                gn, tnn = nrun(rets, lagmat(Wn), mkl)
                cf = cstar(gn, tnn, warm, ins, oos, sb, "full")
                row = dict(seed=s, turnover=float(tnn[warm].sum() / yrs),
                           cstar_full_bps=cf[0], failing_legs_full=cf[2])
                for c in CS:
                    b = blocks(gn - tnn * c / 1e4, warm, ins, oos)
                    row[f"pass4b_{int(c)}"] = all(legs_4b(b, sb).values())
                    row[f"CAGR_{int(c)}"] = b["CAGR"]
                nullrows.append(row)

    grid = pd.DataFrame(rows)
    cst = pd.DataFrame(cstarrows)
    pk = pd.DataFrame(picks)
    bn = pd.DataFrame(benchrows)
    nl = pd.DataFrame(nullrows)

    # remaining gates
    mono = 0.0
    for (p_, N, H), s in grid.groupby(["panel", "N", "H"]):
        s = s.sort_values("cost_bps")
        mono = max(mono, float(max(0.0, np.max(np.diff(s.CAGR.values)))))
    gates["G6 CAGR is non-increasing in the cost rung at every one of the 54 cells"] = (
        mono, mono <= 0.0)
    spread = float(grid[grid.panel == "U56"].groupby(["N", "H"]).CAGR.apply(lambda x: x.max() - x.min()).max())
    gates["G8 the cost axis is LIVE (max U56 CAGR spread across rungs >= 1 pp)"] = (
        spread, spread >= 0.01)

    P("")
    P("## GATES (printed before any result number)")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: |d| = {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(ok)))

    P("")
    P("## THE CANDIDATE ITSELF — U56 N=12 H=21 at every published rung")
    cand = grid[(grid.panel == "U56") & (grid.N == 12) & (grid.H == 21)].sort_values("cost_bps")
    P("      bps   drag     CAGR    Sharpe    MaxDD      H1/H2      OOS C/S/DD"
      "              DDmarg  CAGRmarg   4b 4bOOS 4a   failing legs")
    for _, r in cand.iterrows():
        bad = ",".join(k for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not r[k]) or "-"
        P(f"    {r.cost_bps:5.1f} {r.drag_pp:5.2f}pp {r.CAGR:7.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%}  "
          f"{r.H1:.3f}/{r.H2:.3f}  {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}  "
          f"{r.dd_margin_pp:+6.3f} {r.cagr_margin_pp:+8.3f}   {int(r.pass4b)}   "
          f"{int(r.pass4b_oos)}   {int(r.pass4a)}   {bad}")
    cc = cst[(cst.panel == "U56") & (cst.N == 12) & (cst.H == 21)].iloc[0]
    P(f"    BREAKEVEN: c*_full = {cc.cstar_full_bps:.0f} bps (first failure at "
      f"{cc.first_fail_full_bps:.0f} bps on {cc.failing_legs_full}); c*_OOS = "
      f"{cc.cstar_oos_bps:.0f} bps (first failure at {cc.first_fail_oos_bps:.0f} on "
      f"{cc.failing_legs_oos}).  Pass set contiguous from 0: full {bool(cc.interval_full)}, "
      f"OOS {bool(cc.interval_oos)}.")

    P("")
    P("## THE WHOLE GRID — 4b full-sample pass (1) / fail (0) at every (N, H, rung)")
    for panel in PANELS:
        P(f"   --- {panel} ---   rows N x H, columns the cost ladder {CS} bps")
        P("       N   H   turn  " + "".join(f"{int(c):>5d}" for c in CS) + "   c*_full  c*_OOS  legs@fail")
        for N in NS:
            for H in HS:
                s = grid[(grid.panel == panel) & (grid.N == N) & (grid.H == H)].sort_values("cost_bps")
                cr = cst[(cst.panel == panel) & (cst.N == N) & (cst.H == H)].iloc[0]
                P(f"      {N:2d} {H:3d} {s.turnover.iloc[0]:6.2f}  "
                  + "".join(f"{int(v):>5d}" for v in s.pass4b.values)
                  + f"   {cr.cstar_full_bps:7.1f} {cr.cstar_oos_bps:7.1f}  {cr.failing_legs_full}")
        for c in CS:
            s = grid[(grid.panel == panel) & (grid.cost_bps == c)]
            P(f"      rung {int(c):3d} bps: 4b full {int(s.pass4b.sum())}/{len(s)}   "
              f"4b OOS {int(s.pass4b_oos.sum())}/{len(s)}   4a {int(s.pass4a.sum())}/{len(s)}")

    P("")
    P("## AT WHICH RUNG DOES THE PASS DIE? — breakeven by hold (the queue's question)")
    for panel in PANELS:
        P(f"   --- {panel} ---")
        for H in HS:
            s = cst[(cst.panel == panel) & (cst.H == H)].set_index("N").reindex(NS)
            P(f"      H={H:3d}  turnover " + "".join(f"{v:>7.2f}" for v in s.turnover.values))
            P(f"            c*_full " + "".join(
                f"{(v if v == v else -1):>7.0f}" for v in s.cstar_full_bps.values)
              + "     (-1 = fails already at 0 bps)")

    P("")
    P("## RULE 8 — IS(2009-2016)-only choosers pick (N, H) over 27 cells AT EACH RUNG,")
    P("## OOS(2017-2026) read ONCE.  Each chooser sees only the cost its own book pays.")
    for panel in PANELS:
        for c in CS:
            for _, r in pk[(pk.panel == panel) & (pk.cost_bps == c)].iterrows():
                P(f"   {panel} @{int(r.cost_bps):3d} bps {r.chooser}: picks N={int(r.N)} "
                  f"H={int(r.H)} (turn {r.turnover:.2f}x) -> OOS {r.OOS_CAGR:.2%} / "
                  f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%} | SPY OOS {r.spy_OOS_CAGR:.2%} / "
                  f"{r.spy_OOS_Sharpe:.4f} / {r.spy_OOS_MaxDD:.2%} | RULES v2 OOS "
                  f"{r.live_OOS_CAGR:.2%} / {r.live_OOS_Sharpe:.4f} / {r.live_OOS_MaxDD:.2%} | "
                  f"4b_OOS {r.pass4b_oos} (O_S {r.O_S} O_DD {r.O_DD} O_CAGR {r.O_CAGR}) "
                  f"4b_full {r.pass4b_full} 4a {r.pass4a}")

    # ---------------------------------------------------------------- hypotheses
    def cell(panel, N, H, c):
        return grid[(grid.panel == panel) & (grid.N == N) & (grid.H == H)
                    & (grid.cost_bps == c)].iloc[0]

    def cs_(panel, N, H):
        return float(cst[(cst.panel == panel) & (cst.N == N) & (cst.H == H)].cstar_full_bps.iloc[0])

    P("")
    P("## HYPOTHESES (declared before the run, scored as written)")
    H_ = []
    c25 = cell("U56", 12, 21, 25.0)
    c50 = cell("U56", 12, 21, 50.0)
    H_.append(("H_DIE25 the U56 N=12 H=21 candidate FAILS 4b full-sample at 25 bps",
               bool(not c25.pass4b),
               f"4b at 25 bps = {bool(c25.pass4b)}; CAGR {c25.CAGR:.2%}, MaxDD {c25.MaxDD:.2%}"))
    H_.append(("H_DIE50 it FAILS 4b full-sample at 50 bps", bool(not c50.pass4b),
               f"4b at 50 bps = {bool(c50.pass4b)}; CAGR {c50.CAGR:.2%}"))
    cf = cst[(cst.panel == "U56") & (cst.N == 12) & (cst.H == 21)].iloc[0]
    H_.append(("H_LEG the leg that kills the candidate as cost rises is L_CAGR (rival (b))",
               bool("L_CAGR" in str(cf.failing_legs_full)),
               f"first failing legs at {cf.first_fail_full_bps:.0f} bps: {cf.failing_legs_full}"))
    H_.append(("H_QUEUE c*(N=12, H=21) < c*(N=12, H=126) on U56 — the candidate dies FIRST, as "
               "the queue's 2.4x turnover premise predicts",
               bool(cs_("U56", 12, 21) < cs_("U56", 12, 126)),
               f"c* = {cs_('U56',12,21):.0f} vs {cs_('U56',12,126):.0f} bps"))
    H_.append(("H_MONO every cell's 4b pass set is an INTERVAL contiguous from 0 bps (so "
               "'breakeven rung' is a well-defined object)",
               bool(cst.interval_full.all()),
               f"{int(cst.interval_full.sum())} of {len(cst)} cells contiguous"))
    hold_mono = []
    for panel in PANELS:
        for ch in ("C_ISSHARPE", "C_ISDD", "C_ISCAGR"):
            hs = pk[(pk.panel == panel) & (pk.chooser == ch)].sort_values("cost_bps").H.values
            hold_mono.append(all(hs[i] <= hs[i + 1] for i in range(len(hs) - 1)))
    H_.append(("H_HOLD the IS-only choosers move to LONGER holds as the rung rises (weakly "
               "non-decreasing H in cost), every (panel, chooser)",
               bool(all(hold_mono)),
               f"{sum(hold_mono)} of {len(hold_mono)} (panel, chooser) sequences non-decreasing"))
    valid = cst.dropna(subset=["cstar_full_bps"])
    rho = float(valid.cstar_full_bps.rank().corr(valid.turnover.rank())) if len(valid) > 2 else np.nan
    H_.append(("H_CSTAR_TURN c* is NEGATIVELY rank-correlated with turnover across the cells "
               "that pass at 0 bps (cost robustness is bought with churn, and nothing else)",
               bool(rho < 0), f"Spearman(c*, turnover) = {rho:+.4f} over {len(valid)} cells"))
    H_.append(("H_WF25 at least one rule-8 pick clears 4b OUT OF SAMPLE at 25 bps",
               bool(pk[(pk.cost_bps == 25.0)].pass4b_oos.any()),
               f"{int(pk[(pk.cost_bps==25.0)].pass4b_oos.sum())} of "
               f"{len(pk[pk.cost_bps==25.0])} picks"))
    H_.append(("H_WF50 at least one rule-8 pick clears 4b OUT OF SAMPLE at 50 bps",
               bool(pk[(pk.cost_bps == 50.0)].pass4b_oos.any()),
               f"{int(pk[(pk.cost_bps==50.0)].pass4b_oos.sum())} of "
               f"{len(pk[pk.cost_bps==50.0])} picks"))
    H_.append(("H_4A no cell clears 4a at ANY rung (the DD leg is a book fact, not a cost fact)",
               bool(not grid.pass4a.any()),
               f"{int(grid.pass4a.sum())} of {len(grid)} (cell, rung) pairs pass 4a"))
    spread_cstar = float(valid.cstar_full_bps.max() - valid.cstar_full_bps.min())
    H_.append(("H_FAMILY outcome (c) — the whole grid dies within 10 bps of itself, making the "
               "rung a FAMILY fact rather than an H=21 fact",
               bool(spread_cstar <= 10.0),
               f"c* spread across passing cells = {spread_cstar:.0f} bps"))
    for name, ok, note in H_:
        P(f"   {'PASS' if ok else 'FAIL'}  {name}  [{note}]")

    # ---------------------------------------------------------------- post-run diagnostics
    P("")
    P("## POST-RUN DIAGNOSTICS — computed AFTER reading the grid and labelled as such, NOT")
    P("## pre-declared hypotheses.")
    diag = []
    P("")
    P("   (D1) WHAT THE RUNG COSTS EACH LEG.  Cost enters CAGR through the drag and |MaxDD| only")
    P("        through the compounding of that drag, so the two legs move at very different rates.")
    for panel in PANELS:
        for H in HS:
            a = grid[(grid.panel == panel) & (grid.H == H) & (grid.cost_bps == 0.0)].set_index("N")
            b = grid[(grid.panel == panel) & (grid.H == H) & (grid.cost_bps == 50.0)].set_index("N")
            dc = 100.0 * (a.CAGR - b.CAGR).mean()
            dd = 100.0 * (abs(b.MaxDD) - abs(a.MaxDD)).mean()
            P(f"        {panel} H={H:3d}: mean CAGR lost 0->50 bps {dc:+.3f} pp; mean |MaxDD| "
              f"gained {dd:+.3f} pp; ratio {dc/dd if dd else float('nan'):.2f}x")
            diag.append(dict(diag="D1_leg_rates", panel=panel, H=H, a=dc, b=dd,
                             note="mean pp of CAGR lost vs |MaxDD| gained, 0->50 bps"))
    P("")
    P("   (D2) THE DIAGNOSTIC NULL at the candidate cell (U56, N=12, H=21, 40 random-rank draws,")
    P("        1082/1086's seed recipe, gross 0.75, same hold, NO eligibility gate).  It prices")
    P("        whether the candidate's cost robustness is better than a coin flip's at the same")
    P("        construction — not whether its edge is real, which 1085/1086 already priced.")
    if len(nl):
        P(f"        null turnover median {nl.turnover.median():.2f}x/yr against the book's "
          f"{cand.turnover.iloc[0]:.2f}x/yr")
        for c in CS:
            pr = float(nl[f"pass4b_{int(c)}"].mean())
            P(f"        @{int(c):3d} bps: null 4b pass rate {pr:.3f} ({int(nl[f'pass4b_{int(c)}'].sum())}"
              f"/{len(nl)});  book {'PASS' if bool(cell('U56',12,21,c).pass4b) else 'FAIL'}")
            diag.append(dict(diag="D2_null_pass_rate", panel="U56", H=21, a=c, b=pr,
                             note="gross-matched random-rank null 4b pass rate at this rung"))
        cn = nl.cstar_full_bps.dropna()
        P(f"        null c* median {cn.median() if len(cn) else float('nan'):.0f} bps over "
          f"{len(cn)} of {len(nl)} draws that pass at 0 bps; book c* "
          f"{cf.cstar_full_bps:.0f} bps; book percentile of the null c* distribution "
          f"{float((cn < cf.cstar_full_bps).mean()) if len(cn) else float('nan'):.3f}")
        diag.append(dict(diag="D2_null_cstar", panel="U56", H=21,
                         a=float(cn.median()) if len(cn) else np.nan,
                         b=float(cf.cstar_full_bps), note="median null c* vs book c*, bps"))
    P("")
    P("   (D3) THE BENCHMARK ASYMMETRY BRACKET (declared as (d)).  PROTOCOL charges SPY nothing.")
    P("        The opposite extreme charges SPY the BOOK's own turnover at the same rung.  The")
    P("        truth is inside; the two columns are the bracket, not a new convention.")
    for panel in PANELS:
        spy, sb_ = spy_by_panel[panel]
        warmp = np.zeros(len(spy), dtype=bool)
        warmp[WARMUP:] = True
        oosp = None
        for _, r in cst[(cst.panel == panel)].iterrows():
            if not (r.N == 12 and r.H in (21, 126)):
                continue
            for c in (25.0, 50.0):
                row = cell(panel, int(r.N), int(r.H), c)
                px_ = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
                warm_, ins_, oos_ = windows(px_.index)
                sb_m = blocks(spy - r.turnover / 252.0 * c / 1e4, warm_, ins_, oos_)
                L = legs_4b(dict(row[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR",
                                      "IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                      "OOS_MaxDD"]]), sb_m)
                P(f"        {panel} N={int(r.N)} H={int(r.H)} @{int(c)} bps: PROTOCOL SPY -> 4b "
                  f"{bool(row.pass4b)};  turnover-matched SPY (CAGR {sb_m['CAGR']:.2%}, cap "
                  f"{DD_CAP*abs(sb_m['MaxDD']):.2%}) -> 4b {all(L.values())}")
                diag.append(dict(diag="D3_bracket", panel=panel, H=int(r.H), a=c,
                                 b=float(all(L.values())),
                                 note=f"N={int(r.N)}; PROTOCOL 4b {bool(row.pass4b)}"))

    P("")
    dump(grid, "grid"); dump(cst, "breakeven"); dump(pk, "rule8"); dump(bn, "benchmarks")
    dump(nl, "null"); dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame([dict(hypothesis=n, passed=bool(o), note=t) for n, o, t in H_]),
         "hypotheses")
    dump(pd.DataFrame(diag), "diagnostics")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
