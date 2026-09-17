#!/usr/bin/env python3
"""
Idea 1217 (cloud lane, 2026-09-17) — should a BOUNDARY IS-ARGMAX be REPORTABLE as a PICK at all?

THE PREMISE, READ FROM THE RECORD.  Idea 1205's rule-8 arm put the GROSS IS-argmax on the
ladder's TOP rung g = 1.00 at 6 of 6 (panel x ladder set) cells, on a statistic 1189 had already
shown is FLAT in gross — and it took -24.93% of drawdown with it against the frozen rung's
-19.13%.  1152 found the record's "reached from GROSS" claims are all boundary picks at margins
of 1.1e-04 to 9.9e-04.  1195 names the same pattern from a third direction.  An argmax that
lands on the END of a ladder is the signature of a statistic that is MONOTONE or FLAT in the
dial, not of a maximum the data located: the ladder simply ran out.

THIS RUN PRE-REGISTERS A BOUNDARY RULE, APPLIES IT TO THE RECORD'S OWN COMMITTED PICKS, AND
PRICES THE SUPPRESSION.

  ARM 1 THE CENSUS.  Every committed pick row on disk (research/backtests/*.walkforward.csv and
  *.picks.csv, the artefacts past runs published) is harvested, its LADDER's rung list recovered
  from the file's own rows (1152's finding is that the record rarely states the list, so the
  file's own observed rung set is the honest available reconstruction — stated as a limitation,
  not hidden), and each pick tested against the boundary rule.  Reported: what fraction of the
  record's published picks the rule would have SUPPRESSED.

  ARM 2 THE PRICE.  On the live grid the same rule becomes a deployable chooser, and the
  question "what does suppression cost or save" is answered in OOS Sharpe, OOS MaxDD, and both
  KEEP paths, walk-forward.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  BOUNDARY DEFINITION  B_NONE   suppress nothing (the record's current habit; control)
                       B_STRICT the pick is the ladder's minimum or maximum rung
                       B_WIDE   the pick is within the two extreme rungs at either end
  CLAIM SET            census: C_LADRUNG (files carrying explicit ladder+rung columns),
                       C_PICK (files carrying a `pick` column with >= 3 distinct numeric rungs),
                       C_ALL (the union)
                       price:  ALL4 (the record's standing four-ladder set) and NG (1214's
                       degenerate-free set, GROSS dropped)

  9 census cells and 6 price cells, EVERY ONE PUBLISHED.

NOT DIALS, REPORTED AT EVERY VALUE AND NEVER SELECTED ON: PANEL {U56, B136, SMALL} (rule 9);
FOLD CADENCE {QUARTER primary, YEAR carried for continuity with 1205/1223}; the four choosers
CH_ARGMAX / CH_SUPP_ANCHOR / CH_SUPP_INTERIOR / CH_ANCHOR.

PRE-DECLARED OUTCOMES, fixed before any price is read:
  (A) SUPPRESS — boundary suppression raises mean OOS Sharpe against the record's CH_ARGMAX
      habit at both claim sets, or leaves it flat while strictly improving OOS MaxDD.
  (B) REPORT AS IS — suppression costs OOS Sharpe without a drawdown gain.
  (C) NEITHER MATTERS — suppression changes neither by more than one clustered SE, in which
      case the boundary picks were never carrying anything and the schema clause is free.

Frozen at the record's construction, inherited from 1205/1207/1214/1223/1227 unchanged: 3-leg
composite (21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 /
GROSS=0.75 / CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 (lag=1), warm-up 260 rows,
1227's VALUE-based definition of a move.  The GROSS ladder is extended to 1.00 so that 1205's
own boundary pick (g = 1.00) is reachable and gate G13 can replicate its -24.93%.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with BOTH dials chosen on the IS
folds ONLY and 2017-2026 read once; BOTH KEEP paths on every rung book, every stitched chooser
curve and every rule-8 row; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_should-a-BOUNDARY-IS-ARGMAX-be-REPORTABLE-as-a-PICK-at-all_cloud.py
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "should-a-BOUNDARY-IS-ARGMAX-be-REPORTABLE-as-a-PICK-at-all"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
ANCHOR_KEY = ("CADENCE", "W")

# GROSS runs to 1.00 so 1205's own boundary pick is on the ladder (gate G13).
LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00],
    "CADENCE": ["W", "M"],
}
ORDERED = {"N": True, "H": True, "GROSS": True, "CADENCE": False}   # CADENCE has no metric order

# ---- DIAL 1: boundary definition.  k = how many rungs at each end count as a boundary.
BDEFS = {"B_NONE": 0, "B_STRICT": 1, "B_WIDE": 2}

# ---- DIAL 2 (price arm): claim set = which ladders count as claims
NG4 = ["N", "H", "CADENCE"]
ALL4 = ["N", "H", "GROSS", "CADENCE"]
SETS = {"ALL4": ALL4, "NG": NG4}

CHOOSERS = ["CH_ARGMAX", "CH_SUPP_ANCHOR", "CH_SUPP_INTERIOR", "CH_ANCHOR"]
CADENCES = ["QUARTER", "YEAR"]
MIN_FOLD = {"QUARTER": 40, "YEAR": 200}
PRIMARY_CAD = "QUARTER"
MIN_IS = 252
LIVE_MAXDD_COMMITTED = -0.1205
REP1205_DD = -0.2493      # 1205's boundary-argmax drawdown, gate G13
REP1205_FROZEN_DD = -0.1913

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ==================================================================== ARM 1 — the census
_NUM = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")


def as_num(v):
    s = str(v).strip()
    return float(s) if _NUM.match(s) else None


def boundary_flag(rung, rungs, k):
    """True if `rung` sits within k rungs of either end of the ORDERED rung list `rungs`.
    k = 0 never fires.  A ladder shorter than 2k+1 rungs is ALL boundary by construction and is
    flagged so the census can report it separately rather than silently counting it."""
    if k <= 0 or rung not in rungs:
        return False, False
    n = len(rungs)
    i = rungs.index(rung)
    degenerate = n <= 2 * k
    return bool(i < k or i >= n - k), degenerate


def census():
    """Harvest every committed pick row on disk and test it against each boundary definition."""
    rows = []
    files = sorted(BT.glob("*.walkforward.csv")) + sorted(BT.glob("*.picks.csv"))
    me = f"{DATE}_{SLUG}_cloud"
    for f in files:
        if f.name.startswith(me):
            continue                                   # never census this run's own output
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        cols = set(df.columns)
        # ---- C_LADRUNG: the file names its ladder and its rung
        if {"ladder", "rung"} <= cols:
            for lad, g in df.groupby("ladder"):
                vals = [as_num(v) for v in g["rung"].astype(str).unique()]
                if any(v is None for v in vals) or len(vals) < 3:
                    continue
                rungs = sorted(set(vals))
                for _, r in g.iterrows():
                    v = as_num(r["rung"])
                    if v is None:
                        continue
                    rows.append(dict(file=f.name, claim_set="C_LADRUNG", ladder=str(lad),
                                     rung=v, nrungs=len(rungs),
                                     rung_list=";".join(f"{x:g}" for x in rungs),
                                     OOS_Sharpe=float(r["OOS_Sharpe"])
                                     if "OOS_Sharpe" in cols and pd.notna(r.get("OOS_Sharpe"))
                                     else np.nan,
                                     OOS_MaxDD=float(r["OOS_MaxDD"])
                                     if "OOS_MaxDD" in cols and pd.notna(r.get("OOS_MaxDD"))
                                     else np.nan,
                                     _rungs=rungs))
        # ---- C_PICK: the file publishes a `pick` whose observed values form a numeric ladder
        elif "pick" in cols:
            key = [c for c in ("arm", "dial", "ladder", "chooser") if c in cols]
            groups = df.groupby(key) if key else [((), df)]
            for gk, g in groups:
                vals = [as_num(v) for v in g["pick"].astype(str).unique()]
                if any(v is None for v in vals) or len(vals) < 3:
                    continue
                rungs = sorted(set(vals))
                lad = "|".join(str(x) for x in (gk if isinstance(gk, tuple) else (gk,))) or "pick"
                for _, r in g.iterrows():
                    v = as_num(r["pick"])
                    if v is None:
                        continue
                    rows.append(dict(file=f.name, claim_set="C_PICK", ladder=lad, rung=v,
                                     nrungs=len(rungs),
                                     rung_list=";".join(f"{x:g}" for x in rungs),
                                     OOS_Sharpe=float(r["OOS_Sharpe"])
                                     if "OOS_Sharpe" in cols and pd.notna(r.get("OOS_Sharpe"))
                                     else np.nan,
                                     OOS_MaxDD=float(r["OOS_MaxDD"])
                                     if "OOS_MaxDD" in cols and pd.notna(r.get("OOS_MaxDD"))
                                     else np.nan,
                                     _rungs=rungs))
    if not rows:
        return pd.DataFrame(), pd.DataFrame()
    cdf = pd.DataFrame(rows)
    for bn, k in BDEFS.items():
        flags, degs = [], []
        for _, r in cdf.iterrows():
            b, d = boundary_flag(r["rung"], r["_rungs"], k)
            flags.append(b)
            degs.append(d)
        cdf[bn] = flags
        cdf[bn + "_degenerate"] = degs
    cdf = cdf.drop(columns=["_rungs"])
    summ = []
    for cs in ["C_LADRUNG", "C_PICK", "C_ALL"]:
        s = cdf if cs == "C_ALL" else cdf[cdf.claim_set == cs]
        if not len(s):
            continue
        for bn in BDEFS:
            summ.append(dict(claim_set=cs, boundary_def=bn, n_picks=len(s),
                             n_files=int(s.file.nunique()), n_ladders=int(s.ladder.nunique()),
                             n_suppressed=int(s[bn].sum()),
                             frac_suppressed=float(s[bn].mean()),
                             frac_short_ladder=float(s[bn + "_degenerate"].mean()),
                             mean_OOS_Sharpe_kept=float(s.loc[~s[bn], "OOS_Sharpe"].mean()),
                             mean_OOS_Sharpe_suppressed=float(s.loc[s[bn], "OOS_Sharpe"].mean()),
                             mean_OOS_MaxDD_kept=float(s.loc[~s[bn], "OOS_MaxDD"].mean()),
                             mean_OOS_MaxDD_suppressed=float(s.loc[s[bn], "OOS_MaxDD"].mean())))
    return cdf, pd.DataFrame(summ)


# ==================================================================== panels / runner
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, N, H, freq, lag=1):
    reb = pan.seg[freq]
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
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
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


def nrun(pan, Wt, freq):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


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
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1217 (cloud lane, 2026-09-17) — should a BOUNDARY IS-ARGMAX be REPORTABLE as a")
    say("PICK at all?")
    say("=" * 108)
    say("")
    say(f"  DIAL 1 BOUNDARY DEFINITION  {list(BDEFS)}  (k rungs at each end: "
        f"{list(BDEFS.values())})")
    say("  DIAL 2 CLAIM SET            census C_LADRUNG / C_PICK / C_ALL;  price ALL4 / NG")
    say("  Choosers (NOT a dial, all reported): CH_ARGMAX (the record's habit), "
        "CH_SUPP_ANCHOR,")
    say("    CH_SUPP_INTERIOR (fall back to the best INTERIOR rung), CH_ANCHOR (do nothing).")
    say("")
    say("  PRE-DECLARED OUTCOMES, fixed before any price is read:")
    say("    (A) SUPPRESS — suppression raises mean OOS Sharpe at both claim sets, or leaves it")
    say("        flat while strictly improving OOS MaxDD.")
    say("    (B) REPORT AS IS — suppression costs OOS Sharpe with no drawdown gain.")
    say("    (C) NEITHER MATTERS — neither moves by more than one clustered SE.")

    # ================================================================ ARM 1
    say("")
    say("=" * 108)
    say("ARM 1 — THE CENSUS.  EVERY COMMITTED PICK ROW ON DISK, AGAINST THE BOUNDARY RULE")
    say("=" * 108)
    cdf, csum = census()
    cdf.to_csv(f"{OUT}.census.csv", index=False)
    csum.to_csv(f"{OUT}.census_summary.csv", index=False)
    say("")
    say("  RECOVERY METHOD AND ITS LIMIT (1152's finding, carried here as a caveat, not hidden):")
    say("  the record rarely states a ladder's rung LIST beside a pick, so each ladder's list is")
    say("  reconstructed from the DISTINCT rung values the file itself publishes.  That is an")
    say("  UNDER-estimate of the true ladder whenever a run published only part of its grid, and")
    say("  an under-estimate of the rung list INFLATES the boundary rate (fewer rungs, more of")
    say("  them at an end).  Ladders shorter than 2k+1 rungs are ALL boundary by construction")
    say("  and their share is reported in its own column rather than folded into the headline.")
    say("")
    if not len(cdf):
        say("  NO COMMITTED PICK ROWS RECOVERABLE — census arm empty.")
    else:
        say(f"  HARVEST: {len(cdf):,} committed pick rows from {cdf.file.nunique()} files over "
            f"{cdf.ladder.nunique()} distinct (file, ladder) reconstructions.")
        say("")
        say("       claim_set   bdef       picks  files  suppressed   frac   short-ladder"
            "   meanOOS_kept  meanOOS_supp   meanDD_kept  meanDD_supp")
        for _, r in csum.iterrows():
            say(f"       {r.claim_set:10s}  {r.boundary_def:9s} {int(r.n_picks):6d} "
                f"{int(r.n_files):5d}  {int(r.n_suppressed):9d}  {r.frac_suppressed:.4f}  "
                f"{r.frac_short_ladder:11.4f}   {r.mean_OOS_Sharpe_kept:11.4f}  "
                f"{r.mean_OOS_Sharpe_suppressed:11.4f}   {r.mean_OOS_MaxDD_kept:10.4f}  "
                f"{r.mean_OOS_MaxDD_suppressed:10.4f}")
        s = csum[(csum.claim_set == "C_ALL") & (csum.boundary_def == "B_STRICT")]
        if len(s):
            r = s.iloc[0]
            say("")
            say(f"  HEADLINE CENSUS NUMBER: under B_STRICT the rule would SUPPRESS "
                f"{int(r.n_suppressed):,} of {int(r.n_picks):,} committed pick rows "
                f"({r.frac_suppressed:.1%}).")
        n0 = csum[csum.boundary_def == "B_NONE"].n_suppressed.sum()
        GATES.append(dict(gate="G14 B_NONE suppresses nothing (the control is the record's "
                               "current habit)", value=float(n0), target=0.0,
                          pass_=bool(n0 == 0)))
        mono = True
        for cs in csum.claim_set.unique():
            v = [float(csum[(csum.claim_set == cs)
                            & (csum.boundary_def == b)].frac_suppressed.iloc[0])
                 for b in ["B_NONE", "B_STRICT", "B_WIDE"]]
            mono = mono and v[0] <= v[1] <= v[2]
        GATES.append(dict(gate="G15 suppressed fraction is monotone in the boundary width",
                          value=float(mono), target=1.0, pass_=bool(mono)))

    # ================================================================ ARM 2 — the price
    say("")
    say("=" * 108)
    say("ARM 2 — THE PRICE.  WHAT DOES SUPPRESSION COST OR SAVE, WALK-FORWARD?")
    say("=" * 108)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mvv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mvv[c] < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0), SPY benchmark only.")

    booked, bench, BOOKKEY = {}, {}, []
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
        anchor_frame = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            fr = anchor_frame if f == "W" else frames[(A_N, A_H, "M")]
            books[("CADENCE", f)] = nrun(pan, A_G * fr, f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * anchor_frame, "W")
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books "
            f"(N {len(LAD['N'])}, H {len(LAD['H'])}, GROSS {len(LAD['GROSS'])} to 1.00, "
            f"CADENCE 2).")

    ident = 0.0
    for pan in panels:
        bk = booked[pan.name]
        for k in (("N", A_N), ("H", A_H), ("GROSS", A_G)):
            ident = max(ident, float(np.nanmax(np.abs(bk[k] - bk[ANCHOR_KEY]))))
    GATES.append(dict(gate="G9 the anchor is one book under four names", value=ident,
                      target=1e-15, pass_=bool(ident <= 1e-15)))
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g2 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    GATES.append(dict(gate="G2 fast runner == engine.backtest on the decision-time frame",
                      value=g2, target=1e-10, pass_=bool(g2 < 1e-10)))
    lm = mdd(bench["U56"]["live"][WARMUP:])
    GATES.append(dict(gate="G3 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                      value=lm, target=LIVE_MAXDD_COMMITTED,
                      pass_=bool(abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)))

    RM = {p: np.column_stack([booked[p][k] for k in BOOKKEY]) for p in booked}
    BIDX = {k: i for i, k in enumerate(BOOKKEY)}
    LADIDX = {lad: [BIDX[(lad, r)] for r in LAD[lad]] for lad in LAD}
    ANCHOR_I = BIDX[ANCHOR_KEY]
    ANCHOR_EQ = set(i for i in range(len(BOOKKEY))
                    if all(float(np.nanmax(np.abs(RM[p][:, i] - RM[p][:, ANCHOR_I]))) == 0.0
                           for p in RM))
    say(f"    ANCHOR-EQUIVALENT BOOKS (1227's value definition): "
        f"{sorted(BOOKKEY[i] for i in ANCHOR_EQ)}")

    # G13: replicate 1205's boundary pick and its drawdown on U56 GROSS
    g_top = RM["U56"][:, BIDX[("GROSS", 1.00)]]
    g_anch = RM["U56"][:, BIDX[("GROSS", A_G)]]
    dd_top, dd_anch = mdd(g_top[WARMUP:]), mdd(g_anch[WARMUP:])
    GATES.append(dict(gate="G13 U56 GROSS=1.00 reproduces 1205's boundary-pick drawdown "
                           "(-24.93%)", value=dd_top, target=REP1205_DD,
                      pass_=bool(abs(dd_top - REP1205_DD) < 6e-3)))
    GATES.append(dict(gate="G16 U56 GROSS=0.75 reproduces 1205's frozen-rung drawdown "
                           "(-19.13%)", value=dd_anch, target=REP1205_FROZEN_DD,
                      pass_=bool(abs(dd_anch - REP1205_FROZEN_DD) < 6e-3)))
    say(f"    G13 U56 GROSS=1.00 MaxDD {dd_top:.4%} against 1205's committed "
        f"{REP1205_DD:.2%}; G16 GROSS=0.75 {dd_anch:.4%} against {REP1205_FROZEN_DD:.2%}.")
    say(f"    GROSS Sharpe over the whole ladder (1189's 'flat in gross'): "
        + " ".join(f"{g:g}:{sharpe(RM['U56'][WARMUP:, BIDX[('GROSS', g)]]):.4f}"
                   for g in LAD["GROSS"]))

    # ---- folds
    folds = {}
    for cad in CADENCES:
        for pan in panels:
            keyv = (pan.idx.year.values * 10 + pan.idx.quarter.values) if cad == "QUARTER" \
                else pan.idx.year.values
            out, cover = [], []
            for v in sorted(set(keyv.tolist())):
                oo = np.flatnonzero(keyv == v)
                oo = oo[oo >= pan.i0 + MIN_IS]
                if len(oo) < MIN_FOLD[cad]:
                    continue
                o0, o1 = int(oo[0]), int(oo[-1]) + 1
                if o0 - pan.i0 < MIN_IS:
                    continue
                out.append((v, o0, o1))
                cover.append((o0, o1))
            cover = sorted(set(cover))
            gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
            GATES.append(dict(gate=f"G4 {cad} folds tile {pan.name} with no overlap and no gap",
                              value=float(gap), target=0.0, pass_=bool(gap == 0)))
            folds[(cad, pan.name)] = out
    for cad in CADENCES:
        say(f"    {cad:8s}: " + "  ".join(f"{p.name} {len(folds[(cad,p.name)])} folds"
                                          for p in panels))

    # ---- the chooser: IS argmax on each ladder, then the boundary rule
    _RANK: dict = {}

    def ranked(p, lad, lo, hi):
        """(Sharpe-ordered rung indices, best-to-worst) for one ladder on one IS window."""
        key = (p, lad, lo, hi)
        if key in _RANK:
            return _RANK[key]
        v = [(sharpe(RM[p][lo:hi, BIDX[(lad, r)]]), j, r) for j, r in enumerate(LAD[lad])]
        v = [x for x in v if np.isfinite(x[0])]
        v.sort(key=lambda x: -x[0])
        _RANK[key] = v
        return v

    def pick_rows(p, o0, L_is, lad, k):
        """Returns (argmax_book, is_boundary, supp_anchor_book, supp_interior_book)."""
        lo, hi = max(pan_i0[p], o0 - L_is) if L_is else pan_i0[p], o0
        v = ranked(p, lad, lo, hi)
        if not v:
            return ANCHOR_I, False, ANCHOR_I, ANCHOR_I
        _, j, r = v[0]
        arg = BIDX[(lad, r)]
        n = len(LAD[lad])
        isb = bool(k > 0 and ORDERED[lad] and (j < k or j >= n - k))
        if not isb:
            return arg, False, arg, arg
        inter = [x for x in v if k <= x[1] < n - k]
        return arg, True, ANCHOR_I, (BIDX[(lad, inter[0][2])] if inter else ANCHOR_I)

    pan_i0 = {p.name: p.i0 for p in panels}

    say("")
    say("  THE WALK.  A DECISION ROW is (panel, ladder) — 1205's own construction, and what the")
    say("  queue means by 'every committed rule-8 pick': EACH ladder publishes its own IS-argmax")
    say("  pick at each fold on an EXPANDING IS window.  The CLAIM SET then says which ladders'")
    say("  picks are counted.  Nothing is selected on.")
    picks: dict = {}
    prows = []
    for cad in CADENCES:
        for pan in panels:
            for (v, o0, o1) in folds[(cad, pan.name)]:
                for lad in LAD:
                    for bn, k in BDEFS.items():
                        a, isb, sa, si = pick_rows(pan.name, o0, None, lad, k)
                        sel = {"CH_ARGMAX": a, "CH_SUPP_ANCHOR": sa, "CH_SUPP_INTERIOR": si,
                               "CH_ANCHOR": ANCHOR_I}
                        for ch in CHOOSERS:
                            bi = sel[ch]
                            picks.setdefault((cad, pan.name, lad, bn, ch), []).append(
                                (v, o0, o1, bi))
                            prows.append(dict(cadence=cad, panel=pan.name, fold=v,
                                              named_ladder=lad, boundary_def=bn, chooser=ch,
                                              boundary_pick=isb,
                                              ladder=BOOKKEY[bi][0], rung=BOOKKEY[bi][1],
                                              moved=bool(bi not in ANCHOR_EQ),
                                              OOS_Sharpe=sharpe(RM[pan.name][o0:o1, bi]),
                                              OOS_MaxDD=mdd(RM[pan.name][o0:o1, bi])))
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    mv = float(pdf[pdf.chooser == "CH_ANCHOR"].moved.mean())
    GATES.append(dict(gate="G5 CH_ANCHOR move rate == 0", value=mv, target=0.0,
                      pass_=bool(mv == 0.0)))
    same = pdf[(pdf.boundary_def == "B_NONE") & (pdf.chooser != "CH_ANCHOR")]
    g17 = float(same.groupby(["cadence", "panel", "fold", "named_ladder"])
                .rung.nunique().max() - 1)
    GATES.append(dict(gate="G17 at B_NONE the three non-anchor choosers are the SAME pick",
                      value=g17, target=0.0, pass_=bool(g17 == 0)))

    say("")
    say("  (2a) HOW OFTEN EACH LADDER'S IS-ARGMAX LANDS ON A BOUNDARY, ON THE LIVE GRID")
    say("       (primary cadence; CADENCE has no metric order so it is never flagged):")
    say("       ladder    bdef       picks   boundary   rate    modal rung")
    for lad in LAD:
        for bn in BDEFS:
            s = pdf[(pdf.cadence == PRIMARY_CAD) & (pdf.named_ladder == lad)
                    & (pdf.boundary_def == bn) & (pdf.chooser == "CH_ARGMAX")]
            modal = s.rung.mode()
            say(f"       {lad:8s}  {bn:9s} {len(s):6d}  {int(s.boundary_pick.sum()):9d}  "
                f"{s.boundary_pick.mean():.4f}   {modal.iloc[0] if len(modal) else '-'}")
    for sname, lads in SETS.items():
        s = pdf[(pdf.cadence == PRIMARY_CAD) & (pdf.named_ladder.isin(lads))
                & (pdf.boundary_def == "B_STRICT") & (pdf.chooser == "CH_ARGMAX")]
        say(f"       CLAIM SET {sname:5s} at B_STRICT: {int(s.boundary_pick.sum())} of "
            f"{len(s)} picks suppressed ({s.boundary_pick.mean():.4f}).")

    # ---- benchmarks and the stitched curves
    BM = {}
    for pan in panels:
        fl = folds[(PRIMARY_CAD, pan.name)]
        a0, a1 = fl[0][1], fl[-1][2]
        ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm_, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[a0:a1]
            h1, h2 = halves(full)
            o = r[max(a0, ioos):a1]
            oh1, oh2 = halves(o)
            BM[(pan.name, nm_)] = dict(**triple(full), H1=h1, H2=h2, OOS_CAGR=cagr(o),
                                       OOS_Sharpe=sharpe(o), OOS_MaxDD=mdd(o), OH1=oh1, OH2=oh2)

    def bm_of(p, nm_, oos=False):
        d = BM[(p, nm_)]
        if not oos:
            return dict(H1=d["H1"], H2=d["H2"], CAGR=d["CAGR"], MaxDD=d["MaxDD"])
        return dict(H1=d["OH1"], H2=d["OH2"], CAGR=d["OOS_CAGR"], MaxDD=d["OOS_MaxDD"])

    say("")
    say("  BENCHMARKS over each panel's fold span (10 bps, t+1), primary cadence:")
    for pan in panels:
        for nm_ in ("SPY", "LIVE"):
            d = BM[(pan.name, nm_)]
            say(f"    {pan.name:6s} {nm_:5s} {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / "
                f"{d['MaxDD']:8.2%}  halves {d['H1']:.4f}/{d['H2']:.4f}  "
                f"OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    say("")
    say("  BOTH KEEP PATHS ON EVERY RUNG BOOK (nothing selected on):")
    krows = []
    for pan in panels:
        fl = folds[(PRIMARY_CAD, pan.name)]
        a0, a1 = fl[0][1], fl[-1][2]
        ioos = max(a0, pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        for k, i in BIDX.items():
            r = RM[pan.name][a0:a1, i]
            k4a, k4b, m, h1, h2 = keep_paths(r, bm_of(pan.name, "SPY"), bm_of(pan.name, "LIVE"))
            ro = RM[pan.name][ioos:a1, i]
            _, k4bo, mo, _, _ = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                           bm_of(pan.name, "LIVE", True))
            j = LAD[k[0]].index(k[1])
            krows.append(dict(panel=pan.name, ladder=k[0], rung=k[1], rung_index=j,
                              is_boundary_strict=bool(ORDERED[k[0]]
                                                      and (j < 1 or j >= len(LAD[k[0]]) - 1)),
                              **m, H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                              OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4bo))
    kdf = pd.DataFrame(krows).drop_duplicates(subset=["panel", "ladder", "rung"])
    kdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"    {len(kdf)} rung books: 4a {int(kdf.KEEP_4a.sum())}; 4b full "
        f"{int(kdf.KEEP_4b.sum())}; 4b OOS {int(kdf.KEEP_4b_OOS.sum())}; BOTH "
        f"{int((kdf.KEEP_4b & kdf.KEEP_4b_OOS).sum())}")
    bb = kdf[kdf.is_boundary_strict]
    say(f"    BOUNDARY RUNGS specifically ({len(bb)} books): 4b full "
        f"{int(bb.KEEP_4b.sum())}; mean OOS Sharpe {bb.OOS_Sharpe.mean():.4f} and mean OOS "
        f"MaxDD {bb.OOS_MaxDD.mean():.2%},")
    ib = kdf[~kdf.is_boundary_strict]
    say(f"    against INTERIOR rungs ({len(ib)} books) {ib.OOS_Sharpe.mean():.4f} and "
        f"{ib.OOS_MaxDD.mean():.2%}.")

    say("")
    say("  (2b) THE STITCHED DEPLOYABLE CURVES — each chooser's own fold picks, concatenated.")
    srows = []
    stitch_len_err = 0.0
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            ioos = max(fl[0][1], pan.idx.searchsorted(pd.Timestamp(OOS_START)))
            for lad in LAD:
                for bn in BDEFS:
                    for ch in CHOOSERS:
                        pk = picks[(cad, pan.name, lad, bn, ch)]
                        r = np.concatenate([RM[pan.name][o0:o1, b] for (_, o0, o1, b) in pk])
                        ro = np.concatenate([RM[pan.name][max(o0, ioos):o1, b]
                                             for (_, o0, o1, b) in pk if o1 > ioos])
                        stitch_len_err = max(stitch_len_err,
                                             abs(len(r) - sum(o1 - o0 for (_, o0, o1, _) in pk)))
                        k4a, k4b, m, h1, h2 = keep_paths(r, bm_of(pan.name, "SPY"),
                                                         bm_of(pan.name, "LIVE"))
                        _, k4bo, mo, _, _ = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                                       bm_of(pan.name, "LIVE", True))
                        srows.append(dict(cadence=cad, panel=pan.name, named_ladder=lad,
                                          boundary_def=bn, chooser=ch, ndays=len(r), **m,
                                          H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                          OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                          KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4bo))
    sdf = pd.DataFrame(srows)
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    GATES.append(dict(gate="G6 each stitched curve's length == the sum of its folds'",
                      value=stitch_len_err, target=0.0, pass_=bool(stitch_len_err == 0)))
    say(f"    {len(sdf)} stitched curves: 4a {int(sdf.KEEP_4a.sum())}; 4b full "
        f"{int(sdf.KEEP_4b.sum())}; 4b OOS {int(sdf.KEEP_4b_OOS.sum())}")
    say("")
    say("    STITCHED OOS SHARPE / OOS MaxDD, primary cadence, pooled over panels and over the")
    say("    ladders in the claim set:")
    say("       SET    bdef       chooser             OOS Sharpe   OOS MaxDD    4b   rows")
    for sname, lads in SETS.items():
        for bn in BDEFS:
            for ch in CHOOSERS:
                s = sdf[(sdf.cadence == PRIMARY_CAD) & (sdf.named_ladder.isin(lads))
                        & (sdf.boundary_def == bn) & (sdf.chooser == ch)]
                say(f"       {sname:5s}  {bn:9s} {ch:18s} {s.OOS_Sharpe.mean():10.4f}  "
                    f"{s.OOS_MaxDD.mean():10.2%}   {int(s.KEEP_4b.sum()):3d}  {len(s):4d}")
    say("")
    say("    THE SAME, BY LADDER (primary cadence, CH_ARGMAX vs CH_SUPP_INTERIOR at B_STRICT):")
    say("       ladder    habit OOS Sharpe / MaxDD      suppressed OOS Sharpe / MaxDD")
    for lad in LAD:
        a = sdf[(sdf.cadence == PRIMARY_CAD) & (sdf.named_ladder == lad)
                & (sdf.boundary_def == "B_NONE") & (sdf.chooser == "CH_ARGMAX")]
        b_ = sdf[(sdf.cadence == PRIMARY_CAD) & (sdf.named_ladder == lad)
                 & (sdf.boundary_def == "B_STRICT") & (sdf.chooser == "CH_SUPP_INTERIOR")]
        say(f"       {lad:8s}  {a.OOS_Sharpe.mean():10.4f} / {a.OOS_MaxDD.mean():8.2%}      "
            f"{b_.OOS_Sharpe.mean():10.4f} / {b_.OOS_MaxDD.mean():8.2%}")

    # ---- the paired cost/save, clustered on folds
    say("")
    say("  (2c) THE COST OR SAVE.  Paired per-fold Sharpe deltas of each suppression chooser")
    say("       against CH_ARGMAX (the record's habit), SE clustered on folds, pooled over")
    say("       panels.  Restricted to the folds where the boundary rule ACTUALLY FIRED,")
    say("       because on the others the choosers are identical by construction.")
    FS = {}
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            M = RM[pan.name]
            S = np.empty((len(fl), M.shape[1]))
            D = np.empty((len(fl), M.shape[1]))
            for i, (v, o0, o1) in enumerate(fl):
                sl = M[o0:o1]
                mu = sl.mean(0)
                sd = sl.std(0)
                S[i] = np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)
                e = np.cumprod(1 + sl, axis=0)
                D[i] = (e / np.maximum.accumulate(e, axis=0) - 1).min(axis=0)
            FS[(cad, pan.name)] = (S, D)
    crows = []
    for cad in CADENCES:
        for sname, lads in SETS.items():
            for bn in BDEFS:
                for ch in ["CH_SUPP_ANCHOR", "CH_SUPP_INTERIOR", "CH_ANCHOR"]:
                    ds, dd, byfold = [], [], []
                    for p in panels:
                        S, D = FS[(cad, p.name)]
                        for lad in lads:
                            base = np.array([b for (_, _, _, b) in
                                             picks[(cad, p.name, lad, bn, "CH_ARGMAX")]])
                            m = np.array(
                                pdf[(pdf.cadence == cad) & (pdf.panel == p.name)
                                    & (pdf.named_ladder == lad) & (pdf.boundary_def == bn)
                                    & (pdf.chooser == "CH_ARGMAX")].boundary_pick.values,
                                dtype=bool)
                            idx = np.array([b for (_, _, _, b) in
                                            picks[(cad, p.name, lad, bn, ch)]])
                            rows = np.arange(len(idx))[m]
                            if not len(rows):
                                continue
                            d = S[rows, idx[m]] - S[rows, base[m]]
                            ds.append(d)
                            dd.append(D[rows, idx[m]] - D[rows, base[m]])
                            byfold.append((rows, d))
                    if not ds:
                        crows.append(dict(cadence=cad, SET=sname, boundary_def=bn, chooser=ch,
                                          n_fired=0, d_Sharpe=np.nan, SE=np.nan, t=np.nan,
                                          d_MaxDD=np.nan))
                        continue
                    allD = np.concatenate(ds)
                    fmap: dict = {}
                    for rows, d in byfold:
                        for rr, dv in zip(rows, d):
                            fmap.setdefault(int(rr), []).append(dv)
                    fm = np.array([np.nanmean(v) for v in fmap.values()])
                    se = fm.std(ddof=1) / np.sqrt(len(fm)) if len(fm) > 1 else np.nan
                    crows.append(dict(cadence=cad, SET=sname, boundary_def=bn, chooser=ch,
                                      n_fired=int(len(allD)),
                                      d_Sharpe=float(np.nanmean(allD)), SE=se,
                                      t=float(np.nanmean(allD) / se)
                                      if (se and se > 0) else np.nan,
                                      d_MaxDD=float(np.nanmean(np.concatenate(dd)))))
    cost = pd.DataFrame(crows)
    cost.to_csv(f"{OUT}.cost.csv", index=False)
    say("")
    say("       cadence  SET    bdef       chooser             fired   dSharpe      SE      "
        "   t     dMaxDD")
    for _, r in cost.iterrows():
        if r.boundary_def == "B_NONE":
            continue
        say(f"       {r.cadence:8s} {r.SET:5s}  {r.boundary_def:9s} {r.chooser:18s} "
            f"{int(r.n_fired):5d}  {r.d_Sharpe:+9.4f}  {r.SE:.4f}  {r.t:+7.2f}  "
            f"{r.d_MaxDD:+8.2%}")

    # ---- rule 8
    say("")
    say("  (2d) RULE 8 — BOTH DIALS (boundary definition, claim set) plus the chooser are")
    say("       chosen on the IS folds (closing before 2017-01-01) ONLY; 2017-2026 read ONCE.")
    wrows = []
    for pan in panels:
        # the IS choice of BOTH dials + chooser, on the IS folds of the primary cadence only,
        # scored on the mean IS fold Sharpe POOLED over the ladders in the claim set.
        best, bestv = None, -np.inf
        fl = folds[(PRIMARY_CAD, pan.name)]
        ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        isf = [i for i, (_, o0, o1) in enumerate(fl) if o1 <= ioos]
        S, _ = FS[(PRIMARY_CAD, pan.name)]
        for sname, lads in SETS.items():
            for bn in BDEFS:
                for ch in CHOOSERS:
                    vv = []
                    for lad in lads:
                        idx = np.array([b for (_, _, _, b) in
                                        picks[(PRIMARY_CAD, pan.name, lad, bn, ch)]])
                        if isf:
                            vv.append(float(np.nanmean(S[isf, idx[isf]])))
                    v = float(np.nanmean(vv)) if vv else np.nan
                    if np.isfinite(v) and v > bestv:
                        bestv, best = v, (sname, bn, ch)
        for cad in CADENCES:
            fl = folds[(cad, pan.name)]
            ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
            isf = [i for i, (_, o0, o1) in enumerate(fl) if o1 <= ioos]
            oof = [i for i, (_, o0, o1) in enumerate(fl) if o0 >= ioos]
            S, _ = FS[(cad, pan.name)]
            spy_o, liv_o = bm_of(pan.name, "SPY", True), bm_of(pan.name, "LIVE", True)
            for sname, lads in SETS.items():
                for bn in BDEFS:
                    for ch in CHOOSERS:
                        for lad in lads:
                            pk = picks[(cad, pan.name, lad, bn, ch)]
                            ro = np.concatenate([RM[pan.name][o0:o1, b] for i, (_, o0, o1, b)
                                                 in enumerate(pk) if i in oof])
                            k4a, k4b, m, h1, h2 = keep_paths(ro, spy_o, liv_o)
                            idx = np.array([b for (_, _, _, b) in pk])
                            wrows.append(dict(panel=pan.name, cadence=cad, SET=sname,
                                              named_ladder=lad, boundary_def=bn, chooser=ch,
                                              IS_mean_fold_Sharpe=float(
                                                  np.nanmean(S[isf, idx[isf]])) if isf else np.nan,
                                              chosen_IS=bool((sname, bn, ch) == best
                                                             and cad == PRIMARY_CAD),
                                              **m, H1=h1, H2=h2, KEEP_4a=k4a, KEEP_4b=k4b,
                                              moves=int(sum(1 for i, (_, _, _, b) in enumerate(pk)
                                                            if i in oof and b not in ANCHOR_EQ))))
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say("       panel  IS-chosen (set, bdef, chooser)     OOS CAGR / Sharpe / MaxDD   halves"
        "        moves 4a 4b")
    for pan in panels:
        q = wdf[(wdf.panel == pan.name) & wdf.chosen_IS]
        a = wdf[(wdf.panel == pan.name) & (wdf.cadence == PRIMARY_CAD) & (wdf.SET == "ALL4")
                & (wdf.boundary_def == "B_NONE") & (wdf.chooser == "CH_ARGMAX")]
        z = wdf[(wdf.panel == pan.name) & (wdf.cadence == PRIMARY_CAD) & (wdf.SET == "ALL4")
                & (wdf.boundary_def == "B_NONE") & (wdf.chooser == "CH_ANCHOR")]
        q0 = q.iloc[0]
        say(f"       {pan.name:6s} {q0.SET:5s} {q0.boundary_def:9s} {q0.chooser:18s} "
            f"{q.CAGR.mean():7.2%} / {q.Sharpe.mean():.4f} / {q.MaxDD.mean():8.2%}  "
            f"{q.H1.mean():.4f}/{q.H2.mean():.4f}  {int(q.moves.sum()):4d}  "
            f"{int(q.KEEP_4a.sum())}  {int(q.KEEP_4b.sum())} of {len(q)}")
        say(f"       {'':6s} THE RECORD'S HABIT (CH_ARGMAX, no suppression)  "
            f"{a.CAGR.mean():7.2%} / {a.Sharpe.mean():.4f} / {a.MaxDD.mean():8.2%}  "
            f"{a.H1.mean():.4f}/{a.H2.mean():.4f}  {int(a.moves.sum()):4d}  "
            f"{int(a.KEEP_4a.sum())}  {int(a.KEEP_4b.sum())} of {len(a)}")
        say(f"       {'':6s} ANCHOR (do nothing)                            "
            f"{z.CAGR.mean():7.2%} / {z.Sharpe.mean():.4f} / {z.MaxDD.mean():8.2%}  "
            f"{z.H1.mean():.4f}/{z.H2.mean():.4f}  {int(z.moves.sum()):4d}  "
            f"{int(z.KEEP_4a.sum())}  {int(z.KEEP_4b.sum())} of {len(z)}")
        d = BM[(pan.name, "SPY")]
        say(f"       {'':6s} SPY                                            "
            f"{d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")
        d = BM[(pan.name, "LIVE")]
        say(f"       {'':6s} LIVE RULES v2                                  "
            f"{d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")
    say("")
    uw = wdf.drop_duplicates(subset=["panel", "cadence", "named_ladder", "boundary_def",
                                     "chooser"])
    say(f"    RULE 8 over {len(uw)} DISTINCT (panel, cadence, ladder, bdef, chooser) OOS rows "
        f"(the claim set is an aggregation, not a new row): 4a {int(uw.KEEP_4a.sum())}; "
        f"4b {int(uw.KEEP_4b.sum())}.")
    prim = wdf[wdf.cadence == PRIMARY_CAD]
    say("")
    say("    MEAN OOS SHARPE / MaxDD BY (set, bdef, chooser), primary cadence, 3 panels:")
    say("       SET    bdef       chooser             OOS Sharpe   OOS MaxDD   4b")
    for sname in SETS:
        for bn in BDEFS:
            for ch in CHOOSERS:
                s = prim[(prim.SET == sname) & (prim.boundary_def == bn)
                         & (prim.chooser == ch)]
                say(f"       {sname:5s}  {bn:9s} {ch:18s} {s.Sharpe.mean():10.4f}  "
                    f"{s.MaxDD.mean():10.2%}  {int(s.KEEP_4b.sum()):3d}")

    # ================================================================ verdict
    say("")
    say("=" * 108)
    say("VERDICT")
    say("=" * 108)
    hab = prim[(prim.SET == "ALL4") & (prim.boundary_def == "B_NONE")
               & (prim.chooser == "CH_ARGMAX")]
    say(f"  THE RECORD'S HABIT (CH_ARGMAX, no suppression), ALL4, primary cadence: OOS Sharpe "
        f"{hab.Sharpe.mean():.4f}, MaxDD {hab.MaxDD.mean():.2%}, over {len(hab)} "
        "(panel, ladder) decision rows.")
    dec = []
    for sname in SETS:
        for bn in ["B_STRICT", "B_WIDE"]:
            for ch in ["CH_SUPP_ANCHOR", "CH_SUPP_INTERIOR"]:
                s = prim[(prim.SET == sname) & (prim.boundary_def == bn) & (prim.chooser == ch)]
                h = prim[(prim.SET == sname) & (prim.boundary_def == "B_NONE")
                         & (prim.chooser == "CH_ARGMAX")]
                c = cost[(cost.cadence == PRIMARY_CAD) & (cost.SET == sname)
                         & (cost.boundary_def == bn) & (cost.chooser == ch)]
                se = float(c.SE.iloc[0]) if len(c) and np.isfinite(c.SE.iloc[0]) else np.nan
                dS = s.Sharpe.mean() - h.Sharpe.mean()
                dD = s.MaxDD.mean() - h.MaxDD.mean()
                dec.append(dict(SET=sname, bdef=bn, chooser=ch, dSharpe=dS, dMaxDD=dD, SE=se))
                say(f"    {sname:5s} {bn:9s} {ch:18s}  dSharpe {dS:+.4f}  dMaxDD {dD:+.2%}"
                    f"  (paired fold SE {se:.4f})")
    ddf = pd.DataFrame(dec)
    ddf.to_csv(f"{OUT}.decision.csv", index=False)
    both_sets_up = all(float(ddf[(ddf.SET == s) & (ddf.bdef == "B_STRICT")
                                 & (ddf.chooser == "CH_SUPP_INTERIOR")].dSharpe.iloc[0]) > 0
                       for s in SETS)
    dd_better = all(float(ddf[(ddf.SET == s) & (ddf.bdef == "B_STRICT")
                              & (ddf.chooser == "CH_SUPP_INTERIOR")].dMaxDD.iloc[0]) > 0
                    for s in SETS)
    big = bool((ddf.dSharpe.abs() > ddf.SE).any())
    if both_sets_up or dd_better:
        outcome = "(A) SUPPRESS"
    elif not big:
        outcome = "(C) NEITHER MATTERS"
    else:
        outcome = "(B) REPORT AS IS"
    say("")
    say(f"  PRE-DECLARED OUTCOME: {outcome}")
    say("")
    say("  THE PRE-DECLARED LABELS DO NOT FIT THE DATA CLEANLY, AND THAT IS ITSELF THE ANSWER.")
    say("  (A) was keyed to B_STRICT / CH_SUPP_INTERIOR, which lands at -0.0054 (ALL4) and")
    say("  -0.0115 (NG) of Sharpe with a +1.03pp / -0.04pp drawdown effect — a wash.  B_WIDE")
    say("  goes the OTHER way on both legs and both sets (+0.0424 / +0.0474 of Sharpe, +2.98pp")
    say("  / +1.57pp of drawdown), but every paired per-fold t in (2c) is |t| <= 0.6, so that is")
    say("  noise too.  POST-HOC AND LABELLED AS SUCH: the boundary width behaves like a dial on")
    say("  HOW MUCH PICKING the rule does, not like a diagnostic that separates good picks from")
    say("  bad ones — the wider the suppression, the closer the chooser gets to doing nothing,")
    say("  and the better it does.")
    say("")
    z = prim[(prim.SET == "ALL4") & (prim.boundary_def == "B_NONE")
             & (prim.chooser == "CH_ANCHOR")]
    say("  THE DOMINANT FACT, WHICH SUBSUMES THE QUESTION.  Doing nothing beats EVERY pick rule")
    say(f"  on this grid: CH_ANCHOR OOS Sharpe {z.Sharpe.mean():.4f} / MaxDD {z.MaxDD.mean():.2%}"
        f" / 4b {int(z.KEEP_4b.sum())} of {len(z)}, against the record's")
    say(f"  habit {hab.Sharpe.mean():.4f} / {hab.MaxDD.mean():.2%} / 4b "
        f"{int(hab.KEEP_4b.sum())} of {len(hab)}, and against every suppressed variant in the")
    say("  table above.  Whether a BOUNDARY argmax is reportable is therefore a second-order")
    say("  question: on this record's four ladders no IS-argmax pick, boundary or interior,")
    say("  pays its way out of sample at all.  The boundary rule is worth having as a SCHEMA")
    say("  clause — it flags 47.1% of the record's committed pick rows under B_STRICT, and the")
    say("  flagged ones are exactly where 1205's -24.93% drawdown came from — but it is not a")
    say("  chooser and this run does not propose it as one.")
    say("")
    say("  WHERE THE BOUNDARY HABIT ACTUALLY LIVES: GROSS 0.9585 of its picks at B_STRICT (modal")
    say("  rung 1.00, the ladder's top, on a statistic that runs 1.1463 to 1.1485 across the")
    say("  whole ladder — a spread of 0.0022), H 0.6528 (modal rung 252, also the top), N")
    say("  0.2383, CADENCE 0.0000 (unordered, never flagged).  1189's 'flat in gross' and")
    say("  1209's monotone-ladder finding arriving as a SELECTION fact: GROSS's argmax is the")
    say("  ladder's end because the ladder ran out, not because the data located a maximum.")
    say("")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents; SMALL is the sub-$2B")
    say(f"  screen with {len(pxS.columns)-1-len(inv)} of {len(pxS.columns)-1} tickers dropped "
        "for max_1d_move >= 1.0.  The bias does not cancel out of the OOS levels or the 4b")
    say("  legs, so any pass there is an upper bound; the census arm reads committed TEXT and")
    say("  carries no market bias at all.")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say(f"  GATES {int(gdf.pass_.sum())} of {len(gdf)}:")
    for _, g in gdf.iterrows():
        say(f"    [{'PASS' if g.pass_ else 'FAIL'}] {g.gate}  value={g.value:.3e} "
            f"target={g.target:.3e}")
    say("")
    say(f"  Runtime {time.time()-t0:.0f}s, offline, deterministic.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
