#!/usr/bin/env python3
"""Idea 294 - "is-within-stratum-CORR-a-SECTOR-concentration-proxy" (lane C, 2026-09-06).

The question
------------
Idea 284 held capitalisation fixed (60 seeded k=40 panels, q = 0.5 = 20 small + 20 large)
and found that idea 271's four-characteristic vocabulary does NOT survive intact:

    breadth  -> zero within the stratum (rho +0.022/+0.028/+0.074, perm p 0.87/0.83/0.57)
    corr     -> SURVIVES but with the sign REVERSED (-0.365/-0.482/-0.471 within,
                +0.497/+0.586/+0.606 pooled)
    disp     -> survives, sign reversed
    evol     -> collapses to ~0 (mediated)

and that `S_CORR` (pick the panel with the LOWEST in-sample mean pairwise correlation) is the
only rule-8 selector in that run to beat the do-nothing anchor, SPY and RULES v2 out of
sample in both books.  What idea 284 could NOT say is WHAT within-stratum corr is.  Mean
pairwise correlation of a 40-name basket is mechanically lower when the basket is spread
across many sectors and higher when it piles into one.  If that is all it is, then "corr" is
a re-labelled SECTOR CONCENTRATION statistic, the surviving half of idea 271's vocabulary is
one more proxy, and S_CORR's OOS edge is a diversification effect that should be stated (and
implemented) as a sector cap, not as a correlation screen.

This run tags every panel with its sector Herfindahl and re-fits idea 284's within-stratum
corr -> OOS-Sharpe relation with and without the sector control.

Design
------
PANELS.  Rebuilt with idea 284's construction and seeds VERBATIM (same crc32 seed strings,
same pools, same common calendar), so the panels here are literally idea 284's panels and the
reproduction check below is an equality test, not a similarity test.
    MAIN     q = 0.500, 60 seeded draws, k = 40 (20 small from SMALL439 + 20 large from
             BSTK100).  The whole verdict is read INSIDE this stratum.
    ANCHORS  q = 0.000 and q = 1.000, 20 draws each - used only to report whether the
             pooled/within sign flip is itself a sector story.
    100 panels, every one reported.

SECTOR LABELS.  Two independent schemes, because neither alone is clean:

  ETFBETA (covers all 40 names of every panel).  Each name is assigned to whichever of the 9
    sector SPDRs priced across the whole IS window (XLK XLF XLV XLE XLI XLY XLP XLU XLB) its
    daily returns correlate most with, measured on 2009-01-01..2016-12-31 ONLY.  XLRE (first
    close 2015-10-08) and XLC (2018-06-19) do not exist over the IS window, so the taxonomy
    is the pre-2016 GICS sector scheme by construction, not by choice.
    CAVEAT, stated up front: this labeller is built FROM correlations, so it is biased
    TOWARDS the hypothesis under test (that corr is concentration).  If corr survives this
    control it survives strongly; if it dies under this control alone the reading is
    ambiguous, which is why scheme 2 exists.

  GICS (covers the 20 large names of every panel).  Hardcoded current-GICS sector for each of
    the 100 BSTK100 names - genuine sector identity, no return data of any kind enters it.
    Small caps have no sector field anywhere in the repo and the sandbox has no internet, so
    this scheme measures the Herfindahl of the large half only (20 names).  It is the
    non-circular check: it cannot be an artefact of the correlation matrix.

  For each scheme H = sum_i s_i^2 over sector shares s_i of the names it covers (H = 1/9 at
  perfectly even spread across 9 sectors, H = 1 at total concentration).  H is MEASURED, not
  tuned.

BOOKS.  Idea 284's, unchanged: RULES v1 gate (px > 200d MA AND vol20 < 0.60), composite score
without the vol scaler as the ranking key, top n equal weighted at 75% gross, weekly, 10 bps,
next-day execution; plus EWall (every eligible name), RULES v2 (the live book) and SPY.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. n           (2 values: 10, 20)          - the book's width
    2. label scheme(2 values: ETFBETA, GICS)   - which sector taxonomy defines H
    EWall is carried as a third, UNTUNED book (no n).  k = 40, q, the seeds, the gate, 75%
    gross, weekly cadence, 10 bps and next-day execution are idea 284's published conventions
    and are not tuned here.  ALL 2 x 2 (+EWall) grid points are reported, none selected on.

Rule 8 walk-forward (required; every direction pre-registered before any OOS number was read)
    IS = 2009-01-01..2016-12-31 chooses, OOS = 2017-01-01..end read ONCE.
    Inside q = 0.5, each selector picks ONE panel on an IS quantity and that panel's OOS book
    is read:
        S_CORR    LOWEST IS mean pairwise correlation      (idea 284's winner, reproduced)
        S_HERF    LOWEST IS sector Herfindahl              (the concentration analogue: if
                                                            corr IS concentration this must
                                                            reproduce S_CORR's edge)
        S_CORR|H  LOWEST IS corr AFTER removing H          (corr with the sector story taken
                                                            out - the decisive selector)
        S_HERF|C  LOWEST IS H AFTER removing corr          (the mirror residual)
        S_EWALL   highest IS EWall Sharpe                  (idea 271's winner, benchmark)
    Every selector's reverse extreme is reported as a sign check.  The do-nothing anchor is
    the MEAN OOS Sharpe over all 60 panels with its seed sd; SPY, RULES v2 and RULES v1 OOS
    are reported beside it.

Verdicts (both KEEP paths, on every grid point)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens; every panel
inherits the bias whole.  It moves the LEVEL of every panel's return.  The object here is
whether one panel statistic explains ANOTHER panel statistic's ordering power within a fixed
cap mix, and the bias is common to the stratum, so it does not manufacture the answer either
way.

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
Outputs: .panels.csv .cells.csv .fits.csv .walkforward.csv .console.txt
"""
import sys
import zlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, band_state
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
BAND_V2 = 0.03
K_MIX = 40
Q_MAIN = 0.500
Q_ANCHOR = [0.000, 1.000]
N_SEEDS_MAIN = 60
N_SEEDS_ANCHOR = 20
NS = [10, 20]
SCHEMES = ["ETFBETA", "GICS"]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
N_PERM = 20000

