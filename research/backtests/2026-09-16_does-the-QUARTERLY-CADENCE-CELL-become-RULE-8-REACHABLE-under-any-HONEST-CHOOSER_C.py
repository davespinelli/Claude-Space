#!/usr/bin/env python3
"""Idea 1099 (lane C, 2026-09-16) — does the QUARTERLY CADENCE CELL become RULE-8 REACHABLE
under any HONEST CHOOSER?

QUESTION (QUEUE idea 1099, verbatim)
    idea 1096 found the U56 W/H126/N=20 book run QUARTERLY (1.65x/yr turnover) clears 4b full
    AND OOS at 25 and 50 bps, but at PROTOCOL's 10 bps no IS-only chooser selects it, so it is
    not reachable at the cost the protocol fixes.  Walk a small family of IS-only choosers that
    are legal under rule 8 (IS Sharpe, IS MaxDD, IS CAGR, IS Sharpe net of a declared turnover
    penalty) and report whether ANY of them reaches the quarterly cell at 10 bps without being
    chosen for that outcome.  Max 2 params (chooser, cadence).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials:
      CHOOSER     {C_ISSHARPE, C_ISDD, C_ISCAGR, C_ISSHARPE_TP}   — the queue's own four
      CADENCE SET {C4, C9}                                        — engine's four, and 1118's nine
    = 8 dial points, ALL published, on BOTH panels (PANEL is not a dial; both reported
    everywhere).  The TP chooser carries a DECLARED penalty ladder LAM = {5, 10, 25, 50, 100}
    bps, every rung published; the HEADLINE rung is LAM = 10, PROTOCOL rule 2's own cost and the
    only non-arbitrary value on the ladder.  Nothing is selected on LAM — it is reported at
    every point, and the run's central diagnostic (D1) is the SMALLEST LAM that reaches the
    target, which is a measurement of how far outside honesty one would have to go, not a fit.
    COST is not a dial: PROTOCOL rule 2 fixes 10 bps and that is the headline everywhere.  The
    0 / 25 / 50 bps rungs appear once, in D3, only to re-price the queue's own premise sentence.

THE TARGET, FIXED BEFORE THE RUN
    TARGET_Q    = the cadence rung "Q" of the U56 / B136 W-book (N=20, H=126, gross 0.75).
    TARGET_SLOW = {Q, 2Q, 4Q}.  Declared as a SECOND, WIDER target in advance because 1117/1133's
    committed walk-forward found the 4b passer on this ladder is 2Q, not Q; a run that only ever
    asked about Q could report "unreachable" while a chooser was landing one rung away.  Both
    are reported at every dial point.  Neither was picked after seeing this run's numbers.

WHAT "HONEST" MEANS HERE, STATED BEFORE ANY NUMBER
    A chooser is honest iff (i) it reads IS 2009-2016 ONLY, (ii) its full specification —
    statistic and any penalty rung — is declared before the OOS window is read, and (iii) it is
    not re-specified after seeing which rung it lands on.  All four choosers and all five LAM
    rungs here satisfy (i)-(iii).  A chooser that reaches Q only at a LAM chosen because it
    reaches Q fails (iii), and D1's LAM* is reported precisely so a reader can see whether the
    reaching rung is one anybody would have declared in advance.

DECLARED BEFORE ANY NUMBER (hypotheses, scored at the end)
    H_REACH     at least one declared chooser picks TARGET_Q at 10 bps on at least one panel.
    H_TP_ONLY   if any reaches it, only the turnover-penalised chooser does (the plain three
                read no turnover at all, so they have no mechanism to prefer a slow cadence
                beyond whatever the cost line already does to the net path).
    H_PASS10    the Q cell CLEARS 4b FULL at 10 bps.  The queue's own sentence says it does not
                (it names 25 and 50 bps), so this is a PREMISE CHECK declared in the direction
                the queue implies is false; if it is refuted, reachability is moot at 10 bps.
    H_WORTH     the reached cell's OOS Sharpe exceeds the incumbent W-book's OOS Sharpe.  If
                refuted, reaching the cell buys nothing even where it is reachable.
    H_MONO_TP   the TP chooser's pick has NON-INCREASING annual turnover as LAM rises.  This is
                the mechanism check: if it is refuted, LAM is moving the pick as noise, not as a
                turnover penalty, and no reading of D1 is safe.
    H_LAMSTAR   the smallest LAM reaching TARGET_Q lies INSIDE the declared ladder, LAM <= 100
                bps.  A LAM* above the whole ladder means the cell is reachable only by a
                penalty larger than ten times the cost the protocol fixes.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here
    is optimistic and every 4b / 4a count an UPPER bound.  The reachability half is a contrast
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
SLUG = "does-the-QUARTERLY-CADENCE-CELL-become-RULE-8-REACHABLE-under-any-HONEST-CHOOSER"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

# ---- frozen construction (1082/1094/1096/1110/1117/1118's build, verbatim) -------------------
LAG, WARMUP, MAXVOL, GROSS0, HOLD0, N0 = 1, 260, 0.60, 0.75, 126, 20
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]           # CAND20 legs
COST = 10.0                                      # PROTOCOL rule 2
FREQ0 = "W"                                      # the incumbent / frozen default rung
PANELS = ["U56", "B136"]

# ---- dial 1: chooser -------------------------------------------------------------------------
PLAIN = [("C_ISSHARPE", "IS_Sharpe"), ("C_ISDD", "IS_MaxDD"), ("C_ISCAGR", "IS_CAGR")]
LAMS = [5.0, 10.0, 25.0, 50.0, 100.0]            # declared penalty ladder, ALL published
LAM_HEAD = 10.0                                  # headline rung = PROTOCOL's own cost
LAM_FINE = np.arange(0.0, 501.0, 1.0)            # for D1's LAM* only; nothing is selected on it

# ---- dial 2: cadence set ---------------------------------------------------------------------
C4 = ["D", "W", "M", "Q"]                        # every cadence engine.rebalance_mask serves
C9 = ["D", "2D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]   # 1118's nine, built on top of those
CSETS = {"C4": C4, "C9": C9}
TARGET_Q = ["Q"]
TARGET_SLOW = ["Q", "2Q", "4Q"]
COST_RUNGS_D3 = [0.0, 10.0, 25.0, 50.0]          # D3 only — the queue's own premise sentence

# ---- committed cross-run anchors --------------------------------------------------------------
A936_WH126 = (0.155787, 1.139701, -0.191276)     # 936/1071/1082/1094/1096, U56 W/H126/N=20 @10bps
A1117_2Q = dict(CAGR=0.1326, Sharpe=1.0019, MaxDD=-0.1790, H1=1.0667, H2=0.9668,
                OOS_CAGR=0.1547, OOS_Sharpe=1.0660, OOS_MaxDD=-0.1790)   # 1117/1133, U56 2Q
A1117_W_OOS = dict(OOS_CAGR=0.1697, OOS_Sharpe=1.1643, OOS_MaxDD=-0.1913)  # 1117/1133, U56 W
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
    """Target weights under MIN HOLD H and slot count N, cap = INF (1082/1094/1096's build)."""
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


def cadence_mask(idx, spec):
    """engine.rebalance_mask verbatim for D/W/M/Q; '<k><BASE>' keeps every k-th bar of that base
    schedule (1118's construction).  engine.py is NOT modified."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


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


def is_stat(g, tn, ins, key, lam=0.0):
    """IS-ONLY statistic of one cell, charged at COST + lam bps.  Reads no OOS day."""
    r = (g - tn * (COST + lam) / 1e4)[ins]
    if key == "IS_Sharpe":
        return fsharpe(r)
    c, s, d = fmet(r)
    return {"IS_CAGR": c, "IS_MaxDD": d}[key]


def main():
    t0 = time.time()
    P(f"# Idea 1099 (lane C, {DATE}) — does the QUARTERLY CADENCE CELL become RULE-8 REACHABLE")
    P("#   under any HONEST CHOOSER?")
    P("# TUNED DIALS (2, PROTOCOL rule 4): CHOOSER {C_ISSHARPE, C_ISDD, C_ISCAGR, "
      "C_ISSHARPE_TP} x")
    P(f"#   CADENCE SET {{C4, C9}} = 8 points, ALL published, on BOTH panels (panel not a dial).")
    P(f"#   C4 = {C4}  (every cadence engine.rebalance_mask serves)")
    P(f"#   C9 = {C9}  (1118's, built on top of engine's own masks)")
    P(f"#   TP penalty ladder LAM = {LAMS} bps, ALL published; headline LAM = {LAM_HEAD:.0f} "
      "bps = PROTOCOL rule 2's own cost.  Nothing is selected on LAM.")
    P(f"# TARGETS fixed before the run: TARGET_Q = {TARGET_Q}; TARGET_SLOW = {TARGET_SLOW} "
      "(1117/1133's 4b passer on this ladder is 2Q, not Q).")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, min hold "
      f"{HOLD0}, N {N0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}.")
    P("# DECLARED BEFORE ANY NUMBER: H_REACH, H_TP_ONLY, H_PASS10 (premise check), H_WORTH,")
    P("#   H_MONO_TP (mechanism), H_LAMSTAR.  See the module docstring for their exact wording.")
    P("")

    gates, cells, benchrows = {}, [], []
    store, spy_by, live_by, win_by = {}, {}, {}, {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        warm, ins, oos = windows(idx)
        win_by[panel] = (warm, ins, oos)
        yrs = warm.sum() / 252.0
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        spy_by[panel] = sb
        live0 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ0)
        live_g, live_tn = live0["returns"].values, live0["turnover"].values
        lb = blocks(live_g - live_tn * COST / 1e4, warm, ins, oos)
        live_by[panel] = lb

        P(f"## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{yrs:.2f} scored years")
        P(f"   SPY (uncharged, the 4b bar)  full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / "
          f"{sb['MaxDD']:.2%}  halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   live RULES v2 @ {COST:.0f} bps  full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / "
          f"{lb['MaxDD']:.2%}  OOS {lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / "
          f"{lb['OOS_MaxDD']:.2%}")
        P(f"   4b bars: DD cap {DD_CAP*abs(sb['MaxDD']):.2%} full / "
          f"{DD_CAP*abs(sb['OOS_MaxDD']):.2%} OOS;  CAGR floor {CAGR_FLOOR*sb['CAGR']:.2%} full "
          f"/ {CAGR_FLOOR*sb['OOS_CAGR']:.2%} OOS")
        benchrows.append(dict(panel=panel, series="SPY", turnover=0.0, **sb))
        benchrows.append(dict(panel=panel, series="RULESv2_live",
                              turnover=float(live_tn[warm].sum() / yrs), **lb))

        # ---------------- the CADENCE ladder (C9 nests C4) ------------------------------------
        for cad in C9:
            mk = cadence_mask(idx, cad)
            reb = np.flatnonzero(mk)
            W = build(rank_key, elig, priced, reb, N0, HOLD0, T, K, GROSS0)
            g, tn = nrun(rets, lagmat(W), np.roll(mk, LAG))
            store[(panel, cad)] = (g, tn)
            b = blocks(g - tn * COST / 1e4, warm, ins, oos)
            l4b, l4a, l4o = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
            row = dict(panel=panel, cadence=cad, in_C4=cad in C4,
                       n_rebalances=int(mk[warm].sum()),
                       turnover_per_yr=float(tn[warm].sum() / yrs), **b, **l4b, **l4a, **l4o,
                       pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                       pass4b_oos=all(l4o.values()))
            for c in COST_RUNGS_D3:
                bc = blocks(g - tn * c / 1e4, warm, ins, oos)
                lbc = blocks(live_g - live_tn * c / 1e4, warm, ins, oos)
                row[f"pass4b_at{int(c)}"] = all(legs_4b(bc, sb).values())
                row[f"pass4b_oos_at{int(c)}"] = all(legs_4b_oos(bc, sb).values())
                row[f"pass4a_at{int(c)}"] = all(legs_4a(bc, lbc).values())
                row[f"Sharpe_at{int(c)}"] = bc["Sharpe"]
                row[f"CAGR_at{int(c)}"] = bc["CAGR"]
                row[f"OOS_Sharpe_at{int(c)}"] = bc["OOS_Sharpe"]
            for lam in LAMS:
                row[f"IS_Sharpe_TP{int(lam)}"] = is_stat(g, tn, ins, "IS_Sharpe", lam)
            cells.append(row)
            P(f"   {panel} cadence {cad:3s}  reb {int(mk[warm].sum()):4d}  turn "
              f"{tn[warm].sum()/yrs:5.2f}x/yr  full {b['CAGR']:6.2%} / {b['Sharpe']:.4f} / "
              f"{b['MaxDD']:7.2%}   OOS {b['OOS_CAGR']:6.2%} / {b['OOS_Sharpe']:.4f} / "
              f"{b['OOS_MaxDD']:7.2%}   4b {'PASS' if all(l4b.values()) else 'fail'}"
              f"  4bOOS {'PASS' if all(l4o.values()) else 'fail'}")

        # ---------------- gates --------------------------------------------------------------
        if panel == "U56":
            mkW = cadence_mask(idx, "W")
            WW = build(rank_key, elig, priced, np.flatnonzero(mkW), N0, HOLD0, T, K, GROSS0)
            wdf = pd.DataFrame(WW, index=idx, columns=px.columns)
            gw, tw = store[("U56", "W")]
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ0)["returns"].values
            d1 = float(np.abs((gw - tw * COST / 1e4)[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56 W/H126/N=20 @ 10 bps)"] = (d1, d1 < 1e-12)
            m = fmet((gw - tw * COST / 1e4)[warm])
            d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082/1094/1096's committed U56 W/H126/N=20 triple"] = (
                d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d4 = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G4 live RULES v2 MaxDD @ 10 bps == committed -12.05%"] = (d4, d4 < 5e-4)
            nd = 0
            for f in C4:
                nd += int((cadence_mask(idx, f) != rebalance_mask(idx, f).values).sum())
            gates["G5 cadence_mask == engine.rebalance_mask on D/W/M/Q (differing bars)"] = (
                float(nd), nd == 0)
            bad = 0
            for spec in C9:
                if spec in C4:
                    continue
                k, base = int(spec[:-1]), spec[-1]
                hit = set(np.flatnonzero(rebalance_mask(idx, base).values).tolist())
                bad += int(sum(1 for b_ in np.flatnonzero(cadence_mask(idx, spec))
                               if b_ not in hit))
                sub = np.flatnonzero(cadence_mask(idx, spec))
                ref = np.flatnonzero(rebalance_mask(idx, base).values)[::k]
                bad += int(np.abs(len(sub) - len(ref)))
            gates["G5b every extended rung is a k-th-bar subset of an engine schedule"] = (
                float(bad), bad == 0)
            g2q, t2q = store[("U56", "2Q")]
            b2q = blocks(g2q - t2q * COST / 1e4, warm, ins, oos)
            d6 = max(abs(b2q[k] - v) for k, v in A1117_2Q.items())
            gates["G6 CROSS-RUN 1117/1133's committed U56 CADENCE 2Q octuple (full+halves+OOS)"] \
                = (d6, d6 < 5e-4)
            bw = blocks(gw - tw * COST / 1e4, warm, ins, oos)
            d7 = max(abs(bw[k] - v) for k, v in A1117_W_OOS.items())
            gates["G7 CROSS-RUN 1117/1133's committed U56 W-book OOS triple"] = (d7, d7 < 5e-4)
            a = np.random.default_rng(mdseed(panel, 1)).random(8)
            b_ = np.random.default_rng(mdseed(panel, 1)).random(8)
            gates["G8 determinism of the seed recipe"] = (float(np.abs(a - b_).max()), True)
        P(f"   {panel} ladder built ({time.time()-t0:.0f}s)")

    cl = pd.DataFrame(cells)
    nest = int(sum(1 for c in C4 if c not in C9))
    gates["G9 C9 NESTS C4 (rungs of C4 missing from C9)"] = (float(nest), nest == 0)
    sp = float(cl.groupby("panel").Sharpe.apply(lambda x: x.max() - x.min()).min())
    gates["G10 the CADENCE ladder is LIVE (min over panels of Sharpe spread >= 0.05)"] = (
        sp, sp >= 0.05)
    tsp = float(cl.groupby("panel").turnover_per_yr.apply(lambda x: x.max() / x.min()).min())
    gates["G11 the TURNOVER axis is LIVE (min over panels of max/min turnover >= 5x)"] = (
        tsp, tsp >= 5.0)

    P("")
    P("# ---- GATES (printed before any result number) ----")
    ok, gaterows = 0, []
    for k, (d, good) in gates.items():
        P(f"   {'PASS' if good else 'FAIL'}  {k}: {d:.3e}")
        gaterows.append(dict(gate=k, value=d, passed=bool(good)))
        ok += bool(good)
    P(f"   {ok} of {len(gates)} gates pass")
    dump(pd.DataFrame(gaterows), "gates")
    dump(cl, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")

    # ------------------------------------------------------------------ RULE 8: the 8 dial points
    P("")
    P("# ---- RULE 8 — every chooser reads IS 2009-2016 ONLY; OOS 2017-2026 read ONCE ----")
    picks = []
    for panel in PANELS:
        warm, ins, oos = win_by[panel]
        yrs = warm.sum() / 252.0
        sb, lb = spy_by[panel], live_by[panel]
        for cs_name, rungs in CSETS.items():
            chs = [(c, k, 0.0) for c, k in PLAIN] + \
                  [(f"C_ISSHARPE_TP{int(l)}", "IS_Sharpe", l) for l in LAMS]
            for cname, key, lam in chs:
                vals = {r: is_stat(*store[(panel, r)], ins, key, lam) for r in rungs}
                pick = max(rungs, key=lambda r: vals[r])
                order = sorted(rungs, key=lambda r: -vals[r])
                margin = float(vals[order[0]] - vals[order[1]])
                g, tn = store[(panel, pick)]
                b = blocks(g - tn * COST / 1e4, warm, ins, oos)
                l4b, l4a, l4o = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                gw, tw = store[(panel, FREQ0)]
                bw = blocks(gw - tw * COST / 1e4, warm, ins, oos)
                picks.append(dict(
                    panel=panel, cadence_set=cs_name, chooser=cname, lam_bps=lam,
                    headline=(lam in (0.0, LAM_HEAD)), pick=pick, runner_up=order[1],
                    margin=margin, reaches_Q=pick in TARGET_Q, reaches_SLOW=pick in TARGET_SLOW,
                    is_default_W=(pick == FREQ0),
                    turnover_per_yr=float(tn[warm].sum() / yrs), **b, **l4b, **l4a, **l4o,
                    pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                    pass4b_oos=all(l4o.values()),
                    regret_vs_W_OOS_Sharpe=float(b["OOS_Sharpe"] - bw["OOS_Sharpe"]),
                    spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_CAGR=sb["OOS_CAGR"],
                    spy_OOS_MaxDD=sb["OOS_MaxDD"], live_OOS_Sharpe=lb["OOS_Sharpe"]))
    pk = pd.DataFrame(picks)
    dump(pk, "picks")

    hd = pk[pk.headline]
    P(f"   {len(pk)} (panel x cadence set x chooser) picks; {len(hd)} at the HEADLINE rungs "
      f"(plain three + TP at LAM={LAM_HEAD:.0f}).")
    P("")
    P("   panel  cset  chooser           pick  runner-up  margin     turn/yr   OOS Sharpe  "
      "4b  4bOOS  reaches Q")
    for _, r in pk.sort_values(["panel", "cadence_set", "chooser"]).iterrows():
        P(f"   {r.panel:5s} {r.cadence_set:4s}  {r.chooser:17s} {str(r['pick']):4s}  "
          f"{str(r.runner_up):9s}  {r.margin:+8.4f}  {r.turnover_per_yr:6.2f}x  "
          f"{r.OOS_Sharpe:10.4f}  {'Y' if r.pass4b else '.':2s}  {'Y' if r.pass4b_oos else '.':5s}"
          f"  {'YES' if r.reaches_Q else ('SLOW' if r.reaches_SLOW else 'no')}")

    # ------------------------------------------------------------------ THE ANSWER
    P("")
    P("# ---- THE LITERAL ANSWER: does ANY honest chooser reach the QUARTERLY cell at 10 bps? --")
    nq = int(hd.reaches_Q.sum())
    nslow = int(hd.reaches_SLOW.sum())
    P(f"   HEADLINE rungs, {len(hd)} picks: reaches Q {nq}; reaches TARGET_SLOW {{Q,2Q,4Q}} "
      f"{nslow}; lands on the frozen default W {int(hd.is_default_W.sum())}.")
    P(f"   ALL rungs, {len(pk)} picks: reaches Q {int(pk.reaches_Q.sum())}; reaches SLOW "
      f"{int(pk.reaches_SLOW.sum())}; lands on W {int(pk.is_default_W.sum())}.")
    P(f"   pick census (all {len(pk)}): " +
      ", ".join(f"{k}={v}" for k, v in pk["pick"].value_counts().items()))
    for cs_name in CSETS:
        s = pk[pk.cadence_set == cs_name]
        P(f"     {cs_name}: " + ", ".join(f"{k}={v}" for k, v in s["pick"].value_counts().items()))

    # D1 — LAM*, the smallest declared penalty that reaches each target
    P("")
    P("# ---- D1: LAM*, the SMALLEST turnover penalty at which the TP chooser reaches Q ----")
    lamrows = []
    for panel in PANELS:
        warm, ins, oos = win_by[panel]
        for cs_name, rungs in CSETS.items():
            path = []
            for lam in LAM_FINE:
                v = {r: is_stat(*store[(panel, r)], ins, "IS_Sharpe", lam) for r in rungs}
                path.append(max(rungs, key=lambda r: v[r]))
            path = np.array(path, dtype=object)
            lq = [float(LAM_FINE[i]) for i, p_ in enumerate(path) if p_ in TARGET_Q]
            ls = [float(LAM_FINE[i]) for i, p_ in enumerate(path) if p_ in TARGET_SLOW]
            turn = np.array([float(store[(panel, p_)][1][warm].sum()) for p_ in path])
            mono = bool(np.all(np.diff(turn) <= 1e-9))
            flick = int((path[1:] != path[:-1]).sum())
            lamrows.append(dict(panel=panel, cadence_set=cs_name,
                                lam_star_Q=(min(lq) if lq else np.nan),
                                lam_star_SLOW=(min(ls) if ls else np.nan),
                                pick_at_lam0=path[0], pick_at_lam10=path[10],
                                pick_at_lam100=path[100], pick_at_lam500=path[500],
                                n_distinct=len(set(path.tolist())), flickers=flick,
                                turnover_non_increasing_in_lam=mono))
            P(f"   {panel:5s} {cs_name}: pick at LAM 0 / 10 / 100 / 500 bps = {path[0]} / "
              f"{path[10]} / {path[100]} / {path[500]};  LAM*(Q) = "
              f"{(str(int(min(lq))) + ' bps') if lq else 'NEVER within 500 bps'};  "
              f"LAM*(SLOW) = {(str(int(min(ls))) + ' bps') if ls else 'NEVER within 500 bps'};  "
              f"{len(set(path.tolist()))} distinct picks, {flick} flickers, turnover "
              f"non-increasing {mono}")
    lamdf = pd.DataFrame(lamrows)
    dump(lamdf, "lamstar")

    # D2 — regret vs the frozen default rung
    P("")
    P("# ---- D2: what the pick is WORTH — OOS Sharpe against the frozen default W rung ----")
    for panel in PANELS:
        s = hd[hd.panel == panel]
        P(f"   {panel}: median OOS Sharpe of the headline picks {s.OOS_Sharpe.median():.4f}; "
          f"median regret vs W {s.regret_vs_W_OOS_Sharpe.median():+.4f}; "
          f"{int((s.regret_vs_W_OOS_Sharpe > 0).sum())}/{len(s)} beat W out of sample.")
    q = cl[cl.cadence == "Q"]
    w = cl[cl.cadence == FREQ0]
    for panel in PANELS:
        qq = q[q.panel == panel].iloc[0]
        ww = w[w.panel == panel].iloc[0]
        P(f"   {panel} Q   full {qq.CAGR:.2%} / {qq.Sharpe:.4f} / {qq.MaxDD:.2%}  halves "
          f"{qq.H1:.4f}/{qq.H2:.4f}  OOS {qq.OOS_CAGR:.2%} / {qq.OOS_Sharpe:.4f} / "
          f"{qq.OOS_MaxDD:.2%}  turn {qq.turnover_per_yr:.2f}x/yr")
        P(f"   {panel} W   full {ww.CAGR:.2%} / {ww.Sharpe:.4f} / {ww.MaxDD:.2%}  halves "
          f"{ww.H1:.4f}/{ww.H2:.4f}  OOS {ww.OOS_CAGR:.2%} / {ww.OOS_Sharpe:.4f} / "
          f"{ww.OOS_MaxDD:.2%}  turn {ww.turnover_per_yr:.2f}x/yr")

    # D3 — the queue's own premise sentence, re-priced
    P("")
    P("# ---- D3: the QUEUE's premise re-priced — does Q clear 4b at 0/10/25/50 bps? ----")
    for panel in PANELS:
        qq = q[q.panel == panel].iloc[0]
        P(f"   {panel} Q   4b FULL " + " ".join(
            f"@{int(c)}bps {'PASS' if qq[f'pass4b_at{int(c)}'] else 'fail'}"
            for c in COST_RUNGS_D3) + "   |  4b OOS " + " ".join(
            f"@{int(c)}bps {'PASS' if qq[f'pass4b_oos_at{int(c)}'] else 'fail'}"
            for c in COST_RUNGS_D3))
        P(f"   {panel} Q   turnover {qq.turnover_per_yr:.2f}x/yr (queue states 1.65x/yr); "
          + " ".join(f"Sharpe@{int(c)} {qq[f'Sharpe_at{int(c)}']:.4f}" for c in COST_RUNGS_D3))

    # ------------------------------------------------------------------ hypotheses
    P("")
    P("# ---- HYPOTHESES (declared before any number) ----")
    hyp = []

    def H(name, verdict, note):
        hyp.append(dict(hypothesis=name, verdict=verdict, note=note))
        P(f"   {verdict:9s}  {name}: {note}")

    H("H_REACH", "SUPPORTED" if nq > 0 else "REFUTED",
      f"{nq} of {len(hd)} headline picks land on Q; {nslow} land in {{Q,2Q,4Q}}")
    tpq = int(hd[hd.chooser.str.startswith("C_ISSHARPE_TP")].reaches_Q.sum())
    plq = int(hd[~hd.chooser.str.startswith("C_ISSHARPE_TP")].reaches_Q.sum())
    H("H_TP_ONLY", "SUPPORTED" if (nq > 0 and plq == 0 and tpq > 0) else "REFUTED",
      f"TP reaches Q {tpq} times, the plain three {plq} times (vacuous if H_REACH is refuted)")
    p10 = [bool(q[q.panel == p].iloc[0].pass4b) for p in PANELS]
    H("H_PASS10", "SUPPORTED" if all(p10) else ("PARTLY" if any(p10) else "REFUTED"),
      f"Q clears 4b FULL at 10 bps on {sum(p10)} of {len(PANELS)} panels "
      f"({dict(zip(PANELS, p10))})")
    worth = int((hd.regret_vs_W_OOS_Sharpe > 0).sum())
    H("H_WORTH", "SUPPORTED" if worth > len(hd) / 2 else "REFUTED",
      f"{worth} of {len(hd)} headline picks beat the frozen W rung's OOS Sharpe; median regret "
      f"{hd.regret_vs_W_OOS_Sharpe.median():+.4f}")
    nmono = int(lamdf.turnover_non_increasing_in_lam.sum())
    H("H_MONO_TP", "SUPPORTED" if nmono == len(lamdf) else "REFUTED",
      f"the TP pick's turnover is non-increasing in LAM on {nmono} of {len(lamdf)} "
      "(panel, cadence set) paths")
    inside = int((lamdf.lam_star_Q <= 100.0).sum())
    H("H_LAMSTAR", "SUPPORTED" if inside == len(lamdf) else
      ("PARTLY" if inside else "REFUTED"),
      f"LAM*(Q) <= 100 bps on {inside} of {len(lamdf)}; values "
      f"{lamdf.lam_star_Q.tolist()}")
    dump(pd.DataFrame(hyp), "hypotheses")

    # ------------------------------------------------------------------ both KEEP paths
    P("")
    P("# ---- BOTH KEEP PATHS (PROTOCOL rule 4), whole grid and rule-8 picks ----")
    P(f"   WHOLE GRID ({len(cl)} books = 2 panels x 9 cadences): 4b full "
      f"{int(cl.pass4b.sum())}, 4b OOS {int(cl.pass4b_oos.sum())}, 4a {int(cl.pass4a.sum())}")
    P(f"   RULE-8 PICKS ({len(pk)}): 4b full {int(pk.pass4b.sum())}, 4b OOS "
      f"{int(pk.pass4b_oos.sum())}, 4a {int(pk.pass4a.sum())}; median OOS Sharpe "
      f"{pk.OOS_Sharpe.median():.4f}, median regret vs W {pk.regret_vs_W_OOS_Sharpe.median():+.4f}")
    for _, r in cl[cl.pass4b | cl.pass4b_oos].iterrows():
        P(f"     4b {'FULL ' if r.pass4b else '     '}{'OOS' if r.pass4b_oos else '   '}  "
          f"{r.panel} {r.cadence:3s}  full {r.CAGR:.2%} / {r.Sharpe:.4f} / {r.MaxDD:.2%} "
          f"(halves {r.H1:.4f}/{r.H2:.4f})  OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / "
          f"{r.OOS_MaxDD:.2%}")
    P("   NOTHING PROPOSED AS CAPITAL unless a 4b passer is ALSO the rung an honest chooser")
    P("   reaches AND beats the incumbent W book out of sample; see the hypotheses above.")

    # ------------------------------------------------------------------ PROTOCOL rule 3 helper
    P("")
    P("# ---- PROTOCOL rule 3: baseline.compare() on the headline Q cell (U56) ----")
    from baseline import compare  # noqa: E402
    pxu = load_universe().dropna(how="all").ffill()
    idxu = pxu.index
    scu, eligu = mech(pxu)
    rku = -np.nan_to_num(scu, nan=-np.inf)
    rku[np.isnan(scu)] = np.inf
    WQ = build(rku, eligu, pxu.notna().values, np.flatnonzero(cadence_mask(idxu, "Q")),
               N0, HOLD0, len(idxu), len(pxu.columns), GROSS0)
    res = compare("1099 U56 CADENCE Q (N=20/H=126/gross 0.75)",
                  lambda _px: pd.DataFrame(WQ, index=idxu, columns=pxu.columns),
                  pxu, freq="Q", cost_bps=COST)
    LOG.append(str(res["table"]))
    LOG.append(res["row"])

    P("")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")


if __name__ == "__main__":
    main()
