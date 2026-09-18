#!/usr/bin/env python3
"""2026-09-18 lane B, QUEUE idea 1081 — is the COMMON-FACTOR DRAWDOWN reading of the n DIAL
TRUE on a SMALL-CAP PANEL?

QUESTION (QUEUE idea 1081, verbatim)
    idea 1071 found MaxDD worsens monotonically in n on U56 (-19.13% -> -22.98%) and B136
    (-20.74% -> -25.38%) while CAGR falls, and read it as the book's drawdowns being
    common-factor rather than idiosyncratic.  Small caps carry far more idiosyncratic
    variance, so if the reading is right the n dial should flatten or reverse on the sub-$2B
    panel.  Re-run the same n x cap grid on SMALL (dropping max_1d_move >= 1.0 per
    data/small_meta.csv) and report the sign of d(MaxDD)/dn.  Max 2 params (n, per-name cap).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two) — 1071's LADDERS, UNCHANGED
    1. N       in {20, 25, 30, 40}.   20 is the incumbent (936/1059/1064/1065's CAND20).
    2. CAPMULT k in {1.00, 1.25, 1.50, 2.00, INF}.  Per-name target weight
           w_i = min(g / n_sel, k * g / N),  residual -> CASH (never re-spread, no leverage).
    All 4 x 5 = 20 points are reported at EVERY panel.  Nothing else is tuned.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9).  The book itself is
    frozen at 936/1064/1071's construction: RAW three-leg composite of percentile ranks
    (21/252, 0/126, 0/63), NO vol scaler, gate = above 200d MA AND vol20 < 0.60, H = 126
    minimum hold, GROSS = 0.75, weekly decide / t+1 execution, 10 bps on traded notional,
    warm-up 260 days.  U56 and B136 are re-run to REPRODUCE 1071, not to re-tune it; SMALL is
    the only new measurement.

WHY THIS IS A REAL TEST AND NOT A RE-RUN — DECLARED BEFORE ANY NUMBER
    (a) 1071's reading is a CLAIM ABOUT THE RESIDUAL COVARIANCE of the held names: if the
        drawdown were idiosyncratic, holding 40 names instead of 20 would halve the
        idiosyncratic contribution and cut MaxDD.  It did the opposite on both large-cap
        panels.  The sub-$2B panel is the population where the idiosyncratic share is largest,
        so it is the sharpest available refutation site.
    (b) THE SIGN IS THE DELIVERABLE, NOT THE LEVEL.  Levels on SMALL are survivorship-inflated
        (rule 9 and data/SMALL_PANEL_README.md); a SLOPE IN N measured inside one panel is a
        difference between two books drawn from the SAME biased pool over the SAME tape, and
        the bias very largely cancels out of it.  Every 4b count on SMALL is an UPPER bound and
        is read as one.
    (c) THE MECHANISM IS MEASURED DIRECTLY, not inferred from the sign.  At cap = INF and
        N in {20, 40} this run reports the held book's MEAN PAIRWISE CORRELATION (trailing 63d,
        at every rebalance date) and its DIVERSIFICATION RATIO (weighted mean name vol / book
        vol).  If SMALL's held names are no less correlated than U56's, the queue's premise is
        false on this panel and a flat n dial there would mean something else.
    (d) A DD THAT RISES IN N WHILE VOL FALLS IN N IS NOT A DIVERSIFICATION STORY.  Realised
        annualised vol is reported at every cell precisely so the two can be separated.

PRE-REGISTERED HYPOTHESES, declared before the grid was read, scored as they fell:
  H_SIGN  REPRODUCTION: on U56 and B136 at cap=INF, |MaxDD| RISES with N (1071's finding).
  H_FLAT  THE QUEUE'S PREDICTION: on SMALL, d|MaxDD|/dN <= 0 at a MAJORITY of the 5 caps.
  H_CORR  THE PREMISE: SMALL's held-book mean pairwise correlation is BELOW U56's and B136's.
  H_VOL   on every panel, realised book VOL falls in N at cap=INF (so a rising DD is not a
          failure of diversification to reduce variance).
  H_4b    at least one SMALL cell passes every 4b leg.
  H_R8    rule 8 (choose the cell on warm-up..2016-12-31, read 2017-2026 ONCE) reaches a cell
          whose OOS Sharpe beats the do-nothing anchor (N=20, cap=INF) on a majority of panels.

PRE-DECLARED VERDICT RULE: KEEP (path 4b) only if a cell clears EVERY 4b leg AND rule 8
    reaches it AND its OOS Sharpe is above its panel's anchor.  A cell that clears 4b but is
    not reached is PARK at best.  4a is judged against the live RULES v2 book on the same
    panel.  Neither dial is re-tuned after reading; the ladders are 1071's.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  SMALL is a
    CURRENT sub-$2B screen (715 names, built 2026-09-11) containing only companies still
    listed, still public and still under $2B today — every name survived the whole sample by
    construction, the missing ones are exactly the failures a momentum book would have ridden
    down, and 2010-2015 is the least trustworthy stretch.  All three panels' LEVELS are
    optimistic; the SIGN OF d(MaxDD)/dN, the correlation contrast and every book-vs-book
    difference inside one panel are first-order immune.  SPY is joined to SMALL as a BENCHMARK
    COLUMN ONLY and is excluded from the selection set (gate G6); on U56/B136 it stays inside
    the selection set exactly as 936/1071 built it, so the anchor reproduces.
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

DATE, SLUG = "2026-09-18", "is-the-COMMON-FACTOR-DRAWDOWN-reading-of-the-n-DIAL-TRUE-on-a-SMALL-CAP-PANEL"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
COST, GROSS0, FREQ, HOLD = 10.0, 0.75, "W", 126
LEGS = [(21, 252), (0, 126), (0, 63)]           # CAND20, 936/1064/1071's construction
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

NS = [20, 25, 30, 40]                            # dial 1 — 1071's ladder
CAPS = [1.00, 1.25, 1.50, 2.00, np.inf]          # dial 2 — 1071's ladder
CORR_NS = [20, 40]                               # mechanism probe (cap=INF only)

# committed cross-run anchors (tape vintages differ; tolerances stated at each gate)
A936_WH126 = (0.155787, 1.139701, -0.191276)     # 936/1071 U56 CAND20 W/H126 0.75 10bps
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1071_INF = {"U56": (-0.1913, -0.2298, 0.1558, 0.1346),   # (DD@20, DD@40, CAGR@20, CAGR@40)
             "B136": (-0.2074, -0.2538, np.nan, np.nan)}
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------------------------------ metrics (1071's, verbatim)
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
    """Peak and trough dates of the deepest drawdown of the post-warm-up path."""
    rr = np.asarray(r, float)[warm]
    ii = idx[warm]
    eq = np.cumprod(1.0 + rr)
    pk = np.maximum.accumulate(eq)
    dd = eq / pk - 1.0
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


# ------------------------------------------------------------------ fast runner (1071's, gated)
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


# ------------------------------------------------------------------ the book (1071's, verbatim)
def build(rank_key, elig, priced, reb, N, cap, H, T, K, gross):
    """Target weights under MIN HOLD H, slot count N, per-name cap multiple `cap`.
    w_i = min(gross/n_sel, cap*gross/N); residual -> CASH."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb, gross_by_reb, sel_by_reb = [], [], []
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
        sel_by_reb.append(sel)
        if len(sel):
            w = min(gross / len(sel), per_cap)
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = w
            gross_by_reb.append(w * len(sel))
        else:
            gross_by_reb.append(0.0)
    return W, np.array(nsel_by_reb), np.array(gross_by_reb), sel_by_reb


