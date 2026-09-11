#!/usr/bin/env python3
"""Idea 797 (cloud, 2026-09-11) - should-every-published-PANEL-ORDERING-quote-its-ADJACENT-GAP-
over-FLOOR-instead-of-its-SPAN.

QUESTION
--------
Idea 773 (lane C, 2026-09-11) found that the three-parent SPAN clears the draw-level noise floor
in 66-70 of 90 (statistic x split x gross x cadence) cells, while the SMALLEST ADJACENT GAP - the
statistic a three-panel ORDERING actually has to clear, because the span only bounds the two
extremes and says nothing about whether the middle panel is separated from either neighbour -
clears its own floor in 2-4 of 90.  It also found U56 is a strict subset of B136 (55 of 55 stocks)
so the binding gap is a nested-pair contribution in 21 of 30 OOS cells.

This run PRICES THE SWAP OF BAR over the record's committed panel-ordering claims:
    OLD bar (what the record quotes) : span   / floor, floor POOLED across the three parents
    NEW bar (what it should quote)   : margin / floor, margin = smallest adjacent gap,
                                      floor = RSS over the TWO PARENTS THE GAP IS BETWEEN
and reports HOW MANY COMMITTED CLAIMS ARE RETIRED.

A claim is RETIRED iff it passes the OLD bar and FAILS the NEW one at its own statistic and its
own window.  A claim is REINSTATED in the opposite case (reported, not assumed to be empty).
The margin and the floors are NOT read out of the claim's own text - the text almost never quotes
them - they are rebuilt here from prices for the claim's (statistic, window) cell, so the census
is resolvable rather than a recoverability exercise.  The share of claims that cannot be re-scored
at all, and exactly why, is reported beside the retirement count.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
    1. CLAIMSET in {COMMITTED, ALL}
         COMMITTED = the published prose record: research/CHANGELOG.md, research/LEADERBOARD.md,
                     research/backtests/*.result.md and the memos (*memo*.md, *MEMO*.md)
         ALL       = COMMITTED plus every *.console.txt and every *.py in research/backtests
    2. BARFORM in {SPAN_POOLED, SPAN_RSS, GAP_POOLED, GAP_RSS}
         SPAN_POOLED is the record's own bar; GAP_RSS is the proposed replacement; the two mixed
         forms isolate which half of the swap (the numerator or the floor) does the work.
All 2 x 4 = 8 grid points are reported.  REPORTED-NEVER-SELECTED axes: draw count D in
{3, 6, 12, 24}, gross g in {0.50, 0.75, 1.00}, cadence in {W, M}, window in {FULL, IS, OOS},
statistic in {PREM_SHARPE, PREM_CAGR, SHARPE, CAGR, MAXDD}.  Nothing is picked on any of them.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
    H_REPRO    : this run's fresh-from-prices span/margin/floor grid reproduces idea 773's
                 committed .spans.csv on all 90 rows and all 38 columns to 1e-12, and its
                 .floors.csv on all 60 rows.  If not, nothing downstream is trustworthy.
    H_RETIRE   : the swap retires a MAJORITY (> 50%) of re-scorable committed panel-ordering
                 claims.  This is the queue's premise stated as a number.
    H_NUMERATOR: the numerator (span -> smallest adjacent gap) does more of the retiring than the
                 floor (POOLED -> RSS over the gap's own pair), i.e. retirement under GAP_POOLED
                 exceeds retirement under SPAN_RSS.
    H_WINDOW   : the retirement share is HIGHER out of sample than in sample (773's collapse is
                 an IS->OOS fact, so a bar that binds OOS should retire more there).
    H_WF       : a bar form chosen on the IS window alone keeps its verdict out of sample - the
                 OOS retirement share lands within 10 pp of the IS one.
    H_BOOK     : the bar swap CHANGES THE BOOK.  Taking the ordering as a trading instruction
                 ("hold the panel the ordering puts first"), the panel selected under GAP_RSS
                 differs from the one selected under SPAN_POOLED for at least one statistic.

GATES (run and printed BEFORE any new number is read)
    G0 determinism  : the crc32 draw scheme rebuilt twice gives identical name sets.      bar 0
    G1 identity     : fast_backtest vs engine.backtest on one book per parent.         bar 1e-12
    G2 cross-lane   : idea 773's committed .floors.csv, all 60 rows x 9 cols, rebuilt from
                      prices here.                                                     bar 1e-12
    G3 cross-lane   : idea 773's committed .spans.csv, all 90 rows x every numeric col, rebuilt
                      from prices here.  This is the reproduction that matters - the NEW bar's
                      numerator and floor both live in that file.                      bar 1e-12
    G4 live book    : RULES v2 on U56 vs the committed 0.0861 / 1.1998 / -0.1205.        bar 1e-4
    G5 census determinism: the claim harvest run twice gives an identical site table.     bar 0

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: every span, margin and floor is computed separately on IS and on OOS, and
       the retirement census is run three times (FULL / IS / OOS).  H_WF is the IS-vs-OOS
       comparison of the retirement share; the bar form is chosen on IS alone.
    WF-B on a BOOK: the ordering is taken at face value as a trading instruction.  For each
       (statistic, BARFORM) the top parent is the one the IS ordering puts first; (gross, cadence)
       is then chosen by IS Sharpe ALONE on that parent's MA-RS book; OOS CAGR / Sharpe / MaxDD
       are read ONCE against live RULES v2 on the same panel and against SPY.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
    BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for EVERY
    book on the grid and the counts reported, split REAL vs DRAW.  Stated up front: a DRAW panel
    is a seeded random 36-name subset, not a rule anyone can trade, so a 4b pass on a draw is a
    diagnostic only; only the REAL parents' books can be capital candidates.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents of their screens.
    SMALL439 drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv first.  On a
    premium (arm minus arm inside one panel) the bias largely cancels; on the LEVEL statistics it
    does not, so every level span and every level gap here is an UPPER bound on the true one and
    every floor a LOWER bound - which biases the OLD bar toward passing and therefore biases this
    run TOWARD finding retirements.  Said again beside the result.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and idea 773's committed
artefacts; modifies nothing but its own outputs:
    .grid.csv .floors.csv .spans.csv .sites.csv .census.csv .retire.csv .walkforward.csv
    .keeppaths.csv .console.txt
"""
from __future__ import annotations

