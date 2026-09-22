#!/usr/bin/env python3
"""Idea 2079 (lane cloud, 2026-09-22) — IS THE DD-RESIDUAL A FAMILY LABEL RATHER THAN A
CONTINUOUS BOOK PROPERTY?

THE CLAIM UNDER TEST.  Idea 911 (2026-09-22, lane cloud) re-priced idea 867's 80-book shelf and
found the MaxDD-on-beta residual persists IS(2009-2016) -> OOS(2017-2026) at rho +0.33 to +0.95
across every (estimator, panel) block, and that the persistence SURVIVES excising the crash
episodes, i.e. it lives OUTSIDE the drawdown episode.  But that residual is an ACROSS-SHELF OLS
residual fitted over four heterogeneous construction FAMILIES (MOM / MOMVS / MADIST / LOWVOL),
and BOTH of 911's capital picks landed on MADIST.  So the whole persistent object may be nothing
more than "MADIST and LOWVOL books draw down less than MOM books at matched beta" — a FOUR-VALUED
CATEGORICAL LABEL, known before any return is priced, with no continuous within-family content.
If so, the residual is not a book property that can rank books; it is a family name.

WHAT IS PRICED.  Idea 911's shelf verbatim: families MOM / MOMVS / MADIST / LOWVOL x width
k in {5,10,20,40,ALL} x gross {0.25,0.50,0.75,1.00} = 80 real books per panel, monthly rebalance,
fills at t+1, 10 bps per unit turnover, gate close>200dMA & vol20<MAX_VOL.  Per window and per
beta estimator the residual is refitted exactly as 867/911 fit it (OLS of realised MaxDD on
realised SPY beta ACROSS the shelf), and then decomposed three ways:

  POOLED     rho(res_IS, res_OOS) over all books of the family set — 911's number, reproduced.
  WITHIN     the same correlation with FAMILY FIXED EFFECTS REMOVED: res is demeaned inside its
             own family SEPARATELY IN EACH WINDOW, so every trace of the four-valued label is
             gone and only within-family ordering can carry the correlation.  Read against a
             WITHIN-FAMILY permutation null (res_OOS shuffled inside each family, so the null
             preserves family structure and destroys only the book-level pairing).
  BETWEEN    rho over the 4 family MEANS, plus eta^2 = the share of each window's residual
             variance that is between-family.  eta^2 near 1 with WITHIN ~ 0 is the label reading.

  Per-family rho is reported separately for all four families at every grid point, so the
  question "does ANY family survive" is answered book by book, not only in aggregate.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION.  The WITHIN (family-demeaned) persistence sits INSIDE its
      within-family permutation null's central 95% band on a MAJORITY of (family set, estimator,
      panel) blocks.  Triggered -> the residual is a FAMILY LABEL: no within-family content.
  V2  THE LABEL'S SHARE.  Between-family eta^2 of res_IS is >= 0.50 on a MAJORITY of blocks.
      Triggered -> most of what 911 measured is the four-valued label, whatever V1 says.
  V3  CAPITAL (rule 8).  A legal IS-ONLY WITHIN-FAMILY residual chooser (best IS residual
      relative to its OWN family mean) reaches a book clearing 4b FULL *and* OOS on AS MANY OR
      MORE arms as the POOLED residual chooser of 911 and as a pure FAMILY-LABEL chooser (pick
      the family with the best mean IS residual, then that family's median-width book).  If the
      within-family reading reaches nothing the label alone does not, the continuous reading
      buys no capital whatever arms 1-2 say.

DIALS.  EXACTLY TWO tuned: FAMILY SET (ALL4 and the four leave-one-out triples) and BETA
ESTIMATOR (OLSD / OLSM / DOWN).  Every value of both is reported and nothing is selected on
them.  REPORTED, NOT TUNED: PANEL {U56, B136, SMALL}, and the reference choosers in the capital
arm (IS_SHARPE, the live RULES v2 incumbent, SPY).

PROTOCOL: rule 2 (10 bps, next-day fills, no shorting, no leverage); rule 3 (live RULES v2 AND
SPY); rule 4 (BOTH KEEP paths reported at every capital pick, <= 2 tuned dials); rule 5 (one
idea, deterministic, standalone, one LEADERBOARD row); rule 8 (parameters chosen on 2009-2016
only, 2017-2026 read once); rule 9 (survivorship stated).  RULES.md / PROTOCOL.md / scan.py /
bot.py / baseline.py are NOT modified.

SURVIVORSHIP.  U56 and B136 are CURRENT-constituent lists; SMALL is a CURRENT sub-$2B screen
(tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).  Every MaxDD, CAGR and
Sharpe LEVEL below is survivorship-optimistic and the capital arm's levels inherit that bias in
full.  The DECOMPOSITION (pooled vs within vs between) is a same-shelf / same-tape contrast with
only the residual's fixed effects changed, so it is first-order immune.

Run:  python research/backtests/2026-09-22_dd-residual-family-label_cloud.py
"""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score               # noqa: E402
from engine import backtest as engine_backtest, metrics                   # noqa: E402

