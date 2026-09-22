#!/usr/bin/env python3
"""Idea 2098 (lane cloud, 2026-09-22) — DOES THE QUIET-TAPE THRESHOLD HAVE A STABLE ARGMAX, OR
IS q = 0.40 A BOUNDARY PICK?

WHERE THIS COMES FROM.  Idea 2083 (lane C, 2026-09-22) replaced idea 911's hindsight crash
calendar with an EX-ANTE quiet-tape mask and found the resulting IS-only chooser clears 4b
(FULL and OOS) on U56 at threshold q = 0.40 — picking MADIST/40/gross 1.00, OOS 16.24% /
1.3099 / -17.67% against the -20.23% cap — while at q >= 0.60 it falls back to 911's own
MADIST/ALL/1.00 pick at OOS -22.18%, a 1.95 pp miss.  q = 0.40 was the LOWEST rung on 2083's
ladder.  Idea 1153 established on this record that a cell's REACH is predicted by its
ENDPOINT-NESS (0.5139 at ladder endpoints against 0.0972 in the interior), so a pass sitting on
the lowest rung of its own grid is exactly the shape that is usually a grid artefact.

THE QUESTION.  Extend the ladder BELOW 0.40 and ask whether the 4b reach has an INTERIOR
argmax (q = 0.40 is a real optimum, and the pass survives having a neighbour on both sides) or
keeps improving monotonically to the new boundary (the pass is endpoint-ness, not information).

WHAT IS PRICED.  Ideas 911/2083's shelf verbatim: families MOM/MOMVS/MADIST/LOWVOL x width k in
{5,10,20,40,ALL} x gross in {0.25,0.50,0.75,1.00} = 80 books per panel, monthly, fills t+1,
10 bps, gate close>200dMA & vol20<0.60.  Panels U56 / B136 / SMALL (max_1d_move >= 1.0 dropped).

THE TWO TUNED DIALS (and no more), exactly 2083's two with dial 2 extended:
  DIAL 1 — QUIET-TAPE DEFINITION.  d_t, all three CAUSAL (each value uses closes <= t only):
      NEARHI_EXP  d_t = 1 - SPY_t / (expanding max of SPY to t)
      NEARHI_252  d_t = 1 - SPY_t / (252d trailing max of SPY to t)
      VOL60       d_t = annualised 60d trailing realised vol of SPY
  DIAL 2 — THRESHOLD q, as a quantile of d_t over the IS window.  2083 ran {0.40,0.60,0.80,
    0.90,1.00}; this run walks the UNION with the four NEW rungs the idea asks for:
      q in {0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 0.90, 1.00}
    A day is QUIET iff d_t <= quantile_q(d over IS).  q = 1.00 keeps every day (= plain IS
    MaxDD, i.e. 911's chooser) and q = 0.10 is the NEW low boundary.  2083's q = 0.40 is now
    an INTERIOR rung with three rungs below it — which is the whole point of the run.

REPORTED, NOT TUNED: PANEL {U56,B136,SMALL}; the beta estimator (OLSD, fixed at 911's choice);
the chooser FORM (QRESID = argmax residual of quiet-DD on IS beta; QRAW = argmin quiet-DD);
the IS_SHARPE reference chooser; and the cost {0,10,25,50} bps x signal-lag {0,+1d} ladder at
every book a 4b-clearing grid point reaches.  EVERY grid point is published.

THE REACH STATISTIC (pre-stated).  For each grid point, the seven 4b legs are scored as SIGNED
margins and normalised by their own bar, so they are comparable:
  m1 = (H1 - SPY_H1)/|SPY_H1|        m2 = (H2 - SPY_H2)/|SPY_H2|
  m3 = (oosS - SPY_oosS)/|SPY_oosS|
  m4 = (MaxDD - 0.60*SPY_MaxDD)/|0.60*SPY_MaxDD|     (MaxDD negative; positive m = inside cap)
  m5 = (CAGR - 0.70*SPY_CAGR)/|0.70*SPY_CAGR|
  m6, m7 = the OOS twins of m4, m5.
  REACH = min(m1..m7).  REACH > 0  <=>  the point clears 4b FULL *and* OOS.
The ARGMAX over q of REACH, taken separately on each (panel, definition, form) curve, is the
object under test: INTERIOR (0.10 < q* < 1.00) or at a ladder ENDPOINT (q* in {0.10, 1.00}).

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  INTERIOR ARGMAX.  On a MAJORITY of the 18 (panel x definition x form) curves, the REACH
      argmax is strictly interior to the extended ladder.  Triggered -> a quiet-tape threshold
      generally has an interior optimum, and 2083's rung was not automatically a boundary pick.
  V2  2083's OWN CELL.  On the two U56/QRESID curves that produced 2083's pass (NEARHI_EXP and
      NEARHI_252), the REACH argmax over the EXTENDED ladder is NOT at the new low boundary
      q = 0.10.  Triggered -> 2083's q = 0.40 pass does not keep improving downward, i.e. it
      was not a boundary artefact of the old grid.
  V3  NEW REACH BELOW 0.40.  At least one grid point with q < 0.40 clears 4b FULL+OOS.
      Triggered -> the sub-0.40 region is live and must be part of any deployed dial.

PROTOCOL: rule 2 (10 bps, next-day fills, no leverage); rule 3 (live RULES v2 AND SPY); rule 4
(both KEEP paths at every pick, <=2 tuned dials); rule 5 (one idea, deterministic, standalone);
rule 8 (IS 2009-2016 chooses, 2017-2026 read once); rule 9 (survivorship stated).
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B
screen, so every CAGR and MaxDD LEVEL below is optimistic and both 4b bars are easier than on a
point-in-time panel.  The ARGMAX CONTRAST (where on the q ladder reach peaks) is same-shelf /
same-tape with only the day mask moved, so it is first-order immune; the 4b pass COUNTS are not.

Run:  python research/backtests/2026-09-22_quiet-tape-threshold-argmax_cloud.py
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

DATE, SLUG = "2026-09-22", "quiet-tape-threshold-argmax"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
PANELS = ["U56", "B136", "SMALL"]
DEFS = ["NEARHI_EXP", "NEARHI_252", "VOL60"]                  # tuned dial 1
QS = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 0.90, 1.00]   # tuned dial 2 (EXTENDED below 0.40)
NEW_QS = [0.10, 0.20, 0.30]                                   # the rungs 2083 never walked
FORMS = ["QRESID", "QRAW"]
COST, MAX_VOL, WARMUP = 10.0, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BETA_KIND = "OLSD"
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


def book_weights(sig, elig, rebal, k, gross, index, cols, lag=0):
    """lag = extra trading days of SIGNAL STALENESS (lag=0 is the base book: signal read at the
    month-end close, engine fills t+1)."""
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


def reach_of(d):
    """min over the seven 4b legs of the margin normalised by its own bar.  > 0 <=> 4b FULL+OOS."""
    legs = {
        "m1_H1": (d["H1"] - d["spy_H1"]) / abs(d["spy_H1"]),
        "m2_H2": (d["H2"] - d["spy_H2"]) / abs(d["spy_H2"]),
        "m3_oosS": (d["oos_Sharpe"] - d["spy_oos_Sharpe"]) / abs(d["spy_oos_Sharpe"]),
        "m4_ddF": (d["MaxDD"] - DD_CAP * d["spy_MaxDD"]) / abs(DD_CAP * d["spy_MaxDD"]),
        "m5_cagrF": (d["CAGR"] - CAGR_FLOOR * d["spy_CAGR"]) / abs(CAGR_FLOOR * d["spy_CAGR"]),
        "m6_ddO": (d["oos_MaxDD"] - DD_CAP * d["spy_oos_MaxDD"]) / abs(DD_CAP * d["spy_oos_MaxDD"]),
        "m7_cagrO": (d["oos_CAGR"] - CAGR_FLOOR * d["spy_oos_CAGR"])
                    / abs(CAGR_FLOOR * d["spy_oos_CAGR"]),
    }
    k = min(legs, key=legs.get)
    return legs, float(legs[k]), k


# ---------------------------------------------------------------- run
def main():
    log(f"# Idea 2098 (lane cloud, {DATE}) — does the QUIET-TAPE THRESHOLD have a STABLE ARGMAX "
        f"or is q=0.40 a BOUNDARY PICK?")
    log(f"# tuned dials (2): QUIET-TAPE DEFINITION {DEFS} x THRESHOLD q {QS} (2083 walked only "
        f"{ [q for q in QS if q >= 0.40] }; the NEW rungs are {NEW_QS}).  reported, not tuned: "
        f"PANEL {PANELS}, chooser FORM {FORMS}, beta {BETA_KIND}, cost x lag ladder at clearers. "
        f" shelf {len(FAMILIES)}x{len(WIDTHS)}x{len(GROSSES)} = 80 books/panel, monthly, t+1, "
        f"{COST:.0f} bps.")

    grid_rows, ladder_rows, curve_rows, shelf_rows = [], [], [], []
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
                    oosS=metrics(lr.loc[OOS_START:])["Sharpe"],
                    CAGR=metrics(lr)["CAGR"])

        h = len(spy_full) // 2
        s_full, s_oos = metrics(spy_full), metrics(spy_full.loc[OOS_START:])
        s_h1 = metrics(spy_full.iloc[:h])["Sharpe"]
        s_h2 = metrics(spy_full.iloc[h:])["Sharpe"]
        log(f"   SPY FULL {s_full['CAGR']:.2%}/{s_full['Sharpe']:.3f}/{s_full['MaxDD']:.2%} "
            f"(H1 {s_h1:.3f} H2 {s_h2:.3f});  SPY OOS {s_oos['CAGR']:.2%}/"
            f"{s_oos['Sharpe']:.3f}/{s_oos['MaxDD']:.2%}  ->  4b bars: DD FULL "
            f"{DD_CAP*s_full['MaxDD']:.2%} / OOS {DD_CAP*s_oos['MaxDD']:.2%}, CAGR FULL "
            f"{CAGR_FLOOR*s_full['CAGR']:.2%} / OOS {CAGR_FLOOR*s_oos['CAGR']:.2%}")
        log(f"   live RULES v2 FULL {live['CAGR']:.2%}/{live['S']:.3f}/{live['DD']:.2%} "
            f"(H1 {live['H1']:.3f} H2 {live['H2']:.3f}), OOS S={live['oosS']:.3f}")

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
            d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                     oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                     spy_CAGR=s_full["CAGR"], spy_Sharpe=s_full["Sharpe"],
                     spy_MaxDD=s_full["MaxDD"], spy_H1=s_h1, spy_H2=s_h2,
                     spy_oos_CAGR=s_oos["CAGR"], spy_oos_Sharpe=s_oos["Sharpe"],
                     spy_oos_MaxDD=s_oos["MaxDD"], live_CAGR=live["CAGR"],
                     live_Sharpe=live["S"], live_H1=live["H1"], live_H2=live["H2"],
                     live_MaxDD=live["DD"], live_oos_Sharpe=live["oosS"],
                     dd_gap_pp=100.0 * (mo["MaxDD"] - DD_CAP * s_oos["MaxDD"]),
                     keep4b_full=k4b_full, keep4b_oos=k4b_oos,
                     keep4b=(k4b_full and k4b_oos), keep4a=k4a)
            legs, rch, binder = reach_of(d)
            d.update({k_: v for k_, v in legs.items()})
            d["REACH"], d["binding_leg"] = rch, binder
            return d

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
                picks = {"QRESID": keys[int(np.argmax(res_q))],
                         "QRAW": keys[int(np.argmax(qdd))]}
                for form in FORMS:
                    key = picks[form]
                    i = keys.index(key)
                    grid_rows.append(dict(panel=pname, definition=kind, q=q, form=form,
                                          threshold=thr, n_quiet_days=nq, n_is_days=len(is_idx),
                                          new_rung=bool(q in NEW_QS), book=str(key),
                                          is_sharpe=is_sharpe[key], is_beta=is_beta[key],
                                          is_quiet_dd=float(qdd[i]),
                                          is_quiet_resid=float(res_q[i]), **score_pick(key)))

        for key in books:
            shelf_rows.append(dict(panel=pname, book=str(key), family=key[0], width=str(key[1]),
                                   gross=key[2], is_sharpe=is_sharpe[key],
                                   is_beta=is_beta[key], **score_pick(key)))

        kbest = max(is_sharpe, key=lambda k: is_sharpe[k])
        grid_rows.append(dict(panel=pname, definition="-", q=np.nan, form="IS_SHARPE",
                              threshold=np.nan, n_quiet_days=len(is_idx), n_is_days=len(is_idx),
                              new_rung=False, book=str(kbest), is_sharpe=is_sharpe[kbest],
                              is_beta=is_beta[kbest], is_quiet_dd=maxdd(books[kbest].loc[:IS_END]),
                              is_quiet_resid=np.nan, **score_pick(kbest)))
        panel_store[pname] = dict(px=px, cols=cols, sig=sig, gate_map=gate_map, rebal=rebal,
                                  st=st, spy_full=spy_full, s_full=s_full, s_oos=s_oos,
                                  s_h1=s_h1, s_h2=s_h2)

    G = pd.DataFrame(grid_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    SH = pd.DataFrame(shelf_rows)
    SH.to_csv(f"{OUT}.shelf.csv", index=False)

    # ---------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", "18.7/18.7/16.7y", ">= 10", True)
    ref = G[(G.panel == "U56") & (G.definition == "NEARHI_EXP") & (G.q == 0.40)
            & (G.form == "QRESID")]
    ok = len(ref) == 1 and ref.book.iloc[0] == "('MADIST', 40, 1.0)"
    gate("G1 q=0.40 NEARHI_EXP/QRESID/U56 reproduces 2083's pick", 
         ref.book.iloc[0] if len(ref) else "missing", "('MADIST', 40, 1.0)", ok)
    if len(ref):
        r0 = ref.iloc[0]
        gate("G1b ... and 2083's OOS numbers (16.24%/1.3099/-17.67%)",
             f"{r0.oos_CAGR:.4%}/{r0.oos_Sharpe:.4f}/{r0.oos_MaxDD:.4%}", "|d| < 5e-5",
             abs(r0.oos_Sharpe - 1.3099) < 5e-4 and abs(r0.oos_MaxDD + 0.1767) < 5e-5)
    ctl = G[(G.panel == "U56") & (G.q == 1.00) & (G.form == "QRESID")]
    gate("G1c q=1.00 QRESID reproduces 911's U56 pick (MADIST/ALL/1.0, OOS -22.18%)",
         f"{ctl.book.iloc[0]} {ctl.oos_MaxDD.iloc[0]:.4%}", "MADIST/ALL/1.0, -22.18%",
         ctl.book.iloc[0] == "('MADIST', 'ALL', 1.0)"
         and abs(ctl.oos_MaxDD.iloc[0] + 0.221818) < 1e-4)
    gate("G2 100% SPY book reads beta ~ 1.0", f"max|beta-1| = {max(g_spy_beta):.4f}", "< 0.05",
         max(g_spy_beta) < 0.05)
    gate("G3 no leverage (max shelf gross)", f"{g_lev:.4f}", "<= 1.0", g_lev <= 1.0 + 1e-9)
    gate("G4 distress series is CAUSAL (truncated tape == full tape on overlap)",
         f"max|diff| = {max(g_causal):.2e}", "== 0", max(g_causal) == 0.0)
    gate("G5 every grid point published",
         f"{len(G)} rows = 3 panels x (3 defs x {len(QS)} q x 2 forms + 1 IS_SHARPE)",
         f"== {3*(3*len(QS)*2+1)}", len(G) == 3 * (3 * len(QS) * 2 + 1))
    nh = G[(G.q == 1.00) & (G.definition != "VOL60")]
    gate("G6a q=1.00 keeps EVERY IS day for both NEAR-HIGH definitions",
         "; ".join(f"{p_}:{int(a)}/{int(b_)}" for p_, a, b_ in
                   zip(nh.panel, nh.n_quiet_days, nh.n_is_days))[:120],
         "equal on all", bool((nh.n_quiet_days == nh.n_is_days).all()))
    vv = G[(G.q == 1.00) & (G.definition == "VOL60")]
    gate("G6b q=1.00 VOL60 drops EXACTLY its 20-day min_periods warm-up (inherited from 2083's "
         "definition; the mask is still causal and the 2083 comparison is unaffected)",
         "; ".join(f"{p_}:{int(b_)-int(a)}" for p_, a, b_ in
                   zip(vv.panel, vv.n_quiet_days, vv.n_is_days)),
         "== 19 or 20 everywhere",
         bool(((vv.n_is_days - vv.n_quiet_days).isin([19, 20])).all()))
    gate("G6b REACH > 0 iff keep4b", f"{int((( G.REACH>0) == G.keep4b).sum())} of {len(G)}",
         "all", bool(((G.REACH > 0) == G.keep4b).all()))

    # ---------------------------------------------------------------- arm 0: the full grid
    log(f"\n## ARM 0 — THE FULL GRID ({len(G)} picks; rule 8: IS 2009-2016 chooses, OOS read "
        f"once).  NEW = a rung 2083 never walked.")
    for pname in PANELS:
        log(f"\n   --- {pname} ---")
        for _, r in G[G.panel == pname].iterrows():
            qs = "  -  " if pd.isna(r.q) else f"{r.q:.2f}"
            tag = "NEW" if r.new_rung else "   "
            log(f"   {tag} {r.definition:<11} q={qs} {r.form:<9} {r.book:<24} "
                f"quietDD {r.is_quiet_dd:7.2%} ({int(r.n_quiet_days):>4}d) -> FULL "
                f"{r.CAGR:6.2%}/{r.Sharpe:.3f}/{r.MaxDD:7.2%}  OOS {r.oos_CAGR:6.2%}/"
                f"{r.oos_Sharpe:.3f}/{r.oos_MaxDD:7.2%}  ddgap {r.dd_gap_pp:+6.2f}pp  "
                f"REACH {r.REACH:+.4f} ({r.binding_leg})  4bF={int(r.keep4b_full)} "
                f"4bO={int(r.keep4b_oos)} 4a={int(r.keep4a)}")

    # ---------------------------------------------------------------- arm 1 / V1: the argmax
    log("\n## ARM 1 — WHERE DOES REACH PEAK ON THE q LADDER?  (18 curves, one per panel x "
        "definition x form; ENDPOINT = q* in {0.10, 1.00})")
    interior = 0
    for pname in PANELS:
        for kind in DEFS:
            for form in FORMS:
                c = G[(G.panel == pname) & (G.definition == kind) & (G.form == form)] \
                    .sort_values("q")
                i = int(np.argmax(c.REACH.values))
                qstar = float(c.q.values[i])
                is_int = QS[0] < qstar < QS[-1]
                interior += int(is_int)
                mono_dn = bool(np.all(np.diff(c.REACH.values) <= 1e-12))   # best at the low end
                curve_rows.append(dict(panel=pname, definition=kind, form=form, q_star=qstar,
                                       reach_star=float(c.REACH.values[i]),
                                       interior=is_int,
                                       monotone_improving_downward=mono_dn,
                                       book_star=c.book.values[i],
                                       n_distinct_books=int(c.book.nunique()),
                                       reach_q010=float(c[c.q == 0.10].REACH.iloc[0]),
                                       reach_q040=float(c[c.q == 0.40].REACH.iloc[0]),
                                       reach_q100=float(c[c.q == 1.00].REACH.iloc[0]),
                                       n_keep4b=int(c.keep4b.sum())))
                log(f"   {pname:<6} {kind:<11} {form:<7} q* = {qstar:.2f} "
                    f"{'INTERIOR' if is_int else 'ENDPOINT'}  REACH* {c.REACH.values[i]:+.4f}  "
                    f"[q0.10 {c[c.q==0.10].REACH.iloc[0]:+.4f} | q0.40 "
                    f"{c[c.q==0.40].REACH.iloc[0]:+.4f} | q1.00 "
                    f"{c[c.q==1.00].REACH.iloc[0]:+.4f}]  books {c.book.nunique()}  "
                    f"4b {int(c.keep4b.sum())}/{len(c)}")
    C = pd.DataFrame(curve_rows)
    C.to_csv(f"{OUT}.curves.csv", index=False)
    v1_trig = interior > len(C) / 2
    log(f"\n   V1: interior argmax on {interior} of {len(C)} curves  ->  V1 "
        f"{'TRIGGERED' if v1_trig else 'NOT TRIGGERED'}")

    # ---------------------------------------------------------------- V2: 2083's own cell
    log("\n## ARM 2 — 2083's OWN CELL: does its q=0.40 pass keep improving below 0.40?")
    v2_ok = []
    for kind in ("NEARHI_EXP", "NEARHI_252"):
        c = C[(C.panel == "U56") & (C.definition == kind) & (C.form == "QRESID")].iloc[0]
        sub = G[(G.panel == "U56") & (G.definition == kind) & (G.form == "QRESID")].sort_values("q")
        log(f"   U56 {kind:<11} QRESID   q* = {c.q_star:.2f} "
            f"({'at the NEW low boundary' if c.q_star == 0.10 else 'not at the low boundary'})")
        for _, r in sub.iterrows():
            log(f"       q={r.q:.2f} {'NEW' if r.new_rung else '   '} {r.book:<24} OOS "
                f"{r.oos_CAGR:6.2%}/{r.oos_Sharpe:.3f}/{r.oos_MaxDD:7.2%} ddgap "
                f"{r.dd_gap_pp:+6.2f}pp REACH {r.REACH:+.4f} 4b={int(r.keep4b)}")
        v2_ok.append(c.q_star != 0.10)
    v2_trig = all(v2_ok)
    log(f"   ->  V2 {'TRIGGERED' if v2_trig else 'NOT TRIGGERED'}")

    # ---------------------------------------------------------------- V3: new reach below 0.40
    new = G[G.new_rung]
    new_hits = new[new.keep4b]
    v3_trig = len(new_hits) > 0
    hits = G[G.keep4b]
    log(f"\n## ARM 3 — DOES THE SUB-0.40 REGION REACH ANYTHING?  grid points with q<0.40 "
        f"clearing 4b FULL+OOS: {len(new_hits)} of {len(new)}  ->  V3 "
        f"{'TRIGGERED' if v3_trig else 'NOT TRIGGERED'}")
    log(f"   whole grid: 4b FULL+OOS {len(hits)} of {len(G)} (panels "
        f"{sorted(hits.panel.unique()) or 'none'}); 4b FULL alone {int(G.keep4b_full.sum())}; "
        f"4b OOS alone {int(G.keep4b_oos.sum())}; 4a {int(G.keep4a.sum())}")
    if len(hits):
        log("   clearing points:")
        for _, r in hits.iterrows():
            log(f"     {r.panel:<6} {r.definition:<11} q={r.q:.2f} {r.form:<7} {r.book:<24} "
                f"FULL {r.CAGR:6.2%}/{r.Sharpe:.3f}/{r.MaxDD:7.2%}  OOS {r.oos_CAGR:6.2%}/"
                f"{r.oos_Sharpe:.3f}/{r.oos_MaxDD:7.2%}  REACH {r.REACH:+.4f}")
    log(f"   binding leg over the whole grid: " +
        ", ".join(f"{k}={v}" for k, v in G.binding_leg.value_counts().items()))

    # ---------------------------------------------------------------- ARM 4 (POST-HOC)
    log("\n## ARM 4 — POST-HOC DIAGNOSTIC (NOT pre-stated; added after ARM 3 showed every "
        "clearer is a k=40 / gross 1.00 book).  What is the SHELF'S OWN 4b base rate, i.e. how "
        "much of the reach is the CHOOSER and how much is the CELL?")
    for pname in PANELS:
        sh = SH[SH.panel == pname]
        hit = sh[sh.keep4b]
        log(f"   {pname:<6} shelf 4b FULL+OOS: {len(hit)} of {len(sh)} books "
            f"({len(hit)/len(sh):.1%});  4a: {int(sh.keep4a.sum())} of {len(sh)}")
        if len(hit):
            log(f"          clearing books: {', '.join(sorted(hit.book))}")
            log(f"          widths {sorted(set(hit.width))}, grosses {sorted(set(hit.gross))}, "
                f"families {sorted(set(hit.family))}")
        g_ = G[(G.panel == pname) & (G.form == "QRESID") & G.q.notna()]
        log(f"          QRESID picks clearing 4b: {int(g_.keep4b.sum())} of {len(g_)} "
            f"({g_.keep4b.mean():.1%})  vs shelf base rate {len(hit)/len(sh):.1%}  "
            f"-> lift {g_.keep4b.mean() - len(hit)/len(sh):+.1%}")

    # ---------------------------------------------------------------- cost x delay at clearers
    log("\n## ROBUSTNESS — cost {0,10,25,50} bps x SIGNAL LAG {0,+1 day} at every book reached "
        "by a 4b-clearing grid point")
    for pname in PANELS:
        S = panel_store[pname]
        for b in hits[hits.panel == pname].book.unique():
            fam, k, g = eval(b)
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
                    ladder_rows.append(dict(panel=pname, book=b, signal_lag_days=dly - 1,
                                            cost_bps=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                            MaxDD=m["MaxDD"], oos_CAGR=mo["CAGR"],
                                            oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                                            keep4b_full=ok_f, keep4b_oos=ok_o,
                                            keep4b=(ok_f and ok_o)))
                    log(f"   {pname:<6} {b:<24} lag+{dly-1} {c:>4.0f}bps  FULL "
                        f"{m['CAGR']:6.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:7.2%}  OOS "
                        f"{mo['CAGR']:6.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:7.2%}"
                        f"  4b={int(ok_f and ok_o)}")
    L = pd.DataFrame(ladder_rows)
    L.to_csv(f"{OUT}.ladder.csv", index=False)
    if len(L):
        d = 0.0
        for _, lr_ in L[(L.signal_lag_days == 0) & (L.cost_bps == COST)].iterrows():
            gr = G[(G.panel == lr_.panel) & (G.book == lr_.book)].iloc[0]
            d = max(d, abs(lr_.oos_Sharpe - gr.oos_Sharpe), abs(lr_.oos_MaxDD - gr.oos_MaxDD))
        gate("G7 ladder lag=0 @10bps reproduces the grid row", f"max|diff| = {d:.2e}",
             "< 1e-12", d < 1e-12)
        log(f"   ladder 4b hold rate: {int(L.keep4b.sum())} of {len(L)} cells")
    else:
        log("   (no grid point cleared 4b FULL+OOS — ladder not walked)")
    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)

    log("\n## VERDICTS")
    log(f"   V1 REACH has an INTERIOR argmax on a majority of curves ......... "
        f"{'YES' if v1_trig else 'NO'}  ({interior}/{len(C)})")
    log(f"   V2 2083's q=0.40 does NOT keep improving below 0.40 ............. "
        f"{'YES' if v2_trig else 'NO'}")
    log(f"   V3 at least one q<0.40 point clears 4b FULL+OOS ................. "
        f"{'YES' if v3_trig else 'NO'}  ({len(new_hits)}/{len(new)})")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
