#!/usr/bin/env python3
"""Idea 1162 (cloud lane, 2026-09-17) — is MONOTONICITY of a DIAL a PUBLISHABLE STAMP,
or does it cost a run a SECOND GRID?

Idea 1154 found 40.5% of NON-MONOTONE cells still pick an ENDPOINT and 88.2% of those
preferences are under one SD.  The record therefore reads "it picked the end" as "the dial
saturates" across hundreds of committed argmax claims, and that reading is unsafe in both
directions: a non-monotone ladder can pick an end by noise, and a monotone ladder's
interior pick is not an optimum at all.  The queue asks for a PRICE on a one-line stamp
("is the statistic monotone over this dial: rho and spread") against the record's own
argmax claims: how many claims CHANGE READING, and what does the stamp COST a run that has
already computed the ladder.

WHAT THIS RUN CAN AND CANNOT DO, said plainly up front.  It cannot re-run the record's
committed claims one by one: their cells are not resolvable from prose (idea 1098 found
R_STRICT resolves 82 of 2,088 cost claims; idea 1149 is still open on exactly this).  So
this run does NOT census LEADERBOARD.md text.  It builds a FRESH, FULLY SPECIFIED
population of argmax claims of the same SHAPE the record commits — 4 dials x 4 objectives
x 3 panels = 48 ladders, 120 books, every rung published — and prices the stamp on that.
The number this reports is therefore "how often the stamp changes the reading of an argmax
claim of this shape", not "how many of the record's sentences are wrong".  Stated again in
the memo and in the leaderboard row.

THREE SEPARABLE PIECES OF WORK:
  (A) THE STAMP'S READING.  For all 48 ladders x 4 objectives, is the argmax an endpoint,
      is the ladder monotone (Spearman rho over the dial), and is the argmax's preference
      over its runner-up and over the best endpoint resolvable against the rung's own
      bootstrap SD.  Publishes 1154's 2x2 (endpoint x monotone) on a fresh population.
  (B) THE COST.  Wall-clock seconds and EXTRA BOOK RUNS for each stamp form against the
      ladder the run already has, and against the SECOND GRID the queue names as the
      alternative.  A stamp that needs a second grid is not a stamp.
  (C) THE PRICE LEG, which is what decides capital: is a stamp-aware CHOOSER better OUT OF
      SAMPLE than a plain argmax?  Rule 8 — three choosers read 2009-2016 ONLY, their
      picks are evaluated on the untouched 2017-2026, against the live RULES v2 baseline
      and SPY, on BOTH KEEP paths.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  STAMP     {S_NONE, S_RHO, S_MARGIN, S_BOTH}
  CLAIMSET  {C_SHARPE, C_CAGR, C_MAXDD, C_TENT}   (the objective the argmax is taken on)
= 16 cells, EVERY ONE PUBLISHED in `.stamp.csv`.  PANEL {U56, B136, SMALL} is not a dial —
it is the population, and all three are published everywhere.  DIAL {GROSS, N, H, MAXVOL}
is not a dial either: it is the object under census and all four are published.  The
monotone threshold tau is FROZEN at 0.90 inside S_RHO/S_BOTH and is NOT tuned; the full
tau sweep is published in `.tau.csv` as declared sensitivity, and no verdict is read off it.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1150/1154/1159/1161's construction:
CAND20 legs [(21,252),(0,126),(0,63)], max_vol 0.60, min hold 126, N=20, gross 0.75,
cadence W, cost 10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, zero cash.

SURVIVORSHIP: B136 and SMALL are CURRENT constituents only (PROTOCOL rule 9 /
data/SMALL_PANEL_README.md).  SMALL additionally drops every ticker with
max_1d_move >= 1.0 in data/small_meta.csv before anything else is computed.  No result
here should be read as a live-tradable edge on those panels; they are breadth controls.

Writes: .gates.csv .ladder.csv .stamp.csv .tau.csv .cost.csv .walkforward.csv .console.txt
Deterministic (all bootstraps seeded), standalone, no network.  Does not modify RULES.md /
PROTOCOL.md / scan.py / bot.py / baseline.py / engine.py.
"""
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "is-MONOTONICITY-of-a-DIAL-a-PUBLISHABLE-STAMP-or-does-it-cost-a-run-a-second-grid"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
LOG = []

LAG, WARMUP = 1, 260
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, COST0, MAXVOL0 = 0.75, "W", 126, 20, 10.0, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
START = "2008-01-01"

TAU = 0.90            # FROZEN inside the stamp; the sweep in .tau.csv is sensitivity only
SDBAR = 1.0           # "under one SD" — 1154's own unit, FROZEN
BOOT_B, BOOT_L, SEED = 400, 63, 20260917

# ------------------------------------------------------------------ THE LADDERS (census)
DIALS = {
    "GROSS":  ("gross",  [round(0.20 + 0.05 * i, 3) for i in range(17)]),
    "N":      ("N",      [3, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50]),
    "H":      ("H",      [21, 42, 63, 126, 189, 252]),
    "MAXVOL": ("maxvol", [0.30, 0.40, 0.50, 0.60, 0.80, 1.00]),
}
DEFAULT = {"gross": GROSS0, "N": N0, "H": HOLD0, "maxvol": MAXVOL0}

