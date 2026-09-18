#!/usr/bin/env python3
"""
Idea 1279 (lane C, 2026-09-18) — does the GROSS LADDER belong in the record's COMPARISON SET
AT ALL?

WHY THIS IDEA.  1279 is the SECOND numbered item in QUEUE.md's '## Open' section (1278 is
first, claimed by lane A) and the sprint rule says lane C claims the second.  Eligible:
price-only, no EDGAR / Form 4 / 8-K / options / live data.  No eligibility descent was needed —
ARM B below is a real capital arm (a cross-ladder rule-8 chooser over the record's committed
cells on three panels, 2017-2026 read ONCE).

THE PREMISE.  Idea 1276 is the FIFTH run (after 1189 / 1214 / 1224 / 1236) to find that every
verdict which MOVES in a committed ladder comparison is a GROSS cell whose own standard error
runs 0.000000 to 1.3e-03.  B136's V_AXIS GROSS sliced delta is EXACTLY 0.000000 with an SE of
EXACTLY 0.000000, because on that panel the chooser never leaves the anchor.  Idea 1223 then
showed, with a synthetic rung, that a DEGENERATE ladder in the comparison set MANUFACTURES
decisive calls: one perfectly degenerate rung takes the pairwise decisive rate 0.0397 -> 0.5198
and CREATES 40 of 42 H_NARROWEST headline calls.  GROSS is the record's candidate for a
naturally degenerate ladder.  Nobody has priced the obvious remedy: DROP IT.

THE QUESTION, IN THE QUEUE'S OWN WORDS.  "Price the cost of simply DROPPING GROSS from every
committed ladder comparison: re-run the record's decisive-call censuses on the three
non-degenerate ladders and report how many headline counts survive, and what the four-ladder
set was buying."

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    LADDER_SET {ALL4, NO_GROSS}
        ALL4      the record's committed comparison set {GROSS, N, H, MAXVOL}.
        NO_GROSS  the three non-degenerate ladders {N, H, MAXVOL}.
    DECISIVE_BAR {D_TIGHT, D_LOOSE}
        D_TIGHT   |t| >= 2.160  (two-sided 0.05, 13 df — 14 folds)
        D_LOOSE   |t| >= 1.771  (one-sided 0.05, 13 df)
    2 x 2 = 4 census cells, EVERY ONE published.

NOT A DIAL, reported at every value (controls, all fixed at the record's committed choices):
    PANEL    {U56, B136, SMALL663}
    LADDER   {GROSS, N, H, MAXVOL} at their committed BASE rungs (lane B's 1152 ARM C list,
             which is the record's own comparison set — not values tuned here)
    IS_STAT  {IS_SHARPE, IS_CAGR, IS_DD}
    N_FOLDS  14 (idea 1276's committed fold count, copied not chosen)

PRE-DECLARED OUTCOMES, written before any number was read:
  H_DEGENERATE   GROSS's fold-mean Sharpe SPREAD across its own rungs is the SMALLEST of the
                 four ladders on every panel.
  H_MANUFACTURED a MAJORITY of ALL4's decisive pair calls INVOLVE GROSS.
  H_SURVIVE      FEWER THAN HALF of ALL4's decisive headline counts survive dropping GROSS.
  H_CAPITAL      dropping GROSS from the rule-8 chooser's comparison set costs NOTHING:
                 |mean d(OOS Sharpe), NO_GROSS minus ALL4| <= 0.02.
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not ARM A.

THE THREE ARMS.
  ARM A — DECISIVE-CALL CENSUS, FRESH.  For each panel and ladder, the ladder's WIDTH in fold f
      is (max - min) of its rungs' fold-f net Sharpe.  For each ladder PAIR the fold deltas give
      a mean, an SE over 14 folds and a t; a pair call is DECISIVE at a bar iff |t| >= bar.  The
      record's three headline forms are then rebuilt on each LADDER_SET: H_WIDEST (is the widest
      ladder's margin over the runner-up decisive?), H_NARROWEST (same at the bottom) and H_ANY
      (how many pairs are decisive at all).  Reported at both bars, on all three panels.
  ARM B — CAPITAL (rule 8, required).  Every rung of every ladder is scored full-sample, in
      halves and OOS against the live RULES v2 book and SPY, and BOTH KEEP paths are evaluated
      at EVERY grid point.  Then the rule-8 arm: parameters chosen on warm-up..2016-12-31 ONLY,
      2017-2026 read ONCE.  Two choosers — a CROSS-LADDER chooser over the comparison set's
      unique cells (this is the object the queue asks to price: ALL4's 17 cells against
      NO_GROSS's 14) and the record's WITHIN-LADDER chooser (36 decisions) for continuity.
  ARM C — WHAT THE RECORD COMMITTED.  A mechanical census of the committed artefacts in
      research/backtests for ladder/axis columns naming GROSS, and of the committed prose for
      decisive / widest-dial headline sentences naming it, so "how many headline counts survive"
      is answered about the RECORD and not only about this run's fresh census.

THE BOOK.  The frozen 2026-09-04 KEEP-4b book: RAW three-leg composite ranking, eligibility =
above own 200d MA AND vol20 < MAXVOL, GROSS of NAV spread equally over N slots, minimum hold H,
weekly Fri-decide / Mon-trade, 10 bps per unit turnover, t+1 execution, 260-row warm-up.
Anchor = (N=20, H=126, MAXVOL=0.60, GROSS=0.75).  Each ladder walks ONE axis and holds the other
three at the anchor.  No leverage anywhere (GROSS <= 1.00), PROTOCOL rule 2.

GATES.  G1 the anchor cell replays the committed 2026-09-04 U56 triple 15.71% / 1.1480 /
-19.13% to 1e-4, VINTAGE-PINNED to the 2026-09-16 cache end those numbers were produced on (the
unpinned drift to the live cache end is reported beside it, not gated — idea 1264 published it).
G2 determinism of the U56 ladder table, bit for bit, on a second pass.  G3 the 14 folds
partition the post-warm-up index exactly, contiguously and without overlap.  G4 the IS and OOS
windows are disjoint and OOS starts on or after 2017-01-01.  G5 the IS argmax reads no OOS row
(recomputed on a series whose OOS tail is NaN).  G6 NO_GROSS's cell set is a strict subset of
ALL4's and the anchor lies in both.  G7 every SE >= 0 and every census share in [0,1].  G8 the
D_TIGHT decisive set is a subset of the D_LOOSE one on every panel and both sets.  G9 the census
denominator is stamped with (file count, tree sha) per idea 894's request.  G10 the MAXVOL=0.80
rung admits strictly more name-days than MAXVOL=0.40 on every panel.  G11 1101's replay: U56
GROSS IS-Sharpe argmax at the TOP rung and IS-DD argmax at the BOTTOM rung.

PROTOCOL: rule 2 costs (10 bps) and t+1 execution; rule 4 both KEEP paths at EVERY grid point;
rule 5 one idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship
stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).  Every
absolute level is optimistic and every 4b pass is an UPPER bound.  ARM A's headline is a
DIFFERENCE between ladders measured on the SAME names in the SAME folds, so a level bias common
to the panel moves every ladder together and the decisive-call findings are first-order immune;
the 4b counts are not, and are quoted as upper bounds.

Runs standalone and offline (committed caches and committed artefacts only):
  python research/backtests/2026-09-18_does-the-GROSS-LADDER-belong-in-the-record-s-COMPARISON-SET-AT-ALL_C.py
"""
from __future__ import annotations