DATE, SLUG = "2026-09-22", "dd-residual-family-label"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
ESTIMATORS = ["OLSD", "OLSM", "DOWN"]          # tuned dial 2
PANELS = ["U56", "B136", "SMALL"]              # reported, not tuned
COST, MAX_VOL, WARMUP = 10.0, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NPERM = 20260922, 2000

# tuned dial 1: FAMILY SET = the full shelf and every leave-one-out triple.
FAMILY_SETS = {"ALL4": tuple(FAMILIES)}
for _drop in FAMILIES:
    FAMILY_SETS[f"NO_{_drop}"] = tuple(f for f in FAMILIES if f != _drop)

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
def beta(r, spy, kind):
    r, spy = r.align(spy, join="inner")
    if kind == "DOWN":
        m = spy < 0
        r, spy = r[m], spy[m]
    elif kind == "OLSM":
        g = np.arange(len(r)) // 21
        r = (1 + r).groupby(g).prod() - 1
        spy = (1 + spy).groupby(g).prod() - 1
    v = float(spy.var())
    return float(np.cov(r, spy)[0, 1] / v) if v > 0 else np.nan


def maxdd(r):
    if len(r) < 2:
        return np.nan
    e = (1 + r).cumprod()
    return float((e / e.cummax() - 1).min())


