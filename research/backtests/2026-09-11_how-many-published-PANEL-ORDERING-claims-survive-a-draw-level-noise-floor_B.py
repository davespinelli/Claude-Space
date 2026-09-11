#!/usr/bin/env python3
"""Idea 567 (lane B, 2026-09-11) - how-many-published-PANEL-ORDERING-claims-survive-a-draw-level-noise-floor.

QUESTION
--------
Idea 312 measured the within-rung sd of the MA-gate premium across six same-ETF-share 36-name
draws at 0.0745 Sharpe - 0.76x the ENTIRE published U56 > B136 > SMALL439 gap of 0.0978 - and
found 39.4% of same-s draw pairs crossing that gap.  If one panel's own composition luck moves
the statistic by as much as the published spread between panels, then every claim of the form
"characteristic X orders the three panels" is a THREE-DRAW claim quoted without its error bar.

This run does two things:
  (A) PRICE LEG - rebuild the draw-level noise floor from source, per STATISTIC and per
      DRAW COUNT, drawing k=36 name panels out of each of the three REAL parents (not just
      out of B136 as idea 312 did).  The floor is the within-parent sd of the statistic
      across independent k-matched draws.
  (B) CENSUS LEG - harvest every committed claim in the record that quotes a number against
      two or three of {U56, B136, SMALL439} in the same sentence, recover its margin (the
      smallest adjacent gap in the quoted ordering), classify it to a statistic family, and
      score margin against that family's own floor.

A claim whose margin is inside its own floor is not evidence about panels; it is one draw of
a composition lottery.

DESIGN
------
Parents (the record's three panels, each truncated to its own last bar):
    U56       research/universe.json          56 names, 64.3% ETF
    B136      research/universe_broad.json   136 names, 26.5% ETF
    SMALL439  data/prices_small.csv.gz       439 names,  0% ETF (max_1d_move < 1.0 filter)
Draws: k = 36 names per draw, 24 seeds per parent, drawn with the record's crc32 scheme
    `DRAW|{parent}|{seed}` so the draws are reproducible objects.  k is 36 at every parent,
    so panel WIDTH is never confounded with parent identity.  U56 draws 36 of 56, so its
    draws OVERLAP heavily by construction and its floor is structurally the smallest - that
    is reported, not corrected.

Arms (idea 51 / idea 312 verbatim):
    EWall  gross g spread equally over every priced tradable name          (CONTROL)
    MA-RS  gross g spread equally over names above their 200d MA (RESPREAD) (TREATMENT)
RESPREAD holds gross fixed, so a premium arm-minus-arm is pure selection, no exposure dial.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. STATISTIC in {PREM_SHARPE, PREM_CAGR, SHARPE, CAGR, MAXDD}
    2. DRAW COUNT D in {3, 6, 12, 24}      (nested: D uses the first D of the 24 seeds)
Every one of the 5 x 4 = 20 grid points is reported, at every gross and cadence.
REPORTED (not tuned) axes: gross g in {0.50, 0.75, 1.00}, cadence in {W, M}, and the bar
    multiple b in {1.0, 2.0} sd.  Nothing is selected on any of them.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
-----------------------------------------------------------------
GAP312 = 0.0978  (published U56 - SMALL439 MA-gate premium gap, idea 51 via idea 312)
SD312  = 0.0745  (idea 312's committed within-rung seed sd)
H_FLOOR : the pooled PREM_SHARPE floor at D=6 lands within 2x of SD312 (i.e. in
          [0.0373, 0.1490]).  Falsified if the floor built on the REAL parents is an
          order of magnitude away from the one idea 312 built inside B136.
H_MOST  : a MAJORITY (>50%) of harvested panel-ordering claims have margin < 1.0 sd of
          their own family floor at D=6.  This is the queue's alarm stated as a number.
H_PARENT: the floor is NOT parent-invariant - max over parents / min over parents >= 1.5
          for PREM_SHARPE at D=6.  If it holds, a single pooled floor is the wrong bar and
          a claim must be scored against the floor of the parents it names.
H_D     : the floor is roughly flat in D (sd is a consistent estimator), so the SHARE of
          claims inside the floor moves less than 10 pp from D=3 to D=24.  If it moves
          more, "inside its floor" is itself a resolution statement (idea 528's problem).

GATES (run and printed before any new number is read)
    G0 determinism: the draw scheme rebuilt twice gives identical name sets.       bar 0
    G1 identity: fast_backtest vs engine.backtest on one book per parent.       bar 1e-12
    G2 reproduction: idea 312's committed .noisefloor.csv recomputed from its own committed
       .grid.csv (per-rung sd, range, pair-crossing counts), all 11 rungs.        bar 1e-12
    G3 reproduction: idea 312's headline 0.0745 mean within-rung sd and 65/165 = 39.4%
       pair-crossing share, recomputed from the same committed grid.              bar 1e-4

RULE 8 WALK-FORWARD (required, run whatever the census says)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: rebuild the floor on IS returns only and on OOS returns only and
       report whether the same claims fall inside it (sign/stability of the verdict).
    WF-B on a BOOK: the panel-ordering claim, taken at face value, is a TRADING instruction
       ("run the book on the panel the ordering puts first").  Select (parent, D-draw
       pick) by IS Sharpe alone, then read OOS CAGR/Sharpe/MaxDD ONCE against RULES v2 on
       the same panel and against SPY.  If the ordering is composition luck, the IS-chosen
       panel should not beat its siblings OOS.

KEEP PATHS: 4a (Sharpe > live RULES v2 on the same panel in BOTH halves and MaxDD no worse)
    and 4b (Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of
    SPY's) are evaluated for EVERY book on the grid and the counts reported.  Stated up
    front: a DRAW panel is a seeded random 36-name subset, NOT a rule anyone can trade, so
    a 4b pass on a draw is a diagnostic, not a capital candidate; only the REAL parents'
    books can be capital candidates.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents, so every
    stock-side level carries a survivorship premium.  On an arm-minus-arm premium measured
    on the SAME panel that bias largely cancels; on the LEVEL statistics (SHARPE, CAGR,
    MAXDD) it does not, and those floors are therefore lower bounds on the true dispersion.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py; modifies nothing but its
own outputs: .grid.csv .floors.csv .census.csv .verdicts.csv .walkforward.csv .keeppaths.csv
.console.txt
"""
from __future__ import annotations

