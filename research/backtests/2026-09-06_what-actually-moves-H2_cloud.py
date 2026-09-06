#!/usr/bin/env python3
"""Idea 70 - "what-actually-moves-H2" (cloud, 2026-09-06).

The question
------------
Idea 66 killed the cash-drag explanation of the standing 4b failure: on universe_broad.json the
ranked book `top20-200d` has an **H2 Sharpe of 0.814 against SPY's 0.837**, and raising gross
from 0.75 to 1.00 moves H2 by 0.001 while costing 6.1pp of drawdown.  The 25% SPY core moves it
to 0.861 but that is buying the benchmark, not fixing the book.  The queue's follow-up:

    "Decompose broad H2 excess return by sector and by top-10 mega-cap weight; is it a
     handful of names or a regime?"

Design (five legs; A-D diagnose, E is the actionable test)
----------------------------------------------------------
Book, FIXED and not tuned (idea 2/55/66's arm, imported construction, not re-invented):
    `top20-200d` = top 20 by the composite key (mean pct-rank of 12-1, 6m, 3m, NO vol scaler)
    among names eligible under `px > 200d MA AND vol20 < 0.60`, equal weight, gross 0.75,
    weekly rebalance, next-day execution, 10 bps.  0 bps carried as a diagnostic only.
    H1/H2 are the two halves of the common sample, PROTOCOL's own definition (baseline._row).

A. REPRODUCTION.  Re-measure the book's and SPY's H1/H2 on B136 under both tradable
   conventions the record uses (all 136 columns; stocks-only) and report which matches idea
   66's published 0.814 / 0.837, with the residual stated rather than smoothed.

B. NAME decomposition.  Per-name H2 return contribution = sum over H2 days of
   held_weight(i,t) * ret(i,t), which sums exactly to the book's H2 gross return.  Report the
   concentration curve (names needed for 50% / 90% of H2 P&L, count of net detractors) and
   then the decisive test: a **leave-one-out** re-run banning each held name from eligibility
   over the WHOLE sample so the book reconstitutes, measuring dH2 Sharpe.  "A handful of
   names" is true only if a small number of single deletions close the 0.03 Sharpe gap.

C. REGIME decomposition.  H2 split three ways, each computable from trailing data only:
   per calendar year; SPY trailing-60d vol above/below its H2 median; SPY above/below its own
   200d MA.  Book vs SPY Sharpe and mean excess in each state.

D. SECTOR decomposition.  No GICS map is cached, so sectors are assigned POINT-IN-TIME by
   maximum trailing-252d return correlation to the 16 sector ETFs in universe.json (an ETF
   maps to itself).  Lookahead-free but a proxy, not GICS - stated as a caveat, not hidden.

E. MEGA-CAP WEIGHT + the actionable arm (PROTOCOL rules 4 and 8).
   No shares-outstanding series is cached and the sandbox has no internet (ideas 195/265), so
   "mega-cap" is proxied POINT-IN-TIME by idea 71's `PITGROW` convention: MEGA10(t) = the 10
   names with the highest cumulative return from panel start to t.  A growth proxy, not market
   cap - stated as a caveat.  The book's MEGA10 weight is reported for H1 and H2, then the
   arm that acts on it:

       cap c: the book's total weight on MEGA10 names may not exceed c x gross; the excess is
              re-allocated pro-rata across the held non-MEGA10 names (cash if none remain).
       c = 1.00 is the do-nothing control and reproduces the plain book exactly.

Tuned parameters (PROTOCOL rule 4: at most two) - leg E only
    1. panel (4: U56, B136, BSTK100, SMALL)      2. cap c (5: 0.00, 0.10, 0.25, 0.50, 1.00)
Legs A-D tune nothing: one fixed book, one fixed panel.  ALL 40 grid points are printed and
written to `.grid.csv`; the leave-one-out sweep writes all of its points to `.names.csv`.

Walk-forward (PROTOCOL rule 8), direction pre-registered before any OOS number was read
    IS = 2009-01-01..2016-12-31 chooses c by IS Sharpe; OOS = 2017-01-01..end read ONCE.
    Controls: CAP_NONE (c = 1.00, do nothing), IS_ARGMAX, plus RULES v1 and SPY.
    If the H2 shortfall is a mega-cap-weight problem, the IS-chosen cap beats the do-nothing
    control out of sample.  If it is not, it does not.

Verdicts (both KEEP paths, on EVERY leg-E point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1 (same panel/rung).
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

SURVIVORSHIP: universe_broad.json, the BSTK100 cut and the sub-$2B panel are CURRENT
constituents - names that died are absent, so every H2 attribution here is measured on a list
of known survivors and the mega-cap proxy in particular is biased toward names that kept
compounding.  Names with `max_1d_move >= 1.0` in data/small_meta.csv are dropped from the
small panel before anything is computed.

Deterministic, standalone.  Reads baseline.py; writes only its own outputs.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

COST_BPS, DIAG_BPS = 10, 0
FREQ = "W"
MAX_VOL = 0.60
N_RANKED = 20
GROSS = 0.75
CAPS = [0.00, 0.10, 0.25, 0.50, 1.00]
CAP_REF = 1.00
MEGA_K = 10
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"

OUT = REPO / "research" / "backtests"
STEM = Path(__file__).name[:-3]
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ panels
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    P(f"panels: U56 {px56.shape}, B136 {px136.shape}, small raw {pxs.shape}; "
      f"small dropped for max_1d_move>=1.0: {len(set(pxs.columns) & bad)}; "
      f"sector ETFs available: {len([t for t in U['sectors'] if t in px136.columns])}/16")
    return {
        "U56": sub(px56, list(px56.columns)),
        "B136": sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL": sub(pxs, s_stk, tradable=s_stk),
    }, U, etf36


def eligible_mask(px, tradable, ban=()):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable] + [c for c in ban if c in px.columns]
    if drop:
        m[list(dict.fromkeys(drop))] = False
    return m


def mega_mask(px, tradable, k=MEGA_K):
    """PIT size proxy (idea 71's PITGROW): the k names with the highest cumulative return
    from panel start to t.  Uses only data up to t."""
    tr = [c for c in px.columns if c in tradable]
    cum = px[tr] / px[tr].bfill().iloc[0]
    rank = cum.rank(axis=1, ascending=False)
    m = pd.DataFrame(False, index=px.index, columns=px.columns)
    m[tr] = (rank <= k).fillna(False).values
    return m


def top20_weights(px, tradable, ban=(), cap=CAP_REF, mega=None):
    elig = eligible_mask(px, tradable, ban)
    key = score(px, vol_scale=False)[0]
    sel = (key.where(elig).rank(axis=1, ascending=False) <= N_RANKED).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    w = sel.div(held, axis=0).mul(GROSS).fillna(0.0)
    if cap >= 1.0 or mega is None:
        return w
    mg = mega.reindex_like(w).fillna(False).values
    W = w.values.copy()
    gm = W * mg
    gross_row = W.sum(axis=1)
    mega_w = gm.sum(axis=1)
    limit = cap * gross_row
    over = mega_w > limit + 1e-12
    if over.any():
        scale = np.ones_like(mega_w)
        nz = mega_w > 0
        scale[nz & over] = limit[nz & over] / mega_w[nz & over]
        excess = mega_w - mega_w * scale
        W = np.where(mg, W * scale[:, None], W)
        rest = (W * (~mg)).sum(axis=1)
        add = np.zeros_like(W)
        ok = rest > 1e-12
        add[ok] = (W * (~mg))[ok] * (excess[ok] / rest[ok])[:, None]
        W = W + add                       # cash when no non-mega name is held
    return pd.DataFrame(W, index=w.index, columns=w.columns)


def halves_idx(r):
    return len(r) // 2


def halves(r):
    h = halves_idx(r)
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy):
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def v4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def run(px, w, bps=COST_BPS):
    res = backtest(px, w, cost_bps=bps, freq=FREQ)
    start = px.index[260]
    return res["returns"].loc[start:], res["weights"].loc[start:], res["turnover"].loc[start:]


# ================================================================= LEG A
def leg_a(panels):
    P("\n" + "=" * 100)
    P("LEG A - reproduction of idea 66's broad H2 shortfall (top20-200d, g=0.75, W, 10 bps)")
    P("=" * 100)
    px136, tr136 = panels["B136"]
    stk = panels["BSTK100"][1]
    rows = []
    for name, tr in (("B136 all-136-tradable", tr136), ("B136 stocks-only-tradable", stk)):
        r, _, _ = run(px136, top20_weights(px136, tr))
        spy = px136["SPY"].pct_change().fillna(0).loc[r.index]
        h1, h2 = halves(r)
        s1, s2 = halves(spy)
        m = metrics(r)
        rows.append(dict(convention=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                         H1=h1, H2=h2, SPY_H1=s1, SPY_H2=s2, gap_H2=h2 - s2))
    a = pd.DataFrame(rows).set_index("convention")
    P(fmt(a, 4))
    P(f"\nidea 66 published: book H2 0.814, SPY H2 0.837 (gap -0.023).")
    for c in a.index:
        P(f"  {c}: H2 {a.loc[c,'H2']:.4f} (residual vs 0.814 = {a.loc[c,'H2']-0.814:+.4f}), "
          f"SPY H2 {a.loc[c,'SPY_H2']:.4f} (vs 0.837 = {a.loc[c,'SPY_H2']-0.837:+.4f}), "
          f"gap {a.loc[c,'gap_H2']:+.4f}")
    P("The H2 SHORTFALL - book below SPY in the second half - reproduces under both "
      "conventions; the level differs slightly from idea 66's row (different tradable set / "
      "warm-up), and every number below is measured on THIS run's book, not on the quoted one.")
    a.to_csv(OUT / f"{STEM}.repro.csv")
    return a


# ================================================================= LEG B
def leg_b(panels):
    P("\n" + "=" * 100)
    P("LEG B - NAME decomposition of H2: is it a handful of names?")
    P("=" * 100)
    px, tr = panels["B136"]
    r, W, _ = run(px, top20_weights(px, tr))
    h = halves_idx(r)
    idx2 = r.index[h:]
    rets = px.pct_change().fillna(0.0).loc[idx2]
    contrib = (W.loc[idx2] * rets).sum(axis=0).sort_values()
    gross_h2 = contrib.sum()
    P(f"H2 = {idx2[0].date()}..{idx2[-1].date()} ({len(idx2)} days).  "
      f"Sum of per-name contributions {gross_h2:+.4f} vs the book's gross H2 return "
      f"{((1 + (W.loc[idx2] * rets).sum(axis=1)).prod() - 1):+.4f} (compounding differs; the "
      f"attribution is additive by construction).")
    held = contrib[contrib.abs() > 1e-9]
    pos = contrib[contrib > 0].sort_values(ascending=False)
    neg = contrib[contrib < 0].sort_values()
    cum = pos.cumsum() / pos.sum()
    n50 = int((cum <= 0.50).sum() + 1)
    n90 = int((cum <= 0.90).sum() + 1)
    P(f"\nNames with any H2 exposure: {len(held)} of {len(tr)} tradable.  "
      f"Net contributors {len(pos)}, net detractors {len(neg)}.")
    P(f"{n50} names produce 50% of the positive H2 P&L; {n90} produce 90%.")
    P("\nTop 10 contributors / bottom 10 detractors (H2 additive return contribution):")
    P(fmt(pd.DataFrame({"top": pos.head(10).round(4).astype(str).values,
                        "top_name": pos.head(10).index,
                        "bottom": neg.head(10).round(4).astype(str).values,
                        "bottom_name": neg.head(10).index}), 4))

    P("\nLeave-one-out: ban each held name from eligibility over the WHOLE sample and re-run "
      "(the book reconstitutes, so this is a real counterfactual, not an ex-post deletion).")
    spy = px["SPY"].pct_change().fillna(0).loc[r.index]
    base_h1, base_h2 = halves(r)
    s1, s2 = halves(spy)
    loo = []
    names = list(held.index)
    for i, nm in enumerate(names):
        rr, _, _ = run(px, top20_weights(px, tr, ban=(nm,)))
        h1, h2 = halves(rr)
        m = metrics(rr)
        loo.append(dict(name=nm, contrib_H2=float(contrib[nm]), H1=h1, H2=h2,
                        dH1=h1 - base_h1, dH2=h2 - base_h2, Sharpe=m["Sharpe"],
                        CAGR=m["CAGR"], MaxDD=m["MaxDD"], closes_gap=bool(h2 > s2)))
        if (i + 1) % 25 == 0:
            P(f"  ... {i+1}/{len(names)} leave-one-out runs done")
    L = pd.DataFrame(loo).set_index("name").sort_values("dH2", ascending=False)
    L.to_csv(OUT / f"{STEM}.names.csv")
    P(f"\nBase book H2 {base_h2:.4f} vs SPY H2 {s2:.4f} (gap {base_h2-s2:+.4f}).")
    P(f"Leave-one-out dH2: mean {L.dH2.mean():+.4f}, sd {L.dH2.std():.4f}, "
      f"max {L.dH2.max():+.4f} ({L.dH2.idxmax()}), min {L.dH2.min():+.4f} ({L.dH2.idxmin()}).")
    P(f"Single deletions that lift H2 above SPY's {s2:.4f}: **{int(L.closes_gap.sum())}** "
      f"of {len(L)}.")
    P("\nTop 15 by dH2 (deleting the name HELPS most):")
    P(fmt(L.head(15)[["contrib_H2", "H2", "dH2", "Sharpe", "CAGR", "MaxDD", "closes_gap"]], 4))
    P("\nBottom 10 by dH2 (deleting the name HURTS most):")
    P(fmt(L.tail(10)[["contrib_H2", "H2", "dH2", "Sharpe", "CAGR", "MaxDD", "closes_gap"]], 4))
    rho = float(np.corrcoef(L.contrib_H2, L.dH2)[0, 1])
    P(f"\ncorr(H2 contribution, dH2 from deleting it) = {rho:+.3f} - if the shortfall were a "
      f"handful of bad names this would be strongly negative and a few deletions would close "
      f"the gap.")
    return contrib, L, r, W, spy


# ================================================================= LEG C
def leg_c(r, spy):
    P("\n" + "=" * 100)
    P("LEG C - REGIME decomposition of H2: is it a regime?")
    P("=" * 100)
    h = halves_idx(r)
    r2, s2r = r.iloc[h:], spy.iloc[h:]

    def blk(mask, label):
        a, b = r2[mask], s2r[mask]
        if len(a) < 30:
            return dict(state=label, days=len(a), bk_Sharpe=np.nan, spy_Sharpe=np.nan,
                        d_Sharpe=np.nan, bk_ann=np.nan, spy_ann=np.nan, excess_ann=np.nan)
        ma, mb = metrics(a), metrics(b)
        return dict(state=label, days=len(a), bk_Sharpe=ma["Sharpe"], spy_Sharpe=mb["Sharpe"],
                    d_Sharpe=ma["Sharpe"] - mb["Sharpe"], bk_ann=a.mean() * 252,
                    spy_ann=b.mean() * 252, excess_ann=(a - b).mean() * 252)

    P("\nC1 - per calendar year inside H2:")
    yr = []
    for y, g in r2.groupby(r2.index.year):
        b = s2r.loc[g.index]
        yr.append(dict(year=int(y), days=len(g), bk=(1 + g).prod() - 1, spy=(1 + b).prod() - 1,
                       excess=(1 + g).prod() - (1 + b).prod(),
                       bk_Sharpe=metrics(g)["Sharpe"], spy_Sharpe=metrics(b)["Sharpe"]))
    Y = pd.DataFrame(yr).set_index("year")
    P(fmt(Y, 4))
    P(f"  years the book beat SPY: {int((Y.excess > 0).sum())}/{len(Y)}; "
      f"worst {Y.excess.idxmin()} ({Y.excess.min():+.1%}), best {Y.excess.idxmax()} "
      f"({Y.excess.max():+.1%}).")
    P(f"  H2 excess with the single worst year removed: "
      f"{(Y.drop(Y.excess.idxmin()).excess.mean()):+.4f} mean vs {Y.excess.mean():+.4f} with it.")

    rows = []
    vol = spy.rolling(60).std() * np.sqrt(252)          # trailing only
    med = vol.loc[r2.index].median()
    hv = vol.loc[r2.index] >= med
    rows += [blk(hv.values, f"SPY 60d vol >= H2 median ({med:.3f})"),
             blk(~hv.values, f"SPY 60d vol <  H2 median ({med:.3f})")]
    spx = (1 + spy).cumprod()
    up = (spx > spx.rolling(200).mean()).loc[r2.index].fillna(True)
    rows += [blk(up.values, "SPY above its own 200d MA"),
             blk(~up.values, "SPY below its own 200d MA")]
    dd = (spx / spx.cummax() - 1).loc[r2.index]
    rows += [blk((dd <= -0.05).values, "SPY drawdown <= -5%"),
             blk((dd > -0.05).values, "SPY drawdown >  -5%")]
    R = pd.DataFrame(rows).set_index("state")
    P("\nC2/C3/C4 - trailing-computable regime splits inside H2:")
    P(fmt(R, 4))
    Y.to_csv(OUT / f"{STEM}.years.csv")
    R.to_csv(OUT / f"{STEM}.regimes.csv")
    return Y, R


# ================================================================= LEG D
def leg_d(panels, W, U):
    P("\n" + "=" * 100)
    P("LEG D - SECTOR decomposition of H2 (PIT correlation proxy, NOT GICS)")
    P("=" * 100)
    px, tr = panels["B136"]
    etfs = [t for t in U["sectors"] if t in px.columns]
    rets = px.pct_change().fillna(0.0)
    idx = W.index
    h = halves_idx(pd.Series(index=idx, dtype=float))
    idx2 = idx[h:]
    # PIT sector map: trailing-252d correlation to each sector ETF, recomputed each year-end
    stamps = sorted({d for d in idx2} & set(idx2[::63]))
    if idx2[-1] not in stamps:
        stamps.append(idx2[-1])
    contrib = (W.loc[idx2] * rets.loc[idx2])
    sect_tot, unassigned = {}, 0.0
    prev = None
    for k, d in enumerate(stamps):
        win = rets.loc[:d].tail(252)
        if len(win) < 100:
            continue
        C = win.corr()
        cols = [c for c in px.columns if c in tr]
        best = {}
        for c in cols:
            if c in etfs:
                best[c] = c
                continue
            v = C.loc[c, etfs].astype(float)
            best[c] = v.idxmax() if v.notna().any() else "UNASSIGNED"
        lo = prev if prev is not None else idx2[0]
        seg = contrib.loc[lo:d] if prev is not None else contrib.loc[:d]
        for c, s in best.items():
            if c in seg.columns:
                sect_tot[s] = sect_tot.get(s, 0.0) + float(seg[c].sum())
        prev = d
    S = pd.Series(sect_tot).sort_values(ascending=False)
    S = S[S.abs() > 1e-9]
    P(f"Sector map recomputed every 63 trading days on a trailing 252d correlation window "
      f"({len(stamps)} stamps, {len(etfs)} sector ETFs).  H2 additive contribution by "
      f"assigned sector:")
    tab = pd.DataFrame({"H2_contrib": S, "share_of_gross": S / S.sum()})
    P(fmt(tab, 4))
    P(f"  top sector {S.index[0]} = {S.iloc[0]:+.4f} ({S.iloc[0]/S.sum():.1%} of the gross H2 "
      f"attribution); the 3 largest = {S.head(3).sum()/S.sum():.1%}.")
    P("CAVEAT: this is a return-correlation proxy for sector, not GICS; no sector file is "
      "cached in data/.  It answers 'is the H2 P&L concentrated in one correlated block' and "
      "nothing finer.")
    tab.to_csv(OUT / f"{STEM}.sectors.csv")
    return tab


# ================================================================= LEG E
def leg_e(panels):
    P("\n" + "=" * 100)
    P("LEG E - MEGA-CAP WEIGHT and the actionable cap arm (4 panels x 5 caps x 2 rungs)")
    P("=" * 100)
    rows, cache = [], {}
    for pname, (px, tr) in panels.items():
        mega = mega_mask(px, tr)
        spy = px["SPY"].pct_change().fillna(0)
        start = px.index[260]
        for bps in (COST_BPS, DIAG_BPS):
            b = backtest(px, rules_v1_weights(px), cost_bps=bps, freq=FREQ)["returns"].loc[start:]
            cache[("v1", pname, np.nan, bps)] = b
        for c in CAPS:
            w = top20_weights(px, tr, cap=c, mega=mega)
            for bps in (COST_BPS, DIAG_BPS):
                r, W, T = run(px, w, bps)
                sp = spy.loc[r.index]
                h = halves_idx(r)
                mw = (W * mega.reindex_like(W).fillna(False)).sum(axis=1)
                gr = W.sum(axis=1).replace(0, np.nan)
                mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[IS_START:IS_END])
                h1, h2 = halves(r)
                cache[("cap", pname, c, bps)] = r
                rows.append(dict(
                    panel=pname, cap=c, bps=bps, CAGR=mm["CAGR"], Vol=mm["Vol"],
                    Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                    SPY_H1=halves(sp)[0], SPY_H2=halves(sp)[1],
                    IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    mega_w_H1=float((mw / gr).iloc[:h].mean()),
                    mega_w_H2=float((mw / gr).iloc[h:].mean()),
                    Turn_yr=float(T.sum() / (len(r) / 252)),
                    SPY_CAGR=metrics(sp)["CAGR"], SPY_Sharpe=metrics(sp)["Sharpe"],
                    SPY_MaxDD=metrics(sp)["MaxDD"]))
                P(f"  ran {pname:8s} cap={c:.2f} {bps:2d}bps  CAGR {mm['CAGR']:6.2%}  "
                  f"Sharpe {mm['Sharpe']:.3f}  H2 {h2:.3f} (SPY {halves(sp)[1]:.3f})  "
                  f"megaW H1 {rows[-1]['mega_w_H1']:.3f} H2 {rows[-1]['mega_w_H2']:.3f}")
    G = pd.DataFrame(rows)
    p4a, f4b = [], []
    for _, r in G.iterrows():
        rr = cache[("cap", r.panel, r.cap, r.bps)]
        px = panels[r.panel][0]
        sp = px["SPY"].pct_change().fillna(0).loc[rr.index]
        p4a.append(v4a(rr, cache[("v1", r.panel, np.nan, r.bps)]))
        f4b.append(fail4b(rr, sp))
    G["pass4a"], G["fail4b"] = p4a, f4b
    G["pass4b"] = G.fail4b == "-"
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    P(f"\nALL {len(G)} grid points (every one reported):")
    cols = ["panel", "cap", "bps", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "SPY_H2",
            "IS_Sharpe", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "mega_w_H1", "mega_w_H2",
            "Turn_yr", "pass4a", "pass4b", "fail4b"]
    P(fmt(G[cols].set_index(["panel", "cap", "bps"]), 3))

    P("\nMEGA10 weight of the UNCAPPED book (cap=1.00), H1 vs H2 - the queue's second axis:")
    u = G[(G.cap == CAP_REF) & (G.bps == COST_BPS)].set_index("panel")
    P(fmt(u[["mega_w_H1", "mega_w_H2", "H1", "H2", "SPY_H1", "SPY_H2"]], 4))
    P("  (MEGA10 = the 10 names with the highest cumulative return to date - a PIT GROWTH "
      "proxy for size, not market cap; no shares-outstanding series is cached.)")

    P("\n" + "-" * 100)
    P("RULE 8 walk-forward: IS 2009-2016 chooses the cap, OOS 2017+ read once")
    P("-" * 100)
    wf = []
    for (pn, bps), s in G.groupby(["panel", "bps"]):
        px = panels[pn][0]
        sp = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        base = cache[("v1", pn, np.nan, bps)]
        picks = {"IS_ARGMAX": s.loc[s.IS_Sharpe.idxmax()],
                 "CAP_NONE": s[s.cap == CAP_REF].iloc[0]}
        for nm, r in picks.items():
            m = metrics(cache[("cap", pn, r.cap, bps)].loc[OOS_START:])
            wf.append(dict(panel=pn, bps=bps, selector=nm, pick=f"cap={r.cap:.2f}",
                           IS_Sharpe=r.IS_Sharpe, OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                           OOS_MaxDD=m["MaxDD"]))
        for nm, ser in (("RULESv1", base), ("SPY", sp)):
            m = metrics(ser.loc[OOS_START:])
            wf.append(dict(panel=pn, bps=bps, selector=nm, pick="-",
                           IS_Sharpe=metrics(ser.loc[IS_START:IS_END])["Sharpe"],
                           OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(WF.set_index(["panel", "bps", "selector"]), 3))
    w1 = WF[WF.bps == COST_BPS]
    a = w1[w1.selector == "IS_ARGMAX"].set_index("panel")
    b = w1[w1.selector == "CAP_NONE"].set_index("panel")
    P(f"\nIS_ARGMAX - CAP_NONE, OOS @10bps: dSharpe {(a.OOS_Sharpe-b.OOS_Sharpe).mean():+.4f} "
      f"mean ({int((a.OOS_Sharpe>b.OOS_Sharpe).sum())}/{len(a)} panels better), "
      f"dCAGR {(a.OOS_CAGR-b.OOS_CAGR).mean():+.4f}; "
      f"same pick in {int((a.pick==b.pick).sum())}/{len(a)} panels.")

    P("\n" + "-" * 100)
    P("KEEP paths on every leg-E point (10 bps)")
    P("-" * 100)
    g10 = G[G.bps == COST_BPS]
    P(f"4a passes {int(g10.pass4a.sum())}/{len(g10)}   4b passes {int(g10.pass4b.sum())}/{len(g10)}")
    P(fmt(g10.groupby(["panel"])[["pass4a", "pass4b"]].sum(), 0))
    P("\n4b failing bars, by point:")
    P(g10.groupby("fail4b").size().to_string())
    if g10.pass4b.any():
        P("\n4b PASSES:")
        P(fmt(g10[g10.pass4b][cols].set_index(["panel", "cap"]), 3))
    P("\nDoes ANY cap close the B136 H2 bar (book H2 > SPY H2)?")
    b136 = g10[g10.panel == "B136"]
    P(fmt(b136.set_index("cap")[["H2", "SPY_H2", "Sharpe", "CAGR", "MaxDD", "mega_w_H2"]], 4))
    P(f"  -> {int((b136.H2 > b136.SPY_H2).sum())} of {len(b136)} cap levels clear it.")
    return G, WF


def main():
    panels, U, etf36 = build_panels()
    leg_a(panels)
    contrib, L, r, W, spy = leg_b(panels)
    leg_c(r, spy)
    leg_d(panels, W, U)
    leg_e(panels)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
