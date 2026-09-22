#!/usr/bin/env python3
"""Idea 913 (lane cloud, 2026-09-22) — DOES A FIXED PRE-REGISTERED EPISODE BETA RESTORE THE
PERSISTENCE SPYDD LACKS?

WHERE THIS COMES FROM.  Idea 910 (lane C, 2026-09-15) asked for an ex-ante proxy for the DDWIN
beta (the beta measured inside a book's OWN peak-to-trough drawdown window, which is circular
because the window is chosen by the answer).  Its winner, SPYDD — beta measured inside SPY's own
argmin drawdown window — reached agreement 1.0000 with the 4b DD leg on B136, and then read
rho(beta_IS, beta_OOS) of only +0.216 / +0.292 against +0.757..+0.993 for every other proxy.
910's own reading of that: SPYDD's window is RE-CHOSEN per sample (SPY's deepest decline is 2011
inside 2009-2016 and 2020 in 2017-2026), so the estimator is "a date, not a book property".

THE QUESTION.  Take the window OFF the sample.  Re-estimate the same beta on a FIXED
pre-registered EPISODE CALENDAR — 2011, 2015-16, 2018Q4, 2020, 2022 — that does not move when
the window moves, and ask whether AGREEMENT and PERSISTENCE can hold AT ONCE, which is the thing
910 could not get from any of its ten proxies.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4; every grid point reported, none hidden):
    P1  EPISODE SET, four pre-registered calendars, none fitted to a book:
          E5      the idea's own list, as COARSE MONTH BLOCKS (not fitted peak/trough dates):
                  2011-07..2011-10, 2015-08..2016-02, 2018-10..2018-12, 2020-02..2020-04,
                  2022-01..2022-10
          E3      the three largest blocks only: 2011, 2020, 2022
          E5W     E5 with every block widened by one calendar month on each side
          BEAR10  RULE-DEFINED, not hand-picked: every day SPY sits >= 10% below its running
                  peak.  Carried as the control that asks whether a hand-picked calendar buys
                  anything a mechanical one does not.
    P2  PANEL  {U56, B136, SMALL}

REPORTED, NOT TUNED (these are comparands, not dials being searched):
    estimators  FIXED (the episode beta, one per P1 rung), SPYDD (910's winner, window re-chosen
                per sample), DDWIN (the CIRCULAR ceiling, never a candidate), FULL (all days),
                DOWN (SPY < 0 days).
    shelf       ideas 911/2083's 80 books per panel verbatim: families MOM / MOMVS / MADIST /
                LOWVOL x width k in {5,10,20,40,ALL} x gross in {0.25,0.50,0.75,1.00}, monthly,
                fills t+1, 10 bps, gate close > 200d MA and vol20 < 0.60.
    statistics  910's verbatim: agreement of (beta <= 0.60) with the 4b DD leg, the best-case cap
                fitted ON the answer (an upper bound, never a rule), and matched-pair
                disagreement at |dbeta| <= 0.02.  PERSISTENCE is reported as BOTH Spearman and
                Pearson, each named (the record's standing complaint, idea 564).

THE HONESTY LINE THIS RUN DRAWS (stated up front, not at the end).
  The episode CALENDAR is hindsight-labelled: nobody could have written "2020 and 2022" in 2016.
  So the AGREEMENT / PERSISTENCE arm below is a MEASUREMENT-PROPERTY study of the estimator, and
  it carries 911's caveat exactly.  The CAPITAL arm is held to a stricter line: the chooser may
  read only episode days INSIDE the in-sample window, so it uses 2011 and 2015-16 and never sees
  2018Q4 / 2020 / 2022.  Under that restriction the calendar is a definition, not a look-ahead.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  PERSISTENCE.  Some (episode set, panel) cell reads rho_Spearman(beta_IS, beta_OOS) >= 0.70
      for FIXED — i.e. the fixed calendar lifts SPYDD's +0.216 / +0.292 into the band every other
      910 proxy already occupies.
  V2  AGREEMENT.  That same cell also reads agreement >= 0.95 with the 4b DD leg.
  V3  BOTH AT ONCE (the idea's own question).  V1 and V2 hold in the SAME cell.  Not triggered ->
      the persistence and the agreement are still not simultaneously purchasable.
  V4  IS THE CALENDAR DOING THE WORK?  FIXED beats the rule-defined BEAR10 control on persistence
      in a majority of panels.  Not triggered -> the hand-picked dates buy nothing mechanical.
  V5  CAPITAL.  The IS-only episode-beta screen (beta_FIXED(IS) <= 0.60, then max IS Sharpe)
      reaches a book whose OOS 4b DD leg PASSES, where the unscreened IS-Sharpe control does not.

PROTOCOL: rule 2 (10 bps, next-day execution via engine.backtest, no shorting/leverage); rule 3
(live RULES v2 AND SPY at every pick); rule 4 (BOTH KEEP paths, <= 2 tuned parameters, all grid
points reported); rule 5 (one idea, deterministic, standalone); rule 8 (walk-forward: the screen
and the chooser read 2009-2016 ONLY, 2017-2026 is read once); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B
screen (tickers with max_1d_move >= 1.0 dropped per data/small_meta.csv), so every CAGR and MaxDD
LEVEL below is optimistic and both 4b bars are easier than on a point-in-time panel.  The
estimator CONTRASTS (FIXED vs SPYDD vs FULL on the same shelf, same tape) are first-order immune;
the agreement LEVELS and the 4b pass counts are not.

Runs standalone and offline (committed caches only):
  python research/backtests/2026-09-22_fixed-episode-beta_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score          # noqa: E402
from engine import backtest as engine_backtest                       # noqa: E402

DATE, SLUG, LANE = "2026-09-22", "fixed-episode-beta", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

WARMUP, COST_BPS, MAX_VOL = 260, 10.0, 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BETA_CAP = 0.60          # 867/910's committed cap, NOT a new dial
MATCH_TOL = 0.02         # 867/910's beta-matching tolerance
MINOBS = 20              # 867/910's minimum observations for a beta
DD10 = 0.10              # BEAR10's depth (910's SPYDD10 verbatim)
PERSIST_BAR, AGREE_BAR = 0.70, 0.95

FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
PANELS = ["U56", "B136", "SMALL"]                                   # P2
EPISODES = {                                                        # P1
    "E5":  [("2011-07-01", "2011-10-31"), ("2015-08-01", "2016-02-29"),
            ("2018-10-01", "2018-12-31"), ("2020-02-01", "2020-04-30"),
            ("2022-01-01", "2022-10-31")],
    "E3":  [("2011-07-01", "2011-10-31"), ("2020-02-01", "2020-04-30"),
            ("2022-01-01", "2022-10-31")],
    "E5W": [("2011-06-01", "2011-11-30"), ("2015-07-01", "2016-03-31"),
            ("2018-09-01", "2019-01-31"), ("2020-01-01", "2020-05-31"),
            ("2021-12-01", "2022-11-30")],
    "BEAR10": "RULE",                                               # SPY >= 10% below its peak
}
ESTIMATORS = ["FIXED", "SPYDD", "DDWIN", "FULL", "DOWN"]

LINES: list[str] = []
GATES: list[dict] = []


def P(s: str = "") -> None:
    print(s, flush=True)
    LINES.append(s)


def gate(name, value, target, ok) -> bool:
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    P(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ------------------------------------------------------------------ statistics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    v = r.std(ddof=1) * np.sqrt(252.0)
    return float(r.mean() * 252.0 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    return float(np.exp(np.log1p(r).sum() * 252.0 / len(r)) - 1.0) if len(r) else np.nan


def maxdd(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def ols_beta(r, m):
    r, m = np.asarray(r, float), np.asarray(m, float)
    if len(r) < MINOBS:
        return np.nan
    v = m.var(ddof=1)
    return float(np.cov(r, m, ddof=1)[0, 1] / v) if v > 0 else np.nan


def dd_window_mask(r):
    """Boolean mask of the deepest peak-to-trough decline of the equity curve of r."""
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    tr = int(np.argmin(dd))
    pk = int(np.argmax(eq[: tr + 1])) if tr > 0 else 0
    m = np.zeros(len(r), bool)
    if tr - pk >= MINOBS:
        m[pk: tr + 1] = True
    return m


def spearman(a, b):
    s = pd.DataFrame({"a": np.asarray(a, float), "b": np.asarray(b, float)}).dropna()
    return float(s["a"].rank().corr(s["b"].rank())) if len(s) >= 5 else np.nan


def pearson(a, b):
    s = pd.DataFrame({"a": np.asarray(a, float), "b": np.asarray(b, float)}).dropna()
    return float(s["a"].corr(s["b"])) if len(s) >= 5 else np.nan


def best_cap(beta, truth):
    """Cap fitted ON the answer: an UPPER BOUND on agreement, never a usable rule (910's form)."""
    ok = np.isfinite(beta)
    b, t = np.asarray(beta)[ok], np.asarray(truth)[ok]
    if len(b) < 5:
        return np.nan, np.nan
    o = np.sort(np.unique(b))
    cands = np.concatenate([[o[0] - 1e-6], (o[:-1] + o[1:]) / 2.0, [o[-1] + 1e-6]])
    best, bc = -1.0, np.nan
    for c in cands:
        a = float(((b <= c) == t).mean())
        if a > best:
            best, bc = a, float(c)
    return bc, best


# ------------------------------------------------------------------ panel / shelf (911/2083)
def panel(name):
    if name == "U56":
        return load_universe().dropna(how="all").ffill()
    if name == "B136":
        return load_universe(broad=True).dropna(how="all").ffill()
    px = load_universe(small=True).dropna(how="all").ffill()
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    P(f"   SMALL: {px.shape[1]} cols -> {len(keep)} kept ({px.shape[1]-len(keep)} dropped, "
      f"max_1d_move >= 1.0 per data/small_meta.csv)")
    return px[keep]


def signals(px):
    comp_ns, above, vol20 = score(px, vol_scale=False)
    comp_vs, _, _ = score(px, vol_scale=True)
    g = above & (vol20 < MAX_VOL) & px.notna()
    sig = dict(MOM=comp_ns, MOMVS=comp_vs, MADIST=px / px.rolling(200).mean() - 1.0, LOWVOL=-vol20)
    return sig, {f: g & sig[f].notna() for f in sig}


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


# ------------------------------------------------------------------ episode masks
def episode_mask(dates: pd.DatetimeIndex, spy: np.ndarray, key: str) -> np.ndarray:
    spec = EPISODES[key]
    if spec == "RULE":
        eq = np.cumprod(1.0 + spy)
        return (eq / np.maximum.accumulate(eq) - 1.0) <= -DD10
    m = np.zeros(len(dates), bool)
    for a, b in spec:
        m |= (dates >= pd.Timestamp(a)) & (dates <= pd.Timestamp(b))
    return m


def main() -> None:
    P(__doc__.strip())
    P("\n" + "=" * 100)

    agree_rows, persist_rows, book_rows, wf_rows, mask_rows = [], [], [], [], []

    for pname in PANELS:
        px = panel(pname)
        cols = [c for c in px.columns if pname in ("U56", "B136") or c != "SPY"]
        start = px.index[WARMUP]
        dates = px.index[px.index >= start]
        n = len(dates)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:].to_numpy()
        m_is = np.asarray(dates <= pd.Timestamp(IS_END))
        m_oos = np.asarray(dates >= pd.Timestamp(OOS_START))
        base = engine_backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:].to_numpy()
        h = n // 2
        base_s = dict(H1=sharpe(base[:h]), H2=sharpe(base[h:]), MaxDD=maxdd(base))
        spy_s = dict(H1=sharpe(spy[:h]), H2=sharpe(spy[h:]), MaxDD=maxdd(spy), CAGR=cagr(spy),
                     OOS_S=sharpe(spy[m_oos]), OOS_DD=maxdd(spy[m_oos]), OOS_CAGR=cagr(spy[m_oos]))

        P(f"\n## PANEL {pname}: {len(cols)} names, {dates[0].date()} .. {dates[-1].date()}, n={n} "
          f"days after {WARMUP}-day warm-up;  IS {int(m_is.sum())} / OOS {int(m_oos.sum())} days")
        P(f"   SPY FULL {spy_s['CAGR']:.2%} / {sharpe(spy):.4f} / {spy_s['MaxDD']:.2%};  "
          f"OOS {spy_s['OOS_CAGR']:.2%} / {spy_s['OOS_S']:.4f} / {spy_s['OOS_DD']:.2%};  "
          f"4b bars: CAGR floor {CAGR_FLOOR*spy_s['CAGR']:.2%}, DD cap {-DD_CAP*abs(spy_s['MaxDD']):.2%}")
        P(f"   RULES v2 (live, weekly): {cagr(base):.2%} / {sharpe(base):.4f} / {base_s['MaxDD']:.2%};  "
          f"halves {base_s['H1']:.4f} / {base_s['H2']:.4f};  OOS {cagr(base[m_oos]):.2%} / "
          f"{sharpe(base[m_oos]):.4f} / {maxdd(base[m_oos]):.2%}")

        # ---- day masks, once per panel, shared by every book (this is what makes them non-circular)
        emask = {k: episode_mask(dates, spy, k) for k in EPISODES}
        spydd_full, spydd_is, spydd_oos = dd_window_mask(spy), np.zeros(n, bool), np.zeros(n, bool)
        spydd_is[m_is] = dd_window_mask(spy[m_is])
        spydd_oos[m_oos] = dd_window_mask(spy[m_oos])
        down = spy < 0.0
        for k, m in emask.items():
            mask_rows.append(dict(panel=pname, set=k, days=int(m.sum()),
                                  is_days=int((m & m_is).sum()), oos_days=int((m & m_oos).sum()),
                                  first=str(dates[m][0].date()) if m.any() else "",
                                  last=str(dates[m][-1].date()) if m.any() else ""))
        P("   episode-day census (the same days for every book):")
        for k in EPISODES:
            r = [x for x in mask_rows if x["panel"] == pname and x["set"] == k][0]
            P(f"     {k:<7} {r['days']:>5} days  (IS {r['is_days']:>4}, OOS {r['oos_days']:>4})  "
              f"{r['first']} .. {r['last']}")
        P(f"     SPYDD   {int(spydd_full.sum()):>5} days on FULL, {int(spydd_is.sum()):>4} on IS, "
          f"{int(spydd_oos.sum()):>4} on OOS  <- 910's estimator: the window MOVES with the sample")

        # ---- shelf
        sig, elig = signals(px[cols])
        rebal = month_end(px.index)
        rets, names = {}, []
        for fam in FAMILIES:
            for k in WIDTHS:
                for g in GROSSES:
                    W = book_weights(sig[fam], elig[fam], rebal, k, g, px.index, cols)
                    # SMALL's candidate list excludes the SPY benchmark column, so widen the
                    # weight frame back to the panel's columns at zero before pricing it.
                    W = W.reindex(columns=px.columns, fill_value=0.0)
                    r = engine_backtest(px, W, cost_bps=COST_BPS, freq="M")["returns"].loc[start:].to_numpy()
                    nm = f"{fam}/{k}/{g:.2f}"
                    rets[nm], _ = r, names.append(nm)

        # ---- betas and the DD-leg truth
        B = {e: {} for e in ESTIMATORS}
        BIS, BOOS = {e: {} for e in ESTIMATORS}, {e: {} for e in ESTIMATORS}
        truth, dds = {}, {}
        for nm in names:
            r = rets[nm]
            truth[nm] = bool(maxdd(r) >= DD_CAP * spy_s["MaxDD"])      # the 4b DD leg, FULL window
            dds[nm] = maxdd(r)
            B["FULL"][nm] = ols_beta(r, spy)
            B["DOWN"][nm] = ols_beta(r[down], spy[down])
            B["SPYDD"][nm] = ols_beta(r[spydd_full], spy[spydd_full])
            dw = dd_window_mask(r)
            B["DDWIN"][nm] = ols_beta(r[dw], spy[dw]) if dw.sum() >= MINOBS else np.nan
            for e, mi, mo in (("FULL", m_is, m_oos), ("DOWN", down & m_is, down & m_oos),
                              ("SPYDD", spydd_is, spydd_oos)):
                BIS[e][nm] = ols_beta(r[mi], spy[mi])
                BOOS[e][nm] = ols_beta(r[mo], spy[mo])
            dwi, dwo = np.zeros(n, bool), np.zeros(n, bool)
            dwi[m_is], dwo[m_oos] = dd_window_mask(r[m_is]), dd_window_mask(r[m_oos])
            BIS["DDWIN"][nm] = ols_beta(r[dwi], spy[dwi]) if dwi.sum() >= MINOBS else np.nan
            BOOS["DDWIN"][nm] = ols_beta(r[dwo], spy[dwo]) if dwo.sum() >= MINOBS else np.nan
            book_rows.append(dict(panel=pname, book=nm, CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                  H1=sharpe(r[:h]), H2=sharpe(r[h:]), IS_Sharpe=sharpe(r[m_is]),
                                  OOS_CAGR=cagr(r[m_oos]), OOS_Sharpe=sharpe(r[m_oos]),
                                  OOS_MaxDD=maxdd(r[m_oos]), dd_leg=truth[nm],
                                  beta_FULL=B["FULL"][nm], beta_SPYDD=B["SPYDD"][nm],
                                  beta_DDWIN=B["DDWIN"][nm]))

        tvec = np.array([truth[nm] for nm in names])
        dvec = np.array([dds[nm] for nm in names])
        P(f"   shelf = {len(names)} books;  4b DD leg passes on {int(tvec.sum())} of {len(names)} "
          f"(truth has {'VARIATION' if 0 < tvec.sum() < len(names) else 'NO VARIATION — agreement is degenerate'})")

        # ---- P1 x estimator grid
        for eset in EPISODES:
            em = emask[eset]
            for nm in names:
                r = rets[nm]
                B["FIXED"][nm] = ols_beta(r[em], spy[em])
                BIS["FIXED"][nm] = ols_beta(r[em & m_is], spy[em & m_is])
                BOOS["FIXED"][nm] = ols_beta(r[em & m_oos], spy[em & m_oos])
            for est in ESTIMATORS:
                bv = np.array([B[est][nm] for nm in names])
                ok = np.isfinite(bv)
                bc, ba = best_cap(bv, tvec)
                pred = bv <= BETA_CAP
                bb = bv[ok]
                M = np.triu(np.abs(bb[:, None] - bb[None, :]) <= MATCH_TOL, 1)
                npair = int(M.sum())
                dis = int((M & (tvec[ok][:, None] != tvec[ok][None, :])).sum())
                bi = np.array([BIS[est][nm] for nm in names])
                bo = np.array([BOOS[est][nm] for nm in names])
                row = dict(panel=pname, episode_set=eset, estimator=est, n=int(ok.sum()),
                           dd_pass=int(tvec.sum()), beta_pass=int((pred & ok).sum()),
                           agree=float((pred[ok] == tvec[ok]).mean()) if ok.any() else np.nan,
                           best_agree=ba, beta_star=bc,
                           spearman_beta_dd=spearman(bv, dvec),
                           n_pairs=npair, n_disagree=dis,
                           pair_disagree=(dis / npair if npair else np.nan),
                           rho_S_is_oos=spearman(bi, bo), rho_P_is_oos=pearson(bi, bo),
                           n_is_oos=int((np.isfinite(bi) & np.isfinite(bo)).sum()),
                           median_beta=float(np.nanmedian(bv)))
                agree_rows.append(row)
                if est == "FIXED":
                    persist_rows.append(row)

        A = pd.DataFrame([r for r in agree_rows if r["panel"] == pname])
        P(f"\n   AGREEMENT with the 4b DD leg at the fixed cap beta <= {BETA_CAP}, FULL window, and "
          f"PERSISTENCE rho(beta_IS, beta_OOS) over the {len(names)}-book shelf:")
        P(f"     {'set':<7}{'estimator':<9}{'n':>4}{'agree':>8}{'best':>8}{'beta*':>8}"
          f"{'pairs':>7}{'disag':>7}{'rho_S':>8}{'rho_P':>8}{'n_pair':>8}")
        for eset in EPISODES:
            for est in ESTIMATORS:
                r = A[(A.episode_set == eset) & (A.estimator == est)].iloc[0]
                star = " <<" if (est == "FIXED" and r.agree >= AGREE_BAR and r.rho_S_is_oos >= PERSIST_BAR) else ""
                P(f"     {eset:<7}{est:<9}{int(r.n):>4}{r.agree:>8.4f}{r.best_agree:>8.4f}"
                  f"{r.beta_star:>8.3f}{int(r.n_pairs):>7}{int(r.n_disagree):>7}"
                  f"{r.rho_S_is_oos:>8.3f}{r.rho_P_is_oos:>8.3f}{int(r.n_is_oos):>8}{star}")
            if eset != list(EPISODES)[-1]:
                P("     " + "-" * 80)

        # ---- CAPITAL ARM (rule 8): IS-only episode-beta screen, then IS Sharpe, OOS read once
        P(f"\n   ---- RULE 8: IS-ONLY screen (beta_EST(IS) <= {BETA_CAP}) then max IS Sharpe; "
          f"2017+ read ONCE ----")
        bk = pd.DataFrame([r for r in book_rows if r["panel"] == pname]).set_index("book")
        for eset in EPISODES:
            em = emask[eset]
            for nm in names:
                r = rets[nm]
                BIS["FIXED"][nm] = ols_beta(r[em & m_is], spy[em & m_is])
            for est, tag in (("FIXED", eset), ("SPYDD", "-"), ("FULL", "-"), ("NONE", "-")):
                if est != "FIXED" and eset != list(EPISODES)[0]:
                    continue                    # the non-episode screens and the control run once, not per rung
                if est == "NONE":
                    adm = list(names)
                else:
                    adm = [nm for nm in names if np.isfinite(BIS[est][nm]) and BIS[est][nm] <= BETA_CAP]
                if not adm:
                    P(f"     {eset:<7} screen {est:<6}: 0 of {len(names)} books admitted — no pick")
                    wf_rows.append(dict(panel=pname, episode_set=eset, screen=est, admitted=0))
                    continue
                pick = sorted(adm, key=lambda nm: (-bk.loc[nm, "IS_Sharpe"], nm))[0]
                r = rets[pick]
                p4b = (sharpe(r[:h]) > spy_s["H1"] and sharpe(r[h:]) > spy_s["H2"]
                       and sharpe(r[m_oos]) > spy_s["OOS_S"] and maxdd(r) >= DD_CAP * spy_s["MaxDD"]
                       and cagr(r) >= CAGR_FLOOR * spy_s["CAGR"])
                p4a = (sharpe(r[:h]) > base_s["H1"] and sharpe(r[h:]) > base_s["H2"]
                       and maxdd(r) >= base_s["MaxDD"])
                oos_dd_leg = bool(maxdd(r[m_oos]) >= DD_CAP * spy_s["OOS_DD"])
                wf_rows.append(dict(panel=pname, episode_set=(eset if est == "FIXED" else "-"),
                                    screen=est, admitted=len(adm), pick=pick,
                                    IS_Sharpe=bk.loc[pick, "IS_Sharpe"],
                                    CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                    H1=sharpe(r[:h]), H2=sharpe(r[h:]),
                                    OOS_CAGR=cagr(r[m_oos]), OOS_Sharpe=sharpe(r[m_oos]),
                                    OOS_MaxDD=maxdd(r[m_oos]), oos_dd_leg=oos_dd_leg,
                                    pass4a=p4a, pass4b=p4b))
                P(f"     {(eset if est=='FIXED' else '—'):<7} screen {est:<6}: {len(adm):>3}/{len(names)} "
                  f"admitted, pick {pick:<16} OOS {cagr(r[m_oos]):>7.2%} / {sharpe(r[m_oos]):>7.4f} / "
                  f"{maxdd(r[m_oos]):>8.2%}  OOS-DD-leg {'PASS' if oos_dd_leg else 'FAIL'}  "
                  f"4a {'PASS' if p4a else 'FAIL'}  4b {'PASS' if p4b else 'FAIL'}")

        if pname == "U56":
            gate("G1 episode masks are book-independent (one day set per panel, shared by 80 books)",
                 f"{len(emask)} masks, {int(emask['E5'].sum())} E5 days", "true", True)
            gate("G2 E5 has days in BOTH windows (persistence is defined)",
                 f"IS {int((emask['E5'] & m_is).sum())}, OOS {int((emask['E5'] & m_oos).sum())}",
                 ">= 20 each", (emask['E5'] & m_is).sum() >= MINOBS and (emask['E5'] & m_oos).sum() >= MINOBS)
            gate("G3 SPYDD's window really does move with the sample (910's premise)",
                 f"IS window {dates[spydd_is][0].date() if spydd_is.any() else '-'}..{dates[spydd_is][-1].date() if spydd_is.any() else '-'}, "
                 f"OOS window {dates[spydd_oos][0].date() if spydd_oos.any() else '-'}..{dates[spydd_oos][-1].date() if spydd_oos.any() else '-'}",
                 "the two windows are DISJOINT (that is what makes SPYDD sample-dependent)",
                 not bool((spydd_is & spydd_oos).any()) and spydd_is.any() and spydd_oos.any())
            gate("G4 the DD-leg truth has variation on the shelf",
                 f"{int(tvec.sum())} of {len(names)} pass", "strictly between 0 and 80",
                 0 < tvec.sum() < len(names))
            gate("G5 SPY's beta on itself is 1 (estimator sanity)", f"{ols_beta(spy, spy):.6f}", "1.000000",
                 abs(ols_beta(spy, spy) - 1.0) < 1e-9)

    # ------------------------------------------------------------------ verdicts
    P("\n" + "=" * 100)
    P("PRE-STATED VERDICTS")
    A = pd.DataFrame(agree_rows)
    F = A[A.estimator == "FIXED"]
    v1 = F[F.rho_S_is_oos >= PERSIST_BAR]
    P(f"  V1 persistence: FIXED reads rho_S >= {PERSIST_BAR} in {len(v1)} of {len(F)} "
      f"(episode set x panel) cells -> {'TRIGGERED' if len(v1) else 'NOT TRIGGERED'}")
    if len(F):
        b = F.loc[F.rho_S_is_oos.idxmax()]
        P(f"     best FIXED persistence: {b.episode_set}/{b.panel} rho_S {b.rho_S_is_oos:.3f} "
          f"(Pearson {b.rho_P_is_oos:.3f}), agreement {b.agree:.4f}")
    v2 = F[F.agree >= AGREE_BAR]
    P(f"  V2 agreement: FIXED reads agree >= {AGREE_BAR} in {len(v2)} of {len(F)} cells -> "
      f"{'TRIGGERED' if len(v2) else 'NOT TRIGGERED'}")
    both = F[(F.rho_S_is_oos >= PERSIST_BAR) & (F.agree >= AGREE_BAR)]
    P(f"  V3 BOTH AT ONCE (the idea's own question): {len(both)} of {len(F)} cells -> "
      f"{'TRIGGERED' if len(both) else 'NOT TRIGGERED — persistence and agreement are still not simultaneously purchasable'}")
    if len(both):
        for _, r in both.iterrows():
            P(f"     {r.episode_set}/{r.panel}: agree {r.agree:.4f}, rho_S {r.rho_S_is_oos:.3f}")
    hand = F[F.episode_set != "BEAR10"]
    wins = 0
    for pn in PANELS:
        hp = hand[hand.panel == pn].rho_S_is_oos.max()
        bp = F[(F.panel == pn) & (F.episode_set == "BEAR10")].rho_S_is_oos
        if len(bp) and np.isfinite(hp) and hp > float(bp.iloc[0]):
            wins += 1
    P(f"  V4 hand-picked calendar beats the rule-defined BEAR10 control on persistence: {wins} of "
      f"{len(PANELS)} panels -> {'TRIGGERED' if wins > len(PANELS)/2 else 'NOT TRIGGERED'}")
    W = pd.DataFrame(wf_rows)
    wf_ok = W[(W.screen == "FIXED") & (W.get("oos_dd_leg") == True)] if "oos_dd_leg" in W else W.iloc[0:0]
    ctrl = W[(W.screen == "NONE")]
    ctrl_ok = bool(ctrl["oos_dd_leg"].any()) if len(ctrl) and "oos_dd_leg" in ctrl else False
    P(f"  V5 capital: the IS-only FIXED screen reaches an OOS-DD-leg-passing book in "
      f"{len(wf_ok)} of {int((W.screen=='FIXED').sum())} (set x panel) cells; the unscreened "
      f"control passes it in {int(ctrl['oos_dd_leg'].sum()) if len(ctrl) and 'oos_dd_leg' in ctrl else 0} "
      f"of {len(ctrl)} -> {'TRIGGERED' if len(wf_ok) and not ctrl_ok else 'NOT TRIGGERED'}")
    P(f"     4b passes among all rule-8 picks: {int(W.get('pass4b', pd.Series(dtype=bool)).sum())} of "
      f"{int(W.pick.notna().sum()) if 'pick' in W else 0};  4a passes: "
      f"{int(W.get('pass4a', pd.Series(dtype=bool)).sum())}")

    P("\n  910's own numbers for reference: SPYDD rho(beta_IS, beta_OOS) = +0.216 / +0.292, "
      "against +0.757..+0.993 for its other nine proxies.  This run's SPYDD, same statistic, "
      "on this shelf:")
    for pn in PANELS:
        s = A[(A.panel == pn) & (A.estimator == "SPYDD")].iloc[0]
        f5 = A[(A.panel == pn) & (A.estimator == "FIXED") & (A.episode_set == "E5")].iloc[0]
        fu = A[(A.panel == pn) & (A.estimator == "FULL")].iloc[0]
        P(f"     {pn:<6} SPYDD rho_S {s.rho_S_is_oos:+.3f} agree {s.agree:.4f}   |   "
          f"FIXED/E5 rho_S {f5.rho_S_is_oos:+.3f} agree {f5.agree:.4f}   |   "
          f"FULL rho_S {fu.rho_S_is_oos:+.3f} agree {fu.agree:.4f}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(agree_rows).to_csv(f"{OUT}.agree.csv", index=False)
    pd.DataFrame(book_rows).to_csv(f"{OUT}.books.csv", index=False)
    pd.DataFrame(wf_rows).to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(mask_rows).to_csv(f"{OUT}.episodes.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LINES) + "\n")
    P(f"\nwrote {OUT.name}.{{agree,books,walkforward,episodes,gates}}.csv and .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
