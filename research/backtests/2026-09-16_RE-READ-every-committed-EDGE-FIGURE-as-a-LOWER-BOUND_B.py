#!/usr/bin/env python3
"""Idea 1097 (lane B, 2026-09-16) — RE-READ every committed EDGE FIGURE as a LOWER BOUND.

QUESTION (QUEUE idea 1097, verbatim)
    idea 1085 showed the record's gate-free null is the HARDER comparand, so 1071's +5.07,
    1082's nine-rung ladder and 1086's whole (n, H) panel all UNDER-state rank skill by
    0.03-2.47 pp depending on the rung.  Harvest every committed EDGE figure, re-price it
    against the ELIG null at its own cell, and report how many published readings change sign,
    rank or verdict.  Max 2 params (claim set, null gate).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. CLAIM SET in {STRICT, WIDE}.
         STRICT  a committed EDGE figure that is (i) a book-minus-null CAGR advantage and
                 (ii) machine-readable in a committed CSV with a FULLY DETERMINED cell
                 (panel, N, H, cap, cadence, gross, cost, seeds, DD-match convention), so it
                 can be rebuilt byte-for-byte and re-priced.  This is the arm every number
                 below is read off.
         WIDE    STRICT plus every committed PROSE unit (LEADERBOARD row / CHANGELOG or
                 result.md paragraph / QUEUE line) carrying an `edge` token, a figure in pp AND
                 a null token.  The WIDE arm's deliverable is a CENSUS — how many of the
                 record's "edge" claims are re-priceable at all — not a second set of prices.
    2. NULL GATE in {OPEN, ELIG}.
         OPEN    random ranks, elig = ALL PRICED.  1071's / 1082's / 1086's convention, i.e.
                 the convention every committed EDGE figure in the record was measured under.
                 Reproduced under each committing run's EXACT seed recipe so it must agree to
                 machine precision (gates G5/G6/G7); it is the CONTROL, not a new measurement.
         ELIG    random ranks, elig = the BOOK'S OWN gate (px > 200d MA AND 20d annualised vol
                 < 0.60).  The null gets the gate for free and differs from the book only in
                 how it ORDERS the survivors.  This is 1085's rank-matched null.

    The CELL COORDINATES ARE NOT DIALS.  (panel, N, H, cap, seeds, convention) are taken
    EXACTLY as the record committed them — this run tunes nothing over them, walks no new rung,
    and publishes all 94 committed figures.  Everything else is frozen at 936/1071/1082/1085/
    1086's construction: CAND20 legs [(21,252),(0,126),(0,63)], max_vol 0.60, gross 0.75,
    W cadence, 10 bps, LAG 1.

THE HARVEST, fixed before any number
    FAMILY A (ideas 1082 / 1085 / 1086, cap INF, min hold H in {21,63,126}, 40 seeds, REBUILT
        DD-match): 2 panels x 9 N x 3 H = 54 committed EDGE figures.  1085 re-priced the
        H=126 SLICE ONLY (18 of them); the 36 at H = 21 and 63 have NEVER been scored against
        the ELIG null.
    FAMILY B (idea 1071, H=126, cap in {1.00,1.25,1.50,2.00,INF}, 20 seeds, CASH DD-match):
        2 panels x 4 N x 5 caps = 40 committed EDGE figures.  NONE has been scored against the
        ELIG null, and the cap dial has never been crossed with the null gate at all.
    94 committed figures, 188 prices (each at both gates).  The 18 overlapping (panel, N,
    H=126, cap INF) cells appear in BOTH families because the record committed them twice under
    DIFFERENT conventions and seed counts; both are re-priced and neither is dropped.

WHAT "CHANGES" MEANS, fixed before any number
    SIGN     sign(EDGE_OPEN) != sign(EDGE_ELIG) at the same cell.
    RANK     the argmax of a committed LADDER (a maximal set of cells the record published
             together varying exactly one coordinate) moves between the two gates.
    VERDICT  the decisiveness call flips, where DECISIVE means |EDGE| > 2 * the seed SE of the
             null median at that cell (SE = 1.2533 * s / sqrt(m), the large-sample SE of a
             median).  This is the bar 1082 and 1085 both argued their headlines against.

DECLARED BEFORE ANY NUMBER — what would vindicate 1097's premise and what would refute it
    H_LOWER      GATE = EDGE_OPEN - EDGE_ELIG <= 0 at EVERY committed cell, i.e. every committed
                 EDGE figure really is a LOWER bound.  1085 found 17 of 18 at H=126; the 76 new
                 cells are the test.  REFUTED by a material count of positive GATE.
    H_MAGNITUDE  |GATE| stays inside 1085's committed 0.03-2.47 pp envelope, which the queue
                 text quotes as if it were a record-wide fact.  REFUTED by any cell outside it.
    H_SIGN       no committed EDGE figure changes SIGN.
    H_RANK       no committed LADDER changes its argmax.  This is EXPECTED TO FAIL at least
                 once and is declared anyway: 1085 already published that the U56 H=126 argmax
                 moves 12 -> 5 under ELIG.  The question 1097 adds is how many OTHER ladders do.
    H_VERDICT    no committed cell changes its decisiveness call.
    H_CONV       the two DD-match conventions (CASH, REBUILT) do not change the SIGN of GATE at
                 any of the 18 doubly-committed cells.  If they do, "lower bound" is a
                 convention statement, not a tape statement.

    EDGE IS NOT A KEEP PATH, AND THE RE-READ CANNOT MOVE ONE.  The BOOK at every cell is
    byte-identical across the two gates — only the COMPARAND changes — so 4a and 4b are
    mathematically invariant to this run's dial 2.  Both paths are scored at all 94 cells
    anyway because rule 4 requires it on every run, and the rule-8 walk-forward is run on the
    cells as the record committed them.  If the re-read raises every EDGE and 4b stays shut,
    the honest reading is that the record has been understating a real edge that is still not
    capital.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here
    is optimistic and every 4a/4b count is an UPPER bound.  EDGE_OPEN, EDGE_ELIG and GATE are
    within-pool contrasts over the same tape and the bias very largely cancels out of them; it
    does NOT cancel out of the 4b legs, which are measured against SPY, a real index.
"""
from __future__ import annotations

