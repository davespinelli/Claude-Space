#!/usr/bin/env python3
"""Idea 1730 (lane cloud, 2026-09-20) — IS PATH 4a's DRAWDOWN CLAUSE JUST A GROSS TEST?

Idea 1631 (lane C, 2026-09-20) found that 41 of 51 committed books trip rule 4a's MaxDD leg
against the live RULES v2 book, mean dMaxDD -5.42 pp with only 11 of 52 shallower, while the two
Sharpe legs sit a mean -0.0894 away.  Its three restatements all rewrote the SHARPE legs and so
moved at most 1 of 66 cells.  This script asks the question 1631 never tested:

  (A) REGRESSION.  Across the record's own committed device corpus, regress each book's
      dMaxDD (book MaxDD minus the LIVE book's MaxDD, in pp) on its REALISED-GROSS RATIO to the
      live book.  Report R^2, the slope, and the residual spread.  If gross explains the clause,
      4a is measuring exposure, not risk control.

  (B) RESTATEMENT.  Re-run 4a against a REALISED-GROSS-MATCHED INCUMBENT — the live book's own
      weight vector rescaled to the candidate's exposure — instead of against the live book.
      Two tuned parameters and no more:
          basis  in {MEAN, DAILY}   how the incumbent is matched (constant scalar on mean
                                    realised gross, or day-by-day on the target-gross path)
          tau    in {0, 1, 2, 3, 5} pp   slack in the restated MaxDD leg
      = 10 grid points, EVERY one reported, for REAL books and for NULL books alike.
      A bar that admits a no-signal book is not a bar (this is also idea 1734's question and it
      is answered here because it costs nothing extra to answer it).

  (C) RULE 8.  The (basis, tau) pair and the book it selects are fitted on 2009-2016 rows ONLY;
      2017-2026 is read ONCE.  OOS CAGR / Sharpe / MaxDD reported against RULES v2 and SPY, with
      both KEEP paths (4a and 4b) at every grid point.

Corpus: idea 1631's committed device families, copied verbatim so this file is standalone
(BAND / MAXVOL / DEGROSS / TOPN / SPYFILT / MADIST / STOP / VOLTGT / RULES v1) plus its 14
gross-matched NULLs.  Panels U56 and B136 (cached, CURRENT CONSTITUENTS — survivorship bias).
Price-only, weekly, 10 bps, next-day execution, no leverage.  Deterministic, offline.

    python3 research/backtests/2026-09-20_4a-drawdown-clause-vs-gross_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state   # noqa: E402
from engine import backtest, rebalance_mask                                          # noqa: E402

T0 = time.time()
OUT   = Path(__file__).resolve().parent
STEM  = "2026-09-20_4a-drawdown-clause-vs-gross_cloud"
COST  = 10.0                       # PROTOCOL rule 2
FREQ  = "W"                        # live cadence
GROSS = 0.75                       # live gross
WARM  = 260                        # rows baseline.compare() drops
IS_END = pd.Timestamp("2016-12-31")
TAUS  = (0.00, 0.01, 0.02, 0.03, 0.05)        # dial 2: MaxDD slack, in FRACTION (0-5 pp)
BASES = ("MEAN", "DAILY")                     # dial 1: gross-matching convention
PANELS = [("U56", dict()), ("B136", dict(broad=True))]

# ------------------------------------------------------- device corpus (verbatim from 1631)
def _ew(px, elig, gross=GROSS):
    """Record convention: gross/N over every PRICED name, gated-out weight goes to CASH."""
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
        on = px["SPY"] > px["SPY"].rolling(L).mean()
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

def null_rand(seed, k=20):
    def f(px):
        rng = np.random.default_rng(seed); A = px.notna().values
        M = np.zeros(A.shape, dtype=bool)
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
        rng = np.random.default_rng(seed); V = _comp(px).where(px.notna()).values.copy()
        for i in range(V.shape[0]):
            row = V[i]; ok = np.flatnonzero(~np.isnan(row))
            if len(ok) > 1: row[ok] = rng.permutation(row[ok])
        sh = pd.DataFrame(V, index=px.index, columns=px.columns)
        return (sh.rank(axis=1, ascending=False) <= n).astype(float) * (GROSS / n)
    return f
def null_coinflip(seed):
    def f(px):
        rng = np.random.default_rng(seed); bs = band_state(px, 0.03)
        M = pd.DataFrame(rng.random(bs.shape) < float(bs.values.mean()),
                         index=px.index, columns=px.columns)
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

# ------------------------------------------------------- fast engine twin (from 1723, gated G1)
def fast_run(px_v, w_v, mask_v, cost_bps=COST):
    """Exact numpy translation of engine.backtest.  Returns (portfolio returns, turnover,
    realised held gross)."""
    n = px_v.shape[0]
    rets = np.zeros_like(px_v); rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]          # decided at t, applied at t+1
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]
    cur = np.zeros(px_v.shape[1]); turn = np.zeros(n); port = np.zeros(n); heldg = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        heldg[i] = cur.sum()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn, heldg

def mx(r):
    eq = np.cumprod(1.0 + r); yrs = len(r) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252)
    return float(cagr), float(r.mean() * 252 / vol) if vol else np.nan, dd

def windows(idx):
    full = np.zeros(len(idx), dtype=bool); full[WARM:] = True
    h = full.sum() // 2
    h1 = full.copy(); h1[WARM + h:] = False
    h2 = full.copy(); h2[:WARM + h] = False
    return dict(FULL=full, H1=h1, H2=h2,
                IS=full & np.asarray(idx <= IS_END), OOS=full & np.asarray(idx > IS_END))

def score(port, W):
    o = {}
    for k, m in W.items():
        c, s, d = mx(port[m]); o[k] = (c, s, d)
    return dict(CAGR=o["FULL"][0], Sharpe=o["FULL"][1], MaxDD=o["FULL"][2],
                H1=o["H1"][1], H2=o["H2"][1],
                IS_CAGR=o["IS"][0], IS_Sharpe=o["IS"][1], IS_MaxDD=o["IS"][2],
                OOS_CAGR=o["OOS"][0], OOS_Sharpe=o["OOS"][1], OOS_MaxDD=o["OOS"][2])

def keep_4a(r, b):
    return bool(r["H1"] > b["H1"] and r["H2"] > b["H2"] and r["MaxDD"] >= b["MaxDD"])
def keep_4a_oos(r, b):
    return bool(r["OOS_Sharpe"] > b["OOS_Sharpe"] and r["OOS_MaxDD"] >= b["OOS_MaxDD"])
def keep_4b_full(r, s):
    return bool(r["H1"] > s["H1"] and r["H2"] > s["H2"]
                and r["MaxDD"] >= 0.60 * s["MaxDD"] and r["CAGR"] >= 0.70 * s["CAGR"])
def keep_4b_oos(r, s):
    return bool(r["OOS_Sharpe"] > s["OOS_Sharpe"]
                and r["OOS_MaxDD"] >= 0.60 * s["OOS_MaxDD"] and r["OOS_CAGR"] >= 0.70 * s["OOS_CAGR"])

def ols(x, y):
    """Plain OLS y = a + b x; returns (a, b, R^2, residuals)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    X = np.column_stack([np.ones_like(x), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ coef
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float((res ** 2).sum()) / ss_tot if ss_tot > 0 else np.nan
    return float(coef[0]), float(coef[1]), r2, res


def main():
    gates, rows, reg_rows, grid_rows, pick_rows = [], [], [], [], []
    panel_ref = {}

    for pname, kw in PANELS:
        px = load_universe(**kw).dropna(how="all").ffill()
        idx = px.index; px_v = px.values.astype(float)
        mask_v = rebalance_mask(idx, FREQ).values
        W = windows(idx); fw = W["FULL"]
        spy_col = px.columns.get_loc("SPY")

        spy_r = np.zeros(len(idx)); spy_r[1:] = px_v[1:, spy_col] / px_v[:-1, spy_col] - 1.0
        SPY = score(np.nan_to_num(spy_r), W)

        live_w = rules_v2_weights(px, band=0.03, gross=GROSS)
        live_wv = live_w.values.astype(float)
        live_p, live_t, live_g = fast_run(px_v, live_wv, mask_v)
        LIVE = score(live_p, W)
        live_mean_gross = float(live_g[fw].mean())
        live_target_g = live_wv.sum(axis=1)
        panel_ref[pname] = dict(SPY=SPY, LIVE=LIVE, mg=live_mean_gross)

        # ---- G1: fast_run reproduces engine.backtest on the FULL window --------------
        eng = backtest(px, live_w, cost_bps=COST, freq=FREQ)
        d_ret = float(np.abs(eng["returns"].values[fw] - live_p[fw]).max())
        d_trn = float(np.abs(eng["turnover"].values[fw] - live_t[fw]).max())
        gates.append((f"G1 {pname} fast_run vs engine.backtest (returns / turnover, FULL)",
                      f"{d_ret:.3e} / {d_trn:.3e}", d_ret < 1e-12 and d_trn < 1e-12))
        gates.append((f"G2 {pname} live RULES v2 FULL cell",
                      f"{LIVE['CAGR']:.2%} / {LIVE['Sharpe']:.4f} / {LIVE['MaxDD']:.2%}", True))

        max_gross_seen = 0.0
        for bname, fam, wf, is_null in CORPUS:
            bw = wf(px).reindex(index=idx, columns=px.columns).fillna(0.0)
            bwv = bw.values.astype(float)
            bp, bt, bg = fast_run(px_v, bwv, mask_v)
            B = score(bp, W)
            mg = float(bg[fw].mean())
            ratio = mg / live_mean_gross
            max_gross_seen = max(max_gross_seen, float(bwv.sum(axis=1).max()))

            # --- gross-matched incumbents ------------------------------------------
            tw = {}
            s_mean = min(ratio, 1.0 / max(live_target_g.max(), 1e-12))
            tw["MEAN"] = live_wv * s_mean
            btg = bwv.sum(axis=1)
            sc = np.divide(btg, live_target_g, out=np.zeros_like(btg),
                           where=live_target_g > 1e-12)
            tw["DAILY"] = live_wv * sc[:, None]
            twin = {}
            for basis, wv in tw.items():
                tp, tt, tg = fast_run(px_v, wv, mask_v)
                twin[basis] = dict(sc=score(tp, W), mg=float(tg[fw].mean()),
                                   max_g=float(wv.sum(axis=1).max()))
            # G3: the DAILY twin reproduces the book's TARGET gross path wherever the live
            # book is deployed (it cannot on days the live book is 100% cash -- reported).
            on = live_target_g > 1e-12
            d_daily = float(np.abs(tw["DAILY"].sum(axis=1)[on] - btg[on]).max())
            gates.append((f"G3 {pname} {bname} DAILY twin target-gross match (live-deployed days)",
                          f"{d_daily:.3e}", d_daily < 1e-9))

            rec = dict(panel=pname, book=bname, family=fam, is_null=is_null,
                       mean_gross=mg, gross_ratio=ratio,
                       dMaxDD_pp=(B["MaxDD"] - LIVE["MaxDD"]) * 100,
                       dSh_H1=B["H1"] - LIVE["H1"], dSh_H2=B["H2"] - LIVE["H2"],
                       KEEP_4a_FULL=keep_4a(B, LIVE), KEEP_4b_FULL=keep_4b_full(B, SPY),
                       KEEP_4a_OOS=keep_4a_oos(B, LIVE), KEEP_4b_OOS=keep_4b_oos(B, SPY),
                       **{k: v for k, v in B.items()})
            for basis in BASES:
                t = twin[basis]["sc"]
                rec[f"twin_{basis}_mg"] = twin[basis]["mg"]
                rec[f"twin_{basis}_MaxDD"] = t["MaxDD"]
                rec[f"twin_{basis}_dMaxDD_pp"] = (B["MaxDD"] - t["MaxDD"]) * 100
                rec[f"twin_{basis}_dSh_H1"] = B["H1"] - t["H1"]
                rec[f"twin_{basis}_dSh_H2"] = B["H2"] - t["H2"]
                rec[f"twin_{basis}_IS_dSh"] = B["IS_Sharpe"] - t["IS_Sharpe"]
                rec[f"twin_{basis}_IS_dMaxDD_pp"] = (B["IS_MaxDD"] - t["IS_MaxDD"]) * 100
                rec[f"twin_{basis}_OOS_dSh"] = B["OOS_Sharpe"] - t["OOS_Sharpe"]
                rec[f"twin_{basis}_OOS_dMaxDD_pp"] = (B["OOS_MaxDD"] - t["OOS_MaxDD"]) * 100
            rows.append(rec)
            for basis in BASES:
                for tau in TAUS:
                    t = twin[basis]["sc"]
                    grid_rows.append(dict(
                        panel=pname, book=bname, family=fam, is_null=is_null,
                        basis=basis, tau_pp=tau * 100,
                        R0_CURRENT=keep_4a(B, LIVE),
                        R_FULL=bool(B["H1"] > t["H1"] and B["H2"] > t["H2"]
                                    and B["MaxDD"] >= t["MaxDD"] - tau),
                        R_IS=bool(B["IS_Sharpe"] > t["IS_Sharpe"]
                                  and B["IS_MaxDD"] >= t["IS_MaxDD"] - tau),
                        R_OOS=bool(B["OOS_Sharpe"] > t["OOS_Sharpe"]
                                   and B["OOS_MaxDD"] >= t["OOS_MaxDD"] - tau),
                        IS_Sharpe=B["IS_Sharpe"], OOS_Sharpe=B["OOS_Sharpe"],
                        OOS_CAGR=B["OOS_CAGR"], OOS_MaxDD=B["OOS_MaxDD"],
                        KEEP_4a_OOS=keep_4a_oos(B, LIVE), KEEP_4b_OOS=keep_4b_oos(B, SPY)))
        gates.append((f"G4 {pname} no leverage (max target gross over corpus)",
                      f"{max_gross_seen:.6f}", max_gross_seen <= 1.0 + 1e-12))

    df = pd.DataFrame(rows)
    gd = pd.DataFrame(grid_rows)
    df.to_csv(OUT / f"{STEM}.books.csv", index=False)
    gd.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    gates.append(("G5 two tuned dials only", "basis (MEAN/DAILY), tau (0-5 pp)", True))
    gates.append(("G6 grid points reported", f"{len(BASES)}x{len(TAUS)} = {len(BASES)*len(TAUS)} "
                  f"x {len(CORPUS)} books x {len(PANELS)} panels = {len(gd)} rows", True))

    # ============================== (A) THE REGRESSION =============================
    L = []; P = L.append
    P("# Idea 1730 — is path 4a's drawdown clause just a gross test?\n")
    P(f"Corpus {len(CORPUS)} books ({sum(1 for c in CORPUS if not c[3])} real, "
      f"{sum(1 for c in CORPUS if c[3])} null) x {len(PANELS)} panels = {len(df)} books. "
      f"Weekly, {COST:.0f} bps, next-day execution, no leverage. "
      "Panels U56 / B136 are CURRENT CONSTITUENTS — survivorship bias applies to every "
      "level below; the regression is a WITHIN-panel contrast and is far less exposed to it "
      "than a level claim.\n")

    for pname, _ in PANELS:
        r = panel_ref[pname]
        P(f"**{pname}**  SPY FULL {r['SPY']['CAGR']:.2%} / {r['SPY']['Sharpe']:.4f} / "
          f"{r['SPY']['MaxDD']:.2%} (H1 {r['SPY']['H1']:.4f} / H2 {r['SPY']['H2']:.4f}), "
          f"OOS {r['SPY']['OOS_CAGR']:.2%} / {r['SPY']['OOS_Sharpe']:.4f} / {r['SPY']['OOS_MaxDD']:.2%}  |  "
          f"RULES v2 FULL {r['LIVE']['CAGR']:.2%} / {r['LIVE']['Sharpe']:.4f} / {r['LIVE']['MaxDD']:.2%} "
          f"(H1 {r['LIVE']['H1']:.4f} / H2 {r['LIVE']['H2']:.4f}), "
          f"OOS {r['LIVE']['OOS_CAGR']:.2%} / {r['LIVE']['OOS_Sharpe']:.4f} / {r['LIVE']['OOS_MaxDD']:.2%}, "
          f"mean realised gross {r['mg']:.4f}")

    P("\n## (A) dMaxDD (pp, vs the LIVE book) regressed on REALISED-GROSS RATIO to the live book\n")
    P("| set | n | slope (pp per 1.0 of ratio) | intercept | R^2 | resid SD (pp) | resid min..max (pp) | "
      "rho(Spearman) |")
    P("|---|---|---|---|---|---|---|---|")
    def regline(tag, d):
        if len(d) < 3: return
        a, b, r2, res = ols(d.gross_ratio, d.dMaxDD_pp)
        rho = float(pd.Series(d.gross_ratio).rank().corr(pd.Series(d.dMaxDD_pp).rank()))
        P(f"| {tag} | {len(d)} | {b:+.2f} | {a:+.2f} | {r2:.4f} | {res.std(ddof=2):.2f} | "
          f"{res.min():+.2f} .. {res.max():+.2f} | {rho:+.4f} |")
        reg_rows.append(dict(set=tag, n=len(d), slope=b, intercept=a, r2=r2,
                             resid_sd=float(res.std(ddof=2)), resid_min=float(res.min()),
                             resid_max=float(res.max()), spearman=rho))
    regline("POOLED (all books, both panels)", df)
    regline("POOLED real only", df[~df.is_null])
    regline("POOLED null only", df[df.is_null])
    for pname, _ in PANELS:
        regline(f"{pname} all", df[df.panel == pname])
        regline(f"{pname} real only", df[(df.panel == pname) & (~df.is_null)])
    P("")
    P("### The same regression per device FAMILY (real books only, pooled panels)\n")
    P("| family | n | slope | R^2 | resid SD (pp) | mean gross ratio | mean dMaxDD (pp) |")
    P("|---|---|---|---|---|---|---|")
    for fam, d in df[~df.is_null].groupby("family"):
        if len(d) >= 3:
            a, b, r2, res = ols(d.gross_ratio, d.dMaxDD_pp)
            P(f"| {fam} | {len(d)} | {b:+.2f} | {r2:.4f} | {res.std(ddof=2):.2f} | "
              f"{d.gross_ratio.mean():.3f} | {d.dMaxDD_pp.mean():+.2f} |")
        else:
            P(f"| {fam} | {len(d)} | (n<3) | — | — | {d.gross_ratio.mean():.3f} | "
              f"{d.dMaxDD_pp.mean():+.2f} |")
    P("")
    P("### 1631's headline, reproduced on this corpus\n")
    for pname, _ in PANELS:
        d = df[df.panel == pname]
        trips = int((d.dMaxDD_pp < 0).sum())
        P(f"- {pname}: {trips} of {len(d)} books trip the MaxDD leg against the live book "
          f"(mean dMaxDD {d.dMaxDD_pp.mean():+.2f} pp, {int((d.dMaxDD_pp >= 0).sum())} shallower); "
          f"mean min-half Sharpe margin {np.minimum(d.dSh_H1, d.dSh_H2).mean():+.4f}.")
    tot = df
    P(f"- BOTH PANELS: {int((tot.dMaxDD_pp < 0).sum())} of {len(tot)} trip, mean dMaxDD "
      f"{tot.dMaxDD_pp.mean():+.2f} pp, mean min-half margin "
      f"{np.minimum(tot.dSh_H1, tot.dSh_H2).mean():+.4f}.")

    # ============================== (B) THE RESTATEMENT ============================
    P("\n## (B) restated 4a against a GROSS-MATCHED incumbent — EVERY grid point\n")
    nreal = int((~df.is_null).sum()); nnull = int(df.is_null.sum())
    P(f"Pass counts over the pooled corpus ({nreal} real, {nnull} null book-panel cells). "
      "`R0` is the CURRENT rule (live book, tau=0) and is the same at every row by construction.\n")
    P("| basis | tau (pp) | real PASS (FULL) | null PASS (FULL) | real PASS (IS) | null PASS (IS) | "
      "real PASS (OOS) | null PASS (OOS) | moves vs R0 (FULL) |")
    P("|---|---|---|---|---|---|---|---|---|")
    for basis in BASES:
        for tau in TAUS:
            g = gd[(gd.basis == basis) & (np.isclose(gd.tau_pp, tau * 100))]
            gr, gn = g[~g.is_null], g[g.is_null]
            moves = int((g.R_FULL != g.R0_CURRENT).sum())
            P(f"| {basis} | {tau*100:.0f} | {int(gr.R_FULL.sum())} of {len(gr)} | "
              f"{int(gn.R_FULL.sum())} of {len(gn)} | {int(gr.R_IS.sum())} of {len(gr)} | "
              f"{int(gn.R_IS.sum())} of {len(gn)} | {int(gr.R_OOS.sum())} of {len(gr)} | "
              f"{int(gn.R_OOS.sum())} of {len(gn)} | {moves} of {len(g)} |")
    r0 = gd[(gd.basis == BASES[0]) & (np.isclose(gd.tau_pp, 0.0))]
    P(f"\nR0 (current rule 4a, live book as incumbent): real PASS "
      f"{int(r0[~r0.is_null].R0_CURRENT.sum())} of {len(r0[~r0.is_null])}, "
      f"null PASS {int(r0[r0.is_null].R0_CURRENT.sum())} of {len(r0[r0.is_null])}.")

    P("\n### Per-book detail at the two tau=0 rungs (the restatement the idea proposes)\n")
    P("| panel | book | gross ratio | dMaxDD vs LIVE (pp) | dMaxDD vs MEAN twin (pp) | "
      "dMaxDD vs DAILY twin (pp) | 4a now | 4a MEAN | 4a DAILY | 4b FULL | 4b OOS |")
    P("|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in df.sort_values(["panel", "family", "book"]).iterrows():
        gm = gd[(gd.panel == r.panel) & (gd.book == r.book) & (np.isclose(gd.tau_pp, 0.0))]
        pm = bool(gm[gm.basis == "MEAN"].R_FULL.iloc[0]); pdl = bool(gm[gm.basis == "DAILY"].R_FULL.iloc[0])
        P(f"| {r.panel} | {r.book} | {r.gross_ratio:.3f} | {r.dMaxDD_pp:+.2f} | "
          f"{r.twin_MEAN_dMaxDD_pp:+.2f} | {r.twin_DAILY_dMaxDD_pp:+.2f} | "
          f"{'Y' if r.KEEP_4a_FULL else '.'} | {'Y' if pm else '.'} | {'Y' if pdl else '.'} | "
          f"{'Y' if r.KEEP_4b_FULL else '.'} | {'Y' if r.KEEP_4b_OOS else '.'} |")

    # ============================== (C) RULE 8 =====================================
    P("\n## (C) rule 8 — (basis, tau) and the book both fitted on 2009-2016 ONLY; 2017-2026 read once\n")
    P("Pre-registered chooser: at each (basis, tau) take the REAL books that pass the restated 4a "
      "on IS rows only, pick the highest IS Sharpe among them (ties -> corpus order), then read "
      "that book's OOS once.  `C_NOW` is the same chooser under the CURRENT rule (live incumbent, "
      "tau=0).  A rung whose IS-pass set admits a NULL is flagged.\n")
    P("| panel | chooser | IS pass set (real) | IS nulls admitted | pick | OOS CAGR | OOS Sharpe | "
      "OOS MaxDD | 4a OOS | 4b OOS |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    for pname, _ in PANELS:
        ref = panel_ref[pname]
        def emit(tag, sub, col):
            cand = sub[(~sub.is_null) & (sub[col])]
            nulls = int(sub[(sub.is_null) & (sub[col])].shape[0])
            if len(cand) == 0:
                P(f"| {pname} | {tag} | 0 | {nulls} | (none) | — | — | — | — | — |")
                pick_rows.append(dict(panel=pname, chooser=tag, n_pass=0, nulls=nulls, pick=None))
                return
            pk = cand.sort_values("IS_Sharpe", ascending=False).iloc[0]
            P(f"| {pname} | {tag} | {len(cand)} | {nulls} | {pk.book} | {pk.OOS_CAGR:.2%} | "
              f"{pk.OOS_Sharpe:.4f} | {pk.OOS_MaxDD:.2%} | {'Y' if pk.KEEP_4a_OOS else '.'} | "
              f"{'Y' if pk.KEEP_4b_OOS else '.'} |")
            pick_rows.append(dict(panel=pname, chooser=tag, n_pass=len(cand), nulls=nulls,
                                  pick=pk.book, OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                  OOS_MaxDD=pk.OOS_MaxDD, KEEP_4a_OOS=bool(pk.KEEP_4a_OOS),
                                  KEEP_4b_OOS=bool(pk.KEEP_4b_OOS)))
        base_sub = gd[(gd.panel == pname) & (gd.basis == BASES[0]) & (np.isclose(gd.tau_pp, 0.0))]
        # C_NOW uses the CURRENT rule's IS legs: the live book is the incumbent.
        cur = df[df.panel == pname].copy()
        cur["_is_pass"] = [bool(x) for x in (cur.IS_Sharpe > panel_ref[pname]["LIVE"]["IS_Sharpe"])
                           & (cur.IS_MaxDD >= panel_ref[pname]["LIVE"]["IS_MaxDD"])]
        emit("C_NOW (live incumbent, tau=0)", cur.rename(columns={"_is_pass": "R_IS"}), "R_IS")
        for basis in BASES:
            for tau in TAUS:
                emit(f"C_{basis}_tau{tau*100:.0f}",
                     gd[(gd.panel == pname) & (gd.basis == basis) & (np.isclose(gd.tau_pp, tau * 100))],
                     "R_IS")
        P(f"| {pname} | *SPY (bar)* | — | — | SPY | {ref['SPY']['OOS_CAGR']:.2%} | "
          f"{ref['SPY']['OOS_Sharpe']:.4f} | {ref['SPY']['OOS_MaxDD']:.2%} | — | — |")
        P(f"| {pname} | *RULES v2 (bar)* | — | — | live | {ref['LIVE']['OOS_CAGR']:.2%} | "
          f"{ref['LIVE']['OOS_Sharpe']:.4f} | {ref['LIVE']['OOS_MaxDD']:.2%} | — | — |")

    # ============================== KEEP census ====================================
    P("\n## Both KEEP paths over the whole corpus (rule 4)\n")
    P("| panel | 4a FULL | 4b FULL | 4a OOS | 4b OOS | BOTH 4b |")
    P("|---|---|---|---|---|---|")
    for pname, _ in PANELS:
        d = df[df.panel == pname]
        P(f"| {pname} | {int(d.KEEP_4a_FULL.sum())} of {len(d)} | {int(d.KEEP_4b_FULL.sum())} of {len(d)} | "
          f"{int(d.KEEP_4a_OOS.sum())} of {len(d)} | {int(d.KEEP_4b_OOS.sum())} of {len(d)} | "
          f"{int((d.KEEP_4b_FULL & d.KEEP_4b_OOS).sum())} of {len(d)} |")

    P("\n## Gates\n")
    ok = sum(1 for _, _, g in gates if g)
    P(f"**{ok} of {len(gates)} pass.**\n")
    P("| gate | value | ok |")
    P("|---|---|---|")
    shown = [g for g in gates if not g[0].startswith("G3 ")]
    g3 = [g for g in gates if g[0].startswith("G3 ")]
    for n, v, o in shown:
        P(f"| {n} | {v} | {'OK' if o else 'FAIL'} |")
    P(f"| G3 DAILY twin target-gross match, all {len(g3)} (book, panel) cells | "
      f"max {max(float(v) for _, v, _ in g3):.3e} | {'OK' if all(o for _, _, o in g3) else 'FAIL'} |")

    (OUT / f"{STEM}.result.md").write_text("\n".join(L) + "\n")
    pd.DataFrame(reg_rows).to_csv(OUT / f"{STEM}.regressions.csv", index=False)
    pd.DataFrame(pick_rows).to_csv(OUT / f"{STEM}.picks.csv", index=False)
    print("\n".join(L))
    print(f"\n[{time.time()-T0:.1f}s]  wrote {STEM}.result.md / .books.csv / .grid.csv / "
          ".regressions.csv / .picks.csv")


if __name__ == "__main__":
    main()