def mech(px_inv, cols_all, inv):
    """936/1064/1071's selection score (higher better) and gate, widened to the full column
    space with non-investable columns permanently ineligible."""
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


# ------------------------------------------------------------------ mechanism probe
def held_corr(rets, sel_by_reb, reb, win=63, first=WARMUP):
    """Mean off-diagonal pairwise correlation of the SELECTED names' trailing `win` daily
    returns, and the diversification ratio (equal-weight mean name vol / book vol), averaged
    over post-warm-up rebalance dates."""
    cs, drs = [], []
    for t, sel in zip(reb, sel_by_reb):
        if t < first or len(sel) < 2 or t < win:
            continue
        R = rets[t - win:t][:, sel]
        sd = R.std(axis=0, ddof=1)
        if not np.all(np.isfinite(sd)) or np.any(sd <= 0):
            ok = np.isfinite(sd) & (sd > 0)
            R, sd = R[:, ok], sd[ok]
            if R.shape[1] < 2:
                continue
        C = np.corrcoef(R, rowvar=False)
        m = ~np.eye(C.shape[0], dtype=bool)
        cs.append(float(np.nanmean(C[m])))
        bk = R.mean(axis=1)
        b = bk.std(ddof=1)
        if b > 0:
            drs.append(float(sd.mean() / b))
    return (float(np.mean(cs)) if cs else np.nan,
            float(np.mean(drs)) if drs else np.nan, len(cs))


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# {DATE} lane B, QUEUE idea 1081 — {SLUG}")
    P(f"# 2 tuned dials (1071's ladders, unchanged): N {NS} x CAPMULT "
      f"{['INF' if not np.isfinite(c) else f'{c:.2f}' for c in CAPS]}.  ALL 20 points reported per panel.")
    P(f"# frozen book: RAW composite {LEGS}, no vol scaler, above-200d AND vol20 < {MAXVOL}, "
      f"H={HOLD}, GROSS={GROSS0}, weekly, {COST:.0f} bps, t+{LAG}, warm-up {WARMUP}")
    P("# reported-not-dials: PANEL {U56, B136, SMALL}.  U56/B136 REPRODUCE 1071; SMALL is the test.")
    P("# DECLARED BEFORE ANY NUMBER: the SIGN of d|MaxDD|/dN inside one panel is the deliverable;")
    P("#   SMALL's LEVELS are survivorship-inflated and every 4b count on it is an UPPER bound.")
    P("")

    rows, ladder, mechrows, r8rows, gaterows, benchrows = [], [], [], [], [], []
    gates: dict[str, tuple] = {}

    # ---------------------------------------------------------------- panels
    panels = []
    px_u = load_universe().dropna(how="all").ffill()
    panels.append(("U56", px_u, list(px_u.columns)))
    px_b = load_universe(broad=True).dropna(how="all").ffill()
    panels.append((f"B{px_b.shape[1]}", px_b, list(px_b.columns)))
    px_s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in px_s.columns if c != "SPY" and c not in bad]
    P(f"# SMALL panel: {px_s.shape[1]-1} priced names, {len(bad & set(px_s.columns))} dropped for "
      f"max_1d_move >= 1.0 -> {len(inv_s)} investable; SPY is a BENCHMARK COLUMN, never selectable")
    panels.append((f"SMALL{len(inv_s)}", px_s, inv_s))

    for panel, px, inv in panels:
        cols = list(px.columns)
        idx = px.index
        K = len(cols)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        reb = np.flatnonzero(mk)
        warm, ins, oos = windows(idx)
        sc, elig = mech(px[inv], cols, inv)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        P(f"\n## {panel}: {K} columns ({len(inv)} investable), {len(idx)} days "
          f"{idx[0].date()}..{idx[-1].date()}, {len(reb)} rebalance dates")
        P(f"   SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2  full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  halves "
          f"{lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb), dict(panel=panel, series="RULESv2", **lb)]

        if panel == "U56":
            W, _, _, _ = build(rank_key, elig, priced, reb, 20, np.inf, HOLD, len(idx), K, GROSS0)
            eng = backtest(px, pd.DataFrame(W, index=idx, columns=cols), cost_bps=COST, freq=FREQ)["returns"].values
            g, tn, _ = nrun(rets, lagmat(W), np.roll(mk, LAG))
            fast = g - tn * COST / 1e4
            d1 = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N20, k=INF)"] = (d1, d1 < 1e-12)
            m = fmet(fast[warm])
            d2 = max(abs(m[0] - A936_WH126[0]), abs(m[1] - A936_WH126[1]), abs(m[2] - A936_WH126[2]))
            gates["G2 CROSS-RUN vs 936/1071 committed W/H126 triple (tape vintage differs)"] = (d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-3)
            d4 = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G4 live RULES v2 MaxDD == committed -12.05%"] = (d4, d4 < 5e-3)
        if panel.startswith("SMALL"):
            si = cols.index("SPY")
            gates["G6 SPY never eligible / never scored on SMALL"] = (
                float(elig[:, si].sum() + np.isfinite(rank_key[:, si]).sum()), True)
            gates["G6"] = (float(elig[:, si].sum() + np.isfinite(rank_key[:, si]).sum()),
                           elig[:, si].sum() == 0 and not np.isfinite(rank_key[:, si]).any())
            del gates["G6 SPY never eligible / never scored on SMALL"]

        maxg = 0.0
        for N in NS:
            for cap in CAPS:
                W, nsel, grs, selby = build(rank_key, elig, priced, reb, N, cap, HOLD, len(idx), K, GROSS0)
                g, tn, _ = nrun(rets, lagmat(W), np.roll(mk, LAG))
                r = g - tn * COST / 1e4
                b = blocks(r, warm, ins, oos)
                l4b, l4a = legs_4b(b, sb), legs_4a(b, lb)
                capname = "INF" if not np.isfinite(cap) else f"{cap:.2f}"
                maxg = max(maxg, float(grs.max()))
                rows.append(dict(panel=panel, N=N, cap=capname,
                                 bind_share=float((grs < GROSS0 - 1e-12).mean()),
                                 mean_gross=float(grs.mean()), mean_nsel=float(nsel.mean()),
                                 turnover=float(tn[warm].sum() / (warm.sum() / 252.0)), **b,
                                 pass4b=all(l4b.values()), fail4b=failed(l4b),
                                 pass4a=all(l4a.values()), fail4a=failed(l4a), **l4b, **l4a))
                if cap == np.inf and N in CORR_NS:
                    c_, dr_, nobs = held_corr(rets, selby, reb)
                    pkd, trd, dpt = ddspan(r, idx, warm)
                    mechrows.append(dict(panel=panel, N=N, mean_pair_corr=c_, div_ratio=dr_,
                                         n_dates=nobs, book_vol=b["Vol"], MaxDD=b["MaxDD"],
                                         CAGR=b["CAGR"], mean_nsel=float(nsel.mean()),
                                         dd_peak=pkd, dd_trough=trd, dd_depth=dpt))
        gates[f"G7 no leverage on {panel} (max target gross <= {GROSS0})"] = (maxg, maxg <= GROSS0 + 1e-12)

        u = pd.DataFrame([x for x in rows if x["panel"] == panel])
        if panel == "U56":
            bind = u[u.cap == "1.00"]["bind_share"].max()
            gates["G5 cap dial is LIVE (k=1.00 binds on >5% of U56 rebalance dates)"] = (bind, bind > 0.05)
        inc = float(u[u.cap == "1.00"].bind_share.mean() - u[u.cap == "INF"].bind_share.mean())
        gates[f"G9 cap dial on {panel}: genuine bind increment over the breadth floor (pp)"] = (
            f"{100*inc:.2f}pp{'  -> INERT, reported as inert not as a null' if inc < 1e-9 else ''}", True)
        full = u[u.cap == "INF"].sort_values("N")
        gates[f"G8 N dial is LIVE on {panel} (mean slots filled rises with N)"] = (
            f"{full.mean_nsel.iloc[0]:.1f}->{full.mean_nsel.iloc[-1]:.1f}",
            full.mean_nsel.iloc[-1] > full.mean_nsel.iloc[0] + 1.0)

        # ---- the ladder: sign of d|MaxDD|/dN at every cap ------------------------------------
        P(f"   {'N':>3} {'cap':>4} {'bind%':>6} {'nsel':>5} {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} "
          f"{'Vol':>6} {'turn':>5} {'OOS_S':>7} {'4b':>3} {'4a':>3}  fail4b")
        for _, x in u.iterrows():
            P(f"   {int(x.N):3d} {x.cap:>4} {x.bind_share:6.1%} {x.mean_nsel:5.1f} {x.CAGR:7.2%} "
              f"{x.Sharpe:7.4f} {x.MaxDD:8.2%} {x.Vol:6.2%} {x.turnover:5.2f} {x.OOS_Sharpe:7.4f} "
              f"{'Y' if x.pass4b else 'n':>3} {'Y' if x.pass4a else 'n':>3}  {x.fail4b}")
        for capname in ["1.00", "1.25", "1.50", "2.00", "INF"]:
            s = u[u.cap == capname].sort_values("N")
            sl_dd = olsslope(s.N.values, np.abs(s.MaxDD.values)) * 100.0     # pp of |DD| per name
            sl_cg = olsslope(s.N.values, s.CAGR.values) * 100.0
            sl_vol = olsslope(s.N.values, s.Vol.values) * 100.0
            sl_sh = olsslope(s.N.values, s.Sharpe.values)
            ladder.append(dict(panel=panel, cap=capname,
                               dDD_dN_pp_per_name=sl_dd, dCAGR_dN_pp_per_name=sl_cg,
                               dVol_dN_pp_per_name=sl_vol, dSharpe_dN=sl_sh,
                               DD_20=s.MaxDD.iloc[0], DD_40=s.MaxDD.iloc[-1],
                               d_DD_20_40_pp=100.0 * (abs(s.MaxDD.iloc[-1]) - abs(s.MaxDD.iloc[0])),
                               CAGR_20=s.CAGR.iloc[0], CAGR_40=s.CAGR.iloc[-1],
                               Vol_20=s.Vol.iloc[0], Vol_40=s.Vol.iloc[-1],
                               monotone_up=bool(np.all(np.diff(np.abs(s.MaxDD.values)) > 0)),
                               monotone_down=bool(np.all(np.diff(np.abs(s.MaxDD.values)) < 0)),
                               rankcorr_N_DD=rankcorr(s.N.values, np.abs(s.MaxDD.values))))

        # ---- RULE 8: choose on IS only, read OOS once ----------------------------------------
        anchor = u[(u.N == 20) & (u.cap == "INF")].iloc[0]
        for cname, key, asc in [("C_ISSHARPE", "IS_Sharpe", False), ("C_ISDD", "IS_MaxDD", False),
                                ("C_ISCAGR", "IS_CAGR", False)]:
            v = u[key].values.copy()
            if key == "IS_MaxDD":
                v = -np.abs(v)                    # least deep IS drawdown
            pick = u.iloc[int(np.nanargmax(v))]
            r8rows.append(dict(panel=panel, chooser=cname, N=int(pick.N), cap=pick.cap,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               anchor_OOS_Sharpe=anchor.OOS_Sharpe, anchor_OOS_MaxDD=anchor.OOS_MaxDD,
                               anchor_OOS_CAGR=anchor.OOS_CAGR,
                               d_OOS_Sharpe=pick.OOS_Sharpe - anchor.OOS_Sharpe,
                               d_OOS_MaxDD_pp=100.0 * (abs(pick.OOS_MaxDD) - abs(anchor.OOS_MaxDD)),
                               spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_CAGR=sb["OOS_CAGR"],
                               spy_OOS_MaxDD=sb["OOS_MaxDD"], live_OOS_Sharpe=lb["OOS_Sharpe"],
                               beats_anchor=bool(pick.OOS_Sharpe > anchor.OOS_Sharpe),
                               beats_spy=bool(pick.OOS_Sharpe > sb["OOS_Sharpe"]),
                               rc_Sharpe_IS_OOS=rankcorr(u.IS_Sharpe.values, u.OOS_Sharpe.values),
                               rc_absDD_IS_OOS=rankcorr(np.abs(u.IS_MaxDD.values), np.abs(u.OOS_MaxDD.values)),
                               pass4b=bool(pick.pass4b)))

    grid = pd.DataFrame(rows)
    lad = pd.DataFrame(ladder)
    mdf = pd.DataFrame(mechrows)
    r8 = pd.DataFrame(r8rows)

    # ---------------------------------------------------------------- gates
    P("\n## GATES (printed before any hypothesis is scored)")
    npass = 0
    for k, (v, ok) in gates.items():
        npass += bool(ok)
        vs = v if isinstance(v, str) else f"{v:.3e}" if isinstance(v, float) and abs(v) < 1 else f"{v}"
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: {vs}")
        gaterows.append(dict(gate=k, value=str(v), pass_=bool(ok)))
    P(f"   GATES {npass} of {len(gates)} PASS")

    # ---------------------------------------------------------------- the answer
    P("\n## THE LADDER — sign of d|MaxDD|/dN (pp of drawdown per extra name), every cap")
    P(f"   {'panel':>10} {'cap':>4} {'dDD/dN':>8} {'DD@20':>8} {'DD@40':>8} {'d20-40':>8} "
      f"{'dCAGR/dN':>9} {'dVol/dN':>8} {'dSh/dN':>8} {'mono':>6} {'rc(N,DD)':>9}")
    for _, x in lad.iterrows():
        mono = "UP" if x.monotone_up else ("DOWN" if x.monotone_down else "-")
        P(f"   {x.panel:>10} {x.cap:>4} {x.dDD_dN_pp_per_name:+8.4f} {x.DD_20:8.2%} {x.DD_40:8.2%} "
          f"{x.d_DD_20_40_pp:+8.2f} {x.dCAGR_dN_pp_per_name:+9.4f} {x.dVol_dN_pp_per_name:+8.4f} "
          f"{x.dSharpe_dN:+8.4f} {mono:>6} {x.rankcorr_N_DD:+9.2f}")

    P("\n## THE MECHANISM — how correlated are the names each panel actually holds? (cap=INF)")
    P(f"   {'panel':>10} {'N':>3} {'meanPairCorr':>13} {'DivRatio':>9} {'bookVol':>8} {'MaxDD':>8} {'CAGR':>7} {'dates':>6}")
    for _, x in mdf.iterrows():
        P(f"   {x.panel:>10} {int(x.N):3d} {x.mean_pair_corr:13.4f} {x.div_ratio:9.3f} "
          f"{x.book_vol:8.2%} {x.MaxDD:8.2%} {x.CAGR:7.2%} {int(x.n_dates):6d}")

    pu = [p for p in grid.panel.unique() if p.startswith("U")][0]
    pb = [p for p in grid.panel.unique() if p.startswith("B")][0]
    ps = [p for p in grid.panel.unique() if p.startswith("SMALL")][0]
    c_s = mdf[mdf.panel == ps].mean_pair_corr.mean()
    c_u = mdf[mdf.panel == pu].mean_pair_corr.mean()
    c_b = mdf[mdf.panel == pb].mean_pair_corr.mean()

    P("\n## THE DRAWDOWN EPISODE ITSELF (cap=INF) — is the deepest trough the SAME event at N=20 and N=40?")
    for _, x in mdf.iterrows():
        P(f"   {x.panel:>10} N={int(x.N):2d}  peak {x.dd_peak}  ->  trough {x.dd_trough}  {x.dd_depth:8.2%}")

    P("\n## POST-HOC READING, MEASURED NOT PREDICTED (labelled as such; it is NOT a pre-registered")
    P("##   hypothesis and no dial was moved to obtain it): the SLOPE's MAGNITUDE, absolute and")
    P("##   relative to each panel's own DD@20, beside the correlation of the names it holds.")
    P(f"   {'panel':>10} {'dDD/dN(INF)':>12} {'d(20->40) pp':>13} {'as % of DD@20':>14} {'meanPairCorr':>13} {'DivRatio':>9}")
    for p_ in [pu, pb, ps]:
        z = lad[(lad.panel == p_) & (lad.cap == "INF")].iloc[0]
        mm = mdf[mdf.panel == p_]
        P(f"   {p_:>10} {z.dDD_dN_pp_per_name:+12.4f} {z.d_DD_20_40_pp:+13.2f} "
          f"{100*z.d_DD_20_40_pp/(100*abs(z.DD_20)):14.2f} {mm.mean_pair_corr.mean():13.4f} "
          f"{mm.div_ratio.mean():9.3f}")
    zu = lad[(lad.panel == pu) & (lad.cap == "INF")].iloc[0].dDD_dN_pp_per_name
    zb = lad[(lad.panel == pb) & (lad.cap == "INF")].iloc[0].dDD_dN_pp_per_name
    zs = lad[(lad.panel == ps) & (lad.cap == "INF")].iloc[0].dDD_dN_pp_per_name
    P(f"   SLOPE RATIO U56/SMALL {zu/zs:.1f}x,  B/SMALL {zb/zs:.1f}x   against a held-book CORRELATION"
      f" ratio of {c_u/c_s:.2f}x / {c_b/c_s:.2f}x")

    P("\n## RULE 8 — cell chosen on warm-up..2016-12-31 only, 2017-2026 read ONCE")
    P(f"   {'panel':>10} {'chooser':>10} {'pick':>10} {'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8} "
      f"{'d vs anchor':>11} {'>SPY':>5} {'rc(Sh)':>7} {'rc(|DD|)':>8}")
    for _, x in r8.iterrows():
        P(f"   {x.panel:>10} {x.chooser:>10} {f'N{int(x.N)}/{x.cap}':>10} {x.OOS_CAGR:9.2%} "
          f"{x.OOS_Sharpe:8.4f} {x.OOS_MaxDD:8.2%} {x.d_OOS_Sharpe:+11.4f} "
          f"{'Y' if x.beats_spy else 'n':>5} {x.rc_Sharpe_IS_OOS:+7.2f} {x.rc_absDD_IS_OOS:+8.2f}")

    P("\n## KEEP PATHS, all 60 cells")
    for p in grid.panel.unique():
        s = grid[grid.panel == p]
        P(f"   {p}: 4a {int(s.pass4a.sum())} of {len(s)}   4b {int(s.pass4b.sum())} of {len(s)}   "
          f"binding 4b legs: " + ", ".join(f"{k} {int((~s[k]).sum())}" for k in
                                           ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]) + " FAILs")

    # ---------------------------------------------------------------- hypotheses
    P("\n## PRE-REGISTERED HYPOTHESES")
    H = []
    uinf = lad[(lad.cap == "INF")].set_index("panel")
    H.append(("H_SIGN  REPRODUCTION: |MaxDD| RISES with N at cap=INF on U56 AND B136",
              bool(uinf.loc[pu, "dDD_dN_pp_per_name"] > 0 and uinf.loc[pb, "dDD_dN_pp_per_name"] > 0),
              f"{pu} {uinf.loc[pu,'dDD_dN_pp_per_name']:+.4f} pp/name, {pb} {uinf.loc[pb,'dDD_dN_pp_per_name']:+.4f}"))
    sm = lad[lad.panel == ps]
    nflat = int((sm.dDD_dN_pp_per_name <= 0).sum())
    H.append(("H_FLAT  THE QUEUE'S PREDICTION: d|MaxDD|/dN <= 0 at a MAJORITY of caps on SMALL",
              bool(nflat >= 3), f"{nflat} of {len(sm)} caps <= 0"))
    H.append(("H_CORR  THE PREMISE: SMALL's held names are LESS correlated than U56's and B136's",
              bool(c_s < c_u and c_s < c_b), f"SMALL {c_s:.4f} vs U56 {c_u:.4f} / B {c_b:.4f}"))
    volneg = int((lad[lad.cap == "INF"].dVol_dN_pp_per_name < 0).sum())
    H.append(("H_VOL   book VOL falls in N at cap=INF on EVERY panel",
              bool(volneg == 3), f"{volneg} of 3 panels negative"))
    n4b = int(grid[grid.panel == ps].pass4b.sum())
    H.append(("H_4b    at least one SMALL cell passes every 4b leg", bool(n4b > 0), f"{n4b} of 20"))
    beat = int(r8.beats_anchor.sum())
    H.append(("H_R8    rule 8 reaches a cell beating the do-nothing anchor OOS on a majority of panels",
              bool(beat > len(r8) / 2), f"{beat} of {len(r8)} choosers beat anchor; mean d "
              f"{r8.d_OOS_Sharpe.mean():+.4f}"))
    for name, ok, ev in H:
        P(f"   {'SUPPORTED' if ok else 'REFUTED  '}  {name}   [{ev}]")
    P(f"   HYPOTHESES {sum(1 for _, o, _ in H if o)} of {len(H)} SUPPORTED")

    # ---------------------------------------------------------------- verdict
    reachable = r8[(r8.pass4b) & (r8.d_OOS_Sharpe > 0)]
    # A 4b pass at N = 20 IS the incumbent cell (or one of its four cap clones), not a new book:
    # counted, named, and excluded from KEEP/PARK by the rule declared in the docstring.
    newb = grid[grid.pass4b & (grid.N != 20)]
    verdict = ("KEEP (4b)" if len(reachable)
               else ("PARK" if len(newb) else "KILL (capital), NO NEW BOOK"))
    P(f"\n## VERDICT: {verdict}  — 4a {int(grid.pass4a.sum())} of {len(grid)}, "
      f"4b {int(grid.pass4b.sum())} of {len(grid)} (of which {int((grid.pass4b & (grid.N == 20)).sum())} "
      f"are the INCUMBENT N=20 cell or its cap clones), rule-8 reachable 4b cells {len(reachable)}")
    if len(newb):
        P("   4b PASSES THAT ARE NOT THE INCUMBENT, none of them reached by rule 8:")
        for _, x in newb.iterrows():
            P(f"      {x.panel} N={int(x.N)}/{x.cap}: {x.CAGR:.2%} / {x.Sharpe:.4f} / {x.MaxDD:.2%}, "
              f"OOS Sharpe {x.OOS_Sharpe:.4f}")
    P(f"# runtime {time.time()-t0:.1f}s")

    dump(grid, "grid"); dump(lad, "ladder"); dump(mdf, "mech"); dump(r8, "walkforward")
    dump(pd.DataFrame(gaterows), "gates"); dump(pd.DataFrame(benchrows), "bench")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
