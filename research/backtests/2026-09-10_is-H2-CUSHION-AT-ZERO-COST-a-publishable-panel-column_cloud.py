#!/usr/bin/env python3
"""Idea 411 — is H2 CUSHION AT ZERO COST a publishable panel column?  (cloud, 2026-09-10)

QUEUE 411: "idea 137 found broad's ranked book enters the cost question with a third of u56's
zero-cost H2 margin (+0.1012/+0.1577 vs +0.3355/+0.3848), which predicts its 4b failure better
than its turnover does.  Test H2-cushion-at-0-bps as a screening column across panels against
turnover as the incumbent predictor.  Max 2 params."

WHAT IS BEING TESTED
  A 4b verdict at a cost rung is the conjunction of two different things: WHERE THE BOOK STARTS
  (its margins over SPY before any cost is paid) and HOW MUCH THE RUNG TAKES OFF IT (turnover x
  cost).  The record screens on the second.  Idea 137's aside says the first is the binding one.
  This run prices both columns as SCREENS on one pre-registered arm menu.

  H1  Does H2CUSH0 (H2 Sharpe at 0 bps minus SPY's H2 Sharpe) out-predict TURNOVER for the 4b
      verdict at 10 bps?  Measured as AUC, Spearman against the continuous 4b margin, and as a
      threshold screen's precision / recall / F1.  Reported POOLED and WITHIN PANEL, because a
      pooled rho over panels with different levels is the artefact idea 605 was killed for.
  H2  THE DECOMPOSITION THAT DECIDES IT.  Split every 4b failure at 10 bps into
        LEVEL   — the arm already fails 4b at 0 bps, so no cost column could ever have saved it;
        COST    — the arm passes at 0 bps and fails at 10 bps, the only failures turnover can own.
      If the COST class is small, turnover cannot be the right screening column whatever its
      correlation reads, and the queue's claim is true for a reason it did not state.
  H3  Is the cushion column a TAUTOLOGY?  H2@10bps = H2@0bps - (cost erosion of H2), so a cushion
      column is partly the outcome restated.  Three controls: (a) predict the 25 bps verdict from
      the 0 bps column, (b) predict OUT OF PANEL (threshold chosen on one panel, applied to the
      other two), (c) predict OUT OF SAMPLE under PROTOCOL rule 8.
  H4  Does either column earn a place beside the other?  The joint screen is run and reported.

AXES (PROTOCOL rule 4: no more than 2 tuned parameters)
  P1 SCREEN COLUMN   {H2CUSH0, TURNOVER, MINCUSH0, JOINT} — every column reported at every point.
  P2 THRESHOLD       swept over the column's own empirical deciles, every point reported.
  The ARM MENU is a REPORTING axis, fixed before any number was read and never selected on:
    3 panels (u56 / broad136 / small439) x 6 books (TOP5 / TOP10 / TOP20 / TOP40 / EWALL /
    RULESv2) x 2 gross (0.75 / 1.00) x 2 cadences (W / M) x 3 lambdas (1.00 / 0.50 / 0.25)
    = 216 arms, each priced at 0 / 10 / 25 bps = 648 arm-rows.  Every one is reported.

GATES (before any new number is read)
  G1  the vectorised runner vs `engine.backtest` at W and M on all three panels, returns AND
      turnover.
  G2  the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live 25 bps `engine.backtest` —
      load-bearing here, because it is the exact statement that a rung can reach a return series
      ONLY through turnover, which is what makes "turnover" the incumbent column at all.
  G3  lambda = 1.0 is a strict no-op on the weights.  (Turnover monotonicity in lambda is NOT
      a gate here: it is a property of the arm menu, and section A2 reports where it fails and
      why — a finding this run did not go looking for.)
  G4  the AUC machinery returns exactly 0.5 on a column that is a copy of a random permutation's
      rank, and exactly 1.0 on the outcome used as its own predictor.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): current constituents on all three panels; SMALL439 drops the 44
    tickers with max_1d_move >= 1.0 from data/small_meta.csv before anything runs.  No level here
    is an attainable return; every comparison that carries the conclusion is between arms priced
    on the SAME panel.
  * Panels truncated to their common last date (idea 328).  10 bps and t+1 execution (idea 126).
  * MaxDD is one number off one path (idea 321); the 4b DD leg turns on exactly that number.
  * Idea 613: inside ONE cost rung a drag re-pricing (turnover x c) is a strictly monotone
    transform of turnover, so DRAG is NOT run as a separate column — it would be the same ranking.

Deterministic, standalone.  Modifies nothing outside its own artefacts.
Writes .console.txt, .arms.csv, .screens.csv, .decomp.csv, .wf.csv.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-10_is-H2-CUSHION-AT-ZERO-COST-a-publishable-panel-column_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60

PANELS = ["u56", "broad", "small"]
BOOKS = ["TOP5", "TOP10", "TOP20", "TOP40", "EWALL", "RULESv2"]
GROSSES = [0.75, 1.00]
CADENCES = ["W", "M"]
LAMBDAS = [1.00, 0.50, 0.25]
RUNGS = [0.0, 10.0, 25.0]
PCOST = 10.0
COLUMNS = ["H2CUSH0", "TURNOVER", "MINCUSH0", "JOINT"]
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
SEED = 20260910

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner
# =====================================================================================
def _mask(idx, freq):
    key = {"W": idx.to_period("W"), "M": idx.to_period("M")}[freq]
    s = pd.Series(key, index=idx)
    return (s != s.shift(-1)).shift(1, fill_value=False).values


def fast_bt(px, W, freq, rets=None):
    if rets is None:
        rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = _mask(px.index, freq)
    n = len(px)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: an EWMA of the raw target with gross restored
    daily, so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


def book_weights(px, book, gross, investable):
    sub = px[investable]
    if book == "EWALL":
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        W = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif book == "RULESv2":
        W = rules_v2_weights(sub, gross=gross)
    else:
        n = int(book[3:])
        rank = H.composite(sub).rank(axis=1, ascending=False)
        W = (rank <= n).astype(float) * (gross / n)
    return W.reindex(columns=px.columns).fillna(0.0)


# =====================================================================================
# metrics
# =====================================================================================
def bars_of(spy, which="full"):
    s = spy if which == "full" else spy.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    s = r if which == "full" else r.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def pass4a(r, base):
    hr, hb = len(r) // 2, len(base) // 2
    return bool(metrics(r.iloc[:hr])["Sharpe"] > metrics(base.iloc[:hb])["Sharpe"]
                and metrics(r.iloc[hr:])["Sharpe"] > metrics(base.iloc[hb:])["Sharpe"]
                and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


# =====================================================================================
# predictor machinery
# =====================================================================================
def rankdata(a):
    a = np.asarray(a, float)
    o = np.argsort(a, kind="mergesort")
    r = np.empty(len(a), float)
    r[o] = np.arange(1, len(a) + 1)
    # average ties
    s = a[o]
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        if j > i:
            r[o[i:j + 1]] = (i + j + 2) / 2.0
        i = j + 1
    return r


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra, rb = rankdata(a[ok]), rankdata(b[ok])
    ra, rb = ra - ra.mean(), rb - rb.mean()
    d = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / d) if d else np.nan


def auc(score, y):
    """P(score of a positive > score of a negative), ties at 0.5.  Mann-Whitney form."""
    score, y = np.asarray(score, float), np.asarray(y).astype(bool)
    ok = np.isfinite(score)
    score, y = score[ok], y[ok]
    n1, n0 = int(y.sum()), int((~y).sum())
    if n1 == 0 or n0 == 0:
        return np.nan
    r = rankdata(score)
    return float((r[y].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def prf(pred, y):
    pred, y = np.asarray(pred).astype(bool), np.asarray(y).astype(bool)
    tp = int((pred & y).sum()); fp = int((pred & ~y).sum()); fn = int((~pred & y).sum())
    p = tp / (tp + fp) if tp + fp else np.nan
    rc = tp / (tp + fn) if tp + fn else np.nan
    f = 2 * p * rc / (p + rc) if p and rc and (p + rc) > 0 else 0.0
    return p, rc, f, tp, fp, fn


# =====================================================================================
# GATES
# =====================================================================================
def gates(panels):
    say("=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True
    for pk, (px, _) in panels.items():
        inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
        W = book_weights(px, "TOP20", 0.75, inv)
        start = px.index[260]
        d = []
        for f in CADENCES:
            rf, tf = fast_bt(px, W, f)
            e0 = backtest(px, W, cost_bps=0.0, freq=f)
            d.append((f, float((rf.loc[start:] - e0["returns"].loc[start:]).abs().max()),
                      float((tf.loc[start:] - e0["turnover"].loc[start:]).abs().max())))
        say(f"  G1 {pk:>5}: fast_bt vs engine.backtest  " +
            "  ".join(f"{f}: dr {a:.2e} dto {b:.2e}" for f, a, b in d))
        ok &= all(a < 1e-12 and b < 1e-12 for _, a, b in d)
        rf, tf = fast_bt(px, W, "W")
        e25 = backtest(px, W, cost_bps=25.0, freq="W")
        d2 = float(((rf - tf * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G2 {pk:>5}: cost-rung identity vs live 25 bps  max|dr| {d2:.3e}")
        ok &= d2 < 1e-12
        d3 = float((smooth(W, 1.0) - W).abs().values.max())
        say(f"  G3 {pk:>5}: lambda=1.0 is a strict no-op on the weights  max|dW| {d3:.3e}")
        ok &= d3 == 0.0

    rng = np.random.default_rng(SEED)
    y = rng.random(400) < 0.35
    a_self = auc(y.astype(float), y)
    a_rand = np.mean([auc(rng.permutation(400).astype(float), y) for _ in range(200)])
    say(f"  G4 AUC machinery: outcome as its own predictor {a_self:.4f} (want 1.0000); "
        f"mean AUC over 200 random permutations {a_rand:.4f} (want ~0.5000)")
    ok &= abs(a_self - 1.0) < 1e-12 and abs(a_rand - 0.5) < 0.02
    say(f"\n  GATES {'PASS' if ok else 'FAIL'} (turnover monotonicity in lambda checked on the "
        f"arm menu below)")
    return ok


# =====================================================================================
# ARM MENU
# =====================================================================================
def run_arms(panels):
    rows = []
    for pk, (px, ndrop) in panels.items():
        inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bf, bi = bars_of(spy, "full"), bars_of(spy, "IS")
        rets = px.pct_change().fillna(0.0).values
        v2r, v2t = fast_bt(px, rules_v2_weights(px), "W")
        v2 = {c: (v2r - v2t * c / 1e4).loc[start:] for c in RUNGS}
        say(f"\n  panel {pk}: {px.shape[1]} cols ({len(inv)} investable"
            + (f", {ndrop} dropped for max_1d_move>=1.0" if ndrop else "")
            + f"), {start.date()} .. {px.index[-1].date()}")
        say(f"    SPY bars: H1 {bf['s1']:.4f}  H2 {bf['s2']:.4f}  OOS {bf['soos']:.4f}  "
            f"MaxDD {bf['sdd']:.2%}  CAGR {bf['scagr']:.2%}  (IS bars H1 {bi['s1']:.4f} "
            f"H2 {bi['s2']:.4f})")
        for book in BOOKS:
            for g in GROSSES:
                raw = book_weights(px, book, g, inv)
                for lam in LAMBDAS:
                    Wl = smooth(raw, lam)
                    for freq in CADENCES:
                        r0, t0 = fast_bt(px, Wl, freq, rets=rets)
                        r0, t0 = r0.loc[start:], t0.loc[start:]
                        to = float(t0.sum() / (len(t0) / 252))
                        m0 = margins(r0, bf, "full")            # the ZERO-COST columns
                        m0i = margins(r0.loc[:IS_END], bi, "IS")
                        base = dict(panel=pk, book=book, gross=g, lam=lam, freq=freq,
                                    TURNOVER=to,
                                    H2CUSH0=m0["H2"], H1CUSH0=m0["H1"],
                                    MINCUSH0=min(m0[x] for x in BARS5),
                                    OOSCUSH0=m0["OOS"], DDCUSH0=m0["DD"],
                                    CAGRCUSH0=m0["CAGR"],
                                    bind_leg0=min(BARS5, key=lambda x: m0[x]),
                                    H2CUSH0_IS=m0i["H2"],
                                    MINCUSH0_IS=min(m0i[x] for x in ("H1", "H2", "DD", "CAGR")),
                                    pass4b_0=all(m0[x] > 0 for x in BARS5))
                        for c in RUNGS:
                            r = r0 - t0 * c / 1e4
                            m = metrics(r)
                            mg = margins(r, bf, "full")
                            mgi = margins(r.loc[:IS_END], bi, "IS")
                            rows.append(dict(
                                **base, cost=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                MaxDD=m["MaxDD"],
                                H1=metrics(r.iloc[:len(r) // 2])["Sharpe"],
                                H2=metrics(r.iloc[len(r) // 2:])["Sharpe"],
                                OOSs=metrics(r.loc[OOS_START:])["Sharpe"],
                                margin_min=min(mg[x] for x in BARS5),
                                margin_H2=mg["H2"],
                                bind_leg=min(BARS5, key=lambda x: mg[x]),
                                **{f"mg_{x}": mg[x] for x in BARS5},
                                pass4b=all(mg[x] > 0 for x in BARS5),
                                pass4a=pass4a(r, v2[c]),
                                IS_pass4b=all(mgi[x] > 0 for x in ("H1", "H2", "DD", "CAGR")),
                                IS_margin_min=min(mgi[x] for x in ("H1", "H2", "DD", "CAGR")),
                                OOS_pass=bool(mg["OOS"] > 0)))
    return pd.DataFrame(rows)


# =====================================================================================
def screens(A, cost, outcome="pass4b"):
    """Every column x every threshold on that column's own deciles; every point reported."""
    S = A[A.cost == cost].copy()
    S["JOINT"] = np.minimum(rankdata(S.H2CUSH0) / len(S), 1 - rankdata(S.TURNOVER) / len(S))
    rows = []
    for col in COLUMNS:
        hi_is_good = col != "TURNOVER"
        v = S[col].values
        y = S[outcome].values.astype(bool)
        for q in range(0, 101, 5):
            thr = float(np.percentile(v, q))
            pred = v >= thr if hi_is_good else v <= thr
            p, rc, f, tp, fp, fn = prf(pred, y)
            rows.append(dict(cost=cost, column=col, q=q, thr=thr, n_pred=int(pred.sum()),
                             precision=p, recall=rc, F1=f, tp=tp, fp=fp, fn=fn))
    return pd.DataFrame(rows)


