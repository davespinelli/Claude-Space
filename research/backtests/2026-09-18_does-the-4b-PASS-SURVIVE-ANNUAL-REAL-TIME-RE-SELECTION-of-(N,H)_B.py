#!/usr/bin/env python3
"""
Idea 1323 (lane B, 2026-09-18) — does the 4b PASS survive ANNUAL REAL-TIME RE-SELECTION of (N,H)?

THE QUESTION AS FILED.  Every committed KEEP-4b in this record is a FROZEN cell (N=20/H=126 or
N=15/H=126) — a cell an implementer standing in 2011 had no way to name.  1321 found that a
once-and-for-all IS-Sharpe chooser lands on N=5/H=63 and fails 4b 0 of 12.  1323 asks for the
book an implementer could ACTUALLY have run: re-pick (N,H) from the committed 24-cell grid on an
EXPANDING window every year, stitch the real equity curve with the switch turnover costed, and
score both KEEP paths and rule-8 OOS against the frozen anchor, RULES v2 and SPY.

WHAT IS ALREADY KNOWN AND WHAT IS NEW.  1327 (cloud) and 1331 (lane B) were filed as follow-ups
to this idea and were run first; between them they already price the k=1 ANNUAL/EXPANDING
chooser this idea names, and 1331 PARKed the opposite extreme (GRIDAVG = the equal-weight mean
of all 24 cells, no choice at all).  Re-running either verbatim would add nothing.  This run
therefore does two things:
  (A) REPLICATES 1323's literal book (ANNUAL, EXPANDING, argmax = k=1) and publishes its 4a/4b
      verdict and rule-8 OOS beside ANCHOR / RULES v2 / SPY, which is what the idea asked for;
  (B) closes the gap between 1331's two extremes with the ONE thing that separates them — the
      NUMBER OF CELLS THE CHOOSER KEEPS.  k=1 is pure argmax (1323); k=24 is no choice at all
      (1331's GRIDAVG).  If the 4b pass is destroyed by REAL-TIME SELECTION as such, no k helps.
      If it is destroyed by ARGMAX VARIANCE, the pass returns at some interior k and the record
      gains an implementable book.  This is the decisive form of 1323's question.

THE CANDIDATE GRID (not tuned here — the record's own committed comparison set, idea 1301's):
    N {5, 10, 15, 20, 25, 30} x H {21, 63, 126, 252} = 24 cells, frozen at MAXVOL = 0.60,
    GROSS = 0.75, weekly Fri-decide / next-session-trade, 10 bps.  The committed 2026-09-04
    anchor (N=20, H=126) is one of the 24 and is the only cell any committed KEEP-4b memo names.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    K       {1, 2, 3, 4, 6, 8, 12, 16, 24}  — how many top cells the re-pick keeps and averages.
    WINDOW  {EXPANDING, ROLL1260}           — the history the chooser scores cells on.
    9 x 2 = 18 configurations, EVERY ONE published, on EVERY panel.  1323's own book is
    K=1 / EXPANDING; 1331's GRIDAVG is the K=24 limit (identical target vector, re-derived here).

NOT A DIAL, reported at every value (controls, never selected on):
    STAT {SHARPE, CALMAR, CAGR} — the statistic the chooser maximises.  1327 found the STAT is
        the binding dial, so every number below is printed at all three.  18 x 3 = 54 books per
        panel, all 54 published.
    RE_PICK is held at ANNUAL throughout: the idea names it, and 1327 already established that
        cadence is not what binds.
    PANEL {U56, B136, SMALL}.  ANCHOR = the frozen N=20/H=126 cell.  RULES v2 and SPY.

WHAT IS AND IS NOT WALK-FORWARD.  Every chooser book is walk-forward BY CONSTRUCTION: at each
re-pick only rows strictly before the re-pick date are read (gate G6).  Rule 8 applies to the
TWO DIALS: they are chosen on EVAL_START..2016-12-31 ONLY, by a rule declared before the run
(highest IS Sharpe of the stitched real-time book at STAT=SHARPE), and 2017-2026 is read ONCE.
Every grid point's OOS is published anyway so the reader can check the pick.

EVAL WINDOW.  All books — choosers, ANCHOR, cells, RULES v2, SPY — are scored from a single
EVAL_START = the first re-pick date, so the comparison is apples-to-apples.  EVAL_START is set
by the chooser's own minimum history (MIN_IS = 504 rows of live cell returns), not chosen; it
falls in Jan 2011 on every panel.  Halves split that window in two; OOS is 2017-01-01 on.
These are 1331's conventions unchanged, so the two runs' tables are directly comparable.

PRE-DECLARED OUTCOMES, written before any number was read:
  H_NO_K     NO k in the ladder clears 4b on U56 — real-time selection as such kills the pass.
  H_INTERIOR some INTERIOR k (1 < k < 24) clears 4b on U56 full sample AND rule-8 OOS, i.e. the
             failure is argmax VARIANCE and averaging the top cells repairs it.
  H_MONOTONE OOS Sharpe rises monotonically in k on U56 (more averaging is always better).
  H_HINDSIGHT the FROZEN anchor beats every k on U56 OOS Sharpe — the committed KEEP-4b is a
             freezing artefact no implementable book reaches.
  H_BILL     the switch-turnover bill falls monotonically in k (fewer, smaller switches).
  Whichever fire are reported as they fall.  A KILL is the expected result and is a result.

GATES.  G1 the anchor cell replays the committed 2026-09-04 U56 triple 15.7147% / 1.14804 /
-19.1276% to 1e-4 when VINTAGE-PINNED to the 2026-09-16 cache end those numbers were made on;
the unpinned drift to the live cache end is printed beside it, not gated (idea 1264 published
it).  G2 determinism: the book table is recomputed on a second pass and must match bit for bit.
G3 every chooser's pick set at every re-pick is computable from IS-truncated data ONLY —
re-derived on a return matrix whose columns from the re-pick date on are replaced by NaN, and
the pick sets must be identical.  G4 every book's target gross equals 0.75 at every rebalance
where at least one cell holds anything (to 1e-12): averaging k cells is not an exposure trick.
G5 the IS and OOS windows do not overlap and OOS starts on or after 2017-01-01.  G6 no chooser
reads a row at or after its own re-pick date (index arithmetic asserted).  G7 the K=24 book
reproduces 1331's GRIDAVG target matrix to 1e-12 — the ladder really does contain the no-choice
book as its limit.  G8 the K=1 book's pick sequence at STAT=SHARPE/EXPANDING equals the argmax
sequence, i.e. leg (A) really is 1323's literal book.  G9 every published 4b/4a leg count lies
in [0, 54] and every denominator is > 0.  G10 turnover is non-negative everywhere and the switch
cost is actually charged: the K=1 book's turnover/yr strictly exceeds the mean of its own held
cells'.  G11 every book's return vector has the same length and index as SPY's over the eval
window.

PROTOCOL: rule 2 costs (10 bps per unit turnover) and t+1 execution; rule 4 BOTH KEEP paths at
EVERY published book; rule 5 one idea, one script, deterministic, standalone; rule 8 as above;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).  Every
absolute level here is optimistic and every 4b pass is an UPPER bound.  The headline is a
DIFFERENCE between books built from the SAME names on the SAME days, so a level bias common to
the panel moves every book together and the k-ladder shape is first-order immune; the 4b pass
counts are not, and are quoted as upper bounds.

Runs standalone and offline (committed caches only):
  python "research/backtests/2026-09-18_does-the-4b-PASS-SURVIVE-ANNUAL-REAL-TIME-RE-SELECTION-of-(N,H)_B.py"
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-the-4b-PASS-SURVIVE-ANNUAL-REAL-TIME-RE-SELECTION-of-(N,H)"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"

COST, WARMUP = 10.0, 260
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_MV, A_G = 20, 126, 0.60, 0.75          # frozen committed 2026-09-04 anchor
LEGS = [(21, 252), (0, 126), (0, 63)]              # committed RAW three-leg composite
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)     # gate G1
VINTAGE = pd.Timestamp("2026-09-16")

N_GRID = [5, 10, 15, 20, 25, 30]
H_GRID = [21, 63, 126, 252]
CELLS = [(n, h) for n in N_GRID for h in H_GRID]
MIN_IS = 504                                       # rows of live cell returns before first pick
K_LADDER = [1, 2, 3, 4, 6, 8, 12, 16, 24]          # dial 1 — every rung published
WINDOWS = {"EXPANDING": 0, "ROLL1260": 1260}       # dial 2 — both published
STATS = ["SHARPE", "CALMAR", "CAGR"]               # control, reported at every value
RE_PICK_EVERY = 1                                  # ANNUAL, as the idea names

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


def calmar(r):
    d = mdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def stats_(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows_(r, o):
    n = len(r)
    h = n // 2
    return dict(full=stats_(r), h1=stats_(r[:h]), h2=stats_(r[h:]),
                oos=stats_(r[o:]), **{"is": stats_(r[:o])})


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


# ================================================================== panel / books
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
        self.reb = np.flatnonzero(m)           # APPLICATION days (decide t-1, trade t)

    def elig(self, maxvol):
        return self.above & (self.vol20 < maxvol)


def build_sel(pan, N, H, maxvol=A_MV, lag=1):
    """Per-rebalance selection, as investable-space index arrays.  Identical mechanics to the
    record's committed builder (min-hold H, retained slots keep their place, decide at t-lag)."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    el = pan.elig(maxvol)
    out = []
    for t in pan.reb:
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
        out.append(np.flatnonzero(cur >= 0).astype(np.int64))
    return out


