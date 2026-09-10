#!/usr/bin/env python3
"""Idea 613 — publish DRAG, not TURNOVER, beside every window-width claim.  (cloud, 2026-09-10)

QUEUE 613: "idea 403 found width = intercept(panel, book, sleeve) - slope x drag with the two
terms carrying OPPOSITE signs in turnover (within-cell rho(width, drag) -0.85 to -0.96, but
pooled rho(width, base_to) only -0.127 and the high-turnover book has the WIDER window).  Census
the record's committed width/window claims and re-price each one on drag = base turnover x rung;
report how many change rank.  Max 2 params (claim set, rung ladder)."

WHAT IS ACTUALLY BEING TESTED
  H1  (census)   The record publishes width/window claims without the columns needed to price
                 them on drag.  Falsifiable: if most width files carry a turnover column AND a
                 rung column, the prescription is already met and the idea is a no-op.
  H2  (algebra)  Re-pricing on drag can only change a ranking where the claim's cells sit at
                 DIFFERENT rungs: inside one rung, drag = base_to * c/1e4 is a positive affine
                 map of base_to and the ranking is IDENTICAL by construction.  Falsifiable by
                 counting single-rung vs multi-rung claim sites.
  H3  (slope)    403's within-cell rho(width, drag) in [-0.85, -0.96] replicates on a THIRD
                 panel (SMALL439) and on a SECOND sleeve (CASH, i.e. plain de-grossing) that
                 403 never ran and that exists on every panel, ETFs or not.
  H4  (level)    403's cross-cell result — pooled rho(width, base_to) ~ 0 and the higher-turnover
                 book carrying the WIDER window — replicates on the same fresh grid.
  H5  (the ask)  Ranking width-claim cells by base turnover vs by drag: how many change rank,
                 as a function of the rung ladder.

AXES AND WHAT IS SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
  The queue names the two tuned parameters: CLAIM SET and RUNG LADDER.  Both are swept in full
  and every point is reported.
    P1 claim set  : TIER-A (strict: a column that names an INTERVAL WIDTH on a dial) and
                    TIER-B (loose: TIER-A plus every keyword hit, the census a regex would make).
    P2 rung ladder: L1 = [10], L2 = [10, 25], L4 = [0, 10, 25, 50], L6 = [0, 5, 10, 15, 25, 50].
  The fresh leg carries two further axes, and NEITHER is tuned in the census sense:
    f      the DIAL WHOSE WINDOW IS MEASURED (the sleeve fraction, 403's own dial).  A width is
           a statistic OVER this grid; the grid is uniform (0.00-0.50, step 0.05) and fully
           enumerated, and no point of it is ever chosen.
    lambda the TURNOVER INSTRUMENT (idea 137's partial rebalance, verbatim).  Fully enumerated,
           reported at every point, never chosen.
  Panels, books, sleeves and cost rungs are REPORTED axes and are never selected on.  The ONLY
  place anything is chosen is PROTOCOL rule 8, where (f, lambda) is picked on 2009-2016 alone by
  four pre-registered selectors and 2017-2026 is read exactly once.

GATES (run before any new number is read)
  G1 the vectorised runner vs `engine.backtest` on the evaluated slice, returns AND turnover.
  G2 the rung identity r(c) = r(0) - turnover*c/1e4 vs a live `engine.backtest(cost_bps=25)`.
     This is what licenses reading six rungs off one simulation and it is also the reason the
     question is well posed: with no equity-reading instrument, turnover reaches a return series
     ONLY through cost, so a turnover-cost fact must be a function of drag alone.
  G3 idea 403's committed `.windows.csv`: base turnover strictly monotone in lambda, and the
     within-cell rho(width, drag) band the queue quotes reproduced off the committed artefact.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three panels are current constituents.  SMALL439 additionally
    drops the 44 tickers with max_1d_move >= 1.0 from data/small_meta.csv before anything runs.
  * lambda can only LOWER turnover, so the falsification is one-sided.
  * lambda changes the book's PATH as well as its trading (403's own caveat); the cost route,
    which changes drag and nothing else, is the arbiter.
  * MaxDD is one number off one path (idea 321); the 4b DD cap turns on exactly that number.
  * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
  * The census reads COMMITTED CSVs only.  A width claim made in prose and never written to a
    CSV is invisible to it; TIER-B is the loose bound and is reported beside TIER-A for that
    reason.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .census.csv, .sites.csv,
.grid.csv, .windows.csv, .walkforward.csv next to itself.
"""
from __future__ import annotations

import csv
import glob
import importlib.util
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_publish-DRAG-not-TURNOVER-beside-every-window-width-claim_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I403_WIN = OUT / "2026-09-10_is-the-4b-window-a-TURNOVER-COST-fact-about-the-ranked-book_B.windows.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")                       # idea 94's harness: composite / vol20 / gate_mask
FREQ, GROSS, MAX_VOL = H.FREQ, H.GROSS, H.MAX_VOL
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60                     # 4b CAGR floor / DD cap fractions of SPY