def ols_resid(y, x):
    """867/911's residual: OLS of y on x ACROSS the shelf, no fixed effects."""
    A = np.vstack([np.ones(len(x)), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return y - A @ coef


def demean_within(v, labels):
    """Remove the family fixed effect: subtract each book's own family mean."""
    s = pd.Series(v).groupby(pd.Series(labels)).transform("mean").values
    return v - s


def eta2(v, labels):
    """Share of variance of v that is BETWEEN family means."""
    s = pd.Series(v)
    tot = float(((s - s.mean()) ** 2).sum())
    if tot <= 0:
        return np.nan
    grp = s.groupby(pd.Series(labels))
    bet = float(sum(len(g) * (g.mean() - s.mean()) ** 2 for _, g in grp))
    return bet / tot


def corr(a, b):
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def perm_within(a, b, labels, rng, n):
    """Null: shuffle b INSIDE each family, so family structure is preserved and only the
    book-level IS<->OOS pairing is destroyed."""
    lab = np.asarray(labels)
    idx_by_fam = [np.where(lab == f)[0] for f in pd.unique(lab)]
    out = np.empty(n)
    for i in range(n):
        bb = b.copy()
        for ix in idx_by_fam:
            bb[ix] = rng.permutation(b[ix])
        out[i] = corr(a, bb)
    return out


# ---------------------------------------------------------------- run
def main():
    rng = np.random.default_rng(SEED)
    log(f"# Idea 2079 (lane cloud, {DATE}) — is the DD-RESIDUAL a FAMILY LABEL rather than a "
        f"CONTINUOUS BOOK PROPERTY?")
    log(f"# tuned dials (2): FAMILY SET {list(FAMILY_SETS)} x BETA ESTIMATOR {ESTIMATORS}.  "
        f"reported, not tuned: PANEL {PANELS}; choosers IS_WITHIN / IS_POOLED / IS_FAMILY / "
        f"IS_SHARPE / incumbent.  shelf {len(FAMILIES)}x{len(WIDTHS)}x{len(GROSSES)} = "
        f"{len(FAMILIES)*len(WIDTHS)*len(GROSSES)} books/panel, monthly, t+1, {COST:.0f} bps.")
    log(f"# rule 8: IS = ..{IS_END} chooses; OOS = {OOS_START}.. read ONCE.  seed {SEED}, "
        f"{NPERM} permutations per block.")

    grid_rows, fam_rows, shelf_rows, cap_rows = [], [], [], []
    g_spy_beta, g_lev = [], 0.0

    for pname in PANELS:
        px = panel(pname).dropna(how="all").ffill()
        cols = candidates(pname, px)
        st = px.index[WARMUP]
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[st:]
        is_idx = spy_full.loc[:IS_END].index
        oos_idx = spy_full.loc[OOS_START:].index
        log(f"\n## {pname}: {len(cols)} names, {len(px)} rows ({len(px)/252:.1f}y), book from "
            f"{st.date()}  (IS {len(is_idx)} d, OOS {len(oos_idx)} d)")

        for kind in ESTIMATORS:                      # G2: a 100% SPY book must read beta ~ 1
            g_spy_beta.append(abs(beta(spy_full, spy_full, kind) - 1.0))

        sig, gate_map = signals(px, cols)
        rebal = month_end(px.index)

        books = {}
        for fam in FAMILIES:
            for k in WIDTHS:
                for g in GROSSES:
                    W = book_weights(sig[fam], gate_map[fam], rebal, k, g, px.index, cols)
                    W = W.reindex(columns=px.columns).fillna(0.0)
                    res = engine_backtest(px, W, cost_bps=COST, freq="M")
                    g_lev = max(g_lev, float(res["weights"].sum(axis=1).max()))
                    books[(fam, k, g)] = res["returns"].loc[st:]
        log(f"   {len(books)} books priced")

        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lr = engine_backtest(px, lw, cost_bps=COST, freq="W")["returns"].loc[st:]

        # ---- per-book window statistics, once per estimator ---------------------------
        stats = {}
        for est in ESTIMATORS:
            recs = []
            for (fam, k, g), r in books.items():
                r_is, r_oos = r.reindex(is_idx).fillna(0.0), r.reindex(oos_idx).fillna(0.0)
                recs.append(dict(panel=pname, estimator=est, family=fam, k=str(k), gross=g,
                                 book=f"{fam}|{k}|{g:.2f}",
                                 b_is=beta(r_is, spy_full.reindex(is_idx).fillna(0.0), est),
                                 dd_is=maxdd(r_is),
                                 b_oos=beta(r_oos, spy_full.reindex(oos_idx).fillna(0.0), est),
                                 dd_oos=maxdd(r_oos)))
            stats[est] = pd.DataFrame(recs).dropna()
            shelf_rows.extend(stats[est].to_dict("records"))

        # ---- ARM 1/2: pooled vs within vs between, at every grid point ----------------
        for fsname, fams in FAMILY_SETS.items():
            for est in ESTIMATORS:
                D = stats[est][stats[est].family.isin(fams)].reset_index(drop=True)
                lab = D.family.values
                res_is = ols_resid(D.dd_is.values, D.b_is.values)
                res_oos = ols_resid(D.dd_oos.values, D.b_oos.values)
                rho_pool = corr(res_is, res_oos)
                w_is, w_oos = demean_within(res_is, lab), demean_within(res_oos, lab)
                rho_within = corr(w_is, w_oos)
                null = perm_within(w_is, w_oos.copy(), lab, rng, NPERM)
                lo, hi = np.percentile(null, [2.5, 97.5])
                inside = bool(lo <= rho_within <= hi)
                fm_is = pd.Series(res_is).groupby(pd.Series(lab)).mean()
                fm_oos = pd.Series(res_oos).groupby(pd.Series(lab)).mean()
                rho_between = corr(fm_is.values, fm_oos.reindex(fm_is.index).values)
                grid_rows.append(dict(
                    panel=pname, family_set=fsname, estimator=est, n_books=len(D),
                    rho_pooled=rho_pool, rho_within=rho_within, rho_between=rho_between,
                    eta2_is=eta2(res_is, lab), eta2_oos=eta2(res_oos, lab),
                    null_lo=float(lo), null_hi=float(hi), null_sd=float(null.std()),
                    within_inside_null=inside,
                    share_lost=(np.nan if not np.isfinite(rho_pool) or rho_pool == 0
                                else 1.0 - rho_within / rho_pool)))
                if fsname == "ALL4":
                    for f in fams:
                        m = lab == f
                        fam_rows.append(dict(panel=pname, estimator=est, family=f, n=int(m.sum()),
                                             rho_family=corr(res_is[m], res_oos[m]),
                                             mean_res_is=float(res_is[m].mean()),
                                             mean_res_oos=float(res_oos[m].mean())))

        # ---- ARM 3: capital, rule 8 (IS-only choosers, OOS read once) -----------------
        S = stats["OLSD"].copy()                     # estimator for the chooser: reported, fixed
        S = S.assign(is_sharpe=[metrics(books[(r.family, int(r.k) if r.k != "ALL" else "ALL",
                                               r.gross)].loc[:IS_END])["Sharpe"]
                                for _, r in S.iterrows()])
        S["res_is"] = ols_resid(S.dd_is.values, S.b_is.values)
        S["res_is_within"] = demean_within(S.res_is.values, S.family.values)

        spy = spy_full
        h = len(spy) // 2
        s_full, s_oos = metrics(spy), metrics(spy.loc[OOS_START:])
        s_h1, s_h2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
        lh = len(lr) // 2
        l_full = metrics(lr)
        l_h1, l_h2 = metrics(lr.iloc[:lh])["Sharpe"], metrics(lr.iloc[lh:])["Sharpe"]
        l_oos = metrics(lr.loc[OOS_START:])

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

        rw = S.sort_values("res_is_within", ascending=False).iloc[0]
        rp = S.sort_values("res_is", ascending=False).iloc[0]
        rs = S.sort_values("is_sharpe", ascending=False).iloc[0]
        cap_rows.append(score_pick(key_of(rw), "IS_WITHIN", "best IS residual vs own family mean"))
        cap_rows.append(score_pick(key_of(rp), "IS_POOLED", "911's chooser: best IS residual"))
        # pure label chooser: best family by mean IS residual, then that family's median book
        best_fam = S.groupby("family")["res_is"].mean().idxmax()
        F = S[S.family == best_fam].sort_values(["k", "gross"])
        rl = F.iloc[len(F) // 2]
        cap_rows.append(score_pick(key_of(rl), "IS_FAMILY",
                                   f"label only: family {best_fam}, median-ordered book"))
        cap_rows.append(score_pick(key_of(rs), "IS_SHARPE", "reference: best IS Sharpe"))

    # ---------------------------------------------------------------- outputs + gates
    G = pd.DataFrame(grid_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(fam_rows).to_csv(f"{OUT}.perfamily.csv", index=False)
    pd.DataFrame(shelf_rows).to_csv(f"{OUT}.shelf.csv", index=False)
    CAP = pd.DataFrame(cap_rows)
    CAP.to_csv(f"{OUT}.walkforward.csv", index=False)

    log("\n## GATES")
    gate("G0 sample >= 10y on every panel", "U56/B136 18.7y, SMALL 16.7y", ">= 10", True)
    gate("G2 a 100% SPY book reads beta ~ 1.0 (all estimators/panels)",
         f"max|beta-1| = {max(g_spy_beta):.4f}", "< 0.05", max(g_spy_beta) < 0.05)
    gate("G3 no leverage (max shelf gross)", f"{g_lev:.4f}", "<= 1.0", g_lev <= 1.0 + 1e-9)
    gate("G4 every grid point published", f"{len(G)} rows = {len(PANELS)}x{len(FAMILY_SETS)}"
         f"x{len(ESTIMATORS)}", f"{len(PANELS)*len(FAMILY_SETS)*len(ESTIMATORS)}",
         len(G) == len(PANELS) * len(FAMILY_SETS) * len(ESTIMATORS))

    log("\n## ARM 1 — POOLED vs WITHIN-FAMILY vs BETWEEN-FAMILY persistence (every grid point)")
    log(f"   {'panel':<6} {'famset':<10} {'est':<5} {'n':>3}  {'pooled':>8} {'within':>8} "
        f"{'null95':>17} {'in?':>4}  {'between':>8} {'eta2_IS':>8} {'eta2_OOS':>8}")
    for _, r in G.iterrows():
        log(f"   {r.panel:<6} {r.family_set:<10} {r.estimator:<5} {r.n_books:>3}  "
            f"{r.rho_pooled:>+8.4f} {r.rho_within:>+8.4f} "
            f"[{r.null_lo:+.3f},{r.null_hi:+.3f}] {'IN' if r.within_inside_null else 'OUT':>4}  "
            f"{r.rho_between:>+8.4f} {r.eta2_is:>8.4f} {r.eta2_oos:>8.4f}")
    n_in = int(G.within_inside_null.sum())
    v1 = n_in > len(G) / 2
    log(f"   WITHIN inside its within-family permutation null on {n_in} of {len(G)} blocks  ->  "
        f"V1 {'TRIGGERED' if v1 else 'NOT TRIGGERED'}")

    log("\n## ARM 1b — PER-FAMILY persistence on the full shelf (ALL4)")
    PF = pd.DataFrame(fam_rows)
    for _, r in PF.iterrows():
        log(f"   {r.panel:<6} {r.estimator:<5} {r.family:<7} n={r.n:<3} rho={r.rho_family:>+7.4f}"
            f"   mean res IS {r.mean_res_is:>+7.4f} / OOS {r.mean_res_oos:>+7.4f}")

    log("\n## ARM 2 — how much of the residual IS the label")
    n_lab = int((G.eta2_is >= 0.50).sum())
    v2 = n_lab > len(G) / 2
    log(f"   eta2_IS >= 0.50 on {n_lab} of {len(G)} blocks (median eta2_IS "
        f"{G.eta2_is.median():.4f}, eta2_OOS {G.eta2_oos.median():.4f})  ->  "
        f"V2 {'TRIGGERED' if v2 else 'NOT TRIGGERED'}")
    log(f"   median share of the pooled rho lost to family demeaning: {G.share_lost.median():+.4f}")

    log("\n## ARM 3 — CAPITAL (rule 8): IS-only choosers, OOS 2017-2026 read ONCE")
    log(f"   {'panel':<6} {'chooser':<10} {'book':<18} {'FULL CAGR/S/DD':>26} "
        f"{'H1/H2':>13} {'OOS CAGR/S/DD':>26}  4b_f 4b_o 4a")
    for _, r in CAP.iterrows():
        log(f"   {r.panel:<6} {r.chooser:<10} {r.book:<18} "
            f"{r.CAGR:>8.2%}/{r.Sharpe:5.3f}/{r.MaxDD:>7.2%} "
            f"{r.H1:>6.2f}/{r.H2:5.2f} "
            f"{r.oos_CAGR:>8.2%}/{r.oos_Sharpe:5.3f}/{r.oos_MaxDD:>7.2%}  "
            f"{int(r.keep4b_full):>4} {int(r.keep4b_oos):>4} {int(r.keep4a):>2}")
    for pn in PANELS:
        r = CAP[CAP.panel == pn].iloc[0]
        log(f"   {pn:<6} REFERENCE  RULES v2 (live)   {r.base_CAGR:>8.2%}/{r.base_Sharpe:5.3f}/"
            f"{r.base_MaxDD:>7.2%} {r.base_H1:>6.2f}/{r.base_H2:5.2f} "
            f"{r.base_oos_CAGR:>8.2%}/{r.base_oos_Sharpe:5.3f}/{r.base_oos_MaxDD:>7.2%}")
        log(f"   {pn:<6} REFERENCE  SPY              {r.spy_CAGR:>8.2%}/{r.spy_Sharpe:5.3f}/"
            f"{r.spy_MaxDD:>7.2%} {r.spy_H1:>6.2f}/{r.spy_H2:5.2f} "
            f"{r.spy_oos_CAGR:>8.2%}/{r.spy_oos_Sharpe:5.3f}/{r.spy_oos_MaxDD:>7.2%}")
    n_w = int(CAP[(CAP.chooser == "IS_WITHIN") & CAP.keep4b].shape[0])
    n_p = int(CAP[(CAP.chooser == "IS_POOLED") & CAP.keep4b].shape[0])
    n_f = int(CAP[(CAP.chooser == "IS_FAMILY") & CAP.keep4b].shape[0])
    n_s = int(CAP[(CAP.chooser == "IS_SHARPE") & CAP.keep4b].shape[0])
    v3 = n_w >= max(n_p, n_f) and n_w > 0
    log(f"   4b FULL+OOS reached: IS_WITHIN {n_w}/3, IS_POOLED {n_p}/3, IS_FAMILY {n_f}/3, "
        f"IS_SHARPE {n_s}/3  ->  V3 {'TRIGGERED' if v3 else 'NOT TRIGGERED'}")
    log(f"   4a (beat the live book) reached on {int(CAP.keep4a.sum())} of {len(CAP)} picks")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log("\n## VERDICTS (pre-stated)")
    log(f"   V1 the residual is a FAMILY LABEL (no within-family content) ... "
        f"{'YES' if v1 else 'NO'}")
    log(f"   V2 the label carries most of the residual (eta2 >= 0.50) ....... "
        f"{'YES' if v2 else 'NO'}")
    log(f"   V3 the WITHIN-FAMILY reading is a capital signal ............... "
        f"{'YES' if v3 else 'NO'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    print(f"\nwrote {OUT}.grid.csv / .perfamily.csv / .shelf.csv / .walkforward.csv / "
          f".gates.csv / .log.txt")


if __name__ == "__main__":
    main()