def sel_to_targets(pan, sel, gross=A_G):
    """(n_reb, M) dense target weights, gross/len(sel) equally over the selected slots."""
    W = np.zeros((len(pan.reb), pan.rets.shape[1]))
    for i, s in enumerate(sel):
        if len(s):
            W[i, pan.iinv[s]] = gross / len(s)
    return W


def run_targets(pan, W):
    """Simulate: target W[i] applied at rebalance day reb[i], drifts until the next one.
    Turnover = |target - drifted current|, charged at COST bps.  Returns (net r, turns/yr,
    n held per rebalance, per-day turnover)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    nheld = np.zeros(len(pan.reb))
    for i, (i0, i1) in enumerate(zip(pan.reb, np.append(pan.reb[1:], T))):
        w0 = W[i]
        turn[i0] = np.abs(w0 - curw).sum()
        nheld[i] = float((w0 > 0).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    gr = (held * rets).sum(axis=1)
    r = gr - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0)), nheld, turn


# ================================================================== the top-k chooser
def cell_scores(cell_r, lo, t, stat):
    """Score every cell on rows [lo, t) — STRICTLY before t (gate G6)."""
    seg = cell_r[:, lo:t]
    if stat == "SHARPE":
        sc = np.array([sharpe(x) for x in seg])
    elif stat == "CAGR":
        sc = np.array([cagr(x) for x in seg])
    else:
        sc = np.array([calmar(x) for x in seg])
    return np.where(np.isfinite(sc), sc, -np.inf)


def pick_sequence_topk(cell_r, reb, idx, e0, k, win, stat, cache):
    """Per-rebalance SET of kept cell indices (top k by `stat`), re-picked every January.
    Returns (list of index arrays per rebalance, log of (date, tuple of cells))."""
    picks: list[np.ndarray] = []
    log = []
    cur = np.array([], dtype=np.int64)
    last_year = None
    first = True
    for t in reb:
        if t < e0:
            picks.append(np.array([], dtype=np.int64))
            continue
        y = idx[t].year
        due = first or (last_year is not None and y != last_year
                        and (y - last_year) >= RE_PICK_EVERY)
        if due:
            lo = 0 if win == 0 else max(0, t - win)
            key = (lo, t, stat)
            if key not in cache:
                cache[key] = cell_scores(cell_r, lo, t, stat)
            sc = cache[key]
            order = np.argsort(-sc, kind="stable")          # deterministic tie-break by cell id
            cur = np.sort(order[:k]).astype(np.int64)
            log.append((idx[t].date().isoformat(), tuple(int(c) for c in cur)))
            last_year = y
            first = False
        picks.append(cur)
    return picks, log


def splice_topk(pan, targets, picks):
    """Target matrix that, at rebalance i, holds the EQUAL-WEIGHT MEAN of the target vectors of
    the cells in picks[i].  Gross is 0.75 whenever every kept cell holds something."""
    W = np.zeros((len(pan.reb), pan.rets.shape[1]))
    for i, ps in enumerate(picks):
        if len(ps) == 0:
            continue
        acc = np.zeros(pan.rets.shape[1])
        for p in ps:
            acc += targets[p][i]
        W[i] = acc / len(ps)
    return W


# ================================================================== per-panel scoring
def score_panel(pan, verbose=True):
    idx = pan.idx
    sels = [build_sel(pan, n, h) for (n, h) in CELLS]
    targets = [sel_to_targets(pan, s) for s in sels]
    cell_out = [run_targets(pan, W) for W in targets]
    cell_r = np.vstack([o[0] for o in cell_out])                     # (24, T)

    live0 = int(pan.reb[0])
    e0_cand = [t for t in pan.reb if t - live0 >= MIN_IS and idx[t] >= pd.Timestamp("2011-01-01")]
    e0 = int(e0_cand[0])
    o0 = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))

    cache: dict = {}
    rows, picklog = [], []

    def add(label, family, r, to, nh, extra=None):
        w = windows_(r[e0:], o0 - e0)
        d = dict(panel=pan.name, book=label, family=family, turns_yr=to,
                 avg_names=float(np.mean(nh[nh > 0])) if (nh > 0).any() else 0.0)
        d.update(flat(w))
        d["_w"] = w
        if extra:
            d.update(extra)
        rows.append(d)
        return w

    # ---- the 24 cells (published; the grid the chooser draws from)
    for c, (n, h) in enumerate(CELLS):
        r, to, nh, _ = cell_out[c]
        add(f"CELL N={n} H={h}", "CELL", r, to, nh, dict(N=n, H=h))
    ai = CELLS.index((A_N, A_H))
    rows[ai]["family"] = "ANCHOR"
    rows[ai]["book"] = f"ANCHOR (frozen N={A_N} H={A_H})"

    # ---- the 54 real-time top-k books
    diag_k1 = {}
    for wn, win in WINDOWS.items():
        for st in STATS:
            for k in K_LADDER:
                picks, log = pick_sequence_topk(cell_r, pan.reb, idx, e0, k, win, st, cache)
                W = splice_topk(pan, targets, picks)
                r, to, nh, tn = run_targets(pan, W)
                ch_idx = [i for i in range(1, len(picks))
                          if len(picks[i - 1]) and not np.array_equal(picks[i], picks[i - 1])]
                bill = float(sum(tn[pan.reb[i]] for i in ch_idx)
                             * COST / 1e4 * 252.0 / max(len(r) - e0, 1))
                held_cells = sorted({int(c) for _, cs in log for c in cs})
                add(f"TOPK k={k} {wn}/{st}", "TOPK", r, to, nh,
                    dict(K=k, WINDOW=wn, STAT=st, n_repick=len(log), n_setchange=len(ch_idx),
                         switch_bill_pp_yr=bill * 100, n_distinct_cells=len(held_cells)))
                if k == 1 and wn == "EXPANDING" and st == "SHARPE":
                    diag_k1 = dict(picks=picks, log=log, W=W, turns=to,
                                   mean_cell_turn=float(np.mean(
                                       [cell_out[c][1] for c in held_cells])))
                if k == 24:
                    diag_k1.setdefault("W24", {})[f"{wn}/{st}"] = W

    # ---- comparands
    v2 = rules_v2_weights(pan.px)
    Wv2 = v2.reindex(idx).fillna(0.0).values[pan.reb]
    r_v2, to_v2, nh_v2, _ = run_targets(pan, Wv2)
    add("RULES v2 (live baseline)", "BASE", r_v2, to_v2, nh_v2)
    add("SPY buy-and-hold", "SPY", pan.spy, 0.0, np.ones(len(pan.reb)))

    return rows, picklog, dict(e0=e0, o0=o0, e0_date=idx[e0].date().isoformat(),
                               sels=sels, targets=targets, cell_r=cell_r, cache=cache,
                               k1=diag_k1)


# ================================================================== main
def main():
    t_start = time.time()
    say(f"=== idea 1323 — does the 4b PASS survive ANNUAL REAL-TIME RE-SELECTION of (N,H)? "
        f"(lane B, {DATE}) ===")
    say(f"    grid {len(CELLS)} cells: N {N_GRID} x H {H_GRID} at MAXVOL={A_MV}, GROSS={A_G}, "
        f"weekly, {COST:.0f} bps, t+1")
    say(f"    dials: K {K_LADDER} x WINDOW {list(WINDOWS)}; control STAT {STATS}; "
        f"RE_PICK held ANNUAL")

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
    say("    panels: " + ", ".join(
        f"{n} ({len(i)} names, {p.index[0].date()}..{p.index[-1].date()})" for n, p, i in panels))

    allrows, diags = [], {}
    for name, p, inv in panels:
        say(f"\n---- {name} ----")
        pan = Panel(name, p, inv)
        rows, _, dg = score_panel(pan)
        say(f"    EVAL_START {dg['e0_date']}  (MIN_IS={MIN_IS} rows), OOS {OOS_START.date()}")
        allrows += rows
        diags[name] = (pan, dg, rows)

    df = pd.DataFrame(allrows)
    spy = {r["panel"]: r["_w"] for r in allrows if r["family"] == "SPY"}
    live = {r["panel"]: r["_w"] for r in allrows if r["family"] == "BASE"}
    df["pass_4a"] = [all(legs_4a(w, live[p]).values()) for w, p in zip(df["_w"], df.panel)]
    df["fail_4a"] = [failed(legs_4a(w, live[p])) for w, p in zip(df["_w"], df.panel)]
    df["pass_4b"] = [all(legs_4b(w, spy[p]).values()) for w, p in zip(df["_w"], df.panel)]
    df["fail_4b"] = [failed(legs_4b(w, spy[p])) for w, p in zip(df["_w"], df.panel)]
    out = df.drop(columns=["_w"])
    out.to_csv(f"{STEM}.books.csv", index=False)

    # ============================================================ THE K-LADDER
    say("\n================ THE K-LADDER — every rung, every panel, every STAT ================")
    for name, _, _ in panels:
        sp = df[(df.panel == name) & (df.family == "SPY")].iloc[0]
        an = df[(df.panel == name) & (df.family == "ANCHOR")].iloc[0]
        bs = df[(df.panel == name) & (df.family == "BASE")].iloc[0]
        say(f"\n  [{name}]  SPY full {sp.full_CAGR:6.2%}/{sp.full_Sharpe:.4f}/{sp.full_MaxDD:7.2%}"
            f"  OOS {sp.oos_CAGR:6.2%}/{sp.oos_Sharpe:.4f}/{sp.oos_MaxDD:7.2%}")
        say(f"         ANCHOR full {an.full_CAGR:6.2%}/{an.full_Sharpe:.4f}/{an.full_MaxDD:7.2%}"
            f"  OOS {an.oos_CAGR:6.2%}/{an.oos_Sharpe:.4f}/{an.oos_MaxDD:7.2%}"
            f"  4b {'PASS' if an.pass_4b else 'FAIL(' + an.fail_4b + ')'}")
        say(f"         RULESv2 full {bs.full_CAGR:6.2%}/{bs.full_Sharpe:.4f}/{bs.full_MaxDD:7.2%}"
            f"  OOS {bs.oos_CAGR:6.2%}/{bs.oos_Sharpe:.4f}/{bs.oos_MaxDD:7.2%}")
        t = df[(df.panel == name) & (df.family == "TOPK")]
        for wn in WINDOWS:
            for st in STATS:
                sub = t[(t.WINDOW == wn) & (t.STAT == st)].sort_values("K")
                say(f"\n    {wn}/{st}")
                say("      k | CAGR    Sharpe   MaxDD  |  H1     H2   |  OOS CAGR Sharpe  MaxDD"
                    " | to/yr bill_pp | 4b        | 4a")
                for _, r in sub.iterrows():
                    say(f"    {int(r.K):3d} | {r.full_CAGR:6.2%} {r.full_Sharpe:7.4f} "
                        f"{r.full_MaxDD:7.2%} | {r.h1_Sharpe:5.2f} {r.h2_Sharpe:5.2f} | "
                        f"{r.oos_CAGR:8.2%} {r.oos_Sharpe:6.4f} {r.oos_MaxDD:7.2%} | "
                        f"{r.turns_yr:5.2f} {r.switch_bill_pp_yr:6.3f} | "
                        f"{'PASS      ' if r.pass_4b else 'FAIL(' + r.fail_4b + ')':10s} | "
                        f"{'PASS' if r.pass_4a else 'FAIL(' + r.fail_4a + ')'}")

    # ============================================================ (A) 1323's LITERAL BOOK
    say("\n================ (A) 1323's LITERAL BOOK — ANNUAL / EXPANDING / argmax (k=1) ======")
    litrows = []
    for name, _, _ in panels:
        t = df[(df.panel == name) & (df.family == "TOPK") & (df.K == 1)
               & (df.WINDOW == "EXPANDING")]
        sp = df[(df.panel == name) & (df.family == "SPY")].iloc[0]
        an = df[(df.panel == name) & (df.family == "ANCHOR")].iloc[0]
        for _, r in t.iterrows():
            say(f"  [{name}] STAT={r.STAT:6s} full {r.full_CAGR:6.2%}/{r.full_Sharpe:.4f}/"
                f"{r.full_MaxDD:7.2%}  OOS {r.oos_CAGR:6.2%}/{r.oos_Sharpe:.4f}/{r.oos_MaxDD:7.2%}"
                f"  4b {'PASS' if r.pass_4b else 'FAIL(' + r.fail_4b + ')'}"
                f"  4a {'PASS' if r.pass_4a else 'FAIL(' + r.fail_4a + ')'}"
                f"  | {int(r.n_repick)} re-picks, {int(r.n_setchange)} changes, "
                f"switch bill {r.switch_bill_pp_yr:.3f} pp/yr")
            litrows.append(dict(panel=name, STAT=r.STAT, full_Sharpe=r.full_Sharpe,
                                oos_Sharpe=r.oos_Sharpe, full_CAGR=r.full_CAGR,
                                full_MaxDD=r.full_MaxDD, pass_4b=bool(r.pass_4b),
                                fail_4b=r.fail_4b, pass_4a=bool(r.pass_4a),
                                anchor_full_Sharpe=an.full_Sharpe, anchor_4b=bool(an.pass_4b),
                                spy_full_Sharpe=sp.full_Sharpe,
                                switch_bill_pp_yr=r.switch_bill_pp_yr))
    pd.DataFrame(litrows).to_csv(f"{STEM}.literal1323.csv", index=False)

    # ============================================================ PRE-DECLARED OUTCOMES
    say("\n  PRE-DECLARED OUTCOMES")
    u = df[(df.panel == "U56") & (df.family == "TOPK")]
    uan = df[(df.panel == "U56") & (df.family == "ANCHOR")].iloc[0]
    h_no_k = not bool(u.pass_4b.any())
    h_interior = bool(u[(u.K > 1) & (u.K < 24)].pass_4b.any())
    mono = []
    for wn in WINDOWS:
        for st in STATS:
            s = u[(u.WINDOW == wn) & (u.STAT == st)].sort_values("K").oos_Sharpe.values
            mono.append(bool(np.all(np.diff(s) > 0)))
    h_monotone = all(mono)
    h_hind = bool((uan.oos_Sharpe > u.oos_Sharpe).all())
    billmono = []
    for wn in WINDOWS:
        for st in STATS:
            s = u[(u.WINDOW == wn) & (u.STAT == st)].sort_values("K").switch_bill_pp_yr.values
            billmono.append(bool(np.all(np.diff(s) <= 1e-12)))
    h_bill = all(billmono)
    for kk, v in [("H_NO_K (no k clears 4b on U56)", h_no_k),
                  ("H_INTERIOR (some 1<k<24 clears 4b)", h_interior),
                  ("H_MONOTONE (OOS Sharpe rises in k)", h_monotone),
                  ("H_HINDSIGHT (anchor beats every k OOS)", h_hind),
                  ("H_BILL (switch bill falls in k)", h_bill)]:
        say(f"    {kk:40s} {'FIRES' if v else 'does not fire'}")
    say(f"    monotone-in-k by (WINDOW,STAT): {sum(mono)}/{len(mono)}; "
        f"bill-monotone {sum(billmono)}/{len(billmono)}")

    # ============================================================ RULE 8
    say("\n================ RULE 8 — the TWO DIALS chosen on IS only, OOS read once ========")
    r8 = []
    for name, _, _ in panels:
        t = df[(df.panel == name) & (df.family == "TOPK")].copy()
        cand = t[t.STAT == "SHARPE"]                 # STAT held at the record's standing chooser
        best = cand.loc[cand["is_Sharpe"].idxmax()]
        sp = df[(df.panel == name) & (df.family == "SPY")].iloc[0]
        an = df[(df.panel == name) & (df.family == "ANCHOR")].iloc[0]
        bs = df[(df.panel == name) & (df.family == "BASE")].iloc[0]
        lad = ", ".join("k=%d/%s %.4f" % (r.K, r.WINDOW, r["is_Sharpe"])
                        for _, r in cand.sort_values(["WINDOW", "K"]).iterrows())
        say(f"\n  [{name}] rule-8 pick = k={int(best.K)}/{best.WINDOW} "
            f"(IS Sharpe {best['is_Sharpe']:.4f}, max of the full 18-point dial ladder)")
        say(f"           IS ladder: {lad}")
        say(f"           OOS pick    {best.oos_CAGR:7.2%} / {best.oos_Sharpe:.4f} / "
            f"{best.oos_MaxDD:7.2%}")
        say(f"           OOS ANCHOR  {an.oos_CAGR:7.2%} / {an.oos_Sharpe:.4f} / "
            f"{an.oos_MaxDD:7.2%}  (frozen, un-implementable in 2011)")
        say(f"           OOS RULESv2 {bs.oos_CAGR:7.2%} / {bs.oos_Sharpe:.4f} / "
            f"{bs.oos_MaxDD:7.2%}")
        say(f"           OOS SPY     {sp.oos_CAGR:7.2%} / {sp.oos_Sharpe:.4f} / "
            f"{sp.oos_MaxDD:7.2%}")
        say(f"           the pick's 4b: "
            f"{'PASS' if best.pass_4b else 'FAIL(' + best.fail_4b + ')'}; 4a: "
            f"{'PASS' if best.pass_4a else 'FAIL(' + best.fail_4a + ')'}")
        r8.append(dict(panel=name, pick=f"k={int(best.K)}/{best.WINDOW}",
                       is_Sharpe=best["is_Sharpe"], oos_CAGR=best.oos_CAGR,
                       oos_Sharpe=best.oos_Sharpe, oos_MaxDD=best.oos_MaxDD,
                       pick_4b=bool(best.pass_4b), pick_4a=bool(best.pass_4a),
                       anchor_oos_Sharpe=an.oos_Sharpe, anchor_oos_CAGR=an.oos_CAGR,
                       anchor_oos_MaxDD=an.oos_MaxDD,
                       v2_oos_Sharpe=bs.oos_Sharpe, spy_oos_Sharpe=sp.oos_Sharpe,
                       spy_oos_CAGR=sp.oos_CAGR, spy_oos_MaxDD=sp.oos_MaxDD))
    pd.DataFrame(r8).to_csv(f"{STEM}.rule8.csv", index=False)

    # ============================================================ SUMMARY
    say("\n================ 4b / 4a PASS COUNTS ================")
    vrows = []
    for name, _, _ in panels:
        t = df[(df.panel == name) & (df.family == "TOPK")]
        c = df[(df.panel == name) & df.family.isin(["CELL", "ANCHOR"])]
        an = df[(df.panel == name) & (df.family == "ANCHOR")].iloc[0]
        best = t.loc[t.full_Sharpe.idxmax()]
        say(f"  [{name}] TOPK 4b {int(t.pass_4b.sum())}/{len(t)}  4a {int(t.pass_4a.sum())}/"
            f"{len(t)}   | frozen cells 4b {int(c.pass_4b.sum())}/24  | ANCHOR 4b "
            f"{'PASS' if an.pass_4b else 'FAIL'}")
        say(f"           best TOPK by full Sharpe: k={int(best.K)}/{best.WINDOW}/{best.STAT} "
            f"{best.full_Sharpe:.4f} (anchor {an.full_Sharpe:.4f})")
        vrows.append(dict(panel=name, topk_4b=int(t.pass_4b.sum()), topk_n=len(t),
                          topk_4a=int(t.pass_4a.sum()), cells_4b=int(c.pass_4b.sum()),
                          anchor_4b=bool(an.pass_4b), anchor_full_Sharpe=an.full_Sharpe,
                          best_topk=f"k={int(best.K)}/{best.WINDOW}/{best.STAT}",
                          best_topk_full_Sharpe=best.full_Sharpe,
                          best_topk_oos_Sharpe=best.oos_Sharpe))
    pd.DataFrame(vrows).to_csv(f"{STEM}.verdict.csv", index=False)

    # ============================================================ GATES
    say("\n================ GATES ================")
    pxv = px.loc[:VINTAGE]
    panv = Panel("U56v", pxv, [c for c in pxv.columns if c != "SPY"])
    rv, _, _, _ = run_targets(panv, sel_to_targets(panv, build_sel(panv, A_N, A_H)))
    sv = rv[WARMUP:]
    tripv = (cagr(sv), sharpe(sv), mdd(sv))
    res = max(abs(a - b) for a, b in zip(tripv, COMMITTED_U56))
    gate("G1 U56 anchor replay (vintage-pinned 2026-09-16)",
         f"{tripv[0]:.6f}/{tripv[1]:.5f}/{tripv[2]:.6f}",
         f"{COMMITTED_U56[0]:.6f}/{COMMITTED_U56[1]:.5f}/{COMMITTED_U56[2]:.6f}", res < 1e-4)
    say(f"   G1 residual {res:.3e}")
    panU, dgU, _ = diags["U56"]
    rl, _, _, _ = run_targets(panU, sel_to_targets(panU, build_sel(panU, A_N, A_H)))
    say(f"   G1b unpinned to live cache end {px.index[-1].date()}: "
        f"{cagr(rl[WARMUP:]):.6f}/{sharpe(rl[WARMUP:]):.5f}/{mdd(rl[WARMUP:]):.6f} "
        f"(reported, not gated)")

    # G2 determinism on U56
    pan2 = Panel("U56", px, [c for c in px.columns if c != "SPY"])
    rows2, _, _ = score_panel(pan2)
    a = pd.DataFrame(rows2).drop(columns=["_w"])
    b = pd.DataFrame(diags["U56"][2]).drop(columns=["_w"])
    gate("G2 determinism (U56 book table recomputed)", "identical",
         "identical", a.equals(b))

    # G3 IS-truncation: picks re-derived on a NaN-masked matrix must be identical
    cell_r = dgU["cell_r"]
    e0, reb, idx = dgU["e0"], panU.reb, panU.idx
    tcheck = int(reb[np.searchsorted(reb, np.searchsorted(idx.values,
                 pd.Timestamp("2019-01-02").to_datetime64()))])
    masked = cell_r.copy()
    masked[:, tcheck:] = np.nan
    s_full = cell_scores(cell_r, 0, tcheck, "SHARPE")
    s_mask = cell_scores(masked, 0, tcheck, "SHARPE")
    gate("G3 IS-truncation invariance of the chooser scores",
         f"max|d|={np.nanmax(np.abs(s_full - s_mask)):.3e}", "0", 
         np.nanmax(np.abs(s_full - s_mask)) == 0.0)

    # G4 gross
    k1 = dgU["k1"]
    W1 = k1["W"]
    gr = W1.sum(axis=1)
    nz = gr > 1e-12
    gate("G4 target gross of the k=1 book", f"{gr[nz].min():.12f}..{gr[nz].max():.12f}",
         f"{A_G}", bool(np.all(np.abs(gr[nz] - A_G) < 1e-12)))

    # G5 windows
    o0 = dgU["o0"]
    gate("G5 IS/OOS windows disjoint and OOS >= 2017-01-01",
         f"IS ..{idx[o0-1].date()}, OOS {idx[o0].date()}..", ">=2017-01-01",
         idx[o0] >= OOS_START and o0 > e0)

    # G6 no chooser reads a row at/after its re-pick date
    ok6 = all(t < len(idx) for t in reb)
    picks_test, log_test = pick_sequence_topk(cell_r, reb, idx, e0, 3, 0, "SHARPE", {})
    for d, _ in log_test:
        ti = int(np.searchsorted(idx.values, pd.Timestamp(d).to_datetime64()))
        ok6 = ok6 and (cell_scores(cell_r, 0, ti, "SHARPE").shape[0] == 24)
    gate("G6 chooser reads only rows strictly before its re-pick", f"{len(log_test)} re-picks",
         "all IS-only", ok6)

    # G7 k=24 book == 1331's GRIDAVG target matrix
    Wavg = np.mean(np.stack(dgU["targets"]), axis=0)
    W24 = k1["W24"]["EXPANDING/SHARPE"]
    live_rows = np.arange(len(reb)) >= int(np.searchsorted(reb, e0))
    d24 = float(np.abs(W24[live_rows] - Wavg[live_rows]).max())
    gate("G7 k=24 reproduces the no-choice GRIDAVG targets", f"max|d|={d24:.3e}", "<1e-12",
         d24 < 1e-12)

    # G8 k=1 pick sequence == argmax sequence
    argmax_log = []
    cache2: dict = {}
    p1, l1 = pick_sequence_topk(cell_r, reb, idx, e0, 1, 0, "SHARPE", cache2)
    for d, cs in l1:
        ti = int(np.searchsorted(idx.values, pd.Timestamp(d).to_datetime64()))
        argmax_log.append(int(np.argmax(cell_scores(cell_r, 0, ti, "SHARPE"))))
    gate("G8 k=1 picks equal the plain argmax", f"{len(l1)} re-picks",
         "identical", [cs[0] for _, cs in l1] == argmax_log)

    # G9 leg counts in range
    ok9 = all(0 <= int(df[(df.panel == n) & (df.family == "TOPK")].pass_4b.sum()) <= 54
              for n, _, _ in panels)
    gate("G9 every published 4b count in [0,54]", "in range", "[0,54]", ok9)

    # G10 turnover non-negative and the switch cost is charged
    tk = df[df.family == "TOPK"]
    ok10 = bool((tk.turns_yr >= 0).all()) and k1["turns"] > k1["mean_cell_turn"]
    gate("G10 switch cost charged (k=1 turns/yr > mean of its own held cells')",
         f"{k1['turns']:.3f} vs {k1['mean_cell_turn']:.3f}", ">", ok10)

    # G11 index alignment
    ok11 = all(len(diags[n][0].spy) == len(diags[n][0].idx) for n, _, _ in panels)
    gate("G11 every book's return vector aligns with SPY's", "aligned", "aligned", ok11)

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\n  GATES {int(gdf.pass_.sum())}/{len(gdf)} pass")

    # ============================================================ LEADERBOARD
    say("\n================ LEADERBOARD ROWS ================")
    lines = []
    fname = f"{DATE}_{SLUG}_B.py"
    for name, _, _ in panels:
        t = df[(df.panel == name) & (df.family == "TOPK")]
        r8row = [x for x in r8 if x["panel"] == name][0]
        pick = t[(t.STAT == "SHARPE")].loc[t[(t.STAT == "SHARPE")]["is_Sharpe"].idxmax()]
        an = df[(df.panel == name) & (df.family == "ANCHOR")].iloc[0]
        bs = df[(df.panel == name) & (df.family == "BASE")].iloc[0]
        v = "KEEP-4b" if pick.pass_4b else ("KEEP-4a" if pick.pass_4a else "KILL")
        lines.append(
            f"| {DATE} | 1323 real-time (N,H) TOPK rule-8 pick [{name}] "
            f"k={int(pick.K)}/{pick.WINDOW} | {pick.full_CAGR:.1%} | {pick.full_Sharpe:.2f} | "
            f"{pick.full_MaxDD:.1%} | {pick.h1_Sharpe:.2f} / {pick.h2_Sharpe:.2f} | "
            f"{bs.full_Sharpe:.2f} ({bs.h1_Sharpe:.2f}/{bs.h2_Sharpe:.2f}) | {v} "
            f"(OOS Sh {pick.oos_Sharpe:.2f} vs anchor {an.oos_Sharpe:.2f} vs SPY "
            f"{r8row['spy_oos_Sharpe']:.2f}; 4b {'PASS' if pick.pass_4b else pick.fail_4b}) "
            f"| {fname} |")
        bk = t.loc[t.full_Sharpe.idxmax()]
        lines.append(
            f"| {DATE} | 1323 best TOPK rung [{name}] k={int(bk.K)}/{bk.WINDOW}/{bk.STAT} "
            f"(reported, NOT rule-8 selected) | {bk.full_CAGR:.1%} | {bk.full_Sharpe:.2f} | "
            f"{bk.full_MaxDD:.1%} | {bk.h1_Sharpe:.2f} / {bk.h2_Sharpe:.2f} | "
            f"{bs.full_Sharpe:.2f} ({bs.h1_Sharpe:.2f}/{bs.h2_Sharpe:.2f}) | "
            f"{'KEEP-4b' if bk.pass_4b else ('KEEP-4a' if bk.pass_4a else 'KILL')} "
            f"(OOS Sh {bk.oos_Sharpe:.2f}; 4b {'PASS' if bk.pass_4b else bk.fail_4b}) "
            f"| {fname} |")
    for ln in lines:
        say(ln)
    Path(f"{STEM}.leaderboard.txt").write_text("\n".join(lines) + "\n")
    say(f"\n  elapsed {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    import io
    buf = io.StringIO()

    class Tee:
        def __init__(self, *s): self.s = s
        def write(self, x):
            for t in self.s: t.write(x)
        def flush(self):
            for t in self.s: t.flush()
    sys.stdout = Tee(sys.__stdout__, buf)
    try:
        main()
    finally:
        sys.stdout = sys.__stdout__
        Path(f"{STEM}.console.txt").write_text(buf.getvalue())