# The 9 sector SPDRs priced across the whole IS window.  XLRE (2015-10-08) and XLC
# (2018-06-19) do not exist over 2009-2016, so this IS the pre-2016 GICS sector set.
SECTOR_ETFS = ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB"]

# Current-GICS sector for every BSTK100 name.  Hardcoded identity: no price or return data
# enters this map.  Asserted complete against the live BSTK100 list at run time.
GICS = {
    # Information Technology
    "AAPL": "IT", "ACN": "IT", "ADBE": "IT", "ADI": "IT", "AMAT": "IT", "AMD": "IT",
    "ANET": "IT", "AVGO": "IT", "CRM": "IT", "CSCO": "IT", "IBM": "IT", "INTU": "IT",
    "KLAC": "IT", "LRCX": "IT", "MSFT": "IT", "MU": "IT", "NOW": "IT", "NVDA": "IT",
    "ORCL": "IT", "PANW": "IT", "PLTR": "IT", "QCOM": "IT", "TXN": "IT",
    # Financials (V/MA reclassified into Financials by GICS in March 2023)
    "AXP": "FIN", "BAC": "FIN", "BLK": "FIN", "BRK-B": "FIN", "C": "FIN", "CB": "FIN",
    "GS": "FIN", "ICE": "FIN", "JPM": "FIN", "MA": "FIN", "MMC": "FIN", "MS": "FIN",
    "PGR": "FIN", "SCHW": "FIN", "SPGI": "FIN", "V": "FIN", "WFC": "FIN",
    # Health Care
    "ABBV": "HC", "ABT": "HC", "AMGN": "HC", "BSX": "HC", "CI": "HC", "DHR": "HC",
    "GILD": "HC", "ISRG": "HC", "JNJ": "HC", "LLY": "HC", "MDT": "HC", "MRK": "HC",
    "PFE": "HC", "REGN": "HC", "SYK": "HC", "TMO": "HC", "UNH": "HC", "VRTX": "HC",
    "ZTS": "HC",
    # Consumer Discretionary
    "AMZN": "CD", "BKNG": "CD", "CMG": "CD", "HD": "CD", "LOW": "CD", "MCD": "CD",
    "SBUX": "CD", "TJX": "CD", "TSLA": "CD",
    # Consumer Staples
    "COST": "CS", "KO": "CS", "MDLZ": "CS", "MO": "CS", "PEP": "CS", "PG": "CS",
    "PM": "CS", "WMT": "CS",
    # Industrials (ADP and UBER reclassified into Industrials by GICS in March 2023)
    "ADP": "IND", "BA": "IND", "CAT": "IND", "DE": "IND", "ETN": "IND", "GE": "IND",
    "HON": "IND", "LMT": "IND", "RTX": "IND", "UBER": "IND", "UNP": "IND",
    # Communication Services
    "GOOGL": "COMM", "META": "COMM", "NFLX": "COMM", "T": "COMM",
    # Energy / Materials / Utilities / Real Estate
    "COP": "ENE", "CVX": "ENE", "XOM": "ENE",
    "LIN": "MAT", "SHW": "MAT",
    "DUK": "UTL", "NEE": "UTL", "SO": "UTL",
    "PLD": "RE",
}

