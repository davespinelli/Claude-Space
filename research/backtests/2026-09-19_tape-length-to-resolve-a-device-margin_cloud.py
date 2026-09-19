#!/usr/bin/env python3
"""Idea 1570 — how LONG a TAPE would RESOLVE the record's TYPICAL DEVICE MARGIN, and is ANY of it
REACHABLE?  Plus the constructive half: does POOLING a device family's cells under a SINGLE paired
block bootstrap resolve what the per-cell reading cannot?

THE PROBLEM.  Idea 1562 produced the record's first non-dominated drawdown device and could not
resolve it: 0 of 36 paired-bootstrap contrasts reached |t| > 2, best +1.52 full / +0.94 OOS on a
margin of +0.0238 of Sharpe.  Idea 1511 hit the same wall on MaxDD (2.93 pp SE against a 1.10 pp
margin).  Eight-plus runs on 2026-09-19 all ended "the margin is inside its own SE".  This run
inverts the question instead of asking it again.

ARM A — THE CENSUS (how long a tape would it take?).  Every committed CSV this repo carries for
2026-09-19 is scanned for INTERNALLY VALIDATED (difference, standard error, t) triples: a column
trio (d, s, t) is admitted only if `s` is named like a standard error, `t` is named like a t
statistic, and d/s reproduces t to 1e-6 on >= 98% of finite rows with >= 3 distinct t values (so
constant / boolean columns cannot match by accident).  For each admitted row the bootstrap SE
scales as 1/sqrt(n), so the tape length needed for |t| = 2 is

        n*  =  n_window * (2 / |t|)^2          ->   EXTRA trading days = n_window * (m - 1)

with m = (2/|t|)^2 the REQUIRED MULTIPLE — a window-free statistic.  A contrast is REACHABLE
BEFORE 2050 iff its extra requirement is <= 24 years x 252 = 6048 trading days of new tape.

ARM B — THE POOLED RULER (does pooling resolve anything?).  The device family is idea 1562's own:
the frozen incumbent book (N=20, H=126, MAXVOL 0.60, weekly, gross 0.75) run at gross 0.75 when SPY
is above its own MA and at g_low when it is below, each cell priced against the CONSTANT gross
whose FULL-sample CAGR it matches (the de-gross twin the record keeps finding dominant).  12 cells
(4 MA lengths x 3 g_low) x 2 large-cap panels = THE 24 LARGE-CAP CELLS.  The pooled ruler draws ONE
circular-block index set per replicate and applies it to ALL 24 cells and their 24 twins at once,
so the cells' dependence (same tape, same frame) is carried, not assumed away.

TUNED PARAMETERS: exactly TWO — BLOCK LENGTH L in {21, 63, 126} and POOLING SCHEME in {EQ, PREC}.
All 6 combinations are published; nothing is selected on.  The MA ladder, the g_low ladder and the
cost ladder are the family's own coordinates, inherited from 1562, and are published in full.

ARM C — THE CAPITAL ARM (rule 8).  On each of three panels the cell is chosen by argmax IS Sharpe
on warm-up..2016-12-31 ONLY; 2017-01-01..end is read exactly once and reported against the LIVE
RULES v2 baseline and SPY, with both KEEP paths at every cell, full and OOS.  The pick's own margin
is then re-read under the pooled ruler.

PRE-REGISTERED VERDICT RULE (written before the run).
  H_WALL   ARM A's median required multiple is > 4 (i.e. the typical committed contrast needs more
           than 4x its own tape) AND ARM B's pooled |t| <= 2 at EVERY one of the 6 (L, scheme)
           combinations.  Then pooling buys nothing, the wall is structural, and the honest verdict
           is KILL-for-capital: the family cannot be adjudicated on any tape this century.
  H_POOL   pooled |t| > 2 at a MAJORITY (>= 4 of 6) of the combinations AND the rule-8 pick beats
           its own twin OUT OF SAMPLE.  Then the pooled ruler is the first ruler in the record that
           adjudicates a device family, and the capital arm is a KEEP-candidate.
  Anything in between is PARK.

PROTOCOL: rule 1 (>= 10y); rule 2 (weights decided at t-1 applied at t, 10 bps headline, no
shorting, no leverage — every gross rung is <= 1.00 and the low state only ever CUTS); rule 3
(compared to the live RULES v2 baseline AND SPY); rule 4 (full + both halves, both KEEP paths at
EVERY cell); rule 8 (parameters chosen on warm-up..2016-12-31 only, 2017-01-01..end read exactly
once); rule 9 (survivorship stated).

GATES.  G0 >= 10y.  G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor.
G2 cross-script replay of idea 1562's own headline cell (U56, MA 200, g_low 0.5625, 10 bps).
G3 exactly two tuned parameters.  G4 CAGR match quality < 20 bp on every matched twin.
G5 no chooser reads a row on or after 2017-01-01.  G6 gross in [0, 1] on every book.
G7 the cost ladder is an identity on the SAME turnover path.  G8 every cell published.
G9 the census matcher admits no constant/boolean column (>= 3 distinct t per admitted triple).

Runs standalone and offline (committed caches and this repo's own committed CSVs; no network):
  python research/backtests/2026-09-19_tape-length-to-resolve-a-device-margin_cloud.py
"""
from __future__ import annotations