# ------------------------------------------------------------------ THE TWO DIALS
STAMPS = ["S_NONE", "S_RHO", "S_MARGIN", "S_BOTH"]
CLAIMSETS = ["C_SHARPE", "C_CAGR", "C_MAXDD", "C_TENT"]
OBJ_OF = {"C_SHARPE": "Sharpe", "C_CAGR": "CAGR", "C_MAXDD": "negMaxDD", "C_TENT": "tent"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------- 1082/../1161's fast runner and book, VERBATIM
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


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (comp * (0.5 + 0.5 * above.astype(float))).values, above.values, vol20.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
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


def prep(px):
    idx = px.index
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    sc, above, vol20 = mech(px)
    return dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                warm=warm, ins=ins, oos=oos, sc=sc, above=above, vol20=vol20,
                spy=px["SPY"].pct_change().fillna(0.0).values,
                mk=rebalance_mask(idx, FREQ0).values)


def run_cell(d, gross=GROSS0, N=N0, H=HOLD0, maxvol=MAXVOL0):
    mk = d["mk"]
    mkl = np.roll(mk, LAG)
    mkl[:LAG] = False
    reb = np.flatnonzero(mk)
    el = d["above"] & (d["vol20"] < maxvol)
    W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    g, t = nrun(d["rets"], Wl, mkl)
    return g - t * COST0 / 1e4


def blocks_m(r, d):
    rr = r[d["warm"]]
    c, s, dd = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[d["oos"]])
    ic, is_, idd = fmet(r[d["ins"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return dict(L_H1=b["H1"] > sb["H1"], L_H2=b["H2"] > sb["H2"],
                L_OOS=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                L_DD=abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"]),
                L_CAGR=b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])


def legs_4b_oos(b, sb):
    return dict(O_S=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                O_DD=abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"]),
                O_CAGR=b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])


def legs_4a(b, lbm):
    return dict(A_H1=b["H1"] > lbm["H1"], A_H2=b["H2"] > lbm["H2"], A_DD=b["MaxDD"] >= lbm["MaxDD"])


def tent_is(m, sb):
    """4b's IS margin, min over legs, in each leg's own relative unit (1150/1154's object)."""
    cap = DD_CAP * abs(sb["IS_MaxDD"])
    flo = CAGR_FLOOR * sb["IS_CAGR"]
    return min((m["IS_Sharpe"] - sb["IS_Sharpe"]) / abs(sb["IS_Sharpe"]),
               (cap - abs(m["IS_MaxDD"])) / cap,
               (m["IS_CAGR"] - flo) / abs(flo))


def tent_full(m, sb):
    cap = DD_CAP * abs(sb["MaxDD"])
    flo = CAGR_FLOOR * sb["CAGR"]
    return min((m["Sharpe"] - sb["Sharpe"]) / abs(sb["Sharpe"]),
               (cap - abs(m["MaxDD"])) / cap,
               (m["CAGR"] - flo) / abs(flo))


# --------------------------------------------------------------- THE STAMP'S TWO HALVES
def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    rx = pd.Series(x[ok]).rank().values
    ry = pd.Series(y[ok]).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def boot_draws(rets_mat, statfn, B=BOOT_B, L=BOOT_L, seed=SEED):
    """Moving-block bootstrap draws of `statfn` for every column of rets_mat, on SHARED
    block origins across columns.  Returns the full (B x C) draw matrix.

    SHARING THE DRAWS IS THE POINT.  Two adjacent rungs of one ladder are the SAME book
    one parameter apart and are enormously correlated; the noise unit for a PREFERENCE
    between them is the SD of their DIFFERENCE on common draws, NOT sqrt(sd_a^2+sd_b^2),
    which treats them as independent and inflates the bar until every argmax is
    'unresolved' by construction.  This run's first cut made exactly that error and read
    48 of 48 claims unresolved; the paired unit below is the correction.  Marginal SDs are
    still published (they are the right unit for a SPREAD), but no preference uses them."""
    T, C = rets_mat.shape
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / L))
    out = np.empty((B, C))
    ar = np.arange(L)
    for b in range(B):
        st = rng.integers(0, T - L + 1, size=nb)
        idx = (st[:, None] + ar[None, :]).ravel()[:T]
        samp = rets_mat[idx]
        for c in range(C):
            out[b, c] = statfn(samp[:, c])
    return out


def boot_sd(rets_mat, statfn, B=BOOT_B, L=BOOT_L, seed=SEED):
    return boot_draws(rets_mat, statfn, B, L, seed).std(axis=0, ddof=1)


def analytic_sharpe_sd(r):
    """Lo (2002) iid SE of the ANNUALISED Sharpe — the ZERO-EXTRA-COST noise unit.
    SE(S_ann) = sqrt((1 + S_ann^2/(2*252)) / n_years), n_years = T/252."""
    s = fsharpe(r)
    ny = len(r) / 252.0
    return float(np.sqrt((1.0 + 0.5 * s * s / 252.0) / ny))


def pair_sds(draws, a):
    """SD of (rung a - rung c) over COMMON bootstrap draws, for every c. The paired unit."""
    d = draws - draws[:, [a]]
    s = d.std(axis=0, ddof=1)
    return s