import hashlib
import re
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
SLUG = "RE-READ-every-committed-EDGE-FIGURE-as-a-LOWER-BOUND"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136"]
GATESET = ["OPEN", "ELIG"]                          # dial 2
CLAIMSETS = ["STRICT", "WIDE"]                      # dial 1

# FAMILY A — 1082 / 1085 / 1086's committed coordinates (cap INF, REBUILT match, 40 seeds)
A_NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]
A_HS = [21, 63, 126]
A_SEEDS = 40
A_BISECT = 34
# FAMILY B — 1071's committed coordinates (H=126, CASH match, 20 seeds, 60 bisection steps)
B_NS = [20, 25, 30, 40]
B_CAPS = [1.00, 1.25, 1.50, 2.00, np.inf]
B_HOLD = 126
B_SEEDS = 20
B_BISECT = 60

DECISIVE_K = 2.0                                    # |EDGE| > K * SE(median) = "decisive"

# committed cross-run anchors
A936_WH126 = (0.155787, 1.139701, -0.191276)        # 936 / 1071 / 1082 W/H126/N=20/cap INF
SPY_OOS_COMMITTED = {"U56": (0.1521, 0.8713, -0.3372),      # 1082/1083/1085/1086's committed
                     "B136": (0.1533, 0.8767, -0.3372)}     # triples, one per panel
LIVE_MAXDD_COMMITTED = {"U56": -0.1205, "B136": -0.1224}
SRC_1086 = ROOT / "research" / "backtests" / "2026-09-16_is-the-EDGE-HUMP-a-MIN-HOLD-artefact_cloud.grid.csv"
SRC_1085 = (ROOT / "research" / "backtests"
            / "2026-09-16_does-the-EDGE-PEAK-SURVIVE-a-RANK-MATCHED-null-instead-of-a-UNIFORM-one_B.grid.csv")
SRC_1082 = (ROOT / "research" / "backtests"
            / "2026-09-16_does-the-SELECTION-EDGE-COLLAPSE-in-n-price-the-INCUMBENT-n=20-or-just-EXPOSE-it_B.grid.csv")
SRC_1071 = (ROOT / "research" / "backtests"
            / "2026-09-16_does-the-0.97pp-DRAWDOWN-MISS-close-under-a-NAME-CAP-instead-of-a-GROSS-CUT_cloud.null.csv")

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
    """Gross portfolio returns and turnover; cost applied by the caller.  Construction copied
    verbatim from 936/1071/1082/1085/1086 so the runs are comparable."""
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


