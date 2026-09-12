#!/usr/bin/env python3
"""Idea 846 - is the TIE CONVENTION doing the work in every committed TWIN WIN RATE?
   (lane C, 2026-09-12)

QUESTION (QUEUE idea 846, verbatim)
    Idea 843 found the same 108 arms on the same leg give a PRE win rate of 0.7778 under FULLMATCH
    and exactly 0.0000 under WINMATCH, because an inert arm TIES its win-matched twin and the
    record scores a tie as a loss.  Re-price the record's committed twin win rates with ties scored
    three ways (loss, win, excluded) and report which published orderings survive all three.
    Max 2 params (tie rule, claim set).

WHAT THE RECORD ACTUALLY COMMITTED
    Every committed twin verdict in this repository is the single expression

        win = (dSharpe > TIE),      TIE = 1e-12

    i.e. a STRICT inequality with a tolerance twelve orders of magnitude below any number the
    record prints.  That expression makes three separate decisions at once, and the record has
    only ever documented the first:
        (a) which comparand (the matched-gross twin) - documented everywhere;
        (b) which tolerance (1e-12) - stated in code, never in a memo;
        (c) what to do with a TIE (book it a LOSS) - never stated anywhere.
    (c) is invisible while ties are rare and decisive when they are not.  Ties are NOT rare here:
    a gate that never fires in a window makes m == 1 on every day of that window, so under
    WINMATCH its gross-matched twin is the ungated EWALL book the arm already IS - the two paths
    are the SAME ARRAY, dSharpe is exactly 0.0, and `win = dSharpe > 1e-12` returns False.  The
    record therefore scores "this arm was identical to its control" as "this arm LOST to its
    control".  Ideas 824 and 826 each hit this from one direction (714 of 717 convention flips,
    99.60% of 235,615 sign flips); 843 hit its extreme (0.7778 -> 0.0000 on one leg).  This run
    asks the general question: across EVERY committed win column in the repository and across a
    rebuilt twin corpus, how much of each published win rate is the tie convention?

TUNED PARAMETERS: TWO, exactly the two the queue names.  3 x 3 = 9 points, ALL reported.
    (1) TIE RULE, the scoring of a cell with |d| <= eps:
          LOSS      win = d >  eps                     <- THE RECORD'S OWN, and the HEADLINE,
                                                          declared before anything is computed
          WIN       win = d >= -eps
          EXCLUDED  rate = mean(d > 0 | |d| > eps)     <- ties leave the denominator
    (2) CLAIM SET, which committed win columns are re-priced (three NESTED sets):
          ALL       every (win column, matched delta column) pair in every committed .csv[.gz]
          TWIN      the subset whose comparand is a MATCHED-GROSS TWIN  <- HEADLINE, declared
          HEADLINE  the subset whose rate a sibling .memo.md / .result.md actually quotes
    Everything else is a REPORTED AXIS, printed at every grid point and never chosen:
      eps ladder {0, 1e-12 (the record's), 1e-9, 1e-6, 1e-4, 1e-3}; cost rung {0, 10, 25} bps;
      panel {U56, B136, SMALL}; claim window {FULL, IS, OOS}; matching {FULLMATCH, WINMATCH}.

PRE-REGISTERED HYPOTHESES (stated before any number is read; every one is reported either way)
    H1  TIE SHARE IS MATERIAL.  >= 10% of cells in the TWIN claim set are ties at the record's own
        eps on at least one committed claim window.
    H2  THE RECORD'S FLAGSHIP IS SAFE.  The canonical FULL-sample FULLMATCH win column has a tie
        share < 1%, so the record's most-quoted twin number does not move.
    H3  AN ORDERING REVERSES.  At least one published family ordering (QROLL / QEXP / ABS) differs
        between two tie rules on a committed claim set.
    H4  TIES ARE THE CONVENTION GAP.  Under EXCLUDED the FULLMATCH-vs-WINMATCH win-rate gap falls
        below 0.05 at the headline cell (824/826 found this for one number; test it generally).
    H5  EXACTNESS.  Every WINMATCH tie is an EXACT tie: the never-firing arm's net path and its
        exactly-run WINMATCH twin are the same array, max|d| == 0.0, not merely small.
    H6  RULE 8 ON THE CLAIM.  The tie share measured on 2009-2016 predicts the tie share on
        2017-2026 to within 0.10.
    H7  RULE 8 ON THE BOOKS.  The tie rule changes which arm a twin-win selector picks in >= 10%
        of cells, and therefore changes the OOS book it hands a reader.
    H8  843 REPRODUCES.  The 0.7778 -> 0.0000 collapse rebuilds, and under EXCLUDED the two
        conventions agree on that leg.

GATES (all must PASS before any re-pricing is read)
    G1  fast_run == engine.backtest                                  max|d| < 1e-9
    G2  fast metrics == engine.metrics                               max|d| < 1e-9
    G3  0.01 gross-grid interpolation vs an exact twin run           |dSharpe| < 1e-6
    G4  the committed twin corpus rebuilds (dSharpe and win)         drift bar 6e-3, flips counted.
        REQUIRED on U56 only: the record has already documented that `data/prices_broad.csv` and
        `data/prices_small.csv.gz` are re-cached weekly/nightly and that the committed corpus was
        built on SMALL439 against today's SMALL663 (ideas 609 G4b, 825, 843).  B136 and SMALL are
        REPORTED with their drift and flip counts and are never tolerated into a PASS.
    G5  INERTNESS IDENTITY: a never-firing arm's net path IS its WINMATCH twin's, bit-for-bit.
        Measured against an EXACT gross run (G5a, the identity) and against the 0.01 interpolation
        grid the record's twin is actually built on (G5b, which carries an endpoint artefact).
    G6  the three tie rules coincide EXACTLY wherever the tie count is 0

OUTPUTS (nothing outside research/backtests/ is written)
    .console.txt    the full log
    .census.csv     every committed win column re-priced under 3 tie rules x 6 eps
    .grid.csv       the 9 tuned points x every reported axis
    .orderings.csv  every family ordering under every tie rule, and whether it survives all three
    .arms.csv       the rebuilt arm corpus (price leg)
    .walkforward.csv  the rule-8 picks under each tie rule and their OOS reads vs RULES v2 and SPY
    .result.md      the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
"""
from __future__ import annotations

import gzip
import re
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-12"
SLUG = "is-the-TIE-CONVENTION-doing-the-work-in-every-committed-TWIN-WIN-RATE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
BT = Path(__file__).resolve().parent

FREQ = "W"
LAG = 1
MAX_VOL = 0.60
WARMUP = 260
GROSSES = [0.75, 1.00]
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS_ROLL = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
MINQ = 252
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
RECORD_TIE = 1e-12                       # the tolerance every committed `win` column uses
SMALL_MAXMOVE = 1.0
FAMS = ["ABS", "QEXP", "QROLL"]
GSTEP = 0.01
PANELS = ["U56", "B136", "SMALL"]
PANEL_MAP = {"U56": "U56", "B136": "B136", "SMALL": "SMALL439"}

