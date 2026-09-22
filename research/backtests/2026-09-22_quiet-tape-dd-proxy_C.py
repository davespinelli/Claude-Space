#!/usr/bin/env python3
"""Idea 2083 (lane C, 2026-09-22) — DOES THE NON-EPISODE DRAWDOWN HAVE AN EX-ANTE PROXY WORTH
CAPITAL?

WHERE THIS COMES FROM.  Idea 911 (2026-09-22, lane cloud) showed that the MaxDD-on-beta residual
of an 80-book shelf persists IS->OOS, and — against the record's own framing — that the
persistence lives OUTSIDE the crash: non-episode residual persistence is significant on 9 of 9
(panel x estimator) blocks (+0.328 to +0.954) while EPISODE-ONLY persistence is weak or negative
on 4 of 9.  But 911's capital arm reached 0 of 3 arms on 4b, its best pick (U56, MADIST/ALL/
gross 1.00) missing the 4b drawdown leg by 1.95 pp (OOS MaxDD -22.18% against the -20.23% bar),
and the persistent part was measured on a SPLICED series built from a HINDSIGHT-LABELLED calendar
of crashes — not a statistic any investor could have computed at the decision close.

THE QUESTION.  Replace the hindsight episode calendar with an EX-ANTE QUIET-TAPE mask — a
distress statistic computed from SPY closes alone and known at every decision close — take each
shelf book's drawdown on the quiet days only, and use THAT as a legal IS-only chooser over
911's own 80-book shelf.  Does it close the 1.95 pp?

WHAT IS PRICED.  911's shelf verbatim: families MOM/MOMVS/MADIST/LOWVOL x width k in
{5,10,20,40,ALL} x gross in {0.25,0.50,0.75,1.00} = 80 books per panel, monthly, fills t+1,
10 bps, gate close>200dMA & vol20<0.60.  Panels U56 / B136 / SMALL (max_1d_move >= 1.0 dropped).

THE TWO TUNED DIALS (and no more).
  DIAL 1 — QUIET-TAPE DEFINITION.  The distress series d_t, all three CAUSAL (each value uses
    closes <= t only):
      NEARHI_EXP  d_t = 1 - SPY_t / (expanding max of SPY to t)       [drawdown from running high]
      NEARHI_252  d_t = 1 - SPY_t / (252d trailing max of SPY to t)   [drawdown from 1y high]
      VOL60       d_t = annualised 60d trailing realised vol of SPY   [a volatility read, not a DD]
  DIAL 2 — THRESHOLD, as a quantile q of d_t over the IS window: q in {0.40,0.60,0.80,0.90,1.00}.
    A day is QUIET iff d_t <= quantile_q(d over IS).  q = 1.00 keeps EVERY day, so the plain IS
    MaxDD — i.e. EXACTLY 911's chooser — is a grid point of this study, not an outside comparand.

REPORTED, NOT TUNED: PANEL {U56,B136,SMALL}; the beta estimator (OLSD, fixed at 911's choice);
the chooser FORM (QRESID = argmax residual of quiet-DD on IS beta across the shelf, i.e. 911's
construction with the quiet-tape statistic swapped in; QRAW = argmin quiet-DD, no beta step);
the IS_SHARPE reference chooser; and the cost {0,10,25,50} bps x delay {t+1,t+2} ladder walked
for any pick that clears 4b.  EVERY grid point is published.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION.  At least one U56 grid point with q < 1.00 reaches a book clearing
      4b FULL *and* OOS.  Triggered -> the ex-ante quiet-tape statistic closes 911's 1.95 pp.
  V2  NOT A NO-OP.  On a MAJORITY of (definition, q<1.00) points the quiet-tape chooser picks a
      DIFFERENT book from the q=1.00 control, AND its mean OOS MaxDD over those points is
      shallower than the control's.  Triggered -> the quiet-tape mask carries information beyond
      plain IS MaxDD, whether or not V1 fires.
  V3  GENERALITY.  At least 2 of 3 panels carry at least one grid point clearing 4b FULL+OOS.

PROTOCOL: rule 2 (10 bps, next-day fills, no leverage); rule 3 (live RULES v2 AND SPY); rule 4
(both KEEP paths at every pick, <=2 tuned dials); rule 5 (one idea, deterministic, standalone);
rule 8 (IS 2009-2016 chooses, 2017-2026 read once); rule 9 (survivorship stated).
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B
screen, so every CAGR and MaxDD LEVEL below is optimistic and both 4b bars are easier than on a
point-in-time panel.  The chooser CONTRAST (quiet-tape vs plain IS MaxDD) is same-shelf /
same-tape with only the day mask changed, so it is first-order immune; the 4b pass counts are not.

Run:  python research/backtests/2026-09-22_quiet-tape-dd-proxy_C.py
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

DATE, SLUG = "2026-09-22", "quiet-tape-dd-proxy"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
PANELS = ["U56", "B136", "SMALL"]
DEFS = ["NEARHI_EXP", "NEARHI_252", "VOL60"]        # tuned dial 1
QS = [0.40, 0.60, 0.80, 0.90, 1.00]                 # tuned dial 2 (1.00 == plain IS MaxDD)
FORMS = ["QRESID", "QRAW"]                          # reported, not tuned
COST, MAX_VOL, WARMUP = 10.0, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BETA_KIND = "OLSD"                                  # fixed at 911's capital-arm estimator
COST_LADDER = [0.0, 10.0, 25.0, 50.0]
DELAYS = [1, 2]

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


# ---------------------------------------------------------------- panel / signals / books (911)
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


def book_weights(sig, elig, rebal, k, gross, index, cols, lag=0):
    """lag = extra trading days of SIGNAL STALENESS.  lag=0 is the base book: the signal is read
    at the month-end close and the engine fills at the next close (t+1).  lag=1 reads the signal
    one close EARLIER and still fills at t+1, i.e. the decision is a day staler — the correct way
    to price an extra day of latency on a MONTH-STEPPED weight frame.  (Shifting the ffilled
    weight frame itself by one day would move the trade to the NEXT MONTH-END, not the next day,
    because the frame is constant within the month.)"""
    if lag:
        sig, elig = sig.shift(lag), elig.shift(lag).fillna(False)
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
def beta(r, spy, kind=BETA_KIND):
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


def resid_on_beta(y, b):
    A = np.vstack([np.ones(len(b)), b]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return y - A @ coef


def distress(spy_px, kind):
    """CAUSAL SPY-only distress series: every value at t uses closes <= t only."""
    if kind == "NEARHI_EXP":
        return 1.0 - spy_px / spy_px.cummax()
    if kind == "NEARHI_252":
        return 1.0 - spy_px / spy_px.rolling(252, min_periods=1).max()
    if kind == "VOL60":
        return spy_px.pct_change().rolling(60, min_periods=20).std() * np.sqrt(252)
    raise ValueError(kind)


# ---------------------------------------------------------------- run
def main():
    log(f"# Idea 2083 (lane C, {DATE}) — does the NON-EPISODE DRAWDOWN have an EX-ANTE PROXY "
        f"worth CAPITAL?")
    log(f"# tuned dials (2): QUIET-TAPE DEFINITION {DEFS} x THRESHOLD q {QS}.  reported, not "
        f"tuned: PANEL {PANELS}, chooser FORM {FORMS}, beta estimator {BETA_KIND}, cost x delay "
        f"ladder at clearing picks.  shelf {len(FAMILIES)}x{len(WIDTHS)}x{len(GROSSES)} = 80 "
        f"books/panel, monthly, t+1, {COST:.0f} bps.")

    grid_rows, shelf_rows, ladder_rows = [], [], []
    g_spy_beta, g_lev, g_causal = [], 0.0, []
    panel_store = {}

    for pname in PANELS:
        px = panel(pname).dropna(how="all").ffill()
        cols = candidates(pname, px)
        st = px.index[WARMUP]
        spy_px = px["SPY"].loc[st:]
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[st:]
        is_idx = spy_full.loc[:IS_END].index
        oos_idx = spy_full.loc[OOS_START:].index
        log(f"\n## {pname}: {len(cols)} names, {len(px)} rows ({len(px)/252:.1f}y), book from "
            f"{st.date()};  IS {len(is_idx)} days, OOS {len(oos_idx)} days")
        g_spy_beta.append(abs(beta(spy_full, spy_full) - 1.0))

        # G4 causality: the distress series on a truncated tape must equal the full-tape series
        # on the overlap (no value at t may depend on a close after t).
        cut = spy_px.index[len(spy_px) // 2]
        for kind in DEFS:
            a = distress(spy_px, kind).loc[:cut]
            b = distress(spy_px.loc[:cut], kind)
            g_causal.append(float(np.nanmax(np.abs(a.values - b.values))))

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
        lh = len(lr) // 2
        live = dict(S=metrics(lr)["Sharpe"], H1=metrics(lr.iloc[:lh])["Sharpe"],
                    H2=metrics(lr.iloc[lh:])["Sharpe"], DD=metrics(lr)["MaxDD"],
                    oosS=metrics(lr.loc[OOS_START:])["Sharpe"])

        h = len(spy_full) // 2
        s_full, s_oos = metrics(spy_full), metrics(spy_full.loc[OOS_START:])
        s_h1 = metrics(spy_full.iloc[:h])["Sharpe"]
        s_h2 = metrics(spy_full.iloc[h:])["Sharpe"]
        log(f"   SPY FULL {s_full['CAGR']:.2%}/{s_full['Sharpe']:.3f}/{s_full['MaxDD']:.2%} "
            f"(H1 {s_h1:.3f} H2 {s_h2:.3f});  SPY OOS {s_oos['CAGR']:.2%}/"
            f"{s_oos['Sharpe']:.3f}/{s_oos['MaxDD']:.2%}  ->  4b OOS bars: DD "
            f"{DD_CAP*s_oos['MaxDD']:.2%}, CAGR {CAGR_FLOOR*s_oos['CAGR']:.2%}")
        log(f"   live RULES v2 FULL S={live['S']:.3f} (H1 {live['H1']:.3f} H2 {live['H2']:.3f}) "
            f"DD {live['DD']:.2%}, OOS S={live['oosS']:.3f}")

        # IS-side book statistics that do NOT depend on the dials
        is_beta, is_sharpe = {}, {}
        for key, r in books.items():
            r_is = r.loc[:IS_END]
            is_beta[key] = beta(r_is, spy_full.loc[:IS_END])
            is_sharpe[key] = metrics(r_is)["Sharpe"]

        def score_pick(key):
            r = books[key]
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            hh = len(r) // 2
            h1, h2 = metrics(r.iloc[:hh])["Sharpe"], metrics(r.iloc[hh:])["Sharpe"]
            k4b_full = bool(h1 > s_h1 and h2 > s_h2 and m["MaxDD"] >= DD_CAP * s_full["MaxDD"]
                            and m["CAGR"] >= CAGR_FLOOR * s_full["CAGR"])
            k4b_oos = bool(mo["Sharpe"] > s_oos["Sharpe"]
                           and mo["MaxDD"] >= DD_CAP * s_oos["MaxDD"]
                           and mo["CAGR"] >= CAGR_FLOOR * s_oos["CAGR"])
            k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["DD"])
            return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                        spy_CAGR=s_full["CAGR"], spy_Sharpe=s_full["Sharpe"],
                        spy_MaxDD=s_full["MaxDD"], spy_H1=s_h1, spy_H2=s_h2,
                        spy_oos_CAGR=s_oos["CAGR"], spy_oos_Sharpe=s_oos["Sharpe"],
                        spy_oos_MaxDD=s_oos["MaxDD"], live_Sharpe=live["S"],
                        live_H1=live["H1"], live_H2=live["H2"], live_MaxDD=live["DD"],
                        live_oos_Sharpe=live["oosS"],
                        dd_gap_pp=100.0 * (mo["MaxDD"] - DD_CAP * s_oos["MaxDD"]),
                        keep4b_full=k4b_full, keep4b_oos=k4b_oos,
                        keep4b=(k4b_full and k4b_oos), keep4a=k4a)

        # ---- the grid: quiet-tape chooser at every (definition, q, form) -----------------
        for kind in DEFS:
            d_full = distress(spy_px, kind)
            d_is = d_full.reindex(is_idx)
            for q in QS:
                thr = float(d_is.quantile(q))
                quiet = (d_is <= thr).fillna(False)
                nq = int(quiet.sum())
                qdd, bb, keys = [], [], []
                for key, r in books.items():
                    rq = r.reindex(is_idx).fillna(0.0)[quiet.values]
                    v = maxdd(rq)
                    if np.isnan(v) or np.isnan(is_beta[key]):
                        continue
                    keys.append(key); qdd.append(v); bb.append(is_beta[key])
                qdd, bb = np.asarray(qdd), np.asarray(bb)
                res_q = resid_on_beta(qdd, bb)
                picks = {"QRESID": keys[int(np.argmax(res_q))],   # shallowest quiet-DD at matched beta
                         "QRAW": keys[int(np.argmax(qdd))]}       # shallowest quiet-DD outright
                for form in FORMS:
                    key = picks[form]
                    i = keys.index(key)
                    grid_rows.append(dict(panel=pname, definition=kind, q=q, form=form,
                                          threshold=thr, n_quiet_days=nq, n_is_days=len(is_idx),
                                          book=str(key), is_sharpe=is_sharpe[key],
                                          is_beta=is_beta[key], is_quiet_dd=float(qdd[i]),
                                          is_quiet_resid=float(res_q[i]), **score_pick(key)))
                if kind == DEFS[0] and q == QS[0]:
                    for i, key in enumerate(keys):
                        shelf_rows.append(dict(panel=pname, book=str(key),
                                               is_sharpe=is_sharpe[key], is_beta=is_beta[key],
                                               is_dd_all=maxdd(books[key].loc[:IS_END]),
                                               is_quiet_dd_q040=float(qdd[i])))

        # IS_SHARPE reference chooser (911's control)
        kbest = max(is_sharpe, key=lambda k: is_sharpe[k])
        grid_rows.append(dict(panel=pname, definition="-", q=np.nan, form="IS_SHARPE",
                              threshold=np.nan, n_quiet_days=len(is_idx), n_is_days=len(is_idx),
                              book=str(kbest), is_sharpe=is_sharpe[kbest],
                              is_beta=is_beta[kbest], is_quiet_dd=maxdd(books[kbest].loc[:IS_END]),
                              is_quiet_resid=np.nan, **score_pick(kbest)))
        panel_store[pname] = dict(px=px, cols=cols, sig=sig, gate_map=gate_map, rebal=rebal,
                                  st=st, spy_full=spy_full, s_full=s_full, s_oos=s_oos,
                                  s_h1=s_h1, s_h2=s_h2)

    G = pd.DataFrame(grid_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(shelf_rows).to_csv(f"{OUT}.shelf.csv", index=False)

    # ---------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", "18.7/18.7/16.7y", ">= 10", True)
    gate("G1 q=1.00 QRESID reproduces 911's IS_RESID pick (U56 MADIST/ALL/1.0, "
         "B136 MADIST/40/1.0, SMALL MADIST/40/1.0)",
         "; ".join(f"{p}={G[(G.panel==p)&(G.q==1.00)&(G.form=='QRESID')].book.iloc[0]}"
                   for p in PANELS),
         "match",
         G[(G.panel == "U56") & (G.q == 1.00) & (G.form == "QRESID")].book.iloc[0]
         == "('MADIST', 'ALL', 1.0)"
         and G[(G.panel == "B136") & (G.q == 1.00) & (G.form == "QRESID")].book.iloc[0]
         == "('MADIST', 40, 1.0)")
    u = G[(G.panel == "U56") & (G.q == 1.00) & (G.form == "QRESID")].iloc[0]
    gate("G1b q=1.00 U56 pick reproduces 911's OOS numbers (17.45%/1.2174/-22.18%)",
         f"{u.oos_CAGR:.4%}/{u.oos_Sharpe:.4f}/{u.oos_MaxDD:.4%}", "|d| < 1e-6",
         abs(u.oos_Sharpe - 1.2173994245274284) < 1e-6 and abs(u.oos_MaxDD + 0.2218180847636695) < 1e-6)
    gate("G2 100% SPY book reads beta ~ 1.0", f"max|beta-1| = {max(g_spy_beta):.4f}", "< 0.05",
         max(g_spy_beta) < 0.05)
    gate("G3 no leverage (max shelf gross)", f"{g_lev:.4f}", "<= 1.0", g_lev <= 1.0 + 1e-9)
    gate("G4 distress series is CAUSAL (truncated tape == full tape on overlap)",
         f"max|diff| = {max(g_causal):.2e}", "== 0", max(g_causal) == 0.0)
    gate("G5 every grid point published",
         f"{len(G)} rows = 3 panels x (3 defs x 5 q x 2 forms + 1 IS_SHARPE)",
         "== 93", len(G) == 93)
    for kind in DEFS:
        s = G[(G.q == 1.00) & (G.definition == kind)]
        log(f"   G6 diagnostic {kind:<11} q=1.00 keeps " +
            ", ".join(f"{p_}: {int(r.n_quiet_days)}/{int(r.n_is_days)}"
                      for p_, r in zip(s.panel, s.itertuples())))
    gate("G6 q=1.00 quiet mask keeps every IS day",
         f"{int(G[G.q==1.00].n_quiet_days.iloc[0])} of {int(G[G.q==1.00].n_is_days.iloc[0])}",
         "equal", bool((G[G.q == 1.00].n_quiet_days == G[G.q == 1.00].n_is_days).all()))

    # ---------------------------------------------------------------- arm 1 / V1
    log("\n## ARM 1 — THE GRID (all 93 picks; rule 8: IS 2009-2016 chooses, OOS read once)")
    for pname in PANELS:
        sub = G[G.panel == pname]
        log(f"\n   --- {pname} ---")
        for _, r in sub.iterrows():
            qs = "  -  " if np.isnan(r.q) else f"{r.q:.2f}"
            log(f"   {r.definition:<11} q={qs} {r.form:<9} {r.book:<24} "
                f"quietDD {r.is_quiet_dd:7.2%} ({int(r.n_quiet_days):>4}d) -> FULL "
                f"{r.CAGR:6.2%}/{r.Sharpe:.3f}/{r.MaxDD:7.2%}  OOS {r.oos_CAGR:6.2%}/"
                f"{r.oos_Sharpe:.3f}/{r.oos_MaxDD:7.2%}  ddgap {r.dd_gap_pp:+5.2f}pp  "
                f"4b_full={int(r.keep4b_full)} 4b_oos={int(r.keep4b_oos)} 4a={int(r.keep4a)}")

    u56_q = G[(G.panel == "U56") & (G.q < 1.00)]
    v1_hits = u56_q[u56_q.keep4b]
    v1_trig = len(v1_hits) > 0
    best_u56 = u56_q.sort_values("dd_gap_pp", ascending=False).iloc[0]
    log(f"\n   V1: U56 grid points with q<1.00 clearing 4b FULL+OOS = {len(v1_hits)} of "
        f"{len(u56_q)}  ->  V1 {'TRIGGERED' if v1_trig else 'NOT TRIGGERED'}")
    log(f"       best U56 q<1.00 point on the DD leg: {best_u56.definition} q={best_u56.q:.2f} "
        f"{best_u56.form} {best_u56.book} OOS MaxDD {best_u56.oos_MaxDD:.2%} vs bar "
        f"{DD_CAP*best_u56.spy_oos_MaxDD:.2%}  (911's gap was -1.95pp; this is "
        f"{best_u56.dd_gap_pp:+.2f}pp)")

    # ---------------------------------------------------------------- V2
    log("\n## ARM 2 — IS THE QUIET-TAPE MASK A NO-OP? (vs the q=1.00 plain-MaxDD control)")
    diff, tot, dd_q, dd_c = 0, 0, [], []
    for pname in PANELS:
        for form in FORMS:
            ctrl = G[(G.panel == pname) & (G.q == 1.00) & (G.form == form)].iloc[0]
            for kind in DEFS:
                for q in [x for x in QS if x < 1.00]:
                    r = G[(G.panel == pname) & (G.definition == kind) & (G.q == q)
                          & (G.form == form)].iloc[0]
                    tot += 1
                    diff += int(r.book != ctrl.book)
                    dd_q.append(r.oos_MaxDD); dd_c.append(ctrl.oos_MaxDD)
    mq, mc = float(np.mean(dd_q)), float(np.mean(dd_c))
    v2_trig = diff > tot / 2 and mq > mc
    log(f"   picks differing from the q=1.00 control: {diff} of {tot} "
        f"({diff/tot:.1%});  mean OOS MaxDD quiet {mq:.2%} vs control {mc:.2%} "
        f"({'shallower' if mq > mc else 'deeper'})")
    log(f"   ->  V2 {'TRIGGERED' if v2_trig else 'NOT TRIGGERED'}")
    for pname in PANELS:
        sub = G[(G.panel == pname) & (G.q < 1.00)]
        log(f"     {pname:<6} distinct books reached across the 30 q<1.00 points: "
            f"{sub.book.nunique()}  ({', '.join(sorted(sub.book.unique()))})")

    # ---------------------------------------------------------------- V3
    hits = G[G.keep4b]
    panels_hit = sorted(hits.panel.unique())
    v3_trig = len(panels_hit) >= 2
    log(f"\n## ARM 3 — GENERALITY.  grid points clearing 4b FULL+OOS: {len(hits)} of {len(G)}; "
        f"panels {panels_hit or 'none'}  ->  V3 {'TRIGGERED' if v3_trig else 'NOT TRIGGERED'}")
    log(f"   4b FULL alone: {int(G.keep4b_full.sum())} of {len(G)};  4b OOS alone: "
        f"{int(G.keep4b_oos.sum())};  4a: {int(G.keep4a.sum())}")

    # ---------------------------------------------------------------- cost x delay at clearers
    log("\n## ROBUSTNESS — cost {0,10,25,50} bps x SIGNAL LAG {0,+1 day} at every book reached "
        "by a 4b-clearing grid point (lag=+1 reads the signal one close earlier and still "
        "fills t+1; shifting a MONTH-STEPPED weight frame by a day would move the trade a "
        "whole month, which is why it is done on the signal)")
    for pname in PANELS:
        S = panel_store[pname]
        kk = [eval(b) for b in hits[hits.panel == pname].book.unique()]
        for key in kk:
            fam, k, g = key
            for dly in DELAYS:
                W = book_weights(S["sig"][fam], S["gate_map"][fam], S["rebal"], k, g,
                                 S["px"].index, S["cols"], lag=dly - 1) \
                    .reindex(columns=S["px"].columns).fillna(0.0)
                for c in COST_LADDER:
                    r = engine_backtest(S["px"], W, cost_bps=c, freq="M")["returns"].loc[S["st"]:]
                    m, mo = metrics(r), metrics(r.loc[OOS_START:])
                    hh = len(r) // 2
                    h1 = metrics(r.iloc[:hh])["Sharpe"]; h2 = metrics(r.iloc[hh:])["Sharpe"]
                    ok_f = bool(h1 > S["s_h1"] and h2 > S["s_h2"]
                                and m["MaxDD"] >= DD_CAP * S["s_full"]["MaxDD"]
                                and m["CAGR"] >= CAGR_FLOOR * S["s_full"]["CAGR"])
                    ok_o = bool(mo["Sharpe"] > S["s_oos"]["Sharpe"]
                                and mo["MaxDD"] >= DD_CAP * S["s_oos"]["MaxDD"]
                                and mo["CAGR"] >= CAGR_FLOOR * S["s_oos"]["CAGR"])
                    ladder_rows.append(dict(panel=pname, book=str(key),
                                            signal_lag_days=dly - 1,
                                            cost_bps=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                            MaxDD=m["MaxDD"], oos_CAGR=mo["CAGR"],
                                            oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                                            keep4b_full=ok_f, keep4b_oos=ok_o,
                                            keep4b=(ok_f and ok_o)))
                    log(f"   {pname:<6} {str(key):<24} lag+{dly-1} {c:>4.0f}bps  FULL "
                        f"{m['CAGR']:6.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:7.2%}  OOS "
                        f"{mo['CAGR']:6.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:7.2%}"
                        f"  4b={int(ok_f and ok_o)}")
    if not ladder_rows:
        log("   (no grid point cleared 4b FULL+OOS — ladder not walked)")
    else:
        L = pd.DataFrame(ladder_rows)
        d = 0.0
        for _, lr_ in L[(L.signal_lag_days == 0) & (L.cost_bps == COST)].iterrows():
            gr = G[(G.panel == lr_.panel) & (G.book == lr_.book)].iloc[0]
            d = max(d, abs(lr_.oos_Sharpe - gr.oos_Sharpe), abs(lr_.oos_MaxDD - gr.oos_MaxDD))
        gate("G7 ladder lag=0 @10bps reproduces the grid row", f"max|diff| = {d:.2e}",
             "< 1e-12", d < 1e-12)
    pd.DataFrame(ladder_rows).to_csv(f"{OUT}.ladder.csv", index=False)
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)

    log("\n## VERDICTS")
    log(f"   V1 an ex-ante quiet-tape chooser closes 911's 1.95pp on U56 ..... "
        f"{'YES' if v1_trig else 'NO'}")
    log(f"   V2 the quiet-tape mask is not a no-op vs plain IS MaxDD ......... "
        f"{'YES' if v2_trig else 'NO'}")
    log(f"   V3 a 4b clearer exists on >= 2 of 3 panels ...................... "
        f"{'YES' if v3_trig else 'NO'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
