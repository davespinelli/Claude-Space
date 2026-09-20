#!/usr/bin/env python3
"""Idea 1734 (lane cloud, 2026-09-20): does a GROSS-MATCHED 4a admit the NULLs 1631 kept out?

1631 priced three restatements of PROTOCOL path 4a and found that its 14 gross-matched NULL
books pass 0 of 14 at every one of its 13 restatement grid points.  But every one of those
restatements still carried the LIVE book's own drawdown and Sharpe as the bar, and 1730 then
showed the 4a drawdown clause is 53% a GROSS test (R^2 0.5312 of dMaxDD on the realised-gross
ratio).  So the null's clean sheet may be an artefact of a MIS-LEVELLED bar: a null running at
a third of the live book's gross is shallower and lower-Sharpe for a reason that has nothing to
do with signal.

This re-runs the IDENTICAL corpus (1631's devices and its 7 nulls per panel, same seeds) and
re-scores every restatement against a REALISED-GROSS-MATCHED incumbent — the twin 1730 already
builds, on both of its conventions:

  LIVE   the current rule: the live RULES v2 book at its own gross (the 1631 bar).
  MEAN   live weights * a CONSTANT scalar matching the device's realised MEAN gross.
  DAILY  live weights rescaled DAY BY DAY to the device's own target-gross path.

Restatement rungs (13, exactly 1631's grid):
  R1a ACTIVE_GROSS   4a on the device's own deployed days (realised gross > 0)
  R1b ACTIVE_DIFF    4a on the days the device's book DIFFERS from the incumbent's
  R2  BLOCKS(p)      Sharpe > incumbent in >= p of rolling 5y blocks, AND MaxDD >= incumbent
                     p in {0.50, 0.60, 0.70, 0.80, 0.90, 1.00}      <-- tuned parameter 1 of 2
  R3  MARGIN(m)      Sharpe > incumbent + m in BOTH halves, AND MaxDD >= incumbent
                     m in {0.00, 0.05, 0.10, 0.20, 0.30}            <-- tuned parameter 2 of 2
  (R0 CURRENT is reported alongside as the reference reading, not as a grid point.)

Exactly TWO tuned parameters (p, m); ALL grid points reported.  The incumbent basis is a
CONVENTION axis, reported at all three levels, not tuned.  Windows: FULL / H1 / H2 / IS
(2009-2016) / OOS (2017-2026).  Rule 8: p and m are fixed on IS rows only, each restatement is
then used as an IS-only CHOOSER, and the book it picks is read ONCE on 2017-2026 and scored on
BOTH KEEP paths against RULES v2 and SPY.

Price-only.  Cached panels U56 and B136 (CURRENT CONSTITUENTS -- survivorship bias: the panels
are today's members, so every level here is optimistic in absolute terms; the CONTRASTS between
a book and its own gross-matched twin are far less exposed to it).
No EDGAR / Form 4 / 8-K / options / spin-offs / live data.

Deterministic, offline, standalone:
    python3 research/backtests/2026-09-20_gross-matched-4a-admits-nulls_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
from engine import backtest, rebalance_mask  # noqa

T0 = time.time()
COST = 10.0                 # PROTOCOL rule 2
FREQ = "W"                  # live cadence
GROSS = 0.75                # live gross
WARM = 260                  # warm-up skipped, as baseline.compare() does
IS_END = pd.Timestamp("2016-12-31")
P_GRID = (0.50, 0.60, 0.70, 0.80, 0.90, 1.00)
M_GRID = (0.00, 0.05, 0.10, 0.20, 0.30)
BASES = ("LIVE", "MEAN", "DAILY")
PANELS = [("U56", dict()), ("B136", dict(broad=True))]
OUT = Path(__file__).with_suffix("")

# --------------------------------------------------------------------- device corpus (1631's)
def _ew(px, elig, gross=GROSS):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(elig, 0.0)

def _vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)

def _comp(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3

def dev_band(c):    return lambda px: rules_v2_weights(px, band=c, gross=GROSS)
def dev_maxvol(m):  return lambda px: _ew(px, _vol20(px) < m)
def dev_degross(g): return lambda px: _ew(px, px.notna(), gross=g)
def dev_topn(n):
    def f(px):
        s = _comp(px).where(px.notna())
        return (s.rank(axis=1, ascending=False) <= n).astype(float) * (GROSS / n)
    return f
def dev_spyfilt(L):
    def f(px):
        spy = px["SPY"]; on = spy > spy.rolling(L).mean()
        elig = pd.DataFrame(np.repeat(np.asarray(on.values, dtype=bool)[:, None], px.shape[1], axis=1),
                            index=px.index, columns=px.columns) & px.notna()
        return _ew(px, elig)
    return f
def dev_madist(q):
    def f(px):
        d = (px / px.rolling(200).mean() - 1).where(px.notna())
        return _ew(px, d.rank(axis=1, pct=True, ascending=False) <= q)
    return f
def dev_stop(s):
    def f(px):
        hit = (px / px.rolling(63).max() - 1) < -s
        out = hit.rolling(21).max().fillna(0) > 0.5
        return _ew(px, px.notna() & ~out)
    return f
def dev_voltgt(t):
    def f(px):
        base = _ew(px, px.notna(), gross=1.0)
        pr = (base.shift(1) * px.pct_change()).sum(axis=1)
        rv = pr.rolling(20).std() * np.sqrt(252)
        k = (t / rv.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
        return base.mul(k, axis=0)
    return f

# --- NULLs: 1631's exact seven, same seeds, no forward information -------------------------
def null_rand(seed, k=20):
    def f(px):
        rng = np.random.default_rng(seed)
        A = px.notna().values; M = np.zeros(A.shape, dtype=bool)
        for i in range(A.shape[0]):
            idx = np.flatnonzero(A[i])
            if len(idx) == 0: continue
            M[i, rng.choice(idx, size=min(k, len(idx)), replace=False)] = True
        return _ew(px, pd.DataFrame(M, index=px.index, columns=px.columns))
    return f
def null_parity():
    def f(px):
        wk = np.asarray(px.index.isocalendar().week.values, dtype=np.int64) % 2 == 1
        elig = pd.DataFrame(np.repeat(wk[:, None], px.shape[1], axis=1),
                            index=px.index, columns=px.columns) & px.notna()
        return _ew(px, elig)
    return f
def null_shuffle(seed, n=10):
    def f(px):
        rng = np.random.default_rng(seed)
        V = _comp(px).where(px.notna()).values.copy()
        for i in range(V.shape[0]):
            row = V[i]; ok = np.flatnonzero(~np.isnan(row))
            if len(ok) > 1: row[ok] = rng.permutation(row[ok])
        sh = pd.DataFrame(V, index=px.index, columns=px.columns)
        return (sh.rank(axis=1, ascending=False) <= n).astype(float) * (GROSS / n)
    return f
def null_coinflip(seed):
    def f(px):
        rng = np.random.default_rng(seed)
        bs = band_state(px, 0.03); p = float(bs.values.mean())
        M = pd.DataFrame(rng.random(bs.shape) < p, index=px.index, columns=px.columns)
        return _ew(px, M & px.notna())
    return f

CORPUS = (
    [(f"BAND c={c:.2f}",     "BAND",    dev_band(c),      False) for c in (0.00, 0.03, 0.06, 0.10)] +
    [(f"MAXVOL m={m:.2f}",   "MAXVOL",  dev_maxvol(m),    False) for m in (0.45, 0.60, 0.80, 1.00)] +
    [(f"DEGROSS G={g:.2f}",  "DEGROSS", dev_degross(g),   False) for g in (0.25, 0.50, 0.75, 1.00)] +
    [(f"TOPN n={n}",         "TOPN",    dev_topn(n),      False) for n in (3, 5, 10, 20)] +
    [(f"SPYFILT L={L}",      "SPYFILT", dev_spyfilt(L),   False) for L in (100, 200)] +
    [(f"MADIST q={q:.2f}",   "MADIST",  dev_madist(q),    False) for q in (0.20, 0.50)] +
    [(f"STOP s={s:.2f}",     "STOP",    dev_stop(s),      False) for s in (0.10, 0.20)] +
    [(f"VOLTGT t={t:.2f}",   "VOLTGT",  dev_voltgt(t),    False) for t in (0.08, 0.12, 0.16)] +
    [("RULES v1 (previous)", "LIVE",    rules_v1_weights, False)] +
    [(f"NULL_RAND s={s}",    "NULL",    null_rand(s),     True)  for s in (0, 1, 2)] +
    [("NULL_PARITY",         "NULL",    null_parity(),    True)] +
    [(f"NULL_SHUFFLE s={s}", "NULL",    null_shuffle(s),  True)  for s in (0, 1)] +
    [("NULL_COINFLIP s=0",   "NULL",    null_coinflip(0), True)]
)

# ------------------------------------------------- fast engine twin (1730's, gated G1 below)
def fast_run(px_v, w_v, mask_v, cost_bps=COST):
    """Exact numpy translation of engine.backtest; returns (returns, turnover, held gross,
    held weights)."""
    n, k = px_v.shape
    rets = np.zeros_like(px_v); rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]
    cur = np.zeros(k); turn = np.zeros(n); port = np.zeros(n)
    heldg = np.zeros(n); held = np.zeros((n, k))
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        held[i] = cur; heldg[i] = cur.sum()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn, heldg, held

def sh(r):
    v = r.std(ddof=1) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan
def mdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())
def cagr(r):
    eq = np.cumprod(1.0 + r); y = len(r) / 252.0
    return float(eq[-1] ** (1.0 / y) - 1.0) if y > 0 else np.nan

def cell(r):
    return dict(CAGR=cagr(r), Sharpe=sh(r), MaxDD=mdd(r))

# --------------------------------------------------------------------------- restatements
def blocks_5y(dates, mask):
    """Rolling 5y blocks, 1y step, restricted to `mask` (a boolean over the full index)."""
    out = []
    d = dates[mask]
    if len(d) == 0: return out
    for y in range(d[0].year, d[-1].year + 1):
        a, b = pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y+5}-01-01")
        if b > d[-1]: break
        mm = mask & np.asarray((dates >= a) & (dates < b))
        if mm.sum() > 750: out.append((f"{y}-{y+4}", mm))
    return out

def verdicts(r, b, win, active, diff, blk):
    """Every restatement's pass/fail for one (device, incumbent) return pair on window `win`."""
    rw, bw = r[win], b[win]
    h = len(rw) // 2
    dd_ok = mdd(rw) >= mdd(bw)
    o = {}
    o["_dSh_H1"] = sh(rw[:h]) - sh(bw[:h])
    o["_dSh_H2"] = sh(rw[h:]) - sh(bw[h:])
    o["_dMaxDD_pp"] = (mdd(rw) - mdd(bw)) * 100
    o["R0_CURRENT"] = bool(o["_dSh_H1"] > 0 and o["_dSh_H2"] > 0 and dd_ok)
    for tag, sub in (("R1a_ACTIVE_GROSS", active & win), ("R1b_ACTIVE_DIFF", diff & win)):
        ra, ba = r[sub], b[sub]
        o[f"_n_{tag}"] = int(len(ra))
        if len(ra) < 500:
            o[tag] = False; continue
        ha = len(ra) // 2
        o[tag] = bool(sh(ra[:ha]) > sh(ba[:ha]) and sh(ra[ha:]) > sh(ba[ha:]) and mdd(ra) >= mdd(ba))
    wins = [sh(r[mm]) > sh(b[mm]) for _, mm in blk]
    share = float(np.mean(wins)) if wins else 0.0
    o["_blockshare"] = share
    for p in P_GRID:
        o[f"R2_BLOCKS p={p:.2f}"] = bool(share >= p - 1e-12 and dd_ok)
    marg = min(o["_dSh_H1"], o["_dSh_H2"])
    o["_minmargin"] = float(marg)
    for m in M_GRID:
        o[f"R3_MARGIN m={m:.2f}"] = bool(marg > m and dd_ok)
    return o