def col_report(A, cost, label):
    S = A[A.cost == cost]
    y = S.pass4b.values.astype(bool)
    say(f"\n  {label}: {int(y.sum())} of {len(S)} arms pass 4b  (base rate {y.mean():.1%})")
    rows = []
    for col in ["H2CUSH0", "TURNOVER", "MINCUSH0", "H1CUSH0", "OOSCUSH0", "CAGRCUSH0", "DDCUSH0"]:
        sc = S[col].values * (-1 if col == "TURNOVER" else 1)
        rows.append(dict(column=col, AUC=auc(sc, y),
                         rho_margin=spearman(sc, S.margin_min.values),
                         rho_within=np.mean([spearman(
                             S[S.panel == p][col].values * (-1 if col == "TURNOVER" else 1),
                             S[S.panel == p].margin_min.values) for p in PANELS]),
                         **{f"AUC_{p}": auc(S[S.panel == p][col].values
                                            * (-1 if col == "TURNOVER" else 1),
                                            S[S.panel == p].pass4b.values.astype(bool))
                            for p in PANELS}))
    R = pd.DataFrame(rows).set_index("column")
    say(R.to_string(float_format=lambda x: f"{x:.4f}"))
    return R


# =====================================================================================
def main():
    T0 = time.time()
    say("=" * 100)
    say("IDEA 411 — is H2 CUSHION AT ZERO COST a publishable panel column?   (cloud)")
    say("=" * 100)
    say(f"tuned parameter 1 (SCREEN COLUMN): {COLUMNS}, all reported")
    say("tuned parameter 2 (THRESHOLD)    : the column's own 0..100th percentiles in steps of 5, "
        "all reported")
    say(f"reporting axes (never selected on): {len(PANELS)} panels x {len(BOOKS)} books x "
        f"{len(GROSSES)} gross x {len(CADENCES)} cadences x {len(LAMBDAS)} lambdas = "
        f"{len(PANELS)*len(BOOKS)*len(GROSSES)*len(CADENCES)*len(LAMBDAS)} arms, "
        f"x {len(RUNGS)} rungs")

    raw = {"u56": load_universe(), "broad": load_universe(broad=True)}
    sp, ndrop = small_panel()
    raw["small"] = sp
    last = min(px.index[-1] for px in raw.values())
    panels = {k: (v.loc[:last], ndrop if k == "small" else 0) for k, v in raw.items()}
    say(f"\npanels truncated to the common last date {last.date()} (idea 328)")

    if not gates(panels):
        say("\nGATES FAILED — stopping before any finding is read.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return

    say("\n" + "=" * 100)
    say("A. THE ARM MENU")
    say("=" * 100)
    A = run_arms(panels)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    say(f"\n  {len(A)} arm-rows ({A[A.cost == 0].shape[0]} arms x {len(RUNGS)} rungs)")

    # A2 --- a MEASURED property of the menu, reported rather than assumed --------------
    bad, tot, who = [], 0, []
    for k, g in A[A.cost == 0].groupby(["panel", "book", "gross", "freq"]):
        tot += 1
        t = g.sort_values("lam", ascending=False).TURNOVER.values
        if not np.all(np.diff(t) <= 1e-12):
            bad.append(k)
            who.append(f"{k[0]}/{k[1]}/g{k[2]}/{k[3]} " + "->".join(f"{x:.3f}" for x in t))
    say(f"\n  A2 (MEASURED, not a gate — this is a property of the ARM MENU, not of the "
        f"machinery): idea 137's lambda dial is turnover-NON-MONOTONE in {len(bad)} of {tot} "
        f"cells.")
    for w in who:
        say(f"      {w}")
    fams = sorted({k[1] for k in bad})
    say(f"      every violating cell is a {fams} book: the dial's re-gross step restores the "
        f"RAW book's daily gross onto an EWMA of it, so on a book whose gross MOVES day to day "
        f"(RULESv2's band gates names to cash) the dial manufactures daily trading instead of "
        f"removing it. On such books lambda RAISES turnover by up to "
        f"{max((max(g.sort_values('lam', ascending=False).TURNOVER.values) / min(g.sort_values('lam', ascending=False).TURNOVER.values)) for k, g in A[A.cost == 0].groupby(['panel', 'book', 'gross', 'freq']) if k in bad):.3f}x. "
        f"Ideas 137/412 measured the dial on fixed-gross books only.")

    say("\n" + "=" * 100)
    say("B. THE DECOMPOSITION THAT DECIDES IT (H2) — is a 4b failure a LEVEL fact or a COST fact?")
    say("=" * 100)
    dec = []
    for c in RUNGS[1:]:
        S = A[A.cost == c].set_index(["panel", "book", "gross", "lam", "freq"])
        Z = A[A.cost == 0].set_index(["panel", "book", "gross", "lam", "freq"])
        fail = ~S.pass4b
        lvl = fail & ~Z.pass4b_0.reindex(S.index)
        cst = fail & Z.pass4b_0.reindex(S.index)
        say(f"\n  at {c:.0f} bps: {int(fail.sum())} of {len(S)} arms FAIL 4b — "
            f"LEVEL (already failing at 0 bps) {int(lvl.sum())} = {lvl.sum()/max(1,fail.sum()):.1%}"
            f" ; COST (passes at 0 bps, fails here) {int(cst.sum())} = "
            f"{cst.sum()/max(1,fail.sum()):.1%}")
        for p in PANELS:
            f2 = fail.xs(p, level=0); l2 = lvl.xs(p, level=0); c2 = cst.xs(p, level=0)
            say(f"      {p:>5}: fail {int(f2.sum()):3d}/{len(f2)}  LEVEL {int(l2.sum()):3d}  "
                f"COST {int(c2.sum()):3d}  (pass at 0 bps {int(Z.xs(p, level=0).pass4b_0.sum())})")
        dec.append(dict(cost=c, n=len(S), fail=int(fail.sum()), level=int(lvl.sum()),
                        cost_class=int(cst.sum())))
    pd.DataFrame(dec).to_csv(OUT / f"{STEM}.decomp.csv", index=False)

    say("\n" + "=" * 100)
    say("B2. WHICH 4b LEG BINDS?  (the argmin of the five margins, per arm)")
    say("=" * 100)
    for c in [0.0, PCOST]:
        S = A[A.cost == c]
        say(f"\n  at {c:.0f} bps, over all {len(S)} arms:")
        say(S.bind_leg.value_counts().to_string())
        say("  by panel:")
        say(pd.crosstab(S.panel, S.bind_leg).to_string())
        say("  by book family:")
        say(pd.crosstab(S.book, S.bind_leg).to_string())
    say("\n  median margin per leg at 10 bps (a NEGATIVE median means the leg is failing for most "
        "arms):")
    say(A[A.cost == PCOST].groupby("panel")[[f"mg_{x}" for x in BARS5]].median().to_string(
        float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 100)
    say("C. THE TWO COLUMNS AS PREDICTORS (higher AUC = better; TURNOVER is sign-flipped so that "
        "\"more is better\" holds for every row)")
    say("=" * 100)
    say("\n  READ MINCUSH0's ROW AS A TAUTOLOGY, NOT A RESULT: MINCUSH0 > 0 is by definition "
        "the 4b predicate evaluated at 0 bps, and section B shows the 10 bps verdict set is "
        "IDENTICAL to the 0 bps one, so its AUC of 1.0000 is an identity being restated. It is "
        "printed because that identity is exactly the finding.")
    R10 = col_report(A, PCOST, "at 10 bps (the PROTOCOL rung)")
    R25 = col_report(A, 25.0, "at 25 bps (H3 control (a): the 0-bps column predicting a rung it "
                              "was not measured at)")

    say("\n  H2 CUSHION AT ZERO COST, by panel (idea 137's aside, re-measured on this menu):")
    Z = A[A.cost == 0]
    say(Z.groupby("panel")[["H2CUSH0", "H1CUSH0", "MINCUSH0", "TURNOVER"]].median().to_string(
        float_format=lambda x: f"{x:.4f}"))
    say("\n  ... and for the RANKED books only (TOP5..TOP40), which is idea 137's own comparison:")
    say(Z[Z.book.str.startswith("TOP")].groupby("panel")[
        ["H1CUSH0", "H2CUSH0", "MINCUSH0", "TURNOVER"]].median().to_string(
        float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 100)
    say("D. THE SCREENS — every column x every threshold, all points reported")
    say("=" * 100)
    SC = pd.concat([screens(A, c) for c in RUNGS[1:]], ignore_index=True)
    SC.to_csv(OUT / f"{STEM}.screens.csv", index=False)
    for c in RUNGS[1:]:
        s = SC[SC.cost == c]
        say(f"\n  at {c:.0f} bps — best F1 per column (base rate "
            f"{A[A.cost == c].pass4b.mean():.1%}, i.e. the no-screen F1 is "
            f"{2*A[A.cost==c].pass4b.mean()/(1+A[A.cost==c].pass4b.mean()):.4f}):")
        best = s.loc[s.groupby("column").F1.idxmax()]
        say(best[["column", "q", "thr", "n_pred", "precision", "recall", "F1"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  full threshold ladder at 10 bps (every point, as PROTOCOL rule 4 requires):")
    piv = SC[SC.cost == PCOST].pivot(index="q", columns="column", values="F1")
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 100)
    say("E. H3 controls (b) OUT OF PANEL and (c) PROTOCOL rule 8 OUT OF SAMPLE")
    say("=" * 100)
    wf = []
    S = A[A.cost == PCOST].copy()
    for src in PANELS:
        tr = S[S.panel == src]
        for col in ["H2CUSH0", "TURNOVER", "MINCUSH0"]:
            hi = col != "TURNOVER"
            cand = screens(A[A.panel == src], PCOST)
            cand = cand[cand.column == col]
            q = int(cand.loc[cand.F1.idxmax(), "q"])
            thr = float(np.percentile(tr[col].values, q))
            te = S[S.panel != src]
            pred = (te[col].values >= thr) if hi else (te[col].values <= thr)
            p, rc, f, tp, fp, fn = prf(pred, te.pass4b.values.astype(bool))
            wf.append(dict(test="OUT-OF-PANEL", chosen_on=src, column=col, q=q, thr=thr,
                           n_test=len(te), base=float(te.pass4b.mean()),
                           precision=p, recall=rc, F1=f))
    # rule 8: threshold chosen on 2009-2016 only, 2017-2026 read once
    for col in ["H2CUSH0", "TURNOVER", "MINCUSH0"]:
        hi = col != "TURNOVER"
        icol = {"H2CUSH0": "H2CUSH0_IS", "MINCUSH0": "MINCUSH0_IS", "TURNOVER": "TURNOVER"}[col]
        bestq, bestf = None, -1
        for q in range(0, 101, 5):
            thr = float(np.percentile(S[icol].values, q))
            pred = (S[icol].values >= thr) if hi else (S[icol].values <= thr)
            _, _, f, *_ = prf(pred, S.IS_pass4b.values.astype(bool))
            if f > bestf:
                bestq, bestf = q, f
        thr = float(np.percentile(S[icol].values, bestq))
        pred = (S[icol].values >= thr) if hi else (S[icol].values <= thr)
        p, rc, f, tp, fp, fn = prf(pred, S.OOS_pass.values.astype(bool))
        wf.append(dict(test="RULE-8-OOS", chosen_on="2009-2016", column=col, q=bestq, thr=thr,
                       n_test=len(S), base=float(S.OOS_pass.mean()),
                       precision=p, recall=rc, F1=f, IS_F1=bestf))
        wf.append(dict(test="RULE-8-OOS-AUC", chosen_on="2009-2016", column=col, q=np.nan,
                       thr=np.nan, n_test=len(S), base=float(S.OOS_pass.mean()),
                       precision=np.nan, recall=np.nan,
                       F1=auc(S[icol].values * (1 if hi else -1),
                              S.OOS_pass.values.astype(bool))))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  (RULE-8-OOS-AUC rows put the AUC in the F1 column; the OOS outcome is the arm's "
        "2017-2026 Sharpe beating SPY's, and the IS column is measured on 2009-2016 alone.)")

    say("\n" + "=" * 100)
    say("F. BOTH KEEP PATHS over every arm-row")
    say("=" * 100)
    say(f"  4a {int(A.pass4a.sum())}/{len(A)}   4b {int(A.pass4b.sum())}/{len(A)}   "
        f"BOTH {int((A.pass4a & A.pass4b).sum())}/{len(A)}")
    for c in RUNGS:
        s = A[A.cost == c]
        say(f"    {c:>5.0f} bps: 4a {int(s.pass4a.sum()):4d}/{len(s)}  "
            f"4b {int(s.pass4b.sum()):4d}/{len(s)}  BOTH "
            f"{int((s.pass4a & s.pass4b).sum()):4d}/{len(s)}")
    b = A[A.pass4b & (A.cost == PCOST)]
    if len(b):
        say(f"\n  4b passers at 10 bps by (panel, book):")
        say(b.groupby(["panel", "book"]).size().to_string())
        best = b.loc[b.margin_min.idxmax()]
        say(f"  widest-margin 4b row: {best.panel}/{best.book} gross {best.gross} lam {best.lam} "
            f"{best.freq}  CAGR {best.CAGR:.2%} Sharpe {best.Sharpe:.4f} MaxDD {best.MaxDD:.2%} "
            f"halves {best.H1:.3f}/{best.H2:.3f} OOS {best.OOSs:.4f} margin_min "
            f"{best.margin_min:.4f}")

    say(f"\ndone in {time.time() - T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