def stamp_read(vals, draws, dial_vals, tau=TAU, sdbar=SDBAR):
    """The whole stamp, from a ladder that has ALREADY been computed.
    Returns the reading each stamp form gives of this ladder's argmax claim."""
    v = np.asarray(vals, float)
    n = len(v)
    sds = draws.std(axis=0, ddof=1)
    a = int(np.nanargmax(v))
    endpoint = a in (0, n - 1)
    order = np.argsort(-v)
    runner = int(order[1])
    ps = pair_sds(draws, a)
    margin_runner = (v[a] - v[runner]) / ps[runner] if ps[runner] > 0 else np.inf
    best_end = 0 if v[0] >= v[-1] else n - 1
    margin_end = ((v[a] - v[best_end]) / ps[best_end]) if ps[best_end] > 0 else 0.0
    rho = spearman(np.asarray(dial_vals, float), v)
    mono = bool(abs(rho) >= tau)
    spread_sd = (np.nanmax(v) - np.nanmin(v)) / float(np.nanmean(sds)) if np.nanmean(sds) > 0 else np.nan
    return dict(argmax_i=a, argmax=dial_vals[a], endpoint=endpoint, rho=rho, monotone=mono,
                runner=dial_vals[runner], margin_runner=float(margin_runner),
                margin_end=float(margin_end), spread_sd=float(spread_sd),
                marg_sd_mean=float(np.nanmean(sds)), pair_sd_runner=float(ps[runner]),
                resolved=bool(margin_runner >= sdbar))


def within_1sd_set(vals, draws, sdbar=SDBAR):
    v = np.asarray(vals, float)
    a = int(np.nanargmax(v))
    ps = pair_sds(draws, a)
    keep = np.flatnonzero((v[a] - v) < sdbar * np.where(ps > 0, ps, np.inf))
    return keep if len(keep) else np.array([a])