FSTEP = 0.05
FS = [round(FSTEP * i, 2) for i in range(11)]   # the DIAL whose window is measured (uniform)
LAMBDAS = [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06]   # idea 137's dial, verbatim ladder
BOOKS = ["TOP20", "EWALL"]                  # idea 403's own turnover contrast (~13x vs ~0.8x/yr)
SLEEVES = ["CASH", "ETF3"]                  # CASH = de-gross to (1-f); ETF3 = idea 100/104's
ETF3 = ["TLT", "GLD", "UUP"]                # defensive sleeve, verbatim (403's S3)
NTOP = 20
PANELS = ["u56", "broad", "small"]
RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]
LADDERS = {"L1": [10.0], "L2": [10.0, 25.0], "L4": [0.0, 10.0, 25.0, 50.0], "L6": list(RUNGS)}
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# vectorised runner (segment-exact reproduction of engine.backtest at zero cost)
# =====================================================================================
def fast_bt(px: pd.DataFrame, W: pd.DataFrame, freq=FREQ):
    """engine.backtest's drift algebra, one pass per REBALANCE SEGMENT instead of per day.

    Inside a segment nothing trades, so the book is buy-and-hold: name j's stake grows by
    prod(1+r_j) and the (zero-yield) cash residual is constant, which makes the portfolio's
    daily return exactly S(i)/S(i-1) - 1 with S = sum(stakes) + cash.  Identical to the engine
    on the evaluated slice (G1); row 0 differs only because the engine leaves it NaN.
    """
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
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
    idx = px.index
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# =====================================================================================
# books
# =====================================================================================
def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim (via idea 403): the target is an EWMA of the
    raw target with gross restored daily, so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


def book_weights(px, book, investable):
    """TOP20 = composite top-20, equal weight at GROSS/20 (the record's ranked book).
       EWALL = equal weight over every priced name at GROSS/N (the record's un-ranked control).
    Both ungated, so the ONLY dials in play are f and lambda."""
    sub = px[investable]
    if book == "EWALL":
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        W = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    else:
        rank = H.composite(sub).rank(axis=1, ascending=False)
        W = (rank <= NTOP).astype(float) * (GROSS / NTOP)
    return W.reindex(columns=px.columns).fillna(0.0)