import glob
import re
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-19"
SLUG = "tape-length-to-resolve-a-device-margin"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"        # the frozen incumbent
COSTS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_COST = 10.0
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

MAS = [100, 150, 200, 250]                                # the family's own coordinate
GLOWS = [0.375, 0.5625, 0.675]                            # the family's own coordinate
GGRID = np.round(np.arange(0.05, 1.0001, 0.01), 4)

BLOCKS = [21, 63, 126]                                    # DIAL 1 (tuned)
SCHEMES = ["EQ", "PREC"]                                  # DIAL 2 (tuned)
BOOT_REPS, BOOT_SEED = 400, 20260919
T_BAR = 2.0
HORIZON_DAYS = 24 * 252                                   # new tape available before 2050

C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
C_1562 = dict(CAGR=0.1492, Sharpe=1.1788, MaxDD=-0.1805, oSharpe=1.2250)
MATCH_BAR = 0.0020

RE_SE = re.compile(r"(^|_)(se|sd|stderr|err|sigma)(_|$)", re.I)
RE_T = re.compile(r"(^|_)t(stat)?(_|$)", re.I)
RE_OOS = re.compile(r"(^|_)(oos|out)(_|$)|^o(d|se|t)[_A-Z]|^oos", re.I)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))


# ------------------------------------------------------------------ statistics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def block_index(n, L, reps=BOOT_REPS, seed=BOOT_SEED):
    """ONE circular-block index matrix (reps x n).  The SAME matrix is reused for every series in a
    pooled draw, which is what makes the pooled ruler PAIRED across cells as well as across books."""
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    st = rng.integers(0, n, size=(reps, nb))
    return (st[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def boot_sharpe(x, idx):
    X = np.asarray(x, float)[idx]
    v = X.std(axis=1, ddof=0) * np.sqrt(252)
    return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)


# ------------------------------------------------------------------ the book machinery
def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy_px = px["SPY"]
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values

    def frame_inputs(self):
        above = (self.q > self.q.rolling(200).mean()).values
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < I_V)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        return elig, np.where(np.isfinite(sc), -sc, np.inf)

    def macro_state(self, ma, lag=1):
        s = self.spy_px
        return (s > s.rolling(int(ma)).mean()).shift(int(lag)).fillna(False).values.astype(bool)


def build_frame(pan, elig, key, reb, N=I_N, H=I_H, lag=1):
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_gseq(pan, frame, reb, gseq):
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    g = np.broadcast_to(np.asarray(gseq, float), (T,))
    cur = np.zeros(M)
    rg = np.zeros(T)
    turn = np.zeros(T)
    sc = np.zeros(T)
    gmax = 0.0
    for t in range(T):
        if isreb[t]:
            gt = float(g[t])
            post = gt * frame[t]
        else:
            gt = sc[t - 1] if t else 0.0
            post = cur
        sc[t] = gt
        turn[t] = float(np.abs(post - cur).sum())
        gmax = max(gmax, float(post.sum()))
        r = float(post @ pan.rets[t])
        rg[t] = r
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rg=rg, turn=turn, gmax=gmax, gbar=float(sc[WARMUP:].mean()))


def net_of(run, cost):
    return run["rg"] - run["turn"] * cost / 1e4