def gross_rescaler(rets, wt, mk):
    """f(lam) -> NET returns of the book REBUILT at gross lam * (this book's gross).  The target
    weight is linear in gross (with or without a finite per-name cap, since the cap is itself a
    multiple of gross/N), so a rebuild at lam*g has weights exactly lam*wt.  The PATH is NOT lam
    times this one: the cash sleeve does not scale.  f(1.0) is gated against nrun() exactly."""
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])
    AR = (A * rets).sum(axis=1)
    S = A.sum(axis=1)
    Wsum = wt[s0].sum(axis=1)
    s0p = reb[np.maximum(seg - 1, 0)]
    Ap = (wt[s0p] * (Cp / Cp[s0p]))[reb]
    Sp = Ap.sum(axis=1)
    Wsp = wt[s0p].sum(axis=1)[reb]
    Ap[0] = 0.0
    Sp[0] = 0.0
    Wsp[0] = 0.0
    Wr = wt[reb]
    c = COST / 1e4

    def f(lam):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp = 1.0 + lam * (Sp - Wsp)
        tr = lam * np.abs(Wr - Ap / Vp[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        return out

    return f


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
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, cap, H, T, K, gross):
    """Target weights under MIN HOLD H, slot count N and per-name cap multiple `cap`:
    w_i = min(gross/n_sel, cap*gross/N), residual -> CASH.  cap = inf reproduces 1082/1085/
    1086's build(); finite cap reproduces 1071's."""
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
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            w = min(gross / len(sel), per_cap)
            W[t:stop, sel] = w
            gross_by_reb.append(w * len(sel))
        else:
            gross_by_reb.append(0.0)
    return W, np.array(nsel_by_reb), np.array(gross_by_reb)


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


def lam_cash(r, target_dd, it):
    """1071's convention: lambda in (0,1] with |MaxDD(lambda*r)| = |target_dd|; None if drier."""
    if abs(maxdd(r)) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(it):
        m = 0.5 * (a + b)
        if abs(maxdd(m * r)) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def lam_rebuilt(f, sl, target_dd, it):
    """1082/1085/1086's convention: the null book REBUILT at gross lam*g."""
    if abs(maxdd(f(1.0)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(it):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def se_median(x):
    """Large-sample SE of a median, in pp."""
    x = np.asarray(x, float)
    return 100.0 * 1.2533 * x.std(ddof=1) / np.sqrt(len(x))


# ------------------------------------------------------------------ WIDE arm: the prose census
TOK_EDGE = re.compile(r"\bEDGE\b|\bedge\b")
TOK_PP = re.compile(r"[-+]?\d+\.\d+\s*pp")
TOK_NULL = re.compile(r"\bnulls?\b|\bNULLS?\b|DD-match|DD match|gross-matched|"
                      r"\bchance\b|\brandom(?:ly)?\b|\bcomparand\b")
TOK_CELL = re.compile(r"\bn\s*=\s*\d+|\bN\s*=\s*\d+|\bH\s*=?\s*\d+|min hold|cap\b|U56|B136")


def prose_census():
    """Every committed unit in the record, classified.  LEADERBOARD and QUEUE by LINE (their
    committed unit is a row/line); CHANGELOG and result.md by PARAGRAPH."""
    units = []
    for p in [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "QUEUE.md"]:
        for ln in p.read_text(errors="ignore").split("\n"):
            if ln.strip():
                units.append((p.name, "LINE", ln))
    srcs = [ROOT / "research" / "CHANGELOG.md"] + sorted((ROOT / "research" / "backtests").glob("*.result.md"))
    for p in srcs:
        for para in p.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                units.append((p.name, "PARA", para))
    rows = []
    for src, kind, u in units:
        if not TOK_EDGE.search(u):
            continue
        rows.append(dict(source=src, unit_kind=kind,
                         has_numeral=bool(re.search(r"\d", u)),
                         has_pp_figure=bool(TOK_PP.search(u)),
                         has_null_token=bool(TOK_NULL.search(u)),
                         has_cell_key=bool(TOK_CELL.search(u)),
                         n_pp_figures=len(TOK_PP.findall(u)),
                         excerpt=u[:300].replace("\n", " ")))
    return len(units), pd.DataFrame(rows)


def main():
    t0 = time.time()
    P(f"# Idea 1097 (lane B, {DATE}) — RE-READ every committed EDGE FIGURE as a LOWER BOUND")
    P(f"# 2 tuned dials: CLAIM SET {CLAIMSETS} x NULL GATE {GATESET}.  The CELL COORDINATES")
    P("#   (panel, N, H, cap, seeds, DD-match convention) are NOT dials — they are taken exactly")
    P("#   as the record committed them.  94 committed figures, 188 prices, ALL published.")
    P(f"# FROZEN: CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, cost {COST:.0f} bps, "
      f"LAG {LAG}, cadence {FREQ}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_LOWER     GATE = EDGE_OPEN - EDGE_ELIG <= 0 at EVERY committed cell (1085 found")
    P("#               17/18 at H=126; the 76 cells at H=21/63 and on the cap ladder are new).")
    P("#   H_MAGNITUDE |GATE| inside 1085's committed 0.03-2.47 pp envelope, which 1097's own")
    P("#               queue text quotes as if it were record-wide.")
    P("#   H_SIGN / H_RANK / H_VERDICT  no committed figure changes sign; no committed LADDER")
    P("#               changes argmax; no cell changes its |EDGE| > 2 SE decisiveness call.")
    P("#               H_RANK IS EXPECTED TO FAIL at least once — 1085 already published that")
    P("#               the U56 H=126 argmax moves 12 -> 5.  Declared anyway.")
    P("#   H_CONV      the CASH and REBUILT DD-match conventions agree on the SIGN of GATE at")
    P("#               the 18 doubly-committed cells.")
    P("#   EDGE IS NOT A KEEP PATH and this run's dial 2 CANNOT move one: the book is identical")
    P("#   across gates, only the comparand changes.  4a/4b scored at all 94 cells regardless.")
    P("")

    # ---------------------------------------------------------------- WIDE arm (dial 1) --------
    n_units, cen = prose_census()
    P(f"## CLAIM SET census — corpus {n_units:,} committed units")
    P(f"   units carrying an `edge` token .................. {len(cen):,}")
    for col, lab in [("has_numeral", "+ any numeral"), ("has_pp_figure", "+ a figure in pp"),
                     ("has_null_token", "+ a null/comparand token"),
                     ("has_cell_key", "+ any cell key (n=, H, cap, U56, B136)")]:
        P(f"   {lab:<48s} {int(cen[col].sum()):,}")
    wide = cen[cen.has_pp_figure & cen.has_null_token]
    wide_cell = wide[wide.has_cell_key]
    P(f"   WIDE  = pp figure AND null token ............... {len(wide):,}")
    P(f"   of which also carrying a cell key ............. {len(wide_cell):,}")
    P("   by source: " + ", ".join(f"{k} {v}" for k, v in wide.source.value_counts().head(8).items()))
    dump(cen, "census")

    # ---------------------------------------------------------------- the harvest --------------
    harvest = []
    g1086 = pd.read_csv(SRC_1086)
    g1085 = pd.read_csv(SRC_1085)
    g1082 = pd.read_csv(SRC_1082)
    # 1071's `cap` is a STRING KEY ("INF", "1.00", ...) that enters its md5 seed recipe verbatim.
    # Reading it as a float and re-formatting it would silently draw DIFFERENT nulls, so the
    # column is read as text and never converted.
    n1071 = pd.read_csv(SRC_1071, dtype={"cap": str})
    for _, r in g1086.iterrows():
        harvest.append(dict(family="A", committer="1086", panel=r["panel"], N=int(r["N"]),
                            H=int(r["H"]), cap="INF", seeds=A_SEEDS, convention="REBUILT",
                            committed_EDGE_pp=float(r["EDGE_pp"])))
    for _, r in n1071.iterrows():
        harvest.append(dict(family="B", committer="1071", panel=r["panel"], N=int(r["N"]),
                            H=B_HOLD, cap=str(r["cap"]), seeds=B_SEEDS, convention="CASH",
                            committed_EDGE_pp=100.0 * (float(r["book_CAGR"])
                                                       - float(r["null_ddmatched_CAGR_median"]))))
    H = pd.DataFrame(harvest)
    P(f"\n## HARVEST (STRICT): {len(H)} committed EDGE figures with a fully determined cell")
    P(f"   FAMILY A (1082/1085/1086): {int((H.family == 'A').sum())} "
      f"(2 panels x {len(A_NS)} N x {len(A_HS)} H, cap INF, {A_SEEDS} seeds, REBUILT)")
    P(f"   FAMILY B (1071):           {int((H.family == 'B').sum())} "
      f"(2 panels x {len(B_NS)} N x {len(B_CAPS)} caps, H={B_HOLD}, {B_SEEDS} seeds, CASH)")
    P(f"   of these, scored against the ELIG null by the record so far: {len(g1085)} "
      f"(1085, H=126, cap INF, FAMILY A only) -> {len(H) - len(g1085)} NEVER re-priced")

    rows, gaterows, benchrows = [], [], []
    gates = {}

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
        sc, elig_real = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)
        ALLP = np.ones((T, K), dtype=bool)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        P(f"\n## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates")
        P(f"   SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2   full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  "
          f"halves {lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb), dict(panel=panel, series="RULESv2", **lb)]

        # ---- GATES printed before any result number -------------------------------------
        if panel == "U56":
            W20, _, _ = build(rank_key, elig_real, priced, reb, 20, np.inf, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            gg, tn = nrun(rets, lagmat(W20), mkl)
            fast = gg - tn * COST / 1e4
            d = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N=20, H=126, cap INF)"] = (d, d < 1e-12)
            f20 = gross_rescaler(rets, lagmat(W20), mkl)
            d = float(np.abs(f20(1.0) - fast).max())
            gates["G1b gross_rescaler(1.0) == nrun (bisection kernel is the same book)"] = (d, d < 1e-14)
            Wc, _, _ = build(rank_key, elig_real, priced, reb, 20, 2.00, 126, T, K, GROSS0)
            wdfc = pd.DataFrame(Wc, index=idx, columns=px.columns)
            engc = backtest(px, wdfc, cost_bps=COST, freq=FREQ)["returns"].values
            ggc, tnc = nrun(rets, lagmat(Wc), mkl)
            d = float(np.abs((ggc - tnc * COST / 1e4)[WARMUP:] - engc[WARMUP:]).max())
            gates["G1c capped build == engine.backtest (U56, N=20, cap 2.00) — 1071's arm"] = (d, d < 1e-12)
            m = fmet(fast[warm])
            d = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082 committed W/H126 N=20 triple"] = (d, d < 5e-3)
        sc_ = SPY_OOS_COMMITTED[panel]
        d = max(abs(sb["OOS_CAGR"] - sc_[0]), abs(sb["OOS_Sharpe"] - sc_[1]),
                abs(sb["OOS_MaxDD"] - sc_[2]))
        gates[f"G3 CROSS-RUN SPY OOS triple ({panel})"] = (d, d < 5e-4)
        d = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED[panel])
        gates[f"G4 live RULES v2 MaxDD == committed ({panel})"] = (d, d < 5e-4)

        # ---- the re-pricing --------------------------------------------------------------
        sub = H[H.panel == panel]
        for _, hv in sub.iterrows():
            fam, N, Hh = hv["family"], int(hv["N"]), int(hv["H"])
            cap = np.inf if hv["cap"] == "INF" else float(hv["cap"])
            capname = hv["cap"]
            nseed = int(hv["seeds"])
            conv = hv["convention"]
            bis = A_BISECT if fam == "A" else B_BISECT

            Wb, nsel, grs = build(rank_key, elig_real, priced, reb, N, cap, Hh, T, K, GROSS0)
            gb, tb = nrun(rets, lagmat(Wb), mkl)
            rb = gb - tb * COST / 1e4
            b = blocks(rb, warm, ins, oos)
            l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)

            out = dict(family=fam, committer=hv["committer"], panel=panel, N=N, H=Hh,
                       cap=capname, seeds=nseed, convention=conv,
                       committed_EDGE_pp=float(hv["committed_EDGE_pp"]),
                       mean_nsel=float(nsel.mean()), mean_gross=float(grs.mean()),
                       turnover=float(tb[warm].sum() / (warm.sum() / 252.0)), **b,
                       **l4b, **l4a, **l4bo,
                       pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                       pass4b_oos=all(l4bo.values()))
            out["pass4b_full_and_oos"] = out["pass4b"] and out["pass4b_oos"]

            for gate in GATESET:
                cs, isv, drier, lams = [], [], 0, []
                for s in range(nseed):
                    sd = (mdseed(panel, N, capname, s) if gate == "OPEN"
                          else mdseed(panel, N, capname, "ELIG", s))
                    rk = np.random.default_rng(sd).random((T, K))
                    eg = elig_real if gate == "ELIG" else ALLP
                    Wn, _, _ = build(rk, eg, priced, reb, N, cap, Hh, T, K, GROSS0)
                    if conv == "CASH":
                        gn, tnn = nrun(rets, lagmat(Wn), mkl)
                        rn = (gn - tnn * COST / 1e4)[warm]
                        lam = lam_cash(rn, b["MaxDD"], bis)
                        if lam is None:
                            drier += 1
                            lam = 1.0
                        cs.append(fmet(lam * rn)[0])
                        isv.append(fmet((lam * rn)[ins[warm]])[0])
                        lams.append(lam)
                    else:
                        fn = gross_rescaler(rets, lagmat(Wn), mkl)
                        lam = lam_rebuilt(fn, warm, b["MaxDD"], bis)
                        if lam is None:
                            drier += 1
                            lam = 1.0
                        rr = fn(lam)
                        cs.append(fmet(rr[warm])[0])
                        isv.append(fmet(rr[ins])[0])
                        lams.append(lam)
                cs = np.array(cs)
                isv = np.array(isv)
                e = 100.0 * (b["CAGR"] - float(np.median(cs)))
                eis = 100.0 * (b["IS_CAGR"] - float(np.median(isv)))
                out[f"EDGE_{gate}_pp"] = e
                out[f"EDGE_IS_{gate}_pp"] = eis
                out[f"EDGE_se_{gate}_pp"] = se_median(cs)
                out[f"null_med_{gate}"] = float(np.median(cs))
                out[f"drier_{gate}"] = drier
                out[f"lam_med_{gate}"] = float(np.median(lams))
            out["GATE_pp"] = out["EDGE_OPEN_pp"] - out["EDGE_ELIG_pp"]
            out["GATE_share"] = out["GATE_pp"] / out["EDGE_OPEN_pp"] if out["EDGE_OPEN_pp"] else np.nan
            out["dec_OPEN"] = bool(abs(out["EDGE_OPEN_pp"]) > DECISIVE_K * out["EDGE_se_OPEN_pp"])
            out["dec_ELIG"] = bool(abs(out["EDGE_ELIG_pp"]) > DECISIVE_K * out["EDGE_se_ELIG_pp"])
            out["sign_change"] = bool(np.sign(out["EDGE_OPEN_pp"]) != np.sign(out["EDGE_ELIG_pp"]))
            out["verdict_change"] = bool(out["dec_OPEN"] != out["dec_ELIG"])
            out["repro_err_pp"] = abs(out["EDGE_OPEN_pp"] - out["committed_EDGE_pp"])
            rows.append(out)
            P(f"   [{fam}/{hv['committer']}] {panel} N={N:<2d} H={Hh:<3d} cap={capname:<4s} "
              f"{conv:<7s} committed {out['committed_EDGE_pp']:+7.3f} | OPEN {out['EDGE_OPEN_pp']:+7.3f} "
              f"(repro {out['repro_err_pp']:.2e}) ELIG {out['EDGE_ELIG_pp']:+7.3f} "
              f"GATE {out['GATE_pp']:+7.3f}  t={time.time()-t0:5.0f}s")

    G = pd.DataFrame(rows)

    # ---- cross-run reproduction gates (G5/G6/G7) ---------------------------------------
    a = G[G.family == "A"].merge(g1086[["panel", "N", "H", "EDGE_pp"]], on=["panel", "N", "H"])
    d = float((a.EDGE_OPEN_pp - a.EDGE_pp).abs().max())
    gates[f"G5 CROSS-RUN reproduce 1086's {len(a)} committed EDGE_pp (OPEN/REBUILT/40 seeds)"] = (d, d < 1e-9)
    e = G[(G.family == "A") & (G.H == 126)].merge(
        g1085[["panel", "N", "EDGE_ELIG_pp", "EDGE_OPEN_pp"]], on=["panel", "N"], suffixes=("", "_c"))
    d = max(float((e.EDGE_ELIG_pp - e.EDGE_ELIG_pp_c).abs().max()),
            float((e.EDGE_OPEN_pp - e.EDGE_OPEN_pp_c).abs().max()))
    gates[f"G6 CROSS-RUN reproduce 1085's {len(e)} committed EDGE_ELIG_pp and EDGE_OPEN_pp"] = (d, d < 1e-9)
    n1071["capk"] = n1071["cap"].astype(str)
    bfam = G[G.family == "B"].copy()
    m = bfam.merge(n1071[["panel", "N", "capk", "null_ddmatched_CAGR_median", "book_CAGR"]],
                   left_on=["panel", "N", "cap"], right_on=["panel", "N", "capk"])
    d = max(float((m.null_med_OPEN - m.null_ddmatched_CAGR_median).abs().max()),
            float((m.CAGR - m.book_CAGR).abs().max()))
    gates[f"G7 CROSS-RUN reproduce 1071's {len(m)} committed null medians and book CAGRs (CASH/20)"] = (d, d < 1e-9)
    b82 = G[(G.family == "A") & (G.H == 126)].merge(g1082[["panel", "N", "EDGE_pp"]], on=["panel", "N"])
    d = float((b82.EDGE_OPEN_pp - b82.EDGE_pp).abs().max())
    gates[f"G8 CROSS-RUN reproduce 1082's {len(b82)} committed EDGE_pp"] = (d, d < 1e-9)
    d = float(G.repro_err_pp.max())
    gates["G9 every harvested figure reproduced from its own committer (max |err| pp)"] = (d, d < 1e-9)

    P("\n## GATES")
    for k, (v, ok) in gates.items():
        P(f"   [{'PASS' if ok else 'FAIL'}] {k}: {v:.2e}")
        gaterows.append(dict(gate=k, value=v, passed=ok))
    P(f"   {sum(1 for _, o in gates.values() if o)} of {len(gates)} PASS")

    # ---------------------------------------------------------------- the answer ---------------
    P("\n## THE RE-READ — 94 committed EDGE figures, both gates")
    neg = int((G.GATE_pp <= 0).sum())
    P(f"   H_LOWER: GATE <= 0 at {neg} of {len(G)} committed cells "
      f"({neg/len(G):.3f}).  mean GATE {G.GATE_pp.mean():+.3f} pp, "
      f"median {G.GATE_pp.median():+.3f}, range [{G.GATE_pp.min():+.3f}, {G.GATE_pp.max():+.3f}] pp")
    for fam in ["A", "B"]:
        s = G[G.family == fam]
        P(f"     FAMILY {fam}: {int((s.GATE_pp <= 0).sum())}/{len(s)} negative, "
          f"mean {s.GATE_pp.mean():+.3f} pp, range [{s.GATE_pp.min():+.3f}, {s.GATE_pp.max():+.3f}]")
    for panel in PANELS:
        for Hh in A_HS:
            s = G[(G.family == "A") & (G.panel == panel) & (G.H == Hh)]
            P(f"     A {panel} H={Hh:<3d}: {int((s.GATE_pp <= 0).sum())}/{len(s)} negative, "
              f"mean {s.GATE_pp.mean():+.3f}, range [{s.GATE_pp.min():+.3f}, {s.GATE_pp.max():+.3f}]")
    H_LOWER = neg == len(G)
    H_MAG = bool(G.GATE_pp.abs().max() <= 2.47)
    P(f"   H_MAGNITUDE: max |GATE| {G.GATE_pp.abs().max():.3f} pp against 1085's committed "
      f"0.03-2.47 envelope -> {'PASS' if H_MAG else 'FAIL'} "
      f"({int((G.GATE_pp.abs() > 2.47).sum())} cells outside)")

    nsign = int(G.sign_change.sum())
    nverd = int(G.verdict_change.sum())
    P(f"   H_SIGN:    {nsign} of {len(G)} committed figures change SIGN")
    P(f"   H_VERDICT: {nverd} of {len(G)} change the |EDGE| > {DECISIVE_K:.0f} SE decisiveness call "
      f"(decisive OPEN {int(G.dec_OPEN.sum())}, ELIG {int(G.dec_ELIG.sum())})")

    # ---- ladders and their argmaxes -----------------------------------------------------
    ladders = []
    for panel in PANELS:
        for Hh in A_HS:
            s = G[(G.family == "A") & (G.panel == panel) & (G.H == Hh)].sort_values("N")
            ladders.append(dict(ladder=f"A/{panel}/H={Hh}/N", committer="1082/1086", axis="N",
                                k=len(s),
                                argmax_OPEN=int(s.loc[s.EDGE_OPEN_pp.idxmax(), "N"]),
                                argmax_ELIG=int(s.loc[s.EDGE_ELIG_pp.idxmax(), "N"]),
                                peak_OPEN=float(s.EDGE_OPEN_pp.max()),
                                peak_ELIG=float(s.EDGE_ELIG_pp.max()),
                                spearman=float(s.EDGE_OPEN_pp.rank().corr(s.EDGE_ELIG_pp.rank()))))
        for Nn in A_NS:
            s = G[(G.family == "A") & (G.panel == panel) & (G.N == Nn)].sort_values("H")
            ladders.append(dict(ladder=f"A/{panel}/N={Nn}/H", committer="1086", axis="H", k=len(s),
                                argmax_OPEN=int(s.loc[s.EDGE_OPEN_pp.idxmax(), "H"]),
                                argmax_ELIG=int(s.loc[s.EDGE_ELIG_pp.idxmax(), "H"]),
                                peak_OPEN=float(s.EDGE_OPEN_pp.max()),
                                peak_ELIG=float(s.EDGE_ELIG_pp.max()),
                                spearman=float(s.EDGE_OPEN_pp.rank().corr(s.EDGE_ELIG_pp.rank()))))
        for Nn in B_NS:
            s = G[(G.family == "B") & (G.panel == panel) & (G.N == Nn)]
            s = s.assign(capn=[np.inf if c == "INF" else float(c) for c in s.cap]).sort_values("capn")
            ladders.append(dict(ladder=f"B/{panel}/N={Nn}/cap", committer="1071", axis="cap", k=len(s),
                                argmax_OPEN=str(s.loc[s.EDGE_OPEN_pp.idxmax(), "cap"]),
                                argmax_ELIG=str(s.loc[s.EDGE_ELIG_pp.idxmax(), "cap"]),
                                peak_OPEN=float(s.EDGE_OPEN_pp.max()),
                                peak_ELIG=float(s.EDGE_ELIG_pp.max()),
                                spearman=float(s.EDGE_OPEN_pp.rank().corr(s.EDGE_ELIG_pp.rank()))))
        s = G[(G.family == "B") & (G.panel == panel) & (G.cap == "INF")].sort_values("N")
        ladders.append(dict(ladder=f"B/{panel}/cap=INF/N", committer="1071", axis="N", k=len(s),
                            argmax_OPEN=int(s.loc[s.EDGE_OPEN_pp.idxmax(), "N"]),
                            argmax_ELIG=int(s.loc[s.EDGE_ELIG_pp.idxmax(), "N"]),
                            peak_OPEN=float(s.EDGE_OPEN_pp.max()),
                            peak_ELIG=float(s.EDGE_ELIG_pp.max()),
                            spearman=float(s.EDGE_OPEN_pp.rank().corr(s.EDGE_ELIG_pp.rank()))))
    L = pd.DataFrame(ladders)
    L["argmax_moved"] = L.argmax_OPEN.astype(str) != L.argmax_ELIG.astype(str)
    P(f"\n   H_RANK: {int(L.argmax_moved.sum())} of {len(L)} committed LADDERS change argmax")
    for _, r in L.iterrows():
        P(f"     {r.ladder:<22s} ({r.committer:<9s} axis {r.axis:<3s}, k={r.k})  argmax "
          f"{str(r.argmax_OPEN):>4s} -> {str(r.argmax_ELIG):>4s}  {'MOVED' if r.argmax_moved else 'same '}"
          f"  peak {r.peak_OPEN:+.3f} -> {r.peak_ELIG:+.3f}  rho {r.spearman:+.3f}")
    dump(L, "ladders")

    # ---- H_CONV: the doubly-committed cells ---------------------------------------------
    dbl = G[(G.cap == "INF") & (G.H == 126) & (G.N.isin(B_NS))]
    piv = dbl.pivot_table(index=["panel", "N"], columns="convention", values="GATE_pp")
    piv["sign_agree"] = np.sign(piv["CASH"]) == np.sign(piv["REBUILT"])
    H_CONV = bool(piv.sign_agree.all())
    P(f"\n   H_CONV: the {len(piv)} doubly-committed (panel, N, H=126, cap INF) cells, GATE under "
      f"each convention")
    for (pn, nn), r in piv.iterrows():
        P(f"     {pn} N={nn:<2d}  CASH {r['CASH']:+7.3f}  REBUILT {r['REBUILT']:+7.3f}  "
          f"{'agree' if r['sign_agree'] else 'DISAGREE'}  gap {abs(r['CASH']-r['REBUILT']):.3f} pp")
    P(f"     -> H_CONV {'PASS' if H_CONV else 'FAIL'}; max |CASH - REBUILT| "
      f"{float((piv['CASH']-piv['REBUILT']).abs().max()):.3f} pp")

    # ---------------------------------------------------------------- rule 8 + KEEP paths ------
    P("\n## RULE 8 WALK-FORWARD (cell chosen on IS 2009-2016 ALONE, OOS 2017-2026 read ONCE)")
    picks = []
    CH = [("C_ISEDGE_ELIG", "EDGE_IS_ELIG_pp", True), ("C_ISEDGE_OPEN", "EDGE_IS_OPEN_pp", True),
          ("C_ISSHARPE", "IS_Sharpe", True), ("C_ISDD", "IS_MaxDD", True)]
    bench = {r["panel"]: r for r in benchrows if r["series"] == "SPY"}
    lvb = {r["panel"]: r for r in benchrows if r["series"] == "RULESv2"}
    for panel in PANELS:
        s = G[G.panel == panel]
        sbp, lbp = bench[panel], lvb[panel]
        for cname, col, hi in CH:
            i = s[col].idxmax() if hi else s[col].idxmin()
            r = G.loc[i]
            o = legs_4b_oos(r, sbp)
            f4b = legs_4b(r, sbp)
            f4a = legs_4a(r, lbp)
            picks.append(dict(panel=panel, chooser=cname, family=r["family"], N=int(r["N"]),
                              H=int(r["H"]), cap=r["cap"], convention=r["convention"],
                              OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                              OOS_MaxDD=r["OOS_MaxDD"], **o, pass4b_oos=all(o.values()),
                              pass4b_full=all(f4b.values()), pass4a=all(f4a.values()),
                              EDGE_OPEN_pp=r["EDGE_OPEN_pp"], EDGE_ELIG_pp=r["EDGE_ELIG_pp"]))
            P(f"   {panel} {cname:<14s} -> family {r['family']} N={int(r['N'])} H={int(r['H'])} "
              f"cap={r['cap']}  OOS {r['OOS_CAGR']:.2%} / {r['OOS_Sharpe']:.4f} / "
              f"{r['OOS_MaxDD']:.2%}  4b_OOS {'PASS' if all(o.values()) else 'FAIL'} "
              f"({','.join(k for k, v in o.items() if not v) or 'all legs'})")
    PK = pd.DataFrame(picks)
    P(f"   H_WF: {int(PK.pass4b_oos.sum())} of {len(PK)} IS-only picks clear 4b OUT OF SAMPLE; "
      f"{int(PK.pass4a.sum())} clear 4a")
    dump(PK, "rule8")

    P(f"\n   BOTH KEEP PATHS over all {len(G)} committed cells (the BOOK is invariant to dial 2, "
      f"so these counts are the same under either gate — stated, not assumed):")
    P(f"     4a full-sample:            {int(G.pass4a.sum())} of {len(G)}")
    P(f"     4b full-sample:            {int(G.pass4b.sum())} of {len(G)}")
    P(f"     4b OUT OF SAMPLE:          {int(G.pass4b_oos.sum())} of {len(G)}")
    P(f"     4b full AND out of sample: {int(G.pass4b_full_and_oos.sum())} of {len(G)}")
    for _, r in G[G.pass4b].iterrows():
        P(f"       4b PASS: {r['panel']} N={int(r['N'])} H={int(r['H'])} cap={r['cap']} "
          f"[{r['family']}/{r['committer']}] full {r['CAGR']:.2%} / {r['Sharpe']:.4f} / "
          f"{r['MaxDD']:.2%} halves {r['H1']:.4f}/{r['H2']:.4f}  OOS {r['OOS_CAGR']:.2%} / "
          f"{r['OOS_Sharpe']:.4f} / {r['OOS_MaxDD']:.2%}  4b_OOS "
          f"{'PASS' if r['pass4b_oos'] else 'FAIL'}")

    dump(G, "grid")
    dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame(benchrows), "benchmarks")
    dump(wide.reset_index(drop=True), "wide")
    hyp = pd.DataFrame([
        dict(hypothesis="H_LOWER", declared="GATE <= 0 at every committed cell",
             result=f"{neg}/{len(G)} negative", passed=bool(H_LOWER)),
        dict(hypothesis="H_MAGNITUDE", declared="|GATE| inside 1085's 0.03-2.47 pp envelope",
             result=f"max |GATE| {G.GATE_pp.abs().max():.3f} pp", passed=bool(H_MAG)),
        dict(hypothesis="H_SIGN", declared="no committed EDGE figure changes sign",
             result=f"{nsign}/{len(G)} change sign", passed=bool(nsign == 0)),
        dict(hypothesis="H_RANK", declared="no committed ladder changes argmax (expected to fail)",
             result=f"{int(L.argmax_moved.sum())}/{len(L)} ladders move",
             passed=bool(L.argmax_moved.sum() == 0)),
        dict(hypothesis="H_VERDICT", declared=f"no cell changes the |EDGE| > {DECISIVE_K:.0f} SE call",
             result=f"{nverd}/{len(G)} change", passed=bool(nverd == 0)),
        dict(hypothesis="H_CONV", declared="CASH and REBUILT agree on sign(GATE) at the 8 doubly-"
                                          "committed cells",
             result=f"{int(piv.sign_agree.sum())}/{len(piv)} agree", passed=bool(H_CONV)),
        dict(hypothesis="H_WF", declared="an IS-only pick clears 4b out of sample",
             result=f"{int(PK.pass4b_oos.sum())}/{len(PK)}", passed=bool(PK.pass4b_oos.sum() > 0)),
    ])
    P("\n## HYPOTHESES")
    for _, r in hyp.iterrows():
        P(f"   [{'PASS' if r.passed else 'FAIL'}] {r.hypothesis:<12s} {r.declared} -> {r.result}")
    dump(hyp, "hypotheses")

    P(f"\n## SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT panels.  Every level is")
    P("   optimistic and every 4a/4b count is an UPPER bound.  EDGE_OPEN, EDGE_ELIG and GATE are")
    P("   within-pool contrasts over the same tape, so the bias very largely cancels out of them;")
    P("   it does NOT cancel out of the 4b legs, which are measured against SPY, a real index.")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