def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """Ideas 100/104's defensive sleeve, verbatim via ideas 133/134/138/403: momentum vote x
    risk parity over the sleeve assets."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def blend(base_W, sl_W, f, sleeve):
    """f = the DIAL.  CASH: hold (1-f) of the base book and f in zero-yield cash (the record's
    de-gross convention).  ETF3: idea 134/138/403's blend, (1-f)*base + f*sleeve rescaled to
    GROSS per day."""
    if f == 0.0:
        return base_W
    if sleeve == "CASH":
        return base_W * (1.0 - f)
    raw = (1 - f) * base_W + f * sl_W
    return raw.mul((GROSS / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


# =====================================================================================
# metric helpers
# =====================================================================================
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


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
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or len(set(a[ok])) < 2 or len(set(b[ok])) < 2:
        return np.nan
    return float(np.corrcoef(pd.Series(a[ok]).rank(), pd.Series(b[ok]).rank())[0, 1])


def window_of(sub, col="pass4b"):
    """Window statistics over ONE cell's uniform f grid.  n_pass = passing grid points;
    w_pts = longest contiguous passing run in GRID POINTS; w_units = the same in f units."""
    d = sub.sort_values("f")
    p = d[col].values.astype(bool)
    nv = d["f"].values
    best = cur = 0
    blo = bhi = clo = np.nan
    for i, ok in enumerate(p):
        if ok:
            if cur == 0:
                clo = nv[i]
            cur += 1
            if cur > best:
                best, blo, bhi = cur, clo, nv[i]
        else:
            cur = 0
    return dict(n_pass=int(p.sum()), w_pts=int(best),
                w_units=(best - 1) * FSTEP if best > 0 else 0.0,
                f_lo=blo, f_hi=bhi, is_empty=bool(p.sum() == 0))


def rank_change(vals_a, vals_b, keys):
    """Rank the same cells two ways and price the disagreement.  Returns #cells whose rank
    moves, Kendall tau, and whether the argmin/argmax cell changes."""
    ra = pd.Series(vals_a, index=keys).rank(method="average")
    rb = pd.Series(vals_b, index=keys).rank(method="average")
    moved = int((ra != rb).sum())
    a, b = np.asarray(vals_a, float), np.asarray(vals_b, float)
    conc = disc = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            da, db = a[i] - a[j], b[i] - b[j]
            if da == 0 or db == 0:
                continue
            if da * db > 0:
                conc += 1
            else:
                disc += 1
    tau = (conc - disc) / (conc + disc) if (conc + disc) else np.nan
    return dict(n_cells=len(a), n_moved=moved, frac_moved=moved / len(a) if len(a) else np.nan,
                kendall_tau=tau, n_discordant=disc,
                top_changed=bool(np.argmax(a) != np.argmax(b)))


# =====================================================================================
# panels
# =====================================================================================
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def get_panels():
    P = {}
    P["u56"] = (load_universe(), None)
    P["broad"] = (load_universe(broad=True), None)
    sp, ndrop = small_panel()
    P["small"] = (sp, ndrop)
    return P


# =====================================================================================
# LEG 1 — GATES
# =====================================================================================
def gates(panels):
    say("=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True

    # G1 / G2 on every panel, on the panel's own evaluated slice.
    for pk, (px, _) in panels.items():
        inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
        W = book_weights(px, "TOP20", inv)
        start = px.index[260]
        r_f, t_f = fast_bt(px, W)
        e0 = backtest(px, W, cost_bps=0.0, freq=FREQ)
        d_r = float((r_f.loc[start:] - e0["returns"].loc[start:]).abs().max())
        d_t = float((t_f.loc[start:] - e0["turnover"].loc[start:]).abs().max())
        e25 = backtest(px, W, cost_bps=25.0, freq=FREQ)
        d_c = float(((r_f - t_f * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G1 {pk:>5}: fast_bt vs engine.backtest   max|dr| {d_r:.3e}   max|dturnover| {d_t:.3e}")
        say(f"  G2 {pk:>5}: rung identity vs live 25 bps max|dr| {d_c:.3e}")
        ok &= (d_r < 1e-12) and (d_t < 1e-12) and (d_c < 1e-12)

    # G3 idea 403's committed windows artefact.
    if I403_WIN.exists():
        w403 = pd.read_csv(I403_WIN)
        mono = []
        for k, g in w403.groupby(["panel", "book", "sleeve", "cost"]):
            g = g.sort_values("lam", ascending=False)
            mono.append(bool((g["base_to"].diff().dropna() <= 1e-12).all()))
        rhos = []
        for k, g in w403[w403.cost > 0].groupby(["panel", "book", "sleeve"]):
            rhos.append(spearman(g["w_contig"].values, (g["base_to"] * g["cost"] / 1e4).values))
        say(f"  G3 idea 403 .windows.csv: {len(w403)} rows; base_to monotone in lambda in "
            f"{sum(mono)}/{len(mono)} (panel,book,sleeve,cost) cells")
        say(f"     within-cell rho(w_contig, drag) over {len(rhos)} cells: "
            f"min {np.nanmin(rhos):+.3f}  max {np.nanmax(rhos):+.3f}  "
            f"(the queue quotes -0.854 .. -0.960)")
        ok &= (sum(mono) == len(mono))
    else:
        say("  G3 SKIPPED: idea 403 .windows.csv not found")
        ok = False
    say(f"  GATES {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================================
# LEG 2 — CENSUS of the record's committed width/window claims
# =====================================================================================
# TIER-A: a column that names an INTERVAL WIDTH on a dial (what idea 403's claim is about).
TIER_A = re.compile(
    r"(^|_)(w_contig|w_pts|w_units|width|run_width|med_width|joint_width|min_cell_width|"
    r"zone_width|n_pass|npass|n_runs|nwin)($|_)", re.I)
# TIER-B: TIER-A plus every keyword a naive regex census would catch, including TIME windows.
TIER_B = re.compile(r"(width|window|n_pass|npass|n_runs|nwin|interval)", re.I)
TO_RE = re.compile(r"(turnover|base_to|turn_yr|turn_fwd|turn_ew|turn_ma|turn_q|^to$|_to$|^to_|turn)", re.I)
COST_RE = re.compile(r"(cost_bps|^cost$|^bps$|^rung$|rung|_bps$|^cost_)", re.I)
# A keyword census over-counts (ideas 286/523).  A column only COUNTS as a turnover or a rung if
# its NAME is not a statistic about one and its VALUES are in the right physical range.
NOT_A_QUANTITY = re.compile(r"(spearman|kendall|pearson|rho|corr|_ok$|^ok_|flag|share|frac|pct|rate)", re.I)


def _valid_to(v):
    """A turnover column: non-negative, not a correlation, and actually trading (max > 0.1 x/yr)."""
    v = pd.to_numeric(v, errors="coerce").dropna()
    return len(v) >= 3 and float(v.min()) >= 0.0 and float(v.max()) > 0.1


def _valid_rung(v):
    """A cost rung: non-negative bps, at most 500, and at least one non-zero rung."""
    v = pd.to_numeric(v, errors="coerce").dropna()
    return len(v) >= 3 and float(v.min()) >= 0.0 and float(v.max()) <= 500.0 and float(v.max()) > 0.0
PANEL_RE = re.compile(r"(^panel$|^universe$|^pk$)", re.I)
BOOK_RE = re.compile(r"(^book$|^arm$|^form$|^family$)", re.I)


def census():
    say()
    say("=" * 100)
    say("LEG 2 — CENSUS: every committed CSV in research/backtests")
    say("=" * 100)
    files = [f for f in sorted(glob.glob(str(OUT / "*.csv"))) + sorted(glob.glob(str(OUT / "*.csv.gz")))
             if STEM not in os.path.basename(f)]      # never census this run's own artefacts
    rows = []
    for f in files:
        try:
            if f.endswith(".gz"):
                hdr = list(pd.read_csv(f, nrows=0).columns)
            else:
                with open(f, newline="") as fh:
                    hdr = next(csv.reader(fh))
        except Exception:
            continue
        a = [c for c in hdr if TIER_A.search(c)]
        b = [c for c in hdr if TIER_B.search(c)]
        if not b:
            continue
        t = [c for c in hdr if TO_RE.search(c) and not NOT_A_QUANTITY.search(c)]
        cc = [c for c in hdr if COST_RE.search(c) and not NOT_A_QUANTITY.search(c)]
        if t or cc:                                   # value check, not just the name
            try:
                D0 = pd.read_csv(f, usecols=lambda c: c in set(t) | set(cc))
                t = [c for c in t if c in D0 and _valid_to(D0[c])]
                cc = [c for c in cc if c in D0 and _valid_rung(D0[c])]
            except Exception:
                t, cc = [], []
        rows.append(dict(file=os.path.basename(f), n_cols=len(hdr),
                         tierA=int(bool(a)), tierB=1,
                         width_cols_A=";".join(a), width_cols_B=";".join(b),
                         to_cols=";".join(t), cost_cols=";".join(cc),
                         has_to=int(bool(t)), has_cost=int(bool(cc)),
                         has_panel=int(any(PANEL_RE.search(c) for c in hdr)),
                         has_book=int(any(BOOK_RE.search(c) for c in hdr))))
    C = pd.DataFrame(rows)
    say(f"committed CSVs scanned: {len(files)} (this run's own artefacts excluded)")
    for tier, sub in (("TIER-A (strict: interval width on a dial)", C[C.tierA == 1]),
                      ("TIER-B (loose: every keyword hit)", C)):
        n = len(sub)
        say(f"\n  {tier}")
        say(f"    files carrying a width/window column : {n}")
        say(f"    ... AND a turnover-like column       : {int(sub.has_to.sum())}"
            f"  ({sub.has_to.mean():.1%})")
        say(f"    ... AND a cost/rung-like column      : {int(sub.has_cost.sum())}"
            f"  ({sub.has_cost.mean():.1%})")
        both = sub[(sub.has_to == 1) & (sub.has_cost == 1)]
        say(f"    ... AND BOTH (re-priceable as published): {len(both)}"
            f"  ({len(both)/n:.1%})" if n else "")
        if len(both):
            for _, r in both.iterrows():
                say(f"        {r.file[:78]}")
    return C


def reprice_sites(C):
    """For every re-priceable file: group its rows into claim sites, rank the site's cells by
    base turnover and by drag, and count the rank changes at each rung ladder."""
    say()
    say("=" * 100)
    say("LEG 3 — RE-PRICE the record's re-priceable width claims on drag = base turnover x rung")
    say("=" * 100)
    out = []
    both = C[(C.has_to == 1) & (C.has_cost == 1)]
    for _, meta in both.iterrows():
        path = OUT / meta.file
        try:
            D = pd.read_csv(path)
        except Exception as e:
            say(f"  SKIP {meta.file}: {type(e).__name__}")
            continue
        wcol = (meta.width_cols_A or meta.width_cols_B).split(";")[0]
        tcol = meta.to_cols.split(";")[0]
        ccol = meta.cost_cols.split(";")[0]
        for c in (wcol, tcol, ccol):
            if c not in D.columns:
                break
        else:
            D = D[[wcol, tcol, ccol] + [c for c in ("panel", "book", "sleeve", "lam")
                                        if c in D.columns]].copy()
            for c in (wcol, tcol, ccol):
                D[c] = pd.to_numeric(D[c], errors="coerce")
            D = D.dropna(subset=[wcol, tcol, ccol])
            if len(D) < 3:
                continue
            nrungs = D[ccol].nunique()
            drag = D[tcol] * D[ccol] / 1e4
            rc = rank_change(D[tcol].values, drag.values, list(range(len(D))))
            out.append(dict(file=meta.file, tierA=int(meta.tierA), width_col=wcol,
                            to_col=tcol, cost_col=ccol, n_rows=len(D), n_rungs=nrungs,
                            rho_w_to=spearman(D[wcol].values, D[tcol].values),
                            rho_w_drag=spearman(D[wcol].values, drag.values),
                            **rc))
    S = pd.DataFrame(out)
    if len(S):
        say(S.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        say()
        say(f"  sites re-priced: {len(S)}   single-rung (re-pricing is a NO-OP by construction): "
            f"{int((S.n_rungs == 1).sum())}   multi-rung: {int((S.n_rungs > 1).sum())}")
        say(f"  cells whose rank MOVES under the re-pricing: {int(S.n_moved.sum())} of "
            f"{int(S.n_cells.sum())} ({S.n_moved.sum()/max(S.n_cells.sum(),1):.1%})")
        say(f"  mean rho(width, base_to) {S.rho_w_to.mean():+.3f}   "
            f"mean rho(width, drag) {S.rho_w_drag.mean():+.3f}")
    else:
        say("  NO committed CSV in the record carries (width, turnover, rung) together.")
    return S


# =====================================================================================
# LEG 4 — FRESH GRID: measure the width dial on three panels and re-price it on drag
# =====================================================================================
def run_panel(pk, px, ndrop):
    inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars_full = bars_of(spy, "full")
    bars_is = bars_of(spy, "IS")
    v2r, v2t = fast_bt(px, rules_v2_weights(px))
    v2 = {c: (v2r - v2t * c / 1e4).loc[start:] for c in RUNGS}
    say(f"\n  panel {pk}: {px.shape[1]} cols ({len(inv)} investable"
        + (f", {ndrop} tickers dropped for max_1d_move>=1.0" if ndrop else "") +
        f"), {px.index[0].date()} -> {px.index[-1].date()}, evaluated from {start.date()}")
    say(f"    SPY bars: H1 {bars_full['s1']:.3f}  H2 {bars_full['s2']:.3f}  "
        f"OOS {bars_full['soos']:.3f}  MaxDD {bars_full['sdd']:.1%}  CAGR {bars_full['scagr']:.2%}")

    sleeves = [s for s in SLEEVES if s == "CASH" or all(t in px.columns for t in ETF3)]
    if len(sleeves) < len(SLEEVES):
        say(f"    ETF3 sleeve {ETF3} not priced on this panel -> CASH sleeve only "
            f"(idea 54 note: the small panel is pure small caps, SPY is a benchmark not a name)")
    sl_W = {"ETF3": sleeve_weights(px, ETF3)} if "ETF3" in sleeves else {}
    sl_W["CASH"] = None

    rows, series = [], {}
    for book in BOOKS:
        raw = book_weights(px, book, inv)
        for lam in LAMBDAS:
            base = smooth(raw, lam)
            for sleeve in sleeves:
                for f in FS:
                    r0, t0 = fast_bt(px, blend(base, sl_W.get(sleeve), f, sleeve))
                    r0, t0 = r0.loc[start:], t0.loc[start:]
                    series[(pk, book, sleeve, lam, f)] = (r0, t0)
                    if f == 0.0:
                        base_to_cell = float(t0.sum() / (len(t0) / 252))
                    for c in RUNGS:
                        r = r0 - t0 * c / 1e4
                        m = metrics(r)
                        mg = margins(r, bars_full, "full")
                        mgi = margins(r.loc[:IS_END], bars_is, "IS")
                        rows.append(dict(
                            panel=pk, book=book, sleeve=sleeve, lam=lam, f=f, cost=c,
                            base_to=base_to_cell, drag=base_to_cell * c / 1e4,
                            arm_to=float(t0.sum() / (len(t0) / 252)),
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=halves(r)[0], H2=halves(r)[1],
                            OOSs=metrics(r.loc[OOS_START:])["Sharpe"],
                            **{f"m_{k}": mg[k] for k in BARS5},
                            m_min=min(mg[k] for k in BARS5),
                            pass4b=all(mg[k] > 0 for k in BARS5), pass4a=pass4a(r, v2[c]),
                            IS_pass4b=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"]))
    return pd.DataFrame(rows), series, v2, bars_full


def main():
    T0 = time.time()
    say("=" * 100)
    say("IDEA 613 — publish DRAG, not TURNOVER, beside every window-width claim   (cloud)")
    say("=" * 100)
    say(f"tuned parameter 1 (claim set): TIER-A strict / TIER-B loose — both reported")
    say(f"tuned parameter 2 (rung ladder): {LADDERS} — all reported")
    say(f"measurement dial f (never chosen): {FS}")
    say(f"turnover instrument lambda (never chosen): {LAMBDAS}")
    say(f"books {BOOKS}; sleeves {SLEEVES} (ETF3={ETF3}); panels {PANELS}; rungs {RUNGS} bps; "
        f"weekly, t+1, gross {GROSS}; "
        f"IS <= {IS_END}, OOS >= {OOS_START}")

    panels = get_panels()
    if not gates(panels):
        say("\n*** GATES FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1

    C = census()
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    S = reprice_sites(C)
    if len(S):
        S.to_csv(OUT / f"{STEM}.sites.csv", index=False)

    say()
    say("=" * 100)
    say("LEG 4 — FRESH GRID (3 panels x 2 books x 2 sleeves x 8 lambdas x 11 f, read at 6 rungs)")
    say("=" * 100)
    G, SER, V2, BARS = [], {}, {}, {}
    for pk in PANELS:
        px, ndrop = panels[pk]
        g, ser, v2, bars = run_panel(pk, px, ndrop)
        G.append(g)
        SER.update(ser)
        V2[pk] = v2
        BARS[pk] = bars
    G = pd.concat(G, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    nsim = G[["panel", "book", "sleeve", "lam", "f"]].drop_duplicates().shape[0]
    say(f"\n  {len(G)} arm-rows written ({nsim} simulations x {len(RUNGS)} rungs).")

    # --- windows -------------------------------------------------------------------
    W = []
    for (pk, book, sleeve, lam, c), sub in G.groupby(["panel", "book", "sleeve", "lam", "cost"]):
        w = window_of(sub)
        base_to = float(sub.base_to.iloc[0])
        W.append(dict(panel=pk, book=book, sleeve=sleeve, lam=lam, cost=c, base_to=base_to,
                      drag=base_to * c / 1e4, **w,
                      best_margin=float(sub.m_min.max()),
                      binding=min(BARS5, key=lambda k: sub.loc[sub.m_min.idxmax(), "m_" + k])))
    W = pd.DataFrame(W)
    W.to_csv(OUT / f"{STEM}.windows.csv", index=False)

    say()
    say("-" * 100)
    say("H3 (SLOPE) — within-cell rho(width, drag) and rho(width, base_to)")
    say("-" * 100)
    say("  a 'cell' = (panel, book, sleeve); within it the two routes to drag are the RUNG (cost")
    say("  route: changes drag and nothing else) and LAMBDA (turnover route: drag AND the path).")
    say(f"  {'panel':>6} {'book':>6} {'sleeve':>7} {'rho(w,drag)':>12} {'rho(w,base_to)':>15} "
        f"{'rho@0bps(w,to)':>15} {'rho@25bps(w,to)':>16} {'mean w_pts':>11} {'range w':>8}")
    slope_rows = []
    for (pk, book, sl), sub in W.groupby(["panel", "book", "sleeve"]):
        rd = spearman(sub.w_pts.values, sub.drag.values)
        rt = spearman(sub.w_pts.values, sub.base_to.values)
        r0 = spearman(sub[sub.cost == 0].w_pts.values, sub[sub.cost == 0].base_to.values)
        r25 = spearman(sub[sub.cost == 25].w_pts.values, sub[sub.cost == 25].base_to.values)
        slope_rows.append(dict(panel=pk, book=book, sleeve=sl, rho_drag=rd, rho_to=rt,
                               rho0=r0, rho25=r25, mean_w=sub.w_pts.mean(),
                               rng=sub.w_pts.max() - sub.w_pts.min()))
        say(f"  {pk:>6} {book:>6} {sl:>7} {rd:>12.3f} {rt:>15.3f} {r0:>15.3f} {r25:>16.3f} "
            f"{sub.w_pts.mean():>11.3f} {sub.w_pts.max()-sub.w_pts.min():>8d}")
    SL = pd.DataFrame(slope_rows)
    SL = SL[SL.rng > 0]
    say(f"  ({len(slope_rows)-len(SL)} of {len(slope_rows)} cells are INERT — width constant "
        f"across the whole lambda x rung grid — and are excluded from the rho summary below,")
    say(f"   because a correlation with a constant is undefined, not zero.)")
    say(f"  --> rho(width, drag) over {len(SL)} cells: min {SL.rho_drag.min():+.3f}  "
        f"max {SL.rho_drag.max():+.3f}  median {SL.rho_drag.median():+.3f}")
    say(f"      403 quotes -0.854 .. -0.960 on its own (panel, book, sleeve) cells.")
    say(f"  --> the cost signature: median rho(width, base_to) at 0 bps "
        f"{SL.rho0.median():+.3f}  at 25 bps {SL.rho25.median():+.3f}")

    say()
    say("-" * 100)
    say("H4 (LEVEL) — the cross-cell ordering, pooled")
    say("-" * 100)
    for lab, sub in [("all rungs", W), ("@10 bps only", W[W.cost == 10]),
                     ("@0 bps only", W[W.cost == 0]), ("@25 bps only", W[W.cost == 25])]:
        say(f"  {lab:>14}: rho(width, base_to) {spearman(sub.w_pts.values, sub.base_to.values):+.3f}"
            f"   rho(width, drag) {spearman(sub.w_pts.values, sub.drag.values):+.3f}"
            f"   n={len(sub)}")
    say("  Under a PURE drag law the higher-turnover book must have the NARROWER window at any")
    say("  positive rung.  403 found the opposite on its grid, which is why turnover alone ranks")
    say("  width backwards.  Mean width and mean base turnover by cell:")
    for (pk, book, sl), sub in W.groupby(["panel", "book", "sleeve"]):
        say(f"    {pk:>6} {book:>6} {sl:>5}: base_to {sub.base_to.mean():7.2f} x/yr   "
            f"mean w_pts {sub.w_pts.mean():.3f}   empty {int(sub.is_empty.sum())}/{len(sub)}")
    for (pk, sl), sub in W.groupby(["panel", "sleeve"]):
        a, b = sub[sub.book == "TOP20"], sub[sub.book == "EWALL"]
        if not len(a) or not len(b):
            continue
        hi = "TOP20" if a.base_to.mean() > b.base_to.mean() else "EWALL"
        if a.w_pts.mean() == b.w_pts.mean():
            wide, tag = "TIE  ", "DEGENERATE (both windows empty everywhere - no content)"
        else:
            wide = "TOP20" if a.w_pts.mean() > b.w_pts.mean() else "EWALL"
            tag = ("403 SIGN: intercept runs OPPOSITE to turnover, so turnover alone ranks "
                   "width BACKWARDS" if hi == wide else
                   "drag-consistent: the cheaper book has the wider window")
        say(f"    {pk:>6} {sl:>5}: turnover ratio {a.base_to.mean()/max(b.base_to.mean(),1e-9):5.1f}x  "
            f"higher turnover = {hi:>5}   wider window = {wide:>5}   {tag}")

    say()
    say("-" * 100)
    say("H5 (THE ASK) — how many width-claim cells CHANGE RANK when re-priced on drag")
    say("-" * 100)
    say("  Algebra first: inside ONE rung, drag = base_to * c/1e4 is a positive affine map of")
    say("  base_to, so the ranking is IDENTICAL by construction.  A re-pricing can only move a")
    say("  ranking where the claim pools cells at DIFFERENT rungs.  The ladder is therefore the")
    say("  whole tuned parameter, and it is swept in full.")
    rk = []
    for lname, ladder in LADDERS.items():
        sub = W[W.cost.isin(ladder)]
        keys = list(range(len(sub)))
        rc = rank_change(sub.base_to.values, sub.drag.values, keys)
        rk.append(dict(ladder=lname, rungs=str(ladder), **rc,
                       rho_w_to=spearman(sub.w_pts.values, sub.base_to.values),
                       rho_w_drag=spearman(sub.w_pts.values, sub.drag.values)))
    RK = pd.DataFrame(rk)
    say(RK.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say()
    say("  Same question asked the way a reader would: which of the two orders PREDICTS width?")
    for lname, ladder in LADDERS.items():
        sub = W[W.cost.isin(ladder)]
        a = abs(spearman(sub.w_pts.values, sub.base_to.values))
        b = abs(spearman(sub.w_pts.values, sub.drag.values))
        say(f"    {lname:>3} {str(ladder):<28} |rho(w,to)| {a:.3f}   |rho(w,drag)| {b:.3f}   "
            f"--> {'DRAG' if b > a else 'TURNOVER'} is the better order")

    # --- KEEP paths ----------------------------------------------------------------
    say()
    say("-" * 100)
    say("KEEP PATHS (PROTOCOL 4) — both evaluated on EVERY arm-row")
    say("-" * 100)
    say(f"  4a (vs live RULES v2, cost-matched): {int(G.pass4a.sum())} / {len(G)}")
    say(f"  4b (vs SPY, all five bars)         : {int(G.pass4b.sum())} / {len(G)}")
    say(f"  BOTH                                : {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for c in RUNGS:
        s = G[G.cost == c]
        say(f"    @{c:>4.0f} bps: 4a {int(s.pass4a.sum()):>4}  4b {int(s.pass4b.sum()):>4}  "
            f"BOTH {int((s.pass4a & s.pass4b).sum()):>4}   of {len(s)}")
    for (pk, book, sl), s in G[G.cost == 10].groupby(["panel", "book", "sleeve"]):
        say(f"    {pk:>6} {book:>6} {sl:>5} @10 bps: 4a {int(s.pass4a.sum()):>3}  "
            f"4b {int(s.pass4b.sum()):>3}  of {len(s)}")

    # --- rule 8 --------------------------------------------------------------------
    say()
    say("-" * 100)
    say("RULE 8 (PROTOCOL 8) — (f, lambda) chosen on 2009-2016 ONLY, 2017-2026 read once")
    say("-" * 100)
    wf = []
    for pk in PANELS:
        px, _ = panels[pk]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        spy_o = spy.loc[OOS_START:]
        mo_spy = metrics(spy_o)
        bars_o = dict(s1=metrics(spy_o.iloc[:len(spy_o) // 2])["Sharpe"],
                      s2=metrics(spy_o.iloc[len(spy_o) // 2:])["Sharpe"],
                      sdd=mo_spy["MaxDD"], scagr=mo_spy["CAGR"], soos=mo_spy["Sharpe"])
        for (book, sl), sub0 in G[G.panel == pk].groupby(["book", "sleeve"]):
            for c in RUNGS:
                sub = sub0[sub0.cost == c]
                picks = {"S0_ISsharpe": sub.loc[sub.IS_Sharpe.idxmax()]}
                scr = sub[sub.IS_pass4b]
                picks["S1_IS4b"] = (scr.loc[scr.IS_Sharpe.idxmax()] if len(scr)
                                    else sub.loc[sub.IS_Sharpe.idxmax()])
                # the queue's own question, as a selector: rank the arms by the ARM's realised
                # turnover vs by its drag, and take the cheapest.  Inside one rung these must
                # agree except at c = 0, where drag is identically 0 and the order is UNDEFINED.
                picks["S2_minTO"] = sub.loc[sub.arm_to.idxmin()]
                picks["S3_minDRAG"] = sub.loc[(sub.arm_to * c / 1e4).idxmin()]
                for sname, p in picks.items():
                    r0, t0 = SER[(pk, book, sl, float(p.lam), float(p.f))]
                    r = (r0 - t0 * c / 1e4).loc[OOS_START:]
                    m = metrics(r)
                    h = len(r) // 2
                    o4b = dict(H1=metrics(r.iloc[:h])["Sharpe"] - bars_o["s1"],
                               H2=metrics(r.iloc[h:])["Sharpe"] - bars_o["s2"],
                               OOS=m["Sharpe"] - bars_o["soos"],
                               DD=DELTA * abs(bars_o["sdd"]) - abs(m["MaxDD"]),
                               CAGR=m["CAGR"] - PHI * bars_o["scagr"])
                    v2o = V2[pk][c].loc[OOS_START:]
                    mv = metrics(v2o)
                    wf.append(dict(panel=pk, book=book, sleeve=sl, cost=c, selector=sname,
                                   f=float(p.f), lam=float(p.lam),
                                   OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                                   SPY_CAGR=mo_spy["CAGR"], SPY_Sharpe=mo_spy["Sharpe"],
                                   SPY_MaxDD=mo_spy["MaxDD"],
                                   V2_CAGR=mv["CAGR"], V2_Sharpe=mv["Sharpe"], V2_MaxDD=mv["MaxDD"],
                                   beats_SPY=bool(m["Sharpe"] > mo_spy["Sharpe"]),
                                   beats_V2=bool(m["Sharpe"] > mv["Sharpe"]),
                                   OOS_4b=all(v > 0 for v in o4b.values()),
                                   OOS_4a=pass4a(r, v2o)))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.groupby("selector").agg(
        picks=("f", "size"), median_f=("f", "median"), median_lam=("lam", "median"),
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), beats_SPY=("beats_SPY", "sum"),
        beats_V2=("beats_V2", "sum"), OOS_4b=("OOS_4b", "sum"), OOS_4a=("OOS_4a", "sum")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    say()
    for pk in PANELS:
        s = WF[(WF.panel == pk) & (WF.cost == 10)]
        say(f"  {pk:>6} @10 bps  SPY OOS: CAGR {s.SPY_CAGR.iloc[0]:.2%}  Sharpe "
            f"{s.SPY_Sharpe.iloc[0]:.3f}  MaxDD {s.SPY_MaxDD.iloc[0]:.1%}   |   "
            f"RULES v2 OOS: CAGR {s.V2_CAGR.iloc[0]:.2%}  Sharpe {s.V2_Sharpe.iloc[0]:.3f}  "
            f"MaxDD {s.V2_MaxDD.iloc[0]:.1%}")
        for sn, g in s.groupby("selector"):
            say(f"          {sn:>12}: OOS CAGR {g.OOS_CAGR.mean():.2%}  Sharpe "
                f"{g.OOS_Sharpe.mean():.3f}  MaxDD {g.OOS_MaxDD.mean():.1%}  "
                f"4b {int(g.OOS_4b.sum())}/{len(g)}  4a {int(g.OOS_4a.sum())}/{len(g)}")
    say()
    dis = WF[WF.selector.isin(["S2_minTO", "S3_minDRAG"])].pivot_table(
        index=["panel", "book", "sleeve", "cost"], columns="selector", values=["f", "lam"])
    agree = ((dis[("f", "S2_minTO")] == dis[("f", "S3_minDRAG")]) &
             (dis[("lam", "S2_minTO")] == dis[("lam", "S3_minDRAG")]))
    say(f"  min-TURNOVER vs min-DRAG selector: identical pick in {int(agree.sum())}/{len(dis)} "
        f"cells.  They MUST agree inside a rung (positive affine map); the exceptions are")
    say(f"  exactly the {int((~agree).sum())} zero-rung cells, where drag is identically 0 and the "
        f"order is UNDEFINED, not different:")
    say(f"    disagreeing cells at cost>0: "
        f"{int((~agree & (agree.index.get_level_values('cost') > 0)).sum())}")

    say()
    say("=" * 100)
    say(f"done in {time.time() - T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
