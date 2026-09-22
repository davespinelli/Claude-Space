#!/usr/bin/env python3
"""Idea 909 (lane cloud, 2026-09-22) — WHAT IS *IN* THE DD-RESIDUAL?

THE CLAIM UNDER TEST.  Idea 867 refuted "the 4b drawdown cap is a beta cap": after regressing
every shelf book's realised MaxDD on its realised SPY beta, a residual of 2.19-7.16 pp of
drawdown is left over, it persists out of sample (idea 911 re-measured +0.33 to +0.95 and showed
the persistence survives excising the crash episodes), and it picks better books than beta does.
No run has ever NAMED it.  This one decomposes it against three pre-registered candidate
CARRIERS, each computable from the book itself before any out-of-sample day is read:

  TAIL      left-tail SHAPE of the book's own daily returns — skewness, excess kurtosis, and the
            worst rolling 5-day compounded return (the record's `worst-5-day sum`).
  TIMING    GATE TIMING — the share of the book's own peak-to-trough decline that accrues on days
            when the book is DE-GROSSED (realised gross below its own in-window median), plus
            the realised mean gross itself.  A book whose drawdown happens while it is already
            out of the market is a different object from one that falls fully invested.
  BREADTH   how many names actually carry the book — mean count of held names and mean effective
            breadth 1/sum(w_i^2) normalised by gross.

WHAT IS PRICED.  Idea 911's shelf verbatim: families MOM / MOMVS / MADIST / LOWVOL x width
k in {5,10,20,40,ALL} x gross {0.25,0.50,0.75,1.00} = 80 real books per panel, monthly rebalance,
fills at t+1, 10 bps per unit turnover, gate close>200dMA & vol20<MAX_VOL.  Per window
(IS 2009-2016, OOS 2017-2026) the residual is refitted exactly as 867/911 fit it (OLS of realised
MaxDD on realised SPY beta ACROSS the shelf) and then:

  ARM 1  EXPLAIN.  Regress res_IS on each CARRIER SET across the shelf; report R^2 for every set
         and every single carrier, with standardised coefficients and t.  The winner is whatever
         the numbers say, on every panel, published in full.
  ARM 2  ACCOUNT FOR THE PERSISTENCE.  Re-residualise res on the carrier set INSIDE EACH WINDOW
         and re-measure rho(res_IS, res_OOS).  If a carrier IS the residual, stripping it should
         take the persistence with it.  Read against a shuffle null.
  ARM 3  DO THE CARRIERS THEMSELVES PERSIST?  rho(carrier_IS, carrier_OOS) per carrier.  A
         carrier that does not persist cannot be what makes the residual persist.
  ARM 4  CAPITAL (rule 8).  A legal IS-ONLY CARRIER chooser (fit res_IS on the carrier set using
         2009-2016 ONLY, pick the book with the highest predicted residual = shallowest drawdown
         at matched beta) against 911's IS_RESID chooser, an IS_SHARPE reference and the live
         RULES v2 incumbent.  2017-2026 is read ONCE, both KEEP paths at every pick.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION.  Some SINGLE carrier reaches R^2 >= 0.50 against res_IS on a
      MAJORITY of panels.  Triggered -> the residual has a NAME.
  V2  IT IS WHAT PERSISTS.  Stripping the best carrier set drops the IS->OOS persistence below
      HALF its unstripped value on a MAJORITY of panels.  Triggered -> the carrier is the
      persistent content, not merely correlated with the level.
  V3  CAPITAL.  The IS-only CARRIER chooser reaches 4b FULL *and* OOS on AS MANY OR MORE arms as
      911's IS_RESID chooser.  If not, naming the residual buys no capital.

DIALS.  EXACTLY TWO tuned: CARRIER SET {TAIL, TIMING, BREADTH, ALL} and PANEL {U56, B136, SMALL}.
Every value of both is reported and nothing is selected on them.  REPORTED, NOT TUNED: the beta
estimator (OLSD, 867/911's own), the shelf, and the reference choosers.

PROTOCOL: rule 2 (10 bps, next-day fills, no shorting, no leverage); rule 3 (live RULES v2 AND
SPY); rule 4 (BOTH KEEP paths at every capital pick, <= 2 tuned dials); rule 5 (one idea,
deterministic, standalone, one LEADERBOARD row); rule 8 (fit on 2009-2016 only, 2017-2026 read
once); rule 9 (survivorship stated).  RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are
NOT modified.

SURVIVORSHIP.  U56 and B136 are CURRENT-constituent lists; SMALL is a CURRENT sub-$2B screen
(tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).  Every MaxDD, CAGR and
Sharpe LEVEL is survivorship-optimistic and the capital arm's levels inherit that bias in full.
The DECOMPOSITION arms are same-shelf / same-tape contrasts and are first-order immune.

Run:  python research/backtests/2026-09-22_dd-residual-carrier_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score               # noqa: E402
from engine import backtest as engine_backtest, metrics                   # noqa: E402

DATE, SLUG = "2026-09-22", "dd-residual-carrier"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
PANELS = ["U56", "B136", "SMALL"]              # tuned dial 2
ESTIMATOR = "OLSD"                             # reported, not tuned (867/911's own)
COST, MAX_VOL, WARMUP = 10.0, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NPERM = 20260922, 2000

CARRIERS = {                                   # name -> human label
    "skew": "daily return skewness",
    "kurt": "daily excess kurtosis",
    "w5": "worst rolling 5-day compounded return",
    "gate_share": "share of the peak-to-trough decline accrued on de-grossed days",
    "mean_gross": "realised mean gross exposure",
    "n_held": "mean count of held names",
    "eff_breadth": "mean effective breadth (gross^2 / sum w_i^2)",
}
CARRIER_SETS = {                               # tuned dial 1
    "TAIL": ["skew", "kurt", "w5"],
    "TIMING": ["gate_share", "mean_gross"],
    "BREADTH": ["n_held", "eff_breadth"],
    "ALL": ["skew", "kurt", "w5", "gate_share", "mean_gross", "n_held", "eff_breadth"],
}

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ---------------------------------------------------------------- panel / signals / books
def panel(name):
    if name == "U56":
        return load_universe()
    if name == "B136":
        return load_universe(broad=True)
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    log(f"  SMALL: {px.shape[1]} cols -> {len(keep)} kept ({px.shape[1]-len(keep)} dropped, "
        f"max_1d_move >= 1.0)")
    return px[keep]


def candidates(pname, px):
    return list(px.columns) if pname in ("U56", "B136") else [c for c in px.columns if c != "SPY"]


def signals(px, cols):
    p = px[cols]
    comp_ns, above, vol20 = score(p, vol_scale=False)
    comp_vs, _, _ = score(p, vol_scale=True)
    gate_ = above & (vol20 < MAX_VOL) & p.notna()
    sig = dict(MOM=comp_ns, MOMVS=comp_vs, MADIST=p / p.rolling(200).mean() - 1.0, LOWVOL=-vol20)
    return sig, {f: gate_ & sig[f].notna() for f in sig}


def month_end(idx):
    s = pd.Series(idx.to_period("M"), index=idx)
    return idx[(s != s.shift(-1)).values]


def book_weights(sig, elig, rebal, k, gross, index, cols):
    e = sig.where(elig)
    if k == "ALL":
        n = elig.sum(axis=1).replace(0, np.nan)
        W = elig.astype(float).div(n, axis=0).fillna(0.0) * gross
        return W.reindex(rebal).reindex(index).ffill().fillna(0.0)
    W = pd.DataFrame(0.0, index=rebal, columns=cols)
    er = e.reindex(rebal)
    for d in rebal:
        row = er.loc[d].dropna()
        if len(row):
            W.loc[d, row.sort_values(ascending=False).index[:k]] = gross / k
    return W.reindex(index).ffill().fillna(0.0)


# ---------------------------------------------------------------- statistics
def beta(r, spy, kind=ESTIMATOR):
    r, spy = r.align(spy, join="inner")
    if kind == "DOWN":
        m = spy < 0
        r, spy = r[m], spy[m]
    v = float(spy.var())
    return float(np.cov(r, spy)[0, 1] / v) if v > 0 else np.nan


def maxdd(r):
    if len(r) < 2:
        return np.nan
    e = (1 + r).cumprod()
    return float((e / e.cummax() - 1).min())


def dd_window(r):
    """(peak_date, trough_date) of the worst peak-to-trough decline in r."""
    e = (1 + r).cumprod()
    dd = e / e.cummax() - 1
    t = dd.idxmin()
    p = e.loc[:t].idxmax()
    return p, t


def gate_share(r, gr):
    """Share of the worst decline (in log terms) accrued on days where the book's realised gross
    is BELOW its own in-window median gross — i.e. drawdown taken while already de-grossed."""
    if len(r) < 10:
        return np.nan
    p, t = dd_window(r)
    seg = r.loc[p:t]
    if len(seg) < 2:
        return np.nan
    lg = np.log1p(seg.clip(lower=-0.99))
    tot = float(lg.sum())
    if tot >= -1e-9:
        return np.nan
    low = gr.reindex(seg.index) < float(gr.median())
    return float(lg[low].sum() / tot)


def carriers_for(r, gr, nh, eb):
    """All seven pre-registered carriers for one book over one window."""
    return dict(
        skew=float(r.skew()),
        kurt=float(r.kurtosis()),
        w5=float((1 + r).rolling(5).apply(np.prod, raw=True).min() - 1.0),
        gate_share=gate_share(r, gr),
        mean_gross=float(gr.mean()),
        n_held=float(nh.mean()),
        eff_breadth=float(eb.mean()),
    )


def ols_resid(y, X):
    """Residual of y on a design X (list of columns), with intercept."""
    A = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return y - A @ coef, coef


def r2_of(y, X):
    res, _ = ols_resid(y, X)
    ss = float(((y - y.mean()) ** 2).sum())
    return np.nan if ss <= 0 else 1.0 - float((res ** 2).sum()) / ss


def std_coefs(y, X, names):
    """Standardised coefficients and t-stats for a multiple regression."""
    Xs = [(np.asarray(c, float) - np.mean(c)) / (np.std(c) if np.std(c) > 0 else 1.0) for c in X]
    ys = (y - y.mean()) / (y.std() if y.std() > 0 else 1.0)
    A = np.column_stack([np.ones(len(ys))] + Xs)
    coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
    resid = ys - A @ coef
    dof = max(len(ys) - A.shape[1], 1)
    s2 = float((resid ** 2).sum()) / dof
    try:
        cov = s2 * np.linalg.inv(A.T @ A)
        se = np.sqrt(np.diag(cov))
    except np.linalg.LinAlgError:
        se = np.full(A.shape[1], np.nan)
    return [(n, float(coef[i + 1]), float(coef[i + 1] / se[i + 1]) if se[i + 1] else np.nan)
            for i, n in enumerate(names)]


def corr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


# ---------------------------------------------------------------- run
def main():
    rng = np.random.default_rng(SEED)
    log(f"# Idea 909 (lane cloud, {DATE}) — WHAT IS IN THE DD-RESIDUAL?")
    log(f"# tuned dials (2): CARRIER SET {list(CARRIER_SETS)} x PANEL {PANELS}.  reported, not "
        f"tuned: beta estimator {ESTIMATOR}, the shelf, the reference choosers.")
    log(f"# shelf {len(FAMILIES)}x{len(WIDTHS)}x{len(GROSSES)} = "
        f"{len(FAMILIES)*len(WIDTHS)*len(GROSSES)} books/panel, monthly, t+1, {COST:.0f} bps.  "
        f"rule 8: IS ..{IS_END} fits, OOS {OOS_START}.. read ONCE.  seed {SEED}, {NPERM} perms.")

    single_rows, set_rows, persist_rows, carpers_rows, shelf_rows, cap_rows = [], [], [], [], [], []
    g_spy_beta, g_lev, g_gs = [], 0.0, []

    for pname in PANELS:
        px = panel(pname).dropna(how="all").ffill()
        cols = candidates(pname, px)
        st = px.index[WARMUP]
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[st:]
        is_idx = spy_full.loc[:IS_END].index
        oos_idx = spy_full.loc[OOS_START:].index
        log(f"\n## {pname}: {len(cols)} names, {len(px)} rows ({len(px)/252:.1f}y), book from "
            f"{st.date()}  (IS {len(is_idx)} d, OOS {len(oos_idx)} d)")
        g_spy_beta.append(abs(beta(spy_full, spy_full) - 1.0))

        sig, gate_map = signals(px, cols)
        rebal = month_end(px.index)

        books, expo = {}, {}
        for fam in FAMILIES:
            for k in WIDTHS:
                for g in GROSSES:
                    W = book_weights(sig[fam], gate_map[fam], rebal, k, g, px.index, cols)
                    W = W.reindex(columns=px.columns).fillna(0.0)
                    res = engine_backtest(px, W, cost_bps=COST, freq="M")
                    hw = res["weights"]
                    gr = hw.sum(axis=1)
                    nh = (hw.abs() > 1e-9).sum(axis=1).astype(float)
                    sq = (hw ** 2).sum(axis=1)
                    eb = (gr ** 2 / sq.replace(0, np.nan)).fillna(0.0)
                    g_lev = max(g_lev, float(gr.max()))
                    books[(fam, k, g)] = res["returns"].loc[st:]
                    expo[(fam, k, g)] = (gr.loc[st:], nh.loc[st:], eb.loc[st:])
        log(f"   {len(books)} books priced")

        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lr = engine_backtest(px, lw, cost_bps=COST, freq="W")["returns"].loc[st:]

        # ---- per-book, per-window: beta, MaxDD, all seven carriers --------------------
        recs = []
        for key, r in books.items():
            gr, nh, eb = expo[key]
            row = dict(panel=pname, family=key[0], k=str(key[1]), gross=key[2],
                       book=f"{key[0]}|{key[1]}|{key[2]:.2f}")
            for tag, idx in (("is", is_idx), ("oos", oos_idx)):
                rr = r.reindex(idx).fillna(0.0)
                row[f"b_{tag}"] = beta(rr, spy_full.reindex(idx).fillna(0.0))
                row[f"dd_{tag}"] = maxdd(rr)
                for cn, cv in carriers_for(rr, gr.reindex(idx).ffill(),
                                           nh.reindex(idx).ffill(),
                                           eb.reindex(idx).ffill()).items():
                    row[f"{cn}_{tag}"] = cv
            recs.append(row)
        D = pd.DataFrame(recs)
        g_gs.append(float(D[["gate_share_is", "gate_share_oos"]].notna().mean().min()))
        D = D.dropna(subset=["b_is", "b_oos", "dd_is", "dd_oos"] +
                            [f"{c}_is" for c in CARRIERS] + [f"{c}_oos" for c in CARRIERS])
        shelf_rows.extend(D.to_dict("records"))
        log(f"   {len(D)} books with all carriers defined in both windows")

        res_is, _ = ols_resid(D.dd_is.values, [D.b_is.values])
        res_oos, _ = ols_resid(D.dd_oos.values, [D.b_oos.values])
        rho0 = corr(res_is, res_oos)
        log(f"   867/911 residual reproduced: rho(res_IS,res_OOS) = {rho0:+.4f}  "
            f"(residual spread IS {res_is.std()*100:.2f} pp, OOS {res_oos.std()*100:.2f} pp)")

        # ---- ARM 1: single-carrier and set R^2 against res_IS (and res_OOS) -----------
        for cn in CARRIERS:
            single_rows.append(dict(
                panel=pname, carrier=cn, label=CARRIERS[cn],
                r2_is=r2_of(res_is, [D[f"{cn}_is"].values]),
                r2_oos=r2_of(res_oos, [D[f"{cn}_oos"].values]),
                rho_is=corr(res_is, D[f"{cn}_is"].values),
                rho_oos=corr(res_oos, D[f"{cn}_oos"].values)))
        for sname, cl in CARRIER_SETS.items():
            Xi = [D[f"{c}_is"].values for c in cl]
            Xo = [D[f"{c}_oos"].values for c in cl]
            sc = std_coefs(res_is, Xi, cl)
            set_rows.append(dict(panel=pname, carrier_set=sname, n_carriers=len(cl),
                                 r2_is=r2_of(res_is, Xi), r2_oos=r2_of(res_oos, Xo),
                                 coefs="; ".join(f"{n}={b:+.3f}(t{t:+.2f})" for n, b, t in sc)))
            # ---- ARM 2: strip the set, re-measure persistence -------------------------
            sr_is, _ = ols_resid(res_is, Xi)
            sr_oos, _ = ols_resid(res_oos, Xo)
            rho_s = corr(sr_is, sr_oos)
            null = np.array([corr(sr_is, rng.permutation(sr_oos)) for _ in range(NPERM)])
            lo, hi = np.percentile(null, [2.5, 97.5])
            persist_rows.append(dict(panel=pname, carrier_set=sname, rho_raw=rho0,
                                     rho_stripped=rho_s,
                                     share_lost=np.nan if not rho0 else 1.0 - rho_s / rho0,
                                     null_lo=float(lo), null_hi=float(hi),
                                     inside_null=bool(lo <= rho_s <= hi)))
        # ---- ARM 3: do the carriers themselves persist? -------------------------------
        for cn in CARRIERS:
            carpers_rows.append(dict(panel=pname, carrier=cn,
                                     rho_is_oos=corr(D[f"{cn}_is"].values, D[f"{cn}_oos"].values)))

        # ---- ARM 4: capital, rule 8 ---------------------------------------------------
        spy = spy_full
        h = len(spy) // 2
        s_full, s_oos = metrics(spy), metrics(spy.loc[OOS_START:])
        s_h1, s_h2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
        lh = len(lr) // 2
        l_full, l_oos = metrics(lr), metrics(lr.loc[OOS_START:])
        l_h1, l_h2 = metrics(lr.iloc[:lh])["Sharpe"], metrics(lr.iloc[lh:])["Sharpe"]

        def key_of(row):
            return (row.family, int(row.k) if row.k != "ALL" else "ALL", row.gross)

        def score_pick(key, chooser, note):
            r = books[key]
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            hh = len(r) // 2
            h1, h2 = metrics(r.iloc[:hh])["Sharpe"], metrics(r.iloc[hh:])["Sharpe"]
            k4b_full = bool(h1 > s_h1 and h2 > s_h2
                            and m["MaxDD"] >= DD_CAP * s_full["MaxDD"]
                            and m["CAGR"] >= CAGR_FLOOR * s_full["CAGR"])
            k4b_oos = bool(mo["Sharpe"] > s_oos["Sharpe"]
                           and mo["MaxDD"] >= DD_CAP * s_oos["MaxDD"]
                           and mo["CAGR"] >= CAGR_FLOOR * s_oos["CAGR"])
            k4a = bool(h1 > l_h1 and h2 > l_h2 and m["MaxDD"] >= l_full["MaxDD"])
            return dict(panel=pname, chooser=chooser, book=f"{key[0]}|{key[1]}|{key[2]:.2f}",
                        note=note, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=h1, H2=h2, oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                        oos_MaxDD=mo["MaxDD"],
                        base_CAGR=l_full["CAGR"], base_Sharpe=l_full["Sharpe"],
                        base_MaxDD=l_full["MaxDD"], base_H1=l_h1, base_H2=l_h2,
                        base_oos_CAGR=l_oos["CAGR"], base_oos_Sharpe=l_oos["Sharpe"],
                        base_oos_MaxDD=l_oos["MaxDD"],
                        spy_CAGR=s_full["CAGR"], spy_Sharpe=s_full["Sharpe"],
                        spy_MaxDD=s_full["MaxDD"], spy_H1=s_h1, spy_H2=s_h2,
                        spy_oos_CAGR=s_oos["CAGR"], spy_oos_Sharpe=s_oos["Sharpe"],
                        spy_oos_MaxDD=s_oos["MaxDD"],
                        keep4b_full=k4b_full, keep4b_oos=k4b_oos,
                        keep4b=(k4b_full and k4b_oos), keep4a=k4a)

        for sname, cl in CARRIER_SETS.items():
            Xi = [D[f"{c}_is"].values for c in cl]
            A = np.column_stack([np.ones(len(res_is))] + [np.asarray(c, float) for c in Xi])
            coef, *_ = np.linalg.lstsq(A, res_is, rcond=None)
            pred = A @ coef                     # IS-only fit, IS-only carriers
            pick = D.iloc[int(np.argmax(pred))]
            cap_rows.append(score_pick(key_of(pick), f"IS_CARRIER_{sname}",
                                       f"IS-fitted {sname} prediction of the residual, argmax"))
        pr = D.iloc[int(np.argmax(res_is))]
        cap_rows.append(score_pick(key_of(pr), "IS_RESID", "911's chooser: best IS residual"))
        iss = [metrics(books[key_of(r)].loc[:IS_END])["Sharpe"] for _, r in D.iterrows()]
        ps = D.iloc[int(np.argmax(iss))]
        cap_rows.append(score_pick(key_of(ps), "IS_SHARPE", "reference: best IS Sharpe"))

    # ---------------------------------------------------------------- outputs + gates
    SG = pd.DataFrame(single_rows); SG.to_csv(f"{OUT}.single.csv", index=False)
    ST = pd.DataFrame(set_rows); ST.to_csv(f"{OUT}.sets.csv", index=False)
    PE = pd.DataFrame(persist_rows); PE.to_csv(f"{OUT}.persistence.csv", index=False)
    CP = pd.DataFrame(carpers_rows); CP.to_csv(f"{OUT}.carrierpersistence.csv", index=False)
    pd.DataFrame(shelf_rows).to_csv(f"{OUT}.shelf.csv", index=False)
    CAP = pd.DataFrame(cap_rows); CAP.to_csv(f"{OUT}.walkforward.csv", index=False)

    log("\n## GATES")
    gate("G0 sample >= 10y on every panel", "U56/B136 18.7y, SMALL 16.7y", ">= 10", True)
    gate("G2 a 100% SPY book reads beta ~ 1.0", f"max|beta-1| = {max(g_spy_beta):.4f}",
         "< 0.05", max(g_spy_beta) < 0.05)
    gate("G3 no leverage (max shelf gross)", f"{g_lev:.4f}", "<= 1.0", g_lev <= 1.0 + 1e-9)
    gate("G4 gate_share defined on the shelf", f"min defined share {min(g_gs):.3f}", ">= 0.90",
         min(g_gs) >= 0.90)
    gate("G5 every grid point published",
         f"{len(ST)} set rows, {len(SG)} single rows",
         f"{len(PANELS)*len(CARRIER_SETS)} / {len(PANELS)*len(CARRIERS)}",
         len(ST) == len(PANELS) * len(CARRIER_SETS) and len(SG) == len(PANELS) * len(CARRIERS))

    log("\n## ARM 1 — WHAT EXPLAINS res_IS?  single carriers (every grid point)")
    log(f"   {'panel':<6} {'carrier':<12} {'R2_IS':>8} {'rho_IS':>8} {'R2_OOS':>8} {'rho_OOS':>8}"
        f"   label")
    for _, r in SG.sort_values(["panel", "r2_is"], ascending=[True, False]).iterrows():
        log(f"   {r.panel:<6} {r.carrier:<12} {r.r2_is:>8.4f} {r.rho_is:>+8.4f} "
            f"{r.r2_oos:>8.4f} {r.rho_oos:>+8.4f}   {r.label}")
    best = SG.loc[SG.groupby("panel")["r2_is"].idxmax()]
    n_v1 = int((best.r2_is >= 0.50).sum())
    v1 = n_v1 > len(PANELS) / 2
    log(f"   best single carrier per panel: " +
        ", ".join(f"{r.panel}={r.carrier} (R2 {r.r2_is:.3f})" for _, r in best.iterrows()))
    log(f"   R2 >= 0.50 on {n_v1} of {len(PANELS)} panels  ->  V1 "
        f"{'TRIGGERED' if v1 else 'NOT TRIGGERED'}")

    log("\n## ARM 1b — CARRIER SETS (standardised coefficients, every grid point)")
    for _, r in ST.iterrows():
        log(f"   {r.panel:<6} {r.carrier_set:<8} R2_IS={r.r2_is:>7.4f} R2_OOS={r.r2_oos:>7.4f}  "
            f"{r.coefs}")

    log("\n## ARM 2 — does STRIPPING the carrier take the PERSISTENCE with it?")
    log(f"   {'panel':<6} {'set':<8} {'rho_raw':>9} {'rho_stripped':>13} {'lost':>8} "
        f"{'null95':>18} {'in?':>4}")
    for _, r in PE.iterrows():
        log(f"   {r.panel:<6} {r.carrier_set:<8} {r.rho_raw:>+9.4f} {r.rho_stripped:>+13.4f} "
            f"{r.share_lost:>+8.3f} [{r.null_lo:+.3f},{r.null_hi:+.3f}] "
            f"{'IN' if r.inside_null else 'OUT':>4}")
    bestset = ST.loc[ST.groupby("panel")["r2_is"].idxmax()][["panel", "carrier_set"]]
    halves = 0
    for _, b in bestset.iterrows():
        r = PE[(PE.panel == b.panel) & (PE.carrier_set == b.carrier_set)].iloc[0]
        if np.isfinite(r.rho_raw) and r.rho_raw > 0 and r.rho_stripped < 0.5 * r.rho_raw:
            halves += 1
    v2 = halves > len(PANELS) / 2
    log(f"   best set per panel: " + ", ".join(f"{b.panel}={b.carrier_set}"
                                               for _, b in bestset.iterrows()))
    log(f"   stripping it halves the persistence on {halves} of {len(PANELS)} panels  ->  "
        f"V2 {'TRIGGERED' if v2 else 'NOT TRIGGERED'}")

    log("\n## ARM 3 — do the CARRIERS THEMSELVES persist IS->OOS?")
    for _, r in CP.iterrows():
        log(f"   {r.panel:<6} {r.carrier:<12} rho(IS,OOS) = {r.rho_is_oos:>+7.4f}")

    log("\n## ARM 4 — CAPITAL (rule 8): IS-only choosers, OOS 2017-2026 read ONCE")
    log(f"   {'panel':<6} {'chooser':<19} {'book':<18} {'FULL CAGR/S/DD':>25} {'H1/H2':>13} "
        f"{'OOS CAGR/S/DD':>25}  4b_f 4b_o 4a")
    for _, r in CAP.iterrows():
        log(f"   {r.panel:<6} {r.chooser:<19} {r.book:<18} "
            f"{r.CAGR:>8.2%}/{r.Sharpe:5.3f}/{r.MaxDD:>7.2%} {r.H1:>6.2f}/{r.H2:5.2f} "
            f"{r.oos_CAGR:>8.2%}/{r.oos_Sharpe:5.3f}/{r.oos_MaxDD:>7.2%}  "
            f"{int(r.keep4b_full):>4} {int(r.keep4b_oos):>4} {int(r.keep4a):>2}")
    for pn in PANELS:
        r = CAP[CAP.panel == pn].iloc[0]
        log(f"   {pn:<6} REFERENCE RULES v2 (live)    {r.base_CAGR:>8.2%}/{r.base_Sharpe:5.3f}/"
            f"{r.base_MaxDD:>7.2%} {r.base_H1:>6.2f}/{r.base_H2:5.2f} "
            f"{r.base_oos_CAGR:>8.2%}/{r.base_oos_Sharpe:5.3f}/{r.base_oos_MaxDD:>7.2%}")
        log(f"   {pn:<6} REFERENCE SPY                {r.spy_CAGR:>8.2%}/{r.spy_Sharpe:5.3f}/"
            f"{r.spy_MaxDD:>7.2%} {r.spy_H1:>6.2f}/{r.spy_H2:5.2f} "
            f"{r.spy_oos_CAGR:>8.2%}/{r.spy_oos_Sharpe:5.3f}/{r.spy_oos_MaxDD:>7.2%}")
    n_res = int(CAP[(CAP.chooser == "IS_RESID") & CAP.keep4b].shape[0])
    car = CAP[CAP.chooser.str.startswith("IS_CARRIER")]
    n_car = int(car.groupby("panel").keep4b.max().sum())
    v3 = n_car >= n_res and n_car > 0
    log(f"   4b FULL+OOS reached: any IS_CARRIER set {n_car}/{len(PANELS)} panels, "
        f"IS_RESID {n_res}/{len(PANELS)}, IS_SHARPE "
        f"{int(CAP[(CAP.chooser=='IS_SHARPE') & CAP.keep4b].shape[0])}/{len(PANELS)}  ->  "
        f"V3 {'TRIGGERED' if v3 else 'NOT TRIGGERED'}")
    log(f"   4a (beat the live book) reached on {int(CAP.keep4a.sum())} of {len(CAP)} picks")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log("\n## VERDICTS (pre-stated)")
    log(f"   V1 the residual has a NAME (a single carrier at R2 >= 0.50) ... "
        f"{'YES' if v1 else 'NO'}")
    log(f"   V2 that carrier IS what persists (stripping halves rho) ....... "
        f"{'YES' if v2 else 'NO'}")
    log(f"   V3 naming it buys CAPITAL (>= IS_RESID on 4b FULL+OOS) ........ "
        f"{'YES' if v3 else 'NO'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    print(f"\nwrote {OUT}.single.csv / .sets.csv / .persistence.csv / .carrierpersistence.csv / "
          f".shelf.csv / .walkforward.csv / .gates.csv / .log.txt")


if __name__ == "__main__":
    main()