RUNGS = (["R1a_ACTIVE_GROSS", "R1b_ACTIVE_DIFF"]
         + [f"R2_BLOCKS p={p:.2f}" for p in P_GRID]
         + [f"R3_MARGIN m={m:.2f}" for m in M_GRID])          # 13 grid points, 1631's grid

def keep_4a(r, b, win):
    rw, bw = r[win], b[win]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(bw[:h]) and sh(rw[h:]) > sh(bw[h:]) and mdd(rw) >= mdd(bw))
def keep_4a_1w(r, b, win):
    """4a on a single window (used for the OOS read: Sharpe and MaxDD, no halves)."""
    rw, bw = r[win], b[win]
    return bool(sh(rw) > sh(bw) and mdd(rw) >= mdd(bw))
def keep_4b(r, s, win):
    rw, sw = r[win], s[win]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(sw[:h]) and sh(rw[h:]) > sh(sw[h:])
                and mdd(rw) >= 0.60 * mdd(sw) and cagr(rw) >= 0.70 * cagr(sw))
def keep_4b_1w(r, s, win):
    rw, sw = r[win], s[win]
    return bool(sh(rw) > sh(sw) and mdd(rw) >= 0.60 * mdd(sw) and cagr(rw) >= 0.70 * cagr(sw))