import json
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
BARS = [1.0, 2.0]
STATS = ["PREM_SHARPE", "PREM_CAGR", "SHARPE", "CAGR", "MAXDD"]

GAP312 = 0.0978
SD312 = 0.0745
PARENT312 = OUT / "2026-09-09_is-the-panel-ordering-an-ETF-SHARE-effect_B"
G1_TOL = 1e-12
G2_TOL = 1e-12
G3_TOL = 1e-4

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


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
    """crc32-seeded k-matched draws, `DRAW|{parent}|{seed}`."""
    pool = np.array(sorted(names))
    out = []
    for sd in range(n_seed):
        seed = zlib.crc32(f"DRAW|{parent}|{sd}".encode()) % (2 ** 32)
        rng = np.random.default_rng(seed)
        pick = sorted(rng.choice(pool, size=min(k, len(pool)), replace=False).tolist())
        out.append((sd, pick))
    return out


# ------------------------------------------------------------------------- census
PANELS_RE = re.compile(r"\b(U56|B136|SMALL\d{2,4}|SMALL)\b")
NUM_RE = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")
FAMILY_KEYS = [
    ("PREM_SHARPE", ("premium", "dsharpe", "d sharpe", "advantage", "gate premium", "selection")),
    ("PREM_CAGR", ("dcagr", "d cagr", "pp/yr", "pp / yr")),
    ("SHARPE", ("sharpe",)),
    ("CAGR", ("cagr", "return")),
    ("MAXDD", ("maxdd", "max dd", "drawdown", "dd")),
]


def classify(text):
    t = text.lower()
    for fam, keys in FAMILY_KEYS:
        if any(k in t for k in keys):
            return fam
    return None


def sentences(txt):
    txt = txt.replace("\n", " ")
    return re.split(r"(?<=[.;!?])\s+|\|", txt)