# =================================================================== ARM A — the census
def census():
    files = sorted(glob.glob(str(ROOT / "research" / "backtests" / f"{DATE}*.csv")))
    rows = []
    scanned = 0
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if len(df) == 0:
            continue
        scanned += 1
        num = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if len(num) < 3:
            continue
        V = {c: df[c].values.astype(float) for c in num}
        Mk = {c: np.isfinite(V[c]) for c in num}
        secols = [c for c in num if RE_SE.search(c)]
        tcols = [c for c in num if RE_T.search(c)]
        if not secols or not tcols:
            continue
        base = np.ones(len(df), bool)
        for c in num:
            base &= Mk[c]
        keyrows = np.flatnonzero(base)[:12]
        if len(keyrows) < 3:
            keyrows = np.arange(min(12, len(df)))
        lut = {}
        for c in num:
            lut.setdefault(tuple(np.round(np.nan_to_num(V[c][keyrows], nan=1e300), 9)), []).append(c)
        pan = df["panel"].astype(str).values if "panel" in df.columns else np.array(["?"] * len(df))
        seen = set()
        for tc in tcols:
            for sc in secols:
                if sc == tc:
                    continue
                k = tuple(np.round(np.nan_to_num(V[tc][keyrows] * V[sc][keyrows], nan=1e300), 9))
                for dc in lut.get(k, []):
                    if dc in (tc, sc) or (dc, sc, tc) in seen:
                        continue
                    mm = Mk[tc] & Mk[sc] & Mk[dc] & (V[sc] > 0)
                    if mm.sum() < 5:
                        continue
                    ok = np.abs(V[dc][mm] / V[sc][mm] - V[tc][mm]) <= 1e-6 * np.maximum(1.0, np.abs(V[tc][mm]))
                    if ok.mean() <= 0.98:
                        continue
                    if len(np.unique(np.round(V[tc][mm], 8))) < 3:      # G9: no constant/boolean
                        continue
                    seen.add((dc, sc, tc))
                    win = "OOS" if (RE_OOS.search(dc) or RE_OOS.search(tc) or RE_OOS.search(sc)) else "FULL"
                    for i in np.flatnonzero(mm):
                        rows.append(dict(file=Path(f).name, d_col=dc, se_col=sc, t_col=tc,
                                         panel=pan[i], window=win, d=float(V[dc][i]),
                                         se=float(V[sc][i]), t=float(V[tc][i])))
    return pd.DataFrame(rows), scanned, len(files)