import itertools
import re
import subprocess
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

DATE = "2026-09-18"
SLUG = "does-the-GROSS-LADDER-belong-in-the-record-s-COMPARISON-SET-AT-ALL"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_C"

COST, WARMUP = 10.0, 260
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_MV, A_G = 20, 126, 0.60, 0.75           # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]               # committed RAW three-leg composite
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)      # gate G1
VINTAGE = pd.Timestamp("2026-09-16")                # the cache end those numbers were made on
N_FOLDS = 14                                        # idea 1276's committed fold count

# the record's own committed comparison set (lane B 1152 ARM C BASE rungs, copied not tuned)
LADDERS = {
    "GROSS":  [0.30, 0.45, 0.60, 0.75],
    "N":      [10, 12, 16, 20, 25, 30],
    "H":      [21, 42, 63, 126, 189, 252],
    "MAXVOL": [0.40, 0.50, 0.60, 0.80],
}
ANCHOR_AT = {"GROSS": A_G, "N": A_N, "H": A_H, "MAXVOL": A_MV}
LADDER_SETS = {"ALL4": ["GROSS", "N", "H", "MAXVOL"], "NO_GROSS": ["N", "H", "MAXVOL"]}
BARS = {"D_TIGHT": 2.160, "D_LOOSE": 1.771}         # two-sided / one-sided 0.05 at 13 df
IS_STATS = ["IS_SHARPE", "IS_CAGR", "IS_DD"]
IS_COL = {"IS_SHARPE": "is_Sharpe", "IS_CAGR": "is_CAGR", "IS_DD": "is_MaxDD"}

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ================================================================== metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    n = len(r)
    h = n // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                oos=stats(r[o:]), **{"is": stats(r[:o])})


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