def harvest(paths):
    """Committed sentences quoting a number against >=2 of the three panels."""
    rows = []
    for p in paths:
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        for s in sentences(txt):
            if len(s) > 600:
                continue
            found = PANELS_RE.findall(s)
            fams = {("SMALL" if f.startswith("SMALL") else f) for f in found}
            if len(fams) < 2:
                continue
            fam = classify(s)
            if fam is None:
                continue
            # a value is the first number following each panel token
            vals = {}
            for m in PANELS_RE.finditer(s):
                key = "SMALL" if m.group(1).startswith("SMALL") else m.group(1)
                tail = s[m.end(): m.end() + 40]
                nums = [float(x) for x in NUM_RE.findall(tail)
                        if not re.fullmatch(r"[-+]?\d{2,4}", x)]
                if nums and key not in vals:
                    vals[key] = nums[0]
            if len(vals) < 2:
                continue
            order = sorted(vals.values())
            gaps = [b - a for a, b in zip(order, order[1:])]
            margin = min(gaps) if gaps else np.nan
            if not np.isfinite(margin):
                continue
            rows.append(dict(file=p.name, family=fam, n_panels=len(vals),
                             margin=abs(margin), span=abs(order[-1] - order[0]),
                             claim=s.strip()[:240]))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P(f"# idea 567 - do published PANEL-ORDERING claims clear a draw-level noise floor?")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS<= {IS_END}, OOS >= {OOS_START}")
    P("")

    parents = real_panels()
    pnames = list(parents)
    P("PARENTS:", ", ".join(f"{k} ({len(v[1])} names, {v[0].index[0].date()}..{v[0].index[-1].date()})"
                            for k, v in parents.items()))
    P("")

    # ---------------------------------------------------------------- G0 determinism
    P("=" * 100)
    P("GATES")
    P("=" * 100)
    g0 = 0
    for pn, (_, names) in parents.items():
        a = [set(x[1]) for x in draws(pn, names)]
        b = [set(x[1]) for x in draws(pn, names)]
        g0 += sum(0 if x == y else 1 for x, y in zip(a, b))
        assert all(len(x) == min(K_DRAW, len(names)) for x in a)
    P(f"G0 determinism  : {g0} of {N_SEED*len(parents)} draws differ on rebuild "
      f"(bar 0) -> {'PASS' if g0 == 0 else 'FAIL'}")

    # ---------------------------------------------------------------- G1 identity
    g1 = 0.0
    for pn, (px, names) in parents.items():
        bk = make_books(px, set(names), 0.75)["MA-RS"]
        a = fast_backtest(px, bk, freq="W")["returns"]
        b = backtest(px, bk, cost_bps=COST, freq="W")["returns"]
        g1 = max(g1, float(np.abs(a.values - b.values).max()))
    P(f"G1 identity     : fast_backtest vs engine.backtest max |dret| = {g1:.3e} "
      f"(bar {G1_TOL:.0e}) -> {'PASS' if g1 <= G1_TOL else 'FAIL'}")

    # ------------------------------------------------- G2/G3 reproduce idea 312's floor
    g2 = g3a = g3b = float("nan")
    try:
        pg = pd.read_csv(f"{PARENT312}.grid.csv")
        pf = pd.read_csv(f"{PARENT312}.noisefloor.csv")
        mix = pg[(pg.kind == "MIX") & (pg.arm == "MA-RS")].copy()
        # idea 312's premium is dSharpe_vs_EWall; its rung statistic pools (g, cadence)
        per = (mix.groupby(["flavour", "etf_share", "seed"])["dSharpe_vs_EWall"]
                  .mean().reset_index())
        recomp = []
        for (fl, s), grp in per.groupby(["flavour", "etf_share"]):
            v = grp["dSharpe_vs_EWall"].to_numpy()
            pr = [abs(a - b) for i, a in enumerate(v) for b in v[i + 1:]]
            recomp.append(dict(flavour=fl, etf_share=s, n_seed=len(v), lo=v.min(), hi=v.max(),
                               rng=v.max() - v.min(), sd=v.std(ddof=1), pairs=len(pr),
                               pairs_ge_GAP=sum(1 for x in pr if x > GAP312)))
        rc = pd.DataFrame(recomp)
        mg = pf.merge(rc, on=["flavour", "etf_share"], suffixes=("_c", "_r"))
        assert len(mg) == len(pf), (len(mg), len(pf))
        g2 = max(float(np.abs(mg[f"{c}_c"] - mg[f"{c}_r"]).max())
                 for c in ["lo", "hi", "rng", "sd", "pairs", "pairs_ge_GAP"])
        g3a = abs(float(rc["sd"].mean()) - SD312)
        g3b = abs(float(rc["pairs_ge_GAP"].sum() / rc["pairs"].sum()) - 0.394)
    except Exception as e:  # pragma: no cover - reported, never silently skipped
        P(f"G2/G3 reproduction: could not read idea 312's artefacts ({e!r})")
    P(f"G2 reproduction : idea 312 .noisefloor.csv rebuilt from its own .grid.csv, "
      f"all {len(pf) if 'pf' in dir() else 0} rungs, max |d| = {g2:.3e} "
      f"(bar {G2_TOL:.0e}) -> {'PASS' if g2 <= G2_TOL else 'FAIL'}")
    P(f"G3 reproduction : idea 312 headline mean within-rung sd |d| = {g3a:.3e} vs {SD312}; "
      f"pair-crossing share |d| = {g3b:.3e} vs 0.394 (bar {G3_TOL:.0e}) -> "
      f"{'PASS' if max(g3a, g3b) <= G3_TOL else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- price grid
    P("=" * 100)
    P("PRICE LEG - 36-name draws out of each real parent")
    P("=" * 100)
    rows = []
    spy_cache = {}
    for pn, (px, names) in parents.items():
        spy = px["SPY"].pct_change().fillna(0.0)
        spy_cache[pn] = spy
        units = [("REAL", -1, sorted(names))] + [("DRAW", sd, pick) for sd, pick in draws(pn, names)]
        for kind, sd, pick in units:
            cols = list(dict.fromkeys(pick + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
            for g in GROSS:
                bks = make_books(sub, set(pick), g)
                for cad in CADENCE:
                    res = {a: fast_backtest(sub, w, freq=cad) for a, w in bks.items()}
                    warm = sub.index[260]
                    base = {a: r["returns"].loc[warm:] for a, r in res.items()}
                    for arm in ("EWall", "MA-RS"):
                        r = base[arm]
                        d = rowify(r, res[arm]["turnover"].loc[warm:])
                        d.update(parent=pn, kind=kind, seed=sd, arm=arm, gross=g, cadence=cad,
                                 k=len(pick))
                        d["dSharpe_vs_EWall"] = d["Sharpe"] - metrics(base["EWall"])["Sharpe"]
                        d["dCAGR_vs_EWall"] = d["CAGR"] - metrics(base["EWall"])["CAGR"]
                        d["IS_dSharpe"] = (metrics(r.loc[:IS_END])["Sharpe"]
                                           - metrics(base["EWall"].loc[:IS_END])["Sharpe"])
                        d["OOS_dSharpe"] = (metrics(r.loc[OOS_START:])["Sharpe"]
                                            - metrics(base["EWall"].loc[OOS_START:])["Sharpe"])
                        rows.append(d)
        P(f"  {pn}: {len(units)} panels x {len(GROSS)} gross x {len(CADENCE)} cadence x 2 arms "
          f"done ({time.time()-t0:.0f}s)")
    grid = pd.DataFrame(rows)

    # baselines per parent (RULES v2 on the full parent) + SPY
    P("")
    bases = {}
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b = fast_backtest(px, rules_v2_weights(px), freq="W")["returns"].loc[warm:]
        bases[pn] = b
        s = spy_cache[pn].loc[warm:]
        P(f"  BASE {pn}: RULES v2 {metrics(b)['CAGR']:.2%} / {metrics(b)['Sharpe']:.4f} / "
          f"{metrics(b)['MaxDD']:.2%} (OOS {metrics(b.loc[OOS_START:])['Sharpe']:.4f})   "
          f"SPY {metrics(s)['CAGR']:.2%} / {metrics(s)['Sharpe']:.4f} / {metrics(s)['MaxDD']:.2%} "
          f"(OOS {metrics(s.loc[OOS_START:])['Sharpe']:.4f})")

    # KEEP paths for every book on the grid
    keeps = []
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b = bases[pn]
        s = spy_cache[pn].loc[warm:]
        sel = grid[grid.parent == pn]
        for _, rr in sel.iterrows():
            keeps.append(dict(parent=pn, kind=rr["kind"], seed=rr["seed"], arm=rr["arm"],
                              gross=rr["gross"], cadence=rr["cadence"]))
    # recompute cheaply from stored metrics: rebuild returns is expensive, so re-run per book
    kp_rows = []
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b, s = bases[pn], spy_cache[pn].loc[warm:]
        units = [("REAL", -1, sorted(names))] + [("DRAW", sd, pick) for sd, pick in draws(pn, names)]
        for kind, sd, pick in units:
            cols = list(dict.fromkeys(pick + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
            for g in GROSS:
                bks = make_books(sub, set(pick), g)
                for cad in CADENCE:
                    for arm, w in bks.items():
                        r = fast_backtest(sub, w, freq=cad)["returns"].loc[warm:]
                        f4b = fail_4b(r, s)
                        kp_rows.append(dict(parent=pn, kind=kind, seed=sd, arm=arm, gross=g,
                                            cadence=cad, keep4a=keep_4a(r, b),
                                            fail4b=f4b, keep4b=(f4b == "-")))
    kp = pd.DataFrame(kp_rows)
    P("")
    P(f"KEEP PATHS over {len(kp)} books: 4a {int(kp.keep4a.sum())}/{len(kp)}, "
      f"4b {int(kp.keep4b.sum())}/{len(kp)}, BOTH {int((kp.keep4a & kp.keep4b).sum())}/{len(kp)}")
    P("  4a by parent: " + ", ".join(f"{k} {int(v)}" for k, v in kp.groupby('parent').keep4a.sum().items()))
    P("  4b by parent: " + ", ".join(f"{k} {int(v)}" for k, v in kp.groupby('parent').keep4b.sum().items()))
    P("  4b by kind  : " + ", ".join(f"{k} {int(v)}" for k, v in kp.groupby('kind').keep4b.sum().items()))
    P("  4b binding failure legs: " + ", ".join(
        f"{k} {v}" for k, v in kp.fail4b.value_counts().head(6).items()))

    # ---------------------------------------------------------------- floors
    P("")
    P("=" * 100)
    P("FLOORS - within-parent sd across k-matched draws, by (STATISTIC, DRAW COUNT)")
    P("=" * 100)

    def stat_series(sub, stat, period="FULL"):
        pre = {"FULL": "", "IS": "IS_", "OOS": "OOS_"}[period]
        ma = sub[sub.arm == "MA-RS"]
        if stat == "PREM_SHARPE":
            col = {"FULL": "dSharpe_vs_EWall", "IS": "IS_dSharpe", "OOS": "OOS_dSharpe"}[period]
            return ma[col]
        if stat == "PREM_CAGR":
            if period != "FULL":
                ew = sub[sub.arm == "EWall"].set_index(["seed", "gross", "cadence"])[pre + "CAGR"]
                m2 = ma.set_index(["seed", "gross", "cadence"])[pre + "CAGR"]
                return (m2 - ew.reindex(m2.index))
            return ma["dCAGR_vs_EWall"]
        return ma[pre + {"SHARPE": "Sharpe", "CAGR": "CAGR", "MAXDD": "MaxDD"}[stat]]

    fl_rows = []
    dr = grid[grid.kind == "DRAW"]
    for stat in STATS:
        for D in DRAW_COUNTS:
            for period in ("FULL", "IS", "OOS"):
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
                pooled = float(np.nanmean(list(per_parent.values())))
                row = dict(statistic=stat, D=D, period=period, floor_pooled=pooled,
                           floor_max=float(np.nanmax(list(per_parent.values()))),
                           floor_min=float(np.nanmin(list(per_parent.values()))))
                row.update({f"floor_{k}": v for k, v in per_parent.items()})
                row["parent_ratio"] = row["floor_max"] / row["floor_min"] if row["floor_min"] else np.nan
                fl_rows.append(row)
    floors = pd.DataFrame(fl_rows)
    P(fmt(floors[floors.period == "FULL"].set_index(["statistic", "D"])
          [["floor_pooled", "floor_min", "floor_max", "parent_ratio"]], 4))

    f6 = floors[(floors.statistic == "PREM_SHARPE") & (floors.D == 6) & (floors.period == "FULL")].iloc[0]
    P("")
    P(f"H_FLOOR : pooled PREM_SHARPE floor at D=6 = {f6.floor_pooled:.4f} vs idea 312's "
      f"{SD312} (ratio {f6.floor_pooled/SD312:.2f}x) -> "
      f"{'HOLDS' if 0.5*SD312 <= f6.floor_pooled <= 2*SD312 else 'FALSIFIED'}")
    _pf = ", ".join("%s %.4f" % (p, f6["floor_" + p]) for p in pnames)
    P(f"H_PARENT: parent max/min = {f6.parent_ratio:.2f}x ({_pf}) -> "
      f"{'HOLDS' if f6.parent_ratio >= 1.5 else 'FALSIFIED'}")

    # ---------------------------------------------------------------- census
    P("")
    P("=" * 100)
    P("CENSUS - committed panel-ordering claims")
    P("=" * 100)
    paths = (sorted(OUT.glob("*.result.md")) + sorted(OUT.glob("*.memo.md"))
             + sorted(OUT.glob("*.md")) + sorted((ROOT / "research").glob("*.md")))
    paths = sorted({p for p in paths if p.is_file()})
    cen = harvest(paths)
    P(f"scanned {len(paths)} committed markdown files -> {len(cen)} harvested claims "
      f"quoting >=2 panels with a recoverable number")
    if len(cen):
        P("by family: " + ", ".join(f"{k} {v}" for k, v in cen.family.value_counts().items()))
        P("by panel count: " + ", ".join(f"{k}-panel {v}" for k, v in cen.n_panels.value_counts().items()))
        P(f"margin: median {cen.margin.median():.4f}, p25 {cen.margin.quantile(.25):.4f}, "
          f"p75 {cen.margin.quantile(.75):.4f}, max {cen.margin.max():.4f}")

    # ---------------------------------------------------------------- verdicts
    P("")
    P("=" * 100)
    P("VERDICTS - claim margin vs its own family floor (all 5 x 4 x 2 grid points reported)")
    P("=" * 100)
    ver = []
    for stat in STATS:
        sub = cen[cen.family == stat] if len(cen) else cen
        for D in DRAW_COUNTS:
            fl = floors[(floors.statistic == stat) & (floors.D == D) & (floors.period == "FULL")].iloc[0]
            for bar in BARS:
                thr = bar * fl.floor_pooled
                n = len(sub)
                inside = int((sub.margin < thr).sum()) if n else 0
                ver.append(dict(statistic=stat, D=D, bar=bar, floor=fl.floor_pooled,
                                threshold=thr, n_claims=n, inside=inside,
                                share_inside=(inside / n if n else np.nan)))
    verd = pd.DataFrame(ver)
    P(fmt(verd.set_index(["statistic", "D", "bar"])[["floor", "threshold", "n_claims",
                                                     "inside", "share_inside"]], 4))

    tot = verd[(verd.D == 6) & (verd.bar == 1.0)]
    n_tot = int(tot.n_claims.sum())
    i_tot = int(tot.inside.sum())
    sh6 = i_tot / n_tot if n_tot else np.nan
    P("")
    P(f"H_MOST  : at D=6, bar 1.0 sd -> {i_tot} of {n_tot} claims ({sh6:.1%}) are inside their "
      f"own floor -> {'HOLDS' if sh6 > 0.5 else 'FALSIFIED'}")
    sh_by_D = {}
    for D in DRAW_COUNTS:
        t = verd[(verd.D == D) & (verd.bar == 1.0)]
        sh_by_D[D] = float(t.inside.sum() / t.n_claims.sum()) if t.n_claims.sum() else np.nan
    swing = (max(sh_by_D.values()) - min(sh_by_D.values())) * 100
    P(f"H_D     : share inside by D = " + ", ".join(f"D{k} {v:.1%}" for k, v in sh_by_D.items())
      + f"  (swing {swing:.1f} pp) -> {'HOLDS' if swing < 10 else 'FALSIFIED'}")

    # ---------------------------------------------------------------- WF-A
    P("")
    P("=" * 100)
    P("RULE 8 WALK-FORWARD")
    P("=" * 100)
    P("WF-A (the ANSWER): floor rebuilt on IS only and on OOS only; does the verdict move?")
    wfa = []
    for stat in STATS:
        sub = cen[cen.family == stat] if len(cen) else cen
        r = {}
        for period in ("FULL", "IS", "OOS"):
            fl = floors[(floors.statistic == stat) & (floors.D == 6) & (floors.period == period)].iloc[0]
            r[period] = fl.floor_pooled
            r["in_" + period] = int((sub.margin < fl.floor_pooled).sum()) if len(sub) else 0
        wfa.append(dict(statistic=stat, n_claims=len(sub), floor_FULL=r["FULL"], floor_IS=r["IS"],
                        floor_OOS=r["OOS"], inside_FULL=r["in_FULL"], inside_IS=r["in_IS"],
                        inside_OOS=r["in_OOS"]))
    wfa = pd.DataFrame(wfa)
    P(fmt(wfa.set_index("statistic"), 4))
    if len(cen):
        agree = int((wfa.inside_IS == wfa.inside_OOS).sum())
        P(f"  IS and OOS floors put the SAME count inside in {agree} of {len(wfa)} statistic families.")

    # ---------------------------------------------------------------- WF-B
    P("")
    P("WF-B (a BOOK): take the ordering claim at face value - trade the panel it puts first.")
    P("  Selector: (parent, gross, cadence) chosen by IS Sharpe of the MA-RS book ALONE, on the")
    P("  REAL parents; OOS 2017+ read ONCE against RULES v2 on that panel and SPY.")
    wfb = []
    real = grid[(grid.kind == "REAL") & (grid.arm == "MA-RS")]
    pick = real.sort_values("IS_Sharpe", ascending=False).iloc[0]
    for _, rr in real.iterrows():
        b = bases[rr["parent"]]
        s = spy_cache[rr["parent"]]
        warm = parents[rr["parent"]][0].index[260]
        wfb.append(dict(parent=rr["parent"], gross=rr["gross"], cadence=rr["cadence"],
                        IS_Sharpe=rr["IS_Sharpe"], OOS_CAGR=rr["OOS_CAGR"],
                        OOS_Sharpe=rr["OOS_Sharpe"], OOS_MaxDD=rr["OOS_MaxDD"],
                        base_OOS_Sharpe=metrics(b.loc[OOS_START:])["Sharpe"],
                        base_OOS_CAGR=metrics(b.loc[OOS_START:])["CAGR"],
                        base_OOS_MaxDD=metrics(b.loc[OOS_START:])["MaxDD"],
                        spy_OOS_Sharpe=metrics(s.loc[warm:].loc[OOS_START:])["Sharpe"],
                        spy_OOS_CAGR=metrics(s.loc[warm:].loc[OOS_START:])["CAGR"],
                        spy_OOS_MaxDD=metrics(s.loc[warm:].loc[OOS_START:])["MaxDD"],
                        selected=(rr["parent"] == pick["parent"] and rr["gross"] == pick["gross"]
                                  and rr["cadence"] == pick["cadence"])))
    wfb = pd.DataFrame(wfb)
    P(fmt(wfb.set_index(["parent", "gross", "cadence"]), 4))
    sel = wfb[wfb.selected].iloc[0]
    P("")
    P(f"  SELECTED on IS Sharpe alone: {sel['parent']} gross {sel['gross']:.2f} cadence {sel['cadence']} "
      f"(IS Sharpe {sel['IS_Sharpe']:.4f})")
    P(f"  OOS ONCE: CAGR {sel['OOS_CAGR']:.2%} / Sharpe {sel['OOS_Sharpe']:.4f} / MaxDD {sel['OOS_MaxDD']:.2%}")
    P(f"     vs RULES v2 (same panel): {sel['base_OOS_CAGR']:.2%} / {sel['base_OOS_Sharpe']:.4f} / "
      f"{sel['base_OOS_MaxDD']:.2%}    {'BEATS' if sel['OOS_Sharpe'] > sel['base_OOS_Sharpe'] else 'LOSES TO'} baseline on Sharpe")
    P(f"     vs SPY                 : {sel['spy_OOS_CAGR']:.2%} / {sel['spy_OOS_Sharpe']:.4f} / "
      f"{sel['spy_OOS_MaxDD']:.2%}    {'BEATS' if sel['OOS_Sharpe'] > sel['spy_OOS_Sharpe'] else 'LOSES TO'} SPY on Sharpe")
    n_beat_b = int((wfb.OOS_Sharpe > wfb.base_OOS_Sharpe).sum())
    n_beat_s = int((wfb.OOS_Sharpe > wfb.spy_OOS_Sharpe).sum())
    P(f"  ACROSS ALL {len(wfb)} REAL books: beat RULES v2 OOS {n_beat_b}/{len(wfb)}, "
      f"beat SPY OOS {n_beat_s}/{len(wfb)}")

    # does the IS panel ordering predict the OOS panel ordering?
    P("")
    P("  ORDERING STABILITY (the claim's real content): rank the three parents by the")
    P("  MA-gate premium IS, then OOS, at every (gross, cadence).")
    st = []
    for g in GROSS:
        for cad in CADENCE:
            r = real[(real.gross == g) & (real.cadence == cad)]
            o_is = list(r.sort_values("IS_dSharpe", ascending=False).parent)
            o_oos = list(r.sort_values("OOS_dSharpe", ascending=False).parent)
            st.append(dict(gross=g, cadence=cad, IS_order=">".join(o_is), OOS_order=">".join(o_oos),
                           same=o_is == o_oos,
                           IS_span=float(r.IS_dSharpe.max() - r.IS_dSharpe.min()),
                           OOS_span=float(r.OOS_dSharpe.max() - r.OOS_dSharpe.min())))
    stb = pd.DataFrame(st)
    P(fmt(stb.set_index(["gross", "cadence"]), 4))
    fl_is = floors[(floors.statistic == "PREM_SHARPE") & (floors.D == 6) & (floors.period == "IS")].iloc[0]
    fl_oos = floors[(floors.statistic == "PREM_SHARPE") & (floors.D == 6) & (floors.period == "OOS")].iloc[0]
    P(f"  IS order == OOS order in {int(stb.same.sum())} of {len(stb)} (gross, cadence) cells.")
    P(f"  median IS span {stb.IS_span.median():.4f} vs IS floor {fl_is.floor_pooled:.4f} "
      f"({stb.IS_span.median()/fl_is.floor_pooled:.2f}x); median OOS span {stb.OOS_span.median():.4f} "
      f"vs OOS floor {fl_oos.floor_pooled:.4f} ({stb.OOS_span.median()/fl_oos.floor_pooled:.2f}x)")

    # ---------------------------------------------------------------- write
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    floors.to_csv(OUT / f"{STAMP}.floors.csv", index=False)
    (cen if len(cen) else pd.DataFrame(columns=["file", "family", "margin"])).to_csv(
        OUT / f"{STAMP}.census.csv", index=False)
    verd.to_csv(OUT / f"{STAMP}.verdicts.csv", index=False)
    pd.concat([wfb.assign(leg="WF-B"), stb.assign(leg="ORDER")], ignore_index=True).to_csv(
        OUT / f"{STAMP}.walkforward.csv", index=False)
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P("")
    P(f"wrote grid {len(grid)} rows, floors {len(floors)}, census {len(cen)}, verdicts {len(verd)}, "
      f"keeppaths {len(kp)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