OUT = Path(__file__).with_suffix("")
LOG = []

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 500)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def spearman(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 4:
        return np.nan, len(x)
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan, len(x)
    return float(np.corrcoef(rx, ry)[0, 1]), len(x)


def perm_p(x, y, seed=7):
    """Two-sided permutation p for Spearman under label exchangeability."""
    rho, n = spearman(x, y)
    if not np.isfinite(rho):
        return np.nan, np.nan, n
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    rx = pd.Series(x[ok]).rank().to_numpy()
    ry = pd.Series(y[ok]).rank().to_numpy()
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(N_PERM):
        if abs(float(np.corrcoef(rx, rng.permutation(ry))[0, 1])) >= abs(rho) - 1e-12:
            cnt += 1
    return rho, (cnt + 1) / (N_PERM + 1), n


def _resid_on(a, b):
    """Rank-residual of a on b (both rank-transformed): the partial-Spearman construction."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    ra = pd.Series(a).rank().to_numpy()
    rb = pd.Series(b).rank().to_numpy()
    rb = rb - rb.mean()
    if (rb ** 2).sum() == 0:
        return ra - ra.mean()
    beta = float((ra - ra.mean()) @ rb / (rb @ rb))
    return (ra - ra.mean()) - beta * rb


def partial_spearman(x, y, z, seed=11, n_perm=N_PERM):
    """Spearman(x, y | z) as the correlation of rank residuals, with a permutation p that
    shuffles the x-residual only (the standard exchangeability null for a partial)."""
    x, y, z = (np.asarray(v, float) for v in (x, y, z))
    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    x, y, z = x[ok], y[ok], z[ok]
    ex, ey = _resid_on(x, z), _resid_on(y, z)
    if ex.std() == 0 or ey.std() == 0:
        return np.nan, np.nan, len(x)
    rho = float(np.corrcoef(ex, ey)[0, 1])
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(n_perm):
        if abs(float(np.corrcoef(rng.permutation(ex), ey)[0, 1])) >= abs(rho) - 1e-12:
            cnt += 1
    return rho, (cnt + 1) / (n_perm + 1), len(x)


def ols(y, X):
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n, p = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    ss_res = float(e @ e)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    adj = 1 - (1 - r2) * (n - 1) / max(1, n - p)
    dof = max(1, n - p)
    se = np.sqrt(np.maximum(np.diag(XtXi * (ss_res / dof)), 0))
    t = np.where(se > 0, b / np.where(se > 0, se, 1), np.nan)
    return b, t, r2, adj, n


def z(s):
    s = pd.Series(np.asarray(s, float))
    sd = s.std()
    return ((s - s.mean()) / (sd if sd else 1.0)).to_numpy()


# ------------------------------------------------------------------ panels (idea 284 verbatim)
def build_sources():
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
    P(f"sources: BSTK{len(b_stk)} large-cap stocks, SMALL{len(s_stk)} small-cap stocks, "
      f"ETF{len(etf36)} ETFs")
    missing = [t for t in b_stk if t not in GICS]
    assert not missing, f"GICS map incomplete for {missing}"
    P(f"GICS map covers {len(b_stk)}/{len(b_stk)} BSTK names, "
      f"{len(set(GICS[t] for t in b_stk))} sectors: "
      + ", ".join(f"{s}:{sum(1 for t in b_stk if GICS[t] == s)}"
                  for s in sorted(set(GICS[t] for t in b_stk))))
    return px56, px136, pxs, etf36, b_stk, s_stk


def make_panel(px_small, px_large, small_names, large_names):
    parts = []
    if large_names:
        parts.append(px_large[large_names])
    if small_names:
        parts.append(px_small[small_names])
    p = pd.concat(parts, axis=1)
    p = pd.concat([p, px_large["SPY"].rename("SPY")], axis=1)
    return p.dropna(how="all").ffill(), set(small_names) | set(large_names)


def build_pool(px136, pxs, b_stk, s_stk):
    idx = pxs.index.intersection(px136.index)
    pxs_c = pxs.reindex(idx).ffill()
    pxb_c = px136.reindex(idx).ffill()
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days)")
    pool = {}
    small_pool = np.array(sorted(s_stk))
    large_pool = np.array(sorted(b_stk))
    plan = [(Q_MAIN, N_SEEDS_MAIN)] + [(q, N_SEEDS_ANCHOR) for q in Q_ANCHOR]
    for q, nseeds in plan:
        n_s = int(round(q * K_MIX))
        n_l = K_MIX - n_s
        for sd in range(nseeds):
            seed = zlib.crc32(f"STRAT|{q:.3f}|{sd}".encode()) % (2 ** 32)   # idea 284 verbatim
            rng = np.random.default_rng(seed)
            sc = sorted(rng.choice(small_pool, size=n_s, replace=False).tolist()) if n_s else []
            lc = sorted(rng.choice(large_pool, size=n_l, replace=False).tolist()) if n_l else []
            p, t = make_panel(pxs_c, pxb_c, sc, lc)
            pool[f"q{q:.3f}~s{sd:02d}"] = dict(px=p, tradable=t, kind=f"Q{q:.3f}", q=q,
                                               seed=sd, k=len(t),
                                               small=sc, large=lc)
    return pool, pxs_c, pxb_c


# ------------------------------------------------------------------ sector labels
def etfbeta_labels(pxs_c, pxb_c, s_stk, b_stk):
    """Assign every tradable name to the IS-window-max-correlation sector SPDR.  Measured on
    2009-01-01..2016-12-31 only; ties broken by SECTOR_ETFS order (deterministic)."""
    etf_r = pxb_c[SECTOR_ETFS].pct_change().loc[IS_START:IS_END]
    lab, qual = {}, {}
    for src, names in ((pxb_c, b_stk), (pxs_c, s_stk)):
        r = src[names].pct_change().loc[IS_START:IS_END]
        for t in names:
            a = r[t]
            ok = a.notna()
            if ok.sum() < 250:                    # <1yr of IS overlap -> UNK, reported
                lab[t], qual[t] = "UNK", np.nan
                continue
            cs = {e: a.corr(etf_r[e]) for e in SECTOR_ETFS}
            best = max(SECTOR_ETFS, key=lambda e: (-1e9 if not np.isfinite(cs[e]) else cs[e]))
            lab[t], qual[t] = best, cs[best]
    return lab, qual


def herfindahl(names, labels):
    lab = [labels.get(t, "UNK") for t in names]
    lab = [l for l in lab if l != "UNK"]
    if not lab:
        return np.nan, 0, 0
    s = pd.Series(lab).value_counts() / len(lab)
    return float((s ** 2).sum()), int(s.size), len(lab)


# ------------------------------------------------------------------ books (idea 284 verbatim)
def eligible_mask(px, tradable):
    _, above, vol20 = score(px, vol_scale=False)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def book_weights(px, tradable, arm, n=None):
    key, above, vol20 = score(px, vol_scale=False)
    elig = eligible_mask(px, tradable)
    if arm == "v1":
        s_v1, _, _ = score(px, vol_scale=True)
        rank = s_v1.where(elig).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if arm == "v2":
        e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        for c in px.columns:
            if c in tradable:
                e[c] = px[c].notna().astype(float)
        ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND_V2), 0.0)
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        rank = key.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def stat_block(r):
    h = len(r) // 2
    m = metrics(r)
    out = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
               H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
    out["IS_Sharpe"] = metrics(ris)["Sharpe"] if len(ris) > 60 else np.nan
    mo = metrics(ros) if len(ros) > 60 else dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    out["OOS_CAGR"], out["OOS_Sharpe"], out["OOS_MaxDD"] = mo["CAGR"], mo["Sharpe"], mo["MaxDD"]
    return out


def keep_flags(row, spy_row, v2_row):
    a = bool(row["H1"] > v2_row["H1"] and row["H2"] > v2_row["H2"]
             and row["MaxDD"] >= v2_row["MaxDD"])
    fails = []
    if not row["H1"] > spy_row["H1"]: fails.append("H1")
    if not row["H2"] > spy_row["H2"]: fails.append("H2")
    if not row["OOS_Sharpe"] > spy_row["OOS_Sharpe"]: fails.append("OOS")
    if not abs(row["MaxDD"]) <= 0.60 * abs(spy_row["MaxDD"]): fails.append("DD")
    if not row["CAGR"] >= 0.70 * spy_row["CAGR"]: fails.append("CAGR")
    return a, (len(fails) == 0), (",".join(fails) if fails else "-")


def panel_corr(px, tradable, lo, hi):
    """idea 271/277's `corr`: mean off-diagonal pairwise correlation of daily returns."""
    cols = [c for c in px.columns if c in tradable]
    idx = px.loc[px.index[260]:].index
    idx = idx[idx >= pd.Timestamp(lo)]
    if hi:
        idx = idx[idx <= pd.Timestamp(hi)]
    dr = px[cols].pct_change().loc[idx]
    C = dr.corr().to_numpy()
    k = len(cols)
    iu = np.triu_indices(k, 1)
    return float(np.nanmean(C[iu])) if k > 1 else np.nan


def panel_breadth_disp_evol(px, tradable, elig, lo, hi):
    cols = [c for c in px.columns if c in tradable]
    m = rebalance_mask(px.index, FREQ)
    idx = px.loc[px.index[260]:].index
    idx = idx[idx >= pd.Timestamp(lo)]
    if hi:
        idx = idx[idx <= pd.Timestamp(hi)]
    rb = idx[m.reindex(idx).fillna(False).values]
    e = elig.loc[rb, cols]
    k = len(cols)
    nel = e.sum(axis=1)
    breadth = float((nel / k).mean())
    r63 = (px[cols] / px[cols].shift(63) - 1).loc[rb]
    disp = float(r63.where(e).std(axis=1, ddof=0).mean())
    vol20 = (px[cols].pct_change().rolling(20).std() * np.sqrt(252)).loc[rb]
    evol = float(vol20.where(e).mean(axis=1).mean())
    return breadth, disp, evol, float(nel.median())


# ------------------------------------------------------------------ main
def main():
    px56, px136, pxs, etf36, b_stk, s_stk = build_sources()
    pool, pxs_c, pxb_c = build_pool(px136, pxs, b_stk, s_stk)
    P(f"pool: {len(pool)} panels "
      f"({sum(1 for v in pool.values() if v['kind'] == 'Q0.500')} at q=0.5, "
      f"{sum(1 for v in pool.values() if v['kind'] != 'Q0.500')} anchors)")

    P("\n=== SECTOR LABELLING ===")
    etf_lab, etf_q = etfbeta_labels(pxs_c, pxb_c, s_stk, b_stk)
    nunk = sum(1 for t in list(s_stk) + list(b_stk) if etf_lab.get(t, "UNK") == "UNK")
    P(f"ETFBETA: {len(etf_lab) - nunk} of {len(etf_lab)} names labelled from IS-window "
      f"correlation with {len(SECTOR_ETFS)} sector SPDRs ({nunk} UNK: <250 IS observations).")
    lc = pd.Series({t: etf_lab[t] for t in b_stk}).value_counts()
    sc = pd.Series({t: etf_lab[t] for t in s_stk}).value_counts()
    P("  large-cap assignment counts: " + ", ".join(f"{k}:{v}" for k, v in lc.items()))
    P("  small-cap assignment counts: " + ", ".join(f"{k}:{v}" for k, v in sc.items()))

    # quality of the correlation labeller, checked against hardcoded GICS on the large half
    ETF2G = {"XLK": "IT", "XLF": "FIN", "XLV": "HC", "XLE": "ENE", "XLI": "IND",
             "XLY": "CD", "XLP": "CS", "XLU": "UTL", "XLB": "MAT"}
    comparable = [t for t in b_stk if etf_lab[t] != "UNK" and GICS[t] in set(ETF2G.values())]
    agree = sum(1 for t in comparable if ETF2G[etf_lab[t]] == GICS[t])
    P(f"  labeller quality: ETFBETA agrees with hardcoded GICS on {agree}/{len(comparable)} "
      f"= {agree / len(comparable):.1%} of large-cap names whose GICS sector has an SPDR "
      f"(chance ~ {1 / 9:.1%}).  COMM/RE names have no IS-window SPDR and are excluded here.")
    P(f"  mean IS correlation with the assigned SPDR: large "
      f"{np.nanmean([etf_q[t] for t in b_stk]):.3f}, small "
      f"{np.nanmean([etf_q[t] for t in s_stk]):.3f}")

    # ------------------------------------------------------------- per panel
    prows, crows = [], []
    for i, (name, meta) in enumerate(pool.items(), 1):
        px, tr = meta["px"], meta["tradable"]
        elig = eligible_mask(px, tr)
        names = sorted(tr)
        h_etf, ns_etf, cov_etf = herfindahl(names, etf_lab)
        h_gics, ns_gics, cov_gics = herfindahl(names, GICS)          # large half only
        h_etf_L, _, _ = herfindahl(meta["large"], etf_lab)           # ETFBETA on the same
        corr_is = panel_corr(px, tr, IS_START, IS_END)               #   20 names GICS sees
        corr_oos = panel_corr(px, tr, OOS_START, None)
        br, dp, ev, nel = panel_breadth_disp_evol(px, tr, elig, IS_START, IS_END)

        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_row = stat_block(spy_r)
        books = {}
        for arm, n in [("EWall", None), ("CAND10", 10), ("CAND20", 20), ("v1", None), ("v2", None)]:
            w = book_weights(px, tr, "CAND" if arm.startswith("CAND") else arm, n=n)
            r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
            books[arm] = stat_block(r)
        v2_row = books["v2"]

        rec = dict(panel=name, kind=meta["kind"], q=meta["q"], seed=meta["seed"], k=meta["k"],
                   n_elig_IS=nel, corr_IS=corr_is, corr_OOS=corr_oos,
                   breadth_IS=br, disp_IS=dp, evol_IS=ev,
                   H_ETFBETA=h_etf, nsec_ETFBETA=ns_etf, cov_ETFBETA=cov_etf,
                   H_GICS=h_gics, nsec_GICS=ns_gics, cov_GICS=cov_gics,
                   H_ETFBETA_large=h_etf_L)
        for arm in ("EWall", "CAND10", "CAND20", "v1", "v2"):
            b = books[arm]
            a, bk, fails = keep_flags(b, spy_row, v2_row)
            crows.append(dict(panel=name, kind=meta["kind"], q=meta["q"], seed=meta["seed"],
                              arm=arm, H_ETFBETA=h_etf, H_GICS=h_gics, corr_IS=corr_is,
                              **{k: b[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                   "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
                                                   "OOS_MaxDD")},
                              keep4a=a, keep4b=bk, fails4b=fails))
            for f in ("IS_Sharpe", "OOS_Sharpe", "Sharpe", "CAGR", "MaxDD", "H1", "H2",
                      "OOS_CAGR", "OOS_MaxDD"):
                rec[f"{arm}_{f}"] = b[f]
        for f in ("Sharpe", "OOS_Sharpe", "CAGR", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_MaxDD"):
            rec[f"SPY_{f}"] = spy_row[f]
        prows.append(rec)
        if i % 10 == 0 or i == len(pool):
            P(f"  ... {i}/{len(pool)} panels")

    panels = pd.DataFrame(prows)
    cells = pd.DataFrame(crows)
    panels.to_csv(f"{OUT}.panels.csv", index=False)
    cells.to_csv(f"{OUT}.cells.csv", index=False)

    # ------------------------------------------------------------- reproduction of idea 284
    P("\n=== REPRODUCTION CHECK vs idea 284 (same seeds -> must be the same panels) ===")
    ref = REPO / "research" / "backtests" / \
        "2026-09-06_does-any-panel-property-separate-at-FIXED-cap-mix_C.panels.csv"
    if ref.exists():
        r284 = pd.read_csv(ref).set_index("panel")
        mine = panels.set_index("panel")
        common = [p for p in mine.index if p in r284.index]
        chk = []
        for col in ("corr_IS", "breadth_IS", "disp_IS", "evol_IS",
                    "CAND10_OOS_Sharpe", "CAND20_OOS_Sharpe", "EWall_OOS_Sharpe",
                    "CAND20_Sharpe", "SPY_OOS_Sharpe"):
            if col in r284.columns:
                d = (mine.loc[common, col] - r284.loc[common, col]).abs()
                chk.append(dict(field=col, n=len(common), max_abs_diff=float(d.max()),
                                mean_abs_diff=float(d.mean())))
        P(fmt(pd.DataFrame(chk).set_index("field"), 8))
    else:
        P("  idea 284 panels.csv not found - reproduction check skipped.")

    main_s = panels[panels.kind == f"Q{Q_MAIN:.3f}"].copy()
    a0 = panels[panels.kind == "Q0.000"].copy()
    a1 = panels[panels.kind == "Q1.000"].copy()

    P("\n=== HERFINDAHL BY STRATUM (H = sum of squared sector shares) ===")
    hs = []
    for tag, d in [("q=0.0 (all large)", a0), ("q=0.5 (20+20)", main_s), ("q=1.0 (all small)", a1)]:
        hs.append(dict(stratum=tag, n=len(d),
                       H_ETF_mean=d.H_ETFBETA.mean(), H_ETF_sd=d.H_ETFBETA.std(),
                       H_ETF_min=d.H_ETFBETA.min(), H_ETF_max=d.H_ETFBETA.max(),
                       nsec_ETF=d.nsec_ETFBETA.mean(),
                       H_GICS_mean=d.H_GICS.mean(), H_GICS_sd=d.H_GICS.std(),
                       cov_GICS=d.cov_GICS.mean(),
                       corr_mean=d.corr_IS.mean(), corr_sd=d.corr_IS.std()))
    P(fmt(pd.DataFrame(hs).set_index("stratum")))
    P(f"  (even spread over 9 sectors would give H = {1/9:.4f}; one sector gives H = 1.0)")

    # ------------------------------------------------------------- Q1: is corr = H ?
    P("\n=== Q1: is within-stratum corr the same statistic as sector concentration? ===")
    q1 = []
    for lbl, col in (("ETFBETA (all 40)", "H_ETFBETA"), ("ETFBETA (large 20)", "H_ETFBETA_large"),
                     ("GICS (large 20)", "H_GICS")):
        r_w, p_w, n_w = perm_p(main_s.corr_IS, main_s[col])
        r_p, p_p, n_p = perm_p(panels.corr_IS, panels[col])
        q1.append(dict(scheme=lbl, rho_corr_vs_H_within=r_w, p_within=p_w, n_within=n_w,
                       rho_corr_vs_H_pooled=r_p, p_pooled=p_p, n_pooled=n_p))
    P(fmt(pd.DataFrame(q1).set_index("scheme")))
    P("  If corr were a re-labelled concentration statistic this would be strongly POSITIVE\n"
      "  (more concentrated basket -> higher mean pairwise correlation) and large.")

    # ------------------------------------------------------------- Q2: the controlled re-fit
    P("\n=== Q2: corr -> OOS Sharpe, WITH and WITHOUT the sector control (q=0.5 only) ===")
    fits = []
    for arm in ("CAND10", "CAND20", "EWall"):
        y = main_s[f"{arm}_OOS_Sharpe"]
        r0, p0, n0 = perm_p(main_s.corr_IS, y)
        for lbl, col in (("H_ETFBETA", "H_ETFBETA"), ("H_ETFBETA_large", "H_ETFBETA_large"),
                         ("H_GICS", "H_GICS")):
            rH, pH, _ = perm_p(main_s[col], y)
            rp, pp, npn = partial_spearman(main_s.corr_IS, y, main_s[col])
            rHp, pHp, _ = partial_spearman(main_s[col], y, main_s.corr_IS)
            fits.append(dict(book=arm, control=lbl, n=n0,
                             rho_corr_raw=r0, p_corr_raw=p0,
                             rho_H_raw=rH, p_H_raw=pH,
                             rho_corr_given_H=rp, p_corr_given_H=pp,
                             rho_H_given_corr=rHp, p_H_given_corr=pHp,
                             shrink=(abs(rp) / abs(r0) if r0 else np.nan)))
    fdf = pd.DataFrame(fits)
    fdf.to_csv(f"{OUT}.fits.csv", index=False)
    P(fmt(fdf.set_index(["book", "control"])))
    P("  'shrink' = |partial rho| / |raw rho|.  ~1.0 = the sector control explains none of\n"
      "  corr's ordering power; ~0.0 = corr IS the concentration statistic.")

    P("\nOLS inside the stratum (z-scored regressors), corr alone vs corr + H:")
    orows = []
    for arm in ("CAND10", "CAND20", "EWall"):
        d = main_s.dropna(subset=[f"{arm}_OOS_Sharpe"])
        y = d[f"{arm}_OOS_Sharpe"].to_numpy()
        b1, t1, r21, a1_, n1 = ols(y, np.column_stack([np.ones(len(d)), z(d.corr_IS)]))
        for lbl, col in (("H_ETFBETA", "H_ETFBETA"), ("H_GICS", "H_GICS")):
            b2, t2, r22, a2_, _ = ols(y, np.column_stack([np.ones(len(d)), z(d.corr_IS),
                                                          z(d[col])]))
            orows.append(dict(book=arm, control=lbl, n=n1,
                              b_corr_alone=b1[1], t_corr_alone=t1[1], R2_alone=r21,
                              b_corr_ctrl=b2[1], t_corr_ctrl=t2[1],
                              b_H_ctrl=b2[2], t_H_ctrl=t2[2], R2_ctrl=r22,
                              dR2=r22 - r21))
    P(fmt(pd.DataFrame(orows).set_index(["book", "control"])))

    P("\nSplit-half by seed (seeds 0-29 vs 30-59), corr partialled on H_ETFBETA:")
    srows = []
    for arm in ("CAND10", "CAND20", "EWall"):
        for lbl, d in (("seeds 00-29", main_s[main_s.seed < 30]),
                       ("seeds 30-59", main_s[main_s.seed >= 30])):
            raw, _ = spearman(d.corr_IS, d[f"{arm}_OOS_Sharpe"])
            pr, _, nn = partial_spearman(d.corr_IS, d[f"{arm}_OOS_Sharpe"], d.H_ETFBETA,
                                         n_perm=2000)
            prg, _, _ = partial_spearman(d.corr_IS, d[f"{arm}_OOS_Sharpe"], d.H_GICS,
                                         n_perm=2000)
            srows.append(dict(book=arm, half=lbl, n=nn, rho_raw=raw,
                              rho_given_H_ETF=pr, rho_given_H_GICS=prg))
    P(fmt(pd.DataFrame(srows).set_index(["book", "half"])))

    # ------------------------------------------------------------- Q3: rule 8 walk-forward
    P("\n=== Rule 8 WALK-FORWARD inside q=0.5 (directions pre-registered) ===")
    d0 = main_s.copy()
    d0["corr_resid_ETF"] = _resid_on(d0.corr_IS, d0.H_ETFBETA)
    d0["corr_resid_GICS"] = _resid_on(d0.corr_IS, d0.H_GICS)
    d0["H_resid_ETF"] = _resid_on(d0.H_ETFBETA, d0.corr_IS)
    d0["H_resid_GICS"] = _resid_on(d0.H_GICS, d0.corr_IS)
    SEL = [
        ("S_CORR",      "corr_IS",         "min", "LOWEST IS mean pairwise corr (idea 284)"),
        ("S_HERF_ETF",  "H_ETFBETA",       "min", "LOWEST IS sector Herfindahl (ETFBETA)"),
        ("S_HERF_GICS", "H_GICS",          "min", "LOWEST IS sector Herfindahl (GICS)"),
        ("S_CORR|H_ETF", "corr_resid_ETF", "min", "LOWEST IS corr AFTER removing H (ETFBETA)"),
        ("S_CORR|H_GICS", "corr_resid_GICS", "min", "LOWEST IS corr AFTER removing H (GICS)"),
        ("S_H|CORR_ETF", "H_resid_ETF",    "min", "LOWEST IS H AFTER removing corr (ETFBETA)"),
        ("S_EWALL",     "EWall_IS_Sharpe", "max", "highest IS EWall Sharpe (idea 271 winner)"),
    ]
    wf = []
    for arm in ("CAND10", "CAND20"):
        d = d0.dropna(subset=[f"{arm}_OOS_Sharpe"]).copy()
        anchor = d[f"{arm}_OOS_Sharpe"].mean()
        anchor_sd = d[f"{arm}_OOS_Sharpe"].std()
        best = d[f"{arm}_OOS_Sharpe"].max()
        spy_oos = d["SPY_OOS_Sharpe"].mean()
        v2_oos = d["v2_OOS_Sharpe"].mean()
        v1_oos = d["v1_OOS_Sharpe"].mean()
        sels = list(SEL) + [("S_ISS", f"{arm}_IS_Sharpe", "max", "highest IS Sharpe of the book")]
        for nm, col, direction, desc in sels:
            for lbl, dr in ((nm, direction), (nm + "^rev", "min" if direction == "max" else "max")):
                pick = d.loc[d[col].idxmax() if dr == "max" else d[col].idxmin()]
                _, kb, fails = keep_flags(
                    {k: pick[f"{arm}_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                    {k: pick[f"SPY_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                    {k: pick[f"v2_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")})
                pct = float((d[f"{arm}_OOS_Sharpe"] <= pick[f"{arm}_OOS_Sharpe"]).mean())
                wf.append(dict(book=arm, rule=lbl, prereg=desc if lbl == nm else "sign check",
                               pick=pick["panel"], IS_Sharpe=pick[f"{arm}_IS_Sharpe"],
                               OOS_CAGR=pick[f"{arm}_OOS_CAGR"],
                               OOS_Sharpe=pick[f"{arm}_OOS_Sharpe"],
                               OOS_MaxDD=pick[f"{arm}_OOS_MaxDD"], pctile=pct,
                               vs_anchor=pick[f"{arm}_OOS_Sharpe"] - anchor,
                               vs_SPY=pick[f"{arm}_OOS_Sharpe"] - spy_oos,
                               vs_v2=pick[f"{arm}_OOS_Sharpe"] - v2_oos,
                               regret=best - pick[f"{arm}_OOS_Sharpe"],
                               keep4b=kb, fails4b=fails))
        wf.append(dict(book=arm, rule="ANCHOR (do nothing: mean of 60)", prereg="control",
                       pick="-", IS_Sharpe=d[f"{arm}_IS_Sharpe"].mean(),
                       OOS_CAGR=d[f"{arm}_OOS_CAGR"].mean(), OOS_Sharpe=anchor,
                       OOS_MaxDD=d[f"{arm}_OOS_MaxDD"].mean(), pctile=np.nan, vs_anchor=0.0,
                       vs_SPY=anchor - spy_oos, vs_v2=anchor - v2_oos, regret=best - anchor,
                       keep4b=False, fails4b="n/a (mean)"))
        P(f"\n[{arm}]  anchor OOS Sharpe {anchor:.4f} (seed sd {anchor_sd:.4f}, best {best:.4f});"
          f"  SPY OOS {spy_oos:.4f}   RULES v2 OOS {v2_oos:.4f}   RULES v1 OOS {v1_oos:.4f}")
    wfdf = pd.DataFrame(wf)
    wfdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\n" + fmt(wfdf.set_index(["book", "rule"]).drop(columns=["prereg"])))

    P("\nSelector edge over the do-nothing anchor, pre-registered directions only:")
    prime = wfdf[~wfdf.rule.str.endswith("^rev") & ~wfdf.rule.str.startswith("ANCHOR")]
    P(fmt(prime.pivot_table(index="rule", columns="book", values="vs_anchor")))
    P("\nDid the sector selectors pick the SAME panels as S_CORR?")
    pk = prime.pivot_table(index="rule", columns="book", values="pick", aggfunc="first")
    P(pk.to_string())

    # ------------------------------------------------------------- KEEP paths
    P("\n=== KEEP PATHS over every grid cell (all reported) ===")
    kp = cells.groupby(["kind", "arm"]).agg(n=("keep4a", "size"), keep4a=("keep4a", "sum"),
                                            keep4b=("keep4b", "sum"),
                                            OOS_Sharpe=("OOS_Sharpe", "mean"),
                                            Sharpe=("Sharpe", "mean"), CAGR=("CAGR", "mean"),
                                            MaxDD=("MaxDD", "mean"))
    P(fmt(kp))
    passes = cells[cells.keep4b]
    P(f"\n4b passes: {len(passes)} of {len(cells)} cells;  "
      f"4a passes: {int(cells.keep4a.sum())} of {len(cells)}.")
    if len(passes):
        P(fmt(passes.sort_values("OOS_Sharpe", ascending=False)
              [["panel", "kind", "arm", "H_ETFBETA", "H_GICS", "corr_IS", "CAGR", "Sharpe",
                "MaxDD", "H1", "H2", "OOS_Sharpe", "keep4a"]].head(40)
              .set_index(["panel", "arm"])))
        st = passes[passes.kind == f"Q{Q_MAIN:.3f}"]
        P(f"\n4b passes inside q=0.5: {len(st)} of "
          f"{len(cells[cells.kind == f'Q{Q_MAIN:.3f}'])} stratum cells.")
        P("Do 4b passers differ in sector concentration?  (mean of passers vs non-passers)")
        for arm in ("CAND10", "CAND20", "EWall"):
            sa = st[st.arm == arm]
            if not len(sa):
                continue
            dd = main_s.copy()
            dd["pass"] = dd.panel.isin(set(sa.panel))
            P(f"  [{arm}] {len(set(sa.panel))} passers / {len(dd)}")
            P(fmt(dd.groupby("pass")[["H_ETFBETA", "H_GICS", "corr_IS", "breadth_IS",
                                      f"{arm}_OOS_Sharpe"]].mean()))

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {OUT.name}.panels.csv .cells.csv .fits.csv .walkforward.csv .console.txt")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