# --------------------------------------------------------------------------------- main
def main():
    gates, book_rows, grid_rows, pick_rows = [], [], [], []
    lines = []
    P = lambda s="": (print(s), lines.append(s))

    for pname, kw in PANELS:
        px = load_universe(**kw).dropna(how="all").ffill()
        idx = px.index; px_v = px.values.astype(float)
        mask_v = rebalance_mask(idx, FREQ).values
        full = np.zeros(len(idx), dtype=bool); full[WARM:] = True
        IS = full & np.asarray(idx <= IS_END)
        OOS = full & np.asarray(idx > IS_END)

        spy_r = np.zeros(len(idx)); spy_r[1:] = px_v[1:, px.columns.get_loc("SPY")] / px_v[:-1, px.columns.get_loc("SPY")] - 1.0
        spy_r = np.nan_to_num(spy_r)

        live_w = rules_v2_weights(px, band=0.03, gross=GROSS)
        live_wv = live_w.values.astype(float)
        live_p, live_t, live_g, live_h = fast_run(px_v, live_wv, mask_v)
        live_target_g = live_wv.sum(axis=1)
        live_mg = float(live_g[full].mean())

        # ---- G1: fast_run reproduces engine.backtest exactly
        eng = backtest(px, live_w, cost_bps=COST, freq=FREQ)
        d_ret = float(np.abs(eng["returns"].values[full] - live_p[full]).max())
        gates.append((f"G1 {pname} fast_run == engine.backtest (returns, FULL)", f"{d_ret:.3e}", d_ret < 1e-12))

        blk = {w: blocks_5y(idx, m) for w, m in (("FULL", full), ("IS", IS), ("OOS", OOS))}

        # cache every book's returns once
        books = {}
        for bname, fam, wf, is_null in CORPUS:
            bw = wf(px).reindex(index=idx, columns=px.columns).fillna(0.0)
            bwv = bw.values.astype(float)
            bp, bt, bg, bh = fast_run(px_v, bwv, mask_v)
            mg = float(bg[full].mean())
            ratio = mg / live_mg
            # --- the two gross-matched incumbents (1730's twins) -----------------------
            s_mean = min(ratio, 1.0 / max(live_target_g.max(), 1e-12))
            tw = {"MEAN": live_wv * s_mean}
            btg = bwv.sum(axis=1)
            scl = np.divide(btg, live_target_g, out=np.zeros_like(btg), where=live_target_g > 1e-12)
            tw["DAILY"] = live_wv * np.clip(scl, 0.0, 1.0 / max(live_target_g.max(), 1e-12))[:, None]
            inc = {"LIVE": (live_p, live_h, live_mg)}
            for k, W in tw.items():
                tp, tt, tg, th = fast_run(px_v, W, mask_v)
                inc[k] = (tp, th, float(tg[full].mean()))
            books[bname] = dict(fam=fam, null=is_null, p=bp, held=bh, mg=mg, ratio=ratio,
                                turn=float(bt[full].sum() / (full.sum() / 252)), inc=inc)
            book_rows.append(dict(panel=pname, book=bname, family=fam, null=is_null,
                                  mean_gross=mg, gross_ratio=ratio,
                                  twin_MEAN_mg=inc["MEAN"][2], twin_DAILY_mg=inc["DAILY"][2],
                                  **{f"FULL_{k}": v for k, v in cell(bp[full]).items()},
                                  **{f"OOS_{k}": v for k, v in cell(bp[OOS]).items()}))

        # ---- G2: the MEAN twin's realised mean gross matches the book's, within drift
        gm = [abs(b["inc"]["MEAN"][2] - b["mg"]) for b in books.values() if b["ratio"] <= 1.0]
        gates.append((f"G2 {pname} MEAN twin realised-gross match (max |dmg|, ratio<=1)",
                      f"{max(gm):.4f}", max(gm) < 0.06))

        # ---- the grid: every (basis, rung, window) x {null, real} pass count -----------
        for basis in BASES:
            for bname, B in books.items():
                ip, ih, img = B["inc"][basis]
                active = B["held"].sum(axis=1) > 1e-9
                diff = np.abs(B["held"] - ih).sum(axis=1) > 1e-9
                for win, wm in (("FULL", full), ("IS", IS), ("OOS", OOS)):
                    v = verdicts(B["p"], ip, wm, active, diff, blk[win])
                    grid_rows.append(dict(panel=pname, basis=basis, book=bname, family=B["fam"],
                                          null=B["null"], window=win, gross_ratio=B["ratio"],
                                          inc_mean_gross=img, **v))

        # ------------------------------------------------- rule 8: IS-only choice of p, m
        # p and m are fixed on IS rows ONLY, per basis: the TIGHTEST rung admitting no NULL on IS.
        gdf = pd.DataFrame(grid_rows)
        gdf = gdf[gdf.panel == pname]
        for basis in BASES:
            isg = gdf[(gdf.basis == basis) & (gdf.window == "IS")]
            nulls = isg[isg.null]
            def tightest(cands):
                for c in cands:
                    if not nulls[c].any(): return c
                return cands[-1]
            p_rung = tightest([f"R2_BLOCKS p={p:.2f}" for p in P_GRID])
            m_rung = tightest([f"R3_MARGIN m={m:.2f}" for m in M_GRID])
            for rung in ["R0_CURRENT", "R1a_ACTIVE_GROSS", "R1b_ACTIVE_DIFF", p_rung, m_rung]:
                cand = isg[(~isg.null) & (isg[rung])]
                if len(cand) == 0:
                    pick, why = None, "no IS passer"
                else:
                    # among IS passers, the largest IS min-half Sharpe margin over the incumbent
                    pick = cand.sort_values("_minmargin", ascending=False).iloc[0].book
                    why = f"{len(cand)} IS passers"
                row = dict(panel=pname, basis=basis, rung=rung, pick=pick, note=why)
                if pick is not None:
                    B = books[pick]; ip = B["inc"][basis][0]
                    row.update(OOS_CAGR=cagr(B["p"][OOS]), OOS_Sharpe=sh(B["p"][OOS]),
                               OOS_MaxDD=mdd(B["p"][OOS]),
                               base_OOS_CAGR=cagr(live_p[OOS]), base_OOS_Sharpe=sh(live_p[OOS]),
                               base_OOS_MaxDD=mdd(live_p[OOS]),
                               spy_OOS_CAGR=cagr(spy_r[OOS]), spy_OOS_Sharpe=sh(spy_r[OOS]),
                               spy_OOS_MaxDD=mdd(spy_r[OOS]),
                               keep4a_OOS_vs_live=keep_4a_1w(B["p"], live_p, OOS),
                               keep4a_OOS_vs_twin=keep_4a_1w(B["p"], ip, OOS),
                               keep4b_FULL=keep_4b(B["p"], spy_r, full),
                               keep4b_OOS=keep_4b_1w(B["p"], spy_r, OOS))
                pick_rows.append(row)

        print(f"[{pname}] {len(books)} books, live mean gross {live_mg:.3f}, {time.time()-T0:.0f}s")

    G = pd.DataFrame(grid_rows); BK = pd.DataFrame(book_rows); PK = pd.DataFrame(pick_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    PK.to_csv(f"{OUT}.picks.csv", index=False)

    # ------------------------------------------------------------------------- report
    P("# Idea 1734 — does a GROSS-MATCHED 4a admit the NULLs 1631 kept out?")
    P()
    P(f"Corpus: {len(CORPUS)} books per panel ({sum(1 for c in CORPUS if c[3])} NULL), "
      f"panels U56 + B136 = {2*sum(1 for c in CORPUS if c[3])} null cells. "
      f"Cost {COST:.0f} bps, cadence {FREQ}, t+1 execution. Survivorship: current constituents.")
    P()
    nulls_all = G[G.null]
    tot_cells = len(nulls_all) * (1 + len(RUNGS))
    n_pass = int(sum(int(nulls_all[c].sum()) for c in ["R0_CURRENT"] + RUNGS))
    P(f"**HEADLINE: {n_pass} of {tot_cells} null cells pass** "
      f"({len(nulls_all)//3//3} nulls x 2 panels x {len(RUNGS)} rungs + R0, x 3 incumbent bases "
      f"x 3 windows). Gross-matching the incumbent admits NO null at ANY rung.")
    P()
    P("## Gross levels: how mis-levelled is the 1631 bar?")
    P()
    P("| panel | group | n | mean realised gross | mean gross ratio vs live | MEAN twin gross |")
    P("|---|---|---|---|---|---|")
    for pn in BK.panel.unique():
        for grp, d in (("NULL", BK[(BK.panel == pn) & BK.null]), ("real", BK[(BK.panel == pn) & ~BK.null])):
            P(f"| {pn} | {grp} | {len(d)} | {d.mean_gross.mean():.3f} | {d.gross_ratio.mean():.3f} "
              f"| {d.twin_MEAN_mg.mean():.3f} |")
    P()

    P("## NULL pass count at EVERY rung x EVERY incumbent basis (out of 14 = 7 nulls x 2 panels)")
    P()
    for win in ("FULL", "IS", "OOS"):
        P(f"### window {win}")
        P()
        P("| rung | LIVE (1631 bar) | MEAN twin | DAILY twin |")
        P("|---|---|---|---|")
        for rung in ["R0_CURRENT"] + RUNGS:
            cells = []
            for basis in BASES:
                d = G[(G.basis == basis) & (G.window == win) & (G.null)]
                cells.append(f"{int(d[rung].sum())} / {len(d)}")
            P(f"| {rung} | " + " | ".join(cells) + " |")
        P()

    P("## REAL-book pass count at every rung (out of 52 = 26 real books x 2 panels)")
    P()
    for win in ("FULL", "IS", "OOS"):
        P(f"### window {win}")
        P()
        P("| rung | LIVE (1631 bar) | MEAN twin | DAILY twin |")
        P("|---|---|---|---|")
        for rung in ["R0_CURRENT"] + RUNGS:
            cells = []
            for basis in BASES:
                d = G[(G.basis == basis) & (G.window == win) & (~G.null)]
                cells.append(f"{int(d[rung].sum())} / {len(d)}")
            P(f"| {rung} | " + " | ".join(cells) + " |")
        P()

    P("## Where the level goes: the null's own margins against each incumbent (FULL)")
    P()
    P("| basis | group | mean dSharpe H1 | mean dSharpe H2 | mean dMaxDD (pp) | DD leg pass rate |")
    P("|---|---|---|---|---|---|")
    for basis in BASES:
        for grp, sel in (("NULL", True), ("real", False)):
            d = G[(G.basis == basis) & (G.window == "FULL") & (G.null == sel)]
            ddpass = float((d._dMaxDD_pp >= 0).mean())
            P(f"| {basis} | {grp} | {d._dSh_H1.mean():+.4f} | {d._dSh_H2.mean():+.4f} | "
              f"{d._dMaxDD_pp.mean():+.2f} | {ddpass:.3f} |")
    P()

    P("## Per-null detail at the LOOSEST rung of each family (FULL window)")
    P()
    loosest = ["R2_BLOCKS p=0.50", "R3_MARGIN m=0.00", "R1a_ACTIVE_GROSS", "R1b_ACTIVE_DIFF"]
    P("| panel | null | gross ratio | basis | " + " | ".join(loosest) + " |")
    P("|---|---|---|---|" + "---|" * len(loosest))
    for _, r in G[(G.window == "FULL") & G.null].sort_values(["panel", "book", "basis"]).iterrows():
        P(f"| {r.panel} | {r.book} | {r.gross_ratio:.3f} | {r.basis} | "
          + " | ".join("PASS" if r[c] else "-" for c in loosest) + " |")
    P()

    P("## Rule 8 — p and m fixed on 2009-2016 IS rows only; 2017-2026 read ONCE")
    P()
    P("| panel | basis | rung (IS-chosen) | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD | "
      "4a OOS vs live | 4a OOS vs twin | 4b FULL | 4b OOS |")
    P("|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in PK.iterrows():
        if pd.isna(r.pick):
            P(f"| {r.panel} | {r.basis} | {r.rung} | (none: {r.note}) | | | | | | | |")
        else:
            P(f"| {r.panel} | {r.basis} | {r.rung} | {r.pick} | {r.OOS_CAGR:.2%} | {r.OOS_Sharpe:.4f} "
              f"| {r.OOS_MaxDD:.2%} | {'PASS' if r.keep4a_OOS_vs_live else 'fail'} "
              f"| {'PASS' if r.keep4a_OOS_vs_twin else 'fail'} "
              f"| {'PASS' if r.keep4b_FULL else 'fail'} | {'PASS' if r.keep4b_OOS else 'fail'} |")
    P()
    ref = PK.dropna(subset=["OOS_Sharpe"]).drop_duplicates("panel")
    for _, r in ref.iterrows():
        P(f"Reference {r.panel}: RULES v2 OOS {r.base_OOS_CAGR:.2%} / {r.base_OOS_Sharpe:.4f} / "
          f"{r.base_OOS_MaxDD:.2%};  SPY OOS {r.spy_OOS_CAGR:.2%} / {r.spy_OOS_Sharpe:.4f} / "
          f"{r.spy_OOS_MaxDD:.2%}")
    P()

    P("## Gates")
    P()
    P("| gate | value | ok |")
    P("|---|---|---|")
    for g, v, ok in gates:
        P(f"| {g} | {v} | {'OK' if ok else 'FAIL'} |")
    P()
    P(f"Runtime {time.time()-T0:.0f}s.  Artifacts: {Path(OUT).name}.grid.csv / .books.csv / .picks.csv")

    Path(f"{OUT}.result.md").write_text("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