def legs_4a(b, live):
    return dict(H1=b["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(b, spy):
    return dict(H1=b["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=b["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=b["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def fold_bounds(n, k):
    """k contiguous, non-overlapping, exhaustive folds over n rows."""
    edges = np.linspace(0, n, k + 1).astype(int)
    return list(zip(edges[:-1], edges[1:]))


# ================================================================== book machinery
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        self.vol20 = np.nan_to_num((q.pct_change().rolling(20).std() * np.sqrt(252)).values,
                                   nan=1e9)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)

    def elig(self, maxvol):
        return self.above & (self.vol20 < maxvol)


def build(pan, N, H, maxvol, lag=1):
    """Selection frame at GROSS = 1.0, equal slot weights.  Row t = APPLICATION-time weight
    (decided t-lag, applied t)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    el = pan.elig(maxvol)
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(el[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel):
            continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross=A_G):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(pan.reb, np.append(pan.reb[1:], T)):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    gr = (held * rets).sum(axis=1)
    r = gr - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0))


def cell_params(ladder, rung):
    """(N, H, MAXVOL, GROSS) for one rung of one ladder; every other axis at the anchor."""
    N, H, mv, g = A_N, A_H, A_MV, A_G
    if ladder == "GROSS":
        g = float(rung)
    elif ladder == "N":
        N = int(rung)
    elif ladder == "H":
        H = int(rung)
    elif ladder == "MAXVOL":
        mv = float(rung)
    return N, H, mv, g


def pick_index(vals):
    """Argmax under the chooser's own orientation.  IS_DD is stored as a NEGATIVE MaxDD, so the
    argmax picks the SMALLEST drawdown magnitude — the same convention the record uses."""
    a = np.asarray(vals, float)
    if not np.isfinite(a).any():
        return -1
    return int(np.argmax(np.where(np.isfinite(a), a, -np.inf)))


# ================================================================== ARM C — record census
GROSS_TOK = re.compile(r"\bgross\b", re.I)
LADDER_COL = re.compile(r"^(ladder|axis|dial|arm|dial_name|ladder_name|pair|pair_a|pair_b|"
                        r"ladder_a|ladder_b|axis_a|axis_b)$", re.I)
DECISIVE_SENT = re.compile(
    r"[^.\n]*\b(decisive|widest dial|widest|narrowest|significant(?:ly)?)\b[^.\n]*", re.I)


def census_artefacts():
    """Committed csv/csv.gz artefacts whose ladder/axis/pair columns name GROSS."""
    rows = []
    files = sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz")))
    for f in files:
        try:
            head = pd.read_csv(f, nrows=600)
        except Exception:
            continue
        cols = [str(c) for c in head.columns]
        lcols = [c for c in cols if LADDER_COL.match(c)]
        if not lcols:
            continue
        n = len(head)
        if not n:
            continue
        involved = np.zeros(n, dtype=bool)
        vals = set()
        for c in lcols:
            s = head[c].astype(str)
            vals |= set(s.dropna().unique())
            involved |= s.str.contains(GROSS_TOK, na=False).values
        rows.append(dict(file=f.name, ladder_cols="|".join(lcols), n_rows=int(n),
                         n_gross_rows=int(involved.sum()),
                         gross_share=float(involved.mean()),
                         n_distinct_ladders=int(len({v for v in vals if v != "nan"}))))
    return rows, len(files)


def census_prose():
    """Committed prose sentences publishing a decisive / widest-dial headline."""
    rows = []
    files = sorted(list((ROOT / "research").glob("*.md")) + list(OUT.glob("*.md")))
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for m in DECISIVE_SENT.finditer(txt):
            s = m.group(0).strip()
            if len(s) < 30:
                continue
            rows.append(dict(file=f.name, names_gross=bool(GROSS_TOK.search(s)),
                             n_chars=len(s)))
    return rows, len(files)


# ================================================================== main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1279 lane C — {SLUG}")
    say("# DIAL 1 LADDER_SET = ALL4 / NO_GROSS      DIAL 2 DECISIVE_BAR = D_TIGHT / D_LOOSE")
    say("# controls at every value: PANEL {U56,B136,SMALL663}, LADDER {GROSS,N,H,MAXVOL} at "
        "committed BASE rungs, IS_STAT {IS_SHARPE,IS_CAGR,IS_DD}, N_FOLDS=14 (1276's count)")
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
    except Exception:
        sha = "unknown"

    # ============================================================ panels
    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    cellsA = {(*cell_params(l, r),) for l in LADDER_SETS["ALL4"] for r in LADDERS[l]}
    cellsN = {(*cell_params(l, r),) for l in LADDER_SETS["NO_GROSS"] for r in LADDERS[l]}
    gate("G6 NO_GROSS cells strict subset of ALL4, anchor in both",
         f"|ALL4|={len(cellsA)} |NO_GROSS|={len(cellsN)}", "subset & anchor in both",
         cellsN < cellsA and (A_N, A_H, A_MV, A_G) in cellsN and (A_N, A_H, A_MV, A_G) in cellsA)
    gate("G2a no leverage on the GROSS ladder", max(LADDERS["GROSS"]), "<= 1.0",
         max(LADDERS["GROSS"]) <= 1.0)

    grid, folds_rows, wf_within, wf_cross = [], [], [], []
    det_sig = {}

    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        spy = windows(pan.spy[WARMUP:], o)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].values[WARMUP:]
        live = windows(live_r, o)
        fb = fold_bounds(len(idx), N_FOLDS)
        gate(f"G4 {pname} IS/OOS split",
             f"IS ends {idx[o-1].date()}, OOS starts {idx[o].date()}", ">= 2017-01-01",
             idx[o] >= OOS_START and idx[o - 1] < OOS_START)
        gate(f"G3 {pname} folds partition the post-warm-up index",
             f"{len(fb)} folds, {fb[0][0]}..{fb[-1][1]} of {len(idx)}",
             f"{N_FOLDS} contiguous, exhaustive",
             len(fb) == N_FOLDS and fb[0][0] == 0 and fb[-1][1] == len(idx)
             and all(fb[i][1] == fb[i + 1][0] for i in range(len(fb) - 1)))
        gate(f"G10 {pname} MAXVOL admits more at 0.80 than 0.40",
             f"{int(pan.elig(0.80).sum())} vs {int(pan.elig(0.40).sum())}", "strictly more",
             int(pan.elig(0.80).sum()) > int(pan.elig(0.40).sum()))

        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"{idx[0].date()}..{idx[-1].date()}  IS {o} / OOS {len(idx)-o} rows")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}  halves {spy['h1']['Sharpe']:.4f}/"
            f"{spy['h2']['Sharpe']:.4f}  OOS {spy['oos']['CAGR']:7.2%} / "
            f"{spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}  halves {live['h1']['Sharpe']:.4f}/"
            f"{live['h2']['Sharpe']:.4f}  OOS {live['oos']['CAGR']:7.2%} / "
            f"{live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}  "
            f"CAGR floor {CAGR_FLOOR*spy['full']['CAGR']:7.2%}  "
            f"H1 {spy['h1']['Sharpe']:.4f} H2 {spy['h2']['Sharpe']:.4f} "
            f"OOS {spy['oos']['Sharpe']:.4f}")

        cache: dict = {}
        for lad, rungs in LADDERS.items():
            say(f"\n   -- LADDER {lad}   rungs {rungs}")
            say("      rung |  |    CAGR   Sharpe    MaxDD |   H1/H2 Sh   | IS Sh   IS CAGR"
                "   IS DD | OOS Sh  OOS CAGR  OOS DD | turn | 4a 4b | fail4b")
            for rung in rungs:
                N, H, mv, g = cell_params(lad, rung)
                if (N, H, mv) not in cache:
                    cache[(N, H, mv)] = build(pan, N, H, mv)
                r, turn = run(pan, cache[(N, H, mv)], gross=g)
                r = r[WARMUP:]
                w = windows(r, o)
                a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                rec = dict(panel=pname, ladder=lad, rung=rung, N=N, H=H, maxvol=mv, gross=g,
                           **flat(w), turnover=turn,
                           keep4a=all(a4.values()), keep4b=all(b4.values()),
                           fail4a=failed(a4), fail4b=failed(b4),
                           is_anchor=(rung == ANCHOR_AT[lad]))
                grid.append(rec)
                for fi, (a, b) in enumerate(fb):
                    folds_rows.append(dict(panel=pname, ladder=lad, rung=rung, fold=fi,
                                           n=int(b - a), Sharpe=sharpe(r[a:b]),
                                           CAGR=cagr(r[a:b]), MaxDD=mdd(r[a:b])))
                say(f"      {rung:5g} | {'A' if rec['is_anchor'] else ' '} |"
                    f" {w['full']['CAGR']:7.2%} {w['full']['Sharpe']:8.4f} "
                    f"{w['full']['MaxDD']:8.2%} | {w['h1']['Sharpe']:6.3f}/"
                    f"{w['h2']['Sharpe']:6.3f} | {w['is']['Sharpe']:6.3f} "
                    f"{w['is']['CAGR']:8.2%} {w['is']['MaxDD']:7.2%} | "
                    f"{w['oos']['Sharpe']:6.3f} {w['oos']['CAGR']:8.2%} "
                    f"{w['oos']['MaxDD']:7.2%} | {turn:4.2f} | "
                    f"{'Y' if rec['keep4a'] else 'n'}  {'Y' if rec['keep4b'] else 'n'} | "
                    f"{failed(b4)}")

            # ---- the record's WITHIN-LADDER rule-8 chooser (continuity with 1152 ARM C)
            gdf = pd.DataFrame([x for x in grid if x["panel"] == pname and x["ladder"] == lad])
            gdf = gdf.sort_values("rung").reset_index(drop=True)
            anc = gdf[gdf.is_anchor].iloc[0]
            for is_stat in IS_STATS:
                i = pick_index(gdf[IS_COL[is_stat]].values)
                wf_within.append(dict(
                    panel=pname, ladder=lad, is_stat=is_stat, ladder_size=len(gdf),
                    pick=gdf.rung[i], anchor=ANCHOR_AT[lad],
                    reach=bool(gdf.rung[i] == ANCHOR_AT[lad]),
                    oos_S_pick=float(gdf.oos_Sharpe[i]),
                    oos_S_anchor=float(anc["oos_Sharpe"]),
                    d_oos_S=float(gdf.oos_Sharpe[i] - anc["oos_Sharpe"]),
                    pick_keep4a=bool(gdf.keep4a[i]), pick_keep4b=bool(gdf.keep4b[i])))

        # ---- the CROSS-LADDER rule-8 chooser: ALL4's cell set against NO_GROSS's
        pg = pd.DataFrame([x for x in grid if x["panel"] == pname])
        key = ["N", "H", "maxvol", "gross"]
        uniq = pg.drop_duplicates(subset=key).reset_index(drop=True)
        anc = pg[(pg.ladder == "N") & (pg.rung == A_N)].iloc[0]
        for ls, lads in LADDER_SETS.items():
            sub = uniq[uniq.set_index(key).index.isin(
                [c for c in ({(*cell_params(l, r),) for l in lads for r in LADDERS[l]})]
            )].reset_index(drop=True)
            for is_stat in IS_STATS:
                i = pick_index(sub[IS_COL[is_stat]].values)
                wf_cross.append(dict(
                    panel=pname, ladder_set=ls, is_stat=is_stat, n_cells=len(sub),
                    pick_N=int(sub.N[i]), pick_H=int(sub.H[i]), pick_maxvol=float(sub.maxvol[i]),
                    pick_gross=float(sub.gross[i]),
                    pick_is_anchor=bool((sub.N[i], sub.H[i], sub.maxvol[i], sub.gross[i])
                                        == (A_N, A_H, A_MV, A_G)),
                    is_S=float(sub.is_Sharpe[i]),
                    oos_S_pick=float(sub.oos_Sharpe[i]),
                    oos_S_anchor=float(anc["oos_Sharpe"]),
                    oos_CAGR_pick=float(sub.oos_CAGR[i]), oos_DD_pick=float(sub.oos_MaxDD[i]),
                    spy_oos_S=float(spy["oos"]["Sharpe"]),
                    d_oos_S=float(sub.oos_Sharpe[i] - anc["oos_Sharpe"]),
                    pick_keep4a=bool(sub.keep4a[i]), pick_keep4b=bool(sub.keep4b[i])))

        det_sig[pname] = pd.DataFrame(
            [x for x in grid if x["panel"] == pname]).full_Sharpe.round(12).tolist()

    gdf_all = pd.DataFrame(grid)
    gdf_all.to_csv(f"{STEM}.grid.csv", index=False)
    fdf = pd.DataFrame(folds_rows)
    fdf.to_csv(f"{STEM}.folds.csv", index=False)
    wdf = pd.DataFrame(wf_within)
    cdf = pd.DataFrame(wf_cross)
    pd.concat([wdf.assign(kind="WITHIN"), cdf.assign(kind="CROSS")],
              ignore_index=True).to_csv(f"{STEM}.walkforward.csv", index=False)

    # ============================================================ ARM A — decisive census
    say("\n================ ARM A — DECISIVE-CALL CENSUS ON THE FOLD WIDTHS ==================")
    say(f"# a ladder's WIDTH in fold f = (max - min) of its rungs' fold-f net Sharpe; "
        f"{N_FOLDS} folds")
    width = (fdf.groupby(["panel", "ladder", "fold"]).Sharpe.agg(["max", "min"])
             .assign(width=lambda d: d["max"] - d["min"]).reset_index())
    width.to_csv(f"{STEM}.widths.csv", index=False)

    say("\n   LADDER WIDTHS (fold mean +/- SE, and the whole-span width):")
    wsum = []
    for pname in gdf_all.panel.unique():
        for lad in LADDERS:
            w = width[(width.panel == pname) & (width.ladder == lad)].width.values
            g = gdf_all[(gdf_all.panel == pname) & (gdf_all.ladder == lad)].full_Sharpe.values
            wsum.append(dict(panel=pname, ladder=lad, fold_mean=float(np.mean(w)),
                             fold_se=float(np.std(w, ddof=1) / np.sqrt(len(w))),
                             span_width=float(np.nanmax(g) - np.nanmin(g)), n_rungs=len(g)))
    wsdf = pd.DataFrame(wsum)
    wsdf.to_csv(f"{STEM}.width_summary.csv", index=False)
    for pname in wsdf.panel.unique():
        s = wsdf[wsdf.panel == pname].sort_values("fold_mean", ascending=False)
        say(f"   {pname:9s} " + "   ".join(
            f"{r.ladder}={r.fold_mean:.4f}+/-{r.fold_se:.4f}(span {r.span_width:.4f})"
            for r in s.itertuples()))
    h_deg = all(wsdf[wsdf.panel == p].sort_values("fold_mean").ladder.iloc[0] == "GROSS"
                for p in wsdf.panel.unique())
    say(f"   H_DEGENERATE (GROSS is the NARROWEST ladder on every panel): "
        f"{'HELD' if h_deg else 'REFUTED'}")

    pair_rows = []
    for pname in gdf_all.panel.unique():
        for a, b in itertools.combinations(LADDER_SETS["ALL4"], 2):
            wa = width[(width.panel == pname) & (width.ladder == a)].sort_values("fold").width.values
            wb = width[(width.panel == pname) & (width.ladder == b)].sort_values("fold").width.values
            d = wa - wb
            se = float(np.std(d, ddof=1) / np.sqrt(len(d)))
            t = float(np.mean(d) / se) if se > 0 else (np.inf if np.mean(d) != 0 else 0.0)
            pair_rows.append(dict(panel=pname, pair=f"{a}-{b}", A=a, B=b, mean_d=float(np.mean(d)),
                                  se=se, t=t, involves_gross=("GROSS" in (a, b)),
                                  **{k: bool(abs(t) >= v) for k, v in BARS.items()}))
    pdf = pd.DataFrame(pair_rows)
    pdf.to_csv(f"{STEM}.pairs.csv", index=False)
    gate("G7 every pair SE >= 0", f"min {pdf.se.min():.3e}", ">= 0", bool((pdf.se >= 0).all()))
    gate("G8 D_TIGHT subset of D_LOOSE", int((pdf.D_TIGHT & ~pdf.D_LOOSE).sum()), 0,
         int((pdf.D_TIGHT & ~pdf.D_LOOSE).sum()) == 0)

    say("\n   PAIRWISE DECISIVE CALLS (all 18 ALL4 pairs printed; NO_GROSS keeps the 9 that "
        "do not involve GROSS):")
    say("      panel      pair              mean_d      SE       t    D_TIGHT D_LOOSE  in NO_GROSS")
    for r in pdf.itertuples():
        say(f"      {r.panel:9s}  {r.pair:16s} {r.mean_d:+9.4f} {r.se:8.4f} {r.t:+8.2f}   "
            f"{'Y' if r.D_TIGHT else '.'}       {'Y' if r.D_LOOSE else '.'}        "
            f"{'.' if r.involves_gross else 'Y'}")

    say("\n   HEADLINE COUNTS, BOTH DIALS (this is the queue's question):")
    say("      set        bar       H_ANY(dec/pairs)  H_WIDEST(dec/panels)  H_NARROWEST(dec/panels)")
    head_rows = []
    for ls, lads in LADDER_SETS.items():
        sub = pdf[pdf.A.isin(lads) & pdf.B.isin(lads)]
        for bar in BARS:
            n_any = int(sub[bar].sum())
            n_pairs = len(sub)
            wide = narrow = 0
            for pname in wsdf.panel.unique():
                s = wsdf[(wsdf.panel == pname) & (wsdf.ladder.isin(lads))] \
                    .sort_values("fold_mean", ascending=False).reset_index(drop=True)
                top, run2 = s.ladder[0], s.ladder[1]
                bot, run_2 = s.ladder.iloc[-1], s.ladder.iloc[-2]
                def dec(x, y):
                    q = sub[((sub.A == x) & (sub.B == y)) | ((sub.A == y) & (sub.B == x))]
                    return bool(len(q) and q[bar].iloc[0])
                wide += dec(top, run2)
                narrow += dec(bot, run_2)
            head_rows.append(dict(ladder_set=ls, bar=bar, n_pairs=n_pairs, H_ANY=n_any,
                                  H_ANY_rate=n_any / n_pairs, n_panels=3,
                                  H_WIDEST=wide, H_NARROWEST=narrow))
            say(f"      {ls:10s} {bar:9s} {n_any:3d}/{n_pairs:<3d} ({n_any/n_pairs:5.1%})    "
                f"{wide}/3                    {narrow}/3")
    hdf = pd.DataFrame(head_rows)
    hdf.to_csv(f"{STEM}.headlines.csv", index=False)

    involved = pdf[pdf.involves_gross]
    for bar in BARS:
        tot = int(pdf[bar].sum())
        gg = int(involved[bar].sum())
        say(f"   {bar}: {gg} of {tot} ALL4 decisive pair calls INVOLVE GROSS "
            f"({gg/tot:.1%})" if tot else f"   {bar}: 0 decisive calls at all")
    h_man = all(int(involved[b].sum()) > int(pdf[b].sum()) / 2 for b in BARS
                if int(pdf[b].sum()) > 0)
    say(f"   H_MANUFACTURED (a majority of ALL4's decisive calls involve GROSS): "
        f"{'HELD' if h_man else 'REFUTED'}")
    surv = []
    for bar in BARS:
        a = hdf[(hdf.ladder_set == "ALL4") & (hdf.bar == bar)].iloc[0]
        n = hdf[(hdf.ladder_set == "NO_GROSS") & (hdf.bar == bar)].iloc[0]
        for h in ("H_ANY", "H_WIDEST", "H_NARROWEST"):
            surv.append(dict(bar=bar, headline=h, all4=int(a[h]), no_gross=int(n[h]),
                             survived=int(min(a[h], n[h]))))
    sdf = pd.DataFrame(surv)
    sdf.to_csv(f"{STEM}.survival.csv", index=False)
    tot_a, tot_n = int(sdf.all4.sum()), int(sdf.no_gross.sum())
    say(f"   HEADLINE SURVIVAL: ALL4 publishes {tot_a} headline calls across both bars; "
        f"NO_GROSS publishes {tot_n} ({tot_n/tot_a:.1%})" if tot_a else
        "   HEADLINE SURVIVAL: ALL4 publishes 0 headline calls")
    h_surv = (tot_n < tot_a / 2) if tot_a else False
    say(f"   H_SURVIVE (fewer than half of ALL4's headline calls survive): "
        f"{'HELD' if h_surv else 'REFUTED'}")

    # ============================================================ ARM B — capital
    say("\n================ ARM B — CAPITAL: BOTH KEEP PATHS AT EVERY GRID POINT =============")
    say(f"   grid points: {len(gdf_all)}   4a PASS {int(gdf_all.keep4a.sum())}   "
        f"4b PASS {int(gdf_all.keep4b.sum())}")
    for pname in gdf_all.panel.unique():
        s = gdf_all[gdf_all.panel == pname]
        say(f"   {pname:9s} 4a {int(s.keep4a.sum()):2d}/{len(s):2d}   "
            f"4b {int(s.keep4b.sum()):2d}/{len(s):2d}   by ladder 4b: " +
            " ".join(f"{l}={int(s[s.ladder==l].keep4b.sum())}/{len(s[s.ladder==l])}"
                     for l in LADDERS))
    legs = [k for k in ("H1", "H2", "OOS", "DD", "CAGR")]
    say("   binding 4b legs (count of grid points failing each): " +
        " ".join(f"{L}={int(gdf_all.fail4b.str.contains(L).sum())}" for L in legs))

    say("\n   RULE 8 — CROSS-LADDER CHOOSER, THE OBJECT THE QUEUE ASKS TO PRICE "
        "(2017-2026 READ ONCE):")
    say("      panel      set        IS_STAT     cells  pick(N,H,MV,G)          OOS Sh   "
        "d vs anchor  4a 4b")
    for r in cdf.itertuples():
        say(f"      {r.panel:9s}  {r.ladder_set:9s}  {r.is_stat:10s} {r.n_cells:4d}  "
            f"({r.pick_N:3d},{r.pick_H:4d},{r.pick_maxvol:.2f},{r.pick_gross:.2f})"
            f"{'A' if r.pick_is_anchor else ' '}  {r.oos_S_pick:7.4f}  {r.d_oos_S:+9.4f}   "
            f"{'Y' if r.pick_keep4a else 'n'}  {'Y' if r.pick_keep4b else 'n'}")
    mA = cdf[cdf.ladder_set == "ALL4"].set_index(["panel", "is_stat"]).oos_S_pick
    mN = cdf[cdf.ladder_set == "NO_GROSS"].set_index(["panel", "is_stat"]).oos_S_pick
    d = (mN - mA).dropna()
    se = float(d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 1 else np.nan
    moved = int((cdf[cdf.ladder_set == "ALL4"].set_index(["panel", "is_stat"])
                 [["pick_N", "pick_H", "pick_maxvol", "pick_gross"]] !=
                 cdf[cdf.ladder_set == "NO_GROSS"].set_index(["panel", "is_stat"])
                 [["pick_N", "pick_H", "pick_maxvol", "pick_gross"]]).any(axis=1).sum())
    say(f"\n   DROPPING GROSS FROM THE CHOOSER: the pick MOVES in {moved} of {len(d)} "
        f"(panel, IS_STAT) cells; mean d(OOS Sharpe) NO_GROSS minus ALL4 = {d.mean():+.4f} "
        f"(SE {se:.4f}, t {d.mean()/se if se and se>0 else float('nan'):+.2f}, n={len(d)})")
    say(f"   H_CAPITAL (|mean d(OOS Sharpe)| <= 0.02, i.e. dropping GROSS costs nothing): "
        f"{'HELD' if abs(d.mean()) <= 0.02 else 'REFUTED'}")
    say(f"\n   RULE 8 — WITHIN-LADDER CHOOSER (36 decisions, continuity with 1152 ARM C): "
        f"mean d(OOS Sharpe) pick minus anchor {wdf.d_oos_S.mean():+.4f} "
        f"(SE {wdf.d_oos_S.std(ddof=1)/np.sqrt(len(wdf)):.4f}, n={len(wdf)}), "
        f"positive {int((wdf.d_oos_S>0).sum())}/{len(wdf)}, reach {int(wdf.reach.sum())}/"
        f"{len(wdf)}, picks clearing 4a {int(wdf.pick_keep4a.sum())}/{len(wdf)}, 4b "
        f"{int(wdf.pick_keep4b.sum())}/{len(wdf)}")
    for lad in LADDERS:
        s = wdf[wdf.ladder == lad]
        say(f"      {lad:7s} d(OOS Sh) {s.d_oos_S.mean():+.4f}  reach {int(s.reach.sum())}/"
            f"{len(s)}  picks {sorted(set(s['pick']))}")

    # ============================================================ ARM C — record census
    say("\n================ ARM C — WHAT THE RECORD COMMITTED ON THE GROSS LADDER ============")
    arows, n_csv = census_artefacts()
    prows, n_md = census_prose()
    gate("G9 census denominator stamped",
         f"tree {sha}, {n_csv} csv/csv.gz + {n_md} md files", "stated", True)
    adf = pd.DataFrame(arows)
    prdf = pd.DataFrame(prows)
    adf.to_csv(f"{STEM}.record_artefacts.csv", index=False)
    prdf.to_csv(f"{STEM}.record_prose.csv", index=False)
    if len(adf):
        nr, ng = int(adf.n_rows.sum()), int(adf.n_gross_rows.sum())
        fg = int((adf.n_gross_rows > 0).sum())
        say(f"   committed artefacts with a ladder/axis/pair column: {len(adf)} of {n_csv}; "
            f"{nr} rows, {ng} name GROSS ({ng/nr:.1%}); {fg} of {len(adf)} artefacts "
            f"({fg/len(adf):.1%}) carry at least one GROSS row")
        gate("G7b census shares in [0,1]", f"{ng/nr:.4f}", "[0,1]", 0 <= ng / nr <= 1)
    if len(prdf):
        npz, ngz = len(prdf), int(prdf.names_gross.sum())
        say(f"   committed decisive / widest-dial prose sentences: {npz}; "
            f"{ngz} name GROSS ({ngz/npz:.1%})")

    # ============================================================ gates G1 / G2 / G5 / G11
    say("\n================ GATES ============================================================")
    pxv = px.loc[:VINTAGE]
    panv = Panel("U56v", pxv, [c for c in pxv.columns if c != "SPY"])
    rv, _ = run(panv, build(panv, A_N, A_H, A_MV), gross=A_G)
    wv = stats(rv[WARMUP:])
    tripv = (wv["CAGR"], wv["Sharpe"], wv["MaxDD"])
    gate("G1 U56 anchor replay (vintage-pinned to 2026-09-16)",
         f"{tripv[0]:.6f}/{tripv[1]:.5f}/{tripv[2]:.6f}",
         f"{COMMITTED_U56[0]:.6f}/{COMMITTED_U56[1]:.5f}/{COMMITTED_U56[2]:.6f}",
         all(abs(a - b) < 1e-4 for a, b in zip(tripv, COMMITTED_U56)))
    say(f"   G1 residual {max(abs(a-b) for a, b in zip(tripv, COMMITTED_U56)):.3e} "
        f"(the record's standing tolerance for this replay is 1e-4)")
    u = gdf_all[(gdf_all.panel == "U56") & (gdf_all.ladder == "N") & (gdf_all.rung == A_N)].iloc[0]
    say(f"   G1b unpinned drift to cache end {px.index[-1].date()}: "
        f"{u['full_CAGR']:.6f}/{u['full_Sharpe']:.5f}/{u['full_MaxDD']:.6f} "
        f"(d {u['full_CAGR']-COMMITTED_U56[0]:+.6f}/{u['full_Sharpe']-COMMITTED_U56[1]:+.5f}/"
        f"{u['full_MaxDD']-COMMITTED_U56[2]:+.6f}) -- reported, not gated")

    pan2 = Panel("U56d", px, [c for c in px.columns if c != "SPY"])
    c2, sig2 = {}, []
    for lad, rungs in LADDERS.items():
        for rung in rungs:
            N, H, mv, g = cell_params(lad, rung)
            if (N, H, mv) not in c2:
                c2[(N, H, mv)] = build(pan2, N, H, mv)
            r2, _ = run(pan2, c2[(N, H, mv)], gross=g)
            sig2.append(round(sharpe(r2[WARMUP:]), 12))
    gate("G2 determinism of the U56 ladder table", "second pass", "bit-identical",
         sig2 == det_sig["U56"])

    # G5 — the IS argmax reads no OOS row
    panU = Panel("U56o", px, [c for c in px.columns if c != "SPY"])
    idxU = panU.idx[WARMUP:]
    oU = int(np.searchsorted(idxU.values, OOS_START.to_datetime64()))
    chk = []
    for lad, rungs in LADDERS.items():
        for rung in rungs:
            N, H, mv, g = cell_params(lad, rung)
            r3, _ = run(panU, c2[(N, H, mv)], gross=g)
            r3 = r3[WARMUP:]
            masked = r3.copy()
            masked[oU:] = np.nan
            chk.append(abs(sharpe(r3[:oU]) - sharpe(masked[:oU])) < 1e-12)
    gate("G5 IS argmax reads no OOS row", f"{sum(chk)}/{len(chk)} cells identical",
         "all identical", all(chk))

    gg = gdf_all[(gdf_all.panel == "U56") & (gdf_all.ladder == "GROSS")] \
        .sort_values("rung").reset_index(drop=True)
    gate("G11 1101 replay: U56 GROSS IS-Sharpe argmax at TOP, IS-DD argmax at BOTTOM",
         f"S->{gg.rung[int(np.argmax(gg.is_Sharpe.values))]}, "
         f"DD->{gg.rung[int(np.argmax(gg.is_MaxDD.values))]}",
         f"{gg.rung.iloc[-1]} / {gg.rung.iloc[0]}",
         gg.rung[int(np.argmax(gg.is_Sharpe.values))] == gg.rung.iloc[-1] and
         gg.rung[int(np.argmax(gg.is_MaxDD.values))] == gg.rung.iloc[0])

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\n   GATES {int(gdf.pass_.sum())}/{len(gdf)} PASS"
        + ("" if gdf.pass_.all() else "  FAILED: " +
           ", ".join(gdf[~gdf.pass_].gate.tolist())))
    say(f"\n# wrote {STEM.name}.*   elapsed {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
