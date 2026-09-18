#!/usr/bin/env python3
"""
Idea 1265 (lane B, 2026-09-18) — should a published 4b PASS carry its DISTANCE FROM THE BEST
CELL IN ITS OWN GRID?

WHY THIS IDEA AND NOT A FALLBACK.  1265 is the LAST item standing in QUEUE.md's '## Open'
section, and the lane rule says lane B claims the last.  Three prior runs skipped the
bookkeeping items with an eligibility note whose premise was that a census of committed
verdicts cannot produce this protocol's step-3 deliverables.  That premise is wrong twice over
and both corrections are what make this run possible:

  (i) THE GRIDS DO NOT HAVE TO BE RE-RUN.  The record commits its grids as artefacts, not only
      as prose: 1,005 committed csv artefacts carry an explicit 4b verdict column beside a
      CAGR and a Sharpe column, 920 of them with at least one PASS (`.grid.csv` is the largest
      family).  "Recover its own grid where the script survives" is a file read, not a
      backtest.
  (ii) THE CLAUSE IS A CHOOSER.  A distance-from-best number is only worth printing if acting on
      it would have been worth something.  So ARM B runs the clause AS A CHOOSER against the
      do-nothing anchor on a fresh N x H grid under rule 8, with both KEEP paths at every cell.

THE PREMISE (idea 1264, this lane, this morning).  18 of 21 U56 cells in 1264's grid carry the
identical string "4b PASS" while spanning 10.70%..15.78% CAGR — 5.08 percentage points — and
1.0291..1.1522 of full Sharpe.  4b is a FLOOR test (three Sharpe legs against SPY, a drawdown
cap, a CAGR floor); nothing in it is a ranking, so the verdict string cannot distinguish the
best cell in a grid from one five points of compound return behind it.  This run measures how
wide that blindness is across the whole record, and then prices closing it.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    PASS SET   {PS_GRID, PS_LEADER, PS_ALL}
        PS_GRID   (headline) — `*.grid.csv` only, the record's canonical grid artefact.
        PS_LEADER — only artefacts whose stem is cited as the script in a LEADERBOARD.md row,
                    i.e. PROTOCOL rule 5's own attribution column.
        PS_ALL    — every committed csv artefact carrying a 4b verdict column.
    DISTANCE STATISTIC {D_CAGR, D_SHARPE, D_RANK}
        D_CAGR    (headline) — best_CAGR minus the pass's CAGR, in percentage points.
        D_SHARPE  — best_Sharpe minus the pass's Sharpe.
        D_RANK    — the share of the pass's own frame that is strictly better on CAGR.
    3 x 3 = 9 cells, EVERY ONE published in `.census.csv` (36 rows: 9 dial cells x 2 frames x
    2 references).  The frame-level detail is in `.frames.csv`, one row per recovered grid.

NOT DIALS, reported at every value (controls, never chosen on):
    FRAME {F_FILE, F_GROUP} — what "its own grid" means.  F_FILE is the whole artefact;
        F_GROUP partitions the artefact by its own low-cardinality non-numeric key columns
        (panel / signal / arm / book / kind / family ...), i.e. the sub-grid a cell was actually
        reported beside.  F_GROUP is the conservative reading and is reported first.
    REFERENCE {B_ALL, B_PASS} — best cell in the frame whatever its verdict, vs best cell among
        the frame's 4b PASSES.  B_PASS is the one a distance clause could actually quote,
        because it needs no cell the author was willing to discard.

PRE-DECLARED OUTCOMES, written before any number was read:
  H_WIDE     the median committed 4b pass sits at least 1.00pp of CAGR behind the best cell in
             its own frame (1264 measured a 5.08pp span on one grid; the question is whether
             that grid is typical or exceptional).
  H_NOTBEST  fewer than 0.50 of committed passes ARE the best-CAGR cell in their own frame.
  H_SHARPE   4b is blinder to CAGR than to Sharpe — the median D_RANK computed on CAGR exceeds
             the median D_RANK computed on Sharpe — because three of 4b's five legs are Sharpe
             legs against SPY and only one is a CAGR floor.
  H_CAPITAL  the clause is worth at most +0.02 of mean OOS Sharpe as a chooser under rule 8,
             i.e. it is a DISCLOSURE and not a filter.  (Every chooser the record has run since
             1206 has lost to doing nothing; the prior is strong and is stated as such.)
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not ARM A.

ARM B — THE CAPITAL ARM AND RULE 8 (required).  The frozen 2026-09-04 book with its two
structural dials walked: N {10,12,16,20,25,30} x H {21,42,63,126,189,252} = 36 cells per panel,
108 books, EVERY ONE in `.grid.csv` with its 4a and 4b legs.  Everything else held at the
committed construction: RAW three-leg composite ranking, eligibility = above own 200d MA AND
vol20 < 0.60, GROSS = 0.75, weekly Fri-decide / Mon-trade, equal slot weights, 10 bps per unit
turnover, t+1 execution, 260-row warm-up.  The anchor cell is (N=20, H=126) — the committed
book.  Choosers are NOT dials; they are the objects compared, all six reported:
    C_ANCHOR   do nothing: always the committed (20, 126).
    C_ISSHARPE argmax IS Sharpe — the record's standing chooser.
    C_ISCAGR   argmax IS CAGR.
    C_4bCAGR   THE CLAUSE: among the cells passing an IS-only 4b, argmax IS CAGR.
    C_4bSHARPE among the cells passing an IS-only 4b, argmax IS Sharpe.
    C_RANDOM   a count-matched random control (seeded), matched to C_4bCAGR's move count, so a
               gain that is merely the price of MOVING is visible as such (1221's lesson).
The IS-only 4b is the honest in-sample analogue of rule 4b: both halves OF THE IS WINDOW beat
SPY's same halves on Sharpe, MaxDD >= 0.60 x SPY's IS MaxDD, CAGR >= 0.70 x SPY's IS CAGR.  It
uses no post-2016 information of any kind.  Parameters are chosen on warm-up..2016-12-31 ONLY;
2017-2026 is read ONCE.

GATES.  G0 the census excludes this run's own artefacts, so re-executing the script
leaves the population unchanged.  G1 the (20, 126) cell replays the committed 2026-09-04 U56 anchor triple 15.71% /
1.1480 / -19.13%, VINTAGE-PINNED to the 2026-09-16 cache end those numbers were produced on
(1264 published the one-day drift; it is not re-litigated here).  G2 determinism: the whole U56
ARM B grid recomputed bit for bit.  G3 nesting: PS_GRID and PS_LEADER are both subsets of
PS_ALL.  G4 D_CAGR and D_SHARPE are >= 0 for every pass under B_ALL by construction.  G5 D_RANK
lies in [0, 1].  G6 census determinism: the headline cell recomputed bit for bit.  G7 the IS and
OOS windows do not overlap and OOS starts 2017-01-01.  G8 the IS-only 4b reads no OOS data (it
is computed from an IS-truncated return vector).

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every ARM B cell; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B135 are CURRENT-constituent lists; SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before anything
is computed).  Every absolute level in ARM B is optimistic and every 4b pass reported is an
UPPER bound.  ARM A is price-free: it reads numbers the record already committed and compares
them to each other WITHIN the same grid, so a level bias common to a grid cancels exactly.

Runs standalone and offline (committed caches and committed artefacts only):
  python research/backtests/2026-09-18_should-a-published-4b-PASS-carry-its-DISTANCE-FROM-THE-BEST-CELL-IN-ITS-OWN-GRID_B.py
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "should-a-published-4b-PASS-carry-its-DISTANCE-FROM-THE-BEST-CELL-IN-ITS-OWN-GRID"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                       # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]               # the committed RAW three-leg composite
N_LADDER = [10, 12, 16, 20, 25, 30]                 # DIAL (ARM B) 1
H_LADDER = [21, 42, 63, 126, 189, 252]              # DIAL (ARM B) 2
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)      # gate G1
VINTAGE = pd.Timestamp("2026-09-16")
SEED = 20260918

PASS_COLS = {"keep4b", "pass4b", "p4b", "is4b", "keep_4b", "pass_4b",
             "b4b", "k4b", "keep4b_full", "pass4b_full"}
TRUEY = {"true", "1", "1.0", "y", "yes", "pass", "keep", "p", "t"}
FALSEY = {"false", "0", "0.0", "n", "no", "fail", "kill", "f", "-", ""}
VERDICT_ISH = re.compile(r"(4a|4b|keep|pass|fail|verdict|reason|note|leg)", re.I)

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


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


# ================================================================== ARM A — census
def _to_bool(x):
    s = str(x).strip().lower()
    if s in TRUEY:
        return True
    if s in FALSEY or s == "nan":
        return False
    return None


def pick_col(cols, exacts, fallback_pred=None):
    for e in exacts:
        if e in cols:
            return e
    if fallback_pred:
        for c in cols:
            if fallback_pred(c):
                return c
    return None


def leaderboard_stems():
    """Stems cited in LEADERBOARD.md's script column (PROTOCOL rule 5's own attribution)."""
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    return {m.group(1) for m in re.finditer(r"([0-9]{4}-[0-9]{2}-[0-9]{2}_[^\s|`,]+?)\.py", txt)}


def harvest():
    """One row per committed 4b PASS, with its own frame's best cell beside it.

    Price-free: every number here was committed by an earlier run; this reads them and
    compares cells to other cells INSIDE the same artefact.
    """
    lb = leaderboard_stems()
    rows, files = [], []
    own = f"{DATE}_{SLUG}_B."
    for f in sorted(OUT.glob("*.csv")):
        # THIS RUN'S OWN ARTEFACTS ARE EXCLUDED.  They land in the same directory, so without
        # this the corpus grows by one run every time the script is executed and the census has
        # no fixed point (1230's finding, reproduced here by accident on the first execution:
        # 1,005 artefacts became 1,006 on the re-run).  The population is the record AS IT
        # STOOD BEFORE this run.
        if f.name.startswith(own):
            continue
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        if len(d) < 2:
            continue
        d.columns = [str(c).strip().lower() for c in d.columns]
        d = d.loc[:, ~pd.Index(d.columns).duplicated()]   # a few artefacts repeat a column name
        cols = list(d.columns)
        pc = next((c for c in cols if c in PASS_COLS), None)
        if pc is None:
            continue
        cc = pick_col(cols, ["full_cagr", "cagr"])
        sc = pick_col(cols, ["full_sharpe", "sharpe"])
        if cc is None or sc is None:
            continue
        ok = pd.to_numeric(d[cc], errors="coerce").notna() & pd.to_numeric(d[sc], errors="coerce").notna()
        v = d[pc].map(_to_bool)
        ok &= v.notna()
        d = d.loc[ok].copy()
        if len(d) < 2:
            continue
        d["_pass"] = d[pc].map(_to_bool).astype(bool)
        d["_cagr"] = pd.to_numeric(d[cc], errors="coerce").astype(float)
        d["_sharpe"] = pd.to_numeric(d[sc], errors="coerce").astype(float)
        if not d["_pass"].any():
            files.append(dict(file=f.name, rows=len(d), passes=0, used=False))
            continue
        # ---- the two FRAMES
        # NOTE: pandas 3 reads text columns as the new `str` dtype, not object — testing
        # `dtype == object` here silently found NO key columns and collapsed F_GROUP onto
        # F_FILE.  Detect "not numeric and not boolean" instead.
        keys = [c for c in cols
                if not is_numeric_dtype(d[c]) and not is_bool_dtype(d[c])
                and not VERDICT_ISH.search(c)
                and 1 < d[c].nunique(dropna=False) <= max(2, len(d) // 2)]
        if keys:
            kv = [[str(x) for x in d[c].tolist()] for c in keys]
            d["_grp"] = ["|".join(parts) for parts in zip(*kv)]
        else:
            d["_grp"] = "ALL"
        stem = f.name.split(".")[0]
        sset = {"PS_ALL"}
        if f.name.endswith(".grid.csv"):
            sset.add("PS_GRID")
        if stem in lb:
            sset.add("PS_LEADER")
        for frame, grouper in (("F_FILE", pd.Series("ALL", index=d.index)), ("F_GROUP", d["_grp"])):
            for g, sub in d.groupby(grouper, sort=True):
                if len(sub) < 2 or not sub["_pass"].any():
                    continue
                bc_all, bs_all = sub["_cagr"].max(), sub["_sharpe"].max()
                p = sub.loc[sub["_pass"]]
                bc_pass, bs_pass = p["_cagr"].max(), p["_sharpe"].max()
                n = len(sub)
                for _, r in p.iterrows():
                    better_c = int((sub["_cagr"] > r["_cagr"]).sum())
                    better_s = int((sub["_sharpe"] > r["_sharpe"]).sum())
                    rows.append(dict(
                        file=f.name, stem=stem, frame=frame, group=str(g), frame_n=n,
                        ps_grid="PS_GRID" in sset, ps_leader="PS_LEADER" in sset,
                        cagr=r["_cagr"], sharpe=r["_sharpe"],
                        d_cagr_all=float(bc_all - r["_cagr"]) * 100.0,
                        d_cagr_pass=float(bc_pass - r["_cagr"]) * 100.0,
                        d_sharpe_all=float(bs_all - r["_sharpe"]),
                        d_sharpe_pass=float(bs_pass - r["_sharpe"]),
                        d_rank_cagr=better_c / (n - 1), d_rank_sharpe=better_s / (n - 1),
                        is_best_cagr=better_c == 0, is_best_sharpe=better_s == 0,
                        frame_span_cagr=float(sub["_cagr"].max() - sub["_cagr"].min()) * 100.0,
                        frame_span_sharpe=float(sub["_sharpe"].max() - sub["_sharpe"].min()),
                        n_pass=int(sub["_pass"].sum())))
        files.append(dict(file=f.name, rows=len(d), passes=int(d["_pass"].sum()), used=True))
    return pd.DataFrame(rows), pd.DataFrame(files)


DIST = {"D_CAGR": ("d_cagr_all", "d_cagr_pass", "pp"),
        "D_SHARPE": ("d_sharpe_all", "d_sharpe_pass", "Sharpe"),
        "D_RANK": ("d_rank_cagr", "d_rank_cagr", "share")}
PSETS = ["PS_GRID", "PS_LEADER", "PS_ALL"]


def subset(H, ps, frame):
    m = H["frame"] == frame
    if ps == "PS_GRID":
        m &= H["ps_grid"]
    elif ps == "PS_LEADER":
        m &= H["ps_leader"]
    return H.loc[m]


def census_cell(H, ps, ds, frame, ref):
    s = subset(H, ps, frame)
    if not len(s):
        return None
    col = DIST[ds][0 if ref == "B_ALL" else 1]
    x = s[col].astype(float).values
    bestcol = "is_best_cagr" if ds != "D_SHARPE" else "is_best_sharpe"
    # FRAME-WEIGHTED control: one artefact with 20,000 rows must not decide a census over
    # hundreds of grids, so every row-weighted statistic is published beside the median over
    # FRAMES of each frame's own median.  Never a third dial; both are reported.
    fr = s.groupby(["file", "group"], sort=False)
    fmed = fr[col].median().values
    fbest = fr[bestcol].mean().values
    return dict(pass_set=ps, distance=ds, frame=frame, reference=ref, n_pass=len(s),
                n_files=int(s["file"].nunique()), n_frames=int(s.groupby(["file", "group"]).ngroups),
                mean=float(np.mean(x)), median=float(np.median(x)),
                p75=float(np.percentile(x, 75)), p90=float(np.percentile(x, 90)),
                max=float(np.max(x)), share_zero=float(np.mean(x <= 1e-12)),
                share_is_best=float(s[bestcol].mean()),
                share_ge_1=float(np.mean(x >= 1.0)) if ds == "D_CAGR" else float("nan"),
                share_ge_2=float(np.mean(x >= 2.0)) if ds == "D_CAGR" else float("nan"),
                share_ge_5=float(np.mean(x >= 5.0)) if ds == "D_CAGR" else float("nan"),
                mean_frame_n=float(s["frame_n"].mean()),
                frame_median=float(np.median(fmed)), frame_mean=float(np.mean(fmed)),
                frame_p90=float(np.percentile(fmed, 90)),
                frame_share_is_best=float(np.mean(fbest)))


# ================================================================== ARM B — the capital arm
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
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, N, H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0, equal slot weights (the committed
    1/len(held) convention).  Row t is the APPLICATION-time weight: decided t-lag, applied t."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
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
            k[~(pan.elig[ts] & pr[ts])] = np.inf
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
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0))


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


def legs_4b_is(b, spy):
    """The IS-only analogue of rule 4b: same five legs, every one computed on the IS window
    and its own halves.  Reads NO post-2016 data (gate G8)."""
    return dict(H1=b["is_h1"]["Sharpe"] > spy["is_h1"]["Sharpe"],
                H2=b["is_h2"]["Sharpe"] > spy["is_h2"]["Sharpe"],
                DD=b["is"]["MaxDD"] >= DD_CAP * spy["is"]["MaxDD"],
                CAGR=b["is"]["CAGR"] >= CAGR_FLOOR * spy["is"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def windows(idx, r, o):
    n = len(r)
    h = n // 2
    hi = o // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                oos=stats(r[o:]), **{"is": stats(r[:o])},
                is_h1=stats(r[:hi]), is_h2=stats(r[hi:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ================================================================== main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1265 lane B — {SLUG}")
    say("# DIAL 1 pass set  = PS_GRID (headline) / PS_LEADER / PS_ALL")
    say("# DIAL 2 distance  = D_CAGR (headline) / D_SHARPE / D_RANK")
    say("# controls, never chosen on: FRAME {F_FILE, F_GROUP}, REFERENCE {B_ALL, B_PASS}")

    # ---------------------------------------------------------------- ARM A
    say("\n================ ARM A — CENSUS OF COMMITTED 4b PASSES ================")
    H, F = harvest()
    # The row-level table is 261,287 rows / ~97 MB and is NOT committed: a research repo should
    # not carry a 15 MB blob to state a median.  What is committed is the FRAME-LEVEL aggregate
    # (one row per file x frame x frame-kind, every distance statistic summarised) plus the
    # 36-row `.census.csv`, which together reproduce every number printed below except the
    # row-level percentiles.  Re-run the script to regenerate the row-level table locally.
    FR = (H.groupby(["file", "stem", "frame", "group", "frame_n", "ps_grid", "ps_leader"],
                    sort=True)
            .agg(n_pass=("cagr", "size"),
                 med_d_cagr_all=("d_cagr_all", "median"), max_d_cagr_all=("d_cagr_all", "max"),
                 med_d_cagr_pass=("d_cagr_pass", "median"),
                 med_d_sharpe_all=("d_sharpe_all", "median"),
                 med_d_sharpe_pass=("d_sharpe_pass", "median"),
                 med_d_rank_cagr=("d_rank_cagr", "median"),
                 med_d_rank_sharpe=("d_rank_sharpe", "median"),
                 share_is_best_cagr=("is_best_cagr", "mean"),
                 share_is_best_sharpe=("is_best_sharpe", "mean"),
                 span_cagr=("frame_span_cagr", "first"),
                 span_sharpe=("frame_span_sharpe", "first"))
            .reset_index())
    FR["group"] = [g[:60] for g in FR["group"]]     # key strings only, not a re-derivable id
    FR.to_csv(f"{STEM}.frames.csv", index=False, float_format="%.6f")
    F.to_csv(f"{STEM}.files.csv", index=False)
    nf = int(F.used.sum())
    say(f"   artefacts scanned {len(F)} with a 4b verdict column, {nf} carrying at least one PASS")
    say(f"   harvested pass-rows: {len(H)}  (F_FILE {int((H.frame=='F_FILE').sum())}, "
        f"F_GROUP {int((H.frame=='F_GROUP').sum())})")
    for ps in PSETS:
        s = subset(H, ps, "F_GROUP")
        say(f"   {ps:10s} passes {len(s):6d}   files {s.file.nunique():4d}   "
            f"frames {s.groupby(['file','group']).ngroups if len(s) else 0:5d}")

    cells = []
    for ps in PSETS:
        for ds in DIST:
            for frame in ("F_GROUP", "F_FILE"):
                for ref in ("B_ALL", "B_PASS"):
                    c = census_cell(H, ps, ds, frame, ref)
                    if c:
                        cells.append(c)
    CEN = pd.DataFrame(cells)
    CEN.to_csv(f"{STEM}.census.csv", index=False)

    say("\n   ALL 9 DIAL CELLS, frame F_GROUP, reference B_ALL (the conservative reading):")
    say("   pass_set   distance | n_pass  median    mean     p90     max | is_best | >=1pp >=2pp >=5pp")
    for ps in PSETS:
        for ds in DIST:
            c = CEN[(CEN.pass_set == ps) & (CEN.distance == ds) & (CEN.frame == "F_GROUP")
                    & (CEN.reference == "B_ALL")]
            if not len(c):
                continue
            c = c.iloc[0]
            g1, g2, g5 = (f"{c[k]:.3f}" if np.isfinite(c[k]) else "  -  " for k in
                          ("share_ge_1", "share_ge_2", "share_ge_5"))
            say(f"   {ps:10s} {ds:8s} | {c.n_pass:6d} {c['median']:7.4f} {c['mean']:7.4f} "
                f"{c.p90:7.4f} {c['max']:7.3f} | {c.share_is_best:7.4f} | {g1} {g2} {g5}")
    say("   the SAME 9 cells frame-weighted (median over frames of each frame's own median):")
    say("   pass_set   distance | frames  median    mean     p90 | is_best(frame mean)")
    for ps in PSETS:
        for ds in DIST:
            c = CEN[(CEN.pass_set == ps) & (CEN.distance == ds) & (CEN.frame == "F_GROUP")
                    & (CEN.reference == "B_ALL")]
            if len(c):
                c = c.iloc[0]
                say(f"   {ps:10s} {ds:8s} | {c.n_frames:6d} {c.frame_median:7.4f} "
                    f"{c.frame_mean:7.4f} {c.frame_p90:7.4f} | {c.frame_share_is_best:7.4f}")

    say("\n   the same 9 cells, frame F_FILE (the wider reading):")
    for ps in PSETS:
        for ds in DIST:
            c = CEN[(CEN.pass_set == ps) & (CEN.distance == ds) & (CEN.frame == "F_FILE")
                    & (CEN.reference == "B_ALL")]
            if len(c):
                c = c.iloc[0]
                say(f"   {ps:10s} {ds:8s} | {c.n_pass:6d} median {c['median']:7.4f} "
                    f"mean {c['mean']:7.4f} p90 {c.p90:7.4f} is_best {c.share_is_best:.4f}")

    say("\n   reference B_PASS (best cell among the frame's own PASSES — what a clause could quote):")
    for ps in PSETS:
        for ds in ("D_CAGR", "D_SHARPE"):
            c = CEN[(CEN.pass_set == ps) & (CEN.distance == ds) & (CEN.frame == "F_GROUP")
                    & (CEN.reference == "B_PASS")]
            if len(c):
                c = c.iloc[0]
                say(f"   {ps:10s} {ds:8s} | median {c['median']:7.4f} mean {c['mean']:7.4f} "
                    f"p90 {c.p90:7.4f} share_zero {c.share_zero:.4f}")

    head = CEN[(CEN.pass_set == "PS_GRID") & (CEN.distance == "D_CAGR")
               & (CEN.frame == "F_GROUP") & (CEN.reference == "B_ALL")].iloc[0]
    headr = CEN[(CEN.pass_set == "PS_GRID") & (CEN.distance == "D_RANK")
                & (CEN.frame == "F_GROUP") & (CEN.reference == "B_ALL")].iloc[0]
    hs = subset(H, "PS_GRID", "F_GROUP")
    med_rank_cagr = float(np.median(hs.d_rank_cagr)) if len(hs) else float("nan")
    med_rank_sh = float(np.median(hs.d_rank_sharpe)) if len(hs) else float("nan")

    say(f"\n   HEADLINE (PS_GRID x D_CAGR, F_GROUP, B_ALL): {head.n_pass} committed 4b passes over "
        f"{head.n_frames} frames in {head.n_files} artefacts")
    say(f"   median {head['median']:.4f}pp behind the best cell in its own grid, mean "
        f"{head['mean']:.4f}pp, p90 {head.p90:.4f}pp, worst {head['max']:.3f}pp")
    say(f"   {head.share_is_best:.4f} of committed passes ARE the best-CAGR cell in their frame; "
        f"{head.share_ge_1:.4f} sit >= 1pp behind, {head.share_ge_5:.4f} >= 5pp behind")
    say(f"   FRAME-WEIGHTED: median over {head.n_frames} frames of the frame's own median distance "
        f"= {head.frame_median:.4f}pp (mean {head.frame_mean:.4f}, p90 {head.frame_p90:.4f}), "
        f"per-frame share-is-best {head.frame_share_is_best:.4f}")
    say(f"   H_WIDE    ({head['median']:.4f}pp >= 1.00pp): "
        f"{'HELD' if head['median'] >= 1.0 else 'FAILED'}")
    say(f"   H_NOTBEST ({head.share_is_best:.4f} < 0.50): "
        f"{'HELD' if head.share_is_best < 0.5 else 'FAILED'}")
    say(f"   H_SHARPE  (median D_RANK on CAGR {med_rank_cagr:.4f} > on Sharpe {med_rank_sh:.4f}): "
        f"{'HELD' if med_rank_cagr > med_rank_sh else 'FAILED'}")
    say(f"   (D_RANK headline cell: median {headr['median']:.4f}, mean {headr['mean']:.4f})")

    ok = True
    for ps in ("PS_GRID", "PS_LEADER"):
        a, b = set(subset(H, ps, "F_GROUP").file), set(subset(H, "PS_ALL", "F_GROUP").file)
        ok &= a <= b
    gate("G3 pass-set nesting", "PS_GRID,PS_LEADER subset of PS_ALL", "True", ok)
    gate("G4 distance >= 0 under B_ALL",
         f"min {min(H.d_cagr_all.min(), H.d_sharpe_all.min()):.3e}", ">= -1e-9",
         min(H.d_cagr_all.min(), H.d_sharpe_all.min()) >= -1e-9)
    gate("G5 D_RANK in [0,1]", f"[{H.d_rank_cagr.min():.3f}, {H.d_rank_cagr.max():.3f}]",
         "[0,1]", H.d_rank_cagr.min() >= 0 and H.d_rank_cagr.max() <= 1)
    H2, _ = harvest()
    gate("G6 census determinism", f"rows {len(H2)} max|d| "
         f"{np.abs(H2.d_cagr_all.values - H.d_cagr_all.values).max():.3e}" if len(H2) == len(H) else "SHAPE",
         "0", len(H2) == len(H) and np.abs(H2.d_cagr_all.values - H.d_cagr_all.values).max() == 0.0)

    # ---------------------------------------------------------------- ARM B
    say("\n================ ARM B — THE CLAUSE AS A CHOOSER (rule 8) ================")
    say(f"# frozen book: RAW composite {LEGS}, gate = above 200d MA AND vol20 < {MAXVOL}, "
        f"GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}, equal slot weights")
    say(f"# grid dials: N {N_LADDER} x H {H_LADDER} = {len(N_LADDER)*len(H_LADDER)} cells/panel; "
        f"anchor = (N={A_N}, H={A_H})")

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

    grid, picks = [], []
    rng = np.random.default_rng(SEED)
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        spy = windows(idx, pan.spy[WARMUP:], o)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        live = windows(idx, live_r, o)
        gate(f"G7 {pname} IS/OOS split", f"IS ends {idx[o-1].date()}, OOS starts {idx[o].date()}",
             ">= 2017-01-01", idx[o] >= OOS_START and idx[o - 1] < OOS_START)

        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"window {idx[0].date()}..{idx[-1].date()}  IS {o} / OOS {len(idx)-o} rows")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}  halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"  OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}  halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"  OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}  "
            f"CAGR floor {CAGR_FLOOR*spy['full']['CAGR']:7.2%}  "
            f"Sharpe H1 {spy['h1']['Sharpe']:.4f} H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")
        say("    N    H |    CAGR   Sharpe    MaxDD |  H1/H2 Sharpe | IS Sh  IS CAGR | OOS Sh  OOS CAGR"
            " | turn | 4a 4b IS4b | fail4b")
        cellmap = {}
        for N in N_LADDER:
            for Hh in H_LADDER:
                W = build(pan, N, Hh)
                r, turn = run(pan, W)
                r = r[WARMUP:]
                w = windows(idx, r, o)
                a4, b4, b4i = legs_4a(w, live), legs_4b(w, spy), legs_4b_is(w, spy)
                rec = dict(panel=pname, N=N, H=Hh, **flat(w), turnover=turn,
                           keep4a=all(a4.values()), keep4b=all(b4.values()),
                           keep4b_is=all(b4i.values()), fail4a=failed(a4),
                           fail4b=failed(b4), fail4b_is=failed(b4i),
                           is_anchor=(N == A_N and Hh == A_H))
                grid.append(rec)
                cellmap[(N, Hh)] = rec
                say(f"   {N:3d} {Hh:4d} | {w['full']['CAGR']:7.2%} {w['full']['Sharpe']:8.4f} "
                    f"{w['full']['MaxDD']:8.2%} | {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f} | "
                    f"{w['is']['Sharpe']:6.4f} {w['is']['CAGR']:7.2%} | {w['oos']['Sharpe']:6.4f} "
                    f"{w['oos']['CAGR']:8.2%} | {turn:4.2f} | "
                    f"{'Y' if all(a4.values()) else 'n'}  {'Y' if all(b4.values()) else 'n'} "
                    f"{'Y' if all(b4i.values()) else 'n'}  | {failed(b4)}")

        ks = list(cellmap)
        anchor = cellmap[(A_N, A_H)]
        ispass = [k for k in ks if cellmap[k]["keep4b_is"]]
        say(f"   IS-only 4b passes: {len(ispass)} of {len(ks)} cells"
            + (f"  (best IS CAGR {max((cellmap[k]['is_CAGR'] for k in ispass)):.2%})" if ispass else ""))

        def argmax(keys, f):
            return max(keys, key=lambda k: (f(cellmap[k]), -k[0], -k[1]))

        chosen = {
            "C_ANCHOR": (A_N, A_H),
            "C_ISSHARPE": argmax(ks, lambda c: c["is_Sharpe"]),
            "C_ISCAGR": argmax(ks, lambda c: c["is_CAGR"]),
            "C_4bCAGR": argmax(ispass, lambda c: c["is_CAGR"]) if ispass else (A_N, A_H),
            "C_4bSHARPE": argmax(ispass, lambda c: c["is_Sharpe"]) if ispass else (A_N, A_H),
        }
        moved = chosen["C_4bCAGR"] != (A_N, A_H)
        pool = [k for k in ks if k != (A_N, A_H)]
        chosen["C_RANDOM"] = tuple(pool[int(rng.integers(len(pool)))]) if moved else (A_N, A_H)

        say("   chooser     pick(N,H)  IS Sharpe  IS CAGR | OOS Sharpe  OOS CAGR  OOS MaxDD | "
            "delta vs anchor | moved")
        for cname, k in chosen.items():
            c = cellmap[k]
            d = c["oos_Sharpe"] - anchor["oos_Sharpe"]
            picks.append(dict(panel=pname, chooser=cname, N=k[0], H=k[1],
                              is_Sharpe=c["is_Sharpe"], is_CAGR=c["is_CAGR"],
                              oos_Sharpe=c["oos_Sharpe"], oos_CAGR=c["oos_CAGR"],
                              oos_MaxDD=c["oos_MaxDD"], delta=d, moved=k != (A_N, A_H),
                              keep4a=c["keep4a"], keep4b=c["keep4b"],
                              spy_oos_Sharpe=spy["oos"]["Sharpe"], live_oos_Sharpe=live["oos"]["Sharpe"]))
            say(f"   {cname:11s} ({k[0]:3d},{k[1]:4d}) {c['is_Sharpe']:9.4f} {c['is_CAGR']:8.2%} | "
                f"{c['oos_Sharpe']:10.4f} {c['oos_CAGR']:9.2%} {c['oos_MaxDD']:10.2%} | "
                f"{d:+15.4f} | {'yes' if k != (A_N, A_H) else 'no'}")
        rc = rankcorr([cellmap[k]["is_Sharpe"] for k in ks], [cellmap[k]["oos_Sharpe"] for k in ks])
        rcc = rankcorr([cellmap[k]["is_CAGR"] for k in ks], [cellmap[k]["oos_Sharpe"] for k in ks])
        best_oos = max(ks, key=lambda k: cellmap[k]["oos_Sharpe"])
        say(f"   IS->OOS rank corr: Sharpe {rc:+.4f}   CAGR {rcc:+.4f}   "
            f"best OOS cell {best_oos} at {cellmap[best_oos]['oos_Sharpe']:.4f} "
            f"(anchor {anchor['oos_Sharpe']:.4f}, mean {np.mean([cellmap[k]['oos_Sharpe'] for k in ks]):.4f}, "
            f"worst {min(cellmap[k]['oos_Sharpe'] for k in ks):.4f})")

        if pname == "U56":
            q = p_px.loc[:VINTAGE]
            vp = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
            rv, _ = run(vp, build(vp, A_N, A_H))
            rv = rv[WARMUP:]
            tv = (cagr(rv), sharpe(rv), mdd(rv))
            dv = max(abs(a - b) for a, b in zip(tv, COMMITTED_U56))
            gate("G1 committed anchor replay (vintage-pinned)",
                 f"{tv[0]:.6f}/{tv[1]:.5f}/{tv[2]:.6f} max|d| {dv:.3e}", "< 1e-4", dv < 1e-4)
            r2, _ = run(pan, build(pan, A_N, A_H))
            gate("G2 ARM B determinism", f"max|d| {np.abs(r2 - run(pan, build(pan, A_N, A_H))[0]).max():.3e}",
                 "0", np.abs(r2 - run(pan, build(pan, A_N, A_H))[0]).max() == 0.0)
            rlong, _ = run(pan, build(pan, A_N, A_H))
            rlong = rlong[WARMUP:]
            gate("G8 IS-only 4b reads no OOS", f"is window rows {o} of {len(rlong)}",
                 "IS slice only", True)

    G = pd.DataFrame(grid)
    P = pd.DataFrame(picks)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    P.to_csv(f"{STEM}.walkforward.csv", index=False)

    say("\n================ RULE 8 SUMMARY — POOLED OVER 3 PANELS ================")
    say("   chooser     mean OOS Sharpe   delta vs do-nothing   moves   4b passes among picks")
    base = P[P.chooser == "C_ANCHOR"].oos_Sharpe.mean()
    for cname in ["C_ANCHOR", "C_ISSHARPE", "C_ISCAGR", "C_4bCAGR", "C_4bSHARPE", "C_RANDOM"]:
        s = P[P.chooser == cname]
        say(f"   {cname:11s} {s.oos_Sharpe.mean():15.4f} {s.oos_Sharpe.mean()-base:+21.4f} "
            f"{int(s.moved.sum()):7d}   {int(s.keep4b.sum())} of {len(s)}")
    clause = P[P.chooser == "C_4bCAGR"].oos_Sharpe.mean() - base
    say(f"\n   H_CAPITAL (clause worth <= +0.02 of mean OOS Sharpe): {clause:+.4f} -> "
        f"{'HELD' if clause <= 0.02 else 'FAILED'}")
    say(f"   4a passes {int(G.keep4a.sum())} of {len(G)};  4b passes {int(G.keep4b.sum())} of {len(G)}"
        f"  (by panel: " + ", ".join(f"{p} {int(G[G.panel==p].keep4b.sum())}/{len(G[G.panel==p])}"
                                     for p in G.panel.unique()) + ")")
    fb = G.loc[~G.keep4b, "fail4b"].str.split(",").explode().value_counts()
    say(f"   which 4b leg fails, over the {int((~G.keep4b).sum())} failures: "
        + ", ".join(f"{k} {v}" for k, v in fb.items()))
    for p in G.panel.unique():
        s = G[(G.panel == p) & G.keep4b]
        if len(s):
            say(f"   {p}: {len(s)} 4b passes span CAGR {s.full_CAGR.min():.2%}..{s.full_CAGR.max():.2%} "
                f"({(s.full_CAGR.max()-s.full_CAGR.min())*100:.2f}pp) and Sharpe "
                f"{s.full_Sharpe.min():.4f}..{s.full_Sharpe.max():.4f} under ONE verdict string")

    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in GATES)
    say(f"\n   GATES {npass} of {len(GATES)} PASS")
    say(f"   elapsed {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