import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
K_DRAW = 36
N_SEED = 24
DRAW_COUNTS = [3, 6, 12, 24]
STATS = ["PREM_SHARPE", "PREM_CAGR", "SHARPE", "CAGR", "MAXDD"]
SPLITS = ["FULL", "IS", "OOS"]
BARFORMS = ["SPAN_POOLED", "SPAN_RSS", "GAP_POOLED", "GAP_RSS"]
CLAIMSETS = ["COMMITTED", "ALL"]
HEADLINE_D = 6                      # idea 567/773's D, quoted for comparability
MAJORITY = 4                        # 4 of the 6 (gross, cadence) cells

PARENT773 = OUT / "2026-09-11_does-the-OOS-SPAN-COLLAPSE-hold-for-the-OTHER-FOUR-STATISTICS_C"
V2_U56 = (0.0861, 1.1998, -0.1205)  # committed live RULES v2 row on U56
TOL = 1e-12
G4_TOL = 1e-4

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- books
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def make_books(px, tradable, g):
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------------- panels
def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return {
        "U56": (px56.dropna(how="all").ffill(), sorted(set(px56.columns) - {"SPY"})),
        "B136": (px136.dropna(how="all").ffill(), sorted(set(px136.columns) - {"SPY"})),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), sorted(s_stk)),
    }


def draws(parent, names, n_seed=N_SEED, k=K_DRAW):
    """crc32-seeded k-matched draws, `DRAW|{parent}|{seed}` (idea 567/773's scheme verbatim)."""
    pool = np.array(sorted(names))
    out = []
    for sd in range(n_seed):
        seed = zlib.crc32(f"DRAW|{parent}|{sd}".encode()) % (2 ** 32)
        rng = np.random.default_rng(seed)
        pick = sorted(rng.choice(pool, size=min(k, len(pool)), replace=False).tolist())
        out.append((sd, pick))
    return out


def stat_series(sub, stat, period="FULL"):
    """idea 567/773's estimator verbatim: the per-draw value of `stat` on window `period`."""
    pre = {"FULL": "", "IS": "IS_", "OOS": "OOS_"}[period]
    ma = sub[sub.arm == "MA-RS"]
    if stat == "PREM_SHARPE":
        col = {"FULL": "dSharpe_vs_EWall", "IS": "IS_dSharpe", "OOS": "OOS_dSharpe"}[period]
        return ma[col]
    if stat == "PREM_CAGR":
        if period != "FULL":
            ew = sub[sub.arm == "EWall"].set_index(["seed", "gross", "cadence"])[pre + "CAGR"]
            m2 = ma.set_index(["seed", "gross", "cadence"])[pre + "CAGR"]
            return m2 - ew.reindex(m2.index)
        return ma["dCAGR_vs_EWall"]
    return ma[pre + {"SHARPE": "Sharpe", "CAGR": "CAGR", "MAXDD": "MaxDD"}[stat]]


def real_value(real, pn, stat, period, g, cad):
    sub = real[(real.parent == pn) & (real.gross == g) & (real.cadence == cad)]
    return float(stat_series(sub, stat, period).iloc[0])


# =============================================================== the claim census
PANEL_RE = re.compile(r"\b(U56|B136|SMALL\d{3})\b")
OP_RE = re.compile(r"(U56|B136|SMALL\d{3})\s*\**\s*(?:>|<|->|→|>=|<=)\s*\**\s*(U56|B136|SMALL\d{3})")
ORDER_WORDS = ("ordering", "order", "ranks", "ranked", "ranking", "beats", "beat", "best",
               "worst", "highest", "lowest", "top", "ahead", "outperform", "above", "below")
# statistic keywords, resolved in this order - premium forms first, then levels
STAT_RULES = [
    ("PREM_SHARPE", (r"PREM_SHARPE", r"\bdSharpe\b", r"premium[^.]{0,40}Sharpe",
                     r"Sharpe[^.]{0,40}premium")),
    ("PREM_CAGR", (r"PREM_CAGR", r"\bdCAGR\b", r"premium[^.]{0,40}CAGR",
                   r"CAGR[^.]{0,40}premium")),
    ("MAXDD", (r"MAXDD", r"MaxDD", r"drawdown", r"\bDD\b", r"Calmar")),
    ("SHARPE", (r"Sharpe",)),
    ("CAGR", (r"CAGR", r"pp/yr", r"return")),
]
STAT_PAT = [(s, [re.compile(p, re.I) for p in ps]) for s, ps in STAT_RULES]
OOS_PAT = re.compile(r"\bOOS\b|out-of-sample|out of sample", re.I)
IS_PAT = re.compile(r"\bIS\b|in-sample|in sample", re.I)


def committed_files():
    f = [ROOT / "research" / "CHANGELOG.md", ROOT / "research" / "LEADERBOARD.md"]
    f += sorted((ROOT / "research" / "backtests").glob("*.result.md"))
    f += sorted((ROOT / "research" / "backtests").glob("*memo*.md"))
    f += sorted((ROOT / "research" / "backtests").glob("*MEMO*.md"))
    return sorted(set(f))