# --- the two tuned dials -----------------------------------------------------------------
TIE_RULES = ["LOSS", "WIN", "EXCLUDED"]          # headline LOSS (the record's own)
TIE_HEAD = "LOSS"
CLAIM_SETS = ["ALL", "TWIN", "HEADLINE"]         # headline TWIN
SET_HEAD = "TWIN"
# --- reported axes -----------------------------------------------------------------------
EPS_LADDER = [0.0, 1e-12, 1e-9, 1e-6, 1e-4, 1e-3]
WINDOWS = ["FULL", "IS", "OOS"]
CONVS = ["FULLMATCH", "WINMATCH"]

CELLS = BT / "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.cells.csv.gz"

# a win column's comparand is the matched-gross TWIN if its name is one of these.  Built by
# reading the header of every committed csv (below); this is the classifier, declared up front.
TWIN_WIN_COLS = {"win", "win_IS", "win_OOS", "win_F", "win_W", "win_602", "win_605",
                 "mg_win", "win_CAGR_TWIN", "win_Sharpe_TWIN", "win_MaxDD_TWIN"}
# win column -> the delta column that defines it, tried in order
DELTA_FOR = {
    "win": ["dSharpe", "dSharpe_F", "dOOS"],
    "win_IS": ["dSharpe_IS", "dIS"],
    "win_OOS": ["dSharpe_OOS", "dOOS"],
    "win_F": ["dSharpe_F"], "win_W": ["dSharpe_W"],
    "win_602": ["dSharpe_602"], "win_605": ["dSharpe_605"],
    "mg_win": ["mg_dSharpe", "dOOS"],
    "LEV_win": ["LEV_dSharpe", "dOOS"],
    "win_CAGR_CTRL": ["dCAGR_vs_CTRL"], "win_CAGR_TWIN": ["dCAGR_vs_TWIN"],
    "win_CAGR_PLACEBO": ["dCAGR_vs_PLACEBO"], "win_CAGR_EWALL": ["dCAGR_vs_EWALL"],
    "win_Sharpe_CTRL": ["dSharpe_vs_CTRL"], "win_Sharpe_TWIN": ["dSharpe_vs_TWIN"],
    "win_Sharpe_PLACEBO": ["dSharpe_vs_PLACEBO"], "win_Sharpe_EWALL": ["dSharpe_vs_EWALL"],
    "win_MaxDD_CTRL": ["dMaxDD_vs_CTRL"], "win_MaxDD_TWIN": ["dMaxDD_vs_TWIN"],
    "win_MaxDD_PLACEBO": ["dMaxDD_vs_PLACEBO"], "win_MaxDD_EWALL": ["dMaxDD_vs_EWALL"],
}

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ the tie algebra
def rates(d, eps):
    """Win rate for one delta array under all three tie rules at tolerance eps."""
    d = np.asarray(d, dtype=float)
    d = d[np.isfinite(d)]
    n = len(d)
    if n == 0:
        return dict(n=0, n_tie=0, tie_share=np.nan, LOSS=np.nan, WIN=np.nan, EXCLUDED=np.nan,
                    spread=np.nan)
    tie = np.abs(d) <= eps
    nt = int(tie.sum())
    r_loss = float((d > eps).mean())
    r_win = float((d >= -eps).mean())
    r_ex = float((d[~tie] > 0).mean()) if nt < n else np.nan
    vals = [v for v in (r_loss, r_win, r_ex) if np.isfinite(v)]
    return dict(n=n, n_tie=nt, tie_share=nt / n, LOSS=r_loss, WIN=r_win, EXCLUDED=r_ex,
                spread=float(max(vals) - min(vals)))


# ------------------------------------------------------------------ runner (596/604/824's)
def fast_run(prices, weights, mask, lag=LAG):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx))


def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross, elig):
    e = elig.astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def _cadence(m, idx):
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def gate_series(br, thr, depth, cadence, idx):
    below = (br < thr)
    m = pd.Series(1.0, index=idx).where(~below, 1.0 - depth)
    ok = br.notna() & (thr.notna() if isinstance(thr, pd.Series) else True)
    m = m.where(ok, 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def panel_prices(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= SMALL_MAXMOVE, "ticker"])
        drop = [c for c in px.columns if c in bad and c != "SPY"]
        px = px.drop(columns=drop)
        P(f"   SMALL panel today: dropped {len(drop)} names with max_1d_move >= {SMALL_MAXMOVE}, "
          f"{len([c for c in px.columns if c != 'SPY'])} tradable")
    return px.dropna(how="all").ffill()


# =================================================================== PART A: the census
def read_header(f):
    op = gzip.open if f.name.endswith(".gz") else open
    with op(f, "rt") as fh:
        return [c.strip() for c in fh.readline().strip().split(",")]


def census():
    """Re-price every committed (win column, delta column) pair in research/backtests/."""
    files = sorted([p for p in BT.glob("*.csv")] + [p for p in BT.glob("*.csv.gz")])
    rows, quoted_cache = [], {}
    n_scanned = 0
    for f in files:
        if f.name.startswith(f"{DATE}_{SLUG}"):
            continue                                    # never census our own output
        try:
            cols = read_header(f)
        except Exception:
            continue
        n_scanned += 1
        pairs = []
        for wc in cols:
            if not (wc == "win" or wc.startswith("win_") or wc.endswith("_win")):
                continue
            for dc in DELTA_FOR.get(wc, []):
                if dc in cols:
                    pairs.append((wc, dc))
                    break
        if not pairs:
            continue
        try:
            df = pd.read_csv(f, usecols=sorted({c for p in pairs for c in p}
                                               | ({"family"} if "family" in cols else set())))
        except Exception as e:                          # unreadable committed artefact
            P(f"   [skip] {f.name}: {e}")
            continue
        # does a sibling memo/result quote this column's rate?  (the HEADLINE claim set)
        if f.name not in quoted_cache:
            txt = ""
            stem = f.name.split(".")[0]
            for sib in BT.glob(f"{stem}.*"):
                if sib.suffix in (".md", ".txt"):
                    try:
                        txt += sib.read_text(errors="ignore")
                    except Exception:
                        pass
            quoted_cache[f.name] = txt
        txt = quoted_cache[f.name]
        for wc, dc in pairs:
            d = pd.to_numeric(df[dc], errors="coerce").values
            base = rates(d, RECORD_TIE)
            if base["n"] == 0:
                continue
            # is the committed column literally `d > TIE`?  (verifies the convention is LOSS)
            w_pub = df[wc]
            if w_pub.dtype == object:
                w_pub = w_pub.astype(str).str.strip().str.lower().isin(["true", "1"])
            wp = np.asarray(w_pub, dtype=bool)
            ok = np.isfinite(d)
            agree = float((wp[ok] == (d[ok] > RECORD_TIE)).mean())
            pub_rate = float(wp[ok].mean())
            r4 = f"{base['LOSS']:.4f}"
            r3 = f"{base['LOSS']:.3f}"
            r2 = f"{base['LOSS']:.1%}"
            quoted = bool(r4 in txt or r3 in txt or r2 in txt)
            row = dict(file=f.name, win_col=wc, delta_col=dc, n=base["n"],
                       published_rate=pub_rate, is_loss_convention=agree,
                       twin=bool(wc in TWIN_WIN_COLS), quoted=quoted,
                       has_family=bool("family" in df.columns))
            for e in EPS_LADDER:
                r = rates(d, e)
                tag = "0" if e == 0 else f"{e:g}"
                row[f"tie_{tag}"] = r["tie_share"]
                for tr in TIE_RULES:
                    row[f"{tr}_{tag}"] = r[tr]
                row[f"spread_{tag}"] = r["spread"]
            rows.append(row)
    C = pd.DataFrame(rows)
    return C, n_scanned


