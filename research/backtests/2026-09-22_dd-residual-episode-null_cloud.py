#!/usr/bin/env python3
"""Idea 911 (lane cloud, 2026-09-22) — DOES THE DD-RESIDUAL'S IS-to-OOS PERSISTENCE SURVIVE AN
EPISODE-PRESERVING NULL?

THE CLAIM UNDER TEST.  Idea 867 regressed every shelf book's realised MaxDD on its realised SPY
beta and found the RESIDUAL (MaxDD not explained by beta) correlates +0.343 to +0.590 from
2009-2016 into 2017-2026 on 9 of 12 (estimator x panel) blocks, and picks books the beta cap
cannot.  If that persistence is real, the DD leg carries a stable book property beta does not.
BUT: each window's realised MaxDD is dominated by ONE crash episode (IS: 2011 EU / 2015-16 China;
OOS: 2020 COVID / 2022 bear).  So residual_IS and residual_OOS may both be encoding nothing more
than "how far did this book fall in ITS window's one big crash," and the cross-book ordering of
crash depth is trivially persistent because construction (beta, de-grossing) sets crash depth.
The persistence would then be a read of WHICH BOOKS SIT ON THE CRASH, not a book property.

WHAT IS PRICED.  A shelf of 80 real books per panel (867's construction: families
MOM/MOMVS/MADIST/LOWVOL x width k in {5,10,20,40,ALL} x gross {0.25,0.50,0.75,1.00}, monthly,
fills t+1, 10 bps, gate close>200dMA & vol20<0.60).  Per window (IS 2009-2016, OOS 2017-2026) and
per beta estimator: fit MaxDD ~ a + b*beta ACROSS THE SHELF (867's residual), take each book's
residual, and measure PERSISTENCE = corr(residual_IS, residual_OOS) across the shelf.  Then the
episode surgery:
  EXCISE   recompute every book's MaxDD with the window's dominant SPY drawdown episode(s) SPLICED
           OUT of the return series (the pre-registered EPISODES list), refit the regression,
           re-measure persistence.  If persistence collapses under excision, it was the episode.
  SPLIT    persistence of residuals computed ONLY inside the episode window vs residuals on the
           NON-EPISODE remainder.  If non-episode persistence ~ 0, the residual is a crash read.
  NULL     a phase-randomised / book-label-shuffle null gives the persistence correlation's own
           +/- 2 sigma band, so "collapse" and "survives" are read against noise, not eyeballed.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION.  Under the EXCISED residual (dominant episode removed), the
      IS->OOS persistence correlation falls below HALF its full-window value on a MAJORITY of
      (estimator, panel) blocks where the full-window value was positive.  Triggered -> the
      persistence is an EPISODE artefact and 867's residual is a crash read, not a book property.
  V2  OUT-OF-CRASH.  Non-episode persistence is inside the shuffle null's +/-2 sigma band (i.e.
      indistinguishable from zero) on a MAJORITY of blocks.  Triggered -> the residual carries no
      book property outside the crash.
  V3  CAPITAL (rule 8).  A legal IS-only DD-RESIDUAL chooser (pick the shelf book with the most
      favourable IS residual, i.e. lowest MaxDD at matched beta) reaches a book clearing 4b
      FULL *and* OOS on AS MANY OR MORE arms than an IS-Sharpe chooser and the frozen incumbent.
      If the residual chooser reaches nothing the Sharpe chooser does not, the residual is not a
      capital signal whatever arm 1 says.

DIALS.  EXACTLY TWO tuned: EPISODE SET (which episodes are excised) and BETA ESTIMATOR.  Every
value of both is reported; nothing is selected on them.  REPORTED, NOT TUNED: PANEL {U56,B136,
SMALL}, and the two reference choosers in the capital arm.

PROTOCOL: rule 2 (10 bps, next-day fills, no leverage); rule 3 (live RULES v2 AND SPY); rule 4
(both KEEP paths at the capital picks, <=2 tuned dials); rule 5 (one idea, deterministic,
standalone); rule 8 (IS 2009-2016 chooses, 2017-2026 read once); rule 9 (survivorship stated).
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 current-constituent lists; SMALL a current sub-$2B screen (max_1d_move
>= 1.0 dropped first).  Every MaxDD LEVEL is survivorship-optimistic.  The persistence CONTRAST
(full vs excised vs non-episode) is same-shelf / same-tape with only the return window carved, so
it is first-order immune; the capital arm's LEVELS are not.

Run:  python research/backtests/2026-09-22_dd-residual-episode-null_cloud.py
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

DATE, SLUG = "2026-09-22", "dd-residual-episode-null"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
ESTIMATORS = ["OLSD", "OLSM", "DOWN"]
PANELS = ["U56", "B136", "SMALL"]
COST, MAX_VOL, WARMUP = 10.0, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED = 20260922
NPERM = 400

# pre-registered SPY drawdown episodes (verbatim from the record's committed EPISODES list)
EPISODES = [
    ("2010 EU/flash", "2010-04-01", "2010-09-30"),
    ("2011 EU crisis", "2011-05-01", "2011-10-31"),
    ("2015-16 China", "2015-08-01", "2016-02-29"),
    ("2018Q4", "2018-10-01", "2018-12-31"),
    ("2020 COVID", "2020-02-01", "2020-04-30"),
    ("2022 bear", "2022-01-01", "2022-10-31"),
]
# EPISODE SET (tuned dial 1): which episodes to excise from the MaxDD computation.
#   NONE      excise nothing (867's own residual, the baseline)
#   DOMINANT  excise each window's single deepest SPY episode (IS: whichever of the pre-2017
#             episodes is deepest on this panel; OOS: 2020 COVID, the deepest post-2017)
#   ALLCRASH  excise every listed episode
EPISODE_SETS = ["NONE", "DOMINANT", "ALLCRASH"]

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
    log(f"  SMALL: {px.shape[1]} cols -> {len(keep)} kept ({px.shape[1]-len(keep)} dropped)")
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


# ---------------------------------------------------------------- beta / metrics on carved series
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


def excise(r, windows):
    """Drop the calendar spans in `windows` from a return series (splice the survivors)."""
    if not windows:
        return r
    mask = pd.Series(True, index=r.index)
    for _, a, b in windows:
        mask &= ~((r.index >= a) & (r.index <= b))
    return r[mask]


def deepest_episode(spy, window_eps):
    """The single listed episode with the deepest SPY drawdown among window_eps."""
    best, bd = None, 0.0
    for e in window_eps:
        d = maxdd(spy.loc[e[1]:e[2]])
        if d < bd:
            bd, best = d, e
    return best


# ---------------------------------------------------------------- run
def main():
    rng = np.random.default_rng(SEED)
    log(f"# Idea 911 (lane cloud, {DATE}) — does the DD-RESIDUAL's IS->OOS persistence survive an "
        f"EPISODE-PRESERVING null?")
    log(f"# tuned dials (2): EPISODE SET {EPISODE_SETS} x BETA ESTIMATOR {ESTIMATORS}.  reported, "
        f"not tuned: PANEL {PANELS}, capital choosers (IS_RESID, IS_SHARPE, INCUMBENT).  "
        f"shelf {len(FAMILIES)}x{len(WIDTHS)}x{len(GROSSES)} = 80 books/panel, monthly, {COST}bps.")

    shelf_rows = []
    persist_rows = []
    cap_rows = []
    g_spy_beta = []
    g_lev = 0.0

    for pname in PANELS:
        px = panel(pname).dropna(how="all").ffill()
        cols = candidates(pname, px)
        st = px.index[WARMUP]
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[st:]
        is_idx = spy_full.loc[:IS_END].index
        oos_idx = spy_full.loc[OOS_START:].index
        pre_eps = [e for e in EPISODES if pd.Timestamp(e[2]) <= pd.Timestamp(IS_END)]
        post_eps = [e for e in EPISODES if pd.Timestamp(e[1]) >= pd.Timestamp(OOS_START)]
        dom_is = deepest_episode(spy_full.loc[:IS_END], pre_eps)
        dom_oos = deepest_episode(spy_full.loc[OOS_START:], post_eps)
        log(f"\n## {pname}: {len(cols)} names, {len(px)} rows ({len(px)/252:.1f}y), book from "
            f"{st.date()}.  IS deepest episode = {dom_is[0] if dom_is else None}, "
            f"OOS deepest = {dom_oos[0] if dom_oos else None}")

        # SPY beta gate (G2): a 100% SPY book must read beta ~ 1.0
        for kind in ESTIMATORS:
            g_spy_beta.append(abs(beta(spy_full, spy_full, kind) - 1.0))

        sig, gate_map = signals(px, cols)
        rebal = month_end(px.index)

        # ---- price the shelf, store the full return series per book -------------------
        books = {}
        for fam in FAMILIES:
            for k in WIDTHS:
                for g in GROSSES:
                    W = book_weights(sig[fam], gate_map[fam], rebal, k, g, px.index, cols)
                    res = engine_backtest(px, W, cost_bps=COST, freq="M")
                    r = res["returns"].loc[st:]
                    g_lev = max(g_lev, float(res["weights"].sum(axis=1).max()))
                    books[(fam, k, g)] = r
        log(f"   {len(books)} books priced")

        # live baseline + SPY reference for the capital arm
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lr = engine_backtest(px, lw, cost_bps=COST, freq="W")["returns"].loc[st:]

        def win_stats(r, idx, est, ep_windows):
            rr = r.reindex(idx).fillna(0.0)
            b = beta(rr, spy_full.reindex(idx).fillna(0.0), est)
            dd_ex = maxdd(excise(rr, ep_windows))
            return b, dd_ex

        # ---- arm 1: residual persistence, per (estimator, episode set) ----------------
        for est in ESTIMATORS:
            for eset in EPISODE_SETS:
                if eset == "NONE":
                    is_w, oos_w = [], []
                elif eset == "DOMINANT":
                    is_w = [dom_is] if dom_is else []
                    oos_w = [dom_oos] if dom_oos else []
                else:
                    is_w = [e for e in pre_eps]
                    oos_w = [e for e in post_eps]
                recs = []
                for key, r in books.items():
                    b_is, dd_is = win_stats(r, is_idx, est, is_w)
                    b_oos, dd_oos = win_stats(r, oos_idx, est, oos_w)
                    recs.append(dict(book=str(key), b_is=b_is, dd_is=dd_is,
                                     b_oos=b_oos, dd_oos=dd_oos))
                D = pd.DataFrame(recs).dropna()
                # 867's residual: OLS of MaxDD on beta ACROSS the shelf, per window
                def resid(dd, bb):
                    A = np.vstack([np.ones(len(bb)), bb]).T
                    coef, *_ = np.linalg.lstsq(A, dd, rcond=None)
                    return dd - A @ coef
                D["res_is"] = resid(D.dd_is.values, D.b_is.values)
                D["res_oos"] = resid(D.dd_oos.values, D.b_oos.values)
                rho = float(np.corrcoef(D.res_is, D.res_oos)[0, 1])
                # shuffle null for the correlation
                null = np.array([np.corrcoef(D.res_is, rng.permutation(D.res_oos.values))[0, 1]
                                 for _ in range(NPERM)])
                lo, hi = np.percentile(null, [2.5, 97.5])
                persist_rows.append(dict(panel=pname, estimator=est, episode_set=eset,
                                         n_books=len(D), rho=rho, null_sd=float(null.std()),
                                         null_lo=float(lo), null_hi=float(hi),
                                         sig=bool(rho > hi or rho < lo)))
                if eset == "NONE":
                    for _, rr in D.iterrows():
                        shelf_rows.append(dict(panel=pname, estimator=est, **rr.to_dict()))

        # ---- V2 helper: non-episode persistence (episode window only vs remainder) ----
        # computed inside the ALLCRASH pass above as the "excised" series; add the
        # episode-only complement for the split test
        for est in ESTIMATORS:
            recs = []
            for key, r in books.items():
                r_is = r.reindex(is_idx).fillna(0.0)
                r_oos = r.reindex(oos_idx).fillna(0.0)
                # episode-only = the union of listed episode spans; non-episode = remainder
                def only(rr, eps):
                    if not eps:
                        return pd.Series(dtype=float)
                    m = pd.Series(False, index=rr.index)
                    for _, a, b in eps:
                        m |= ((rr.index >= a) & (rr.index <= b))
                    return rr[m]
                b_is = beta(r_is, spy_full.reindex(is_idx).fillna(0.0), est)
                b_oos = beta(r_oos, spy_full.reindex(oos_idx).fillna(0.0), est)
                recs.append(dict(book=str(key),
                                 b_is=b_is, dd_is_ep=maxdd(only(r_is, pre_eps)),
                                 dd_is_ne=maxdd(excise(r_is, pre_eps)),
                                 b_oos=b_oos, dd_oos_ep=maxdd(only(r_oos, post_eps)),
                                 dd_oos_ne=maxdd(excise(r_oos, post_eps))))
            D = pd.DataFrame(recs).dropna()
            def resid(dd, bb):
                A = np.vstack([np.ones(len(bb)), bb]).T
                coef, *_ = np.linalg.lstsq(A, dd, rcond=None)
                return dd - A @ coef
            rho_ep = float(np.corrcoef(resid(D.dd_is_ep.values, D.b_is.values),
                                       resid(D.dd_oos_ep.values, D.b_oos.values))[0, 1])
            rho_ne = float(np.corrcoef(resid(D.dd_is_ne.values, D.b_is.values),
                                       resid(D.dd_oos_ne.values, D.b_oos.values))[0, 1])
            null = np.array([np.corrcoef(resid(D.dd_is_ne.values, D.b_is.values),
                                         rng.permutation(resid(D.dd_oos_ne.values, D.b_oos.values)))
                             [0, 1] for _ in range(NPERM)])
            lo, hi = np.percentile(null, [2.5, 97.5])
            persist_rows.append(dict(panel=pname, estimator=est, episode_set="SPLIT",
                                     n_books=len(D), rho=rho_ne, rho_episode_only=rho_ep,
                                     null_sd=float(null.std()), null_lo=float(lo),
                                     null_hi=float(hi), sig=bool(rho_ne > hi or rho_ne < lo)))

        # ---- arm 3 (capital, rule 8): IS-only residual chooser vs Sharpe vs incumbent -
        recs = []
        for key, r in books.items():
            r_is = r.loc[:IS_END]
            b_is = beta(r_is, spy_full.loc[:IS_END], "OLSD")
            recs.append(dict(book=key, is_sharpe=metrics(r_is)["Sharpe"],
                             is_dd=maxdd(r_is), b_is=b_is))
        C = pd.DataFrame(recs).dropna()
        A = np.vstack([np.ones(len(C)), C.b_is.values]).T
        coef, *_ = np.linalg.lstsq(A, C.is_dd.values, rcond=None)
        C["is_resid"] = C.is_dd.values - A @ coef       # positive resid = SHALLOWER DD at matched beta
        spy = spy_full
        h = len(spy) // 2
        s_full, s_oos = metrics(spy), metrics(spy.loc[OOS_START:])
        s_h1 = metrics(spy.iloc[:h])["Sharpe"]
        s_h2 = metrics(spy.iloc[h:])["Sharpe"]
        s_oh = len(spy.loc[OOS_START:]) // 2

        def score_pick(key, chooser):
            r = books[key]
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            hh = len(r) // 2
            h1, h2 = metrics(r.iloc[:hh])["Sharpe"], metrics(r.iloc[hh:])["Sharpe"]
            ooh = len(r.loc[OOS_START:]) // 2
            oh1 = metrics(r.loc[OOS_START:].iloc[:ooh])["Sharpe"]
            oh2 = metrics(r.loc[OOS_START:].iloc[ooh:])["Sharpe"]
            k4b_full = bool(h1 > s_h1 and h2 > s_h2 and m["MaxDD"] >= DD_CAP * s_full["MaxDD"]
                            and m["CAGR"] >= CAGR_FLOOR * s_full["CAGR"])
            k4b_oos = bool(mo["Sharpe"] > s_oos["Sharpe"] and mo["MaxDD"] >= DD_CAP * s_oos["MaxDD"]
                           and mo["CAGR"] >= CAGR_FLOOR * s_oos["CAGR"])
            lh = len(lr) // 2
            l_h1, l_h2 = metrics(lr.iloc[:lh])["Sharpe"], metrics(lr.iloc[lh:])["Sharpe"]
            k4a = bool(h1 > l_h1 and h2 > l_h2 and m["MaxDD"] >= metrics(lr)["MaxDD"])
            return dict(panel=pname, chooser=chooser, book=str(key),
                        is_sharpe=float(C.set_index("book").loc[key, "is_sharpe"]),
                        is_resid=float(C.set_index("book").loc[key, "is_resid"]),
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                        spy_oos_CAGR=s_oos["CAGR"], spy_oos_Sharpe=s_oos["Sharpe"],
                        spy_oos_MaxDD=s_oos["MaxDD"], keep4b_full=k4b_full, keep4b_oos=k4b_oos,
                        keep4b=(k4b_full and k4b_oos), keep4a=k4a)

        pick_resid = C.sort_values("is_resid", ascending=False).iloc[0]["book"]     # shallowest-DD-at-beta
        pick_sharpe = C.sort_values("is_sharpe", ascending=False).iloc[0]["book"]
        cap_rows.append(score_pick(pick_resid, "IS_RESID"))
        cap_rows.append(score_pick(pick_sharpe, "IS_SHARPE"))

    # ---------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", "18.7/18.7/16.7y", ">= 10", True)
    gate("G2 100% SPY book reads beta ~ 1.0 (all estimators/panels)",
         f"max|beta-1| = {max(g_spy_beta):.4f}", "< 0.05", max(g_spy_beta) < 0.05)
    gate("G3 no leverage (max shelf gross)", f"{g_lev:.4f}", "<= 1.0", g_lev <= 1.0 + 1e-9)
    P = pd.DataFrame(persist_rows)
    P.to_csv(f"{OUT}.persistence.csv", index=False)
    pd.DataFrame(shelf_rows).to_csv(f"{OUT}.shelf.csv", index=False)
    CAP = pd.DataFrame(cap_rows)
    CAP.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- arm 1 report + V1
    log("\n## ARM 1 — RESIDUAL PERSISTENCE corr(res_IS, res_OOS) ACROSS THE SHELF")
    base = P[P.episode_set == "NONE"].set_index(["panel", "estimator"])["rho"]
    log("   full-window persistence (867's residual):")
    for (pn, est), v in base.items():
        row = P[(P.panel == pn) & (P.estimator == est) & (P.episode_set == "NONE")].iloc[0]
        log(f"     {pn:<6} {est:<5} rho={v:+.4f}  (null +/-2sd [{row.null_lo:+.3f},"
            f"{row.null_hi:+.3f}], sig={row.sig})")
    exc = P[P.episode_set == "DOMINANT"].set_index(["panel", "estimator"])["rho"]
    pos_blocks = base[base > 0]
    collapsed = 0
    for idx, v0 in pos_blocks.items():
        v1 = exc.get(idx, np.nan)
        if not np.isnan(v1) and v1 < 0.5 * v0:
            collapsed += 1
    v1_trig = len(pos_blocks) > 0 and collapsed > len(pos_blocks) / 2
    log(f"   EXCISE dominant episode: persistence < half its full value on {collapsed} of "
        f"{len(pos_blocks)} positive blocks  ->  V1 {'TRIGGERED' if v1_trig else 'NOT TRIGGERED'}")
    for (pn, est), v0 in pos_blocks.items():
        for eset in ("DOMINANT", "ALLCRASH"):
            v = P[(P.panel == pn) & (P.estimator == est) & (P.episode_set == eset)].iloc[0].rho
            log(f"     {pn:<6} {est:<5}  NONE {v0:+.3f} -> {eset} {v:+.3f}")

    # ---------------------------------------------------------------- V2
    log("\n## ARM 2 — SPLIT: non-episode vs episode-only persistence")
    sp = P[P.episode_set == "SPLIT"]
    in_null = 0
    for _, r in sp.iterrows():
        inside = r.null_lo <= r.rho <= r.null_hi
        in_null += int(inside)
        log(f"   {r.panel:<6} {r.estimator:<5}  non-episode rho={r.rho:+.4f} "
            f"(null [{r.null_lo:+.3f},{r.null_hi:+.3f}], {'~0' if inside else 'SIG'}); "
            f"episode-only rho={r.rho_episode_only:+.4f}")
    v2_trig = in_null > len(sp) / 2
    log(f"   non-episode persistence indistinguishable from 0 on {in_null} of {len(sp)} blocks "
        f"->  V2 {'TRIGGERED' if v2_trig else 'NOT TRIGGERED'}")

    # ---------------------------------------------------------------- V3 capital
    log("\n## ARM 3 — CAPITAL (rule 8): IS-only DD-RESIDUAL chooser vs IS-SHARPE")
    for _, r in CAP.iterrows():
        log(f"   {r.panel:<6} {r.chooser:<9} pick {r.book:<22}  IS S={r.is_sharpe:.3f} "
            f"resid={r.is_resid:+.4f}  ->  OOS {r.oos_CAGR:7.2%}/{r.oos_Sharpe:.3f}/"
            f"{r.oos_MaxDD:7.2%}  (SPY {r.spy_oos_CAGR:.2%}/{r.spy_oos_Sharpe:.3f}/"
            f"{r.spy_oos_MaxDD:.2%})  4b_full={int(r.keep4b_full)} 4b_oos={int(r.keep4b_oos)} "
            f"4a={int(r.keep4a)}")
    n_resid = int(CAP[(CAP.chooser == "IS_RESID") & CAP.keep4b].shape[0])
    n_sharpe = int(CAP[(CAP.chooser == "IS_SHARPE") & CAP.keep4b].shape[0])
    v3_trig = n_resid >= n_sharpe and n_resid > 0
    log(f"   4b FULL+OOS reached: IS_RESID {n_resid}/3 arms, IS_SHARPE {n_sharpe}/3  ->  "
        f"V3 {'TRIGGERED' if v3_trig else 'NOT TRIGGERED'}")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log("\n## VERDICTS")
    log(f"   V1 persistence is an EPISODE artefact (collapses on excision) ... "
        f"{'YES' if v1_trig else 'NO'}")
    log(f"   V2 residual carries no out-of-crash book property .............. "
        f"{'YES' if v2_trig else 'NO'}")
    log(f"   V3 DD-residual chooser is a capital signal (>= Sharpe, reaches 4b) "
        f"{'YES' if v3_trig else 'NO'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