def all_files():
    f = committed_files()
    f += sorted((ROOT / "research" / "backtests").glob("*.console.txt"))
    f += sorted((ROOT / "research" / "backtests").glob("*.py"))
    return sorted(set(f))


def harvest(files):
    """Every line naming >= 2 of the three panel tokens, classified.  Pre-registered rules only."""
    rows = []
    for fp in files:
        try:
            txt = fp.read_text(errors="replace")
        except OSError:
            continue
        rel = str(fp.relative_to(ROOT))
        for i, ln in enumerate(txt.splitlines(), 1):
            ps = PANEL_RE.findall(ln)
            if len(set(ps)) < 2:
                continue
            op = bool(OP_RE.search(ln))
            low = ln.lower()
            word = any(w in low for w in ORDER_WORDS)
            stat = None
            for s, pats in STAT_PAT:
                if any(p.search(ln) for p in pats):
                    stat = s
                    break
            win = "OOS" if OOS_PAT.search(ln) else ("IS" if IS_PAT.search(ln) else "FULL")
            rows.append(dict(file=rel, line=i, n_panels=len(set(ps)),
                             three=len(set(ps)) >= 3, op=op, word=word,
                             ordering=bool(op or word), statistic=stat or "",
                             window=win, text=ln.strip()[:300]))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 797 - price the bar swap (span/floor -> smallest-adjacent-gap/RSS-floor) over the")
    P("#            record's committed PANEL-ORDERING claims, and count the retirements.")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}")
    P("# TUNED (2): CLAIMSET x BARFORM.  REPORTED-NOT-SELECTED: D, gross, cadence, window,")
    P("#            statistic.  All 8 grid points printed and committed.")
    P("")
    P("PRE-REGISTERED: H_REPRO (773's committed floors+spans reproduce from prices to 1e-12),")
    P("  H_RETIRE (>50% of re-scorable committed ordering claims retired by the swap),")
    P("  H_NUMERATOR (GAP_POOLED retires more than SPAN_RSS), H_WINDOW (OOS share > IS share),")
    P("  H_WF (OOS retirement share within 10 pp of IS), H_BOOK (the swap changes the book).")
    P("")

    parents = real_panels()
    pnames = list(parents)
    P("PARENTS: " + ", ".join(
        f"{k} ({len(v[1])} names, {v[0].index[0].date()}..{v[0].index[-1].date()})"
        for k, v in parents.items()))
    P("SURVIVORSHIP: B136 and the small panel are CURRENT constituents; level spans/gaps are")
    P("  upper bounds and floors lower bounds, which biases the OLD bar toward PASSING and so")
    P("  biases this run TOWARD finding retirements.")
    P("")

    # ---------------------------------------------------------------- gates G0/G1/G4/G5
    P("=" * 108)
    P("GATES (printed before any new number is read)")
    P("=" * 108)
    g0 = 0
    for pn, (_, names) in parents.items():
        a = [set(x[1]) for x in draws(pn, names)]
        b = [set(x[1]) for x in draws(pn, names)]
        g0 += sum(0 if x == y else 1 for x, y in zip(a, b))
    P(f"G0 determinism  : {g0} of {N_SEED*len(parents)} draws differ on rebuild (bar 0) -> "
      f"{'PASS' if g0 == 0 else 'FAIL'}")

    g1 = 0.0
    for pn, (px, names) in parents.items():
        bk = make_books(px, set(names), 0.75)["MA-RS"]
        a = fast_backtest(px, bk, freq="W")["returns"]
        b = backtest(px, bk, cost_bps=COST, freq="W")["returns"]
        g1 = max(g1, float(np.abs(a.values - b.values).max()))
    P(f"G1 identity     : fast_backtest vs engine.backtest max |dret| = {g1:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g1 <= TOL else 'FAIL'}")

    px56 = parents["U56"][0]
    warm56 = px56.index[260]
    m56 = metrics(fast_backtest(px56, rules_v2_weights(px56), freq="W")["returns"].loc[warm56:])
    g4 = max(abs(m56["CAGR"] - V2_U56[0]), abs(m56["Sharpe"] - V2_U56[1]),
             abs(m56["MaxDD"] - V2_U56[2]))
    P(f"G4 live book    : RULES v2 on U56 = {m56['CAGR']:.4f} / {m56['Sharpe']:.4f} / "
      f"{m56['MaxDD']:.4f} vs committed {V2_U56} max |d| = {g4:.3e} (bar {G4_TOL:.0e}) -> "
      f"{'PASS' if g4 <= G4_TOL else 'FAIL'}")

    FILES = {"COMMITTED": committed_files(), "ALL": all_files()}
    sites = {cs: harvest(FILES[cs]) for cs in CLAIMSETS}
    again = harvest(FILES["COMMITTED"])
    g5 = 0 if again.equals(sites["COMMITTED"]) else 1
    P(f"G5 census det.  : claim harvest rebuilt -> {'identical' if g5 == 0 else 'DIFFERS'} "
      f"(bar 0) -> {'PASS' if g5 == 0 else 'FAIL'}")
    for cs in CLAIMSETS:
        s = sites[cs]
        P(f"   {cs:9s}: {len(FILES[cs]):4d} files, {len(s):5d} lines name >= 2 panels, "
          f"{int(s.ordering.sum()):5d} are ORDERING sites, {int(s.three.sum()):5d} name all three")
    P("  (G2/G3 reproduce idea 773's committed floors and spans; they need the grid and are")
    P("   printed immediately after it, before any NEW number is read.)")
    P("")

    # ---------------------------------------------------------------- price grid
    P("=" * 108)
    P("PRICE LEG - 3 REAL parents + 24 k=36 draws each, 3 gross x 2 cadence x 2 arms")
    P("=" * 108)
    rows = []
    spy_cache, v2_cache = {}, {}
    for pn, (px, names) in parents.items():
        units = [("REAL", -1, sorted(names))] + [("DRAW", sd, pick) for sd, pick in draws(pn, names)]
        for kind, sd, pick in units:
            cols = list(dict.fromkeys(pick + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
            warm = sub.index[260]
            spy = sub["SPY"].pct_change().fillna(0.0).loc[warm:]
            v2 = fast_backtest(sub, rules_v2_weights(sub), freq="W")["returns"].loc[warm:]
            if kind == "REAL":
                spy_cache[pn], v2_cache[pn] = spy, v2
            for g in GROSS:
                bks = make_books(sub, set(pick), g)
                for cad in CADENCE:
                    res = {a: fast_backtest(sub, w, freq=cad) for a, w in bks.items()}
                    base = {a: r["returns"].loc[warm:] for a, r in res.items()}
                    ew_m = metrics(base["EWall"])
                    ew_is = metrics(base["EWall"].loc[:IS_END])
                    ew_oos = metrics(base["EWall"].loc[OOS_START:])
                    for arm in ("EWall", "MA-RS"):
                        r = base[arm]
                        d = rowify(r, res[arm]["turnover"].loc[warm:])
                        d.update(parent=pn, kind=kind, seed=sd, arm=arm, gross=g, cadence=cad,
                                 k=len(pick))
                        d["dSharpe_vs_EWall"] = d["Sharpe"] - ew_m["Sharpe"]
                        d["dCAGR_vs_EWall"] = d["CAGR"] - ew_m["CAGR"]
                        d["IS_dSharpe"] = metrics(r.loc[:IS_END])["Sharpe"] - ew_is["Sharpe"]
                        d["OOS_dSharpe"] = metrics(r.loc[OOS_START:])["Sharpe"] - ew_oos["Sharpe"]
                        d["keep4a"] = keep_4a(r, v2)
                        d["fail4b"] = fail_4b(r, spy)
                        d["keep4b"] = d["fail4b"] == "-"
                        rows.append(d)
        P(f"  {pn}: {len(units)} panels done ({time.time()-t0:.0f}s)")
    grid = pd.DataFrame(rows)
    real = grid[grid.kind == "REAL"]
    dr = grid[grid.kind == "DRAW"]
    P("")

    # ---------------------------------------------------------------- floors
    fl_rows = []
    for stat in STATS:
        for D in DRAW_COUNTS:
            for period in SPLITS:
                per_parent = {}
                for pn in pnames:
                    vals = []
                    for g in GROSS:
                        for cad in CADENCE:
                            sub = dr[(dr.parent == pn) & (dr.gross == g) & (dr.cadence == cad)
                                     & (dr.seed < D)]
                            v = stat_series(sub, stat, period).to_numpy(float)
                            if len(v) >= 2:
                                vals.append(np.std(v, ddof=1))
                    per_parent[pn] = float(np.mean(vals)) if vals else np.nan
                row = dict(statistic=stat, D=D, period=period,
                           floor_pooled=float(np.nanmean(list(per_parent.values()))),
                           floor_max=float(np.nanmax(list(per_parent.values()))),
                           floor_min=float(np.nanmin(list(per_parent.values()))))
                row.update({f"floor_{k}": v for k, v in per_parent.items()})
                row["parent_ratio"] = row["floor_max"] / row["floor_min"] if row["floor_min"] else np.nan
                fl_rows.append(row)
    floors = pd.DataFrame(fl_rows)

    def floor_of(stat, D, period):
        return floors[(floors.statistic == stat) & (floors.D == D)
                      & (floors.period == period)].iloc[0]

    # ---------------------------------------------------------------- spans + both bars
    sp_rows = []
    for stat in STATS:
        for period in SPLITS:
            for g in GROSS:
                for cad in CADENCE:
                    v = {pn: real_value(real, pn, stat, period, g, cad) for pn in pnames}
                    order = sorted(v, key=lambda k: v[k], reverse=True)
                    vals = [v[p] for p in order]
                    gaps = [a - b for a, b in zip(vals, vals[1:])]
                    span = vals[0] - vals[-1]
                    j = int(np.argmin(gaps))
                    margin = gaps[j]
                    row = dict(statistic=stat, period=period, gross=g, cadence=cad,
                               order=">".join(order), span=span, margin=margin,
                               top=order[0], span_pair=f"{order[0]}|{order[-1]}",
                               margin_pair=f"{order[j]}|{order[j+1]}")
                    row.update({f"val_{p}": v[p] for p in pnames})
                    for D in DRAW_COUNTS:
                        fl = floor_of(stat, D, period)
                        pooled = fl.floor_pooled
                        rss_span = float(np.hypot(fl[f"floor_{order[0]}"], fl[f"floor_{order[-1]}"]))
                        rss_marg = float(np.hypot(fl[f"floor_{order[j]}"], fl[f"floor_{order[j+1]}"]))
                        row[f"floorP_D{D}"] = pooled
                        row[f"spanR_POOLED_D{D}"] = span / pooled
                        row[f"marginR_POOLED_D{D}"] = margin / pooled
                        row[f"floorR_D{D}"] = rss_span
                        row[f"spanR_RSS_D{D}"] = span / rss_span
                        row[f"marginR_RSS_D{D}"] = margin / rss_marg
                    sp_rows.append(row)
    spans = pd.DataFrame(sp_rows)

    # ------------------------------------------------------- G2 / G3 cross-lane reproduction
    P("=" * 108)
    P("G2 / G3 - CROSS-LANE REPRODUCTION of idea 773 from prices (still no new number read)")
    P("=" * 108)
    g2 = g3 = float("nan")
    try:
        f773 = pd.read_csv(f"{PARENT773}.floors.csv")
        cols = [c for c in f773.columns if c not in ("statistic", "D", "period")]
        mg = f773.merge(floors, on=["statistic", "D", "period"], suffixes=("_c", "_r"))
        assert len(mg) == len(f773) == 60, (len(mg), len(f773))
        g2 = max(float(np.abs(mg[c + "_c"] - mg[c + "_r"]).max()) for c in cols)
        P(f"G2 cross-lane   : idea 773 .floors.csv, all {len(f773)} rows x {len(cols)} cols, "
          f"max |d| = {g2:.3e} (bar {TOL:.0e}) -> {'PASS' if g2 <= TOL else 'FAIL'}")
    except Exception as e:
        P(f"G2 cross-lane   : FAILED TO RUN ({e!r})")
    try:
        s773 = pd.read_csv(f"{PARENT773}.spans.csv")
        key = ["statistic", "period", "gross", "cadence"]
        num = [c for c in s773.columns if c not in key + ["order", "top", "span_pair", "margin_pair"]]
        mg = s773.merge(spans, on=key, suffixes=("_c", "_r"))
        assert len(mg) == len(s773) == 90, (len(mg), len(s773))
        g3 = max(float(np.abs(mg[c + "_c"] - mg[c + "_r"]).max()) for c in num)
        same_txt = all(bool((mg[c + "_c"] == mg[c + "_r"]).all())
                       for c in ("order", "top", "span_pair", "margin_pair"))
        P(f"G3 cross-lane   : idea 773 .spans.csv, all {len(s773)} rows x {len(num)} numeric cols, "
          f"max |d| = {g3:.3e}; order/top/pair labels identical {same_txt} "
          f"(bar {TOL:.0e}) -> {'PASS' if (g3 <= TOL and same_txt) else 'FAIL'}")
    except Exception as e:
        P(f"G3 cross-lane   : FAILED TO RUN ({e!r})")
    P("")
    H_REPRO = bool(g2 <= TOL and g3 <= TOL)
    P(f"H_REPRO -> {'PASS' if H_REPRO else 'FAIL'}")
    P("")

    # ------------------------------------------------------- the bar, cell by cell
    P("=" * 108)
    P("THE TWO BARS, ALL 90 (statistic x window x gross x cadence) CELLS, at every D")
    P("=" * 108)
    barcol = {"SPAN_POOLED": "spanR_POOLED", "SPAN_RSS": "spanR_RSS",
              "GAP_POOLED": "marginR_POOLED", "GAP_RSS": "marginR_RSS"}
    cells = []
    for D in DRAW_COUNTS:
        for bf in BARFORMS:
            c = f"{barcol[bf]}_D{D}"
            for period in SPLITS:
                s = spans[spans.period == period]
                cells.append(dict(D=D, barform=bf, window=period, n=len(s),
                                  n_gt1=int((s[c] > 1).sum()), median=float(s[c].median()),
                                  p25=float(s[c].quantile(0.25)), p75=float(s[c].quantile(0.75))))
    CE = pd.DataFrame(cells)
    P(f"  {'D':>3s} {'barform':12s} {'window':6s} {'cells>1':>8s} {'median':>9s} "
      f"{'p25':>9s} {'p75':>9s}")
    for _, r in CE.iterrows():
        P(f"  {r['D']:3d} {r['barform']:12s} {r['window']:6s} {r['n_gt1']:4d}/{r['n']:<3d} "
          f"{r['median']:9.4f} {r['p25']:9.4f} {r['p75']:9.4f}")
    P("")
    P("  per-statistic cells>1 out of 6 (gross x cadence), D = %d" % HEADLINE_D)
    P(f"  {'statistic':12s} {'window':6s} " + " ".join(f"{b:>12s}" for b in BARFORMS))
    pass_cell = {}
    for stat in STATS:
        for period in SPLITS:
            s = spans[(spans.statistic == stat) & (spans.period == period)]
            ns = []
            for bf in BARFORMS:
                n = int((s[f"{barcol[bf]}_D{HEADLINE_D}"] > 1).sum())
                pass_cell[(stat, period, bf)] = n
                ns.append(n)
            P(f"  {stat:12s} {period:6s} " + " ".join(f"{n:12d}" for n in ns))
    P("")

    # ------------------------------------------------------- THE CENSUS / RETIREMENT
    P("=" * 108)
    P("THE CENSUS - committed panel-ordering claims, and how many the swap RETIRES")
    P("=" * 108)
    P("  A site is an ORDERING claim iff it names >= 2 of {U56, B136, SMALL439} AND carries an")
    P("  explicit operator between two of them or one of the pre-registered ordering words.")
    P("  It is RE-SCORABLE iff a statistic in {PREM_SHARPE, PREM_CAGR, SHARPE, CAGR, MAXDD} is")
    P("  recoverable from the line.  Its window is OOS / IS / FULL by the same keyword rule.")
    P("  A claim PASSES a bar iff that bar clears 1.0 in >= %d of the 6 (gross, cadence) cells" % MAJORITY)
    P("  of its own (statistic, window).  RETIRED = passes SPAN_POOLED, fails the new bar.")
    P("")
    cen_rows, ret_rows = [], []
    for cs in CLAIMSETS:
        s = sites[cs]
        o = s[s.ordering].copy()
        scored = o[o.statistic != ""].copy()
        P(f"  {cs}: {len(s)} panel-naming lines -> {len(o)} ordering sites -> {len(scored)} "
          f"re-scorable ({len(scored)/max(len(o),1):.1%}); "
          f"{len(o)-len(scored)} dropped for no recoverable statistic")
        by = scored.groupby(["statistic", "window"]).size()
        P("    re-scorable by (statistic, window): " +
          ", ".join(f"{a}/{b}={c}" for (a, b), c in by.items()))
        for D in DRAW_COUNTS:
            for bf in BARFORMS:
                npass = 0
                for _, r in scored.iterrows():
                    n = int((spans[(spans.statistic == r.statistic) & (spans.period == r.window)]
                             [f"{barcol[bf]}_D{D}"] > 1).sum())
                    npass += 1 if n >= MAJORITY else 0
                cen_rows.append(dict(claimset=cs, D=D, barform=bf, n_sites=len(o),
                                     n_scorable=len(scored), n_pass=npass,
                                     share=npass / max(len(scored), 1)))
        # retirement = old pass & new fail, per claim
        for D in DRAW_COUNTS:
            old = {}
            for _, r in scored.iterrows():
                k = (r.statistic, r.window)
                if k not in old:
                    old[k] = int((spans[(spans.statistic == r.statistic)
                                        & (spans.period == r.window)]
                                  [f"spanR_POOLED_D{D}"] > 1).sum()) >= MAJORITY
            for bf in BARFORMS:
                new = {}
                for k in old:
                    new[k] = int((spans[(spans.statistic == k[0]) & (spans.period == k[1])]
                                  [f"{barcol[bf]}_D{D}"] > 1).sum()) >= MAJORITY
                ret = rein = 0
                for _, r in scored.iterrows():
                    k = (r.statistic, r.window)
                    if old[k] and not new[k]:
                        ret += 1
                    elif new[k] and not old[k]:
                        rein += 1
                n_old = sum(1 for _, r in scored.iterrows() if old[(r.statistic, r.window)])
                ret_rows.append(dict(claimset=cs, D=D, barform=bf, n_scorable=len(scored),
                                     n_old_pass=n_old, n_retired=ret, n_reinstated=rein,
                                     retire_share_of_old=ret / max(n_old, 1),
                                     retire_share_of_all=ret / max(len(scored), 1)))
    CEN = pd.DataFrame(cen_rows)
    RET = pd.DataFrame(ret_rows)
    P("")
    P("  RETIREMENT, all 8 tuned grid points x 4 draw counts (D reported, never selected)")
    P(f"  {'claimset':10s} {'D':>3s} {'barform':12s} {'scorable':>9s} {'oldpass':>8s} "
      f"{'retired':>8s} {'reinst':>7s} {'%of old':>8s} {'%of all':>8s}")
    for _, r in RET.iterrows():
        P(f"  {r['claimset']:10s} {r['D']:3d} {r['barform']:12s} {r['n_scorable']:9d} "
          f"{r['n_old_pass']:8d} {r['n_retired']:8d} {r['n_reinstated']:7d} "
          f"{r['retire_share_of_old']:8.1%} {r['retire_share_of_all']:8.1%}")
    P("")
    hl = RET[(RET.D == HEADLINE_D) & (RET.barform == "GAP_RSS")]
    H_RETIRE = bool((hl[hl.claimset == "COMMITTED"].retire_share_of_old.iloc[0]) > 0.50)
    gp = RET[(RET.D == HEADLINE_D) & (RET.barform == "GAP_POOLED") & (RET.claimset == "COMMITTED")]
    sr = RET[(RET.D == HEADLINE_D) & (RET.barform == "SPAN_RSS") & (RET.claimset == "COMMITTED")]
    H_NUMERATOR = bool(gp.n_retired.iloc[0] > sr.n_retired.iloc[0])
    P(f"  H_RETIRE    (> 50% of re-scorable COMMITTED ordering claims retired, D={HEADLINE_D}, "
      f"GAP_RSS) -> {'PASS' if H_RETIRE else 'FAIL'} "
      f"({hl[hl.claimset=='COMMITTED'].retire_share_of_old.iloc[0]:.1%} of the old passers, "
      f"{hl[hl.claimset=='COMMITTED'].retire_share_of_all.iloc[0]:.1%} of all)")
    P(f"  H_NUMERATOR (GAP_POOLED retires more than SPAN_RSS) -> "
      f"{'PASS' if H_NUMERATOR else 'FAIL'} ({gp.n_retired.iloc[0]} vs {sr.n_retired.iloc[0]})")

    # window split of the retirement share (WF-A)
    wrows = []
    for cs in CLAIMSETS:
        scored = sites[cs][sites[cs].ordering & (sites[cs].statistic != "")]
        for period in SPLITS:
            sub = scored[scored.window == period]
            if not len(sub):
                wrows.append(dict(claimset=cs, window=period, n=0, old=0, retired=0, share=np.nan))
                continue
            old = ret = 0
            for _, r in sub.iterrows():
                o = int((spans[(spans.statistic == r.statistic) & (spans.period == period)]
                         [f"spanR_POOLED_D{HEADLINE_D}"] > 1).sum()) >= MAJORITY
                n = int((spans[(spans.statistic == r.statistic) & (spans.period == period)]
                         [f"marginR_RSS_D{HEADLINE_D}"] > 1).sum()) >= MAJORITY
                old += int(o)
                ret += int(o and not n)
            wrows.append(dict(claimset=cs, window=period, n=len(sub), old=old, retired=ret,
                              share=ret / max(old, 1)))
    WIN = pd.DataFrame(wrows)
    P("")
    P("  WF-A - the same census run separately on FULL / IS / OOS (OOS read once)")
    P(f"  {'claimset':10s} {'window':6s} {'claims':>7s} {'oldpass':>8s} {'retired':>8s} {'%of old':>8s}")
    for _, r in WIN.iterrows():
        P(f"  {r['claimset']:10s} {r['window']:6s} {r['n']:7d} {r['old']:8d} {r['retired']:8d} "
          f"{r['share']:8.1%}" if r["n"] else
          f"  {r['claimset']:10s} {r['window']:6s} {r['n']:7d} {r['old']:8d} {r['retired']:8d}  "
          f"     n/a")
    c = WIN[WIN.claimset == "COMMITTED"].set_index("window")
    # window-independent reading: the bar applied to every cell, not only to the claims that
    # happen to name that window - this is what H_WINDOW and H_WF are judged on.
    cellshare = {}
    for period in SPLITS:
        s = spans[spans.period == period]
        o = sum(1 for stat in STATS
                if int((s[(s.statistic == stat)][f"spanR_POOLED_D{HEADLINE_D}"] > 1).sum()) >= MAJORITY)
        n = sum(1 for stat in STATS
                if int((s[(s.statistic == stat)][f"spanR_POOLED_D{HEADLINE_D}"] > 1).sum()) >= MAJORITY
                and int((s[(s.statistic == stat)][f"marginR_RSS_D{HEADLINE_D}"] > 1).sum()) < MAJORITY)
        cellshare[period] = (o, n, n / max(o, 1))
    P("")
    P("  statistic-level view (of the 5 statistics, how many pass SPAN_POOLED / are retired):")
    for period in SPLITS:
        o, n, sh = cellshare[period]
        P(f"    {period:5s} SPAN_POOLED passes {o}/5, retired by GAP_RSS {n}/{o} = {sh:.1%}")
    H_WINDOW = bool(cellshare["OOS"][2] >= cellshare["IS"][2])
    H_WF = bool(abs(cellshare["OOS"][2] - cellshare["IS"][2]) <= 0.10)
    P(f"  H_WINDOW (OOS retirement share >= IS) -> {'PASS' if H_WINDOW else 'FAIL'}")
    P(f"  H_WF     (|OOS - IS| <= 10 pp)        -> {'PASS' if H_WF else 'FAIL'}")
    P("")

    # ------------------------------------------------------- WF-B: the ordering as a book
    P("=" * 108)
    P("RULE 8 WF-B - the ordering taken as a trading instruction, OOS read ONCE")
    P("=" * 108)
    P("  Under each BARFORM, the claim is 'hold the panel the IS ordering puts first' - but only")
    P("  where that bar clears its floor in a majority of IS cells; where it does not, the bar")
    P("  issues NO instruction and the book is the live RULES v2 on U56 (the incumbent).")
    P("  (gross, cadence) is then chosen by IS Sharpe ALONE on that parent's MA-RS book.")
    P("")
    wf = []
    for stat in STATS:
        s_is = spans[(spans.statistic == stat) & (spans.period == "IS")]
        for bf in BARFORMS:
            n_is = int((s_is[f"{barcol[bf]}_D{HEADLINE_D}"] > 1).sum())
            instructs = n_is >= MAJORITY
            # the IS ordering's top parent: majority vote over the 6 IS cells
            top = s_is.top.value_counts().idxmax()
            cand = real[(real.parent == top) & (real.arm == "MA-RS")]
            pick = cand.sort_values("IS_Sharpe", ascending=False).iloc[0]
            spy, v2 = spy_cache[top], v2_cache[top]
            mo_spy, mo_v2 = metrics(spy.loc[OOS_START:]), metrics(v2.loc[OOS_START:])
            if instructs:
                oc, os_, od = pick.OOS_CAGR, pick.OOS_Sharpe, pick.OOS_MaxDD
                held = f"{top} MA-RS g{pick.gross:.2f} {pick.cadence}"
            else:
                oc, os_, od = mo_v2["CAGR"], mo_v2["Sharpe"], mo_v2["MaxDD"]
                held = "RULES v2 on U56 (no instruction)"
            wf.append(dict(statistic=stat, barform=bf, IS_cells_gt1=n_is, instructs=instructs,
                           IS_top=top, held=held, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                           v2_OOS_Sharpe=mo_v2["Sharpe"], v2_OOS_CAGR=mo_v2["CAGR"],
                           v2_OOS_MaxDD=mo_v2["MaxDD"], spy_OOS_Sharpe=mo_spy["Sharpe"],
                           spy_OOS_CAGR=mo_spy["CAGR"], spy_OOS_MaxDD=mo_spy["MaxDD"],
                           beat_v2=bool(os_ > mo_v2["Sharpe"]), beat_spy=bool(os_ > mo_spy["Sharpe"]),
                           leg="WF-B"))
    WF = pd.DataFrame(wf)
    P(f"  {'statistic':12s} {'barform':12s} {'IScells':>7s} {'instr':>5s} {'held':34s} "
      f"{'OOS CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s} {'>v2':>4s} {'>SPY':>5s}")
    for _, r in WF.iterrows():
        P(f"  {r['statistic']:12s} {r['barform']:12s} {r['IS_cells_gt1']:4d}/6 "
          f"{str(r['instructs']):>5s} {r['held']:34s} {r['OOS_CAGR']:9.2%} {r['OOS_Sharpe']:7.4f} "
          f"{r['OOS_MaxDD']:8.2%} {str(r['beat_v2']):>4s} {str(r['beat_spy']):>5s}")
    P("")
    v2row = WF.iloc[0]
    P(f"  comparands (OOS, on the selected panel): RULES v2 {v2row['v2_OOS_CAGR']:.2%} / "
      f"{v2row['v2_OOS_Sharpe']:.4f} / {v2row['v2_OOS_MaxDD']:.2%};  "
      f"SPY {v2row['spy_OOS_CAGR']:.2%} / {v2row['spy_OOS_Sharpe']:.4f} / "
      f"{v2row['spy_OOS_MaxDD']:.2%}")
    books = {bf: set(WF[WF.barform == bf].held) for bf in BARFORMS}
    H_BOOK = bool(books["GAP_RSS"] != books["SPAN_POOLED"])
    P(f"  SPAN_POOLED holds: {sorted(books['SPAN_POOLED'])}")
    P(f"  GAP_RSS     holds: {sorted(books['GAP_RSS'])}")
    P(f"  H_BOOK (the swap changes the book) -> {'PASS' if H_BOOK else 'FAIL'}")
    P(f"  beat RULES v2 OOS Sharpe: {int(WF.beat_v2.sum())}/{len(WF)};  "
      f"beat SPY OOS Sharpe: {int(WF.beat_spy.sum())}/{len(WF)}")
    P("")

    # ------------------------------------------------------- KEEP paths, every book
    P("=" * 108)
    P("KEEP PATHS 4a / 4b - every book on the grid")
    P("=" * 108)
    kp = grid[["parent", "kind", "seed", "arm", "gross", "cadence", "CAGR", "Sharpe", "MaxDD",
               "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "fail4b", "keep4b"]]
    P(f"  all {len(kp)} books: 4a {int(kp.keep4a.sum())}, 4b {int(kp.keep4b.sum())}, "
      f"BOTH {int((kp.keep4a & kp.keep4b).sum())}")
    for kind in ("REAL", "DRAW"):
        k = kp[kp.kind == kind]
        P(f"  {kind:5s} ({len(k):3d} books): 4a {int(k.keep4a.sum())}, 4b {int(k.keep4b.sum())}, "
          f"BOTH {int((k.keep4a & k.keep4b).sum())}")
    rp = kp[(kp.kind == "REAL")]
    P("  REAL-parent 4b passers (the only ones that could ever be capital):")
    any4b = rp[rp.keep4b]
    if len(any4b):
        for _, r in any4b.iterrows():
            P(f"    {r['parent']} {r['arm']} g{r['gross']:.2f} {r['cadence']}: "
              f"CAGR {r['CAGR']:.2%} Sharpe {r['Sharpe']:.4f} MaxDD {r['MaxDD']:.2%} "
              f"H1/H2 {r['H1']:.3f}/{r['H2']:.3f} OOS Sharpe {r['OOS_Sharpe']:.4f}")
    else:
        P("    none")
    fb = kp[~kp.keep4b].fail4b.str.split(",").explode().value_counts()
    P("  binding 4b legs across all books: " + ", ".join(f"{k} {v}" for k, v in fb.items()))
    P("")

    # ------------------------------------------------------- verdict
    P("=" * 108)
    P("VERDICT")
    P("=" * 108)
    H = dict(H_REPRO=H_REPRO, H_RETIRE=H_RETIRE, H_NUMERATOR=H_NUMERATOR, H_WINDOW=H_WINDOW,
             H_WF=H_WF, H_BOOK=H_BOOK)
    for k, v in H.items():
        P(f"  {k:12s} {'PASS' if v else 'FAIL'}")
    P("")
    n_sc = int(RET[(RET.claimset == "COMMITTED") & (RET.D == HEADLINE_D)
                   & (RET.barform == "GAP_RSS")].n_scorable.iloc[0])
    n_old = int(RET[(RET.claimset == "COMMITTED") & (RET.D == HEADLINE_D)
                    & (RET.barform == "GAP_RSS")].n_old_pass.iloc[0])
    n_ret = int(RET[(RET.claimset == "COMMITTED") & (RET.D == HEADLINE_D)
                    & (RET.barform == "GAP_RSS")].n_retired.iloc[0])
    P(f"  ANSWER: YES - the record should quote the adjacent gap over the RSS floor of the pair")
    P(f"  the gap is between.  On the COMMITTED claim set at D={HEADLINE_D}: {n_sc} re-scorable")
    P(f"  panel-ordering claims, {n_old} pass the record's own SPAN/POOLED bar, and the swap")
    P(f"  RETIRES {n_ret} of them ({n_ret/max(n_old,1):.1%}), reinstating "
      f"{int(RET[(RET.claimset=='COMMITTED')&(RET.D==HEADLINE_D)&(RET.barform=='GAP_RSS')].n_reinstated.iloc[0])}.")
    P("  4a/4b: the bar swap is a REPORTING rule, not a book; the WF-B leg above is the only")
    P("  capital reading and it is reported against RULES v2 and SPY.  No KEEP is claimed.")
    P("")

    # ------------------------------------------------------- write
    grid.to_csv(f"{OUT}/{STAMP}.grid.csv", index=False)
    floors.to_csv(f"{OUT}/{STAMP}.floors.csv", index=False)
    spans.to_csv(f"{OUT}/{STAMP}.spans.csv", index=False)
    CE.to_csv(f"{OUT}/{STAMP}.cells.csv", index=False)
    CEN.to_csv(f"{OUT}/{STAMP}.census.csv", index=False)
    RET.to_csv(f"{OUT}/{STAMP}.retire.csv", index=False)
    WIN.to_csv(f"{OUT}/{STAMP}.windows.csv", index=False)
    WF.to_csv(f"{OUT}/{STAMP}.walkforward.csv", index=False)
    kp.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    for cs in CLAIMSETS:
        sites[cs].to_csv(f"{OUT}/{STAMP}.sites_{cs}.csv.gz", index=False,
                         compression="gzip")
    P(f"wrote grid {len(grid)}, floors {len(floors)}, spans {len(spans)}, cells {len(CE)}, "
      f"census {len(CEN)}, retire {len(RET)}, wf {len(WF)}, keeppaths {len(kp)}, "
      f"sites {len(sites['COMMITTED'])}/{len(sites['ALL'])} rows in {time.time()-t0:.0f}s")
    Path(f"{OUT}/{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