# =================================================================== main
def main():
    t0 = time.time()
    say("=" * 126)
    say("IDEA 1570 — how LONG a TAPE would RESOLVE the record's TYPICAL DEVICE MARGIN, and does "
        "POOLING a family's cells resolve it?   (lane cloud, idea 1 of 2)")
    say("  PRE-REGISTERED  H_WALL: median required multiple > 4 AND pooled |t| <= 2 at ALL 6 "
        "(L, scheme) combinations -> KILL for capital, the family is unadjudicable.")
    say("  PRE-REGISTERED  H_POOL: pooled |t| > 2 at >= 4 of 6 AND the rule-8 pick beats its own "
        "twin OOS -> the pooled ruler adjudicates, capital arm is a KEEP-candidate.")
    say("=" * 126)

    # ---------------- panels ----------------
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"\n  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "ARM A is a statement about the record's own published |t| values and is bias-free by "
        "construction; ARM B is a CONTRAST between two books over the SAME names on the SAME days; "
        "the 4a / 4b pass counts in ARM C are NOT immune and are reported as upper bounds.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G3 exactly two tuned parameters (block length, pooling scheme); the MA / g_low / cost "
         "ladders are the family's inherited coordinates, published in full, never selected on",
         2, "== 2", True)

    # window lengths used to convert a required MULTIPLE into required TAPE
    nwin = {}
    for p in panels:
        i_oos = int(np.searchsorted(p.idx.values, np.datetime64(OOS_START)))
        nwin[(p.name, "FULL")] = len(p.idx) - WARMUP
        nwin[(p.name, "OOS")] = len(p.idx) - i_oos
    nwin[("?", "FULL")] = int(np.median([nwin[(p.name, "FULL")] for p in panels]))
    nwin[("?", "OOS")] = int(np.median([nwin[(p.name, "OOS")] for p in panels]))
    say("\n  WINDOW LENGTHS used to convert a required MULTIPLE into required TAPE (trading days):")
    for k in sorted(nwin):
        say(f"    {k[0]:>6} {k[1]:<5} {nwin[k]}")

    # ================================================================ ARM A
    say("\n" + "=" * 126)
    say("ARM A — THE CENSUS.  How long a tape would the record's OWN 2026-09-19 contrasts need?")
    say("=" * 126)
    cen, scanned, nfiles = census()
    if len(cen) == 0:
        say("  no admissible (d, se, t) triples found — ARM A is empty.")
    else:
        def nlookup(r):
            key = (r["panel"] if (r["panel"], r["window"]) in nwin else "?", r["window"])
            return nwin[key]
        cen["n_window"] = cen.apply(nlookup, axis=1)
        cen["abs_t"] = cen["t"].abs()
        cen["req_mult"] = (T_BAR / cen["abs_t"].replace(0, np.nan)) ** 2
        cen["req_n"] = cen["n_window"] * cen["req_mult"]
        cen["extra_days"] = cen["req_n"] - cen["n_window"]
        cen["extra_years"] = cen["extra_days"] / 252.0
        cen["resolved_now"] = cen["abs_t"] > T_BAR
        cen["reach_2050"] = cen["extra_days"] <= HORIZON_DAYS
        ntrip = cen.groupby(["file", "d_col", "se_col", "t_col"]).ngroups
        say(f"  CORPUS: {nfiles} committed {DATE} CSVs, {scanned} non-empty, "
            f"{ntrip} internally validated (d, se, t) triples, {len(cen)} contrast ROWS.")
        gate("G9 census matcher admits no constant/boolean column (>= 3 distinct t per triple)",
             f"{ntrip} triples admitted", "all with >= 3 distinct t", True)
        q = cen["abs_t"].quantile([0.25, 0.5, 0.75, 0.9, 0.95]).to_dict()
        say(f"  |t| DISTRIBUTION: min {cen['abs_t'].min():.3f}  q25 {q[0.25]:.3f}  MEDIAN "
            f"{q[0.5]:.3f}  q75 {q[0.75]:.3f}  q90 {q[0.9]:.3f}  q95 {q[0.95]:.3f}  max "
            f"{cen['abs_t'].max():.3f}")
        say(f"  ALREADY RESOLVED (|t| > 2) TODAY: {int(cen['resolved_now'].sum())} of {len(cen)} "
            f"= {cen['resolved_now'].mean():.4f}")
        un = cen[~cen["resolved_now"]]
        qm = un["req_mult"].quantile([0.25, 0.5, 0.75, 0.9]).to_dict()
        say(f"  REQUIRED MULTIPLE of its own window, UNRESOLVED rows only (n = {len(un)}): "
            f"q25 {qm[0.25]:.2f}x  MEDIAN {qm[0.5]:.2f}x  q75 {qm[0.75]:.2f}x  q90 {qm[0.9]:.2f}x")
        qy = un["extra_years"].quantile([0.25, 0.5, 0.75, 0.9]).to_dict()
        say(f"  EXTRA TAPE REQUIRED (years), UNRESOLVED rows only: q25 {qy[0.25]:.1f}y  MEDIAN "
            f"{qy[0.5]:.1f}y  q75 {qy[0.75]:.1f}y  q90 {qy[0.9]:.1f}y")
        say(f"  REACHABLE BEFORE 2050 (<= 24 more years of tape):  ALL rows "
            f"{cen['reach_2050'].mean():.4f} ({int(cen['reach_2050'].sum())} of {len(cen)})  |  "
            f"UNRESOLVED rows {un['reach_2050'].mean():.4f} ({int(un['reach_2050'].sum())} of "
            f"{len(un)})")
        say("  BY WINDOW:")
        for w, g in cen.groupby("window"):
            gu = g[~g["resolved_now"]]
            say(f"    {w:<5} rows {len(g):>6}  resolved {g['resolved_now'].mean():.4f}  "
                f"median |t| {g['abs_t'].median():.3f}  median extra "
                f"{(gu['extra_years'].median() if len(gu) else np.nan):.1f}y  reach2050 "
                f"{g['reach_2050'].mean():.4f}")
        say("  BY PANEL (top 6 by row count):")
        for p, g in sorted(cen.groupby("panel"), key=lambda x: -len(x[1]))[:6]:
            gu = g[~g["resolved_now"]]
            say(f"    {str(p):<8} rows {len(g):>6}  resolved {g['resolved_now'].mean():.4f}  "
                f"median |t| {g['abs_t'].median():.3f}  median extra "
                f"{(gu['extra_years'].median() if len(gu) else np.nan):.1f}y")
        cen.to_csv(f"{OUT}.census.csv", index=False)
        say(f"  -> {Path(OUT).name}.census.csv")

    # ================================================================ ARM B + C
    say("\n" + "=" * 126)
    say("ARM B / C — THE DEVICE FAMILY (idea 1562's two-state gross), its CAGR-MATCHED DE-GROSS "
        "TWINS, the POOLED RULER, and the rule-8 capital arm.")
    say("=" * 126)

    grid, pooled_rows, wf_rows = [], [], []
    cell_series = {}          # (panel, ma, gl) -> (cand net, twin net) at headline cost, full window
    g1_ok = g2_ok = None
    worst_match = 0.0
    gmax_global = 0.0
    g7_dev = 0.0
    bench = {}

    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=HEADLINE_COST,
                      freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        bench[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO, i_oos=i_oos, i_is=i_is)

        say(f"\n  [{pan.name}]  SPY {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/{spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps {live['CAGR']:.2%}/{live['Sharpe']:.4f}/"
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        elig, key = pan.frame_inputs()
        reb = cadence_rows(pan.idx, I_C)
        frame = build_frame(pan, elig, key, reb)

        A = run_gseq(pan, frame, reb, I_G)
        gmax_global = max(gmax_global, A["gmax"])
        g7_dev = max(g7_dev, float(np.abs(net_of(A, 0.0) - A["rg"]).max()))
        anch = net_of(A, HEADLINE_COST)
        am, ao = triple(anch[WARMUP:]), triple(anch[i_oos:])
        ah1, ah2 = halves(anch[WARMUP:])
        a4a, a4b, _, _, _, _ = keep_paths(anch[WARMUP:], spy, live)
        a4aO, a4bO, _, _, _, _ = keep_paths(anch[i_oos:], spyO, liveO)
        say(f"           FROZEN ANCHOR g=0.75  {am['CAGR']:.2%}/{am['Sharpe']:.4f}/"
            f"{am['MaxDD']:.2%}  H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | 4a {a4a}/{a4aO} 4b {a4b}/{a4bO} | mean gross "
            f"{A['gbar']:.4f}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor "
                         "(15.80%/1.1537/-19.13% full; 1.1857 OOS)", f"max |dev| {d:.2e}",
                         "< 5e-3", d < 5e-3)

        # the constant de-gross ladder = the comparand family
        lad = {}
        for g in GGRID:
            lad[float(g)] = run_gseq(pan, frame, reb, float(g))
        gs = np.array(sorted(lad))
        curve = {c: np.array([cagr(net_of(lad[float(g)], c)[WARMUP:]) for g in gs]) for c in COSTS}

        def matched_twin(target, cost):
            y = curve[cost]
            o = np.argsort(y)
            gstar = float(min(max(float(np.interp(target, y[o], gs[o])), 0.0), 1.0))
            R = run_gseq(pan, frame, reb, gstar)
            rn = net_of(R, cost)
            return gstar, R, rn, abs(cagr(rn[WARMUP:]) - target)

        for ma in MAS:
            for gl in GLOWS:
                st = pan.macro_state(ma, 1)
                C = run_gseq(pan, frame, reb, np.where(st, I_G, gl))
                gmax_global = max(gmax_global, C["gmax"])
                for c in COSTS:
                    rn = net_of(C, c)
                    k4a, k4b, m, h1, h2, lg = keep_paths(rn[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, lgO = keep_paths(rn[i_oos:], spyO, liveO)
                    gstar, TW, tw, gap = matched_twin(m["CAGR"], c)
                    worst_match = max(worst_match, gap)
                    tm, tmo = triple(tw[WARMUP:]), triple(tw[i_oos:])
                    grid.append(dict(
                        panel=pan.name, ma=ma, g_low=gl, cost=c,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                        keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                        legH1=lg["H1"], legH2=lg["H2"], legDD=lg["DD"], legCAGR=lg["CAGR"],
                        olegH1=lgO["H1"], olegH2=lgO["H2"], olegDD=lgO["DD"], olegCAGR=lgO["CAGR"],
                        mean_gross=C["gbar"], twin_g=gstar, twin_match_bp=gap * 1e4,
                        twin_Sharpe=tm["Sharpe"], twin_MaxDD=tm["MaxDD"], twin_CAGR=tm["CAGR"],
                        twin_oSharpe=tmo["Sharpe"], twin_oMaxDD=tmo["MaxDD"],
                        d_sharpe_vs_twin=m["Sharpe"] - tm["Sharpe"],
                        d_maxdd_pp_vs_twin=(m["MaxDD"] - tm["MaxDD"]) * 100,
                        od_sharpe_vs_twin=mo["Sharpe"] - tmo["Sharpe"],
                        is_Sharpe=sharpe(rn[WARMUP:i_is]),
                        spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"], spy_CAGR=spy["CAGR"],
                        live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                        anchor_Sharpe=am["Sharpe"], anchor_MaxDD=am["MaxDD"],
                        anchor_oSharpe=ao["Sharpe"]))
                    if c == HEADLINE_COST:
                        cell_series[(pan.name, ma, gl)] = (rn.copy(), tw.copy())
                        if pan.name == "U56" and ma == 200 and gl == 0.5625:
                            d2 = max(abs(m["Sharpe"] - C_1562["Sharpe"]),
                                     abs(mo["Sharpe"] - C_1562["oSharpe"]),
                                     abs(m["CAGR"] - C_1562["CAGR"]),
                                     abs(m["MaxDD"] - C_1562["MaxDD"]))
                            g2_ok = gate("G2 cross-script replay of idea 1562's headline cell "
                                         "(U56, MA 200, g_low 0.5625, 10 bps: "
                                         "14.92%/1.1788/-18.05%, OOS 1.2250)",
                                         f"max |dev| {d2:.2e}", "< 5e-3", d2 < 5e-3)

    gate("G4 CAGR match quality on every matched twin", f"worst |gap| {worst_match*1e4:.2f} bp",
         f"< {MATCH_BAR*1e4:.0f} bp", worst_match < MATCH_BAR)
    gate("G6 gross in [0, 1] on every book", f"max realised weight sum {gmax_global:.4f}",
         "<= 1.0", gmax_global <= 1.0 + 1e-9)
    gate("G7 the cost ladder is an identity on the same turnover path (0 bps == gross path)",
         f"max |dev| {g7_dev:.2e}", "== 0", g7_dev == 0.0)
    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G8 every cell published", f"{len(G)} rows = 3 panels x {len(MAS)} MA x {len(GLOWS)} "
         f"g_low x {len(COSTS)} cost", f"== {3*len(MAS)*len(GLOWS)*len(COSTS)}",
         len(G) == 3 * len(MAS) * len(GLOWS) * len(COSTS))

    say(f"\n  FULL CELL GRID at the headline 10 bps rung (every cell; 4b legs H1/H2/DD/CAGR):")
    say(f"    {'panel':<6}{'MA':>5}{'gLow':>8}{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}"
        f"{'oCAGR':>9}{'oSharpe':>9}{'oMaxDD':>9}{'4a':>5}{'4b':>5}{'4aO':>5}{'4bO':>5}"
        f"{'twin g':>8}{'dS':>9}{'dDD pp':>9}{'odS':>9}")
    for _, r in G[G.cost == HEADLINE_COST].iterrows():
        say(f"    {r.panel:<6}{r.ma:>5.0f}{r.g_low:>8.4f}{r.CAGR:>9.2%}{r.Sharpe:>9.4f}"
            f"{r.MaxDD:>9.2%}{r.oCAGR:>9.2%}{r.oSharpe:>9.4f}{r.oMaxDD:>9.2%}"
            f"{str(r.keep4a):>5}{str(r.keep4b):>5}{str(r.keep4a_oos):>5}{str(r.keep4b_oos):>5}"
            f"{r.twin_g:>8.4f}{r.d_sharpe_vs_twin:>+9.4f}{r.d_maxdd_pp_vs_twin:>+9.2f}"
            f"{r.od_sharpe_vs_twin:>+9.4f}")

    # -------------------------------------------------- the POOLED RULER
    say("\n  THE POOLED RULER.  24 LARGE-CAP CELLS (U56 + B136, 12 each) at 10 bps, each against "
        "its own CAGR-matched constant de-gross twin.  One circular-block index set per replicate "
        "is applied to ALL 24 cells and their twins at once, so the cells' shared tape is carried.")
    big = [(p, ma, gl) for p in ("U56", "B136") for ma in MAS for gl in GLOWS]
    say(f"    cells pooled: {len(big)}")
    for L in BLOCKS:
        # per-cell readings (the ruler the record has been using)
        per = []
        for kc in big:
            a, b = cell_series[kc]
            a, b = a[WARMUP:], b[WARMUP:]
            idx = block_index(len(a), L)
            d = boot_sharpe(a, idx) - boot_sharpe(b, idx)
            obs = sharpe(a) - sharpe(b)
            se = float(np.nanstd(d, ddof=1))
            per.append(dict(panel=kc[0], ma=kc[1], g_low=kc[2], L=L, obs=obs, se=se,
                            t=(obs / se if se > 0 else np.nan), draws=d))
        P = pd.DataFrame([{k: v for k, v in p.items() if k != "draws"} for p in per])
        nres = int((P["t"].abs() > T_BAR).sum())
        say(f"\n    [L = {L:>3}]  PER-CELL: {nres} of {len(P)} reach |t| > {T_BAR:.0f}.  "
            f"max |t| {P['t'].abs().max():.4f}  median |t| {P['t'].abs().median():.4f}  "
            f"mean margin {P['obs'].mean():+.4f}  mean SE {P['se'].mean():.4f}")
        D = np.vstack([p["draws"] for p in per])            # (cells x reps), COMMON index set
        obsv = P["obs"].values
        for sch in SCHEMES:
            if sch == "EQ":
                w = np.ones(len(obsv)) / len(obsv)
            else:                                            # PREC: inverse bootstrap variance
                v = P["se"].values ** 2
                w = (1.0 / np.where(v > 0, v, np.nan))
                w = w / np.nansum(w)
            pooled_obs = float(np.nansum(w * obsv))
            pooled_draws = np.nansum(w[:, None] * D, axis=0)
            pse = float(np.nanstd(pooled_draws, ddof=1))
            pt = pooled_obs / pse if pse > 0 else np.nan
            # what a NAIVE independence assumption would have claimed
            naive_se = float(np.sqrt(np.nansum((w ** 2) * (P["se"].values ** 2))))
            naive_t = pooled_obs / naive_se if naive_se > 0 else np.nan
            req_mult = (T_BAR / abs(pt)) ** 2 if np.isfinite(pt) and pt != 0 else np.inf
            n_big = len(cell_series[("U56", 200, 0.5625)][0]) - WARMUP
            pooled_rows.append(dict(L=L, scheme=sch, cells=len(obsv), pooled_d=pooled_obs,
                                    pooled_se=pse, pooled_t=pt, naive_se=naive_se,
                                    naive_t=naive_t, se_inflation=pse / naive_se,
                                    best_cell_t=float(P["t"].abs().max()),
                                    med_cell_se=float(P["se"].median()),
                                    resolves=bool(abs(pt) > T_BAR), req_mult=req_mult,
                                    req_extra_years=(req_mult - 1) * n_big / 252.0))
            say(f"      POOL {sch:<4}  margin {pooled_obs:+.4f}  pooled SE {pse:.4f}  |t| "
                f"{abs(pt):.4f}  {'RESOLVES' if abs(pt) > T_BAR else 'does NOT resolve'}   "
                f"(independence-assuming SE {naive_se:.4f} -> |t| {abs(naive_t):.4f}; the paired "
                f"pooled SE is {pse/naive_se:.2f}x that)   required extra tape "
                f"{(req_mult-1)*n_big/252.0:.1f}y")
        for p in per:
            p.pop("draws")
        pd.DataFrame(per).to_csv(f"{OUT}.percell_L{L}.csv", index=False)
    PL = pd.DataFrame(pooled_rows)
    PL.to_csv(f"{OUT}.pooled.csv", index=False)

    # -------------------------------------------------- ARM C: rule 8
    say("\n  ARM C — RULE 8.  Cell chosen by argmax IS Sharpe on warm-up..2016-12-31 ONLY; "
        "2017-01-01..end read exactly ONCE.")
    chooser_max_row = {}
    for pan in panels:
        b = bench[pan.name]
        sub = G[(G.panel == pan.name) & (G.cost == HEADLINE_COST)]
        pick = sub.loc[sub["is_Sharpe"].idxmax()]
        chooser_max_row[pan.name] = IS_END
        a, tw = cell_series[(pan.name, int(pick.ma), float(pick.g_low))]
        io = b["i_oos"]
        k4a, k4b, m, h1, h2, lg = keep_paths(a[WARMUP:], b["spy"], b["live"])
        k4aO, k4bO, mo, oh1, oh2, lgO = keep_paths(a[io:], b["spyO"], b["liveO"])
        idx = block_index(len(a) - io, 63)
        od = sharpe(a[io:]) - sharpe(tw[io:])
        ose = float(np.nanstd(boot_sharpe(a[io:], idx) - boot_sharpe(tw[io:], idx), ddof=1))
        say(f"\n    [{pan.name}] PICK  MA {int(pick.ma)}  g_low {pick.g_low:.4f}  (IS Sharpe "
            f"{pick.is_Sharpe:.4f}, chosen on rows <= {IS_END})")
        say(f"      FULL  {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   H1/H2 "
            f"{h1:.4f}/{h2:.4f}   4a {k4a}  4b {k4b}  legs H1 {lg['H1']} H2 {lg['H2']} DD "
            f"{lg['DD']} CAGR {lg['CAGR']}")
        say(f"      OOS   {mo['CAGR']:.2%} / {mo['Sharpe']:.4f} / {mo['MaxDD']:.2%}   4a {k4aO}  "
            f"4b {k4bO}  legs H1 {lgO['H1']} H2 {lgO['H2']} DD {lgO['DD']} CAGR {lgO['CAGR']}")
        say(f"      vs LIVE RULES v2 OOS {b['liveO']['CAGR']:.2%}/{b['liveO']['Sharpe']:.4f}/"
            f"{b['liveO']['MaxDD']:.2%}   vs SPY OOS {b['spyO']['CAGR']:.2%}/"
            f"{b['spyO']['Sharpe']:.4f}/{b['spyO']['MaxDD']:.2%}")
        say(f"      vs its OWN CAGR-MATCHED TWIN, OOS: dSharpe {od:+.4f}  SE {ose:.4f}  |t| "
            f"{abs(od/ose) if ose>0 else float('nan'):.4f}  -> "
            f"{'beats' if od > 0 else 'LOSES TO'} the twin, "
            f"{'resolved' if ose>0 and abs(od/ose)>T_BAR else 'UNRESOLVED'}")
        wf_rows.append(dict(panel=pan.name, ma=int(pick.ma), g_low=float(pick.g_low),
                            is_Sharpe=float(pick.is_Sharpe), CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                            MaxDD=m["MaxDD"], H1=h1, H2=h2, keep4a=k4a, keep4b=k4b,
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            keep4a_oos=k4aO, keep4b_oos=k4bO,
                            live_oCAGR=b["liveO"]["CAGR"], live_oSharpe=b["liveO"]["Sharpe"],
                            live_oMaxDD=b["liveO"]["MaxDD"], spy_oCAGR=b["spyO"]["CAGR"],
                            spy_oSharpe=b["spyO"]["Sharpe"], spy_oMaxDD=b["spyO"]["MaxDD"],
                            od_vs_twin=od, ose_vs_twin=ose,
                            ot_vs_twin=(od / ose if ose > 0 else np.nan)))
    W = pd.DataFrame(wf_rows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G5 no chooser reads a row on or after 2017-01-01",
         f"chooser windows end {sorted(set(chooser_max_row.values()))}", f"<= {IS_END}", True)

    # -------------------------------------------------- verdict
    say("\n" + "=" * 126)
    med_mult = float(cen[~cen["resolved_now"]]["req_mult"].median()) if len(cen) else np.nan
    nres_pool = int(PL["resolves"].sum())
    wall = (med_mult > 4.0) and (nres_pool == 0)
    poolwin = (nres_pool >= 4) and bool((W["od_vs_twin"] > 0).all())
    verdict = "KILL" if wall else ("KEEP-candidate" if poolwin else "PARK")
    say(f"ARM A: median required multiple on unresolved contrasts = {med_mult:.2f}x its own window; "
        f"{cen['reach_2050'].mean():.1%} of the record's own {len(cen)} contrast rows are "
        f"resolvable with tape available before 2050.")
    say(f"ARM B: the pooled ruler resolves {nres_pool} of {len(PL)} (L, scheme) combinations.")
    say(f"ARM C: rule-8 picks beat their own CAGR-matched twin OOS on "
        f"{int((W['od_vs_twin'] > 0).sum())} of {len(W)} panels; 4b OOS passes "
        f"{int(W['keep4b_oos'].sum())} of {len(W)}; 4a OOS passes {int(W['keep4a_oos'].sum())}.")
    say(f"PRE-REGISTERED VERDICT: H_WALL {wall}, H_POOL {poolwin}  ->  {verdict}")
    say("=" * 126)

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    nfail = int((~gdf["pass_"]).sum())
    say(f"\nGATES: {len(gdf)} recorded, {nfail} FAIL.")
    say(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return verdict, G, PL, W, cen


if __name__ == "__main__":
    main()
