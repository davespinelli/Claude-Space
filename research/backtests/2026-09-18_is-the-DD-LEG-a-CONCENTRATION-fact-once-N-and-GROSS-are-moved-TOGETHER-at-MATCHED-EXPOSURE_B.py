#!/usr/bin/env python3
"""2026-09-18 lane B, QUEUE idea 1270 — is the DD LEG a CONCENTRATION fact once N and GROSS
are moved TOGETHER at MATCHED EXPOSURE?

QUESTION (QUEUE idea 1270, verbatim)
    N and GROSS have each been dialled alone, and each is a pure CAGR-for-drawdown slide;
    nobody has moved them together along an ISO-EXPOSURE line, where diversification is
    bought without buying it with cash.  Walk (N, GROSS) pairs holding realised mean exposure
    at the committed 0.75 (N {10,20,30,40,50} x the gross that matches), report all grid
    points, both KEEP paths, rule-8 OOS, and the realised exposure of every cell as proof the
    line is level.  Rationale: if the DD leg is breadth rather than exposure, this is the only
    cut that can show it.  Max 2 params (N, exposure target).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. N      in {10, 20, 30, 40, 50} slots.  20 is the incumbent (936/1059/1064/1071/1081).
    2. EBAR   in {0.55, 0.65, 0.75, 0.85} — the TARGET REALISED MEAN EXPOSURE.  0.75 is the
              committed level.  GROSS is NOT a third dial: it is SOLVED, per (panel, N, EBAR),
              as the unique G whose IN-SAMPLE realised mean exposure equals EBAR.
    All 5 x 4 = 20 cells are reported at EVERY panel, including cells that turn out
    INFEASIBLE (G > 1.00 would be needed — no leverage, PROTOCOL rule 2).  Nothing else is
    tuned.  The anchor cell (N=20, EBAR=0.75) is the do-nothing point.

WHY GROSS HAS TO BE SOLVED RATHER THAN DIALLED — THE ENTANGLEMENT THIS RUN CORRECTS
    The book is a SLOT book: N slots, per-name target G/N, UNFILLED SLOTS STAY IN CASH (the
    live RULES v2 de-gross clause: gated-out weight goes to cash, never re-spread).  The
    eligible pool thins as N grows, so realised exposure is G * E[n_sel]/N and FALLS in N at
    fixed G.  1071 and 1081 dialled N with G pinned at 0.75 and therefore slid DOWN in
    exposure as they widened — exactly the confound idea 1270 names.  Holding EBAR level
    forces G UP as N rises, so the extra breadth is paid for out of the same exposure budget
    and not out of cash.  If the 4b drawdown leg is a BREADTH fact, this is the cut that
    shows it; if it is an EXPOSURE fact, the iso-exposure rows will be flat in N.

WHAT MAKES THIS A TEST AND NOT A RE-RUN — DECLARED BEFORE ANY NUMBER
    (a) The grid is 2-D ON PURPOSE.  Along a ROW (fixed EBAR, N varying) is PURE BREADTH at
        level exposure.  Along a COLUMN (fixed N, EBAR varying) is the PURE FLAT GROSS CUT.
        Both are measured on the same tape with the same book, so the two can be priced
        against each other instead of against a memory of an earlier run.
    (b) THE FLAT-CUT ISOQUANT IS THE COMPARAND, stated in advance.  The N=20 column is the
        incumbent breadth at four exposures — a (|MaxDD|, CAGR) curve.  Every N != 20 cell is
        priced against that curve INTERPOLATED AT ITS OWN |MaxDD|: the question "does breadth
        buy the drawdown more cheaply than cash does?" has one number, CAGR_cell minus
        CAGR_flatcut_at_equal_DD, and it is reported for all of them.
    (c) EVERY CELL PUBLISHES ITS REALISED EXPOSURE (daily held gross, full / IS / OOS, plus
        target gross at rebalance dates) so the levelness of each row is EVIDENCE, not an
        assumption.  The within-row spread is gated.
    (d) G IS CALIBRATED ON THE IN-SAMPLE WINDOW ONLY (warm-up..2016-12-31).  The OOS arm
        therefore contains no full-sample information at all, not even through the exposure
        normalisation, so rule 8 is clean by construction.

PRE-REGISTERED HYPOTHESES, declared before the grid was read, scored as they fell:
  H_ENTANGLE  the confound is real: the solved G RISES in N at EBAR = 0.75 on both panels.
  H_LEVEL     the iso-exposure rows are LEVEL: within-row spread of full-sample realised
              exposure <= 0.010 at every (panel, EBAR).
  H_BREADTH   THE QUEUE'S QUESTION: at level exposure |MaxDD| still RISES in N (breadth does
              NOT buy the drawdown leg).  Scored at EBAR = 0.75 on both panels.
  H_CHEAPER   breadth buys the drawdown MORE CHEAPLY than cash: some N != 20 cell beats the
              N=20 flat-cut isoquant interpolated at its own |MaxDD| (gap > 0).
  H_DOMINATE  some N > 20 cell DOMINATES its own row's N=20 cell on BOTH CAGR and |MaxDD|.
  H_4b        at least one NON-INCUMBENT cell (N != 20 or EBAR != 0.75) passes all five 4b legs.
  H_R8        rule 8 (cell chosen on warm-up..2016-12-31, 2017-2026 read ONCE) reaches a cell
              whose OOS Sharpe beats the do-nothing anchor on a MAJORITY of (panel, chooser).

PRE-DECLARED VERDICT RULE: KEEP (path 4b) only if a cell clears EVERY 4b leg AND rule 8
    reaches it AND its OOS Sharpe is above its panel's anchor.  A cell that clears 4b but is
    not reached by any honest chooser is PARK at best.  A 4b pass AT the anchor cell is the
    INCUMBENT, not a new book, and is counted, named and excluded from KEEP/PARK.  4a is
    judged against the live RULES v2 book on the same panel.  Neither dial is re-tuned after
    reading; both ladders and the verdict rule are fixed by this docstring.

FROZEN BOOK (936/1064/1071/1081's construction, nothing here re-tunes it): RAW three-leg
    composite of percentile ranks (21/252, 0/126, 0/63), NO vol scaler, gate = above 200d MA
    AND vol20 < 0.60, H = 126 minimum hold, weekly decide / t+1 execution, 10 bps on traded
    notional, warm-up 260 days.  The ONLY departure is the sizing clause, which is the object
    of the study: per-name G/N with residual to CASH (== 1081's cap = 1.00 corner).

SURVIVORSHIP (PROTOCOL rule 9).  U56 (research/universe.json) and B136
    (research/universe_broad.json) are CURRENT-CONSTITUENT lists, so every LEVEL here —
    CAGR, Sharpe, and every 4b count — is optimistic, and the 4b counts are UPPER bounds.
    The deliverables of this run are DIFFERENCES INSIDE ONE PANEL over the SAME tape: the
    sign of d|MaxDD|/dN along a level-exposure row, the row-vs-column contrast, and the
    flat-cut isoquant gap.  Those are books drawn from the same biased pool and the bias
    very largely cancels out of them.  SPY sits inside the U56/B136 selection sets exactly as
    936/1071/1081 built them, so the incumbent anchor reproduces (gate G2).
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "is-the-DD-LEG-a-CONCENTRATION-fact-once-N-and-GROSS-are-moved-TOGETHER-at-MATCHED-EXPOSURE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
COST, FREQ, HOLD = 10.0, "W", 126
GROSS0 = 0.75                      # the committed exposure level / incumbent target gross
LEGS = [(21, 252), (0, 126), (0, 63)]
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GMAX = 1.00                        # no leverage (PROTOCOL rule 2); cells needing more are INFEASIBLE

NS = [10, 20, 30, 40, 50]                  # dial 1
EBARS = [0.55, 0.65, 0.75, 0.85]           # dial 2 (target realised mean exposure)
ANCHOR = (20, 0.75)
LEVEL_TOL = 0.010                          # H_LEVEL / gate G10 within-row exposure spread

# committed cross-run anchors (tape vintages differ; tolerances stated at each gate)
A936_WH126 = (0.155787, 1.139701, -0.191276)   # 936/1071/1081 U56 CAND20 W/H126 0.75 10bps, re-spread
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------------------------------ metrics (1071/1081's, verbatim)
def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    c = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return c, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def fvol(r):
    return float(np.asarray(r, float).std(ddof=1) * np.sqrt(252.0))


def ddspan(r, idx, warm):
    rr = np.asarray(r, float)[warm]
    ii = idx[warm]
    eq = np.cumprod(1.0 + rr)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    j = int(dd.argmin())
    i = int(np.argmax(eq[:j + 1])) if j else 0
    return str(ii[i].date()), str(ii[j].date()), float(dd[j])


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    if ra.std(ddof=0) == 0 or rb.std(ddof=0) == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (ra.std(ddof=0) * rb.std(ddof=0)))


def olsslope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 2 or x.std() == 0:
        return float("nan")
    return float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    return warm, warm & ~oos, oos


def blocks(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, Vol=fvol(rr), H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_Vol=fvol(r[oos]))


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ------------------------------------------------------------------ fast runner (1081's, gated)
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
    return (held * rets).sum(axis=1), turn, held


# ------------------------------------------------------------------ selection (1081's build, factored)
def build_sel(rank_key, elig, priced, reb, N, H, T, K):
    """The frozen selection: N slots, minimum hold H, fill empty slots from the eligible set
    by composite rank.  Returns the 0/1 HELD indicator (T x K) and n_sel per rebalance date.
    Selection does NOT depend on gross, so one call serves every G on the same N."""
    S = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel, selby = [], []
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
        nsel.append(len(sel))
        selby.append(sel)
        stop = reb[i + 1] if i + 1 < len(reb) else T
        S[t:stop, sel] = 1.0
    return S, np.array(nsel), selby


def build_respread(rank_key, elig, priced, reb, N, H, T, K, gross):
    """1081's cap=INF corner, kept ONLY to reproduce the committed incumbent triple (gate G2):
    w_i = gross / n_sel, so target gross is `gross` whenever the pool is non-empty."""
    S, nsel, _ = build_sel(rank_key, elig, priced, reb, N, H, T, K)
    n = S.sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(n[:, None] > 0, S * (gross / np.maximum(n, 1)[:, None]), 0.0)


def mech(px_inv, cols_all, inv):
    """936/1064/1071/1081's selection score (higher better) and gate, widened to the full
    column space with non-investable columns permanently ineligible."""
    parts = []
    for skip, look in LEGS:
        x = (px_inv.shift(skip) / px_inv.shift(look) - 1.0) if skip else (px_inv / px_inv.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px_inv > px_inv.rolling(200).mean()
    vol20 = px_inv.pct_change().rolling(20).std() * np.sqrt(252)
    sc_i = (comp * (0.5 + 0.5 * above.astype(float))).values
    el_i = (above & (vol20 < MAXVOL)).values
    T, K = len(px_inv), len(cols_all)
    pos = np.array([cols_all.index(c) for c in inv])
    sc = np.full((T, K), np.nan)
    el = np.zeros((T, K), dtype=bool)
    sc[:, pos] = sc_i
    el[:, pos] = el_i
    return sc, el


# ------------------------------------------------------------------ the iso-exposure solve
def run_G(rets, S, mk_lag, N, G):
    """Size the frozen selection at G/N per slot, residual -> CASH. Returns net returns,
    turnover and the DAILY REALISED EXPOSURE path (held gross as a fraction of NAV)."""
    W = S * (G / N)
    g, tn, held = nrun(rets, lagmat(W), mk_lag)
    return g - tn * COST / 1e4, tn, held.sum(axis=1)


def solve_G(rets, S, mk_lag, N, ebar, ins, iters=48):
    """The unique G whose IN-SAMPLE mean realised exposure equals `ebar`.  Monotone in G, so
    bisection on [0, GMAX].  Returns (G, feasible): infeasible when even G = GMAX (no
    leverage) cannot reach `ebar`."""
    def expo(G):
        return float(run_G(rets, S, mk_lag, N, G)[2][ins].mean())
    hi = expo(GMAX)
    if hi < ebar:
        return GMAX, False
    lo_g, hi_g = 0.0, GMAX
    for _ in range(iters):
        mid = 0.5 * (lo_g + hi_g)
        if expo(mid) < ebar:
            lo_g = mid
        else:
            hi_g = mid
    return 0.5 * (lo_g + hi_g), True


def isoquant_gap(row20, dd, cagr):
    """CAGR of the N=20 FLAT-CUT curve interpolated at |MaxDD| = dd, and the cell's excess.
    row20 is the four (|DD|, CAGR) points of the anchor-breadth column, sorted by |DD|."""
    x = np.array([abs(d) for d, _ in row20], float)
    y = np.array([c for _, c in row20], float)
    o = np.argsort(x)
    x, y = x[o], y[o]
    ad = abs(dd)
    if ad < x[0] or ad > x[-1]:
        return np.nan, np.nan, "extrapolation-refused"
    fc = float(np.interp(ad, x, y))
    return fc, float(cagr - fc), "ok"


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# {DATE} lane B, QUEUE idea 1270 — {SLUG}")
    P(f"# 2 tuned dials: N {NS} x EBAR (target realised mean exposure) {EBARS}.  ALL 20 cells")
    P(f"#   reported per panel.  GROSS is SOLVED per cell, not dialled: the G whose IN-SAMPLE")
    P(f"#   realised mean exposure == EBAR, capped at {GMAX:.2f} (no leverage; cells needing more")
    P(f"#   are published INFEASIBLE).  Anchor cell = N{ANCHOR[0]} / EBAR {ANCHOR[1]:.2f}.")
    P(f"# frozen book: RAW composite {LEGS}, no vol scaler, above-200d AND vol20 < {MAXVOL}, "
      f"H={HOLD}, weekly, {COST:.0f} bps, t+{LAG}, warm-up {WARMUP}; sizing = G/N per slot, "
      f"unfilled slots -> CASH")
    P("# reported-not-dials: PANEL {U56, B136} (rule 9, current constituents).")
    P("# DECLARED BEFORE ANY NUMBER: the deliverable is the SIGN of d|MaxDD|/dN ALONG A LEVEL-")
    P("#   EXPOSURE ROW and the FLAT-CUT ISOQUANT GAP; levels are survivorship-inflated and")
    P("#   every 4b count is an UPPER bound.  G is calibrated on IS only, so OOS is clean.")
    P("")

    rows, expo_rows, r8rows, gaterows, benchrows, ddrows = [], [], [], [], [], []
    gates: dict[str, tuple] = {}

    panels = []
    px_u = load_universe().dropna(how="all").ffill()
    panels.append((f"U{px_u.shape[1]}", px_u, list(px_u.columns)))
    px_b = load_universe(broad=True).dropna(how="all").ffill()
    panels.append((f"B{px_b.shape[1]}", px_b, list(px_b.columns)))

    for panel, px, inv in panels:
        cols = list(px.columns)
        idx = px.index
        K = len(cols)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        reb = np.flatnonzero(mk)
        mk_lag = np.roll(mk, LAG)
        warm, ins, oos = windows(idx)
        sc, elig = mech(px[inv], cols, inv)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        P(f"\n## {panel}: {K} columns, {len(idx)} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates; IS <= {IS_END} ({int(ins.sum())}d), OOS ({int(oos.sum())}d)")
        P(f"   SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   4b bars on this panel: |MaxDD| <= {DD_CAP*abs(sb['MaxDD']):.2%}, "
          f"CAGR >= {CAGR_FLOOR*sb['CAGR']:.2%}, Sharpe > SPY in H1 / H2 / OOS")
        P(f"   RULES v2  full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  halves "
          f"{lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb), dict(panel=panel, series="RULESv2", **lb)]

        # ---- selection built ONCE per N (it does not depend on G) ----------------------------
        SEL = {}
        for N in NS:
            SEL[N] = build_sel(rank_key, elig, priced, reb, N, HOLD, len(idx), K)

        # ---- gates that need the incumbent re-spread book -------------------------------------
        if panel.startswith("U"):
            Wr = build_respread(rank_key, elig, priced, reb, 20, HOLD, len(idx), K, GROSS0)
            eng = backtest(px, pd.DataFrame(Wr, index=idx, columns=cols),
                           cost_bps=COST, freq=FREQ)["returns"].values
            g, tn, _ = nrun(rets, lagmat(Wr), mk_lag)
            fast = g - tn * COST / 1e4
            d1 = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U, incumbent re-spread N20/0.75)"] = (d1, d1 < 1e-12)
            m = fmet(fast[warm])
            d2 = max(abs(m[0] - A936_WH126[0]), abs(m[1] - A936_WH126[1]), abs(m[2] - A936_WH126[2]))
            gates["G2 CROSS-RUN vs 936/1071/1081 committed W/H126 triple (tape vintage differs)"] = (d2, d2 < 5e-3)
            P(f"   INCUMBENT (re-spread N20 @ {GROSS0}): {m[0]:.2%} / {m[1]:.4f} / {m[2]:.2%}   "
              f"committed {A936_WH126[0]:.2%} / {A936_WH126[1]:.4f} / {A936_WH126[2]:.2%}  max|d| {d2:.2e}")
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-3)
            d4 = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G4 live RULES v2 MaxDD == committed -12.05%"] = (d4, d4 < 5e-3)

        # ---- THE ENTANGLEMENT the run corrects: exposure at FIXED gross, as N moves ----------
        for N in NS:
            S, nsel, _ = SEL[N]
            _, _, ex = run_G(rets, S, mk_lag, N, GROSS0)
            expo_rows.append(dict(panel=panel, N=N, fixed_G=GROSS0, mean_nsel=float(nsel.mean()),
                                  fill=float(nsel.mean() / N),
                                  realised_expo_full=float(ex[warm].mean()),
                                  realised_expo_IS=float(ex[ins].mean()),
                                  realised_expo_OOS=float(ex[oos].mean())))

        # ---- the 5 x 4 iso-exposure grid ------------------------------------------------------
        maxG = 0.0
        for N in NS:
            S, nsel, selby = SEL[N]
            for ebar in EBARS:
                G, feas = solve_G(rets, S, mk_lag, N, ebar, ins)
                r, tn, ex = run_G(rets, S, mk_lag, N, G)
                b = blocks(r, warm, ins, oos)
                l4b, l4a = legs_4b(b, sb), legs_4a(b, lb)
                maxG = max(maxG, G)
                pk, tr, dp = ddspan(r, idx, warm)
                rows.append(dict(panel=panel, N=N, ebar=ebar, G=G, feasible=feas,
                                 mean_nsel=float(nsel.mean()), fill=float(nsel.mean() / N),
                                 expo_full=float(ex[warm].mean()), expo_IS=float(ex[ins].mean()),
                                 expo_OOS=float(ex[oos].mean()), expo_sd=float(ex[warm].std(ddof=1)),
                                 turnover=float(tn[warm].sum() / (warm.sum() / 252.0)), **b,
                                 dd_peak=pk, dd_trough=tr, dd_depth=dp,
                                 is_anchor=bool(N == ANCHOR[0] and abs(ebar - ANCHOR[1]) < 1e-12),
                                 pass4b=all(l4b.values()), fail4b=failed(l4b),
                                 pass4a=all(l4a.values()), fail4a=failed(l4a), **l4b, **l4a))
        gates[f"G7 no leverage on {panel} (max solved target gross <= {GMAX:.2f})"] = (maxG, maxG <= GMAX + 1e-12)

        u = pd.DataFrame([x for x in rows if x["panel"] == panel])
        f0 = pd.DataFrame([x for x in expo_rows if x["panel"] == panel]).sort_values("N")
        gates[f"G8 N dial is LIVE on {panel} (mean slots filled rises with N)"] = (
            f"{f0.mean_nsel.iloc[0]:.1f}->{f0.mean_nsel.iloc[-1]:.1f}",
            f0.mean_nsel.iloc[-1] > f0.mean_nsel.iloc[0] + 1.0)
        gates[f"G9 EBAR dial is LIVE on {panel} (realised exposure separates the four rows)"] = (
            f"{u[u.N==20].sort_values('ebar').expo_full.iloc[0]:.4f}"
            f"->{u[u.N==20].sort_values('ebar').expo_full.iloc[-1]:.4f}",
            u[u.N == 20].expo_full.max() - u[u.N == 20].expo_full.min() > 0.10)
        spreads = {e: float(u[u.ebar == e].expo_full.max() - u[u.ebar == e].expo_full.min()) for e in EBARS}
        gates[f"G10 iso-exposure rows LEVEL on {panel} (max within-row full-sample spread <= {LEVEL_TOL})"] = (
            max(spreads.values()), max(spreads.values()) <= LEVEL_TOL)
        gates[f"G11 IS calibration EXACT on {panel} (max |expo_IS - EBAR| over feasible cells)"] = (
            float(np.nanmax(np.abs(u[u.feasible].expo_IS - u[u.feasible].ebar))),
            float(np.nanmax(np.abs(u[u.feasible].expo_IS - u[u.feasible].ebar))) < 1e-6)

        # ---- the grid, printed in full --------------------------------------------------------
        P(f"\n   ALL {len(u)} CELLS on {panel}  (G solved on IS; expo = realised daily held gross)")
        P(f"   {'N':>3} {'EBAR':>5} {'G':>6} {'feas':>4} {'nsel':>5} {'fill':>5} {'expoF':>6} "
          f"{'expoIS':>6} {'expoOOS':>7} {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'Vol':>6} "
          f"{'turn':>5} {'H1':>6} {'H2':>6} {'OOS_S':>7} {'4b':>3} {'4a':>3}  fail4b")
        for _, x in u.sort_values(["ebar", "N"]).iterrows():
            P(f"   {int(x.N):3d} {x.ebar:5.2f} {x.G:6.4f} {'Y' if x.feasible else 'NO':>4} "
              f"{x.mean_nsel:5.1f} {x.fill:5.1%} {x.expo_full:6.4f} {x.expo_IS:6.4f} {x.expo_OOS:7.4f} "
              f"{x.CAGR:7.2%} {x.Sharpe:7.4f} {x.MaxDD:8.2%} {x.Vol:6.2%} {x.turnover:5.2f} "
              f"{x.H1:6.3f} {x.H2:6.3f} {x.OOS_Sharpe:7.4f} {'Y' if x.pass4b else 'n':>3} "
              f"{'Y' if x.pass4a else 'n':>3}  {x.fail4b}")

        # ---- THE ANSWER: d|MaxDD|/dN ALONG each level-exposure row ----------------------------
        P(f"\n   d|MaxDD|/dN ALONG EACH LEVEL-EXPOSURE ROW on {panel} (pp of drawdown per extra slot)")
        P(f"   {'EBAR':>5} {'rowSpreadExpo':>13} {'dDD/dN':>8} {'DD@N10':>8} {'DD@N50':>8} "
          f"{'d10-50':>8} {'dCAGR/dN':>9} {'dVol/dN':>8} {'dSh/dN':>8} {'mono':>6} {'rc(N,DD)':>9}")
        for ebar in EBARS:
            s = u[u.ebar == ebar].sort_values("N")
            P(f"   {ebar:5.2f} {spreads[ebar]:13.5f} "
              f"{olsslope(s.N.values, np.abs(s.MaxDD.values))*100:+8.4f} {s.MaxDD.iloc[0]:8.2%} "
              f"{s.MaxDD.iloc[-1]:8.2%} {100*(abs(s.MaxDD.iloc[-1])-abs(s.MaxDD.iloc[0])):+8.2f} "
              f"{olsslope(s.N.values, s.CAGR.values)*100:+9.4f} "
              f"{olsslope(s.N.values, s.Vol.values)*100:+8.4f} "
              f"{olsslope(s.N.values, s.Sharpe.values):+8.4f} "
              f"{('UP' if np.all(np.diff(np.abs(s.MaxDD.values))>0) else ('DOWN' if np.all(np.diff(np.abs(s.MaxDD.values))<0) else '-')):>6} "
              f"{rankcorr(s.N.values, np.abs(s.MaxDD.values)):+9.2f}")

        P(f"\n   THE PURE FLAT CUT for comparison on {panel} — the N=20 COLUMN (EBAR varying)")
        P(f"   {'EBAR':>5} {'expoF':>6} {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'OOS_S':>7}")
        for _, x in u[u.N == 20].sort_values("ebar").iterrows():
            P(f"   {x.ebar:5.2f} {x.expo_full:6.4f} {x.CAGR:7.2%} {x.Sharpe:7.4f} {x.MaxDD:8.2%} {x.OOS_Sharpe:7.4f}")

        # ---- RULE 8: choose on IS only, read OOS once -----------------------------------------
        anc = u[u.is_anchor].iloc[0]
        for cname, key in [("C_ISSHARPE", "IS_Sharpe"), ("C_ISDD", "IS_MaxDD"),
                           ("C_ISCAGR", "IS_CAGR"), ("C_ISCALMAR", "IS_CALMAR")]:
            uu = u[u.feasible]
            if key == "IS_MaxDD":
                v = -np.abs(uu.IS_MaxDD.values)
            elif key == "IS_CALMAR":
                v = uu.IS_CAGR.values / np.abs(uu.IS_MaxDD.values)
            else:
                v = uu[key].values
            pick = uu.iloc[int(np.nanargmax(v))]
            r8rows.append(dict(panel=panel, chooser=cname, N=int(pick.N), ebar=float(pick.ebar),
                               G=float(pick.G), OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD, anchor_OOS_Sharpe=anc.OOS_Sharpe,
                               anchor_OOS_MaxDD=anc.OOS_MaxDD, anchor_OOS_CAGR=anc.OOS_CAGR,
                               d_OOS_Sharpe=pick.OOS_Sharpe - anc.OOS_Sharpe,
                               d_OOS_MaxDD_pp=100.0 * (abs(pick.OOS_MaxDD) - abs(anc.OOS_MaxDD)),
                               spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_CAGR=sb["OOS_CAGR"],
                               spy_OOS_MaxDD=sb["OOS_MaxDD"], live_OOS_Sharpe=lb["OOS_Sharpe"],
                               beats_anchor=bool(pick.OOS_Sharpe > anc.OOS_Sharpe),
                               beats_spy=bool(pick.OOS_Sharpe > sb["OOS_Sharpe"]),
                               picks_anchor=bool(pick.is_anchor), pass4b=bool(pick.pass4b),
                               rc_Sharpe_IS_OOS=rankcorr(uu.IS_Sharpe.values, uu.OOS_Sharpe.values),
                               rc_absDD_IS_OOS=rankcorr(np.abs(uu.IS_MaxDD.values), np.abs(uu.OOS_MaxDD.values)),
                               rc_N_OOSDD=rankcorr(uu.N.values, np.abs(uu.OOS_MaxDD.values))))

        for _, x in u.iterrows():
            ddrows.append(dict(panel=panel, N=int(x.N), ebar=float(x.ebar),
                               dd_peak=x.dd_peak, dd_trough=x.dd_trough, dd_depth=x.dd_depth))

    grid = pd.DataFrame(rows)
    r8 = pd.DataFrame(r8rows)
    fixdf = pd.DataFrame(expo_rows)

    # ---------------------------------------------------------------- flat-cut isoquant gap
    iso = []
    for panel in grid.panel.unique():
        u = grid[grid.panel == panel]
        row20 = [(x.MaxDD, x.CAGR) for _, x in u[u.N == 20].iterrows()]
        for _, x in u[u.N != 20].iterrows():
            fc, gap, st = isoquant_gap(row20, x.MaxDD, x.CAGR)
            iso.append(dict(panel=panel, N=int(x.N), ebar=float(x.ebar), G=x.G, CAGR=x.CAGR,
                            MaxDD=x.MaxDD, flatcut_CAGR_at_equal_DD=fc, gap_pp=100.0 * gap
                            if np.isfinite(gap) else np.nan, status=st,
                            OOS_Sharpe=x.OOS_Sharpe, Sharpe=x.Sharpe))
    isod = pd.DataFrame(iso)

    # ---------------------------------------------------------------- gates
    P("\n## GATES (printed before any hypothesis is scored)")
    npass = 0
    for k, (v, ok) in gates.items():
        npass += bool(ok)
        vs = v if isinstance(v, str) else (f"{v:.3e}" if isinstance(v, float) and abs(v) < 1 else f"{v}")
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: {vs}")
        gaterows.append(dict(gate=k, value=str(v), pass_=bool(ok)))
    P(f"   GATES {npass} of {len(gates)} PASS")

    # ---------------------------------------------------------------- the entanglement
    P("\n## THE CONFOUND idea 1270 NAMES — realised exposure at FIXED gross 0.75 as N moves")
    P(f"   {'panel':>6} {'N':>3} {'mean_nsel':>9} {'fill':>6} {'expo_full':>9} {'expo_IS':>8} {'expo_OOS':>8}")
    for _, x in fixdf.iterrows():
        P(f"   {x.panel:>6} {int(x.N):3d} {x.mean_nsel:9.2f} {x.fill:6.1%} {x.realised_expo_full:9.4f} "
          f"{x.realised_expo_IS:8.4f} {x.realised_expo_OOS:8.4f}")
    for panel in fixdf.panel.unique():
        z = fixdf[fixdf.panel == panel].sort_values("N")
        P(f"   {panel}: exposure at fixed G=0.75 runs {z.realised_expo_full.iloc[0]:.4f} -> "
          f"{z.realised_expo_full.iloc[-1]:.4f} over N {z.N.iloc[0]}->{z.N.iloc[-1]} "
          f"({100*(z.realised_expo_full.iloc[-1]-z.realised_expo_full.iloc[0]):+.2f} pp), slope "
          f"{olsslope(z.N.values, z.realised_expo_full.values)*100:+.4f} pp/slot")
        g75 = grid[(grid.panel == panel) & (grid.ebar == 0.75)].sort_values("N")
        P(f"   {panel}: the G that RESTORES 0.75 runs {g75.G.iloc[0]:.4f} -> {g75.G.iloc[-1]:.4f} "
          f"over the same N ({olsslope(g75.N.values, g75.G.values)*1000:+.4f} per 1000 slots)")

    # ---------------------------------------------------------------- flat-cut isoquant
    P("\n## THE FLAT-CUT ISOQUANT — does BREADTH buy the drawdown more cheaply than CASH?")
    P("##   gap_pp = cell CAGR minus the N=20 flat-cut curve's CAGR interpolated at the SAME |MaxDD|.")
    P("##   gap > 0 means breadth bought that drawdown more cheaply than de-grossing did.")
    P(f"   {'panel':>6} {'N':>3} {'EBAR':>5} {'MaxDD':>8} {'CAGR':>7} {'flatcutCAGR':>11} {'gap_pp':>7}  status")
    for _, x in isod.iterrows():
        fc = f"{x.flatcut_CAGR_at_equal_DD:11.2%}" if np.isfinite(x.flatcut_CAGR_at_equal_DD) else f"{'-':>11}"
        gp = f"{x.gap_pp:+7.2f}" if np.isfinite(x.gap_pp) else f"{'-':>7}"
        P(f"   {x.panel:>6} {int(x.N):3d} {x.ebar:5.2f} {x.MaxDD:8.2%} {x.CAGR:7.2%} {fc} {gp}  {x.status}")
    ok = isod[np.isfinite(isod.gap_pp)]
    P(f"   comparable cells {len(ok)} of {len(isod)}; gap > 0 at {int((ok.gap_pp > 0).sum())} of {len(ok)}; "
      f"mean {ok.gap_pp.mean():+.3f} pp, best {ok.gap_pp.max():+.3f} pp, worst {ok.gap_pp.min():+.3f} pp")

    # ---------------------------------------------------------------- dominance
    dom = []
    for panel in grid.panel.unique():
        u = grid[grid.panel == panel]
        for ebar in EBARS:
            a = u[(u.N == 20) & (u.ebar == ebar)].iloc[0]
            for _, x in u[(u.N > 20) & (u.ebar == ebar)].iterrows():
                dom.append(dict(panel=panel, N=int(x.N), ebar=ebar,
                                d_CAGR_pp=100.0 * (x.CAGR - a.CAGR),
                                d_absDD_pp=100.0 * (abs(x.MaxDD) - abs(a.MaxDD)),
                                dominates=bool(x.CAGR >= a.CAGR and abs(x.MaxDD) <= abs(a.MaxDD)
                                               and (x.CAGR > a.CAGR or abs(x.MaxDD) < abs(a.MaxDD)))))
    domd = pd.DataFrame(dom)
    P("\n## DOMINANCE AT LEVEL EXPOSURE — does any WIDER book beat its own row's N=20 on BOTH legs?")
    P(f"   {'panel':>6} {'N':>3} {'EBAR':>5} {'dCAGR pp':>9} {'d|DD| pp':>9}  dominates")
    for _, x in domd.iterrows():
        P(f"   {x.panel:>6} {int(x.N):3d} {x.ebar:5.2f} {x.d_CAGR_pp:+9.2f} {x.d_absDD_pp:+9.2f}  "
          f"{'YES' if x.dominates else 'no'}")
    P(f"   dominating cells {int(domd.dominates.sum())} of {len(domd)}")

    # ---------------------------------------------------------------- drawdown episode
    P("\n## THE DRAWDOWN EPISODE ITSELF at EBAR = 0.75 — same event at every breadth?")
    dd = pd.DataFrame(ddrows)
    for _, x in dd[dd.ebar == 0.75].iterrows():
        P(f"   {x.panel:>6} N={int(x.N):2d}  peak {x.dd_peak}  ->  trough {x.dd_trough}  {x.dd_depth:8.2%}")

    # ---------------------------------------------------------------- rule 8
    P("\n## RULE 8 — cell chosen on warm-up..2016-12-31 ONLY (G also calibrated there), 2017-2026 read ONCE")
    P(f"   {'panel':>6} {'chooser':>11} {'pick':>14} {'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8} "
      f"{'d vs anchor':>11} {'>SPY':>5} {'=anchor':>7} {'rc(Sh)':>7} {'rc(|DD|)':>8} {'rc(N,ooDD)':>10}")
    for _, x in r8.iterrows():
        P(f"   {x.panel:>6} {x.chooser:>11} {f'N{int(x.N)}/E{x.ebar:.2f}':>14} {x.OOS_CAGR:9.2%} "
          f"{x.OOS_Sharpe:8.4f} {x.OOS_MaxDD:8.2%} {x.d_OOS_Sharpe:+11.4f} "
          f"{'Y' if x.beats_spy else 'n':>5} {'Y' if x.picks_anchor else 'n':>7} "
          f"{x.rc_Sharpe_IS_OOS:+7.2f} {x.rc_absDD_IS_OOS:+8.2f} {x.rc_N_OOSDD:+10.2f}")
    P(f"   choosers beating the anchor OOS: {int(r8.beats_anchor.sum())} of {len(r8)}; "
      f"mean d_OOS_Sharpe {r8.d_OOS_Sharpe.mean():+.4f}; mean d_OOS|DD| {r8.d_OOS_MaxDD_pp.mean():+.2f} pp")

    # ---------------------------------------------------------------- KEEP paths
    P("\n## KEEP PATHS, all cells")
    for p in grid.panel.unique():
        s = grid[grid.panel == p]
        P(f"   {p}: 4a {int(s.pass4a.sum())} of {len(s)}   4b {int(s.pass4b.sum())} of {len(s)}   "
          f"(4b passes that are the ANCHOR cell: {int((s.pass4b & s.is_anchor).sum())})   "
          f"binding 4b legs: " + ", ".join(f"{k} {int((~s[k]).sum())}" for k in
                                           ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]) + " FAILs")
        P(f"      4a FAIL legs: " + ", ".join(f"{k} {int((~s[k]).sum())}" for k in ["A_H1", "A_H2", "A_DD"]))

    # ---------------------------------------------------------------- hypotheses
    P("\n## PRE-REGISTERED HYPOTHESES")
    H = []
    ent = []
    for panel in fixdf.panel.unique():
        g75 = grid[(grid.panel == panel) & (grid.ebar == 0.75)].sort_values("N")
        ent.append(olsslope(g75.N.values, g75.G.values) > 0)
    H.append(("H_ENTANGLE  the solved G RISES in N at EBAR=0.75 on BOTH panels",
              bool(all(ent)), f"{sum(ent)} of {len(ent)} panels positive"))
    sprd = []
    for panel in grid.panel.unique():
        u = grid[grid.panel == panel]
        sprd += [float(u[u.ebar == e].expo_full.max() - u[u.ebar == e].expo_full.min()) for e in EBARS]
    H.append((f"H_LEVEL     every iso-exposure row level to <= {LEVEL_TOL} of realised exposure",
              bool(max(sprd) <= LEVEL_TOL), f"max within-row spread {max(sprd):.5f} over {len(sprd)} rows"))
    bre = []
    for panel in grid.panel.unique():
        s = grid[(grid.panel == panel) & (grid.ebar == 0.75)].sort_values("N")
        bre.append(olsslope(s.N.values, np.abs(s.MaxDD.values)) > 0)
    H.append(("H_BREADTH   at LEVEL exposure |MaxDD| still RISES in N (breadth does NOT buy the DD leg)",
              bool(all(bre)), f"{sum(bre)} of {len(bre)} panels d|DD|/dN > 0 at EBAR=0.75"))
    nch = int((ok.gap_pp > 0).sum()) if len(ok) else 0
    H.append(("H_CHEAPER   breadth buys the DD more cheaply than cash at some cell (isoquant gap > 0)",
              bool(nch > 0), f"{nch} of {len(ok)} comparable cells, best {ok.gap_pp.max():+.3f} pp"
              if len(ok) else "no comparable cells"))
    H.append(("H_DOMINATE  some N > 20 cell dominates its own row's N=20 on BOTH CAGR and |MaxDD|",
              bool(domd.dominates.any()), f"{int(domd.dominates.sum())} of {len(domd)}"))
    newb = grid[grid.pass4b & ~grid.is_anchor]
    H.append(("H_4b        at least one NON-INCUMBENT cell passes all five 4b legs",
              bool(len(newb) > 0), f"{len(newb)} of {len(grid)} cells (anchor passes: "
              f"{int((grid.pass4b & grid.is_anchor).sum())})"))
    beat = int(r8.beats_anchor.sum())
    H.append(("H_R8        rule 8 reaches a cell beating the anchor OOS on a MAJORITY of choosers",
              bool(beat > len(r8) / 2), f"{beat} of {len(r8)}; mean d {r8.d_OOS_Sharpe.mean():+.4f}"))
    for name, okh, ev in H:
        P(f"   {'SUPPORTED' if okh else 'REFUTED  '}  {name}   [{ev}]")
    P(f"   HYPOTHESES {sum(1 for _, o, _ in H if o)} of {len(H)} SUPPORTED")

    # ---------------------------------------------------------------- verdict
    reach = r8[(r8.pass4b) & (r8.d_OOS_Sharpe > 0) & (~r8.picks_anchor)]
    verdict = ("KEEP (4b)" if len(reach) else ("PARK" if len(newb) else "KILL (capital), NO NEW BOOK"))
    P(f"\n## VERDICT: {verdict}  — 4a {int(grid.pass4a.sum())} of {len(grid)}, "
      f"4b {int(grid.pass4b.sum())} of {len(grid)} (of which "
      f"{int((grid.pass4b & grid.is_anchor).sum())} are the ANCHOR cell itself), "
      f"non-incumbent 4b {len(newb)}, rule-8-reachable non-incumbent 4b cells {len(reach)}")
    if len(newb):
        P("   4b PASSES THAT ARE NOT THE ANCHOR:")
        for _, x in newb.iterrows():
            P(f"      {x.panel} N={int(x.N)}/E{x.ebar:.2f} (G {x.G:.4f}, realised expo {x.expo_full:.4f}): "
              f"{x.CAGR:.2%} / {x.Sharpe:.4f} / {x.MaxDD:.2%}, halves {x.H1:.4f}/{x.H2:.4f}, "
              f"OOS Sharpe {x.OOS_Sharpe:.4f}"
              + ("   [REACHED by rule 8]" if ((r8.N == x.N) & (r8.ebar == x.ebar)
                                              & (r8.panel == x.panel)).any() else "   [not reached by rule 8]"))
    P(f"# runtime {time.time()-t0:.1f}s")

    dump(grid, "grid"); dump(fixdf, "fixedgross"); dump(isod, "isoquant")
    dump(domd, "dominance"); dump(r8, "walkforward"); dump(dd, "ddspan")
    dump(pd.DataFrame(gaterows), "gates"); dump(pd.DataFrame(benchrows), "bench")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