def set_mask(C, cs):
    if cs == "ALL":
        return pd.Series(True, index=C.index)
    if cs == "TWIN":
        return C.twin
    return C.twin & C.quoted


# =================================================================== main
def main():
    T0 = time.time()
    P(f"# Idea 846 - {SLUG}  (lane C, {DATE})")
    P("# OBJECT: every committed twin verdict in this repository is `win = dSharpe > 1e-12`, a")
    P("#   strict inequality that books an EXACT TIE as a LOSS.  Ties are not rare: a gate that")
    P("#   never fires in a window makes its WINMATCH twin the same array as the arm.")
    P(f"# TUNED: tie rule {TIE_RULES} x claim set {CLAIM_SETS} = "
      f"{len(TIE_RULES)*len(CLAIM_SETS)} points, ALL reported; HEADLINE = "
      f"({TIE_HEAD}, {SET_HEAD}), declared before anything is computed.")
    P(f"# REPORTED AXES: eps {EPS_LADDER}; rungs {RUNGS} bps (head {RUNG_HEAD:g}); panels "
      f"{PANELS}; windows {WINDOWS}; matching {CONVS}.")
    P("# SURVIVORSHIP: all three panels are CURRENT-constituent lists; levels optimistic, SMALL")
    P("#   worst.  Nothing here is a live-capital claim.")

    # ================= PART A - the committed census ==================================
    P(f"\n{'='*118}\nPART A - CENSUS of every committed win column in research/backtests/"
      f"\n{'='*118}")
    C, n_scanned = census()
    C.to_csv(f"{OUT}.census.csv", index=False)
    P(f"   {n_scanned} committed csv/csv.gz headers scanned; {len(C)} (win column, delta column) "
      f"pairs re-priced over {C.file.nunique()} files, {int(C.n.sum())} cells.")
    conv = C.is_loss_convention
    P(f"   is the committed convention LOSS?  `win == (d > 1e-12)` holds on "
      f"{int((conv > 0.9999).sum())} of {len(C)} columns "
      f"(min agreement {conv.min():.4f}, mean {conv.mean():.4f}).")
    P(f"   claim sets: ALL {int(set_mask(C,'ALL').sum())}, TWIN {int(set_mask(C,'TWIN').sum())}, "
      f"HEADLINE {int(set_mask(C,'HEADLINE').sum())} columns.")

    P(f"\n   {'claim set':<9} {'tie rule':<9} {'cols':>5} {'cells':>9} {'tie share':>10} "
      f"{'pooled rate':>12} {'vs LOSS':>9} {'cols moved':>11} {'max move':>9}")
    grid = []
    for cs in CLAIM_SETS:
        s = C[set_mask(C, cs)]
        tot = int(s.n.sum())
        tie_pool = float((s[f"tie_{RECORD_TIE:g}"] * s.n).sum() / tot) if tot else np.nan
        base_pool = float((s[f"LOSS_{RECORD_TIE:g}"] * s.n).sum() / tot) if tot else np.nan
        for tr in TIE_RULES:
            col = f"{tr}_{RECORD_TIE:g}"
            if tr == "EXCLUDED":
                nn = s.n * (1 - s[f"tie_{RECORD_TIE:g}"])
                ok = s[col].notna() & (nn > 0)
                pool = float((s.loc[ok, col] * nn[ok]).sum() / nn[ok].sum()) if ok.any() else np.nan
            else:
                pool = float((s[col] * s.n).sum() / tot) if tot else np.nan
            mv = (s[col] - s[f"LOSS_{RECORD_TIE:g}"]).abs()
            grid.append(dict(claim_set=cs, tie_rule=tr, n_cols=len(s), n_cells=tot,
                             tie_share=tie_pool, pooled_rate=pool, d_vs_LOSS=pool - base_pool,
                             cols_moved=int((mv > 1e-9).sum()), max_col_move=float(mv.max())
                             if len(s) else np.nan, headline=bool(cs == SET_HEAD
                                                                  and tr == TIE_HEAD)))
            g = grid[-1]
            P(f"   {cs:<9} {tr:<9} {g['n_cols']:>5} {g['n_cells']:>9} {tie_pool:>10.4f} "
              f"{pool:>12.4f} {g['d_vs_LOSS']:>+9.4f} {g['cols_moved']:>11} "
              f"{g['max_col_move']:>9.4f}" + ("   <- HEADLINE" if g["headline"] else ""))

    # the eps ladder on the headline claim set
    s = C[set_mask(C, SET_HEAD)]
    P(f"\n   eps ladder on the {SET_HEAD} claim set (pooled over {int(s.n.sum())} cells):")
    P(f"   {'eps':>8} {'tie share':>10} {'LOSS':>8} {'WIN':>8} {'EXCLUDED':>9} {'spread':>8}")
    for e in EPS_LADDER:
        tag = "0" if e == 0 else f"{e:g}"
        tot = int(s.n.sum())
        line = [float((s[f"{tr}_{tag}"].fillna(0) * s.n).sum() / tot) for tr in TIE_RULES]
        P(f"   {tag:>8} {float((s[f'tie_{tag}']*s.n).sum()/tot):>10.4f} {line[0]:>8.4f} "
          f"{line[1]:>8.4f} {line[2]:>9.4f} {max(line)-min(line):>8.4f}")

    # the worst offenders
    w = C[set_mask(C, "TWIN")].copy()
    w["move"] = (w[f"WIN_{RECORD_TIE:g}"] - w[f"LOSS_{RECORD_TIE:g}"]).abs()
    w = w.sort_values("move", ascending=False)
    P(f"\n   the 12 committed TWIN win columns whose rate moves most between LOSS and WIN:")
    P(f"   {'move':>7} {'tie':>7} {'LOSS':>7} {'WIN':>7} {'EXCL':>7} {'n':>7}  quoted  file.column")
    for _, r in w.head(12).iterrows():
        P(f"   {r['move']:>7.4f} {r[f'tie_{RECORD_TIE:g}']:>7.4f} "
          f"{r[f'LOSS_{RECORD_TIE:g}']:>7.4f} {r[f'WIN_{RECORD_TIE:g}']:>7.4f} "
          f"{(r[f'EXCLUDED_{RECORD_TIE:g}'] if np.isfinite(r[f'EXCLUDED_{RECORD_TIE:g}']) else float('nan')):>7.4f} "
          f"{int(r['n']):>7}  {str(r['quoted']):<6}  {r['file']}.{r['win_col']}")

    H1 = bool(float((s[f"tie_{RECORD_TIE:g}"] * s.n).sum() / s.n.sum()) >= 0.10)
    P(f"\n   H1 (tie share >= 10% of the TWIN claim set at the record's eps): "
      f"{'PASS' if H1 else 'FAIL'}")

    # ================= PART B - the price leg ==========================================
    P(f"\n{'='*118}\nPART B - REBUILD the twin corpus and re-price its ORDERINGS\n{'='*118}")
    old = pd.read_csv(CELLS)
    old = old[old.family.isin(FAMS)].copy()
    P(f"   committed corpus {CELLS.name}: {len(old)} cells, "
      f"{old.panel.nunique()} panels x {old.arm.nunique()} arms x {old.rung.nunique()} rungs")

    cellrows, armrows, wfrows = [], [], []
    G5a_max, G5b_max, G5_n = 0.0, 0.0, 0

    for pname in PANELS:
        P(f"\n{'-'*118}\nPANEL {pname}\n{'-'*118}")
        px = panel_prices(pname)
        idx = px.index
        start = idx[WARMUP]
        eidx = px.loc[start:].index
        T = len(eidx)
        mask = rebalance_mask(idx, FREQ)
        elig = eligible_mask(px)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:].values
        P(f"   {px.shape[1]-1} tradable names, {T} scored days "
          f"{eidx[0].date()}..{eidx[-1].date()}")

        br_full = breadth(px)
        thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
        thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q)
                    for q in QS for w in WS_ROLL}

        base0 = {}
        for g in GROSSES:
            rg, tn = fast_run(px, ewall_weights(px, g, elig), mask)
            base0[g] = (rg.loc[start:].values, tn.loc[start:].values)
        gg = np.round(np.arange(0.0, 1.0 + GSTEP / 2, GSTEP), 6)
        GR = np.zeros((len(gg), T))
        GT = np.zeros((len(gg), T))
        for i, x in enumerate(gg):
            if x == 0.0:
                continue
            rg, tn = fast_run(px, ewall_weights(px, float(x), elig), mask)
            GR[i], GT[i] = rg.loc[start:].values, tn.loc[start:].values

        if pname == "U56":
            P(f"\n{'-'*118}\nGATES G1-G3\n{'-'*118}")
            Wb = ewall_weights(px, 0.75, elig)
            rg, tn = fast_run(px, Wb, mask)
            eng = backtest(px, Wb, cost_bps=10, freq=FREQ)
            g1 = float(np.abs(((rg - tn * 10 / 1e4) - eng["returns"]).loc[start:].values).max())
            P(f"   G1 fast_run == engine.backtest                  max|d| {g1:.3e} "
              f"{'PASS' if g1 < 1e-9 else 'FAIL'}")
            assert g1 < 1e-9
            ser = pd.Series((rg - tn * 10 / 1e4).loc[start:].values)
            m = metrics(ser)
            fc, fs, fd = fmet(ser.values)
            g2 = max(abs(fc - m["CAGR"]), abs(fs - m["Sharpe"]), abs(fd - m["MaxDD"]))
            P(f"   G2 fast metrics == engine.metrics               max|d| {g2:.3e} "
              f"{'PASS' if g2 < 1e-9 else 'FAIL'}")
            assert g2 < 1e-9
            xt = 0.6237
            lo = int(np.floor(round(xt, 6) / GSTEP))
            lam = (xt - gg[lo]) / GSTEP
            ex_r, ex_t = fast_run(px, ewall_weights(px, xt, elig), mask)
            en = (ex_r - ex_t * 10 / 1e4).loc[start:].values
            inn = ((1 - lam) * (GR[lo] - GT[lo] * 10 / 1e4)
                   + lam * (GR[lo + 1] - GT[lo + 1] * 10 / 1e4))
            g3 = abs(fsharpe(en) - fsharpe(inn))
            P(f"   G3 0.01-grid interpolation vs an EXACT twin run |dSharpe| {g3:.3e} "
              f"{'PASS' if g3 < 1e-6 else 'FAIL'}")
            assert g3 < 1e-6

        h = T // 2
        is_end = int(eidx.searchsorted(pd.Timestamp(IS_END), side="right"))
        oos0 = int(eidx.searchsorted(pd.Timestamp(OOS_START), side="left"))
        SPANS = {"FULL": (0, T), "IS": (0, is_end), "OOS": (oos0, T)}
        P("   claim windows: " + "  ".join(
            f"{k} {eidx[a].date()}..{eidx[b-1].date()} n={b-a}" for k, (a, b) in SPANS.items()))

        arms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
                + [("QROLL", q, w) for q in QS for w in WS_ROLL])
        keys, ME, ARM, GEFF_FULL = [], [], {c: [] for c in RUNGS}, []
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            thr = lev if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
            m = gate_series(br_full, thr, d, cad, idx)
            me = m.reindex(eidx).shift(1).fillna(1.0).values
            sw = np.abs(np.diff(me, prepend=me[0]))
            for g in GROSSES:
                r0, t0 = base0[g]
                keys.append((fam, lev, w, d, cad, g))
                ME.append(me)
                GEFF_FULL.append(g * float(me.mean()))
                for c in RUNGS:
                    ARM[c].append(me * r0 - (me * t0 + g * sw) * c / 1e4)
        K = len(keys)
        ME = np.asarray(ME)
        GEFF_FULL = np.asarray(GEFF_FULL)
        P(f"   {K} arms built")

        NET = {c: np.asarray(ARM[c]) for c in RUNGS}
        TNET = {c: GR - GT * c / 1e4 for c in RUNGS}

        def twin_path(c, g_eff):
            lo = int(np.clip(np.floor(round(float(g_eff), 6) / GSTEP), 0, len(gg) - 2))
            lam = (g_eff - gg[lo]) / GSTEP
            return (1 - lam) * TNET[c][lo] + lam * TNET[c][lo + 1]

        # ---- G5: the inertness identity ----------------------------------------------
        # A never-firing arm has m == 1 on every day of the window, so its WINMATCH twin is the
        # ungated EWALL book at the arm's own gross.  G5a compares it to that book run EXACTLY
        # (base0[g], no interpolation); G5b to the 0.01 interpolation grid the record's twin is
        # actually built on.
        for c in RUNGS:
            A = NET[c]
            for i in range(K):
                g = keys[i][5]
                r0, t0 = base0[g]
                exact = r0 - t0 * c / 1e4
                for wn, (a, b) in SPANS.items():
                    if float(ME[i, a:b].mean()) < 1.0 - 1e-12:
                        continue
                    tw = twin_path(c, g * float(ME[i, a:b].mean()))[a:b]
                    G5a_max = max(G5a_max, float(np.abs(A[i, a:b] - exact[a:b]).max()))
                    G5b_max = max(G5b_max, float(np.abs(A[i, a:b] - tw).max()))
                    G5_n += 1

        # ---- per-cell re-pricing under both conventions, every window ----------------
        for c in RUNGS:
            A = NET[c]
            for i in range(K):
                fam, lev, w, d, cad, g = keys[i]
                tf_full = twin_path(c, GEFF_FULL[i])
                for wn, (a, b) in SPANS.items():
                    ra = A[i, a:b]
                    mm = float(ME[i, a:b].mean())
                    tw = twin_path(c, g * mm)[a:b]
                    tf = tf_full[a:b]
                    sa = fsharpe(ra)
                    cellrows.append(dict(
                        panel=pname, rung=c, family=fam, level=lev, w=w, depth=d, cadence=cad,
                        gross=g, window=wn, n_days=b - a, on_share=mm,
                        neverfire=bool(mm >= 1.0 - 1e-12),
                        dSharpe_FULLMATCH=sa - fsharpe(tf), dSharpe_WINMATCH=sa - fsharpe(tw)))

        # ---- full-sample arm table + rule-8 machinery --------------------------------
        sc, ss, sd_ = fmet(spy)
        spy_pack = (fsharpe(spy[:h]), fsharpe(spy[h:]), fsharpe(spy[oos0:]), sd_, sc)
        v2rg, v2tn = fast_run(px, rules_v2_weights(px), mask)
        v2rg, v2tn = v2rg.loc[start:].values, v2tn.loc[start:].values
        v1rg, v1tn = fast_run(px, rules_v1_weights(px), mask)
        v1rg, v1tn = v1rg.loc[start:].values, v1tn.loc[start:].values
        P(f"   SPY {sc:.2%} / {ss:.3f} / {sd_:.2%};  4b bars: CAGR floor {0.70*sc:.2%}, DD cap "
          f"{-0.60*abs(sd_):.2%}, halves {spy_pack[0]:.3f}/{spy_pack[1]:.3f}, "
          f"OOS {spy_pack[2]:.3f}")
        for c in RUNGS:
            v2 = v2rg - v2tn * c / 1e4
            b1, b2, bdd = fsharpe(v2[:h]), fsharpe(v2[h:]), fmet(v2)[2]
            A = NET[c]
            for i in range(K):
                fam, lev, w, d, cad, g = keys[i]
                ra = A[i]
                tfull = twin_path(c, GEFF_FULL[i])
                mm_is = float(ME[i, :is_end].mean())
                t_is_W = twin_path(c, g * mm_is)[:is_end]
                ca, sa, da = fmet(ra)
                oc, os_, od = fmet(ra[oos0:])
                ct, st, dt = fmet(tfull)
                t4b = dict(H1=fsharpe(ra[:h]) > spy_pack[0], H2=fsharpe(ra[h:]) > spy_pack[1],
                           OOS=os_ > spy_pack[2], DD=abs(da) <= 0.60 * abs(sd_),
                           CAGR=ca >= 0.70 * sc)
                sis = fsharpe(ra[:is_end])
                armrows.append(dict(
                    panel=pname, rung=c, family=fam, level=lev, w=w, depth=d, cadence=cad,
                    gross=g, arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}",
                    g_eff=GEFF_FULL[i], on_share_IS=mm_is,
                    CAGR=ca, Sharpe=sa, MaxDD=da, H1=fsharpe(ra[:h]), H2=fsharpe(ra[h:]),
                    IS_Sharpe=sis, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                    twin_Sharpe=st, dSharpe=sa - st,
                    dIS_FULLMATCH=sis - fsharpe(tfull[:is_end]),
                    dIS_WINMATCH=sis - fsharpe(t_is_W),
                    win=bool(sa - st > RECORD_TIE),
                    pass_4a=bool(fsharpe(ra[:h]) > b1 and fsharpe(ra[h:]) > b2 and da >= bdd),
                    pass_4b=all(t4b.values()),
                    fail_4b="+".join(k for k, v in t4b.items() if not v) or "-none-",
                    SPY_CAGR=sc, SPY_Sharpe=ss, SPY_MaxDD=sd_,
                    SPY_OOS_CAGR=fmet(spy[oos0:])[0], SPY_OOS_Sharpe=spy_pack[2],
                    SPY_OOS_MaxDD=fmet(spy[oos0:])[2],
                    V2_OOS_CAGR=fmet(v2[oos0:])[0], V2_OOS_Sharpe=fsharpe(v2[oos0:]),
                    V2_OOS_MaxDD=fmet(v2[oos0:])[2], V2_Sharpe=fsharpe(v2),
                    V1_Sharpe=fsharpe(v1rg - v1tn * c / 1e4)))
        del px, GR, GT, ARM

    CE = pd.DataFrame(cellrows)
    AR = pd.DataFrame(armrows)
    AR.to_csv(f"{OUT}.arms.csv", index=False)
    P(f"\n   {len(CE)} twin cells rebuilt, {len(AR)} arm rows")

    P(f"\n   G5 INERTNESS IDENTITY over {G5_n} never-firing (arm, window, rung) cells:")
    P(f"      G5a vs an EXACTLY RUN twin at the arm's gross   max|d| {G5a_max:.3e}  "
      f"{'PASS' if G5a_max == 0.0 else 'FAIL'}   (H5)")
    P(f"      G5b vs the record's 0.01 INTERPOLATION grid     max|d| {G5b_max:.3e}  "
      f"{'PASS' if G5b_max < 1e-15 else 'FAIL'}")
    P(f"      G5b's residual is the g=1.00 endpoint of the interpolation "
      f"((1-lam) = -8.9e-16 there); it is {RECORD_TIE/max(G5b_max,1e-300):.3g}x below the "
      f"record's own 1e-12 tie tolerance, so it moves no verdict.")
    H5 = bool(G5a_max == 0.0)

    # ---- G4 reproduction of the committed corpus ----------------------------------
    P(f"\n{'-'*118}\nG4 REPRODUCTION of the committed twin corpus\n{'-'*118}")
    JK = ["family", "level", "w", "depth", "cadence", "gross"]

    def norm(d):
        d = d.copy()
        d["level"] = d.level.astype(float).round(6)
        d["w"] = d.w.astype(float).round(0).astype(int)
        d["depth"] = d.depth.astype(float).round(6)
        d["gross"] = d.gross.astype(float).round(6)
        return d

    ARn, oldn = norm(AR), norm(old)
    P("   PASS bar: max|d dSharpe| < 6e-3 (idea 406's known data/prices.csv re-download drift);")
    P("   verdict flips are COUNTED, never tolerated into the bar.  The gate is REQUIRED on U56,")
    P("   the one panel whose cache the record has not documented as re-written: `prices_broad.csv`")
    P("   is re-cached weekly and the committed corpus's SMALL panel is SMALL439 against today's")
    P("   SMALL663 (ideas 609 G4b, 825, 843).  B136/SMALL drift is REPORTED, never tolerated.")
    P(f"   {'panel':<6} {'rung':>5} {'n':>5} {'win flips':>9} {'max|d dSharpe|':>14}  "
      f"{'required':>8}  verdict")
    g4ok = True
    for pn, opn in PANEL_MAP.items():
        for c in RUNGS:
            a = ARn[(ARn.panel == pn) & (ARn.rung == c)].set_index(JK)
            o = oldn[(oldn.panel == opn) & (oldn.rung == c)].set_index(JK)
            j = a[["dSharpe", "win"]].join(o[["dSharpe", "win"]], how="inner",
                                           lsuffix="_new", rsuffix="_old")
            if j.empty:
                continue
            md = float((j.dSharpe_new - j.dSharpe_old).abs().max())
            fl = int((j.win_new != j.win_old).sum())
            req = pn == "U56"
            v = ("PASS" if md < 6e-3 else "FAIL") if req else \
                ("reproduces" if md < 6e-3 else "CACHE DRIFT (documented)")
            if req:
                g4ok &= md < 6e-3
            P(f"   {pn:<6} {c:>5.0f} {len(j):>5} {fl:>9} {md:>14.3e}  "
              f"{str(req):>8}  {v}")
    P(f"   G4 (U56, required) {'PASS' if g4ok else 'FAIL'}")
    assert g4ok, "G4 failed on the one panel whose cache is unchanged"

    # ---- G6: the three rules coincide where there are no ties --------------------
    d0 = CE.dSharpe_FULLMATCH.values
    notie = np.abs(d0) > RECORD_TIE
    r_all = rates(d0[notie], RECORD_TIE)
    g6 = max(abs(r_all["LOSS"] - r_all["EXCLUDED"]), abs(r_all["WIN"] - r_all["EXCLUDED"]))
    P(f"\n   G6 three tie rules coincide on the tie-free subpopulation "
      f"({int(notie.sum())} cells): max|d| {g6:.3e}  {'PASS' if g6 < 1e-12 else 'FAIL'}")

    # ================= PART C - the orderings ========================================
    P(f"\n{'='*118}\nPART C - do the published FAMILY ORDERINGS survive all three tie rules?"
      f"\n{'='*118}")
    ordrows = []
    for pn, c, wn, cv in product(PANELS, RUNGS, WINDOWS, CONVS):
        s = CE[(CE.panel == pn) & (CE.rung == c) & (CE.window == wn)]
        if s.empty:
            continue
        col = f"dSharpe_{cv}"
        per = {}
        for tr in TIE_RULES:
            fr = {}
            for fam in FAMS:
                fr[fam] = rates(s.loc[s.family == fam, col].values, RECORD_TIE)[tr]
            per[tr] = fr
        orders = {tr: ">".join(sorted(FAMS, key=lambda f: (-per[tr][f] if np.isfinite(per[tr][f])
                                                           else 1e9, f))) for tr in TIE_RULES}
        surv = len(set(orders.values())) == 1
        ordrows.append(dict(panel=pn, rung=c, window=wn, matching=cv,
                            tie_share=float(rates(s[col].values, RECORD_TIE)["tie_share"]),
                            **{f"{tr}_{fam}": per[tr][fam] for tr in TIE_RULES for fam in FAMS},
                            **{f"order_{tr}": orders[tr] for tr in TIE_RULES},
                            survives_all_three=surv))
    OD = pd.DataFrame(ordrows)
    OD.to_csv(f"{OUT}.orderings.csv", index=False)
    P(f"   {len(OD)} (panel x rung x window x matching) ordering cells")
    P(f"   ORDERINGS THAT SURVIVE ALL THREE TIE RULES: {int(OD.survives_all_three.sum())} of "
      f"{len(OD)} ({OD.survives_all_three.mean():.4f})")
    for cv in CONVS:
        s = OD[OD.matching == cv]
        P(f"     {cv:<10} {int(s.survives_all_three.sum())} of {len(s)} "
          f"({s.survives_all_three.mean():.4f}),  mean tie share {s.tie_share.mean():.4f}")
    for wn in WINDOWS:
        s = OD[OD.window == wn]
        P(f"     window {wn:<5} {int(s.survives_all_three.sum())} of {len(s)} "
          f"({s.survives_all_three.mean():.4f})")
    H3 = bool((~OD.survives_all_three).any())
    P(f"   H3 (at least one published ordering differs between tie rules): "
      f"{'PASS' if H3 else 'FAIL'}")

    P(f"\n   the headline cell ({RUNG_HEAD:g} bps), every panel x window x matching:")
    P(f"   {'panel':<6} {'window':<5} {'match':<10} {'tie':>7} | "
      + " ".join(f"{tr[:4]}:{f[:5]:<5}" for tr in TIE_RULES for f in FAMS) + " | survives")
    for _, r in OD[OD.rung == RUNG_HEAD].iterrows():
        cells = " ".join(f"{r[f'{tr}_{f}']:.3f}" if np.isfinite(r[f"{tr}_{f}"]) else "  nan"
                         for tr in TIE_RULES for f in FAMS)
        P(f"   {r.panel:<6} {r.window:<5} {r.matching:<10} {r.tie_share:>7.4f} | {cells} | "
          f"{'YES' if r.survives_all_three else 'NO  ->  ' + ' / '.join(sorted(set(r[f'order_{t}'] for t in TIE_RULES)))}")

    # H4: the convention gap under each tie rule, headline cell
    P(f"\n   H4 - the FULLMATCH-vs-WINMATCH win-rate gap under each tie rule "
      f"({RUNG_HEAD:g} bps, pooled over panels):")
    P(f"   {'window':<7} {'tie share F':>12} {'tie share W':>12} " +
      " ".join(f"{tr:>10}" for tr in TIE_RULES))
    H4 = True
    for wn in WINDOWS:
        s = CE[(CE.rung == RUNG_HEAD) & (CE.window == wn)]
        rf = {tr: rates(s.dSharpe_FULLMATCH.values, RECORD_TIE)[tr] for tr in TIE_RULES}
        rw = {tr: rates(s.dSharpe_WINMATCH.values, RECORD_TIE)[tr] for tr in TIE_RULES}
        gaps = {tr: rf[tr] - rw[tr] for tr in TIE_RULES}
        if wn == "OOS" and np.isfinite(gaps["EXCLUDED"]):
            H4 = bool(abs(gaps["EXCLUDED"]) < 0.05)
        P(f"   {wn:<7} {rates(s.dSharpe_FULLMATCH.values, RECORD_TIE)['tie_share']:>12.4f} "
          f"{rates(s.dSharpe_WINMATCH.values, RECORD_TIE)['tie_share']:>12.4f} "
          + " ".join(f"{gaps[tr]:>+10.4f}" for tr in TIE_RULES))
    P(f"   H4 (EXCLUDED closes the convention gap below 0.05 on OOS): "
      f"{'PASS' if H4 else 'FAIL'}")

    # H8: 843's leg
    P(f"\n   H8 - idea 843's leg (QROLL, IS window, {RUNG_HEAD:g} bps), by lookback w:")
    P(f"   {'panel':<6} {'w':>5} {'n':>4} | {'F-tie':>6} {'F-LOSS':>7} {'F-WIN':>7} {'F-EXCL':>7}"
      f" | {'W-tie':>6} {'W-LOSS':>7} {'W-WIN':>7} {'W-EXCL':>7}")
    h8rows = []
    for pn in PANELS:
        for w in WS_ROLL:
            s = CE[(CE.panel == pn) & (CE.rung == RUNG_HEAD) & (CE.window == "IS")
                   & (CE.family == "QROLL") & (CE.w == w)]
            if s.empty:
                continue
            rf = rates(s.dSharpe_FULLMATCH.values, RECORD_TIE)
            rw = rates(s.dSharpe_WINMATCH.values, RECORD_TIE)
            h8rows.append((pn, w, rf, rw))
            P(f"   {pn:<6} {w:>5} {rf['n']:>4} | {rf['tie_share']:>6.4f} {rf['LOSS']:>7.4f} "
              f"{rf['WIN']:>7.4f} {rf['EXCLUDED']:>7.4f} | {rw['tie_share']:>6.4f} "
              f"{rw['LOSS']:>7.4f} {rw['WIN']:>7.4f} {rw['EXCLUDED']:>7.4f}")
    zero = [r for r in h8rows if r[3]["LOSS"] == 0.0 and r[3]["tie_share"] == 1.0]
    agree = [r for r in h8rows if np.isfinite(r[2]["EXCLUDED"]) and np.isfinite(r[3]["EXCLUDED"])
             and abs(r[2]["EXCLUDED"] - r[3]["EXCLUDED"]) < 0.05]
    H8 = bool(zero)
    P(f"   843's exact-0.0000 WINMATCH collapse reproduces in {len(zero)} of {len(h8rows)} "
      f"(panel, w) legs, all of them 100% ties;  EXCLUDED agrees across conventions in "
      f"{len(agree)} of {len(h8rows)}.")
    P(f"   H8 (the 0.0000 collapse rebuilds): {'PASS' if H8 else 'FAIL'}")

    # ================= PART D - rule 8 ===============================================
    P(f"\n{'='*118}\nPART D - RULE 8\n{'='*118}")
    P("   (a) ON THE CLAIM: is the tie share a stable property, i.e. does the IS reading predict")
    P("       the OOS reading?  Measured per (panel, rung, family, matching).")
    P(f"   {'matching':<10} {'n cells':>8} {'mean IS':>9} {'mean OOS':>9} {'max|d|':>9} "
      f"{'corr':>7}  verdict")
    r8a = {}
    for cv in CONVS:
        col = f"dSharpe_{cv}"
        a_, b_ = [], []
        for pn, c, fam in product(PANELS, RUNGS, FAMS):
            si = CE[(CE.panel == pn) & (CE.rung == c) & (CE.window == "IS") & (CE.family == fam)]
            so = CE[(CE.panel == pn) & (CE.rung == c) & (CE.window == "OOS") & (CE.family == fam)]
            if si.empty or so.empty:
                continue
            a_.append(rates(si[col].values, RECORD_TIE)["tie_share"])
            b_.append(rates(so[col].values, RECORD_TIE)["tie_share"])
        a_, b_ = np.array(a_), np.array(b_)
        mx = float(np.abs(a_ - b_).max())
        cr = float(np.corrcoef(a_, b_)[0, 1]) if a_.std() > 0 and b_.std() > 0 else np.nan
        r8a[cv] = mx
        P(f"   {cv:<10} {len(a_):>8} {a_.mean():>9.4f} {b_.mean():>9.4f} {mx:>9.4f} "
          f"{cr:>7.3f}  {'PASS' if mx <= 0.10 else 'FAIL'}")
    H6 = bool(max(r8a.values()) <= 0.10)
    P(f"   H6 (IS tie share predicts OOS to within 0.10): {'PASS' if H6 else 'FAIL'}")

    P("\n   (b) ON THE BOOKS: a twin-win SELECTOR chooses, inside each (panel, rung, family,")
    P("       gross, depth, cadence) cell, the highest-IS-Sharpe arm among those ELIGIBLE under")
    P("       the tie rule.  LOSS/EXCLUDED require a STRICT in-sample win over the IS twin;")
    P("       WIN admits the tied (never-firing) arms too.  Parameters are chosen on 2009-2016")
    P("       only; 2017-2026 is untouched.  Both conventions reported.")
    CELLKEYS = ["panel", "rung", "family", "gross", "depth", "cadence"]
    for cv in CONVS:
        dcol = f"dIS_{cv}"
        for tr in TIE_RULES:
            for kk, s in AR.groupby(CELLKEYS):
                if tr == "WIN":
                    elig_ = s[s[dcol] >= -RECORD_TIE]
                else:
                    elig_ = s[s[dcol] > RECORD_TIE]
                empty = elig_.empty
                if empty:
                    elig_ = s
                pk = elig_.loc[elig_.IS_Sharpe.idxmax()]
                wfrows.append(dict(zip(CELLKEYS, kk)) | dict(
                    matching=cv, tie_rule=tr, n_eligible=len(elig_), fellback=empty,
                    level=pk.level, w=pk.w, arm=pk.arm, IS_Sharpe=pk.IS_Sharpe,
                    OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                    pass_4a=pk.pass_4a, pass_4b=pk.pass_4b, fail_4b=pk.fail_4b,
                    SPY_OOS_CAGR=pk.SPY_OOS_CAGR, SPY_OOS_Sharpe=pk.SPY_OOS_Sharpe,
                    SPY_OOS_MaxDD=pk.SPY_OOS_MaxDD, V2_OOS_CAGR=pk.V2_OOS_CAGR,
                    V2_OOS_Sharpe=pk.V2_OOS_Sharpe, V2_OOS_MaxDD=pk.V2_OOS_MaxDD))
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    P(f"\n   {'match':<10} {'tie rule':<9} {'cells':>6} {'moved':>6} {'share':>7} "
      f"{'OOS CAGR':>9} {'OOS Shp':>8} {'OOS DD':>8} {'4a':>5} {'4b':>5}")
    base_pick = {}
    move_max = 0.0
    for cv in CONVS:
        for tr in TIE_RULES:
            s = WF[(WF.matching == cv) & (WF.tie_rule == tr)].set_index(CELLKEYS)
            if tr == TIE_HEAD:
                base_pick[cv] = s.arm
                moved, share = 0, 0.0
            else:
                j = s.arm.to_frame("new").join(base_pick[cv].to_frame("old"))
                moved = int((j.new != j.old).sum())
                share = moved / len(j)
                move_max = max(move_max, share)
            P(f"   {cv:<10} {tr:<9} {len(s):>6} {moved:>6} {share:>7.4f} "
              f"{s.OOS_CAGR.mean():>9.2%} {s.OOS_Sharpe.mean():>8.3f} {s.OOS_MaxDD.mean():>8.2%} "
              f"{int(s.pass_4a.sum()):>5} {int(s.pass_4b.sum()):>5}")
    H7 = bool(move_max >= 0.10)
    P(f"   H7 (the tie rule moves >= 10% of selector picks): {'PASS' if H7 else 'FAIL'}  "
      f"(max share moved {move_max:.4f})")

    P(f"\n   the HEADLINE rung ({RUNG_HEAD:g} bps), WINMATCH, picks vs their benchmarks:")
    P(f"   {'tie rule':<9} {'panel':<6} {'OOS CAGR':>9} {'OOS Shp':>8} {'OOS DD':>8} | "
      f"{'RULES v2 OOS':>28} | {'SPY OOS':>26} | {'4a':>4} {'4b':>4}")
    for tr in TIE_RULES:
        for pn in PANELS:
            s = WF[(WF.matching == "WINMATCH") & (WF.tie_rule == tr) & (WF.rung == RUNG_HEAD)
                   & (WF.panel == pn)]
            if s.empty:
                continue
            P(f"   {tr:<9} {pn:<6} {s.OOS_CAGR.mean():>9.2%} {s.OOS_Sharpe.mean():>8.3f} "
              f"{s.OOS_MaxDD.mean():>8.2%} | "
              f"{s.V2_OOS_CAGR.iloc[0]:>9.2%} {s.V2_OOS_Sharpe.iloc[0]:>7.3f} "
              f"{s.V2_OOS_MaxDD.iloc[0]:>8.2%} | "
              f"{s.SPY_OOS_CAGR.iloc[0]:>8.2%} {s.SPY_OOS_Sharpe.iloc[0]:>7.3f} "
              f"{s.SPY_OOS_MaxDD.iloc[0]:>8.2%} | {int(s.pass_4a.sum()):>4} "
              f"{int(s.pass_4b.sum()):>4}")

    P(f"\n   BOTH KEEP PATHS over the whole rebuilt corpus ({len(AR)} arm rows):")
    P(f"   {'rung':>5} {'panel':<6} {'4a':>6} {'4b':>6} {'BOTH':>6} {'n':>6}")
    for c in RUNGS:
        for pn in PANELS:
            s = AR[(AR.rung == c) & (AR.panel == pn)]
            P(f"   {c:>5.0f} {pn:<6} {int(s.pass_4a.sum()):>6} {int(s.pass_4b.sum()):>6} "
              f"{int((s.pass_4a & s.pass_4b).sum()):>6} {len(s):>6}")

    # the best rule-8 4b pick at the headline rung, by OOS Sharpe
    cand = WF[(WF.rung == RUNG_HEAD) & WF.pass_4b]
    if not cand.empty:
        b = cand.loc[cand.OOS_Sharpe.idxmax()]
        P(f"\n   best rule-8 4b pick at {RUNG_HEAD:g} bps: {b.panel} {b.arm} "
          f"({b.matching}/{b.tie_rule})")
        P(f"     OOS  CAGR {b.OOS_CAGR:.2%}  Sharpe {b.OOS_Sharpe:.3f}  MaxDD {b.OOS_MaxDD:.2%}")
        P(f"     RULES v2 OOS  CAGR {b.V2_OOS_CAGR:.2%}  Sharpe {b.V2_OOS_Sharpe:.3f}  "
          f"MaxDD {b.V2_OOS_MaxDD:.2%}")
        P(f"     SPY      OOS  CAGR {b.SPY_OOS_CAGR:.2%}  Sharpe {b.SPY_OOS_Sharpe:.3f}  "
          f"MaxDD {b.SPY_OOS_MaxDD:.2%}")
        n_tr = cand.groupby("tie_rule").size().to_dict()
        P(f"     4b picks by tie rule: {n_tr}")

    # ---- the 9-point tuned grid, written out --------------------------------------
    GD = pd.DataFrame(grid)
    for cs, tr in product(CLAIM_SETS, TIE_RULES):
        m = (GD.claim_set == cs) & (GD.tie_rule == tr)
        GD.loc[m, "corpus_rate_WINMATCH_OOS"] = rates(
            CE[(CE.rung == RUNG_HEAD) & (CE.window == "OOS")].dSharpe_WINMATCH.values,
            RECORD_TIE)[tr]
        GD.loc[m, "corpus_rate_FULLMATCH_OOS"] = rates(
            CE[(CE.rung == RUNG_HEAD) & (CE.window == "OOS")].dSharpe_FULLMATCH.values,
            RECORD_TIE)[tr]
    GD.to_csv(f"{OUT}.grid.csv", index=False)

    # ================= verdict ========================================================
    P(f"\n{'='*118}\nHYPOTHESIS SCORECARD\n{'='*118}")
    H2col = C[(C.file == CELLS.name) & (C.win_col == "win")]
    H2 = bool(len(H2col) and float(H2col[f"tie_{RECORD_TIE:g}"].iloc[0]) < 0.01)
    hyps = [("H1 tie share >= 10% of the TWIN claim set", H1),
            ("H2 the canonical FULL/FULLMATCH win column has tie share < 1%", H2),
            ("H3 a published family ordering differs between tie rules", H3),
            ("H4 EXCLUDED closes the FULLMATCH/WINMATCH gap below 0.05 on OOS", H4),
            ("H5 every WINMATCH tie is EXACT (max|d| == 0.0)", H5),
            ("H6 IS tie share predicts OOS to within 0.10", H6),
            ("H7 the tie rule moves >= 10% of selector picks", H7),
            ("H8 843's 0.7778 -> 0.0000 collapse rebuilds", H8)]
    for n, v in hyps:
        P(f"   {'PASS' if v else 'FAIL'}  {n}")
    P(f"   {sum(v for _, v in hyps)} of {len(hyps)} pre-registered hypotheses PASS")
    P(f"\n   runtime {time.time()-T0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(C=C, CE=CE, AR=AR, OD=OD, WF=WF, GD=GD,
                hyps=hyps, H2col=H2col, G5a=G5a_max, G5b=G5b_max, g6=g6)


if __name__ == "__main__":
    main()