def main():
    t_run0 = time.time()
    P("=" * 100)
    P(f"IDEA 1162 (cloud) {DATE} — is MONOTONICITY of a DIAL a PUBLISHABLE STAMP,")
    P("                    or does it cost a run a SECOND GRID?")
    P("=" * 100)
    P("")
    P("WHAT IS MEASURED, AND ON WHAT.  Not the record's prose (its claim cells are not")
    P("resolvable from prose — 1098's R_STRICT: 82 of 2,088; idea 1149 still open).  A")
    P("FRESH population of argmax claims of the SAME SHAPE the record commits:")
    P("  3 panels x 4 dials = 12 ladders, 40 rungs each panel, 120 books, ALL published;")
    P("  x 4 objectives = 48 argmax claims, ALL published.")
    P("Read every share below as 'of argmax claims of this shape', NOT 'of the record'.")
    P("")
    P("THE TWO TUNED PARAMETERS (rule 4): STAMP {S_NONE,S_RHO,S_MARGIN,S_BOTH} x")
    P("CLAIMSET {C_SHARPE,C_CAGR,C_MAXDD,C_TENT} = 16 cells, all published.")
    P(f"tau FROZEN at {TAU}, SD bar FROZEN at {SDBAR} (1154's own unit); tau sweep is")
    P("declared SENSITIVITY in .tau.csv and no verdict is read off it.")
    P("")

    # ------------------------------------------------------------------ PANELS
    P("-" * 100)
    P("PANELS")
    P("-" * 100)
    panels = {}
    u56 = load_universe(start=START)
    panels["U56"] = u56
    b136 = load_universe(start=START, broad=True)
    panels["B136"] = b136
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    sm = load_universe(small=True)
    dropped = [c for c in sm.columns if c in bad]
    sm = sm.drop(columns=dropped)
    panels["SMALL"] = sm
    P(f"  U56   {u56.shape[1]:>4} cols  {u56.index[0].date()}..{u56.index[-1].date()}  {len(u56):,} rows")
    P(f"  B136  {b136.shape[1]:>4} cols  {b136.index[0].date()}..{b136.index[-1].date()}  {len(b136):,} rows"
      f"   (SURVIVORSHIP: current constituents, PROTOCOL rule 9)")
    P(f"  SMALL {sm.shape[1]:>4} cols  {sm.index[0].date()}..{sm.index[-1].date()}  {len(sm):,} rows"
      f"   (dropped {len(dropped)} tickers with max_1d_move >= 1.0; SURVIVORSHIP: current constituents)")
    P("")

    D, BENCH = {}, {}
    for pn, px in panels.items():
        d = prep(px)
        D[pn] = d
        sb = blocks_m(d["spy"], d)
        lbm = blocks_m(backtest(px, rules_v2_weights(px), cost_bps=COST0, freq="W")["returns"]
                       .reindex(px.index).fillna(0.0).values, d)
        BENCH[pn] = dict(spy=sb, live=lbm)
        P(f"  {pn:<6} SPY   CAGR {sb['CAGR']:7.2%}  Sharpe {sb['Sharpe']:.4f}  MaxDD {sb['MaxDD']:7.2%}"
          f"  | OOS {sb['OOS_CAGR']:7.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:7.2%}")
        P(f"  {pn:<6} LIVE  CAGR {lbm['CAGR']:7.2%}  Sharpe {lbm['Sharpe']:.4f}  MaxDD {lbm['MaxDD']:7.2%}"
          f"  | OOS {lbm['OOS_CAGR']:7.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:7.2%}")
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100)
    P("CROSS-RUN GATES")
    P("-" * 100)
    gates = []

    def gate(name, what, value, ok):
        gates.append(dict(gate=name, what=what, value=value, pass_=bool(ok)))
        P(f"  {name:<5} {'PASS' if ok else 'FAIL'}  {what}  = {value}")

    inc = run_cell(D["U56"])
    m_inc = blocks_m(inc, D["U56"])
    P(f"  incumbent cell U56 W/H126/N=20/gross 0.75: CAGR {m_inc['CAGR']:.6f}  "
      f"Sharpe {m_inc['Sharpe']:.6f}  MaxDD {m_inc['MaxDD']:.6f}")
    for nm, got, want, tol in (("G1", m_inc["CAGR"], 0.155787, 5e-3),
                               ("G2", m_inc["Sharpe"], 1.139701, 5e-3),
                               ("G3", m_inc["MaxDD"], -0.191276, 5e-3)):
        gate(nm, f"incumbent anchor vs committed {want}", round(float(got), 6), abs(got - want) <= tol)
    gate("G4", "LAG is 1 and warm-up is 260", f"{LAG}/{WARMUP}", LAG == 1 and WARMUP == 260)
    gate("G5", "SPY is a benchmark, never a SMALL constituent",
         "SPY" in panels["SMALL"].columns, "SPY" in panels["SMALL"].columns)
    r1 = run_cell(D["U56"])
    gate("G6", "run_cell deterministic across calls", float(np.abs(r1 - inc).max()),
         float(np.abs(r1 - inc).max()) == 0.0)
    s1 = boot_sd(np.column_stack([inc[D["U56"]["warm"]]]), fsharpe, B=50)
    s2 = boot_sd(np.column_stack([inc[D["U56"]["warm"]]]), fsharpe, B=50)
    gate("G7", "bootstrap seeded / reproducible", float(abs(s1[0] - s2[0])), abs(s1[0] - s2[0]) == 0.0)
    gate("G8", "spearman(x,x) == 1 on a strict ladder", spearman([1, 2, 3, 4], [1, 2, 3, 4]),
         spearman([1, 2, 3, 4], [1, 2, 3, 4]) == 1.0)
    _dr = np.random.default_rng(0).normal(0, 0.1, size=(200, 4)) + np.array([1., 2., 3., 4.])
    _st = stamp_read([1., 2., 3., 4.], _dr, [1, 2, 3, 4])
    gate("G9", "stamp_read picks the endpoint on a strictly monotone ladder",
         _st["endpoint"], _st["endpoint"] is True)
    # the paired unit must be STRICTLY TIGHTER than the independent one on a correlated
    # ladder — the correction this run makes to its own first cut
    _c = np.random.default_rng(1).normal(0, 1, size=(400, 1)) + np.random.default_rng(2).normal(
        0, 0.05, size=(400, 2))
    _ind = float(np.sqrt(_c[:, 0].var(ddof=1) + _c[:, 1].var(ddof=1)))
    _pair = float((_c[:, 0] - _c[:, 1]).std(ddof=1))
    gate("G10", "paired SD < independent SD on correlated rungs (the correction)",
         round(_pair / _ind, 4), _pair < _ind)
    P("")

    # ------------------------------------------------------------------ (A) THE LADDERS
    P("-" * 100)
    P("(A) THE LADDER CENSUS — 3 panels x 4 dials, every rung published")
    P("-" * 100)
    t_lad0 = time.time()
    rows, RET = [], {}
    nbooks = 0
    for pn in ("U56", "B136", "SMALL"):
        d, sb, lbm = D[pn], BENCH[pn]["spy"], BENCH[pn]["live"]
        for dial, (kw, rungs) in DIALS.items():
            for rv in rungs:
                kwargs = dict(gross=DEFAULT["gross"], N=DEFAULT["N"], H=DEFAULT["H"],
                              maxvol=DEFAULT["maxvol"])
                kwargs[kw] = rv
                r = run_cell(d, **kwargs)
                nbooks += 1
                RET[(pn, dial, rv)] = r
                m = blocks_m(r, d)
                l4b, l4bo, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lbm)
                rows.append(dict(panel=pn, dial=dial, rung=rv, **{k: float(v) for k, v in m.items()},
                                 tent_IS=tent_is(m, sb), tent_full=tent_full(m, sb),
                                 negMaxDD=-abs(m["MaxDD"]), IS_negMaxDD=-abs(m["IS_MaxDD"]),
                                 pass_4b=bool(all(l4b.values())),
                                 pass_4b_oos=bool(all(l4bo.values())),
                                 pass_4a=bool(all(l4a.values()))))
            P(f"  {pn:<6} {dial:<7} {len(rungs):>3} rungs built")
    t_ladder = time.time() - t_lad0
    lad = pd.DataFrame(rows)
    lad["tent"] = lad["tent_full"]
    dump(lad, "ladder")
    P(f"  {nbooks} books, {t_ladder:.1f}s  ({t_ladder / nbooks:.2f}s per book)")
    P("")
    P("  BASE RATES over all 120 books (context for every share below):")
    for pn in ("U56", "B136", "SMALL"):
        s = lad[lad.panel == pn]
        P(f"    {pn:<6} 4b full {int(s.pass_4b.sum()):>3}/{len(s)}   4b OOS {int(s.pass_4b_oos.sum()):>3}/{len(s)}"
          f"   4a {int(s.pass_4a.sum()):>3}/{len(s)}")
    P(f"    ALL    4b full {int(lad.pass_4b.sum()):>3}/{len(lad)}   4b OOS {int(lad.pass_4b_oos.sum()):>3}/{len(lad)}"
      f"   4a {int(lad.pass_4a.sum()):>3}/{len(lad)}")
    P("")

    # ------------------------------------------------------------------ noise units
    P("-" * 100)
    P("THE NOISE UNIT — moving-block bootstrap SD per rung (B=%d, L=%d, seed %d)" % (BOOT_B, BOOT_L, SEED))
    P("-" * 100)
    P("  Draws are SHARED across the rungs of a ladder, so a PREFERENCE between two rungs")
    P("  uses the SD of their DIFFERENCE, not sqrt(sd_a^2+sd_b^2).  Adjacent rungs are the")
    P("  same book one parameter apart; the independent-variance bar would declare every")
    P("  argmax unresolved by construction.  Marginal SDs are published for SPREADS only.")
    t_sd0 = time.time()
    SD = {}     # (panel, dial, objective, window) -> (B x rungs) draw matrix
    for pn in ("U56", "B136", "SMALL"):
        d = D[pn]
        for dial, (kw, rungs) in DIALS.items():
            full = np.column_stack([RET[(pn, dial, rv)][d["warm"]] for rv in rungs])
            ins = np.column_stack([RET[(pn, dial, rv)][d["ins"]] for rv in rungs])
            SD[(pn, dial, "Sharpe", "full")] = boot_draws(full, fsharpe)
            SD[(pn, dial, "CAGR", "full")] = boot_draws(full, lambda r: fmet(r)[0])
            SD[(pn, dial, "negMaxDD", "full")] = boot_draws(full, lambda r: -abs(fmet(r)[2]))
            SD[(pn, dial, "Sharpe", "IS")] = boot_draws(ins, fsharpe, seed=SEED + 1)
            SD[(pn, dial, "CAGR", "IS")] = boot_draws(ins, lambda r: fmet(r)[0], seed=SEED + 1)
            SD[(pn, dial, "negMaxDD", "IS")] = boot_draws(ins, lambda r: -abs(fmet(r)[2]), seed=SEED + 1)
        P(f"  {pn} done  ({time.time() - t_sd0:.0f}s cumulative)")
    # the tent is a min of three relative legs; its draws are the Sharpe draws rescaled by
    # the SPY Sharpe the leg is divided by — a conservative stand-in, published as such
    for key in list(SD.keys()):
        if key[2] == "Sharpe":
            SD[(key[0], key[1], "tent", key[3])] = SD[key] / max(
                abs(BENCH[key[0]]["spy"]["Sharpe"]), 1e-9)
    t_sd = time.time() - t_sd0
    P(f"  noise units: {t_sd:.1f}s for {3 * 4 * 6} statistic-ladders (NO new books)")
    P("")

    # ------------------------------------------------------------------ (A) THE STAMP
    P("-" * 100)
    P("(A) THE STAMP'S READING — 16 (STAMP x CLAIMSET) cells x 3 panels x 4 dials, ALL published")
    P("-" * 100)
    srows = []
    for cs in CLAIMSETS:
        obj = OBJ_OF[cs]
        for pn in ("U56", "B136", "SMALL"):
            for dial, (kw, rungs) in DIALS.items():
                sub = lad[(lad.panel == pn) & (lad.dial == dial)].set_index("rung").loc[rungs]
                vals = sub[obj].values.astype(float)
                st = stamp_read(vals, SD[(pn, dial, obj, "full")], rungs)
                # what each STAMP form says about this one claim
                read = {}
                read["S_NONE"] = "END" if st["endpoint"] else "INTERIOR"
                read["S_RHO"] = ("SATURATING" if st["monotone"] else
                                 ("END-NOT-SATURATING" if st["endpoint"] else "INTERIOR"))
                read["S_MARGIN"] = (("END" if st["endpoint"] else "INTERIOR") if st["resolved"]
                                    else "UNRESOLVED")
                if st["monotone"]:
                    read["S_BOTH"] = "SATURATING"
                elif not st["resolved"]:
                    read["S_BOTH"] = "UNRESOLVED"
                else:
                    read["S_BOTH"] = "END-NOT-SATURATING" if st["endpoint"] else "INTERIOR"
                for stamp in STAMPS:
                    srows.append(dict(stamp=stamp, claimset=cs, objective=obj, panel=pn, dial=dial,
                                      n_rungs=len(rungs), argmax=st["argmax"], endpoint=st["endpoint"],
                                      rho=st["rho"], monotone=st["monotone"], runner=st["runner"],
                                      margin_runner_sd=st["margin_runner"],
                                      margin_vs_best_end_sd=st["margin_end"],
                                      pair_sd_runner=st["pair_sd_runner"],
                                      marg_sd_mean=st["marg_sd_mean"],
                                      spread_sd=st["spread_sd"], resolved=st["resolved"],
                                      reading=read[stamp],
                                      changes_reading=bool(read[stamp] != read["S_NONE"])))
    stamp = pd.DataFrame(srows)
    dump(stamp, "stamp")

    base = stamp[stamp.stamp == "S_NONE"].drop_duplicates(["claimset", "panel", "dial"])
    P(f"  claim population: {len(base)} argmax claims (4 objectives x 3 panels x 4 dials)")
    P("")
    P("  1154's 2x2, rebuilt on this population (endpoint x monotone):")
    ct = pd.crosstab(base.endpoint, base.monotone)
    P("    " + ct.to_string().replace("\n", "\n    "))
    nonmono = base[~base.monotone]
    P(f"  NON-MONOTONE claims that still pick an ENDPOINT: {int(nonmono.endpoint.sum())} of {len(nonmono)}"
      f" = {(nonmono.endpoint.mean() if len(nonmono) else np.nan):.3f}"
      f"   (1154 on its own population: 0.405)")
    if int(nonmono.endpoint.sum()):
        ne = nonmono[nonmono.endpoint]
        P(f"  of those, preference over the runner-up UNDER ONE SD: {int((~ne.resolved).sum())} of {len(ne)}"
          f" = {(~ne.resolved).mean():.3f}   (1154: 0.882)")
    P(f"  MONOTONE claims that pick an INTERIOR rung (the stamp's other direction): "
      f"{int((base.monotone & ~base.endpoint).sum())} of {len(base)}")
    P(f"  claims whose argmax is UNRESOLVED at {SDBAR:.0f} SD: {int((~base.resolved).sum())} of {len(base)}"
      f" = {(~base.resolved).mean():.3f}")
    P("")
    P("  HOW MANY CLAIMS CHANGE READING, per (STAMP x CLAIMSET) cell — all 16 published:")
    P(f"  {'':<10} " + "".join(f"{c:>12}" for c in CLAIMSETS))
    for s in STAMPS:
        line = f"  {s:<10} "
        for cs in CLAIMSETS:
            q = stamp[(stamp.stamp == s) & (stamp.claimset == cs)]
            line += f"{int(q.changes_reading.sum()):>6}/{len(q):<5}"
        P(line)
    P("")
    P("  same, as a share:")
    P(f"  {'':<10} " + "".join(f"{c:>12}" for c in CLAIMSETS))
    for s in STAMPS:
        line = f"  {s:<10} "
        for cs in CLAIMSETS:
            q = stamp[(stamp.stamp == s) & (stamp.claimset == cs)]
            line += f"{q.changes_reading.mean():>12.3f}"
        P(line)
    P("")

    # tau sensitivity — DECLARED, not a dial
    trows = []
    for tau in (0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99):
        for cs in CLAIMSETS:
            obj = OBJ_OF[cs]
            chg = mono = 0
            tot = 0
            for pn in ("U56", "B136", "SMALL"):
                for dial, (kw, rungs) in DIALS.items():
                    sub = lad[(lad.panel == pn) & (lad.dial == dial)].set_index("rung").loc[rungs]
                    st = stamp_read(sub[obj].values.astype(float),
                                    SD[(pn, dial, obj, "full")], rungs, tau=tau)
                    tot += 1
                    mono += int(st["monotone"])
                    r0 = "END" if st["endpoint"] else "INTERIOR"
                    rb = ("SATURATING" if st["monotone"] else
                          ("UNRESOLVED" if not st["resolved"] else
                           ("END-NOT-SATURATING" if st["endpoint"] else "INTERIOR")))
                    chg += int(rb != r0)
            trows.append(dict(tau=tau, claimset=cs, n_claims=tot, n_monotone=mono,
                              n_changes_S_BOTH=chg, share_changes=chg / tot))
    tdf = pd.DataFrame(trows)
    dump(tdf, "tau")
    P("  tau SENSITIVITY (declared, NOT a dial — no verdict is read off this):")
    P("    " + tdf.pivot(index="tau", columns="claimset", values="n_monotone").to_string().replace("\n", "\n    "))
    P("")

    # ------------------------------------------------------------------ (B) THE COST
    P("-" * 100)
    P("(B) THE COST — what the stamp asks of a run that ALREADY computed the ladder")
    P("-" * 100)
    t0 = time.time()
    for cs in CLAIMSETS:
        obj = OBJ_OF[cs]
        for pn in ("U56", "B136", "SMALL"):
            for dial, (kw, rungs) in DIALS.items():
                sub = lad[(lad.panel == pn) & (lad.dial == dial)].set_index("rung").loc[rungs]
                spearman(np.asarray(rungs, float), sub[obj].values.astype(float))
    t_rho = time.time() - t0
    t0 = time.time()
    for pn in ("U56", "B136", "SMALL"):
        d = D[pn]
        for dial, (kw, rungs) in DIALS.items():
            for rv in rungs:
                analytic_sharpe_sd(RET[(pn, dial, rv)][d["warm"]])
    t_analytic = time.time() - t0
    crows = [
        dict(stamp="S_NONE", extra_books=0, extra_path_evals=0, seconds=0.0,
             note="the record's status quo"),
        dict(stamp="S_RHO", extra_books=0, extra_path_evals=0, seconds=round(t_rho, 4),
             note="Spearman over the ladder the run already has"),
        dict(stamp="S_MARGIN(analytic)", extra_books=0, extra_path_evals=0,
             seconds=round(t_analytic, 4), note="Lo iid Sharpe SE, closed form, no resampling"),
        dict(stamp="S_MARGIN(bootstrap)", extra_books=0,
             extra_path_evals=int(BOOT_B * 3 * 40 * 2), seconds=round(t_sd, 2),
             note=f"moving-block SD, B={BOOT_B}, L={BOOT_L}, IS and full; no new BOOKS"),
        dict(stamp="S_BOTH(analytic)", extra_books=0, extra_path_evals=0,
             seconds=round(t_rho + t_analytic, 4), note="rho + closed-form SE"),
        dict(stamp="SECOND GRID (the alternative)", extra_books=int(nbooks),
             extra_path_evals=0, seconds=round(t_ladder, 2),
             note="re-run the whole ladder on a second sub-sample to check monotonicity"),
    ]
    cost = pd.DataFrame(crows)
    cost["books_pct_of_ladder"] = (cost.extra_books / nbooks * 100).round(1)
    cost["seconds_pct_of_ladder"] = (cost.seconds / t_ladder * 100).round(3)
    dump(cost, "cost")
    P("  " + cost.to_string(index=False).replace("\n", "\n  "))
    P("")
    P(f"  THE ANSWER TO THE QUEUE'S SECOND HALF: the ladder itself cost {t_ladder:.1f}s / {nbooks} books.")
    P(f"  S_RHO costs {t_rho:.4f}s and ZERO extra books ({t_rho / t_ladder * 100:.3f}% of the ladder).")
    P(f"  S_MARGIN costs ZERO extra BOOKS either way: {t_analytic:.4f}s closed form, {t_sd:.1f}s")
    P(f"  ({t_sd / t_ladder * 100:.1f}% of the ladder) if resampled.  A SECOND GRID costs +100%.")
    P("")

    # ------------------------------------------------------------------ (C) RULE 8
    P("-" * 100)
    P("(C) RULE 8 — three choosers read 2009-2016 ONLY; picks evaluated on untouched 2017-2026")
    P("-" * 100)
    P("  CH_ARGMAX  plain IS argmax of the objective                        (the record's habit)")
    P("  CH_STAMP   monotone -> refuse the end, fall back to the FROZEN INCUMBENT rung;")
    P("             else resolved -> argmax; else -> median rung of the within-1-SD set")
    P("  CH_STAMPM  IDENTICAL, except the monotone fallback is the ladder's own MIDPOINT.")
    P("             THE FALSIFICATION CONTROL.  CH_STAMP's incumbent fallback is a rung the")
    P("             record already chose with hindsight, so any OOS gain CH_STAMP shows is")
    P("             confounded with it.  CH_STAMPM knows nothing but the ladder.  If the")
    P("             stamp is worth anything, CH_STAMPM must beat CH_ARGMAX too.")
    P("  CH_CENTER  always the median rung of the within-1-SD set            (control)")
    P("")
    wrows = []
    for cs in CLAIMSETS:
        obj = OBJ_OF[cs]
        is_obj = {"Sharpe": "IS_Sharpe", "CAGR": "IS_CAGR",
                  "negMaxDD": "IS_negMaxDD", "tent": "tent_IS"}[obj]
        for pn in ("U56", "B136", "SMALL"):
            d, sb, lbm = D[pn], BENCH[pn]["spy"], BENCH[pn]["live"]
            for dial, (kw, rungs) in DIALS.items():
                sub = lad[(lad.panel == pn) & (lad.dial == dial)].set_index("rung").loc[rungs]
                v_is = sub[is_obj].values.astype(float)
                dr = SD[(pn, dial, obj, "IS")]
                st = stamp_read(v_is, dr, rungs)
                w1 = within_1sd_set(v_is, dr)
                center = rungs[int(np.median(w1))] if len(w1) else rungs[st["argmax_i"]]
                midrung = rungs[len(rungs) // 2]
                picks = {
                    "CH_ARGMAX": rungs[st["argmax_i"]],
                    "CH_STAMP": (DEFAULT[kw] if st["monotone"]
                                 else (rungs[st["argmax_i"]] if st["resolved"] else center)),
                    "CH_STAMPM": (midrung if st["monotone"]
                                  else (rungs[st["argmax_i"]] if st["resolved"] else center)),
                    "CH_CENTER": center,
                }
                for ch, pick in picks.items():
                    if pick not in rungs:      # the frozen default is always a rung of its own dial
                        pick = min(rungs, key=lambda x: abs(x - pick))
                    m = blocks_m(RET[(pn, dial, pick)], d)
                    l4b, l4bo, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lbm)
                    wrows.append(dict(
                        chooser=ch, claimset=cs, objective=obj, panel=pn, dial=dial, pick=pick,
                        is_argmax=rungs[st["argmax_i"]], IS_monotone=st["monotone"],
                        IS_rho=st["rho"], IS_resolved=st["resolved"],
                        IS_margin_sd=st["margin_runner"],
                        OOS_CAGR=m["OOS_CAGR"], OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                        FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"],
                        H1=m["H1"], H2=m["H2"],
                        SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                        SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                        LIVE_OOS_Sharpe=lbm["OOS_Sharpe"],
                        pass_4b=bool(all(l4b.values())), pass_4b_oos=bool(all(l4bo.values())),
                        pass_4a=bool(all(l4a.values())),
                        **{f"leg_{k}": bool(v) for k, v in l4b.items()},
                        **{f"legO_{k}": bool(v) for k, v in l4bo.items()}))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")

    CHOOSERS = ("CH_ARGMAX", "CH_STAMP", "CH_STAMPM", "CH_CENTER")
    P("  CHOOSER SCOREBOARD (48 picks each; OOS is 2017-2026, never read by any chooser):")
    P(f"  {'chooser':<11}{'medOOS_Sh':>11}{'meanOOS_Sh':>12}{'>SPY OOS':>10}{'4b full':>9}{'4b OOS':>9}{'4a':>7}")
    for ch in CHOOSERS:
        q = wf[wf.chooser == ch]
        P(f"  {ch:<11}{q.OOS_Sharpe.median():>11.4f}{q.OOS_Sharpe.mean():>12.4f}"
          f"{int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum()):>7}/{len(q):<3}"
          f"{int(q.pass_4b.sum()):>6}/{len(q):<3}{int(q.pass_4b_oos.sum()):>6}/{len(q):<3}"
          f"{int(q.pass_4a.sum()):>4}/{len(q):<3}")
    P("")
    P("  per panel, median OOS Sharpe by chooser (SPY OOS Sharpe in the last column):")
    for pn in ("U56", "B136", "SMALL"):
        q = wf[wf.panel == pn]
        line = f"    {pn:<6}"
        for ch in CHOOSERS:
            line += f"  {ch} {q[q.chooser == ch].OOS_Sharpe.median():.4f}"
        line += f"   | SPY {BENCH[pn]['spy']['OOS_Sharpe']:.4f}"
        P(line)
    P("")
    P("  HOW OFTEN DOES THE STAMP MOVE THE PICK AT ALL, and does it help when it does?")
    a = wf[wf.chooser == "CH_ARGMAX"].set_index(["claimset", "panel", "dial"]).sort_index()
    for ch in ("CH_STAMP", "CH_STAMPM", "CH_CENTER"):
        s = wf[wf.chooser == ch].set_index(["claimset", "panel", "dial"]).sort_index()
        moved = a.pick != s.pick
        line = f"    {ch:<10} moved {int(moved.sum()):>2} of {len(a)} picks"
        if int(moved.sum()):
            dd = (s.OOS_Sharpe - a.OOS_Sharpe)[moved]
            line += (f"   OOS Sharpe delta on the moved: mean {dd.mean():+.4f}"
                     f"  median {dd.median():+.4f}  better at {int((dd > 0).sum())} of {len(dd)}")
        P(line)
    P("")
    P("  THE CONFOUND, PRICED.  CH_STAMP's monotone fallback is the INCUMBENT rung")
    P("  (gross 0.75 / N 20 / H 126 / maxvol 0.60) — a cell the record already chose.")
    nmono = int((wf[wf.chooser == "CH_STAMP"].IS_monotone).sum())
    P(f"  Of 48 IS ladders, {nmono} read MONOTONE, so that fallback fires {nmono} times.")
    sM = wf[wf.chooser == "CH_STAMPM"]
    sI = wf[wf.chooser == "CH_STAMP"]
    P(f"  CH_STAMP  4b full {int(sI.pass_4b.sum())}/48   median OOS Sharpe {sI.OOS_Sharpe.median():.4f}")
    P(f"  CH_STAMPM 4b full {int(sM.pass_4b.sum())}/48   median OOS Sharpe {sM.OOS_Sharpe.median():.4f}"
      f"   <- the same stamp WITHOUT the incumbent")
    P("")
    P("  EVERY 4b-CLEARING PICK (full sample AND OOS), named:")
    good = wf[wf.pass_4b & wf.pass_4b_oos]
    if len(good):
        for _, r in good.iterrows():
            P(f"    {r.chooser:<10} {r.panel:<6} {r.dial:<7} pick {r['pick']:<6} ({r.claimset})  "
              f"full {r.FULL_CAGR:7.2%}/{r.FULL_Sharpe:.4f}/{r.FULL_MaxDD:7.2%}  "
              f"OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}")
    else:
        P("    NONE")
    P("")
    P("  EVERY 4a-CLEARING PICK, named:")
    g4a = wf[wf.pass_4a]
    if len(g4a):
        for _, r in g4a.iterrows():
            P(f"    {r.chooser:<10} {r.panel:<6} {r.dial:<7} pick {r['pick']:<6} ({r.claimset})  "
              f"full {r.FULL_CAGR:7.2%}/{r.FULL_Sharpe:.4f}/{r.FULL_MaxDD:7.2%}")
    else:
        P("    NONE")
    P("")

    dump(pd.DataFrame(gates), "gates")
    P("-" * 100)
    P(f"GATES {sum(g['pass_'] for g in gates)} of {len(gates)} PASS")
    P(f"TOTAL RUNTIME {time.time() - t_run0:.1f}s")
    P("-" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")


if __name__ == "__main__":
    main()
